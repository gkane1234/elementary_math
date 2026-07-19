"""Proportions and literal equations — linear, policy max_degree=1."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from question_engine.frameworks.difficulty_budget import DifficultyFactor, select_upgrades
from question_engine.frameworks.niceness import NicenessError
from question_engine.frameworks.primitives._algebra_render import num_latex, sample_integerish
from question_engine.frameworks.primitives.registry import PRIM_EQUATIONS, PrimitiveContext

PROPORTIONS_SETTINGS_SCHEMA: dict[str, Any] = {}
LITERALS_SETTINGS_SCHEMA: dict[str, Any] = {}

_PROP_UPGRADES: tuple[DifficultyFactor, ...] = (
    DifficultyFactor("variable_in_denom", 2.0, ("structure",)),
    DifficultyFactor("multi_step_clear", 2.5, ("structure",)),
)

_LIT_UPGRADES: tuple[DifficultyFactor, ...] = (
    DifficultyFactor("multi_letter", 1.5, ("structure",)),
    DifficultyFactor("rearrange_hard", 2.5, ("structure",)),
)


@dataclass(frozen=True)
class ProportionEquation:
    latex: str
    text: str
    solution_latex: str
    solution: Fraction
    var_latex: str
    var_name: str
    upgrades: tuple[str, ...]
    effective_d: float


@dataclass(frozen=True)
class LiteralEquation:
    latex: str
    text: str
    solution_latex: str
    target_var: str
    form: str
    upgrades: tuple[str, ...]
    effective_d: float


def sample_proportion(ctx: PrimitiveContext) -> ProportionEquation:
    ctx.policy.assert_degree(1, where="proportion")
    eff = ctx.effective_d(PRIM_EQUATIONS)
    purchased, _, _ = select_upgrades(_PROP_UPGRADES, eff, rng=ctx.rng)
    ids = {f.id for f in purchased}
    for _ in range(12):
        try:
            return _build_prop(ctx, ids, eff)
        except (NicenessError, ValueError, ZeroDivisionError):
            if not ids:
                break
            drop = max(ids, key=lambda i: next(f.cost for f in _PROP_UPGRADES if f.id == i))
            ids.remove(drop)
            ctx.note_degraded(drop)
    return _build_prop(ctx, set(), eff)


def sample_literal_equation(ctx: PrimitiveContext) -> LiteralEquation:
    ctx.policy.assert_degree(1, where="literal")
    eff = ctx.effective_d(PRIM_EQUATIONS)
    purchased, _, _ = select_upgrades(_LIT_UPGRADES, eff, rng=ctx.rng)
    ids = {f.id for f in purchased}
    for _ in range(10):
        try:
            return _build_lit(ctx, ids, eff)
        except (NicenessError, ValueError):
            if not ids:
                break
            drop = max(ids, key=lambda i: next(f.cost for f in _LIT_UPGRADES if f.id == i))
            ids.remove(drop)
            ctx.note_degraded(drop)
    return _build_lit(ctx, set(), eff)


def _build_prop(ctx: PrimitiveContext, ids: set[str], eff: float) -> ProportionEquation:
    var = ctx.sample_variable()
    # a/b = c/x  or  a/x = b/c  or  a/b = x/c
    a = abs(int(sample_integerish(ctx, exclude_zero=True, prefer_positive=True).value))
    b = abs(int(sample_integerish(ctx, exclude_zero=True, prefer_positive=True).value))
    c = abs(int(sample_integerish(ctx, exclude_zero=True, prefer_positive=True).value))
    if min(a, b, c) < 1:
        a, b, c = 2, 3, 4

    if "variable_in_denom" in ids:
        # a/x = b/c  → x = a c / b
        sol = Fraction(a * c, b)
        latex = f"\\frac{{{a}}}{{{var.latex}}} = \\frac{{{b}}}{{{c}}}"
        text = f"{a}/{var.name} = {b}/{c}"
    elif "multi_step_clear" in ids:
        # (a)/(b) = (x+d)/c → cross multiply
        d = int(sample_integerish(ctx, exclude_zero=False).value)
        # a/b = (x+d)/c → a c = b(x+d) → x = (a c)/b - d
        sol = Fraction(a * c, b) - d
        inner = f"{var.latex} + {d}" if d >= 0 else f"{var.latex} - {abs(d)}"
        latex = f"\\frac{{{a}}}{{{b}}} = \\frac{{{inner}}}{{{c}}}"
        text = f"{a}/{b} = ({var.name}+{d})/{c}"
    else:
        # a/b = x/c → x = a c / b
        sol = Fraction(a * c, b)
        latex = f"\\frac{{{a}}}{{{b}}} = \\frac{{{var.latex}}}{{{c}}}"
        text = f"{a}/{b} = {var.name}/{c}"

    return ProportionEquation(
        latex=latex,
        text=text,
        solution_latex=f"{var.latex} = {num_latex(sol)}",
        solution=sol,
        var_latex=var.latex,
        var_name=var.name,
        upgrades=tuple(sorted(ids)),
        effective_d=eff,
    )


def _build_lit(ctx: PrimitiveContext, ids: set[str], eff: float) -> LiteralEquation:
    hard = "rearrange_hard" in ids
    multi = "multi_letter" in ids or hard

    if not multi:
        form = ctx.rng.choice(["area", "distance", "interest"])
        if form == "area":
            latex = r"A = \ell w \quad \text{Solve for } w."
            text = "A = lw. Solve for w."
            ans = r"w = \frac{A}{\ell}"
            target = "w"
        elif form == "distance":
            latex = r"d = r t \quad \text{Solve for } t."
            text = "d = rt. Solve for t."
            ans = r"t = \frac{d}{r}"
            target = "t"
        else:
            latex = r"I = p r t \quad \text{Solve for } r."
            text = "I = prt. Solve for r."
            ans = r"r = \frac{I}{p t}"
            target = "r"
    elif hard:
        form = ctx.rng.choice(["triangle", "volume", "point_slope"])
        a = abs(int(sample_integerish(ctx, exclude_zero=True, prefer_positive=True).value)) or 2
        if form == "triangle":
            latex = r"A = \frac{1}{2} b h \quad \text{Solve for } h."
            text = "A = (1/2)bh. Solve for h."
            ans = r"h = \frac{2A}{b}"
            target = "h"
        elif form == "volume":
            latex = r"V = \ell w h \quad \text{Solve for } w."
            text = "V = lwh. Solve for w."
            ans = r"w = \frac{V}{\ell h}"
            target = "w"
        else:
            x1 = abs(int(sample_integerish(ctx, exclude_zero=True).value)) or 1
            y1 = abs(int(sample_integerish(ctx, exclude_zero=False).value))
            latex = f"y - {y1} = {a}(x - {x1}) \\quad \\text{{Solve for }} y."
            text = f"y - {y1} = {a}(x - {x1}). Solve for y."
            # y = a(x - x1) + y1 = a x + (y1 - a x1)
            b = y1 - a * x1
            if b >= 0:
                ans = f"y = {a}x + {b}" if a != 1 else f"y = x + {b}"
            else:
                ans = f"y = {a}x - {abs(b)}" if a != 1 else f"y = x - {abs(b)}"
            if a == -1:
                ans = f"y = -x + {b}" if b >= 0 else f"y = -x - {abs(b)}"
            target = "y"
    else:
        form = "standard"
        a = abs(int(sample_integerish(ctx, exclude_zero=True, prefer_positive=True).value)) or 2
        b = abs(int(sample_integerish(ctx, exclude_zero=True, prefer_positive=True).value)) or 3
        if a == b:
            b = a + 1
        c = int(sample_integerish(ctx, exclude_zero=False).value)
        latex = f"{a}x + {b}y = {c} \\quad \\text{{Solve for }} y."
        text = f"{a}x + {b}y = {c}. Solve for y."
        ans = f"y = \\frac{{{c} - {a}x}}{{{b}}}"
        target = "y"

    return LiteralEquation(
        latex=latex,
        text=text,
        solution_latex=ans,
        target_var=target,
        form=form,
        upgrades=tuple(sorted(ids)),
        effective_d=eff,
    )
