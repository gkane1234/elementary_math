"""Geo parallel writing linear equations — linear settings profile."""

from question_engine.frameworks.linear import WritingLinearEquationsFramework
from question_engine.types._linear_type import register_linear_type

register_linear_type(
    "geo_parallel_writing_linear_equations",
    WritingLinearEquationsFramework(),
)
