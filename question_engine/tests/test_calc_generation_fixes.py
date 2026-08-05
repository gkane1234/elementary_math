"""Calc generation fixes: D=0 basics, no cost_pad, structural high-D, shortfall honesty."""

from __future__ import annotations

import random
import re

from question_engine.frameworks.primitives.complexity_wrap import (
    CoreExpr,
    complexity_wrap,
    render_core_expr,
)
from question_engine.frameworks.primitives.derivatives import sample_derivative_expression
from question_engine.frameworks.primitives.integrals import sample_integral_expression
from question_engine.frameworks.primitives.limits import sample_limit_expression


def _assert_no_cost_pad(meta: dict) -> None:
    wraps = meta.get("wrappers_applied") or []
    costs = meta.get("difficulty_costs") or []
    assert "cost_pad" not in wraps
    assert all(c.get("feature") != "cost_pad" for c in costs)


def test_d0_quotient_is_basic_near_zero_cost() -> None:
    for seed in range(25):
        sample = sample_derivative_expression(
            {"difficulty": 0, "seed": seed, "include_answer_key": True},
            generator_key="derivative_quotient_rule",
        )
        assert sample.metadata.get("form_id") == "quotient_poly"
        assert float(sample.metadata.get("difficulty_cost_total") if sample.metadata.get("difficulty_cost_total") is not None else 99) <= 1.0
        body = sample.prompt_latex
        assert r"\sin" not in body and r"\cos" not in body
        assert r"e^{" not in body and r"\ln" not in body
        assert not re.search(r"x\^\{[3-9]", body)
        _assert_no_cost_pad(sample.metadata)


def test_no_cost_pad_across_leaves() -> None:
    leaves = [
        ("derivative_power_rule", sample_derivative_expression),
        ("derivative_product_rule", sample_derivative_expression),
        ("derivative_quotient_rule", sample_derivative_expression),
        ("limit_jump", sample_limit_expression),
        ("limit_continuity", sample_limit_expression),
        ("limit_essential", sample_limit_expression),
        ("limit_removable", sample_limit_expression),
        ("limit_direct_evaluation", sample_limit_expression),
        ("integral_power_rule", sample_integral_expression),
        ("first_fundamental_theorem", sample_integral_expression),
        ("integration_by_parts", sample_integral_expression),
    ]
    for key, sampler in leaves:
        for seed in range(12):
            sample = sampler(
                {"difficulty": 12, "seed": seed, "include_answer_key": True},
                generator_key=key,
            )
            meta = sample.metadata
            _assert_no_cost_pad(meta)
            total = float(meta.get("difficulty_cost_total") or 0)
            shortfall = meta.get("difficulty_shortfall")
            if total + 1e-9 < 12.0:
                assert shortfall is not None and float(shortfall) > 0, (
                    f"{key} seed={seed} under target without shortfall "
                    f"total={total} costs={meta.get('difficulty_costs')}"
                )
            else:
                assert shortfall is None or float(shortfall) <= 1e-9


def test_jump_d0_basic_near_zero_cost() -> None:
    for seed in range(20):
        sample = sample_limit_expression(
            {"difficulty": 0, "seed": seed, "include_answer_key": True},
            generator_key="limit_jump",
        )
        meta = sample.metadata
        assert meta.get("left_kind") == "const" and meta.get("right_kind") == "const"
        total = meta.get("difficulty_cost_total")
        assert total is not None and float(total) <= 1.0
        _assert_no_cost_pad(meta)
        assert meta.get("difficulty_shortfall") is None


def test_jump_d12_structural_difference() -> None:
    """High D must change piecewise structure — not pad, not const||const forever."""
    for seed in range(30):
        sample = sample_limit_expression(
            {"difficulty": 12, "seed": seed, "include_answer_key": True},
            generator_key="limit_jump",
        )
        meta = sample.metadata
        _assert_no_cost_pad(meta)
        kinds = {meta.get("left_kind"), meta.get("right_kind")}
        wraps = list(meta.get("wrappers_applied") or [])
        structural = bool(kinds - {"const"}) or any(
            str(w).startswith("jump_") for w in wraps
        ) or int(meta.get("n_pieces") or 2) >= 3
        assert structural, f"seed={seed} still const||const kinds={kinds} wraps={wraps}"
        # Prompt must look different from a bare const||const cases block
        assert "begin{cases}" in sample.prompt_latex
        total = float(meta.get("difficulty_cost_total") or 0)
        if total + 1e-9 < 12.0:
            assert float(meta.get("difficulty_shortfall") or 0) > 0


def test_cancel_factor_not_identical_top_bottom() -> None:
    for seed in range(40):
        rng = random.Random(seed)
        core = CoreExpr(kind="rational_pow", var="x", coef=1, power=1, center=0, approach=0)
        core = complexity_wrap(
            core,
            14.0,
            rng,
            allowed=("cancel_factor", "sign", "constant_multiple", "unfactored_form"),
        )
        if "cancel_factor" not in (core.wrappers_applied or []):
            continue
        body = render_core_expr(core)
        assert core.hole is not None
        if r"\frac{" not in body:
            continue
        inner = body.split(r"\frac{", 1)[1]
        depth = 0
        split_at = None
        for i, ch in enumerate(inner):
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0 and i + 1 < len(inner) and inner[i + 1] == "{":
                    split_at = i
                    break
        if split_at is None:
            continue
        num = inner[: split_at + 1]
        den = inner[split_at + 1 :]
        hole = int(core.hole)
        if hole == 0:
            fac = "x"
        elif hole > 0:
            fac = f"(x-{hole})"
        else:
            fac = f"(x+{-hole})"
        if fac in num and fac in den:
            raise AssertionError(f"identical cancel factor {fac} in {body}")
    hits = 0
    for seed in range(60):
        rng = random.Random(1000 + seed)
        core = CoreExpr(kind="rational_pow", var="x", coef=1, power=1, center=2, approach=2)
        core = complexity_wrap(
            core,
            16.0,
            rng,
            allowed=("cancel_factor",),
        )
        if "cancel_factor" in (core.wrappers_applied or []):
            hits += 1
            body = render_core_expr(core)
            assert "x^{2}" in body or "-" in body
    assert hits >= 5


def test_removable_linear_factor_not_identical() -> None:
    for seed in range(20):
        sample = sample_limit_expression(
            {
                "difficulty": 6,
                "seed": seed,
                "require_removable": True,
                "allow_removable": True,
            },
            generator_key="limit_removable",
        )
        _assert_no_cost_pad(sample.metadata)
        if sample.metadata.get("variant") != "linear_factor":
            continue
        prompt = sample.prompt_latex
        assert ")(" not in prompt or prompt.count("(x-") <= 1


def test_removable_high_d_expanded_not_scale_stack() -> None:
    scale_stacks = 0
    factor_samples = 0
    expanded_factors = 0
    for seed in range(25):
        sample = sample_limit_expression(
            {"difficulty": 14, "seed": seed, "include_answer_key": True},
            generator_key="limit_removable",
        )
        meta = sample.metadata
        _assert_no_cost_pad(meta)
        wraps = [str(w).split("#", 1)[0] for w in (meta.get("wrappers_applied") or [])]
        if wraps.count("constant_multiple") > 1:
            scale_stacks += 1
        variant = str(meta.get("variant") or meta.get("form_id") or "")
        if "rationalize" in variant:
            continue
        factor_samples += 1
        if "removable_expand" in wraps or "removable_extra_factor" in wraps:
            expanded_factors += 1
        elif "x^{3}" in sample.prompt_latex or "x^{2}" in sample.prompt_latex:
            expanded_factors += 1
    assert scale_stacks == 0
    assert factor_samples >= 1
    # Factor removers at high D should use expanded presentations (not scale stacks)
    assert expanded_factors >= max(1, factor_samples // 2)


def test_triple_product_gated_by_setting() -> None:
    blocked = 0
    allowed = 0
    for seed in range(40):
        off = sample_derivative_expression(
            {
                "difficulty": 20,
                "seed": seed,
                "allow_triple_product": False,
                "require_product": True,
                "include_answer_key": True,
            },
            generator_key="derivative_product_rule",
        )
        n_off = int(off.metadata.get("n_factors") or 0)
        assert n_off <= 2
        blocked += 1

        on = sample_derivative_expression(
            {
                "difficulty": 20,
                "seed": seed,
                "allow_triple_product": True,
                "require_product": True,
                "include_answer_key": True,
            },
            generator_key="derivative_product_rule",
        )
        if int(on.metadata.get("n_factors") or 0) >= 3:
            allowed += 1
    assert blocked == 40
    assert allowed >= 8
