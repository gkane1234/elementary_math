"""Shared cancel-count unlocks and continuous structure growth for rationals.

Default / free (low D): exactly 1 cancel. Higher D unlocks 0, then 2, then 3,
then exact counts 4, 5, … growing unboundedly with D (same spirit as
``continuous_abs_max`` / ratio inflate). Explicit ``cancel_factor_count`` in
settings always wins. When fewer factors are available than requested, builders
clamp with ``min(requested, available)`` and still succeed.

UI select value ``\"4\"`` (and ``\"all\"``) means cancel every available factor
in a normal-sized problem (hard-capped). Integer ``4`` means exactly four cancels.
"""

from __future__ import annotations

import random
from typing import Any

from question_engine.frameworks.difficulty_budget import settings_difficulty
from question_engine.frameworks.primitives.difficulty_knobs import fget, section

# Defaults mirrored in difficulty_knobs.json → rational_cancel
_DEFAULT_COUNT = 1
_UNLOCK_0_D = 4.0
_UNLOCK_2_D = 6.0
_UNLOCK_3_D = 10.0
_UNLOCK_4_D = 14.0
_PREFER_DEFAULT_WEIGHT = 2.5

# UI / string "all" / "4" → cancel every available LCD factor (clamped later).
ALL_AVAILABLE_CANCEL = 10**9

# Classroom safety: "all available" cancels every factor *in the problem*, but
# the problem itself must stay bounded — never grow LCD/cancel count to the
# continuous D ceiling (which can hit 100+ and hang the UI).
ALL_AVAILABLE_FACTOR_CAP = 8

# Add-then-cancel (±): after combining over the LCD, the *expanded* combined
# numerator must be hand-factorable without RRT (deg ≤ 2: linear/quadratic /
# GCF / grouping / DOS). With a constant reduced core that means at most two
# linear cancel factors. Higher requests are clamped; prefer honest clamp over
# leaking construction factorizations into solution steps.
HAND_FACTORABLE_END_CANCEL_MAX = 2


def max_hand_factorable_end_cancel(
    *,
    rrt_exclude: bool = True,
    final_core_degree: int = 0,
) -> int:
    """Max end-of-addition cancel factors that keep combined num classroom-factorable.

    When RRT is allowed there is no pedagogical cap (return a huge sentinel).
    Otherwise ``combined_deg ≈ final_core_degree + cancel_count`` for linear
    cancels, and we require ``combined_deg ≤ 2``.
    """
    if not rrt_exclude:
        return ALL_AVAILABLE_CANCEL
    return max(0, HAND_FACTORABLE_END_CANCEL_MAX - max(0, int(final_core_degree)))


def clamp_end_cancel_hand_factorable(
    requested: int,
    *,
    rrt_exclude: bool = True,
    final_core_degree: int = 0,
) -> int:
    """Clamp a requested end-cancel count to the hand-factorable maximum."""
    cap = max_hand_factorable_end_cancel(
        rrt_exclude=rrt_exclude,
        final_core_degree=final_core_degree,
    )
    return max(0, min(int(requested), int(cap)))


def all_available_factor_cap(settings: dict[str, Any] | None = None) -> int:
    """Max factors when UI asks to cancel all available."""
    settings = settings or {}
    raw = settings.get("max_lcd_factors")
    try:
        if raw is not None:
            return max(1, min(int(raw), ALL_AVAILABLE_FACTOR_CAP))
    except (TypeError, ValueError):
        pass
    return ALL_AVAILABLE_FACTOR_CAP


def sample_all_available_factor_count(
    settings: dict[str, Any] | None = None,
    *,
    default: int = 3,
) -> int:
    """Pick a normal problem size, then cancel all of those factors.

    Uses continuous sampling when D is set, but hard-caps so \"all available\"
    never means \"grow to 100 and cancel all\".
    """
    settings = settings or {}
    cap = all_available_factor_cap(settings)
    sampled = sample_rational_lcd_factors(settings, default=default)
    # Prefer at least two factors so \"all cancel\" is pedagogically visible.
    return max(2, min(int(sampled), cap)) if cap >= 2 else max(1, min(int(sampled), cap))


def _unlock_thresholds() -> dict[int, float]:
    sec = section("rational_cancel")
    return {
        0: float(sec.get("unlock_0_d", _UNLOCK_0_D)),
        2: float(sec.get("unlock_2_d", _UNLOCK_2_D)),
        3: float(sec.get("unlock_3_d", _UNLOCK_3_D)),
        4: float(sec.get("unlock_4_d", _UNLOCK_4_D)),
    }


def default_cancel_count() -> int:
    try:
        return int(fget("rational_cancel", "default_count", float(_DEFAULT_COUNT)))
    except (TypeError, ValueError):
        return _DEFAULT_COUNT


def continuous_rational_cancel_max(d: float) -> int:
    """Max exact cancel count unlocked at difficulty ``d`` (unbounded).

    D≈0 → 1, D≈14 → ~4, D≈40 → ~11, D≈1000 → hundreds.
    Polynomial growth — no soft asymptote that flattens by D=20.
    """
    d = max(0.0, float(d))
    sec = section("rational_cancel")
    base = float(sec.get("cancel_max_base", 1.0))
    lin = float(sec.get("cancel_max_linear", 0.25))
    quad = float(sec.get("cancel_max_quad", 0.00009))
    return max(1, int(base + lin * d + quad * d * d))


def continuous_rational_lcd_factors_max(settings: dict[str, Any] | None) -> int | None:
    """Max distinct LCD factors from continuous ``difficulty``, else ``None``.

    D≈0 → 2, D≈10 → ~4, D≈40 → ~10, D≈1000 → ~100+.
    """
    settings = settings or {}
    if "difficulty" not in settings or settings["difficulty"] is None:
        return None
    d = max(0.0, settings_difficulty(settings, default=0.0))
    sec = section("rational_cancel")
    base = float(sec.get("lcd_max_base", 2.0))
    lin = float(sec.get("lcd_max_linear", 0.2))
    quad = float(sec.get("lcd_max_quad", 0.00008))
    return max(1, int(base + lin * d + quad * d * d))


def continuous_rational_term_count_max(settings: dict[str, Any] | None) -> int | None:
    """Max rational terms / ×÷ operands from continuous ``difficulty``, else ``None``.

    D≈0 → 2, D≈40 → ~8, D≈1000 → ~100+.
    """
    settings = settings or {}
    if "difficulty" not in settings or settings["difficulty"] is None:
        return None
    d = max(0.0, settings_difficulty(settings, default=0.0))
    sec = section("rational_cancel")
    base = float(sec.get("term_max_base", 2.0))
    lin = float(sec.get("term_max_linear", 0.15))
    quad = float(sec.get("term_max_quad", 0.00008))
    return max(2, int(base + lin * d + quad * d * d))


def sample_rational_term_count(settings: dict[str, Any] | None, *, default: int = 3) -> int:
    """Pick a term count: continuous band when D is set, else settings/default.

    Ceiling grows unboundedly with D; sampling biases low so absurd sizes are
    possible without making every high-D draw O(100) terms.
    """
    settings = settings or {}
    hi = continuous_rational_term_count_max(settings)
    if hi is not None:
        d = max(0.0, settings_difficulty(settings, default=0.0))
        if d < 6:
            return int(random.randint(2, min(3, hi)))
        # Power bias toward the low end; ``random()**3`` still reaches ``hi``.
        u = random.random() ** 3
        return max(2, int(2 + (hi - 2) * u))
    raw = settings.get("term_count", default)
    try:
        return max(2, int(raw))
    except (TypeError, ValueError):
        return max(2, int(default))


def sample_rational_lcd_factors(settings: dict[str, Any] | None, *, default: int = 4) -> int:
    """Pick max LCD factor count: continuous band when D is set, else settings."""
    settings = settings or {}
    hi = continuous_rational_lcd_factors_max(settings)
    if hi is not None:
        d = max(0.0, settings_difficulty(settings, default=0.0))
        if d < 6:
            return int(random.randint(1, min(2, hi)))
        u = random.random() ** 3
        return max(1, int(1 + (hi - 1) * u))
    raw = settings.get("max_lcd_factors", default)
    try:
        return max(1, int(raw))
    except (TypeError, ValueError):
        return max(1, int(default))


def apply_continuous_rational_structure(settings: dict[str, Any] | None) -> dict[str, Any]:
    """When continuous D is set, override EMH plateaus for LCD / term caps.

    Pedagogical add/subtract recipes (``shared_lcd`` / ``unlike_binomials`` /
    ``multi_term``) keep their fixed structure; ``complex`` and simplify/×÷
    paths grow unboundedly with D.
    """
    out = dict(settings or {})
    structure = str(out.get("add_subtract_structure", "")).strip().lower()
    if structure in {"shared_lcd", "unlike_binomials", "multi_term"}:
        return out

    lcd = continuous_rational_lcd_factors_max(out)
    terms = continuous_rational_term_count_max(out)
    if lcd is not None:
        # Ceiling grows unboundedly; builder samples within ``[lo, max]``.
        out["max_lcd_factors"] = int(lcd)
        out["max_rational_terms"] = max(
            int(out.get("max_rational_terms") or 0),
            int(lcd),
            int(terms or 2),
        )
    if terms is not None:
        out["term_count"] = sample_rational_term_count(out, default=terms)
        out["max_rational_terms"] = max(
            int(out.get("max_rational_terms") or 0),
            int(out["term_count"]),
        )
        # ×÷ operand budget tracks the same continuous growth.
        d = max(0.0, settings_difficulty(out, default=0.0))
        if d < 6:
            out["operand_count"] = 2
        else:
            u = random.random() ** 3
            out["operand_count"] = max(2, int(2 + (terms - 2) * u))
    return out


def allowed_rational_cancel_counts(d: float) -> tuple[int, ...]:
    """Cancel counts unlocked at difficulty ``d`` (always includes default=1).

    After ``unlock_4_d``, exact counts grow with ``continuous_rational_cancel_max``
    (unbounded — no plateau at 4).
    """
    eff = max(0.0, float(d))
    thresholds = _unlock_thresholds()
    unlocked = [default_cancel_count()]
    for count, min_d in sorted(thresholds.items()):
        if count == default_cancel_count():
            continue
        if count >= 4:
            continue  # handled by continuous growth below
        if eff + 1e-12 >= float(min_d) and count not in unlocked:
            unlocked.append(count)

    hi = continuous_rational_cancel_max(eff)
    unlock_hi = float(thresholds.get(4, _UNLOCK_4_D))
    if eff + 1e-12 >= unlock_hi:
        for count in range(4, hi + 1):
            if count not in unlocked:
                unlocked.append(count)
    return tuple(sorted(unlocked))


def _coerce_explicit_cancel_count(raw: Any) -> int | None:
    if raw is None:
        return None
    if isinstance(raw, str):
        text = raw.strip().lower()
        if text in {"", "random", "auto"}:
            return None
        # UI option "4" is labeled "All available"; keep that classroom meaning.
        if text in {"all", "all_available", "max", "4"}:
            return ALL_AVAILABLE_CANCEL
        raw = text
    try:
        return max(0, int(raw))
    except (TypeError, ValueError):
        return None


def resolve_rational_cancel_count(
    settings: dict[str, Any] | None,
    *,
    d: float | None = None,
    rng: random.Random | None = None,
) -> int:
    """Pick a cancel count: explicit setting, else sample from D-unlocked pool."""
    settings = settings or {}
    explicit = _coerce_explicit_cancel_count(settings.get("cancel_factor_count"))
    if explicit is not None:
        return explicit

    eff = float(d) if d is not None else settings_difficulty(settings, default=0.0)
    pool = allowed_rational_cancel_counts(eff)
    if len(pool) == 1:
        return pool[0]

    prefer = default_cancel_count()
    weight = fget("rational_cancel", "prefer_default_weight", _PREFER_DEFAULT_WEIGHT)
    weights = [float(weight) if c == prefer else 1.0 for c in pool]
    chooser = rng if rng is not None else random
    return int(chooser.choices(pool, weights=weights, k=1)[0])


def clamp_cancel_to_available(requested: int, available: int) -> int:
    """Honor cancel target when possible; otherwise cancel every available factor.

    Never fails generation — returns ``min(requested, available)`` (floored at 0).
    """
    return max(0, min(int(requested), max(0, int(available))))


def cancel_count_unlocked(d: float, count: int) -> bool:
    return int(count) in allowed_rational_cancel_counts(d)


def is_all_available_cancel(count: int) -> bool:
    return int(count) >= ALL_AVAILABLE_CANCEL
