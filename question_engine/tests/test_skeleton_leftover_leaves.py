"""Live-path smoke for leftover skeleton leaves (do-now + soon)."""

from __future__ import annotations

import re

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


def test_proportion_d0_and_opt_out():
    q = _q("solving_proportions", 0.0)
    assert _pat(q) == "Proportion"
    assert r"\frac" in (q.prompt_latex or "")
    assert "=" in (q.prompt_latex or "")
    q_hi = _q("solving_proportions", 16.0, seed=207)
    assert _pat(q_hi) == "Proportion"
    old = _q("solving_proportions", 0.0, extra={"use_sample_proportion": True})
    assert _pat(old) != "Proportion"
    g6 = _q("g6_equivalent_ratio_equations", 0.0)
    assert _pat(g6) == "Proportion"
    pa = _q("pa_checking_for_a_proportion", 0.0)
    assert _pat(pa) == "Proportion"


def test_factor_gcf_d0_and_opt_out():
    q = _q("polynomial_factoring_common_factor", 0.0)
    assert _pat(q) == "FactorGcf"
    prompt = q.prompt_latex or ""
    assert "^" not in prompt or "x^2" not in prompt.replace(" ", "")
    old = _q(
        "polynomial_factoring_common_factor",
        0.0,
        extra={"use_factor_poly": True},
    )
    assert _pat(old) != "FactorGcf"


def test_factor_gcf_climbs_with_d_like_old():
    """Live GCF leaf must add x in the GCF at D≥8 (old 4x(2x-3)), not 3x+6 forever."""
    easy = {
        (_q("polynomial_factoring_common_factor", 0.0, seed=s).prompt_latex or "")
        for s in (101, 207, 313, 419)
    }
    assert all("^{2}" not in p and "x^2" not in p.replace(" ", "") for p in easy), easy
    hi_prompts = []
    hi_answers = []
    for seed in (101, 207, 313, 419, 523):
        q = _q("polynomial_factoring_common_factor", 8.0, seed=seed)
        assert _pat(q) == "FactorGcf"
        hi_prompts.append(q.prompt_latex or "")
        hi_answers.append(q.answer_latex or "")
        meta = q.metadata or {}
        assert "variable_gcf" in list(meta.get("upgrades") or []) or "x" in (
            meta.get("gcf") or ""
        ) or "^{2}" in (q.prompt_latex or "")
    blob = " ".join(hi_prompts + hi_answers)
    assert "^{2}" in blob or "x^2" in blob.replace(" ", "")
    assert any("x" in (a.replace(" ", "")) and "\\left(" in a for a in hi_answers)
    # Not the same binomial at every seed/D.
    assert len(set(hi_prompts)) >= 2, hi_prompts
    d16 = _q("polynomial_factoring_common_factor", 16.0, seed=101)
    assert "^{2}" in (d16.prompt_latex or "") or "x^2" in (d16.prompt_latex or "").replace(
        " ", ""
    )


def test_graph_inequality_d0_isolated():
    q = _q("graphing_single_variable_inequalities", 0.0)
    assert _pat(q) == "SolveInequality"
    blob = q.prompt_latex or ""
    assert re.search(r"x\s*(\\le|\\ge|<|>)", blob)
    assert r"\left(" not in blob
    meta = q.metadata or {}
    assert meta.get("number_line_spec")
    assert (meta.get("number_line_spec") or {}).get("blank") is True
    assert meta.get("answer_number_line_spec")
    g6 = _q("g6_solutions_to_inequalities", 0.0)
    assert (g6.metadata or {}).get("number_line_spec")
    hi = _q("graphing_single_variable_inequalities", 16.0, seed=207)
    assert _pat(hi) == "SolveInequality"


def test_factor_grouping_d0_is_four_term_not_trinomial():
    """Gold is OpenStax §7.1 grouping at D=0 — never a quadratic trinomial."""
    for seed in (101, 207, 313, 419):
        q = _q("polynomial_factoring_grouping", 0.0, seed=seed)
        assert _pat(q) == "FactorProduct"
        meta = q.metadata or {}
        assert meta.get("form_id") == "factor_by_grouping"
        assert meta.get("factor_kind") == "grouping"
        assert int(meta.get("degree") or 0) == 3
        blob = (q.prompt_latex or "").replace(" ", "")
        assert "x^{3}" in blob or "x^3" in blob
        assert r"\left(" not in blob
    hi = _q("polynomial_factoring_grouping", 16.0, seed=207)
    assert _pat(hi) == "FactorProduct"
    assert int((hi.metadata or {}).get("degree") or 0) == 3


def test_factor_equations_d0():
    q = _q("quadratic_factoring_equations", 0.0)
    assert _pat(q) == "FactorProduct"
    blob = (q.prompt_latex or "").replace(" ", "")
    assert blob.endswith("=0") or "=0" in blob
    # Old factor_poly D=0: monic (x+a)(x+b) with a,b>0.
    assert blob.startswith("x^{2}") or blob.startswith("x^2")
    assert r"x^{3}" not in blob and "x^3" not in blob
    hi = _q("quadratic_factoring_equations", 16.0, seed=207)
    assert "= 0" in (hi.prompt_latex or "") or "=0" in (hi.prompt_latex or "").replace(
        " ", ""
    )
    a2 = _q(
        "a2_quadratic_functions_and_inequalities_solving_equations_by_factoring",
        0.0,
    )
    assert _pat(a2) == "FactorProduct"


def test_compound_inequality_d0():
    q = _q("compound_inequalities", 0.0)
    assert _pat(q) == "CompoundInequality"
    blob = q.prompt_latex or ""
    assert r"\text{Solve:" not in blob
    assert r"\left(" not in blob
    # Old easy: isolated given compound; prompt = answer; blank number line.
    assert re.search(r"(\\text\{\s*or\s*\}|<)", blob)
    assert q.answer_latex
    assert q.answer_latex == blob
    assert r"\cup" not in (q.answer_latex or "")
    meta = q.metadata or {}
    nls = meta.get("number_line_spec") or {}
    ans_nl = meta.get("answer_number_line_spec") or {}
    assert nls.get("blank") is True
    assert ans_nl
    assert ans_nl.get("blank") is not True
    assert "boundary_high" in ans_nl
    assert ans_nl.get("direction") in {"both", "outside"}
    hi = _q("compound_inequalities", 16.0, seed=207)
    assert _pat(hi) == "CompoundInequality"
    hi_nl = (hi.metadata or {}).get("answer_number_line_spec") or {}
    assert hi_nl.get("boundary_high") is not None
    a2 = _q("a2_equations_and_inequalities_compound_inequalities", 0.0)
    assert _pat(a2) == "CompoundInequality"
    old = _q(
        "compound_inequalities",
        0.0,
        extra={"use_sample_compound_inequality": True},
    )
    assert _pat(old) != "CompoundInequality"


def test_abs_equation_d0():
    q = _q("absolute_value_equations", 0.0)
    assert _pat(q) == "AbsEquation"
    assert r"\left|" in (q.prompt_latex or "") or "|" in (q.prompt_latex or "")
    hi = _q("absolute_value_equations", 16.0, seed=207)
    assert _pat(hi) == "AbsEquation"
    old = _q(
        "absolute_value_equations",
        0.0,
        extra={"use_sample_absolute_value_equation": True},
    )
    assert _pat(old) != "AbsEquation"


def test_abs_inequality_d0():
    q = _q("absolute_value_inequalities", 0.0)
    assert _pat(q) == "AbsInequality"
    meta = q.metadata or {}
    assert meta.get("number_line_spec")
    hi = _q("absolute_value_inequalities", 16.0, seed=207)
    assert _pat(hi) == "AbsInequality"


def _inner_a(q) -> int:
    raw = (q.metadata or {}).get("inner_a")
    assert raw is not None, q.metadata
    return abs(int(str(raw).split("/")[0])) if "/" in str(raw) else abs(int(raw))


def test_abs_eq_and_ineq_d0_a_is_one():
    for type_id in ("absolute_value_equations", "absolute_value_inequalities"):
        for seed in range(16):
            q = _q(type_id, 0.0, seed=101 + seed)
            assert _inner_a(q) == 1, (type_id, seed, q.prompt_latex)


def test_abs_eq_and_ineq_high_d_a_ne_1():
    """Old medium (D=8) linear inner was |ax+b| with |a|≥2; match that."""
    for type_id in ("absolute_value_equations", "absolute_value_inequalities"):
        for d in (8.0, 16.0):
            for seed in range(12):
                q = _q(type_id, d, seed=200 + seed)
                assert _inner_a(q) >= 2, (type_id, d, seed, q.prompt_latex)



def test_eq_cancel_d0_proportion():
    q = _q("rational_expressions_equations", 0.0)
    assert _pat(q) == "EqCancel"
    assert r"\frac" in (q.prompt_latex or "")
    hi = _q("rational_expressions_equations", 16.0, seed=207)
    assert _pat(hi) == "EqCancel"
    old = _q(
        "rational_expressions_equations",
        4.0,
        extra={"use_hand_rational_equations": True},
    )
    assert _pat(old) != "EqCancel"
    a2 = _q("a2_rational_expressions_equations", 0.0)
    assert _pat(a2) == "EqCancel"


def test_like_terms_and_distribute_d0():
    q = _q("g6_combining_like_terms", 0.0)
    assert _pat(q) == "AffineInflate"
    blob = q.prompt_latex or ""
    assert r"\left(" not in blob
    assert blob.count("x") >= 2
    dist = _q("g6_distributive_property_algebraic", 0.0)
    assert _pat(dist) == "AffineInflate"
    assert r"\left(" in (dist.prompt_latex or "")
    exp = _q("a2_beginning_algebra_simplifying_algebraic_expressions", 0.0)
    assert _pat(exp) == "AffineInflate"
    old = _q(
        "g6_combining_like_terms",
        0.0,
        extra={"use_sample_like_terms": True},
    )
    assert _pat(old) != "AffineInflate"


def test_poly_add_sub_d0_linear():
    q = _q("polynomial_add_subtract", 0.0)
    assert _pat(q) == "PolyAddSub"
    blob = q.prompt_latex or ""
    assert blob.count("\\left(") >= 2
    assert "x^2" not in blob.replace(" ", "")
    hi = _q("polynomial_add_subtract", 16.0, seed=207)
    assert _pat(hi) == "PolyAddSub"
    old = _q(
        "polynomial_add_subtract",
        0.0,
        extra={"use_sample_polynomial_add_subtract": True},
    )
    assert _pat(old) != "PolyAddSub"


def test_similar_figures_wp_story_and_diagram():
    q = _q("pa_similar_figures", 0.0, extra={"prompt_style": "diagram"})
    assert _pat(q) == "SimilarFigures"
    assert not looks_like_dumped_equation(q.prompt_latex or "")
    assert "$3x+2=17$" not in (q.prompt_latex or "")
    meta = q.metadata or {}
    assert meta.get("diagram_svg") and "<svg" in str(meta.get("diagram_svg"))
    desc = _q(
        "pa_similar_figures",
        0.0,
        extra={"prompt_style": "description_only"},
    )
    assert not (desc.metadata or {}).get("diagram_svg")
    old = _q(
        "pa_similar_figures",
        0.0,
        extra={"use_legacy_similar_figures": True, "prompt_style": "diagram"},
    )
    assert _pat(old) != "SimilarFigures"


def test_proportion_rate_wp_unbroken():
    from question_engine.generators.primitive_linear import GENERATORS as LIN

    qs = LIN["wp_proportion"](
        "wp_proportion",
        {
            "difficulty": 0,
            "count": 1,
            "seed": 11,
            "include_answer_key": True,
        },
    )
    assert qs
    assert qs[0].metadata.get("skeleton_pattern") == "ProportionRate"
    assert not looks_like_dumped_equation(qs[0].prompt_latex or "")


def test_check_equation_d0_and_opt_out():
    q = _q("g6_solutions_to_equations", 0.0)
    assert _pat(q) == "SolveLinear"
    blob = q.prompt_latex or ""
    assert r"\text{Is }" in blob
    assert "a solution of" in blob
    # Old D=0: one-step, no both-sides, no distribute.
    assert r"\left(" not in blob
    assert (q.metadata or {}).get("steps") == "one"
    assert q.answer_latex in {r"\text{yes}", r"\text{no}"}
    hi = _q("g6_solutions_to_equations", 16.0, seed=207)
    assert _pat(hi) == "SolveLinear"
    old = _q(
        "g6_solutions_to_equations",
        0.0,
        extra={"use_sample_linear_equation": True},
    )
    assert _pat(old) != "SolveLinear"


def test_check_equation_species_follows_old():
    for seed in range(8):
        q0 = _q("g6_solutions_to_equations", 0.0, seed=101 + seed)
        assert (q0.metadata or {}).get("steps") == "one"
        q8 = _q("g6_solutions_to_equations", 8.0, seed=101 + seed)
        assert (q8.metadata or {}).get("steps") == "two"


def test_write_one_step_rate_d0():
    q = _q("g6_constant_rate_equations", 0.0)
    assert _pat(q) == "SolveLinear"
    blob = (q.prompt_latex or "") + " " + (q.prompt_text or "")
    assert "Write an equation" in blob
    assert "find" in blob.lower()
    meta = q.metadata or {}
    assert meta.get("ask") == "distance"
    assert meta.get("vehicle") in {"bike", "car", "walk", "bus", "train"}
    assert r"d =" in (q.answer_latex or "") or "d =" in (q.answer_latex or "")
    hi = _q("g6_constant_rate_equations", 16.0, seed=207)
    assert _pat(hi) == "SolveLinear"
    old = _q(
        "g6_constant_rate_equations",
        0.0,
        extra={"use_sample_linear_equation": True},
    )
    assert _pat(old) != "SolveLinear"


def test_write_one_step_other_d0():
    q = _q("g6_equations_for_other_relationships", 0.0)
    assert _pat(q) == "SolveLinear"
    blob = q.prompt_latex or ""
    assert "Write an equation" in blob
    fid = str((q.metadata or {}).get("frame_id") or "")
    assert fid in {
        "write_cost",
        "write_tickets",
        "write_square",
        "write_triangle",
        "write_cost_invert",
        "write_square_invert",
    }
    hi = _q("g6_equations_for_other_relationships", 16.0, seed=207)
    assert _pat(hi) == "SolveLinear"
    assert "Write an equation" in (hi.prompt_latex or "")


def test_a1_systems_elimination_d0_opposite():
    q = _q("systems_elimination", 0.0)
    assert _pat(q) == "LinearSystem"
    assert r"\begin{cases}" in (q.prompt_latex or "")
    meta = q.metadata or {}
    assert meta.get("method") == "elimination"
    assert "opposite_coeffs" in list(meta.get("upgrades") or [])
    hi = _q("systems_elimination", 16.0, seed=207)
    assert _pat(hi) == "LinearSystem"


def test_a1_systems_substitution_isolated_y():
    q = _q("systems_substitution", 0.0)
    assert _pat(q) == "LinearSystem"
    blob = (q.prompt_latex or "").replace(" ", "")
    assert "y=" in blob
    assert r"\begin{cases}" in (q.prompt_latex or "")


def test_a1_systems_graphing_is_linear_system():
    q = _q("systems_graphing", 0.0)
    assert _pat(q) == "LinearSystem"
    blob = (q.prompt_latex or "") + " " + (q.prompt_text or "")
    assert "graph" in blob.lower()
    assert r"\begin{cases}" in (q.prompt_latex or "")
    assert (q.metadata or {}).get("solution_type") == "unique"


def test_a1_graphing_systems_of_inequalities_d0():
    q = _q("graphing_systems_of_inequalities", 0.0)
    assert _pat(q) == "GraphSystemIneq"
    blob = q.prompt_latex or ""
    assert r"\begin{cases}" in blob
    assert "y" in blob
    assert "<" in blob or ">" in blob or r"\le" in blob or r"\ge" in blob


def test_a1_slope_write_and_graph():
    q = _q("slope", 0.0)
    assert _pat(q) == "Slope"
    assert "slope" in (q.prompt_text or "").lower()
    w = _q("writing_linear_equations", 0.0)
    assert _pat(w) == "WriteLinear"
    g = _q("graphing_linear_equations", 0.0)
    assert _pat(g) == "GraphLinear"
    assert "Graph" in (g.prompt_latex or "") or "graph" in (g.prompt_text or "").lower()
    gi = _q("graphing_linear_inequalities", 0.0)
    assert _pat(gi) == "GraphLinearIneq"


def test_more_on_slope_is_parallel_perp_not_points():
    for seed in range(12):
        q = _q("more_on_slope", 0.0, seed=101 + seed)
        assert _pat(q) == "MoreOnSlope"
        blob = ((q.prompt_latex or "") + " " + (q.prompt_text or "")).lower()
        assert "through" not in blob
        assert "parallel" in blob
    hi = _q("more_on_slope", 16.0, seed=207)
    assert _pat(hi) == "MoreOnSlope"
    hi_blob = ((hi.prompt_latex or "") + " " + (hi.prompt_text or "")).lower()
    assert "perpendicular" in hi_blob or "parallel" in hi_blob


def test_unclear_function_leaves_still_generate():
    for type_id in (
        "evaluating_graphing_functions",
        "discrete_relations",
        "continuous_relations",
        "graphing_absolute_value_equations",
    ):
        q = _q(type_id, 0.0)
        assert q.prompt_latex, type_id
        assert q.answer_latex, type_id


def test_evaluate_affine_d0_and_opt_out():
    q = _q("g6_evaluating_algebraic_expressions", 0.0)
    assert _pat(q) == "AffineInflate"
    blob = q.prompt_latex or ""
    assert r"\text{ when }" in blob
    # Old D=0 is already-simplified ax+b, not 2(x+3).
    assert r"\left(" not in blob
    hi = _q("g6_evaluating_algebraic_expressions", 16.0, seed=207)
    assert _pat(hi) == "AffineInflate"
    old = _q(
        "g6_evaluating_algebraic_expressions",
        0.0,
        extra={"use_sample_evaluate": True},
    )
    assert _pat(old) != "AffineInflate"
