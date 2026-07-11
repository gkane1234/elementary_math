"""Settings fields for graph and number-line metadata."""

from __future__ import annotations

from ...core.models import SettingField


def graphing_metadata_settings() -> list[SettingField]:
    return [
        SettingField(
            "include_graph_metadata",
            "Include graph / number-line metadata",
            "bool",
            False,
            group="graphing",
        ),
        SettingField(
            "show_grid",
            "Show grid lines",
            "bool",
            True,
            group="graphing",
        ),
        SettingField(
            "show_points",
            "Show plotted points",
            "bool",
            True,
            group="graphing",
        ),
    ]


def graph_dimension_settings() -> list[SettingField]:
    return [
        SettingField(
            "graph_dimension",
            "Graph dimension",
            "select",
            "coordinate",
            options=["coordinate", "number_line"],
            group="graphing",
        ),
    ]


def number_line_range_settings(
    *,
    min_default: int = -12,
    max_default: int = 12,
    show_zero_default: bool = True,
) -> list[SettingField]:
    return [
        SettingField(
            "number_line_min",
            "Number line min",
            "int",
            min_default,
            min=-50,
            max=0,
            group="graphing",
        ),
        SettingField(
            "number_line_max",
            "Number line max",
            "int",
            max_default,
            min=0,
            max=50,
            group="graphing",
        ),
        SettingField(
            "number_line_show_zero",
            "Show 0 on number line",
            "bool",
            show_zero_default,
            group="graphing",
        ),
        SettingField(
            "number_line_tick_interval",
            "Number line tick interval",
            "int",
            1,
            min=1,
            max=10,
            group="graphing",
        ),
    ]
