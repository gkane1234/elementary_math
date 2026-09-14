"""SolveLinear / SolveInequality / SolveLiteral — goal-first reverse construction.

Species
-------
- **one** — one inverse operation (OpenStax EA2e §2.1–2.2 / §2.7)
- **two** — ``ax ± b = c`` (two inverse ops; §2.2–2.3 / §2.7)
- **multi** — one extra structure at low D, then sequential format unlocks
  (both sides, distribute, combine, fractions; §2.3–2.5 / §2.7)
- **literal** — isolate a specified letter in a formula (§2.6)

Pipeline
--------
1. Goal: intended solution ``x = s`` (equations) or ``x < s`` (inequalities).
2. Map D → numeric_tier then format_tier (see ``skeleton_difficulty``).
3. Reverse-apply allowed transforms to build ``LHS rel RHS``.
4. Inequalities: multiplying/dividing by a negative **flips** the displayed
   relation so the answer relation stays the seeded goal.
5. Literals: reverse-isolate a named formula for a target letter.

Difficulty
----------
Numeric hardness (coeff size, negatives) before format (distribute, both
sides, combine like terms, fractions, nested inflate). **D=0 multi-step is
simple**: ``2(x+1)=8`` *or* ``3x+2=x+8`` — not nested distribute + both
sides + fractions at once. Inequality D=0 does not require a direction flip.
Literal D=0 is one-step isolate (``d=rt`` for ``t``), not nested formulas.

Opt-out
-------
Equations: ``use_sample_linear_equation=True`` / ``use_solve_linear_skeleton=False``.
Inequalities: ``use_sample_linear_inequality=True`` / ``use_solve_inequality_skeleton=False``.
Literals: ``use_sample_literal_equation=True`` / ``use_solve_literal_skeleton=False``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Literal

from question_engine.frameworks.primitives._algebra_render import (
    coeff_times_var,
    join_signed_terms,
    num_latex,
    sample_integerish,
)
from question_engine.frameworks.primitives.openstax_form_catalogs import (
    catalog_form_meta,
    load_form_catalog,
)
from question_engine.frameworks.primitives.registry import PRIM_EQUATIONS, PRIM_NUMBERS, PrimitiveContext
from question_engine.frameworks.primitives.skeleton_difficulty import SkeletonDifficultyBands
from question_engine.frameworks.primitives.variables import SampledVariable

Species = Literal["one", "two", "multi"]
SolutionKind = Literal["unique", "identity", "no_solution"]
SkeletonKind = Literal["eq", "ineq"]
IneqOp = Literal["<", ">", "\\le", "\\ge"]

CATALOG_NAME = "algebra1_linear_equations"

# form_id → construction knobs (OpenStax EA2e Ch. 2 / §2.7).
_FORM_KNOBS: dict[str, dict[str, Any]] = {
    "one_step_add_sub": {"species": "one", "ops": ("add", "sub")},
    "one_step_mul_div": {"species": "one", "ops": ("mul", "div")},
    "two_step": {"species": "two"},
    "vars_both_sides": {"species": "multi", "require_both_sides": True},
    "multi_step_distribute": {"species": "multi", "require_distribute": True},
    "fraction_or_decimal_coeffs": {
        "species": "multi",
        "require_fractions": True,
    },
    "one_step_ineq_add_sub": {"species": "one", "ops": ("add", "sub")},
    "one_step_ineq_mul_div": {"species": "one", "ops": ("mul", "div")},
    "two_step_ineq": {"species": "two"},
    "vars_both_sides_ineq": {"species": "multi", "require_both_sides": True},
    "multi_step_ineq_distribute": {"species": "multi", "require_distribute": True},
    "fraction_ineq": {"species": "multi", "require_fractions": True},
    "literal_equation": {"species": "one", "literal": True},
}

_EQ_TO_INEQ_FORM = {
    "one_step_add_sub": "one_step_ineq_add_sub",
    "one_step_mul_div": "one_step_ineq_mul_div",
    "two_step": "two_step_ineq",
    "vars_both_sides": "vars_both_sides_ineq",
    "multi_step_distribute": "multi_step_ineq_distribute",
    "fraction_or_decimal_coeffs": "fraction_ineq",
}

_INEQ_OPS: tuple[IneqOp, ...] = ("<", ">", "\\le", "\\ge")
_OP_TEXT = {"<": "<", ">": ">", "\\le": "<=", "\\ge": ">="}
_OP_FLIP: dict[str, str] = {"<": ">", ">": "<", "\\le": "\\ge", "\\ge": "\\le"}
_OP_FOR_NUMBER_LINE = {"\\le": "\\leq", "\\ge": "\\geq"}
_LEGACY_EQ_PATTERNS = {
    "equations",
    "hand",
    "constructive",
    "Constructive",
    "sample_linear_equation",
    "legacy",
}
_LEGACY_INEQ_PATTERNS = {
    "inequalities",
    "hand",
    "constructive",
    "Constructive",
    "sample_linear_inequality",
    "legacy",
}
_LEGACY_LIT_PATTERNS = {
    "literal",
    "hand",
    "constructive",
    "sample_literal_equation",
    "legacy",
}


@dataclass(frozen=True)
class SolveLinearKnobs:
    """Numeric-then-format box for one reverse-construction draw."""

    species: Species
    numeric_tier: int
    format_tier: int
    addend_hi: int
    mul_hi: int
    sol_hi: int
    allow_neg: bool
    allow_div_form: bool
    allow_fraction_coeffs: bool
    allow_fraction_solution: bool
    allow_decimals: bool
    allow_distribute: bool
    allow_both_sides: bool
    allow_combine: bool
    allow_nested: bool
    ops: tuple[str, ...] = ()
    require_distribute: bool = False
    require_both_sides: bool = False
    require_fractions: bool = False


@dataclass(frozen=True)
class SolveLinearResult:
    latex: str
    text: str
    solution_latex: str
    solution: Fraction
    var_latex: str
    var_name: str
    steps: Species
    n_ops: int
    upgrades: tuple[str, ...]
    effective_d: float
    solution_kind: SolutionKind
    form_id: str | None
    transforms: tuple[str, ...]
    metadata: dict[str, Any] = field(default_factory=dict)
    leading: Fraction = Fraction(1)
    relation: str = "="
    op: str = "="
    flipped: bool = False

    def debug_dict(self) -> dict[str, Any]:
        pat = "SolveInequality" if self.op != "=" else "SolveLinear"
        return {
            "pattern": pat,
            "species": self.steps,
            "form_id": self.form_id,
            "n_ops": self.n_ops,
            "transforms": list(self.transforms),
            "flipped": self.flipped,
            **self.metadata,
        }

    @property
    def solution_value(self) -> Fraction:
        """Boundary value (alias for number-line wiring)."""
        return self.solution

    @property
    def number_line_op(self) -> str:
        return _OP_FOR_NUMBER_LINE.get(self.op, self.op)


def use_solve_linear_skeleton(settings: dict[str, Any] | None) -> bool:
    """SolveLinear is the live default for one-/two-/multi-step leaves."""
    s = dict(settings or {})
    if bool(s.get("use_sample_linear_equation")) or bool(
        s.get("use_legacy_equations")
    ):
        return False
    pat = str(s.get("skeleton_pattern", "")).strip()
    if pat in _LEGACY_EQ_PATTERNS:
        return False
    if "use_solve_linear_skeleton" in s:
        return bool(s.get("use_solve_linear_skeleton"))
    if pat in {"SolveLinear", "solve_linear"}:
        return True
    return True


def use_solve_inequality_skeleton(settings: dict[str, Any] | None) -> bool:
    """SolveInequality is the live default for one-/two-/multi-step inequalities."""
    s = dict(settings or {})
    if bool(s.get("use_sample_linear_inequality")) or bool(
        s.get("use_legacy_inequalities")
    ):
        return False
    pat = str(s.get("skeleton_pattern", "")).strip()
    if pat in _LEGACY_INEQ_PATTERNS:
        return False
    if "use_solve_inequality_skeleton" in s:
        return bool(s.get("use_solve_inequality_skeleton"))
    if pat in {"SolveInequality", "solve_inequality", "SolveLinear"}:
        return True
    return True


def use_solve_literal_skeleton(settings: dict[str, Any] | None) -> bool:
    """SolveLiteral is the live default for ``literal_equations``."""
    s = dict(settings or {})
    if bool(s.get("use_sample_literal_equation")) or bool(
        s.get("use_legacy_literals")
    ):
        return False
    pat = str(s.get("skeleton_pattern", "")).strip()
    if pat in _LEGACY_LIT_PATTERNS:
        return False
    if "use_solve_literal_skeleton" in s:
        return bool(s.get("use_solve_literal_skeleton"))
    if pat in {"SolveLiteral", "solve_literal", "SolveLinear"}:
        return True
    return True


def knobs_from_form_id(form_id: str | None) -> dict[str, Any]:
    fid = str(form_id or "").strip()
    return dict(_FORM_KNOBS.get(fid) or {})


def solve_linear_knobs(
    d: float,
    species: Species,
    *,
    settings: dict[str, Any] | None = None,
    form_id: str | None = None,
    integers_only: bool = True,
) -> SolveLinearKnobs:
    """Map D → numeric-then-format knobs; form_id may force a shape."""
    bands = SkeletonDifficultyBands.from_d(d)
    nt = bands.numeric_tier
    ft = bands.format_tier
    s = dict(settings or {})
    ints_only = bool(integers_only or s.get("integers_only"))
    addend_hi = (4, 9, 16, 28, 40)[nt]
    mul_hi = (4, 6, 8, 10, 12)[nt]
    sol_hi = (6, 9, 12, 16, 24)[nt]
    allow_neg = nt >= 1
    allow_frac = (not ints_only) and ft >= 3
    allow_dec = (not ints_only) and ft >= 4
    form = knobs_from_form_id(form_id)

    if species == "one":
        ops = tuple(form.get("ops") or ())
        return SolveLinearKnobs(
            species="one",
            numeric_tier=nt,
            format_tier=ft,
            addend_hi=addend_hi,
            mul_hi=mul_hi,
            sol_hi=sol_hi,
            allow_neg=allow_neg,
            allow_div_form=ft >= 1 or (ops == ("mul", "div")),
            allow_fraction_coeffs=allow_frac,
            allow_fraction_solution=nt >= 3 and not ints_only,
            allow_decimals=allow_dec,
            allow_distribute=False,
            allow_both_sides=False,
            allow_combine=False,
            allow_nested=False,
            ops=ops,
        )
    if species == "two":
        return SolveLinearKnobs(
            species="two",
            numeric_tier=nt,
            format_tier=ft,
            addend_hi=addend_hi,
            mul_hi=mul_hi,
            sol_hi=sol_hi,
            allow_neg=allow_neg,
            allow_div_form=False,
            allow_fraction_coeffs=allow_frac,
            allow_fraction_solution=nt >= 3 and not ints_only,
            allow_decimals=allow_dec,
            allow_distribute=False,
            allow_both_sides=False,
            allow_combine=False,
            allow_nested=False,
            ops=(),
        )

    # Multi: one extra structure at format_tier 0; unlock sequentially.
    return SolveLinearKnobs(
        species="multi",
        numeric_tier=nt,
        format_tier=ft,
        addend_hi=addend_hi,
        mul_hi=mul_hi,
        sol_hi=sol_hi,
        allow_neg=allow_neg,
        allow_div_form=False,
        allow_fraction_coeffs=allow_frac or bool(form.get("require_fractions")),
        allow_fraction_solution=nt >= 3 and not ints_only,
        allow_decimals=allow_dec,
        allow_distribute=True,
        allow_both_sides=True,
        allow_combine=ft >= 1,
        allow_nested=ft >= 4 or (ft >= 3 and ints_only),
        ops=(),
        require_distribute=bool(form.get("require_distribute")),
        require_both_sides=bool(form.get("require_both_sides")),
        require_fractions=bool(form.get("require_fractions")),
    )


def _integers_only(ctx: PrimitiveContext) -> bool:
    nums = ctx.settings_for(PRIM_NUMBERS)
    top = getattr(ctx, "settings", None) or {}
    eq = ctx.settings_for(PRIM_EQUATIONS)
    return bool(
        nums.get("integers_only")
        or top.get("integers_only")
        or eq.get("integers_only")
    )


def _top_settings(ctx: PrimitiveContext) -> dict[str, Any]:
    return dict(getattr(ctx, "settings", None) or {})


def _leaf_id(ctx: PrimitiveContext) -> str:
    return str(getattr(ctx, "leaf_id", None) or _top_settings(ctx).get("leaf_id") or "")


def _parse_species(
    force_steps: str | None,
    ctx: PrimitiveContext,
) -> Species:
    raw = (force_steps or "").strip().lower()
    if not raw:
        raw = str(ctx.settings_for(PRIM_EQUATIONS).get("force_steps") or "").strip().lower()
    if not raw or raw in {"auto", "none"}:
        leaf = _leaf_id(ctx)
        if "one_step" in leaf:
            return "one"
        if "two_step" in leaf:
            return "two"
        if "multi_step" in leaf or "multi" in leaf:
            return "multi"
        return "one"
    if raw in {"one", "1", "one_step"}:
        return "one"
    if raw in {"two", "2", "two_step"}:
        return "two"
    return "multi"


def _nz_int(
    rng,
    hi: int,
    *,
    lo: int = 1,
    allow_neg: bool = False,
    not_one: bool = False,
    ctx: PrimitiveContext | None = None,
) -> Fraction:
    hi = max(lo, int(hi))
    lo = max(1, int(lo))
    if not_one and hi == 1:
        hi = 2
    if ctx is not None:
        try:
            n = sample_integerish(ctx, exclude_zero=True, prefer_positive=not allow_neg)
            mag = abs(int(n.value))
            mag = max(lo, min(hi, mag if mag else lo))
            if not_one and mag == 1:
                mag = min(hi, 2) if hi >= 2 else 2
            v = mag
            if allow_neg and ctx.rng.random() < 0.4:
                v = -v
            return Fraction(v)
        except Exception:
            pass
    for _ in range(24):
        v = rng.randint(lo, hi)
        if not_one and v == 1:
            continue
        if allow_neg and rng.random() < 0.4:
            v = -v
        if v != 0:
            return Fraction(v)
    v = hi if not not_one else max(2, hi)
    return Fraction(-v if allow_neg else v)


def _sample_solution(rng, knobs: SolveLinearKnobs) -> Fraction:
    s = _nz_int(rng, knobs.sol_hi, allow_neg=knobs.allow_neg)
    if knobs.allow_fraction_solution and rng.random() < 0.35:
        den = rng.choice([2, 3, 4, 5])
        return Fraction(int(s), den)
    return s


def _affine_lt(a: Fraction, b: Fraction, var: SampledVariable) -> tuple[str, str]:
    parts: list[tuple[Fraction, str]] = []
    if a != 0:
        parts.append((a, var.latex))
    if b != 0:
        parts.append((b, ""))
    if not parts:
        return "0", "0"
    return join_signed_terms(parts)


def _paren_inner(inner_l: str, inner_t: str, *, heavy: bool) -> tuple[str, str]:
    if heavy:
        return f"\\left({inner_l}\\right)", f"({inner_t})"
    return f"({inner_l})", f"({inner_t})"


def _scaled_paren(
    k: Fraction,
    inner_l: str,
    inner_t: str,
    *,
    heavy: bool,
) -> tuple[str, str]:
    body_l, body_t = _paren_inner(inner_l, inner_t, heavy=heavy)
    if k == 1:
        return body_l, body_t
    if k == -1:
        return f"-{body_l}", f"-{body_t}"
    kl = num_latex(k)
    return f"{kl}{body_l}", f"{kl}{body_t}"


def _eq(left_l: str, left_t: str, right_l: str, right_t: str) -> tuple[str, str]:
    return f"{left_l} = {right_l}", f"{left_t} = {right_t}"


def _swap_rel(latex: str, text: str, rel: str) -> tuple[str, str]:
    if rel == "=":
        return latex, text
    rel_t = _OP_TEXT.get(rel, rel)
    return latex.replace(" = ", f" {rel} ", 1), text.replace(" = ", f" {rel_t} ", 1)


def _flip_op(op: str) -> str:
    return _OP_FLIP.get(op, op)


def _pick_ineq_op(rng) -> IneqOp:
    return rng.choice(_INEQ_OPS)


def _solution_latex(kind: SolutionKind, solution: Fraction) -> str:
    if kind == "identity":
        return r"\text{all real numbers}"
    if kind == "no_solution":
        return r"\text{no solution}"
    return num_latex(solution)


def _catalog_meta(form_id: str | None) -> dict[str, Any]:
    if not form_id:
        return {}
    try:
        catalog = load_form_catalog(CATALOG_NAME)
    except FileNotFoundError:
        return {"form_id": form_id, "openstax_form": form_id}
    for f in catalog.get("forms") or []:
        if str(f.get("form_id")) == form_id:
            return catalog_form_meta(f, catalog)
    return {"form_id": form_id, "openstax_form": form_id}


def _finish(
    *,
    latex: str,
    text: str,
    solution: Fraction,
    var: SampledVariable,
    steps: Species,
    n_ops: int,
    upgrades: tuple[str, ...],
    eff: float,
    form_id: str | None,
    transforms: tuple[str, ...],
    knobs: SolveLinearKnobs,
    solution_kind: SolutionKind = "unique",
    extra_meta: dict[str, Any] | None = None,
    leading: Fraction = Fraction(1),
    kind: SkeletonKind = "eq",
    answer_op: str = "=",
    rhs: Fraction | None = None,
) -> SolveLinearResult:
    flipped = bool(kind == "ineq" and leading < 0)
    relation = "="
    op = "="
    pattern = "SolveLinear"
    if kind == "ineq":
        pattern = "SolveInequality"
        op = answer_op if answer_op != "=" else "<"
        relation = _flip_op(op) if flipped else op
        latex, text = _swap_rel(latex, text, relation)
        form_id = _EQ_TO_INEQ_FORM.get(str(form_id or ""), form_id)
        sol_body = _solution_latex("unique", solution)
        solution_latex = f"{var.latex} {op} {sol_body}"
    else:
        solution_latex = _solution_latex(solution_kind, solution)
    cat = _catalog_meta(form_id)
    extra = dict(extra_meta or {})
    if rhs is not None:
        extra.setdefault("rhs", str(rhs))
    meta = {
        "skeleton_pattern": pattern,
        "species": steps,
        "numeric_tier": knobs.numeric_tier,
        "format_tier": knobs.format_tier,
        "transforms": list(transforms),
        "n_ops": n_ops,
        "steps": steps,
        "leading": str(leading),
        "relation": relation,
        "flipped": flipped,
        **cat,
        **extra,
    }
    if form_id and not meta.get("form_id"):
        meta["form_id"] = form_id
        meta["openstax_form"] = form_id
    if kind == "ineq":
        meta["construction"] = "reverse_skeleton"
        meta["skeleton_pattern"] = "SolveInequality"
    return SolveLinearResult(
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
        solution_kind=solution_kind if kind == "eq" else "unique",
        form_id=str(meta.get("form_id") or form_id or "") or None,
        transforms=transforms,
        metadata=meta,
        leading=leading,
        relation=relation,
        op=op,
        flipped=flipped,
    )


def _one_step(
    ctx: PrimitiveContext,
    knobs: SolveLinearKnobs,
    var: SampledVariable,
    solution: Fraction,
    eff: float,
    *,
    kind: SkeletonKind = "eq",
    answer_op: str = "=",
) -> SolveLinearResult:
    rng = ctx.rng
    force_neg = bool(_top_settings(ctx).get("force_negative_coeff")) and knobs.allow_neg
    ops = list(knobs.ops) if knobs.ops else ["add", "sub", "mul"]
    if knobs.allow_div_form and "div" not in ops:
        ops.append("div")
    if knobs.format_tier == 0 and not knobs.ops:
        # OpenStax §2.1–2.2: add/sub *or* mul; no x/a=b yet.
        op = rng.choice(["add", "sub", "mul", "mul"])
        ops = [op]
    if force_neg:
        ops = ["mul"]
    if knobs.allow_fraction_coeffs and rng.random() < 0.45:
        op = "mul"
        den = rng.choice([2, 3, 4, 5])
        num = rng.choice([1, 2, 3, 4, 5])
        a = Fraction(num, den)
        if a == 1 or a == 0:
            a = Fraction(3, 4)
        if force_neg or (knobs.allow_neg and rng.random() < 0.35):
            a = -abs(a)
        rhs = a * solution
        left_l = coeff_times_var(a, var.latex)
        left_t = coeff_times_var(a, var.name)
        latex, text = _eq(left_l, left_t, num_latex(rhs), num_latex(rhs))
        return _finish(
            latex=latex,
            text=text,
            solution=solution,
            var=var,
            steps="one",
            n_ops=1,
            upgrades=("one_step", "fraction_coeff"),
            eff=eff,
            form_id="one_step_mul_div",
            transforms=("mul",),
            knobs=knobs,
            leading=a,
            kind=kind,
            answer_op=answer_op,
            rhs=rhs,
        )
    op = rng.choice(ops)
    if op in {"add", "sub"}:
        a = _nz_int(rng, knobs.addend_hi, allow_neg=False)
        if op == "sub" or (knobs.allow_neg and rng.random() < 0.35):
            # x - a = s - a
            rhs = solution - a
            left_l, left_t = _affine_lt(Fraction(1), -a, var)
            trans = "sub"
        else:
            rhs = solution + a
            left_l, left_t = _affine_lt(Fraction(1), a, var)
            trans = "add"
        latex, text = _eq(left_l, left_t, num_latex(rhs), num_latex(rhs))
        return _finish(
            latex=latex,
            text=text,
            solution=solution,
            var=var,
            steps="one",
            n_ops=1,
            upgrades=("one_step", trans),
            eff=eff,
            form_id="one_step_add_sub",
            transforms=(trans,),
            knobs=knobs,
            leading=Fraction(1),
            kind=kind,
            answer_op=answer_op,
            rhs=rhs,
        )
    if op == "div" and knobs.allow_div_form:
        a = _nz_int(rng, knobs.mul_hi, lo=2, allow_neg=knobs.allow_neg, not_one=True)
        if force_neg:
            a = -abs(a)
        rhs = solution / a
        latex = f"\\frac{{{var.latex}}}{{{num_latex(a)}}} = {num_latex(rhs)}"
        text = f"({var.name})/({num_latex(a)}) = {num_latex(rhs)}"
        return _finish(
            latex=latex,
            text=text,
            solution=solution,
            var=var,
            steps="one",
            n_ops=1,
            upgrades=("one_step", "div"),
            eff=eff,
            form_id="one_step_mul_div",
            transforms=("div",),
            knobs=knobs,
            leading=Fraction(1, a) if a != 0 else Fraction(1),
            kind=kind,
            answer_op=answer_op,
            rhs=rhs,
        )
    a = _nz_int(rng, knobs.mul_hi, lo=2, allow_neg=knobs.allow_neg, not_one=True)
    if force_neg:
        a = -abs(a)
    rhs = a * solution
    left_l = coeff_times_var(a, var.latex)
    left_t = coeff_times_var(a, var.name)
    latex, text = _eq(left_l, left_t, num_latex(rhs), num_latex(rhs))
    return _finish(
        latex=latex,
        text=text,
        solution=solution,
        var=var,
        steps="one",
        n_ops=1,
        upgrades=("one_step", "mul"),
        eff=eff,
        form_id="one_step_mul_div",
        transforms=("mul",),
        knobs=knobs,
        leading=a,
        kind=kind,
        answer_op=answer_op,
        rhs=rhs,
    )


def _two_step(
    ctx: PrimitiveContext,
    knobs: SolveLinearKnobs,
    var: SampledVariable,
    solution: Fraction,
    eff: float,
    *,
    kind: SkeletonKind = "eq",
    answer_op: str = "=",
) -> SolveLinearResult:
    rng = ctx.rng
    force_neg = bool(_top_settings(ctx).get("force_negative_coeff")) and knobs.allow_neg
    if knobs.allow_fraction_coeffs and rng.random() < 0.5:
        den = rng.choice([2, 3, 4])
        a = Fraction(1, den)
        if force_neg:
            a = -a
        b = Fraction(rng.choice([1, 1, 2]), rng.choice([2, 3, 4]))
        if knobs.allow_neg and rng.random() < 0.3:
            b = -b
        rhs = a * solution + b
        left_l, left_t = _affine_lt(a, b, var)
        latex, text = _eq(left_l, left_t, num_latex(rhs), num_latex(rhs))
        return _finish(
            latex=latex,
            text=text,
            solution=solution,
            var=var,
            steps="two",
            n_ops=2,
            upgrades=("two_step", "fraction_coeff"),
            eff=eff,
            form_id="two_step",
            transforms=("add", "mul"),
            knobs=knobs,
            leading=a,
            kind=kind,
            answer_op=answer_op,
            rhs=rhs,
        )
    a = _nz_int(rng, knobs.mul_hi, lo=2, allow_neg=knobs.allow_neg, not_one=True)
    if force_neg:
        a = -abs(a)
    b = _nz_int(rng, knobs.addend_hi, allow_neg=knobs.allow_neg)
    rhs = a * solution + b
    left_l, left_t = _affine_lt(a, b, var)
    latex, text = _eq(left_l, left_t, num_latex(rhs), num_latex(rhs))
    return _finish(
        latex=latex,
        text=text,
        solution=solution,
        var=var,
        steps="two",
        n_ops=2,
        upgrades=("two_step",),
        eff=eff,
        form_id="two_step",
        transforms=("add", "mul"),
        knobs=knobs,
        leading=a,
        kind=kind,
        answer_op=answer_op,
        rhs=rhs,
    )


def _simple_distribute(
    rng,
    knobs: SolveLinearKnobs,
    var: SampledVariable,
    solution: Fraction,
    *,
    with_const: bool,
    heavy: bool,
) -> tuple[str, str, tuple[str, ...], int]:
    k = _nz_int(rng, knobs.mul_hi, lo=2, allow_neg=knobs.allow_neg, not_one=True)
    inner_hi = (3, 5, 7, 10, 14)[knobs.numeric_tier]
    c = _nz_int(rng, inner_hi, allow_neg=knobs.allow_neg)
    inner_l, inner_t = _affine_lt(Fraction(1), c, var)
    left_l, left_t = _scaled_paren(k, inner_l, inner_t, heavy=heavy)
    rhs = k * (solution + c)
    n_ops = 2
    trans = ["add", "mul", "distribute"]
    if with_const:
        m = _nz_int(rng, knobs.addend_hi, allow_neg=knobs.allow_neg)
        if m > 0:
            left_l = f"{left_l} + {num_latex(m)}"
            left_t = f"{left_t} + {num_latex(m)}"
        else:
            left_l = f"{left_l} - {num_latex(abs(m))}"
            left_t = f"{left_t} - {num_latex(abs(m))}"
        rhs = rhs + m
        n_ops = 3
        trans.append("add_const")
    latex, text = _eq(left_l, left_t, num_latex(rhs), num_latex(rhs))
    return latex, text, tuple(trans), n_ops, k


def _simple_both_sides(
    rng,
    knobs: SolveLinearKnobs,
    var: SampledVariable,
    solution: Fraction,
    *,
    combine: bool,
    positive_leading: bool = False,
) -> tuple[str, str, tuple[str, ...], int, Fraction]:
    left_a = _nz_int(rng, knobs.mul_hi, lo=2, allow_neg=knobs.allow_neg, not_one=True)
    right_a = _nz_int(rng, knobs.mul_hi, lo=1, allow_neg=knobs.allow_neg)
    if right_a == left_a:
        right_a = left_a - Fraction(1 if left_a > 0 else -1)
        if right_a == 0:
            right_a = Fraction(-1 if left_a > 0 else 1)
    if positive_leading and left_a - right_a <= 0:
        right_a = left_a - Fraction(1)
        if right_a == 0:
            right_a = Fraction(1)
            left_a = Fraction(2)
    left_b = _nz_int(rng, knobs.addend_hi, allow_neg=knobs.allow_neg)
    right_b = left_a * solution + left_b - right_a * solution
    n_ops = 3
    trans = ["mul", "add_ax", "add"]
    if combine and knobs.allow_combine:
        split = _nz_int(rng, min(3, knobs.mul_hi), lo=1, allow_neg=False)
        if split == abs(left_a):
            split = Fraction(1)
        a1 = left_a - split
        if a1 == 0:
            a1 = Fraction(1)
            split = left_a - a1
        t1_l, t1_t = _affine_lt(a1, left_b, var)
        extra_l = coeff_times_var(split, var.latex)
        extra_t = coeff_times_var(split, var.name)
        if split > 0:
            left_l, left_t = f"{t1_l} + {extra_l}", f"{t1_t} + {extra_t}"
        else:
            left_l, left_t = f"{t1_l} - {coeff_times_var(abs(split), var.latex)}", (
                f"{t1_t} - {coeff_times_var(abs(split), var.name)}"
            )
        trans = (*trans, "combine")
        n_ops = 4
    else:
        left_l, left_t = _affine_lt(left_a, left_b, var)
    right_l, right_t = _affine_lt(right_a, right_b, var)
    latex, text = _eq(left_l, left_t, right_l, right_t)
    return latex, text, tuple(trans), n_ops, left_a - right_a


def _distribute_and_both(
    rng,
    knobs: SolveLinearKnobs,
    var: SampledVariable,
    solution: Fraction,
    *,
    heavy: bool,
    positive_leading: bool = False,
) -> tuple[str, str, tuple[str, ...], int, Fraction]:
    k = _nz_int(rng, knobs.mul_hi, lo=2, allow_neg=knobs.allow_neg, not_one=True)
    inner_hi = (3, 5, 7, 10, 14)[knobs.numeric_tier]
    c = _nz_int(rng, inner_hi, allow_neg=knobs.allow_neg)
    m = Fraction(0)
    if rng.random() < 0.65:
        m = _nz_int(rng, knobs.addend_hi, allow_neg=knobs.allow_neg)
    inner_l, inner_t = _affine_lt(Fraction(1), c, var)
    left_l, left_t = _scaled_paren(k, inner_l, inner_t, heavy=heavy)
    if m != 0:
        if m > 0:
            left_l = f"{left_l} + {num_latex(m)}"
            left_t = f"{left_t} + {num_latex(m)}"
        else:
            left_l = f"{left_l} - {num_latex(abs(m))}"
            left_t = f"{left_t} - {num_latex(abs(m))}"
    left_a, left_b = k, k * c + m
    right_a = _nz_int(rng, knobs.mul_hi, lo=1, allow_neg=knobs.allow_neg)
    if right_a == left_a:
        right_a = left_a + Fraction(1 if left_a >= 0 else -1)
        if right_a == 0:
            right_a = Fraction(2)
    if positive_leading and left_a - right_a <= 0:
        right_a = left_a - Fraction(1 if left_a > 1 else 0)
        if right_a <= 0:
            left_a = Fraction(max(2, int(abs(left_a)) + 1))
            k = left_a
            left_b = k * c + m
            inner_l, inner_t = _affine_lt(Fraction(1), c, var)
            left_l, left_t = _scaled_paren(k, inner_l, inner_t, heavy=heavy)
            if m != 0:
                if m > 0:
                    left_l = f"{left_l} + {num_latex(m)}"
                    left_t = f"{left_t} + {num_latex(m)}"
                else:
                    left_l = f"{left_l} - {num_latex(abs(m))}"
                    left_t = f"{left_t} - {num_latex(abs(m))}"
            right_a = Fraction(1)
    # Optional second distribute on the right at format_tier >= 2.
    right_b = left_a * solution + left_b - right_a * solution
    if knobs.format_tier >= 2 and rng.random() < 0.55 and right_a != 0:
        p = right_a
        q = _nz_int(rng, inner_hi, allow_neg=knobs.allow_neg)
        # p(x+q) + r  with r chosen so affine matches (right_a, right_b)
        r = right_b - p * q
        inner_r_l, inner_r_t = _affine_lt(Fraction(1), q, var)
        right_l, right_t = _scaled_paren(p, inner_r_l, inner_r_t, heavy=heavy)
        if r != 0:
            if r > 0:
                right_l = f"{right_l} + {num_latex(r)}"
                right_t = f"{right_t} + {num_latex(r)}"
            else:
                right_l = f"{right_l} - {num_latex(abs(r))}"
                right_t = f"{right_t} - {num_latex(abs(r))}"
    else:
        right_l, right_t = _affine_lt(right_a, right_b, var)
    latex, text = _eq(left_l, left_t, right_l, right_t)
    return latex, text, ("distribute", "add_ax", "add"), 4, left_a - right_a


def _fraction_multi(
    rng,
    knobs: SolveLinearKnobs,
    var: SampledVariable,
    solution: Fraction,
    *,
    heavy: bool,
) -> tuple[str, str, tuple[str, ...], int]:
    """OpenStax §2.5-style fraction coefficients (clear denominators)."""
    den = rng.choice([2, 3, 4, 5])
    if rng.random() < 0.5:
        # (1/d)(ax+b) = c  or  (1/d)x + b = c
        a_in = _nz_int(rng, 4, lo=1, allow_neg=knobs.allow_neg)
        b_in = _nz_int(rng, knobs.addend_hi, allow_neg=knobs.allow_neg)
        k = Fraction(1, den)
        inner_l, inner_t = _affine_lt(a_in, b_in, var)
        left_l, left_t = _scaled_paren(k, inner_l, inner_t, heavy=heavy)
        rhs = k * (a_in * solution + b_in)
        latex, text = _eq(left_l, left_t, num_latex(rhs), num_latex(rhs))
        return latex, text, ("mul", "distribute", "clear_denoms"), 3, k * a_in
    # both sides fractions: (1/d)(x+c) = (1/e)(x+f)
    e = rng.choice([2, 3, 4, 5])
    if e == den:
        e = den + 1
    c = _nz_int(rng, 5, allow_neg=knobs.allow_neg)
    # left: (1/den)(x+c)  affine a=1/den, b=c/den
    # right: (1/e)(x+f) must match at solution
    left_a = Fraction(1, den)
    left_b = Fraction(c, den)
    right_a = Fraction(1, e)
    right_b = left_a * solution + left_b - right_a * solution
    f = right_b * e  # so (1/e)(x+f) has const f/e = right_b
    inner_l, inner_t = _affine_lt(Fraction(1), c, var)
    left_l, left_t = _scaled_paren(left_a, inner_l, inner_t, heavy=heavy)
    inner_r_l, inner_r_t = _affine_lt(Fraction(1), f, var)
    right_l, right_t = _scaled_paren(right_a, inner_r_l, inner_r_t, heavy=heavy)
    latex, text = _eq(left_l, left_t, right_l, right_t)
    return latex, text, ("distribute", "both_sides", "clear_denoms"), 4, left_a - right_a


def _combine_one_side(
    rng,
    knobs: SolveLinearKnobs,
    var: SampledVariable,
    solution: Fraction,
) -> tuple[str, str, tuple[str, ...], int]:
    """OpenStax §2.1-style combine then isolate: 8y-4-7y-7=4."""
    a = _nz_int(rng, knobs.mul_hi, lo=2, allow_neg=False, not_one=True)
    split = _nz_int(rng, min(4, knobs.mul_hi), lo=1, allow_neg=False)
    a1 = a + split
    b1 = _nz_int(rng, knobs.addend_hi, allow_neg=knobs.allow_neg)
    b2 = _nz_int(rng, knobs.addend_hi, allow_neg=knobs.allow_neg)
    # a1 x + b1 - split x + b2  (b2 may be shown as extra const)
    t1 = coeff_times_var(a1, var.latex)
    t1t = coeff_times_var(a1, var.name)
    if b1 >= 0:
        left_l = f"{t1} + {num_latex(b1)}"
        left_t = f"{t1t} + {num_latex(b1)}"
    else:
        left_l = f"{t1} - {num_latex(abs(b1))}"
        left_t = f"{t1t} - {num_latex(abs(b1))}"
    extra = coeff_times_var(split, var.latex)
    extra_t = coeff_times_var(split, var.name)
    left_l = f"{left_l} - {extra}"
    left_t = f"{left_t} - {extra_t}"
    if b2 >= 0:
        left_l = f"{left_l} - {num_latex(b2)}"
        left_t = f"{left_t} - {num_latex(b2)}"
        b_total = b1 - b2
    else:
        left_l = f"{left_l} + {num_latex(abs(b2))}"
        left_t = f"{left_t} + {num_latex(abs(b2))}"
        b_total = b1 + abs(b2)
    # simplified: (a1-split)x + b_total = a x + b_total
    rhs = a * solution + b_total
    latex, text = _eq(left_l, left_t, num_latex(rhs), num_latex(rhs))
    return latex, text, ("combine", "add"), 3, a


def _legacy_inflate(ctx: PrimitiveContext, eff: float) -> SolveLinearResult:
    from question_engine.frameworks.primitives.equations import sample_linear_equation

    eq = sample_linear_equation(ctx, force_steps="multi")
    knobs = solve_linear_knobs(eff, "multi", integers_only=_integers_only(ctx))

    class _Var:
        latex = eq.var_latex
        name = eq.var_name

    return _finish(
        latex=eq.latex,
        text=eq.text,
        solution=eq.solution,
        var=_Var(),  # type: ignore[arg-type]
        steps="multi",
        n_ops=eq.n_ops,
        upgrades=tuple(eq.upgrades) + ("legacy_inflate",),
        eff=eff,
        form_id="multi_step_distribute",
        transforms=("legacy_inflate",),
        knobs=knobs,
        solution_kind=eq.solution_kind,  # type: ignore[arg-type]
        extra_meta={"legacy_engine": "sample_linear_equation"},
    )


def _special_multi(
    ctx: PrimitiveContext,
    knobs: SolveLinearKnobs,
    var: SampledVariable,
    eff: float,
    kind: SolutionKind,
) -> SolveLinearResult:
    rng = ctx.rng
    k = _nz_int(rng, knobs.mul_hi, lo=2, not_one=True, allow_neg=False)
    c = _nz_int(rng, knobs.addend_hi, allow_neg=knobs.allow_neg)
    heavy = knobs.format_tier >= 2
    inner_l, inner_t = _affine_lt(Fraction(1), c, var)
    left_l, left_t = _scaled_paren(k, inner_l, inner_t, heavy=heavy)
    right_a = k
    right_b = k * c if kind == "identity" else k * c + _nz_int(rng, knobs.addend_hi, lo=1)
    right_l, right_t = _affine_lt(right_a, right_b, var)
    latex, text = _eq(left_l, left_t, right_l, right_t)
    return _finish(
        latex=latex,
        text=text,
        solution=Fraction(0),
        var=var,
        steps="multi",
        n_ops=2,
        upgrades=("special", kind),
        eff=eff,
        form_id="multi_step_distribute",
        transforms=("distribute", kind),
        knobs=knobs,
        solution_kind=kind,
    )


def _special_kind(ctx: PrimitiveContext) -> SolutionKind | None:
    settings = ctx.settings_for(PRIM_EQUATIONS)
    top = _top_settings(ctx)
    special = str(
        settings.get("allow_special_solutions")
        or top.get("allow_special_solutions")
        or "none"
    ).strip().lower()
    if special in {"identity"}:
        return "identity"
    if special in {"no_sol", "no_solution", "none_sol"}:
        return "no_solution"
    if special == "mixed":
        r = ctx.rng.random()
        if r < 0.34:
            return None
        return "identity" if r < 0.67 else "no_solution"
    return None


def _multi(
    ctx: PrimitiveContext,
    knobs: SolveLinearKnobs,
    var: SampledVariable,
    solution: Fraction,
    eff: float,
    *,
    kind: SkeletonKind = "eq",
    answer_op: str = "=",
) -> SolveLinearResult:
    rng = ctx.rng
    special = _special_kind(ctx) if kind == "eq" else None
    if special:
        return _special_multi(ctx, knobs, var, eff, special)

    force_clear = ctx.settings_for(PRIM_EQUATIONS).get("clear_fractions") or _top_settings(ctx).get(
        "clear_fractions"
    )
    want_frac = knobs.require_fractions or (
        (knobs.allow_fraction_coeffs or force_clear in (True, "true", "1", 1, "yes"))
        and knobs.format_tier >= 3
    )

    if (
        kind == "eq"
        and knobs.allow_nested
        and not knobs.require_distribute
        and not knobs.require_both_sides
    ):
        if not want_frac or rng.random() < 0.45:
            wrapped = _legacy_inflate(ctx, eff)
            # Rebuild with a real SampledVariable-shaped object already in eq.
            return wrapped

    heavy = knobs.format_tier >= 2
    pos_lead = kind == "ineq" and not knobs.allow_neg
    shape = "both_sides"
    if knobs.require_fractions or want_frac:
        shape = "fractions"
    elif knobs.require_distribute and not knobs.require_both_sides:
        shape = "distribute"
    elif knobs.require_both_sides and not knobs.require_distribute:
        shape = "both_sides"
    elif knobs.format_tier == 0:
        shape = rng.choice(["distribute", "both_sides"])
    elif knobs.format_tier == 1:
        shape = rng.choice(["distribute_const", "both_sides", "combine"])
    else:
        shape = rng.choice(["distribute_both", "distribute_both", "both_sides"])

    leading = Fraction(1)
    if shape == "fractions" and knobs.allow_fraction_coeffs:
        latex, text, trans, n_ops, leading = _fraction_multi(
            rng, knobs, var, solution, heavy=heavy
        )
        form_id = "fraction_or_decimal_coeffs"
    elif shape == "distribute":
        latex, text, trans, n_ops, leading = _simple_distribute(
            rng, knobs, var, solution, with_const=False, heavy=heavy
        )
        form_id = "multi_step_distribute"
    elif shape == "distribute_const":
        latex, text, trans, n_ops, leading = _simple_distribute(
            rng, knobs, var, solution, with_const=True, heavy=heavy
        )
        form_id = "multi_step_distribute"
    elif shape == "combine":
        latex, text, trans, n_ops, leading = _combine_one_side(rng, knobs, var, solution)
        form_id = "multi_step_distribute"
    elif shape == "distribute_both":
        latex, text, trans, n_ops, leading = _distribute_and_both(
            rng, knobs, var, solution, heavy=heavy, positive_leading=pos_lead
        )
        form_id = "multi_step_distribute"
    else:
        latex, text, trans, n_ops, leading = _simple_both_sides(
            rng,
            knobs,
            var,
            solution,
            combine=knobs.allow_combine and knobs.format_tier >= 1,
            positive_leading=pos_lead,
        )
        form_id = "vars_both_sides"

    forced = str(_top_settings(ctx).get("form_id") or "").strip()
    if forced:
        form_id = forced

    return _finish(
        latex=latex,
        text=text,
        solution=solution,
        var=var,
        steps="multi",
        n_ops=n_ops,
        upgrades=("solve_linear", shape, *trans),
        eff=eff,
        form_id=form_id,
        transforms=trans,
        knobs=knobs,
        leading=leading,
        kind=kind,
        answer_op=answer_op,
    )


def sample_solve_linear(
    ctx: PrimitiveContext,
    *,
    force_steps: str | None = None,
    form_id: str | None = None,
    kind: SkeletonKind = "eq",
) -> SolveLinearResult:
    """Sample one SolveLinear equation from the goal solution."""
    species = _parse_species(force_steps, ctx)
    top = _top_settings(ctx)
    fid = str(
        form_id
        or top.get("form_id")
        or ctx.settings_for(PRIM_EQUATIONS).get("form_id")
        or ""
    ).strip() or None
    form_knobs = knobs_from_form_id(fid)
    if form_knobs.get("species") in {"one", "two", "multi"} and not force_steps:
        species = form_knobs["species"]  # type: ignore[assignment]
    # Dedicated leaves keep their species even if form_id is from another family.
    leaf = _leaf_id(ctx)
    if "one_step" in leaf:
        species = "one"
    elif "two_step" in leaf:
        species = "two"
    elif "multi_step" in leaf or leaf.endswith("multi_step_equations"):
        species = "multi"

    ints_only = _integers_only(ctx)
    d = float(ctx.topic_d)
    knobs = solve_linear_knobs(
        d,
        species,
        settings=top,
        form_id=fid,
        integers_only=ints_only,
    )
    var = ctx.sample_variable()
    try:
        ctx.sample_number(exclude_zero=False)
    except Exception:
        pass
    solution = _sample_solution(ctx.rng, knobs)
    answer_op: str = "="
    if kind == "ineq":
        answer_op = _pick_ineq_op(ctx.rng)
    if species == "one":
        return _one_step(
            ctx, knobs, var, solution, d, kind=kind, answer_op=answer_op
        )
    if species == "two":
        return _two_step(
            ctx, knobs, var, solution, d, kind=kind, answer_op=answer_op
        )
    return _multi(ctx, knobs, var, solution, d, kind=kind, answer_op=answer_op)


def sample_solve_inequality(
    ctx: PrimitiveContext,
    *,
    force_steps: str | None = None,
    form_id: str | None = None,
) -> SolveLinearResult:
    """Sample one SolveInequality item (same reverse tape as SolveLinear)."""
    return sample_solve_linear(
        ctx, force_steps=force_steps, form_id=form_id, kind="ineq"
    )


def generate_solve_linear_question(
    settings: dict[str, Any] | None = None,
    *,
    force_steps: str = "multi",
    leaf_id: str = "multi_step_equations",
) -> SolveLinearResult:
    """Demo / gallery API: build context and sample one SolveLinear item."""
    from question_engine.frameworks.primitives import (
        PRIM_NUMBERS,
        PRIM_VARIABLE,
        build_context,
    )
    from question_engine.frameworks.primitives.expression_policy import LINEAR_POLICY

    settings = dict(settings or {})
    settings.setdefault("count", 1)
    ctx = build_context(
        settings,
        [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_EQUATIONS],
        policy=LINEAR_POLICY,
        leaf_id=str(settings.get("_leaf_id") or leaf_id),
    )
    return sample_solve_linear(
        ctx,
        force_steps=force_steps,
        form_id=settings.get("form_id"),
    )


def generate_solve_inequality_question(
    settings: dict[str, Any] | None = None,
    *,
    force_steps: str = "multi",
    leaf_id: str = "multi_step_inequalities",
) -> SolveLinearResult:
    """Demo / gallery API: one SolveInequality item."""
    from question_engine.frameworks.primitives import (
        PRIM_INEQUALITIES,
        PRIM_NUMBERS,
        PRIM_VARIABLE,
        build_context,
    )
    from question_engine.frameworks.primitives.expression_policy import LINEAR_POLICY

    settings = dict(settings or {})
    settings.setdefault("count", 1)
    ctx = build_context(
        settings,
        [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_INEQUALITIES],
        policy=LINEAR_POLICY,
        leaf_id=str(settings.get("_leaf_id") or leaf_id),
    )
    return sample_solve_inequality(
        ctx,
        force_steps=force_steps,
        form_id=settings.get("form_id"),
    )


@dataclass(frozen=True)
class SolveLiteralResult:
    latex: str
    text: str
    solution_latex: str
    target_var: str
    form: str
    n_ops: int
    form_id: str
    upgrades: tuple[str, ...]
    effective_d: float
    metadata: dict[str, Any] = field(default_factory=dict)

    def debug_dict(self) -> dict[str, Any]:
        return {
            "pattern": "SolveLiteral",
            "form_id": self.form_id,
            "form": self.form,
            "target_var": self.target_var,
            "n_ops": self.n_ops,
            **self.metadata,
        }


def _lit_prompt(eq_l: str, eq_t: str, target: str) -> tuple[str, str]:
    latex = f"{eq_l} \\quad \\text{{Solve for }} {target}."
    text = f"{eq_t}. Solve for {target}."
    return latex, text


def sample_solve_literal(ctx: PrimitiveContext) -> SolveLiteralResult:
    """Goal-first isolate of a named formula (OpenStax EA2e §2.6)."""
    rng = ctx.rng
    d = float(ctx.topic_d)
    knobs = solve_linear_knobs(d, "one", settings=_top_settings(ctx), integers_only=True)
    nt, ft = knobs.numeric_tier, knobs.format_tier
    # Sequential format: one-step product → extra letters / two-step → distribute / fractions.
    if ft == 0:
        pool = ["product2", "circ"]
        if nt >= 1:
            pool.append("sum3")
        if nt >= 1:
            pool.append("slope_add")  # y - b = mx  for y (one add)
    elif ft == 1:
        pool = ["product3", "linear_two"]
    elif ft == 2:
        pool = ["perimeter", "slope_x", "linear_two"]
    else:
        pool = ["triangle", "volume", "perimeter", "linear_two"]
    shape = rng.choice(pool)
    hi = (3, 6, 9, 12, 16)[nt]

    def _pos() -> int:
        return max(1, int(_nz_int(rng, hi, lo=1, allow_neg=False)))

    if shape == "product2":
        form = rng.choice(["distance", "area"])
        if form == "distance":
            target = rng.choice(["t", "r"])
            eq_l, eq_t = r"d = r t", "d = rt"
            ans = r"t = \frac{d}{r}" if target == "t" else r"r = \frac{d}{t}"
            n_ops = 1
        else:
            target = rng.choice(["w", r"\ell"])
            eq_l, eq_t = r"A = \ell w", "A = lw"
            ans = (
                r"w = \frac{A}{\ell}"
                if target == "w"
                else r"\ell = \frac{A}{w}"
            )
            n_ops = 1
    elif shape == "circ":
        form = "circumference"
        target = "d"
        eq_l, eq_t = r"C = \pi d", "C = pi d"
        ans = r"d = \frac{C}{\pi}"
        n_ops = 1
    elif shape == "sum3":
        form = "perimeter_tri"
        target = rng.choice(["a", "b", "c"])
        eq_l, eq_t = r"P = a + b + c", "P = a + b + c"
        others = [v for v in ("a", "b", "c") if v != target]
        ans = f"{target} = P - {others[0]} - {others[1]}"
        n_ops = 1
    elif shape == "slope_add":
        form = "slope_intercept_y"
        m = _pos()
        b = _pos()
        target = "y"
        eq_l = f"y - {b} = {m}x" if m != 1 else f"y - {b} = x"
        eq_t = eq_l.replace("x", "x")
        ml = "" if m == 1 else str(m)
        ans = f"y = {ml}x + {b}"
        n_ops = 1
    elif shape == "product3":
        form = rng.choice(["interest", "volume"])
        if form == "interest":
            target = rng.choice(["r", "P", "t"])
            eq_l, eq_t = r"I = P r t", "I = Prt"
            if target == "r":
                ans = r"r = \frac{I}{P t}"
            elif target == "P":
                ans = r"P = \frac{I}{r t}"
            else:
                ans = r"t = \frac{I}{P r}"
            n_ops = 1
        else:
            target = rng.choice(["H", "L", "W"])
            eq_l, eq_t = r"V = L W H", "V = LWH"
            if target == "H":
                ans = r"H = \frac{V}{L W}"
            elif target == "L":
                ans = r"L = \frac{V}{W H}"
            else:
                ans = r"W = \frac{V}{L H}"
            n_ops = 1
    elif shape == "linear_two":
        form = "standard"
        a = _pos()
        b = _pos()
        if a == b:
            b = a + 1
        c = _pos()
        target = "y"
        eq_l = f"{a}x + {b}y = {c}"
        eq_t = eq_l
        ans = f"y = \\frac{{{c} - {a}x}}{{{b}}}"
        n_ops = 2
    elif shape == "perimeter":
        form = "rectangle"
        target = rng.choice(["W", "L"])
        eq_l, eq_t = r"P = 2L + 2W", "P = 2L + 2W"
        if target == "W":
            ans = r"W = \frac{P - 2L}{2}"
        else:
            ans = r"L = \frac{P - 2W}{2}"
        n_ops = 2
    elif shape == "slope_x":
        form = "slope_intercept_x"
        m = _pos()
        b = _pos()
        target = "x"
        ml = "" if m == 1 else str(m)
        eq_l = f"y = {ml}x + {b}" if m != 1 else f"y = x + {b}"
        eq_t = eq_l
        ans = f"x = \\frac{{y - {b}}}{{{m}}}"
        n_ops = 2
    elif shape == "triangle":
        form = "triangle"
        target = rng.choice(["h", "b"])
        eq_l, eq_t = r"A = \frac{1}{2} b h", "A = (1/2)bh"
        ans = r"h = \frac{2A}{b}" if target == "h" else r"b = \frac{2A}{h}"
        n_ops = 2
    else:
        form = "volume"
        target = "H"
        eq_l, eq_t = r"V = L W H", "V = LWH"
        ans = r"H = \frac{V}{L W}"
        n_ops = 1

    latex, text = _lit_prompt(eq_l, eq_t, target)
    cat = _catalog_meta("literal_equation")
    meta = {
        "skeleton_pattern": "SolveLiteral",
        "form_id": "literal_equation",
        "openstax_form": "literal_equation",
        "literal_shape": shape,
        "form": form,
        "target_var": target,
        "n_ops": n_ops,
        "numeric_tier": nt,
        "format_tier": ft,
        "construction": "reverse_skeleton",
        **cat,
    }
    meta["skeleton_pattern"] = "SolveLiteral"
    meta["construction"] = "reverse_skeleton"
    return SolveLiteralResult(
        latex=latex,
        text=text,
        solution_latex=ans,
        target_var=target.replace("\\ell", "l"),
        form=form,
        n_ops=n_ops,
        form_id="literal_equation",
        upgrades=("solve_literal", shape),
        effective_d=d,
        metadata=meta,
    )


def generate_solve_literal_question(
    settings: dict[str, Any] | None = None,
    *,
    leaf_id: str = "literal_equations",
) -> SolveLiteralResult:
    """Demo / gallery API: one SolveLiteral item."""
    from question_engine.frameworks.primitives import (
        PRIM_NUMBERS,
        PRIM_VARIABLE,
        build_context,
    )
    from question_engine.frameworks.primitives.expression_policy import LINEAR_POLICY

    settings = dict(settings or {})
    settings.setdefault("count", 1)
    ctx = build_context(
        settings,
        [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_EQUATIONS],
        policy=LINEAR_POLICY,
        leaf_id=str(settings.get("_leaf_id") or leaf_id),
    )
    return sample_solve_literal(ctx)


# ---------------------------------------------------------------------------
# Proportion / graph-inequality / compound / abs — reuse SolveLinear tape
# ---------------------------------------------------------------------------

_LEGACY_PROP_PATTERNS = {
    "sample_proportion",
    "hand",
    "constructive",
    "legacy",
    "proportions",
}
_LEGACY_COMPOUND_PATTERNS = {
    "sample_compound_inequality",
    "hand",
    "constructive",
    "legacy",
    "compound",
}
_LEGACY_ABS_PATTERNS = {
    "sample_absolute_value",
    "hand",
    "constructive",
    "legacy",
    "absolute_value",
}

CompoundStyle = Literal["chain", "and", "or"]


def use_solve_proportion_skeleton(settings: dict[str, Any] | None) -> bool:
    """Algebraic proportions default to the thin SolveLinear species."""
    s = dict(settings or {})
    if bool(s.get("use_sample_proportion")):
        return False
    if bool(s.get("use_solve_proportion_skeleton") is False):
        return False
    pat = str(s.get("skeleton_pattern", "")).strip()
    if pat in _LEGACY_PROP_PATTERNS:
        return False
    if "use_solve_proportion_skeleton" in s:
        return bool(s.get("use_solve_proportion_skeleton"))
    if pat in {"Proportion", "proportion", "SolveLinear"}:
        return True
    return True


def use_compound_skeleton(settings: dict[str, Any] | None) -> bool:
    s = dict(settings or {})
    if bool(s.get("use_sample_compound_inequality")):
        return False
    if bool(s.get("use_compound_skeleton") is False):
        return False
    pat = str(s.get("skeleton_pattern", "")).strip()
    if pat in _LEGACY_COMPOUND_PATTERNS:
        return False
    if "use_compound_skeleton" in s:
        return bool(s.get("use_compound_skeleton"))
    return True


def use_abs_equation_skeleton(settings: dict[str, Any] | None) -> bool:
    s = dict(settings or {})
    if bool(s.get("use_sample_absolute_value_equation")):
        return False
    if bool(s.get("use_abs_equation_skeleton") is False):
        return False
    pat = str(s.get("skeleton_pattern", "")).strip()
    if pat in _LEGACY_ABS_PATTERNS:
        return False
    if "use_abs_equation_skeleton" in s:
        return bool(s.get("use_abs_equation_skeleton"))
    return True


def use_abs_inequality_skeleton(settings: dict[str, Any] | None) -> bool:
    s = dict(settings or {})
    if bool(s.get("use_sample_absolute_value_inequality")):
        return False
    if bool(s.get("use_abs_inequality_skeleton") is False):
        return False
    pat = str(s.get("skeleton_pattern", "")).strip()
    if pat in _LEGACY_ABS_PATTERNS:
        return False
    if "use_abs_inequality_skeleton" in s:
        return bool(s.get("use_abs_inequality_skeleton"))
    return True


def _frac_pair(num: Any, den: Any) -> tuple[str, str]:
    nl, nt = num_latex(Fraction(num)), str(num)
    dl, dt = num_latex(Fraction(den)), str(den)
    return rf"\frac{{{nl}}}{{{dl}}}", f"({nt})/({dt})"


def sample_solve_proportion(ctx: PrimitiveContext) -> SolveLinearResult:
    """Thin one-step proportion ``a/b = x/c`` (OpenStax EA §8.7).

    D=0 is two small positive integer fractions with the unknown in a numerator.
    Numeric tier grows coeffs; format unlocks unknown-in-denom, then a linear
    numerator that needs clearing.
    """
    rng = ctx.rng
    d = float(ctx.topic_d)
    bands = SkeletonDifficultyBands.from_d(d)
    nt, ft = bands.numeric_tier, bands.format_tier
    var = ctx.sample_variable()
    hi = (5, 8, 12, 18, 28)[max(0, min(4, nt))]
    a = rng.randint(1, max(2, hi // 2 + 1))
    b = rng.randint(2, max(3, hi // 2 + 1))
    c = rng.randint(2, max(3, hi // 2 + 1))
    if nt == 0 and ft == 0:
        a, b, c = rng.choice([(2, 3, 4), (1, 2, 3), (2, 5, 4), (3, 4, 6), (1, 3, 5)])
    if a == b and ft >= 2:
        a = a + 1
    dummy = SolveLinearKnobs(
        species="one",
        numeric_tier=nt,
        format_tier=ft,
        addend_hi=hi,
        mul_hi=hi,
        sol_hi=hi,
        allow_neg=nt >= 2,
        allow_div_form=True,
        allow_fraction_coeffs=False,
        allow_fraction_solution=True,
        allow_decimals=False,
        allow_distribute=False,
        allow_both_sides=False,
        allow_combine=False,
        allow_nested=False,
    )
    form = "a_over_b_eq_x_over_c"
    n_ops = 1
    transforms: tuple[str, ...] = ("cross_multiply",)
    if ft == 0:
        # a/b = x/c  →  x = a c / b
        sol = Fraction(a * c, b)
        left_l, left_t = _frac_pair(a, b)
        right_l = rf"\frac{{{var.latex}}}{{{num_latex(Fraction(c))}}}"
        right_t = f"({var.name})/({c})"
        latex, text = _eq(left_l, left_t, right_l, right_t)
    elif ft == 1:
        # a/x = b/c  →  x = a c / b
        sol = Fraction(a * c, b)
        left_l = rf"\frac{{{num_latex(Fraction(a))}}}{{{var.latex}}}"
        left_t = f"({a})/({var.name})"
        right_l, right_t = _frac_pair(b, c)
        latex, text = _eq(left_l, left_t, right_l, right_t)
        form = "a_over_x_eq_b_over_c"
        transforms = ("cross_multiply", "var_in_denom")
    else:
        # a/b = (x+k)/c  →  x = a c / b - k
        k = rng.randint(1, max(1, min(4, hi // 3)))
        if nt >= 2 and rng.random() < 0.35:
            k = -k
        sol = Fraction(a * c, b) - Fraction(k)
        left_l, left_t = _frac_pair(a, b)
        inner_l, inner_t = join_signed_terms(
            [(Fraction(1), var.latex), (Fraction(k), "")]
        )
        right_l = rf"\frac{{{inner_l}}}{{{num_latex(Fraction(c))}}}"
        right_t = f"({inner_t})/({c})"
        latex, text = _eq(left_l, left_t, right_l, right_t)
        form = "a_over_b_eq_linear_over_c"
        n_ops = 2
        transforms = ("cross_multiply", "add")
    return _finish(
        latex=latex,
        text=text,
        solution=sol,
        var=var,
        steps="one" if n_ops == 1 else "two",
        n_ops=n_ops,
        upgrades=("proportion", form),
        eff=d,
        form_id="proportion_application",
        transforms=transforms,
        knobs=dummy,
        extra_meta={
            "skeleton_pattern": "Proportion",
            "species": "proportion",
            "construction": "reverse_skeleton",
            "form": form,
        },
    )


def sample_graph_inequality(ctx: PrimitiveContext) -> SolveLinearResult:
    """Number-line 1-var inequality. D=0 is already isolated ``x < k``."""
    d = float(ctx.topic_d)
    bands = SkeletonDifficultyBands.from_d(d)
    ft = bands.format_tier
    if ft == 0:
        rng = ctx.rng
        var = ctx.sample_variable()
        op = _pick_ineq_op(rng)
        s = Fraction(rng.randint(1, 6))
        if bands.numeric_tier >= 2 and rng.random() < 0.35:
            s = -s
        latex = f"{var.latex} {op} {num_latex(s)}"
        text = f"{var.name} {_OP_TEXT.get(op, op)} {num_latex(s)}"
        dummy = SolveLinearKnobs(
            species="one",
            numeric_tier=bands.numeric_tier,
            format_tier=0,
            addend_hi=6,
            mul_hi=6,
            sol_hi=6,
            allow_neg=bands.numeric_tier >= 2,
            allow_div_form=False,
            allow_fraction_coeffs=False,
            allow_fraction_solution=False,
            allow_decimals=False,
            allow_distribute=False,
            allow_both_sides=False,
            allow_combine=False,
            allow_nested=False,
        )
        result = _finish(
            latex=latex,
            text=text,
            solution=s,
            var=var,
            steps="one",
            n_ops=0,
            upgrades=("graph_inequality", "isolated"),
            eff=d,
            form_id="one_step_ineq_add_sub",
            transforms=("isolated",),
            knobs=dummy,
            kind="ineq",
            answer_op=op,
            extra_meta={"species": "graph_isolated", "n_ops": 0},
        )
        return result
    force = "one" if ft == 1 else "two"
    item = sample_solve_inequality(ctx, force_steps=force)
    packed = dict(item.metadata)
    packed["species"] = f"graph_{force}"
    return SolveLinearResult(
        latex=item.latex,
        text=item.text,
        solution_latex=item.solution_latex,
        solution=item.solution,
        var_latex=item.var_latex,
        var_name=item.var_name,
        steps=item.steps,
        n_ops=item.n_ops,
        upgrades=tuple([*item.upgrades, "graph_inequality"]),
        effective_d=item.effective_d,
        solution_kind=item.solution_kind,
        form_id=item.form_id,
        transforms=item.transforms,
        metadata=packed,
        leading=item.leading,
        relation=item.relation,
        op=item.op,
        flipped=item.flipped,
    )


def sample_check_equation(ctx: PrimitiveContext) -> SolveLinearResult:
    """G6 "is x=k a solution?" — same SolveLinear species as the old hand leaf.

    Live old ``check_equation_solution`` (topic_fit + D=0/8/16/22):
    - D=0: one-step ``3x=24`` / ``x+4=6``
    - D=8: two-step ``ax+b=c``
    - D=16: two-step or both-sides
    - D≥21: fraction coeffs (old ignores ``integers_only`` here)
    """
    d = float(ctx.topic_d)
    rng = ctx.rng
    form_id = None
    if d < 4.0:
        force: Species = "one"
    elif d < 16.0:
        force = "two"
    elif d < 21.0:
        # Old D=16–20: two-step with negatives, or vars on both sides — not distribute.
        if rng.random() < 0.45:
            force = "multi"
            form_id = "vars_both_sides"
        else:
            force = "two"
    else:
        force = "multi"
        form_id = "fraction_or_decimal_coeffs"
    item = sample_solve_linear(ctx, force_steps=force, form_id=form_id)
    if item.solution_kind != "unique":
        item = sample_solve_linear(ctx, force_steps=force, form_id=form_id)
    true_s = Fraction(item.solution)
    if rng.random() < 0.55:
        cand = true_s
    else:
        cand = true_s
        for _ in range(10):
            if true_s.denominator != 1:
                bump = Fraction(rng.choice([-2, -1, 1, 2, 3]), rng.choice([1, 2]))
                cand = true_s + bump
            else:
                span = max(6, abs(int(true_s)) + 6)
                cand = Fraction(rng.randint(-span // 2, span))
            if cand != true_s:
                break
        if cand == true_s:
            cand = true_s + Fraction(1)
    is_sol = cand == true_s
    prompt = (
        rf"\text{{Is }} {item.var_latex} = {num_latex(cand)} \text{{ a solution of }} "
        rf"{item.latex}\text{{?}}"
    )
    text = f"Is {item.var_name} = {num_latex(cand)} a solution of {item.text}?"
    answer = r"\text{yes}" if is_sol else r"\text{no}"
    packed = dict(item.metadata)
    packed.update(
        {
            "skeleton_pattern": "SolveLinear",
            "species": f"check_{force}",
            "candidate": str(cand),
            "is_solution": is_sol,
            "hidden_eq": item.latex,
        }
    )
    return SolveLinearResult(
        latex=prompt,
        text=text,
        solution_latex=answer,
        solution=true_s,
        var_latex=item.var_latex,
        var_name=item.var_name,
        steps=item.steps,
        n_ops=item.n_ops,
        upgrades=tuple([*item.upgrades, "check_solution"]),
        effective_d=item.effective_d,
        solution_kind=item.solution_kind,
        form_id=item.form_id,
        transforms=item.transforms,
        metadata=packed,
        leading=item.leading,
        relation=item.relation,
        op=item.op,
        flipped=item.flipped,
    )


def _interval_latex(
    lo: Fraction,
    hi: Fraction,
    *,
    style: CompoundStyle,
    lo_inc: bool,
    hi_inc: bool,
) -> str:
    left = "[" if lo_inc else "("
    right = "]" if hi_inc else ")"
    if style == "or":
        left_end = "]" if lo_inc else ")"
        right_start = "[" if hi_inc else "("
        return (
            rf"(-\infty,{num_latex(lo)}{left_end} \cup "
            rf"{right_start}{num_latex(hi)},\infty)"
        )
    return f"{left}{num_latex(lo)}, {num_latex(hi)}{right}"


def _abs_inner(
    ctx: PrimitiveContext,
    var,
    *,
    ft: int,
    nt: int,
) -> tuple[str, str, Fraction, Fraction]:
    """Return (inner_latex, inner_text, a, b) for ``|ax+b|``.

    Inners match old ``AbsoluteValue*Framework`` at comparable D — not new
    packaging (no abs=abs, coeff-outside, or abs-vs-linear):

    - easy (nt = 0): ``|x|`` or ``|x+b|``, a = 1 (old simple + shifted)
    - early numeric (nt = 1): ``|x+b|`` with larger b, still a = 1
    - medium+ (nt ≥ 2, old D=8 linear): ``|ax+b|`` with ``|a| ≥ 2``
    """
    rng = ctx.rng
    addend_hi = (4, 9, 16, 28, 40)[max(0, min(4, nt))]
    mul_hi = (4, 6, 8, 10, 12)[max(0, min(4, nt))]
    allow_neg = nt >= 1
    # nt≥2 is D≥8 (old medium). format_tier is unused for the inner; empty
    # k<0 stays in the equation caller.
    _ = ft
    if nt >= 2:
        a = _nz_int(rng, mul_hi, lo=2, allow_neg=allow_neg, not_one=True, ctx=ctx)
        # Old integer_only linear: b is a multiple of a so ±k branches stay int.
        span = max(1, min(4, 1 + nt))
        m = rng.randint(-span, span)
        if m == 0 and rng.random() < 0.75:
            m = rng.choice((-1, 1))
        b = a * Fraction(m)
        inner_l, inner_t = _affine_lt(a, b, var)
        return inner_l, inner_t, a, b
    a = Fraction(1)
    if nt == 0 and rng.random() < 0.55:
        return var.latex, var.name, a, Fraction(0)
    b_hi = 3 if nt == 0 else addend_hi
    b = _nz_int(rng, b_hi, allow_neg=True, ctx=ctx)
    inner_l, inner_t = _affine_lt(a, b, var)
    return inner_l, inner_t, a, b


def _abs_nice_k(
    rng,
    a: Fraction,
    b: Fraction,
    *,
    hi: int,
    empty: bool,
) -> Fraction:
    """RHS k. Reverse from an integer x0 so solutions stay classroom-nice."""
    if empty:
        return Fraction(-rng.randint(1, max(1, hi // 3)))
    for _ in range(16):
        x0 = Fraction(rng.randint(-hi, hi))
        k = abs(a * x0 + b)
        if k > 0:
            return k
    return abs(a) if a != 0 else Fraction(1)


@dataclass(frozen=True)
class AbsEquationResult:
    latex: str
    text: str
    solution_latex: str
    solution_kind: str
    k: Fraction
    inner_a: Fraction
    inner_b: Fraction
    var_latex: str
    upgrades: tuple[str, ...]
    effective_d: float
    metadata: dict[str, Any] = field(default_factory=dict)

    def debug_dict(self) -> dict[str, Any]:
        return {"pattern": "AbsEquation", "k": str(self.k), **self.metadata}


@dataclass(frozen=True)
class AbsInequalityResult:
    latex: str
    text: str
    solution_latex: str
    compound_style: CompoundStyle
    lo: Fraction | None
    hi: Fraction | None
    lo_inclusive: bool
    hi_inclusive: bool
    var_latex: str
    op: str
    k: Fraction
    inner_a: Fraction
    inner_b: Fraction
    upgrades: tuple[str, ...]
    effective_d: float
    metadata: dict[str, Any] = field(default_factory=dict)

    def debug_dict(self) -> dict[str, Any]:
        return {
            "pattern": "AbsInequality",
            "compound_style": self.compound_style,
            **self.metadata,
        }


def sample_abs_equation_skeleton(ctx: PrimitiveContext) -> AbsEquationResult:
    """Split ``|inner| = k`` into two SolveLinear cases. Empty when k < 0."""
    rng = ctx.rng
    d = float(ctx.topic_d)
    bands = SkeletonDifficultyBands.from_d(d)
    nt, ft = bands.numeric_tier, bands.format_tier
    var = ctx.sample_variable()
    hi = (4, 7, 11, 16, 24)[max(0, min(4, nt))]
    empty = ft >= 3 and rng.random() < 0.28
    inner_l, inner_t, a, b = _abs_inner(ctx, var, ft=ft, nt=nt)
    k = _abs_nice_k(rng, a, b, hi=hi, empty=empty)
    prompt_l = rf"\left|{inner_l}\right| = {num_latex(k)}"
    prompt_t = f"|{inner_t}| = {num_latex(k)}"
    if k < 0:
        ans = r"\emptyset"
        kind = "empty"
        tags = ("abs_eq", "empty")
    elif a == 0:
        ans = r"\emptyset"
        kind = "empty"
        tags = ("abs_eq", "empty")
    else:
        # |ax+b| = k → ax+b = k or ax+b = -k
        s1 = (k - b) / a
        s2 = (-k - b) / a
        uniq = sorted({s1, s2})
        ans = " \\text{ or } ".join(f"{var.latex} = {num_latex(s)}" for s in uniq)
        kind = "two_roots" if len(uniq) == 2 else "one_root"
        tags = ("abs_eq", f"ft:{ft}")
    meta = {
        "skeleton_pattern": "AbsEquation",
        "species": "abs_eq",
        "numeric_tier": nt,
        "format_tier": ft,
        "construction": "abs_split_solve_linear",
        "form_id": "absolute_value_equation",
        "k": str(k),
        "inner_a": str(a),
        "inner_b": str(b),
        "solution_kind": kind,
    }
    return AbsEquationResult(
        latex=prompt_l,
        text=prompt_t,
        solution_latex=ans,
        solution_kind=kind,
        k=k,
        inner_a=a,
        inner_b=b,
        var_latex=var.latex,
        upgrades=tags,
        effective_d=d,
        metadata=meta,
    )


def sample_abs_inequality_skeleton(ctx: PrimitiveContext) -> AbsInequalityResult:
    """``|inner| < k`` → compound and; ``|inner| > k`` → or + number line."""
    rng = ctx.rng
    d = float(ctx.topic_d)
    bands = SkeletonDifficultyBands.from_d(d)
    nt, ft = bands.numeric_tier, bands.format_tier
    var = ctx.sample_variable()
    hi = (3, 5, 8, 12, 18)[max(0, min(4, nt))]
    inner_l, inner_t, a, b = _abs_inner(ctx, var, ft=ft, nt=nt)
    k = _abs_nice_k(rng, a, b, hi=hi, empty=False)
    less = rng.random() < 0.55
    inclusive = bool(nt >= 1 and rng.random() < 0.3)
    if less:
        op = "\\le" if inclusive else "<"
        style: CompoundStyle = "chain"
    else:
        op = "\\ge" if inclusive else ">"
        style = "or"
    prompt_l = rf"\left|{inner_l}\right| {op} {num_latex(k)}"
    prompt_t = f"|{inner_t}| {_OP_TEXT.get(op, op)} {num_latex(k)}"
    # |ax+b| < k → -k < ax+b < k → bounds on x: ((-k-b)/a , (k-b)/a) if a>0
    if a == 0:
        lo = hi_b = None
        ans = r"\emptyset"
        tags = ("abs_ineq", "empty")
        lo_inc = hi_inc = False
    else:
        raw_lo = (-k - b) / a
        raw_hi = (k - b) / a
        if a < 0:
            raw_lo, raw_hi = raw_hi, raw_lo
            # flipping inequality when dividing by negative — already encoded
            # by swapping bounds for the chain; for or, same swap.
        lo, hi_b = raw_lo, raw_hi
        if lo > hi_b:
            lo, hi_b = hi_b, lo
        lo_inc = hi_inc = inclusive
        if style == "or":
            ans = _interval_latex(lo, hi_b, style="or", lo_inc=lo_inc, hi_inc=hi_inc)
        else:
            ans = _interval_latex(lo, hi_b, style="chain", lo_inc=lo_inc, hi_inc=hi_inc)
        tags = ("abs_ineq", style, f"ft:{ft}")
    meta = {
        "skeleton_pattern": "AbsInequality",
        "species": "abs_ineq",
        "numeric_tier": nt,
        "format_tier": ft,
        "construction": "abs_to_compound",
        "form_id": "absolute_value_inequality",
        "compound_style": style,
        "op": op,
        "k": str(k),
        "inner_a": str(a),
        "inner_b": str(b),
        "lo": str(lo) if lo is not None else None,
        "hi": str(hi_b) if hi_b is not None else None,
        "lo_inclusive": lo_inc,
        "hi_inclusive": hi_inc,
    }
    return AbsInequalityResult(
        latex=prompt_l,
        text=prompt_t,
        solution_latex=ans,
        compound_style=style,
        lo=lo,
        hi=hi_b,
        lo_inclusive=lo_inc,
        hi_inclusive=hi_inc,
        var_latex=var.latex,
        op=op,
        k=k,
        inner_a=a,
        inner_b=b,
        upgrades=tags,
        effective_d=d,
        metadata=meta,
    )
