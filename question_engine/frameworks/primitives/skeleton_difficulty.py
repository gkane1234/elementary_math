"""Skeleton difficulty ladder — numeric hardness before format/structure.

User preference: at low/mid D only increase coefficient messiness inside a fixed
shape box; unlock presentation/structure dimensions sequentially at higher D.

``numeric_tier`` — larger coeffs, a≠1, fractions (same factor count / task shape).
``format_tier`` — factored prompts, expanded dens, extra inventory, insert-cancel
pairs, complex-fraction tiers, unsimplify dress, richer multiply shapes.

Both are deterministic functions of continuous D (no probabilistic tier bumps).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

# Format unlocks lag numeric so low/mid D widens coefficients inside a fixed shape.
_NUMERIC_THRESHOLDS = (4.0, 8.0, 14.0, 20.0)
_FORMAT_THRESHOLDS = (10.0, 16.0, 22.0, 28.0)


def _tier_from_thresholds(d: float, thresholds: tuple[float, ...]) -> int:
    d = max(0.0, float(d))
    tier = 0
    for edge in thresholds:
        if d >= edge:
            tier += 1
        else:
            break
    return tier


def skeleton_numeric_tier(d: float) -> int:
    """0–4: coefficient / monic hardness only."""
    return _tier_from_thresholds(d, _NUMERIC_THRESHOLDS)


def skeleton_format_tier(d: float) -> int:
    """0–4: structural / presentation unlocks."""
    return _tier_from_thresholds(d, _FORMAT_THRESHOLDS)


@dataclass(frozen=True)
class SkeletonDifficultyBands:
    numeric_tier: int
    format_tier: int
    effective_d: float

    @classmethod
    def from_d(cls, d: float) -> "SkeletonDifficultyBands":
        d = max(0.0, float(d))
        return cls(
            numeric_tier=skeleton_numeric_tier(d),
            format_tier=skeleton_format_tier(d),
            effective_d=d,
        )


def numeric_bias_for_tier(tier: int) -> dict[str, Any]:
    """Sampler weights / ranges for ``factor_sampler`` (numeric only)."""
    tier = max(0, min(4, int(tier)))
    const_hi = (4, 5, 7, 9, 12)[tier]
    nonmonic_weight = (0.0, 0.12, 0.35, 0.55, 0.75)[tier]
    coef_abs_bias = (0.05, 0.2, 0.4, 0.6, 0.85)[tier]
    leading_max = (1, 1, 2, 3, 4)[tier]
    allow_fraction_const = tier >= 3
    return {
        "const_hi_default": const_hi,
        "nonmonic_weight": nonmonic_weight,
        "coef_abs_bias": coef_abs_bias,
        "leading_max_default": leading_max,
        "allow_fraction_const": allow_fraction_const,
        "allow_nonmonic_from_d": 6.0 if tier >= 1 else 99.0,
    }


def format_bias_for_tier(tier: int) -> dict[str, Any]:
    """Presentation / dens_style bias (format only)."""
    tier = max(0, min(4, int(tier)))
    expand_weight = (0.0, 0.2, 0.45, 0.65, 0.8)[tier]
    prefer_factored_prompt = tier >= 1
    return {
        "expand_weight": expand_weight,
        "prefer_factored_prompt": prefer_factored_prompt,
    }


def complex_fraction_tier_from_format(format_tier: int) -> str:
    """Map format tier → complex-fraction structure band (deterministic)."""
    ft = max(0, int(format_tier))
    if ft >= 3:
        return "hard"
    if ft >= 2:
        return "medium"
    return "easy"
