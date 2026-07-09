"""Settings fields for misc / algebraic-expression question types."""

from __future__ import annotations

from ...core.models import SettingField


def misc_expression_settings(
    *,
    term_count_default: int = 4,
    exponent_min_default: int = 2,
    exponent_max_default: int = 7,
    phrase_complexity_default: str = "standard",
) -> list[SettingField]:
    return [
        SettingField(
            "term_count",
            "Number of terms",
            "int",
            term_count_default,
            min=2,
            max=8,
            group="expression",
        ),
        SettingField(
            "exponent_min",
            "Exponent min",
            "int",
            exponent_min_default,
            min=1,
            max=12,
            group="expression",
        ),
        SettingField(
            "exponent_max",
            "Exponent max",
            "int",
            exponent_max_default,
            min=1,
            max=12,
            group="expression",
        ),
        SettingField(
            "phrase_complexity",
            "Phrase complexity",
            "select",
            phrase_complexity_default,
            options=["simple", "standard", "advanced"],
            group="expression",
        ),
        SettingField(
            "constant_min",
            "Constant min",
            "int",
            2,
            min=1,
            max=30,
            group="expression",
        ),
        SettingField(
            "constant_max",
            "Constant max",
            "int",
            12,
            min=1,
            max=30,
            group="expression",
        ),
        SettingField(
            "max_phrase_operations",
            "Max operations in phrase",
            "int",
            2,
            min=1,
            max=4,
            group="expression",
        ),
        SettingField(
            "allow_fraction_constants",
            "Allow fractions in constants",
            "bool",
            False,
            group="expression",
        ),
    ]
