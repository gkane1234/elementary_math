"""G6 / early-algebra generators driven by shared primitives + continuous difficulty."""

from __future__ import annotations

from typing import Any

from fractions import Fraction

from question_engine.core.models import Question
from question_engine.frameworks.primitives import (
    PRIM_DISTRIBUTIVE,
    PRIM_EQUATIONS,
    PRIM_EVALUATE,
    PRIM_EXPAND_SIMPLIFY,
    PRIM_FACTOR_GCF,
    PRIM_INEQUALITIES,
    PRIM_LIKE_TERMS,
    PRIM_NUMBERS,
    PRIM_OOO,
    PRIM_VARIABLE,
    build_context,
)
from question_engine.frameworks.primitives.distributive import sample_distributive_numeric
from question_engine.frameworks.primitives.equations import sample_linear_equation
from question_engine.frameworks.primitives.evaluate import sample_evaluate_expression
from question_engine.frameworks.primitives.expand_simplify import sample_expand_simplify
from question_engine.frameworks.primitives.expression_policy import LINEAR_POLICY
from question_engine.frameworks.primitives.factor_gcf import sample_factor_gcf
from question_engine.frameworks.primitives.inequalities import sample_linear_inequality
from question_engine.frameworks.primitives.like_terms import sample_like_terms
from question_engine.frameworks.primitives.ooo import sample_ooo_expression
from question_engine.generators.utils import frac_latex, make_questions


def _answer_latex(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return frac_latex(value)


def order_of_operations(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            settings,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_OOO],
        )
        expr = sample_ooo_expression(ctx)
        answer = _answer_latex(expr.value) if include_answer_key else None
        last["meta"] = {**ctx.metadata(), "primitive_engine": "ooo"}
        # Stem only — worksheet UI factors catalog instruction_latex as a header.
        return (expr.latex, expr.text, answer)

    def metadata_builder(_p: str, _t: str, _a: str | None) -> dict[str, Any]:
        return dict(last.get("meta") or {})

    return make_questions(
        topic,
        count,
        include_answer_key,
        build,
        metadata_builder=metadata_builder,
        settings=settings,
    )


def distributive_property(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            settings,
            [PRIM_NUMBERS, PRIM_DISTRIBUTIVE],
        )
        # Prefer no zeros for a cleaner distributive feel; lane follows D + constraints.
        if PRIM_NUMBERS not in ctx.prereq_settings:
            ctx.prereq_settings[PRIM_NUMBERS] = {}
        ctx.prereq_settings[PRIM_NUMBERS].setdefault("exclude_zero", True)
        expr = sample_distributive_numeric(ctx)
        answer = expr.expanded_latex if include_answer_key else None
        last["meta"] = {**ctx.metadata(), "primitive_engine": "distributive"}
        # Stem only — instruction comes from catalog / metadata.instruction_latex.
        return (expr.latex, expr.text, answer)

    def metadata_builder(_p: str, _t: str, _a: str | None) -> dict[str, Any]:
        return dict(last.get("meta") or {})

    return make_questions(
        topic,
        count,
        include_answer_key,
        build,
        metadata_builder=metadata_builder,
        settings=settings,
    )


def distributive_property_algebraic(topic: str, settings: dict) -> list[Question]:
    """Algebraic distributive via presentation layer (var-outer or const-outer forms)."""
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}

    def build() -> tuple[str, str, str | None]:
        from question_engine.frameworks.primitives.distributive import (
            sample_distributive_algebraic,
        )

        ctx = build_context(
            settings,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_DISTRIBUTIVE],
        )
        if PRIM_NUMBERS not in ctx.prereq_settings:
            ctx.prereq_settings[PRIM_NUMBERS] = {}
        ctx.prereq_settings[PRIM_NUMBERS].setdefault("exclude_zero", True)
        expr = sample_distributive_algebraic(ctx)
        answer = expr.expanded_latex if include_answer_key else None
        cancel_tags = [u for u in expr.upgrades if str(u).startswith("cancel:")]
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "distributive_algebraic",
            "distributive_form": expr.form,
            "cancel_clutter": cancel_tags,
        }
        return (expr.latex, expr.text, answer)

    def metadata_builder(_p: str, _t: str, _a: str | None) -> dict[str, Any]:
        return dict(last.get("meta") or {})

    return make_questions(
        topic,
        count,
        include_answer_key,
        build,
        metadata_builder=metadata_builder,
        settings=settings,
    )


def evaluate_algebraic_expressions(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            settings,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_EVALUATE],
            policy=LINEAR_POLICY,
            leaf_id="evaluate_algebraic_expressions",
        )
        expr = sample_evaluate_expression(ctx)
        answer = expr.value_latex if include_answer_key else None
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "evaluate",
            "upgrades": list(expr.upgrades),
            "n_terms": expr.n_terms,
            "n_parens": expr.n_parens,
            "nest_depth": expr.nest_depth,
            "n_ops": expr.n_ops,
            "op_pool": list(expr.op_pool),
            "coeff_a": str(expr.coeff_a),
            "coeff_b": str(expr.coeff_b),
        }
        # Keep substitution in the stem (per-question); "Evaluate." is the header.
        return (
            f"{expr.latex} \\text{{ when }} {expr.var_latex} = {expr.subst_latex}",
            f"{expr.text} when {expr.var_name} = {expr.subst_latex}",
            answer,
        )

    def metadata_builder(_p: str, _t: str, _a: str | None) -> dict[str, Any]:
        return dict(last.get("meta") or {})

    return make_questions(
        topic,
        count,
        include_answer_key,
        build,
        metadata_builder=metadata_builder,
        settings=settings,
    )


def combining_like_terms(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            settings,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_LIKE_TERMS],
            policy=LINEAR_POLICY,
            leaf_id="combining_like_terms",
        )
        expr = sample_like_terms(ctx)
        answer = expr.simplified_latex if include_answer_key else None
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "like_terms",
            "upgrades": list(expr.upgrades),
        }
        return (expr.latex, expr.text, answer)

    def metadata_builder(_p: str, _t: str, _a: str | None) -> dict[str, Any]:
        return dict(last.get("meta") or {})

    return make_questions(
        topic,
        count,
        include_answer_key,
        build,
        metadata_builder=metadata_builder,
        settings=settings,
    )


def expand_then_simplify(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            settings,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_EXPAND_SIMPLIFY],
            policy=LINEAR_POLICY,
            leaf_id="expand_simplify",
        )
        expr = sample_expand_simplify(ctx)
        answer = expr.simplified_latex if include_answer_key else None
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "expand_simplify",
            "upgrades": list(expr.upgrades),
            "n_groups": expr.n_groups,
            "n_lone": expr.n_lone,
            "nested": expr.nested,
            "nest_depth": expr.nest_depth,
            "coeff_a": str(expr.coeff_a),
            "coeff_b": str(expr.coeff_b),
        }
        return (expr.latex, expr.text, answer)

    def metadata_builder(_p: str, _t: str, _a: str | None) -> dict[str, Any]:
        return dict(last.get("meta") or {})

    return make_questions(
        topic,
        count,
        include_answer_key,
        build,
        metadata_builder=metadata_builder,
        settings=settings,
    )


def _equation_generator(force_steps: str | None):
    def generator(topic: str, settings: dict) -> list[Question]:
        count = int(settings.get("count", 10))
        include_answer_key = bool(settings.get("include_answer_key", False))
        last: dict[str, Any] = {"meta": {}}
        local = dict(settings)
        if force_steps:
            local.setdefault("force_steps", force_steps)
            prereq = dict(local.get("prereq_settings") or {})
            eq_s = dict(prereq.get(PRIM_EQUATIONS) or {})
            eq_s["force_steps"] = force_steps
            prereq[PRIM_EQUATIONS] = eq_s
            local["prereq_settings"] = prereq

        def build() -> tuple[str, str, str | None]:
            ctx = build_context(
                local,
                [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_EQUATIONS],
                policy=LINEAR_POLICY,
            )
            force = force_steps if force_steps in {"one", "two", "multi"} else None
            eq = sample_linear_equation(ctx, force_steps=force)
            if eq.solution_kind == "unique":
                answer = (
                    f"{eq.var_latex} = {eq.solution_latex}" if include_answer_key else None
                )
            else:
                answer = eq.solution_latex if include_answer_key else None
            last["meta"] = {
                **ctx.metadata(),
                "primitive_engine": "equations",
                "steps": eq.steps,
                "n_ops": eq.n_ops,
                "upgrades": list(eq.upgrades),
                "solution_kind": eq.solution_kind,
            }
            return (eq.latex, eq.text, answer)

        def metadata_builder(_p: str, _t: str, _a: str | None) -> dict[str, Any]:
            return dict(last.get("meta") or {})

        return make_questions(
            topic,
            count,
            include_answer_key,
            build,
            metadata_builder=metadata_builder,
            settings=local,
        )

    return generator


def _inequality_generator(force_steps: str | None):
    def generator(topic: str, settings: dict) -> list[Question]:
        from question_engine.frameworks.graphing import (
            metadata_from_number_line_spec,
            number_line_spec_from_symbol_and_value,
        )

        count = int(settings.get("count", 10))
        include_answer_key = bool(settings.get("include_answer_key", False))
        last: dict[str, Any] = {"meta": {}}
        local = dict(settings)
        if force_steps:
            local.setdefault("force_steps", force_steps)
            prereq = dict(local.get("prereq_settings") or {})
            ineq_s = dict(prereq.get(PRIM_INEQUALITIES) or {})
            ineq_s["force_steps"] = force_steps
            prereq[PRIM_INEQUALITIES] = ineq_s
            local["prereq_settings"] = prereq

        def build() -> tuple[str, str, str | None]:
            ctx = build_context(
                local,
                [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_INEQUALITIES],
                policy=LINEAR_POLICY,
            )
            force = force_steps if force_steps in {"one", "two", "multi"} else None
            ineq = sample_linear_inequality(ctx, force_steps=force)
            answer = ineq.solution_latex if include_answer_key else None
            meta: dict[str, Any] = {
                **ctx.metadata(),
                "primitive_engine": "inequalities",
                "steps": ineq.steps,
                "n_ops": ineq.n_ops,
                "flipped": ineq.flipped,
                "upgrades": list(ineq.upgrades),
            }
            # Blank prompt number line + shaded answer (matches legacy inequality frameworks).
            try:
                spec = number_line_spec_from_symbol_and_value(
                    ineq.op,
                    float(ineq.solution_value),
                    local,
                )
                meta.update(metadata_from_number_line_spec(spec, prompt="blank"))
            except (TypeError, ValueError):
                pass
            last["meta"] = meta
            return (ineq.latex, ineq.text, answer)

        def metadata_builder(_p: str, _t: str, _a: str | None) -> dict[str, Any]:
            return dict(last.get("meta") or {})

        return make_questions(
            topic,
            count,
            include_answer_key,
            build,
            metadata_builder=metadata_builder,
            settings=local,
        )

    return generator


def factor_gcf(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}

    def build() -> tuple[str, str, str | None]:
        # GCF wants integers; nudge constraints without killing lane system.
        local = dict(settings)
        if "integers_only" not in local:
            local["integers_only"] = True
        ctx = build_context(
            local,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_FACTOR_GCF],
            policy=LINEAR_POLICY,
            leaf_id="factor_gcf",
        )
        expr = sample_factor_gcf(ctx)
        answer = expr.factored_latex if include_answer_key else None
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "factor_gcf",
            "upgrades": list(expr.upgrades),
            "gcf": expr.gcf_latex,
        }
        return (expr.latex, expr.text, answer)

    def metadata_builder(_p: str, _t: str, _a: str | None) -> dict[str, Any]:
        return dict(last.get("meta") or {})

    return make_questions(
        topic,
        count,
        include_answer_key,
        build,
        metadata_builder=metadata_builder,
        settings=settings,
    )


one_step_equations = _equation_generator("one")
two_step_equations = _equation_generator("two")
multi_step_equations = _equation_generator("multi")
one_step_inequalities = _inequality_generator("one")
two_step_inequalities = _inequality_generator("two")
multi_step_inequalities = _inequality_generator("multi")


GENERATORS = {
    "order_of_operations": order_of_operations,
    "distributive_property": distributive_property,
    "distributive_property_algebraic": distributive_property_algebraic,
    # Catalog aliases used by grade_6
    "g6_distributive_property_numeric": distributive_property,
    "g6_distributive_property_algebraic": distributive_property_algebraic,
    # Layer 1
    "evaluate_algebraic_expressions": evaluate_algebraic_expressions,
    "g6_evaluating_algebraic_expressions": evaluate_algebraic_expressions,
    "combining_like_terms": combining_like_terms,
    "g6_combining_like_terms": combining_like_terms,
    "expand_simplify": expand_then_simplify,
    "expand_then_simplify": expand_then_simplify,
    "one_step_equations": one_step_equations,
    "two_step_equations": two_step_equations,
    "multi_step_equations": multi_step_equations,
    "pa_equations_multi_step_equations": multi_step_equations,
    "a2_equations_and_inequalities_multi_step_equations": multi_step_equations,
    "a2_beginning_algebra_simplifying_algebraic_expressions": expand_then_simplify,
    "geo_review_multi_step_equations": multi_step_equations,
    "one_step_inequalities": one_step_inequalities,
    "two_step_inequalities": two_step_inequalities,
    "multi_step_inequalities": multi_step_inequalities,
    "pa_multi_step_inequalities": multi_step_inequalities,
    "a2_equations_and_inequalities_multi_step_inequalities": multi_step_inequalities,
    "g6_solving_and_graphing_one_step_inequalities": one_step_inequalities,
    "factor_gcf": factor_gcf,
    "g6_factor_gcf": factor_gcf,
    "polynomial_factoring_common_factor": factor_gcf,
}
