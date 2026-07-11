"""Linear functions, systems, relations, and variation frameworks."""

from __future__ import annotations

import random
from fractions import Fraction
from typing import Any, Literal

from .base import QuestionFramework
from ..core.metadata import question_metadata
from ..generators.utils import random_int_range

Quadrant = Literal["I", "II", "III", "IV", "all"]


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
    max_mag = int(settings.get("max_coefficient_magnitude", settings.get("system_coef_max", 5)))
    min_mag = int(settings.get("system_coef_min", 1))
    lo = min(min_mag, max_mag)
    hi = max(min_mag, max_mag)
    return _random_in_bounds(
        settings,
        "system_coef_min",
        "system_coef_max",
        lo,
        hi,
        exclude={0} if bool(settings.get("exclude_zero_coefficients", True)) else None,
    )


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


class WritingLinearEquationsFramework(QuestionFramework):
    """Write linear equations from slope/point, two points, or intercept info."""

    instruction_latex = r"\text{Write an equation of the line.}"
    instruction_text = "Write an equation of the line."

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        mode = random.choice(["slope_point", "two_points", "slope_intercept"])
        if mode == "slope_point":
            m = _random_slope(settings)
            x1, y1 = _random_point(settings)
            b = y1 - m * x1
            prompt = (
                f"\\text{{Write the equation of the line with slope }} {m} "
                f"\\text{{ that passes through }} ({x1}, {y1})."
            )
            answer = _slope_intercept_latex(m, b)
        elif mode == "two_points":
            m = _random_slope(settings)
            b = _random_intercept(settings)
            x1, y1 = _random_point(settings)
            _, coord_max = _bounds(settings, "coord_min", "coord_max", -8, 8)
            dx = random_int_range(1, max(1, abs(coord_max)), exclude=set())
            x2 = x1 + dx * random.choice([-1, 1])
            y2 = m * x2 + b
            prompt = (
                f"\\text{{Write the equation of the line through }} "
                f"({x1}, {y1}) \\text{{ and }} ({x2}, {y2})."
            )
            answer = _slope_intercept_latex(m, b)
        else:
            m = _random_slope(settings)
            b = _random_intercept(settings)
            prompt = (
                f"\\text{{Write the equation of the line with slope }} {m} "
                f"\\text{{ and }} y\\text{{-intercept }} {b}."
            )
            answer = _slope_intercept_latex(m, b)
        return prompt, "Write linear equation", answer

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return question_metadata(linear_form="slope_intercept")


class SlopeFramework(QuestionFramework):
    """Find slope from two points or from a linear equation."""

    instruction_latex = r"\text{Find the slope.}"
    instruction_text = "Find the slope."

    def __init__(self, *, from_equation: bool = False) -> None:
        self.from_equation = from_equation
        self._last_plane_spec: CoordinatePlaneSpec | None = None

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        if self.from_equation:
            m = _random_slope(settings)
            b = _random_intercept(settings)
            eq = _slope_intercept_latex(m, b)
            prompt = f"\\text{{Find the slope of the line }} {eq}."
            answer = str(m)
            self._last_plane_spec = _plane_spec(settings, slope=m, y_intercept=b)
            return prompt, "Slope from equation", answer

        x1, y1 = _random_point(settings)
        dx = random_int_range(-5, 5, exclude={0})
        dy = random_int_range(-5, 5, exclude={0})
        x2, y2 = x1 + dx, y1 + dy
        slope = _slope_from_points(x1, y1, x2, y2)
        prompt = (
            f"\\text{{Find the slope of the line through }} "
            f"({x1}, {y1}) \\text{{ and }} ({x2}, {y2})."
        )
        answer = _frac_latex(slope) if slope.denominator != 1 else str(slope.numerator)
        # Keep fractional slopes (e.g. -1/2); integer truncation drew the wrong line.
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
        return prompt, "Slope from points", answer

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return question_metadata(slope_source="equation" if self.from_equation else "two_points")

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
        eq1 = f"{a1}x + {b1}y = {c1}"
        eq2 = f"{a2}x + {b2}y = {c2}"
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
        eq2 = f"{a2}x + {b2}y = {c2}"
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
                answer = f"y = {k}x"
            else:
                prompt = (
                    f"\\text{{If }} y \\text{{ varies directly with }} x "
                    f"\\text{{ and }} y = {y} \\text{{ when }} x = {x}, "
                    f"\\text{{ write the equation.}}"
                )
                answer = f"y = {k}x"
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
        prompt = f"\\text{{Complete the table for }} y = {m}x + {b}. \\\\ {table}"
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
