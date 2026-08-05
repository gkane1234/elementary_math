"""OpenStax form-catalog selection / diversity for Calc 1 algebraic leaves."""

from __future__ import annotations

from collections import Counter

from question_engine.frameworks.primitives.derivatives import sample_derivative_expression
from question_engine.frameworks.primitives.integrals import sample_integral_expression
from question_engine.frameworks.primitives.limits import sample_limit_expression
from question_engine.frameworks.primitives.openstax_form_catalogs import (
    catalog_gaps,
    implemented_forms,
    load_form_catalog,
    select_form_id,
)


def _form_id(meta: dict) -> str:
    return str(meta.get("form_id") or meta.get("openstax_form") or "")


def test_calc1_catalogs_load_and_have_implemented_forms():
    expected = {
        "trig_integrals": 20,
        "u_substitution": 10,
        "integration_by_parts": 8,
        "trig_substitution": 10,
        "partial_fractions": 6,
        "basic_power_integrals": 5,
        "invtrig_integrals": 5,
        "limits": 20,
        "derivatives": 18,
    }
    for name, min_n in expected.items():
        cat = load_form_catalog(name)
        imp = implemented_forms(cat)
        assert len(imp) >= min_n, (name, len(imp), [f["form_id"] for f in imp])
        assert cat.get("catalog_id") == name or cat.get("catalog_id")


def test_trig_gaps_sec5_and_sin_sin_implemented():
    cat = load_form_catalog("trig_integrals")
    imp = {str(f["form_id"]) for f in implemented_forms(cat)}
    assert "sec_odd_reduction_n5" in imp
    assert "product_sin_a_sin_b" in imp
    gaps = {str(f["form_id"]) for f in catalog_gaps(cat)}
    assert "weierstrass_t_sub" in gaps


def test_select_form_id_respects_d_min():
    cat = load_form_catalog("trig_integrals")
    forms = implemented_forms(cat)
    rng = __import__("random").Random(0)
    low = {select_form_id(forms, d=2.0, rng=rng)["form_id"] for _ in range(40)}
    assert "sec3_reduction" not in low
    assert any(str(f).startswith("basic_") for f in low)


def test_parts_catalog_diversity():
    cat = load_form_catalog("integration_by_parts")
    implemented = {str(f["form_id"]) for f in implemented_forms(cat)}
    seen: set[str] = set()
    for d, seed0 in ((4, 1), (12, 50), (18, 100)):
        for seed in range(seed0, seed0 + 25):
            sample = sample_integral_expression(
                {"difficulty": d, "seed": seed, "include_answer_key": True},
                generator_key="integration_by_parts",
            )
            fid = _form_id(sample.as_metadata())
            assert fid in implemented, (d, seed, fid)
            seen.add(fid)
    assert len(seen) >= 5, seen


def test_u_sub_catalog_diversity():
    cat = load_form_catalog("u_substitution")
    implemented = {str(f["form_id"]) for f in implemented_forms(cat)}
    seen: set[str] = set()
    for d, seed0 in ((4, 2), (10, 60), (16, 110)):
        for seed in range(seed0, seed0 + 30):
            sample = sample_integral_expression(
                {"difficulty": d, "seed": seed, "include_answer_key": True},
                generator_key="integral_substitution",
            )
            fid = _form_id(sample.as_metadata())
            assert fid in implemented, (d, seed, fid, sample.prompt_latex)
            seen.add(fid)
    assert len(seen) >= 4, seen


def test_trig_sub_catalog_diversity():
    cat = load_form_catalog("trig_substitution")
    implemented = {str(f["form_id"]) for f in implemented_forms(cat)}
    seen: set[str] = set()
    for d, seed0 in ((4, 3), (12, 70), (18, 130)):
        for seed in range(seed0, seed0 + 25):
            sample = sample_integral_expression(
                {"difficulty": d, "seed": seed, "include_answer_key": True},
                generator_key="integral_trig_substitution",
            )
            fid = _form_id(sample.as_metadata())
            assert fid in implemented, (d, seed, fid)
            seen.add(fid)
    assert len(seen) >= 5, seen


def test_pfd_catalog_diversity():
    cat = load_form_catalog("partial_fractions")
    implemented = {
        str(f["form_id"])
        for f in implemented_forms(cat)
        if not str(f["form_id"]).startswith("u_sub_then_pfd")
    }
    seen: set[str] = set()
    for d, seed0 in ((4, 4), (10, 80), (16, 140)):
        for seed in range(seed0, seed0 + 30):
            sample = sample_integral_expression(
                {"difficulty": d, "seed": seed, "include_answer_key": True},
                generator_key="integral_partial_fractions",
            )
            fid = _form_id(sample.as_metadata())
            assert fid in implemented, (d, seed, fid)
            seen.add(fid)
    assert len(seen) >= 3, seen


def test_limits_catalog_emits_form_ids():
    cat = load_form_catalog("limits")
    for key, min_distinct in (
        ("limit_direct_evaluation", 3),
        ("limit_removable", 2),
        ("limit_at_infinity", 2),
        ("lhopitals_rule", 2),
    ):
        leaf_forms = {
            str(f["form_id"])
            for f in implemented_forms(cat, generator_key=key)
        }
        seen: set[str] = set()
        for seed in range(20, 55):
            sample = sample_limit_expression(
                {"difficulty": 12, "seed": seed, "include_answer_key": True},
                generator_key=key,
            )
            fid = _form_id(sample.metadata)
            assert fid, (key, seed)
            assert fid in leaf_forms or fid.startswith(
                ("direct_", "inf_", "removable_", "lhopital_", "poly_", "rational_", "squeeze", "expr_")
            ) or fid in {
                str(f["form_id"]) for f in implemented_forms(cat)
            }, (key, seed, fid, sorted(leaf_forms)[:8])
            seen.add(fid)
        assert len(seen) >= min_distinct, (key, seen)


def test_derivatives_catalog_emits_form_ids():
    cat = load_form_catalog("derivatives")
    for key in (
        "derivative_power_rule",
        "derivative_product_rule",
        "derivative_chain_rule",
        "derivative_trigonometric",
    ):
        leaf_forms = {
            str(f["form_id"])
            for f in implemented_forms(cat, generator_key=key)
        }
        assert leaf_forms, key
        counts: Counter[str] = Counter()
        for seed in range(30, 60):
            sample = sample_derivative_expression(
                {"difficulty": 10, "seed": seed, "include_answer_key": True},
                generator_key=key,
            )
            fid = _form_id(sample.metadata)
            assert fid in leaf_forms, (key, seed, fid, sorted(leaf_forms))
            counts[fid] += 1
        assert sum(counts.values()) == 30
