from typing import Callable

from .base import QuestionType, register
from ..catalogs.base import TypeCatalogEntry
from .registry import TYPE_CATALOG
from ..settings.generator_profiles import config_for_generator
from ..settings.resolve import TypeSettingConfig, resolve_type_settings
from ..generators import GENERATORS
from .models import Question, SettingField
from .metadata import scaffold_metadata


def make_catalog_type(
    entry: TypeCatalogEntry,
    *,
    setting_config: TypeSettingConfig | None = None,
) -> type[QuestionType]:
    generator_key = entry.generator
    uses_scaffold = generator_key == "scaffold" or generator_key not in GENERATORS
    generator: Callable[[str, dict], list[Question]] = GENERATORS.get(
        generator_key,
        GENERATORS["scaffold"],
    )
    resolved_config = setting_config or config_for_generator(generator_key)
    if resolved_config is None:
        resolved_config = TypeSettingConfig(count_default=entry.count_default)
    elif resolved_config.count_default == 10 and entry.count_default != 10:
        resolved_config = TypeSettingConfig(
            setting_profile=resolved_config.setting_profile,
            inherits=resolved_config.inherits,
            exclude_settings=resolved_config.exclude_settings,
            include_settings=resolved_config.include_settings,
            extra_settings=resolved_config.extra_settings,
            setting_defaults=resolved_config.setting_defaults,
            count_default=entry.count_default,
            count_max=resolved_config.count_max,
        )

    class CatalogQuestionType(QuestionType):
        id = entry.id
        name = entry.name
        category = entry.category
        subcategory = entry.subcategory
        description = entry.description
        instruction_latex = entry.instruction_latex
        instruction_text = entry.instruction_text
        _count_default = entry.count_default
        _generator = staticmethod(generator)
        _uses_scaffold = uses_scaffold
        _setting_config = resolved_config
        setting_profile = resolved_config.setting_profile if resolved_config else None

        def settings_schema(self) -> list[SettingField]:
            return resolve_type_settings(self._setting_config)

        def generate(self, settings: dict) -> list[Question]:
            questions = self._generator(self.id, settings)
            if self._uses_scaffold:
                for question in questions:
                    question.metadata = {**scaffold_metadata(), **question.metadata}
            return questions

    CatalogQuestionType.__name__ = f"{''.join(part.title() for part in entry.id.split('_'))}QuestionType"
    return CatalogQuestionType


def register_catalog_types() -> None:
    for entry in TYPE_CATALOG:
        if entry.generator != "scaffold":
            continue
        register(make_catalog_type(entry))
