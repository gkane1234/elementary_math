"""Systems elimination — framework-backed with systems settings profile."""

from question_engine.frameworks.linear import SystemsEliminationFramework
from question_engine.types._linear_type import register_linear_type

register_linear_type(
    "systems_elimination",
    SystemsEliminationFramework(),
    profile="systems",
)
