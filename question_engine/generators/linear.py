"""Linear functions, systems, relations, and variation generators."""

from __future__ import annotations

from typing import Callable

from ..core.models import Question
from ..frameworks.linear import (
    ContinuousRelationsFramework,
    DirectVariationFramework,
    DiscreteRelationsFramework,
    EvaluatingGraphingFunctionsFramework,
    PlottingPointsFramework,
    SlopeFramework,
    SystemsEliminationFramework,
    SystemsSubstitutionFramework,
    WritingLinearEquationsFramework,
)

_WRITING_LINEAR = WritingLinearEquationsFramework()
_SLOPE = SlopeFramework()
_MORE_ON_SLOPE = SlopeFramework(multi_mode=True)
_PLOTTING_POINTS = PlottingPointsFramework()
_SYSTEMS_ELIMINATION = SystemsEliminationFramework()
_SYSTEMS_SUBSTITUTION = SystemsSubstitutionFramework()
_DIRECT_VARIATION = DirectVariationFramework()
_DISCRETE_RELATIONS = DiscreteRelationsFramework()
_CONTINUOUS_RELATIONS = ContinuousRelationsFramework()
_EVALUATING_GRAPHING = EvaluatingGraphingFunctionsFramework()


def _batch(framework, topic: str, settings: dict) -> list[Question]:
    return framework.generate_batch(topic, settings)


GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = {
    "writing_linear_equations": lambda topic, settings: _batch(_WRITING_LINEAR, topic, settings),
    "slope": lambda topic, settings: _batch(_SLOPE, topic, settings),
    "more_on_slope": lambda topic, settings: _batch(_MORE_ON_SLOPE, topic, settings),
    "plotting_points": lambda topic, settings: _batch(_PLOTTING_POINTS, topic, settings),
    "systems_elimination": lambda topic, settings: _batch(_SYSTEMS_ELIMINATION, topic, settings),
    "systems_substitution": lambda topic, settings: _batch(_SYSTEMS_SUBSTITUTION, topic, settings),
    "direct_inverse_variation": lambda topic, settings: _batch(_DIRECT_VARIATION, topic, settings),
    "discrete_relations": lambda topic, settings: _batch(_DISCRETE_RELATIONS, topic, settings),
    "continuous_relations": lambda topic, settings: _batch(_CONTINUOUS_RELATIONS, topic, settings),
    "evaluating_graphing_functions": lambda topic, settings: _batch(_EVALUATING_GRAPHING, topic, settings),
}
