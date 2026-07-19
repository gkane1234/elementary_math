"""Polynomial-family generators on shared primitives (ExpressionPolicy max_degree≥2).

Overrides legacy basic/misc polynomial keys via last-wins in ``generators/__init__.py``.
"""

from __future__ import annotations

from typing import Any, Callable

from question_engine.core.models import Question
from question_engine.frameworks.primitives import (
    PRIM_EVALUATE,
    PRIM_EXPAND_SIMPLIFY,
    PRIM_FACTOR_GCF,
    PRIM_LIKE_TERMS,
    PRIM_NUMBERS,
    PRIM_VARIABLE,
    build_context,
)
from question_engine.frameworks.primitives.evaluate import sample_evaluate_expression
from question_engine.frameworks.primitives.expand_simplify import sample_expand_simplify
from question_engine.frameworks.primitives.expression_policy import polynomial_policy
from question_engine.frameworks.primitives.factor_gcf import sample_factor_gcf
from question_engine.frameworks.primitives.factor_poly import (
    PRIM_FACTOR_POLY,
    sample_factoring_grouping,
    sample_quadratic_factoring,
    sample_special_factoring,
)
from question_engine.frameworks.primitives.like_terms import sample_like_terms
from question_engine.frameworks.primitives.polynomials import (
    PRIM_POLYNOMIALS,
    sample_polynomial_add_subtract,
    sample_polynomial_multiply,
    sample_polynomial_naming,
)
from question_engine.generators.utils import make_questions


def _meta_builder(last: dict[str, Any]):
    def metadata_builder(_p: str, _t: str, _a: str | None) -> dict[str, Any]:
        return dict(last.get("meta") or {})

    return metadata_builder


def _poly_settings(settings: dict) -> dict[str, Any]:
    local = dict(settings)
    local.setdefault("integers_only", True)
    local.setdefault("expression_family", "polynomial")
    md = int(local.get("max_degree", local.get("poly_max_degree", 3)))
    local["max_degree"] = md
    return local


def _policy_from(settings: dict):
    md = int(settings.get("max_degree", 3))
    return polynomial_policy(max_degree=md)


def polynomial_naming(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}
    local = _poly_settings(settings)

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            local,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_POLYNOMIALS],
            policy=_policy_from(local),
            leaf_id="polynomial_naming",
        )
        item = sample_polynomial_naming(ctx)
        answer = item.answer_latex if include_answer_key else None
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "polynomial_naming",
            "degree": item.degree,
            "leading_coeff": str(item.leading_coeff),
            "n_terms": item.n_terms,
            "upgrades": list(item.upgrades),
        }
        return (
            f"\\text{{Name the polynomial: }} {item.latex}",
            f"Name the polynomial: {item.text}",
            answer,
        )

    return make_questions(
        topic, count, include_answer_key, build,
        metadata_builder=_meta_builder(last), settings=settings,
    )


def polynomial_add_subtract(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}
    local = _poly_settings(settings)

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            local,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_POLYNOMIALS],
            policy=_policy_from(local),
            leaf_id="polynomial_add_subtract",
        )
        item = sample_polynomial_add_subtract(ctx)
        answer = item.simplified_latex if include_answer_key else None
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "polynomial_add_subtract",
            "degree": item.degree,
            "op": item.op,
            "upgrades": list(item.upgrades),
        }
        return (
            f"\\text{{Simplify: }} {item.latex}",
            f"Simplify: {item.text}",
            answer,
        )

    return make_questions(
        topic, count, include_answer_key, build,
        metadata_builder=_meta_builder(last), settings=settings,
    )


def polynomial_multiply(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}
    local = _poly_settings(settings)

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            local,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_POLYNOMIALS],
            policy=_policy_from(local),
            leaf_id="polynomial_multiply",
        )
        item = sample_polynomial_multiply(ctx, special=False)
        answer = item.product_latex if include_answer_key else None
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "polynomial_multiply",
            "degree": item.degree,
            "pattern": item.pattern,
            "left_terms": item.left_terms,
            "right_terms": item.right_terms,
            "upgrades": list(item.upgrades),
        }
        return (
            f"\\text{{Multiply: }} {item.latex}",
            f"Multiply: {item.text}",
            answer,
        )

    return make_questions(
        topic, count, include_answer_key, build,
        metadata_builder=_meta_builder(last), settings=settings,
    )


def polynomial_multiply_special(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}
    local = _poly_settings(settings)

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            local,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_POLYNOMIALS],
            policy=_policy_from(local),
            leaf_id="polynomial_multiply_special",
        )
        item = sample_polynomial_multiply(ctx, special=True)
        answer = item.product_latex if include_answer_key else None
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "polynomial_multiply_special",
            "degree": item.degree,
            "pattern": item.pattern,
            "upgrades": list(item.upgrades),
        }
        return (
            f"\\text{{Multiply: }} {item.latex}",
            f"Multiply: {item.text}",
            answer,
        )

    return make_questions(
        topic, count, include_answer_key, build,
        metadata_builder=_meta_builder(last), settings=settings,
    )


def evaluate_polynomial(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}
    local = _poly_settings(settings)

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            local,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_EVALUATE],
            policy=_policy_from(local),
            leaf_id="evaluate_polynomial",
        )
        expr = sample_evaluate_expression(ctx)
        answer = expr.value_latex if include_answer_key else None
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "evaluate_polynomial",
            "max_degree": expr.max_degree,
            "upgrades": list(expr.upgrades),
            "n_terms": expr.n_terms,
        }
        return (
            (
                f"\\text{{Evaluate }} {expr.latex} "
                f"\\text{{ when }} {expr.var_latex} = {expr.subst_latex}"
            ),
            f"Evaluate {expr.text} when {expr.var_name} = {expr.subst_latex}",
            answer,
        )

    return make_questions(
        topic, count, include_answer_key, build,
        metadata_builder=_meta_builder(last), settings=settings,
    )


def poly_combine_like_terms(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}
    local = _poly_settings(settings)

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            local,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_LIKE_TERMS],
            policy=_policy_from(local),
            leaf_id="poly_combine_like_terms",
        )
        expr = sample_like_terms(ctx)
        answer = expr.simplified_latex if include_answer_key else None
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "poly_like_terms",
            "max_degree": expr.max_degree,
            "upgrades": list(expr.upgrades),
        }
        return (
            f"\\text{{Simplify: }} {expr.latex}",
            f"Simplify: {expr.text}",
            answer,
        )

    return make_questions(
        topic, count, include_answer_key, build,
        metadata_builder=_meta_builder(last), settings=settings,
    )


def poly_expand_simplify(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}
    local = _poly_settings(settings)

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            local,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_EXPAND_SIMPLIFY],
            policy=_policy_from(local),
            leaf_id="poly_expand_simplify",
        )
        expr = sample_expand_simplify(ctx)
        answer = expr.simplified_latex if include_answer_key else None
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "poly_expand_simplify",
            "max_degree": expr.max_degree,
            "upgrades": list(expr.upgrades),
            "n_groups": expr.n_groups,
        }
        return (
            f"\\text{{Expand and simplify: }} {expr.latex}",
            f"Expand and simplify: {expr.text}",
            answer,
        )

    return make_questions(
        topic, count, include_answer_key, build,
        metadata_builder=_meta_builder(last), settings=settings,
    )


def factor_gcf_poly(topic: str, settings: dict) -> list[Question]:
    """Poly leaf: same GCF engine, polynomial ExpressionPolicy (may emit x^2)."""
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}
    local = _poly_settings(settings)

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            local,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_FACTOR_GCF],
            policy=_policy_from(local),
            leaf_id="polynomial_factoring_common_factor",
        )
        expr = sample_factor_gcf(ctx)
        answer = expr.factored_latex if include_answer_key else None
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "factor_gcf",
            "upgrades": list(expr.upgrades),
            "gcf": expr.gcf_latex,
            "max_degree": expr.max_degree,
        }
        return (
            f"\\text{{Factor: }} {expr.latex}",
            f"Factor: {expr.text}",
            answer,
        )

    return make_questions(
        topic, count, include_answer_key, build,
        metadata_builder=_meta_builder(last), settings=settings,
    )


def quadratic_factoring(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}
    local = _poly_settings(settings)
    local["max_degree"] = min(2, int(local.get("max_degree", 2)))

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            local,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_FACTOR_POLY],
            policy=polynomial_policy(max_degree=2),
            leaf_id="quadratic_factoring",
        )
        item = sample_quadratic_factoring(ctx)
        answer = item.factored_latex if include_answer_key else None
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "quadratic_factoring",
            "method": item.method,
            "degree": item.degree,
            "upgrades": list(item.upgrades),
        }
        return (
            f"\\text{{Factor: }} {item.latex}",
            f"Factor: {item.text}",
            answer,
        )

    return make_questions(
        topic, count, include_answer_key, build,
        metadata_builder=_meta_builder(last), settings=settings,
    )


def polynomial_factoring_special_cases(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}
    local = _poly_settings(settings)

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            local,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_FACTOR_POLY],
            policy=_policy_from(local),
            leaf_id="polynomial_factoring_special_cases",
        )
        item = sample_special_factoring(ctx)
        answer = item.factored_latex if include_answer_key else None
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "polynomial_factoring_special_cases",
            "method": item.method,
            "degree": item.degree,
            "upgrades": list(item.upgrades),
        }
        return (
            f"\\text{{Factor: }} {item.latex}",
            f"Factor: {item.text}",
            answer,
        )

    return make_questions(
        topic, count, include_answer_key, build,
        metadata_builder=_meta_builder(last), settings=settings,
    )


def polynomial_factoring_grouping(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}
    local = _poly_settings(settings)

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            local,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_FACTOR_POLY],
            policy=_policy_from(local),
            leaf_id="polynomial_factoring_grouping",
        )
        item = sample_factoring_grouping(ctx)
        answer = item.factored_latex if include_answer_key else None
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "polynomial_factoring_grouping",
            "method": item.method,
            "degree": item.degree,
            "upgrades": list(item.upgrades),
        }
        return (
            f"\\text{{Factor: }} {item.latex}",
            f"Factor: {item.text}",
            answer,
        )

    return make_questions(
        topic, count, include_answer_key, build,
        metadata_builder=_meta_builder(last), settings=settings,
    )


GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = {
    "polynomial_naming": polynomial_naming,
    "a2_polynomial_functions_naming": polynomial_naming,
    "polynomial_add_subtract": polynomial_add_subtract,
    "pa_polynomials_adding_and_subtracting": polynomial_add_subtract,
    "a2_polynomial_functions_adding_and_subtracting": polynomial_add_subtract,
    "polynomial_multiply": polynomial_multiply,
    "pa_polynomials_multiplying": polynomial_multiply,
    "a2_polynomial_functions_multiplying": polynomial_multiply,
    "polynomial_multiply_special": polynomial_multiply_special,
    "a2_polynomial_functions_multiplying_special_cases": polynomial_multiply_special,
    "evaluate_polynomial": evaluate_polynomial,
    "poly_combine_like_terms": poly_combine_like_terms,
    "poly_expand_simplify": poly_expand_simplify,
    "polynomial_factoring_common_factor": factor_gcf_poly,
    "quadratic_factoring": quadratic_factoring,
    "a2_quadratic_functions_and_inequalities_factoring_quadratic_expressions": quadratic_factoring,
    "a2_polynomial_functions_factoring_quadratic_form": quadratic_factoring,
    "polynomial_factoring_special_cases": polynomial_factoring_special_cases,
    "a2_quadratic_functions_and_inequalities_factoring_special_case_quadratic_expressions": (
        polynomial_factoring_special_cases
    ),
    "polynomial_factoring_grouping": polynomial_factoring_grouping,
    "a2_polynomial_functions_factoring_by_grouping": polynomial_factoring_grouping,
    "a2_polynomial_functions_factoring_all_techniques": polynomial_factoring_grouping,
}
