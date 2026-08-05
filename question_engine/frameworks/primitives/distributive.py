"""Distributive-property primitive on Layer 0 numbers (+ algebraic variants).

Structure is sampled via continuous-D ``DifficultyFactor`` upgrades, then
rendered through the shared presentation helpers (``render_scaled_sum``,
``render_product``, multiply glyphs / commute). Forms:

* ``scaled_sum`` — factor × sum (left or right factor side)
* ``two_binomials`` — (a+b)(c+d) at high D (still distributive expand)
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from fractions import Fraction
from typing import Any, Sequence

from question_engine.frameworks.difficulty_budget import DifficultyFactor, select_upgrades
from question_engine.frameworks.niceness import NicenessError
from question_engine.frameworks.primitives.presentation import (
    DisplayPiece,
    cancel_clutter_chance,
    cancel_clutter_intensity,
    expand_scaled_sum_latex,
    join_signed_display,
    order_commutative,
    presentation_for_ctx,
    render_product,
    render_scaled_sum,
)
from question_engine.frameworks.primitives.registry import PRIM_DISTRIBUTIVE, PrimitiveContext

DISTRIBUTIVE_SETTINGS_SCHEMA: dict[str, Any] = {
    "numeric_only": {"type": "bool", "default": True},
}

# Cheaper structure unlocks first; binomial×binomial is the high-D form.
_UPGRADES: tuple[DifficultyFactor, ...] = (
    DifficultyFactor("factor_right", 0.5, ("structure",)),
    DifficultyFactor("signed_inside", 1.0, ("structure",)),
    DifficultyFactor("three_terms", 1.5, ("structure",)),
    DifficultyFactor("two_binomials", 4.5, ("structure",)),
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
    value_check: Fraction  # outer * sum(inner), or product of binomial sums
    upgrades: tuple[str, ...]
    effective_d: float
    form: str = "numeric"  # numeric | var_outer | const_outer | two_binomials
    form_id: str = "scaled_sum"  # scaled_sum | two_binomials
    n_terms_inside: int = 2
    factor_side: str = "left"  # left | right | both


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
    return _render_scaled_numeric(
        ctx,
        a.latex,
        a.value,
        [(b.latex, b.latex, b.value), (c.latex, c.latex, c.value)],
        tuple(ids),
        eff,
        factor_side=_choose_factor_side(ctx, eff, ids),
    )


def sample_distributive_algebraic(ctx: PrimitiveContext) -> DistributiveExpression:
    """Algebraic distributive: sample structure from upgrades, render via presentation."""
    eff = ctx.effective_d(PRIM_DISTRIBUTIVE)
    # Resolve presentation once so notation knobs (explicit ·/×) stick for the item.
    presentation_for_ctx(ctx, d=eff, primitive_id=PRIM_DISTRIBUTIVE)
    purchased, _, _ = select_upgrades(_UPGRADES, eff, rng=ctx.rng)
    ids = {f.id for f in purchased}

    for _ in range(10):
        try:
            if _pick_structure(ctx, ids, eff) == "two_binomials":
                return _build_algebraic_two_binomials(ctx, ids, eff)
            return _build_algebraic_scaled_sum(ctx, ids, eff)
        except (NicenessError, ValueError):
            if not ids:
                break
            costs = {f.id: f.cost for f in _UPGRADES}
            drop = max(ids, key=lambda i: costs.get(i, 0))
            ids.remove(drop)
            ctx.note_degraded(drop)

    return _build_algebraic_scaled_sum(ctx, set(), eff)


def _choose_factor_side(ctx: PrimitiveContext, eff: float, ids: set[str]) -> str:
    """Left/right mix; ``factor_right`` upgrade unlocks a fair coin, else soft D chance."""
    if "factor_right" in ids:
        return "right" if ctx.rng.random() < 0.5 else "left"
    soft_p = min(0.35, 0.12 + 0.02 * float(eff))
    return "right" if ctx.rng.random() < soft_p else "left"


def _style_for_side(ctx: PrimitiveContext, eff: float, factor_side: str):
    """Force factor order on top of an already-resolved presentation style."""
    base = presentation_for_ctx(ctx, d=eff, primitive_id=PRIM_DISTRIBUTIVE, reuse=True)
    if factor_side == "right":
        style = replace(base, commute_mul=True)
    elif factor_side == "left":
        style = replace(base, commute_mul=False)
    else:
        style = base
    try:
        ctx._presentation_style = style
    except Exception:
        pass
    return style


def _maybe_cancel(
    ctx: PrimitiveContext,
    style,
    *,
    var_latex: str,
    var_text: str,
    latex: str,
    text: str,
    eff: float,
    upgrades: tuple[str, ...],
) -> tuple[str, str, tuple[str, ...]]:
    """Optional cancel-clutter wrap (knob-gated; amount=0 → no-op)."""
    from question_engine.frameworks.primitives.presentation import maybe_inject_cancel_clutter

    settings = ctx.settings if isinstance(getattr(ctx, "settings", None), dict) else {}
    # Prefer topic-level distributive.cancel_clutter when present on settings.
    latex2, text2, tags = maybe_inject_cancel_clutter(
        ctx,
        style,
        var_latex=var_latex,
        var_text=var_text,
        core_latex=latex,
        core_text=text,
        d=eff,
        settings=settings,
    )
    if tags:
        return latex2, text2, upgrades + tags
    return latex, text, upgrades


def _unsigned_terms(
    ctx: PrimitiveContext,
    terms: list[tuple[str, str, Fraction]],
    ids: set[str],
) -> list[tuple[str, str, Fraction]]:
    if "signed_inside" in ids:
        return terms
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
    return fixed


def _sample_inner_terms(
    ctx: PrimitiveContext, ids: set[str], *, n: int | None = None
) -> list[tuple[str, str, Fraction]]:
    count = n if n is not None else (3 if "three_terms" in ids else 2)
    for _attempt in range(12):
        terms: list[tuple[str, str, Fraction]] = []
        for _ in range(count):
            s = ctx.sample_number()
            terms.append((s.latex, s.latex, s.value))
        terms = _unsigned_terms(ctx, terms, ids)
        if sum((t[2] for t in terms), Fraction(0)) != 0:
            return terms
    # Non-canceling fallback
    fallback = [
        ("2", "2", Fraction(2)),
        ("3", "3", Fraction(3)),
    ]
    if count >= 3:
        fallback.append(("1", "1", Fraction(1)))
    return fallback[:count]


def _pick_structure(
    ctx: PrimitiveContext, ids: set[str], eff: float
) -> str:
    """Choose form_id among unlocked structures (harder forms weighted up with D)."""
    weights: dict[str, float] = {"scaled_sum": 3.0}
    if "two_binomials" in ids:
        # Unlock ≠ always: ramp share with D so scaled_sum/trinomial remain.
        weights["two_binomials"] = max(0.8, 0.4 + 0.35 * max(0.0, float(eff) - 6.0))
    keys = list(weights.keys())
    wts = [weights[k] for k in keys]
    return ctx.rng.choices(keys, weights=wts, k=1)[0]


def _group_sum(
    terms: Sequence[tuple[str, str, Fraction]],
    style,
    rng,
) -> DisplayPiece:
    ordered = order_commutative(list(terms), commute=style.commute_add, rng=rng)
    inner_l, inner_t = join_signed_display(ordered)
    return DisplayPiece(latex=rf"\left({inner_l}\right)", text=f"({inner_t})")


def expand_product_of_sums_latex(
    left: Sequence[tuple[str, Fraction]],
    right: Sequence[tuple[str, Fraction]],
) -> str:
    """FOIL-style expand ``(a±b)(c±d)`` as ``a·c + a·d + …`` (always ``\\cdot``)."""
    parts: list[str] = []
    for l_l, l_v in left:
        for r_l, r_v in right:
            neg = (l_v < 0) != (r_v < 0)
            l_body = l_l[1:] if l_v < 0 and l_l.startswith("-") else l_l
            r_body = r_l[1:] if r_v < 0 and r_l.startswith("-") else r_l
            piece = f"{l_body}\\cdot {r_body}"
            parts.append(f"- {piece}" if neg else piece)
    if not parts:
        return "0"
    out = parts[0]
    for p in parts[1:]:
        if p.startswith("- "):
            out = f"{out} - {p[2:]}"
        else:
            out = f"{out} + {p}"
    return out


def _log_form(
    ctx: PrimitiveContext,
    *,
    form_id: str,
    n_terms_inside: int,
    factor_side: str,
    upgrades: tuple[str, ...],
    eff: float,
    form: str,
) -> None:
    ctx._sample_log.append(
        {
            "primitive": PRIM_DISTRIBUTIVE,
            "form_id": form_id,
            "n_terms_inside": n_terms_inside,
            "factor_side": factor_side,
            "form": form,
            "upgrades": list(upgrades),
            "d": eff,
        }
    )


def _build_numeric(
    ctx: PrimitiveContext, ids: set[str], eff: float
) -> DistributiveExpression:
    if _pick_structure(ctx, ids, eff) == "two_binomials":
        return _build_numeric_two_binomials(ctx, ids, eff)

    outer = ctx.sample_number(exclude_zero=True)
    terms = _sample_inner_terms(ctx, ids)
    return _render_scaled_numeric(
        ctx,
        outer.latex,
        outer.value,
        terms,
        tuple(sorted(ids)),
        eff,
        factor_side=_choose_factor_side(ctx, eff, ids),
    )


def _build_numeric_two_binomials(
    ctx: PrimitiveContext, ids: set[str], eff: float
) -> DistributiveExpression:
    left = _sample_inner_terms(ctx, ids, n=2)
    right = _sample_inner_terms(ctx, ids, n=2)
    style = _style_for_side(ctx, eff, "both")
    # Mild commute of the two binomial factors is fine; keep both grouped.
    left_g = _group_sum(left, style, ctx.rng)
    right_g = _group_sum(right, style, ctx.rng)
    latex, text = render_product([left_g, right_g], style, ctx.rng)
    expanded = expand_product_of_sums_latex(
        [(t[0], t[2]) for t in left],
        [(t[0], t[2]) for t in right],
    )
    total_l = sum((t[2] for t in left), Fraction(0))
    total_r = sum((t[2] for t in right), Fraction(0))
    upgrades = tuple(sorted(ids))
    _log_form(
        ctx,
        form_id="two_binomials",
        n_terms_inside=2,
        factor_side="both",
        upgrades=upgrades,
        eff=eff,
        form="two_binomials",
    )
    return DistributiveExpression(
        latex=latex,
        text=text,
        expanded_latex=expanded,
        value_check=total_l * total_r,
        upgrades=upgrades,
        effective_d=eff,
        form="two_binomials",
        form_id="two_binomials",
        n_terms_inside=2,
        factor_side="both",
    )


def _render_scaled_numeric(
    ctx: PrimitiveContext,
    outer_latex: str,
    outer_val: Fraction,
    terms: list[tuple[str, str, Fraction]],
    upgrades: tuple[str, ...],
    eff: float,
    *,
    factor_side: str,
) -> DistributiveExpression:
    style = _style_for_side(ctx, eff, factor_side)
    outer = DisplayPiece(outer_latex, outer_latex)
    latex, text = render_scaled_sum(outer, terms, style, ctx.rng)
    expanded = expand_scaled_sum_latex(outer_latex, [(t[0], t[2]) for t in terms])
    total_inside = sum((t[2] for t in terms), Fraction(0))
    n_terms = len(terms)
    _log_form(
        ctx,
        form_id="scaled_sum",
        n_terms_inside=n_terms,
        factor_side=factor_side,
        upgrades=upgrades,
        eff=eff,
        form="numeric",
    )
    return DistributiveExpression(
        latex=latex,
        text=text,
        expanded_latex=expanded,
        value_check=outer_val * total_inside,
        upgrades=upgrades,
        effective_d=eff,
        form="numeric",
        form_id="scaled_sum",
        n_terms_inside=n_terms,
        factor_side=factor_side,
    )


def _build_algebraic_scaled_sum(
    ctx: PrimitiveContext, ids: set[str], eff: float
) -> DistributiveExpression:
    """``k(x+…)`` / ``(x+…)k`` or ``x(a+b[+c])`` / ``(a+b)x``."""
    var = ctx.sample_variable()
    factor_side = _choose_factor_side(ctx, eff, ids)
    style = _style_for_side(ctx, eff, factor_side)
    n_extra = 2 if "three_terms" in ids else 1  # var + extras, or numeric inners

    # ~half var-outer (variable as the factor), else const-outer.
    if ctx.rng.random() < 0.5:
        inners = _sample_inner_terms(ctx, ids, n=2 if "three_terms" not in ids else 3)
        # Avoid degenerate sum that cancels to 0.
        if sum((t[2] for t in inners), Fraction(0)) == 0:
            inners = _unsigned_terms(
                ctx,
                [
                    ("2", "2", Fraction(2)),
                    ("3", "3", Fraction(3)),
                ]
                + ([("1", "1", Fraction(1))] if "three_terms" in ids else []),
                ids,
            )
        outer = DisplayPiece(var.latex, var.name)
        latex, text = render_scaled_sum(outer, inners, style, ctx.rng)
        expanded = expand_scaled_sum_latex(var.latex, [(t[0], t[2]) for t in inners])
        form = "var_outer"
        value_check = sum((t[2] for t in inners), Fraction(0))
        n_terms = len(inners)
    else:
        from question_engine.frameworks.primitives._algebra_render import num_latex

        outer_n = ctx.sample_number(exclude_zero=True)
        # Avoid ±1 outer — juxtaposition reads as a lone sum.
        for _ in range(8):
            if abs(outer_n.value) != 1:
                break
            outer_n = ctx.sample_number(exclude_zero=True)
        if abs(outer_n.value) == 1:
            outer_piece = DisplayPiece(num_latex(Fraction(3)), "3")
            outer_val = Fraction(3)
        else:
            outer_piece = DisplayPiece(outer_n.latex, outer_n.latex)
            outer_val = outer_n.value

        extras = _sample_inner_terms(ctx, ids, n=n_extra)
        summands: list[tuple[str, str, Fraction]] = [
            (var.latex, var.name, Fraction(1)),
            *extras,
        ]
        latex, text = render_scaled_sum(outer_piece, summands, style, ctx.rng)
        expanded = expand_scaled_sum_latex(
            outer_piece.latex, [(t[0], t[2]) for t in summands]
        )
        form = "const_outer"
        value_check = outer_val
        n_terms = len(summands)

    upgrades = tuple(sorted(ids))
    latex, text, upgrades = _maybe_cancel(
        ctx,
        style,
        var_latex=var.latex,
        var_text=var.name,
        latex=latex,
        text=text,
        eff=eff,
        upgrades=upgrades,
    )
    _log_form(
        ctx,
        form_id="scaled_sum",
        n_terms_inside=n_terms,
        factor_side=factor_side,
        upgrades=upgrades,
        eff=eff,
        form=form,
    )
    return DistributiveExpression(
        latex=latex,
        text=text,
        expanded_latex=expanded,
        value_check=value_check,
        upgrades=upgrades,
        effective_d=eff,
        form=form,
        form_id="scaled_sum",
        n_terms_inside=n_terms,
        factor_side=factor_side,
    )


def _build_algebraic_two_binomials(
    ctx: PrimitiveContext, ids: set[str], eff: float
) -> DistributiveExpression:
    """One-variable binomial × numeric binomial — distributive, not full FOIL poly."""
    from question_engine.frameworks.primitives._algebra_render import num_latex

    var = ctx.sample_variable()
    a = ctx.sample_number()
    if "signed_inside" not in ids and a.value < 0:
        for _ in range(6):
            a = ctx.sample_number()
            if a.value >= 0:
                break
    if a.value == 0 or ("signed_inside" not in ids and a.value < 0):
        a_latex, a_val = num_latex(Fraction(2)), Fraction(2)
    else:
        a_latex, a_val = a.latex, a.value

    right = _sample_inner_terms(ctx, ids, n=2)
    left: list[tuple[str, str, Fraction]] = [
        (var.latex, var.name, Fraction(1)),
        (a_latex, a_latex, a_val),
    ]
    style = _style_for_side(ctx, eff, "both")
    # Prefer var-binomial on the left for classroom reading; allow product commute.
    left_g = _group_sum(left, replace(style, commute_add=style.commute_add), ctx.rng)
    right_g = _group_sum(right, style, ctx.rng)
    latex, text = render_product([left_g, right_g], style, ctx.rng)
    expanded = expand_product_of_sums_latex(
        [(t[0], t[2]) for t in left],
        [(t[0], t[2]) for t in right],
    )
    upgrades = tuple(sorted(ids))
    latex, text, upgrades = _maybe_cancel(
        ctx,
        style,
        var_latex=var.latex,
        var_text=var.name,
        latex=latex,
        text=text,
        eff=eff,
        upgrades=upgrades,
    )
    _log_form(
        ctx,
        form_id="two_binomials",
        n_terms_inside=2,
        factor_side="both",
        upgrades=upgrades,
        eff=eff,
        form="two_binomials",
    )
    total_r = sum((t[2] for t in right), Fraction(0))
    return DistributiveExpression(
        latex=latex,
        text=text,
        expanded_latex=expanded,
        value_check=total_r,  # coeff of var after expand = sum(right)
        upgrades=upgrades,
        effective_d=eff,
        form="two_binomials",
        form_id="two_binomials",
        n_terms_inside=2,
        factor_side="both",
    )
