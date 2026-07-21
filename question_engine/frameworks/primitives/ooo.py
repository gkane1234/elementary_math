"""Order-of-operations — flat sum-of-products (thin expression-generator consumer).

Classroom OOO needs *precedence ambiguity*: ``2 + 3 \\times 4``. This builder
seeds a numeric target, then builds a left-to-right sum/difference of addends
(many products/quotients). Exponent policy (unlock, site chances, types,
``(a±b)^{e}``) lives in ``expression_exponents`` / ``expression_structure``
knobs — OOO only passes ``allow_exponents`` and difficulty into that API.
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
from question_engine.frameworks.primitives.expression_exponents import (
    EXPONENT_SETTINGS_SCHEMA,
    exp_number_chance,
    exponents_unlocked,
    sample_exponent_value,
    try_raise_number,
    try_raise_paren,
)
from question_engine.frameworks.primitives.registry import PRIM_OOO, PrimitiveContext

OOO_SETTINGS_SCHEMA: dict[str, Any] = {
    "max_depth": {
        "type": "int",
        "default": None,
        "description": "Optional soft cap on intentional grouping parentheses (0 = none).",
    },
    # Exponent knobs are owned by the shared expression generator; surface here
    # so catalog/settings UIs that read OOO schema still see the same keys.
    **EXPONENT_SETTINGS_SCHEMA,
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


def _small_factor_int(ctx: PrimitiveContext) -> int:
    """Positive integer factor in ``[2, 9]`` (avoids boring ``× 1``)."""
    for _ in range(12):
        v = sample_integerish(ctx, exclude_zero=True).value
        if v.denominator == 1 and 2 <= abs(int(v)) <= 9:
            return abs(int(v))
    return int(ctx.rng.choice([2, 3, 4, 5, 6]))


def _make_product(
    ctx: PrimitiveContext,
    *,
    chance_d: float,
    allow_exponents: bool,
    force_exponent: bool = False,
) -> tuple[Fraction, str, str, str]:
    a0 = _small_factor_int(ctx)
    b0 = _small_factor_int(ctx)
    a, a_l, a_t, a_pow = try_raise_number(
        ctx,
        chance_d,
        a0,
        allow_exponents=allow_exponents,
        force=force_exponent,
    )
    b, b_l, b_t, b_pow = try_raise_number(
        ctx, chance_d, b0, allow_exponents=allow_exponents
    )
    val = a * b
    latex = f"{a_l} \\times {b_l}"
    text = f"{a_t}*{b_t}"
    if a_pow and b_pow:
        tag = "product_power_both"
    elif a_pow or b_pow:
        tag = "product_power"
    else:
        tag = "product"
    return val, latex, text, tag


def _make_quotient(
    ctx: PrimitiveContext,
    *,
    chance_d: float,
    allow_exponents: bool,
    force_exponent: bool = False,
) -> tuple[Fraction, str, str, str] | None:
    b = int(ctx.rng.choice([2, 3, 4, 5, 6]))
    q = _small_factor_int(ctx)
    a0 = b * q
    if force_exponent:
        p = 1.0
    else:
        p = exp_number_chance(chance_d, allow_exponents=allow_exponents)
    if p > 0.0 and (force_exponent or ctx.rng.random() < p):
        for _ in range(10):
            exp = sample_exponent_value(ctx, site="number")
            if exp is None or a0 < 2 or a0**exp > 256:
                continue
            pow_val = Fraction(a0**exp)
            if pow_val % b != 0:
                continue
            val = pow_val / b
            if val.denominator != 1:
                continue
            latex = f"{a0}^{{{exp}}} \\div {num_latex(Fraction(b))}"
            text = f"{a0}**{exp}/{num_latex(Fraction(b))}"
            return val, latex, text, "power_quotient"
        if force_exponent:
            # Fall through to a forced plain power addend instead of bare quotient.
            return None
    val = Fraction(a0) / b
    latex = f"{num_latex(Fraction(a0))} \\div {num_latex(Fraction(b))}"
    text = f"{num_latex(Fraction(a0))}/{num_latex(Fraction(b))}"
    return val, latex, text, "quotient"


def _sample_group_inner(ctx: PrimitiveContext) -> tuple[Fraction, str, str, str]:
    a = Fraction(_small_factor_int(ctx))
    b = Fraction(_small_factor_int(ctx))
    if ctx.rng.random() < 0.5:
        inner = a + b
        inner_l = f"{num_latex(a)} + {num_latex(b)}"
        inner_t = f"{num_latex(a)}+{num_latex(b)}"
        tag = "add"
    else:
        if a < b:
            a, b = b, a
        if a == b:
            a = a + 1
        inner = a - b
        inner_l = f"{num_latex(a)} - {num_latex(b)}"
        inner_t = f"{num_latex(a)}-{num_latex(b)}"
        tag = "sub"
    return inner, inner_l, inner_t, tag


def _make_grouped(
    ctx: PrimitiveContext,
    *,
    chance_d: float,
    allow_exponents: bool,
) -> tuple[Fraction, str, str, str]:
    inner, inner_l, inner_t, tag = _sample_group_inner(ctx)
    g_val, g_l, g_t, powered = try_raise_paren(
        ctx, chance_d, inner, inner_l, inner_t, allow_exponents=allow_exponents
    )
    if powered:
        return g_val, g_l, g_t, f"group_power_{tag}"

    c0 = _small_factor_int(ctx)
    c, c_l, c_t, c_pow = try_raise_number(
        ctx, chance_d, c0, allow_exponents=allow_exponents
    )
    val = inner * c
    latex = f"\\left({inner_l}\\right) \\times {c_l}"
    text = f"({inner_t})*{c_t}"
    kind = f"group_{tag}_power" if c_pow else f"group_{tag}"
    return val, latex, text, kind


def _make_plain(
    ctx: PrimitiveContext,
    *,
    chance_d: float,
    allow_exponents: bool,
    force_exponent: bool = False,
) -> tuple[Fraction, str, str, str]:
    for _ in range(12):
        v = sample_integerish(ctx, exclude_zero=True).value
        if v.denominator == 1 and 1 <= abs(v) <= 12:
            base = abs(int(v))
            val, latex, text, powered = try_raise_number(
                ctx,
                chance_d,
                base,
                allow_exponents=allow_exponents,
                force=force_exponent,
            )
            return val, latex, text, "power" if powered else "plain"
    base = ctx.rng.randint(1, 9)
    val, latex, text, powered = try_raise_number(
        ctx,
        chance_d,
        base,
        allow_exponents=allow_exponents,
        force=force_exponent,
    )
    return val, latex, text, "power" if powered else "plain"


def _make_addend(
    ctx: PrimitiveContext,
    *,
    d: float,
    chance_d: float,
    force_product: bool = False,
    allow_group: bool = False,
    allow_exponents: bool = False,
    force_exponent: bool = False,
) -> tuple[Fraction, str, str, str]:
    """Pick an addend; exponents roll at sites via the shared expression API."""
    if force_exponent:
        # Guaranteed power site — prefer a plain powered number (clearest for the topic).
        if ctx.rng.random() < 0.55:
            return _make_plain(
                ctx,
                chance_d=chance_d,
                allow_exponents=True,
                force_exponent=True,
            )
        return _make_product(
            ctx,
            chance_d=chance_d,
            allow_exponents=True,
            force_exponent=True,
        )

    prod_chance = min(0.9, _fget("product_chance_base", 0.55) + float(d) / 50.0)
    div_chance = min(0.35, _fget("div_chance_base", 0.12) + float(d) / 80.0)
    group_chance = 0.0
    if allow_group:
        group_chance = min(
            0.25, _fget("group_paren_chance", 0.08) * (0.5 + float(d) / 24.0)
        )

    want_compound = force_product or ctx.rng.random() < prod_chance

    if want_compound:
        if allow_group and ctx.rng.random() < group_chance:
            return _make_grouped(
                ctx, chance_d=chance_d, allow_exponents=allow_exponents
            )
        if ctx.rng.random() < div_chance:
            q = _make_quotient(
                ctx, chance_d=chance_d, allow_exponents=allow_exponents
            )
            if q is not None:
                return q
        return _make_product(
            ctx, chance_d=chance_d, allow_exponents=allow_exponents
        )

    return _make_plain(ctx, chance_d=chance_d, allow_exponents=allow_exponents)


def _fold_leading_minus(
    sign: int, val: Fraction, latex: str, text: str
) -> tuple[int, Fraction, str, str]:
    if latex.startswith("-"):
        return -sign, -val, latex[1:], text[1:] if text.startswith("-") else text
    return sign, val, latex, text


def _join_signed(parts: list[tuple[int, str, str]]) -> tuple[str, str]:
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
                latex = f"{latex} - \\left({l}\\right)"
                text = f"{text} - ({t})"
            else:
                latex = f"{latex} - {l}"
                text = f"{text} - {t}"
    return latex, text


def _absorb_product(last: Fraction, rng) -> tuple[int, Fraction, str, str, str] | None:
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
        b = mag / a
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
    allow_exponents: bool | None = None,
    exp_d: float | None = None,
    require_exponents: bool = False,
) -> OooExpression:
    """Answer-first flat OOO expression that evaluates to ``target``.

    ``allow_exponents`` defaults from shared ``exponents_unlocked(exp_d)``.
    ``require_exponents`` forces at least one ``a^{e}`` site (topic skill).
    """
    tgt = target or seed_numeric_target(ctx)
    if tgt.value == 0 and d < 4 and ctx.rng.random() < 0.7:
        tgt = NumericTarget(value=Fraction(ctx.rng.choice([2, 3, 4, 5, 6, 8, 9, 12])))

    n = max(2, target_n_addends(d))
    max_add = _iget("max_addends", 24)
    n = min(n, max_add)

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

    chance_d = float(d if exp_d is None else exp_d)
    use_exp = True if require_exponents else (
        exponents_unlocked(chance_d)
        if allow_exponents is None
        else bool(allow_exponents)
    )
    force_exp_slot = (
        ctx.rng.randrange(max(1, n - 1)) if require_exponents else None
    )

    parts_val: list[tuple[int, Fraction, str, str, str]] = []
    running = Fraction(0)
    tags: list[str] = ["flat_ooo"]

    for i in range(n - 1):
        sign = 1 if i == 0 else ctx.rng.choice([1, -1])
        val, latex, text, kind = _make_addend(
            ctx,
            d=d,
            chance_d=chance_d,
            force_product=(i in force_prod_slots),
            allow_group=allow_group,
            allow_exponents=use_exp,
            force_exponent=(force_exp_slot is not None and i == force_exp_slot),
        )
        sign, val, latex, text = _fold_leading_minus(sign, val, latex, text)
        parts_val.append((sign, val, latex, text, kind))
        running += sign * val
        tags.append(kind)

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

    n_ops = max(0, len(parts_val) - 1)
    for _s, _v, l, _t, _k in parts_val:
        n_ops += l.count("\\times") + l.count("\\div") + l.count("*")
        n_ops += l.count("^{")
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


def sample_ooo_expression(
    ctx: PrimitiveContext,
    *,
    require_exponents: bool | None = None,
) -> OooExpression:
    """Sample an OOO expression; exponent policy follows shared expression knobs.

    Topics that *are* exponents (e.g. numeric expressions with exponents) pass
    ``require_exponents=True`` so every stem contains at least one power.
    """
    topic = float(ctx.topic_d)
    eff = max(float(ctx.effective_d(PRIM_OOO)), topic * 0.85)
    settings = ctx.settings_for(PRIM_OOO)
    require = (
        bool(require_exponents)
        if require_exponents is not None
        else bool(settings.get("require_exponents", False))
    )
    leaf = getattr(ctx, "leaf_id", None) or ""
    if "with_exponents" in str(leaf):
        require = True
    allow_exp = True if require else exponents_unlocked(topic)
    return build_flat_ooo(
        ctx,
        d=eff,
        allow_exponents=allow_exp,
        exp_d=topic,
        require_exponents=require,
    )
