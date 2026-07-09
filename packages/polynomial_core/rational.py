from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any, Literal

from .factoring import (
    FactorablePolynomialOptions,
    create_factorable_polynomial_with_exact_degree,
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
    term_kind: TermKind = "factor"

    @property
    def is_polynomial_term(self) -> bool:
        return self.denominator is None

    def to_latex(self) -> str:
        """LaTeX for this term (polynomial or fraction)."""
        if self.is_polynomial_term:
            return self.numerator.to_latex()
        assert self.denominator is not None
        if self.denominator.deg() == 0:
            return self.numerator.to_latex()
        return fraction_latex(self.numerator.to_latex(), term_denominator_latex(self))

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


def _ensure_denominator_factors(
    factors: list[Polynomial],
    term_count: int,
    coef_min: int,
    coef_max: int,
) -> list[Polynomial]:
    unique_factors = _unique_polynomials(factors)
    while len(unique_factors) < term_count:
        candidate = Polynomial([1, Polynomial.randomCoefficient(coef_min, coef_max, nonZero=True)])
        if not any(candidate == existing for existing in unique_factors):
            unique_factors.append(candidate)
    return unique_factors[:term_count]


def _product(factors: list[Polynomial]) -> Polynomial:
    result = Polynomial([1])
    for factor in factors:
        result *= factor
    return result


def _factors_to_polynomial(factors: tuple[Polynomial, ...] | list[Polynomial]) -> Polynomial:
    if not factors:
        return Polynomial([1])
    return _product(list(factors))


def _is_substitution_quadratic_pair(left: Polynomial, right: Polynomial) -> bool:
    for polynomial in (left, right):
        if polynomial.deg() != 2:
            return False
        if abs(float(polynomial.coef(1))) > 1e-10:
            return False
    return True


def _should_display_denominator_expanded(
    factors: tuple[Polynomial, ...],
    options: FactorablePolynomialOptions,
) -> bool:
    if len(factors) <= 1:
        return True

    enabled = set(options.enabled_method_pool())

    if all(factor.deg() == 1 for factor in factors):
        if len(factors) == 2:
            return True
        return options.rrt_mode == "only"

    if len(factors) == 2:
        degrees = sorted(factor.deg() for factor in factors)
        if degrees == [1, 2]:
            return "grouping" in enabled
        if degrees == [2, 2] and _is_substitution_quadratic_pair(factors[0], factors[1]):
            return "substitution" in enabled

    return False


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


def rational_excluded_values_latex(values: list[int]) -> str:
    """Format excluded values for display, e.g. ``x \\neq 2, -3``."""
    if not values:
        return ""
    parts = ", ".join(str(value) for value in sorted(values))
    return f"x \\neq {parts}"


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
    prods: list[Polynomial] = []
    for index in range(len(denominator_factors)):
        cofactor = Polynomial([1])
        for other_index, factor in enumerate(denominator_factors):
            if index != other_index:
                cofactor *= factor
        prods.append(cofactor)

    degree = (prods[0] * denominator_factors[0]).deg()
    coefs: list[list[float]] = []
    diffs: list[int] = []

    for cofactor in prods:
        term_coef = cofactor.coef_list(reverse=True)
        diff = degree - len(term_coef)
        diffs.append(diff)
        for shift in range(diff + 1):
            coefs.append(([0.0] * shift) + [float(value) for value in term_coef] + ([0.0] * (diff - shift)))

    numerator_coefs = numerator.coef_list(reverse=True) + (
        [0.0] * (degree - len(numerator.coef_list(reverse=True)))
    )
    coefs.append([float(value) for value in numerator_coefs])

    from sympy import Matrix

    matrix = Matrix(coefs).transpose()
    reduced = matrix.rref()[0]
    variable_count = sum(diff + 1 for diff in diffs)

    partial_numerators: list[Polynomial] = []
    cursor = 0
    for diff in diffs:
        terms = ((0, 0),)
        for exponent in range(diff + 1):
            terms += ((float(reduced[cursor + exponent, -1]), exponent),)
        partial_numerators.append(Polynomial(terms[1::]))
        cursor += diff + 1

    solution = [float(reduced[row, -1]) for row in range(variable_count)]
    return partial_numerators, [list(map(float, row)) for row in matrix.tolist()], [
        float(value) for value in numerator_coefs
    ], solution


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
) -> list[Polynomial]:
    max_factor_degree = (
        2
        if options.rrt_mode == "exclude"
        else min(3, max(2, options.target_degree_max))
    )

    for _ in range(200):
        lcd_factors: list[Polynomial] = []
        for _ in range(lcd_factor_count):
            factor = _pick_atomic_lcd_factor(options, max_factor_degree)
            if factor is None:
                break
            lcd_factors.append(factor)
        else:
            unique_factors = _unique_polynomials(lcd_factors)
            if len(unique_factors) >= min(2, lcd_factor_count):
                return _ensure_denominator_factors(
                    unique_factors,
                    lcd_factor_count,
                    coef_min,
                    coef_max,
                )

    return _ensure_denominator_factors(
        [],
        lcd_factor_count,
        coef_min,
        coef_max,
    )


def _pick_term_denominators(
    lcd_factors: list[Polynomial],
    term_count: int,
    max_subset_size: int | None = None,
) -> list[tuple[Polynomial, ...]]:
    factor_count = len(lcd_factors)
    max_size = factor_count if max_subset_size is None else min(max_subset_size, factor_count)
    denominators: list[tuple[Polynomial, ...]] = []

    for _ in range(term_count):
        subset_size = random.randint(0, max_size)
        if subset_size == 0:
            denominators.append(())
        else:
            indices = sorted(random.sample(range(factor_count), subset_size))
            denominators.append(tuple(lcd_factors[index] for index in indices))

    if not any(factors for factors in denominators):
        subset_size = random.randint(1, max_size)
        indices = sorted(random.sample(range(factor_count), subset_size))
        denominators[-1] = tuple(lcd_factors[index] for index in indices)

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
        else:
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
    if cancel_factor_count is None or cancel_factor_count == "random":
        return random.randint(0, lcd_factor_count)
    return max(0, min(int(cancel_factor_count), lcd_factor_count))


def _pick_cancelled_lcd_factors(
    lcd_factors: list[Polynomial],
    cancel_count: int,
) -> tuple[Polynomial, ...]:
    if cancel_count <= 0:
        return ()
    return tuple(random.sample(lcd_factors, cancel_count))


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

    remaining_factors = [
        factor for factor in lcd_factors if factor not in cancelled_lcd_factors
    ]
    final_denominator = (
        _factors_to_polynomial(remaining_factors) if remaining_factors else Polynomial([1])
    )
    return final_numerator, final_denominator


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
) -> RationalExpressionTerm:
    base_denominator = _factors_to_polynomial(denominator_factors)
    display_factors = denominator_factors
    display_expanded = _should_display_denominator_expanded(denominator_factors, options)
    if term_inflation.deg() > 0:
        display_factors = denominator_factors + (term_inflation,)
        return RationalExpressionTerm(
            numerator=numerator * term_inflation,
            denominator=base_denominator * term_inflation,
            denominator_factors=display_factors,
            denominator_display_expanded=display_expanded,
            term_kind="factor",
        )
    return RationalExpressionTerm(
        numerator=numerator,
        denominator=base_denominator,
        denominator_factors=display_factors,
        denominator_display_expanded=display_expanded,
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
) -> RationalExpressionSolution:
    term_count = max(2, min(5, term_count))
    coef_min, coef_max = options.normalized_coef_range()

    for _ in range(200):
        include_polynomial = allow_polynomial_terms and random.random() < 0.6
        include_full_lcd = allow_full_lcd_terms and random.random() < 0.4

        reserved = int(include_polynomial) + int(include_full_lcd)
        factor_term_count = max(1, term_count - reserved)

        lcd_factor_count = random.randint(max(2, factor_term_count), min(4, max(2, options.target_degree_max)))
        lcd_factors = _build_lcd_factors(
            options,
            lcd_factor_count,
            coef_min,
            coef_max,
        )

        max_subset_size = 1 if options.rrt_mode == "exclude" else None
        term_denominator_factor_lists = _pick_term_denominators(
            lcd_factors,
            factor_term_count,
            max_subset_size=max_subset_size,
        )
        term_denominators = [
            _factors_to_polynomial(factors) for factors in term_denominator_factor_lists
        ]
        lcd = _product(lcd_factors)
        simplified_denominator = lcd

        target_cancel_count = _resolve_cancel_factor_count(
            cancel_factor_count,
            len(lcd_factors),
        )
        cancelled_lcd_factors = _pick_cancelled_lcd_factors(lcd_factors, target_cancel_count)
        cancel_product = _factors_to_polynomial(cancelled_lcd_factors)

        polynomial_term = None
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
            if cancel_product.deg() > 0:
                partial_numerators = [
                    partial_num * cancel_product for partial_num in partial_numerators
                ]
        else:
            seed_numerator = Polynomial.random_polynomial(
                random.randint(1, max(1, lcd.deg() - 1)),
                coef_min,
                coef_max,
                positive_leading=options.positive_leading,
            )
            partial_numerators, _, _, _ = _solve_partial_fractions_pfd(seed_numerator, lcd_factors)
            partial_numerators = partial_numerators[:factor_term_count]
            if cancel_product.deg() > 0:
                partial_numerators = [
                    partial_num * cancel_product for partial_num in partial_numerators
                ]
            term_denominator_factor_lists = [(factor,) for factor in lcd_factors[:factor_term_count]]
            term_denominators = [
                _factors_to_polynomial(factors) for factors in term_denominator_factor_lists
            ]

        full_lcd_numerator = None
        if include_full_lcd:
            full_lcd_numerator = _random_numerator_for_denominator(
                lcd,
                coef_min,
                coef_max,
                options.positive_leading,
            )
            if cancel_product.deg() > 0:
                full_lcd_numerator = full_lcd_numerator * cancel_product

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

        if simplified_denominator.is_zero():
            continue

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

        if polynomial_term is not None:
            display_terms.append(
                RationalExpressionTerm(
                    numerator=polynomial_term,
                    denominator=None,
                    term_kind="polynomial",
                )
            )

        for partial_num, term_denominator, term_factors in zip(
            partial_numerators,
            term_denominators,
            term_denominator_factor_lists,
            strict=True,
        ):
            term_inflation = _maybe_pick_term_inflation(
                options,
                inflation_chance,
                max_inflation_degree,
            )
            if term_inflation.deg() > 0 and inflation_factor.deg() == 0:
                inflation_factor = term_inflation

            if term_denominator.deg() == 0:
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
                _build_fraction_display_term(partial_num, term_factors, term_inflation, options)
            )

        if full_lcd_numerator is not None:
            lcd_factor_tuple = tuple(lcd_factors)
            display_terms.append(
                RationalExpressionTerm(
                    numerator=full_lcd_numerator,
                    denominator=lcd,
                    denominator_factors=lcd_factor_tuple,
                    denominator_display_expanded=_should_display_denominator_expanded(
                        lcd_factor_tuple,
                        options,
                    ),
                    term_kind="full_lcd",
                )
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
                    term.numerator.to_latex(),
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
        return str(term.numerator)
    assert term.denominator is not None
    return f"({term.numerator})/({term_denominator_text(term)})"
