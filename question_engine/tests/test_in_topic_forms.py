"""Same-skill forms that a single-topic set must be able to ask."""

from __future__ import annotations

from question_engine.api.handler import _generate_for_type


def _batch(type_id: str, difficulty: float, *, count: int = 12, seed: int = 101):
    return _generate_for_type(
        type_id,
        {
            "difficulty": difficulty,
            "seed": seed,
            "count": count,
            "include_answer_key": True,
            "include_diagram": True,
        },
    )


def _blob(q) -> str:
    return ((q.prompt_latex or "") + " " + (q.prompt_text or "")).lower()


def test_fraction_rectangle_has_area_missing_side_and_equation():
    qs = _batch("g6_rectangles_with_fraction_side_lengths", 0.0) + _batch(
        "g6_rectangles_with_fraction_side_lengths", 16.0, seed=207
    )
    blobs = [_blob(q) for q in qs]
    assert any("find the area" in b for b in blobs)
    assert any("find the height" in b or "find the base" in b for b in blobs)
    assert any("which equation relates" in b for b in blobs)
    assert all("hose" not in b and "gallon" not in b for b in blobs)
    assert all("how many groups" not in b for b in blobs)


def test_fraction_triangle_has_the_same_area_forms():
    qs = _batch("g6_triangles_with_fraction_side_lengths", 0.0)
    blobs = [_blob(q) for q in qs]
    assert any("find the area" in b for b in blobs)
    assert any("find the height" in b or "find the base" in b for b in blobs)
    assert any("which equation relates" in b for b in blobs)


def test_hanger_selects_and_writes_the_equation():
    qs = _batch("g6_equations_hanger_diagrams", 0.0)
    blobs = [_blob(q) for q in qs]
    assert any("which equation matches the hanger" in b for b in blobs)
    assert any("write the equation shown" in b for b in blobs)
    assert any("solve for" in b for b in blobs)
    # The select / write stems do not hand the student the equation to solve.
    for q in qs:
        form = (q.metadata or {}).get("question_form")
        if form in {"select_equation", "write_equation"}:
            assert "solve" not in _blob(q)


def test_dividing_fractions_groups_and_related_quotient():
    qs = _batch("g6_dividing_fractions", 0.0) + _batch(
        "g6_dividing_fractions", 16.0, seed=19
    )
    blobs = [_blob(q) for q in qs]
    assert any("how many groups" in b for b in blobs)
    assert any("you know that" in b for b in blobs)
    assert any("\\div" in (q.prompt_latex or "") for q in qs)
    assert all("mile" not in b and "gallon" not in b and "hour" not in b for b in blobs)


def test_absolute_value_plots_and_orders():
    for type_id in (
        "g6_absolute_values",
        "g6_comparing_with_absolute_values",
        "g6_ordering_with_absolute_values",
    ):
        qs = _batch(type_id, 0.0, count=8, seed=5)
        blobs = [_blob(q) for q in qs]
        assert any("plot all numbers" in b for b in blobs), type_id
    order_qs = _batch("g6_absolute_values", 8.0, count=9, seed=4)
    assert any("order from least" in _blob(q) for q in order_qs)


def test_one_step_can_check_a_solution():
    qs = _batch("one_step_equations", 0.0, count=9, seed=2)
    checks = [q for q in qs if "a solution of" in _blob(q)]
    assert checks
    assert all((q.metadata or {}).get("steps") == "one" for q in qs)
    assert any((q.answer_latex or "").endswith("yes}") or "yes" in (q.answer_latex or "") for q in checks)
    assert any("no" in (q.answer_latex or "") for q in checks)


def test_more_on_slope_includes_two_points():
    qs = _batch("more_on_slope", 0.0, count=9, seed=3) + _batch(
        "more_on_slope", 16.0, count=9, seed=4
    )
    blobs = [_blob(q) for q in qs]
    assert any("through" in b for b in blobs)
    assert any("parallel" in b or "perpendicular" in b for b in blobs)


def test_quotient_product_and_power_have_point_forms():
    power = _batch("calc_diff_power_rule", 0.0, count=8, seed=1) + _batch(
        "pc_power_rule_for_differentiation", 16.0, count=8, seed=1
    )
    assert any("f'" in (q.prompt_latex or "") and "for" in _blob(q) for q in power)
    product = _batch("calc_diff_product_rule", 4.0, count=8, seed=1)
    assert any("f(x)" in (q.prompt_latex or "") and "g(x)" in (q.prompt_latex or "") for q in product)
    quotient = _batch("calc_diff_quotient_rule", 0.0, count=12, seed=1)
    blobs = [q.prompt_latex or "" for q in quotient]
    assert any("f'" in p and "dfrac" in p for p in blobs)
    assert any("f(x)" in p and "g(x)" in p for p in blobs)


def test_related_rates_y_of_x():
    qs = _batch("calc_app_diff_related_rates", 0.0, count=8, seed=2) + _batch(
        "calc_app_diff_related_rates", 16.0, count=8, seed=2
    )
    assert any("dy" in (q.prompt_latex or "") and "dx" in (q.prompt_latex or "") for q in qs)


def test_congruence_can_decide():
    qs = _batch("geo_congruent_proving_triangles_congruent", 0.0, count=9, seed=1)
    blobs = [_blob(q) for q in qs]
    assert any("are the triangles congruent" in b or "necessarily congruent" in b for b in blobs)
    assert any("theorem" in b for b in blobs)


def test_trapezoid_missing_side():
    qs = _batch("geo_quadrilaterals_trapezoids", 0.0, count=9, seed=1)
    blobs = [_blob(q) for q in qs]
    assert any("find the area" in b for b in blobs)
    assert any("find the height" in b or "find the other base" in b for b in blobs)


def test_triangle_area_formula_missing_side():
    qs = _batch("g6_triangles_understanding_area_formula", 0.0, count=8, seed=1)
    blobs = [_blob(q) for q in qs]
    assert any("find the height" in b or "find the base" in b for b in blobs)
    assert any("find the area" in b for b in blobs)


def test_box_dot_histogram_missing_forms():
    boxes = _batch("g6_drawing_box_plots", 0.0, count=10, seed=1) + _batch(
        "g6_interpreting_box_plots", 8.0, count=10, seed=2
    )
    box_blobs = [_blob(q) for q in boxes]
    assert any("maximum" in b for b in box_blobs)
    assert any("create a box plot" in b for b in box_blobs)
    dots = _batch("g6_drawing_dot_plots", 0.0, count=8, seed=1) + _batch(
        "g6_interpreting_dot_plots", 4.0, count=8, seed=1
    )
    dot_blobs = [_blob(q) for q in dots]
    assert any("same dot plot" in b for b in dot_blobs)
    assert any("create a dot plot" in b for b in dot_blobs)
    hists = _batch("g6_drawing_histograms", 0.0, count=8, seed=1) + _batch(
        "g6_interpreting_histograms", 4.0, count=8, seed=1
    )
    hist_blobs = [_blob(q) for q in hists]
    assert any("same dot plot as a histogram" in b for b in hist_blobs)
    assert any("create a histogram" in b for b in hist_blobs)


def test_off_topic_same_skill_forms():
    divs = _batch("g6_long_division_with_remainders", 0.0, count=9, seed=1)
    assert any("which place" in _blob(q) for q in divs)
    assert any("r" in (q.answer_latex or "").lower() for q in divs)
    rates = _batch("g6_constant_rate_equations", 0.0, count=9, seed=1)
    assert any("complete the distances" in _blob(q) for q in rates)
    assert any("write an equation" in _blob(q) for q in rates)
    conv = _batch("pa_converting_fractions_and_decimals", 0.0, count=9, seed=1)
    assert any("overline" in (q.prompt_latex or "") for q in conv)
    assert any("as a decimal" in _blob(q) or "as a fraction" in _blob(q) for q in conv)


def test_ftc_companion_forms():
    first = _batch(
        "calc_def_int_first_fundamental_theorem_of_calculus", 0.0, count=16, seed=3
    ) + _batch(
        "calc_def_int_first_fundamental_theorem_of_calculus", 16.0, count=16, seed=3
    )
    fids = {(q.metadata or {}).get("form_id") for q in first}
    assert fids & {"ftc1_at_point", "ftc1_deriv"}
    assert any(r"\int_" in (q.prompt_latex or "") and "F'" not in (q.prompt_latex or "") for q in first)
    second = _batch(
        "calc_def_int_second_fundamental_theorem_of_calculus", 0.0, count=16, seed=3
    )
    sids = {(q.metadata or {}).get("form_id") for q in second}
    assert sids & {"ftc2_at_point", "ftc2_integrate"}
