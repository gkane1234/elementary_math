"""GeometryMeasure — G6 area / volume / coordinate from diagrams.

Reuses existing geometry frameworks and Grade 6 visual helpers. New sampling
only where the old path was a dump or a duplicate:

- plot / identify a point (old ``plotting_points`` dumped ``(x,y)→(x,y)``)
- axis-aligned distance with a diagram, unlocking vertical after D=0
- shaded composite = outer − inner (old ``shaded_polygon`` cloned grid polygons)

Other G6 geometry leaves wrap the live old generators and stamp
``skeleton_pattern``. Opt out with ``use_legacy_geometry=True`` or
``use_geometry_skeleton=False``.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Callable, Literal

from question_engine.core.models import Question
from question_engine.frameworks.difficulty_budget import settings_difficulty
from question_engine.generators.utils import make_questions

Mode = Literal[
    "plot_point",
    "axis_distance",
    "coord_perimeter",
    "parallelogram_area",
    "parallelogram_missing",
    "triangle_area",
    "triangle_missing",
    "trapezoid_area",
    "kite_area",
    "grid_polygon",
    "shaded_composite",
    "classify_polyhedron",
    "isometric",
    "cube_formula",
    "fraction_rectangle",
    "fraction_triangle",
    "fraction_prism",
]

PATTERN = "GeometryMeasure"

# Catalog type_id → mode. Shared generator keys (plotting_points, geo_triangle_area,
# …) are also used by PA / Geometry; only these topics take the G6 skeleton.
G6_GEO_MODES: dict[str, Mode] = {
    "g6_points_on_the_coordinate_plane": "plot_point",
    "g6_distances_on_the_coordinate_plane": "axis_distance",
    "g6_shapes_and_perimeter_on_the_coordinate_plane": "coord_perimeter",
    "g6_parallelograms": "parallelogram_area",
    "g6_parallelograms_understanding_area_formula": "parallelogram_missing",
    "g6_triangles": "triangle_area",
    "g6_triangles_understanding_area_formula": "triangle_missing",
    "g6_trapezoids": "trapezoid_area",
    "g6_kites": "kite_area",
    "g6_polygons_on_a_grid_or_coordinate_plane": "grid_polygon",
    "g6_polygons_and_shaded_regions": "shaded_composite",
    "g6_classifying_and_naming": "classify_polyhedron",
    "g6_volume_and_surface_area_using_isometric_drawings": "isometric",
    "g6_formulas_for_volume_and_surface_area_of_a_cube": "cube_formula",
    "g6_rectangles_with_fraction_side_lengths": "fraction_rectangle",
    "g6_triangles_with_fraction_side_lengths": "fraction_triangle",
    "g6_right_rectangular_prisms_with_fraction_side_lengths": "fraction_prism",
}

# Generator key used by the catalog / old path for each G6 type_id.
G6_LEGACY_KEY: dict[str, str] = {
    "g6_points_on_the_coordinate_plane": "plotting_points",
    "g6_distances_on_the_coordinate_plane": "geo_coordinate_distance",
    "g6_shapes_and_perimeter_on_the_coordinate_plane": "g6_coordinate_perimeter",
    "g6_parallelograms": "geo_parallelogram_area",
    "g6_parallelograms_understanding_area_formula": "geo_parallelogram_area",
    "g6_triangles": "geo_triangle_area",
    "g6_triangles_understanding_area_formula": "geo_triangle_area",
    "g6_trapezoids": "geo_trapezoid_area",
    "g6_kites": "geo_kite_area",
    "g6_polygons_on_a_grid_or_coordinate_plane": "g6_polygon_grid_area",
    "g6_polygons_and_shaded_regions": "g6_shaded_polygon_area",
    "g6_classifying_and_naming": "g6_classify_polyhedron",
    "g6_volume_and_surface_area_using_isometric_drawings": "g6_isometric_measure",
    "g6_formulas_for_volume_and_surface_area_of_a_cube": "geo_solid_volume_surface",
    "g6_rectangles_with_fraction_side_lengths": "g6_fraction_rectangle_area",
    "g6_triangles_with_fraction_side_lengths": "g6_fraction_triangle_area",
    "g6_right_rectangular_prisms_with_fraction_side_lengths": "g6_fraction_prism_volume",
}

_CUSTOM_MODES: frozenset[Mode] = frozenset(
    {"plot_point", "axis_distance", "shaded_composite"}
)

_LEGACY_FLAG = {
    "legacy",
    "hand",
}


def use_geometry_skeleton(settings: dict[str, Any] | None, topic: str = "") -> bool:
    s = dict(settings or {})
    if bool(s.get("use_legacy_geometry")) or bool(s.get("use_geometry_skeleton") is False):
        return False
    pat = str(s.get("skeleton_pattern", "")).strip()
    if pat in _LEGACY_FLAG:
        return False
    if topic and topic not in G6_GEO_MODES:
        return False
    if "use_geometry_skeleton" in s:
        return bool(s.get("use_geometry_skeleton"))
    if pat in {PATTERN, "geometry_measure", "geometry"}:
        return True
    return True


def _legacy_generators() -> dict[str, Callable[[str, dict], list[Question]]]:
    from question_engine.generators.geometry import GENERATORS as geo
    from question_engine.generators.grade6 import GENERATORS as g6
    from question_engine.generators.linear import GENERATORS as linear

    return {**linear, **geo, **g6}


def call_legacy_geometry(
    topic: str,
    settings: dict[str, Any],
    *,
    generator_key: str | None = None,
) -> list[Question]:
    key = generator_key or G6_LEGACY_KEY.get(topic) or topic
    gens = _legacy_generators()
    fn = gens.get(key)
    if fn is None:
        raise KeyError(f"no legacy geometry generator for {topic!r} ({key})")
    return fn(topic, settings)


def _stamp(qs: list[Question], *, mode: Mode, **extra: Any) -> list[Question]:
    for q in qs:
        meta = dict(q.metadata or {})
        meta["skeleton_pattern"] = PATTERN
        meta["primitive_engine"] = "geometry_skeleton"
        meta["mode"] = mode
        for k, v in extra.items():
            if v is not None and v != "":
                meta[k] = v
        q.metadata = meta
    return qs


@dataclass
class GeometryMeasureResult:
    prompt_latex: str
    prompt_text: str
    answer_latex: str
    mode: Mode
    construction: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def debug_dict(self) -> dict[str, Any]:
        return {
            "pattern": PATTERN,
            "mode": self.mode,
            "construction": self.construction,
            **self.metadata,
        }


def generate_g6_geometry(topic: str, settings: dict[str, Any]) -> list[Question]:
    mode = G6_GEO_MODES.get(topic)
    if mode is None:
        return call_legacy_geometry(topic, settings)
    if not use_geometry_skeleton(settings, topic):
        return call_legacy_geometry(topic, settings)
    if mode in _CUSTOM_MODES:
        return _generate_custom(topic, settings, mode)
    qs = call_legacy_geometry(topic, settings)
    return _stamp(qs, mode=mode)


def _generate_custom(
    topic: str, settings: dict[str, Any], mode: Mode
) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}

    def build() -> tuple[str, str, str | None]:
        if mode == "plot_point":
            item = sample_plot_or_identify_point(settings)
        elif mode == "axis_distance":
            item = sample_axis_aligned_distance(settings)
        else:
            item = sample_shaded_composite(settings)
        last["meta"] = {
            "skeleton_pattern": PATTERN,
            "primitive_engine": "geometry_skeleton",
            "mode": item.mode,
            "construction": item.construction,
            **item.metadata,
        }
        answer = item.answer_latex if include_answer_key else None
        return item.prompt_latex, item.prompt_text, answer

    def metadata_builder(_p: str, _t: str, _a: str | None) -> dict[str, Any]:
        return dict(last.get("meta") or {})

    return make_questions(
        topic,
        count,
        include_answer_key,
        build,
        metadata_builder=metadata_builder,
        settings=settings,
    )


# --- plot / identify a point -------------------------------------------------

def _coord_range(d: float) -> tuple[int, int]:
    if d < 8:
        return 1, 6
    if d < 16:
        return -6, 6
    return -8, 8


def _sample_ordered_pair(d: float) -> tuple[int, int]:
    lo, hi = _coord_range(d)
    if d < 8:
        return random.randint(lo, hi), random.randint(lo, hi)
    if d < 16:
        # Four quadrants; skip axes so "which quadrant" is unambiguous.
        xs = [n for n in range(lo, hi + 1) if n != 0]
        ys = [n for n in range(lo, hi + 1) if n != 0]
        return random.choice(xs), random.choice(ys)
    # High D: intercepts allowed.
    x, y = random.randint(lo, hi), random.randint(lo, hi)
    if x == 0 and y == 0 and random.random() < 0.7:
        x = random.choice([-3, -2, -1, 1, 2, 3])
    return x, y


def sample_plot_or_identify_point(settings: dict[str, Any]) -> GeometryMeasureResult:
    from question_engine.diagrams.grade6_figures import coordinate_points_svg

    d = settings_difficulty(settings, default=0.0)
    x, y = _sample_ordered_pair(d)
    pair = f"({x}, {y})"
    # Catalog says "Identify"; OpenStax 11.1 also plots. Mix both.
    identify_p = 0.45 if d < 8 else 0.5
    identify = random.random() < identify_p
    if identify:
        prompt = r"\text{What are the coordinates of point } A?"
        text = "What are the coordinates of point A?"
        construction = "identify_point"
        diagram = coordinate_points_svg([(x, y)], labels=["A"], blank=False)
        answer_diagram = diagram
    else:
        prompt = rf"\text{{Plot the point }} {pair} \text{{ on the coordinate plane.}}"
        text = f"Plot the point {pair} on the coordinate plane."
        construction = "plot_point"
        diagram = coordinate_points_svg([(x, y)], labels=["A"], blank=True)
        answer_diagram = coordinate_points_svg([(x, y)], labels=["A"], blank=False)
    return GeometryMeasureResult(
        prompt_latex=prompt,
        prompt_text=text,
        answer_latex=pair,
        mode="plot_point",
        construction=construction,
        metadata={
            "diagram_svg": diagram,
            "answer_diagram_svg": answer_diagram,
            "coordinate_points": [{"x": x, "y": y}],
            "form_id": construction,
        },
    )


# --- axis-aligned distance ---------------------------------------------------

def sample_axis_aligned_distance(settings: dict[str, Any]) -> GeometryMeasureResult:
    from question_engine.diagrams.grade6_figures import coordinate_points_svg

    d = settings_difficulty(settings, default=0.0)
    if d < 8:
        horizontal = True
        lo, hi = -5, 6
        dist_hi = 4
    elif d < 16:
        horizontal = random.random() < 0.45
        lo, hi = -8, 8
        dist_hi = 6
    else:
        horizontal = random.random() < 0.4
        lo, hi = -10, 10
        dist_hi = 8

    dist = random.randint(1, dist_hi)
    sign = random.choice([-1, 1])
    if horizontal:
        y = random.randint(lo, hi)
        x1 = random.randint(lo, hi)
        x2 = x1 + sign * dist
        if not (lo <= x2 <= hi):
            x2 = x1 - sign * dist
        y1 = y2 = y
    else:
        x = random.randint(lo, hi)
        y1 = random.randint(lo, hi)
        y2 = y1 + sign * dist
        if not (lo <= y2 <= hi):
            y2 = y1 - sign * dist
        x1 = x2 = x
    dist = abs(x2 - x1) + abs(y2 - y1)
    prompt = (
        rf"\text{{Find the distance between }} ({x1}, {y1}) "
        rf"\text{{ and }} ({x2}, {y2})."
    )
    text = f"Find the distance between ({x1}, {y1}) and ({x2}, {y2})."
    diagram = coordinate_points_svg(
        [(x1, y1), (x2, y2)],
        labels=["A", "B"],
        segment=True,
    )
    construction = "distance_h" if horizontal else "distance_v"
    return GeometryMeasureResult(
        prompt_latex=prompt,
        prompt_text=text,
        answer_latex=str(dist),
        mode="axis_distance",
        construction=construction,
        metadata={
            "diagram_svg": diagram,
            "coordinate_points": [{"x": x1, "y": y1}, {"x": x2, "y": y2}],
            "form_id": construction,
            "axis": "horizontal" if horizontal else "vertical",
        },
    )


# --- shaded composite (outer − inner) ----------------------------------------

def _place_rect(w: int, h: int) -> tuple[int, int]:
    """Origin so the rectangle fits on the 8×5 classroom grid."""
    x0 = random.randint(0, max(0, 8 - w))
    y0 = random.randint(0, max(0, 5 - h))
    return x0, y0


def _rect(x0: int, y0: int, w: int, h: int) -> list[tuple[int, int]]:
    return [(x0, y0), (x0 + w, y0), (x0 + w, y0 + h), (x0, y0 + h)]


def sample_shaded_composite(settings: dict[str, Any]) -> GeometryMeasureResult:
    from question_engine.diagrams.grade6_figures import shaded_composite_svg

    d = settings_difficulty(settings, default=0.0)
    if d < 8:
        kinds = ("rect_minus_triangle", "frame")
    elif d < 16:
        kinds = ("frame", "l_cut", "rect_minus_triangle")
    else:
        kinds = ("frame", "l_cut")
    kind = random.choice(kinds)

    if kind == "rect_minus_triangle":
        w = random.randint(3, 5)
        h = random.randint(3, 4)
        x0, y0 = _place_rect(w, h)
        outer = _rect(x0, y0, w, h)
        cut_b = random.randint(1, w - 1)
        cut_h = random.randint(1, h - 1)
        # Right triangle cut from the top-right corner.
        inner = [
            (x0 + w, y0 + h),
            (x0 + w - cut_b, y0 + h),
            (x0 + w, y0 + h - cut_h),
        ]
        area = Fraction(w * h) - Fraction(cut_b * cut_h, 2)
    elif kind == "frame":
        ow = random.randint(4, 6)
        oh = random.randint(3, 5)
        x0, y0 = _place_rect(ow, oh)
        inset = 1
        iw, ih = ow - 2 * inset, oh - 2 * inset
        if iw < 1 or ih < 1:
            iw, ih = max(1, ow - 2), max(1, oh - 2)
        outer = _rect(x0, y0, ow, oh)
        inner = _rect(x0 + inset, y0 + inset, iw, ih)
        area = Fraction(ow * oh - iw * ih)
    else:
        ow = random.randint(4, 6)
        oh = random.randint(3, 5)
        x0, y0 = _place_rect(ow, oh)
        cut_w = random.randint(1, ow - 1)
        cut_h = random.randint(1, oh - 1)
        outer = _rect(x0, y0, ow, oh)
        # Cut a rectangle from the top-right → L (OpenStax 9.5 patio).
        inner = _rect(x0 + ow - cut_w, y0 + oh - cut_h, cut_w, cut_h)
        area = Fraction(ow * oh - cut_w * cut_h)

    if area.denominator == 1:
        body = str(area.numerator)
    else:
        from question_engine.generators.utils import frac_latex

        body = frac_latex(area)
    answer = rf"{body}\text{{ square units}}"
    prompt = r"\text{Find the area of the shaded region on the grid.}"
    diagram = shaded_composite_svg(outer, inner)
    return GeometryMeasureResult(
        prompt_latex=prompt,
        prompt_text="Find the area of the shaded region on the grid.",
        answer_latex=answer,
        mode="shaded_composite",
        construction=kind,
        metadata={
            "diagram_svg": diagram,
            "shape_kind": kind,
            "form_id": kind,
            "area": str(area),
        },
    )
