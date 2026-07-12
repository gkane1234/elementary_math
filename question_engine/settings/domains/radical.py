"""Settings fields for radical expression question types."""

from __future__ import annotations

from ...core.models import SettingField


def radical_settings(
    *,
    radicand_min_default: int = 12,
    radicand_max_default: int = 300,
    index_default: int = 2,
) -> list[SettingField]:
    return [
        SettingField(
            "radicand_min",
            "Radicand min",
            "int",
            radicand_min_default,
            min=2,
            max=1000,
            group="radical",
        ),
        SettingField(
            "radicand_max",
            "Radicand max",
            "int",
            radicand_max_default,
            min=2,
            max=1000,
            group="radical",
        ),
        SettingField(
            "radical_index",
            "Root index",
            "int",
            index_default,
            min=2,
            max=5,
            group="radical",
        ),
        SettingField(
            "require_simplifiable",
            "Require simplifiable radicals",
            "bool",
            True,
            group="radical",
        ),
    ]


def radical_equation_form_settings() -> list[SettingField]:
    """Selectable templates for radical equations.

    Easy uses a single radical with light prep before squaring. Medium adds
    isolation algebra and √ = linear (extraneous checks). Hard uses two
    radicals that require squaring more than once.
    """
    return [
        SettingField(
            "allow_light_prep",
            "Allow light prep (move constant / divide, then square)",
            "bool",
            True,
            group="radical_equation_forms",
        ),
        SettingField(
            "allow_isolate_algebra",
            "Allow more algebra before isolating the radical",
            "bool",
            False,
            group="radical_equation_forms",
        ),
        SettingField(
            "allow_radical_equals_linear",
            "Allow √(ax + b) = cx + d (check extraneous)",
            "bool",
            False,
            group="radical_equation_forms",
        ),
        SettingField(
            "allow_two_radicals",
            "Allow two radicals (square more than once)",
            "bool",
            False,
            group="radical_equation_forms",
        ),
    ]


def radical_add_subtract_form_settings() -> list[SettingField]:
    """Selectable templates for adding/subtracting radical expressions.

    Easy combines already-simplified like radicals. Medium/Hard require
    factoring perfect squares before combining.
    """
    return [
        SettingField(
            "allow_like_radicals",
            "Allow already-simplified like radicals (e.g. 2√3 + 5√3)",
            "bool",
            True,
            group="radical_add_subtract",
        ),
        SettingField(
            "allow_unsimplified_radicals",
            "Allow unsimplified radicands (e.g. √12 + √3)",
            "bool",
            False,
            group="radical_add_subtract",
        ),
        SettingField(
            "allow_coeff_unsimplified",
            "Allow coefficients on unsimplified radicals (e.g. 2√18 − 3√8)",
            "bool",
            False,
            group="radical_add_subtract",
        ),
        SettingField(
            "coef_min",
            "Coefficient min",
            "int",
            1,
            min=1,
            max=40,
            group="radical_add_subtract",
        ),
        SettingField(
            "coef_max",
            "Coefficient max",
            "int",
            6,
            min=1,
            max=40,
            group="radical_add_subtract",
        ),
        SettingField(
            "min_terms",
            "Min terms",
            "int",
            2,
            min=2,
            max=6,
            group="radical_add_subtract",
        ),
        SettingField(
            "max_terms",
            "Max terms",
            "int",
            2,
            min=2,
            max=6,
            group="radical_add_subtract",
        ),
    ]


def radical_divide_form_settings() -> list[SettingField]:
    """Selectable templates for dividing radical expressions.

    Easy uses already-reduced quotients. Medium/Hard require simplifying
    perfect squares and/or rationalizing the denominator.
    """
    return [
        SettingField(
            "allow_reduced_quotients",
            "Allow already-reduced quotients (e.g. √12/√3, 6√5/2√5)",
            "bool",
            True,
            group="radical_divide",
        ),
        SettingField(
            "allow_simplify_quotients",
            "Allow quotients that need simplify/cancel (e.g. √48/√6 → 2√3)",
            "bool",
            False,
            group="radical_divide",
        ),
        SettingField(
            "allow_rationalize_divide",
            "Allow rationalizing / multi-factor forms (e.g. 3/√5, 6√18/2√8)",
            "bool",
            False,
            group="radical_divide",
        ),
        SettingField(
            "coef_min",
            "Coefficient min",
            "int",
            1,
            min=1,
            max=40,
            group="radical_divide",
        ),
        SettingField(
            "coef_max",
            "Coefficient max",
            "int",
            6,
            min=1,
            max=40,
            group="radical_divide",
        ),
    ]


def radical_multiply_form_settings() -> list[SettingField]:
    """Selectable templates for multiplying radical expressions.

    Easy is √a·√b. Medium adds outer coefficients. Hard uses binomial FOIL.
    """
    return [
        SettingField(
            "allow_simple_product",
            "Allow simple products (√a · √b)",
            "bool",
            True,
            group="radical_multiply",
        ),
        SettingField(
            "allow_coeff_product",
            "Allow coefficient products (k√a · m√b)",
            "bool",
            False,
            group="radical_multiply",
        ),
        SettingField(
            "allow_binomial_product",
            "Allow binomial products ((p√a ± q√b)(…))",
            "bool",
            False,
            group="radical_multiply",
        ),
        SettingField(
            "coef_min",
            "Coefficient min",
            "int",
            1,
            min=1,
            max=40,
            group="radical_multiply",
        ),
        SettingField(
            "coef_max",
            "Coefficient max",
            "int",
            4,
            min=1,
            max=40,
            group="radical_multiply",
        ),
    ]
