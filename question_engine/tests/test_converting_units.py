"""g6_converting_units: conversion word problems with double-number-line stimuli."""

from __future__ import annotations

from fractions import Fraction

from question_engine.diagrams.grade6_figures import double_number_line_svg
from question_engine.frameworks.number import (
    ConvertingUnitsFramework,
    _convert_tick_pair,
)
from question_engine.generators import GENERATORS


def test_double_number_line_svg_single():
    svg = double_number_line_svg(
        title="Frame",
        top_label="mm",
        bottom_label="cm",
        top_values=[0, 10, 20, 30, 40, 50],
        bottom_values=[0, 1, 2, 3, 4, 5],
    )
    assert "<svg" in svg
    assert "mm" in svg and "cm" in svg
    assert "50" in svg and "5" in svg


def test_convert_tick_pair_mm_cm_example():
    tops, bots = _convert_tick_pair(10, 1, 50)
    assert tops == [0, 10, 20, 30, 40, 50]
    assert bots == [0, 1, 2, 3, 4, 5]


def test_convert_tick_pair_half_step_kg_lb():
    tops, bots = _convert_tick_pair(10, 22, 5)
    assert tops == [0, 5, 10]
    assert bots == [0, 11, 22]


def test_converting_units_not_unit_rate():
    gen = GENERATORS["g6_converting_units"]
    for d in (0, 10, 20, 40):
        qs = gen(
            "g6_converting_units",
            {
                "difficulty": d,
                "count": 12,
                "seed": 200 + d,
                "include_answer_key": True,
            },
        )
        for q in qs:
            prompt = q.prompt_latex or ""
            assert "Find the unit rate" not in prompt
            assert "Find the unit price" not in prompt
            assert "Given that" in prompt, prompt
            meta = q.metadata or {}
            assert meta.get("stimulus_kind") == "double_number_line"
            svg = meta.get("diagram_svg") or ""
            assert "<svg" in svg
            conv = meta.get("conversion") or {}
            assert conv.get("from_unit") and conv.get("to_unit")
            assert conv.get("amount")
            assert meta.get("double_number_line_spec")
            assert q.answer_latex


def test_converting_units_answer_matches_proportion():
    fw = ConvertingUnitsFramework()
    import random

    for seed in range(50):
        random.seed(seed)
        d = (0, 10, 20, 40)[seed % 4]
        _latex, _text, answer = fw.build_prompt(
            {"difficulty": d, "include_answer_key": True}
        )
        assert answer is not None
        conv = fw._metadata["conversion"]
        expected = Fraction(
            int(conv["amount"]) * int(conv["to_step"]),
            int(conv["from_step"]),
        )
        if expected.denominator == 1:
            assert answer == str(expected.numerator)
        else:
            # Fraction latex or terminating decimal.
            if "frac" in answer:
                assert Fraction(expected) == expected
            else:
                assert abs(float(answer) - float(expected)) < 1e-9


def test_converting_units_low_d_metric_whole():
    """Low D: metric-style power-of-10 / small-integer facts, whole answers."""
    fw = ConvertingUnitsFramework()
    import random

    for seed in range(30):
        random.seed(seed)
        _l, _t, answer = fw.build_prompt({"difficulty": 0})
        conv = fw._metadata["conversion"]
        assert not conv["approx"], conv
        assert conv["from_step"] in (10, 100)
        assert answer is not None
        assert "frac" not in answer and "/" not in answer
        assert int(conv["amount"]) % int(conv["from_step"]) == 0


def test_converting_units_high_d_can_be_approx_or_partial():
    """High D: approximate customary rates and/or non-unit multiples."""
    fw = ConvertingUnitsFramework()
    import random

    approx = 0
    partial = 0
    for seed in range(50):
        random.seed(seed)
        fw.build_prompt({"difficulty": 40})
        conv = fw._metadata["conversion"]
        if conv["approx"]:
            approx += 1
        if int(conv["amount"]) % int(conv["from_step"]) != 0:
            partial += 1
    assert approx >= 15
    assert partial + approx >= 20


def test_converting_units_amount_grows_unbounded():
    """Continuous D: multiples grow without a soft cap (D=40 hard, D=1000 absurd)."""
    from question_engine.frameworks.number import _convert_multiples_hi

    assert _convert_multiples_hi(0) == 3
    assert _convert_multiples_hi(40) >= 40  # hard-but-doable dozens
    assert _convert_multiples_hi(1000) > 10_000  # absurd

    fw = ConvertingUnitsFramework()
    import random

    def _max_amount(d: float, trials: int = 40) -> int:
        best = 0
        for seed in range(trials):
            random.seed(seed)
            fw.build_prompt({"difficulty": d})
            best = max(best, int(fw._metadata["conversion"]["amount"]))
        return best

    max0 = _max_amount(0)
    max40 = _max_amount(40)
    max1000 = _max_amount(1000, trials=20)
    assert max40 > max0
    assert max1000 > 50 * max40

    # High D must not collapse to tiny half-step amounts (e.g. 2 m when 5≈16).
    tiny = 0
    for seed in range(40):
        random.seed(seed)
        fw.build_prompt({"difficulty": 40})
        conv = fw._metadata["conversion"]
        if int(conv["amount"]) < int(conv["from_step"]):
            tiny += 1
    assert tiny == 0


def test_catalog_wires_converting_units_generator():
    from question_engine.core.registry import get_catalog_entry

    entry = get_catalog_entry("g6_converting_units")
    assert entry.generator == "g6_converting_units"
    assert "double number line" in (entry.instruction_text or "").lower()
