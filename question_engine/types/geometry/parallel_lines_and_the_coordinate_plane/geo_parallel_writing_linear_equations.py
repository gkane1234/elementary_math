"""Geo parallel writing linear equations — write y=mx+b from a shown graph."""

from question_engine.frameworks.graphing import ReadEquationFromGraphFramework
from question_engine.types._graphing_type import register_graphing_type

register_graphing_type(
    "geo_parallel_writing_linear_equations",
    ReadEquationFromGraphFramework(),
)
