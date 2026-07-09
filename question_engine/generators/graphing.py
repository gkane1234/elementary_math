"""Coordinate-plane and number-line graphing generators."""

from __future__ import annotations

from typing import Callable

from ..core.models import Question
from ..frameworks.graphing import (
    GraphAbsoluteValueFramework,
    GraphExponentialFramework,
    GraphInequalityFramework,
    GraphLinearEquationFramework,
    GraphPointTableFramework,
    GraphQuadraticFramework,
    GraphQuadraticInequalityFramework,
    GraphSystemFramework,
    GraphSystemInequalitiesFramework,
    GraphTransformationsFramework,
    NumberLinePlotFramework,
    ReadInterceptFromGraphFramework,
    ReadSlopeFromGraphFramework,
)

_GRAPH_LINEAR = GraphLinearEquationFramework()
_GRAPH_INEQUALITY = GraphInequalityFramework()
_GRAPH_INEQUALITY_NUMBER_LINE = GraphInequalityFramework(default_dimension="number_line")
_GRAPH_LINEAR_INEQUALITY = GraphInequalityFramework()
_GRAPH_ABSOLUTE_VALUE = GraphAbsoluteValueFramework()
_GRAPH_SYSTEM = GraphSystemFramework()
_GRAPH_SYSTEM_INEQUALITIES = GraphSystemInequalitiesFramework()
_GRAPH_EXPONENTIAL = GraphExponentialFramework()
_GRAPH_QUADRATIC = GraphQuadraticFramework()
_GRAPH_QUADRATIC_INEQUALITY = GraphQuadraticInequalityFramework()
_NUMBER_LINE_PLOT = NumberLinePlotFramework()
_READ_SLOPE = ReadSlopeFromGraphFramework()
_READ_INTERCEPT = ReadInterceptFromGraphFramework()
_GRAPH_POINT_TABLE = GraphPointTableFramework()
_GRAPH_TRANSFORMATIONS = GraphTransformationsFramework()
_GRAPH_SINGLE_VARIABLE = GraphInequalityFramework(default_dimension="number_line")


def _batch(framework, topic: str, settings: dict) -> list[Question]:
    return framework.generate_batch(topic, settings)


GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = {
    "graph_linear_equation": lambda topic, settings: _batch(_GRAPH_LINEAR, topic, settings),
    "graph_linear_inequality": lambda topic, settings: _batch(_GRAPH_LINEAR_INEQUALITY, topic, settings),
    "graph_inequality": lambda topic, settings: _batch(_GRAPH_INEQUALITY, topic, settings),
    "graph_inequality_number_line": lambda topic, settings: _batch(
        _GRAPH_INEQUALITY_NUMBER_LINE, topic, settings
    ),
    "graph_absolute_value": lambda topic, settings: _batch(_GRAPH_ABSOLUTE_VALUE, topic, settings),
    "graph_system": lambda topic, settings: _batch(_GRAPH_SYSTEM, topic, settings),
    "graph_system_inequalities": lambda topic, settings: _batch(
        _GRAPH_SYSTEM_INEQUALITIES, topic, settings
    ),
    "graph_exponential": lambda topic, settings: _batch(_GRAPH_EXPONENTIAL, topic, settings),
    "graph_quadratic": lambda topic, settings: _batch(_GRAPH_QUADRATIC, topic, settings),
    "graph_quadratic_inequality": lambda topic, settings: _batch(
        _GRAPH_QUADRATIC_INEQUALITY, topic, settings
    ),
    "number_line_plot": lambda topic, settings: _batch(_NUMBER_LINE_PLOT, topic, settings),
    "read_slope_from_graph": lambda topic, settings: _batch(_READ_SLOPE, topic, settings),
    "read_intercept_from_graph": lambda topic, settings: _batch(_READ_INTERCEPT, topic, settings),
    "graph_point_table": lambda topic, settings: _batch(_GRAPH_POINT_TABLE, topic, settings),
    "graph_transformations": lambda topic, settings: _batch(_GRAPH_TRANSFORMATIONS, topic, settings),
    "graph_single_variable_inequality": lambda topic, settings: _batch(
        _GRAPH_SINGLE_VARIABLE, topic, settings
    ),
}
