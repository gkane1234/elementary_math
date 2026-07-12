"""Number generator framework — rationals, decimals, percents, ratios, rates."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction
from typing import Any

from .base import QuestionFramework
from ..generators.utils import (
    format_fraction_division_latex,
    format_linear_latex,
    frac_latex,
    frac_or_mixed_latex,
    random_fraction,
    random_int_range,
)
from ..settings.params import allowed_division_notations


@dataclass(frozen=True)
class NumberParams:
    num_min: int = -10
    num_max: int = 10
    denom_min: int = 2
    denom_max: int = 12
    allow_negative: bool = True
    allow_mixed: bool = False
    require_proper: bool = False


def _bounded_int(settings: dict, key: str, default: int) -> int:
    return int(settings.get(key, default))


def _int_range(settings: dict, min_key: str, max_key: str, *, lo_default: int, hi_default: int) -> tuple[int, int]:
    lo = _bounded_int(settings, min_key, lo_default)
    hi = _bounded_int(settings, max_key, hi_default)
    return min(lo, hi), max(lo, hi)


def number_params_from_settings(settings: dict) -> NumberParams:
    from ..settings.enrichment import apply_positive_coefficient_restriction, scaled_int_range

    allow_negative = bool(settings.get("allow_negative", True))
    if bool(settings.get("coefficients_positive_only", False)):
        allow_negative = False
    num_min = int(settings.get("coef_min", settings.get("num_min", -10)))
    num_max = int(settings.get("coef_max", settings.get("num_max", 10)))
    num_min, num_max = scaled_int_range(settings, num_min, num_max)
    num_min, num_max = apply_positive_coefficient_restriction(settings, num_min, num_max)
    if not allow_negative:
        num_min = max(1, num_min)
        num_max = max(num_min, num_max)
    denom_min, denom_max = _int_range(
        settings, "denom_min", "denom_max", lo_default=2, hi_default=12
    )
    return NumberParams(
        num_min=min(num_min, num_max),
        num_max=max(num_min, num_max),
        denom_min=denom_min,
        denom_max=denom_max,
        allow_negative=allow_negative,
        allow_mixed=bool(settings.get("allow_mixed", False)),
        require_proper=bool(settings.get("require_proper", False)),
    )


def _ratio_bounds(settings: dict) -> tuple[int, int]:
    return _int_range(
        settings, "ratio_part_min", "ratio_part_max", lo_default=2, hi_default=15
    )


def _unit_rate_bounds(settings: dict) -> tuple[int, int, int, int]:
    rate_min, rate_max = _int_range(
        settings, "unit_rate_min", "unit_rate_max", lo_default=2, hi_default=12
    )
    mult_min, mult_max = _int_range(
        settings,
        "unit_rate_multiplier_min",
        "unit_rate_multiplier_max",
        lo_default=2,
        hi_default=8,
    )
    return rate_min, rate_max, mult_min, mult_max


def _sci_exp_bounds(settings: dict) -> tuple[int, int]:
    lo, hi = _int_range(settings, "sci_exp_min", "sci_exp_max", lo_default=-8, hi_default=8)
    if not bool(settings.get("allow_negative_exponents", True)):
        lo = max(0, lo)
        hi = max(lo, hi)
    return lo, hi


def _sci_mantissa_decimals(settings: dict) -> int:
    return max(1, min(3, int(settings.get("mantissa_decimals", 1))))


def _random_sci_mantissa(settings: dict) -> float:
    """Return a mantissa in [1, 10) with the configured decimal places."""
    decimals = _sci_mantissa_decimals(settings)
    scale = 10**decimals
    # Integers from 1*scale .. 10*scale - 1 → [1.0, 10.0)
    return random.randint(scale, 10 * scale - 1) / scale


def _normalize_sci(mantissa: float, exponent: int) -> tuple[float, int]:
    if mantissa == 0:
        return 0.0, 0
    sign = 1 if mantissa > 0 else -1
    m = abs(mantissa)
    exp = exponent
    while m >= 10:
        m /= 10
        exp += 1
    while m < 1:
        m *= 10
        exp -= 1
    return sign * m, exp


def _format_sci_latex(mantissa: float, exponent: int) -> str:
    m, exp = _normalize_sci(mantissa, exponent)
    # Round to 6 significant figures to avoid float noise in answers.
    m_dec = Decimal(str(m)).normalize()
    # Quantize relative to magnitude: keep up to 6 significant digits.
    if m_dec == 0:
        return "0 \\times 10^{0}"
    sig = abs(m_dec)
    # Round to 6 significant figures via scientific quantization.
    rounded = float(f"{float(sig):.6g}")
    if m < 0:
        rounded = -rounded
    m_text = f"{rounded:g}"
    return f"{m_text} \\times 10^{{{exp}}}"


def _ordinary_number_latex(mantissa: float, exponent: int) -> str:
    """Plain decimal/integer form (avoids float for large |exponent|)."""
    value = Decimal(str(mantissa)) * (Decimal(10) ** exponent)
    text = format(value.normalize(), "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


def _sci_exp_diff_bounds(settings: dict) -> tuple[int, int]:
    return _int_range(
        settings, "sci_exp_diff_min", "sci_exp_diff_max", lo_default=0, hi_default=0
    )


def _format_decimal(value: Decimal, *, places: int = 2) -> str:
    quantize = Decimal(10) ** -places
    normalized = value.quantize(quantize, rounding=ROUND_HALF_UP).normalize()
    text = format(normalized, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


def _random_decimal(
    *,
    places: int = 1,
    minimum: float = 0.1,
    maximum: float = 99.9,
    allow_negative: bool = False,
) -> Decimal:
    scale = 10**places
    low = int(minimum * scale)
    high = int(maximum * scale)
    value = random.randint(low, high) / scale
    if allow_negative and random.choice([True, False]):
        value = -value
    return Decimal(str(value)).quantize(Decimal(10) ** -places)


class NumberFramework(QuestionFramework):
    """Shared batch generation for numeric expression types."""


class RationalFramework(NumberFramework):
    """Adding/subtracting/multiplying/dividing rational numbers."""

    def __init__(self, operation: str = "+"):
        self.operation = operation

    def _random_fraction(self, params: NumberParams) -> Fraction:
        return random_fraction(
            num_min=params.num_min,
            num_max=params.num_max,
            denom_min=params.denom_min,
            denom_max=params.denom_max,
            allow_negative=params.allow_negative,
            require_proper=params.require_proper,
            allow_mixed=params.allow_mixed,
        )

    def _format_operand(self, value: Fraction, params: NumberParams) -> str:
        # Mixed display only when enabled and the value is improper.
        show_mixed = params.allow_mixed and abs(value.numerator) > value.denominator
        return frac_or_mixed_latex(value, allow_mixed=show_mixed)

    def _resolve_operation(self) -> str:
        if self.operation == "+-":
            return random.choice(["+", "-"])
        return self.operation

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        params = number_params_from_settings(settings)
        a = self._random_fraction(params)
        b = self._random_fraction(params)
        if self.operation == "/":
            while b == 0:
                b = self._random_fraction(params)

        op = self._resolve_operation()
        ops = {
            "+": lambda x, y: x + y,
            "-": lambda x, y: x - y,
            "*": lambda x, y: x * y,
            "/": lambda x, y: x / y,
        }
        result = ops[op](a, b)
        if op == "/":
            notation = random.choice(allowed_division_notations(settings))
            prompt_latex = format_fraction_division_latex(a, b, notation)
        else:
            latex_op = {"+": "+", "-": "-", "*": "\\cdot"}[op]
            prompt_latex = (
                f"{self._format_operand(a, params)} {latex_op} {self._format_operand(b, params)}"
            )
        return prompt_latex, f"{a} {op} {b}", frac_latex(result)


class PercentFramework(NumberFramework):
    """Percent-of, find-percent, and percent-change prompts."""

    def __init__(self, *, percent_change: bool = False):
        self.percent_change = percent_change

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        from ..settings.enrichment import format_answer_value

        pct_lo, pct_hi = _int_range(
            settings, "percent_min", "percent_max", lo_default=5, hi_default=75
        )
        base_lo, base_hi = _int_range(
            settings, "base_min", "base_max", lo_default=10, hi_default=200
        )
        round_whole = bool(settings.get("round_to_whole", settings.get("round_answers_to_whole", False)))
        allow_decimal_pct = bool(settings.get("allow_decimal_percents", False))

        if self.percent_change:
            original = random.randint(base_lo, base_hi)
            if allow_decimal_pct:
                percent = round(random.uniform(pct_lo, pct_hi), 1)
            else:
                percent = random.randint(pct_lo, pct_hi)
            increased = random.choice([True, False])
            change = round(original * percent / 100)
            if change == 0:
                change = random.randint(5, min(40, base_hi // 4 or 5))
            new_value = original + change if increased else original - change
            actual_pct = abs(change) / original * 100
            if round_whole:
                actual_pct = round(actual_pct)
            direction = "increase" if increased else "decrease"
            prompt = f"\\text{{From {original} to {new_value}, find the percent {direction}.}}"
            answer_value = format_answer_value(
                {**settings, "round_answers_to_whole": round_whole},
                actual_pct,
            )
            return prompt, f"From {original} to {new_value}", f"{answer_value}\\%"

        mode = random.choice(["percent_of", "find_percent", "find_whole"])
        if allow_decimal_pct:
            percent = round(random.uniform(pct_lo, pct_hi), 1)
        else:
            percent = random.randint(pct_lo, pct_hi)
        if mode == "percent_of":
            base = random.randint(base_lo, base_hi)
            result = percent * base / 100
            if round_whole:
                result = round(result)
            prompt = f"\\text{{What is {percent}\\% of {base}?}}"
            answer = format_answer_value({**settings, "round_answers_to_whole": round_whole}, result)
            return prompt, f"What is {percent}% of {base}?", answer

        if mode == "find_percent":
            whole = random.randint(base_lo, base_hi)
            part = whole * percent // 100 if not allow_decimal_pct else round(whole * percent / 100, 1)
            if part == 0:
                part = max(1, percent // 10)
            prompt = f"\\text{{{part} is what percent of {whole}?}}"
            pct_answer = format_answer_value(
                {**settings, "round_answers_to_whole": round_whole},
                percent,
            )
            return prompt, f"{part} is what percent of {whole}?", f"{pct_answer}\\%"

        part = random.randint(max(1, base_lo // 10), min(60, base_hi // 3 or 60))
        result = part * 100 / percent
        if round_whole:
            result = round(result)
        prompt = f"\\text{{{part} is {percent}\\% of what number?}}"
        answer = format_answer_value({**settings, "round_answers_to_whole": round_whole}, result)
        return prompt, f"{part} is {percent}% of what number?", answer


class RatioFramework(NumberFramework):
    """Introduction to ratios and equivalent-ratio prompts."""

    def __init__(self, *, equivalent: bool = False):
        self.equivalent = equivalent

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        part_lo, part_hi = _ratio_bounds(settings)
        if self.equivalent:
            a = random.randint(part_lo, part_hi)
            b = random.randint(part_lo, part_hi)
            factor = random.randint(2, 5)
            c = a * factor
            missing = b * factor
            form = random.choice(["colon", "fraction"])
            if form == "colon":
                prompt = f"\\text{{Find the missing value: }} {a}:{b} = {c}:x"
                answer = str(missing)
            else:
                prompt = f"\\frac{{{a}}}{{{b}}} = \\frac{{{c}}}{{x}}"
                answer = str(missing)
            return prompt, f"{a}:{b} = {c}:x", answer

        a = random.randint(part_lo, part_hi)
        b = random.randint(part_lo, part_hi)
        context = random.choice(["marbles", "apples", "books", "stickers"])
        color_a = random.choice(["red", "blue", "green"])
        color_b = random.choice(["yellow", "orange", "purple"])
        while color_b == color_a:
            color_b = random.choice(["yellow", "orange", "purple"])
        form = random.choice(["word", "fraction"])
        if form == "word":
            prompt = (
                f"\\text{{There are {a} {color_a} {context} and {b} {color_b} {context}. "
                f"Write the ratio of {color_a} to {color_b}.}}"
            )
            answer = f"{a}:{b}"
        else:
            prompt = f"\\text{{Write the ratio }} {a}:{b} \\text{{ as a fraction in simplest form.}}"
            g = Fraction(a, b)
            answer = frac_latex(g)
        return prompt, f"ratio {a} to {b}", answer


class UnitRateFramework(NumberFramework):
    """Unit rate word problems."""

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        rate_lo, rate_hi, mult_lo, mult_hi = _unit_rate_bounds(settings)
        kind = random.choice(["speed", "reading rate", "unit price"])
        rate = random.randint(rate_lo, rate_hi)
        multiplier = random.randint(mult_lo, mult_hi)

        if kind == "unit price":
            pounds = multiplier
            total_cost = rate * pounds
            prompt = (
                f"\\text{{\\${total_cost} for {pounds} pounds of fruit. "
                f"Find the unit price in dollars per pound.}}"
            )
            return prompt, "unit price", f"\\${rate}"

        scenarios = {
            "speed": ("miles", "hours", "A car travels"),
            "reading rate": ("pages", "minutes", "A student reads"),
        }
        quantity, unit, subject = scenarios[kind]
        total = rate * multiplier
        unit_singular = unit[:-1] if unit.endswith("s") else unit
        prompt = (
            f"\\text{{{subject} {total} {quantity} in {multiplier} {unit}. "
            f"Find the unit rate in {quantity} per {unit_singular}.}}"
        )
        return prompt, f"unit rate ({kind})", str(rate)


def _terminating_decimal_places(frac: Fraction) -> int | None:
    """Places needed for an exact decimal, or None if the decimal repeats."""
    denom = frac.denominator
    twos = fives = 0
    while denom % 2 == 0:
        denom //= 2
        twos += 1
    while denom % 5 == 0:
        denom //= 5
        fives += 1
    if denom != 1:
        return None
    return max(twos, fives)


def _exact_terminating_decimal(frac: Fraction) -> str:
    """Format a terminating fraction as an exact decimal string (no rounding)."""
    places = _terminating_decimal_places(frac)
    if places is None:
        raise ValueError(f"non-terminating fraction: {frac}")
    if places == 0:
        return str(frac.numerator // frac.denominator)
    quantized = (Decimal(frac.numerator) / Decimal(frac.denominator)).quantize(
        Decimal(10) ** -places
    )
    text = format(quantized, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text


class DecimalArithmeticFramework(NumberFramework):
    """Decimal addition, subtraction, multiplication, and division."""

    def __init__(self, operation: str = "+"):
        self.operation = operation

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        places = int(settings.get("decimal_places", 2))
        allow_negative = bool(settings.get("allow_negative", False))
        minimum = 0.1 if not allow_negative else -99.9
        a_places = places
        b_places = places
        a = _random_decimal(places=places, minimum=minimum, maximum=99.9, allow_negative=allow_negative)
        b = _random_decimal(places=places, minimum=minimum, maximum=99.9, allow_negative=allow_negative)
        if self.operation == "-":
            if not allow_negative:
                while b > a:
                    b = _random_decimal(places=places, minimum=0.1, maximum=float(a))
            elif random.choice([True, False]):
                while b > a:
                    a, b = b, a
        if self.operation == "*":
            a, b, a_places, b_places = self._multiplication_factors(settings)
        if self.operation == "/":
            divisor = random.randint(2, 9)
            quotient = _random_decimal(places=places, minimum=0.5, maximum=9.5)
            a = (quotient * Decimal(divisor)).quantize(Decimal(10) ** -places)
            b = Decimal(divisor)
            b_places = 0

        ops = {
            "+": lambda x, y: x + y,
            "-": lambda x, y: x - y,
            "*": lambda x, y: x * y,
            "/": lambda x, y: x / y,
        }
        result = ops[self.operation](a, b)
        latex_op = {"+": "+", "-": "-", "*": "\\cdot", "/": "\\div"}[self.operation]
        answer_places = a_places + b_places if self.operation == "*" else places
        prompt_latex = (
            f"{_format_decimal(a, places=a_places)} {latex_op} {_format_decimal(b, places=b_places)}"
        )
        return prompt_latex, f"{a} {self.operation} {b}", _format_decimal(result, places=answer_places)

    def _multiplication_factors(
        self, settings: dict
    ) -> tuple[Decimal, Decimal, int, int]:
        """Build multiplication factors shaped by difficulty settings.

        - whole_times_decimal: whole number × decimal (tenths when decimal_places=1)
        - otherwise both factors are decimals with 1..max_decimal_places places
        """
        places = max(1, int(settings.get("decimal_places", 2)))
        max_places = max(1, int(settings.get("max_decimal_places", places)))
        allow_negative = bool(settings.get("allow_negative", False))
        whole_times = bool(settings.get("whole_times_decimal", False))

        def fractional_decimal(factor_places: int) -> Decimal:
            while True:
                value = _random_decimal(
                    places=factor_places,
                    minimum=0.1,
                    maximum=9.9,
                    allow_negative=False,
                )
                if value != value.to_integral_value():
                    if allow_negative and random.choice([True, False]):
                        value = -value
                    return value

        if whole_times:
            whole = Decimal(random.randint(2, 20))
            decimal_places = min(places, max_places)
            # Tenths-only easy items look like 7 × 0.3, not 17 × 7.5.
            while True:
                decimal = _random_decimal(
                    places=decimal_places,
                    minimum=0.1,
                    maximum=0.9 if decimal_places == 1 else 9.9,
                    allow_negative=False,
                )
                if decimal != decimal.to_integral_value():
                    break
            if allow_negative and random.choice([True, False]):
                whole = -whole
            # Prefer whole × decimal (matches grade-6 presentation).
            return whole, decimal, 0, decimal_places

        a_places = random.randint(1, max_places)
        b_places = random.randint(1, max_places)
        return fractional_decimal(a_places), fractional_decimal(b_places), a_places, b_places


class WholeDivideToDecimalFramework(NumberFramework):
    """Whole ÷ whole with a terminating non-integer decimal quotient."""

    _DIVISORS_BY_PLACES: dict[int, tuple[int, ...]] = {
        1: (2, 4, 5, 10),
        2: (4, 5, 8, 10, 16, 20, 25, 40, 50),
        3: (8, 16, 20, 25, 40, 50, 80, 100, 125, 200),
    }

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        places = max(1, min(3, int(settings.get("decimal_places", 2))))
        max_places = settings.get("max_decimal_places")
        if max_places is not None:
            places = max(1, min(places, int(max_places)))
        num_max = max(4, int(settings.get("num_max", 50)))
        dividend_hi = max(num_max, 10)
        divisors = [d for d in self._DIVISORS_BY_PLACES[places] if d <= max(num_max, 10)]
        if not divisors:
            divisors = list(self._DIVISORS_BY_PLACES[places])

        # Prefer quotients that use the full place budget on harder tiers.
        prefer_exact_places = places >= 2

        for _ in range(120):
            divisor = random.choice(divisors)
            dividend = random.randint(1, dividend_hi)
            if dividend % divisor == 0:
                continue
            frac = Fraction(dividend, divisor)
            needed = _terminating_decimal_places(frac)
            if needed is None or needed < 1 or needed > places:
                continue
            if prefer_exact_places and needed < places and random.random() < 0.65:
                continue
            answer = _exact_terminating_decimal(frac)
            prompt_latex = f"{dividend} \\div {divisor}"
            return prompt_latex, f"{dividend} / {divisor}", answer

        # Guaranteed terminating fallbacks by place budget.
        fallbacks = {1: (5, 2), 2: (7, 4), 3: (3, 8)}
        dividend, divisor = fallbacks[places]
        answer = _exact_terminating_decimal(Fraction(dividend, divisor))
        return f"{dividend} \\div {divisor}", f"{dividend} / {divisor}", answer


class DistributiveFramework(NumberFramework):
    """Numeric and simple algebraic distributive property."""

    def __init__(self, *, algebraic: bool = False):
        self.algebraic = algebraic

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        allow_negative = bool(settings.get("allow_negative", True))
        coef_lo = int(settings.get("coef_min", -9))
        coef_hi = int(settings.get("coef_max", 9))
        if not allow_negative:
            coef_lo = max(1, coef_lo)
            coef_hi = max(coef_lo, coef_hi)
        outer = random_int_range(min(coef_lo, coef_hi), max(coef_lo, coef_hi), exclude={0})
        inner_a = random.randint(1, 9)
        inner_b = random.randint(1, 9)
        op = random.choice(["+", "-"])

        if self.algebraic:
            inner = f"x {op} {inner_b}" if op == "+" else f"x - {inner_b}"
            prompt_latex = f"{outer}({inner})"
            if op == "+":
                answer = format_linear_latex(outer, outer * inner_b)
            else:
                answer = format_linear_latex(outer, -outer * inner_b)
            return prompt_latex, prompt_latex, answer

        result = outer * (inner_a + inner_b) if op == "+" else outer * (inner_a - inner_b)
        prompt_latex = f"{outer}({inner_a} {op} {inner_b})"
        return prompt_latex, prompt_latex, str(result)


class OrderOfOperationsFramework(NumberFramework):
    """Evaluate numeric expressions using order of operations."""

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        complexity = str(settings.get("pemdas_complexity", "mixed"))
        lo, hi = _int_range(settings, "num_min", "num_max", lo_default=2, hi_default=9)
        patterns = {
            "basic": ["pemdas_basic"],
            "parentheses": ["parentheses"],
            "exponent": ["exponent"],
            "mixed": ["pemdas_basic", "parentheses", "exponent"],
        }
        pattern = random.choice(patterns.get(complexity, patterns["mixed"]))
        if pattern == "pemdas_basic":
            a = random.randint(lo, hi)
            b = random.randint(lo, hi)
            c = random.randint(lo, hi)
            d = random.randint(lo, min(hi, 6))
            prompt = f"{a} + {b} \\cdot {c} - {d}"
            answer = str(a + b * c - d)
        elif pattern == "parentheses":
            a = random.randint(lo, hi)
            b = random.randint(lo, hi)
            c = random.randint(lo, min(hi, 6))
            prompt = f"({a} + {b}) \\cdot {c}"
            answer = str((a + b) * c)
        else:
            base = random.randint(lo, min(hi, 5))
            exp = random.randint(2, 3)
            addend = random.randint(lo, hi)
            prompt = f"{base}^{{{exp}}} + {addend}"
            answer = str(base**exp + addend)
        return prompt, "order of operations", answer


class ProportionFramework(NumberFramework):
    """Solve proportions for an unknown."""

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        part_lo, part_hi = _ratio_bounds(settings)
        x = random.randint(part_lo, part_hi)
        a = random.randint(part_lo, min(part_hi, 9))
        b = random.randint(part_lo, min(part_hi, 9))
        c = x * b // a
        while c * a != x * b or c == 0:
            x = random.randint(part_lo, part_hi)
            a = random.randint(part_lo, min(part_hi, 9))
            b = random.randint(part_lo, min(part_hi, 9))
            c = x * b // a
        form = random.choice(["x_numerator", "x_denominator"])
        if form == "x_numerator":
            prompt = f"\\frac{{x}}{{{b}}} = \\frac{{{c}}}{{{a}}}"
        else:
            prompt = f"\\frac{{{a}}}{{{b}}} = \\frac{{x}}{{{c}}}"
        return prompt, f"{a}/{b} = x/{c}", str(x)


class ScientificNotationFramework(NumberFramework):
    """Write and operate with numbers in scientific notation."""

    def __init__(self, *, mode: str = "write"):
        self.mode = mode

    def _random_sci_pair(self, settings: dict) -> tuple[float, int]:
        exp_lo, exp_hi = _sci_exp_bounds(settings)
        exponent = random.randint(exp_lo, exp_hi)
        return _random_sci_mantissa(settings), exponent

    def _pick_operation(self, settings: dict) -> str:
        mode = str(settings.get("sci_operation", "mixed")).strip().lower()
        if mode == "multiply":
            return "\\times"
        if mode == "divide":
            return "\\div"
        return random.choice(["\\times", "\\div"])

    def _ops_pair(
        self, settings: dict, *, op: str, require_norm: bool
    ) -> tuple[float, int, float, int]:
        a, a_exp = self._random_sci_pair(settings)
        b, b_exp = self._random_sci_pair(settings)
        if not require_norm:
            return a, a_exp, b, b_exp

        decimals = _sci_mantissa_decimals(settings)
        scale = 10**decimals
        if op == "\\times":
            # Force product mantissa ≥ 10 so the result needs renormalization.
            lo = max(scale, 5 * scale)
            a = random.randint(lo, 10 * scale - 1) / scale
            b = random.randint(lo, 10 * scale - 1) / scale
        else:
            # Force quotient mantissa < 1 so the result needs renormalization.
            b = random.randint(5 * scale, 10 * scale - 1) / scale
            a_hi = min(4 * scale, int(b * scale) - 1)
            a = random.randint(scale, max(scale, a_hi)) / scale
        return a, a_exp, b, b_exp

    def _write_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        direction = str(settings.get("sci_write_direction", "to_sci")).strip().lower()
        allow_compare = bool(settings.get("allow_magnitude_compare", False))
        if direction == "compare" or (allow_compare and random.random() < 0.35):
            return self._compare_prompt(settings)

        if direction == "both":
            direction = random.choice(["to_sci", "from_sci"])

        mantissa, exponent = self._random_sci_pair(settings)
        sci = _format_sci_latex(mantissa, exponent)
        ordinary = _ordinary_number_latex(mantissa, exponent)

        if direction == "from_sci":
            prompt = f"\\text{{Write in standard form: }} {sci}"
            return prompt, f"standard form of {sci}", ordinary

        prompt = f"\\text{{Write in scientific notation: }} {ordinary}"
        return prompt, f"scientific notation of {ordinary}", sci

    def _compare_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        a, a_exp = self._random_sci_pair(settings)
        b, b_exp = self._random_sci_pair(settings)
        # Ensure distinct magnitudes.
        for _ in range(20):
            if (a, a_exp) != (b, b_exp):
                break
            b, b_exp = self._random_sci_pair(settings)
        a_m, a_e = _normalize_sci(a, a_exp)
        b_m, b_e = _normalize_sci(b, b_exp)
        if a_e > b_e or (a_e == b_e and a_m >= b_m):
            larger = "first"
        else:
            larger = "second"
        prompt = (
            f"\\text{{Which is greater? }} "
            f"{_format_sci_latex(a, a_exp)} \\text{{ or }} {_format_sci_latex(b, b_exp)}"
        )
        answer = (
            _format_sci_latex(a, a_exp)
            if larger == "first"
            else _format_sci_latex(b, b_exp)
        )
        return prompt, "compare scientific notation", answer

    def _operations_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        op = self._pick_operation(settings)
        require_norm = bool(settings.get("require_normalization", False))
        a, a_exp, b, b_exp = self._ops_pair(settings, op=op, require_norm=require_norm)
        a_dec, b_dec = Decimal(str(a)), Decimal(str(b))
        if op == "\\times":
            raw_m = float(a_dec * b_dec)
            result_m, result_e = _normalize_sci(raw_m, a_exp + b_exp)
        else:
            raw_m = float(a_dec / b_dec)
            result_m, result_e = _normalize_sci(raw_m, a_exp - b_exp)
        prompt = (
            f"({a:g} \\times 10^{{{a_exp}}}) {op} "
            f"({b:g} \\times 10^{{{b_exp}}})"
        )
        return prompt, "scientific notation operation", _format_sci_latex(result_m, result_e)

    def _add_subtract_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        exp_lo, exp_hi = _sci_exp_bounds(settings)
        diff_lo, diff_hi = _sci_exp_diff_bounds(settings)
        diff = random.randint(diff_lo, diff_hi)

        # Keep both exponents inside the configured range when possible.
        if diff == 0:
            exp_a = random.randint(exp_lo, exp_hi)
            exp_b = exp_a
        else:
            max_start = exp_hi
            min_start = exp_lo + diff
            if min_start > max_start:
                exp_a = exp_hi
                exp_b = exp_hi - diff
            else:
                exp_a = random.randint(min_start, max_start)
                exp_b = exp_a - diff

        a = _random_sci_mantissa(settings)
        b = _random_sci_mantissa(settings)
        op = random.choice(["+", "-"])

        a_dec, b_dec = Decimal(str(a)), Decimal(str(b))
        if exp_a >= exp_b:
            aligned_a = a_dec
            aligned_b = b_dec / (Decimal(10) ** (exp_a - exp_b))
            base_exp = exp_a
        else:
            aligned_a = a_dec / (Decimal(10) ** (exp_b - exp_a))
            aligned_b = b_dec
            base_exp = exp_b

        combined = aligned_a + aligned_b if op == "+" else aligned_a - aligned_b
        if combined == 0:
            op = "+"
            combined = aligned_a + aligned_b

        result_m, result_e = _normalize_sci(float(combined), base_exp)
        # Same-exponent hard items: nudge so the sum needs renormalization.
        if (
            bool(settings.get("require_normalization", False))
            and diff == 0
            and abs(float(combined)) < 10
        ):
            a = random.randint(55, 99) / 10
            b = random.randint(55, 99) / 10
            combined_f = a + b if op == "+" else a - b
            if abs(combined_f) < 1:
                op = "+"
                combined_f = a + b
            result_m, result_e = _normalize_sci(combined_f, base_exp)

        prompt = (
            f"({a:g} \\times 10^{{{exp_a}}}) {op} "
            f"({b:g} \\times 10^{{{exp_b}}})"
        )
        return prompt, "scientific notation add/subtract", _format_sci_latex(result_m, result_e)

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        if self.mode == "write":
            return self._write_prompt(settings)
        if self.mode == "operations":
            return self._operations_prompt(settings)
        return self._add_subtract_prompt(settings)


def _int_bounds(settings: dict, *, lo_default: int = -20, hi_default: int = 20) -> tuple[int, int]:
    return _int_range(settings, "num_min", "num_max", lo_default=lo_default, hi_default=hi_default)


def _factor_bounds(settings: dict) -> tuple[int, int]:
    return _int_range(settings, "factor_min", "factor_max", lo_default=4, hi_default=60)


def _require_gcf_greater_than_one(settings: dict) -> bool:
    return bool(settings.get("require_gcf_greater_than_one", True))


def _sample_values_for_gcf(lo: int, hi: int, count: int, *, require_gt_one: bool) -> list[int]:
    """Sample ``count`` integers in [lo, hi]; optionally force GCF ≥ 2."""
    lo = max(2, lo)
    hi = max(lo, hi)
    if not require_gt_one:
        values: list[int] = []
        while len(values) < count:
            candidate = random.randint(lo, hi)
            if candidate > 1:
                values.append(candidate)
        return values

    max_g = max(2, min(hi // 2, 12))
    for _ in range(40):
        g = random.randint(2, max_g)
        mult_hi = hi // g
        mult_lo = max(1, (lo + g - 1) // g)
        if mult_lo > mult_hi:
            continue
        values = [g * random.randint(mult_lo, mult_hi) for _ in range(count)]
        if math.gcd(*values) >= 2:
            return values

    g = 2
    mult_hi = max(2, hi // g)
    mult_lo = max(1, (lo + g - 1) // g)
    if mult_lo > mult_hi:
        mult_lo = 1
    return [g * random.randint(mult_lo, mult_hi) for _ in range(count)]


def _sample_gcf_pair(lo: int, hi: int, *, require_gt_one: bool) -> tuple[int, int, int]:
    """Return (a, b, gcf) with optional GCF ≥ 2 constraint."""
    lo = max(2, lo)
    hi = max(lo, hi)
    g_lo = 2 if require_gt_one else 1
    max_g = max(g_lo, min(hi // 2, 12))
    for _ in range(40):
        g = random.randint(g_lo, max_g)
        mult_hi = hi // g
        mult_lo = max(1, (lo + g - 1) // g)
        if mult_lo > mult_hi:
            continue
        m1 = random.randint(mult_lo, mult_hi)
        m2 = random.randint(mult_lo, mult_hi)
        # Keep multipliers coprime so the GCF of the pair is exactly g.
        if math.gcd(m1, m2) != 1:
            continue
        a, b = g * m1, g * m2
        if a == b:
            continue
        return a, b, g
    # Fallback pair that always shares factor 2 when required.
    if require_gt_one:
        return 12, 18, 6
    return 8, 15, 1


class IntegerArithmeticFramework(NumberFramework):
    """Integer addition, subtraction, multiplication, and division."""

    def __init__(self, operation: str = "+-"):
        self.operation = operation

    def _resolve_operation(self) -> str:
        if self.operation == "+-":
            return random.choice(["+", "-"])
        return self.operation

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        lo, hi = _int_bounds(settings)
        allow_negative = bool(settings.get("allow_negative", True))
        if not allow_negative:
            lo = max(1, lo)
            hi = max(lo, hi)

        op = self._resolve_operation()
        a = random.randint(lo, hi)
        b = random.randint(lo, hi)
        if op == "/":
            while b == 0:
                b = random.randint(lo, hi)
            if not allow_negative and a % b != 0:
                a = b * random.randint(max(1, lo // max(abs(b), 1) or 1), max(1, hi // max(abs(b), 1)))
        elif op == "-" and not allow_negative and b > a:
            a, b = b, a
        elif op == "*":
            if not allow_negative:
                a = abs(a) or random.randint(1, hi)
                b = abs(b) or random.randint(1, hi)

        ops = {
            "+": lambda x, y: x + y,
            "-": lambda x, y: x - y,
            "*": lambda x, y: x * y,
            "/": lambda x, y: x // y,
        }
        result = ops[op](a, b)
        latex_op = {"+": "+", "-": "-", "*": "\\cdot", "/": "\\div"}[op]
        prompt_latex = f"{a} {latex_op} {b}"
        return prompt_latex, f"{a} {op} {b}", str(result)


class LongDivisionWithRemaindersFramework(NumberFramework):
    """Whole-number long division with a nonzero remainder."""

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        dividend_min = max(1, int(settings.get("dividend_min", 10)))
        dividend_max = max(dividend_min, int(settings.get("dividend_max", 99)))
        divisor_min = max(2, int(settings.get("divisor_min", 2)))
        divisor_max = max(divisor_min, int(settings.get("divisor_max", 9)))

        dividend = dividend_min
        divisor = divisor_min
        quotient = 0
        remainder = 1
        for _ in range(60):
            divisor = random.randint(divisor_min, divisor_max)
            if divisor < 2:
                continue
            rem = random.randint(1, divisor - 1)
            max_q = (dividend_max - rem) // divisor
            min_q = max(1, (dividend_min - rem + divisor - 1) // divisor)
            if min_q > max_q or max_q < 1:
                continue
            quotient = random.randint(min_q, max_q)
            dividend = quotient * divisor + rem
            if dividend_min <= dividend <= dividend_max:
                remainder = rem
                break
        else:
            # Deterministic fallback within easy-scale bounds.
            divisor = min(divisor_max, max(divisor_min, 3))
            remainder = 1
            quotient = max(1, dividend_min // divisor)
            dividend = quotient * divisor + remainder
            if dividend > dividend_max:
                quotient = max(1, (dividend_max - remainder) // divisor)
                dividend = quotient * divisor + remainder

        prompt_latex = f"{dividend} \\div {divisor}"
        answer = f"{quotient} \\text{{ R }} {remainder}"
        return prompt_latex, f"{dividend} ÷ {divisor}", answer


class LikeDenominatorFractionFramework(NumberFramework):
    """Add or subtract fractions with a common denominator."""

    def __init__(self, operation: str = "+-"):
        self.operation = operation

    def _resolve_operation(self) -> str:
        if self.operation == "+-":
            return random.choice(["+", "-"])
        return self.operation

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        params = number_params_from_settings(settings)
        op = self._resolve_operation()
        denominator = random.randint(params.denom_min, params.denom_max)
        lo = max(1, params.num_min) if not params.allow_negative else params.num_min
        hi = params.num_max
        n1 = random.randint(lo, hi)
        n2 = random.randint(lo, hi)
        while n1 == 0 or n2 == 0:
            n1 = random.randint(lo, hi)
            n2 = random.randint(lo, hi)
        if op == "-" and not params.allow_negative and n2 > n1:
            n1, n2 = n2, n1

        a = Fraction(n1, denominator)
        b = Fraction(n2, denominator)
        result = a + b if op == "+" else a - b
        latex_op = "+" if op == "+" else "-"
        prompt_latex = f"{frac_latex(a)} {latex_op} {frac_latex(b)}"
        return prompt_latex, f"{a} {op} {b}", frac_latex(result)


class UnlikeDenominatorFractionFramework(NumberFramework):
    """Add or subtract fractions with unlike denominators."""

    def __init__(self, operation: str = "+-"):
        self.operation = operation

    def _resolve_operation(self) -> str:
        if self.operation == "+-":
            return random.choice(["+", "-"])
        return self.operation

    def _random_unlike_pair(self, params: NumberParams) -> tuple[Fraction, Fraction]:
        a = random_fraction(
            num_min=params.num_min,
            num_max=params.num_max,
            denom_min=params.denom_min,
            denom_max=params.denom_max,
            allow_negative=params.allow_negative,
        )
        b = random_fraction(
            num_min=params.num_min,
            num_max=params.num_max,
            denom_min=params.denom_min,
            denom_max=params.denom_max,
            allow_negative=params.allow_negative,
        )
        while a.denominator == b.denominator:
            b = random_fraction(
                num_min=params.num_min,
                num_max=params.num_max,
                denom_min=params.denom_min,
                denom_max=params.denom_max,
                allow_negative=params.allow_negative,
            )
        return a, b

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        params = number_params_from_settings(settings)
        op = self._resolve_operation()
        a, b = self._random_unlike_pair(params)
        if op == "-" and not params.allow_negative and a < b:
            a, b = b, a
        result = a + b if op == "+" else a - b
        latex_op = "+" if op == "+" else "-"
        prompt_latex = f"{frac_latex(a)} {latex_op} {frac_latex(b)}"
        return prompt_latex, f"{a} {op} {b}", frac_latex(result)


class FractionDivideWordFramework(NumberFramework):
    """Fraction division word problems (how many groups, how much per group).

    Tier shape is driven by presets:
      - dividend_form / divisor_form: ``whole`` | ``fraction`` | ``any``
      - require_whole_quotient / require_non_whole_quotient
    """

    def __init__(self, *, mode: str = "groups"):
        self.mode = mode

    def _format_value(self, value: Fraction, params: NumberParams) -> str:
        show_mixed = params.allow_mixed and abs(value.numerator) > value.denominator
        return frac_or_mixed_latex(value, allow_mixed=show_mixed)

    def _sample_whole(self, params: NumberParams, *, lo: int = 2, hi: int | None = None) -> Fraction:
        upper = hi if hi is not None else max(lo, min(24, abs(params.num_max) or 12))
        upper = max(lo, upper)
        return Fraction(random.randint(lo, upper))

    def _sample_non_whole(self, params: NumberParams) -> Fraction:
        return random_fraction(
            num_min=max(1, params.num_min),
            num_max=max(3, abs(params.num_max) or 12),
            denom_min=params.denom_min,
            denom_max=min(12, max(params.denom_min + 1, params.denom_max)),
            allow_negative=False,
            require_proper=params.require_proper,
            allow_mixed=params.allow_mixed,
        )

    def _sample_operand(self, form: str, params: NumberParams) -> Fraction:
        kind = (form or "fraction").strip().lower()
        if kind == "whole":
            return self._sample_whole(params)
        if kind == "any":
            if random.random() < 0.5:
                return self._sample_whole(params)
            return self._sample_non_whole(params)
        return self._sample_non_whole(params)

    def _pair_for_tier(self, settings: dict, params: NumberParams) -> tuple[Fraction, Fraction]:
        """Return (dividend, divisor) matching preset operand / quotient constraints."""
        dividend_form = str(settings.get("dividend_form", "fraction")).strip().lower()
        divisor_form = str(settings.get("divisor_form", "fraction")).strip().lower()
        require_whole_q = bool(settings.get("require_whole_quotient", False))
        require_non_whole_q = bool(settings.get("require_non_whole_quotient", False))

        # Easy: whole ÷ whole with whole quotient (constructively).
        if dividend_form == "whole" and divisor_form == "whole" and require_whole_q:
            divisor_n = random.randint(2, 6)
            quotient_n = random.randint(2, 8)
            return Fraction(divisor_n * quotient_n), Fraction(divisor_n)

        for _ in range(80):
            # Medium: whole dividend; divisor whole (non-int quot) or fraction.
            if dividend_form == "whole" and divisor_form in {"any", "fraction", "mixed"}:
                if divisor_form == "fraction" or (
                    divisor_form in {"any", "mixed"} and random.random() < 0.55
                ):
                    divisor = self._sample_non_whole(params)
                    # Prefer a modest whole quotient so the dividend stays whole.
                    if require_non_whole_q and random.random() < 0.45:
                        quot = Fraction(random.randint(1, 5), random.randint(2, 4))
                        while quot.denominator == 1:
                            quot = Fraction(random.randint(1, 5), random.randint(2, 4))
                    else:
                        quot = Fraction(random.randint(2, 8))
                    dividend = divisor * quot
                    if dividend.denominator != 1 or dividend <= 0:
                        continue
                    dividend = Fraction(dividend.numerator)
                else:
                    divisor_n = random.randint(2, 9)
                    dividend_n = random.randint(divisor_n + 1, max(divisor_n + 2, 24))
                    while dividend_n % divisor_n == 0:
                        dividend_n = random.randint(divisor_n + 1, max(divisor_n + 2, 24))
                    dividend = Fraction(dividend_n)
                    divisor = Fraction(divisor_n)
            elif dividend_form == "fraction" and divisor_form == "fraction":
                # Build from a modest quotient so hard stays grade-6 friendly.
                divisor = self._sample_non_whole(params)
                if self.mode == "groups" or random.random() < 0.55:
                    quot = Fraction(random.randint(2, 6))
                else:
                    quot = Fraction(random.randint(1, 5), random.randint(2, 5))
                    while quot.denominator == 1:
                        quot = Fraction(random.randint(1, 5), random.randint(2, 5))
                dividend = divisor * quot
                if dividend.denominator == 1:
                    continue
            else:
                dividend = self._sample_operand(dividend_form, params)
                divisor = self._sample_operand(divisor_form, params)

            if divisor == 0 or dividend <= 0 or divisor <= 0:
                continue
            if dividend_form == "whole" and dividend.denominator != 1:
                continue
            if dividend_form == "fraction" and dividend.denominator == 1:
                continue
            if divisor_form == "whole" and divisor.denominator != 1:
                continue
            if divisor_form == "fraction" and divisor.denominator == 1:
                continue

            quot = dividend / divisor
            if require_whole_q and quot.denominator != 1:
                continue
            if require_non_whole_q and quot.denominator == 1 and divisor.denominator == 1:
                # Whole ÷ fraction with whole quot is allowed on medium; only reject
                # whole÷whole that accidentally lands on a whole answer.
                continue
            return dividend, divisor

        # Deterministic fallbacks by intended shape.
        if dividend_form == "whole" and divisor_form == "whole":
            return Fraction(10), Fraction(4)
        if dividend_form == "whole":
            return Fraction(6), Fraction(1, 2)
        return Fraction(5, 6), Fraction(2, 3)

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        params = number_params_from_settings(settings)
        if self.mode == "whole":
            dividend = self._sample_operand(
                str(settings.get("dividend_form", "fraction")), params
            )
            portion = Fraction(1, 2)
            prompt = (
                f"\\text{{What fraction of a whole is }} {self._format_value(portion, params)} "
                f"\\text{{ of }} {self._format_value(dividend, params)}\\text{{?}}"
            )
            return prompt, "fraction of a whole", self._format_value(portion * dividend, params)

        dividend, divisor = self._pair_for_tier(settings, params)
        answer = dividend / divisor
        if self.mode == "groups":
            prompt = (
                f"\\text{{How many groups of }} {self._format_value(divisor, params)} "
                f"\\text{{ are in }} {self._format_value(dividend, params)}\\text{{?}}"
            )
        else:
            # Partitive / per-time: whole group counts keep the classic wording;
            # fractional "groups" use a per-period framing that still asks ÷.
            if divisor.denominator == 1:
                prompt = (
                    f"\\text{{If }} {self._format_value(dividend, params)} "
                    f"\\text{{ is shared equally into }} {self._format_value(divisor, params)} "
                    f"\\text{{ groups, how much is in each group?}}"
                )
            else:
                prompt = (
                    f"\\text{{If }} {self._format_value(dividend, params)} "
                    f"\\text{{ is used in }} {self._format_value(divisor, params)} "
                    f"\\text{{ of a period, how much is used in one full period?}}"
                )
        return prompt, f"fraction division ({self.mode})", self._format_value(answer, params)


class GcfLcmFramework(NumberFramework):
    """Greatest common factor and least common multiple."""

    def __init__(self, *, mode: str = "gcf"):
        self.mode = mode

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        lo, hi = _factor_bounds(settings)
        count = random.choice([2, 2, 3])
        if self.mode == "gcf":
            values = _sample_values_for_gcf(
                lo,
                hi,
                count,
                require_gt_one=_require_gcf_greater_than_one(settings),
            )
            result = math.gcd(*values)
            label = "GCF"
        else:
            values = []
            while len(values) < count:
                candidate = random.randint(lo, hi)
                if candidate > 1:
                    values.append(candidate)
            result = math.lcm(*values)
            label = "LCM"
        numbers = ", ".join(str(v) for v in values)
        prompt = f"\\text{{Find the {label} of }} {numbers}"
        return prompt, f"{label} of {numbers}", str(result)


class GcfLcmWordFramework(NumberFramework):
    """GCF/LCM word problems."""

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        lo, hi = _factor_bounds(settings)
        use_gcf = random.choice([True, False])
        if use_gcf:
            a, b, g = _sample_gcf_pair(
                lo,
                hi,
                require_gt_one=_require_gcf_greater_than_one(settings),
            )
            items = random.choice(["apples", "cookies", "stickers"])
            prompt = (
                f"\\text{{You have {a} {items} and {b} {items}. "
                f"What is the greatest number of identical bags you can make?}}"
            )
            return prompt, "GCF word problem", str(g)
        a = random.randint(lo, hi)
        b = random.randint(lo, hi)
        lcm_val = math.lcm(a, b)
        event = random.choice(["bell", "alarm", "timer"])
        prompt = (
            f"\\text{{Event A happens every {a} minutes and Event B every {b} minutes. "
            f"After how many minutes do they happen together?}}"
        )
        return prompt, "LCM word problem", str(lcm_val)


_SMALL_PRIMES: tuple[int, ...] = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47)


def _prime_factorization_latex(n: int) -> str:
    factors: dict[int, int] = {}
    d = 2
    value = n
    while d * d <= value:
        while value % d == 0:
            factors[d] = factors.get(d, 0) + 1
            value //= d
        d += 1
    if value > 1:
        factors[value] = factors.get(value, 0) + 1
    parts = []
    for prime in sorted(factors):
        exp = factors[prime]
        if exp == 1:
            parts.append(str(prime))
        else:
            parts.append(f"{prime}^{{{exp}}}")
    return " \\cdot ".join(parts)


def _count_prime_factors(n: int) -> int:
    """Total number of prime factors counting multiplicity."""
    count = 0
    value = n
    d = 2
    while d * d <= value:
        while value % d == 0:
            count += 1
            value //= d
        d += 1
    if value > 1:
        count += 1
    return count


def _sample_prime_product(settings: dict) -> int:
    """Build a composite from prime factors honoring count / size presets."""
    count_min, count_max = _int_range(
        settings, "prime_factor_count_min", "prime_factor_count_max", lo_default=2, hi_default=4
    )
    prime_max = max(3, int(settings.get("prime_max", 13)))
    product_max = max(6, int(settings.get("factor_product_max", settings.get("factor_max", 999))))
    primes = [p for p in _SMALL_PRIMES if p <= prime_max]
    if len(primes) < 2:
        primes = [2, 3, 5, 7]

    for _ in range(80):
        count = random.randint(count_min, count_max)
        factors = [random.choice(primes) for _ in range(count)]
        product = 1
        for p in factors:
            if product > product_max // p:
                product = 0
                break
            product *= p
        if product < 4 or product > product_max:
            continue
        if _count_prime_factors(product) < count_min:
            continue
        return product

    # Deterministic fallback: two distinct small primes under the product cap.
    for a in primes:
        for b in primes:
            if a * b <= product_max and a * b >= 4:
                return a * b
    return 6


class PrimeFactorizationFramework(NumberFramework):
    """Prime factorization of a composite whole number."""

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        # Prefer factor-count presets when present; otherwise fall back to range sampling.
        if "prime_factor_count_min" in settings or "prime_factor_count_max" in settings:
            n = _sample_prime_product(settings)
        else:
            lo, hi = _factor_bounds(settings)
            lo = max(lo, 4)
            n = random.randint(lo, hi)
            while n < 4 or _count_prime_factors(n) < 2:
                n = random.randint(lo, hi)
        prompt = f"\\text{{Write the prime factorization of }} {n}"
        return prompt, f"prime factorization of {n}", _prime_factorization_latex(n)


class DivisibilityFramework(NumberFramework):
    """Divisibility rules for 2, 3, 4, 5, 6, 9, and 10."""

    _RULES: dict[int, str] = {
        2: "2",
        3: "3",
        4: "4",
        5: "5",
        6: "6",
        9: "9",
        10: "10",
    }

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        lo, hi = _factor_bounds(settings)
        divisor = random.choice(list(self._RULES))
        if random.choice([True, False]):
            base = random.randint(lo, hi)
            if base % divisor == 0:
                n = base
            else:
                n = base + (divisor - base % divisor) % divisor
                if n == base:
                    n = base + divisor
        else:
            base = random.randint(lo, hi)
            n = base if base % divisor != 0 else base + 1
        divisible = n % divisor == 0
        prompt = f"\\text{{Is }} {n} \\text{{ divisible by {divisor}?}}"
        answer = "\\text{Yes}" if divisible else "\\text{No}"
        return prompt, f"divisible by {divisor}?", answer


class AbsoluteValueFramework(NumberFramework):
    """Evaluate, compare, or order absolute values."""

    def __init__(self, *, mode: str = "evaluate"):
        self.mode = mode

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        lo, hi = _int_bounds(settings, lo_default=-15, hi_default=15)
        if self.mode == "evaluate":
            n = random.randint(lo, hi)
            prompt = f"\\left| {n} \\right|"
            return prompt, f"|{n}|", str(abs(n))

        values = [random.randint(lo, hi) for _ in range(3 if self.mode == "order" else 2)]
        while len({abs(v) for v in values}) < len(values):
            values = [random.randint(lo, hi) for _ in range(len(values))]

        if self.mode == "compare":
            a, b = values
            prompt = f"\\left| {a} \\right| \\; ? \\; \\left| {b} \\right|"
            if abs(a) > abs(b):
                answer = ">"
            elif abs(a) < abs(b):
                answer = "<"
            else:
                answer = "="
            return prompt, f"|{a}| vs |{b}|", answer

        ordered = sorted(values, key=abs)
        labels = ", ".join(str(v) for v in values)
        prompt = (
            f"\\text{{Order from least to greatest absolute value: }} "
            f"{labels.replace(', ', ', ')}"
        )
        answer = ", ".join(str(v) for v in ordered)
        return prompt, "order by absolute value", answer


class OppositeFramework(NumberFramework):
    """Find the opposite of an integer."""

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        lo, hi = _int_bounds(settings, lo_default=-20, hi_default=20)
        n = random.randint(lo, hi)
        while n == 0:
            n = random.randint(lo, hi)
        prompt = f"\\text{{Find the opposite of }} {n}"
        return prompt, f"opposite of {n}", str(-n)


class CompareOrderFramework(NumberFramework):
    """Compare or order integers, fractions, and decimals."""

    def __init__(self, *, mode: str = "compare"):
        self.mode = mode

    def _random_value(self, settings: dict) -> tuple[str, float]:
        kind = random.choice(["int", "frac", "decimal"])
        lo, hi = _int_bounds(settings, lo_default=-10, hi_default=10)
        if kind == "int":
            v = random.randint(lo, hi)
            return str(v), float(v)
        if kind == "frac":
            params = number_params_from_settings(settings)
            frac = random_fraction(
                num_min=max(1, lo) if lo > 0 else params.num_min,
                num_max=hi,
                denom_min=params.denom_min,
                denom_max=params.denom_max,
                allow_negative=params.allow_negative,
            )
            return frac_latex(frac), float(frac)
        places = int(settings.get("decimal_places", 2))
        dec = _random_decimal(places=places, minimum=0.1, maximum=9.9, allow_negative=True)
        return _format_decimal(dec, places=places), float(dec)

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        if self.mode == "compare":
            latex_a, val_a = self._random_value(settings)
            latex_b, val_b = self._random_value(settings)
            while val_a == val_b:
                latex_b, val_b = self._random_value(settings)
            prompt = f"{latex_a} \\; ? \\; {latex_b}"
            if val_a > val_b:
                answer = ">"
            elif val_a < val_b:
                answer = "<"
            else:
                answer = "="
            return prompt, "compare numbers", answer

        count = 3
        entries: list[tuple[str, float]] = []
        while len(entries) < count:
            latex, val = self._random_value(settings)
            if not any(abs(val - e[1]) < 1e-9 for e in entries):
                entries.append((latex, val))
        ordered = sorted(entries, key=lambda e: e[1])
        labels = ", ".join(e[0] for e in entries)
        prompt = f"\\text{{Order from least to greatest: }} {labels}"
        answer = ", ".join(e[0] for e in ordered)
        return prompt, "order numbers", answer


class FractionDecimalConvertFramework(NumberFramework):
    """Convert between fractions and decimals."""

    def __init__(self, *, to_decimal: bool | None = None):
        self.to_decimal = to_decimal

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        params = number_params_from_settings(settings)
        denom = random.choice([2, 4, 5, 8, 10, 20, 25, 50, 100])
        num = random.randint(1, denom - 1)
        while math.gcd(num, denom) != 1:
            num = random.randint(1, denom - 1)
        frac = Fraction(num, denom)
        to_decimal = self.to_decimal if self.to_decimal is not None else random.choice([True, False])
        if to_decimal:
            prompt = f"\\text{{Write }} {frac_latex(frac)} \\text{{ as a decimal.}}"
            answer = _format_decimal(Decimal(frac.numerator) / Decimal(frac.denominator), places=3)
        else:
            dec = Decimal(frac.numerator) / Decimal(frac.denominator)
            prompt = f"\\text{{Write }} {_format_decimal(dec, places=3)} \\text{{ as a fraction.}}"
            answer = frac_latex(frac)
        return prompt, "fraction-decimal conversion", answer


class Grade6VisualFramework(NumberFramework):
    """Grade 6 measurement and visual-model prompts with rendered SVG figures."""

    def __init__(self, mode: str):
        self.mode = mode
        self._metadata: dict[str, object] = {}

    @staticmethod
    def _positive_fraction() -> Fraction:
        denominator = random.choice([2, 3, 4, 5, 6, 8])
        numerator = random.randint(1, denominator * 2 - 1)
        return Fraction(numerator, denominator)

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        from ..diagrams.charts import dot_plot_svg, histogram_svg
        from ..diagrams.grade6_figures import (
            area_model_svg,
            cube_net_svg,
            grid_polygon_svg,
            hanger_svg,
            prism_svg,
            rectangle_measure_svg,
            triangle_measure_svg,
        )

        unit = random.choice(["cm", "in"])
        if self.mode in {"fraction_rectangle", "fraction_triangle", "fraction_prism"}:
            a, b = self._positive_fraction(), self._positive_fraction()
            if self.mode == "fraction_prism":
                c = self._positive_fraction()
                volume = a * b * c
                self._metadata = {
                    "diagram_svg": prism_svg(
                        f"{a} {unit}", f"{b} {unit}", f"{c} {unit}"
                    )
                }
                return (
                    f"\\text{{Find the volume of the right rectangular prism with side lengths }} "
                    f"{frac_latex(a)}{unit},\\ {frac_latex(b)}{unit},\\ {frac_latex(c)}{unit}.",
                    f"Volume of prism with sides {a}, {b}, and {c} {unit}",
                    f"{frac_latex(volume)}\\ {unit}^3",
                )
            area = a * b if self.mode == "fraction_rectangle" else a * b / 2
            shape = "rectangle" if self.mode == "fraction_rectangle" else "right triangle"
            figure = (
                rectangle_measure_svg(f"{a} {unit}", f"{b} {unit}")
                if self.mode == "fraction_rectangle"
                else triangle_measure_svg(f"{a} {unit}", f"{b} {unit}")
            )
            self._metadata = {"diagram_svg": figure}
            return (
                f"\\text{{Find the area of the {shape} with base }} {frac_latex(a)}{unit} "
                f"\\text{{ and height }} {frac_latex(b)}{unit}.",
                f"Area of {shape}: base {a} {unit}, height {b} {unit}",
                f"{frac_latex(area)}\\ {unit}^2",
            )

        if self.mode in {"tape", "hanger", "inequality_hanger"}:
            inequality = self.mode == "inequality_hanger"
            if self.mode == "tape":
                return self._build_tape_diagram(settings)

            parts = random.randint(2, 5)
            solution = random.randint(2, 12)
            total = parts * solution
            self._metadata = {
                "diagram_svg": hanger_svg(parts, total, inequality=inequality)
            }
            relation = "\\le" if inequality else "="
            answer_relation = "\\le" if inequality else "="
            return (
                f"\\text{{Use the diagram to solve }} {parts}x {relation} {total}.",
                f"Solve {parts}x {'<=' if inequality else '='} {total}",
                f"x {answer_relation} {solution}" if inequality else str(solution),
            )

        if self.mode == "area_model_algebraic":
            outer = random.randint(2, 8)
            constant = random.randint(2, 9)
            self._metadata = {"diagram_svg": area_model_svg(str(outer), "x", str(constant))}
            return (
                f"\\text{{Use the area model to expand }} {outer}(x + {constant}).",
                f"Expand {outer}(x + {constant})",
                f"{format_linear_latex(outer, outer * constant)}",
            )

        if self.mode in {"grid_polygon", "shaded_polygon"}:
            width, height = random.randint(2, 5), random.randint(2, 4)
            points = [(1, 1), (1 + width, 1), (1 + width, 1 + height), (1, 1 + height)]
            area = width * height
            self._metadata = {"diagram_svg": grid_polygon_svg(points, shaded=self.mode == "shaded_polygon")}
            noun = "shaded region" if self.mode == "shaded_polygon" else "polygon"
            return (
                f"\\text{{Find the area of the {noun} on the grid.}}",
                f"Area of the {noun} on the grid",
                f"{area}\\text{{ square units}}",
            )

        if self.mode in {"nets", "net_surface", "net_grid", "invalid_net"}:
            invalid = self.mode == "invalid_net"
            side = random.randint(2, 8)
            self._metadata = {"diagram_svg": cube_net_svg(side, invalid=invalid)}
            if self.mode == "invalid_net":
                return (
                    "\\text{Does this arrangement form a valid net for a cube?}",
                    "Is this a valid cube net?",
                    "\\text{No}",
                )
            if self.mode == "nets":
                return (
                    "\\text{This net folds to make what solid?}",
                    "Identify the solid made by this net",
                    "\\text{cube}",
                )
            return (
                f"\\text{{The net is for a cube with edge length }} {side}\\text{{ units. Find its surface area.}}",
                f"Surface area of cube net with edge {side}",
                f"{6 * side * side}\\text{{ square units}}",
            )

        if self.mode in {"isometric", "isometric_measure"}:
            length, width, height = (random.randint(2, 5) for _ in range(3))
            self._metadata = {"diagram_svg": prism_svg(str(length), str(width), str(height))}
            if self.mode == "isometric":
                return (
                    "\\text{Sketch/copy the rectangular prism shown in the isometric drawing.}",
                    "Sketch the rectangular prism shown",
                    None,
                )
            volume = length * width * height
            surface = 2 * (length * width + length * height + width * height)
            ask_volume = random.choice([True, False])
            return (
                f"\\text{{Use the drawing to find the {'volume' if ask_volume else 'surface area'}.}}",
                "Measure the rectangular prism shown",
                f"{volume}\\text{{ cubic units}}" if ask_volume else f"{surface}\\text{{ square units}}",
            )

        if self.mode == "classify_polyhedron":
            self._metadata = {"diagram_svg": prism_svg("4", "3", "2")}
            return (
                "\\text{Classify the polyhedron shown.}",
                "Classify the polyhedron",
                "\\text{rectangular prism}",
            )

        if self.mode in {"draw_dot_plot", "draw_histogram"}:
            values = [random.randint(1, 12) for _ in range(random.randint(6, 10))]
            listed = ",\\ ".join(str(v) for v in values)
            if self.mode == "draw_dot_plot":
                self._metadata = {"diagram_svg": dot_plot_svg(values, title="Dot plot to copy")}
                label = "dot plot"
            else:
                lo, hi = min(values), max(values)
                bins = [(float(i), float(i + 2)) for i in range(lo - lo % 2, hi + 2, 2)]
                self._metadata = {"diagram_svg": histogram_svg(values, bins, title="Histogram to copy")}
                label = "histogram"
            return (
                f"\\text{{Sketch/copy the {label} for the data set }} \\{{{listed}\\}}.",
                f"Draw a {label} for {values}",
                None,
            )
        raise ValueError(f"Unknown Grade 6 visual mode: {self.mode}")

    def _build_tape_diagram(self, settings: dict) -> tuple[str, str, str | None]:
        """Uniform equal-x boxes or non-uniform segments with one missing piece."""
        from ..diagrams.grade6_figures import tape_svg

        tier = str(
            settings.get("difficulty_tier") or settings.get("difficulty") or "medium"
        ).strip().lower()
        forced = str(settings.get("tape_style") or "").strip().lower()
        if forced in {"uniform", "nonuniform"}:
            style = forced
        elif forced == "mixed" or tier == "medium":
            style = random.choice(["uniform", "nonuniform"])
        elif tier == "easy":
            style = "uniform"
        elif tier == "hard":
            style = "nonuniform"
        else:
            style = random.choice(["uniform", "nonuniform"])

        if style == "uniform":
            if tier == "easy":
                parts = random.randint(2, 3)
                solution = random.randint(2, 8)
            elif tier == "hard":
                parts = random.randint(3, 6)
                solution = random.randint(4, 15)
            else:
                parts = random.randint(2, 5)
                solution = random.randint(2, 12)
            total = parts * solution
            self._metadata = {
                "diagram_svg": tape_svg(
                    labels=["x"] * parts,
                    total=total,
                    weights=[1.0] * parts,
                    title="Equal-size parts",
                )
            }
            return (
                f"\\text{{Use the tape diagram to find }} x.",
                f"Solve {parts}x = {total}",
                str(solution),
            )

        # Non-uniform: known sizes inside segments, one missing piece.
        if tier == "hard":
            n_segs = random.randint(3, 5)
            value_lo, value_hi = 4, 28
        else:
            n_segs = random.randint(3, 4)
            value_lo, value_hi = 2, 16

        values = [random.randint(value_lo, value_hi) for _ in range(n_segs)]
        # Keep segments visibly distinct so proportional widths read clearly.
        for i in range(1, n_segs):
            while values[i] == values[i - 1]:
                values[i] = random.randint(value_lo, value_hi)
        missing_i = random.randrange(n_segs)
        missing = values[missing_i]
        total = sum(values)
        labels = ["?" if i == missing_i else str(v) for i, v in enumerate(values)]
        self._metadata = {
            "diagram_svg": tape_svg(
                labels=labels,
                total=total,
                weights=[float(v) for v in values],
                title="Find the missing part",
            )
        }
        return (
            "\\text{Use the tape diagram to find the missing value.}",
            f"Missing part in tape totaling {total}",
            str(missing),
        )

    def build_question_metadata(
        self, settings: dict, *, prompt_latex: str, prompt_text: str, answer: str | None
    ) -> dict[str, object]:
        return dict(self._metadata)


# ---------------------------------------------------------------------------
# Sets of numbers (natural / whole / integer / rational / irrational / real)
# ---------------------------------------------------------------------------

_SET_ORDER = ("natural", "whole", "integer", "rational", "irrational", "real")

_SET_DISPLAY = {
    "natural": "natural",
    "whole": "whole",
    "integer": "integer",
    "rational": "rational",
    "irrational": "irrational",
    "real": "real",
}

_IRRATIONAL_POOL: tuple[tuple[str, str], ...] = (
    (r"\sqrt{2}", "√2"),
    (r"\sqrt{3}", "√3"),
    (r"\sqrt{5}", "√5"),
    (r"\sqrt{7}", "√7"),
    (r"\sqrt{11}", "√11"),
    (r"\pi", "π"),
    (r"2\pi", "2π"),
    (r"\frac{\pi}{2}", "π/2"),
    (r"e", "e"),
    (r"\sqrt[3]{2}", "∛2"),
    (r"1 + \sqrt{2}", "1 + √2"),
    (r"-\sqrt{2}", "-√2"),
)


@dataclass(frozen=True)
class _NumberExample:
    """A concrete number plus its most-specific kind."""

    latex: str
    text: str
    # Most specific: natural | whole | integer | rational | irrational
    kind: str


def _enabled_sets(settings: dict) -> list[str]:
    enabled = [
        name
        for name in _SET_ORDER
        if bool(settings.get(f"include_{name}", True))
    ]
    if not enabled:
        return ["integer", "rational", "real"]
    return enabled


def _membership(example: _NumberExample, set_name: str) -> bool:
    kind = example.kind
    if set_name == "natural":
        return kind == "natural"
    if set_name == "whole":
        return kind in {"natural", "whole"}
    if set_name == "integer":
        return kind in {"natural", "whole", "integer"}
    if set_name == "rational":
        return kind != "irrational"
    if set_name == "irrational":
        return kind == "irrational"
    if set_name == "real":
        return True
    return False


def _sets_for_example(example: _NumberExample, enabled: list[str]) -> list[str]:
    return [name for name in enabled if _membership(example, name)]


def _format_set_list(names: list[str]) -> str:
    labels = [_SET_DISPLAY[n] for n in names]
    if not labels:
        return r"\text{(none)}"
    return r"\text{" + ", ".join(labels) + "}"


def _make_natural(settings: dict) -> _NumberExample:
    lo, hi = _int_bounds(settings)
    lo = max(1, lo)
    hi = max(lo, hi)
    n = random.randint(lo, hi)
    return _NumberExample(str(n), str(n), "natural")


def _make_whole(settings: dict) -> _NumberExample:
    if random.random() < 0.4:
        return _NumberExample("0", "0", "whole")
    return _make_natural(settings)


def _make_integer(settings: dict) -> _NumberExample:
    lo, hi = _int_bounds(settings)
    allow_negative = bool(settings.get("allow_negative", True))
    if allow_negative and lo < 0:
        # Prefer a non-whole integer so classification is interesting.
        n = random.randint(min(lo, -1), -1)
        return _NumberExample(str(n), str(n), "integer")
    # Fall back to a whole number if negatives are off.
    return _make_whole(settings)


def _make_rational(settings: dict) -> _NumberExample:
    allow_negative = bool(settings.get("allow_negative", True))
    if bool(settings.get("allow_fractions", True)) and random.random() < 0.65:
        frac = random_fraction(
            num_min=-9 if allow_negative else 1,
            num_max=9,
            denom_min=2,
            denom_max=9,
            allow_negative=allow_negative,
        )
        # Ensure non-integer.
        while frac.denominator == 1:
            frac = random_fraction(
                num_min=-9 if allow_negative else 1,
                num_max=9,
                denom_min=2,
                denom_max=9,
                allow_negative=allow_negative,
            )
        return _NumberExample(frac_latex(frac), str(frac), "rational")

    # Terminating / repeating decimal that is rational but not an integer.
    tenths = random.randint(1, 9)
    sign = -1 if allow_negative and random.random() < 0.35 else 1
    whole = random.randint(0, 8)
    value = sign * (whole + tenths / 10)
    text = f"{value:g}"
    if "." not in text:
        text = f"{value:.1f}"
    latex = text
    return _NumberExample(latex, text, "rational")


def _make_irrational(settings: dict) -> _NumberExample:
    allow_negative = bool(settings.get("allow_negative", True))
    pool = list(_IRRATIONAL_POOL)
    if not allow_negative:
        pool = [(latex, text) for latex, text in pool if not latex.startswith("-")]
    latex, text = random.choice(pool)
    return _NumberExample(latex, text, "irrational")


def _example_factories(settings: dict) -> list[tuple[str, Any]]:
    """Return (kind, factory) pairs that settings currently allow."""
    factories: list[tuple[str, Any]] = [
        ("natural", lambda: _make_natural(settings)),
        ("whole", lambda: _make_whole(settings)),
        ("integer", lambda: _make_integer(settings)),
    ]
    if bool(settings.get("allow_fractions", True)):
        factories.append(("rational", lambda: _make_rational(settings)))
    if bool(settings.get("allow_irrationals", True)) and bool(
        settings.get("include_irrational", True)
    ):
        factories.append(("irrational", lambda: _make_irrational(settings)))
    return factories


def _random_example(settings: dict, *, prefer_kind: str | None = None) -> _NumberExample:
    factories = _example_factories(settings)
    if prefer_kind:
        matched = [f for kind, f in factories if kind == prefer_kind]
        if matched:
            return matched[0]()
    return random.choice(factories)[1]()


def _resolve_ask_mode(settings: dict) -> str:
    mode = str(settings.get("ask_mode", "mixed")).strip().lower()
    if mode == "mixed":
        return random.choice(["classify", "pick", "membership"])
    if mode in {"classify", "pick", "membership"}:
        return mode
    return "classify"


class SetsOfNumbersFramework(NumberFramework):
    """Classify numbers into standard number sets."""

    instruction_latex = r"\text{To which set(s) of numbers does each number belong?}"
    instruction_text = "To which set(s) of numbers does each number belong?"

    def __init__(self) -> None:
        self._last_distractors: list[str] = []

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        self._last_distractors = []
        mode = _resolve_ask_mode(settings)
        enabled = _enabled_sets(settings)

        if mode == "pick":
            return self._build_pick(settings, enabled)
        if mode == "membership":
            return self._build_membership(settings, enabled)
        return self._build_classify(settings, enabled)

    def _build_classify(
        self, settings: dict, enabled: list[str]
    ) -> tuple[str, str, str | None]:
        example = _random_example(settings)
        belonging = _sets_for_example(example, enabled)
        answer = _format_set_list(belonging)
        # Distractors: other plausible set-list answers.
        distractors: list[str] = []
        for _ in range(8):
            other = _random_example(settings)
            other_sets = _format_set_list(_sets_for_example(other, enabled))
            if other_sets != answer and other_sets not in distractors:
                distractors.append(other_sets)
            if len(distractors) >= 3:
                break
        self._last_distractors = distractors
        prompt_latex = example.latex
        prompt_text = f"Classify {example.text}"
        return prompt_latex, prompt_text, answer

    def _build_pick(
        self, settings: dict, enabled: list[str]
    ) -> tuple[str, str, str | None]:
        allow_fractions = bool(settings.get("allow_fractions", True))
        allow_irrationals = bool(settings.get("allow_irrationals", True)) and bool(
            settings.get("include_irrational", True)
        )
        allow_negative = bool(settings.get("allow_negative", True))

        # Only ask about sets where we can also generate clear counterexamples.
        candidates: list[str] = []
        if "irrational" in enabled and allow_irrationals:
            candidates.append("irrational")
        if "natural" in enabled and (allow_negative or allow_fractions or allow_irrationals):
            # Counterexamples: 0, negatives, fractions, irrationals.
            candidates.append("natural")
        if "whole" in enabled and (allow_negative or allow_fractions or allow_irrationals):
            candidates.append("whole")
        if "integer" in enabled and (allow_fractions or allow_irrationals):
            candidates.append("integer")
        if "rational" in enabled and allow_irrationals:
            # Without irrationals every generated value is rational.
            candidates.append("rational")
        if not candidates:
            # Fall back to classify-style when pick cannot produce contrast.
            return self._build_classify(settings, enabled)

        target_set = random.choice(candidates)

        if target_set == "irrational":
            target = _make_irrational(settings)
        elif target_set == "natural":
            target = _make_natural(settings)
        elif target_set == "whole":
            target = _make_whole(settings)
        elif target_set == "integer":
            target = _make_integer(settings)
        else:
            target = _make_rational(settings)

        options = [target]
        for _ in range(60):
            if len(options) >= 4:
                break
            candidate = _random_example(settings)
            if _membership(candidate, target_set):
                continue
            if any(c.latex == candidate.latex for c in options):
                continue
            options.append(candidate)

        # Guaranteed counterexamples if the random pool was unlucky.
        fallbacks: list[_NumberExample] = []
        if target_set == "irrational":
            fallbacks = [_make_natural(settings), _make_integer(settings), _make_rational(settings)]
        elif target_set == "rational":
            fallbacks = [_make_irrational(settings)] * 3
        elif target_set == "integer":
            if allow_fractions:
                fallbacks.append(_make_rational(settings))
            if allow_irrationals:
                fallbacks.append(_make_irrational(settings))
        elif target_set == "natural":
            fallbacks.append(_NumberExample("0", "0", "whole"))
            if allow_negative:
                fallbacks.append(_make_integer(settings))
            if allow_fractions:
                fallbacks.append(_make_rational(settings))
        elif target_set == "whole":
            if allow_negative:
                fallbacks.append(_make_integer(settings))
            if allow_fractions:
                fallbacks.append(_make_rational(settings))

        for filler in fallbacks:
            if len(options) >= 4:
                break
            if _membership(filler, target_set):
                continue
            if any(c.latex == filler.latex for c in options):
                continue
            options.append(filler)

        while len(options) < 4:
            # Last resort: distinct copies of a safe non-member label.
            options.append(_NumberExample(r"\pi", "π", "irrational") if allow_irrationals else _NumberExample("0.5", "0.5", "rational"))

        options = options[:4]
        random.shuffle(options)
        lines = [
            rf"\text{{{chr(65 + i)}. }} {opt.latex}"
            for i, opt in enumerate(options)
        ]
        prompt_latex = (
            rf"\text{{Which of the following is {_SET_DISPLAY[target_set]}?}}"
            + r" \\ "
            + r" \\ ".join(lines)
        )
        prompt_text = (
            f"Which of the following is {_SET_DISPLAY[target_set]}? "
            + "; ".join(f"{chr(65 + i)}. {opt.text}" for i, opt in enumerate(options))
        )
        answer = target.latex
        self._last_distractors = [o.latex for o in options if o.latex != target.latex]
        return prompt_latex, prompt_text, answer

    def _build_membership(
        self, settings: dict, enabled: list[str]
    ) -> tuple[str, str, str | None]:
        example = _random_example(settings)
        # Prefer a set that yields a non-trivial true/false (not always true for reals).
        claim_pool = [s for s in enabled if s != "real"] or enabled
        claim_set = random.choice(claim_pool)
        is_member = _membership(example, claim_set)
        # Occasionally force a false claim for variety when the random pick is true.
        if is_member and random.random() < 0.45 and len(claim_pool) > 1:
            false_sets = [s for s in claim_pool if not _membership(example, s)]
            if false_sets:
                claim_set = random.choice(false_sets)
                is_member = False

        truth = "True" if is_member else "False"
        set_label = _SET_DISPLAY[claim_set]
        article = "an" if set_label[0] in "aeiou" else "a"
        prompt_latex = (
            rf"\text{{True or false: }} {example.latex}"
            rf"\text{{ is {article} {set_label} number.}}"
        )
        prompt_text = f"True or false: {example.text} is {article} {set_label} number."
        answer = rf"\text{{{truth}}}"
        self._last_distractors = [r"\text{True}" if truth == "False" else r"\text{False}"]
        return prompt_latex, prompt_text, answer

    def build_question_metadata(
        self,
        settings: dict,
        *,
        prompt_latex: str,
        prompt_text: str,
        answer: str | None,
    ) -> dict[str, object]:
        meta: dict[str, object] = {}
        if self._last_distractors:
            meta["mc_distractors"] = list(self._last_distractors)
        return meta

