"""Polynomial arithmetic helpers (GCD, LCM, etc.)."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .polynomial import Polynomial


def _normalize_leading(poly: Polynomial) -> Polynomial:
    """Scale so the leading coefficient is 1, or return zero polynomial."""
    if poly.is_zero():
        return poly
    lead = poly.leading_coefficient()
    if abs(lead) < 1e-10:
        return poly
    if abs(lead - 1.0) < 1e-10:
        return poly
    return poly * (1.0 / lead)


def polynomial_gcd(a: Polynomial, b: Polynomial, *, monic: bool = False) -> Polynomial:
    """Greatest common divisor of two polynomials via the Euclidean algorithm."""
    left, right = a, b
    while not right.is_zero():
        _, remainder = left.poly_div(right)
        left, right = right, remainder
    if monic:
        return _normalize_leading(left)
    return left


def polynomial_lcm(a: Polynomial, b: Polynomial) -> Polynomial:
    """Least common multiple: |a * b| / gcd(a, b)."""
    if a.is_zero() or b.is_zero():
        return a if a.is_zero() else b
    gcd = polynomial_gcd(a, b)
    return (a * b).poly_div(gcd)[0]


def content_gcd(poly: Polynomial) -> int:
    """Greatest common divisor of all integer coefficients (content)."""
    from math import gcd

    coeffs = [int(round(c)) for c in poly.coef_list(reverse=True) if abs(c) >= 1e-10]
    if not coeffs:
        return 0
    result = abs(coeffs[0])
    for coeff in coeffs[1:]:
        result = gcd(result, abs(int(round(coeff))))
    return result
