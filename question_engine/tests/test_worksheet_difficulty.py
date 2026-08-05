"""Tests for worksheet-level difficulty → D ramp mapping."""

from __future__ import annotations

import question_engine.types  # noqa: F401
from question_engine.api.handler import handle_generate
from question_engine.worksheet_difficulty import (
    NAMED_RAMPS,
    WORKSHEET_DIFFICULTY_PRESETS,
    apply_worksheet_difficulty,
    worksheet_difficulty_to_ramp,
)


def test_named_ramps_documented_bands():
    assert WORKSHEET_DIFFICULTY_PRESETS == [
        "level-0",
        "level-1",
        "level-2",
        "level-3",
        "level-4",
    ]
    assert NAMED_RAMPS["level-0"]["d_min"] == 0
    assert NAMED_RAMPS["level-0"]["d_max"] == 3
    assert NAMED_RAMPS["level-1"]["d_min"] == 0
    assert NAMED_RAMPS["level-1"]["d_max"] == 8
    assert NAMED_RAMPS["level-2"]["d_min"] == 3
    assert NAMED_RAMPS["level-2"]["d_max"] == 20
    assert NAMED_RAMPS["level-3"]["d_min"] == 8
    assert NAMED_RAMPS["level-3"]["d_max"] == 25
    assert NAMED_RAMPS["level-4"]["d_min"] == 20
    assert NAMED_RAMPS["level-4"]["d_max"] == 25
    # Legacy EMH + prior D-range aliases still resolve to closest levels.
    assert NAMED_RAMPS["easy"]["level"] == "level-1"
    assert NAMED_RAMPS["medium"]["level"] == "level-2"
    assert NAMED_RAMPS["hard"]["level"] == "level-3"
    assert NAMED_RAMPS["d0-8"]["level"] == "level-1"
    assert NAMED_RAMPS["d4-14"]["level"] == "level-2"
    assert NAMED_RAMPS["d10-22"]["level"] == "level-3"


def test_labels_are_levels_not_emh_or_bare_d_range():
    for key in (
        "level-0",
        "level-1",
        "level-2",
        "level-3",
        "level-4",
        "easy",
        "medium",
        "hard",
        "d0-8",
        "d4-14",
        "d10-22",
    ):
        ramp = worksheet_difficulty_to_ramp(key)
        label = ramp["label"]
        assert "Easy" not in label and "Medium" not in label and "Hard" not in label
        assert label.startswith("Level ")
        assert ramp["level"].startswith("level-")


def test_slider_interpolates_between_level_0_and_4():
    mid = worksheet_difficulty_to_ramp(12)
    assert mid["d_min"] == 10.0  # lerp(0, 20, 0.5)
    assert mid["d_max"] == 14.0  # lerp(3, 25, 0.5)
    assert mid["schedule"] == "moderate"
    assert mid["label"] == "D 12"
    assert "band" not in mid["label"].lower()
    assert "Easy" not in mid["label"]


def test_apply_fills_progressive_body():
    out = apply_worksheet_difficulty(
        {"seed": "g6_introduction_to_ratios", "worksheet_difficulty": "level-1"}
    )
    assert out["d_min"] == 0
    assert out["d_max"] == 8
    assert out["schedule"] == "gentle"
    assert out["worksheet_difficulty"] == "level-1"


def test_api_worksheet_difficulty_level_1_ramp():
    import json

    status, _, body = handle_generate(
        {
            "title": "Ratios Level 1",
            "progressive": {
                "seed": "g6_introduction_to_ratios",
                "count": 5,
                "worksheet_difficulty": "level-1",
                "include_related": True,
                "max_topics": 3,
            },
        }
    )
    assert status == 200
    data = json.loads(body)
    diffs = data["progressive"]["difficulties"]
    assert diffs[0] == 0
    assert diffs[-1] == 8
    assert all(diffs[i] <= diffs[i + 1] for i in range(len(diffs) - 1))


def test_api_legacy_easy_alias_still_works():
    import json

    status, _, body = handle_generate(
        {
            "title": "Legacy easy alias",
            "progressive": {
                "seed": "g6_introduction_to_ratios",
                "count": 5,
                "worksheet_difficulty": "easy",
                "include_related": True,
                "max_topics": 3,
            },
        }
    )
    assert status == 200
    data = json.loads(body)
    diffs = data["progressive"]["difficulties"]
    assert diffs[0] == 0
    assert diffs[-1] == 8


def test_api_legacy_d0_8_alias_maps_to_level_1():
    import json

    status, _, body = handle_generate(
        {
            "title": "Legacy d0-8 alias",
            "progressive": {
                "seed": "g6_introduction_to_ratios",
                "count": 5,
                "worksheet_difficulty": "d0-8",
                "include_related": True,
                "max_topics": 3,
            },
        }
    )
    assert status == 200
    data = json.loads(body)
    diffs = data["progressive"]["difficulties"]
    assert diffs[0] == 0
    assert diffs[-1] == 8
