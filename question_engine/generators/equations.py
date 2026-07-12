"""Equation and inequality generators backed by frameworks."""

from __future__ import annotations

from typing import Callable

from ..core.models import Question
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

_FRAMEWORKS = {
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


def _framework_generator(key: str) -> Callable[[str, dict], list[Question]]:
    framework = _FRAMEWORKS[key]

    def generate(topic: str, settings: dict) -> list[Question]:
        return framework.generate_batch(topic, settings)

    return generate


GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = {
    key: _framework_generator(key) for key in _FRAMEWORKS
}
