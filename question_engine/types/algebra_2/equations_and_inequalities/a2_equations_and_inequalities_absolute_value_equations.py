"""Algebra 2 absolute value equations — framework-backed type."""

from question_engine.frameworks.equation import AbsoluteValueEquationsFramework
from question_engine.types._framework_type import register_framework_type

register_framework_type(
    "a2_equations_and_inequalities_absolute_value_equations",
    AbsoluteValueEquationsFramework(),
    setting_profile="equation",
    exclude_settings=(
        "allow_add",
        "allow_subtract",
        "allow_multiply",
        "allow_divide",
    ),
)
