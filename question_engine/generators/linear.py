"""Linear functions, systems, relations, and variation generators."""

from __future__ import annotations

from typing import Callable

from ..core.models import Question
from ..frameworks.adapters import framework_generators
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

GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = framework_generators(
    {
        "writing_linear_equations": WritingLinearEquationsFramework(),
        "slope": SlopeFramework(),
        "more_on_slope": SlopeFramework(multi_mode=True),
        "plotting_points": PlottingPointsFramework(),
        "systems_elimination": SystemsEliminationFramework(),
        "systems_substitution": SystemsSubstitutionFramework(),
        "direct_inverse_variation": DirectVariationFramework(),
        "discrete_relations": DiscreteRelationsFramework(),
        "continuous_relations": ContinuousRelationsFramework(),
        "evaluating_graphing_functions": EvaluatingGraphingFunctionsFramework(),
    }
)
