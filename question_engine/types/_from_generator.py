"""Register a catalog entry that uses a real generator from generators/."""

from __future__ import annotations

from typing import Any

from ..core.base import register
from ..core.registry import get_catalog_entry
from ..core.scaffold import make_catalog_type
from ..settings.resolve import TypeSettingConfig


def register_from_catalog(
    type_id: str,
    *,
    setting_profile: str | None = None,
    inherits: list[str] | tuple[str, ...] | None = None,
    exclude_settings: list[str] | tuple[str, ...] | None = None,
    setting_defaults: dict[str, Any] | None = None,
) -> None:
    entry = get_catalog_entry(type_id)
    if entry.generator == "scaffold":
        raise ValueError(
            f"{type_id} uses scaffold generator; register via register_catalog_types()"
        )

    override: TypeSettingConfig | None = None
    if any([setting_profile, inherits, exclude_settings, setting_defaults]):
        override = TypeSettingConfig(
            setting_profile=setting_profile,
            inherits=tuple(inherits or ()),
            exclude_settings=tuple(exclude_settings or ()),
            setting_defaults=setting_defaults or {},
            count_default=entry.count_default,
        )

    register(make_catalog_type(entry, setting_config=override))
