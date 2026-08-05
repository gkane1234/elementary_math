"""Algebraic ML metadata + Spec packs + PFD facade (A1/A2/PC)."""

from __future__ import annotations

import random

from question_engine.frameworks.primitives.algebraic_ml import enrich_algebraic_meta
from question_engine.frameworks.primitives.partial_fractions import (
    apply_pfd_continuous_knobs,
    combine_pf_to_rational,
    pfd_term_count_from_d,
)
from question_engine.frameworks.primitives.poly_expression import (
    ExpressionSpec,
    pack_compose_algebraic,
    pack_poly_expand,
    pack_poly_factor,
    pack_poly_product,
    pack_power_rule,
    sample_expression,
    spec_snapshot,
)
from question_engine.frameworks.primitives.registry import build_context
from question_engine.ml.schema import build_generation_record
from question_engine.generators.primitive_polynomial import simplify_polynomials
from question_engine.generators.primitive_rational import (
    partial_fraction_decomposition,
    rational_add_subtract,
    rational_simplify,
)


def test_algebraic_spec_packs_sample_and_snapshot():
    for pack_fn, d in (
        (pack_poly_expand, 8.0),
        (pack_poly_product, 10.0),
        (pack_poly_factor, 12.0),
        (pack_compose_algebraic, 14.0),
    ):
        spec = pack_fn(d, course_tag="a1")
        assert isinstance(spec, ExpressionSpec)
        assert spec.course_tag == "a1"
        snap = spec_snapshot(spec)
        assert snap["course_tag"] == "a1"
        assert "degree_max" in snap
        expr = sample_expression(spec, rng=random.Random(42))
        assert expr is not None


def test_algebraic_packs_do_not_break_power_rule_defaults():
    """Calc power-rule pack still samples; new Spec fields default harmlessly."""
    spec = pack_power_rule(6.0)
    assert spec.course_tag == ""
    assert spec.factor_count_min == 1
    assert spec.composition_depth == 0
    expr = sample_expression(spec, rng=random.Random(7))
    assert expr is not None


def test_enrich_algebraic_meta_emits_snapshot():
    meta = enrich_algebraic_meta(
        {"primitive_engine": "construct_poly", "degree": 3, "n_terms": 4},
        pack="structured_poly_simplify",
        generator="simplify_polynomials",
        methods_used=["expand", "simplify"],
        answer="x^2+1",
        course_tag="a1",
    )
    assert meta["spec_snapshot"]["pack"] == "structured_poly_simplify"
    assert meta["structure_id"].startswith("simplify_polynomials:")
    assert meta["effort_features"]["answer_len"] == len("x^2+1")
    assert "algebraic" in meta["function_classes"]


def test_pfd_knobs_and_wrap_construct_pfd():
    assert pfd_term_count_from_d(3.0) == 2
    assert pfd_term_count_from_d(10.0) == 3
    assert pfd_term_count_from_d(20.0) == 4
    knobs = apply_pfd_continuous_knobs({"difficulty": 10})
    assert knobs["pfd_term_count"] == 3
    ctx = build_context(
        {"difficulty": 8, "seed": 11},
        ["numbers", "variable"],
        leaf_id="pc_partial_fraction_decomposition",
    )
    surface = combine_pf_to_rational(ctx, d=8.0, n_terms=2)
    assert surface.level == "L4"
    assert surface.simplified_latex
    assert "pfd" in (surface.metadata.get("mode") or "")


def test_a1_poly_and_rational_emit_spec_snapshot():
    qs = simplify_polynomials(
        "simplify_polynomials",
        {"difficulty": 8, "count": 1, "include_answer_key": True, "seed": 21},
    )
    assert qs
    meta = qs[0].metadata or {}
    assert isinstance(meta.get("spec_snapshot"), dict)
    assert meta["spec_snapshot"].get("pack")
    rec = build_generation_record("simplify_polynomials", qs[0], {"difficulty": 8, "seed": 21})
    assert rec.theta_full.get("spec_snapshot") or rec.structural_features.get("spec_snapshot")

    rs = rational_simplify(
        "rational_simplification",
        {"difficulty": 6, "count": 1, "include_answer_key": True, "seed": 22},
    )
    assert rs[0].metadata.get("spec_snapshot", {}).get("pack") == "structured_rational_simplify"

    ra = rational_add_subtract(
        "rational_expression_simplification",
        {"difficulty": 8, "count": 1, "include_answer_key": True, "seed": 23},
    )
    assert ra[0].metadata.get("spec_snapshot", {}).get("pack") == "structured_rational_add"


def test_pc_pfd_emits_structured_snapshot():
    qs = partial_fraction_decomposition(
        "pc_partial_fraction_decomposition",
        {"difficulty": 10, "count": 1, "include_answer_key": True, "seed": 31},
    )
    assert qs
    snap = qs[0].metadata.get("spec_snapshot") or {}
    assert snap.get("pack") == "structured_pfd"
    # Term count may follow OpenStax form_id (2–4) rather than D-only knobs.
    n = snap.get("pfd_term_count") or qs[0].metadata.get("pfd_term_count")
    assert n in {2, 3, 4}
    assert "partial_fractions" in (qs[0].metadata.get("methods_used") or [])
    assert qs[0].metadata.get("form_id")
    assert qs[0].metadata.get("openstax_form") == qs[0].metadata.get("form_id")
