"""Geometry generators backed by ``frameworks.geometry``."""

from __future__ import annotations

from typing import Callable

from ..core.models import Question
from ..frameworks.geometry import (
    AnglesFramework,
    CircleMeasureFramework,
    ClassifyingAnglesFramework,
    CoordinateDistanceFramework,
    PythagoreanTheoremFramework,
    SegmentLengthFramework,
    SimilarTrianglesFramework,
    TriangleAngleSumFramework,
    TriangleAreaFramework,
    TrianglePerimeterFramework,
)

_ANGLES = AnglesFramework()
_CLASSIFYING_ANGLES = ClassifyingAnglesFramework()
_SEGMENT_LENGTH = SegmentLengthFramework()
_TRIANGLE_ANGLE_SUM = TriangleAngleSumFramework()
_TRIANGLE_AREA = TriangleAreaFramework()
_TRIANGLE_PERIMETER = TrianglePerimeterFramework()
_PYTHAGOREAN = PythagoreanTheoremFramework()
_SIMILAR_TRIANGLES = SimilarTrianglesFramework()
_CIRCLE_MEASURE = CircleMeasureFramework()
_COORDINATE_DISTANCE = CoordinateDistanceFramework()


def _batch(framework, topic: str, settings: dict) -> list[Question]:
    return framework.generate_batch(topic, settings)


GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = {
    "geo_angles": lambda topic, settings: _batch(_ANGLES, topic, settings),
    "geo_classifying_angles": lambda topic, settings: _batch(_CLASSIFYING_ANGLES, topic, settings),
    "geo_segment_length": lambda topic, settings: _batch(_SEGMENT_LENGTH, topic, settings),
    "geo_triangle_angle_sum": lambda topic, settings: _batch(_TRIANGLE_ANGLE_SUM, topic, settings),
    "geo_triangle_area": lambda topic, settings: _batch(_TRIANGLE_AREA, topic, settings),
    "geo_triangle_perimeter": lambda topic, settings: _batch(_TRIANGLE_PERIMETER, topic, settings),
    "geo_pythagorean_theorem": lambda topic, settings: _batch(_PYTHAGOREAN, topic, settings),
    "geo_similar_triangles": lambda topic, settings: _batch(_SIMILAR_TRIANGLES, topic, settings),
    "geo_circle_measure": lambda topic, settings: _batch(_CIRCLE_MEASURE, topic, settings),
    "geo_coordinate_distance": lambda topic, settings: _batch(_COORDINATE_DISTANCE, topic, settings),
}
