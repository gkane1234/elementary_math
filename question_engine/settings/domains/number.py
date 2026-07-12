"""Settings fields for numeric expression question types."""

from __future__ import annotations

from ...core.models import SettingField


def number_coef_settings(
    *,
    num_min_default: int = -10,
    num_max_default: int = 10,
    num_bound: int = 50,
) -> list[SettingField]:
    return [
        SettingField(
            "num_min",
            "Numerator min",
            "int",
            num_min_default,
            min=-num_bound,
            max=num_bound,
            group="number",
        ),
        SettingField(
            "num_max",
            "Numerator max",
            "int",
            num_max_default,
            min=-num_bound,
            max=num_bound,
            group="number",
        ),
    ]


def denominator_settings(
    *,
    denom_min_default: int = 2,
    denom_max_default: int = 12,
) -> list[SettingField]:
    return [
        SettingField(
            "denom_min",
            "Denominator min",
            "int",
            denom_min_default,
            min=2,
            max=50,
            group="number",
        ),
        SettingField(
            "denom_max",
            "Denominator max",
            "int",
            denom_max_default,
            min=2,
            max=50,
            group="number",
        ),
    ]


def percent_settings() -> list[SettingField]:
    return [
        SettingField(
            "percent_min",
            "Percent min",
            "int",
            5,
            min=1,
            max=100,
            group="number",
        ),
        SettingField(
            "percent_max",
            "Percent max",
            "int",
            75,
            min=1,
            max=100,
            group="number",
        ),
        SettingField(
            "base_min",
            "Base value min",
            "int",
            10,
            min=1,
            max=1000,
            group="number",
        ),
        SettingField(
            "base_max",
            "Base value max",
            "int",
            200,
            min=1,
            max=1000,
            group="number",
        ),
        SettingField(
            "round_to_whole",
            "Round percent answers to whole numbers",
            "bool",
            False,
            group="number",
        ),
        SettingField(
            "allow_decimal_percents",
            "Allow decimal percents",
            "bool",
            False,
            group="number",
        ),
    ]


def decimal_places_settings() -> list[SettingField]:
    return [
        SettingField(
            "decimal_places",
            "Decimal places",
            "int",
            2,
            min=1,
            max=3,
            group="number",
        ),
    ]


def decimal_multiplication_settings() -> list[SettingField]:
    return [
        SettingField(
            "whole_times_decimal",
            "Whole number times decimal",
            "bool",
            False,
            group="number",
        ),
        SettingField(
            "max_decimal_places",
            "Max decimal places per factor",
            "int",
            2,
            min=1,
            max=3,
            group="number",
        ),
    ]


def allow_negative_settings(*, default: bool = True) -> list[SettingField]:
    return [
        SettingField(
            "allow_negative",
            "Allow negative numbers",
            "bool",
            default,
            group="number",
        ),
    ]


def ratio_settings(
    *,
    part_min_default: int = 2,
    part_max_default: int = 15,
) -> list[SettingField]:
    return [
        SettingField(
            "ratio_part_min",
            "Ratio part min",
            "int",
            part_min_default,
            min=1,
            max=50,
            group="number",
        ),
        SettingField(
            "ratio_part_max",
            "Ratio part max",
            "int",
            part_max_default,
            min=1,
            max=50,
            group="number",
        ),
    ]


def unit_rate_settings() -> list[SettingField]:
    return [
        SettingField(
            "unit_rate_min",
            "Unit rate min",
            "int",
            2,
            min=1,
            max=50,
            group="number",
        ),
        SettingField(
            "unit_rate_max",
            "Unit rate max",
            "int",
            12,
            min=1,
            max=50,
            group="number",
        ),
        SettingField(
            "unit_rate_multiplier_min",
            "Quantity multiplier min",
            "int",
            2,
            min=2,
            max=20,
            group="number",
        ),
        SettingField(
            "unit_rate_multiplier_max",
            "Quantity multiplier max",
            "int",
            8,
            min=2,
            max=20,
            group="number",
        ),
    ]


def scientific_notation_settings() -> list[SettingField]:
    return [
        SettingField(
            "sci_exp_min",
            "Exponent min",
            "int",
            -8,
            min=-12,
            max=12,
            group="number",
        ),
        SettingField(
            "sci_exp_max",
            "Exponent max",
            "int",
            8,
            min=-12,
            max=12,
            group="number",
        ),
        SettingField(
            "allow_negative_exponents",
            "Allow negative exponents",
            "bool",
            True,
            group="number",
        ),
        SettingField(
            "mantissa_decimals",
            "Mantissa decimal places",
            "int",
            1,
            min=1,
            max=3,
            group="number",
        ),
        SettingField(
            "sci_write_direction",
            "Write direction",
            "select",
            "to_sci",
            options=["to_sci", "from_sci", "both", "compare"],
            group="number",
        ),
        SettingField(
            "sci_operation",
            "Multiply / divide",
            "select",
            "mixed",
            options=["multiply", "divide", "mixed"],
            group="number",
        ),
        SettingField(
            "require_normalization",
            "Require renormalization",
            "bool",
            False,
            group="number",
        ),
        SettingField(
            "sci_exp_diff_min",
            "Exponent difference min",
            "int",
            0,
            min=0,
            max=8,
            group="number",
        ),
        SettingField(
            "sci_exp_diff_max",
            "Exponent difference max",
            "int",
            0,
            min=0,
            max=8,
            group="number",
        ),
        SettingField(
            "allow_magnitude_compare",
            "Include magnitude compare",
            "bool",
            False,
            group="number",
        ),
    ]


def factor_bounds_settings(
    *,
    factor_min_default: int = 4,
    factor_max_default: int = 60,
) -> list[SettingField]:
    return [
        SettingField(
            "factor_min",
            "Factor range min",
            "int",
            factor_min_default,
            min=2,
            max=200,
            group="number",
        ),
        SettingField(
            "factor_max",
            "Factor range max",
            "int",
            factor_max_default,
            min=2,
            max=200,
            group="number",
        ),
    ]


def prime_factorization_settings() -> list[SettingField]:
    """Prime-factor count / size knobs for prime factorization prompts."""
    return [
        SettingField(
            "prime_factor_count_min",
            "Prime factor count min",
            "int",
            2,
            min=2,
            max=8,
            group="number",
        ),
        SettingField(
            "prime_factor_count_max",
            "Prime factor count max",
            "int",
            4,
            min=2,
            max=8,
            group="number",
        ),
        SettingField(
            "prime_max",
            "Largest prime factor allowed",
            "int",
            13,
            min=3,
            max=47,
            group="number",
        ),
        SettingField(
            "factor_product_max",
            "Product max",
            "int",
            999,
            min=6,
            max=2000,
            group="number",
        ),
    ]


def gcf_constraint_settings(
    *,
    require_gcf_greater_than_one_default: bool = True,
) -> list[SettingField]:
    """GCF-only: require a non-trivial greatest common factor."""
    return [
        SettingField(
            "require_gcf_greater_than_one",
            "Require GCF > 1",
            "bool",
            require_gcf_greater_than_one_default,
            group="number",
        ),
    ]


def long_division_remainder_settings() -> list[SettingField]:
    """Dividend / divisor bounds for long division with remainders."""
    return [
        SettingField(
            "dividend_min",
            "Dividend min",
            "int",
            10,
            min=1,
            max=10000,
            group="number",
        ),
        SettingField(
            "dividend_max",
            "Dividend max",
            "int",
            99,
            min=1,
            max=10000,
            group="number",
        ),
        SettingField(
            "divisor_min",
            "Divisor min",
            "int",
            2,
            min=2,
            max=49,
            group="number",
        ),
        SettingField(
            "divisor_max",
            "Divisor max",
            "int",
            9,
            min=2,
            max=49,
            group="number",
        ),
    ]


def pemdas_settings() -> list[SettingField]:
    return [
        SettingField(
            "pemdas_complexity",
            "PEMDAS complexity",
            "select",
            "mixed",
            options=["basic", "parentheses", "exponent", "mixed"],
            group="number",
        ),
    ]


def sets_of_numbers_settings() -> list[SettingField]:
    """Controls for classifying numbers into natural/whole/integer/rational/etc."""
    return [
        SettingField(
            "ask_mode",
            "Question style",
            "select",
            "mixed",
            options=["classify", "pick", "membership", "mixed"],
            group="number_sets",
        ),
        SettingField(
            "include_natural",
            "Include natural numbers",
            "bool",
            True,
            group="number_sets",
        ),
        SettingField(
            "include_whole",
            "Include whole numbers",
            "bool",
            True,
            group="number_sets",
        ),
        SettingField(
            "include_integer",
            "Include integers",
            "bool",
            True,
            group="number_sets",
        ),
        SettingField(
            "include_rational",
            "Include rational numbers",
            "bool",
            True,
            group="number_sets",
        ),
        SettingField(
            "include_irrational",
            "Include irrational numbers",
            "bool",
            True,
            group="number_sets",
        ),
        SettingField(
            "include_real",
            "Include real numbers",
            "bool",
            True,
            group="number_sets",
        ),
        SettingField(
            "allow_negative",
            "Allow negative numbers",
            "bool",
            True,
            group="number_sets",
        ),
        SettingField(
            "allow_fractions",
            "Allow fractions / decimals",
            "bool",
            True,
            group="number_sets",
        ),
        SettingField(
            "allow_irrationals",
            "Allow irrational examples (√2, π, …)",
            "bool",
            True,
            group="number_sets",
        ),
        SettingField(
            "num_min",
            "Integer value min",
            "int",
            -12,
            min=-50,
            max=50,
            group="number_sets",
        ),
        SettingField(
            "num_max",
            "Integer value max",
            "int",
            12,
            min=-50,
            max=50,
            group="number_sets",
        ),
    ]
