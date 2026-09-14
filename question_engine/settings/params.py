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


def allowed_division_notations(settings: dict) -> list[str]:
    """Enabled fraction-division prompt forms; falls back to obelus if none selected."""
    forms: list[str] = []
    if bool(settings.get("allow_obelus", True)):
        forms.append("obelus")
    if bool(settings.get("allow_complex_fraction", True)):
        forms.append("complex_fraction")
    if bool(settings.get("allow_slash", True)):
        forms.append("slash")
    return forms or ["obelus"]


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
    local = apply_trigonometry_continuous_knobs(settings)
    functions: list[str] = []
    if bool(local.get("allow_sin", True)):
        functions.append("sin")
    if bool(local.get("allow_cos", True)):
        functions.append("cos")
    if bool(local.get("allow_tan", True)):
        functions.append("tan")
    if bool(local.get("allow_cot", False)):
        functions.append("cot")
    if not functions:
        functions = ["sin", "cos", "tan"]
    angle_min = int(local.get("angle_min", 0))
    angle_max = int(local.get("angle_max", 360))
    return TrigonometryParams(
        angle_unit=str(local.get("angle_unit", "degrees")),
        angle_min=min(angle_min, angle_max),
        angle_max=max(angle_min, angle_max),
        unit_circle_only=bool(local.get("unit_circle_only", True)),
        functions=tuple(functions),
        allow_reciprocal_identities=bool(local.get("allow_reciprocal_identities", True)),
        allow_pythagorean_identities=bool(local.get("allow_pythagorean_identities", True)),
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
    local = apply_logarithm_continuous_knobs(settings)
    base_min = int(local.get("log_base_min", 2))
    base_max = int(local.get("log_base_max", 10))
    arg_min = int(local.get("log_argument_min", 2))
    arg_max = int(local.get("log_argument_max", 1000))
    return LogarithmParams(
        base_min=min(base_min, base_max),
        base_max=max(base_min, base_max),
        allow_natural_log=bool(local.get("allow_natural_log", True)),
        allow_common_log=bool(local.get("allow_common_log", True)),
        argument_min=min(arg_min, arg_max),
        argument_max=max(arg_min, arg_max),
        require_integer_result=bool(local.get("require_integer_result", True)),
        allow_change_of_base=bool(local.get("allow_change_of_base", True)),
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


def apply_exponential_continuous_knobs(settings: dict) -> dict:
    """Map continuous D → exponential base/exponent/coef ladders."""
    d = _continuous_d_or_none(settings)
    if d is None:
        return settings
    out = dict(settings)
    if d < 4.0:
        out["exp_base_min"], out["exp_base_max"] = 2, 4
        out["exp_exponent_min"], out["exp_exponent_max"] = 1, 3
        out["coef_min"], out["coef_max"] = -3, 3
        out["allow_fractional_exponents"] = False
    elif d < 10.0:
        out["exp_base_min"], out["exp_base_max"] = 2, 6
        out["exp_exponent_min"], out["exp_exponent_max"] = 1, 4
        out["coef_min"], out["coef_max"] = -5, 5
        out["allow_fractional_exponents"] = False
    elif d < 16.0:
        out["exp_base_min"], out["exp_base_max"] = 2, 10
        out["exp_exponent_min"], out["exp_exponent_max"] = 1, 5
        out["coef_min"], out["coef_max"] = -8, 8
        out["allow_fractional_exponents"] = d >= 14.0
    else:
        span = min(16, 10 + int((d - 16) // 4))
        out["exp_base_min"], out["exp_base_max"] = 2, span
        out["exp_exponent_min"], out["exp_exponent_max"] = 1, min(8, 5 + int((d - 16) // 5))
        cspan = min(16, 8 + int(d // 4))
        out["coef_min"], out["coef_max"] = -cspan, cspan
        out["allow_fractional_exponents"] = True
    return out


def exponential_params_from_settings(settings: dict) -> ExponentialParams:
    local = apply_exponential_continuous_knobs(settings)
    base_min = int(local.get("exp_base_min", 2))
    base_max = int(local.get("exp_base_max", 10))
    exp_min = int(local.get("exp_exponent_min", 1))
    exp_max = int(local.get("exp_exponent_max", 5))
    coef_min = int(local.get("coef_min", -6))
    coef_max = int(local.get("coef_max", 6))
    return ExponentialParams(
        base_min=min(base_min, base_max),
        base_max=max(base_min, base_max),
        exponent_min=min(exp_min, exp_max),
        exponent_max=max(exp_min, exp_max),
        allow_fractional_exponents=bool(local.get("allow_fractional_exponents", False)),
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
    local = apply_sequence_continuous_knobs(settings)
    first_min = int(local.get("first_term_min", -10))
    first_max = int(local.get("first_term_max", 10))
    nth_min = int(local.get("nth_min", 3))
    nth_max = int(local.get("nth_max", 12))
    diff_min = int(local.get("common_diff_min", -8))
    diff_max = int(local.get("common_diff_max", 8))
    ratio_min = int(local.get("common_ratio_min", -4))
    ratio_max = int(local.get("common_ratio_max", 4))
    return SequenceParams(
        first_term_min=min(first_min, first_max),
        first_term_max=max(first_min, first_max),
        nth_min=min(nth_min, nth_max),
        nth_max=max(nth_min, nth_max),
        common_diff_min=min(diff_min, diff_max),
        common_diff_max=max(diff_min, diff_max),
        common_ratio_min=min(ratio_min, ratio_max),
        common_ratio_max=max(ratio_min, ratio_max),
        allow_negative_ratio=bool(local.get("allow_negative_ratio", False)),
        integer_terms_only=bool(local.get("integer_terms_only", True)),
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


def _continuous_d_or_none(settings: dict) -> float | None:
    """Return continuous difficulty when present as a numeric value."""
    if "difficulty" not in settings or settings["difficulty"] is None:
        return None
    try:
        return float(settings["difficulty"])
    except (TypeError, ValueError):
        return None


def apply_calculus_continuous_knobs(settings: dict) -> dict:
    """Map continuous D → poly term/power/coef knobs for limits/derivatives/integrals.

    Returns a shallow copy with knobs filled when continuous ``difficulty`` is set;
    otherwise returns ``settings`` unchanged so EMH / explicit knobs win.
    """
    d = _continuous_d_or_none(settings)
    if d is None:
        return settings
    out = dict(settings)
    if d < 4.0:
        out["term_count"] = 1
        out["power_min"] = 1
        out["power_max"] = 2
        out["coef_min"], out["coef_max"] = -3, 3
        out["limit_approach_min"], out["limit_approach_max"] = -3, 3
        out["allow_infinity"] = False
    elif d < 10.0:
        out["term_count"] = 2
        out["power_min"] = 0
        out["power_max"] = 3
        out["coef_min"], out["coef_max"] = -5, 5
        out["limit_approach_min"], out["limit_approach_max"] = -5, 5
        out["allow_infinity"] = False
    elif d < 16.0:
        out["term_count"] = 3
        out["power_min"] = 0
        out["power_max"] = 4
        out["coef_min"], out["coef_max"] = -8, 8
        out["limit_approach_min"], out["limit_approach_max"] = -8, 8
        out["allow_infinity"] = d >= 12.0
    else:
        out["term_count"] = min(5, 3 + int((d - 16) // 6))
        out["power_min"] = 0
        out["power_max"] = min(8, 4 + int((d - 16) // 5))
        span = min(20, 8 + int(d // 4))
        out["coef_min"], out["coef_max"] = -span, span
        out["limit_approach_min"], out["limit_approach_max"] = -span, span
        out["allow_infinity"] = True
    return out


def apply_logarithm_continuous_knobs(settings: dict) -> dict:
    """Map continuous D → log base/argument / integer-exponent ladders."""
    d = _continuous_d_or_none(settings)
    if d is None:
        return settings
    out = dict(settings)
    if d < 4.0:
        out["log_base_min"], out["log_base_max"] = 2, 5
        out["log_argument_max"] = 32
        out["require_integer_result"] = True
        out["allow_natural_log"] = False
        out["allow_common_log"] = False
    elif d < 10.0:
        out["log_base_min"], out["log_base_max"] = 2, 10
        out["log_argument_max"] = 256
        out["require_integer_result"] = True
        out["allow_natural_log"] = False
        out["allow_common_log"] = True
    elif d < 16.0:
        out["log_base_min"], out["log_base_max"] = 2, 10
        out["log_argument_max"] = 1000
        out["require_integer_result"] = True
        out["allow_natural_log"] = True
        out["allow_common_log"] = True
    else:
        out["log_base_min"], out["log_base_max"] = 2, 12
        out["log_argument_max"] = max(1000, int(200 * d))
        out["require_integer_result"] = d < 22.0
        out["allow_natural_log"] = True
        out["allow_common_log"] = True
    return out


def apply_trigonometry_continuous_knobs(settings: dict) -> dict:
    """Map continuous D → trig function unlock + angle span + identity / graph knobs."""
    d = _continuous_d_or_none(settings)
    if d is None:
        return settings
    out = dict(settings)
    out["allow_sin"] = True
    out["allow_cos"] = True
    if d < 4.0:
        out["allow_tan"] = False
        out["allow_cot"] = False
        out["angle_max"] = 180
        out["allow_reciprocal_identities"] = False
        out["allow_pythagorean_identities"] = True
        out["allow_sum_difference_identities"] = False
        out["allow_double_angle_identities"] = False
        out["allow_product_to_sum_identities"] = False
        out["trig_amp_max"] = 1
        out["trig_period_factor_max"] = 1
        out["allow_trig_phase"] = False
        out["allow_trig_reflection"] = False
    elif d < 10.0:
        out["allow_tan"] = True
        out["allow_cot"] = False
        out["angle_max"] = 360
        out["allow_reciprocal_identities"] = True
        out["allow_pythagorean_identities"] = True
        out["allow_sum_difference_identities"] = d >= 6.0
        out["allow_double_angle_identities"] = d >= 7.0
        out["allow_product_to_sum_identities"] = False
        out["trig_amp_max"] = 2 + int(d // 5)
        out["trig_period_factor_max"] = 1
        out["allow_trig_phase"] = False
        out["allow_trig_reflection"] = d >= 8.0
    elif d < 16.0:
        out["allow_tan"] = True
        out["allow_cot"] = True
        out["angle_max"] = 360
        out["allow_reciprocal_identities"] = True
        out["allow_pythagorean_identities"] = True
        out["allow_sum_difference_identities"] = True
        out["allow_double_angle_identities"] = True
        out["allow_product_to_sum_identities"] = d >= 12.0
        out["trig_amp_max"] = 3 + int((d - 10) // 3)
        out["trig_period_factor_max"] = 2 if d < 14.0 else 3
        out["allow_trig_phase"] = d >= 12.0
        out["allow_trig_reflection"] = True
    else:
        out["allow_tan"] = True
        out["allow_cot"] = True
        out["angle_max"] = 720
        out["allow_reciprocal_identities"] = True
        out["allow_pythagorean_identities"] = True
        out["allow_sum_difference_identities"] = True
        out["allow_double_angle_identities"] = True
        out["allow_product_to_sum_identities"] = True
        out["trig_amp_max"] = min(6, 4 + int((d - 16) // 4))
        out["trig_period_factor_max"] = min(4, 3 + int((d - 16) // 6))
        out["allow_trig_phase"] = True
        out["allow_trig_reflection"] = True
    return out


def trig_graph_structure_from_continuous(settings: dict) -> dict | None:
    """Map continuous D → graphing-trig mode (parent / amplitude / transform)."""
    d = _continuous_d_or_none(settings)
    if d is None:
        return None
    local = apply_trigonometry_continuous_knobs(settings)
    if d < 4.0:
        mode = "parent"
    elif d < 10.0:
        mode = "amplitude"
    else:
        mode = "transform"
    return {
        "difficulty": d,
        "mode": mode,
        "amp_max": int(local.get("trig_amp_max", 1)),
        "period_factor_max": int(local.get("trig_period_factor_max", 1)),
        "allow_phase": bool(local.get("allow_trig_phase", False)),
        "allow_reflection": bool(local.get("allow_trig_reflection", False)),
    }


def apply_sequence_continuous_knobs(settings: dict) -> dict:
    """Map continuous D → arithmetic/geometric sequence term & ratio spans."""
    d = _continuous_d_or_none(settings)
    if d is None:
        return settings
    out = dict(settings)
    if d < 4.0:
        out["first_term_min"], out["first_term_max"] = -5, 5
        out["nth_min"], out["nth_max"] = 3, 6
        out["common_diff_min"], out["common_diff_max"] = -3, 3
        out["common_ratio_min"], out["common_ratio_max"] = 2, 3
        out["allow_negative_ratio"] = False
    elif d < 10.0:
        out["first_term_min"], out["first_term_max"] = -8, 8
        out["nth_min"], out["nth_max"] = 3, 8 + int(d // 4)
        out["common_diff_min"], out["common_diff_max"] = -5, 5
        out["common_ratio_min"], out["common_ratio_max"] = -2 if d >= 7.0 else 2, 4
        out["allow_negative_ratio"] = d >= 7.0
    elif d < 16.0:
        out["first_term_min"], out["first_term_max"] = -12, 12
        out["nth_min"], out["nth_max"] = 4, 12
        out["common_diff_min"], out["common_diff_max"] = -8, 8
        out["common_ratio_min"], out["common_ratio_max"] = -3, 5
        out["allow_negative_ratio"] = True
    else:
        span = min(20, 12 + int((d - 16) // 3))
        out["first_term_min"], out["first_term_max"] = -span, span
        out["nth_min"], out["nth_max"] = 5, min(20, 12 + int((d - 16) // 3))
        out["common_diff_min"], out["common_diff_max"] = -min(12, 8 + int((d - 16) // 4)), min(
            12, 8 + int((d - 16) // 4)
        )
        out["common_ratio_min"], out["common_ratio_max"] = -4, min(6, 4 + int((d - 16) // 5))
        out["allow_negative_ratio"] = True
    return out


def geometry_proof_structure_from_continuous(settings: dict) -> dict | None:
    """Map continuous D → congruence-theorem / similarity proof pool."""
    d = _continuous_d_or_none(settings)
    if d is None:
        return None
    local = apply_geometry_continuous_knobs(settings)
    if d < 4.0:
        theorems = ("SSS",)
        band = "easy"
    elif d < 10.0:
        theorems = ("SSS", "SAS", "ASA")
        band = "medium"
    elif d < 16.0:
        theorems = ("SAS", "ASA", "AAS", "HL")
        band = "hard"
    else:
        theorems = ("ASA", "AAS", "HL", "SAS")
        band = "hard"
    return {
        "difficulty": d,
        "band": band,
        "theorems": theorems,
        "similarity_ratio_min": int(local.get("similarity_ratio_min", 2)),
        "similarity_ratio_max": int(local.get("similarity_ratio_max", 4)),
        "side_min": int(local.get("side_min", 3)),
        "side_max": int(local.get("side_max", 12)),
        "angle_min": int(local.get("angle_min", 20)),
        "angle_max": int(local.get("angle_max", 120)),
        "coord_min": int(local.get("coord_min", -5)),
        "coord_max": int(local.get("coord_max", 5)),
        "allow_dilation": d >= 10.0,
        "allow_composition": d >= 14.0,
    }


def calc_application_structure_from_continuous(settings: dict) -> dict | None:
    """Map continuous D → related-rates / volume / DE / optimization structure."""
    d = _continuous_d_or_none(settings)
    if d is None:
        return None
    # related_frames: OpenStax §4.1 rotation + easy leftover lockout
    # (see related_rates_frames.related_frames_for_difficulty).
    # related_shapes kept for volume/legacy callers (circle/sphere/cone).
    # volume_methods: leftover lockout of disk_linear (out at d>=10) and
    # disk_quadratic (out at d>=16). shell/cross_semi aliases collapsed —
    # those leaves have their own generators; this leaf's high-D builder is washer.
    from question_engine.frameworks.primitives.optimization_frames import (
        optimization_frames_for_difficulty,
    )
    from question_engine.frameworks.primitives.related_rates_frames import (
        related_frames_for_difficulty,
    )

    related_frames = related_frames_for_difficulty(d)
    opt_frames = optimization_frames_for_difficulty(d)
    if d < 4.0:
        return {
            "difficulty": d,
            "band": "easy",
            "radius_max": 5,
            "rate_max": 3,
            "bound_max": 4,
            "related_shapes": ("circle",),
            "related_frames": related_frames,
            "volume_methods": ("disk_linear",),
            "de_family": "poly",
            "opt_perimeter_max": 20,
            "opt_shapes": ("square",),
            "opt_frames": opt_frames,
        }
    if d < 10.0:
        return {
            "difficulty": d,
            "band": "medium",
            "radius_max": 6 + int(d // 3),
            "rate_max": 4 + int(d // 5),
            "bound_max": 5,
            "related_shapes": ("circle", "sphere"),
            "related_frames": related_frames,
            "volume_methods": ("disk_linear", "disk_quadratic"),
            "de_family": "exp",
            "opt_perimeter_max": 24 + int(d),
            "opt_shapes": ("square", "rectangle"),
            "opt_frames": opt_frames,
        }
    if d < 16.0:
        return {
            "difficulty": d,
            "band": "hard",
            "radius_max": 10 + int((d - 10) // 2),
            "rate_max": 6,
            "bound_max": 5 + int((d - 10) // 3),
            "related_shapes": ("circle", "sphere", "cone"),
            "related_frames": related_frames,
            "volume_methods": ("disk_quadratic", "washer"),
            "de_family": "homogeneous",
            "opt_perimeter_max": 36 + int(d),
            "opt_shapes": ("square", "rectangle", "cylinder"),
            "opt_frames": opt_frames,
        }
    return {
        "difficulty": d,
        "band": "hard",
        "radius_max": min(20, 12 + int((d - 16) // 2)),
        "rate_max": min(10, 6 + int((d - 16) // 4)),
        "bound_max": min(8, 5 + int((d - 16) // 3)),
        "related_shapes": ("circle", "sphere", "cone"),
        "related_frames": related_frames,
        "volume_methods": ("washer",),
        "de_family": "homogeneous",
        "opt_perimeter_max": min(80, 40 + int(d)),
        "opt_shapes": ("square", "rectangle", "cylinder"),
        "opt_frames": opt_frames,
    }


def piecewise_structure_from_continuous(settings: dict) -> dict | None:
    """Map continuous D → piecewise piece count / coef / breakpoint spans."""
    d = _continuous_d_or_none(settings)
    if d is None:
        return None
    if d < 4.0:
        return {
            "difficulty": d,
            "piece_count": 2,
            "coef_span": 3,
            "breakpoint_span": 2,
            "allow_quadratic_piece": False,
        }
    if d < 10.0:
        return {
            "difficulty": d,
            "piece_count": 2,
            "coef_span": 4 + int(d // 4),
            "breakpoint_span": 3,
            "allow_quadratic_piece": d >= 7.0,
        }
    if d < 16.0:
        return {
            "difficulty": d,
            "piece_count": 3 if d >= 12.0 else 2,
            "coef_span": 6 + int((d - 10) // 3),
            "breakpoint_span": 4,
            "allow_quadratic_piece": True,
        }
    return {
        "difficulty": d,
        "piece_count": min(4, 3 + int((d - 16) // 8)),
        "coef_span": min(12, 7 + int((d - 16) // 3)),
        "breakpoint_span": min(8, 4 + int((d - 16) // 4)),
        "allow_quadratic_piece": True,
    }


def apply_geometry_continuous_knobs(settings: dict) -> dict:
    """Map continuous D → angle/side/radius bounds and protractor step.

    Returns a shallow copy when ``difficulty`` is set; otherwise unchanged so
    EMH presets and explicit knobs win.
    """
    d = _continuous_d_or_none(settings)
    if d is None:
        return settings
    out = dict(settings)
    if d < 4.0:
        out["angle_min"], out["angle_max"] = 20, 120
        out["side_min"], out["side_max"] = 3, 10
        out["radius_min"], out["radius_max"] = 2, 6
        out["coord_min"], out["coord_max"] = -5, 5
        out["similarity_ratio_min"], out["similarity_ratio_max"] = 2, 3
        out["protractor_step"] = 10
        out["angle_piece_min"], out["angle_piece_max"] = 2, 2
    elif d < 10.0:
        out["angle_min"], out["angle_max"] = 15, 150
        out["side_min"], out["side_max"] = 3, max(12, int(8 + 0.5 * d))
        out["radius_min"], out["radius_max"] = 2, max(8, int(5 + 0.4 * d))
        out["coord_min"], out["coord_max"] = -8, 8
        out["similarity_ratio_min"], out["similarity_ratio_max"] = 2, 4
        out["protractor_step"] = 5
        out["angle_piece_min"], out["angle_piece_max"] = 2, 3
    elif d < 16.0:
        out["angle_min"], out["angle_max"] = 10, 170
        out["side_min"], out["side_max"] = 4, max(18, int(10 + 0.6 * d))
        out["radius_min"], out["radius_max"] = 2, max(12, int(6 + 0.5 * d))
        out["coord_min"], out["coord_max"] = -10, 10
        out["similarity_ratio_min"], out["similarity_ratio_max"] = 2, 5
        out["protractor_step"] = 1
        out["angle_piece_min"], out["angle_piece_max"] = 3, 4
    else:
        side_hi = min(36, int(14 + 0.9 * d))
        rad_hi = min(24, int(8 + 0.7 * d))
        out["angle_min"], out["angle_max"] = 5, 175
        out["side_min"], out["side_max"] = 5, side_hi
        out["radius_min"], out["radius_max"] = 2, rad_hi
        span = min(15, 10 + int((d - 16) // 4))
        out["coord_min"], out["coord_max"] = -span, span
        out["similarity_ratio_min"], out["similarity_ratio_max"] = 2, min(8, 5 + int((d - 16) // 6))
        out["protractor_step"] = 1
        out["angle_piece_min"], out["angle_piece_max"] = 3, min(5, 4 + int((d - 16) // 8))
    return out


def geometry_angle_structure_from_continuous(settings: dict) -> dict | None:
    """Map continuous D → multi-ray angle diagram structure (or None if EMH-only)."""
    d = _continuous_d_or_none(settings)
    if d is None:
        return None
    local = apply_geometry_continuous_knobs(settings)
    piece_lo = int(local.get("angle_piece_min", 2))
    piece_hi = int(local.get("angle_piece_max", 2))
    if d < 4.0:
        modes = ("sum", "sum", "subtract")
        allow_span = False
        allow_crowded = False
        total_cap = 160
    elif d < 10.0:
        modes = ("sum", "subtract", "sum_span")
        allow_span = True
        allow_crowded = False
        total_cap = 165
    elif d < 16.0:
        modes = ("sum_span", "subtract_span", "sum_span", "crowded_sum")
        allow_span = True
        allow_crowded = True
        total_cap = 175
    else:
        modes = ("sum_span", "subtract_span", "crowded_sum", "subtract_span")
        allow_span = True
        allow_crowded = True
        total_cap = 175
    return {
        "difficulty": d,
        "piece_min": piece_lo,
        "piece_max": max(piece_lo, piece_hi),
        "modes": modes,
        "allow_span": allow_span,
        "allow_crowded": allow_crowded,
        "total_cap": total_cap,
        "protractor_step": int(local.get("protractor_step", 1)),
        "angle_min": int(local.get("angle_min", 10)),
        "angle_max": int(local.get("angle_max", 170)),
        "side_min": int(local.get("side_min", 3)),
        "side_max": int(local.get("side_max", 20)),
        "radius_min": int(local.get("radius_min", 2)),
        "radius_max": int(local.get("radius_max", 15)),
    }


def apply_matrix_continuous_knobs(settings: dict) -> dict:
    """Map continuous D → matrix entry magnitude / det constraints."""
    d = _continuous_d_or_none(settings)
    if d is None:
        return settings
    out = dict(settings)
    if d < 4.0:
        out["matrix_entry_min"], out["matrix_entry_max"] = -3, 3
        out["matrix_det_abs_max"] = 4
        out["matrix_scalar_max"] = 4
        out["matrix_point_max"] = 4
    elif d < 10.0:
        out["matrix_entry_min"], out["matrix_entry_max"] = -5, 5
        out["matrix_det_abs_max"] = 6
        out["matrix_scalar_max"] = 6
        out["matrix_point_max"] = 6
    elif d < 16.0:
        out["matrix_entry_min"], out["matrix_entry_max"] = -7, 7
        out["matrix_det_abs_max"] = 9
        out["matrix_scalar_max"] = 8
        out["matrix_point_max"] = 8
    else:
        span = min(12, 7 + int((d - 16) // 4))
        out["matrix_entry_min"], out["matrix_entry_max"] = -span, span
        out["matrix_det_abs_max"] = min(16, 9 + int((d - 16) // 3))
        out["matrix_scalar_max"] = min(12, 8 + int((d - 16) // 4))
        out["matrix_point_max"] = min(12, 8 + int((d - 16) // 4))
    return out


def apply_conic_continuous_knobs(settings: dict) -> dict:
    """Map continuous D → conic center/radius/axis spans and translated forms."""
    d = _continuous_d_or_none(settings)
    if d is None:
        return settings
    out = dict(settings)
    if d < 4.0:
        out["conic_center_min"], out["conic_center_max"] = 0, 0
        out["conic_radius_min"], out["conic_radius_max"] = 2, 4
        out["conic_axis_min"], out["conic_axis_max"] = 2, 5
        out["conic_focus_max"] = 3
        out["conic_allow_translated"] = False
    elif d < 10.0:
        out["conic_center_min"], out["conic_center_max"] = -3, 3
        out["conic_radius_min"], out["conic_radius_max"] = 2, 6
        out["conic_axis_min"], out["conic_axis_max"] = 2, 7
        out["conic_focus_max"] = 4
        out["conic_allow_translated"] = True
    elif d < 16.0:
        out["conic_center_min"], out["conic_center_max"] = -5, 5
        out["conic_radius_min"], out["conic_radius_max"] = 2, 8
        out["conic_axis_min"], out["conic_axis_max"] = 2, 9
        out["conic_focus_max"] = 6
        out["conic_allow_translated"] = True
    else:
        cspan = min(10, 5 + int((d - 16) // 4))
        out["conic_center_min"], out["conic_center_max"] = -cspan, cspan
        out["conic_radius_min"], out["conic_radius_max"] = 2, min(12, 8 + int((d - 16) // 4))
        out["conic_axis_min"], out["conic_axis_max"] = 2, min(14, 9 + int((d - 16) // 3))
        out["conic_focus_max"] = min(10, 6 + int((d - 16) // 4))
        out["conic_allow_translated"] = True
    return out


def apply_graph_transform_continuous_knobs(settings: dict) -> dict:
    """Map continuous D → abs/radical/rational/exp/log graph transform unlocks."""
    d = _continuous_d_or_none(settings)
    if d is None:
        return settings
    out = dict(settings)
    if d < 4.0:
        out["allow_shift_h"] = True
        out["allow_shift_k"] = False
        out["allow_stretch"] = False
        out["allow_reflection"] = False
        out["coef_min"], out["coef_max"] = 1, 1
        out["integer_only"] = True
    elif d < 10.0:
        out["allow_shift_h"] = True
        out["allow_shift_k"] = d >= 6.0
        out["allow_stretch"] = d >= 8.0
        out["allow_reflection"] = False
        out["coef_min"], out["coef_max"] = 1, 2 if d >= 8.0 else 1
        out["integer_only"] = True
    elif d < 16.0:
        out["allow_shift_h"] = True
        out["allow_shift_k"] = True
        out["allow_stretch"] = True
        out["allow_reflection"] = d >= 12.0
        out["coef_min"], out["coef_max"] = 1, 3
        out["integer_only"] = True
    else:
        out["allow_shift_h"] = True
        out["allow_shift_k"] = True
        out["allow_stretch"] = True
        out["allow_reflection"] = True
        out["coef_min"], out["coef_max"] = 1, min(5, 3 + int((d - 16) // 4))
        out["integer_only"] = d < 20.0
    return out


def apply_quadratic_graph_continuous_knobs(settings: dict) -> dict:
    """Map continuous D → quadratic graph form / transform unlocks.

    Mirrors EMH ``quadratic_graph`` presets: clean vertex → standard/factored
    / light messy → fractional stretch + messy rewrite.
    """
    d = _continuous_d_or_none(settings)
    if d is None:
        return settings
    out = dict(settings)
    out["allow_vertex_form"] = True
    out["allow_shift_h"] = True
    out["allow_shift_k"] = True
    if d < 4.0:
        out["allow_standard_form"] = False
        out["allow_factored_form"] = False
        out["allow_messy_form"] = False
        out["allow_stretch"] = False
        out["allow_reflection"] = False
        out["coef_min"], out["coef_max"] = 1, 1
        out["integer_only"] = True
        out["leading_coefficient_one"] = True
        out["monic_only"] = True
        out["coord_min"], out["coord_max"] = -3, 3
        out["intercept_min"], out["intercept_max"] = -3, 3
    elif d < 10.0:
        out["allow_standard_form"] = d >= 5.0
        out["allow_factored_form"] = d >= 7.0
        out["allow_messy_form"] = d >= 8.0
        out["allow_stretch"] = d >= 6.0
        out["allow_reflection"] = d >= 8.0
        out["coef_min"], out["coef_max"] = (-2, 2) if d >= 6.0 else (1, 1)
        out["integer_only"] = True
        out["leading_coefficient_one"] = d < 6.0
        out["monic_only"] = d < 6.0
        out["coord_min"], out["coord_max"] = -5, 5
        out["intercept_min"], out["intercept_max"] = -5, 5
    elif d < 16.0:
        out["allow_standard_form"] = True
        out["allow_factored_form"] = True
        out["allow_messy_form"] = True
        out["allow_stretch"] = True
        out["allow_reflection"] = True
        out["coef_min"], out["coef_max"] = -2, 2
        out["integer_only"] = True
        out["leading_coefficient_one"] = False
        out["monic_only"] = False
        out["coord_min"], out["coord_max"] = -6, 6
        out["intercept_min"], out["intercept_max"] = -6, 6
    else:
        out["allow_standard_form"] = True
        out["allow_factored_form"] = True
        out["allow_messy_form"] = True
        out["allow_stretch"] = True
        out["allow_reflection"] = True
        out["coef_min"], out["coef_max"] = -3, 3
        out["integer_only"] = d < 20.0
        out["leading_coefficient_one"] = False
        out["monic_only"] = False
        out["coord_min"], out["coord_max"] = -8, 8
        out["intercept_min"], out["intercept_max"] = -8, 8
    return out


def apply_growth_decay_continuous_knobs(settings: dict) -> dict:
    """Map continuous D → exponential growth/decay ask-mode and rate/period spans."""
    d = _continuous_d_or_none(settings)
    if d is None:
        return settings
    out = dict(settings)
    out["allow_growth"] = True
    out["allow_decay"] = True
    out["discrete_only"] = True
    if d < 4.0:
        out["ask_mode"] = "find_final"
        out["rate_min"], out["rate_max"] = 5, 10
        out["periods_min"], out["periods_max"] = 2, 4
        out["allow_how_much_more"] = False
        out["allow_compare"] = False
        out["allow_threshold"] = False
        out["allow_half_life"] = False
        out["allow_fractional_periods"] = False
    elif d < 10.0:
        out["ask_mode"] = "mixed"
        out["rate_min"], out["rate_max"] = 5, 20
        out["periods_min"], out["periods_max"] = 3, 6 + int(d // 3)
        out["allow_how_much_more"] = d >= 6.0
        out["allow_compare"] = False
        out["allow_threshold"] = False
        out["allow_half_life"] = False
        out["allow_fractional_periods"] = False
    elif d < 16.0:
        out["ask_mode"] = "mixed"
        out["rate_min"], out["rate_max"] = 3, 25
        out["periods_min"], out["periods_max"] = 4, 10
        out["allow_how_much_more"] = True
        out["allow_compare"] = d >= 12.0
        out["allow_threshold"] = d >= 12.0
        out["allow_half_life"] = d >= 14.0
        out["allow_fractional_periods"] = False
    else:
        out["ask_mode"] = "mixed"
        out["rate_min"], out["rate_max"] = 3, min(40, 25 + int((d - 16) // 2))
        out["periods_min"], out["periods_max"] = 5, min(16, 10 + int((d - 16) // 2))
        out["allow_how_much_more"] = True
        out["allow_compare"] = True
        out["allow_threshold"] = True
        out["allow_half_life"] = True
        out["allow_fractional_periods"] = True
    return out


def apply_inverse_exp_log_continuous_knobs(settings: dict) -> dict:
    """Map continuous D → inverse exp/log base and shift spans."""
    d = _continuous_d_or_none(settings)
    if d is None:
        return settings
    out = dict(settings)
    if d < 4.0:
        out["inv_base_choices"] = (2, 3)
        out["inv_shift_max"] = 0
    elif d < 10.0:
        out["inv_base_choices"] = (2, 3, 5)
        out["inv_shift_max"] = 2
    elif d < 16.0:
        out["inv_base_choices"] = (2, 3, 5, 10)
        out["inv_shift_max"] = 4
    else:
        out["inv_base_choices"] = (2, 3, 5, 10)
        out["inv_shift_max"] = min(8, 4 + int((d - 16) // 3))
    return out


def apply_systems_continuous_knobs(settings: dict) -> dict:
    """Map continuous D → 2/3-var system coefficient and solution spans."""
    d = _continuous_d_or_none(settings)
    if d is None:
        return settings
    out = dict(settings)
    if d < 4.0:
        out["system_coef_min"], out["system_coef_max"] = 1, 3
        out["max_coefficient_magnitude"] = 3
        out["solution_coord_max"] = 3
    elif d < 10.0:
        out["system_coef_min"], out["system_coef_max"] = 1, 5
        out["max_coefficient_magnitude"] = 5
        out["solution_coord_max"] = 5
    elif d < 16.0:
        out["system_coef_min"], out["system_coef_max"] = -6, 6
        out["max_coefficient_magnitude"] = 6
        out["solution_coord_max"] = 6
    else:
        span = min(10, 6 + int((d - 16) // 3))
        out["system_coef_min"], out["system_coef_max"] = -span, span
        out["max_coefficient_magnitude"] = span
        out["solution_coord_max"] = span
    return out


def apply_complex_continuous_knobs(settings: dict) -> dict:
    """Map continuous D → complex entry magnitude / multiply unlock."""
    d = _continuous_d_or_none(settings)
    if d is None:
        return settings
    out = dict(settings)
    if d < 4.0:
        out["complex_entry_min"], out["complex_entry_max"] = -3, 3
        out["complex_prefer_multiply"] = False
    elif d < 10.0:
        out["complex_entry_min"], out["complex_entry_max"] = -5, 5
        out["complex_prefer_multiply"] = d >= 7.0
    elif d < 16.0:
        out["complex_entry_min"], out["complex_entry_max"] = -7, 7
        out["complex_prefer_multiply"] = True
    else:
        span = min(12, 7 + int((d - 16) // 3))
        out["complex_entry_min"], out["complex_entry_max"] = -span, span
        out["complex_prefer_multiply"] = True
    return out


def apply_triangle_laws_continuous_knobs(settings: dict) -> dict:
    """Map continuous D → law-of-sines/cosines side and angle spans."""
    d = _continuous_d_or_none(settings)
    if d is None:
        return settings
    out = dict(settings)
    if d < 4.0:
        out["triangle_side_min"], out["triangle_side_max"] = 5, 12
        out["triangle_angle_choices"] = (30, 45, 60)
        out["allow_obtuse"] = False
    elif d < 10.0:
        out["triangle_side_min"], out["triangle_side_max"] = 5, 18
        out["triangle_angle_choices"] = (30, 40, 45, 50, 60, 70)
        out["allow_obtuse"] = False
    elif d < 16.0:
        out["triangle_side_min"], out["triangle_side_max"] = 5, 22
        out["triangle_angle_choices"] = (30, 40, 45, 50, 60, 70, 80, 100)
        out["allow_obtuse"] = True
    else:
        out["triangle_side_min"], out["triangle_side_max"] = 5, min(30, 22 + int((d - 16) // 2))
        out["triangle_angle_choices"] = (30, 40, 45, 50, 60, 70, 80, 100, 120)
        out["allow_obtuse"] = True
    return out


def apply_variation_continuous_knobs(settings: dict) -> dict:
    """Map continuous D → variation constant span and inverse mix."""
    d = _continuous_d_or_none(settings)
    if d is None:
        return settings
    out = dict(settings)
    if d < 4.0:
        out["variation_constant_min"], out["variation_constant_max"] = 2, 6
        out["direct_variation_weight"], out["inverse_variation_weight"] = 80, 20
    elif d < 10.0:
        out["variation_constant_min"], out["variation_constant_max"] = 2, 12
        out["direct_variation_weight"], out["inverse_variation_weight"] = 55, 45
    elif d < 16.0:
        out["variation_constant_min"], out["variation_constant_max"] = 3, 20
        out["direct_variation_weight"], out["inverse_variation_weight"] = 40, 60
    else:
        out["variation_constant_min"], out["variation_constant_max"] = 4, min(40, 20 + int(d - 16))
        out["direct_variation_weight"], out["inverse_variation_weight"] = 30, 70
    return out


def apply_counting_continuous_knobs(settings: dict) -> dict:
    """Map continuous D → permutation/combination n,r spans."""
    d = _continuous_d_or_none(settings)
    if d is None:
        return settings
    out = dict(settings)
    if d < 4.0:
        out["counting_n_min"], out["counting_n_max"] = 4, 7
        out["counting_r_max"] = 2
    elif d < 10.0:
        out["counting_n_min"], out["counting_n_max"] = 5, 10
        out["counting_r_max"] = 3
    elif d < 16.0:
        out["counting_n_min"], out["counting_n_max"] = 6, 12
        out["counting_r_max"] = 4
    else:
        out["counting_n_min"], out["counting_n_max"] = 7, min(16, 12 + int((d - 16) // 3))
        out["counting_r_max"] = min(6, 4 + int((d - 16) // 4))
    return out


def apply_relations_continuous_knobs(settings: dict) -> dict:
    """Map continuous D → slope/intercept/coord spans and table row count."""
    d = _continuous_d_or_none(settings)
    if d is None:
        return settings
    out = dict(settings)
    if d < 4.0:
        out["slope_min"], out["slope_max"] = -3, 3
        out["intercept_min"], out["intercept_max"] = -4, 4
        out["coord_min"], out["coord_max"] = -5, 5
        out["table_row_count"] = 3
    elif d < 10.0:
        out["slope_min"], out["slope_max"] = -6, 6
        out["intercept_min"], out["intercept_max"] = -8, 8
        out["coord_min"], out["coord_max"] = -8, 8
        out["table_row_count"] = 4 if d >= 7.0 else 3
    elif d < 16.0:
        out["slope_min"], out["slope_max"] = -8, 8
        out["intercept_min"], out["intercept_max"] = -10, 10
        out["coord_min"], out["coord_max"] = -10, 10
        out["table_row_count"] = 5
    else:
        span = min(12, 8 + int((d - 16) // 3))
        out["slope_min"], out["slope_max"] = -span, span
        out["intercept_min"], out["intercept_max"] = -span, span
        out["coord_min"], out["coord_max"] = -span, span
        out["table_row_count"] = min(8, 5 + int((d - 16) // 4))
    return out


def apply_solve_by_graphing_continuous_knobs(settings: dict) -> dict:
    """Map continuous D → solve-by-graphing root/degree/leading unlocks.

    Mirrors EMH ``polynomial_solve_graph`` presets.
    """
    d = _continuous_d_or_none(settings)
    if d is None:
        return settings
    out = dict(settings)
    if d < 4.0:
        out["leading_coefficient_one"] = True
        out["monic_only"] = True
        out["allow_stretch"] = False
        out["allow_reflection"] = False
        out["allow_factored_form"] = False
        out["coef_min"], out["coef_max"] = 1, 1
        out["root_min"], out["root_max"] = -3, 3
        out["min_degree"], out["max_degree"] = 2, 2
        out["integer_only"] = True
        out["coord_min"], out["coord_max"] = -5, 5
    elif d < 10.0:
        out["leading_coefficient_one"] = d < 6.0
        out["monic_only"] = d < 6.0
        out["allow_stretch"] = d >= 6.0
        out["allow_reflection"] = d >= 7.0
        out["allow_factored_form"] = d >= 7.0
        out["coef_min"], out["coef_max"] = (-3, 3) if d >= 6.0 else (1, 1)
        out["root_min"], out["root_max"] = -5, 5
        out["min_degree"], out["max_degree"] = 2, 2
        out["integer_only"] = True
        out["coord_min"], out["coord_max"] = -8, 8
    elif d < 16.0:
        out["leading_coefficient_one"] = False
        out["monic_only"] = False
        out["allow_stretch"] = True
        out["allow_reflection"] = True
        out["allow_factored_form"] = True
        out["coef_min"], out["coef_max"] = -4, 4
        out["root_min"], out["root_max"] = -7, 7
        out["min_degree"], out["max_degree"] = 2, 3 if d >= 12.0 else 2
        out["integer_only"] = True
        out["coord_min"], out["coord_max"] = -10, 10
    else:
        out["leading_coefficient_one"] = False
        out["monic_only"] = False
        out["allow_stretch"] = True
        out["allow_reflection"] = True
        out["allow_factored_form"] = True
        out["coef_min"], out["coef_max"] = -5, 5
        span = min(10, 7 + int((d - 16) // 3))
        out["root_min"], out["root_max"] = -span, span
        out["min_degree"], out["max_degree"] = 2, 3
        out["integer_only"] = True
        out["coord_min"], out["coord_max"] = -span - 2, span + 2
    return out


def apply_polynomial_theory_continuous_knobs(settings: dict) -> dict:
    """Map continuous D → poly theory spans (binomial, Descartes, FTA, …)."""
    d = _continuous_d_or_none(settings)
    if d is None:
        return settings
    out = dict(settings)
    if d < 4.0:
        out["poly_theory_degree_min"], out["poly_theory_degree_max"] = 3, 3
        out["poly_theory_coef_min"], out["poly_theory_coef_max"] = -4, 4
        out["binomial_n_min"], out["binomial_n_max"] = 3, 4
        out["binomial_a_max"] = 2
        out["root_span"] = 3
        out["leading_choices"] = (1, 2)
        out["constant_choices"] = (2, 3, 4)
    elif d < 10.0:
        out["poly_theory_degree_min"], out["poly_theory_degree_max"] = 3, 4
        out["poly_theory_coef_min"], out["poly_theory_coef_max"] = -6, 6
        out["binomial_n_min"], out["binomial_n_max"] = 3, 5
        out["binomial_a_max"] = 3
        out["root_span"] = 5
        out["leading_choices"] = (2, 3, 4)
        out["constant_choices"] = (2, 3, 4, 5, 6)
    elif d < 16.0:
        out["poly_theory_degree_min"], out["poly_theory_degree_max"] = 3, 6
        out["poly_theory_coef_min"], out["poly_theory_coef_max"] = -8, 8
        out["binomial_n_min"], out["binomial_n_max"] = 4, 6
        out["binomial_a_max"] = 4
        out["root_span"] = 6
        out["leading_choices"] = (2, 3, 4, 5, 6)
        out["constant_choices"] = (2, 3, 4, 5, 6, 8, 9, 10)
    else:
        deg_hi = min(8, 6 + int((d - 16) // 4))
        out["poly_theory_degree_min"], out["poly_theory_degree_max"] = 4, deg_hi
        span = min(12, 8 + int((d - 16) // 3))
        out["poly_theory_coef_min"], out["poly_theory_coef_max"] = -span, span
        out["binomial_n_min"], out["binomial_n_max"] = 5, min(8, 6 + int((d - 16) // 4))
        out["binomial_a_max"] = min(6, 4 + int((d - 16) // 4))
        out["root_span"] = min(8, 6 + int((d - 16) // 4))
        out["leading_choices"] = (2, 3, 4, 5, 6)
        out["constant_choices"] = (2, 3, 4, 5, 6, 8, 9, 10, 12)
    return out


def apply_radical_domain_continuous_knobs(settings: dict) -> dict:
    """Map continuous D → radical domain/range shift and stretch spans."""
    d = _continuous_d_or_none(settings)
    if d is None:
        return settings
    out = dict(settings)
    if d < 4.0:
        out["coord_min"], out["coord_max"] = -3, 3
        out["coef_min"], out["coef_max"] = 1, 1
        out["allow_reflection"] = False
    elif d < 10.0:
        out["coord_min"], out["coord_max"] = -5, 5
        out["coef_min"], out["coef_max"] = 1, 2
        out["allow_reflection"] = d >= 7.0
    elif d < 16.0:
        out["coord_min"], out["coord_max"] = -6, 6
        out["coef_min"], out["coef_max"] = 1, 3
        out["allow_reflection"] = True
    else:
        span = min(10, 6 + int((d - 16) // 3))
        out["coord_min"], out["coord_max"] = -span, span
        out["coef_min"], out["coef_max"] = 1, min(5, 3 + int((d - 16) // 4))
        out["allow_reflection"] = True
    return out


def apply_radical_expression_continuous_knobs(settings: dict) -> dict:
    """Map continuous D → add/sub/mul/div radical mode unlocks + coef spans.

    Fills form-flags used by ``basic._radical_*_modes`` so numeric D drives
    structure without relying on EMH preset injection alone.
    """
    d = _continuous_d_or_none(settings)
    if d is None:
        return settings
    out = dict(settings)
    # Add / subtract
    if d < 4.0:
        out["allow_like_radicals"] = True
        out["allow_unsimplified_radicals"] = False
        out["allow_coeff_unsimplified"] = False
        out["coef_min"], out["coef_max"] = 1, 4
        out["min_terms"], out["max_terms"] = 2, 2
    elif d < 10.0:
        out["allow_like_radicals"] = d < 7.0
        out["allow_unsimplified_radicals"] = True
        out["allow_coeff_unsimplified"] = d >= 8.0
        out["coef_min"], out["coef_max"] = 1, 1 if d < 8.0 else 5
        out["min_terms"], out["max_terms"] = 2, 2 if d < 8.0 else 3
    else:
        out["allow_like_radicals"] = False
        out["allow_unsimplified_radicals"] = d < 14.0
        out["allow_coeff_unsimplified"] = True
        out["coef_min"], out["coef_max"] = 1, min(10, 6 + int((d - 10) // 3))
        out["min_terms"] = 3
        out["max_terms"] = min(5, 3 + int((d - 10) // 5))

    # Multiply
    if d < 4.0:
        out["allow_simple_product"] = True
        out["allow_coeff_product"] = False
        out["allow_binomial_product"] = False
    elif d < 10.0:
        out["allow_simple_product"] = d < 6.0
        out["allow_coeff_product"] = True
        out["allow_binomial_product"] = d >= 8.0
    else:
        out["allow_simple_product"] = False
        out["allow_coeff_product"] = d < 14.0
        out["allow_binomial_product"] = True

    # Divide
    if d < 4.0:
        out["allow_reduced_quotients"] = True
        out["allow_simplify_quotients"] = False
        out["allow_rationalize_divide"] = False
    elif d < 10.0:
        out["allow_reduced_quotients"] = d < 6.0
        out["allow_simplify_quotients"] = True
        out["allow_rationalize_divide"] = d >= 8.0
    else:
        out["allow_reduced_quotients"] = False
        out["allow_simplify_quotients"] = d < 14.0
        out["allow_rationalize_divide"] = True
    return out


def complex_fraction_structure_from_continuous(settings: dict) -> dict | None:
    """Map continuous D → complex-fraction builder band + coef span."""
    d = _continuous_d_or_none(settings)
    if d is None:
        return None
    if d < 4.0:
        return {"difficulty": d, "band": "easy", "coef_hi": 5}
    if d < 10.0:
        return {"difficulty": d, "band": "medium", "coef_hi": 6 + int(d // 4)}
    if d < 16.0:
        return {"difficulty": d, "band": "hard", "coef_hi": 8 + int((d - 10) // 3)}
    return {"difficulty": d, "band": "hard", "coef_hi": min(12, 10 + int((d - 16) // 4))}


def compound_interest_structure_from_continuous(settings: dict) -> dict | None:
    """Map continuous D → principal / rate / time / compounding spans."""
    d = _continuous_d_or_none(settings)
    if d is None:
        return None
    if d < 4.0:
        return {
            "difficulty": d,
            "band": "easy",
            "principals": (500, 1000, 1500, 2000),
            "rates": (3, 4, 5, 6, 8),
            "t_min": 2,
            "t_max": 4,
            "n_choices": (1,),
            "allow_interest_question": False,
        }
    if d < 10.0:
        return {
            "difficulty": d,
            "band": "medium",
            "principals": (1000, 1500, 2000, 2500),
            "rates": (3, 4, 5, 6, 8),
            "t_min": 2,
            "t_max": 4 + int(d // 3),
            "n_choices": (1, 2, 4),
            "allow_interest_question": d >= 6.0,
        }
    return {
        "difficulty": d,
        "band": "hard",
        "principals": (1000, 2000, 2500, 5000, 8000),
        "rates": (3, 4, 5, 6, 7, 8, 9, 12),
        "t_min": 4,
        "t_max": min(12, 6 + int((d - 10) // 2)),
        "n_choices": (2, 4, 12) if d >= 14.0 else (1, 2, 4),
        "allow_interest_question": True,
    }

def derivative_rule_structure_from_continuous(settings: dict) -> dict | None:
    """Map continuous D → derivative-rule family unlock + coef spans.

    Returns None when continuous ``difficulty`` is absent so EMH band logic wins.
    Respects settings ``allow_*`` hard gates (topic defaults applied upstream).
    """
    d = _continuous_d_or_none(settings)
    if d is None:
        return None
    from question_engine.frameworks.primitives.derivatives import (
        derivative_rule_structure,
    )

    structure = derivative_rule_structure(settings)
    # Drop non-JSON helper object used by the sampler.
    structure.pop("_allow", None)
    return structure


def calc_topic_structure_from_continuous(settings: dict) -> dict | None:
    """Continuous knobs + family unlock gates for calc topics that used EMH bands.

    Prefer this over ``settings_difficulty_band`` for structure. ``band`` is kept
    only as a coarse metadata label; generators should spend ``difficulty`` via
    unlock flags and numeric knobs.
    """
    d = _continuous_d_or_none(settings)
    if d is None:
        return None
    if d < 4.0:
        band = "easy"
    elif d < 10.0:
        band = "medium"
    else:
        band = "hard"
    return {
        "difficulty": d,
        "band": band,
        "coef_hi": max(3, min(10, 3 + int(d // 3))),
        "power_max": max(2, min(8, 2 + int(d // 4))),
        "n_max": max(2, min(8, 2 + int(d // 3))),
        "k_max": max(2, min(8, 2 + int(d // 4))),
        "interval_width_max": max(2, min(8, 2 + int(d // 4))),
        "bound_max": max(3, min(10, 3 + int(d // 3))),
        "riemann_n_max": max(2, min(8, 2 + int(d // 4))),
        "riemann_L_max": max(4, min(12, 4 + int(d // 3))),
        "table_points": max(3, min(6, 3 + int(d // 6))),
        # Progressive family unlocks (not a 3-way EMH collapse).
        "unlock_medium": d >= 4.0,
        "unlock_hard": d >= 10.0,
        "unlock_advanced": d >= 14.0,
        "unlock_trig": d >= 6.0,
        "unlock_exp": d >= 7.0,
        "unlock_log": d >= 12.0,
        "unlock_roots": d >= 8.0,
        "unlock_reciprocal": d >= 8.0,
        "unlock_quotient_table": d >= 6.0,
        "unlock_compose_table": d >= 12.0,
        "unlock_chain_ftc": d >= 10.0,
        "unlock_ibp_trig": d >= 6.0,
        "unlock_ibp_quad": d >= 12.0,
        "unlock_midpoint_table": d >= 10.0,
        "unlock_sec_csc": d >= 10.0,
        "unlock_base_a_integral": d >= 12.0,
        "unlock_scaled_invtrig": d >= 10.0,
        "unlock_poly_inner_sub": d >= 6.0,
        "unlock_power_inner_sub": d >= 12.0,
    }


def pick_unlocked_families(
    structure: dict,
    easy: list[str],
    medium: list[str] | None = None,
    hard: list[str] | None = None,
    *,
    advanced: list[str] | None = None,
    extra: list[str] | None = None,
) -> list[str]:
    """Accumulate family ids unlocked by continuous structure gates."""
    out = list(easy)
    if structure.get("unlock_medium") and medium:
        out.extend(medium)
    if structure.get("unlock_hard") and hard:
        out.extend(hard)
    if structure.get("unlock_advanced") and advanced:
        out.extend(advanced)
    if extra:
        out.extend(extra)
    return out or list(easy)


def calculus_params_from_settings(settings: dict) -> CalculusParams:
    local = apply_calculus_continuous_knobs(settings)
    coef_min = int(local.get("coef_min", -6))
    coef_max = int(local.get("coef_max", 6))
    power_min = int(local.get("power_min", 1))
    power_max = int(local.get("power_max", 3))
    approach_min = int(local.get("limit_approach_min", -5))
    approach_max = int(local.get("limit_approach_max", 5))
    return CalculusParams(
        coef_min=min(coef_min, coef_max),
        coef_max=max(coef_min, coef_max),
        power_min=min(power_min, power_max),
        power_max=max(power_min, power_max),
        term_count=int(local.get("term_count", 2)),
        include_constant_term=bool(local.get("include_constant_term", True)),
        variable=str(local.get("variable", "x")),
        limit_approach_min=min(approach_min, approach_max),
        limit_approach_max=max(approach_min, approach_max),
        allow_infinity=bool(local.get("allow_infinity", False)),
        require_positive_power=bool(local.get("require_positive_power", True)),
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
