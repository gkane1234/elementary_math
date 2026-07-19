"""Order-of-operations — flat sum-of-products (answer-first, minimal parentheses).

Classroom OOO practice needs *precedence ambiguity*: ``2 + 3 \\times 4``, not
``(2 + 3) \\times 4`` or a bare numeral. This builder seeds a numeric target,
then builds a left-to-right sum/difference of addends where many addends are
products or quotients — so ``\\times``/``\\div`` bind tighter than ``+``/``-``
and parentheses are rare (only for intentional ``(a \\pm b) \\times c``).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from question_engine.frameworks.primitives._algebra_render import (
    num_latex,
    sample_integerish,
)
from question_engine.frameworks.primitives.constructive import NumericTarget, seed_numeric_target
from question_engine.frameworks.primitives.registry import PRIM_OOO, PrimitiveContext

OOO_SETTINGS_SCHEMA: dict[str, Any] = {
    "max_depth": {
        "type": "int",
        "default": None,
        "description": "Optional soft cap on intentional grouping parentheses (0 = none).",
    },
}


@dataclass(frozen=True)
class OooExpression:
    latex: str
    text: str
    value: Fraction
    upgrades: tuple[str, ...]
    effective_d: float
    shape_id: str = ""
    n_ops: int = 0
    nest_depth: int = 0


def _fget(key: str, default: float) -> float:
    from question_engine.frameworks.primitives.difficulty_knobs import fget

    return fget("ooo", key, default)


def _iget(key: str, default: int) -> int:
    from question_engine.frameworks.primitives.difficulty_knobs import iget

    return iget("ooo", key, default)


def target_n_addends(d: float) -> int:
    """Number of ± addends: ``base + floor(D / addend_scale)``, uncapped."""
    d = max(0.0, float(d))
    base = _iget("base_addends", 2)
    scale = max(1e-9, _fget("addend_scale", 3.0))
    return base + int(math.floor(d / scale))


def _small_factor(ctx: PrimitiveContext) -> Fraction:
    """Positive integer factor in ``[2, 9]`` (avoids boring ``× 1``)."""
    for _ in range(12):
        v = sample_integerish(ctx, exclude_zero=True).value
        if v.denominator == 1 and 2 <= abs(int(v)) <= 9:
            return Fraction(abs(int(v)))
    return Fraction(ctx.rng.choice([2, 3, 4, 5, 6]))


def _make_product(ctx: PrimitiveContext) -> tuple[Fraction, str, str, str]:
    a = _small_factor(ctx)
    b = _small_factor(ctx)
    val = a * b
    latex = f"{num_latex(a)} \\times {num_latex(b)}"
    text = f"{num_latex(a)}*{num_latex(b)}"
    return val, latex, text, "product"


def _make_quotient(ctx: PrimitiveContext) -> tuple[Fraction, str, str, str] | None:
    b = Fraction(ctx.rng.choice([2, 3, 4, 5, 6]))
    # Positive dividend multiple of divisor → clean integer quotient.
    q = _small_factor(ctx)
    a = b * q
    val = a / b
    latex = f"{num_latex(a)} \\div {num_latex(b)}"
    text = f"{num_latex(a)}/{num_latex(b)}"
    return val, latex, text, "quotient"


def _make_grouped_product(ctx: PrimitiveContext) -> tuple[Fraction, str, str, str]:
    """Intentional parentheses: ``(a ± b) × c`` — rare; creates a real grouping need."""
    a = _small_factor(ctx)
    b = _small_factor(ctx)
    c = _small_factor(ctx)
    if ctx.rng.random() < 0.5:
        inner = a + b
        inner_l = f"{num_latex(a)} + {num_latex(b)}"
        inner_t = f"{num_latex(a)}+{num_latex(b)}"
        tag = "group_add"
    else:
        # Prefer a > b so the difference is positive (sign lives on the ± join).
        if a < b:
            a, b = b, a
        if a == b:
            a = a + 1
        inner = a - b
        inner_l = f"{num_latex(a)} - {num_latex(b)}"
        inner_t = f"{num_latex(a)}-{num_latex(b)}"
        tag = "group_sub"
    val = inner * c
    latex = f"\\left({inner_l}\\right) \\times {num_latex(c)}"
    text = f"({inner_t})*{num_latex(c)}"
    return val, latex, text, tag


def _make_plain(ctx: PrimitiveContext) -> tuple[Fraction, str, str, str]:
    for _ in range(12):
        v = sample_integerish(ctx, exclude_zero=True).value
        if v.denominator == 1 and 1 <= abs(v) <= 12:
            # Positive display; caller folds overall ± via join sign.
            v = Fraction(abs(int(v)))
            return v, num_latex(v), num_latex(v), "plain"
    v = Fraction(ctx.rng.randint(1, 9))
    return v, num_latex(v), num_latex(v), "plain"


def _make_addend(
    ctx: PrimitiveContext,
    *,
    d: float,
    force_product: bool = False,
    allow_group: bool = False,
) -> tuple[Fraction, str, str, str]:
    prod_chance = min(0.9, _fget("product_chance_base", 0.55) + float(d) / 50.0)
    div_chance = min(0.35, _fget("div_chance_base", 0.12) + float(d) / 80.0)
    group_chance = 0.0
    if allow_group:
        group_chance = min(
            0.25, _fget("group_paren_chance", 0.08) * (0.5 + float(d) / 24.0)
        )

    r = ctx.rng.random()
    if force_product or r < prod_chance:
        if allow_group and ctx.rng.random() < group_chance:
            return _make_grouped_product(ctx)
        if ctx.rng.random() < div_chance:
            q = _make_quotient(ctx)
            if q is not None:
                return q
        return _make_product(ctx)
    return _make_plain(ctx)


def _fold_leading_minus(
    sign: int, val: Fraction, latex: str, text: str
) -> tuple[int, Fraction, str, str]:
    """Move a leading ``-`` on the addend into ``sign`` so joins stay schoolbook."""
    if latex.startswith("-"):
        return -sign, -val, latex[1:], text[1:] if text.startswith("-") else text
    return sign, val, latex, text


def _join_signed(
    parts: list[tuple[int, str, str]],
) -> tuple[str, str]:
    """Join ``(sign, latex, text)`` with schoolbook +/−.

    ``latex``/``text`` should be the value of the addend *before* ``sign``.
    Contribution of each part is ``sign * value(latex)``. When ``latex`` still
    starts with ``-``, wrap so subtracting a negative-looking term is
    ``- (-…)`` (not the incorrect ``+ (-…)``).
    """
    if not parts:
        return "0", "0"
    sign0, l0, t0 = parts[0]
    if sign0 < 0:
        if l0.startswith("-"):
            latex, text = f"-\\left({l0}\\right)", f"-({t0})"
        else:
            latex, text = f"-{l0}", f"-{t0}"
    else:
        latex, text = l0, t0
    for sign, l, t in parts[1:]:
        if sign >= 0:
            if l.startswith("-"):
                latex = f"{latex} + \\left({l}\\right)"
                text = f"{text} + ({t})"
            else:
                latex = f"{latex} + {l}"
                text = f"{text} + {t}"
        else:
            if l.startswith("-"):
                # Subtracting a negative-looking addend: -(-expr) == -val
                latex = f"{latex} - \\left({l}\\right)"
                text = f"{text} - ({t})"
            else:
                latex = f"{latex} - {l}"
                text = f"{text} - {t}"
    return latex, text


def _absorb_product(last: Fraction, rng) -> tuple[int, Fraction, str, str, str] | None:
    """Try to write ``last`` as ``± (a × b)`` with positive factors."""
    if last == 0 or abs(last) > 81:
        return None
    if rng.random() >= 0.55:
        return None
    mag = abs(last)
    sign = 1 if last > 0 else -1
    for a_int in (2, 3, 4, 5, 6):
        a = Fraction(a_int)
        if mag % a != 0:
            continue
        b = mag / a  # exact Fraction division
        if b.denominator != 1:
            continue
        if 2 <= abs(b) <= 12:
            latex = f"{num_latex(a)} \\times {num_latex(b)}"
            text = f"{num_latex(a)}*{num_latex(b)}"
            return sign, mag, latex, text, "product_absorb"
    return None


def build_flat_ooo(
    ctx: PrimitiveContext,
    *,
    d: float,
    target: NumericTarget | None = None,
) -> OooExpression:
    """Answer-first flat OOO expression that evaluates to ``target``."""
    tgt = target or seed_numeric_target(ctx)
    # Avoid a boring zero-only worksheet at low D when seed is 0 often.
    if tgt.value == 0 and d < 4 and ctx.rng.random() < 0.7:
        tgt = NumericTarget(value=Fraction(ctx.rng.choice([2, 3, 4, 5, 6, 8, 9, 12])))

    n = max(2, target_n_addends(d))
    max_add = _iget("max_addends", 24)
    n = min(n, max_add)

    # At least one product so there is a precedence decision.
    force_prod_slots = {0} if n == 2 else {ctx.rng.randrange(n - 1)}
    if n >= 3 and ctx.rng.random() < 0.7:
        force_prod_slots.add(ctx.rng.randrange(n - 1))

    allow_group = d >= _fget("group_paren_min_d", 8.0)
    settings = ctx.settings_for(PRIM_OOO)
    max_depth = settings.get("max_depth")
    if max_depth is not None:
        try:
            if int(max_depth) <= 0:
                allow_group = False
        except (TypeError, ValueError):
            pass

    parts_val: list[tuple[int, Fraction, str, str, str]] = []
    running = Fraction(0)
    tags: list[str] = ["flat_ooo"]

    for i in range(n - 1):
        sign = 1 if i == 0 else ctx.rng.choice([1, -1])
        val, latex, text, kind = _make_addend(
            ctx,
            d=d,
            force_product=(i in force_prod_slots),
            allow_group=allow_group,
        )
        sign, val, latex, text = _fold_leading_minus(sign, val, latex, text)
        parts_val.append((sign, val, latex, text, kind))
        running += sign * val
        tags.append(kind)

    # Last addend absorbs so the expression equals the target.
    # Skip a trailing "+ 0" when earlier addends already hit the target.
    last = tgt.value - running
    if last != 0 or len(parts_val) < 2:
        absorbed = _absorb_product(last, ctx.rng)
        if absorbed is not None:
            last_sign, last_val, last_latex, last_text, last_kind = absorbed
        else:
            last_sign = 1 if last >= 0 else -1
            last_val = abs(last)
            last_latex = num_latex(last_val)
            last_text = num_latex(last_val)
            last_kind = "absorb"
            if last == 0:
                last_sign = 1
                last_val = Fraction(0)
                last_latex = "0"
                last_text = "0"
        parts_val.append((last_sign, last_val, last_latex, last_text, last_kind))
        tags.append(last_kind)

    join_parts = [(s, l, t) for s, _v, l, t, _k in parts_val]
    latex, text = _join_signed(join_parts)

    # Count operators roughly: each ± between addends + each ×/÷ inside.
    n_ops = max(0, len(parts_val) - 1)
    for _s, _v, l, _t, _k in parts_val:
        n_ops += l.count("\\times") + l.count("\\div") + l.count("*")
    # Intentional grouping only — ignore join wraps around bare negatives.
    nest = 1 if any(k.startswith("group_") for k in tags) else 0

    return OooExpression(
        latex=latex,
        text=text,
        value=tgt.value,
        upgrades=tuple(tags),
        effective_d=d,
        shape_id="ooo:" + "+".join(tags[1:4]),
        n_ops=n_ops,
        nest_depth=nest,
    )


def sample_ooo_expression(ctx: PrimitiveContext) -> OooExpression:
    """Sample an OOO expression for the current topic difficulty."""
    # Prefer topic D so high worksheet difficulty really lengthens expressions
    # (not only the OOO budget slice after number-lane spend).
    eff = max(float(ctx.effective_d(PRIM_OOO)), float(ctx.topic_d) * 0.85)
    return build_flat_ooo(ctx, d=eff)
