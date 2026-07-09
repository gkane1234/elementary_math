"""Shared generation utilities for question builders."""

from __future__ import annotations

import random
import uuid
from fractions import Fraction
from typing import Any, Callable

from ..core.models import Question


def frac_latex(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    if value.numerator < 0:
        return f"-\\frac{{{abs(value.numerator)}}}{{{value.denominator}}}"
    return f"\\frac{{{value.numerator}}}{{{value.denominator}}}"


def random_fraction(
    *,
    num_min: int = -10,
    num_max: int = 10,
    denom_min: int = 2,
    denom_max: int = 12,
) -> Fraction:
    denominator = random.randint(denom_min, denom_max)
    numerator = random.randint(num_min, num_max)
    while numerator == 0:
        numerator = random.randint(num_min, num_max)
    return Fraction(numerator, denominator)


def make_questions(
    topic: str,
    count: int,
    include_answer_key: bool,
    builder: Callable[[], tuple[str, str, str | None]],
    *,
    metadata: dict[str, Any] | None = None,
) -> list[Question]:
    questions: list[Question] = []
    base_metadata = dict(metadata or {})
    for _ in range(count):
        prompt_latex, prompt_text, answer = builder()
        questions.append(
            Question(
                id=str(uuid.uuid4()),
                topic=topic,
                prompt_latex=prompt_latex,
                prompt_text=prompt_text,
                answer_latex=answer if include_answer_key else None,
                metadata=dict(base_metadata),
            )
        )
    return questions


def random_int_range(
    minimum: int,
    maximum: int,
    *,
    exclude: set[int] | None = None,
) -> int:
    while True:
        value = random.randint(minimum, maximum)
        if exclude is None or value not in exclude:
            return value


def pick_operation(operations: list[str]) -> str:
    return random.choice(operations)


def format_equation_latex(
    lhs: str,
    rhs: str,
    *,
    relation: str = "=",
) -> str:
    return f"{lhs} {relation} {rhs}"


# Backward-compatible aliases used by generators/basic.py
_frac_latex = frac_latex
_random_fraction = random_fraction
_make_questions = make_questions
