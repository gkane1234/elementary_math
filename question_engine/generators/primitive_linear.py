"""Linear-family generators on shared primitives (abs, compound, forms, systems, WP).

Overrides legacy equation/linear/graphing/word_problem keys via last-wins in
``generators/__init__.py``.
"""

from __future__ import annotations

from typing import Any, Callable

from question_engine.core.models import Question
from question_engine.frameworks.primitives import (
    PRIM_EQUATIONS,
    PRIM_INEQUALITIES,
    PRIM_NUMBERS,
    PRIM_VARIABLE,
    build_context,
)
from question_engine.frameworks.primitives.absolute_value import (
    sample_absolute_value_equation,
    sample_absolute_value_inequality,
)
from question_engine.frameworks.primitives.compound import sample_compound_inequality
from question_engine.frameworks.primitives.expression_policy import (
    LINEAR_ABS_POLICY,
    LINEAR_POLICY,
    SYSTEMS_POLICY,
)
from question_engine.frameworks.primitives.linear_forms import (
    sample_slope,
    sample_writing_linear,
    slope_intercept_latex,
)
from question_engine.frameworks.primitives.proportions import (
    sample_literal_equation,
    sample_proportion,
)
from question_engine.frameworks.primitives.systems import sample_linear_system
from question_engine.frameworks.primitives.word_problems import WPKind, sample_word_problem
from question_engine.generators.utils import make_questions


def _meta_builder(last: dict[str, Any]):
    def metadata_builder(_p: str, _t: str, _a: str | None) -> dict[str, Any]:
        return dict(last.get("meta") or {})

    return metadata_builder


def absolute_value_equations(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            settings,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_EQUATIONS],
            policy=LINEAR_ABS_POLICY,
            leaf_id="absolute_value_equations",
        )
        eq = sample_absolute_value_equation(ctx)
        answer = eq.solution_latex if include_answer_key else None
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "absolute_value_equations",
            "form": eq.form,
            "upgrades": list(eq.upgrades),
            "solution_kind": eq.solution_kind,
        }
        return (
            f"\\text{{Solve: }} {eq.latex}",
            f"Solve: {eq.text}",
            answer,
        )

    return make_questions(
        topic, count, include_answer_key, build,
        metadata_builder=_meta_builder(last), settings=settings,
    )


def absolute_value_inequalities(topic: str, settings: dict) -> list[Question]:
    from question_engine.frameworks.graphing import (
        metadata_from_number_line_spec,
        number_line_spec_from_symbol_and_value,
    )

    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            settings,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_INEQUALITIES],
            policy=LINEAR_ABS_POLICY,
            leaf_id="absolute_value_inequalities",
        )
        ineq = sample_absolute_value_inequality(ctx)
        answer = ineq.solution_latex if include_answer_key else None
        meta: dict[str, Any] = {
            **ctx.metadata(),
            "primitive_engine": "absolute_value_inequalities",
            "compound_style": ineq.compound_style,
            "upgrades": list(ineq.upgrades),
        }
        try:
            # Approximate number line from boundary magnitude for |x| forms.
            sym = ">" if ineq.compound_style == "or" else "<"
            if ineq.inclusive:
                sym = "\\ge" if ineq.compound_style == "or" else "\\le"
            # For and-style use left endpoint style; graphing helper expects single ray.
            if ineq.compound_style == "and":
                spec = number_line_spec_from_symbol_and_value(
                    "\\le" if ineq.inclusive else "<",
                    float(ineq.boundary),
                    settings,
                )
            else:
                spec = number_line_spec_from_symbol_and_value(
                    sym, float(ineq.boundary), settings
                )
            meta.update(metadata_from_number_line_spec(spec, prompt="blank"))
        except (TypeError, ValueError):
            pass
        last["meta"] = meta
        return (f"\\text{{Solve: }} {ineq.latex}", f"Solve: {ineq.text}", answer)

    return make_questions(
        topic, count, include_answer_key, build,
        metadata_builder=_meta_builder(last), settings=settings,
    )


def compound_inequalities(topic: str, settings: dict) -> list[Question]:
    from question_engine.frameworks.graphing import (
        metadata_from_number_line_spec,
        number_line_spec_from_symbol_and_value,
    )

    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            settings,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_INEQUALITIES],
            policy=LINEAR_POLICY,
            leaf_id="compound_inequalities",
        )
        item = sample_compound_inequality(ctx)
        answer = item.solution_latex if include_answer_key else None
        meta: dict[str, Any] = {
            **ctx.metadata(),
            "primitive_engine": "compound_inequalities",
            "style": item.style,
            "upgrades": list(item.upgrades),
        }
        if item.hi is not None:
            try:
                spec = number_line_spec_from_symbol_and_value(
                    "\\le" if item.hi_inclusive else "<",
                    float(item.hi),
                    settings,
                )
                meta.update(metadata_from_number_line_spec(spec, prompt="blank"))
            except (TypeError, ValueError):
                pass
        last["meta"] = meta
        return (f"\\text{{Solve: }} {item.latex}", f"Solve: {item.text}", answer)

    return make_questions(
        topic, count, include_answer_key, build,
        metadata_builder=_meta_builder(last), settings=settings,
    )


def solving_proportions(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            settings,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_EQUATIONS],
            policy=LINEAR_POLICY,
            leaf_id="solving_proportions",
        )
        prop = sample_proportion(ctx)
        answer = prop.solution_latex if include_answer_key else None
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "proportions",
            "upgrades": list(prop.upgrades),
        }
        return (
            f"\\text{{Solve: }} {prop.latex}",
            f"Solve: {prop.text}",
            answer,
        )

    return make_questions(
        topic, count, include_answer_key, build,
        metadata_builder=_meta_builder(last), settings=settings,
    )


def literal_equations(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            settings,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_EQUATIONS],
            policy=LINEAR_POLICY,
            leaf_id="literal_equations",
        )
        lit = sample_literal_equation(ctx)
        answer = lit.solution_latex if include_answer_key else None
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "literal_equations",
            "form": lit.form,
            "target_var": lit.target_var,
            "upgrades": list(lit.upgrades),
        }
        return (lit.latex, lit.text, answer)

    return make_questions(
        topic, count, include_answer_key, build,
        metadata_builder=_meta_builder(last), settings=settings,
    )


def slope(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            settings,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_EQUATIONS],
            policy=LINEAR_POLICY,
            leaf_id="slope",
        )
        item = sample_slope(ctx)
        answer = item.answer_latex if include_answer_key else None
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "slope",
            "mode": item.mode,
            "upgrades": list(item.upgrades),
        }
        return (item.latex, item.text, answer)

    return make_questions(
        topic, count, include_answer_key, build,
        metadata_builder=_meta_builder(last), settings=settings,
    )


def writing_linear_equations(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            settings,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_EQUATIONS],
            policy=LINEAR_POLICY,
            leaf_id="writing_linear_equations",
        )
        item = sample_writing_linear(ctx)
        answer = item.answer_latex if include_answer_key else None
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "writing_linear",
            "mode": item.mode,
            "upgrades": list(item.upgrades),
        }
        return (item.latex, item.text, answer)

    return make_questions(
        topic, count, include_answer_key, build,
        metadata_builder=_meta_builder(last), settings=settings,
    )


def _graph_linear_equations(topic: str, settings: dict) -> list[Question]:
    """Graph a line — reuse writing/slope coeffs + graphing stimulus pipeline."""
    from question_engine.frameworks.graphing import (
        _linear_function_expr,
        _plane_spec,
        coordinate_plane_metadata,
    )

    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            settings,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_EQUATIONS],
            policy=LINEAR_POLICY,
            leaf_id="graphing_linear_equations",
        )
        item = sample_writing_linear(ctx)
        eq = slope_intercept_latex(item.line.m, item.line.b)
        answer = eq if include_answer_key else None
        meta: dict[str, Any] = {
            **ctx.metadata(),
            "primitive_engine": "graph_linear",
            "upgrades": list(item.upgrades),
            "slope": str(item.line.m),
            "intercept": str(item.line.b),
        }
        try:
            m = float(item.line.m)
            b = float(item.line.b)
            spec = _plane_spec(
                settings,
                slope=m,
                y_intercept=b,
                functions=[_linear_function_expr(m, b)],
            )
            meta.update(coordinate_plane_metadata(spec, settings, prompt="blank"))
        except Exception:
            pass
        last["meta"] = meta
        return (
            f"\\text{{Graph: }} {eq}",
            f"Graph: {eq}",
            answer,
        )

    return make_questions(
        topic, count, include_answer_key, build,
        metadata_builder=_meta_builder(last), settings=settings,
    )


def _graph_linear_inequality(topic: str, settings: dict) -> list[Question]:
    from question_engine.frameworks.graphing import (
        _half_plane_region,
        _linear_function_expr,
        _plane_spec,
        coordinate_plane_metadata,
    )

    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            settings,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_INEQUALITIES],
            policy=LINEAR_POLICY,
            leaf_id="graphing_linear_inequalities",
        )
        item = sample_writing_linear(ctx)
        op = ctx.rng.choice(["<", ">", "\\le", "\\ge"])
        rhs = slope_intercept_latex(item.line.m, item.line.b).replace("y = ", "")
        latex = f"y {op} {rhs}"
        answer = latex if include_answer_key else None
        meta: dict[str, Any] = {
            **ctx.metadata(),
            "primitive_engine": "graph_linear_inequality",
            "upgrades": list(item.upgrades),
        }
        try:
            m = float(item.line.m)
            b = float(item.line.b)
            spec = _plane_spec(
                settings,
                slope=m,
                y_intercept=b,
                functions=[_linear_function_expr(m, b)],
                regions=[_half_plane_region(m, b, op)],
            )
            meta.update(coordinate_plane_metadata(spec, settings, prompt="blank"))
        except Exception:
            pass
        last["meta"] = meta
        return (
            f"\\text{{Graph the inequality: }} {latex}",
            f"Graph the inequality: {latex}",
            answer,
        )

    return make_questions(
        topic, count, include_answer_key, build,
        metadata_builder=_meta_builder(last), settings=settings,
    )


def _graphing_single_variable_inequalities(topic: str, settings: dict) -> list[Question]:
    """Number-line graph — reuse inequality primitive."""
    from question_engine.generators.primitive_g6 import one_step_inequalities

    local = dict(settings)
    local.setdefault("force_steps", "one")
    return one_step_inequalities(topic, local)


def _system_generator(method: str) -> Callable[[str, dict], list[Question]]:
    def generator(topic: str, settings: dict) -> list[Question]:
        count = int(settings.get("count", 10))
        include_answer_key = bool(settings.get("include_answer_key", False))
        last: dict[str, Any] = {"meta": {}}
        local = dict(settings)
        local.setdefault("method", method)

        def build() -> tuple[str, str, str | None]:
            ctx = build_context(
                local,
                [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_EQUATIONS],
                policy=SYSTEMS_POLICY,
                leaf_id=f"systems_{method}",
            )
            sys = sample_linear_system(ctx, method=method)  # type: ignore[arg-type]
            answer = sys.solution_latex if include_answer_key else None
            last["meta"] = {
                **ctx.metadata(),
                "primitive_engine": "systems",
                "method": sys.method,
                "solution_type": sys.solution_type,
                "upgrades": list(sys.upgrades),
            }
            return (
                f"\\text{{Solve: }} {sys.latex}",
                f"Solve: {sys.text}",
                answer,
            )

        return make_questions(
            topic, count, include_answer_key, build,
            metadata_builder=_meta_builder(last), settings=local,
        )

    return generator


def _wp_generator(kind: WPKind) -> Callable[[str, dict], list[Question]]:
    def generator(topic: str, settings: dict) -> list[Question]:
        count = int(settings.get("count", 10))
        include_answer_key = bool(settings.get("include_answer_key", False))
        last: dict[str, Any] = {"meta": {}}
        policy = SYSTEMS_POLICY if kind == "systems" else LINEAR_POLICY

        def build() -> tuple[str, str, str | None]:
            ctx = build_context(
                settings,
                [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_EQUATIONS],
                policy=policy,
                leaf_id=f"wp_{kind}",
            )
            item = sample_word_problem(ctx, kind)
            answer = item.answer_latex if include_answer_key else None
            last["meta"] = {
                **ctx.metadata(),
                "primitive_engine": "word_problem",
                "wp_kind": item.kind,
                "equation_latex": item.equation_latex,
                "upgrades": list(item.upgrades),
            }
            return (item.latex, item.text, answer)

        return make_questions(
            topic, count, include_answer_key, build,
            metadata_builder=_meta_builder(last), settings=settings,
        )

    return generator


def factor_gcf_poly(topic: str, settings: dict) -> list[Question]:
    """Poly leaf: same engine, polynomial ExpressionPolicy (may emit x^2)."""
    from question_engine.frameworks.primitives import PRIM_FACTOR_GCF
    from question_engine.frameworks.primitives.expression_policy import polynomial_policy
    from question_engine.frameworks.primitives.factor_gcf import sample_factor_gcf

    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}
    local = dict(settings)
    local.setdefault("integers_only", True)
    md = int(local.get("max_degree", 3))

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            local,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_FACTOR_GCF],
            policy=polynomial_policy(max_degree=md),
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


def _graph_systems_inequalities(topic: str, settings: dict) -> list[Question]:
    """Two half-planes — reuse system lines + inequality regions."""
    from question_engine.frameworks.graphing import (
        _half_plane_region,
        _linear_function_expr,
        _plane_spec,
        coordinate_plane_metadata,
    )

    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            settings,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_INEQUALITIES],
            policy=SYSTEMS_POLICY,
            leaf_id="graphing_systems_of_inequalities",
        )
        sys = sample_linear_system(ctx, method="graphing")
        op1 = ctx.rng.choice(["<", ">", "\\le", "\\ge"])
        op2 = ctx.rng.choice(["<", ">", "\\le", "\\ge"])
        e1 = slope_intercept_latex(sys.line1.m, sys.line1.b).replace("y = ", "")
        e2 = slope_intercept_latex(sys.line2.m, sys.line2.b).replace("y = ", "")
        latex = f"\\begin{{cases}} y {op1} {e1} \\\\ y {op2} {e2} \\end{{cases}}"
        answer = latex if include_answer_key else None
        meta: dict[str, Any] = {
            **ctx.metadata(),
            "primitive_engine": "graph_systems_inequalities",
            "upgrades": list(sys.upgrades),
        }
        try:
            m1, b1 = float(sys.line1.m), float(sys.line1.b)
            m2, b2 = float(sys.line2.m), float(sys.line2.b)
            spec = _plane_spec(
                settings,
                functions=[
                    _linear_function_expr(m1, b1),
                    _linear_function_expr(m2, b2),
                ],
                regions=[
                    _half_plane_region(m1, b1, op1),
                    _half_plane_region(m2, b2, op2),
                ],
            )
            meta.update(coordinate_plane_metadata(spec, settings, prompt="blank"))
        except Exception:
            pass
        last["meta"] = meta
        return (
            f"\\text{{Graph the system: }} {latex}",
            f"Graph the system: {latex}",
            answer,
        )

    return make_questions(
        topic, count, include_answer_key, build,
        metadata_builder=_meta_builder(last), settings=settings,
    )


GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = {
    "absolute_value_equations": absolute_value_equations,
    "a2_equations_and_inequalities_absolute_value_equations": absolute_value_equations,
    "absolute_value_inequalities": absolute_value_inequalities,
    "a2_equations_and_inequalities_absolute_value_inequalities": absolute_value_inequalities,
    "compound_inequalities": compound_inequalities,
    "a2_equations_and_inequalities_compound_inequalities": compound_inequalities,
    "solving_proportions": solving_proportions,
    "pa_checking_for_a_proportion": solving_proportions,
    "literal_equations": literal_equations,
    "slope": slope,
    "more_on_slope": slope,
    "pa_slope": slope,
    "writing_linear_equations": writing_linear_equations,
    "pa_writing_linear_equations": writing_linear_equations,
    "graphing_linear_equations": _graph_linear_equations,
    "graph_linear_equation": _graph_linear_equations,
    "a2_linear_functions_graphing_linear_equations": _graph_linear_equations,
    "a2_linear_relations_and_functions_graphing_linear_equations": _graph_linear_equations,
    "graphing_linear_inequalities": _graph_linear_inequality,
    "graph_linear_inequality": _graph_linear_inequality,
    "a2_linear_relations_and_functions_graphing_linear_inequalities": _graph_linear_inequality,
    "graphing_single_variable_inequalities": _graphing_single_variable_inequalities,
    "graphing_systems_of_inequalities": _graph_systems_inequalities,
    "graph_system_inequalities": _graph_systems_inequalities,
    "a2_systems_of_equations_and_inequalities_graphing_systems_of_linear_inequalities": _graph_systems_inequalities,
    "systems_elimination": _system_generator("elimination"),
    "systems_substitution": _system_generator("substitution"),
    "systems_graphing": _system_generator("graphing"),
    "graph_system": _system_generator("graphing"),
    "pa_systems_of_equations_elimination": _system_generator("elimination"),
    "pa_systems_of_equations_substitution": _system_generator("substitution"),
    "a2_systems_of_equations_elimination": _system_generator("elimination"),
    "a2_systems_of_equations_substitution": _system_generator("substitution"),
    "polynomial_factoring_common_factor": factor_gcf_poly,
    "wp_one_step_equation": _wp_generator("one_step"),
    "wp_two_step_equation": _wp_generator("two_step"),
    # wp_mixture / wp_distance_rate_time: real narrative frameworks in word_problems.py
    # (do not override with equation-with-story stubs).
    "wp_work": _wp_generator("work"),
    "wp_age": _wp_generator("age"),
    "wp_coin": _wp_generator("coin"),
    "wp_consecutive_integers": _wp_generator("consecutive"),
    "wp_percent": _wp_generator("percent"),
    "wp_proportion": _wp_generator("proportion"),
    "wp_inequality": _wp_generator("inequality"),
    "wp_systems": _wp_generator("systems"),
    "a2_linear_relations_and_functions_writing_linear_equations": writing_linear_equations,
}
