"""Shared exponent policy for the expression generator.

Used by ``expression_structure`` (tree builder) and thin consumers such as
``ooo`` (flat sum-of-products). Debug knobs live under
``difficulty_knobs.json`` → ``expression_structure``.

Site model
----------
- **Number sites**: bare numerals / numeric factors — ``exp_type_number``,
  chance ``exp_chance_at_unlock`` → ``exp_chance_max``.
- **Paren sites**: parenthetical bases ``(a±b)^{e}`` — ``exp_type_paren``
  (independent; may later be ``rational`` for power-rule topics), chance
  defaults to ``number_chance * exp_chance_paren_factor`` when linked.

Defaults for stock numeric OOO / evaluate: both types ``positive_integer``,
tiny powers (prefer 2–3, rarely 4). Richer types are schema-legal on either
site; numeric evaluation currently implements ``positive_integer`` only.
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Any, Literal

from question_engine.frameworks.primitives._algebra_render import num_latex
from question_engine.frameworks.primitives.registry import PrimitiveContext

ExpSite = Literal["number", "paren"]

EXP_TYPE_POSITIVE_INTEGER = "positive_integer"
EXP_TYPES: tuple[str, ...] = (
    EXP_TYPE_POSITIVE_INTEGER,
    "integer",  # reserved (signed int) — algebraic / advanced numeric later
    "rational",  # reserved (e.g. 2/3) — power-rule / algebraic OOO later
)

EXPONENT_SETTINGS_SCHEMA: dict[str, Any] = {
    "exp_unlock_d": {
        "type": "float",
        "default": 10.0,
        "description": "Exponents allowed when D > this (default 10 → unlock at 11).",
    },
    "max_exponent": {
        "type": "int",
        "default": 3,
        "description": "Cap for positive_integer exponents (prefer 2–3; 4 rare).",
    },
    "exp_type_number": {
        "type": "enum",
        "default": EXP_TYPE_POSITIVE_INTEGER,
        "options": list(EXP_TYPES),
        "description": "Exponent value type at bare-number / factor sites.",
    },
    "exp_type_paren": {
        "type": "enum",
        "default": EXP_TYPE_POSITIVE_INTEGER,
        "options": list(EXP_TYPES),
        "description": (
            "Exponent value type at parenthetical sites (independent of "
            "exp_type_number). May be rational for (1+x)^{2/3} topics later."
        ),
    },
    "exp_chance_at_unlock": {
        "type": "float",
        "default": 0.05,
        "description": "Number-site chance just above unlock.",
    },
    "exp_chance_max": {
        "type": "float",
        "default": 0.2,
        "description": "Number-site chance as D → ∞.",
    },
    "exp_chance_scale": {
        "type": "float",
        "default": 0.2,
        "description": "Asymptotic rate for number (and unlinked paren) chance.",
    },
    "exp_chance_paren_factor": {
        "type": "float",
        "default": 0.45,
        "description": "When linked: paren_chance = number_chance * factor.",
    },
    "exp_paren_link_to_number": {
        "type": "bool",
        "default": True,
        "description": "If true, paren chance tracks number chance via factor.",
    },
    "exp_chance_paren_at_unlock": {
        "type": "float",
        "default": 0.0225,
        "description": "Paren-site chance just above unlock when unlinked.",
    },
    "exp_chance_paren_max": {
        "type": "float",
        "default": 0.09,
        "description": "Paren-site chance as D → ∞ when unlinked.",
    },
}

_KNOB_SECTION = "expression_structure"


def _fget(key: str, default: float) -> float:
    from question_engine.frameworks.primitives.difficulty_knobs import fget

    return fget(_KNOB_SECTION, key, default)


def _iget(key: str, default: int) -> int:
    from question_engine.frameworks.primitives.difficulty_knobs import iget

    return iget(_KNOB_SECTION, key, default)


def _bget(key: str, default: bool) -> bool:
    from question_engine.frameworks.primitives.difficulty_knobs import section

    return bool(section(_KNOB_SECTION).get(key, default))


def _sget(key: str, default: str) -> str:
    from question_engine.frameworks.primitives.difficulty_knobs import section

    val = section(_KNOB_SECTION).get(key, default)
    if val is None:
        return default
    return str(val)


def exponents_unlocked(d: float) -> bool:
    """True when ``D > exp_unlock_d`` (default 10 → unlock at D=11)."""
    return float(d) > _fget("exp_unlock_d", 10.0)


def exp_type_for_site(site: ExpSite) -> str:
    """Configured exponent type for a site (may be richer than numeric eval supports)."""
    key = "exp_type_number" if site == "number" else "exp_type_paren"
    raw = _sget(key, EXP_TYPE_POSITIVE_INTEGER).strip().lower()
    if raw not in EXP_TYPES:
        return EXP_TYPE_POSITIVE_INTEGER
    return raw


def numeric_exp_type(site: ExpSite) -> str:
    """Type used for Fraction-valued numeric evaluation today.

    Configured richer types remain legal in knobs/schema for algebraic reuse;
    numeric paths fall back to ``positive_integer`` until those evaluators exist.
    """
    configured = exp_type_for_site(site)
    if configured != EXP_TYPE_POSITIVE_INTEGER:
        return EXP_TYPE_POSITIVE_INTEGER
    return configured


def _asymptotic_chance(
    d: float, *, p0: float, pmax: float, scale: float, unlock: float
) -> float:
    if float(d) <= unlock:
        return 0.0
    p0 = max(0.0, min(1.0, p0))
    pmax = max(p0, min(1.0, pmax))
    k = max(0.0, scale)
    excess = float(d) - unlock
    return pmax - (pmax - p0) * math.exp(-k * excess)


def exp_number_chance(d: float, *, allow_exponents: bool = True) -> float:
    """Per-site chance to raise a bare number / numeric factor."""
    if not allow_exponents:
        return 0.0
    unlock = _fget("exp_unlock_d", 10.0)
    return _asymptotic_chance(
        d,
        p0=_fget("exp_chance_at_unlock", 0.05),
        pmax=_fget("exp_chance_max", 0.2),
        scale=_fget("exp_chance_scale", 0.2),
        unlock=unlock,
    )


def exp_paren_chance(d: float, *, allow_exponents: bool = True) -> float:
    """Per-site chance to raise a parenthetical ``(a±b)``."""
    if not allow_exponents:
        return 0.0
    unlock = _fget("exp_unlock_d", 10.0)
    if float(d) <= unlock:
        return 0.0
    factor = max(0.0, min(1.0, _fget("exp_chance_paren_factor", 0.45)))
    if _bget("exp_paren_link_to_number", True):
        return exp_number_chance(d, allow_exponents=True) * factor
    return _asymptotic_chance(
        d,
        p0=_fget("exp_chance_paren_at_unlock", 0.05 * 0.45),
        pmax=_fget("exp_chance_paren_max", 0.2 * 0.45),
        scale=_fget("exp_chance_scale", 0.2),
        unlock=unlock,
    )


def exp_site_chance(d: float, *, allow_exponents: bool = True) -> float:
    """Alias for number-site chance (backward compatible)."""
    return exp_number_chance(d, allow_exponents=allow_exponents)


def sample_positive_integer_exponent(ctx: PrimitiveContext) -> int:
    """Tiny positive integer: prefer 2–3, rarely 4 (capped by ``max_exponent``)."""
    max_exp = max(2, min(_iget("max_exponent", 3), 4))
    pool: list[tuple[int, float]] = []
    for exp, w in ((2, 0.55), (3, 0.35), (4, 0.10)):
        if exp <= max_exp:
            pool.append((exp, w))
    if not pool:
        return 2
    total = sum(w for _e, w in pool)
    r = ctx.rng.random() * total
    acc = 0.0
    for exp, w in pool:
        acc += w
        if r <= acc:
            return exp
    return pool[-1][0]


def sample_exponent_value(ctx: PrimitiveContext, *, site: ExpSite) -> int | None:
    """Sample an exponent for ``site`` under numeric evaluation rules."""
    if numeric_exp_type(site) == EXP_TYPE_POSITIVE_INTEGER:
        return sample_positive_integer_exponent(ctx)
    return None


def try_raise_number(
    ctx: PrimitiveContext,
    d: float,
    base: int,
    *,
    allow_exponents: bool,
    force: bool = False,
) -> tuple[Fraction, str, str, bool]:
    """Independently roll raising a positive integer base (number site).

    ``force=True`` skips the chance roll (still needs a valid base ≥ 2).
    """
    if force:
        p = 1.0 if allow_exponents else 0.0
    else:
        p = exp_number_chance(d, allow_exponents=allow_exponents)
    if p <= 0.0 or (not force and ctx.rng.random() >= p):
        v = Fraction(base)
        s = num_latex(v)
        return v, s, s, False
    work_base = base if base >= 2 else ctx.rng.randint(2, 5)
    for _ in range(12):
        exp = sample_exponent_value(ctx, site="number")
        if exp is None:
            break
        if work_base**exp > 256:
            continue
        val = Fraction(work_base**exp)
        return val, f"{work_base}^{{{exp}}}", f"{work_base}**{exp}", True
    if force:
        # Guaranteed tiny power when the topic requires an exponent.
        exp = 2
        work_base = min(work_base, 9)
        val = Fraction(work_base**exp)
        return val, f"{work_base}^{{{exp}}}", f"{work_base}**{exp}", True
    v = Fraction(base)
    s = num_latex(v)
    return v, s, s, False


def try_raise_paren(
    ctx: PrimitiveContext,
    d: float,
    inner: Fraction,
    inner_l: str,
    inner_t: str,
    *,
    allow_exponents: bool,
) -> tuple[Fraction, str, str, bool]:
    """Independently roll ``(inner)^{e}`` (paren site; type independently configurable)."""
    p = exp_paren_chance(d, allow_exponents=allow_exponents)
    wrapped_l = f"\\left({inner_l}\\right)"
    wrapped_t = f"({inner_t})"
    if p <= 0.0 or ctx.rng.random() >= p:
        return inner, wrapped_l, wrapped_t, False
    if inner.denominator != 1:
        return inner, wrapped_l, wrapped_t, False
    base = abs(int(inner))
    if base < 2 or base > 9:
        return inner, wrapped_l, wrapped_t, False
    for _ in range(10):
        exp = sample_exponent_value(ctx, site="paren")
        if exp is None:
            break
        if base**exp > 256:
            continue
        val = Fraction(base**exp)
        return val, f"{wrapped_l}^{{{exp}}}", f"{wrapped_t}**{exp}", True
    return inner, wrapped_l, wrapped_t, False


__all__ = [
    "EXP_TYPES",
    "EXP_TYPE_POSITIVE_INTEGER",
    "EXPONENT_SETTINGS_SCHEMA",
    "exp_number_chance",
    "exp_paren_chance",
    "exp_site_chance",
    "exp_type_for_site",
    "exponents_unlocked",
    "numeric_exp_type",
    "sample_exponent_value",
    "sample_positive_integer_exponent",
    "try_raise_number",
    "try_raise_paren",
]
