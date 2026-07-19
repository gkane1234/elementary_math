"""Shared expression-structure engine — numeric OOO and algebraic linear trees.

One structural DNA for both modes: sample a binary expression tree (operators at
internal nodes, leaves = numbers or affine atoms), place parentheses with
intentional variety, and scale complexity with difficulty ``D``::

    n_leaves(D) = 1 + floor(log2(1 + D / LEAF_SCALE))   # LEAF_SCALE = 1.5
    nest_budget(D) = floor(log2(1 + D / NEST_SCALE))     # NEST_SCALE = 3.0
    scale_budget(D) = … ×/÷ wrappers after MUL_UNLOCK

**Numeric** mode (order of operations): leaves are Layer-0 numbers; result is
an evaluated ``Fraction``. Optional small exponents when D is high.

**Algebraic** mode (evaluate / expand-simplify / multi-step sides): leaves are
constants or ``coeff·var``; result simplifies to affine ``a·var + b``. Linear
policy forbids var×var; ×/÷ use nonzero constants only.

Callers share this so OOO, expand/simplify, evaluate, and multi-step equation
sides do not each invent a different paren/op pattern.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Literal

from question_engine.frameworks.niceness import NicenessError
from question_engine.frameworks.primitives._algebra_render import (
    coeff_times_var,
    join_signed_terms,
    num_latex,
)
from question_engine.frameworks.primitives.presentation import (
    DisplayPiece,
    PresentationStyle,
    maybe_clutter,
    presentation_for_ctx,
    render_addition,
    render_division,
    render_product,
    render_subtraction,
)
from question_engine.frameworks.primitives.registry import (
    PRIM_EXPAND_SIMPLIFY,
    PRIM_NUMBERS,
    PrimitiveContext,
)
from question_engine.frameworks.primitives.variables import SampledVariable

ExprMode = Literal["numeric", "algebraic"]

LEAF_SCALE = 1.5
NEST_SCALE = 3.0
SCALE_OP_SCALE = 2.5
MUL_UNLOCK = 2.0
DIV_UNLOCK = 4.0
EXP_UNLOCK = 3.0

# Shape association biases (randomized per sample for variety).
_ASSOC_LEFT = "left"
_ASSOC_RIGHT = "right"
_ASSOC_BALANCED = "balanced"
_ASSOC_CHAIN = "chain"  # flat sum/product chain with optional mid parens


def target_n_leaves(d: float) -> int:
    from question_engine.frameworks.primitives.difficulty_knobs import fget

    d = max(0.0, float(d))
    scale = fget("expression_structure", "leaf_scale", LEAF_SCALE)
    return 1 + int(math.floor(math.log2(1.0 + d / scale)))


def target_nest_budget(d: float) -> int:
    from question_engine.frameworks.primitives.difficulty_knobs import fget

    d = max(0.0, float(d))
    scale = fget("expression_structure", "nest_scale", NEST_SCALE)
    return int(math.floor(math.log2(1.0 + d / scale)))


def target_scale_budget(d: float) -> int:
    from question_engine.frameworks.primitives.difficulty_knobs import fget

    d = max(0.0, float(d))
    mul_unlock = fget("expression_structure", "mul_unlock_d", MUL_UNLOCK)
    scale = fget("expression_structure", "scale_op_scale", SCALE_OP_SCALE)
    if d < mul_unlock:
        return 0
    return int(math.floor(math.log2(1.0 + (d - mul_unlock) / scale)))


def op_pool_for_d(d: float, *, mode: ExprMode, allow_exponent: bool) -> tuple[str, ...]:
    from question_engine.frameworks.primitives.difficulty_knobs import fget

    d = max(0.0, float(d))
    ops: list[str] = ["+", "-"]
    if d >= fget("expression_structure", "mul_unlock_d", MUL_UNLOCK):
        ops.append("*")
    if d >= fget("expression_structure", "div_unlock_d", DIV_UNLOCK) and mode == "algebraic":
        ops.append("/")
    if allow_exponent and mode == "numeric" and d >= fget(
        "expression_structure", "exp_unlock_d", EXP_UNLOCK
    ):
        ops.append("^")
    return tuple(ops)


def min_d_for_n_leaves(n: int) -> float:
    from question_engine.frameworks.primitives.difficulty_knobs import fget

    n = max(1, int(n))
    if n <= 1:
        return 0.0
    scale = fget("expression_structure", "leaf_scale", LEAF_SCALE)
    return scale * (2 ** (n - 1) - 1)


@dataclass
class _Node:
    """Affine ``a·var + b`` (numeric ⇒ a=0, value=b) plus display metadata."""

    a: Fraction
    b: Fraction
    latex: str
    text: str
    n_leaves: int = 1
    n_parens: int = 0
    n_ops: int = 0
    nest_depth: int = 0
    used_mul: bool = False
    used_div: bool = False
    used_exp: bool = False
    is_wrapped: bool = False
    ops: list[str] = field(default_factory=list)
    shape_bits: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class StructuredExpression:
    latex: str
    text: str
    value: Fraction
    coeff_a: Fraction
    coeff_b: Fraction
    var_name: str | None
    var_latex: str | None
    n_leaves: int
    n_parens: int
    nest_depth: int
    n_ops: int
    ops_used: tuple[str, ...]
    shape_id: str
    upgrades: tuple[str, ...]
    effective_d: float
    mode: ExprMode
    simplified_latex: str = ""
    simplified_text: str = ""
    n_groups: int = 0
    n_lone: int = 0


def sample_structured_expression(
    ctx: PrimitiveContext,
    *,
    mode: ExprMode = "algebraic",
    d: float | None = None,
    var: SampledVariable | None = None,
    force_var: bool = False,
    prefer_distribute: bool = False,
    allow_exponent: bool | None = None,
    strip_outer_parens: bool = True,
) -> StructuredExpression:
    """Sample one structured expression (numeric or algebraic linear)."""
    if d is None:
        # Prefer expand_simplify layer when present; else numbers (OOO often
        # budgets under ooo — callers should pass explicit d).
        d = ctx.effective_d(PRIM_EXPAND_SIMPLIFY)
        if d <= 0:
            d = ctx.effective_d(PRIM_NUMBERS)
    eff = max(0.0, float(d))

    if mode == "algebraic":
        if ctx.policy.max_degree < 1 and force_var:
            raise ValueError("algebraic mode requires degree ≥ 1 when force_var")
        var = var or ctx.sample_variable()
    else:
        var = None

    if allow_exponent is None:
        allow_exponent = mode == "numeric"

    # One presentation style for the whole tree (commute / flip / multiply glyph).
    presentation_for_ctx(ctx, d=eff)

    for _ in range(14):
        try:
            node = _build_tree(
                ctx,
                mode=mode,
                eff=eff,
                var=var,
                force_var=force_var or (mode == "algebraic" and prefer_distribute),
                prefer_distribute=prefer_distribute,
                allow_exponent=bool(allow_exponent),
            )
            if strip_outer_parens and node.is_wrapped:
                node = _strip_outer(node)
            if mode == "algebraic" and force_var and node.a == 0:
                raise ValueError("expected variable term")
            if mode == "numeric" and node.n_ops == 0 and target_n_leaves(eff) > 1:
                raise ValueError("too trivial for D")
            return _finish(node, mode=mode, var=var, eff=eff)
        except (NicenessError, ValueError, ZeroDivisionError):
            continue
    return _fallback(ctx, mode=mode, var=var, eff=eff, force_var=force_var)


def append_constant_to_expression(
    latex: str,
    text: str,
    const: Fraction,
) -> tuple[str, str]:
    """Append ``± const`` to a display (equation RHS adjustment)."""
    if const == 0:
        return latex, text
    if const > 0:
        return f"{latex} + {num_latex(const)}", f"{text} + {num_latex(const)}"
    return f"{latex} - {num_latex(abs(const))}", f"{text} - {num_latex(abs(const))}"


# --- Build -------------------------------------------------------------------


def _build_tree(
    ctx: PrimitiveContext,
    *,
    mode: ExprMode,
    eff: float,
    var: SampledVariable | None,
    force_var: bool,
    prefer_distribute: bool,
    allow_exponent: bool,
) -> _Node:
    n_leaves = target_n_leaves(eff)
    nest = target_nest_budget(eff)
    scale = target_scale_budget(eff)
    pool = op_pool_for_d(eff, mode=mode, allow_exponent=allow_exponent)

    if prefer_distribute and mode == "algebraic":
        # Bias: one or more k(…) groups joined by +/− (expand-then-simplify look).
        return _build_distribute_style(
            ctx,
            var=var,  # type: ignore[arg-type]
            n_leaves=n_leaves,
            nest=nest,
            scale=max(scale, 1 if eff >= MUL_UNLOCK else 0),
            pool=pool,
            force_var=force_var,
            eff=eff,
        )

    assoc = _pick_assoc(ctx, n_leaves, nest)
    node = _sample_expr(
        ctx,
        mode=mode,
        var=var,
        n_leaves=n_leaves,
        nest=nest,
        scale=scale,
        pool=pool,
        force_var=force_var,
        assoc=assoc,
        allow_exponent=allow_exponent,
    )
    node.shape_bits.append(f"assoc:{assoc}")
    return node


def _pick_assoc(ctx: PrimitiveContext, n_leaves: int, nest: int) -> str:
    if n_leaves <= 2:
        return _ASSOC_CHAIN
    choices = [_ASSOC_LEFT, _ASSOC_RIGHT, _ASSOC_BALANCED, _ASSOC_CHAIN]
    # Deeper nest → prefer left/right nesting over flat chain.
    if nest >= 2:
        choices.extend([_ASSOC_LEFT, _ASSOC_RIGHT])
    return ctx.rng.choice(choices)


def _sample_expr(
    ctx: PrimitiveContext,
    *,
    mode: ExprMode,
    var: SampledVariable | None,
    n_leaves: int,
    nest: int,
    scale: int,
    pool: tuple[str, ...],
    force_var: bool,
    assoc: str,
    allow_exponent: bool,
) -> _Node:
    n_leaves = max(1, int(n_leaves))
    nest = max(0, int(nest))
    scale = max(0, int(scale))

    if n_leaves == 1:
        leaf = _leaf(ctx, mode=mode, var=var, force_var=force_var)
        if allow_exponent and mode == "numeric" and "^" in pool and ctx.rng.random() < 0.22:
            leaf = _apply_square(ctx, leaf)
        return _maybe_scale_node(
            ctx,
            leaf,
            mode=mode,
            var=var,
            nest=nest,
            scale=scale,
            pool=pool,
        )

    # Split leaf budget by association style.
    if assoc == _ASSOC_LEFT:
        left_n, right_n = n_leaves - 1, 1
    elif assoc == _ASSOC_RIGHT:
        left_n, right_n = 1, n_leaves - 1
    elif assoc == _ASSOC_BALANCED:
        left_n = max(1, n_leaves // 2)
        right_n = n_leaves - left_n
    else:  # chain — still binary recurse but prefer balanced-ish random split
        left_n = ctx.rng.randint(1, n_leaves - 1)
        right_n = n_leaves - left_n

    # Nest budget: concentrate on one side for deeper trees, or split.
    if nest >= 2 and ctx.rng.random() < 0.5:
        if ctx.rng.random() < 0.5:
            left_nest, right_nest = nest - 1, 0
        else:
            left_nest, right_nest = 0, nest - 1
        outer_paren = 1 if nest > 0 and ctx.rng.random() < 0.4 else 0
    else:
        outer_paren = 1 if nest > 0 and ctx.rng.random() < 0.45 else 0
        inner = nest - outer_paren
        left_nest = inner // 2
        right_nest = inner - left_nest

    left_scale = scale // 2
    right_scale = scale - left_scale
    # Child assoc: often inherit, sometimes flip for variety.
    child_assoc = assoc
    if ctx.rng.random() < 0.35:
        child_assoc = _pick_assoc(ctx, max(left_n, right_n), max(left_nest, right_nest))

    left = _sample_expr(
        ctx,
        mode=mode,
        var=var,
        n_leaves=left_n,
        nest=left_nest,
        scale=left_scale,
        pool=pool,
        force_var=force_var,
        assoc=child_assoc,
        allow_exponent=allow_exponent,
    )
    right = _sample_expr(
        ctx,
        mode=mode,
        var=var,
        n_leaves=right_n,
        nest=right_nest,
        scale=right_scale,
        pool=pool,
        force_var=False,
        assoc=child_assoc,
        allow_exponent=allow_exponent,
    )

    op = _choose_combine_op(ctx, pool, left, right, mode=mode)
    combined = _combine(ctx, left, right, op, mode=mode, var=var)

    if outer_paren:
        combined = _wrap(combined)
        combined.shape_bits.append("outer_paren")

    # Occasional outer constant scale (algebraic distribute look / numeric factor).
    if scale > 0 and "*" in pool and ctx.rng.random() < 0.4:
        combined = _scale_const(ctx, combined, mode=mode, var=var, op="*")
    elif scale > 0 and "/" in pool and mode == "algebraic" and ctx.rng.random() < 0.2:
        combined = _scale_const(ctx, combined, mode=mode, var=var, op="/")

    return combined


def _build_distribute_style(
    ctx: PrimitiveContext,
    *,
    var: SampledVariable,
    n_leaves: int,
    nest: int,
    scale: int,
    pool: tuple[str, ...],
    force_var: bool,
    eff: float,
) -> _Node:
    """Multiple constant×(linear) groups + optional lone constants."""
    n_groups = max(1, min(n_leaves, 1 + nest + (1 if scale else 0)))
    if n_leaves >= 3:
        n_groups = max(n_groups, 2) if eff >= 1.5 else n_groups
    n_lone = max(0, target_nest_budget(eff) // 2) if eff >= 3 else (1 if eff >= 1.5 and ctx.rng.random() < 0.4 else 0)

    parts: list[_Node] = []
    need_var = force_var
    for i in range(n_groups):
        depth = 1 + (nest if i == 0 else max(0, nest - i))
        depth = max(1, min(depth, 1 + nest))
        g = _nested_distribute_group(ctx, var, depth=depth)
        parts.append(g)
        if g.a != 0:
            need_var = False
    if need_var:
        parts.append(_nested_distribute_group(ctx, var, depth=1))

    for _ in range(n_lone):
        c = _small_const(ctx, exclude_zero=True)
        parts.append(
            _Node(
                a=Fraction(0),
                b=c,
                latex=num_latex(c),
                text=num_latex(c),
                shape_bits=["lone"],
            )
        )

    ctx.rng.shuffle(parts)
    acc = parts[0]
    for p in parts[1:]:
        acc = _combine(ctx, acc, p, "+", mode="algebraic", var=var)
    acc.shape_bits.append(f"distribute_groups:{n_groups}")
    acc.shape_bits.append(f"lone:{n_lone}")
    return acc


def _nested_distribute_group(
    ctx: PrimitiveContext,
    var: SampledVariable,
    *,
    depth: int,
) -> _Node:
    """depth 1 → k(ax+b); depth 2 → k(m(ax+b)±c); etc."""
    depth = max(1, int(depth))
    if depth == 1:
        k = _small_const(ctx, exclude_zero=True, prefer_abs_ge_2=True)
        inner_a = _small_const(ctx, exclude_zero=True)
        inner_b = _small_const(ctx, exclude_zero=False)
        inner = _Node(
            a=inner_a,
            b=inner_b,
            latex=_render_affine(inner_a, inner_b, var)[0],
            text=_render_affine(inner_a, inner_b, var)[1],
            n_leaves=1 if inner_a == 0 or inner_b == 0 else 2,
            n_ops=0 if inner_a == 0 or inner_b == 0 else 1,
        )
        return _wrap_scale(k, inner, ctx=ctx)
    k = _small_const(ctx, exclude_zero=True, prefer_abs_ge_2=True)
    inner = _nested_distribute_group(ctx, var, depth=depth - 1)
    c = _small_const(ctx, exclude_zero=True)
    if c >= 0:
        body = _Node(
            a=inner.a,
            b=inner.b + c,
            latex=f"{inner.latex} + {num_latex(c)}",
            text=f"{inner.text} + {num_latex(c)}",
            n_leaves=inner.n_leaves + 1,
            n_parens=inner.n_parens,
            n_ops=inner.n_ops + 1,
            nest_depth=inner.nest_depth,
            used_mul=inner.used_mul,
            ops=inner.ops + ["+"],
            shape_bits=inner.shape_bits + ["nest_add"],
        )
    else:
        body = _Node(
            a=inner.a,
            b=inner.b + c,
            latex=f"{inner.latex} - {num_latex(abs(c))}",
            text=f"{inner.text} - {num_latex(abs(c))}",
            n_leaves=inner.n_leaves + 1,
            n_parens=inner.n_parens,
            n_ops=inner.n_ops + 1,
            nest_depth=inner.nest_depth,
            used_mul=inner.used_mul,
            ops=inner.ops + ["-"],
            shape_bits=inner.shape_bits + ["nest_sub"],
        )
    return _wrap_scale(k, body, ctx=ctx)


def _style(ctx: PrimitiveContext | None) -> PresentationStyle:
    if ctx is None:
        return PresentationStyle.schoolbook()
    cached = getattr(ctx, "_presentation_style", None)
    if isinstance(cached, PresentationStyle):
        return cached
    return presentation_for_ctx(ctx)


def _wrap_scale(
    k: Fraction,
    inner: _Node,
    *,
    extra_leaves: int = 0,
    mode: ExprMode = "algebraic",
    ctx: PrimitiveContext | None = None,
) -> _Node:
    style = _style(ctx)
    rng = ctx.rng if ctx is not None else None
    if mode == "numeric" and inner.a == 0 and inner.n_ops == 0 and not inner.is_wrapped:
        left = DisplayPiece(num_latex(k), num_latex(k))
        right = DisplayPiece(inner.latex, inner.text)
        if rng is not None and (
            style.strange_mode or style.explicit_multiply or style.clutter_amount > 0
        ):
            latex, text = render_product([left, right], style, rng)
        elif style.commute_mul:
            latex = f"{right.latex} \\times {left.latex}"
            text = f"{right.text} * {left.text}"
        else:
            latex = f"{left.latex} \\times {right.latex}"
            text = f"{left.text} * {right.text}"
        return _Node(
            a=Fraction(0),
            b=k * inner.b,
            latex=latex,
            text=text,
            n_leaves=inner.n_leaves + max(0, extra_leaves),
            n_parens=inner.n_parens,
            n_ops=inner.n_ops + 1,
            nest_depth=inner.nest_depth,
            used_mul=True,
            ops=inner.ops + ["*"],
            shape_bits=inner.shape_bits + ["*"],
        )
    wrapped = _wrap(inner) if not inner.is_wrapped else inner
    if k == 1:
        latex, text = wrapped.latex, wrapped.text
    elif k == -1:
        latex, text = f"-{wrapped.latex}", f"-{wrapped.text}"
    else:
        outer = DisplayPiece(num_latex(k), num_latex(k))
        group = DisplayPiece(wrapped.latex, wrapped.text)
        if rng is not None:
            latex, text = render_product([outer, group], style, rng)
        else:
            latex = f"{outer.latex}{group.latex}"
            text = f"{outer.text}{group.text}"
    return _Node(
        a=k * inner.a,
        b=k * inner.b,
        latex=latex,
        text=text,
        n_leaves=inner.n_leaves + max(0, extra_leaves),
        n_parens=wrapped.n_parens,
        n_ops=inner.n_ops + 1,
        nest_depth=wrapped.nest_depth,
        used_mul=True,
        used_div=inner.used_div,
        ops=inner.ops + ["*"],
        shape_bits=inner.shape_bits + ["dist"],
        is_wrapped=False,
    )


# --- Leaves / combine / scale ------------------------------------------------


def _leaf(
    ctx: PrimitiveContext,
    *,
    mode: ExprMode,
    var: SampledVariable | None,
    force_var: bool,
) -> _Node:
    if mode == "numeric" or var is None:
        n = ctx.sample_number(exclude_zero=True)
        return _Node(
            a=Fraction(0),
            b=n.value,
            latex=n.latex,
            text=n.latex,
            shape_bits=["num"],
        )
    if force_var or ctx.rng.random() < 0.55:
        coeff = ctx.sample_number(exclude_zero=True).value
        if coeff.denominator == 1 and abs(coeff) == 1 and ctx.rng.random() < 0.4:
            coeff = Fraction(ctx.rng.randint(2, 5) * ctx.rng.choice([1, -1]))
        latex = coeff_times_var(coeff, var.latex)
        text = coeff_times_var(coeff, var.name)
        style = _style(ctx)
        if style.clutter_amount > 0:
            cluttered = maybe_clutter(DisplayPiece(latex, text), style, ctx.rng)
            latex, text = cluttered.latex, cluttered.text
        return _Node(
            a=coeff,
            b=Fraction(0),
            latex=latex,
            text=text,
            shape_bits=["var"],
        )
    const = ctx.sample_number(exclude_zero=True).value
    return _Node(
        a=Fraction(0),
        b=const,
        latex=num_latex(const),
        text=num_latex(const),
        shape_bits=["const"],
    )


def _choose_combine_op(
    ctx: PrimitiveContext,
    pool: tuple[str, ...],
    left: _Node,
    right: _Node,
    *,
    mode: ExprMode,
) -> str:
    # Prefer +/−; use × when unlocked and both sides are “simple” enough, or randomly.
    add_ops = [o for o in pool if o in {"+", "-"}]
    mul_ops = [o for o in pool if o == "*"]
    # Never multiply two variable-bearing nodes under linear policy.
    if mode == "algebraic" and left.a != 0 and right.a != 0:
        mul_ops = []
    # Avoid × that would create var×var; const×expr handled by scale.
    choices = list(add_ops) if add_ops else ["+"]
    if mul_ops and (left.a == 0 or right.a == 0) and ctx.rng.random() < 0.35:
        choices.append("*")
    return ctx.rng.choice(choices)


def _combine(
    ctx: PrimitiveContext,
    left: _Node,
    right: _Node,
    op: str,
    *,
    mode: ExprMode,
    var: SampledVariable | None,
) -> _Node:
    style = _style(ctx)
    if op == "*":
        return _combine_mul(ctx, left, right, mode=mode, var=var)
    if op == "+":
        a, b = left.a + right.a, left.b + right.b
        l_piece = DisplayPiece(left.latex, left.text)
        r_l, r_t, extra_p, extra_d = right.latex, right.text, 0, 0
        if _needs_group_as_addend(right):
            r_l, r_t = f"\\left({right.latex}\\right)", f"({right.text})"
            extra_p, extra_d = 1, 1
        # Bare negative const → subtraction spelling (unless commuting addends).
        if (
            not style.commute_add
            and right.a == 0
            and right.b < 0
            and right.n_ops == 0
            and not right.is_wrapped
            and not right.used_mul
        ):
            latex = f"{left.latex} - {num_latex(abs(right.b))}"
            text = f"{left.text} - {num_latex(abs(right.b))}"
        else:
            r_piece = DisplayPiece(r_l, r_t)
            latex, text = render_addition(l_piece, r_piece, style, ctx.rng)
        return _Node(
            a=a,
            b=b,
            latex=latex,
            text=text,
            n_leaves=left.n_leaves + right.n_leaves,
            n_parens=left.n_parens + right.n_parens + extra_p,
            n_ops=left.n_ops + right.n_ops + 1,
            nest_depth=max(left.nest_depth, right.nest_depth + extra_d),
            used_mul=left.used_mul or right.used_mul,
            used_div=left.used_div or right.used_div,
            used_exp=left.used_exp or right.used_exp,
            ops=left.ops + right.ops + ["+"],
            shape_bits=left.shape_bits + right.shape_bits + ["+"],
        )

    # Subtraction — optional value-preserving flip: a-b → -(b-a)
    a, b = left.a - right.a, left.b - right.b
    r_l, r_t, extra_p, extra_d = right.latex, right.text, 0, 0
    if _needs_group_as_addend(right) or right.text.startswith("-") or right.latex.startswith("-"):
        if not right.is_wrapped:
            r_l, r_t = f"\\left({right.latex}\\right)", f"({right.text})"
            extra_p, extra_d = 1, 1
    l_piece = DisplayPiece(left.latex, left.text)
    r_piece = DisplayPiece(r_l, r_t)
    latex, text = render_subtraction(l_piece, r_piece, style, ctx.rng)
    if style.flip_subtraction:
        extra_p += 1
        extra_d += 1
    return _Node(
        a=a,
        b=b,
        latex=latex,
        text=text,
        n_leaves=left.n_leaves + right.n_leaves,
        n_parens=left.n_parens + right.n_parens + extra_p,
        n_ops=left.n_ops + right.n_ops + 1,
        nest_depth=max(left.nest_depth, right.nest_depth + extra_d),
        used_mul=left.used_mul or right.used_mul,
        used_div=left.used_div or right.used_div,
        used_exp=left.used_exp or right.used_exp,
        ops=left.ops + right.ops + ["-"],
        shape_bits=left.shape_bits + right.shape_bits + ["-"],
    )


def _combine_mul(
    ctx: PrimitiveContext,
    left: _Node,
    right: _Node,
    *,
    mode: ExprMode,
    var: SampledVariable | None,
) -> _Node:
    # Linear: at most one side may carry the variable.
    if mode == "algebraic" and left.a != 0 and right.a != 0:
        raise ValueError("var×var forbidden")
    # Prefer constant × expression display.
    if left.a == 0 and left.n_ops == 0 and not left.is_wrapped:
        return _wrap_scale(left.b, right, extra_leaves=left.n_leaves, mode=mode, ctx=ctx)
    if right.a == 0 and right.n_ops == 0 and not right.is_wrapped:
        return _wrap_scale(right.b, left, extra_leaves=right.n_leaves, mode=mode, ctx=ctx)
    # Numeric: both constants / subtrees — use × and evaluate.
    if mode == "numeric":
        style = _style(ctx)
        l_l, l_t = left.latex, left.text
        r_l, r_t = right.latex, right.text
        if left.n_ops > 0 and not left.is_wrapped:
            l_l, l_t = f"\\left({left.latex}\\right)", f"({left.text})"
        if right.n_ops > 0 and not right.is_wrapped:
            r_l, r_t = f"\\left({right.latex}\\right)", f"({right.text})"
        left_p = DisplayPiece(l_l, l_t)
        right_p = DisplayPiece(r_l, r_t)
        if style.strange_mode or style.explicit_multiply or style.clutter_amount > 0:
            latex, text = render_product([left_p, right_p], style, ctx.rng)
        elif style.commute_mul:
            latex = f"{right_p.latex} \\times {left_p.latex}"
            text = f"{right_p.text} * {left_p.text}"
        else:
            latex = f"{left_p.latex} \\times {right_p.latex}"
            text = f"{left_p.text} * {right_p.text}"
        return _Node(
            a=Fraction(0),
            b=left.b * right.b,
            latex=latex,
            text=text,
            n_leaves=left.n_leaves + right.n_leaves,
            n_parens=left.n_parens + right.n_parens,
            n_ops=left.n_ops + right.n_ops + 1,
            nest_depth=max(left.nest_depth, right.nest_depth),
            used_mul=True,
            used_exp=left.used_exp or right.used_exp,
            ops=left.ops + right.ops + ["*"],
            shape_bits=left.shape_bits + right.shape_bits + ["*"],
        )
    raise ValueError("cannot multiply algebraic subtrees")


def _needs_group_as_addend(node: _Node) -> bool:
    if node.is_wrapped or node.used_div:
        return False
    # Constant×(…) / distribute products are already grouped for +/−.
    if node.used_mul:
        return False
    return node.n_ops > 0


def _wrap(node: _Node) -> _Node:
    if node.is_wrapped:
        return node
    return _Node(
        a=node.a,
        b=node.b,
        latex=f"\\left({node.latex}\\right)",
        text=f"({node.text})",
        n_leaves=node.n_leaves,
        n_parens=node.n_parens + 1,
        n_ops=node.n_ops,
        nest_depth=node.nest_depth + 1,
        used_mul=node.used_mul,
        used_div=node.used_div,
        used_exp=node.used_exp,
        is_wrapped=True,
        ops=list(node.ops),
        shape_bits=node.shape_bits + ["paren"],
    )


def _strip_outer(node: _Node) -> _Node:
    if not node.is_wrapped:
        return node
    latex = node.latex
    text = node.text
    if latex.startswith("\\left(") and latex.endswith("\\right)"):
        latex = latex[len("\\left(") : -len("\\right)")]
    if text.startswith("(") and text.endswith(")"):
        text = text[1:-1]
    return _Node(
        a=node.a,
        b=node.b,
        latex=latex,
        text=text,
        n_leaves=node.n_leaves,
        n_parens=max(0, node.n_parens - 1),
        n_ops=node.n_ops,
        nest_depth=max(0, node.nest_depth - 1),
        used_mul=node.used_mul,
        used_div=node.used_div,
        used_exp=node.used_exp,
        is_wrapped=False,
        ops=list(node.ops),
        shape_bits=node.shape_bits,
    )


def _maybe_scale_node(
    ctx: PrimitiveContext,
    node: _Node,
    *,
    mode: ExprMode,
    var: SampledVariable | None,
    nest: int,
    scale: int,
    pool: tuple[str, ...],
) -> _Node:
    out = node
    while scale > 0 and ("*" in pool or "/" in pool):
        if nest > 0 and not out.is_wrapped and out.n_ops > 0 and ctx.rng.random() < 0.6:
            out = _wrap(out)
            nest -= 1
        op = "*" if "*" in pool and ( "/" not in pool or ctx.rng.random() < 0.7) else (
            "/" if "/" in pool and mode == "algebraic" else "*"
        )
        if op not in pool:
            break
        out = _scale_const(ctx, out, mode=mode, var=var, op=op)
        scale -= 1
        if ctx.rng.random() < 0.45:
            break
    if nest > 0 and out.n_ops > 0 and not out.is_wrapped and ctx.rng.random() < 0.3:
        out = _wrap(out)
    return out


def _scale_const(
    ctx: PrimitiveContext,
    node: _Node,
    *,
    mode: ExprMode,
    var: SampledVariable | None,
    op: str,
) -> _Node:
    c = _small_const(ctx, exclude_zero=True, prefer_abs_ge_2=True)
    if op == "*":
        return _wrap_scale(c, node, mode=mode, ctx=ctx)
    # Division (algebraic) — optional value-preserving flip: n/d → 1/(d/n)
    style = _style(ctx)
    numer = DisplayPiece(node.latex, node.text)
    denom = DisplayPiece(num_latex(c), num_latex(c))
    latex, text = render_division(numer, denom, style, ctx.rng)
    if not style.flip_division:
        # Prefer paren text for compound numerators (schoolbook).
        text = (
            f"({node.text})/{num_latex(c)}"
            if node.n_ops > 0 and not node.is_wrapped
            else f"{node.text}/{num_latex(c)}"
        )
    return _Node(
        a=node.a / c,
        b=node.b / c,
        latex=latex,
        text=text,
        n_leaves=node.n_leaves,
        n_parens=node.n_parens,
        n_ops=node.n_ops + 1,
        nest_depth=node.nest_depth,
        used_mul=node.used_mul,
        used_div=True,
        used_exp=node.used_exp,
        ops=node.ops + ["/"],
        shape_bits=node.shape_bits + ["/"],
    )


def _apply_square(ctx: PrimitiveContext, node: _Node) -> _Node:
    """Numeric leaf squared (small bases only)."""
    if node.a != 0 or node.n_ops > 0:
        return node
    if abs(node.b) > 6 or node.b.denominator != 1:
        v = Fraction(ctx.rng.randint(2, 5))
        node = _Node(a=Fraction(0), b=v, latex=str(int(v)), text=str(int(v)))
    base_l = node.latex
    base_t = node.text
    # Parenthesize negative bases only.
    if node.b < 0:
        base_l = f"\\left({base_l}\\right)"
        base_t = f"({base_t})"
    return _Node(
        a=Fraction(0),
        b=node.b * node.b,
        latex=f"{{{base_l}}}^{{2}}",
        text=f"{base_t}^2",
        n_leaves=1,
        n_ops=1,
        used_exp=True,
        ops=["^"],
        shape_bits=node.shape_bits + ["^2"],
    )


def _small_const(
    ctx: PrimitiveContext,
    *,
    exclude_zero: bool = True,
    prefer_abs_ge_2: bool = False,
) -> Fraction:
    for _ in range(10):
        v = ctx.sample_number(exclude_zero=exclude_zero).value
        if exclude_zero and v == 0:
            continue
        if prefer_abs_ge_2 and abs(v) == 1:
            if ctx.rng.random() < 0.55:
                v = Fraction(ctx.rng.choice([2, 3, 4, 5]) * (1 if v > 0 else -1))
        if v.denominator == 1 and abs(v) <= 12:
            return v
    return Fraction(ctx.rng.randint(2 if prefer_abs_ge_2 else 1, 6) * ctx.rng.choice([1, -1]))


def _render_affine(a: Fraction, b: Fraction, var: SampledVariable) -> tuple[str, str]:
    if a == 0:
        return num_latex(b), num_latex(b)
    if b == 0:
        return coeff_times_var(a, var.latex), coeff_times_var(a, var.name)
    left_l = coeff_times_var(a, var.latex)
    left_t = coeff_times_var(a, var.name)
    if b >= 0:
        return f"{left_l} + {num_latex(b)}", f"{left_t} + {num_latex(b)}"
    return f"{left_l} - {num_latex(abs(b))}", f"{left_t} - {num_latex(abs(b))}"


def _finish(
    node: _Node,
    *,
    mode: ExprMode,
    var: SampledVariable | None,
    eff: float,
) -> StructuredExpression:
    value = node.b if mode == "numeric" else node.b
    simp_l, simp_t = "", ""
    if mode == "algebraic" and var is not None:
        simp_l, simp_t = join_signed_terms([(node.a, var.latex), (node.b, "")])
    elif mode == "numeric":
        simp_l, simp_t = num_latex(node.b), num_latex(node.b)
        value = node.b

    n_groups = 0
    n_lone = 0
    for bit in node.shape_bits:
        if bit.startswith("distribute_groups:"):
            try:
                n_groups = int(bit.split(":", 1)[1])
            except ValueError:
                pass
        if bit.startswith("lone:"):
            try:
                n_lone = int(bit.split(":", 1)[1])
            except ValueError:
                pass
    if n_groups <= 0:
        n_groups = max(1, node.n_leaves)

    shape_id = "|".join(node.shape_bits) if node.shape_bits else "flat"
    tags = [
        f"leaves:{node.n_leaves}",
        f"ops:{node.n_ops}",
        f"nest:{node.nest_depth}",
        f"shape:{shape_id[:48]}",
    ]
    if node.used_mul:
        tags.append("mul")
    if node.used_div:
        tags.append("div")
    if node.used_exp:
        tags.append("exp")

    return StructuredExpression(
        latex=node.latex,
        text=node.text,
        value=value,
        coeff_a=node.a,
        coeff_b=node.b,
        var_name=var.name if var else None,
        var_latex=var.latex if var else None,
        n_leaves=node.n_leaves,
        n_parens=node.n_parens,
        nest_depth=node.nest_depth,
        n_ops=node.n_ops,
        ops_used=tuple(node.ops),
        shape_id=shape_id,
        upgrades=tuple(tags),
        effective_d=eff,
        mode=mode,
        simplified_latex=simp_l,
        simplified_text=simp_t,
        n_groups=n_groups,
        n_lone=n_lone,
    )


def _fallback(
    ctx: PrimitiveContext,
    *,
    mode: ExprMode,
    var: SampledVariable | None,
    eff: float,
    force_var: bool,
) -> StructuredExpression:
    if mode == "numeric":
        a = ctx.sample_number(exclude_zero=True)
        b = ctx.sample_number(exclude_zero=True)
        op = ctx.rng.choice(["+", "-", "*"])
        if op == "+":
            val = a.value + b.value
            latex = f"{a.latex} + {b.latex}"
            text = latex
        elif op == "-":
            val = a.value - b.value
            latex = f"{a.latex} - {b.latex}"
            text = latex
        else:
            val = a.value * b.value
            latex = f"{a.latex} \\times {b.latex}"
            text = f"{a.latex} * {b.latex}"
        return StructuredExpression(
            latex=latex,
            text=text,
            value=val,
            coeff_a=Fraction(0),
            coeff_b=val,
            var_name=None,
            var_latex=None,
            n_leaves=2,
            n_parens=0,
            nest_depth=0,
            n_ops=1,
            ops_used=(op,),
            shape_id="fallback",
            upgrades=("fallback",),
            effective_d=eff,
            mode="numeric",
            simplified_latex=num_latex(val),
            simplified_text=num_latex(val),
        )
    var = var or ctx.sample_variable()
    k, b, c = Fraction(2), Fraction(3), Fraction(1)
    latex = f"{num_latex(k)}\\left({var.latex} + {num_latex(b)}\\right) + {num_latex(c)}"
    text = f"{num_latex(k)}({var.name} + {num_latex(b)}) + {num_latex(c)}"
    a_tot, b_tot = k, k * b + c
    simp_l, simp_t = join_signed_terms([(a_tot, var.latex), (b_tot, "")])
    return StructuredExpression(
        latex=latex,
        text=text,
        value=b_tot,
        coeff_a=a_tot,
        coeff_b=b_tot,
        var_name=var.name,
        var_latex=var.latex,
        n_leaves=2,
        n_parens=1,
        nest_depth=1,
        n_ops=2,
        ops_used=("*", "+"),
        shape_id="fallback",
        upgrades=("fallback",),
        effective_d=eff,
        mode="algebraic",
        simplified_latex=simp_l,
        simplified_text=simp_t,
    )
