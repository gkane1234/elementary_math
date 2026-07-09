"""Settings fields for calculus question types."""

from __future__ import annotations

from ...core.models import SettingField


def limit_settings(
    *,
    approach_min_default: int = -5,
    approach_max_default: int = 5,
) -> list[SettingField]:
    return [
        SettingField(
            "limit_approach_min",
            "Approach value min",
            "int",
            approach_min_default,
            min=-20,
            max=20,
            group="limits",
        ),
        SettingField(
            "limit_approach_max",
            "Approach value max",
            "int",
            approach_max_default,
            min=-20,
            max=20,
            group="limits",
        ),
        SettingField(
            "allow_infinity",
            "Include limits at infinity",
            "bool",
            False,
            group="limits",
        ),
        SettingField(
            "coef_min",
            "Coefficient min",
            "int",
            -6,
            min=-20,
            max=20,
            group="limits",
        ),
        SettingField(
            "coef_max",
            "Coefficient max",
            "int",
            6,
            min=-20,
            max=20,
            group="limits",
        ),
        SettingField(
            "power_min",
            "Power min",
            "int",
            1,
            min=0,
            max=6,
            group="limits",
        ),
        SettingField(
            "power_max",
            "Power max",
            "int",
            3,
            min=0,
            max=6,
            group="limits",
        ),
    ]


def derivative_settings(
    *,
    power_min_default: int = 1,
    power_max_default: int = 4,
    term_count_default: int = 2,
) -> list[SettingField]:
    return [
        SettingField(
            "power_min",
            "Power min",
            "int",
            power_min_default,
            min=0,
            max=8,
            group="derivatives",
        ),
        SettingField(
            "power_max",
            "Power max",
            "int",
            power_max_default,
            min=0,
            max=8,
            group="derivatives",
        ),
        SettingField(
            "term_count",
            "Number of terms",
            "int",
            term_count_default,
            min=1,
            max=5,
            group="derivatives",
        ),
        SettingField(
            "coef_min",
            "Coefficient min",
            "int",
            -8,
            min=-20,
            max=20,
            group="derivatives",
        ),
        SettingField(
            "coef_max",
            "Coefficient max",
            "int",
            8,
            min=-20,
            max=20,
            group="derivatives",
        ),
        SettingField(
            "include_constant_term",
            "Include constant terms",
            "bool",
            True,
            group="derivatives",
        ),
        SettingField(
            "variable",
            "Variable",
            "select",
            "x",
            options=["x", "t", "u"],
            group="derivatives",
        ),
    ]


def integral_settings(
    *,
    power_min_default: int = 1,
    power_max_default: int = 4,
    term_count_default: int = 2,
) -> list[SettingField]:
    return [
        SettingField(
            "power_min",
            "Power min",
            "int",
            power_min_default,
            min=0,
            max=8,
            group="integrals",
        ),
        SettingField(
            "power_max",
            "Power max",
            "int",
            power_max_default,
            min=0,
            max=8,
            group="integrals",
        ),
        SettingField(
            "term_count",
            "Number of terms",
            "int",
            term_count_default,
            min=1,
            max=5,
            group="integrals",
        ),
        SettingField(
            "coef_min",
            "Coefficient min",
            "int",
            -8,
            min=-20,
            max=20,
            group="integrals",
        ),
        SettingField(
            "coef_max",
            "Coefficient max",
            "int",
            8,
            min=-20,
            max=20,
            group="integrals",
        ),
        SettingField(
            "include_constant_term",
            "Include constant terms",
            "bool",
            True,
            group="integrals",
        ),
        SettingField(
            "require_positive_power",
            "Require positive power (avoid 1/x)",
            "bool",
            True,
            group="integrals",
        ),
        SettingField(
            "variable",
            "Variable",
            "select",
            "x",
            options=["x", "t", "u"],
            group="integrals",
        ),
    ]
