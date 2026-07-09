"""Algebra 2 absolute value inequalities — framework-backed type."""

from question_engine.frameworks.equation import AbsoluteValueInequalitiesFramework
from question_engine.types._framework_type import register_framework_type

register_framework_type(
    "a2_equations_and_inequalities_absolute_value_inequalities",
    AbsoluteValueInequalitiesFramework(),
    setting_profile="inequality",
    exclude_settings=("steps",),
)
