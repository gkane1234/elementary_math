"""Algebra 2 multi-step equations — framework-backed type."""

from question_engine.frameworks.equation import MultiStepEquationsFramework
from question_engine.types._framework_type import register_framework_type

register_framework_type(
    "a2_equations_and_inequalities_multi_step_equations",
    MultiStepEquationsFramework(),
    setting_profile="equation",
)
