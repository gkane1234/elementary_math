"""Settings fields for statistics and probability question types."""

from __future__ import annotations

from ...core.models import SettingField


def statistics_data_settings(
    *,
    size_min_default: int = 5,
    size_max_default: int = 10,
    value_min_default: int = 1,
    value_max_default: int = 20,
) -> list[SettingField]:
    return [
        SettingField(
            "data_set_size_min",
            "Data set size min",
            "int",
            size_min_default,
            min=3,
            max=30,
            group="statistics",
        ),
        SettingField(
            "data_set_size_max",
            "Data set size max",
            "int",
            size_max_default,
            min=3,
            max=30,
            group="statistics",
        ),
        SettingField(
            "value_min",
            "Data value min",
            "int",
            value_min_default,
            min=-100,
            max=100,
            group="statistics",
        ),
        SettingField(
            "value_max",
            "Data value max",
            "int",
            value_max_default,
            min=-100,
            max=100,
            group="statistics",
        ),
        SettingField(
            "integer_data_only",
            "Integer data only",
            "bool",
            True,
            group="statistics",
        ),
    ]


def statistics_measure_settings() -> list[SettingField]:
    return [
        SettingField(
            "measure_type",
            "Measure to find",
            "select",
            "random",
            options=["random", "mean", "median", "mode", "range"],
            group="statistics",
        ),
    ]


def probability_format_settings() -> list[SettingField]:
    return [
        SettingField(
            "probability_format",
            "Probability answer format",
            "select",
            "fraction",
            options=["fraction", "decimal", "percent"],
            group="statistics",
        ),
    ]


def chart_drawing_settings() -> list[SettingField]:
    return [
        SettingField(
            "include_axis",
            "Include blank axis",
            "bool",
            True,
            group="statistics",
        ),
    ]


def statistics_settings() -> list[SettingField]:
    return [
        *statistics_data_settings(),
        *statistics_measure_settings(),
        *probability_format_settings(),
    ]
