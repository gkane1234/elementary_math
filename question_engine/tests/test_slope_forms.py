"""Slope prompt forms: points + equation variants, graphs opt-in only."""

from __future__ import annotations

from question_engine.api.handler import _generate_for_type
from question_engine.frameworks.linear import _point_slope_latex, _standard_form_latex


def test_standard_and_point_slope_latex():
    assert _standard_form_latex(5, -3, 2) == "5x - 3y = 2"
    assert _point_slope_latex(2, 3, -1) == "y + 1 = 2(x - 3)"
    assert _point_slope_latex(-5, 0, 2) == "y - 2 = -5x"
    assert _point_slope_latex(1, 0, 4) == "y - 4 = x"


def test_slope_equation_forms_have_no_graph():
    for form in ("slope_intercept", "point_slope", "standard"):
        qs = _generate_for_type(
            "slope",
            {
                "count": 4,
                "difficulty_tier": "hard",
                "from_equation": True,
                "equation_form": form,
                "include_answer_key": True,
            },
        )
        assert qs
        for q in qs:
            assert q.metadata.get("equation_form") == form
            assert "graph_spec" not in q.metadata
            assert "diagram_svg" not in q.metadata
            assert "coordinate_plane" not in q.metadata


def test_easy_equation_is_slope_intercept_only():
    qs = _generate_for_type(
        "slope",
        {
            "count": 20,
            "difficulty_tier": "easy",
            "from_equation": True,
            "include_answer_key": True,
        },
    )
    assert {q.metadata.get("equation_form") for q in qs} == {"slope_intercept"}


def test_two_points_graph_opt_in():
    off = _generate_for_type(
        "slope",
        {
            "count": 3,
            "ask_mode": "from_points",
            "difficulty_tier": "medium",
            "include_answer_key": True,
        },
    )
    assert all("graph_spec" not in q.metadata for q in off)

    on = _generate_for_type(
        "slope",
        {
            "count": 3,
            "ask_mode": "from_points",
            "graph_for_two_points": True,
            "include_graph_metadata": True,
            "difficulty_tier": "medium",
            "include_answer_key": True,
        },
    )
    assert any("graph_spec" in q.metadata for q in on)
