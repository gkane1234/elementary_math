"""OpenStax form-catalog selection / diversity for Calc 1 algebraic leaves."""

from __future__ import annotations

from collections import Counter

from question_engine.frameworks.primitives.derivatives import sample_derivative_expression
from question_engine.frameworks.primitives.integrals import sample_integral_expression
from question_engine.frameworks.primitives.limits import sample_limit_expression
from question_engine.frameworks.primitives.openstax_form_catalogs import (
    catalog_gaps,
    implemented_forms,
    load_form_catalog,
    select_form_id,
)


def _form_id(meta: dict) -> str:
    return str(meta.get("form_id") or meta.get("openstax_form") or "")


def test_calc1_catalogs_load_and_have_implemented_forms():
    expected = {
        "trig_integrals": 20,
        "u_substitution": 10,
        "integration_by_parts": 8,
        "trig_substitution": 10,
        "partial_fractions": 6,
        "basic_power_integrals": 5,
        "invtrig_integrals": 5,
        "limits": 20,
        "derivatives": 18,
    }
    for name, min_n in expected.items():
        cat = load_form_catalog(name)
        imp = implemented_forms(cat)
        assert len(imp) >= min_n, (name, len(imp), [f["form_id"] for f in imp])
        assert cat.get("catalog_id") == name or cat.get("catalog_id")


def test_trig_gaps_sec5_and_sin_sin_implemented():
    cat = load_form_catalog("trig_integrals")
    imp = {str(f["form_id"]) for f in implemented_forms(cat)}
    assert "sec_odd_reduction_n5" in imp
    assert "product_sin_a_sin_b" in imp
    assert "sin_cos_both_odd" in imp
    assert "one_over_one_plus_cos" in imp
    assert "csc_j_cot" in imp
    gaps = {str(f["form_id"]) for f in catalog_gaps(cat)}
    assert "weierstrass_t_sub" in gaps
    assert "csc5_reduction" in gaps
    assert "tan4_sec3" in gaps


def test_trig_bank_closed_forms_live():
    """BC bank §3 closed forms unlock at mid D; D=0 stays table."""
    bank = {
        "sin_cos_both_odd",
        "csc_j_cot",
        "sin_over_one_plus_cos2",
        "one_over_one_plus_cos",
        "one_over_one_plus_sin",
    }
    for seed in range(20):
        sample = sample_integral_expression(
            {"difficulty": 0, "seed": seed, "include_answer_key": True},
            generator_key="integral_trigonometric",
        )
        fid = _form_id(sample.as_metadata())
        assert fid not in bank, (seed, fid, sample.prompt_latex)
        assert fid.startswith("basic_") or fid in {"basic_tan"}
    hits = set()
    for seed in range(80):
        sample = sample_integral_expression(
            {"difficulty": 16, "seed": seed, "include_answer_key": True},
            generator_key="integral_trigonometric",
        )
        fid = _form_id(sample.as_metadata())
        if fid in bank:
            hits.add(fid)
            assert "+C" in (sample.answer_latex or "")
    assert hits, "expected at least one BC-bank trig form at D=16"


def test_select_form_id_respects_d_min():
    cat = load_form_catalog("trig_integrals")
    forms = implemented_forms(cat)
    rng = __import__("random").Random(0)
    low = {select_form_id(forms, d=2.0, rng=rng)["form_id"] for _ in range(40)}
    assert "sec3_reduction" not in low
    assert any(str(f).startswith("basic_") for f in low)


def test_select_form_id_quality_weights_shift_probability():
    from collections import Counter

    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        live_quality_form_weights,
    )

    forms = [
        {"form_id": "a", "d_min": 0, "d_weight": 1.0},
        {"form_id": "b", "d_min": 0, "d_weight": 1.0},
    ]
    rng = __import__("random").Random(0)
    baseline = Counter(select_form_id(forms, d=8.0, rng=rng)["form_id"] for _ in range(240))
    rng = __import__("random").Random(0)
    tilted = Counter(
        select_form_id(
            forms, d=8.0, rng=rng, quality_weights={"a": 2.0, "b": -2.0}
        )["form_id"]
        for _ in range(240)
    )
    assert tilted["a"] > baseline["a"]
    assert tilted["a"] > tilted["b"]
    rng = __import__("random").Random(1)
    with live_quality_form_weights({"a": -2.0, "b": 2.0}):
        ctx = Counter(select_form_id(forms, d=8.0, rng=rng)["form_id"] for _ in range(240))
    assert ctx["b"] > ctx["a"]


def test_parts_catalog_diversity():
    cat = load_form_catalog("integration_by_parts")
    implemented = {str(f["form_id"]) for f in implemented_forms(cat)}
    seen: set[str] = set()
    for d, seed0 in ((4, 1), (12, 50), (18, 100)):
        for seed in range(seed0, seed0 + 25):
            sample = sample_integral_expression(
                {"difficulty": d, "seed": seed, "include_answer_key": True},
                generator_key="integration_by_parts",
            )
            fid = _form_id(sample.as_metadata())
            assert fid in implemented, (d, seed, fid)
            seen.add(fid)
    assert len(seen) >= 5, seen


def test_parts_d0_one_step_k1():
    """D=0: one parts step, coefficient 1 — rotate ln / xe^x / x sin / x cos."""
    allowed = {"ln_alone", "poly1_exp", "poly1_sin", "poly1_cos"}
    seen: set[str] = set()
    for seed in range(40):
        sample = sample_integral_expression(
            {"difficulty": 0, "seed": seed, "include_answer_key": True},
            generator_key="integration_by_parts",
        )
        fid = _form_id(sample.as_metadata())
        assert fid in allowed, (seed, fid, sample.prompt_latex)
        prompt = sample.prompt_latex or ""
        assert r"\int" in prompt
        assert "+C" in (sample.answer_latex or "")
        assert "e^{2" not in prompt
        assert r"\sin(2" not in prompt
        assert r"\cos(2" not in prompt
        assert r"x^{2}" not in prompt
        seen.add(fid)
    assert len(seen) >= 3, seen


def test_parts_high_d_not_ln_alone():
    """ln_alone has d_max=8; D=16/22 must be tabular / cyclic / arctan / poly1_ln."""
    easy = {"ln_alone"}
    seen: set[str] = set()
    for seed in range(30):
        sample = sample_integral_expression(
            {"difficulty": 22, "seed": seed, "include_answer_key": True},
            generator_key="integration_by_parts",
        )
        fid = _form_id(sample.as_metadata())
        assert fid not in easy, (seed, fid, sample.prompt_latex)
        assert "+C" in (sample.answer_latex or "")
        seen.add(fid)
    assert seen & {
        "poly2_exp",
        "poly2_sin",
        "poly2_cos",
        "poly3_exp",
        "cyclic_exp_sin",
        "cyclic_exp_cos",
        "arctan_alone",
        "ln_power_2",
        "ln_power_3",
        "poly1_arctan",
        "poly1_arcsin",
    }, seen


def test_parts_mid_d_scales_inner():
    """D=8 still one-step LIATE but k≥2 or ln(ax) when those forms hit."""
    scaled = 0
    for seed in range(40):
        sample = sample_integral_expression(
            {"difficulty": 8, "seed": seed, "include_answer_key": True},
            generator_key="integration_by_parts",
        )
        prompt = sample.prompt_latex or ""
        fid = _form_id(sample.as_metadata())
        assert fid not in {
            "poly2_exp",
            "poly2_sin",
            "poly2_cos",
            "poly3_exp",
            "poly3_sin",
            "poly3_cos",
            "cyclic_exp_sin",
            "cyclic_exp_cos",
            "arctan_alone",
            "poly1_arctan",
            "poly1_arcsin",
            "arcsin_alone",
            "ln_power_2",
            "ln_power_3",
            "power_frac_ln",
            "ln_quad",
            "poly2_ln",
        }
        if any(
            token in prompt
            for token in ("e^{2", "e^{3", r"\sin(2", r"\sin(3", r"\cos(2", r"\cos(3", r"\ln(2", r"\ln(3")
        ):
            scaled += 1
    assert scaled >= 8, scaled


def test_parts_bc_bank_catalog_and_deferred():
    cat = load_form_catalog("integration_by_parts")
    imp = {str(f["form_id"]) for f in implemented_forms(cat)}
    for fid in (
        "poly3_exp",
        "poly3_sin",
        "poly3_cos",
        "poly2_cos",
        "poly2_ln",
        "ln_power_2",
        "ln_power_3",
        "poly1_arctan",
        "poly1_arcsin",
        "arcsin_alone",
        "power_frac_ln",
        "ln_quad",
    ):
        assert fid in imp, fid
    gaps = {str(f["form_id"]) for f in catalog_gaps(cat)}
    assert "poly_exp_trig" in gaps
    assert "poly1_arccos" in gaps
    assert "poly2_ln_quad" in gaps
    pfd_gaps = {str(f["form_id"]) for f in catalog_gaps(load_form_catalog("partial_fractions"))}
    assert "x4_plus_1" in pfd_gaps
    assert "repeated_quad_square" in pfd_gaps


def test_parts_bc_bank_preset_lookalikes():
    from question_engine.frameworks.primitives.integrals import PARTS_FORM_PRESETS

    bank = PARTS_FORM_PRESETS["bc_bank"]
    prompts: set[str] = set()
    seen: set[str] = set()
    for seed in range(90):
        sample = sample_integral_expression(
            {
                "difficulty": 16,
                "seed": seed,
                "include_answer_key": True,
                "parts_form_preset": "bc_bank",
            },
            generator_key="integration_by_parts",
        )
        fid = _form_id(sample.as_metadata())
        assert fid in bank, (seed, fid, sample.prompt_latex)
        assert fid != "ln_alone"
        assert "+C" in (sample.answer_latex or "")
        prompts.add(sample.prompt_latex or "")
        seen.add(fid)
    assert len(prompts) >= 8, prompts
    assert len(seen) >= 4, seen
    frozen = {
        r"\int x^{3}e^{2x}\,dx",
        r"\int x\arctan(x)\,dx",
        r"\int (\ln(x))^{2}\,dx",
    }
    assert any(p not in frozen for p in prompts), prompts


def test_parts_d0_not_bc_bank_tabular():
    """Host auto D=0 stays one-step LIATE even after bank families exist."""
    allowed = {"ln_alone", "poly1_exp", "poly1_sin", "poly1_cos"}
    for seed in range(30):
        sample = sample_integral_expression(
            {"difficulty": 0, "seed": seed, "include_answer_key": True},
            generator_key="integration_by_parts",
        )
        fid = _form_id(sample.as_metadata())
        assert fid in allowed, (seed, fid, sample.prompt_latex)


def test_pfd_bc_bank_preset_lookalikes():
    from question_engine.frameworks.primitives.integrals import PFD_FORM_PRESETS

    bank = PFD_FORM_PRESETS["bc_bank"]
    prompts: set[str] = set()
    seen: set[str] = set()
    for seed in range(70):
        sample = sample_integral_expression(
            {
                "difficulty": 16,
                "seed": seed,
                "include_answer_key": True,
                "pfd_form_preset": "bc_bank",
            },
            generator_key="integral_partial_fractions",
        )
        fid = _form_id(sample.as_metadata())
        assert fid in bank, (seed, fid, sample.prompt_latex)
        assert fid != "x4_plus_1"
        assert "+C" in (sample.answer_latex or "")
        prompts.add(sample.prompt_latex or "")
        seen.add(fid)
    assert len(prompts) >= 5, prompts
    assert seen & {"distinct_linear_3", "mixed_linear_quad", "repeated_linear_square"}, seen


def test_u_sub_catalog_diversity():
    cat = load_form_catalog("u_substitution")
    implemented = {str(f["form_id"]) for f in implemented_forms(cat)}
    seen: set[str] = set()
    for d, seed0 in ((4, 2), (10, 60), (16, 110)):
        for seed in range(seed0, seed0 + 30):
            sample = sample_integral_expression(
                {
                    "difficulty": d,
                    "seed": seed,
                    "include_answer_key": True,
                    "u_sub_construction": "catalog",
                },
                generator_key="integral_substitution",
            )
            fid = _form_id(sample.as_metadata())
            assert fid in implemented, (d, seed, fid, sample.prompt_latex)
            seen.add(fid)
    assert len(seen) >= 4, seen


def test_trig_sub_catalog_diversity():
    cat = load_form_catalog("trig_substitution")
    implemented = {str(f["form_id"]) for f in implemented_forms(cat)}
    seen: set[str] = set()
    for d, seed0 in ((4, 3), (12, 70), (18, 130)):
        for seed in range(seed0, seed0 + 25):
            sample = sample_integral_expression(
                {"difficulty": d, "seed": seed, "include_answer_key": True},
                generator_key="integral_trig_substitution",
            )
            fid = _form_id(sample.as_metadata())
            assert fid in implemented, (d, seed, fid)
            seen.add(fid)
    assert len(seen) >= 5, seen


def test_pfd_catalog_diversity():
    cat = load_form_catalog("partial_fractions")
    implemented = {
        str(f["form_id"])
        for f in implemented_forms(cat)
        if not str(f["form_id"]).startswith("u_sub_then_pfd")
    }
    seen: set[str] = set()
    for d, seed0 in ((4, 4), (10, 80), (16, 140)):
        for seed in range(seed0, seed0 + 30):
            sample = sample_integral_expression(
                {"difficulty": d, "seed": seed, "include_answer_key": True},
                generator_key="integral_partial_fractions",
            )
            fid = _form_id(sample.as_metadata())
            assert fid in implemented, (d, seed, fid)
            seen.add(fid)
    assert len(seen) >= 3, seen


def test_pfd_d0_distinct_linear_2():
    """D=0 stays two distinct linears — OpenStax §3.4 easy."""
    for seed in range(20):
        sample = sample_integral_expression(
            {"difficulty": 0, "seed": seed, "include_answer_key": True},
            generator_key="integral_partial_fractions",
        )
        fid = _form_id(sample.as_metadata())
        assert fid == "distinct_linear_2", (seed, fid, sample.prompt_latex)
        assert r"\int" in (sample.prompt_latex or "")
        assert "+C" in (sample.answer_latex or "")


def test_pfd_high_d_not_distinct_linear_2():
    """distinct_linear_2 has d_max=10; D=16/22 must be 3-linear / mixed / repeated / quad."""
    seen: set[str] = set()
    for seed in range(36):
        sample = sample_integral_expression(
            {"difficulty": 22, "seed": seed, "include_answer_key": True},
            generator_key="integral_partial_fractions",
        )
        fid = _form_id(sample.as_metadata())
        assert fid != "distinct_linear_2", (seed, fid, sample.prompt_latex)
        seen.add(fid)
        assert "+C" in (sample.answer_latex or "")
    assert seen & {
        "distinct_linear_3",
        "mixed_linear_quad",
        "repeated_linear_square",
    }, seen


def test_pfd_live_seed_101_high_d_not_two_linear():
    from question_engine.api.handler import _generate_for_type

    q = _generate_for_type(
        "calc_indef_int_partial_fractions",
        {"difficulty": 22, "seed": 101, "count": 1, "include_answer_key": True},
    )[0]
    fid = str((q.metadata or {}).get("form_id") or "")
    assert fid != "distinct_linear_2", (fid, q.prompt_latex)
    assert q.answer_latex


def test_limits_catalog_emits_form_ids():
    cat = load_form_catalog("limits")
    for key, min_distinct in (
        ("limit_direct_evaluation", 3),
        ("limit_removable", 2),
        ("limit_at_infinity", 2),
        ("lhopitals_rule", 2),
    ):
        leaf_forms = {
            str(f["form_id"])
            for f in implemented_forms(cat, generator_key=key)
        }
        seen: set[str] = set()
        for seed in range(20, 55):
            sample = sample_limit_expression(
                {"difficulty": 12, "seed": seed, "include_answer_key": True},
                generator_key=key,
            )
            fid = _form_id(sample.metadata)
            assert fid, (key, seed)
            assert fid in leaf_forms or fid.startswith(
                ("direct_", "inf_", "removable_", "lhopital_", "poly_", "rational_", "squeeze", "expr_")
            ) or fid in {
                str(f["form_id"]) for f in implemented_forms(cat)
            }, (key, seed, fid, sorted(leaf_forms)[:8])
            seen.add(fid)
        assert len(seen) >= min_distinct, (key, seen)


def test_derivatives_catalog_emits_form_ids():
    cat = load_form_catalog("derivatives")
    for key in (
        "derivative_power_rule",
        "derivative_product_rule",
        "derivative_chain_rule",
        "derivative_trigonometric",
    ):
        leaf_forms = {
            str(f["form_id"])
            for f in implemented_forms(cat, generator_key=key)
        }
        assert leaf_forms, key
        counts: Counter[str] = Counter()
        for seed in range(30, 60):
            sample = sample_derivative_expression(
                {"difficulty": 10, "seed": seed, "include_answer_key": True},
                generator_key=key,
            )
            fid = _form_id(sample.metadata)
            assert fid in leaf_forms, (key, seed, fid, sorted(leaf_forms))
            counts[fid] += 1
        assert sum(counts.values()) == 30


def test_logdiff_catalog_forms_implemented():
    cat = load_form_catalog("derivatives")
    imp = {
        str(f["form_id"])
        for f in implemented_forms(cat, generator_key="derivative_logarithmic")
    }
    assert "logdiff_power" in imp
    assert "logdiff_x_x" in imp
    assert "logdiff_trig_x" in imp
    gaps = {str(f["form_id"]) for f in catalog_gaps(cat)}
    assert "logarithmic_diff" not in gaps


def test_other_base_catalog_forms_implemented():
    cat = load_form_catalog("derivatives")
    imp = {
        str(f["form_id"])
        for f in implemented_forms(cat, generator_key="derivative_other_base")
    }
    assert "other_base_a_x" in imp
    assert "other_base_log_linear" in imp
    assert "other_base_product" in imp
    a_x = next(f for f in implemented_forms(cat, generator_key="derivative_other_base") if f["form_id"] == "other_base_a_x")
    assert float(a_x.get("d_max")) == 5


def test_invfn_catalog_forms_implemented():
    cat = load_form_catalog("derivatives")
    imp = {
        str(f["form_id"])
        for f in implemented_forms(cat, generator_key="derivative_inverse_functions")
    }
    assert "invfn_power" in imp
    assert "invfn_trig" in imp
    assert "invfn_cubic" in imp
    exp = next(f for f in implemented_forms(cat, generator_key="derivative_inverse_functions") if f["form_id"] == "invfn_exp")
    assert float(exp.get("d_max")) == 18
