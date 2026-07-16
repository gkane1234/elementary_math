"""Tests for rational simplification cancel-factor settings."""

from __future__ import annotations

import random

import question_engine.types  # noqa: F401 — register types
from question_engine.core.base import QUESTION_TYPES
from question_engine.settings.generator_profiles import schema_for_generator
from question_engine.settings.presets import apply_difficulty_presets, lookup_difficulty_preset
from question_engine.types.algebra_1.rational_expressions.rational_simplification import (
    _create_rational_simplification_problem,
)


def test_schema_exposes_cancel_factor_count():
    keys = {field.key for field in schema_for_generator("rational_simplification")}
    assert "cancel_factor_count" in keys
    field = next(
        f for f in schema_for_generator("rational_simplification") if f.key == "cancel_factor_count"
    )
    assert field.min == 1
    assert field.max == 4
    assert field.default == 1


def test_presets_use_cancel_factor_count():
    easy = lookup_difficulty_preset("easy", type_id="rational_simplification")
    medium = lookup_difficulty_preset("medium", type_id="rational_simplification")
    hard = lookup_difficulty_preset("hard", type_id="rational_simplification")

    assert easy["cancel_factor_count"] == 1
    assert medium["cancel_factor_count"] == 1
    assert hard["cancel_factor_count"] == 2
    assert "max_cancel_factors" not in easy
    assert "max_cancel_factors" not in hard


def test_exact_cancel_factor_count_respected():
    for n in (1, 2, 3):
        settings = {
            "cancel_factor_count": n,
            "numerator_degree_min": n,
            "numerator_degree_max": n + 1,
            "denominator_degree_min": n,
            "denominator_degree_max": n + 1,
            "leading_coefficient_one": True,
            "monic_only": True,
        }
        for i in range(12):
            random.seed(1000 + n * 50 + i)
            num, _den, rnum, _rden, _excl, cancel = _create_rational_simplification_problem(
                settings,
                settings["numerator_degree_min"],
                settings["numerator_degree_max"],
                settings["denominator_degree_min"],
                settings["denominator_degree_max"],
            )
            assert cancel == n
            assert num.deg() - rnum.deg() == n


def test_cancel_count_bumps_degrees_when_needed():
    """Low degree settings still produce N cancels by raising degrees."""
    settings = {
        "cancel_factor_count": 3,
        "numerator_degree_min": 1,
        "numerator_degree_max": 2,
        "denominator_degree_min": 1,
        "denominator_degree_max": 2,
        "leading_coefficient_one": True,
        "monic_only": True,
    }
    for i in range(10):
        random.seed(2000 + i)
        num, den, rnum, _rden, _excl, cancel = _create_rational_simplification_problem(
            settings,
            settings["numerator_degree_min"],
            settings["numerator_degree_max"],
            settings["denominator_degree_min"],
            settings["denominator_degree_max"],
        )
        assert cancel == 3
        assert num.deg() >= 3
        assert den.deg() >= 3
        assert num.deg() - rnum.deg() == 3


def test_legacy_max_cancel_factors_still_honored():
    settings = {
        "max_cancel_factors": 2,
        "numerator_degree_min": 2,
        "numerator_degree_max": 3,
        "denominator_degree_min": 2,
        "denominator_degree_max": 3,
        "leading_coefficient_one": True,
    }
    random.seed(42)
    _num, _den, _rnum, _rden, _excl, cancel = _create_rational_simplification_problem(
        settings, 2, 3, 2, 3
    )
    assert cancel == 2


def test_generate_metadata_includes_cancel_count():
    qt = QUESTION_TYPES["rational_simplification"]
    settings = apply_difficulty_presets(
        {
            "difficulty_tier": "hard",
            "count": 5,
            "include_answer_key": True,
            "cancel_factor_count": 2,
        },
        type_id="rational_simplification",
    )
    questions = qt.generate(settings)
    assert len(questions) == 5
    for q in questions:
        assert q.metadata["cancel_factor_count"] == 2
        assert q.prompt_latex
        assert q.answer_latex
