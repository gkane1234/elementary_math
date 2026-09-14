"""Goal A: allow_* toggles drop catalog forms. Goal B: bank families are lookalikes."""

from __future__ import annotations

from collections import Counter

from question_engine.frameworks.primitives.integrals import (
    sample_integral_expression,
    topic_allow_defaults,
)
from question_engine.frameworks.primitives.openstax_form_catalogs import (
    filter_forms_by_allows,
    implemented_forms,
    load_form_catalog,
)
from question_engine.generators import GENERATORS


PARTS_FORM_IDS = {
    str(f["form_id"])
    for f in implemented_forms(load_form_catalog("integration_by_parts"))
}
PFD_FORM_IDS = {
    str(f["form_id"])
    for f in implemented_forms(load_form_catalog("partial_fractions"))
}
TRIG_FORM_IDS = {
    str(f["form_id"])
    for f in implemented_forms(load_form_catalog("trig_integrals"))
}
USUB_TRIG_FORM_IDS = {
    str(f["form_id"])
    for f in implemented_forms(load_form_catalog("u_substitution"))
    if "allow_trig" in (f.get("requires_allows") or [])
    or "trig" in (f.get("tricks") or [])
}


def _fid(sample) -> str:
    return str(sample.as_metadata().get("form_id") or "")


def test_filter_forms_by_allows_honors_integral_tricks():
    parts = implemented_forms(load_form_catalog("integration_by_parts"))
    on = filter_forms_by_allows(
        parts,
        {"allow_parts": True, "allow_exp": True, "allow_log": True, "allow_trig": True},
        fallback_on_empty=False,
        soft_c_schedule=False,
    )
    off = filter_forms_by_allows(
        parts,
        {"allow_parts": False, "allow_exp": True, "allow_log": True, "allow_trig": True},
        fallback_on_empty=False,
        soft_c_schedule=False,
    )
    assert {str(f["form_id"]) for f in on} & {"poly1_exp", "cyclic_exp_sin"}
    assert off == []


def test_filter_no_fallback_when_requested():
    trig = implemented_forms(load_form_catalog("trig_integrals"))
    out = filter_forms_by_allows(
        trig,
        {"allow_trig": False},
        fallback_on_empty=False,
        soft_c_schedule=False,
    )
    assert out == []
    restored = filter_forms_by_allows(
        trig,
        {"allow_trig": False},
        fallback_on_empty=True,
        soft_c_schedule=False,
    )
    assert restored  # derivative-style fallback still available


def test_general_defaults_all_technique_allows_on():
    d = topic_allow_defaults("integral_general")
    assert d["allow_trig"] is True
    assert d["allow_exp"] is True
    assert d["allow_log"] is True
    assert d["allow_invtrig"] is True
    assert d["allow_substitution"] is True
    assert d["allow_parts"] is True
    assert d["allow_pfd"] is True
    assert d["allow_trig_sub"] is True


def test_general_allow_parts_off_excludes_parts_form_ids():
    seen: set[str] = set()
    for seed in range(80):
        sample = sample_integral_expression(
            {
                "difficulty": 16,
                "seed": seed,
                "include_answer_key": True,
                "allow_parts": False,
            },
            generator_key="integral_general",
        )
        fid = _fid(sample)
        seen.add(fid)
        assert sample.prompt_latex
        assert sample.answer_latex
        assert fid not in PARTS_FORM_IDS, (seed, fid, sample.prompt_latex)
        tricks = list(sample.as_metadata().get("tricks_required") or [])
        assert "parts" not in tricks, (seed, tricks, sample.prompt_latex)
    assert seen


def test_general_allow_pfd_off_excludes_pfd_form_ids():
    for seed in range(80):
        sample = sample_integral_expression(
            {
                "difficulty": 16,
                "seed": seed,
                "include_answer_key": True,
                "allow_pfd": False,
            },
            generator_key="integral_general",
        )
        fid = _fid(sample)
        assert fid not in PFD_FORM_IDS, (seed, fid, sample.prompt_latex)
        tricks = list(sample.as_metadata().get("tricks_required") or [])
        assert "pfd" not in tricks, (seed, tricks, sample.prompt_latex)


def test_general_allow_trig_off_excludes_trig_bank_families():
    for seed in range(90):
        sample = sample_integral_expression(
            {
                "difficulty": 16,
                "seed": seed,
                "include_answer_key": True,
                "allow_trig": False,
            },
            generator_key="integral_general",
        )
        fid = _fid(sample)
        assert fid not in TRIG_FORM_IDS, (seed, fid, sample.prompt_latex)
        assert fid not in USUB_TRIG_FORM_IDS, (seed, fid, sample.prompt_latex)
        tricks = list(sample.as_metadata().get("tricks_required") or [])
        assert "trig" not in tricks, (seed, tricks, sample.prompt_latex)


def test_usub_leaf_allow_trig_off_drops_trig_bank_forms():
    for seed in range(60):
        sample = sample_integral_expression(
            {
                "difficulty": 16,
                "seed": seed,
                "include_answer_key": True,
                "allow_trig": False,
                "u_sub_form_preset": "bc_bank",
                "u_sub_construction": "catalog",
            },
            generator_key="integral_substitution",
        )
        fid = _fid(sample)
        assert fid not in USUB_TRIG_FORM_IDS, (seed, fid, sample.prompt_latex)
        assert fid != "trig_over_linear_trig_power"
        assert fid != "sin_of_sqrt"


def test_parts_allow_exp_off_drops_cyclic_and_exp_lookalikes():
    banned = {
        "poly1_exp",
        "poly2_exp",
        "poly3_exp",
        "cyclic_exp_sin",
        "cyclic_exp_cos",
    }
    for seed in range(50):
        sample = sample_integral_expression(
            {
                "difficulty": 18,
                "seed": seed,
                "include_answer_key": True,
                "allow_exp": False,
            },
            generator_key="integration_by_parts",
        )
        fid = _fid(sample)
        assert fid not in banned, (seed, fid, sample.prompt_latex)


def test_parts_allow_invtrig_off_drops_arctan_arcsin():
    banned = {
        "arctan_alone",
        "poly1_arctan",
        "poly1_arcsin",
        "arcsin_alone",
        "ln_quad",
    }
    for seed in range(50):
        sample = sample_integral_expression(
            {
                "difficulty": 18,
                "seed": seed,
                "include_answer_key": True,
                "allow_invtrig": False,
            },
            generator_key="integration_by_parts",
        )
        fid = _fid(sample)
        assert fid not in banned, (seed, fid, sample.prompt_latex)
        tricks = list(sample.as_metadata().get("tricks_required") or [])
        assert "invtrig" not in tricks, (seed, tricks, sample.prompt_latex)


def test_parts_allow_log_off_drops_ln_families():
    banned = {
        "ln_alone",
        "poly1_ln",
        "poly2_ln",
        "ln_power_2",
        "ln_power_3",
        "power_frac_ln",
        "ln_quad",
    }
    for seed in range(50):
        sample = sample_integral_expression(
            {
                "difficulty": 18,
                "seed": seed,
                "include_answer_key": True,
                "allow_log": False,
            },
            generator_key="integration_by_parts",
        )
        fid = _fid(sample)
        assert fid not in banned, (seed, fid, sample.prompt_latex)


def test_parts_allow_trig_off_drops_sin_cos_cyclic():
    banned = {
        "poly1_sin",
        "poly1_cos",
        "poly2_sin",
        "poly2_cos",
        "poly3_sin",
        "poly3_cos",
        "cyclic_exp_sin",
        "cyclic_exp_cos",
    }
    for seed in range(50):
        sample = sample_integral_expression(
            {
                "difficulty": 18,
                "seed": seed,
                "include_answer_key": True,
                "allow_trig": False,
            },
            generator_key="integration_by_parts",
        )
        fid = _fid(sample)
        assert fid not in banned, (seed, fid, sample.prompt_latex)


def test_power_quad_neg_lookalikes_not_only_bank_copy():
    """Bank ∫ x/(x²+1)⁴ is one draw of ∫ ax/(bx²+c)^n."""
    prompts: set[str] = set()
    for seed in range(80):
        sample = sample_integral_expression(
            {
                "difficulty": 16,
                "seed": seed,
                "include_answer_key": True,
                "u_sub_form_preset": "bc_bank",
                "u_sub_construction": "catalog",
            },
            generator_key="integral_substitution",
        )
        if _fid(sample) != "power_quad_neg":
            continue
        prompts.add(sample.prompt_latex or "")
        assert "+C" in (sample.answer_latex or "")
        meta = sample.as_metadata()
        assert "u_sub" in (meta.get("tricks_required") or [])
        assert meta.get("form_id") == "power_quad_neg"
    assert len(prompts) >= 3, prompts
    bank_exact = r"\int \frac{x}{\left(x^{2}+1\right)^{4}}\,dx"
    assert any(p != bank_exact for p in prompts), prompts


def test_ln_power_over_x_lookalike_exponent_varies():
    exponents: set[str] = set()
    for seed in range(100):
        sample = sample_integral_expression(
            {
                "difficulty": 16,
                "seed": seed,
                "include_answer_key": True,
                "u_sub_form_preset": "bc_bank",
                "u_sub_construction": "catalog",
            },
            generator_key="integral_log_exp_substitution",
        )
        if _fid(sample) != "ln_power_over_x":
            continue
        exponents.add(sample.prompt_latex or "")
    assert len(exponents) >= 2, exponents


def test_general_d0_stays_simple():
    hard = PARTS_FORM_IDS | PFD_FORM_IDS | {
        "power_quad_neg",
        "cyclic_exp_sin",
        "poly2_exp",
    }
    for seed in range(25):
        sample = sample_integral_expression(
            {"difficulty": 0, "seed": seed, "include_answer_key": True},
            generator_key="integral_general",
        )
        fid = _fid(sample)
        assert fid not in hard, (seed, fid, sample.prompt_latex)
        assert r"\int" in (sample.prompt_latex or "")


def test_general_live_generator_path():
    qs = GENERATORS["integral_general"](
        "calc_indef_int_general",
        {"count": 5, "difficulty": 14, "include_answer_key": True, "seed": 11},
    )
    assert len(qs) == 5
    for q in qs:
        assert q.prompt_latex
        assert q.metadata.get("form_id")
        assert q.metadata.get("tricks_required") is not None


def test_general_high_d_uses_several_techniques():
    techniques: Counter[str] = Counter()
    for seed in range(60):
        sample = sample_integral_expression(
            {"difficulty": 16, "seed": seed, "include_answer_key": True},
            generator_key="integral_general",
        )
        tech = str(sample.technique or "")
        techniques[tech] += 1
        assert sample.as_metadata().get("form_id")
    assert len(techniques) >= 3, techniques
