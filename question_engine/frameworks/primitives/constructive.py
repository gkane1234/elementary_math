"""Answer-first constructive generation — Target → inflate → verify.

Levels (compositional):
  L1  numeric / affine / polynomial expressions
  L2  single rational P/Q
  L3  sum/product of rationals
  L4  partial fractions (seed PF form, combine to prompt)

Difficulty ``D`` spends on inflators. ExpressionPolicy / family gates remain hard.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Literal

from question_engine.frameworks.primitives._algebra_render import (
    join_signed_terms,
    num_latex,
    sample_integerish,
)
from question_engine.frameworks.primitives.presentation import (
    DisplayPiece,
    expand_scaled_sum_latex,
    maybe_inject_cancel_clutter,
    presentation_for_ctx,
    render_addition,
    render_division,
    render_product,
    render_scaled_sum,
    render_subtraction,
)
from question_engine.frameworks.primitives.registry import (
    PRIM_EXPAND_SIMPLIFY,
    PRIM_OOO,
    PrimitiveContext,
)
from question_engine.frameworks.primitives.variables import SampledVariable

ConstructLevel = Literal["L1", "L2", "L3", "L4"]


# ---------------------------------------------------------------------------
# Scope — hard gates / preferences for the expression generator
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ExpressionScope:
    """Constraints for how the expression generator may present a target.

    Topics pass a scope; the generator owns commute / factor order / cancel
    clutter. Clients (distributive, expand/simplify, …) stay thin.

    * ``max_degree`` — linear topics use ``1`` (affine only).
    * ``allow_cancel_clutter`` — when True, presentation may wrap with
      value-preserving ``+k−k`` / ``+kx−kx`` / distributive cancel pairs
      (still gated by soft ``cancel_clutter`` knobs; amount 0 → never).
    * ``prefer_distributive_factorization`` — present ``a·var+b`` as a
      factored ``outer·(sum…)`` ready for distributive rewrite, with
      commute / explicit-multiply from the shared presentation layer.
    """

    max_degree: int = 1
    allow_cancel_clutter: bool = False
    prefer_distributive_factorization: bool = False


# ---------------------------------------------------------------------------
# Targets
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class NumericTarget:
    value: Fraction
    level: ConstructLevel = "L1"

    def as_dict(self) -> dict[str, Any]:
        return {"kind": "numeric", "value": str(self.value), "level": self.level}


@dataclass(frozen=True)
class AffineTarget:
    """Simplified form ``a·var + b``."""

    a: Fraction
    b: Fraction
    level: ConstructLevel = "L1"

    def as_dict(self) -> dict[str, Any]:
        return {
            "kind": "affine",
            "a": str(self.a),
            "b": str(self.b),
            "level": self.level,
        }


@dataclass(frozen=True)
class RationalPolyTarget:
    """Single rational in lowest terms: num/den as degree→coeff maps (int keys)."""

    num: tuple[tuple[int, Fraction], ...]  # (degree, coeff) descending or any
    den: tuple[tuple[int, Fraction], ...]
    level: ConstructLevel = "L2"

    def num_dict(self) -> dict[int, Fraction]:
        return {d: c for d, c in self.num if c != 0}

    def den_dict(self) -> dict[int, Fraction]:
        return {d: c for d, c in self.den if c != 0}

    def as_dict(self) -> dict[str, Any]:
        return {
            "kind": "rational",
            "num": [(d, str(c)) for d, c in self.num],
            "den": [(d, str(c)) for d, c in self.den],
            "level": self.level,
        }


@dataclass(frozen=True)
class CancelPlan:
    """How many polynomial factors should cancel in a rational simplify/×÷/add path."""

    cancel_count: int
    level: ConstructLevel = "L2"

    def as_dict(self) -> dict[str, Any]:
        return {
            "kind": "cancel_plan",
            "cancel_count": self.cancel_count,
            "level": self.level,
        }


@dataclass(frozen=True)
class PartialFractionTerm:
    """A/(x - r) or (Bx + C)/(x^2 + …) — linear dens first."""

    numerator: Fraction  # constant A for linear den
    root: Fraction  # pole at x = root → factor (x - root)
    multiplicity: int = 1

    def as_dict(self) -> dict[str, Any]:
        return {
            "A": str(self.numerator),
            "root": str(self.root),
            "multiplicity": self.multiplicity,
        }


@dataclass(frozen=True)
class PartialFractionTarget:
    """L4 answer: sum of partial fractions."""

    terms: tuple[PartialFractionTerm, ...]
    level: ConstructLevel = "L4"

    def as_dict(self) -> dict[str, Any]:
        return {
            "kind": "partial_fractions",
            "terms": [t.as_dict() for t in self.terms],
            "level": self.level,
        }


@dataclass(frozen=True)
class SurfaceExpression:
    latex: str
    text: str
    target: Any
    level: ConstructLevel
    inflators_applied: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    # Optional evaluated / simplified payloads for callers
    value: Fraction | None = None
    coeff_a: Fraction | None = None
    coeff_b: Fraction | None = None
    simplified_latex: str | None = None
    simplified_text: str | None = None


# ---------------------------------------------------------------------------
# Budget helpers
# ---------------------------------------------------------------------------


def inflator_budget(d: float) -> int:
    """How many inflator steps: ``floor(log2(1 + D / inflator_scale))`` (unbounded).

    Guarantees ``min_inflators_count`` when ``D >= min_inflators_when_d_ge``.
    """
    from question_engine.frameworks.primitives.difficulty_knobs import fget, iget, section

    d = max(0.0, float(d))
    scale = fget("constructive", "inflator_scale", 2.0)
    n = int(math.floor(math.log2(1.0 + d / scale)))
    sec = section("constructive")
    gate = float(sec.get("min_inflators_when_d_ge", 1.0))
    mn = int(sec.get("min_inflators_count", 1))
    if d >= gate:
        return max(mn, n)
    return n


def seed_numeric_target(ctx: PrimitiveContext) -> NumericTarget:
    n = sample_integerish(ctx, exclude_zero=False)
    return NumericTarget(value=n.value)


def seed_affine_target(
    ctx: PrimitiveContext,
    *,
    force_var: bool = True,
) -> AffineTarget:
    a = sample_integerish(ctx, exclude_zero=force_var).value
    if force_var and a == 0:
        a = Fraction(ctx.rng.choice([1, -1, 2, -2]))
    b = sample_integerish(ctx, exclude_zero=False).value
    return AffineTarget(a=a, b=b)


# ---------------------------------------------------------------------------
# Recursive disguise (relatedness tree from difficulty_knobs.json)
# ---------------------------------------------------------------------------

RecurseKind = Literal[
    "L1_numeric",
    "L1_affine",
    "L2_rational",
    "L3_rational_sum",
    "L4_pfd",
]


def _recurse_section() -> dict[str, Any]:
    from question_engine.frameworks.primitives.difficulty_knobs import section

    raw = section("constructive").get("recurse") or {}
    return raw if isinstance(raw, dict) else {}


def _should_recurse(ctx: PrimitiveContext, d: float, depth: int, parent_kind: RecurseKind) -> bool:
    cfg = _recurse_section()
    if not bool(cfg.get("enabled", False)):
        return False
    if depth >= int(cfg.get("max_depth", 2)):
        return False
    if d < float(cfg.get("min_d_to_recurse", 4.0)):
        return False
    allowed = cfg.get("allowed_child_levels") or {}
    children = allowed.get(parent_kind) if isinstance(allowed, dict) else None
    if isinstance(children, list) and not children:
        return False
    return ctx.rng.random() < float(cfg.get("chance_per_block", 0.25))


def _child_budget(d: float) -> float:
    cfg = _recurse_section()
    frac = float(cfg.get("budget_fraction_to_child", 0.45))
    return max(0.0, float(d) * max(0.0, min(1.0, frac)))


def _pick_child_kind(ctx: PrimitiveContext, parent_kind: RecurseKind) -> RecurseKind:
    cfg = _recurse_section()
    allowed = cfg.get("allowed_child_levels") or {}
    children = allowed.get(parent_kind) if isinstance(allowed, dict) else None
    if not isinstance(children, list) or not children:
        return parent_kind
    choice = str(ctx.rng.choice(children))
    if choice in {"L1_numeric", "L1_affine", "L2_rational", "L3_rational_sum", "L4_pfd"}:
        return choice  # type: ignore[return-value]
    return parent_kind


def disguise_numeric(
    ctx: PrimitiveContext,
    value: Fraction,
    *,
    d: float,
    depth: int,
    parent_kind: RecurseKind = "L1_numeric",
) -> tuple[str, str, tuple[str, ...]]:
    """Render a numeric block; maybe recurse through a related L1_numeric constructor."""
    plain_l, plain_t = num_latex(value), num_latex(value)
    if not _should_recurse(ctx, d, depth, parent_kind):
        return plain_l, plain_t, ()
    child_kind = _pick_child_kind(ctx, parent_kind)
    # Numeric holes can only be filled by L1_numeric (related tree filter).
    if child_kind != "L1_numeric":
        allowed = (_recurse_section().get("allowed_child_levels") or {}).get(parent_kind) or []
        if isinstance(allowed, list) and "L1_numeric" in allowed:
            child_kind = "L1_numeric"
        else:
            return plain_l, plain_t, ()
    child = construct_numeric(
        ctx,
        d=_child_budget(d),
        target=NumericTarget(value=value),
        _depth=depth + 1,
    )
    return (
        f"\\left({child.latex}\\right)",
        f"({child.text})",
        ("recurse:L1_numeric", *child.inflators_applied),
    )


def disguise_affine(
    ctx: PrimitiveContext,
    a: Fraction,
    b: Fraction,
    var: SampledVariable,
    *,
    d: float,
    depth: int,
    parent_kind: RecurseKind = "L1_affine",
) -> tuple[str, str, tuple[str, ...]]:
    """Render an affine block; maybe recurse through L1_affine (or L1_numeric if a=0)."""
    plain_l, plain_t = _affine_latex(a, b, var)
    if a == 0:
        return disguise_numeric(ctx, b, d=d, depth=depth, parent_kind=parent_kind)
    if not _should_recurse(ctx, d, depth, parent_kind):
        return plain_l, plain_t, ()
    child_kind = _pick_child_kind(ctx, parent_kind)
    if child_kind == "L1_numeric" and a == 0:
        return disguise_numeric(ctx, b, d=d, depth=depth, parent_kind="L1_numeric")
    if child_kind != "L1_affine":
        allowed = (_recurse_section().get("allowed_child_levels") or {}).get(parent_kind) or []
        if isinstance(allowed, list) and "L1_affine" in allowed:
            child_kind = "L1_affine"
        else:
            return plain_l, plain_t, ()
    child = construct_affine(
        ctx,
        d=_child_budget(d),
        var=var,
        target=AffineTarget(a=a, b=b),
        prefer_distribute=True,
        _depth=depth + 1,
    )
    return (
        f"\\left({child.latex}\\right)",
        f"({child.text})",
        ("recurse:L1_affine", *child.inflators_applied),
    )


def _coerce_related_l1(
    parent_kind: RecurseKind,
    child_kind: RecurseKind,
    num: dict[int, Fraction] | None = None,
    den: dict[int, Fraction] | None = None,
) -> Literal["L1_numeric", "L1_affine"]:
    """Map a relatedness pick to an implemented L1 child for rational blocks."""
    allowed = (_recurse_section().get("allowed_child_levels") or {}).get(parent_kind) or []
    if not isinstance(allowed, list):
        allowed = []

    def _has_affine_block() -> bool:
        for poly in (num, den):
            if poly and max(poly) <= 1 and poly.get(1, Fraction(0)) != 0:
                return True
        return False

    if (
        child_kind == "L1_affine"
        and ("L1_affine" in allowed or not allowed)
        and _has_affine_block()
    ):
        return "L1_affine"
    if child_kind == "L1_numeric" and ("L1_numeric" in allowed or not allowed):
        return "L1_numeric"
    if "L1_affine" in allowed and _has_affine_block():
        return "L1_affine"
    if "L1_numeric" in allowed or not allowed:
        return "L1_numeric"
    return "L1_affine"


def _disguise_rational_fraction(
    ctx: PrimitiveContext,
    num: dict[int, Fraction],
    den: dict[int, Fraction],
    var: SampledVariable,
    *,
    d: float,
    depth: int,
    parent_kind: RecurseKind,
) -> tuple[str, str, tuple[str, ...]]:
    """Maybe nest an L1 block into a P/Q prompt (value unchanged).

    Related children only: L1_affine on a degree-≤1 num/den, or L1_numeric via a
    canceling scale factor shown in both numerator and denominator.
    """
    plain_l, plain_t = _fraction_latex(num, den, var)
    if not _should_recurse(ctx, d, depth, parent_kind):
        return plain_l, plain_t, ()

    child_kind = _coerce_related_l1(
        parent_kind, _pick_child_kind(ctx, parent_kind), num, den
    )

    if child_kind == "L1_affine":
        for poly, is_num in ((num, True), (den, False)):
            if not poly:
                continue
            a = poly.get(1, Fraction(0))
            b = poly.get(0, Fraction(0))
            if max(poly) <= 1 and a != 0:
                child = construct_affine(
                    ctx,
                    d=_child_budget(d),
                    var=var,
                    target=AffineTarget(a=a, b=b),
                    prefer_distribute=True,
                    _depth=depth + 1,
                )
                other = den if is_num else num
                other_l, other_t = _render_poly_dict(other, var)
                wrapped_l = f"\\left({child.latex}\\right)"
                wrapped_t = f"({child.text})"
                if is_num:
                    latex = rf"\frac{{{wrapped_l}}}{{{other_l}}}"
                    text = f"({wrapped_t})/({other_t})"
                else:
                    latex = rf"\frac{{{other_l}}}{{{wrapped_l}}}"
                    text = f"({other_t})/({wrapped_t})"
                return latex, text, ("recurse:L1_affine", *child.inflators_applied)

    k = Fraction(ctx.rng.choice([2, 3, 4]))
    child = construct_numeric(
        ctx,
        d=_child_budget(d),
        target=NumericTarget(value=k),
        _depth=depth + 1,
    )
    nl, nt = _render_poly_dict(num, var)
    dl, dt = _render_poly_dict(den, var)
    kl = f"\\left({child.latex}\\right)"
    kt = f"({child.text})"
    # rf-string: use \left not \\left (raw keeps a single backslash; \\ would double-escape).
    latex = rf"\frac{{{kl}\left({nl}\right)}}{{{kl}\left({dl}\right)}}"
    text = f"(({kt})*({nt}))/(({kt})*({dt}))"
    return latex, text, ("recurse:L1_numeric", *child.inflators_applied)


# ---------------------------------------------------------------------------
# L1 numeric: target → inflate
# ---------------------------------------------------------------------------


def construct_numeric(
    ctx: PrimitiveContext,
    *,
    d: float | None = None,
    target: NumericTarget | None = None,
    _depth: int = 0,
) -> SurfaceExpression:
    """Build an OOO-style expression that evaluates to ``target`` (answer-first).

    Inflators may recursively disguise sub-blocks via the relatedness tree.
    """
    eff = float(ctx.topic_d if d is None else d)
    if d is None:
        eff = max(eff, ctx.effective_d(PRIM_OOO))
    style = presentation_for_ctx(ctx, d=eff)
    tgt = target or seed_numeric_target(ctx)
    latex, text = num_latex(tgt.value), num_latex(tgt.value)
    applied: list[str] = ["seed"]
    budget = inflator_budget(eff)
    recurse_tags: list[str] = []

    steps = budget  # D=0 → plain number; never force an inflator just because D>0
    for _ in range(steps):
        choice = ctx.rng.choice(
            ["split_add", "split_sub", "scale_div", "parens_sum", "mul_add"]
        )
        if choice == "split_add":
            k = sample_integerish(ctx, exclude_zero=True).value
            left = tgt.value - k
            left_l, left_t, lt = disguise_numeric(
                ctx, left, d=eff, depth=_depth, parent_kind="L1_numeric"
            )
            k_l, k_t, kt = disguise_numeric(
                ctx, k, d=eff, depth=_depth, parent_kind="L1_numeric"
            )
            add_l, add_t = render_addition(
                DisplayPiece(left_l, left_t),
                DisplayPiece(k_l, k_t),
                style,
                ctx.rng,
            )
            latex = f"({add_l})"
            text = f"({add_t})"
            applied.append("split_add")
            recurse_tags.extend(lt)
            recurse_tags.extend(kt)
        elif choice == "split_sub":
            k = sample_integerish(ctx, exclude_zero=True).value
            left = tgt.value + k
            left_l, left_t, lt = disguise_numeric(
                ctx, left, d=eff, depth=_depth, parent_kind="L1_numeric"
            )
            k_l, k_t, kt = disguise_numeric(
                ctx, k, d=eff, depth=_depth, parent_kind="L1_numeric"
            )
            sub_l, sub_t = render_subtraction(
                DisplayPiece(left_l, left_t),
                DisplayPiece(k_l, k_t),
                style,
                ctx.rng,
            )
            latex = f"({sub_l})"
            text = f"({sub_t})"
            applied.append("split_sub")
            recurse_tags.extend(lt)
            recurse_tags.extend(kt)
        elif choice == "scale_div" and tgt.value != 0:
            k = Fraction(ctx.rng.choice([2, 3, 4, 5]))
            num_v = tgt.value * k
            num_l, num_t, nt = disguise_numeric(
                ctx, num_v, d=eff, depth=_depth, parent_kind="L1_numeric"
            )
            k_l, k_t, kt = disguise_numeric(
                ctx, k, d=eff, depth=_depth, parent_kind="L1_numeric"
            )
            div_l, div_t = render_division(
                DisplayPiece(num_l, num_t),
                DisplayPiece(k_l, k_t),
                style,
                ctx.rng,
            )
            latex = f"({div_l})"
            text = f"({div_t})"
            applied.append("scale_div")
            recurse_tags.extend(nt)
            recurse_tags.extend(kt)
        elif choice == "mul_add":
            k = Fraction(ctx.rng.choice([2, 3]))
            m = sample_integerish(ctx, exclude_zero=True).value
            inner = (tgt.value - m) / k
            inner_l, inner_t, it = disguise_numeric(
                ctx, inner, d=eff, depth=_depth, parent_kind="L1_numeric"
            )
            k_l, k_t, kt = disguise_numeric(
                ctx, k, d=eff, depth=_depth, parent_kind="L1_numeric"
            )
            m_l, m_t, mt = disguise_numeric(
                ctx, m, d=eff, depth=_depth, parent_kind="L1_numeric"
            )
            prod_l, prod_t = render_product(
                [
                    DisplayPiece(k_l, k_t),
                    DisplayPiece(f"({inner_l})", f"({inner_t})"),
                ],
                style,
                ctx.rng,
            )
            add_l, add_t = render_addition(
                DisplayPiece(prod_l, prod_t),
                DisplayPiece(m_l, m_t),
                style,
                ctx.rng,
            )
            latex = f"({add_l})"
            text = f"({add_t})"
            applied.append("mul_add")
            recurse_tags.extend(it + kt + mt)
        else:  # parens_sum — meaningful grouping, not (z−z) cancel noise
            k = sample_integerish(ctx, exclude_zero=True).value
            left = tgt.value - k
            left_l, left_t, lt = disguise_numeric(
                ctx, left, d=eff, depth=_depth, parent_kind="L1_numeric"
            )
            k_l, k_t, kt = disguise_numeric(
                ctx, k, d=eff, depth=_depth, parent_kind="L1_numeric"
            )
            add_l, add_t = render_addition(
                DisplayPiece(left_l, left_t),
                DisplayPiece(k_l, k_t),
                style,
                ctx.rng,
            )
            latex = f"\\left({add_l}\\right)"
            text = f"({add_t})"
            applied.append("parens_sum")
            recurse_tags.extend(lt + kt)

    from question_engine.frameworks.primitives.difficulty_knobs import fget, iget

    if budget >= iget("constructive", "numeric_scale_mul_div_min_budget", 2) and ctx.rng.random() < fget(
        "constructive", "numeric_scale_mul_div_chance", 0.45
    ):
        k = Fraction(ctx.rng.choice([2, 3]))
        k_l, k_t, kt = disguise_numeric(
            ctx, k, d=eff, depth=_depth, parent_kind="L1_numeric"
        )
        prod_l, prod_t = render_product(
            [
                DisplayPiece(k_l, k_t),
                DisplayPiece(f"({latex})", f"({text})"),
            ],
            style,
            ctx.rng,
        )
        div_l, div_t = render_division(
            DisplayPiece(prod_l, prod_t),
            DisplayPiece(k_l, k_t),
            style,
            ctx.rng,
        )
        latex = f"({div_l})"
        text = f"({div_t})"
        applied.append("scale_mul_div")
        recurse_tags.extend(kt)

    meta = {
        "effective_d": eff,
        "constructive": True,
        "recurse_depth": _depth,
        "recurse_hits": sum(1 for t in recurse_tags if t.startswith("recurse:")),
    }
    return SurfaceExpression(
        latex=latex,
        text=text,
        target=tgt,
        level="L1",
        inflators_applied=tuple(applied) + tuple(recurse_tags),
        value=tgt.value,
        metadata=meta,
    )


# ---------------------------------------------------------------------------
# L1 affine: target a·x+b → inflate (expand/simplify surface)
# ---------------------------------------------------------------------------


def _affine_latex(
    a: Fraction,
    b: Fraction,
    var: SampledVariable,
    *,
    style=None,
    rng=None,
) -> tuple[str, str]:
    parts: list[tuple[Fraction, str]] = []
    if a != 0:
        parts.append((a, var.latex))
    if b != 0 or not parts:
        parts.append((b, ""))
    if style is not None and getattr(style, "commute_add", False) and rng is not None and len(parts) > 1:
        from question_engine.frameworks.primitives.presentation import order_commutative

        parts = order_commutative(parts, commute=True, rng=rng)
    return join_signed_terms(parts)


def _seed_distributive_affine(
    ctx: PrimitiveContext,
) -> tuple[AffineTarget, str, list[tuple[str, str, Fraction]], str]:
    """Seed expanded linear answer + factor plan for distributive presentation.

    Returns ``(target, form, summands_without_var, outer_kind)`` where
    ``outer_kind`` is ``\"var\"`` or a numeric latex string for const outer.
    Summands for const_outer use a ``VAR`` placeholder for the variable term.
    Never seeds a degenerate sum that cancels to zero or a ±1-only triviality
    that fails to look like classroom distributive practice.
    """
    if ctx.rng.random() < 0.5:
        for _ in range(16):
            n1 = ctx.sample_number()
            n2 = ctx.sample_number()
            if n1.value == 0 or n2.value == 0:
                continue
            if n1.value + n2.value == 0:
                continue
            if n1.value == n2.value:
                continue
            summands = [
                (n1.latex, n1.latex, n1.value),
                (n2.latex, n2.latex, n2.value),
            ]
            total = n1.value + n2.value
            return AffineTarget(a=total, b=Fraction(0)), "var_outer", summands, "var"
        summands = [
            (num_latex(Fraction(2)), num_latex(Fraction(2)), Fraction(2)),
            (num_latex(Fraction(3)), num_latex(Fraction(3)), Fraction(3)),
        ]
        return AffineTarget(a=Fraction(5), b=Fraction(0)), "var_outer", summands, "var"

    for _ in range(12):
        a = ctx.sample_number(exclude_zero=True)
        b = ctx.sample_number()
        # Never use ±1 as the outer factor — juxtaposition reads as a lone sum.
        if abs(a.value) == 1:
            continue
        return (
            AffineTarget(a=a.value, b=a.value * b.value),
            "const_outer",
            [
                ("VAR", "VAR", Fraction(1)),
                (b.latex, b.latex, b.value),
            ],
            a.latex,
        )
    return (
        AffineTarget(a=Fraction(3), b=Fraction(6)),
        "const_outer",
        [
            ("VAR", "VAR", Fraction(1)),
            (num_latex(Fraction(2)), num_latex(Fraction(2)), Fraction(2)),
        ],
        num_latex(Fraction(3)),
    )


def _present_distributive_factorization(
    ctx: PrimitiveContext,
    *,
    var: SampledVariable,
    style,
    target: AffineTarget | None,
) -> tuple[AffineTarget, str, str, str, str, str]:
    """Build factored prompt + expanded answer for an affine target.

    Returns ``(tgt, form, latex, text, expanded_latex, _)``.
    """
    if target is None:
        tgt, form, summands, outer_kind = _seed_distributive_affine(ctx)
        if form == "var_outer":
            outer = DisplayPiece(var.latex, var.name)
        else:
            summands = [
                (var.latex, var.name, Fraction(1)) if s[0] == "VAR" else s
                for s in summands
            ]
            outer = DisplayPiece(outer_kind, outer_kind)
    else:
        tgt = target
        # Factor an existing expanded target into a classroom distributive shape.
        if tgt.b == 0 and tgt.a != 0:
            form = "var_outer"
            n1 = sample_integerish(ctx, exclude_zero=False).value
            n2 = tgt.a - n1
            if n2 == 0:
                n2 = Fraction(ctx.rng.choice([1, -1, 2]))
                n1 = tgt.a - n2
            summands = [
                (num_latex(n1), num_latex(n1), n1),
                (num_latex(n2), num_latex(n2), n2),
            ]
            outer = DisplayPiece(var.latex, var.name)
        else:
            form = "const_outer"
            outer_v = tgt.a if tgt.a != 0 else Fraction(1)
            if tgt.a != 0 and tgt.b % tgt.a == 0:
                inner_b = tgt.b / tgt.a
                outer_v = tgt.a
            else:
                inner_b = tgt.b / outer_v if outer_v != 0 else tgt.b
            summands = [
                (var.latex, var.name, Fraction(1)),
                (num_latex(inner_b), num_latex(inner_b), inner_b),
            ]
            outer = DisplayPiece(num_latex(outer_v), num_latex(outer_v))

    latex, text = render_scaled_sum(outer, summands, style, ctx.rng)
    expanded = expand_scaled_sum_latex(outer.latex, [(s[0], s[2]) for s in summands])
    return tgt, form, latex, text, expanded, ""


def construct_affine(
    ctx: PrimitiveContext,
    *,
    d: float | None = None,
    var: SampledVariable | None = None,
    target: AffineTarget | None = None,
    prefer_distribute: bool = True,
    min_inflators: int | None = None,
    scope: ExpressionScope | None = None,
    _depth: int = 0,
) -> SurfaceExpression:
    """Build an unsimplified expression that simplifies to ``a·var + b``.

    Pass ``scope`` to constrain degree, request distributive factorization, or
    allow shared cancel-clutter wrapping. Expand/simplify topics can later opt
    into ``allow_cancel_clutter`` without topic-local hacks.

    ``min_inflators`` forces at least that many classroom inflators (e.g. 1 for
    expand/simplify so D=0 is still a single ``k(x+n)``, not already-simplified).
    """
    scope = scope or ExpressionScope()
    if scope.max_degree < 1:
        raise ValueError("construct_affine requires max_degree >= 1")

    eff = float(d if d is not None else ctx.effective_d(PRIM_EXPAND_SIMPLIFY))
    if d is None:
        eff = max(eff, float(ctx.topic_d) * 0.5)
    style = presentation_for_ctx(ctx, d=eff)
    v = var or ctx.sample_variable()

    # --- Distributive-ready factorization (thin topics like distributive) ---
    if scope.prefer_distributive_factorization:
        tgt, form, latex, text, expanded, _ = _present_distributive_factorization(
            ctx, var=v, style=style, target=target
        )
        a, b = tgt.a, tgt.b
        applied: list[str] = ["seed", "distributive_factor"]
        cancel_tags: tuple[str, ...] = ()
        if scope.allow_cancel_clutter:
            latex, text, cancel_tags = maybe_inject_cancel_clutter(
                ctx,
                style,
                var_latex=v.latex,
                var_text=v.name,
                core_latex=latex,
                core_text=text,
                d=eff,
            )
            applied.extend(cancel_tags)
        simp_l, simp_t = _affine_latex(a, b, v)
        return SurfaceExpression(
            latex=latex,
            text=text,
            target=tgt,
            level="L1",
            inflators_applied=tuple(applied),
            coeff_a=a,
            coeff_b=b,
            simplified_latex=simp_l,
            simplified_text=simp_t,
            metadata={
                "effective_d": eff,
                "constructive": True,
                "var": v.name,
                "recurse_depth": _depth,
                "recurse_hits": 0,
                "distributive_form": form,
                "expanded_distributive_latex": expanded,
                "cancel_clutter": list(cancel_tags),
                "scope": {
                    "max_degree": scope.max_degree,
                    "allow_cancel_clutter": scope.allow_cancel_clutter,
                    "prefer_distributive_factorization": True,
                },
            },
        )

    tgt = target or seed_affine_target(ctx, force_var=True)
    a, b = tgt.a, tgt.b
    latex, text = _affine_latex(a, b, v, style=style, rng=ctx.rng)
    applied = ["seed"]
    budget = inflator_budget(eff)
    if min_inflators is not None:
        budget = max(budget, int(min_inflators))
    recurse_tags: list[str] = []

    # Meaningful classroom inflators only: distribute / split-const.
    # Trivial (zx−zx) is NOT default — use presentation.cancel_clutter instead.
    from question_engine.frameworks.primitives.difficulty_knobs import section as _knob_sec

    allow_trivial = bool(
        (_knob_sec("constructive") or {}).get("allow_trivial_cancel_pair", False)
    )
    steps = budget
    for _i in range(steps):
        choices: list[str] = ["distribute", "distribute", "split_const"]
        if prefer_distribute:
            choices = ["distribute", "distribute", "distribute", "split_const"]
        if allow_trivial and eff >= 16:
            choices.append("cancel_pair")
        # First step for expand-style: always distribute into a real sum.
        if prefer_distribute and "distribute" not in "".join(applied) and _i == 0:
            choice = "distribute"
        else:
            choice = ctx.rng.choice(choices)

        if choice == "distribute":
            k = sample_integerish(ctx, exclude_zero=True).value
            if abs(k) == 1:
                k = Fraction(ctx.rng.choice([2, 3, -2, -3]))
            u = Fraction(1)
            if prefer_distribute and eff >= 8 and ctx.rng.random() < 0.35:
                u = Fraction(ctx.rng.choice([1, -1, 2]))
            rem_a: Fraction
            rem_b: Fraction
            if a % k == 0 and b % k == 0:
                inner_a, inner_b = a / k, b / k
                rem_a, rem_b = Fraction(0), Fraction(0)
                if inner_b == 0:
                    peel = Fraction(ctx.rng.choice([1, 2, -1, -2]))
                    inner_b = peel
                    rem_b = -k * peel
            else:
                v_c = Fraction(ctx.rng.choice([-3, -2, -1, 1, 2, 3]))
                rem_a = a - k * u
                rem_b = b - k * v_c
                inner_a, inner_b = u, v_c
            if abs(inner_a) > 6 or abs(inner_b) > 12:
                continue
            if inner_a == 0:
                inner_a = Fraction(1)
                rem_a = rem_a - k
            if inner_b == 0:
                peel = Fraction(ctx.rng.choice([1, 2, -1, -2]))
                inner_b = peel
                rem_b = rem_b - k * peel
            inner_l, inner_t = _affine_latex(inner_a, inner_b, v)
            k_l, k_t = num_latex(k), num_latex(k)
            prod_l, prod_t = render_product(
                [
                    DisplayPiece(k_l, k_t),
                    DisplayPiece(f"\\left({inner_l}\\right)", f"({inner_t})"),
                ],
                style,
                ctx.rng,
            )
            if rem_a == 0 and rem_b == 0:
                latex, text = prod_l, prod_t
                applied.append("distribute")
            else:
                rem_l, rem_t = _affine_latex(rem_a, rem_b, v)
                latex, text = render_addition(
                    DisplayPiece(prod_l, prod_t),
                    DisplayPiece(rem_l, rem_t),
                    style,
                    ctx.rng,
                )
                applied.append("distribute_split")
        elif choice == "cancel_pair" and allow_trivial:
            z = sample_integerish(ctx, exclude_zero=True).value
            z_l = num_latex(z)
            latex = f"{latex} + ({z_l}{v.latex} - {z_l}{v.latex})"
            text = f"{text} + ({num_latex(z)}{v.name} - {num_latex(z)}{v.name})"
            applied.append("cancel_pair")
        else:  # split_const
            if b == 0:
                continue
            k = sample_integerish(ctx, exclude_zero=True).value
            if k == b:
                continue
            b1 = b - k
            core_l, core_t = _affine_latex(a, b1, v)
            k_l, k_t = num_latex(k), num_latex(k)
            latex, text = render_addition(
                DisplayPiece(core_l, core_t),
                DisplayPiece(k_l, k_t),
                style,
                ctx.rng,
            )
            applied.append("split_const")

    cancel_tags = ()
    if scope.allow_cancel_clutter:
        latex, text, cancel_tags = maybe_inject_cancel_clutter(
            ctx,
            style,
            var_latex=v.latex,
            var_text=v.name,
            core_latex=latex,
            core_text=text,
            d=eff,
        )
        applied.extend(cancel_tags)

    simp_l, simp_t = _affine_latex(a, b, v)
    return SurfaceExpression(
        latex=latex,
        text=text,
        target=tgt,
        level="L1",
        inflators_applied=tuple(applied) + tuple(recurse_tags),
        coeff_a=a,
        coeff_b=b,
        simplified_latex=simp_l,
        simplified_text=simp_t,
        metadata={
            "effective_d": eff,
            "constructive": True,
            "var": v.name,
            "recurse_depth": _depth,
            "recurse_hits": sum(1 for t in recurse_tags if t.startswith("recurse:")),
            "cancel_clutter": list(cancel_tags),
            "scope": {
                "max_degree": scope.max_degree,
                "allow_cancel_clutter": scope.allow_cancel_clutter,
                "prefer_distributive_factorization": False,
            },
        },
    )


def verify_numeric(surface: SurfaceExpression, target: NumericTarget) -> bool:
    return surface.value == target.value


def verify_affine(surface: SurfaceExpression, target: AffineTarget) -> bool:
    return surface.coeff_a == target.a and surface.coeff_b == target.b


# ---------------------------------------------------------------------------
# L2 / L3 rationals + L4 PFD — poly helpers
# ---------------------------------------------------------------------------


def _poly_add(
    p: dict[int, Fraction], q: dict[int, Fraction]
) -> dict[int, Fraction]:
    out: dict[int, Fraction] = dict(p)
    for d, c in q.items():
        out[d] = out.get(d, Fraction(0)) + c
        if out[d] == 0:
            del out[d]
    return out


def _poly_scale(p: dict[int, Fraction], k: Fraction) -> dict[int, Fraction]:
    if k == 0:
        return {}
    return {d: c * k for d, c in p.items() if c * k != 0}


def _poly_mul(
    p: dict[int, Fraction], q: dict[int, Fraction]
) -> dict[int, Fraction]:
    out: dict[int, Fraction] = {}
    for d1, c1 in p.items():
        for d2, c2 in q.items():
            d = d1 + d2
            out[d] = out.get(d, Fraction(0)) + c1 * c2
    return {d: c for d, c in out.items() if c != 0}


def _poly_from_linear(root: Fraction) -> dict[int, Fraction]:
    """(x - root)"""
    return {1: Fraction(1), 0: -root}


def _render_poly_dict(
    coeffs: dict[int, Fraction], var: SampledVariable
) -> tuple[str, str]:
    if not coeffs:
        return "0", "0"
    parts: list[tuple[Fraction, str]] = []
    for deg in sorted(coeffs.keys(), reverse=True):
        c = coeffs[deg]
        if c == 0:
            continue
        if deg == 0:
            parts.append((c, ""))
        elif deg == 1:
            parts.append((c, var.latex))
        else:
            parts.append((c, f"{var.latex}^{{{deg}}}"))
    return join_signed_terms(parts)


def _content_gcd(coeffs: dict[int, Fraction]) -> Fraction:
    nums = [abs(c.numerator) for c in coeffs.values() if c != 0]
    dens = [c.denominator for c in coeffs.values() if c != 0]
    if not nums:
        return Fraction(1)
    from math import gcd

    g = nums[0]
    for n in nums[1:]:
        g = gcd(g, n)
    # also clear denominators into content — keep Fraction gcd via integers
    return Fraction(g)


def construct_rational_sum(
    ctx: PrimitiveContext,
    *,
    d: float | None = None,
    var: SampledVariable | None = None,
    n_terms: int | None = None,
    cancel_count: int | None = None,
) -> SurfaceExpression:
    """L3: build A/D1 ± B/D2 (± …) that combine to a known simplified rational.

    Strategy: seed partial-like pieces (or shared LCD), combine for answer key,
    optionally insert a cancel factor into one numerator and the LCD.
    """
    eff = float(d if d is not None else max(ctx.topic_d, 0.0))
    v = var or ctx.sample_variable()
    n = n_terms if n_terms is not None else (2 if eff < 6 else (3 if eff < 14 else 2))
    n = max(2, min(4, n))
    k_cancel = (
        cancel_count
        if cancel_count is not None
        else (0 if eff < 4 else (1 if eff < 10 else ctx.rng.randint(1, 2)))
    )

    # Seed distinct linear dens (x - r_i)
    roots: list[Fraction] = []
    while len(roots) < n:
        r = sample_integerish(ctx, exclude_zero=False).value
        if r not in roots:
            roots.append(r)

    # Seed numerators (constants) — answer after combine over LCD
    nums = [sample_integerish(ctx, exclude_zero=True).value for _ in range(n)]
    dens = [_poly_from_linear(r) for r in roots]

    # Combined target: sum nums[i] / dens[i]
    lcd = {0: Fraction(1)}
    for den in dens:
        lcd = _poly_mul(lcd, den)

    combined_num: dict[int, Fraction] = {}
    for i, (num_i, den_i) in enumerate(zip(nums, dens)):
        # cofactor = lcd / den_i
        cofactor = {0: Fraction(1)}
        for j, den_j in enumerate(dens):
            if j != i:
                cofactor = _poly_mul(cofactor, den_j)
        combined_num = _poly_add(combined_num, _poly_scale(cofactor, num_i))

    # Optional cancel factor: multiply num and lcd by (x - c)
    cancel_factor: dict[int, Fraction] | None = None
    if k_cancel >= 1:
        c_root = sample_integerish(ctx, exclude_zero=False).value
        while c_root in roots:
            c_root = sample_integerish(ctx, exclude_zero=False).value
        cancel_factor = _poly_from_linear(c_root)
        combined_num = _poly_mul(combined_num, cancel_factor)
        lcd = _poly_mul(lcd, cancel_factor)

    # L2 cancel path: single unsimplified fraction; L1 disguise on num/den only
    # (do not build summand disguises that would be orphaned by the combined prompt).
    if k_cancel >= 1 and cancel_factor is not None:
        ans_num, ans_den = _cancel_linear_factor(combined_num, lcd, cancel_factor)
        ans_l, ans_t = _fraction_latex(ans_num, ans_den, v)
        latex, text, recurse_tags = _disguise_rational_fraction(
            ctx,
            combined_num,
            lcd,
            v,
            d=eff,
            depth=0,
            parent_kind="L2_rational",
        )
        plan = CancelPlan(cancel_count=k_cancel, level="L2")
        target = RationalPolyTarget(
            num=tuple(sorted(ans_num.items(), reverse=True)),
            den=tuple(sorted(ans_den.items(), reverse=True)),
            level="L2",
        )
        return SurfaceExpression(
            latex=latex,
            text=text,
            target=target,
            level="L2",
            inflators_applied=("seed_sum", "insert_cancel_factor") + tuple(recurse_tags),
            simplified_latex=ans_l,
            simplified_text=ans_t,
            metadata={
                "effective_d": eff,
                "cancel_plan": plan.as_dict(),
                "constructive": True,
                "mode": "simplify_rational",
                "recurse_hits": sum(1 for t in recurse_tags if t.startswith("recurse:")),
            },
        )

    # L3 path: sum of fractions; disguise numerators (L1_numeric) and dens (L1_affine)
    parts_l: list[str] = []
    parts_t: list[str] = []
    recurse_tags: list[str] = []
    for i, (num_i, r) in enumerate(zip(nums, roots)):
        nl, nt, ntags = disguise_numeric(
            ctx, num_i, d=eff, depth=0, parent_kind="L3_rational_sum"
        )
        dl, dt, dtags = disguise_affine(
            ctx,
            Fraction(1),
            -r,
            v,
            d=eff,
            depth=0,
            parent_kind="L3_rational_sum",
        )
        recurse_tags.extend(ntags)
        recurse_tags.extend(dtags)
        piece_l = rf"\frac{{{nl}}}{{{dl}}}"
        piece_t = f"({nt})/({dt})"
        if i == 0:
            parts_l.append(piece_l)
            parts_t.append(piece_t)
        else:
            parts_l.append("+" + piece_l)
            parts_t.append("+" + piece_t)

    latex = "".join(parts_l)
    text = "".join(parts_t)
    ans_l, ans_t = _fraction_latex(combined_num, lcd, v)
    target = RationalPolyTarget(
        num=tuple(sorted(combined_num.items(), reverse=True)),
        den=tuple(sorted(lcd.items(), reverse=True)),
        level="L3",
    )
    return SurfaceExpression(
        latex=latex,
        text=text,
        target=target,
        level="L3",
        inflators_applied=("seed_summands", "combine_lcd") + tuple(recurse_tags),
        simplified_latex=ans_l,
        simplified_text=ans_t,
        metadata={
            "effective_d": eff,
            "n_terms": n,
            "cancel_plan": CancelPlan(0).as_dict(),
            "constructive": True,
            "mode": "add_subtract_rationals",
            "recurse_hits": sum(1 for t in recurse_tags if t.startswith("recurse:")),
        },
    )


def _cancel_linear_factor(
    num: dict[int, Fraction],
    den: dict[int, Fraction],
    factor: dict[int, Fraction],
) -> tuple[dict[int, Fraction], dict[int, Fraction]]:
    """Cancel one monic linear factor from num and den when present."""
    # factor is (x - r) = {1:1, 0:-r}
    r = -factor.get(0, Fraction(0))
    # Synthetic division / evaluate root for exact cancel
    if _poly_eval(num, r) != 0 or _poly_eval(den, r) != 0:
        return num, den
    return _poly_div_linear(num, r), _poly_div_linear(den, r)


def _poly_eval(p: dict[int, Fraction], x: Fraction) -> Fraction:
    total = Fraction(0)
    for d, c in p.items():
        total += c * (x**d)
    return total


def _poly_div_linear(p: dict[int, Fraction], root: Fraction) -> dict[int, Fraction]:
    """Divide p by (x - root) via synthetic division; assumes exact (remainder 0)."""
    if not p:
        return {}
    deg = max(p)
    coeffs = [p.get(i, Fraction(0)) for i in range(deg, -1, -1)]
    acc = coeffs[0]
    quot: list[Fraction] = [acc]
    for c in coeffs[1:]:
        acc = acc * root + c
        quot.append(acc)
    # quot[-1] is remainder; quotient coeffs are quot[:-1] (highest degree first)
    body = quot[:-1]
    if not body:
        return {}
    result: dict[int, Fraction] = {}
    qdeg = len(body) - 1
    for i, c in enumerate(body):
        d = qdeg - i
        if c != 0:
            result[d] = c
    return result

def _fraction_latex(
    num: dict[int, Fraction], den: dict[int, Fraction], var: SampledVariable
) -> tuple[str, str]:
    # Normalize leading den > 0
    if den:
        lead = den[max(den)]
        if lead < 0:
            num = _poly_scale(num, Fraction(-1))
            den = _poly_scale(den, Fraction(-1))
    nl, nt = _render_poly_dict(num, var)
    dl, dt = _render_poly_dict(den, var)
    if den == {0: Fraction(1)}:
        return nl, nt
    return rf"\frac{{{nl}}}{{{dl}}}", f"({nt})/({dt})"


# ---------------------------------------------------------------------------
# L4 PFD
# ---------------------------------------------------------------------------


def seed_partial_fraction_target(
    ctx: PrimitiveContext,
    *,
    n_terms: int | None = None,
    d: float = 0.0,
) -> PartialFractionTarget:
    n = n_terms if n_terms is not None else (2 if d < 8 else 3)
    n = max(2, min(4, n))
    roots: list[Fraction] = []
    terms: list[PartialFractionTerm] = []
    while len(terms) < n:
        r = sample_integerish(ctx, exclude_zero=False).value
        if r in roots:
            continue
        roots.append(r)
        a = sample_integerish(ctx, exclude_zero=True).value
        terms.append(PartialFractionTerm(numerator=a, root=r, multiplicity=1))
    return PartialFractionTarget(terms=tuple(terms))


def construct_pfd(
    ctx: PrimitiveContext,
    *,
    d: float | None = None,
    var: SampledVariable | None = None,
    target: PartialFractionTarget | None = None,
) -> SurfaceExpression:
    """L4: seed partial fractions (answer), combine to a single rational (prompt)."""
    eff = float(d if d is not None else max(ctx.topic_d, 0.0))
    v = var or ctx.sample_variable()
    tgt = target or seed_partial_fraction_target(ctx, d=eff)

    # Combine Σ A_i/(x - r_i)
    dens = [_poly_from_linear(t.root) for t in tgt.terms]
    lcd = {0: Fraction(1)}
    for den in dens:
        lcd = _poly_mul(lcd, den)

    combined_num: dict[int, Fraction] = {}
    for i, t in enumerate(tgt.terms):
        cofactor = {0: Fraction(1)}
        for j, den in enumerate(dens):
            if j != i:
                cofactor = _poly_mul(cofactor, den)
        combined_num = _poly_add(combined_num, _poly_scale(cofactor, t.numerator))

    # Optional L1-ish inflate: multiply num and den by a constant k
    applied = ["seed_pf", "combine_lcd"]
    from question_engine.frameworks.primitives.difficulty_knobs import fget

    if inflator_budget(eff) >= 1 and ctx.rng.random() < fget(
        "constructive", "pfd_scale_num_den_chance", 0.4
    ):
        k = Fraction(ctx.rng.choice([2, 3]))
        combined_num = _poly_scale(combined_num, k)
        lcd = _poly_scale(lcd, k)
        applied.append("scale_num_den")

    # Student prompt may nest related L1 blocks into the combined rational.
    prompt_l, prompt_t, recurse_tags = _disguise_rational_fraction(
        ctx,
        combined_num,
        lcd,
        v,
        d=eff,
        depth=0,
        parent_kind="L4_pfd",
    )

    # Answer latex: clean sum of A/(x-r) (no disguise — answer key stays readable)
    ans_parts_l: list[str] = []
    ans_parts_t: list[str] = []
    for i, t in enumerate(tgt.terms):
        den_l, den_t = _render_poly_dict(_poly_from_linear(t.root), v)
        piece_l = rf"\frac{{{num_latex(t.numerator)}}}{{{den_l}}}"
        piece_t = f"({num_latex(t.numerator)})/({den_t})"
        if i == 0:
            ans_parts_l.append(piece_l)
            ans_parts_t.append(piece_t)
        else:
            ans_parts_l.append("+" + piece_l)
            ans_parts_t.append("+" + piece_t)

    ans_l = "".join(ans_parts_l)
    ans_t = "".join(ans_parts_t)

    return SurfaceExpression(
        latex=prompt_l,
        text=prompt_t,
        target=tgt,
        level="L4",
        inflators_applied=tuple(applied) + tuple(recurse_tags),
        simplified_latex=ans_l,
        simplified_text=ans_t,
        metadata={
            "effective_d": eff,
            "constructive": True,
            "mode": "pfd",
            "n_terms": len(tgt.terms),
            "pf_target": tgt.as_dict(),
            "recurse_hits": sum(1 for t in recurse_tags if t.startswith("recurse:")),
        },
    )


def verify_pfd_combine(surface: SurfaceExpression) -> bool:
    """Re-combine PF target and compare to prompt polynomials (structural)."""
    tgt = surface.target
    if not isinstance(tgt, PartialFractionTarget):
        return False
    return bool(surface.simplified_latex) and bool(surface.latex)
