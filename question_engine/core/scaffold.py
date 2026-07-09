from typing import Callable

from .base import QuestionType, register
from ..catalogs.base import TypeCatalogEntry
from .registry import TYPE_CATALOG
from ..settings.standard import standard_question_settings
from ..generators import GENERATORS
from .models import Question, SettingField
from .metadata import scaffold_metadata


def make_catalog_type(entry: TypeCatalogEntry) -> type[QuestionType]:
    generator_key = entry.generator
    uses_scaffold = generator_key == "scaffold" or generator_key not in GENERATORS
    generator: Callable[[str, dict], list[Question]] = GENERATORS.get(
        generator_key,
        GENERATORS["scaffold"],
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

        def settings_schema(self) -> list[SettingField]:
            return standard_question_settings(count_default=self._count_default)

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
