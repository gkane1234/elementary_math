"""Tests for geometry diagram DSL and wired generators."""

from __future__ import annotations

from question_engine.diagram_readiness import type_requires_diagram
from question_engine.diagrams import (
    GeometryFigure,
    Point,
    Polygon,
    Segment,
    angle_figure,
    circle_figure,
    polygon_figure,
    triangle_figure,
)
from question_engine.generators.geometry import GENERATORS


def test_arbitrary_polygon_emits_svg_and_tikz():
    fig = polygon_figure(
        [("A", 0, 0), ("B", 2, 0), ("C", 2.5, 1.2), ("D", 0.4, 1.8)],
    )
    meta = fig.to_metadata()
    assert "diagram_svg" in meta
    assert "<svg" in meta["diagram_svg"]
    assert "tikzpicture" in meta["diagram_latex"]
    assert meta["diagram_spec"]["kind"] == "polygon"


def test_custom_figure_compose():
    fig = GeometryFigure(kind="custom")
    fig.add_point(Point("P", 0, 0, label="P"))
    fig.add_point(Point("Q", 1, 0, label="Q"))
    fig.add_point(Point("R", 0.5, 1, label="R"))
    fig.add(Polygon(["P", "Q", "R"]), Segment("P", "Q"))
    svg = fig.to_svg()
    assert "polygon" in svg or "polyline" in svg


def test_builders_produce_nonempty_svg():
    assert "<svg" in angle_figure("A", "B", "C", 55).to_svg()
    assert "<svg" in triangle_figure(["A", "B", "C"], [40, 60, 80], missing="C").to_svg()
    assert "<svg" in circle_figure(6).to_svg()


def test_angle_generator_emits_diagram():
    questions = GENERATORS["geo_angles"]("geo_basics_angles_and_their_measures", {"count": 2})
    assert len(questions) == 2
    for q in questions:
        assert q.metadata
        assert q.metadata.get("diagram_svg")
        assert "tikzpicture" in (q.metadata.get("diagram_latex") or "")
        assert q.metadata.get("diagram_spec")


def test_triangle_and_circle_generators_emit_diagram():
    tri = GENERATORS["geo_triangle_angle_sum"](
        "geo_congruent_triangle_angle_sum", {"count": 1}
    )[0]
    circ = GENERATORS["geo_circle_measure"](
        "geo_circles_circumference_and_area", {"count": 1}
    )[0]
    assert tri.metadata and tri.metadata.get("diagram_svg")
    assert circ.metadata and circ.metadata.get("diagram_svg")


def test_reenabled_types_not_demoted():
    for tid in (
        "geo_basics_angles_and_their_measures",
        "geo_basics_classifying_angles",
        "geo_congruent_triangle_angle_sum",
        "geo_circles_circumference_and_area",
    ):
        assert not type_requires_diagram(tid), tid
