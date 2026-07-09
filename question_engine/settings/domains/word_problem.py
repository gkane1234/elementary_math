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
            "units",
            "Answer units",
            "select",
            "",
            options=["", "ft", "m", "cm", "mi", "km", "hr", "min", "dollars"],
            group="word_problem",
        ),
    ]
