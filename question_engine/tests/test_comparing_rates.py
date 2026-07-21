"""g6_comparing_rates: compare two rates with double-number-line stimuli."""

from __future__ import annotations

import math
from fractions import Fraction

from question_engine.diagrams.grade6_figures import comparing_rates_double_number_lines_svg
from question_engine.frameworks.number import ComparingRatesFramework
from question_engine.generators import GENERATORS


def test_double_number_line_svg_has_both_people():
    svg = comparing_rates_double_number_lines_svg(
        {
            "title": "Daniel",
            "top_label": "dollars",
            "bottom_label": "pounds",
            "top_values": ["$0", "$2", "$4", "$6", "$8"],
            "bottom_values": [0, 1, 2, 3, 4],
        },
        {
            "title": "Julio",
            "top_label": "dollars",
            "bottom_label": "pounds",
            "top_values": ["$0", "$9"],
            "bottom_values": [0, 4],
        },
    )
    assert "<svg" in svg
    assert "Daniel" in svg and "Julio" in svg
    assert "dollars" in svg and "pounds" in svg


def test_comparing_rates_not_unit_rate_find():
    gen = GENERATORS["g6_comparing_rates"]
    for d in (0, 10, 20, 40):
        qs = gen(
            "g6_comparing_rates",
            {
                "difficulty": d,
                "count": 12,
                "seed": 100 + d,
                "include_answer_key": True,
            },
        )
        for q in qs:
            prompt = q.prompt_latex or ""
            assert "Find the unit rate" not in prompt
            assert "Find the unit price" not in prompt
            assert (
                "higher unit price" in prompt
                or "lower unit price" in prompt
                or "went faster" in prompt
                or "went slower" in prompt
            ), prompt
            meta = q.metadata or {}
            assert meta.get("stimulus_kind") == "double_number_line"
            svg = meta.get("diagram_svg") or ""
            assert "<svg" in svg
            assert meta.get("rate_a") and meta.get("rate_b")
            ans = q.answer_latex or ""
            assert r"\text{" in ans


def test_comparing_rates_answer_matches_comparison():
    fw = ComparingRatesFramework()
    import random

    for seed in range(40):
        random.seed(seed)
        d = (0, 10, 20, 40)[seed % 4]
        latex, _text, answer = fw.build_prompt(
            {"difficulty": d, "include_answer_key": True}
        )
        assert answer is not None
        meta = fw._metadata
        a = meta["rate_a"]
        b = meta["rate_b"]
        name1, t1, b1 = a["name"], a["top"], a["bottom"]
        name2, t2, b2 = b["name"], b["top"], b["bottom"]
        rate1 = Fraction(int(t1), int(b1))
        rate2 = Fraction(int(t2), int(b2))
        assert rate1 != rate2
        winner = answer.replace(r"\text{", "").rstrip("}")
        if "higher" in latex or "faster" in latex:
            expected = name1 if rate1 > rate2 else name2
        else:
            expected = name1 if rate1 < rate2 else name2
        assert winner == expected, (latex, answer, rate1, rate2)


def test_comparing_rates_low_d_often_unit_quantity():
    """At D≈0, at least one given amount is frequently a unit quantity."""
    fw = ComparingRatesFramework()
    import random

    unitish = 0
    for seed in range(40):
        random.seed(seed)
        fw.build_prompt({"difficulty": 0})
        a = fw._metadata["rate_a"]
        b = fw._metadata["rate_b"]
        if int(a["bottom"]) == 1 or int(b["bottom"]) == 1:
            unitish += 1
    assert unitish >= 15


def test_comparing_rates_high_d_can_be_unsimplified():
    """At high D, pairs should have large composite GCFs (not unit qty = 1)."""
    fw = ComparingRatesFramework()
    import random

    messy = 0
    unit_qty = 0
    max_amt = 0
    for seed in range(50):
        random.seed(seed)
        fw.build_prompt({"difficulty": 40})
        a = fw._metadata["rate_a"]
        b = fw._metadata["rate_b"]
        g1 = math.gcd(int(a["top"]), int(a["bottom"]))
        g2 = math.gcd(int(b["top"]), int(b["bottom"]))
        if g1 > 1 or g2 > 1:
            messy += 1
        if int(a["bottom"]) == 1 or int(b["bottom"]) == 1:
            unit_qty += 1
        max_amt = max(
            max_amt,
            int(a["top"]),
            int(a["bottom"]),
            int(b["top"]),
            int(b["bottom"]),
        )
    assert messy >= 40
    assert unit_qty == 0
    assert max_amt >= 40


def test_comparing_rates_continuous_ladder():
    """D≈0 tiny/friendly; D≈40 hard; D=1000 absurd magnitudes."""
    fw = ComparingRatesFramework()
    import random

    easy_max = 0
    for seed in range(40):
        random.seed(seed)
        fw.build_prompt({"difficulty": 0})
        a = fw._metadata["rate_a"]
        b = fw._metadata["rate_b"]
        easy_max = max(
            easy_max,
            int(a["top"]),
            int(a["bottom"]),
            int(b["top"]),
            int(b["bottom"]),
        )
    assert easy_max <= 40

    hard_max = 0
    hard_gcf = 0
    for seed in range(50):
        random.seed(2000 + seed)
        fw.build_prompt({"difficulty": 40})
        a = fw._metadata["rate_a"]
        b = fw._metadata["rate_b"]
        vals = (
            int(a["top"]),
            int(a["bottom"]),
            int(b["top"]),
            int(b["bottom"]),
        )
        hard_max = max(hard_max, *vals)
        assert int(a["bottom"]) > 1 and int(b["bottom"]) > 1
        g = max(
            math.gcd(int(a["top"]), int(a["bottom"])),
            math.gcd(int(b["top"]), int(b["bottom"])),
        )
        if g >= 4:
            hard_gcf += 1
    assert hard_max >= 40
    assert hard_max > easy_max * 2
    assert hard_gcf >= 20

    random.seed(7)
    fw.build_prompt({"difficulty": 1000})
    a = fw._metadata["rate_a"]
    b = fw._metadata["rate_b"]
    extreme_max = max(
        int(a["top"]),
        int(a["bottom"]),
        int(b["top"]),
        int(b["bottom"]),
    )
    assert extreme_max >= 1000
    assert extreme_max > hard_max


def test_comparing_rates_extreme_d_survives():
    """D=1000 must generate huge numbers without crashing."""
    gen = GENERATORS["g6_comparing_rates"]
    qs = gen(
        "g6_comparing_rates",
        {"difficulty": 1000, "count": 2, "seed": 11, "include_answer_key": True},
    )
    assert len(qs) == 2
    for q in qs:
        assert q.prompt_latex
        meta = q.metadata or {}
        a = meta["rate_a"]
        b = meta["rate_b"]
        assert max(int(a["top"]), int(a["bottom"]), int(b["top"]), int(b["bottom"])) >= 1000
        assert "<svg" in (meta.get("diagram_svg") or "")


def test_catalog_wires_comparing_rates_generator():
    from question_engine.core.registry import get_catalog_entry

    entry = get_catalog_entry("g6_comparing_rates")
    assert entry.generator == "g6_comparing_rates"
    assert "double number line" in (entry.instruction_text or "").lower()
