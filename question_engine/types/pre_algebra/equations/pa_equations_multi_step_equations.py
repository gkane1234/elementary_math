"""Pre-Algebra multi-step equations — framework-backed type."""

from question_engine.frameworks.equation import MultiStepEquationsFramework
from question_engine.types._framework_type import register_framework_type

register_framework_type(
    "pa_equations_multi_step_equations",
    MultiStepEquationsFramework(),
    setting_profile="equation",
)
