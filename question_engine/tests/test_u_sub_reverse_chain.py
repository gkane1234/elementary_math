"""Reverse-chain u-sub + named OpenStax form presets."""

from __future__ import annotations

import random

from question_engine.api.handler import _generate_for_type
from question_engine.frameworks.primitives import u_substitution as usub
from question_engine.frameworks.primitives.integrals import sample_integral_expression
from question_engine.frameworks.primitives.poly_expression import differentiate, render_latex
from question_engine.settings.presets import apply_difficulty_presets


CHALLENGING = usub.U_SUB_FORM_PRESETS["challenging"]
POWER_QUAD = usub.U_SUB_FORM_PRESETS["power_quadratic"]


def test_named_presets_are_catalog_form_ids():
    catalog_ids = {
        "power_linear_du",
        "power_quad_x_du",
        "root_quad_x_du",
        "du_over_u_linear",
        "du_over_u_trig",
        "exp_of_trig",
        "exp_of_poly",
        "trig_of_linear",
        "arctan_of_linear",
        "ln_squared_chain",
        "alteration_linear_over_root",
        "nested_trig_exp",
        "sec2_of_u",
        "power_cubic_x2_du",
        "exp_of_cubic",
        "exp_of_quartic",
        "exp_root_chain",
        "exp_power_of_exp",
        "composite_ln_of_trig",
        "power_quad_neg",
        "power_cubic_neg",
        "root_quad_minus",
        "power_quad_m3_2",
        "ln_power_over_x",
        "power_of_one_plus_ln",
        "exp_over_power_of_exp",
        "exp_e2x_over_power",
        "trig_over_linear_trig_power",
        "ln_ln_nested",
        "ln_over_x_sqrt",
        "arctan_of_ln",
        "du_over_u_quadratic",
        "du_over_ln_of_poly",
        "cos_of_ln_over_x",
        "sin_of_sqrt",
        "exp_of_sqrt",
        "root_ln_of_linear",
        "ln_sq_over_root_ln_cube",
        "power_hex_neg",
        "root_of_x4",
    }
    for name, forms in usub.U_SUB_FORM_PRESETS.items():
        if forms is None:
            continue
        assert forms <= catalog_ids, (name, forms - catalog_ids)


def test_hard_preset_selects_challenging_structure():
    settings = apply_difficulty_presets(
        {"difficulty_tier": "hard", "seed": 11, "count": 1, "include_answer_key": True},
        type_id="calc_indef_int_power_rule_with_substitution",
    )
    assert settings["u_sub_form_preset"] == "challenging"
    forms = set()
    for seed in range(25):
        sample = sample_integral_expression(
            {**settings, "seed": seed, "u_sub_construction": "catalog"},
            generator_key="integral_substitution",
        )
        fid = str(sample.as_metadata().get("form_id"))
        forms.add(fid)
        assert fid in CHALLENGING, (fid, sample.prompt_latex)
        assert r"\int" in (sample.prompt_latex or "")
    assert len(forms) >= 2, forms


def test_easy_preset_power_linear_only():
    settings = apply_difficulty_presets(
        {"difficulty_tier": "easy", "seed": 3, "include_answer_key": True},
        type_id="calc_indef_int_power_rule_with_substitution",
    )
    assert settings["u_sub_form_preset"] == "power_linear"
    for seed in range(8):
        sample = sample_integral_expression(
            {**settings, "seed": seed},
            generator_key="integral_substitution",
        )
        assert sample.as_metadata().get("form_id") == "power_linear_du"
        assert "+C" in (sample.answer_latex or "")


def test_medium_preset_quadratic_family():
    settings = apply_difficulty_presets(
        {"difficulty_tier": "medium", "seed": 5, "include_answer_key": True},
        type_id="calc_indef_int_power_rule_with_substitution",
    )
    assert settings["u_sub_form_preset"] == "power_quadratic"
    for seed in range(10):
        sample = sample_integral_expression(
            {**settings, "seed": seed},
            generator_key="integral_substitution",
        )
        assert sample.as_metadata().get("form_id") in POWER_QUAD


def test_reverse_chain_antiderivative_matches_f_of_g():
    rng = random.Random(9)
    for flavor in ("power", "ln_exp", "trig", "invtrig"):
        for d in (0.0, 8.0, 16.0, 22.0):
            sample = usub.sample_reverse_chain_integral(
                d=d,
                flavor=flavor,
                include_plus_c=True,
                allow_trig=flavor in {"trig", "ln_exp"},
                allow_exp=flavor == "ln_exp",
                allow_log=flavor == "ln_exp",
                allow_invtrig=flavor == "invtrig",
                omit_du_constant=False,
                rng=rng,
            )
            assert sample.prompt_latex.startswith(r"\int")
            assert sample.answer_latex.endswith("+C")
            assert sample.metadata.get("construction") == "reverse_chain_expr_skeleton"
            check = sample.metadata.get("deriv_check_latex")
            assert check
            assert check in sample.prompt_latex


def test_reverse_chain_differentiate_equals_integrand_ast():
    from question_engine.frameworks.primitives.expr_skeleton import sample_from_form

    F, Fp, f_tex, fp_tex, _inv = sample_from_form(
        "chain_power_linear",
        conceptual_d=0.0,
        allows={"allow_chain": True, "require_chain": True},
        rng=random.Random(21),
        var="x",
        seed=21,
    )
    dF = differentiate(F, "x")
    assert render_latex(dF, paren_style="minimal") == render_latex(
        Fp, paren_style="minimal"
    )
    sample = usub.sample_reverse_chain_integral(
        d=0.0,
        flavor="power",
        omit_du_constant=False,
        rng=random.Random(21),
        seed=21,
    )
    assert sample.answer_latex.endswith("+C")
    assert r"\int" in sample.prompt_latex
    # Undressed antiderivative is F∘g; integrand is its derivative.
    assert sample.metadata.get("deriv_check_latex") in sample.prompt_latex


def test_live_reverse_chain_leaf():
    qs = _generate_for_type(
        "calc_indef_int_power_rule_with_substitution",
        {
            "difficulty": 16,
            "seed": 44,
            "count": 4,
            "include_answer_key": True,
            "u_sub_construction": "reverse_chain",
            "u_sub_form_preset": "auto",
        },
    )
    assert len(qs) == 4
    for q in qs:
        assert r"\int" in (q.prompt_latex or "")
        assert "+C" in (q.answer_latex or "")
        cons = (q.metadata or {}).get("construction")
        assert cons == "reverse_chain_expr_skeleton", cons


def test_d0_catalog_stays_simple():
    q = _generate_for_type(
        "calc_indef_int_power_rule_with_substitution",
        {
            "difficulty": 0,
            "seed": 101,
            "count": 1,
            "include_answer_key": True,
            "u_sub_construction": "catalog",
            "u_sub_form_preset": "auto",
        },
    )[0]
    assert r"\int" in (q.prompt_latex or "")
    assert (q.metadata or {}).get("form_id") == "power_linear_du"
    assert "+C" in (q.answer_latex or "")


def test_power_cubic_preset_matches_openstax_shape():
    for seed in range(8):
        sample = sample_integral_expression(
            {
                "difficulty": 8,
                "seed": seed,
                "include_answer_key": True,
                "u_sub_form_preset": "power_cubic",
                "u_sub_construction": "catalog",
            },
            generator_key="integral_substitution",
        )
        assert sample.as_metadata().get("form_id") == "power_cubic_x2_du"
        assert r"x^{2}" in (sample.prompt_latex or "")
        assert r"x^{3}" in (sample.prompt_latex or "")
        assert "+C" in (sample.answer_latex or "")


def test_challenging_power_leaf_includes_cubic():
    forms = set()
    for seed in range(40):
        sample = sample_integral_expression(
            {
                "difficulty": 16,
                "seed": seed,
                "include_answer_key": True,
                "u_sub_form_preset": "challenging",
                "u_sub_construction": "catalog",
            },
            generator_key="integral_substitution",
        )
        fid = str(sample.as_metadata().get("form_id"))
        forms.add(fid)
        assert fid in CHALLENGING
        assert fid in {
            "power_cubic_x2_du",
            "root_quad_x_du",
            "alteration_linear_over_root",
        }, fid
    assert "power_cubic_x2_du" in forms, forms
    assert len(forms) >= 2, forms


def test_challenging_ln_exp_includes_openstax_56_shapes():
    forms = set()
    for seed in range(50):
        sample = sample_integral_expression(
            {
                "difficulty": 16,
                "seed": seed,
                "include_answer_key": True,
                "u_sub_form_preset": "challenging",
                "u_sub_construction": "catalog",
            },
            generator_key="integral_log_exp_substitution",
        )
        fid = str(sample.as_metadata().get("form_id"))
        forms.add(fid)
        assert fid in CHALLENGING, (fid, sample.prompt_latex)
    assert forms & {
        "exp_of_cubic",
        "exp_of_quartic",
        "exp_root_chain",
        "exp_power_of_exp",
        "ln_squared_chain",
        "nested_trig_exp",
    }, forms
    assert len(forms) >= 2, forms


def test_exp_of_quartic_matches_checkpoint_533():
    """OpenStax Checkpoint 5.33: ∫ 2x³ e^{x⁴} dx (hide 2 at high format)."""
    hits = []
    for seed in range(80):
        sample = sample_integral_expression(
            {
                "difficulty": 8,
                "seed": seed,
                "include_answer_key": True,
                "u_sub_form_preset": "exp_chain",
                "u_sub_construction": "catalog",
            },
            generator_key="integral_log_exp_substitution",
        )
        if str(sample.as_metadata().get("form_id")) != "exp_of_quartic":
            continue
        p = sample.prompt_latex or ""
        a = sample.answer_latex or ""
        assert r"x^{3}" in p
        assert r"x^{4}" in p
        assert r"e^{" in p
        assert r"2x^{3}" in p  # D=8 format_tier < 2 keeps OpenStax 2
        assert "+C" in a
        assert r"e^{" in a
        assert r"\int" not in a
        hits.append(p)
    assert hits, "expected Checkpoint 5.33 quartic exp form in exp_chain mix"


def test_ln_exp_d0_stays_simple_not_quartic():
    for seed in (101, 207, 3, 11, 44):
        sample = sample_integral_expression(
            {
                "difficulty": 0,
                "seed": seed,
                "include_answer_key": True,
                "u_sub_construction": "catalog",
                "u_sub_form_preset": "auto",
            },
            generator_key="integral_log_exp_substitution",
        )
        fid = str(sample.as_metadata().get("form_id"))
        assert fid != "exp_of_quartic", (seed, sample.prompt_latex)
        assert fid in {"du_over_u_linear", "du_over_u_trig", "exp_of_poly"}, (
            seed,
            fid,
            sample.prompt_latex,
        )


def test_composite_ln_of_trig_cot_or_tan():
    sample = sample_integral_expression(
        {
            "difficulty": 10,
            "seed": 4,
            "include_answer_key": True,
            "u_sub_form_preset": "trig_chain",
            "u_sub_construction": "catalog",
        },
        generator_key="integral_substitution",
    )
    # Power leaf + trig_chain falls through to the full preset set.
    fid = str(sample.as_metadata().get("form_id"))
    assert fid in usub.U_SUB_FORM_PRESETS["trig_chain"]
    hits = set()
    for seed in range(30):
        s = sample_integral_expression(
            {
                "difficulty": 10,
                "seed": seed,
                "include_answer_key": True,
                "u_sub_form_preset": "trig_chain",
                "u_sub_construction": "catalog",
            },
            generator_key="integral_log_exp_substitution",
        )
        hits.add(str(s.as_metadata().get("form_id")))
        if str(s.as_metadata().get("form_id")) == "composite_ln_of_trig":
            p = s.prompt_latex or ""
            assert r"\cot" in p or r"\tan" in p
            assert r"\ln" in (s.answer_latex or "")
    # trig_chain on ln_exp host intersects exp/trig forms; cot may or may not
    # appear depending on flavor filter. Force via power-leaf fall-through:
    found = False
    for seed in range(40):
        s = sample_integral_expression(
            {
                "difficulty": 10,
                "seed": seed,
                "include_answer_key": True,
                "u_sub_form_preset": "trig_chain",
                "u_sub_construction": "catalog",
            },
            generator_key="integral_substitution",
        )
        if str(s.as_metadata().get("form_id")) == "composite_ln_of_trig":
            found = True
            p = s.prompt_latex or ""
            assert r"\cot" in p or r"\tan" in p
            break
    assert found, hits


def test_reverse_chain_elides_unit_exponents():
    for flavor in ("power", "ln_exp", "invtrig"):
        for d in (0.0, 8.0, 16.0, 22.0):
            for seed in range(12):
                sample = usub.sample_reverse_chain_integral(
                    d=d,
                    flavor=flavor,
                    include_plus_c=True,
                    allow_trig=flavor in {"trig", "ln_exp"},
                    allow_exp=flavor == "ln_exp",
                    allow_log=flavor == "ln_exp",
                    allow_invtrig=flavor == "invtrig",
                    rng=random.Random(seed),
                    seed=seed,
                )
                assert "^{1}" not in (sample.prompt_latex or ""), (
                    flavor,
                    d,
                    seed,
                    sample.prompt_latex,
                )
                assert "^{1}" not in (sample.answer_latex or "")
                check = sample.metadata.get("deriv_check_latex") or ""
                assert "^{1}" not in check


BC_BANK = usub.U_SUB_FORM_PRESETS["bc_bank"]


def _bc_bank_hits(generator_key: str, *, d: float = 16.0, n: int = 80) -> dict[str, str]:
    hits: dict[str, str] = {}
    for seed in range(n):
        sample = sample_integral_expression(
            {
                "difficulty": d,
                "seed": seed,
                "include_answer_key": True,
                "u_sub_form_preset": "bc_bank",
                "u_sub_construction": "catalog",
            },
            generator_key=generator_key,
        )
        fid = str(sample.as_metadata().get("form_id"))
        assert fid in BC_BANK, (fid, sample.prompt_latex)
        assert r"\int" in (sample.prompt_latex or "")
        assert "+C" in (sample.answer_latex or "")
        hits.setdefault(fid, sample.prompt_latex or "")
    return hits


def test_bc_bank_power_emits_quad_neg_family():
    hits = _bc_bank_hits("integral_substitution")
    assert hits.keys() & {
        "power_quad_neg",
        "power_cubic_neg",
        "root_quad_minus",
        "power_quad_m3_2",
        "power_hex_neg",
        "root_of_x4",
        "du_over_u_quadratic",
        "sin_of_sqrt",
    }
    assert "power_quad_neg" in hits, hits
    assert r"\frac{" in hits["power_quad_neg"]


def test_bc_bank_ln_exp_named_shapes():
    hits = _bc_bank_hits("integral_log_exp_substitution", n=120)
    assert "ln_power_over_x" in hits, hits
    assert r"\ln" in hits["ln_power_over_x"]
    assert "exp_over_power_of_exp" in hits, hits
    assert r"e^{" in hits["exp_over_power_of_exp"]


def test_bc_bank_trig_over_a_plus_trig():
    """sin/(a+cos)^n lives on trig_chain (power host fall-through), not power∩bc_bank."""
    hits: dict[str, str] = {}
    for seed in range(80):
        sample = sample_integral_expression(
            {
                "difficulty": 16,
                "seed": seed,
                "include_answer_key": True,
                "allow_trig": True,
                "u_sub_form_preset": "trig_chain",
                "u_sub_construction": "catalog",
            },
            generator_key="integral_substitution",
        )
        fid = str(sample.as_metadata().get("form_id"))
        hits[fid] = sample.prompt_latex or ""
        assert fid in usub.U_SUB_FORM_PRESETS["trig_chain"], (fid, sample.prompt_latex)
        assert "+C" in (sample.answer_latex or "")
    assert "trig_over_linear_trig_power" in hits, hits
    p = hits["trig_over_linear_trig_power"]
    assert r"\sin" in p or r"\cos" in p or r"\sec" in p or r"\tan" in p


def test_bc_bank_d0_auto_stays_openstax_easy():
    for seed in (101, 207, 3, 11, 44):
        sample = sample_integral_expression(
            {
                "difficulty": 0,
                "seed": seed,
                "include_answer_key": True,
                "u_sub_construction": "catalog",
                "u_sub_form_preset": "auto",
            },
            generator_key="integral_substitution",
        )
        fid = str(sample.as_metadata().get("form_id"))
        assert fid not in BC_BANK, (seed, fid, sample.prompt_latex)
        assert fid == "power_linear_du", (seed, fid, sample.prompt_latex)
