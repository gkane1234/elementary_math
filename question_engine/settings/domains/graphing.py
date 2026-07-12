"""Settings fields for graph and number-line metadata."""

from __future__ import annotations

from ...core.models import SettingField


def graphing_metadata_settings() -> list[SettingField]:
    return [
        SettingField(
            "include_graph_metadata",
            "Include graph / number-line metadata",
            "bool",
            False,
            group="graphing",
        ),
        SettingField(
            "show_grid",
            "Show grid lines",
            "bool",
            True,
            group="graphing",
        ),
        SettingField(
            "show_points",
            "Show plotted points",
            "bool",
            True,
            group="graphing",
        ),
    ]


def exponential_graph_settings(
    *,
    base_min_default: int = 2,
    base_max_default: int = 5,
) -> list[SettingField]:
    """Difficulty knobs for graphing y = a · b^(x−h) + k."""
    return [
        SettingField(
            "exp_base_min",
            "Base min (integer ≥ 2)",
            "int",
            base_min_default,
            min=2,
            max=10,
            group="exponential",
        ),
        SettingField(
            "exp_base_max",
            "Base max (integer ≥ 2)",
            "int",
            base_max_default,
            min=2,
            max=10,
            group="exponential",
        ),
        SettingField(
            "allow_decay",
            "Allow decay bases (0 < b < 1)",
            "bool",
            False,
            group="exponential",
        ),
        SettingField(
            "allow_stretch",
            "Allow vertical stretch (a ≠ ±1)",
            "bool",
            False,
            group="exponential",
        ),
        SettingField(
            "allow_vertical_shift",
            "Allow vertical shift (+k)",
            "bool",
            False,
            group="exponential",
        ),
        SettingField(
            "allow_horizontal_shift",
            "Allow horizontal shift (x − h)",
            "bool",
            False,
            group="exponential",
        ),
        SettingField(
            "allow_reflection",
            "Allow reflection over x-axis (a < 0)",
            "bool",
            False,
            group="exponential",
        ),
    ]


def absolute_value_graph_settings(
    *,
    coef_min_default: int = 1,
    coef_max_default: int = 1,
) -> list[SettingField]:
    """Difficulty knobs for graphing y = a|x − h| + k."""
    return [
        SettingField(
            "allow_shift_h",
            "Allow horizontal shift (|x − h|)",
            "bool",
            True,
            group="absolute_value_graph",
        ),
        SettingField(
            "allow_shift_k",
            "Allow vertical shift (+k)",
            "bool",
            False,
            group="absolute_value_graph",
        ),
        SettingField(
            "allow_stretch",
            "Allow vertical stretch (|a| ≠ 1)",
            "bool",
            False,
            group="absolute_value_graph",
        ),
        SettingField(
            "allow_reflection",
            "Allow reflection over x-axis (a < 0)",
            "bool",
            False,
            group="absolute_value_graph",
        ),
        SettingField(
            "coef_min",
            "Coefficient min (a)",
            "int",
            coef_min_default,
            min=-10,
            max=10,
            group="absolute_value_graph",
        ),
        SettingField(
            "coef_max",
            "Coefficient max (a)",
            "int",
            coef_max_default,
            min=-10,
            max=10,
            group="absolute_value_graph",
        ),
        SettingField(
            "integer_only",
            "Integer stretch coefficients only",
            "bool",
            True,
            group="absolute_value_graph",
        ),
    ]


def quadratic_graph_settings(
    *,
    coef_min_default: int = 1,
    coef_max_default: int = 1,
) -> list[SettingField]:
    """Difficulty knobs for graphing quadratics in several equation forms."""
    return [
        SettingField(
            "allow_vertex_form",
            "Allow vertex form a(x − h)² + k",
            "bool",
            True,
            group="quadratic_graph",
        ),
        SettingField(
            "allow_standard_form",
            "Allow standard form ax² + bx + c",
            "bool",
            False,
            group="quadratic_graph",
        ),
        SettingField(
            "allow_factored_form",
            "Allow factored / intercept form a(x − r)(x − s)",
            "bool",
            False,
            group="quadratic_graph",
        ),
        SettingField(
            "allow_messy_form",
            "Allow messy forms that need algebra first",
            "bool",
            False,
            group="quadratic_graph",
        ),
        SettingField(
            "allow_shift_h",
            "Allow horizontal shift (x − h)",
            "bool",
            True,
            group="quadratic_graph",
        ),
        SettingField(
            "allow_shift_k",
            "Allow vertical shift (+k)",
            "bool",
            True,
            group="quadratic_graph",
        ),
        SettingField(
            "allow_stretch",
            "Allow vertical stretch (|a| ≠ 1)",
            "bool",
            False,
            group="quadratic_graph",
        ),
        SettingField(
            "allow_reflection",
            "Allow reflection over x-axis (a < 0)",
            "bool",
            False,
            group="quadratic_graph",
        ),
        SettingField(
            "coef_min",
            "Coefficient min (a)",
            "int",
            coef_min_default,
            min=-10,
            max=10,
            group="quadratic_graph",
        ),
        SettingField(
            "coef_max",
            "Coefficient max (a)",
            "int",
            coef_max_default,
            min=-10,
            max=10,
            group="quadratic_graph",
        ),
        SettingField(
            "integer_only",
            "Integer stretch coefficients only",
            "bool",
            True,
            group="quadratic_graph",
        ),
    ]


def graph_dimension_settings() -> list[SettingField]:
    return [
        SettingField(
            "graph_dimension",
            "Graph dimension",
            "select",
            "coordinate",
            options=["coordinate", "number_line"],
            group="graphing",
        ),
    ]


def polynomial_solve_graph_settings() -> list[SettingField]:
    """Knobs for solving polynomial equations by graphing."""
    return [
        SettingField(
            "leading_coefficient_one",
            "Leading coefficient must be 1 (monic)",
            "bool",
            True,
            group="polynomial_solve_graph",
        ),
        SettingField(
            "monic_only",
            "Monic polynomials only",
            "bool",
            True,
            group="polynomial_solve_graph",
        ),
        SettingField(
            "allow_stretch",
            "Allow leading coefficient |a| ≠ 1",
            "bool",
            False,
            group="polynomial_solve_graph",
        ),
        SettingField(
            "allow_reflection",
            "Allow negative leading coefficient",
            "bool",
            False,
            group="polynomial_solve_graph",
        ),
        SettingField(
            "allow_factored_form",
            "Allow factored form prompts",
            "bool",
            False,
            group="polynomial_solve_graph",
        ),
        SettingField(
            "coef_min",
            "Leading coefficient min",
            "int",
            1,
            min=-10,
            max=10,
            group="polynomial_solve_graph",
        ),
        SettingField(
            "coef_max",
            "Leading coefficient max",
            "int",
            1,
            min=-10,
            max=10,
            group="polynomial_solve_graph",
        ),
        SettingField(
            "root_min",
            "Root min",
            "int",
            -3,
            min=-20,
            max=20,
            group="polynomial_solve_graph",
        ),
        SettingField(
            "root_max",
            "Root max",
            "int",
            3,
            min=-20,
            max=20,
            group="polynomial_solve_graph",
        ),
        SettingField(
            "min_degree",
            "Minimum degree",
            "int",
            2,
            min=2,
            max=3,
            group="polynomial_solve_graph",
        ),
        SettingField(
            "max_degree",
            "Maximum degree",
            "int",
            2,
            min=2,
            max=3,
            group="polynomial_solve_graph",
        ),
        SettingField(
            "integer_only",
            "Integer leading coefficients only",
            "bool",
            True,
            group="polynomial_solve_graph",
        ),
    ]


def number_line_range_settings(
    *,
    min_default: int = -12,
    max_default: int = 12,
    show_zero_default: bool = True,
) -> list[SettingField]:
    return [
        SettingField(
            "number_line_min",
            "Number line min",
            "int",
            min_default,
            min=-50,
            max=0,
            group="graphing",
        ),
        SettingField(
            "number_line_max",
            "Number line max",
            "int",
            max_default,
            min=0,
            max=50,
            group="graphing",
        ),
        SettingField(
            "number_line_show_zero",
            "Show 0 on number line",
            "bool",
            show_zero_default,
            group="graphing",
        ),
        SettingField(
            "number_line_tick_interval",
            "Number line tick interval",
            "int",
            1,
            min=1,
            max=10,
            group="graphing",
        ),
    ]
