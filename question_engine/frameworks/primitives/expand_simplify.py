"""Expand then simplify — Layer 1+ on the shared expression-structure engine.

Under **linear** policy: samples unsimplified affine expressions via
``sample_structured_expression(..., prefer_distribute=True)`` (constant ×
groups, nesting, lone constants). Under **polynomial** policy: FOIL / products
capped by ``target_poly_degree``.

Difficulty ``D`` drives leaf / nest / scale budgets in the shared engine
(same DNA as OOO numeric and evaluate algebraic). Answer = fully simplified
linear (or poly) expression.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from question_engine.frameworks.niceness import NicenessError
from question_engine.frameworks.primitives._algebra_render import (
    num_latex,
)
from question_engine.frameworks.primitives.expression_structure import (
    LEAF_SCALE,
    append_constant_to_expression,
    sample_structured_expression,
    target_n_leaves,
    target_nest_budget,
)
from question_engine.frameworks.primitives.poly_helpers import (
    multiply_coeffs,
    render_poly,
    target_poly_degree,
    wrap_parens,
)
from question_engine.frameworks.primitives.registry import (
    PRIM_EXPAND_SIMPLIFY,
    PrimitiveContext,
)
from question_engine.frameworks.primitives.variables import SampledVariable

EXPAND_SIMPLIFY_SETTINGS_SCHEMA: dict[str, Any] = {}

# Compat aliases for tests / audits that still reference group/nest formulas.
GROUP_SCALE = LEAF_SCALE
LONE_SCALE = 3.0
NEST_SCALE = 4.0  # legacy nest_extra scale (tests); structure uses STRUCT_NEST_SCALE


def target_n_groups(d: float) -> int:
    """Compat: group count ≈ leaf budget under distribute style."""
    return target_n_leaves(d)


def target_n_lone(d: float) -> int:
    d = max(0.0, float(d))
    return int(math.floor(math.log2(1.0 + d / LONE_SCALE)))


def target_nest_extra(d: float) -> int:
    """Extra nest depth: ``floor(log2(1 + D / NEST_SCALE))`` with NEST_SCALE=4."""
    d = max(0.0, float(d))
    return int(math.floor(math.log2(1.0 + d / NEST_SCALE)))


def min_d_for_n_groups(n: int) -> float:
    n = max(1, int(n))
    if n <= 1:
        return 0.0
    return GROUP_SCALE * (2 ** (n - 1) - 1)


def min_d_for_nest_extra(e: int) -> float:
    e = max(0, int(e))
    if e <= 0:
        return 0.0
    return NEST_SCALE * (2**e - 1)


@dataclass(frozen=True)
class ExpandSimplifyExpression:
    latex: str
    text: str
    simplified_latex: str
    simplified_text: str
    coeff_a: Fraction
    coeff_b: Fraction
    n_groups: int
    n_lone: int
    nested: bool
    nest_depth: int
    upgrades: tuple[str, ...]
    effective_d: float
    max_degree: int = 1
    coeffs: tuple[tuple[int, str], ...] = ()


def sample_expand_simplify(ctx: PrimitiveContext) -> ExpandSimplifyExpression:
    eff = ctx.effective_d(PRIM_EXPAND_SIMPLIFY)
    for _ in range(12):
        try:
            if ctx.policy.max_degree >= 2 and ctx.policy.allow_var_var_product:
                return _build_poly(ctx, eff)
            return sample_linear_expression_to_simplify(ctx, d=eff)
        except (NicenessError, ValueError, ZeroDivisionError):
            continue
    if ctx.policy.max_degree >= 2 and ctx.policy.allow_var_var_product:
        try:
            return _build_poly(ctx, eff)
        except (NicenessError, ValueError, ZeroDivisionError):
            pass
    return sample_linear_expression_to_simplify(ctx, d=eff)


def sample_linear_expression_to_simplify(
    ctx: PrimitiveContext,
    *,
    d: float | None = None,
    var: SampledVariable | None = None,
    min_inflators: int = 1,
) -> ExpandSimplifyExpression:
    """Shared linear expand/simplify — answer-first constructive (seed affine, inflate).

    Cancel clutter is available on ``construct_affine`` via
    ``ExpressionScope.allow_cancel_clutter``; this topic leaves it off for now.
    """
    from question_engine.frameworks.primitives.constructive import (
        construct_affine,
        verify_affine,
    )

    eff = float(ctx.effective_d(PRIM_EXPAND_SIMPLIFY) if d is None else d)
    surface = construct_affine(
        ctx,
        d=eff,
        var=var,
        prefer_distribute=True,
        min_inflators=max(0, int(min_inflators)),
    )
    assert surface.coeff_a is not None and surface.coeff_b is not None
    assert verify_affine(surface, surface.target)
    nested = "distribute" in "".join(surface.inflators_applied)
    n_groups = max(1, sum(1 for u in surface.inflators_applied if "distribute" in u))
    return ExpandSimplifyExpression(
        latex=surface.latex,
        text=surface.text,
        simplified_latex=surface.simplified_latex or "",
        simplified_text=surface.simplified_text or "",
        coeff_a=surface.coeff_a,
        coeff_b=surface.coeff_b,
        n_groups=n_groups,
        n_lone=1 if surface.coeff_b != 0 else 0,
        nested=nested,
        nest_depth=2 if nested else 1,
        upgrades=surface.inflators_applied,
        effective_d=eff,
        max_degree=1,
    )


# Re-export for equations / inequalities.
__all__ = [
    "EXPAND_SIMPLIFY_SETTINGS_SCHEMA",
    "ExpandSimplifyExpression",
    "GROUP_SCALE",
    "LONE_SCALE",
    "NEST_SCALE",
    "append_constant_to_expression",
    "min_d_for_n_groups",
    "min_d_for_nest_extra",
    "sample_expand_simplify",
    "sample_linear_expression_to_simplify",
    "target_n_groups",
    "target_n_lone",
    "target_nest_extra",
]


def _nonzero_int(ctx: PrimitiveContext, *, prefer_abs_ge_2: bool = False) -> Fraction:
    from question_engine.frameworks.primitives._algebra_render import sample_integerish

    n = sample_integerish(ctx, exclude_zero=True)
    v = n.value
    if prefer_abs_ge_2 and abs(v) == 1 and ctx.rng.random() < 0.55:
        v = Fraction(ctx.rng.choice([2, 3, 4, 5]) * (1 if v > 0 else -1))
    return v


def _signed_int(ctx: PrimitiveContext, *, exclude_zero: bool = False) -> Fraction:
    from question_engine.frameworks.primitives._algebra_render import sample_integerish

    return sample_integerish(ctx, exclude_zero=exclude_zero).value


def _linear_factor_coeffs(ctx: PrimitiveContext) -> dict[int, Fraction]:
    a = _nonzero_int(ctx)
    b = _signed_int(ctx, exclude_zero=False)
    return {1: a, 0: b}


def _render_factor(coeffs: dict[int, Fraction], var: SampledVariable) -> tuple[str, str]:
    latex, text = render_poly(coeffs, var, descending=True)
    return wrap_parens(latex, text)


def _build_poly(ctx: PrimitiveContext, eff: float) -> ExpandSimplifyExpression:
    """Poly expand: FOIL / product of linear factors + optional constant scales."""
    deg_cap = target_poly_degree(eff, ctx.policy)
    ctx.policy.assert_degree(min(deg_cap, ctx.policy.max_degree), where="expand_simplify.poly")
    var = ctx.sample_variable()

    n_factors = 2
    if deg_cap >= 3 and eff >= 6.0 and ctx.rng.random() < 0.45:
        n_factors = 3
    while n_factors > 1 and n_factors > deg_cap:
        n_factors -= 1
    n_factors = max(2, min(n_factors, deg_cap))

    factors = [_linear_factor_coeffs(ctx) for _ in range(n_factors)]
    if n_factors > ctx.policy.max_degree:
        n_factors = ctx.policy.max_degree
        factors = factors[:n_factors]

    product: dict[int, Fraction] = {0: Fraction(1)}
    for f in factors:
        product = multiply_coeffs(product, f)
    used_deg = max(product.keys()) if product else 0
    ctx.policy.assert_degree(used_deg, where="expand_simplify.product")

    scale = Fraction(1)
    if eff >= 2.0 and ctx.rng.random() < 0.4:
        scale = _nonzero_int(ctx, prefer_abs_ge_2=True)
        product = {d: c * scale for d, c in product.items()}

    n_lone = target_n_lone(eff)
    lone_total = Fraction(0)
    lone_parts: list[tuple[str, str]] = []
    for _ in range(n_lone):
        c = _signed_int(ctx, exclude_zero=True)
        lone_total += c
        lone_parts.append((num_latex(c), num_latex(c)))
    if lone_total:
        product[0] = product.get(0, Fraction(0)) + lone_total
        product = {d: c for d, c in product.items() if c != 0}

    display_parts: list[tuple[str, str]] = []
    for f in factors:
        display_parts.append(_render_factor(f, var))
    latex = "".join(p[0] for p in display_parts)
    text = "".join(p[1] for p in display_parts)
    if scale != 1:
        latex = f"{num_latex(scale)}{latex}"
        text = f"{num_latex(scale)}{text}"
    for pl, pt in lone_parts:
        if pl.startswith("-"):
            latex = f"{latex} - {pl[1:]}"
            text = f"{text} - {pt[1:]}"
        else:
            latex = f"{latex} + {pl}"
            text = f"{text} + {pt}"

    simp_l, simp_t = render_poly(product, var, descending=True)
    coeff_a = product.get(1, Fraction(0))
    coeff_b = product.get(0, Fraction(0))
    tags = [f"factors:{n_factors}", f"degree:{used_deg}", f"lone:{n_lone}"]
    if scale != 1:
        tags.append("scaled")

    return ExpandSimplifyExpression(
        latex=latex,
        text=text,
        simplified_latex=simp_l,
        simplified_text=simp_t,
        coeff_a=coeff_a,
        coeff_b=coeff_b,
        n_groups=n_factors,
        n_lone=n_lone,
        nested=False,
        nest_depth=1,
        upgrades=tuple(tags),
        effective_d=eff,
        max_degree=used_deg,
        coeffs=tuple((d, str(product[d])) for d in sorted(product.keys(), reverse=True)),
    )
