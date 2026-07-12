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
    "factor_perfect_square_trinomial",
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
            "factor_perfect_square_trinomial",
            "Perfect square trinomial",
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


def special_case_extra_settings() -> list[SettingField]:
    """Settings specific to special-product factoring types."""
    return [
        SettingField(
            "allow_higher_even_powers",
            "Higher even powers (x⁴−1, x⁸−1, …)",
            "bool",
            False,
            group="factoring",
        ),
        SettingField(
            "max_even_power",
            "Max even power for higher-power problems",
            "int",
            8,
            min=4,
            max=8,
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
        SettingField(
            "monic_only",
            "Monic polynomials only (leading coeff 1)",
            "bool",
            False,
            group="factoring",
        ),
        SettingField(
            "require_gcf",
            "Require GCF factoring step",
            "bool",
            False,
            group="factoring",
        ),
        SettingField(
            "difference_of_squares_only",
            "Difference of squares only",
            "bool",
            False,
            group="factoring",
        ),
        *factoring_method_settings(),
    ]


def factoring_method_overrides(settings: dict[str, Any]) -> dict[str, bool]:
    """Map UI factoring toggles to enabled_methods for polynomial_core."""
    if bool(settings.get("difference_of_squares_only", False)):
        return {
            "factor_normal": False,
            "factor_grouping": False,
            "factor_substitution": False,
            "factor_difference_of_squares": True,
            "factor_perfect_square_trinomial": False,
            "factor_difference_of_cubes": False,
            "factor_sum_of_cubes": False,
            "factor_rrt": False,
        }

    if bool(settings.get("require_gcf", False)):
        return {
            "factor_normal": True,
            "factor_grouping": False,
            "factor_substitution": False,
            "factor_difference_of_squares": False,
            "factor_perfect_square_trinomial": False,
            "factor_difference_of_cubes": False,
            "factor_sum_of_cubes": False,
            "factor_rrt": False,
        }

    return {}


def parse_factoring_settings(settings: dict[str, Any]) -> ParsedFactoringSettings:
    coef_min = int(settings.get("coef_min", settings.get("c_min", -8)))
    coef_max = int(settings.get("coef_max", settings.get("c_max", 8)))

    if "factor_rrt" in settings:
        rrt_mode = "allow" if bool(settings.get("factor_rrt")) else "exclude"
    else:
        legacy_rrt = str(settings.get("rrt_mode", "exclude"))
        rrt_mode = "exclude" if legacy_rrt == "exclude" else "allow"

    overrides = factoring_method_overrides(settings)
    enabled_methods = {
        "normal": bool(overrides.get("factor_normal", settings.get("factor_normal", True))),
        "grouping": bool(overrides.get("factor_grouping", settings.get("factor_grouping", True))),
        "substitution": bool(
            overrides.get("factor_substitution", settings.get("factor_substitution", True))
        ),
        "difference_of_squares": bool(
            overrides.get(
                "factor_difference_of_squares",
                settings.get("factor_difference_of_squares", True),
            )
        ),
        "perfect_square_trinomial": bool(
            overrides.get(
                "factor_perfect_square_trinomial",
                settings.get("factor_perfect_square_trinomial", True),
            )
        ),
        "difference_of_cubes": bool(
            overrides.get(
                "factor_difference_of_cubes",
                settings.get("factor_difference_of_cubes", True),
            )
        ),
        "sum_of_cubes": bool(
            overrides.get("factor_sum_of_cubes", settings.get("factor_sum_of_cubes", True))
        ),
        "rrt": rrt_mode != "exclude" and bool(overrides.get("factor_rrt", True)),
    }

    leading_one = bool(settings.get("leading_coefficient_one", False)) or bool(
        settings.get("monic_only", False)
    )

    return ParsedFactoringSettings(
        leading_coefficient_one=leading_one,
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
