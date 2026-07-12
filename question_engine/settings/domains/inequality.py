"""Settings fields for inequality question types."""

from __future__ import annotations

from ...core.models import SettingField


def inequality_settings() -> list[SettingField]:
    return [
        SettingField(
            "steps",
            "Solution steps",
            "int",
            1,
            min=1,
            max=3,
            group="inequality",
        ),
        SettingField(
            "include_graph_metadata",
            "Include graph / number-line metadata",
            "bool",
            False,
            group="inequality",
        ),
    ]


def inequality_direction_settings() -> list[SettingField]:
    return [
        SettingField("allow_lt", "Allow <", "bool", True, group="inequality"),
        SettingField("allow_gt", "Allow >", "bool", True, group="inequality"),
        SettingField("allow_lte", "Allow ≤", "bool", True, group="inequality"),
        SettingField("allow_gte", "Allow ≥", "bool", True, group="inequality"),
    ]


def compound_inequality_settings() -> list[SettingField]:
    return [
        SettingField(
            "compound_style",
            "Compound style",
            "select",
            "and",
            options=["and", "or", "mixed"],
            group="inequality",
        ),
        SettingField(
            "allow_inclusive",
            "Allow inclusive inequalities (≤ / ≥)",
            "bool",
            True,
            group="inequality",
        ),
    ]
