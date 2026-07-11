"""Graphing framework — coordinate plane, slope, and number-line metadata."""

from __future__ import annotations

import random
import re
from dataclasses import dataclass, field
from typing import Any, Literal

from .base import QuestionFramework
from ..core.metadata import GraphSpec, question_metadata
from ..generators.utils import random_int_range

Quadrant = Literal["I", "II", "III", "IV", "all"]
NumberLineDirection = Literal["left", "right", "both"]


GraphPromptRole = Literal["blank", "stimulus"]


@dataclass(frozen=True)
class NumberLineSpec:
    min_value: float
    max_value: float
    boundary: float
    direction: NumberLineDirection
    inclusive: bool = False
    tick_interval: float = 1.0
    boundary_high: float | None = None
    show_zero: bool = True
    blank: bool = False


@dataclass
class CoordinatePlaneSpec:
    points: list[tuple[float, float]] = field(default_factory=list)
    functions: list[str] = field(default_factory=list)
    slope: float | None = None
    y_intercept: float | None = None
    x_intercept: float | None = None
    show_grid: bool = True
    show_points: bool = True
    quadrant: Quadrant = "all"
    x_min: float | None = None
    x_max: float | None = None
    y_min: float | None = None
    y_max: float | None = None


def include_graph_metadata(settings: dict) -> bool:
    return bool(settings.get("include_graph_metadata", False))


def _number_line_bounds(settings: dict, *values: float) -> tuple[float, float, float]:
    """1D bounds that include 0 and any given values (origin-aware)."""
    raw_min = float(settings.get("number_line_min", -12))
    raw_max = float(settings.get("number_line_max", 12))
    half = max(abs(raw_min), abs(raw_max), 1.0)
    padding = 2.0
    for value in values:
        half = max(half, abs(float(value)) + padding)
    tick = float(settings.get("number_line_tick_interval", 1))
    return -half, half, max(tick, 1.0)


def _number_line_show_zero(settings: dict) -> bool:
    return bool(settings.get("number_line_show_zero", True))


def _settings_half_range(settings: dict | None, default: float = 8.0) -> float:
    """Half-range implied by coord_min/coord_max (always origin-aware)."""
    if not settings:
        return default
    coord_min = float(settings.get("coord_min", -default))
    coord_max = float(settings.get("coord_max", default))
    return max(abs(coord_min), abs(coord_max), 1.0)


def _coordinate_bounds(settings: dict) -> tuple[float, float, float, float]:
    """Default origin-centered viewport from settings (no feature expansion)."""
    return origin_centered_bounds(settings=settings)


def origin_centered_bounds(
    features: list[tuple[float, float]] | None = None,
    *,
    settings: dict | None = None,
    min_half_range: float | None = None,
    padding: float = 2.0,
    square: bool = True,
) -> tuple[float, float, float, float]:
    """
    Origin-centered viewport that includes all feature points.

    Returns (x_min, x_max, y_min, y_max) with x_min=-Rx, x_max=Rx,
    y_min=-Ry, y_max=Ry. When square=True (default), Rx == Ry == R.

    Uses settings coord_min/coord_max as the minimum half-range when
    min_half_range is omitted. Features expand the range with padding so
    the graph fits without cropping the viewport tightly around a vertex
    or other feature (which would give away its location).
    """
    half = float(min_half_range) if min_half_range is not None else _settings_half_range(settings)
    rx = half
    ry = half
    for x, y in features or []:
        rx = max(rx, abs(float(x)) + padding)
        ry = max(ry, abs(float(y)) + padding)
    if square:
        r = max(rx, ry)
        return -r, r, -r, r
    return -rx, rx, -ry, ry


def _bounds_with_padding(
    xs: list[float],
    ys: list[float],
    *,
    settings: dict,
    padding: float = 2,
) -> tuple[float, float, float, float]:
    """Deprecated alias — prefer origin_centered_bounds."""
    features = list(zip(xs, ys)) if xs and ys and len(xs) == len(ys) else [
        (x, 0.0) for x in xs
    ] + [(0.0, y) for y in ys]
    return origin_centered_bounds(features, settings=settings, padding=padding)


_SIMPLE_INEQUALITY = re.compile(r"^(\w+)\s*(<=|>=|<|>)\s*(-?\d+(?:\.\d+)?)$")
_COMPOUND_INEQUALITY = re.compile(r"^(-?\d+(?:\.\d+)?)\s*<\s*(\w+)\s*<\s*(-?\d+(?:\.\d+)?)$")
_LATEX_FRAC = re.compile(r"\\frac\{(-?\d+)\}\{(\d+)\}")


def _parse_numeric(token: str) -> float:
    cleaned = token.strip()
    frac = _LATEX_FRAC.fullmatch(cleaned)
    if frac:
        return float(frac.group(1)) / float(frac.group(2))
    return float(cleaned.replace("g", ""))


def symbol_to_direction(symbol: str) -> tuple[NumberLineDirection, bool]:
    text = symbol.replace(r"\leq", "<=").replace(r"\geq", ">=")
    inclusive = text in ("<=", ">=")
    direction: NumberLineDirection = "left" if text in ("<=", "<") else "right"
    return direction, inclusive


def number_line_spec_from_symbol_and_value(
    symbol: str,
    boundary: float,
    settings: dict,
    *,
    boundary_high: float | None = None,
) -> NumberLineSpec:
    extras = (boundary,) if boundary_high is None else (boundary, boundary_high)
    lo, hi, tick = _number_line_bounds(settings, *extras)
    show_zero = _number_line_show_zero(settings)
    if boundary_high is not None:
        return NumberLineSpec(
            min_value=lo,
            max_value=hi,
            boundary=boundary,
            boundary_high=boundary_high,
            direction="both",
            inclusive=False,
            tick_interval=tick,
            show_zero=show_zero,
        )
    direction, inclusive = symbol_to_direction(symbol)
    return NumberLineSpec(
        min_value=lo,
        max_value=hi,
        boundary=boundary,
        direction=direction,
        inclusive=inclusive,
        tick_interval=tick,
        show_zero=show_zero,
    )


def number_line_spec_to_dict(spec: NumberLineSpec) -> dict[str, Any]:
    data: dict[str, Any] = {
        "min_value": spec.min_value,
        "max_value": spec.max_value,
        "boundary": spec.boundary,
        "direction": spec.direction,
        "inclusive": spec.inclusive,
        "tick_interval": spec.tick_interval,
        "show_zero": spec.show_zero,
        "blank": spec.blank,
    }
    if spec.boundary_high is not None:
        data["boundary_high"] = spec.boundary_high
    return data


def number_line_graph_spec(spec: NumberLineSpec) -> GraphSpec:
    return {
        "x_min": spec.min_value,
        "x_max": spec.max_value,
        "y_min": -1,
        "y_max": 1,
        "functions": [],
        "points": [],
        "show_grid": False,
        "show_points": False,
    }


def blank_number_line_spec(settings: dict) -> NumberLineSpec:
    lo, hi, tick = _number_line_bounds(settings)
    return NumberLineSpec(
        min_value=lo,
        max_value=hi,
        boundary=0.0,
        direction="both",
        inclusive=False,
        tick_interval=tick,
        show_zero=_number_line_show_zero(settings),
        blank=True,
    )


def blank_graph_spec(graph: GraphSpec) -> GraphSpec:
    """Axes/grid/bounds only — no solution curves or points."""
    return {
        "x_min": graph["x_min"],
        "x_max": graph["x_max"],
        "y_min": graph["y_min"],
        "y_max": graph["y_max"],
        "functions": [],
        "points": [],
        "show_grid": graph.get("show_grid", True),
        "show_points": False,
    }


def metadata_from_number_line_spec(
    spec: NumberLineSpec,
    *,
    prompt: GraphPromptRole = "stimulus",
) -> dict[str, Any]:
    """Emit prompt number line (+ optional answer_number_line_spec for blank prompts)."""
    answer_dict = number_line_spec_to_dict(
        NumberLineSpec(
            min_value=spec.min_value,
            max_value=spec.max_value,
            boundary=spec.boundary,
            direction=spec.direction,
            inclusive=spec.inclusive,
            tick_interval=spec.tick_interval,
            boundary_high=spec.boundary_high,
            show_zero=spec.show_zero,
            blank=False,
        )
    )
    companion = number_line_graph_spec(spec)
    if prompt == "blank":
        blank_dict = number_line_spec_to_dict(
            NumberLineSpec(
                min_value=spec.min_value,
                max_value=spec.max_value,
                boundary=0.0,
                direction="both",
                inclusive=False,
                tick_interval=spec.tick_interval,
                show_zero=spec.show_zero,
                blank=True,
            )
        )
        return question_metadata(
            number_line_spec=blank_dict,
            answer_number_line_spec=answer_dict,
            graph_spec=companion,
            answer_graph_spec=companion,
            graph_role="blank",
        )
    return question_metadata(
        number_line_spec=answer_dict,
        graph_spec=companion,
        graph_role="stimulus",
    )


def number_line_spec_from_settings(settings: dict) -> NumberLineSpec | None:
    if not include_graph_metadata(settings):
        return None
    return blank_number_line_spec(settings)


def number_line_spec_from_answer(answer: str | None, settings: dict) -> NumberLineSpec | None:
    if not include_graph_metadata(settings):
        return None
    if not answer:
        return blank_number_line_spec(settings)

    text = answer.strip()

    compound = _COMPOUND_INEQUALITY.match(text)
    if compound:
        low = _parse_numeric(compound.group(1))
        high = _parse_numeric(compound.group(3))
        return number_line_spec_from_symbol_and_value("<", low, settings, boundary_high=high)

    simple = _SIMPLE_INEQUALITY.match(text)
    if simple:
        symbol = simple.group(2)
        boundary = _parse_numeric(simple.group(3))
        return number_line_spec_from_symbol_and_value(symbol, boundary, settings)

    return blank_number_line_spec(settings)


def number_line_metadata(answer: str | None, settings: dict) -> dict[str, Any]:
    """Blank prompt number line; solution shading goes in answer_number_line_spec when known."""
    spec = number_line_spec_from_answer(answer, settings)
    if spec is None:
        return {}
    # Solve-and-graph / graph-the-inequality: student works on a blank line.
    return metadata_from_number_line_spec(spec, prompt="blank")


def coordinate_plane_spec_to_graph_spec(spec: CoordinatePlaneSpec, settings: dict) -> GraphSpec:
    xs = [p[0] for p in spec.points]
    ys = [p[1] for p in spec.points]
    features: list[tuple[float, float]] = list(spec.points)
    if spec.y_intercept is not None:
        features.append((0.0, float(spec.y_intercept)))
    if spec.x_intercept is not None:
        features.append((float(spec.x_intercept), 0.0))

    if spec.x_min is not None and spec.x_max is not None and spec.y_min is not None and spec.y_max is not None:
        # Explicit full bounds on the spec win; still prefer origin-centered callers.
        x_min, x_max = spec.x_min, spec.x_max
        y_min, y_max = spec.y_min, spec.y_max
    else:
        auto_x_min, auto_x_max, auto_y_min, auto_y_max = origin_centered_bounds(
            features, settings=settings,
        )
        x_min = spec.x_min if spec.x_min is not None else auto_x_min
        x_max = spec.x_max if spec.x_max is not None else auto_x_max
        y_min = spec.y_min if spec.y_min is not None else auto_y_min
        y_max = spec.y_max if spec.y_max is not None else auto_y_max

    functions: list[str] = list(spec.functions)
    if not functions and spec.slope is not None and spec.y_intercept is not None:
        functions.append(_linear_function_expr(spec.slope, spec.y_intercept))

    return {
        "x_min": x_min,
        "x_max": x_max,
        "y_min": y_min,
        "y_max": y_max,
        "functions": functions,
        "points": list(spec.points),
        "show_grid": spec.show_grid,
        "show_points": spec.show_points,
    }


def coordinate_plane_metadata(
    spec: CoordinatePlaneSpec,
    settings: dict,
    *,
    prompt: GraphPromptRole = "stimulus",
) -> dict[str, Any]:
    """
    Build graph metadata.

    prompt=\"blank\": empty plane for student work; solution in answer_graph_spec.
    prompt=\"stimulus\": show the graph (line/points) with the question.
    """
    if not include_graph_metadata(settings):
        return {}
    spec.show_grid = bool(settings.get("show_grid", spec.show_grid))
    spec.show_points = bool(settings.get("show_points", spec.show_points))
    answer_gs = coordinate_plane_spec_to_graph_spec(spec, settings)
    if prompt == "blank":
        # Prompt metadata must not leak sampled curve points (abs/quad/exp/etc.).
        plane_meta = {
            "show_grid": spec.show_grid,
            "show_points": False,
            "quadrant": spec.quadrant,
            "slope": None,
            "y_intercept": None,
            "x_intercept": None,
            "points": [],
        }
        return question_metadata(
            coordinate_plane=plane_meta,
            graph_spec=blank_graph_spec(answer_gs),
            answer_graph_spec=answer_gs,
            graph_role="blank",
        )
    plane_meta = {
        "show_grid": spec.show_grid,
        "show_points": spec.show_points,
        "quadrant": spec.quadrant,
        "slope": spec.slope,
        "y_intercept": spec.y_intercept,
        "x_intercept": spec.x_intercept,
        "points": list(spec.points),
    }
    return question_metadata(
        coordinate_plane=plane_meta,
        graph_spec=answer_gs,
        graph_role="stimulus",
    )


def graph_spec_from_points(
    points: list[tuple[float, float]],
    settings: dict,
    *,
    slope: float | None = None,
    y_intercept: float | None = None,
    prompt: GraphPromptRole = "blank",
) -> dict[str, Any]:
    spec = CoordinatePlaneSpec(
        points=points,
        slope=slope,
        y_intercept=y_intercept,
        show_grid=bool(settings.get("show_grid", True)),
        show_points=bool(settings.get("show_points", True)),
    )
    return coordinate_plane_metadata(spec, settings, prompt=prompt)


def _linear_function_expr(m: float, b: float) -> str:
    """Emit mx+b in the form the frontend linear parser accepts (e.g. -0.5*x+1)."""
    return f"{float(m):g}*x+{float(b):g}"


def _bounds(settings: dict, min_key: str, max_key: str, lo: int, hi: int) -> tuple[int, int]:
    a = int(settings.get(min_key, lo))
    b = int(settings.get(max_key, hi))
    return (a, b) if a <= b else (b, a)


def _random_in_bounds(settings: dict, min_key: str, max_key: str, lo: int, hi: int, *, exclude: set[int] | None = None) -> int:
    lo2, hi2 = _bounds(settings, min_key, max_key, lo, hi)
    for _ in range(50):
        value = random.randint(lo2, hi2)
        if exclude is None or value not in exclude:
            return value
    return lo2


def _random_slope(settings: dict) -> int:
    return _random_in_bounds(settings, "slope_min", "slope_max", -6, 6, exclude={0})


def _random_intercept(settings: dict) -> int:
    return _random_in_bounds(settings, "intercept_min", "intercept_max", -8, 8)


def _random_coord(settings: dict) -> int:
    return _random_in_bounds(settings, "coord_min", "coord_max", -8, 8)


def _random_point(settings: dict) -> tuple[int, int]:
    return _random_coord(settings), _random_coord(settings)


def _format_signed(value: int, *, variable: str = "") -> str:
    if value == 0 and variable:
        return "0"
    if variable:
        if value == 1:
            return variable
        if value == -1:
            return f"-{variable}"
        return f"{value}{variable}"
    return str(value)


def _slope_intercept_latex(m: int, b: int) -> str:
    if m == 0:
        return f"y = {b}"
    slope_part = _format_signed(m, variable="x")
    if b == 0:
        return f"y = {slope_part}"
    sign = "+" if b > 0 else "-"
    return f"y = {slope_part} {sign} {abs(b)}"


def _system_latex(eq1: str, eq2: str) -> str:
    return f"\\begin{{cases}} {eq1} \\\\ {eq2} \\end{{cases}}"


def _slope_from_points(x1: int, y1: int, x2: int, y2: int):
    from fractions import Fraction
    return Fraction(y2 - y1, x2 - x1)


def _plane_spec(
    settings: dict,
    *,
    points: list[tuple[int, int]] | None = None,
    slope: int | None = None,
    y_intercept: int | None = None,
    functions: list[str] | None = None,
) -> CoordinatePlaneSpec:
    return CoordinatePlaneSpec(
        points=[(float(x), float(y)) for x, y in (points or [])],
        functions=list(functions or []),
        slope=float(slope) if slope is not None else None,
        y_intercept=float(y_intercept) if y_intercept is not None else None,
        show_grid=bool(settings.get("show_grid", True)),
        show_points=bool(settings.get("show_points", True)),
        quadrant=settings.get("quadrant", "all"),  # type: ignore[arg-type]
    )


def _pick_inequality_symbol() -> str:
    return random.choice([">", "<", r"\geq", r"\leq"])


def _graph_dimension(settings: dict, default: str = "coordinate") -> str:
    return str(settings.get("graph_dimension", default))


class GraphLinearEquationFramework(QuestionFramework):
    instruction_latex = r"\text{Graph the following equations.}"
    instruction_text = "Graph the following equations."

    def __init__(self) -> None:
        self._last_spec: CoordinatePlaneSpec | None = None

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        m = _random_slope(settings)
        b = _random_intercept(settings)
        eq = _slope_intercept_latex(m, b)
        self._last_spec = _plane_spec(settings, slope=m, y_intercept=b)
        return eq, "Graph linear equation", eq

    def build_question_metadata(
        self, settings: dict, *, prompt_latex: str, prompt_text: str, answer: str | None,
    ) -> dict[str, Any]:
        if self._last_spec is None:
            return {}
        return coordinate_plane_metadata(self._last_spec, settings, prompt="blank")


class GraphInequalityFramework(QuestionFramework):
    instruction_latex = r"\text{Graph the following inequalities.}"
    instruction_text = "Graph the following inequalities."

    def __init__(self, *, default_dimension: str = "coordinate") -> None:
        self.default_dimension = default_dimension
        self._last_number_line: NumberLineSpec | None = None
        self._last_plane: CoordinatePlaneSpec | None = None
        if default_dimension == "number_line":
            self.instruction_latex = r"\text{Graph the following on the number line.}"
            self.instruction_text = "Graph the following on the number line."

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        dimension = _graph_dimension(settings, self.default_dimension)
        symbol = _pick_inequality_symbol()

        if dimension == "number_line":
            boundary = random.randint(-8, 8)
            prompt = f"x {symbol} {boundary}"
            answer = f"x {symbol} {boundary}"
            direction, inclusive = symbol_to_direction(symbol)
            lo, hi, tick = _number_line_bounds(settings, float(boundary))
            self._last_number_line = NumberLineSpec(
                min_value=lo,
                max_value=hi,
                boundary=float(boundary),
                direction=direction,
                inclusive=inclusive,
                tick_interval=tick,
                show_zero=_number_line_show_zero(settings),
            )
            self._last_plane = None
            return prompt, "Graph inequality (number line)", answer

        m = _random_slope(settings)
        b = _random_intercept(settings)
        rhs = _slope_intercept_latex(m, b).replace("y = ", "")
        prompt = f"y {symbol} {rhs}"
        answer = f"y {symbol} {rhs}"
        self._last_plane = _plane_spec(
            settings, slope=m, y_intercept=b, functions=[_linear_function_expr(m, b)],
        )
        self._last_number_line = None
        return prompt, "Graph inequality (plane)", answer

    def build_question_metadata(
        self, settings: dict, *, prompt_latex: str, prompt_text: str, answer: str | None,
    ) -> dict[str, Any]:
        if not include_graph_metadata(settings):
            return {}
        if self._last_number_line is not None:
            return metadata_from_number_line_spec(self._last_number_line, prompt="blank")
        if self._last_plane is not None:
            return coordinate_plane_metadata(self._last_plane, settings, prompt="blank")
        return {}


class GraphAbsoluteValueFramework(QuestionFramework):
    instruction_latex = r"\text{Graph the following equations.}"
    instruction_text = "Graph the following equations."

    def __init__(self) -> None:
        self._last_spec: CoordinatePlaneSpec | None = None

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        h = _random_coord(settings)
        k = _random_intercept(settings)
        inner = f"x - {h}" if h > 0 else (f"x + {abs(h)}" if h < 0 else "x")
        eq = f"y = |{inner}| + {k}" if k >= 0 else f"y = |{inner}| - {abs(k)}"
        points = [(float(h + d), float(abs(d) + k)) for d in range(-5, 6)]
        self._last_spec = _plane_spec(settings, points=[(int(x), int(y)) for x, y in points])
        return eq, "Graph absolute value", eq

    def build_question_metadata(
        self, settings: dict, *, prompt_latex: str, prompt_text: str, answer: str | None,
    ) -> dict[str, Any]:
        if self._last_spec is None:
            return {}
        return coordinate_plane_metadata(self._last_spec, settings, prompt="blank")


class GraphSystemFramework(QuestionFramework):
    instruction_latex = r"\text{Solve the following systems by graphing.}"
    instruction_text = "Solve the following systems by graphing."

    def __init__(self) -> None:
        self._last_spec: CoordinatePlaneSpec | None = None

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        x_sol, y_sol = _random_point(settings)
        m1 = _random_slope(settings)
        b1 = y_sol - m1 * x_sol
        m2 = _random_slope(settings)
        while m2 == m1:
            m2 = _random_slope(settings)
        b2 = y_sol - m2 * x_sol
        eq1 = _slope_intercept_latex(m1, b1)
        eq2 = _slope_intercept_latex(m2, b2)
        prompt = _system_latex(eq1, eq2)
        answer = f"(x, y) = ({x_sol}, {y_sol})"
        self._last_spec = _plane_spec(
            settings,
            points=[(x_sol, y_sol)],
            functions=[_linear_function_expr(m1, b1), _linear_function_expr(m2, b2)],
        )
        return prompt, "Graph system", answer

    def build_question_metadata(
        self, settings: dict, *, prompt_latex: str, prompt_text: str, answer: str | None,
    ) -> dict[str, Any]:
        if self._last_spec is None:
            return {}
        return coordinate_plane_metadata(self._last_spec, settings, prompt="blank")


class GraphSystemInequalitiesFramework(QuestionFramework):
    instruction_latex = r"\text{Graph the following systems.}"
    instruction_text = "Graph the following systems."

    def __init__(self) -> None:
        self._last_spec: CoordinatePlaneSpec | None = None

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        m1 = _random_slope(settings)
        b1 = _random_intercept(settings)
        m2 = _random_slope(settings)
        while m2 == m1:
            m2 = _random_slope(settings)
        b2 = _random_intercept(settings)
        sym1 = _pick_inequality_symbol()
        sym2 = _pick_inequality_symbol()
        rhs1 = _slope_intercept_latex(m1, b1).replace("y = ", "")
        rhs2 = _slope_intercept_latex(m2, b2).replace("y = ", "")
        eq1 = f"y {sym1} {rhs1}"
        eq2 = f"y {sym2} {rhs2}"
        prompt = _system_latex(eq1, eq2)
        answer = f"y {sym1} {rhs1}, y {sym2} {rhs2}"
        self._last_spec = _plane_spec(
            settings,
            functions=[_linear_function_expr(m1, b1), _linear_function_expr(m2, b2)],
        )
        return prompt, "Graph system of inequalities", answer

    def build_question_metadata(
        self, settings: dict, *, prompt_latex: str, prompt_text: str, answer: str | None,
    ) -> dict[str, Any]:
        if self._last_spec is None:
            return {}
        return coordinate_plane_metadata(self._last_spec, settings, prompt="blank")


class GraphExponentialFramework(QuestionFramework):
    instruction_latex = r"\text{Graph the following functions.}"
    instruction_text = "Graph the following functions."

    def __init__(self) -> None:
        self._last_spec: CoordinatePlaneSpec | None = None

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        base = random.choice([2, 3])
        coeff = random.choice([1, 2])
        fn = f"y = {coeff} \\cdot {base}^x" if coeff != 1 else f"y = {base}^x"
        points = [(x, coeff * (base**x)) for x in range(-3, 4)]
        self._last_spec = _plane_spec(settings, points=points)
        return fn, "Graph exponential", fn

    def build_question_metadata(
        self, settings: dict, *, prompt_latex: str, prompt_text: str, answer: str | None,
    ) -> dict[str, Any]:
        if self._last_spec is None:
            return {}
        return coordinate_plane_metadata(self._last_spec, settings, prompt="blank")


class GraphQuadraticFramework(QuestionFramework):
    instruction_latex = r"\text{Graph the following functions.}"
    instruction_text = "Graph the following functions."

    def __init__(self) -> None:
        self._last_spec: CoordinatePlaneSpec | None = None

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        h = _random_coord(settings)
        k = _random_intercept(settings)
        a = random.choice([1, 2])
        fn = f"y = {a}(x - {h})^2 + {k}" if k >= 0 else f"y = {a}(x - {h})^2 - {abs(k)}"
        points = [(h + dx, a * dx * dx + k) for dx in range(-4, 5)]
        self._last_spec = _plane_spec(settings, points=points)
        return fn, "Graph quadratic", fn

    def build_question_metadata(
        self, settings: dict, *, prompt_latex: str, prompt_text: str, answer: str | None,
    ) -> dict[str, Any]:
        if self._last_spec is None:
            return {}
        return coordinate_plane_metadata(self._last_spec, settings, prompt="blank")


class GraphQuadraticInequalityFramework(QuestionFramework):
    instruction_latex = r"\text{Graph the following inequalities.}"
    instruction_text = "Graph the following inequalities."

    def __init__(self) -> None:
        self._last_spec: CoordinatePlaneSpec | None = None

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        h = _random_coord(settings)
        k = _random_intercept(settings)
        symbol = _pick_inequality_symbol()
        fn = f"y {symbol} (x - {h})^2 + {k}"
        points = [(h + dx, dx * dx + k) for dx in range(-4, 5)]
        self._last_spec = _plane_spec(settings, points=points)
        return fn, "Graph quadratic inequality", fn

    def build_question_metadata(
        self, settings: dict, *, prompt_latex: str, prompt_text: str, answer: str | None,
    ) -> dict[str, Any]:
        if self._last_spec is None:
            return {}
        return coordinate_plane_metadata(self._last_spec, settings, prompt="blank")


class NumberLinePlotFramework(QuestionFramework):
    instruction_latex = r"\text{Plot the following numbers on the number line.}"
    instruction_text = "Plot the following numbers on the number line."

    def __init__(self) -> None:
        self._last_value: float | None = None

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        value = random.randint(-10, 10)
        prompt = str(value)
        self._last_value = float(value)
        return prompt, str(value), str(value)

    def build_question_metadata(
        self, settings: dict, *, prompt_latex: str, prompt_text: str, answer: str | None,
    ) -> dict[str, Any]:
        if not include_graph_metadata(settings) or self._last_value is None:
            return {}
        lo, hi, tick = _number_line_bounds(settings, self._last_value)
        spec = NumberLineSpec(
            min_value=lo,
            max_value=hi,
            boundary=self._last_value,
            direction="both",
            inclusive=True,
            tick_interval=tick,
            show_zero=_number_line_show_zero(settings),
        )
        return metadata_from_number_line_spec(spec, prompt="blank")


class ReadSlopeFromGraphFramework(QuestionFramework):
    instruction_latex = r"\text{Find the slope of the line shown.}"
    instruction_text = "Find the slope of the line shown."

    def __init__(self) -> None:
        self._last_spec: CoordinatePlaneSpec | None = None

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        m = _random_slope(settings)
        x1, y1 = _random_point(settings)
        dx = random_int_range(1, 4, exclude=set())
        x2, y2 = x1 + dx, y1 + m * dx
        # Intercept must match the plotted points (same line), not a random b.
        b = y1 - m * x1
        slope = _slope_from_points(x1, y1, x2, y2)
        answer = (
            str(slope.numerator)
            if slope.denominator == 1
            else f"\\frac{{{slope.numerator}}}{{{slope.denominator}}}"
        )
        prompt = "\\text{The line is shown on the coordinate plane. Find the slope.}"
        self._last_spec = _plane_spec(
            settings,
            points=[(x1, y1), (x2, y2)],
            slope=m,
            y_intercept=b,
            functions=[_linear_function_expr(m, b)],
        )
        return prompt, "Read slope from graph", answer

    def build_question_metadata(
        self, settings: dict, *, prompt_latex: str, prompt_text: str, answer: str | None,
    ) -> dict[str, Any]:
        if self._last_spec is None:
            return {}
        return coordinate_plane_metadata(self._last_spec, settings, prompt="stimulus")


class GraphPointTableFramework(QuestionFramework):
    instruction_latex = r"\text{Complete the table and graph each relation.}"
    instruction_text = "Complete the table and graph each relation."

    def __init__(self) -> None:
        self._last_spec: CoordinatePlaneSpec | None = None

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        m = _random_slope(settings)
        b = _random_intercept(settings)
        row_count = int(settings.get("table_row_count", 4))
        coord_min = int(settings.get("coord_min", -6))
        coord_max = int(settings.get("coord_max", 6))
        pool = list(range(coord_min, coord_max + 1))
        xs = sorted(random.sample(pool, k=min(row_count, len(pool))))
        rows = [(x, m * x + b) for x in xs]
        missing_x = random.choice(xs)
        missing_y = m * missing_x + b
        table_rows = [f"{x} & {'?' if x == missing_x else y} \\\\" for x, y in rows]
        table = "\\begin{array}{|c|c|} \\hline x & y \\\\ \\hline " + " ".join(table_rows) + " \\hline \\end{array}"
        prompt = f"y = {m}x + {b} \\\\ {table}"
        self._last_spec = _plane_spec(settings, points=rows, slope=m, y_intercept=b)
        return prompt, f"Table value when x={missing_x}", str(missing_y)

    def build_question_metadata(
        self, settings: dict, *, prompt_latex: str, prompt_text: str, answer: str | None,
    ) -> dict[str, Any]:
        if self._last_spec is None:
            return {}
        return coordinate_plane_metadata(self._last_spec, settings, prompt="blank")


class ReadInterceptFromGraphFramework(QuestionFramework):
    instruction_latex = r"\text{Find the y-intercept of the line shown.}"
    instruction_text = "Find the y-intercept of the line shown."

    def __init__(self) -> None:
        self._last_spec: CoordinatePlaneSpec | None = None

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        m = _random_slope(settings)
        b = _random_intercept(settings)
        prompt = "\\text{The line is shown on the coordinate plane. Find the y-intercept.}"
        self._last_spec = _plane_spec(
            settings,
            slope=m,
            y_intercept=b,
            functions=[_linear_function_expr(m, b)],
        )
        return prompt, "Read intercept from graph", str(b)

    def build_question_metadata(
        self, settings: dict, *, prompt_latex: str, prompt_text: str, answer: str | None,
    ) -> dict[str, Any]:
        if self._last_spec is None:
            return {}
        return coordinate_plane_metadata(self._last_spec, settings, prompt="stimulus")


class ReadEquationFromGraphFramework(QuestionFramework):
    """Write y = mx + b from a line shown on the coordinate plane."""

    instruction_latex = r"\text{Write the equation of the line shown.}"
    instruction_text = "Write the equation of the line shown."

    def __init__(self) -> None:
        self._last_spec: CoordinatePlaneSpec | None = None

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        m = _random_slope(settings)
        b = _random_intercept(settings)
        eq = _slope_intercept_latex(m, b)
        prompt = (
            "\\text{The line is shown on the coordinate plane. "
            "Write its equation in slope-intercept form.}"
        )
        x_sample = _random_coord(settings)
        y_sample = m * x_sample + b
        self._last_spec = _plane_spec(
            settings,
            points=[(0, b), (x_sample, y_sample)],
            slope=m,
            y_intercept=b,
            functions=[_linear_function_expr(m, b)],
        )
        return prompt, "Read equation from graph", eq

    def build_question_metadata(
        self, settings: dict, *, prompt_latex: str, prompt_text: str, answer: str | None,
    ) -> dict[str, Any]:
        if self._last_spec is None:
            return {}
        return coordinate_plane_metadata(self._last_spec, settings, prompt="stimulus")


class GraphTransformationsFramework(QuestionFramework):
    instruction_latex = r"\text{Describe the transformation.}"
    instruction_text = "Describe the transformation."

    def __init__(self) -> None:
        self._last_spec: CoordinatePlaneSpec | None = None

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        h = _random_coord(settings)
        k = _random_intercept(settings)
        fn = f"y = (x - {h})^2 + {k}" if k >= 0 else f"y = (x - {h})^2 - {abs(k)}"
        prompt = f"\\text{{Graph the transformation of }} f(x) = x^2 \\text{{ to }} {fn}."
        points = [(h + dx, dx * dx + k) for dx in range(-4, 5)]
        self._last_spec = _plane_spec(settings, points=points)
        return prompt, "Graph transformation", fn

    def build_question_metadata(
        self, settings: dict, *, prompt_latex: str, prompt_text: str, answer: str | None,
    ) -> dict[str, Any]:
        if self._last_spec is None:
            return {}
        return coordinate_plane_metadata(self._last_spec, settings, prompt="blank")


class GraphingFramework(QuestionFramework):
    """Tier-2 skeleton — use concrete frameworks in this module instead."""

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        raise NotImplementedError("Use a concrete graphing framework class.")
