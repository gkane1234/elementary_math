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
            meta = dict(item.metadata)
            meta["form_id"] = item.form_id
            meta["family"] = item.form_id
            meta.setdefault("frame_id", item.form_id)
            build._last_meta = meta  # type: ignore[attr-defined]
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


def _related_rates_simple(topic: str, settings: dict) -> list[Question]:
    """Related rates via OpenStax §4.1 frames; stamps live-loop form_id / generator."""
    from question_engine.frameworks.primitives.calc_app_diff import sample_app_diff
    from question_engine.frameworks.primitives.related_rates_frames import (
        RELATED_RATES_GENERATOR,
    )

    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        item = sample_app_diff("related_rates", settings, rng=random)
        fid = item.form_id
        snap = item.metadata.get("spec_snapshot")
        build._last_meta = {  # type: ignore[attr-defined]
            **item.metadata,
            "form_id": fid,
            "family": fid,
            "generator": RELATED_RATES_GENERATOR,
            "frame_id": fid,
            "related_rates_frame": fid,
            "spec_snapshot": {
                **(snap if isinstance(snap, dict) else {}),
                "form_id": fid,
                "family": fid,
                "generator": RELATED_RATES_GENERATOR,
            },
        }
        answer = item.answer_latex if include_answer_key else None
        return item.prompt_latex, item.label, answer

    def _sketch_meta(prompt_latex: str, prompt_text: str, answer: str | None) -> dict:
        from question_engine.diagrams.figure_families import sample_figure_from_settings

        sample = sample_figure_from_settings(
            "function_sketch",
            settings,
            features=["curve", "related_rates_circle", "related_rates_ladder"],
            curve_kind="parabola",
        )
        extras = sample.to_metadata_extras()
        extras.update(getattr(build, "_last_meta", {}) or {})
        return extras

    return _make_questions(
        topic,
        count,
        include_answer_key,
        build,
        metadata_builder=_sketch_meta,
        settings=settings,
    )


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
    "related_rates_simple": _related_rates_simple,
}
