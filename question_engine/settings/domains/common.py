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


def continuous_difficulty_settings(
    *,
    default_d: int = 6,
) -> list[SettingField]:
    """Numeric difficulty slider (EMH tier is hidden in UI when this is present)."""
    return [
        SettingField(
            "difficulty",
            "Difficulty",
            "int",
            default_d,
            min=0,
            group="difficulty",
        ),
    ]


def primitive_layered_settings(
    *,
    primitive_ids: list[str],
    d_max: int = 24,
    default_d: int = 6,
    include_number_profile: bool = True,
    include_number_constraints: bool | None = None,
) -> list[SettingField]:
    """Continuous difficulty + optional per-prereq max caps + Layer 0 constraints.

    Topic difficulty has no hard upper bound (type any non-negative number).
    ``d_max`` is retained for call-site compatibility; soft slider max (typically 24)
    lives in the UI / difficulty knobs, not as a hard SettingField.max.

    Prerequisite caps default to **no cap** (empty string). An explicit non-negative
    number limits that primitive; omit / leave empty so the budget is not limited
    by a hidden 24-style ceiling.

    Number lane is selected from topic difficulty + constraints (not a parallel
    difficulty knob). Optional ``number_profile`` remains as an advanced override.

    Used by generators on the experiment/difficulty-slider branch.
    """
    from question_engine.frameworks.primitives.numbers import NUMBER_PROFILES, PROFILE_CATALOG

    if include_number_constraints is None:
        include_number_constraints = include_number_profile

    fields: list[SettingField] = [
        SettingField(
            "difficulty",
            "Difficulty",
            "int",
            default_d,
            min=0,
            group="difficulty",
        ),
    ]
    labels = {
        "numbers": "Max difficulty: numbers",
        "variable": "Max difficulty: variable",
        "ooo": "Max difficulty: order of operations",
        "distributive": "Max difficulty: distributive",
        "evaluate": "Max difficulty: evaluate linear",
        "like_terms": "Max difficulty: like terms",
        "expand_simplify": "Max difficulty: expand then simplify",
        "equations": "Max difficulty: equations",
        "inequalities": "Max difficulty: inequalities",
        "factor_gcf": "Max difficulty: factor GCF",
    }
    for pid in primitive_ids:
        fields.append(
            SettingField(
                f"prereq_cap_{pid}",
                labels.get(pid, f"Max difficulty: {pid}"),
                "int",
                "",  # empty = no cap (unlimited)
                min=0,
                group="prereq_caps",
            )
        )
    if include_number_constraints and "numbers" in primitive_ids:
        fields.extend(
            [
                SettingField(
                    "integers_only",
                    "Integers only",
                    "bool",
                    False,
                    group="layer0",
                ),
                SettingField(
                    "allow_negatives",
                    "Allow negatives",
                    "bool",
                    True,
                    group="layer0",
                ),
                SettingField(
                    "allow_fractions",
                    "Allow fractions",
                    "bool",
                    True,
                    group="layer0",
                ),
                SettingField(
                    "allow_decimals",
                    "Allow decimals",
                    "bool",
                    True,
                    group="layer0",
                ),
                SettingField(
                    "exclude_zero",
                    "Exclude zero",
                    "bool",
                    False,
                    group="layer0",
                ),
                # Advanced override — not the primary control; auto selects from D + constraints.
                SettingField(
                    "number_profile",
                    "Force number lane (optional)",
                    "select",
                    "auto",
                    options=["auto", *NUMBER_PROFILES],
                    group="layer0_advanced",
                ),
            ]
        )
    if "variable" in primitive_ids:
        from question_engine.frameworks.primitives.variables import (
            LANE_CATALOG,
            VARIABLE_LANES,
        )

        fields.extend(
            [
                SettingField(
                    "only_x",
                    "Only x",
                    "bool",
                    False,
                    group="layer0",
                ),
                SettingField(
                    "allow_greek",
                    "Allow Greek letters",
                    "bool",
                    True,
                    group="layer0",
                ),
                SettingField(
                    "max_variable_lane",
                    "Max variable pool",
                    "select",
                    "auto",
                    options=["auto", *VARIABLE_LANES],
                    group="layer0",
                ),
                SettingField(
                    "lock_variable",
                    "Lock variable",
                    "select",
                    "none",
                    options=["none", "x", "y", "z", "n", "t", "a", "b"],
                    group="layer0",
                ),
                SettingField(
                    "variable_lane",
                    "Force variable lane (optional)",
                    "select",
                    "auto",
                    options=["auto", *VARIABLE_LANES],
                    group="layer0_advanced",
                ),
            ]
        )
        _ = LANE_CATALOG
    # Keep PROFILE_CATALOG referenced for future API exposure / audit.
    _ = PROFILE_CATALOG
    return fields


def answer_format_settings(
    *,
    answer_format_default: str = "auto",
    round_whole_default: bool = False,
) -> list[SettingField]:
    # Multiple choice is a separate presentation toggle, not an answer-format option.
    if answer_format_default == "multiple_choice":
        answer_format_default = "auto"
    return [
        SettingField(
            "answer_format",
            "Answer format",
            "select",
            answer_format_default,
            options=["auto", "integer", "fraction", "decimal"],
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
    """MC is a simple toggle; ratio is a deeper option shown only when MC is on."""
    return [
        SettingField(
            "multiple_choice",
            "Use multiple choice instead of free response",
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
