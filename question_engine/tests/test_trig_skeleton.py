"""Tests for trig skeleton species (PC §7.1–7.5)."""

from __future__ import annotations

from question_engine.api.handler import _generate_for_type
from question_engine.frameworks.primitives import build_context
from question_engine.frameworks.primitives.trig_skeleton import (
    sample_trig_double_angle_item,
    sample_trig_factor_eq_item,
    sample_trig_product_to_sum_item,
    sample_trig_rewrite_item,
    sample_trig_sum_diff_item,
    use_trig_double_angle_skeleton,
    use_trig_factor_eq_skeleton,
    use_trig_identity_skeleton,
    use_trig_product_to_sum_skeleton,
    use_trig_sum_diff_skeleton,
)
from question_engine.generators import GENERATORS


def test_use_trig_identity_skeleton_defaults_and_opt_out():
    assert use_trig_identity_skeleton({}) is True
    assert use_trig_identity_skeleton({"use_sample_trig_identities": True}) is False
    assert use_trig_identity_skeleton({"use_trig_identity_skeleton": False}) is False
    assert use_trig_identity_skeleton({"skeleton_pattern": "trig_basic_identities"}) is False


def test_sample_trig_rewrite_d0_single_step():
    ctx = build_context(
        {"difficulty": 0.0, "seed": 101},
        [],
        leaf_id="pc_fundamental_identities",
    )
    item = sample_trig_rewrite_item(ctx, leaf_id="pc_fundamental_identities")
    assert item.metadata.get("skeleton_pattern") == "TrigRewrite"
    assert item.n_steps >= 1
    assert r"\text{Simplify:" in item.prompt_latex or r"\text{Verify:" in item.prompt_latex
    assert item.answer_latex


def test_sample_trig_rewrite_high_d_compound():
    ctx = build_context(
        {"difficulty": 16.0, "seed": 207},
        [],
        leaf_id="pc_fundamental_identities",
    )
    item = sample_trig_rewrite_item(ctx, leaf_id="pc_fundamental_identities")
    assert item.metadata.get("format_tier", 0) >= 1
    assert item.n_steps >= 1


def test_live_default_uses_skeleton():
    qs = _generate_for_type(
        "pc_fundamental_identities",
        {"difficulty": 0.0, "seed": 101, "count": 1, "include_answer_key": True},
    )
    meta = qs[0].metadata or {}
    assert meta.get("skeleton_pattern") == "TrigRewrite"
    assert meta.get("primitive_engine") == "trig_skeleton"
    assert qs[0].prompt_latex
    assert qs[0].answer_latex


def test_opt_out_restores_old_path():
    qs = _generate_for_type(
        "pc_fundamental_identities",
        {
            "difficulty": 0.0,
            "seed": 101,
            "count": 1,
            "include_answer_key": True,
            "use_sample_trig_identities": True,
        },
    )
    meta = qs[0].metadata or {}
    assert meta.get("skeleton_pattern") != "TrigRewrite"
    assert meta.get("primitive_engine") == "trig_basic_identities"


def test_high_d_unlocks_more_steps():
    low = _generate_for_type(
        "pc_fundamental_identities",
        {"difficulty": 0.0, "seed": 101, "count": 5, "include_answer_key": True},
    )
    high = _generate_for_type(
        "pc_fundamental_identities",
        {"difficulty": 16.0, "seed": 101, "count": 5, "include_answer_key": True},
    )
    low_steps = {int((q.metadata or {}).get("n_steps") or 1) for q in low}
    high_steps = {int((q.metadata or {}).get("n_steps") or 1) for q in high}
    assert max(high_steps) >= max(low_steps)


def test_generator_registry_overrides_precalc():
    assert GENERATORS["trig_basic_identities"].__module__.endswith("primitive_precalc")
    assert GENERATORS["trig_sum_difference"].__module__.endswith("primitive_precalc")
    assert GENERATORS["trig_multiple_angle"].__module__.endswith("primitive_precalc")
    assert GENERATORS["trig_product_to_sum"].__module__.endswith("primitive_precalc")
    assert GENERATORS["trig_factoring_equations"].__module__.endswith("primitive_precalc")


def test_sum_diff_d0_expand_sin_cos_only():
    assert use_trig_sum_diff_skeleton({}) is True
    ctx = build_context(
        {"difficulty": 0.0, "seed": 101},
        [],
        leaf_id="pc_sum_and_difference_identities",
    )
    item = sample_trig_sum_diff_item(ctx, leaf_id="pc_sum_and_difference_identities")
    assert item.metadata.get("skeleton_pattern") == "TrigSumDiff"
    assert "Expand" in item.prompt_latex or r"\text{Expand" in item.prompt_latex
    assert "tan" not in item.prompt_latex.lower()
    assert "exact value" not in item.prompt_latex.lower()


def test_sum_diff_live_and_opt_out():
    qs = _generate_for_type(
        "pc_sum_and_difference_identities",
        {"difficulty": 0.0, "seed": 101, "count": 1, "include_answer_key": True},
    )
    assert (qs[0].metadata or {}).get("skeleton_pattern") == "TrigSumDiff"
    old = _generate_for_type(
        "pc_sum_and_difference_identities",
        {
            "difficulty": 0.0,
            "seed": 101,
            "count": 1,
            "include_answer_key": True,
            "use_sample_trig_identities": True,
        },
    )
    assert (old[0].metadata or {}).get("primitive_engine") == "trig_sum_difference"
    assert (old[0].metadata or {}).get("skeleton_pattern") != "TrigSumDiff"


def test_sum_diff_high_d_unlocks_tan_or_exact():
    rules = set()
    for seed in (101, 207, 313, 419, 521):
        qs = _generate_for_type(
            "pc_sum_and_difference_identities",
            {"difficulty": 16.0, "seed": seed, "count": 3, "include_answer_key": True},
        )
        for q in qs:
            rules.add(str((q.metadata or {}).get("rule_id") or ""))
    assert any("tan" in r or "cos_" in r or "sin_" in r for r in rules)


def test_double_angle_live():
    assert use_trig_double_angle_skeleton({}) is True
    qs = _generate_for_type(
        "pc_multiple_angle_identities",
        {"difficulty": 0.0, "seed": 101, "count": 1, "include_answer_key": True},
    )
    meta = qs[0].metadata or {}
    assert meta.get("skeleton_pattern") == "TrigDoubleAngle"
    assert "double-angle" in qs[0].prompt_latex
    ctx = build_context(
        {"difficulty": 0.0, "seed": 101},
        [],
        leaf_id="pc_multiple_angle_identities",
    )
    item = sample_trig_double_angle_item(ctx, leaf_id="pc_multiple_angle_identities")
    assert item.rule_id in {"sin_2", "cos_2_diff"}


def test_product_to_sum_live():
    assert use_trig_product_to_sum_skeleton({}) is True
    qs = _generate_for_type(
        "pc_product_to_sum_identities",
        {"difficulty": 0.0, "seed": 101, "count": 1, "include_answer_key": True},
    )
    meta = qs[0].metadata or {}
    assert meta.get("skeleton_pattern") == "TrigProductToSum"
    assert r"\sin A\cos B" in qs[0].prompt_latex or "as a sum" in qs[0].prompt_latex
    ctx = build_context(
        {"difficulty": 0.0, "seed": 101},
        [],
        leaf_id="pc_product_to_sum_identities",
    )
    item = sample_trig_product_to_sum_item(ctx, leaf_id="pc_product_to_sum_identities")
    assert item.rule_id == "sin_cos"


def test_factor_eq_live_gold_leaf():
    assert use_trig_factor_eq_skeleton({}) is True
    qs = _generate_for_type(
        "pc_equations_with_factoring_and_fundamental_identities",
        {"difficulty": 0.0, "seed": 101, "count": 1, "include_answer_key": True},
    )
    meta = qs[0].metadata or {}
    assert meta.get("skeleton_pattern") == "TrigFactorEq"
    assert r"\text{Solve" in qs[0].prompt_latex
    # D=0 must stay on quadratic-in-trig (old-path gold), not double-angle.
    assert meta.get("rule_id", "").startswith("quadratic") or "sin^2" in qs[0].prompt_latex
    ctx = build_context(
        {"difficulty": 0.0, "seed": 101},
        [],
        leaf_id="pc_equations_with_factoring_and_fundamental_identities",
    )
    item = sample_trig_factor_eq_item(
        ctx, leaf_id="pc_equations_with_factoring_and_fundamental_identities"
    )
    assert item.metadata.get("skeleton_pattern") == "TrigFactorEq"
    assert item.rule_id.startswith("quadratic")


def test_factor_eq_opt_out():
    qs = _generate_for_type(
        "pc_equations_with_factoring_and_fundamental_identities",
        {
            "difficulty": 0.0,
            "seed": 101,
            "count": 1,
            "include_answer_key": True,
            "use_sample_trig_equations": True,
        },
    )
    assert (qs[0].metadata or {}).get("skeleton_pattern") != "TrigFactorEq"
    assert (qs[0].metadata or {}).get("primitive_engine") == "trig_factoring_equations"


def test_low_variety_equations_leaf_stays_old_path():
    """pc_equations_and_multiple_angle_identities — LOW_VARIETY, gold not locked."""
    qs = _generate_for_type(
        "pc_equations_and_multiple_angle_identities",
        {"difficulty": 0.0, "seed": 101, "count": 1, "include_answer_key": True},
    )
    meta = qs[0].metadata or {}
    assert meta.get("skeleton_pattern") != "TrigFactorEq"
    assert meta.get("primitive_engine") == "trig_factoring_equations"
