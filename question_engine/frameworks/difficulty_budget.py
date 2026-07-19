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
    if "difficulty" in settings and settings["difficulty"] is not None:
        try:
            return float(settings["difficulty"])
        except (TypeError, ValueError):
            pass
    tier = str(settings.get("difficulty_tier", "")).strip().lower()
    legacy = {"easy": 3.0, "medium": 8.0, "hard": 14.0}
    return legacy.get(tier, default)
