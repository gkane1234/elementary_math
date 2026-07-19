"""Polynomial expression ops — naming, add/subtract, multiply, special products.

Uses ``ExpressionPolicy`` for degree caps and Layer 0 number/variable lanes.
Degree vs D: ``target_poly_degree`` (log growth, hard-capped by policy).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Literal

from question_engine.frameworks.niceness import NicenessError
from question_engine.frameworks.primitives._algebra_render import num_latex
from question_engine.frameworks.primitives.poly_helpers import (
    combine_coeff_maps,
    degree_name,
    multiply_coeffs,
    poly_degree,
    render_poly,
    sample_coeff,
    sample_poly_coeffs,
    scale_coeffs,
    target_n_terms,
    target_poly_degree,
    wrap_parens,
)
from question_engine.frameworks.primitives.registry import (
    PrimitiveContext,
)

POLYNOMIALS_SETTINGS_SCHEMA: dict[str, Any] = {}

# Local primitive id for budget (maps via LEAF_TO_PRIMITIVE).
PRIM_POLYNOMIALS = "polynomials"


@dataclass(frozen=True)
class PolyNamingItem:
    latex: str
    text: str
    answer_latex: str
    answer_text: str
    degree: int
    leading_coeff: Fraction
    n_terms: int
    upgrades: tuple[str, ...]
    effective_d: float


@dataclass(frozen=True)
class PolyAddSubItem:
    latex: str
    text: str
    simplified_latex: str
    simplified_text: str
    op: Literal["+", "-"]
    degree: int
    upgrades: tuple[str, ...]
    effective_d: float


@dataclass(frozen=True)
class PolyMultiplyItem:
    latex: str
    text: str
    product_latex: str
    product_text: str
    left_terms: int
    right_terms: int
    degree: int
    pattern: str
    upgrades: tuple[str, ...]
    effective_d: float


def sample_polynomial_naming(ctx: PrimitiveContext) -> PolyNamingItem:
    eff = ctx.effective_d(PRIM_POLYNOMIALS)
    for _ in range(12):
        try:
            return _naming(ctx, eff)
        except (NicenessError, ValueError):
            continue
    return _naming(ctx, eff)


def _naming(ctx: PrimitiveContext, eff: float) -> PolyNamingItem:
    deg = target_poly_degree(eff, ctx.policy)
    ctx.policy.assert_degree(deg, where="polynomial_naming")
    var = ctx.sample_variable()
    n_terms = min(deg + 1, max(2, target_n_terms(eff)))
    coeffs = sample_poly_coeffs(ctx, degree=deg, n_terms=n_terms, require_leading=True)
    used = poly_degree(coeffs)
    latex, text = render_poly(coeffs, var, descending=True)
    ans_l, ans_t = degree_name(used)
    # Also ask leading coefficient when D is higher.
    lead = coeffs.get(used, Fraction(1))
    tags = [f"degree:{used}", f"terms:{n_terms}"]
    if eff >= 4.0 and ctx.rng.random() < 0.4:
        # Prompt stays "name"; answer includes degree class (standard leaf).
        tags.append("leading_meta")
    return PolyNamingItem(
        latex=latex,
        text=text,
        answer_latex=ans_l,
        answer_text=ans_t,
        degree=used,
        leading_coeff=lead,
        n_terms=n_terms,
        upgrades=tuple(tags),
        effective_d=eff,
    )


def sample_polynomial_add_subtract(ctx: PrimitiveContext) -> PolyAddSubItem:
    eff = ctx.effective_d(PRIM_POLYNOMIALS)
    for _ in range(12):
        try:
            return _add_sub(ctx, eff)
        except (NicenessError, ValueError):
            continue
    return _add_sub(ctx, eff)


def _add_sub(ctx: PrimitiveContext, eff: float) -> PolyAddSubItem:
    deg = target_poly_degree(eff, ctx.policy)
    ctx.policy.assert_degree(deg, where="polynomial_add_subtract")
    var = ctx.sample_variable()
    n_terms = min(deg + 1, max(2, target_n_terms(eff)))
    p = sample_poly_coeffs(ctx, degree=deg, n_terms=n_terms, require_leading=True)
    # Second poly: same max degree, maybe fewer terms.
    q_deg = deg if ctx.rng.random() < 0.7 else max(1, deg - 1)
    q = sample_poly_coeffs(
        ctx,
        degree=q_deg,
        n_terms=min(q_deg + 1, max(2, n_terms - 1)),
        require_leading=True,
    )
    op: Literal["+", "-"] = "+" if ctx.rng.random() < 0.55 else "-"
    if op == "+":
        result = combine_coeff_maps(p, q)
    else:
        result = combine_coeff_maps(p, scale_coeffs(q, Fraction(-1)))

    pl, pt = render_poly(p, var)
    ql, qt = render_poly(q, var)
    left_l, left_t = wrap_parens(pl, pt)
    right_l, right_t = wrap_parens(ql, qt)
    latex = f"{left_l} {op} {right_l}"
    text = f"{left_t} {op} {right_t}"
    simp_l, simp_t = render_poly(result, var, descending=True)
    used = poly_degree(result) if result else 0
    return PolyAddSubItem(
        latex=latex,
        text=text,
        simplified_latex=simp_l,
        simplified_text=simp_t,
        op=op,
        degree=max(used, deg),
        upgrades=(f"degree:{deg}", f"op:{op}", f"terms:{n_terms}"),
        effective_d=eff,
    )


def sample_polynomial_multiply(
    ctx: PrimitiveContext,
    *,
    special: bool = False,
) -> PolyMultiplyItem:
    eff = ctx.effective_d(PRIM_POLYNOMIALS)
    for _ in range(12):
        try:
            if special:
                return _multiply_special(ctx, eff)
            return _multiply(ctx, eff)
        except (NicenessError, ValueError):
            continue
    if special:
        return _multiply_special(ctx, eff)
    return _multiply(ctx, eff)


def _factor_shape(ctx: PrimitiveContext, eff: float, deg_cap: int) -> tuple[int, int]:
    """Return (left_terms, right_terms) growing gently with D."""
    # Unlock shapes: monomial×binomial → FOIL → longer.
    if eff < 2.0:
        return (1, 2) if ctx.rng.random() < 0.5 else (2, 1)
    if eff < 6.0 or deg_cap <= 2:
        return (2, 2)
    # Higher D: allow trinomial factor.
    options = [(2, 2), (1, 3), (3, 1), (2, 3)]
    if deg_cap >= 4 and eff >= 10:
        options.append((3, 2))
    return ctx.rng.choice(options)


def _sparse_factor(
    ctx: PrimitiveContext,
    *,
    n_terms: int,
    max_degree: int,
) -> dict[int, Fraction]:
    n_terms = max(1, min(n_terms, max_degree + 1))
    # Degree of factor: for monomial use max_degree or mid; for binomial use 1 typically.
    if n_terms == 1:
        deg = max(0, min(max_degree, 1 + int(math.floor(math.log2(1 + ctx.topic_d / 4)))))
        deg = max(1, min(deg, max_degree)) if max_degree >= 1 else 0
        return {deg: sample_coeff(ctx, exclude_zero=True)}
    if n_terms == 2:
        # Classic binomial: ax^k + b (prefer k=1 for FOIL).
        k = 1 if max_degree >= 1 else 0
        if max_degree >= 2 and ctx.rng.random() < 0.25:
            k = min(max_degree, 2)
        return {
            k: sample_coeff(ctx, exclude_zero=True),
            0: sample_coeff(ctx, exclude_zero=True),
        }
    # Trinomial: ax^2 + bx + c (or up to max_degree).
    deg = min(2, max_degree) if max_degree >= 2 else max_degree
    return sample_poly_coeffs(ctx, degree=deg, n_terms=3, require_leading=True)


def _multiply(ctx: PrimitiveContext, eff: float) -> PolyMultiplyItem:
    deg_cap = target_poly_degree(eff, ctx.policy)
    ctx.policy.assert_degree(deg_cap, where="polynomial_multiply")
    var = ctx.sample_variable()
    left_n, right_n = _factor_shape(ctx, eff, deg_cap)

    # Bound factor degrees so product ≤ deg_cap.
    # Prefer deg-1×deg-1 for FOIL when deg_cap≥2.
    left = _sparse_factor(ctx, n_terms=left_n, max_degree=max(1, deg_cap // 2 + 1))
    right = _sparse_factor(ctx, n_terms=right_n, max_degree=max(1, deg_cap - poly_degree(left)))
    product = multiply_coeffs(left, right)
    used = poly_degree(product)
    if used > ctx.policy.max_degree:
        # Degenerate fallback: (x+a)(x+b)
        a = sample_coeff(ctx)
        b = sample_coeff(ctx)
        left = {1: Fraction(1), 0: a}
        right = {1: Fraction(1), 0: b}
        product = multiply_coeffs(left, right)
        used = poly_degree(product)
    ctx.policy.assert_degree(used, where="polynomial_multiply.product")

    ll, lt = wrap_parens(*render_poly(left, var))
    rl, rt = wrap_parens(*render_poly(right, var))
    latex = f"{ll}{rl}"
    text = f"{lt}{rt}"
    pl, pt = render_poly(product, var, descending=True)
    pattern = "foil" if left_n == 2 and right_n == 2 else "distribute"
    return PolyMultiplyItem(
        latex=latex,
        text=text,
        product_latex=pl,
        product_text=pt,
        left_terms=left_n,
        right_terms=right_n,
        degree=used,
        pattern=pattern,
        upgrades=(f"degree:{used}", f"shape:{left_n}x{right_n}", pattern),
        effective_d=eff,
    )


def _multiply_special(ctx: PrimitiveContext, eff: float) -> PolyMultiplyItem:
    """(a±b)^2, (a+b)(a−b), optionally non-monic at higher D."""
    deg_cap = max(2, target_poly_degree(eff, ctx.policy))
    ctx.policy.assert_degree(min(2, deg_cap), where="polynomial_multiply_special")
    var = ctx.sample_variable()
    monic = eff < 6.0 or ctx.rng.random() < 0.55
    lead = Fraction(1) if monic else sample_coeff(ctx, exclude_zero=True)
    if abs(lead) == 1 and not monic:
        lead = Fraction(ctx.rng.choice([2, 3, 4]))
    a = abs(sample_coeff(ctx, exclude_zero=True))
    if a == 0:
        a = Fraction(2)

    patterns = ["square", "diff_squares"]
    if eff >= 3.0:
        patterns.append("sum_diff")
    pattern = ctx.rng.choice(patterns)

    if pattern == "square":
        sign = 1 if ctx.rng.random() < 0.5 else -1
        inner = {1: lead, 0: sign * a}
        left = right = inner
        product = multiply_coeffs(left, right)
        ll, lt = wrap_parens(*render_poly(inner, var))
        latex = f"{ll}^{{2}}"
        text = f"{lt}^2"
    elif pattern == "diff_squares":
        left = {1: lead, 0: a}
        right = {1: lead, 0: -a}
        product = multiply_coeffs(left, right)
        ll, lt = wrap_parens(*render_poly(left, var))
        rl, rt = wrap_parens(*render_poly(right, var))
        latex = f"{ll}{rl}"
        text = f"{lt}{rt}"
    else:
        b = abs(sample_coeff(ctx, exclude_zero=True))
        while b == a:
            b = Fraction(ctx.rng.randint(1, 6))
        sign = 1 if ctx.rng.random() < 0.5 else -1
        left = {1: lead, 0: a}
        right = {1: lead, 0: sign * b}
        product = multiply_coeffs(left, right)
        ll, lt = wrap_parens(*render_poly(left, var))
        rl, rt = wrap_parens(*render_poly(right, var))
        latex = f"{ll}{rl}"
        text = f"{lt}{rt}"

    used = poly_degree(product)
    ctx.policy.assert_degree(used, where="polynomial_multiply_special.product")
    pl, pt = render_poly(product, var, descending=True)
    return PolyMultiplyItem(
        latex=latex,
        text=text,
        product_latex=pl,
        product_text=pt,
        left_terms=2,
        right_terms=2,
        degree=used,
        pattern=pattern,
        upgrades=(f"degree:{used}", pattern, "monic" if monic else "nonmonic"),
        effective_d=eff,
    )
