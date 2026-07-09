"""Settings fields for sequence and series question types."""

from __future__ import annotations

from ...core.models import SettingField


def sequence_settings(
    *,
    first_term_min_default: int = -10,
    first_term_max_default: int = 10,
    nth_min_default: int = 3,
    nth_max_default: int = 12,
) -> list[SettingField]:
    return [
        SettingField(
            "first_term_min",
            "First term min",
            "int",
            first_term_min_default,
            min=-50,
            max=50,
            group="sequence",
        ),
        SettingField(
            "first_term_max",
            "First term max",
            "int",
            first_term_max_default,
            min=-50,
            max=50,
            group="sequence",
        ),
        SettingField(
            "nth_min",
            "Term index min (n)",
            "int",
            nth_min_default,
            min=2,
            max=30,
            group="sequence",
        ),
        SettingField(
            "nth_max",
            "Term index max (n)",
            "int",
            nth_max_default,
            min=2,
            max=30,
            group="sequence",
        ),
        SettingField(
            "common_diff_min",
            "Common difference min",
            "int",
            -8,
            min=-20,
            max=20,
            group="sequence",
        ),
        SettingField(
            "common_diff_max",
            "Common difference max",
            "int",
            8,
            min=-20,
            max=20,
            group="sequence",
        ),
        SettingField(
            "common_ratio_min",
            "Common ratio min",
            "int",
            -4,
            min=-10,
            max=10,
            group="sequence",
        ),
        SettingField(
            "common_ratio_max",
            "Common ratio max",
            "int",
            4,
            min=-10,
            max=10,
            group="sequence",
        ),
        SettingField(
            "allow_negative_ratio",
            "Allow negative common ratio",
            "bool",
            False,
            group="sequence",
        ),
        SettingField(
            "integer_terms_only",
            "Integer terms only",
            "bool",
            True,
            group="sequence",
        ),
    ]
