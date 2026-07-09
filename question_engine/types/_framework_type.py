"""Register a catalog-backed question type that delegates to a QuestionFramework."""

from __future__ import annotations

from typing import Any, Callable

from ..core.base import QuestionType, register
from ..core.models import SettingField
from ..core.registry import get_catalog_entry
from ..frameworks.base import QuestionFramework
from ..settings.resolve import TypeSettingConfig, resolve_type_settings


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
    config = TypeSettingConfig(
        setting_profile=setting_profile,
        inherits=inherits,
        exclude_settings=exclude_settings,
        extra_settings=extra_settings,
        setting_defaults=setting_defaults or {},
        count_default=entry.count_default or 10,
    )

    @register
    class FrameworkQuestionType(QuestionType):
        id = entry.id
        name = entry.name
        category = entry.category
        subcategory = entry.subcategory
        description = entry.description
        instruction_latex = entry.instruction_latex
        instruction_text = entry.instruction_text

        def settings_schema(self) -> list[SettingField]:
            return resolve_type_settings(config, *setting_schemas)

        def generate(self, settings: dict) -> list:
            return framework.generate_batch(self.id, settings)

    FrameworkQuestionType.__name__ = (
        f"{''.join(part.title() for part in type_id.split('_'))}QuestionType"
    )
    return FrameworkQuestionType
