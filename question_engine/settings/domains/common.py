"""Cross-cutting setting field builders shared across generator families."""

from __future__ import annotations

from ...core.models import SettingField


def difficulty_settings(
    *,
    default: str = "medium",
) -> list[SettingField]:
    return [
        SettingField(
            "difficulty_tier",
            "Difficulty tier",
            "select",
            default,
            options=["easy", "medium", "hard"],
            group="difficulty",
        ),
    ]


def answer_format_settings(
    *,
    answer_format_default: str = "auto",
    round_whole_default: bool = False,
) -> list[SettingField]:
    return [
        SettingField(
            "answer_format",
            "Answer format",
            "select",
            answer_format_default,
            options=["auto", "integer", "fraction", "decimal", "multiple_choice"],
            group="answer",
        ),
        SettingField(
            "round_answers_to_whole",
            "Round answers to whole numbers",
            "bool",
            round_whole_default,
            group="answer",
        ),
    ]


def sign_restrictions(
    *,
    positive_only_default: bool = False,
    exclude_zero_solutions_default: bool = False,
) -> list[SettingField]:
    return [
        SettingField(
            "coefficients_positive_only",
            "Positive coefficients only",
            "bool",
            positive_only_default,
            group="signs",
        ),
        SettingField(
            "exclude_zero_solutions",
            "Exclude zero solutions",
            "bool",
            exclude_zero_solutions_default,
            group="signs",
        ),
        SettingField(
            "exclude_zero_coefficients",
            "Exclude zero coefficients",
            "bool",
            True,
            group="signs",
        ),
    ]


def term_count_settings(
    *,
    min_default: int = 2,
    max_default: int = 4,
    min_bound: int = 2,
    max_bound: int = 8,
) -> list[SettingField]:
    return [
        SettingField(
            "min_terms",
            "Minimum terms",
            "int",
            min_default,
            min=min_bound,
            max=max_bound,
            group="terms",
        ),
        SettingField(
            "max_terms",
            "Maximum terms",
            "int",
            max_default,
            min=min_bound,
            max=max_bound,
            group="terms",
        ),
    ]


def multiple_choice_settings(
    *,
    ratio_default: int = 0,
    show_work_default: int = 0,
    multiple_choice_default: bool = False,
) -> list[SettingField]:
    return [
        SettingField(
            "multiple_choice",
            "Multiple choice",
            "bool",
            multiple_choice_default,
            group="presentation",
        ),
        SettingField(
            "multiple_choice_ratio",
            "Multiple choice ratio",
            "range",
            ratio_default,
            min=0,
            max=100,
            group="presentation",
        ),
        SettingField(
            "show_work_lines",
            "Show work lines",
            "int",
            show_work_default,
            min=0,
            max=8,
            group="presentation",
        ),
    ]
