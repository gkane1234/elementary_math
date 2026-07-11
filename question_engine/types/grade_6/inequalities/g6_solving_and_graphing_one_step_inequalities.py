"""Grade 6 one-step inequalities with graph metadata — framework-backed type."""

from question_engine.frameworks.equation import OneStepInequalitiesFramework
from question_engine.types._framework_type import register_framework_type

register_framework_type(
    "g6_solving_and_graphing_one_step_inequalities",
    OneStepInequalitiesFramework(),
    setting_profile="inequality",
    exclude_settings=("steps", "min_terms", "max_terms", "phrase_complexity", "max_phrase_operations"),
    setting_defaults={"include_graph_metadata": True},
)
