"""Resolve inherited setting profiles into a final schema for a question type."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

from ..core.models import SettingField
from .profiles import PROFILE_BUILDERS
from .standard import merge_settings, standard_question_settings


@dataclass(frozen=True)
class TypeSettingConfig:
    """Declarative settings inheritance for a question type."""

    setting_profile: str | None = None
    inherits: tuple[str, ...] = ()
    exclude_settings: tuple[str, ...] = ()
    include_settings: tuple[SettingField, ...] = ()
    extra_settings: tuple[Callable[..., list[SettingField]], ...] = ()
    setting_defaults: dict[str, Any] = field(default_factory=dict)
    count_default: int = 10
    count_max: int = 50


def _profile_fields(profile_name: str) -> list[SettingField]:
    builder = PROFILE_BUILDERS.get(profile_name)
    if builder is None:
        raise KeyError(f"Unknown setting profile: {profile_name}")
    return builder()


def _collect_profile_fields(config: TypeSettingConfig) -> list[SettingField]:
    # Put common_enrichment first so difficulty appears early in the schema UI.
    enrichment: list[str] = []
    other_inherits: list[str] = []
    for name in config.inherits:
        if name == "common_enrichment":
            enrichment.append(name)
        else:
            other_inherits.append(name)

    profile_names: list[str] = [*enrichment]
    if config.setting_profile:
        profile_names.append(config.setting_profile)
    profile_names.extend(other_inherits)

    fields: list[SettingField] = []
    for name in profile_names:
        fields.extend(_profile_fields(name))
    return fields


def _apply_exclusions(
    fields: list[SettingField],
    exclude_keys: tuple[str, ...],
) -> list[SettingField]:
    if not exclude_keys:
        return fields
    excluded = set(exclude_keys)
    return [field for field in fields if field.key not in excluded]


def _apply_defaults(
    fields: list[SettingField],
    defaults: dict[str, Any],
) -> list[SettingField]:
    if not defaults:
        return fields
    updated: list[SettingField] = []
    for setting_field in fields:
        if setting_field.key not in defaults:
            updated.append(setting_field)
            continue
        updated.append(
            SettingField(
                setting_field.key,
                setting_field.label,
                setting_field.type,
                defaults[setting_field.key],
                min=setting_field.min,
                max=setting_field.max,
                options=setting_field.options,
                group=setting_field.group,
            )
        )
    return updated


def resolve_type_settings(
    config: TypeSettingConfig | None = None,
    *legacy_schemas: Callable[..., list[SettingField]],
) -> list[SettingField]:
    """Merge standard settings with inherited profiles and optional overrides.

    ``legacy_schemas`` are kept for backward compatibility with call sites that
    still pass explicit domain builders (e.g. ``equation_coef_settings``).
    """
    cfg = config or TypeSettingConfig()

    domain_fields = _collect_profile_fields(cfg)
    for schema in cfg.extra_settings:
        domain_fields.extend(schema())
    domain_fields.extend(cfg.include_settings)
    for schema in legacy_schemas:
        domain_fields.extend(schema())

    domain_fields = _apply_exclusions(domain_fields, cfg.exclude_settings)
    domain_fields = merge_settings(domain_fields)
    domain_fields = _apply_defaults(domain_fields, cfg.setting_defaults)

    return merge_settings(
        standard_question_settings(
            count_default=cfg.count_default,
            count_max=cfg.count_max,
        ),
        domain_fields,
    )
