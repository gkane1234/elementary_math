"""Settings fields for rational-expression question types."""

from __future__ import annotations

from ...core.models import SettingField


def rational_operation_settings() -> list[SettingField]:
    return [
        SettingField("allow_add", "Allow addition", "bool", True, group="rational"),
        SettingField("allow_subtract", "Allow subtraction", "bool", True, group="rational"),
        SettingField("allow_multiply", "Allow multiplication", "bool", True, group="rational"),
        SettingField("allow_divide", "Allow division", "bool", True, group="rational"),
    ]


def division_notation_settings() -> list[SettingField]:
    """Multi-select forms for fraction / rational division prompts.

    At least one must stay enabled; generation falls back to obelus (÷) if none are.
    """
    return [
        SettingField(
            "allow_obelus",
            "Allow ÷ symbol",
            "bool",
            True,
            group="division",
        ),
        SettingField(
            "allow_complex_fraction",
            "Allow complex fraction (stacked)",
            "bool",
            True,
            group="division",
        ),
        SettingField(
            "allow_slash",
            "Allow slash form (a/b) / (c/d)",
            "bool",
            True,
            group="division",
        ),
    ]


def rational_expression_extra_settings() -> list[SettingField]:
    """Type-specific controls for combining rational terms."""
    return [
        SettingField(
            "term_count",
            "Number of rational terms",
            "int",
            3,
            min=2,
            max=5,
            group="rational",
        ),
        SettingField(
            "use_random_partial_solution",
            "Use random partial-fraction numerators",
            "bool",
            True,
            group="rational",
        ),
        SettingField(
            "allow_polynomial_terms",
            "Allow terms with no denominator",
            "bool",
            True,
            group="rational",
        ),
        SettingField(
            "allow_full_lcd_terms",
            "Allow terms over the full LCD",
            "bool",
            True,
            group="rational",
        ),
        SettingField(
            "inflation_chance",
            "Degree inflation chance (%)",
            "range",
            15,
            min=0,
            max=100,
            group="rational",
        ),
        SettingField(
            "max_inflation_degree",
            "Max inflation factor degree",
            "int",
            2,
            min=1,
            max=4,
            group="rational",
        ),
        SettingField(
            "cancel_factor_count",
            "LCD factors to cancel in final answer",
            "select",
            "random",
            options=["random", "0", "1", "2", "3", "4"],
            group="rational",
        ),
        SettingField(
            "include_solution_details",
            "Include complete solution details in metadata",
            "bool",
            True,
            group="rational",
        ),
        SettingField(
            "force_lcd",
            "Force a full-LCD term in every problem",
            "bool",
            False,
            group="rational",
        ),
        SettingField(
            "allow_unlike_denominators",
            "Allow unlike denominators",
            "bool",
            True,
            group="rational",
        ),
        SettingField(
            "max_rational_terms",
            "Maximum rational terms",
            "int",
            5,
            min=2,
            max=5,
            group="rational",
        ),
    ]
