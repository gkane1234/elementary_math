"""Figure family registry — textbook-style diagram *kinds*, parameterized.

We do **not** copy OpenStax (or any) bitmaps. Families recreate common
textbook figure types (number lines, angle diagrams, area models, etc.) with
a parameter space so worksheets get varied silhouettes, not clones.

``sample_figure(family_id, difficulty, ...)`` returns layout/complexity params
(and optionally a built ``GeometryFigure``). Continuous ``difficulty`` unlocks
more complex variants. Batch item index + seed keep items within a worksheet
distinct while remaining reproducible.
"""

from __future__ import annotations

import hashlib
import math
import random
from dataclasses import dataclass, field
from typing import Any, Callable

from question_engine.frameworks.difficulty_budget import settings_difficulty

# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class FigureFamily:
    """One textbook figure *kind* with a difficulty-aware parameter space."""

    id: str
    topic_tags: tuple[str, ...]
    description: str
    courses: tuple[str, ...] = ("g6", "pa", "geo")
    # Named complexity tiers unlocked as continuous D rises.
    complexity_tiers: tuple[str, ...] = ("simple", "standard", "complex")


FIGURE_FAMILIES: dict[str, FigureFamily] = {
    "angle_rays": FigureFamily(
        id="angle_rays",
        topic_tags=("angles", "classify", "measure"),
        description="Two rays from a vertex; orientation and measure vary.",
        courses=("g6", "pa", "geo", "a1"),
    ),
    "adjacent_angles": FigureFamily(
        id="adjacent_angles",
        topic_tags=("angles", "addition", "complementary", "supplementary"),
        description="Multi-ray fan at one vertex; piece count rises with D.",
        courses=("pa", "geo", "a1"),
    ),
    "complementary_angles": FigureFamily(
        id="complementary_angles",
        topic_tags=("angles", "complementary"),
        description="Right angle split by a ray; rotation varies.",
        courses=("pa", "geo", "a1"),
    ),
    "supplementary_angles": FigureFamily(
        id="supplementary_angles",
        topic_tags=("angles", "supplementary"),
        description="Straight line + ray; which side is given / unknown varies.",
        courses=("pa", "geo", "a1"),
    ),
    "vertical_angles": FigureFamily(
        id="vertical_angles",
        topic_tags=("angles", "vertical"),
        description="Two intersecting lines; rotation of the pair varies.",
        courses=("pa", "geo", "a1"),
    ),
    "parallel_transversal": FigureFamily(
        id="parallel_transversal",
        topic_tags=("angles", "parallel", "transversal"),
        description="Parallels cut by a transversal; slant and relation vary.",
        courses=("pa", "geo"),
    ),
    "triangle_angles": FigureFamily(
        id="triangle_angles",
        topic_tags=("triangles", "angles"),
        description="Labeled triangle; rotation/reflection and missing vertex vary.",
        courses=("pa", "geo"),
    ),
    "right_triangle": FigureFamily(
        id="right_triangle",
        topic_tags=("triangles", "pythagorean", "trig"),
        description="Right triangle; orientation, reflection, unknown side vary.",
        courses=("pa", "geo", "a1", "a2"),
    ),
    "triangle_area": FigureFamily(
        id="triangle_area",
        topic_tags=("triangles", "area"),
        description="Base/height with right / interior / exterior altitude layouts.",
        courses=("g6", "pa", "geo"),
    ),
    "parallelogram": FigureFamily(
        id="parallelogram",
        topic_tags=("quadrilaterals", "area"),
        description="Parallelogram / rhombus silhouette; skew and lean vary.",
        courses=("g6", "pa", "geo"),
    ),
    "trapezoid": FigureFamily(
        id="trapezoid",
        topic_tags=("quadrilaterals", "area"),
        description="Trapezoid with bases/height; orientation varies.",
        courses=("g6", "pa", "geo"),
    ),
    "circle_radius": FigureFamily(
        id="circle_radius",
        topic_tags=("circles", "circumference", "area"),
        description="Circle with radius (or diameter) drawn at a varied angle.",
        courses=("pa", "geo", "a2"),
    ),
    "circle_sector": FigureFamily(
        id="circle_sector",
        topic_tags=("circles", "arc", "sector"),
        description="Circle with central angle / sector wedge.",
        courses=("geo", "a2"),
    ),
    "number_line": FigureFamily(
        id="number_line",
        topic_tags=("integers", "inequalities", "plot"),
        description="1D number line; range, tick density, and mark style scale with D.",
        courses=("g6", "pa", "a1"),
    ),
    "coordinate_plane": FigureFamily(
        id="coordinate_plane",
        topic_tags=("graphing", "coordinates", "functions"),
        description="Axes + points/curves; window and object count scale with D.",
        courses=("g6", "pa", "a1", "a2", "calc"),
    ),
    "percent_shade": FigureFamily(
        id="percent_shade",
        topic_tags=("percents", "fractions"),
        description="Grid / bar / circle shade models; pattern and figure unlock with D.",
        courses=("g6", "pa"),
    ),
    "area_model": FigureFamily(
        id="area_model",
        topic_tags=("distributive", "multiply"),
        description="Rectangle split for distributive / product models.",
        courses=("g6", "pa", "a1"),
    ),
    "tape_diagram": FigureFamily(
        id="tape_diagram",
        topic_tags=("equations", "ratios"),
        description="Tape / bar model with equal or unequal segments.",
        courses=("g6", "pa"),
    ),
    "function_sketch": FigureFamily(
        id="function_sketch",
        topic_tags=("functions", "calculus", "tangent"),
        description="Curve sketch with optional tangent / area shading (calc).",
        courses=("a2", "pc", "calc"),
        complexity_tiers=("simple", "standard", "complex", "related_rates"),
    ),
    "decimal_grid": FigureFamily(
        id="decimal_grid",
        topic_tags=("decimals", "place_value", "addition", "subtraction"),
        description="Place-value columns or hundredths shade for decimal ±.",
        courses=("g6", "pa"),
    ),
    "box_plot": FigureFamily(
        id="box_plot",
        topic_tags=("statistics", "box_plot", "iqr"),
        description="Box-and-whisker layout; whisker/outlier unlock with D.",
        courses=("g6", "pa", "a1"),
    ),
}


# type_id / generator family → primary figure family (documentation + helpers).
TYPE_ID_FAMILY: dict[str, str] = {
    # Angles
    "geo_basics_classifying_angles": "angle_rays",
    "geo_basics_basic_angle_terminology": "angle_rays",
    "geo_basics_angles_and_their_measures": "angle_rays",
    "pa_drawing_and_measuring_angles": "angle_rays",
    "geo_basics_angle_addition_postulate": "adjacent_angles",
    "geo_basics_angle_relationships": "complementary_angles",
    "pa_angle_relationships": "complementary_angles",
    "geo_parallel_parallel_lines_and_transversals": "parallel_transversal",
    "geo_basics_segment_addition_postulate": "number_line",
    "geo_basics_line_segments_and_their_measures": "number_line",
    "finding_angles": "angle_rays",
    # Triangles / quads
    "g6_triangles": "triangle_area",
    "g6_triangles_understanding_area_formula": "triangle_area",
    "pa_plane_figures_triangles": "triangle_area",
    "g6_parallelograms": "parallelogram",
    "g6_parallelograms_understanding_area_formula": "parallelogram",
    "g6_trapezoids": "trapezoid",
    "geo_right_pythagorean_theorem": "right_triangle",
    "pythagorean_theorem": "right_triangle",
    "geo_congruent_classifying_triangles": "triangle_angles",
    "geo_congruent_triangle_angle_sum": "triangle_angles",
    "geo_triangle_midsegment": "triangle_angles",
    # Circles
    "pa_circles": "circle_radius",
    "geo_circles_circumference_and_area": "circle_radius",
    "geo_circles_arc_length_and_sector_area": "circle_sector",
    "a2_trigonometry_arc_length_and_sector_area": "circle_sector",
    # Number line / plane
    "g6_numbers_on_a_number_line": "number_line",
    "g6_number_line_word_problems": "number_line",
    "graph_single_variable_inequality": "number_line",
    "g6_points_on_the_coordinate_plane": "coordinate_plane",
    "pa_plotting_points": "coordinate_plane",
    "g6_distances_on_the_coordinate_plane": "coordinate_plane",
    # G6 visuals
    "g6_introduction_to_percents": "percent_shade",
    "g6_distributive_property_area_diagrams_algebraic": "area_model",
    "g6_distributive_property_area_diagrams_numeric": "area_model",
    "g6_equations_tape_diagrams": "tape_diagram",
    "g6_equations_hanger_diagrams": "tape_diagram",
    # Previously deferred “with diagrams” topics — now family-wired
    "g6_decimal_addition_with_diagrams": "decimal_grid",
    "g6_decimal_subtraction_with_diagrams": "decimal_grid",
    "g6_decimal_multiplication_with_area_diagrams": "area_model",
    "g6_solving_percent_problems_with_diagrams": "percent_shade",
    # Stats charts
    "g6_interpreting_box_plots": "box_plot",
    "g6_drawing_box_plots": "box_plot",
    "center_and_spread": "box_plot",
    "g6_data_center_and_spread": "box_plot",
    # Calc — function sketches attached by generators
    "calc_app_diff_slope_tangent_and_normal_lines": "function_sketch",
    "calc_app_diff_related_rates": "function_sketch",
    "calc_def_int_approximating_area_under_a_curve": "function_sketch",
    "calc_app_int_area_under_a_curve": "function_sketch",
    "geo_basics_angle_addition_postulate": "adjacent_angles",
}


@dataclass
class FigureSample:
    """Sampled layout / complexity for a family (optionally with a built figure)."""

    family_id: str
    complexity: str
    params: dict[str, Any] = field(default_factory=dict)
    figure: Any | None = None  # GeometryFigure when built
    diagram_spec: dict[str, Any] = field(default_factory=dict)

    def to_metadata_extras(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "figure_family": self.family_id,
            "figure_complexity": self.complexity,
            "figure_params": dict(self.params),
        }
        svg = self.diagram_spec.get("diagram_svg")
        if svg:
            out["diagram_svg"] = svg
        return out


def family_for_type(type_id: str) -> FigureFamily | None:
    fid = TYPE_ID_FAMILY.get(type_id)
    if fid is None:
        return None
    return FIGURE_FAMILIES.get(fid)


def complexity_for_difficulty(difficulty: float, *, tiers: tuple[str, ...] | None = None) -> str:
    """Map continuous D → complexity tier name."""
    names = tiers or ("simple", "standard", "complex")
    d = max(0.0, float(difficulty))
    if len(names) == 1:
        return names[0]
    if d < 5.0:
        return names[0]
    if d < 14.0:
        return names[min(1, len(names) - 1)]
    if d < 28.0 or len(names) < 4:
        return names[min(2, len(names) - 1)]
    return names[-1]


def _stable_int(*parts: Any) -> int:
    raw = "|".join(str(p) for p in parts).encode("utf-8")
    return int(hashlib.md5(raw).hexdigest()[:8], 16)


def figure_rng(
    settings: dict[str, Any] | None = None,
    *,
    family_id: str = "",
    seed: int | None = None,
    batch_index: int | None = None,
) -> random.Random:
    """Deterministic RNG from seed + batch index + family (falls back to global)."""
    settings = settings or {}
    if seed is None and settings.get("seed") is not None:
        try:
            seed = int(settings["seed"])
        except (TypeError, ValueError):
            seed = None
    if batch_index is None:
        batch_index = int(settings.get("_batch_index", 0) or 0)
    if seed is None:
        # Advance global RNG so successive calls still differ within a batch.
        return random.Random(random.getrandbits(32))
    return random.Random(_stable_int(seed, batch_index, family_id) + int(seed) + batch_index * 1009)


def _orientation_pool(complexity: str, rng: random.Random) -> float:
    """Degrees for rotating a figure; wider set at higher complexity."""
    if complexity == "simple":
        pool = (0.0, 10.0, 15.0, 20.0)
    elif complexity == "standard":
        pool = (0.0, 15.0, 25.0, 35.0, 45.0, 60.0, 75.0, 90.0, 120.0, 150.0)
    else:
        pool = tuple(float(x) for x in range(0, 360, 15))
    return float(rng.choice(pool))


def _sample_angle_rays(complexity: str, rng: random.Random, **kwargs: Any) -> FigureSample:
    measure = kwargs.get("measure_deg")
    if measure is None:
        if complexity == "simple":
            measure = float(rng.choice([30, 45, 60, 90, 120]))
        elif complexity == "standard":
            measure = float(rng.randint(15, 165))
        else:
            measure = float(rng.randint(10, 170))
    base = _orientation_pool(complexity, rng)
    # Keep acute/obtuse framing readable: bias base so both rays stay on-screen.
    if measure <= 90 and base > 160:
        base = base % 90
    params = {
        "measure_deg": float(measure),
        "base_deg": base,
        "show_measure": bool(kwargs.get("show_measure", True)),
    }
    return FigureSample(
        family_id="angle_rays",
        complexity=complexity,
        params=params,
        diagram_spec={"kind": "angle", **params},
    )


def _sample_adjacent(complexity: str, rng: random.Random, **kwargs: Any) -> FigureSample:
    """Multi-ray fan; piece count rises with complexity / continuous D."""
    if "piece_count" in kwargs:
        n = int(kwargs["piece_count"])
    elif complexity == "simple":
        n = 2
    elif complexity == "standard":
        n = int(rng.choice([2, 3, 3]))
    else:
        n = int(rng.choice([3, 4, 4, 5]))
    n = max(2, min(6, n))
    params = {
        "piece_count": n,
        "base_deg": _orientation_pool(complexity, rng) % 120,
        "reflect": complexity == "complex" and rng.random() < 0.4,
    }
    return FigureSample(
        family_id="adjacent_angles",
        complexity=complexity,
        params=params,
        diagram_spec={"kind": "adjacent_angles", **params},
    )


def _sample_complementary(complexity: str, rng: random.Random, **kwargs: Any) -> FigureSample:
    given = kwargs.get("given_deg")
    if given is None:
        lo, hi = (20, 45) if complexity == "simple" else (15, 75)
        given = float(rng.randint(lo, hi))
    unknown_first = complexity != "simple" and rng.random() < 0.45
    params = {
        "given_deg": float(given),
        "rotation_deg": _orientation_pool(complexity, rng) % 180,
        "unknown_on": "second" if not unknown_first else "first",
        "reflect": complexity == "complex" and rng.random() < 0.5,
    }
    return FigureSample(
        family_id="complementary_angles",
        complexity=complexity,
        params=params,
        diagram_spec={"kind": "complementary_angles", **params},
    )


def _sample_supplementary(complexity: str, rng: random.Random, **kwargs: Any) -> FigureSample:
    given = kwargs.get("given_deg")
    if given is None:
        lo, hi = (40, 80) if complexity == "simple" else (25, 155)
        given = float(rng.randint(lo, hi))
    params = {
        "given_deg": float(given),
        "rotation_deg": _orientation_pool(complexity, rng) % 180,
        "reflect": complexity != "simple" and rng.random() < 0.4,
    }
    return FigureSample(
        family_id="supplementary_angles",
        complexity=complexity,
        params=params,
        diagram_spec={"kind": "supplementary_angles", **params},
    )


def _sample_vertical(complexity: str, rng: random.Random, **kwargs: Any) -> FigureSample:
    given = kwargs.get("given_deg")
    if given is None:
        given = float(rng.randint(25, 155))
        if abs(given - 90) < 8:
            given = 70.0 if given < 90 else 110.0
    params = {
        "given_deg": float(given),
        "rotation_deg": _orientation_pool(complexity, rng) % 180,
    }
    return FigureSample(
        family_id="vertical_angles",
        complexity=complexity,
        params=params,
        diagram_spec={"kind": "vertical_angles", **params},
    )


def _sample_parallel(complexity: str, rng: random.Random, **kwargs: Any) -> FigureSample:
    angle = kwargs.get("angle_deg")
    if angle is None:
        if complexity == "simple":
            angle = float(rng.choice([40, 50, 55, 60, 120, 130]))
        else:
            angle = float(rng.randint(30, 150))
    relations = ("corresponding", "alternate interior", "same-side interior")
    if complexity == "simple":
        relations = ("corresponding",)
    elif complexity == "standard":
        relations = ("corresponding", "alternate interior")
    params = {
        "angle_deg": float(angle),
        "relation": kwargs.get("relation") or rng.choice(relations),
        "reflect": complexity == "complex" and rng.random() < 0.4,
    }
    return FigureSample(
        family_id="parallel_transversal",
        complexity=complexity,
        params=params,
        diagram_spec={"kind": "parallel_transversal", **params},
    )


def _sample_triangle_angles(complexity: str, rng: random.Random, **kwargs: Any) -> FigureSample:
    angles = kwargs.get("angles")
    if angles is None:
        a = rng.randint(30, 80)
        b = rng.randint(30, 80)
        c = 180 - a - b
        if c < 20:
            c = 30
            b = 180 - a - c
        angles = (float(a), float(b), float(c))
    params = {
        "angles": tuple(float(x) for x in angles),
        "rotation_deg": _orientation_pool(complexity, rng) % 180,
        "reflect": complexity != "simple" and rng.random() < 0.45,
    }
    return FigureSample(
        family_id="triangle_angles",
        complexity=complexity,
        params=params,
        diagram_spec={"kind": "triangle", **params},
    )


def _sample_right_triangle(complexity: str, rng: random.Random, **kwargs: Any) -> FigureSample:
    params = {
        "orientation_deg": _orientation_pool(complexity, rng) % 360,
        "reflect": complexity != "simple" and rng.random() < 0.5,
        "missing": kwargs.get("missing")
        or rng.choice(["leg_a", "leg_b", "hypotenuse"] if complexity != "simple" else ["hypotenuse"]),
    }
    return FigureSample(
        family_id="right_triangle",
        complexity=complexity,
        params=params,
        diagram_spec={"kind": "right_triangle", **params},
    )


def _sample_triangle_area(complexity: str, rng: random.Random, **kwargs: Any) -> FigureSample:
    if complexity == "simple":
        layout = "right"
    elif complexity == "standard":
        layout = rng.choices(("right", "interior", "exterior"), weights=(0.25, 0.5, 0.25), k=1)[0]
    else:
        layout = rng.choices(("right", "interior", "exterior"), weights=(0.1, 0.4, 0.5), k=1)[0]
    layout = kwargs.get("layout") or layout
    params = {
        "layout": layout,
        "orientation_deg": 0.0 if complexity == "simple" else _orientation_pool(complexity, rng) % 180,
        "reflect": complexity == "complex" and rng.random() < 0.4,
        "foot_fraction": None
        if layout != "interior"
        else (0.28 + rng.random() * 0.44),
    }
    return FigureSample(
        family_id="triangle_area",
        complexity=complexity,
        params=params,
        diagram_spec={"kind": "triangle_area", **params},
    )


def _sample_parallelogram(complexity: str, rng: random.Random, **kwargs: Any) -> FigureSample:
    if complexity == "simple":
        skew = 0.3
    elif complexity == "standard":
        skew = rng.uniform(0.2, 0.5)
    else:
        skew = rng.uniform(0.15, 0.65)
    if complexity != "simple" and rng.random() < 0.5:
        skew = -skew
    params = {
        "skew_ratio": float(kwargs.get("skew_ratio", skew)),
        "orientation_deg": 0.0 if complexity == "simple" else _orientation_pool(complexity, rng) % 90,
    }
    return FigureSample(
        family_id="parallelogram",
        complexity=complexity,
        params=params,
        diagram_spec={"kind": "parallelogram", **params},
    )


def _sample_circle_radius(complexity: str, rng: random.Random, **kwargs: Any) -> FigureSample:
    params = {
        "radius_angle_deg": _orientation_pool(complexity, rng),
        "show_diameter": complexity == "complex" and rng.random() < 0.35,
    }
    return FigureSample(
        family_id="circle_radius",
        complexity=complexity,
        params=params,
        diagram_spec={"kind": "circle", **params},
    )


def _sample_circle_sector(complexity: str, rng: random.Random, **kwargs: Any) -> FigureSample:
    central = kwargs.get("central_deg")
    if central is None:
        if complexity == "simple":
            central = float(rng.choice([60, 90, 120]))
        else:
            central = float(rng.randint(30, 300))
    params = {
        "central_deg": float(central),
        "start_angle_deg": _orientation_pool(complexity, rng),
    }
    return FigureSample(
        family_id="circle_sector",
        complexity=complexity,
        params=params,
        diagram_spec={"kind": "circle_sector", **params},
    )


def _sample_number_line(complexity: str, rng: random.Random, **kwargs: Any) -> FigureSample:
    if complexity == "simple":
        half = rng.choice([5, 8, 10])
        tick = 1.0
    elif complexity == "standard":
        half = rng.choice([8, 10, 12, 15])
        tick = float(rng.choice([1, 1, 2]))
    else:
        half = rng.choice([12, 15, 20, 25])
        tick = float(rng.choice([1, 2, 5]))
    params = {
        "number_line_min": float(kwargs.get("number_line_min", -half)),
        "number_line_max": float(kwargs.get("number_line_max", half)),
        "number_line_tick_interval": float(kwargs.get("number_line_tick_interval", tick)),
        "mark_style": rng.choice(["closed", "open", "ray"])
        if complexity != "simple"
        else "closed",
    }
    return FigureSample(
        family_id="number_line",
        complexity=complexity,
        params=params,
        diagram_spec={"kind": "number_line", **params},
    )


def _sample_coordinate_plane(complexity: str, rng: random.Random, **kwargs: Any) -> FigureSample:
    if complexity == "simple":
        bound = 5
    elif complexity == "standard":
        bound = rng.choice([6, 8, 10])
    else:
        bound = rng.choice([8, 10, 12, 15])
    params = {
        "x_min": -bound,
        "x_max": bound,
        "y_min": -bound,
        "y_max": bound,
        "show_grid": True,
        "object_budget": 1 if complexity == "simple" else (2 if complexity == "standard" else 3),
    }
    return FigureSample(
        family_id="coordinate_plane",
        complexity=complexity,
        params=params,
        diagram_spec={"kind": "coordinate_plane", **params},
    )


def _sample_percent_shade(complexity: str, rng: random.Random, **kwargs: Any) -> FigureSample:
    if complexity == "simple":
        figure = "hundred_grid"
        shade_pattern = "row"
    elif complexity == "standard":
        figure = rng.choice(["hundred_grid", "hundred_grid", "bar", "grid"])
        shade_pattern = rng.choice(["row", "col"])
    else:
        figure = rng.choice(["hundred_grid", "bar", "circle", "grid", "multi"])
        shade_pattern = rng.choice(["row", "col", "checker", "blocks"])
    params = {
        "figure": kwargs.get("figure") or figure,
        "shade_pattern": kwargs.get("shade_pattern") or shade_pattern,
        "start_angle_deg": float(rng.choice([0, 90, 180, 270]))
        if figure == "circle" or complexity == "complex"
        else -90.0,
    }
    return FigureSample(
        family_id="percent_shade",
        complexity=complexity,
        params=params,
        diagram_spec={"kind": "percent_shade", **params},
    )


def _sample_area_model(complexity: str, rng: random.Random, **kwargs: Any) -> FigureSample:
    params = {
        "split": kwargs.get("split")
        or ("vertical" if complexity == "simple" else rng.choice(["vertical", "horizontal"])),
        "orientation": "standard"
        if complexity != "complex"
        else rng.choice(["standard", "flipped"]),
    }
    return FigureSample(
        family_id="area_model",
        complexity=complexity,
        params=params,
        diagram_spec={"kind": "area_model", **params},
    )


def _sample_tape(complexity: str, rng: random.Random, **kwargs: Any) -> FigureSample:
    n = 3 if complexity == "simple" else (rng.randint(3, 5) if complexity == "standard" else rng.randint(4, 7))
    params = {
        "parts": int(kwargs.get("parts", n)),
        "unequal": complexity == "complex" and rng.random() < 0.55,
    }
    return FigureSample(
        family_id="tape_diagram",
        complexity=complexity,
        params=params,
        diagram_spec={"kind": "tape_diagram", **params},
    )


def _function_sketch_svg(params: dict[str, Any], rng: random.Random) -> str:
    """Calc-style axes + curve (+ optional tangent / shade / asymptote / Riemann)."""
    features = list(params.get("features") or ["curve"])
    window = params.get("window") or (-3, 3)
    x0, x1 = float(window[0]), float(window[1])
    w, h = 360, 220
    pad = 28
    mid_x = w / 2
    x_span = max(x1 - x0, 1e-6)
    y_span = x_span
    y0, y1 = -y_span / 2, y_span / 2
    mid_y = h - pad - (0.0 - y0) / y_span * (h - 2 * pad)

    def sx(x: float) -> float:
        return pad + (x - x0) / x_span * (w - 2 * pad)

    def sy(y: float) -> float:
        return h - pad - (y - y0) / y_span * (h - 2 * pad)

    curve_kind = str(params.get("curve_kind") or "parabola")
    a = float(params.get("a", 0.35))
    b = float(params.get("b", 0.0))
    c = float(params.get("c", 0.0))

    def f(x: float) -> float:
        if curve_kind == "cubic":
            return a * x * x * x + b * x + c
        if curve_kind == "sine":
            return a * 2.2 * math.sin(b * x + c) if abs(b) > 1e-6 else a * 2.2 * math.sin(x) + c
        if curve_kind == "exp":
            return a * math.exp(0.35 * x) + b
        if curve_kind == "reciprocal":
            xx = x if abs(x) > 0.25 else (0.25 if x >= 0 else -0.25)
            return a * 2.0 / xx + b
        if curve_kind == "abs_linear":
            return a * abs(x) + b * x + c
        if curve_kind == "linear":
            return a * x + b
        return a * x * x + b * x + c

    n_samp = 64 if curve_kind in {"exp", "reciprocal", "sine"} else 48
    xs = [x0 + i * (x1 - x0) / n_samp for i in range(n_samp + 1)]
    if curve_kind == "reciprocal":
        # Skip the asymptote neighborhood so the path does not jump.
        xs = [x for x in xs if abs(x) > 0.22]
    pts = [(sx(x), sy(f(x))) for x in xs]
    pts = [(px, max(pad, min(h - pad, py))) for px, py in pts]
    path = "M " + " L ".join(f"{px:.1f},{py:.1f}" for px, py in pts)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
        f'<rect width="{w}" height="{h}" fill="#fafafa"/>',
        f'<line x1="{pad}" y1="{mid_y}" x2="{w - pad}" y2="{mid_y}" stroke="#64748b" stroke-width="1.5"/>',
        f'<line x1="{mid_x}" y1="{pad}" x2="{mid_x}" y2="{h - pad}" stroke="#64748b" stroke-width="1.5"/>',
    ]
    if "asymptote" in features or curve_kind == "reciprocal":
        parts.append(
            f'<line x1="{sx(0):.1f}" y1="{pad}" x2="{sx(0):.1f}" y2="{h - pad}" '
            f'stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="5 4"/>'
        )
    if "shaded_area" in features or "riemann" in features:
        xa = float(params.get("shade_a", x0 + 0.2 * x_span))
        xb = float(params.get("shade_b", x0 + 0.7 * x_span))
        if "riemann" in features:
            n_rect = int(params.get("riemann_n", 4))
            n_rect = max(2, min(8, n_rect))
            dx = (xb - xa) / n_rect
            for i in range(n_rect):
                xl = xa + i * dx
                xr = xl + dx
                mid = (xl + xr) / 2
                yh = max(0.0, f(mid))
                parts.append(
                    f'<rect x="{sx(xl):.1f}" y="{sy(yh):.1f}" '
                    f'width="{max(1.0, sx(xr) - sx(xl)):.1f}" height="{max(0.0, sy(0) - sy(yh)):.1f}" '
                    f'fill="#93c5fd" fill-opacity="0.4" stroke="#1d4ed8" stroke-width="0.8"/>'
                )
        else:
            shade_xs = [xa + i * (xb - xa) / 20 for i in range(21)]
            shade_pts = [(sx(x), sy(f(x))) for x in shade_xs]
            poly = (
                f"{sx(xa):.1f},{sy(0):.1f} "
                + " ".join(f"{px:.1f},{py:.1f}" for px, py in shade_pts)
                + f" {sx(xb):.1f},{sy(0):.1f}"
            )
            parts.append(
                f'<polygon points="{poly}" fill="#93c5fd" fill-opacity="0.45" stroke="none"/>'
            )
    parts.append(f'<path d="{path}" fill="none" stroke="#1d4ed8" stroke-width="2.2"/>')

    if any(feat in features for feat in ("tangent", "secant", "normal", "point")):
        tx = float(params.get("touch_x", rng.uniform(x0 + 0.4, x1 - 0.4)))
        if curve_kind == "reciprocal" and abs(tx) < 0.3:
            tx = 0.8 if tx >= 0 else -0.8
        ty = f(tx)
        eps = 0.05
        m = (f(tx + eps) - f(tx - eps)) / (2 * eps)
        if "tangent" in features or "secant" in features:
            dx = 1.2
            parts.append(
                f'<line x1="{sx(tx - dx):.1f}" y1="{sy(ty - m * dx):.1f}" '
                f'x2="{sx(tx + dx):.1f}" y2="{sy(ty + m * dx):.1f}" '
                f'stroke="#dc2626" stroke-width="1.8"/>'
            )
        if "normal" in features and abs(m) > 1e-6:
            mn = -1.0 / m
            dx = 0.9
            parts.append(
                f'<line x1="{sx(tx - dx):.1f}" y1="{sy(ty - mn * dx):.1f}" '
                f'x2="{sx(tx + dx):.1f}" y2="{sy(ty + mn * dx):.1f}" '
                f'stroke="#16a34a" stroke-width="1.6" stroke-dasharray="4 3"/>'
            )
        if "point" in features or "tangent" in features or "normal" in features:
            parts.append(
                f'<circle cx="{sx(tx):.1f}" cy="{sy(ty):.1f}" r="3.5" fill="#0f172a"/>'
            )
            if "label_point" in features:
                parts.append(
                    f'<text x="{sx(tx) + 6:.1f}" y="{sy(ty) - 6:.1f}" font-size="11" '
                    f'fill="#0f172a">P</text>'
                )
    if "related_rates_ladder" in features:
        lx0, ly0 = sx(x0 + 0.3 * x_span), sy(0)
        lx1, ly1 = sx(x0 + 0.75 * x_span), sy(y_span * 0.35)
        parts.append(
            f'<line x1="{lx0:.1f}" y1="{ly0:.1f}" x2="{lx1:.1f}" y2="{ly1:.1f}" '
            f'stroke="#7c3aed" stroke-width="2.2"/>'
        )
        parts.append(
            f'<line x1="{lx0:.1f}" y1="{ly0:.1f}" x2="{lx1:.1f}" y2="{ly0:.1f}" '
            f'stroke="#94a3b8" stroke-width="1.2" stroke-dasharray="3 2"/>'
        )
        # Expanding circle silhouette for radius-related rates
        if "related_rates_circle" in features:
            cr = 28 + 10 * rng.random()
            parts.append(
                f'<circle cx="{sx(0):.1f}" cy="{sy(0):.1f}" r="{cr:.1f}" '
                f'fill="none" stroke="#7c3aed" stroke-width="1.8" stroke-dasharray="4 3"/>'
            )
    parts.append("</svg>")
    return "".join(parts)


def _sample_function_sketch(complexity: str, rng: random.Random, **kwargs: Any) -> FigureSample:
    if "features" in kwargs:
        features = list(kwargs["features"])
    else:
        features = ["curve"]
        if complexity in {"standard", "complex", "related_rates"}:
            features.append(rng.choice(["tangent", "secant", "point", "label_point"]))
        if complexity in {"complex", "related_rates"}:
            features.append(
                rng.choice(
                    ["shaded_area", "normal", "related_rates_ladder", "riemann", "asymptote"]
                )
            )
        if complexity == "related_rates":
            features.append(rng.choice(["related_rates_ladder", "related_rates_circle"]))
    if "curve_kind" in kwargs:
        curve_kind = str(kwargs["curve_kind"])
    elif complexity == "simple":
        curve_kind = "parabola"
    elif complexity == "standard":
        curve_kind = rng.choice(["parabola", "cubic", "sine", "abs_linear"])
    else:
        curve_kind = rng.choice(
            ["parabola", "cubic", "sine", "exp", "reciprocal", "abs_linear"]
        )
    params = {
        "features": features,
        "curve_kind": curve_kind,
        "a": float(kwargs.get("a", round(rng.uniform(0.15, 0.55) * rng.choice([-1, 1]), 3))),
        "b": float(kwargs.get("b", round(rng.uniform(-0.4, 0.4), 3))),
        "c": float(kwargs.get("c", round(rng.uniform(-0.5, 0.5), 3))),
        "touch_x": float(kwargs.get("touch_x", round(rng.uniform(-1.5, 1.5), 3))),
        "window": kwargs.get("window")
        or (
            rng.choice([(-3, 3), (-5, 5), (-2, 6), (-4, 4)])
            if complexity != "simple"
            else (-3, 3)
        ),
        "riemann_n": int(kwargs.get("riemann_n", rng.choice([3, 4, 5, 6]))),
        "shade_a": kwargs.get("shade_a"),
        "shade_b": kwargs.get("shade_b"),
    }
    params = {k: v for k, v in params.items() if v is not None}
    svg = _function_sketch_svg(params, rng)
    return FigureSample(
        family_id="function_sketch",
        complexity=complexity,
        params=params,
        diagram_spec={"kind": "function_sketch", "diagram_svg": svg, **params},
    )


def _sample_decimal_grid(complexity: str, rng: random.Random, **kwargs: Any) -> FigureSample:
    if complexity == "simple":
        style = "place_value"
        places = 1
    elif complexity == "standard":
        style = rng.choice(["place_value", "place_value", "hundredths"])
        places = rng.choice([1, 2])
    else:
        style = rng.choice(["place_value", "hundredths", "hundredths"])
        places = rng.choice([2, 3])
    params = {
        "style": kwargs.get("style") or style,
        "places": int(kwargs.get("places", places)),
        "shade_pattern": kwargs.get("shade_pattern")
        or rng.choice(["row", "col", "blocks"]),
        "op": kwargs.get("op") or "+",
    }
    return FigureSample(
        family_id="decimal_grid",
        complexity=complexity,
        params=params,
        diagram_spec={"kind": "decimal_grid", **params},
    )


def _sample_box_plot(complexity: str, rng: random.Random, **kwargs: Any) -> FigureSample:
    params = {
        "show_outliers": complexity == "complex" and rng.random() < 0.45,
        "orientation": "horizontal"
        if complexity == "simple"
        else rng.choice(["horizontal", "horizontal", "vertical"]),
        "label_fences": complexity != "simple",
    }
    return FigureSample(
        family_id="box_plot",
        complexity=complexity,
        params=params,
        diagram_spec={"kind": "box_plot", **params},
    )


_SAMPLERS: dict[str, Callable[..., FigureSample]] = {
    "angle_rays": _sample_angle_rays,
    "adjacent_angles": _sample_adjacent,
    "complementary_angles": _sample_complementary,
    "supplementary_angles": _sample_supplementary,
    "vertical_angles": _sample_vertical,
    "parallel_transversal": _sample_parallel,
    "triangle_angles": _sample_triangle_angles,
    "right_triangle": _sample_right_triangle,
    "triangle_area": _sample_triangle_area,
    "parallelogram": _sample_parallelogram,
    "trapezoid": _sample_parallelogram,
    "circle_radius": _sample_circle_radius,
    "circle_sector": _sample_circle_sector,
    "number_line": _sample_number_line,
    "coordinate_plane": _sample_coordinate_plane,
    "percent_shade": _sample_percent_shade,
    "area_model": _sample_area_model,
    "tape_diagram": _sample_tape,
    "function_sketch": _sample_function_sketch,
    "decimal_grid": _sample_decimal_grid,
    "box_plot": _sample_box_plot,
}


def sample_figure(
    family_id: str,
    difficulty: float = 6.0,
    *,
    rng: random.Random | None = None,
    seed: int | None = None,
    batch_index: int = 0,
    build: bool = False,
    settings: dict[str, Any] | None = None,
    **kwargs: Any,
) -> FigureSample:
    """Sample layout/complexity params for ``family_id``.

    When ``build=True``, attaches a ``GeometryFigure`` for families that have a
    direct builder mapping (angles, triangles, circles, …).
    """
    family = FIGURE_FAMILIES.get(family_id)
    if family is None:
        raise KeyError(f"Unknown figure family: {family_id}")
    if settings is not None and ("difficulty" in settings or "difficulty_tier" in settings):
        difficulty = settings_difficulty(settings, default=float(difficulty))
    complexity = complexity_for_difficulty(difficulty, tiers=family.complexity_tiers)
    use_rng = rng or figure_rng(
        settings, family_id=family_id, seed=seed, batch_index=batch_index
    )
    sampler = _SAMPLERS.get(family_id)
    if sampler is None:
        sample = FigureSample(family_id=family_id, complexity=complexity, params={})
    else:
        sample = sampler(complexity, use_rng, **kwargs)

    if build:
        sample.figure = _build_figure(family_id, sample, use_rng, **kwargs)
        if sample.figure is not None:
            sample.diagram_spec = {
                **sample.diagram_spec,
                **(sample.figure.to_diagram_spec() if hasattr(sample.figure, "to_diagram_spec") else {}),
            }
    return sample


def sample_figure_from_settings(
    family_id: str,
    settings: dict[str, Any],
    *,
    build: bool = False,
    **kwargs: Any,
) -> FigureSample:
    """Convenience: difficulty / seed / batch index from worksheet settings."""
    return sample_figure(
        family_id,
        settings_difficulty(settings, default=6.0),
        settings=settings,
        build=build,
        **kwargs,
    )


def _build_figure(
    family_id: str,
    sample: FigureSample,
    rng: random.Random,
    **kwargs: Any,
) -> Any | None:
    """Optionally construct a GeometryFigure from sampled params."""
    from .builders import (
        angle_figure,
        circle_figure,
        complementary_angles_figure,
        parallel_lines_transversal_figure,
        parallelogram_figure,
        right_triangle_figure,
        supplementary_angles_figure,
        triangle_figure,
        vertical_angles_figure,
    )

    p = sample.params
    labels3 = kwargs.get("labels") or ("A", "B", "C")
    if family_id == "angle_rays":
        labs = kwargs.get("labels") or tuple(rng.sample(list("ABCDEFGH"), 3))
        return angle_figure(
            labs[0],
            labs[1],
            labs[2],
            float(p["measure_deg"]),
            show_measure=bool(p.get("show_measure", True)),
            base_deg=float(p.get("base_deg", 15.0)),
        )
    if family_id == "complementary_angles":
        return complementary_angles_figure(
            float(p["given_deg"]),
            rotation_deg=float(p.get("rotation_deg", 0.0)),
            reflect=bool(p.get("reflect", False)),
            unknown_on=str(p.get("unknown_on", "second")),
        )
    if family_id == "supplementary_angles":
        return supplementary_angles_figure(
            float(p["given_deg"]),
            rotation_deg=float(p.get("rotation_deg", 0.0)),
            reflect=bool(p.get("reflect", False)),
        )
    if family_id == "vertical_angles":
        return vertical_angles_figure(
            float(p["given_deg"]),
            rotation_deg=float(p.get("rotation_deg", 0.0)),
        )
    if family_id == "parallel_transversal":
        return parallel_lines_transversal_figure(
            float(p["angle_deg"]),
            relation=str(p.get("relation", "corresponding")),
            reflect=bool(p.get("reflect", False)),
        )
    if family_id == "triangle_angles":
        return triangle_figure(
            labels3,
            p["angles"],
            rotation_deg=float(p.get("rotation_deg", 0.0)),
            reflect=bool(p.get("reflect", False)),
        )
    if family_id == "right_triangle":
        a = float(kwargs.get("leg_a", 3))
        b = float(kwargs.get("leg_b", 4))
        return right_triangle_figure(
            a,
            b,
            labels=labels3,
            orientation_deg=float(p.get("orientation_deg", 0.0)),
            reflect=bool(p.get("reflect", False)),
        )
    if family_id == "circle_radius":
        r = float(kwargs.get("radius", 5))
        return circle_figure(
            r,
            radius_angle_deg=float(p.get("radius_angle_deg", 0.0)),
            show_diameter=bool(p.get("show_diameter", False)),
        )
    if family_id == "parallelogram":
        return parallelogram_figure(
            float(kwargs.get("base", 6)),
            float(kwargs.get("height", 4)),
            skew_ratio=float(p.get("skew_ratio", 0.35)),
        )
    return None


def apply_batch_seed(settings: dict[str, Any], batch_index: int) -> None:
    """Reseed global ``random`` for worksheet item ``batch_index`` when seed set.

    Mutates ``settings`` with ``_batch_index``. Call once per item in a batch so
    figure params and numeric content both diversify under a fixed worksheet seed.
    """
    settings["_batch_index"] = int(batch_index)
    raw = settings.get("seed")
    if raw is None:
        return
    try:
        seed = int(raw)
    except (TypeError, ValueError):
        return
    random.seed(seed + int(batch_index) * 1009)
