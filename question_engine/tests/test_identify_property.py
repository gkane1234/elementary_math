"""Tests for Grade-6 identify-the-property questions."""

from __future__ import annotations

import random

from question_engine.frameworks.number import (
    IdentifyPropertyFramework,
    _PROPERTY_LABELS,
)
from question_engine.qa.topic_fit import (
    check_identify_property_answers,
    check_miswire,
    evaluate_topic_fit,
)
from question_engine.catalogs.base import TypeCatalogEntry


def test_identify_property_answers_are_property_names():
    framework = IdentifyPropertyFramework()
    random.seed(11)
    questions = framework.generate_batch(
        "g6_properties_of_addition_and_multiplication",
        {
            "count": 12,
            "include_answer_key": True,
            "multiple_choice": True,
            "difficulty_tier": "medium",
            "coef_min": 2,
            "coef_max": 9,
        },
    )
    assert len(questions) == 12
    label_set = set(_PROPERTY_LABELS)
    for question in questions:
        assert "=" in question.prompt_latex
        plain = (question.answer_latex or "").replace(r"\text{", "").replace("}", "")
        assert plain in label_set
        choices = question.metadata.get("choices")
        assert question.metadata.get("answer_mode") == "multiple_choice"
        assert isinstance(choices, list)
        assert len(choices) == 4
        correct = [c for c in choices if c.get("correct")]
        assert len(correct) == 1
        assert correct[0]["latex"] == question.answer_latex
        distractor_text = {
            c["latex"].replace(r"\text{", "").replace("}", "")
            for c in choices
            if not c.get("correct")
        }
        assert distractor_text <= label_set
        assert plain not in distractor_text


def test_identify_property_miswire_heuristic():
    fails, _ = check_miswire(
        "g6_properties_of_addition_and_multiplication",
        "g6_integer_multiply",
    )
    assert any("identify-property" in f for f in fails)

    fails_ok, _ = check_miswire(
        "g6_properties_of_addition_and_multiplication",
        "g6_properties_of_addition_and_multiplication",
    )
    assert not any("identify-property" in f for f in fails_ok)


def test_identify_property_answer_shape_heuristic():
    assert check_identify_property_answers([r"\text{multiplication}"])
    assert check_identify_property_answers(["18"])
    assert not check_identify_property_answers(
        [r"\text{commutative property of multiplication}"]
    )


def test_evaluate_topic_fit_flags_wrong_keys():
    entry = TypeCatalogEntry(
        id="g6_properties_of_addition_and_multiplication",
        name="Properties of addition and multiplication",
        category="grade_6",
        generator="g6_integer_multiply",
        instruction_text="Identify the property.",
    )
    result = evaluate_topic_fit(
        entry,
        {"medium": ["6 \\cdot 3", "8 \\cdot 4"]},
        answers_by_tier={"medium": ["18", "32"]},
    )
    assert result.status == "FAIL"
    joined = " ".join(result.hard_fails)
    assert "miswire" in joined or "identify-property" in joined
