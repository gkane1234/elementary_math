"""Tests for geometry diagram DSL and wired generators."""

from __future__ import annotations

import math

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
from question_engine.diagrams.builders import rectangle_figure, right_triangle_figure
from question_engine.diagrams.primitives import Label
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


def test_side_length_labels_offset_outward():
    """Side lengths sit outside the stroke, not on the edge midpoint."""
    fig = triangle_figure(
        ["A", "B", "C"],
        [40, 60, 80],
        side_labels={"AB": "5 cm", "BC": "4 cm", "CA": "3 cm"},
    )
    pts = {pid: (p.x, p.y) for pid, p in fig.points.items()}
    cx = sum(x for x, _ in pts.values()) / 3
    cy = sum(y for _, y in pts.values()) / 3
    labels = {el.text: el for el in fig.elements if isinstance(el, Label)}

    def assert_outward(key: str, text: str) -> None:
        p, q = key[0], key[1]
        mx = (pts[p][0] + pts[q][0]) / 2
        my = (pts[p][1] + pts[q][1]) / 2
        lab = labels[text]
        # Label must leave the midpoint toward the exterior (away from centroid).
        outward = (mx - cx) * (lab.x - mx) + (my - cy) * (lab.y - my)
        assert outward > 0.05, (key, text, lab.x, lab.y, mx, my)
        assert math.hypot(lab.x - mx, lab.y - my) >= 0.4

    assert_outward("AB", "5 cm")
    assert_outward("BC", "4 cm")
    assert_outward("CA", "3 cm")

    rect = rectangle_figure(8, 5)
    rlabels = [el for el in rect.elements if isinstance(el, Label)]
    assert len(rlabels) == 2
    # Width below base (y < 0); height to the right of right side (x > width draw).
    width_lab = next(el for el in rlabels if el.text.startswith("8"))
    height_lab = next(el for el in rlabels if el.text.startswith("5"))
    assert width_lab.y < -0.3
    assert height_lab.x > rect.points["B"].x + 0.3

    rt = right_triangle_figure(
        3,
        4,
        side_labels={"AB": "5", "BC": "3", "CA": "4"},
    )
    rt_pts = {pid: (p.x, p.y) for pid, p in rt.points.items()}
    rcx = sum(x for x, _ in rt_pts.values()) / 3
    rcy = sum(y for _, y in rt_pts.values()) / 3
    for el in rt.elements:
        if not isinstance(el, Label):
            continue
        # Every side label is outside relative to the triangle centroid.
        # Find nearest edge midpoint among AB/BC/CA.
        best = None
        for u, v in (("A", "B"), ("B", "C"), ("C", "A")):
            mx = (rt_pts[u][0] + rt_pts[v][0]) / 2
            my = (rt_pts[u][1] + rt_pts[v][1]) / 2
            dist = math.hypot(el.x - mx, el.y - my)
            if best is None or dist < best[0]:
                best = (dist, mx, my)
        assert best is not None
        _, mx, my = best
        assert (mx - rcx) * (el.x - mx) + (my - rcy) * (el.y - my) > 0.05


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
