"""Settings fields for equation-solving question types."""

from __future__ import annotations

from ...core.models import SettingField


def equation_variable_settings() -> list[SettingField]:
    return [
        SettingField(
            "variable",
            "Variable",
            "select",
            "x",
            options=["x", "y", "t", "n"],
            group="equation",
        ),
    ]


def equation_solution_settings() -> list[SettingField]:
    return [
        SettingField(
            "integer_only",
            "Integer solutions only",
            "bool",
            True,
            group="equation",
        ),
    ]


def equation_operation_settings() -> list[SettingField]:
    return [
        SettingField("allow_add", "Allow addition", "bool", True, group="equation"),
        SettingField("allow_subtract", "Allow subtraction", "bool", True, group="equation"),
        SettingField("allow_multiply", "Allow multiplication", "bool", True, group="equation"),
        SettingField("allow_divide", "Allow division", "bool", True, group="equation"),
    ]


def equation_coef_settings(
    *,
    coef_min_default: int = -12,
    coef_max_default: int = 12,
    coef_bound: int = 50,
    include_positive_leading: bool = False,
) -> list[SettingField]:
    fields = [
        SettingField(
            "coef_min",
            "Coefficient min",
            "int",
            coef_min_default,
            min=-coef_bound,
            max=coef_bound,
            group="equation",
        ),
        SettingField(
            "coef_max",
            "Coefficient max",
            "int",
            coef_max_default,
            min=-coef_bound,
            max=coef_bound,
            group="equation",
        ),
    ]
    if include_positive_leading:
        fields.append(
            SettingField(
                "positive_leading_coefficient",
                "Positive leading coefficient",
                "bool",
                True,
                group="equation",
            )
        )
    return fields


def inequality_coef_settings(
    *,
    coef_min_default: int = -12,
    coef_max_default: int = 12,
    coef_bound: int = 50,
) -> list[SettingField]:
    """Coefficient bounds for inequality-solving types (same knobs as equations)."""
    return equation_coef_settings(
        coef_min_default=coef_min_default,
        coef_max_default=coef_max_default,
        coef_bound=coef_bound,
    )
