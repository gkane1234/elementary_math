"""Graphing framework — coordinate plane, slope, and intercept metadata.

Unlocks the Graphing & linear catalog family (29 types). Tier 1
``writing_linear_equations`` already exists; this module standardizes metadata
for slope-from-points, intercept identification, and inequality shading on the
coordinate plane.

Tier 2 plan
-----------
- Sample two points or slope-intercept form from settings
- Populate ``CoordinatePlaneSpec`` in question metadata
- Client renderers read ``graph_spec`` (see ``core.metadata.GraphSpec``)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

from .base import QuestionFramework
from ..core.metadata import GraphSpec, question_metadata

Quadrant = Literal["I", "II", "III", "IV", "all"]


@dataclass
class CoordinatePlaneSpec:
    """Coordinate-plane prompt metadata (points, slope, intercept)."""

    points: list[tuple[float, float]] = field(default_factory=list)
    slope: float | None = None
    y_intercept: float | None = None
    x_intercept: float | None = None
    show_grid: bool = True
    quadrant: Quadrant = "all"

    def to_graph_spec(self) -> GraphSpec:
        xs = [p[0] for p in self.points]
        ys = [p[1] for p in self.points]
        padding = 2
        x_min = min(xs, default=-10) - padding
        x_max = max(xs, default=10) + padding
        y_min = min(ys, default=-10) - padding
        y_max = max(ys, default=10) + padding
        functions: list[str] = []
        if self.slope is not None and self.y_intercept is not None:
            functions.append(f"{self.slope}*x + {self.y_intercept}")
        return GraphSpec(
            x_min=x_min,
            x_max=x_max,
            y_min=y_min,
            y_max=y_max,
            functions=functions,
            points=self.points,
        )


class GraphingFramework(QuestionFramework):
    """Shared batch generation for coordinate-graphing types.

  Settings (framework-level keys, domain schema TBD):
  - ``show_grid`` — include grid lines in ``graph_spec`` metadata
  - ``quadrant`` — restrict point sampling to a single quadrant or ``all``
  """

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        spec = CoordinatePlaneSpec(
            show_grid=bool(settings.get("show_grid", True)),
            quadrant=settings.get("quadrant", "all"),  # type: ignore[arg-type]
        )
        return question_metadata(
            coordinate_plane={
                "show_grid": spec.show_grid,
                "quadrant": spec.quadrant,
                "slope": spec.slope,
                "y_intercept": spec.y_intercept,
            },
            graph_spec=spec.to_graph_spec(),
        )

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        raise NotImplementedError(
            "GraphingFramework.build_prompt is a Tier 2 skeleton. "
            "Implement point/slope sampling and linear equation prompts."
        )
