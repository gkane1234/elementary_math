"""Spec-driven Calc 1 integral generators (trick pipeline + construct_pfd)."""

from __future__ import annotations

from typing import Callable

from ..core.models import Question
from .utils import _make_questions


def _framework_generator(generator_key: str):
    def _gen(topic: str, settings: dict) -> list[Question]:
        from question_engine.frameworks.primitives.integrals import (
            sample_integral_expression,
        )

        count = int(settings.get("count", 10))
        include_answer_key = bool(settings.get("include_answer_key", False))
        label = {
            "integral_power_rule": "power rule integral",
            "integral_trigonometric": "trigonometric integral",
            "integral_log_exp": "log/exp integral",
            "integral_inverse_trig": "inverse trig integral",
            "integral_substitution": "substitution integral",
            "integral_definite_substitution": "definite substitution integral",
            "integral_trig_substitution": "trig substitution integral",
            "integral_log_exp_substitution": "log/exp substitution integral",
            "integral_invtrig_substitution": "invtrig substitution integral",
            "integration_by_parts": "integration by parts",
            "integral_partial_fractions": "partial fractions integral",
            "integral_multi_trick": "multi-trick integral",
            "integral_general": "general integral",
            "first_fundamental_theorem": "first fundamental theorem",
            "second_fundamental_theorem": "second fundamental theorem",
        }.get(generator_key, "integral")

        def build() -> tuple[str, str, str | None]:
            sample = sample_integral_expression(
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
    "integral_power_rule": _framework_generator("integral_power_rule"),
    "integral_trigonometric": _framework_generator("integral_trigonometric"),
    "integral_log_exp": _framework_generator("integral_log_exp"),
    "integral_inverse_trig": _framework_generator("integral_inverse_trig"),
    "integral_substitution": _framework_generator("integral_substitution"),
    "integral_definite_substitution": _framework_generator(
        "integral_definite_substitution"
    ),
    "integral_trig_substitution": _framework_generator("integral_trig_substitution"),
    "integral_log_exp_substitution": _framework_generator(
        "integral_log_exp_substitution"
    ),
    "integral_invtrig_substitution": _framework_generator(
        "integral_invtrig_substitution"
    ),
    "integration_by_parts": _framework_generator("integration_by_parts"),
    "integral_partial_fractions": _framework_generator("integral_partial_fractions"),
    "integral_multi_trick": _framework_generator("integral_multi_trick"),
    "integral_general": _framework_generator("integral_general"),
    "first_fundamental_theorem": _framework_generator("first_fundamental_theorem"),
    "second_fundamental_theorem": _framework_generator("second_fundamental_theorem"),
}
