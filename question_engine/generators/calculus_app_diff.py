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


def _optimization_applied(topic: str, settings: dict) -> list[Question]:
    """Optimization via OpenStax §4.7 frames; stamps live-loop form_id / generator."""
    from question_engine.frameworks.primitives.calc_app_diff import sample_app_diff
    from question_engine.frameworks.primitives.optimization_frames import (
        OPTIMIZATION_GENERATOR,
    )

    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        item = sample_app_diff("optimization", settings, rng=random)
        fid = item.form_id
        snap = item.metadata.get("spec_snapshot")
        build._last_meta = {  # type: ignore[attr-defined]
            **item.metadata,
            "form_id": fid,
            "family": fid,
            "generator": OPTIMIZATION_GENERATOR,
            "frame_id": fid,
            "spec_snapshot": {
                **(snap if isinstance(snap, dict) else {}),
                "form_id": fid,
                "family": fid,
                "generator": OPTIMIZATION_GENERATOR,
            },
        }
        answer = item.answer_latex if include_answer_key else None
        return item.prompt_latex, item.label, answer

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


def _intervals_increase_decrease(topic: str, settings: dict) -> list[Question]:
    """First-derivative sign chart; stamps live-loop form_id / generator."""
    from question_engine.frameworks.primitives.calc_app_diff import (
        INCREASE_DECREASE_GENERATOR,
        sample_app_diff,
    )

    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        item = sample_app_diff("increase_decrease", settings, rng=random)
        fid = item.form_id
        snap = item.metadata.get("spec_snapshot")
        build._last_meta = {  # type: ignore[attr-defined]
            **item.metadata,
            "form_id": fid,
            "family": fid,
            "generator": INCREASE_DECREASE_GENERATOR,
            "spec_snapshot": {
                **(snap if isinstance(snap, dict) else {}),
                "form_id": fid,
                "family": fid,
                "generator": INCREASE_DECREASE_GENERATOR,
            },
        }
        answer = item.answer_latex if include_answer_key else None
        return item.prompt_latex, item.label, answer

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


def _intervals_concavity(topic: str, settings: dict) -> list[Question]:
    """Second-derivative sign chart; stamps live-loop form_id / generator."""
    from question_engine.frameworks.primitives.calc_app_diff import (
        CONCAVITY_GENERATOR,
        sample_app_diff,
    )

    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        item = sample_app_diff("concavity", settings, rng=random)
        fid = item.form_id
        snap = item.metadata.get("spec_snapshot")
        build._last_meta = {  # type: ignore[attr-defined]
            **item.metadata,
            "form_id": fid,
            "family": fid,
            "generator": CONCAVITY_GENERATOR,
            "spec_snapshot": {
                **(snap if isinstance(snap, dict) else {}),
                "form_id": fid,
                "family": fid,
                "generator": CONCAVITY_GENERATOR,
            },
        }
        answer = item.answer_latex if include_answer_key else None
        return item.prompt_latex, item.label, answer

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


def _mean_value_theorem(topic: str, settings: dict) -> list[Question]:
    """MVT find-c; stamps live-loop form_id / generator."""
    from question_engine.frameworks.primitives.calc_app_diff import (
        MVT_GENERATOR,
        sample_app_diff,
    )

    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        item = sample_app_diff("mean_value", settings, rng=random)
        fid = item.form_id
        snap = item.metadata.get("spec_snapshot")
        build._last_meta = {  # type: ignore[attr-defined]
            **item.metadata,
            "form_id": fid,
            "family": fid,
            "generator": MVT_GENERATOR,
            "spec_snapshot": {
                **(snap if isinstance(snap, dict) else {}),
                "form_id": fid,
                "family": fid,
                "generator": MVT_GENERATOR,
            },
        }
        answer = item.answer_latex if include_answer_key else None
        return item.prompt_latex, item.label, answer

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


def _rolles_theorem(topic: str, settings: dict) -> list[Question]:
    """Rolle find-c; stamps live-loop form_id / generator."""
    from question_engine.frameworks.primitives.calc_app_diff import (
        ROLLES_GENERATOR,
        sample_app_diff,
    )

    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        item = sample_app_diff("rolles", settings, rng=random)
        fid = item.form_id
        snap = item.metadata.get("spec_snapshot")
        build._last_meta = {  # type: ignore[attr-defined]
            **item.metadata,
            "form_id": fid,
            "family": fid,
            "generator": ROLLES_GENERATOR,
            "spec_snapshot": {
                **(snap if isinstance(snap, dict) else {}),
                "form_id": fid,
                "family": fid,
                "generator": ROLLES_GENERATOR,
            },
        }
        answer = item.answer_latex if include_answer_key else None
        return item.prompt_latex, item.label, answer

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


def _curve_sketching(topic: str, settings: dict) -> list[Question]:
    """Vertex / extrema / inflection checklist; stamps live-loop form_id / generator."""
    from question_engine.frameworks.primitives.calc_app_diff import (
        CURVE_SKETCH_GENERATOR,
        sample_app_diff,
    )

    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        item = sample_app_diff("curve_sketching", settings, rng=random)
        fid = item.form_id
        snap = item.metadata.get("spec_snapshot")
        build._last_meta = {  # type: ignore[attr-defined]
            **item.metadata,
            "form_id": fid,
            "family": fid,
            "generator": CURVE_SKETCH_GENERATOR,
            "spec_snapshot": {
                **(snap if isinstance(snap, dict) else {}),
                "form_id": fid,
                "family": fid,
                "generator": CURVE_SKETCH_GENERATOR,
            },
        }
        answer = item.answer_latex if include_answer_key else None
        return item.prompt_latex, item.label, answer

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


def _relative_extrema(topic: str, settings: dict) -> list[Question]:
    """First-derivative extrema; stamps live-loop form_id / generator."""
    from question_engine.frameworks.primitives.calc_app_diff import (
        RELATIVE_EXTREMA_GENERATOR,
        sample_app_diff,
    )

    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        item = sample_app_diff("relative_extrema", settings, rng=random)
        fid = item.form_id
        snap = item.metadata.get("spec_snapshot")
        build._last_meta = {  # type: ignore[attr-defined]
            **item.metadata,
            "form_id": fid,
            "family": fid,
            "generator": RELATIVE_EXTREMA_GENERATOR,
            "spec_snapshot": {
                **(snap if isinstance(snap, dict) else {}),
                "form_id": fid,
                "family": fid,
                "generator": RELATIVE_EXTREMA_GENERATOR,
            },
        }
        answer = item.answer_latex if include_answer_key else None
        return item.prompt_latex, item.label, answer

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


GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = {
    "relative_extrema": _relative_extrema,
    "absolute_extrema": _framework("absolute_extrema", "absolute extrema"),
    "intervals_concavity": _intervals_concavity,
    "mean_value_theorem": _mean_value_theorem,
    "rolles_theorem": _rolles_theorem,
    "newtons_method": _framework("newtons_method", "Newton's method"),
    "motion_along_a_line": _framework("motion", "motion along a line"),
    "motion_along_a_line_integral": _framework(
        "motion_integral", "motion (integral)"
    ),
    "de_introduction": _framework("de_intro", "DE introduction"),
    "optimization_applied": _optimization_applied,
    "intervals_increase_decrease": _intervals_increase_decrease,
    "curve_sketching": _curve_sketching,
    "graphical_f_fp": _framework("graphical_f_fp", "graphs of f and f'"),
    "related_rates_simple": _related_rates_simple,
}
