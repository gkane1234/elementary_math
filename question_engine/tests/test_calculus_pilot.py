"""Focused tests for calculus pilot generators (expression variety)."""

from __future__ import annotations

import pytest

from question_engine.generators.calculus_pilot import GENERATORS


PILOT_KEYS = (
    "tangent_normal_line",
    "differentials",
    "integral_log_exp_substitution",
)


@pytest.mark.parametrize("key", PILOT_KEYS)
@pytest.mark.parametrize("tier", ("easy", "medium", "hard"))
def test_pilot_generators_produce_prompts(key: str, tier: str) -> None:
    gen = GENERATORS[key]
    qs = gen(
        key,
        {
            "count": 8,
            "difficulty_tier": tier,
            "include_answer_key": True,
        },
    )
    assert len(qs) == 8
    prompts = {q.prompt_latex for q in qs}
    # Variety: not all identical stems
    assert len(prompts) >= 3
    for q in qs:
        assert q.prompt_latex
        assert q.answer_latex


def test_catalog_wires_pilot_generators() -> None:
    from question_engine.catalogs.calculus import CATALOG

    by_id = {e.id: e for e in CATALOG}
    assert by_id["calc_app_diff_slope_tangent_and_normal_lines"].generator == "tangent_normal_line"
    assert by_id["calc_app_diff_differentials"].generator == "differentials"
    assert (
        by_id["calc_indef_int_logarithmic_rule_and_exponentials_with_substitution"].generator
        == "integral_log_exp_substitution"
    )
