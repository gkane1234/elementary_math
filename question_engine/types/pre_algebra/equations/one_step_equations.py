"""One-step equations — framework-backed type."""

from question_engine.frameworks.equation import OneStepEquationsFramework
from question_engine.types._framework_type import register_framework_type

register_framework_type(
    "one_step_equations",
    OneStepEquationsFramework(),
    setting_profile="equation",
)
