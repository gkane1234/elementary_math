"""Calculus generators: limits, derivatives, integrals."""

from __future__ import annotations

import random
from fractions import Fraction
from typing import Callable

from ..core.models import Question
from ..settings.params import calculus_params_from_settings
from .utils import _make_questions, frac_latex, random_int_range


def _format_coef(coef: int, power: int, variable: str) -> str:
    if power == 0:
        return str(coef)
    if coef == 1:
        coef_str = ""
    elif coef == -1:
        coef_str = "-"
    else:
        coef_str = str(coef)
    if power == 1:
        return f"{coef_str}{variable}"
    return f"{coef_str}{variable}^{{{power}}}"


def _format_poly_terms(terms: list[tuple[int, int]], variable: str) -> str:
    parts: list[str] = []
    for coef, power in sorted(terms, key=lambda item: item[1], reverse=True):
        if coef == 0:
            continue
        term = _format_coef(abs(coef), power, variable)
        if not parts:
            parts.append(f"-{term}" if coef < 0 else term)
        else:
            sign = "+" if coef > 0 else "-"
            parts.append(f" {sign} {term}")
    return "".join(parts) or "0"


def _random_poly_terms(params) -> list[tuple[int, int]]:
    terms: list[tuple[int, int]] = []
    used_powers: set[int] = set()
    for _ in range(params.term_count):
        power = random.randint(params.power_min, params.power_max)
        while power in used_powers:
            power = random.randint(params.power_min, params.power_max)
        used_powers.add(power)
        coef = random_int_range(params.coef_min, params.coef_max, exclude={0})
        terms.append((coef, power))
    if params.include_constant_term and 0 not in used_powers and random.choice([True, False]):
        terms.append((random.randint(params.coef_min, params.coef_max), 0))
    return terms


def _eval_poly(terms: list[tuple[int, int]], x: int) -> int:
    return sum(coef * (x**power) for coef, power in terms)


def _limit_direct_evaluation(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = calculus_params_from_settings(settings)

    def build() -> tuple[str, str, str | None]:
        terms = _random_poly_terms(params)
        approach = random.randint(params.limit_approach_min, params.limit_approach_max)
        value = _eval_poly(terms, approach)
        poly = _format_poly_terms(terms, params.variable)
        prompt = (
            f"\\lim_{{{params.variable} \\to {approach}}} "
            f"\\left({poly}\\right)"
        )
        answer = str(value) if include_answer_key else None
        return prompt, f"limit at {approach}", answer

    return _make_questions(topic, count, include_answer_key, build)


def _limit_at_infinity(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = calculus_params_from_settings(settings)

    def build() -> tuple[str, str, str | None]:
        lead_coef = random_int_range(params.coef_min, params.coef_max, exclude={0})
        lead_power = random.randint(max(1, params.power_min), params.power_max)
        lower_power = random.randint(0, max(0, lead_power - 1))
        lower_coef = random_int_range(params.coef_min, params.coef_max, exclude={0})
        num = _format_poly_terms([(lead_coef, lead_power), (lower_coef, lower_power)], params.variable)
        den_power = random.randint(0, lead_power)
        den_coef = random_int_range(1, max(1, params.coef_max))
        den = _format_coef(den_coef, den_power, params.variable)
        infinity = random.choice([r"\infty", r"-\infty"])
        prompt = (
            f"\\lim_{{{params.variable} \\to {infinity}}} "
            f"\\frac{{{num}}}{{{den}}}"
        )
        if lead_power > den_power:
            answer = r"\infty" if (lead_coef > 0) == (infinity == r"\infty") else r"-\infty"
        elif lead_power < den_power:
            answer = "0"
        else:
            answer = frac_latex(Fraction(lead_coef, den_coef))
        if not include_answer_key:
            answer = None
        return prompt, "limit at infinity", answer

    return _make_questions(topic, count, include_answer_key, build)


def _derivative_power_rule(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = calculus_params_from_settings(settings)

    def build() -> tuple[str, str, str | None]:
        terms = _random_poly_terms(params)
        poly = _format_poly_terms(terms, params.variable)
        deriv_terms: list[tuple[int, int]] = []
        for coef, power in terms:
            if power == 0:
                continue
            deriv_terms.append((coef * power, power - 1))
        deriv = _format_poly_terms(deriv_terms, params.variable) if deriv_terms else "0"
        prompt = (
            f"\\frac{{d}}{{d{params.variable}}} "
            f"\\left({poly}\\right)"
        )
        answer = deriv if include_answer_key else None
        return prompt, "power rule derivative", answer

    return _make_questions(topic, count, include_answer_key, build)


def _integral_power_rule(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = calculus_params_from_settings(settings)

    def build() -> tuple[str, str, str | None]:
        terms = _random_poly_terms(params)
        if params.require_positive_power:
            terms = [(coef, max(1, power)) for coef, power in terms if power != 0]
            if not terms:
                terms = [(random_int_range(params.coef_min, params.coef_max, exclude={0}), 1)]
        poly = _format_poly_terms(terms, params.variable)
        integral_terms: list[str] = []
        for coef, power in terms:
            new_power = power + 1
            new_coef = Fraction(coef, new_power)
            coef_latex = frac_latex(new_coef)
            if coef_latex == "1":
                term = f"{params.variable}^{{{new_power}}}"
            elif coef_latex == "-1":
                term = f"-{params.variable}^{{{new_power}}}"
            else:
                term = f"{coef_latex}{params.variable}^{{{new_power}}}"
            integral_terms.append(term)
        if params.include_constant_term and random.choice([True, False]):
            integral_terms.append("C")
        answer_body = " + ".join(integral_terms) if integral_terms else "C"
        prompt = f"\\int {poly} \\, d{params.variable}"
        answer = answer_body if include_answer_key else None
        return prompt, "power rule integral", answer

    return _make_questions(topic, count, include_answer_key, build)


GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = {
    "limit_direct_evaluation": _limit_direct_evaluation,
    "limit_at_infinity": _limit_at_infinity,
    "derivative_power_rule": _derivative_power_rule,
    "integral_power_rule": _integral_power_rule,
}
