"""Runtime helpers for reading resolved settings in generators and frameworks."""

from __future__ import annotations

import random
from dataclasses import dataclass
from fractions import Fraction

from ..generators.utils import frac_latex, pick_operation, random_fraction, random_int_range


@dataclass(frozen=True)
class PolynomialParams:
    min_degree: int = 1
    max_degree: int = 3
    coef_min: int = -8
    coef_max: int = 8
    positive_leading: bool = True
    variable: str = "x"
    integer_only: bool = True


def polynomial_params_from_settings(settings: dict) -> PolynomialParams:
    min_degree = int(settings.get("min_degree", 1))
    max_degree = int(settings.get("max_degree", 3))
    if min_degree > max_degree:
        min_degree, max_degree = max_degree, min_degree
    coef_min = int(settings.get("coef_min", -8))
    coef_max = int(settings.get("coef_max", 8))
    from .enrichment import apply_positive_coefficient_restriction, scaled_int_range

    coef_min, coef_max = scaled_int_range(settings, coef_min, coef_max)
    coef_min, coef_max = apply_positive_coefficient_restriction(settings, coef_min, coef_max)
    return PolynomialParams(
        min_degree=min_degree,
        max_degree=max_degree,
        coef_min=coef_min,
        coef_max=coef_max,
        positive_leading=bool(settings.get("positive_leading_coefficient", True)),
        variable=str(settings.get("variable", "x")),
        integer_only=bool(settings.get("integer_coefficients_only", True)),
    )


@dataclass(frozen=True)
class LinearParams:
    slope_min: int = -6
    slope_max: int = 6
    intercept_min: int = -8
    intercept_max: int = 8
    coord_min: int = -8
    coord_max: int = 8
    integer_coordinates: bool = True


def linear_params_from_settings(settings: dict) -> LinearParams:
    slope_min = int(settings.get("slope_min", -6))
    slope_max = int(settings.get("slope_max", 6))
    intercept_min = int(settings.get("intercept_min", -8))
    intercept_max = int(settings.get("intercept_max", 8))
    coord_min = int(settings.get("coord_min", -8))
    coord_max = int(settings.get("coord_max", 8))
    return LinearParams(
        slope_min=min(slope_min, slope_max),
        slope_max=max(slope_min, slope_max),
        intercept_min=min(intercept_min, intercept_max),
        intercept_max=max(intercept_min, intercept_max),
        coord_min=min(coord_min, coord_max),
        coord_max=max(coord_min, coord_max),
        integer_coordinates=bool(settings.get("integer_coordinates", True)),
    )


def random_slope(params: LinearParams) -> int:
    return random_int_range(params.slope_min, params.slope_max, exclude={0})


def random_intercept(params: LinearParams) -> int:
    return random.randint(params.intercept_min, params.intercept_max)


def random_coordinate(params: LinearParams) -> int:
    return random.randint(params.coord_min, params.coord_max)


def allowed_equation_operations(settings: dict) -> list[str]:
    ops: list[str] = []
    if bool(settings.get("allow_add", True)):
        ops.append("+")
    if bool(settings.get("allow_subtract", True)):
        ops.append("-")
    if bool(settings.get("allow_multiply", True)):
        ops.append("*")
    if bool(settings.get("allow_divide", True)):
        ops.append("/")
    return ops or ["+", "-"]


def allowed_rational_operations(settings: dict) -> list[str]:
    ops: list[str] = []
    if bool(settings.get("allow_add", True)):
        ops.append("+")
    if bool(settings.get("allow_subtract", True)):
        ops.append("-")
    return ops or ["+", "-"]


@dataclass(frozen=True)
class RadicalParams:
    radicand_min: int = 12
    radicand_max: int = 300
    radical_index: int = 2
    require_simplifiable: bool = True


def radical_params_from_settings(settings: dict) -> RadicalParams:
    radicand_min = int(settings.get("radicand_min", 12))
    radicand_max = int(settings.get("radicand_max", 300))
    if radicand_min > radicand_max:
        radicand_min, radicand_max = radicand_max, radicand_min
    return RadicalParams(
        radicand_min=radicand_min,
        radicand_max=radicand_max,
        radical_index=int(settings.get("radical_index", 2)),
        require_simplifiable=bool(settings.get("require_simplifiable", True)),
    )


@dataclass(frozen=True)
class MiscExpressionParams:
    term_count: int = 4
    exponent_min: int = 2
    exponent_max: int = 7
    phrase_complexity: str = "standard"
    constant_min: int = 2
    constant_max: int = 12
    coef_min: int = -12
    coef_max: int = 12
    variable: str = "x"
    max_phrase_operations: int = 2
    allow_fraction_constants: bool = False


def misc_expression_params_from_settings(settings: dict) -> MiscExpressionParams:
    exponent_min = int(settings.get("exponent_min", 2))
    exponent_max = int(settings.get("exponent_max", 7))
    constant_min = int(settings.get("constant_min", 2))
    constant_max = int(settings.get("constant_max", 12))
    coef_min = int(settings.get("coef_min", -12))
    coef_max = int(settings.get("coef_max", 12))
    from .enrichment import apply_positive_coefficient_restriction, scaled_int_range

    coef_min, coef_max = scaled_int_range(settings, coef_min, coef_max)
    coef_min, coef_max = apply_positive_coefficient_restriction(settings, coef_min, coef_max)
    return MiscExpressionParams(
        term_count=int(settings.get("term_count", 4)),
        exponent_min=min(exponent_min, exponent_max),
        exponent_max=max(exponent_min, exponent_max),
        phrase_complexity=str(settings.get("phrase_complexity", "standard")),
        constant_min=min(constant_min, constant_max),
        constant_max=max(constant_min, constant_max),
        coef_min=coef_min,
        coef_max=coef_max,
        variable=str(settings.get("variable", "x")),
        max_phrase_operations=int(settings.get("max_phrase_operations", 2)),
        allow_fraction_constants=bool(settings.get("allow_fraction_constants", False)),
    )


@dataclass(frozen=True)
class EquationParams:
    variable: str = "x"
    coef_min: int = -12
    coef_max: int = 12
    integer_only: bool = True


def equation_params_from_settings(settings: dict) -> EquationParams:
    coef_min = int(settings.get("coef_min", -12))
    coef_max = int(settings.get("coef_max", 12))
    if coef_min > coef_max:
        coef_min, coef_max = coef_max, coef_min
    from .enrichment import apply_positive_coefficient_restriction, scaled_int_range

    coef_min, coef_max = scaled_int_range(settings, coef_min, coef_max)
    coef_min, coef_max = apply_positive_coefficient_restriction(settings, coef_min, coef_max)

    integer_only = settings.get("integer_only")
    if integer_only is None:
        integer_only = settings.get("solution_type", "integer") == "integer"

    return EquationParams(
        variable=str(settings.get("variable", "x")),
        coef_min=coef_min,
        coef_max=coef_max,
        integer_only=bool(integer_only),
    )


def random_equation_solution(params: EquationParams) -> int | Fraction:
    lo, hi = params.coef_min, params.coef_max
    if lo > hi:
        lo, hi = hi, lo
    if params.integer_only:
        return random.randint(lo, hi)
    return random_fraction(
        num_min=lo,
        num_max=hi,
        denom_min=2,
        denom_max=6,
    )


def pick_equation_solution(settings: dict, params: EquationParams) -> int | Fraction:
    """Sample a solution honoring exclude-zero and difficulty-scaled bounds."""
    from .enrichment import solution_allowed

    for _ in range(40):
        value = random_equation_solution(params)
        if solution_allowed(settings, value):
            return value
    return 1 if params.coef_min <= 1 <= params.coef_max else params.coef_min


def format_solution_value(value: int | Fraction, settings: dict | None = None) -> str:
    if settings is not None:
        from .enrichment import format_answer_value

        return format_answer_value(settings, value)
    if isinstance(value, Fraction):
        return frac_latex(value)
    return str(value)


@dataclass(frozen=True)
class TrigonometryParams:
    angle_unit: str = "degrees"
    angle_min: int = 0
    angle_max: int = 360
    unit_circle_only: bool = True
    functions: tuple[str, ...] = ("sin", "cos", "tan")
    allow_reciprocal_identities: bool = True
    allow_pythagorean_identities: bool = True


def trigonometry_params_from_settings(settings: dict) -> TrigonometryParams:
    functions: list[str] = []
    if bool(settings.get("allow_sin", True)):
        functions.append("sin")
    if bool(settings.get("allow_cos", True)):
        functions.append("cos")
    if bool(settings.get("allow_tan", True)):
        functions.append("tan")
    if bool(settings.get("allow_cot", False)):
        functions.append("cot")
    if not functions:
        functions = ["sin", "cos", "tan"]
    angle_min = int(settings.get("angle_min", 0))
    angle_max = int(settings.get("angle_max", 360))
    return TrigonometryParams(
        angle_unit=str(settings.get("angle_unit", "degrees")),
        angle_min=min(angle_min, angle_max),
        angle_max=max(angle_min, angle_max),
        unit_circle_only=bool(settings.get("unit_circle_only", True)),
        functions=tuple(functions),
        allow_reciprocal_identities=bool(settings.get("allow_reciprocal_identities", True)),
        allow_pythagorean_identities=bool(settings.get("allow_pythagorean_identities", True)),
    )


@dataclass(frozen=True)
class LogarithmParams:
    base_min: int = 2
    base_max: int = 10
    allow_natural_log: bool = True
    allow_common_log: bool = True
    argument_min: int = 2
    argument_max: int = 1000
    require_integer_result: bool = True
    allow_change_of_base: bool = True


def logarithm_params_from_settings(settings: dict) -> LogarithmParams:
    base_min = int(settings.get("log_base_min", 2))
    base_max = int(settings.get("log_base_max", 10))
    arg_min = int(settings.get("log_argument_min", 2))
    arg_max = int(settings.get("log_argument_max", 1000))
    return LogarithmParams(
        base_min=min(base_min, base_max),
        base_max=max(base_min, base_max),
        allow_natural_log=bool(settings.get("allow_natural_log", True)),
        allow_common_log=bool(settings.get("allow_common_log", True)),
        argument_min=min(arg_min, arg_max),
        argument_max=max(arg_min, arg_max),
        require_integer_result=bool(settings.get("require_integer_result", True)),
        allow_change_of_base=bool(settings.get("allow_change_of_base", True)),
    )


@dataclass(frozen=True)
class ExponentialParams:
    base_min: int = 2
    base_max: int = 10
    exponent_min: int = 1
    exponent_max: int = 5
    allow_fractional_exponents: bool = False
    coef_min: int = -6
    coef_max: int = 6


def exponential_params_from_settings(settings: dict) -> ExponentialParams:
    base_min = int(settings.get("exp_base_min", 2))
    base_max = int(settings.get("exp_base_max", 10))
    exp_min = int(settings.get("exp_exponent_min", 1))
    exp_max = int(settings.get("exp_exponent_max", 5))
    coef_min = int(settings.get("coef_min", -6))
    coef_max = int(settings.get("coef_max", 6))
    return ExponentialParams(
        base_min=min(base_min, base_max),
        base_max=max(base_min, base_max),
        exponent_min=min(exp_min, exp_max),
        exponent_max=max(exp_min, exp_max),
        allow_fractional_exponents=bool(settings.get("allow_fractional_exponents", False)),
        coef_min=min(coef_min, coef_max),
        coef_max=max(coef_min, coef_max),
    )


@dataclass(frozen=True)
class SequenceParams:
    first_term_min: int = -10
    first_term_max: int = 10
    nth_min: int = 3
    nth_max: int = 12
    common_diff_min: int = -8
    common_diff_max: int = 8
    common_ratio_min: int = -4
    common_ratio_max: int = 4
    allow_negative_ratio: bool = False
    integer_terms_only: bool = True


def sequence_params_from_settings(settings: dict) -> SequenceParams:
    first_min = int(settings.get("first_term_min", -10))
    first_max = int(settings.get("first_term_max", 10))
    nth_min = int(settings.get("nth_min", 3))
    nth_max = int(settings.get("nth_max", 12))
    diff_min = int(settings.get("common_diff_min", -8))
    diff_max = int(settings.get("common_diff_max", 8))
    ratio_min = int(settings.get("common_ratio_min", -4))
    ratio_max = int(settings.get("common_ratio_max", 4))
    return SequenceParams(
        first_term_min=min(first_min, first_max),
        first_term_max=max(first_min, first_max),
        nth_min=min(nth_min, nth_max),
        nth_max=max(nth_min, nth_max),
        common_diff_min=min(diff_min, diff_max),
        common_diff_max=max(diff_min, diff_max),
        common_ratio_min=min(ratio_min, ratio_max),
        common_ratio_max=max(ratio_min, ratio_max),
        allow_negative_ratio=bool(settings.get("allow_negative_ratio", False)),
        integer_terms_only=bool(settings.get("integer_terms_only", True)),
    )


@dataclass(frozen=True)
class CalculusParams:
    coef_min: int = -6
    coef_max: int = 6
    power_min: int = 1
    power_max: int = 3
    term_count: int = 2
    include_constant_term: bool = True
    variable: str = "x"
    limit_approach_min: int = -5
    limit_approach_max: int = 5
    allow_infinity: bool = False
    require_positive_power: bool = True


def calculus_params_from_settings(settings: dict) -> CalculusParams:
    coef_min = int(settings.get("coef_min", -6))
    coef_max = int(settings.get("coef_max", 6))
    power_min = int(settings.get("power_min", 1))
    power_max = int(settings.get("power_max", 3))
    approach_min = int(settings.get("limit_approach_min", -5))
    approach_max = int(settings.get("limit_approach_max", 5))
    return CalculusParams(
        coef_min=min(coef_min, coef_max),
        coef_max=max(coef_min, coef_max),
        power_min=min(power_min, power_max),
        power_max=max(power_min, power_max),
        term_count=int(settings.get("term_count", 2)),
        include_constant_term=bool(settings.get("include_constant_term", True)),
        variable=str(settings.get("variable", "x")),
        limit_approach_min=min(approach_min, approach_max),
        limit_approach_max=max(approach_min, approach_max),
        allow_infinity=bool(settings.get("allow_infinity", False)),
        require_positive_power=bool(settings.get("require_positive_power", True)),
    )


def allowed_inequality_symbols(settings: dict) -> list[str]:
    symbols: list[str] = []
    if bool(settings.get("allow_lt", True)):
        symbols.append("<")
    if bool(settings.get("allow_gt", True)):
        symbols.append(">")
    if bool(settings.get("allow_lte", True)):
        symbols.append(r"\leq")
    if bool(settings.get("allow_gte", True)):
        symbols.append(r"\geq")
    return symbols or ["<", ">"]
