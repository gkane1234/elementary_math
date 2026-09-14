"""General polynomial factor sampler — constraints + difficulty bias.

Hardness is **not** a separate magic shape ladder. Callers set a box:
  - min/max factor count (⇒ product degree for linear factors)
  - coef / constant ranges and constant type (int, fraction, …)
  - monic vs allow leading a≠1
  - hand-factorable / ``factor_rrt``
  - presentation: factored vs expanded product

Difficulty biases draws **inside** that box toward uglier factors (larger
coefs, a≠1, fractions if allowed). Low D biases simple (monic, small ints).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from math import gcd
from typing import Any, Literal

from question_engine.frameworks.primitives.poly_helpers import (
    multiply_coeffs,
    poly_degree,
    render_poly,
    scale_coeffs,
    wrap_parens,
)
from question_engine.frameworks.primitives.registry import PrimitiveContext

CoefType = Literal["int", "fraction"]
DensStyle = Literal["factored", "expanded", "auto"]
FactorKind = Literal[
    "linear",
    "diff_squares",
    "perfect_square",
    "grouping",
    "cubes",
    "quadratic_form",
    "mono_poly",
]

# Rational-lane default (AddSubCancel etc.): product of linears stays ≤ quadratic.
# Poly FactorProduct may raise ``max_product_degree`` as a real structural knob
# (grouping/cubes/quadratic-form/3-linear products) — never a cost pad.
DEFAULT_MAX_PRODUCT_DEGREE = 2
_KIND_SET = {
    "linear",
    "diff_squares",
    "perfect_square",
    "grouping",
    "cubes",
    "quadratic_form",
    "mono_poly",
}


@dataclass(frozen=True)
class FactorConstraints:
    """Box for sampling linear factors (and their product)."""

    min_factors: int = 1
    max_factors: int = 2
    # Leading coef a of ax+b
    leading_min: int = 1
    leading_max: int = 1  # monic-only by default; widen via D bias / settings
    allow_nonmonic: bool = False
    # Constant term b
    const_min: int = -4
    const_max: int = 4
    const_type: CoefType = "int"
    # Fraction constants (only if const_type == "fraction")
    frac_den_max: int = 3
    require_content_primitive: bool = True  # gcd(|a|,|b|)==1
    positive_leading: bool = True
    allow_zero_const: bool = False
    factor_rrt: bool = False
    dens_style: DensStyle = "auto"
    max_product_degree: int = DEFAULT_MAX_PRODUCT_DEGREE
    factor_kind: FactorKind = "linear"
    require_gcf: bool = False
    # Soft bias knobs (filled by ``constraints_from_settings``)
    nonmonic_weight: float = 0.0  # P(pick a≠1 | allow_nonmonic)
    coef_abs_bias: float = 0.0  # 0 → prefer small |b|; 1 → uniform in range
    expand_weight: float = 0.0  # P(expanded presentation) when dens_style=auto

    def clamped(self) -> "FactorConstraints":
        cap = max(1, int(self.max_product_degree or DEFAULT_MAX_PRODUCT_DEGREE))
        mn = max(1, int(self.min_factors))
        mx = max(mn, int(self.max_factors))
        # Product of linears: each factor deg 1 ⇒ n_factors ≤ max product deg.
        mx = min(mx, cap)
        mn = min(mn, mx)
        lead_lo = max(1, int(self.leading_min))
        lead_hi = max(lead_lo, int(self.leading_max))
        if not self.allow_nonmonic:
            lead_lo = lead_hi = 1
        c_lo = int(self.const_min)
        c_hi = int(self.const_max)
        if c_lo > c_hi:
            c_lo, c_hi = c_hi, c_lo
        return FactorConstraints(
            min_factors=mn,
            max_factors=mx,
            leading_min=lead_lo,
            leading_max=lead_hi,
            allow_nonmonic=bool(self.allow_nonmonic) and lead_hi > 1,
            const_min=c_lo,
            const_max=c_hi,
            const_type="fraction" if self.const_type == "fraction" else "int",
            frac_den_max=max(1, int(self.frac_den_max)),
            require_content_primitive=bool(self.require_content_primitive),
            positive_leading=bool(self.positive_leading),
            allow_zero_const=bool(self.allow_zero_const),
            factor_rrt=bool(self.factor_rrt),
            dens_style=self.dens_style
            if self.dens_style in {"factored", "expanded", "auto"}
            else "auto",
            max_product_degree=cap,
            factor_kind=self.factor_kind if self.factor_kind in _KIND_SET else "linear",
            require_gcf=bool(self.require_gcf),
            nonmonic_weight=max(0.0, min(1.0, float(self.nonmonic_weight))),
            coef_abs_bias=max(0.0, min(1.0, float(self.coef_abs_bias))),
            expand_weight=max(0.0, min(1.0, float(self.expand_weight))),
        )


def constraints_from_settings(
    settings: dict[str, Any] | None,
    *,
    d: float = 0.0,
) -> FactorConstraints:
    """Build constraints from settings; difficulty biases weights / ranges."""
    from question_engine.frameworks.primitives.skeleton_difficulty import (
        SkeletonDifficultyBands,
        format_bias_for_tier,
        numeric_bias_for_tier,
    )

    s = dict(settings or {})
    d = max(0.0, float(d))
    rrt = bool(s.get("factor_rrt", False))
    bands = SkeletonDifficultyBands.from_d(d)
    num_bias = numeric_bias_for_tier(bands.numeric_tier)
    fmt_bias = format_bias_for_tier(bands.format_tier)

    # Explicit ranges win; else widen by numeric tier only (not raw D).
    const_hi_default = int(num_bias["const_hi_default"])
    const_lo = int(s.get("const_min", s.get("coef_min", -const_hi_default)))
    const_hi = int(s.get("const_max", s.get("coef_max", const_hi_default)))

    allow_nonmonic = bool(
        s.get(
            "allow_nonmonic",
            s.get("leading_coefficient_one", True) is False
            or s.get("monic_only", True) is False
            or d >= float(num_bias["allow_nonmonic_from_d"]),
        )
    )
    if "allow_nonmonic" in s:
        allow_nonmonic = bool(s["allow_nonmonic"])
    elif s.get("leading_coefficient_one") is True or s.get("monic_only") is True:
        allow_nonmonic = False
    elif s.get("leading_coefficient_one") is False or s.get("monic_only") is False:
        allow_nonmonic = True

    lead_max = int(
        s.get(
            "leading_max",
            1 if not allow_nonmonic else int(num_bias["leading_max_default"]),
        )
    )
    lead_min = int(s.get("leading_min", 1))

    # Numeric bias inside the box (tier-driven, not mixed with format).
    nonmonic_weight = float(s.get("nonmonic_weight", 0.0))
    if "nonmonic_weight" not in s:
        if not allow_nonmonic:
            nonmonic_weight = 0.0
        else:
            nonmonic_weight = float(num_bias["nonmonic_weight"])

    coef_abs_bias = float(s.get("coef_abs_bias", 0.0))
    if "coef_abs_bias" not in s:
        coef_abs_bias = float(num_bias["coef_abs_bias"])

    expand_weight = float(s.get("expand_weight", 0.0))
    if "expand_weight" not in s:
        expand_weight = float(fmt_bias["expand_weight"])

    dens_style: DensStyle = "auto"
    raw_style = s.get("dens_style")
    if raw_style in {"factored", "expanded", "auto"}:
        dens_style = raw_style  # type: ignore[assignment]

    raw_kind = str(s.get("factor_kind", "linear")).strip().lower()
    factor_kind: FactorKind = raw_kind if raw_kind in _KIND_SET else "linear"  # type: ignore[assignment]
    max_product_degree = int(s.get("max_product_degree", DEFAULT_MAX_PRODUCT_DEGREE))
    require_gcf = bool(s.get("require_gcf", False))

    const_type: CoefType = "int"
    raw_ct = str(s.get("const_type", s.get("coef_type", "int"))).lower()
    if raw_ct in {"fraction", "frac", "rational"}:
        const_type = "fraction"
        # Fraction constants unlock at numeric tier 3+ (D≥14), not with format tricks.
        if not num_bias["allow_fraction_const"] and "const_type" not in s and "coef_type" not in s:
            const_type = "int"

    min_f = int(s.get("min_factors", s.get("n_factors", 1)))
    max_f = int(s.get("max_factors", s.get("n_factors", 2)))
    if s.get("n_factors") is not None and "min_factors" not in s and "max_factors" not in s:
        min_f = max_f = int(s["n_factors"])

    return FactorConstraints(
        min_factors=min_f,
        max_factors=max_f,
        leading_min=lead_min,
        leading_max=lead_max,
        allow_nonmonic=allow_nonmonic,
        const_min=const_lo,
        const_max=const_hi,
        const_type=const_type,
        frac_den_max=int(s.get("frac_den_max", 3)),
        require_content_primitive=bool(s.get("content_primitive", True)) and not rrt,
        positive_leading=bool(s.get("positive_leading", True)),
        allow_zero_const=bool(s.get("allow_zero_const", False)),
        factor_rrt=rrt,
        dens_style=dens_style,
        max_product_degree=max_product_degree,
        factor_kind=factor_kind,
        require_gcf=require_gcf,
        nonmonic_weight=nonmonic_weight,
        coef_abs_bias=coef_abs_bias,
        expand_weight=expand_weight,
    ).clamped()


@dataclass(frozen=True)
class LinearFactor:
    """Linear factor ``a x + b`` (a ≠ 0)."""

    a: Fraction
    b: Fraction

    def coeffs(self) -> dict[int, Fraction]:
        return {1: Fraction(self.a), 0: Fraction(self.b)}

    def root(self) -> Fraction:
        return -Fraction(self.b) / Fraction(self.a)

    def eval_at(self, x: Fraction) -> Fraction:
        return Fraction(self.a) * x + Fraction(self.b)

    def is_monic(self) -> bool:
        return Fraction(self.a) == 1

    def as_dict(self) -> dict[str, Any]:
        return {
            "a": str(Fraction(self.a)),
            "b": str(Fraction(self.b)),
            "root": str(self.root()),
            "monic": self.is_monic(),
        }


@dataclass(frozen=True)
class PolyFactor:
    """Sparse univariate factor (linear, even binomial, cubes quadratic, …)."""

    terms: tuple[tuple[int, Fraction], ...]

    @classmethod
    def from_coeffs(cls, coeffs: dict[int, Fraction]) -> "PolyFactor":
        items = tuple(
            sorted((int(d), Fraction(c)) for d, c in coeffs.items() if c != 0)
        )
        return cls(terms=items)

    def coeffs(self) -> dict[int, Fraction]:
        return {d: c for d, c in self.terms}

    def degree(self) -> int:
        return max((d for d, _c in self.terms), default=0)

    def as_linear(self) -> LinearFactor | None:
        c = self.coeffs()
        if set(c) <= {0, 1} and c.get(1, Fraction(0)) != 0:
            return LinearFactor(a=c.get(1, Fraction(0)), b=c.get(0, Fraction(0)))
        return None

    def as_dict(self) -> dict[str, Any]:
        return {str(d): str(c) for d, c in self.terms}


@dataclass(frozen=True)
class FactorDraw:
    """Sampled factors + product (degree = product degree)."""

    factors: tuple[LinearFactor, ...]
    constraints: FactorConstraints
    dens_style: DensStyle
    product: dict[int, Fraction]
    effective_d: float
    poly_factors: tuple[PolyFactor, ...] = ()
    outer_gcf: Fraction = Fraction(1)
    factor_kind: str = "linear"

    @property
    def n_factors(self) -> int:
        if self.poly_factors:
            return len(self.poly_factors)
        return len(self.factors)

    @property
    def degree(self) -> int:
        return poly_degree(self.product) if self.product else len(self.factors)

    @property
    def factor_rrt(self) -> bool:
        return self.constraints.factor_rrt

    def as_dict(self) -> dict[str, Any]:
        c = self.constraints
        return {
            "n_factors": self.n_factors,
            "degree": self.degree,
            "dens_style": self.dens_style,
            "factor_kind": self.factor_kind,
            "outer_gcf": str(self.outer_gcf),
            "factors": [f.as_dict() for f in self.factors],
            "poly_factors": [f.as_dict() for f in self.poly_factors],
            "effective_d": self.effective_d,
            "factor_rrt": self.factor_rrt,
            "constraints": {
                "allow_nonmonic": c.allow_nonmonic,
                "leading_max": c.leading_max,
                "const_min": c.const_min,
                "const_max": c.const_max,
                "const_type": c.const_type,
                "max_product_degree": c.max_product_degree,
                "factor_kind": c.factor_kind,
                "require_gcf": c.require_gcf,
                "nonmonic_weight": c.nonmonic_weight,
                "coef_abs_bias": c.coef_abs_bias,
                "expand_weight": c.expand_weight,
            },
            # Convenience labels for galleries (derived, not a sampler ladder).
            "bias_label": _bias_label(c, self.dens_style),
        }


def _bias_label(c: FactorConstraints, dens_style: DensStyle) -> str:
    bits: list[str] = []
    bits.append("nonmonic" if c.allow_nonmonic and c.nonmonic_weight >= 0.4 else "monic_bias")
    if dens_style == "expanded":
        bits.append("expanded")
    if c.const_type == "fraction":
        bits.append("frac")
    return "+".join(bits)


def _var_stub(var_latex: str):
    from question_engine.frameworks.primitives.variables import SampledVariable

    return SampledVariable(
        name="x",
        effective_d=0.0,
        cost=0.0,
        locked=True,
        latex=var_latex or "x",
        profile="only_x",
    )


def _sample_int_biased(
    ctx: PrimitiveContext,
    lo: int,
    hi: int,
    *,
    abs_bias: float,
    exclude_zero: bool,
) -> int:
    """Sample int in [lo, hi]; low abs_bias prefers values near 0."""
    lo, hi = int(lo), int(hi)
    if lo > hi:
        lo, hi = hi, lo
    candidates = list(range(lo, hi + 1))
    if exclude_zero:
        candidates = [v for v in candidates if v != 0]
    if not candidates:
        return 1 if exclude_zero else 0
    if abs_bias <= 1e-9:
        # Prefer smallest |v|
        candidates.sort(key=lambda v: (abs(v), v))
        # Soft: top half of smallest
        cut = max(1, (len(candidates) + 1) // 2)
        return int(ctx.rng.choice(candidates[:cut]))
    if abs_bias >= 1.0 - 1e-9:
        return int(ctx.rng.choice(candidates))
    # Weight ∝ (1-bias)/(|v|+1) + bias  (mix small-prefer and uniform)
    weights: list[float] = []
    for v in candidates:
        w_small = 1.0 / (abs(v) + 1.0)
        w_uni = 1.0
        weights.append((1.0 - abs_bias) * w_small + abs_bias * w_uni)
    return int(ctx.rng.choices(candidates, weights=weights, k=1)[0])


def _sample_const(
    ctx: PrimitiveContext,
    cons: FactorConstraints,
) -> Fraction:
    if cons.const_type == "fraction" and cons.frac_den_max > 1 and ctx.rng.random() < 0.35:
        den = int(ctx.rng.randint(2, cons.frac_den_max))
        num = _sample_int_biased(
            ctx,
            cons.const_min,
            cons.const_max,
            abs_bias=cons.coef_abs_bias,
            exclude_zero=not cons.allow_zero_const,
        )
        return Fraction(num, den)
    v = _sample_int_biased(
        ctx,
        cons.const_min,
        cons.const_max,
        abs_bias=cons.coef_abs_bias,
        exclude_zero=not cons.allow_zero_const,
    )
    return Fraction(v)


def _sample_leading(ctx: PrimitiveContext, cons: FactorConstraints) -> int:
    if not cons.allow_nonmonic or cons.leading_max <= 1:
        return 1
    if ctx.rng.random() >= cons.nonmonic_weight:
        return 1
    pool = list(range(max(2, cons.leading_min), cons.leading_max + 1))
    if not pool:
        pool = [2]
    return int(ctx.rng.choice(pool))


def sample_linear_factor(
    ctx: PrimitiveContext,
    *,
    constraints: FactorConstraints | None = None,
    d: float | None = None,
    used_roots: set[Fraction] | None = None,
    force_nonmonic: bool = False,
) -> LinearFactor:
    """Draw one linear ``ax+b`` inside ``constraints``."""
    settings = getattr(ctx, "settings", None) or {}
    eff = float(d if d is not None else getattr(ctx, "topic_d", 0.0) or 0.0)
    cons = (constraints or constraints_from_settings(settings, d=eff)).clamped()
    seen = set(used_roots or ())

    for _ in range(64):
        a_int = _sample_leading(ctx, cons)
        if force_nonmonic and a_int == 1 and cons.allow_nonmonic:
            a_int = max(2, cons.leading_min if cons.leading_min > 1 else 2)
            a_int = min(a_int, cons.leading_max)
        b = _sample_const(ctx, cons)
        a = Fraction(a_int)
        if cons.require_content_primitive and b.denominator == 1 and a.denominator == 1:
            g = gcd(abs(int(a)), abs(int(b))) if b != 0 else abs(int(a))
            if g > 1:
                a = Fraction(int(a) // g)
                b = Fraction(int(b) // g)
        if a == 0:
            continue
        if cons.positive_leading and a < 0:
            a, b = -a, -b
        fac = LinearFactor(a=a, b=b)
        if fac.root() in seen:
            continue
        return fac

    # Deterministic fallback monic distinct root
    fb = 1
    while Fraction(-fb) in seen:
        fb += 1
    return LinearFactor(a=Fraction(1), b=Fraction(fb))


def _resolve_style(
    ctx: PrimitiveContext,
    cons: FactorConstraints,
    dens_style: DensStyle | str | None,
) -> DensStyle:
    style: DensStyle = cons.dens_style
    if dens_style in {"factored", "expanded", "auto"}:
        style = dens_style  # type: ignore[assignment]
    if style == "auto":
        style = "expanded" if ctx.rng.random() < cons.expand_weight else "factored"
    return style


def _maybe_gcf(
    ctx: PrimitiveContext,
    product: dict[int, Fraction],
    cons: FactorConstraints,
) -> tuple[dict[int, Fraction], Fraction]:
    if not cons.require_gcf:
        return product, Fraction(1)
    g = Fraction(int(ctx.rng.choice([2, 3, 4, 5])))
    return scale_coeffs(product, g), g


def _finish_draw(
    *,
    poly_facs: list[PolyFactor],
    product: dict[int, Fraction],
    cons: FactorConstraints,
    style: DensStyle,
    eff: float,
    kind: str,
    outer_gcf: Fraction,
) -> FactorDraw:
    linears: list[LinearFactor] = []
    for pf in poly_facs:
        lin = pf.as_linear()
        if lin is not None:
            linears.append(lin)
    if len(linears) != len(poly_facs):
        linears = []
    return FactorDraw(
        factors=tuple(linears),
        constraints=cons,
        dens_style=style,
        product=product,
        effective_d=eff,
        poly_factors=tuple(poly_facs),
        outer_gcf=outer_gcf,
        factor_kind=kind,
    )


def _sample_linear_product(
    ctx: PrimitiveContext,
    cons: FactorConstraints,
    *,
    n: int,
    d: float,
) -> list[PolyFactor]:
    factors: list[LinearFactor] = []
    roots: set[Fraction] = set()
    force_one_nonmonic = (
        cons.allow_nonmonic
        and cons.nonmonic_weight >= 0.5
        and ctx.rng.random() < cons.nonmonic_weight
    )
    for i in range(n):
        fac = sample_linear_factor(
            ctx,
            constraints=cons,
            d=d,
            used_roots=roots,
            force_nonmonic=force_one_nonmonic and i == 0,
        )
        factors.append(fac)
        roots.add(fac.root())
    return [PolyFactor.from_coeffs(f.coeffs()) for f in factors]


def _sample_kind_factors(
    ctx: PrimitiveContext,
    cons: FactorConstraints,
    *,
    kind: str,
    n: int,
    d: float,
) -> list[PolyFactor]:
    """Sample factor pieces for a named kind (still one inventory, not a fork pack)."""
    lead = _sample_leading(ctx, cons)
    b = _sample_const(ctx, cons)
    if b == 0:
        b = Fraction(1)

    if kind == "diff_squares":
        left = {1: Fraction(lead), 0: b}
        right = {1: Fraction(lead), 0: -b}
        return [PolyFactor.from_coeffs(left), PolyFactor.from_coeffs(right)]

    if kind == "perfect_square":
        inner = {1: Fraction(lead), 0: b}
        pf = PolyFactor.from_coeffs(inner)
        return [pf, pf]

    if kind == "grouping":
        # OpenStax §7.1 grouping is four terms: (px+q)(r x^2 + s), never a
        # quadratic trinomial of two linear factors (old D=0 dump).
        p = Fraction(1 if not cons.allow_nonmonic else lead)
        q = _sample_const(ctx, cons)
        r = Fraction(_sample_leading(ctx, cons) if cons.allow_nonmonic else 1)
        s = _sample_const(ctx, cons)
        if q == 0:
            q = Fraction(2)
        if s == 0:
            s = Fraction(-1)
        if r == 0:
            r = Fraction(1)
        if p == 0:
            p = Fraction(1)
        left = {1: p, 0: q}
        right = {2: r, 0: s}
        return [PolyFactor.from_coeffs(left), PolyFactor.from_coeffs(right)]

    if kind == "cubes":
        a = 1 if not cons.allow_nonmonic else max(1, lead)
        bb = abs(int(b)) or 1
        use_sum = d >= 3.0 and ctx.rng.random() < 0.5
        if use_sum:
            linear = {1: Fraction(a), 0: Fraction(bb)}
            quadratic = {
                2: Fraction(a * a),
                1: Fraction(-a * bb),
                0: Fraction(bb * bb),
            }
        else:
            linear = {1: Fraction(a), 0: Fraction(-bb)}
            quadratic = {
                2: Fraction(a * a),
                1: Fraction(a * bb),
                0: Fraction(bb * bb),
            }
        return [PolyFactor.from_coeffs(linear), PolyFactor.from_coeffs(quadratic)]

    if kind == "quadratic_form":
        power = 2
        p = 1 if not cons.allow_nonmonic else max(1, lead)
        r = 1 if not cons.allow_nonmonic else max(1, _sample_leading(ctx, cons))
        q = _sample_const(ctx, cons)
        s = _sample_const(ctx, cons)
        if q == 0:
            q = Fraction(2)
        if s == 0 or s == q:
            s = Fraction(-1 if q > 0 else 2)
        left = {power: Fraction(p), 0: q}
        right = {power: Fraction(r), 0: s}
        return [PolyFactor.from_coeffs(left), PolyFactor.from_coeffs(right)]

    if kind == "mono_poly":
        k = 1 if cons.max_product_degree <= 2 else min(2, cons.max_product_degree - 1)
        k = max(1, k)
        mono_c = Fraction(_sample_leading(ctx, cons) if cons.allow_nonmonic else 1)
        if ctx.rng.random() < 0.35:
            mono_c = Fraction(ctx.rng.choice([2, 3, 4, 5]))
        mono = {k: mono_c}
        # Residual: binomial (or trinomial when room).
        if cons.max_product_degree - k >= 2 and ctx.rng.random() < 0.35:
            poly = {
                min(2, cons.max_product_degree - k): Fraction(1),
                1: _sample_const(ctx, cons),
                0: _sample_const(ctx, cons) or Fraction(1),
            }
        else:
            lin = sample_linear_factor(ctx, constraints=cons, d=d)
            poly = lin.coeffs()
        return [PolyFactor.from_coeffs(mono), PolyFactor.from_coeffs(poly)]

    return _sample_linear_product(ctx, cons, n=n, d=d)


def sample_factor_product(
    ctx: PrimitiveContext,
    *,
    n_factors: int | None = None,
    d: float | None = None,
    constraints: FactorConstraints | None = None,
    dens_style: DensStyle | str | None = None,
    factor_kind: FactorKind | str | None = None,
) -> FactorDraw:
    """Sample a factor inventory; product degree ≤ ``max_product_degree`` (default 2)."""
    settings = getattr(ctx, "settings", None) or {}
    eff = float(d if d is not None else getattr(ctx, "topic_d", 0.0) or 0.0)
    cons = (constraints or constraints_from_settings(settings, d=eff)).clamped()
    kind = str(factor_kind or cons.factor_kind or "linear")
    if kind not in _KIND_SET:
        kind = "linear"

    cap = max(1, int(cons.max_product_degree))
    if n_factors is None:
        n = int(ctx.rng.randint(cons.min_factors, cons.max_factors))
    else:
        n = max(cons.min_factors, min(int(n_factors), cons.max_factors))
    n = max(1, min(n, cap))

    poly_facs = _sample_kind_factors(ctx, cons, kind=kind, n=n, d=eff)
    product: dict[int, Fraction] = {0: Fraction(1)}
    for pf in poly_facs:
        product = multiply_coeffs(product, pf.coeffs())
    product, outer_gcf = _maybe_gcf(ctx, product, cons)
    style = _resolve_style(ctx, cons, dens_style)
    return _finish_draw(
        poly_facs=poly_facs,
        product=product,
        cons=cons,
        style=style,
        eff=eff,
        kind=kind,
        outer_gcf=outer_gcf,
    )


def render_factor(fac: LinearFactor, var_latex: str) -> tuple[str, str]:
    return render_poly(fac.coeffs(), _var_stub(var_latex))


def render_poly_factor(fac: PolyFactor, var_latex: str) -> tuple[str, str]:
    return render_poly(fac.coeffs(), _var_stub(var_latex))


def render_factor_product(
    draw: FactorDraw,
    var_latex: str,
    *,
    dens_style: DensStyle | None = None,
    as_square: bool = False,
) -> tuple[str, str]:
    var = _var_stub(var_latex)
    style = dens_style or draw.dens_style
    if style == "expanded":
        return render_poly(draw.product, var)
    pieces = list(draw.poly_factors) if draw.poly_factors else [
        PolyFactor.from_coeffs(f.coeffs()) for f in draw.factors
    ]
    if draw.outer_gcf != 1 and style == "factored":
        from question_engine.frameworks.primitives._algebra_render import num_latex

        g_l = num_latex(draw.outer_gcf)
        g_t = str(draw.outer_gcf)
    else:
        g_l = g_t = ""
    if as_square and len(pieces) == 2 and pieces[0] == pieces[1]:
        fl, ft = wrap_parens(*render_poly(pieces[0].coeffs(), var))
        return f"{g_l}{fl}^{{2}}", f"{g_t}{ft}^2"
    if len(pieces) == 1:
        body_l, body_t = render_poly(pieces[0].coeffs(), var)
        if g_l:
            wrapped_l, wrapped_t = wrap_parens(body_l, body_t)
            return f"{g_l}{wrapped_l}", f"{g_t}{wrapped_t}"
        return body_l, body_t
    parts_l: list[str] = []
    parts_t: list[str] = []
    if g_l:
        parts_l.append(g_l)
        parts_t.append(g_t)
    for f in pieces:
        coeffs = f.coeffs()
        # Monomials don't need parens.
        if len(coeffs) == 1:
            fl, ft = render_poly(coeffs, var)
        else:
            fl, ft = wrap_parens(*render_poly(coeffs, var))
        parts_l.append(fl)
        parts_t.append(ft)
    return "".join(parts_l), "".join(parts_t)


# Back-compat aliases for early callers / galleries
FactorHardness = str  # deprecated label; use constraints + bias_label


def resolve_factor_hardness(d: float, *, explicit: str | None = None) -> str:
    """Deprecated: returns a bias label string for docs/galleries only."""
    if explicit:
        return str(explicit)
    cons = constraints_from_settings({}, d=d)
    style: DensStyle = "expanded" if cons.expand_weight >= 0.5 else "factored"
    return _bias_label(cons, style)
