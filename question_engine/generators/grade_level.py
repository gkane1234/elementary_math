"""Thin generators that fix grade-level / wrong-skill catalog wirings."""

from __future__ import annotations

import random
from decimal import ROUND_HALF_UP, Decimal
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
# Round-to targets: (singular place name in prompt, decimal places after round).
_ROUND_TARGETS = (
    ("whole number", 0),
    ("tenth", 1),
    ("hundredth", 2),
    ("thousandth", 3),
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
    if n < 1_000_000:
        thousands, rest = divmod(n, 1000)
        head = f"{_int_to_words(thousands)} thousand"
        if rest == 0:
            return head
        return f"{head} {_int_to_words(rest)}"
    millions, rest = divmod(n, 1_000_000)
    head = f"{_int_to_words(millions)} million"
    if rest == 0:
        return head
    return f"{head} {_int_to_words(rest)}"


def _words_max_for_difficulty(d: float) -> int:
    """Place-value ladder for writing numbers — plateaus by skill, not forever.

    Easy: teens/two-digit. Then hundreds → thousands → ten-thousands →
    hundred-thousands → low millions. Past that the skill is the same.
    """
    if d < 3.0:
        return 20
    if d < 6.0:
        return 99
    if d < 10.0:
        return 999
    if d < 14.0:
        return 9_999
    if d < 18.0:
        return 99_999
    if d < 24.0:
        return 999_999
    return 9_999_999


def _place_rounding_params(d: float) -> dict[str, float | int]:
    """Continuous place-value / rounding ladder (not EMH plateau).

    Returns caps that grow with ``d``:
    - ``whole_max`` / ``whole_lo`` — magnitude of the integer part
    - ``show_decimals`` — how many decimal digits are displayed
    - ``name_max_place`` — deepest place that can be asked (1=tenths … 3=thousandths)
    - ``round_max`` — deepest round-to target (0=whole … 2=hundredth)
    - ``carry_p`` — probability of constructing a carry-across rounding case
    - ``name_p`` — probability of a name-the-digit prompt vs round
    """
    d = max(0.0, float(d))
    if d < 4.0:
        return {
            "whole_lo": 1,
            "whole_max": 20,
            "show_decimals": 1,
            "name_max_place": 1,
            "round_max": 1,
            "carry_p": 0.05,
            "name_p": 0.55,
        }
    if d < 8.0:
        return {
            "whole_lo": 5,
            "whole_max": 99,
            "show_decimals": 2,
            "name_max_place": 2,
            "round_max": 2,
            "carry_p": 0.15,
            "name_p": 0.5,
        }
    if d < 14.0:
        return {
            "whole_lo": 10,
            "whole_max": 999,
            "show_decimals": 2 if d < 11.0 else 3,
            "name_max_place": 2 if d < 11.0 else 3,
            "round_max": 2,
            "carry_p": 0.3,
            "name_p": 0.45,
        }
    if d < 22.0:
        return {
            "whole_lo": 50,
            "whole_max": 9_999,
            "show_decimals": 3,
            "name_max_place": 3,
            "round_max": 2,
            "carry_p": 0.45,
            "name_p": 0.4,
        }
    # Keep growing magnitude past the place-skill plateau.
    extra = d - 22.0
    whole_max = int(9_999 + 200 * extra + 12 * extra * extra)
    return {
        "whole_lo": max(100, whole_max // 10),
        "whole_max": whole_max,
        "show_decimals": 3,
        "name_max_place": 3,
        "round_max": 2,
        "carry_p": min(0.7, 0.45 + extra / 40.0),
        "name_p": 0.35,
    }


def _format_decimal_from_digits(whole: int, digits: list[int]) -> str:
    if not digits:
        return str(whole)
    return f"{whole}." + "".join(str(x) for x in digits)


def _decimal_from_digits(whole: int, digits: list[int]) -> Decimal:
    return Decimal(_format_decimal_from_digits(whole, digits))


def _round_half_up(value: Decimal, ndigits: int) -> Decimal:
    if ndigits <= 0:
        quant = Decimal("1")
    else:
        quant = Decimal("1").scaleb(-ndigits)
    return value.quantize(quant, rounding=ROUND_HALF_UP)


def _sample_decimal_digits(show: int, *, force_nonzero_last: bool = True) -> list[int]:
    digits = [random.randint(0, 9) for _ in range(show)]
    if force_nonzero_last and show > 0 and digits[-1] == 0:
        digits[-1] = random.randint(1, 9)
    return digits


def _apply_rounding_carry(digits: list[int], ndigits: int) -> list[int]:
    """Bias digits so rounding to ``ndigits`` needs a carry (often cascading 9s)."""
    show = len(digits)
    if show <= ndigits:
        # Need one more place past the round target to decide up/down.
        digits = digits + [0] * (ndigits + 1 - show)
        show = len(digits)
    # Digit immediately right of target decides round-up.
    digits[ndigits] = random.randint(5, 9)
    # Cascade-friendly: make the rounded place (and maybe ones above) be 9.
    cascade_depth = random.randint(0, min(ndigits, 2))
    for i in range(ndigits - cascade_depth, ndigits):
        if i >= 0:
            digits[i] = 9
    # Trailing places after the decision digit: keep display full-length.
    for i in range(ndigits + 1, show):
        digits[i] = random.randint(0, 9)
    if digits[-1] == 0:
        digits[-1] = random.randint(1, 9)
    return digits


def place_value_and_rounding(topic: str, settings: dict) -> list[Question]:
    """Name a decimal place or round to a given place (Pre-Algebra).

    Continuous ``difficulty`` climbs a place ladder: tenths/small wholes →
    hundredths → thousandths with larger magnitudes and carry-across rounding.
    """
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        from question_engine.frameworks.difficulty_budget import settings_difficulty

        d = settings_difficulty(settings, default=8.0)
        p = _place_rounding_params(d)
        whole_lo = int(p["whole_lo"])
        whole_max = int(p["whole_max"])
        show = int(p["show_decimals"])
        name_max = int(p["name_max_place"])
        round_max = int(p["round_max"])
        # Mix a lighter whole band ~25% so review stays present.
        if whole_lo > 1 and random.random() < 0.25:
            whole_lo = max(1, whole_lo // 5)
        whole = random.randint(whole_lo, whole_max)

        do_name = random.random() < float(p["name_p"])
        if do_name:
            digits = _sample_decimal_digits(show)
            # Prefer asking about the deepest unlocked place ~60% of the time.
            place_choices = list(range(1, name_max + 1))
            # High D: sometimes name the ones digit in a multi-place decimal.
            if d >= 14.0 and random.random() < 0.2:
                place_choices = [0] + place_choices
            if random.random() < 0.6:
                place_idx = place_choices[-1]
            else:
                place_idx = random.choice(place_choices)
            place_idx = min(place_idx, show) if place_idx > 0 else 0
            place_name = _PLACE_NAMES[place_idx][0]
            if place_idx == 0:
                digit = whole % 10
            else:
                digit = digits[place_idx - 1]
            shown = _format_decimal_from_digits(whole, digits)
            prompt = (
                rf"\text{{What digit is in the {place_name} place of }} "
                rf"{shown}\text{{?}}"
            )
            return prompt, "place value", str(digit) if keyed else None

        # Rounding prompt.
        ndigits = random.randint(0, round_max)
        # Need at least one digit past the round target when possible.
        need_show = max(show, ndigits + 1)
        need_show = min(need_show, 3)
        digits = _sample_decimal_digits(need_show)
        want_carry = random.random() < float(p["carry_p"])
        if want_carry and need_show > ndigits:
            digits = _apply_rounding_carry(digits, ndigits)
            # Cascade into the ones place when the fractional run is all 9s.
            frac_nines = all(digits[i] == 9 for i in range(ndigits))
            if (ndigits == 0 or frac_nines) and random.random() < 0.55:
                whole = whole - (whole % 10) + 9
        value = _decimal_from_digits(whole, digits)
        place_name, _ = _ROUND_TARGETS[ndigits]
        rounded = _round_half_up(value, ndigits)
        shown = _format_decimal_from_digits(whole, digits)
        prompt = (
            rf"\text{{Round }} {shown} \text{{ to the nearest {place_name}.}}"
        )
        if ndigits == 0:
            answer = format(rounded, "f").split(".")[0]
        else:
            answer = f"{rounded:.{ndigits}f}"
        return prompt, "rounding", answer if keyed else None

    return _make_questions(topic, count, keyed, build)


def writing_numbers_with_words(topic: str, settings: dict) -> list[Question]:
    """Write whole numbers in words (Pre-Algebra).

    Difficulty climbs a place-value ladder (teens → … → millions) then plateaus —
    bigger digits stop buying new skill past low millions. At higher D, sometimes
    ask the reverse (words → numeral).
    """
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        from question_engine.frameworks.difficulty_budget import settings_difficulty

        d = settings_difficulty(settings, default=8.0)
        max_n = _words_max_for_difficulty(d)
        # Prefer the new place band so D=10 isn't mostly two-digit leftovers.
        if max_n <= 20:
            lo = 1
        elif max_n <= 99:
            lo = 21
        elif max_n <= 999:
            lo = 100
        elif max_n <= 9_999:
            lo = 1_000
        elif max_n <= 99_999:
            lo = 10_000
        elif max_n <= 999_999:
            lo = 100_000
        else:
            lo = 1_000_000
        # Mix in easier band ~30% so review stays present.
        if lo > 1 and random.random() < 0.3:
            lo = max(1, lo // 10)
        n = random.randint(lo, max_n)
        words = _int_to_words(n)
        # Reverse direction unlocks once students can write thousands+.
        if d >= 12.0 and random.random() < min(0.45, (d - 12.0) / 20.0):
            prompt = rf"\text{{Write in numerals: }} \text{{{words}}}"
            answer = str(n)
            return prompt, "words to number", answer if keyed else None
        prompt = rf"\text{{Write }} {n} \text{{ in words.}}"
        answer = rf"\text{{{words}}}"
        return prompt, "number words", answer if keyed else None

    return _make_questions(topic, count, keyed, build)


def simplifying_numeric_fractions(topic: str, settings: dict) -> list[Question]:
    """Simplify numeric fractions by canceling a GCF (not polynomial rationals).

    Continuous ``difficulty`` builds factors-first: pick reduced ``a/b`` (gcd=1),
    inflate by ``k`` (possibly a product of primes), show ``(a·k)/(b·k)``.
    Hardness tracks number size, |GCF|, and composite multi-step cancel feel.
    """
    from question_engine.frameworks.number import sample_unreduced_numeric_fraction

    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        num, den = sample_unreduced_numeric_fraction(settings)
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
    "check_equation_solution": check_equation_solution,
    "write_one_step_equation": write_one_step_equation,
}
