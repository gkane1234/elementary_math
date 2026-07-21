"""Polynomial factoring beyond GCF — factors-first, then expand (optional unsimplify).

Quadratic / special / grouping leaves **seed the factors**, multiply out to the
prompt polynomial, and (when topic D > unsimplify gate) disguise the expanded
form via ``construct_poly`` so students still factor to the same answer.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Literal

from question_engine.frameworks.niceness import NicenessError
from question_engine.frameworks.primitives._algebra_render import num_latex
from question_engine.frameworks.primitives.poly_helpers import (
    multiply_coeffs,
    poly_degree,
    render_poly,
    sample_coeff,
    scale_coeffs,
    target_poly_degree,
    wrap_parens,
)
from question_engine.frameworks.primitives.registry import PrimitiveContext

FACTOR_POLY_SETTINGS_SCHEMA: dict[str, Any] = {}
PRIM_FACTOR_POLY = "factor_poly"


@dataclass(frozen=True)
class FactorPolyItem:
    latex: str
    text: str
    factored_latex: str
    factored_text: str
    method: str
    degree: int
    upgrades: tuple[str, ...]
    effective_d: float
    poly_coeffs: dict[int, Fraction] | None = None
    factor_coeffs: tuple[dict[int, Fraction], ...] = ()


def _topic_d(ctx: PrimitiveContext, eff: float) -> float:
    """Prefer worksheet topic D so unlocks track the difficulty slider."""
    return max(float(eff), float(getattr(ctx, "topic_d", 0.0) or 0.0))


def _knobs() -> dict[str, Any]:
    from question_engine.frameworks.primitives.difficulty_knobs import section

    return section("quadratic_factoring") or {}


def sample_quadratic_factoring(ctx: PrimitiveContext) -> FactorPolyItem:
    eff = ctx.effective_d(PRIM_FACTOR_POLY)
    for _ in range(20):
        try:
            return _quadratic(ctx, eff)
        except (NicenessError, ValueError):
            continue
    return _quadratic(ctx, eff)


def sample_special_factoring(ctx: PrimitiveContext) -> FactorPolyItem:
    eff = ctx.effective_d(PRIM_FACTOR_POLY)
    for _ in range(16):
        try:
            return _special(ctx, eff)
        except (NicenessError, ValueError):
            continue
    return _special(ctx, eff)


def sample_factoring_grouping(ctx: PrimitiveContext) -> FactorPolyItem:
    eff = ctx.effective_d(PRIM_FACTOR_POLY)
    for _ in range(16):
        try:
            return _grouping(ctx, eff)
        except (NicenessError, ValueError):
            continue
    return _grouping(ctx, eff)


def sample_sum_diff_cubes(ctx: PrimitiveContext) -> FactorPolyItem:
    """Factors-first sum/difference of cubes ``a³x³ ± b³``."""
    eff = ctx.effective_d(PRIM_FACTOR_POLY)
    for _ in range(16):
        try:
            return _sum_diff_cubes(ctx, eff)
        except (NicenessError, ValueError):
            continue
    return _sum_diff_cubes(ctx, eff)


def sample_quadratic_form(ctx: PrimitiveContext) -> FactorPolyItem:
    """Factors-first quadratic-in-u (typically ``(ax²+b)(cx²+d)`` → degree 4)."""
    eff = ctx.effective_d(PRIM_FACTOR_POLY)
    for _ in range(16):
        try:
            return _quadratic_form(ctx, eff)
        except (NicenessError, ValueError):
            continue
    return _quadratic_form(ctx, eff)


def sample_factoring_all_techniques(ctx: PrimitiveContext) -> FactorPolyItem:
    """Thin mixer: GCF / quadratic / special / grouping / cubes (when unlocked)."""
    eff = ctx.effective_d(PRIM_FACTOR_POLY)
    for _ in range(20):
        try:
            return _all_techniques(ctx, eff)
        except (NicenessError, ValueError):
            continue
    return _all_techniques(ctx, eff)


def _small_pos(ctx: PrimitiveContext, *, hi: int) -> int:
    return ctx.rng.randint(1, max(1, hi))


def _signed_small(ctx: PrimitiveContext, *, hi: int, allow_neg: bool) -> int:
    v = _small_pos(ctx, hi=hi)
    if allow_neg and ctx.rng.random() < 0.5:
        return -v
    return v


def _factor_content(fac: dict[int, Fraction]) -> int:
    """Largest positive integer dividing all integer coefficients."""
    from math import gcd

    vals: list[int] = []
    for c in fac.values():
        if c == 0:
            continue
        if c.denominator != 1:
            return 1
        vals.append(abs(int(c.numerator)))
    if not vals:
        return 1
    g = vals[0]
    for v in vals[1:]:
        g = gcd(g, v)
    return g or 1


def _complete_factors(
    factors: list[dict[int, Fraction]],
    gcf: Fraction | None = None,
) -> tuple[list[dict[int, Fraction]], Fraction | None]:
    """Pull integer contents from factors into an outer GCF (factor completely)."""
    outer = Fraction(gcf or 1)
    out: list[dict[int, Fraction]] = []
    for f in factors:
        c = _factor_content(f)
        if c > 1:
            outer *= c
            f = scale_coeffs(f, Fraction(1, c))
        out.append(f)
    if outer == 1:
        return out, None
    return out, outer


def _format_factors(
    factors: list[dict[int, Fraction]],
    var,
    *,
    gcf: Fraction | None = None,
) -> tuple[str, str]:
    parts_l: list[str] = []
    parts_t: list[str] = []
    if gcf is not None and gcf != 1:
        parts_l.append(num_latex(gcf))
        parts_t.append(num_latex(gcf))
    for f in factors:
        fl, ft = wrap_parens(*render_poly(f, var))
        parts_l.append(fl)
        parts_t.append(ft)
    return "".join(parts_l), "".join(parts_t)


def _present_expanded(
    ctx: PrimitiveContext,
    product: dict[int, Fraction],
    var,
    *,
    d: float,
) -> tuple[str, str, tuple[str, ...]]:
    """Render expanded poly; optionally unsimplify when D > gate."""
    kn = _knobs()
    gate = float(kn.get("unsimplify_from_d", 10.0))
    plain_l, plain_t = render_poly(product, var, descending=True)
    if d <= gate:
        return plain_l, plain_t, ()

    from question_engine.frameworks.primitives.constructive import (
        ExpressionScope,
        PolynomialTarget,
        construct_poly,
        verify_poly,
    )

    # Spend leftover difficulty on compositional disguise of the same target.
    inflate_d = max(1.0, d - gate)
    min_inflators = 1 + int(inflate_d // 8)
    for _ in range(8):
        surface = construct_poly(
            ctx,
            d=inflate_d,
            var=var,
            target=PolynomialTarget.from_dict(dict(product), single_hot=False),
            scope=ExpressionScope(max_degree=max(2, poly_degree(product))),
            prefer_distribute=True,
            min_inflators=min_inflators,
        )
        if verify_poly(surface, surface.target):
            tags = ("unsimplified", *tuple(
                t for t in surface.inflators_applied if str(t).startswith("compose:")
            )[:4])
            return surface.latex, surface.text, tags
    return plain_l, plain_t, ()


def _quadratic(ctx: PrimitiveContext, eff: float) -> FactorPolyItem:
    """Factors-first ``(px+q)(rx+s)`` → expand → optional unsimplify."""
    if ctx.policy.max_degree < 2:
        raise ValueError("quadratic factoring requires max_degree≥2")
    ctx.policy.assert_degree(2, where="quadratic_factoring")
    var = ctx.sample_variable()
    d = _topic_d(ctx, eff)
    kn = _knobs()

    # --- Difficulty ladder for factor shapes ---
    # D≈0–3: monic, small positive constants (x+1)(x+2)
    # D≈3–6: monic, allow one negative
    # D≈6–10: monic, both signs free, slightly larger
    # D≥ nonmonic_from_d: leading coeffs > 1 (ac method)
    # D> unsimplify_from_d: disguise expanded form
    nonmonic_from = float(kn.get("nonmonic_from_d", 8.0))
    gcf_from = float(kn.get("gcf_from_d", 12.0))
    const_hi_easy = int(kn.get("const_hi_easy", 4))
    const_hi_mid = int(kn.get("const_hi_mid", 6))
    const_hi_hard = int(kn.get("const_hi_hard", 9))

    if d < 3.0:
        p = r = 1
        q = _small_pos(ctx, hi=const_hi_easy)
        s = _small_pos(ctx, hi=const_hi_easy)
        if q == s and ctx.rng.random() < 0.5:
            s = q + 1 if q < const_hi_easy else max(1, q - 1)
        method = "monic_simple"
    elif d < 6.0:
        p = r = 1
        q = _small_pos(ctx, hi=const_hi_easy)
        s = _small_pos(ctx, hi=const_hi_easy)
        # Exactly one negative constant.
        if ctx.rng.random() < 0.5:
            q = -q
        else:
            s = -s
        method = "monic_one_negative"
    elif d < nonmonic_from:
        p = r = 1
        q = _signed_small(ctx, hi=const_hi_mid, allow_neg=True)
        s = _signed_small(ctx, hi=const_hi_mid, allow_neg=True)
        method = "monic_signed"
    else:
        # Non-monic: small positive leading coeffs
        p = _small_pos(ctx, hi=3)
        r = _small_pos(ctx, hi=3)
        if d < nonmonic_from + 4 and ctx.rng.random() < 0.45:
            # Often keep one factor monic for gentler ac-method
            if ctx.rng.random() < 0.5:
                p = 1
            else:
                r = 1
        q = _signed_small(ctx, hi=const_hi_hard, allow_neg=True)
        s = _signed_small(ctx, hi=const_hi_hard, allow_neg=True)
        method = "ac_method"

    # Avoid zero constants → bare px factors (unless intentional later).
    if q == 0:
        q = 1
    if s == 0:
        s = -1 if d >= 3 else 2

    left = {1: Fraction(p), 0: Fraction(q)}
    right = {1: Fraction(r), 0: Fraction(s)}
    product = multiply_coeffs(left, right)

    gcf: Fraction | None = None
    if d >= gcf_from and ctx.rng.random() < float(kn.get("gcf_chance", 0.3)):
        g = Fraction(ctx.rng.choice([2, 3, 4, 5]))
        product = scale_coeffs(product, g)
        gcf = g

    factors, gcf = _complete_factors([left, right], gcf)
    used = poly_degree(product)
    latex, text, u_tags = _present_expanded(ctx, product, var, d=d)
    fact_l, fact_t = _format_factors(factors, var, gcf=gcf)
    tags = [method, f"degree:{used}", f"d:{d:.1f}"]
    if gcf is not None:
        tags.append("with_gcf")
    tags.extend(u_tags)
    return FactorPolyItem(
        latex=latex,
        text=text,
        factored_latex=fact_l,
        factored_text=fact_t,
        method=method,
        degree=used,
        upgrades=tuple(tags),
        effective_d=d,
        poly_coeffs=dict(product),
        factor_coeffs=tuple(dict(f) for f in factors),
    )


def _special(ctx: PrimitiveContext, eff: float) -> FactorPolyItem:
    if ctx.policy.max_degree < 2:
        raise ValueError("special factoring requires max_degree≥2")
    ctx.policy.assert_degree(2, where="polynomial_factoring_special_cases")
    var = ctx.sample_variable()
    d = _topic_d(ctx, eff)
    kn = _knobs()
    nonmonic_from = float(kn.get("special_nonmonic_from_d", 6.0))

    monic = d < nonmonic_from or ctx.rng.random() < 0.55
    lead = 1 if monic else _small_pos(ctx, hi=3)
    a = _small_pos(ctx, hi=4 if d < 5 else 7)

    patterns: list[Literal["diff_squares", "perfect_square"]] = [
        "diff_squares",
        "perfect_square",
    ]
    # Very low D: prefer difference of squares (often introduced first)
    if d < 3.0:
        pattern: Literal["diff_squares", "perfect_square"] = "diff_squares"
    else:
        pattern = ctx.rng.choice(patterns)

    if pattern == "diff_squares":
        left = {1: Fraction(lead), 0: Fraction(a)}
        right = {1: Fraction(lead), 0: Fraction(-a)}
        product = multiply_coeffs(left, right)
        factors, gcf = _complete_factors([left, right])
        fact_l, fact_t = _format_factors(factors, var, gcf=gcf)
        method = "difference_of_squares"
        facs = tuple(dict(f) for f in factors)
    else:
        sign = 1 if d < 4.0 or ctx.rng.random() < 0.5 else -1
        inner = {1: Fraction(lead), 0: Fraction(sign * a)}
        product = multiply_coeffs(inner, inner)
        factors, gcf = _complete_factors([dict(inner), dict(inner)])
        # Prefer squared form when both factors match after content pull.
        if gcf is None and len(factors) == 2 and factors[0] == factors[1]:
            fl, ft = wrap_parens(*render_poly(factors[0], var))
            fact_l = f"{fl}^{{2}}"
            fact_t = f"{ft}^2"
        else:
            fact_l, fact_t = _format_factors(factors, var, gcf=gcf)
        method = "perfect_square"
        facs = tuple(dict(f) for f in factors)

    used = poly_degree(product)
    latex, text, u_tags = _present_expanded(ctx, product, var, d=d)
    tags = [method, f"degree:{used}", "monic" if monic else "nonmonic", *u_tags]
    return FactorPolyItem(
        latex=latex,
        text=text,
        factored_latex=fact_l,
        factored_text=fact_t,
        method=method,
        degree=used,
        upgrades=tuple(tags),
        effective_d=d,
        poly_coeffs=dict(product),
        factor_coeffs=facs,
    )


def _grouping(ctx: PrimitiveContext, eff: float) -> FactorPolyItem:
    """Four-term grouping from factors-first ``(px+q)(r x^2 + s)`` when cubic."""
    deg_cap = target_poly_degree(eff, ctx.policy)
    if deg_cap < 2:
        raise ValueError("grouping requires poly policy")
    d = _topic_d(ctx, eff)
    want_cubic = deg_cap >= 3 and d >= 4.0
    ctx.policy.assert_degree(3 if want_cubic else 2, where="factoring_grouping")
    var = ctx.sample_variable()

    a = _small_pos(ctx, hi=4)
    b = _signed_small(ctx, hi=5, allow_neg=d >= 3)
    c = _signed_small(ctx, hi=5, allow_neg=d >= 3)
    if b == 0:
        b = 2
    if c == 0:
        c = 1

    if want_cubic:
        p = Fraction(1)
        q = Fraction(c)
        r = Fraction(a)
        s = Fraction(b)
        left = {1: p, 0: q}
        right = {2: r, 0: s}
        product = multiply_coeffs(left, right)
        factors = [left, right]
        method = "grouping_cubic"
    else:
        # Quadratic fallback still factors-first.
        left = {1: Fraction(1), 0: Fraction(c)}
        right = {1: Fraction(a), 0: Fraction(b)}
        product = multiply_coeffs(left, right)
        factors = [left, right]
        method = "grouping_quadratic"

    factors, gcf = _complete_factors(factors)
    used = poly_degree(product)
    latex, text, u_tags = _present_expanded(ctx, product, var, d=d)
    fact_l, fact_t = _format_factors(factors, var, gcf=gcf)
    tags = [method, f"degree:{used}", *u_tags]
    if gcf is not None:
        tags.append("with_gcf")
    return FactorPolyItem(
        latex=latex,
        text=text,
        factored_latex=fact_l,
        factored_text=fact_t,
        method=method,
        degree=used,
        upgrades=tuple(tags),
        effective_d=d,
        poly_coeffs=dict(product),
        factor_coeffs=tuple(dict(f) for f in factors),
    )


def _sum_diff_cubes(ctx: PrimitiveContext, eff: float) -> FactorPolyItem:
    """Seed ``(ax±b)(a²x²∓abx+b²)`` → expand to ``a³x³±b³``; optional unsimplify."""
    if ctx.policy.max_degree < 3:
        raise ValueError("sum/difference of cubes requires max_degree≥3")
    ctx.policy.assert_degree(3, where="sum_diff_cubes")
    var = ctx.sample_variable()
    d = _topic_d(ctx, eff)
    kn = _knobs()
    nonmonic_from = float(kn.get("cubes_nonmonic_from_d", 8.0))
    const_hi = int(kn.get("cubes_const_hi_easy", 3) if d < 5 else kn.get("cubes_const_hi_hard", 5))

    monic = d < nonmonic_from or ctx.rng.random() < 0.5
    a = 1 if monic else _small_pos(ctx, hi=3)
    b = _small_pos(ctx, hi=const_hi)

    # Low D: prefer difference of cubes (often taught first).
    if d < 3.0:
        use_sum = False
    elif d < 6.0:
        use_sum = ctx.rng.random() < 0.45
    else:
        use_sum = ctx.rng.random() < 0.5

    if use_sum:
        # (ax + b)(a²x² − abx + b²) = a³x³ + b³
        linear = {1: Fraction(a), 0: Fraction(b)}
        quadratic = {2: Fraction(a * a), 1: Fraction(-a * b), 0: Fraction(b * b)}
        method = "sum_of_cubes"
    else:
        # (ax − b)(a²x² + abx + b²) = a³x³ − b³
        linear = {1: Fraction(a), 0: Fraction(-b)}
        quadratic = {2: Fraction(a * a), 1: Fraction(a * b), 0: Fraction(b * b)}
        method = "difference_of_cubes"

    product = multiply_coeffs(linear, quadratic)
    factors, gcf = _complete_factors([linear, quadratic])
    used = poly_degree(product)
    latex, text, u_tags = _present_expanded(ctx, product, var, d=d)
    fact_l, fact_t = _format_factors(factors, var, gcf=gcf)
    tags = [
        method,
        f"degree:{used}",
        "monic" if monic else "nonmonic",
        f"d:{d:.1f}",
        *u_tags,
    ]
    return FactorPolyItem(
        latex=latex,
        text=text,
        factored_latex=fact_l,
        factored_text=fact_t,
        method=method,
        degree=used,
        upgrades=tuple(tags),
        effective_d=d,
        poly_coeffs=dict(product),
        factor_coeffs=tuple(dict(f) for f in factors),
    )


def _quadratic_form(ctx: PrimitiveContext, eff: float) -> FactorPolyItem:
    """Seed ``(ax²+b)(cx²+d)`` (or cubic-in-u at high D) → expand; optional unsimplify."""
    if ctx.policy.max_degree < 4:
        raise ValueError("quadratic form requires max_degree≥4")
    d = _topic_d(ctx, eff)
    kn = _knobs()
    nonmonic_from = float(kn.get("quadratic_form_nonmonic_from_d", 8.0))
    const_hi_easy = int(kn.get("const_hi_easy", 4))
    const_hi_mid = int(kn.get("const_hi_mid", 6))
    const_hi_hard = int(kn.get("const_hi_hard", 9))

    # High D + room: quadratic in x³ → degree 6.
    use_cubic_u = (
        ctx.policy.max_degree >= 6
        and d >= float(kn.get("quadratic_form_cubic_u_from_d", 16.0))
        and ctx.rng.random() < 0.35
    )
    power = 3 if use_cubic_u else 2
    ctx.policy.assert_degree(2 * power, where="quadratic_form")
    var = ctx.sample_variable()

    if d < 3.0:
        p = r = 1
        q = _small_pos(ctx, hi=const_hi_easy)
        s = _small_pos(ctx, hi=const_hi_easy)
        if q == s:
            s = q + 1 if q < const_hi_easy else max(1, q - 1)
        method = "quadratic_form_simple"
    elif d < nonmonic_from:
        p = r = 1
        q = _signed_small(ctx, hi=const_hi_mid, allow_neg=True)
        s = _signed_small(ctx, hi=const_hi_mid, allow_neg=True)
        if q == 0:
            q = 2
        if s == 0:
            s = -1
        method = "quadratic_form_signed"
    else:
        p = _small_pos(ctx, hi=3)
        r = _small_pos(ctx, hi=3)
        if d < nonmonic_from + 4 and ctx.rng.random() < 0.45:
            if ctx.rng.random() < 0.5:
                p = 1
            else:
                r = 1
        q = _signed_small(ctx, hi=const_hi_hard, allow_neg=True)
        s = _signed_small(ctx, hi=const_hi_hard, allow_neg=True)
        if q == 0:
            q = 1
        if s == 0:
            s = -2
        method = "quadratic_form_ac"

    left = {power: Fraction(p), 0: Fraction(q)}
    right = {power: Fraction(r), 0: Fraction(s)}
    product = multiply_coeffs(left, right)
    factors, gcf = _complete_factors([left, right])
    used = poly_degree(product)
    latex, text, u_tags = _present_expanded(ctx, product, var, d=d)
    fact_l, fact_t = _format_factors(factors, var, gcf=gcf)
    tags = [method, f"degree:{used}", f"u_power:{power}", f"d:{d:.1f}", *u_tags]
    if gcf is not None:
        tags.append("with_gcf")
    return FactorPolyItem(
        latex=latex,
        text=text,
        factored_latex=fact_l,
        factored_text=fact_t,
        method=method,
        degree=used,
        upgrades=tuple(tags),
        effective_d=d,
        poly_coeffs=dict(product),
        factor_coeffs=tuple(dict(f) for f in factors),
    )


def _gcf_as_factor_poly(ctx: PrimitiveContext) -> FactorPolyItem:
    """Adapt factor_gcf leaf into FactorPolyItem for the all-techniques mixer."""
    from question_engine.frameworks.primitives.factor_gcf import sample_factor_gcf

    g = sample_factor_gcf(ctx)
    return FactorPolyItem(
        latex=g.latex,
        text=g.text,
        factored_latex=g.factored_latex,
        factored_text=g.factored_text,
        method="gcf",
        degree=int(g.max_degree),
        upgrades=tuple(["gcf", *g.upgrades]),
        effective_d=g.effective_d,
        poly_coeffs=None,
        factor_coeffs=(),
    )


def _all_techniques(ctx: PrimitiveContext, eff: float) -> FactorPolyItem:
    """Sample one existing factor leaf; cubes only when leaf/policy unlocks them."""
    leaf = str(getattr(ctx, "leaf_id", "") or "")
    # A2 "all techniques" includes cubes; A1 general strategy does not.
    include_cubes = "all_techniques" in leaf and ctx.policy.max_degree >= 3

    choices: list[str] = ["gcf", "quadratic", "special", "grouping"]
    if include_cubes:
        choices.append("cubes")

    # Weight slightly toward quadratic/special at mid D (common decision-tree middle).
    d = _topic_d(ctx, eff)
    weights = {
        "gcf": 1.2 if d < 4 else 1.0,
        "quadratic": 1.4,
        "special": 1.2,
        "grouping": 1.0 if d >= 3 else 0.6,
        "cubes": 1.0,
    }
    pool = choices[:]
    w = [weights.get(c, 1.0) for c in pool]
    total = sum(w)
    r = ctx.rng.random() * total
    pick = pool[-1]
    acc = 0.0
    for c, wi in zip(pool, w):
        acc += wi
        if r <= acc:
            pick = c
            break

    if pick == "gcf":
        item = _gcf_as_factor_poly(ctx)
    elif pick == "quadratic":
        item = sample_quadratic_factoring(ctx)
    elif pick == "special":
        item = sample_special_factoring(ctx)
    elif pick == "cubes":
        item = sample_sum_diff_cubes(ctx)
    else:
        item = sample_factoring_grouping(ctx)

    tags = ("all_techniques", pick, *item.upgrades)
    return FactorPolyItem(
        latex=item.latex,
        text=item.text,
        factored_latex=item.factored_latex,
        factored_text=item.factored_text,
        method=f"all:{item.method}",
        degree=item.degree,
        upgrades=tags,
        effective_d=item.effective_d,
        poly_coeffs=item.poly_coeffs,
        factor_coeffs=item.factor_coeffs,
    )


def sample_quadratic_equation_by_factoring(ctx: PrimitiveContext) -> FactorPolyItem:
    """Factors-first quadratic set to zero."""
    item = sample_quadratic_factoring(ctx)
    return FactorPolyItem(
        latex=f"{item.latex} = 0",
        text=f"{item.text} = 0",
        factored_latex=item.factored_latex,
        factored_text=item.factored_text,
        method=item.method + "_equation",
        degree=item.degree,
        upgrades=tuple(list(item.upgrades) + ["equation"]),
        effective_d=item.effective_d,
        poly_coeffs=item.poly_coeffs,
        factor_coeffs=item.factor_coeffs,
    )
