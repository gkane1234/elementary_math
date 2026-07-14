"""Thin adapters from QuestionFramework instances to GENERATORS callables.

Catalog entries look up producers by family key in ``GENERATORS``. Prefer
implementing math in ``QuestionFramework`` subclasses, then expose them with
``framework_generators`` so catalog wiring stays a single dict of keys.
"""

from __future__ import annotations

from typing import Callable

from ..core.models import Question
from .base import QuestionFramework


def framework_generator(
    framework: QuestionFramework,
) -> Callable[[str, dict], list[Question]]:
    def generate(topic: str, settings: dict) -> list[Question]:
        return framework.generate_batch(topic, settings)

    return generate


def framework_generators(
    frameworks: dict[str, QuestionFramework],
) -> dict[str, Callable[[str, dict], list[Question]]]:
    return {key: framework_generator(framework) for key, framework in frameworks.items()}
