"""Lazy wrappers so catalog entries can use hand-written generator keys."""

from __future__ import annotations

from typing import Callable

from ..core.models import Question

HAND_WRITTEN_KEYS = frozenset(
    {
        "quadratic_factoring",
        "polynomial_long_division",
        "radical_simplification",
        "rational_simplification",
        "rational_expression_simplification",
    }
)


def _wrap_hand_written(canonical_id: str) -> Callable[[str, dict], list[Question]]:
    def generate(topic: str, settings: dict) -> list[Question]:
        from question_engine.core.base import QUESTION_TYPES

        if canonical_id not in QUESTION_TYPES:
            import question_engine.types  # noqa: F401

        question_type = QUESTION_TYPES[canonical_id]
        questions = question_type.generate(settings)
        for question in questions:
            question.topic = topic
        return questions

    return generate


GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = {
    key: _wrap_hand_written(key) for key in HAND_WRITTEN_KEYS
}
