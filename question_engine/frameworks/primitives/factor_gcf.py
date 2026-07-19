"""Factor GCF / reverse distributive — Layer 1 on numbers + variables.

Under ``ExpressionPolicy.max_degree=1`` (linear leaves), never emit ``x^2``:
``variable_gcf`` is blocked and ``three_terms`` stays affine (optional 2nd var).
Poly policy may re-enable higher-degree forms later.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from question_engine.frameworks.difficulty_budget import DifficultyFactor, select_upgrades
from question_engine.frameworks.niceness import NicenessError
from question_engine.frameworks.primitives._algebra_render import (
    coeff_times_var,
    join_signed_terms,
    num_latex,
)
from question_engine.frameworks.primitives.registry import PRIM_FACTOR_GCF, PrimitiveContext

FACTOR_GCF_SETTINGS_SCHEMA: dict[str, Any] = {}

_UPGRADES: tuple[DifficultyFactor, ...] = (
    DifficultyFactor("three_terms", 1.5, ("structure",)),
    DifficultyFactor("signed_terms", 1.0, ("structure",)),
    DifficultyFactor("variable_gcf", 2.5, ("structure",)),
)


@dataclass(frozen=True)
class FactorGcfExpression:
    latex: str
    text: str
    factored_latex: str
    factored_text: str
    gcf_latex: str
    upgrades: tuple[str, ...]
    effective_d: float
    max_degree: int = 1


def sample_factor_gcf(ctx: PrimitiveContext) -> FactorGcfExpression:
    eff = ctx.effective_d(PRIM_FACTOR_GCF)
    purchased, _, _ = select_upgrades(_UPGRADES, eff, rng=ctx.rng)
    ids = {f.id for f in purchased}
    # Policy gates degree-raising upgrades (D never buys degree on linear).
    ids = {i for i in ids if ctx.policy.allows_upgrade(i)}
    if ctx.policy.max_degree <= 1:
        ids.discard("variable_gcf")

    for _ in range(12):
        try:
            return _build(ctx, ids, eff)
        except (NicenessError, ValueError):
            if not ids:
                break
            costs = {f.id: f.cost for f in _UPGRADES}
            drop = max(ids, key=lambda i: costs.get(i, 0))
            ids.remove(drop)
            ctx.note_degraded(drop)

    return _build(ctx, set(), eff)


def _coprime_inners(rng, n: int, *, allow_neg: bool, span: int) -> list[int]:
    """Draw n nonzero integers whose gcd is 1."""
    for _ in range(40):
        vals = []
        for _i in range(n):
            k = rng.randint(1, span)
            if allow_neg and rng.random() < 0.35:
                k = -k
            vals.append(k)
        g = abs(vals[0])
        for v in vals[1:]:
            g = math.gcd(g, abs(v))
        if g == 1:
            return vals
        vals = [v // g for v in vals]
        if all(v != 0 for v in vals):
            return vals
    return ([2, 3, 1] if n >= 3 else [2, 3])[:n]


def _build(ctx: PrimitiveContext, ids: set[str], eff: float) -> FactorGcfExpression:
    var = ctx.sample_variable()
    g = ctx.rng.randint(2, max(3, min(12, 2 + int(eff))))
    n_terms = 3 if "three_terms" in ids else 2
    allow_neg = "signed_terms" in ids
    span = max(2, min(8, 2 + int(eff // 2)))
    inners = _coprime_inners(ctx.rng, n_terms, allow_neg=allow_neg, span=span)
    linear = ctx.policy.max_degree <= 1

    if "variable_gcf" in ids and not linear:
        return _with_variable_gcf(ctx, ids, eff, var, g, inners)

    # Numeric GCF:
    # Linear / deg≤1:
    #   2-term: g(ax + b) → ga x + gb
    #   3-term: g(ax + by + c) or g(ax + b + c) — never x^2
    # Poly (max_degree≥2):
    #   3-term: g(ax^2 + bx + c)
    if n_terms == 2:
        a, b = inners[0], inners[1]
        display = [
            (Fraction(g * a), var.latex),
            (Fraction(g * b), ""),
        ]
        inner_parts = [(Fraction(a), var.latex), (Fraction(b), "")]
        deg = 1
    elif linear:
        a, b, c = inners[0], inners[1], inners[2]
        y_var = None
        if ctx.policy.max_variables >= 2 and ctx.rng.random() < 0.55:
            for _ in range(6):
                y_var = ctx.sample_variable()
                if y_var.name != var.name:
                    break
            if y_var is not None and y_var.name == var.name:
                y_var = None
        if y_var is not None:
            display = [
                (Fraction(g * a), var.latex),
                (Fraction(g * b), y_var.latex),
                (Fraction(g * c), ""),
            ]
            inner_parts = [
                (Fraction(a), var.latex),
                (Fraction(b), y_var.latex),
                (Fraction(c), ""),
            ]
        else:
            # Three affine terms in one variable: ga x + gb + gc
            display = [
                (Fraction(g * a), var.latex),
                (Fraction(g * b), ""),
                (Fraction(g * c), ""),
            ]
            inner_parts = [
                (Fraction(a), var.latex),
                (Fraction(b), ""),
                (Fraction(c), ""),
            ]
        deg = 1
    else:
        a, b, c = inners[0], inners[1], inners[2]
        display = [
            (Fraction(g * a), f"{var.latex}^{{2}}"),
            (Fraction(g * b), var.latex),
            (Fraction(g * c), ""),
        ]
        inner_parts = [
            (Fraction(a), f"{var.latex}^{{2}}"),
            (Fraction(b), var.latex),
            (Fraction(c), ""),
        ]
        deg = 2
        ctx.policy.assert_degree(deg, where="factor_gcf.three_terms")

    ctx.rng.shuffle(display)
    latex, text = join_signed_terms(display)
    inner_l, inner_t = join_signed_terms(inner_parts)
    gcf_l = num_latex(Fraction(g))
    return FactorGcfExpression(
        latex=latex,
        text=text,
        factored_latex=f"{gcf_l}\\left({inner_l}\\right)",
        factored_text=f"{gcf_l}({inner_t})",
        gcf_latex=gcf_l,
        upgrades=tuple(sorted(ids)),
        effective_d=eff,
        max_degree=deg,
    )


def _with_variable_gcf(ctx, ids, eff, var, g, inners) -> FactorGcfExpression:
    """Poly-only: gx(ax + b) → ga x^2 + gb x."""
    ctx.policy.assert_degree(2, where="factor_gcf.variable_gcf")
    a = abs(inners[0]) or 1
    b = inners[1] if len(inners) > 1 else 1
    if b == 0:
        b = 1
    if len(inners) >= 3 and "three_terms" in ids:
        c = inners[2] or 1
        b = b + c

    display = [
        (Fraction(g * a), f"{var.latex}^{{2}}"),
        (Fraction(g * b), var.latex),
    ]
    ctx.rng.shuffle(display)
    latex, text = join_signed_terms(display)
    inner_l, inner_t = join_signed_terms(
        [(Fraction(a), var.latex), (Fraction(b), "")]
    )
    gcf_l = coeff_times_var(Fraction(g), var.latex)
    return FactorGcfExpression(
        latex=latex,
        text=text,
        factored_latex=f"{gcf_l}\\left({inner_l}\\right)",
        factored_text=f"{gcf_l}({inner_t})",
        gcf_latex=gcf_l,
        upgrades=tuple(sorted(ids)),
        effective_d=eff,
        max_degree=2,
    )
