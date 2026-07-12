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
            "steps": 1,
            "compound_style": "mixed",
            "allow_inclusive": False,
            "allow_lt": True,
            "allow_gt": True,
            "allow_lte": False,
            "allow_gte": False,
        },
        "medium": {
            "coef_min": -12,
            "coef_max": 12,
            "integer_only": True,
            "steps": 2,
            "compound_style": "mixed",
            "allow_inclusive": True,
            "allow_lt": True,
            "allow_gt": True,
            "allow_lte": True,
            "allow_gte": True,
        },
        "hard": {
            "coef_min": -20,
            "coef_max": 20,
            "integer_only": False,
            "steps": 3,
            "compound_style": "mixed",
            "allow_inclusive": True,
            "allow_lt": True,
            "allow_gt": True,
            "allow_lte": True,
            "allow_gte": True,
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
    # Factoring pedagogy:
    #   easy   — monic quadratics (a = 1) via normal factoring
    #   medium — non-monic quadratics (a ≠ 1) via normal factoring
    #   hard   — non-quadratic techniques (grouping, cubes, substitution)
    "polynomial_factoring": {
        "easy": {
            "coef_min": -5,
            "coef_max": 5,
            "min_degree": 2,
            "max_degree": 2,
            "leading_coefficient_one": True,
            "monic_only": True,
            "factor_normal": True,
            "factor_grouping": False,
            "factor_substitution": False,
            "factor_difference_of_squares": False,
            "factor_perfect_square_trinomial": False,
            "factor_difference_of_cubes": False,
            "factor_sum_of_cubes": False,
            "factor_rrt": False,
            "require_gcf": False,
            "difference_of_squares_only": False,
        },
        "medium": {
            "coef_min": -10,
            "coef_max": 10,
            "min_degree": 2,
            "max_degree": 2,
            "leading_coefficient_one": False,
            "monic_only": False,
            "factor_normal": True,
            "factor_grouping": False,
            "factor_substitution": False,
            "factor_difference_of_squares": False,
            "factor_perfect_square_trinomial": False,
            "factor_difference_of_cubes": False,
            "factor_sum_of_cubes": False,
            "factor_rrt": False,
            "require_gcf": False,
            "difference_of_squares_only": False,
        },
        "hard": {
            "coef_min": -12,
            "coef_max": 12,
            "min_degree": 3,
            "max_degree": 4,
            "leading_coefficient_one": False,
            "monic_only": False,
            "factor_normal": False,
            "factor_grouping": True,
            "factor_substitution": True,
            "factor_difference_of_squares": False,
            "factor_perfect_square_trinomial": False,
            "factor_difference_of_cubes": True,
            "factor_sum_of_cubes": True,
            "factor_rrt": False,
            "require_gcf": False,
            "difference_of_squares_only": False,
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
    "scientific_notation": {
        "easy": {
            "sci_exp_min": 1,
            "sci_exp_max": 3,
            "allow_negative_exponents": False,
            "mantissa_decimals": 1,
            "sci_write_direction": "to_sci",
            "sci_operation": "multiply",
            "require_normalization": False,
            "sci_exp_diff_min": 0,
            "sci_exp_diff_max": 0,
            "allow_magnitude_compare": False,
        },
        "medium": {
            "sci_exp_min": -4,
            "sci_exp_max": 6,
            "allow_negative_exponents": True,
            "mantissa_decimals": 2,
            "sci_write_direction": "both",
            "sci_operation": "mixed",
            "require_normalization": True,
            "sci_exp_diff_min": 1,
            "sci_exp_diff_max": 2,
            "allow_magnitude_compare": False,
        },
        "hard": {
            "sci_exp_min": -10,
            "sci_exp_max": 10,
            "allow_negative_exponents": True,
            "mantissa_decimals": 3,
            "sci_write_direction": "both",
            "sci_operation": "mixed",
            "require_normalization": True,
            "sci_exp_diff_min": 3,
            "sci_exp_diff_max": 6,
            "allow_magnitude_compare": True,
        },
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
    "more_on_slope": {
        "easy": {
            "slope_min": -3,
            "slope_max": 3,
            "intercept_min": -5,
            "intercept_max": 5,
            "coord_min": -5,
            "coord_max": 5,
            "ask_mode": "mixed",
            "allow_from_points": True,
            "allow_from_equation": True,
            "allow_from_graph": True,
            "allow_find_equation": False,
            "allow_classify": True,
            "allow_parallel_perpendicular": False,
            "show_points": False,
        },
        "medium": {
            "slope_min": -6,
            "slope_max": 6,
            "intercept_min": -8,
            "intercept_max": 8,
            "coord_min": -8,
            "coord_max": 8,
            "ask_mode": "mixed",
            "allow_from_points": True,
            "allow_from_equation": True,
            "allow_from_graph": True,
            "allow_find_equation": True,
            "allow_classify": True,
            "allow_parallel_perpendicular": True,
            "show_points": False,
        },
        "hard": {
            "slope_min": -10,
            "slope_max": 10,
            "intercept_min": -12,
            "intercept_max": 12,
            "coord_min": -12,
            "coord_max": 12,
            "ask_mode": "mixed",
            "allow_from_points": True,
            "allow_from_equation": True,
            "allow_from_graph": True,
            "allow_find_equation": True,
            "allow_classify": True,
            "allow_parallel_perpendicular": True,
            "show_points": False,
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
        "easy": {
            "coef_min": -5,
            "coef_max": 5,
            "integer_only": True,
            "system_coef_min": 1,
            "system_coef_max": 5,
            "max_coefficient_magnitude": 5,
            "prefer_integer_solutions": True,
        },
        "medium": {
            "coef_min": -10,
            "coef_max": 10,
            "integer_only": True,
            "system_coef_min": 1,
            "system_coef_max": 10,
            "max_coefficient_magnitude": 10,
            "prefer_integer_solutions": True,
        },
        "hard": {
            "coef_min": -15,
            "coef_max": 15,
            "integer_only": False,
            "system_coef_min": 1,
            "system_coef_max": 15,
            "max_coefficient_magnitude": 15,
            "prefer_integer_solutions": True,
        },
    },
    # Plane graphing types share linear slope/intercept/coord knobs.
    "graphing": {
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
    # Quadratic solve / analyze types (formula, square roots, discriminant, CTS, …):
    #   easy   — monic (a = 1); smaller coeffs; simpler discriminants/roots
    #   medium — a may be ≠ 1; wider integer coeffs
    #   hard   — a often ≠ 1; wider / messier (non-integer allowed)
    "quadratic": {
        "easy": {
            "coef_min": -5,
            "coef_max": 5,
            "integer_only": True,
            "leading_coefficient_one": True,
            "monic_only": True,
            **_COMMON_TERMS["easy"],
        },
        "medium": {
            "coef_min": -10,
            "coef_max": 10,
            "integer_only": True,
            "leading_coefficient_one": False,
            "monic_only": False,
            **_COMMON_TERMS["medium"],
        },
        "hard": {
            "coef_min": -15,
            "coef_max": 15,
            "integer_only": False,
            "leading_coefficient_one": False,
            "monic_only": False,
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
    "logarithm": {
        "easy": {"coef_min": 2, "coef_max": 5, "require_integer_result": True},
        "medium": {"coef_min": 2, "coef_max": 10, "require_integer_result": True},
        "hard": {"coef_min": 2, "coef_max": 16, "require_integer_result": False},
    },
    "exponential": {
        "easy": {"exp_base_min": 2, "exp_base_max": 5, "exp_exponent_max": 3},
        "medium": {"exp_base_min": 2, "exp_base_max": 8, "exp_exponent_max": 4},
        "hard": {"exp_base_min": 2, "exp_base_max": 12, "exp_exponent_max": 5},
    },
    "exponential_graph": {
        "easy": {
            "exp_base_min": 2,
            "exp_base_max": 3,
            "allow_decay": False,
            "allow_stretch": False,
            "allow_vertical_shift": False,
            "allow_horizontal_shift": False,
            "allow_reflection": False,
            "coord_min": -5,
            "coord_max": 5,
        },
        "medium": {
            "exp_base_min": 2,
            "exp_base_max": 4,
            "allow_decay": True,
            "allow_stretch": True,
            "allow_vertical_shift": True,
            "allow_horizontal_shift": True,
            "allow_reflection": False,
            "coord_min": -6,
            "coord_max": 6,
        },
        "hard": {
            "exp_base_min": 2,
            "exp_base_max": 5,
            "allow_decay": True,
            "allow_stretch": True,
            "allow_vertical_shift": True,
            "allow_horizontal_shift": True,
            "allow_reflection": True,
            "coord_min": -8,
            "coord_max": 8,
        },
    },
    "absolute_value_graph": {
        "easy": {
            "allow_shift_h": True,
            "allow_shift_k": False,
            "allow_stretch": False,
            "allow_reflection": False,
            "coef_min": 1,
            "coef_max": 1,
            "integer_only": True,
            "coord_min": -5,
            "coord_max": 5,
            "intercept_min": 0,
            "intercept_max": 0,
        },
        "medium": {
            "allow_shift_h": True,
            "allow_shift_k": True,
            "allow_stretch": True,
            "allow_reflection": True,
            "coef_min": -2,
            "coef_max": 2,
            "integer_only": True,
            "coord_min": -6,
            "coord_max": 6,
            "intercept_min": -5,
            "intercept_max": 5,
        },
        "hard": {
            "allow_shift_h": True,
            "allow_shift_k": True,
            "allow_stretch": True,
            "allow_reflection": True,
            "coef_min": -3,
            "coef_max": 3,
            "integer_only": False,
            "coord_min": -8,
            "coord_max": 8,
            "intercept_min": -8,
            "intercept_max": 8,
        },
    },
    # Graphing quadratics (forms + transforms):
    #   easy   — clean vertex; a = 1; one-axis shift; no rewrite
    #   medium — mix vertex / standard / factored; a≠1 sometimes; light messy
    #   hard   — often messy (needs algebra); fractional a; wider h/k
    "quadratic_graph": {
        "easy": {
            "allow_vertex_form": True,
            "allow_standard_form": False,
            "allow_factored_form": False,
            "allow_messy_form": False,
            "allow_shift_h": True,
            "allow_shift_k": True,
            "allow_stretch": False,
            "allow_reflection": False,
            "coef_min": 1,
            "coef_max": 1,
            "integer_only": True,
            "leading_coefficient_one": True,
            "monic_only": True,
            "coord_min": -3,
            "coord_max": 3,
            "intercept_min": -3,
            "intercept_max": 3,
        },
        "medium": {
            "allow_vertex_form": True,
            "allow_standard_form": True,
            "allow_factored_form": True,
            "allow_messy_form": True,
            "allow_shift_h": True,
            "allow_shift_k": True,
            "allow_stretch": True,
            "allow_reflection": True,
            "coef_min": -2,
            "coef_max": 2,
            "integer_only": True,
            "leading_coefficient_one": False,
            "monic_only": False,
            "coord_min": -5,
            "coord_max": 5,
            "intercept_min": -5,
            "intercept_max": 5,
        },
        "hard": {
            "allow_vertex_form": True,
            "allow_standard_form": True,
            "allow_factored_form": True,
            "allow_messy_form": True,
            "allow_shift_h": True,
            "allow_shift_k": True,
            "allow_stretch": True,
            "allow_reflection": True,
            "coef_min": -3,
            "coef_max": 3,
            "integer_only": False,
            "leading_coefficient_one": False,
            "monic_only": False,
            "coord_min": -8,
            "coord_max": 8,
            "intercept_min": -8,
            "intercept_max": 8,
        },
    },
    # Solve polynomials by graphing:
    #   easy   — monic (a=1); small integer roots
    #   medium — a ≠ 1 allowed; wider roots; factored prompts ok
    #   hard   — stretch/reflection; optional cubic; wider root range
    "polynomial_solve_graph": {
        "easy": {
            "leading_coefficient_one": True,
            "monic_only": True,
            "allow_stretch": False,
            "allow_reflection": False,
            "allow_factored_form": False,
            "coef_min": 1,
            "coef_max": 1,
            "root_min": -3,
            "root_max": 3,
            "min_degree": 2,
            "max_degree": 2,
            "integer_only": True,
            "coord_min": -5,
            "coord_max": 5,
        },
        "medium": {
            "leading_coefficient_one": False,
            "monic_only": False,
            "allow_stretch": True,
            "allow_reflection": True,
            "allow_factored_form": True,
            "coef_min": -3,
            "coef_max": 3,
            "root_min": -5,
            "root_max": 5,
            "min_degree": 2,
            "max_degree": 2,
            "integer_only": True,
            "coord_min": -8,
            "coord_max": 8,
        },
        "hard": {
            "leading_coefficient_one": False,
            "monic_only": False,
            "allow_stretch": True,
            "allow_reflection": True,
            "allow_factored_form": True,
            "coef_min": -4,
            "coef_max": 4,
            "root_min": -7,
            "root_max": 7,
            "min_degree": 2,
            "max_degree": 3,
            "integer_only": True,
            "coord_min": -10,
            "coord_max": 10,
        },
    },
    # Graphing quadratic inequalities (forms + symbols):
    #   easy   — clean vertex or standard; a=1; < / > only
    #   medium — factored / expand / light messy; a≠1; ≤ ≥ unlocked
    #   hard   — messy rewrite + CTS standard; fractional a
    "quadratic_inequality_graph": {
        "easy": {
            "allow_vertex_form": True,
            "allow_standard_form": True,
            "allow_factored_form": False,
            "allow_messy_form": False,
            "allow_shift_h": True,
            "allow_shift_k": True,
            "allow_stretch": False,
            "allow_reflection": False,
            "coef_min": 1,
            "coef_max": 1,
            "integer_only": True,
            "leading_coefficient_one": True,
            "monic_only": True,
            "coord_min": -3,
            "coord_max": 3,
            "intercept_min": -3,
            "intercept_max": 3,
            "allow_lt": True,
            "allow_gt": True,
            "allow_lte": False,
            "allow_gte": False,
        },
        "medium": {
            "allow_vertex_form": True,
            "allow_standard_form": True,
            "allow_factored_form": True,
            "allow_messy_form": True,
            "allow_shift_h": True,
            "allow_shift_k": True,
            "allow_stretch": True,
            "allow_reflection": True,
            "coef_min": -2,
            "coef_max": 2,
            "integer_only": True,
            "leading_coefficient_one": False,
            "monic_only": False,
            "coord_min": -5,
            "coord_max": 5,
            "intercept_min": -5,
            "intercept_max": 5,
            "allow_lt": True,
            "allow_gt": True,
            "allow_lte": True,
            "allow_gte": True,
        },
        "hard": {
            "allow_vertex_form": True,
            "allow_standard_form": True,
            "allow_factored_form": True,
            "allow_messy_form": True,
            "allow_shift_h": True,
            "allow_shift_k": True,
            "allow_stretch": True,
            "allow_reflection": True,
            "coef_min": -3,
            "coef_max": 3,
            "integer_only": False,
            "leading_coefficient_one": False,
            "monic_only": False,
            "coord_min": -8,
            "coord_max": 8,
            "intercept_min": -8,
            "intercept_max": 8,
            "allow_lt": True,
            "allow_gt": True,
            "allow_lte": True,
            "allow_gte": True,
        },
    },
    "trigonometry": {
        "easy": {"angle_min": 0, "angle_max": 90, "unit_circle_only": True},
        "medium": {"angle_min": 0, "angle_max": 360, "unit_circle_only": True},
        "hard": {"angle_min": 0, "angle_max": 360, "unit_circle_only": False},
    },
    "limits": {
        "easy": {"power_min": 1, "power_max": 2, "allow_infinity": False},
        "medium": {"power_min": 1, "power_max": 3, "allow_infinity": False},
        "hard": {"power_min": 1, "power_max": 4, "allow_infinity": True},
    },
    "derivatives": {
        "easy": {"term_count": 2, "power_max": 3},
        "medium": {"term_count": 3, "power_max": 4},
        "hard": {"term_count": 4, "power_max": 6},
    },
    "integrals": {
        "easy": {"term_count": 1, "power_max": 3, "require_positive_power": True},
        "medium": {"term_count": 2, "power_max": 4, "require_positive_power": True},
        "hard": {"term_count": 3, "power_max": 5, "require_positive_power": False},
    },
    "statistics": {
        "easy": {"data_set_size_min": 4, "data_set_size_max": 8, "value_min": 1, "value_max": 20},
        "medium": {"data_set_size_min": 6, "data_set_size_max": 12, "value_min": 1, "value_max": 40},
        "hard": {"data_set_size_min": 8, "data_set_size_max": 16, "value_min": 1, "value_max": 80},
    },
    "algebra_expression": {
        "easy": {"coef_min": -5, "coef_max": 5, **_COMMON_TERMS["easy"]},
        "medium": {"coef_min": -10, "coef_max": 10, **_COMMON_TERMS["medium"]},
        "hard": {"coef_min": -15, "coef_max": 15, **_COMMON_TERMS["hard"]},
    },
    "number_sets": {
        "easy": {
            "ask_mode": "classify",
            "include_natural": True,
            "include_whole": True,
            "include_integer": True,
            "include_rational": False,
            "include_irrational": False,
            "include_real": False,
            "allow_negative": True,
            "allow_fractions": False,
            "allow_irrationals": False,
            "num_min": -10,
            "num_max": 10,
        },
        "medium": {
            "ask_mode": "mixed",
            "include_natural": True,
            "include_whole": True,
            "include_integer": True,
            "include_rational": True,
            "include_irrational": False,
            "include_real": True,
            "allow_negative": True,
            "allow_fractions": True,
            "allow_irrationals": False,
            "num_min": -12,
            "num_max": 12,
        },
        "hard": {
            "ask_mode": "mixed",
            "include_natural": True,
            "include_whole": True,
            "include_integer": True,
            "include_rational": True,
            "include_irrational": True,
            "include_real": True,
            "allow_negative": True,
            "allow_fractions": True,
            "allow_irrationals": True,
            "num_min": -20,
            "num_max": 20,
        },
    },
    "common_enrichment": dict(_COMMON_TERMS),
}

_CONSECUTIVE_INTEGERS_TIERS: TierPresets = {
    "easy": {
        "difficulty": "easy",
        "min_consecutive_count": 2,
        "max_consecutive_count": 3,
        "allow_consecutive_integers": True,
        "allow_consecutive_even": False,
        "allow_consecutive_odd": False,
        "allow_sum_goal": True,
        "allow_sum_first_last_goal": False,
        "allow_product_goal": False,
    },
    "medium": {
        "difficulty": "medium",
        "min_consecutive_count": 3,
        "max_consecutive_count": 4,
        "allow_consecutive_integers": True,
        "allow_consecutive_even": True,
        "allow_consecutive_odd": True,
        "allow_sum_goal": True,
        "allow_sum_first_last_goal": True,
        "allow_product_goal": False,
    },
    "hard": {
        "difficulty": "hard",
        "min_consecutive_count": 4,
        "max_consecutive_count": 5,
        "allow_consecutive_integers": True,
        "allow_consecutive_even": True,
        "allow_consecutive_odd": True,
        "allow_sum_goal": True,
        "allow_sum_first_last_goal": True,
        "allow_product_goal": True,
    },
}

_DISTANCE_RATE_TIME_TIERS: TierPresets = {
    "easy": {
        "difficulty": "easy",
        "allow_drt_find_missing": True,
        "allow_drt_round_trip": False,
        "allow_drt_two_segments": False,
        "allow_drt_opposite": False,
        "allow_drt_same_direction": False,
        "allow_distance_mi": True,
        "allow_distance_km": True,
        "allow_distance_m": True,
        "allow_distance_ft": True,
        "allow_time_hr": True,
        "allow_time_min": True,
    },
    "medium": {
        "difficulty": "medium",
        "allow_drt_find_missing": True,
        "allow_drt_round_trip": True,
        "allow_drt_two_segments": True,
        "allow_drt_opposite": False,
        "allow_drt_same_direction": False,
        "allow_distance_mi": True,
        "allow_distance_km": True,
        "allow_distance_m": True,
        "allow_distance_ft": True,
        "allow_time_hr": True,
        "allow_time_min": True,
    },
    "hard": {
        "difficulty": "hard",
        "allow_drt_find_missing": False,
        "allow_drt_round_trip": True,
        "allow_drt_two_segments": True,
        "allow_drt_opposite": True,
        "allow_drt_same_direction": True,
        "allow_distance_mi": True,
        "allow_distance_km": True,
        "allow_distance_m": True,
        "allow_distance_ft": True,
        "allow_time_hr": True,
        "allow_time_min": True,
    },
}

_WORK_PROBLEM_TIERS: TierPresets = {
    "easy": {
        "difficulty": "easy",
        "allow_work_together": True,
        "allow_work_find_one_rate": True,
        "allow_work_three": False,
        "allow_work_find_one_time": False,
        "allow_work_starts_later": False,
        "allow_work_pipes": False,
        "allow_work_time_hr": True,
        "allow_work_time_min": True,
    },
    "medium": {
        "difficulty": "medium",
        "allow_work_together": False,
        "allow_work_find_one_rate": False,
        "allow_work_three": True,
        "allow_work_find_one_time": True,
        "allow_work_starts_later": False,
        "allow_work_pipes": False,
        "allow_work_time_hr": True,
        "allow_work_time_min": True,
    },
    "hard": {
        "difficulty": "hard",
        "allow_work_together": False,
        "allow_work_find_one_rate": False,
        "allow_work_three": False,
        "allow_work_find_one_time": False,
        "allow_work_starts_later": True,
        "allow_work_pipes": True,
        "allow_work_time_hr": True,
        "allow_work_time_min": True,
    },
}

# Common-factor generator always uses normal factoring; keep degree 2 so RRT-exclude stays valid.
_FACTORING_COMMON_FACTOR_TIERS: TierPresets = {
    # GCF-only: remaining poly stays expanded; difficulty = GCF shape + degree.
    "easy": {
        "coef_min": -5,
        "coef_max": 5,
        "min_degree": 1,
        "max_degree": 2,
        "leading_coefficient_one": True,
        "monic_only": True,
    },
    "medium": {
        "coef_min": -8,
        "coef_max": 8,
        "min_degree": 2,
        "max_degree": 2,
        "leading_coefficient_one": False,
        "monic_only": False,
    },
    "hard": {
        "coef_min": -12,
        "coef_max": 12,
        "min_degree": 2,
        "max_degree": 3,
        "leading_coefficient_one": False,
        "monic_only": False,
    },
}

# Solving by factoring stays quadratic; mirror monic / non-monic leading-coeff pedagogy.
_FACTORING_EQUATIONS_TIERS: TierPresets = {
    "easy": {
        "coef_min": -5,
        "coef_max": 5,
        "leading_coefficient_one": True,
        "monic_only": True,
        "factor_normal": True,
        "factor_grouping": False,
        "factor_substitution": False,
        "factor_difference_of_squares": False,
        "factor_perfect_square_trinomial": False,
        "factor_difference_of_cubes": False,
        "factor_sum_of_cubes": False,
        "factor_rrt": False,
    },
    "medium": {
        "coef_min": -10,
        "coef_max": 10,
        "leading_coefficient_one": False,
        "monic_only": False,
        "factor_normal": True,
        "factor_grouping": False,
        "factor_substitution": False,
        "factor_difference_of_squares": False,
        "factor_perfect_square_trinomial": False,
        "factor_difference_of_cubes": False,
        "factor_sum_of_cubes": False,
        "factor_rrt": False,
    },
    "hard": {
        "coef_min": -15,
        "coef_max": 15,
        "leading_coefficient_one": False,
        "monic_only": False,
        "factor_normal": True,
        "factor_grouping": False,
        "factor_substitution": False,
        "factor_difference_of_squares": True,
        "factor_perfect_square_trinomial": True,
        "factor_difference_of_cubes": False,
        "factor_sum_of_cubes": False,
        "factor_rrt": False,
    },
}

# Quadratic expressions (catalog topic): stay degree 2 on every tier.
_QUADRATIC_FACTORING_TIERS: TierPresets = {
    "easy": {
        "coef_min": -5,
        "coef_max": 5,
        "min_degree": 2,
        "max_degree": 2,
        "leading_coefficient_one": True,
        "monic_only": True,
        "factor_normal": True,
        "factor_grouping": False,
        "factor_substitution": False,
        "factor_difference_of_squares": False,
        "factor_perfect_square_trinomial": False,
        "factor_difference_of_cubes": False,
        "factor_sum_of_cubes": False,
        "factor_rrt": False,
        "require_gcf": False,
    },
    "medium": {
        "coef_min": -10,
        "coef_max": 10,
        "min_degree": 2,
        "max_degree": 2,
        "leading_coefficient_one": False,
        "monic_only": False,
        "factor_normal": True,
        "factor_grouping": False,
        "factor_substitution": False,
        "factor_difference_of_squares": False,
        "factor_perfect_square_trinomial": False,
        "factor_difference_of_cubes": False,
        "factor_sum_of_cubes": False,
        "factor_rrt": False,
        "require_gcf": False,
    },
    "hard": {
        "coef_min": -15,
        "coef_max": 15,
        "min_degree": 2,
        "max_degree": 2,
        "leading_coefficient_one": False,
        "monic_only": False,
        "factor_normal": True,
        "factor_grouping": False,
        "factor_substitution": False,
        "factor_difference_of_squares": True,
        "factor_perfect_square_trinomial": True,
        "factor_difference_of_cubes": False,
        "factor_sum_of_cubes": False,
        "factor_rrt": False,
        "require_gcf": False,
    },
}

# Factoring by grouping requires cubics (four-term structure).
_FACTORING_GROUPING_TIERS: TierPresets = {
    "easy": {
        "coef_min": -5,
        "coef_max": 5,
        "min_degree": 3,
        "max_degree": 3,
        "leading_coefficient_one": True,
        "monic_only": True,
        "factor_normal": False,
        "factor_grouping": True,
        "factor_substitution": False,
        "factor_difference_of_squares": False,
        "factor_perfect_square_trinomial": False,
        "factor_difference_of_cubes": False,
        "factor_sum_of_cubes": False,
        "factor_rrt": False,
    },
    "medium": {
        "coef_min": -10,
        "coef_max": 10,
        "min_degree": 3,
        "max_degree": 3,
        "leading_coefficient_one": False,
        "monic_only": False,
        "factor_normal": False,
        "factor_grouping": True,
        "factor_substitution": False,
        "factor_difference_of_squares": False,
        "factor_perfect_square_trinomial": False,
        "factor_difference_of_cubes": False,
        "factor_sum_of_cubes": False,
        "factor_rrt": False,
    },
    "hard": {
        "coef_min": -15,
        "coef_max": 15,
        "min_degree": 3,
        "max_degree": 3,
        "leading_coefficient_one": False,
        "monic_only": False,
        "factor_normal": False,
        "factor_grouping": True,
        "factor_substitution": False,
        "factor_difference_of_squares": False,
        "factor_perfect_square_trinomial": False,
        "factor_difference_of_cubes": False,
        "factor_sum_of_cubes": False,
        "factor_rrt": False,
    },
}

# Algebra 1 "solve by graphing" stays quadratic; harder = a≠1 / factored / wider roots.
_QUADRATIC_SOLVE_BY_GRAPH_TIERS: TierPresets = {
    "easy": {
        "leading_coefficient_one": True,
        "monic_only": True,
        "allow_stretch": False,
        "allow_reflection": False,
        "allow_factored_form": False,
        "coef_min": 1,
        "coef_max": 1,
        "root_min": -3,
        "root_max": 3,
        "min_degree": 2,
        "max_degree": 2,
        "integer_only": True,
        "coord_min": -5,
        "coord_max": 5,
    },
    "medium": {
        "leading_coefficient_one": False,
        "monic_only": False,
        "allow_stretch": True,
        "allow_reflection": True,
        "allow_factored_form": True,
        "coef_min": -3,
        "coef_max": 3,
        "root_min": -5,
        "root_max": 5,
        "min_degree": 2,
        "max_degree": 2,
        "integer_only": True,
        "coord_min": -8,
        "coord_max": 8,
    },
    "hard": {
        "leading_coefficient_one": False,
        "monic_only": False,
        "allow_stretch": True,
        "allow_reflection": True,
        "allow_factored_form": True,
        "coef_min": -4,
        "coef_max": 4,
        "root_min": -7,
        "root_max": 7,
        "min_degree": 2,
        "max_degree": 2,
        "integer_only": True,
        "coord_min": -10,
        "coord_max": 10,
    },
}

_POLYNOMIAL_MULTIPLY_SPECIAL_TIERS: TierPresets = {
    "easy": {
        "coef_min": -5,
        "coef_max": 5,
        "leading_coefficient_one": True,
        "monic_only": True,
    },
    "medium": {
        "coef_min": -9,
        "coef_max": 9,
        "leading_coefficient_one": True,
        "monic_only": True,
    },
    "hard": {
        "coef_min": -12,
        "coef_max": 12,
        "leading_coefficient_one": False,
        "monic_only": False,
    },
}

# Optional per-generator / type-id overrides (wins over profile presets).
_EXPONENTIAL_GROWTH_DECAY_TIERS: TierPresets = {
    "easy": {
        "ask_mode": "find_final",
        "allow_growth": True,
        "allow_decay": True,
        "rate_min": 5,
        "rate_max": 10,
        "periods_min": 2,
        "periods_max": 4,
        "discrete_only": True,
        "allow_how_much_more": False,
        "allow_compare": False,
        "allow_threshold": False,
        "allow_half_life": False,
        "allow_fractional_periods": False,
    },
    "medium": {
        "ask_mode": "mixed",
        "allow_growth": True,
        "allow_decay": True,
        "rate_min": 5,
        "rate_max": 20,
        "periods_min": 4,
        "periods_max": 8,
        "discrete_only": True,
        "allow_how_much_more": True,
        "allow_compare": False,
        "allow_threshold": False,
        "allow_half_life": False,
        "allow_fractional_periods": False,
    },
    "hard": {
        "ask_mode": "mixed",
        "allow_growth": True,
        "allow_decay": True,
        "rate_min": 3,
        "rate_max": 25,
        "periods_min": 5,
        "periods_max": 12,
        "discrete_only": True,
        "allow_how_much_more": True,
        "allow_compare": True,
        "allow_threshold": True,
        "allow_half_life": True,
        "allow_fractional_periods": True,
    },
}

_POLYNOMIAL_MULTIPLY_TIERS: TierPresets = {
    "easy": {
        "coef_min": -5,
        "coef_max": 5,
        "min_degree": 1,
        "max_degree": 2,
        "integer_coefficients_only": True,
        "allow_monomial_binomial": True,
        "allow_binomial_binomial": True,
        "allow_trinomial": False,
        "leading_coefficient_one": True,
        "max_factor_terms": 2,
    },
    "medium": {
        "coef_min": -9,
        "coef_max": 9,
        "min_degree": 1,
        "max_degree": 3,
        "integer_coefficients_only": True,
        "allow_monomial_binomial": True,
        "allow_binomial_binomial": True,
        "allow_trinomial": True,
        "leading_coefficient_one": False,
        "max_factor_terms": 3,
    },
    "hard": {
        "coef_min": -12,
        "coef_max": 12,
        "min_degree": 2,
        "max_degree": 5,
        "integer_coefficients_only": True,
        "allow_monomial_binomial": True,
        "allow_binomial_binomial": True,
        "allow_trinomial": True,
        "leading_coefficient_one": False,
        "max_factor_terms": 5,
    },
}

_SPECIAL_FACTORING_TIERS: TierPresets = {
    "easy": {
        "coef_min": -5,
        "coef_max": 5,
        "factor_difference_of_squares": True,
        "factor_perfect_square_trinomial": True,
        "factor_difference_of_cubes": False,
        "factor_sum_of_cubes": False,
        "allow_higher_even_powers": False,
        "max_even_power": 4,
        "require_gcf": False,
        "leading_coefficient_one": True,
    },
    "medium": {
        "coef_min": -10,
        "coef_max": 10,
        "factor_difference_of_squares": True,
        "factor_perfect_square_trinomial": True,
        "factor_difference_of_cubes": True,
        "factor_sum_of_cubes": True,
        "allow_higher_even_powers": False,
        "max_even_power": 4,
        "require_gcf": False,
        "leading_coefficient_one": False,
    },
    "hard": {
        "coef_min": -12,
        "coef_max": 12,
        "factor_difference_of_squares": True,
        "factor_perfect_square_trinomial": True,
        "factor_difference_of_cubes": True,
        "factor_sum_of_cubes": True,
        "allow_higher_even_powers": True,
        "max_even_power": 8,
        "require_gcf": False,
        "leading_coefficient_one": False,
    },
}

GENERATOR_DIFFICULTY_PRESETS: dict[str, TierPresets] = {
    # Algebra 1 finding_angles: geometry relationships only (no inverse trig).
    # easy   — numeric complementary / supplementary / vertical / adjacent
    # medium — algebraic complementary / supplementary / vertical
    # hard   — triangle angle-sum / multi-step with algebra
    "finding_angles": {
        "easy": {
            "angle_min": 20,
            "angle_max": 120,
            "coef_min": -3,
            "coef_max": 3,
        },
        "medium": {
            "angle_min": 15,
            "angle_max": 160,
            "coef_min": -5,
            "coef_max": 5,
        },
        "hard": {
            "angle_min": 10,
            "angle_max": 170,
            "coef_min": -6,
            "coef_max": 6,
        },
    },
    "rational_simplification": {
        # Always built from linear factors (then expanded).
        # easy   — GCF / obvious linear cancel
        # medium — difference of squares / easy trinomials
        # hard   — higher degree, more canceling; still factorable
        "easy": {
            "coef_min": -5,
            "coef_max": 5,
            "numerator_degree_min": 1,
            "numerator_degree_max": 2,
            "denominator_degree_min": 1,
            "denominator_degree_max": 2,
            "leading_coefficient_one": True,
            "monic_only": True,
            "allow_constant_gcf": True,
            "prefer_difference_of_squares": False,
            "max_cancel_factors": 1,
        },
        "medium": {
            "coef_min": -8,
            "coef_max": 8,
            "numerator_degree_min": 2,
            "numerator_degree_max": 3,
            "denominator_degree_min": 2,
            "denominator_degree_max": 3,
            "leading_coefficient_one": True,
            "monic_only": True,
            "allow_constant_gcf": False,
            "prefer_difference_of_squares": True,
            "max_cancel_factors": 1,
        },
        "hard": {
            "coef_min": -9,
            "coef_max": 9,
            "numerator_degree_min": 3,
            "numerator_degree_max": 4,
            "denominator_degree_min": 2,
            "denominator_degree_max": 4,
            "leading_coefficient_one": False,
            "monic_only": False,
            "allow_constant_gcf": False,
            "prefer_difference_of_squares": True,
            "max_cancel_factors": 2,
        },
    },
    "polynomial_factoring_special_cases": dict(_SPECIAL_FACTORING_TIERS),
    "consecutive_integers_word_problems": dict(_CONSECUTIVE_INTEGERS_TIERS),
    "wp_consecutive_integers": dict(_CONSECUTIVE_INTEGERS_TIERS),
    "distance_rate_time_word_problems": dict(_DISTANCE_RATE_TIME_TIERS),
    "wp_distance_rate_time": dict(_DISTANCE_RATE_TIME_TIERS),
    "a2_equations_and_inequalities_distance_rate_time_word_problems": dict(
        _DISTANCE_RATE_TIME_TIERS
    ),
    "work_word_problems": dict(_WORK_PROBLEM_TIERS),
    "wp_work": dict(_WORK_PROBLEM_TIERS),
    "a2_equations_and_inequalities_work_word_problems": dict(_WORK_PROBLEM_TIERS),
    "polynomial_factoring_common_factor": dict(_FACTORING_COMMON_FACTOR_TIERS),
    "quadratic_factoring": dict(_QUADRATIC_FACTORING_TIERS),
    "polynomial_factoring_grouping": dict(_FACTORING_GROUPING_TIERS),
    "a2_polynomial_functions_factoring_by_grouping": dict(_FACTORING_GROUPING_TIERS),
    "polynomial_multiply_special": dict(_POLYNOMIAL_MULTIPLY_SPECIAL_TIERS),
    "quadratic_factoring_equations": dict(_FACTORING_EQUATIONS_TIERS),
    "a2_quadratic_functions_and_inequalities_solving_equations_by_factoring": dict(
        _FACTORING_EQUATIONS_TIERS
    ),
    # Adding/subtracting rational expressions:
    #   easy   — exactly 2 terms; LCD is a single monomial/binomial
    #   medium — unlike non-monic binomials (2 terms) OR monic 3-term
    #   hard   — multi-factor LCDs, optional cancel/inflation, more terms
    "rational_expression_simplification": {
        "easy": {
            "coef_min": -4,
            "coef_max": 4,
            "term_count": 2,
            "denominator_degree_min": 1,
            "denominator_degree_max": 1,
            "leading_coefficient_one": True,
            "monic_only": True,
            "add_subtract_structure": "shared_lcd",
            "max_lcd_factors": 1,
            "prefer_simple_factors": True,
            "content_primitive_denominators": True,
            "allow_polynomial_terms": False,
            "allow_full_lcd_terms": False,
            "inflation_chance": 0,
            "cancel_factor_count": "0",
            "factor_rrt": False,
            "force_lcd": False,
        },
        "medium": {
            "coef_min": -5,
            "coef_max": 5,
            "term_count": 3,
            "denominator_degree_min": 1,
            "denominator_degree_max": 1,
            "leading_coefficient_one": False,
            "monic_only": False,
            "add_subtract_structure": "auto",
            "max_lcd_factors": 2,
            "prefer_simple_factors": True,
            "content_primitive_denominators": True,
            "allow_polynomial_terms": False,
            "allow_full_lcd_terms": False,
            "inflation_chance": 0,
            "cancel_factor_count": "0",
            "factor_rrt": False,
            "force_lcd": False,
        },
        "hard": {
            "coef_min": -5,
            "coef_max": 5,
            "term_count": 3,
            "denominator_degree_min": 1,
            "denominator_degree_max": 2,
            "leading_coefficient_one": False,
            "monic_only": False,
            "add_subtract_structure": "complex",
            "max_lcd_factors": 3,
            "prefer_simple_factors": True,
            "content_primitive_denominators": True,
            "allow_polynomial_terms": True,
            "allow_full_lcd_terms": True,
            "inflation_chance": 15,
            "cancel_factor_count": "random",
            "factor_rrt": False,
            "force_lcd": False,
        },
    },
    "quadratic_square_roots": {
        # easy   — monic isolated squares only (x² = k / simple (x±h)²)
        # medium — vertex form; a may be ≠ 1
        # hard   — messy vertex (a≠1) and/or complete-the-square first
        "easy": {
            "coef_min": -5,
            "coef_max": 5,
            "integer_only": True,
            "leading_coefficient_one": True,
            "monic_only": True,
            "allow_isolated": True,
            "allow_vertex": False,
            "allow_complete_square": False,
        },
        "medium": {
            "coef_min": -8,
            "coef_max": 8,
            "integer_only": True,
            "leading_coefficient_one": False,
            "monic_only": False,
            "allow_isolated": False,
            "allow_vertex": True,
            "allow_complete_square": False,
        },
        "hard": {
            "coef_min": -12,
            "coef_max": 12,
            "integer_only": False,
            "leading_coefficient_one": False,
            "monic_only": False,
            "allow_isolated": False,
            "allow_vertex": True,
            "allow_complete_square": True,
        },
    },
    "exponential_growth_decay": dict(_EXPONENTIAL_GROWTH_DECAY_TIERS),
    "a2_exponential_and_logarithmic_expressions_discrete_exponential_growth_and_decay_word_problems": dict(
        _EXPONENTIAL_GROWTH_DECAY_TIERS
    ),
    "discrete_exponential_growth_and_decay_word_problems": dict(_EXPONENTIAL_GROWTH_DECAY_TIERS),
    "polynomial_multiply": dict(_POLYNOMIAL_MULTIPLY_TIERS),
    "pa_polynomials_multiplying": dict(_POLYNOMIAL_MULTIPLY_TIERS),
    "a2_polynomial_functions_multiplying": dict(_POLYNOMIAL_MULTIPLY_TIERS),
    "more_on_slope": {
        "easy": {
            "ask_mode": "mixed",
            "allow_from_points": True,
            "allow_from_equation": True,
            "allow_from_graph": True,
            "allow_find_equation": False,
            "allow_classify": True,
            "allow_parallel_perpendicular": False,
            "show_points": False,
            "slope_min": -3,
            "slope_max": 3,
            "intercept_min": -5,
            "intercept_max": 5,
            "coord_min": -5,
            "coord_max": 5,
        },
        "medium": {
            "ask_mode": "mixed",
            "allow_from_points": True,
            "allow_from_equation": True,
            "allow_from_graph": True,
            "allow_find_equation": True,
            "allow_classify": True,
            "allow_parallel_perpendicular": True,
            "show_points": False,
            "slope_min": -6,
            "slope_max": 6,
            "intercept_min": -8,
            "intercept_max": 8,
            "coord_min": -8,
            "coord_max": 8,
        },
        "hard": {
            "ask_mode": "mixed",
            "allow_from_points": True,
            "allow_from_equation": True,
            "allow_from_graph": True,
            "allow_find_equation": True,
            "allow_classify": True,
            "allow_parallel_perpendicular": True,
            "show_points": False,
            "slope_min": -10,
            "slope_max": 10,
            "intercept_min": -12,
            "intercept_max": 12,
            "coord_min": -12,
            "coord_max": 12,
        },
    },
    "absolute_value_equations": {
        "easy": {
            "coef_min": -5,
            "coef_max": 5,
            "integer_only": True,
            "allow_basic": True,
            "allow_isolated_right": True,
            "allow_simple": True,
            "allow_abs_plus_constant": False,
            "allow_factored_inside": False,
            "allow_coeff_outside": False,
            "allow_abs_equals_abs": False,
            "allow_abs_equals_linear": False,
        },
        "medium": {
            "coef_min": -12,
            "coef_max": 12,
            "integer_only": True,
            "allow_basic": False,
            "allow_isolated_right": False,
            "allow_simple": False,
            "allow_abs_plus_constant": True,
            "allow_factored_inside": True,
            "allow_coeff_outside": False,
            "allow_abs_equals_abs": False,
            "allow_abs_equals_linear": False,
        },
        "hard": {
            "coef_min": -20,
            "coef_max": 20,
            "integer_only": False,
            "allow_basic": False,
            "allow_isolated_right": False,
            "allow_simple": False,
            "allow_abs_plus_constant": False,
            "allow_factored_inside": False,
            "allow_coeff_outside": True,
            "allow_abs_equals_abs": True,
            "allow_abs_equals_linear": True,
        },
    },
    "absolute_value_inequalities": {
        "easy": {
            "coef_min": -5,
            "coef_max": 5,
            "integer_only": True,
            "allow_simple": True,
            "allow_shifted": True,
            "allow_linear": False,
            "allow_abs_plus_constant": False,
            "allow_abs_vs_linear": False,
            "allow_lt": True,
            "allow_gt": True,
            "allow_lte": False,
            "allow_gte": False,
        },
        "medium": {
            "coef_min": -12,
            "coef_max": 12,
            "integer_only": True,
            "allow_simple": False,
            "allow_shifted": False,
            "allow_linear": True,
            "allow_abs_plus_constant": False,
            "allow_abs_vs_linear": False,
            "allow_lt": True,
            "allow_gt": True,
            "allow_lte": True,
            "allow_gte": True,
        },
        "hard": {
            "coef_min": -20,
            "coef_max": 20,
            "integer_only": False,
            "allow_simple": False,
            "allow_shifted": False,
            "allow_linear": True,
            "allow_abs_plus_constant": True,
            "allow_abs_vs_linear": True,
            "allow_lt": True,
            "allow_gt": True,
            "allow_lte": True,
            "allow_gte": True,
        },
    },
    # Adding/subtracting radicals:
    #   easy   — already-simplified like radicals (2√3 + 5√3)
    #   medium — light simplify first (√12 + √3, √18 − √8)
    #   hard   — coefficients + larger perfect squares / more terms
    "radical_add_subtract": {
        "easy": {
            "allow_like_radicals": True,
            "allow_unsimplified_radicals": False,
            "allow_coeff_unsimplified": False,
            "coef_min": 1,
            "coef_max": 6,
            "min_terms": 2,
            "max_terms": 2,
        },
        "medium": {
            "allow_like_radicals": False,
            "allow_unsimplified_radicals": True,
            "allow_coeff_unsimplified": False,
            "coef_min": 1,
            "coef_max": 1,
            "min_terms": 2,
            "max_terms": 2,
        },
        "hard": {
            "allow_like_radicals": False,
            "allow_unsimplified_radicals": False,
            "allow_coeff_unsimplified": True,
            "coef_min": 1,
            "coef_max": 8,
            "min_terms": 3,
            "max_terms": 4,
        },
    },
    # Dividing radicals:
    #   easy   — already-reduced quotients (√12/√3, 6√5/2√5)
    #   medium — simplify perfect squares / cancel after rewriting
    #   hard   — rationalize denominator + multi-factor coeffs
    "radical_divide": {
        "easy": {
            "allow_reduced_quotients": True,
            "allow_simplify_quotients": False,
            "allow_rationalize_divide": False,
            "coef_min": 1,
            "coef_max": 6,
        },
        "medium": {
            "allow_reduced_quotients": False,
            "allow_simplify_quotients": True,
            "allow_rationalize_divide": False,
            "coef_min": 1,
            "coef_max": 3,
        },
        "hard": {
            "allow_reduced_quotients": False,
            "allow_simplify_quotients": False,
            "allow_rationalize_divide": True,
            "coef_min": 1,
            "coef_max": 8,
        },
    },
    # Multiplying radicals:
    #   easy   — √a · √b
    #   medium — k√a · m√b
    #   hard   — binomial FOIL (p√a ± q√b)(…)
    "radical_multiply": {
        "easy": {
            "allow_simple_product": True,
            "allow_coeff_product": False,
            "allow_binomial_product": False,
            "coef_min": 1,
            "coef_max": 4,
        },
        "medium": {
            "allow_simple_product": False,
            "allow_coeff_product": True,
            "allow_binomial_product": False,
            "coef_min": 1,
            "coef_max": 6,
        },
        "hard": {
            "allow_simple_product": False,
            "allow_coeff_product": False,
            "allow_binomial_product": True,
            "coef_min": 1,
            "coef_max": 5,
        },
    },
    # Simplifying single radicals by radicand size / structure.
    "radical_simplification": {
        "easy": {
            "radicand_min": 12,
            "radicand_max": 96,
            "require_simplifiable": True,
            "radical_index": 2,
        },
        "medium": {
            "radicand_min": 48,
            "radicand_max": 200,
            "require_simplifiable": True,
            "radical_index": 2,
        },
        "hard": {
            "radicand_min": 100,
            "radicand_max": 400,
            "require_simplifiable": True,
            "radical_index": 2,
        },
    },
    # Complex fractions:
    #   easy   — monomial dens / simple stacked forms
    #   medium — (a/x + b)/(c/x + d)
    #   hard   — unlike linear dens in a stacked fraction
    "complex_fractions": {
        "easy": {"coef_min": -5, "coef_max": 5, "difficulty_tier": "easy"},
        "medium": {"coef_min": -8, "coef_max": 8, "difficulty_tier": "medium"},
        "hard": {"coef_min": -10, "coef_max": 10, "difficulty_tier": "hard"},
    },
    # Rational expression multiply / divide:
    #   easy   — monic linears, one cancel, ÷ only for division
    #   medium — non-monic, 1–2 cancels, ÷ or slash
    #   hard   — expanded polys, 2 cancels, 3 factors, ÷ or complex fraction
    "rational_expression_multiply_divide": {
        "easy": {
            "coef_min": -4,
            "coef_max": 4,
            "allow_multiply": True,
            "allow_divide": True,
            "cancel_factor_count": 1,
            "max_factor_degree": 1,
            "expand_polynomials": False,
            "operand_count": 2,
            "leading_coefficient_one": True,
            "allow_obelus": True,
            "allow_complex_fraction": False,
            "allow_slash": False,
        },
        "medium": {
            "coef_min": -8,
            "coef_max": 8,
            "allow_multiply": True,
            "allow_divide": True,
            "cancel_factor_count": 2,
            "max_factor_degree": 1,
            "expand_polynomials": False,
            "operand_count": 2,
            "leading_coefficient_one": False,
            "allow_obelus": True,
            "allow_complex_fraction": False,
            "allow_slash": True,
        },
        "hard": {
            "coef_min": -10,
            "coef_max": 10,
            "allow_multiply": True,
            "allow_divide": True,
            "cancel_factor_count": 2,
            "max_factor_degree": 2,
            "expand_polynomials": True,
            "operand_count": 3,
            "leading_coefficient_one": False,
            "allow_obelus": True,
            "allow_complex_fraction": True,
            "allow_slash": False,
        },
    },
    # Radical equations:
    #   easy   — single radical; move/divide then square; occasional extraneous check
    #   medium — more algebra to isolate; √ = linear with checking
    #   hard   — two radicals (square more than once); nestier; designed extraneous
    "radical_equations": {
        "easy": {
            "coef_min": -6,
            "coef_max": 6,
            "integer_only": True,
            "allow_light_prep": True,
            "allow_isolate_algebra": False,
            "allow_radical_equals_linear": False,
            "allow_two_radicals": False,
        },
        "medium": {
            "coef_min": -10,
            "coef_max": 10,
            "integer_only": True,
            "allow_light_prep": False,
            "allow_isolate_algebra": True,
            "allow_radical_equals_linear": True,
            "allow_two_radicals": False,
        },
        "hard": {
            "coef_min": -12,
            "coef_max": 12,
            "integer_only": True,
            "allow_light_prep": False,
            "allow_isolate_algebra": False,
            "allow_radical_equals_linear": True,
            "allow_two_radicals": True,
        },
    },
    # Rational equations:
    #   easy   — single fraction = constant (or simple proportion)
    #   medium — proportions + fraction plus constant
    #   hard   — two rational terms (LCD; extraneous checks)
    "rational_equations": {
        "easy": {
            "coef_min": -6,
            "coef_max": 6,
            "integer_only": True,
            "allow_simple_fraction": True,
            "allow_proportion": True,
            "allow_fraction_plus_constant": False,
            "allow_two_fractions": False,
        },
        "medium": {
            "coef_min": -10,
            "coef_max": 10,
            "integer_only": True,
            "allow_simple_fraction": False,
            "allow_proportion": True,
            "allow_fraction_plus_constant": True,
            "allow_two_fractions": False,
        },
        "hard": {
            "coef_min": -12,
            "coef_max": 12,
            "integer_only": True,
            "allow_simple_fraction": False,
            "allow_proportion": False,
            "allow_fraction_plus_constant": False,
            "allow_two_fractions": True,
        },
    },
}
_ABS_EQ_TIERS = GENERATOR_DIFFICULTY_PRESETS["absolute_value_equations"]
GENERATOR_DIFFICULTY_PRESETS["a2_equations_and_inequalities_absolute_value_equations"] = dict(
    _ABS_EQ_TIERS
)
_ABS_INEQ_TIERS = GENERATOR_DIFFICULTY_PRESETS["absolute_value_inequalities"]
GENERATOR_DIFFICULTY_PRESETS["a2_equations_and_inequalities_absolute_value_inequalities"] = dict(
    _ABS_INEQ_TIERS
)
_SQUARE_ROOT_TIERS = GENERATOR_DIFFICULTY_PRESETS["quadratic_square_roots"]
GENERATOR_DIFFICULTY_PRESETS[
    "a2_quadratic_functions_and_inequalities_solving_equations_by_taking_square_roots"
] = dict(_SQUARE_ROOT_TIERS)
GENERATOR_DIFFICULTY_PRESETS["solving_equations_by_taking_square_roots"] = dict(_SQUARE_ROOT_TIERS)
_SPECIAL_FACT_TIERS = GENERATOR_DIFFICULTY_PRESETS["polynomial_factoring_special_cases"]
GENERATOR_DIFFICULTY_PRESETS["a2_polynomial_functions_factoring_sum_difference_of_cubes"] = dict(
    _SPECIAL_FACT_TIERS
)
GENERATOR_DIFFICULTY_PRESETS[
    "a2_quadratic_functions_and_inequalities_factoring_special_case_quadratic_expressions"
] = dict(_SPECIAL_FACT_TIERS)
GENERATOR_DIFFICULTY_PRESETS["a2_polynomial_functions_conjugate_roots_and_factoring"] = dict(
    _SPECIAL_FACT_TIERS
)
_SOLVE_BY_GRAPH_TIERS = PROFILE_DIFFICULTY_PRESETS["polynomial_solve_graph"]
GENERATOR_DIFFICULTY_PRESETS["solve_polynomial_by_graphing"] = dict(_SOLVE_BY_GRAPH_TIERS)
GENERATOR_DIFFICULTY_PRESETS["quadratic_solve_by_graphing"] = dict(_QUADRATIC_SOLVE_BY_GRAPH_TIERS)
GENERATOR_DIFFICULTY_PRESETS[
    "a2_quadratic_functions_and_inequalities_solving_equations_by_graphing"
] = dict(_QUADRATIC_SOLVE_BY_GRAPH_TIERS)
_RADICAL_ADD_SUB_TIERS = GENERATOR_DIFFICULTY_PRESETS["radical_add_subtract"]
GENERATOR_DIFFICULTY_PRESETS[
    "a2_radical_functions_and_rational_exponents_adding_and_subtracting_radical_expressions"
] = dict(_RADICAL_ADD_SUB_TIERS)
GENERATOR_DIFFICULTY_PRESETS["geo_review_adding_and_subtracting_square_roots"] = dict(
    _RADICAL_ADD_SUB_TIERS
)
_RADICAL_DIVIDE_TIERS = GENERATOR_DIFFICULTY_PRESETS["radical_divide"]
GENERATOR_DIFFICULTY_PRESETS[
    "a2_radical_functions_and_rational_exponents_dividing_radical_expressions"
] = dict(_RADICAL_DIVIDE_TIERS)
GENERATOR_DIFFICULTY_PRESETS["geo_review_dividing_square_roots"] = dict(_RADICAL_DIVIDE_TIERS)
_RADICAL_MULTIPLY_TIERS = GENERATOR_DIFFICULTY_PRESETS["radical_multiply"]
GENERATOR_DIFFICULTY_PRESETS[
    "a2_radical_functions_and_rational_exponents_multiplying_radical_expressions"
] = dict(_RADICAL_MULTIPLY_TIERS)
GENERATOR_DIFFICULTY_PRESETS["geo_review_multiplying_square_roots"] = dict(
    _RADICAL_MULTIPLY_TIERS
)
_RADICAL_SIMP_TIERS = GENERATOR_DIFFICULTY_PRESETS["radical_simplification"]
GENERATOR_DIFFICULTY_PRESETS[
    "a2_radical_functions_and_rational_exponents_simplifying_radicals"
] = dict(_RADICAL_SIMP_TIERS)
_COMPLEX_FRAC_TIERS = GENERATOR_DIFFICULTY_PRESETS["complex_fractions"]
GENERATOR_DIFFICULTY_PRESETS["a2_rational_expressions_complex_fractions"] = dict(
    _COMPLEX_FRAC_TIERS
)
_RATIONAL_MD_TIERS = GENERATOR_DIFFICULTY_PRESETS["rational_expression_multiply_divide"]
GENERATOR_DIFFICULTY_PRESETS["a2_rational_expressions_multiplying_and_dividing"] = dict(
    _RATIONAL_MD_TIERS
)
GENERATOR_DIFFICULTY_PRESETS["rational_expressions_multiplying_and_dividing"] = dict(
    _RATIONAL_MD_TIERS
)
_RATIONAL_ADD_SUB_TIERS = GENERATOR_DIFFICULTY_PRESETS["rational_expression_simplification"]
GENERATOR_DIFFICULTY_PRESETS["a2_rational_expressions_adding_and_subtracting"] = dict(
    _RATIONAL_ADD_SUB_TIERS
)
GENERATOR_DIFFICULTY_PRESETS["rational_expressions_adding_and_subtracting"] = dict(
    _RATIONAL_ADD_SUB_TIERS
)
_RATIONAL_SIMP_TIERS = GENERATOR_DIFFICULTY_PRESETS["rational_simplification"]
GENERATOR_DIFFICULTY_PRESETS["a2_rational_expressions_simplifying"] = dict(
    _RATIONAL_SIMP_TIERS
)
GENERATOR_DIFFICULTY_PRESETS["rational_expressions_simplifying"] = dict(
    _RATIONAL_SIMP_TIERS
)
_RADICAL_EQ_TIERS = GENERATOR_DIFFICULTY_PRESETS["radical_equations"]
GENERATOR_DIFFICULTY_PRESETS[
    "a2_radical_functions_and_rational_exponents_radical_equations"
] = dict(_RADICAL_EQ_TIERS)
GENERATOR_DIFFICULTY_PRESETS[
    "a2_radical_functions_and_rational_exponents_rational_exponent_equations"
] = dict(_RADICAL_EQ_TIERS)
_RATIONAL_EQ_TIERS = GENERATOR_DIFFICULTY_PRESETS["rational_equations"]
GENERATOR_DIFFICULTY_PRESETS["rational_expressions_equations"] = dict(_RATIONAL_EQ_TIERS)
GENERATOR_DIFFICULTY_PRESETS["a2_rational_expressions_equations"] = dict(_RATIONAL_EQ_TIERS)
GENERATOR_DIFFICULTY_PRESETS["pc_rational_equations"] = dict(_RATIONAL_EQ_TIERS)

# --- Course-tiered overrides (same generator, different type_id hardness) ---
# Geometry review radicals: stay on square roots / lighter structures than A2.
_GEO_REVIEW_RAD_ADD = {
    "easy": {
        "allow_like_radicals": True,
        "allow_unsimplified_radicals": False,
        "allow_coeff_unsimplified": False,
        "coef_min": 1,
        "coef_max": 4,
        "min_terms": 2,
        "max_terms": 2,
    },
    "medium": {
        "allow_like_radicals": False,
        "allow_unsimplified_radicals": True,
        "allow_coeff_unsimplified": False,
        "coef_min": 1,
        "coef_max": 1,
        "min_terms": 2,
        "max_terms": 2,
    },
    "hard": {
        "allow_like_radicals": False,
        "allow_unsimplified_radicals": False,
        "allow_coeff_unsimplified": True,
        "coef_min": 1,
        "coef_max": 5,
        "min_terms": 2,
        "max_terms": 3,
    },
}
GENERATOR_DIFFICULTY_PRESETS["geo_review_adding_and_subtracting_square_roots"] = _GEO_REVIEW_RAD_ADD
GENERATOR_DIFFICULTY_PRESETS["geo_review_multiplying_square_roots"] = {
    "easy": {
        "allow_simple_product": True,
        "allow_coeff_product": False,
        "allow_binomial_product": False,
        "coef_min": 1,
        "coef_max": 3,
    },
    "medium": {
        "allow_simple_product": False,
        "allow_coeff_product": True,
        "allow_binomial_product": False,
        "coef_min": 1,
        "coef_max": 4,
    },
    "hard": {
        "allow_simple_product": False,
        "allow_coeff_product": True,
        "allow_binomial_product": False,
        "coef_min": 1,
        "coef_max": 6,
    },
}
GENERATOR_DIFFICULTY_PRESETS["geo_review_dividing_square_roots"] = {
    "easy": {
        "allow_reduced_quotients": True,
        "allow_simplify_quotients": False,
        "allow_rationalize_divide": False,
        "coef_min": 1,
        "coef_max": 4,
    },
    "medium": {
        "allow_reduced_quotients": False,
        "allow_simplify_quotients": True,
        "allow_rationalize_divide": False,
        "coef_min": 1,
        "coef_max": 3,
    },
    "hard": {
        "allow_reduced_quotients": False,
        "allow_simplify_quotients": True,
        "allow_rationalize_divide": False,
        "coef_min": 1,
        "coef_max": 5,
    },
}
GENERATOR_DIFFICULTY_PRESETS["geo_review_simplifying_square_roots"] = {
    "easy": {
        "radicand_min": 8,
        "radicand_max": 50,
        "require_simplifiable": True,
        "radical_index": 2,
    },
    "medium": {
        "radicand_min": 18,
        "radicand_max": 120,
        "require_simplifiable": True,
        "radical_index": 2,
    },
    "hard": {
        "radicand_min": 48,
        "radicand_max": 200,
        "require_simplifiable": True,
        "radical_index": 2,
    },
}

# A2 radicals: slightly wider than A1 base presets.
_A2_RAD_ADD = {
    tier: {**vals, "coef_max": int(vals.get("coef_max", 6)) + 2}
    for tier, vals in GENERATOR_DIFFICULTY_PRESETS["radical_add_subtract"].items()
}
GENERATOR_DIFFICULTY_PRESETS[
    "a2_radical_functions_and_rational_exponents_adding_and_subtracting_radical_expressions"
] = _A2_RAD_ADD
_A2_RAD_SIMP = {
    "easy": {
        "radicand_min": 18,
        "radicand_max": 120,
        "require_simplifiable": True,
        "radical_index": 2,
    },
    "medium": {
        "radicand_min": 50,
        "radicand_max": 250,
        "require_simplifiable": True,
        "radical_index": 2,
    },
    "hard": {
        "radicand_min": 120,
        "radicand_max": 500,
        "require_simplifiable": True,
        "radical_index": 2,
    },
}
GENERATOR_DIFFICULTY_PRESETS[
    "a2_radical_functions_and_rational_exponents_simplifying_radicals"
] = _A2_RAD_SIMP

# Grade 6 / Pre-Algebra softer shared skills
GENERATOR_DIFFICULTY_PRESETS["g6_numeric_expressions_and_order_of_operations"] = {
    "easy": {"pemdas_complexity": "basic", "num_min": 1, "num_max": 5},
    "medium": {"pemdas_complexity": "basic", "num_min": 2, "num_max": 8},
    "hard": {"pemdas_complexity": "mixed", "num_min": 2, "num_max": 9},
}
_DECIMAL_MULTIPLICATION_TIERS = {
    "easy": {
        "whole_times_decimal": True,
        "decimal_places": 1,
        "max_decimal_places": 1,
        "allow_negative": False,
    },
    "medium": {
        "whole_times_decimal": False,
        "decimal_places": 2,
        "max_decimal_places": 2,
        "allow_negative": False,
    },
    "hard": {
        "whole_times_decimal": False,
        "decimal_places": 3,
        "max_decimal_places": 3,
        "allow_negative": False,
    },
}
GENERATOR_DIFFICULTY_PRESETS["g6_decimal_multiplication"] = dict(_DECIMAL_MULTIPLICATION_TIERS)
GENERATOR_DIFFICULTY_PRESETS["g6_decimal_multiplication_with_equivalent_fractions"] = dict(
    _DECIMAL_MULTIPLICATION_TIERS
)
GENERATOR_DIFFICULTY_PRESETS["g6_decimal_multiplication_with_area_diagrams"] = dict(
    _DECIMAL_MULTIPLICATION_TIERS
)
_WHOLE_DIVIDE_TO_DECIMAL_TIERS = {
    "easy": {
        "decimal_places": 1,
        "max_decimal_places": 1,
        "allow_negative": False,
        "num_min": 1,
        "num_max": 20,
    },
    "medium": {
        "decimal_places": 2,
        "max_decimal_places": 2,
        "allow_negative": False,
        "num_min": 1,
        "num_max": 50,
    },
    "hard": {
        "decimal_places": 3,
        "max_decimal_places": 3,
        "allow_negative": False,
        "num_min": 1,
        "num_max": 200,
    },
}
GENERATOR_DIFFICULTY_PRESETS["g6_dividing_whole_numbers_that_result_in_decimals"] = dict(
    _WHOLE_DIVIDE_TO_DECIMAL_TIERS
)
GENERATOR_DIFFICULTY_PRESETS["g6_distributive_property_numeric"] = {
    "easy": {"coef_min": 2, "coef_max": 5, "allow_negative": False},
    "medium": {"coef_min": 2, "coef_max": 9, "allow_negative": False},
    "hard": {"coef_min": 2, "coef_max": 12, "allow_negative": False},
}
GENERATOR_DIFFICULTY_PRESETS["g6_distributive_property_algebraic"] = {
    "easy": {"coef_min": 2, "coef_max": 5, "allow_negative": False},
    "medium": {"coef_min": 2, "coef_max": 8, "allow_negative": False},
    "hard": {"coef_min": -5, "coef_max": 9, "allow_negative": True},
}
GENERATOR_DIFFICULTY_PRESETS["distributive_property_algebraic"] = dict(
    GENERATOR_DIFFICULTY_PRESETS["g6_distributive_property_algebraic"]
)
GENERATOR_DIFFICULTY_PRESETS["g6_distances_on_the_coordinate_plane"] = {
    "easy": {
        "coord_min": -5,
        "coord_max": 5,
        "integer_coordinates": True,
        "axis_aligned_only": True,
    },
    "medium": {
        "coord_min": -8,
        "coord_max": 8,
        "integer_coordinates": True,
        "axis_aligned_only": True,
    },
    "hard": {
        "coord_min": -10,
        "coord_max": 10,
        "integer_coordinates": True,
        "axis_aligned_only": True,
    },
}
# Fraction multiply: small proper → improper/mixed → large mixed.
_FRACTION_MULTIPLY_TIERS: TierPresets = {
    "easy": {
        "num_min": 1,
        "num_max": 5,
        "denom_min": 2,
        "denom_max": 6,
        "coef_min": 1,
        "coef_max": 5,
        "allow_negative": False,
        "allow_mixed": False,
        "require_proper": True,
    },
    "medium": {
        "num_min": 1,
        "num_max": 12,
        "denom_min": 2,
        "denom_max": 12,
        "coef_min": 1,
        "coef_max": 12,
        "allow_negative": False,
        "allow_mixed": True,
        "require_proper": False,
    },
    "hard": {
        "num_min": 5,
        "num_max": 50,
        "denom_min": 8,
        "denom_max": 50,
        "coef_min": 5,
        "coef_max": 50,
        "allow_negative": False,
        "allow_mixed": True,
        "require_proper": False,
    },
}
GENERATOR_DIFFICULTY_PRESETS["g6_fraction_multiply"] = dict(_FRACTION_MULTIPLY_TIERS)
GENERATOR_DIFFICULTY_PRESETS["rational_multiply"] = dict(_FRACTION_MULTIPLY_TIERS)
# Fraction division word problems (how many groups / how much in each):
# easy  — whole ÷ whole → whole
# medium — whole ÷ (whole or fraction); answer often non-whole
# hard  — non-whole ÷ non-whole (fractions / mixed)
_FRACTION_DIVIDE_WORD_TIERS: TierPresets = {
    "easy": {
        "num_min": 2,
        "num_max": 12,
        "denom_min": 2,
        "denom_max": 6,
        "coef_min": 2,
        "coef_max": 12,
        "allow_negative": False,
        "allow_mixed": False,
        "require_proper": False,
        "dividend_form": "whole",
        "divisor_form": "whole",
        "require_whole_quotient": True,
        "require_non_whole_quotient": False,
    },
    "medium": {
        "num_min": 1,
        "num_max": 12,
        "denom_min": 2,
        "denom_max": 8,
        "coef_min": 1,
        "coef_max": 12,
        "allow_negative": False,
        "allow_mixed": True,
        "require_proper": False,
        "dividend_form": "whole",
        "divisor_form": "any",
        "require_whole_quotient": False,
        "require_non_whole_quotient": False,
    },
    "hard": {
        "num_min": 1,
        "num_max": 15,
        "denom_min": 2,
        "denom_max": 12,
        "coef_min": 1,
        "coef_max": 15,
        "allow_negative": False,
        "allow_mixed": True,
        "require_proper": False,
        "dividend_form": "fraction",
        "divisor_form": "fraction",
        "require_whole_quotient": False,
        "require_non_whole_quotient": False,
    },
}
GENERATOR_DIFFICULTY_PRESETS["g6_how_many_groups_times"] = dict(_FRACTION_DIVIDE_WORD_TIERS)
GENERATOR_DIFFICULTY_PRESETS["g6_how_much_in_each_group_time"] = dict(_FRACTION_DIVIDE_WORD_TIERS)
GENERATOR_DIFFICULTY_PRESETS["g6_fraction_divide_groups"] = dict(_FRACTION_DIVIDE_WORD_TIERS)
GENERATOR_DIFFICULTY_PRESETS["g6_fraction_divide_each"] = dict(_FRACTION_DIVIDE_WORD_TIERS)
# Prime factorization: two small primes → 2–4 factors → 3–6 factors under 1000.
_PRIME_FACTOR_TIERS: TierPresets = {
    "easy": {
        "prime_factor_count_min": 2,
        "prime_factor_count_max": 2,
        "prime_max": 7,
        "factor_product_max": 50,
    },
    "medium": {
        "prime_factor_count_min": 2,
        "prime_factor_count_max": 4,
        "prime_max": 11,
        "factor_product_max": 200,
    },
    "hard": {
        "prime_factor_count_min": 3,
        "prime_factor_count_max": 6,
        "prime_max": 19,
        "factor_product_max": 999,
    },
}
GENERATOR_DIFFICULTY_PRESETS["g6_factoring"] = dict(_PRIME_FACTOR_TIERS)
GENERATOR_DIFFICULTY_PRESETS["pa_factoring"] = dict(_PRIME_FACTOR_TIERS)
# Long division with remainders: larger dividends / wider divisors by tier;
# remainders are always nonzero (enforced in the generator).
_LONG_DIVISION_REMAINDER_TIERS: TierPresets = {
    "easy": {
        "dividend_min": 10,
        "dividend_max": 99,
        "divisor_min": 2,
        "divisor_max": 9,
        "allow_negative": False,
    },
    "medium": {
        "dividend_min": 100,
        "dividend_max": 999,
        "divisor_min": 2,
        "divisor_max": 9,
        "allow_negative": False,
    },
    "hard": {
        "dividend_min": 1000,
        "dividend_max": 10000,
        "divisor_min": 2,
        "divisor_max": 49,
        "allow_negative": False,
    },
}
GENERATOR_DIFFICULTY_PRESETS["g6_long_division_with_remainders"] = dict(
    _LONG_DIVISION_REMAINDER_TIERS
)
GENERATOR_DIFFICULTY_PRESETS["g6_shapes_and_perimeter_on_the_coordinate_plane"] = {
    "easy": {
        "coord_min": 0,
        "coord_max": 6,
        "max_side": 4,
        "allow_l_shape": False,
    },
    "medium": {
        "coord_min": -3,
        "coord_max": 7,
        "max_side": 5,
        "allow_l_shape": False,
    },
    "hard": {
        "coord_min": -5,
        "coord_max": 8,
        "max_side": 6,
        "allow_l_shape": True,
    },
}
GENERATOR_DIFFICULTY_PRESETS["g6_coordinate_perimeter"] = dict(
    GENERATOR_DIFFICULTY_PRESETS["g6_shapes_and_perimeter_on_the_coordinate_plane"]
)
GENERATOR_DIFFICULTY_PRESETS["g6_equations_tape_diagrams"] = {
    "easy": {"tape_style": "uniform", "difficulty_tier": "easy"},
    "medium": {"tape_style": "mixed", "difficulty_tier": "medium"},
    "hard": {"tape_style": "nonuniform", "difficulty_tier": "hard"},
}
GENERATOR_DIFFICULTY_PRESETS["pa_integers_adding_and_subtracting"] = {
    "easy": {"num_min": -10, "num_max": 10, "allow_negative": True},
    "medium": {"num_min": -20, "num_max": 20, "allow_negative": True},
    "hard": {"num_min": -50, "num_max": 50, "allow_negative": True},
}
GENERATOR_DIFFICULTY_PRESETS["pa_integers_multiplying"] = dict(
    GENERATOR_DIFFICULTY_PRESETS["pa_integers_adding_and_subtracting"]
)
GENERATOR_DIFFICULTY_PRESETS["pa_integers_dividing"] = dict(
    GENERATOR_DIFFICULTY_PRESETS["pa_integers_adding_and_subtracting"]
)

# Algebra 2 / Precalc rational equations: harder structural mix
GENERATOR_DIFFICULTY_PRESETS["a2_rational_expressions_equations"] = {
    "easy": {
        "coef_min": -8,
        "coef_max": 8,
        "integer_only": True,
        "allow_simple_fraction": True,
        "allow_proportion": True,
        "allow_fraction_plus_constant": False,
        "allow_two_fractions": False,
    },
    "medium": {
        "coef_min": -12,
        "coef_max": 12,
        "integer_only": True,
        "allow_simple_fraction": False,
        "allow_proportion": False,
        "allow_fraction_plus_constant": True,
        "allow_two_fractions": True,
    },
    "hard": {
        "coef_min": -15,
        "coef_max": 15,
        "integer_only": True,
        "allow_simple_fraction": False,
        "allow_proportion": False,
        "allow_fraction_plus_constant": False,
        "allow_two_fractions": True,
    },
}
GENERATOR_DIFFICULTY_PRESETS["pc_rational_equations"] = dict(
    GENERATOR_DIFFICULTY_PRESETS["a2_rational_expressions_equations"]
)

# A1 intro trig sides: keep acute right triangles / modest ranges via geometry presets
GENERATOR_DIFFICULTY_PRESETS["find_missing_sides_of_triangles"] = {
    "easy": {"side_min": 3, "side_max": 12, "integer_only": True},
    "medium": {"side_min": 3, "side_max": 20, "integer_only": True},
    "hard": {"side_min": 5, "side_max": 30, "integer_only": False},
}
GENERATOR_DIFFICULTY_PRESETS["finding_sine_cosine_tangent"] = dict(
    GENERATOR_DIFFICULTY_PRESETS["find_missing_sides_of_triangles"]
)


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
