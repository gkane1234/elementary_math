"""Graphing framework — coordinate plane, slope, and number-line metadata."""

from __future__ import annotations

import math
import random
import re
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Literal

from .base import QuestionFramework
from ..core.metadata import GraphSpec, question_metadata
from ..settings.params import allowed_inequality_symbols
from ..generators.utils import (
    format_monomial_latex,
    format_polynomial_latex,
    format_slope_intercept_latex,
    random_int_range,
)

Quadrant = Literal["I", "II", "III", "IV", "all"]
NumberLineDirection = Literal["left", "right", "both", "outside"]


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
    inclusive_high: bool | None = None
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
    # Inequality half-planes: {"kind":"half_plane","m":…,"b":…,"op":">="}
    regions: list[dict[str, Any]] = field(default_factory=list)

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
_COMPOUND_INEQUALITY = re.compile(
    r"^(-?\d+(?:\.\d+)?)\s*(\\leq|<=|<)\s*(\w+)\s*(\\leq|<=|<)\s*(-?\d+(?:\.\d+)?)$"
)
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
    outside: bool = False,
    inclusive: bool | None = None,
    inclusive_high: bool | None = None,
) -> NumberLineSpec:
    extras = (boundary,) if boundary_high is None else (boundary, boundary_high)
    lo, hi, tick = _number_line_bounds(settings, *extras)
    show_zero = _number_line_show_zero(settings)
    symbol_inclusive = symbol in {r"\leq", r"\geq", "<=", ">="}
    if boundary_high is not None:
        low_inclusive = bool(inclusive) if inclusive is not None else symbol_inclusive
        high_inclusive = (
            bool(inclusive_high) if inclusive_high is not None else low_inclusive
        )
        return NumberLineSpec(
            min_value=lo,
            max_value=hi,
            boundary=boundary,
            boundary_high=boundary_high,
            direction="outside" if outside else "both",
            inclusive=low_inclusive,
            inclusive_high=high_inclusive,
            tick_interval=tick,
            show_zero=show_zero,
        )
    direction, detected = symbol_to_direction(symbol)
    return NumberLineSpec(
        min_value=lo,
        max_value=hi,
        boundary=boundary,
        direction=direction,
        inclusive=bool(inclusive) if inclusive is not None else detected,
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
    if spec.inclusive_high is not None:
        data["inclusive_high"] = spec.inclusive_high
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
    """Axes/grid/bounds only — no solution curves, points, or shaded regions."""
    return {
        "x_min": graph["x_min"],
        "x_max": graph["x_max"],
        "y_min": graph["y_min"],
        "y_max": graph["y_max"],
        "functions": [],
        "points": [],
        "show_grid": graph.get("show_grid", True),
        "show_points": False,
        "regions": [],
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
            inclusive_high=spec.inclusive_high,
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
        low_sym = compound.group(2)
        high_sym = compound.group(4)
        high = _parse_numeric(compound.group(5))
        return number_line_spec_from_symbol_and_value(
            "<",
            low,
            settings,
            boundary_high=high,
            inclusive=low_sym in {"<=", r"\leq"},
            inclusive_high=high_sym in {"<=", r"\leq"},
        )

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

    result: GraphSpec = {
        "x_min": x_min,
        "x_max": x_max,
        "y_min": y_min,
        "y_max": y_max,
        "functions": functions,
        "points": list(spec.points),
        "show_grid": spec.show_grid,
        "show_points": spec.show_points,
    }
    if spec.regions:
        result["regions"] = list(spec.regions)
    return result


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
    term = format_monomial_latex(value, variable=variable or "", degree=1 if variable else 0)
    if term is None:
        return "0"
    return term


def _slope_intercept_latex(m: int, b: int) -> str:
    return format_slope_intercept_latex(m, b)


def _system_latex(eq1: str, eq2: str) -> str:
    return f"\\begin{{cases}} {eq1} \\\\ {eq2} \\end{{cases}}"


def _slope_from_points(x1: int, y1: int, x2: int, y2: int):
    from fractions import Fraction
    return Fraction(y2 - y1, x2 - x1)


def _plane_spec(
    settings: dict,
    *,
    points: list[tuple[float, float]] | None = None,
    slope: int | None = None,
    y_intercept: int | None = None,
    functions: list[str] | None = None,
    regions: list[dict[str, Any]] | None = None,
) -> CoordinatePlaneSpec:
    return CoordinatePlaneSpec(
        points=[(float(x), float(y)) for x, y in (points or [])],
        functions=list(functions or []),
        slope=float(slope) if slope is not None else None,
        y_intercept=float(y_intercept) if y_intercept is not None else None,
        show_grid=bool(settings.get("show_grid", True)),
        show_points=bool(settings.get("show_points", True)),
        quadrant=settings.get("quadrant", "all"),  # type: ignore[arg-type]
        regions=list(regions or []),
    )


def _inequality_op(symbol: str) -> str:
    """Normalize LaTeX/ASCII inequality symbols to a GraphRegion op."""
    if symbol in {r"\geq", ">=", "≥"}:
        return ">="
    if symbol in {r"\leq", "<=", "≤"}:
        return "<="
    if symbol == ">":
        return ">"
    return "<"


def _half_plane_region(m: float, b: float, symbol: str) -> dict[str, Any]:
    return {
        "kind": "half_plane",
        "m": float(m),
        "b": float(b),
        "op": _inequality_op(symbol),
    }


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
            lo_bound, hi_bound = _bounds(settings, "number_line_min", "number_line_max", -8, 8)
            # Keep the marked value strictly inside the visible window.
            inner_lo = lo_bound + 1 if hi_bound - lo_bound > 2 else lo_bound
            inner_hi = hi_bound - 1 if hi_bound - lo_bound > 2 else hi_bound
            if inner_lo > inner_hi:
                inner_lo, inner_hi = lo_bound, hi_bound
            boundary = random.randint(inner_lo, inner_hi)
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
            settings,
            slope=m,
            y_intercept=b,
            functions=[_linear_function_expr(m, b)],
            regions=[_half_plane_region(float(m), float(b), symbol)],
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
        allow_h = bool(settings.get("allow_shift_h", True))
        allow_k = bool(settings.get("allow_shift_k", False))
        allow_stretch = bool(settings.get("allow_stretch", False))
        allow_reflection = bool(settings.get("allow_reflection", False))
        integer_only = bool(settings.get("integer_only", True))

        # Hard unlocks full vertex form when all transform families are on and
        # fractional coefficients are allowed. Medium keeps translate XOR stretch.
        full_form = (
            allow_h
            and allow_k
            and (allow_stretch or allow_reflection)
            and not integer_only
        )
        if full_form:
            mode = "full"
        elif allow_k and (allow_stretch or allow_reflection):
            mode = random.choice(["translate", "stretch"])
        elif allow_k:
            mode = "translate"
        elif allow_stretch or allow_reflection:
            mode = "stretch"
        else:
            mode = "basic"

        a: int | Fraction = 1
        h = 0
        k = 0

        if mode == "basic":
            if allow_h and random.random() < 0.65:
                h = _nonzero_coord(settings)
        elif mode == "translate":
            a = 1
            if allow_h:
                h = _nonzero_coord(settings) if random.random() < 0.8 else 0
            k = _nonzero_intercept(settings)
        elif mode == "stretch":
            a = _pick_abs_coef(
                settings,
                allow_stretch=allow_stretch,
                allow_reflection=allow_reflection,
                integer_only=integer_only,
                prefer_nonunit=True,
            )
            h = 0
            k = 0
        else:  # full
            a = _pick_abs_coef(
                settings,
                allow_stretch=allow_stretch,
                allow_reflection=allow_reflection,
                integer_only=integer_only,
                prefer_nonunit=True,
            )
            h = _nonzero_coord(settings) if allow_h else 0
            k = _nonzero_intercept(settings) if allow_k else 0
            # Bias away from the parent shape so hard stays distinct from easy.
            if a == 1 and (allow_stretch or allow_reflection):
                a = _pick_abs_coef(
                    settings,
                    allow_stretch=allow_stretch,
                    allow_reflection=allow_reflection,
                    integer_only=integer_only,
                    prefer_nonunit=True,
                )

        eq = _format_abs_latex(a=a, h=h, k=k)
        a_float = float(a)
        expr = _abs_function_expr(a_float, h, k)
        wing = 3.0
        features = [
            (float(h), float(k)),
            (float(h) + wing, a_float * wing + float(k)),
            (float(h) - wing, a_float * wing + float(k)),
        ]
        x_min, x_max, y_min, y_max = origin_centered_bounds(features, settings=settings)
        self._last_spec = CoordinatePlaneSpec(
            points=[],
            functions=[expr],
            show_grid=bool(settings.get("show_grid", True)),
            show_points=False,
            quadrant=settings.get("quadrant", "all"),  # type: ignore[arg-type]
            x_min=x_min,
            x_max=x_max,
            y_min=y_min,
            y_max=y_max,
        )
        return eq, "Graph absolute value", eq

    def build_question_metadata(
        self, settings: dict, *, prompt_latex: str, prompt_text: str, answer: str | None,
    ) -> dict[str, Any]:
        if self._last_spec is None:
            return {}
        return coordinate_plane_metadata(self._last_spec, settings, prompt="blank")


def _nonzero_coord(settings: dict) -> int:
    value = _random_coord(settings)
    if value != 0:
        return value
    lo, hi = _bounds(settings, "coord_min", "coord_max", -5, 5)
    candidates = [n for n in range(lo, hi + 1) if n != 0]
    return random.choice(candidates) if candidates else 1


def _nonzero_intercept(settings: dict) -> int:
    value = _random_intercept(settings)
    if value != 0:
        return value
    lo, hi = _bounds(settings, "intercept_min", "intercept_max", -5, 5)
    candidates = [n for n in range(lo, hi + 1) if n != 0]
    return random.choice(candidates) if candidates else 1


def _pick_abs_coef(
    settings: dict,
    *,
    allow_stretch: bool,
    allow_reflection: bool,
    integer_only: bool,
    prefer_nonunit: bool = False,
) -> int | Fraction:
    lo, hi = _bounds(settings, "coef_min", "coef_max", 1, 2)
    choices: list[int | Fraction] = []

    if integer_only:
        max_mag = max(abs(lo), abs(hi), 1)
        for n in range(1, max_mag + 1):
            if not allow_stretch and n != 1:
                continue
            if n <= hi:
                choices.append(n)
            if allow_reflection and -n >= lo:
                choices.append(-n)
    else:
        pool = [
            Fraction(1, 2),
            Fraction(3, 2),
            Fraction(1),
            Fraction(2),
            Fraction(3),
        ]
        for f in pool:
            if not allow_stretch and f != 1:
                continue
            if float(f) <= hi + 1e-12:
                choices.append(f)
            if allow_reflection and float(-f) >= lo - 1e-12:
                choices.append(-f)

    if not allow_reflection:
        choices = [c for c in choices if c > 0]
    if not choices:
        choices = [1]

    if prefer_nonunit:
        interesting = [c for c in choices if c != 1]
        if interesting:
            choices = interesting

    return random.choice(choices)


def _format_abs_coef_latex(a: int | Fraction) -> str:
    if isinstance(a, Fraction):
        if a.denominator == 1:
            a = a.numerator
        else:
            sign = "-" if a < 0 else ""
            return f"{sign}\\frac{{{abs(a.numerator)}}}{{{a.denominator}}}"
    if a == 1:
        return ""
    if a == -1:
        return "-"
    return str(a)


def _format_abs_inner(h: int) -> str:
    if h == 0:
        return "x"
    if h > 0:
        return f"x - {h}"
    return f"x + {abs(h)}"


def _format_abs_latex(*, a: int | Fraction, h: int, k: int) -> str:
    coef = _format_abs_coef_latex(a)
    body = f"{coef}|{_format_abs_inner(h)}|"
    if k == 0:
        return f"y = {body}"
    sign = "+" if k > 0 else "-"
    return f"y = {body} {sign} {abs(k)}"


def _abs_function_expr(a: float, h: int, k: int) -> str:
    """Emit a*abs(x-h)+k for the frontend / SVG abs sampler."""
    shift = -h
    if abs(a - 1.0) < 1e-12:
        head = "abs(x"
    else:
        head = f"{a:g}*abs(x"
    mid = f"{shift:+g}" if shift != 0 else ""
    body = f"{head}{mid})"
    if k == 0:
        return body
    return f"{body}{k:+d}"


def _pick_quad_coef(
    settings: dict,
    *,
    allow_stretch: bool,
    allow_reflection: bool,
    integer_only: bool,
    prefer_nonunit: bool = False,
) -> int | Fraction:
    """Pick leading coefficient a for y = a(x−h)² + k."""
    if bool(settings.get("leading_coefficient_one", False)) or bool(
        settings.get("monic_only", False)
    ):
        return 1

    lo, hi = _bounds(settings, "coef_min", "coef_max", 1, 2)
    choices: list[int | Fraction] = []

    if integer_only:
        max_mag = max(abs(lo), abs(hi), 1)
        for n in range(1, max_mag + 1):
            if not allow_stretch and n != 1:
                continue
            if n <= hi:
                choices.append(n)
            if allow_reflection and -n >= lo:
                choices.append(-n)
    else:
        pool = [
            Fraction(1, 2),
            Fraction(3, 2),
            Fraction(1),
            Fraction(2),
            Fraction(3),
        ]
        for f in pool:
            if not allow_stretch and f != 1:
                continue
            if float(f) <= hi + 1e-12:
                choices.append(f)
            if allow_reflection and float(-f) >= lo - 1e-12:
                choices.append(-f)

    if not allow_reflection:
        choices = [c for c in choices if c > 0]
    if not choices:
        choices = [1]

    if prefer_nonunit:
        interesting = [c for c in choices if c != 1]
        if interesting:
            choices = interesting

    return random.choice(choices)


def _format_quad_coef_latex(a: int | Fraction) -> str:
    if isinstance(a, Fraction):
        if a.denominator == 1:
            a = a.numerator
        else:
            sign = "-" if a < 0 else ""
            return f"{sign}\\frac{{{abs(a.numerator)}}}{{{a.denominator}}}"
    if a == 1:
        return ""
    if a == -1:
        return "-"
    return str(a)


def _format_quad_vertex_latex(*, a: int | Fraction, h: int, k: int) -> str:
    coef = _format_quad_coef_latex(a)
    if h == 0:
        body = f"{coef}x^2"
    elif h > 0:
        body = f"{coef}(x - {h})^2"
    else:
        body = f"{coef}(x + {abs(h)})^2"
    if k == 0:
        return f"y = {body}"
    sign = "+" if k > 0 else "-"
    return f"y = {body} {sign} {abs(k)}"


def _format_quad_standard_term(coef: int | Fraction, *, variable: str) -> str | None:
    if coef == 0:
        return None
    if isinstance(coef, Fraction) and coef.denominator != 1:
        sign = "-" if coef < 0 else ""
        latex = f"{sign}\\frac{{{abs(coef.numerator)}}}{{{coef.denominator}}}{variable}"
        return latex
    n = int(coef) if isinstance(coef, Fraction) else int(coef)
    if variable == "":
        return str(n)
    if n == 1:
        return variable
    if n == -1:
        return f"-{variable}"
    return f"{n}{variable}"


def _format_quad_standard_latex(*, a: int | Fraction, b: int | Fraction, c: int | Fraction) -> str:
    return f"y = {format_polynomial_latex([a, b, c])}"


def _format_quad_factor(root: int) -> str:
    if root == 0:
        return "x"
    if root > 0:
        return f"(x - {root})"
    return f"(x + {abs(root)})"


def _format_quad_factored_latex(*, a: int | Fraction, r: int, s: int) -> str:
    coef = _format_quad_coef_latex(a)
    return f"y = {coef}{_format_quad_factor(r)}{_format_quad_factor(s)}"


def _format_signed_const(value: int | Fraction) -> str:
    if isinstance(value, Fraction) and value.denominator != 1:
        sign = "-" if value < 0 else ""
        return f"{sign}\\frac{{{abs(value.numerator)}}}{{{value.denominator}}}"
    n = int(value)
    return str(n)


def _as_int_if_whole(value: int | Fraction) -> int | Fraction:
    if isinstance(value, Fraction) and value.denominator == 1:
        return int(value.numerator)
    if isinstance(value, Fraction):
        return value
    return int(value)


def _quad_abc(a: int | Fraction, h: int | float, k: int | float) -> tuple[int | Fraction, int | Fraction, int | Fraction]:
    b = -2 * a * h
    c = a * h * h + k
    return _as_int_if_whole(a), _as_int_if_whole(b), _as_int_if_whole(c)


def _quad_function_expr(a: float, h: float, k: float) -> str:
    """Emit expanded ax^2+bx+c for the frontend sampler."""
    aa = a
    bb = -2.0 * a * h
    cc = a * h * h + k
    return f"{aa:g}*x^2+{bb:g}*x+{cc:g}"


def _format_messy_quadratic_latex(
    *,
    a: int | Fraction,
    h: int,
    k: int,
    light: bool,
) -> str:
    """Present a parabola so the student must rearrange before graphing."""
    aa, bb, cc = _quad_abc(a, h, k)

    light_styles = ["point_vertex", "partial_expand"]
    heavy_styles = ["point_vertex", "partial_expand", "isolate_y", "distribute_binom"]
    style = random.choice(light_styles if light else heavy_styles)

    if style == "point_vertex":
        # y - k = a(x - h)^2
        left = "y" if k == 0 else (f"y - {k}" if k > 0 else f"y + {abs(k)}")
        right = _format_quad_vertex_latex(a=a, h=h, k=0).replace("y = ", "")
        return f"{left} = {right}"

    if style == "partial_expand":
        # y = a(x^2 - 2hx) + (ah^2 + k)
        two_h = 2 * h
        const = _as_int_if_whole(a * h * h + k)
        if two_h == 0:
            inner = "x^2"
        elif two_h > 0:
            inner = f"x^2 - {two_h}x"
        else:
            inner = f"x^2 + {abs(two_h)}x"
        if a == 1:
            body = f"({inner})"
        elif a == -1:
            body = f"-({inner})"
        else:
            body = f"{_format_quad_coef_latex(a)}({inner})"
        const_f = float(const)
        if abs(const_f) < 1e-12:
            return f"y = {body}"
        sign = "+" if const_f > 0 else "-"
        mag = abs(const) if isinstance(const, Fraction) else abs(int(const))
        return f"y = {body} {sign} {_format_signed_const(mag)}"

    if style == "isolate_y":
        # From y = aa x^2 + bb x + cc  =>  (-aa)x^2 + (-bb)x + y = cc
        neg_a = _as_int_if_whole(-aa)
        neg_b = _as_int_if_whole(-bb)
        poly = _format_quad_standard_latex(a=neg_a, b=neg_b, c=0).replace("y = ", "")
        rhs = _format_signed_const(cc)
        if not poly:
            return f"y = {rhs}"
        return f"{poly} + y = {rhs}".replace("+ -", "- ")

    # distribute_binom: y = a(x-r)(x-s) + m
    d = random.randint(1, 3)
    r = h - d
    s = h + d
    m = _as_int_if_whole(k + a * d * d)
    factored = _format_quad_factored_latex(a=a, r=r, s=s).replace("y = ", "")
    m_f = float(m)
    if abs(m_f) < 1e-12:
        return f"y = {factored}"
    sign = "+" if m_f > 0 else "-"
    mag = abs(m) if isinstance(m, Fraction) else abs(int(m))
    return f"y = {factored} {sign} {_format_signed_const(mag)}"


def _pick_quadratic_form(settings: dict, *, complexity: str) -> str:
    """Choose presentation form from enabled toggles and difficulty."""
    allow_vertex = bool(settings.get("allow_vertex_form", True))
    allow_standard = bool(settings.get("allow_standard_form", False))
    allow_factored = bool(settings.get("allow_factored_form", False))
    allow_messy = bool(settings.get("allow_messy_form", False))

    weighted: list[tuple[str, float]] = []
    if complexity == "easy":
        if allow_vertex:
            weighted.append(("vertex", 1.0))
    elif complexity == "medium":
        if allow_vertex:
            weighted.append(("vertex", 0.30))
        if allow_standard:
            weighted.append(("standard", 0.25))
        if allow_factored:
            weighted.append(("factored", 0.30))
        if allow_messy:
            weighted.append(("messy", 0.15))
    else:
        if allow_messy:
            weighted.append(("messy", 0.45))
        if allow_standard:
            weighted.append(("standard", 0.20))
        if allow_factored:
            weighted.append(("factored", 0.20))
        if allow_vertex:
            weighted.append(("vertex", 0.15))

    if not weighted:
        # Fallbacks if toggles are all off
        if allow_messy:
            weighted.append(("messy", 1.0))
        elif allow_standard:
            weighted.append(("standard", 1.0))
        elif allow_factored:
            weighted.append(("factored", 1.0))
        else:
            weighted.append(("vertex", 1.0))

    forms = [f for f, _ in weighted]
    weights = [w for _, w in weighted]
    return random.choices(forms, weights=weights, k=1)[0]


def _sample_quadratic_params(
    settings: dict,
    *,
    complexity: str,
) -> tuple[int | Fraction, int, int]:
    """Pick (a, h, k) for the underlying parabola."""
    allow_h = bool(settings.get("allow_shift_h", True))
    allow_k = bool(settings.get("allow_shift_k", True))
    allow_stretch = bool(settings.get("allow_stretch", False))
    allow_reflection = bool(settings.get("allow_reflection", False))
    integer_only = bool(settings.get("integer_only", True))

    if complexity == "easy":
        a: int | Fraction = 1
        modes: list[str] = ["parent"]
        if allow_h:
            modes.append("shift_h")
        if allow_k:
            modes.append("shift_k")
        mode = random.choice(modes)
        h = _nonzero_coord(settings) if mode == "shift_h" else 0
        k = _nonzero_intercept(settings) if mode == "shift_k" else 0
        return a, h, k

    prefer_nonunit = complexity != "easy"
    a = _pick_quad_coef(
        settings,
        allow_stretch=allow_stretch or complexity == "hard",
        allow_reflection=allow_reflection,
        integer_only=integer_only if complexity != "hard" else integer_only,
        prefer_nonunit=prefer_nonunit,
    )
    if complexity == "hard" and a == 1:
        a = _pick_quad_coef(
            settings,
            allow_stretch=True,
            allow_reflection=allow_reflection,
            integer_only=integer_only,
            prefer_nonunit=True,
        )

    h = _nonzero_coord(settings) if allow_h else 0
    k = _nonzero_intercept(settings) if allow_k else 0
    # Medium/hard: both shifts when allowed
    if complexity in {"medium", "hard"} and allow_h and allow_k:
        if h == 0:
            h = _nonzero_coord(settings)
        if k == 0:
            k = _nonzero_intercept(settings)
    return a, h, k


def _sample_factored_roots(settings: dict, h: int) -> tuple[int, int]:
    """Distinct integer roots straddling h when possible (even sum → integer vertex)."""
    lo, hi = _bounds(settings, "coord_min", "coord_max", -5, 5)
    d = random.randint(1, 3)
    r, s = h - d, h + d
    if r == s:
        s = r + 2
    if r < lo - 2 or s > hi + 2:
        candidates = [n for n in range(lo, hi + 1)]
        if len(candidates) < 2:
            candidates = [-3, -1, 1, 3]
        r = random.choice(candidates)
        options = [n for n in candidates if n != r and (r + n) % 2 == 0]
        s = random.choice(options) if options else r + 2
    if r > s:
        r, s = s, r
    return r, s


def _sample_quadratic_graph(settings: dict) -> tuple[str, float, float, float, str]:
    """Return (prompt_latex, a, h, k, function_expr) for a graphing quadratic.

    Difficulty is inferred from settings flags:
      easy   — clean vertex; a = 1; one-axis shift; no rewrite
      medium — mix vertex / standard / factored; light messy sometimes
      hard   — often messy (needs algebra); fractional a; wider ranges
    """
    tier = str(settings.get("difficulty_tier", "")).strip().lower()
    if tier in {"easy", "medium", "hard"}:
        complexity = tier
    else:
        allow_messy = bool(settings.get("allow_messy_form", False))
        allow_standard = bool(settings.get("allow_standard_form", False))
        allow_factored = bool(settings.get("allow_factored_form", False))
        integer_only = bool(settings.get("integer_only", True))
        allow_stretch = bool(settings.get("allow_stretch", False))
        allow_reflection = bool(settings.get("allow_reflection", False))

        if not integer_only:
            complexity = "hard"
        elif allow_messy or allow_standard or allow_factored or allow_stretch or allow_reflection:
            complexity = "medium"
        else:
            complexity = "easy"

    form = _pick_quadratic_form(settings, complexity=complexity)
    a, h, k = _sample_quadratic_params(settings, complexity=complexity)

    # Factored form: rebuild from integer roots so intercepts are clean
    if form == "factored":
        r, s = _sample_factored_roots(settings, h)
        # Recompute vertex from roots
        h = (r + s) // 2 if (r + s) % 2 == 0 else (r + s) / 2  # type: ignore[assignment]
        if isinstance(h, float) and h == int(h):
            h = int(h)
        # Keep integer h for medium when possible
        if complexity == "medium" and isinstance(h, float):
            # Nudge s so r+s is even
            s = s + 1 if (r + s) % 2 else s
            h = (r + s) // 2
        k_val = a * (float(h) - r) * (float(h) - s)
        k = int(k_val) if float(k_val) == int(k_val) else k  # prefer exact
        if float(k_val) == int(k_val):
            k = int(k_val)
        else:
            # Fall back: keep a,r,s and accept float k via expr
            k = int(round(float(k_val)))
        latex = _format_quad_factored_latex(a=a, r=r, s=s)
        h_f = float(h)
        k_f = float(a) * (h_f - r) * (h_f - s)
        a_float = float(a)
        return latex, a_float, h_f, k_f, _quad_function_expr(a_float, h_f, k_f)

    a_float = float(a)
    h_f = float(h)
    k_f = float(k)
    expr = _quad_function_expr(a_float, h_f, k_f)

    if form == "standard":
        aa, bb, cc = _quad_abc(a, h, k)
        latex = _format_quad_standard_latex(a=aa, b=bb, c=cc)
    elif form == "messy":
        latex = _format_messy_quadratic_latex(
            a=a, h=int(h), k=int(k), light=(complexity != "hard"),
        )
    else:
        latex = _format_quad_vertex_latex(a=a, h=int(h), k=int(k))

    return latex, a_float, h_f, k_f, expr


def _flip_inequality_symbol(symbol: str) -> str:
    return {
        ">": "<",
        "<": ">",
        r"\geq": r"\leq",
        r"\leq": r"\geq",
    }.get(symbol, symbol)


def _pick_quad_inequality_symbol(settings: dict) -> str:
    return random.choice(allowed_inequality_symbols(settings))


def _equation_to_inequality_latex(eq_latex: str, symbol: str) -> str:
    """Turn ``y = …`` / ``lhs = rhs`` equation latex into an inequality."""
    if " = " not in eq_latex:
        return eq_latex
    left, right = eq_latex.split(" = ", 1)
    if right.strip() == "y":
        return f"{left} {_flip_inequality_symbol(symbol)} y"
    return f"{left} {symbol} {right}"


def _scale_y_inequality(eq_latex: str, symbol: str) -> str | None:
    """Optionally rewrite ``y = rhs`` as ``m y ⋈ rhs`` (divide both sides)."""
    if not eq_latex.startswith("y = "):
        return None
    m = random.choice([2, 3])
    return f"{m}y {symbol} {eq_latex[4:]}"


def _sample_quadratic_inequality(
    settings: dict,
) -> tuple[str, float, float, float, str, str]:
    """Return (prompt_latex, a, h, k, function_expr, symbol).

    Easy: clean vertex or standard; little rewrite.
    Medium: expand / move terms; factored or a≠1 vertex.
    Hard: messy rewrite, completing-the-square (standard), factored, scale sides.
    """
    symbol = _pick_quad_inequality_symbol(settings)
    latex, a, h, k, expr = _sample_quadratic_graph(settings)
    tier = str(settings.get("difficulty_tier", "")).strip().lower()
    allow_messy = bool(settings.get("allow_messy_form", False))

    # Hard: sometimes force a multiply-both-sides presentation on a clean RHS.
    if (
        tier == "hard"
        and allow_messy
        and latex.startswith("y = ")
        and random.random() < 0.4
    ):
        scaled = _scale_y_inequality(latex, symbol)
        if scaled is not None:
            return scaled, a, h, k, expr, symbol

    prompt = _equation_to_inequality_latex(latex, symbol)
    return prompt, a, h, k, expr, symbol


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
            regions=[
                _half_plane_region(float(m1), float(b1), sym1),
                _half_plane_region(float(m2), float(b2), sym2),
            ],
        )
        return prompt, "Graph system of inequalities", answer

    def build_question_metadata(
        self, settings: dict, *, prompt_latex: str, prompt_text: str, answer: str | None,
    ) -> dict[str, Any]:
        if self._last_spec is None:
            return {}
        return coordinate_plane_metadata(self._last_spec, settings, prompt="blank")


def _exp_bool(settings: dict, key: str, default: bool = False) -> bool:
    return bool(settings.get(key, default))


def _exp_integer_bases(settings: dict) -> list[int]:
    lo, hi = _bounds(settings, "exp_base_min", "exp_base_max", 2, 5)
    lo = max(2, lo)
    hi = max(lo, hi)
    return list(range(lo, hi + 1))


def _format_exp_base_latex(base: float, integer_base: int, *, decay: bool) -> str:
    if decay:
        return rf"\left(\frac{{1}}{{{integer_base}}}\right)"
    if float(base).is_integer():
        return str(int(base))
    return f"{base:g}"


def _format_exp_latex(*, a: int, base_latex: str, h: int, k: int) -> str:
    """Build y = a · b^(x−h) + k with tidy signs."""
    if h == 0:
        exponent = "x"
    elif h > 0:
        exponent = f"x - {h}"
    else:
        exponent = f"x + {abs(h)}"

    power = f"{base_latex}^{{{exponent}}}"
    if a == 1:
        body = power
    elif a == -1:
        body = f"-{power}"
    else:
        body = f"{a} \\cdot {power}"

    if k == 0:
        return f"y = {body}"
    sign = "+" if k > 0 else "-"
    return f"y = {body} {sign} {abs(k)}"


def _format_exp_function_expr(
    *, a: int, base: float, integer_base: int, decay: bool, h: int, k: int
) -> str:
    """Canonical form for the frontend sampler: a*b^(x-h)+k."""
    base_s = f"(1/{integer_base})" if decay else f"{int(base)}"
    if h == 0:
        power = f"{base_s}^x"
    else:
        inner = f"x{-h:+d}"
        power = f"{base_s}^({inner})"
    if a == 1:
        body = power
    else:
        body = f"{a}*{power}"
    if k == 0:
        return body
    return f"{body}{k:+d}"


def _sample_exp_points(
    *, a: int, base: float, h: int, k: int, x_values: range
) -> list[tuple[float, float]]:
    points: list[tuple[float, float]] = []
    for x in x_values:
        try:
            y = a * (base ** (x - h)) + k
        except OverflowError:
            continue
        if not isinstance(y, (int, float)):
            continue
        if y != y or abs(y) > 1e6:  # NaN / huge
            continue
        points.append((float(x), float(y)))
    return points


class GraphExponentialFramework(QuestionFramework):
    instruction_latex = r"\text{Graph the following functions.}"
    instruction_text = "Graph the following functions."

    def __init__(self) -> None:
        self._last_spec: CoordinatePlaneSpec | None = None

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        integer_bases = _exp_integer_bases(settings)
        integer_base = random.choice(integer_bases)

        allow_decay = _exp_bool(settings, "allow_decay")
        allow_stretch = _exp_bool(settings, "allow_stretch")
        allow_vertical = _exp_bool(settings, "allow_vertical_shift")
        allow_horizontal = _exp_bool(settings, "allow_horizontal_shift")
        allow_reflection = _exp_bool(settings, "allow_reflection")

        decay = bool(allow_decay and random.choice([True, False]))
        base = 1.0 / integer_base if decay else float(integer_base)

        a = 1
        if allow_stretch and allow_reflection:
            a = random.choice([-3, -2, -1, 1, 2, 3])
        elif allow_stretch:
            a = random.choice([1, 2, 3])
        elif allow_reflection:
            a = random.choice([-1, 1])

        h = 0
        if allow_horizontal:
            # Prefer a real shift on medium/hard so forms differ from easy.
            h = random.choice([-2, -1, 1, 2]) if random.random() < 0.75 else 0

        k = 0
        if allow_vertical:
            k = random.choice([-3, -2, -1, 1, 2, 3]) if random.random() < 0.75 else 0

        # Hard: when all transforms are allowed, bias toward a fuller form.
        if allow_reflection and allow_horizontal and allow_vertical and allow_stretch:
            if a == 1 and random.random() < 0.5:
                a = random.choice([-2, -1, 2, 3])
            if h == 0:
                h = random.choice([-2, -1, 1, 2])
            if k == 0:
                k = random.choice([-3, -2, -1, 1, 2, 3])

        base_latex = _format_exp_base_latex(base, integer_base, decay=decay)
        fn = _format_exp_latex(a=a, base_latex=base_latex, h=h, k=k)
        expr = _format_exp_function_expr(
            a=a, base=base, integer_base=integer_base, decay=decay, h=h, k=k,
        )

        points = _sample_exp_points(
            a=a, base=base, h=h, k=k, x_values=range(h - 3, h + 4),
        )
        nice_points = [
            (x, y) for x, y in points if abs(y - round(y)) < 1e-9
        ]
        marker_points = nice_points if nice_points else points[:5]

        self._last_spec = _plane_spec(settings, points=marker_points, functions=[expr])
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
        latex, a, h, k, expr = _sample_quadratic_graph(settings)
        wing = 3.0
        features = [
            (h, k),
            (h + wing, a * wing * wing + k),
            (h - wing, a * wing * wing + k),
        ]
        x_min, x_max, y_min, y_max = origin_centered_bounds(features, settings=settings)
        self._last_spec = CoordinatePlaneSpec(
            points=[],
            functions=[expr],
            show_grid=bool(settings.get("show_grid", True)),
            show_points=False,
            quadrant=settings.get("quadrant", "all"),  # type: ignore[arg-type]
            x_min=x_min,
            x_max=x_max,
            y_min=y_min,
            y_max=y_max,
        )
        return latex, "Graph quadratic", latex

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
        prompt, a, h, k, expr, symbol = _sample_quadratic_inequality(settings)
        wing = 3.0
        features = [
            (h, k),
            (h + wing, a * wing * wing + k),
            (h - wing, a * wing * wing + k),
        ]
        x_min, x_max, y_min, y_max = origin_centered_bounds(features, settings=settings)
        self._last_spec = CoordinatePlaneSpec(
            points=[],
            functions=[expr],
            show_grid=bool(settings.get("show_grid", True)),
            show_points=False,
            quadrant=settings.get("quadrant", "all"),  # type: ignore[arg-type]
            x_min=x_min,
            x_max=x_max,
            y_min=y_min,
            y_max=y_max,
        )
        inclusive = symbol in {r"\geq", r"\leq"}
        answer = (
            f"{prompt} \\text{{ (solid boundary)}}"
            if inclusive
            else f"{prompt} \\text{{ (dashed boundary)}}"
        )
        return prompt, "Graph quadratic inequality", answer

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
        b = _random_intercept(settings)
        prompt = "\\text{The line is shown on the coordinate plane. Find the slope.}"
        # Line only — marked points would reveal rise/run.
        self._last_spec = _plane_spec(
            settings,
            points=[],
            slope=m,
            y_intercept=b,
            functions=[_linear_function_expr(m, b)],
        )
        self._last_spec.show_points = False
        return prompt, "Read slope from graph", str(m)

    def build_question_metadata(
        self, settings: dict, *, prompt_latex: str, prompt_text: str, answer: str | None,
    ) -> dict[str, Any]:
        if self._last_spec is None:
            return {}
        self._last_spec.points = []
        self._last_spec.show_points = False
        forced = {**settings, "show_points": False}
        return coordinate_plane_metadata(self._last_spec, forced, prompt="stimulus")


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
        prompt = f"{_slope_intercept_latex(m, b)} \\\\ {table}"
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


def _sample_solve_poly_roots(settings: dict) -> tuple[int, ...]:
    """Distinct integer roots sized by root_min / root_max (fallback: coord bounds)."""
    lo, hi = _bounds(settings, "root_min", "root_max", -3, 3)
    if lo == hi:
        lo, hi = lo - 1, hi + 1
    pool = list(range(lo, hi + 1))
    degree = max(2, min(3, int(settings.get("max_degree", 2))))
    min_degree = max(2, min(degree, int(settings.get("min_degree", 2))))
    n_roots = random.randint(min_degree, degree)
    n_roots = min(n_roots, len(pool))
    n_roots = max(2, n_roots)
    if len(pool) < n_roots:
        pool = list(range(-n_roots, n_roots + 1))
    return tuple(sorted(random.sample(pool, n_roots)))


def _poly_from_roots(a: int | Fraction, roots: tuple[int, ...]) -> list[int | Fraction]:
    """Expand a(x−r1)(x−r2)… into descending coefficients."""
    coeffs: list[int | Fraction] = [a]
    for root in roots:
        next_coeffs: list[int | Fraction] = [0] * (len(coeffs) + 1)
        for i, coef in enumerate(coeffs):
            next_coeffs[i] += coef
            next_coeffs[i + 1] += coef * (-root)
        coeffs = next_coeffs
    return [_as_int_if_whole(c) for c in coeffs]


def _poly_function_expr(coeffs: list[int | Fraction]) -> str:
    """Frontend sampler expression: a*x^n+… (quadratic / cubic)."""
    degree = len(coeffs) - 1
    parts: list[str] = []
    for i, coef in enumerate(coeffs):
        power = degree - i
        value = float(coef)
        if power == 0:
            parts.append(f"{value:g}")
        elif power == 1:
            parts.append(f"{value:g}*x")
        else:
            parts.append(f"{value:g}*x^{power}")
    return "+".join(parts)


def _format_factored_eq_latex(a: int | Fraction, roots: tuple[int, ...]) -> str:
    coef = _format_quad_coef_latex(a)
    body = "".join(_format_quad_factor(r) for r in roots)
    return f"{coef}{body} = 0"


def _sample_solve_by_graphing(settings: dict) -> tuple[str, str, list[int | Fraction], tuple[int, ...], str]:
    """Return (prompt_latex, answer_latex, coeffs, roots, function_expr)."""
    roots = _sample_solve_poly_roots(settings)
    leading_one = bool(settings.get("leading_coefficient_one", False)) or bool(
        settings.get("monic_only", False)
    )
    allow_stretch = bool(settings.get("allow_stretch", not leading_one))
    allow_reflection = bool(settings.get("allow_reflection", False))
    integer_only = bool(settings.get("integer_only", True))
    if leading_one:
        a: int | Fraction = 1
    else:
        a = _pick_quad_coef(
            settings,
            allow_stretch=allow_stretch or True,
            allow_reflection=allow_reflection,
            integer_only=integer_only,
            prefer_nonunit=True,
        )
        if a == 1 and allow_stretch:
            # Force a non-unit leading coefficient when presets allow stretch.
            candidates = [2, 3, -2, -3] if allow_reflection else [2, 3]
            a = random.choice(candidates)

    coeffs = _poly_from_roots(a, roots)
    allow_factored = bool(settings.get("allow_factored_form", False))
    if allow_factored and random.random() < 0.45:
        prompt = _format_factored_eq_latex(a, roots)
    else:
        prompt = f"{format_polynomial_latex(coeffs)} = 0"

    unique_roots = tuple(sorted(set(roots)))
    answer = ", ".join(f"x = {r}" for r in unique_roots)
    expr = _poly_function_expr(coeffs)
    return prompt, answer, coeffs, unique_roots, expr


class SolvePolynomialByGraphingFramework(QuestionFramework):
    """Solve polynomial equations by graphing (blank plane; answer key shows curve + roots)."""

    instruction_latex = r"\text{Solve by graphing.}"
    instruction_text = "Solve by graphing."

    def __init__(self) -> None:
        self._last_spec: CoordinatePlaneSpec | None = None

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        prompt, answer, coeffs, roots, expr = _sample_solve_by_graphing(settings)
        # Feature points: roots on the x-axis and a couple of curve samples for bounds.
        features: list[tuple[float, float]] = [(float(r), 0.0) for r in roots]
        a = float(coeffs[0])
        if len(coeffs) == 3:
            # Quadratic vertex from roots midpoint.
            h = sum(roots) / len(roots)
            b = float(coeffs[1])
            c = float(coeffs[2])
            k = a * h * h + b * h + c
            features.append((h, k))
            wing = max(2.0, max(abs(r) for r in roots) * 0.5 + 1.0)
            features.append((h + wing, a * (h + wing) ** 2 + b * (h + wing) + c))
            features.append((h - wing, a * (h - wing) ** 2 + b * (h - wing) + c))
        else:
            for x in range(min(roots) - 1, max(roots) + 2):
                y = 0.0
                for i, coef in enumerate(coeffs):
                    power = len(coeffs) - 1 - i
                    y += float(coef) * (x**power)
                features.append((float(x), y))

        x_min, x_max, y_min, y_max = origin_centered_bounds(features, settings=settings)
        self._last_spec = CoordinatePlaneSpec(
            points=[(float(r), 0.0) for r in roots],
            functions=[expr],
            show_grid=bool(settings.get("show_grid", True)),
            show_points=True,
            quadrant=settings.get("quadrant", "all"),  # type: ignore[arg-type]
            x_min=x_min,
            x_max=x_max,
            y_min=y_min,
            y_max=y_max,
        )
        return prompt, "Solve by graphing", answer

    def build_question_metadata(
        self, settings: dict, *, prompt_latex: str, prompt_text: str, answer: str | None,
    ) -> dict[str, Any]:
        if self._last_spec is None:
            return {}
        return coordinate_plane_metadata(self._last_spec, settings, prompt="blank")


def _format_radical_inner(h: int) -> str:
    if h == 0:
        return "x"
    if h > 0:
        return f"x - {h}"
    return f"x + {abs(h)}"


def _format_radical_latex(*, a: int, h: int, k: int) -> str:
    coef = "" if a == 1 else ("-" if a == -1 else str(a))
    body = f"{coef}\\sqrt{{{_format_radical_inner(h)}}}"
    if k == 0:
        return f"y = {body}"
    sign = "+" if k > 0 else "-"
    return f"y = {body} {sign} {abs(k)}"


def _radical_function_expr(a: float, h: int, k: int) -> str:
    """Emit a*sqrt(x-h)+k for the frontend sampler."""
    shift = -h
    if abs(a - 1.0) < 1e-12:
        head = "sqrt(x"
    else:
        head = f"{a:g}*sqrt(x"
    mid = f"{shift:+g}" if shift != 0 else ""
    body = f"{head}{mid})"
    if k == 0:
        return body
    return f"{body}{k:+d}"


class GraphRadicalFramework(QuestionFramework):
    instruction_latex = r"\text{Graph the following equations.}"
    instruction_text = "Graph the following equations."

    def __init__(self) -> None:
        self._last_spec: CoordinatePlaneSpec | None = None

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        allow_h = bool(settings.get("allow_shift_h", True))
        allow_k = bool(settings.get("allow_shift_k", False))
        allow_stretch = bool(settings.get("allow_stretch", False))
        allow_reflection = bool(settings.get("allow_reflection", False))

        a = 1
        if allow_stretch and allow_reflection:
            a = random.choice([-2, -1, 1, 2])
        elif allow_stretch:
            a = random.choice([1, 2])
        elif allow_reflection:
            a = random.choice([-1, 1])

        h = _nonzero_coord(settings) if allow_h and random.random() < 0.7 else 0
        k = _nonzero_intercept(settings) if allow_k and random.random() < 0.7 else 0

        eq = _format_radical_latex(a=a, h=h, k=k)
        expr = _radical_function_expr(float(a), h, k)
        # Sample a few domain points for viewport sizing.
        features = [(float(h), float(k))]
        for t in (1.0, 4.0, 9.0):
            features.append((float(h) + t, a * (t**0.5) + float(k)))
        x_min, x_max, y_min, y_max = origin_centered_bounds(features, settings=settings)
        self._last_spec = CoordinatePlaneSpec(
            points=[],
            functions=[expr],
            show_grid=bool(settings.get("show_grid", True)),
            show_points=False,
            quadrant=settings.get("quadrant", "all"),  # type: ignore[arg-type]
            x_min=x_min,
            x_max=x_max,
            y_min=y_min,
            y_max=y_max,
        )
        return eq, "Graph radical", eq

    def build_question_metadata(
        self, settings: dict, *, prompt_latex: str, prompt_text: str, answer: str | None,
    ) -> dict[str, Any]:
        if self._last_spec is None:
            return {}
        return coordinate_plane_metadata(self._last_spec, settings, prompt="blank")


def _format_log_latex(*, a: int, base: int, h: int, k: int) -> str:
    arg = _format_radical_inner(h)
    if base == 10:
        core = rf"\log\left({arg}\right)"
    elif base == 2:
        core = rf"\log_{{2}}\left({arg}\right)"
    else:
        core = rf"\log_{{{base}}}\left({arg}\right)"
    if a == 1:
        body = core
    elif a == -1:
        body = f"-{core}"
    else:
        body = f"{a}{core}"
    if k == 0:
        return f"y = {body}"
    sign = "+" if k > 0 else "-"
    return f"y = {body} {sign} {abs(k)}"


def _log_function_expr(*, a: int, base: int, h: int, k: int) -> str:
    """Emit a*log(base,x-h)+k for the frontend sampler."""
    shift = -h
    mid = f"{shift:+g}" if shift != 0 else ""
    if abs(a - 1) < 1e-12:
        head = f"log({base},x"
    else:
        head = f"{a:g}*log({base},x"
    body = f"{head}{mid})"
    if k == 0:
        return body
    return f"{body}{k:+d}"


class GraphLogarithmicFramework(QuestionFramework):
    instruction_latex = r"\text{Graph the following functions.}"
    instruction_text = "Graph the following functions."

    def __init__(self) -> None:
        self._last_spec: CoordinatePlaneSpec | None = None

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        allow_h = bool(settings.get("allow_horizontal_shift", False))
        allow_k = bool(settings.get("allow_vertical_shift", False))
        allow_stretch = bool(settings.get("allow_stretch", False))
        allow_reflection = bool(settings.get("allow_reflection", False))
        bases = [b for b in (2, 10) if b >= int(settings.get("base_min", 2))]
        base = random.choice(bases or [2, 10])

        a = 1
        if allow_stretch and allow_reflection:
            a = random.choice([-2, -1, 1, 2])
        elif allow_stretch:
            a = random.choice([1, 2])
        elif allow_reflection:
            a = random.choice([-1, 1])

        h = random.choice([-2, -1, 1, 2]) if allow_h and random.random() < 0.7 else 0
        k = random.choice([-3, -2, -1, 1, 2, 3]) if allow_k and random.random() < 0.7 else 0

        fn = _format_log_latex(a=a, base=base, h=h, k=k)
        expr = _log_function_expr(a=a, base=base, h=h, k=k)
        features = [(float(h) + 1.0, float(k))]
        for t in (base, base**2):
            features.append((float(h) + float(t), a * math.log(t, base) + float(k)))
        x_min, x_max, y_min, y_max = origin_centered_bounds(features, settings=settings)
        self._last_spec = CoordinatePlaneSpec(
            points=[],
            functions=[expr],
            show_grid=bool(settings.get("show_grid", True)),
            show_points=False,
            quadrant=settings.get("quadrant", "all"),  # type: ignore[arg-type]
            x_min=x_min,
            x_max=x_max,
            y_min=y_min,
            y_max=y_max,
        )
        return fn, "Graph logarithmic", fn

    def build_question_metadata(
        self, settings: dict, *, prompt_latex: str, prompt_text: str, answer: str | None,
    ) -> dict[str, Any]:
        if self._last_spec is None:
            return {}
        return coordinate_plane_metadata(self._last_spec, settings, prompt="blank")


def _format_rational_latex(*, a: int, h: int, k: int) -> str:
    denom = _format_radical_inner(h)
    if a == 1:
        body = f"\\frac{{1}}{{{denom}}}"
    elif a == -1:
        body = f"-\\frac{{1}}{{{denom}}}"
    else:
        body = f"\\frac{{{a}}}{{{denom}}}"
    if k == 0:
        return f"y = {body}"
    sign = "+" if k > 0 else "-"
    return f"y = {body} {sign} {abs(k)}"


def _rational_function_expr(*, a: int, h: int, k: int) -> str:
    """Emit a/(x-h)+k for the frontend sampler."""
    shift = -h
    mid = f"{shift:+g}" if shift != 0 else ""
    body = f"{a:g}/(x{mid})" if mid else f"{a:g}/x"
    if k == 0:
        return body
    return f"{body}{k:+d}"


class GraphRationalFramework(QuestionFramework):
    instruction_latex = r"\text{Graph the following functions.}"
    instruction_text = "Graph the following functions."

    def __init__(self) -> None:
        self._last_spec: CoordinatePlaneSpec | None = None

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        allow_h = bool(settings.get("allow_shift_h", True))
        allow_k = bool(settings.get("allow_shift_k", False))
        allow_stretch = bool(settings.get("allow_stretch", False))
        allow_reflection = bool(settings.get("allow_reflection", False))

        a = 1
        if allow_stretch and allow_reflection:
            a = random.choice([-3, -2, -1, 1, 2, 3])
        elif allow_stretch:
            a = random.choice([1, 2, 3])
        elif allow_reflection:
            a = random.choice([-1, 1])

        h = _nonzero_coord(settings) if allow_h and random.random() < 0.65 else 0
        k = _nonzero_intercept(settings) if allow_k and random.random() < 0.65 else 0

        fn = _format_rational_latex(a=a, h=h, k=k)
        expr = _rational_function_expr(a=a, h=h, k=k)
        features = [(float(h) + 1.0, a + float(k)), (float(h) - 1.0, -a + float(k)), (float(h), float(k))]
        x_min, x_max, y_min, y_max = origin_centered_bounds(features, settings=settings)
        self._last_spec = CoordinatePlaneSpec(
            points=[],
            functions=[expr],
            show_grid=bool(settings.get("show_grid", True)),
            show_points=False,
            quadrant=settings.get("quadrant", "all"),  # type: ignore[arg-type]
            x_min=x_min,
            x_max=x_max,
            y_min=y_min,
            y_max=y_max,
        )
        return fn, "Graph rational", fn

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
