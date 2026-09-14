"""G6 geometry / measurement generators via GeometryMeasure.

Overrides catalog generator keys only when the topic is a G6 geometry leaf.
PA / Geometry catalog types that share ``plotting_points`` / ``geo_triangle_area``
keep the old frameworks.
"""

from __future__ import annotations

from typing import Any, Callable

from question_engine.core.models import Question
from question_engine.frameworks.primitives.geometry_skeleton import (
    G6_GEO_MODES,
    call_legacy_geometry,
    generate_g6_geometry,
    use_geometry_skeleton,
)


def _dispatch(legacy_key: str) -> Callable[[str, dict], list[Question]]:
    def generator(topic: str, settings: dict[str, Any]) -> list[Question]:
        leaf = str(topic or "")
        if leaf in G6_GEO_MODES and use_geometry_skeleton(settings, leaf):
            return generate_g6_geometry(leaf, settings)
        # Tests sometimes pass the generator key as topic; still honor G6 leaves
        # when settings carry ``_topic_id``.
        topic_id = str(settings.get("_topic_id") or "")
        if topic_id in G6_GEO_MODES and use_geometry_skeleton(settings, topic_id):
            return generate_g6_geometry(topic_id, settings)
        return call_legacy_geometry(leaf or legacy_key, settings, generator_key=legacy_key)

    return generator


# Catalog generator keys that G6 geometry leaves use.
GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = {
    "plotting_points": _dispatch("plotting_points"),
    "geo_coordinate_distance": _dispatch("geo_coordinate_distance"),
    "g6_coordinate_perimeter": _dispatch("g6_coordinate_perimeter"),
    "geo_parallelogram_area": _dispatch("geo_parallelogram_area"),
    "geo_triangle_area": _dispatch("geo_triangle_area"),
    "geo_trapezoid_area": _dispatch("geo_trapezoid_area"),
    "geo_kite_area": _dispatch("geo_kite_area"),
    "g6_polygon_grid_area": _dispatch("g6_polygon_grid_area"),
    "g6_shaded_polygon_area": _dispatch("g6_shaded_polygon_area"),
    "g6_classify_polyhedron": _dispatch("g6_classify_polyhedron"),
    "g6_isometric_measure": _dispatch("g6_isometric_measure"),
    "geo_solid_volume_surface": _dispatch("geo_solid_volume_surface"),
    "g6_fraction_rectangle_area": _dispatch("g6_fraction_rectangle_area"),
    "g6_fraction_triangle_area": _dispatch("g6_fraction_triangle_area"),
    "g6_fraction_prism_volume": _dispatch("g6_fraction_prism_volume"),
}
