"""A2 evaluating and graphing functions — framework-backed with relations settings profile."""

from question_engine.frameworks.linear import EvaluatingGraphingFunctionsFramework
from question_engine.types._linear_type import register_linear_type

register_linear_type(
    "a2_relations_and_introduction_to_functions_evaluating_and_graphing_functions",
    EvaluatingGraphingFunctionsFramework(),
    profile="relations",
)
