"""Genuine mixture (weighted average) and DRT (round-trip / catch-up) checks."""

from __future__ import annotations

import random
import re

from question_engine.frameworks.word_problem import (
    DistanceRateTimeFramework,
    MixtureProblemFramework,
)
from question_engine.generators import GENERATORS


def test_generators_are_narrative_frameworks_not_equation_stubs():
    """Regression: primitive equation-with-fluff must not override these keys."""
    mix = GENERATORS["wp_mixture"]
    drt = GENERATORS["wp_distance_rate_time"]
    qs = mix("mixture_word_problems", {"count": 1, "difficulty": 5, "include_answer_key": True})
    text = qs[0].prompt_text
    assert "amounts satisfy" not in text
    assert "Find x" not in text and "Find z" not in text
    assert "%" in text or "per lb" in text or "costing" in text

    qs2 = drt(
        "distance_rate_time_word_problems",
        {"count": 1, "difficulty": 8, "include_answer_key": True},
    )
    text2 = qs2[0].prompt_text
    assert "DRT gives" not in text2
    assert "amounts satisfy" not in text2


def test_mixture_percent_is_weighted_average():
    fw = MixtureProblemFramework()
    hits = 0
    for seed in range(80):
        random.seed(seed)
        _latex, text, answer = fw.build_prompt(
            {"difficulty": 3, "allow_mixture_percent": True, "allow_mixture_cost": False}
        )
        if "costing" in text or "per lb" in text and "peanuts" not in text and "sand" not in text:
            if "costing" in text:
                continue
        # Percent frames
        m = re.search(
            r"mixes (\d+) (?:cubic yards of soil that is|lb of nuts that are|fl oz of a) "
            r"(\d+)% (?:sand|peanuts|alcohol solution) with "
            r"(\d+) (?:cubic yards of soil that is|lb of nuts that are|fl oz of a) "
            r"(\d+)%",
            text,
        )
        if not m:
            # alcohol wording differs slightly
            m = re.search(
                r"mixes (\d+) fl oz of a (\d+)% alcohol solution with "
                r"(\d+) fl oz of a (\d+)% alcohol solution",
                text,
            )
        if not m:
            m = re.search(
                r"mixes (\d+) cubic yards of soil that is (\d+)% sand with "
                r"(\d+) cubic yards of soil that is (\d+)% sand",
                text,
            )
        if not m:
            m = re.search(
                r"mixes (\d+) lb of nuts that are (\d+)% peanuts with "
                r"(\d+) lb of nuts that are (\d+)% peanuts",
                text,
            )
        assert m, text
        a1, p1, a2, p2 = map(int, m.groups())
        expected = (a1 * p1 + a2 * p2) / (a1 + a2)
        ans = float(str(answer).replace(r"\%", "").replace("%", "").strip())
        assert abs(ans - expected) < 0.05, (text, answer, expected)
        hits += 1
    assert hits >= 40, hits


def test_mixture_cost_is_weighted_average():
    fw = MixtureProblemFramework()
    hits = 0
    for seed in range(100):
        random.seed(seed)
        _latex, text, answer = fw.build_prompt(
            {"difficulty": 10, "allow_mixture_percent": False, "allow_mixture_cost": True}
        )
        if "costing" not in text:
            continue
        m = re.search(
            r"blends (\d+) lb of .+? costing \$(\d+) per lb with "
            r"(\d+) lb of .+? costing \$(\d+) per lb",
            text,
        )
        assert m, text
        w1, c1, w2, c2 = map(int, m.groups())
        expected = (w1 * c1 + w2 * c2) / (w1 + w2)
        ans = float(str(answer).replace(r"\$", "").replace("$", "").strip())
        assert abs(ans - expected) < 0.02, (text, answer, expected)
        hits += 1
    assert hits >= 20, hits


def test_drt_round_trip_find_speed_there():
    fw = DistanceRateTimeFramework()
    hits = 0
    for seed in range(120):
        random.seed(seed)
        _latex, text, answer = fw.build_prompt(
            {
                "difficulty": 8,
                "allow_drt_find_missing": False,
                "allow_drt_round_trip": True,
                "allow_drt_same_direction": False,
                "allow_drt_two_segments": False,
                "allow_drt_opposite": False,
                "allow_distance_mi": True,
                "allow_distance_km": False,
                "allow_distance_m": False,
                "allow_distance_ft": False,
                "allow_time_hr": True,
                "allow_time_min": False,
            }
        )
        if "speed on the way there" not in text:
            continue
        m = re.search(
            r"in (\d+) hr and returns in (\d+) hr at (\d+) mi/hr",
            text,
        )
        if not m:
            m = re.search(
                r"in (\d+) hr and returns in (\d+) hr at (\d+) km/hr",
                text,
            )
        assert m, text
        t_there, t_back, r_back = map(int, m.groups())
        # Same distance: r_there * t_there = r_back * t_back
        expected = r_back * t_back / t_there
        ans = float(str(answer).split()[0])
        assert abs(ans - expected) < 1e-6, (text, answer, expected)
        hits += 1
    assert hits >= 5, hits


def test_drt_catchup_find_slow_speed():
    fw = DistanceRateTimeFramework()
    hits = 0
    for seed in range(150):
        random.seed(seed)
        _latex, text, answer = fw.build_prompt(
            {
                "difficulty": 10,
                "allow_drt_find_missing": False,
                "allow_drt_round_trip": False,
                "allow_drt_same_direction": True,
                "allow_drt_two_segments": False,
                "allow_drt_opposite": False,
                "allow_distance_mi": True,
                "allow_distance_km": False,
                "allow_distance_m": False,
                "allow_distance_ft": False,
                "allow_time_hr": True,
                "allow_time_min": False,
            }
        )
        if "slow" not in text.lower() or "unknown speed" not in text:
            continue
        m = re.search(
            r"(\d+) hr later a faster \w+ leaves the same station at "
            r"(\d+) (?:mi/hr|km/hr) and catches up after (\d+) hr",
            text,
        )
        assert m, text
        head, fast, catch = map(int, m.groups())
        expected = fast * catch / (head + catch)
        ans = float(str(answer).split()[0])
        assert abs(ans - expected) < 1e-6, (text, answer, expected)
        hits += 1
    assert hits >= 5, hits


def test_mixture_drt_smoke_across_difficulty():
    for key, type_id in (
        ("wp_mixture", "mixture_word_problems"),
        ("wp_distance_rate_time", "distance_rate_time_word_problems"),
    ):
        gen = GENERATORS[key]
        for d in (0, 5, 10, 15, 20):
            qs = gen(type_id, {"count": 2, "difficulty": d, "include_answer_key": True})
            assert len(qs) == 2, (key, d)
            assert qs[0].prompt_text
            assert qs[0].answer_latex
            assert "amounts satisfy" not in qs[0].prompt_text
