"""Algebra 2 generators: quadratics, complex numbers, matrices, inverses."""

from __future__ import annotations

import math
import random
import uuid
from fractions import Fraction
from typing import Any, Callable

from ..core.metadata import question_metadata
from ..core.models import Question
from ..frameworks.graphing import include_graph_metadata, origin_centered_bounds, _sample_quadratic_graph
from .utils import (
    _make_questions,
    format_linear_latex,
    format_monomial_latex,
    format_polynomial_latex,
    join_algebra_terms,
    random_int_range,
)

Matrix2 = tuple[tuple[int, int], tuple[int, int]]


def _format_signed(value: int | float) -> str:
    if value == 0:
        return "0"
    if value == int(value):
        return str(int(value))
    return f"{value:g}"


def _graph_quad_fn(a: float, b: float, c: float) -> str:
    from packages.polynomial_core import normalize_expression_signs

    return normalize_expression_signs(
        f"{_format_signed(a)}*x^2+{_format_signed(b)}*x+{_format_signed(c)}"
    )


def _vertex_from_standard(a: float, b: float, c: float) -> tuple[float, float]:
    h = -b / (2 * a)
    k = a * h * h + b * h + c
    return h, k


def _parabola_graph_metadata(
    a: float,
    b: float,
    c: float,
    settings: dict,
    *,
    extra_points: list[tuple[float, float]] | None = None,
    prompt: str = "blank",
) -> dict[str, Any]:
    if not include_graph_metadata(settings):
        return {}
    h, k = _vertex_from_standard(a, b, c)
    xs = [h - 3, h, h + 3, 0, 1]
    features: list[tuple[float, float]] = [(x, a * x * x + b * x + c) for x in xs]
    points: list[tuple[float, float]] = [(h, k)]
    if extra_points:
        features.extend(extra_points)
        points.extend(extra_points)
    x_min, x_max, y_min, y_max = origin_centered_bounds(features, settings=settings)
    answer_gs = {
        "x_min": x_min,
        "x_max": x_max,
        "y_min": y_min,
        "y_max": y_max,
        "functions": [_graph_quad_fn(a, b, c)],
        "points": [],
        "show_grid": bool(settings.get("show_grid", True)),
        "show_points": False,
    }
    if prompt == "blank":
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
    return question_metadata(graph_spec=answer_gs, graph_role="stimulus")


def _vertex_form_latex(a: int, h: int, k: int) -> str:
    a_part = "" if a == 1 else ("-" if a == -1 else str(a))
    h_part = f"(x - {h})" if h > 0 else (f"(x + {-h})" if h < 0 else "x")
    if k == 0:
        return f"y = {a_part}{h_part}^2"
    sign = "+" if k > 0 else "-"
    return f"y = {a_part}{h_part}^2 {sign} {abs(k)}"


def _complex_latex(real: int, imag: int) -> str:
    if imag == 0:
        return str(real)
    sign = "+" if imag > 0 else "-"
    imag_part = "i" if abs(imag) == 1 else f"{abs(imag)}i"
    if real == 0:
        return f"{sign[0]}{imag_part}" if imag < 0 else imag_part
    return f"{real} {sign} {imag_part}"


def _matrix_latex(matrix: Matrix2) -> str:
    rows = " \\\\ ".join(" & ".join(str(value) for value in row) for row in matrix)
    return rf"\begin{{pmatrix}}{rows}\end{{pmatrix}}"


def _random_vertex_parabola(settings: dict) -> tuple[int, int, int, int, int]:
    """Legacy int sampler for non-graphing quadratic helpers."""
    from .utils import pick_quadratic_leading_coef, settings_require_monic

    coef_max = int(settings.get("coef_max", 3) or 3)
    coef_min = int(settings.get("coef_min", -3) or -3)
    # Easy graph defaults pin a = 1 via coef_min/max or monic flags.
    if (
        settings_require_monic(settings)
        or (coef_min == 1 and coef_max == 1)
        or bool(settings.get("allow_stretch") is False and coef_max <= 1 and coef_min >= 1)
    ):
        a = 1
    else:
        a_mag = pick_quadratic_leading_coef(
            settings,
            coef_max=max(abs(coef_min), abs(coef_max), 1),
            max_a=max(1, min(5, max(abs(coef_min), abs(coef_max), 1))),
            prefer_nonunit=True,
        )
        allow_reflection = bool(settings.get("allow_reflection", True))
        a = -a_mag if allow_reflection and random.random() < 0.45 else a_mag
    coord_lo = int(settings.get("coord_min", -5))
    coord_hi = int(settings.get("coord_max", 5))
    intercept_lo = int(settings.get("intercept_min", -8))
    intercept_hi = int(settings.get("intercept_max", 8))
    h = random.randint(min(coord_lo, coord_hi), max(coord_lo, coord_hi))
    k = random.randint(min(intercept_lo, intercept_hi), max(intercept_lo, intercept_hi))
    b = -2 * a * h
    c = a * h * h + k
    return a, h, k, b, c


def _quadratic_graph_vertex(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    questions: list[Question] = []
    for _ in range(count):
        latex, a, h, k, _expr = _sample_quadratic_graph(settings)
        b = -2.0 * a * h
        c = a * h * h + k
        prompt = f"\\text{{Graph }} {latex}"
        answer = f"\\text{{vertex }} ({h:g}, {k:g})" if include_answer_key else None
        questions.append(
            Question(
                id=str(uuid.uuid4()),
                topic=topic,
                prompt_latex=prompt,
                prompt_text=f"Graph {latex}",
                answer_latex=answer,
                metadata=_parabola_graph_metadata(a, b, c, settings),
            )
        )
    return questions


def _quadratic_vertex_identify(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        a, h, k, _, _ = _random_vertex_parabola(settings)
        prompt = f"\\text{{Find the vertex of }} {_vertex_form_latex(a, h, k)}"
        answer = f"({h}, {k})" if include_answer_key else None
        return prompt, f"vertex ({h},{k})", answer

    return _make_questions(topic, count, include_answer_key, build)


def _quadratic_vertex_form_write(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        a, h, k, _, _ = _random_vertex_parabola(settings)
        prompt = (
            f"\\text{{Write the equation in vertex form for a parabola with "
            f"vertex }} ({h}, {k}) \\text{{ and }} a = {a}."
        )
        answer = _vertex_form_latex(a, h, k).replace("y = ", "") if include_answer_key else None
        return prompt, f"vertex form ({h},{k})", answer

    return _make_questions(topic, count, include_answer_key, build)


def _quadratic_completing_square_vertex(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        a, h, k, b, c = _random_vertex_parabola(settings)
        poly = format_polynomial_latex([a, b, c])
        prompt = f"\\text{{Complete the square: }} {poly}"
        answer = _vertex_form_latex(a, h, k).replace("y = ", "") if include_answer_key else None
        return prompt, "complete square to vertex", answer

    return _make_questions(topic, count, include_answer_key, build)


def _quadratic_graph_inequality(topic: str, settings: dict) -> list[Question]:
    """Algebra 2 entry point — same generator as Algebra 1 graphing inequalities."""
    from ..frameworks.graphing import GraphQuadraticInequalityFramework

    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    framework = GraphQuadraticInequalityFramework()
    questions: list[Question] = []
    for _ in range(count):
        prompt, prompt_text, answer = framework.build_prompt(settings)
        meta = framework.build_question_metadata(
            settings, prompt_latex=prompt, prompt_text=prompt_text, answer=answer
        )
        questions.append(
            Question(
                id=str(uuid.uuid4()),
                topic=topic,
                prompt_latex=prompt,
                prompt_text=prompt_text,
                answer_latex=answer if include_answer_key else None,
                metadata=meta,
            )
        )
    return questions


def _random_complex() -> tuple[int, int]:
    return random.randint(-8, 8), random.randint(-8, 8)


def _complex_add_subtract(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        a1, b1 = _random_complex()
        a2, b2 = _random_complex()
        op = random.choice(["+", "-"])
        if op == "+":
            real, imag = a1 + a2, b1 + b2
        else:
            real, imag = a1 - a2, b1 - b2
        prompt = f"\\left({_complex_latex(a1, b1)}\\right) {op} \\left({_complex_latex(a2, b2)}\\right)"
        answer = _complex_latex(real, imag) if include_answer_key else None
        return prompt, "complex add/subtract", answer

    return _make_questions(topic, count, include_answer_key, build)


def _complex_multiply(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        a1, b1 = _random_complex()
        a2, b2 = _random_complex()
        real = a1 * a2 - b1 * b2
        imag = a1 * b2 + b1 * a2
        prompt = f"\\left({_complex_latex(a1, b1)}\\right)\\left({_complex_latex(a2, b2)}\\right)"
        answer = _complex_latex(real, imag) if include_answer_key else None
        return prompt, "complex multiply", answer

    return _make_questions(topic, count, include_answer_key, build)


def _complex_operations(topic: str, settings: dict) -> list[Question]:
    fn = random.choice([_complex_add_subtract, _complex_multiply])
    return fn(topic, settings)


def _complex_graph(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    questions: list[Question] = []
    for _ in range(count):
        real, imag = _random_complex()
        prompt = f"\\text{{Plot }} {_complex_latex(real, imag)} \\text{{ on the complex plane.}}"
        answer = f"({real}, {imag})" if include_answer_key else None
        metadata: dict[str, Any] = {}
        if include_graph_metadata(settings):
            x_min, x_max, y_min, y_max = origin_centered_bounds(
                [(float(real), float(imag))], settings=settings,
            )
            answer_gs = {
                "x_min": x_min,
                "x_max": x_max,
                "y_min": y_min,
                "y_max": y_max,
                "functions": [],
                "points": [(real, imag)],
                "show_grid": bool(settings.get("show_grid", True)),
                "show_points": bool(settings.get("show_points", True)),
            }
            metadata = question_metadata(
                graph_spec={
                    **answer_gs,
                    "points": [],
                    "show_points": False,
                },
                answer_graph_spec=answer_gs,
                graph_role="blank",
            )
        questions.append(
            Question(
                id=str(uuid.uuid4()),
                topic=topic,
                prompt_latex=prompt,
                prompt_text=f"Plot {real}+{imag}i",
                answer_latex=answer,
                metadata=metadata,
            )
        )
    return questions


def _complex_absolute_value(topic: str, settings: dict) -> list[Question]:
    """Modulus of a complex number |a+bi|."""
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        real, imag = _random_complex()
        # Prefer non-zero imag so this is clearly a complex modulus.
        if imag == 0:
            imag = random.choice([-3, -2, -1, 1, 2, 3])
        prompt = rf"\left|{_complex_latex(real, imag)}\right|"
        mag_sq = real * real + imag * imag
        # Exact simplified radical when possible
        root = int(math.isqrt(mag_sq))
        if root * root == mag_sq:
            answer = str(root)
        else:
            # Factor out perfect-square part
            remaining = mag_sq
            coeff = 1
            for p in range(2, int(math.isqrt(remaining)) + 1):
                while remaining % (p * p) == 0:
                    remaining //= p * p
                    coeff *= p
            answer = rf"{coeff}\sqrt{{{remaining}}}" if coeff > 1 else rf"\sqrt{{{mag_sq}}}"
        return prompt, "complex modulus", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _conic_blank_and_answer(
    settings: dict,
    *,
    curve: str,
    features: list[tuple[float, float]],
) -> dict[str, Any]:
    """Blank student plane + answer curve for conic graphing topics."""
    if not include_graph_metadata(settings):
        return {}
    x_min, x_max, y_min, y_max = origin_centered_bounds(features, settings=settings)
    answer_gs = {
        "x_min": x_min,
        "x_max": x_max,
        "y_min": y_min,
        "y_max": y_max,
        "functions": [curve],
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


def _conic_sections(topic: str, settings: dict) -> list[Question]:
    """Circles / ellipses / hyperbolas: graph, write equations, or classify."""
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))
    tid = topic.lower()
    graphing = "graphing" in tid or ("graphs" in tid and "writing" not in tid)
    # Carry curve metadata from the most recent build() into metadata_builder.
    last: dict[str, Any] = {"meta": {}}

    def build() -> tuple[str, str, str | None]:
        last["meta"] = {}

        if "classify" in tid:
            kind = random.choice(["circle", "ellipse", "hyperbola", "parabola"])
            if kind == "circle":
                r = random.randint(2, 6)
                eq = rf"x^2+y^2={r * r}"
            elif kind == "ellipse":
                a, b = random.randint(4, 7), random.randint(2, 5)
                while a == b:
                    b = random.randint(2, 5)
                eq = rf"\frac{{x^2}}{{{a * a}}}+\frac{{y^2}}{{{b * b}}}=1"
            elif kind == "hyperbola":
                a, b = random.randint(2, 5), random.randint(2, 5)
                if random.choice([True, False]):
                    eq = rf"\frac{{x^2}}{{{a * a}}}-\frac{{y^2}}{{{b * b}}}=1"
                else:
                    eq = rf"\frac{{y^2}}{{{a * a}}}-\frac{{x^2}}{{{b * b}}}=1"
            else:
                p = random.randint(1, 4)
                eq = rf"x^2={4 * p}y"
            return rf"\text{{Classify the conic: }} {eq}.", "conic classify", kind if keyed else None

        if "circle" in tid:
            h, k, r = random.randint(-5, 5), random.randint(-5, 5), random.randint(2, 7)
            eq = rf"(x-({h}))^2+(y-({k}))^2={r * r}"
            if "writing" in tid:
                prompt = (
                    rf"\text{{Write the equation of the circle with center }}({h},{k})"
                    rf"\text{{ and radius }}{r}."
                )
                answer = eq
            elif graphing:
                prompt = eq
                answer = rf"\text{{center }}({h},{k}),\ \text{{radius }}{r}"
                last["meta"] = _conic_blank_and_answer(
                    settings,
                    curve=f"circle({h},{k},{r})",
                    features=[(h - r, k), (h + r, k), (h, k - r), (h, k + r), (h, k)],
                )
            else:
                prompt = rf"\text{{Find the center and radius of }} {eq}."
                answer = rf"\text{{center }}({h},{k}),\ \text{{radius }}{r}"
            return prompt, "circle conic", answer if keyed else None

        if "ellipse" in tid:
            a, b = random.randint(3, 8), random.randint(2, 6)
            while a == b:
                b = random.randint(2, 6)
            eq = rf"\frac{{x^2}}{{{a * a}}}+\frac{{y^2}}{{{b * b}}}=1"
            if "writing" in tid:
                prompt = (
                    rf"\text{{Write the equation of an ellipse centered at the origin "
                    rf"with }}a={a}\text{{ and }}b={b}."
                )
                answer = eq
            elif graphing:
                prompt = eq
                answer = rf"a={a},\ b={b}"
                last["meta"] = _conic_blank_and_answer(
                    settings,
                    curve=f"ellipse(0,0,{a},{b})",
                    features=[(a, 0), (-a, 0), (0, b), (0, -b)],
                )
            else:
                prompt = rf"\text{{Find }}a\text{{ and }}b\text{{ for }} {eq}."
                answer = rf"a={a},\ b={b}"
            return prompt, "ellipse conic", answer if keyed else None

        if "hyperbola" in tid:
            a, b = random.randint(2, 6), random.randint(2, 6)
            horizontal = random.choice([True, False])
            if horizontal:
                eq = rf"\frac{{x^2}}{{{a * a}}}-\frac{{y^2}}{{{b * b}}}=1"
                orient = "horizontal"
                curve = f"hyperbola_h(0,0,{a},{b})"
                features = [(a, 0), (-a, 0), (a + 2, b), (-a - 2, b)]
            else:
                eq = rf"\frac{{y^2}}{{{a * a}}}-\frac{{x^2}}{{{b * b}}}=1"
                orient = "vertical"
                curve = f"hyperbola_v(0,0,{a},{b})"
                features = [(0, a), (0, -a), (b, a + 2), (b, -a - 2)]
            if "writing" in tid:
                prompt = (
                    rf"\text{{Write the equation of a {orient} hyperbola centered at the "
                    rf"origin with }}a={a}\text{{ and }}b={b}."
                )
                answer = eq
            elif graphing:
                prompt = eq
                answer = rf"a={a},\ b={b},\ \text{{{orient}}}"
                last["meta"] = _conic_blank_and_answer(
                    settings, curve=curve, features=features
                )
            else:
                prompt = rf"\text{{Identify }}a,\ b,\text{{ and the orientation of }} {eq}."
                answer = rf"a={a},\ b={b},\ \text{{{orient}}}"
            return prompt, "hyperbola conic", answer if keyed else None

        # Parabola (writing / focus–directrix form)
        p = random.randint(1, 5)
        vertical = random.choice([True, False])
        if vertical:
            eq = rf"x^2={4 * p}y"
            focus = f"(0,{p})"
            features = [(0, 0), (0, p), (2 * p, p), (-2 * p, p)]
            curve = f"parabola_v(0,0,{p})"
        else:
            eq = rf"y^2={4 * p}x"
            focus = f"({p},0)"
            features = [(0, 0), (p, 0), (p, 2 * p), (p, -2 * p)]
            curve = f"parabola_h(0,0,{p})"
        if "writing" in tid or not graphing:
            prompt = (
                rf"\text{{Write the equation of a parabola with vertex }}(0,0)"
                rf"\text{{ and focus }}{focus}."
            )
            answer = eq
        else:
            prompt = eq
            answer = rf"\text{{vertex }}(0,0),\ \text{{focus }}{focus}"
            last["meta"] = _conic_blank_and_answer(
                settings, curve=curve, features=features
            )
        return prompt, "parabola conic", answer if keyed else None

    def metadata_builder(_prompt: str, _text: str, _answer: str | None) -> dict[str, Any]:
        return dict(last.get("meta") or {})

    return _make_questions(
        topic, count, keyed, build, metadata_builder=metadata_builder, settings=settings
    )


def _random_matrix() -> Matrix2:
    return (
        (random.randint(-5, 5), random.randint(-5, 5)),
        (random.randint(-5, 5), random.randint(-5, 5)),
    )


def _matrix_add_subtract(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        m1 = _random_matrix()
        m2 = _random_matrix()
        op = random.choice(["+", "-"])
        if op == "+":
            result = (
                (m1[0][0] + m2[0][0], m1[0][1] + m2[0][1]),
                (m1[1][0] + m2[1][0], m1[1][1] + m2[1][1]),
            )
        else:
            result = (
                (m1[0][0] - m2[0][0], m1[0][1] - m2[0][1]),
                (m1[1][0] - m2[1][0], m1[1][1] - m2[1][1]),
            )
        prompt = f"{_matrix_latex(m1)} {op} {_matrix_latex(m2)}"
        answer = _matrix_latex(result) if include_answer_key else None
        return prompt, f"matrix {op}", answer

    return _make_questions(topic, count, include_answer_key, build)


def _matrix_scalar_multiply(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        scalar = random_int_range(-6, 6, exclude={0})
        m = _random_matrix()
        result = (
            (scalar * m[0][0], scalar * m[0][1]),
            (scalar * m[1][0], scalar * m[1][1]),
        )
        prompt = f"{scalar} \\cdot {_matrix_latex(m)}"
        answer = _matrix_latex(result) if include_answer_key else None
        return prompt, f"scalar {scalar} * matrix", answer

    return _make_questions(topic, count, include_answer_key, build)


def _matrix_operations(topic: str, settings: dict) -> list[Question]:
    fn = random.choice([_matrix_add_subtract, _matrix_scalar_multiply])
    return fn(topic, settings)


def _inverse_function_basic(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        m = random_int_range(-6, 6, exclude={0})
        b = random.randint(-8, 8)
        prompt = f"\\text{{Find the inverse of }} f(x) = {format_linear_latex(m, b)}"
        inv_b = -b / m
        inv_sign = "+" if inv_b >= 0 else "-"
        if abs(m) == 1:
            answer = f"f^{{-1}}(x) = x {inv_sign} {abs(inv_b):g}" if include_answer_key else None
        else:
            inv_slope = f"\\frac{{1}}{{{m}}}"
            answer = (
                f"f^{{-1}}(x) = {inv_slope}(x {inv_sign} {abs(inv_b):g})"
                if include_answer_key
                else None
            )
        return prompt, "inverse linear", answer

    return _make_questions(topic, count, include_answer_key, build)


def _function_evaluate(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        kind = random.choice(["linear", "quadratic"])
        x = random.randint(-4, 4)
        if kind == "linear":
            m = random_int_range(-5, 5, exclude={0})
            b = random.randint(-6, 6)
            value = m * x + b
            prompt = f"\\text{{If }} f(x) = {format_linear_latex(m, b)}, \\text{{ find }} f({x})."
        else:
            a = random.choice([-2, -1, 1, 2])
            h = random.randint(-3, 3)
            k = random.randint(-6, 6)
            value = a * (x - h) ** 2 + k
            prompt = f"\\text{{If }} f(x) = {_vertex_form_latex(a, h, k).replace('y = ', '')}, \\text{{ find }} f({x})."
        answer = str(value) if include_answer_key else None
        return prompt, f"f({x})", answer

    return _make_questions(topic, count, include_answer_key, build)


def _function_operations(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        x = random.randint(-3, 3)
        m1 = random.randint(1, 4)
        b1 = random.randint(-5, 5)
        m2 = random.randint(1, 4)
        b2 = random.randint(-5, 5)
        op = random.choice(["+", "-"])
        f_val = m1 * x + b1
        g_val = m2 * x + b2
        result = f_val + g_val if op == "+" else f_val - g_val
        s1 = "+" if b1 >= 0 else "-"
        s2 = "+" if b2 >= 0 else "-"
        prompt = (
            f"\\text{{If }} f(x) = {m1}x {s1} {abs(b1)} \\text{{ and }} "
            f"g(x) = {m2}x {s2} {abs(b2)}, \\text{{ find }} (f {op} g)({x})."
        )
        answer = str(result) if include_answer_key else None
        return prompt, f"(f {op} g)({x})", answer

    return _make_questions(topic, count, include_answer_key, build)


def _matrix_inverse(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        while True:
            matrix = _random_matrix()
            determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
            if determinant in {-4, -3, -2, -1, 1, 2, 3, 4}:
                break
        adjugate = ((matrix[1][1], -matrix[0][1]), (-matrix[1][0], matrix[0][0]))
        answer = (
            rf"\frac{{1}}{{{determinant}}}{_matrix_latex(adjugate)}" if keyed else None
        )
        return rf"\text{{Find the inverse of }} {_matrix_latex(matrix)}.", "matrix inverse", answer

    return _make_questions(topic, count, keyed, build)


def _matrix_cramers_rule(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        while True:
            a, b, c, d = (random_int_range(-5, 5, exclude={0}) for _ in range(4))
            if abs(a * d - b * c) >= 2:
                break
        x, y = random.randint(-5, 5), random.randint(-5, 5)
        e, f = a * x + b * y, c * x + d * y
        eq1 = f"{join_algebra_terms([format_monomial_latex(a, variable='x'), format_monomial_latex(b, variable='y')])} = {e}"
        eq2 = f"{join_algebra_terms([format_monomial_latex(c, variable='x'), format_monomial_latex(d, variable='y')])} = {f}"
        prompt = rf"\text{{Use Cramer's Rule to solve }} \begin{{cases}} {eq1}\\ {eq2} \end{{cases}}"
        return prompt, "Cramer's Rule", f"({x}, {y})" if keyed else None

    return _make_questions(topic, count, keyed, build)


def _matrix_transformation(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))
    transforms = (
        ("reflection across the x-axis", ((1, 0), (0, -1))),
        ("reflection across the y-axis", ((-1, 0), (0, 1))),
        ("a 90^\\circ counterclockwise rotation", ((0, -1), (1, 0))),
        ("a 180^\\circ rotation", ((-1, 0), (0, -1))),
    )

    def build() -> tuple[str, str, str | None]:
        name, matrix = random.choice(transforms)
        x, y = random.randint(-6, 6), random.randint(-6, 6)
        image = (matrix[0][0] * x + matrix[0][1] * y, matrix[1][0] * x + matrix[1][1] * y)
        prompt = rf"\text{{Apply {name} to }} ({x}, {y}) \text{{ using }} {_matrix_latex(matrix)}."
        return prompt, name, f"({image[0]}, {image[1]})" if keyed else None

    return _make_questions(topic, count, keyed, build)


def _polynomial_writing(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        roots = random.sample([value for value in range(-6, 7) if value], 2)
        a = random.choice([-2, -1, 1, 2])
        coefficient_b = -a * sum(roots)
        coefficient_c = a * roots[0] * roots[1]
        expression = format_polynomial_latex([a, coefficient_b, coefficient_c])
        prompt = rf"\text{{Write a quadratic function with zeros }} {roots[0]} \text{{ and }} {roots[1]} \text{{ and leading coefficient }} {a}."
        return prompt, "write polynomial from zeros", expression if keyed else None

    return _make_questions(topic, count, keyed, build)


def _polynomial_conjugate_writing(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        real = random.randint(-4, 4)
        imaginary = random.randint(1, 5)
        b, c = -2 * real, real * real + imaginary * imaginary
        sign = "+" if real >= 0 else "-"
        prompt = rf"\text{{Write a monic quadratic with roots }} {real} {sign} {imaginary}i \text{{ and }} {real} {'-' if real >= 0 else '+'} {imaginary}i."
        return prompt, "conjugate-root polynomial", format_polynomial_latex([1, b, c]) if keyed else None

    return _make_questions(topic, count, keyed, build)


def _descartes_rule_of_signs(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def changes(values: list[int]) -> int:
        return sum(left * right < 0 for left, right in zip(values, values[1:]))

    def build() -> tuple[str, str, str | None]:
        coefficients = [random_int_range(-6, 6, exclude={0}) for _ in range(4)]
        positive = changes(coefficients)
        negative = changes([value if (3 - index) % 2 == 0 else -value for index, value in enumerate(coefficients)])
        expression = format_polynomial_latex(coefficients)
        answer = (
            rf"\text{{positive: }} {positive}, {positive - 2}, \ldots; "
            rf"\text{{negative: }} {negative}, {negative - 2}, \ldots"
            if keyed else None
        )
        return rf"\text{{Use Descartes' Rule of Signs for }} f(x)={expression}.", "Descartes signs", answer

    return _make_questions(topic, count, keyed, build)


def _polynomial_end_behavior(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        degree = random.choice([3, 4, 5, 6])
        leading = random.choice([-3, -2, 2, 3])
        mid = random.randint(-8, 8)
        const = random.randint(-8, 8)
        # Sparse polynomial: leading, x^2, constant (zeros omitted by formatter).
        coeffs = [0] * (degree + 1)
        coeffs[0] = leading
        coeffs[degree - 2] = mid
        coeffs[degree] = const
        expression = format_polynomial_latex(coeffs)
        if leading > 0 and degree % 2 == 0:
            answer = r"\text{as }x\to\pm\infty,\ f(x)\to\infty"
        elif leading < 0 and degree % 2 == 0:
            answer = r"\text{as }x\to\pm\infty,\ f(x)\to-\infty"
        elif leading > 0:
            answer = r"x\to-\infty:f(x)\to-\infty;\quad x\to\infty:f(x)\to\infty"
        else:
            answer = r"x\to-\infty:f(x)\to\infty;\quad x\to\infty:f(x)\to-\infty"
        return rf"\text{{Describe the end behavior of }} f(x)={expression}.", "polynomial end behavior", answer if keyed else None

    return _make_questions(topic, count, keyed, build)


def _fundamental_theorem_algebra(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        degree = random.randint(3, 8)
        return (
            rf"\text{{By the Fundamental Theorem of Algebra, how many complex zeros, counting multiplicity, does a degree-}}{degree}\text{{ polynomial have?}}",
            "number of complex zeros",
            str(degree) if keyed else None,
        )

    return _make_questions(topic, count, keyed, build)


def _rational_zero_root_theorem(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def divisors(number: int) -> list[int]:
        return [factor for factor in range(1, abs(number) + 1) if number % factor == 0]

    def build() -> tuple[str, str, str | None]:
        leading = random.choice([2, 3, 4, 5, 6])
        constant = random.choice([2, 3, 4, 5, 6, 8, 9, 10])
        candidates = sorted({Fraction(p, q) for p in divisors(constant) for q in divisors(leading)})
        candidate_text = [str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}" for value in candidates]
        answer = rf"\pm\{{{', '.join(candidate_text)}\}}" if keyed else None
        poly = format_polynomial_latex(
            [leading, random.randint(-8, 8), random.randint(-8, 8), constant]
        )
        return rf"\text{{List all possible rational zeros of }} {poly}.", "rational zero candidates", answer

    return _make_questions(topic, count, keyed, build)


def _radical_domain_range(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        h, k = random.randint(-6, 6), random.randint(-6, 6)
        a = random.choice([-3, -2, -1, 1, 2, 3])
        inner = f"x - {h}" if h >= 0 else f"x + {-h}"
        domain = rf"[{h}, \infty)"
        value = rf"[{k}, \infty)" if a > 0 else rf"(-\infty, {k}]"
        return rf"\text{{Find the domain and range of }} f(x)={a}\sqrt{{{inner}}} {k:+}.", "radical domain and range", (rf"\text{{Domain }}{domain};\ \text{{Range }}{value}" if keyed else None)

    return _make_questions(topic, count, keyed, build)


def _quadratic_system(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        roots = random.sample(range(-4, 5), 2)
        # x^2 = mx+b has prescribed intersections at the selected roots.
        intercept = roots[0] * roots[1]
        linear_constant = -intercept
        slope = sum(roots)
        prompt = (
            rf"\text{{Solve }} \begin{{cases}} y=x^2\\ "
            rf"y={format_linear_latex(slope, linear_constant)}\end{{cases}}"
        )
        answer = rf"({roots[0]}, {roots[0] ** 2}),\ ({roots[1]}, {roots[1] ** 2})" if keyed else None
        return prompt, "quadratic system", answer

    return _make_questions(topic, count, keyed, build)


def _points_three_dimensions(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        point = tuple(random.randint(-8, 8) for _ in range(3))
        return rf"\text{{State the coordinates of point }} P \text{{ in three dimensions: }} P=({point[0]}, {point[1]}, {point[2]}).", "3D coordinates", rf"({point[0]}, {point[1]}, {point[2]})" if keyed else None

    return _make_questions(topic, count, keyed, build)


def _planes(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        a, b, c = (random_int_range(-4, 4, exclude={0}) for _ in range(3))
        x, y = random.randint(-4, 4), random.randint(-4, 4)
        z = random.randint(-4, 4)
        d = a * x + b * y + c * z
        plane = join_algebra_terms(
            [
                format_monomial_latex(a, variable="x"),
                format_monomial_latex(b, variable="y"),
                format_monomial_latex(c, variable="z"),
            ]
        )
        return (
            rf"\text{{Does }} ({x}, {y}, {z}) \text{{ lie on the plane }} {plane}={d}\text{{?}}",
            "point on plane",
            r"\text{Yes}" if keyed else None,
        )

    return _make_questions(topic, count, keyed, build)


def _system_three_variables(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        x, y, z = (random.randint(-5, 5) for _ in range(3))
        while True:
            a, b, c = (
                random_int_range(-4, 4, exclude={0}),
                random_int_range(-4, 4, exclude={0}),
                random_int_range(-4, 4, exclude={0}),
            )
            determinant = (
                a * ((-c) * (-b) - a * a)
                - b * (b * (-b) - a * c)
                + c * (b * a - (-c) * c)
            )
            if determinant:
                break
        e, f, g = a * x + b * y + c * z, b * x - c * y + a * z, c * x + a * y - b * z
        eq1 = f"{join_algebra_terms([format_monomial_latex(a, variable='x'), format_monomial_latex(b, variable='y'), format_monomial_latex(c, variable='z')])}={e}"
        eq2 = f"{join_algebra_terms([format_monomial_latex(b, variable='x'), format_monomial_latex(-c, variable='y'), format_monomial_latex(a, variable='z')])}={f}"
        eq3 = f"{join_algebra_terms([format_monomial_latex(c, variable='x'), format_monomial_latex(a, variable='y'), format_monomial_latex(-b, variable='z')])}={g}"
        prompt = rf"\text{{Solve }} \begin{{cases}} {eq1}\\ {eq2}\\ {eq3}\end{{cases}}"
        return prompt, "three-variable system", rf"({x}, {y}, {z})" if keyed else None

    return _make_questions(topic, count, keyed, build)


def _angle_measure(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        measure = random.randint(15, 165)
        relation = random.choice(["complementary", "supplementary", "vertical"])
        answer = 90 - measure if relation == "complementary" else (180 - measure if relation == "supplementary" else measure)
        if relation == "complementary" and answer <= 0:
            measure = random.randint(10, 80)
            answer = 90 - measure
        return rf"\text{{An angle measures }} {measure}^\circ\text{{. Find the measure of its {relation} angle.}}", f"{relation} angle", rf"{answer}^\circ" if keyed else None

    return _make_questions(topic, count, keyed, build)


def _degrees_minutes_seconds(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        degrees, minutes, seconds = random.randint(1, 179), random.randint(0, 59), random.randint(0, 59)
        decimal = degrees + minutes / 60 + seconds / 3600
        prompt = rf"\text{{Convert }} {degrees}^\circ {minutes}' {seconds}'' \text{{ to decimal degrees. Round to the nearest thousandth.}}"
        return prompt, "DMS to decimal degrees", f"{decimal:.3f}^\\circ" if keyed else None

    return _make_questions(topic, count, keyed, build)


def _graphing_trig_functions(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))
    tier = str(settings.get("difficulty_tier") or "medium").lower()
    # Easy: parent ±sin/±cos. Medium: amplitude. Hard: amplitude + period (+ optional phase).
    if tier == "easy":
        mode = "parent"
    elif tier == "hard":
        mode = "transform"
    else:
        mode = "amplitude"

    questions: list[Question] = []
    for _ in range(count):
        fn = random.choice(["sin", "cos"])
        sign = random.choice([1, -1])
        amp = 1
        b = 1  # period factor: period = 2π/b
        h = 0  # phase shift
        if mode == "amplitude":
            amp = random.choice([2, 3, 4])
        elif mode == "transform":
            amp = random.choice([2, 3, 4])
            b = random.choice([2, 3])
            if random.random() < 0.5:
                h = random.choice([1, 2])  # shift by π/h style: write as (bx - π/k)

        if mode == "parent":
            core_latex = rf"\{fn} x"
            expr = f"{fn}(x)"
            period_tex = r"2\pi"
        elif mode == "amplitude":
            core_latex = rf"{amp}\{fn} x"
            expr = f"{amp}*{fn}(x)"
            period_tex = r"2\pi"
        elif h:
            phase = r"\pi" if h == 1 else rf"\frac{{\pi}}{{{h}}}"
            core_latex = rf"{amp}\{fn}\left({b}x-{phase}\right)"
            expr = f"{amp}*{fn}({b}*x - pi/{h})"
            period_tex = r"\pi" if b == 2 else (r"\frac{2\pi}{3}" if b == 3 else rf"\frac{{2\pi}}{{{b}}}")
        else:
            core_latex = rf"{amp}\{fn}\left({b}x\right)"
            expr = f"{amp}*{fn}({b}*x)"
            period_tex = r"\pi" if b == 2 else (r"\frac{2\pi}{3}" if b == 3 else rf"\frac{{2\pi}}{{{b}}}")

        if sign < 0:
            latex_fn = rf"-{core_latex}"
            expr = f"-({expr})"
            reflect = r",\ \text{reflection over the x-axis}"
        else:
            latex_fn = core_latex
            reflect = ""

        features = (
            rf"\text{{amplitude }}{amp},\ \text{{period }}{period_tex},"
            rf"\ \text{{midline }}y=0{reflect}"
        )

        meta: dict[str, Any] = {}
        if include_graph_metadata(settings):
            y_pad = float(max(amp + 1, 2))
            x_min, x_max, y_min, y_max = origin_centered_bounds(
                [(-6.5, -y_pad), (6.5, y_pad)],
                settings=settings,
                padding=0.5,
                min_half_range=4.0,
            )
            answer_gs = {
                "x_min": x_min,
                "x_max": x_max,
                "y_min": y_min,
                "y_max": y_max,
                "functions": [expr],
                "points": [],
                "show_grid": bool(settings.get("show_grid", True)),
                "show_points": False,
            }
            meta = question_metadata(
                graph_spec={
                    **answer_gs,
                    "functions": [],
                    "points": [],
                },
                answer_graph_spec=answer_gs,
                graph_role="blank",
            )
        questions.append(
            Question(
                id=str(uuid.uuid4()),
                topic=topic,
                prompt_latex=rf"\text{{Graph }} y={latex_fn}\text{{ over one period.}}",
                prompt_text=f"Graph y = {expr} over one period.",
                answer_latex=features if keyed else None,
                metadata=meta,
            )
        )
    return questions


def _inverse_exponential_logarithmic(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        base = random.choice([2, 3, 5])
        h, k = random.randint(-4, 4), random.randint(-4, 4)
        if random.choice([True, False]):
            prompt = rf"\text{{Find the inverse of }} f(x)={base}^{{x {h:+}}} {k:+}."
            answer = rf"f^{{-1}}(x)=\log_{{{base}}}(x {(-k):+}) {-h:+}"
        else:
            prompt = rf"\text{{Find the inverse of }} f(x)=\log_{{{base}}}(x {h:+}) {k:+}."
            answer = rf"f^{{-1}}(x)={base}^{{x {(-k):+}}} {-h:+}"
        return prompt, "inverse exponential or logarithm", answer if keyed else None

    return _make_questions(topic, count, keyed, build)


GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = {
    "quadratic_graph_vertex": _quadratic_graph_vertex,
    "quadratic_vertex_identify": _quadratic_vertex_identify,
    "quadratic_vertex_form_write": _quadratic_vertex_form_write,
    "quadratic_completing_square_vertex": _quadratic_completing_square_vertex,
    "quadratic_graph_inequality": _quadratic_graph_inequality,
    "complex_add_subtract": _complex_add_subtract,
    "complex_multiply": _complex_multiply,
    "complex_operations": _complex_operations,
    "complex_graph": _complex_graph,
    "complex_absolute_value": _complex_absolute_value,
    "conic_sections": _conic_sections,
    "matrix_add_subtract": _matrix_add_subtract,
    "matrix_scalar_multiply": _matrix_scalar_multiply,
    "matrix_operations": _matrix_operations,
    "matrix_inverse": _matrix_inverse,
    "matrix_cramers_rule": _matrix_cramers_rule,
    "matrix_transformation": _matrix_transformation,
    "inverse_function_basic": _inverse_function_basic,
    "function_evaluate": _function_evaluate,
    "function_operations": _function_operations,
    "polynomial_writing": _polynomial_writing,
    "polynomial_conjugate_writing": _polynomial_conjugate_writing,
    "descartes_rule_of_signs": _descartes_rule_of_signs,
    "polynomial_end_behavior": _polynomial_end_behavior,
    "fundamental_theorem_algebra": _fundamental_theorem_algebra,
    "rational_zero_root_theorem": _rational_zero_root_theorem,
    "radical_domain_range": _radical_domain_range,
    "quadratic_system": _quadratic_system,
    "points_three_dimensions": _points_three_dimensions,
    "planes": _planes,
    "system_three_variables": _system_three_variables,
    "angle_measure": _angle_measure,
    "degrees_minutes_seconds": _degrees_minutes_seconds,
    "graphing_trig_functions": _graphing_trig_functions,
    "inverse_exponential_logarithmic": _inverse_exponential_logarithmic,
}
