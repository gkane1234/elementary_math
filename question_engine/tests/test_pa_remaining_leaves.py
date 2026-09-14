"""Live-path smoke for remaining PA catalog leaves (not already on eq/ineq skeletons)."""

from __future__ import annotations

from question_engine.api.handler import _generate_for_type
from question_engine.frameworks.primitives.wp_packaging import looks_like_dumped_equation


def _q(type_id: str, d: float, seed: int = 101, extra: dict | None = None):
    settings = {
        "difficulty": d,
        "seed": seed,
        "count": 1,
        "include_answer_key": True,
        "integers_only": True,
        "only_x": True,
        **(extra or {}),
    }
    qs = _generate_for_type(type_id, settings)
    assert qs, (type_id, d, seed)
    return qs[0]


def _pat(q) -> str:
    return str((q.metadata or {}).get("skeleton_pattern") or "")


def test_pa_number_leaves_stamp_numberop():
    for type_id in (
        "pa_naming_decimal_places_and_rounding",
        "pa_writing_numbers_with_words",
        "pa_integers_adding_and_subtracting",
        "pa_integers_multiplying",
        "pa_simplifying_fractions",
        "pa_fractions_add_like",
        "pa_squares_and_square_roots",
        "pa_fractions_decimals_and_percents",
        "pa_divisibility",
        "pa_factoring",
        "pa_greatest_common_factor",
        "pa_least_common_multiple",
    ):
        q = _q(type_id, 0.0)
        assert q.prompt_latex, type_id
        assert q.answer_latex, type_id
        assert _pat(q) == "NumberOp", (type_id, _pat(q))


def test_pa_markup_is_retail_story():
    seen = set()
    for seed in range(20):
        q = _q("pa_markup_discount_and_tax", 0.0, seed)
        prompt = (q.prompt_latex or "") + " " + (q.prompt_text or "")
        assert not looks_like_dumped_equation(prompt), prompt
        assert _pat(q) == "PercentWP"
        blob = prompt.lower()
        if "commission" in blob:
            seen.add("commission")
        if "tax" in blob:
            seen.add("tax")
        if "mark" in blob:
            seen.add("markup")
        if "sale" in blob or "off" in blob or "discount" in blob:
            seen.add("discount")
        assert q.answer_latex
    assert len(seen) >= 2, seen


def test_pa_interest_d0_is_simple_find_i():
    for seed in range(8):
        q = _q("pa_simple_and_compound_interest", 0.0, seed)
        text = (q.prompt_text or "").lower()
        assert "simple interest" in text
        assert "how much interest is earned" in text
        assert "compounded" not in text
        assert _pat(q) == "InterestWP"
        assert q.answer_latex and q.answer_latex.startswith("\\$")


def test_pa_interest_high_d_can_solve_for_p_r_or_t():
    kinds = set()
    for seed in range(24):
        q = _q("pa_simple_and_compound_interest", 16.0, seed)
        text = (q.prompt_text or "").lower()
        if "principal" in text:
            kinds.add("principal")
        if "interest rate" in text:
            kinds.add("rate")
        if "how many years" in text:
            kinds.add("time")
        if "how much interest is earned" in text:
            kinds.add("interest")
        if "balance at the end" in text:
            kinds.add("amount")
        if "compounded" in text:
            kinds.add("compound")
        assert _pat(q) == "InterestWP"
    assert kinds & {"principal", "rate", "time"}, kinds


def test_pa_slope_and_write_linear():
    q = _q("pa_slope", 0.0)
    assert _pat(q) == "Slope"
    assert "slope" in (q.prompt_text or "").lower()
    w = _q("pa_writing_linear_equations", 0.0)
    assert _pat(w) == "WriteLinear"
    assert "slope" in (w.prompt_text or "").lower() or "through" in (w.prompt_text or "").lower()


def test_pa_systems_substitution_isolated_y():
    q = _q("pa_systems_substitution", 0.0)
    assert _pat(q) == "LinearSystem"
    assert r"\begin{cases}" in (q.prompt_latex or "")
    assert "y =" in (q.prompt_latex or "").replace(" ", "") or "y=" in (
        q.prompt_latex or ""
    ).replace(" ", "")


def test_pa_graphing_systems_is_linear_system():
    q = _q("pa_graphing_systems_of_equations", 0.0)
    assert _pat(q) == "LinearSystem"
    blob = (q.prompt_latex or "") + " " + (q.prompt_text or "")
    assert "graph" in blob.lower()
    assert r"\begin{cases}" in (q.prompt_latex or "")


def test_pa_geometry_reuse():
    for type_id, pat in (
        ("pa_angle_relationships", "GeoMeasure"),
        ("pa_area_of_triangles_and_quadrilaterals", "GeoMeasure"),
        ("pa_circles", "GeoMeasure"),
        ("pythagorean_theorem", "GeoMeasure"),
        ("pa_transformations", "Transform"),
        ("pa_plotting_points", "PlotPoints"),
    ):
        q = _q(type_id, 0.0)
        assert q.prompt_latex, type_id
        assert _pat(q) == pat, (type_id, _pat(q), q.prompt_latex[:80])


def test_pa_poly_simplify():
    q = _q("pa_polynomials_simplifying", 0.0)
    assert _pat(q) == "PolySimplify"
    assert q.answer_latex
