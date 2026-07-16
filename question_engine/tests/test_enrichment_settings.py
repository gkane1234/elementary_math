"""Verify enrichment settings measurably change generated output."""

from __future__ import annotations

import random

from question_engine.frameworks.equation import OneStepEquationsFramework
from question_engine.frameworks.number import PercentFramework
from question_engine.settings.enrichment import scaled_int_range
from question_engine.settings.generator_profiles import schema_for_generator
from question_engine.settings.resolve import resolve_type_settings
from question_engine.settings.resolve import TypeSettingConfig
from question_engine.types.algebra_1.polynomials.quadratic_factoring import QuadraticFactoringQuestionType
from question_engine.types.algebra_1.rational_expressions.rational_expression_simplification import (
    RationalExpressionSimplificationQuestionType,
)


def _coef_bounds(settings: dict) -> tuple[int, int]:
    framework = OneStepEquationsFramework()
    params_settings = {**settings, "include_answer_key": True, "count": 30}
    coefs: set[int] = set()
    for _ in range(30):
        _, _, answer = framework.build_prompt(params_settings)
        assert answer is not None
    from question_engine.settings.params import equation_params_from_settings

    params = equation_params_from_settings(params_settings)
    return params.coef_min, params.coef_max


def test_difficulty_tier_scales_coefficient_bounds():
    easy_lo, easy_hi = scaled_int_range({"difficulty_tier": "easy"}, -12, 12)
    hard_lo, hard_hi = scaled_int_range({"difficulty_tier": "hard"}, -12, 12)
    assert (hard_hi - hard_lo) > (easy_hi - easy_lo)


def test_exclude_zero_solutions_changes_answers():
    framework = OneStepEquationsFramework()
    random.seed(7)
    answers = set()
    for _ in range(40):
        _, _, answer = framework.build_prompt(
            {
                "count": 1,
                "include_answer_key": True,
                "exclude_zero_solutions": True,
                "coef_min": -3,
                "coef_max": 3,
                "allow_add": True,
                "allow_subtract": False,
                "allow_multiply": False,
                "allow_divide": False,
            }
        )
        assert answer != "0"
        answers.add(answer)
    assert answers


def test_percents_round_to_whole_changes_answer():
    framework = PercentFramework()
    random.seed(3)
    settings = {
        "count": 1,
        "percent_min": 13,
        "percent_max": 17,
        "base_min": 40,
        "base_max": 40,
        "round_to_whole": True,
        "allow_decimal_percents": False,
    }
    _, _, answer = framework.build_prompt(settings)
    assert answer is not None
    assert "." not in answer.replace("\\%", "")


def test_quadratic_factoring_difference_of_squares_only():
    qt = QuadraticFactoringQuestionType()
    random.seed(11)
    questions = qt.generate(
        {
            "count": 8,
            "include_answer_key": True,
            "difference_of_squares_only": True,
            "leading_coefficient_one": True,
        }
    )
    assert questions
    assert all(q.metadata.get("factoring_method") == "difference_of_squares" for q in questions)


def test_rational_expression_force_lcd():
    qt = RationalExpressionSimplificationQuestionType()
    random.seed(5)
    questions = qt.generate(
        {
            "count": 6,
            "include_answer_key": True,
            "force_lcd": True,
            "allow_polynomial_terms": False,
            "term_count": 3,
        }
    )
    assert questions
    assert all(q.metadata.get("has_full_lcd_term") for q in questions)


def test_common_enrichment_in_schema():
    schema = schema_for_generator("one_step_equations")
    keys = {field.key for field in schema}
    assert "difficulty_tier" in keys
    assert "answer_format" in keys
    assert "multiple_choice" in keys
    assert "multiple_choice_ratio" in keys
    # Terms are not a universal enrichment knob.
    assert "min_terms" not in keys
    assert "max_terms" not in keys
    answer_format = next(field for field in schema if field.key == "answer_format")
    assert "multiple_choice" not in (answer_format.options or [])


def test_common_enrichment_profile_resolves():
    schema = resolve_type_settings(TypeSettingConfig(setting_profile="common_enrichment"))
    keys = {field.key for field in schema}
    assert "multiple_choice" in keys
    assert "show_work_lines" in keys
    assert "min_terms" not in keys


def test_radical_add_subtract_keeps_term_controls():
    schema = schema_for_generator("radical_add_subtract")
    keys = {field.key for field in schema}
    assert "min_terms" in keys
    assert "max_terms" in keys
