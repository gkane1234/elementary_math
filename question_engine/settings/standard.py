"""Standard question settings shared across all question types."""

from __future__ import annotations

from ..core.models import SettingField


def standard_question_settings(
    *,
    count_default: int = 10,
    count_max: int = 50,
) -> list[SettingField]:
    return [
        SettingField("count", "Number of questions", "int", count_default, min=1, max=count_max),
        SettingField(
            "max_columns",
            "Columns (auto-fit up to 3)",
            "select",
            "auto",
            options=["auto", "1", "2", "3"],
        ),
        SettingField("include_answer_key", "Include answer key", "bool", False),
    ]


def merge_settings(*schemas: list[SettingField]) -> list[SettingField]:
    """Combine setting schemas, keeping the first definition for duplicate keys."""
    seen: set[str] = set()
    merged: list[SettingField] = []
    for schema in schemas:
        for field in schema:
            if field.key in seen:
                continue
            seen.add(field.key)
            merged.append(field)
    return merged
