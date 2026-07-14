"""Centralized LaTeX formatting for polynomials and rational expressions."""

from __future__ import annotations

import re
from fractions import Fraction
from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    from .polynomial import Polynomial

Coef = int | float | Fraction

# Unsigned numeric token for slash/op second-operand cleanup.
_UNSIGNED_NUM = r"\d+(?:\.\d+)?(?:[eE][+-]?\d+)?"


def fraction_latex(numerator: str, denominator: str) -> str:
    """Format a LaTeX fraction."""
    return f"\\frac{{{numerator}}}{{{denominator}}}"


def unit_latex(unit: str, *, leading_space: bool = True) -> str:
    """Upright unit label for math mode (avoids italicized ``cm`` / ``in`` / …).

    Examples:
        ``unit_latex("cm")`` → ``\\text{ cm}``
        ``unit_latex("cm", leading_space=False)`` → ``\\text{cm}``
    """
    u = (unit or "").strip()
    if not u:
        return ""
    if leading_space:
        return f"\\text{{ {u}}}"
    return f"\\text{{{u}}}"


def format_with_unit(
    value: Coef | str,
    unit: str,
    *,
    power: int | None = None,
) -> str:
    """Numeric (or LaTeX) value with an upright unit suffix.

    Examples:
        ``format_with_unit(3, "cm")`` → ``3\\text{ cm}``
        ``format_with_unit(r"\\frac{3}{2}", "cm")`` → ``\\frac{3}{2}\\text{ cm}``
        ``format_with_unit(5, "cm", power=2)`` → ``5\\text{ cm}^{2}``
    """
    body = value if isinstance(value, str) else _coef_token(value)
    suffix = unit_latex(unit)
    if not suffix:
        if power is not None and power != 1:
            return f"{body}^{{{power}}}"
        return body
    if power is not None and power != 1:
        return f"{body}{suffix}^{{{power}}}"
    return f"{body}{suffix}"


def format_measurement_text(
    value: Coef | str,
    unit: str,
    *,
    power: int | None = None,
) -> str:
    """Plain-text measurement for SVG / TikZ labels / ``prompt_text``."""
    body = value if isinstance(value, str) else _coef_token(value)
    u = (unit or "").strip()
    if not u:
        if power is not None and power != 1:
            return f"{body}^{power}"
        return body
    if power is not None and power != 1:
        return f"{body} {u}^{power}"
    return f"{body} {u}"


def _coef_token(value: Coef) -> str:
    """Plain signed number string (no forced parentheses)."""
    value = _as_number(value)
    if isinstance(value, Fraction):
        if value.denominator == 1:
            return str(value.numerator)
        sign = "-" if value < 0 else ""
        return f"{sign}\\frac{{{abs(value.numerator)}}}{{{value.denominator}}}"
    if isinstance(value, float) and abs(value - round(value)) < 1e-10:
        return str(int(round(value)))
    if isinstance(value, float):
        return f"{value:g}"
    return str(value)


def paren_if_negative(value: Coef | str) -> str:
    """Parenthesize a negative numeric token (e.g. for slash denominators)."""
    if isinstance(value, str):
        text = value.strip()
        if text.startswith("-") and not text.startswith("("):
            return f"({text})"
        return text
    token = _coef_token(value)
    if token.startswith("-"):
        return f"({token})"
    return token


def format_slash_fraction(numerator: Coef | str, denominator: Coef | str) -> str:
    """Format ``a/b`` with parentheses around a negative denominator: ``2/(-1)``."""
    num = numerator if isinstance(numerator, str) else _coef_token(numerator)
    den = paren_if_negative(denominator)
    return f"{num}/{den}"


def format_binop_expression(
    left: Coef | str,
    op: str,
    right: Coef | str,
    *,
    spaced: bool = True,
) -> str:
    """Format a binary operation without awkward ``+-`` / bare ``/-``.

    - ``5 + (-2)`` / ``5+-2`` → ``5 - 2`` (or spaced ``5 - 2``)
    - ``2 / -1`` → ``2/(-1)``
    - ``2 \\div -1`` → ``2 \\div (-1)``
    """
    left_s = left if isinstance(left, str) else _coef_token(left)
    right_s = right if isinstance(right, str) else _coef_token(right)
    op_s = op.strip()
    sep = " " if spaced else ""

    right_negative = right_s.startswith("-") and not right_s.startswith("(")

    if op_s == "+":
        if right_negative:
            return f"{left_s}{sep}-{sep}{right_s[1:]}"
        return f"{left_s}{sep}+{sep}{right_s}"

    if op_s == "-":
        if right_negative:
            return f"{left_s}{sep}-{sep}({right_s})"
        return f"{left_s}{sep}-{sep}{right_s}"

    if op_s == "/":
        return format_slash_fraction(left_s, right_s)

    # *, \\cdot, \\div, ÷ — parenthesize negative right operands
    if right_negative:
        right_s = f"({right_s})"
    return f"{left_s}{sep}{op_s}{sep}{right_s}"


def normalize_expression_signs(expr: str | None) -> str:
    """Collapse awkward sign juxtaposition and parenthesize negative slash denoms.

    Examples:
        ``5+-2`` → ``5-2``
        ``5 + -2`` → ``5 - 2``
        ``5--2`` → ``5+2``
        ``2/-1`` → ``2/(-1)``
        ``2*x+-3`` → ``2*x-3``
    """
    if not expr:
        return "" if expr is None else expr

    s = expr
    for _ in range(8):
        prev = s
        # Unspaced sign runs first (keep compact forms like `2*x-3`).
        s = re.sub(r"\+-", "-", s)
        s = re.sub(r"-\+", "-", s)
        s = re.sub(r"--", "+", s)
        # Spaced juxtapositions: `5 + -2` → `5 - 2`.
        s = re.sub(r"\s+\+\s+-", " - ", s)
        s = re.sub(r"\s+-\s+\+", " - ", s)
        s = re.sub(r"\s+-\s+-", " + ", s)
        # Slash with bare negative number (not already parenthesized).
        s = re.sub(rf"/(\s*)-({_UNSIGNED_NUM})(?!\))", r"/(\1-\2)", s)
        # Tighten "/( -1)" → "/(-1)"
        s = re.sub(rf"/\(\s*-({_UNSIGNED_NUM})\s*\)", r"/(-\1)", s)
        # Div/mul ops with bare negative second operand.
        s = re.sub(
            rf"(\\div|÷|\\cdot|\*)(\s*)-({_UNSIGNED_NUM})(?!\))",
            r"\1\2(-\3)",
            s,
        )
        if s == prev:
            break
    return s


def square_root_latex(coeff: int, radicand: int) -> str:
    """Format a coefficient times a square root in LaTeX."""
    if radicand <= 1:
        return str(coeff)
    if coeff == 1:
        return f"\\sqrt{{{radicand}}}"
    if coeff == -1:
        return f"-\\sqrt{{{radicand}}}"
    return f"{coeff}\\sqrt{{{radicand}}}"


def _as_number(coef: Coef) -> int | float | Fraction:
    if isinstance(coef, Fraction):
        return coef
    if isinstance(coef, float) and abs(coef - round(coef)) < 1e-10:
        return int(round(coef))
    return coef


def _is_zero(coef: Coef) -> bool:
    if isinstance(coef, Fraction):
        return coef == 0
    return abs(float(coef)) < 1e-12


def _is_one(coef: Coef) -> bool:
    if isinstance(coef, Fraction):
        return coef == 1
    return abs(float(coef) - 1) < 1e-12


def _is_neg_one(coef: Coef) -> bool:
    if isinstance(coef, Fraction):
        return coef == -1
    return abs(float(coef) + 1) < 1e-12


def _coef_abs_latex(coef: Coef) -> str:
    """Absolute value of a coefficient as LaTeX (no leading sign)."""
    coef = _as_number(coef)
    if isinstance(coef, Fraction):
        n, d = abs(coef.numerator), coef.denominator
        if d == 1:
            return str(n)
        return f"\\frac{{{n}}}{{{d}}}"
    value = abs(coef)
    if isinstance(value, float) and abs(value - round(value)) < 1e-10:
        return str(int(round(value)))
    return f"{value:g}"


def _power_suffix(variable: str, degree: int, *, latex: bool) -> str:
    if not variable or degree == 0:
        return ""
    if degree == 1:
        return variable
    if latex:
        return f"{variable}^{{{degree}}}"
    return f"{variable}^{degree}"


def format_monomial_latex(
    coef: Coef,
    *,
    variable: str = "x",
    degree: int = 1,
    latex: bool = True,
) -> str | None:
    """Format a single monomial.

    Returns ``None`` when the coefficient is zero so callers can omit the term.
    Constant zero is also ``None``; use :func:`format_polynomial_latex` when the
    whole expression may be the zero polynomial (which renders as ``0``).
    """
    if _is_zero(coef):
        return None

    suffix = _power_suffix(variable, degree, latex=latex)
    if not suffix:
        # Constant term
        coef = _as_number(coef)
        if isinstance(coef, Fraction) and coef.denominator != 1:
            sign = "-" if coef < 0 else ""
            return f"{sign}\\frac{{{abs(coef.numerator)}}}{{{coef.denominator}}}"
        if isinstance(coef, float) and abs(coef - round(coef)) < 1e-10:
            return str(int(round(coef)))
        return str(coef) if not isinstance(coef, float) else f"{coef:g}"

    if _is_one(coef):
        return suffix
    if _is_neg_one(coef):
        return f"-{suffix}"

    coef = _as_number(coef)
    if isinstance(coef, Fraction) and coef.denominator != 1:
        sign = "-" if coef < 0 else ""
        return f"{sign}\\frac{{{abs(coef.numerator)}}}{{{coef.denominator}}}{suffix}"

    if coef < 0:
        return f"-{_coef_abs_latex(coef)}{suffix}"
    return f"{_coef_abs_latex(coef)}{suffix}"


def join_algebra_terms(
    terms: Sequence[str | None],
    *,
    spaced: bool = True,
) -> str:
    """Join monomial strings with ``+`` / ``-``. Empty input becomes ``0``."""
    parts = [term for term in terms if term]
    if not parts:
        return "0"

    sep = " " if spaced else ""
    out = parts[0]
    for term in parts[1:]:
        if term.startswith("-"):
            out += f"{sep}-{sep}{term[1:]}"
        else:
            out += f"{sep}+{sep}{term}"
    return out


def format_polynomial_latex(
    coefficients: Sequence[Coef],
    *,
    variable: str = "x",
    latex: bool = True,
    spaced: bool = True,
    descending: bool = True,
) -> str:
    """Format a polynomial from coefficients.

    By default *coefficients* are highest-degree first (e.g. ``[1, 0, -3]`` →
    ``x^{2} - 3``). Pass ``descending=False`` for lowest-degree first.
    """
    coeffs = list(coefficients)
    if not descending:
        coeffs = list(reversed(coeffs))

    degree = len(coeffs) - 1
    terms: list[str | None] = [
        format_monomial_latex(coef, variable=variable, degree=degree - index, latex=latex)
        for index, coef in enumerate(coeffs)
    ]
    return join_algebra_terms(terms, spaced=spaced)


def format_linear_latex(
    a: Coef,
    b: Coef = 0,
    *,
    variable: str = "x",
    spaced: bool = True,
) -> str:
    """Format ``ax + b`` with standard coefficient conventions."""
    return format_polynomial_latex([a, b], variable=variable, spaced=spaced, latex=True)


def format_slope_intercept_latex(
    m: Coef,
    b: Coef,
    *,
    lhs: str = "y",
    spaced: bool = True,
) -> str:
    """Format ``y = mx + b`` (or custom *lhs*)."""
    rhs = format_linear_latex(m, b, spaced=spaced)
    return f"{lhs} = {rhs}"


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
    """Render a polynomial ratio as LaTeX.

    Constant denominator ±1 collapses to a polynomial (no ``/1``).
    """
    if denominator is None or denominator.is_zero():
        return numerator.to_latex()
    if denominator.deg() == 0:
        lead = float(denominator.coef(0))
        if abs(lead - 1.0) < 1e-10:
            return numerator.to_latex()
        if abs(lead + 1.0) < 1e-10:
            return (numerator * -1).to_latex()
    return fraction_latex(numerator.to_latex(), denominator.to_latex())
