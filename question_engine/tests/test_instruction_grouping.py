"""Tests for consecutive instruction factoring on worksheets."""

from __future__ import annotations

from question_engine.api.handler import _annotate_questions, _generate_for_type
from question_engine.core.base import QUESTION_TYPES
from question_engine.core.models import Question
from question_engine.utils.instruction_grouping import (
    group_questions_by_instruction,
    instruction_of,
    should_show_section_header,
)


def _q(qid: str, instruction: str | None) -> Question:
    meta = {}
    if instruction is not None:
        meta["instruction_latex"] = instruction
    return Question(
        id=qid,
        topic="t",
        prompt_latex=f"body-{qid}",
        prompt_text=f"body-{qid}",
        metadata=meta,
    )


def test_group_questions_by_instruction_aaba_pattern():
    """A A B A → header A + 2 bodies, header B + 1, header A + 1."""
    questions = [
        _q("1", "A"),
        _q("2", "A"),
        _q("3", "B"),
        _q("4", "A"),
    ]
    groups = group_questions_by_instruction(questions)
    assert len(groups) == 3
    assert groups[0].instruction == "A"
    assert [q.id for q in groups[0].questions] == ["1", "2"]
    assert groups[0].start_index == 0
    assert groups[1].instruction == "B"
    assert [q.id for q in groups[1].questions] == ["3"]
    assert groups[1].start_index == 2
    assert groups[2].instruction == "A"
    assert [q.id for q in groups[2].questions] == ["4"]
    assert groups[2].start_index == 3


def test_group_questions_null_instructions_stay_together():
    questions = [_q("1", None), _q("2", None), _q("3", "A")]
    groups = group_questions_by_instruction(questions)
    assert len(groups) == 2
    assert groups[0].instruction is None
    assert len(groups[0].questions) == 2
    assert groups[1].instruction == "A"


def test_should_show_section_header_skips_page_header_match():
    assert should_show_section_header(r"\text{Solve.}", r"\text{Solve.}") is False
    assert should_show_section_header(r"\text{Solve.}", None) is True
    assert should_show_section_header(None, None) is False


def test_distributive_stems_omit_instruction_and_factor_in_groups():
    type_id = "g6_distributive_property_numeric"
    question_type = QUESTION_TYPES[type_id]
    questions = _generate_for_type(
        type_id,
        {
            "count": 3,
            "include_answer_key": True,
            "difficulty": 5,
            "integers_only": True,
        },
    )
    assert len(questions) == 3
    instruction = instruction_of(questions[0])
    assert instruction
    assert "distributive" in instruction.lower()

    for q in questions:
        assert instruction_of(q) == instruction
        blob = f"{q.prompt_latex} {q.prompt_text}".lower()
        assert "distributive" not in blob
        assert "rewrite" not in blob
        # Stem is the expression body only.
        assert q.prompt_latex.strip()
        assert q.prompt_text.strip()

    groups = group_questions_by_instruction(questions)
    assert len(groups) == 1
    assert groups[0].instruction == instruction
    assert len(groups[0].questions) == 3
    # Same instruction as page header → no per-section header needed.
    assert should_show_section_header(instruction, instruction) is False


def test_annotate_preserves_catalog_instruction_on_stems():
    question_type = QUESTION_TYPES["g6_distributive_property_algebraic"]
    raw = [
        Question(
            id="a",
            topic="g6_distributive_property_algebraic",
            prompt_latex="3(x+2)",
            prompt_text="3(x+2)",
            metadata={},
        )
    ]
    annotated = _annotate_questions(raw, question_type, {"count": 1})
    assert "distributive" in (instruction_of(annotated[0]) or "").lower()
    assert "Rewrite" not in annotated[0].prompt_text
