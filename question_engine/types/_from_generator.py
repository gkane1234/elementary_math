"""Optional catalog re-registration with setting overrides.

Catalog entries are already registered by ``register_catalog_types()``. Use this
helper only when a type needs a different ``TypeSettingConfig`` than
``generator_profiles.config_for_generator(entry.generator)``. Prefer that path
over adding no-op ``register_from_catalog("id")`` modules.
"""

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

    has_override = any(
        [setting_profile, inherits, exclude_settings, setting_defaults]
    )
    if not has_override:
        raise ValueError(
            f"{type_id}: register_from_catalog requires setting overrides; "
            "catalog registration already covers the default family config"
        )

    override = TypeSettingConfig(
        setting_profile=setting_profile,
        inherits=tuple(inherits or ()),
        exclude_settings=tuple(exclude_settings or ()),
        setting_defaults=setting_defaults or {},
        count_default=entry.count_default,
    )
    register(make_catalog_type(entry, setting_config=override))
