"""Shared generation utilities for question builders."""

from __future__ import annotations

import random
import uuid
from fractions import Fraction
from typing import Any, Callable

from packages.polynomial_core import (
    format_binop_expression,
    format_linear_latex,
    format_measurement_text,
    format_monomial_latex,
    format_polynomial_latex,
    format_slash_fraction,
    format_slope_intercept_latex,
    format_with_unit,
    join_algebra_terms,
    normalize_expression_signs,
    paren_if_negative,
    unit_latex,
)

from ..core.models import Question

# Re-export polynomial term formatters for generator convenience.
__all_formatters__ = (
    "format_binop_expression",
    "format_linear_latex",
    "format_measurement_text",
    "format_monomial_latex",
    "format_polynomial_latex",
    "format_slash_fraction",
    "format_slope_intercept_latex",
    "format_with_unit",
    "join_algebra_terms",
    "normalize_expression_signs",
    "paren_if_negative",
    "unit_latex",
)


def frac_latex(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    if value.numerator < 0:
        return f"-\\frac{{{abs(value.numerator)}}}{{{value.denominator}}}"
    return f"\\frac{{{value.numerator}}}{{{value.denominator}}}"


def mixed_number_latex(value: Fraction) -> str:
    """Format ``value`` as a mixed number when improper; otherwise a proper fraction."""
    if value.denominator == 1:
        return str(value.numerator)
    sign = "-" if value < 0 else ""
    num = abs(value.numerator)
    den = value.denominator
    whole, rem = divmod(num, den)
    if whole == 0:
        return f"{sign}\\frac{{{rem}}}{{{den}}}"
    if rem == 0:
        return f"{sign}{whole}"
    return f"{sign}{whole}\\frac{{{rem}}}{{{den}}}"


def frac_or_mixed_latex(value: Fraction, *, allow_mixed: bool) -> str:
    if allow_mixed and abs(value.numerator) > value.denominator:
        return mixed_number_latex(value)
    return frac_latex(value)


def format_fraction_division_latex(left: Fraction, right: Fraction, notation: str) -> str:
    """Render ``left ÷ right`` in the chosen division notation."""
    a = frac_latex(left)
    b = frac_latex(right)
    if notation == "complex_fraction":
        return f"\\frac{{{a}}}{{{b}}}"
    if notation == "slash":
        return f"\\left({a}\\right) / \\left({b}\\right)"
    return f"{a} \\div {b}"


def random_fraction(
    *,
    num_min: int = -10,
    num_max: int = 10,
    denom_min: int = 2,
    denom_max: int = 12,
    allow_negative: bool = True,
    require_proper: bool = False,
    allow_mixed: bool = False,
) -> Fraction:
    lo, hi = num_min, num_max
    if not allow_negative:
        lo = max(1, lo)
        hi = max(lo, hi)
    for _ in range(60):
        denominator = random.randint(denom_min, denom_max)
        if allow_mixed and not require_proper and random.random() < 0.65:
            # Build an improper fraction via mixed number (whole + proper part).
            max_whole = max(1, min(8, max(1, hi // max(denominator, 1))))
            whole = random.randint(1, max_whole)
            rem = random.randint(1, denominator - 1)
            numerator = whole * denominator + rem
            if allow_negative and lo < 0 and random.random() < 0.35:
                numerator = -numerator
            value = Fraction(numerator, denominator)
        else:
            numerator = random.randint(lo, hi)
            while numerator == 0:
                numerator = random.randint(lo, hi)
            if require_proper:
                numerator = abs(numerator) % denominator
                if numerator == 0:
                    numerator = random.randint(1, denominator - 1)
                if allow_negative and lo < 0 and random.random() < 0.35:
                    numerator = -numerator
            value = Fraction(numerator, denominator)
        # Keep true fractional operands (not whole numbers after reduction).
        if value.denominator == 1:
            continue
        if require_proper and abs(value.numerator) >= value.denominator:
            continue
        return value
    denominator = max(2, denom_min)
    return Fraction(1, denominator)


def make_questions(
    topic: str,
    count: int,
    include_answer_key: bool,
    builder: Callable[[], tuple[str, str, str | None]],
    *,
    metadata: dict[str, Any] | None = None,
    metadata_builder: Callable[[str, str, str | None], dict[str, Any]] | None = None,
    settings: dict[str, Any] | None = None,
) -> list[Question]:
    from ..settings.enrichment import merge_enrichment_metadata

    questions: list[Question] = []
    base_metadata = dict(metadata or {})
    generation_settings = settings or {}
    for _ in range(count):
        prompt_latex, prompt_text, answer = builder()
        question_metadata = dict(base_metadata)
        if metadata_builder is not None:
            question_metadata.update(metadata_builder(prompt_latex, prompt_text, answer))
        elif generation_settings:
            question_metadata = merge_enrichment_metadata(
                generation_settings,
                question_metadata,
                answer=answer,
            )
        questions.append(
            Question(
                id=str(uuid.uuid4()),
                topic=topic,
                prompt_latex=prompt_latex,
                prompt_text=prompt_text,
                answer_latex=answer if include_answer_key else None,
                metadata=question_metadata,
            )
        )
    return questions


def random_int_range(
    minimum: int,
    maximum: int,
    *,
    exclude: set[int] | None = None,
) -> int:
    while True:
        value = random.randint(minimum, maximum)
        if exclude is None or value not in exclude:
            return value


def pick_operation(operations: list[str]) -> str:
    return random.choice(operations)


def format_equation_latex(
    lhs: str,
    rhs: str,
    *,
    relation: str = "=",
) -> str:
    return f"{lhs} {relation} {rhs}"


def settings_require_monic(settings: dict[str, Any] | None) -> bool:
    """True when presets/settings force leading coefficient 1."""
    if not settings:
        return False
    return bool(settings.get("leading_coefficient_one", False)) or bool(
        settings.get("monic_only", False)
    )


def pick_quadratic_leading_coef(
    settings: dict[str, Any],
    *,
    coef_max: int,
    max_a: int = 4,
    prefer_nonunit: bool = False,
) -> int:
    """Pick leading coefficient ``a > 0`` for a quadratic equation/expression."""
    if settings_require_monic(settings):
        return 1
    hi = max(1, min(max_a, abs(int(coef_max)) or max_a))
    if prefer_nonunit and hi >= 2:
        return random.randint(2, hi)
    return random.randint(1, hi)


# Backward-compatible aliases used by generators/basic.py
_frac_latex = frac_latex
_random_fraction = random_fraction
_make_questions = make_questions
