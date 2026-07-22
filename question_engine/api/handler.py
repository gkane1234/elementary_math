import json
import os
import sys
from typing import Any

from ..core.base import QUESTION_TYPES, list_question_types
from ..utils.instruction_latex import repair_instruction_latex
from ..utils.layout import resolve_column_count
from ..core.models import Question, QuestionSet
from ..settings.presets import apply_difficulty_presets, resolve_setting_profile_for_type


def _json_response(status: int, body: dict[str, Any]) -> tuple[int, dict[str, str], str]:
    return status, {"Content-Type": "application/json"}, json.dumps(body)


def _log_generated_enabled() -> bool:
    """Log each generated question to stderr. Off with QE_LOG_GENERATED=0/false/off."""
    raw = os.environ.get("QE_LOG_GENERATED", "1").strip().lower()
    return raw not in {"0", "false", "no", "off"}


def _difficulty_label(settings: dict[str, Any]) -> str | None:
    tier = settings.get("difficulty_tier")
    difficulty = settings.get("difficulty")
    if tier is not None and str(tier).strip():
        if difficulty is not None and str(difficulty).strip():
            return f"{tier} (d={difficulty})"
        return str(tier)
    if difficulty is not None and str(difficulty).strip():
        return str(difficulty)
    return None


def _log_generated_questions(
    type_id: str,
    settings: dict[str, Any],
    questions: list[Question],
) -> None:
    if not _log_generated_enabled() or not questions:
        return
    difficulty = _difficulty_label(settings)
    sep = "=" * 56
    for index, question in enumerate(questions, start=1):
        lines = [
            sep,
            f"GENERATED [{index}/{len(questions)}]",
            f"topic: {type_id}",
        ]
        if difficulty:
            lines.append(f"difficulty: {difficulty}")
        lines.append("prompt:")
        lines.append(question.prompt_latex or "")
        if question.answer_latex:
            lines.append("answer:")
            lines.append(question.answer_latex)
        # Pedagogy QA flags (e.g. nonclassroom_factor_step).
        qa_flags = None
        if question.metadata:
            qa_flags = question.metadata.get("qa_flags")
            if not qa_flags:
                solution = question.metadata.get("solution")
                if isinstance(solution, dict):
                    qa_flags = solution.get("qa_flags")
        if qa_flags:
            lines.append("qa_flags:")
            lines.append(", ".join(str(f) for f in qa_flags))
            details = (
                question.metadata.get("qa_flag_details") if question.metadata else None
            )
            if not details and question.metadata:
                solution = question.metadata.get("solution")
                if isinstance(solution, dict):
                    details = solution.get("qa_flag_details")
            if details:
                for detail in details:
                    if isinstance(detail, dict):
                        role = detail.get("role") or "?"
                        deg = detail.get("degree")
                        latex = detail.get("latex") or ""
                        lines.append(f"  - {role} (deg={deg}): {latex}")
        # Optional show-steps experiment: student-order LaTeX on metadata.
        raw_steps = question.metadata.get("solution_steps") if question.metadata else None
        if not raw_steps and question.metadata:
            solution = question.metadata.get("solution")
            if isinstance(solution, dict):
                raw_steps = solution.get("solution_steps")
                if not raw_steps:
                    gen = solution.get("generation_steps") or []
                    raw_steps = list(reversed(gen))
        if raw_steps:
            lines.append("steps:")
            for step_index, step in enumerate(raw_steps, start=1):
                if isinstance(step, dict):
                    latex = step.get("latex") or ""
                else:
                    latex = str(step)
                lines.append(f"Step {step_index}: {latex}")
        lines.append(sep)
        print("\n".join(lines), file=sys.stderr, flush=True)


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
    annotated = _annotate_questions(questions, question_type, resolved)
    _log_generated_questions(type_id, resolved, annotated)
    return annotated


def handle_generate(body: dict[str, Any]) -> tuple[int, dict[str, str], str]:
    title = body.get("title") or "Worksheet"
    worksheet_settings = body.get("worksheet_settings", {})
    sections = body.get("sections")

    try:
        return _handle_generate_body(title, worksheet_settings, sections, body)
    except Exception as error:  # noqa: BLE001 — surface generator failures to the client
        return _json_response(500, {"error": str(error) or "Generation failed"})


def _handle_generate_body(
    title: str,
    worksheet_settings: dict[str, Any],
    sections: Any,
    body: dict[str, Any],
) -> tuple[int, dict[str, str], str]:
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
