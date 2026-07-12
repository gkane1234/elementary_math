"""Symbolic polynomial layer for question generation."""

from .factoring import (
    FactorablePolynomialOptions,
    FactorablePolynomialResult,
    create_factorable_polynomial,
    create_factorable_polynomial_with_exact_degree,
)
from .special_products import (
    SpecialProductResult,
    create_special_product_problem,
    enabled_special_patterns,
)
from .latex import (
    format_factor_product_latex,
    format_linear_latex,
    format_monomial_latex,
    format_polynomial_latex,
    format_slope_intercept_latex,
    fraction_latex,
    join_algebra_terms,
    polynomial_fraction_latex,
    polynomial_to_latex,
    square_root_latex,
)
from .operations import content_gcd, polynomial_gcd, polynomial_lcm
from .polynomial import Expression, Polynomial, SpecialPhrase
from .rational import (
    PartialFractionTerm,
    RationalExpressionSolution,
    RationalExpressionTerm,
    build_rational_expression_problem,
    polynomial_excluded_values,
    rational_excluded_values_latex,
    sum_of_fractions_latex,
    term_denominator_latex,
    term_denominator_text,
    term_prompt_text,
)

# Module-level convenience aliases
random_polynomial = Polynomial.random_polynomial
from_roots = Polynomial.from_roots
from_coefficients = Polynomial.from_coefficients

__all__ = [
    # Core
    "Polynomial",
    "Expression",
    "SpecialPhrase",
    # Factoring
    "FactorablePolynomialOptions",
    "FactorablePolynomialResult",
    "create_factorable_polynomial",
    "create_factorable_polynomial_with_exact_degree",
    "SpecialProductResult",
    "create_special_product_problem",
    "enabled_special_patterns",
    # Rational expressions
    "PartialFractionTerm",
    "RationalExpressionTerm",
    "RationalExpressionSolution",
    "build_rational_expression_problem",
    "polynomial_excluded_values",
    "rational_excluded_values_latex",
    "sum_of_fractions_latex",
    "term_denominator_latex",
    "term_denominator_text",
    "term_prompt_text",
    # LaTeX
    "fraction_latex",
    "square_root_latex",
    "polynomial_to_latex",
    "polynomial_fraction_latex",
    "format_factor_product_latex",
    "format_monomial_latex",
    "format_polynomial_latex",
    "format_linear_latex",
    "format_slope_intercept_latex",
    "join_algebra_terms",
    # Operations
    "polynomial_gcd",
    "polynomial_lcm",
    "content_gcd",
    # Factories
    "random_polynomial",
    "from_roots",
    "from_coefficients",
]
