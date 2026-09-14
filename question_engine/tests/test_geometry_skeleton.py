"""G6 GeometryMeasure: plot/identify, axis distance, shaded composite, wraps."""

from __future__ import annotations

import random
import re

from question_engine.api.handler import _generate_for_type
from question_engine.diagrams.grade6_figures import (
    coordinate_points_svg,
    shaded_composite_svg,
)
from question_engine.frameworks.primitives.geometry_skeleton import (
    PATTERN,
    sample_axis_aligned_distance,
    sample_plot_or_identify_point,
    sample_shaded_composite,
)


def _q(type_id: str, d: float, seed: int = 101, extra: dict | None = None):
    settings = {
        "difficulty": d,
        "seed": seed,
        "count": 1,
        "include_answer_key": True,
        **(extra or {}),
    }
    qs = _generate_for_type(type_id, settings)
    assert qs, (type_id, d, seed)
    return qs[0]


def _pat(q) -> str:
    return str((q.metadata or {}).get("skeleton_pattern") or "")


def test_coordinate_points_svg_plot_and_identify():
    blank = coordinate_points_svg([(3, 2)], labels=["A"], blank=True)
    shown = coordinate_points_svg([(3, 2)], labels=["A"], blank=False)
    assert "<svg" in blank and "<svg" in shown
    assert "A" not in blank
    assert "A" in shown
    seg = coordinate_points_svg([(1, 2), (4, 2)], labels=["A", "B"], segment=True)
    assert "<line" in seg and "A" in seg and "B" in seg


def test_shaded_composite_svg_has_cutout():
    svg = shaded_composite_svg(
        [(1, 1), (6, 1), (6, 4), (1, 4)],
        [(2, 2), (5, 2), (5, 3), (2, 3)],
    )
    assert "<svg" in svg
    assert "evenodd" in svg


def test_points_not_identity_dump():
    q = _q("g6_points_on_the_coordinate_plane", 0.0)
    assert _pat(q) == PATTERN
    prompt = q.prompt_latex or ""
    assert prompt.strip() != (q.answer_latex or "").strip()
    assert "Plot the point" in prompt or "coordinates of point" in prompt
    assert (q.metadata or {}).get("diagram_svg")
    assert "<svg" in str((q.metadata or {}).get("diagram_svg"))


def test_points_opt_out_restores_dump():
    q = _q(
        "g6_points_on_the_coordinate_plane",
        0.0,
        extra={"use_legacy_geometry": True},
    )
    assert _pat(q) != PATTERN
    prompt = (q.prompt_latex or "").strip()
    answer = (q.answer_latex or "").strip()
    assert prompt == answer
    assert re.match(r"^\(.*\)$", prompt)


def test_pa_plotting_points_not_hijacked():
    q = _q("pa_plotting_points", 0.0)
    assert _pat(q) != PATTERN
    prompt = (q.prompt_latex or "").strip()
    answer = (q.answer_latex or "").strip()
    assert prompt == answer


def test_distances_d0_horizontal_and_vertical_unlock():
    q0 = _q("g6_distances_on_the_coordinate_plane", 0.0)
    assert _pat(q0) == PATTERN
    assert (q0.metadata or {}).get("axis") == "horizontal"
    assert (q0.metadata or {}).get("diagram_svg")
    prompt = q0.prompt_latex or ""
    assert "Find the distance between" in prompt

    axes = set()
    for seed in range(101, 121):
        q = _q("g6_distances_on_the_coordinate_plane", 16.0, seed=seed)
        axes.add((q.metadata or {}).get("axis"))
    assert "horizontal" in axes
    assert "vertical" in axes


def test_shaded_is_outer_minus_inner():
    q = _q("g6_polygons_and_shaded_regions", 0.0)
    assert _pat(q) == PATTERN
    prompt = q.prompt_latex or ""
    assert "shaded region" in prompt
    assert "shaded triangle" not in prompt
    kind = (q.metadata or {}).get("shape_kind") or (q.metadata or {}).get("construction")
    assert kind in {"rect_minus_triangle", "frame", "l_cut"}
    assert "evenodd" in str((q.metadata or {}).get("diagram_svg") or "")


def test_grid_polygon_wraps_old_shapes():
    q = _q("g6_polygons_on_a_grid_or_coordinate_plane", 0.0)
    assert _pat(q) == PATTERN
    assert "on the grid" in (q.prompt_latex or "")
    assert (q.metadata or {}).get("diagram_svg")


def test_parallelogram_and_understanding():
    area = _q("g6_parallelograms", 0.0)
    assert _pat(area) == PATTERN
    assert "Find the area of the parallelogram" in (area.prompt_latex or "")
    assert (area.metadata or {}).get("diagram_svg")

    missing = _q("g6_parallelograms_understanding_area_formula", 22.0, seed=101)
    assert _pat(missing) == PATTERN
    blob = missing.prompt_latex or ""
    assert "Find the area" in blob or "Find the height" in blob or "Find the base" in blob


def test_triangle_trapezoid_fraction_cube():
    tri = _q("g6_triangles", 0.0)
    assert "triangle" in (tri.prompt_latex or "").lower() or "triangle" in (
        tri.prompt_text or ""
    ).lower()
    trap = _q("g6_trapezoids", 0.0)
    assert "trapezoid" in (trap.prompt_latex or "")
    rect = _q("g6_rectangles_with_fraction_side_lengths", 0.0)
    assert r"\frac" in (rect.prompt_latex or "")
    cube = _q("g6_formulas_for_volume_and_surface_area_of_a_cube", 0.0)
    assert "cube" in (cube.prompt_latex or "")
    assert _pat(tri) == _pat(trap) == _pat(rect) == _pat(cube) == PATTERN


def test_classify_and_isometric_and_kite_stamp():
    cls = _q("g6_classifying_and_naming", 0.0)
    assert _pat(cls) == PATTERN
    assert "Classify the polyhedron" in (cls.prompt_latex or "")
    iso = _q("g6_volume_and_surface_area_using_isometric_drawings", 0.0)
    assert _pat(iso) == PATTERN
    assert "Use the drawing" in (iso.prompt_latex or "")
    kite = _q("g6_kites", 0.0)
    assert _pat(kite) == PATTERN
    assert "kite" in (kite.prompt_latex or "")


def test_perimeter_has_vertices_and_svg():
    q = _q("g6_shapes_and_perimeter_on_the_coordinate_plane", 0.0)
    assert _pat(q) == PATTERN
    assert "Find the perimeter" in (q.prompt_latex or "")
    assert (q.metadata or {}).get("diagram_svg")


def test_sample_helpers_stable_under_seed():
    random.seed(7)
    a = sample_plot_or_identify_point({"difficulty": 0})
    random.seed(7)
    b = sample_plot_or_identify_point({"difficulty": 0})
    assert a.prompt_latex == b.prompt_latex
    random.seed(11)
    d0 = sample_axis_aligned_distance({"difficulty": 0})
    assert d0.metadata.get("axis") == "horizontal"
    random.seed(3)
    sh = sample_shaded_composite({"difficulty": 0})
    assert sh.construction in {"rect_minus_triangle", "frame"}
