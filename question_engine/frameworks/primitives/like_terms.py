"""Combine like terms / simplify — Layer 1 on numbers + variables.

Linear policy (``max_degree ≤ 1``): degree-1 terms (+ optional 2nd var).
Polynomial policy: monomial keys are powers ``x^k`` up to ``target_poly_degree``.

Difficulty north star: **D=0 = simplest possible** — 2 like + 2 unlike, friendly
positive coeffs, no clutter upgrades. Through mid D (≈5), total terms stay in
{3, 4}. Heavier structure (more likes, many terms, 2nd variable) unlocks later
via expensive upgrades (see ``difficulty_knobs.json`` → ``like_terms``).
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from question_engine.frameworks.difficulty_budget import DifficultyFactor, select_upgrades
from question_engine.frameworks.niceness import NicenessError
from question_engine.frameworks.primitives._algebra_render import (
    join_signed_terms,
    sample_integerish,
)
from question_engine.frameworks.primitives.difficulty_knobs import fget, iget, section
from question_engine.frameworks.primitives.poly_helpers import (
    power_atom,
    target_n_terms,
    target_poly_degree,
)
from question_engine.frameworks.primitives.registry import PRIM_LIKE_TERMS, PrimitiveContext

LIKE_TERMS_SETTINGS_SCHEMA: dict[str, Any] = {}


def _upgrade_catalog() -> tuple[DifficultyFactor, ...]:
    """Upgrade costs from knobs (expensive so mid-D stays mild)."""
    return (
        DifficultyFactor(
            "negatives",
            fget("like_terms", "upgrade_negatives_cost", 3.0),
            ("structure",),
        ),
        DifficultyFactor(
            "more_like",
            fget("like_terms", "upgrade_more_like_cost", 5.0),
            ("structure",),
        ),
        DifficultyFactor(
            "many_terms",
            fget("like_terms", "upgrade_many_terms_cost", 8.0),
            ("structure",),
        ),
        DifficultyFactor(
            "second_variable",
            fget("like_terms", "upgrade_second_variable_cost", 10.0),
            ("structure",),
        ),
    )


@dataclass(frozen=True)
class LikeTermsExpression:
    latex: str
    text: str
    simplified_latex: str
    simplified_text: str
    upgrades: tuple[str, ...]
    effective_d: float
    max_degree: int = 1
    n_terms: int = 0


def sample_like_terms(ctx: PrimitiveContext) -> LikeTermsExpression:
    eff = ctx.effective_d(PRIM_LIKE_TERMS)
    purchased, _, _ = select_upgrades(_upgrade_catalog(), eff, rng=ctx.rng)
    ids = {f.id for f in purchased}

    for _ in range(10):
        try:
            return _build(ctx, ids, eff)
        except (NicenessError, ValueError):
            if not ids:
                break
            costs = {f.id: f.cost for f in _upgrade_catalog()}
            drop = max(ids, key=lambda i: costs.get(i, 0))
            ids.remove(drop)
            ctx.note_degraded(drop)

    return _build(ctx, set(), eff)


def _signed_coeff(ctx: PrimitiveContext, ids: set[str], *, exclude_zero: bool = True) -> Fraction:
    prefer_pos = "negatives" not in ids
    n = sample_integerish(ctx, exclude_zero=exclude_zero, prefer_positive=prefer_pos)
    if "negatives" not in ids and n.value < 0:
        return abs(n.value) if n.value != 0 else Fraction(1)
    return n.value


def _linear_term_counts(ctx: PrimitiveContext, ids: set[str]) -> tuple[int, int]:
    """Return (n_like, n_unlike) for the linear combine-like-terms shape.

    D=0 → always base (2 like + 2 unlike).
    Through mid_d → total in {mid_total_lo, mid_total_hi} (typically 3–4).
    Above mid_d → base + purchased structure upgrades.
    """
    sec = section("like_terms")
    n_like = int(sec.get("base_n_like", 2))
    n_unlike = int(sec.get("base_n_unlike", 2))
    topic_d = max(0.0, float(ctx.topic_d))
    mid_d = float(sec.get("mid_d", 5.0))
    lo = int(sec.get("mid_total_lo", 3))
    hi = int(sec.get("mid_total_hi", 4))
    prefer_lo = float(sec.get("mid_prefer_lo_chance", 0.6))

    if topic_d <= 1e-12:
        return max(2, n_like), max(1, n_unlike)

    if topic_d <= mid_d + 1e-12:
        # Mild band: mostly ``lo`` terms (2 like + 1 unlike), sometimes ``hi`` (2+2).
        total = lo if ctx.rng.random() < prefer_lo else hi
        total = max(lo, min(hi, int(total)))
        # Keep exactly 2 like; remaining slots are unlike (constants).
        return 2, max(1, total - 2)

    # Past mid: apply structural upgrades.
    if "more_like" in ids:
        n_like += int(sec.get("more_like_extra", 1))
    if "many_terms" in ids:
        n_like += int(sec.get("many_terms_extra_like", 2))
        n_unlike += int(sec.get("many_terms_extra_unlike", 1))
    return max(2, n_like), max(1, n_unlike)


def _build(ctx: PrimitiveContext, ids: set[str], eff: float) -> LikeTermsExpression:
    deg_cap = target_poly_degree(eff, ctx.policy)
    if deg_cap >= 2:
        return _build_poly(ctx, ids, eff, deg_cap)
    return _build_linear(ctx, ids, eff)


def _build_linear(ctx: PrimitiveContext, ids: set[str], eff: float) -> LikeTermsExpression:
    var = ctx.sample_variable()
    n_like, n_const = _linear_term_counts(ctx, ids)
    mid_d = fget("like_terms", "mid_d", 5.0)
    # Structure / sign upgrades only bite past the mild band (D ≤ mid_d).
    active = set(ids) if ctx.topic_d > mid_d + 1e-12 else set()

    x_coeffs = [_signed_coeff(ctx, active, exclude_zero=True) for _ in range(n_like)]
    const_coeffs = [_signed_coeff(ctx, active, exclude_zero=True) for _ in range(n_const)]

    y_coeffs: list[Fraction] = []
    y_var = None
    if (
        "second_variable" in active
        and ctx.policy.max_variables >= 2
    ):
        for _ in range(8):
            y_var = ctx.sample_variable()
            if y_var.name != var.name:
                break
        if y_var is None or y_var.name == var.name:
            y_var = None
        else:
            n_y = 2 if "more_like" in active else 1
            y_coeffs = [_signed_coeff(ctx, active, exclude_zero=True) for _ in range(n_y)]

    display: list[tuple[Fraction, str]] = [(c, var.latex) for c in x_coeffs]
    display.extend((c, "") for c in const_coeffs)
    if y_var is not None:
        display.extend((c, y_var.latex) for c in y_coeffs)
    ctx.rng.shuffle(display)

    latex, text = join_signed_terms(display)

    total_x = sum(x_coeffs, Fraction(0))
    total_c = sum(const_coeffs, Fraction(0))
    total_y = sum(y_coeffs, Fraction(0))
    simplified_parts: list[tuple[Fraction, str]] = []
    if total_x != 0:
        simplified_parts.append((total_x, var.latex))
    if y_var is not None and total_y != 0:
        simplified_parts.append((total_y, y_var.latex))
    if total_c != 0:
        simplified_parts.append((total_c, ""))
    simp_l, simp_t = join_signed_terms(simplified_parts)

    return LikeTermsExpression(
        latex=latex,
        text=text,
        simplified_latex=simp_l,
        simplified_text=simp_t,
        upgrades=tuple(sorted(active)),
        effective_d=eff,
        max_degree=1,
        n_terms=len([c for c, _ in display if c != 0]),
    )


def _build_poly(
    ctx: PrimitiveContext,
    ids: set[str],
    eff: float,
    deg_cap: int,
) -> LikeTermsExpression:
    """Combine like powers up to ``deg_cap`` (policy-gated)."""
    var = ctx.sample_variable()
    ctx.policy.assert_degree(deg_cap, where="like_terms.poly")

    # Which degrees appear: always include deg_cap and 0; fill middles with D.
    degrees = [deg_cap]
    if deg_cap >= 1:
        degrees.append(1)
    degrees.append(0)
    for d in range(2, deg_cap):
        if d not in degrees and ctx.rng.random() < 0.55 + 0.05 * eff:
            degrees.append(d)
    degrees = sorted(set(degrees), reverse=True)  # high powers first so deg_cap always appears

    # Cap total display length; keep poly mild near low D.
    topic_d = max(0.0, float(ctx.topic_d))
    mid_d = fget("like_terms", "mid_d", 5.0)
    active = set(ids) if topic_d > mid_d + 1e-12 else set()
    if topic_d <= mid_d:
        max_display = int(fget("like_terms", "mid_total_hi", 4))
        n_per = 1
        degrees = [deg_cap, 0] if deg_cap >= 1 else [0]
    else:
        if "more_like" in active:
            n_per = 2 + iget("like_terms", "more_like_extra", 1)
        else:
            n_per = 2
        if "many_terms" in active:
            n_per += 1
        max_display = max(4, target_n_terms(eff) + 2, n_per * len(degrees))

    totals: dict[int, Fraction] = {d: Fraction(0) for d in degrees}
    display: list[tuple[Fraction, str]] = []
    for d in degrees:
        n = n_per if d > 0 else max(1, n_per)
        atom = power_atom(var.latex, d)
        for _ in range(n):
            if len(display) >= max_display and d != deg_cap and totals.get(deg_cap, 0) != 0:
                break
            c = _signed_coeff(ctx, active, exclude_zero=(d > 0))
            if c == 0 and d > 0:
                c = Fraction(1)
            display.append((c, atom))
            totals[d] += c
        # Always ensure at least one term at deg_cap.
        if d == deg_cap and totals[d] == 0:
            c = _signed_coeff(ctx, active, exclude_zero=True)
            display.append((c, atom))
            totals[d] += c

    if len(display) < 2:
        raise ValueError("need multiple like-term candidates")

    ctx.rng.shuffle(display)
    latex, text = join_signed_terms(display)

    simp_parts = [
        (totals[d], power_atom(var.latex, d))
        for d in sorted(totals.keys(), reverse=True)
        if totals[d] != 0
    ]
    simp_l, simp_t = join_signed_terms(simp_parts)
    used_deg = max((d for d, c in totals.items() if c != 0), default=0)

    tags = list(active) + [f"degree:{used_deg}"]
    return LikeTermsExpression(
        latex=latex,
        text=text,
        simplified_latex=simp_l,
        simplified_text=simp_t,
        upgrades=tuple(sorted(tags)),
        effective_d=eff,
        max_degree=used_deg,
        n_terms=len([c for c, _ in display if c != 0]),
    )
