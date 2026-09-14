"""OpenStax Algebra 1 form catalogs + wired leaf sampling."""

from __future__ import annotations

from question_engine.api.handler import _generate_for_type
from question_engine.frameworks.primitives.openstax_form_catalogs import (
    catalog_gaps,
    forms_for_leaf,
    implemented_forms,
    load_form_catalog,
    select_form_id,
)


A1_CATALOGS = (
    "algebra1_factoring",
    "algebra1_linear_equations",
    "algebra1_polynomials",
    "algebra1_rationals",
    "algebra1_radicals",
    "algebra1_quadratics",
)


def test_a1_catalogs_load_and_have_forms():
    totals = {}
    for name in A1_CATALOGS:
        cat = load_form_catalog(name)
        assert cat.get("catalog_id") == name
        forms = cat.get("forms") or []
        assert len(forms) >= 4, name
        totals[name] = {
            "total": len(forms),
            "implemented": len(implemented_forms(cat)),
            "gaps": len(catalog_gaps(cat)),
        }
        for f in forms:
            assert f.get("form_id"), name
            assert f.get("generation_status") in {
                "implemented",
                "stub",
                "deferred",
            }
    # Sanity: factoring is the richest wired catalog
    assert totals["algebra1_factoring"]["implemented"] >= 6
    assert totals["algebra1_factoring"]["gaps"] >= 1


def test_factoring_leaf_filters():
    cat = load_form_catalog("algebra1_factoring")
    qf = {str(f["form_id"]) for f in forms_for_leaf(cat, "quadratic_factoring")}
    assert "trinomial_x2_bx_c" in qf
    assert "trinomial_ax2_bx_c" in qf
    assert "gcf_monomial" not in qf

    sp = {str(f["form_id"]) for f in forms_for_leaf(cat, "polynomial_factoring_special_cases")}
    assert sp <= {"difference_of_squares", "perfect_square_trinomial"}

    gen = {str(f["form_id"]) for f in forms_for_leaf(cat, "polynomial_factoring_general_strategy")}
    assert "gcf_monomial" in gen
    assert "factor_by_grouping" in gen
    assert "gcf_then_pattern" in gen


def test_select_form_id_respects_d_min():
    import random

    cat = load_form_catalog("algebra1_factoring")
    forms = forms_for_leaf(cat, "quadratic_factoring")
    rng = random.Random(0)
    low = {select_form_id(forms, d=2.0, rng=rng)["form_id"] for _ in range(40)}
    assert "trinomial_ax2_bx_c" not in low
    assert "trinomial_x2_bx_c" in low
    high = {select_form_id(forms, d=14.0, rng=rng)["form_id"] for _ in range(60)}
    assert "trinomial_ax2_bx_c" in high


def _meta_form_id(q) -> str:
    meta = getattr(q, "metadata", None) or {}
    if not isinstance(meta, dict):
        return ""
    return str(meta.get("form_id") or meta.get("openstax_form") or "")


def test_wired_factoring_leaves_emit_form_ids():
    cat = load_form_catalog("algebra1_factoring")
    implemented = {str(f["form_id"]) for f in implemented_forms(cat)}

    for tid, min_distinct in (
        ("quadratic_factoring", 2),
        ("polynomial_factoring_special_cases", 2),
        ("polynomial_factoring_general_strategy", 4),
    ):
        seen: set[str] = set()
        for d, seed0 in ((2.0, 11), (8.0, 40), (14.0, 90), (20.0, 140)):
            for seed in range(seed0, seed0 + 12):
                qs = _generate_for_type(
                    tid,
                    {
                        "difficulty": d,
                        "count": 1,
                        "seed": seed,
                        "include_answer_key": True,
                    },
                )
                assert qs, (tid, d, seed)
                fid = _meta_form_id(qs[0])
                assert fid in implemented, (tid, d, seed, fid, qs[0].prompt_latex)
                assert qs[0].metadata.get("openstax_form") == fid
                assert qs[0].metadata.get("construction") == "forward_form_catalog"
                seen.add(fid)
        assert len(seen) >= min_distinct, (tid, seen)


def test_linear_equation_leaves_emit_form_ids():
    cat = load_form_catalog("algebra1_linear_equations")
    implemented = {str(f["form_id"]) for f in implemented_forms(cat)}
    one = {str(f["form_id"]) for f in forms_for_leaf(cat, "one_step_equations")}
    two = {str(f["form_id"]) for f in forms_for_leaf(cat, "two_step_equations")}
    multi = {str(f["form_id"]) for f in forms_for_leaf(cat, "multi_step_equations")}
    assert one <= {"one_step_add_sub", "one_step_mul_div"}
    assert "two_step" in two
    assert "vars_both_sides" in multi
    assert "multi_step_distribute" in multi

    for tid, allowed in (
        ("one_step_equations", one),
        ("two_step_equations", two),
        ("multi_step_equations", multi),
    ):
        seen: set[str] = set()
        for d, seed in ((0.0, 3), (8.0, 11), (16.0, 21)):
            qs = _generate_for_type(
                tid,
                {
                    "difficulty": d,
                    "count": 1,
                    "seed": seed,
                    "include_answer_key": True,
                    "integers_only": True,
                    "only_x": True,
                },
            )
            assert qs, (tid, d, seed)
            meta = qs[0].metadata or {}
            assert meta.get("skeleton_pattern") == "SolveLinear"
            fid = _meta_form_id(qs[0])
            assert fid in implemented, (tid, d, seed, fid)
            assert fid in allowed or fid in implemented
            seen.add(fid)
        assert seen, tid


def test_linear_inequality_and_literal_leaves_emit_form_ids():
    cat = load_form_catalog("algebra1_linear_equations")
    one_i = {str(f["form_id"]) for f in forms_for_leaf(cat, "one_step_inequalities")}
    two_i = {str(f["form_id"]) for f in forms_for_leaf(cat, "two_step_inequalities")}
    multi_i = {str(f["form_id"]) for f in forms_for_leaf(cat, "multi_step_inequalities")}
    lit = {str(f["form_id"]) for f in forms_for_leaf(cat, "literal_equations")}
    assert one_i <= {"one_step_ineq_add_sub", "one_step_ineq_mul_div"}
    assert "two_step_ineq" in two_i
    assert "vars_both_sides_ineq" in multi_i
    assert "multi_step_ineq_distribute" in multi_i
    assert lit == {"literal_equation"}

    for tid, allowed, pat in (
        ("one_step_inequalities", one_i, "SolveInequality"),
        ("two_step_inequalities", two_i, "SolveInequality"),
        ("multi_step_inequalities", multi_i, "SolveInequality"),
        ("literal_equations", lit, "SolveLiteral"),
    ):
        qs = _generate_for_type(
            tid,
            {
                "difficulty": 0.0,
                "count": 1,
                "seed": 5,
                "include_answer_key": True,
                "integers_only": True,
                "only_x": True,
            },
        )
        assert qs, tid
        meta = qs[0].metadata or {}
        assert meta.get("skeleton_pattern") == pat
        fid = _meta_form_id(qs[0])
        assert fid in allowed, (tid, fid, allowed)


def test_rational_simplification_stamps_simplify_cancel():
    for seed in range(20, 35):
        qs = _generate_for_type(
            "rational_simplification",
            {
                "difficulty": 8.0,
                "count": 1,
                "seed": seed,
                "include_answer_key": True,
            },
        )
        assert qs
        meta = qs[0].metadata or {}
        assert meta.get("form_id") == "simplify_cancel"
        assert meta.get("catalog_id") == "algebra1_rationals"
        assert meta.get("construction") == "forward_form_catalog"
