"""Spec-driven Calc 1 limit generators (override thin Mad-Libs / stubs)."""

from __future__ import annotations

from typing import Callable

from ..core.models import Question
from .utils import _make_questions


def _framework_generator(generator_key: str):
    def _gen(topic: str, settings: dict) -> list[Question]:
        from question_engine.frameworks.primitives.limits import sample_limit_expression

        count = int(settings.get("count", 10))
        include_answer_key = bool(settings.get("include_answer_key", False))
        label = {
            "limit_direct_evaluation": "limit (direct)",
            "limit_at_infinity": "limit at infinity",
            "limit_removable": "removable discontinuity limit",
            "limit_jump": "jump discontinuity limit",
            "limit_essential": "essential discontinuity limit",
            "limit_continuity": "continuity classification",
            "lhopitals_rule": "L'Hôpital limit",
        }.get(generator_key, "limit")

        def build() -> tuple[str, str, str | None]:
            sample = sample_limit_expression(
                settings, generator_key=generator_key, topic=topic
            )
            build._last_meta = sample.as_metadata()  # type: ignore[attr-defined]
            answer = sample.answer_latex if include_answer_key else None
            return sample.prompt_latex, label, answer

        def metadata_builder(_p: str, _t: str, _a: str | None) -> dict:
            return dict(getattr(build, "_last_meta", {}) or {})

        return _make_questions(
            topic,
            count,
            include_answer_key,
            build,
            metadata_builder=metadata_builder,
            settings=settings,
        )

    return _gen


GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = {
    "limit_direct_evaluation": _framework_generator("limit_direct_evaluation"),
    "limit_at_infinity": _framework_generator("limit_at_infinity"),
    "limit_removable": _framework_generator("limit_removable"),
    "limit_jump": _framework_generator("limit_jump"),
    "limit_essential": _framework_generator("limit_essential"),
    "limit_continuity": _framework_generator("limit_continuity"),
    "lhopitals_rule": _framework_generator("lhopitals_rule"),
}
