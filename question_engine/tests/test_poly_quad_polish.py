"""Polish checks for grouping non-monic leading and quadratic-formula reduction."""

from __future__ import annotations

from packages.polynomial_core.factoring import (
    FactorablePolynomialOptions,
    create_factorable_polynomial,
)
from question_engine.generators.basic import _quadratic_formula_answer_latex


def test_grouping_respects_non_monic_leading():
    opts = FactorablePolynomialOptions(
        coef_min=-10,
        coef_max=10,
        leading_coefficient_one=False,
        enabled_methods={
            "grouping": True,
            "normal": False,
            "substitution": False,
            "difference_of_squares": False,
            "perfect_square_trinomial": False,
            "difference_of_cubes": False,
            "sum_of_cubes": False,
            "rrt": False,
        },
        target_degree_min=3,
        target_degree_max=3,
    )
    leads = {
        abs(int(create_factorable_polynomial(opts).polynomial.leading_coefficient()))
        for _ in range(30)
    }
    assert 1 not in leads or len(leads) > 1
    assert any(lead != 1 for lead in leads)


def test_grouping_easy_stays_monic():
    opts = FactorablePolynomialOptions(
        coef_min=-5,
        coef_max=5,
        leading_coefficient_one=True,
        enabled_methods={
            "grouping": True,
            "normal": False,
            "substitution": False,
            "difference_of_squares": False,
            "perfect_square_trinomial": False,
            "difference_of_cubes": False,
            "sum_of_cubes": False,
            "rrt": False,
        },
        target_degree_min=3,
        target_degree_max=3,
    )
    leads = {
        int(create_factorable_polynomial(opts).polynomial.leading_coefficient())
        for _ in range(20)
    }
    assert leads == {1}


def test_quadratic_formula_reduces_common_factor():
    # 3x^2 + 20x + 16 = 0 → (-20 ± 4√13)/6 → (-10 ± 2√13)/3
    assert _quadratic_formula_answer_latex(3, 20, 16) == r"x = \frac{-10 \pm 2\sqrt{13}}{3}"
