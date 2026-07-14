"""Geometry diagram DSL — compose figures, emit TikZ LaTeX and SVG.

Quick start
-----------
::

    from question_engine.diagrams import angle_figure, triangle_figure, circle_figure

    fig = angle_figure("A", "B", "C", 65, show_measure=True)
    meta = fig.to_metadata()  # diagram_spec, diagram_latex, diagram_svg

Attach ``meta`` to ``Question.metadata``. The web UI renders ``diagram_svg``;
export/print can use ``diagram_latex`` (TikZ).

See ``README.md`` in this package for adding shapes and wiring generators.
"""

from __future__ import annotations

from .builders import (
    adjacent_angles_figure,
    angle_figure,
    circle_figure,
    complementary_angles_figure,
    kite_figure,
    parallel_lines_transversal_figure,
    parallelogram_figure,
    polygon_figure,
    rectangle_figure,
    rhombus_figure,
    right_triangle_figure,
    segment_figure,
    similar_figures_pair_figure,
    starter_ray_figure,
    supplementary_angles_figure,
    trapezoid_figure,
    triangle_base_height_figure,
    triangle_figure,
    vertical_angles_figure,
)
from .charts import box_plot_svg, dot_plot_svg, histogram_svg
from .figure import GeometryFigure
from .primitives import (
    AngleMark,
    Arc,
    CirclePrim,
    Label,
    Line,
    Point,
    Polygon,
    Ray,
    RightAngleMark,
    Segment,
    ShadedRegion,
)

__all__ = [
    "GeometryFigure",
    "Point",
    "Segment",
    "Ray",
    "Line",
    "Polygon",
    "CirclePrim",
    "Arc",
    "AngleMark",
    "RightAngleMark",
    "Label",
    "ShadedRegion",
    "angle_figure",
    "adjacent_angles_figure",
    "starter_ray_figure",
    "complementary_angles_figure",
    "supplementary_angles_figure",
    "vertical_angles_figure",
    "triangle_figure",
    "circle_figure",
    "polygon_figure",
    "rectangle_figure",
    "segment_figure",
    "right_triangle_figure",
    "triangle_base_height_figure",
    "parallelogram_figure",
    "rhombus_figure",
    "trapezoid_figure",
    "kite_figure",
    "parallel_lines_transversal_figure",
    "similar_figures_pair_figure",
    "dot_plot_svg",
    "histogram_svg",
    "box_plot_svg",
]
