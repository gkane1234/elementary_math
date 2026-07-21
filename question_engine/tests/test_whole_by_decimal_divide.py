"""g6_dividing_whole_numbers_by_decimals continuous ladder."""

from __future__ import annotations

import re
from decimal import Decimal

import random

from question_engine.api.handler import _resolve_generation_settings
from question_engine.frameworks.number import WholeByDecimalDivideFramework
from question_engine.generators import GENERATORS
from question_engine.settings.presets import apply_difficulty_presets, lookup_difficulty_preset


def _parse_div_prompt(latex: str) -> tuple[Decimal, Decimal]:
    """Extract dividend and divisor from a÷b latex (optional parens on negatives)."""
    text = latex.replace(" ", "")
    m = re.match(
        r"^(-?\d+(?:\.\d+)?|\\left\(-?\d+(?:\.\d+)?\\right\)|\(-?\d+(?:\.\d+)?\))"
        r"(?:\\div|/)"
        r"(-?\d+(?:\.\d+)?|\\left\(-?\d+(?:\.\d+)?\\right\)|\(-?\d+(?:\.\d+)?\))$",
        text,
    )
    assert m, latex
    def _num(s: str) -> Decimal:
        s = s.replace("\\left(", "").replace("\\right)", "").replace("(", "").replace(")", "")
        return Decimal(s)
    return _num(m.group(1)), _num(m.group(2))


def test_presets_unlock_ge_one_and_negatives():
    easy = lookup_difficulty_preset("easy", type_id="g6_dividing_whole_numbers_by_decimals")
    medium = lookup_difficulty_preset("medium", type_id="g6_dividing_whole_numbers_by_decimals")
    hard = lookup_difficulty_preset("hard", type_id="g6_dividing_whole_numbers_by_decimals")
    assert easy["divisor_ge_one"] is False
    assert easy["allow_negative"] is False
    assert medium["divisor_ge_one"] is True
    assert medium["allow_negative"] is False
    assert hard["divisor_ge_one"] is True
    assert hard["allow_negative"] is True


def test_apply_presets_maps_continuous_d():
    low = apply_difficulty_presets(
        {"difficulty": 0}, type_id="g6_dividing_whole_numbers_by_decimals"
    )
    mid = apply_difficulty_presets(
        {"difficulty": 10}, type_id="g6_dividing_whole_numbers_by_decimals"
    )
    hi = apply_difficulty_presets(
        {"difficulty": 20}, type_id="g6_dividing_whole_numbers_by_decimals"
    )
    assert low["divisor_ge_one"] is False
    assert mid["divisor_ge_one"] is True
    assert hi["allow_negative"] is True


def test_easy_divisors_strictly_between_0_and_1():
    fw = WholeByDecimalDivideFramework()
    for seed in range(40):
        random.seed(seed)
        latex, _t, answer = fw.build_prompt({"difficulty": 0, "allow_negative": False})
        a, b = _parse_div_prompt(latex)
        assert a == a.to_integral_value()
        assert Decimal("0") < abs(b) < Decimal("1")
        assert "." in str(b)
        assert answer is not None
        assert (a / b) == Decimal(answer)


def test_mid_can_have_divisor_ge_one():
    fw = WholeByDecimalDivideFramework()
    ge1 = 0
    for seed in range(50):
        random.seed(seed + 50)
        settings = apply_difficulty_presets(
            {"difficulty": 10}, type_id="g6_dividing_whole_numbers_by_decimals"
        )
        latex, _t, answer = fw.build_prompt(settings)
        a, b = _parse_div_prompt(latex)
        assert a == a.to_integral_value()
        assert b != b.to_integral_value()
        if abs(b) > Decimal("1"):
            ge1 += 1
        assert answer is not None
        assert (a / b) == Decimal(answer)
    assert ge1 >= 10


def test_high_unlocks_negatives():
    fw = WholeByDecimalDivideFramework()
    signed = 0
    ge1 = 0
    for seed in range(50):
        random.seed(seed + 200)
        settings = apply_difficulty_presets(
            {"difficulty": 20}, type_id="g6_dividing_whole_numbers_by_decimals"
        )
        latex, _t, answer = fw.build_prompt(settings)
        a, b = _parse_div_prompt(latex)
        if a < 0 or b < 0:
            signed += 1
        if abs(b) > Decimal("1"):
            ge1 += 1
        assert answer is not None
        assert (a / b) == Decimal(answer)
    assert signed >= 15
    assert ge1 >= 10


def test_generator_wired_through_api_settings():
    gen = GENERATORS["g6_whole_by_decimal_divide"]
    settings = _resolve_generation_settings(
        "g6_dividing_whole_numbers_by_decimals",
        {"difficulty": 40, "count": 12, "seed": 7, "include_answer_key": True},
    )
    qs = gen("g6_dividing_whole_numbers_by_decimals", settings)
    assert len(qs) == 12
    signed = 0
    for q in qs:
        a, b = _parse_div_prompt(q.prompt_latex or "")
        if a < 0 or b < 0:
            signed += 1
        assert b != b.to_integral_value()
        assert Decimal(q.answer_latex or "0") == (a / b)
    assert signed >= 1
