"""Centralized LaTeX formatting for polynomials and rational expressions."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .polynomial import Polynomial


def fraction_latex(numerator: str, denominator: str) -> str:
    """Format a LaTeX fraction."""
    return f"\\frac{{{numerator}}}{{{denominator}}}"


def square_root_latex(coeff: int, radicand: int) -> str:
    """Format a coefficient times a square root in LaTeX."""
    if radicand <= 1:
        return str(coeff)
    if coeff == 1:
        return f"\\sqrt{{{radicand}}}"
    if coeff == -1:
        return f"-\\sqrt{{{radicand}}}"
    return f"{coeff}\\sqrt{{{radicand}}}"


def polynomial_to_latex(
    polynomial: Polynomial,
    rounding: int = 5,
    variable: str | None = None,
) -> str:
    """Render a polynomial as a LaTeX string."""
    if variable is not None:
        return round(polynomial, rounding).outputWithNewVariable(rounding=rounding, var=variable)
    return polynomial.to_latex(rounding=rounding)


def format_factor_product_latex(factors: tuple[Polynomial, ...] | list) -> str:
    """Render a product of polynomial factors in LaTeX."""
    if not factors:
        return "1"
    if len(factors) == 1:
        return factors[0].to_latex()
    return "".join(f"({factor.to_latex()})" for factor in factors)


def polynomial_fraction_latex(numerator: Polynomial, denominator: Polynomial) -> str:
    """Render a polynomial ratio as LaTeX."""
    return fraction_latex(numerator.to_latex(), denominator.to_latex())
