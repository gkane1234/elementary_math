"""Evaluate algebraic expressions — Layer 1 on numbers + variables.

Linear path uses the shared ``expression_structure`` engine (same DNA as OOO
and expand/simplify). Polynomial path samples sparse univariate polys.

Difficulty ``D`` drives leaf / nest / scale budgets via the shared engine::

    n_terms ≈ 1 + floor(log2(1 + D / 1.5))
    nest    ≈ floor(log2(1 + D / 3))
    × unlocks at D≥2, ÷ at D≥4
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from question_engine.frameworks.niceness import NicenessError
from question_engine.frameworks.primitives._algebra_render import (
    coeff_times_var,
    num_latex,
)
from question_engine.frameworks.primitives.expression_structure import (
    DIV_UNLOCK,
    LEAF_SCALE,
    MUL_UNLOCK,
    NEST_SCALE as PAREN_SCALE,
    SCALE_OP_SCALE,
    op_pool_for_d as _struct_op_pool,
    sample_structured_expression,
    target_n_leaves,
    target_nest_budget,
    target_scale_budget,
)
from question_engine.frameworks.primitives.poly_helpers import (
    evaluate_poly,
    render_poly,
    sample_poly_coeffs,
    target_poly_degree,
)
from question_engine.frameworks.primitives.registry import PRIM_EVALUATE, PrimitiveContext

EVALUATE_SETTINGS_SCHEMA: dict[str, Any] = {}

TERM_SCALE = LEAF_SCALE


def target_n_terms(d: float) -> int:
    return target_n_leaves(d)


def target_n_parens(d: float) -> int:
    return target_nest_budget(d)


def target_n_scale(d: float) -> int:
    return target_scale_budget(d)


def op_pool_for_d(d: float) -> tuple[str, ...]:
    return _struct_op_pool(d, mode="algebraic", allow_exponent=False)


def min_d_for_n_terms(n: int) -> float:
    n = max(1, int(n))
    if n <= 1:
        return 0.0
    return TERM_SCALE * (2 ** (n - 1) - 1)


@dataclass(frozen=True)
class EvaluateExpression:
    latex: str
    text: str
    value_latex: str
    value: Fraction
    var_name: str
    var_latex: str
    subst_latex: str
    subst_value: Fraction
    coeff_a: Fraction
    coeff_b: Fraction
    n_terms: int
    n_parens: int
    nest_depth: int
    n_ops: int
    op_pool: tuple[str, ...]
    upgrades: tuple[str, ...]
    effective_d: float
    max_degree: int = 1


def sample_evaluate_expression(ctx: PrimitiveContext) -> EvaluateExpression:
    """Sample an evaluate item (affine under linear policy; poly under poly policy)."""
    eff = ctx.effective_d(PRIM_EVALUATE)
    if ctx.policy.max_degree >= 2:
        for _ in range(12):
            try:
                return _build_poly(ctx, eff)
            except (NicenessError, ValueError, ZeroDivisionError):
                continue
    for _ in range(12):
        try:
            return _build(ctx, eff)
        except (NicenessError, ValueError, ZeroDivisionError):
            continue
    return _build_fallback(ctx, eff)


def sample_evaluate_linear_expression(ctx: PrimitiveContext) -> EvaluateExpression:
    return sample_evaluate_expression(ctx)


def _build_fallback(ctx: PrimitiveContext, eff: float) -> EvaluateExpression:
    var = ctx.sample_variable()
    subst = ctx.sample_number()
    a = Fraction(ctx.rng.choice([1, 2, 3, -1, -2]))
    latex = coeff_times_var(a, var.latex)
    text = coeff_times_var(a, var.name)
    total = a * subst.value
    return EvaluateExpression(
        latex=latex,
        text=text,
        value_latex=num_latex(total),
        value=total,
        var_name=var.name,
        var_latex=var.latex,
        subst_latex=num_latex(subst.value),
        subst_value=subst.value,
        coeff_a=a,
        coeff_b=Fraction(0),
        n_terms=1,
        n_parens=0,
        nest_depth=0,
        n_ops=0,
        op_pool=op_pool_for_d(eff),
        upgrades=("fallback",),
        effective_d=eff,
        max_degree=1,
    )


def _build_poly(ctx: PrimitiveContext, eff: float) -> EvaluateExpression:
    deg = target_poly_degree(eff, ctx.policy)
    ctx.policy.assert_degree(deg, where="evaluate.poly")
    var = ctx.sample_variable()
    subst = ctx.sample_number()
    if subst.value.denominator != 1 or abs(subst.value) > 6:
        subst_val = Fraction(ctx.rng.randint(-4, 4))
        if subst_val == 0 and ctx.rng.random() < 0.5:
            subst_val = Fraction(ctx.rng.choice([-2, -1, 1, 2, 3]))
    else:
        subst_val = subst.value

    n_terms = min(deg + 1, max(2, target_n_terms(eff)))
    coeffs = sample_poly_coeffs(ctx, degree=deg, n_terms=n_terms, require_leading=True)
    used_deg = max((d for d, c in coeffs.items() if c != 0), default=0)
    latex, text = render_poly(coeffs, var, descending=True)
    total = evaluate_poly(coeffs, subst_val)
    tags = [f"terms:{len([c for c in coeffs.values() if c != 0])}", f"degree:{used_deg}"]
    return EvaluateExpression(
        latex=latex,
        text=text,
        value_latex=num_latex(total),
        value=total,
        var_name=var.name,
        var_latex=var.latex,
        subst_latex=num_latex(subst_val),
        subst_value=subst_val,
        coeff_a=coeffs.get(1, Fraction(0)),
        coeff_b=coeffs.get(0, Fraction(0)),
        n_terms=len([c for c in coeffs.values() if c != 0]),
        n_parens=0,
        nest_depth=0,
        n_ops=max(0, len(coeffs) - 1),
        op_pool=("+", "-"),
        upgrades=tuple(tags),
        effective_d=eff,
        max_degree=used_deg,
    )


def _build(ctx: PrimitiveContext, eff: float) -> EvaluateExpression:
    """Answer-first: seed affine target, constructive inflate, then substitute."""
    from question_engine.frameworks.primitives.constructive import (
        construct_affine,
        seed_affine_target,
        verify_affine,
    )

    pool = op_pool_for_d(eff)
    var = ctx.sample_variable()
    subst = ctx.sample_number()
    tgt = seed_affine_target(ctx, force_var=True)
    surface = construct_affine(ctx, d=eff, var=var, target=tgt, prefer_distribute=True)
    assert surface.coeff_a is not None and surface.coeff_b is not None
    assert verify_affine(surface, tgt)
    total = surface.coeff_a * subst.value + surface.coeff_b
    nest = surface.latex.count("(")
    return EvaluateExpression(
        latex=surface.latex,
        text=surface.text,
        value_latex=num_latex(total),
        value=total,
        var_name=var.name,
        var_latex=var.latex,
        subst_latex=num_latex(subst.value),
        subst_value=subst.value,
        coeff_a=surface.coeff_a,
        coeff_b=surface.coeff_b,
        n_terms=max(1, (1 if surface.coeff_a else 0) + (1 if surface.coeff_b else 0)),
        n_parens=nest,
        nest_depth=max(1, nest),
        n_ops=max(0, len(surface.inflators_applied) - 1),
        op_pool=pool,
        upgrades=surface.inflators_applied,
        effective_d=eff,
        max_degree=1,
    )
