"""Settings fields for word-problem template types."""

from __future__ import annotations

from ...core.models import SettingField


def word_problem_settings() -> list[SettingField]:
    return [
        SettingField(
            "difficulty",
            "Difficulty",
            "select",
            "medium",
            options=["easy", "medium", "hard"],
            group="word_problem",
        ),
        SettingField(
            "integer_only_answers",
            "Integer answers only",
            "bool",
            True,
            group="word_problem",
        ),
        SettingField(
            "name_style",
            "Name placeholders",
            "select",
            "names",
            options=["names", "letters", "person_a_b"],
            group="word_problem",
        ),
        SettingField(
            "show_unit_labels",
            "Show unit labels in prompts",
            "bool",
            True,
            group="word_problem",
        ),
        SettingField(
            "answer_units",
            "Answer units",
            "select",
            "",
            options=["", "ft", "m", "cm", "mi", "km", "hr", "min", "dollars", "years", "coins"],
            group="word_problem",
        ),
        SettingField(
            "max_steps",
            "Max equation steps",
            "int",
            2,
            min=1,
            max=4,
            group="word_problem",
        ),
    ]


def distance_rate_time_settings() -> list[SettingField]:
    """Structure and unit toggles for distance-rate-time word problems."""
    return [
        SettingField(
            "allow_drt_find_missing",
            "Allow single-traveler find d/r/t",
            "bool",
            True,
            group="drt_structure",
        ),
        SettingField(
            "allow_drt_round_trip",
            "Allow round-trip problems",
            "bool",
            False,
            group="drt_structure",
        ),
        SettingField(
            "allow_drt_two_segments",
            "Allow two-segment trips",
            "bool",
            False,
            group="drt_structure",
        ),
        SettingField(
            "allow_drt_opposite",
            "Allow opposite-direction (two travelers)",
            "bool",
            False,
            group="drt_structure",
        ),
        SettingField(
            "allow_drt_same_direction",
            "Allow same-direction / catch-up",
            "bool",
            False,
            group="drt_structure",
        ),
        SettingField(
            "allow_distance_mi",
            "Allow miles",
            "bool",
            True,
            group="drt_units",
        ),
        SettingField(
            "allow_distance_km",
            "Allow kilometers",
            "bool",
            True,
            group="drt_units",
        ),
        SettingField(
            "allow_distance_m",
            "Allow meters (with m/s)",
            "bool",
            True,
            group="drt_units",
        ),
        SettingField(
            "allow_distance_ft",
            "Allow feet (with ft/s)",
            "bool",
            True,
            group="drt_units",
        ),
        SettingField(
            "allow_time_hr",
            "Allow hours (mi/hr, km/hr)",
            "bool",
            True,
            group="drt_units",
        ),
        SettingField(
            "allow_time_min",
            "Allow minutes (mi/min, km/min)",
            "bool",
            True,
            group="drt_units",
        ),
    ]


def work_problem_settings() -> list[SettingField]:
    """Structure and time-unit toggles for work word problems."""
    return [
        SettingField(
            "allow_work_together",
            "Allow two workers, find combined time",
            "bool",
            True,
            group="work_structure",
        ),
        SettingField(
            "allow_work_find_one_rate",
            "Allow find one worker's time given combined",
            "bool",
            True,
            group="work_structure",
        ),
        SettingField(
            "allow_work_three",
            "Allow three workers together",
            "bool",
            False,
            group="work_structure",
        ),
        SettingField(
            "allow_work_find_one_time",
            "Allow find one person's solo time (given two others)",
            "bool",
            False,
            group="work_structure",
        ),
        SettingField(
            "allow_work_starts_later",
            "Allow one worker starts later",
            "bool",
            False,
            group="work_structure",
        ),
        SettingField(
            "allow_work_pipes",
            "Allow pipes / fill-and-drain style",
            "bool",
            False,
            group="work_structure",
        ),
        SettingField(
            "allow_work_time_hr",
            "Allow hours",
            "bool",
            True,
            group="work_units",
        ),
        SettingField(
            "allow_work_time_min",
            "Allow minutes",
            "bool",
            True,
            group="work_units",
        ),
    ]


def consecutive_integers_settings() -> list[SettingField]:
    """Count, parity, and goal toggles for consecutive-integer word problems."""
    return [
        SettingField(
            "min_consecutive_count",
            "Min consecutive integers",
            "int",
            2,
            min=2,
            max=5,
            group="consecutive",
        ),
        SettingField(
            "max_consecutive_count",
            "Max consecutive integers",
            "int",
            4,
            min=2,
            max=5,
            group="consecutive",
        ),
        SettingField(
            "allow_consecutive_integers",
            "Allow consecutive integers",
            "bool",
            True,
            group="consecutive",
        ),
        SettingField(
            "allow_consecutive_even",
            "Allow consecutive even integers",
            "bool",
            True,
            group="consecutive",
        ),
        SettingField(
            "allow_consecutive_odd",
            "Allow consecutive odd integers",
            "bool",
            True,
            group="consecutive",
        ),
        SettingField(
            "allow_sum_goal",
            "Allow sum of all",
            "bool",
            True,
            group="consecutive",
        ),
        SettingField(
            "allow_sum_first_last_goal",
            "Allow sum of first and last",
            "bool",
            False,
            group="consecutive",
        ),
        SettingField(
            "allow_product_goal",
            "Allow product of first and last",
            "bool",
            False,
            group="consecutive",
        ),
    ]
