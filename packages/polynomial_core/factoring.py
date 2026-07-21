from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Literal

from .polynomial import Polynomial

FactorMethod = Literal[
    "normal",
    "grouping",
    "substitution",
    "difference_of_squares",
    "perfect_square_trinomial",
    "difference_of_cubes",
    "sum_of_cubes",
    "rrt",
]

RrtMode = Literal["exclude", "allow", "only"]

METHOD_DEGREE_RANGE: dict[FactorMethod, tuple[int, int]] = {
    "difference_of_squares": (2, 2),
    "perfect_square_trinomial": (2, 2),
    "difference_of_cubes": (3, 3),
    "sum_of_cubes": (3, 3),
    "grouping": (3, 3),
    "substitution": (4, 4),
    "normal": (2, 8),
    "rrt": (2, 8),
}


@dataclass(frozen=True)
class FactorablePolynomialResult:
    polynomial: Polynomial
    factors: tuple[Polynomial, ...]
    method: FactorMethod


@dataclass(frozen=True)
class FactorablePolynomialOptions:
    coef_min: int
    coef_max: int
    leading_coefficient_one: bool = False
    positive_leading: bool = True
    # Default exclude: do not require Rational Root Theorem unless opted in.
    rrt_mode: RrtMode = "exclude"
    enabled_methods: dict[FactorMethod, bool] | None = None
    target_degree_min: int = 2
    target_degree_max: int = 4

    def normalized_coef_range(self) -> tuple[int, int]:
        if self.coef_min <= self.coef_max:
            return self.coef_min, self.coef_max
        return self.coef_max, self.coef_min

    def enabled_method_pool(self) -> list[FactorMethod]:
        defaults: dict[FactorMethod, bool] = {
            "normal": True,
            "grouping": True,
            "substitution": True,
            "difference_of_squares": True,
            "perfect_square_trinomial": True,
            "difference_of_cubes": True,
            "sum_of_cubes": True,
            "rrt": False,
        }
        enabled = {**defaults, **(self.enabled_methods or {})}
        rrt_enabled = enabled.get("rrt", False)

        if self.rrt_mode == "only":
            return ["rrt"] if rrt_enabled else []

        pool: list[FactorMethod] = []
        for method, is_enabled in enabled.items():
            if not is_enabled:
                continue
            if self.rrt_mode == "exclude" and method == "rrt":
                continue
            pool.append(method)
        return pool


def _random_nonzero(coef_min: int, coef_max: int) -> int:
    value = Polynomial.randomCoefficient(coef_min, coef_max, nonZero=True)
    while value == 0:
        value = Polynomial.randomCoefficient(coef_min, coef_max, nonZero=True)
    return int(value)


def _leading_coefficient(options: FactorablePolynomialOptions) -> int:
    coef_min, coef_max = options.normalized_coef_range()
    if options.leading_coefficient_one:
        return 1
    # Prefer small a ≠ 1 so expanded special-case polynomials stay readable.
    bound = max(2, min(4, abs(coef_min), abs(coef_max) or 4))
    for _ in range(24):
        value = _random_nonzero(-bound, bound)
        if abs(value) == 1:
            continue
        if options.positive_leading and value < 0:
            value *= -1
        return value
    return 2 if options.positive_leading else -2


def _method_fits_degree(method: FactorMethod, degree_min: int, degree_max: int) -> bool:
    if method == "normal":
        return degree_min <= 8 and degree_max >= 0
    method_min, method_max = METHOD_DEGREE_RANGE[method]
    return method_min <= degree_max and method_max >= degree_min


def _normal_requires_rrt(degree: int) -> bool:
    """Products of 3+ linear factors generally need RRT to factor when expanded."""
    return degree >= 3


def _method_allowed_without_rrt(method: FactorMethod, degree: int) -> bool:
    if method != "normal":
        return True
    return not _normal_requires_rrt(degree)


def _is_substitution_quadratic_pair(left: Polynomial, right: Polynomial) -> bool:
    for polynomial in (left, right):
        if polynomial.deg() != 2:
            return False
        if abs(float(polynomial.coef(1))) > 1e-10:
            return False
    return True


def should_display_factor_product_expanded(
    factors: tuple[Polynomial, ...] | list[Polynomial],
    options: FactorablePolynomialOptions | None = None,
) -> bool:
    """Whether to show an expanded product vs keeping the factor product.

    Expand when the product is factorable by normal classroom methods (two
    linears, GCF, grouping, difference of squares, quadratic-form substitution,
    …). Keep **factored** when the expanded poly would require RRT (e.g. dense
    cubic/quartic from 3+ distinct linear factors), unless RRT is enabled.
    """
    factor_list = tuple(factors)
    if len(factor_list) <= 1:
        return True

    opts = options or FactorablePolynomialOptions(coef_min=-8, coef_max=8)
    enabled = set(opts.enabled_method_pool())

    # Leading constants don't change the factoring technique for the variable part.
    variable_factors = tuple(f for f in factor_list if f.deg() >= 1)
    if len(variable_factors) <= 1:
        return True

    if all(factor.deg() == 1 for factor in variable_factors):
        if len(variable_factors) == 2:
            return True
        # 3+ linear factors → expanded form needs RRT; keep factored unless RRT on.
        return opts.rrt_mode != "exclude"

    if len(variable_factors) == 2:
        degrees = sorted(factor.deg() for factor in variable_factors)
        if degrees == [1, 2]:
            return "grouping" in enabled
        if degrees == [2, 2] and _is_substitution_quadratic_pair(
            variable_factors[0], variable_factors[1]
        ):
            return "substitution" in enabled

    return False


def format_polynomial_from_factors(
    factors: tuple[Polynomial, ...] | list[Polynomial],
    options: FactorablePolynomialOptions | None = None,
    *,
    force_factored: bool = False,
    force_expanded: bool = False,
) -> str:
    """Render a factor product as expanded or factored latex based on pedagogy."""
    from .latex import format_factor_product_latex

    factor_list = tuple(factors)
    if not factor_list:
        return "0"
    if force_expanded or (
        not force_factored and should_display_factor_product_expanded(factor_list, options)
    ):
        product = factor_list[0]
        for other in factor_list[1:]:
            product = product * other
        return product.to_latex()
    return format_factor_product_latex(factor_list)


def _filter_methods_for_rrt_mode(
    methods: list[FactorMethod],
    options: FactorablePolynomialOptions,
    degree: int,
) -> list[FactorMethod]:
    if options.rrt_mode != "exclude":
        return methods
    return [method for method in methods if _method_allowed_without_rrt(method, degree)]


def _pick_method(options: FactorablePolynomialOptions) -> FactorMethod | None:
    if options.target_degree_min == options.target_degree_max == 0:
        return "normal"

    pool = [
        method
        for method in options.enabled_method_pool()
        if _method_fits_degree(method, options.target_degree_min, options.target_degree_max)
    ]
    if not pool:
        return None

    if options.target_degree_min == options.target_degree_max:
        exact_methods = _methods_for_exact_degree(
            options.target_degree_min,
            pool,
            options,
        )
        if exact_methods:
            pool = exact_methods
    elif options.rrt_mode == "exclude":
        pool = [
            method
            for method in pool
            if any(
                _method_allowed_without_rrt(method, degree)
                for degree in range(options.target_degree_min, options.target_degree_max + 1)
            )
        ]

    if options.rrt_mode == "exclude":
        pool = _filter_methods_for_rrt_mode(
            pool,
            options,
            options.target_degree_max,
        )

    if not pool:
        return None

    return random.choice(pool)


def _generate_difference_of_squares(options: FactorablePolynomialOptions) -> FactorablePolynomialResult:
    coef_min, coef_max = options.normalized_coef_range()
    leading = _leading_coefficient(options)
    constant = _random_nonzero(coef_min, coef_max)
    factor_a = Polynomial([leading, constant])
    factor_b = Polynomial([leading, -constant])
    polynomial = factor_a * factor_b
    return FactorablePolynomialResult(polynomial, (factor_a, factor_b), "difference_of_squares")


def _generate_perfect_square_trinomial(
    options: FactorablePolynomialOptions,
) -> FactorablePolynomialResult:
    coef_min, coef_max = options.normalized_coef_range()
    leading = _leading_coefficient(options)
    constant = _random_nonzero(coef_min, coef_max)
    factor = Polynomial([leading, constant])
    polynomial = factor * factor
    return FactorablePolynomialResult(polynomial, (factor, factor), "perfect_square_trinomial")


def _generate_difference_of_cubes(options: FactorablePolynomialOptions) -> FactorablePolynomialResult:
    coef_min, coef_max = options.normalized_coef_range()
    leading = _leading_coefficient(options)
    constant = _random_nonzero(coef_min, coef_max)
    factor_a = Polynomial([leading, -constant])
    factor_b = Polynomial([leading * leading, leading * constant, constant * constant])
    polynomial = factor_a * factor_b
    return FactorablePolynomialResult(polynomial, (factor_a, factor_b), "difference_of_cubes")


def _generate_sum_of_cubes(options: FactorablePolynomialOptions) -> FactorablePolynomialResult:
    coef_min, coef_max = options.normalized_coef_range()
    leading = _leading_coefficient(options)
    constant = _random_nonzero(coef_min, coef_max)
    factor_a = Polynomial([leading, constant])
    factor_b = Polynomial([leading * leading, -leading * constant, constant * constant])
    polynomial = factor_a * factor_b
    return FactorablePolynomialResult(polynomial, (factor_a, factor_b), "sum_of_cubes")


def _generate_grouping(options: FactorablePolynomialOptions) -> FactorablePolynomialResult:
    """Four-term cubic that factors by grouping: (a x^2 + b)(x + r).

    When ``leading_coefficient_one`` is False, leading ``a`` is chosen ≠ 1 so
    medium/hard monic_only=False presets actually produce non-monic cubics.
    """
    coef_min, coef_max = options.normalized_coef_range()
    leading = _leading_coefficient(options)
    root = _random_nonzero(coef_min, coef_max)
    # Keep the constant factor readable relative to coefficient width.
    quad_const_bound = max(1, min(abs(coef_max), abs(coef_min) or abs(coef_max), 8))
    quadratic_constant = _random_nonzero(-quad_const_bound, quad_const_bound)
    linear = Polynomial([1, root])
    quadratic = Polynomial([leading, 0, quadratic_constant])
    polynomial = linear * quadratic
    return FactorablePolynomialResult(polynomial, (linear, quadratic), "grouping")


def _generate_substitution(options: FactorablePolynomialOptions) -> FactorablePolynomialResult:
    coef_min, coef_max = options.normalized_coef_range()
    first = _random_nonzero(coef_min, coef_max)
    second = _random_nonzero(coef_min, coef_max)
    factor_a = Polynomial([1, 0, first])
    factor_b = Polynomial([1, 0, second])
    polynomial = factor_a * factor_b
    return FactorablePolynomialResult(polynomial, (factor_a, factor_b), "substitution")


def _methods_for_exact_degree(
    degree: int,
    enabled_pool: list[FactorMethod],
    options: FactorablePolynomialOptions | None = None,
) -> list[FactorMethod]:
    if degree <= 0:
        return []

    methods: list[FactorMethod] = []
    for method in enabled_pool:
        method_min, method_max = METHOD_DEGREE_RANGE[method]
        if method in ("normal", "rrt"):
            if options is not None and not _method_allowed_without_rrt(method, degree):
                continue
            methods.append(method)
        elif method_min == method_max == degree:
            methods.append(method)
    return methods


def _generate_linear_polynomial(options: FactorablePolynomialOptions) -> FactorablePolynomialResult:
    coef_min, coef_max = options.normalized_coef_range()
    leading = _leading_coefficient(options)
    constant = _random_nonzero(coef_min, coef_max)
    factor = Polynomial([leading, constant])
    return FactorablePolynomialResult(factor, (factor,), "normal")


def _generate_constant_polynomial() -> FactorablePolynomialResult:
    constant = Polynomial([1])
    return FactorablePolynomialResult(constant, (constant,), "normal")


def _generate_normal(options: FactorablePolynomialOptions) -> FactorablePolynomialResult:
    coef_min, coef_max = options.normalized_coef_range()
    exact_degree = (
        options.target_degree_min
        if options.target_degree_min == options.target_degree_max
        else None
    )

    if exact_degree == 0:
        return _generate_constant_polynomial()
    if exact_degree == 1:
        return _generate_linear_polynomial(options)

    if exact_degree is not None:
        factor_count = exact_degree
    else:
        degree_min = max(2, options.target_degree_min)
        degree_max = max(degree_min, options.target_degree_max)
        factor_count = random.randint(2, min(4, degree_max))

    # Always build monic linear factors; scale one factor when non-monic is required.
    leading_range = (1, 1)

    degree_min = max(0, options.target_degree_min)
    degree_max = max(degree_min, options.target_degree_max)

    def _scale_non_monic(
        polynomial: Polynomial, factors: list[Polynomial]
    ) -> tuple[Polynomial, list[Polynomial]]:
        if options.leading_coefficient_one:
            return polynomial, factors
        scale_hi = max(2, min(6, abs(coef_max), abs(coef_min) or 6))
        scale = random.randint(2, scale_hi)
        if not options.positive_leading and random.random() < 0.5:
            scale = -scale
        scaled_factors = list(factors)
        first = scaled_factors[0]
        # Polynomial list ctor expects high-degree-first coefficients.
        first_coeffs = [int(c) * scale for c in first.coef_list()]
        scaled_factors[0] = Polynomial(first_coeffs)
        scaled_poly = scaled_factors[0]
        for other in scaled_factors[1:]:
            scaled_poly = scaled_poly * other
        return scaled_poly, scaled_factors

    for _ in range(50):
        polynomial, factors = Polynomial.createPolynomialWithIntegerFactorsRanges(
            leading_range,
            (coef_min, coef_max),
            factor_count,
            returnFactors=True,
            positiveLeadingCoefficient=options.positive_leading,
        )
        factors_list = list(factors)
        polynomial, factors_list = _scale_non_monic(polynomial, factors_list)
        if exact_degree is not None:
            if polynomial.deg() == exact_degree:
                return FactorablePolynomialResult(polynomial, tuple(factors_list), "normal")
        elif degree_min <= polynomial.deg() <= degree_max:
            return FactorablePolynomialResult(polynomial, tuple(factors_list), "normal")

    polynomial, factors = Polynomial.createPolynomialWithIntegerFactorsRanges(
        leading_range,
        (coef_min, coef_max),
        max(1, factor_count),
        returnFactors=True,
        positiveLeadingCoefficient=options.positive_leading,
    )
    factors_list = list(factors)
    polynomial, factors_list = _scale_non_monic(polynomial, factors_list)
    return FactorablePolynomialResult(polynomial, tuple(factors_list), "normal")


def _generate_rrt(options: FactorablePolynomialOptions) -> FactorablePolynomialResult:
    coef_min, coef_max = options.normalized_coef_range()
    exact_degree = (
        options.target_degree_min
        if options.target_degree_min == options.target_degree_max
        else None
    )
    degree_min = max(2, options.target_degree_min)
    degree_max = max(degree_min, options.target_degree_max)
    terms = exact_degree if exact_degree is not None else random.randint(degree_min, min(degree_max, 4))
    non_one_terms = 0 if options.leading_coefficient_one else random.randint(0, min(2, terms - 1))
    polynomial = Polynomial.rrt(
        coef_min,
        coef_max,
        terms=terms,
        nonOneTerms=non_one_terms,
        maximumCoefficient=max(abs(coef_min), abs(coef_max)) * 4,
    )
    factors = tuple(Polynomial([1, -root]) for root in _integer_roots(polynomial, coef_min, coef_max))
    if not factors:
        factors = (polynomial,)
    return FactorablePolynomialResult(polynomial, factors, "rrt")


def _integer_roots(polynomial: Polynomial, coef_min: int, coef_max: int) -> list[int]:
    roots: list[int] = []
    for candidate in range(coef_min, coef_max + 1):
        if candidate == 0:
            continue
        if abs(float(polynomial @ candidate)) < 1e-8:
            roots.append(candidate)
    return roots


def _generate_by_method(method: FactorMethod, options: FactorablePolynomialOptions) -> FactorablePolynomialResult:
    generators = {
        "difference_of_squares": _generate_difference_of_squares,
        "perfect_square_trinomial": _generate_perfect_square_trinomial,
        "difference_of_cubes": _generate_difference_of_cubes,
        "sum_of_cubes": _generate_sum_of_cubes,
        "grouping": _generate_grouping,
        "substitution": _generate_substitution,
        "normal": _generate_normal,
        "rrt": _generate_rrt,
    }
    return generators[method](options)


def create_factorable_polynomial(
    options: FactorablePolynomialOptions,
    max_attempts: int = 200,
) -> FactorablePolynomialResult:
    if options.target_degree_min == options.target_degree_max == 0:
        return _generate_constant_polynomial()

    for _ in range(max_attempts):
        method = _pick_method(options)
        if method is None:
            break
        result = _generate_by_method(method, options)
        if options.rrt_mode == "exclude" and result.method == "normal":
            if _normal_requires_rrt(result.polynomial.deg()):
                continue
        if options.target_degree_min <= result.polynomial.deg() <= options.target_degree_max:
            if (
                options.target_degree_min != options.target_degree_max
                or result.polynomial.deg() == options.target_degree_min
            ):
                return result

    fallback_methods: dict[FactorMethod, bool] = {"normal": True}
    if options.rrt_mode == "exclude":
        fallback_methods = {
            "normal": options.target_degree_max < 3,
            "grouping": True,
            "substitution": options.target_degree_max >= 4,
            "difference_of_squares": options.target_degree_max >= 2,
            "perfect_square_trinomial": options.target_degree_max >= 2,
            "difference_of_cubes": options.target_degree_max >= 3,
            "sum_of_cubes": options.target_degree_max >= 3,
        }

    fallback = FactorablePolynomialOptions(
        coef_min=options.coef_min,
        coef_max=options.coef_max,
        leading_coefficient_one=options.leading_coefficient_one,
        positive_leading=options.positive_leading,
        rrt_mode="exclude" if options.rrt_mode == "only" else options.rrt_mode,
        enabled_methods=fallback_methods,
        target_degree_min=options.target_degree_min,
        target_degree_max=options.target_degree_max,
    )
    method = _pick_method(fallback)
    if method is not None:
        return _generate_by_method(method, fallback)
    return _generate_normal(fallback)


def create_factorable_polynomial_with_exact_degree(
    options: FactorablePolynomialOptions,
    exact_degree: int,
) -> FactorablePolynomialResult:
    exact_options = FactorablePolynomialOptions(
        coef_min=options.coef_min,
        coef_max=options.coef_max,
        leading_coefficient_one=options.leading_coefficient_one,
        positive_leading=options.positive_leading,
        rrt_mode=options.rrt_mode,
        enabled_methods=options.enabled_methods,
        target_degree_min=exact_degree,
        target_degree_max=exact_degree,
    )
    return create_factorable_polynomial(exact_options)
