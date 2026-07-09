import json
from typing import Any

from ..core.base import QUESTION_TYPES, list_question_types
from ..utils.layout import resolve_column_count
from ..core.models import Question, QuestionSet


def _json_response(status: int, body: dict[str, Any]) -> tuple[int, dict[str, str], str]:
    return status, {"Content-Type": "application/json"}, json.dumps(body)


def _settings_for_regeneration(settings: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in settings.items() if key not in {"count", "max_columns"}}


def _annotate_questions(
    questions: list[Question],
    question_type,
    settings: dict[str, Any],
) -> list[Question]:
    generation_settings = _settings_for_regeneration(settings)
    for question in questions:
        question.metadata = {
            **question.metadata,
            "generation_settings": generation_settings,
            "instruction_latex": question_type.instruction_latex,
        }
    return questions


def _generate_for_type(type_id: str, settings: dict[str, Any]) -> list[Question]:
    question_type = QUESTION_TYPES.get(type_id)
    if question_type is None:
        raise ValueError(f"Unknown question type: {type_id}")

    questions = question_type.generate(settings)
    return _annotate_questions(questions, question_type, settings)


def handle_generate(body: dict[str, Any]) -> tuple[int, dict[str, str], str]:
    title = body.get("title") or "Worksheet"
    worksheet_settings = body.get("worksheet_settings", {})
    sections = body.get("sections")

    if sections:
        all_questions: list[Question] = []
        for section in sections:
            type_id = section.get("type_id")
            if not type_id:
                return _json_response(400, {"error": "Each section requires type_id"})

            section_settings = dict(section.get("settings", {}))
            section_settings["count"] = int(section.get("count", section_settings.get("count", 1)))

            try:
                all_questions.extend(_generate_for_type(type_id, section_settings))
            except ValueError as error:
                return _json_response(404, {"error": str(error)})

        columns = resolve_column_count(
            len(all_questions),
            worksheet_settings.get("max_columns", "auto"),
        )
        question_set = QuestionSet(
            title=title,
            questions=all_questions,
            settings_snapshot=worksheet_settings,
            columns=columns,
        )
        return _json_response(200, question_set.to_dict())

    type_id = body.get("type_id")
    if not type_id:
        return _json_response(400, {"error": "type_id or sections is required"})

    question_type = QUESTION_TYPES.get(type_id)
    if question_type is None:
        return _json_response(404, {"error": f"Unknown question type: {type_id}"})

    settings = body.get("settings", {})
    questions = _generate_for_type(type_id, settings)
    columns = resolve_column_count(len(questions), settings.get("max_columns", "auto"))
    question_set = QuestionSet(
        title=title,
        questions=questions,
        settings_snapshot=settings,
        instruction_latex=question_type.instruction_latex,
        instruction_text=question_type.instruction_text,
        columns=columns,
    )
    return _json_response(200, question_set.to_dict())


def handle_question_types() -> tuple[int, dict[str, str], str]:
    return _json_response(200, {"types": list_question_types()})
