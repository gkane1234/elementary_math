"""A2 systems elimination — framework-backed with systems settings profile."""

from question_engine.frameworks.linear import SystemsEliminationFramework
from question_engine.types._linear_type import register_linear_type

register_linear_type(
    "a2_systems_of_equations_and_inequalities_solving_systems_by_elimination_2_variables",
    SystemsEliminationFramework(),
    profile="systems",
)
