"""Thin generators that fix grade-level / wrong-skill catalog wirings."""

from __future__ import annotations

import math
import random
from fractions import Fraction
from typing import Callable

from ..core.models import Question
from .utils import _make_questions, frac_latex


_ONES_WORDS = {
    0: "zero",
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten",
    11: "eleven",
    12: "twelve",
    13: "thirteen",
    14: "fourteen",
    15: "fifteen",
    16: "sixteen",
    17: "seventeen",
    18: "eighteen",
    19: "nineteen",
}
_TENS_WORDS = {
    2: "twenty",
    3: "thirty",
    4: "forty",
    5: "fifty",
    6: "sixty",
    7: "seventy",
    8: "eighty",
    9: "ninety",
}
_PLACE_NAMES = (
    ("ones", 0),
    ("tenths", 1),
    ("hundredths", 2),
    ("thousandths", 3),
)


def _int_to_words(n: int) -> str:
    if n < 0:
        return "negative " + _int_to_words(-n)
    if n < 20:
        return _ONES_WORDS[n]
    if n < 100:
        tens, ones = divmod(n, 10)
        if ones == 0:
            return _TENS_WORDS[tens]
        return f"{_TENS_WORDS[tens]}-{_ONES_WORDS[ones]}"
    if n < 1000:
        hundreds, rest = divmod(n, 100)
        if rest == 0:
            return f"{_ONES_WORDS[hundreds]} hundred"
        return f"{_ONES_WORDS[hundreds]} hundred {_int_to_words(rest)}"
    thousands, rest = divmod(n, 1000)
    if rest == 0:
        return f"{_int_to_words(thousands)} thousand"
    return f"{_int_to_words(thousands)} thousand {_int_to_words(rest)}"


def place_value_and_rounding(topic: str, settings: dict) -> list[Question]:
    """Name a decimal place or round to a given place (Pre-Algebra)."""
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        if random.choice([True, False]):
            whole = random.randint(10, 999)
            tenths = random.randint(0, 9)
            hundredths = random.randint(0, 9)
            thousandths = random.randint(1, 9)
            value = whole + tenths / 10 + hundredths / 100 + thousandths / 1000
            place_name, place_idx = random.choice(_PLACE_NAMES[1:])  # tenths+
            digit = (tenths, hundredths, thousandths)[place_idx - 1]
            prompt = (
                rf"\text{{What digit is in the {place_name} place of }} "
                rf"{value:.3f}\text{{?}}"
            )
            answer = str(digit)
            return prompt, "place value", answer if keyed else None

        value = round(random.uniform(1, 99), 3)
        place_name, ndigits = random.choice(
            (("whole number", 0), ("tenth", 1), ("hundredth", 2))
        )
        rounded = round(value, ndigits)
        prompt = (
            rf"\text{{Round }} {value:.3f} \text{{ to the nearest {place_name}.}}"
        )
        fmt = f"{{:.{ndigits}f}}" if ndigits else "{:.0f}"
        answer = fmt.format(rounded)
        return prompt, "rounding", answer if keyed else None

    return _make_questions(topic, count, keyed, build)


def writing_numbers_with_words(topic: str, settings: dict) -> list[Question]:
    """Write whole numbers in words (Pre-Algebra)."""
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))
    max_n = int(settings.get("coef_max", 9999))

    def build() -> tuple[str, str, str | None]:
        n = random.randint(1, max(1, max_n))
        prompt = rf"\text{{Write }} {n} \text{{ in words.}}"
        answer = rf"\text{{{_int_to_words(n)}}}"
        return prompt, "number words", answer if keyed else None

    return _make_questions(topic, count, keyed, build)


def simplifying_numeric_fractions(topic: str, settings: dict) -> list[Question]:
    """Simplify numeric fractions by canceling a GCF (not polynomial rationals)."""
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        g = random.randint(2, 12)
        a = random.randint(1, 12)
        b = random.randint(1, 12)
        while math.gcd(a, b) != 1:
            b = random.randint(1, 12)
        num, den = a * g, b * g
        if random.choice([True, False]):
            num, den = den, num
        simplified = Fraction(num, den)
        prompt = rf"\text{{Simplify }} \frac{{{num}}}{{{den}}}."
        answer = frac_latex(simplified)
        return prompt, "simplify fraction", answer if keyed else None

    return _make_questions(topic, count, keyed, build)


def complex_rationalize_denominator(topic: str, settings: dict) -> list[Question]:
    """Rationalize denominators of complex numbers (multiply by conjugate)."""
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        # a/(b+ci) or (a+bi)/(c+di) — keep integers small and den non-real.
        if random.choice([True, False]):
            a = random.randint(1, 8)
            c = random.randint(-6, 6)
            d = random.choice([i for i in range(-6, 7) if i != 0])
            # a/(c+di) * (c-di)/(c-di)
            den = c * c + d * d
            real = Fraction(a * c, den)
            imag = Fraction(-a * d, den)
            prompt = rf"\text{{Rationalize }} \dfrac{{{a}}}{{{c}{'+' if d > 0 else ''}{d}i}}."
        else:
            a = random.randint(-5, 5)
            b = random.choice([i for i in range(-5, 6) if i != 0])
            c = random.randint(-5, 5)
            d = random.choice([i for i in range(-5, 6) if i != 0])
            den = c * c + d * d
            real = Fraction(a * c + b * d, den)
            imag = Fraction(b * c - a * d, den)
            num = f"{a}{'+' if b > 0 else ''}{b}i" if a != 0 else f"{b}i"
            if a == 0 and b == 1:
                num = "i"
            elif a == 0 and b == -1:
                num = "-i"
            den_s = f"{c}{'+' if d > 0 else ''}{d}i"
            prompt = rf"\text{{Rationalize }} \dfrac{{{num}}}{{{den_s}}}."

        def _ci(re: Fraction, im: Fraction) -> str:
            parts = []
            if re != 0 or im == 0:
                parts.append(frac_latex(re))
            if im != 0:
                coef = frac_latex(abs(im)) if abs(im) != 1 else ""
                sign = "+" if im > 0 and parts else ("-" if im < 0 else "")
                if abs(im) == 1:
                    parts.append(f"{sign}i" if sign else "i")
                else:
                    parts.append(f"{sign}{coef}i" if sign else f"{coef}i")
            return "".join(parts) if parts else "0"

        answer = _ci(real, imag)
        return prompt, "complex rationalize", answer if keyed else None

    return _make_questions(topic, count, keyed, build)


def trigonometry_and_area(topic: str, settings: dict) -> list[Question]:
    """Area of a triangle via (1/2)ab sin C."""
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        a = random.randint(3, 12)
        b = random.randint(3, 12)
        # Nice sine values
        angle, sin_val = random.choice(
            [
                (30, Fraction(1, 2)),
                (45, Fraction(1, 1)),  # use √2/2 → area = ab√2/4
                (60, Fraction(1, 1)),  # √3/2 → area = ab√3/4
                (90, Fraction(1, 1)),
            ]
        )
        if angle == 45:
            area_latex = rf"\frac{{{a * b}}}{{4}}\sqrt{{2}}"
            # store numeric for check: ab * sqrt(2) / 4
        elif angle == 60:
            area_latex = rf"\frac{{{a * b}}}{{4}}\sqrt{{3}}"
        elif angle == 90:
            area_val = Fraction(a * b, 2)
            area_latex = frac_latex(area_val)
        else:  # 30
            area_val = Fraction(a * b, 4)
            area_latex = frac_latex(area_val)

        prompt = (
            rf"\text{{In }} \triangle ABC, AB={b}, AC={a}, "
            rf"\text{{ and }} \angle A={angle}^\circ. "
            rf"\text{{Find the area.}}"
        )
        return prompt, "trig area", area_latex if keyed else None

    return _make_questions(topic, count, keyed, build)


def scatter_plot_interpret(topic: str, settings: dict) -> list[Question]:
    """Describe association / make a prediction from a described scatter trend."""
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        mode = random.choice(["association", "predict"])
        if mode == "association":
            kind = random.choice(
                [
                    ("positive", "positive"),
                    ("negative", "negative"),
                    ("no clear", "none"),
                ]
            )
            prompt = (
                rf"\text{{A scatter plot of hours studied vs. test score shows a "
                rf"{kind[0]} linear trend. What type of association is this?}}"
            )
            answer = rf"\text{{{kind[1]} association}}"
            return prompt, "scatter association", answer if keyed else None

        slope = random.choice([2, 3, 4, 5])
        intercept = random.randint(10, 40)
        x = random.randint(2, 8)
        y = slope * x + intercept
        prompt = (
            rf"\text{{A linear model for a scatter plot is }} "
            rf"y = {slope}x + {intercept}. "
            rf"\text{{Predict }} y \text{{ when }} x = {x}."
        )
        return prompt, "scatter predict", str(y) if keyed else None

    return _make_questions(topic, count, keyed, build)


def g6_whole_by_decimal_divide(topic: str, settings: dict) -> list[Question]:
    """Divide a whole number by a decimal (Grade 6)."""
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        # n ÷ 0.2 = 5n, etc. — exact integer answers
        divisor, mult = random.choice([(0.2, 5), (0.25, 4), (0.5, 2)])
        n = random.randint(2, 15)
        prompt = f"{n} \\div {divisor}"
        return prompt, "whole ÷ decimal", str(n * mult) if keyed else None

    return _make_questions(topic, count, keyed, build)


def check_equation_solution(topic: str, settings: dict) -> list[Question]:
    """Ask whether a given value is a solution (Grade 6), not solve for x."""
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        a = random.randint(2, 9)
        x = random.randint(1, 12)
        b = random.randint(1, 20)
        rhs = a * x + b
        candidate = x if random.random() < 0.55 else random.randint(1, 12)
        while candidate == x and random.random() < 0.5:
            candidate = random.randint(1, 12)
        is_sol = candidate == x
        prompt = (
            rf"\text{{Is }} x = {candidate} \text{{ a solution of }} "
            rf"{a}x + {b} = {rhs}\text{{?}}"
        )
        answer = r"\text{yes}" if is_sol else r"\text{no}"
        return prompt, "check solution", answer if keyed else None

    return _make_questions(topic, count, keyed, build)


def write_one_step_equation(topic: str, settings: dict) -> list[Question]:
    """Write a one-step equation from a simple verbal relationship (Grade 6)."""
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        rate = random.randint(2, 12)
        hours = random.randint(2, 8)
        total = rate * hours
        prompt = (
            rf"\text{{A bike travels at }} {rate} \text{{ miles per hour. "
            rf"Write an equation for the distance }} d \text{{ after }} "
            rf"{hours} \text{{ hours, then find }} d."
        )
        answer = rf"d = {rate}\cdot {hours};\; d = {total}"
        return prompt, "write rate equation", answer if keyed else None

    return _make_questions(topic, count, keyed, build)


GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = {
    "place_value_and_rounding": place_value_and_rounding,
    "writing_numbers_with_words": writing_numbers_with_words,
    "simplifying_numeric_fractions": simplifying_numeric_fractions,
    "complex_rationalize_denominator": complex_rationalize_denominator,
    "trigonometry_and_area": trigonometry_and_area,
    "scatter_plot_interpret": scatter_plot_interpret,
    "g6_whole_by_decimal_divide": g6_whole_by_decimal_divide,
    "check_equation_solution": check_equation_solution,
    "write_one_step_equation": write_one_step_equation,
}
