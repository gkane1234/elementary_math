"""Number generator framework — rationals, decimals, percents, ratios, rates."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction

from .base import QuestionFramework
from ..generators.utils import format_fraction_division_latex, frac_latex, random_fraction, random_int_range
from ..settings.params import allowed_division_notations


@dataclass(frozen=True)
class NumberParams:
    num_min: int = -10
    num_max: int = 10
    denom_min: int = 2
    denom_max: int = 12
    allow_negative: bool = True


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
    return _int_range(settings, "sci_exp_min", "sci_exp_max", lo_default=-8, hi_default=8)


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
        )

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
            prompt_latex = f"{frac_latex(a)} {latex_op} {frac_latex(b)}"
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


class DecimalArithmeticFramework(NumberFramework):
    """Decimal addition, subtraction, multiplication, and division."""

    def __init__(self, operation: str = "+"):
        self.operation = operation

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        places = int(settings.get("decimal_places", 2))
        allow_negative = bool(settings.get("allow_negative", False))
        minimum = 0.1 if not allow_negative else -99.9
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
            a = _random_decimal(places=min(places, 1), minimum=0.2, maximum=9.9)
            b = _random_decimal(places=min(places, 1), minimum=0.2, maximum=9.9)
        if self.operation == "/":
            divisor = random.randint(2, 9)
            quotient = _random_decimal(places=places, minimum=0.5, maximum=9.5)
            a = (quotient * Decimal(divisor)).quantize(Decimal(10) ** -places)
            b = Decimal(divisor)

        ops = {
            "+": lambda x, y: x + y,
            "-": lambda x, y: x - y,
            "*": lambda x, y: x * y,
            "/": lambda x, y: x / y,
        }
        result = ops[self.operation](a, b)
        latex_op = {"+": "+", "-": "-", "*": "\\cdot", "/": "\\div"}[self.operation]
        prompt_latex = f"{_format_decimal(a, places=places)} {latex_op} {_format_decimal(b, places=places)}"
        return prompt_latex, f"{a} {self.operation} {b}", _format_decimal(result, places=places)


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
                answer = f"{outer}x {('+' if outer * inner_b >= 0 else '-')} {abs(outer * inner_b)}"
            else:
                answer = f"{outer}x {'+' if -outer * inner_b >= 0 else '-'} {abs(outer * inner_b)}"
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
        mantissa = random.randint(11, 99) / 10
        return mantissa, exponent

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        if self.mode == "write":
            mantissa, exponent = self._random_sci_pair(settings)
            value = mantissa * (10**exponent)
            if exponent >= 0:
                prompt = f"\\text{{Write in scientific notation: }} {value:g}"
            else:
                prompt = f"\\text{{Write in scientific notation: }} {value:.6g}"
            return prompt, str(value), f"{mantissa:g} \\times 10^{{{exponent}}}"

        if self.mode == "operations":
            a, a_exp = self._random_sci_pair(settings)
            b, b_exp = self._random_sci_pair(settings)
            op = random.choice(["\\times", "\\div"])
            if op == "\\times":
                product = a * b
                exp_sum = a_exp + b_exp
                answer = f"{product:.2g} \\times 10^{{{exp_sum}}}"
            else:
                quotient = a / b
                exp_diff = a_exp - b_exp
                answer = f"{quotient:.2g} \\times 10^{{{exp_diff}}}"
            prompt = (
                f"({a:g} \\times 10^{{{a_exp}}}) {op} "
                f"({b:g} \\times 10^{{{b_exp}}})"
            )
            return prompt, "scientific notation operation", answer

        exp_lo, exp_hi = _sci_exp_bounds(settings)
        exp = random.randint(max(exp_lo, -3), min(exp_hi, 3))
        a = random.randint(11, 99) / 10
        b = random.randint(11, 99) / 10
        op = random.choice(["+", "-"])
        result = (a + b if op == "+" else a - b) * (10**exp)
        prompt = (
            f"({a:g} \\times 10^{{{exp}}}) {op} "
            f"({b:g} \\times 10^{{{exp}}})"
        )
        return prompt, "scientific notation add/subtract", f"{result:g}"


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
    """Fraction division word problems (how many groups, how much per group)."""

    def __init__(self, *, mode: str = "groups"):
        self.mode = mode

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        params = number_params_from_settings(settings)
        divisor = random_fraction(
            num_min=1,
            num_max=max(3, params.num_max // 2),
            denom_min=params.denom_min,
            denom_max=min(8, params.denom_max),
            allow_negative=False,
        )
        quotient = random.randint(2, 6)
        dividend = divisor * quotient
        contexts = {
            "groups": (
                f"\\text{{How many groups of }} {frac_latex(divisor)} "
                f"\\text{{ are in }} {frac_latex(dividend)}\\text{{?}}"
            ),
            "each": (
                f"\\text{{If }} {frac_latex(dividend)} \\text{{ is shared equally into "
                f"}}{quotient} \\text{{ groups, how much is in each group?}}"
            ),
            "whole": (
                f"\\text{{What fraction of a whole is }} {frac_latex(Fraction(1, 2))} "
                f"\\text{{ of }} {frac_latex(dividend)}\\text{{?}}"
            ),
        }
        prompt = contexts[self.mode]
        if self.mode == "whole":
            portion = Fraction(1, 2)
            answer = frac_latex(portion * dividend)
        else:
            answer = frac_latex(quotient) if self.mode == "groups" else frac_latex(divisor)
        return prompt, f"fraction division ({self.mode})", answer


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


class PrimeFactorizationFramework(NumberFramework):
    """Prime factorization of a composite whole number."""

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        lo, hi = _factor_bounds(settings)
        lo = max(lo, 12)
        n = random.randint(lo, hi)
        while n < 12 or all(n % p != 0 for p in (2, 3, 5)):
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
