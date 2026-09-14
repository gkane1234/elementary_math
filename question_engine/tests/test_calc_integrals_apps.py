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


def test_ftc1_d0_easy_high_d_sqrt_sin_lockout():
    from question_engine.frameworks.primitives.integrals import (
        ftc1_forms_for_difficulty,
    )

    assert ftc1_forms_for_difficulty(0) == ("ftc1_linear", "ftc1_quad")
    med = ftc1_forms_for_difficulty(8)
    assert "ftc1_linear" in med and "ftc1_quad" in med
    assert "ftc1_quad_const" in med
    assert "ftc1_sqrt" not in med and "ftc1_sin" not in med
    hard = ftc1_forms_for_difficulty(16)
    assert "ftc1_linear" not in hard and "ftc1_quad" not in hard
    assert hard == ("ftc1_quad_const", "ftc1_sqrt", "ftc1_sin")
    assert ftc1_forms_for_difficulty(22) == ("ftc1_sqrt", "ftc1_sin")

    q0 = _gen("calc_def_int_first_fundamental_theorem_of_calculus", 0, seed=101)[0]
    fid0 = (q0.metadata or {}).get("form_id")
    assert fid0 in {"ftc1_linear", "ftc1_quad"}
    assert (q0.metadata or {}).get("generator") == "first_fundamental_theorem"
    assert r"\sqrt" not in (q0.prompt_latex or "")
    assert r"\sin" not in (q0.prompt_latex or "")
    snap = (q0.metadata or {}).get("spec_snapshot") or {}
    assert snap.get("form_id") == fid0
    assert snap.get("generator") == "first_fundamental_theorem"

    mid = set()
    for seed in range(30):
        q = _gen(
            "calc_def_int_first_fundamental_theorem_of_calculus", 8, seed=seed
        )[0]
        fid = (q.metadata or {}).get("form_id")
        mid.add(fid)
        assert (q.metadata or {}).get("generator") == "first_fundamental_theorem"
        assert r"\sqrt" not in (q.prompt_latex or "")
        assert r"\sin" not in (q.prompt_latex or "")
    assert "ftc1_linear" in mid
    assert "ftc1_quad" in mid
    assert "ftc1_quad_const" in mid
    assert mid <= {"ftc1_linear", "ftc1_quad", "ftc1_quad_const"}

    high = set()
    for seed in range(36):
        q = _gen(
            "calc_def_int_first_fundamental_theorem_of_calculus", 16, seed=seed
        )[0]
        fid = (q.metadata or {}).get("form_id")
        high.add(fid)
        assert fid not in {"ftc1_linear", "ftc1_quad"}
        p = q.prompt_latex or ""
        assert r"} x\,d" not in p
        assert (q.metadata or {}).get("generator") == "first_fundamental_theorem"
    assert high <= {"ftc1_quad_const", "ftc1_sqrt", "ftc1_sin"}
    assert "ftc1_quad_const" in high
    assert high & {"ftc1_sqrt", "ftc1_sin"}

    expert = set()
    for seed in range(30):
        q = _gen(
            "calc_def_int_first_fundamental_theorem_of_calculus", 22, seed=seed
        )[0]
        fid = (q.metadata or {}).get("form_id")
        expert.add(fid)
        assert fid in {"ftc1_sqrt", "ftc1_sin"}
        p = q.prompt_latex or ""
        assert r"} x\,d" not in p
        assert r"x^{2}" not in p
        assert (q.metadata or {}).get("generator") == "first_fundamental_theorem"
        snap = (q.metadata or {}).get("spec_snapshot") or {}
        assert snap.get("form_id") == fid
        assert snap.get("generator") == "first_fundamental_theorem"
    assert expert == {"ftc1_sqrt", "ftc1_sin"}


def test_ftc1_quality_weights_tilt():
    from contextlib import nullcontext
    import random as _random

    from question_engine.frameworks.primitives.integrals import (
        sample_integral_expression,
    )
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        live_quality_form_weights,
    )

    def _counts(weights):
        c = Counter()
        ctx = live_quality_form_weights(weights) if weights else nullcontext()
        with ctx:
            for i in range(240):
                sample = sample_integral_expression(
                    {"difficulty": 8.0, "include_answer_key": True},
                    generator_key="first_fundamental_theorem",
                    rng=_random.Random(i),
                )
                c[sample.metadata.get("form_id")] += 1
        return c

    baseline = _counts(None)
    tilted = _counts({"ftc1_linear": -2.5, "ftc1_quad": 2.5})
    assert tilted["ftc1_quad"] > baseline["ftc1_quad"]


def test_ftc2_is_derivative_of_integral():
    q = _gen("calc_def_int_second_fundamental_theorem_of_calculus", 0, seed=101)[0]
    assert r"\frac{d}" in (q.prompt_latex or "")
    assert r"\int_" in (q.prompt_latex or "")
    assert q.answer_latex


def test_ftc2_d0_poly_high_d_chain_lockout():
    from question_engine.frameworks.primitives.integrals import (
        ftc2_forms_for_difficulty,
    )

    assert ftc2_forms_for_difficulty(0) == ("ftc2_poly",)
    med = ftc2_forms_for_difficulty(8)
    assert med == ("ftc2_poly", "ftc2_trig")
    hard = ftc2_forms_for_difficulty(16)
    assert hard == ("ftc2_trig", "ftc2_chain")
    assert "ftc2_poly" not in hard
    assert ftc2_forms_for_difficulty(22) == ("ftc2_chain",)

    q0 = _gen("calc_def_int_second_fundamental_theorem_of_calculus", 0, seed=101)[0]
    assert (q0.metadata or {}).get("form_id") == "ftc2_poly"
    assert (q0.metadata or {}).get("generator") == "second_fundamental_theorem"
    assert r"t^{2}" in (q0.prompt_latex or "")
    assert r"\sin" not in (q0.prompt_latex or "")
    snap = (q0.metadata or {}).get("spec_snapshot") or {}
    assert snap.get("form_id") == "ftc2_poly"
    assert snap.get("generator") == "second_fundamental_theorem"

    mid = set()
    for seed in range(24):
        q = _gen(
            "calc_def_int_second_fundamental_theorem_of_calculus", 8, seed=seed
        )[0]
        fid = (q.metadata or {}).get("form_id")
        mid.add(fid)
        assert (q.metadata or {}).get("generator") == "second_fundamental_theorem"
        p = q.prompt_latex or ""
        assert r"e^{" not in p
    assert "ftc2_poly" in mid
    assert "ftc2_trig" in mid
    assert mid <= {"ftc2_poly", "ftc2_trig"}

    high = set()
    for seed in range(30):
        q = _gen(
            "calc_def_int_second_fundamental_theorem_of_calculus", 16, seed=seed
        )[0]
        fid = (q.metadata or {}).get("form_id")
        high.add(fid)
        assert fid != "ftc2_poly"
        p = q.prompt_latex or ""
        assert r"t^{2}" not in p
        assert (q.metadata or {}).get("generator") == "second_fundamental_theorem"
    assert high <= {"ftc2_trig", "ftc2_chain"}
    assert "ftc2_trig" in high
    assert "ftc2_chain" in high

    expert = set()
    for seed in range(24):
        q = _gen(
            "calc_def_int_second_fundamental_theorem_of_calculus", 22, seed=seed
        )[0]
        fid = (q.metadata or {}).get("form_id")
        expert.add(fid)
        assert fid == "ftc2_chain"
        p = q.prompt_latex or ""
        assert r"t^{2}" not in p
        assert r"\sin" not in p
        assert r"e^{" in p
        assert (q.metadata or {}).get("generator") == "second_fundamental_theorem"
        snap = (q.metadata or {}).get("spec_snapshot") or {}
        assert snap.get("form_id") == "ftc2_chain"
        assert snap.get("generator") == "second_fundamental_theorem"
    assert expert == {"ftc2_chain"}


def test_ftc2_quality_weights_tilt():
    from contextlib import nullcontext
    import random as _random

    from question_engine.frameworks.primitives.integrals import (
        sample_integral_expression,
    )
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        live_quality_form_weights,
    )

    def _counts(weights):
        c = Counter()
        ctx = live_quality_form_weights(weights) if weights else nullcontext()
        with ctx:
            for i in range(240):
                sample = sample_integral_expression(
                    {"difficulty": 8.0, "include_answer_key": True},
                    generator_key="second_fundamental_theorem",
                    rng=_random.Random(i),
                )
                c[sample.metadata.get("form_id")] += 1
        return c

    baseline = _counts(None)
    tilted = _counts({"ftc2_poly": -2.5, "ftc2_trig": 2.5})
    assert tilted["ftc2_trig"] > baseline["ftc2_trig"]


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


def test_area_under_curve_d0_linear_high_d_quad_coef_lockout():
    from question_engine.frameworks.primitives.calc_app_diff import (
        area_under_curve_forms_for_difficulty,
    )

    assert area_under_curve_forms_for_difficulty(0) == ("auc_linear",)
    med = area_under_curve_forms_for_difficulty(8)
    assert "auc_linear" in med and "auc_quad" in med
    hard = area_under_curve_forms_for_difficulty(16)
    assert "auc_linear" not in hard
    assert hard == ("auc_quad", "auc_quad_coef")
    assert area_under_curve_forms_for_difficulty(22) == ("auc_quad_coef",)

    q0 = _gen("calc_app_int_area_under_a_curve", 0, seed=101)[0]
    assert (q0.metadata or {}).get("form_id") == "auc_linear"
    assert (q0.metadata or {}).get("generator") == "area_under_curve"
    assert r"y=x\text{ from }" in (q0.prompt_latex or "")
    assert r"x^{2}" not in (q0.prompt_latex or "")
    snap = (q0.metadata or {}).get("spec_snapshot") or {}
    assert snap.get("form_id") == "auc_linear"
    assert snap.get("generator") == "area_under_curve"

    mid = set()
    for seed in range(24):
        q = _gen("calc_app_int_area_under_a_curve", 8, seed=seed)[0]
        mid.add((q.metadata or {}).get("form_id"))
        assert (q.metadata or {}).get("generator") == "area_under_curve"
        assert r"y=2x^{2}" not in (q.prompt_latex or "")
        assert r"y=3x^{2}" not in (q.prompt_latex or "")
        assert r"y=4x^{2}" not in (q.prompt_latex or "")
    assert "auc_linear" in mid
    assert "auc_quad" in mid
    assert mid <= {"auc_linear", "auc_quad"}

    high = set()
    for seed in range(30):
        q = _gen("calc_app_int_area_under_a_curve", 16, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        high.add(fid)
        assert fid != "auc_linear"
        assert r"y=x\text{ from }" not in (q.prompt_latex or "")
        assert (q.metadata or {}).get("generator") == "area_under_curve"
    assert high <= {"auc_quad", "auc_quad_coef"}
    assert "auc_quad_coef" in high

    expert = set()
    for seed in range(24):
        q = _gen("calc_app_int_area_under_a_curve", 22, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        expert.add(fid)
        assert fid == "auc_quad_coef"
        p = q.prompt_latex or ""
        assert r"y=x\text{ from }" not in p
        assert r"x^{2}" in p
        assert (q.metadata or {}).get("generator") == "area_under_curve"
        snap = (q.metadata or {}).get("spec_snapshot") or {}
        assert snap.get("form_id") == "auc_quad_coef"
        assert snap.get("generator") == "area_under_curve"
    assert expert == {"auc_quad_coef"}


def test_area_under_curve_quality_weights_tilt():
    from contextlib import nullcontext
    import random as _random

    from question_engine.frameworks.primitives.calc_app_diff import (
        sample_area_under_curve,
    )
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        live_quality_form_weights,
    )

    def _counts(weights):
        c = Counter()
        ctx = live_quality_form_weights(weights) if weights else nullcontext()
        with ctx:
            for i in range(240):
                item = sample_area_under_curve(
                    _random.Random(i), {"difficulty": 8.0}
                )
                c[item.form_id] += 1
        return c

    baseline = _counts(None)
    tilted = _counts({"auc_linear": -2.5, "auc_quad": 2.5})
    assert tilted["auc_quad"] > baseline["auc_quad"]


def test_volume_disk_washer_d0_linear_high_d_washer_lockout():
    from question_engine.frameworks.primitives.calc_app_diff import (
        volume_disk_washer_forms_for_difficulty,
    )

    assert volume_disk_washer_forms_for_difficulty(0) == ("vdw_disk_linear",)
    med = volume_disk_washer_forms_for_difficulty(8)
    assert "vdw_disk_linear" in med and "vdw_disk_quadratic" in med
    assert "vdw_washer" not in med
    # volume_methods leftover: disk_linear out at d>=10; disk_quadratic out at d>=16.
    mid_hard = volume_disk_washer_forms_for_difficulty(12)
    assert "vdw_disk_linear" not in mid_hard
    assert mid_hard == ("vdw_disk_quadratic", "vdw_washer")
    assert volume_disk_washer_forms_for_difficulty(16) == ("vdw_washer",)
    assert volume_disk_washer_forms_for_difficulty(22) == ("vdw_washer",)

    q0 = _gen("calc_app_int_volume_by_slicing_disks_and_washers", 0, seed=101)[0]
    assert (q0.metadata or {}).get("form_id") == "vdw_disk_linear"
    assert (q0.metadata or {}).get("generator") == "volume_disk_washer"
    p0 = q0.prompt_latex or ""
    assert r"y=x\text{ on }" in p0
    assert r"x^{2}" not in p0
    assert "disk method" in p0
    assert "washer" not in p0.lower()
    snap = (q0.metadata or {}).get("spec_snapshot") or {}
    assert snap.get("form_id") == "vdw_disk_linear"
    assert snap.get("generator") == "volume_disk_washer"

    mid = set()
    for seed in range(24):
        q = _gen("calc_app_int_volume_by_slicing_disks_and_washers", 8, seed=seed)[0]
        mid.add((q.metadata or {}).get("form_id"))
        assert (q.metadata or {}).get("generator") == "volume_disk_washer"
        assert "washer" not in (q.prompt_latex or "").lower()
        assert "region between" not in (q.prompt_latex or "").lower()
    assert "vdw_disk_linear" in mid
    assert "vdw_disk_quadratic" in mid
    assert mid <= {"vdw_disk_linear", "vdw_disk_quadratic"}

    for d in (16, 22):
        seen = set()
        for seed in range(24):
            q = _gen(
                "calc_app_int_volume_by_slicing_disks_and_washers", d, seed=seed
            )[0]
            fid = (q.metadata or {}).get("form_id")
            seen.add(fid)
            assert fid == "vdw_washer"
            p = q.prompt_latex or ""
            assert "washer method" in p
            assert "disk method" not in p
            assert r"y=x^{2}" not in p
            assert (q.metadata or {}).get("generator") == "volume_disk_washer"
            snap = (q.metadata or {}).get("spec_snapshot") or {}
            assert snap.get("form_id") == "vdw_washer"
            assert snap.get("generator") == "volume_disk_washer"
        assert seen == {"vdw_washer"}


def test_volume_disk_washer_quality_weights_tilt():
    from contextlib import nullcontext
    import random as _random

    from question_engine.frameworks.primitives.calc_app_diff import (
        sample_volume_disk_washer,
    )
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        live_quality_form_weights,
    )

    def _counts(weights):
        c = Counter()
        ctx = live_quality_form_weights(weights) if weights else nullcontext()
        with ctx:
            for i in range(240):
                item = sample_volume_disk_washer(
                    _random.Random(i), {"difficulty": 8.0}
                )
                c[item.form_id] += 1
        return c

    baseline = _counts(None)
    tilted = _counts({"vdw_disk_linear": -2.5, "vdw_disk_quadratic": 2.5})
    assert tilted["vdw_disk_quadratic"] > baseline["vdw_disk_quadratic"]


def test_volume_shell_d0_linear_high_d_line_lockout():
    from question_engine.frameworks.primitives.calc_app_diff import (
        volume_shell_forms_for_difficulty,
    )

    assert volume_shell_forms_for_difficulty(0) == ("vsh_linear",)
    med = volume_shell_forms_for_difficulty(8)
    assert "vsh_linear" in med and "vsh_quadratic" in med
    assert "vsh_line" not in med
    hard = volume_shell_forms_for_difficulty(16)
    assert "vsh_linear" not in hard
    assert hard == ("vsh_quadratic", "vsh_line")
    assert volume_shell_forms_for_difficulty(22) == ("vsh_line",)

    q0 = _gen("calc_app_int_volume_by_cylinders", 0, seed=101)[0]
    assert (q0.metadata or {}).get("form_id") == "vsh_linear"
    assert (q0.metadata or {}).get("generator") == "volume_shell"
    p0 = q0.prompt_latex or ""
    assert r"y=x\text{ on }" in p0
    assert r"x^{2}" not in p0
    assert "shell method" in p0
    assert r"y\text{-axis" in p0
    snap = (q0.metadata or {}).get("spec_snapshot") or {}
    assert snap.get("form_id") == "vsh_linear"
    assert snap.get("generator") == "volume_shell"

    mid = set()
    for seed in range(24):
        q = _gen("calc_app_int_volume_by_cylinders", 8, seed=seed)[0]
        mid.add((q.metadata or {}).get("form_id"))
        assert (q.metadata or {}).get("generator") == "volume_shell"
        p = q.prompt_latex or ""
        assert "shell method" in p
        stripped = p.replace(r"y=x^{2}", "").replace(r"y=x", "")
        assert "-x" not in stripped
    assert "vsh_linear" in mid
    assert "vsh_quadratic" in mid
    assert mid <= {"vsh_linear", "vsh_quadratic"}

    high = set()
    for seed in range(30):
        q = _gen("calc_app_int_volume_by_cylinders", 16, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        high.add(fid)
        assert fid != "vsh_linear"
        p = q.prompt_latex or ""
        assert r"y=x\text{ on }" not in p
        assert (q.metadata or {}).get("generator") == "volume_shell"
    assert high <= {"vsh_quadratic", "vsh_line"}
    assert "vsh_line" in high

    expert = set()
    for seed in range(24):
        q = _gen("calc_app_int_volume_by_cylinders", 22, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        expert.add(fid)
        assert fid == "vsh_line"
        p = q.prompt_latex or ""
        assert "shell method" in p
        assert r"y=x^{2}" not in p
        assert r"y=x\text{ on }" not in p
        assert (q.metadata or {}).get("generator") == "volume_shell"
        snap = (q.metadata or {}).get("spec_snapshot") or {}
        assert snap.get("form_id") == "vsh_line"
        assert snap.get("generator") == "volume_shell"
    assert expert == {"vsh_line"}


def test_volume_cross_sections_d0_square_high_d_semi_lockout():
    from question_engine.frameworks.primitives.calc_app_diff import (
        volume_cross_sections_forms_for_difficulty,
    )

    assert volume_cross_sections_forms_for_difficulty(0) == ("vcs_square",)
    med = volume_cross_sections_forms_for_difficulty(8)
    assert "vcs_square" in med and "vcs_equilateral" in med
    assert "vcs_semicircle" not in med
    hard = volume_cross_sections_forms_for_difficulty(16)
    assert "vcs_square" not in hard
    assert hard == ("vcs_equilateral", "vcs_semicircle")
    assert volume_cross_sections_forms_for_difficulty(22) == ("vcs_semicircle",)

    q0 = _gen(
        "calc_app_int_volume_of_solids_with_known_cross_sections", 0, seed=101
    )[0]
    assert (q0.metadata or {}).get("form_id") == "vcs_square"
    assert (q0.metadata or {}).get("generator") == "volume_cross_sections"
    p0 = q0.prompt_latex or ""
    assert "square cross sections" in p0
    assert "equilateral" not in p0
    assert "semicircle" not in p0
    snap = (q0.metadata or {}).get("spec_snapshot") or {}
    assert snap.get("form_id") == "vcs_square"
    assert snap.get("generator") == "volume_cross_sections"

    mid = set()
    for seed in range(24):
        q = _gen(
            "calc_app_int_volume_of_solids_with_known_cross_sections", 8, seed=seed
        )[0]
        mid.add((q.metadata or {}).get("form_id"))
        assert (q.metadata or {}).get("generator") == "volume_cross_sections"
        p = q.prompt_latex or ""
        assert "semicircle" not in p
        assert "square" in p or "equilateral" in p
    assert "vcs_square" in mid
    assert "vcs_equilateral" in mid
    assert mid <= {"vcs_square", "vcs_equilateral"}

    high = set()
    for seed in range(30):
        q = _gen(
            "calc_app_int_volume_of_solids_with_known_cross_sections", 16, seed=seed
        )[0]
        fid = (q.metadata or {}).get("form_id")
        high.add(fid)
        assert fid != "vcs_square"
        p = q.prompt_latex or ""
        assert "square cross sections" not in p
        assert (q.metadata or {}).get("generator") == "volume_cross_sections"
    assert high <= {"vcs_equilateral", "vcs_semicircle"}
    assert "vcs_semicircle" in high

    expert = set()
    for seed in range(24):
        q = _gen(
            "calc_app_int_volume_of_solids_with_known_cross_sections", 22, seed=seed
        )[0]
        fid = (q.metadata or {}).get("form_id")
        expert.add(fid)
        assert fid == "vcs_semicircle"
        p = q.prompt_latex or ""
        assert "semicircles with diameter" in p
        assert "square" not in p
        assert "equilateral" not in p
        assert (q.metadata or {}).get("generator") == "volume_cross_sections"
        snap = (q.metadata or {}).get("spec_snapshot") or {}
        assert snap.get("form_id") == "vcs_semicircle"
        assert snap.get("generator") == "volume_cross_sections"
    assert expert == {"vcs_semicircle"}


def test_volume_shell_quality_weights_tilt():
    from contextlib import nullcontext
    import random as _random

    from question_engine.frameworks.primitives.calc_app_diff import (
        sample_volume_shell,
    )
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        live_quality_form_weights,
    )

    def _counts(weights):
        c = Counter()
        ctx = live_quality_form_weights(weights) if weights else nullcontext()
        with ctx:
            for i in range(240):
                item = sample_volume_shell(
                    _random.Random(i), {"difficulty": 8.0}
                )
                c[item.form_id] += 1
        return c

    baseline = _counts(None)
    tilted = _counts({"vsh_linear": -2.5, "vsh_quadratic": 2.5})
    assert tilted["vsh_quadratic"] > baseline["vsh_quadratic"]


def test_volume_cross_sections_quality_weights_tilt():
    from contextlib import nullcontext
    import random as _random

    from question_engine.frameworks.primitives.calc_app_diff import (
        sample_volume_cross_sections,
    )
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        live_quality_form_weights,
    )

    def _counts(weights):
        c = Counter()
        ctx = live_quality_form_weights(weights) if weights else nullcontext()
        with ctx:
            for i in range(240):
                item = sample_volume_cross_sections(
                    _random.Random(i), {"difficulty": 8.0}
                )
                c[item.form_id] += 1
        return c

    baseline = _counts(None)
    tilted = _counts({"vcs_square": -2.5, "vcs_equilateral": 2.5})
    assert tilted["vcs_equilateral"] > baseline["vcs_equilateral"]


def test_def_int_mean_value_d0_linear_high_d_quad_coef_lockout():
    from question_engine.frameworks.primitives.calc_app_diff import (
        def_int_mean_value_forms_for_difficulty,
    )

    assert def_int_mean_value_forms_for_difficulty(0) == ("dimvt_linear",)
    med = def_int_mean_value_forms_for_difficulty(8)
    assert "dimvt_linear" in med and "dimvt_quad" in med
    hard = def_int_mean_value_forms_for_difficulty(16)
    assert "dimvt_linear" not in hard
    assert hard == ("dimvt_quad", "dimvt_quad_coef")
    assert def_int_mean_value_forms_for_difficulty(22) == ("dimvt_quad_coef",)

    q0 = _gen("calc_def_int_mean_value_theorem", 0, seed=101)[0]
    assert (q0.metadata or {}).get("form_id") == "dimvt_linear"
    assert (q0.metadata or {}).get("generator") == "def_int_mean_value"
    assert r"f(x)=x\text{ on }" in (q0.prompt_latex or "")
    assert r"x^{2}" not in (q0.prompt_latex or "")
    snap = (q0.metadata or {}).get("spec_snapshot") or {}
    assert snap.get("form_id") == "dimvt_linear"
    assert snap.get("generator") == "def_int_mean_value"

    mid = set()
    for seed in range(24):
        q = _gen("calc_def_int_mean_value_theorem", 8, seed=seed)[0]
        mid.add((q.metadata or {}).get("form_id"))
        assert (q.metadata or {}).get("generator") == "def_int_mean_value"
        assert r"f(x)=2x^{2}" not in (q.prompt_latex or "")
        assert r"f(x)=3x^{2}" not in (q.prompt_latex or "")
        assert r"f(x)=4x^{2}" not in (q.prompt_latex or "")
    assert "dimvt_linear" in mid
    assert "dimvt_quad" in mid
    assert mid <= {"dimvt_linear", "dimvt_quad"}

    high = set()
    for seed in range(30):
        q = _gen("calc_def_int_mean_value_theorem", 16, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        high.add(fid)
        assert fid != "dimvt_linear"
        assert r"f(x)=x\text{ on }" not in (q.prompt_latex or "")
        assert (q.metadata or {}).get("generator") == "def_int_mean_value"
    assert high <= {"dimvt_quad", "dimvt_quad_coef"}
    assert "dimvt_quad_coef" in high

    expert = set()
    for seed in range(24):
        q = _gen("calc_def_int_mean_value_theorem", 22, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        expert.add(fid)
        assert fid == "dimvt_quad_coef"
        p = q.prompt_latex or ""
        assert r"f(x)=x\text{ on }" not in p
        assert r"x^{2}" in p
        assert (q.metadata or {}).get("generator") == "def_int_mean_value"
        snap = (q.metadata or {}).get("spec_snapshot") or {}
        assert snap.get("form_id") == "dimvt_quad_coef"
        assert snap.get("generator") == "def_int_mean_value"
    assert expert == {"dimvt_quad_coef"}


def test_riemann_sum_tables_d0_left3_high_d_midpoint_lockout():
    from question_engine.frameworks.primitives.calc_app_diff import (
        riemann_sum_tables_forms_for_difficulty,
    )

    assert riemann_sum_tables_forms_for_difficulty(0) == ("rst_left3",)
    med = riemann_sum_tables_forms_for_difficulty(8)
    assert "rst_left3" in med and "rst_left_right4" in med
    hard = riemann_sum_tables_forms_for_difficulty(16)
    assert "rst_left3" not in hard
    assert hard == ("rst_left_right4", "rst_midpoint")
    assert riemann_sum_tables_forms_for_difficulty(22) == ("rst_midpoint",)

    q0 = _gen("calc_def_int_riemann_sum_tables", 0, seed=101)[0]
    assert (q0.metadata or {}).get("form_id") == "rst_left3"
    assert (q0.metadata or {}).get("generator") == "riemann_sum_tables"
    p0 = q0.prompt_latex or ""
    assert r"f(2)=" in p0
    assert r"f(3)=" not in p0
    assert "midpoint" not in p0.lower()
    snap = (q0.metadata or {}).get("spec_snapshot") or {}
    assert snap.get("form_id") == "rst_left3"
    assert snap.get("generator") == "riemann_sum_tables"

    mid = set()
    for seed in range(24):
        q = _gen("calc_def_int_riemann_sum_tables", 8, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        mid.add(fid)
        p = q.prompt_latex or ""
        assert (q.metadata or {}).get("generator") == "riemann_sum_tables"
        assert "midpoint" not in p.lower()
    assert "rst_left3" in mid
    assert "rst_left_right4" in mid
    assert mid <= {"rst_left3", "rst_left_right4"}

    high = set()
    for seed in range(30):
        q = _gen("calc_def_int_riemann_sum_tables", 16, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        high.add(fid)
        p = q.prompt_latex or ""
        assert fid != "rst_left3"
        assert not (r"f(2)=" in p and r"f(3)=" not in p and "midpoint" not in p.lower())
        assert (q.metadata or {}).get("generator") == "riemann_sum_tables"
    assert high <= {"rst_left_right4", "rst_midpoint"}
    assert "rst_midpoint" in high

    expert = set()
    for seed in range(24):
        q = _gen("calc_def_int_riemann_sum_tables", 22, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        expert.add(fid)
        p = q.prompt_latex or ""
        assert fid == "rst_midpoint"
        assert "midpoint" in p.lower()
        assert r"f(3)=" in p
        assert (q.metadata or {}).get("generator") == "riemann_sum_tables"
        snap = (q.metadata or {}).get("spec_snapshot") or {}
        assert snap.get("form_id") == "rst_midpoint"
        assert snap.get("generator") == "riemann_sum_tables"
    assert expert == {"rst_midpoint"}


def test_riemann_sum_tables_quality_weights_tilt():
    from contextlib import nullcontext
    import random as _random

    from question_engine.frameworks.primitives.calc_app_diff import (
        sample_riemann_sum_tables,
    )
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        live_quality_form_weights,
    )

    def _counts(weights):
        c = Counter()
        ctx = live_quality_form_weights(weights) if weights else nullcontext()
        with ctx:
            for i in range(240):
                item = sample_riemann_sum_tables(
                    _random.Random(i), {"difficulty": 8.0}
                )
                c[item.form_id] += 1
        return c

    baseline = _counts(None)
    tilted = _counts({"rst_left3": -2.5, "rst_left_right4": 2.5})
    assert tilted["rst_left_right4"] > baseline["rst_left_right4"]


def test_def_int_mean_value_quality_weights_tilt():
    from contextlib import nullcontext
    import random as _random

    from question_engine.frameworks.primitives.calc_app_diff import (
        sample_def_int_mean_value,
    )
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        live_quality_form_weights,
    )

    def _counts(weights):
        c = Counter()
        ctx = live_quality_form_weights(weights) if weights else nullcontext()
        with ctx:
            for i in range(240):
                item = sample_def_int_mean_value(
                    _random.Random(i), {"difficulty": 8.0}
                )
                c[item.form_id] += 1
        return c

    baseline = _counts(None)
    tilted = _counts({"dimvt_linear": -2.5, "dimvt_quad": 2.5})
    assert tilted["dimvt_quad"] > baseline["dimvt_quad"]


def test_area_between_curves_d0_linear_high_d_two_curve_lockout():
    from question_engine.frameworks.primitives.calc_app_diff import (
        area_between_curves_forms_for_difficulty,
    )

    assert area_between_curves_forms_for_difficulty(0) == ("abc_linear_axis",)
    med = area_between_curves_forms_for_difficulty(8)
    assert "abc_linear_axis" in med
    assert "abc_quad_axis" in med
    assert "abc_hline_linear" in med
    assert "abc_linear_quad" not in med
    hard = area_between_curves_forms_for_difficulty(16)
    assert "abc_linear_axis" not in hard
    assert "abc_diag_axis" not in hard
    assert hard == ("abc_quad_axis", "abc_hline_linear", "abc_linear_quad")
    assert area_between_curves_forms_for_difficulty(22) == ("abc_linear_quad",)

    q0 = _gen("calc_app_int_area_between_curves", 0, seed=101)[0]
    assert (q0.metadata or {}).get("form_id") == "abc_linear_axis"
    assert (q0.metadata or {}).get("generator") == "area_between_curves"
    p0 = q0.prompt_latex or ""
    assert r"y=x\text{ and }y=0" in p0
    assert r"x^{2}" not in p0
    snap = (q0.metadata or {}).get("spec_snapshot") or {}
    assert snap.get("form_id") == "abc_linear_axis"
    assert snap.get("generator") == "area_between_curves"

    mid = set()
    for seed in range(40):
        q = _gen("calc_app_int_area_between_curves", 8, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        mid.add(fid)
        assert (q.metadata or {}).get("generator") == "area_between_curves"
        assert fid != "abc_linear_quad"
        assert r"y=x\text{ and }y=x^{2}" not in (q.prompt_latex or "")
    assert "abc_linear_axis" in mid
    assert mid <= {
        "abc_linear_axis",
        "abc_quad_axis",
        "abc_hline_linear",
        "abc_diag_axis",
    }

    high = set()
    for seed in range(40):
        q = _gen("calc_app_int_area_between_curves", 16, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        high.add(fid)
        p = q.prompt_latex or ""
        assert fid != "abc_linear_axis"
        assert fid != "abc_diag_axis"
        assert r"y=x\text{ and }y=0" not in p
        assert r"-x\text{ and }y=0" not in p
        assert (q.metadata or {}).get("generator") == "area_between_curves"
    assert high <= {"abc_quad_axis", "abc_hline_linear", "abc_linear_quad"}
    assert "abc_linear_quad" in high

    expert = set()
    for seed in range(24):
        q = _gen("calc_app_int_area_between_curves", 22, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        expert.add(fid)
        p = q.prompt_latex or ""
        assert fid == "abc_linear_quad"
        assert r"y=x\text{ and }y=x^{2}" in p
        assert r"-x\text{ and }y=0" not in p
        assert (q.metadata or {}).get("generator") == "area_between_curves"
        snap = (q.metadata or {}).get("spec_snapshot") or {}
        assert snap.get("form_id") == "abc_linear_quad"
        assert snap.get("generator") == "area_between_curves"
    assert expert == {"abc_linear_quad"}


def test_area_between_curves_quality_weights_tilt():
    from contextlib import nullcontext
    import random as _random

    from question_engine.frameworks.primitives.calc_app_diff import (
        sample_area_between_curves,
    )
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        live_quality_form_weights,
    )

    def _counts(weights):
        c = Counter()
        ctx = live_quality_form_weights(weights) if weights else nullcontext()
        with ctx:
            for i in range(240):
                item = sample_area_between_curves(
                    _random.Random(i), {"difficulty": 8.0}
                )
                c[item.form_id] += 1
        return c

    baseline = _counts(None)
    tilted = _counts({"abc_linear_axis": -2.5, "abc_quad_axis": 2.5})
    assert tilted["abc_quad_axis"] > baseline["abc_quad_axis"]


def test_relative_extrema_d0_parabola_high_d_shifted_lockout():
    q0 = _gen("calc_app_diff_relative_extrema", 0, seed=101)[0]
    assert (q0.metadata or {}).get("form_id") == "parabola_vertex"
    assert (q0.metadata or {}).get("generator") == "relative_extrema"
    assert "minimum" in (q0.prompt_latex or "").lower() or "minimum" in (q0.answer_latex or "").lower()
    snap = (q0.metadata or {}).get("spec_snapshot") or {}
    assert snap.get("form_id") == "parabola_vertex"

    mid = set()
    for seed in range(24):
        q = _gen("calc_app_diff_relative_extrema", 8, seed=seed)[0]
        mid.add((q.metadata or {}).get("form_id"))
    assert "parabola_vertex" in mid
    assert "cubic_first_derivative_test" in mid

    high = set()
    for seed in range(30):
        q = _gen("calc_app_diff_relative_extrema", 16, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        high.add(fid)
        assert fid != "parabola_vertex"
        assert "rel max" in (q.answer_latex or "") or "relative" in (q.answer_latex or "")
        assert (q.metadata or {}).get("generator") == "relative_extrema"
    assert high <= {"cubic_first_derivative_test", "cubic_shifted_extrema"}
    assert "cubic_shifted_extrema" in high

    expert = set()
    for seed in range(24):
        q = _gen("calc_app_diff_relative_extrema", 22, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        expert.add(fid)
        assert fid == "cubic_shifted_extrema"
        p = (q.metadata or {}).get("p")
        qv = (q.metadata or {}).get("q")
        assert p is not None and qv is not None and p != -qv
        assert (q.metadata or {}).get("generator") == "relative_extrema"
    assert expert == {"cubic_shifted_extrema"}


def test_relative_extrema_quality_weights_tilt():
    from contextlib import nullcontext
    import random as _random

    from question_engine.frameworks.primitives.calc_app_diff import (
        sample_relative_extrema,
    )
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        live_quality_form_weights,
    )

    def _counts(weights):
        c = Counter()
        ctx = live_quality_form_weights(weights) if weights else nullcontext()
        with ctx:
            for i in range(240):
                item = sample_relative_extrema(
                    _random.Random(i), {"difficulty": 8.0}
                )
                c[item.form_id] += 1
        return c

    baseline = _counts(None)
    tilted = _counts({"parabola_vertex": -2.5, "cubic_first_derivative_test": 2.5})
    assert tilted["cubic_first_derivative_test"] > baseline["cubic_first_derivative_test"]


def test_absolute_extrema_d0_parabola_high_d_shifted_lockout():
    q0 = _gen("calc_app_diff_absolute_extrema", 0, seed=101)[0]
    assert (q0.metadata or {}).get("form_id") == "closed_interval_parabola"
    assert (q0.metadata or {}).get("generator") == "absolute_extrema"
    assert "[" in (q0.prompt_latex or "")
    assert "abs min" in (q0.answer_latex or "")
    snap = (q0.metadata or {}).get("spec_snapshot") or {}
    assert snap.get("form_id") == "closed_interval_parabola"

    mid = set()
    for seed in range(24):
        q = _gen("calc_app_diff_absolute_extrema", 8, seed=seed)[0]
        mid.add((q.metadata or {}).get("form_id"))
        assert "[" in (q.prompt_latex or "")
    assert "closed_interval_parabola" in mid
    assert "closed_interval_cubic" in mid

    high = set()
    for seed in range(30):
        q = _gen("calc_app_diff_absolute_extrema", 16, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        high.add(fid)
        assert fid != "closed_interval_parabola"
        assert "abs min" in (q.answer_latex or "")
        assert (q.metadata or {}).get("generator") == "absolute_extrema"
        assert "[" in (q.prompt_latex or "")
    assert high <= {"closed_interval_cubic", "closed_interval_shifted_cubic"}
    assert "closed_interval_shifted_cubic" in high

    expert = set()
    for seed in range(24):
        q = _gen("calc_app_diff_absolute_extrema", 22, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        expert.add(fid)
        assert fid == "closed_interval_shifted_cubic"
        p = (q.metadata or {}).get("p")
        qv = (q.metadata or {}).get("q")
        assert p is not None and qv is not None and p != -qv
        iv = (q.metadata or {}).get("interval")
        assert iv is not None and len(iv) == 2
        lo, hi = iv
        assert lo < p < qv < hi
        assert (q.metadata or {}).get("generator") == "absolute_extrema"
    assert expert == {"closed_interval_shifted_cubic"}


def test_absolute_extrema_quality_weights_tilt():
    from contextlib import nullcontext
    import random as _random

    from question_engine.frameworks.primitives.calc_app_diff import (
        sample_absolute_extrema,
    )
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        live_quality_form_weights,
    )

    def _counts(weights):
        c = Counter()
        ctx = live_quality_form_weights(weights) if weights else nullcontext()
        with ctx:
            for i in range(240):
                item = sample_absolute_extrema(
                    _random.Random(i), {"difficulty": 8.0}
                )
                c[item.form_id] += 1
        return c

    baseline = _counts(None)
    tilted = _counts(
        {"closed_interval_parabola": -2.5, "closed_interval_cubic": 2.5}
    )
    assert tilted["closed_interval_cubic"] > baseline["closed_interval_cubic"]


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


def test_rolles_d0_even_quad_high_d_cubic_lockout():
    q0 = _gen("calc_app_diff_rolles_theorem", 0, seed=101)[0]
    assert (q0.metadata or {}).get("form_id") == "rolles_even_quad"
    assert (q0.metadata or {}).get("generator") == "rolles_theorem"
    assert (q0.answer_latex or "") == "0"
    snap = (q0.metadata or {}).get("spec_snapshot") or {}
    assert snap.get("form_id") == "rolles_even_quad"

    mid = set()
    for seed in range(24):
        q = _gen("calc_app_diff_rolles_theorem", 8, seed=seed)[0]
        mid.add((q.metadata or {}).get("form_id"))
    assert "rolles_even_quad" in mid
    assert "rolles_two_roots" in mid

    high = set()
    for seed in range(30):
        q = _gen("calc_app_diff_rolles_theorem", 16, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        high.add(fid)
        assert fid != "rolles_even_quad"
        assert (q.answer_latex or "") != "0"
        assert (q.metadata or {}).get("generator") == "rolles_theorem"
    assert high <= {"rolles_two_roots", "rolles_cubic_odd"}
    assert "rolles_cubic_odd" in high

    expert = set()
    for seed in range(24):
        q = _gen("calc_app_diff_rolles_theorem", 22, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        expert.add(fid)
        assert fid == "rolles_cubic_odd"
        assert (q.answer_latex or "") != "0"
        assert r"\sqrt" in (q.answer_latex or "")
    assert expert == {"rolles_cubic_odd"}


def test_rolles_quality_weights_tilt():
    from contextlib import nullcontext
    import random as _random

    from question_engine.frameworks.primitives.calc_app_diff import (
        sample_rolles,
    )
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        live_quality_form_weights,
    )

    def _counts(weights):
        c = Counter()
        ctx = live_quality_form_weights(weights) if weights else nullcontext()
        with ctx:
            for i in range(240):
                item = sample_rolles(_random.Random(i), {"difficulty": 8.0})
                c[item.form_id] += 1
        return c

    baseline = _counts(None)
    tilted = _counts({"rolles_even_quad": -2.5, "rolles_two_roots": 2.5})
    assert tilted["rolles_two_roots"] > baseline["rolles_two_roots"]


def test_newton_d0_one_quad_high_d_two_cubic_lockout():
    from question_engine.frameworks.primitives.calc_app_diff import (
        newton_forms_for_difficulty,
    )

    assert newton_forms_for_difficulty(0) == ("newton_one_quad",)
    med = newton_forms_for_difficulty(8)
    assert "newton_one_quad" in med and "newton_one_cubic" in med
    hard = newton_forms_for_difficulty(16)
    assert "newton_one_quad" not in hard
    assert hard == ("newton_one_cubic", "newton_two_cubic")
    assert newton_forms_for_difficulty(22) == ("newton_two_cubic",)

    q0 = _gen("calc_app_diff_newtons_method", 0, seed=101)[0]
    assert (q0.metadata or {}).get("form_id") == "newton_one_quad"
    assert (q0.metadata or {}).get("generator") == "newtons_method"
    assert r"x^{2}" in (q0.prompt_latex or "")
    assert "x_1=" in (q0.answer_latex or "")
    snap = (q0.metadata or {}).get("spec_snapshot") or {}
    assert snap.get("form_id") == "newton_one_quad"
    assert snap.get("generator") == "newtons_method"

    mid = set()
    for seed in range(24):
        q = _gen("calc_app_diff_newtons_method", 8, seed=seed)[0]
        mid.add((q.metadata or {}).get("form_id"))
        assert "x_1=" in (q.answer_latex or "")
    assert "newton_one_quad" in mid
    assert "newton_one_cubic" in mid

    high = set()
    for seed in range(30):
        q = _gen("calc_app_diff_newtons_method", 16, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        high.add(fid)
        assert fid != "newton_one_quad"
        assert r"x^{2}" not in (q.prompt_latex or "")
        assert (q.metadata or {}).get("generator") == "newtons_method"
    assert high <= {"newton_one_cubic", "newton_two_cubic"}
    assert "newton_two_cubic" in high

    expert = set()
    for seed in range(24):
        q = _gen("calc_app_diff_newtons_method", 22, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        expert.add(fid)
        assert fid == "newton_two_cubic"
        assert "x_2=" in (q.answer_latex or "")
        assert r"x^{3}" in (q.prompt_latex or "")
        assert (q.metadata or {}).get("generator") == "newtons_method"
        snap = (q.metadata or {}).get("spec_snapshot") or {}
        assert snap.get("form_id") == "newton_two_cubic"
    assert expert == {"newton_two_cubic"}


def test_newton_quality_weights_tilt():
    from contextlib import nullcontext
    import random as _random

    from question_engine.frameworks.primitives.calc_app_diff import (
        sample_newton,
    )
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        live_quality_form_weights,
    )

    def _counts(weights):
        c = Counter()
        ctx = live_quality_form_weights(weights) if weights else nullcontext()
        with ctx:
            for i in range(240):
                item = sample_newton(_random.Random(i), {"difficulty": 8.0})
                c[item.form_id] += 1
        return c

    baseline = _counts(None)
    tilted = _counts({"newton_one_quad": -2.5, "newton_one_cubic": 2.5})
    assert tilted["newton_one_cubic"] > baseline["newton_one_cubic"]


def test_differentials_d0_easy_high_d_nested_lockout():
    from question_engine.frameworks.primitives.calc_app_diff import (
        differential_forms_for_difficulty,
    )

    easy = ("poly_power", "poly_quad", "trig", "exp", "ln")
    assert differential_forms_for_difficulty(0) == easy
    med = differential_forms_for_difficulty(8)
    assert "ln" in med and "poly_power" in med
    assert "radical" in med and "reciprocal" in med
    assert "chain_exp" not in med and "quotient" not in med
    hard = differential_forms_for_difficulty(16)
    assert "ln" not in hard and "poly_power" not in hard and "trig" not in hard
    assert hard == (
        "radical", "reciprocal", "product", "quotient", "chain_exp", "eval_dx",
    )
    assert differential_forms_for_difficulty(22) == (
        "product", "quotient", "chain_exp", "eval_dx",
    )

    q0 = _gen("calc_app_diff_differentials", 0, seed=101)[0]
    assert (q0.metadata or {}).get("form_id") in easy
    assert (q0.metadata or {}).get("generator") == "differentials"
    assert r"find }dy" in (q0.prompt_latex or "")
    snap = (q0.metadata or {}).get("spec_snapshot") or {}
    assert snap.get("form_id") in easy
    assert snap.get("generator") == "differentials"

    d0 = set()
    for seed in range(40):
        q = _gen("calc_app_diff_differentials", 0, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        d0.add(fid)
        assert fid in easy
        assert (q.metadata or {}).get("generator") == "differentials"
        assert (q.metadata or {}).get("structure_id", "").startswith("differentials:")
    assert len(d0) >= 3, d0

    mid = set()
    for seed in range(40):
        q = _gen("calc_app_diff_differentials", 8, seed=seed)[0]
        mid.add((q.metadata or {}).get("form_id"))
        assert (q.metadata or {}).get("generator") == "differentials"
    assert mid & {"ln", "poly_power", "poly_quad", "trig", "exp"}
    assert mid & {"radical", "reciprocal"}
    assert mid <= set(med)

    high = set()
    for seed in range(40):
        q = _gen("calc_app_diff_differentials", 16, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        high.add(fid)
        assert fid not in easy
        assert (q.metadata or {}).get("generator") == "differentials"
    assert high <= set(hard)
    assert high & {"product", "quotient", "chain_exp", "eval_dx"}
    assert high & {"radical", "reciprocal"}

    expert = set()
    for seed in range(40):
        q = _gen("calc_app_diff_differentials", 22, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        expert.add(fid)
        assert fid in {"product", "quotient", "chain_exp", "eval_dx"}
        assert fid not in easy
        assert fid not in {"radical", "reciprocal"}
        assert (q.metadata or {}).get("generator") == "differentials"
        snap = (q.metadata or {}).get("spec_snapshot") or {}
        assert snap.get("form_id") == fid
        assert snap.get("generator") == "differentials"
    assert len(expert) >= 2, expert


def test_differentials_quality_weights_tilt():
    from contextlib import nullcontext
    import random as _random

    from question_engine.frameworks.primitives.calc_app_diff import (
        sample_differentials,
    )
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        live_quality_form_weights,
    )

    def _counts(weights):
        c = Counter()
        ctx = live_quality_form_weights(weights) if weights else nullcontext()
        with ctx:
            for i in range(240):
                item = sample_differentials(_random.Random(i), {"difficulty": 8.0})
                c[item.form_id] += 1
        return c

    baseline = _counts(None)
    tilted = _counts({"ln": -2.5, "reciprocal": 2.5})
    assert tilted["reciprocal"] > baseline["reciprocal"]


def test_linear_approx_d0_easy_high_d_lockout():
    from question_engine.frameworks.primitives.calc_app_diff import (
        linear_approx_forms_for_difficulty,
    )

    easy = ("quad", "sqrt")
    assert linear_approx_forms_for_difficulty(0) == easy
    med = linear_approx_forms_for_difficulty(8)
    assert "quad" in med and "sqrt" in med
    assert "quad_estimate" in med and "reciprocal" in med and "exp" in med
    hard = linear_approx_forms_for_difficulty(16)
    assert "quad" not in hard and "quad_estimate" not in hard
    assert hard == ("sqrt", "reciprocal", "exp")
    assert linear_approx_forms_for_difficulty(22) == ("reciprocal", "exp")

    q0 = _gen("calc_app_diff_linear_approximations", 0, seed=101)[0]
    assert (q0.metadata or {}).get("form_id") in easy
    assert (q0.metadata or {}).get("generator") == "linear_approximation"
    assert "linear approximation" in (q0.prompt_latex or "")
    snap = (q0.metadata or {}).get("spec_snapshot") or {}
    assert snap.get("form_id") in easy
    assert snap.get("generator") == "linear_approximation"
    assert snap.get("pack") == "structured_linear_approximation"

    d0 = set()
    for seed in range(40):
        q = _gen("calc_app_diff_linear_approximations", 0, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        d0.add(fid)
        assert fid in easy
        assert (q.metadata or {}).get("generator") == "linear_approximation"
        assert (q.metadata or {}).get("structure_id", "").startswith(
            "linear_approximation:"
        )
        assert "x^{2}" in (q.prompt_latex or "") or r"\sqrt{x}" in (q.prompt_latex or "")
        assert "estimate" not in (q.prompt_latex or "")
    assert d0 == set(easy), d0

    mid = set()
    for seed in range(40):
        q = _gen("calc_app_diff_linear_approximations", 8, seed=seed)[0]
        mid.add((q.metadata or {}).get("form_id"))
        assert (q.metadata or {}).get("generator") == "linear_approximation"
    assert mid & {"quad", "sqrt"}
    assert mid & {"reciprocal", "exp", "quad_estimate"}
    assert mid <= set(med)

    high = set()
    for seed in range(40):
        q = _gen("calc_app_diff_linear_approximations", 16, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        high.add(fid)
        assert fid not in {"quad", "quad_estimate"}
        assert (q.metadata or {}).get("generator") == "linear_approximation"
        assert "x^{2}" not in (q.prompt_latex or "")
    assert high <= set(hard)
    assert high & {"reciprocal", "exp"}
    assert "sqrt" in high

    expert = set()
    for seed in range(40):
        q = _gen("calc_app_diff_linear_approximations", 22, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        expert.add(fid)
        assert fid in {"reciprocal", "exp"}
        assert fid not in easy
        assert fid != "quad_estimate"
        assert (q.metadata or {}).get("generator") == "linear_approximation"
        snap = (q.metadata or {}).get("spec_snapshot") or {}
        assert snap.get("form_id") == fid
        assert snap.get("generator") == "linear_approximation"
        p = q.prompt_latex or ""
        assert r"\frac{1}{x}" in p or r"e^{x}" in p
        assert "x^{2}" not in p
        assert r"\sqrt{x}" not in p
    assert expert == {"reciprocal", "exp"}, expert


def test_linear_approx_quality_weights_tilt():
    from contextlib import nullcontext
    import random as _random

    from question_engine.frameworks.primitives.calc_app_diff import (
        sample_linear_approximation,
    )
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        live_quality_form_weights,
    )

    def _counts(weights):
        c = Counter()
        ctx = live_quality_form_weights(weights) if weights else nullcontext()
        with ctx:
            for i in range(240):
                item = sample_linear_approximation(
                    _random.Random(i), {"difficulty": 8.0}
                )
                c[item.form_id] += 1
        return c

    baseline = _counts(None)
    tilted = _counts({"quad": -2.5, "reciprocal": 2.5})
    assert tilted["reciprocal"] > baseline["reciprocal"]


def test_tangent_normal_d0_easy_high_d_lockout():
    from question_engine.frameworks.primitives.calc_app_diff import (
        tangent_forms_for_difficulty,
    )

    easy = ("poly_mono", "poly_quad", "trig", "exp", "ln")
    assert tangent_forms_for_difficulty(0) == easy
    med = tangent_forms_for_difficulty(8)
    assert "poly_mono" in med and "ln" in med
    assert "reciprocal" in med and "radical" in med
    assert "trig_chain" not in med and "poly_cubic" not in med
    hard = tangent_forms_for_difficulty(16)
    assert "poly_mono" not in hard and "ln" not in hard and "trig" not in hard
    assert hard == (
        "reciprocal", "radical", "poly_cubic", "rational_linear", "trig_chain",
    )
    assert tangent_forms_for_difficulty(22) == (
        "poly_cubic", "rational_linear", "trig_chain",
    )

    q0 = _gen("calc_app_diff_slope_tangent_and_normal_lines", 0, seed=101)[0]
    assert (q0.metadata or {}).get("form_id") in easy
    assert (q0.metadata or {}).get("generator") == "tangent_normal_line"
    assert "tangent line" in (q0.prompt_latex or "")
    snap = (q0.metadata or {}).get("spec_snapshot") or {}
    assert snap.get("form_id") in easy
    assert snap.get("generator") == "tangent_normal_line"
    assert snap.get("pack") == "structured_tangent_normal_line"

    d0 = set()
    for seed in range(40):
        q = _gen("calc_app_diff_slope_tangent_and_normal_lines", 0, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        d0.add(fid)
        assert fid in easy
        assert (q.metadata or {}).get("generator") == "tangent_normal_line"
        assert (q.metadata or {}).get("structure_id", "").startswith(
            "tangent_normal_line:"
        )
        assert "normal line" not in (q.prompt_latex or "")
    assert len(d0) >= 3, d0

    mid = set()
    for seed in range(40):
        q = _gen("calc_app_diff_slope_tangent_and_normal_lines", 8, seed=seed)[0]
        mid.add((q.metadata or {}).get("form_id"))
        assert (q.metadata or {}).get("generator") == "tangent_normal_line"
    assert mid & {"poly_mono", "poly_quad", "trig", "exp", "ln"}
    assert mid & {"reciprocal", "radical"}
    assert mid <= set(med)

    high = set()
    for seed in range(40):
        q = _gen("calc_app_diff_slope_tangent_and_normal_lines", 16, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        high.add(fid)
        assert fid not in easy
        assert (q.metadata or {}).get("generator") == "tangent_normal_line"
        p = q.prompt_latex or ""
        assert r"\ln" not in p
        assert r"e^{" not in p and r"\exp" not in p
    assert high <= set(hard)
    assert high & {"poly_cubic", "rational_linear", "trig_chain"}
    assert high & {"reciprocal", "radical"}

    expert = set()
    for seed in range(40):
        q = _gen("calc_app_diff_slope_tangent_and_normal_lines", 22, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        expert.add(fid)
        assert fid in {"poly_cubic", "rational_linear", "trig_chain"}
        assert fid not in easy
        assert fid not in {"reciprocal", "radical"}
        assert (q.metadata or {}).get("generator") == "tangent_normal_line"
        snap = (q.metadata or {}).get("spec_snapshot") or {}
        assert snap.get("form_id") == fid
        assert snap.get("generator") == "tangent_normal_line"
        p = q.prompt_latex or ""
        assert r"\ln" not in p
        assert r"\frac{1}{x}" not in p and r"x^{-1}" not in p
        assert r"\sqrt" not in p
    assert len(expert) >= 2, expert


def test_tangent_normal_quality_weights_tilt():
    from contextlib import nullcontext
    import random as _random

    from question_engine.frameworks.primitives.calc_app_diff import (
        sample_tangent_normal_line,
    )
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        live_quality_form_weights,
    )

    def _counts(weights):
        c = Counter()
        ctx = live_quality_form_weights(weights) if weights else nullcontext()
        with ctx:
            for i in range(240):
                item = sample_tangent_normal_line(
                    _random.Random(i), {"difficulty": 8.0}
                )
                c[item.form_id] += 1
        return c

    baseline = _counts(None)
    tilted = _counts({"poly_mono": -2.5, "reciprocal": 2.5})
    assert tilted["reciprocal"] > baseline["reciprocal"]


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
    assert "0" in (qih.answer_latex or "") or (qih.metadata or {}).get(
        "form_id"
    ) in {"disp_const_v", "disp_sign_change"}


def test_motion_integral_d0_linear_high_d_sign_change_lockout():
    from question_engine.frameworks.primitives.calc_app_diff import (
        motion_integral_forms_for_difficulty,
    )

    assert motion_integral_forms_for_difficulty(0) == ("disp_linear_v",)
    med = motion_integral_forms_for_difficulty(8)
    assert "disp_linear_v" in med and "disp_const_v" in med
    hard = motion_integral_forms_for_difficulty(16)
    assert "disp_linear_v" not in hard
    assert hard == ("disp_const_v", "disp_sign_change")
    assert motion_integral_forms_for_difficulty(22) == ("disp_sign_change",)

    q0 = _gen("calc_app_int_motion_along_a_line_revisited", 0, seed=101)[0]
    assert (q0.metadata or {}).get("form_id") == "disp_linear_v"
    assert (q0.metadata or {}).get("generator") == "motion_along_a_line_integral"
    assert r"v(t)=2t." in (q0.prompt_latex or "")
    assert "displacement" in (q0.prompt_latex or "").lower()
    snap = (q0.metadata or {}).get("spec_snapshot") or {}
    assert snap.get("form_id") == "disp_linear_v"
    assert snap.get("generator") == "motion_along_a_line_integral"

    mid = set()
    for seed in range(24):
        q = _gen("calc_app_int_motion_along_a_line_revisited", 8, seed=seed)[0]
        mid.add((q.metadata or {}).get("form_id"))
        assert (q.metadata or {}).get("generator") == "motion_along_a_line_integral"
        assert r"v(t)=2t-" not in (q.prompt_latex or "")
    assert "disp_linear_v" in mid
    assert "disp_const_v" in mid
    assert mid <= {"disp_linear_v", "disp_const_v"}

    high = set()
    for seed in range(30):
        q = _gen("calc_app_int_motion_along_a_line_revisited", 16, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        high.add(fid)
        assert fid != "disp_linear_v"
        assert r"v(t)=2t." not in (q.prompt_latex or "")
        assert (q.metadata or {}).get("generator") == "motion_along_a_line_integral"
    assert high <= {"disp_const_v", "disp_sign_change"}
    assert "disp_sign_change" in high

    expert = set()
    for seed in range(24):
        q = _gen("calc_app_int_motion_along_a_line_revisited", 22, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        expert.add(fid)
        assert fid == "disp_sign_change"
        assert (q.answer_latex or "") == "0"
        assert r"v(t)=2t-" in (q.prompt_latex or "")
        assert (q.metadata or {}).get("generator") == "motion_along_a_line_integral"
        snap = (q.metadata or {}).get("spec_snapshot") or {}
        assert snap.get("form_id") == "disp_sign_change"
        assert snap.get("generator") == "motion_along_a_line_integral"
    assert expert == {"disp_sign_change"}


def test_motion_integral_quality_weights_tilt():
    from contextlib import nullcontext
    import random as _random

    from question_engine.frameworks.primitives.calc_app_diff import (
        sample_motion_integral,
    )
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        live_quality_form_weights,
    )

    def _counts(weights):
        c = Counter()
        ctx = live_quality_form_weights(weights) if weights else nullcontext()
        with ctx:
            for i in range(240):
                item = sample_motion_integral(
                    _random.Random(i), {"difficulty": 8.0}
                )
                c[item.form_id] += 1
        return c

    baseline = _counts(None)
    tilted = _counts({"disp_linear_v": -2.5, "disp_const_v": 2.5})
    assert tilted["disp_const_v"] > baseline["disp_const_v"]


def test_motion_d0_eval_velocity_high_d_cubic_lockout():
    q0 = _gen("calc_app_diff_motion_along_a_line", 0, seed=101)[0]
    assert (q0.metadata or {}).get("form_id") == "eval_velocity"
    assert (q0.metadata or {}).get("generator") == "motion_along_a_line"
    assert r"s(t)=t^{2}" in (q0.prompt_latex or "")
    assert r"Find }v(" in (q0.prompt_latex or "")
    snap = (q0.metadata or {}).get("spec_snapshot") or {}
    assert snap.get("form_id") == "eval_velocity"
    assert snap.get("generator") == "motion_along_a_line"

    mid = set()
    for seed in range(24):
        q = _gen("calc_app_diff_motion_along_a_line", 8, seed=seed)[0]
        mid.add((q.metadata or {}).get("form_id"))
        assert r"t^{2}" in (q.prompt_latex or "")
    assert "eval_velocity" in mid
    assert "particle_at_rest" in mid

    high = set()
    for seed in range(30):
        q = _gen("calc_app_diff_motion_along_a_line", 16, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        high.add(fid)
        assert fid != "eval_velocity"
        assert fid != "acceleration_const"
        assert (q.metadata or {}).get("generator") == "motion_along_a_line"
        assert "at rest" in (q.prompt_latex or "")
    assert high <= {"particle_at_rest", "cubic_at_rest"}
    assert "cubic_at_rest" in high

    expert = set()
    for seed in range(30):
        q = _gen("calc_app_diff_motion_along_a_line", 22, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        expert.add(fid)
        assert fid not in {"eval_velocity", "particle_at_rest", "acceleration_const"}
        plain = (q.prompt_latex or "").replace(" ", "")
        assert "s(t)=t^{2}-" not in plain
        assert (q.metadata or {}).get("generator") == "motion_along_a_line"
        snap = (q.metadata or {}).get("spec_snapshot") or {}
        assert snap.get("form_id") == fid
        assert snap.get("generator") == "motion_along_a_line"
    assert expert <= {"cubic_at_rest", "cubic_speed_sign"}
    assert "cubic_at_rest" in expert
    assert "cubic_speed_sign" in expert


def test_motion_quality_weights_tilt():
    from contextlib import nullcontext
    import random as _random

    from question_engine.frameworks.primitives.calc_app_diff import (
        sample_motion,
    )
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        live_quality_form_weights,
    )

    def _counts(weights):
        c = Counter()
        ctx = live_quality_form_weights(weights) if weights else nullcontext()
        with ctx:
            for i in range(240):
                item = sample_motion(_random.Random(i), {"difficulty": 8.0})
                c[item.form_id] += 1
        return c

    baseline = _counts(None)
    tilted = _counts({"eval_velocity": -2.5, "particle_at_rest": 2.5})
    assert tilted["particle_at_rest"] > baseline["particle_at_rest"]


def test_de_intro_d0_exp_high_d_euler_lockout():
    from question_engine.frameworks.primitives.calc_app_diff import (
        de_intro_forms_for_difficulty,
    )

    assert de_intro_forms_for_difficulty(0) == ("verify_exp",)
    med = de_intro_forms_for_difficulty(8)
    assert "verify_exp" in med and "verify_euler" in med
    hard = de_intro_forms_for_difficulty(16)
    assert "verify_exp" not in hard
    assert hard == ("verify_euler",)
    assert de_intro_forms_for_difficulty(22) == ("verify_euler",)

    q0 = _gen("calc_diff_eq_introduction", 0, seed=101)[0]
    assert (q0.metadata or {}).get("form_id") == "verify_exp"
    assert (q0.metadata or {}).get("generator") == "de_introduction"
    assert "Verify" in (q0.prompt_latex or "")
    assert "e^" in (q0.prompt_latex or "")
    snap = (q0.metadata or {}).get("spec_snapshot") or {}
    assert snap.get("form_id") == "verify_exp"
    assert snap.get("generator") == "de_introduction"

    mid = set()
    for seed in range(24):
        q = _gen("calc_diff_eq_introduction", 8, seed=seed)[0]
        mid.add((q.metadata or {}).get("form_id"))
        assert (q.metadata or {}).get("generator") == "de_introduction"
        assert "Verify" in (q.prompt_latex or "")
    assert "verify_exp" in mid
    assert "verify_euler" in mid
    assert mid <= {"verify_exp", "verify_euler"}

    high = set()
    for seed in range(30):
        q = _gen("calc_diff_eq_introduction", 16, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        high.add(fid)
        assert fid == "verify_euler"
        assert "e^" not in (q.prompt_latex or "")
        assert "Cx" in (q.prompt_latex or "") or "x^{" in (q.prompt_latex or "")
        assert (q.metadata or {}).get("generator") == "de_introduction"
    assert high == {"verify_euler"}

    expert = set()
    for seed in range(24):
        q = _gen("calc_diff_eq_introduction", 22, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        expert.add(fid)
        assert fid == "verify_euler"
        assert "e^" not in (q.prompt_latex or "")
        assert (q.metadata or {}).get("generator") == "de_introduction"
        snap = (q.metadata or {}).get("spec_snapshot") or {}
        assert snap.get("form_id") == "verify_euler"
        assert snap.get("generator") == "de_introduction"
    assert expert == {"verify_euler"}


def test_slope_field_d0_x_high_d_xy_lockout():
    from question_engine.frameworks.primitives.calc_app_diff import (
        slope_field_forms_for_difficulty,
    )

    assert slope_field_forms_for_difficulty(0) == ("sf_x",)
    med = slope_field_forms_for_difficulty(8)
    assert "sf_x" in med and "sf_x_plus_y" in med
    hard = slope_field_forms_for_difficulty(16)
    assert "sf_x" not in hard
    assert hard == ("sf_x_plus_y", "sf_xy")
    assert slope_field_forms_for_difficulty(22) == ("sf_xy",)

    q0 = _gen("calc_diff_eq_slope_fields", 0, seed=101)[0]
    assert (q0.metadata or {}).get("form_id") == "sf_x"
    assert (q0.metadata or {}).get("generator") == "slope_field_interpret"
    assert "y'=x," in (q0.prompt_latex or "")
    assert "x+y" not in (q0.prompt_latex or "")
    assert "xy" not in (q0.prompt_latex or "")
    snap = (q0.metadata or {}).get("spec_snapshot") or {}
    assert snap.get("form_id") == "sf_x"
    assert snap.get("generator") == "slope_field_interpret"

    mid = set()
    for seed in range(24):
        q = _gen("calc_diff_eq_slope_fields", 8, seed=seed)[0]
        mid.add((q.metadata or {}).get("form_id"))
        assert (q.metadata or {}).get("generator") == "slope_field_interpret"
        assert "y'=xy" not in (q.prompt_latex or "")
    assert "sf_x" in mid
    assert "sf_x_plus_y" in mid
    assert mid <= {"sf_x", "sf_x_plus_y"}

    high = set()
    for seed in range(30):
        q = _gen("calc_diff_eq_slope_fields", 16, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        high.add(fid)
        assert fid != "sf_x"
        p = q.prompt_latex or ""
        assert "y'=x," not in p
        assert (q.metadata or {}).get("generator") == "slope_field_interpret"
    assert high <= {"sf_x_plus_y", "sf_xy"}
    assert "sf_xy" in high

    expert = set()
    for seed in range(24):
        q = _gen("calc_diff_eq_slope_fields", 22, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        expert.add(fid)
        assert fid == "sf_xy"
        assert "y'=xy" in (q.prompt_latex or "")
        assert (q.metadata or {}).get("generator") == "slope_field_interpret"
        snap = (q.metadata or {}).get("spec_snapshot") or {}
        assert snap.get("form_id") == "sf_xy"
        assert snap.get("generator") == "slope_field_interpret"
    assert expert == {"sf_xy"}


def test_slope_field_quality_weights_tilt():
    from contextlib import nullcontext
    import random as _random

    from question_engine.frameworks.primitives.calc_app_diff import (
        sample_slope_field,
    )
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        live_quality_form_weights,
    )

    def _counts(weights):
        c = Counter()
        ctx = live_quality_form_weights(weights) if weights else nullcontext()
        with ctx:
            for i in range(240):
                item = sample_slope_field(_random.Random(i), {"difficulty": 8.0})
                c[item.form_id] += 1
        return c

    baseline = _counts(None)
    tilted = _counts({"sf_x": -2.5, "sf_x_plus_y": 2.5})
    assert tilted["sf_x_plus_y"] > baseline["sf_x_plus_y"]


def test_growth_decay_d0_story_high_d_half_life_lockout():
    from question_engine.frameworks.primitives.calc_app_diff import (
        growth_decay_forms_for_difficulty,
    )

    assert growth_decay_forms_for_difficulty(0) == ("egd_growth_story",)
    med = growth_decay_forms_for_difficulty(8)
    assert "egd_growth_story" in med
    assert "egd_decay_story" in med and "egd_ivp" in med
    hard = growth_decay_forms_for_difficulty(16)
    assert "egd_growth_story" not in hard
    assert hard == ("egd_decay_story", "egd_ivp", "egd_doubling", "egd_half_life")
    assert growth_decay_forms_for_difficulty(22) == ("egd_doubling", "egd_half_life")

    q0 = _gen("calc_diff_eq_exponential_growth_and_decay", 0, seed=101)[0]
    assert (q0.metadata or {}).get("form_id") == "egd_growth_story"
    assert (q0.metadata or {}).get("generator") == "calc_continuous_growth_decay"
    p0 = q0.prompt_latex or ""
    assert "grows continuously" in p0
    assert "y'=" in p0 and "y'=-" not in p0
    assert "Solve" not in p0
    assert "half-life" not in p0 and "doubles" not in p0
    snap = (q0.metadata or {}).get("spec_snapshot") or {}
    assert snap.get("form_id") == "egd_growth_story"
    assert snap.get("generator") == "calc_continuous_growth_decay"

    mid = set()
    for seed in range(36):
        q = _gen("calc_diff_eq_exponential_growth_and_decay", 8, seed=seed)[0]
        mid.add((q.metadata or {}).get("form_id"))
        assert (q.metadata or {}).get("generator") == "calc_continuous_growth_decay"
        p = q.prompt_latex or ""
        assert "half-life" not in p
        assert "doubles" not in p
    assert "egd_growth_story" in mid
    assert "egd_decay_story" in mid
    assert "egd_ivp" in mid
    assert mid <= {"egd_growth_story", "egd_decay_story", "egd_ivp"}

    high = set()
    for seed in range(40):
        q = _gen("calc_diff_eq_exponential_growth_and_decay", 16, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        high.add(fid)
        assert fid != "egd_growth_story"
        p = q.prompt_latex or ""
        assert "grows continuously" not in p
        assert (q.metadata or {}).get("generator") == "calc_continuous_growth_decay"
    leftover = {"egd_decay_story", "egd_ivp"}
    hard_forms = {"egd_doubling", "egd_half_life"}
    assert high <= leftover | hard_forms
    assert high & leftover
    assert high & hard_forms

    expert = set()
    for seed in range(24):
        q = _gen("calc_diff_eq_exponential_growth_and_decay", 22, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        expert.add(fid)
        p = q.prompt_latex or ""
        assert fid in {"egd_doubling", "egd_half_life"}
        assert "grows continuously" not in p
        assert "Solve" not in p
        assert "decays continuously" not in p
        assert (q.metadata or {}).get("generator") == "calc_continuous_growth_decay"
        snap = (q.metadata or {}).get("spec_snapshot") or {}
        assert snap.get("form_id") == fid
        assert snap.get("generator") == "calc_continuous_growth_decay"
    assert expert == {"egd_doubling", "egd_half_life"}


def test_growth_decay_quality_weights_tilt():
    from contextlib import nullcontext
    import random as _random

    from question_engine.frameworks.primitives.calc_app_diff import (
        sample_growth_decay,
    )
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        live_quality_form_weights,
    )

    def _counts(weights):
        c = Counter()
        ctx = live_quality_form_weights(weights) if weights else nullcontext()
        with ctx:
            for i in range(240):
                item = sample_growth_decay(_random.Random(i), {"difficulty": 8.0})
                c[item.form_id] += 1
        return c

    baseline = _counts(None)
    tilted = _counts({"egd_growth_story": -2.5, "egd_ivp": 2.5})
    assert tilted["egd_ivp"] > baseline["egd_ivp"]


def test_separable_d0_poly_high_d_homogeneous_lockout():
    from question_engine.frameworks.primitives.calc_app_diff import (
        separable_forms_for_difficulty,
    )

    assert separable_forms_for_difficulty(0) == ("sep_poly",)
    med = separable_forms_for_difficulty(8)
    assert "sep_poly" in med and "sep_exp" in med
    hard = separable_forms_for_difficulty(16)
    assert "sep_poly" not in hard
    assert hard == ("sep_exp", "sep_homogeneous")
    assert separable_forms_for_difficulty(22) == ("sep_homogeneous",)

    q0 = _gen("calc_diff_eq_separable", 0, seed=101)[0]
    assert (q0.metadata or {}).get("form_id") == "sep_poly"
    assert (q0.metadata or {}).get("generator") == "separable_diff_eq"
    assert r"\frac{dy}{dx}" in (q0.prompt_latex or "")
    assert r"\frac{y}{x}" not in (q0.prompt_latex or "")
    assert "e^" not in (q0.answer_latex or "")
    snap = (q0.metadata or {}).get("spec_snapshot") or {}
    assert snap.get("form_id") == "sep_poly"
    assert snap.get("generator") == "separable_diff_eq"

    mid = set()
    for seed in range(24):
        q = _gen("calc_diff_eq_separable", 8, seed=seed)[0]
        mid.add((q.metadata or {}).get("form_id"))
        assert (q.metadata or {}).get("generator") == "separable_diff_eq"
        assert r"\frac{y}{x}" not in (q.prompt_latex or "")
    assert "sep_poly" in mid
    assert "sep_exp" in mid
    assert mid <= {"sep_poly", "sep_exp"}

    high = set()
    for seed in range(30):
        q = _gen("calc_diff_eq_separable", 16, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        high.add(fid)
        assert fid != "sep_poly"
        p = q.prompt_latex or ""
        assert not (
            r"=x," in p or r"=2x," in p or r"=3x," in p
        )
        assert (q.metadata or {}).get("generator") == "separable_diff_eq"
    assert high <= {"sep_exp", "sep_homogeneous"}
    assert "sep_homogeneous" in high

    expert = set()
    for seed in range(24):
        q = _gen("calc_diff_eq_separable", 22, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        expert.add(fid)
        assert fid == "sep_homogeneous"
        assert r"\frac{y}{x}" in (q.prompt_latex or "")
        assert (q.answer_latex or "") == "y=4x"
        assert (q.metadata or {}).get("generator") == "separable_diff_eq"
        snap = (q.metadata or {}).get("spec_snapshot") or {}
        assert snap.get("form_id") == "sep_homogeneous"
        assert snap.get("generator") == "separable_diff_eq"
    assert expert == {"sep_homogeneous"}


def test_separable_quality_weights_tilt():
    from contextlib import nullcontext
    import random as _random

    from question_engine.frameworks.primitives.calc_app_diff import (
        sample_separable_de,
    )
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        live_quality_form_weights,
    )

    def _counts(weights):
        c = Counter()
        ctx = live_quality_form_weights(weights) if weights else nullcontext()
        with ctx:
            for i in range(240):
                item = sample_separable_de(_random.Random(i), {"difficulty": 8.0})
                c[item.form_id] += 1
        return c

    baseline = _counts(None)
    tilted = _counts({"sep_poly": -2.5, "sep_exp": 2.5})
    assert tilted["sep_exp"] > baseline["sep_exp"]


def test_de_intro_quality_weights_tilt():
    from contextlib import nullcontext
    import random as _random

    from question_engine.frameworks.primitives.calc_app_diff import (
        sample_de_intro,
    )
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        live_quality_form_weights,
    )

    def _counts(weights):
        c = Counter()
        ctx = live_quality_form_weights(weights) if weights else nullcontext()
        with ctx:
            for i in range(240):
                item = sample_de_intro(_random.Random(i), {"difficulty": 8.0})
                c[item.form_id] += 1
        return c

    baseline = _counts(None)
    tilted = _counts({"verify_exp": -2.5, "verify_euler": 2.5})
    assert tilted["verify_euler"] > baseline["verify_euler"]


def test_curve_sketch_d0_parabola_high_d_shifted_lockout():
    qs = _gen("calc_app_diff_curve_sketching", 0, seed=101)[0]
    assert (qs.metadata or {}).get("form_id") == "parabola_sketch"
    assert (qs.metadata or {}).get("generator") == "curve_sketching"
    assert "vertex" in (qs.answer_latex or "")
    snap = (qs.metadata or {}).get("spec_snapshot") or {}
    assert snap.get("form_id") == "parabola_sketch"

    mid = set()
    for seed in range(24):
        q = _gen("calc_app_diff_curve_sketching", 8, seed=seed)[0]
        mid.add((q.metadata or {}).get("form_id"))
    assert "parabola_sketch" in mid
    assert "cubic_sketch_checklist" in mid

    high = set()
    for seed in range(30):
        q = _gen("calc_app_diff_curve_sketching", 16, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        high.add(fid)
        assert fid != "parabola_sketch"
        assert "inflection" in (q.answer_latex or "")
        assert (q.metadata or {}).get("generator") == "curve_sketching"
    assert high <= {"cubic_sketch_checklist", "cubic_shifted_sketch"}
    assert "cubic_shifted_sketch" in high

    expert = set()
    for seed in range(24):
        q = _gen("calc_app_diff_curve_sketching", 22, seed=seed)[0]
        fid = (q.metadata or {}).get("form_id")
        expert.add(fid)
        assert fid == "cubic_shifted_sketch"
        h = (q.metadata or {}).get("h")
        assert h not in (0, None)
        assert r"inflection at }x=0" not in (q.answer_latex or "")
    assert expert == {"cubic_shifted_sketch"}


def test_curve_sketch_quality_weights_tilt():
    from contextlib import nullcontext
    import random as _random

    from question_engine.frameworks.primitives.calc_app_diff import (
        sample_curve_sketching,
    )
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        live_quality_form_weights,
    )

    def _counts(weights):
        c = Counter()
        ctx = live_quality_form_weights(weights) if weights else nullcontext()
        with ctx:
            for i in range(240):
                item = sample_curve_sketching(_random.Random(i), {"difficulty": 8.0})
                c[item.form_id] += 1
        return c

    baseline = _counts(None)
    tilted = _counts({"parabola_sketch": -2.5, "cubic_sketch_checklist": 2.5})
    assert tilted["cubic_sketch_checklist"] > baseline["cubic_sketch_checklist"]


def test_graphical_sign_of_fp():
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

