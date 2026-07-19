"""Tests for enriched calculus derivative-rule generators."""

from __future__ import annotations

import pytest

from question_engine.generators.calculus_derivative_rules import GENERATORS


KEYS = tuple(GENERATORS.keys())


@pytest.mark.parametrize("key", KEYS)
@pytest.mark.parametrize("tier", ("easy", "medium", "hard"))
def test_derivative_rule_generators_produce_variety(key: str, tier: str) -> None:
    qs = GENERATORS[key](
        key,
        {"count": 8, "difficulty_tier": tier, "include_answer_key": True},
    )
    assert len(qs) == 8
    prompts = {q.prompt_latex for q in qs}
    assert len(prompts) >= 2
    for q in qs:
        assert q.prompt_latex
        assert q.answer_latex


def test_catalog_wires_derivative_rule_stubs() -> None:
    from question_engine.catalogs.calculus import CATALOG

    by_id = {e.id: e for e in CATALOG}
    assert by_id["calc_diff_instantaneous_rates_of_change"].generator == (
        "instantaneous_rate_of_change"
    )
    assert by_id["calc_diff_inverse_functions"].generator == (
        "derivative_inverse_functions"
    )
    assert by_id["calc_diff_logarithmic"].generator == "derivative_logarithmic"
    assert by_id["calc_diff_power_rule"].generator == "derivative_power_rule"


def test_logarithmic_prompts_mention_technique() -> None:
    qs = GENERATORS["derivative_logarithmic"](
        "calc_diff_logarithmic",
        {"count": 6, "difficulty_tier": "medium", "include_answer_key": True},
    )
    assert any("logarithmic" in (q.prompt_latex or "").lower() for q in qs)
