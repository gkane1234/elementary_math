"""Rational + PFD generators on the constructive spine (L2–L4)."""

from __future__ import annotations

from typing import Any

from question_engine.core.models import Question
from question_engine.frameworks.primitives import (
    PRIM_NUMBERS,
    PRIM_VARIABLE,
    build_context,
)
from question_engine.frameworks.primitives.constructive import (
    construct_pfd,
    construct_rational_sum,
)
from question_engine.frameworks.primitives.expression_policy import POLYNOMIAL_POLICY_DEFAULT
from question_engine.frameworks.primitives.rational_cancel import resolve_rational_cancel_count
from question_engine.generators.utils import make_questions


def _meta_builder(last: dict[str, Any]):
    def metadata_builder(_p: str, _t: str, _a: str | None) -> dict[str, Any]:
        return dict(last.get("meta") or {})

    return metadata_builder


def _rational_ctx(settings: dict):
    return build_context(
        settings,
        [PRIM_NUMBERS, PRIM_VARIABLE],
        policy=POLYNOMIAL_POLICY_DEFAULT,
        leaf_id=str(settings.get("_leaf_id") or settings.get("type_id") or ""),
    )


def rational_add_subtract(topic: str, settings: dict) -> list[Question]:
    """L3: add/subtract rational expressions (constructive combine + cancel)."""
    from question_engine.frameworks.primitives.rational_cancel import (
        apply_continuous_rational_structure,
    )

    settings = apply_continuous_rational_structure(settings)
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}

    def build() -> tuple[str, str, str | None]:
        ctx = _rational_ctx(settings)
        k = resolve_rational_cancel_count(settings, d=ctx.topic_d, rng=ctx.rng)
        n_terms = int(settings["term_count"]) if settings.get("term_count") is not None else None
        surface = construct_rational_sum(
            ctx, d=ctx.topic_d, cancel_count=k, as_sum=True, n_terms=n_terms
        )
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "constructive_rational",
            "level": surface.level,
            "cancel_factor_count": surface.metadata.get("cancel_factor_count", k),
            "n_terms": surface.metadata.get("n_terms"),
            "excluded_values": surface.metadata.get("excluded_values") or [],
            "constructive": surface.metadata,
        }
        answer = surface.simplified_latex if include_answer_key else None
        return (
            rf"\text{{Combine and simplify: }} {surface.latex}",
            f"Combine and simplify: {surface.text}",
            answer,
        )

    return make_questions(
        topic,
        count,
        include_answer_key,
        build,
        metadata_builder=_meta_builder(last),
        settings=settings,
    )


def rational_simplify(topic: str, settings: dict) -> list[Question]:
    """L2: simplify a rational with planned cancellation."""
    from question_engine.frameworks.primitives.rational_cancel import (
        apply_continuous_rational_structure,
    )

    settings = apply_continuous_rational_structure(settings)
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}

    def build() -> tuple[str, str, str | None]:
        ctx = _rational_ctx(settings)
        k = resolve_rational_cancel_count(settings, d=ctx.topic_d, rng=ctx.rng)
        surface = construct_rational_sum(
            ctx, d=ctx.topic_d, cancel_count=k, as_sum=False
        )
        actual_k = surface.metadata.get("cancel_factor_count", k)
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "constructive_rational",
            "level": surface.level,
            "cancel_factor_count": actual_k,
            "excluded_values": surface.metadata.get("excluded_values") or [],
            "constructive": surface.metadata,
        }
        answer = surface.simplified_latex if include_answer_key else None
        return (
            rf"\text{{Simplify: }} {surface.latex}",
            f"Simplify: {surface.text}",
            answer,
        )

    return make_questions(
        topic,
        count,
        include_answer_key,
        build,
        metadata_builder=_meta_builder(last),
        settings=settings,
    )


def partial_fraction_decomposition(topic: str, settings: dict) -> list[Question]:
    """L4: seed PF answer, combine to single rational prompt."""
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}

    def build() -> tuple[str, str, str | None]:
        ctx = _rational_ctx(settings)
        surface = construct_pfd(ctx, d=ctx.topic_d)
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "constructive_pfd",
            "level": surface.level,
            "constructive": surface.metadata,
        }
        answer = surface.simplified_latex if include_answer_key else None
        return (
            rf"\text{{Decompose }} {surface.latex}",
            f"Decompose {surface.text}",
            answer,
        )

    return make_questions(
        topic,
        count,
        include_answer_key,
        build,
        metadata_builder=_meta_builder(last),
        settings=settings,
    )


GENERATORS = {
    "rational_expression_simplification": rational_add_subtract,
    "a2_rational_expressions_adding_and_subtracting": rational_add_subtract,
    "rational_expressions_adding_and_subtracting": rational_add_subtract,
    "rational_simplification": rational_simplify,
    "a2_rational_expressions_simplifying": rational_simplify,
    "rational_expressions_simplifying": rational_simplify,
    "partial_fraction_decomposition": partial_fraction_decomposition,
    "pc_partial_fraction_decomposition": partial_fraction_decomposition,
}
