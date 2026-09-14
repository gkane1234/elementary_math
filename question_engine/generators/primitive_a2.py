"""A2 catalog wrappers — stamp skeleton_pattern; reuse A1 / skeleton engines.

Complex algebra, 3-var systems, and variation packaging live here. Equation /
rational / poly / WP families reuse existing primitive modules; this module only
adds stamps and A2 ``type_id`` aliases where the catalog generator key differs.
"""

from __future__ import annotations

from typing import Any, Callable

from question_engine.core.models import Question
from question_engine.generators.algebra2 import GENERATORS as _A2
from question_engine.generators.grade_level import GENERATORS as _GRADE
from question_engine.generators.primitive_linear import (
    _system_generator,
    _wp_generator,
    writing_linear_equations,
)
from question_engine.generators.word_problems import GENERATORS as _WP


def _stamp(
    fn: Callable[[str, dict], list[Question]],
    pattern: str,
    engine: str,
) -> Callable[[str, dict], list[Question]]:
    def generate(topic: str, settings: dict) -> list[Question]:
        qs = fn(topic, settings)
        for q in qs:
            md: dict[str, Any] = dict(q.metadata or {})
            md["skeleton_pattern"] = pattern
            md.setdefault("primitive_engine", engine)
            q.metadata = md
        return qs

    return generate


def _variation(topic: str, settings: dict) -> list[Question]:
    from question_engine.frameworks.primitives import PRIM_NUMBERS, PRIM_VARIABLE, build_context
    from question_engine.frameworks.primitives.wp_packaging import (
        sample_variation_packaged,
        use_variation_packaging,
    )
    from question_engine.generators.utils import make_questions

    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}

    def build() -> tuple[str, str, str | None]:
        if not use_variation_packaging(settings):
            from question_engine.generators.linear import GENERATORS as LIN

            qs = LIN["direct_inverse_variation"](topic, settings)
            q = qs[0]
            last["meta"] = dict(q.metadata or {})
            return q.prompt_latex or "", q.prompt_text or "", q.answer_latex

        ctx = build_context(
            settings,
            [PRIM_NUMBERS, PRIM_VARIABLE],
            leaf_id=str(topic or "direct_inverse_variation"),
        )
        item = sample_variation_packaged(ctx)
        last["meta"] = {
            **ctx.metadata(),
            **dict(item.metadata or {}),
            "primitive_engine": "variation_packaging",
            "skeleton_pattern": "VariationEq",
            "frame_id": item.frame,
            "upgrades": list(item.upgrades),
        }
        answer = item.answer_latex if include_answer_key else None
        return item.latex, item.text, answer

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


GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = {
    "direct_inverse_variation": _variation,
    "a2_direct_and_inverse_variation_direct_and_inverse_variation": _variation,
    "complex_operations": _stamp(_A2["complex_operations"], "ComplexOp", "complex_algebra"),
    "a2_complex_numbers_operations": _stamp(
        _A2["complex_operations"], "ComplexOp", "complex_algebra"
    ),
    "complex_absolute_value": _stamp(
        _A2["complex_absolute_value"], "ComplexAbs", "complex_algebra"
    ),
    "a2_complex_numbers_absolute_value": _stamp(
        _A2["complex_absolute_value"], "ComplexAbs", "complex_algebra"
    ),
    "complex_rationalize_denominator": _stamp(
        _GRADE["complex_rationalize_denominator"],
        "ComplexRationalize",
        "complex_algebra",
    ),
    "a2_complex_numbers_rationalizing_denominators": _stamp(
        _GRADE["complex_rationalize_denominator"],
        "ComplexRationalize",
        "complex_algebra",
    ),
    "system_three_variables": _stamp(
        _A2["system_three_variables"], "LinearSystem3", "systems"
    ),
    "a2_systems_of_equations_and_inequalities_solving_systems_with_three_variables": _stamp(
        _A2["system_three_variables"], "LinearSystem3", "systems"
    ),
    "a2_systems_of_equations_and_inequalities_solving_systems_by_elimination_2_variables": _system_generator(
        "elimination"
    ),
    "a2_systems_of_equations_and_inequalities_solving_systems_by_substitution_2_variables": _system_generator(
        "substitution"
    ),
    "a2_systems_of_equations_and_inequalities_solving_systems_by_graphing_2_variables": _system_generator(
        "graphing"
    ),
    "a2_linear_relations_and_functions_writing_linear_equations": writing_linear_equations,
    "a2_equations_and_inequalities_work_word_problems": _WP["wp_work"],
    "a2_equations_and_inequalities_distance_rate_time_word_problems": _WP["wp_distance_rate_time"],
    "a2_equations_and_inequalities_mixture_word_problems": _WP["wp_mixture"],
    "a2_systems_of_equations_and_inequalities_systems_of_equations_word_problems_2_variables": _wp_generator(
        "systems"
    ),
}
