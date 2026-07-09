"""Word-problem generators backed by ``frameworks.word_problem``."""

from __future__ import annotations

from typing import Callable

from ..core.models import Question
from ..frameworks.word_problem import (
    AgeProblemFramework,
    CoinProblemFramework,
    ConsecutiveIntegersFramework,
    CoordinateDistanceWordFramework,
    DistanceRateTimeFramework,
    GcfLcmWordFramework,
    InequalityWordProblemFramework,
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

_DRT = DistanceRateTimeFramework()
_WORK = WorkProblemFramework()
_AGE = AgeProblemFramework()
_CONSECUTIVE = ConsecutiveIntegersFramework()
_COIN = CoinProblemFramework()
_MIXTURE = MixtureProblemFramework()
_PERIMETER_AREA = PerimeterAreaFramework()
_PERCENT = PercentWordProblemFramework()
_PROPORTION = ProportionWordProblemFramework()
_ONE_STEP = OneStepEquationWordFramework()
_TWO_STEP = TwoStepEquationWordFramework()
_SYSTEMS = SystemsWordProblemFramework()
_INEQUALITY = InequalityWordProblemFramework()
_GCF_LCM = GcfLcmWordFramework()
_NUMBER_LINE = NumberLineWordFramework()
_COORDINATE_DISTANCE = CoordinateDistanceWordFramework()
_SIMILAR_FIGURES = SimilarFiguresWordFramework()


def _batch(framework, topic: str, settings: dict) -> list[Question]:
    return framework.generate_batch(topic, settings)


GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = {
    "wp_distance_rate_time": lambda topic, settings: _batch(_DRT, topic, settings),
    "wp_work": lambda topic, settings: _batch(_WORK, topic, settings),
    "wp_age": lambda topic, settings: _batch(_AGE, topic, settings),
    "wp_consecutive_integers": lambda topic, settings: _batch(_CONSECUTIVE, topic, settings),
    "wp_coin": lambda topic, settings: _batch(_COIN, topic, settings),
    "wp_mixture": lambda topic, settings: _batch(_MIXTURE, topic, settings),
    "wp_perimeter_area": lambda topic, settings: _batch(_PERIMETER_AREA, topic, settings),
    "wp_percent": lambda topic, settings: _batch(_PERCENT, topic, settings),
    "wp_proportion": lambda topic, settings: _batch(_PROPORTION, topic, settings),
    "wp_one_step_equation": lambda topic, settings: _batch(_ONE_STEP, topic, settings),
    "wp_two_step_equation": lambda topic, settings: _batch(_TWO_STEP, topic, settings),
    "wp_systems": lambda topic, settings: _batch(_SYSTEMS, topic, settings),
    "wp_inequality": lambda topic, settings: _batch(_INEQUALITY, topic, settings),
    "wp_gcf_lcm": lambda topic, settings: _batch(_GCF_LCM, topic, settings),
    "wp_number_line": lambda topic, settings: _batch(_NUMBER_LINE, topic, settings),
    "wp_coordinate_distance": lambda topic, settings: _batch(_COORDINATE_DISTANCE, topic, settings),
    "wp_similar_figures": lambda topic, settings: _batch(_SIMILAR_FIGURES, topic, settings),
}
