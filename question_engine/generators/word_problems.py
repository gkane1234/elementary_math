"""Word-problem generators backed by ``frameworks.word_problem``."""

from __future__ import annotations

from typing import Callable

from ..core.models import Question
from ..frameworks.adapters import framework_generators
from ..frameworks.word_problem import (
    AgeProblemFramework,
    CoinProblemFramework,
    ConsecutiveIntegersFramework,
    CoordinateDistanceWordFramework,
    DistanceRateTimeFramework,
    GcfLcmWordFramework,
    InequalityWordProblemFramework,
    InterestWordProblemFramework,
    MixtureProblemFramework,
    NumberLineWordFramework,
    OneStepEquationWordFramework,
    PercentWordProblemFramework,
    PerimeterAreaFramework,
    ProportionWordProblemFramework,
    SimilarFiguresWordFramework,
    SystemsWordProblemFramework,
    TwoStepEquationWordFramework,
    WorkProblemFramework,
)

GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = framework_generators(
    {
        "wp_distance_rate_time": DistanceRateTimeFramework(),
        "wp_work": WorkProblemFramework(),
        "wp_age": AgeProblemFramework(),
        "wp_consecutive_integers": ConsecutiveIntegersFramework(),
        "wp_coin": CoinProblemFramework(),
        "wp_mixture": MixtureProblemFramework(),
        "wp_perimeter_area": PerimeterAreaFramework(),
        "wp_percent": PercentWordProblemFramework(),
        "wp_simple_and_compound_interest": InterestWordProblemFramework(),
        "wp_proportion": ProportionWordProblemFramework(),
        "wp_one_step_equation": OneStepEquationWordFramework(),
        "wp_two_step_equation": TwoStepEquationWordFramework(),
        "wp_systems": SystemsWordProblemFramework(),
        "wp_inequality": InequalityWordProblemFramework(),
        "wp_gcf_lcm": GcfLcmWordFramework(),
        "wp_number_line": NumberLineWordFramework(),
        "wp_coordinate_distance": CoordinateDistanceWordFramework(),
        "wp_similar_figures": SimilarFiguresWordFramework(),
    }
)
