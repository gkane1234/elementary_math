"""Settings fields for polynomial question types."""

from __future__ import annotations

from ...core.models import SettingField
from ..factoring_settings import shared_factoring_settings


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


def polynomial_factoring_settings() -> list[SettingField]:
    """Re-export factoring method toggles for polynomial types."""
    return shared_factoring_settings()
