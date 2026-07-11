"""Settings fields for numeric expression question types."""

from __future__ import annotations

from ...core.models import SettingField


def number_coef_settings(
    *,
    num_min_default: int = -10,
    num_max_default: int = 10,
    num_bound: int = 50,
) -> list[SettingField]:
    return [
        SettingField(
            "num_min",
            "Numerator min",
            "int",
            num_min_default,
            min=-num_bound,
            max=num_bound,
            group="number",
        ),
        SettingField(
            "num_max",
            "Numerator max",
            "int",
            num_max_default,
            min=-num_bound,
            max=num_bound,
            group="number",
        ),
    ]


def denominator_settings(
    *,
    denom_min_default: int = 2,
    denom_max_default: int = 12,
) -> list[SettingField]:
    return [
        SettingField(
            "denom_min",
            "Denominator min",
            "int",
            denom_min_default,
            min=2,
            max=50,
            group="number",
        ),
        SettingField(
            "denom_max",
            "Denominator max",
            "int",
            denom_max_default,
            min=2,
            max=50,
            group="number",
        ),
    ]


def percent_settings() -> list[SettingField]:
    return [
        SettingField(
            "percent_min",
            "Percent min",
            "int",
            5,
            min=1,
            max=100,
            group="number",
        ),
        SettingField(
            "percent_max",
            "Percent max",
            "int",
            75,
            min=1,
            max=100,
            group="number",
        ),
        SettingField(
            "base_min",
            "Base value min",
            "int",
            10,
            min=1,
            max=1000,
            group="number",
        ),
        SettingField(
            "base_max",
            "Base value max",
            "int",
            200,
            min=1,
            max=1000,
            group="number",
        ),
        SettingField(
            "round_to_whole",
            "Round percent answers to whole numbers",
            "bool",
            False,
            group="number",
        ),
        SettingField(
            "allow_decimal_percents",
            "Allow decimal percents",
            "bool",
            False,
            group="number",
        ),
    ]


def decimal_places_settings() -> list[SettingField]:
    return [
        SettingField(
            "decimal_places",
            "Decimal places",
            "int",
            2,
            min=1,
            max=3,
            group="number",
        ),
    ]


def allow_negative_settings(*, default: bool = True) -> list[SettingField]:
    return [
        SettingField(
            "allow_negative",
            "Allow negative numbers",
            "bool",
            default,
            group="number",
        ),
    ]


def ratio_settings(
    *,
    part_min_default: int = 2,
    part_max_default: int = 15,
) -> list[SettingField]:
    return [
        SettingField(
            "ratio_part_min",
            "Ratio part min",
            "int",
            part_min_default,
            min=1,
            max=50,
            group="number",
        ),
        SettingField(
            "ratio_part_max",
            "Ratio part max",
            "int",
            part_max_default,
            min=1,
            max=50,
            group="number",
        ),
    ]


def unit_rate_settings() -> list[SettingField]:
    return [
        SettingField(
            "unit_rate_min",
            "Unit rate min",
            "int",
            2,
            min=1,
            max=50,
            group="number",
        ),
        SettingField(
            "unit_rate_max",
            "Unit rate max",
            "int",
            12,
            min=1,
            max=50,
            group="number",
        ),
        SettingField(
            "unit_rate_multiplier_min",
            "Quantity multiplier min",
            "int",
            2,
            min=2,
            max=20,
            group="number",
        ),
        SettingField(
            "unit_rate_multiplier_max",
            "Quantity multiplier max",
            "int",
            8,
            min=2,
            max=20,
            group="number",
        ),
    ]


def scientific_notation_settings() -> list[SettingField]:
    return [
        SettingField(
            "sci_exp_min",
            "Exponent min",
            "int",
            -8,
            min=-12,
            max=12,
            group="number",
        ),
        SettingField(
            "sci_exp_max",
            "Exponent max",
            "int",
            8,
            min=-12,
            max=12,
            group="number",
        ),
    ]


def factor_bounds_settings(
    *,
    factor_min_default: int = 4,
    factor_max_default: int = 60,
) -> list[SettingField]:
    return [
        SettingField(
            "factor_min",
            "Factor range min",
            "int",
            factor_min_default,
            min=2,
            max=200,
            group="number",
        ),
        SettingField(
            "factor_max",
            "Factor range max",
            "int",
            factor_max_default,
            min=2,
            max=200,
            group="number",
        ),
    ]


def gcf_constraint_settings(
    *,
    require_gcf_greater_than_one_default: bool = True,
) -> list[SettingField]:
    """GCF-only: require a non-trivial greatest common factor."""
    return [
        SettingField(
            "require_gcf_greater_than_one",
            "Require GCF > 1",
            "bool",
            require_gcf_greater_than_one_default,
            group="number",
        ),
    ]


def pemdas_settings() -> list[SettingField]:
    return [
        SettingField(
            "pemdas_complexity",
            "PEMDAS complexity",
            "select",
            "mixed",
            options=["basic", "parentheses", "exponent", "mixed"],
            group="number",
        ),
    ]
