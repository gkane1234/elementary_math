"""Algebra 2 compound inequalities — framework-backed type."""

from question_engine.frameworks.equation import CompoundInequalitiesFramework
from question_engine.types._framework_type import register_framework_type

register_framework_type(
    "a2_equations_and_inequalities_compound_inequalities",
    CompoundInequalitiesFramework(),
    setting_profile="compound_inequality",
    exclude_settings=("steps",),
)
