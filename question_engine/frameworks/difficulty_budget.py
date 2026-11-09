"""Continuous difficulty budget: caps, downstream-weighted allocation, degradation."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Any, Sequence

# Soft UI guidance for the convenience slider (not a hard generation ceiling).
# Live value also in difficulty_knobs.json → ui.soft_slider_max.
DEFAULT_D_MAX = 24.0


def soft_slider_max() -> float:
    from question_engine.frameworks.primitives.difficulty_knobs import fget

    return fget("ui", "soft_slider_max", DEFAULT_D_MAX)


@dataclass(frozen=True)
class DifficultyFactor:
    id: str
    cost: float
    tags: tuple[str, ...] = ()


@dataclass
class LayerAllocation:
    primitive_id: str
    allocated: float
    cap: float
    effective: float
    depth_weight: float


@dataclass
class BudgetPlan:
    topic_d: float
    d_max: float
    layers: list[LayerAllocation] = field(default_factory=list)
    degraded: list[str] = field(default_factory=list)

    def effective_for(self, primitive_id: str) -> float:
        for layer in self.layers:
            if layer.primitive_id == primitive_id:
                return layer.effective
        return 0.0

    def to_spend_dict(self) -> dict[str, float]:
        return {layer.primitive_id: round(layer.effective, 3) for layer in self.layers}


def clamp_difficulty(d: float, d_max: float | None = None) -> float:
    """Floor difficulty at 0; optionally apply an upper bound when ``d_max`` is set.

    User-entered topic difficulty is not capped by default — pass ``d_max`` only
    when an explicit ceiling is intended.
    """
    try:
        value = float(d)
    except (TypeError, ValueError):
        return 0.0
    if math.isnan(value) or math.isinf(value) or value < 0:
        return 0.0
    if d_max is not None:
        try:
            upper = float(d_max)
        except (TypeError, ValueError):
            return value
        if math.isfinite(upper):
            return min(value, upper)
    return value


def parse_optional_prereq_cap(value: Any) -> float | None:
    """Parse a prereq-cap setting value.

    Returns ``None`` for no-cap sentinels (``None``, empty / whitespace string,
    ``\"none\"`` / ``\"uncapped\"`` / ``\"unlimited\"``, non-finite numbers).
    Otherwise returns a non-negative finite float (floor at 0).
    """
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, str):
        text = value.strip().lower()
        if text in {"", "none", "uncapped", "unlimited", "null", "undefined"}:
            return None
        try:
            parsed = float(text)
        except ValueError:
            return None
    else:
        try:
            parsed = float(value)
        except (TypeError, ValueError):
            return None
    if not math.isfinite(parsed):
        return None
    return max(0.0, parsed)


def _softmax_weights(raw: Sequence[float], temperature: float = 1.0) -> list[float]:
    if not raw:
        return []
    t = max(1e-6, float(temperature))
    shifted = [w / t for w in raw]
    m = max(shifted)
    exps = [math.exp(w - m) for w in shifted]
    s = sum(exps) or 1.0
    return [e / s for e in exps]


def allocate_budget(
    topic_d: float,
    primitive_ids: Sequence[str],
    *,
    prereq_caps: dict[str, float] | None = None,
    depth_weights: Sequence[float] | None = None,
    d_max: float | None = None,
    rng: random.Random | None = None,
    temperature: float = 1.0,
) -> BudgetPlan:
    """Allocate topic D across primitives with downstream-biased weights.

    Later primitives in ``primitive_ids`` (prereq order: early → late) get higher
    default depth weights. Caps clamp each share. Total effective spend may be
    less than topic_d when caps bind — that is intentional.

    ``d_max`` is an optional explicit ceiling on topic D and uncapped layer
    defaults. When omitted, topic D is only floored at 0 and uncapped layers
    may use their full share of topic D.
    """
    rng = rng or random.Random()
    caps = prereq_caps or {}
    topic_d = clamp_difficulty(topic_d, d_max)
    plan_d_max = float(d_max) if d_max is not None else topic_d
    ids = list(primitive_ids)
    n = len(ids)
    if n == 0:
        return BudgetPlan(topic_d=topic_d, d_max=plan_d_max)

    if depth_weights is None:
        # Prefer later / downstream complexity: 1, 2, ..., n
        depth_weights = [float(i + 1) for i in range(n)]
    else:
        depth_weights = [float(w) for w in depth_weights]
        if len(depth_weights) != n:
            raise ValueError("depth_weights must match primitive_ids length")

    # Light noise so allocation is not deterministic every time.
    noisy = [max(1e-6, w * rng.uniform(0.75, 1.25)) for w in depth_weights]
    probs = _softmax_weights(noisy, temperature=temperature)

    # Draw a Dirichlet-like share via normalized exponential noise * weights.
    draws = [p * rng.random() for p in probs]
    draw_sum = sum(draws) or 1.0
    shares = [topic_d * (x / draw_sum) for x in draws]

    layers: list[LayerAllocation] = []
    for pid, weight, share in zip(ids, depth_weights, shares):
        if pid in caps:
            cap = max(0.0, float(caps[pid]))
        elif d_max is not None:
            cap = max(0.0, float(d_max))
        else:
            # No prereq cap and no global ceiling: allow the full share.
            cap = topic_d
        effective = min(share, cap)
        layers.append(
            LayerAllocation(
                primitive_id=pid,
                allocated=share,
                cap=cap,
                effective=effective,
                depth_weight=weight,
            )
        )
    return BudgetPlan(topic_d=topic_d, d_max=plan_d_max, layers=layers)


def select_upgrades(
    upgrades: Sequence[DifficultyFactor],
    budget: float,
    *,
    allowed_ids: set[str] | None = None,
    rng: random.Random | None = None,
) -> tuple[list[DifficultyFactor], float, list[str]]:
    """Buy upgrades in list order while budget remains (in-layer priority).

    Returns (purchased, remaining_budget, skipped_ids).
    """
    rng = rng or random.Random()
    remaining = float(budget)
    purchased: list[DifficultyFactor] = []
    skipped: list[str] = []
    for factor in upgrades:
        if allowed_ids is not None and factor.id not in allowed_ids:
            skipped.append(factor.id)
            continue
        if factor.cost <= remaining + 1e-9:
            purchased.append(factor)
            remaining -= factor.cost
        else:
            skipped.append(factor.id)
    return purchased, remaining, skipped


def degrade_drop_most_expensive(
    purchased: list[DifficultyFactor],
) -> tuple[list[DifficultyFactor], str | None]:
    """Graceful degradation: drop the most expensive purchased upgrade."""
    if not purchased:
        return purchased, None
    idx = max(range(len(purchased)), key=lambda i: purchased[i].cost)
    dropped = purchased[idx]
    kept = [f for i, f in enumerate(purchased) if i != idx]
    return kept, dropped.id


def settings_difficulty(settings: dict[str, Any], default: float = 0.0) -> float:
    """Read continuous difficulty from settings; shim old EMH tiers if needed."""
    legacy = {"easy": 3.0, "medium": 8.0, "hard": 14.0}
    # Prefer explicit conceptual axis when present (Calc dual-difficulty UI).
    if (
        "conceptual_difficulty" in settings
        and settings["conceptual_difficulty"] is not None
    ):
        raw = settings["conceptual_difficulty"]
        try:
            return float(raw)
        except (TypeError, ValueError):
            pass
    if "difficulty" in settings and settings["difficulty"] is not None:
        raw = settings["difficulty"]
        try:
            return float(raw)
        except (TypeError, ValueError):
            # UI / presets sometimes put the tier name in ``difficulty``.
            mapped = legacy.get(str(raw).strip().lower())
            if mapped is not None:
                return mapped
    tier = str(settings.get("difficulty_tier", "")).strip().lower()
    return legacy.get(tier, default)


def settings_conceptual_difficulty(
    settings: dict[str, Any], default: float = 0.0
) -> float:
    """Conceptual / method difficulty (capped by leaf approx max)."""
    return settings_difficulty(settings, default=default)


def settings_spec_difficulty(settings: dict[str, Any]) -> float | None:
    """Independent Spec/effort difficulty, or None when unset (legacy single-D).

    ``None`` means callers should derive Spec spend from the legacy single-D
    budget split. An explicit ``0`` means Spec is intentionally off.
    """
    if "spec_difficulty" not in settings or settings["spec_difficulty"] is None:
        return None
    try:
        return max(0.0, float(settings["spec_difficulty"]))
    except (TypeError, ValueError):
        return None


def resolve_dual_difficulty(
    settings: dict[str, Any], *, default_conceptual: float = 6.0
) -> tuple[float, float | None]:
    """Return ``(conceptual_d, spec_d_or_None)``.

    When ``spec_difficulty`` is absent, Spec is ``None`` (legacy single-D path).
    """
    c = settings_conceptual_difficulty(settings, default=default_conceptual)
    return max(0.0, float(c)), settings_spec_difficulty(settings)


def dual_axis_rngs(
    settings: dict[str, Any],
    *,
    xor_mask: int = 0,
) -> tuple[random.Random, random.Random]:
    """Return ``(skeleton_rng, dress_rng)`` for dual-axis Spec isolation.

    Skeleton stream ignores Spec seed when ``conceptual_seed`` is set (or when
    Spec is peeled from ``seed``). Dress stream may mix ``spec_seed``.
    Legacy single-D (no ``spec_difficulty``): both streams share the same seed.
    """
    raw = settings.get("seed")
    try:
        base = int(raw) if raw is not None else None
    except (TypeError, ValueError):
        base = None

    spec = settings_spec_difficulty(settings)
    c = float(settings_conceptual_difficulty(settings, default=0.0))

    # Dress / Spec stream
    if base is None and settings.get("spec_seed") is None:
        dress = random.Random()
    else:
        dbase = 0 if base is None else base
        try:
            if settings.get("spec_seed") is not None:
                dbase = dbase + int(settings["spec_seed"]) * 10007
        except (TypeError, ValueError):
            pass
        idx = int(settings.get("_batch_index") or 0)
        dress = random.Random((dbase + idx * 1009) ^ int(xor_mask))

    # Skeleton / conceptual stream
    if spec is None and settings.get("conceptual_seed") is None:
        return dress, dress

    if settings.get("conceptual_seed") is not None:
        try:
            sk = random.Random(int(settings["conceptual_seed"]) + int(c * 1000))
            return sk, dress
        except (TypeError, ValueError):
            pass

    sk_base = 0 if base is None else base
    try:
        # Gallery historically used seed += int(S*31); peel Spec contribution.
        if spec is not None:
            sk_base = sk_base - int(float(spec) * 31)
    except (TypeError, ValueError):
        pass
    sk = random.Random(
        (sk_base & 0xFFFFFFFF) ^ (int(c * 1009) & 0xFFFFFFFF) ^ int(xor_mask)
    )
    return sk, dress


def difficulty_band(d: float) -> str:
    """Map continuous D to legacy easy / medium / hard bands for presets."""
    if d <= 4.0 + 1e-9:
        return "easy"
    if d <= 11.0 + 1e-9:
        return "medium"
    return "hard"


def band_anchor(d: float, edges: Sequence[float] = (0.0, 4.0, 11.0)) -> float:
    """Left edge of the difficulty step that contains ``d``.

    Structural ladders may stay constant across a step. Numeric windows use
    the edge as the point where that step's bounds were written, then climb
    from there.
    """
    value = max(0.0, float(d))
    anchor = float(edges[0]) if edges else 0.0
    for edge in edges:
        if float(edge) <= value + 1e-9:
            anchor = float(edge)
        else:
            break
    return anchor


def slide_window(
    lo: int,
    hi: int,
    d: float,
    *,
    anchor: float | None = None,
    edges: Sequence[float] = (0.0, 4.0, 11.0),
    cap: int | None = None,
    lo_floor: int | None = None,
) -> tuple[int, int]:
    """Slide an integer window up with difficulty past ``anchor``.

    The width stays the same, so a seeded ``randint(lo, hi)`` draws a value
    that is larger by exactly the number of steps. Use this when the question
    form would otherwise stay put: the numbers themselves get harder.

    ``cap`` stops the ceiling (percents, angles). The floor never passes it.
    """
    if lo > hi:
        lo, hi = hi, lo
    if anchor is None:
        anchor = band_anchor(d, edges)
    steps = int(math.floor(max(0.0, float(d) - float(anchor))))
    new_lo = int(lo) + steps
    new_hi = int(hi) + steps
    if lo_floor is not None:
        new_lo = max(int(lo_floor), new_lo)
    if cap is not None:
        new_hi = min(int(cap), new_hi)
        new_lo = min(new_lo, new_hi)
    if new_lo > new_hi:
        new_lo = new_hi
    return new_lo, new_hi


# Structural counters. Climbing these would change the question form inside a
# step that is supposed to stay on one skill (degree, how many angle pieces).
_DO_NOT_CLIMB = frozenset(
    {
        "power_min",
        "power_max",
        "angle_piece_min",
        "angle_piece_max",
        "max_degree",
        "poly_theory_degree_max",
        "pfd_term_count",
    }
)


def _numeric_difficulty(settings: dict[str, Any]) -> float | None:
    if "difficulty" not in settings or settings["difficulty"] is None:
        return None
    try:
        return float(settings["difficulty"])
    except (TypeError, ValueError):
        return None


def _is_climbable_bound(key: str) -> bool:
    if key in _DO_NOT_CLIMB or "degree" in key:
        return False
    return key.endswith("_min") or key.endswith("_max")


def _climb_frozen_int_bounds(raw_fn, settings: dict[str, Any]):
    """Raise integer bounds that a difficulty step would otherwise leave frozen.

    ``raw_fn(settings)`` is the existing ladder. Where that ladder's integer
    bound does not move, the result still moves by one per difficulty point:
    positive windows slide up (same width, so a seeded draw is larger), and
    windows that cross zero grow in magnitude.
    """
    produced = raw_fn(settings)
    if not isinstance(produced, dict):
        return produced
    d = _numeric_difficulty(settings)
    if d is None or d <= 0:
        return produced
    steps = int(math.floor(d))
    protected = {
        key
        for key, value in settings.items()
        if isinstance(value, int) and not isinstance(value, bool)
    }
    cache: dict[int, dict[str, Any]] = {}

    def raw_at(t: int) -> dict[str, Any]:
        hit = cache.get(t)
        if hit is None:
            probe = dict(settings)
            probe["difficulty"] = t
            hit = raw_fn(probe)
            cache[t] = hit if isinstance(hit, dict) else {}
        return hit

    keys = [
        key
        for key, value in produced.items()
        if key not in protected
        and _is_climbable_bound(key)
        and isinstance(value, int)
        and not isinstance(value, bool)
    ]
    paired: set[str] = set()
    out = dict(produced)
    for key in keys:
        if not key.endswith("_max"):
            continue
        partner = key[: -len("_max")] + "_min"
        if partner not in keys:
            continue
        paired.add(key)
        paired.add(partner)
        first = None
        for t in range(0, steps + 1):
            raw_max = raw_at(t).get(key)
            raw_min = raw_at(t).get(partner)
            if isinstance(raw_max, int) and not isinstance(raw_max, bool) and isinstance(
                raw_min, int
            ) and not isinstance(raw_min, bool):
                first = t
                break
        if first is None:
            continue
        climbed_max = int(raw_at(first)[key])
        for t in range(first + 1, steps + 1):
            raw_max = raw_at(t).get(key)
            if not isinstance(raw_max, int) or isinstance(raw_max, bool):
                raw_max = climbed_max
            climbed_max = max(climbed_max + 1, int(raw_max))
        if key == "angle_max":
            climbed_max = min(climbed_max, 175)
        raw_max_now = int(raw_at(steps)[key])
        raw_min_now = int(raw_at(steps)[partner])
        delta = climbed_max - raw_max_now
        if raw_min_now < 0 < raw_max_now:
            climbed_min = -climbed_max if raw_min_now == -raw_max_now else raw_min_now - delta
        else:
            climbed_min = raw_min_now + delta
        if key == "angle_max":
            climbed_min = min(max(1, climbed_min), climbed_max - 5)
        out[partner] = climbed_min
        out[key] = climbed_max
    for key in keys:
        if key in paired:
            continue
        first = None
        for t in range(0, steps + 1):
            raw_value = raw_at(t).get(key)
            if isinstance(raw_value, int) and not isinstance(raw_value, bool):
                first = t
                break
        if first is None:
            continue
        value = int(raw_at(first)[key])
        for t in range(first + 1, steps + 1):
            raw_value = raw_at(t).get(key)
            if not isinstance(raw_value, int) or isinstance(raw_value, bool):
                raw_value = value
            value = max(value + 1, int(raw_value))
        out[key] = value
    return out


def climb_frozen_int_bounds(raw_fn):
    """Decorator: integer magnitude bounds keep moving after a ladder step stalls."""

    def wrapped(settings: dict[str, Any]):
        return _climb_frozen_int_bounds(raw_fn, settings)

    wrapped.__name__ = getattr(raw_fn, "__name__", "wrapped")
    wrapped.__doc__ = getattr(raw_fn, "__doc__", None)
    wrapped.__wrapped__ = raw_fn
    return wrapped


def settings_difficulty_band(settings: dict[str, Any], *, default: float = 8.0) -> str:
    """Band from continuous ``difficulty`` when present, else ``difficulty_tier``."""
    if "difficulty" in settings and settings["difficulty"] is not None:
        raw = settings["difficulty"]
        try:
            return difficulty_band(float(raw))
        except (TypeError, ValueError):
            legacy = str(raw).strip().lower()
            if legacy in {"easy", "medium", "hard"}:
                return legacy
    tier = str(settings.get("difficulty_tier", "")).strip().lower()
    if tier in {"easy", "medium", "hard"}:
        return tier
    return difficulty_band(default)
