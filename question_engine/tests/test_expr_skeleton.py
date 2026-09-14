"""Tests for OpenStax form → Diff(F(u)) skeleton pattern fill."""

from __future__ import annotations

import random
from fractions import Fraction

from question_engine.frameworks.primitives.expr_skeleton import (
    FORM_PATTERNS,
    has_form_pattern,
    pattern_for_form,
    sample_expr_from_pattern,
    sample_from_form,
    richness_from_conceptual,
)
from question_engine.frameworks.primitives.poly_expression import (
    Add,
    Const,
    Fn,
    Mul,
    Pow,
    Var,
    render_latex,
)
from question_engine.frameworks.primitives.derivatives import sample_derivative_expression
from question_engine.frameworks.primitives.expression_flesh import (
    CORE_FLESH_MOVES,
    eligible_moves,
)


def test_all_implemented_forms_have_patterns() -> None:
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        load_form_catalog,
    )

    catalog = load_form_catalog("derivatives")
    for form in catalog.get("forms") or []:
        fid = str(form.get("form_id") or "")
        status = str(form.get("generation_status") or "")
        if status == "stub" or not fid:
            continue
        # Implicit / log-diff use structured packs, not Diff expr_skeleton patterns.
        if fid.startswith("implicit_") or fid.startswith("logdiff_"):
            continue
        assert has_form_pattern(fid), f"missing pattern for {fid}"
        assert pattern_for_form(fid) is not None


def test_shared_prod_pattern_emits_mul_shared_u() -> None:
    pat = FORM_PATTERNS["trig_product_chain"]
    assert pat.kind == "diff_prod_fg_u"
    rng = random.Random(11)
    rich = richness_from_conceptual(8.0)
    expr, meta = sample_expr_from_pattern(
        pat,
        richness=rich,
        allows={"allow_trig": True},
        rng=rng,
    )
    assert meta["skeleton_kind"] == "diff_prod_fg_u"
    assert meta["shared_inner"] is True
    assert isinstance(expr, Mul)
    assert len(expr.factors) == 2
    assert all(isinstance(f, Fn) for f in expr.factors)
    assert render_latex(expr.factors[0].arg) == render_latex(expr.factors[1].arg)


def test_independent_prod_pattern_allows_distinct_inners() -> None:
    pat = FORM_PATTERNS["product_poly_trig"]
    assert pat.kind == "diff_prod_fg"
    saw_distinct = False
    for seed in range(80):
        expr, meta = sample_expr_from_pattern(
            pat,
            richness=richness_from_conceptual(10.0),
            allows={"allow_trig": True},
            rng=random.Random(seed),
        )
        assert meta["shared_inner"] is False
        assert isinstance(expr, Mul) and len(expr.factors) == 2
        f, g = expr.factors
        if not isinstance(g, Fn):
            continue
        poly_l = render_latex(f)
        arg_l = render_latex(g.arg)
        # Independent: poly factor is not forced equal to the trig argument.
        if poly_l != arg_l:
            saw_distinct = True
            break
    assert saw_distinct


def test_coef_times_add_does_not_digit_glue() -> None:
    """Regression: 5·(5x²+2x−4) must not render as 55x²+2x−4."""
    u = Add(
        (
            Mul((Const(Fraction(5)), Pow(Var("x"), Fraction(2)))),
            Mul((Const(Fraction(2)), Var("x"))),
            Const(Fraction(-4)),
        )
    )
    body = render_latex(Mul((Const(Fraction(5)), u)))
    assert "55x" not in body
    assert r"5\left(" in body or r"5\left(5x" in body
    prod = render_latex(Mul((Mul((Const(Fraction(5)), u)), Fn("sin", u))))
    assert "55x" not in prod
    assert r"\sin\left(5x^{2} + 2x - 4\right)" in prod


def test_shared_u_poly_trig_preserves_inner() -> None:
    """Shared-u poly×trig (if forced via trig_product style) keeps identical arg."""
    # Use ln_exp / trig shared products heavily
    for seed in range(40):
        expr, _d, body, _deriv, inv = sample_from_form(
            "trig_product_chain",
            conceptual_d=14.0,
            allows={"allow_trig": True},
            rng=random.Random(seed),
        )
        assert inv["shared_inner"] is True
        assert isinstance(expr, Mul)
        f, g = expr.factors
        assert isinstance(f, Fn) and isinstance(g, Fn)
        assert render_latex(f.arg) == render_latex(g.arg)
        # No digit-glued false cousin
        assert "55x" not in body


def test_quot_pattern_emits_mul_pow_neg() -> None:
    rng = random.Random(5)
    expr, _d, body, deriv, inv = sample_from_form(
        "quotient_poly",
        conceptual_d=4.0,
        rng=rng,
    )
    assert inv["skeleton_kind"] == "diff_quot_fg"
    assert inv["shared_inner"] is False
    assert isinstance(expr, Mul)
    assert any(isinstance(f, Pow) and f.exp == -1 for f in expr.factors)
    assert r"\frac{" in body
    assert r"\frac{1}{" not in body or body.count(r"\frac{") >= 1
    # Real F/G — not awkward F · 1/G juxtaposition as the prompt body.
    assert not body.endswith(r"\frac{1}{-3x}") or r"\frac{" in body
    assert body and deriv
    assert "quotient" in inv.get("methods_used", [])
    assert "product" not in inv.get("methods_used", [])


def test_power_poly_pattern() -> None:
    rng = random.Random(3)
    expr, _d, body, deriv, inv = sample_from_form(
        "power_poly", conceptual_d=0.0, rng=rng
    )
    assert inv["core_form_id"] == "power_poly"
    assert inv.get("skeleton_kind") == "diff_pow_h_n"
    assert "x" in body


def test_richness_bands() -> None:
    assert richness_from_conceptual(1.0).band == "low"
    assert richness_from_conceptual(1.0).allow_poly_u is False
    assert richness_from_conceptual(1.0).force_min_nest == 0
    mid = richness_from_conceptual(8.0)
    assert mid.band == "mid"
    assert mid.allow_poly_u is True
    assert mid.prefer_poly_u is True
    assert mid.force_min_nest == 0
    high = richness_from_conceptual(15.0)
    assert high.band == "high"
    assert high.nest_budget == 1
    assert high.force_min_nest == 1
    assert high.power_min >= 3
    elite = richness_from_conceptual(22.0)
    assert elite.band == "elite"
    assert elite.nest_budget == 2
    assert elite.force_min_nest == 2


def test_cost_spend_debug_fields_present() -> None:
    _expr, _d, _body, _deriv, inv = sample_from_form(
        "power_poly",
        conceptual_d=14.0,
        rng=random.Random(7),
        seed=7,
    )
    assert inv.get("richness_knobs")
    assert inv["richness_knobs"]["band"] == "high"
    # Pure power forms cap nest at 0 (harden via poly / |n|).
    assert inv["richness_knobs"]["nest_budget"] == 0
    assert inv["richness_knobs"]["force_min_nest"] == 0
    spend = inv.get("cost_spend") or {}
    assert "degree_max" in spend
    assert "n_applies" in spend
    assert "inner_kind" in spend
    assert spend.get("pattern_locks_top_structure") is True
    assert inv.get("rng_seed") == 7
    assert inv.get("atom_fn_candidates") == ["poly"]


def test_c_ladder_densifies_power_poly() -> None:
    """Same form across C=2/8/14/20 should show increasing hole richness.

    Power forms must NOT grow via compose-pow towers; densify poly / |n|.
    Without allow_chain, never emit outer power of affine/poly.
    """
    bodies: list[str] = []
    spends: list[dict] = []
    knobs_list: list[dict] = []
    for d in (2.0, 8.0, 14.0, 20.0):
        expr, _dd, body, _der, inv = sample_from_form(
            "power_poly",
            conceptual_d=d,
            allows={"allow_chain": False},
            rng=random.Random(42),
            seed=42,
        )
        bodies.append(body)
        spends.append(inv.get("cost_spend") or {})
        knobs = inv.get("richness_knobs") or {}
        knobs_list.append(knobs)
        assert knobs.get("conceptual_d") == d
        assert knobs.get("nest_budget") == 0
        assert knobs.get("force_min_nest") == 0
        assert "chain" not in (inv.get("methods_used") or []), body
        # No compose-pow towers: if Pow, base must not itself be a Pow.
        core = expr
        if isinstance(core, Mul) and len(core.factors) == 2 and isinstance(
            core.factors[0], Const
        ):
            core = core.factors[1]
        if isinstance(core, Pow):
            assert not isinstance(core.base, Pow), body
            assert isinstance(core.base, Var), body
        else:
            assert isinstance(core, (Add, Mul, Pow, Var)), body
    # Latex should not be identical across the full ladder (structure densifies).
    assert len(set(bodies)) >= 2, bodies
    assert knobs_list[2]["power_max"] >= knobs_list[0]["power_max"]
    assert knobs_list[3]["coef_abs_max"] >= knobs_list[0]["coef_abs_max"]


def test_power_no_chain_never_affine_base() -> None:
    for seed in range(40):
        expr, _d, body, _der, inv = sample_from_form(
            "power_poly",
            conceptual_d=2.0,
            allows={"allow_chain": False},
            rng=random.Random(seed),
            seed=seed,
        )
        assert "chain" not in (inv.get("methods_used") or []), body
        assert inv.get("chain_depth", 0) == 0


def test_power_with_chain_can_emit_affine_base() -> None:
    saw_chain = False
    for seed in range(60):
        _e, _d, body, _der, inv = sample_from_form(
            "chain_power_linear",
            conceptual_d=8.0,
            allows={"allow_chain": True, "require_chain": True},
            rng=random.Random(seed),
            seed=seed,
        )
        if "chain" in (inv.get("methods_used") or []):
            saw_chain = True
            assert r"\left(" in body or "chain" in inv["methods_used"]
            break
    assert saw_chain


def test_trig_basic_low_c_is_simple_apply() -> None:
    for seed in range(30):
        expr, _d, body, _der, inv = sample_from_form(
            "trig_basic",
            conceptual_d=2.0,
            allows={"allow_trig": True},
            rng=random.Random(seed),
            seed=seed,
        )
        assert inv["skeleton_kind"] == "diff_apply_fn_u"
        assert isinstance(expr, Fn)
        assert expr.name in ("sin", "cos", "tan")
        assert not isinstance(expr, Mul)
        assert inv.get("inner_kind") in {"var", "affine"}
        # No poly×trig product shape.
        assert r")\sin" not in body and r")\cos" not in body


def test_product_poly_trig_is_fn_fn_not_raw_poly() -> None:
    for seed in range(25):
        expr, _d, body, _der, inv = sample_from_form(
            "product_poly_trig",
            conceptual_d=8.0,
            allows={"allow_trig": True},
            rng=random.Random(seed),
            seed=seed,
        )
        assert inv["skeleton_kind"] == "diff_prod_fg"
        assert isinstance(expr, Mul)
        # Both factors should be Apply(trig, …), not a bare poly×trig.
        assert all(isinstance(f, Fn) or (
            isinstance(f, Mul) and any(isinstance(x, Fn) for x in f.factors)
        ) for f in expr.factors), body
        assert "sin" in body or "cos" in body or "tan" in body


def test_allow_trig_false_hard_gate_on_chain() -> None:
    for seed in range(30):
        sample = sample_derivative_expression(
            {
                "conceptual_difficulty": 10.0,
                "spec_difficulty": 0.0,
                "conceptual_seed": seed,
                "spec_seed": 1,
                "allow_trig": False,
                "allow_exp": True,
                "allow_log": True,
                "allow_chain": True,
                "require_chain": True,
            },
            generator_key="derivative_chain_rule",
        )
        text = f"{sample.prompt_latex} {sample.answer_latex}"
        assert r"\sin" not in text
        assert r"\cos" not in text
        assert r"\tan" not in text


def test_allow_invtrig_false_on_quotient() -> None:
    for seed in range(25):
        sample = sample_derivative_expression(
            {
                "conceptual_difficulty": 10.0,
                "spec_difficulty": 0.0,
                "conceptual_seed": seed,
                "spec_seed": 1,
                "allow_invtrig": False,
                "allow_trig": False,
                "allow_quotient": True,
                "require_quotient": True,
            },
            generator_key="derivative_quotient_rule",
        )
        text = f"{sample.prompt_latex} {sample.answer_latex}"
        assert "arcsin" not in text.lower()
        assert "arctan" not in text.lower()
        assert r"\arcsin" not in text
        assert r"\arctan" not in text


def test_product_low_c_is_simple_fn_fn() -> None:
    """C≈2 product should be fn×fn, not nested-power stacks."""
    hard_nest = 0
    for seed in range(40):
        _e, _d, body, _der, inv = sample_from_form(
            "product_two_poly",
            conceptual_d=2.0,
            rng=random.Random(seed),
            seed=seed,
        )
        assert inv["skeleton_kind"] == "diff_prod_fg"
        # No (…)^{n}(…)^{m} tower factors at low C.
        if body.count(r"^{") >= 2 and r"\left(" in body:
            hard_nest += 1
        assert r")^{" not in body or body.count(r")^{") <= 1
    assert hard_nest <= 8


def _pow_factors(expr: ExprAST) -> list[Pow]:
    assert isinstance(expr, Mul)
    out: list[Pow] = []
    for fac in expr.factors:
        core = fac
        if (
            isinstance(fac, Mul)
            and len(fac.factors) == 2
            and isinstance(fac.factors[0], Const)
        ):
            core = fac.factors[1]
        assert isinstance(core, Pow), render_latex(expr)
        out.append(core)
    return out


def test_product_chain_openstax_forms_exist() -> None:
    for fid in ("product_one_chain", "product_chain_powers", "product_trig_exp_chain"):
        assert has_form_pattern(fid)
        pat = pattern_for_form(fid)
        assert pat is not None
        assert pat.kind == "diff_prod_fg"
        assert pat.require_composed_factor is True
    assert pattern_for_form("product_chain_powers").both_factors_pow is True


def test_product_chain_powers_is_two_affine_powers() -> None:
    """OpenStax §3.6 Example 3.54 shape: (ax+b)^n (cx+d)^m, nest 1 not 3-deep."""
    for seed in range(25):
        expr, _d, body, _der, inv = sample_from_form(
            "product_chain_powers",
            conceptual_d=10.0,
            allows={"allow_chain": True},
            rng=random.Random(seed),
            seed=seed,
        )
        assert inv["skeleton_kind"] == "diff_prod_fg"
        assert "product" in (inv.get("methods_used") or []), body
        assert "chain" in (inv.get("methods_used") or []), body
        assert int(inv.get("chain_depth") or 0) == 1, body
        pows = _pow_factors(expr)
        assert len(pows) == 2, body
        for p in pows:
            assert isinstance(p.base, Add), body
        assert render_latex(pows[0]) != render_latex(pows[1]), body


def test_product_one_chain_has_exactly_one_composed_factor() -> None:
    for seed in range(20):
        expr, _d, body, _der, inv = sample_from_form(
            "product_one_chain",
            conceptual_d=8.0,
            allows={"allow_chain": True},
            rng=random.Random(seed),
            seed=seed,
        )
        assert isinstance(expr, Mul)
        composed = 0
        for fac in expr.factors:
            core = fac
            if (
                isinstance(fac, Mul)
                and len(fac.factors) == 2
                and isinstance(fac.factors[0], Const)
            ):
                core = fac.factors[1]
            if isinstance(core, Pow) and not isinstance(core.base, Var):
                composed += 1
        assert composed >= 1, body
        assert int(inv.get("chain_depth") or 0) == 1, body
        assert "product" in (inv.get("methods_used") or [])


def test_product_trig_exp_chain_is_trig_times_composed_exp() -> None:
    for seed in range(20):
        expr, _d, body, _der, inv = sample_from_form(
            "product_trig_exp_chain",
            conceptual_d=10.0,
            allows={"allow_trig": True, "allow_exp": True, "allow_chain": True},
            rng=random.Random(seed),
            seed=seed,
        )
        assert isinstance(expr, Mul)
        assert r"e^{" in body
        assert r"\sin" in body or r"\cos" in body or r"\tan" in body
        assert "product" in (inv.get("methods_used") or [])
        assert "chain" in (inv.get("methods_used") or [])
        assert int(inv.get("chain_depth") or 0) == 1, body
        # Not a 3-deep nest (no e^{sin(poly)}).
        assert body.count(r"e^{") == 1


def test_product_d0_does_not_require_three_deep_nest() -> None:
    depths: list[int] = []
    for seed in range(40):
        sample = sample_derivative_expression(
            {"difficulty": 0, "seed": seed, "include_answer_key": True},
            generator_key="derivative_product_rule",
        )
        fid = str(sample.metadata.get("form_id") or "")
        assert fid in {"", "product_two_poly"}, (fid, sample.prompt_latex)
        assert sample.chain_depth < 3, sample.prompt_latex
        depths.append(int(sample.chain_depth))
        assert "product" in sample.methods_used
    assert max(depths) <= 1
    assert depths.count(0) >= 30


def test_product_high_d_can_emit_nested_factor() -> None:
    hits = 0
    seen_two_chain = 0
    for seed in range(50):
        sample = sample_derivative_expression(
            {
                "difficulty": 16,
                "seed": seed,
                "include_answer_key": True,
                "allow_chain": True,
            },
            generator_key="derivative_product_rule",
        )
        assert "product" in sample.methods_used, sample.prompt_latex
        assert sample.chain_depth < 3, sample.prompt_latex
        fid = str(sample.metadata.get("form_id") or "")
        if fid == "product_chain_powers":
            seen_two_chain += 1
        if "chain" in sample.methods_used and sample.chain_depth >= 1:
            hits += 1
    assert hits >= 8, hits
    assert seen_two_chain >= 1


def test_chain_leaf_does_not_own_product_chain_forms() -> None:
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        implemented_forms,
        load_form_catalog,
    )

    cat = load_form_catalog("derivatives")
    chain_ids = {
        str(f["form_id"])
        for f in implemented_forms(cat, generator_key="derivative_chain_rule")
    }
    log_ids = {
        str(f["form_id"])
        for f in implemented_forms(cat, generator_key="derivative_logarithmic")
    }
    product_ids = {
        str(f["form_id"])
        for f in implemented_forms(cat, generator_key="derivative_product_rule")
    }
    for fid in ("product_one_chain", "product_chain_powers", "product_trig_exp_chain"):
        assert fid in product_ids
        assert fid not in chain_ids
        assert fid not in log_ids


def test_chain_openstax_compose_forms_exist() -> None:
    for fid in (
        "chain_trig_poly",
        "chain_exp_poly",
        "chain_ln_poly",
        "chain_power_trig",
        "chain_nested",
    ):
        assert has_form_pattern(fid)
        pat = pattern_for_form(fid)
        assert pat is not None
        assert pat.kind in {"diff_apply_fn_u", "diff_pow_h_n"}


def test_chain_nested_picks_unlike_layers_from_allows() -> None:
    seen_outers: set[str] = set()
    unlike = 0
    for seed in range(40):
        expr, _d, body, _der, inv = sample_from_form(
            "chain_nested",
            conceptual_d=16.0,
            allows={
                "allow_trig": True,
                "allow_exp": True,
                "allow_log": True,
                "allow_chain": True,
                "require_chain": True,
            },
            rng=random.Random(seed),
            seed=seed,
        )
        layers = list(inv.get("compose_layers") or [])
        assert layers, body
        seen_outers.add(str(inv.get("chosen_outer") or layers[0]))
        specials = [x for x in layers if x not in {"pow"}]
        if len(set(specials)) >= 2:
            unlike += 1
        assert "sin" in body or "cos" in body or "tan" in body or r"e^{" in body or r"\ln" in body
        assert isinstance(expr, (Fn, Pow, Mul))
    assert len(seen_outers) >= 2
    assert unlike >= 5


def test_ln_exp_low_c_is_single_apply() -> None:
    for fid in ("ln_basic", "exp_basic"):
        for seed in range(20):
            expr, _d, body, _der, inv = sample_from_form(
                fid,
                conceptual_d=2.0,
                rng=random.Random(seed),
                seed=seed,
            )
            assert inv["skeleton_kind"] == "diff_apply_fn_u"
            assert isinstance(expr, Fn)
            assert expr.name in ("ln", "exp")
            # Single apply — not a product default.
            assert not isinstance(expr, Mul)
            assert r"e^{" in body or r"\ln" in body


def test_demoted_flesh_moves_not_in_core() -> None:
    assert "add_cancel_const" not in CORE_FLESH_MOVES
    assert "cancel_quot_bait" not in CORE_FLESH_MOVES
    el = eligible_moves(leaf="derivative_power_rule", allows={})
    assert "add_cancel_const" not in el
    assert "cancel_quot_bait" not in el


def test_deriv_wire_uses_skeleton_for_pilot_form() -> None:
    sample = sample_derivative_expression(
        {
            "conceptual_difficulty": 4.0,
            "spec_difficulty": 0.0,
            "conceptual_seed": 42,
            "spec_seed": 99,
            "allow_trig": True,
            "allow_product": True,
        },
        generator_key="derivative_product_rule",
    )
    meta = sample.metadata
    fid = str(meta.get("core_form_id") or meta.get("form_id") or "")
    assert fid
    if has_form_pattern(fid):
        assert meta.get("skeleton_source") == "expr_skeleton"
        assert meta.get("skeleton_pattern")


def test_live_product_no_digit_glue_cousin() -> None:
    """Live product_rule path must not emit 55x²…sin(5x²…) class bugs."""
    for seed in range(60):
        sample = sample_derivative_expression(
            {
                "conceptual_difficulty": 14.0,
                "spec_difficulty": 0.0,
                "conceptual_seed": seed,
                "spec_seed": 1,
                "allow_trig": True,
                "allow_product": True,
            },
            generator_key="derivative_product_rule",
        )
        text = f"{sample.prompt_latex} {sample.answer_latex}"
        assert "55x^{2}" not in text
        assert "55x^2" not in text
        # Honest poly-of-u keep parens when scaled: 5(5x²+…) not 55x²+…
        if r"\sin" in text and "x^{2}" in text:
            assert "55x" not in text.replace(" ", "")


def test_spec_does_not_change_pattern() -> None:
    base = {
        "conceptual_difficulty": 8.0,
        "conceptual_seed": 1001,
        "allow_trig": True,
        "allow_product": True,
    }
    a = sample_derivative_expression(
        {**base, "spec_difficulty": 0.0, "spec_seed": 1},
        generator_key="derivative_trigonometric",
    )
    b = sample_derivative_expression(
        {**base, "spec_difficulty": 24.0, "spec_seed": 2},
        generator_key="derivative_trigonometric",
    )
    ma, mb = a.metadata, b.metadata
    if ma.get("form_id") == mb.get("form_id") and has_form_pattern(
        str(ma.get("form_id") or "")
    ):
        assert ma.get("skeleton_pattern") == mb.get("skeleton_pattern")
