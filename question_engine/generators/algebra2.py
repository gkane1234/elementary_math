"""Algebra 2 generators: quadratics, complex numbers, matrices, inverses."""

from __future__ import annotations

import random
import uuid
from typing import Any, Callable

from ..core.metadata import question_metadata
from ..core.models import Question
from ..frameworks.graphing import include_graph_metadata
from .utils import _make_questions, random_int_range

Matrix2 = tuple[tuple[int, int], tuple[int, int]]


def _format_signed(value: int | float) -> str:
    if value == 0:
        return "0"
    if value == int(value):
        return str(int(value))
    return f"{value:g}"


def _graph_quad_fn(a: float, b: float, c: float) -> str:
    return f"{_format_signed(a)}*x^2+{_format_signed(b)}*x+{_format_signed(c)}"


def _vertex_from_standard(a: int, b: int, c: int) -> tuple[float, float]:
    h = -b / (2 * a)
    k = a * h * h + b * h + c
    return h, k


def _parabola_graph_metadata(
    a: int,
    b: int,
    c: int,
    settings: dict,
    *,
    extra_points: list[tuple[float, float]] | None = None,
) -> dict[str, Any]:
    if not include_graph_metadata(settings):
        return {}
    h, k = _vertex_from_standard(a, b, c)
    coord_min = float(settings.get("coord_min", -8))
    coord_max = float(settings.get("coord_max", 8))
    xs = [h - 3, h, h + 3, 0, 1]
    ys = [a * x * x + b * x + c for x in xs]
    if extra_points:
        xs.extend(p[0] for p in extra_points)
        ys.extend(p[1] for p in extra_points)
    padding = 2.0
    x_min = min(min(xs), coord_min) - padding
    x_max = max(max(xs), coord_max) + padding
    y_min = min(min(ys), coord_min) - padding
    y_max = max(max(ys), coord_max) + padding
    points: list[tuple[float, float]] = [(h, k)]
    if extra_points:
        points.extend(extra_points)
    return question_metadata(
        graph_spec={
            "x_min": x_min,
            "x_max": x_max,
            "y_min": y_min,
            "y_max": y_max,
            "functions": [_graph_quad_fn(a, b, c)],
            "points": points,
            "show_grid": bool(settings.get("show_grid", True)),
            "show_points": bool(settings.get("show_points", True)),
        }
    )


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
    a = random.choice([-3, -2, -1, 1, 2, 3])
    h = random.randint(-5, 5)
    k = random.randint(-8, 8)
    b = -2 * a * h
    c = a * h * h + k
    return a, h, k, b, c


def _quadratic_graph_vertex(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    questions: list[Question] = []
    for _ in range(count):
        a, h, k, b, c = _random_vertex_parabola(settings)
        prompt = f"\\text{{Graph }} {_vertex_form_latex(a, h, k)}"
        answer = f"\\text{{vertex }} ({h}, {k})" if include_answer_key else None
        questions.append(
            Question(
                id=str(uuid.uuid4()),
                topic=topic,
                prompt_latex=prompt,
                prompt_text=f"Graph y = {a}(x-{h})^2 + {k}",
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
        if a != 1:
            prompt = f"\\text{{Complete the square: }} {a}x^2 + {b}x + {c}"
            answer = _vertex_form_latex(a, h, k).replace("y = ", "") if include_answer_key else None
        else:
            prompt = f"\\text{{Complete the square: }} x^2 + {b}x + {c}"
            answer = _vertex_form_latex(1, h, k).replace("y = ", "") if include_answer_key else None
        return prompt, "complete square to vertex", answer

    return _make_questions(topic, count, include_answer_key, build)


def _quadratic_graph_inequality(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    questions: list[Question] = []
    for _ in range(count):
        a, h, k, b, c = _random_vertex_parabola(settings)
        opens_up = a > 0
        symbol = random.choice([r">", r"\geq"]) if opens_up else random.choice([r"<", r"\leq"])
        relation = ">" if ">" in symbol else "<"
        if opens_up:
            answer_text = f"x < {h - 1:g} \\text{{ or }} x > {h + 1:g}" if relation == ">" else f"{h - 1:g} < x < {h + 1:g}"
        else:
            answer_text = f"{h - 1:g} < x < {h + 1:g}" if relation == ">" else f"x < {h - 1:g} \\text{{ or }} x > {h + 1:g}"
        prompt = f"\\text{{Describe the solution set of }} {_vertex_form_latex(a, h, k).replace('y = ', 'y ')}{symbol} 0"
        answer = answer_text if include_answer_key else None
        questions.append(
            Question(
                id=str(uuid.uuid4()),
                topic=topic,
                prompt_latex=prompt,
                prompt_text=f"Quadratic inequality vertex ({h},{k})",
                answer_latex=answer,
                metadata=_parabola_graph_metadata(a, b, c, settings),
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
            coord_min = float(settings.get("coord_min", -8))
            coord_max = float(settings.get("coord_max", 8))
            metadata = question_metadata(
                graph_spec={
                    "x_min": coord_min,
                    "x_max": coord_max,
                    "y_min": coord_min,
                    "y_max": coord_max,
                    "functions": [],
                    "points": [(real, imag)],
                    "show_grid": bool(settings.get("show_grid", True)),
                    "show_points": bool(settings.get("show_points", True)),
                }
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
        sign = "+" if b >= 0 else "-"
        prompt = f"\\text{{Find the inverse of }} f(x) = {m}x {sign} {abs(b)}"
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
            sign = "+" if b >= 0 else "-"
            prompt = f"\\text{{If }} f(x) = {m}x {sign} {abs(b)}, \\text{{ find }} f({x})."
        else:
            a = random.choice([-2, -1, 1, 2])
            h = random.randint(-3, 3)
            k = random.randint(-6, 6)
            value = a * (x - h) ** 2 + k
            prompt = f"\\text{{If }} f(x) = {a}(x - {h})^2 + {k}, \\text{{ find }} f({x})."
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
    "matrix_add_subtract": _matrix_add_subtract,
    "matrix_scalar_multiply": _matrix_scalar_multiply,
    "matrix_operations": _matrix_operations,
    "inverse_function_basic": _inverse_function_basic,
    "function_evaluate": _function_evaluate,
    "function_operations": _function_operations,
}
