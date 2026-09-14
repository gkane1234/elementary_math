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
    require_exponents = bool(settings.get("require_exponents", False)) or (
        "with_exponents" in topic
    )

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            {**settings, "require_exponents": require_exponents},
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_OOO],
            leaf_id=topic,
        )
        expr = sample_ooo_expression(ctx, require_exponents=require_exponents)
        answer = _answer_latex(expr.value) if include_answer_key else None
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "ooo",
            "skeleton_pattern": "OrderOfOperations",
            "require_exponents": require_exponents,
            "upgrades": list(expr.upgrades),
            "n_ops": expr.n_ops,
            "nest_depth": expr.nest_depth,
            "shape_id": expr.shape_id,
            "effective_d": expr.effective_d,
        }
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


def numeric_expressions_with_exponents(topic: str, settings: dict) -> list[Question]:
    """OOO stems that always include at least one exponent."""
    return order_of_operations(topic, {**settings, "require_exponents": True})


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
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "distributive",
            "distributive_form": expr.form,
            "form_id": expr.form_id,
            "n_terms_inside": expr.n_terms_inside,
            "factor_side": expr.factor_side,
            "structure_upgrades": list(expr.upgrades),
        }
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


def _g6_algebra_settings(settings: dict) -> dict:
    """Classroom G6 defaults: no Greek vars; integers preferred at low D."""
    local = dict(settings)
    local.setdefault("allow_greek", False)
    try:
        d = float(local["difficulty"]) if local.get("difficulty") is not None else None
    except (TypeError, ValueError):
        d = None
    if d is not None and d < 8.0:
        local.setdefault("force_variable_lane", "only_x")
    elif d is not None:
        local.setdefault("force_variable_lane", "xyz")
    if d is not None and d < 12.0:
        local.setdefault("integers_only", True)
    return local


def distributive_property_algebraic(topic: str, settings: dict) -> list[Question]:
    """Algebraic distributive via shared primitive + presentation forms."""
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}
    local_settings = (
        _g6_algebra_settings(settings) if topic.startswith("g6_") else dict(settings)
    )

    def build() -> tuple[str, str, str | None]:
        from question_engine.frameworks.primitives.affine_skeleton import (
            sample_affine_inflate,
            use_affine_inflate_skeleton,
        )
        from question_engine.frameworks.primitives.distributive import (
            sample_distributive_algebraic,
        )

        ctx = build_context(
            local_settings,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_DISTRIBUTIVE],
            policy=LINEAR_POLICY,
            leaf_id=str(topic or "distributive_property_algebraic"),
        )
        if use_affine_inflate_skeleton(settings, mode="distribute"):
            expr = sample_affine_inflate(ctx, mode="distribute")
            answer = expr.answer_latex if include_answer_key else None
            last["meta"] = {
                **ctx.metadata(),
                "primitive_engine": "affine_skeleton",
                "upgrades": list(expr.upgrades),
                **expr.metadata,
            }
            return (expr.prompt_latex, expr.prompt_text, answer)
        if PRIM_NUMBERS not in ctx.prereq_settings:
            ctx.prereq_settings[PRIM_NUMBERS] = {}
        ctx.prereq_settings[PRIM_NUMBERS].setdefault("exclude_zero", True)
        expr_old = sample_distributive_algebraic(ctx)
        answer = expr_old.expanded_latex if include_answer_key else None
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "distributive_algebraic",
            "distributive_form": expr_old.form,
            "form_id": expr_old.form_id,
            "n_terms_inside": expr_old.n_terms_inside,
            "factor_side": expr_old.factor_side,
            "structure_upgrades": list(expr_old.upgrades),
            "cancel_clutter": [u for u in expr_old.upgrades if str(u).startswith("cancel:")],
        }
        return (expr_old.latex, expr_old.text, answer)

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
    local_settings = _g6_algebra_settings(settings) if topic.startswith("g6_") else dict(settings)

    def build() -> tuple[str, str, str | None]:
        from question_engine.frameworks.primitives.affine_skeleton import (
            sample_affine_inflate,
            use_affine_inflate_skeleton,
        )

        ctx = build_context(
            local_settings,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_EVALUATE],
            policy=LINEAR_POLICY,
            leaf_id=str(topic or "evaluate_algebraic_expressions"),
        )
        if use_affine_inflate_skeleton(settings, mode="evaluate"):
            expr = sample_affine_inflate(ctx, mode="evaluate")
            answer = expr.answer_latex if include_answer_key else None
            last["meta"] = {
                **ctx.metadata(),
                "primitive_engine": "affine_skeleton",
                "upgrades": list(expr.upgrades),
                **expr.metadata,
            }
            return (expr.prompt_latex, expr.prompt_text, answer)
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
    local_settings = _g6_algebra_settings(settings) if topic.startswith("g6_") else dict(settings)
    # Stretch classroom D so structure upgrades land inside the 0–25 slider
    # on the *legacy* like-terms sampler only. AffineInflate uses numeric/format
    # tiers from D directly — do not stretch when the skeleton is on.
    from question_engine.frameworks.primitives.affine_skeleton import (
        use_affine_inflate_skeleton,
    )

    if (
        topic.startswith("g6_")
        and local_settings.get("difficulty") is not None
        and not use_affine_inflate_skeleton(settings, mode="like_terms")
    ):
        try:
            d = float(local_settings["difficulty"])
            # Map 0→0, 5→9, 10→18, 15→27, 20→36, 25→45 so mid/high buy upgrades.
            local_settings["difficulty"] = d * 1.8 if d >= 1 else 0.0
        except (TypeError, ValueError):
            pass

    def build() -> tuple[str, str, str | None]:
        from question_engine.frameworks.primitives.affine_skeleton import (
            sample_affine_inflate,
            use_affine_inflate_skeleton,
        )

        ctx = build_context(
            local_settings,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_LIKE_TERMS],
            policy=LINEAR_POLICY,
            leaf_id=str(topic or "combining_like_terms"),
        )
        if use_affine_inflate_skeleton(settings, mode="like_terms"):
            expr = sample_affine_inflate(ctx, mode="like_terms")
            answer = expr.answer_latex if include_answer_key else None
            last["meta"] = {
                **ctx.metadata(),
                "primitive_engine": "affine_skeleton",
                "upgrades": list(expr.upgrades),
                **expr.metadata,
            }
            return (expr.prompt_latex, expr.prompt_text, answer)
        expr_old = sample_like_terms(ctx)
        answer = expr_old.simplified_latex if include_answer_key else None
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "like_terms",
            "upgrades": list(expr_old.upgrades),
        }
        return (expr_old.latex, expr_old.text, answer)

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
        from question_engine.frameworks.primitives.affine_skeleton import (
            sample_affine_inflate,
            use_affine_inflate_skeleton,
        )

        ctx = build_context(
            settings,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_EXPAND_SIMPLIFY],
            policy=LINEAR_POLICY,
            leaf_id=str(topic or "expand_simplify"),
        )
        if use_affine_inflate_skeleton(settings, mode="expand"):
            expr = sample_affine_inflate(ctx, mode="expand")
            answer = expr.answer_latex if include_answer_key else None
            last["meta"] = {
                **ctx.metadata(),
                "primitive_engine": "affine_skeleton",
                "upgrades": list(expr.upgrades),
                **expr.metadata,
            }
            return (expr.prompt_latex, expr.prompt_text, answer)
        expr_old = sample_expand_simplify(ctx)
        answer = expr_old.simplified_latex if include_answer_key else None
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "expand_simplify",
            "upgrades": list(expr_old.upgrades),
            "n_groups": expr_old.n_groups,
            "n_lone": expr_old.n_lone,
            "nested": expr_old.nested,
            "nest_depth": expr_old.nest_depth,
            "coeff_a": str(expr_old.coeff_a),
            "coeff_b": str(expr_old.coeff_b),
        }
        return (expr_old.latex, expr_old.text, answer)

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
            from question_engine.frameworks.primitives.equation_skeleton import (
                sample_solve_linear,
                use_solve_linear_skeleton,
            )

            ctx = build_context(
                local,
                [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_EQUATIONS],
                policy=LINEAR_POLICY,
                leaf_id=str(topic or ""),
            )
            force = force_steps if force_steps in {"one", "two", "multi"} else None
            if use_solve_linear_skeleton(local):
                eq = sample_solve_linear(ctx, force_steps=force)
                if eq.solution_kind == "unique":
                    answer = (
                        f"{eq.var_latex} = {eq.solution_latex}"
                        if include_answer_key
                        else None
                    )
                else:
                    answer = eq.solution_latex if include_answer_key else None
                last["meta"] = {
                    **ctx.metadata(),
                    "primitive_engine": "equation_skeleton",
                    "steps": eq.steps,
                    "n_ops": eq.n_ops,
                    "upgrades": list(eq.upgrades),
                    "solution_kind": eq.solution_kind,
                    **eq.metadata,
                }
                return (eq.latex, eq.text, answer)

            eq_old = sample_linear_equation(ctx, force_steps=force)
            if eq_old.solution_kind == "unique":
                answer = (
                    f"{eq_old.var_latex} = {eq_old.solution_latex}"
                    if include_answer_key
                    else None
                )
            else:
                answer = eq_old.solution_latex if include_answer_key else None
            last["meta"] = {
                **ctx.metadata(),
                "primitive_engine": "equations",
                "steps": eq_old.steps,
                "n_ops": eq_old.n_ops,
                "upgrades": list(eq_old.upgrades),
                "solution_kind": eq_old.solution_kind,
            }
            return (eq_old.latex, eq_old.text, answer)

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
            from question_engine.frameworks.primitives.equation_skeleton import (
                sample_solve_inequality,
                use_solve_inequality_skeleton,
            )

            ctx = build_context(
                local,
                [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_INEQUALITIES],
                policy=LINEAR_POLICY,
                leaf_id=str(topic or ""),
            )
            force = force_steps if force_steps in {"one", "two", "multi"} else None
            if use_solve_inequality_skeleton(local):
                ineq = sample_solve_inequality(ctx, force_steps=force)
                answer = ineq.solution_latex if include_answer_key else None
                meta: dict[str, Any] = {
                    **ctx.metadata(),
                    "primitive_engine": "equation_skeleton",
                    "steps": ineq.steps,
                    "n_ops": ineq.n_ops,
                    "flipped": ineq.flipped,
                    "upgrades": list(ineq.upgrades),
                    **ineq.metadata,
                }
                try:
                    spec = number_line_spec_from_symbol_and_value(
                        ineq.number_line_op,
                        float(ineq.solution_value),
                        local,
                    )
                    meta.update(metadata_from_number_line_spec(spec, prompt="blank"))
                except (TypeError, ValueError):
                    pass
                last["meta"] = meta
                return (ineq.latex, ineq.text, answer)

            ineq_old = sample_linear_inequality(ctx, force_steps=force)
            answer = ineq_old.solution_latex if include_answer_key else None
            meta = {
                **ctx.metadata(),
                "primitive_engine": "inequalities",
                "steps": ineq_old.steps,
                "n_ops": ineq_old.n_ops,
                "flipped": ineq_old.flipped,
                "upgrades": list(ineq_old.upgrades),
            }
            # Blank prompt number line + shaded answer (matches legacy inequality frameworks).
            try:
                spec = number_line_spec_from_symbol_and_value(
                    ineq_old.op,
                    float(ineq_old.solution_value),
                    local,
                )
                meta.update(metadata_from_number_line_spec(spec, prompt="blank"))
            except (TypeError, ValueError):
                pass
            last["meta"] = meta
            return (ineq_old.latex, ineq_old.text, answer)

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
        from question_engine.frameworks.primitives.poly_skeleton import (
            sample_factor_product_item,
            use_factor_product_skeleton,
        )

        local = dict(settings)
        if "integers_only" not in local:
            local["integers_only"] = True
        ctx = build_context(
            local,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_FACTOR_GCF],
            policy=LINEAR_POLICY,
            leaf_id=str(topic or "factor_gcf"),
        )
        if use_factor_product_skeleton(settings):
            item = sample_factor_product_item(
                ctx, task="factor", leaf_id=str(topic or "factor_gcf")
            )
            answer = item.answer_latex if include_answer_key else None
            last["meta"] = {
                **ctx.metadata(),
                "primitive_engine": "poly_skeleton",
                "upgrades": list(item.upgrades),
                **item.metadata,
            }
            return (item.prompt_latex, item.prompt_text, answer)
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


def check_equation_solution(topic: str, settings: dict) -> list[Question]:
    """Is x=k a solution? Default SolveLinear; opt out keeps the old hand leaf."""
    from question_engine.frameworks.primitives.equation_skeleton import (
        sample_check_equation,
        use_solve_linear_skeleton,
    )
    from question_engine.generators.grade_level import (
        check_equation_solution as _old_check,
    )

    if not use_solve_linear_skeleton(settings):
        return _old_check(topic, settings)

    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}
    local = _g6_algebra_settings(settings)
    try:
        d = float(local["difficulty"]) if local.get("difficulty") is not None else 0.0
    except (TypeError, ValueError):
        d = 0.0
    # Old D≥21 used fraction coeffs even when integers_only was set.
    if d >= 21.0:
        local["integers_only"] = False

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            local,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_EQUATIONS],
            policy=LINEAR_POLICY,
            leaf_id=str(topic or "g6_solutions_to_equations"),
        )
        eq = sample_check_equation(ctx)
        answer = eq.solution_latex if include_answer_key else None
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "equation_skeleton",
            "upgrades": list(eq.upgrades),
            **eq.metadata,
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
        settings=settings,
    )


def write_one_step_equation(topic: str, settings: dict) -> list[Question]:
    """Write d=rt / cost / perimeter then find the value. Opt out = old hand leaf."""
    from question_engine.frameworks.primitives.equation_skeleton import (
        use_solve_linear_skeleton,
    )
    from question_engine.frameworks.primitives.wp_packaging import sample_write_one_step
    from question_engine.generators.grade_level import (
        write_one_step_equation as _old_write,
    )

    if not use_solve_linear_skeleton(settings):
        return _old_write(topic, settings)

    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}
    local = _g6_algebra_settings(settings)
    local.setdefault("force_steps", "one")
    other = "other_relationship" in str(topic or "")

    def build() -> tuple[str, str, str | None]:
        ctx = build_context(
            local,
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_EQUATIONS],
            policy=LINEAR_POLICY,
            leaf_id=str(topic or "write_one_step_equation"),
        )
        item = sample_write_one_step(ctx, other=other)
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


GENERATORS = {
    "order_of_operations": order_of_operations,
    # Catalog leaves that share the continuous OOO / expression-exponents path.
    "g6_numeric_expressions_with_exponents": numeric_expressions_with_exponents,
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
    "check_equation_solution": check_equation_solution,
    "g6_solutions_to_equations": check_equation_solution,
    "write_one_step_equation": write_one_step_equation,
    "g6_constant_rate_equations": write_one_step_equation,
    "g6_equations_for_other_relationships": write_one_step_equation,
}
