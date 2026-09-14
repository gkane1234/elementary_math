"""A1 leftover wrappers — stamp skeleton_pattern; reuse existing generators.

Poly/factor leftovers stay on FactorProduct / PolySimplify. Quadratic solve,
radicals, numeric rationals, naming, long division, and graphing reuse the
old generators (no new engines). Opt-out flags on those generators are
unchanged.
"""

from __future__ import annotations

from typing import Any, Callable

from question_engine.core.models import Question
from question_engine.generators.basic import GENERATORS as BASIC
from question_engine.generators.graphing import GENERATORS as GRAPH
from question_engine.generators.hand_written import GENERATORS as HAND
from question_engine.generators.numbers import GENERATORS as NUM


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


def _from_basic(key: str, pattern: str, engine: str) -> Callable[[str, dict], list[Question]]:
    return _stamp(BASIC[key], pattern, engine)


def _from_hand(key: str, pattern: str, engine: str) -> Callable[[str, dict], list[Question]]:
    return _stamp(HAND[key], pattern, engine)


def _from_graph(key: str, pattern: str, engine: str) -> Callable[[str, dict], list[Question]]:
    return _stamp(GRAPH[key], pattern, engine)


def _from_num(key: str, pattern: str, engine: str) -> Callable[[str, dict], list[Question]]:
    return _stamp(NUM[key], pattern, engine)


GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = {
    "polynomial_long_division": _from_hand(
        "polynomial_long_division", "PolyLongDiv", "poly_long_division"
    ),
    "radical_simplification": _from_hand(
        "radical_simplification", "RadicalSimplify", "radical_simplification"
    ),
    "quadratic_square_roots": _from_basic(
        "quadratic_square_roots", "QuadraticSqrt", "quadratic_square_roots"
    ),
    "quadratic_formula": _from_basic(
        "quadratic_formula", "QuadraticFormula", "quadratic_formula"
    ),
    "quadratic_discriminant": _from_basic(
        "quadratic_discriminant", "QuadraticDiscriminant", "quadratic_discriminant"
    ),
    "quadratic_completing_square_constant": _from_basic(
        "quadratic_completing_square_constant",
        "CompleteSquareConst",
        "quadratic_completing_square_constant",
    ),
    "quadratic_completing_square_solve": _from_basic(
        "quadratic_completing_square_solve",
        "CompleteSquareSolve",
        "quadratic_completing_square_solve",
    ),
    "radical_add_subtract": _from_basic(
        "radical_add_subtract", "RadicalAddSub", "radical_add_subtract"
    ),
    "radical_multiply": _from_basic(
        "radical_multiply", "RadicalMul", "radical_multiply"
    ),
    "radical_divide": _from_basic(
        "radical_divide", "RadicalDiv", "radical_divide"
    ),
    "radical_equations": _from_basic(
        "radical_equations", "RadicalEq", "radical_equations"
    ),
    "graph_quadratic": _from_graph(
        "graph_quadratic", "GraphQuadratic", "graph_quadratic"
    ),
    "graph_quadratic_inequality": _from_graph(
        "graph_quadratic_inequality", "GraphQuadraticIneq", "graph_quadratic_inequality"
    ),
    "solve_polynomial_by_graphing": _from_graph(
        "solve_polynomial_by_graphing", "SolveByGraphing", "solve_polynomial_by_graphing"
    ),
    "sets_of_numbers": _from_num("sets_of_numbers", "NumberCore", "sets_of_numbers"),
    "rational_add_subtract": _from_num(
        "rational_add_subtract", "FractionAddSub", "rational_numbers"
    ),
    "rational_multiply": _from_num("rational_multiply", "FractionMul", "rational_numbers"),
    "rational_divide": _from_num("rational_divide", "FractionDiv", "rational_numbers"),
}
