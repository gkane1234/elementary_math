"""Tests for multiple-choice enrichment and choice builders."""

from __future__ import annotations

import random

from question_engine.frameworks.equation import OneStepEquationsFramework
from question_engine.frameworks.mc import make_multiple_choice_choices
from question_engine.settings.enrichment import merge_enrichment_metadata
from question_engine.settings.multiple_choice import build_multiple_choice_metadata


def test_make_multiple_choice_choices_shape():
    random.seed(1)
    choices = make_multiple_choice_choices("5", ["4", "6", "7"])
    assert len(choices) == 4
    assert sum(1 for c in choices if c["correct"]) == 1
    assert {c["latex"] for c in choices if c["correct"]} == {"5"}
    assert all("id" in c and "latex" in c and "correct" in c for c in choices)
    assert [c["id"] for c in choices] == ["a", "b", "c", "d"]


def test_one_step_equations_multiple_choice_on():
    framework = OneStepEquationsFramework()
    random.seed(42)
    questions = framework.generate_batch(
        "one_step_equations",
        {
            "count": 5,
            "include_answer_key": True,
            "multiple_choice": True,
            "coef_min": -5,
            "coef_max": 5,
            "allow_add": True,
            "allow_subtract": True,
            "allow_multiply": False,
            "allow_divide": False,
        },
    )
    assert len(questions) == 5
    for question in questions:
        choices = question.metadata.get("choices")
        assert question.metadata.get("answer_mode") == "multiple_choice"
        assert isinstance(choices, list)
        assert len(choices) == 4
        correct = [c for c in choices if c.get("correct")]
        assert len(correct) == 1
        assert correct[0]["latex"] == question.answer_latex


def test_one_step_equations_multiple_choice_off():
    framework = OneStepEquationsFramework()
    random.seed(42)
    questions = framework.generate_batch(
        "one_step_equations",
        {
            "count": 5,
            "include_answer_key": True,
            "multiple_choice": False,
            "multiple_choice_ratio": 0,
            "coef_min": -5,
            "coef_max": 5,
            "allow_add": True,
            "allow_subtract": False,
            "allow_multiply": False,
            "allow_divide": False,
        },
    )
    assert questions
    assert all(q.metadata.get("answer_mode") != "multiple_choice" for q in questions)
    assert all("choices" not in q.metadata for q in questions)


def test_linear_equation_distractors():
    random.seed(3)
    meta = build_multiple_choice_metadata("y = 2x + 3")
    choices = meta["choices"]
    assert len(choices) == 4
    assert sum(1 for c in choices if c["correct"]) == 1
    latexes = {c["latex"] for c in choices}
    assert "y = 2x + 3" in latexes
    assert any(text != "y = 2x + 3" and text.startswith("y =") for text in latexes)


def test_merge_preserves_framework_choices():
    meta = merge_enrichment_metadata(
        {"multiple_choice": True},
        {
            "choices": [
                {"id": "a", "latex": "1", "correct": True},
                {"id": "b", "latex": "2", "correct": False},
            ],
            "answer_mode": "multiple_choice",
        },
        answer="9",
    )
    assert meta["choices"][0]["latex"] == "1"
