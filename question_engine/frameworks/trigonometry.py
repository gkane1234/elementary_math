"""Trigonometry framework — right-triangle ratio and solve prompts.

Unlocks the Trigonometry catalog family (38 types). Tier 2 focuses on
right-triangle ratio tables (sin/cos/tan) and missing-side/angle solves using
``RightTriangleSpec`` metadata for diagram renderers.

Tier 2 plan
-----------
1. Sample leg lengths and reference angle from settings
2. Attach ``right_triangle_spec`` + ``diagram_spec`` to metadata
3. Prompt for a ratio, side length, or angle measure
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from .base import QuestionFramework
from ..core.metadata import DiagramSpec, question_metadata

RatioTarget = Literal["sin", "cos", "tan", "any"]


@dataclass
class RightTriangleSpec:
    """Right triangle with labeled legs and reference angle."""

    leg_a: float
    leg_b: float
    angle_deg: float
    right_angle_vertex: str = "C"
    ratio_target: RatioTarget = "any"

    def to_diagram_spec(self) -> DiagramSpec:
        return DiagramSpec(
            kind="right_triangle",
            labels=["A", "B", self.right_angle_vertex],
            segments=[("A", "B"), ("B", self.right_angle_vertex), (self.right_angle_vertex, "A")],
            angles=[self.angle_deg, 90.0],
        )


class TrigFramework(QuestionFramework):
    """Shared batch generation for right-triangle trigonometry types."""

    ratio_target: RatioTarget = "any"

    def __init__(self, ratio_target: RatioTarget = "any"):
        self.ratio_target = ratio_target

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        tri = RightTriangleSpec(leg_a=3.0, leg_b=4.0, angle_deg=37.0, ratio_target=self.ratio_target)
        return question_metadata(
            right_triangle_spec={
                "leg_a": tri.leg_a,
                "leg_b": tri.leg_b,
                "angle_deg": tri.angle_deg,
                "ratio_target": tri.ratio_target,
            },
            diagram_spec=tri.to_diagram_spec(),
        )

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        raise NotImplementedError(
            "TrigFramework.build_prompt is a Tier 2 skeleton. "
            "Implement right-triangle ratio and solve prompts."
        )
