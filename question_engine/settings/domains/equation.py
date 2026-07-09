"""Settings fields for equation-solving question types."""

from __future__ import annotations

from ...core.models import SettingField


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
