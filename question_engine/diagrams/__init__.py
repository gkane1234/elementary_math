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
    angle_figure,
    circle_figure,
    polygon_figure,
    rectangle_figure,
    triangle_figure,
)
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
    "triangle_figure",
    "circle_figure",
    "polygon_figure",
    "rectangle_figure",
]
