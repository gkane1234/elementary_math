from dataclasses import dataclass
from typing import Any

from packages.polynomial_core import FactorablePolynomialOptions

from ..core.models import SettingField

FACTORING_METHOD_KEYS = (
    "factor_rrt",
    "factor_normal",
    "factor_grouping",
    "factor_substitution",
    "factor_difference_of_squares",
    "factor_difference_of_cubes",
    "factor_sum_of_cubes",
)


@dataclass(frozen=True)
class ParsedFactoringSettings:
    leading_coefficient_one: bool
    rrt_mode: str
    enabled_methods: dict[str, bool]
    coef_min: int
    coef_max: int
    positive_leading: bool


def factoring_method_settings() -> list[SettingField]:
    return [
        SettingField(
            "factor_rrt",
            "Rational root theorem (RRT)",
            "bool",
            False,
            group="factoring",
        ),
        SettingField(
            "factor_normal",
            "Normal factoring",
            "bool",
            True,
            group="factoring",
        ),
        SettingField(
            "factor_grouping",
            "Factoring by grouping",
            "bool",
            True,
            group="factoring",
        ),
        SettingField(
            "factor_substitution",
            "Substitution (quadratic form)",
            "bool",
            True,
            group="factoring",
        ),
        SettingField(
            "factor_difference_of_squares",
            "Difference of squares",
            "bool",
            True,
            group="factoring",
        ),
        SettingField(
            "factor_difference_of_cubes",
            "Difference of cubes",
            "bool",
            True,
            group="factoring",
        ),
        SettingField(
            "factor_sum_of_cubes",
            "Sum of cubes",
            "bool",
            True,
            group="factoring",
        ),
    ]


def shared_factoring_settings() -> list[SettingField]:
    return [
        SettingField(
            "leading_coefficient_one",
            "Leading coefficient = 1 only",
            "bool",
            False,
            group="factoring",
        ),
        *factoring_method_settings(),
    ]


def parse_factoring_settings(settings: dict[str, Any]) -> ParsedFactoringSettings:
    coef_min = int(settings.get("coef_min", settings.get("c_min", -8)))
    coef_max = int(settings.get("coef_max", settings.get("c_max", 8)))

    if "factor_rrt" in settings:
        rrt_mode = "allow" if bool(settings.get("factor_rrt")) else "exclude"
    else:
        legacy_rrt = str(settings.get("rrt_mode", "exclude"))
        rrt_mode = "exclude" if legacy_rrt == "exclude" else "allow"

    enabled_methods = {
        "normal": bool(settings.get("factor_normal", True)),
        "grouping": bool(settings.get("factor_grouping", True)),
        "substitution": bool(settings.get("factor_substitution", True)),
        "difference_of_squares": bool(settings.get("factor_difference_of_squares", True)),
        "difference_of_cubes": bool(settings.get("factor_difference_of_cubes", True)),
        "sum_of_cubes": bool(settings.get("factor_sum_of_cubes", True)),
        "rrt": rrt_mode != "exclude",
    }

    return ParsedFactoringSettings(
        leading_coefficient_one=bool(settings.get("leading_coefficient_one", False)),
        rrt_mode=rrt_mode,
        enabled_methods=enabled_methods,
        coef_min=coef_min,
        coef_max=coef_max,
        positive_leading=bool(settings.get("positive_leading_coefficient", True)),
    )


def build_factorable_options(
    settings: dict[str, Any],
    target_degree_min: int,
    target_degree_max: int,
) -> FactorablePolynomialOptions:
    parsed = parse_factoring_settings(settings)
    return FactorablePolynomialOptions(
        coef_min=parsed.coef_min,
        coef_max=parsed.coef_max,
        leading_coefficient_one=parsed.leading_coefficient_one,
        positive_leading=parsed.positive_leading,
        rrt_mode=parsed.rrt_mode,  # type: ignore[arg-type]
        enabled_methods=parsed.enabled_methods,  # type: ignore[arg-type]
        target_degree_min=target_degree_min,
        target_degree_max=target_degree_max,
    )
