"""Worksheet-level difficulty → per-question D ramp bands.

Named Level presets (and a continuous 0–24 slider) map to ``d_min`` / ``d_max``
used by progressive practice (``difficulty_ramp`` / ``build_progressive_sections``).

Documented mapping
------------------
| Worksheet preset | label   | d_min | d_max | schedule |
|------------------|---------|-------|-------|----------|
| level-0          | Level 0 | 0     | 3     | intro    |
| level-1          | Level 1 | 0     | 8     | gentle   |
| level-2          | Level 2 | 3     | 20    | moderate |
| level-3          | Level 3 | 8     | 25    | steep    |
| level-4          | Level 4 | 20    | 25    | intense  |

There is no Level 5 — only five ranges (0–4) were specified.

Legacy / prior-preset aliases (input only — never used as display labels)
-----------------------------------------------------------------------
| Alias                         | Maps to  |
|-------------------------------|----------|
| easy, e                       | level-1  |
| medium, m                     | level-2  |
| hard, h                       | level-3  |
| d0-8                          | level-1  |
| d4-14                         | level-2  |
| d10-22                        | level-3  |
| d0-3, d3-20, d8-25, d20-25    | level-0…4 |

A numeric worksheet D in ``[0, 24]`` linearly interpolates between the level-0
and level-4 bands (so D≈0 ≈ level-0, D≈24 ≈ level-4).
"""

from __future__ import annotations

from typing import Any

WorksheetDifficulty = str | int | float

NAMED_RAMPS: dict[str, dict[str, Any]] = {
    "level-0": {
        "level": "level-0",
        "label": "Level 0",
        "d_min": 0.0,
        "d_max": 3.0,
        "schedule": "intro",
        "description": "Introductory band: most items at very low D.",
    },
    "level-1": {
        "level": "level-1",
        "label": "Level 1",
        "d_min": 0.0,
        "d_max": 8.0,
        "schedule": "gentle",
        "description": "Most items at low D with a gentle ramp.",
    },
    "level-2": {
        "level": "level-2",
        "label": "Level 2",
        "d_min": 3.0,
        "d_max": 20.0,
        "schedule": "moderate",
        "description": "Mid-band difficulties with a moderate ramp.",
    },
    "level-3": {
        "level": "level-3",
        "label": "Level 3",
        "d_min": 8.0,
        "d_max": 25.0,
        "schedule": "steep",
        "description": "High-band difficulties with a steep ramp.",
    },
    "level-4": {
        "level": "level-4",
        "label": "Level 4",
        "d_min": 20.0,
        "d_max": 25.0,
        "schedule": "intense",
        "description": "Sustained high-D practice near the top of the band.",
    },
}

WORKSHEET_DIFFICULTY_PRESETS = [
    "level-0",
    "level-1",
    "level-2",
    "level-3",
    "level-4",
]

# Legacy EMH + prior D-range aliases (input only — never used as display labels).
_LEGACY = {
    "easy": "level-1",
    "e": "level-1",
    "medium": "level-2",
    "m": "level-2",
    "hard": "level-3",
    "h": "level-3",
    "d0-8": "level-1",
    "d4-14": "level-2",
    "d10-22": "level-3",
    "d0-3": "level-0",
    "d3-20": "level-2",
    "d8-25": "level-3",
    "d20-25": "level-4",
}
for _alias, _target in _LEGACY.items():
    NAMED_RAMPS[_alias] = NAMED_RAMPS[_target]

_SCHEDULE_BY_BUCKET = ("intro", "gentle", "moderate", "steep", "intense")


def _lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def worksheet_difficulty_to_ramp(level: WorksheetDifficulty) -> dict[str, Any]:
    """Map a worksheet difficulty label or 0–24 slider value to a D ramp.

    Returns ``{level, label, d_min, d_max, schedule, description}``.
    """
    if isinstance(level, str):
        key = level.strip().lower()
        if key in NAMED_RAMPS:
            return dict(NAMED_RAMPS[key])
        # Allow numeric strings ("12", "12.5").
        try:
            level = float(key)
        except ValueError as exc:
            raise ValueError(
                f"Unknown worksheet difficulty {level!r}; "
                "use level-0…level-4 or a number in [0, 24]."
            ) from exc

    t = max(0.0, min(24.0, float(level))) / 24.0
    low = NAMED_RAMPS["level-0"]
    high = NAMED_RAMPS["level-4"]
    d_min = round(_lerp(float(low["d_min"]), float(high["d_min"]), t), 4)
    d_max = round(_lerp(float(low["d_max"]), float(high["d_max"]), t), 4)
    bucket = min(4, int(t * 5))
    named = WORKSHEET_DIFFICULTY_PRESETS[bucket]
    schedule = _SCHEDULE_BY_BUCKET[bucket]
    return {
        "level": named,
        "slider": float(level) if not isinstance(level, str) else float(t * 24),
        "label": f"D {float(level):g}",
        "d_min": d_min,
        "d_max": d_max,
        "schedule": schedule,
        "description": (
            f"Continuous worksheet D={float(level):g} → "
            f"questions ramp from {d_min:g} to {d_max:g} ({schedule})."
        ),
    }


def apply_worksheet_difficulty(
    progressive: dict[str, Any],
    level: WorksheetDifficulty | None = None,
) -> dict[str, Any]:
    """Return a copy of ``progressive`` with d_min/d_max filled from worksheet difficulty.

    Uses ``level`` if given, else ``progressive["worksheet_difficulty"]``.
    Existing explicit d_min/d_max win unless ``overwrite`` is set via level only.
    """
    out = dict(progressive)
    raw = level if level is not None else out.get("worksheet_difficulty")
    if raw is None:
        return out
    ramp = worksheet_difficulty_to_ramp(raw)  # type: ignore[arg-type]
    out["worksheet_difficulty"] = ramp["level"]
    out["d_min"] = ramp["d_min"]
    out["d_max"] = ramp["d_max"]
    out["schedule"] = ramp["schedule"]
    return out
