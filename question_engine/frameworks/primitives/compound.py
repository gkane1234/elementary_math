"""Compound inequalities (and / or / chain) — builds on linear inequality sides."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Literal

from question_engine.frameworks.difficulty_budget import DifficultyFactor, select_upgrades
from question_engine.frameworks.niceness import NicenessError
from question_engine.frameworks.primitives._algebra_render import (
    coeff_times_var,
    num_latex,
    sample_integerish,
)
from question_engine.frameworks.primitives.registry import PRIM_INEQUALITIES, PrimitiveContext

COMPOUND_SETTINGS_SCHEMA: dict[str, Any] = {
    "compound_style": {
        "type": "enum",
        "values": ["and", "or", "chain", "auto"],
        "default": "auto",
    },
}

_UPGRADES: tuple[DifficultyFactor, ...] = (
    DifficultyFactor("two_step_sides", 2.0, ("structure",)),
    DifficultyFactor("or_style", 1.5, ("structure",)),
    DifficultyFactor("chain", 2.5, ("structure",)),
)


@dataclass(frozen=True)
class CompoundInequality:
    latex: str
    text: str
    solution_latex: str
    var_latex: str
    var_name: str
    style: Literal["and", "or", "chain"]
    upgrades: tuple[str, ...]
    effective_d: float
    # Number-line helpers
    lo: Fraction | None
    hi: Fraction | None
    lo_inclusive: bool
    hi_inclusive: bool


def sample_compound_inequality(ctx: PrimitiveContext) -> CompoundInequality:
    eff = ctx.effective_d(PRIM_INEQUALITIES)
    purchased, _, _ = select_upgrades(_UPGRADES, eff, rng=ctx.rng)
    ids = {f.id for f in purchased}
    settings = ctx.settings_for(PRIM_INEQUALITIES)
    force = str(settings.get("compound_style", "auto")).strip().lower()

    for _ in range(12):
        try:
            return _build(ctx, ids, eff, force)
        except (NicenessError, ValueError, ZeroDivisionError):
            if not ids:
                break
            costs = {f.id: f.cost for f in _UPGRADES}
            drop = max(ids, key=lambda i: costs.get(i, 0))
            ids.remove(drop)
            ctx.note_degraded(drop)
    return _build(ctx, set(), eff, force)


def _side(a: Fraction, var_l: str, b: Fraction) -> str:
    left = coeff_times_var(a, var_l)
    if b == 0:
        return left
    if b > 0:
        return f"{left} + {num_latex(b)}"
    return f"{left} - {num_latex(abs(b))}"


def _build(
    ctx: PrimitiveContext,
    ids: set[str],
    eff: float,
    force: str,
) -> CompoundInequality:
    var = ctx.sample_variable()
    two_step = "two_step_sides" in ids

    if force == "or" or (force == "auto" and "or_style" in ids and "chain" not in ids):
        style: Literal["and", "or", "chain"] = "or"
    elif force == "chain" or (force == "auto" and "chain" in ids):
        style = "chain"
    elif force == "and":
        style = "and"
    else:
        style = "and"

    a = Fraction(1)
    if two_step:
        a = Fraction(sample_integerish(ctx, exclude_zero=True).value)
        if a == 0:
            a = Fraction(2)

    if style == "chain":
        # lo < ax+b < hi
        mid = Fraction(sample_integerish(ctx, exclude_zero=False).value)
        span = abs(int(sample_integerish(ctx, exclude_zero=True, prefer_positive=True).value))
        if span < 2:
            span = 3
        lo_b = mid - span
        hi_b = mid + span
        b = Fraction(sample_integerish(ctx, exclude_zero=False).value) if two_step else Fraction(0)
        # Solve: lo < a x + b < hi  →  (lo-b)/a < x < (hi-b)/a  (assume a>0)
        if a < 0:
            a = abs(a)
        lo_x = Fraction(lo_b - b, a)
        hi_x = Fraction(hi_b - b, a)
        if lo_x > hi_x:
            lo_x, hi_x = hi_x, lo_x
        left = _side(a, var.latex, b)
        latex = f"{num_latex(Fraction(lo_b))} < {left} < {num_latex(Fraction(hi_b))}"
        text = f"{lo_b} < {a}{var.name}+{b} < {hi_b}"
        sol = f"{num_latex(lo_x)} < {var.latex} < {num_latex(hi_x)}"
        return CompoundInequality(
            latex=latex,
            text=text,
            solution_latex=sol,
            var_latex=var.latex,
            var_name=var.name,
            style="chain",
            upgrades=tuple(sorted(ids)),
            effective_d=eff,
            lo=lo_x,
            hi=hi_x,
            lo_inclusive=False,
            hi_inclusive=False,
        )

    # and / or: two separate inequalities
    c1 = Fraction(sample_integerish(ctx, exclude_zero=False).value)
    c2 = Fraction(sample_integerish(ctx, exclude_zero=False).value)
    if c1 == c2:
        c2 = c1 + Fraction(3)
    op1 = ctx.rng.choice(["<", "\\le"])
    op2 = ctx.rng.choice([">", "\\ge"])

    if style == "and":
        # x > lo and x < hi
        lo, hi = (c1, c2) if c1 < c2 else (c2, c1)
        latex = (
            f"{var.latex} {op2} {num_latex(lo)} \\text{{ and }} "
            f"{var.latex} {op1} {num_latex(hi)}"
        )
        text = f"{var.name} {op2} {lo} and {var.name} {op1} {hi}"
        sol = (
            f"{num_latex(lo)} {op2.replace('>', '<').replace('\\ge', '\\le') if False else ''} "
        )
        # Clean solution interval
        lo_inc = op2 in {">", "\\ge"} and op2 == "\\ge"
        # Actually: x ≥ lo and x ≤ hi
        lo_inc = op2 == "\\ge"
        hi_inc = op1 == "\\le"
        left_sym = "\\le" if lo_inc else "<"
        # Wait — op2 is > or ≥ meaning x > lo, so lower bound.
        left_sym = "\\ge" if op2 == "\\ge" else ">"
        right_sym = "\\le" if op1 == "\\le" else "<"
        # Standard: lo < x < hi form when possible
        if left_sym in {">", "\\ge"} and right_sym in {"<", "\\le"}:
            if left_sym == "\\ge" and right_sym == "\\le":
                sol = f"{num_latex(lo)} \\le {var.latex} \\le {num_latex(hi)}"
            elif left_sym == ">" and right_sym == "<":
                sol = f"{num_latex(lo)} < {var.latex} < {num_latex(hi)}"
            else:
                sol = (
                    f"{var.latex} {op2} {num_latex(lo)} \\text{{ and }} "
                    f"{var.latex} {op1} {num_latex(hi)}"
                )
        else:
            sol = latex
        return CompoundInequality(
            latex=latex,
            text=text,
            solution_latex=sol,
            var_latex=var.latex,
            var_name=var.name,
            style="and",
            upgrades=tuple(sorted(ids)),
            effective_d=eff,
            lo=lo,
            hi=hi,
            lo_inclusive=lo_inc,
            hi_inclusive=hi_inc,
        )

    # or: x < lo or x > hi
    lo, hi = (c1, c2) if c1 < c2 else (c2, c1)
    latex = (
        f"{var.latex} < {num_latex(lo)} \\text{{ or }} "
        f"{var.latex} > {num_latex(hi)}"
    )
    text = f"{var.name} < {lo} or {var.name} > {hi}"
    return CompoundInequality(
        latex=latex,
        text=text,
        solution_latex=latex,
        var_latex=var.latex,
        var_name=var.name,
        style="or",
        upgrades=tuple(sorted(ids)),
        effective_d=eff,
        lo=lo,
        hi=hi,
        lo_inclusive=False,
        hi_inclusive=False,
    )
