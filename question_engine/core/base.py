from abc import ABC, abstractmethod

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
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "subcategory": self.subcategory,
            "instruction_latex": self.instruction_latex,
            "instruction_text": self.instruction_text,
            "settings": [field.to_dict() for field in self.settings_schema()],
        }


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
