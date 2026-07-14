"""Register a catalog-backed question type that delegates to a QuestionFramework."""

from __future__ import annotations

from typing import Any, Callable

from ..core.base import QuestionType, register
from ..core.models import SettingField
from ..core.registry import get_catalog_entry
from ..frameworks.base import QuestionFramework
from ..settings.generator_profiles import config_for_type
from ..settings.resolve import TypeSettingConfig, resolve_type_settings

_ENRICHMENT = "common_enrichment"


def _merge_excludes(*groups: tuple[str, ...]) -> tuple[str, ...]:
    keys: list[str] = []
    for group in groups:
        keys.extend(group)
    return tuple(dict.fromkeys(keys))


def register_framework_type(
    type_id: str,
    framework: QuestionFramework,
    *setting_schemas: Callable[..., list[SettingField]],
    setting_profile: str | None = None,
    inherits: tuple[str, ...] = (),
    exclude_settings: tuple[str, ...] = (),
    extra_settings: tuple[Callable[..., list[SettingField]], ...] = (),
    setting_defaults: dict[str, Any] | None = None,
) -> type[QuestionType]:
    entry = get_catalog_entry(type_id)
    gen_config = config_for_type(type_id)

    profile = setting_profile
    inherit_profiles = inherits
    excludes = exclude_settings
    extras = extra_settings
    defaults = dict(setting_defaults or {})

    if gen_config is not None:
        profile = profile or gen_config.setting_profile
        if not inherit_profiles:
            inherit_profiles = gen_config.inherits
        excludes = _merge_excludes(gen_config.exclude_settings, exclude_settings)
        if not extras:
            extras = gen_config.extra_settings
        defaults = {**gen_config.setting_defaults, **defaults}

    if _ENRICHMENT not in inherit_profiles:
        inherit_profiles = (_ENRICHMENT, *inherit_profiles)

    config = TypeSettingConfig(
        setting_profile=profile,
        inherits=inherit_profiles,
        exclude_settings=excludes,
        extra_settings=extras,
        setting_defaults=defaults,
        count_default=entry.count_default or 10,
    )
    resolved_profile = profile

    @register
    class FrameworkQuestionType(QuestionType):
        id = entry.id
        name = entry.name
        category = entry.category
        subcategory = entry.subcategory
        description = entry.description
        instruction_latex = entry.instruction_latex
        instruction_text = entry.instruction_text
        setting_profile = resolved_profile
        _setting_config = config

        def settings_schema(self) -> list[SettingField]:
            return resolve_type_settings(config, *setting_schemas)

        def generate(self, settings: dict) -> list:
            return framework.generate_batch(self.id, settings)

    FrameworkQuestionType.__name__ = (
        f"{''.join(part.title() for part in type_id.split('_'))}QuestionType"
    )
    return FrameworkQuestionType
