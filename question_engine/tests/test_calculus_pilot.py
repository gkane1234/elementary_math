"""Focused tests for calculus pilot generators (expression variety)."""

from __future__ import annotations

import pytest

from question_engine.generators.calculus_pilot import GENERATORS


PILOT_KEYS = (
    "tangent_normal_line",
    "differentials",
    "linear_approximation",
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
        by_id["calc_app_diff_linear_approximations"].generator == "linear_approximation"
    )
    assert (
        by_id["calc_indef_int_logarithmic_rule_and_exponentials_with_substitution"].generator
        == "integral_log_exp_substitution"
    )


def test_differentials_emit_structure_family() -> None:
    gen = GENERATORS["differentials"]
    qs = gen(
        "differentials",
        {"count": 12, "difficulty": 18.0, "include_answer_key": True},
    )
    families = {q.metadata.get("family") for q in qs}
    assert None not in families
    assert len(families) >= 2
    assert all(q.metadata.get("structure_id", "").startswith("differentials:") for q in qs)


def test_linear_approximation_emit_structure_family() -> None:
    gen = GENERATORS["linear_approximation"]
    qs = gen(
        "linear_approximation",
        {"count": 12, "difficulty": 16.0, "include_answer_key": True},
    )
    families = {q.metadata.get("family") for q in qs}
    assert None not in families
    assert all(
        q.metadata.get("structure_id", "").startswith("linear_approximation:")
        for q in qs
    )
    assert families <= {"sqrt", "reciprocal", "exp"}
    assert "quad" not in families
    assert len(families) >= 2

