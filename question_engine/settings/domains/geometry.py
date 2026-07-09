"""Settings fields for geometry measurement question types."""

from __future__ import annotations

from ...core.models import SettingField


def geometry_settings() -> list[SettingField]:
    return [
        SettingField(
            "include_diagram",
            "Include diagram metadata",
            "bool",
            False,
            group="geometry",
        ),
    ]
