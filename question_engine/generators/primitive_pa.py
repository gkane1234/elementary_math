"""PA catalog wrappers — stamp skeleton_pattern without editing G6/geo engines.

Catalog leaves keep PA-prefixed generator keys. Underlying math is reused from
grade6 / numbers / grade_level / geometry / linear frameworks.
"""

from __future__ import annotations

from typing import Any, Callable

from question_engine.core.models import Question
from question_engine.generators.grade6 import (
    g6_divisibility,
    g6_factoring,
    g6_fraction_add_like,
    g6_fraction_add_unlike,
    g6_fraction_divide,
    g6_fraction_multiply,
    g6_fraction_subtract_like,
    g6_fraction_subtract_unlike,
    g6_greatest_common_factor,
    g6_integer_divide,
    g6_integer_multiply,
    g6_least_common_multiple,
)
from question_engine.generators.grade_level import (
    place_value_and_rounding,
    simplifying_numeric_fractions,
    writing_numbers_with_words,
)
from question_engine.generators.numbers import (
    converting_fractions_and_decimals,
    fractions_decimals_and_percents,
    pa_integers_adding_and_subtracting as _pa_int_add,
    pa_squares_and_square_roots as _pa_squares,
)


def _stamp(
    fn: Callable[[str, dict], list[Question]],
    pattern: str,
    engine: str,
) -> Callable[[str, dict], list[Question]]:
    def generate(topic: str, settings: dict) -> list[Question]:
        qs = fn(topic, settings)
        for q in qs:
            md: dict[str, Any] = dict(q.metadata or {})
            md["skeleton_pattern"] = pattern
            md.setdefault("primitive_engine", engine)
            q.metadata = md
        return qs

    return generate


def _geo(key: str, pattern: str = "GeoMeasure") -> Callable[[str, dict], list[Question]]:
    def generate(topic: str, settings: dict) -> list[Question]:
        from question_engine.generators.geometry import GENERATORS as GEO

        qs = GEO[key](topic, settings)
        for q in qs:
            md: dict[str, Any] = dict(q.metadata or {})
            md["skeleton_pattern"] = pattern
            md.setdefault("primitive_engine", "geometry_reuse")
            q.metadata = md
        return qs

    return generate


def _plotting_points(topic: str, settings: dict) -> list[Question]:
    from question_engine.generators.linear import GENERATORS as LIN

    qs = LIN["plotting_points"](topic, settings)
    for q in qs:
        md: dict[str, Any] = dict(q.metadata or {})
        md["skeleton_pattern"] = "PlotPoints"
        md.setdefault("primitive_engine", "plotting_points")
        q.metadata = md
    return qs


GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = {
    "pa_naming_decimal_places_and_rounding": _stamp(
        place_value_and_rounding, "NumberOp", "place_value"
    ),
    "pa_writing_numbers_with_words": _stamp(
        writing_numbers_with_words, "NumberOp", "writing_words"
    ),
    "pa_integers_adding_and_subtracting": _stamp(
        _pa_int_add, "NumberOp", "integer_ops"
    ),
    "pa_integers_multiplying": _stamp(g6_integer_multiply, "NumberOp", "integer_ops"),
    "pa_integers_dividing": _stamp(g6_integer_divide, "NumberOp", "integer_ops"),
    "pa_factoring": _stamp(g6_factoring, "NumberOp", "factoring"),
    "pa_greatest_common_factor": _stamp(
        g6_greatest_common_factor, "NumberOp", "gcf"
    ),
    "pa_least_common_multiple": _stamp(
        g6_least_common_multiple, "NumberOp", "lcm"
    ),
    "pa_simplifying_fractions": _stamp(
        simplifying_numeric_fractions, "NumberOp", "simplify_frac"
    ),
    "pa_fractions_add_like": _stamp(g6_fraction_add_like, "NumberOp", "frac_ops"),
    "pa_fractions_subtract_like": _stamp(
        g6_fraction_subtract_like, "NumberOp", "frac_ops"
    ),
    "pa_fractions_add_unlike": _stamp(g6_fraction_add_unlike, "NumberOp", "frac_ops"),
    "pa_fractions_subtract_unlike": _stamp(
        g6_fraction_subtract_unlike, "NumberOp", "frac_ops"
    ),
    "pa_fractions_multiply": _stamp(g6_fraction_multiply, "NumberOp", "frac_ops"),
    "pa_fractions_divide": _stamp(g6_fraction_divide, "NumberOp", "frac_ops"),
    "pa_converting_fractions_and_decimals": _stamp(
        converting_fractions_and_decimals, "NumberOp", "frac_decimal"
    ),
    "pa_divisibility": _stamp(g6_divisibility, "NumberOp", "divisibility"),
    "pa_squares_and_square_roots": _stamp(_pa_squares, "NumberOp", "squares"),
    "pa_fractions_decimals_and_percents": _stamp(
        fractions_decimals_and_percents, "NumberOp", "fdp"
    ),
    "pa_plotting_points": _plotting_points,
    "pa_drawing_and_measuring_angles": _geo("geo_angles"),
    "pa_angle_relationships": _geo("geo_angle_relationships"),
    "pa_plane_figures_triangles": _geo("geo_triangle_area"),
    "pa_quadrilaterals": _geo("geo_quadrilateral_area"),
    "pa_area_of_triangles_and_quadrilaterals": _geo(
        "geo_triangles_and_quadrilaterals_area"
    ),
    "pa_circles": _geo("geo_circle_measure"),
    "pa_transformations": _geo("geo_transformations", "Transform"),
    "pa_classifying_volume_and_surface_area": _geo("geo_solid_volume_surface"),
    "pa_pythagorean_theorem": _geo("geo_pythagorean_theorem"),
}
