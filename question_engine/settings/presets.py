"""Difficulty-tier presets that fill domain settings for a profile or generator.

Structure
---------
``PROFILE_DIFFICULTY_PRESETS`` maps a setting profile name (``equation``,
``polynomial``, …) to ``{easy|medium|hard: {setting_key: value}}``.

``GENERATOR_DIFFICULTY_PRESETS`` optionally overrides by generator / type id.

On generate, call ``apply_difficulty_presets`` so API clients that only send
``difficulty_tier`` get the same bounds as the UI. Explicit settings always win
over preset values (``{**preset, **settings}``).

To add presets for a new question type:
1. Prefer adding under the type's ``setting_profile`` in
   ``PROFILE_DIFFICULTY_PRESETS``.
2. For one-off generator overrides, add an entry in
   ``GENERATOR_DIFFICULTY_PRESETS`` keyed by generator / type id.
"""

from __future__ import annotations

from typing import Any, Mapping

DifficultyTier = str  # "easy" | "medium" | "hard"
PresetValues = dict[str, Any]
TierPresets = dict[DifficultyTier, PresetValues]

# Shared enrichment knobs applied when a profile has no more specific entry.
_COMMON_TERMS: TierPresets = {
    "easy": {"min_terms": 2, "max_terms": 3},
    "medium": {"min_terms": 2, "max_terms": 4},
    "hard": {"min_terms": 3, "max_terms": 6},
}

PROFILE_DIFFICULTY_PRESETS: dict[str, TierPresets] = {
    "equation": {
        "easy": {
            "coef_min": -5,
            "coef_max": 5,
            "integer_only": True,
        },
        "medium": {
            "coef_min": -12,
            "coef_max": 12,
            "integer_only": True,
        },
        "hard": {
            "coef_min": -20,
            "coef_max": 20,
            "integer_only": False,
        },
    },
    "inequality": {
        "easy": {
            "coef_min": -5,
            "coef_max": 5,
            "integer_only": True,
        },
        "medium": {
            "coef_min": -12,
            "coef_max": 12,
            "integer_only": True,
        },
        "hard": {
            "coef_min": -20,
            "coef_max": 20,
            "integer_only": False,
        },
    },
    "compound_inequality": {
        "easy": {
            "coef_min": -5,
            "coef_max": 5,
            "integer_only": True,
        },
        "medium": {
            "coef_min": -12,
            "coef_max": 12,
            "integer_only": True,
        },
        "hard": {
            "coef_min": -20,
            "coef_max": 20,
            "integer_only": False,
        },
    },
    "polynomial": {
        "easy": {
            "coef_min": -5,
            "coef_max": 5,
            "min_degree": 1,
            "max_degree": 2,
            "integer_coefficients_only": True,
        },
        "medium": {
            "coef_min": -10,
            "coef_max": 10,
            "min_degree": 1,
            "max_degree": 3,
            "integer_coefficients_only": True,
        },
        "hard": {
            "coef_min": -15,
            "coef_max": 15,
            "min_degree": 2,
            "max_degree": 5,
            "integer_coefficients_only": False,
        },
    },
    "polynomial_factoring": {
        "easy": {
            "coef_min": -5,
            "coef_max": 5,
            "min_degree": 2,
            "max_degree": 2,
        },
        "medium": {
            "coef_min": -10,
            "coef_max": 10,
            "min_degree": 2,
            "max_degree": 3,
        },
        "hard": {
            "coef_min": -15,
            "coef_max": 15,
            "min_degree": 2,
            "max_degree": 4,
        },
    },
    "polynomial_division": {
        "easy": {
            "coef_min": -5,
            "coef_max": 5,
            "numerator_degree_min": 2,
            "numerator_degree_max": 3,
            "denominator_degree_min": 1,
            "denominator_degree_max": 1,
            "divide_cleanly": True,
        },
        "medium": {
            "coef_min": -10,
            "coef_max": 10,
            "numerator_degree_min": 2,
            "numerator_degree_max": 4,
            "denominator_degree_min": 1,
            "denominator_degree_max": 2,
            "divide_cleanly": True,
        },
        "hard": {
            "coef_min": -15,
            "coef_max": 15,
            "numerator_degree_min": 3,
            "numerator_degree_max": 5,
            "denominator_degree_min": 1,
            "denominator_degree_max": 2,
            "divide_cleanly": False,
        },
    },
    "number": {
        "easy": {
            "num_min": -5,
            "num_max": 5,
            "denom_min": 2,
            "denom_max": 6,
            "allow_negative": False,
            **_COMMON_TERMS["easy"],
        },
        "medium": {
            "num_min": -10,
            "num_max": 10,
            "denom_min": 2,
            "denom_max": 12,
            "allow_negative": True,
            **_COMMON_TERMS["medium"],
        },
        "hard": {
            "num_min": -20,
            "num_max": 20,
            "denom_min": 2,
            "denom_max": 20,
            "allow_negative": True,
            **_COMMON_TERMS["hard"],
        },
    },
    "rational": {
        "easy": {
            "num_min": -5,
            "num_max": 5,
            "denom_min": 2,
            "denom_max": 6,
            "coef_min": -5,
            "coef_max": 5,
            "allow_negative": False,
            "allow_obelus": True,
            "allow_complex_fraction": False,
            "allow_slash": False,
            **_COMMON_TERMS["easy"],
        },
        "medium": {
            "num_min": -10,
            "num_max": 10,
            "denom_min": 2,
            "denom_max": 12,
            "coef_min": -10,
            "coef_max": 10,
            "allow_negative": True,
            "allow_obelus": True,
            "allow_complex_fraction": False,
            "allow_slash": True,
            **_COMMON_TERMS["medium"],
        },
        "hard": {
            "num_min": -20,
            "num_max": 20,
            "denom_min": 2,
            "denom_max": 20,
            "coef_min": -15,
            "coef_max": 15,
            "allow_negative": True,
            "allow_obelus": True,
            "allow_complex_fraction": True,
            "allow_slash": True,
            **_COMMON_TERMS["hard"],
        },
    },
    "percent": {
        "easy": {
            "percent_min": 5,
            "percent_max": 50,
            "base_min": 10,
            "base_max": 100,
            "round_to_whole": True,
            "allow_decimal_percents": False,
        },
        "medium": {
            "percent_min": 5,
            "percent_max": 75,
            "base_min": 10,
            "base_max": 200,
            "round_to_whole": False,
            "allow_decimal_percents": False,
        },
        "hard": {
            "percent_min": 1,
            "percent_max": 99,
            "base_min": 10,
            "base_max": 500,
            "round_to_whole": False,
            "allow_decimal_percents": True,
        },
    },
    "decimal": {
        "easy": {"decimal_places": 1, "allow_negative": False},
        "medium": {"decimal_places": 2, "allow_negative": False},
        "hard": {"decimal_places": 3, "allow_negative": True},
    },
    "ratio": {
        "easy": {"ratio_part_min": 1, "ratio_part_max": 8},
        "medium": {"ratio_part_min": 2, "ratio_part_max": 15},
        "hard": {"ratio_part_min": 2, "ratio_part_max": 30},
    },
    "unit_rate": {
        "easy": {
            "unit_rate_min": 2,
            "unit_rate_max": 8,
            "unit_rate_multiplier_min": 2,
            "unit_rate_multiplier_max": 5,
        },
        "medium": {
            "unit_rate_min": 2,
            "unit_rate_max": 12,
            "unit_rate_multiplier_min": 2,
            "unit_rate_multiplier_max": 10,
        },
        "hard": {
            "unit_rate_min": 2,
            "unit_rate_max": 25,
            "unit_rate_multiplier_min": 3,
            "unit_rate_multiplier_max": 15,
        },
    },
    "proportion": {
        "easy": {"ratio_part_min": 1, "ratio_part_max": 8},
        "medium": {"ratio_part_min": 2, "ratio_part_max": 12},
        "hard": {"ratio_part_min": 2, "ratio_part_max": 25},
    },
    "integer": {
        "easy": {"num_min": -10, "num_max": 10, "allow_negative": True},
        "medium": {"num_min": -20, "num_max": 20, "allow_negative": True},
        "hard": {"num_min": -50, "num_max": 50, "allow_negative": True},
    },
    "factor": {
        "easy": {"factor_min": 4, "factor_max": 30},
        "medium": {"factor_min": 4, "factor_max": 60},
        "hard": {"factor_min": 6, "factor_max": 120},
    },
    "order_of_operations": {
        "easy": {
            "pemdas_complexity": "basic",
            "num_min": 2,
            "num_max": 6,
        },
        "medium": {
            "pemdas_complexity": "mixed",
            "num_min": 2,
            "num_max": 9,
        },
        "hard": {
            "pemdas_complexity": "exponent",
            "num_min": 2,
            "num_max": 12,
        },
    },
    "distributive": {
        "easy": {"coef_min": -5, "coef_max": 5, "allow_negative": False},
        "medium": {"coef_min": -9, "coef_max": 9, "allow_negative": True},
        "hard": {"coef_min": -15, "coef_max": 15, "allow_negative": True},
    },
    "linear": {
        "easy": {
            "slope_min": -3,
            "slope_max": 3,
            "intercept_min": -5,
            "intercept_max": 5,
            "coord_min": -5,
            "coord_max": 5,
        },
        "medium": {
            "slope_min": -6,
            "slope_max": 6,
            "intercept_min": -8,
            "intercept_max": 8,
            "coord_min": -8,
            "coord_max": 8,
        },
        "hard": {
            "slope_min": -10,
            "slope_max": 10,
            "intercept_min": -12,
            "intercept_max": 12,
            "coord_min": -12,
            "coord_max": 12,
        },
    },
    "coordinate_plane": {
        "easy": {"coord_min": -5, "coord_max": 5},
        "medium": {"coord_min": -8, "coord_max": 8},
        "hard": {"coord_min": -12, "coord_max": 12},
    },
    "number_line": {
        "easy": {"number_line_min": -8, "number_line_max": 8},
        "medium": {"number_line_min": -12, "number_line_max": 12},
        "hard": {"number_line_min": -20, "number_line_max": 20},
    },
    "systems": {
        "easy": {"coef_min": -5, "coef_max": 5, "integer_only": True},
        "medium": {"coef_min": -10, "coef_max": 10, "integer_only": True},
        "hard": {"coef_min": -15, "coef_max": 15, "integer_only": False},
    },
    "quadratic": {
        "easy": {
            "coef_min": -5,
            "coef_max": 5,
            "integer_only": True,
            **_COMMON_TERMS["easy"],
        },
        "medium": {
            "coef_min": -10,
            "coef_max": 10,
            "integer_only": True,
            **_COMMON_TERMS["medium"],
        },
        "hard": {
            "coef_min": -15,
            "coef_max": 15,
            "integer_only": False,
            **_COMMON_TERMS["hard"],
        },
    },
    "radical": {
        "easy": {"coef_min": 1, "coef_max": 10, **_COMMON_TERMS["easy"]},
        "medium": {"coef_min": 1, "coef_max": 20, **_COMMON_TERMS["medium"]},
        "hard": {"coef_min": 1, "coef_max": 40, **_COMMON_TERMS["hard"]},
    },
    "geometry": {
        "easy": {"side_min": 3, "side_max": 12, "angle_min": 20, "angle_max": 120},
        "medium": {"side_min": 3, "side_max": 20, "angle_min": 10, "angle_max": 170},
        "hard": {"side_min": 5, "side_max": 40, "angle_min": 5, "angle_max": 175},
    },
    "geometry_basic": {
        "easy": {"side_min": 3, "side_max": 12},
        "medium": {"side_min": 3, "side_max": 20},
        "hard": {"side_min": 5, "side_max": 40},
    },
    "geometry_angles": {
        "easy": {"angle_min": 20, "angle_max": 120},
        "medium": {"angle_min": 10, "angle_max": 170},
        "hard": {"angle_min": 5, "angle_max": 175},
    },
    "geometry_triangles": {
        "easy": {"side_min": 3, "side_max": 12, "angle_min": 20, "angle_max": 120},
        "medium": {"side_min": 3, "side_max": 20, "angle_min": 10, "angle_max": 170},
        "hard": {"side_min": 5, "side_max": 40, "angle_min": 5, "angle_max": 175},
    },
    "geometry_circles": {
        "easy": {"side_min": 3, "side_max": 12},
        "medium": {"side_min": 3, "side_max": 20},
        "hard": {"side_min": 5, "side_max": 40},
    },
    "word_problem": {
        "easy": {"difficulty": "easy", **_COMMON_TERMS["easy"]},
        "medium": {"difficulty": "medium", **_COMMON_TERMS["medium"]},
        "hard": {"difficulty": "hard", **_COMMON_TERMS["hard"]},
    },
    "common_enrichment": dict(_COMMON_TERMS),
}

# Optional per-generator / type-id overrides (wins over profile presets).
GENERATOR_DIFFICULTY_PRESETS: dict[str, TierPresets] = {}


def _normalize_tier(tier: Any) -> str | None:
    if tier is None:
        return None
    value = str(tier).strip().lower()
    if value in {"easy", "medium", "hard"}:
        return value
    return None


def lookup_difficulty_preset(
    tier: Any,
    *,
    type_id: str | None = None,
    setting_profile: str | None = None,
) -> PresetValues:
    """Return preset values for a tier, preferring generator overrides."""
    normalized = _normalize_tier(tier)
    if normalized is None:
        return {}

    if type_id:
        generator_presets = GENERATOR_DIFFICULTY_PRESETS.get(type_id)
        if generator_presets and normalized in generator_presets:
            return dict(generator_presets[normalized])

    if setting_profile:
        profile_presets = PROFILE_DIFFICULTY_PRESETS.get(setting_profile)
        if profile_presets and normalized in profile_presets:
            return dict(profile_presets[normalized])

    common = PROFILE_DIFFICULTY_PRESETS.get("common_enrichment", {})
    return dict(common.get(normalized, {}))


def resolve_setting_profile_for_type(type_id: str | None) -> str | None:
    """Best-effort profile lookup from generator setting configs."""
    if not type_id:
        return None
    try:
        from .generator_profiles import config_for_generator
    except ImportError:
        return None
    config = config_for_generator(type_id)
    if config is None:
        return None
    return config.setting_profile


def apply_difficulty_presets(
    settings: Mapping[str, Any],
    *,
    type_id: str | None = None,
    setting_profile: str | None = None,
) -> dict[str, Any]:
    """Merge difficulty presets under explicit settings.

    Preset keys fill gaps / provide defaults; any key already present in
    ``settings`` keeps the caller's value.
    """
    merged = dict(settings)
    tier = merged.get("difficulty_tier")
    profile = setting_profile or resolve_setting_profile_for_type(type_id)
    preset = lookup_difficulty_preset(tier, type_id=type_id, setting_profile=profile)
    if not preset:
        return merged
    return {**preset, **merged}
