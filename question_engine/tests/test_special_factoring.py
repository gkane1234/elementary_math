"""Tests for special-product factoring generation."""

from __future__ import annotations

import random

from packages.polynomial_core.special_products import (
    create_special_product_problem,
    _factor_x_n_minus_one,
)
from packages.polynomial_core import Polynomial
from question_engine.generators.basic import _polynomial_factoring_special_cases
from question_engine.settings.presets import apply_difficulty_presets, lookup_difficulty_preset


def test_x8_minus_one_factors_completely():
    factors = _factor_x_n_minus_one(8)
    product = Polynomial([1])
    for factor in factors:
        product = product * factor
    assert product.to_latex() == "x^{8}-1"
    assert len(factors) == 4


def test_hard_preset_enables_higher_even_powers():
    preset = lookup_difficulty_preset("hard", type_id="polynomial_factoring_special_cases")
    assert preset.get("allow_higher_even_powers") is True
    assert int(preset.get("max_even_power", 0)) == 8


def test_hard_can_emit_x8_minus_one_style():
    random.seed(0)
    settings = apply_difficulty_presets(
        {"difficulty_tier": "hard", "count": 40, "include_answer_key": True},
        type_id="polynomial_factoring_special_cases",
    )
    # Force higher-power pattern pool for this check
    settings["factor_difference_of_squares"] = False
    settings["factor_perfect_square_trinomial"] = False
    settings["factor_sum_of_cubes"] = False
    settings["factor_difference_of_cubes"] = False
    settings["allow_higher_even_powers"] = True
    questions = _polynomial_factoring_special_cases("polynomial_factoring_special_cases", settings)
    prompts = {q.prompt_latex for q in questions}
    assert any(p in {"x^{8}-1", "x^{4}-1", "x^{6}-1"} or "x^{8}" in p or "x^{4}" in p for p in prompts)
    assert all("(" not in q.prompt_latex for q in questions)
    assert any(q.answer_latex and "(x-1)" in q.answer_latex for q in questions)


def test_easy_only_square_patterns():
    random.seed(2)
    settings = apply_difficulty_presets(
        {"difficulty_tier": "easy", "count": 20, "include_answer_key": True},
        type_id="polynomial_factoring_special_cases",
    )
    questions = _polynomial_factoring_special_cases("polynomial_factoring_special_cases", settings)
    methods = {q.metadata.get("special_pattern") for q in questions}
    assert methods <= {"difference_of_squares", "perfect_square_trinomial"}
    assert all("(" not in q.prompt_latex for q in questions)


def test_prompts_are_expanded_not_factored():
    random.seed(4)
    for pattern_settings in (
        {"factor_difference_of_squares": True, "factor_perfect_square_trinomial": False,
         "factor_sum_of_cubes": False, "factor_difference_of_cubes": False},
        {"factor_difference_of_squares": False, "factor_perfect_square_trinomial": True,
         "factor_sum_of_cubes": False, "factor_difference_of_cubes": False},
        {"factor_difference_of_squares": False, "factor_perfect_square_trinomial": False,
         "factor_sum_of_cubes": True, "factor_difference_of_cubes": False},
        {"factor_difference_of_squares": False, "factor_perfect_square_trinomial": False,
         "factor_sum_of_cubes": False, "factor_difference_of_cubes": True},
    ):
        for _ in range(10):
            result = create_special_product_problem({**pattern_settings, "coef_max": 5})
            prompt = result.polynomial.to_latex()
            assert "(" not in prompt
            assert result.answer_latex()
