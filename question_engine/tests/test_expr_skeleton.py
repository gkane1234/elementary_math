"""Tests for OpenStax form → Diff(F(u)) skeleton pattern fill."""

from __future__ import annotations

import random

from question_engine.frameworks.primitives.expr_skeleton import (
    FORM_PATTERNS,
    has_form_pattern,
    pattern_for_form,
    sample_expr_from_pattern,
    sample_from_form,
    richness_from_conceptual,
)
from question_engine.frameworks.primitives.poly_expression import Mul, Fn, Pow
from question_engine.frameworks.primitives.derivatives import sample_derivative_expression
from question_engine.frameworks.primitives.expression_flesh import (
    CORE_FLESH_MOVES,
    eligible_moves,
)


def test_all_implemented_forms_have_patterns() -> None:
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        load_form_catalog,
    )

    catalog = load_form_catalog("derivatives")
    for form in catalog.get("forms") or []:
        fid = str(form.get("form_id") or "")
        status = str(form.get("generation_status") or "")
        if status == "stub" or not fid:
            continue
        assert has_form_pattern(fid), f"missing pattern for {fid}"
        assert pattern_for_form(fid) is not None


def test_prod_pattern_emits_mul() -> None:
    pat = FORM_PATTERNS["trig_product_chain"]
    rng = random.Random(11)
    rich = richness_from_conceptual(8.0)
    expr, meta = sample_expr_from_pattern(
        pat,
        richness=rich,
        allows={"allow_trig": True},
        rng=rng,
    )
    assert meta["skeleton_kind"] == "diff_prod_fg_u"
    assert isinstance(expr, Mul)
    assert len(expr.factors) == 2
    assert all(isinstance(f, Fn) for f in expr.factors)


def test_quot_pattern_emits_mul_pow_neg() -> None:
    rng = random.Random(5)
    expr, _d, body, deriv, inv = sample_from_form(
        "quotient_poly",
        conceptual_d=4.0,
        rng=rng,
    )
    assert inv["skeleton_kind"] == "diff_quot_fg_u"
    assert isinstance(expr, Mul)
    assert any(isinstance(f, Pow) and f.exp == -1 for f in expr.factors)
    assert body and deriv
    assert "quotient" in inv.get("methods_used", [])


def test_power_poly_pattern() -> None:
    rng = random.Random(3)
    expr, _d, body, deriv, inv = sample_from_form(
        "power_poly", conceptual_d=0.0, rng=rng
    )
    assert inv["core_form_id"] == "power_poly"
    assert inv.get("skeleton_kind") == "diff_pow_h_n"
    assert "x" in body


def test_demoted_flesh_moves_not_in_core() -> None:
    assert "add_cancel_const" not in CORE_FLESH_MOVES
    assert "cancel_quot_bait" not in CORE_FLESH_MOVES
    el = eligible_moves(leaf="derivative_power_rule", allows={})
    assert "add_cancel_const" not in el
    assert "cancel_quot_bait" not in el


def test_deriv_wire_uses_skeleton_for_pilot_form() -> None:
    sample = sample_derivative_expression(
        {
            "conceptual_difficulty": 4.0,
            "spec_difficulty": 0.0,
            "conceptual_seed": 42,
            "spec_seed": 99,
            "allow_trig": True,
            "allow_product": True,
        },
        generator_key="derivative_product_rule",
    )
    meta = sample.metadata
    fid = str(meta.get("core_form_id") or meta.get("form_id") or "")
    assert fid
    if has_form_pattern(fid):
        assert meta.get("skeleton_source") == "expr_skeleton"
        assert meta.get("skeleton_pattern")


def test_spec_does_not_change_pattern() -> None:
    base = {
        "conceptual_difficulty": 8.0,
        "conceptual_seed": 1001,
        "allow_trig": True,
        "allow_product": True,
    }
    a = sample_derivative_expression(
        {**base, "spec_difficulty": 0.0, "spec_seed": 1},
        generator_key="derivative_trigonometric",
    )
    b = sample_derivative_expression(
        {**base, "spec_difficulty": 24.0, "spec_seed": 2},
        generator_key="derivative_trigonometric",
    )
    ma, mb = a.metadata, b.metadata
    if ma.get("form_id") == mb.get("form_id") and has_form_pattern(
        str(ma.get("form_id") or "")
    ):
        assert ma.get("skeleton_pattern") == mb.get("skeleton_pattern")
