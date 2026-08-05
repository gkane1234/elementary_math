"""Smoke + structure tests for continuous-D ladder deepening (geo/A2/PC/Calc)."""

from __future__ import annotations

import re

import question_engine.types  # noqa: F401
from question_engine.core.base import QUESTION_TYPES
from question_engine.diagrams.figure_families import (
    complexity_for_difficulty,
    sample_figure,
)
from question_engine.settings.params import (
    apply_conic_continuous_knobs,
    apply_exponential_continuous_knobs,
    apply_geometry_continuous_knobs,
    apply_matrix_continuous_knobs,
    apply_sequence_continuous_knobs,
    apply_trigonometry_continuous_knobs,
    calc_application_structure_from_continuous,
    derivative_rule_structure_from_continuous,
    geometry_angle_structure_from_continuous,
    geometry_proof_structure_from_continuous,
    piecewise_structure_from_continuous,
    trig_graph_structure_from_continuous,
)


def _gen(type_id: str, d: float, *, seed: int = 7, count: int = 3):
    qt = QUESTION_TYPES[type_id]
    return qt.generate(
        {
            "difficulty": d,
            "count": count,
            "include_answer_key": True,
            "seed": seed,
            "include_diagram": True,
        }
    )


def test_geometry_knobs_widen_with_d():
    assert apply_geometry_continuous_knobs({"difficulty_tier": "hard"}) == {
        "difficulty_tier": "hard"
    }
    easy = apply_geometry_continuous_knobs({"difficulty": 0})
    hard = apply_geometry_continuous_knobs({"difficulty": 20})
    assert easy["angle_piece_max"] < hard["angle_piece_max"]
    assert easy["side_max"] < hard["side_max"]
    assert easy["radius_max"] < hard["radius_max"]
    assert easy["protractor_step"] > hard["protractor_step"]

    s0 = geometry_angle_structure_from_continuous({"difficulty": 0})
    s20 = geometry_angle_structure_from_continuous({"difficulty": 20})
    assert s0 is not None and s20 is not None
    assert s0["piece_max"] < s20["piece_max"]


def test_matrix_conic_exp_knobs_widen():
    m0 = apply_matrix_continuous_knobs({"difficulty": 0})
    m20 = apply_matrix_continuous_knobs({"difficulty": 20})
    assert m0["matrix_entry_max"] < m20["matrix_entry_max"]

    c0 = apply_conic_continuous_knobs({"difficulty": 0})
    c20 = apply_conic_continuous_knobs({"difficulty": 20})
    assert c0["conic_allow_translated"] is False
    assert c20["conic_allow_translated"] is True
    assert c0["conic_radius_max"] < c20["conic_radius_max"]

    e0 = apply_exponential_continuous_knobs({"difficulty": 0})
    e20 = apply_exponential_continuous_knobs({"difficulty": 20})
    assert e0["exp_base_max"] < e20["exp_base_max"]
    assert e0["exp_exponent_max"] < e20["exp_exponent_max"]

    from question_engine.settings.params import (
        apply_growth_decay_continuous_knobs,
        apply_graph_transform_continuous_knobs,
        apply_quadratic_graph_continuous_knobs,
        apply_sequence_continuous_knobs,
        apply_inverse_exp_log_continuous_knobs,
    )

    g0 = apply_growth_decay_continuous_knobs({"difficulty": 0})
    g20 = apply_growth_decay_continuous_knobs({"difficulty": 20})
    assert g0["periods_max"] < g20["periods_max"]
    assert g0["allow_half_life"] is False
    assert g20["allow_half_life"] is True

    gt0 = apply_graph_transform_continuous_knobs({"difficulty": 0})
    gt20 = apply_graph_transform_continuous_knobs({"difficulty": 20})
    assert gt0["allow_shift_k"] is False
    assert gt20["allow_stretch"] is True

    q0 = apply_quadratic_graph_continuous_knobs({"difficulty": 0})
    q20 = apply_quadratic_graph_continuous_knobs({"difficulty": 20})
    assert q0["allow_standard_form"] is False
    assert q0["allow_messy_form"] is False
    assert q20["allow_standard_form"] is True
    assert q20["allow_messy_form"] is True
    assert q20["integer_only"] is False

    s0 = apply_sequence_continuous_knobs({"difficulty": 0})
    s20 = apply_sequence_continuous_knobs({"difficulty": 20})
    assert s0["nth_max"] < s20["nth_max"]

    inv0 = apply_inverse_exp_log_continuous_knobs({"difficulty": 0})
    inv20 = apply_inverse_exp_log_continuous_knobs({"difficulty": 20})
    assert inv0["inv_shift_max"] < inv20["inv_shift_max"]

    from question_engine.settings.params import (
        apply_complex_continuous_knobs,
        apply_counting_continuous_knobs,
        apply_systems_continuous_knobs,
        apply_triangle_laws_continuous_knobs,
        apply_variation_continuous_knobs,
    )

    sys0 = apply_systems_continuous_knobs({"difficulty": 0})
    sys20 = apply_systems_continuous_knobs({"difficulty": 20})
    assert sys0["max_coefficient_magnitude"] < sys20["max_coefficient_magnitude"]

    cx0 = apply_complex_continuous_knobs({"difficulty": 0})
    cx20 = apply_complex_continuous_knobs({"difficulty": 20})
    assert cx0["complex_entry_max"] < cx20["complex_entry_max"]

    tri0 = apply_triangle_laws_continuous_knobs({"difficulty": 0})
    tri20 = apply_triangle_laws_continuous_knobs({"difficulty": 20})
    assert tri0["allow_obtuse"] is False
    assert tri20["allow_obtuse"] is True
    assert tri0["triangle_side_max"] < tri20["triangle_side_max"]

    var0 = apply_variation_continuous_knobs({"difficulty": 0})
    var20 = apply_variation_continuous_knobs({"difficulty": 20})
    assert var0["inverse_variation_weight"] < var20["inverse_variation_weight"]

    cnt0 = apply_counting_continuous_knobs({"difficulty": 0})
    cnt20 = apply_counting_continuous_knobs({"difficulty": 20})
    assert cnt0["counting_n_max"] < cnt20["counting_n_max"]
    assert cnt0["counting_r_max"] < cnt20["counting_r_max"]

    from question_engine.settings.params import (
        apply_polynomial_theory_continuous_knobs,
        apply_radical_domain_continuous_knobs,
        apply_relations_continuous_knobs,
        apply_solve_by_graphing_continuous_knobs,
    )

    rel0 = apply_relations_continuous_knobs({"difficulty": 0})
    rel20 = apply_relations_continuous_knobs({"difficulty": 20})
    assert rel0["slope_max"] < rel20["slope_max"]
    assert rel0["table_row_count"] < rel20["table_row_count"]

    sg0 = apply_solve_by_graphing_continuous_knobs({"difficulty": 0})
    sg20 = apply_solve_by_graphing_continuous_knobs({"difficulty": 20})
    assert sg0["max_degree"] < sg20["max_degree"] or sg0["allow_stretch"] is False
    assert sg0["allow_stretch"] is False
    assert sg20["allow_stretch"] is True

    pt0 = apply_polynomial_theory_continuous_knobs({"difficulty": 0})
    pt20 = apply_polynomial_theory_continuous_knobs({"difficulty": 20})
    assert pt0["binomial_n_max"] < pt20["binomial_n_max"]
    assert pt0["poly_theory_degree_max"] < pt20["poly_theory_degree_max"]

    rd0 = apply_radical_domain_continuous_knobs({"difficulty": 0})
    rd20 = apply_radical_domain_continuous_knobs({"difficulty": 20})
    assert rd0["coef_max"] < rd20["coef_max"]
    assert rd0["allow_reflection"] is False
    assert rd20["allow_reflection"] is True


def test_derivative_rule_structure_unlocks():
    assert derivative_rule_structure_from_continuous({"difficulty_tier": "hard"}) is None
    # Bare continuous probe opens allows → function classes from D=0 (checkbox model).
    d0 = derivative_rule_structure_from_continuous({"difficulty": 0})
    d8 = derivative_rule_structure_from_continuous({"difficulty": 8})
    d20 = derivative_rule_structure_from_continuous({"difficulty": 20})
    assert d0 is not None and d8 is not None and d20 is not None
    assert d0["allow_trig"] is True
    assert d8["allow_trig"] is True
    assert d20["allow_ln"] is True
    assert d0["coef_hi"] < d20["coef_hi"]
    closed = derivative_rule_structure_from_continuous(
        {"difficulty": 20, "allow_trig": False, "allow_exp": False, "allow_log": False}
    )
    assert closed is not None
    assert closed["allow_trig"] is False
    assert closed["allow_exp"] is False
    assert closed["allow_log"] is False


def test_figure_complexity_scales_with_d():
    assert complexity_for_difficulty(0) == "simple"
    assert complexity_for_difficulty(8) == "standard"
    assert complexity_for_difficulty(20) == "complex"
    adj0 = sample_figure("adjacent_angles", 0, seed=1)
    adj20 = sample_figure("adjacent_angles", 20, seed=1)
    assert adj0.params["piece_count"] < adj20.params["piece_count"]
    ang0 = sample_figure("angle_rays", 0, seed=2)
    ang20 = sample_figure("angle_rays", 20, seed=2)
    assert ang0.complexity != ang20.complexity or ang0.params != ang20.params


def test_sequence_trig_proof_calc_app_knobs():
    assert apply_sequence_continuous_knobs({"difficulty_tier": "hard"}) == {
        "difficulty_tier": "hard"
    }
    s0 = apply_sequence_continuous_knobs({"difficulty": 0})
    s20 = apply_sequence_continuous_knobs({"difficulty": 20})
    assert s0["nth_max"] < s20["nth_max"]
    assert s0["allow_negative_ratio"] is False
    assert s20["allow_negative_ratio"] is True

    t0 = apply_trigonometry_continuous_knobs({"difficulty": 0})
    t20 = apply_trigonometry_continuous_knobs({"difficulty": 20})
    assert t0["allow_reciprocal_identities"] is False
    assert t20["allow_product_to_sum_identities"] is True
    assert t0["trig_amp_max"] < t20["trig_amp_max"]

    g0 = trig_graph_structure_from_continuous({"difficulty": 0})
    g20 = trig_graph_structure_from_continuous({"difficulty": 20})
    assert g0 is not None and g20 is not None
    assert g0["mode"] == "parent"
    assert g20["mode"] == "transform"

    p0 = geometry_proof_structure_from_continuous({"difficulty": 0})
    p20 = geometry_proof_structure_from_continuous({"difficulty": 20})
    assert p0 is not None and p20 is not None
    assert p0["theorems"] == ("SSS",)
    assert "HL" in p20["theorems"] or "AAS" in p20["theorems"]
    assert p0["similarity_ratio_max"] < p20["similarity_ratio_max"]

    a0 = calc_application_structure_from_continuous({"difficulty": 0})
    a20 = calc_application_structure_from_continuous({"difficulty": 20})
    assert a0 is not None and a20 is not None
    assert a0["related_shapes"] == ("circle",)
    assert "cone" in a20["related_shapes"]
    assert a0["radius_max"] < a20["radius_max"]
    assert a0["bound_max"] < a20["bound_max"]

    pw0 = piecewise_structure_from_continuous({"difficulty": 0})
    pw20 = piecewise_structure_from_continuous({"difficulty": 20})
    assert pw0 is not None and pw20 is not None
    assert pw0["piece_count"] < pw20["piece_count"] or pw0["coef_span"] < pw20["coef_span"]
    assert pw0["allow_quadratic_piece"] is False
    assert pw20["allow_quadratic_piece"] is True


def test_smoke_geo_structure_differs_d0_vs_d20():
    """Angle / circle type_ids: piece count or radius span should differ."""
    tags0 = []
    tags20 = []
    for seed in range(5):
        for q in _gen("geo_basics_angle_addition_postulate", 0, seed=seed, count=2):
            tags0.append(q.prompt_text or q.prompt_latex or "")
        for q in _gen("geo_basics_angle_addition_postulate", 20, seed=seed, count=2):
            tags20.append(q.prompt_text or q.prompt_latex or "")
    avg0 = sum(t.count("m\\angle") + t.count("m∠") for t in tags0) / max(1, len(tags0))
    avg20 = sum(t.count("m\\angle") + t.count("m∠") for t in tags20) / max(1, len(tags20))
    assert avg20 >= avg0

    radii0, radii20 = [], []
    for seed in range(8):
        for q in _gen("geo_circles_circumference_and_area", 0, seed=seed, count=1):
            meta = q.metadata or {}
            dims = (meta.get("figure_spec") or {}).get("dimensions") or {}
            if "radius" in dims:
                radii0.append(float(dims["radius"]))
        for q in _gen("geo_circles_circumference_and_area", 20, seed=seed, count=1):
            meta = q.metadata or {}
            dims = (meta.get("figure_spec") or {}).get("dimensions") or {}
            if "radius" in dims:
                radii20.append(float(dims["radius"]))
    if radii0 and radii20:
        assert max(radii20) >= max(radii0)


def test_smoke_geo_proof_similarity_d0_vs_d20():
    theorems0 = set()
    theorems20 = set()
    for seed in range(12):
        q0 = _gen("geo_congruent_proving_triangles_congruent", 0, seed=seed, count=1)[0]
        q20 = _gen("geo_congruent_proving_triangles_congruent", 20, seed=seed, count=1)[0]
        a0 = (q0.answer_latex or "").strip()
        a20 = (q20.answer_latex or "").strip()
        if a0:
            theorems0.add(a0)
        if a20:
            theorems20.add(a20)
    assert theorems0 <= {"SSS"}
    assert theorems20 - {"SSS"}  # high D unlocks non-SSS theorems

    scales0, scales20 = [], []
    for seed in range(10):
        for q in _gen("geo_similarity_similar_polygons", 0, seed=seed, count=1):
            nums = [int(n) for n in re.findall(r"\b(\d+)\b", q.prompt_latex or "")]
            scales0.extend(nums)
        for q in _gen("geo_similarity_similar_polygons", 20, seed=seed, count=1):
            nums = [int(n) for n in re.findall(r"\b(\d+)\b", q.prompt_latex or "")]
            scales20.extend(nums)
    assert max(scales20 or [0]) >= max(scales0 or [0])


def test_smoke_a2_matrix_conic_structure():
    entry_pat = re.compile(r"-?\d+")
    max_abs0, max_abs20 = 0, 0
    for seed in range(6):
        for q in _gen("a2_matrices_inverses", 0, seed=seed, count=1):
            nums = [abs(int(n)) for n in entry_pat.findall(q.prompt_latex or "")]
            if nums:
                max_abs0 = max(max_abs0, max(nums))
        for q in _gen("a2_matrices_inverses", 20, seed=seed, count=1):
            nums = [abs(int(n)) for n in entry_pat.findall(q.prompt_latex or "")]
            if nums:
                max_abs20 = max(max_abs20, max(nums))
    assert max_abs0 <= 4
    assert max_abs20 >= max_abs0

    for seed in range(10):
        qs = _gen(
            "a2_conic_sections_circles_writing_equations", 20, seed=seed, count=1
        )
        _ = qs[0].prompt_latex or ""
    qs0 = _gen("a2_conic_sections_circles_writing_equations", 0, seed=1, count=3)
    for q in qs0:
        assert "(0,0)" in (q.prompt_latex or "") or "origin" in (
            q.prompt_latex or ""
        ).lower() or re.search(r"center\s*}\s*\(0,0\)", q.prompt_latex or "")


def test_smoke_a2_trig_sequence_structure():
    texts0, texts20 = [], []
    for seed in range(8):
        texts0.append(
            _gen("a2_trigonometry_graphing_trig_functions", 0, seed=seed, count=1)[
                0
            ].prompt_latex
            or ""
        )
        texts20.append(
            _gen("a2_trigonometry_graphing_trig_functions", 20, seed=seed, count=1)[
                0
            ].prompt_latex
            or ""
        )
    assert any(
        re.search(r"[2-9]\\sin|[2-9]\\cos|\\sin\\left\([2-9]|\\cos\\left\([2-9]", t)
        for t in texts20
    )
    assert all("\\sin x" in t or "\\cos x" in t for t in texts0)

    ns0, ns20 = [], []
    for seed in range(10):
        q0 = _gen("a2_sequences_and_series_arithmetic_sequences", 0, seed=seed, count=1)[0]
        q20 = _gen(
            "a2_sequences_and_series_arithmetic_sequences", 20, seed=seed, count=1
        )[0]
        m0 = re.search(r"(\d+)\^\{\\text\{th\}\}", q0.prompt_latex or "")
        m20 = re.search(r"(\d+)\^\{\\text\{th\}\}", q20.prompt_latex or "")
        if m0:
            ns0.append(int(m0.group(1)))
        if m20:
            ns20.append(int(m20.group(1)))
    assert ns0 and ns20
    assert max(ns20) >= max(ns0)
    assert sum(ns20) / len(ns20) > sum(ns0) / len(ns0)


def test_smoke_precalc_calc_structure():
    from question_engine.settings.params import (
        apply_calculus_continuous_knobs,
        apply_logarithm_continuous_knobs,
        apply_trigonometry_continuous_knobs,
    )

    log0 = apply_logarithm_continuous_knobs({"difficulty": 0})
    log20 = apply_logarithm_continuous_knobs({"difficulty": 20})
    assert log0["allow_natural_log"] is False
    assert log20["allow_natural_log"] is True

    trig0 = apply_trigonometry_continuous_knobs({"difficulty": 0})
    trig20 = apply_trigonometry_continuous_knobs({"difficulty": 20})
    assert trig0["allow_tan"] is False
    assert trig20["allow_cot"] is True

    calc0 = apply_calculus_continuous_knobs({"difficulty": 0})
    calc20 = apply_calculus_continuous_knobs({"difficulty": 20})
    assert calc0["term_count"] < calc20["term_count"] or calc0["power_max"] < calc20[
        "power_max"
    ]
    assert calc20["allow_infinity"] is True

    for type_id, d in (
        ("calc_limits_by_direct_evaluation", 0),
        ("calc_limits_by_direct_evaluation", 20),
        ("calc_diff_power_rule", 0),
        ("calc_diff_product_rule", 20),
        ("calc_diff_chain_rule", 15),
        ("calc_indef_int_power_rule", 12),
        ("pc_evaluating_logarithms", 0),
        ("pc_evaluating_logarithms", 20),
        ("pc_trig_functions_of_any_angle", 0),
        ("pc_trig_functions_of_any_angle", 20),
        ("pc_exponential_equations_not_requiring_logarithms", 20),
        ("pc_piecewise_functions", 0),
        ("pc_piecewise_functions", 20),
        ("geo_basics_classifying_angles", 0),
        ("geo_basics_classifying_angles", 20),
        ("geo_congruent_proving_triangles_congruent", 0),
        ("geo_constructions_circles", 20),
        ("a2_matrices_cramers_rule", 10),
        ("a2_trigonometry_graphing_trig_functions", 0),
        ("a2_trigonometry_graphing_trig_functions", 20),
        ("calc_app_diff_related_rates", 0),
        ("calc_app_diff_related_rates", 20),
        ("calc_app_int_volume_by_slicing_disks_and_washers", 0),
        ("calc_app_int_volume_by_slicing_disks_and_washers", 20),
        ("calc_diff_eq_separable", 0),
        ("calc_diff_eq_separable", 20),
        ("calc_app_diff_optimization", 20),
    ):
        qs = _gen(type_id, d, seed=3, count=1)
        assert qs, type_id
        assert (qs[0].prompt_latex or qs[0].prompt_text or "").strip(), type_id


def test_smoke_calc_apps_structure_differs():
    shapes20 = set()
    for seed in range(16):
        text = (
            _gen("calc_app_diff_related_rates", 20, seed=seed, count=1)[0].prompt_latex
            or ""
        ).lower()
        if "sphere" in text:
            shapes20.add("sphere")
        elif "cone" in text:
            shapes20.add("cone")
        else:
            shapes20.add("circle")
    assert "circle" in shapes20
    assert shapes20 & {"sphere", "cone"}

    for seed in range(6):
        text0 = (
            _gen("calc_app_diff_related_rates", 0, seed=seed, count=1)[0].prompt_latex
            or ""
        ).lower()
        assert "circle" in text0
        assert "sphere" not in text0 and "cone" not in text0

    washer20 = 0
    for seed in range(12):
        t = (
            _gen("calc_app_int_volume_by_slicing_disks_and_washers", 20, seed=seed, count=1)[
                0
            ].prompt_latex
            or ""
        ).lower()
        if "washer" in t or "region between" in t:
            washer20 += 1
    assert washer20 >= 1

    de0 = _gen("calc_diff_eq_separable", 0, seed=1, count=3)
    de20 = _gen("calc_diff_eq_separable", 20, seed=1, count=3)
    assert all("y/x" not in (q.prompt_latex or "").replace(" ", "") for q in de0)
    assert any(
        r"\frac{y}{x}" in (q.prompt_latex or "") or "y/x" in (q.prompt_latex or "")
        for q in de20
    )


def test_limits_term_count_differs():
    """Poly limit prompts at D=20 should often have more terms than D=0."""

    def _termish(latex: str) -> int:
        return latex.count("+") + latex.count("-")

    scores0, scores20 = [], []
    for seed in range(10):
        q0 = _gen("calc_limits_by_direct_evaluation", 0, seed=seed, count=1)[0]
        q20 = _gen("calc_limits_by_direct_evaluation", 20, seed=seed, count=1)[0]
        scores0.append(_termish(q0.prompt_latex or ""))
        scores20.append(_termish(q20.prompt_latex or ""))
    assert sum(scores20) / len(scores20) > sum(scores0) / len(scores0)
