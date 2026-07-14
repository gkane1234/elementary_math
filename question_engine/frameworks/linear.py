"""Linear functions, systems, relations, and variation frameworks."""

from __future__ import annotations

import random
from fractions import Fraction
from typing import Any, Literal

from .base import QuestionFramework
from ..core.metadata import question_metadata
from ..generators.utils import (
    format_monomial_latex,
    format_slope_intercept_latex,
    join_algebra_terms,
    random_int_range,
)

Quadrant = Literal["I", "II", "III", "IV", "all"]


def _format_signed(value: int, *, variable: str = "") -> str:
    term = format_monomial_latex(value, variable=variable or "", degree=1 if variable else 0)
    if term is None:
        return "0"
    return term


def _slope_intercept_latex(m: int, b: int) -> str:
    return format_slope_intercept_latex(m, b)


def _system_latex(eq1: str, eq2: str) -> str:
    return f"\\begin{{cases}} {eq1} \\\\ {eq2} \\end{{cases}}"


def _slope_from_points(x1: int, y1: int, x2: int, y2: int) -> Fraction:
    return Fraction(y2 - y1, x2 - x1)


def _frac_latex(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"\\frac{{{value.numerator}}}{{{value.denominator}}}"


def _bounds(
    settings: dict,
    min_key: str,
    max_key: str,
    default_min: int,
    default_max: int,
) -> tuple[int, int]:
    lo = int(settings.get(min_key, default_min))
    hi = int(settings.get(max_key, default_max))
    if lo > hi:
        lo, hi = hi, lo
    return lo, hi


def _random_in_bounds(
    settings: dict,
    min_key: str,
    max_key: str,
    default_min: int,
    default_max: int,
    *,
    exclude: set[int] | None = None,
) -> int:
    lo, hi = _bounds(settings, min_key, max_key, default_min, default_max)
    return random_int_range(lo, hi, exclude=exclude)


def _random_slope(settings: dict, *, exclude_zero: bool = True) -> int:
    exclude = {0} if exclude_zero else None
    return _random_in_bounds(settings, "slope_min", "slope_max", -6, 6, exclude=exclude)


def _random_intercept(settings: dict) -> int:
    return _random_in_bounds(settings, "intercept_min", "intercept_max", -8, 8)


def _random_coord(settings: dict) -> int:
    return _random_in_bounds(settings, "coord_min", "coord_max", -8, 8)


def _random_system_coef(settings: dict) -> int:
    """Pick a nonzero system coefficient.

    Honors ``coef_min`` / ``coef_max`` from difficulty presets when present;
    otherwise falls back to ``system_coef_*`` / ``max_coefficient_magnitude``.
    """
    exclude = {0} if bool(settings.get("exclude_zero_coefficients", True)) else None
    if "coef_min" in settings or "coef_max" in settings:
        return _random_in_bounds(
            settings, "coef_min", "coef_max", -5, 5, exclude=exclude
        )
    max_mag = int(settings.get("max_coefficient_magnitude", settings.get("system_coef_max", 5)))
    min_mag = int(settings.get("system_coef_min", 1))
    lo = min(min_mag, max_mag)
    hi = max(min_mag, max_mag)
    # Magnitude range then random sign (legacy UI knobs are often positive-only).
    mag = random_int_range(max(1, lo), max(1, hi), exclude=None)
    return mag * random.choice([-1, 1])


def _system_solution(settings: dict) -> tuple[int, int]:
    if bool(settings.get("prefer_integer_solutions", True)):
        return _random_point(settings)
    x = random.uniform(-6, 6)
    y = random.uniform(-6, 6)
    return round(x), round(y)


def _random_variation_constant(settings: dict) -> int:
    return _random_in_bounds(settings, "variation_constant_min", "variation_constant_max", 2, 12)


def _quadrant_range(
    quadrant: Quadrant,
    coord_min: int,
    coord_max: int,
    *,
    axis: Literal["x", "y"],
) -> tuple[int, int]:
    if quadrant == "all":
        return coord_min, coord_max
    positive_lo = max(1, coord_min if coord_min > 0 else 1)
    positive_hi = max(positive_lo, coord_max if coord_max > 0 else 1)
    negative_lo = min(-1, coord_min if coord_min < 0 else -1)
    negative_hi = min(-1, coord_max if coord_max < 0 else -1)
    if axis == "x":
        if quadrant == "I":
            return positive_lo, positive_hi
        if quadrant == "II":
            return negative_lo, negative_hi
        if quadrant == "III":
            return negative_lo, negative_hi
        return positive_lo, positive_hi
    if quadrant == "I":
        return positive_lo, positive_hi
    if quadrant == "II":
        return positive_lo, positive_hi
    if quadrant == "III":
        return negative_lo, negative_hi
    return negative_lo, negative_hi


def _random_point(settings: dict) -> tuple[int, int]:
    quadrant: Quadrant = settings.get("quadrant", "all")  # type: ignore[assignment]
    coord_min, coord_max = _bounds(settings, "coord_min", "coord_max", -8, 8)
    x_lo, x_hi = _quadrant_range(quadrant, coord_min, coord_max, axis="x")
    y_lo, y_hi = _quadrant_range(quadrant, coord_min, coord_max, axis="y")
    if x_lo > x_hi:
        x_lo, x_hi = x_hi, x_lo
    if y_lo > y_hi:
        y_lo, y_hi = y_hi, y_lo
    return random.randint(x_lo, x_hi), random.randint(y_lo, y_hi)


def _weighted_choice(settings: dict, positive_key: str, negative_key: str) -> bool:
    positive = max(0, int(settings.get(positive_key, 50)))
    negative = max(0, int(settings.get(negative_key, 50)))
    total = positive + negative
    if total == 0:
        return random.choice([True, False])
    return random.randint(1, total) <= positive


def _plane_spec(
    settings: dict,
    *,
    points: list[tuple[float, float]] | None = None,
    slope: float | None = None,
    y_intercept: float | None = None,
    functions: list[str] | None = None,
) -> "CoordinatePlaneSpec":
    from .graphing import CoordinatePlaneSpec

    return CoordinatePlaneSpec(
        points=[(float(x), float(y)) for x, y in (points or [])],
        functions=list(functions or []),
        slope=float(slope) if slope is not None else None,
        y_intercept=float(y_intercept) if y_intercept is not None else None,
        show_grid=bool(settings.get("show_grid", True)),
        show_points=bool(settings.get("show_points", True)),
        quadrant=settings.get("quadrant", "all"),  # type: ignore[arg-type]
    )


_WRITING_ASK_MODES = (
    "slope_point",
    "two_points",
    "slope_intercept_info",
    "to_point_slope",
    "to_slope_intercept",
    "simplify_messy",
    "from_graph",
)

_WRITING_ALLOW_KEYS: dict[str, str] = {
    "slope_point": "allow_slope_point",
    "two_points": "allow_two_points",
    "slope_intercept_info": "allow_slope_intercept_info",
    "to_point_slope": "allow_to_point_slope",
    "to_slope_intercept": "allow_to_slope_intercept",
    "simplify_messy": "allow_simplify_messy",
    "from_graph": "allow_from_graph",
}


def _resolve_writing_ask_mode(settings: dict) -> str:
    """Pick a writing-linear mode from ask_mode / allow_* toggles."""
    raw = str(settings.get("ask_mode", "mixed")).strip().lower()
    if raw in _WRITING_ASK_MODES:
        allow_key = _WRITING_ALLOW_KEYS[raw]
        if bool(settings.get(allow_key, True)):
            return raw
    enabled = [
        mode
        for mode, key in _WRITING_ALLOW_KEYS.items()
        if bool(settings.get(key, True))
    ]
    if not enabled:
        enabled = list(_WRITING_ASK_MODES)
    return random.choice(enabled)


def _random_standard_coeffs(settings: dict, *, m: int, b: int) -> tuple[int, int, int]:
    """Pick Ax + By = C equivalent to y = mx + b with integer A, B, C."""
    # B y = -A x + C  with y = mx + b ⇒ A = -k m, B = k, C = k b for k ≠ 0
    k = random_int_range(1, 4, exclude=set()) * random.choice([-1, 1])
    a = -k * m
    bb = k
    c = k * b
    # Prefer positive leading x coeff when easy to flip.
    if a < 0 and random.random() < 0.55:
        a, bb, c = -a, -bb, -c
    return a, bb, c


def _messy_linear_prompt(settings: dict) -> tuple[str, int, int]:
    """Build an unsimplified linear relation; return (latex, m, b) for y = mx + b."""
    m = _random_slope(settings)
    b = _random_intercept(settings)
    variant = random.choice(["distribute_rhs", "combine_like", "clear_constant", "mixed_paren"])
    if variant == "distribute_rhs":
        # y = a(x + p) + q  → m = a, b = a*p + q
        a = m
        p = random_int_range(-4, 4, exclude={0})
        q = b - a * p
        inner = f"x + {p}" if p > 0 else (f"x - {abs(p)}" if p < 0 else "x")
        q_term = f" + {q}" if q > 0 else (f" - {abs(q)}" if q < 0 else "")
        expr = f"y = {a}({inner}){q_term}" if a not in (1, -1) else (
            f"y = ({inner}){q_term}" if a == 1 else f"y = -({inner}){q_term}"
        )
        return f"\\text{{Simplify to slope-intercept form: }} {expr}", m, b
    if variant == "combine_like":
        # y = (m-r)x + s + r x + (b-s)
        r = random_int_range(-4, 4, exclude={0, m})
        s = random_int_range(-5, 5, exclude={0})
        t = b - s
        m1 = m - r
        terms = join_algebra_terms(
            [
                format_monomial_latex(m1, variable="x"),
                format_monomial_latex(s, variable="", degree=0),
                format_monomial_latex(r, variable="x"),
                format_monomial_latex(t, variable="", degree=0),
            ]
        )
        return f"\\text{{Simplify to slope-intercept form: }} y = {terms}", m, b
    if variant == "clear_constant":
        # ky - k b = k m x  →  rearrange / divide
        k = random_int_range(2, 5, exclude=set())
        left = join_algebra_terms(
            [
                format_monomial_latex(k, variable="y"),
                format_monomial_latex(-k * b, variable="", degree=0),
            ]
        )
        right = format_monomial_latex(k * m, variable="x") or "0"
        return (
            f"\\text{{Write in slope-intercept form: }} {left} = {right}",
            m,
            b,
        )
    # mixed_paren: y - y1 = m(x - x1) + c - c  (point-slope plus canceling junk)
    x1, y1 = _random_point(settings)
    # Keep same line: m, b with b = y1 - m*x1 — already have m,b; snap point onto line
    y1 = m * x1 + b
    junk = random_int_range(1, 4, exclude=set())
    ps = _point_slope_latex(m, x1, y1)
    # Insert +junk - junk on the right when point-slope has a product form
    messy = f"{ps} + {junk} - {junk}"
    return f"\\text{{Simplify to slope-intercept form: }} {messy}", m, b


class WritingLinearEquationsFramework(QuestionFramework):
    """Write linear equations: given info, form conversions, simplify, or from a graph."""

    instruction_latex = r"\text{Write an equation of the line.}"
    instruction_text = "Write an equation of the line."

    def __init__(self) -> None:
        self._last_plane_spec: CoordinatePlaneSpec | None = None
        self._last_ask_mode: str | None = None
        self._last_target_form: str = "slope_intercept"

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        self._last_plane_spec = None
        mode = _resolve_writing_ask_mode(settings)
        self._last_ask_mode = mode
        if mode == "slope_point":
            return self._prompt_slope_point(settings)
        if mode == "two_points":
            return self._prompt_two_points(settings)
        if mode == "slope_intercept_info":
            return self._prompt_slope_intercept_info(settings)
        if mode == "to_point_slope":
            return self._prompt_to_point_slope(settings)
        if mode == "to_slope_intercept":
            return self._prompt_to_slope_intercept(settings)
        if mode == "simplify_messy":
            return self._prompt_simplify_messy(settings)
        return self._prompt_from_graph(settings)

    def _prompt_slope_point(self, settings: dict) -> tuple[str, str, str | None]:
        m = _random_slope(settings)
        x1, y1 = _random_point(settings)
        b = y1 - m * x1
        target = random.choice(["slope_intercept", "point_slope"])
        self._last_target_form = target
        if target == "point_slope":
            prompt = (
                f"\\text{{Write the equation of the line with slope }} {m} "
                f"\\text{{ that passes through }} ({x1}, {y1}) "
                f"\\text{{ in point-slope form.}}"
            )
            return prompt, "Write point-slope equation", _point_slope_latex(m, x1, y1)
        prompt = (
            f"\\text{{Write the equation of the line with slope }} {m} "
            f"\\text{{ that passes through }} ({x1}, {y1}) "
            f"\\text{{ in slope-intercept form.}}"
        )
        return prompt, "Write slope-intercept equation", _slope_intercept_latex(m, b)

    def _prompt_two_points(self, settings: dict) -> tuple[str, str, str | None]:
        m = _random_slope(settings)
        b = _random_intercept(settings)
        x1, y1 = _random_point(settings)
        y1 = m * x1 + b
        _, coord_max = _bounds(settings, "coord_min", "coord_max", -8, 8)
        dx = random_int_range(1, max(1, abs(coord_max)), exclude=set())
        x2 = x1 + dx * random.choice([-1, 1])
        y2 = m * x2 + b
        self._last_target_form = "slope_intercept"
        prompt = (
            f"\\text{{Write the equation of the line through }} "
            f"({x1}, {y1}) \\text{{ and }} ({x2}, {y2}) "
            f"\\text{{ in slope-intercept form.}}"
        )
        return prompt, "Write equation from two points", _slope_intercept_latex(m, b)

    def _prompt_slope_intercept_info(self, settings: dict) -> tuple[str, str, str | None]:
        m = _random_slope(settings)
        b = _random_intercept(settings)
        self._last_target_form = "slope_intercept"
        prompt = (
            f"\\text{{Write the equation of the line with slope }} {m} "
            f"\\text{{ and }} y\\text{{-intercept }} {b} "
            f"\\text{{ in slope-intercept form.}}"
        )
        return prompt, "Write from slope and intercept", _slope_intercept_latex(m, b)

    def _prompt_to_point_slope(self, settings: dict) -> tuple[str, str, str | None]:
        m = _random_slope(settings)
        b = _random_intercept(settings)
        x1, y1 = _random_point(settings)
        y1 = m * x1 + b
        self._last_target_form = "point_slope"
        source = random.choice(["slope_intercept", "standard", "two_points"])
        if source == "slope_intercept":
            given = _slope_intercept_latex(m, b)
            prompt = (
                f"\\text{{Write }} {given} \\text{{ in point-slope form "
                f"using the point }} ({x1}, {y1})."
            )
        elif source == "standard":
            a, bb, c = _random_standard_coeffs(settings, m=m, b=b)
            given = _standard_form_latex(a, bb, c)
            prompt = (
                f"\\text{{Write }} {given} \\text{{ in point-slope form "
                f"using the point }} ({x1}, {y1})."
            )
        else:
            dx = random_int_range(1, 5, exclude=set()) * random.choice([-1, 1])
            x2, y2 = x1 + dx, y1 + m * dx
            prompt = (
                f"\\text{{Write the equation of the line through }} "
                f"({x1}, {y1}) \\text{{ and }} ({x2}, {y2}) "
                f"\\text{{ in point-slope form.}}"
            )
        return prompt, "Convert to point-slope", _point_slope_latex(m, x1, y1)

    def _prompt_to_slope_intercept(self, settings: dict) -> tuple[str, str, str | None]:
        m = _random_slope(settings)
        b = _random_intercept(settings)
        self._last_target_form = "slope_intercept"
        source = random.choice(["point_slope", "standard"])
        if source == "point_slope":
            x1, y1 = _random_point(settings)
            y1 = m * x1 + b
            given = _point_slope_latex(m, x1, y1)
            prompt = (
                f"\\text{{Write }} {given} \\text{{ in slope-intercept form.}}"
            )
        else:
            a, bb, c = _random_standard_coeffs(settings, m=m, b=b)
            given = _standard_form_latex(a, bb, c)
            prompt = (
                f"\\text{{Write }} {given} \\text{{ in slope-intercept form.}}"
            )
        return prompt, "Convert to slope-intercept", _slope_intercept_latex(m, b)

    def _prompt_simplify_messy(self, settings: dict) -> tuple[str, str, str | None]:
        prompt, m, b = _messy_linear_prompt(settings)
        self._last_target_form = "slope_intercept"
        return prompt, "Simplify to linear equation", _slope_intercept_latex(m, b)

    def _prompt_from_graph(self, settings: dict) -> tuple[str, str, str | None]:
        m = _random_slope(settings)
        b = _random_intercept(settings)
        self._last_target_form = "slope_intercept"
        prompt = (
            "\\text{The line is shown on the coordinate plane. "
            "Write its equation in slope-intercept form.}"
        )
        # Line only — no highlighted points (would reveal rise/run / intercept).
        self._last_plane_spec = _line_stimulus_spec(
            settings, slope=float(m), y_intercept=float(b)
        )
        return prompt, "Read equation from graph", _slope_intercept_latex(m, b)

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return {}

    def build_question_metadata(
        self,
        settings: dict,
        *,
        prompt_latex: str,
        prompt_text: str,
        answer: str | None,
    ) -> dict[str, Any]:
        meta = question_metadata(linear_form=self._last_target_form)
        if self._last_plane_spec is None:
            return meta
        from .graphing import coordinate_plane_metadata

        self._last_plane_spec.points = []
        self._last_plane_spec.show_points = False
        forced = {**settings, "show_points": False, "include_graph_metadata": True}
        plane = coordinate_plane_metadata(self._last_plane_spec, forced, prompt="stimulus")
        return {**meta, **plane}


_SLOPE_ASK_MODES = (
    "from_points",
    "from_equation",
    "from_graph",
    "find_equation",
    "classify",
    "parallel_perpendicular",
)

_SLOPE_ALLOW_KEYS: dict[str, str] = {
    "from_points": "allow_from_points",
    "from_equation": "allow_from_equation",
    "from_graph": "allow_from_graph",
    "find_equation": "allow_find_equation",
    "classify": "allow_classify",
    "parallel_perpendicular": "allow_parallel_perpendicular",
}

_SLOPE_EQUATION_FORMS = ("slope_intercept", "point_slope", "standard")


def _slope_bool(settings: dict, key: str, default: bool = True) -> bool:
    return bool(settings.get(key, default))


def _slope_difficulty_tier(settings: dict) -> str:
    tier = str(
        settings.get("difficulty_tier") or settings.get("difficulty") or "medium"
    ).strip().lower()
    return tier if tier in {"easy", "medium", "hard"} else "medium"


def _resolve_slope_ask_mode(settings: dict, *, multi_mode: bool) -> str:
    """Pick an ask mode from settings toggles (multi-mode) or mixed find-slope forms."""
    if not multi_mode:
        if bool(settings.get("from_equation", False)):
            return "from_equation"
        raw = str(settings.get("ask_mode", "mixed")).strip().lower()
        if raw == "from_points":
            return "from_points"
        if raw == "from_equation":
            return "from_equation"
        # Basic slope: mix two-points and equation prompts (no graph mode).
        return random.choice(["from_points", "from_equation"])

    raw = str(settings.get("ask_mode", "mixed")).strip().lower()
    if raw in _SLOPE_ASK_MODES:
        allow_key = _SLOPE_ALLOW_KEYS[raw]
        default_on = raw != "parallel_perpendicular"
        if _slope_bool(settings, allow_key, default_on):
            return raw

    enabled = [
        mode
        for mode, key in _SLOPE_ALLOW_KEYS.items()
        if _slope_bool(settings, key, default=(mode != "parallel_perpendicular"))
    ]
    if not enabled:
        enabled = ["from_points", "from_equation", "from_graph"]
    return random.choice(enabled)


def _pick_slope_equation_form(settings: dict) -> str:
    """Choose equation presentation by difficulty / toggles.

    easy → slope-intercept; medium/hard → also point-slope and standard form.
    """
    explicit = str(settings.get("equation_form", "mixed")).strip().lower()
    if explicit in _SLOPE_EQUATION_FORMS:
        return explicit

    tier = _slope_difficulty_tier(settings)
    forms: list[str] = []
    if _slope_bool(settings, "allow_slope_intercept_form", True):
        forms.append("slope_intercept")
    if tier in {"medium", "hard"}:
        if _slope_bool(settings, "allow_point_slope_form", True):
            forms.append("point_slope")
        if _slope_bool(settings, "allow_standard_form", True):
            forms.append("standard")
    if not forms:
        forms = ["slope_intercept"]
    return random.choice(forms)


def _format_slope_answer(slope: Fraction) -> str:
    if slope.denominator == 1:
        return str(slope.numerator)
    # Prefer -\frac{a}{b} over \frac{-a}{b}
    sign = "-" if slope < 0 else ""
    return f"{sign}\\frac{{{abs(slope.numerator)}}}{{{slope.denominator}}}"


def _point_slope_latex(m: int, x1: int, y1: int) -> str:
    """Format ``y - y1 = m(x - x1)`` with clean signs."""
    if y1 == 0:
        left = "y"
    elif y1 > 0:
        left = f"y - {y1}"
    else:
        left = f"y + {abs(y1)}"

    if x1 == 0:
        x_part = "x"
        wrapped = False
    elif x1 > 0:
        x_part = f"(x - {x1})"
        wrapped = True
    else:
        x_part = f"(x + {abs(x1)})"
        wrapped = True

    if m == 0:
        right = "0"
    elif m == 1:
        # Keep explicit 1(x − x1) so students recognize point-slope form.
        right = f"1{x_part}" if wrapped else x_part
    elif m == -1:
        right = f"-1{x_part}" if wrapped else f"-{x_part}"
    else:
        right = f"{m}{x_part}" if wrapped else f"{m}({x_part})"
    return f"{left} = {right}"


def _standard_form_latex(a: int, b: int, c: int) -> str:
    """Format ``Ax + By = C``."""
    lhs = join_algebra_terms(
        [
            format_monomial_latex(a, variable="x"),
            format_monomial_latex(b, variable="y"),
        ]
    )
    return f"{lhs} = {c}"


def _line_stimulus_spec(
    settings: dict,
    *,
    slope: float,
    y_intercept: float,
) -> "CoordinatePlaneSpec":
    """Stimulus line on the plane — never mark coordinate points (gives away slope)."""
    from .graphing import _linear_function_expr

    spec = _plane_spec(
        settings,
        points=[],
        slope=slope,
        y_intercept=y_intercept,
        functions=[_linear_function_expr(slope, y_intercept)],
    )
    spec.show_points = False
    return spec


class SlopeFramework(QuestionFramework):
    """Slope questions: two points, equation, graph, classify, write equation, parallel/perp."""

    instruction_latex = r"\text{Find the slope.}"
    instruction_text = "Find the slope."

    def __init__(self, *, from_equation: bool = False, multi_mode: bool = False) -> None:
        self.from_equation = from_equation
        self.multi_mode = multi_mode or from_equation
        self._last_plane_spec: CoordinatePlaneSpec | None = None
        self._last_graph_role: Literal["blank", "stimulus"] | None = None
        self._last_ask_mode: str | None = None
        self._last_equation_form: str | None = None

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        self._last_plane_spec = None
        self._last_graph_role = None
        self._last_equation_form = None
        mode = _resolve_slope_ask_mode(settings, multi_mode=self.multi_mode)
        if self.from_equation and not self.multi_mode:
            mode = "from_equation"
        self._last_ask_mode = mode

        if mode == "from_equation":
            return self._prompt_from_equation(settings)
        if mode == "from_graph":
            return self._prompt_from_graph(settings)
        if mode == "find_equation":
            return self._prompt_find_equation(settings)
        if mode == "classify":
            return self._prompt_classify(settings)
        if mode == "parallel_perpendicular":
            return self._prompt_parallel_perpendicular(settings)
        return self._prompt_from_points(settings)

    def _prompt_from_points(self, settings: dict) -> tuple[str, str, str | None]:
        x1, y1 = _random_point(settings)
        dx = random_int_range(-5, 5, exclude={0})
        dy = random_int_range(-5, 5, exclude={0})
        x2, y2 = x1 + dx, y1 + dy
        slope = _slope_from_points(x1, y1, x2, y2)
        prompt = (
            f"\\text{{Find the slope of the line through }} "
            f"({x1}, {y1}) \\text{{ and }} ({x2}, {y2})."
        )
        answer = _format_slope_answer(slope)
        # Blank student graph only when explicitly requested (default off).
        if bool(settings.get("graph_for_two_points", False)):
            m = float(slope)
            b = float(y1) - m * float(x1)
            from .graphing import _linear_function_expr

            self._last_plane_spec = _plane_spec(
                settings,
                points=[(x1, y1), (x2, y2)],
                slope=m,
                y_intercept=b,
                functions=[_linear_function_expr(m, b)],
            )
            self._last_graph_role = "blank"
        return prompt, "Slope from points", answer

    def _prompt_from_equation(self, settings: dict) -> tuple[str, str, str | None]:
        # Equation prompts never attach a coordinate-plane figure.
        form = _pick_slope_equation_form(settings)
        self._last_equation_form = form
        m = _random_slope(settings, exclude_zero=(form == "standard"))
        if form == "point_slope":
            x1, y1 = _random_point(settings)
            eq = _point_slope_latex(m, x1, y1)
            prompt = f"\\text{{Find the slope of the line }} {eq}."
            return prompt, "Slope from point-slope", _format_slope_answer(Fraction(m))
        if form == "standard":
            b_int = _random_intercept(settings)
            tier = _slope_difficulty_tier(settings)
            if tier == "hard":
                scale = random.randint(2, 5)
            elif tier == "medium":
                scale = random.choice([1, 1, 2, 3])
            else:
                scale = 1
            a = m * scale
            b_coef = -scale
            c = -b_int * scale
            if a < 0 or (a == 0 and b_coef < 0):
                a, b_coef, c = -a, -b_coef, -c
            eq = _standard_form_latex(a, b_coef, c)
            prompt = f"\\text{{Find the slope of the line }} {eq}."
            return prompt, "Slope from standard form", _format_slope_answer(Fraction(m))
        b = _random_intercept(settings)
        eq = _slope_intercept_latex(m, b)
        prompt = f"\\text{{Find the slope of the line }} {eq}."
        return prompt, "Slope from slope-intercept", _format_slope_answer(Fraction(m))

    def _prompt_from_graph(self, settings: dict) -> tuple[str, str, str | None]:
        m = _random_slope(settings, exclude_zero=False)
        b = _random_intercept(settings)
        prompt = (
            "\\text{The line is shown on the coordinate plane. Find the slope.}"
        )
        self._last_plane_spec = _line_stimulus_spec(settings, slope=float(m), y_intercept=float(b))
        self._last_graph_role = "stimulus"
        return prompt, "Slope from graph", str(m)

    def _prompt_find_equation(self, settings: dict) -> tuple[str, str, str | None]:
        variant = random.choice(["slope_point_eq", "slope_point_intercept", "two_points_eq"])
        m = _random_slope(settings, exclude_zero=False)
        if variant == "slope_point_eq":
            x1, y1 = _random_point(settings)
            b = y1 - m * x1
            prompt = (
                f"\\text{{Write the equation of the line with slope }} {m} "
                f"\\text{{ that passes through }} ({x1}, {y1})."
            )
            return prompt, "Equation from slope and point", _slope_intercept_latex(m, b)
        if variant == "slope_point_intercept":
            x1, y1 = _random_point(settings)
            b = y1 - m * x1
            prompt = (
                f"\\text{{A line has slope }} {m} \\text{{ and passes through }} "
                f"({x1}, {y1}). \\text{{ Find the }} y\\text{{-intercept.}}"
            )
            return prompt, "Y-intercept from slope and point", str(b)
        x1, y1 = _random_point(settings)
        dx = random_int_range(1, 5, exclude=set())
        x2 = x1 + dx * random.choice([-1, 1])
        y2 = y1 + m * (x2 - x1)
        b = y1 - m * x1
        prompt = (
            f"\\text{{Write the equation of the line through }} "
            f"({x1}, {y1}) \\text{{ and }} ({x2}, {y2})."
        )
        return prompt, "Equation from two points", _slope_intercept_latex(m, b)

    def _prompt_classify(self, settings: dict) -> tuple[str, str, str | None]:
        use_graph = bool(settings.get("include_graph_metadata", True)) and random.random() < 0.55
        kind = random.choice(["positive", "negative", "zero", "undefined"])
        if use_graph and kind != "undefined":
            if kind == "zero":
                m, b = 0, _random_intercept(settings)
            elif kind == "positive":
                m = abs(_random_slope(settings)) or 1
                b = _random_intercept(settings)
            else:
                m = -abs(_random_slope(settings)) or -1
                b = _random_intercept(settings)
            prompt = (
                "\\text{The line is shown on the coordinate plane. "
                "Is its slope positive, negative, zero, or undefined?}"
            )
            self._last_plane_spec = _line_stimulus_spec(
                settings, slope=float(m), y_intercept=float(b)
            )
            self._last_graph_role = "stimulus"
            return prompt, "Classify slope from graph", kind

        descriptions = {
            "positive": (
                r"\text{A line that rises from left to right has a }"
                r"\underline{\hspace{2cm}}\text{ slope.}"
            ),
            "negative": (
                r"\text{A line that falls from left to right has a }"
                r"\underline{\hspace{2cm}}\text{ slope.}"
            ),
            "zero": (
                r"\text{A horizontal line has a }"
                r"\underline{\hspace{2cm}}\text{ slope.}"
            ),
            "undefined": (
                r"\text{A vertical line has an }"
                r"\underline{\hspace{2cm}}\text{ slope.}"
            ),
        }
        return descriptions[kind], "Classify slope from description", kind

    def _prompt_parallel_perpendicular(self, settings: dict) -> tuple[str, str, str | None]:
        variant = random.choice(["parallel_slope", "perpendicular_slope", "relationship"])
        m = _random_slope(settings)
        if variant == "parallel_slope":
            prompt = (
                f"\\text{{A line has slope }} {m}. "
                f"\\text{{ What is the slope of a line parallel to it?}}"
            )
            return prompt, "Parallel slope", str(m)
        if variant == "perpendicular_slope":
            # Perpendicular slope is -1/m for nonzero m.
            perp = Fraction(-1, m)
            prompt = (
                f"\\text{{A line has slope }} {m}. "
                f"\\text{{ What is the slope of a line perpendicular to it?}}"
            )
            return prompt, "Perpendicular slope", _format_slope_answer(perp)
        m2 = m if random.choice([True, False]) else (
            Fraction(-1, m) if random.choice([True, False]) else _random_slope(settings)
        )
        if isinstance(m2, Fraction):
            m2_disp = _format_slope_answer(m2)
            m2_val = float(m2)
        else:
            m2_disp = str(m2)
            m2_val = float(m2)
        if abs(m2_val - float(m)) < 1e-9:
            answer = "parallel"
        elif abs(m2_val * float(m) + 1) < 1e-9:
            answer = "perpendicular"
        else:
            answer = "neither"
        prompt = (
            f"\\text{{Two lines have slopes }} {m} \\text{{ and }} {m2_disp}. "
            f"\\text{{ Are the lines parallel, perpendicular, or neither?}}"
        )
        return prompt, "Slope relationship", answer

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return {}

    def build_question_metadata(
        self,
        settings: dict,
        *,
        prompt_latex: str,
        prompt_text: str,
        answer: str | None,
    ) -> dict[str, Any]:
        meta_kwargs: dict[str, Any] = {
            "slope_source": self._last_ask_mode or "two_points",
        }
        if self._last_equation_form:
            meta_kwargs["equation_form"] = self._last_equation_form
        meta = question_metadata(**meta_kwargs)
        if self._last_plane_spec is None:
            return meta
        from .graphing import coordinate_plane_metadata

        role = self._last_graph_role or "stimulus"
        # Force no point markers on slope stimulus graphs (settings may default show_points=True).
        if role == "stimulus":
            self._last_plane_spec.points = []
            self._last_plane_spec.show_points = False
            forced = {**settings, "show_points": False}
            plane = coordinate_plane_metadata(self._last_plane_spec, forced, prompt="stimulus")
        else:
            plane = coordinate_plane_metadata(self._last_plane_spec, settings, prompt=role)
        return {**meta, **plane}

class PlottingPointsFramework(QuestionFramework):
    """Identify or plot a point on the coordinate plane."""

    instruction_latex = r"\text{Plot the following points on the coordinate plane.}"
    instruction_text = "Plot the following points on the coordinate plane."

    def __init__(self) -> None:
        self._last_point: tuple[float, float] | None = None

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        x, y = _system_solution(settings)
        self._last_point = (float(x), float(y))
        prompt = f"({x}, {y})"
        answer = f"({x}, {y})"
        return prompt, f"({x}, {y})", answer

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return {}

    def build_question_metadata(
        self,
        settings: dict,
        *,
        prompt_latex: str,
        prompt_text: str,
        answer: str | None,
    ) -> dict[str, Any]:
        if self._last_point is None:
            return {}
        from .graphing import graph_spec_from_points

        return graph_spec_from_points([self._last_point], settings, prompt="blank")


class SystemsEliminationFramework(QuestionFramework):
    """Solve 2×2 linear systems suited for elimination."""

    instruction_latex = r"\text{Solve the system.}"
    instruction_text = "Solve the system."

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        x, y = _system_solution(settings)
        a1 = _random_system_coef(settings)
        b1 = _random_system_coef(settings)
        a2 = _random_system_coef(settings)
        b2 = _random_system_coef(settings)
        while abs(a1 * b2 - a2 * b1) < 2:
            a2 = _random_system_coef(settings)
            b2 = _random_system_coef(settings)
        c1 = a1 * x + b1 * y
        c2 = a2 * x + b2 * y
        eq1 = f"{join_algebra_terms([format_monomial_latex(a1, variable='x'), format_monomial_latex(b1, variable='y')])} = {c1}"
        eq2 = f"{join_algebra_terms([format_monomial_latex(a2, variable='x'), format_monomial_latex(b2, variable='y')])} = {c2}"
        prompt = _system_latex(eq1, eq2)
        answer = f"(x, y) = ({x}, {y})"
        return prompt, "system (elimination)", answer

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return question_metadata(method="elimination")


class SystemsSubstitutionFramework(QuestionFramework):
    """Solve 2×2 linear systems with one equation solved for a variable."""

    instruction_latex = r"\text{Solve the system.}"
    instruction_text = "Solve the system."

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        x, y = _system_solution(settings)
        m = _random_slope(settings)
        b = y - m * x
        a2 = _random_system_coef(settings)
        b2 = _random_system_coef(settings)
        c2 = a2 * x + b2 * y
        eq1 = _slope_intercept_latex(m, b)
        eq2 = f"{join_algebra_terms([format_monomial_latex(a2, variable='x'), format_monomial_latex(b2, variable='y')])} = {c2}"
        prompt = _system_latex(eq1, eq2)
        answer = f"(x, y) = ({x}, {y})"
        return prompt, "system (substitution)", answer

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return question_metadata(method="substitution")


class DirectVariationFramework(QuestionFramework):
    """Direct and inverse variation equations and applications."""

    instruction_latex = r"\text{Write the variation equation.}"
    instruction_text = "Write the variation equation."

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        is_direct = _weighted_choice(
            settings,
            "direct_variation_weight",
            "inverse_variation_weight",
        )
        k = _random_variation_constant(settings)
        _, coord_max = _bounds(settings, "coord_min", "coord_max", -8, 8)
        x = random.randint(1, max(1, coord_max))
        if is_direct:
            y = k * x
            if random.choice([True, False]):
                prompt = f"\\text{{Write a direct variation equation with }} k = {k}."
                answer = _slope_intercept_latex(k, 0)
            else:
                prompt = (
                    f"\\text{{If }} y \\text{{ varies directly with }} x "
                    f"\\text{{ and }} y = {y} \\text{{ when }} x = {x}, "
                    f"\\text{{ write the equation.}}"
                )
                answer = _slope_intercept_latex(k, 0)
        else:
            y = Fraction(k, x)
            if random.choice([True, False]):
                prompt = f"\\text{{Write an inverse variation equation with }} k = {k}."
                answer = f"y = \\frac{{{k}}}{{x}}"
            else:
                prompt = (
                    f"\\text{{If }} y \\text{{ varies inversely with }} x "
                    f"\\text{{ and }} y = {_frac_latex(y)} \\text{{ when }} x = {x}, "
                    f"\\text{{ write the equation.}}"
                )
                answer = f"y = \\frac{{{k}}}{{x}}"
        return prompt, "Variation equation", answer

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return question_metadata(variation="direct_or_inverse")


class DiscreteRelationsFramework(QuestionFramework):
    """Evaluate or complete a discrete linear relation given as a table."""

    instruction_latex = r"\text{Evaluate the relation.}"
    instruction_text = "Evaluate the relation."

    def __init__(self) -> None:
        self._last_plane_spec: CoordinatePlaneSpec | None = None

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        m = _random_slope(settings)
        b = _random_intercept(settings)
        row_count = int(settings.get("table_row_count", settings.get("min_terms", 3)))
        row_count = max(3, min(8, row_count))
        coord_min, coord_max = _bounds(settings, "coord_min", "coord_max", -8, 8)
        pool = list(range(coord_min, coord_max + 1))
        xs = sorted(random.sample(pool, k=min(row_count, len(pool))))
        rows = [(x, m * x + b) for x in xs]
        missing_x = random.choice(xs)
        missing_y = m * missing_x + b
        table_rows = []
        for x, y in rows:
            if x == missing_x:
                table_rows.append(f"{x} & ? \\\\")
            else:
                table_rows.append(f"{x} & {y} \\\\")
        table = "\\begin{array}{|c|c|} \\hline x & y \\\\ \\hline " + " ".join(table_rows) + " \\hline \\end{array}"
        prompt = f"\\text{{Complete the table for }} {_slope_intercept_latex(m, b)}. \\\\ {table}"
        answer = str(missing_y)
        self._last_plane_spec = _plane_spec(settings, points=rows, slope=m, y_intercept=b)
        return prompt, f"y when x={missing_x}", answer

    def build_question_metadata(
        self,
        settings: dict,
        *,
        prompt_latex: str,
        prompt_text: str,
        answer: str | None,
    ) -> dict[str, Any]:
        if self._last_plane_spec is None:
            return {}
        from .graphing import coordinate_plane_metadata

        return coordinate_plane_metadata(self._last_plane_spec, settings)


class ContinuousRelationsFramework(QuestionFramework):
    """Evaluate a continuous linear relation at a given input."""

    instruction_latex = r"\text{Evaluate the relation.}"
    instruction_text = "Evaluate the relation."

    def __init__(self) -> None:
        self._last_plane_spec: CoordinatePlaneSpec | None = None

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        m = _random_slope(settings)
        b = _random_intercept(settings)
        x = _random_coord(settings)
        y = m * x + b
        eq = _slope_intercept_latex(m, b)
        prompt = f"\\text{{Given }} {eq}, \\text{{ find }} y \\text{{ when }} x = {x}."
        answer = str(y)
        self._last_plane_spec = _plane_spec(settings, points=[(x, y)], slope=m, y_intercept=b)
        return prompt, f"y when x={x}", answer

    def build_question_metadata(
        self,
        settings: dict,
        *,
        prompt_latex: str,
        prompt_text: str,
        answer: str | None,
    ) -> dict[str, Any]:
        if self._last_plane_spec is None:
            return {}
        from .graphing import coordinate_plane_metadata

        return coordinate_plane_metadata(self._last_plane_spec, settings)


class EvaluatingGraphingFunctionsFramework(QuestionFramework):
    """Evaluate a linear function at a given value."""

    instruction_latex = r"\text{Evaluate.}"
    instruction_text = "Evaluate."

    def __init__(self) -> None:
        self._last_plane_spec: CoordinatePlaneSpec | None = None

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        m = _random_slope(settings)
        b = _random_intercept(settings)
        x = _random_coord(settings)
        value = m * x + b
        fn = _slope_intercept_latex(m, b).replace("y =", "f(x) =")
        prompt = f"\\text{{Given }} {fn}, \\text{{ find }} f({x})."
        answer = str(value)
        self._last_plane_spec = _plane_spec(settings, points=[(x, value)], slope=m, y_intercept=b)
        return prompt, f"f({x})", answer

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return question_metadata(function_family="linear")

    def build_question_metadata(
        self,
        settings: dict,
        *,
        prompt_latex: str,
        prompt_text: str,
        answer: str | None,
    ) -> dict[str, Any]:
        if self._last_plane_spec is None:
            return {}
        from .graphing import coordinate_plane_metadata

        return coordinate_plane_metadata(self._last_plane_spec, settings)
