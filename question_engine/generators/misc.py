"""Simple generators for high-value scaffold types."""

from __future__ import annotations

import random
from typing import Callable

from packages.polynomial_core import Polynomial

from ..core.models import Question
from ..settings.enrichment import random_term_count
from .utils import _make_questions

_VERBAL_TEMPLATES: list[tuple[str, str, str]] = [
    ("\\text{{the sum of }} {a} \\text{{ and a number}}", "the sum of {a} and a number", "{a} + x"),
    ("\\text{{}} {a} \\text{{ more than a number}}", "{a} more than a number", "x + {a}"),
    ("\\text{{}} {a} \\text{{ less than a number}}", "{a} less than a number", "x - {a}"),
    ("\\text{{the product of }} {a} \\text{{ and a number}}", "the product of {a} and a number", "{a}x"),
    ("\\text{{a number divided by }} {a}", "a number divided by {a}", "\\frac{{x}}{{{a}}}"),
    ("\\text{{}} {a} \\text{{ times a number}}", "{a} times a number", "{a}x"),
    ("\\text{{a number increased by }} {a}", "a number increased by {a}", "x + {a}"),
    ("\\text{{a number decreased by }} {a}", "a number decreased by {a}", "x - {a}"),
    ("\\text{{the quotient of a number and }} {a}", "the quotient of a number and {a}", "\\frac{{x}}{{{a}}}"),
    ("\\text{{}} {a} \\text{{ less than twice a number}}", "{a} less than twice a number", "2x - {a}"),
]


_VERBAL_ADVANCED_TEMPLATES: list[tuple[str, str, str]] = [
    ("\\text{{}} {a} \\text{{ less than twice a number}}", "{a} less than twice a number", "2x - {a}"),
    ("\\text{{the sum of a number and }} {a} \\text{{, divided by }} {b}", "sum and quotient", "\\frac{{x + {a}}}{{{b}}}"),
]


def _templates_for_complexity(complexity: str, *, max_operations: int) -> list[tuple[str, str, str]]:
    if complexity == "simple":
        pool = _VERBAL_TEMPLATES[:4]
    elif complexity == "advanced":
        pool = _VERBAL_TEMPLATES + _VERBAL_ADVANCED_TEMPLATES
    else:
        pool = _VERBAL_TEMPLATES[:8]
    if max_operations <= 1:
        return pool[:4]
    if max_operations == 2:
        return pool[:8]
    return pool


def _verbal_expressions(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = misc_expression_params_from_settings(settings)
    templates = _templates_for_complexity(
        params.phrase_complexity,
        max_operations=params.max_phrase_operations,
    )

    def build() -> tuple[str, str, str | None]:
        if params.allow_fraction_constants:
            a_num = random.randint(params.constant_min, params.constant_max)
            a_den = random.randint(2, max(2, params.constant_max // 2))
            a = f"\\frac{{{a_num}}}{{{a_den}}}"
            a_text = f"{a_num}/{a_den}"
        else:
            a_val = random.randint(params.constant_min, params.constant_max)
            a = str(a_val)
            a_text = str(a_val)
        latex_tpl, text_tpl, answer_tpl = random.choice(templates)
        b = random.randint(2, max(2, params.constant_min))
        prompt_latex = latex_tpl.format(a=a, b=b)
        prompt_text = text_tpl.format(a=a_text, b=b)
        answer = answer_tpl.format(a=a, b=b) if include_answer_key else None
        return prompt_latex, prompt_text, answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _polynomial_naming(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = polynomial_params_from_settings(settings)

    def build() -> tuple[str, str, str | None]:
        degree = random.randint(params.min_degree, params.max_degree)
        poly = Polynomial.random_polynomial(
            degree,
            params.coef_min,
            params.coef_max,
            positive_leading=params.positive_leading,
        )
        names = {0: "constant", 1: "linear", 2: "quadratic", 3: "cubic", 4: "quartic"}
        answer = names.get(degree, f"degree-{degree}") if include_answer_key else None
        return poly.to_latex(), str(poly), answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _combining_like_terms(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = misc_expression_params_from_settings(settings)
    variable = params.variable

    def build() -> tuple[str, str, str | None]:
        term_count = max(2, random_term_count(settings, default=params.term_count))
        like_pairs = max(1, term_count // 2)
        terms: list[str] = []
        total_coeff = 0
        total_const = 0

        for _ in range(like_pairs):
            coeff = random.randint(max(1, params.coef_min), max(2, params.coef_max))
            terms.append(f"{coeff}{variable}")
            total_coeff += coeff
            repeat = random.randint(1, max(1, term_count - len(terms)))
            for _ in range(repeat):
                if len(terms) >= term_count:
                    break
                delta = random.randint(1, max(1, params.coef_max // 2))
                terms.append(f"{delta}{variable}")
                total_coeff += delta

        while len(terms) < term_count:
            const = random.randint(params.coef_min, params.coef_max)
            terms.append(str(const))
            total_const += const

        random.shuffle(terms)
        prompt = " + ".join(terms).replace("+ -", "- ")
        if total_const == 0:
            answer = f"{total_coeff}{variable}" if include_answer_key else None
        elif total_const > 0:
            answer = f"{total_coeff}{variable} + {total_const}" if include_answer_key else None
        else:
            answer = f"{total_coeff}{variable} - {abs(total_const)}" if include_answer_key else None
        return prompt, prompt, answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


def _properties_of_exponents(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = misc_expression_params_from_settings(settings)
    ops = allowed_rational_operations(settings)

    def build() -> tuple[str, str, str | None]:
        patterns = ["product", "quotient", "power", "negative"]
        if "+" in ops or "-" in ops:
            patterns.append("sum")
        pattern = random.choice(patterns)
        base = random.choice([params.variable, "y", "a"])
        exp_lo, exp_hi = params.exponent_min, params.exponent_max
        if pattern == "product":
            m, n = random.randint(exp_lo, exp_hi), random.randint(exp_lo, exp_hi)
            prompt = f"{base}^{{{m}}} \\cdot {base}^{{{n}}}"
            answer = f"{base}^{{{m + n}}}" if include_answer_key else None
        elif pattern == "quotient":
            m, n = random.randint(exp_lo + 1, exp_hi + 2), random.randint(exp_lo, exp_hi)
            prompt = f"\\frac{{{base}^{{{m}}}}}{{{base}^{{{n}}}}}"
            answer = f"{base}^{{{m - n}}}" if include_answer_key else None
        elif pattern == "power":
            m, n = random.randint(exp_lo, exp_hi), random.randint(exp_lo, min(exp_hi, 4))
            prompt = f"\\left({base}^{{{m}}}\\right)^{{{n}}}"
            answer = f"{base}^{{{m * n}}}" if include_answer_key else None
        elif pattern == "sum":
            m, n = random.randint(exp_lo, exp_hi), random.randint(exp_lo, exp_hi)
            op = random.choice(ops)
            prompt = f"{base}^{{{m}}} {op} {base}^{{{n}}}"
            answer = prompt if include_answer_key else None
        else:
            n = random.randint(exp_lo, exp_hi)
            prompt = f"{base}^{{-{n}}}"
            answer = f"\\frac{{1}}{{{base}^{{{n}}}}}" if include_answer_key else None
        return prompt, prompt.replace("\\", ""), answer

    return _make_questions(topic, count, include_answer_key, build, settings=settings)


GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = {
    "verbal_expressions": _verbal_expressions,
    "pa_verbal_expressions": _verbal_expressions,
    "g6_writing_algebraic_expressions": _verbal_expressions,
    "polynomial_naming": _polynomial_naming,
    "combining_like_terms": _combining_like_terms,
    "g6_combining_like_terms": _combining_like_terms,
    "properties_of_exponents": _properties_of_exponents,
}
