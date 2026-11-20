"""Geometry progressive worksheet plans.

The shared dispatcher in ``question_engine.progressive`` is owned by another
change. These tests call ``plan_topics`` directly, and they call
``build_progressive_sections`` only when that function already delegates here.
"""

from __future__ import annotations

import importlib.util
import inspect
import json
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[2]
_GALLERY_PATH = _REPO / "config" / "worksheet-gallery-geometry.json"
_GEOMETRY_PATH = _REPO / "question_engine" / "worksheet_courses" / "geometry.py"

BASICS = [
    "geo_basics_line_segments_and_their_measures",
    "geo_basics_segment_addition_postulate",
    "geo_basics_angles_and_their_measures",
    "geo_basics_classifying_angles",
    "geo_basics_basic_angle_terminology",
    "geo_basics_angle_addition_postulate",
    "geo_basics_angle_relationships",
    "geo_basics_geometric_diagrams_and_notation",
]

PARALLEL = [
    "geo_parallel_parallel_lines_and_transversals",
    "geo_parallel_points_of_the_coordinate_plane",
    "radical_midpoint_formula",
    "geo_parallel_distance_formula",
    "geo_parallel_slope_and_lines",
    "geo_parallel_graphing_linear_equations",
    "geo_parallel_writing_linear_equations",
]

_PLAN_KEYS = {
    "focus",
    "warmup",
    "drill",
    "stretch",
    "omitted",
    "spiral_suggestion",
    "course_id",
}

_TEMPLATE_IDS = (
    "geo-basics-unit-lesson",
    "geo-angle-relationships-lesson",
    "geo-basics-adjacent-lesson",
    "geo-congruent-triangles-spiral",
)


def _load_geometry():
    """Prefer the package import. Fall back if ``__init__.py`` is mid-write."""
    try:
        import question_engine.worksheet_courses.geometry as module

        return module
    except Exception:
        spec = importlib.util.spec_from_file_location(
            "geometry_worksheet_course_plan",
            _GEOMETRY_PATH,
        )
        if spec is None or spec.loader is None:
            raise
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module


_geometry = _load_geometry()
plan_topics = _geometry.plan_topics


def _assert_shape(plan: dict) -> None:
    assert set(plan) == _PLAN_KEYS
    assert plan["course_id"] == "geometry"
    assert plan["omitted"] == []
    for key in ("focus", "warmup", "drill", "stretch"):
        assert isinstance(plan[key], list)


def test_lesson_topic_angles_warmup_is_earlier_basics():
    plan = plan_topics(
        ["geo_basics_angles_and_their_measures"],
        scope="topic",
        pairing="lesson",
    )
    _assert_shape(plan)
    assert plan["focus"] == ["geo_basics_angles_and_their_measures"]
    assert plan["warmup"] == [
        "geo_basics_line_segments_and_their_measures",
        "geo_basics_segment_addition_postulate",
    ]
    assert plan["stretch"] == ["geo_basics_classifying_angles"]
    assert plan["drill"] == plan["focus"]
    assert plan["spiral_suggestion"] is None
    assert len(plan["focus"]) + len(plan["warmup"]) + len(plan["stretch"]) <= 4


def test_scope_unit_basics_is_that_chapter_only():
    plan = plan_topics(
        ["geo_basics_angles_and_their_measures"],
        scope="unit",
        pairing="lesson",
        max_topics=30,
    )
    _assert_shape(plan)
    assert plan["focus"] == BASICS
    assert plan["warmup"] == [
        "geo_review_multiplying_square_roots",
        "geo_review_dividing_square_roots",
    ]
    assert plan["stretch"] == ["geo_parallel_parallel_lines_and_transversals"]
    assert not any(type_id in PARALLEL for type_id in plan["focus"])
    assert not any(type_id.startswith("geo_review_") for type_id in plan["focus"])


def test_scope_adjacent_adds_parallel_lines_after_basics():
    plan = plan_topics(
        ["geo_basics_angles_and_their_measures"],
        scope="adjacent",
        pairing="lesson",
        max_topics=30,
    )
    _assert_shape(plan)
    assert plan["focus"] == BASICS + PARALLEL
    assert "geo_congruent_classifying_triangles" not in plan["focus"]
    assert plan["stretch"] == ["geo_congruent_classifying_triangles"]
    assert plan["focus"][0] == "geo_basics_line_segments_and_their_measures"
    assert plan["focus"][-1] == "geo_parallel_writing_linear_equations"


def test_spiral_congruent_triangles_reviews_previous_unit():
    plan = plan_topics(
        ["geo_congruent_classifying_triangles"],
        pairing="spiral",
        scope="topic",
    )
    _assert_shape(plan)
    assert plan["focus"] == ["geo_congruent_classifying_triangles"]
    assert plan["warmup"] == [
        "geo_parallel_graphing_linear_equations",
        "geo_parallel_writing_linear_equations",
    ]
    assert plan["stretch"] == ["geo_properties_midsegment"]
    assert plan["drill"] == []
    assert plan["spiral_suggestion"] is not None
    assert "Parallel Lines and the Coordinate Plane" in plan["spiral_suggestion"]
    assert all(type_id in PARALLEL for type_id in plan["warmup"])


def test_spiral_first_unit_has_no_suggestion():
    plan = plan_topics(
        ["geo_review_multi_step_equations"],
        pairing="spiral",
        scope="topic",
    )
    _assert_shape(plan)
    assert plan["spiral_suggestion"] is None
    assert plan["warmup"] == []
    assert plan["focus"] == ["geo_review_multi_step_equations"]
    assert plan["stretch"] == ["geo_basics_line_segments_and_their_measures"]


def test_one_step_equations_is_not_geometry():
    plan = plan_topics(["one_step_equations"])
    _assert_shape(plan)
    assert plan["focus"] == []
    assert plan["warmup"] == []
    assert plan["drill"] == []
    assert plan["stretch"] == []
    blob = plan["focus"] + plan["warmup"] + plan["drill"] + plan["stretch"]
    assert "one_step_equations" not in blob

    mixed = plan_topics(
        ["one_step_equations", "geo_basics_angles_and_their_measures"],
        scope="topic",
        pairing="lesson",
    )
    assert mixed["focus"] == ["geo_basics_angles_and_their_measures"]
    assert "one_step_equations" not in (
        mixed["focus"] + mixed["warmup"] + mixed["drill"] + mixed["stretch"]
    )


def test_distance_formula_topic_id_uses_curriculum_type_id():
    plan = plan_topics(
        ["radical_distance_formula"],
        scope="unit",
        pairing="drill",
        max_topics=20,
    )
    _assert_shape(plan)
    assert plan["focus"] == PARALLEL
    assert "radical_distance_formula" not in plan["focus"]
    assert "geo_parallel_distance_formula" in plan["focus"]
    assert plan["warmup"] == []
    assert plan["stretch"] == []
    assert plan["drill"] == plan["focus"]


def test_pythagorean_topic_id_resolves_to_type_id():
    plan = plan_topics(["pythagorean_theorem"], pairing="drill", scope="topic")
    _assert_shape(plan)
    assert plan["focus"] == [
        "geo_right_pythagorean_theorem",
        "geo_right_multi_step_pythagorean_theorem_problems",
    ]
    assert "pythagorean_theorem" not in plan["focus"]


def test_drill_topic_is_previous_seed_and_next():
    plan = plan_topics(
        ["geo_basics_angles_and_their_measures"],
        pairing="drill",
        scope="topic",
    )
    assert plan["focus"] == [
        "geo_basics_segment_addition_postulate",
        "geo_basics_angles_and_their_measures",
        "geo_basics_classifying_angles",
    ]
    assert plan["warmup"] == []
    assert plan["stretch"] == []
    assert plan["drill"] == plan["focus"]


def test_include_related_false_clears_warmup_and_stretch():
    plan = plan_topics(
        ["geo_basics_angles_and_their_measures"],
        include_related=False,
    )
    assert plan["focus"] == ["geo_basics_angles_and_their_measures"]
    assert plan["warmup"] == []
    assert plan["stretch"] == []

    spiral = plan_topics(
        ["geo_congruent_classifying_triangles"],
        pairing="spiral",
        include_related=False,
    )
    assert spiral["warmup"] == []
    assert spiral["stretch"] == []
    assert spiral["focus"] == ["geo_congruent_classifying_triangles"]
    assert "Parallel Lines and the Coordinate Plane" in spiral["spiral_suggestion"]


def test_omitted_topics_cap_trims_stretch_then_warmup_then_keeps_seed():
    trimmed = plan_topics(
        ["geo_basics_geometric_diagrams_and_notation"],
        scope="unit",
        pairing="lesson",
        max_topics=3,
    )
    assert trimmed["warmup"] == []
    assert trimmed["stretch"] == []
    assert trimmed["focus"] == [
        "geo_basics_line_segments_and_their_measures",
        "geo_basics_segment_addition_postulate",
        "geo_basics_geometric_diagrams_and_notation",
    ]
    assert trimmed["omitted"] == []

    drop_stretch = plan_topics(
        ["geo_basics_angles_and_their_measures"],
        scope="topic",
        pairing="lesson",
        max_topics=3,
    )
    assert drop_stretch["stretch"] == []
    assert drop_stretch["warmup"] == BASICS[:2]
    assert drop_stretch["focus"] == ["geo_basics_angles_and_their_measures"]


def test_explicit_topics_are_not_dropped_for_max_topics():
    plan = plan_topics(
        ["geo_basics_angles_and_their_measures"],
        scope="unit",
        topics=[
            "geo_basics_geometric_diagrams_and_notation",
            "geo_basics_line_segments_and_their_measures",
            "geo_parallel_parallel_lines_and_transversals",
        ],
        max_topics=1,
    )
    assert plan["focus"] == [
        "geo_basics_line_segments_and_their_measures",
        "geo_basics_geometric_diagrams_and_notation",
    ]
    assert plan["warmup"] == []
    assert plan["stretch"] == []
    assert len(plan["focus"]) > 1


def test_topic_leaves_requires_replace_earlier_unit_leaves(monkeypatch):
    monkeypatch.setattr(
        _geometry,
        "_requires_for",
        lambda type_id: (
            ("geo_basics_classifying_angles", "geo_basics_angle_relationships")
            if type_id == "geo_basics_angles_and_their_measures"
            else ()
        ),
    )
    plan = plan_topics(
        ["geo_basics_angles_and_their_measures"],
        scope="topic",
        pairing="lesson",
    )
    assert plan["warmup"] == [
        "geo_basics_classifying_angles",
        "geo_basics_angle_relationships",
    ]
    assert "geo_basics_line_segments_and_their_measures" not in plan["warmup"]


def test_not_ready_leaf_is_omitted_from_unit():
    plan = plan_topics(
        ["geo_trig_finding_trig_ratios"],
        scope="unit",
        pairing="drill",
        max_topics=20,
    )
    assert "geo_trig_finding_trig_ratios" in plan["focus"]
    assert "geo_trig_trigonometry_and_area" in plan["focus"]
    assert "geo_trig_rhombuses_and_kites_with_right_triangles" not in plan["focus"]


def test_lesson_unit_for_congruent_uses_json_prereq_not_previous_chapter():
    plan = plan_topics(
        ["geo_congruent_classifying_triangles"],
        pairing="lesson",
        scope="unit",
        max_topics=20,
    )
    assert plan["warmup"] == [
        "geo_basics_angle_relationships",
        "geo_basics_geometric_diagrams_and_notation",
    ]
    assert not any(type_id in PARALLEL for type_id in plan["warmup"])
    assert plan["stretch"] == ["geo_properties_midsegment"]


def test_geometry_gallery_templates():
    raw = json.loads(_GALLERY_PATH.read_text(encoding="utf-8"))
    assert raw["version"] == 1
    entries = raw["entries"]
    assert [entry["id"] for entry in entries] == list(_TEMPLATE_IDS)
    seeds = [entry["seed"] for entry in entries]
    assert len(seeds) == len(set(seeds))
    assert all(seed not in range(1001, 1011) for seed in seeds)

    for entry in entries:
        assert entry["style"] == "ramp"
        assert entry["course"] == "Geometry"
        assert entry["includeRelated"] is True
        assert "rampEachTopic" in entry
        assert entry["worksheetDifficulty"]
        assert entry["count"] >= 1
        assert entry["pairing"] in {"lesson", "drill", "spiral"}
        assert entry["scope"] in {"topic", "unit", "adjacent"}
        plan = plan_topics(
            entry["seeds"],
            pairing=entry["pairing"],
            scope=entry["scope"],
            topics=entry.get("topics"),
            max_topics=entry["maxTopics"],
            include_related=entry["includeRelated"],
        )
        _assert_shape(plan)
        assert plan["focus"]
        if not entry.get("topics"):
            assert (
                len(plan["focus"]) + len(plan["warmup"]) + len(plan["stretch"])
                <= entry["maxTopics"]
            )

    basics = plan_topics(
        ["geo_basics_angles_and_their_measures"],
        pairing="lesson",
        scope="unit",
        max_topics=12,
        include_related=True,
    )
    assert basics["focus"] == BASICS

    angles = plan_topics(
        ["geo_basics_angle_relationships"],
        pairing="lesson",
        scope="topic",
        max_topics=4,
    )
    assert angles["focus"] == ["geo_basics_angle_relationships"]
    assert angles["warmup"] == [
        "geo_basics_basic_angle_terminology",
        "geo_basics_angle_addition_postulate",
    ]
    assert angles["stretch"] == ["geo_basics_geometric_diagrams_and_notation"]

    adjacent = plan_topics(
        ["geo_basics_angles_and_their_measures"],
        pairing="lesson",
        scope="adjacent",
        max_topics=20,
    )
    assert adjacent["focus"] == BASICS + PARALLEL

    spiral = plan_topics(
        ["geo_congruent_classifying_triangles"],
        pairing="spiral",
        scope="topic",
        max_topics=4,
    )
    assert "Parallel Lines and the Coordinate Plane" in spiral["spiral_suggestion"]


def _progressive_source() -> str:
    import question_engine.progressive as progressive

    try:
        return inspect.getsource(progressive)
    except OSError:
        return ""


def test_dispatcher_basics_unit_sheet_when_wired():
    """Monotone D and no parallel-lines chapter when the shared planner calls us."""
    src = _progressive_source()
    if "plan_topics" not in src or "geometry" not in src:
        pytest.skip(
            "build_progressive_sections does not dispatch to geometry.plan_topics yet"
        )

    import question_engine.progressive as progressive

    sig = inspect.signature(progressive.build_progressive_sections)
    params = sig.parameters
    has_var = any(p.kind is inspect.Parameter.VAR_KEYWORD for p in params.values())
    if not has_var and "scope" not in params and "pairing" not in params:
        pytest.skip(
            "dispatcher mentions geometry but does not accept scope/pairing yet"
        )

    kwargs = {
        "seeds": ["geo_basics_angles_and_their_measures"],
        "count": 8,
        "d_min": 0,
        "d_max": 12,
        "include_related": True,
        "max_topics": 8,
    }
    for key, value in (("scope", "unit"), ("pairing", "lesson")):
        if has_var or key in params:
            kwargs[key] = value

    built = progressive.build_progressive_sections(**kwargs)
    plan = built["plan"]
    diffs = list(plan.get("difficulties") or [])
    if not diffs:
        diffs = [section["settings"]["difficulty"] for section in built["sections"]]
    assert diffs
    assert diffs == sorted(diffs)
    assert all(diffs[i] <= diffs[i + 1] for i in range(len(diffs) - 1))

    placed = [section["type_id"] for section in built["sections"]]
    assert placed
    assert not any(type_id in PARALLEL for type_id in placed)
    assert all(type_id.startswith("geo_basics_") for type_id in placed)

    parser_src = ""
    if hasattr(progressive, "parse_progressive_body"):
        try:
            parser_src = inspect.getsource(progressive.parse_progressive_body)
        except OSError:
            parser_src = ""
    if "scope" not in parser_src and "pairing" not in parser_src:
        return

    from question_engine.api.handler import handle_generate

    status, _, body = handle_generate(
        {
            "title": "Geometry basics unit",
            "progressive": {
                "seeds": ["geo_basics_angles_and_their_measures"],
                "count": 8,
                "d_min": 0,
                "d_max": 12,
                "include_related": True,
                "max_topics": 8,
                "scope": "unit",
                "pairing": "lesson",
                "plan_only": True,
            },
        }
    )
    assert status == 200, body
    data = json.loads(body)
    live_diffs = data["progressive"]["difficulties"]
    assert live_diffs == sorted(live_diffs)
    live_topics = [section["type_id"] for section in data["sections"]]
    assert not any(type_id in PARALLEL for type_id in live_topics)
