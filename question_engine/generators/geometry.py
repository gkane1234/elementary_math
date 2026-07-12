"""Geometry generators backed by ``frameworks.geometry`` and extensions."""

from __future__ import annotations

from typing import Callable

from ..core.models import Question
from ..frameworks.geometry import (
    AnglesFramework,
    CircleMeasureFramework,
    ClassifyingAnglesFramework,
    CoordinateDistanceFramework,
    CoordinatePerimeterFramework,
    PythagoreanTheoremFramework,
    SegmentLengthFramework,
    SimilarTrianglesFramework,
    TriangleAngleSumFramework,
    TriangleAreaFramework,
    TrianglePerimeterFramework,
)
from ..frameworks.geometry_extended import (
    AlgebraFindingAnglesFramework,
    AngleAdditionFramework,
    AngleRelationshipsFramework,
    ArcLengthSectorFramework,
    CentralArcAngleFramework,
    ClassifyingTrianglesFramework,
    ExteriorAngleFramework,
    InscribedAngleFramework,
    IsoscelesTriangleFramework,
    KiteAreaFramework,
    ParallelTransversalFramework,
    ParallelogramAreaFramework,
    PolygonInteriorAngleFramework,
    RemainingGeometryFramework,
    SegmentAdditionFramework,
    SolidVolumeSurfaceFramework,
    SpecialRightTriangleFramework,
    TrapezoidAreaFramework,
    TriangleInequalityFramework,
)
from ..frameworks.trigonometry import RightTriangleTrigFramework

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
_COORDINATE_PERIMETER = CoordinatePerimeterFramework()
_ANGLE_ADDITION = AngleAdditionFramework()
_SEGMENT_ADDITION = SegmentAdditionFramework()
_ANGLE_RELATIONSHIPS = AngleRelationshipsFramework()
_ALGEBRA_FINDING_ANGLES = AlgebraFindingAnglesFramework()
_EXTERIOR_ANGLE = ExteriorAngleFramework()
_CLASSIFYING_TRIANGLES = ClassifyingTrianglesFramework()
_ISOSCELES = IsoscelesTriangleFramework()
_PARALLEL_TRANSVERSAL = ParallelTransversalFramework()
_TRIANGLE_INEQUALITY = TriangleInequalityFramework()
_SPECIAL_RIGHT = SpecialRightTriangleFramework()
_POLYGON_INTERIOR = PolygonInteriorAngleFramework()
_PARALLELOGRAM_AREA = ParallelogramAreaFramework()
_TRAPEZOID_AREA = TrapezoidAreaFramework()
_KITE_AREA = KiteAreaFramework()
_CENTRAL_ARC = CentralArcAngleFramework()
_INSCRIBED = InscribedAngleFramework()
_ARC_SECTOR = ArcLengthSectorFramework()
_SOLID = SolidVolumeSurfaceFramework()
_TRIG_RATIO = RightTriangleTrigFramework(mode="ratio")
_TRIG_ANGLE = RightTriangleTrigFramework(mode="angle")
_TRIG_SIDE = RightTriangleTrigFramework(mode="side")
_TRIG_ANY = RightTriangleTrigFramework(mode="any")


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
    "g6_coordinate_perimeter": lambda topic, settings: _batch(_COORDINATE_PERIMETER, topic, settings),
    "geo_angle_addition": lambda topic, settings: _batch(_ANGLE_ADDITION, topic, settings),
    "geo_segment_addition": lambda topic, settings: _batch(_SEGMENT_ADDITION, topic, settings),
    "geo_angle_relationships": lambda topic, settings: _batch(_ANGLE_RELATIONSHIPS, topic, settings),
    "finding_angles": lambda topic, settings: _batch(_ALGEBRA_FINDING_ANGLES, topic, settings),
    "geo_exterior_angle": lambda topic, settings: _batch(_EXTERIOR_ANGLE, topic, settings),
    "geo_classifying_triangles": lambda topic, settings: _batch(_CLASSIFYING_TRIANGLES, topic, settings),
    "geo_isosceles_triangle": lambda topic, settings: _batch(_ISOSCELES, topic, settings),
    "geo_parallel_transversal": lambda topic, settings: _batch(_PARALLEL_TRANSVERSAL, topic, settings),
    "geo_triangle_inequality": lambda topic, settings: _batch(_TRIANGLE_INEQUALITY, topic, settings),
    "geo_special_right_triangle": lambda topic, settings: _batch(_SPECIAL_RIGHT, topic, settings),
    "geo_polygon_interior": lambda topic, settings: _batch(_POLYGON_INTERIOR, topic, settings),
    "geo_parallelogram_area": lambda topic, settings: _batch(_PARALLELOGRAM_AREA, topic, settings),
    "geo_trapezoid_area": lambda topic, settings: _batch(_TRAPEZOID_AREA, topic, settings),
    "geo_kite_area": lambda topic, settings: _batch(_KITE_AREA, topic, settings),
    "geo_central_arc": lambda topic, settings: _batch(_CENTRAL_ARC, topic, settings),
    "geo_inscribed_angle": lambda topic, settings: _batch(_INSCRIBED, topic, settings),
    "geo_arc_sector": lambda topic, settings: _batch(_ARC_SECTOR, topic, settings),
    "geo_solid_volume_surface": lambda topic, settings: _batch(_SOLID, topic, settings),
    "geo_right_triangle_trig": lambda topic, settings: _batch(_TRIG_ANY, topic, settings),
    "geo_right_triangle_trig_ratio": lambda topic, settings: _batch(_TRIG_RATIO, topic, settings),
    "geo_right_triangle_trig_angle": lambda topic, settings: _batch(_TRIG_ANGLE, topic, settings),
    "geo_right_triangle_trig_side": lambda topic, settings: _batch(_TRIG_SIDE, topic, settings),
    "geo_geometric_notation": lambda topic, settings: _batch(RemainingGeometryFramework("notation"), topic, settings),
    "geo_triangle_congruence": lambda topic, settings: _batch(RemainingGeometryFramework("congruence"), topic, settings),
    "geo_triangle_congruence_proof": lambda topic, settings: _batch(RemainingGeometryFramework("congruence_proof"), topic, settings),
    "geo_triangle_midsegment": lambda topic, settings: _batch(RemainingGeometryFramework("midsegment"), topic, settings),
    "geo_triangle_angle_bisector": lambda topic, settings: _batch(RemainingGeometryFramework("angle_bisector"), topic, settings),
    "geo_triangle_median": lambda topic, settings: _batch(RemainingGeometryFramework("medians"), topic, settings),
    "geo_triangle_centroid": lambda topic, settings: _batch(RemainingGeometryFramework("centroid"), topic, settings),
    "geo_quadrilateral_classifying": lambda topic, settings: _batch(RemainingGeometryFramework("quadrilateral_classifying"), topic, settings),
    "geo_regular_polygon_area": lambda topic, settings: _batch(RemainingGeometryFramework("regular_polygon_area"), topic, settings),
    "geo_similar_polygons": lambda topic, settings: _batch(RemainingGeometryFramework("similar_polygons"), topic, settings),
    "geo_proportional_parts": lambda topic, settings: _batch(RemainingGeometryFramework("proportional_parts"), topic, settings),
    "geo_circle_chords": lambda topic, settings: _batch(RemainingGeometryFramework("circle_chords"), topic, settings),
    "geo_circle_tangents": lambda topic, settings: _batch(RemainingGeometryFramework("tangents"), topic, settings),
    "geo_secant_tangent_segments": lambda topic, settings: _batch(RemainingGeometryFramework("secant_tangent"), topic, settings),
    "geo_circle_segment_measures": lambda topic, settings: _batch(RemainingGeometryFramework("circle_segments"), topic, settings),
    "geo_circle_equation_using": lambda topic, settings: _batch(RemainingGeometryFramework("circle_equation_using"), topic, settings),
    "geo_circle_equation_writing": lambda topic, settings: _batch(RemainingGeometryFramework("circle_equation_writing"), topic, settings),
    "geo_transformations": lambda topic, settings: _batch(RemainingGeometryFramework("transformations"), topic, settings),
    "geo_construction_segments": lambda topic, settings: _batch(RemainingGeometryFramework("construction_segments"), topic, settings),
    "geo_construction_perpendicular": lambda topic, settings: _batch(RemainingGeometryFramework("construction_perpendicular"), topic, settings),
    "geo_construction_angles": lambda topic, settings: _batch(RemainingGeometryFramework("construction_angles"), topic, settings),
    "geo_construction_triangles": lambda topic, settings: _batch(RemainingGeometryFramework("construction_triangles"), topic, settings),
    "geo_construction_medians": lambda topic, settings: _batch(RemainingGeometryFramework("construction_medians"), topic, settings),
    "geo_construction_altitudes": lambda topic, settings: _batch(RemainingGeometryFramework("construction_altitudes"), topic, settings),
    "geo_construction_bisectors": lambda topic, settings: _batch(RemainingGeometryFramework("construction_bisectors"), topic, settings),
    "geo_construction_circles": lambda topic, settings: _batch(RemainingGeometryFramework("construction_circles"), topic, settings),
}
