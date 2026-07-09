"""Precalculus generators: trigonometry, logarithms, exponentials, sequences."""

from __future__ import annotations

import math
import random
from fractions import Fraction
from typing import Callable

from ..core.models import Question
from ..settings.params import (
    exponential_params_from_settings,
    logarithm_params_from_settings,
    sequence_params_from_settings,
    trigonometry_params_from_settings,
)
from .utils import _make_questions, random_int_range

# Standard unit-circle angles (degrees) and exact values
_UNIT_CIRCLE_DEG: dict[int, tuple[str, str, str]] = {
    0: (r"0", r"1", r"0"),
    30: (r"\frac{1}{2}", r"\frac{\sqrt{3}}{2}", r"\frac{\sqrt{3}}{3}"),
    45: (r"\frac{\sqrt{2}}{2}", r"\frac{\sqrt{2}}{2}", "1"),
    60: (r"\frac{\sqrt{3}}{2}", r"\frac{1}{2}", r"\sqrt{3}"),
    90: (r"1", r"0", r"\infty"),
    120: (r"\frac{\sqrt{3}}{2}", r"-\frac{1}{2}", r"-\sqrt{3}"),
    135: (r"\frac{\sqrt{2}}{2}", r"-\frac{\sqrt{2}}{2}", "-1"),
    150: (r"\frac{1}{2}", r"-\frac{\sqrt{3}}{2}", r"-\frac{\sqrt{3}}{3}"),
    180: (r"0", r"-1", r"0"),
    210: (r"-\frac{1}{2}", r"-\frac{\sqrt{3}}{2}", r"\frac{\sqrt{3}}{3}"),
    225: (r"-\frac{\sqrt{2}}{2}", r"-\frac{\sqrt{2}}{2}", "1"),
    240: (r"-\frac{\sqrt{3}}{2}", r"-\frac{1}{2}", r"\sqrt{3}"),
    270: (r"-1", r"0", r"\infty"),
    300: (r"-\frac{\sqrt{3}}{2}", r"\frac{1}{2}", r"-\sqrt{3}"),
    315: (r"-\frac{\sqrt{2}}{2}", r"\frac{\sqrt{2}}{2}", "-1"),
    330: (r"-\frac{1}{2}", r"\frac{\sqrt{3}}{2}", r"-\frac{\sqrt{3}}{3}"),
    360: (r"0", r"1", r"0"),
}

_RADIAN_LABELS: dict[int, str] = {
    0: "0",
    30: r"\frac{\pi}{6}",
    45: r"\frac{\pi}{4}",
    60: r"\frac{\pi}{3}",
    90: r"\frac{\pi}{2}",
    120: r"\frac{2\pi}{3}",
    135: r"\frac{3\pi}{4}",
    150: r"\frac{5\pi}{6}",
    180: r"\pi",
    210: r"\frac{7\pi}{6}",
    225: r"\frac{5\pi}{4}",
    240: r"\frac{4\pi}{3}",
    270: r"\frac{3\pi}{2}",
    300: r"\frac{5\pi}{3}",
    315: r"\frac{7\pi}{4}",
    330: r"\frac{11\pi}{6}",
    360: r"2\pi",
}


def _pick_unit_circle_angle(params) -> tuple[int, str]:
    candidates = [deg for deg in _UNIT_CIRCLE_DEG if params.angle_min <= deg <= params.angle_max]
    if not candidates:
        candidates = list(_UNIT_CIRCLE_DEG)
    deg = random.choice(candidates)
    if params.angle_unit == "radians":
        return deg, _RADIAN_LABELS[deg]
    if params.angle_unit == "both" and random.choice([True, False]):
        return deg, _RADIAN_LABELS[deg]
    return deg, rf"{deg}^\circ"


def _trig_fn_latex(fn: str, angle_latex: str) -> str:
    return f"\\{fn}\\left({angle_latex}\\right)"


def _trig_evaluate(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = trigonometry_params_from_settings(settings)

    def build() -> tuple[str, str, str | None]:
        deg, angle_latex = _pick_unit_circle_angle(params)
        fn = random.choice(params.functions)
        sin_v, cos_v, tan_v = _UNIT_CIRCLE_DEG[deg]
        values = {"sin": sin_v, "cos": cos_v, "tan": tan_v, "cot": tan_v}
        if fn == "cot" and tan_v in ("0", r"\infty"):
            fn = random.choice(["sin", "cos"])
        prompt = _trig_fn_latex(fn, angle_latex)
        answer = values[fn] if include_answer_key else None
        return prompt, f"{fn}({deg}°)", answer

    return _make_questions(topic, count, include_answer_key, build)


def _trig_unit_circle(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = trigonometry_params_from_settings(settings)

    def build() -> tuple[str, str, str | None]:
        deg, angle_latex = _pick_unit_circle_angle(params)
        fn = random.choice([f for f in ("sin", "cos") if f in params.functions] or ["sin", "cos"])
        sin_v, cos_v, _ = _UNIT_CIRCLE_DEG[deg]
        value = sin_v if fn == "sin" else cos_v
        if random.choice([True, False]):
            prompt = (
                f"\\text{{Find }} {_trig_fn_latex(fn, angle_latex)} "
                f"\\text{{ on the unit circle.}}"
            )
            answer = value if include_answer_key else None
            label = f"unit circle {fn} at {deg}°"
        else:
            prompt = (
                f"\\text{{An angle on the unit circle has }} \\{fn} = {value}. "
                f"\\text{{Which standard angle (in degrees) has this value?}}"
            )
            answer = str(deg) if include_answer_key else None
            label = f"unit circle angle for {fn}={value}"
        return prompt, label, answer

    return _make_questions(topic, count, include_answer_key, build)


def _trig_basic_identities(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = trigonometry_params_from_settings(settings)

    identities: list[tuple[str, str]] = []
    if params.allow_pythagorean_identities:
        identities.extend(
            [
                (r"\sin^2 \theta + \cos^2 \theta", "1"),
                (r"\sec^2 \theta - \tan^2 \theta", "1"),
                (r"1 + \cot^2 \theta", r"\csc^2 \theta"),
            ]
        )
    if params.allow_reciprocal_identities:
        identities.extend(
            [
                (r"\tan \theta", r"\frac{\sin \theta}{\cos \theta}"),
                (r"\cot \theta", r"\frac{\cos \theta}{\sin \theta}"),
                (r"\sec \theta", r"\frac{1}{\cos \theta}"),
                (r"\csc \theta", r"\frac{1}{\sin \theta}"),
            ]
        )
    if not identities:
        identities = [(r"\sin^2 \theta + \cos^2 \theta", "1")]

    def build() -> tuple[str, str, str | None]:
        lhs, rhs = random.choice(identities)
        if random.choice([True, False]):
            prompt = f"\\text{{Simplify: }} {lhs}"
            answer = rhs if include_answer_key else None
        else:
            prompt = f"\\text{{Rewrite using a fundamental identity: }} {lhs} = {rhs}"
            answer = lhs if include_answer_key else None
        return prompt, "trig identity", answer

    return _make_questions(topic, count, include_answer_key, build)


def _random_log_base(params) -> tuple[int | str, str]:
    choices: list[tuple[int | str, str]] = []
    lo, hi = params.base_min, params.base_max
    for base in range(lo, hi + 1):
        choices.append((base, str(base)))
    if params.allow_common_log:
        choices.append(("10", r"10"))
    if params.allow_natural_log:
        choices.append(("e", "e"))
    return random.choice(choices or [(2, "2")])


def _log_base_latex(base_key: int | str, base_label: str) -> str:
    if base_key == "e":
        return r"\ln"
    if base_key == "10":
        return r"\log"
    return rf"\log_{{{base_label}}}"


def _log_evaluate(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = logarithm_params_from_settings(settings)

    def build() -> tuple[str, str, str | None]:
        base_key, base_label = _random_log_base(params)
        if params.require_integer_result:
            exponent = random.randint(1, 6)
            if isinstance(base_key, int):
                argument = base_key**exponent
            elif base_key == "e":
                argument = round(math.e**exponent, 4)
                exponent = exponent
            else:
                argument = 10**exponent
            answer_value = str(exponent)
        else:
            argument = random.randint(params.argument_min, params.argument_max)
            if isinstance(base_key, int):
                answer_value = f"{math.log(argument, base_key):.3g}"
            elif base_key == "e":
                answer_value = f"{math.log(argument):.3g}"
            else:
                answer_value = f"{math.log10(argument):.3g}"
        log_latex = _log_base_latex(base_key, base_label)
        prompt = f"{log_latex}\\left({argument}\\right)"
        answer = answer_value if include_answer_key else None
        return prompt, f"log eval base={base_label}", answer

    return _make_questions(topic, count, include_answer_key, build)


def _log_change_of_base(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = logarithm_params_from_settings(settings)

    def build() -> tuple[str, str, str | None]:
        base = random.randint(params.base_min, params.base_max)
        exponent = random.randint(2, 5)
        argument = base**exponent
        new_base = random.randint(params.base_min, params.base_max)
        while new_base == base:
            new_base = random.randint(params.base_min, params.base_max)
        prompt = (
            f"\\text{{Rewrite using change of base: }} "
            f"\\log_{{{base}}}({argument})"
        )
        answer = (
            rf"\frac{{\log_{{{new_base}}}({argument})}}{{\log_{{{new_base}}}({base})}}"
            if include_answer_key
            else None
        )
        return prompt, "change of base", answer

    return _make_questions(topic, count, include_answer_key, build)


def _log_equation_simple(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = logarithm_params_from_settings(settings)

    def build() -> tuple[str, str, str | None]:
        base_key, base_label = _random_log_base(params)
        exponent = random.randint(1, 5)
        if isinstance(base_key, int):
            solution = base_key**exponent
        elif base_key == "e":
            solution = round(math.e**exponent, 4)
        else:
            solution = 10**exponent
        log_latex = _log_base_latex(base_key, base_label)
        prompt = f"{log_latex}(x) = {exponent}"
        answer = f"x = {solution}" if include_answer_key else None
        return prompt, "log equation", answer

    return _make_questions(topic, count, include_answer_key, build)


def _exponential_equation_simple(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = exponential_params_from_settings(settings)

    def build() -> tuple[str, str, str | None]:
        base = random.randint(params.base_min, params.base_max)
        exponent = random.randint(params.exponent_min, params.exponent_max)
        rhs = base**exponent
        prompt = f"{base}^{{x}} = {rhs}"
        answer = f"x = {exponent}" if include_answer_key else None
        return prompt, "exponential equation", answer

    return _make_questions(topic, count, include_answer_key, build)


def _exponential_equation_with_log(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = exponential_params_from_settings(settings)

    def build() -> tuple[str, str, str | None]:
        base = random.randint(params.base_min, params.base_max)
        coef = random_int_range(params.coef_min, params.coef_max, exclude={0})
        exponent = random.randint(params.exponent_min, params.exponent_max)
        rhs = base ** (coef * exponent)
        prompt = f"{base}^{{{coef}x}} = {rhs}"
        answer = f"x = {exponent}" if include_answer_key else None
        return prompt, "exponential equation with log", answer

    return _make_questions(topic, count, include_answer_key, build)


def _sequence_arithmetic_nth_term(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = sequence_params_from_settings(settings)

    def build() -> tuple[str, str, str | None]:
        a1 = random.randint(params.first_term_min, params.first_term_max)
        d = random.randint(params.common_diff_min, params.common_diff_max)
        while d == 0:
            d = random.randint(params.common_diff_min, params.common_diff_max)
        n = random.randint(params.nth_min, params.nth_max)
        an = a1 + (n - 1) * d
        prompt = (
            f"\\text{{Find the }} {n}^{{\\text{{th}}}} \\text{{ term of the arithmetic sequence "
            f"with }} a_1 = {a1} \\text{{ and }} d = {d}."
        )
        answer = str(an) if include_answer_key else None
        return prompt, f"arithmetic a_{n}", answer

    return _make_questions(topic, count, include_answer_key, build)


def _sequence_geometric_nth_term(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = sequence_params_from_settings(settings)

    def build() -> tuple[str, str, str | None]:
        a1 = random.randint(params.first_term_min, params.first_term_max)
        if a1 == 0:
            a1 = 1
        lo, hi = params.common_ratio_min, params.common_ratio_max
        if not params.allow_negative_ratio:
            lo, hi = max(1, lo), max(1, hi)
        r = random.randint(lo, hi)
        while r in (0, 1):
            r = random.randint(lo, hi)
        n = random.randint(params.nth_min, params.nth_max)
        an = a1 * (r ** (n - 1))
        prompt = (
            f"\\text{{Find the }} {n}^{{\\text{{th}}}} \\text{{ term of the geometric sequence "
            f"with }} a_1 = {a1} \\text{{ and }} r = {r}."
        )
        answer = str(an) if include_answer_key else None
        return prompt, f"geometric a_{n}", answer

    return _make_questions(topic, count, include_answer_key, build)


GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = {
    "trig_evaluate": _trig_evaluate,
    "trig_unit_circle": _trig_unit_circle,
    "trig_basic_identities": _trig_basic_identities,
    "log_evaluate": _log_evaluate,
    "log_change_of_base": _log_change_of_base,
    "log_equation_simple": _log_equation_simple,
    "exponential_equation_simple": _exponential_equation_simple,
    "exponential_equation_with_log": _exponential_equation_with_log,
    "sequence_arithmetic_nth_term": _sequence_arithmetic_nth_term,
    "sequence_geometric_nth_term": _sequence_geometric_nth_term,
}
