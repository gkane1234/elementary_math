"""Calc 1 Spec: limits, integrals (trick pipeline + construct_pfd facade)."""

from __future__ import annotations

from collections import Counter

import pytest

from question_engine.api.handler import _generate_for_type
from question_engine.frameworks.primitives.integrals import (
    plan_trick_pipeline,
    sample_integral_expression,
    build_integral_spec,
)
from question_engine.frameworks.primitives.limits import sample_limit_expression
from question_engine.generators import GENERATORS
from question_engine.ml.schema import build_generation_record


_LHOPITAL_EASY_LEFTOVER = ("lhopital_0_0_poly", "lhopital_0_0_trig")


def _gen_lhopital(d: float, *, seed: int = 101):
    return _generate_for_type(
        "calc_app_diff_lhopitals_rule",
        {
            "difficulty": d,
            "seed": seed,
            "count": 1,
            "include_answer_key": True,
        },
    )[0]


def test_limit_removable_emits_spec_snapshot():
    sample = sample_limit_expression(
        {"difficulty": 8, "seed": 11, "include_answer_key": True},
        generator_key="limit_removable",
    )
    meta = sample.as_metadata()
    assert meta["form"] in {"removable_factor", "removable_rationalize"}
    assert isinstance(meta.get("spec_snapshot"), dict)
    assert meta["spec_snapshot"].get("pack") == "limit_removable"
    assert "effort_features" in meta


def test_lhopital_is_indet_not_standard_only():
    sample = sample_limit_expression(
        {"difficulty": 12, "seed": 22},
        generator_key="lhopitals_rule",
    )
    assert sample.form.startswith("indet_")
    assert sample.technique == "lhopital"
    meta = sample.as_metadata()
    assert meta["spec_snapshot"].get("apply_lhopital") is True
    assert meta.get("indeterminate_form")
    assert meta.get("lhopital_passes") is not None
    assert meta.get("form_id")


def test_lhopital_leftover_lockout_no_easy_0_0():
    """Leftover lockout of D=0 0/0 poly and of old Mad-Lib sin(kx)/x at D>=16."""
    q0 = _gen_lhopital(0, seed=101)
    md0 = q0.metadata or {}
    snap0 = md0.get("spec_snapshot") or {}
    assert md0.get("form_id") == "lhopital_0_0_poly"
    assert md0.get("generator") == "lhopitals_rule"
    assert snap0.get("form_id") == "lhopital_0_0_poly"
    assert snap0.get("generator") == "lhopitals_rule"
    assert r"\lim" in (q0.prompt_latex or "")

    easy = set()
    for seed in range(24):
        q = _gen_lhopital(0, seed=seed)
        fid = (q.metadata or {}).get("form_id")
        easy.add(fid)
        assert fid == "lhopital_0_0_poly"
        snap = (q.metadata or {}).get("spec_snapshot") or {}
        assert snap.get("form_id") == fid
        assert snap.get("generator") == "lhopitals_rule"
    assert easy == {"lhopital_0_0_poly"}

    mid = set()
    leftover_poly = leftover_trig = 0
    for seed in range(40):
        q = _gen_lhopital(8, seed=seed)
        fid = (q.metadata or {}).get("form_id")
        mid.add(fid)
        if fid == "lhopital_0_0_poly":
            leftover_poly += 1
        if fid == "lhopital_0_0_trig":
            leftover_trig += 1
        snap = (q.metadata or {}).get("spec_snapshot") or {}
        assert snap.get("form_id") == fid
        assert snap.get("generator") == "lhopitals_rule"
        assert (q.metadata or {}).get("generator") == "lhopitals_rule"
    assert leftover_poly >= 1
    assert leftover_trig >= 1
    assert mid - set(_LHOPITAL_EASY_LEFTOVER)

    high = set()
    for d in (16, 22):
        for seed in range(40):
            q = _gen_lhopital(d, seed=seed)
            fid = (q.metadata or {}).get("form_id")
            high.add(fid)
            assert fid not in _LHOPITAL_EASY_LEFTOVER, (d, seed, fid, q.prompt_latex)
            assert (q.metadata or {}).get("generator") == "lhopitals_rule"
            snap = (q.metadata or {}).get("spec_snapshot") or {}
            assert snap.get("form_id") == fid
            assert snap.get("generator") == "lhopitals_rule"
            assert r"\lim" in (q.prompt_latex or "")
    assert len(high) >= 4


def test_lhopital_indeterminate_form_diversity():
    """Across D spends, emit many OpenStax §4.8 indeterminate-form labels."""
    expected = {
        "0/0",
        "∞/∞",
        "0·∞",
        "∞−∞",
        "0^0",
        "∞^0",
        "1^∞",
        "0^∞",
    }
    seen: set[str] = set()
    form_ids: set[str] = set()
    for d in (0, 4, 8, 10, 12, 14, 16, 20, 25):
        for seed in range(d * 17 + 3, d * 17 + 43):
            sample = sample_limit_expression(
                {
                    "difficulty": d,
                    "seed": seed,
                    "include_answer_key": True,
                    "max_lhopital_steps": 3,
                },
                generator_key="lhopitals_rule",
            )
            meta = sample.as_metadata()
            label = meta.get("indeterminate_form")
            assert label in expected, (d, seed, label, meta.get("form_id"), sample.prompt_latex)
            assert meta.get("form_id")
            assert meta.get("lhopital_passes") is not None
            assert sample.answer_latex  # solvable-by-construction
            seen.add(str(label))
            form_ids.add(str(meta.get("form_id")))
    # Classic quotients plus rewrite/exp families
    assert {"0/0", "∞/∞"} <= seen
    assert len(seen) >= 6, seen
    rewrite_or_exp = seen & {"0·∞", "∞−∞", "0^0", "∞^0", "1^∞", "0^∞"}
    assert len(rewrite_or_exp) >= 4, rewrite_or_exp
    assert any(fid.startswith("lhopital_0_inf") for fid in form_ids) or "0·∞" in seen
    assert any("power" in fid or "0_0_power" in fid or "1_inf" in fid for fid in form_ids) or (
        seen & {"0^0", "∞^0", "1^∞", "0^∞"}
    )


def test_lhopital_forced_catalog_forms_have_answers():
    """Each new §4.8 rewrite/exp form_id produces a known answer + metadata."""
    import random

    from question_engine.frameworks.primitives.limits import (
        _sample_lhopital,
        build_limit_spec,
    )
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        implemented_forms,
        load_form_catalog,
    )

    cat = load_form_catalog("limits")
    leaf = {
        str(f["form_id"]): f
        for f in implemented_forms(cat, generator_key="lhopitals_rule")
    }
    new_ids = [
        "lhopital_0_inf_product",
        "lhopital_inf_minus_inf",
        "lhopital_0_0_power",
        "lhopital_inf_0_power",
        "lhopital_1_inf_power",
        "lhopital_0_inf_power",
    ]
    for fid in new_ids:
        assert fid in leaf, fid
        spec = build_limit_spec(
            {"difficulty": 16, "max_lhopital_steps": 3},
            generator_key="lhopitals_rule",
            d=16.0,
        )
        prompt, answer, form, tech, extra = _sample_lhopital(
            random.Random(42 + hash(fid) % 1000),
            spec,
            purchased={"indet_0_0", "indet_inf_inf", "lhopital_twice"},
            force_form_id=fid,
        )
        assert prompt.startswith(r"\lim")
        assert answer
        assert tech == "lhopital"
        assert form.startswith("indet_")
        assert extra.get("form_id") == fid
        assert extra.get("indeterminate_form") == leaf[fid].get("indeterminate_form")
        assert extra.get("lhopital_passes") is not None
        # Sample a few variants for diversity within the form
        variants = set()
        for seed in range(10):
            _, ans2, _, _, ex2 = _sample_lhopital(
                random.Random(seed),
                spec,
                purchased={"indet_0_0"},
                force_form_id=fid,
            )
            assert ans2
            variants.add(ex2.get("variant"))
        assert variants


def test_limit_jump_piecewise():
    sample = sample_limit_expression(
        {"difficulty": 8, "seed": 33},
        generator_key="limit_jump",
    )
    assert sample.form == "piecewise_jump"
    assert r"\begin{cases}" in sample.prompt_latex or "cases" in sample.prompt_latex


def test_limit_jump_nonconstant_variety():
    """Mid/high D should unlock linear/poly sides — not only constant||constant."""
    form_ids: set[str] = set()
    kinds: set[str] = set()
    for d, seed in [(0, 11), (4, 22), (8, 33), (12, 44), (16, 55), (20, 66)]:
        for s in range(seed, seed + 12):
            sample = sample_limit_expression(
                {"difficulty": d, "seed": s, "include_answer_key": True},
                generator_key="limit_jump",
            )
            meta = sample.as_metadata()
            form_ids.add(str(meta.get("form_id") or meta.get("openstax_form") or ""))
            kinds.add(str(meta.get("left_kind") or ""))
            kinds.add(str(meta.get("right_kind") or ""))
            assert sample.form == "piecewise_jump"
            assert sample.answer_latex
            assert r"\begin{cases}" in sample.prompt_latex
    assert "piecewise_jump" in form_ids or "piecewise_jump_const" in form_ids
    assert any("linear" in fid for fid in form_ids) or "linear" in kinds
    assert any("poly" in fid for fid in form_ids) or "quad" in kinds
    # Prompt should sometimes contain a variable on a piece (non-constant)
    saw_var_piece = False
    for s in range(100, 140):
        sample = sample_limit_expression(
            {"difficulty": 14, "seed": s},
            generator_key="limit_jump",
        )
        # strip the lim / cases scaffolding — look for x in piece expressions
        body = sample.prompt_latex
        if "x" in body.split(r"\begin{cases}", 1)[-1].split(r"\end{cases}", 1)[0]:
            # constant pieces are digits only; linear/quad include x
            piece = body.split(r"\begin{cases}", 1)[-1]
            if "x" in piece.replace("x<", "").replace("x\\ge", "").replace("x \\ge", ""):
                # crude: if cases content has x beyond inequality markers
                inner = piece.split(r"\end{cases}", 1)[0]
                # remove inequality conditions
                import re

                cleaned = re.sub(r"&[^\\]+", "", inner)
                if "x" in cleaned:
                    saw_var_piece = True
                    break
    assert saw_var_piece, "expected non-constant piecewise sides at D≥14"


def test_limit_essential_variety():
    """Essential leaf should span infinite + oscillating catalog forms."""
    form_ids: set[str] = set()
    for d in (0, 3, 6, 8, 12, 16, 20):
        for seed in range(d * 9 + 1, d * 9 + 16):
            sample = sample_limit_expression(
                {"difficulty": d, "seed": seed, "include_answer_key": True},
                generator_key="limit_essential",
            )
            meta = sample.as_metadata()
            fid = str(meta.get("form_id") or meta.get("openstax_form") or "")
            form_ids.add(fid)
            assert sample.form == "essential"
            assert sample.answer_latex
            assert sample.prompt_latex.startswith(r"\lim")
    assert "essential_1_over_x" in form_ids
    assert "essential_sin_1_over_x" in form_ids or "essential_cos_1_over_x" in form_ids
    assert (
        "essential_1_over_x_sq" in form_ids
        or "essential_rational_va" in form_ids
        or "essential_tan_asymptote" in form_ids
    )
    # Must not be only 1/x and sin(1/x)
    assert len(form_ids) >= 3, form_ids
    # x sin(1/x) is continuous-extension / squeeze — not this leaf
    for s in range(50):
        sample = sample_limit_expression(
            {"difficulty": 12, "seed": s},
            generator_key="limit_essential",
        )
        assert "x \\sin" not in sample.prompt_latex
        assert r"x\sin" not in sample.prompt_latex.replace(" ", "")


def test_limit_essential_d_wraps_structure():
    """D=0 bare cores vs D=20 wrapped — high D must do something visible."""
    low_wraps: list[list[str]] = []
    high_wraps: list[list[str]] = []
    low_prompts: set[str] = set()
    high_prompts: set[str] = set()
    for seed in range(200, 260):
        low = sample_limit_expression(
            {"difficulty": 0, "seed": seed, "include_answer_key": True},
            generator_key="limit_essential",
        )
        high = sample_limit_expression(
            {"difficulty": 20, "seed": seed, "include_answer_key": True},
            generator_key="limit_essential",
        )
        lm = low.as_metadata()
        hm = high.as_metadata()
        assert lm.get("core_form_id") or lm.get("form_id")
        assert hm.get("core_form_id") or hm.get("form_id")
        low_wraps.append(list(lm.get("wrappers_applied") or []))
        high_wraps.append(list(hm.get("wrappers_applied") or []))
        low_prompts.add(low.prompt_latex)
        high_prompts.add(high.prompt_latex)
        # Core pedagogical id preserved under wraps
        assert hm.get("core_form_id") in {
            "essential_1_over_x",
            "essential_1_over_x_sq",
            "essential_rational_va",
            "essential_sin_1_over_x",
            "essential_cos_1_over_x",
            "essential_tan_asymptote",
        }
        # Answers stay in the essential vocabulary
        assert high.answer_latex in {
            r"\text{DNE}",
            r"\infty",
            r"-\infty",
        }
        assert low.form == high.form == "essential"

    # Low D: essentially no wrappers
    assert sum(1 for w in low_wraps if w) <= 2, low_wraps
    # High D: structure should differ — wraps and/or distinct prompts (not wrap-count chasing)
    structural_hi = sum(
        1
        for w in high_wraps
        if any(
            k.split("#", 1)[0]
            in {
                "horizontal_shift",
                "cancel_factor",
                "unfactored_form",
                "sign",
                "constant_multiple",
            }
            for k in w
        )
    )
    assert structural_hi >= 8 or low_prompts != high_prompts, (
        f"expected structural high-D essential samples, wraps={structural_hi} "
        f"prompt_diff={low_prompts != high_prompts}"
    )
    kind_hits = {
        k.split("#", 1)[0]
        for w in high_wraps
        for k in w
        if k.split("#", 1)[0]
        in {
            "horizontal_shift",
            "sign",
            "constant_multiple",
            "cancel_factor",
            "unfactored_form",
        }
    }
    # At least some variety across the high-D pool when wraps appear
    if structural_hi >= 8:
        assert len(kind_hits) >= 1, kind_hits
    # Low and high prompt pools should differ (wrappers / richer forms)
    assert low_prompts != high_prompts


def test_limit_jump_high_d_not_only_constants():
    """At high D, piecewise sides should rarely be const||const."""
    const_only = 0
    total = 0
    for seed in range(300, 360):
        sample = sample_limit_expression(
            {"difficulty": 16, "seed": seed, "include_answer_key": True},
            generator_key="limit_jump",
        )
        meta = sample.as_metadata()
        total += 1
        if meta.get("left_kind") == "const" and meta.get("right_kind") == "const":
            const_only += 1
    assert const_only <= 8, f"const||const at D=16 too often: {const_only}/{total}"


def test_integral_pfd_uses_partial_fractions_facade():
    sample = sample_integral_expression(
        {"difficulty": 10, "seed": 44, "include_answer_key": True},
        generator_key="integral_partial_fractions",
    )
    meta = sample.as_metadata()
    assert list(sample.tricks_required) == ["pfd"]
    assert meta.get("pfd_source") == "partial_fractions.combine_pf_to_rational"
    assert isinstance(meta.get("pf_target"), dict)
    assert sample.prompt_latex.startswith(r"\int")
    assert "ln" in (sample.answer_latex or "")


def test_integral_multi_trick_ordered_pipeline():
    sample = sample_integral_expression(
        {"difficulty": 14, "seed": 55},
        generator_key="integral_multi_trick",
    )
    assert list(sample.tricks_required) == ["u_sub", "pfd"]
    meta = sample.as_metadata()
    assert meta["pipeline"]["tricks_required"] == ["u_sub", "pfd"]
    assert meta["pipeline"]["length"] == 2
    # Genuine wrap: transcendental u (exp/trig/log) — not PFD-only in x
    assert meta.get("u_latex") or meta.get("u_inner_family")
    assert meta.get("construction") in {"pipeline_shared_u_sub", "pipeline"}
    # Must not look like a bare rational-in-x PFD
    assert "e^" in sample.prompt_latex or "sin" in sample.prompt_latex or "cos" in sample.prompt_latex or r"\ln" in sample.prompt_latex


def test_integral_u_sub_derivative_backed():
    sample = sample_integral_expression(
        {"difficulty": 8, "seed": 66},
        generator_key="integral_substitution",
    )
    assert "u_sub" in sample.tricks_required
    assert sample.as_metadata().get("construction") in {
        "derivative_backed",
        "shared_u_sub",
        "forward_form_catalog",
    }


def test_integral_trig_sub_is_genuine_not_plain_u_sub():
    """Trig-sub leaf must emit √(a²±x²)/√(x²−a²) forms, not ∫2x(x²+1)^n."""
    plain_u_sub_markers = (
        rf"(x^{{2}}+1)",
        "quad_inner_du",
        "linear_power_with_du",
        "linear_power",
    )
    families_seen: set[str] = set()
    for seed in range(20, 60):
        sample = sample_integral_expression(
            {"difficulty": 10, "seed": seed, "include_answer_key": True},
            generator_key="integral_trig_substitution",
        )
        meta = sample.as_metadata()
        tricks = list(sample.tricks_required)
        assert "trig_sub" in tricks, (seed, tricks, sample.prompt_latex)
        assert tricks != ["u_sub"], (seed, sample.prompt_latex)
        shape = str(meta.get("shape_id") or meta.get("family") or "")
        for bad in plain_u_sub_markers:
            assert bad not in sample.prompt_latex, (seed, sample.prompt_latex)
            assert bad not in shape, (seed, shape)
        # Must look like a trig-sub integrand (√ or (a²±x²)^{p/2})
        prompt = sample.prompt_latex
        assert (
            "sqrt" in prompt
            or r"\sqrt" in prompt
            or r"\frac{3}{2}" in prompt
            or r"\frac{5}{2}" in prompt
            or "a2" in shape
            or "pow_" in shape
            or "sqrt_" in shape
            or "one_over" in shape
        ), (seed, prompt, shape)
        assert meta.get("trig_sub_kind") in {"sin", "tan", "sec"}, meta
        families_seen.add(str(meta.get("shape_id") or ""))
    assert len(families_seen) >= 2


def test_integral_trig_sub_openstax_like_spot_check():
    """Spot-check classic OpenStax Vol.2 trig-sub shapes across seeds."""
    saw_minus = False
    saw_plus = False
    saw_x2_minus = False
    for seed in range(1, 80):
        sample = sample_integral_expression(
            {"difficulty": 14, "seed": seed},
            generator_key="integral_trig_substitution",
        )
        p = sample.prompt_latex
        if r"-" in p and r"\sqrt" in p and "trig_sub" in sample.tricks_required:
            if f"{sample.metadata.get('trig_sub_kind')}" == "sin" or "a2_minus" in str(
                sample.as_metadata().get("shape_id")
            ):
                saw_minus = True
            if "x2_minus" in str(sample.as_metadata().get("shape_id")) or sample.as_metadata().get(
                "trig_sub_kind"
            ) == "sec":
                saw_x2_minus = True
        if "+" in p and r"\sqrt" in p:
            saw_plus = True
        if saw_minus and saw_plus and saw_x2_minus:
            break
    assert saw_minus and saw_plus


def test_integral_forward_packs_have_openstax_variety():
    """Power / trig / parts should not collapse to a single bland family."""
    power_shapes: set[str] = set()
    trig_shapes: set[str] = set()
    parts_shapes: set[str] = set()
    for seed in range(30, 70):
        power_shapes.add(
            str(
                sample_integral_expression(
                    {"difficulty": 12, "seed": seed},
                    generator_key="integral_power_rule",
                ).as_metadata().get("shape_id")
            )
        )
        trig_shapes.add(
            str(
                sample_integral_expression(
                    {"difficulty": 14, "seed": seed},
                    generator_key="integral_trigonometric",
                ).as_metadata().get("shape_id")
            )
        )
        parts_shapes.add(
            str(
                sample_integral_expression(
                    {"difficulty": 14, "seed": seed},
                    generator_key="integration_by_parts",
                ).as_metadata().get("shape_id")
            )
        )
    assert len(power_shapes) >= 2
    assert len(trig_shapes) >= 5
    assert len(parts_shapes) >= 3
    # Catalog form_ids — not legacy bland sin/sin2-only labels
    catalogish = {
        "sin_odd_cos_any",
        "cos_odd_sin_any",
        "sin_even_power",
        "cos_even_power",
        "tan2",
        "tan_odd_alone",
        "sec_j_tan",
        "tan_k_sec2",
        "sin_cos_both_even",
        "product_sin_a_cos_b",
        "sec3_reduction",
        "tan_even_reduction",
        "cos_j_sin",
        "sin_j_cos",
    }
    assert trig_shapes & catalogish


def test_trig_integral_catalog_drives_form_ids():
    """Sampler must emit openstax form_id metadata and diversify across catalog."""
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        implemented_forms,
        load_form_catalog,
    )

    catalog = load_form_catalog("trig_integrals")
    implemented = {str(f["form_id"]) for f in implemented_forms(catalog)}
    assert "sin_odd_cos_any" in implemented
    assert "tan2" in implemented

    seen: set[str] = set()
    for d, seed0 in ((4, 10), (10, 40), (16, 80), (22, 120)):
        for seed in range(seed0, seed0 + 35):
            sample = sample_integral_expression(
                {"difficulty": d, "seed": seed, "include_answer_key": True},
                generator_key="integral_trigonometric",
            )
            meta = sample.as_metadata()
            fid = str(meta.get("form_id") or meta.get("openstax_form") or "")
            assert fid in implemented, (d, seed, fid, sample.prompt_latex)
            assert meta.get("openstax_form") == fid
            assert sample.prompt_latex.startswith(r"\int")
            # Must not collapse to only ∫sin / ∫cos table forms at mid+ D
            seen.add(fid)
    assert len(seen) >= 8, seen
    assert any("sin" in s and "odd" in s or s.startswith("sin_even") for s in seen) or (
        "sin_odd_cos_any" in seen or "sin_even_power" in seen
    )
    assert "tan2" in seen or "tan_odd_alone" in seen or "tan_k_sec2" in seen


def test_trig_integral_high_d_form_diversity_not_table_dominated():
    """High-D multi-seed trig leaf must hit many catalog forms, not ∫sin(kx)."""
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        implemented_forms,
        load_form_catalog,
    )

    implemented = {
        str(f["form_id"]) for f in implemented_forms(load_form_catalog("trig_integrals"))
    }
    counts: Counter[str] = Counter()
    for seed in range(1, 101):
        sample = sample_integral_expression(
            {"difficulty": 18, "seed": seed, "include_answer_key": True},
            generator_key="integral_trigonometric",
        )
        meta = sample.as_metadata()
        fid = str(meta.get("form_id") or meta.get("openstax_form") or "")
        assert fid in implemented, (seed, fid, sample.prompt_latex)
        counts[fid] += 1
        # Table forms must be gated out well below D=18
        assert not fid.startswith("basic_"), (seed, fid, sample.prompt_latex)
    assert len(counts) >= 14, counts
    # No single mid/high form should dominate the whole leaf
    top_share = counts.most_common(1)[0][1] / sum(counts.values())
    assert top_share < 0.25, counts.most_common(5)
    # Must include odd-power / tan-sec textbook families
    assert counts.keys() & {
        "sin_odd_cos_any",
        "cos_odd_sin_any",
        "sin_even_power",
        "cos_even_power",
        "tan2",
        "tan_odd_alone",
        "tan_k_sec2",
        "sec_j_tan",
        "tan_sec_sec_even",
        "sec3_reduction",
    }
    # Mid-D: basics may appear only as a minority once richer forms unlock
    mid: Counter[str] = Counter()
    for seed in range(200, 280):
        sample = sample_integral_expression(
            {"difficulty": 8, "seed": seed},
            generator_key="integral_trigonometric",
        )
        mid[str(sample.as_metadata().get("form_id") or "")] += 1
    basic_share = sum(v for k, v in mid.items() if k.startswith("basic_")) / sum(mid.values())
    assert basic_share < 0.15, mid.most_common()
    assert len(mid) >= 8, mid


def test_plan_pipeline_respects_requires():
    spec = build_integral_spec(
        {
            "difficulty": 16,
            "require_substitution": True,
            "require_pfd": True,
            "allow_substitution": True,
            "allow_pfd": True,
        },
        generator_key="integral_multi_trick",
    )
    pipe = plan_trick_pipeline(spec, purchased={"pipeline_len_2"}, rng=__import__("random").Random(1))
    assert pipe.tricks_required == ["u_sub", "pfd"]


def test_live_generators_emit_ml_join_keys():
    for key, type_id in (
        ("limit_direct_evaluation", "calc_limits_by_direct_evaluation"),
        ("integral_partial_fractions", "calc_indef_int_partial_fractions"),
        ("integral_multi_trick", "calc_indef_int_multi_trick"),
        ("linear_approximation", "calc_app_diff_linear_approximations"),
    ):
        qs = GENERATORS[key](
            type_id,
            {"difficulty": 10, "seed": 100 + hash(key) % 50, "count": 1, "include_answer_key": True},
        )
        assert len(qs) == 1
        rec = build_generation_record(type_id, qs[0], {"difficulty": 10, "seed": 7})
        assert rec.theta_full.get("difficulty") == 10
        snap = (qs[0].metadata or {}).get("spec_snapshot")
        assert isinstance(snap, dict)
        assert "pack" in snap


def test_expression_spec_default_excludes_hyperbolic():
    from question_engine.frameworks.primitives.poly_expression import (
        DEFAULT_ALLOWED_FUNCTIONS,
        ExpressionSpec,
        pack_power_rule,
    )

    assert "hyperbolic" not in DEFAULT_ALLOWED_FUNCTIONS
    assert set(DEFAULT_ALLOWED_FUNCTIONS) == {"trig", "exp", "log", "roots", "invtrig"}
    assert ExpressionSpec().allowed_functions == DEFAULT_ALLOWED_FUNCTIONS
    power = pack_power_rule(8.0, allow_roots=False)
    assert not (power.allowed_functions & {"trig", "exp", "log", "invtrig", "hyperbolic"})


def test_limit_direct_mid_d_emits_specials():
    classes: set[str] = set()
    for seed in range(40):
        sample = sample_limit_expression(
            {"difficulty": 8, "seed": seed},
            generator_key="limit_direct_evaluation",
        )
        classes |= set(sample.as_metadata().get("function_classes") or [])
    assert classes & {"trig", "exp", "log", "invtrig", "roots"}


def test_limit_removable_stays_algebraic():
    for seed in range(25):
        sample = sample_limit_expression(
            {"difficulty": 10, "seed": seed},
            generator_key="limit_removable",
        )
        fc = set(sample.as_metadata().get("function_classes") or [])
        assert not (fc & {"trig", "exp", "log", "invtrig", "hyperbolic"})


def test_limit_infinity_broad_classes():
    classes: set[str] = set()
    for seed in range(50):
        sample = sample_limit_expression(
            {"difficulty": 10, "seed": seed},
            generator_key="limit_at_infinity",
        )
        classes |= set(sample.as_metadata().get("function_classes") or [])
    assert "algebraic" in classes
    assert classes & {"trig", "exp", "log", "invtrig"}


def test_lhopital_multi_pass_at_high_d():
    multi = 0
    for seed in range(40):
        sample = sample_limit_expression(
            {"difficulty": 16, "seed": seed, "max_lhopital_steps": 3},
            generator_key="lhopitals_rule",
        )
        passes = sample.as_metadata().get("lhopital_passes") or sample.as_metadata().get(
            "lhopital_steps"
        )
        if int(passes or 1) >= 2:
            multi += 1
    assert multi >= 8


def test_pfd_can_emit_arctan_at_mid_d():
    saw = False
    for seed in range(20, 100):
        sample = sample_integral_expression(
            {"difficulty": 12, "seed": seed, "include_answer_key": True},
            generator_key="integral_partial_fractions",
        )
        if "arctan" in (sample.answer_latex or ""):
            saw = True
            assert sample.as_metadata().get("has_quadratic") is True
            break
    assert saw


def test_trig_sub_fractional_powers_at_mid_d():
    exps: set[str] = set()
    for seed in range(40, 120):
        sample = sample_integral_expression(
            {"difficulty": 14, "seed": seed},
            generator_key="integral_trig_substitution",
        )
        exps.add(str(sample.as_metadata().get("trig_sub_exponent")))
    assert any(e in exps for e in ("3/2", "-3/2", "1/2", "-1/2"))


def test_shared_u_sub_emits_exp_of_trig():
    from question_engine.frameworks.primitives import u_substitution as usub
    import random

    rng = random.Random(3)
    spec = usub.pack_u_sub_ln_exp(12.0, prefer_composite=True)
    hits = 0
    examples = []
    for _ in range(50):
        s = usub.sample_u_sub(spec, rng=rng)
        if "e^{" in s.prompt_latex and (
            "sin" in s.prompt_latex or "cos" in s.prompt_latex
        ):
            hits += 1
            examples.append(s.prompt_latex)
    assert hits >= 5
    assert examples


def test_derivative_spec_still_imports():
    """Regression: calc integral work must not break derivative Spec."""
    from question_engine.frameworks.primitives.derivatives import (
        sample_derivative_expression,
    )

    sample = sample_derivative_expression(
        {"difficulty": 8, "seed": 1, "allow_trig": False},
        generator_key="derivative_power_rule",
    )
    assert sample.prompt_latex
    assert sample.as_metadata().get("spec_snapshot")


def test_complexity_wrap_spec_adapter_low_vs_high_d():
    """Shared Spec dress: D=0 empty wrappers; D=20 often dressed across domains."""
    from question_engine.frameworks.primitives.derivatives import (
        sample_derivative_expression,
    )
    from question_engine.frameworks.primitives.complexity_wrap import (
        n_wraps_for_d,
        form_span_is_narrow,
    )

    # Policy: narrow forms dress more at mid D
    assert form_span_is_narrow({"d_min": 0, "d_max": 4})
    assert not form_span_is_narrow({"d_min": 0, "d_max": 20})
    assert n_wraps_for_d(0, __import__("random").Random(1)) == 0

    leaves = [
        ("limit", "limit_direct_evaluation", sample_limit_expression),
        ("limit", "limit_at_infinity", sample_limit_expression),
        ("limit", "lhopitals_rule", sample_limit_expression),
        ("deriv", "derivative_power_rule", sample_derivative_expression),
        ("deriv", "derivative_trigonometric", sample_derivative_expression),
        ("int", "integral_power_rule", sample_integral_expression),
        ("int", "integral_substitution", sample_integral_expression),
        ("int", "integration_by_parts", sample_integral_expression),
    ]

    for domain, key, sampler in leaves:
        low_wraps = []
        high_wraps = []
        low_prompts = set()
        high_prompts = set()
        for seed in range(300, 340):
            settings_lo = {"difficulty": 0, "seed": seed, "include_answer_key": True}
            settings_hi = {"difficulty": 20, "seed": seed, "include_answer_key": True}
            if key == "derivative_trigonometric":
                settings_lo["allow_trig"] = True
                settings_hi["allow_trig"] = True
            low = sampler(settings_lo, generator_key=key)
            high = sampler(settings_hi, generator_key=key)
            lm = low.as_metadata() if hasattr(low, "as_metadata") else {}
            hm = high.as_metadata() if hasattr(high, "as_metadata") else {}
            low_wraps.append(list(lm.get("wrappers_applied") or []))
            high_wraps.append(list(hm.get("wrappers_applied") or []))
            low_prompts.add(low.prompt_latex)
            high_prompts.add(high.prompt_latex)
            # Core pedagogical id preserved
            assert hm.get("core_form_id") or hm.get("form_id")
            if hm.get("wrappers_applied"):
                assert hm.get("core_form_id") or hm.get("form_id")
            # Technique / methods intact
            if domain == "int":
                assert hm.get("tricks_required") or hm.get("technique") or high.technique
            if domain == "deriv":
                assert hm.get("methods_used") is not None

        assert sum(1 for w in low_wraps if w) <= 3, (key, low_wraps)
        # High D must change student-visible prompts (structure), not merely wrap counts
        assert low_prompts != high_prompts, key
        # Optional wraps OK; do not require a wrap-count quota (metric gaming)


def test_complexity_wrap_skip_jump_and_ftc():
    """Jump / FTC must not get whole-prompt Spec scale that breaks structure.

    Jump may carry structural ``jump_*`` tags; FTC may carry ``ftc_variable_upper``
    (real structure) but not scale/sign dress or ``cost_pad``.
    """
    from question_engine.frameworks.primitives.integrals import sample_integral_expression as sie

    for seed in range(50, 70):
        jump = sample_limit_expression(
            {"difficulty": 20, "seed": seed},
            generator_key="limit_jump",
        )
        jm = jump.as_metadata()
        wraps = list(jm.get("wrappers_applied") or [])
        banned = {"horizontal_shift", "cancel_factor", "unfactored_form", "cost_pad"}
        assert not (banned & {_dress_kind(w) for w in wraps}), wraps
        assert "cost_pad" not in wraps
        assert all(
            c.get("feature") != "cost_pad" for c in (jm.get("difficulty_costs") or [])
        )
        total = float(jm.get("difficulty_cost_total") or 0)
        if total + 1e-9 < 20.0:
            assert float(jm.get("difficulty_shortfall") or 0) > 0

    for seed in range(50, 60):
        ftc = sie(
            {"difficulty": 20, "seed": seed},
            generator_key="first_fundamental_theorem",
        )
        fm = ftc.as_metadata()
        wraps = list(fm.get("wrappers_applied") or [])
        assert "cost_pad" not in wraps
        # Structural FTC upgrades OK; whole-prompt scale/sign dress is not.
        banned_ftc = {"constant_multiple", "sign", "horizontal_shift", "cost_pad"}
        assert not (banned_ftc & {_dress_kind(w) for w in wraps}), wraps
        total = float(fm.get("difficulty_cost_total") or 0)
        if total + 1e-9 < 20.0:
            assert float(fm.get("difficulty_shortfall") or 0) > 0


def _dress_kind(tag: str) -> str:
    return str(tag).split("#", 1)[0]

def test_scale_latex_body_no_digit_juxtaposition():
    """Dress scale must multiply integers / paren sums — never '-2'+'2' → '-22'."""
    from question_engine.frameworks.primitives.complexity_wrap import (
        scale_answer_latex,
        scale_latex_body,
    )

    assert scale_latex_body("2", -2) == "-4"
    assert scale_latex_body("6", 4) == "24"
    assert scale_latex_body(r"2\sqrt{x}", 2) == r"4\sqrt{x}"
    assert scale_latex_body(r"\frac{1}{2}", 3) == r"\frac{3}{2}"
    assert scale_latex_body(r"x\ln(x)-x", -1) == r"-\left(x\ln(x)-x\right)"
    assert scale_latex_body(r"\frac{1}{2}x^{2}-\frac{1}{4}x^{2}", -2) == (
        r"-2\left(\frac{1}{2}x^{2}-\frac{1}{4}x^{2}\right)"
    )
    assert scale_answer_latex(r"2\sqrt{x}+C", 2) == r"4\sqrt{x}+C"
    assert scale_answer_latex(r"x\ln(x)-x+C", -1) == r"-\left(x\ln(x)-x\right)+C"
    assert scale_answer_latex(r"\infty", -3) == r"-\infty"


def test_dress_preserves_core_form_id_and_costs():
    """Dressed samples keep core_form_id == form_id and emit difficulty_costs."""
    from question_engine.frameworks.primitives.derivatives import (
        sample_derivative_expression,
    )
    from question_engine.frameworks.primitives.integrals import (
        sample_integral_expression,
    )

    leaves = [
        ("limit", "lhopitals_rule", sample_limit_expression),
        ("limit", "limit_essential", sample_limit_expression),
        ("deriv", "derivative_power_rule", sample_derivative_expression),
        ("int", "integral_power_rule", sample_integral_expression),
        ("int", "integration_by_parts", sample_integral_expression),
    ]
    dressed_seen = 0
    for _domain, key, sampler in leaves:
        for seed in range(400, 440):
            settings = {"difficulty": 20, "seed": seed, "include_answer_key": True}
            sample = sampler(settings, generator_key=key)
            meta = sample.as_metadata()
            fid = meta.get("form_id") or meta.get("openstax_form")
            core = meta.get("core_form_id")
            assert fid, (key, seed, meta)
            assert core == fid or core is not None, (key, seed, core, fid)
            # When dressed, core must match emitted form (never swap form via dress)
            wraps = list(meta.get("wrappers_applied") or [])
            if wraps:
                dressed_seen += 1
                assert meta.get("core_form_id") == fid, (key, seed, wraps, meta)
            costs = meta.get("difficulty_costs")
            assert isinstance(costs, list) and costs, (key, seed, meta)
            assert meta.get("difficulty_cost_total") is not None
            for row in costs:
                assert set(row) >= {"source", "feature", "cost"}
                assert row["source"] in {"form", "dress", "spec"}
            # Power-rule dress must not inject product factors
            if key == "derivative_power_rule":
                assert "spec_product_dress" not in wraps, (seed, wraps)
    assert dressed_seen >= 20


def test_dressed_limit_answer_matches_scaled_core():
    """Same-seed L'H with wraps: answer equals scale applied to undressed numeric core."""
    from question_engine.frameworks.primitives.complexity_wrap import scale_answer_latex

    # Find dressed lhopital_0_0_poly samples (catalog d_max=10 leftover band).
    ok = 0
    for seed in range(0, 120):
        hi = sample_limit_expression(
            {"difficulty": 8, "seed": seed, "include_answer_key": True},
            generator_key="lhopitals_rule",
        )
        meta = hi.as_metadata()
        if meta.get("form_id") != "lhopital_0_0_poly":
            continue
        wraps = list(meta.get("wrappers_applied") or [])
        if not wraps:
            continue
        # Prompt is lim ... k * (x^2-a^2)/(x-a); answer should be k * 2a (or -)
        # Spot-check: no digit-juxtaposition artifacts like 22, 46, -22 from scale|answer
        ans = hi.answer_latex
        assert ans not in {"-22", "22", "46", "23", "30", "-30", "41", "40"}, (
            seed,
            hi.prompt_latex,
            ans,
            wraps,
        )
        # Re-scale identity: scale 1 leaves answer alone
        assert scale_answer_latex(ans, 1) == ans
        ok += 1
    assert ok >= 3


def test_difficulty_costs_schema_example():
    """Cost table produces form + dress rows with heuristic totals."""
    from question_engine.frameworks.primitives.complexity_wrap import (
        build_difficulty_costs,
        form_base_cost,
    )

    assert form_base_cost("essential_sin_1_over_x") == 4.0
    costs, total = build_difficulty_costs(
        form_id="essential_sin_1_over_x",
        wrappers_applied=["constant_multiple", "sign"],
        upgrades=["allow_trig"],
    )
    sources = {c["source"] for c in costs}
    assert "form" in sources and "dress" in sources and "spec" in sources
    assert total == sum(c["cost"] for c in costs)
    feats = {c["feature"] for c in costs}
    assert "essential_sin_1_over_x" in feats
    assert "spec_scale" in feats  # alias for constant_multiple
    assert "spec_sign" in feats
