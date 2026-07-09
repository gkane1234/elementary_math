"""Base class for reusable question generator frameworks."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from ..core.models import Question, SettingField
from ..generators.utils import make_questions
from ..settings.standard import merge_settings, standard_question_settings


class QuestionFramework(ABC):
    """Shared batch generation for families of related question types."""

    instruction_latex: str | None = None
    instruction_text: str | None = None

    @abstractmethod
    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        """Return (prompt_latex, prompt_text, answer)."""

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return {}

    def generate_batch(self, topic_id: str, settings: dict) -> list[Question]:
        count = int(settings.get("count", 10))
        include_answer_key = bool(settings.get("include_answer_key", False))
        metadata = self.build_metadata(settings)

        def builder() -> tuple[str, str, str | None]:
            return self.build_prompt(settings)

        return make_questions(
            topic_id,
            count,
            include_answer_key,
            builder,
            metadata=metadata,
        )

    @staticmethod
    def framework_settings(*schemas: list[SettingField]) -> list[SettingField]:
        """Merge standard worksheet settings with domain-specific fields."""
        return merge_settings(standard_question_settings(), *schemas)
