"""PA systems substitution — framework-backed with systems settings profile."""

from question_engine.frameworks.linear import SystemsSubstitutionFramework
from question_engine.types._linear_type import register_linear_type

register_linear_type(
    "pa_systems_substitution",
    SystemsSubstitutionFramework(),
    profile="systems",
)
