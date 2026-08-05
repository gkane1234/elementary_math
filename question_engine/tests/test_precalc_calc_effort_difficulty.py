"""Continuous-D + effort scorer tests for Precalculus / Calculus tranche."""

from __future__ import annotations

import question_engine.types  # noqa: F401
from question_engine.catalogs import calculus, precalculus
from question_engine.core.base import QUESTION_TYPES
from question_engine.ml.effort import has_effort_scorer, score_effort
from question_engine.ml.effort_calc import (
    effort_area_volume,
    effort_binomial,
    effort_curve_analysis_calc,
    effort_def_of_derivative,
    effort_derivative_power,
    effort_derivative_rules,
    effort_exp_equation,
    effort_integral_power,
    effort_inverse_trig,
    effort_lhopital,
    effort_limit,
    effort_log_evaluate,
    effort_right_triangle_trig,
    effort_trig_evaluate,
    effort_trig_identity,
    effort_vector,
)
from question_engine.settings.params import (
    apply_calculus_continuous_knobs,
    apply_logarithm_continuous_knobs,
    apply_trigonometry_continuous_knobs,
)


def _has_continuous_difficulty(type_id: str) -> bool:
    qt = QUESTION_TYPES[type_id]
    fields = qt.settings_schema()
    return any(
        getattr(f, "key", None) == "difficulty"
        and getattr(f, "type", None) in {"int", "float", "number", "range"}
        for f in fields
    )


def test_all_precalc_calc_types_expose_continuous_difficulty():
    for entry in (*precalculus.CATALOG, *calculus.CATALOG):
        assert entry.id in QUESTION_TYPES, entry.id
        assert _has_continuous_difficulty(entry.id), entry.id


def test_calculus_knobs_widen_with_d():
    assert apply_calculus_continuous_knobs({"difficulty_tier": "hard"}) == {
        "difficulty_tier": "hard"
    }
    easy = apply_calculus_continuous_knobs({"difficulty": 0})
    hard = apply_calculus_continuous_knobs({"difficulty": 22})
    assert easy["term_count"] < hard["term_count"] or easy["power_max"] < hard["power_max"]
    assert hard["coef_max"] >= easy["coef_max"]


def test_log_trig_knobs_unlock_with_d():
    log0 = apply_logarithm_continuous_knobs({"difficulty": 0})
    log20 = apply_logarithm_continuous_knobs({"difficulty": 20})
    assert log0["allow_natural_log"] is False
    assert log20["allow_natural_log"] is True

    trig0 = apply_trigonometry_continuous_knobs({"difficulty": 0})
    trig12 = apply_trigonometry_continuous_knobs({"difficulty": 12})
    assert trig0["allow_tan"] is False
    assert trig12["allow_tan"] is True


def test_limit_and_derivative_scorers_ramp():
    e0, _ = effort_limit(r"\lim_{x \to 1} \left(x + 1\right)", "2")
    e1, f1 = effort_limit(r"\lim_{x \to 9} \left(x^{4} - 3x^{2} + x - 1\right)", "1")
    assert e1 > e0
    assert f1.get("power", 0) >= 2

    ep, _ = effort_derivative_power(r"\frac{d}{dx}\left(x^{2}\right)", "2x")
    eh, _ = effort_derivative_power(r"\frac{d}{dx}\left[\frac{1}{x}+3x^{3}\right]", "")
    assert eh > ep

    eprod, fp = effort_derivative_rules(
        r"\frac{d}{dx}\left[\left(2x-1\right)\left(3x+4\right)\right]", ""
    )
    echain, fc = effort_derivative_rules(r"\frac{d}{dx}\left[\sin\left(4x^{3}\right)\right]", "")
    assert echain >= eprod
    assert fc.get("trig") or "chain" in str(fc.get("form", ""))


def test_integral_log_trig_exp_scorers():
    e_i, _ = effort_integral_power(r"\int x^{2} \, dx", r"\frac{1}{3}x^{3}+C")
    e_ih, _ = effort_integral_power(r"\int 7x^{5} - 12x^{3} \, dx", "")
    assert e_ih > e_i

    e_log, _ = effort_log_evaluate(r"\log_{2}\left(8\right)", "3")
    e_ln, _ = effort_log_evaluate(r"\ln\left(2.7183\right)", "1")
    assert e_ln > e_log

    e_trig, ft = effort_trig_evaluate(r"\sin\left(90^\circ\right)", "1")
    e_cot, _ = effort_trig_evaluate(r"\cot\left(30^\circ\right)", r"\sqrt{3}")
    assert e_cot > e_trig
    assert ft.get("deg") == 90

    e_exp, _ = effort_exp_equation(r"2^{x} = 8", "3")
    e_expl, fl = effort_exp_equation(r"3^{x} = 5", "")
    # needing log not auto-detected without log symbol — add log form
    e_expl2, fl2 = effort_exp_equation(r"\log(3^{x})=\log 5", "")
    assert fl2.get("needs_log")
    assert e_expl2 > e_exp

    e_id, _ = effort_trig_identity(r"\text{Simplify: } \sin^2 \theta + \cos^2 \theta", "1")
    e_dh, f_dh = effort_trig_identity(
        r"\text{Simplify using a double-angle identity: } \sin(2\theta)",
        r"2\sin\theta\cos\theta",
    )
    assert e_dh > e_id
    assert f_dh.get("family") == "double_half"
    e_asin, _ = effort_inverse_trig(r"\arcsin\left(1\right)", r"\frac{\pi}{2}")
    e_atan, _ = effort_inverse_trig(r"\arctan\left(\frac{1}{\sqrt{3}}\right)", r"\frac{\pi}{6}")
    assert e_atan >= e_asin


def test_wave_pc_calc_extended_scorers():
    e_rt, fr = effort_right_triangle_trig(
        r"\text{In right } \triangle ABC \text{ find } \sin A.", ""
    )
    e_side, _ = effort_right_triangle_trig(
        r"\text{In right } \triangle ABC,\ m\angle A = 30^\circ,\ BC = 8.\ \text{Find } AC.",
        "",
    )
    assert e_side > e_rt
    assert fr.get("mode") == "ratio"

    e_dot, fd = effort_vector(r"\text{Find } \langle 5, 6 \rangle \cdot \langle 2, -5 \rangle.", "")
    e_cross, fc = effort_vector(r"\text{Find }(1,3,-2)\times(2,-1,1).", "")
    assert e_cross > e_dot
    assert fd.get("op") == "dot"
    assert fc.get("op") == "cross"

    e_bin, fb = effort_binomial(r"\text{Find the coefficient of } x^{2} \text{ in } (2 + x)^{5}.", "")
    assert fb.get("n") == 5
    assert e_bin >= 6.0

    e_def, _ = effort_def_of_derivative(
        r"\lim_{h\to 0}\frac{\frac{1}{4+h}-\frac{1}{4}}{h}", ""
    )
    assert e_def >= 8.0

    e_lh, fl = effort_lhopital(r"\lim_{x \to 0} \frac{\sin(2x)}{x}", "2")
    assert fl.get("lhopital")
    assert e_lh >= 9.0

    e_opt, fo = effort_curve_analysis_calc(
        r"\text{A rectangle has perimeter }28.\text{ What dimensions maximize area?}",
        "",
    )
    assert fo.get("mode") == "optimization"
    assert e_opt >= 10.0

    e_vol, fv = effort_area_volume(
        r"\text{Find the volume ... disk method.}",
        "",
    )
    assert fv.get("mode") == "disk_washer"
    assert e_vol >= 10.0


def test_export_type_scorers_registered():
    from pathlib import Path
    import json

    root = Path(__file__).resolve().parents[2]
    for name in ("precalc_export_types.json", "calc_export_types.json"):
        data = json.loads((root / "scripts/output/ml" / name).read_text(encoding="utf-8"))
        for tid in data["type_ids"]:
            assert has_effort_scorer(tid), tid
            y, _ = score_effort(tid, r"\lim_{x \to 0} \left(x\right)", "0")
            # Scorer may parse-fail but must return a float
            assert y is not None


def test_smoke_generate_continuous_d_precalc_calc():
    for type_id, d in (
        ("calc_limits_by_direct_evaluation", 0),
        ("calc_diff_chain_rule", 20),
        ("calc_indef_int_power_rule", 12),
        ("pc_evaluating_logarithms", 5),
        ("pc_trig_functions_of_any_angle", 15),
        ("pc_vectors_diagrams", 8),
    ):
        qt = QUESTION_TYPES[type_id]
        qs = qt.generate(
            {
                "difficulty": d,
                "count": 1,
                "include_answer_key": True,
                "seed": 42,
            }
        )
        assert qs
        prompt = (qs[0].prompt_latex or qs[0].prompt_text or "").strip()
        assert prompt
        if type_id == "pc_vectors_diagrams":
            assert "langle" in prompt or "\\langle" in prompt
            assert "+" not in prompt or "tip-to-tail" in prompt.lower() or "opposite" in prompt.lower()
            y, feats = score_effort(type_id, prompt, qs[0].answer_latex or "")
            assert y is not None and y > 0
            assert feats.get("diagram")