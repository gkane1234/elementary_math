"""Group consecutive worksheet questions that share the same instruction.

Mirrors ``groupQuestionsByInstruction`` / ``shouldShowSectionHeader`` in
``lib/worksheet.ts`` so generators and gallery scripts can reason about
factored headers the same way as the React worksheet UI.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence


@dataclass(frozen=True)
class InstructionGroup:
    instruction: str | None
    questions: list[Any]
    start_index: int


def instruction_of(question: Any) -> str | None:
    """Resolve instruction from a question object, dict, or metadata."""
    if question is None:
        return None
    if isinstance(question, Mapping):
        direct = question.get("instruction_latex")
        if isinstance(direct, str) and direct:
            return direct
        meta = question.get("metadata") or {}
        if isinstance(meta, Mapping):
            nested = meta.get("instruction_latex")
            if isinstance(nested, str) and nested:
                return nested
        return None
    direct = getattr(question, "instruction_latex", None)
    if isinstance(direct, str) and direct:
        return direct
    meta = getattr(question, "metadata", None) or {}
    if isinstance(meta, Mapping):
        nested = meta.get("instruction_latex")
        if isinstance(nested, str) and nested:
            return nested
    return None


def group_questions_by_instruction(questions: Sequence[Any]) -> list[InstructionGroup]:
    """Group consecutive questions that share the same instruction_latex."""
    if not questions:
        return []

    groups: list[InstructionGroup] = []
    current: InstructionGroup | None = None

    for index, question in enumerate(questions):
        instruction = instruction_of(question)
        if current is None or current.instruction != instruction:
            current = InstructionGroup(
                instruction=instruction,
                questions=[question],
                start_index=index,
            )
            groups.append(current)
            continue
        current.questions.append(question)

    return groups


def should_show_section_header(
    instruction: str | None,
    header_instruction: str | None,
) -> bool:
    """Whether to show a section header (skip if already in the page header)."""
    if not instruction:
        return False
    if header_instruction and instruction == header_instruction:
        return False
    return True
