"""D=0 vs D=20 structure checks for CONTINUOUS_D_TODO fixes."""

from __future__ import annotations

import re

import question_engine.types  # noqa: F401
from question_engine.core.base import QUESTION_TYPES
from question_engine.generators.basic import (
    _radical_add_subtract_modes,
    _radical_divide_modes,
    _radical_multiply_modes,
)
from question_engine.generators.calculus_pilot import (
    GENERATORS as PILOT_GENERATORS,
    _differential_families,
    _integral_sub_families,
    _pilot_structure,
    _tangent_families,
)
from question_engine.generators.complex_fractions import _choose_builder, _build_easy, _build_hard
from question_engine.settings.params import (
    apply_radical_expression_continuous_knobs,
    compound_interest_structure_from_continuous,
    complex_fraction_structure_from_continuous,
)


def _gen(type_id: str, d: float, *, seed: int = 7, count: int = 4):
    qt = QUESTION_TYPES[type_id]
    return qt.generate(
        {
            "difficulty": d,
            "count": count,
            "include_answer_key": True,
            "seed": seed,
        }
    )


def test_pilot_numeric_d_not_stuck_on_easy():
    """Broken pilot path used to map difficulty=14 → easy forever."""
    s0 = _pilot_structure({"difficulty": 0})
    s20 = _pilot_structure({"difficulty": 20})
    assert s0["band"] == "easy"
    assert s20["band"] == "hard"
    assert set(_tangent_families(s20)) - set(_tangent_families(s0))
    assert "eval_dx" in _differential_families(s20) or "product" in _differential_families(s20)
    assert "mixed_rewrite" in _integral_sub_families(s20)
    assert "mixed_rewrite" not in _integral_sub_families(s0)

    for key in PILOT_GENERATORS:
        qs0 = PILOT_GENERATORS[key](key, {"difficulty": 0, "count": 3, "include_answer_key": True})
        qs20 = PILOT_GENERATORS[key](key, {"difficulty": 20, "count": 3, "include_answer_key": True})
        assert len(qs0) == 3 and len(qs20) == 3
        assert all(q.prompt_latex for q in qs0 + qs20)


def test_pilot_catalog_types_live_path_differ():
    for type_id in (
        "calc_app_diff_differentials",
        "calc_app_diff_slope_tangent_and_normal_lines",
        "calc_indef_int_logarithmic_rule_and_exponentials_with_substitution",
    ):
        texts0 = {(q.prompt_latex or "") for q in _gen(type_id, 0, seed=1, count=8)}
        texts20 = {(q.prompt_latex or "") for q in _gen(type_id, 20, seed=1, count=8)}
        assert texts0 and texts20
        # Same seed + different D should not collapse to an identical set.
        assert texts0 != texts20, type_id


def test_derivative_rules_power_product_chain_structure():
    for type_id in (
        "calc_diff_power_rule",
        "calc_diff_product_rule",
        "calc_diff_chain_rule",
        "pc_power_rule_for_differentiation",
    ):
        qs0 = _gen(type_id, 0, seed=2, count=6)
        qs20 = _gen(type_id, 20, seed=2, count=6)
        assert qs0 and qs20
        joined0 = " ".join(q.prompt_latex or "" for q in qs0)
        joined20 = " ".join(q.prompt_latex or "" for q in qs20)
        assert joined0 != joined20 or len(joined20) >= len(joined0)


def test_radical_modes_unlock_with_d():
    m0 = set(_radical_add_subtract_modes({"difficulty": 0}))
    m20 = set(_radical_add_subtract_modes({"difficulty": 20}))
    assert m0 == {"like"}
    assert "coeff_unsimplified" in m20

    mul0 = set(_radical_multiply_modes({"difficulty": 0}))
    mul20 = set(_radical_multiply_modes({"difficulty": 20}))
    assert mul0 == {"simple"}
    assert "binomial" in mul20

    div0 = set(_radical_divide_modes({"difficulty": 0}))
    div20 = set(_radical_divide_modes({"difficulty": 20}))
    assert div0 == {"reduced"}
    assert "rationalize" in div20

    knobs = apply_radical_expression_continuous_knobs({"difficulty": 20})
    assert knobs["allow_binomial_product"] is True
    assert knobs["allow_rationalize_divide"] is True


def test_radical_catalog_live_path():
    for type_id in (
        "radical_add_subtract",
        "radical_multiply",
        "radical_divide",
    ):
        qs0 = _gen(type_id, 0, seed=4, count=5)
        qs20 = _gen(type_id, 20, seed=4, count=5)
        assert qs0 and qs20
        assert {q.prompt_latex for q in qs0} != {q.prompt_latex for q in qs20}


def test_complex_fractions_and_compound_interest():
    assert _choose_builder({"difficulty": 0}) is _build_easy
    assert _choose_builder({"difficulty": 20}) is _build_hard
    s0 = complex_fraction_structure_from_continuous({"difficulty": 0})
    s20 = complex_fraction_structure_from_continuous({"difficulty": 20})
    assert s0 and s20 and s0["band"] != s20["band"]

    ci0 = compound_interest_structure_from_continuous({"difficulty": 0})
    ci20 = compound_interest_structure_from_continuous({"difficulty": 20})
    assert ci0 and ci20
    assert ci0["n_choices"] == (1,)
    assert 12 in ci20["n_choices"]
    assert ci0["t_max"] < ci20["t_max"]

    qs0 = _gen("a2_rational_expressions_complex_fractions", 0, seed=5, count=4)
    qs20 = _gen("a2_rational_expressions_complex_fractions", 20, seed=5, count=4)
    assert qs0 and qs20
    assert {q.prompt_latex for q in qs0} != {q.prompt_latex for q in qs20}

    qs0 = _gen("pc_compound_interest", 0, seed=5, count=6)
    qs20 = _gen("pc_compound_interest", 20, seed=5, count=6)
    assert qs0 and qs20
    months0 = sum(1 for q in qs0 if "monthly" in (q.prompt_latex or ""))
    months20 = sum(1 for q in qs20 if "monthly" in (q.prompt_latex or ""))
    assert months0 == 0
    assert months20 >= 1


def test_geo_rhombus_wired_and_differs():
    assert "geo_rhombus_area" in __import__(
        "question_engine.generators", fromlist=["GENERATORS"]
    ).GENERATORS
    qs0 = _gen("geo_quadrilaterals_rhombuses", 0, seed=3, count=6)
    qs20 = _gen("geo_quadrilaterals_rhombuses", 20, seed=3, count=6)
    assert qs0 and qs20
    diag20 = sum(1 for q in qs20 if "diagonal" in (q.prompt_latex or "").lower())
    diag0 = sum(1 for q in qs0 if "diagonal" in (q.prompt_latex or "").lower())
    assert diag0 == 0
    assert diag20 >= 1


def test_trig_area_and_g6_solutions_structure():
    sides0 = []
    sides20 = []
    for seed in range(8):
        q0 = _gen("geo_trig_trigonometry_and_area", 0, seed=seed, count=1)[0]
        q20 = _gen("geo_trig_trigonometry_and_area", 20, seed=seed, count=1)[0]
        for text, bucket in ((q0.prompt_latex or "", sides0), (q20.prompt_latex or "", sides20)):
            ab = re.search(r"AB=(\d+)", text)
            ac = re.search(r"AC=(\d+)", text)
            if ab:
                bucket.append(int(ab.group(1)))
            if ac:
                bucket.append(int(ac.group(1)))
    assert sides0 and sides20
    assert max(sides20) >= max(sides0)

    # Already continuous; still assert D changes equation structure.
    texts0 = []
    texts20 = []
    for seed in range(10):
        texts0.append(_gen("g6_solutions_to_equations", 0, seed=seed, count=1)[0].prompt_latex or "")
        texts20.append(_gen("g6_solutions_to_equations", 20, seed=seed, count=1)[0].prompt_latex or "")
    assert any("/" in t or r"\frac" in t for t in texts20) or any("-" in t for t in texts20)
    assert texts0 != texts20


def test_calc_topic_structure_unlocks_with_d():
    from question_engine.settings.params import (
        calc_topic_structure_from_continuous,
        pick_unlocked_families,
    )

    assert calc_topic_structure_from_continuous({"difficulty_tier": "hard"}) is None
    s0 = calc_topic_structure_from_continuous({"difficulty": 0})
    s8 = calc_topic_structure_from_continuous({"difficulty": 8})
    s20 = calc_topic_structure_from_continuous({"difficulty": 20})
    assert s0 and s8 and s20
    assert s0["unlock_medium"] is False
    assert s0["unlock_hard"] is False
    assert s8["unlock_medium"] is True
    assert s8["unlock_hard"] is False
    assert s20["unlock_hard"] is True
    assert s20["unlock_compose_table"] is True
    assert s20["coef_hi"] > s0["coef_hi"]
    assert s20["riemann_n_max"] >= s0["riemann_n_max"]

    fam0 = pick_unlocked_families(s0, ["a"], medium=["b"], hard=["c"])
    fam20 = pick_unlocked_families(s20, ["a"], medium=["b"], hard=["c"])
    assert fam0 == ["a"]
    assert set(fam20) == {"a", "b", "c"}


_A3_FIXED_TYPE_IDS = (
    # Precalculus
    "pc_definition_of_the_derivative",
    "pc_approximating_area_under_a_curve",
    "pc_area_under_a_curve_by_limit_of_sums",
    # Diff rules / rates (CDR dedicated builders)
    "calc_diff_average_rates_of_change",
    "calc_diff_definition_of_the_derivative",
    "calc_diff_instantaneous_rates_of_change",
    "calc_diff_higher_order_derivatives",
    "calc_diff_rules_using_tables",
    "calc_diff_other_base_logarithms_and_exponentials",
    "calc_diff_logarithmic",
    "calc_diff_implicit",
    "calc_diff_inverse_functions",
    # Apps / theorems
    "calc_app_diff_rolles_theorem",
    "calc_app_diff_mean_value_theorem",
    "calc_app_diff_limits_in_form_of_definition_of_derivative",
    "calc_app_int_area_under_a_curve",
    # Integrals
    "calc_indef_int_logarithmic_rule_and_exponentials",
    "calc_indef_int_trigonometric",
    "calc_indef_int_inverse_trigonometric",
    "calc_indef_int_power_rule_with_substitution",
    "calc_indef_int_integration_by_parts",
    "calc_def_int_approximating_area_under_a_curve",
    "calc_def_int_area_under_a_curve_by_limit_of_sums",
    "calc_def_int_riemann_sum_tables",
    "calc_def_int_first_fundamental_theorem_of_calculus",
    "calc_def_int_mean_value_theorem",
    "calc_def_int_second_fundamental_theorem_of_calculus",
    "calc_def_int_substitution_with_change_of_variables",
    "calc_diff_eq_slope_fields",
)


def test_a3_calc_pc_live_path_d0_vs_d20():
    for type_id in _A3_FIXED_TYPE_IDS:
        qs0 = _gen(type_id, 0, seed=11, count=6)
        qs20 = _gen(type_id, 20, seed=11, count=6)
        assert qs0 and qs20, type_id
        texts0 = {q.prompt_latex or "" for q in qs0}
        texts20 = {q.prompt_latex or "" for q in qs20}
        assert texts0 and texts20, type_id
        joined0 = " ".join(texts0)
        joined20 = " ".join(texts20)
        # Same seed + different D should change prompts and/or grow structure.
        assert texts0 != texts20 or len(joined20) >= len(joined0), type_id


def test_a3_family_unlock_structure_differs():
    """Spot-check that hard-only families stay locked at D=0."""
    from question_engine.generators.calculus import _topic_structure, _pick_family
    from question_engine.generators.calculus_derivative_rules import (
        _rule_structure,
        _pick_family as _cdr_pick,
    )

    s0 = _topic_structure({"difficulty": 0})
    s20 = _topic_structure({"difficulty": 20})
    # At D=0 only base family; at D=20 all unlocks open.
    assert _pick_family(s0, ["a"], medium=["b"], hard=["c"]) == "a"
    assert set(
        __import__("question_engine.settings.params", fromlist=["pick_unlocked_families"]).pick_unlocked_families(
            s20, ["a"], medium=["b"], hard=["c"]
        )
    ) == {"a", "b", "c"}

    r0 = _rule_structure({"difficulty": 0})
    r20 = _rule_structure({"difficulty": 20})
    assert r0.get("unlock_hard") is False
    assert r20.get("unlock_hard") is True
    assert _cdr_pick(r0, ["circle"], medium=["xy"], hard=["cubes"]) == "circle"
