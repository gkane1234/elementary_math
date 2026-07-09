"""Base class for reusable question generator frameworks."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from ..core.models import Question, SettingField
from ..generators.utils import make_questions
from ..settings.enrichment import merge_enrichment_metadata
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

    def build_question_metadata(
        self,
        settings: dict,
        *,
        prompt_latex: str,
        prompt_text: str,
        answer: str | None,
    ) -> dict[str, Any]:
        """Optional per-question metadata (e.g. graph specs tied to the answer)."""
        return {}

    def generate_batch(self, topic_id: str, settings: dict) -> list[Question]:
        count = int(settings.get("count", 10))
        include_answer_key = bool(settings.get("include_answer_key", False))
        base_metadata = self.build_metadata(settings)

        def builder() -> tuple[str, str, str | None]:
            return self.build_prompt(settings)

        def metadata_builder(
            prompt_latex: str,
            prompt_text: str,
            answer: str | None,
        ) -> dict[str, Any]:
            per_question = self.build_question_metadata(
                settings,
                prompt_latex=prompt_latex,
                prompt_text=prompt_text,
                answer=answer,
            )
            return merge_enrichment_metadata(settings, per_question, answer=answer)

        return make_questions(
            topic_id,
            count,
            include_answer_key,
            builder,
            metadata=base_metadata,
            metadata_builder=metadata_builder,
        )

    @staticmethod
    def framework_settings(*schemas: list[SettingField]) -> list[SettingField]:
        """Merge standard worksheet settings with domain-specific fields."""
        return merge_settings(standard_question_settings(), *schemas)
