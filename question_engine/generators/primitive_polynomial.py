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
from question_engine.frameworks.primitives.constructive import (
    ExpressionScope,
    construct_poly,
    verify_poly,
)
from question_engine.frameworks.primitives.evaluate import sample_evaluate_expression
from question_engine.frameworks.primitives.expand_simplify import sample_expand_simplify
from question_engine.frameworks.primitives.expression_policy import polynomial_policy
from question_engine.frameworks.primitives.factor_gcf import sample_factor_gcf
from question_engine.frameworks.primitives.factor_poly import (
    PRIM_FACTOR_POLY,
    sample_factoring_all_techniques,
    sample_factoring_grouping,
    sample_quadratic_factoring,
    sample_quadratic_form,
    sample_special_factoring,
    sample_sum_diff_cubes,
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


def simplify_polynomials(topic: str, settings: dict) -> list[Question]:
    """Answer-first: seed a PolynomialTarget, inflate via construct_poly, simplify.

    Thin course variants differ only via target constraints in settings:
    ``max_degree``, ``min_degree``, ``max_terms``, ``exact_terms``,
    ``prefer_single_hot``.
    """
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}
    local = _poly_settings(settings)
    max_degree = int(local.get("max_degree", 3))
    min_degree = int(local.get("min_degree", 2))
    max_terms = local.get("max_terms")
    exact_terms = local.get("exact_terms")
    if max_terms is not None:
        max_terms = int(max_terms)
    if exact_terms is not None:
        exact_terms = int(exact_terms)

    def _visibly_unsimplified(prompt: str, answer: str) -> bool:
        from packages.polynomial_core import normalize_expression_signs

        p = normalize_expression_signs(prompt or "").replace(" ", "")
        a = normalize_expression_signs(answer or "").replace(" ", "")
        return p != a

    def build() -> tuple[str, str, str | None]:
        from fractions import Fraction

        from question_engine.frameworks.primitives._algebra_render import (
            num_latex,
            sample_integerish,
        )
        from question_engine.frameworks.primitives.poly_helpers import (
            render_poly,
            scale_coeffs,
        )
        from question_engine.frameworks.primitives.presentation import (
            DisplayPiece,
            presentation_for_ctx,
            render_addition,
            render_product,
        )

        ctx = build_context(
            local,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_EXPAND_SIMPLIFY],
            policy=_policy_from(local),
            leaf_id=str(topic or "simplify_polynomials"),
        )
        d = float(ctx.topic_d)
        # D=0 may be almost-simplified; D>0 must look unsimplified.
        min_inflators = 0 if d <= 0 else 1
        prefer_single: bool | None = None
        if "prefer_single_hot" in local:
            prefer_single = bool(local["prefer_single_hot"])
        scope = ExpressionScope(
            max_degree=max(2, max_degree),
            min_degree=max(2, min_degree),
            prefer_single_hot=prefer_single,
            max_terms=max_terms,
            exact_terms=exact_terms,
        )
        surface = None
        for _ in range(12):
            candidate = construct_poly(
                ctx,
                d=d,
                scope=scope,
                prefer_distribute=True,
                min_inflators=min_inflators,
            )
            assert verify_poly(candidate, candidate.target)
            surface = candidate
            if d <= 0:
                break
            if _visibly_unsimplified(candidate.latex, candidate.simplified_latex or ""):
                break
            min_inflators = max(min_inflators + 1, 2)

        assert surface is not None

        # Last-resort classroom distribute wrap if inflate still looked simplified.
        if d > 0 and not _visibly_unsimplified(
            surface.latex, surface.simplified_latex or ""
        ):
            coeffs = dict(surface.poly_coeffs or {})
            v = ctx.sample_variable()
            style = presentation_for_ctx(ctx, d=d)
            k = sample_integerish(ctx, exclude_zero=True).value
            if abs(k) == 1:
                k = Fraction(ctx.rng.choice([2, 3, -2, -3]))
            deg = max(coeffs) if coeffs else 2
            lead = coeffs.get(deg, Fraction(1))
            if lead % k == 0 and all(c % k == 0 for c in coeffs.values()):
                inner = scale_coeffs(coeffs, Fraction(1) / k)
                rem: dict[int, Fraction] = {}
            else:
                inner = {deg: Fraction(1)}
                rem = dict(coeffs)
                rem[deg] = rem.get(deg, Fraction(0)) - k
                if rem[deg] == 0:
                    del rem[deg]
            inner_l, inner_t = render_poly(inner, v)
            k_l = num_latex(k)
            prod_l, prod_t = render_product(
                [
                    DisplayPiece(k_l, k_l),
                    DisplayPiece(f"\\left({inner_l}\\right)", f"({inner_t})"),
                ],
                style,
                ctx.rng,
            )
            if rem:
                rem_l, rem_t = render_poly(rem, v)
                latex, text = render_addition(
                    DisplayPiece(prod_l, prod_t),
                    DisplayPiece(rem_l, rem_t),
                    style,
                    ctx.rng,
                )
            else:
                latex, text = prod_l, prod_t
            from dataclasses import replace

            surface = replace(
                surface,
                latex=latex,
                text=text,
                inflators_applied=tuple(surface.inflators_applied) + ("force_distribute",),
            )

        answer = surface.simplified_latex if include_answer_key else None
        n_terms = len([c for c in (surface.poly_coeffs or {}).values() if c != 0])
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "construct_poly",
            "poly_degree": surface.metadata.get("poly_degree"),
            "n_hot_terms": surface.metadata.get("n_hot_terms"),
            "n_terms": n_terms,
            "single_hot": surface.metadata.get("single_hot"),
            "inflators": list(surface.inflators_applied),
            "constructive": surface.metadata,
            "target_constraints": {
                "max_degree": max_degree,
                "min_degree": min_degree,
                "max_terms": max_terms,
                "exact_terms": exact_terms,
                "prefer_single_hot": prefer_single,
            },
        }
        # Catalog instruction is "Simplify."; stem is the unsimplified expression.
        return (surface.latex, surface.text, answer)

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
            leaf_id=str(topic or "quadratic_factoring"),
        )
        item = sample_quadratic_factoring(ctx)
        answer = item.factored_latex if include_answer_key else None
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "quadratic_factoring",
            "method": item.method,
            "degree": item.degree,
            "upgrades": list(item.upgrades),
            "effective_d": item.effective_d,
        }
        # Catalog instruction is "Factor."; stem is the (maybe unsimplified) poly.
        return item.latex, item.text, answer

    return make_questions(
        topic, count, include_answer_key, build,
        metadata_builder=_meta_builder(last), settings=settings,
    )


def quadratic_factoring_equations(topic: str, settings: dict) -> list[Question]:
    """Solve by factoring — same factors-first ladder as quadratic_factoring."""
    from fractions import Fraction

    from question_engine.frameworks.primitives._algebra_render import num_latex
    from question_engine.frameworks.primitives.factor_poly import (
        sample_quadratic_equation_by_factoring,
    )

    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}
    local = _poly_settings(settings)
    local["max_degree"] = 2

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            local,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_FACTOR_POLY],
            policy=polynomial_policy(max_degree=2),
            leaf_id=str(topic or "quadratic_factoring_equations"),
        )
        item = sample_quadratic_equation_by_factoring(ctx)
        answer = None
        if include_answer_key:
            roots: list[Fraction] = []
            for fac in item.factor_coeffs:
                p = fac.get(1, Fraction(0))
                q = fac.get(0, Fraction(0))
                if p != 0:
                    roots.append(-q / p)
            # Deduplicate while sorting
            uniq = sorted(set(roots))
            answer = ", ".join(f"x = {num_latex(r)}" for r in uniq)
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "quadratic_factoring_equations",
            "method": item.method,
            "upgrades": list(item.upgrades),
            "effective_d": item.effective_d,
        }
        return item.latex, item.text, answer

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
        return item.latex, item.text, answer

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
            item.latex,
            item.text,
            answer,
        )

    return make_questions(
        topic, count, include_answer_key, build,
        metadata_builder=_meta_builder(last), settings=settings,
    )


def polynomial_factoring_sum_diff_cubes(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}
    local = _poly_settings(settings)
    local["max_degree"] = max(3, int(local.get("max_degree", 3)))

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            local,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_FACTOR_POLY],
            policy=polynomial_policy(max_degree=3),
            leaf_id=str(topic or "polynomial_factoring_sum_diff_cubes"),
        )
        item = sample_sum_diff_cubes(ctx)
        answer = item.factored_latex if include_answer_key else None
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "polynomial_factoring_sum_diff_cubes",
            "method": item.method,
            "degree": item.degree,
            "upgrades": list(item.upgrades),
            "effective_d": item.effective_d,
        }
        return item.latex, item.text, answer

    return make_questions(
        topic, count, include_answer_key, build,
        metadata_builder=_meta_builder(last), settings=settings,
    )


def polynomial_factoring_quadratic_form(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}
    local = _poly_settings(settings)
    local["max_degree"] = max(4, int(local.get("max_degree", 4)))

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            local,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_FACTOR_POLY],
            policy=polynomial_policy(max_degree=int(local["max_degree"])),
            leaf_id=str(topic or "polynomial_factoring_quadratic_form"),
        )
        item = sample_quadratic_form(ctx)
        answer = item.factored_latex if include_answer_key else None
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "polynomial_factoring_quadratic_form",
            "method": item.method,
            "degree": item.degree,
            "upgrades": list(item.upgrades),
            "effective_d": item.effective_d,
        }
        return item.latex, item.text, answer

    return make_questions(
        topic, count, include_answer_key, build,
        metadata_builder=_meta_builder(last), settings=settings,
    )


def polynomial_factoring_all_techniques(topic: str, settings: dict) -> list[Question]:
    """Mixer over GCF / quadratic / special / grouping (+ cubes for A2 all-techniques)."""
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}
    local = _poly_settings(settings)
    tid = str(topic or "polynomial_factoring_all_techniques")
    # A2 all-techniques needs degree ≥3 for cubes; A1 general strategy stays ≤3.
    if "all_techniques" in tid:
        local["max_degree"] = max(3, int(local.get("max_degree", 3)))
    else:
        local["max_degree"] = min(3, max(2, int(local.get("max_degree", 3))))

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            local,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_FACTOR_POLY, PRIM_FACTOR_GCF],
            policy=_policy_from(local),
            leaf_id=tid,
        )
        item = sample_factoring_all_techniques(ctx)
        answer = item.factored_latex if include_answer_key else None
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "polynomial_factoring_all_techniques",
            "method": item.method,
            "degree": item.degree,
            "upgrades": list(item.upgrades),
            "effective_d": item.effective_d,
        }
        return item.latex, item.text, answer

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
    "simplify_polynomials": simplify_polynomials,
    "polynomial_factoring_common_factor": factor_gcf_poly,
    "quadratic_factoring": quadratic_factoring,
    "a2_quadratic_functions_and_inequalities_factoring_quadratic_expressions": quadratic_factoring,
    "quadratic_factoring_equations": quadratic_factoring_equations,
    "a2_quadratic_functions_and_inequalities_solving_equations_by_factoring": (
        quadratic_factoring_equations
    ),
    "a2_polynomial_functions_solving_polynomial_equations": quadratic_factoring_equations,
    "polynomial_factoring_special_cases": polynomial_factoring_special_cases,
    "a2_quadratic_functions_and_inequalities_factoring_special_case_quadratic_expressions": (
        polynomial_factoring_special_cases
    ),
    "polynomial_factoring_sum_diff_cubes": polynomial_factoring_sum_diff_cubes,
    "a2_polynomial_functions_factoring_sum_difference_of_cubes": (
        polynomial_factoring_sum_diff_cubes
    ),
    "polynomial_factoring_quadratic_form": polynomial_factoring_quadratic_form,
    "a2_polynomial_functions_factoring_quadratic_form": polynomial_factoring_quadratic_form,
    "polynomial_factoring_grouping": polynomial_factoring_grouping,
    "a2_polynomial_functions_factoring_by_grouping": polynomial_factoring_grouping,
    "polynomial_factoring_all_techniques": polynomial_factoring_all_techniques,
    "a2_polynomial_functions_factoring_all_techniques": polynomial_factoring_all_techniques,
    "polynomial_factoring_general_strategy": polynomial_factoring_all_techniques,
}
