"""Distributive-property primitive on Layer 0 numbers (+ algebraic variants).

Algebraic distributive is a thin client of the shared expression generator:
seed an expanded linear answer, ask ``construct_affine`` for a factored
presentation (commute / explicit multiply / optional cancel clutter).
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from question_engine.frameworks.difficulty_budget import DifficultyFactor, select_upgrades
from question_engine.frameworks.niceness import NicenessError
from question_engine.frameworks.primitives.constructive import (
    ExpressionScope,
    construct_affine,
)
from question_engine.frameworks.primitives.presentation import (
    DisplayPiece,
    cancel_clutter_chance,
    cancel_clutter_intensity,
    expand_scaled_sum_latex,
    presentation_for_ctx,
    render_scaled_sum,
)
from question_engine.frameworks.primitives.registry import PRIM_DISTRIBUTIVE, PrimitiveContext

DISTRIBUTIVE_SETTINGS_SCHEMA: dict[str, Any] = {
    "numeric_only": {"type": "bool", "default": True},
}

_UPGRADES: tuple[DifficultyFactor, ...] = (
    DifficultyFactor("three_terms", 1.5, ("structure",)),
    DifficultyFactor("signed_inside", 1.0, ("structure",)),
)

# Re-export for tests / callers that imported from distributive historically.
__all__ = [
    "DISTRIBUTIVE_SETTINGS_SCHEMA",
    "DistributiveExpression",
    "cancel_clutter_chance",
    "cancel_clutter_intensity",
    "sample_distributive_algebraic",
    "sample_distributive_numeric",
]


@dataclass(frozen=True)
class DistributiveExpression:
    latex: str
    text: str
    expanded_latex: str
    value_check: Fraction  # outer * sum(inner) numeric value when numeric
    upgrades: tuple[str, ...]
    effective_d: float
    form: str = "numeric"  # numeric | var_outer | const_outer


def sample_distributive_numeric(ctx: PrimitiveContext) -> DistributiveExpression:
    eff = ctx.effective_d(PRIM_DISTRIBUTIVE)
    purchased, _, _ = select_upgrades(_UPGRADES, eff, rng=ctx.rng)
    ids = {f.id for f in purchased}

    for _ in range(10):
        try:
            return _build_numeric(ctx, ids, eff)
        except (NicenessError, ValueError):
            if not ids:
                break
            costs = {f.id: f.cost for f in _UPGRADES}
            drop = max(ids, key=lambda i: costs.get(i, 0))
            ids.remove(drop)
            ctx.note_degraded(drop)

    a = ctx.sample_number(exclude_zero=True)
    b = ctx.sample_number()
    c = ctx.sample_number()
    return _render_numeric(
        ctx,
        a.latex,
        [(b.latex, b.latex, b.value), (c.latex, c.latex, c.value)],
        a.value,
        tuple(ids),
        eff,
    )


def sample_distributive_algebraic(ctx: PrimitiveContext) -> DistributiveExpression:
    """Linear distributive via shared expression generator (answer-first).

    1. Seed expanded linear answer inside ``construct_affine``
    2. Scope: ``max_degree=1``, prefer factored ``outer·(sum)``, allow cancel
       clutter (knob-gated; off when amount=0)
    3. Presentation commute / explicit multiply come from the shared layer

    Answer remains the core distributive expansion (cancel terms do not change it).
    """
    eff = ctx.effective_d(PRIM_DISTRIBUTIVE)
    # Resolve presentation once so constructive reuses the same style.
    presentation_for_ctx(ctx, d=eff, primitive_id=PRIM_DISTRIBUTIVE)

    surface = construct_affine(
        ctx,
        d=eff,
        scope=ExpressionScope(
            max_degree=1,
            allow_cancel_clutter=True,
            prefer_distributive_factorization=True,
        ),
    )
    form = str(surface.metadata.get("distributive_form") or "const_outer")
    expanded = str(
        surface.metadata.get("expanded_distributive_latex")
        or surface.simplified_latex
        or ""
    )
    cancel_tags = tuple(
        u for u in surface.inflators_applied if str(u).startswith("cancel:")
    )
    # value_check: var_outer → coeff of var after expand; const_outer → outer coeff
    if form == "var_outer":
        value_check = surface.coeff_a if surface.coeff_a is not None else Fraction(0)
    else:
        value_check = surface.coeff_a if surface.coeff_a is not None else Fraction(0)

    return DistributiveExpression(
        latex=surface.latex,
        text=surface.text,
        expanded_latex=expanded,
        value_check=value_check,
        upgrades=cancel_tags,
        effective_d=eff,
        form=form,
    )


def _build_numeric(
    ctx: PrimitiveContext, ids: set[str], eff: float
) -> DistributiveExpression:
    a = ctx.sample_number(exclude_zero=True)
    b = ctx.sample_number()
    c = ctx.sample_number()
    terms: list[tuple[str, str, Fraction]] = [
        (b.latex, b.latex, b.value),
        (c.latex, c.latex, c.value),
    ]
    if "three_terms" in ids:
        d = ctx.sample_number()
        terms.append((d.latex, d.latex, d.value))
    if "signed_inside" not in ids:
        fixed: list[tuple[str, str, Fraction]] = []
        for _latex, _text, val in terms:
            if val < 0:
                n = ctx.sample_number()
                for _ in range(5):
                    if n.value >= 0:
                        break
                    n = ctx.sample_number()
                vv = n.value if n.value >= 0 else abs(n.value)
                fixed.append((n.latex if n.value >= 0 else str(vv), str(vv), vv))
            else:
                fixed.append((_latex, _text, val))
        terms = fixed

    return _render_numeric(ctx, a.latex, terms, a.value, tuple(sorted(ids)), eff)


def _render_numeric(
    ctx: PrimitiveContext,
    outer_latex: str,
    terms: list[tuple[str, str, Fraction]],
    outer_val: Fraction,
    upgrades: tuple[str, ...],
    eff: float,
) -> DistributiveExpression:
    style = presentation_for_ctx(ctx, d=eff, primitive_id=PRIM_DISTRIBUTIVE)
    outer = DisplayPiece(outer_latex, outer_latex)
    latex, text = render_scaled_sum(outer, terms, style, ctx.rng)
    expanded = expand_scaled_sum_latex(outer_latex, [(t[0], t[2]) for t in terms])
    total_inside = sum((t[2] for t in terms), Fraction(0))
    return DistributiveExpression(
        latex=latex,
        text=text,
        expanded_latex=expanded,
        value_check=outer_val * total_inside,
        upgrades=upgrades,
        effective_d=eff,
        form="numeric",
    )
