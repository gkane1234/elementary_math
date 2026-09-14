"""Dedicated Calc-1 apps-of-diff / DE-intro generators (not calculus_foundations)."""

from __future__ import annotations

import random
from typing import Callable

from ..core.models import Question
from .utils import _make_questions


def _framework(kind: str, label: str):
    def _gen(topic: str, settings: dict) -> list[Question]:
        from question_engine.frameworks.primitives.calc_app_diff import sample_app_diff

        count = int(settings.get("count", 10))
        include_answer_key = bool(settings.get("include_answer_key", False))

        def build() -> tuple[str, str, str | None]:
            item = sample_app_diff(kind, settings, rng=random)  # type: ignore[arg-type]
            build._last_meta = {  # type: ignore[attr-defined]
                "form_id": item.form_id,
                "family": item.form_id,
                "frame_id": item.metadata.get("frame_id") or item.form_id,
                **item.metadata,
            }
            answer = item.answer_latex if include_answer_key else None
            return item.prompt_latex, label, answer

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
    "relative_extrema": _framework("relative_extrema", "relative extrema"),
    "absolute_extrema": _framework("absolute_extrema", "absolute extrema"),
    "intervals_concavity": _framework("concavity", "concavity"),
    "newtons_method": _framework("newtons_method", "Newton's method"),
    "motion_along_a_line": _framework("motion", "motion along a line"),
    "motion_along_a_line_integral": _framework(
        "motion_integral", "motion (integral)"
    ),
    "de_introduction": _framework("de_intro", "DE introduction"),
    "optimization_applied": _framework("optimization", "optimization"),
    "curve_sketching": _framework("curve_sketching", "curve sketching"),
    "graphical_f_fp": _framework("graphical_f_fp", "graphs of f and f'"),
}
