"""One-step / two-step / multi-step linear inequalities — Layer 1 on numbers + variables.

Mirrors ``equations.py``. Multi-step composes expand/simplify expressions on
each side (same as multi-step equations) and uses the unbounded op-growth
formula::

    n_ops(D) = 3 + floor(log2(1 + D / STEP_SCALE))
    STEP_SCALE = 2.0

When the variable coefficient is negative on the isolation step, the inequality
direction is flipped (same as one-/two-step). Number-line graphing is left to
presentation layers when catalog leaves request it.
"""

from __future__ import annotations

import math
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
from question_engine.frameworks.primitives.equations import (
    STEP_SCALE,
    compose_rhs_for_solution,
    min_d_for_n_ops,
    target_n_ops,
)
from question_engine.frameworks.primitives.expand_simplify import (
    sample_linear_expression_to_simplify,
)
from question_engine.frameworks.primitives.registry import PRIM_INEQUALITIES, PrimitiveContext
from question_engine.frameworks.primitives.variables import SampledVariable

INEQUALITIES_SETTINGS_SCHEMA: dict[str, Any] = {
    "force_steps": {
        "type": "enum",
        "values": ["auto", "one", "two", "multi"],
        "default": "auto",
    },
}

_UPGRADES: tuple[DifficultyFactor, ...] = (
    DifficultyFactor("two_step", 3.0, ("structure",)),
    DifficultyFactor("multiply_divide", 1.0, ("structure",)),
    DifficultyFactor("negative_coeff", 2.0, ("structure",)),
    DifficultyFactor("non_strict", 0.5, ("structure",)),
)

StepMode = Literal["one", "two", "multi"]
IneqOp = Literal["<", ">", "\\le", "\\ge"]

_OPS_STRICT: tuple[IneqOp, ...] = ("<", ">")
_OPS_ALL: tuple[IneqOp, ...] = ("<", ">", "\\le", "\\ge")
_OP_TEXT = {"<": "<", ">": ">", "\\le": "<=", "\\ge": ">="}
_OP_FLIP = {"<": ">", ">": "<", "\\le": "\\ge", "\\ge": "\\le"}

# Re-export for audits / tests that import from inequalities.
__all__ = [
    "INEQUALITIES_SETTINGS_SCHEMA",
    "LinearInequality",
    "STEP_SCALE",
    "min_d_for_n_ops",
    "sample_linear_inequality",
    "target_n_ops",
]


@dataclass(frozen=True)
class LinearInequality:
    latex: str
    text: str
    solution_latex: str  # e.g. x < 3
    solution_value: Fraction
    op: IneqOp
    var_latex: str
    var_name: str
    steps: StepMode
    n_ops: int
    flipped: bool
    upgrades: tuple[str, ...]
    effective_d: float


def sample_linear_inequality(
    ctx: PrimitiveContext,
    *,
    force_steps: StepMode | None = None,
) -> LinearInequality:
    eff = ctx.effective_d(PRIM_INEQUALITIES)
    settings = ctx.settings_for(PRIM_INEQUALITIES)
    raw_force = force_steps or str(settings.get("force_steps", "auto")).strip().lower()
    if raw_force in {"one", "1", "one_step"}:
        force: StepMode | None = "one"
    elif raw_force in {"two", "2", "two_step"}:
        force = "two"
    elif raw_force in {"multi", "multi_step", "multistep", "3", "three"}:
        force = "multi"
    else:
        force = None

    if force == "multi":
        return _sample_multi(ctx, eff)

    purchased, _, _ = select_upgrades(_UPGRADES, eff, rng=ctx.rng)
    ids = {f.id for f in purchased}
    if force == "one":
        ids.discard("two_step")
    elif force == "two":
        ids.add("two_step")

    for _ in range(12):
        try:
            return _build(ctx, ids, eff)
        except (NicenessError, ValueError, ZeroDivisionError):
            if not ids:
                break
            costs = {f.id: f.cost for f in _UPGRADES}
            droppable = [i for i in ids if i != "two_step" or force != "two"]
            if not droppable:
                break
            drop = max(droppable, key=lambda i: costs.get(i, 0))
            ids.remove(drop)
            ctx.note_degraded(drop)

    return _build(ctx, {"two_step"} if force == "two" else set(), eff)


def _pick_op(ctx: PrimitiveContext, ids: set[str]) -> IneqOp:
    pool = _OPS_ALL if "non_strict" in ids else _OPS_STRICT
    return ctx.rng.choice(pool)


def _maybe_neg(ctx: PrimitiveContext, ids: set[str], value: Fraction) -> Fraction:
    if "negative_coeff" in ids and ctx.rng.random() < 0.5:
        return -abs(value) if value != 0 else Fraction(-1)
    if "negative_coeff" not in ids and value < 0:
        return abs(value) if value != 0 else Fraction(1)
    return value


def _sol_latex(var_latex: str, op: IneqOp, value: Fraction) -> str:
    return f"{var_latex} {op} {num_latex(value)}"


def _finish(
    *,
    latex: str,
    text: str,
    boundary: Fraction,
    sol_op: IneqOp,
    var: SampledVariable,
    steps: StepMode,
    n_ops: int,
    flipped: bool,
    upgrades: tuple[str, ...],
    eff: float,
) -> LinearInequality:
    return LinearInequality(
        latex=latex,
        text=text,
        solution_latex=_sol_latex(var.latex, sol_op, boundary),
        solution_value=boundary,
        op=sol_op,
        var_latex=var.latex,
        var_name=var.name,
        steps=steps,
        n_ops=n_ops,
        flipped=flipped,
        upgrades=upgrades,
        effective_d=eff,
    )


def _build(ctx: PrimitiveContext, ids: set[str], eff: float) -> LinearInequality:
    var = ctx.sample_variable()
    boundary = sample_integerish(ctx, exclude_zero=False).value
    op = _pick_op(ctx, ids)
    two_step = "two_step" in ids
    prefer_md = "multiply_divide" in ids

    if not two_step:
        return _one_step(ctx, ids, eff, var, boundary, op, prefer_md)
    return _two_step(ctx, ids, eff, var, boundary, op)


def _one_step(ctx, ids, eff, var, boundary, op, prefer_md) -> LinearInequality:
    op_pool = ["add", "sub", "mul", "div"] if prefer_md else ["add", "sub"]
    kind = ctx.rng.choice(["mul", "div"] if prefer_md and ctx.rng.random() < 0.5 else op_pool)
    flipped = False
    sol_op = op

    if kind in {"add", "sub"}:
        a = sample_integerish(ctx, exclude_zero=True)
        a_v = _maybe_neg(ctx, ids, a.value)
        if kind == "add":
            rhs = boundary + a_v
            left_l = (
                f"{var.latex} + {num_latex(a_v)}"
                if a_v >= 0
                else f"{var.latex} - {num_latex(abs(a_v))}"
            )
            left_t = (
                f"{var.name} + {num_latex(a_v)}"
                if a_v >= 0
                else f"{var.name} - {num_latex(abs(a_v))}"
            )
        else:
            rhs = boundary - a_v
            left_l = (
                f"{var.latex} - {num_latex(a_v)}"
                if a_v >= 0
                else f"{var.latex} + {num_latex(abs(a_v))}"
            )
            left_t = (
                f"{var.name} - {num_latex(a_v)}"
                if a_v >= 0
                else f"{var.name} + {num_latex(abs(a_v))}"
            )
        latex = f"{left_l} {op} {num_latex(rhs)}"
        text = f"{left_t} {_OP_TEXT[op]} {num_latex(rhs)}"
    elif kind == "mul":
        a = sample_integerish(ctx, exclude_zero=True)
        a_v = _maybe_neg(ctx, ids, a.value)
        if a_v == 0 or abs(a_v) == 1:
            a_v = Fraction(-2 if a_v < 0 else 2)
        rhs = a_v * boundary
        left_l = coeff_times_var(a_v, var.latex)
        left_t = coeff_times_var(a_v, var.name)
        latex = f"{left_l} {op} {num_latex(rhs)}"
        text = f"{left_t} {_OP_TEXT[op]} {num_latex(rhs)}"
        if a_v < 0:
            flipped = True
            sol_op = _OP_FLIP[op]
    else:
        a = sample_integerish(ctx, exclude_zero=True, prefer_positive=True)
        a_v = abs(a.value) if a.value != 0 else Fraction(2)
        a_v = _maybe_neg(ctx, ids, a_v)
        if a_v == 0:
            a_v = Fraction(2)
        rhs = boundary / a_v
        latex = f"\\frac{{{var.latex}}}{{{num_latex(a_v)}}} {op} {num_latex(rhs)}"
        text = f"({var.name})/({num_latex(a_v)}) {_OP_TEXT[op]} {num_latex(rhs)}"
        if a_v < 0:
            flipped = True
            sol_op = _OP_FLIP[op]

    return _finish(
        latex=latex,
        text=text,
        boundary=boundary,
        sol_op=sol_op,
        var=var,
        steps="one",
        n_ops=1,
        flipped=flipped,
        upgrades=tuple(sorted(ids)),
        eff=eff,
    )


def _two_step(ctx, ids, eff, var, boundary, op) -> LinearInequality:
    a = sample_integerish(ctx, exclude_zero=True)
    b = sample_integerish(ctx, exclude_zero=True)
    a_v = _maybe_neg(ctx, ids, a.value)
    b_v = _maybe_neg(ctx, ids, b.value)
    if a_v == 0:
        a_v = Fraction(2)
    rhs = a_v * boundary + b_v
    left = coeff_times_var(a_v, var.latex)
    left_t = coeff_times_var(a_v, var.name)
    if b_v >= 0:
        left = f"{left} + {num_latex(b_v)}"
        left_t = f"{left_t} + {num_latex(b_v)}"
    else:
        left = f"{left} - {num_latex(abs(b_v))}"
        left_t = f"{left_t} - {num_latex(abs(b_v))}"
    latex = f"{left} {op} {num_latex(rhs)}"
    text = f"{left_t} {_OP_TEXT[op]} {num_latex(rhs)}"
    flipped = a_v < 0
    sol_op = _OP_FLIP[op] if flipped else op
    return _finish(
        latex=latex,
        text=text,
        boundary=boundary,
        sol_op=sol_op,
        var=var,
        steps="two",
        n_ops=2,
        flipped=flipped,
        upgrades=tuple(sorted(ids)),
        eff=eff,
    )


# --- Multi-step (mirrors equations; tracks flip from final leading coeff) -----


def _sample_multi(ctx: PrimitiveContext, eff: float) -> LinearInequality:
    n_ops = target_n_ops(eff)
    for _ in range(14):
        try:
            return _build_multi(ctx, eff, n_ops)
        except (NicenessError, ValueError, ZeroDivisionError):
            continue
    return _build_multi(ctx, eff, 3)


def _build_multi(ctx: PrimitiveContext, eff: float, n_ops: int) -> LinearInequality:
    """Compose expand/simplify expressions on one or both sides (mirrors equations)."""
    var = ctx.sample_variable()
    boundary = sample_integerish(ctx, exclude_zero=False).value
    op = ctx.rng.choice(_OPS_ALL if eff >= 4 else _OPS_STRICT)
    n_ops = max(3, int(n_ops))

    left = sample_linear_expression_to_simplify(ctx, d=eff, var=var)
    if left.coeff_a == 0:
        raise ValueError("left side has no variable after simplify")

    use_both = n_ops >= 4
    tags_list = ["compose_simplify", f"ops:{n_ops}", f"groups:{left.n_groups}"]
    if left.nested:
        tags_list.append("nested")

    if use_both:
        right_l, right_t, right_groups, a_r = compose_rhs_for_solution(
            ctx,
            eff=eff,
            n_ops=n_ops,
            var=var,
            left_a=left.coeff_a,
            left_b=left.coeff_b,
            solution=boundary,
        )
        leading = left.coeff_a - a_r
        tags_list.append("both_sides")
        tags_list.append(f"right_groups:{right_groups}")
    else:
        leading = left.coeff_a
        rhs = left.coeff_a * boundary + left.coeff_b
        right_l, right_t = num_latex(rhs), num_latex(rhs)

    latex = f"{left.latex} {op} {right_l}"
    text = f"{left.text} {_OP_TEXT[op]} {right_t}"
    flipped = leading < 0
    sol_op = _OP_FLIP[op] if flipped else op
    return _finish(
        latex=latex,
        text=text,
        boundary=boundary,
        sol_op=sol_op,
        var=var,
        steps="multi",
        n_ops=n_ops,
        flipped=flipped,
        upgrades=tuple(tags_list),
        eff=eff,
    )
