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
