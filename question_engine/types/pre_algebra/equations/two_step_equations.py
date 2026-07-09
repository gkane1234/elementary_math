"""Two-step equations — framework-backed type."""

from question_engine.frameworks.equation import TwoStepEquationsFramework
from question_engine.types._framework_type import register_framework_type

register_framework_type(
    "two_step_equations",
    TwoStepEquationsFramework(),
    setting_profile="equation",
)
