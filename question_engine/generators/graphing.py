"""Coordinate-plane and number-line graphing generators."""

from __future__ import annotations

from typing import Callable

from ..core.models import Question
from ..frameworks.adapters import framework_generators
from ..frameworks.graphing import (
    GraphAbsoluteValueFramework,
    GraphExponentialFramework,
    GraphInequalityFramework,
    GraphLinearEquationFramework,
    GraphLogarithmicFramework,
    GraphPointTableFramework,
    GraphQuadraticFramework,
    GraphQuadraticInequalityFramework,
    GraphRadicalFramework,
    GraphRationalFramework,
    GraphSystemFramework,
    GraphSystemInequalitiesFramework,
    GraphTransformationsFramework,
    NumberLinePlotFramework,
    ReadEquationFromGraphFramework,
    ReadInterceptFromGraphFramework,
    ReadSlopeFromGraphFramework,
    SolvePolynomialByGraphingFramework,
)

GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = framework_generators(
    {
        "graph_linear_equation": GraphLinearEquationFramework(),
        "graph_linear_inequality": GraphInequalityFramework(),
        "graph_inequality": GraphInequalityFramework(),
        "graph_inequality_number_line": GraphInequalityFramework(default_dimension="number_line"),
        "graph_absolute_value": GraphAbsoluteValueFramework(),
        "graph_radical": GraphRadicalFramework(),
        "graph_rational": GraphRationalFramework(),
        "graph_system": GraphSystemFramework(),
        "graph_system_inequalities": GraphSystemInequalitiesFramework(),
        "graph_exponential": GraphExponentialFramework(),
        "graph_logarithmic": GraphLogarithmicFramework(),
        "graph_quadratic": GraphQuadraticFramework(),
        "graph_quadratic_inequality": GraphQuadraticInequalityFramework(),
        "solve_polynomial_by_graphing": SolvePolynomialByGraphingFramework(),
        "number_line_plot": NumberLinePlotFramework(),
        "read_slope_from_graph": ReadSlopeFromGraphFramework(),
        "read_intercept_from_graph": ReadInterceptFromGraphFramework(),
        "read_equation_from_graph": ReadEquationFromGraphFramework(),
        "graph_point_table": GraphPointTableFramework(),
        "graph_transformations": GraphTransformationsFramework(),
        "graph_single_variable_inequality": GraphInequalityFramework(
            default_dimension="number_line"
        ),
    }
)
