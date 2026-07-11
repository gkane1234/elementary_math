from abc import ABC, abstractmethod

from ..utils.instruction_latex import repair_instruction_latex
from .models import Question, SettingField

QUESTION_TYPES: dict[str, "QuestionType"] = {}


class QuestionType(ABC):
    id: str
    name: str
    description: str
    category: str = "Other"
    subcategory: str | None = None
    instruction_latex: str | None = None
    instruction_text: str | None = None

    @abstractmethod
    def settings_schema(self) -> list[SettingField]:
        pass

    @abstractmethod
    def generate(self, settings: dict) -> list[Question]:
        pass

    def to_dict(self) -> dict:
        from ..type_readiness import (
            type_incorrect_implementation,
            type_not_ready,
            type_requires_diagram,
        )

        payload = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "subcategory": self.subcategory,
            "instruction_latex": repair_instruction_latex(self.instruction_latex),
            "instruction_text": self.instruction_text,
            "settings": [field.to_dict() for field in self.settings_schema()],
            "requires_diagram": type_requires_diagram(self.id),
            "incorrect_implementation": type_incorrect_implementation(self.id),
            "not_ready": type_not_ready(self.id),
        }
        profile = getattr(self, "setting_profile", None)
        if profile is None:
            config = getattr(self, "_setting_config", None)
            if config is not None:
                profile = getattr(config, "setting_profile", None)
        if profile:
            payload["setting_profile"] = profile
        return payload


def register(question_type_cls: type[QuestionType]) -> type[QuestionType]:
    instance = question_type_cls()
    QUESTION_TYPES[instance.id] = instance
    return question_type_cls


def _type_sort_key(question_type: QuestionType) -> tuple[int, str, str, str]:
    from .registry import CATEGORY_ORDER

    try:
        category_index = CATEGORY_ORDER.index(question_type.category)
    except ValueError:
        category_index = len(CATEGORY_ORDER)

    subcategory = question_type.subcategory or ""
    return (category_index, subcategory, question_type.name.lower(), question_type.id)


def list_question_types() -> list[dict]:
    sorted_types = sorted(QUESTION_TYPES.values(), key=_type_sort_key)
    return [qt.to_dict() for qt in sorted_types]
