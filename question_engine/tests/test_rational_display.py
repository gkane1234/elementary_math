"""Tests for rational display rule engine (print-time standardization)."""

from __future__ import annotations

from fractions import Fraction
from types import SimpleNamespace

from question_engine.frameworks.primitives.factor_sampler import LinearFactor
from question_engine.frameworks.primitives.rational_display import (
    ABSORB_NESTED_NUMERIC_COEFF,
    FACTOR_JUXTAPOSITION,
    OMIT_COEFF_1,
    DISPLAY_PRESETS,
    format_leading_coef_times_den,
    plan_fraction_display,
    resolve_display_config,
    should_absorb_nested_numeric,
    try_absorb_constant_rational_num,
)
from question_engine.frameworks.primitives.rational_skeleton import _render_fraction


def _var(name: str = "x"):
    return SimpleNamespace(name=name, latex=name)


def test_try_absorb_constant_rational_only():
    fac = LinearFactor(a=Fraction(1), b=Fraction(2))  # x+2
    got = try_absorb_constant_rational_num({0: Fraction(3, 2)}, (fac,))
    assert got is not None
    assert got.num == {0: Fraction(3)}
    assert got.leading_den_coef == 2

    assert try_absorb_constant_rational_num({0: Fraction(3)}, (fac,)) is None
    assert try_absorb_constant_rational_num({0: Fraction(3, 2)}, ()) is None
    assert try_absorb_constant_rational_num({1: Fraction(1, 2)}, (fac,)) is None


def test_default_none_intent_polishes():
    """Missing/None intent + normalize → absorb (same as atomic_pf_term)."""
    assert should_absorb_nested_numeric(
        display_normalize=True, display_intent=None
    )
    assert should_absorb_nested_numeric(
        display_normalize=True, display_intent="atomic_pf_term"
    )
    cfg = resolve_display_config(display_normalize=True, display_intent=None)
    assert ABSORB_NESTED_NUMERIC_COEFF in cfg.active_rules
    assert cfg.preset == "standard_rational"


def test_intent_gate_blocks_opt_outs():
    assert not should_absorb_nested_numeric(
        display_normalize=True, display_intent="complex_fraction_skill"
    )
    assert not should_absorb_nested_numeric(
        display_normalize=True, display_intent="as_built"
    )
    assert not should_absorb_nested_numeric(
        display_normalize=False, display_intent=None
    )

    cf = resolve_display_config(
        display_normalize=True, display_intent="complex_fraction_skill"
    )
    assert ABSORB_NESTED_NUMERIC_COEFF not in cf.active_rules
    # as_built skips all rules
    built = resolve_display_config(display_normalize=True, display_intent="as_built")
    assert built.active_rules == ()


def test_standard_rational_preset_membership():
    rules = DISPLAY_PRESETS["standard_rational"]
    assert ABSORB_NESTED_NUMERIC_COEFF in rules
    assert FACTOR_JUXTAPOSITION in rules
    assert OMIT_COEFF_1 in rules


def test_plan_absorb_rule_applies():
    fac = LinearFactor(a=Fraction(1), b=Fraction(2))
    plan = plan_fraction_display(
        {0: Fraction(3, 2)},
        (fac,),
        display_intent=None,
    )
    assert plan.num == {0: Fraction(3)}
    assert plan.leading_den_coef == 2
    assert ABSORB_NESTED_NUMERIC_COEFF in plan.applied_rules
    assert FACTOR_JUXTAPOSITION in plan.applied_rules


def test_plan_skips_absorb_for_complex_fraction_skill():
    fac = LinearFactor(a=Fraction(1), b=Fraction(2))
    plan = plan_fraction_display(
        {0: Fraction(3, 2)},
        (fac,),
        display_intent="complex_fraction_skill",
    )
    assert plan.num == {0: Fraction(3, 2)}
    assert plan.leading_den_coef == 1
    assert ABSORB_NESTED_NUMERIC_COEFF not in plan.applied_rules


def test_render_fraction_unwraps_with_none_intent():
    """Default None intent: \\frac{\\frac{3}{2}}{x + 2} → flat form."""
    fac = LinearFactor(a=Fraction(1), b=Fraction(2))
    nested, _ = _render_fraction(
        {0: Fraction(3, 2)},
        (fac,),
        _var(),
        dens_style="factored",
        display_normalize=False,
        display_intent="as_built",
    )
    assert nested == r"\frac{\frac{3}{2}}{x + 2}"

    flat, _ = _render_fraction(
        {0: Fraction(3, 2)},
        (fac,),
        _var(),
        dens_style="factored",
        display_normalize=True,
        display_intent=None,
    )
    assert flat == r"\frac{3}{2\left(x + 2\right)}"
    # Safe default does NOT distribute to 2x+4.
    assert "2x" not in flat
    assert "2x + 4" not in flat


def test_render_fraction_preserves_complex_fraction_intent():
    fac = LinearFactor(a=Fraction(1), b=Fraction(2))
    latex, _ = _render_fraction(
        {0: Fraction(3, 2)},
        (fac,),
        _var(),
        dens_style="factored",
        display_normalize=True,
        display_intent="complex_fraction_skill",
    )
    assert latex == r"\frac{\frac{3}{2}}{x + 2}"


def test_render_fraction_atomic_pf_term_still_polishes():
    fac = LinearFactor(a=Fraction(1), b=Fraction(2))
    latex, _ = _render_fraction(
        {0: Fraction(3, 2)},
        (fac,),
        _var(),
        dens_style="factored",
        display_normalize=True,
        display_intent="atomic_pf_term",
    )
    assert latex == r"\frac{3}{2\left(x + 2\right)}"


def test_format_leading_coef_times_den_juxtaposition_no_distribute():
    assert format_leading_coef_times_den(1, "x + 2") == "x + 2"
    assert format_leading_coef_times_den(2, "x + 2") == r"2\left(x + 2\right)"
    assert (
        format_leading_coef_times_den(2, r"\left(x - 1\right)\left(x + 2\right)")
        == r"2\left(x - 1\right)\left(x + 2\right)"
    )


def test_explicit_display_rules_override_preset():
    cfg = resolve_display_config(
        display_normalize=True,
        display_intent=None,
        display_rules=[FACTOR_JUXTAPOSITION, OMIT_COEFF_1],
    )
    assert ABSORB_NESTED_NUMERIC_COEFF not in cfg.active_rules
    assert FACTOR_JUXTAPOSITION in cfg.active_rules


def test_settings_resolve_display_config():
    cfg = resolve_display_config(
        settings={
            "display_normalize": True,
            "display_intent": None,
            "display_preset": "standard_rational",
        }
    )
    assert ABSORB_NESTED_NUMERIC_COEFF in cfg.active_rules


def test_complex_fractions_stamps_opt_out_intent():
    from question_engine.generators.complex_fractions import generate_complex_fractions

    qs = generate_complex_fractions(
        "a2_rational_expressions_complex_fractions",
        {"count": 2, "difficulty": 5, "seed": 7, "include_answer_key": True},
    )
    assert qs
    for q in qs:
        assert q.metadata.get("display_intent") == "complex_fraction_skill"
