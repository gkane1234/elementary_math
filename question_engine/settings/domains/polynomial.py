"""Settings fields for polynomial question types."""

from __future__ import annotations

from ...core.models import SettingField
from ..factoring_settings import shared_factoring_settings


def polynomial_degree_settings(
    *,
    min_degree_default: int = 1,
    max_degree_default: int = 3,
    degree_bound: int = 8,
) -> list[SettingField]:
    return [
        SettingField(
            "min_degree",
            "Degree min",
            "int",
            min_degree_default,
            min=0,
            max=degree_bound,
            group="polynomial",
        ),
        SettingField(
            "max_degree",
            "Degree max",
            "int",
            max_degree_default,
            min=0,
            max=degree_bound,
            group="polynomial",
        ),
    ]


def polynomial_variable_settings() -> list[SettingField]:
    return [
        SettingField(
            "variable",
            "Variable",
            "select",
            "x",
            options=["x", "y", "t", "n"],
            group="polynomial",
        ),
        SettingField(
            "integer_coefficients_only",
            "Integer coefficients only",
            "bool",
            True,
            group="polynomial",
        ),
    ]


def polynomial_division_settings() -> list[SettingField]:
    return [
        SettingField(
            "numerator_degree_min",
            "Numerator degree min",
            "int",
            2,
            min=1,
            max=8,
            group="polynomial",
        ),
        SettingField(
            "numerator_degree_max",
            "Numerator degree max",
            "int",
            4,
            min=1,
            max=8,
            group="polynomial",
        ),
        SettingField(
            "denominator_degree_min",
            "Denominator degree min",
            "int",
            1,
            min=1,
            max=6,
            group="polynomial",
        ),
        SettingField(
            "denominator_degree_max",
            "Denominator degree max",
            "int",
            2,
            min=1,
            max=6,
            group="polynomial",
        ),
        SettingField(
            "divide_cleanly",
            "Divide evenly (no remainder)",
            "bool",
            True,
            group="polynomial",
        ),
    ]


def polynomial_coef_settings(
    *,
    coef_min_default: int = -10,
    coef_max_default: int = 10,
    coef_bound: int = 20,
) -> list[SettingField]:
    return [
        SettingField(
            "coef_min",
            "Coefficient min",
            "int",
            coef_min_default,
            min=-coef_bound,
            max=coef_bound,
            group="polynomial",
        ),
        SettingField(
            "coef_max",
            "Coefficient max",
            "int",
            coef_max_default,
            min=-coef_bound,
            max=coef_bound,
            group="polynomial",
        ),
        SettingField(
            "positive_leading_coefficient",
            "Positive leading coefficient",
            "bool",
            True,
            group="polynomial",
        ),
    ]


def polynomial_multiply_settings() -> list[SettingField]:
    """Factor-shape toggles for polynomial multiplication."""
    return [
        SettingField(
            "allow_monomial_binomial",
            "Allow monomial × binomial",
            "bool",
            True,
            group="polynomial_multiply",
        ),
        SettingField(
            "allow_binomial_binomial",
            "Allow binomial × binomial",
            "bool",
            True,
            group="polynomial_multiply",
        ),
        SettingField(
            "allow_trinomial",
            "Allow a trinomial factor",
            "bool",
            False,
            group="polynomial_multiply",
        ),
        SettingField(
            "leading_coefficient_one",
            "Leading coefficient = 1 only",
            "bool",
            True,
            group="polynomial_multiply",
        ),
        SettingField(
            "max_factor_terms",
            "Max terms per factor",
            "int",
            2,
            min=1,
            max=8,
            group="polynomial_multiply",
        ),
    ]


def polynomial_factoring_settings() -> list[SettingField]:
    """Re-export factoring method toggles for polynomial types."""
    return shared_factoring_settings()
