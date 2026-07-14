"""Percent construction must keep part / whole / percent consistent."""

from __future__ import annotations

import random
import re
from fractions import Fraction

import pytest

from question_engine.frameworks.number import (
    FractionDecimalConvertFramework,
    PercentFramework,
    _soft_fail_independent_percent,
)
from question_engine.generators.numbers import fractions_decimals_and_percents


def _parse_keyed_percent(answer: str) -> float:
    text = answer.replace(r"\%", "").replace("%", "").strip()
    return float(text)


def test_soft_fail_independent_percent_catches_legacy_bug():
    """Legacy path: part = whole * pct // 100 then key pct (e.g. 6 of 67 → 10%)."""
    with pytest.raises(ValueError, match="inconsistent percent triple"):
        _soft_fail_independent_percent(6, 67, 10)


def test_find_percent_answer_matches_part_over_whole():
    framework = PercentFramework()
    settings = {
        "percent_min": 5,
        "percent_max": 50,
        "base_min": 20,
        "base_max": 100,
        "round_to_whole": True,
        "allow_decimal_percents": False,
        "difficulty_tier": "easy",
    }
    find_percent_seen = 0
    for seed in range(80):
        random.seed(seed)
        text = ""
        answer = ""
        for _ in range(12):
            _, text, answer = framework.build_prompt(settings)
            if "what percent of" in text:
                break
        else:
            continue
        find_percent_seen += 1
        match = re.match(r"(-?\d+(?:\.\d+)?) is what percent of (\d+)\?", text)
        assert match is not None, text
        part = Fraction(match.group(1))
        whole = int(match.group(2))
        keyed = _parse_keyed_percent(answer or "")
        actual = float(part * 100 / whole)
        assert keyed == pytest.approx(actual, abs=1e-9), (text, answer, actual)
    assert find_percent_seen >= 20


def test_easy_percent_of_is_mental_math():
    framework = PercentFramework()
    settings = {
        "percent_min": 5,
        "percent_max": 50,
        "base_min": 20,
        "base_max": 100,
        "round_to_whole": True,
        "allow_decimal_percents": False,
        "difficulty_tier": "easy",
    }
    nice = {5, 10, 20, 25, 40, 50, 75}
    for seed in range(40):
        random.seed(seed)
        _, text, answer = framework.build_prompt(settings)
        if not text.startswith("What is"):
            continue
        match = re.match(r"What is (\d+(?:\.\d+)?)% of (\d+)\?", text)
        assert match is not None, text
        percent = float(match.group(1))
        base = int(match.group(2))
        assert percent in nice
        expected = percent * base / 100
        assert expected == int(expected)
        assert float(answer or "") == pytest.approx(expected)


def test_pa_fdp_uses_conversion_forms_not_percent_of():
    random.seed(3)
    questions = fractions_decimals_and_percents(
        "pa_fractions_decimals_and_percents",
        {
            "count": 12,
            "include_answer_key": True,
            "difficulty_tier": "easy",
        },
    )
    assert len(questions) == 12
    for question in questions:
        text = (question.prompt_text or "").lower()
        latex = question.prompt_latex or ""
        assert "what percent of" not in text
        assert "write" in latex.lower() or "write" in text
        assert " as a " in text or " as a " in latex.lower() or "Write" in latex


def test_fdp_framework_easy_bank():
    framework = FractionDecimalConvertFramework(include_percent=True)
    random.seed(9)
    for _ in range(20):
        latex, text, answer = framework.build_prompt({"difficulty_tier": "easy"})
        assert answer
        assert "Write" in latex
