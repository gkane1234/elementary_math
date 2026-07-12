"""Compound inequalities — framework-backed type."""

from question_engine.frameworks.equation import CompoundInequalitiesFramework
from question_engine.types._framework_type import register_framework_type

register_framework_type(
    "compound_inequalities",
    CompoundInequalitiesFramework(),
    setting_profile="compound_inequality",
    exclude_settings=("min_terms", "max_terms", "phrase_complexity", "max_phrase_operations"),
)
