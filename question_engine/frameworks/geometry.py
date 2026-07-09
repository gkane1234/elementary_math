"""Geometry figure framework — area, volume, and measurement prompts.

64 geometry measurement types (catalog family) depend on ``GeometryFigureSpec``
to describe labeled figures before prompt generation. Tier 2 types reuse formula
templates (rectangle area, cylinder volume); Tier 3 types need diagram renderers
fed by ``diagram_spec`` metadata.

Tier 2 plan
-----------
1. Sample dimensions from settings bounds
2. Emit ``GeometryFigureSpec`` + optional ``diagram_spec`` in metadata
3. Build LaTeX prompt from figure type + measured quantity requested
4. Wire catalog ``geo_*`` entries through ``GeometryFramework`` subclasses
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

from .base import QuestionFramework
from ..core.metadata import DiagramSpec, question_metadata

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


def geometry_figure_from_settings(settings: dict) -> GeometryFigureSpec:
    """Placeholder sampler — real generators will randomize dimensions."""
    return GeometryFigureSpec(
        figure_type=settings.get("figure_type", "rectangle"),  # type: ignore[arg-type]
        labels=["A", "B", "C", "D"],
        dimensions={"length": 8.0, "width": 5.0},
        unit=settings.get("units", "cm"),
    )


class GeometryFramework(QuestionFramework):
    """Shared batch generation for geometry measurement types.

  Settings (via ``geometry_settings()``):
  - ``include_diagram`` — attach ``diagram_spec`` / ``figure_spec`` to metadata

  Depends on the 64-type Geometry measurement catalog family; implement
  ``build_prompt`` per figure category (2D area, 3D volume, composite).
  """

    quantity: str = "area"

    def __init__(self, *, figure_type: FigureType = "rectangle", quantity: str = "area"):
        self.figure_type = figure_type
        self.quantity = quantity

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        figure = geometry_figure_from_settings({**settings, "figure_type": self.figure_type})
        meta: dict[str, Any] = {
            "figure_spec": {
                "figure_type": figure.figure_type,
                "labels": figure.labels,
                "dimensions": figure.dimensions,
                "unit": figure.unit,
            },
            "quantity": self.quantity,
        }
        if bool(settings.get("include_diagram", False)):
            meta["diagram_spec"] = figure.to_diagram_spec()
        return question_metadata(**meta)

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        raise NotImplementedError(
            "GeometryFramework.build_prompt is a skeleton. "
            f"Implement formula for {self.figure_type} {self.quantity}."
        )
