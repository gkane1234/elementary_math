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


def quadratic_square_root_form_settings() -> list[SettingField]:
    """Selectable templates for solve-by-square-roots equations.

    At least one form should stay enabled; generation falls back to isolated
    ``x^2 = k`` if none are selected.
    """
    return [
        SettingField(
            "allow_isolated",
            "Allow isolated squares (x² = k, ax² = k)",
            "bool",
            True,
            group="square_root_forms",
        ),
        SettingField(
            "allow_vertex",
            "Allow vertex form a(x − h)² = m",
            "bool",
            True,
            group="square_root_forms",
        ),
        SettingField(
            "allow_complete_square",
            "Allow standard form (complete the square first)",
            "bool",
            False,
            group="square_root_forms",
        ),
    ]


def absolute_value_equation_form_settings() -> list[SettingField]:
    """Selectable templates for absolute-value equation prompts.

    At least one form should stay enabled; generation falls back to basic
    ``|ax + b| = c`` if none are selected.
    """
    return [
        SettingField(
            "allow_basic",
            "Allow |ax + b| = c",
            "bool",
            True,
            group="abs_forms",
        ),
        SettingField(
            "allow_isolated_right",
            "Allow c = |ax + b|",
            "bool",
            True,
            group="abs_forms",
        ),
        SettingField(
            "allow_simple",
            "Allow |x| = c",
            "bool",
            True,
            group="abs_forms",
        ),
        SettingField(
            "allow_abs_plus_constant",
            "Allow |ax + b| ± c = d",
            "bool",
            True,
            group="abs_forms",
        ),
        SettingField(
            "allow_factored_inside",
            "Allow |a(x + b)| = c",
            "bool",
            True,
            group="abs_forms",
        ),
        SettingField(
            "allow_coeff_outside",
            "Allow a|x + b| = c",
            "bool",
            False,
            group="abs_forms",
        ),
        SettingField(
            "allow_abs_equals_abs",
            "Allow |ax + b| = |cx + d|",
            "bool",
            False,
            group="abs_forms",
        ),
        SettingField(
            "allow_abs_equals_linear",
            "Allow |ax + b| = cx + d",
            "bool",
            False,
            group="abs_forms",
        ),
    ]


def absolute_value_inequality_form_settings() -> list[SettingField]:
    """Selectable templates for absolute-value inequality prompts.

    At least one form should stay enabled; generation falls back to
    ``|x| < c`` if none are selected.
    """
    return [
        SettingField(
            "allow_simple",
            "Allow |x| ⋈ c",
            "bool",
            True,
            group="abs_forms",
        ),
        SettingField(
            "allow_shifted",
            "Allow |x ± a| ⋈ c",
            "bool",
            True,
            group="abs_forms",
        ),
        SettingField(
            "allow_linear",
            "Allow |ax + b| ⋈ c",
            "bool",
            True,
            group="abs_forms",
        ),
        SettingField(
            "allow_abs_plus_constant",
            "Allow |ax + b| ± k ⋈ c",
            "bool",
            False,
            group="abs_forms",
        ),
        SettingField(
            "allow_abs_vs_linear",
            "Allow |ax + b| ⋈ cx + d",
            "bool",
            False,
            group="abs_forms",
        ),
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
