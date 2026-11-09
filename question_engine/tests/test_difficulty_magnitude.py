"""Difficulty keeps moving the numbers after the question form stops changing.

A flat window replays a seeded draw. Positive windows slide (same width, higher
floor and ceiling). Windows that cross zero grow in magnitude. This is the
sampling bound, not a second draw when two prompts happen to match.
"""

from __future__ import annotations

import contextlib
import io
import json
import math
import random

from question_engine.api.handler import handle_generate
from question_engine.frameworks.difficulty_budget import slide_window
from question_engine.settings.enrichment import difficulty_scale, scaled_int_range
from question_engine.settings.params import apply_geometry_continuous_knobs


def test_slide_window_shifts_every_seed_by_the_step_gap():
    low = slide_window(20, 500, 15, anchor=11)
    high = slide_window(20, 500, 20, anchor=11)
    assert high[0] - low[0] == 5
    assert high[1] - low[1] == 5
    assert high[1] - high[0] == low[1] - low[0]
    for seed in range(30):
        before = random.Random(seed).randint(*low)
        after = random.Random(seed).randint(*high)
        assert after == before + 5


def test_soft_scale_is_unchanged_through_d8_and_bounds_keep_moving_after():
    soft8 = 0.45 + 1.2 * (1.0 - math.exp(-8 / 9.0))
    assert difficulty_scale({"difficulty": 8}) == soft8

    signed8 = scaled_int_range({"difficulty": 8}, -12, 12)
    signed9 = scaled_int_range({"difficulty": 9}, -12, 12)
    signed25 = scaled_int_range({"difficulty": 25}, -12, 12)
    assert signed9 == (signed8[0] - 1, signed8[1] + 1)
    assert signed25[0] < signed9[0]
    assert signed25[1] > signed9[1]

    pos8 = scaled_int_range({"difficulty": 8}, 2, 10)
    pos13 = scaled_int_range({"difficulty": 13}, 2, 10)
    assert pos13[0] == pos8[0] + 5
    assert pos13[1] == pos8[1] + 5


def test_geometry_side_bounds_climb_inside_a_flat_step():
    at0 = apply_geometry_continuous_knobs({"difficulty": 0})
    at1 = apply_geometry_continuous_knobs({"difficulty": 1})
    at3 = apply_geometry_continuous_knobs({"difficulty": 3})
    assert at0["side_max"] == 10
    assert at1["side_max"] == 11
    assert at3["side_max"] == 13
    assert at3["side_max"] - at3["side_min"] == at0["side_max"] - at0["side_min"]
    assert apply_geometry_continuous_knobs({"difficulty": 40})["angle_max"] == 175


def _one(type_id: str, difficulty: float, seed: int) -> dict:
    with contextlib.redirect_stdout(io.StringIO()):
        status, _headers, raw = handle_generate(
            {
                "title": type_id,
                "worksheet_settings": {},
                "progressive": {
                    "seeds": [type_id],
                    "count": 1,
                    "d_min": difficulty,
                    "d_max": difficulty,
                    "include_related": False,
                    "max_topics": 1,
                    "base_settings": {"seed": seed, "include_answer_key": True},
                },
            }
        )
    data = json.loads(raw)
    assert status == 200, data.get("error")
    return data["questions"][0]


def _signature(question: dict) -> str:
    meta = question.get("metadata") or {}
    svg = str(meta.get("diagram_svg") or meta.get("figure_svg") or "")
    return "|".join(
        [
            str(question.get("prompt_latex") or ""),
            str(question.get("prompt_text") or ""),
            str(question.get("answer_latex") or ""),
            svg,
        ]
    )


def test_known_plateaus_change_with_the_same_seed():
    cases = (
        ("pa_squares_and_square_roots", 15, 25, 1),
        ("pa_squares_and_square_roots", 20, 25, 1),
        ("g6_numbers_on_a_number_line", 10, 15, 7),
        ("g6_solving_percent_problems_with_formulas", 15, 25, 1),
        ("g6_equations_tape_diagrams", 20, 25, 1),
        ("g6_volume_and_surface_area_using_isometric_drawings", 20, 25, 7),
        ("g6_parallelograms", 0, 5, 1),
    )
    for type_id, low_d, high_d, seed in cases:
        before = _one(type_id, low_d, seed)
        after = _one(type_id, high_d, seed)
        assert _signature(before) != _signature(after), type_id
