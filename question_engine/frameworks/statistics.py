"""Statistics framework — data sets, chart metadata, and probability prompts."""

from __future__ import annotations

import random
from collections import Counter
from dataclasses import dataclass, field
from fractions import Fraction
from statistics import median as stats_median
from typing import Any, Literal

from .base import QuestionFramework
from ..core.metadata import question_metadata
from ..generators.utils import frac_latex, random_int_range

ChartType = Literal["dot_plot", "histogram", "box_plot", "bar_chart", "line_plot"]
MeasureType = Literal["mean", "median", "mode", "range"]
ProbabilityFormat = Literal["fraction", "decimal", "percent"]

_MEASURE_LABELS: dict[MeasureType, str] = {
    "mean": "mean",
    "median": "median",
    "mode": "mode",
    "range": "range",
}


@dataclass
class DataSetSpec:
    """Synthetic or sampled data for statistics items."""

    values: list[float] = field(default_factory=list)
    labels: list[str] = field(default_factory=list)
    unit: str = ""
    frequencies: dict[str, int] = field(default_factory=dict)


@dataclass
class ChartSpec:
    """Chart rendering hints stored in question metadata."""

    chart_type: ChartType
    title: str = ""
    x_label: str = ""
    y_label: str = ""
    bin_width: float | None = None
    bins: list[tuple[float, float]] = field(default_factory=list)
    five_number_summary: dict[str, float] = field(default_factory=dict)


@dataclass(frozen=True)
class StatisticsParams:
    size_min: int
    size_max: int
    value_min: int
    value_max: int
    integer_data_only: bool
    measure_type: str
    probability_format: ProbabilityFormat


def _bounded_int(settings: dict, key: str, default: int) -> int:
    return int(settings.get(key, default))


def _int_range(
    settings: dict,
    min_key: str,
    max_key: str,
    *,
    lo_default: int,
    hi_default: int,
) -> tuple[int, int]:
    lo = _bounded_int(settings, min_key, lo_default)
    hi = _bounded_int(settings, max_key, hi_default)
    return min(lo, hi), max(lo, hi)


def statistics_params_from_settings(settings: dict) -> StatisticsParams:
    size_min, size_max = _int_range(
        settings, "data_set_size_min", "data_set_size_max", lo_default=5, hi_default=10
    )
    value_min, value_max = _int_range(
        settings, "value_min", "value_max", lo_default=1, hi_default=20
    )
    probability_format = str(settings.get("probability_format", "fraction"))
    if probability_format not in ("fraction", "decimal", "percent"):
        probability_format = "fraction"
    return StatisticsParams(
        size_min=size_min,
        size_max=size_max,
        value_min=value_min,
        value_max=value_max,
        integer_data_only=bool(settings.get("integer_data_only", True)),
        measure_type=str(settings.get("measure_type", "random")),
        probability_format=probability_format,  # type: ignore[arg-type]
    )


def _generate_data_set(settings: dict, *, params: StatisticsParams | None = None) -> list[float]:
    params = params or statistics_params_from_settings(settings)
    count = random.randint(params.size_min, params.size_max)
    values: list[float] = []
    for _ in range(count):
        if params.integer_data_only:
            values.append(float(random_int_range(params.value_min, params.value_max)))
        else:
            whole = random_int_range(params.value_min, params.value_max)
            values.append(round(whole + random.random(), 1))
    return values


def _values_latex(values: list[float]) -> str:
    formatted = [str(int(v)) if v == int(v) else f"{v:.1f}" for v in values]
    return ",\\ ".join(formatted)


def _compute_mean(values: list[float]) -> float:
    return sum(values) / len(values)


def _compute_median(values: list[float]) -> float:
    return float(stats_median(values))


def _compute_mode(values: list[float]) -> float:
    counts = Counter(values)
    max_count = max(counts.values())
    modes = sorted(value for value, count in counts.items() if count == max_count)
    return modes[0]


def _compute_range(values: list[float]) -> float:
    return max(values) - min(values)


def _resolve_measure(settings: dict, explicit: MeasureType | None = None) -> MeasureType:
    if explicit is not None:
        return explicit
    measure = str(settings.get("measure_type", "random"))
    if measure in _MEASURE_LABELS:
        return measure  # type: ignore[return-value]
    return random.choice(["mean", "median", "mode", "range"])


def _compute_measure(values: list[float], measure: MeasureType) -> float:
    if measure == "mean":
        return _compute_mean(values)
    if measure == "median":
        return _compute_median(values)
    if measure == "mode":
        return _compute_mode(values)
    return _compute_range(values)


def _format_numeric_answer(value: float, *, integer_only: bool) -> str:
    if value == int(value):
        return str(int(round(value)))
    return f"{value:.2f}".rstrip("0").rstrip(".")


def _format_probability(probability: Fraction, settings: dict) -> str:
    params = statistics_params_from_settings(settings)
    if params.probability_format == "decimal":
        return f"{float(probability):.2f}".rstrip("0").rstrip(".")
    if params.probability_format == "percent":
        pct = float(probability) * 100
        if pct == int(pct):
            return f"{int(pct)}\\%"
        return f"{pct:.1f}\\%"
    return frac_latex(probability)


def _frequency_table(values: list[float]) -> dict[str, int]:
    counts = Counter(values)
    return {str(int(v) if v == int(v) else v): count for v, count in sorted(counts.items())}


def _data_metadata(
    values: list[float],
    chart: ChartSpec | None = None,
) -> dict[str, Any]:
    from ..diagrams.charts import box_plot_svg, dot_plot_svg, histogram_svg

    data = DataSetSpec(
        values=values,
        frequencies=_frequency_table(values),
    )
    meta: dict[str, Any] = {
        "data_set": {
            "values": data.values,
            "labels": data.labels,
            "unit": data.unit,
            "frequencies": data.frequencies,
        },
    }
    if chart is not None:
        meta["chart_spec"] = {
            "chart_type": chart.chart_type,
            "title": chart.title,
            "x_label": chart.x_label,
            "y_label": chart.y_label,
            "bin_width": chart.bin_width,
            "bins": [{"low": low, "high": high} for low, high in chart.bins],
            "five_number_summary": chart.five_number_summary,
        }
        if chart.chart_type == "dot_plot":
            meta["diagram_svg"] = dot_plot_svg(values, title=chart.title or "Dot plot")
        elif chart.chart_type == "histogram":
            bins = chart.bins or _histogram_bins(values, int(chart.bin_width or 2))
            meta["diagram_svg"] = histogram_svg(
                values, bins, title=chart.title or "Histogram"
            )
        elif chart.chart_type == "box_plot":
            summary = chart.five_number_summary or _five_number_summary(values)
            meta["diagram_svg"] = box_plot_svg(
                summary, title=chart.title or "Box plot"
            )
    return question_metadata(**meta)



def _histogram_bins(values: list[float], bin_width: int) -> list[tuple[float, float]]:
    minimum = int(min(values))
    maximum = int(max(values))
    start = (minimum // bin_width) * bin_width
    bins: list[tuple[float, float]] = []
    edge = start
    while edge <= maximum:
        bins.append((float(edge), float(edge + bin_width)))
        edge += bin_width
    if not bins:
        bins.append((float(minimum), float(minimum + bin_width)))
    return bins


def _count_in_bin(values: list[float], low: float, high: float) -> int:
    return sum(1 for value in values if low <= value < high or (value == high and high == max(values)))


def _five_number_summary(values: list[float]) -> dict[str, float]:
    ordered = sorted(values)
    n = len(ordered)
    midpoint = n // 2
    lower_half = ordered[:midpoint]
    upper_half = ordered[midpoint + (n % 2) :]
    return {
        "min": ordered[0],
        "q1": _compute_median(lower_half),
        "median": _compute_median(ordered),
        "q3": _compute_median(upper_half),
        "max": ordered[-1],
    }


class StatisticsFramework(QuestionFramework):
    """Shared batch generation for statistics and data-display types."""

    chart_type: ChartType = "dot_plot"

    def __init__(self, chart_type: ChartType = "dot_plot"):
        self.chart_type = chart_type

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        values = _generate_data_set(settings)
        chart = ChartSpec(chart_type=self.chart_type)
        return _data_metadata(values, chart)

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        raise NotImplementedError(
            "StatisticsFramework.build_prompt is abstract; use a concrete subclass."
        )

    def build_question_metadata(
        self,
        settings: dict,
        *,
        prompt_latex: str,
        prompt_text: str,
        answer: str | None,
    ) -> dict[str, Any]:
        return {}


class CenterSpreadFramework(StatisticsFramework):
    """Find mean, median, mode, or range from a listed data set."""

    def __init__(self, measure: MeasureType | None = None):
        super().__init__(chart_type="dot_plot")
        self.measure = measure
        self._last_values: list[float] = []
        self._last_chart: ChartSpec | None = None

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        params = statistics_params_from_settings(settings)
        values = _generate_data_set(settings, params=params)
        measure = _resolve_measure(settings, self.measure)
        if measure == "mode":
            # A strict majority guarantees that the requested mode exists and is unique.
            mode_value = values[0]
            values[: len(values) // 2 + 1] = [mode_value] * (len(values) // 2 + 1)
        result = _compute_measure(values, measure)
        self._last_values = values
        self._last_chart = ChartSpec(chart_type="dot_plot", title="Data set")
        include_answer = bool(settings.get("include_answer_key", False))
        prompt = (
            f"\\text{{Find the {_MEASURE_LABELS[measure]} of the data set: }} "
            f"\\{{{_values_latex(values)}\\}}."
        )
        answer = _format_numeric_answer(result, integer_only=params.integer_data_only) if include_answer else None
        return prompt, f"{measure} of data set", answer

    def build_question_metadata(
        self,
        settings: dict,
        *,
        prompt_latex: str,
        prompt_text: str,
        answer: str | None,
    ) -> dict[str, Any]:
        if not self._last_values:
            return {}
        return _data_metadata(self._last_values, self._last_chart)


class MeanFramework(CenterSpreadFramework):
    def __init__(self) -> None:
        super().__init__(measure="mean")


class MedianFramework(CenterSpreadFramework):
    def __init__(self) -> None:
        super().__init__(measure="median")


class ModeFramework(CenterSpreadFramework):
    def __init__(self) -> None:
        super().__init__(measure="mode")


class RangeFramework(CenterSpreadFramework):
    def __init__(self) -> None:
        super().__init__(measure="range")


class StatisticalModelFramework(StatisticsFramework):
    """Predict from a small linear data table with a constant rate of change."""

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        include_answer = bool(settings.get("include_answer_key", False))
        context, x_label, y_label = random.choice(
            [
                ("A plant's height", "Weeks", "Height (cm)"),
                ("A taxi fare", "Miles traveled", "Cost (dollars)"),
                ("A savings account balance", "Weeks", "Balance (dollars)"),
            ]
        )
        slope = random.randint(2, 8)
        intercept = random.randint(4, 20)
        input_values = list(range(1, 5))
        output_values = [slope * x + intercept for x in input_values]
        target_input = 5
        rows = r" \\ ".join(
            f"{x} & {y}" for x, y in zip(input_values, output_values)
        )
        prompt = (
            f"\\text{{{context} follows a linear pattern.}}\\\\"
            f"\\begin{{array}}{{c|c}}{x_label} & {y_label}\\\\\\hline "
            f"{rows}\\end{{array}}\\\\"
            f"\\text{{Use the model to predict the {y_label.lower()} at "
            f"{x_label.lower()} = {target_input}.}}"
        )
        answer = str(slope * target_input + intercept) if include_answer else None
        return prompt, f"linear model prediction at {target_input}", answer


class DotPlotReadFramework(StatisticsFramework):
    """Read counts or measures from a dot plot."""

    def __init__(self) -> None:
        super().__init__(chart_type="dot_plot")
        self._last_values: list[float] = []
        self._last_chart: ChartSpec | None = None

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        params = statistics_params_from_settings(settings)
        values = _generate_data_set(settings, params=params)
        target = random.choice(sorted(set(values)))
        count = values.count(target)
        self._last_values = values
        self._last_chart = ChartSpec(
            chart_type="dot_plot", title="Dot plot", x_label="Value", y_label="Frequency"
        )
        include_answer = bool(settings.get("include_answer_key", False))
        target_text = str(int(target) if target == int(target) else target)
        prompt = (
            f"\\text{{The dot plot shows the data set below. How many dots are at }} {target_text}\\text{{?}}\\\\"
            f"\\text{{Data: }} \\{{{_values_latex(values)}\\}}"
        )
        answer = str(count) if include_answer else None
        return prompt, f"dot count at {target_text}", answer

    def build_question_metadata(
        self,
        settings: dict,
        *,
        prompt_latex: str,
        prompt_text: str,
        answer: str | None,
    ) -> dict[str, Any]:
        if not self._last_values:
            return {}
        return _data_metadata(self._last_values, self._last_chart)


class HistogramReadFramework(StatisticsFramework):
    """Read bin counts from a histogram."""

    def __init__(self) -> None:
        super().__init__(chart_type="histogram")
        self._last_values: list[float] = []
        self._last_chart: ChartSpec | None = None

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        params = statistics_params_from_settings(settings)
        values = _generate_data_set(settings, params=params)
        bin_width = max(2, (params.value_max - params.value_min) // 4)
        bins = _histogram_bins(values, bin_width)
        populated_bins = [
            bin_range
            for bin_range in bins
            if _count_in_bin(values, bin_range[0], bin_range[1]) > 0
        ]
        target = random.choice(populated_bins)
        count = _count_in_bin(values, target[0], target[1])
        self._last_values = values
        self._last_chart = ChartSpec(
            chart_type="histogram",
            title="Histogram",
            x_label="Value",
            y_label="Frequency",
            bin_width=float(bin_width),
            bins=bins,
        )
        include_answer = bool(settings.get("include_answer_key", False))
        low = int(target[0])
        high = int(target[1])
        prompt = (
            f"\\text{{How many values fall in the interval }} [{low},\\ {high})\\text{{?}}\\\\"
            f"\\text{{Data: }} \\{{{_values_latex(values)}\\}}"
        )
        answer = str(count) if include_answer else None
        return prompt, f"histogram bin [{low}, {high})", answer

    def build_question_metadata(
        self,
        settings: dict,
        *,
        prompt_latex: str,
        prompt_text: str,
        answer: str | None,
    ) -> dict[str, Any]:
        if not self._last_values:
            return {}
        return _data_metadata(self._last_values, self._last_chart)


class BoxPlotBasicsFramework(StatisticsFramework):
    """Find median, IQR, or range from a box plot summary."""

    def __init__(self) -> None:
        super().__init__(chart_type="box_plot")
        self._last_values: list[float] = []
        self._last_chart: ChartSpec | None = None

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        params = statistics_params_from_settings(settings)
        values = _generate_data_set(settings, params=params)
        summary = _five_number_summary(values)
        question = random.choice(["median", "iqr", "range"])
        self._last_values = values
        self._last_chart = ChartSpec(
            chart_type="box_plot",
            title="Box plot",
            x_label="Value",
            five_number_summary=summary,
        )
        include_answer = bool(settings.get("include_answer_key", False))
        if question == "median":
            result = summary["median"]
            label = "median"
        elif question == "iqr":
            result = summary["q3"] - summary["q1"]
            label = "interquartile range"
        else:
            result = summary["max"] - summary["min"]
            label = "range"
        prompt = f"\\text{{From the box plot, find the {label}.}}"
        answer = _format_numeric_answer(result, integer_only=params.integer_data_only) if include_answer else None
        return prompt, f"box plot {label}", answer

    def build_question_metadata(
        self,
        settings: dict,
        *,
        prompt_latex: str,
        prompt_text: str,
        answer: str | None,
    ) -> dict[str, Any]:
        if not self._last_values:
            return {}
        return _data_metadata(self._last_values, self._last_chart)


class SingleEventProbabilityFramework(StatisticsFramework):
    """Probability of a single event from a finite sample space."""

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        include_answer = bool(settings.get("include_answer_key", False))
        scenario = random.choice(["marbles", "spinner", "dice"])
        if scenario == "marbles":
            red = random.randint(2, 8)
            blue = random.randint(2, 8)
            total = red + blue
            color = random.choice(["red", "blue"])
            favorable = red if color == "red" else blue
            prompt = (
                f"\\text{{A bag has {red} red marbles and {blue} blue marbles. "
                f"What is the probability of drawing a {color} marble?}}"
            )
            text = f"P({color} marble)"
        elif scenario == "spinner":
            sections = random.randint(4, 8)
            target = random.randint(1, sections)
            prompt = (
                f"\\text{{A spinner has {sections} equal sections numbered 1 through {sections}. "
                f"What is the probability of landing on {target}?}}"
            )
            favorable = 1
            total = sections
            text = f"P({target})"
        else:
            total = 6
            target = random.randint(1, 6)
            prompt = (
                f"\\text{{A fair die is rolled. What is the probability of rolling a {target}?}}"
            )
            favorable = 1
            text = f"P({target})"
        probability = Fraction(favorable, total)
        answer = _format_probability(probability, settings) if include_answer else None
        return prompt, text, answer


class CompoundIndependentProbabilityFramework(StatisticsFramework):
    """Probability of two independent events both occurring."""

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        include_answer = bool(settings.get("include_answer_key", False))
        coin = random.choice([True, False])
        if coin:
            prompt = (
                "\\text{{A fair coin is flipped and a fair die is rolled. "
                "What is the probability of getting heads and rolling an even number?}}"
            )
            probability = Fraction(1, 2) * Fraction(1, 2)
            text = "P(heads and even)"
        else:
            red = random.randint(2, 5)
            blue = random.randint(2, 5)
            green = random.randint(2, 5)
            total = red + blue + green
            prompt = (
                f"\\text{{A bag has {red} red, {blue} blue, and {green} green marbles. "
                f"You draw one marble, replace it, then draw again. "
                f"What is the probability of drawing red both times?}}"
            )
            probability = Fraction(red, total) ** 2
            text = "P(red and red)"
        answer = _format_probability(probability, settings) if include_answer else None
        return prompt, text, answer


class CountingPrincipleFramework(StatisticsFramework):
    """Basic counting principle: multiply numbers of choices."""

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        include_answer = bool(settings.get("include_answer_key", False))
        if random.choice([True, False]):
            entrees = random.randint(3, 6)
            desserts = random.randint(2, 5)
            prompt = (
                f"\\text{{A restaurant offers {entrees} entrees and {desserts} desserts. "
                f"How many entree-dessert combinations are possible?}}"
            )
            result = entrees * desserts
            text = f"{entrees} x {desserts} outcomes"
        else:
            shirts = random.randint(3, 7)
            pants = random.randint(2, 5)
            shoes = random.randint(2, 4)
            prompt = (
                f"\\text{{A store sells {shirts} shirts, {pants} pants, and {shoes} pairs of shoes. "
                f"How many shirt-pants-shoes outfits are possible?}}"
            )
            result = shirts * pants * shoes
            text = f"{shirts} x {pants} x {shoes} outcomes"
        answer = str(result) if include_answer else None
        return prompt, text, answer


class MutuallyExclusiveProbabilityFramework(StatisticsFramework):
    """Probability of one of two mutually exclusive events."""

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        include_answer = bool(settings.get("include_answer_key", False))
        red = random.randint(2, 6)
        blue = random.randint(2, 6)
        green = random.randint(2, 6)
        total = red + blue + green
        color_a, color_b = random.sample(["red", "blue", "green"], 2)
        counts = {"red": red, "blue": blue, "green": green}
        favorable = counts[color_a] + counts[color_b]
        prompt = (
            f"\\text{{A bag has {red} red, {blue} blue, and {green} green marbles. "
            f"What is the probability of drawing a {color_a} or {color_b} marble?}}"
        )
        probability = Fraction(favorable, total)
        answer = _format_probability(probability, settings) if include_answer else None
        return prompt, f"P({color_a} or {color_b})", answer
