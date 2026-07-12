"""Tests for rational expression multiply / divide difficulty + notation."""

from __future__ import annotations

import random

from question_engine.generators.rational_multiply_divide import (
    build_rational_multiply_divide_prompt,
    generate_rational_expression_multiply_divide,
)
from question_engine.settings.generator_profiles import schema_for_generator
from question_engine.settings.presets import apply_difficulty_presets, lookup_difficulty_preset


def test_presets_differ_structurally_by_tier():
    easy = lookup_difficulty_preset("easy", type_id="rational_expression_multiply_divide")
    medium = lookup_difficulty_preset("medium", type_id="rational_expression_multiply_divide")
    hard = lookup_difficulty_preset("hard", type_id="rational_expression_multiply_divide")

    assert easy["cancel_factor_count"] == 1
    assert easy["leading_coefficient_one"] is True
    assert easy["expand_polynomials"] is False
    assert easy["operand_count"] == 2
    assert easy["allow_complex_fraction"] is False

    assert medium["cancel_factor_count"] == 2
    assert medium["leading_coefficient_one"] is False
    assert medium["expand_polynomials"] is False
    assert medium["allow_slash"] is True

    assert hard["expand_polynomials"] is True
    assert hard["operand_count"] == 3
    assert hard["max_factor_degree"] == 2
    assert hard["allow_complex_fraction"] is True

    a2 = lookup_difficulty_preset(
        "hard", type_id="a2_rational_expressions_multiplying_and_dividing"
    )
    assert a2["operand_count"] == 3


def test_schema_includes_division_and_structure_settings():
    keys = {field.key for field in schema_for_generator("rational_expression_multiply_divide")}
    assert {
        "allow_multiply",
        "allow_divide",
        "cancel_factor_count",
        "expand_polynomials",
        "operand_count",
        "allow_obelus",
        "allow_complex_fraction",
        "allow_slash",
        "coef_min",
        "coef_max",
    } <= keys
    # Factoring knobs from the old profile should not appear.
    assert "factor_normal" not in keys


def test_samples_differ_across_tiers():
    def sample(tier: str, n: int = 24) -> list[str]:
        settings = apply_difficulty_presets(
            {"difficulty_tier": tier, "include_answer_key": True},
            type_id="rational_expression_multiply_divide",
        )
        out: list[str] = []
        for i in range(n):
            random.seed(4000 + i * 31 + len(tier) * 97)
            prompt, _, _ = build_rational_multiply_divide_prompt(settings)
            out.append(prompt)
        return out

    easy = sample("easy")
    medium = sample("medium")
    hard = sample("hard")

    # Easy stays factored monic linears: no expanded x^2 products in display.
    assert all("x^{2}" not in p and "x^2" not in p for p in easy)
    # Hard expands products → quadratic terms appear.
    assert any("x^{2}" in p or "x^2" in p for p in hard)
    # Hard often has three · factors.
    assert any(p.count("\\cdot") >= 2 for p in hard)
    # Medium uses non-monic coefficients more often than easy.
    assert any(r"\left(2" in p or r"\left(3" in p or r"\frac{2" in p for p in medium)


def test_division_uses_div_or_complex_fraction_not_reciprocal_multiply():
    settings = apply_difficulty_presets(
        {
            "difficulty_tier": "hard",
            "allow_multiply": False,
            "allow_divide": True,
            "allow_obelus": True,
            "allow_complex_fraction": True,
            "allow_slash": False,
            "include_answer_key": True,
        },
        type_id="rational_expression_multiply_divide",
    )
    seen_div = seen_complex = False
    for i in range(40):
        random.seed(7000 + i)
        prompt, _, _ = build_rational_multiply_divide_prompt(settings)
        assert "\\cdot" not in prompt  # not pre-written as multiply-by-reciprocal
        if "\\div" in prompt:
            seen_div = True
        else:
            # complex fraction: outer frac of two fracs
            assert prompt.startswith("\\frac{")
            seen_complex = True
        if seen_div and seen_complex:
            break
    assert seen_div and seen_complex


def test_easy_division_uses_obelus_only():
    settings = apply_difficulty_presets(
        {
            "difficulty_tier": "easy",
            "allow_multiply": False,
            "allow_divide": True,
            "include_answer_key": True,
        },
        type_id="rational_expression_multiply_divide",
    )
    for i in range(20):
        random.seed(8000 + i)
        prompt, _, _ = build_rational_multiply_divide_prompt(settings)
        assert "\\div" in prompt
        # Not a stacked complex fraction of two rationals (would be frac{frac...}{frac...})
        assert not prompt.startswith("\\frac{\\frac")


def test_generate_returns_questions():
    settings = apply_difficulty_presets(
        {"difficulty_tier": "medium", "count": 5, "include_answer_key": True},
        type_id="rational_expression_multiply_divide",
    )
    questions = generate_rational_expression_multiply_divide("Rational", settings)
    assert len(questions) == 5
    assert all(q.prompt_latex for q in questions)
    assert all(q.answer_latex for q in questions)
