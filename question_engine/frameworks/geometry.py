"""Geometry figure framework — angles, triangles, circles, and measurement prompts."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Any, Literal

from .base import QuestionFramework
from ..core.metadata import DiagramSpec, question_metadata
from ..diagrams import (
    GeometryFigure,
    angle_figure,
    circle_figure,
    parallelogram_figure,
    right_triangle_figure,
    segment_figure,
    trapezoid_figure,
    triangle_figure,
)
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
    diagram: GeometryFigure | None = None,
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
    include = bool(settings.get("include_diagram", True))
    if include and diagram is not None:
        meta.update(diagram.to_metadata())
    elif include:
        meta["diagram_spec"] = figure.to_diagram_spec()
    return question_metadata(**meta)


def _diagram_enabled(settings: dict) -> bool:
    return bool(settings.get("include_diagram", True))


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

    def __init__(self, *, figure_type: FigureType = "composite", quantity: str = "area"):
        super().__init__(figure_type=figure_type, quantity=quantity)
        self._last: dict[str, Any] = {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        angle = _random_angle(settings)
        vertex, p1, p2 = random.sample(_ANGLE_LABELS, 3)
        symbol = _angle_symbol(settings)
        prompt = (
            f"\\text{{Find }} m\\angle {p1}{vertex}{p2}"
            f"\\text{{ using the diagram.}}"
        )
        answer = f"{_format_angle(angle, settings)}{symbol}"
        self._last = {
            "angle": angle,
            "vertex": vertex,
            "p1": p1,
            "p2": p2,
            "figure": angle_figure(p1, vertex, p2, float(angle), show_measure=True),
        }
        return prompt, f"angle {p1}{vertex}{p2} = {angle}", answer

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
        last = self._last
        if not last:
            return {}
        return _figure_metadata(
            settings,
            figure_type="composite",
            labels=[last["p1"], last["vertex"], last["p2"]],
            dimensions={"angle_deg": float(last["angle"])},
            diagram=last.get("figure") if _diagram_enabled(settings) else None,
        )


class ClassifyingAnglesFramework(GeometryFramework):
    """Classify an angle as acute, right, obtuse, or straight."""

    def __init__(self, *, figure_type: FigureType = "composite", quantity: str = "area"):
        super().__init__(figure_type=figure_type, quantity=quantity)
        self._last: dict[str, Any] = {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        angle_min, angle_max = _bounds(settings, "angle_min", "angle_max", 10, 170)
        choices = list(range(max(1, angle_min), min(180, angle_max) + 1))
        if bool(settings.get("allow_right", True)):
            choices.append(90)
        angle = random.choice(choices)
        vertex, p1, p2 = random.sample(_ANGLE_LABELS, 3)
        symbol = _angle_symbol(settings)
        prompt = (
            f"\\text{{Classify }} \\angle {p1}{vertex}{p2}"
            f"\\text{{ as acute, right, obtuse, or straight.}}"
        )
        answer = _classify_angle(angle)
        self._last = {
            "angle": angle,
            "vertex": vertex,
            "p1": p1,
            "p2": p2,
            "figure": angle_figure(
                p1, vertex, p2, float(angle), show_measure=True, kind="classifying_angle"
            ),
        }
        # Keep measure in prompt_text for answer-key context; diagram shows degrees.
        _ = symbol
        return prompt, f"classify angle {angle}", answer

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
        last = self._last
        if not last:
            return {}
        return _figure_metadata(
            settings,
            figure_type="composite",
            labels=[last["p1"], last["vertex"], last["p2"]],
            dimensions={"angle_deg": float(last["angle"])},
            diagram=last.get("figure") if _diagram_enabled(settings) else None,
        )


class SegmentLengthFramework(GeometryFramework):
    """Find the length of a line segment."""

    def __init__(self, *, figure_type: FigureType = "composite", quantity: str = "area"):
        super().__init__(figure_type=figure_type, quantity=quantity)
        self._last: dict[str, Any] = {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        unit = _measurement_unit(settings)
        length = _random_side(settings)
        a, b = random.sample(_ANGLE_LABELS, 2)
        prompt = (
            f"\\text{{Find the length of }} \\overline{{{a}{b}}} "
            f"\\text{{ using the diagram.}}"
        )
        answer = f"{length}\\text{{ {unit}}}"
        self._last = {
            "length": length,
            "a": a,
            "b": b,
            "unit": unit,
            "figure": segment_figure(
                float(length), labels=(a, b), unit=unit, show_length=True
            ),
        }
        return prompt, f"segment {a}{b} = {length} {unit}", answer

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
        last = self._last
        if not last:
            return {}
        return _figure_metadata(
            settings,
            figure_type="composite",
            labels=[last["a"], last["b"]],
            dimensions={"length": float(last["length"])},
            diagram=last.get("figure") if _diagram_enabled(settings) else None,
        )


class TriangleAngleSumFramework(GeometryFramework):
    """Use the triangle angle sum to find a missing angle."""

    def __init__(self, *, figure_type: FigureType = "triangle", quantity: str = "area"):
        super().__init__(figure_type=figure_type, quantity=quantity)
        self._last: dict[str, Any] = {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        symbol = _angle_symbol(settings)
        a = _random_angle(settings)
        b = _random_angle(settings)
        while a + b >= 170:
            b = _random_angle(settings)
        missing = 180 - a - b
        labels = list(_TRIANGLE_LABELS)
        known = random.sample(labels, 2)
        unknown = next(label for label in labels if label not in known)
        angle_map = {known[0]: a, known[1]: b, unknown: missing}
        angles = (angle_map["A"], angle_map["B"], angle_map["C"])
        prompt = (
            f"\\text{{In }} \\triangle {''.join(labels)},\\ "
            f"m\\angle {known[0]} = {a}{symbol}\\text{{ and }} "
            f"m\\angle {known[1]} = {b}{symbol}.\\ "
            f"\\text{{Find }} m\\angle {unknown}."
        )
        answer = f"{missing}{symbol}"
        self._last = {
            "angles": angle_map,
            "unknown": unknown,
            "labels": labels,
            "figure": triangle_figure(labels, angles, missing=unknown),
        }
        return prompt, f"triangle angle sum; find {unknown}", answer

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
        last = self._last
        if not last:
            return {}
        angles = last["angles"]
        return _figure_metadata(
            settings,
            figure_type="triangle",
            labels=last["labels"],
            dimensions={
                "angle_a": float(angles["A"]),
                "angle_b": float(angles["B"]),
                "angle_c": float(angles["C"]),
            },
            diagram=last.get("figure") if _diagram_enabled(settings) else None,
        )


class TriangleAreaFramework(GeometryFramework):
    """Find the area of a triangle from base and height."""

    def __init__(self, *, figure_type: FigureType = "triangle", quantity: str = "area"):
        super().__init__(figure_type=figure_type, quantity=quantity)
        self._last: dict[str, Any] = {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        unit = _measurement_unit(settings)
        base = _random_side(settings)
        height = _random_side(settings)
        area = base * height / 2
        labels = list(_TRIANGLE_LABELS)
        prompt = (
            f"\\text{{Find the area of }} \\triangle {''.join(labels)}."
        )
        answer = f"{area:g}\\text{{ {unit}}}^2"
        # Right triangle with base/height labeled
        fig = right_triangle_figure(
            float(base),
            float(height),
            labels=(labels[0], labels[1], labels[2]),
            right_angle_at=labels[2],
            side_labels={
                f"{labels[1]}{labels[2]}": f"{base} {unit}",
                f"{labels[0]}{labels[2]}": f"{height} {unit}",
            },
            kind="triangle_area",
        )
        self._last = {
            "base": base,
            "height": height,
            "labels": labels,
            "figure": fig,
        }
        return prompt, f"triangle area b={base} h={height}", answer

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
        last = self._last
        if not last:
            return {}
        return _figure_metadata(
            settings,
            figure_type="triangle",
            labels=last["labels"],
            dimensions={"base": float(last["base"]), "height": float(last["height"])},
            diagram=last.get("figure") if _diagram_enabled(settings) else None,
        )


class TrianglePerimeterFramework(GeometryFramework):
    """Find the perimeter of a triangle with three given sides."""

    def __init__(self, *, figure_type: FigureType = "triangle", quantity: str = "area"):
        super().__init__(figure_type=figure_type, quantity=quantity)
        self._last: dict[str, Any] = {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        unit = _measurement_unit(settings)
        a = _random_side(settings)
        b = _random_side(settings)
        c = _random_side(settings)
        while a + b <= c or a + c <= b or b + c <= a:
            c = _random_side(settings)
        perimeter = a + b + c
        labels = list(_TRIANGLE_LABELS)
        # Approximate angles via law of cosines for a drawable triangle
        ang_a = math.degrees(math.acos(max(-1, min(1, (b * b + c * c - a * a) / (2 * b * c)))))
        ang_b = math.degrees(math.acos(max(-1, min(1, (a * a + c * c - b * b) / (2 * a * c)))))
        ang_c = 180 - ang_a - ang_b
        prompt = f"\\text{{Find the perimeter of }} \\triangle {''.join(labels)}."
        answer = f"{perimeter}\\text{{ {unit}}}"
        fig = triangle_figure(
            labels,
            (ang_a, ang_b, ang_c),
            side_labels={
                f"{labels[1]}{labels[2]}": f"{a} {unit}",
                f"{labels[0]}{labels[2]}": f"{b} {unit}",
                f"{labels[0]}{labels[1]}": f"{c} {unit}",
            },
            kind="triangle_perimeter",
        )
        self._last = {
            "a": a,
            "b": b,
            "c": c,
            "labels": labels,
            "figure": fig,
        }
        return prompt, f"triangle perimeter {a}+{b}+{c}", answer

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
        last = self._last
        if not last:
            return {}
        return _figure_metadata(
            settings,
            figure_type="triangle",
            labels=last["labels"],
            dimensions={
                "side_a": float(last["a"]),
                "side_b": float(last["b"]),
                "side_c": float(last["c"]),
            },
            diagram=last.get("figure") if _diagram_enabled(settings) else None,
        )


class PythagoreanTheoremFramework(GeometryFramework):
    """Find a missing side of a right triangle."""

    def __init__(self, *, figure_type: FigureType = "triangle", quantity: str = "area"):
        super().__init__(figure_type=figure_type, quantity=quantity)
        self._last: dict[str, Any] = {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        unit = _measurement_unit(settings)
        _, side_max = _bounds(settings, "side_min", "side_max", 3, 20)
        a, b, c = _pythagorean_triple(side_max)
        labels = list(_TRIANGLE_LABELS)
        missing = random.choice(["leg_a", "leg_b", "hypotenuse"])
        if missing == "leg_a":
            prompt = (
                f"\\text{{In right }} \\triangle {''.join(labels)},\\ "
                f"\\text{{find }} {labels[0]}{labels[1]}."
            )
            answer = f"{a}\\text{{ {unit}}}"
            side_labels = {
                f"{labels[1]}{labels[2]}": f"{b} {unit}",
                f"{labels[0]}{labels[2]}": f"{c} {unit}",
                f"{labels[0]}{labels[1]}": "?",
            }
        elif missing == "leg_b":
            prompt = (
                f"\\text{{In right }} \\triangle {''.join(labels)},\\ "
                f"\\text{{find }} {labels[1]}{labels[2]}."
            )
            answer = f"{b}\\text{{ {unit}}}"
            side_labels = {
                f"{labels[0]}{labels[1]}": f"{a} {unit}",
                f"{labels[0]}{labels[2]}": f"{c} {unit}",
                f"{labels[1]}{labels[2]}": "?",
            }
        else:
            prompt = (
                f"\\text{{In right }} \\triangle {''.join(labels)},\\ "
                f"\\text{{find }} {labels[0]}{labels[2]}."
            )
            answer = f"{c}\\text{{ {unit}}}"
            side_labels = {
                f"{labels[0]}{labels[1]}": f"{a} {unit}",
                f"{labels[1]}{labels[2]}": f"{b} {unit}",
                f"{labels[0]}{labels[2]}": "?",
            }
        fig = right_triangle_figure(
            float(a),
            float(b),
            labels=(labels[0], labels[1], labels[2]),
            right_angle_at=labels[2],
            side_labels=side_labels,
            kind="pythagorean",
        )
        self._last = {
            "a": a,
            "b": b,
            "c": c,
            "labels": labels,
            "figure": fig,
        }
        return prompt, "pythagorean theorem", answer

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
        last = self._last
        if not last:
            return {}
        return _figure_metadata(
            settings,
            figure_type="triangle",
            labels=last["labels"],
            dimensions={
                "leg_a": float(last["a"]),
                "leg_b": float(last["b"]),
                "hypotenuse": float(last["c"]),
            },
            diagram=last.get("figure") if _diagram_enabled(settings) else None,
        )


class SimilarTrianglesFramework(GeometryFramework):
    """Use similarity ratios to find a missing side."""

    def __init__(self, *, figure_type: FigureType = "triangle", quantity: str = "area"):
        super().__init__(figure_type=figure_type, quantity=quantity)
        self._last: dict[str, Any] = {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        unit = _measurement_unit(settings)
        ratio = _random_similarity_ratio(settings)
        side_a = _random_side(settings)
        side_b = _random_side(settings)
        large_a = side_a * ratio
        large_b = side_b * ratio
        labels = list(_TRIANGLE_LABELS)
        if random.choice([True, False]):
            prompt = (
                f"\\triangle {''.join(labels)} \\sim \\triangle DEF.\\ "
                f"\\text{{Find }} EF."
            )
            answer = f"{large_b}\\text{{ {unit}}}"
            side_labels = {
                f"{labels[0]}{labels[1]}": f"{side_a} {unit}",
                f"{labels[1]}{labels[2]}": f"{side_b} {unit}",
            }
        else:
            prompt = (
                f"\\triangle {''.join(labels)} \\sim \\triangle DEF.\\ "
                f"\\text{{Find }} {labels[0]}{labels[1]}."
            )
            answer = f"{side_a}\\text{{ {unit}}}"
            side_labels = {
                f"{labels[0]}{labels[1]}": "?",
                f"{labels[1]}{labels[2]}": f"{side_b} {unit}",
            }
        fig = triangle_figure(
            labels,
            (50, 60, 70),
            side_labels=side_labels,
            kind="similar_triangles",
        )
        self._last = {
            "ratio": ratio,
            "labels": labels,
            "figure": fig,
            "large_a": large_a,
        }
        return prompt, f"similar triangles ratio {ratio}", answer

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
        last = self._last
        if not last:
            return {}
        return _figure_metadata(
            settings,
            figure_type="triangle",
            labels=last["labels"],
            dimensions={"similarity_ratio": float(last["ratio"])},
            diagram=last.get("figure") if _diagram_enabled(settings) else None,
        )


class CircleMeasureFramework(GeometryFramework):
    """Find circumference or area of a circle."""

    def __init__(self, *, quantity: Literal["circumference", "area", "either"] = "either"):
        super().__init__(figure_type="circle")
        self.circle_quantity = quantity
        self._last: dict[str, Any] = {}

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
        self._last = {
            "radius": radius,
            "unit": unit,
            "quantity": quantity,
            "figure": circle_figure(float(radius), unit=unit),
        }
        return prompt, f"circle {quantity} r={radius}", answer

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
        last = self._last
        if not last:
            return {}
        return _figure_metadata(
            settings,
            figure_type="circle",
            labels=["O", "A"],
            dimensions={"radius": float(last["radius"])},
            diagram=last.get("figure") if _diagram_enabled(settings) else None,
        )


class CoordinateDistanceFramework(GeometryFramework):
    """Find the distance between two coordinate-plane points."""

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        integer_only = bool(settings.get("integer_coordinates", True))
        axis_aligned = bool(settings.get("axis_aligned_only", False))
        x1, y1 = _random_coord(settings), _random_coord(settings)
        if axis_aligned:
            if random.choice([True, False]):
                x2, y2 = x1, _random_coord(settings)
                while y2 == y1:
                    y2 = _random_coord(settings)
            else:
                x2, y2 = _random_coord(settings), y1
                while x2 == x1:
                    x2 = _random_coord(settings)
        else:
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


def _axis_aligned_perimeter(points: list[tuple[int, int]]) -> int:
    total = 0
    n = len(points)
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        total += abs(x2 - x1) + abs(y2 - y1)
    return total


def _random_axis_aligned_rectangle(settings: dict) -> list[tuple[int, int]]:
    lo, hi = _bounds(settings, "coord_min", "coord_max", 0, 8)
    max_side = max(2, min(6, int(settings.get("max_side", 5))))
    span = max(2, hi - lo)
    width = random.randint(2, min(max_side, span))
    height = random.randint(2, min(max_side, span))
    x = random.randint(lo, hi - width)
    y = random.randint(lo, hi - height)
    return [(x, y), (x + width, y), (x + width, y + height), (x, y + height)]


def _random_axis_aligned_l_shape(settings: dict) -> list[tuple[int, int]]:
    """Six-vertex L polygon with all sides parallel to the axes."""
    lo, hi = _bounds(settings, "coord_min", "coord_max", 0, 8)
    max_side = max(3, min(7, int(settings.get("max_side", 6))))
    span = max(3, hi - lo)
    outer_w = random.randint(3, min(max_side, span))
    outer_h = random.randint(3, min(max_side, span))
    cut_w = random.randint(1, outer_w - 1)
    cut_h = random.randint(1, outer_h - 1)
    x = random.randint(lo, hi - outer_w)
    y = random.randint(lo, hi - outer_h)
    # Cut from the top-right corner → staircase L.
    return [
        (x, y),
        (x + outer_w, y),
        (x + outer_w, y + cut_h),
        (x + cut_w, y + cut_h),
        (x + cut_w, y + outer_h),
        (x, y + outer_h),
    ]


class CoordinatePerimeterFramework(GeometryFramework):
    """Perimeter of an axis-aligned polygon on the coordinate plane (Grade 6)."""

    instruction_latex = r"\text{Find the perimeter.}"
    instruction_text = "Find the perimeter."

    def __init__(self) -> None:
        super().__init__(figure_type="rectangle", quantity="perimeter")
        self._last: dict[str, Any] = {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        allow_l = bool(settings.get("allow_l_shape", False))
        if allow_l and random.random() < 0.55:
            points = _random_axis_aligned_l_shape(settings)
            shape = "L-shaped polygon"
        else:
            points = _random_axis_aligned_rectangle(settings)
            shape = "rectangle" if len(points) == 4 else "polygon"
        labels = list("ABCDEF")[: len(points)]
        perimeter = _axis_aligned_perimeter(points)
        verts = ",\\ ".join(
            f"{lab}({x}, {y})" for lab, (x, y) in zip(labels, points)
        )
        prompt = (
            f"\\text{{A {shape} on the coordinate plane has vertices }} "
            f"{verts}\\text{{. Find the perimeter.}}"
        )
        from ..diagrams.grade6_figures import coordinate_polygon_svg

        self._last = {
            "points": points,
            "labels": labels,
            "perimeter": perimeter,
            "diagram_svg": coordinate_polygon_svg(points, labels=labels),
        }
        return prompt, f"perimeter of {shape} {points}", str(perimeter)

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return question_metadata(kind="coordinate_perimeter")

    def build_question_metadata(
        self,
        settings: dict,
        *,
        prompt_latex: str,
        prompt_text: str,
        answer: str | None,
    ) -> dict[str, Any]:
        last = self._last
        if not last:
            return {}
        return {
            "diagram_svg": last.get("diagram_svg"),
            "coordinate_points": [{"x": x, "y": y} for x, y in last.get("points", [])],
        }
