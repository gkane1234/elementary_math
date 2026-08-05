"""Tests for geo / stats / variation / graphing effort scorers."""

from __future__ import annotations

from question_engine.ml.effort import has_effort_scorer, score_effort
from question_engine.ml.effort_geo import (
    GEO_STATS_SCORERS,
    effort_box_plot_read,
    effort_calc_tangent_line,
    effort_center_spread,
    effort_circle_measure,
    effort_classify_angles,
    effort_construction,
    effort_decimal_ops,
    effort_finding_angles,
    effort_g6_fraction_measure,
    effort_g6_grid_polygon,
    effort_g6_isometric,
    effort_graph_linear,
    effort_pythagorean,
    effort_scatter_plot,
    effort_sets_of_numbers,
    effort_variation,
)


def test_geo_stats_scorers_registered():
    for tid in GEO_STATS_SCORERS:
        assert has_effort_scorer(tid), tid


def test_classify_angles_ramp():
    e_acute, _ = effort_classify_angles("Classify", "acute")
    e_obtuse, _ = effort_classify_angles("Classify", "obtuse")
    e_straight, _ = effort_classify_angles("Classify", "straight")
    assert e_acute < e_obtuse <= e_straight


def test_finding_angles_more_exprs_harder():
    easy = r"Find x. Supplementary: (x)^\circ and 40^\circ"
    hard = (
        r"In \triangle ABC, m\angle A = (2x+1)^\circ, "
        r"m\angle B = (3x)^\circ, m\angle C = (x+5)^\circ"
    )
    e0, _ = effort_finding_angles(easy, "40")
    e1, _ = effort_finding_angles(hard, "20")
    assert e1 > e0


def test_sets_and_variation_and_stats():
    e_set, f_set = effort_sets_of_numbers(r"\sqrt{2}", r"\text{irrational, real}")
    assert e_set >= 4.0
    assert f_set.get("irrational_present")
    e_inv, f_inv = effort_variation(
        r"If y varies inversely with x and y = 3 when x = 4, write the equation.",
        r"y = \frac{12}{x}",
    )
    e_dir, _ = effort_variation(r"Write a direct variation equation with k = 4.", r"y = 4x")
    assert e_inv > e_dir
    assert f_inv.get("kind") == "inverse"
    e_mean, f_mean = effort_center_spread(
        r"Find the mean of the data set: \{1,\ 2,\ 3,\ 4,\ 5,\ 6,\ 7\}.",
        "4",
    )
    e_range, _ = effort_center_spread(
        r"Find the range of the data set: \{1,\ 2,\ 3\}.",
        "2",
    )
    assert e_mean > e_range
    assert f_mean.get("measure") == "mean"
    e_iqr, _ = effort_box_plot_read(r"From the box plot, find the interquartile range.", "5")
    e_med, _ = effort_box_plot_read(r"From the box plot, find the median.", "3")
    assert e_iqr > e_med


def test_graph_linear_inequality_premium():
    e_eq, _ = effort_graph_linear(r"\text{Graph: } y = 2x + 1", "y = 2x + 1")
    e_ineq, f = effort_graph_linear(r"\text{Graph the inequality: } y \ge 2x", "y \\ge 2x")
    assert e_ineq > e_eq
    assert f.get("inequality")


def test_circle_decimal_pythag_ramp():
    e_c, _ = effort_circle_measure(
        r"\text{Find the circumference of a circle with radius } 7\text{ cm}.",
        r"14\pi",
    )
    e_s, f = effort_circle_measure(
        r"\text{A circle has radius } 8\text{ cm} \text{ and a central angle of } 60^\circ."
        r"\ \text{Find the sector area.}",
        r"\frac{60}{360}\pi 8^{2}",
    )
    assert e_s > e_c
    assert f.get("ask") == "sector"
    e_add, _ = effort_decimal_ops("1.2 + 3.4", "4.6")
    e_div, fd = effort_decimal_ops(r"12.5 \div 0.5", "25")
    assert e_div > e_add
    assert fd.get("op") == "div"
    e_py, _ = effort_pythagorean(r"In right triangle find BC.", "5")
    e_3060, _ = effort_pythagorean(r"In a 30-60-90 triangle, find the long leg.", r"5\sqrt{3}")
    assert e_3060 > e_py


def test_calc_tangent_scorer_and_live_score():
    e, f = effort_calc_tangent_line(
        r"\text{Find the normal line to }y=x^{2}\text{ at }x=3.",
        r"y-9=-\frac{1}{6}(x-3)",
    )
    assert e >= 8.0
    assert f.get("normal")
    scored, feats = score_effort(
        "calc_app_diff_slope_tangent_and_normal_lines",
        r"\text{Find the tangent line to }y=\sin(x)\text{ at }x=0.",
        "y=x",
    )
    assert scored is not None and scored > 8.0
    assert feats.get("trig")


def test_live_generate_scores_geo_and_stats():
    import question_engine.generators  # noqa: F401
    from question_engine.core.base import QUESTION_TYPES

    for tid in (
        "geo_basics_classifying_angles",
        "geo_circles_circumference_and_area",
        "geo_parallel_parallel_lines_and_transversals",
        "geo_right_pythagorean_theorem",
        "sets_of_numbers",
        "direct_inverse_variation",
        "center_and_spread",
        "g6_interpreting_box_plots",
        "g6_decimal_addition",
        "g6_parallelograms",
        "geo_constructions_altitudes_of_a_triangle",
        "geo_basics_geometric_diagrams_and_notation",
        "g6_rectangles_with_fraction_side_lengths",
        "g6_polygons_and_shaded_regions",
        "g6_volume_and_surface_area_using_isometric_drawings",
        "scatter_plots",
        "visualizing_data",
    ):
        qt = QUESTION_TYPES[tid]
        qs = qt.generate({"count": 3, "seed": 9, "difficulty": 10, "include_answer_key": True})
        for q in qs:
            e, _ = score_effort(tid, q.prompt_latex or "", q.answer_latex or "")
            assert e is not None and e > 0, tid


def test_construction_and_fraction_measure_ramps():
    e_seg, f_seg = effort_construction(
        r"\text{Identify the result of the standard construction shown: } a segment congruent to the given segment.",
        "segment congruent to the given segment",
    )
    e_alt, f_alt = effort_construction(
        r"\text{Identify the result of the standard construction shown: } an altitude.",
        "an altitude",
    )
    assert e_alt > e_seg
    assert f_alt.get("kind") == "altitude"
    assert f_seg.get("kind") == "segment"

    e_rect, _ = effort_g6_fraction_measure(
        r"\text{Find the area of the rectangle with base } 1\text{ in} \text{ and height } 1\text{ in}.",
        r"1\text{ in}^{2}",
    )
    e_prism, f_prism = effort_g6_fraction_measure(
        r"\text{Find the volume of the right rectangular prism with side lengths } "
        r"\frac{5}{6}\text{ cm},\ 2\text{ cm},\ \frac{1}{2}\text{ cm}.",
        r"\frac{5}{6}\text{ cm}^{3}",
    )
    assert e_prism > e_rect
    assert f_prism.get("shape") == "prism"

    e_sq, _ = effort_g6_grid_polygon(
        r"\text{Find the area of the square on the grid.}",
        r"4\text{ square units}",
    )
    e_l, f_l = effort_g6_grid_polygon(
        r"\text{Find the area of the shaded L-shaped polygon on the grid.}",
        r"\frac{15}{2}\text{ square units}",
    )
    assert e_l > e_sq
    assert f_l.get("shaded") and f_l.get("half_unit")

    e_vol, _ = effort_g6_isometric(r"\text{Use the drawing to find the volume.}", r"12\text{ cubic units}")
    e_sa, f_sa = effort_g6_isometric(
        r"\text{Use the drawing to find the surface area.}",
        r"32\text{ square units}",
    )
    assert e_sa > e_vol
    assert f_sa.get("ask") == "surface_area"

    e_assoc, _ = effort_scatter_plot(
        r"\text{A scatter plot shows a positive linear trend. What type of association is this?}",
        r"\text{positive association}",
    )
    e_pred, f_pred = effort_scatter_plot(
        r"\text{A linear model for a scatter plot is } y = 4x + 14. \text{Predict } y \text{ when } x = 4.",
        "30",
    )
    assert e_pred > e_assoc
    assert f_pred.get("task") == "predict"
