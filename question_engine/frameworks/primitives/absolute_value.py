"""Absolute value equations & inequalities — linear inner expressions only."""

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
from question_engine.frameworks.primitives.registry import (
    PRIM_EQUATIONS,
    PrimitiveContext,
)

# Reuse equations spend lane for abs structure (no separate budget id required).
PRIM_ABS = "equations"

ABS_EQ_SETTINGS_SCHEMA: dict[str, Any] = {
    "allow_basic": {"type": "bool", "default": True},
    "allow_abs_equals_abs": {"type": "bool", "default": True},
    "allow_coeff_outside": {"type": "bool", "default": True},
    "allow_no_solution": {"type": "bool", "default": True},
}

ABS_INEQ_SETTINGS_SCHEMA: dict[str, Any] = {
    "compound_style": {
        "type": "enum",
        "values": ["and", "or", "auto"],
        "default": "auto",
    },
}

_EQ_UPGRADES: tuple[DifficultyFactor, ...] = (
    DifficultyFactor("linear_inner", 1.0, ("structure",)),
    DifficultyFactor("coeff_outside", 2.0, ("structure",)),
    DifficultyFactor("abs_equals_abs", 3.0, ("structure",)),
    DifficultyFactor("no_solution", 2.5, ("structure",)),
)

_INEQ_UPGRADES: tuple[DifficultyFactor, ...] = (
    DifficultyFactor("linear_inner", 1.0, ("structure",)),
    DifficultyFactor("coeff_outside", 2.0, ("structure",)),
)


@dataclass(frozen=True)
class AbsoluteValueEquation:
    latex: str
    text: str
    solution_latex: str
    solutions: tuple[Fraction, ...]
    var_latex: str
    var_name: str
    form: str
    upgrades: tuple[str, ...]
    effective_d: float
    solution_kind: Literal["unique", "two", "no_solution"] = "two"


@dataclass(frozen=True)
class AbsoluteValueInequality:
    latex: str
    text: str
    solution_latex: str
    var_latex: str
    var_name: str
    op: str
    compound_style: Literal["and", "or"]
    upgrades: tuple[str, ...]
    effective_d: float
    # For number-line: boundary and open/closed
    boundary: Fraction
    inclusive: bool


def sample_absolute_value_equation(ctx: PrimitiveContext) -> AbsoluteValueEquation:
    if not ctx.policy.allow_abs and ctx.policy.family == "linear":
        # Abs is still linear in the unknown; allow when leaf requests it.
        pass
    eff = ctx.effective_d(PRIM_ABS)
    purchased, _, _ = select_upgrades(_EQ_UPGRADES, eff, rng=ctx.rng)
    ids = {f.id for f in purchased}
    settings = ctx.settings_for(PRIM_EQUATIONS)
    if settings.get("allow_abs_equals_abs") is False:
        ids.discard("abs_equals_abs")
    if settings.get("allow_coeff_outside") is False:
        ids.discard("coeff_outside")
    if settings.get("allow_no_solution") is False:
        ids.discard("no_solution")

    for _ in range(14):
        try:
            return _build_eq(ctx, ids, eff)
        except (NicenessError, ValueError, ZeroDivisionError):
            if not ids:
                break
            costs = {f.id: f.cost for f in _EQ_UPGRADES}
            drop = max(ids, key=lambda i: costs.get(i, 0))
            ids.remove(drop)
            ctx.note_degraded(drop)
    return _build_eq(ctx, set(), eff)


def sample_absolute_value_inequality(ctx: PrimitiveContext) -> AbsoluteValueInequality:
    eff = ctx.effective_d(PRIM_ABS)
    purchased, _, _ = select_upgrades(_INEQ_UPGRADES, eff, rng=ctx.rng)
    ids = {f.id for f in purchased}
    for _ in range(12):
        try:
            return _build_ineq(ctx, ids, eff)
        except (NicenessError, ValueError, ZeroDivisionError):
            if not ids:
                break
            costs = {f.id: f.cost for f in _INEQ_UPGRADES}
            drop = max(ids, key=lambda i: costs.get(i, 0))
            ids.remove(drop)
            ctx.note_degraded(drop)
    return _build_ineq(ctx, set(), eff)


def _abs_inner(a: Fraction, var_l: str, b: Fraction) -> str:
    body = coeff_times_var(a, var_l) if a != 0 else ""
    if a == 0:
        return f"|{num_latex(b)}|"
    if b == 0:
        return f"|{body}|"
    if b > 0:
        return f"|{body} + {num_latex(b)}|"
    return f"|{body} - {num_latex(abs(b))}|"


def _fmt_sols(var_l: str, sols: list[Fraction]) -> str:
    if not sols:
        return r"\text{no solution}"
    if len(sols) == 1:
        return f"{var_l} = {num_latex(sols[0])}"
    parts = [f"{var_l} = {num_latex(s)}" for s in sorted(sols)]
    return r" \text{ or } ".join(parts)


def _build_eq(ctx: PrimitiveContext, ids: set[str], eff: float) -> AbsoluteValueEquation:
    var = ctx.sample_variable()
    # No-solution: |ax+b| = negative
    if "no_solution" in ids and ctx.rng.random() < 0.55:
        a = Fraction(sample_integerish(ctx, exclude_zero=True).value)
        b = Fraction(sample_integerish(ctx, exclude_zero=False).value)
        rhs = -abs(int(sample_integerish(ctx, exclude_zero=True).value))
        if rhs >= 0:
            rhs = -1
        latex = f"{_abs_inner(a, var.latex, b)} = {num_latex(Fraction(rhs))}"
        text = f"|{a}{var.name}+{b}| = {rhs}"
        return AbsoluteValueEquation(
            latex=latex,
            text=text,
            solution_latex=r"\text{no solution}",
            solutions=(),
            var_latex=var.latex,
            var_name=var.name,
            form="no_solution",
            upgrades=tuple(sorted(ids)),
            effective_d=eff,
            solution_kind="no_solution",
        )

    if "abs_equals_abs" in ids:
        a = Fraction(sample_integerish(ctx, exclude_zero=True).value)
        c = Fraction(sample_integerish(ctx, exclude_zero=True).value)
        b = Fraction(sample_integerish(ctx, exclude_zero=False).value)
        d = Fraction(sample_integerish(ctx, exclude_zero=False).value)
        if a == c and b == d:
            d = b + Fraction(1)
        if a == -c and b == -d:
            d = b + Fraction(2)
        sols: list[Fraction] = []
        seen: set[Fraction] = set()
        if a != c:
            cand = Fraction(d - b, a - c)
            if cand.denominator == 1 or abs(cand.denominator) <= 6:
                seen.add(cand)
                sols.append(cand)
        if a != -c:
            cand = Fraction(-d - b, a + c)
            if cand not in seen and (cand.denominator == 1 or abs(cand.denominator) <= 6):
                sols.append(cand)
        if not sols:
            raise ValueError("no clean abs=abs solutions")
        latex = f"{_abs_inner(a, var.latex, b)} = {_abs_inner(c, var.latex, d)}"
        text = f"|{a}{var.name}+{b}| = |{c}{var.name}+{d}|"
        return AbsoluteValueEquation(
            latex=latex,
            text=text,
            solution_latex=_fmt_sols(var.latex, sols),
            solutions=tuple(sols),
            var_latex=var.latex,
            var_name=var.name,
            form="abs_equals_abs",
            upgrades=tuple(sorted(ids)),
            effective_d=eff,
            solution_kind="two" if len(sols) > 1 else "unique",
        )

    # Basic / coeff outside: |ax+b| = k or c|x+b| = k
    x0 = Fraction(sample_integerish(ctx, exclude_zero=False).value)
    if "coeff_outside" in ids:
        c_out = abs(int(sample_integerish(ctx, exclude_zero=True, prefer_positive=True).value))
        if c_out < 2:
            c_out = 2
        b = Fraction(sample_integerish(ctx, exclude_zero=False).value)
        inner = abs(x0 + b)
        k = Fraction(c_out) * inner
        # solutions: x = -b ± k/c
        half = k / Fraction(c_out)
        sols = [ -b + half, -b - half ]
        # dedupe
        uniq = []
        for s in sols:
            if s not in uniq:
                uniq.append(s)
        abs_part = _abs_inner(Fraction(1), var.latex, b)
        latex = f"{c_out}{abs_part} = {num_latex(k)}"
        text = f"{c_out}|{var.name}+{b}| = {k}"
        form = "coeff_outside"
    else:
        a = Fraction(1)
        if "linear_inner" in ids:
            a = Fraction(sample_integerish(ctx, exclude_zero=True).value)
            if abs(a) == 1 and ctx.rng.random() < 0.5:
                a = Fraction(2 if ctx.rng.random() < 0.5 else -2)
        b = Fraction(sample_integerish(ctx, exclude_zero=False).value)
        inner = a * x0 + b
        k = abs(inner)
        # |ax+b|=k → ax+b = ±k
        sols = []
        if a != 0:
            for sign in (1, -1):
                sols.append(Fraction(sign * k - b, a))
        uniq = []
        for s in sols:
            if s not in uniq:
                uniq.append(s)
        latex = f"{_abs_inner(a, var.latex, b)} = {num_latex(k)}"
        text = f"|{a}{var.name}+{b}| = {k}"
        form = "basic"

    return AbsoluteValueEquation(
        latex=latex,
        text=text,
        solution_latex=_fmt_sols(var.latex, uniq),
        solutions=tuple(uniq),
        var_latex=var.latex,
        var_name=var.name,
        form=form,
        upgrades=tuple(sorted(ids)),
        effective_d=eff,
        solution_kind="two" if len(uniq) > 1 else ("unique" if uniq else "no_solution"),
    )


def _build_ineq(ctx: PrimitiveContext, ids: set[str], eff: float) -> AbsoluteValueInequality:
    var = ctx.sample_variable()
    # |x| < k → -k < x < k (and); |x| > k → x < -k or x > k
    k = abs(int(sample_integerish(ctx, exclude_zero=True, prefer_positive=True).value))
    if k < 1:
        k = 2
    op = ctx.rng.choice(["<", ">", "\\le", "\\ge"])
    if op in {"<", "\\le"}:
        style: Literal["and", "or"] = "and"
        inclusive = op == "\\le"
        if "linear_inner" in ids:
            b = Fraction(sample_integerish(ctx, exclude_zero=False).value)
            abs_l = _abs_inner(Fraction(1), var.latex, b)
            # |x+b| < k → -k-b < x < k-b  (shift)
            lo, hi = -k - b, k - b
            if inclusive:
                sol = f"{num_latex(lo)} \\le {var.latex} \\le {num_latex(hi)}"
            else:
                sol = f"{num_latex(lo)} < {var.latex} < {num_latex(hi)}"
            latex = f"{abs_l} {op} {k}"
        else:
            abs_l = f"|{var.latex}|"
            if inclusive:
                sol = f"-{k} \\le {var.latex} \\le {k}"
            else:
                sol = f"-{k} < {var.latex} < {k}"
            latex = f"{abs_l} {op} {k}"
            lo, hi = Fraction(-k), Fraction(k)
        text = latex.replace("\\le", "<=").replace("\\ge", ">=")
        return AbsoluteValueInequality(
            latex=latex,
            text=text,
            solution_latex=sol,
            var_latex=var.latex,
            var_name=var.name,
            op=op,
            compound_style=style,
            upgrades=tuple(sorted(ids)),
            effective_d=eff,
            boundary=Fraction(k),
            inclusive=inclusive,
        )

    # greater-than family → or
    style = "or"
    inclusive = op == "\\ge"
    abs_l = f"|{var.latex}|"
    if inclusive:
        sol = f"{var.latex} \\le -{k} \\text{{ or }} {var.latex} \\ge {k}"
    else:
        sol = f"{var.latex} < -{k} \\text{{ or }} {var.latex} > {k}"
    latex = f"{abs_l} {op} {k}"
    text = latex.replace("\\le", "<=").replace("\\ge", ">=")
    return AbsoluteValueInequality(
        latex=latex,
        text=text,
        solution_latex=sol,
        var_latex=var.latex,
        var_name=var.name,
        op=op,
        compound_style=style,
        upgrades=tuple(sorted(ids)),
        effective_d=eff,
        boundary=Fraction(k),
        inclusive=inclusive,
    )
