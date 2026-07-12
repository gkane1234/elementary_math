"""Advanced generators: law of sines/cosines, binomial, remainder, vectors, limits extras."""

from __future__ import annotations

import math
import random
from typing import Callable

from ..core.models import Question
from .utils import _make_questions, format_monomial_latex, format_polynomial_latex, random_int_range


def _law_of_sines(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        angle_a = random.choice([30, 40, 45, 50, 60, 70])
        angle_b = random.choice([30, 40, 45, 50, 60, 70])
        while angle_a + angle_b >= 170:
            angle_b = random.choice([30, 40, 45, 50, 60, 70])
        side_a = random.randint(5, 20)
        # sin B / b = sin A / a  => b = a * sin B / sin A
        b = side_a * math.sin(math.radians(angle_b)) / math.sin(math.radians(angle_a))
        prompt = (
            f"\\text{{In }} \\triangle ABC,\\ m\\angle A = {angle_a}^\\circ,\\ "
            f"m\\angle B = {angle_b}^\\circ,\\ a = {side_a}.\\ "
            f"\\text{{Find }} b \\text{{ (Law of Sines).}}"
        )
        answer = f"{b:.2f}" if include_answer_key else None
        return prompt, "law of sines", answer

    return _make_questions(topic, count, include_answer_key, build)


def _law_of_cosines(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        a = random.randint(5, 15)
        b = random.randint(5, 15)
        angle_c = random.choice([40, 50, 60, 70, 80, 100, 120])
        c2 = a * a + b * b - 2 * a * b * math.cos(math.radians(angle_c))
        c = math.sqrt(max(c2, 0.01))
        prompt = (
            f"\\text{{In }} \\triangle ABC,\\ a = {a},\\ b = {b},\\ "
            f"m\\angle C = {angle_c}^\\circ.\\ \\text{{Find }} c \\text{{ (Law of Cosines).}}"
        )
        answer = f"{c:.2f}" if include_answer_key else None
        return prompt, "law of cosines", answer

    return _make_questions(topic, count, include_answer_key, build)


def _binomial_theorem(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        n = random.randint(3, 6)
        a = random.randint(1, 4)
        k = random.randint(1, n - 1)
        # Coefficient of x^k in (a+x)^n is C(n,k) * a^(n-k)
        from math import comb

        coef = comb(n, k) * (a ** (n - k))
        prompt = (
            f"\\text{{Find the coefficient of }} x^{{{k}}} "
            f"\\text{{ in }} ({a} + x)^{{{n}}}."
        )
        answer = str(coef) if include_answer_key else None
        return prompt, "binomial theorem", answer

    return _make_questions(topic, count, include_answer_key, build)


def _remainder_theorem(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        # p(x) = x^2 + bx + c, divide by (x - a), remainder p(a)
        b = random_int_range(-6, 6, exclude={0})
        c = random_int_range(-8, 8, exclude={0})
        a = random_int_range(-5, 5, exclude={0})
        rem = a * a + b * a + c
        prompt = (
            f"\\text{{Find the remainder when }} {format_polynomial_latex([1, b, c])} "
            f"\\text{{ is divided by }} (x - {a})."
        )
        answer = str(rem) if include_answer_key else None
        return prompt, "remainder theorem", answer

    return _make_questions(topic, count, include_answer_key, build)


def _compound_interest(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        p = random.choice([500, 1000, 1500, 2000, 2500])
        r = random.choice([3, 4, 5, 6, 8])
        t = random.randint(2, 8)
        n = random.choice([1, 2, 4, 12])
        amount = p * (1 + r / (100 * n)) ** (n * t)
        prompt = (
            f"\\text{{Principal }} \\${p} \\text{{ at }} {r}\\% "
            f"\\text{{ compounded }} {n} \\text{{ time(s) per year for }} {t} "
            f"\\text{{ years. Find the balance.}}"
        )
        answer = f"{amount:.2f}" if include_answer_key else None
        return prompt, "compound interest", answer

    return _make_questions(topic, count, include_answer_key, build)


def _writing_numeric_expressions(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    templates = [
        (
            lambda a, b: (
                f"\\text{{Write an expression for }} {a} \\text{{ more than }} {b}.",
                f"{b} + {a}",
            )
        ),
        (
            lambda a, b: (
                f"\\text{{Write an expression for }} {a} \\text{{ less than }} {b}.",
                f"{b} - {a}",
            )
        ),
        (
            lambda a, b: (
                f"\\text{{Write an expression for the product of }} {a} \\text{{ and }} {b}.",
                f"{a} \\cdot {b}",
            )
        ),
        (
            lambda a, b: (
                f"\\text{{Write an expression for }} {a} \\text{{ times the sum of }} {b} "
                f"\\text{{ and 3.}}",
                f"{a}({b} + 3)",
            )
        ),
    ]

    def build() -> tuple[str, str, str | None]:
        a = random.randint(2, 12)
        b = random.randint(2, 20)
        prompt, expr = random.choice(templates)(a, b)
        answer = expr if include_answer_key else None
        return prompt, "writing numeric expression", answer

    return _make_questions(topic, count, include_answer_key, build)


def _decimal_divide(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        divisor = random.choice([0.2, 0.25, 0.5, 1.5, 2.5])
        quotient = random.randint(2, 12)
        dividend = round(divisor * quotient, 2)
        prompt = f"{dividend} \\div {divisor}"
        answer = str(quotient) if include_answer_key else None
        return prompt, "decimal division", answer

    return _make_questions(topic, count, include_answer_key, build)


def _vector_basics(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        a1, a2 = random.randint(-5, 5), random.randint(-5, 5)
        b1, b2 = random.randint(-5, 5), random.randint(-5, 5)
        op = random.choice(["add", "subtract", "magnitude"])
        if op == "add":
            prompt = (
                f"\\text{{Find }} \\langle {a1}, {a2} \\rangle + "
                f"\\langle {b1}, {b2} \\rangle."
            )
            answer = f"\\langle {a1 + b1}, {a2 + b2} \\rangle"
        elif op == "subtract":
            prompt = (
                f"\\text{{Find }} \\langle {a1}, {a2} \\rangle - "
                f"\\langle {b1}, {b2} \\rangle."
            )
            answer = f"\\langle {a1 - b1}, {a2 - b2} \\rangle"
        else:
            prompt = f"\\text{{Find }} \\lVert \\langle {a1}, {a2} \\rangle \\rVert."
            mag = math.sqrt(a1 * a1 + a2 * a2)
            answer = f"{mag:.3g}" if mag != int(mag) else str(int(mag))
        return prompt, f"vector {op}", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _dot_product(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        a1, a2 = random.randint(-6, 6), random.randint(-6, 6)
        b1, b2 = random.randint(-6, 6), random.randint(-6, 6)
        prompt = (
            f"\\text{{Find }} \\langle {a1}, {a2} \\rangle \\cdot "
            f"\\langle {b1}, {b2} \\rangle."
        )
        answer = str(a1 * b1 + a2 * b2) if include_answer_key else None
        return prompt, "dot product", answer

    return _make_questions(topic, count, include_answer_key, build)


def _polar_coordinates(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        r = random.randint(2, 10)
        theta = random.choice([0, 30, 45, 60, 90, 120, 135, 150, 180])
        x = r * math.cos(math.radians(theta))
        y = r * math.sin(math.radians(theta))
        prompt = (
            f"\\text{{Convert }} ({r}, {theta}^\\circ) "
            f"\\text{{ from polar to rectangular coordinates.}}"
        )
        answer = f"({x:.2f}, {y:.2f})" if include_answer_key else None
        return prompt, "polar to rectangular", answer

    return _make_questions(topic, count, include_answer_key, build)


def _limit_removable(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        a = random.randint(1, 6)
        # lim x->a of (x^2 - a^2)/(x - a) = 2a
        prompt = (
            f"\\lim_{{x \\to {a}}} \\frac{{x^{{2}} - {a * a}}}{{x - {a}}}"
        )
        answer = str(2 * a) if include_answer_key else None
        return prompt, "removable discontinuity limit", answer

    return _make_questions(topic, count, include_answer_key, build)


def _related_rates_simple(topic: str, settings: dict) -> list[Question]:
    """Simple related rates: expanding circle / similar."""
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        r = random.randint(2, 10)
        drdt = random.randint(1, 5)
        # dA/dt = 2 pi r dr/dt
        prompt = (
            f"\\text{{The radius of a circle increases at }} {drdt}\\text{{ cm/s. "
            f"How fast is the area increasing when }} r = {r}\\text{{ cm?}}"
        )
        answer = f"{2 * r * drdt}\\pi" if include_answer_key else None
        return prompt, "related rates circle", answer

    return _make_questions(topic, count, include_answer_key, build)


def _derivative_ln_exp(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        if random.choice([True, False]):
            n = random.randint(2, 5)
            prompt = f"\\frac{{d}}{{dx}}\\left[\\ln(x^{{{n}}})\\right]"
            answer = f"\\frac{{{n}}}{{x}}"
        else:
            k = random.randint(2, 5)
            prompt = f"\\frac{{d}}{{dx}}\\left[e^{{{k}x}}\\right]"
            answer = f"{k}e^{{{k}x}}"
        return prompt, "ln/exp derivative", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _intervals_increase_decrease(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        # f(x) = x^2 + bx + c → critical point at x = -b/2
        b = random_int_range(-8, 8, exclude={0})
        c = random.randint(-5, 5)
        crit = -b / 2
        sign_b = f"+ {b}x" if b > 0 else f"- {-b}x"
        sign_c = f"+ {c}" if c > 0 else (f"- {-c}" if c < 0 else "")
        prompt = (
            f"\\text{{Find the intervals where }} f(x) = x^{{2}} {sign_b}{sign_c} "
            f"\\text{{ is increasing.}}"
        )
        answer = f"({crit:g}, \\infty)" if include_answer_key else None
        return prompt, "intervals of increase", answer

    return _make_questions(topic, count, include_answer_key, build)


def _lhopitals_rule(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        a = random.randint(2, 6)
        # lim x->0 (sin(ax))/x = a
        arg = format_monomial_latex(a) or "0"
        prompt = f"\\lim_{{x \\to 0}} \\frac{{\\sin({arg})}}{{x}}"
        answer = str(a) if include_answer_key else None
        return prompt, "lhopital / standard limit", answer

    return _make_questions(topic, count, include_answer_key, build)


def _area_between_curves(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        a = random.randint(1, 4)
        # area between y=a and y=0 from 0 to 1 is a
        prompt = (
            f"\\text{{Find the area between }} y = {a} \\text{{ and }} y = 0 "
            f"\\text{{ from }} x = 0 \\text{{ to }} x = 1."
        )
        answer = str(a) if include_answer_key else None
        return prompt, "area between curves", answer

    return _make_questions(topic, count, include_answer_key, build)


def _inverse_trig_functions(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    values = {
        ("arcsin", "0"): "0",
        ("arcsin", r"\frac{1}{2}"): r"\frac{\pi}{6}",
        ("arcsin", r"\frac{\sqrt{2}}{2}"): r"\frac{\pi}{4}",
        ("arcsin", "1"): r"\frac{\pi}{2}",
        ("arccos", "0"): r"\frac{\pi}{2}",
        ("arccos", r"\frac{1}{2}"): r"\frac{\pi}{3}",
        ("arctan", "0"): "0",
        ("arctan", "1"): r"\frac{\pi}{4}",
    }

    def build() -> tuple[str, str, str | None]:
        (fn, arg), val = random.choice(list(values.items()))
        prompt = f"\\{fn}\\left({arg}\\right)"
        answer = val if include_answer_key else None
        return prompt, "inverse trig", answer

    return _make_questions(topic, count, include_answer_key, build)


GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = {
    "law_of_sines": _law_of_sines,
    "law_of_cosines": _law_of_cosines,
    "binomial_theorem": _binomial_theorem,
    "remainder_theorem": _remainder_theorem,
    "compound_interest": _compound_interest,
    "writing_numeric_expressions": _writing_numeric_expressions,
    "g6_decimal_divide": _decimal_divide,
    "vector_basics": _vector_basics,
    "dot_product": _dot_product,
    "polar_coordinates": _polar_coordinates,
    "limit_removable": _limit_removable,
    "related_rates_simple": _related_rates_simple,
    "derivative_ln_exp": _derivative_ln_exp,
    "intervals_increase_decrease": _intervals_increase_decrease,
    "lhopitals_rule": _lhopitals_rule,
    "area_between_curves": _area_between_curves,
    "inverse_trig_functions": _inverse_trig_functions,
}
