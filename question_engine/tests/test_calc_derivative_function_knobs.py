"""Tests for calculus derivative function/method allow-lists + continuous D."""

from __future__ import annotations

import pytest

from question_engine.frameworks.primitives.derivatives import (
    resolve_derivative_allows,
    sample_derivative_expression,
    topic_allow_defaults,
)
from question_engine.generators.calculus_derivative_rules import GENERATORS
from question_engine.settings.params import derivative_rule_structure_from_continuous


def test_product_rule_seed_stable_across_calls() -> None:
    """Seeded Spec sampling must not depend on frozenset iteration order."""
    settings = {
        "difficulty": 12,
        "seed": 110157,
        "include_answer_key": True,
        "allow_trig": True,
        "allow_exp": True,
        "allow_log": True,
        "allow_product": True,
        "require_product": True,
    }
    a = sample_derivative_expression(
        settings, generator_key="derivative_product_rule"
    ).prompt_latex
    b = sample_derivative_expression(
        settings, generator_key="derivative_product_rule"
    ).prompt_latex
    assert a == b
    assert a  # non-empty


def test_algebraic_topic_defaults_exclude_specials() -> None:
    defaults = topic_allow_defaults("derivative_power_rule")
    assert defaults["allow_trig"] is False
    assert defaults["allow_exp"] is False
    assert defaults["allow_log"] is False
    assert defaults["allow_hyperbolic"] is False
    assert defaults["allow_invtrig"] is False
    assert defaults["allow_chain"] is False
    assert defaults["allow_product"] is False


def test_trig_topic_defaults_include_trig_only() -> None:
    defaults = topic_allow_defaults("derivative_trigonometric")
    assert defaults["allow_trig"] is True
    assert defaults["allow_exp"] is False
    assert defaults["allow_log"] is False
    assert defaults["allow_chain"] is True
    assert defaults["allow_product"] is True


def test_chain_topic_requires_chain_specials_on_by_default() -> None:
    allow = resolve_derivative_allows({}, generator_key="derivative_chain_rule")
    assert allow.require_chain is True
    assert allow.allow_chain is True
    # OpenStax §3.6 leaf: specials ON; D-unlocks keep D=0 algebraic.
    assert allow.allow_trig is True
    assert allow.allow_exp is True
    assert allow.allow_log is True
    off = resolve_derivative_allows(
        {"allow_trig": False, "allow_exp": False, "allow_log": False},
        generator_key="derivative_chain_rule",
    )
    assert off.allow_trig is False
    assert off.allow_exp is False
    assert off.allow_log is False


def test_product_topic_specials_opt_in() -> None:
    allow = resolve_derivative_allows({}, generator_key="derivative_product_rule")
    assert allow.require_product is True
    assert allow.allow_trig is False
    assert allow.allow_exp is False
    assert allow.allow_log is False
    on = resolve_derivative_allows(
        {"allow_trig": True},
        generator_key="derivative_product_rule",
    )
    assert on.allow_trig is True


def test_quotient_topic_specials_opt_in_no_soft_unlock() -> None:
    allow = resolve_derivative_allows({}, generator_key="derivative_quotient_rule")
    assert allow.require_quotient is True
    assert allow.allow_trig is False
    assert allow.allow_exp is False
    assert allow.allow_log is False
    off = resolve_derivative_allows(
        {"allow_trig": False, "allow_exp": False, "allow_log": False},
        generator_key="derivative_quotient_rule",
    )
    assert off.allow_trig is False
    on = resolve_derivative_allows(
        {"allow_trig": True},
        generator_key="derivative_quotient_rule",
    )
    assert on.allow_trig is True

    # Structure: checked → available at D=0; unchecked → off at high D
    from question_engine.frameworks.primitives.derivatives import (
        derivative_rule_structure,
    )

    d0_on = derivative_rule_structure(
        {"difficulty": 0, "allow_trig": True},
        generator_key="derivative_quotient_rule",
    )
    d20_off = derivative_rule_structure(
        {"difficulty": 20, "allow_trig": False},
        generator_key="derivative_quotient_rule",
    )
    assert d0_on["allow_trig"] is True
    assert d20_off["allow_trig"] is False

def test_settings_can_force_include_exclude() -> None:
    off = resolve_derivative_allows(
        {"allow_trig": False},
        generator_key="derivative_trigonometric",
    )
    assert off.allow_trig is False
    on = resolve_derivative_allows(
        {"allow_trig": True, "allow_exp": True},
        generator_key="derivative_power_rule",
    )
    assert on.allow_trig is True
    assert on.allow_exp is True


def test_power_rule_samples_exclude_trig_by_default() -> None:
    for d in (0, 8, 20):
        for seed in range(12):
            sample = sample_derivative_expression(
                {"difficulty": d, "seed": seed, "include_answer_key": True},
                generator_key="derivative_power_rule",
            )
            assert "trig" not in sample.function_classes
            assert "exp" not in sample.function_classes
            assert "log" not in sample.function_classes
            assert "invtrig" not in sample.function_classes
            assert "hyperbolic" not in sample.function_classes


def test_trig_topic_samples_include_trig() -> None:
    hits = 0
    for seed in range(20):
        sample = sample_derivative_expression(
            {"difficulty": 6, "seed": seed, "include_answer_key": True},
            generator_key="derivative_trigonometric",
        )
        if "trig" in sample.function_classes:
            hits += 1
    assert hits >= 15


def test_high_d_uses_more_methods_when_allowed() -> None:
    easy_methods: set[str] = set()
    hard_methods: set[str] = set()
    easy_classes: set[str] = set()
    hard_classes: set[str] = set()
    for seed in range(30):
        e = sample_derivative_expression(
            {
                "difficulty": 2,
                "seed": seed,
                "allow_trig": True,
                "allow_exp": True,
                "allow_log": True,
                "allow_chain": True,
                "allow_product": True,
                "allow_quotient": True,
            },
            generator_key="derivative_chain_rule",
        )
        h = sample_derivative_expression(
            {
                "difficulty": 22,
                "seed": seed,
                "allow_trig": True,
                "allow_exp": True,
                "allow_log": True,
                "allow_chain": True,
                "allow_product": True,
                "allow_quotient": True,
            },
            generator_key="derivative_chain_rule",
        )
        easy_methods.update(e.methods_used)
        hard_methods.update(h.methods_used)
        easy_classes.update(e.function_classes)
        hard_classes.update(h.function_classes)
        assert e.chain_depth >= 1 or "chain" in e.methods_used
    # High D should unlock class variety and/or deeper nesting when allowed
    assert len(hard_classes) >= len(easy_classes)
    assert max(
        sample_derivative_expression(
            {
                "difficulty": 22,
                "seed": s,
                "allow_trig": True,
                "allow_chain": True,
                "require_chain": True,
            },
            generator_key="derivative_chain_rule",
        ).chain_depth
        for s in range(40)
    ) >= max(
        sample_derivative_expression(
            {
                "difficulty": 2,
                "seed": s,
                "allow_trig": True,
                "allow_chain": True,
                "require_chain": True,
            },
            generator_key="derivative_chain_rule",
        ).chain_depth
        for s in range(40)
    )


def test_metadata_fields_present() -> None:
    sample = sample_derivative_expression(
        {"difficulty": 10, "seed": 1, "include_answer_key": True},
        generator_key="derivative_product_rule",
    )
    meta = sample.as_metadata()
    assert "function_classes" in meta
    assert "methods_used" in meta
    assert "chain_depth" in meta
    assert "product" in sample.methods_used


def test_generator_emits_metadata() -> None:
    qs = GENERATORS["derivative_power_rule"](
        "calc_diff_power_rule",
        {"count": 3, "difficulty": 5, "include_answer_key": True, "seed": 7},
    )
    assert len(qs) == 3
    for q in qs:
        assert "function_classes" in q.metadata
        assert "methods_used" in q.metadata
        assert "chain_depth" in q.metadata


def test_force_exclude_trig_on_trig_topic() -> None:
    for seed in range(15):
        sample = sample_derivative_expression(
            {
                "difficulty": 15,
                "seed": seed,
                "allow_trig": False,
                "allow_chain": True,
                "allow_product": True,
            },
            generator_key="derivative_trigonometric",
        )
        assert "trig" not in sample.function_classes


def test_continuous_structure_respects_allow_gate() -> None:
    # Bare continuous probe: allows open → available from D=0 (no soft unlock).
    open_s = derivative_rule_structure_from_continuous({"difficulty": 0})
    closed = derivative_rule_structure_from_continuous(
        {"difficulty": 8, "allow_trig": False, "allow_exp": False, "allow_log": False}
    )
    assert open_s is not None and closed is not None
    assert open_s["allow_trig"] is True
    assert closed["allow_trig"] is False
    assert closed["allow_exp"] is False


def test_product_high_d_can_emit_trig() -> None:
    hits = 0
    for seed in range(40):
        sample = sample_derivative_expression(
            {
                "difficulty": 14,
                "seed": seed,
                "allow_trig": True,
                "include_answer_key": True,
            },
            generator_key="derivative_product_rule",
        )
        assert "product" in sample.methods_used
        if "trig" in sample.function_classes:
            hits += 1
    assert hits >= 8


def test_quotient_default_stays_algebraic_at_any_d() -> None:
    """Topic default: specials OFF — no soft unlock with D."""
    for d in (0, 2, 20):
        for seed in range(15):
            sample = sample_derivative_expression(
                {"difficulty": d, "seed": seed, "include_answer_key": True},
                generator_key="derivative_quotient_rule",
            )
            assert "quotient" in sample.methods_used
            assert r"\frac{" in sample.prompt_latex
            specials = set(sample.function_classes) - {"algebraic", "roots"}
            assert not specials


def test_quotient_allow_trig_at_d0_can_emit_trig() -> None:
    """allow_trig is a hard gate; at D=0 trig is rare (C schedule), not free.

    Opt-in + modest D should be able to emit trig; D=0 may still be mostly algebraic.
    """
    hits_low = 0
    hits_mid = 0
    for seed in range(50):
        low = sample_derivative_expression(
            {
                "difficulty": 0,
                "seed": seed,
                "allow_trig": True,
                "include_answer_key": True,
            },
            generator_key="derivative_quotient_rule",
        )
        mid = sample_derivative_expression(
            {
                "difficulty": 8,
                "seed": seed,
                "allow_trig": True,
                "include_answer_key": True,
            },
            generator_key="derivative_quotient_rule",
        )
        assert "quotient" in low.methods_used
        assert "quotient" in mid.methods_used
        if "trig" in low.function_classes:
            hits_low += 1
        if "trig" in mid.function_classes:
            hits_mid += 1
    # Mid D with allow_trig should reliably surface trig; low D stays mostly core.
    assert hits_mid >= 8
    assert hits_low <= hits_mid


def test_quotient_allow_trig_false_at_d20_never_trig() -> None:
    for seed in range(30):
        sample = sample_derivative_expression(
            {
                "difficulty": 20,
                "seed": seed,
                "allow_trig": False,
                "allow_exp": False,
                "allow_log": False,
                "include_answer_key": True,
            },
            generator_key="derivative_quotient_rule",
        )
        assert "trig" not in sample.function_classes
        assert "exp" not in sample.function_classes
        assert "log" not in sample.function_classes


def test_quotient_high_d_can_emit_specials() -> None:
    hits = 0
    seen: set[str] = set()
    for seed in range(50):
        sample = sample_derivative_expression(
            {
                "difficulty": 16,
                "seed": seed,
                "allow_trig": True,
                "allow_exp": True,
                "allow_log": True,
                "include_answer_key": True,
            },
            generator_key="derivative_quotient_rule",
        )
        assert "quotient" in sample.methods_used
        assert r"\frac{" in sample.prompt_latex
        specials = set(sample.function_classes) - {"algebraic", "roots"}
        if specials:
            hits += 1
            seen.update(specials)
        assert isinstance(sample.metadata.get("spec_snapshot"), dict)
        assert sample.metadata.get("form_id") or sample.metadata.get("shape_id")
    assert hits >= 10
    assert seen & {"trig", "exp", "log"}

def test_chain_high_d_can_emit_trig() -> None:
    hits = 0
    for seed in range(40):
        sample = sample_derivative_expression(
            {
                "difficulty": 16,
                "seed": seed,
                "allow_trig": True,
                "allow_exp": False,
                "allow_log": False,
                "allow_roots": False,
                "include_answer_key": True,
            },
            generator_key="derivative_chain_rule",
        )
        if "trig" in sample.function_classes:
            hits += 1
    assert hits >= 8


def test_trig_high_d_multi_fn_structure() -> None:
    """Trig leaf at high D should produce multi-Fn products or nested chains."""
    import random

    from question_engine.frameworks.primitives.poly_expression import (
        Fn,
        Mul,
        pack_special_atom,
        sample_expression,
    )

    def count_fns(expr: object) -> int:
        if isinstance(expr, Fn):
            return 1 + count_fns(expr.arg)
        if isinstance(expr, Mul):
            return sum(count_fns(f) for f in expr.factors)
        if hasattr(expr, "terms"):
            return sum(count_fns(t) for t in expr.terms)  # type: ignore[attr-defined]
        if hasattr(expr, "base"):
            return count_fns(expr.base)  # type: ignore[attr-defined]
        return 0

    multi = 0
    for seed in range(40):
        spec = pack_special_atom(18.0, primary="trig", prefer_chained_fn=True)
        expr = sample_expression(spec, rng=random.Random(seed))
        if count_fns(expr) >= 3 or (
            isinstance(expr, Mul) and count_fns(expr) >= 2
        ):
            multi += 1
        sample = sample_derivative_expression(
            {"difficulty": 18, "seed": seed, "include_answer_key": True},
            generator_key="derivative_trigonometric",
        )
        assert "trig" in sample.function_classes
    assert multi >= 15


def test_general_topic_defaults_all_allows_on() -> None:
    defaults = topic_allow_defaults("derivative_general")
    assert defaults["allow_trig"] is True
    assert defaults["allow_exp"] is True
    assert defaults["allow_log"] is True
    assert defaults["allow_invtrig"] is True
    assert defaults["allow_hyperbolic"] is True
    assert defaults["allow_roots"] is True
    assert defaults["allow_chain"] is True
    assert defaults["allow_product"] is True
    assert defaults["allow_quotient"] is True


def test_general_topic_samples_multiple_classes() -> None:
    seen: set[str] = set()
    for seed in range(60):
        sample = sample_derivative_expression(
            {"difficulty": 18, "seed": seed, "include_answer_key": True},
            generator_key="derivative_general",
        )
        seen.update(sample.function_classes)
        assert sample.prompt_latex
        assert sample.answer_latex
        assert "effort_features" in sample.metadata or "d_spend" in sample.metadata
    specials = seen - {"algebraic", "roots"}
    assert len(specials) >= 3


def test_deep_mixed_chain_via_chain_leaf_with_allows() -> None:
    """Chain leaf with many allows + high D can emit heterogeneous nests."""
    mixed = 0
    deep = 0
    for seed in range(50):
        sample = sample_derivative_expression(
            {
                "difficulty": 22,
                "seed": seed,
                "allow_trig": True,
                "allow_exp": True,
                "allow_log": True,
                "allow_invtrig": True,
                "allow_chain": True,
                "require_chain": True,
                "include_answer_key": True,
            },
            generator_key="derivative_chain_rule",
        )
        specials = set(sample.function_classes) - {"algebraic", "roots"}
        if len(specials) >= 2:
            mixed += 1
        if sample.chain_depth >= 3 or int(sample.metadata.get("nest_depth") or 0) >= 3:
            deep += 1
    assert mixed >= 5
    assert deep >= 3


def test_d25_budgets_not_absurd() -> None:
    from question_engine.frameworks.primitives.derivatives import structure_knobs_from_d

    knobs = structure_knobs_from_d(25.0)
    assert knobs["coef_hi"] <= 7
    assert knobs["term_budget"] <= 4
    for seed in range(20):
        sample = sample_derivative_expression(
            {
                "difficulty": 25,
                "seed": seed,
                "allow_trig": True,
                "allow_exp": True,
                "allow_log": True,
                "allow_chain": True,
                "require_chain": True,
                "include_answer_key": True,
            },
            generator_key="derivative_chain_rule",
        )
        n_factors = int(sample.metadata.get("n_factors") or 0)
        nest = int(sample.metadata.get("nest_depth") or 0)
        assert n_factors <= 4
        assert nest <= 5
        assert sample.coef_hi <= 7


def test_fn_power_appears_in_trig_samples() -> None:
    hits = 0
    for seed in range(50):
        sample = sample_derivative_expression(
            {"difficulty": 14, "seed": seed, "include_answer_key": True},
            generator_key="derivative_trigonometric",
        )
        body = sample.prompt_latex
        if any(t in body for t in (r"\sin^{", r"\cos^{", r"\tan^{", r"\ln^{")):
            hits += 1
        if sample.metadata.get("has_fn_power"):
            hits += 1
    assert hits >= 5


def test_general_generator_live_path() -> None:
    qs = GENERATORS["derivative_general"](
        "calc_diff_general",
        {"count": 5, "difficulty": 16, "include_answer_key": True, "seed": 11},
    )
    assert len(qs) == 5
    for q in qs:
        assert q.prompt_latex
        assert "function_classes" in q.metadata


def test_higher_order_uses_spec_order_at_least_two() -> None:
    for seed in range(12):
        sample = sample_derivative_expression(
            {"difficulty": 10, "seed": seed, "include_answer_key": True},
            generator_key="derivative_higher_order",
        )
        assert int(sample.metadata.get("derivative_order") or 0) >= 2
        assert isinstance(sample.metadata.get("spec_snapshot"), dict)
        assert sample.prompt_latex
        assert "d^{" in sample.prompt_latex or "''" in sample.prompt_latex


def test_first_deriv_leaves_stay_order_one_at_d22() -> None:
    """Specialty Diff leaves must not bleed d²/dx² at high D (notes flag)."""
    keys = (
        "derivative_power_rule",
        "derivative_product_rule",
        "derivative_quotient_rule",
        "derivative_chain_rule",
        "derivative_trigonometric",
        "derivative_ln_exp",
        "derivative_inverse_trig",
        "derivative_general",
    )
    for key in keys:
        for seed in range(8):
            sample = sample_derivative_expression(
                {"difficulty": 22, "seed": seed, "include_answer_key": True},
                generator_key=key,
            )
            assert int(sample.metadata.get("derivative_order") or 0) == 1, key
            assert "d^{2}" not in sample.prompt_latex
            assert "d^{3}" not in sample.prompt_latex
            assert sample.metadata.get("skeleton_pattern")


def test_quotient_leaf_form_id_matches_algebraic_flesh() -> None:
    """Without allow_exp/log, quotient forms must stay poly (not mislabeled)."""
    for seed in range(16):
        sample = sample_derivative_expression(
            {"difficulty": 16, "seed": seed, "include_answer_key": True},
            generator_key="derivative_quotient_rule",
        )
        fid = str(sample.metadata.get("form_id") or "")
        assert fid in {"", "quotient_poly"} or fid.startswith("quotient_poly"), (
            f"unexpected form_id={fid!r} seed={seed} body={sample.prompt_latex}"
        )
        assert "quotient_exp" not in fid
        assert "quotient_log" not in fid
        assert "mixed_special" not in fid
        body = sample.prompt_latex
        assert r"e^{" not in body
        assert r"\ln" not in body
        assert r"\sin" not in body


def test_power_root_form_keeps_fractional_power() -> None:
    from question_engine.frameworks.primitives.expr_skeleton import sample_from_form

    for seed in range(12):
        _e, _d, body, _der, inv = sample_from_form(
            "power_root",
            conceptual_d=8.0,
            allows={"allow_roots": True, "allow_chain": False},
            seed=seed,
        )
        assert inv.get("skeleton_pattern")
        assert r"\frac{" in body or "^{" in body
        # Fractional exponent marker (p/q) — not a bare poly sum alone.
        assert "/" in body or r"\frac" in body


def test_structured_gap_packs_emit_ml_metadata() -> None:
    for key, type_id, pack_token in (
        ("derivative_other_base", "calc_diff_other_base_logarithms_and_exponentials", "structured_other_base"),
        ("derivative_logarithmic", "calc_diff_logarithmic", "structured_logarithmic"),
        ("derivative_implicit", "calc_diff_implicit", "structured_implicit"),
    ):
        qs = GENERATORS[key](
            type_id,
            {"count": 3, "difficulty": 12, "include_answer_key": True, "seed": 42},
        )
        assert len(qs) == 3
        for q in qs:
            meta = q.metadata or {}
            assert meta.get("generator") == key
            assert meta.get("function_classes")
            assert meta.get("methods_used")
            snap = meta.get("spec_snapshot") or {}
            assert snap.get("pack") == pack_token
            assert "effort_features" in meta
            assert q.prompt_latex


def test_implicit_d0_circle_only() -> None:
    from question_engine.api.handler import _generate_for_type

    forms: set[str] = set()
    for seed in range(20):
        q = _generate_for_type(
            "calc_diff_implicit",
            {"difficulty": 0, "seed": seed, "count": 1, "include_answer_key": True},
        )[0]
        fid = (q.metadata or {}).get("form_id")
        forms.add(str(fid))
        assert fid == "implicit_basic", (seed, fid, q.prompt_latex)
        assert r"^{2}" in (q.prompt_latex or "")
        assert r"^{3}" not in (q.prompt_latex or "")
    assert forms == {"implicit_basic"}


def test_implicit_high_d_catalog_variety() -> None:
    from question_engine.api.handler import _generate_for_type

    forms: set[str] = set()
    for seed in range(36):
        q = _generate_for_type(
            "calc_diff_implicit",
            {"difficulty": 22, "seed": seed, "count": 1, "include_answer_key": True},
        )[0]
        fid = str((q.metadata or {}).get("form_id") or "")
        assert fid != "implicit_basic", (seed, q.prompt_latex)
        assert fid.startswith("implicit_"), (seed, fid)
        forms.add(fid)
        assert q.answer_latex
    assert len(forms) >= 3, forms
    assert forms & {"implicit_trig", "implicit_exp", "implicit_folium", "implicit_cubes"}


def test_logdiff_d0_power_only() -> None:
    from question_engine.api.handler import _generate_for_type

    forms: set[str] = set()
    for seed in range(20):
        q = _generate_for_type(
            "calc_diff_logarithmic",
            {"difficulty": 0, "seed": seed, "count": 1, "include_answer_key": True},
        )[0]
        fid = (q.metadata or {}).get("form_id")
        forms.add(str(fid))
        assert fid == "logdiff_power", (seed, fid, q.prompt_latex)
        assert r"^{x}" not in (q.prompt_latex or "")
        assert r"\sin" not in (q.prompt_latex or "")
        assert r"\sqrt" not in (q.prompt_latex or "")
        assert "logarithmic" in (q.prompt_latex or "").lower()
    assert forms == {"logdiff_power"}


def test_logdiff_mid_d_product_root_quotient() -> None:
    from question_engine.api.handler import _generate_for_type

    allowed = {
        "logdiff_product_powers",
        "logdiff_quotient_powers",
        "logdiff_root",
    }
    forms: set[str] = set()
    for seed in range(24):
        q = _generate_for_type(
            "calc_diff_logarithmic",
            {"difficulty": 8, "seed": seed, "count": 1, "include_answer_key": True},
        )[0]
        fid = str((q.metadata or {}).get("form_id") or "")
        assert fid in allowed, (seed, fid, q.prompt_latex)
        forms.add(fid)
    assert len(forms) >= 2, forms


def test_logdiff_high_d_catalog_variety() -> None:
    from question_engine.api.handler import _generate_for_type

    forms: set[str] = set()
    for seed in range(36):
        q = _generate_for_type(
            "calc_diff_logarithmic",
            {"difficulty": 22, "seed": seed, "count": 1, "include_answer_key": True},
        )[0]
        fid = str((q.metadata or {}).get("form_id") or "")
        assert fid != "logdiff_power", (seed, q.prompt_latex)
        assert fid.startswith("logdiff_"), (seed, fid)
        forms.add(fid)
        assert q.answer_latex
    assert len(forms) >= 2, forms
    assert forms & {"logdiff_x_x", "logdiff_a_x", "logdiff_trig_x"}


def test_other_base_d0_a_x_or_log_x_only() -> None:
    from question_engine.api.handler import _generate_for_type

    forms: set[str] = set()
    for seed in range(20):
        q = _generate_for_type(
            "calc_diff_other_base_logarithms_and_exponentials",
            {"difficulty": 0, "seed": seed, "count": 1, "include_answer_key": True},
        )[0]
        fid = str((q.metadata or {}).get("form_id") or "")
        forms.add(fid)
        assert fid in {"other_base_a_x", "other_base_log_x"}, (seed, fid, q.prompt_latex)
        p = q.prompt_latex or ""
        assert r"^{2}" not in p
        assert r"\cdot" not in p or r"\log_" in p
    assert forms == {"other_base_a_x", "other_base_log_x"}


def test_other_base_mid_d_chain_only() -> None:
    from question_engine.api.handler import _generate_for_type

    allowed = {"other_base_a_kx", "other_base_log_linear"}
    forms: set[str] = set()
    for seed in range(24):
        q = _generate_for_type(
            "calc_diff_other_base_logarithms_and_exponentials",
            {"difficulty": 8, "seed": seed, "count": 1, "include_answer_key": True},
        )[0]
        fid = str((q.metadata or {}).get("form_id") or "")
        assert fid in allowed, (seed, fid, q.prompt_latex)
        if fid == "other_base_a_kx":
            assert r"\cdot" in (q.answer_latex or ""), (seed, q.answer_latex)
        forms.add(fid)
    assert forms == allowed


def test_other_base_high_d_catalog_variety() -> None:
    from question_engine.api.handler import _generate_for_type

    forms: set[str] = set()
    for seed in range(36):
        q = _generate_for_type(
            "calc_diff_other_base_logarithms_and_exponentials",
            {"difficulty": 22, "seed": seed, "count": 1, "include_answer_key": True},
        )[0]
        fid = str((q.metadata or {}).get("form_id") or "")
        assert fid not in {"other_base_a_x", "other_base_log_x"}, (seed, q.prompt_latex)
        assert fid.startswith("other_base_"), (seed, fid)
        forms.add(fid)
        assert q.answer_latex
    assert len(forms) >= 2, forms
    assert forms & {"other_base_a_poly", "other_base_log_power", "other_base_product"}


def test_invfn_d0_power_only() -> None:
    from question_engine.api.handler import _generate_for_type

    forms: set[str] = set()
    for seed in range(20):
        q = _generate_for_type(
            "calc_diff_inverse_functions",
            {"difficulty": 0, "seed": seed, "count": 1, "include_answer_key": True},
        )[0]
        fid = (q.metadata or {}).get("form_id")
        forms.add(str(fid))
        assert fid == "invfn_power", (seed, fid, q.prompt_latex)
        p = q.prompt_latex or ""
        assert r"e^{" not in p
        assert r"\sin" not in p
        assert r"\ln" not in p
    assert forms == {"invfn_power"}


def test_invfn_mid_d_table_linear() -> None:
    from question_engine.api.handler import _generate_for_type

    allowed = {"invfn_table", "invfn_linear"}
    forms: set[str] = set()
    for seed in range(24):
        q = _generate_for_type(
            "calc_diff_inverse_functions",
            {"difficulty": 8, "seed": seed, "count": 1, "include_answer_key": True},
        )[0]
        fid = str((q.metadata or {}).get("form_id") or "")
        assert fid in allowed, (seed, fid, q.prompt_latex)
        forms.add(fid)
    assert forms == allowed


def test_invfn_high_d_not_exp_leftover() -> None:
    from question_engine.api.handler import _generate_for_type

    forms: set[str] = set()
    for seed in range(36):
        q = _generate_for_type(
            "calc_diff_inverse_functions",
            {"difficulty": 22, "seed": seed, "count": 1, "include_answer_key": True},
        )[0]
        fid = str((q.metadata or {}).get("form_id") or "")
        assert fid not in {"invfn_power", "invfn_exp"}, (seed, fid, q.prompt_latex)
        assert fid.startswith("invfn_"), (seed, fid)
        forms.add(fid)
        assert q.answer_latex
    assert len(forms) >= 2, forms
    assert forms & {"invfn_trig", "invfn_ln", "invfn_cubic"}


def _chain_specials(sample) -> set[str]:
    return set(sample.function_classes) - {"algebraic", "roots"}


def test_chain_d0_stays_simple_one_composition() -> None:
    """D=0 matches old easy: one power of an affine, no unlike nest."""
    for seed in range(24):
        sample = sample_derivative_expression(
            {"difficulty": 0, "seed": seed, "include_answer_key": True},
            generator_key="derivative_chain_rule",
        )
        fid = str(sample.metadata.get("form_id") or "")
        assert fid == "chain_power_linear", (seed, fid, sample.prompt_latex)
        assert sample.chain_depth <= 1
        layers = sample.metadata.get("compose_layers") or []
        assert layers.count("pow") <= 1
        assert not _chain_specials(sample)
        assert "d^{2}" not in sample.prompt_latex


def test_chain_mid_d_rotates_unlike_classes() -> None:
    """D=8: still f(g(x)), but trig/exp/ln appear when defaults are on."""
    forms: set[str] = set()
    specials: set[str] = set()
    deep = 0
    for seed in range(50):
        sample = sample_derivative_expression(
            {"difficulty": 8, "seed": seed, "include_answer_key": True},
            generator_key="derivative_chain_rule",
        )
        fid = str(sample.metadata.get("form_id") or "")
        forms.add(fid)
        specials |= _chain_specials(sample)
        layers = list(sample.metadata.get("compose_layers") or [])
        if len(layers) >= 3:
            deep += 1
        assert fid != "chain_nested_power"
        assert sample.metadata.get("form_id")
        assert sample.function_classes
    assert "chain_trig_poly" in forms or "trig" in specials
    assert specials & {"trig", "exp", "log"}
    assert deep <= 8


def test_chain_high_d_not_dominated_by_nested_power() -> None:
    """D=16/22: unlike nests; chain_nested_power must not dominate."""
    counts: dict[str, int] = {}
    specials: set[str] = set()
    deep = 0
    mixed = 0
    for d in (16, 22):
        for seed in range(40):
            sample = sample_derivative_expression(
                {"difficulty": d, "seed": seed, "include_answer_key": True},
                generator_key="derivative_chain_rule",
            )
            fid = str(sample.metadata.get("form_id") or "")
            counts[fid] = counts.get(fid, 0) + 1
            spec = _chain_specials(sample)
            specials |= spec
            layers = list(sample.metadata.get("compose_layers") or [])
            if len(layers) >= 2 or sample.chain_depth >= 2:
                deep += 1
            if len(spec) >= 2 or (
                spec and "pow" in layers and spec
            ):
                mixed += 1
            body = sample.prompt_latex
            assert sample.metadata.get("form_id")
            assert "d^{2}" not in body
    assert counts.get("chain_nested_power", 0) == 0
    assert specials & {"trig", "exp", "log"}
    assert len(specials) >= 2
    assert deep >= 20
    # At least one non-power form must appear often.
    unlike_forms = sum(
        n for fid, n in counts.items() if fid != "chain_power_linear"
    )
    assert unlike_forms >= 20, counts


def test_chain_nest_depth_scales_with_d() -> None:
    """More compositions at high D — not just nastier coefficients."""
    def layer_counts(d: float, n: int = 36) -> list[int]:
        out = []
        for seed in range(n):
            sample = sample_derivative_expression(
                {"difficulty": d, "seed": seed, "include_answer_key": True},
                generator_key="derivative_chain_rule",
            )
            layers = list(sample.metadata.get("compose_layers") or [])
            out.append(max(len(layers), int(sample.chain_depth or 0)))
        return out

    d0 = layer_counts(0)
    d8 = layer_counts(8)
    d16 = layer_counts(16)
    d22 = layer_counts(22)
    assert max(d0) <= 1
    assert sum(1 for n in d8 if n <= 2) >= 24
    assert sum(1 for n in d16 if n >= 2) >= 8
    assert max(d22) >= max(d0)
    assert sum(1 for n in d22 if n >= 2) >= sum(1 for n in d0 if n >= 2)


def test_live_product_d0_no_three_deep_nest() -> None:
    from question_engine.api.handler import _generate_for_type

    for seed in range(16):
        q = _generate_for_type(
            "calc_diff_product_rule",
            {"difficulty": 0, "seed": seed, "count": 1, "include_answer_key": True},
        )[0]
        meta = q.metadata or {}
        fid = str(meta.get("form_id") or "")
        assert fid in {"", "product_two_poly"}, (seed, fid, q.prompt_latex)
        assert int(meta.get("chain_depth") or 0) < 3, q.prompt_latex
        assert "product" in (meta.get("methods_used") or [])


def test_live_product_high_d_can_emit_nested_factor() -> None:
    from question_engine.api.handler import _generate_for_type

    hits = 0
    for seed in range(40):
        q = _generate_for_type(
            "calc_diff_product_rule",
            {"difficulty": 16, "seed": seed, "count": 1, "include_answer_key": True},
        )[0]
        meta = q.metadata or {}
        methods = set(meta.get("methods_used") or [])
        assert "product" in methods, q.prompt_latex
        assert int(meta.get("chain_depth") or 0) < 3, q.prompt_latex
        if "chain" in methods and int(meta.get("chain_depth") or 0) >= 1:
            hits += 1
    assert hits >= 5, hits
