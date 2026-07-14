"""Simple generators for high-value scaffold types."""

from __future__ import annotations

import random
from typing import Callable

from packages.polynomial_core import Polynomial, format_monomial_latex

from ..core.models import Question
from ..settings.enrichment import random_term_count
from ..settings.params import (
    allowed_rational_operations,
    misc_expression_params_from_settings,
    polynomial_params_from_settings,
)
from .utils import _make_questions, format_slash_fraction

def _verbal_constant(params, *, variable: str = "x") -> tuple[str, str, str]:
    """Return (latex, plain_text, ax_latex) for one constant."""
    if params.allow_fraction_constants and random.random() < 0.35:
        a_num = random.randint(params.constant_min, params.constant_max)
        a_den = random.randint(2, max(2, params.constant_max // 2))
        a = f"\\frac{{{a_num}}}{{{a_den}}}"
        return a, format_slash_fraction(a_num, a_den), f"{a}{variable}"
    a_val = random.randint(params.constant_min, params.constant_max)
    return (
        str(a_val),
        str(a_val),
        format_monomial_latex(a_val, variable=variable) or "0",
    )


def _verbal_expressions(topic: str, settings: dict) -> list[Question]:
    """Translate verbal phrases into algebraic expressions.

    Tiered like writing numeric expressions:
    - simple: one operation (sum/product/quotient with a variable)
    - standard: multi-step / parentheses (quantity, times the sum/difference)
    - advanced: consecutive integers, products of binomials, squared quantities
    Medium uses standard forms only (not diluted with Easy); Hard weights advanced.
    """
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = misc_expression_params_from_settings(settings)
    var = params.variable
    complexity = params.phrase_complexity
    max_ops = params.max_phrase_operations

    def _c() -> tuple[str, str, str]:
        return _verbal_constant(params, variable=var)

    def _second() -> tuple[str, str]:
        b_val = random.randint(params.constant_min, params.constant_max)
        if b_val == 0:
            b_val = max(2, params.constant_min)
        return str(b_val), str(b_val)

    def simple_forms() -> list[tuple[str, str, str]]:
        a, a_text, ax = _c()
        return [
            (
                f"\\text{{the sum of }} {a} \\text{{ and a number}}",
                f"the sum of {a_text} and a number",
                f"{a} + {var}",
            ),
            (
                f"\\text{{}} {a} \\text{{ more than a number}}",
                f"{a_text} more than a number",
                f"{var} + {a}",
            ),
            (
                f"\\text{{}} {a} \\text{{ less than a number}}",
                f"{a_text} less than a number",
                f"{var} - {a}",
            ),
            (
                f"\\text{{the product of }} {a} \\text{{ and a number}}",
                f"the product of {a_text} and a number",
                ax,
            ),
            (
                f"\\text{{}} {a} \\text{{ times a number}}",
                f"{a_text} times a number",
                ax,
            ),
            (
                f"\\text{{a number increased by }} {a}",
                f"a number increased by {a_text}",
                f"{var} + {a}",
            ),
            (
                f"\\text{{a number decreased by }} {a}",
                f"a number decreased by {a_text}",
                f"{var} - {a}",
            ),
            (
                f"\\text{{a number divided by }} {a}",
                f"a number divided by {a_text}",
                f"\\frac{{{var}}}{{{a}}}",
            ),
            (
                f"\\text{{the quotient of a number and }} {a}",
                f"the quotient of a number and {a_text}",
                f"\\frac{{{var}}}{{{a}}}",
            ),
            (
                f"\\text{{the difference of a number and }} {a}",
                f"the difference of a number and {a_text}",
                f"{var} - {a}",
            ),
            (
                f"\\text{{twice a number}}",
                "twice a number",
                f"2{var}",
            ),
            (
                f"\\text{{}} {a} \\text{{ fewer than a number}}",
                f"{a_text} fewer than a number",
                f"{var} - {a}",
            ),
        ]

    def standard_forms() -> list[tuple[str, str, str]]:
        a, a_text, _ax = _c()
        b, b_text = _second()
        bx = format_monomial_latex(int(b), variable=var) if b.isdigit() else f"{b}{var}"
        if not bx:
            bx = f"{b}{var}"
        return [
            (
                f"\\text{{}} {a} \\text{{ less than twice a number}}",
                f"{a_text} less than twice a number",
                f"2{var} - {a}",
            ),
            (
                f"\\text{{}} {a} \\text{{ more than twice a number}}",
                f"{a_text} more than twice a number",
                f"2{var} + {a}",
            ),
            (
                f"\\text{{}} {a} \\text{{ times the sum of a number and }} {b}",
                f"{a_text} times the sum of a number and {b_text}",
                f"{a}({var} + {b})",
            ),
            (
                f"\\text{{}} {a} \\text{{ times the difference of a number and }} {b}",
                f"{a_text} times the difference of a number and {b_text}",
                f"{a}({var} - {b})",
            ),
            (
                f"\\text{{the product of }} {a} \\text{{ and the sum of a number and }} {b}",
                f"the product of {a_text} and the sum of a number and {b_text}",
                f"{a}({var} + {b})",
            ),
            (
                f"\\text{{the sum of a number and }} {a} \\text{{, divided by }} {b}",
                f"the sum of a number and {a_text}, divided by {b_text}",
                f"\\frac{{{var} + {a}}}{{{b}}}",
            ),
            (
                f"\\text{{the quotient of the sum of a number and }} {a}\\text{{, and }} {b}",
                f"the quotient of the sum of a number and {a_text}, and {b_text}",
                f"\\frac{{{var} + {a}}}{{{b}}}",
            ),
            (
                f"\\text{{}} {a} \\text{{ more than the product of }} {b} \\text{{ and a number}}",
                f"{a_text} more than the product of {b_text} and a number",
                f"{bx} + {a}",
            ),
            (
                f"\\text{{}} {a} \\text{{ less than the product of }} {b} \\text{{ and a number}}",
                f"{a_text} less than the product of {b_text} and a number",
                f"{bx} - {a}",
            ),
            (
                f"\\text{{}} {a} \\text{{ times the quantity of a number plus }} {b}",
                f"{a_text} times the quantity of a number plus {b_text}",
                f"{a}({var} + {b})",
            ),
            (
                f"\\text{{}} {a} \\text{{ times the quantity of a number minus }} {b}",
                f"{a_text} times the quantity of a number minus {b_text}",
                f"{a}({var} - {b})",
            ),
            (
                f"\\text{{the difference of }} {a} \\text{{ and the product of }} {b} "
                f"\\text{{ and a number}}",
                f"the difference of {a_text} and the product of {b_text} and a number",
                f"{a} - {bx}",
            ),
            (
                f"\\text{{}} {b} \\text{{ groups of the sum of a number and }} {a}",
                f"{b_text} groups of the sum of a number and {a_text}",
                f"{b}({var} + {a})",
            ),
            (
                f"\\text{{the sum of }} {a} \\text{{ and the product of }} {b} "
                f"\\text{{ and a number}}",
                f"the sum of {a_text} and the product of {b_text} and a number",
                f"{a} + {bx}",
            ),
            (
                f"\\text{{}} {a} \\text{{ times the quantity of twice a number plus }} {b}",
                f"{a_text} times the quantity of twice a number plus {b_text}",
                f"{a}(2{var} + {b})",
            ),
            (
                f"\\text{{the sum of a number and }} {a}\\text{{, multiplied by }} {b}",
                f"the sum of a number and {a_text}, multiplied by {b_text}",
                f"{b}({var} + {a})",
            ),
            (
                f"\\text{{twice the quantity of a number decreased by }} {a}",
                f"twice the quantity of a number decreased by {a_text}",
                f"2({var} - {a})",
            ),
            (
                f"\\text{{}} {a} \\text{{ less than twice the quantity of a number plus }} {b}",
                f"{a_text} less than twice the quantity of a number plus {b_text}",
                f"2({var} + {b}) - {a}",
            ),
        ]

    def advanced_forms() -> list[tuple[str, str, str]]:
        a, a_text, _ax = _c()
        b, b_text = _second()
        # Keep a,b distinct for binomial products / consecutive phrasing clarity.
        if a == b:
            b_val = int(b) + 1 if b.isdigit() else params.constant_max
            b, b_text = str(b_val), str(b_val)
        return [
            (
                f"\\text{{the product of a number plus }} {a} \\text{{ and a number plus }} {b}",
                f"the product of a number plus {a_text} and a number plus {b_text}",
                f"({var} + {a})({var} + {b})",
            ),
            (
                f"\\text{{the product of a number minus }} {a} \\text{{ and a number plus }} {b}",
                f"the product of a number minus {a_text} and a number plus {b_text}",
                f"({var} - {a})({var} + {b})",
            ),
            (
                f"\\text{{the product of the quantity a number plus }} {a} "
                f"\\text{{ and the quantity a number minus }} {b}",
                f"the product of the quantity a number plus {a_text} "
                f"and the quantity a number minus {b_text}",
                f"({var} + {a})({var} - {b})",
            ),
            (
                f"\\text{{the square of the sum of a number and }} {a}",
                f"the square of the sum of a number and {a_text}",
                f"({var} + {a})^{{2}}",
            ),
            (
                f"\\text{{the square of the difference of a number and }} {a}",
                f"the square of the difference of a number and {a_text}",
                f"({var} - {a})^{{2}}",
            ),
            (
                f"\\text{{a number squared plus }} {a}",
                f"a number squared plus {a_text}",
                f"{var}^{{2}} + {a}",
            ),
            (
                f"\\text{{}} {a} \\text{{ times the quantity of a number squared plus }} {b}",
                f"{a_text} times the quantity of a number squared plus {b_text}",
                f"{a}({var}^{{2}} + {b})",
            ),
            (
                f"\\text{{twice the quantity of a number increased by }} {a}",
                f"twice the quantity of a number increased by {a_text}",
                f"2({var} + {a})",
            ),
            (
                f"\\text{{the sum of the squares of a number and }} {a}",
                f"the sum of the squares of a number and {a_text}",
                f"{var}^{{2}} + {a}^{{2}}",
            ),
            (
                f"\\text{{the sum of three consecutive integers starting with a number}}",
                "the sum of three consecutive integers starting with a number",
                f"{var} + ({var} + 1) + ({var} + 2)",
            ),
            (
                f"\\text{{the sum of two consecutive integers starting with a number}}",
                "the sum of two consecutive integers starting with a number",
                f"{var} + ({var} + 1)",
            ),
            (
                f"\\text{{the sum of three consecutive even integers starting with a number}}",
                "the sum of three consecutive even integers starting with a number",
                f"{var} + ({var} + 2) + ({var} + 4)",
            ),
            (
                f"\\text{{the sum of three consecutive odd integers starting with a number}}",
                "the sum of three consecutive odd integers starting with a number",
                f"{var} + ({var} + 2) + ({var} + 4)",
            ),
            (
                f"\\text{{}} {a} \\text{{ less than the square of a number}}",
                f"{a_text} less than the square of a number",
                f"{var}^{{2}} - {a}",
            ),
            (
                f"\\text{{the product of }} {a} \\text{{ and the square of the sum of a number "
                f"and }} {b}",
                f"the product of {a_text} and the square of the sum of a number and {b_text}",
                f"{a}({var} + {b})^{{2}}",
            ),
            (
                f"\\text{{the cube of a number increased by }} {a}",
                f"the cube of a number increased by {a_text}",
                f"{var}^{{3}} + {a}",
            ),
            (
                f"\\text{{the quotient of }} {a} \\text{{ times a number and the quantity of a "
                f"number plus }} {b}",
                f"the quotient of {a_text} times a number and the quantity of a number plus {b_text}",
                f"\\frac{{{_ax}}}{{{var} + {b}}}",
            ),
        ]

    if complexity == "simple" or max_ops <= 1:
        pool_builders = [simple_forms]
    elif complexity == "advanced" or max_ops >= 3:
        # Hard: nested / exponent / consecutive, with some medium variety.
        pool_builders = [standard_forms, advanced_forms, advanced_forms]
    else:
        # Medium: multi-op / grouping only — do not dilute with Easy one-ops.
        pool_builders = [standard_forms]

    def build() -> tuple[str, str, str | None]:
        forms: list[tuple[str, str, str]] = []
        for builder in pool_builders:
            forms.extend(builder())
        prompt_latex, prompt_text, answer_expr = random.choice(forms)
        answer = answer_expr if include_answer_key else None
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
        names = {
            0: r"\text{constant}",
            1: r"\text{linear}",
            2: r"\text{quadratic}",
            3: r"\text{cubic}",
            4: r"\text{quartic}",
        }
        answer = names.get(degree, rf"\text{{degree-{degree}}}") if include_answer_key else None
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
