"""Calc integrals / apps: related-rates frames, FTC split, definite u-sub."""

from __future__ import annotations

from collections import Counter

from question_engine.api.handler import _generate_for_type
from question_engine.frameworks.primitives.integrals import sample_integral_expression
from question_engine.frameworks.primitives.related_rates_frames import (
    FRAME_BANDS,
    related_frames_for_difficulty,
    sample_related_rates_frame,
)
from question_engine.settings.params import calc_application_structure_from_continuous


def _gen(type_id: str, d: float, *, seed: int = 101, count: int = 1):
    return _generate_for_type(
        type_id,
        {
            "difficulty": d,
            "seed": seed,
            "count": count,
            "include_answer_key": True,
        },
    )


def test_related_rates_d0_circle_only():
    a0 = calc_application_structure_from_continuous({"difficulty": 0})
    assert a0 is not None
    assert a0["related_frames"] == ("expanding_circle",)
    frames = set()
    for seed in range(20):
        q = _gen("calc_app_diff_related_rates", 0, seed=seed)[0]
        fid = (q.metadata or {}).get("frame_id") or (q.metadata or {}).get(
            "related_rates_frame"
        )
        frames.add(fid)
        assert "circle" in (q.prompt_latex or "").lower() or fid == "expanding_circle"
    assert frames == {"expanding_circle"}


def test_related_rates_easy_leftovers_lock_out():
    """Circle/sphere leftovers drop after medium (PFD-style d_max)."""
    assert related_frames_for_difficulty(0) == ("expanding_circle",)
    med = related_frames_for_difficulty(8)
    assert "expanding_circle" in med and "balloon_radius" in med
    hard = related_frames_for_difficulty(12)
    assert "expanding_circle" not in hard and "expanding_sphere" not in hard
    assert set(hard) == {"balloon_radius", "cone_similar", "sliding_ladder"}
    vh = related_frames_for_difficulty(16)
    assert "balloon_radius" not in vh and "expanding_circle" not in vh
    assert "cone_drain" in vh and "sliding_ladder" in vh
    exp = related_frames_for_difficulty(22)
    assert "sliding_ladder" not in exp
    assert "two_rate_distance" in exp and "rocket_angle" in exp
    a20 = calc_application_structure_from_continuous({"difficulty": 20})
    assert a20 is not None
    assert a20["related_frames"] == related_frames_for_difficulty(20)


def test_related_rates_high_d_openstax_variety():
    frames16: set[str] = set()
    for seed in range(40):
        q = _gen("calc_app_diff_related_rates", 16, seed=seed)[0]
        fid = (q.metadata or {}).get("frame_id") or (q.metadata or {}).get(
            "related_rates_frame"
        )
        assert fid, q.prompt_latex
        frames16.add(str(fid))
        assert q.answer_latex
        assert fid != "expanding_circle"
        assert fid != "expanding_sphere"
    assert len(frames16) >= 3, frames16
    assert frames16 & {"sliding_ladder", "lamp_shadow", "airplane_distance", "cone_drain"}

    frames22: set[str] = set()
    for seed in range(40):
        q = _gen("calc_app_diff_related_rates", 22, seed=seed)[0]
        fid = (q.metadata or {}).get("frame_id") or (q.metadata or {}).get(
            "related_rates_frame"
        )
        assert fid, q.prompt_latex
        frames22.add(str(fid))
        assert fid not in {"expanding_circle", "expanding_sphere", "balloon_radius", "sliding_ladder"}
    assert len(frames22) >= 4, frames22
    assert frames22 & {"two_rate_distance", "rocket_angle", "cone_drain"}


def test_related_rates_frame_builders_solvable():
    import random

    rng = random.Random(7)
    for band, frames in FRAME_BANDS.items():
        for _ in range(8):
            item = sample_related_rates_frame(rng, frames=frames, r_max=8, rate_max=4)
            assert item.frame_id in frames
            assert item.prompt_latex
            assert item.answer_latex


def test_ftc1_evaluates_definite():
    q = _gen("calc_def_int_first_fundamental_theorem_of_calculus", 0, seed=101)[0]
    assert r"\int_" in (q.prompt_latex or "")
    assert r"\frac{d}" not in (q.prompt_latex or "")
    assert q.answer_latex


def test_ftc2_is_derivative_of_integral():
    q = _gen("calc_def_int_second_fundamental_theorem_of_calculus", 0, seed=101)[0]
    assert r"\frac{d}" in (q.prompt_latex or "")
    assert r"\int_" in (q.prompt_latex or "")
    assert q.answer_latex
    # High D unlocks chain / trig families across seeds
    forms = set()
    for seed in range(30):
        qq = _gen(
            "calc_def_int_second_fundamental_theorem_of_calculus", 16, seed=seed
        )[0]
        forms.add((qq.metadata or {}).get("form_id") or (qq.metadata or {}).get("family"))
    assert "ftc2_poly" in forms
    assert forms & {"ftc2_trig", "ftc2_chain"}


def test_definite_u_sub_has_limits_no_plus_c():
    q = _gen("calc_def_int_substitution_with_change_of_variables", 0, seed=101)[0]
    p = q.prompt_latex or ""
    assert r"\int_" in p
    assert "+C" not in (q.answer_latex or "")
    sample = sample_integral_expression(
        {"difficulty": 0, "seed": 101, "include_answer_key": True},
        generator_key="integral_definite_substitution",
        topic="calc_def_int_substitution_with_change_of_variables",
    )
    assert sample.metadata.get("definite") is True or "definite" in str(
        sample.metadata.get("form_id")
    )


def test_indef_power_and_pfd_still_live():
    p = _gen("calc_indef_int_power_rule", 0, seed=101)[0]
    assert r"\int" in (p.prompt_latex or "")
    assert "+C" in (p.answer_latex or "")
    pf = _gen("calc_indef_int_partial_fractions", 8, seed=101)[0]
    assert r"\frac" in (pf.prompt_latex or "")
    assert "+C" in (pf.answer_latex or "")


def test_area_under_curve_d0_simple():
    q = _gen("calc_app_int_area_under_a_curve", 0, seed=101)[0]
    assert "area under" in (q.prompt_latex or "").lower()
    assert q.answer_latex


def test_relative_extrema_d0_parabola_high_d_cubic():
    q0 = _gen("calc_app_diff_relative_extrema", 0, seed=101)[0]
    assert "minimum" in (q0.prompt_latex or "").lower() or "minimum" in (q0.answer_latex or "").lower()
    assert (q0.metadata or {}).get("form_id") == "parabola_vertex"
    forms = set()
    for seed in range(12):
        q = _gen("calc_app_diff_relative_extrema", 16, seed=seed)[0]
        forms.add((q.metadata or {}).get("form_id"))
        assert "rel max" in (q.answer_latex or "") or "relative" in (q.answer_latex or "")
    assert "cubic_first_derivative_test" in forms


def test_absolute_extrema_closed_interval():
    q = _gen("calc_app_diff_absolute_extrema", 0, seed=101)[0]
    assert "[" in (q.prompt_latex or "")
    assert "abs min" in (q.answer_latex or "")
    qh = _gen("calc_app_diff_absolute_extrema", 16, seed=101)[0]
    assert (qh.metadata or {}).get("form_id") == "closed_interval_cubic"


def test_concavity_d0_ray_high_d_shifted_lockout():
    q0 = _gen("calc_app_diff_intervals_of_concavity", 0, seed=101)[0]
    assert (q0.metadata or {}).get("form_id") == "odd_power_positive_ray"
    assert (q0.metadata or {}).get("generator") == "intervals_concavity"
    assert "concave" in (q0.answer_latex or "")
    snap = (q0.metadata or {}).get("spec_snapshot") or {}
    assert snap.get("form_id") == "odd_power_positive_ray"

    mid = set()
    for seed in range(24):
        q = _gen("calc_app_diff_intervals_of_concavity", 8, seed=seed)[0]
        mid.add((q.metadata or {}).get("form_id"))
    assert "odd_power_positive_ray" in mid
    assert "cubic_second_derivative" in mid

    high = set()
    for seed in range(30):
        q = _gen("calc_app_diff_intervals_of_concavity", 16, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        high.add(fid)
        assert fid != "odd_power_positive_ray"
        assert "concave down" in (q.answer_latex or "")
        assert "concave up" in (q.answer_latex or "")
        assert (q.metadata or {}).get("generator") == "intervals_concavity"
    assert high <= {"cubic_second_derivative", "cubic_shifted_inflection"}
    assert "cubic_shifted_inflection" in high

    expert = set()
    for seed in range(24):
        q = _gen("calc_app_diff_intervals_of_concavity", 22, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        expert.add(fid)
        assert fid == "cubic_shifted_inflection"
        h = (q.metadata or {}).get("h")
        assert h not in (0, None)
        assert r"(-\infty,0)" not in (q.answer_latex or "")
    assert expert == {"cubic_shifted_inflection"}


def test_concavity_quality_weights_tilt():
    from contextlib import nullcontext
    import random as _random

    from question_engine.frameworks.primitives.calc_app_diff import (
        sample_concavity,
    )
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        live_quality_form_weights,
    )

    def _counts(weights):
        c = Counter()
        ctx = live_quality_form_weights(weights) if weights else nullcontext()
        with ctx:
            for i in range(240):
                item = sample_concavity(_random.Random(i), {"difficulty": 8.0})
                c[item.form_id] += 1
        return c

    baseline = _counts(None)
    tilted = _counts({"odd_power_positive_ray": -2.5, "cubic_second_derivative": 2.5})
    assert tilted["cubic_second_derivative"] > baseline["cubic_second_derivative"]


def test_mvt_d0_quad_high_d_sqrt_lockout():
    q0 = _gen("calc_app_diff_mean_value_theorem", 0, seed=101)[0]
    assert (q0.metadata or {}).get("form_id") == "mvt_x_squared"
    assert (q0.metadata or {}).get("generator") == "mean_value_theorem"
    assert r"x^{2}" in (q0.prompt_latex or "")
    snap = (q0.metadata or {}).get("spec_snapshot") or {}
    assert snap.get("form_id") == "mvt_x_squared"

    mid = set()
    for seed in range(24):
        q = _gen("calc_app_diff_mean_value_theorem", 8, seed=seed)[0]
        mid.add((q.metadata or {}).get("form_id"))
    assert "mvt_x_squared" in mid
    assert "mvt_k_x_cubed" in mid

    high = set()
    for seed in range(30):
        q = _gen("calc_app_diff_mean_value_theorem", 16, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        high.add(fid)
        assert fid != "mvt_x_squared"
        assert (q.metadata or {}).get("generator") == "mean_value_theorem"
    assert high <= {"mvt_k_x_cubed", "mvt_sqrt_x"}
    assert "mvt_sqrt_x" in high

    expert = set()
    for seed in range(20):
        q = _gen("calc_app_diff_mean_value_theorem", 22, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        expert.add(fid)
        assert fid == "mvt_sqrt_x"
        assert r"\sqrt" in (q.prompt_latex or "")
    assert expert == {"mvt_sqrt_x"}


def test_mvt_quality_weights_tilt():
    from contextlib import nullcontext
    import random as _random

    from question_engine.frameworks.primitives.calc_app_diff import (
        sample_mean_value,
    )
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        live_quality_form_weights,
    )

    def _counts(weights):
        c = Counter()
        ctx = live_quality_form_weights(weights) if weights else nullcontext()
        with ctx:
            for i in range(240):
                item = sample_mean_value(_random.Random(i), {"difficulty": 8.0})
                c[item.form_id] += 1
        return c

    baseline = _counts(None)
    tilted = _counts({"mvt_x_squared": -2.5, "mvt_k_x_cubed": 2.5})
    assert tilted["mvt_k_x_cubed"] > baseline["mvt_k_x_cubed"]


def test_newton_one_then_two_steps():
    q0 = _gen("calc_app_diff_newtons_method", 0, seed=101)[0]
    assert "Newton" in (q0.prompt_latex or "")
    assert "x_1=" in (q0.answer_latex or "")
    qh = _gen("calc_app_diff_newtons_method", 18, seed=5)[0]
    assert "x_2=" in (qh.answer_latex or "") or "x_1=" in (qh.answer_latex or "")


def test_optimization_frames_unlock():
    frames = set()
    for seed in range(20):
        q = _gen("calc_app_diff_optimization", 0, seed=seed)[0]
        frames.add((q.metadata or {}).get("form_id"))
        text = (q.prompt_latex or "").lower()
        assert "perimeter" in text or "fencing" in text
        assert (q.metadata or {}).get("generator") == "optimization_applied"
    assert frames == {"rectangle_perimeter"}
    high = set()
    for seed in range(25):
        q = _gen("calc_app_diff_optimization", 18, seed=seed)[0]
        high.add((q.metadata or {}).get("form_id") or (q.metadata or {}).get("frame_id"))
        assert q.answer_latex
    assert "rectangle_perimeter" not in high
    assert high <= {"garden_three_sides", "open_box", "linear_revenue"}
    assert high & {"garden_three_sides", "open_box"}


def test_optimization_easy_leftovers_lock_out():
    from question_engine.frameworks.primitives.optimization_frames import (
        optimization_frames_for_difficulty,
    )

    assert optimization_frames_for_difficulty(0) == ("rectangle_perimeter",)
    med = optimization_frames_for_difficulty(8)
    assert "rectangle_perimeter" in med and "garden_three_sides" in med
    hard = optimization_frames_for_difficulty(16)
    assert "rectangle_perimeter" not in hard
    assert "linear_revenue" in hard and "open_box" in hard
    expert = set(optimization_frames_for_difficulty(22))
    assert "garden_three_sides" not in expert
    assert "rectangle_perimeter" not in expert
    assert expert >= {
        "inscribed_ellipse",
        "closed_cylinder",
        "inscribed_triangle",
        "open_box_rect",
    }
    seen = set()
    for seed in range(40):
        q = _gen("calc_app_diff_optimization", 22, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        seen.add(fid)
        assert fid not in {"rectangle_perimeter", "garden_three_sides", "linear_revenue"}
        assert (q.metadata or {}).get("generator") == "optimization_applied"
        snap = (q.metadata or {}).get("spec_snapshot") or {}
        assert snap.get("form_id") == fid
        assert snap.get("generator") == "optimization_applied"
    assert len(seen) >= 3, seen


def test_optimization_quality_weights_tilt_frame_mix():
    from contextlib import nullcontext
    import random as _random

    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        live_quality_form_weights,
    )
    from question_engine.frameworks.primitives.optimization_frames import (
        optimization_frames_for_difficulty,
        sample_optimization_frame,
    )

    frames = optimization_frames_for_difficulty(8.0)

    def _counts(weights):
        c = Counter()
        ctx = live_quality_form_weights(weights) if weights else nullcontext()
        with ctx:
            for i in range(240):
                item = sample_optimization_frame(
                    _random.Random(i), frames=frames, d=8.0
                )
                c[item.frame_id] += 1
        return c

    baseline = _counts(None)
    tilted = _counts({"rectangle_perimeter": -2.5, "garden_three_sides": 2.5})
    assert tilted["garden_three_sides"] > baseline["garden_three_sides"]


def test_increase_decrease_d0_parabola_high_d_cubic_lockout():
    q0 = _gen("calc_app_diff_intervals_of_increase_and_decrease", 0, seed=101)[0]
    assert (q0.metadata or {}).get("form_id") == "parabola_increasing"
    assert (q0.metadata or {}).get("generator") == "intervals_increase_decrease"
    assert "increasing" in (q0.prompt_latex or "").lower()
    assert r"x^{2}" in (q0.prompt_latex or "") or r"x^2" in (q0.prompt_latex or "")
    snap = (q0.metadata or {}).get("spec_snapshot") or {}
    assert snap.get("form_id") == "parabola_increasing"

    mid = set()
    for seed in range(24):
        q = _gen("calc_app_diff_intervals_of_increase_and_decrease", 8, seed=seed)[0]
        mid.add((q.metadata or {}).get("form_id"))
    assert "parabola_increasing" in mid
    assert "cubic_odd_sign_chart" in mid

    high = set()
    for seed in range(30):
        q = _gen("calc_app_diff_intervals_of_increase_and_decrease", 16, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        high.add(fid)
        assert fid != "parabola_increasing"
        assert "decreasing" in (q.answer_latex or "")
        assert (q.metadata or {}).get("generator") == "intervals_increase_decrease"
    assert high <= {"cubic_odd_sign_chart", "cubic_shifted_sign_chart"}
    assert "cubic_shifted_sign_chart" in high

    expert = set()
    for seed in range(20):
        q = _gen("calc_app_diff_intervals_of_increase_and_decrease", 22, seed=seed)[0]
        expert.add((q.metadata or {}).get("form_id"))
        assert (q.metadata or {}).get("form_id") == "cubic_shifted_sign_chart"
    assert expert == {"cubic_shifted_sign_chart"}


def test_increase_decrease_quality_weights_tilt():
    from contextlib import nullcontext
    import random as _random

    from question_engine.frameworks.primitives.calc_app_diff import (
        sample_intervals_increase,
    )
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        live_quality_form_weights,
    )

    def _counts(weights):
        c = Counter()
        ctx = live_quality_form_weights(weights) if weights else nullcontext()
        with ctx:
            for i in range(240):
                item = sample_intervals_increase(
                    _random.Random(i), {"difficulty": 8.0}
                )
                c[item.form_id] += 1
        return c

    baseline = _counts(None)
    tilted = _counts({"parabola_increasing": -2.5, "cubic_odd_sign_chart": 2.5})
    assert tilted["cubic_odd_sign_chart"] > baseline["cubic_odd_sign_chart"]


def test_motion_and_integral_not_generic_ddx():
    q = _gen("calc_app_diff_motion_along_a_line", 0, seed=101)[0]
    assert r"s(t)" in (q.prompt_latex or "")
    assert r"\frac{d}{dx}" not in (q.prompt_latex or "")
    qi = _gen("calc_app_int_motion_along_a_line_revisited", 0, seed=101)[0]
    assert "displacement" in (qi.prompt_latex or "").lower()
    qih = _gen("calc_app_int_motion_along_a_line_revisited", 18, seed=3)[0]
    assert "0" in (qih.answer_latex or "")


def test_de_intro_verify_exp_then_euler():
    q0 = _gen("calc_diff_eq_introduction", 0, seed=101)[0]
    assert "Verify" in (q0.prompt_latex or "")
    assert "e^" in (q0.prompt_latex or "")
    qh = _gen("calc_diff_eq_introduction", 16, seed=101)[0]
    assert "Cx" in (qh.prompt_latex or "") or "x^{" in (qh.prompt_latex or "")


def test_curve_sketch_and_graphical_sign_of_fp():
    qs = _gen("calc_app_diff_curve_sketching", 0, seed=101)[0]
    assert "vertex" in (qs.answer_latex or "")
    qg = _gen("calc_app_diff_graphical_comparison_of_f_f_prime_and_f_double_prime", 0, seed=101)[0]
    assert "f'" in (qg.prompt_latex or "") or "f'(x)" in (qg.prompt_latex or "")
    assert r"\frac{d}{dx}" not in (qg.prompt_latex or "")


def test_related_rates_stamps_form_id_generator_and_two_seeds_differ():
    from question_engine.ml.knob_introspect import has_continuous_difficulty
    from question_engine.ml.rating_regressor import extract_skeleton_features
    from question_engine.ml.schema import build_generation_record
    from question_engine.type_readiness import type_not_ready

    tid = "calc_app_diff_related_rates"
    assert has_continuous_difficulty(tid)
    assert not type_not_ready(tid)

    q = _gen(tid, 8, seed=101)[0]
    meta = q.metadata or {}
    fid = meta.get("form_id")
    assert fid
    assert meta.get("generator") == "related_rates_simple"
    assert meta.get("family") == fid
    assert (meta.get("spec_snapshot") or {}).get("form_id") == fid
    rec = build_generation_record(tid, q, {"difficulty": 8, "seed": 101})
    feats = extract_skeleton_features(rec.to_dict())
    assert feats["form_id"] == str(fid)
    assert feats["generator"] == "related_rates_simple"

    seen = set()
    for seed in range(40):
        qq = _gen(tid, 8, seed=seed)[0]
        seen.add(str((qq.metadata or {}).get("form_id") or ""))
    assert len(seen) >= 2, seen
    assert seen <= {"expanding_circle", "expanding_sphere", "balloon_radius"}


def test_related_rates_quality_weights_tilt_frame_mix():
    from collections import Counter
    from contextlib import nullcontext
    import random as _random

    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        live_quality_form_weights,
    )

    frames = related_frames_for_difficulty(8.0)

    def _counts(weights):
        c = Counter()
        ctx = live_quality_form_weights(weights) if weights else nullcontext()
        with ctx:
            for i in range(240):
                item = sample_related_rates_frame(
                    _random.Random(i), frames=frames, d=8.0
                )
                c[item.frame_id] += 1
        return c

    baseline = _counts(None)
    tilted = _counts({"expanding_circle": -2.5, "balloon_radius": 2.5})
    assert tilted["balloon_radius"] > baseline["balloon_radius"]


def test_bc_integral_leaves_emit_form_id_via_select_form_id():
    """General + parts/pfd/trig-sub bc_bank still stamp form_id / generator."""
    from question_engine.frameworks.primitives.integrals import (
        PARTS_FORM_PRESETS,
        PFD_FORM_PRESETS,
        TRIG_SUB_FORM_PRESETS,
        sample_integral_expression,
    )

    general = sample_integral_expression(
        {"difficulty": 8, "seed": 207, "include_answer_key": True},
        generator_key="integral_general",
        topic="calc_indef_int_general",
    )
    gmeta = general.as_metadata()
    assert gmeta.get("generator") == "integral_general"
    assert gmeta.get("form_id")
    qg = _gen("calc_indef_int_general", 8, seed=207)[0]
    assert (qg.metadata or {}).get("form_id")
    assert (qg.metadata or {}).get("generator") == "integral_general"

    checks = (
        ("integration_by_parts", "parts_form_preset", PARTS_FORM_PRESETS["bc_bank"]),
        ("integral_partial_fractions", "pfd_form_preset", PFD_FORM_PRESETS["bc_bank"]),
        ("integral_trig_substitution", "trig_sub_form_preset", TRIG_SUB_FORM_PRESETS["bc_bank"]),
    )
    for key, preset_key, bank in checks:
        sample = sample_integral_expression(
            {
                "difficulty": 16,
                "seed": 11,
                "include_answer_key": True,
                preset_key: "bc_bank",
            },
            generator_key=key,
        )
        meta = sample.as_metadata()
        assert meta.get("generator") == key
        assert meta.get("form_id")
        assert meta["form_id"] in bank, (key, meta["form_id"])

