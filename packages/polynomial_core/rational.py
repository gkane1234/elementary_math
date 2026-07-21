from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any, Literal

from .factoring import (
    FactorablePolynomialOptions,
    create_factorable_polynomial_with_exact_degree,
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
    matrix_rows: list[list[float]] = field(default_factory=list)
    matrix_aug_column: list[float] = field(default_factory=list)
    matrix_solution: list[float] = field(default_factory=list)

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
            "final_numerator_latex": (
                self.final_numerator.to_latex() if self.final_numerator is not None else None
            ),
            "final_denominator_latex": (
                self.final_denominator.to_latex() if self.final_denominator is not None else None
            ),
            "matrix_rows": self.matrix_rows,
            "matrix_aug_column": self.matrix_aug_column,
            "matrix_solution": self.matrix_solution,
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
] | None:
    """Build a cancellable expression from the reduced answer outward.

    Start from a nice reduced answer, split it into several simple terms, then
    distribute each cancel factor onto some of those terms as balanced
    inflation. That keeps numerators small and avoids dumping the whole cancel
    product onto one residual term.
    """
    del max_subset_size  # inflated cancel terms may use remaining+cancel factors
    coef_min, coef_max = options.normalized_coef_range()
    lcd = _product(lcd_factors)
    cancel_product = _factors_to_polynomial(cancelled_lcd_factors)
    remaining_factors = _remaining_lcd_factors(lcd_factors, cancelled_lcd_factors)

    polynomial_term = None
    if include_polynomial:
        polynomial_term = _random_polynomial_term(
            coef_min,
            coef_max,
            max_degree=min(2, max(0, lcd.deg() - 1)),
            positive_leading=options.positive_leading,
        )

    # All-cancel (no remaining LCD factors) must still emit ≥2 fractional terms
    # so the outer builder does not reject/retry forever. Build from a constant
    # reduced answer and distribute cancel factors across terms (same path as
    # partial cancel). Optional polynomial term is additive only.
    # Constant reduced numerators keep post-inflation terms small and readable.
    # Choose a magnitude large enough to split across the cancel-factor terms.
    min_abs = max(2, len(cancelled_lcd_factors) + 1)
    final_value = int(Polynomial.randomCoefficient(coef_min, coef_max, nonZero=True))
    if abs(final_value) < min_abs:
        sign = 1 if final_value > 0 else -1
        final_value = sign * min_abs
    final_core = Polynomial([final_value])
    # Enough terms that each cancel factor can land on a distinct fraction,
    # with at least one uninflated term left when possible.
    desired = max(factor_term_count, len(cancelled_lcd_factors) + 1, 2)
    pieces = _split_polynomial_into_summands(final_core, desired, coef_min, coef_max)
    base_factor_tuple = tuple(remaining_factors)
    expanded_entries = [
        (piece, base_factor_tuple)
        for piece in pieces
        if not piece.is_zero()
    ]
    if not expanded_entries:
        expanded_entries = [(final_core, base_factor_tuple)]

    while len(expanded_entries) < len(cancelled_lcd_factors) + 1:
        index = random.randrange(len(expanded_entries))
        numerator, factors = expanded_entries.pop(index)
        before = len(expanded_entries)
        split_pieces = _split_polynomial_into_summands(numerator, 2, coef_min, coef_max)
        for piece in split_pieces:
            if not piece.is_zero():
                expanded_entries.append((piece, factors))
        if len(expanded_entries) <= before:
            # Could not actually split (e.g. numerator ±1). Put it back and stop.
            expanded_entries.append((numerator, factors))
            break

    random.shuffle(expanded_entries)
    mutable_entries: list[tuple[Polynomial, list[Polynomial]]] = [
        (numerator, list(factors)) for numerator, factors in expanded_entries
    ]

    # Assign each cancel factor only to currently uninflated terms so numerators
    # stay linear (constant × one binomial), never the full cancel product.
    for cancel_factor in cancelled_lcd_factors:
        if not mutable_entries:
            break
        unused = [
            index
            for index, (_, factors) in enumerate(mutable_entries)
            if len(factors) <= len(base_factor_tuple)
        ]
        if not unused:
            # Make room by splitting an uninflated term. If none remain, reject
            # this attempt rather than stack cancel factors or add inconsistent terms.
            uninflated = [
                index
                for index, (_, factors) in enumerate(mutable_entries)
                if len(factors) <= len(base_factor_tuple)
            ]
            if not uninflated:
                return None
            index = uninflated[random.randrange(len(uninflated))]
            numerator, factors = mutable_entries.pop(index)
            split_pieces = _split_polynomial_into_summands(numerator, 2, coef_min, coef_max)
            for piece in split_pieces:
                if not piece.is_zero():
                    mutable_entries.append((piece, list(factors)))
            unused = [
                idx
                for idx, (_, entry_factors) in enumerate(mutable_entries)
                if len(entry_factors) <= len(base_factor_tuple)
            ]
            if not unused:
                return None

        if len(unused) == 1:
            targets = unused
        else:
            target_count = random.randint(1, len(unused) - 1)
            targets = random.sample(unused, target_count)

        next_entries: list[tuple[Polynomial, list[Polynomial]]] = []
        for index, (numerator, factors) in enumerate(mutable_entries):
            if index in targets:
                next_entries.append((numerator * cancel_factor, factors + [cancel_factor]))
            else:
                next_entries.append((numerator, factors))
        mutable_entries = next_entries

    packaged = [(num, tuple(factors)) for num, factors in mutable_entries if not num.is_zero()]
    random.shuffle(packaged)
    packaged_numerators = [numerator for numerator, _ in packaged]
    packaged_factor_lists = [factors for _, factors in packaged]

    if not packaged_numerators and polynomial_term is None:
        return None

    simplified_numerator = final_core * cancel_product
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

    return (
        polynomial_term,
        packaged_numerators,
        packaged_factor_lists,
        simplified_numerator,
        final_numerator,
        final_denominator,
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
    display_expanded = (
        False
        if force_factored
        else _should_display_denominator_expanded(denominator_factors, options)
    )
    num_factors = numerator_factors or ()
    if term_inflation.deg() > 0:
        display_factors = denominator_factors + (term_inflation,)
        inflated_num_factors = (
            (num_factors + (term_inflation,)) if num_factors else ()
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
            denominator_display_expanded=display_expanded and not force_factored,
            numerator_factors=inflated_num_factors,
            numerator_display_expanded=num_expanded,
            term_kind="factor",
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
    # No pedagogical hard cap — continuous D may request dozens/hundreds of terms.
    term_count = max(2, int(term_count))
    coef_min, coef_max = options.normalized_coef_range()
    if allow_empty_denominators is None:
        allow_empty_denominators = allow_polynomial_terms

    _ALL_CANCEL = 10**9

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
                lo = max(1 if max_lcd_factors == 1 else 2, factor_term_count if max_lcd_factors is None else 1)
                if max_lcd_factors is not None:
                    lo = min(lo, max_lcd_factors)
                    hi = max(lo, max_lcd_factors)
                else:
                    hi = max(lo, max(2, options.target_degree_max))
                lcd_factor_count = random.randint(lo, hi)
            elif max_lcd_factors is not None and planned_cancel >= max_lcd_factors:
                # Exact request ≥ capacity → cancel every available LCD factor.
                lcd_factor_count = max(1, max_lcd_factors)
            else:
                # Leave a single remaining factor so dens stay simple after distribution.
                lcd_factor_count = planned_cancel + 1
            if max_lcd_factors is not None:
                lcd_factor_count = max(1, min(lcd_factor_count, max_lcd_factors))

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
        elif planned_cancel <= 0:
            target_cancel_count = 0
        elif planned_cancel >= len(lcd_factors):
            target_cancel_count = len(lcd_factors)
        else:
            target_cancel_count = min(planned_cancel, len(lcd_factors) - 1)

        cancelled_lcd_factors = _pick_cancelled_lcd_factors(lcd_factors, target_cancel_count)

        polynomial_term = None
        full_lcd_numerator = None
        partial_numerators: list[Polynomial]
        term_denominator_factor_lists: list[tuple[Polynomial, ...]]
        term_denominators: list[Polynomial]
        final_numerator: Polynomial
        final_denominator: Polynomial

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
            zip(partial_numerators, term_denominators, term_denominator_factor_lists, strict=True)
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

        for partial_num, term_denominator, term_factors in fractional_slots:
            term_inflation = _maybe_pick_term_inflation(
                options,
                inflation_chance,
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

        combined_numerator = simplified_numerator
        combined_denominator = simplified_denominator

        return RationalExpressionSolution(
            cancel_factor=Polynomial([1]),
            inflation_factor=inflation_factor,
            numerator_extension=simplified_numerator,
            denominator_extension=simplified_denominator,
            simplified_numerator=simplified_numerator,
            simplified_denominator=simplified_denominator,
            lcd=lcd,
            lcd_factors=tuple(lcd_factors),
            display_terms=tuple(display_terms),
            partial_numerators=tuple(partial_numerators),
            polynomial_term=polynomial_term,
            full_lcd_numerator=full_lcd_numerator,
            combined_numerator=combined_numerator,
            combined_denominator=combined_denominator,
            cancelled_lcd_factors=cancelled_lcd_factors,
            final_numerator=final_numerator,
            final_denominator=final_denominator,
            matrix_rows=matrix_rows,
            matrix_aug_column=matrix_aug,
            matrix_solution=matrix_solution,
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
