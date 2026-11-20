"""Grade 6 progressive worksheet templates.

Lesson order follows ``lib/curriculum.ts`` (course ``grade_6_math``). Other
courses stay on ``select_coherent_topics``.
"""

from __future__ import annotations

import json

import question_engine.types  # noqa: F401 — register catalog types
from question_engine.api.handler import handle_generate
from question_engine.progressive import (
    assign_progressive_slots,
    build_progressive_sections,
    select_coherent_topics,
)
from question_engine.worksheet_courses.base import plan_topics_for_seeds
from question_engine.worksheet_courses.grade_6 import plan_topics

_PLAN_KEYS = {
    "focus",
    "warmup",
    "drill",
    "stretch",
    "omitted",
    "spiral_suggestion",
    "course_id",
}

RATIOS = [
    "g6_introduction_to_ratios",
    "g6_equivalent_ratios",
    "g6_part_part_whole_ratios",
    "g6_comparing_ratios",
]
RATES = [
    "g6_unit_rates_and_equivalent_rates",
    "g6_comparing_rates",
    "g6_converting_units",
]

_ALGEBRA_NEIGHBORS = [
    "one_step_equations",
    "two_step_equations",
    "pa_equations_one_step_word_problems",
    "pa_equations_two_step_word_problems",
]


def _phase_runs(phases: list[str]) -> list[str]:
    runs: list[str] = []
    for phase in phases:
        if not runs or runs[-1] != phase:
            runs.append(phase)
    return runs


def test_lesson_ramp_phase_order_and_monotone_d():
    built = build_progressive_sections(
        seed="g6_comparing_ratios",
        count=10,
        d_min=0,
        d_max=18,
        pairing="lesson",
        scope="topic",
        style="ramp",
        include_related=True,
        max_topics=4,
    )
    phases = [slot["phase"] for slot in built["slots"]]
    assert _phase_runs(phases) == ["warmup", "focus", "drill", "stretch"]
    diffs = built["plan"]["difficulties"]
    assert diffs == sorted(diffs)
    assert diffs[0] == 0
    assert diffs[-1] == 18
    assert all(diffs[i] <= diffs[i + 1] for i in range(len(diffs) - 1))
    assert built["slots"][0]["type_id"] == "g6_equivalent_ratios"
    assert built["slots"][1]["type_id"] == "g6_part_part_whole_ratios"
    assert built["plan"]["focus"] == ["g6_comparing_ratios"]
    assert built["slots"][-1]["type_id"] == "g6_unit_rates_and_equivalent_rates"
    assert built["plan"]["stretch"] == ["g6_unit_rates_and_equivalent_rates"]
    assert len(built["plan"]["topics"]) <= 4


def test_flat_customization_is_one_difficulty_and_checked_topics_only():
    checked = ["g6_equivalent_ratios", "g6_comparing_ratios"]
    built = build_progressive_sections(
        seed="g6_introduction_to_ratios",
        count=6,
        d_min=0,
        d_max=18,
        scope="unit",
        topics=checked,
        style="straight",
        pairing="lesson",
        include_related=True,
    )
    diffs = built["plan"]["difficulties"]
    assert len(set(diffs)) == 1
    assert diffs[0] == 9.0
    assert [slot["type_id"] for slot in built["slots"]] == [
        "g6_equivalent_ratios",
        "g6_equivalent_ratios",
        "g6_equivalent_ratios",
        "g6_comparing_ratios",
        "g6_comparing_ratios",
        "g6_comparing_ratios",
    ]
    assert set(built["plan"]["phases"]) == {"focus"}
    assert built["plan"]["warmup"] == []
    assert built["plan"]["stretch"] == []
    assert built["plan"]["style"] == "straight"
    assert built["plan"]["omitted_topics"] == []


def test_short_count_reports_omitted_topics():
    built = build_progressive_sections(
        seed="g6_introduction_to_ratios",
        count=2,
        d_min=0,
        d_max=10,
        scope="unit",
        topics=RATIOS,
        style="ramp",
        pairing="lesson",
    )
    assert [slot["type_id"] for slot in built["slots"]] == RATIOS[:2]
    assert built["plan"]["omitted_topics"] == RATIOS[2:]
    assert built["plan"]["difficulties"] == sorted(built["plan"]["difficulties"])


def test_algebra_seed_keeps_select_coherent_topics():
    assert plan_topics_for_seeds(["one_step_equations"]) is None
    assert plan_topics_for_seeds(
        ["g6_introduction_to_ratios", "one_step_equations"]
    ) is None
    old = select_coherent_topics("one_step_equations", n=4, include_related=True)
    assert old == _ALGEBRA_NEIGHBORS
    built = build_progressive_sections(
        seed="one_step_equations",
        count=8,
        d_min=0,
        d_max=18,
        include_related=True,
        max_topics=4,
    )
    assert built["plan"]["topics"] == old
    assert built["plan"]["course_id"] is None
    expected = assign_progressive_slots(old, 8, d_min=0, d_max=18)
    assert [slot["type_id"] for slot in built["slots"]] == [
        slot["type_id"] for slot in expected
    ]
    assert [slot["difficulty"] for slot in built["slots"]] == [
        slot["difficulty"] for slot in expected
    ]


def test_legacy_grade_6_call_defaults_to_lesson_ramp_topic():
    built = build_progressive_sections(
        seed="g6_introduction_to_ratios",
        count=6,
        d_min=0,
        d_max=12,
        include_related=True,
        max_topics=4,
    )
    assert built["plan"]["pairing"] == "lesson"
    assert built["plan"]["scope"] == "topic"
    assert built["plan"]["style"] == "ramp"
    assert built["plan"]["course_id"] == "grade_6_math"
    assert built["plan"]["difficulties"][0] == 0
    assert built["plan"]["difficulties"][-1] == 12
    assert built["slots"][0]["type_id"] == "g6_introduction_to_ratios"
    assert "g6_equivalent_ratios" in [slot["type_id"] for slot in built["slots"]]


def test_omitted_topic_list_stays_within_max_topics():
    plan = plan_topics(
        ["g6_decimal_addition"],
        pairing="lesson",
        scope="unit",
        max_topics=4,
    )
    assert set(plan) == _PLAN_KEYS
    unique = set(plan["focus"]) | set(plan["warmup"]) | set(plan["stretch"])
    assert len(unique) <= 4
    assert "g6_decimal_addition" in plan["focus"]
    assert plan["omitted"] == []


def test_explicit_topics_are_kept_past_max_topics():
    topics = [
        "g6_decimal_addition_with_diagrams",
        "g6_decimal_addition",
        "g6_decimal_subtraction_with_diagrams",
        "g6_decimal_subtraction",
        "g6_decimal_multiplication_with_equivalent_fractions",
        "g6_decimal_multiplication_with_area_diagrams",
        "g6_decimal_multiplication",
        "g6_long_division_with_remainders",
        "g6_dividing_whole_numbers_that_result_in_decimals",
        "g6_dividing_decimals_by_whole_numbers",
        "g6_dividing_whole_numbers_by_decimals",
        "g6_dividing_decimals_by_decimals",
    ]
    plan = plan_topics(
        ["g6_decimal_addition"],
        pairing="lesson",
        scope="unit",
        topics=topics,
        max_topics=4,
    )
    assert len(plan["focus"]) > 4
    assert set(plan["focus"]) <= set(topics)
    assert "g6_decimal_addition" in plan["focus"]
    assert len(plan["warmup"]) + len(plan["stretch"]) == 0


def test_spiral_names_the_previous_unit_without_switching_pairing():
    lesson = plan_topics(
        ["g6_introduction_to_percents"],
        pairing="lesson",
        scope="topic",
    )
    assert lesson["spiral_suggestion"] == "Rates"
    assert lesson["course_id"] == "grade_6_math"
    spiral = plan_topics(
        ["g6_introduction_to_percents"],
        pairing="spiral",
        scope="topic",
    )
    assert spiral["spiral_suggestion"] == "Rates"
    assert spiral["drill"] == []
    assert spiral["warmup"] == ["g6_comparing_rates", "g6_converting_units"]
    assert spiral["focus"] == ["g6_introduction_to_percents"]
    assert spiral["stretch"] == ["g6_dividing_fractions"]
    first = plan_topics(["g6_introduction_to_ratios"], pairing="lesson", scope="topic")
    assert first["spiral_suggestion"] is None


def test_drill_topic_is_neighbors_without_warmup():
    plan = plan_topics(
        ["g6_equivalent_ratios"],
        pairing="drill",
        scope="topic",
    )
    assert plan["focus"] == RATIOS[:3]
    assert plan["warmup"] == []
    assert plan["stretch"] == []
    assert plan["drill"] == plan["focus"]


def test_include_related_false_suppresses_warmup_and_stretch():
    plan = plan_topics(
        ["g6_comparing_ratios"],
        pairing="lesson",
        scope="topic",
        include_related=False,
    )
    assert plan["focus"] == ["g6_comparing_ratios"]
    assert plan["warmup"] == []
    assert plan["stretch"] == []


def test_rates_lesson_uses_ratio_prereq_not_an_invented_pairing():
    plan = plan_topics(
        ["g6_unit_rates_and_equivalent_rates"],
        pairing="lesson",
        scope="unit",
        max_topics=12,
    )
    assert plan["focus"] == RATES
    assert plan["warmup"] == ["g6_part_part_whole_ratios", "g6_comparing_ratios"]
    assert plan["stretch"] == ["g6_introduction_to_percents"]
    assert plan["spiral_suggestion"] == "Ratios"


def test_handle_generate_ratios_and_rates_lesson_is_ordered_and_monotone():
    status, _, body = handle_generate(
        {
            "title": "Ratios and Rates",
            "progressive": {
                "seeds": ["g6_introduction_to_ratios"],
                "count": 12,
                "d_min": 0,
                "d_max": 18,
                "include_related": True,
                "max_topics": 12,
                "pairing": "lesson",
                "scope": "adjacent",
                "topics": RATIOS + RATES,
                "style": "ramp",
                "plan_only": False,
            },
        }
    )
    assert status == 200, body
    data = json.loads(body)
    assert len(data["questions"]) == 12
    plan = data["progressive"]
    diffs = plan["difficulties"]
    assert diffs == sorted(diffs)
    assert diffs[0] == 0
    assert diffs[-1] == 18
    phases = plan["phases"]
    assert _phase_runs(phases) == ["focus", "drill", "stretch"]
    topics = [question["topic"] for question in data["questions"]]
    assert topics[0] == "g6_introduction_to_ratios"
    first_rate = next(index for index, topic in enumerate(topics) if topic in RATES)
    assert first_rate > 0
    assert all(topic in RATIOS for topic in topics[:first_rate])
    assert topics[-1] == "g6_introduction_to_percents"
    assert plan["stretch"] == ["g6_introduction_to_percents"]
    resolved = []
    for question in data["questions"]:
        settings = (question.get("metadata") or {}).get("generation_settings") or {}
        resolved.append(float(settings["difficulty"]))
    assert resolved == sorted(resolved)
    assert plan["pairing"] == "lesson"
    assert plan["scope"] == "adjacent"
    assert plan["style"] == "ramp"
    assert plan["course_id"] == "grade_6_math"
    assert set(RATIOS + RATES) <= set(topics)
    assert plan["omitted_topics"] == []
