"""Slope — framework-backed with linear settings profile."""

from question_engine.frameworks.linear import SlopeFramework
from question_engine.types._linear_type import register_linear_type

register_linear_type("slope", SlopeFramework())
