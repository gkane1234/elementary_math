"""Settings fields for linear functions, systems, and coordinate-plane types."""

from __future__ import annotations

from ...core.models import SettingField


def linear_slope_settings(
    *,
    slope_min_default: int = -6,
    slope_max_default: int = 6,
) -> list[SettingField]:
    return [
        SettingField(
            "slope_min",
            "Slope min",
            "int",
            slope_min_default,
            min=-20,
            max=20,
            group="linear",
        ),
        SettingField(
            "slope_max",
            "Slope max",
            "int",
            slope_max_default,
            min=-20,
            max=20,
            group="linear",
        ),
    ]


def linear_intercept_settings(
    *,
    intercept_min_default: int = -8,
    intercept_max_default: int = 8,
) -> list[SettingField]:
    return [
        SettingField(
            "intercept_min",
            "Intercept min",
            "int",
            intercept_min_default,
            min=-20,
            max=20,
            group="linear",
        ),
        SettingField(
            "intercept_max",
            "Intercept max",
            "int",
            intercept_max_default,
            min=-20,
            max=20,
            group="linear",
        ),
    ]


def coordinate_bounds_settings(
    *,
    coord_min_default: int = -8,
    coord_max_default: int = 8,
) -> list[SettingField]:
    return [
        SettingField(
            "coord_min",
            "Coordinate min",
            "int",
            coord_min_default,
            min=-20,
            max=0,
            group="linear",
        ),
        SettingField(
            "coord_max",
            "Coordinate max",
            "int",
            coord_max_default,
            min=0,
            max=20,
            group="linear",
        ),
        SettingField(
            "integer_coordinates",
            "Integer coordinates only",
            "bool",
            True,
            group="linear",
        ),
        SettingField(
            "axis_aligned_only",
            "Axis-aligned segments only",
            "bool",
            False,
            group="linear",
        ),
    ]


def quadrant_settings() -> list[SettingField]:
    return [
        SettingField(
            "quadrant",
            "Point quadrant",
            "select",
            "all",
            options=["all", "I", "II", "III", "IV"],
            group="linear",
        ),
    ]


def systems_settings() -> list[SettingField]:
    return [
        SettingField(
            "system_size",
            "Number of variables",
            "int",
            2,
            min=2,
            max=2,
            group="systems",
        ),
        SettingField(
            "system_coef_min",
            "System coefficient min",
            "int",
            1,
            min=-12,
            max=12,
            group="systems",
        ),
        SettingField(
            "system_coef_max",
            "System coefficient max",
            "int",
            5,
            min=-12,
            max=12,
            group="systems",
        ),
        SettingField(
            "elimination_weight",
            "Elimination method weight",
            "int",
            50,
            min=0,
            max=100,
            group="systems",
        ),
        SettingField(
            "substitution_weight",
            "Substitution method weight",
            "int",
            50,
            min=0,
            max=100,
            group="systems",
        ),
        SettingField(
            "prefer_integer_solutions",
            "Prefer integer solutions",
            "bool",
            True,
            group="systems",
        ),
        SettingField(
            "max_coefficient_magnitude",
            "Max coefficient magnitude",
            "int",
            5,
            min=1,
            max=12,
            group="systems",
        ),
    ]


def variation_settings() -> list[SettingField]:
    return [
        SettingField(
            "variation_constant_min",
            "Variation constant min",
            "int",
            2,
            min=1,
            max=50,
            group="variation",
        ),
        SettingField(
            "variation_constant_max",
            "Variation constant max",
            "int",
            12,
            min=1,
            max=50,
            group="variation",
        ),
        SettingField(
            "direct_variation_weight",
            "Direct variation weight",
            "int",
            50,
            min=0,
            max=100,
            group="variation",
        ),
        SettingField(
            "inverse_variation_weight",
            "Inverse variation weight",
            "int",
            50,
            min=0,
            max=100,
            group="variation",
        ),
    ]


def relations_settings(
    *,
    table_row_count_default: int = 3,
) -> list[SettingField]:
    return [
        SettingField(
            "table_row_count",
            "Table row count",
            "int",
            table_row_count_default,
            min=3,
            max=8,
            group="relations",
        ),
    ]


def more_on_slope_settings() -> list[SettingField]:
    """Ask-mode toggles for More on slope (mix of slope skills)."""
    return [
        SettingField(
            "ask_mode",
            "Question style",
            "select",
            "mixed",
            options=[
                "from_points",
                "from_equation",
                "from_graph",
                "find_equation",
                "classify",
                "parallel_perpendicular",
                "mixed",
            ],
            group="slope",
        ),
        SettingField(
            "allow_from_points",
            "Allow find slope from two points",
            "bool",
            True,
            group="slope",
        ),
        SettingField(
            "allow_from_equation",
            "Allow find slope from y = mx + b",
            "bool",
            True,
            group="slope",
        ),
        SettingField(
            "allow_from_graph",
            "Allow find slope from a graph",
            "bool",
            True,
            group="slope",
        ),
        SettingField(
            "allow_find_equation",
            "Allow write equation / find y-intercept",
            "bool",
            True,
            group="slope",
        ),
        SettingField(
            "allow_classify",
            "Allow classify positive/negative/zero/undefined",
            "bool",
            True,
            group="slope",
        ),
        SettingField(
            "allow_parallel_perpendicular",
            "Allow parallel / perpendicular slope",
            "bool",
            False,
            group="slope",
        ),
    ]
