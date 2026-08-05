"""Proportions and literal equations — linear, policy max_degree=1."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import math
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
    from question_engine.frameworks.number import (
        _build_k_with_meaningful_steps,
        _target_meaningful_cancel_steps,
        meaningful_cancel_steps,
    )

    var = ctx.sample_variable()
    # Meaningful-effort cores: inflate with non-10ⁿ cancel steps as D rises.
    target = _target_meaningful_cancel_steps(eff)
    k_max = max(6, 4 + int(eff))
    if target <= 0:
        a, b, c = 2, 3, 4
        k = 1
    else:
        k = _build_k_with_meaningful_steps(target, k_max, min_k=2 if eff >= 5 else 1)
        core_a, core_b = 2, 3
        # Vary small coprime cores.
        cores = [(2, 3), (3, 4), (2, 5), (3, 5), (4, 5), (2, 7), (3, 7)]
        core_a, core_b = ctx.rng.choice(cores)
        a, b = core_a * k, core_b * k
        # Third part also uses a related multiple so cross-multiply isn't trivial 1.
        m = max(2, min(9, 2 + int(eff // 4)))
        c = core_a * m if "variable_in_denom" in ids else core_b * m
        if c < 1:
            c = max(2, m)

    # Prefer multi_step_clear when both upgrades purchased (was shadowed before).
    if "multi_step_clear" in ids and (
        "variable_in_denom" not in ids or ctx.rng.random() < 0.55
    ):
        d_add = int(sample_integerish(ctx, exclude_zero=False).value)
        if abs(d_add) > 8:
            d_add = 3 if d_add > 0 else -3
        # a/b = (x+d)/c → x = (a c)/b - d
        sol = Fraction(a * c, b) - d_add
        inner = f"{var.latex} + {d_add}" if d_add >= 0 else f"{var.latex} - {abs(d_add)}"
        latex = f"\\frac{{{a}}}{{{b}}} = \\frac{{{inner}}}{{{c}}}"
        text = f"{a}/{b} = ({var.name}+{d_add})/{c}"
        used = {"multi_step_clear"}
        if meaningful_cancel_steps(math.gcd(a, b)) >= 2:
            used.add("meaningful_cancel")
    elif "variable_in_denom" in ids:
        # a/x = b/c  → x = a c / b
        # Rebuild so left numerator carries inflate effort.
        sol = Fraction(a * c, b)
        latex = f"\\frac{{{a}}}{{{var.latex}}} = \\frac{{{b}}}{{{c}}}"
        text = f"{a}/{var.name} = {b}/{c}"
        used = {"variable_in_denom"}
        if meaningful_cancel_steps(math.gcd(a, b)) >= 2:
            used.add("meaningful_cancel")
    else:
        # a/b = x/c → x = a c / b
        sol = Fraction(a * c, b)
        latex = f"\\frac{{{a}}}{{{b}}} = \\frac{{{var.latex}}}{{{c}}}"
        text = f"{a}/{b} = {var.name}/{c}"
        used = set()
        if meaningful_cancel_steps(math.gcd(a, b)) >= 1:
            used.add("meaningful_cancel")

    return ProportionEquation(
        latex=latex,
        text=text,
        solution_latex=f"{var.latex} = {num_latex(sol)}",
        solution=sol,
        var_latex=var.latex,
        var_name=var.name,
        upgrades=tuple(sorted(used | (ids & {"variable_in_denom", "multi_step_clear"}))),
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
