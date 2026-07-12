"""Precalculus generators: trigonometry, logarithms, exponentials, sequences."""

from __future__ import annotations

import math
import random
from fractions import Fraction
from typing import Any, Callable

from ..core.metadata import question_metadata
from ..core.models import Question
from ..frameworks.graphing import include_graph_metadata, origin_centered_bounds
from ..settings.params import (
    exponential_params_from_settings,
    logarithm_params_from_settings,
    sequence_params_from_settings,
    trigonometry_params_from_settings,
)
from .utils import (
    _make_questions,
    format_linear_latex,
    format_monomial_latex,
    frac_latex,
    random_int_range,
)

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


def _simple_trig_equations(topic: str, settings: dict) -> list[Question]:
    """Solve basic unit-circle trig equations like sin(x) = 1/2."""
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = trigonometry_params_from_settings(settings)

    # Exact unit-circle solutions in [0, 360) for common RHS values.
    solutions: dict[tuple[str, str], list[int]] = {
        ("sin", r"0"): [0, 180],
        ("sin", r"\frac{1}{2}"): [30, 150],
        ("sin", r"\frac{\sqrt{2}}{2}"): [45, 135],
        ("sin", r"\frac{\sqrt{3}}{2}"): [60, 120],
        ("sin", r"1"): [90],
        ("sin", r"-1"): [270],
        ("sin", r"-\frac{1}{2}"): [210, 330],
        ("sin", r"-\frac{\sqrt{2}}{2}"): [225, 315],
        ("sin", r"-\frac{\sqrt{3}}{2}"): [240, 300],
        ("cos", r"0"): [90, 270],
        ("cos", r"1"): [0],
        ("cos", r"-1"): [180],
        ("cos", r"\frac{1}{2}"): [60, 300],
        ("cos", r"\frac{\sqrt{2}}{2}"): [45, 315],
        ("cos", r"\frac{\sqrt{3}}{2}"): [30, 330],
        ("cos", r"-\frac{1}{2}"): [120, 240],
        ("cos", r"-\frac{\sqrt{2}}{2}"): [135, 225],
        ("cos", r"-\frac{\sqrt{3}}{2}"): [150, 210],
    }
    allowed_fns = [fn for fn in params.functions if fn in ("sin", "cos")]
    if not allowed_fns:
        allowed_fns = ["sin", "cos"]
    keys = [key for key in solutions if key[0] in allowed_fns]

    def _angle_latex(deg: int) -> str:
        if params.angle_unit == "radians":
            return _RADIAN_LABELS.get(deg, rf"{deg}^\circ")
        if params.angle_unit == "both" and random.choice([True, False]):
            return _RADIAN_LABELS.get(deg, rf"{deg}^\circ")
        return rf"{deg}^\circ"

    def build() -> tuple[str, str, str | None]:
        fn, rhs = random.choice(keys)
        degs = solutions[(fn, rhs)]
        prompt = f"\\{fn}(x) = {rhs}"
        if include_answer_key:
            answers = ", ".join(_angle_latex(d) for d in degs)
            answer = rf"x = {answers}"
        else:
            answer = None
        return prompt, "trig equation", answer

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
        prompt = f"{base}^{{{format_monomial_latex(coef) or '0'}}} = {rhs}"
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


def _sequence_arithmetic_geometric_mean(topic: str, settings: dict) -> list[Question]:
    """Find the arithmetic or geometric mean between two numbers."""
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        use_geo = random.choice([True, False])
        if use_geo:
            a = random.randint(1, 8)
            r = random.choice([2, 3, 4, 5])
            c = a * r * r
            prompt = (
                rf"\text{{Find the geometric mean of }} {a} \text{{ and }} {c}."
            )
            answer = str(a * r)
        else:
            a = random.randint(-10, 10)
            c = random.randint(-10, 10)
            while c == a:
                c = random.randint(-10, 10)
            prompt = (
                rf"\text{{Find the arithmetic mean of }} {a} \text{{ and }} {c}."
            )
            mean = Fraction(a + c, 2)
            answer = frac_latex(mean) if mean.denominator != 1 else str(mean.numerator)
        return prompt, "arithmetic or geometric mean", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _sequence_arithmetic_series(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = sequence_params_from_settings(settings)

    def build() -> tuple[str, str, str | None]:
        a1 = random.randint(params.first_term_min, params.first_term_max)
        d = random.randint(params.common_diff_min, params.common_diff_max)
        while d == 0:
            d = random.randint(params.common_diff_min, params.common_diff_max)
        n = random.randint(max(3, params.nth_min), max(4, params.nth_max))
        an = a1 + (n - 1) * d
        total = n * (a1 + an) // 2
        prompt = (
            rf"\text{{Find the sum of the first }} {n} \text{{ terms of the arithmetic "
            rf"sequence with }} a_1 = {a1} \text{{ and }} d = {d}."
        )
        return prompt, f"arithmetic series S_{n}", str(total) if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _sequence_geometric_series(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = sequence_params_from_settings(settings)

    def build() -> tuple[str, str, str | None]:
        a1 = random.randint(1, 5)
        r = random.choice([2, 3, -2, -3])
        n = random.randint(3, 6)
        if r == 1:
            total = n * a1
        else:
            total = a1 * (r**n - 1) // (r - 1)
        prompt = (
            rf"\text{{Find the sum of the first }} {n} \text{{ terms of the geometric "
            rf"sequence with }} a_1 = {a1} \text{{ and }} r = {r}."
        )
        return prompt, f"geometric series S_{n}", str(total) if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _trig_sum_difference(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        choice = random.choice(
            [
                (r"\sin(\alpha+\beta)", r"\sin\alpha\cos\beta+\cos\alpha\sin\beta"),
                (r"\sin(\alpha-\beta)", r"\sin\alpha\cos\beta-\cos\alpha\sin\beta"),
                (r"\cos(\alpha+\beta)", r"\cos\alpha\cos\beta-\sin\alpha\sin\beta"),
                (r"\cos(\alpha-\beta)", r"\cos\alpha\cos\beta+\sin\alpha\sin\beta"),
                (r"\tan(\alpha+\beta)", r"\frac{\tan\alpha+\tan\beta}{1-\tan\alpha\tan\beta}"),
            ]
        )
        prompt = rf"\text{{Expand }}{choice[0]}."
        return prompt, "sum/difference identity", choice[1] if keyed else None

    return _make_questions(topic, count, keyed, build, settings=settings)


def _trig_multiple_angle(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        choice = random.choice(
            [
                (r"\sin(2\theta)", r"2\sin\theta\cos\theta"),
                (r"\cos(2\theta)", r"\cos^2\theta-\sin^2\theta"),
                (r"\tan(2\theta)", r"\frac{2\tan\theta}{1-\tan^2\theta}"),
                (r"\sin\theta\cos\theta", r"\frac{1}{2}\sin(2\theta)"),
            ]
        )
        prompt = rf"\text{{Rewrite }}{choice[0]}\text{{ using a double-angle identity.}}"
        return prompt, "multiple-angle identity", choice[1] if keyed else None

    return _make_questions(topic, count, keyed, build, settings=settings)


def _trig_product_to_sum(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        choice = random.choice(
            [
                (
                    r"\sin A\cos B",
                    r"\frac{1}{2}\left[\sin(A+B)+\sin(A-B)\right]",
                ),
                (
                    r"\cos A\cos B",
                    r"\frac{1}{2}\left[\cos(A+B)+\cos(A-B)\right]",
                ),
                (
                    r"\sin A\sin B",
                    r"\frac{1}{2}\left[\cos(A-B)-\cos(A+B)\right]",
                ),
            ]
        )
        prompt = rf"\text{{Rewrite }}{choice[0]}\text{{ as a sum.}}"
        return prompt, "product-to-sum", choice[1] if keyed else None

    return _make_questions(topic, count, keyed, build, settings=settings)


def _trig_factoring_equations(topic: str, settings: dict) -> list[Question]:
    """Simple trig equations that factor with fundamental identities."""
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        choice = random.choice(["sin2", "cos2", "factor"])
        if choice == "sin2":
            prompt = r"\text{Solve }2\sin\theta\cos\theta=0\text{ for }0\le\theta<2\pi."
            answer = r"\theta=0,\frac{\pi}{2},\pi,\frac{3\pi}{2}"
        elif choice == "cos2":
            prompt = r"\text{Solve }\cos(2\theta)=0\text{ for }0\le\theta<\pi."
            answer = r"\theta=\frac{\pi}{4},\frac{3\pi}{4}"
        else:
            prompt = r"\text{Solve }2\sin^2\theta-\sin\theta=0\text{ for }0\le\theta<2\pi."
            answer = r"\theta=0,\frac{\pi}{6},\pi,\frac{5\pi}{6}"
        return prompt, "trig factoring equation", answer if keyed else None

    return _make_questions(topic, count, keyed, build, settings=settings)


def _vector_3d_basics(topic: str, settings: dict) -> list[Question]:
    """Magnitude / unit direction for 3D vectors (not cross products)."""
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        components = random.choice(
            [
                (3, 4, 0),
                (2, 3, 6),
                (1, 2, 2),
                (4, 4, 7),
                (1, 4, 8),
            ]
        )
        x, y, z = components
        mag_sq = x * x + y * y + z * z
        root = int(math.isqrt(mag_sq))
        mag = str(root) if root * root == mag_sq else rf"\sqrt{{{mag_sq}}}"
        if random.choice([True, False]):
            prompt = rf"\text{{Find the magnitude of }}\langle {x},{y},{z}\rangle."
            answer = mag
        else:
            prompt = rf"\text{{Find a unit vector in the direction of }}\langle {x},{y},{z}\rangle."
            if root * root == mag_sq:
                answer = rf"\left\langle\frac{{{x}}}{{{root}}},\frac{{{y}}}{{{root}}},\frac{{{z}}}{{{root}}}\right\rangle"
            else:
                answer = rf"\left\langle\frac{{{x}}}{{\sqrt{{{mag_sq}}}}},\frac{{{y}}}{{\sqrt{{{mag_sq}}}}},\frac{{{z}}}{{\sqrt{{{mag_sq}}}}}\right\rangle"
        return prompt, "3d vector basics", answer if keyed else None

    return _make_questions(topic, count, keyed, build, settings=settings)


def _precalc_foundations(topic: str, settings: dict) -> list[Question]:
    """Generate compact exact questions for the remaining precalculus topics."""
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        n, m = random.randint(2, 6), random.randint(2, 6)
        if "circle" in topic:
            h, k, r = random.randint(-4, 4), random.randint(-4, 4), random.randint(2, 6)
            prompt, value = (
                f"\\text{{Write the equation of the circle with center }}({h},{k})"
                f"\\text{{ and radius }}{r}.",
                rf"(x-({h}))^2+(y-({k}))^2={r**2}",
            )
        elif "ellipse" in topic:
            a, b = random.randint(3, 6), random.randint(2, 5)
            prompt, value = (
                f"\\text{{Write an ellipse centered at the origin with }}a={a}\\text{{ and }}b={b}.",
                rf"\frac{{x^2}}{{{a * a}}}+\frac{{y^2}}{{{b * b}}}=1",
            )
        elif "hyperbola" in topic:
            a, b = random.randint(2, 5), random.randint(2, 5)
            prompt, value = (
                f"\\text{{Write a horizontal hyperbola centered at the origin with }}a={a}"
                f"\\text{{ and }}b={b}.",
                rf"\frac{{x^2}}{{{a * a}}}-\frac{{y^2}}{{{b * b}}}=1",
            )
        elif "parabola" in topic:
            p = random.randint(1, 5)
            prompt, value = (
                f"\\text{{Write the equation of a parabola with vertex }}(0,0)"
                f"\\text{{ and focus }}(0,{p}).",
                rf"x^2={4 * p}y",
            )
        elif "permutation" in topic:
            total = n + m
            prompt, value = (
                f"\\text{{How many ordered selections of }}{m}\\text{{ items can be made from }}"
                f"{total}\\text{{ distinct items?}}",
                str(math.factorial(total) // math.factorial(total - m)),
            )
        elif "induction" in topic:
            n0 = random.choice([1, 2])
            prompt, value = (
                rf"\text{{Verify the base case }}n={n0}\text{{ for }}"
                rf"\sum_{{k=1}}^n k=\frac{{n(n+1)}}2.",
                f"{n0}={n0}" if n0 == 1 else r"1+2=3",
            )
        elif "average_rates" in topic:
            a, b = random.randint(-3, 2), random.randint(3, 6)
            prompt, value = (
                rf"\text{{Find the average rate of change of }}f(x)=x^2\text{{ on }}[{a},{b}].",
                str(a + b),
            )
        elif "extrema_intervals" in topic:
            a = random.choice([1, 2, 3])
            prompt, value = (
                rf"\text{{Find the extrema and intervals of increase for }}f(x)={a}x^2.",
                rf"\text{{minimum }}0\text{{ at }}x=0;\ \text{{increasing on }}(0,\infty)",
            )
        elif "piecewise" in topic:
            c = random.randint(-3, 4)
            x0 = random.randint(-2, 3)
            prompt, value = (
                rf"f(x)=\begin{{cases}}x+{c},&x<0\\{c},&x\ge0\end{{cases}}."
                rf"\quad\text{{Evaluate }}f({x0}).",
                str(x0 + c if x0 < 0 else c),
            )
        elif "continuity" in topic:
            c = random.randint(-3, 4)
            prompt, value = (
                rf"f(x)=\begin{{cases}}x+{c},&x<0\\{c},&x\ge0\end{{cases}}."
                rf"\quad\text{{Is }}f\text{{ continuous at }}0?",
                "Yes",
            )
        elif "power_functions" in topic:
            prompt, value = (rf"\text{{Evaluate }}f(x)=x^{{{n}}}\text{{ at }}x={m}.", str(m**n))
        elif "logarithmic" in topic:
            base, shift = random.randint(2, 5), random.randint(-3, 3)
            prompt, value = (
                rf"\text{{State the vertical asymptote of }}f(x)=\log_{{{base}}}(x-({shift})).",
                f"x = {shift}",
            )
        elif "parametric" in topic:
            t = random.randint(1, 5)
            prompt, value = (
                rf"x=t^2,\ y=2t+1.\quad\text{{Find }}(x,y)\text{{ when }}t={t}.",
                f"({t * t}, {2 * t + 1})",
            )
        elif "projectile" in topic:
            v = random.randint(3, 8)
            prompt, value = (
                rf"h(t)=-16t^2+{32 * v}t.\quad\text{{Find the time of maximum height.}}",
                str(v),
            )
        elif "3d_points" in topic:
            x, y, z = (random.randint(1, 6) for _ in range(3))
            if random.random() < 0.5:
                x, y, z = random.choice([(3, 4, 12), (2, 3, 6), (1, 2, 2), (4, 4, 7)])
            dist_sq = x * x + y * y + z * z
            root = int(math.isqrt(dist_sq))
            ans = str(root) if root * root == dist_sq else rf"\sqrt{{{dist_sq}}}"
            prompt, value = (
                rf"\text{{Find the distance from }}(0,0,0)\text{{ to }}({x},{y},{z}).",
                ans,
            )
        elif "cross_products" in topic or "3d_vectors_operations" in topic:
            a = [random.randint(-3, 3) for _ in range(3)]
            b = [random.randint(-3, 3) for _ in range(3)]
            cx = a[1] * b[2] - a[2] * b[1]
            cy = a[2] * b[0] - a[0] * b[2]
            cz = a[0] * b[1] - a[1] * b[0]
            prompt, value = (
                rf"\text{{Find }}({a[0]},{a[1]},{a[2]})\times({b[0]},{b[1]},{b[2]}).",
                rf"({cx},{cy},{cz})",
            )
        elif "3d_vectors" in topic:
            # Basics fallback: magnitude
            x, y, z = random.choice([(3, 4, 0), (2, 3, 6), (1, 2, 2)])
            mag_sq = x * x + y * y + z * z
            root = int(math.isqrt(mag_sq))
            prompt, value = (
                rf"\text{{Find the magnitude of }}\langle {x},{y},{z}\rangle.",
                str(root) if root * root == mag_sq else rf"\sqrt{{{mag_sq}}}",
            )
        elif "partial_fraction" in topic:
            num = format_linear_latex(n, m)
            prompt, value = (
                rf"\text{{Decompose }}\frac{{{num}}}{{(x+1)(x+2)}}.",
                rf"\frac{{{m - n}}}{{x+1}}+\frac{{{2 * n - m}}}{{x+2}}",
            )
        elif "multivariable" in topic:
            s = random.randint(4, 9)
            z = random.randint(1, 3)
            x = (s - z) // 2
            y = x
            prompt, value = (
                rf"\text{{Solve }}x+y+z={s},\ x-y=0,\ z={z}.",
                rf"({x},{y},{z})",
            )
        elif "rational_inequalities" in topic:
            # (x-n)/(x+m) > 0 with critical points n and -m
            prompt, value = (
                rf"\frac{{x-{n}}}{{x+{m}}}>0.",
                rf"x<-{m}\text{{ or }}x>{n}",
            )
        elif "polynomial_inequalities" in topic or "inequalities" in topic:
            prompt, value = (
                rf"(x-{n})(x+{m})>0.",
                rf"x<-{m}\text{{ or }}x>{n}",
            )
        elif "rational_equations" in topic:
            prompt, value = (rf"\frac{{1}}{{x}}=\frac{{1}}{{{n}}}.", f"x = {n}")
        elif "complex_zeros" in topic:
            k = random.randint(2, 6)
            prompt, value = (rf"\text{{Find the zeros of }}x^2+{k * k}=0.", rf"x=\pm {k}i")
        elif "conjugate_roots" in topic:
            re = random.randint(1, 4)
            im = random.randint(1, 4)
            prompt, value = (
                rf"\text{{Write the monic polynomial with roots }}{re}+{im}i"
                rf"\text{{ and }}{re}-{im}i.",
                rf"x^2-{2 * re}x+{re * re + im * im}",
            )
        elif "power_series" in topic:
            c = random.choice([1, 2, 3])
            prompt, value = (
                rf"\text{{Find the radius of convergence of }}\sum_{{n=0}}^{{\infty}}({c}x)^n.",
                frac_latex(Fraction(1, c)),
            )
        elif "angles_and_angle" in topic:
            prompt, value = (
                rf"\text{{Convert }}{n * 30}^\circ\text{{ to radians.}}",
                _RADIAN_LABELS[n * 30],
            )
        elif "limits_at_essential" in topic or "essential_discontinuities" in topic:
            p = random.choice([1, 2])
            prompt, value = (rf"\lim_{{x\to0}}\frac{{1}}{{x^{{{p}}}}}", r"\text{does not exist}")
        elif "kinks" in topic or "jumps" in topic:
            c = random.randint(1, 4)
            prompt, value = (rf"\lim_{{x\to0}}|{c}x|", "0")
        elif "definition_of_the_derivative" in topic or "definition_of_derivative" in topic:
            prompt, value = (
                rf"\lim_{{h\to0}}\frac{{({n}+h)^{{2}}-{n * n}}}{{h}}",
                str(2 * n),
            )
        elif "instantaneous" in topic:
            prompt, value = (
                rf"\text{{Find }}f'({n})\text{{ for }}f(x)=x^{{2}}.",
                str(2 * n),
            )
        elif "approximating_area" in topic:
            L = 2 * n
            # Midpoint Riemann, 2 intervals, f(x)=x on [0,L] equals exact area L^2/2
            prompt, value = (
                rf"\text{{Use a midpoint Riemann sum with 2 equal intervals for }}"
                rf"f(x)=x\text{{ on }}[0,{L}].",
                frac_latex(Fraction(L * L, 2)),
            )
        elif "area_under" in topic or "limit_of_sums" in topic:
            prompt, value = (
                rf"\text{{Find the area under }}y=x\text{{ from }}0\text{{ to }}{n}.",
                frac_latex(Fraction(n * n, 2)),
            )
        elif "motion" in topic:
            prompt, value = (rf"s(t)=t^2+{n}t.\quad\text{{Find }}v(2).", str(4 + n))
        else:
            # Last-resort: still topic-shaped rather than n+m arithmetic.
            prompt, value = (
                rf"\text{{Evaluate }}f({n})\text{{ for }}f(x)=x^{{2}}.",
                str(n * n),
            )
        return prompt, topic, value if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _conic_rotation_identify(topic: str, settings: dict) -> list[Question]:
    """Identify whether an xy-term requires axis rotation, and the angle formula."""
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        a = random.randint(1, 5)
        b = random.choice([0, 2, 4, 6])
        c = random.randint(1, 5)
        # Ax^2 + Bxy + Cy^2 + ...
        if b == 0:
            ax2 = format_monomial_latex(a, degree=2) or "0"
            cy2 = format_monomial_latex(c, variable="y", degree=2) or "0"
            prompt = (
                f"\\text{{Does }} {ax2} + {cy2} = 1 "
                f"\\text{{ require a rotation of axes to eliminate an }} xy "
                f"\\text{{ term?}}"
            )
            answer = "no"
        else:
            # cot(2θ) = (A-C)/B
            ax2 = format_monomial_latex(a, degree=2) or "0"
            bxy = format_monomial_latex(b, variable="xy", degree=1) or "0"
            cy2 = format_monomial_latex(c, variable="y", degree=2) or "0"
            prompt = (
                f"\\text{{For }} {ax2} + {bxy} + {cy2} = 1,\\ "
                f"\\text{{find }} \\cot 2\\theta \\text{{ used to eliminate the }} xy "
                f"\\text{{ term.}}"
            )
            answer = f"\\frac{{{a - c}}}{{{b}}}"
        return prompt, "conic rotation", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _polar_graph_meta(
    settings: dict, *, curve: str, features: list[tuple[float, float]]
) -> dict[str, Any]:
    if not include_graph_metadata(settings):
        return {}
    x_min, x_max, y_min, y_max = origin_centered_bounds(features, settings=settings)
    answer_gs = {
        "x_min": x_min,
        "x_max": x_max,
        "y_min": y_min,
        "y_max": y_max,
        "functions": [curve] if curve else [],
        "points": [],
        "show_grid": bool(settings.get("show_grid", True)),
        "show_points": False,
    }
    return question_metadata(
        graph_spec={
            **answer_gs,
            "functions": [],
            "points": [],
            "show_points": False,
        },
        answer_graph_spec=answer_gs,
        graph_role="blank",
    )


def _polar_graphs(topic: str, settings: dict) -> list[Question]:
    """Graph / identify classic polar curves (circles, roses, cardioids, limaçons)."""
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}

    def build() -> tuple[str, str, str | None]:
        last["meta"] = {}
        kind = random.choice(
            ["circle_cos", "circle_sin", "cardioid", "rose", "limaçon", "line_theta"]
        )
        a = random.randint(2, 5)

        if kind == "circle_cos":
            prompt = rf"r={2 * a}\cos\theta"
            answer = rf"\text{{circle, center }}({a},0),\ \text{{radius }}{a}"
            last["meta"] = _polar_graph_meta(
                settings,
                curve=f"circle({a},0,{a})",
                features=[(0, 0), (2 * a, 0), (a, a), (a, -a)],
            )
        elif kind == "circle_sin":
            prompt = rf"r={2 * a}\sin\theta"
            answer = rf"\text{{circle, center }}(0,{a}),\ \text{{radius }}{a}"
            last["meta"] = _polar_graph_meta(
                settings,
                curve=f"circle(0,{a},{a})",
                features=[(0, 0), (0, 2 * a), (a, a), (-a, a)],
            )
        elif kind == "cardioid":
            sign = random.choice(["+", "-"])
            prompt = rf"r={a}(1{sign}\cos\theta)"
            answer = r"\text{cardioid}"
            # Blank plane only — cardioid is not a cartesian function curve.
            last["meta"] = _polar_graph_meta(
                settings, curve="", features=[(0, 0), (2 * a, 0), (0, a), (0, -a)]
            )
        elif kind == "rose":
            n = random.choice([2, 3, 4])
            fn = random.choice(["cos", "sin"])
            prompt = rf"r={a}\cos({n}\theta)" if fn == "cos" else rf"r={a}\sin({n}\theta)"
            petals = 2 * n if n % 2 == 0 else n
            answer = rf"\text{{rose with }}{petals}\text{{ petals}}"
            last["meta"] = _polar_graph_meta(
                settings, curve="", features=[(a, 0), (-a, 0), (0, a), (0, -a)]
            )
        elif kind == "limaçon":
            b = random.randint(1, max(1, a - 1))
            prompt = rf"r={a}+{b}\cos\theta"
            answer = r"\text{limacon}"
            last["meta"] = _polar_graph_meta(
                settings,
                curve="",
                features=[(a + b, 0), (b - a, 0), (0, a), (0, -a)],
            )
        else:
            k = random.choice([2, 3, 4, 6])
            prompt = rf"\theta=\frac{{\pi}}{{{k}}}"
            answer = r"\text{line through the origin}"
            last["meta"] = _polar_graph_meta(
                settings, curve="", features=[(0, 0), (4, 4), (-4, -4)]
            )
        return prompt, "polar graph", answer if keyed else None

    def metadata_builder(_p: str, _t: str, _a: str | None) -> dict[str, Any]:
        return dict(last.get("meta") or {})

    return _make_questions(
        topic, count, keyed, build, metadata_builder=metadata_builder, settings=settings
    )


def _polar_rectangular_forms(topic: str, settings: dict) -> list[Question]:
    """Convert equations between polar and rectangular form."""
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        mode = random.choice(["r_to_rect_circle", "r_to_rect_line", "rect_to_polar"])
        a = random.randint(2, 6)
        if mode == "r_to_rect_circle":
            # r = 2a cos θ → (x-a)^2 + y^2 = a^2
            prompt = (
                rf"\text{{Convert }}r={2 * a}\cos\theta"
                rf"\text{{ to rectangular form.}}"
            )
            answer = rf"(x-{a})^2+y^2={a * a}"
        elif mode == "r_to_rect_line":
            prompt = rf"\text{{Convert }}r\cos\theta={a}\text{{ to rectangular form.}}"
            answer = rf"x={a}"
        else:
            prompt = (
                rf"\text{{Convert }}x^2+y^2={a * a}"
                rf"\text{{ to polar form.}}"
            )
            answer = rf"r={a}"
        return prompt, "polar rectangular forms", answer if keyed else None

    return _make_questions(topic, count, keyed, build, settings=settings)


def _polar_conic_forms(topic: str, settings: dict) -> list[Question]:
    """Identify conic type from polar form r = ed / (1 ± e cos/sin θ)."""
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        # e < 1 ellipse, e = 1 parabola, e > 1 hyperbola
        kind = random.choice(["ellipse", "parabola", "hyperbola"])
        d = random.randint(2, 6)
        trig = random.choice(["\\cos", "\\sin"])
        sign = random.choice(["+", "-"])
        if kind == "ellipse":
            # Use e = p/q with p < q
            p, q = random.choice([(1, 2), (1, 3), (2, 3), (1, 4), (3, 4)])
            e_latex = rf"\frac{{{p}}}{{{q}}}"
            num = p * d
            den = q
            prompt = rf"r=\frac{{{num}}}{{{den}{sign}{p}{trig}\theta}}"
            # Normalize display: r = (ed)/(1 ± e cos) with ed = p*d/q
            # Prefer integer numerator form already above; answer is type + e
            answer = rf"\text{{ellipse }}, e={e_latex}"
        elif kind == "parabola":
            prompt = rf"r=\frac{{{d}}}{{1{sign}{trig}\theta}}"
            answer = r"\text{parabola }, e=1"
        else:
            p, q = random.choice([(3, 2), (4, 3), (5, 2), (5, 3), (5, 4)])
            e_latex = rf"\frac{{{p}}}{{{q}}}"
            prompt = rf"r=\frac{{{p * d}}}{{{q}{sign}{p}{trig}\theta}}"
            answer = rf"\text{{hyperbola }}, e={e_latex}"
        return prompt, "polar conic", answer if keyed else None

    return _make_questions(topic, count, keyed, build, settings=settings)


def _complex_polar_form(topic: str, settings: dict) -> list[Question]:
    """Convert complex numbers between rectangular and polar (cis) form."""
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    exact: list[tuple[int, int, str]] = [
        (1, 0, r"\cos 0+i\sin 0"),
        (0, 1, r"\cos\frac{\pi}{2}+i\sin\frac{\pi}{2}"),
        (-1, 0, r"\cos\pi+i\sin\pi"),
        (0, -1, r"\cos\frac{3\pi}{2}+i\sin\frac{3\pi}{2}"),
        (1, 1, r"\sqrt{2}\left(\cos\frac{\pi}{4}+i\sin\frac{\pi}{4}\right)"),
        (-1, 1, r"\sqrt{2}\left(\cos\frac{3\pi}{4}+i\sin\frac{3\pi}{4}\right)"),
        (-1, -1, r"\sqrt{2}\left(\cos\frac{5\pi}{4}+i\sin\frac{5\pi}{4}\right)"),
        (1, -1, r"\sqrt{2}\left(\cos\frac{7\pi}{4}+i\sin\frac{7\pi}{4}\right)"),
    ]

    def rect_latex(a: int, b: int) -> str:
        if a == 0 and b == 1:
            return "i"
        if a == 0 and b == -1:
            return "-i"
        if b == 0:
            return str(a)
        if a == 0:
            return f"{b}i"
        imag = "i" if abs(b) == 1 else f"{abs(b)}i"
        return f"{a}+{imag}" if b > 0 else f"{a}-{imag}"

    def build() -> tuple[str, str, str | None]:
        if random.random() < 0.55:
            a, b, polar = random.choice(exact)
            prompt = rf"\text{{Write }}{rect_latex(a, b)}\text{{ in polar form.}}"
            answer = polar
        else:
            a, b, polar = random.choice(exact)
            prompt = rf"\text{{Write }}{polar}\text{{ in rectangular form.}}"
            answer = rect_latex(a, b)
        return prompt, "complex polar", answer if keyed else None

    return _make_questions(topic, count, keyed, build, settings=settings)


GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = {
    "trig_evaluate": _trig_evaluate,
    "simple_trig_equations": _simple_trig_equations,
    "trig_unit_circle": _trig_unit_circle,
    "trig_basic_identities": _trig_basic_identities,
    "log_evaluate": _log_evaluate,
    "log_change_of_base": _log_change_of_base,
    "log_equation_simple": _log_equation_simple,
    "exponential_equation_simple": _exponential_equation_simple,
    "exponential_equation_with_log": _exponential_equation_with_log,
    "sequence_arithmetic_nth_term": _sequence_arithmetic_nth_term,
    "sequence_geometric_nth_term": _sequence_geometric_nth_term,
    "sequence_arithmetic_geometric_mean": _sequence_arithmetic_geometric_mean,
    "sequence_arithmetic_series": _sequence_arithmetic_series,
    "sequence_geometric_series": _sequence_geometric_series,
    "precalc_foundations": _precalc_foundations,
    "trig_sum_difference": _trig_sum_difference,
    "trig_multiple_angle": _trig_multiple_angle,
    "trig_product_to_sum": _trig_product_to_sum,
    "trig_factoring_equations": _trig_factoring_equations,
    "vector_3d_basics": _vector_3d_basics,
    "conic_rotation_identify": _conic_rotation_identify,
    "polar_graphs": _polar_graphs,
    "polar_rectangular_forms": _polar_rectangular_forms,
    "polar_conic_forms": _polar_conic_forms,
    "complex_polar_form": _complex_polar_form,
}
