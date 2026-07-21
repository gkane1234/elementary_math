"""Unfactorable / RRT-demanding polys prefer factored presentation; RRT off by default."""

from __future__ import annotations

from packages.polynomial_core import (
    FactorablePolynomialOptions,
    format_polynomial_from_factors,
    should_display_factor_product_expanded,
)
from packages.polynomial_core.polynomial import Polynomial
from question_engine.frameworks.graphing import _sample_solve_by_graphing
from question_engine.frameworks.primitives import (
    PRIM_NUMBERS,
    PRIM_VARIABLE,
    build_context,
)
from question_engine.frameworks.primitives.constructive import construct_rational_sum
from question_engine.frameworks.primitives.expression_policy import POLYNOMIAL_POLICY_DEFAULT
from question_engine.settings.factoring_settings import parse_factoring_settings
from question_engine.settings.generator_profiles import schema_for_generator


def test_rrt_deselected_by_default_in_parse_and_schema():
    parsed = parse_factoring_settings({})
    assert parsed.rrt_mode == "exclude"
    assert parsed.enabled_methods["rrt"] is False

    opts = FactorablePolynomialOptions(coef_min=-5, coef_max=5)
    assert opts.rrt_mode == "exclude"
    assert "rrt" not in opts.enabled_method_pool()

    for gen in (
        "quadratic_factoring",
        "polynomial_factoring_grouping",
        "a2_polynomial_functions_factoring_all_techniques",
    ):
        fields = {f.key: f for f in schema_for_generator(gen)}
        assert fields["factor_rrt"].default is False


def test_three_plus_linears_stay_factored_when_rrt_excluded():
    factors = (Polynomial([1, -1]), Polynomial([1, -2]), Polynomial([1, 3]), Polynomial([1, 4]))
    exclude = FactorablePolynomialOptions(coef_min=-6, coef_max=6, rrt_mode="exclude")
    allow = FactorablePolynomialOptions(
        coef_min=-6,
        coef_max=6,
        rrt_mode="allow",
        enabled_methods={"rrt": True, "normal": True},
    )

    assert should_display_factor_product_expanded(factors, exclude) is False
    assert should_display_factor_product_expanded(factors, allow) is True

    factored = format_polynomial_from_factors(factors, exclude)
    assert factored.startswith("(")
    assert "x^{" not in factored or factored.count("(") >= 3

    expanded = format_polynomial_from_factors(factors, allow)
    assert "(" not in expanded
    assert "x^{4}" in expanded or "x^4" in expanded.replace("{", "").replace("}", "")


def test_two_linears_still_expand_for_normal_factoring():
    factors = (Polynomial([1, -2]), Polynomial([1, 3]))
    opts = FactorablePolynomialOptions(coef_min=-6, coef_max=6, rrt_mode="exclude")
    assert should_display_factor_product_expanded(factors, opts) is True
    latex = format_polynomial_from_factors(factors, opts)
    assert "(" not in latex


def test_constant_plus_two_linears_still_expand():
    """Leading constant does not turn a classroom quadratic into an RRT problem."""
    factors = (Polynomial([2]), Polynomial([1, -1]), Polynomial([1, 2]))
    opts = FactorablePolynomialOptions(coef_min=-6, coef_max=6, rrt_mode="exclude")
    assert should_display_factor_product_expanded(factors, opts) is True


def test_solve_by_graphing_cubic_prefers_factored_without_rrt():
    settings = {
        "leading_coefficient_one": True,
        "monic_only": True,
        "allow_factored_form": False,
        "factor_rrt": False,
        "min_degree": 3,
        "max_degree": 3,
        "root_min": -4,
        "root_max": 4,
        "coef_min": 1,
        "coef_max": 1,
        "integer_only": True,
    }
    for _ in range(12):
        prompt, _, _, roots, _ = _sample_solve_by_graphing(settings)
        if len(roots) < 3:
            continue
        assert "(x" in prompt or "x +" in prompt or "x -" in prompt
        assert prompt.count("(") >= 2
        return
    raise AssertionError("expected at least one cubic sample")


def _rational_ctx(seed: int = 0, **extra):
    settings = {"count": 1, "seed": seed, "factor_rrt": False, **extra}
    return build_context(
        settings,
        [PRIM_NUMBERS, PRIM_VARIABLE],
        policy=POLYNOMIAL_POLICY_DEFAULT,
        leaf_id="rational_expression_simplification",
    )


def test_rational_add_quadratic_dens_expand_when_rrt_off():
    """Two-linear dens (quadratic) stay expanded — classroom factoring for LCD."""
    seen_quad = False
    for seed in range(16):
        ctx = _rational_ctx(seed)
        surface = construct_rational_sum(ctx, d=10.0, cancel_count=1, as_sum=True)
        if "x^{2}" in surface.latex:
            seen_quad = True
            # cancel_count=1 → at most 2 linear dens per term → no cubic/quartic dens.
            assert "x^{3}" not in surface.latex
            assert "x^{4}" not in surface.latex
    assert seen_quad


def test_rational_add_three_plus_linears_factored_when_rrt_off():
    """3+ linear dens stay factored unless RRT is enabled."""
    found = False
    for seed in range(24):
        ctx = _rational_ctx(seed)
        surface = construct_rational_sum(
            ctx, d=14.0, cancel_count=2, as_sum=True, n_terms=3
        )
        if r"\left(" in surface.latex and surface.latex.count(r"\left(") >= 3:
            found = True
            assert "x^{3}" not in surface.latex
            assert "x^{4}" not in surface.latex
            break
    assert found


def test_rational_add_three_plus_linears_may_expand_when_rrt_on():
    ctx = _rational_ctx(1, factor_rrt=True)
    surface = construct_rational_sum(ctx, d=14.0, cancel_count=2, as_sum=True, n_terms=3)
    # With RRT on, multi-linear products are allowed to expand to x^{3}/x^{4}.
    assert "x^{3}" in surface.latex or "x^{4}" in surface.latex or r"\left(" in surface.latex
