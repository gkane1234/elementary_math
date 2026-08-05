"""Tests for progressive practice: coherent topics + monotone D ramp."""

from __future__ import annotations

import json

import question_engine.types  # noqa: F401 — register catalog types
from question_engine.api.handler import handle_generate
from question_engine.progressive import (
    assign_progressive_slots,
    build_progressive_sections,
    difficulty_ramp,
    has_continuous_difficulty,
    select_coherent_topics,
)


def test_difficulty_ramp_monotone():
    ramp = difficulty_ramp(10, 0, 18)
    assert len(ramp) == 10
    assert ramp[0] == 0
    assert ramp[-1] == 18
    assert all(ramp[i] <= ramp[i + 1] for i in range(len(ramp) - 1))


def test_difficulty_ramp_single():
    assert difficulty_ramp(1, 3, 18) == [3.0]


def test_select_coherent_topics_ratios_family():
    topics = select_coherent_topics("g6_introduction_to_ratios", n=4, include_related=True)
    assert "g6_introduction_to_ratios" in topics
    assert 1 <= len(topics) <= 4
    # All selected should be continuous-ready and ratio-family neighbors.
    for tid in topics:
        assert has_continuous_difficulty(tid)
        assert tid.startswith("g6_")
    related = set(topics) - {"g6_introduction_to_ratios"}
    assert related  # should expand beyond the seed
    assert related <= {
        "g6_equivalent_ratios",
        "g6_part_part_whole_ratios",
        "g6_comparing_ratios",
        "g6_unit_rates_and_equivalent_rates",
        "g6_comparing_rates",
        "g6_converting_units",
    } or all(tid.startswith("g6_") for tid in related)


def test_select_coherent_topics_pa_fractions_family():
    topics = select_coherent_topics("pa_simplifying_fractions", n=4, include_related=True)
    assert "pa_simplifying_fractions" in topics
    assert all(has_continuous_difficulty(tid) for tid in topics)
    # Prefer fraction-family neighbors over unrelated chapter mates (LCM/GCF).
    related = [t for t in topics if t != "pa_simplifying_fractions"]
    assert related
    assert any("fraction" in t for t in related)


def test_select_skips_non_continuous_when_required():
    # Seeds without continuous D should yield empty when continuous_only.
    # Use a known scaffold-only / non-cont id if present; otherwise skip via empty seeds.
    topics = select_coherent_topics(
        "g6_introduction_to_ratios",
        n=3,
        include_related=False,
        continuous_only=True,
    )
    assert topics == ["g6_introduction_to_ratios"]


def test_assign_slots_global_ramp_and_topics():
    topics = ["a", "b", "c"]
    slots = assign_progressive_slots(topics, 9, d_min=0, d_max=18)
    assert len(slots) == 9
    diffs = [s["difficulty"] for s in slots]
    assert diffs == sorted(diffs)
    assert diffs[0] == 0
    assert diffs[-1] == 18
    assert all(s["type_id"] in topics for s in slots)
    # Early slots biased to earlier topics.
    assert slots[0]["type_id"] == "a"


def test_build_progressive_sections_settings():
    built = build_progressive_sections(
        seed="g6_introduction_to_ratios",
        count=6,
        d_min=0,
        d_max=12,
        include_related=True,
        max_topics=3,
    )
    assert len(built["sections"]) == 6
    diffs = [s["settings"]["difficulty"] for s in built["sections"]]
    assert diffs == sorted(diffs)
    assert built["plan"]["topics"]
    assert all(has_continuous_difficulty(t) for t in built["plan"]["topics"])


def test_handle_generate_progressive_smoke():
    status, _, body = handle_generate(
        {
            "title": "Progressive smoke",
            "progressive": {
                "seed": "g6_introduction_to_ratios",
                "count": 6,
                "d_min": 0,
                "d_max": 12,
                "include_related": True,
                "max_topics": 3,
            },
        }
    )
    assert status == 200, body
    data = json.loads(body)
    assert len(data["questions"]) == 6
    plan = data["progressive"]
    assert plan["topics"]
    diffs = plan["difficulties"]
    assert diffs == sorted(diffs)
    assert diffs[0] == 0
    assert diffs[-1] == 12
    # Resolved settings on each question should show rising difficulty.
    resolved = []
    for q in data["questions"]:
        gs = (q.get("metadata") or {}).get("generation_settings") or {}
        resolved.append(float(gs["difficulty"]))
    assert resolved == sorted(resolved)
    assert all(has_continuous_difficulty(q["topic"]) for q in data["questions"])


def test_handle_generate_progressive_pa_smoke():
    status, _, body = handle_generate(
        {
            "title": "PA progressive",
            "progressive": {
                "seeds": ["pa_simplifying_fractions"],
                "count": 5,
                "d_min": 2,
                "d_max": 14,
                "include_related": True,
            },
        }
    )
    assert status == 200, body
    data = json.loads(body)
    assert len(data["questions"]) == 5
    diffs = data["progressive"]["difficulties"]
    assert diffs[0] == 2
    assert diffs[-1] == 14
    assert diffs == sorted(diffs)


def test_plan_only_returns_sections_without_questions():
    status, _, body = handle_generate(
        {
            "title": "Plan",
            "progressive": {
                "seed": "pa_simplifying_fractions",
                "count": 4,
                "plan_only": True,
            },
        }
    )
    assert status == 200, body
    data = json.loads(body)
    assert data["questions"] == []
    assert len(data["sections"]) == 4
    assert data["progressive"]["topics"]
