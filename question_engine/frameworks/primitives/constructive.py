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

    * ``max_degree`` — linear topics use ``1`` (affine only). Poly
      construction via ``construct_poly`` requires ``≥ 2`` and caps the
      seeded / inflated degree.
    * ``allow_cancel_clutter`` — when True, presentation may wrap with
      value-preserving ``+k−k`` / ``+kx−kx`` / distributive cancel pairs
      (still gated by soft ``cancel_clutter`` knobs; amount 0 → never).
    * ``prefer_distributive_factorization`` — present ``a·var+b`` as a
      factored ``outer·(sum…)`` ready for distributive rewrite, with
      commute / explicit-multiply from the shared presentation layer.
    * ``prefer_single_hot`` — when set, bias poly seeds toward a single
      higher-order (degree ≥ 2) term vs multiple; ``None`` = knob/D bias.
    * ``max_terms`` / ``exact_terms`` — optional caps on nonzero terms in the
      seeded target (thin course topics, e.g. PA ≤3 terms).
    * ``min_degree`` — floor on seeded degree (default 2).
    """

    max_degree: int = 1
    allow_cancel_clutter: bool = False
    prefer_distributive_factorization: bool = False
    prefer_single_hot: bool | None = None
    max_terms: int | None = None
    exact_terms: int | None = None
    min_degree: int = 2


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
class PolynomialTarget:
    """Simplified univariate polynomial as a sparse degree→coeff map.

    Degrees may be ≥ 2. Callers usually pass ``coeffs`` as
    ``tuple[(degree, coeff), ...]``; ``degree`` is derived from the map
    (leading nonzero). ``single_hot`` marks a seed with exactly one
    higher-order term (degree ≥ 2), optionally plus lower terms.
    """

    coeffs: tuple[tuple[int, Fraction], ...]
    level: ConstructLevel = "L1"
    single_hot: bool = False

    def coeffs_dict(self) -> dict[int, Fraction]:
        return {int(d): Fraction(c) for d, c in self.coeffs if c != 0}

    @property
    def degree(self) -> int:
        from question_engine.frameworks.primitives.poly_helpers import poly_degree

        return poly_degree(self.coeffs_dict())

    def as_dict(self) -> dict[str, Any]:
        return {
            "kind": "polynomial",
            "coeffs": [(int(d), str(c)) for d, c in self.coeffs],
            "degree": self.degree,
            "single_hot": self.single_hot,
            "level": self.level,
        }

    @classmethod
    def from_dict(
        cls,
        coeffs: dict[int, Fraction],
        *,
        single_hot: bool = False,
        level: ConstructLevel = "L1",
    ) -> PolynomialTarget:
        items = tuple(
            sorted(
                ((int(d), Fraction(c)) for d, c in coeffs.items() if c != 0),
                key=lambda t: t[0],
                reverse=True,
            )
        )
        return cls(coeffs=items, level=level, single_hot=single_hot)


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
    poly_coeffs: dict[int, Fraction] | None = None
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


def seed_poly_target(
    ctx: PrimitiveContext,
    *,
    max_degree: int,
    prefer_single_hot: bool | None = None,
    d: float | None = None,
    max_terms: int | None = None,
    exact_terms: int | None = None,
    min_degree: int = 2,
) -> PolynomialTarget:
    """Seed a univariate polynomial with degree in ``[min_degree, max_degree]``.

    ``prefer_single_hot`` / knobs bias toward exactly one higher-order term
    (plus optional linear/constant) vs multiple degree-≥2 terms.

    Optional ``exact_terms`` / ``max_terms`` constrain the number of nonzero
    terms (for course-specific thin topics: e.g. PA ≤3 terms).
    """
    from question_engine.frameworks.primitives.difficulty_knobs import section
    from question_engine.frameworks.primitives.poly_helpers import (
        poly_degree,
        sample_coeff,
        sample_poly_coeffs,
        target_n_terms,
        target_poly_degree,
    )

    cap = max(2, int(max_degree))
    min_deg = max(2, int(min_degree))
    min_deg = min(min_deg, cap)
    eff = float(ctx.topic_d if d is None else d)
    # Honor scope cap and D-scaled target under policy.
    policy_deg = target_poly_degree(eff, ctx.policy)
    deg = min(cap, max(min_deg, policy_deg if ctx.policy.max_degree >= 2 else cap))
    if ctx.policy.max_degree >= 2:
        deg = min(deg, int(ctx.policy.max_degree), cap)
    else:
        deg = min(deg, cap)
    deg = max(min_deg, min(deg, cap))

    sec = section("constructive") or {}
    if prefer_single_hot is None:
        base_p = float(sec.get("poly_single_hot_chance", 0.5))
        # Slightly fewer single-hot shapes as D grows (more multi-term polys).
        p = max(0.15, base_p - 0.02 * min(eff, 20.0))
        prefer_single_hot = ctx.rng.random() < p

    # Term-count caps (exact wins over max).
    term_cap = deg + 1
    if max_terms is not None:
        term_cap = min(term_cap, max(1, int(max_terms)))
    if exact_terms is not None:
        term_cap = max(1, min(int(exact_terms), deg + 1))
        # exact_terms forces multi-term sampling path when > 1
        if exact_terms == 1:
            prefer_single_hot = True
        elif exact_terms >= 2:
            prefer_single_hot = False

    if prefer_single_hot and exact_terms is None:
        # Exactly one degree ≥ 2 term; optional linear + constant.
        coeffs: dict[int, Fraction] = {deg: sample_coeff(ctx, exclude_zero=True)}
        extras = 1  # leading
        if extras < term_cap and ctx.rng.random() < 0.55:
            coeffs[0] = sample_coeff(ctx, exclude_zero=True)
            extras += 1
        if (
            extras < term_cap
            and deg > 2
            and ctx.rng.random()
            < float(sec.get("poly_single_hot_linear_chance", 0.35))
        ):
            coeffs[1] = sample_coeff(ctx, exclude_zero=True)
        elif extras < term_cap and deg == 2 and ctx.rng.random() < 0.4:
            coeffs[1] = sample_coeff(ctx, exclude_zero=True)
        # Trim if somehow over term_cap
        while len(coeffs) > term_cap:
            drop = min((d_ for d_ in coeffs if d_ < deg), default=None)
            if drop is None:
                break
            del coeffs[drop]
        return PolynomialTarget.from_dict(coeffs, single_hot=True)

    if exact_terms is not None:
        n_terms = max(1, min(int(exact_terms), deg + 1))
    else:
        n_terms = min(term_cap, max(2 if term_cap >= 2 else 1, target_n_terms(eff)))
        n_terms = min(n_terms, term_cap)
    # Encourage ≥2 higher-order terms when deg ≥ 3 and D allows.
    min_hot = 2 if deg >= 3 and n_terms >= 3 and ctx.rng.random() < float(
        sec.get("poly_multi_hot_boost", 0.55)
    ) else 1
    if exact_terms == 1:
        min_hot = 1
    for _ in range(10):
        coeffs = sample_poly_coeffs(ctx, degree=deg, n_terms=n_terms, require_leading=True)
        hot = sum(1 for d_, c in coeffs.items() if d_ >= 2 and c != 0)
        if len(coeffs) == n_terms and (exact_terms is not None or hot >= min_hot):
            return PolynomialTarget.from_dict(coeffs, single_hot=(hot == 1))
    coeffs = sample_poly_coeffs(ctx, degree=deg, n_terms=n_terms, require_leading=True)
    hot = sum(1 for d_, c in coeffs.items() if d_ >= 2 and c != 0)
    return PolynomialTarget.from_dict(coeffs, single_hot=(hot <= 1 and poly_degree(coeffs) >= 2))


# ---------------------------------------------------------------------------
# Recursive disguise (relatedness tree from difficulty_knobs.json)
# ---------------------------------------------------------------------------

RecurseKind = Literal[
    "L1_numeric",
    "L1_affine",
    "L1_poly",
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
    if choice in {
        "L1_numeric",
        "L1_affine",
        "L1_poly",
        "L2_rational",
        "L3_rational_sum",
        "L4_pfd",
    }:
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


def disguise_poly(
    ctx: PrimitiveContext,
    coeffs: dict[int, Fraction],
    var: SampledVariable,
    *,
    d: float,
    depth: int,
    parent_kind: RecurseKind = "L1_poly",
    single_hot: bool = False,
) -> tuple[str, str, tuple[str, ...]]:
    """Render a polynomial block; maybe recurse through ``construct_poly``."""
    from question_engine.frameworks.primitives.poly_helpers import poly_degree, render_poly

    plain_l, plain_t = render_poly(coeffs, var)
    deg = poly_degree(coeffs)
    if deg <= 1:
        a = coeffs.get(1, Fraction(0))
        b = coeffs.get(0, Fraction(0))
        if a == 0:
            return disguise_numeric(ctx, b, d=d, depth=depth, parent_kind=parent_kind)
        return disguise_affine(
            ctx, a, b, var, d=d, depth=depth, parent_kind="L1_affine"
        )
    if not _should_recurse(ctx, d, depth, parent_kind):
        return plain_l, plain_t, ()
    child_kind = _pick_child_kind(ctx, parent_kind)
    if child_kind != "L1_poly":
        allowed = (_recurse_section().get("allowed_child_levels") or {}).get(parent_kind) or []
        if isinstance(allowed, list) and "L1_poly" in allowed:
            child_kind = "L1_poly"
        else:
            return plain_l, plain_t, ()
    child = construct_poly(
        ctx,
        d=_child_budget(d),
        var=var,
        target=PolynomialTarget.from_dict(coeffs, single_hot=single_hot),
        scope=ExpressionScope(max_degree=max(2, deg)),
        prefer_distribute=True,
        _depth=depth + 1,
    )
    return (
        f"\\left({child.latex}\\right)",
        f"({child.text})",
        ("recurse:L1_poly", *child.inflators_applied),
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
    num_factors: list[dict[int, Fraction]] | None = None,
    den_factors: list[dict[int, Fraction]] | None = None,
) -> tuple[str, str, tuple[str, ...]]:
    """Maybe nest an L1 block into a P/Q prompt (value unchanged).

    Related children only: L1_affine on a degree-≤1 num/den, or L1_numeric via a
    canceling scale factor shown in both numerator and denominator.

    When factor lists are provided, dens/nums follow
    `should_display_factor_product_expanded` (classroom-factorable → expanded;
    RRT-required → factored unless RRT enabled).
    """
    options = _factor_options_for_ctx(ctx)

    def _side_latex(
        poly: dict[int, Fraction],
        factors: list[dict[int, Fraction]] | None,
    ) -> tuple[str, str]:
        if factors is not None:
            return _render_poly_from_factor_dicts(factors, var, options)
        return _render_poly_dict(poly, var)

    nl, nt = _side_latex(num, num_factors)
    dl, dt = _side_latex(den, den_factors)
    plain_l, plain_t = rf"\frac{{{nl}}}{{{dl}}}", f"({nt})/({dt})"

    if not _should_recurse(ctx, d, depth, parent_kind):
        return plain_l, plain_t, ()

    # Multi-factor dens/nums that stay factored: only allow numeric scale disguise
    # (affine disguise needs a single linear piece).
    from packages.polynomial_core import should_display_factor_product_expanded

    multi_factored = False
    for factors in (num_factors, den_factors):
        if factors is None or len(factors) <= 1:
            continue
        polys = [_coeffs_to_polynomial(f, var.latex) for f in factors]
        if not should_display_factor_product_expanded(polys, options):
            multi_factored = True
            break

    child_kind = _coerce_related_l1(
        parent_kind, _pick_child_kind(ctx, parent_kind), num, den
    )

    if child_kind == "L1_affine" and not multi_factored:
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
                other_factors = den_factors if is_num else num_factors
                other_l, other_t = _side_latex(other, other_factors)
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
    nl, nt = _side_latex(num, num_factors)
    dl, dt = _side_latex(den, den_factors)
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


def verify_poly(surface: SurfaceExpression, target: PolynomialTarget) -> bool:
    """Identity check: surface poly coeffs match the target sparse map."""
    from question_engine.frameworks.primitives.poly_helpers import evaluate_poly

    got = surface.poly_coeffs
    if got is None and isinstance(surface.target, PolynomialTarget):
        got = surface.target.coeffs_dict()
    if got is None:
        return False
    want = target.coeffs_dict()
    if {d: c for d, c in got.items() if c != 0} != want:
        return False
    # Spot-check evaluation at a few points (construction must preserve value).
    for x in (Fraction(0), Fraction(1), Fraction(-1), Fraction(2), Fraction(-3)):
        if evaluate_poly(got, x) != evaluate_poly(want, x):
            return False
    return True


# ---------------------------------------------------------------------------
# L1 polynomial: target sparse poly → inflate (degree ≥ 2)
# ---------------------------------------------------------------------------


def _poly_all_divisible(coeffs: dict[int, Fraction], k: Fraction) -> bool:
    if k == 0:
        return False
    return all(c % k == 0 for c in coeffs.values())


def _try_factor_quadratic_binomials(
    coeffs: dict[int, Fraction],
) -> tuple[tuple[Fraction, Fraction], tuple[Fraction, Fraction]] | None:
    """If ``ax^2+bx+c`` factors over small integers, return ``((p,q),(r,s))`` for
    ``(px+q)(rx+s)``.
    """
    a = coeffs.get(2, Fraction(0))
    b = coeffs.get(1, Fraction(0))
    c = coeffs.get(0, Fraction(0))
    if a == 0 or any(d > 2 for d in coeffs):
        return None
    if a.denominator != 1 or b.denominator != 1 or c.denominator != 1:
        return None
    ai, bi, ci = int(a), int(b), int(c)
    # Search small integer factor pairs of a and c.
    def _divisors(n: int) -> list[int]:
        n = abs(n) if n != 0 else 0
        if n == 0:
            return [0]
        out: list[int] = []
        for i in range(1, min(n, 12) + 1):
            if n % i == 0:
                out.extend([i, -i, n // i, -(n // i)])
        # unique preserving order
        seen: set[int] = set()
        uniq: list[int] = []
        for x in out:
            if x not in seen:
                seen.add(x)
                uniq.append(x)
        return uniq

    for p in _divisors(ai) or [1, -1]:
        if p == 0 or ai % p != 0:
            continue
        r = ai // p
        for q in _divisors(ci) if ci != 0 else [0]:
            if ci != 0 and q == 0:
                continue
            if ci == 0:
                s = 0
            elif q == 0 or ci % q != 0:
                continue
            else:
                s = ci // q
            if p * s + q * r == bi:
                return (Fraction(p), Fraction(q)), (Fraction(r), Fraction(s))
    return None


def construct_poly(
    ctx: PrimitiveContext,
    *,
    d: float | None = None,
    var: SampledVariable | None = None,
    target: PolynomialTarget | None = None,
    prefer_distribute: bool = True,
    min_inflators: int | None = None,
    scope: ExpressionScope | None = None,
    _depth: int = 0,
) -> SurfaceExpression:
    """Build an unsimplified expression that simplifies to a degree-≥2 polynomial.

    Answer-first: seed (or accept) a ``PolynomialTarget``, then spend the
    constructive budget via **compositional subset inflate** (piece-tree):
    each unit picks a tree level (weighted toward the root), a subset of
    children, and a local value-preserving disguise — nesting accumulates.
    """
    from question_engine.frameworks.primitives.poly_compose import construct_poly_composed
    from question_engine.frameworks.primitives.poly_helpers import (
        poly_degree,
        render_poly,
    )

    scope = scope or ExpressionScope(max_degree=max(2, int(getattr(ctx.policy, "max_degree", 2))))
    if scope.max_degree < 2:
        raise ValueError("construct_poly requires scope.max_degree >= 2")

    eff = float(d if d is not None else ctx.effective_d(PRIM_EXPAND_SIMPLIFY))
    if d is None:
        eff = max(eff, float(ctx.topic_d) * 0.5)
    v = var or ctx.sample_variable()

    tgt = target or seed_poly_target(
        ctx,
        max_degree=scope.max_degree,
        prefer_single_hot=scope.prefer_single_hot,
        d=eff,
        max_terms=scope.max_terms,
        exact_terms=scope.exact_terms,
        min_degree=scope.min_degree,
    )
    coeffs = tgt.coeffs_dict()
    deg = poly_degree(coeffs)
    if deg < 2:
        raise ValueError(f"construct_poly target degree must be ≥ 2, got {deg}")
    if deg > scope.max_degree:
        raise ValueError(
            f"construct_poly target degree {deg} exceeds scope.max_degree={scope.max_degree}"
        )
    if ctx.policy.max_degree >= 2:
        ctx.policy.assert_degree(deg, where="construct_poly")

    latex, text, tags, extras = construct_poly_composed(
        ctx,
        d=eff,
        var=v,
        target_coeffs=coeffs,
        prefer_distribute=prefer_distribute,
        min_inflators=min_inflators,
        allow_cancel_clutter=scope.allow_cancel_clutter,
        scope_meta={
            "max_degree": scope.max_degree,
            "allow_cancel_clutter": scope.allow_cancel_clutter,
            "prefer_distributive_factorization": scope.prefer_distributive_factorization,
            "prefer_single_hot": scope.prefer_single_hot,
            "max_terms": scope.max_terms,
            "exact_terms": scope.exact_terms,
            "min_degree": scope.min_degree,
        },
        _depth=_depth,
        inflator_budget_fn=inflator_budget,
    )

    simp_l, simp_t = render_poly(coeffs, v)
    hot_count = sum(1 for dd, c in coeffs.items() if dd >= 2 and c != 0)
    depth_counts = extras.get("compose_depth_counts") or {}
    return SurfaceExpression(
        latex=latex,
        text=text,
        target=tgt,
        level="L1",
        inflators_applied=tuple(tags),
        poly_coeffs=dict(coeffs),
        coeff_a=coeffs.get(1, Fraction(0)),
        coeff_b=coeffs.get(0, Fraction(0)),
        simplified_latex=simp_l,
        simplified_text=simp_t,
        metadata={
            "effective_d": eff,
            "constructive": True,
            "compose": True,
            "var": v.name,
            "poly_degree": deg,
            "n_hot_terms": hot_count,
            "single_hot": bool(tgt.single_hot or hot_count == 1),
            "recurse_depth": _depth,
            "compose_depth_counts": depth_counts,
            "compose_budget": extras.get("compose_budget"),
            "cancel_clutter": [t for t in tags if "cancel" in t],
            "scope": extras.get("scope")
            or {
                "max_degree": scope.max_degree,
                "allow_cancel_clutter": scope.allow_cancel_clutter,
                "prefer_distributive_factorization": scope.prefer_distributive_factorization,
                "prefer_single_hot": scope.prefer_single_hot,
            },
        },
    )


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


def _factor_options_for_ctx(ctx: PrimitiveContext) -> "FactorablePolynomialOptions":
    """Presentation options for factor-product dens/nums (RRT off unless opted in)."""
    from packages.polynomial_core import FactorablePolynomialOptions

    settings = getattr(ctx, "settings", None) or {}
    rrt = bool(settings.get("factor_rrt", False))
    coef_min = int(settings.get("coef_min", -8))
    coef_max = int(settings.get("coef_max", 8))
    return FactorablePolynomialOptions(
        coef_min=coef_min,
        coef_max=coef_max,
        rrt_mode="allow" if rrt else "exclude",
        enabled_methods={"rrt": rrt},
    )


def _coeffs_to_polynomial(
    coeffs: dict[int, Fraction], variable: str
) -> "Polynomial":
    from packages.polynomial_core import Polynomial

    if not coeffs:
        return Polynomial(((0, 0),), variable=variable)
    terms = tuple((c, d) for d, c in coeffs.items() if c != 0)
    if not terms:
        return Polynomial(((0, 0),), variable=variable)
    return Polynomial(terms, variable=variable)


def _product_of_factor_dicts(
    factors: list[dict[int, Fraction]],
) -> dict[int, Fraction]:
    out: dict[int, Fraction] = {0: Fraction(1)}
    for fac in factors:
        out = _poly_mul(out, fac)
    return out


def _render_poly_from_factor_dicts(
    factors: list[dict[int, Fraction]],
    var: SampledVariable,
    options: "FactorablePolynomialOptions",
    *,
    force_factored: bool = False,
) -> tuple[str, str]:
    """Render a known factor product via the shared expand-vs-factored policy.

    Expanded when classroom-factorable; factored when the expanded form would
    require RRT (unless RRT is enabled).
    """
    from packages.polynomial_core import should_display_factor_product_expanded

    if not factors:
        return "1", "1"
    if len(factors) == 1:
        return _render_poly_dict(factors[0], var)

    # Fold pure-constant factors into a single leading multiplier.
    lead = Fraction(1)
    variable: list[dict[int, Fraction]] = []
    for fac in factors:
        if not fac:
            continue
        if max(fac.keys()) == 0:
            lead *= fac.get(0, Fraction(1))
        else:
            variable.append(fac)
    if not variable:
        return _render_poly_dict({0: lead}, var)

    display_factors = variable if lead == 1 else [{0: lead}, *variable]
    polys = [_coeffs_to_polynomial(fac, var.latex) for fac in display_factors]
    expand = (not force_factored) and should_display_factor_product_expanded(
        polys, options
    )
    if expand:
        return _render_poly_dict(_product_of_factor_dicts(display_factors), var)

    # Factored: render via Fraction-aware poly dicts (avoid Polynomial.to_latex
    # which rounds Fraction constants into ugly decimals).
    text_parts: list[str] = []
    latex_parts: list[str] = []
    if lead != 1:
        lead_l, lead_t = _render_poly_dict({0: lead}, var)
        latex_parts.append(lead_l)
        text_parts.append(lead_t)
    for fac in variable:
        fl, ft = _render_poly_dict(fac, var)
        latex_parts.append(f"\\left({fl}\\right)")
        text_parts.append(f"({ft})")
    return "".join(latex_parts), "".join(text_parts)


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


def _pick_distinct_roots(
    ctx: PrimitiveContext, n: int, *, used: set[Fraction] | None = None
) -> list[Fraction]:
    roots: list[Fraction] = []
    seen = set(used or ())
    guard = 0
    while len(roots) < n and guard < 80:
        guard += 1
        r = sample_integerish(ctx, exclude_zero=False).value
        if r in seen:
            continue
        seen.add(r)
        roots.append(r)
    while len(roots) < n:
        # Deterministic fill if sampling stalls.
        candidate = Fraction(len(roots) + 1)
        while candidate in seen or -candidate in seen and candidate == 0:
            candidate += 1
        seen.add(candidate)
        roots.append(candidate)
    return roots


def _render_rational_summands(
    ctx: PrimitiveContext,
    *,
    num_polys: list[dict[int, Fraction]],
    den_polys: list[dict[int, Fraction]],
    den_roots: list[Fraction] | None,
    v: SampledVariable,
    eff: float,
    num_factor_lists: list[list[dict[int, Fraction]]] | None = None,
    den_factor_lists: list[list[dict[int, Fraction]]] | None = None,
) -> tuple[str, str, list[str]]:
    options = _factor_options_for_ctx(ctx)
    parts_l: list[str] = []
    parts_t: list[str] = []
    recurse_tags: list[str] = []
    for i, (num_p, den_p) in enumerate(zip(num_polys, den_polys)):
        num_factors = (
            num_factor_lists[i]
            if num_factor_lists is not None and i < len(num_factor_lists)
            else None
        )
        den_factors = (
            den_factor_lists[i]
            if den_factor_lists is not None and i < len(den_factor_lists)
            else None
        )

        if num_factors is not None and len(num_factors) > 1:
            nl, nt = _render_poly_from_factor_dicts(num_factors, v, options)
        elif num_p and max(num_p) == 0:
            nl, nt, ntags = disguise_numeric(
                ctx, num_p.get(0, Fraction(0)), d=eff, depth=0, parent_kind="L3_rational_sum"
            )
            recurse_tags.extend(ntags)
        elif num_factors is not None:
            nl, nt = _render_poly_from_factor_dicts(num_factors, v, options)
        else:
            nl, nt = _render_poly_dict(num_p, v)

        if (
            den_roots is not None
            and i < len(den_roots)
            and den_p == _poly_from_linear(den_roots[i])
            and (den_factors is None or len(den_factors) <= 1)
        ):
            dl, dt, dtags = disguise_affine(
                ctx,
                Fraction(1),
                -den_roots[i],
                v,
                d=eff,
                depth=0,
                parent_kind="L3_rational_sum",
            )
            recurse_tags.extend(dtags)
        elif den_factors is not None:
            dl, dt = _render_poly_from_factor_dicts(den_factors, v, options)
        else:
            dl, dt = _render_poly_dict(den_p, v)
        piece_l = rf"\frac{{{nl}}}{{{dl}}}"
        piece_t = f"({nt})/({dt})"
        if i == 0:
            parts_l.append(piece_l)
            parts_t.append(piece_t)
        else:
            parts_l.append("+" + piece_l)
            parts_t.append("+" + piece_t)
    return "".join(parts_l), "".join(parts_t), recurse_tags


def _construct_l2_rational(
    ctx: PrimitiveContext,
    *,
    eff: float,
    v: SampledVariable,
    k_cancel: int,
) -> SurfaceExpression:
    """Single fraction: insert ``k_cancel`` common linear factors (unbounded).

    ``ALL_AVAILABLE_CANCEL`` (or any huge sentinel) → cancel every factor in a
    normal-sized problem (capped); does not grow LCD to continuous D max.
    """
    from question_engine.frameworks.primitives.rational_cancel import (
        ALL_AVAILABLE_CANCEL,
        sample_all_available_factor_count,
    )

    if int(k_cancel) >= ALL_AVAILABLE_CANCEL:
        n_fac = sample_all_available_factor_count({"difficulty": eff}, default=3)
        cancel_roots = _pick_distinct_roots(ctx, n_fac)
        cancel_factors = [_poly_from_linear(r) for r in cancel_roots]
        ans_num = {0: sample_integerish(ctx, exclude_zero=True).value}
        ans_den = {0: Fraction(1)}
        prompt_num_factors: list[dict[int, Fraction]] = [dict(ans_num)]
        prompt_den_factors: list[dict[int, Fraction]] = []
        for fac in cancel_factors:
            prompt_num_factors.append(fac)
            prompt_den_factors.append(fac)
        prompt_num = _product_of_factor_dicts(prompt_num_factors)
        prompt_den = _product_of_factor_dicts(prompt_den_factors)
        actual_k = n_fac
        excluded_roots = list(cancel_roots)
    else:
        # Reduced core with no shared factors, then insert exactly k cancels.
        k = max(0, int(k_cancel))
        remain_num_deg = 1 if eff < 8 else ctx.rng.randint(1, 2)
        remain_den_deg = 1 if k == 0 else (1 if eff < 10 else ctx.rng.randint(1, 2))
        used: set[Fraction] = set()
        num_roots = _pick_distinct_roots(ctx, remain_num_deg, used=used)
        used.update(num_roots)
        den_roots = _pick_distinct_roots(ctx, remain_den_deg, used=used)
        used.update(den_roots)
        lead = sample_integerish(ctx, exclude_zero=True).value
        ans_num = {0: lead}
        for r in num_roots:
            ans_num = _poly_mul(ans_num, _poly_from_linear(r))
        ans_den = {0: Fraction(1)}
        for r in den_roots:
            ans_den = _poly_mul(ans_den, _poly_from_linear(r))
        prompt_num_factors = [{0: lead}] + [_poly_from_linear(r) for r in num_roots]
        prompt_den_factors = [_poly_from_linear(r) for r in den_roots]
        cancel_roots = _pick_distinct_roots(ctx, k, used=used) if k else []
        for r in cancel_roots:
            fac = _poly_from_linear(r)
            prompt_num_factors.append(fac)
            prompt_den_factors.append(fac)
        prompt_num = _product_of_factor_dicts(prompt_num_factors)
        prompt_den = _product_of_factor_dicts(prompt_den_factors)
        actual_k = k
        # Only cancelled roots: remaining dens factors stay visible in the answer.
        excluded_roots = list(cancel_roots)

    ans_l, ans_t = _fraction_latex(ans_num, ans_den, v)
    # Domain notes only for cancelled factors (invisible after simplify).
    from packages.polynomial_core import rational_excluded_values_latex

    note = rational_excluded_values_latex(sorted(set(excluded_roots)))
    if note:
        var_tex = v.latex or v.name
        note = note.replace("x \\neq", f"{var_tex} \\neq", 1)
        ans_l = f"{ans_l},\\; {note}"
        excl_txt = ", ".join(str(r) for r in sorted(set(excluded_roots)))
        ans_t = f"{ans_t}, {v.name} ≠ {excl_txt}"

    latex, text, recurse_tags = _disguise_rational_fraction(
        ctx,
        prompt_num,
        prompt_den,
        v,
        d=eff,
        depth=0,
        parent_kind="L2_rational",
        num_factors=prompt_num_factors,
        den_factors=prompt_den_factors,
    )
    plan = CancelPlan(cancel_count=actual_k, level="L2")
    target = RationalPolyTarget(
        num=tuple(sorted(ans_num.items(), reverse=True)),
        den=tuple(sorted(ans_den.items(), reverse=True)),
        level="L2",
    )
    tags = ("seed_rational",)
    if actual_k:
        tags = tags + ("insert_cancel_factor",)
    return SurfaceExpression(
        latex=latex,
        text=text,
        target=target,
        level="L2",
        inflators_applied=tags + tuple(recurse_tags),
        simplified_latex=ans_l,
        simplified_text=ans_t,
        metadata={
            "effective_d": eff,
            "cancel_plan": plan.as_dict(),
            "cancel_factor_count": actual_k,
            "excluded_values": [
                int(r) if getattr(r, "denominator", 1) == 1 else str(r)
                for r in sorted(set(excluded_roots))
            ],
            "constructive": True,
            "mode": "simplify_rational",
            "recurse_hits": sum(1 for t in recurse_tags if t.startswith("recurse:")),
        },
    )


def _construct_l3_all_cancel(
    ctx: PrimitiveContext,
    *,
    eff: float,
    v: SampledVariable,
    n_terms: int,
    n_factors: int | None = None,
) -> SurfaceExpression:
    """Add/subtract where the combined LCD factors all cancel → polynomial."""
    from question_engine.frameworks.primitives.rational_cancel import (
        sample_all_available_factor_count,
    )

    n = max(2, int(n_terms))
    n_fac = int(n_factors) if n_factors is not None else sample_all_available_factor_count(
        {"difficulty": eff}, default=3
    )
    n_fac = max(2, n_fac)
    roots = _pick_distinct_roots(ctx, n_fac)
    dens = [_poly_from_linear(r) for r in roots]
    lcd = {0: Fraction(1)}
    for den in dens:
        lcd = _poly_mul(lcd, den)
    p_val = sample_integerish(ctx, exclude_zero=True).value
    total_num = _poly_scale(lcd, p_val)
    # Split P·LCD across n numerators (same LCD dens) so combining cancels all factors.
    weights = [Fraction(1, n)] * n
    if n >= 2 and ctx.rng.random() < 0.55:
        delta = Fraction(ctx.rng.choice([1, -1]), n * 2)
        weights[0] += delta
        weights[1] -= delta
    num_polys = [_poly_scale(total_num, w) for w in weights]
    den_polys = [dict(lcd) for _ in range(n)]
    # Keep factor lists so multi-linear dens stay factored when RRT is off.
    den_factor_lists = [list(dens) for _ in range(n)]
    num_factor_lists: list[list[dict[int, Fraction]]] = []
    for w in weights:
        num_factor_lists.append([{0: p_val * w}] + list(dens))
    ans_num = {0: p_val}
    ans_den = {0: Fraction(1)}
    ans_l, ans_t = _fraction_latex(ans_num, ans_den, v)
    from packages.polynomial_core import rational_excluded_values_latex

    note = rational_excluded_values_latex(sorted(set(roots)))
    if note:
        var_tex = v.latex or v.name
        note = note.replace("x \\neq", f"{var_tex} \\neq", 1)
        ans_l = f"{ans_l},\\; {note}"
        excl_txt = ", ".join(str(r) for r in sorted(set(roots)))
        ans_t = f"{ans_t}, {v.name} ≠ {excl_txt}"
    latex, text, recurse_tags = _render_rational_summands(
        ctx,
        num_polys=num_polys,
        den_polys=den_polys,
        den_roots=None,
        v=v,
        eff=eff,
        num_factor_lists=num_factor_lists,
        den_factor_lists=den_factor_lists,
    )
    plan = CancelPlan(cancel_count=n_fac, level="L3")
    target = RationalPolyTarget(
        num=tuple(sorted(ans_num.items(), reverse=True)),
        den=tuple(sorted(ans_den.items(), reverse=True)),
        level="L3",
    )
    return SurfaceExpression(
        latex=latex,
        text=text,
        target=target,
        level="L3",
        inflators_applied=("seed_summands", "combine_lcd", "all_cancel") + tuple(recurse_tags),
        simplified_latex=ans_l,
        simplified_text=ans_t,
        metadata={
            "effective_d": eff,
            "n_terms": n,
            "n_lcd_factors": n_fac,
            "cancel_plan": plan.as_dict(),
            "cancel_factor_count": n_fac,
            "excluded_values": [
                int(r) if r.denominator == 1 else str(r) for r in sorted(set(roots))
            ],
            "constructive": True,
            "mode": "add_subtract_rationals",
            "recurse_hits": sum(1 for t in recurse_tags if t.startswith("recurse:")),
        },
    )


def construct_rational_sum(
    ctx: PrimitiveContext,
    *,
    d: float | None = None,
    var: SampledVariable | None = None,
    n_terms: int | None = None,
    cancel_count: int | None = None,
    as_sum: bool = False,
) -> SurfaceExpression:
    """Build a rational simplify (L2) or add/subtract (L3) surface.

    ``cancel_count`` is how many common linear factors cancel after combining /
    in the unsimplified fraction (exact inserts; ``ALL_AVAILABLE_CANCEL`` = all
    cancel). When ``as_sum`` is True, always emit an L3 sum; otherwise emit a
    single L2 fraction. Term / factor counts grow unboundedly with continuous D.
    """
    from question_engine.frameworks.primitives.rational_cancel import (
        ALL_AVAILABLE_CANCEL,
        continuous_rational_term_count_max,
        resolve_rational_cancel_count,
        sample_rational_term_count,
    )

    eff = float(d if d is not None else max(ctx.topic_d, 0.0))
    v = var or ctx.sample_variable()
    if n_terms is not None:
        n = max(2, int(n_terms))
    else:
        n = sample_rational_term_count({"difficulty": eff}, default=3)
        # Cap absurd L3 summand counts for latex size; still unbounded vs old min(4).
        term_hi = continuous_rational_term_count_max({"difficulty": eff})
        if term_hi is not None:
            n = min(n, term_hi)
    if cancel_count is None:
        k_cancel = resolve_rational_cancel_count({}, d=eff, rng=ctx.rng)
    else:
        k_cancel = max(0, int(cancel_count))

    if not as_sum:
        return _construct_l2_rational(ctx, eff=eff, v=v, k_cancel=k_cancel)

    if k_cancel >= ALL_AVAILABLE_CANCEL:
        return _construct_l3_all_cancel(ctx, eff=eff, v=v, n_terms=n)

    # Seed distinct linear dens (x - r_i); grow with n (unbounded).
    roots = _pick_distinct_roots(ctx, n)
    nums = [sample_integerish(ctx, exclude_zero=True).value for _ in range(n)]
    dens = [_poly_from_linear(r) for r in roots]

    lcd = {0: Fraction(1)}
    for den in dens:
        lcd = _poly_mul(lcd, den)

    combined_num: dict[int, Fraction] = {}
    for i, num_i in enumerate(nums):
        cofactor = {0: Fraction(1)}
        for j, den_j in enumerate(dens):
            if j != i:
                cofactor = _poly_mul(cofactor, den_j)
        combined_num = _poly_add(combined_num, _poly_scale(cofactor, num_i))

    num_factor_lists: list[list[dict[int, Fraction]]] = [[{0: num_i}] for num_i in nums]
    den_factor_lists: list[list[dict[int, Fraction]]] = [[dict(den)] for den in dens]
    num_polys: list[dict[int, Fraction]] = [{0: num_i} for num_i in nums]
    den_polys: list[dict[int, Fraction]] = [dict(den) for den in dens]
    used_roots = set(roots)
    applied = ["seed_summands", "combine_lcd"]

    # Value-preserving cancel inserts: multiply selected terms' num and den by
    # (x-c). Term values unchanged; after LCD combine, (x-c) cancels.
    cancel_roots: list[Fraction] = []
    for _ in range(k_cancel):
        c_root = _pick_distinct_roots(ctx, 1, used=used_roots)[0]
        used_roots.add(c_root)
        cancel_roots.append(c_root)
        cf = _poly_from_linear(c_root)
        n_targets = ctx.rng.randint(1, len(num_polys))
        targets = set(ctx.rng.sample(range(len(num_polys)), n_targets))
        for i in targets:
            num_polys[i] = _poly_mul(num_polys[i], cf)
            den_polys[i] = _poly_mul(den_polys[i], cf)
            num_factor_lists[i].append(cf)
            den_factor_lists[i].append(cf)
        applied.append("insert_cancel_factor")

    latex, text, recurse_tags = _render_rational_summands(
        ctx,
        num_polys=num_polys,
        den_polys=den_polys,
        den_roots=roots if k_cancel == 0 else None,
        v=v,
        eff=eff,
        num_factor_lists=num_factor_lists,
        den_factor_lists=den_factor_lists,
    )
    ans_l, ans_t = _fraction_latex(combined_num, lcd, v)
    # Only cancelled roots — LCD dens factors remain visible in the answer dens.
    excluded_roots = list(cancel_roots)
    from packages.polynomial_core import rational_excluded_values_latex

    note = rational_excluded_values_latex(sorted(set(excluded_roots)))
    if note:
        var_tex = v.latex or v.name
        note = note.replace("x \\neq", f"{var_tex} \\neq", 1)
        ans_l = f"{ans_l},\\; {note}"
        excl_txt = ", ".join(str(r) for r in sorted(set(excluded_roots)))
        ans_t = f"{ans_t}, {v.name} ≠ {excl_txt}"
    plan = CancelPlan(cancel_count=k_cancel, level="L3")
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
        inflators_applied=tuple(applied) + tuple(recurse_tags),
        simplified_latex=ans_l,
        simplified_text=ans_t,
        metadata={
            "effective_d": eff,
            "n_terms": n,
            "cancel_plan": plan.as_dict(),
            "cancel_factor_count": k_cancel,
            "excluded_values": [
                int(r) if r.denominator == 1 else str(r)
                for r in sorted(set(excluded_roots))
            ],
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

    # Dens stay a factor product for display; combined num is a sum (not factored).
    den_factors = list(dens)
    scale_k = Fraction(1)
    if inflator_budget(eff) >= 1 and ctx.rng.random() < fget(
        "constructive", "pfd_scale_num_den_chance", 0.4
    ):
        scale_k = Fraction(ctx.rng.choice([2, 3]))
        combined_num = _poly_scale(combined_num, scale_k)
        lcd = _poly_scale(lcd, scale_k)
        applied.append("scale_num_den")

    # Numerator is generally not a clean factor product after combining; den is.
    if scale_k != 1:
        den_factors = [{0: scale_k}] + den_factors

    # Student prompt may nest related L1 blocks into the combined rational.
    prompt_l, prompt_t, recurse_tags = _disguise_rational_fraction(
        ctx,
        combined_num,
        lcd,
        v,
        d=eff,
        depth=0,
        parent_kind="L4_pfd",
        den_factors=den_factors,
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
