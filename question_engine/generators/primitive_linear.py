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
    graphable_line_latex,
    sample_graphable_line,
    sample_more_on_slope,
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
        from question_engine.frameworks.primitives.equation_skeleton import (
            sample_abs_equation_skeleton,
            use_abs_equation_skeleton,
        )

        ctx = build_context(
            settings,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_EQUATIONS],
            policy=LINEAR_ABS_POLICY,
            leaf_id=str(topic or "absolute_value_equations"),
        )
        if use_abs_equation_skeleton(settings):
            eq = sample_abs_equation_skeleton(ctx)
            answer = eq.solution_latex if include_answer_key else None
            last["meta"] = {
                **ctx.metadata(),
                "primitive_engine": "equation_skeleton",
                "upgrades": list(eq.upgrades),
                "solution_kind": eq.solution_kind,
                **eq.metadata,
            }
            return (
                f"\\text{{Solve: }} {eq.latex}",
                f"Solve: {eq.text}",
                answer,
            )
        eq_old = sample_absolute_value_equation(ctx)
        answer = eq_old.solution_latex if include_answer_key else None
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "absolute_value_equations",
            "form": eq_old.form,
            "upgrades": list(eq_old.upgrades),
            "solution_kind": eq_old.solution_kind,
        }
        return (
            f"\\text{{Solve: }} {eq_old.latex}",
            f"Solve: {eq_old.text}",
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
        from question_engine.frameworks.primitives.equation_skeleton import (
            sample_abs_inequality_skeleton,
            use_abs_inequality_skeleton,
        )

        ctx = build_context(
            settings,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_INEQUALITIES],
            policy=LINEAR_ABS_POLICY,
            leaf_id=str(topic or "absolute_value_inequalities"),
        )
        if use_abs_inequality_skeleton(settings):
            ineq = sample_abs_inequality_skeleton(ctx)
            answer = ineq.solution_latex if include_answer_key else None
            meta: dict[str, Any] = {
                **ctx.metadata(),
                "primitive_engine": "equation_skeleton",
                "compound_style": ineq.compound_style,
                "upgrades": list(ineq.upgrades),
                **ineq.metadata,
            }
            try:
                if ineq.lo is not None and ineq.hi is not None:
                    spec = number_line_spec_from_symbol_and_value(
                        ineq.op,
                        float(ineq.lo),
                        settings,
                        boundary_high=float(ineq.hi),
                        outside=ineq.compound_style == "or",
                        inclusive=ineq.lo_inclusive,
                        inclusive_high=ineq.hi_inclusive,
                    )
                    meta.update(metadata_from_number_line_spec(spec, prompt="blank"))
            except (TypeError, ValueError):
                pass
            last["meta"] = meta
            return (f"\\text{{Solve: }} {ineq.latex}", f"Solve: {ineq.text}", answer)

        ineq_old = sample_absolute_value_inequality(ctx)
        answer = ineq_old.solution_latex if include_answer_key else None
        meta = {
            **ctx.metadata(),
            "primitive_engine": "absolute_value_inequalities",
            "compound_style": ineq_old.compound_style,
            "upgrades": list(ineq_old.upgrades),
        }
        try:
            sym = ">" if ineq_old.compound_style == "or" else "<"
            if ineq_old.inclusive:
                sym = "\\ge" if ineq_old.compound_style == "or" else "\\le"
            if ineq_old.compound_style == "and":
                spec = number_line_spec_from_symbol_and_value(
                    "\\le" if ineq_old.inclusive else "<",
                    float(ineq_old.boundary),
                    settings,
                )
            else:
                spec = number_line_spec_from_symbol_and_value(
                    sym, float(ineq_old.boundary), settings
                )
            meta.update(metadata_from_number_line_spec(spec, prompt="blank"))
        except (TypeError, ValueError):
            pass
        last["meta"] = meta
        return (f"\\text{{Solve: }} {ineq_old.latex}", f"Solve: {ineq_old.text}", answer)

    return make_questions(
        topic, count, include_answer_key, build,
        metadata_builder=_meta_builder(last), settings=settings,
    )


def compound_inequalities(topic: str, settings: dict) -> list[Question]:
    """Old CompoundInequalitiesFramework: given compound + blank number line.

    Easy (D≤4, steps=1): isolated ``-1 < x < 2`` / ``x < -1 or x > 1``;
    prompt = answer = the inequality; student graphs it.
    Medium/hard: solve a linear compound, then graph the isolated form.
    Number-line helper is the same as the old framework:
    ``number_line_spec_from_symbol_and_value`` + blank prompt spec.
    """
    from question_engine.frameworks.equation import CompoundInequalitiesFramework
    from question_engine.frameworks.graphing import (
        metadata_from_number_line_spec,
        number_line_spec_from_symbol_and_value,
    )
    from question_engine.frameworks.primitives.equation_skeleton import (
        use_compound_skeleton,
    )
    from question_engine.settings.presets import apply_difficulty_presets

    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}
    local = apply_difficulty_presets(
        dict(settings),
        type_id=str(topic or "compound_inequalities"),
        setting_profile="compound_inequality",
    )
    local.setdefault("include_graph_metadata", True)

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            local,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_INEQUALITIES],
            policy=LINEAR_POLICY,
            leaf_id=str(topic or "compound_inequalities"),
        )
        if not use_compound_skeleton(local):
            item_old = sample_compound_inequality(ctx)
            answer = item_old.solution_latex if include_answer_key else None
            meta = {
                **ctx.metadata(),
                "primitive_engine": "compound_inequalities",
                "style": item_old.style,
                "upgrades": list(item_old.upgrades),
            }
            if item_old.hi is not None:
                try:
                    spec = number_line_spec_from_symbol_and_value(
                        "\\le" if item_old.hi_inclusive else "<",
                        float(item_old.hi),
                        local,
                    )
                    meta.update(metadata_from_number_line_spec(spec, prompt="blank"))
                except (TypeError, ValueError):
                    pass
            last["meta"] = meta
            return (f"\\text{{Solve: }} {item_old.latex}", f"Solve: {item_old.text}", answer)

        fw = CompoundInequalitiesFramework()
        prompt_l, prompt_t, answer = fw.build_prompt(local)
        graph = fw._inequality_graph
        fw._inequality_graph = None
        steps = int(local.get("steps", fw.steps))
        outside = bool((graph or {}).get("outside", False))
        meta: dict[str, Any] = {
            **ctx.metadata(),
            "skeleton_pattern": "CompoundInequality",
            "primitive_engine": "compound_inequalities",
            "form_id": "compound_inequality",
            "species": "or" if outside else "chain",
            "steps": steps,
            "construction": {1: "isolated", 2: "middle", 3: "hard"}.get(steps, "middle"),
        }
        if graph:
            try:
                spec = number_line_spec_from_symbol_and_value(
                    str(graph["symbol"]),
                    float(graph["boundary"]),
                    local,
                    boundary_high=graph.get("boundary_high"),
                    outside=outside,
                    inclusive=graph.get("inclusive"),
                    inclusive_high=graph.get("inclusive_high"),
                )
                meta.update(metadata_from_number_line_spec(spec, prompt="blank"))
            except (TypeError, ValueError):
                pass
        last["meta"] = meta
        return (prompt_l, prompt_t, answer if include_answer_key else None)

    return make_questions(
        topic, count, include_answer_key, build,
        metadata_builder=_meta_builder(last), settings=local,
    )


def solving_proportions(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}

    def build() -> tuple[str, str, str | None]:
        from question_engine.frameworks.primitives.equation_skeleton import (
            sample_solve_proportion,
            use_solve_proportion_skeleton,
        )

        ctx = build_context(
            settings,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_EQUATIONS],
            policy=LINEAR_POLICY,
            leaf_id=str(topic or "solving_proportions"),
        )
        if use_solve_proportion_skeleton(settings):
            prop = sample_solve_proportion(ctx)
            answer = prop.solution_latex if include_answer_key else None
            last["meta"] = {
                **ctx.metadata(),
                "primitive_engine": "equation_skeleton",
                "upgrades": list(prop.upgrades),
                **prop.metadata,
            }
            return (
                f"\\text{{Solve: }} {prop.latex}",
                f"Solve: {prop.text}",
                answer,
            )
        prop_old = sample_proportion(ctx)
        answer = prop_old.solution_latex if include_answer_key else None
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "proportions",
            "upgrades": list(prop_old.upgrades),
        }
        return (
            f"\\text{{Solve: }} {prop_old.latex}",
            f"Solve: {prop_old.text}",
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
        from question_engine.frameworks.primitives.equation_skeleton import (
            sample_solve_literal,
            use_solve_literal_skeleton,
        )

        ctx = build_context(
            settings,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_EQUATIONS],
            policy=LINEAR_POLICY,
            leaf_id=str(topic or "literal_equations"),
        )
        if use_solve_literal_skeleton(settings):
            lit = sample_solve_literal(ctx)
            answer = lit.solution_latex if include_answer_key else None
            last["meta"] = {
                **ctx.metadata(),
                "primitive_engine": "equation_skeleton",
                "form": lit.form,
                "target_var": lit.target_var,
                "upgrades": list(lit.upgrades),
                **lit.metadata,
            }
            return (lit.latex, lit.text, answer)
        lit_old = sample_literal_equation(ctx)
        answer = lit_old.solution_latex if include_answer_key else None
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "literal_equations",
            "form": lit_old.form,
            "target_var": lit_old.target_var,
            "upgrades": list(lit_old.upgrades),
        }
        return (lit_old.latex, lit_old.text, answer)

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
            "skeleton_pattern": "Slope",
            "mode": item.mode,
            "upgrades": list(item.upgrades),
        }
        if item.equation_form:
            last["meta"]["equation_form"] = item.equation_form
        if (
            item.mode == "from_points"
            and item.points
            and bool(settings.get("graph_for_two_points"))
        ):
            try:
                from question_engine.frameworks.graphing import (
                    _linear_function_expr,
                    _plane_spec,
                    coordinate_plane_metadata,
                )

                (x1, y1), (x2, y2) = item.points
                m = float(item.slope)
                b = float(y1) - m * float(x1)
                spec = _plane_spec(
                    settings,
                    points=[(x1, y1), (x2, y2)],
                    slope=m,
                    y_intercept=b,
                    functions=[_linear_function_expr(m, b)],
                )
                last["meta"].update(
                    coordinate_plane_metadata(spec, settings, prompt="blank")
                )
            except Exception:
                pass
        return (item.latex, item.text, answer)

    return make_questions(
        topic, count, include_answer_key, build,
        metadata_builder=_meta_builder(last), settings=settings,
    )


def more_on_slope(topic: str, settings: dict) -> list[Question]:
    """Parallel / perpendicular — OpenStax EA §4.6, not a slope-from-points clone."""
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            settings,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_EQUATIONS],
            policy=LINEAR_POLICY,
            leaf_id="more_on_slope",
        )
        item = sample_more_on_slope(ctx)
        answer = item.answer_latex if include_answer_key else None
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "more_on_slope",
            "skeleton_pattern": "MoreOnSlope",
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
            "skeleton_pattern": "WriteLinear",
            "mode": item.mode,
            "upgrades": list(item.upgrades),
        }
        return (item.latex, item.text, answer)

    return make_questions(
        topic, count, include_answer_key, build,
        metadata_builder=_meta_builder(last), settings=settings,
    )


def _graph_linear_equations(topic: str, settings: dict) -> list[Question]:
    """Graph a line — D=0 through origin (old y=x / y=3x); intercept / standard later."""
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
        line = sample_graphable_line(ctx)
        eq = graphable_line_latex(line)
        answer = eq if include_answer_key else None
        meta: dict[str, Any] = {
            **ctx.metadata(),
            "primitive_engine": "graph_linear",
            "skeleton_pattern": "GraphLinear",
            "slope": str(line.m),
            "intercept": str(line.b),
        }
        try:
            m = float(line.m)
            b = float(line.b)
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
        line = sample_graphable_line(ctx)
        for _ in range(8):
            if not (line.b_std == 0 and line.a_std != 0):
                break
            line = sample_graphable_line(ctx)
        op = ctx.rng.choice(["<", ">", "\\le", "\\ge"])
        rhs = slope_intercept_latex(line.m, line.b).replace("y = ", "")
        latex = f"y {op} {rhs}"
        answer = latex if include_answer_key else None
        meta: dict[str, Any] = {
            **ctx.metadata(),
            "primitive_engine": "graph_linear_inequality",
            "skeleton_pattern": "GraphLinearIneq",
        }
        try:
            m = float(line.m)
            b = float(line.b)
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
    """Number-line 1-var inequality — isolated at D=0, then SolveInequality."""
    from question_engine.frameworks.graphing import (
        metadata_from_number_line_spec,
        number_line_spec_from_symbol_and_value,
    )
    from question_engine.frameworks.primitives.equation_skeleton import (
        sample_graph_inequality,
        use_solve_inequality_skeleton,
    )
    from question_engine.generators.primitive_g6 import one_step_inequalities

    if not use_solve_inequality_skeleton(settings):
        local = dict(settings)
        local.setdefault("force_steps", "one")
        return one_step_inequalities(topic, local)

    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            settings,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_INEQUALITIES],
            policy=LINEAR_POLICY,
            leaf_id=str(topic or "graphing_single_variable_inequalities"),
        )
        ineq = sample_graph_inequality(ctx)
        answer = ineq.solution_latex if include_answer_key else None
        meta: dict[str, Any] = {
            **ctx.metadata(),
            "primitive_engine": "equation_skeleton",
            "steps": ineq.steps,
            "n_ops": ineq.n_ops,
            "upgrades": list(ineq.upgrades),
            **ineq.metadata,
        }
        try:
            spec = number_line_spec_from_symbol_and_value(
                ineq.number_line_op,
                float(ineq.solution_value),
                settings,
            )
            meta.update(metadata_from_number_line_spec(spec, prompt="blank"))
        except (TypeError, ValueError):
            pass
        last["meta"] = meta
        return (ineq.latex, ineq.text, answer)

    return make_questions(
        topic, count, include_answer_key, build,
        metadata_builder=_meta_builder(last), settings=settings,
    )


def _wp_similar_figures(topic: str, settings: dict) -> list[Question]:
    """Scale-factor story on a proportion frame (not a dumped equation)."""
    from question_engine.frameworks.primitives.wp_packaging import use_wp_packaging
    from question_engine.generators.word_problems import GENERATORS as WP_LEGACY

    if not use_wp_packaging(settings, "similar_figures"):
        return WP_LEGACY["wp_similar_figures"](topic, settings)

    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            settings,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_EQUATIONS],
            policy=LINEAR_POLICY,
            leaf_id=str(topic or "wp_similar_figures"),
        )
        item = sample_word_problem(ctx, "similar_figures")
        answer = item.answer_latex if include_answer_key else None
        packed = dict(getattr(item, "metadata", None) or {})
        last["meta"] = {
            **ctx.metadata(),
            **packed,
            "primitive_engine": packed.get("construction") or "wp_packaging",
            "wp_kind": item.kind,
            "equation_latex": item.equation_latex,
            "frame_id": item.frame or packed.get("frame_id") or "",
            "upgrades": list(item.upgrades),
        }
        return (item.latex, item.text, answer)

    return make_questions(
        topic, count, include_answer_key, build,
        metadata_builder=_meta_builder(last), settings=settings,
    )


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
            meta: dict[str, Any] = {
                **ctx.metadata(),
                "primitive_engine": "systems",
                "skeleton_pattern": "LinearSystem",
                "method": sys.method,
                "solution_type": sys.solution_type,
                "upgrades": list(sys.upgrades),
            }
            if method == "graphing":
                try:
                    from question_engine.frameworks.graphing import (
                        _linear_function_expr,
                        _plane_spec,
                        coordinate_plane_metadata,
                    )

                    m1, b1 = float(sys.line1.m), float(sys.line1.b)
                    m2, b2 = float(sys.line2.m), float(sys.line2.b)
                    spec = _plane_spec(
                        local,
                        functions=[
                            _linear_function_expr(m1, b1),
                            _linear_function_expr(m2, b2),
                        ],
                    )
                    meta.update(coordinate_plane_metadata(spec, local, prompt="blank"))
                except Exception:
                    pass
            last["meta"] = meta
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
        local = dict(settings)
        if kind == "one_step":
            local.setdefault("force_steps", "one")
        elif kind == "two_step":
            local.setdefault("force_steps", "two")
        # G6 equation / inequality word problems: classroom variables / integers until mid D.
        if topic.startswith("g6_") and kind in {"one_step", "two_step", "inequality"}:
            local.setdefault("allow_greek", False)
            try:
                d = float(local["difficulty"]) if local.get("difficulty") is not None else None
            except (TypeError, ValueError):
                d = None
            if d is not None and d < 12.0:
                local.setdefault("integers_only", True)
            if d is not None and d < 6.0:
                local.setdefault("force_variable_lane", "only_x")
                local.setdefault("only_x", True)
            else:
                local.setdefault("force_variable_lane", "xyz")

        def build() -> tuple[str, str, str | None]:
            prims = [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_EQUATIONS]
            if kind == "inequality":
                prims = [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_INEQUALITIES]
            ctx = build_context(
                local,
                prims,
                policy=policy,
                leaf_id=str(topic or f"wp_{kind}"),
            )
            item = sample_word_problem(ctx, kind)
            answer = item.answer_latex if include_answer_key else None
            packed = dict(getattr(item, "metadata", None) or {})
            last["meta"] = {
                **ctx.metadata(),
                **packed,
                "primitive_engine": packed.get("construction") or "word_problem",
                "wp_kind": item.kind,
                "equation_latex": item.equation_latex,
                "frame_id": item.frame or packed.get("frame_id") or "",
                "upgrades": list(item.upgrades),
            }
            return (item.latex, item.text, answer)

        return make_questions(
            topic, count, include_answer_key, build,
            metadata_builder=_meta_builder(last), settings=local,
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
    """Two half-planes. D=0: y>x and y<k (OpenStax EA §5.6); mixed solid/dashed later."""
    from question_engine.frameworks.graphing import (
        _half_plane_region,
        _linear_function_expr,
        _plane_spec,
        coordinate_plane_metadata,
    )
    from question_engine.frameworks.primitives.skeleton_difficulty import (
        SkeletonDifficultyBands,
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
        bands = SkeletonDifficultyBands.from_d(float(ctx.topic_d))
        if bands.format_tier == 0:
            m1, b1 = 1.0, 0.0
            k = float(ctx.rng.randint(2, 4 + bands.numeric_tier))
            m2, b2 = 0.0, k
            op1 = ctx.rng.choice([">", "\\ge"])
            op2 = ctx.rng.choice(["<", "\\le"])
            e1 = "x"
            e2 = str(int(k))
            upgrades = ("easy_halfplanes",)
        else:
            line1 = sample_graphable_line(ctx)
            line2 = sample_graphable_line(ctx)
            m1, b1 = float(line1.m), float(line1.b)
            m2, b2 = float(line2.m), float(line2.b)
            op1 = ctx.rng.choice(["<", ">", "\\le", "\\ge"])
            op2 = ctx.rng.choice(["<", ">", "\\le", "\\ge"])
            e1 = slope_intercept_latex(line1.m, line1.b).replace("y = ", "")
            e2 = slope_intercept_latex(line2.m, line2.b).replace("y = ", "")
            upgrades = ("two_slopes",)
        latex = f"\\begin{{cases}} y {op1} {e1} \\\\ y {op2} {e2} \\end{{cases}}"
        answer = latex if include_answer_key else None
        meta: dict[str, Any] = {
            **ctx.metadata(),
            "primitive_engine": "graph_systems_inequalities",
            "skeleton_pattern": "GraphSystemIneq",
            "upgrades": list(upgrades),
        }
        try:
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
    "a2_equations_and_inequalities_literal_equations": literal_equations,
    "slope": slope,
    "more_on_slope": more_on_slope,
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
    "graph_single_variable_inequality": _graphing_single_variable_inequalities,
    "graph_inequality_number_line": _graphing_single_variable_inequalities,
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
    # Narrative frameworks in word_problems.py — do not override with
    # equation-with-story stubs: mixture / DRT / work / age / coin /
    # consecutive / percent.
    "wp_proportion": _wp_generator("proportion"),
    "wp_inequality": _wp_generator("inequality"),
    "wp_systems": _wp_generator("systems"),
    "wp_similar_figures": _wp_similar_figures,
    "a2_linear_relations_and_functions_writing_linear_equations": writing_linear_equations,
}
