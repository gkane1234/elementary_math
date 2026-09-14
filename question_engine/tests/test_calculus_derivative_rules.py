"""Tests for enriched calculus derivative-rule generators."""

from __future__ import annotations

from collections import Counter

import pytest

from question_engine.api.handler import _generate_for_type
from question_engine.generators.calculus_derivative_rules import (
    GENERATORS,
    definition_of_derivative_forms_for_difficulty,
)


def _gen_def(type_id: str, d: float, *, seed: int = 101, count: int = 1):
    return _generate_for_type(
        type_id,
        {
            "difficulty": d,
            "seed": seed,
            "count": count,
            "include_answer_key": True,
        },
    )


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


_DEF_TYPE = "calc_app_diff_limits_in_form_of_definition_of_derivative"
_EASY = {"limit_h", "limit_x"}
_MEDIUM = {"cube", "linear_coef", "named"}
_HARD = {"reciprocal", "sqrt", "poly"}


def test_definition_of_derivative_d0_limit_high_d_hard_lockout() -> None:
    assert definition_of_derivative_forms_for_difficulty(0) == ("limit_h", "limit_x")
    med = definition_of_derivative_forms_for_difficulty(8)
    assert _EASY <= set(med) and _MEDIUM <= set(med)
    assert med == ("limit_h", "limit_x", "cube", "linear_coef", "named")
    hard = definition_of_derivative_forms_for_difficulty(16)
    assert hard == ("cube", "linear_coef", "named", "reciprocal", "sqrt", "poly")
    assert not (_EASY & set(hard))
    assert definition_of_derivative_forms_for_difficulty(22) == (
        "reciprocal",
        "sqrt",
        "poly",
    )

    q0 = _gen_def(_DEF_TYPE, 0, seed=101)[0]
    assert (q0.metadata or {}).get("form_id") in _EASY
    assert (q0.metadata or {}).get("generator") == "definition_of_derivative"
    p0 = q0.prompt_latex or ""
    assert r"\lim_" in p0
    assert r"^{3}" not in p0
    assert "Use the definition" not in p0
    snap = (q0.metadata or {}).get("spec_snapshot") or {}
    assert snap.get("form_id") in _EASY
    assert snap.get("generator") == "definition_of_derivative"

    mid = set()
    for seed in range(40):
        q = _gen_def(_DEF_TYPE, 8, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        mid.add(fid)
        assert fid in _EASY | _MEDIUM
        assert (q.metadata or {}).get("generator") == "definition_of_derivative"
        p = q.prompt_latex or ""
        assert r"\sqrt{" not in p
    assert mid & _EASY
    assert mid & _MEDIUM
    assert mid <= _EASY | _MEDIUM

    high = set()
    for seed in range(40):
        q = _gen_def(_DEF_TYPE, 16, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        high.add(fid)
        assert fid not in _EASY
        p = q.prompt_latex or ""
        assert r"\lim_{x\to" not in p
        assert (q.metadata or {}).get("generator") == "definition_of_derivative"
    assert high <= _MEDIUM | _HARD
    assert high & _HARD

    expert = set()
    for seed in range(30):
        q = _gen_def(_DEF_TYPE, 22, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        expert.add(fid)
        assert fid in _HARD
        p = q.prompt_latex or ""
        assert r"\lim_{x\to" not in p
        assert (q.metadata or {}).get("generator") == "definition_of_derivative"
        snap = (q.metadata or {}).get("spec_snapshot") or {}
        assert snap.get("form_id") in _HARD
        assert snap.get("generator") == "definition_of_derivative"
    assert expert <= _HARD
    assert expert & _HARD


def test_definition_of_derivative_quality_weights_tilt() -> None:
    from contextlib import nullcontext

    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        live_quality_form_weights,
    )

    def _counts(weights):
        c = Counter()
        ctx = live_quality_form_weights(weights) if weights else nullcontext()
        with ctx:
            for i in range(240):
                q = GENERATORS["definition_of_derivative"](
                    _DEF_TYPE,
                    {
                        "difficulty": 8.0,
                        "seed": i,
                        "count": 1,
                        "include_answer_key": True,
                        "live_quality_form_weights": weights,
                    },
                )[0]
                c[(q.metadata or {}).get("form_id")] += 1
        return c

    baseline = _counts(None)
    tilted = _counts({"limit_x": -2.5, "named": 2.5})
    assert tilted["named"] > baseline["named"]
