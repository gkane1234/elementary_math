"""Settings fields for radical expression question types."""

from __future__ import annotations

from ...core.models import SettingField


def radical_settings(
    *,
    radicand_max_default: int = 200,
    index_default: int = 2,
) -> list[SettingField]:
    return [
        SettingField(
            "radicand_max",
            "Radicand max",
            "int",
            radicand_max_default,
            min=2,
            max=1000,
            group="radical",
        ),
        SettingField(
            "radical_index",
            "Root index",
            "int",
            index_default,
            min=2,
            max=5,
            group="radical",
        ),
    ]
