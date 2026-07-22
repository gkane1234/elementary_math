from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any, Literal

from .factoring import (
    NONCLASSROOM_FACTOR_STEP_FLAG,
    FactorablePolynomialOptions,
    create_factorable_polynomial_with_exact_degree,
    format_polynomial_from_factors,
    is_classroom_factorable,
    should_display_factor_product_expanded,
)
from .latex import format_factor_product_latex, fraction_latex
from .polynomial import Polynomial

TermKind = Literal["polynomial", "factor", "full_lcd"]


@dataclass(frozen=True)
class RationalExpressionTerm:
    numerator: Polynomial
    denominator: Polynomial | None
    denominator_factors: tuple[Polynomial, ...] = ()
    denominator_display_expanded: bool = True
    numerator_factors: tuple[Polynomial, ...] = ()
    numerator_display_expanded: bool = True
    term_kind: TermKind = "factor"

    @property
    def is_polynomial_term(self) -> bool:
        return self.denominator is None

    def to_latex(self) -> str:
        """LaTeX for this term (polynomial or fraction)."""
        if self.is_polynomial_term:
            return term_numerator_latex(self)
        assert self.denominator is not None
        if self.denominator.deg() == 0:
            return term_numerator_latex(self)
        return fraction_latex(term_numerator_latex(self), term_denominator_latex(self))

    def to_text(self) -> str:
        """Plain-text for this term."""
        return term_prompt_text(self)


# Backward-compatible alias
PartialFractionTerm = RationalExpressionTerm


@dataclass
class RationalExpressionSolution:
    cancel_factor: Polynomial
    inflation_factor: Polynomial
    numerator_extension: Polynomial
    denominator_extension: Polynomial
    simplified_numerator: Polynomial
    simplified_denominator: Polynomial
    lcd: Polynomial
    lcd_factors: tuple[Polynomial, ...]
    display_terms: tuple[RationalExpressionTerm, ...]
    partial_numerators: tuple[Polynomial, ...]
    polynomial_term: Polynomial | None
    full_lcd_numerator: Polynomial | None
    combined_numerator: Polynomial
    combined_denominator: Polynomial
    cancelled_lcd_factors: tuple[Polynomial, ...] = ()
    final_numerator: Polynomial | None = None
    final_denominator: Polynomial | None = None
    final_numerator_factors: tuple[Polynomial, ...] = ()
    final_denominator_factors: tuple[Polynomial, ...] = ()
    matrix_rows: list[list[float]] = field(default_factory=list)
    matrix_aug_column: list[float] = field(default_factory=list)
    matrix_solution: list[float] = field(default_factory=list)
    # Generation order (answer → prompt). Reverse for the student solution path.
    generation_steps: list[dict[str, str]] = field(default_factory=list)
    # Pedagogy QA flags (e.g. nonclassroom_factor_step) when a solution step
    # asks students to factor something that is not hand-factorable.
    qa_flags: list[str] = field(default_factory=list)
    qa_flag_details: list[dict[str, Any]] = field(default_factory=list)

    def student_solution_steps(self) -> list[str]:
        """LaTeX steps in student order (prompt → answer)."""
        return [
            step["latex"]
            for step in reversed(self.generation_steps)
            if isinstance(step, dict) and step.get("latex")
        ]

    def to_dict(self) -> dict[str, Any]:
        return {
            "cancel_factor": str(self.cancel_factor),
            "cancel_factor_latex": self.cancel_factor.to_latex(),
            "inflation_factor": str(self.inflation_factor),
            "inflation_factor_latex": self.inflation_factor.to_latex(),
            "numerator_extension": str(self.numerator_extension),
            "denominator_extension": str(self.denominator_extension),
            "simplified_numerator": str(self.simplified_numerator),
            "simplified_denominator": str(self.simplified_denominator),
            "simplified_numerator_latex": self.simplified_numerator.to_latex(),
            "simplified_denominator_latex": self.simplified_denominator.to_latex(),
            "lcd": str(self.lcd),
            "lcd_latex": self.lcd.to_latex(),
            "lcd_factors": [str(factor) for factor in self.lcd_factors],
            "polynomial_term": str(self.polynomial_term) if self.polynomial_term else None,
            "full_lcd_numerator": str(self.full_lcd_numerator) if self.full_lcd_numerator else None,
            "display_terms": [
                {
                    "numerator": str(term.numerator),
                    "denominator": None if term.denominator is None else str(term.denominator),
                    "numerator_latex": term.numerator.to_latex(),
                    "denominator_latex": None
                    if term.denominator is None
                    else term_denominator_latex(term),
                    "denominator_factors": [str(factor) for factor in term.denominator_factors],
                    "denominator_display_expanded": term.denominator_display_expanded,
                    "numerator_factors": [str(factor) for factor in term.numerator_factors],
                    "numerator_display_expanded": term.numerator_display_expanded,
                    "term_kind": term.term_kind,
                    "is_polynomial_term": term.is_polynomial_term,
                }
                for term in self.display_terms
            ],
            "partial_numerators": [str(poly) for poly in self.partial_numerators],
            "combined_numerator": str(self.combined_numerator),
            "combined_denominator": str(self.combined_denominator),
            "combined_numerator_latex": self.combined_numerator.to_latex(),
            "combined_denominator_latex": self.combined_denominator.to_latex(),
            "cancelled_lcd_factors": [str(factor) for factor in self.cancelled_lcd_factors],
            "cancelled_lcd_factor_count": len(self.cancelled_lcd_factors),
            "final_numerator": str(self.final_numerator) if self.final_numerator is not None else None,
            "final_denominator": str(self.final_denominator) if self.final_denominator is not None else None,
            "final_numerator_factors": [str(f) for f in self.final_numerator_factors],
            "final_denominator_factors": [str(f) for f in self.final_denominator_factors],
            "final_numerator_latex": (
                self.final_numerator.to_latex() if self.final_numerator is not None else None
            ),
            "final_denominator_latex": (
                self.final_denominator.to_latex() if self.final_denominator is not None else None
            ),
            "matrix_rows": self.matrix_rows,
            "matrix_aug_column": self.matrix_aug_column,
            "matrix_solution": self.matrix_solution,
            "generation_steps": list(self.generation_steps),
            "solution_steps": self.student_solution_steps(),
            "qa_flags": list(self.qa_flags),
            "qa_flag_details": list(self.qa_flag_details),
        }


def _unique_polynomials(factors: list[Polynomial]) -> list[Polynomial]:
    unique: list[Polynomial] = []
    for factor in factors:
        if not any(factor == existing for existing in unique):
            unique.append(factor)
    return unique


def _make_content_primitive(polynomial: Polynomial) -> Polynomial:
    """Divide out integer content so factors like 4x+2 become 2x+1."""
    content = int(polynomial.content_gcd())
    if content <= 1:
        return _integerize_polynomial(polynomial)
    terms: list[tuple[int, int]] = []
    for coefficient, exponent in polynomial.terms:
        value = int(round(float(coefficient)))
        if value % content != 0:
            # Non-integral content — fall back to integerized original.
            return _integerize_polynomial(polynomial)
        scaled = value // content
        if scaled != 0:
            terms.append((scaled, exponent))
    return Polynomial(tuple(terms) if terms else ((0, 0),))


def _integer_coefficient_lcd(denominators: list[Polynomial]) -> Polynomial:
    """Least common multiple over Z[x] (integer-coefficient LCD).

    ``polynomial_lcm`` is Euclidean over Q[x], so ``lcm(x+1, 2x+2)`` collapses
    to ``x+1``. Classroom LCDs must stay integer multiples of every denominator
    (here ``2x+2``), so we LCM contents separately from primitive parts.
    """
    from math import lcm as int_lcm

    from .operations import polynomial_gcd

    nonzero = [
        _integerize_polynomial(den)
        for den in denominators
        if den is not None and not den.is_zero() and den.deg() >= 1
    ]
    if not nonzero:
        return Polynomial([1])

    lcd = nonzero[0]
    for other in nonzero[1:]:
        cont_a = max(1, abs(int(lcd.content_gcd() or 1)))
        cont_b = max(1, abs(int(other.content_gcd() or 1)))
        prim_a = _make_content_primitive(lcd)
        prim_b = _make_content_primitive(other)
        try:
            # Over Q, coprime polys have a constant gcd (e.g. -1/3). Treat as 1.
            gcd_raw = polynomial_gcd(prim_a, prim_b)
            if gcd_raw.deg() <= 0:
                gcd_prim = Polynomial([1])
            else:
                gcd_prim = _make_content_primitive(_integerize_polynomial(gcd_raw))
                if gcd_prim.is_zero() or abs(float(gcd_prim.leading_coefficient())) < 1e-10:
                    gcd_prim = Polynomial([1])
            prim_lcm = _integerize_polynomial(_exact_divide(prim_a * prim_b, gcd_prim))
            lcd = _integerize_polynomial(prim_lcm * int_lcm(cont_a, cont_b))
        except ValueError:
            # Float Euclidean edge case — fall back to product of primitives.
            lcd = _integerize_polynomial(prim_a * prim_b * int_lcm(cont_a, cont_b))

    if float(lcd.leading_coefficient()) < 0:
        lcd = _integerize_polynomial(lcd * -1)
    return lcd


def _scale_fraction_to_integers(
    numerator: Polynomial,
    denominator: Polynomial,
) -> tuple[Polynomial, Polynomial]:
    """Clear fractional coefficients from a rational answer, then reduce content."""
    from fractions import Fraction
    from math import gcd, lcm

    dens = [
        Fraction(float(coefficient)).limit_denominator(10_000).denominator
        for coefficient, _exponent in (*numerator.terms, *denominator.terms)
    ]
    clear_by = 1
    for value in dens:
        clear_by = lcm(clear_by, value)

    def _scaled(poly: Polynomial) -> Polynomial:
        terms: list[tuple[int, int]] = []
        for coefficient, exponent in poly.terms:
            value = int(
                Fraction(float(coefficient)).limit_denominator(10_000) * clear_by
            )
            if value != 0:
                terms.append((value, exponent))
        return Polynomial(tuple(terms) if terms else ((0, 0),))

    num = _scaled(numerator)
    den = _scaled(denominator)
    if den.is_zero():
        return num, Polynomial([1])

    if float(den.leading_coefficient()) < 0:
        num = _integerize_polynomial(num * -1)
        den = _integerize_polynomial(den * -1)

    num_content = abs(int(num.content_gcd() or 0))
    den_content = abs(int(den.content_gcd() or 0))
    common = gcd(num_content, den_content) if num_content and den_content else 1
    if common > 1:
        num_terms = [
            (int(round(float(c))) // common, e)
            for c, e in num.terms
            if int(round(float(c))) // common != 0
        ]
        den_terms = [
            (int(round(float(c))) // common, e)
            for c, e in den.terms
            if int(round(float(c))) // common != 0
        ]
        num = Polynomial(tuple(num_terms) if num_terms else ((0, 0),))
        den = Polynomial(tuple(den_terms) if den_terms else ((1, 0),))

    return _integerize_polynomial(num), _integerize_polynomial(den)


def _simple_linear_factor(
    coef_min: int,
    coef_max: int,
    *,
    monic: bool,
    positive_leading: bool = True,
    allow_monomial: bool = False,
) -> Polynomial:
    """Build a small content-primitive linear (or monomial) factor from coeffs."""
    from math import gcd

    bound = max(1, min(4, abs(coef_min), abs(coef_max) or 4))
    for _ in range(80):
        if monic:
            leading = 1
        else:
            leading = random.randint(2, max(2, bound))
            if positive_leading is False and random.random() < 0.25:
                leading = -leading

        if allow_monomial and random.random() < 0.18:
            constant = 0
        else:
            constant = int(Polynomial.randomCoefficient(coef_min, coef_max, nonZero=True))

        if constant != 0 and gcd(abs(leading), abs(constant)) != 1:
            continue
        if positive_leading and leading < 0:
            leading = -leading
            constant = -constant
        return Polynomial([leading, constant])

    # Fallback: monic x ± 1
    return Polynomial([1, random.choice([-1, 1])])


def _ensure_denominator_factors(
    factors: list[Polynomial],
    term_count: int,
    coef_min: int,
    coef_max: int,
    *,
    monic: bool = True,
    content_primitive: bool = True,
) -> list[Polynomial]:
    unique_factors = _unique_polynomials(factors)
    while len(unique_factors) < term_count:
        candidate = _simple_linear_factor(
            coef_min,
            coef_max,
            monic=monic,
            allow_monomial=False,
        )
        if content_primitive:
            candidate = _make_content_primitive(candidate)
        if not any(candidate == existing for existing in unique_factors):
            unique_factors.append(candidate)
    result = unique_factors[:term_count]
    if content_primitive:
        result = [_make_content_primitive(factor) for factor in result]
    return result


def _product(factors: list[Polynomial]) -> Polynomial:
    result = Polynomial([1])
    for factor in factors:
        result *= factor
    return result


def _factors_to_polynomial(factors: tuple[Polynomial, ...] | list[Polynomial]) -> Polynomial:
    if not factors:
        return Polynomial([1])
    return _product(list(factors))


def _should_display_denominator_expanded(
    factors: tuple[Polynomial, ...],
    options: FactorablePolynomialOptions,
) -> bool:
    return should_display_factor_product_expanded(factors, options)


def _format_factor_product_latex(factors: tuple[Polynomial, ...]) -> str:
    return format_factor_product_latex(factors)


def polynomial_excluded_values(
    denominator: Polynomial,
    coef_min: int = -20,
    coef_max: int = 20,
) -> list[int]:
    """Integer values of x that make *denominator* zero (excluded from domain)."""
    excluded: list[int] = []
    for candidate in range(coef_min, coef_max + 1):
        if abs(float(denominator.evaluate(candidate))) < 1e-8:
            excluded.append(candidate)
    return excluded


def linear_factor_excluded_value(factor: Polynomial):
    """Exact excluded root of a linear factor ``ax + b`` (as ``Fraction``), else ``None``."""
    from fractions import Fraction

    if factor is None or factor.deg() != 1:
        return None
    a = int(round(float(factor.coef(1))))
    b = int(round(float(factor.coef(0))))
    if a == 0:
        return None
    return Fraction(-b, a)


def excluded_values_from_factors(factors) -> list:
    """Excluded values from linear factors (and integer roots of higher-degree pieces).

    Prefer per-factor roots so canceled non-monic linears (e.g. ``3x-2``) are not
    lost when only the expanded LCD product is scanned for integer zeros.
    """
    from fractions import Fraction

    excluded: list[Fraction] = []
    seen: set[Fraction] = set()

    def _add(value) -> None:
        if value is None:
            return
        frac = Fraction(value).limit_denominator()
        if frac in seen:
            return
        seen.add(frac)
        excluded.append(frac)

    for factor in factors or ():
        if factor is None:
            continue
        root = linear_factor_excluded_value(factor)
        if root is not None:
            _add(root)
            continue
        if factor.deg() >= 2:
            for candidate in polynomial_excluded_values(factor, coef_min=-20, coef_max=20):
                _add(candidate)
    return sorted(excluded)


def rational_excluded_values_latex(values: list) -> str:
    """Format excluded values for display, e.g. ``x \\neq 2, -3`` or fractions."""
    if not values:
        return ""
    from fractions import Fraction

    unique: list[Fraction] = []
    seen: set[Fraction] = set()
    for value in values:
        frac = Fraction(value).limit_denominator()
        if frac in seen:
            continue
        seen.add(frac)
        unique.append(frac)
    unique.sort()
    parts: list[str] = []
    for frac in unique:
        if frac.denominator == 1:
            parts.append(str(frac.numerator))
        elif frac.numerator < 0:
            parts.append(f"-\\frac{{{abs(frac.numerator)}}}{{{frac.denominator}}}")
        else:
            parts.append(f"\\frac{{{frac.numerator}}}{{{frac.denominator}}}")
    return f"x \\neq {', '.join(parts)}"


def term_numerator_latex(term: RationalExpressionTerm) -> str:
    if term.numerator_factors and not term.numerator_display_expanded:
        return _format_factor_product_latex(term.numerator_factors)
    return term.numerator.to_latex()


def term_denominator_latex(term: RationalExpressionTerm) -> str:
    if term.denominator is None:
        return ""
    if term.denominator.deg() == 0:
        return term.denominator.to_latex()
    if term.denominator_factors and not term.denominator_display_expanded:
        return _format_factor_product_latex(term.denominator_factors)
    return term.denominator.to_latex()


def _exact_divide(dividend: Polynomial, divisor: Polynomial) -> Polynomial:
    quotient, remainder = dividend.poly_div(divisor)
    if not remainder.is_zero():
        raise ValueError("Polynomial division did not divide evenly")
    return quotient


def _compose_partial_fraction_numerators(
    partial_numerators: list[Polynomial],
    denominator_factors: list[Polynomial],
) -> Polynomial:
    lcd = _product(denominator_factors)
    total = Polynomial(((0, 0),))
    for partial_num, factor in zip(partial_numerators, denominator_factors, strict=True):
        cofactor = _exact_divide(lcd, factor)
        total = total + partial_num * cofactor
    return total


def _solve_partial_fractions_pfd(
    numerator: Polynomial,
    denominator_factors: list[Polynomial],
) -> tuple[list[Polynomial], list[list[float]], list[float], list[float]]:
    from sympy import Matrix, Rational

    prods: list[Polynomial] = []
    for index in range(len(denominator_factors)):
        cofactor = Polynomial([1])
        for other_index, factor in enumerate(denominator_factors):
            if index != other_index:
                cofactor *= factor
        prods.append(cofactor)

    degree = (prods[0] * denominator_factors[0]).deg()
    coefs: list[list] = []
    diffs: list[int] = []

    def _to_rational(value) -> Rational:
        if isinstance(value, Rational):
            return value
        as_float = float(value)
        nearest = round(as_float)
        if abs(as_float - nearest) < 1e-10:
            return Rational(int(nearest))
        return Rational(as_float).limit_denominator(10_000)

    for cofactor in prods:
        term_coef = cofactor.coef_list(reverse=True)
        diff = degree - len(term_coef)
        diffs.append(diff)
        for shift in range(diff + 1):
            coefs.append(
                ([Rational(0)] * shift)
                + [_to_rational(value) for value in term_coef]
                + ([Rational(0)] * (diff - shift))
            )

    numerator_coefs = numerator.coef_list(reverse=True) + (
        [0] * (degree - len(numerator.coef_list(reverse=True)))
    )
    coefs.append([_to_rational(value) for value in numerator_coefs])

    matrix = Matrix(coefs).transpose()
    reduced = matrix.rref()[0]
    variable_count = sum(diff + 1 for diff in diffs)

    partial_numerators: list[Polynomial] = []
    cursor = 0
    for diff in diffs:
        terms = ((0, 0),)
        for exponent in range(diff + 1):
            raw = reduced[cursor + exponent, -1]
            coefficient = _to_rational(raw)
            terms += ((coefficient, exponent),)
        partial_numerators.append(_clear_rational_polynomial(Polynomial(terms[1::])))
        cursor += diff + 1

    solution = [float(reduced[row, -1]) for row in range(variable_count)]
    return partial_numerators, [list(map(float, row)) for row in matrix.tolist()], [
        float(value) for value in numerator_coefs
    ], solution


def _clear_rational_polynomial(polynomial: Polynomial) -> Polynomial:
    """Convert sympy Rational / float coefficients into Python ints or floats."""
    from fractions import Fraction

    terms: list[tuple[float | int, int]] = []
    for coefficient, exponent in polynomial.terms:
        if hasattr(coefficient, "p") and hasattr(coefficient, "q"):
            frac = Fraction(int(coefficient.p), int(coefficient.q))
        else:
            frac = Fraction(float(coefficient)).limit_denominator(10_000)
        if frac.denominator == 1:
            value: float | int = int(frac.numerator)
        else:
            value = float(frac)
        if abs(float(value)) >= 1e-12:
            terms.append((value, exponent))
    return Polynomial(tuple(terms) if terms else ((0, 0),))


def _absorb_coefficient_denominators(
    numerator: Polynomial,
    factors: tuple[Polynomial, ...],
) -> tuple[Polynomial, tuple[Polynomial, ...]]:
    """Rewrite (p/q)/factor as p/(q·factor) so displayed numerators stay integers."""
    from fractions import Fraction
    from math import lcm

    denominators: list[int] = []
    scaled_terms: list[tuple[Fraction, int]] = []
    for coefficient, exponent in numerator.terms:
        frac = Fraction(float(coefficient)).limit_denominator(10_000)
        denominators.append(frac.denominator)
        scaled_terms.append((frac, exponent))

    if not denominators:
        return numerator, factors

    clear_by = lcm(*denominators) if len(denominators) > 1 else denominators[0]
    if clear_by == 1:
        return _integerize_polynomial(numerator), factors

    cleared_terms = [
        (int(frac * clear_by), exponent)
        for frac, exponent in scaled_terms
        if frac * clear_by != 0
    ]
    cleared = Polynomial(tuple(cleared_terms) if cleared_terms else ((0, 0),))
    return cleared, (Polynomial([clear_by]),) + factors


def _max_numerator_degree(denominator: Polynomial) -> int:
    return max(0, denominator.deg() - 1)


def _random_numerator_degree(denominator: Polynomial) -> int:
    return random.randint(0, _max_numerator_degree(denominator))


def random_partial_fraction_numerators(
    denominator_factors: list[Polynomial],
    coef_min: int,
    coef_max: int,
) -> list[Polynomial]:
    partial_numerators: list[Polynomial] = []
    for factor in denominator_factors:
        partial_degree = _random_numerator_degree(factor)
        coeffs = [
            float(Polynomial.randomCoefficient(coef_min, coef_max, nonZero=False))
            for _ in range(partial_degree + 1)
        ]
        coeffs = [int(coeff) if abs(coeff - round(coeff)) < 1e-9 else coeff for coeff in coeffs]
        if partial_degree == 0 and coeffs[0] == 0:
            coeffs[0] = float(Polynomial.randomCoefficient(coef_min, coef_max, nonZero=True))
        terms = tuple((coeff, exponent) for exponent, coeff in enumerate(coeffs) if abs(coeff) >= 1e-10)
        partial_numerators.append(Polynomial(terms or ((0, 0),)))
    return partial_numerators


def _atomic_factors_from_result(factors: tuple[Polynomial, ...]) -> list[Polynomial]:
    return [factor for factor in factors if factor.deg() >= 1]


def _pick_atomic_lcd_factor(
    options: FactorablePolynomialOptions,
    max_factor_degree: int,
) -> Polynomial | None:
    factor_degree = random.randint(1, max(1, max_factor_degree))
    result = create_factorable_polynomial_with_exact_degree(options, factor_degree)
    atomic_factors = _atomic_factors_from_result(result.factors)
    if not atomic_factors:
        return None
    return random.choice(atomic_factors)


def _build_lcd_factors(
    options: FactorablePolynomialOptions,
    lcd_factor_count: int,
    coef_min: int,
    coef_max: int,
    *,
    prefer_simple_factors: bool = False,
    content_primitive: bool = True,
    allow_monomial_factors: bool = False,
) -> list[Polynomial]:
    max_factor_degree = (
        1
        if prefer_simple_factors and options.target_degree_max <= 1
        else (
            2
            if options.rrt_mode == "exclude"
            else min(3, max(2, options.target_degree_max))
        )
    )
    monic = bool(options.leading_coefficient_one)

    if prefer_simple_factors or max_factor_degree <= 1:
        factors: list[Polynomial] = []
        for _ in range(200):
            factors = []
            for _ in range(lcd_factor_count):
                factor = _simple_linear_factor(
                    coef_min,
                    coef_max,
                    monic=monic,
                    positive_leading=options.positive_leading,
                    allow_monomial=allow_monomial_factors,
                )
                if content_primitive:
                    factor = _make_content_primitive(factor)
                factors.append(factor)
            unique_factors = _unique_polynomials(factors)
            if len(unique_factors) >= min(lcd_factor_count, 1 if lcd_factor_count == 1 else 2):
                return _ensure_denominator_factors(
                    unique_factors,
                    lcd_factor_count,
                    coef_min,
                    coef_max,
                    monic=monic,
                    content_primitive=content_primitive,
                )
        return _ensure_denominator_factors(
            [],
            lcd_factor_count,
            coef_min,
            coef_max,
            monic=monic,
            content_primitive=content_primitive,
        )

    for _ in range(200):
        lcd_factors: list[Polynomial] = []
        for _ in range(lcd_factor_count):
            factor = _pick_atomic_lcd_factor(options, max_factor_degree)
            if factor is None:
                break
            if content_primitive:
                factor = _make_content_primitive(factor)
            lcd_factors.append(factor)
        else:
            unique_factors = _unique_polynomials(lcd_factors)
            if len(unique_factors) >= min(2, lcd_factor_count):
                return _ensure_denominator_factors(
                    unique_factors,
                    lcd_factor_count,
                    coef_min,
                    coef_max,
                    monic=monic,
                    content_primitive=content_primitive,
                )

    return _ensure_denominator_factors(
        [],
        lcd_factor_count,
        coef_min,
        coef_max,
        monic=monic,
        content_primitive=content_primitive,
    )


def _pick_term_denominators(
    lcd_factors: list[Polynomial],
    term_count: int,
    max_subset_size: int | None = None,
    *,
    allow_empty: bool = True,
    force_shared_single: bool = False,
) -> list[tuple[Polynomial, ...]]:
    factor_count = len(lcd_factors)
    max_size = factor_count if max_subset_size is None else min(max_subset_size, factor_count)
    denominators: list[tuple[Polynomial, ...]] = []

    if force_shared_single and factor_count >= 1:
        shared = (lcd_factors[0],)
        return [shared for _ in range(term_count)]

    min_subset = 0 if allow_empty else 1
    min_subset = min(min_subset, max_size) if max_size > 0 else 0

    for _ in range(term_count):
        if max_size <= 0:
            denominators.append(())
            continue
        subset_size = random.randint(min_subset, max_size)
        if subset_size == 0:
            denominators.append(())
        else:
            indices = sorted(random.sample(range(factor_count), subset_size))
            denominators.append(tuple(lcd_factors[index] for index in indices))

    if not any(factors for factors in denominators):
        subset_size = random.randint(1, max(1, max_size))
        indices = sorted(random.sample(range(factor_count), min(subset_size, factor_count)))
        denominators[-1] = tuple(lcd_factors[index] for index in indices)

    if not allow_empty:
        for index, factors in enumerate(denominators):
            if factors:
                continue
            subset_size = 1 if max_subset_size == 1 else random.randint(1, max(1, max_size))
            indices = sorted(random.sample(range(factor_count), min(subset_size, factor_count)))
            denominators[index] = tuple(lcd_factors[i] for i in indices)

    nonzero_denominators = [factors for factors in denominators if factors]
    if term_count >= 2 and len(_unique_polynomials([_factors_to_polynomial(f) for f in nonzero_denominators])) < 2:
        if max_subset_size == 1:
            used = nonzero_denominators[0] if nonzero_denominators else None
            alternatives = [
                (factor,)
                for factor in lcd_factors
                if used is None or not (factor == used[0])
            ]
            if alternatives:
                denominators[-1] = random.choice(alternatives)
        elif not force_shared_single:
            denominators[-1] = tuple(lcd_factors)

    return denominators


def _random_numerator_for_denominator(
    denominator: Polynomial,
    coef_min: int,
    coef_max: int,
    positive_leading: bool,
) -> Polynomial:
    partial_degree = _random_numerator_degree(denominator)
    if partial_degree == 0:
        return Polynomial([Polynomial.randomCoefficient(coef_min, coef_max, nonZero=True)])
    return Polynomial.random_polynomial(
        partial_degree,
        coef_min,
        coef_max,
        positive_leading=positive_leading,
    )


def _compose_over_term_denominators(
    partial_numerators: list[Polynomial],
    term_denominators: list[Polynomial],
    lcd: Polynomial,
) -> Polynomial:
    total = Polynomial(((0, 0),))
    for partial_num, term_denominator in zip(partial_numerators, term_denominators, strict=True):
        if term_denominator.deg() == 0:
            cofactor = lcd
        else:
            cofactor = _exact_divide(lcd, term_denominator)
        total = total + partial_num * cofactor
    return total


def _resolve_cancel_factor_count(
    cancel_factor_count: int | str | None,
    lcd_factor_count: int,
) -> int:
    if lcd_factor_count <= 0:
        return 0
    if cancel_factor_count is None:
        return random.randint(0, lcd_factor_count)
    if isinstance(cancel_factor_count, str):
        text = cancel_factor_count.strip().lower()
        if text in {"", "random", "auto"}:
            return random.randint(0, lcd_factor_count)
        if text in {"all", "all_available", "max"}:
            return lcd_factor_count
        cancel_factor_count = text
    # Explicit request: cancel exactly that many, or all available if fewer exist.
    return max(0, min(int(cancel_factor_count), lcd_factor_count))


def _pick_cancelled_lcd_factors(
    lcd_factors: list[Polynomial],
    cancel_count: int,
) -> tuple[Polynomial, ...]:
    if cancel_count <= 0:
        return ()
    return tuple(random.sample(lcd_factors, cancel_count))


def _remaining_lcd_factors(
    lcd_factors: list[Polynomial],
    cancelled_lcd_factors: tuple[Polynomial, ...],
) -> list[Polynomial]:
    cancelled = list(cancelled_lcd_factors)
    remaining: list[Polynomial] = []
    for factor in lcd_factors:
        matched = next((index for index, cancel in enumerate(cancelled) if factor == cancel), None)
        if matched is None:
            remaining.append(factor)
        else:
            cancelled.pop(matched)
    return remaining


def _final_form_after_cancellation(
    simplified_numerator: Polynomial,
    lcd_factors: list[Polynomial],
    cancelled_lcd_factors: tuple[Polynomial, ...],
) -> tuple[Polynomial, Polynomial] | None:
    if not cancelled_lcd_factors:
        return simplified_numerator, _product(lcd_factors)

    cancel_product = _factors_to_polynomial(cancelled_lcd_factors)
    final_numerator, remainder = simplified_numerator.poly_div(cancel_product)
    if not remainder.is_zero():
        return None

    remaining_factors = _remaining_lcd_factors(lcd_factors, cancelled_lcd_factors)
    final_denominator = (
        _factors_to_polynomial(remaining_factors) if remaining_factors else Polynomial([1])
    )
    return final_numerator, final_denominator


def _integerize_polynomial(polynomial: Polynomial) -> Polynomial:
    terms: list[tuple[float | int, int]] = []
    for coefficient, exponent in polynomial.terms:
        nearest = round(float(coefficient))
        if abs(float(coefficient) - nearest) < 1e-8:
            value: float | int = int(nearest)
        else:
            value = float(coefficient)
        if abs(float(value)) >= 1e-10:
            terms.append((value, exponent))
    return Polynomial(tuple(terms) if terms else ((0, 0),))


def _merge_fraction_entries(
    left_num: Polynomial,
    left_factors: tuple[Polynomial, ...],
    right_num: Polynomial,
    right_factors: tuple[Polynomial, ...],
) -> tuple[Polynomial, tuple[Polynomial, ...]]:
    left_den = _factors_to_polynomial(left_factors)
    right_den = _factors_to_polynomial(right_factors)
    return left_num * right_den + right_num * left_den, left_factors + right_factors


def _package_pfd_entries(
    partial_numerators: list[Polynomial],
    lcd_factors: list[Polynomial],
    target_term_count: int,
    max_subset_size: int | None,
) -> list[tuple[Polynomial, tuple[Polynomial, ...]]]:
    entries: list[tuple[Polynomial, tuple[Polynomial, ...]]] = []
    for numerator, factor in zip(partial_numerators, lcd_factors, strict=True):
        cleaned = _integerize_polynomial(_clear_rational_polynomial(numerator))
        if cleaned.is_zero():
            continue
        cleared_num, cleared_factors = _absorb_coefficient_denominators(cleaned, (factor,))
        entries.append((cleared_num, cleared_factors))

    if not entries:
        return []

    random.shuffle(entries)

    can_merge = max_subset_size is None or max_subset_size > 1
    while can_merge and len(entries) > max(1, target_term_count):
        mergeable = [
            index
            for index, (_, factors) in enumerate(entries)
            if max_subset_size is None or len([f for f in factors if f.deg() > 0]) < max_subset_size
        ]
        if len(mergeable) < 2:
            break
        left_index, right_index = sorted(random.sample(mergeable, 2))
        right_num, right_factors = entries.pop(right_index)
        left_num, left_factors = entries.pop(left_index)
        variable_count = len([f for f in left_factors + right_factors if f.deg() > 0])
        if max_subset_size is not None and variable_count > max_subset_size:
            entries.insert(left_index, (left_num, left_factors))
            insert_right = right_index if right_index <= left_index else right_index - 1
            entries.insert(insert_right, (right_num, right_factors))
            break
        merged_num, merged_factors = _merge_fraction_entries(
            left_num,
            left_factors,
            right_num,
            right_factors,
        )
        merged_num, merged_factors = _absorb_coefficient_denominators(
            _integerize_polynomial(merged_num),
            merged_factors,
        )
        entries.append((merged_num, merged_factors))
        random.shuffle(entries)

    random.shuffle(entries)
    return entries


def _split_polynomial_into_summands(
    total: Polynomial,
    parts: int,
    coef_min: int,
    coef_max: int,
) -> list[Polynomial]:
    parts = max(1, parts)
    if parts == 1 or total.is_zero():
        return [total]

    if total.deg() != 0:
        # Only split constants; higher-degree totals stay whole.
        return [total]

    value = int(round(float(total.coef_list(reverse=True)[0])))
    if value == 0:
        return [total]

    max_parts = max(1, abs(value))
    parts = min(parts, max_parts)

    summands: list[Polynomial] = []
    remaining_value = value
    for index in range(parts - 1):
        slots_left_after = parts - 2 - index
        low = max(coef_min, remaining_value - coef_max * max(slots_left_after, 0) - coef_max)
        high = min(coef_max, remaining_value - coef_min * max(slots_left_after, 0) - coef_min)
        if low > high:
            low, high = coef_min, coef_max
        candidates = [candidate for candidate in range(low, high + 1) if candidate != 0]
        if not candidates:
            candidates = [candidate for candidate in range(coef_min, coef_max + 1) if candidate != 0]
        piece_value = random.choice(candidates)
        # Keep leftover representable in the remaining slots.
        leftover = remaining_value - piece_value
        if slots_left_after == 0 and leftover == 0:
            piece_value = 1 if remaining_value != 1 else -1
            if abs(piece_value) > abs(coef_max) and coef_max != 0:
                piece_value = 1 if remaining_value > 0 else -1
            leftover = remaining_value - piece_value
        summands.append(Polynomial([piece_value]))
        remaining_value = leftover

    if remaining_value == 0:
        if summands:
            adjust = 1 if summands[-1].coef_list(reverse=True)[0] > 0 else -1
            summands[-1] = summands[-1] - Polynomial([adjust])
            remaining_value = adjust
    summands.append(Polynomial([remaining_value]))
    return summands


def _poly_divisible_by(dividend: Polynomial, divisor: Polynomial) -> bool:
    if divisor.is_zero() or divisor.deg() < 1:
        return False
    try:
        _exact_divide(dividend, divisor)
        return True
    except ValueError:
        return False


def _numerator_shares_den_factor(
    numerator: Polynomial,
    den_factors: tuple[Polynomial, ...] | list[Polynomial],
) -> bool:
    """True when a displayed term already cancels (num shares a den factor)."""
    if numerator.is_zero():
        return False
    for factor in den_factors:
        if factor.deg() >= 1 and _poly_divisible_by(numerator, factor):
            return True
    return False


def _count_per_term_cancels(
    numerators: list[Polynomial],
    den_factor_lists: list[tuple[Polynomial, ...]],
) -> int:
    return sum(
        1
        for num, dens in zip(numerators, den_factor_lists, strict=True)
        if _numerator_shares_den_factor(num, dens)
    )


def _split_target_for_add_then_cancel(
    target: Polynomial,
    avoid_factors: tuple[Polynomial, ...],
    parts: int,
    coef_min: int,
    coef_max: int,
    positive_leading: bool,
    *,
    rrt_exclude: bool = True,
) -> list[Polynomial] | None:
    """Split combined numerator into summands that rarely share avoid_factors.

    No individual summand should be divisible by a cancel factor when all terms
    share the full LCD (that would allow per-term cancel). With RRT excluded,
    keep companion degrees ≤ 2; the residual may still be higher degree — callers
    should prefer unlike dens when ``target.deg() >= 3``.
    """
    parts = max(2, parts)
    max_deg = max(0, target.deg())
    if rrt_exclude:
        max_deg = min(max_deg, 2)

    for _ in range(80):
        summands: list[Polynomial] = []
        running = Polynomial(((0, 0),))
        for _index in range(parts - 1):
            # Prefer constants so cancel structure is not concentrated awkwardly.
            if rrt_exclude or random.random() < 0.65:
                deg = 0
            else:
                deg = random.randint(0, max_deg)
            if deg == 0:
                piece = Polynomial(
                    [Polynomial.randomCoefficient(coef_min, coef_max, nonZero=True)]
                )
            else:
                piece = Polynomial.random_polynomial(
                    deg, coef_min, coef_max, positive_leading=positive_leading
                )
                if piece.is_zero():
                    piece = Polynomial(
                        [Polynomial.randomCoefficient(coef_min, coef_max, nonZero=True)]
                    )
            summands.append(_integerize_polynomial(piece))
            running = running + piece
        last = _integerize_polynomial(target - running)
        if last.is_zero() or any(s.is_zero() for s in summands):
            continue
        summands.append(last)
        # Every summand must avoid cancel factors for shared-LCD pedagogy.
        shared = _count_per_term_cancels(
            summands,
            [tuple(avoid_factors) for _ in summands],
        )
        if shared == 0:
            return summands
        if shared == 1 and random.random() < 0.08:
            return summands

    # Fallback: constant offset split (last usually avoids exact cancel factors).
    if target.deg() == 0:
        return _split_polynomial_into_summands(target, parts, coef_min, coef_max)
    offset = Polynomial(
        [Polynomial.randomCoefficient(coef_min, coef_max, nonZero=True)]
    )
    last = _integerize_polynomial(target - offset)
    if last.is_zero():
        offset = Polynomial([offset.coef_list(reverse=True)[0] + 1])
        last = _integerize_polynomial(target - offset)
    return [last, offset]


def _known_numerator_factors_for_display(
    numerator: Polynomial,
    cancelled_lcd_factors: tuple[Polynomial, ...],
    options: FactorablePolynomialOptions,
) -> tuple[Polynomial, ...]:
    """Recover linear factors from construction when expanded form needs RRT."""
    if numerator.is_zero() or numerator.deg() <= 2:
        return ()
    if options.rrt_mode != "exclude":
        return ()
    remaining = numerator
    peeled: list[Polynomial] = []
    for factor in cancelled_lcd_factors:
        if factor.deg() < 1:
            continue
        if _poly_divisible_by(remaining, factor):
            try:
                remaining = _exact_divide(remaining, factor)
            except ValueError:
                continue
            peeled.append(factor)
    if not peeled:
        return ()
    remaining = _integerize_polynomial(remaining)
    if remaining.is_zero():
        return ()
    # Only useful when peeling leaves a simple cofactor and enough factors to
    # justify factored display (≥3 variable factors total, or deg≥3 product).
    factors = ((remaining,) if not (
        remaining.deg() == 0 and abs(float(remaining.coef(0)) - 1.0) < 1e-10
    ) else ()) + tuple(peeled)
    variable = [f for f in factors if f.deg() >= 1]
    if len(variable) < 2 and remaining.deg() <= 2:
        return ()
    if not should_display_factor_product_expanded(factors, options):
        return factors
    return ()


def _build_cancelled_expression_pieces(
    options: FactorablePolynomialOptions,
    lcd_factors: list[Polynomial],
    cancelled_lcd_factors: tuple[Polynomial, ...],
    factor_term_count: int,
    include_polynomial: bool,
    max_subset_size: int | None,
) -> tuple[
    Polynomial | None,
    list[Polynomial],
    list[tuple[Polynomial, ...]],
    Polynomial,
    Polynomial,
    Polynomial,
    tuple[Polynomial, ...],
    tuple[Polynomial, ...],
    list[tuple[Polynomial, ...]],
] | None:
    """Build an add-then-cancel rational sum.

    ``cancel_factor_count`` means: after rewriting over the LCD and adding
    numerators, that many LCD factors cancel. Individual terms generally do
    *not* already carry those cancel factors in both num and den (per-term
    inflation is rare, not the main mechanism).

    When RRT is excluded, the expanded combined numerator must stay
    hand-factorable (deg ≤ 2). Callers should clamp cancel count accordingly
    and avoid polynomial/full-LCD terms that inflate the combined degree.
    """
    coef_min, coef_max = options.normalized_coef_range()
    lcd = _product(lcd_factors)
    cancel_product = _factors_to_polynomial(cancelled_lcd_factors)
    remaining_factors = _remaining_lcd_factors(lcd_factors, cancelled_lcd_factors)
    lcd_factor_tuple = tuple(lcd_factors)
    remaining_tuple = tuple(remaining_factors)
    rrt_exclude = options.rrt_mode == "exclude"

    # Poly / full-LCD extras make the expanded combined num RRT-hard; skip them
    # for honest end-cancel pedagogy when RRT is off.
    if rrt_exclude and cancelled_lcd_factors:
        include_polynomial = False

    polynomial_term = None
    if include_polynomial:
        polynomial_term = _random_polynomial_term(
            coef_min,
            coef_max,
            max_degree=min(2, max(0, lcd.deg() - 1)),
            positive_leading=options.positive_leading,
        )

    # Constant reduced numerator keeps the post-cancel answer readable.
    # Combined num = final_core × cancel_product → deg = cancel count (linears).
    min_abs = max(1, min(3, abs(coef_max) or 3))
    final_value = int(Polynomial.randomCoefficient(coef_min, coef_max, nonZero=True))
    if abs(final_value) < min_abs:
        sign = 1 if final_value > 0 else -1
        final_value = sign * min_abs
    final_core = Polynomial([final_value])

    # Pre-cancel combined numerator over the full LCD.
    target_fractional = _integerize_polynomial(final_core * cancel_product)
    if rrt_exclude and target_fractional.deg() > 2:
        return None

    n_terms = max(2, int(factor_term_count))

    summands = _split_target_for_add_then_cancel(
        target_fractional,
        cancelled_lcd_factors,
        n_terms,
        coef_min,
        coef_max,
        options.positive_leading,
        rrt_exclude=rrt_exclude,
    )
    if not summands:
        return None

    # Prefer shared LCD whenever the combined numerator is classroom-degree.
    # When RRT is off, force shared LCD so the student path is: rewrite → add →
    # factor expanded combined (≤ quadratic) → cancel — no unlike-den residuals.
    use_shared_lcd = target_fractional.deg() <= 2
    if rrt_exclude and cancelled_lcd_factors:
        use_shared_lcd = True
    packaged_numerators = [s for s in summands if not s.is_zero()]
    packaged_factor_lists: list[tuple[Polynomial, ...]] = [
        lcd_factor_tuple for _ in packaged_numerators
    ]
    packaged_num_factor_lists: list[tuple[Polynomial, ...]] = [
        _known_numerator_factors_for_display(num, cancelled_lcd_factors, options)
        for num in packaged_numerators
    ]

    # Unlike dens (add-then-cancel): residual method with rejection when a term
    # would already cancel. Forced when shared LCD would show RRT-hard nums.
    allow_unlike = (
        (not use_shared_lcd)
        or (
            (not rrt_exclude or not cancelled_lcd_factors)
            and (max_subset_size is None or max_subset_size >= 1)
            and len(lcd_factors) >= 2
            and random.random() < 0.4
        )
    )
    unlike_ok = False
    if allow_unlike:
        for _attempt in range(40 if not use_shared_lcd else 25):
            dens = _pick_term_denominators(
                lcd_factors,
                len(packaged_numerators),
                max_subset_size=max_subset_size,
                allow_empty=False,
                force_shared_single=False,
            )
            if len(dens) != len(packaged_numerators):
                continue
            dens_list = list(dens)
            nums: list[Polynomial] = []
            ok = True
            for i in range(len(dens_list) - 1):
                den_poly = _factors_to_polynomial(dens_list[i])
                num = _random_numerator_for_denominator(
                    den_poly, coef_min, coef_max, options.positive_leading
                )
                for _retry in range(10):
                    if not _numerator_shares_den_factor(num, dens_list[i]):
                        break
                    num = _random_numerator_for_denominator(
                        den_poly, coef_min, coef_max, options.positive_leading
                    )
                if _numerator_shares_den_factor(num, dens_list[i]):
                    ok = False
                    break
                # Keep prompt nums classroom-factorable when RRT is off.
                if options.rrt_mode == "exclude" and num.deg() >= 3:
                    ok = False
                    break
                nums.append(_integerize_polynomial(num))
            if not ok:
                continue
            try:
                partial = _compose_over_term_denominators(
                    nums,
                    [_factors_to_polynomial(d) for d in dens_list[:-1]],
                    lcd,
                )
            except ValueError:
                continue
            residual = _integerize_polynomial(target_fractional - partial)
            last_den = _factors_to_polynomial(dens_list[-1])
            try:
                cofactor = _exact_divide(lcd, last_den)
                last_num = _exact_divide(residual, cofactor)
            except ValueError:
                dens_list[-1] = lcd_factor_tuple
                last_num = residual
            last_num = _integerize_polynomial(last_num)
            if last_num.is_zero():
                continue
            if _numerator_shares_den_factor(last_num, dens_list[-1]):
                continue
            if options.rrt_mode == "exclude" and last_num.deg() >= 3:
                # Only accept if we can show it factored from known cancels.
                known = _known_numerator_factors_for_display(
                    last_num, cancelled_lcd_factors, options
                )
                if not known:
                    continue
            nums.append(last_num)
            if _count_per_term_cancels(nums, dens_list) > 0:
                continue
            try:
                check = _compose_over_term_denominators(
                    nums,
                    [_factors_to_polynomial(d) for d in dens_list],
                    lcd,
                )
            except ValueError:
                continue
            if _integerize_polynomial(check - target_fractional).is_zero():
                packaged_numerators = nums
                packaged_factor_lists = [tuple(d) for d in dens_list]
                packaged_num_factor_lists = [
                    _known_numerator_factors_for_display(
                        num, cancelled_lcd_factors, options
                    )
                    for num in nums
                ]
                unlike_ok = True
                break

    if not use_shared_lcd and not unlike_ok:
        # Last resort: shared LCD with factored high-degree nums when possible.
        if any(
            options.rrt_mode == "exclude"
            and num.deg() >= 3
            and not packaged_num_factor_lists[i]
            for i, num in enumerate(packaged_numerators)
        ):
            return None

    # Rare light per-term cancel spice (~8%): inflate one term by one cancel factor.
    # Skip when RRT is off — spice makes per-term cancel visible, which is a
    # different skill than honest end-of-addition cancel.
    if (
        cancelled_lcd_factors
        and packaged_numerators
        and not rrt_exclude
        and random.random() < 0.08
    ):
        idx = random.randrange(len(packaged_numerators))
        spice = random.choice(cancelled_lcd_factors)
        if spice not in packaged_factor_lists[idx]:
            packaged_numerators[idx] = _integerize_polynomial(
                packaged_numerators[idx] * spice
            )
            packaged_factor_lists[idx] = packaged_factor_lists[idx] + (spice,)
            base_num_factors = packaged_num_factor_lists[idx]
            if base_num_factors:
                packaged_num_factor_lists[idx] = base_num_factors + (spice,)
            elif packaged_numerators[idx].deg() >= 3:
                packaged_num_factor_lists[idx] = _known_numerator_factors_for_display(
                    packaged_numerators[idx], cancelled_lcd_factors, options
                )

    if not packaged_numerators and polynomial_term is None:
        return None

    simplified_numerator = target_fractional
    if polynomial_term is not None:
        simplified_numerator = simplified_numerator + polynomial_term * lcd
    simplified_numerator = _integerize_polynomial(simplified_numerator)
    if simplified_numerator.is_zero():
        return None

    final_form = _final_form_after_cancellation(
        simplified_numerator,
        lcd_factors,
        cancelled_lcd_factors,
    )
    if final_form is None:
        return None
    final_numerator, final_denominator = final_form

    # Known factors for factored answer presentation.
    if polynomial_term is None and final_numerator.deg() == 0:
        final_num_factors: tuple[Polynomial, ...] = (final_numerator,)
    else:
        final_num_factors = ()
    final_den_factors = remaining_tuple

    return (
        polynomial_term,
        packaged_numerators,
        packaged_factor_lists,
        simplified_numerator,
        final_numerator,
        final_denominator,
        final_num_factors,
        final_den_factors,
        packaged_num_factor_lists,
    )


def _maybe_pick_term_inflation(
    options: FactorablePolynomialOptions,
    inflation_chance: float,
    max_inflation_degree: int,
) -> Polynomial:
    if inflation_chance <= 0 or random.random() >= inflation_chance:
        return Polynomial([1])

    coef_min, coef_max = options.normalized_coef_range()
    inflation_degree = random.randint(1, max(1, max_inflation_degree))
    if options.rrt_mode == "exclude":
        inflation_degree = 1
    if inflation_degree == 1:
        return Polynomial([1, Polynomial.randomCoefficient(coef_min, coef_max, nonZero=True)])
    result = create_factorable_polynomial_with_exact_degree(options, inflation_degree)
    return result.polynomial


def _random_polynomial_term(
    coef_min: int,
    coef_max: int,
    max_degree: int,
    positive_leading: bool,
) -> Polynomial:
    degree = random.randint(0, max(0, max_degree))
    if degree == 0:
        return Polynomial([Polynomial.randomCoefficient(coef_min, coef_max, nonZero=True)])
    return Polynomial.random_polynomial(degree, coef_min, coef_max, positive_leading=positive_leading)


def _build_fraction_display_term(
    numerator: Polynomial,
    denominator_factors: tuple[Polynomial, ...],
    term_inflation: Polynomial,
    options: FactorablePolynomialOptions,
    force_factored: bool = False,
    numerator_factors: tuple[Polynomial, ...] | None = None,
) -> RationalExpressionTerm:
    base_denominator = _factors_to_polynomial(denominator_factors)
    display_factors = denominator_factors
    num_factors = tuple(numerator_factors) if numerator_factors else ()
    if term_inflation.deg() > 0:
        # Decide expand-vs-factored on the *final* factor list. Inflating a
        # classroom-quadratic (2 linears → expand) with another linear yields a
        # dense cubic that needs RRT — keep that product factored when RRT is off.
        display_factors = denominator_factors + (term_inflation,)
        if num_factors:
            inflated_num_factors = num_factors + (term_inflation,)
        elif numerator.deg() == 0 and not numerator.is_zero():
            # constant × inflation linear — track factors for RRT policy
            inflated_num_factors = (numerator, term_inflation)
        else:
            inflated_num_factors = ()
        display_expanded = (
            False
            if force_factored
            else _should_display_denominator_expanded(display_factors, options)
        )
        num_expanded = (
            False
            if force_factored
            else (
                _should_display_denominator_expanded(inflated_num_factors, options)
                if inflated_num_factors
                else True
            )
        )
        return RationalExpressionTerm(
            numerator=numerator * term_inflation,
            denominator=base_denominator * term_inflation,
            denominator_factors=display_factors,
            denominator_display_expanded=display_expanded,
            numerator_factors=inflated_num_factors,
            numerator_display_expanded=num_expanded,
            term_kind="factor",
        )
    display_expanded = (
        False
        if force_factored
        else _should_display_denominator_expanded(denominator_factors, options)
    )
    num_expanded = (
        False
        if force_factored
        else (
            _should_display_denominator_expanded(num_factors, options)
            if num_factors
            else True
        )
    )
    return RationalExpressionTerm(
        numerator=numerator,
        denominator=base_denominator,
        denominator_factors=display_factors,
        denominator_display_expanded=display_expanded,
        numerator_factors=num_factors,
        numerator_display_expanded=num_expanded,
        term_kind="factor",
    )


def _lcd_display_latex(lcd: Polynomial, lcd_factors: tuple[Polynomial, ...]) -> str:
    """Prefer factored LCD when construction tracked multiple factors."""
    if lcd_factors and len(lcd_factors) > 1:
        return format_factor_product_latex(lcd_factors)
    if lcd_factors and len(lcd_factors) == 1:
        return lcd_factors[0].to_latex()
    return lcd.to_latex()


def _is_unit_constant(poly: Polynomial) -> bool:
    return (
        not poly.is_zero()
        and poly.deg() == 0
        and abs(float(poly.coef(0)) - 1.0) < 1e-10
    )


def _product_matches(factors: tuple[Polynomial, ...], target: Polynomial) -> bool:
    if not factors:
        return False
    product = factors[0]
    for other in factors[1:]:
        product = product * other
    return _integerize_polynomial(product - target).is_zero()


def _rewritten_numerator_over_lcd(
    term: RationalExpressionTerm,
    lcd: Polynomial,
) -> Polynomial | None:
    """Numerator of ``term`` after rewriting over ``lcd``, or None if not exact."""
    if term.is_polynomial_term or term.denominator is None or term.denominator.deg() < 1:
        return _integerize_polynomial(term.numerator * lcd)
    try:
        cofactor = _exact_divide(lcd, term.denominator)
    except ValueError:
        return None
    return _integerize_polynomial(term.numerator * cofactor)


def _rewritten_numerator_factors_for_display(
    term: RationalExpressionTerm,
    lcd_factors: tuple[Polynomial, ...],
    rewritten_num: Polynomial,
) -> tuple[Polynomial, ...]:
    """Known factors for a term rewritten over the LCD (when construction tracked them)."""
    if rewritten_num.is_zero():
        return ()

    if term.is_polynomial_term or term.denominator is None or term.denominator.deg() < 1:
        # polynomial × LCD → show poly × LCD factors so dens cancel by eye.
        if _is_unit_constant(term.numerator):
            factors = tuple(lcd_factors)
        else:
            factors = (term.numerator,) + tuple(lcd_factors)
        return factors if _product_matches(factors, rewritten_num) else ()

    cofactor_factors = tuple(
        _remaining_lcd_factors(list(lcd_factors), term.denominator_factors)
    )
    num_factors = tuple(term.numerator_factors)
    if not num_factors:
        if _is_unit_constant(term.numerator):
            num_factors = ()
        elif term.numerator.deg() == 0 and not term.numerator.is_zero():
            num_factors = (term.numerator,)
        else:
            return ()

    factors = num_factors + cofactor_factors
    return factors if _product_matches(factors, rewritten_num) else ()


def _rewritten_numerator_latex(
    term: RationalExpressionTerm,
    lcd: Polynomial,
    lcd_factors: tuple[Polynomial, ...],
    options: FactorablePolynomialOptions,
) -> str | None:
    rewritten_num = _rewritten_numerator_over_lcd(term, lcd)
    if rewritten_num is None:
        return None
    factors = _rewritten_numerator_factors_for_display(term, lcd_factors, rewritten_num)
    # Prefer factored when expanded form would be RRT-hard (or poly×multi-factor LCD).
    if factors and not should_display_factor_product_expanded(factors, options):
        return format_polynomial_from_factors(factors, options, force_factored=True)
    if factors and options.rrt_mode == "exclude" and rewritten_num.deg() >= 3:
        return format_polynomial_from_factors(factors, options, force_factored=True)
    return rewritten_num.to_latex()


def _force_factored_answer_dens(
    denominator_factors: tuple[Polynomial, ...],
    options: FactorablePolynomialOptions,
) -> bool:
    """Keep 2+ remaining linears factored in the answer when RRT is off."""
    if options.rrt_mode != "exclude":
        return False
    variable = [f for f in denominator_factors if f.deg() >= 1]
    return len(variable) >= 2


def _combined_numerator_factor_candidates(
    combined_numerator: Polynomial,
    cancelled_lcd_factors: tuple[Polynomial, ...],
    final_numerator: Polynomial | None,
    final_numerator_factors: tuple[Polynomial, ...] = (),
) -> tuple[Polynomial, ...]:
    """Best-effort construction factors for the expanded combined numerator."""
    if combined_numerator.is_zero():
        return ()
    remaining: tuple[Polynomial, ...] = ()
    if final_numerator_factors and _product_matches(
        final_numerator_factors, final_numerator or Polynomial([1])
    ):
        remaining = tuple(
            f
            for f in final_numerator_factors
            if not (f.deg() == 0 and _is_unit_constant(f))
        )
    elif final_numerator is not None and not final_numerator.is_zero():
        if not _is_unit_constant(final_numerator):
            remaining = (final_numerator,)

    cancelled = tuple(f for f in cancelled_lcd_factors if f.deg() >= 1 or not _is_unit_constant(f))
    factors = cancelled + remaining
    if factors and _product_matches(factors, combined_numerator):
        return factors
    if cancelled and _product_matches(cancelled, combined_numerator):
        return cancelled
    return ()


def collect_nonclassroom_factor_step_details(
    display_terms: tuple[RationalExpressionTerm, ...] | list[RationalExpressionTerm],
    *,
    combined_numerator: Polynomial,
    cancelled_lcd_factors: tuple[Polynomial, ...],
    final_numerator: Polynomial | None = None,
    final_numerator_factors: tuple[Polynomial, ...] = (),
    options: FactorablePolynomialOptions | None = None,
) -> list[dict[str, Any]]:
    """Return details for solution-step targets that are not classroom-factorable.

    Checks:
    - Expanded prompt nums/dens whose known factors need RRT
    - Combined-before-cancel numerator when end-cancel requires factoring it
    """
    opts = options or FactorablePolynomialOptions(coef_min=-8, coef_max=8)
    details: list[dict[str, Any]] = []

    for index, term in enumerate(display_terms):
        if (
            term.denominator is not None
            and term.denominator_display_expanded
            and term.denominator_factors
            and term.denominator.deg() >= 1
            and not is_classroom_factorable(
                term.denominator, opts, factors=term.denominator_factors
            )
        ):
            details.append(
                {
                    "flag": NONCLASSROOM_FACTOR_STEP_FLAG,
                    "role": "prompt_denominator",
                    "term_index": index,
                    "degree": term.denominator.deg(),
                    "latex": term.denominator.to_latex(),
                }
            )
        if (
            term.numerator_display_expanded
            and term.numerator_factors
            and term.numerator.deg() >= 1
            and not is_classroom_factorable(
                term.numerator, opts, factors=term.numerator_factors
            )
        ):
            details.append(
                {
                    "flag": NONCLASSROOM_FACTOR_STEP_FLAG,
                    "role": "prompt_numerator",
                    "term_index": index,
                    "degree": term.numerator.deg(),
                    "latex": term.numerator.to_latex(),
                }
            )

    if cancelled_lcd_factors and combined_numerator.deg() >= 1:
        factors = _combined_numerator_factor_candidates(
            combined_numerator,
            cancelled_lcd_factors,
            final_numerator,
            final_numerator_factors,
        )
        if not is_classroom_factorable(combined_numerator, opts, factors=factors or None):
            details.append(
                {
                    "flag": NONCLASSROOM_FACTOR_STEP_FLAG,
                    "role": "combined_before_cancel",
                    "degree": combined_numerator.deg(),
                    "latex": combined_numerator.to_latex(),
                    "cancelled_factor_count": len(cancelled_lcd_factors),
                }
            )

    return details


def nonclassroom_factor_step_qa_flags(
    details: list[dict[str, Any]],
) -> list[str]:
    """Deduplicate flag names from detail records."""
    flags: list[str] = []
    for detail in details:
        name = str(detail.get("flag") or "")
        if name and name not in flags:
            flags.append(name)
    return flags


def _record_rational_generation_steps(
    display_terms: tuple[RationalExpressionTerm, ...] | list[RationalExpressionTerm],
    lcd: Polynomial,
    lcd_factors: tuple[Polynomial, ...],
    combined_numerator: Polynomial,
    combined_denominator: Polynomial,
    cancelled_lcd_factors: tuple[Polynomial, ...],
    final_numerator: Polynomial,
    final_denominator: Polynomial,
    final_numerator_factors: tuple[Polynomial, ...] = (),
    final_denominator_factors: tuple[Polynomial, ...] = (),
    options: FactorablePolynomialOptions | None = None,
) -> list[dict[str, str]]:
    """Record generation steps in answer→prompt order (reverse for students).

    Typical cancel≥1 construction:
      final → combined-before-cancel → sum over LCD → prompt

    Combined-before-cancel shows the *expanded* numerator students get by
    adding — never a construction-only factorization they could not derive.
    Construction must keep that expanded numerator hand-factorable (deg ≤ 2
    when RRT is off); dens may stay factored because the LCD rewrite exposes them.
    """
    opts = options or FactorablePolynomialOptions(coef_min=-8, coef_max=8)
    steps: list[dict[str, str]] = []
    final_latex = format_simplified_rational_latex(
        final_numerator,
        final_denominator,
        numerator_factors=final_numerator_factors,
        denominator_factors=final_denominator_factors,
        options=opts,
    )
    steps.append({"role": "final", "latex": final_latex})

    # Honest path: expanded combined numerator (no secret cancel-product display).
    combined_latex = format_simplified_rational_latex(
        combined_numerator,
        combined_denominator,
        numerator_factors=(),
        denominator_factors=lcd_factors if combined_denominator.deg() >= 1 else (),
        options=opts,
        force_numerator_factored=False,
        force_denominator_factored=_force_factored_answer_dens(lcd_factors, opts)
        if lcd_factors
        else False,
    )
    if cancelled_lcd_factors:
        steps.append({"role": "combined_before_cancel", "latex": combined_latex})
    elif combined_latex != final_latex:
        steps.append({"role": "combined", "latex": combined_latex})

    lcd_tex = _lcd_display_latex(lcd, lcd_factors)
    rewritten_parts: list[str] = []
    for term in display_terms:
        num_tex = _rewritten_numerator_latex(term, lcd, lcd_factors, opts)
        if num_tex is None:
            rewritten_parts = []
            break
        rewritten_parts.append(fraction_latex(num_tex, lcd_tex))
    prompt_latex = sum_of_fractions_latex(list(display_terms))
    if rewritten_parts:
        sum_over_lcd = " + ".join(rewritten_parts)
        # Skip when prompt is already the LCD rewrite (common shared-LCD cancel path).
        if sum_over_lcd != prompt_latex:
            steps.append({"role": "sum_over_lcd", "latex": sum_over_lcd})

    steps.append({"role": "prompt", "latex": prompt_latex})
    return steps


def format_simplified_rational_latex(
    numerator: Polynomial,
    denominator: Polynomial,
    *,
    numerator_factors: tuple[Polynomial, ...] = (),
    denominator_factors: tuple[Polynomial, ...] = (),
    options: FactorablePolynomialOptions | None = None,
    force_numerator_factored: bool = False,
    force_denominator_factored: bool | None = None,
) -> str:
    """Render a simplified answer using known factors when RRT policy says so."""
    opts = options or FactorablePolynomialOptions(coef_min=-8, coef_max=8)
    if force_denominator_factored is None:
        force_denominator_factored = _force_factored_answer_dens(
            denominator_factors, opts
        )

    if denominator is None or denominator.is_zero():
        if numerator_factors:
            return format_polynomial_from_factors(
                numerator_factors, opts, force_factored=force_numerator_factored
            )
        return numerator.to_latex()

    if denominator.deg() == 0:
        lead = float(denominator.coef(0))
        if abs(lead - 1.0) < 1e-10:
            if numerator_factors:
                return format_polynomial_from_factors(
                    numerator_factors, opts, force_factored=force_numerator_factored
                )
            return numerator.to_latex()
        if abs(lead + 1.0) < 1e-10:
            flipped = _integerize_polynomial(numerator * -1)
            if numerator_factors:
                flipped_factors = tuple(
                    _integerize_polynomial(f * -1) if i == 0 else f
                    for i, f in enumerate(numerator_factors)
                )
                return format_polynomial_from_factors(
                    flipped_factors, opts, force_factored=force_numerator_factored
                )
            return flipped.to_latex()

    if numerator_factors:
        num_latex = format_polynomial_from_factors(
            numerator_factors, opts, force_factored=force_numerator_factored
        )
    else:
        num_latex = numerator.to_latex()

    if denominator_factors:
        den_latex = format_polynomial_from_factors(
            denominator_factors, opts, force_factored=bool(force_denominator_factored)
        )
    else:
        den_latex = denominator.to_latex()
    return fraction_latex(num_latex, den_latex)


def _compose_expression_numerator(
    lcd: Polynomial,
    polynomial_term: Polynomial | None,
    partial_numerators: list[Polynomial],
    denominator_factors: list[Polynomial],
    full_lcd_numerator: Polynomial | None,
) -> Polynomial:
    total = Polynomial(((0, 0),))
    if polynomial_term is not None:
        total = total + polynomial_term * lcd
    total = total + _compose_partial_fraction_numerators(partial_numerators, denominator_factors)
    if full_lcd_numerator is not None:
        total = total + full_lcd_numerator
    return total


def build_rational_expression_problem(
    options: FactorablePolynomialOptions,
    term_count: int = 2,
    use_random_partial_solution: bool = True,
    allow_polynomial_terms: bool = True,
    allow_full_lcd_terms: bool = True,
    inflation_chance: float = 0.15,
    max_inflation_degree: int = 2,
    cancel_factor_count: int | str = "random",
    max_lcd_factors: int | None = None,
    prefer_simple_factors: bool = False,
    content_primitive: bool = True,
    allow_empty_denominators: bool | None = None,
    force_shared_lcd: bool = False,
    allow_monomial_lcd: bool = False,
) -> RationalExpressionSolution:
    # No pedagogical hard cap on term count — continuous D may request dozens.
    # End-cancel with RRT off: expanded combined num must stay ≤ quadratic
    # (constant core × ≤2 linear cancel factors). Matches
    # question_engine...HAND_FACTORABLE_END_CANCEL_MAX.
    term_count = max(2, int(term_count))
    coef_min, coef_max = options.normalized_coef_range()
    if allow_empty_denominators is None:
        allow_empty_denominators = allow_polynomial_terms

    _ALL_CANCEL = 10**9
    rrt_exclude = options.rrt_mode == "exclude"
    # Constant reduced core → at most 2 linear cancels without RRT.
    _hand_cancel_cap = 2 if rrt_exclude else _ALL_CANCEL

    for _ in range(200):
        include_polynomial = allow_polynomial_terms and random.random() < 0.6
        include_full_lcd = allow_full_lcd_terms and random.random() < 0.4

        reserved = int(include_polynomial) + int(include_full_lcd)
        factor_term_count = max(1, term_count - reserved)

        planned_cancel: int | None
        cancel_is_auto = cancel_factor_count is None or (
            isinstance(cancel_factor_count, str)
            and cancel_factor_count.strip().lower() in {"", "random", "auto"}
        )
        if cancel_is_auto:
            # Pick cancel intent first so LCD size can leave a simple remainder.
            default_max = max(2, options.target_degree_max)
            if max_lcd_factors is not None:
                default_max = max(1, min(default_max, max_lcd_factors))
            lo = max(1 if max_lcd_factors == 1 else 2, factor_term_count if max_lcd_factors is None else 1)
            if max_lcd_factors is not None:
                lo = min(lo, max_lcd_factors)
                hi = max(lo, max_lcd_factors)
            else:
                hi = max(lo, default_max)
            lcd_factor_count = random.randint(lo, hi)
            if max_lcd_factors is not None:
                lcd_factor_count = min(lcd_factor_count, max_lcd_factors)
            if random.random() < 0.35:
                planned_cancel = 0
            elif max_lcd_factors is not None and max_lcd_factors <= 2:
                planned_cancel = 0
            elif random.random() < 0.25:
                planned_cancel = lcd_factor_count  # all cancel
                if allow_polynomial_terms:
                    include_polynomial = True
            else:
                planned_cancel = random.randint(1, max(1, lcd_factor_count - 1))
                lcd_factor_count = min(max(hi, lcd_factor_count), planned_cancel + 1)
                if max_lcd_factors is not None:
                    lcd_factor_count = min(lcd_factor_count, max_lcd_factors)
            if planned_cancel and planned_cancel > 0:
                planned_cancel = min(planned_cancel, _hand_cancel_cap)
        else:
            planned_cancel = max(0, int(cancel_factor_count))
            if planned_cancel <= 0:
                lo = max(1 if max_lcd_factors == 1 else 2, factor_term_count if max_lcd_factors is None else 1)
                if max_lcd_factors is not None:
                    lo = min(lo, max_lcd_factors)
                    hi = max(lo, max_lcd_factors)
                else:
                    hi = max(lo, max(2, options.target_degree_max))
                lcd_factor_count = random.randint(lo, hi)
            elif planned_cancel >= _ALL_CANCEL:
                # "All available": size the LCD normally, then cancel every factor
                # present — do not inflate LCD to the cancel sentinel / continuous max.
                # With RRT off, still clamp to hand-factorable end-cancel.
                lo = max(1 if max_lcd_factors == 1 else 2, factor_term_count if max_lcd_factors is None else 1)
                if max_lcd_factors is not None:
                    lo = min(lo, max_lcd_factors)
                    hi = max(lo, max_lcd_factors)
                else:
                    hi = max(lo, max(2, options.target_degree_max))
                lcd_factor_count = random.randint(lo, hi)
                planned_cancel = min(lcd_factor_count, _hand_cancel_cap)
            elif max_lcd_factors is not None and planned_cancel >= max_lcd_factors:
                # Exact request ≥ capacity → cancel every available LCD factor.
                lcd_factor_count = max(1, max_lcd_factors)
                planned_cancel = min(planned_cancel, _hand_cancel_cap, lcd_factor_count)
            else:
                # Leave at least one remaining dens factor after cancel. When
                # capacity allows, prefer richer LCDs so students cancel after
                # combining over a multi-factor LCD (not cancel+1 only).
                planned_cancel = min(planned_cancel, _hand_cancel_cap)
                min_lcd = planned_cancel + 1
                if max_lcd_factors is not None:
                    lcd_factor_count = random.randint(
                        min_lcd, max(min_lcd, max_lcd_factors)
                    )
                else:
                    lcd_factor_count = min_lcd + random.randint(0, 2)
            if max_lcd_factors is not None:
                lcd_factor_count = max(1, min(lcd_factor_count, max_lcd_factors))
            if planned_cancel and 0 < planned_cancel < _ALL_CANCEL:
                planned_cancel = min(planned_cancel, _hand_cancel_cap)
        # Honest end-cancel: no poly/full-LCD extras that inflate combined deg.
        if rrt_exclude and planned_cancel and planned_cancel > 0:
            include_polynomial = False
            include_full_lcd = False
            reserved = 0
            factor_term_count = max(1, term_count)
        lcd_factors = _build_lcd_factors(
            options,
            lcd_factor_count,
            coef_min,
            coef_max,
            prefer_simple_factors=prefer_simple_factors or (max_lcd_factors is not None and max_lcd_factors <= 2),
            content_primitive=content_primitive,
            allow_monomial_factors=allow_monomial_lcd and lcd_factor_count == 1,
        )

        # Allow multi-factor dens even when RRT is excluded; display policy keeps
        # hard products factored via should_display_factor_product_expanded.
        max_subset_size = max_lcd_factors
        force_shared = force_shared_lcd or lcd_factor_count == 1
        term_denominator_factor_lists = _pick_term_denominators(
            lcd_factors,
            factor_term_count,
            max_subset_size=max_subset_size,
            allow_empty=allow_empty_denominators and not force_shared,
            force_shared_single=force_shared,
        )

        # Easy-style related dens: same linear, one term scaled by a small constant.
        # LCD remains a single binomial (e.g. x+1 and 2x+2 → LCD 2x+2).
        if (
            force_shared
            and lcd_factor_count == 1
            and factor_term_count == 2
            and lcd_factors[0].deg() == 1
            and abs(float(lcd_factors[0].coef(0))) >= 1e-10  # not a pure monomial
            and random.random() < 0.45
        ):
            base = lcd_factors[0]
            scale = random.choice([2, 3])
            # Keep the constant factor so the LCD stays a single binomial (e.g. 2x+2).
            scaled = _integerize_polynomial(base * scale)
            lcd_factors = [scaled]
            term_denominator_factor_lists = [(base,), (scaled,)]

        term_denominators = [
            _factors_to_polynomial(factors) for factors in term_denominator_factor_lists
        ]
        lcd = _product(lcd_factors)
        # Related dens (x+1 and 2x+2) need a Z[x] LCD, not Q[x] lcm.
        # Ignore empty/constant dens from polynomial terms — those must not
        # collapse the LCD away from the full factor product.
        fractional_dens = [
            den
            for den in term_denominators
            if den is not None and not den.is_zero() and den.deg() >= 1
        ]
        if len(fractional_dens) >= 2:
            true_lcd = _integer_coefficient_lcd(fractional_dens)
            if not true_lcd.is_zero() and true_lcd.deg() >= 1:
                divides_all = True
                for den in fractional_dens:
                    try:
                        _exact_divide(true_lcd, den)
                    except ValueError:
                        divides_all = False
                        break
                if divides_all:
                    lcd = true_lcd
                    # Keep lcd_factors aligned with the true LCD for final cancellation.
                    if len(lcd_factors) == 1 and lcd_factors[0].deg() == lcd.deg():
                        lcd_factors = [lcd]
        simplified_denominator = lcd

        if planned_cancel is None:
            target_cancel_count = _resolve_cancel_factor_count(
                cancel_factor_count,
                len(lcd_factors),
            )
            target_cancel_count = min(target_cancel_count, _hand_cancel_cap)
        elif planned_cancel <= 0:
            target_cancel_count = 0
        elif planned_cancel >= len(lcd_factors):
            target_cancel_count = min(len(lcd_factors), _hand_cancel_cap)
        else:
            target_cancel_count = min(planned_cancel, len(lcd_factors) - 1, _hand_cancel_cap)

        cancelled_lcd_factors = _pick_cancelled_lcd_factors(lcd_factors, target_cancel_count)

        polynomial_term = None
        full_lcd_numerator = None
        partial_numerators: list[Polynomial]
        term_denominator_factor_lists: list[tuple[Polynomial, ...]]
        term_denominators: list[Polynomial]
        final_numerator: Polynomial
        final_denominator: Polynomial
        final_numerator_factors: tuple[Polynomial, ...] = ()
        final_denominator_factors: tuple[Polynomial, ...] = ()
        term_numerator_factor_lists: list[tuple[Polynomial, ...]] = []

        if cancelled_lcd_factors:
            pieces = _build_cancelled_expression_pieces(
                options,
                lcd_factors,
                cancelled_lcd_factors,
                factor_term_count=factor_term_count,
                include_polynomial=include_polynomial,
                max_subset_size=max_subset_size,
            )
            if pieces is None:
                continue
            (
                polynomial_term,
                partial_numerators,
                term_denominator_factor_lists,
                simplified_numerator,
                final_numerator,
                final_denominator,
                final_numerator_factors,
                final_denominator_factors,
                term_numerator_factor_lists,
            ) = pieces
            term_denominators = [
                _factors_to_polynomial(factors) for factors in term_denominator_factor_lists
            ]
            # Cancelled construction rebuilds term dens from lcd_factors; keep LCD
            # aligned (related-den LCD rewrite above can otherwise desync).
            lcd = _product(lcd_factors)
            simplified_denominator = lcd
            try:
                fractional_numerator = _compose_over_term_denominators(
                    partial_numerators,
                    term_denominators,
                    lcd,
                )
            except ValueError:
                continue
        else:
            final_numerator_factors = ()
            final_denominator_factors = tuple(lcd_factors)
            term_numerator_factor_lists = [() for _ in range(factor_term_count)]
            if include_polynomial:
                polynomial_term = _random_polynomial_term(
                    coef_min,
                    coef_max,
                    max_degree=min(2, lcd.deg() - 1),
                    positive_leading=options.positive_leading,
                )

            if use_random_partial_solution:
                partial_numerators = [
                    _random_numerator_for_denominator(
                        term_denominator,
                        coef_min,
                        coef_max,
                        options.positive_leading,
                    )
                    for term_denominator in term_denominators
                ]
            else:
                seed_numerator = Polynomial.random_polynomial(
                    random.randint(1, max(1, lcd.deg() - 1)),
                    coef_min,
                    coef_max,
                    positive_leading=options.positive_leading,
                )
                partial_numerators, _, _, _ = _solve_partial_fractions_pfd(
                    seed_numerator,
                    lcd_factors,
                )
                partial_numerators = partial_numerators[:factor_term_count]
                term_denominator_factor_lists = [
                    (factor,) for factor in lcd_factors[:factor_term_count]
                ]
                term_denominators = [
                    _factors_to_polynomial(factors) for factors in term_denominator_factor_lists
                ]

            if include_full_lcd:
                full_lcd_numerator = _random_numerator_for_denominator(
                    lcd,
                    coef_min,
                    coef_max,
                    options.positive_leading,
                )

            fractional_numerator = _compose_over_term_denominators(
                partial_numerators,
                term_denominators,
                lcd,
            )
            simplified_numerator = fractional_numerator
            if polynomial_term is not None:
                simplified_numerator = simplified_numerator + polynomial_term * lcd
            if full_lcd_numerator is not None:
                simplified_numerator = simplified_numerator + full_lcd_numerator

            if simplified_numerator.is_zero():
                continue

            final_form = _final_form_after_cancellation(
                simplified_numerator,
                lcd_factors,
                cancelled_lcd_factors,
            )
            if final_form is None:
                continue
            final_numerator, final_denominator = final_form

        if simplified_denominator.is_zero():
            continue

        if simplified_numerator.is_zero():
            continue

        # Reject problems that collapsed away from the requested term count.
        expected_min_terms = factor_term_count + int(polynomial_term is not None) + int(
            full_lcd_numerator is not None
        )
        if expected_min_terms < term_count and not cancelled_lcd_factors:
            continue

        matrix_rows: list[list[float]] = []
        matrix_aug: list[float] = []
        matrix_solution: list[float] = []
        try:
            _, matrix_rows, matrix_aug, matrix_solution = _solve_partial_fractions_pfd(
                fractional_numerator,
                lcd_factors,
            )
        except Exception:
            pass

        inflation_factor = Polynomial([1])

        display_terms: list[RationalExpressionTerm] = []

        # Shuffle fractional slots so no fixed position absorbs extras.
        fractional_slots = list(
            zip(
                partial_numerators,
                term_denominators,
                term_denominator_factor_lists,
                (
                    term_numerator_factor_lists
                    + [() for _ in range(max(0, len(partial_numerators) - len(term_numerator_factor_lists)))]
                )[: len(partial_numerators)],
                strict=True,
            )
        )
        random.shuffle(fractional_slots)

        if polynomial_term is not None and random.random() < 0.5:
            display_terms.append(
                RationalExpressionTerm(
                    numerator=polynomial_term,
                    denominator=None,
                    term_kind="polynomial",
                )
            )
            polynomial_term_placed = True
        else:
            polynomial_term_placed = False

        for partial_num, term_denominator, term_factors, num_factors in fractional_slots:
            # When cancels are planned, keep per-term degree inflation rare so
            # cancellation happens after combining — not inside each term.
            # With RRT off, disable inflation entirely for honest end-cancel.
            effective_inflation = inflation_chance
            if cancelled_lcd_factors:
                effective_inflation = (
                    0.0 if rrt_exclude else min(inflation_chance, 0.05)
                )
            term_inflation = _maybe_pick_term_inflation(
                options,
                effective_inflation,
                max_inflation_degree,
            )
            if term_inflation.deg() > 0 and inflation_factor.deg() == 0:
                inflation_factor = term_inflation

            if term_denominator.deg() == 0:
                if not allow_empty_denominators:
                    continue
                if term_inflation.deg() > 0:
                    display_terms.append(
                        RationalExpressionTerm(
                            numerator=partial_num * term_inflation,
                            denominator=term_inflation,
                            denominator_factors=(term_inflation,),
                            term_kind="polynomial",
                        )
                    )
                else:
                    display_terms.append(
                        RationalExpressionTerm(
                            numerator=partial_num,
                            denominator=None,
                            term_kind="polynomial",
                        )
                    )
                continue

            display_terms.append(
                _build_fraction_display_term(
                    partial_num,
                    term_factors,
                    term_inflation,
                    options,
                    numerator_factors=num_factors or None,
                )
            )

        if polynomial_term is not None and not polynomial_term_placed:
            insert_at = random.randint(0, len(display_terms))
            display_terms.insert(
                insert_at,
                RationalExpressionTerm(
                    numerator=polynomial_term,
                    denominator=None,
                    term_kind="polynomial",
                ),
            )

        if full_lcd_numerator is not None:
            lcd_factor_tuple = tuple(lcd_factors)
            insert_at = random.randint(0, len(display_terms))
            display_terms.insert(
                insert_at,
                RationalExpressionTerm(
                    numerator=full_lcd_numerator,
                    denominator=lcd,
                    denominator_factors=lcd_factor_tuple,
                    denominator_display_expanded=_should_display_denominator_expanded(
                        lcd_factor_tuple,
                        options,
                    ),
                    term_kind="full_lcd",
                ),
            )

        if len(display_terms) < 2:
            continue
        if not allow_polynomial_terms and any(term.is_polynomial_term for term in display_terms):
            continue
        if max_lcd_factors is not None and max_lcd_factors <= 1 and lcd.deg() > 1:
            continue

        simplified_numerator, simplified_denominator = _scale_fraction_to_integers(
            simplified_numerator,
            simplified_denominator,
        )
        final_numerator, final_denominator = _scale_fraction_to_integers(
            final_numerator,
            final_denominator,
        )
        # Keep factor lists aligned with any content scaling of the final dens.
        if final_denominator_factors:
            scaled_den = _factors_to_polynomial(final_denominator_factors)
            if not _integerize_polynomial(scaled_den - final_denominator).is_zero():
                # Content scaling changed dens; drop stale factor metadata for dens
                # only when the product no longer matches (num factors usually fine).
                if abs(float(scaled_den.content_gcd() or 1)) > 1:
                    pass
                # If degrees match, keep factors; answer formatter uses them for shape.
                if scaled_den.deg() != final_denominator.deg():
                    final_denominator_factors = ()

        if final_numerator_factors:
            scaled_num = _factors_to_polynomial(final_numerator_factors)
            if scaled_num.deg() != final_numerator.deg():
                final_numerator_factors = ()
            elif (
                final_numerator.deg() == 0
                and final_numerator_factors
                and final_numerator_factors[0].deg() == 0
            ):
                final_numerator_factors = (final_numerator,)

        combined_numerator = simplified_numerator
        combined_denominator = simplified_denominator
        # Honest end-cancel: expanded combined num must be classroom-factorable.
        if (
            rrt_exclude
            and cancelled_lcd_factors
            and combined_numerator.deg() > 2
        ):
            continue
        lcd_factor_tuple = tuple(lcd_factors)
        display_term_tuple = tuple(display_terms)
        generation_steps = _record_rational_generation_steps(
            display_term_tuple,
            lcd,
            lcd_factor_tuple,
            combined_numerator,
            combined_denominator,
            cancelled_lcd_factors,
            final_numerator,
            final_denominator,
            final_numerator_factors=final_numerator_factors,
            final_denominator_factors=final_denominator_factors,
            options=options,
        )
        qa_flag_details = collect_nonclassroom_factor_step_details(
            display_term_tuple,
            combined_numerator=combined_numerator,
            cancelled_lcd_factors=cancelled_lcd_factors,
            final_numerator=final_numerator,
            final_numerator_factors=final_numerator_factors,
            options=options,
        )
        qa_flags = nonclassroom_factor_step_qa_flags(qa_flag_details)

        return RationalExpressionSolution(
            cancel_factor=Polynomial([1]),
            inflation_factor=inflation_factor,
            numerator_extension=simplified_numerator,
            denominator_extension=simplified_denominator,
            simplified_numerator=simplified_numerator,
            simplified_denominator=simplified_denominator,
            lcd=lcd,
            lcd_factors=lcd_factor_tuple,
            display_terms=display_term_tuple,
            partial_numerators=tuple(partial_numerators),
            polynomial_term=polynomial_term,
            full_lcd_numerator=full_lcd_numerator,
            combined_numerator=combined_numerator,
            combined_denominator=combined_denominator,
            cancelled_lcd_factors=cancelled_lcd_factors,
            final_numerator=final_numerator,
            final_denominator=final_denominator,
            final_numerator_factors=final_numerator_factors,
            final_denominator_factors=final_denominator_factors,
            matrix_rows=matrix_rows,
            matrix_aug_column=matrix_aug,
            matrix_solution=matrix_solution,
            generation_steps=generation_steps,
            qa_flags=qa_flags,
            qa_flag_details=qa_flag_details,
        )

    raise RuntimeError("Unable to build rational expression problem")


def sum_of_fractions_latex(terms: list[RationalExpressionTerm]) -> str:
    parts: list[str] = []
    for term in terms:
        if term.is_polynomial_term:
            parts.append(term.numerator.to_latex())
        elif term.denominator is not None and term.denominator.deg() == 0:
            parts.append(term.numerator.to_latex())
        else:
            assert term.denominator is not None
            parts.append(
                fraction_latex(
                    term_numerator_latex(term),
                    term_denominator_latex(term),
                )
            )
    return " + ".join(parts)


def term_denominator_text(term: RationalExpressionTerm) -> str:
    if term.denominator is None:
        return ""
    if term.denominator_factors and not term.denominator_display_expanded:
        if len(term.denominator_factors) == 1:
            return str(term.denominator_factors[0])
        return "".join(f"({factor})" for factor in term.denominator_factors)
    return str(term.denominator)


def term_prompt_text(term: RationalExpressionTerm) -> str:
    if term.is_polynomial_term:
        if term.numerator_factors and not term.numerator_display_expanded:
            if len(term.numerator_factors) == 1:
                return str(term.numerator_factors[0])
            return "".join(f"({factor})" for factor in term.numerator_factors)
        return str(term.numerator)
    assert term.denominator is not None
    num_text = (
        "".join(f"({factor})" for factor in term.numerator_factors)
        if term.numerator_factors and not term.numerator_display_expanded
        else str(term.numerator)
    )
    if term.numerator_factors and not term.numerator_display_expanded and len(term.numerator_factors) == 1:
        num_text = str(term.numerator_factors[0])
    return f"({num_text})/({term_denominator_text(term)})"
