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


def test_chain_topic_requires_chain_specials_opt_in() -> None:
    allow = resolve_derivative_allows({}, generator_key="derivative_chain_rule")
    assert allow.require_chain is True
    assert allow.allow_chain is True
    # Algebraic leaf: specials OFF by default (checkbox opt-in)
    assert allow.allow_trig is False
    assert allow.allow_exp is False
    assert allow.allow_log is False
    on = resolve_derivative_allows(
        {"allow_trig": True, "allow_exp": True, "allow_log": True},
        generator_key="derivative_chain_rule",
    )
    assert on.allow_trig is True
    assert on.allow_exp is True
    assert on.allow_log is True


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
    hits = 0
    for seed in range(50):
        sample = sample_derivative_expression(
            {
                "difficulty": 0,
                "seed": seed,
                "allow_trig": True,
                "include_answer_key": True,
            },
            generator_key="derivative_quotient_rule",
        )
        assert "quotient" in sample.methods_used
        if "trig" in sample.function_classes:
            hits += 1
    assert hits >= 8


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
