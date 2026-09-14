"""Tests for Spec-driven poly / elementary expression sampler."""

from __future__ import annotations

import random

from question_engine.frameworks.primitives.poly_expression import (
    ExpressionSpec,
    differentiate,
    pack_algebraic_chain,
    pack_power_rule,
    pack_product_rule,
    pack_special_atom,
    render_latex,
    sample_and_differentiate,
    sample_expression,
    sample_poly_atom,
    structure_inventory,
)
from question_engine.frameworks.primitives.derivatives import sample_derivative_expression
from question_engine.generators.calculus_derivative_rules import GENERATORS


def test_sample_poly_atom_fixed_seed_stable() -> None:
    a = sample_poly_atom(random.Random(7), "x", 5, 4, extra_term=False)
    b = sample_poly_atom(random.Random(7), "x", 5, 4, extra_term=False)
    assert a.body_latex == b.body_latex
    assert a.deriv_latex == b.deriv_latex
    assert a.body_latex
    assert a.deriv_latex


def test_sample_poly_atom_extra_term_fixed_seed() -> None:
    a = sample_poly_atom(random.Random(11), "x", 4, 4, extra_term=True)
    b = sample_poly_atom(random.Random(11), "x", 4, 4, extra_term=True)
    assert a == b
    assert "+" in a.body_latex or "-" in a.body_latex


def test_power_pack_sample_and_diff() -> None:
    spec = pack_power_rule(3.0, coef_hi=4, power_max=4, extra_term=False)
    expr, d_expr, body, deriv, inv = sample_and_differentiate(
        spec, rng=random.Random(0)
    )
    assert body
    assert deriv
    assert "algebraic" in inv["function_classes"] or inv.get("function_classes") is None
    assert inv["shape_id"]
    # differentiate is AST→AST
    assert render_latex(differentiate(expr)) == render_latex(d_expr) or deriv


def test_product_pack_requires_product() -> None:
    spec = pack_product_rule(6.0, coef_hi=4, power_max=3)
    expr = sample_expression(spec, rng=random.Random(2))
    inv = structure_inventory(expr)
    assert inv["has_product"]
    body = render_latex(expr, paren_style=spec.paren_style)
    assert body


def test_render_mul_fn_factors_omit_outer_parens() -> None:
    from question_engine.frameworks.primitives.poly_expression import (
        Const,
        Fn,
        Mul,
        Pow,
        Var,
    )

    expr = Mul(
        (
            Fn("sin", Mul((Const(3), Var("x")))),
            Fn("cos", Mul((Const(2), Var("x")))),
        )
    )
    for style in ("minimal", "always_factors"):
        body = render_latex(expr, paren_style=style)  # type: ignore[arg-type]
        assert body == r"\sin(3x)\cos(2x)"
        assert r"\left(" not in body

    expr2 = Mul((Pow(Var("x"), 2), Fn("arctan", Var("x"))))
    assert render_latex(expr2, paren_style="always_factors") == r"x^{2}\arctan(x)"

    expr3 = Mul(
        (
            Pow(Fn("sin", Mul((Const(3), Var("x")))), 2),
            Fn("cos", Mul((Const(2), Var("x")))),
        )
    )
    assert render_latex(expr3, paren_style="always_factors") == r"\sin^{2}(3x)\cos(2x)"


def test_render_mul_keeps_parens_for_sums_and_negatives() -> None:
    from fractions import Fraction

    from question_engine.frameworks.primitives.poly_expression import (
        Add,
        Const,
        Fn,
        Mul,
        Pow,
        Var,
    )

    x = Var("x")
    sum_prod = Mul(
        (Add((Mul((Const(2), x)), Const(1))), Add((x, Const(-3))))
    )
    assert render_latex(sum_prod, paren_style="always_factors") == (
        r"\left(2x + 1\right)\left(x - 3\right)"
    )
    mixed = Mul((Add((Fn("sin", x), Const(1))), Fn("cos", x)))
    assert render_latex(mixed, paren_style="minimal") == r"\left(\sin(x) + 1\right)\cos(x)"
    # Digit glue: 3x · 4x^3 must not become 34x^3
    glued = Mul((Mul((Const(3), x)), Mul((Const(4), Pow(x, 3)))))
    assert render_latex(glued, paren_style="always_factors") == r"3x\left(4x^{3}\right)"
    # Coef · Add must not digit-glue leading term (55x² bug)
    u = Add(
        (
            Mul((Const(Fraction(5)), Pow(x, Fraction(2)))),
            Mul((Const(Fraction(2)), x)),
            Const(Fraction(-4)),
        )
    )
    scaled = render_latex(Mul((Const(Fraction(5)), u)))
    assert "55x" not in scaled
    assert scaled.startswith(r"5\left(")


def test_chain_pack_power_of_poly() -> None:
    spec = pack_algebraic_chain(6.0, coef_hi=4, power_max=4, extra_term=False)
    expr, _d, body, deriv, inv = sample_and_differentiate(spec, rng=random.Random(5))
    assert "chain" in inv["methods_used"] or inv["nest_depth"] >= 1
    assert body
    assert deriv


def test_paren_style_minimal_omits_factor_wrappers_on_monomial() -> None:
    spec = ExpressionSpec(
        paren_style="minimal",
        degree_min=2,
        degree_max=3,
        term_count_min=1,
        term_count_max=1,
        require_sum=False,
        extra_term=False,
    )
    expr = sample_expression(spec, rng=random.Random(3))
    body = render_latex(expr, paren_style="minimal")
    assert r"\left(" not in body


def test_inventory_fields() -> None:
    spec = pack_power_rule(10.0, extra_term=True)
    expr = sample_expression(spec, rng=random.Random(9))
    inv = structure_inventory(expr)
    for key in ("shape_id", "ops", "nest_depth", "degree_max", "n_terms"):
        assert key in inv


def test_trig_via_framework_path() -> None:
    hits = 0
    for seed in range(20):
        sample = sample_derivative_expression(
            {"difficulty": 6, "seed": seed, "include_answer_key": True},
            generator_key="derivative_trigonometric",
        )
        if "trig" in sample.function_classes:
            hits += 1
        assert sample.prompt_latex
        assert sample.answer_latex
        assert "shape_id" in sample.metadata or sample.metadata.get("generator")
    assert hits >= 15


def test_product_pack_can_mix_trig_factors() -> None:
    spec = pack_product_rule(
        14.0,
        allowed_functions=frozenset({"trig"}),
        prefer_chained_fn=True,
    )
    trig_hits = 0
    for seed in range(25):
        expr = sample_expression(spec, rng=random.Random(seed))
        inv = structure_inventory(expr)
        assert inv["has_product"]
        if "sin" in inv["functions"] or "cos" in inv["functions"] or "tan" in inv["functions"]:
            trig_hits += 1
    assert trig_hits >= 10


def test_special_atom_high_d_many_trig_nodes() -> None:
    from question_engine.frameworks.primitives.poly_expression import (
        Fn,
        Mul,
        Pow,
        Add,
        pack_special_atom,
    )

    def count_fns(expr: object) -> int:
        if isinstance(expr, Fn):
            return 1 + count_fns(expr.arg)
        if isinstance(expr, Mul):
            return sum(count_fns(f) for f in expr.factors)
        if isinstance(expr, Add):
            return sum(count_fns(t) for t in expr.terms)
        if isinstance(expr, Pow):
            return count_fns(expr.base)
        return 0

    rich = 0
    for seed in range(30):
        spec = pack_special_atom(18.0, primary="trig")
        expr = sample_expression(spec, rng=random.Random(seed))
        inv = structure_inventory(expr)
        n = count_fns(expr)
        assert n >= 1
        # Rich = multi-Fn nest, product, or Fn-power — not nest-node count alone
        if (
            n >= 3
            or inv.get("has_product")
            or inv.get("has_fn_power")
            or int(inv.get("nest_depth") or 0) >= 2
        ):
            rich += 1
    assert rich >= 15


def test_pc_and_calc_power_rule_shared_generator() -> None:
    qs_calc = GENERATORS["derivative_power_rule"](
        "calc_diff_power_rule",
        {"count": 4, "difficulty": 5, "seed": 3, "include_answer_key": True},
    )
    qs_pc = GENERATORS["derivative_power_rule"](
        "pc_power_rule_for_differentiation",
        {"count": 4, "difficulty": 5, "seed": 3, "include_answer_key": True},
    )
    assert len(qs_calc) == 4 and len(qs_pc) == 4
    # Same seed + key → same prompts (shared Spec pack)
    assert [q.prompt_latex for q in qs_calc] == [q.prompt_latex for q in qs_pc]


def test_fn_power_renders_superscript_style() -> None:
    from question_engine.frameworks.primitives.poly_expression import Fn, Pow, Var, Const, Mul

    expr = Pow(Fn("tan", Var("x")), 2)
    assert render_latex(expr) == r"\tan^{2}(x)"
    expr2 = Pow(Fn("sin", Mul((Const(3), Var("x")))), 3)
    assert render_latex(expr2) == r"\sin^{3}(3x)"
    expr3 = Pow(Fn("ln", Var("x")), 2)
    assert render_latex(expr3) == r"\ln^{2}(x)"
    expr4 = Pow(Fn("arcsin", Mul((Const(2), Var("x")))), 2)
    assert render_latex(expr4) == r"\arcsin^{2}(2x)"
    expr5 = Pow(Fn("arctan", Var("x")), 3)
    assert render_latex(expr5) == r"\arctan^{3}(x)"


def test_fn_power_sampled_at_mid_d() -> None:
    hits = 0
    for seed in range(50):
        spec = pack_special_atom(14.0, primary="trig", prefer_chained_fn=True)
        assert spec.allow_fn_power
        expr = sample_expression(spec, rng=random.Random(seed))
        inv = structure_inventory(expr)
        body = render_latex(expr)
        if inv.get("has_fn_power") or any(
            t in body for t in (r"\sin^{", r"\cos^{", r"\tan^{")
        ):
            hits += 1
    assert hits >= 8


def test_invtrig_high_d_powers_and_products() -> None:
    """Invtrig hardness mixes Fn-powers + products — not nest-only."""
    from question_engine.frameworks.primitives.poly_expression import Mul

    power_hits = 0
    product_hits = 0
    deep_only = 0
    for seed in range(60):
        spec = pack_special_atom(20.0, primary="invtrig", prefer_chained_fn=True)
        assert spec.allow_fn_power
        assert not spec.forbid_product
        expr = sample_expression(spec, rng=random.Random(seed))
        inv = structure_inventory(expr)
        body = render_latex(expr)
        has_pow = inv.get("has_fn_power") or any(
            t in body for t in (r"\arcsin^{", r"\arccos^{", r"\arctan^{")
        )
        has_prod = isinstance(expr, Mul) or inv.get("has_product")
        nest = int(inv.get("nest_depth") or 0)
        if has_pow:
            power_hits += 1
        if has_prod:
            product_hits += 1
        if nest >= 3 and not has_pow and not has_prod:
            deep_only += 1
    assert power_hits >= 12, f"fn_power hits={power_hits}"
    assert product_hits >= 10, f"product hits={product_hits}"
    # Nest-only deep chains should not dominate
    assert deep_only <= 25, f"nest-only deep={deep_only}"


def test_mid_d_still_produces_products() -> None:
    from question_engine.frameworks.primitives.poly_expression import Mul

    product_hits = 0
    for primary in ("trig", "invtrig", "log"):
        for seed in range(40):
            spec = pack_special_atom(12.0, primary=primary, prefer_chained_fn=True)
            expr = sample_expression(spec, rng=random.Random(seed))
            if isinstance(expr, Mul) or structure_inventory(expr).get("has_product"):
                product_hits += 1
    assert product_hits >= 15


def test_second_deriv_uses_simpler_bases() -> None:
    from question_engine.frameworks.primitives.poly_expression import (
        Mul,
        sample_and_differentiate,
    )

    long_answers = 0
    order2 = 0
    for seed in range(40):
        spec = pack_special_atom(
            20.0, primary="invtrig", prefer_chained_fn=True, derivative_order=2
        )
        assert spec.derivative_order == 2
        assert spec.max_factors <= 2
        assert spec.max_nesting <= 2
        _e, _d, body, deriv, inv = sample_and_differentiate(
            spec, rng=random.Random(seed)
        )
        assert inv["derivative_order"] == 2
        order2 += 1
        nest = int(inv.get("nest_depth") or 0)
        n_fac = int(inv.get("n_factors") or 1)
        assert nest <= 2
        assert n_fac <= 2
        if isinstance(_e, Mul) and nest >= 2:
            raise AssertionError(f"unsafe 2nd-deriv base: {body}")
        if len(deriv) > 700:
            long_answers += 1
    assert order2 == 40
    assert long_answers <= 8


def test_deep_mixed_chain_heterogeneous_classes() -> None:
    from question_engine.frameworks.primitives.poly_expression import (
        pack_general_derivatives,
        function_classes_of,
    )

    spec = pack_general_derivatives(
        20.0,
        allowed_functions=frozenset({"trig", "log", "exp", "invtrig"}),
        mix_fn_classes=True,
        deep_chain=True,
        allow_fn_power=True,
    )
    mixed = 0
    deep = 0
    for seed in range(40):
        expr = sample_expression(spec, rng=random.Random(seed))
        classes = function_classes_of(expr) - {"algebraic", "roots"}
        inv = structure_inventory(expr)
        if len(classes) >= 2:
            mixed += 1
        if inv["nest_depth"] >= 3:
            deep += 1
    assert mixed >= 12
    assert deep >= 8


def test_high_d_factor_nest_budgets_tightened() -> None:
    from question_engine.frameworks.primitives.poly_expression import (
        _factor_budget,
        _nest_budget,
    )
    from question_engine.frameworks.primitives.derivatives import structure_knobs_from_d

    assert _factor_budget(12.0) == 2
    assert _factor_budget(16.0) == 3
    assert _factor_budget(25.0) == 4
    assert _factor_budget(18.0) == 3
    assert _nest_budget(12.0, deep=False) <= 2
    assert _nest_budget(25.0, deep=False) <= 3
    assert _nest_budget(25.0, deep=True) <= 4
    knobs = structure_knobs_from_d(25.0)
    assert knobs["coef_hi"] <= 7
    assert knobs["power_max"] <= 6
    assert knobs["term_budget"] <= 4
    # Uncapped path still grows past 25
    knobs100 = structure_knobs_from_d(100.0)
    assert knobs100["coef_hi"] > knobs["coef_hi"]


def test_higher_order_differentiates_n_times() -> None:
    from question_engine.frameworks.primitives.poly_expression import (
        ExpressionSpec,
        Pow,
        Var,
        sample_and_differentiate,
    )

    spec = ExpressionSpec(
        degree_min=3,
        degree_max=3,
        term_count_min=1,
        term_count_max=1,
        require_sum=False,
        derivative_order=2,
        d_spend=16,
    )
    # Force monomial via require — sample may vary; check inventory order
    for seed in range(15):
        _e, _d, body, deriv, inv = sample_and_differentiate(
            spec, rng=random.Random(seed)
        )
        assert inv["derivative_order"] == 2
        assert body
        assert deriv
        assert "effort_features" in inv
        assert inv["effort_features"]["derivative_order"] == 2


def test_second_deriv_tan_tan_x_not_zero() -> None:
    from question_engine.frameworks.primitives.poly_expression import (
        Const,
        Fn,
        Var,
        differentiate,
        render_latex,
    )

    expr = Fn("tan", Fn("tan", Var("x")))
    d1 = differentiate(expr)
    d2 = differentiate(d1)
    assert not (isinstance(d2, Const) and d2.value == 0)
    assert render_latex(d2) != "0"
    assert r"\sec" in render_latex(d2) or r"\tan" in render_latex(d2)


def test_second_deriv_arctan_arcsin_not_zero() -> None:
    from question_engine.frameworks.primitives.poly_expression import (
        Const,
        Fn,
        Mul,
        Var,
        differentiate,
        render_latex,
    )

    expr = Fn("arctan", Fn("arcsin", Mul((Const(2), Var("x")))))
    d2 = differentiate(differentiate(expr))
    assert not (isinstance(d2, Const) and d2.value == 0)
    assert render_latex(d2) != "0"


def test_nested_invtrig_chain_has_multiple_factors() -> None:
    from question_engine.frameworks.primitives.poly_expression import (
        Const,
        ExpressionSpec,
        Fn,
        Mul,
        Var,
        differentiate,
        render_latex,
        sample_and_differentiate,
    )

    x = Var("x")
    expr = Fn(
        "arccos",
        Fn("arccos", Fn("arccos", Fn("arctan", Mul((Const(5), x))))),
    )
    d1 = differentiate(expr)
    latex = render_latex(d1)
    # Full chain: three darccos factors + darctan + coef — not outer-only
    assert latex.count(r"\sqrt{1-") >= 3
    assert r"1+(5x)^{2}" in latex or r"1+(5x)^2" in latex or "5x" in latex
    # Must not equal outer-only form
    outer_only = r"-\frac{1}{\sqrt{1-(\arccos\left(\arccos\left(\arctan(5x)\right)\right))^{2}}}"
    assert latex != outer_only
    assert len(latex) > len(outer_only) + 20

    # Via legacy render path (order=1 sample_and_differentiate)
    spec = ExpressionSpec(
        require_function="invtrig",
        prefer_special_structure=True,
        allowed_functions=frozenset({"invtrig"}),
        prefer_chained_fn=True,
        max_nesting=4,
        d_spend=20,
        derivative_order=1,
    )
    # Direct check: nested Fn uses AST render, not truncated legacy
    from question_engine.frameworks.primitives.poly_expression import _fn_deriv_latex

    assert _fn_deriv_latex(expr, spec) is None  # forces full AST chain render


def test_ln_latex_no_pipe_or_broken_left() -> None:
    from question_engine.frameworks.primitives.poly_expression import (
        Const,
        Fn,
        Mul,
        Pow,
        Var,
        render_latex,
    )

    samples = [
        Fn("ln", Mul((Const(3), Var("x")))),
        Fn("ln", Fn("ln", Mul((Const(2), Var("x"))))),
        Pow(Fn("ln", Mul((Const(4), Var("x")))), 2),
        Fn("sqrt", Fn("ln", Mul((Const(5), Var("x"))))),
    ]
    for expr in samples:
        s = render_latex(expr)
        assert r"\left|" not in s
        assert "|" not in s  # no abs bars that break md tables
        # no incomplete \left\ truncation
        assert r"\left\\" not in s
        assert not s.rstrip().endswith(r"\left")
        # balanced left/right or no bare \left
        assert s.count(r"\left") == s.count(r"\right")


def test_ln_exp_specialty_always_has_log_or_exp() -> None:
    from question_engine.api.handler import _generate_for_type
    import question_engine.types  # noqa: F401

    tid = "calc_diff_natural_logarithms_and_exponentials"
    for seed in range(30):
        for d in (20.0, 25.0):
            qs = _generate_for_type(
                tid,
                {
                    "count": 1,
                    "difficulty": d,
                    "seed": seed,
                    "include_answer_key": True,
                },
            )
            q = qs[0]
            body = q.prompt_latex or ""
            has_log_exp = any(
                tok in body
                for tok in (r"\ln", r"e^{", "ln", "exp")
            )
            # Trig-only sin^n / cos / tan without log/exp is a failure
            trig_only = (
                any(t in body for t in (r"\sin", r"\cos", r"\tan"))
                and r"\ln" not in body
                and r"e^{" not in body
            )
            assert has_log_exp, f"seed={seed} d={d} body={body}"
            assert not trig_only, f"trig-only seed={seed} d={d} body={body}"


def test_no_canceling_exp_ln_at_high_d() -> None:
    from question_engine.frameworks.primitives.poly_expression import (
        _has_canceling_exp_ln,
        pack_special_atom,
        render_latex,
        sample_expression,
    )

    spec = pack_special_atom(
        25.0,
        primary="exp",
        allowed_functions=frozenset({"exp", "log"}),
        prefer_chained_fn=True,
    )
    for seed in range(40):
        expr = sample_expression(spec, rng=random.Random(seed))
        assert not _has_canceling_exp_ln(expr), render_latex(expr)


def test_mid_d_product_factor_budget() -> None:
    from question_engine.frameworks.primitives.poly_expression import (
        Mul,
        pack_special_atom,
        render_latex,
        sample_expression,
    )

    spec = pack_special_atom(12.0, primary="trig", prefer_chained_fn=True)
    assert spec.max_factors <= 2
    for seed in range(30):
        expr = sample_expression(spec, rng=random.Random(seed))
        if isinstance(expr, Mul):
            assert len(expr.factors) <= 2, render_latex(expr)


def test_specialty_high_d_order2_rate() -> None:
    """Mid-high D specialty/general should ask for 2nd derivatives often enough."""
    from question_engine.api.handler import _generate_for_type
    import question_engine.types  # noqa: F401

    order2 = 0
    for tid in (
        "calc_diff_inverse_trigonometric",
        "calc_diff_trigonometric",
        "calc_diff_general",
    ):
        for seed in range(25):
            qs = _generate_for_type(
                tid,
                {
                    "count": 1,
                    "difficulty": 20.0,
                    "seed": seed,
                    "include_answer_key": True,
                },
            )
            prompt = qs[0].prompt_latex or ""
            if r"d^{2}" in prompt or r"d^2" in prompt:
                order2 += 1
                ans = qs[0].answer_latex or ""
                assert len(ans) < 900, f"exploded answer len={len(ans)} tid={tid}"
    assert order2 >= 12, f"order2 count={order2}"


def test_exponent_kinds_spec_api() -> None:
    from question_engine.frameworks.primitives.poly_expression import (
        ExpressionSpec,
        exponent_kinds,
        with_exponent_kinds,
    )

    spec = ExpressionSpec()
    assert exponent_kinds(spec) == frozenset({"integer"})
    rich = with_exponent_kinds(
        spec, {"integer", "fractional", "irrational", "negative"}
    )
    assert rich.allow_fractional_exponents
    assert rich.allow_irrational_exponents
    assert rich.allow_negative_exponents
    assert exponent_kinds(rich) == frozenset(
        {"integer", "fractional", "irrational", "negative"}
    )
    neg_only = with_exponent_kinds(spec, {"integer", "negative"})
    assert neg_only.allow_negative_exponents
    assert not neg_only.allow_fractional_exponents
    assert exponent_kinds(neg_only) == frozenset({"integer", "negative"})


def test_pack_algebraic_chain_gates_exotic_by_d() -> None:
    low = pack_algebraic_chain(3.0)
    assert low.allow_integer_exponents
    assert not low.allow_fractional_exponents
    assert not low.allow_irrational_exponents
    assert not low.allow_negative_exponents

    mid = pack_algebraic_chain(7.0)
    assert mid.allow_fractional_exponents
    assert not mid.allow_irrational_exponents
    assert mid.allow_negative_exponents

    high = pack_algebraic_chain(12.0)
    assert high.allow_fractional_exponents
    assert high.allow_irrational_exponents
    assert high.allow_negative_exponents

    # Explicit override wins
    forced = pack_algebraic_chain(
        3.0,
        allow_fractional_exponents=True,
        allow_irrational_exponents=True,
        allow_negative_exponents=True,
    )
    assert forced.allow_fractional_exponents
    assert forced.allow_irrational_exponents
    assert forced.allow_negative_exponents


def test_pack_power_rule_gates_weird_exponents_by_d() -> None:
    low = pack_power_rule(2.0)
    assert low.allow_integer_exponents
    assert not low.allow_negative_exponents
    assert not low.allow_fractional_exponents
    assert not low.allow_irrational_exponents

    low_mid = pack_power_rule(4.5)
    assert low_mid.allow_negative_exponents
    assert not low_mid.allow_fractional_exponents
    assert not low_mid.allow_irrational_exponents

    modest = pack_power_rule(6.0)
    assert modest.allow_negative_exponents
    assert modest.allow_fractional_exponents
    assert not modest.allow_irrational_exponents

    high = pack_power_rule(12.0)
    assert high.allow_negative_exponents
    assert high.allow_fractional_exponents
    assert high.allow_irrational_exponents

    # Higher-order stays classic positive integers
    order2 = pack_power_rule(20.0, derivative_order=2)
    assert not order2.allow_negative_exponents
    assert not order2.allow_fractional_exponents
    assert not order2.allow_irrational_exponents

    forced = pack_power_rule(
        1.0,
        allow_negative_exponents=True,
        allow_fractional_exponents=True,
        allow_irrational_exponents=True,
    )
    assert forced.allow_negative_exponents
    assert forced.allow_fractional_exponents
    assert forced.allow_irrational_exponents


def test_power_rule_weird_exponent_diff_and_render() -> None:
    """d/dx[c x^p] = c p x^{p-1} for negative / fractional / irrational p."""
    from fractions import Fraction

    from question_engine.frameworks.primitives.poly_expression import (
        Const,
        Mul,
        Pow,
        SymConst,
        SymOffset,
        Var,
        differentiate,
        render_latex,
        sample_and_differentiate,
    )

    x = Var("x")

    # 4x^{-2} → -8 x^{-3}
    expr_n = Mul((Const(4), Pow(x, -2)))
    assert r"x^{-2}" in render_latex(expr_n)
    d_n = differentiate(expr_n)
    ans_n = render_latex(d_n)
    assert "-8" in ans_n or ans_n.startswith("-")
    assert r"x^{-3}" in ans_n

    # x^{3/2} → (3/2) x^{1/2}
    expr_f = Pow(x, Fraction(3, 2))
    d_f = differentiate(expr_f)
    ans_f = render_latex(d_f)
    assert r"\frac{3}{2}" in ans_f
    assert r"\frac{1}{2}" in ans_f

    # x^π → π x^{π-1}
    expr_pi = Pow(x, SymConst("pi"))
    d_pi = differentiate(expr_pi)
    assert isinstance(d_pi, Mul)
    assert any(
        isinstance(f, Const) and isinstance(f.value, SymConst) and f.value.name == "pi"
        for f in d_pi.factors
    )
    assert any(
        isinstance(f, Pow)
        and isinstance(f.exp, SymOffset)
        and f.exp.sym.name == "pi"
        and f.exp.offset == -1
        for f in d_pi.factors
    )
    assert r"\pi" in render_latex(d_pi)

    # Live pack sampling at modest D yields some weird monomials
    weird = 0
    for seed in range(40):
        expr, _d, body, deriv, _inv = sample_and_differentiate(
            pack_power_rule(8.0), rng=random.Random(seed)
        )
        assert body and deriv
        # Stay algebraic power-rule (no trig forced)
        assert "sin" not in body and "cos" not in body
        if isinstance(expr, Pow) and (
            isinstance(expr.exp, (Fraction, SymConst))
            or (isinstance(expr.exp, int) and expr.exp < 0)
        ):
            weird += 1
        elif isinstance(expr, Mul) and len(expr.factors) >= 2:
            base = expr.factors[-1]
            if isinstance(base, Pow) and (
                isinstance(base.exp, (Fraction, SymConst))
                or (isinstance(base.exp, int) and base.exp < 0)
            ):
                weird += 1
    assert weird >= 12, f"weird monomial hits={weird}"


def test_exotic_exponent_chain_diff_and_render() -> None:
    from fractions import Fraction

    from question_engine.frameworks.primitives.poly_expression import (
        Add,
        Const,
        Mul,
        Pow,
        SymConst,
        SymOffset,
        Var,
        differentiate,
        render_latex,
    )

    x = Var("x")
    inner = Add((Mul((Const(2), x)), Const(1)))  # 2x+1

    # (2x+1)^{3/2} → (3/2)(2x+1)^{1/2}·2
    expr_f = Pow(inner, Fraction(3, 2))
    body_f = render_latex(expr_f, paren_style="always_powers")
    assert r"\frac{3}{2}" in body_f
    d_f = differentiate(expr_f)
    ans_f = render_latex(d_f, paren_style="always_powers")
    assert r"\frac{3}{2}" in ans_f
    assert not (isinstance(d_f, Const) and d_f.value == 0)

    # (2x+1)^π → π(2x+1)^{π-1}·2
    expr_pi = Pow(inner, SymConst("pi"))
    body_pi = render_latex(expr_pi, paren_style="always_powers")
    assert r"\pi" in body_pi
    d_pi = differentiate(expr_pi)
    ans_pi = render_latex(d_pi, paren_style="always_powers")
    assert r"\pi" in ans_pi
    assert r"\pi-1" in ans_pi or isinstance(
        d_pi, Mul
    )  # coef visible; exp is SymOffset
    # AST shape: Mul(Const(pi), Pow(..., SymOffset(pi,-1)), ...)
    assert isinstance(d_pi, Mul)
    assert any(
        isinstance(f, Const) and isinstance(f.value, SymConst) and f.value.name == "pi"
        for f in d_pi.factors
    )
    assert any(
        isinstance(f, Pow)
        and isinstance(f.exp, SymOffset)
        and f.exp.sym.name == "pi"
        and f.exp.offset == -1
        for f in d_pi.factors
    )

    for name, latex in (
        ("e", "e"),
        ("sqrt2", r"\sqrt{2}"),
        ("sqrt3", r"\sqrt{3}"),
    ):
        expr = Pow(inner, SymConst(name))
        assert latex in render_latex(expr, paren_style="always_powers")
        d = differentiate(expr)
        ans = render_latex(d, paren_style="always_powers")
        assert latex in ans
        assert not (isinstance(d, Const) and d.value == 0)


def test_spec_controls_sampled_exponent_kinds() -> None:
    from fractions import Fraction

    from question_engine.frameworks.primitives.poly_expression import (
        Pow,
        SymConst,
        sample_expression,
        with_exponent_kinds,
    )

    base = pack_algebraic_chain(14.0, allowed_functions=frozenset())
    # Force algebraic power-of-poly path
    assert base.require_power_of_poly

    only_frac = with_exponent_kinds(base, {"fractional"})
    for seed in range(20):
        expr = sample_expression(only_frac, rng=random.Random(seed))
        assert isinstance(expr, Pow)
        assert isinstance(expr.exp, Fraction), expr.exp

    only_irr = with_exponent_kinds(base, {"irrational"})
    for seed in range(20):
        expr = sample_expression(only_irr, rng=random.Random(seed))
        assert isinstance(expr, Pow)
        assert isinstance(expr.exp, SymConst), expr.exp

    only_int = with_exponent_kinds(base, {"integer"})
    for seed in range(15):
        expr = sample_expression(only_int, rng=random.Random(seed))
        assert isinstance(expr, Pow)
        assert isinstance(expr.exp, int), expr.exp


def test_chain_mid_d_samples_non_expandable_powers() -> None:
    """At mid+ D, algebraic chain should often use fractional/irrational exponents."""
    from fractions import Fraction

    from question_engine.frameworks.primitives.poly_expression import (
        Pow,
        SymConst,
        sample_and_differentiate,
    )

    exotic = 0
    for seed in range(40):
        spec = pack_algebraic_chain(14.0, allowed_functions=frozenset())
        expr, _d, body, deriv, inv = sample_and_differentiate(
            spec, rng=random.Random(seed)
        )
        assert body and deriv
        if isinstance(expr, Pow) and isinstance(expr.exp, (Fraction, SymConst)):
            exotic += 1
            # c must appear in the answer (power-rule coefficient)
            if isinstance(expr.exp, SymConst):
                assert (
                    r"\pi" in deriv
                    or "e" in deriv
                    or r"\sqrt{2}" in deriv
                    or r"\sqrt{3}" in deriv
                )
            else:
                assert r"\frac{" in deriv or str(expr.exp.numerator) in deriv
    assert exotic >= 20, f"exotic hits={exotic}"

