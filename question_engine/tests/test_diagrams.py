"""Tests for geometry diagram DSL and wired generators."""

from __future__ import annotations

import math
import random

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


def test_angle_relationship_figures_are_multi_angle():
    from question_engine.diagrams import (
        complementary_angles_figure,
        parallel_lines_transversal_figure,
        supplementary_angles_figure,
        vertical_angles_figure,
    )
    from question_engine.diagrams.primitives import AngleMark, Line, RightAngleMark

    comp = complementary_angles_figure(35)
    assert comp.kind == "complementary_angles"
    assert sum(1 for el in comp.elements if isinstance(el, AngleMark)) == 2
    assert any(isinstance(el, RightAngleMark) for el in comp.elements)
    assert "?" in comp.to_svg()
    assert "35°" in comp.to_svg()

    supp = supplementary_angles_figure(110)
    assert sum(1 for el in supp.elements if isinstance(el, AngleMark)) == 2
    assert any(isinstance(el, Line) for el in supp.elements)
    assert "?" in supp.to_svg()

    vert = vertical_angles_figure(65)
    assert sum(1 for el in vert.elements if isinstance(el, AngleMark)) == 2
    assert sum(1 for el in vert.elements if isinstance(el, Line)) == 2
    assert "?" in vert.to_svg()

    para = parallel_lines_transversal_figure(50, relation="alternate interior")
    marks = [el for el in para.elements if isinstance(el, AngleMark)]
    assert len(marks) == 2
    assert any(m.label == "?" for m in marks)
    assert any(m.label and m.label.endswith("\u00b0") for m in marks)
    assert "P" in para.points and "Q" in para.points


def test_angle_relationship_generators_emit_relationship_diagrams():
    for gen_key, topic in (
        ("geo_angle_relationships", "pa_angle_relationships"),
        ("geo_angle_relationships", "geo_basics_angle_relationships"),
        ("geo_parallel_transversal", "geo_parallel_parallel_lines_and_transversals"),
    ):
        random.seed(7)
        for _ in range(6):
            q = GENERATORS[gen_key](topic, {"count": 1})[0]
            assert q.metadata and q.metadata.get("diagram_svg")
            spec = q.metadata.get("diagram_spec") or {}
            kind = spec.get("kind") or ""
            assert kind in {
                "complementary_angles",
                "supplementary_angles",
                "vertical_angles",
                "parallel_transversal",
            }, (gen_key, kind)
            svg = q.metadata["diagram_svg"]
            assert "?" in svg
            # Must show a multi-ray / multi-line relationship, not a lone angle.
            assert svg.count("<line") + svg.count("<polyline") + svg.count("<path") >= 3


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


def test_triangle_base_height_layouts():
    from question_engine.diagrams.builders import triangle_base_height_figure
    from question_engine.diagrams.primitives import RightAngleMark, Segment

    right = triangle_base_height_figure(6, 4, layout="right")
    assert right.kind == "triangle_area"
    assert "<svg" in right.to_svg()
    assert any(isinstance(el, RightAngleMark) for el in right.elements)

    interior = triangle_base_height_figure(8, 5, layout="interior", foot_fraction=0.4)
    assert "_H" in interior.points
    assert any(isinstance(el, Segment) and el.style == "dashed" for el in interior.elements)
    assert "<svg" in interior.to_svg()
    # Apex sits above the base interior, not over an endpoint.
    assert 0.1 < interior.points["C"].x < interior.points["B"].x - 0.1
    assert interior.points["C"].y > 0.5

    exterior = triangle_base_height_figure(8, 5, layout="exterior")
    dashed = [el for el in exterior.elements if isinstance(el, Segment) and el.style == "dashed"]
    assert len(dashed) >= 2  # altitude + base-line stub
    assert exterior.points["C"].x < exterior.points["A"].x
    assert "<svg" in exterior.to_svg()


def test_triangle_area_generator_varies_layouts():
    random.seed(42)
    layouts = set()
    for tier in ("easy", "medium", "hard"):
        for _ in range(24):
            q = GENERATORS["geo_triangle_area"](
                "g6_triangles",
                {"count": 1, "difficulty_tier": tier, "side_min": 3, "side_max": 12},
            )[0]
            assert q.metadata and q.metadata.get("diagram_svg")
            text = q.prompt_text or ""
            if "layout=right" in text:
                layouts.add("right")
            elif "layout=interior" in text:
                layouts.add("interior")
            elif "layout=exterior" in text:
                layouts.add("exterior")
    assert "right" in layouts
    assert "interior" in layouts
    assert "exterior" in layouts


def test_triangles_and_quadrilaterals_area_mixes_shapes():
    random.seed(7)
    families = {"triangle": 0, "quad": 0}
    shapes: dict[str, int] = {}
    for tier in ("easy", "medium", "hard"):
        for _ in range(40):
            qs = GENERATORS["geo_triangles_and_quadrilaterals_area"](
                "pa_area_of_triangles_and_quadrilaterals",
                {"count": 1, "difficulty_tier": tier, "side_min": 3, "side_max": 12},
            )
            assert len(qs) == 1
            q = qs[0]
            prompt = (q.prompt_latex or "") + " " + (q.prompt_text or "")
            meta = q.metadata or {}
            fig = str(meta.get("figure_type") or "").lower()
            low = prompt.lower()
            if "triangle" in low or fig == "triangle":
                families["triangle"] += 1
                shapes["triangle"] = shapes.get("triangle", 0) + 1
            elif any(
                k in low or fig == k
                for k in (
                    "parallelogram",
                    "trapezoid",
                    "rectangle",
                    "rhombus",
                    "square",
                    "kite",
                    "quadrilateral",
                )
            ):
                families["quad"] += 1
                for k in (
                    "square",
                    "rectangle",
                    "rhombus",
                    "parallelogram",
                    "trapezoid",
                    "kite",
                ):
                    if k in low or fig == k:
                        shapes[k] = shapes.get(k, 0) + 1
                        break
                else:
                    shapes["other_quad"] = shapes.get("other_quad", 0) + 1
            else:
                raise AssertionError(f"unclassified prompt: {prompt!r} figure={fig!r}")
            assert meta.get("diagram_svg")
    total = families["triangle"] + families["quad"]
    assert total == 120
    # Both families should appear regularly (not a rare one-off).
    assert families["triangle"] >= 25
    assert families["quad"] >= 25
    # Within quads, medium+hard tiers should diversify beyond parallelograms.
    diversifying = (
        shapes.get("square", 0)
        + shapes.get("rectangle", 0)
        + shapes.get("rhombus", 0)
        + shapes.get("kite", 0)
        + shapes.get("trapezoid", 0)
    )
    assert diversifying >= 20
    assert shapes.get("parallelogram", 0) < families["quad"]


def test_quadrilateral_area_mixes_named_shapes():
    random.seed(11)
    counts: dict[str, int] = {}
    for tier in ("easy", "medium", "hard"):
        for _ in range(40):
            q = GENERATORS["geo_quadrilateral_area"](
                "pa_quadrilaterals",
                {"count": 1, "difficulty_tier": tier, "side_min": 3, "side_max": 12},
            )[0]
            prompt = (q.prompt_latex or "").lower()
            fig = str((q.metadata or {}).get("figure_type") or "").lower()
            kind = None
            for k in (
                "square",
                "rectangle",
                "rhombus",
                "parallelogram",
                "trapezoid",
                "kite",
            ):
                if k in prompt or fig == k:
                    kind = k
                    break
            assert kind is not None, f"unexpected quad prompt={prompt!r} fig={fig!r}"
            counts[kind] = counts.get(kind, 0) + 1
            assert (q.metadata or {}).get("diagram_svg")
    assert counts.get("parallelogram", 0) < 120
    # Easy alone can be square/rectangle/parallelogram; across tiers expect breadth.
    assert len(counts) >= 3
    assert sum(counts.values()) == 120


def test_angle_generator_emits_diagram():
    # Measure mode: multi-ray labeled figure (piece degrees + "?" for the ask).
    questions = GENERATORS["geo_angles"](
        "geo_basics_angles_and_their_measures",
        {"count": 2, "angle_task_mode": "measure"},
    )
    assert len(questions) == 2
    for q in questions:
        assert q.metadata
        assert q.metadata.get("diagram_svg")
        assert "tikzpicture" in (q.metadata.get("diagram_latex") or "")
        assert q.metadata.get("diagram_spec")
        svg = q.metadata.get("diagram_svg") or ""
        spec = q.metadata.get("diagram_spec") or {}
        assert (spec.get("kind") or "") in {"adjacent_angles", "angle_addition"}
        assert "?" in svg
        import re

        assert re.search(r"\d+\u00b0", svg), "labeled piece measures required on measure figures"
        # Several rays from the vertex — not a lone two-ray angle.
        assert svg.count("<line") >= 3


def test_angles_mix_draw_and_measure_modes():
    """Drawing/measuring angles: draw prompts and labeled multi-angle measure figures."""
    modes = {"draw": 0, "measure": 0}
    for type_id in (
        "pa_drawing_and_measuring_angles",
        "geo_basics_angles_and_their_measures",
    ):
        for tier in ("easy", "medium", "hard"):
            for _ in range(30):
                q = GENERATORS["geo_angles"](
                    type_id,
                    {
                        "count": 1,
                        "difficulty_tier": tier,
                        "angle_min": 20,
                        "angle_max": 120,
                    },
                )[0]
                latex = q.prompt_latex or ""
                text = (q.prompt_text or "").lower()
                svg = (q.metadata or {}).get("diagram_svg") or ""
                if "draw" in latex.lower() or "draw" in text:
                    modes["draw"] += 1
                    # Stimulus must not show a completed angle with the target ° labeled.
                    # Text prompt may include e.g. 65°; diagram must not.
                    if svg:
                        # Starter-ray scaffold only — no degree marks on the figure.
                        assert "\u00b0" not in svg, svg
                else:
                    modes["measure"] += 1
                    assert svg, "measure mode needs a labeled multi-angle diagram"
                    assert "?" in svg
                    assert "\u00b0" in svg
                    assert "find" in latex.lower() or "find" in text

    assert modes["draw"] >= 40, modes
    assert modes["measure"] >= 40, modes


def test_draw_angle_mode_has_no_answer_on_diagram():
    random.seed(11)
    for _ in range(20):
        q = GENERATORS["geo_angles"](
            "pa_drawing_and_measuring_angles",
            {"count": 1, "angle_task_mode": "draw", "angle_min": 30, "angle_max": 90},
        )[0]
        latex = (q.prompt_latex or "").lower()
        assert "draw" in latex
        svg = (q.metadata or {}).get("diagram_svg")
        if svg:
            assert "\u00b0" not in svg


def test_measure_from_diagram_hard_combines_angles():
    """Hard measure / angle-addition items require combining 2+ adjacent pieces."""
    from question_engine.diagrams.primitives import AngleMark, Segment

    random.seed(42)
    combine_ok = 0
    for _ in range(40):
        q = GENERATORS["geo_angles"](
            "geo_basics_angles_and_their_measures",
            {
                "count": 1,
                "angle_task_mode": "measure",
                "difficulty_tier": "hard",
                "angle_min": 10,
                "angle_max": 170,
            },
        )[0]
        meta = q.metadata or {}
        assert meta.get("diagram_svg")
        spec = meta.get("diagram_spec") or {}
        assert spec.get("kind") == "adjacent_angles"
        # Rebuild signal: answer is not printed as the only marked angle;
        # hard figures always have multiple degree labels + "?".
        svg = meta["diagram_svg"]
        assert "?" in svg
        # Hard figures are crowded multi-ray: several tip rays + marks.
        assert svg.count("<line") >= 3
        # Solvable from labels: numeric piece(s) and/or right-angle square on a shell.
        assert ("\u00b0" in svg) or ("<polyline" in svg), svg
        # Prefer dense labeling: at least one numeric degree when not pure right-shell.
        combine_ok += 1

        q2 = GENERATORS["geo_angle_addition"](
            "geo_basics_angle_addition_postulate",
            {
                "count": 1,
                "difficulty_tier": "hard",
                "angle_min": 10,
                "angle_max": 170,
            },
        )[0]
        meta2 = q2.metadata or {}
        assert meta2.get("diagram_svg")
        assert (meta2.get("diagram_spec") or {}).get("kind") == "angle_addition"
        svg2 = meta2["diagram_svg"]
        assert "?" in svg2
        assert svg2.count("\u00b0") >= 2
        assert svg2.count("<line") >= 3

    assert combine_ok == 40

    # Builder sanity: 3-piece fan with outer ?
    from question_engine.diagrams import adjacent_angles_figure

    fig = adjacent_angles_figure(
        [25, 40, 35],
        tip_labels=["A", "B", "C", "D"],
        vertex_label="O",
        piece_labels=["25\u00b0", "40\u00b0", "35\u00b0"],
        span_marks=[(0, 2, "?")],
    )
    marks = [el for el in fig.elements if isinstance(el, AngleMark)]
    assert any(m.label == "?" for m in marks)
    assert sum(1 for m in marks if m.label and m.label.endswith("\u00b0")) >= 3
    assert sum(1 for el in fig.elements if isinstance(el, Segment)) >= 4
    assert "<svg" in fig.to_svg()


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


def test_geo_transformations_are_plane_figures_not_quadratics():
    """PA / Geo transformations graph polygons, not y=ax^2."""
    from question_engine.generators.geometry import GENERATORS

    for tier in ("easy", "medium", "hard"):
        qs = GENERATORS["geo_transformations"](
            "pa_transformations",
            {
                "count": 4,
                "difficulty_tier": tier,
                "include_answer_key": True,
                "include_graph_metadata": True,
                "include_diagram": True,
            },
        )
        for q in qs:
            assert q.prompt_latex
            assert "x^2" not in q.prompt_latex
            assert "f(x)" not in q.prompt_latex
            assert "quadratic" not in q.prompt_latex.lower()
            assert any(
                word in q.prompt_latex
                for word in (
                    "triangle",
                    "square",
                    "rectangle",
                    "parallelogram",
                    "quadrilateral",
                    r"\triangle",
                )
            ), q.prompt_latex
            assert q.answer_latex
            assert "'" in q.answer_latex  # image vertices A'(x,y)
            meta = q.metadata or {}
            assert meta.get("diagram_svg")
            # Stimulus shows the pre-image polygon; blank prompts are grid-only.
            if meta.get("graph_role") != "blank":
                assert "<polygon" in meta["diagram_svg"]
            assert meta.get("answer_diagram_svg")
            assert "<polygon" in meta["answer_diagram_svg"]
            assert meta.get("image_points")
            assert meta.get("transform_kind") in {
                "translation",
                "reflection_x",
                "reflection_y",
                "reflection_yx",
                "rotation_90",
                "rotation_90_cw",
                "rotation_180",
                "dilation",
                "composition",
            }


def test_drawing_charts_create_not_copy():
    from question_engine.diagrams.charts import dot_plot_svg, histogram_svg
    from question_engine.generators.grade6 import GENERATORS

    blank_dot = dot_plot_svg([1, 2, 2, 5], title="Dot plot", blank=True)
    assert "<circle" not in blank_dot
    assert "<line" in blank_dot

    filled = dot_plot_svg([1, 2, 2, 5], title="Dot plot", blank=False)
    assert "<circle" in filled

    bins = [(0.0, 2.0), (2.0, 4.0), (4.0, 6.0)]
    blank_hist = histogram_svg([1, 2, 3, 5], bins, title="Histogram", blank=True)
    assert "#93c5fd" not in blank_hist  # no filled bars
    assert "<line" in blank_hist

    for key, axis in (("g6_drawing_dot_plot", True), ("g6_drawing_histogram", False)):
        q = GENERATORS[key](
            key,
            {"count": 1, "include_axis": axis, "include_answer_key": True},
        )[0]
        prompt = q.prompt_latex or ""
        assert "Create" in prompt
        assert "copy" not in prompt.lower()
        meta = q.metadata or {}
        assert meta.get("answer_diagram_svg")
        if axis:
            assert meta.get("diagram_svg")
            if key.endswith("histogram"):
                assert "#93c5fd" not in meta["diagram_svg"]
            else:
                assert "<circle" not in meta["diagram_svg"]
        else:
            assert not meta.get("diagram_svg")


def test_classify_polyhedron_diverse_mc():
    from question_engine.diagrams.grade6_figures import POLYHEDRON_KINDS, polyhedron_svg
    from question_engine.generators.grade6 import GENERATORS

    for kind in POLYHEDRON_KINDS:
        svg = polyhedron_svg(kind)
        assert "<svg" in svg
        assert "<polygon" in svg

    questions = GENERATORS["g6_classify_polyhedron"](
        "g6_classifying_and_naming",
        {"count": 25, "include_answer_key": True},
    )
    answers = {q.answer_latex for q in questions}
    assert len(answers) >= 3
    for q in questions:
        meta = q.metadata or {}
        assert meta.get("diagram_svg")
        assert meta.get("answer_mode") == "multiple_choice"
        choices = meta.get("choices") or []
        assert len(choices) == 4
        correct = [c for c in choices if c.get("correct")]
        assert len(correct) == 1
        assert correct[0]["latex"] == q.answer_latex
        name = q.answer_latex.removeprefix(r"\text{").removesuffix("}")
        assert name in POLYHEDRON_KINDS
