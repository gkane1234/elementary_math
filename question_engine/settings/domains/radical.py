"""Settings fields for radical expression question types."""

from __future__ import annotations

from ...core.models import SettingField


def radical_settings(
    *,
    radicand_min_default: int = 12,
    radicand_max_default: int = 300,
    index_default: int = 2,
) -> list[SettingField]:
    return [
        SettingField(
            "radicand_min",
            "Radicand min",
            "int",
            radicand_min_default,
            min=2,
            max=1000,
            group="radical",
        ),
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
        SettingField(
            "require_simplifiable",
            "Require simplifiable radicals",
            "bool",
            True,
            group="radical",
        ),
    ]
