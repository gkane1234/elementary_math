"""Tests for GenerationRecord schema, effort scoring, and forward/inverse pilots."""

from __future__ import annotations

from question_engine.core.models import Question
from question_engine.ml.effort import has_effort_scorer, score_effort
from question_engine.ml.features import build_design_matrix, record_feature_dict
from question_engine.ml.forward import train_forward_model
from question_engine.ml.inverse import optimize_theta
from question_engine.ml.schema import GenerationRecord, build_generation_record


def test_build_generation_record_captures_theta_and_spend():
    q = Question(
        id="q1",
        topic="g6_introduction_to_ratios",
        prompt_latex=r"Write the ratio } 12:18",
        prompt_text="Write the ratio 12:18",
        answer_latex="2:3",
        metadata={
            "spend": {"numbers": 4.2},
            "sample_log": [{"lane": "friendly_wholes"}],
            "upgrades": ["ops:3"],
            "qa_flags": ["ok"],
        },
    )
    settings = {"difficulty": 10, "seed": 42, "count": 1}
    rec = build_generation_record(
        "g6_introduction_to_ratios",
        q,
        settings,
        y_effort=7.5,
        y_mode="simplify",
        effort_feats={"meaningful_steps": 2},
    )
    assert rec.type_id == "g6_introduction_to_ratios"
    assert rec.difficulty == 10.0
    assert rec.seed == 42
    assert rec.theta_full["difficulty"] == 10
    assert rec.theta_full["spend"]["numbers"] == 4.2
    assert rec.theta_full["upgrades"] == ["ops:3"]
    assert rec.y_effort == 7.5
    assert rec.y_mode == "simplify"
    assert "spend" in rec.structural_features
    d = rec.to_dict()
    assert d["prompt_latex"].startswith("Write the ratio")
    assert d["answer_latex"] == "2:3"


def test_score_effort_intro_ratios():
    assert has_effort_scorer("g6_introduction_to_ratios")
    effort, feats = score_effort(
        "g6_introduction_to_ratios",
        r"Write the ratio } 24:36",
        "2:3",
    )
    assert effort is not None
    assert effort > 4.0
    assert feats.get("form") == "simplify"
    assert feats.get("meaningful_steps", 0) >= 1

    missing, empty = score_effort("unknown_type_xyz", "anything")
    assert missing is None
    assert empty == {}


def test_forward_and_inverse_pilot_on_synthetic_records():
    records: list[GenerationRecord] = []
    for i, d in enumerate([0, 5, 10, 15, 20, 25] * 4):
        # Synthetic: effort roughly tracks difficulty with noise.
        effort = 2.0 + 0.7 * d + (i % 3) * 0.4
        records.append(
            GenerationRecord(
                type_id="g6_introduction_to_ratios",
                seed=1000 + i,
                difficulty=float(d),
                theta_full={"difficulty": float(d), "type_id": "g6_introduction_to_ratios"},
                prompt_latex=f"d={d}",
                prompt_text="",
                answer_latex="",
                answer_text="",
                y_effort=effort,
                effort_feats={"meaningful_steps": int(d // 5)},
            )
        )
    X, y, names, kept = build_design_matrix(records)
    assert len(y) == len(records)
    assert len(names) >= 1
    assert len(kept) == len(records)

    model = train_forward_model(records, prefer_gbr=False, seed=1, test_fraction=0.25)
    assert model.model_kind == "ridge"
    assert model.metrics["n_train"] >= 4
    # Should recover positive correlation with difficulty.
    assert model.metrics["pearson_r"] > 0.5

    cand = optimize_theta(
        model,
        "g6_introduction_to_ratios",
        target_effort=12.0,
        n_candidates=80,
        seed=2,
        vary_extra_bounds=False,
    )
    assert cand.abs_error < 4.0
    assert 0.0 <= float(cand.theta["difficulty"]) <= 25.0


def test_record_feature_dict_flattens_spend():
    rec = GenerationRecord(
        type_id="g6_equivalent_ratios",
        seed=1,
        difficulty=8.0,
        theta_full={"difficulty": 8.0, "spend": {"numbers": 3.5, "ooo": 1.0}},
        prompt_latex="",
        prompt_text="",
        answer_latex="",
        answer_text="",
        structural_features={"n_ops": 4},
        y_effort=9.0,
    )
    feats = record_feature_dict(rec)
    assert feats["spend_numbers"] == 3.5
    assert feats["n_ops"] == 4.0
    assert feats["type_id"] == "g6_equivalent_ratios"


def test_derivative_knobs_and_spec_land_on_record_and_features():
    """Derivative allow_* / Spec exponent knobs must not be dropped by export."""
    q = Question(
        id="q_calc",
        topic="calc_diff_chain_rule",
        prompt_latex=r"\frac{d}{dx}\left[\sin(x^{2})\right]",
        prompt_text="",
        answer_latex=r"\cos(x^{2})\cdot 2x",
        metadata={
            "generation_settings": {
                "difficulty": 18,
                "seed": 7,
                "allow_trig": True,
                "allow_chain": True,
                "require_chain": True,
            },
            "generator": "derivative_chain_rule",
            "function_classes": ["algebraic", "trig"],
            "methods_used": ["chain", "power"],
            "chain_depth": 2,
            "shape_id": "fn:sin+power",
            "effort_features": {
                "answer_len": 20,
                "chain_applications": 2,
                "has_fn_power": False,
            },
            "spec_snapshot": {
                "allow_integer_exponents": True,
                "allow_fractional_exponents": True,
                "allow_irrational_exponents": False,
                "allow_negative_exponents": False,
                "allow_fn_power": True,
                "derivative_order": 1,
                "allowed_functions": ["trig"],
                "degree_max": 4,
            },
            "upgrades": ["classes:trig"],
        },
    )
    rec = build_generation_record(
        "calc_diff_chain_rule",
        q,
        {"difficulty": 18, "seed": 7},
        y_effort=12.0,
    )
    assert rec.theta_full.get("allow_trig") is True
    assert rec.theta_full.get("allow_fractional_exponents") is True
    assert rec.structural_features.get("function_classes") == ["algebraic", "trig"]
    assert isinstance(rec.structural_features.get("spec_snapshot"), dict)
    assert rec.rating_1_to_5 is None

    feats = record_feature_dict(rec)
    assert feats.get("allow_trig") == 1.0
    assert feats.get("allow_fractional_exponents") == 1.0
    assert feats.get("function_classes:trig") == 1.0
    assert feats.get("methods_used:chain") == 1.0
    assert feats.get("spec_allow_fn_power") == 1.0
    assert feats.get("ast_ef_chain_applications") == 2.0


def test_structured_pack_snapshot_merges_into_theta():
    """Structured (non-ExpressionSpec) packs still join via spec_snapshot → θ."""
    q = Question(
        id="q_ob",
        topic="calc_diff_other_base_logarithms_and_exponentials",
        prompt_latex=r"\frac{d}{dx}\left[2^{x}\right]",
        prompt_text="",
        answer_latex=r"2^{x}\ln(2)",
        metadata={
            "generation_settings": {
                "difficulty": 8,
                "seed": 3,
                "allow_exp": True,
                "allow_log": True,
            },
            "generator": "derivative_other_base",
            "function_classes": ["exp", "algebraic"],
            "methods_used": ["power"],
            "family": "a_x",
            "structure_id": "derivative_other_base:a_x",
            "spec_snapshot": {
                "pack": "structured_other_base",
                "family": "a_x",
                "allow_exp": True,
                "allow_log": True,
                "allow_chain": True,
                "derivative_order": 1,
            },
            "effort_features": {"answer_len": 12, "derivative_order": 1},
        },
    )
    rec = build_generation_record(
        "calc_diff_other_base_logarithms_and_exponentials",
        q,
        {"difficulty": 8, "seed": 3},
    )
    assert rec.theta_full.get("allow_exp") is True
    assert rec.theta_full.get("spec_snapshot", {}).get("pack") == "structured_other_base"
    feats = record_feature_dict(rec)
    assert feats.get("spec_pack") == "structured_other_base" or feats.get(
        "spec_family"
    ) == "a_x"
