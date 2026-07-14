"""Number-line topic types emit blank prompt + answer_number_line_spec."""

from __future__ import annotations

import json

import question_engine.types  # noqa: F401
from question_engine.api.handler import handle_generate

# Explicit number-line / graph-on-number-line topics (G6 / PA / A1).
NUMBER_LINE_TYPES = [
    "g6_numbers_on_a_number_line",
    "g6_number_line_word_problems",
    "g6_solutions_to_inequalities",
    "g6_writing_and_graphing_inequalities",
    "g6_solving_and_graphing_one_step_inequalities",
    "graphing_single_variable_inequalities",
    "one_step_inequalities",
    "two_step_inequalities",
    "multi_step_inequalities",
    "pa_multi_step_inequalities",
    "compound_inequalities",
    "absolute_value_inequalities",
]


def test_number_line_types_emit_blank_number_line_by_default():
    for tid in NUMBER_LINE_TYPES:
        status, _, body = handle_generate(
            {"type_id": tid, "settings": {"count": 1, "include_answer_key": True}}
        )
        data = json.loads(body)
        assert status == 200, f"{tid}: {data.get('error')}"
        meta = data["questions"][0].get("metadata") or {}
        nls = meta.get("number_line_spec")
        assert nls, f"{tid}: missing number_line_spec"
        assert nls.get("blank") is True, f"{tid}: prompt line should be blank for student work"
        assert meta.get("answer_number_line_spec"), f"{tid}: missing answer_number_line_spec"


def test_number_line_word_problem_answer_marks_endpoint():
    status, _, body = handle_generate(
        {
            "type_id": "g6_number_line_word_problems",
            "settings": {"count": 1, "include_answer_key": True},
        }
    )
    data = json.loads(body)
    assert status == 200
    meta = data["questions"][0]["metadata"]
    ans = meta["answer_number_line_spec"]
    assert ans.get("direction") == "both"
    assert ans.get("inclusive") is True
    assert ans.get("blank") is not True
