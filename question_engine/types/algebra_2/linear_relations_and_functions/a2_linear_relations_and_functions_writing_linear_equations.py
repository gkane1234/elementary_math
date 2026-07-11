"""A2 writing linear equations — write y=mx+b from a shown graph."""

from question_engine.frameworks.graphing import ReadEquationFromGraphFramework
from question_engine.types._graphing_type import register_graphing_type

register_graphing_type(
    "a2_linear_relations_and_functions_writing_linear_equations",
    ReadEquationFromGraphFramework(),
)
