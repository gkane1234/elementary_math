"""Geometry figure framework — angles, triangles, circles, and measurement prompts."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Any, Literal

from .base import QuestionFramework
from ..core.metadata import DiagramSpec, question_metadata
from ..generators.utils import random_int_range

FigureType = Literal[
    "triangle",
    "rectangle",
    "parallelogram",
    "trapezoid",
    "circle",
    "prism",
    "cylinder",
    "sphere",
    "composite",
]

_ANGLE_LABELS = ["A", "B", "C", "D", "E", "F"]
_TRIANGLE_LABELS = ["A", "B", "C"]


@dataclass
class GeometryFigureSpec:
    """Labeled figure with dimensions for area/volume/measurement items."""

    figure_type: FigureType
    labels: list[str] = field(default_factory=list)
    dimensions: dict[str, float] = field(default_factory=dict)
    unit: str = "cm"

    def to_diagram_spec(self) -> DiagramSpec:
        """Convert to generic ``DiagramSpec`` for client renderers."""
        segments = [
            (self.labels[i], self.labels[i + 1])
            for i in range(len(self.labels) - 1)
        ]
        return DiagramSpec(
            kind=self.figure_type,
            labels=self.labels,
            segments=segments,
            angles=[],
        )


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


def _measurement_unit(settings: dict) -> str:
    return str(settings.get("measurement_unit", "cm"))


def _angle_unit(settings: dict) -> str:
    return str(settings.get("angle_unit", "degrees"))


def _format_angle(value: float, settings: dict) -> str:
    if _angle_unit(settings) == "radians":
        radians = math.radians(value) if value > 2 * math.pi else value
        return f"{radians:.2f}"
    return str(int(round(value)))


def _angle_symbol(settings: dict) -> str:
    return "rad" if _angle_unit(settings) == "radians" else "^\\circ"


def _random_angle(settings: dict) -> int:
    return _random_in_bounds(settings, "angle_min", "angle_max", 10, 170)


def _random_side(settings: dict) -> int:
    return _random_in_bounds(settings, "side_min", "side_max", 3, 20)


def _random_radius(settings: dict) -> int:
    return _random_in_bounds(settings, "radius_min", "radius_max", 2, 15)


def _random_similarity_ratio(settings: dict) -> int:
    return _random_in_bounds(
        settings, "similarity_ratio_min", "similarity_ratio_max", 2, 5
    )


def _random_coord(settings: dict) -> int:
    return _random_in_bounds(settings, "coord_min", "coord_max", -8, 8)


def _pythagorean_triple(max_leg: int) -> tuple[int, int, int]:
    triples = [
        (3, 4, 5),
        (5, 12, 13),
        (8, 15, 17),
        (7, 24, 25),
        (9, 40, 41),
        (6, 8, 10),
        (9, 12, 15),
        (12, 16, 20),
        (15, 20, 25),
    ]
    valid = [triple for triple in triples if max(triple[:2]) <= max_leg]
    if not valid:
        a = random.randint(3, max(3, max_leg // 2))
        b = random.randint(a + 1, max_leg)
        c = int(math.sqrt(a * a + b * b))
        while c * c != a * a + b * b:
            a = random.randint(3, max(3, max_leg // 2))
            b = random.randint(a + 1, max_leg)
            c = int(math.sqrt(a * a + b * b))
        return a, b, c
    return random.choice(valid)


def _classify_angle(degrees: int) -> str:
    if degrees == 90:
        return "right"
    if degrees < 90:
        return "acute"
    if degrees < 180:
        return "obtuse"
    return "straight"


def _figure_metadata(
    settings: dict,
    *,
    figure_type: FigureType,
    labels: list[str],
    dimensions: dict[str, float],
) -> dict[str, Any]:
    figure = GeometryFigureSpec(
        figure_type=figure_type,
        labels=labels,
        dimensions=dimensions,
        unit=_measurement_unit(settings),
    )
    meta: dict[str, Any] = {
        "figure_spec": {
            "figure_type": figure.figure_type,
            "labels": figure.labels,
            "dimensions": figure.dimensions,
            "unit": figure.unit,
        },
    }
    if bool(settings.get("include_diagram", False)):
        meta["diagram_spec"] = figure.to_diagram_spec()
    return question_metadata(**meta)


class GeometryFramework(QuestionFramework):
    """Shared batch generation for geometry measurement types."""

    quantity: str = "area"

    def __init__(self, *, figure_type: FigureType = "rectangle", quantity: str = "area"):
        self.figure_type = figure_type
        self.quantity = quantity

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return _figure_metadata(
            settings,
            figure_type=self.figure_type,
            labels=["A", "B", "C", "D"],
            dimensions={"length": 8.0, "width": 5.0},
        )

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        raise NotImplementedError(
            "GeometryFramework.build_prompt is a skeleton. "
            f"Implement formula for {self.figure_type} {self.quantity}."
        )


class AnglesFramework(GeometryFramework):
    """Find the measure of a given angle."""

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        angle = _random_angle(settings)
        vertex, p1, p2 = random.sample(_ANGLE_LABELS, 3)
        symbol = _angle_symbol(settings)
        prompt = f"m\\angle {p1}{vertex}{p2} = {angle}{symbol}"
        answer = f"{_format_angle(angle, settings)}{symbol}"
        return prompt, f"angle {p1}{vertex}{p2} = {angle}", answer

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return _figure_metadata(
            settings,
            figure_type="composite",
            labels=["A", "B", "C"],
            dimensions={"angle_deg": float(_random_angle(settings))},
        )


class ClassifyingAnglesFramework(GeometryFramework):
    """Classify an angle as acute, right, obtuse, or straight."""

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        angle_min, angle_max = _bounds(settings, "angle_min", "angle_max", 10, 170)
        choices = list(range(max(1, angle_min), min(180, angle_max) + 1))
        if bool(settings.get("allow_right", True)):
            choices.append(90)
        angle = random.choice(choices)
        vertex, p1, p2 = random.sample(_ANGLE_LABELS, 3)
        symbol = _angle_symbol(settings)
        prompt = (
            f"\\text{{Classify }} m\\angle {p1}{vertex}{p2} = {angle}{symbol}"
            f"\\text{{ as acute, right, obtuse, or straight.}}"
        )
        answer = _classify_angle(angle)
        return prompt, f"classify angle {angle}", answer


class SegmentLengthFramework(GeometryFramework):
    """Find the length of a line segment."""

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        unit = _measurement_unit(settings)
        length = _random_side(settings)
        a, b = random.sample(_ANGLE_LABELS, 2)
        prompt = f"\\overline{{{a}{b}}} = {length}\\text{{ {unit}}}"
        answer = f"{length}\\text{{ {unit}}}"
        return prompt, f"segment {a}{b} = {length} {unit}", answer

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        length = float(_random_side(settings))
        return _figure_metadata(
            settings,
            figure_type="composite",
            labels=["A", "B"],
            dimensions={"length": length},
        )


class TriangleAngleSumFramework(GeometryFramework):
    """Use the triangle angle sum to find a missing angle."""

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        symbol = _angle_symbol(settings)
        a = _random_angle(settings)
        b = _random_angle(settings)
        while a + b >= 170:
            b = _random_angle(settings)
        missing = 180 - a - b
        labels = _TRIANGLE_LABELS
        known = random.sample(labels, 2)
        unknown = next(label for label in labels if label not in known)
        prompt = (
            f"\\text{{In }} \\triangle {''.join(labels)},\\ "
            f"m\\angle {known[0]} = {a}{symbol}\\text{{ and }} "
            f"m\\angle {known[1]} = {b}{symbol}.\\ "
            f"\\text{{Find }} m\\angle {unknown}."
        )
        answer = f"{missing}{symbol}"
        return prompt, f"triangle angle sum; find {unknown}", answer

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return _figure_metadata(
            settings,
            figure_type="triangle",
            labels=_TRIANGLE_LABELS,
            dimensions={"angle_a": 60.0, "angle_b": 70.0, "angle_c": 50.0},
        )


class TriangleAreaFramework(GeometryFramework):
    """Find the area of a triangle from base and height."""

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        unit = _measurement_unit(settings)
        base = _random_side(settings)
        height = _random_side(settings)
        area = base * height / 2
        labels = _TRIANGLE_LABELS
        prompt = (
            f"\\text{{Find the area of }} \\triangle {''.join(labels)} "
            f"\\text{{ with base }} {base}\\text{{ {unit}}} "
            f"\\text{{ and height }} {height}\\text{{ {unit}}}."
        )
        answer = f"{area:g}\\text{{ {unit}}}^2"
        return prompt, f"triangle area b={base} h={height}", answer

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        base = float(_random_side(settings))
        height = float(_random_side(settings))
        return _figure_metadata(
            settings,
            figure_type="triangle",
            labels=_TRIANGLE_LABELS,
            dimensions={"base": base, "height": height},
        )


class TrianglePerimeterFramework(GeometryFramework):
    """Find the perimeter of a triangle with three given sides."""

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        unit = _measurement_unit(settings)
        a = _random_side(settings)
        b = _random_side(settings)
        c = _random_side(settings)
        while a + b <= c or a + c <= b or b + c <= a:
            c = _random_side(settings)
        perimeter = a + b + c
        labels = _TRIANGLE_LABELS
        prompt = (
            f"\\text{{Find the perimeter of }} \\triangle {''.join(labels)} "
            f"\\text{{ with sides }} {a}\\text{{ {unit}}}, "
            f"{b}\\text{{ {unit}}}, \\text{{ and }} {c}\\text{{ {unit}}}."
        )
        answer = f"{perimeter}\\text{{ {unit}}}"
        return prompt, f"triangle perimeter {a}+{b}+{c}", answer

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        a = float(_random_side(settings))
        b = float(_random_side(settings))
        c = float(_random_side(settings))
        return _figure_metadata(
            settings,
            figure_type="triangle",
            labels=_TRIANGLE_LABELS,
            dimensions={"side_a": a, "side_b": b, "side_c": c},
        )


class PythagoreanTheoremFramework(GeometryFramework):
    """Find a missing side of a right triangle."""

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        unit = _measurement_unit(settings)
        _, side_max = _bounds(settings, "side_min", "side_max", 3, 20)
        a, b, c = _pythagorean_triple(side_max)
        labels = _TRIANGLE_LABELS
        missing = random.choice(["leg_a", "leg_b", "hypotenuse"])
        if missing == "leg_a":
            prompt = (
                f"\\text{{In right }} \\triangle {''.join(labels)},\\ "
                f"{labels[2]} \\text{{ is the right angle, }} "
                f"{labels[1]}{labels[2]} = {b}\\text{{ {unit}}}, "
                f"\\text{{ and }} {labels[0]}{labels[2]} = {c}\\text{{ {unit}}}.\\ "
                f"\\text{{Find }} {labels[0]}{labels[1]}."
            )
            answer = f"{a}\\text{{ {unit}}}"
        elif missing == "leg_b":
            prompt = (
                f"\\text{{In right }} \\triangle {''.join(labels)},\\ "
                f"{labels[2]} \\text{{ is the right angle, }} "
                f"{labels[0]}{labels[1]} = {a}\\text{{ {unit}}}, "
                f"\\text{{ and }} {labels[0]}{labels[2]} = {c}\\text{{ {unit}}}.\\ "
                f"\\text{{Find }} {labels[1]}{labels[2]}."
            )
            answer = f"{b}\\text{{ {unit}}}"
        else:
            prompt = (
                f"\\text{{In right }} \\triangle {''.join(labels)},\\ "
                f"{labels[2]} \\text{{ is the right angle, }} "
                f"{labels[0]}{labels[1]} = {a}\\text{{ {unit}}}, "
                f"\\text{{ and }} {labels[1]}{labels[2]} = {b}\\text{{ {unit}}}.\\ "
                f"\\text{{Find }} {labels[0]}{labels[2]}."
            )
            answer = f"{c}\\text{{ {unit}}}"
        return prompt, "pythagorean theorem", answer

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        _, side_max = _bounds(settings, "side_min", "side_max", 3, 20)
        a, b, c = _pythagorean_triple(side_max)
        return _figure_metadata(
            settings,
            figure_type="triangle",
            labels=_TRIANGLE_LABELS,
            dimensions={"leg_a": float(a), "leg_b": float(b), "hypotenuse": float(c)},
        )


class SimilarTrianglesFramework(GeometryFramework):
    """Use similarity ratios to find a missing side."""

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        unit = _measurement_unit(settings)
        ratio = _random_similarity_ratio(settings)
        side_a = _random_side(settings)
        side_b = _random_side(settings)
        large_a = side_a * ratio
        large_b = side_b * ratio
        labels = _TRIANGLE_LABELS
        if random.choice([True, False]):
            prompt = (
                f"\\triangle {''.join(labels)} \\sim \\triangle DEF.\\ "
                f"{labels[0]}{labels[1]} = {side_a}\\text{{ {unit}}}, "
                f"{labels[1]}{labels[2]} = {side_b}\\text{{ {unit}}}, "
                f"\\text{{and the similarity ratio is }} {ratio} : 1.\\ "
                f"\\text{{Find }} EF."
            )
            answer = f"{large_b}\\text{{ {unit}}}"
        else:
            prompt = (
                f"\\triangle {''.join(labels)} \\sim \\triangle DEF.\\ "
                f"DE = {large_a}\\text{{ {unit}}} "
                f"\\text{{and }} EF = {large_b}\\text{{ {unit}}}.\\ "
                f"\\text{{Find }} {labels[0]}{labels[1]}."
            )
            answer = f"{side_a}\\text{{ {unit}}}"
        return prompt, f"similar triangles ratio {ratio}", answer

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        ratio = float(_random_similarity_ratio(settings))
        return _figure_metadata(
            settings,
            figure_type="triangle",
            labels=_TRIANGLE_LABELS,
            dimensions={"similarity_ratio": ratio},
        )


class CircleMeasureFramework(GeometryFramework):
    """Find circumference or area of a circle."""

    def __init__(self, *, quantity: Literal["circumference", "area", "either"] = "either"):
        super().__init__(figure_type="circle")
        self.circle_quantity = quantity

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        unit = _measurement_unit(settings)
        radius = _random_radius(settings)
        quantity = self.circle_quantity
        if quantity == "either":
            quantity = random.choice(["circumference", "area"])
        if quantity == "circumference":
            prompt = (
                f"\\text{{Find the circumference of a circle with radius }} "
                f"{radius}\\text{{ {unit}}}."
            )
            answer = f"{2 * radius}\\pi\\text{{ {unit}}}"
        else:
            prompt = (
                f"\\text{{Find the area of a circle with radius }} "
                f"{radius}\\text{{ {unit}}}."
            )
            answer = f"{radius * radius}\\pi\\text{{ {unit}}}^2"
        return prompt, f"circle {quantity} r={radius}", answer

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        radius = float(_random_radius(settings))
        return _figure_metadata(
            settings,
            figure_type="circle",
            labels=["O"],
            dimensions={"radius": radius},
        )


class CoordinateDistanceFramework(GeometryFramework):
    """Find the distance between two coordinate-plane points."""

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        integer_only = bool(settings.get("integer_coordinates", True))
        x1, y1 = _random_coord(settings), _random_coord(settings)
        x2, y2 = _random_coord(settings), _random_coord(settings)
        while x1 == x2 and y1 == y2:
            x2, y2 = _random_coord(settings), _random_coord(settings)
        dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        prompt = (
            f"\\text{{Find the distance between }} ({x1}, {y1}) "
            f"\\text{{ and }} ({x2}, {y2})."
        )
        if integer_only and dist == int(dist):
            answer = str(int(dist))
        else:
            answer = f"{dist:.3g}"
        return prompt, f"distance ({x1},{y1}) to ({x2},{y2})", answer

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return question_metadata(
            coordinate_points=[
                {"x": _random_coord(settings), "y": _random_coord(settings)},
                {"x": _random_coord(settings), "y": _random_coord(settings)},
            ]
        )
