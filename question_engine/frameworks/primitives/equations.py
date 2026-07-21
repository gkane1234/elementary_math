"""One-step / two-step / multi-step linear equations — Layer 1 on numbers + variables.

**One- / two-step** use discrete upgrades (``two_step``, ``multiply_divide``,
``negative_coeff``). Catalog leaves force ``force_steps`` to ``one`` or ``two``.

**Multi-step** (``force_steps="multi"``) composes the shared expand/simplify
expression builder: each side is an unsimplified linear expression (distribute,
like terms, nesting). The equation is ``LHS = RHS``; the answer is the solved
value after simplifying both sides. Difficulty ``D`` drives an **uncapped**
linear step target::

    n_ops(D) = base_ops + floor(D / step_scale)

Defaults: ``base_ops=3``, ``step_scale=2`` → D=0→3, D=24→15, D=194→100, …
Multi-step floors at 4 ops (both sides). Expression complexity on each side
scales with ``n_ops`` (not only the equations budget slice).

**Solution complexity** (``seed_equation_solution``) also tracks equation ``D``
via ``difficulty_knobs.json`` → ``equations.solution``: small integers at low D,
larger ints / simple fractions mid-range, harder rations at high D when the
catalog allows fractions. Special-solution modes (identity / no solution) are
unchanged.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Literal

from question_engine.frameworks.difficulty_budget import DifficultyFactor, select_upgrades
from question_engine.frameworks.niceness import NicenessError
from question_engine.frameworks.primitives._algebra_render import (
    coeff_times_var,
    num_latex,
    sample_integerish,
)
from question_engine.frameworks.primitives.expand_simplify import (
    sample_linear_expression_to_simplify,
)
from question_engine.frameworks.primitives.expression_structure import (
    append_constant_to_expression,
)
from question_engine.frameworks.primitives.registry import PRIM_EQUATIONS, PrimitiveContext
from question_engine.frameworks.primitives.variables import SampledVariable

EQUATIONS_SETTINGS_SCHEMA: dict[str, Any] = {
    "force_steps": {
        "type": "enum",
        "values": ["auto", "one", "two", "multi"],
        "default": "auto",
        "description": "Force one-/two-/multi-step; auto uses difficulty upgrades.",
    },
    "allow_special_solutions": {
        "type": "enum",
        "values": ["none", "identity", "no_sol", "mixed", "auto"],
        "default": "none",
        "description": "Identity / no-solution on multi-step. Default none (unique solutions only). auto = none; use identity/no_sol/mixed to opt in.",
    },
    "clear_fractions": {
        "type": "bool",
        "default": False,
        "description": "Force LCD / fraction coefficients on multi-step.",
    },
}

_UPGRADES: tuple[DifficultyFactor, ...] = (
    DifficultyFactor("two_step", 3.0, ("structure",)),
    DifficultyFactor("multiply_divide", 1.0, ("structure",)),
    DifficultyFactor("negative_coeff", 1.5, ("structure",)),
)

# Multi-step structure upgrades (bought from leftover D after n_ops growth).
# Special solutions are NOT purchased from D — only via allow_special_solutions.
_MULTI_UPGRADES: tuple[DifficultyFactor, ...] = (
    DifficultyFactor("clear_fractions", 2.5, ("structure",)),
)

StepMode = Literal["one", "two", "multi"]
SolutionKind = Literal["unique", "identity", "no_solution"]

STEP_SCALE = 2.0

_LEFT_RIGHT_RE = re.compile(r"\\left\(([^()]*)\\right\)")


def _solution_knobs() -> dict[str, Any]:
    from question_engine.frameworks.primitives.difficulty_knobs import section

    raw = section("equations").get("solution") or {}
    return raw if isinstance(raw, dict) else {}


def seed_equation_solution(
    ctx: PrimitiveContext,
    *,
    d: float | None = None,
    exclude_zero: bool = False,
) -> Fraction:
    """Sample the unknown's value; complexity tracks equation difficulty ``D``.

    Unlike coefficient sampling (which uses the numbers budget slice), the
    solution is seeded from equation ``D`` so answers harden even when
    ``prereq_cap_numbers`` is low. Catalog constraints (``integers_only``,
    ``allow_fractions``, ``allow_negatives``) still apply. Decimals are off
    by default so answers stay exact fractions/integers.
    """
    from question_engine.frameworks.primitives.numbers import sample_number
    from question_engine.frameworks.primitives.registry import PRIM_NUMBERS

    cfg = _solution_knobs()
    eq_d = float(d if d is not None else ctx.effective_d(PRIM_EQUATIONS))
    sol_d = max(0.0, eq_d * float(cfg.get("d_scale", 1.0)))
    integers_until = float(cfg.get("integers_until_d", 5.0))
    allow_decimals = bool(cfg.get("allow_decimals", False))
    prefer_frac_from = float(cfg.get("prefer_fractions_from_d", 8.0))
    force_frac_chance = float(cfg.get("force_fraction_chance", 0.55))
    difficult_from = float(cfg.get("difficult_fractions_from_d", 16.0))

    settings = dict(ctx.settings_for(PRIM_NUMBERS))
    if not allow_decimals:
        settings["allow_decimals"] = False

    catalog_ints_only = bool(settings.get("integers_only", False))
    if not catalog_ints_only and sol_d <= integers_until:
        settings["integers_only"] = True

    fractions_ok = (
        not bool(settings.get("integers_only", False))
        and bool(settings.get("allow_fractions", True))
        and not bool(settings.get("no_fractions", False))
    )
    if (
        fractions_ok
        and sol_d >= prefer_frac_from
        and "number_profile" not in settings
        and "force_number_profile" not in settings
        and ctx.rng.random() < force_frac_chance
    ):
        settings["number_profile"] = (
            "difficult_rations" if sol_d >= difficult_from else "simple_rations"
        )

    try:
        return sample_number(
            sol_d,
            settings=settings,
            rng=ctx.rng,
            exclude_zero=exclude_zero,
        ).value
    except NicenessError:
        return sample_integerish(ctx, exclude_zero=exclude_zero).value


def _max_right_constant(solution: Fraction) -> float:
    """Reject RHS constants that are pedagogically huge for the seeded solution."""
    base = float(_solution_knobs().get("max_right_constant", 180))
    # Fractional / large solutions need a little more room for (Δa)·x.
    extra = abs(solution.numerator) + max(1, solution.denominator)
    return base * min(3.0, 1.0 + 0.08 * extra)


def _paren_inners(latex: str) -> set[str]:
    s = latex or ""
    found = {m.group(1).replace(" ", "") for m in _LEFT_RIGHT_RE.finditer(s)}
    for m in re.finditer(r"(?<!\\left)\(([^()]+)\)", s):
        found.add(m.group(1).replace(" ", ""))
    return {x for x in found if x}


def _is_numeric_atom(inner: str) -> bool:
    return bool(re.fullmatch(r"-?\d+(?:/\d+)?", inner.replace(" ", "")))


def sides_too_similar(left_latex: str, right_latex: str) -> bool:
    """True if sides are copies or near-copies (not merely sharing one factor)."""
    l = (left_latex or "").replace(" ", "")
    r = (right_latex or "").replace(" ", "")
    if not l or not r:
        return False
    if l == r:
        return True
    if l.startswith(r) or r.startswith(l):
        longer, shorter = (l, r) if len(l) >= len(r) else (r, l)
        rest = longer[len(shorter) :]
        if re.fullmatch(r"[+\-]\d+(\.\d+)?", rest):
            return True
    left_in = {p for p in _paren_inners(left_latex) if len(p) >= 2 and not _is_numeric_atom(p)}
    right_in = {p for p in _paren_inners(right_latex) if len(p) >= 2 and not _is_numeric_atom(p)}
    shared = left_in & right_in
    if not shared:
        return False
    # Short sides: any shared distribute chunk looks like a twin.
    if len(left_in) <= 2 and len(right_in) <= 2:
        return True
    # Long multi-chunk sides: only reject heavy overlap.
    union = left_in | right_in
    return len(shared) >= 3 and len(shared) / max(1, len(union)) >= 0.5


def target_n_ops(d: float) -> int:
    """Multi-step op count: ``base + floor(D / step_scale)`` (uncapped).

    With defaults ``base_ops=3``, ``step_scale=2``: D=0→3, D=24→15, D=194→100.
    """
    from question_engine.frameworks.primitives.difficulty_knobs import fget, iget

    d = max(0.0, float(d))
    scale = max(1e-9, fget("equations", "step_scale", STEP_SCALE))
    base = iget("equations", "base_ops", 3)
    return base + int(math.floor(d / scale))


def min_d_for_n_ops(n: int) -> float:
    """Inverse of ``target_n_ops`` for ``n ≥ base_ops``."""
    from question_engine.frameworks.primitives.difficulty_knobs import fget, iget

    base = iget("equations", "base_ops", 3)
    scale = max(1e-9, fget("equations", "step_scale", STEP_SCALE))
    n = max(base, int(n))
    if n <= base:
        return 0.0
    return scale * (n - base)


@dataclass(frozen=True)
class LinearEquation:
    latex: str
    text: str
    solution_latex: str
    solution: Fraction
    var_latex: str
    var_name: str
    steps: StepMode
    n_ops: int
    upgrades: tuple[str, ...]
    effective_d: float
    solution_kind: SolutionKind = "unique"


def sample_linear_equation(
    ctx: PrimitiveContext,
    *,
    force_steps: StepMode | None = None,
) -> LinearEquation:
    eff = ctx.effective_d(PRIM_EQUATIONS)
    settings = ctx.settings_for(PRIM_EQUATIONS)
    raw_force = force_steps or str(settings.get("force_steps", "auto")).strip().lower()
    if raw_force in {"one", "1", "one_step"}:
        force: StepMode | None = "one"
    elif raw_force in {"two", "2", "two_step"}:
        force = "two"
    elif raw_force in {"multi", "multi_step", "multistep", "3", "three"}:
        force = "multi"
    else:
        force = None

    if force == "multi":
        return _sample_multi(ctx, eff)

    purchased, _, _ = select_upgrades(_UPGRADES, eff, rng=ctx.rng)
    ids = {f.id for f in purchased}
    if force == "one":
        ids.discard("two_step")
    elif force == "two":
        ids.add("two_step")

    for _ in range(12):
        try:
            return _build(ctx, ids, eff)
        except (NicenessError, ValueError, ZeroDivisionError):
            if not ids:
                break
            costs = {f.id: f.cost for f in _UPGRADES}
            droppable = [i for i in ids if i != "two_step" or force != "two"]
            if not droppable:
                break
            drop = max(droppable, key=lambda i: costs.get(i, 0))
            ids.remove(drop)
            ctx.note_degraded(drop)

    return _build(ctx, {"two_step"} if force == "two" else set(), eff)


def _maybe_neg(ctx: PrimitiveContext, ids: set[str], value: Fraction) -> Fraction:
    if "negative_coeff" in ids and ctx.rng.random() < 0.45:
        return -abs(value) if value != 0 else Fraction(-1)
    if "negative_coeff" not in ids and value < 0:
        return abs(value) if value != 0 else Fraction(1)
    return value


def _build(ctx: PrimitiveContext, ids: set[str], eff: float) -> LinearEquation:
    var = ctx.sample_variable()
    solution = seed_equation_solution(ctx, d=eff, exclude_zero=False)

    two_step = "two_step" in ids
    prefer_md = "multiply_divide" in ids

    if not two_step:
        return _one_step(ctx, ids, eff, var, solution, prefer_md)
    return _two_step(ctx, ids, eff, var, solution)


def _finish(
    *,
    latex: str,
    text: str,
    solution: Fraction,
    var: SampledVariable,
    steps: StepMode,
    n_ops: int,
    upgrades: tuple[str, ...],
    eff: float,
    solution_kind: SolutionKind = "unique",
    solution_latex: str | None = None,
) -> LinearEquation:
    if solution_latex is None:
        if solution_kind == "identity":
            solution_latex = r"\text{all real numbers}"
        elif solution_kind == "no_solution":
            solution_latex = r"\text{no solution}"
        else:
            solution_latex = num_latex(solution)
    return LinearEquation(
        latex=latex,
        text=text,
        solution_latex=solution_latex,
        solution=solution,
        var_latex=var.latex,
        var_name=var.name,
        steps=steps,
        n_ops=n_ops,
        upgrades=upgrades,
        effective_d=eff,
        solution_kind=solution_kind,
    )


def _one_step(ctx, ids, eff, var, solution, prefer_md) -> LinearEquation:
    op_pool = ["add", "sub", "mul", "div"] if prefer_md else ["add", "sub"]
    if prefer_md and ctx.rng.random() < 0.55:
        op = ctx.rng.choice(["mul", "div"])
    else:
        op = ctx.rng.choice(op_pool)

    if op in {"add", "sub"}:
        a = sample_integerish(ctx, exclude_zero=True)
        a_v = _maybe_neg(ctx, ids, a.value)
        if op == "add":
            rhs = solution + a_v
            left_l = f"{var.latex} + {num_latex(a_v)}" if a_v >= 0 else (
                f"{var.latex} - {num_latex(abs(a_v))}"
            )
            left_t = f"{var.name} + {num_latex(a_v)}" if a_v >= 0 else (
                f"{var.name} - {num_latex(abs(a_v))}"
            )
        else:
            rhs = solution - a_v
            left_l = f"{var.latex} - {num_latex(a_v)}" if a_v >= 0 else (
                f"{var.latex} + {num_latex(abs(a_v))}"
            )
            left_t = f"{var.name} - {num_latex(a_v)}" if a_v >= 0 else (
                f"{var.name} + {num_latex(abs(a_v))}"
            )
        latex = f"{left_l} = {num_latex(rhs)}"
        text = f"{left_t} = {num_latex(rhs)}"
    elif op == "mul":
        a = sample_integerish(ctx, exclude_zero=True)
        a_v = _maybe_neg(ctx, ids, a.value)
        if a_v == 0 or abs(a_v) == 1:
            a_v = Fraction(-2 if a_v < 0 else 2)
        rhs = a_v * solution
        left_l = coeff_times_var(a_v, var.latex)
        left_t = coeff_times_var(a_v, var.name)
        latex = f"{left_l} = {num_latex(rhs)}"
        text = f"{left_t} = {num_latex(rhs)}"
    else:
        a = sample_integerish(ctx, exclude_zero=True, prefer_positive=True)
        a_v = abs(a.value) if a.value != 0 else Fraction(2)
        a_v = _maybe_neg(ctx, ids, a_v)
        if a_v == 0:
            a_v = Fraction(2)
        rhs = solution / a_v
        latex = f"\\frac{{{var.latex}}}{{{num_latex(a_v)}}} = {num_latex(rhs)}"
        text = f"({var.name})/({num_latex(a_v)}) = {num_latex(rhs)}"

    return _finish(
        latex=latex,
        text=text,
        solution=solution,
        var=var,
        steps="one",
        n_ops=1,
        upgrades=tuple(sorted(ids)),
        eff=eff,
    )


def _two_step(ctx, ids, eff, var, solution) -> LinearEquation:
    a = sample_integerish(ctx, exclude_zero=True)
    b = sample_integerish(ctx, exclude_zero=True)
    a_v = _maybe_neg(ctx, ids, a.value)
    b_v = _maybe_neg(ctx, ids, b.value)
    if a_v == 0:
        a_v = Fraction(2)
    rhs = a_v * solution + b_v
    left = coeff_times_var(a_v, var.latex)
    left_t = coeff_times_var(a_v, var.name)
    if b_v >= 0:
        left = f"{left} + {num_latex(b_v)}"
        left_t = f"{left_t} + {num_latex(b_v)}"
    else:
        left = f"{left} - {num_latex(abs(b_v))}"
        left_t = f"{left_t} - {num_latex(abs(b_v))}"
    latex = f"{left} = {num_latex(rhs)}"
    text = f"{left_t} = {num_latex(rhs)}"
    return _finish(
        latex=latex,
        text=text,
        solution=solution,
        var=var,
        steps="two",
        n_ops=2,
        upgrades=tuple(sorted(ids)),
        eff=eff,
    )


# --- Multi-step ---------------------------------------------------------------


def _multi_upgrade_ids(ctx: PrimitiveContext, eff: float) -> set[str]:
    settings = ctx.settings_for(PRIM_EQUATIONS)
    n_ops = target_n_ops(eff)
    # Linear spend estimate (old exponential blew up at high n_ops).
    scale = STEP_SCALE
    try:
        from question_engine.frameworks.primitives.difficulty_knobs import fget

        scale = max(1e-9, fget("equations", "step_scale", STEP_SCALE))
    except Exception:
        pass
    spent_struct = max(0.0, (n_ops - 3) * scale * 0.35)
    leftover = max(0.0, eff - spent_struct)
    purchased, _, _ = select_upgrades(_MULTI_UPGRADES, leftover, rng=ctx.rng)
    ids = {f.id for f in purchased}

    # Specials are opt-in only (default none). "auto" no longer D-purchases them.
    special = str(settings.get("allow_special_solutions", "none")).strip().lower()
    if special in {"identity"}:
        ids.add("special_identity")
    elif special in {"no_sol", "no_solution", "none_sol"}:
        ids.add("special_no_sol")
    elif special == "mixed":
        if ctx.rng.random() < 0.5:
            pass  # unique
        elif ctx.rng.random() < 0.5:
            ids.add("special_identity")
        else:
            ids.add("special_no_sol")
    # none / auto / off → unique only

    force_clear = settings.get("clear_fractions") or settings.get("force_lcd")
    if force_clear in (True, "true", "1", 1, "yes"):
        ids.add("clear_fractions")
    return ids


def _sample_multi(ctx: PrimitiveContext, eff: float) -> LinearEquation:
    # Multi-step structure tracks topic difficulty (uncapped). The equations-layer
    # budget slice alone can be tiny after number/variable spend.
    struct_d = max(float(eff), float(ctx.topic_d))
    n_ops = max(4, target_n_ops(struct_d))  # ≥4 ⇒ variables on both sides
    ids = _multi_upgrade_ids(ctx, struct_d)
    for _ in range(24):
        try:
            return _build_multi(ctx, struct_d, n_ops, ids)
        except (NicenessError, ValueError, ZeroDivisionError):
            continue
    return _build_multi(ctx, struct_d, n_ops, set())


def _nz(ctx: PrimitiveContext, *, abs_ge: int = 1) -> Fraction:
    for _ in range(16):
        v = sample_integerish(ctx, exclude_zero=True).value
        if abs(v) >= abs_ge:
            return v
    return Fraction(ctx.rng.randint(abs_ge, abs_ge + 4) * ctx.rng.choice([1, -1]))


def _lin_side(
    a: Fraction,
    b: Fraction,
    var: SampledVariable,
) -> tuple[str, str]:
    """Render ``a·var + b`` without a leading ``+``."""
    if a == 0:
        return num_latex(b), num_latex(b)
    left_l = coeff_times_var(a, var.latex)
    left_t = coeff_times_var(a, var.name)
    if b == 0:
        return left_l, left_t
    if b > 0:
        return f"{left_l} + {num_latex(b)}", f"{left_t} + {num_latex(b)}"
    return f"{left_l} - {num_latex(abs(b))}", f"{left_t} - {num_latex(abs(b))}"


def _frac_coef(ctx: PrimitiveContext) -> Fraction:
    """Small proper/improper fraction for clear-fractions upgrade."""
    den = ctx.rng.choice([2, 3, 4, 5, 6])
    num = ctx.rng.randint(1, den + 2)
    if ctx.rng.random() < 0.4:
        num = -num
    return Fraction(num, den)


def _chunks_per_side(n_ops: int) -> int:
    """How many distribute-chunks per side so structure tracks claimed ops.

    Rough classroom accounting: each chunk ≈ expand + combine (~2–3 ops), and
    both sides share the budget, plus a couple isolate steps.
    ``chunks ≈ (n_ops - 2) / 4``, capped by knobs.
    """
    from question_engine.frameworks.primitives.difficulty_knobs import iget

    max_chunks = max(1, iget("equations", "max_chunks_per_side", 40))
    n_ops = max(3, int(n_ops))
    return max(1, min(max_chunks, max(1, (n_ops - 2) // 4)))


def _split_affine_target(
    rng,
    a: Fraction,
    b: Fraction,
    n: int,
) -> list[tuple[Fraction, Fraction]]:
    """Split ``(a, b)`` into ``n`` affine summands (last absorbs the remainder)."""
    n = max(1, int(n))
    if n == 1:
        return [(Fraction(a), Fraction(b))]
    parts: list[tuple[Fraction, Fraction]] = []
    ra, rb = Fraction(a), Fraction(b)
    for _ in range(n - 1):
        ca = Fraction(rng.choice([-3, -2, -1, 1, 2, 3]))
        cb = Fraction(rng.choice([-4, -3, -2, -1, 0, 1, 2, 3, 4]))
        parts.append((ca, cb))
        ra -= ca
        rb -= cb
    parts.append((ra, rb))
    return parts


def _compose_multi_chunk_side(
    ctx: PrimitiveContext,
    *,
    a: Fraction,
    b: Fraction,
    var: SampledVariable,
    n_chunks: int,
    d: float,
) -> tuple[str, str, int]:
    """Build one equation side as a sum of distribute chunks equaling ``a·var+b``.

    Returns ``(latex, text, n_chunks_used)``.
    """
    from question_engine.frameworks.primitives.constructive import (
        AffineTarget,
        construct_affine,
        verify_affine,
    )
    from question_engine.frameworks.primitives.presentation import join_signed_display

    parts = _split_affine_target(ctx.rng, a, b, n_chunks)
    if ctx.rng.random() < 0.5:
        ctx.rng.shuffle(parts)

    terms: list[tuple[str, str, Fraction]] = []
    for i, (ca, cb) in enumerate(parts):
        # Huge remainder coeffs: render plain so prompts stay readable.
        if abs(ca) > 40 or abs(cb) > 80:
            chunk_l, chunk_t = _lin_side(ca, cb, var)
        else:
            tgt = AffineTarget(a=ca, b=cb)
            surface = construct_affine(
                ctx,
                d=min(float(d), 14.0),
                var=var,
                target=tgt,
                prefer_distribute=True,
                min_inflators=1,
            )
            if verify_affine(surface, tgt):
                chunk_l, chunk_t = surface.latex, surface.text
            else:
                chunk_l, chunk_t = _lin_side(ca, cb, var)
        # Subsequent chunks: wrap so leading minuses don't look like subtraction glue.
        if i > 0 and (
            chunk_l.lstrip().startswith("-")
            or "+" in chunk_l
            or "-" in chunk_l[1:]
        ):
            chunk_l = f"\\left({chunk_l}\\right)"
            chunk_t = f"({chunk_t})"
        terms.append((chunk_l, chunk_t, Fraction(1)))

    latex, text = join_signed_display(terms)
    return latex, text, len(parts)


def _build_multi(
    ctx: PrimitiveContext,
    eff: float,
    n_ops: int,
    ids: set[str] | None = None,
) -> LinearEquation:
    """Build a multi-step equation by composing expand/simplify expressions.

    Each side is a sum of distribute-chunks that together equal an affine
    ``Ax+B``. Higher ``n_ops`` ⇒ more chunks (real structure), not just a label.

    Op / structure gates:
      4+: variables on both sides
      higher n_ops: more chunks per side (see ``_chunks_per_side``)

    Clear-fractions only for modest ``n_ops`` (or when forced); it must not
    replace a high-op multi equation with a two-term fraction line.
    """
    ids = set(ids or ())
    var = ctx.sample_variable()
    solution = seed_equation_solution(ctx, d=eff, exclude_zero=False)
    n_ops = max(3, int(n_ops))

    # --- Special solutions (opt-in only): different surfaces, same/shifted affine ---
    if "special_identity" in ids or "special_no_sol" in ids:
        from question_engine.frameworks.primitives.constructive import (
            AffineTarget,
            construct_affine,
            verify_affine,
        )

        want_id = "special_identity" in ids and (
            "special_no_sol" not in ids or ctx.rng.random() < 0.5
        )
        a = sample_integerish(ctx, exclude_zero=True).value
        b = sample_integerish(ctx, exclude_zero=False).value
        tgt_left = AffineTarget(a=a, b=b)
        tgt_right = AffineTarget(a=a, b=b if want_id else b + _nz(ctx))
        left = construct_affine(
            ctx,
            d=eff,
            var=var,
            target=tgt_left,
            prefer_distribute=True,
            min_inflators=1,
        )
        right = construct_affine(
            ctx,
            d=eff,
            var=var,
            target=tgt_right,
            prefer_distribute=True,
            min_inflators=1,
        )
        assert verify_affine(left, tgt_left) and verify_affine(right, tgt_right)
        kind: SolutionKind = "identity" if want_id else "no_solution"
        tags = (
            "compose_simplify",
            "both_sides",
            "identity" if want_id else "no_solution",
            f"ops:{n_ops}",
        )
        latex = f"{left.latex} = {right.latex}"
        text = f"{left.text} = {right.text}"
        return _finish(
            latex=latex,
            text=text,
            solution=Fraction(0),
            var=var,
            steps="multi",
            n_ops=n_ops,
            upgrades=tags,
            eff=eff,
            solution_kind=kind,
        )

    # --- Clear fractions: modest ops only (unless forced) ---------------------
    settings = ctx.settings_for(PRIM_EQUATIONS)
    force_clear = settings.get("clear_fractions") or settings.get("force_lcd")
    forced_clear = force_clear in (True, "true", "1", 1, "yes")
    allow_clear = forced_clear or (n_ops <= 8 and ctx.rng.random() < 0.12)
    if "clear_fractions" in ids and allow_clear:
        a = _frac_coef(ctx)
        b = _frac_coef(ctx)
        if a == 0:
            a = Fraction(1, 2)
        use_both = n_ops >= 4
        if use_both:
            c = _frac_coef(ctx)
            if c == a:
                c = a + Fraction(1, 3)
            d = a * solution + b - c * solution
            left_l, left_t = _lin_side(a, b, var)
            right_l, right_t = _lin_side(c, d, var)
            tags = ("clear_fractions", "both_sides", f"ops:{n_ops}")
        else:
            rhs = a * solution + b
            left_l, left_t = _lin_side(a, b, var)
            right_l, right_t = num_latex(rhs), num_latex(rhs)
            tags = ("clear_fractions", f"ops:{n_ops}")
        latex = f"{left_l} = {right_l}"
        text = f"{left_t} = {right_t}"
        return _finish(
            latex=latex,
            text=text,
            solution=solution,
            var=var,
            steps="multi",
            n_ops=n_ops,
            upgrades=tags,
            eff=eff,
        )

    # --- Multi-chunk compose (structure scales with n_ops) --------------------
    from question_engine.frameworks.primitives.difficulty_knobs import fget

    ops_to_expr = fget("equations", "ops_to_expr_d", 0.85)
    expr_d = max(float(eff), float(max(0, n_ops - 3)) * ops_to_expr)
    n_chunks = _chunks_per_side(n_ops)

    # Seed a solvable left affine, then match right to the solution.
    left_a = sample_integerish(ctx, exclude_zero=True).value
    left_b = sample_integerish(ctx, exclude_zero=False).value
    left_l, left_t, left_chunks = _compose_multi_chunk_side(
        ctx, a=left_a, b=left_b, var=var, n_chunks=n_chunks, d=expr_d
    )

    use_both = n_ops >= 4
    tags_list = [
        "compose_simplify",
        f"ops:{n_ops}",
        f"chunks:{left_chunks}",
        f"groups:{left_chunks}",
    ]

    if use_both:
        # Distinct slope on the right; bake constant for the solution.
        max_rb = _max_right_constant(solution)
        for _ in range(16):
            delta = Fraction(ctx.rng.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, -6]))
            right_a = left_a + delta
            if right_a == 0 or right_a == left_a:
                continue
            right_b = left_a * solution + left_b - right_a * solution
            if abs(right_b) > max_rb:
                continue
            right_l, right_t, right_chunks = _compose_multi_chunk_side(
                ctx,
                a=right_a,
                b=right_b,
                var=var,
                n_chunks=n_chunks,
                d=expr_d,
            )
            if sides_too_similar(left_l, right_l):
                continue
            tags_list.extend(["both_sides", f"right_chunks:{right_chunks}"])
            break
        else:
            right_a = left_a + Fraction(2 if left_a >= 0 else -2)
            if right_a == 0:
                right_a = Fraction(3)
            right_b = left_a * solution + left_b - right_a * solution
            right_l, right_t, right_chunks = _compose_multi_chunk_side(
                ctx,
                a=right_a,
                b=right_b,
                var=var,
                n_chunks=max(1, n_chunks // 2),
                d=expr_d,
            )
            tags_list.extend(["both_sides", f"right_chunks:{right_chunks}"])
    else:
        rhs = left_a * solution + left_b
        right_l, right_t = num_latex(rhs), num_latex(rhs)

    if use_both and sides_too_similar(left_l, right_l):
        # Last resort: keep mathematically correct sides even if a bit alike.
        pass

    latex = f"{left_l} = {right_l}"
    text = f"{left_t} = {right_t}"
    return _finish(
        latex=latex,
        text=text,
        solution=solution,
        var=var,
        steps="multi",
        n_ops=n_ops,
        upgrades=tuple(tags_list),
        eff=eff,
    )


def compose_rhs_for_solution(
    ctx: PrimitiveContext,
    *,
    eff: float,
    n_ops: int,
    var: SampledVariable,
    left_a: Fraction,
    left_b: Fraction,
    solution: Fraction,
    left_latex: str = "",
    min_inflators: int = 1,
) -> tuple[str, str, int, Fraction]:
    """Build an RHS that simplifies to the affine needed for ``solution``.

    The constant is baked into the constructive target — never tacked on as a
    trailing ``+N``. Retries when the surface shares distribute chunks with LHS.
    """
    from question_engine.frameworks.primitives.constructive import (
        AffineTarget,
        construct_affine,
        verify_affine,
    )
    from question_engine.frameworks.primitives.difficulty_knobs import fget, iget

    ops_to_expr = fget("equations", "ops_to_expr_d", 0.85)
    max_inf = iget("equations", "max_side_inflators", 12)
    right_d = max(
        float(eff) * (0.55 if n_ops <= 5 else 0.85),
        float(max(0, n_ops - 3)) * ops_to_expr * 0.85,
    )
    min_inf = max(
        1,
        min(max_inf, int(min_inflators), 1 + max(0, n_ops - 4) // 6),
    )
    for attempt in range(28):
        # Prefer slopes that won't share easy common factors with left.
        delta = Fraction(
            ctx.rng.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, -6, 7, -7])
        )
        a_r = left_a + delta
        if a_r == 0:
            a_r = left_a + (Fraction(3) if delta > 0 else Fraction(-3))
        if a_r == left_a:
            continue
        target_b = left_a * solution + left_b - a_r * solution
        if abs(target_b) > _max_right_constant(solution):
            continue
        tgt = AffineTarget(a=a_r, b=target_b)
        # Slightly vary d so distribute choices diverge from the left side.
        d_try = right_d * (0.7 + 0.6 * ((attempt % 5) / 4.0))
        surface = construct_affine(
            ctx,
            d=max(0.0, d_try),
            var=var,
            target=tgt,
            prefer_distribute=True,
            min_inflators=min_inf,
        )
        if not verify_affine(surface, tgt):
            continue
        if left_latex and sides_too_similar(left_latex, surface.latex):
            continue
        n_groups = max(
            1, sum(1 for u in surface.inflators_applied if "distribute" in str(u))
        )
        return surface.latex, surface.text, n_groups, a_r

    # Fallback: clearly different simplified linear (still correct).
    a_r = left_a + Fraction(2 if left_a >= 0 else -2)
    if a_r == 0:
        a_r = Fraction(3)
    target_b = left_a * solution + left_b - a_r * solution
    latex, text = _lin_side(a_r, target_b, var)
    if left_latex and sides_too_similar(left_latex, latex):
        latex, text = _lin_side(a_r + 1, target_b - solution, var)
        a_r = a_r + 1
    return latex, text, 0, a_r
