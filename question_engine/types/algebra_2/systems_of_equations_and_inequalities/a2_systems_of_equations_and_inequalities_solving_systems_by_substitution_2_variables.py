"""A2 systems substitution — framework-backed with systems settings profile."""

from question_engine.frameworks.linear import SystemsSubstitutionFramework
from question_engine.types._linear_type import register_linear_type

register_linear_type(
    "a2_systems_of_equations_and_inequalities_solving_systems_by_substitution_2_variables",
    SystemsSubstitutionFramework(),
    profile="systems",
)
