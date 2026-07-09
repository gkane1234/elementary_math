"""Statistics and probability question generators."""

from __future__ import annotations

from typing import Callable

from ..core.models import Question
from ..frameworks.statistics import (
    BoxPlotBasicsFramework,
    CenterSpreadFramework,
    CompoundIndependentProbabilityFramework,
    CountingPrincipleFramework,
    DotPlotReadFramework,
    HistogramReadFramework,
    MeanFramework,
    MedianFramework,
    ModeFramework,
    MutuallyExclusiveProbabilityFramework,
    RangeFramework,
    SingleEventProbabilityFramework,
)

_MEAN = MeanFramework()
_MEDIAN = MedianFramework()
_MODE = ModeFramework()
_RANGE = RangeFramework()
_CENTER_SPREAD = CenterSpreadFramework()
_DOT_PLOT_READ = DotPlotReadFramework()
_HISTOGRAM_READ = HistogramReadFramework()
_BOX_PLOT_BASICS = BoxPlotBasicsFramework()
_PROBABILITY_SINGLE = SingleEventProbabilityFramework()
_PROBABILITY_COMPOUND = CompoundIndependentProbabilityFramework()
_PROBABILITY_MUTUALLY_EXCLUSIVE = MutuallyExclusiveProbabilityFramework()
_COUNTING_PRINCIPLE = CountingPrincipleFramework()


def _batch(framework, topic: str, settings: dict) -> list[Question]:
    return framework.generate_batch(topic, settings)


def stats_mean(topic: str, settings: dict) -> list[Question]:
    return _batch(_MEAN, topic, settings)


def stats_median(topic: str, settings: dict) -> list[Question]:
    return _batch(_MEDIAN, topic, settings)


def stats_mode(topic: str, settings: dict) -> list[Question]:
    return _batch(_MODE, topic, settings)


def stats_range(topic: str, settings: dict) -> list[Question]:
    return _batch(_RANGE, topic, settings)


def stats_center_spread(topic: str, settings: dict) -> list[Question]:
    return _batch(_CENTER_SPREAD, topic, settings)


def stats_dot_plot_read(topic: str, settings: dict) -> list[Question]:
    return _batch(_DOT_PLOT_READ, topic, settings)


def stats_histogram_read(topic: str, settings: dict) -> list[Question]:
    return _batch(_HISTOGRAM_READ, topic, settings)


def stats_box_plot_basics(topic: str, settings: dict) -> list[Question]:
    return _batch(_BOX_PLOT_BASICS, topic, settings)


def stats_probability_single(topic: str, settings: dict) -> list[Question]:
    return _batch(_PROBABILITY_SINGLE, topic, settings)


def stats_probability_compound_independent(topic: str, settings: dict) -> list[Question]:
    return _batch(_PROBABILITY_COMPOUND, topic, settings)


def stats_probability_mutually_exclusive(topic: str, settings: dict) -> list[Question]:
    return _batch(_PROBABILITY_MUTUALLY_EXCLUSIVE, topic, settings)


def stats_counting_principle(topic: str, settings: dict) -> list[Question]:
    return _batch(_COUNTING_PRINCIPLE, topic, settings)


GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = {
    "stats_mean": stats_mean,
    "stats_median": stats_median,
    "stats_mode": stats_mode,
    "stats_range": stats_range,
    "stats_center_spread": stats_center_spread,
    "stats_dot_plot_read": stats_dot_plot_read,
    "stats_histogram_read": stats_histogram_read,
    "stats_box_plot_basics": stats_box_plot_basics,
    "stats_probability_single": stats_probability_single,
    "stats_probability_compound_independent": stats_probability_compound_independent,
    "stats_probability_mutually_exclusive": stats_probability_mutually_exclusive,
    "stats_counting_principle": stats_counting_principle,
}
