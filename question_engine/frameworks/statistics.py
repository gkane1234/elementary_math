"""Statistics framework — data sets and chart metadata.

Unlocks the Statistics & data catalog family (16 types). Tier 2 generators
synthesize numeric data sets and attach chart specs for dot plots, histograms,
and box plots without rendering charts server-side.

Tier 2 plan
-----------
1. ``DataSetSpec`` — values, labels, optional frequency table
2. ``ChartSpec`` — chart type + bin width / scale hints for client renderers
3. Prompt asks for mean, median, IQR, or interpretation from the displayed chart
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

from .base import QuestionFramework
from ..core.metadata import question_metadata

ChartType = Literal["dot_plot", "histogram", "box_plot", "bar_chart", "line_plot"]


@dataclass
class DataSetSpec:
    """Synthetic or sampled data for statistics items."""

    values: list[float] = field(default_factory=list)
    labels: list[str] = field(default_factory=list)
    unit: str = ""


@dataclass
class ChartSpec:
    """Chart rendering hints stored in question metadata."""

    chart_type: ChartType
    title: str = ""
    x_label: str = ""
    y_label: str = ""
    bin_width: float | None = None


class StatisticsFramework(QuestionFramework):
    """Shared batch generation for statistics and data-display types."""

    chart_type: ChartType = "dot_plot"

    def __init__(self, chart_type: ChartType = "dot_plot"):
        self.chart_type = chart_type

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        data = DataSetSpec(values=[], labels=[])
        chart = ChartSpec(chart_type=self.chart_type)
        return question_metadata(
            data_set={
                "values": data.values,
                "labels": data.labels,
                "unit": data.unit,
            },
            chart_spec={
                "chart_type": chart.chart_type,
                "title": chart.title,
                "bin_width": chart.bin_width,
            },
        )

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        raise NotImplementedError(
            "StatisticsFramework.build_prompt is a Tier 2 skeleton. "
            f"Implement data sampling for {self.chart_type}."
        )
