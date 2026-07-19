"""Polynomial factoring beyond GCF — trinomials, special products, grouping.

GCF itself lives in ``factor_gcf.py`` (policy-gated). This module covers:
- quadratic trinomials ``x^2+bx+c`` / ``ax^2+bx+c``
- difference of squares / perfect-square trinomials
- factoring by grouping (4-term)

Degree is policy-capped (typically 2 for quadratics); D controls monic vs
non-monic, sign messiness, and optional GCF prefix — not leftover-D degree drift.
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


def sample_quadratic_factoring(ctx: PrimitiveContext) -> FactorPolyItem:
    eff = ctx.effective_d(PRIM_FACTOR_POLY)
    for _ in range(16):
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


def _small_int(ctx: PrimitiveContext, *, lo: int = 1, hi: int = 6) -> int:
    for _ in range(12):
        n = sample_coeff(ctx, exclude_zero=True)
        if n.denominator == 1 and lo <= abs(int(n)) <= hi:
            return int(n)
    return ctx.rng.randint(lo, hi) * ctx.rng.choice([1, -1])


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


def _quadratic(ctx: PrimitiveContext, eff: float) -> FactorPolyItem:
    # Force degree 2 for this leaf (policy may allow higher but we stay quadratic).
    if ctx.policy.max_degree < 2:
        raise ValueError("quadratic factoring requires max_degree≥2")
    ctx.policy.assert_degree(2, where="quadratic_factoring")
    var = ctx.sample_variable()

    monic = eff < 5.0 or ctx.rng.random() < 0.55
    # Roots / factors: (px+q)(rx+s)
    if monic:
        p, r = 1, 1
    else:
        p = abs(_small_int(ctx, lo=1, hi=3))
        r = abs(_small_int(ctx, lo=1, hi=3))
    q = _small_int(ctx, lo=1, hi=6)
    s = _small_int(ctx, lo=1, hi=6)
    # Avoid (x+0) style.
    if q == 0:
        q = 1
    if s == 0:
        s = 2

    left = {1: Fraction(p), 0: Fraction(q)}
    right = {1: Fraction(r), 0: Fraction(s)}
    product = multiply_coeffs(left, right)

    gcf: Fraction | None = None
    if eff >= 8.0 and ctx.rng.random() < 0.35:
        g = Fraction(ctx.rng.choice([2, 3, 4, 5]))
        product = scale_coeffs(product, g)
        gcf = g

    used = poly_degree(product)
    latex, text = render_poly(product, var, descending=True)
    fact_l, fact_t = _format_factors([left, right], var, gcf=gcf)
    method = "monic_trinomial" if monic else "ac_method"
    tags = [method, f"degree:{used}"]
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
        effective_d=eff,
    )


def _special(ctx: PrimitiveContext, eff: float) -> FactorPolyItem:
    if ctx.policy.max_degree < 2:
        raise ValueError("special factoring requires max_degree≥2")
    ctx.policy.assert_degree(2, where="polynomial_factoring_special_cases")
    var = ctx.sample_variable()

    monic = eff < 6.0 or ctx.rng.random() < 0.6
    lead = 1 if monic else abs(_small_int(ctx, lo=2, hi=4))
    a = abs(_small_int(ctx, lo=1, hi=6))

    patterns: list[Literal["diff_squares", "perfect_square"]] = [
        "diff_squares",
        "perfect_square",
    ]
    pattern = ctx.rng.choice(patterns)

    if pattern == "diff_squares":
        # (lx)^2 - a^2
        left = {1: Fraction(lead), 0: Fraction(a)}
        right = {1: Fraction(lead), 0: Fraction(-a)}
        product = multiply_coeffs(left, right)
        fact_l, fact_t = _format_factors([left, right], var)
        method = "difference_of_squares"
    else:
        # (lx ± a)^2
        sign = 1 if ctx.rng.random() < 0.5 else -1
        inner = {1: Fraction(lead), 0: Fraction(sign * a)}
        product = multiply_coeffs(inner, inner)
        fl, ft = wrap_parens(*render_poly(inner, var))
        fact_l = f"{fl}^{{2}}"
        fact_t = f"{ft}^2"
        method = "perfect_square"

    used = poly_degree(product)
    latex, text = render_poly(product, var, descending=True)
    tags = [method, f"degree:{used}", "monic" if monic else "nonmonic"]
    return FactorPolyItem(
        latex=latex,
        text=text,
        factored_latex=fact_l,
        factored_text=fact_t,
        method=method,
        degree=used,
        upgrades=tuple(tags),
        effective_d=eff,
    )


def _grouping(ctx: PrimitiveContext, eff: float) -> FactorPolyItem:
    """Four-term: ax^3+bx^2+cx+d = (px+q)(rx^2+s) style grouping → (px+q)(rx+s) wait.

    Classic: ax^3 + bx^2 + cx + d factored as (ex + f)(gx^2 + h) when structured,
    or more commonly (ax+b)(cx+d) after expanding from two binomials — but that's
    quadratic. For grouping leaf we emit 4-term that groups as (ax+b)(cx+d) where
    we use x^3 form: x(ax+b)+c(ax+b) = (x+c)(ax+b).
    """
    deg_cap = target_poly_degree(eff, ctx.policy)
    if deg_cap < 2:
        raise ValueError("grouping requires poly policy")
    # Prefer cubic grouping when allowed.
    want_cubic = deg_cap >= 3 and eff >= 4.0
    ctx.policy.assert_degree(3 if want_cubic else 2, where="factoring_grouping")
    var = ctx.sample_variable()

    a = abs(_small_int(ctx, lo=1, hi=4))
    b = _small_int(ctx, lo=1, hi=5)
    c = _small_int(ctx, lo=1, hi=5)
    if b == 0:
        b = 2
    if c == 0:
        c = 1

    if want_cubic:
        # (x + c)(a x^2 + b) → a x^3 + b x + a c x^2 + b c
        # Better classic: (x+c)(ax+b) = a x^2 + ... that's 3-term.
        # True 4-term grouping: (px + q)(r x^2 + s) = p r x^3 + p s x + q r x^2 + q s
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
        # Fall back to quadratic FOIL presented as expandable — still factorable.
        # Use (ax+b)(cx+d) which is 3-term; to get 4-term need an extra zero mid?
        # Emit (ax+b)(x+c) and accept trinomial, OR force grouping form with y?
        # Standard Alg1 grouping: ax^3+bx^2+cx+d with shared binomial.
        p = Fraction(1)
        q = Fraction(c)
        r = Fraction(a)
        s = Fraction(b)
        left = {1: p, 0: q}
        right = {1: r, 0: s}
        product = multiply_coeffs(left, right)
        factors = [left, right]
        method = "grouping_quadratic"

    used = poly_degree(product)
    # For cubic, ensure 4 nonzero terms when possible.
    latex, text = render_poly(product, var, descending=True)
    fact_l, fact_t = _format_factors(factors, var)
    tags = [method, f"degree:{used}"]
    return FactorPolyItem(
        latex=latex,
        text=text,
        factored_latex=fact_l,
        factored_text=fact_t,
        method=method,
        degree=used,
        upgrades=tuple(tags),
        effective_d=eff,
    )
