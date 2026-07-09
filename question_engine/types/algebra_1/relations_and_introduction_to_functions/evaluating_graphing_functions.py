"""Evaluating and graphing functions — framework-backed with relations settings profile."""

from question_engine.frameworks.linear import EvaluatingGraphingFunctionsFramework
from question_engine.types._linear_type import register_linear_type

register_linear_type(
    "evaluating_graphing_functions",
    EvaluatingGraphingFunctionsFramework(),
    profile="relations",
)
