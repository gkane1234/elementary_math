"""Multi-step inequalities — framework-backed type."""

from question_engine.frameworks.equation import MultiStepInequalitiesFramework
from question_engine.types._framework_type import register_framework_type

register_framework_type(
    "multi_step_inequalities",
    MultiStepInequalitiesFramework(),
    setting_profile="inequality",
    exclude_settings=("steps",),
)
