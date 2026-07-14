"""Trigonometry framework — right-triangle ratio and solve prompts with diagrams."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Any, Literal

from .base import QuestionFramework
from .geometry import (
    _diagram_enabled,
    _figure_metadata,
    _measurement_unit,
    _pythagorean_triple,
    _bounds,
)
from ..core.metadata import DiagramSpec
from ..diagrams import right_triangle_figure
from ..generators.utils import format_measurement_text, format_with_unit

RatioTarget = Literal["sin", "cos", "tan", "any"]


@dataclass
class RightTriangleSpec:
    """Right triangle with labeled legs and reference angle (metadata helper)."""

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


class RightTriangleTrigFramework(QuestionFramework):
    """Find sin/cos/tan ratios or missing sides/angles from a right triangle."""

    def __init__(self, mode: Literal["ratio", "angle", "side", "any"] = "any"):
        self.mode = mode
        self._last: dict[str, Any] = {}

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        unit = _measurement_unit(settings)
        _, side_max = _bounds(settings, "side_min", "side_max", 3, 20)
        a, b, c = _pythagorean_triple(side_max)
        labels = ["A", "B", "C"]  # C right angle; angle at A is reference
        # angle at A: opposite=BC=a? Layout: C right, B=(a,0), A=(0,b) → AB hypot
        # opposite to A is BC = a (horizontal leg), adjacent is AC = b
        opp, adj, hyp = a, b, c
        mode = self.mode
        if mode == "any":
            mode = random.choice(["ratio", "angle", "side"])

        side_labels = {
            "BC": format_measurement_text(opp, unit),
            "AC": format_measurement_text(adj, unit),
            "AB": format_measurement_text(hyp, unit),
        }
        angle_labels = {"A": "θ"}

        if mode == "ratio":
            fn = random.choice(["sin", "cos", "tan"])
            prompt = (
                f"\\text{{In right }} \\triangle ABC \\text{{ with right angle at }} C,"
                f"\\ \\text{{find }} \\{fn} A."
            )
            if fn == "sin":
                answer = f"\\frac{{{opp}}}{{{hyp}}}"
            elif fn == "cos":
                answer = f"\\frac{{{adj}}}{{{hyp}}}"
            else:
                answer = f"\\frac{{{opp}}}{{{adj}}}"
            text = f"{fn} A"
        elif mode == "angle":
            # Give two sides, ask for angle (leave as inverse trig expression)
            fn = random.choice(["sin", "cos", "tan"])
            if fn == "sin":
                prompt = (
                    f"\\text{{In right }} \\triangle ABC \\text{{ with right angle at }} C,"
                    f"\\ BC = {format_with_unit(opp, unit)},\\ AB = {format_with_unit(hyp, unit)}.\\ "
                    f"\\text{{Find }} m\\angle A."
                )
                answer = f"\\sin^{{-1}}\\left(\\frac{{{opp}}}{{{hyp}}}\\right)"
                side_labels = {
                    "BC": format_measurement_text(opp, unit),
                    "AB": format_measurement_text(hyp, unit),
                }
            elif fn == "cos":
                prompt = (
                    f"\\text{{In right }} \\triangle ABC \\text{{ with right angle at }} C,"
                    f"\\ AC = {format_with_unit(adj, unit)},\\ AB = {format_with_unit(hyp, unit)}.\\ "
                    f"\\text{{Find }} m\\angle A."
                )
                answer = f"\\cos^{{-1}}\\left(\\frac{{{adj}}}{{{hyp}}}\\right)"
                side_labels = {
                    "AC": format_measurement_text(adj, unit),
                    "AB": format_measurement_text(hyp, unit),
                }
            else:
                prompt = (
                    f"\\text{{In right }} \\triangle ABC \\text{{ with right angle at }} C,"
                    f"\\ BC = {format_with_unit(opp, unit)},\\ AC = {format_with_unit(adj, unit)}.\\ "
                    f"\\text{{Find }} m\\angle A."
                )
                answer = f"\\tan^{{-1}}\\left(\\frac{{{opp}}}{{{adj}}}\\right)"
                side_labels = {
                    "BC": format_measurement_text(opp, unit),
                    "AC": format_measurement_text(adj, unit),
                }
            text = "find angle A"
        else:
            # Missing side via trig with given angle (use nice acute angle label)
            angle = random.choice([30, 45, 60])
            find = random.choice(["opp", "adj", "hyp"])
            if find == "opp":
                prompt = (
                    f"\\text{{In right }} \\triangle ABC,\\ m\\angle A = {angle}^\\circ,"
                    f"\\ AC = {format_with_unit(adj, unit)}.\\ \\text{{Find }} BC."
                )
                answer = f"{adj}\\tan {angle}^\\circ"
                side_labels = {"AC": format_measurement_text(adj, unit), "BC": "?"}
            elif find == "adj":
                prompt = (
                    f"\\text{{In right }} \\triangle ABC,\\ m\\angle A = {angle}^\\circ,"
                    f"\\ BC = {format_with_unit(opp, unit)}.\\ \\text{{Find }} AC."
                )
                answer = f"\\frac{{{opp}}}{{\\tan {angle}^\\circ}}"
                side_labels = {"BC": format_measurement_text(opp, unit), "AC": "?"}
            else:
                prompt = (
                    f"\\text{{In right }} \\triangle ABC,\\ m\\angle A = {angle}^\\circ,"
                    f"\\ BC = {format_with_unit(opp, unit)}.\\ \\text{{Find }} AB."
                )
                answer = f"\\frac{{{opp}}}{{\\sin {angle}^\\circ}}"
                side_labels = {"BC": format_measurement_text(opp, unit), "AB": "?"}
            angle_labels = {"A": f"{angle}°"}
            text = "trig missing side"

        fig = right_triangle_figure(
            float(opp),
            float(adj),
            labels=("A", "B", "C"),
            right_angle_at="C",
            side_labels=side_labels,
            angle_labels=angle_labels,
            kind="right_triangle_trig",
        )
        self._last = {
            "figure": fig,
            "a": opp,
            "b": adj,
            "c": hyp,
        }
        return prompt, text, answer

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        return {}

    def build_question_metadata(
        self,
        settings: dict,
        *,
        prompt_latex: str,
        prompt_text: str,
        answer: str | None,
    ) -> dict[str, Any]:
        last = self._last
        if not last:
            return {}
        return _figure_metadata(
            settings,
            figure_type="triangle",
            labels=["A", "B", "C"],
            dimensions={
                "leg_a": float(last["a"]),
                "leg_b": float(last["b"]),
                "hypotenuse": float(last["c"]),
            },
            diagram=last.get("figure") if _diagram_enabled(settings) else None,
        )


# Back-compat alias for older imports
class TrigFramework(RightTriangleTrigFramework):
    def __init__(self, ratio_target: RatioTarget = "any"):
        mode: Literal["ratio", "angle", "side", "any"] = "ratio" if ratio_target != "any" else "any"
        super().__init__(mode=mode)
        self.ratio_target = ratio_target
