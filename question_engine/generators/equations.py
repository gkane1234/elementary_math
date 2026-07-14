"""Equation and inequality generators backed by frameworks."""

from __future__ import annotations

from typing import Callable

from ..core.models import Question
from ..frameworks.adapters import framework_generators
from ..frameworks.equation import (
    AbsoluteValueEquationsFramework,
    AbsoluteValueInequalitiesFramework,
    CompoundInequalitiesFramework,
    LiteralEquationsFramework,
    MultiStepEquationsFramework,
    MultiStepInequalitiesFramework,
    OneStepEquationsFramework,
    OneStepInequalitiesFramework,
    TwoStepEquationsFramework,
    TwoStepInequalitiesFramework,
)

GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = framework_generators(
    {
        "one_step_equations": OneStepEquationsFramework(),
        "two_step_equations": TwoStepEquationsFramework(),
        "multi_step_equations": MultiStepEquationsFramework(),
        "literal_equations": LiteralEquationsFramework(),
        "absolute_value_equations": AbsoluteValueEquationsFramework(),
        "one_step_inequalities": OneStepInequalitiesFramework(),
        "two_step_inequalities": TwoStepInequalitiesFramework(),
        "multi_step_inequalities": MultiStepInequalitiesFramework(),
        "compound_inequalities": CompoundInequalitiesFramework(),
        "absolute_value_inequalities": AbsoluteValueInequalitiesFramework(),
    }
)
