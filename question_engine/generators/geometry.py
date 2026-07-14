"""Geometry generators backed by ``frameworks.geometry`` and extensions."""

from __future__ import annotations

from typing import Callable

from ..core.models import Question
from ..frameworks.adapters import framework_generators
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
    GeometricTransformationsFramework,
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

GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = framework_generators(
    {
        "geo_angles": AnglesFramework(),
        "geo_classifying_angles": ClassifyingAnglesFramework(),
        "geo_segment_length": SegmentLengthFramework(),
        "geo_triangle_angle_sum": TriangleAngleSumFramework(),
        "geo_triangle_area": TriangleAreaFramework(),
        "geo_triangle_perimeter": TrianglePerimeterFramework(),
        "geo_pythagorean_theorem": PythagoreanTheoremFramework(),
        "geo_similar_triangles": SimilarTrianglesFramework(),
        "geo_circle_measure": CircleMeasureFramework(),
        "geo_coordinate_distance": CoordinateDistanceFramework(),
        "g6_coordinate_perimeter": CoordinatePerimeterFramework(),
        "geo_angle_addition": AngleAdditionFramework(),
        "geo_segment_addition": SegmentAdditionFramework(),
        "geo_angle_relationships": AngleRelationshipsFramework(),
        "finding_angles": AlgebraFindingAnglesFramework(),
        "geo_exterior_angle": ExteriorAngleFramework(),
        "geo_classifying_triangles": ClassifyingTrianglesFramework(),
        "geo_isosceles_triangle": IsoscelesTriangleFramework(),
        "geo_parallel_transversal": ParallelTransversalFramework(),
        "geo_triangle_inequality": TriangleInequalityFramework(),
        "geo_special_right_triangle": SpecialRightTriangleFramework(),
        "geo_polygon_interior": PolygonInteriorAngleFramework(),
        "geo_parallelogram_area": ParallelogramAreaFramework(),
        "geo_trapezoid_area": TrapezoidAreaFramework(),
        "geo_kite_area": KiteAreaFramework(),
        "geo_central_arc": CentralArcAngleFramework(),
        "geo_inscribed_angle": InscribedAngleFramework(),
        "geo_arc_sector": ArcLengthSectorFramework(),
        "geo_solid_volume_surface": SolidVolumeSurfaceFramework(),
        "geo_right_triangle_trig": RightTriangleTrigFramework(mode="any"),
        "geo_right_triangle_trig_ratio": RightTriangleTrigFramework(mode="ratio"),
        "geo_right_triangle_trig_angle": RightTriangleTrigFramework(mode="angle"),
        "geo_right_triangle_trig_side": RightTriangleTrigFramework(mode="side"),
        "geo_geometric_notation": RemainingGeometryFramework("notation"),
        "geo_triangle_congruence": RemainingGeometryFramework("congruence"),
        "geo_triangle_congruence_proof": RemainingGeometryFramework("congruence_proof"),
        "geo_triangle_midsegment": RemainingGeometryFramework("midsegment"),
        "geo_triangle_angle_bisector": RemainingGeometryFramework("angle_bisector"),
        "geo_triangle_median": RemainingGeometryFramework("medians"),
        "geo_triangle_centroid": RemainingGeometryFramework("centroid"),
        "geo_quadrilateral_classifying": RemainingGeometryFramework(
            "quadrilateral_classifying"
        ),
        "geo_regular_polygon_area": RemainingGeometryFramework("regular_polygon_area"),
        "geo_similar_polygons": RemainingGeometryFramework("similar_polygons"),
        "geo_proportional_parts": RemainingGeometryFramework("proportional_parts"),
        "geo_circle_chords": RemainingGeometryFramework("circle_chords"),
        "geo_circle_tangents": RemainingGeometryFramework("tangents"),
        "geo_secant_tangent_segments": RemainingGeometryFramework("secant_tangent"),
        "geo_circle_segment_measures": RemainingGeometryFramework("circle_segments"),
        "geo_circle_equation_using": RemainingGeometryFramework("circle_equation_using"),
        "geo_circle_equation_writing": RemainingGeometryFramework(
            "circle_equation_writing"
        ),
        "geo_transformations": GeometricTransformationsFramework(),
        "geo_construction_segments": RemainingGeometryFramework("construction_segments"),
        "geo_construction_perpendicular": RemainingGeometryFramework(
            "construction_perpendicular"
        ),
        "geo_construction_angles": RemainingGeometryFramework("construction_angles"),
        "geo_construction_triangles": RemainingGeometryFramework("construction_triangles"),
        "geo_construction_medians": RemainingGeometryFramework("construction_medians"),
        "geo_construction_altitudes": RemainingGeometryFramework(
            "construction_altitudes"
        ),
        "geo_construction_bisectors": RemainingGeometryFramework(
            "construction_bisectors"
        ),
        "geo_construction_circles": RemainingGeometryFramework("construction_circles"),
    }
)
