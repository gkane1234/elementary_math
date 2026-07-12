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
    StatisticalModelFramework,
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
_STATISTICAL_MODEL = StatisticalModelFramework()


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


def stats_statistical_model(topic: str, settings: dict) -> list[Question]:
    return _batch(_STATISTICAL_MODEL, topic, settings)


def stats_probability_single(topic: str, settings: dict) -> list[Question]:
    return _batch(_PROBABILITY_SINGLE, topic, settings)


def stats_probability_compound_independent(topic: str, settings: dict) -> list[Question]:
    return _batch(_PROBABILITY_COMPOUND, topic, settings)


def stats_probability_mutually_exclusive(topic: str, settings: dict) -> list[Question]:
    return _batch(_PROBABILITY_MUTUALLY_EXCLUSIVE, topic, settings)


def stats_counting_principle(topic: str, settings: dict) -> list[Question]:
    return _batch(_COUNTING_PRINCIPLE, topic, settings)


def _stats_permutations(topic: str, settings: dict) -> list[Question]:
    from ..generators.utils import _make_questions
    import math
    import random

    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build():
        n = random.randint(5, 10)
        r = random.randint(2, min(4, n))
        prompt = rf"\text{{Evaluate }} {{}}_{{{n}}}P_{{{r}}}."
        answer = str(math.perm(n, r))
        return prompt, "permutation", answer if keyed else None

    return _make_questions(topic, count, keyed, build)


def _stats_combinations(topic: str, settings: dict) -> list[Question]:
    from ..generators.utils import _make_questions
    import math
    import random

    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build():
        n = random.randint(5, 12)
        r = random.randint(2, min(5, n))
        prompt = rf"\text{{Evaluate }} {{}}_{{{n}}}C_{{{r}}}."
        answer = str(math.comb(n, r))
        return prompt, "combination", answer if keyed else None

    return _make_questions(topic, count, keyed, build)


def _stats_permutations_vs_combinations(topic: str, settings: dict) -> list[Question]:
    from ..generators.utils import _make_questions
    import math
    import random

    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build():
        n = random.randint(6, 10)
        r = random.randint(2, 4)
        if random.choice([True, False]):
            prompt = (
                rf"\text{{How many ways can {r} students be lined up from a class of {n}?}}"
            )
            answer = str(math.perm(n, r))
            kind = "permutation context"
        else:
            prompt = (
                rf"\text{{How many ways can {r} students be chosen from a class of {n}?}}"
            )
            answer = str(math.comb(n, r))
            kind = "combination context"
        return prompt, kind, answer if keyed else None

    return _make_questions(topic, count, keyed, build)


GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = {
    "stats_mean": stats_mean,
    "stats_median": stats_median,
    "stats_mode": stats_mode,
    "stats_range": stats_range,
    "stats_center_spread": stats_center_spread,
    "stats_dot_plot_read": stats_dot_plot_read,
    "stats_histogram_read": stats_histogram_read,
    "stats_box_plot_basics": stats_box_plot_basics,
    "stats_statistical_model": stats_statistical_model,
    "stats_probability_single": stats_probability_single,
    "stats_probability_compound_independent": stats_probability_compound_independent,
    "stats_probability_mutually_exclusive": stats_probability_mutually_exclusive,
    "stats_counting_principle": stats_counting_principle,
    "stats_permutations": _stats_permutations,
    "stats_combinations": _stats_combinations,
    "stats_permutations_vs_combinations": _stats_permutations_vs_combinations,
}
