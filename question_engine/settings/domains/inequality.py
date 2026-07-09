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
