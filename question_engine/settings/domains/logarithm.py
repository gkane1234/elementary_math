"""Settings fields for logarithmic and exponential expression types."""

from __future__ import annotations

from ...core.models import SettingField


def logarithm_settings(
    *,
    base_min_default: int = 2,
    base_max_default: int = 10,
    argument_min_default: int = 2,
    argument_max_default: int = 1000,
) -> list[SettingField]:
    return [
        SettingField(
            "log_base_min",
            "Log base min",
            "int",
            base_min_default,
            min=2,
            max=20,
            group="logarithm",
        ),
        SettingField(
            "log_base_max",
            "Log base max",
            "int",
            base_max_default,
            min=2,
            max=20,
            group="logarithm",
        ),
        SettingField(
            "allow_natural_log",
            "Include natural log (ln)",
            "bool",
            True,
            group="logarithm",
        ),
        SettingField(
            "allow_common_log",
            "Include common log (log₁₀)",
            "bool",
            True,
            group="logarithm",
        ),
        SettingField(
            "log_argument_min",
            "Log argument min",
            "int",
            argument_min_default,
            min=2,
            max=10000,
            group="logarithm",
        ),
        SettingField(
            "log_argument_max",
            "Log argument max",
            "int",
            argument_max_default,
            min=2,
            max=10000,
            group="logarithm",
        ),
        SettingField(
            "require_integer_result",
            "Require integer log results",
            "bool",
            True,
            group="logarithm",
        ),
        SettingField(
            "allow_change_of_base",
            "Allow change-of-base problems",
            "bool",
            True,
            group="logarithm",
        ),
    ]


def exponential_equation_settings(
    *,
    base_min_default: int = 2,
    base_max_default: int = 10,
    exponent_min_default: int = 1,
    exponent_max_default: int = 5,
) -> list[SettingField]:
    return [
        SettingField(
            "exp_base_min",
            "Exponent base min",
            "int",
            base_min_default,
            min=2,
            max=20,
            group="exponential",
        ),
        SettingField(
            "exp_base_max",
            "Exponent base max",
            "int",
            base_max_default,
            min=2,
            max=20,
            group="exponential",
        ),
        SettingField(
            "exp_exponent_min",
            "Exponent min",
            "int",
            exponent_min_default,
            min=1,
            max=10,
            group="exponential",
        ),
        SettingField(
            "exp_exponent_max",
            "Exponent max",
            "int",
            exponent_max_default,
            min=1,
            max=10,
            group="exponential",
        ),
        SettingField(
            "allow_fractional_exponents",
            "Allow fractional exponents",
            "bool",
            False,
            group="exponential",
        ),
        SettingField(
            "coef_min",
            "Coefficient min",
            "int",
            -6,
            min=-20,
            max=20,
            group="exponential",
        ),
        SettingField(
            "coef_max",
            "Coefficient max",
            "int",
            6,
            min=-20,
            max=20,
            group="exponential",
        ),
    ]
