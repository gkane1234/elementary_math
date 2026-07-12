import json
from typing import Any

from ..core.base import QUESTION_TYPES, list_question_types
from ..utils.instruction_latex import repair_instruction_latex
from ..utils.layout import resolve_column_count
from ..core.models import Question, QuestionSet
from ..settings.presets import apply_difficulty_presets, resolve_setting_profile_for_type


def _json_response(status: int, body: dict[str, Any]) -> tuple[int, dict[str, str], str]:
    return status, {"Content-Type": "application/json"}, json.dumps(body)


def _settings_for_regeneration(settings: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in settings.items() if key not in {"count", "max_columns"}}


def _resolve_generation_settings(type_id: str, settings: dict[str, Any]) -> dict[str, Any]:
    profile = resolve_setting_profile_for_type(type_id)
    question_type = QUESTION_TYPES.get(type_id)
    merged = dict(settings)
    if question_type is not None:
        config = getattr(question_type, "_setting_config", None)
        if profile is None:
            profile = getattr(question_type, "setting_profile", None)
            if profile is None and config is not None:
                profile = getattr(config, "setting_profile", None)
        # Schema defaults (e.g. include_graph_metadata) apply when the client
        # omits them — explicit request settings still win.
        defaults = getattr(config, "setting_defaults", None) if config is not None else None
        if defaults:
            merged = {**defaults, **merged}
    return apply_difficulty_presets(merged, type_id=type_id, setting_profile=profile)


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
            "instruction_latex": repair_instruction_latex(question_type.instruction_latex),
        }
    return questions


def _generate_for_type(type_id: str, settings: dict[str, Any]) -> list[Question]:
    question_type = QUESTION_TYPES.get(type_id)
    if question_type is None:
        raise ValueError(f"Unknown question type: {type_id}")

    resolved = _resolve_generation_settings(type_id, settings)
    questions = question_type.generate(resolved)
    return _annotate_questions(questions, question_type, resolved)


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
        instruction_latex=repair_instruction_latex(question_type.instruction_latex),
        instruction_text=question_type.instruction_text,
        columns=columns,
    )
    return _json_response(200, question_set.to_dict())


def handle_question_types() -> tuple[int, dict[str, str], str]:
    return _json_response(200, {"types": list_question_types()})
