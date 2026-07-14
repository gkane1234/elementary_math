"""Number, ratio, rate, percent, and fraction question generators."""

from __future__ import annotations

import random
from typing import Callable

from packages.polynomial_core import Polynomial, square_root_latex

from ..core.models import Question
from ..frameworks.number import (
    DecimalArithmeticFramework,
    DistributiveFramework,
    FractionDecimalConvertFramework,
    MixedNumberArithmeticFramework,
    OrderOfOperationsFramework,
    PercentFramework,
    ProportionFramework,
    RationalFramework,
    RatioFramework,
    ScientificNotationFramework,
    SetsOfNumbersFramework,
    UnitRateFramework,
)
from .utils import make_questions

_SQUARE_FREE_BASES = (2, 3, 5, 6, 7, 10, 11, 13, 14, 15, 17, 19, 21, 22, 23, 26, 29, 30)
_EXTRACT_SQUARES = (4, 9, 16, 25, 36, 49)

_RATIONAL_ADD_SUBTRACT = RationalFramework("+-")
_RATIONAL_MULTIPLY = RationalFramework("*")
_RATIONAL_DIVIDE = RationalFramework("/")
_PA_MIXED_ADD_SUBTRACT = MixedNumberArithmeticFramework("+-")
_DISTRIBUTIVE = DistributiveFramework()
_DISTRIBUTIVE_ALGEBRAIC = DistributiveFramework(algebraic=True)
_PERCENTS = PercentFramework()
_PERCENT_OF_CHANGE = PercentFramework(percent_change=True)
_FRAC_DECIMAL = FractionDecimalConvertFramework()
_FRAC_DECIMAL_PERCENT = FractionDecimalConvertFramework(include_percent=True)
_PROPORTIONS = ProportionFramework()
_RATIO_INTRO = RatioFramework()
_RATIO_EQUIVALENT = RatioFramework(equivalent=True)
_UNIT_RATE = UnitRateFramework()
_DECIMAL_ADD = DecimalArithmeticFramework("+")
_DECIMAL_SUBTRACT = DecimalArithmeticFramework("-")
_DECIMAL_MULTIPLY = DecimalArithmeticFramework("*")
_ORDER_OF_OPERATIONS = OrderOfOperationsFramework()
_SCI_NOTATION_WRITE = ScientificNotationFramework(mode="write")
_SCI_NOTATION_OPS = ScientificNotationFramework(mode="operations")
_SCI_NOTATION_ADD_SUB = ScientificNotationFramework(mode="add_subtract")
_SETS_OF_NUMBERS = SetsOfNumbersFramework()


def _framework_generator(framework, topic: str, settings: dict) -> list[Question]:
    return framework.generate_batch(topic, settings)


def sets_of_numbers(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_SETS_OF_NUMBERS, topic, settings)


def rational_add_subtract(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_RATIONAL_ADD_SUBTRACT, topic, settings)


def pa_integers_adding_and_subtracting(topic: str, settings: dict) -> list[Question]:
    """Pre-Algebra Integers/Decimals/Fractions: mixed add/subtract forms."""
    return _framework_generator(_PA_MIXED_ADD_SUBTRACT, topic, settings)


def rational_multiply(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_RATIONAL_MULTIPLY, topic, settings)


def rational_divide(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_RATIONAL_DIVIDE, topic, settings)


def distributive_property(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_DISTRIBUTIVE, topic, settings)


def distributive_property_algebraic(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_DISTRIBUTIVE_ALGEBRAIC, topic, settings)


def percents(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_PERCENTS, topic, settings)


def percent_of_change(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_PERCENT_OF_CHANGE, topic, settings)


def converting_fractions_and_decimals(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_FRAC_DECIMAL, topic, settings)


def fractions_decimals_and_percents(topic: str, settings: dict) -> list[Question]:
    """Fraction ↔ decimal ↔ percent conversions (not percent-of loops)."""
    settings = {**settings, "include_percent_conversions": True}
    return _framework_generator(_FRAC_DECIMAL_PERCENT, topic, settings)


def solving_proportions(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_PROPORTIONS, topic, settings)


def scientific_notation_write(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_SCI_NOTATION_WRITE, topic, settings)


def scientific_notation_operations(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_SCI_NOTATION_OPS, topic, settings)


def scientific_notation_add_subtract(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_SCI_NOTATION_ADD_SUB, topic, settings)


def g6_introduction_to_ratios(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_RATIO_INTRO, topic, settings)


def g6_equivalent_ratios(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_RATIO_EQUIVALENT, topic, settings)


def g6_unit_rates(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_UNIT_RATE, topic, settings)


def g6_decimal_addition(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_DECIMAL_ADD, topic, settings)


def g6_decimal_subtraction(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_DECIMAL_SUBTRACT, topic, settings)


def g6_decimal_multiplication(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_DECIMAL_MULTIPLY, topic, settings)


def order_of_operations(topic: str, settings: dict) -> list[Question]:
    return _framework_generator(_ORDER_OF_OPERATIONS, topic, settings)


def _normalize_base_range(settings: dict) -> tuple[int, int]:
    lo = max(1, int(settings.get("base_min", 2)))
    hi = max(lo, int(settings.get("base_max", 12)))
    return lo, hi


def pa_squares_and_square_roots(topic: str, settings: dict) -> list[Question]:
    """Evaluate squares (n²) and square roots (√n) for Pre-Algebra.

    Easy/medium stay on perfect-square mental math. Hard mixes larger perfects
    with non-perfect radicands (leave under √ or extract a square factor).
    """
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    allow_roots = bool(settings.get("allow_square_roots", True))
    allow_squares = bool(settings.get("allow_squares", True))
    allow_word = bool(settings.get("allow_word_prompts", True))
    perfect_only = bool(settings.get("perfect_squares_only", True))
    allow_extract = bool(settings.get("allow_extract_square_factors", False))
    base_lo, base_hi = _normalize_base_range(settings)

    modes: list[str] = []
    if allow_roots:
        modes.append("root")
    if allow_squares:
        modes.append("square")
    if not modes:
        modes = ["root", "square"]

    def _square_prompt(n: int) -> tuple[str, str, str | None]:
        answer = str(n * n) if include_answer_key else None
        if allow_word and random.random() < 0.45:
            return (
                f"\\text{{What is }} {n} \\text{{ squared?}}",
                f"What is {n} squared?",
                answer,
            )
        return f"{n}^{{2}}", f"{n}^2", answer

    def _perfect_root(n: int) -> tuple[str, str, str | None]:
        radicand = n * n
        answer = str(n) if include_answer_key else None
        return f"\\sqrt{{{radicand}}}", f"sqrt({radicand})", answer

    def _extract_root() -> tuple[str, str, str | None]:
        outer_sq = random.choice(_EXTRACT_SQUARES)
        leftover = random.choice(_SQUARE_FREE_BASES)
        radicand = outer_sq * leftover
        coeff, simplified = Polynomial.simplify_square_root(radicand)
        answer = (
            square_root_latex(coeff, simplified) if include_answer_key else None
        )
        return f"\\sqrt{{{radicand}}}", f"sqrt({radicand})", answer

    def _non_perfect_root() -> tuple[str, str, str | None]:
        # Square-free (or residual) radicand — answer stays under a root.
        leftover = random.choice(_SQUARE_FREE_BASES)
        # Occasionally pad with a small square so extract path is also exercised
        # when allow_extract is on; when false, keep purely square-free.
        if allow_extract and random.random() < 0.55:
            return _extract_root()
        answer = (
            square_root_latex(1, leftover) if include_answer_key else None
        )
        return f"\\sqrt{{{leftover}}}", f"sqrt({leftover})", answer

    def build() -> tuple[str, str, str | None]:
        mode = random.choice(modes)
        if mode == "square":
            n = random.randint(base_lo, base_hi)
            return _square_prompt(n)

        if perfect_only:
            n = random.randint(base_lo, base_hi)
            return _perfect_root(n)

        # Hard: mix large perfects with non-perfect / extractable radicals.
        # Bias toward non-perfect / extract so Hard is visibly not "just bigger
        # perfect squares."
        roll = random.random()
        if roll < 0.22:
            n = random.randint(base_lo, base_hi)
            return _perfect_root(n)
        if roll < 0.40:
            n = random.randint(base_lo, base_hi)
            return _square_prompt(n)
        return _non_perfect_root()

    return make_questions(topic, count, include_answer_key, build, settings=settings)


GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = {
    "sets_of_numbers": sets_of_numbers,
    "rational_add_subtract": rational_add_subtract,
    "pa_integers_adding_and_subtracting": pa_integers_adding_and_subtracting,
    "rational_multiply": rational_multiply,
    "rational_divide": rational_divide,
    "distributive_property": distributive_property,
    "distributive_property_algebraic": distributive_property_algebraic,
    "percents": percents,
    "percent_of_change": percent_of_change,
    "converting_fractions_and_decimals": converting_fractions_and_decimals,
    "fractions_decimals_and_percents": fractions_decimals_and_percents,
    "pa_fractions_decimals_and_percents": fractions_decimals_and_percents,
    "solving_proportions": solving_proportions,
    "scientific_notation_write": scientific_notation_write,
    "scientific_notation_operations": scientific_notation_operations,
    "scientific_notation_add_subtract": scientific_notation_add_subtract,
    "g6_introduction_to_ratios": g6_introduction_to_ratios,
    "g6_equivalent_ratios": g6_equivalent_ratios,
    "g6_unit_rates": g6_unit_rates,
    "g6_decimal_addition": g6_decimal_addition,
    "g6_decimal_subtraction": g6_decimal_subtraction,
    "g6_decimal_multiplication": g6_decimal_multiplication,
    "order_of_operations": order_of_operations,
    "pa_squares_and_square_roots": pa_squares_and_square_roots,
}
