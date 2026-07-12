"""Typed metadata contracts for Question.metadata."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, TypedDict


class ScaffoldMetadata(TypedDict, total=False):
    scaffolded: bool


class GenerationSettingsMetadata(TypedDict, total=False):
    generation_settings: dict[str, Any]
    instruction_latex: str


class GraphRegion(TypedDict, total=False):
    """Shaded region on a coordinate plane (linear half-planes for inequalities)."""

    kind: str  # "half_plane"
    m: float
    b: float
    op: str  # ">", ">=", "<", "<="


class GraphSpec(TypedDict, total=False):
    """Minimal coordinate-plane spec for client-side graph renderers."""

    x_min: float
    x_max: float
    y_min: float
    y_max: float
    functions: list[str]
    points: list[tuple[float, float]]
    show_grid: bool
    show_points: bool
    regions: list[GraphRegion]


class NumberLineSpecDict(TypedDict, total=False):
    """Number-line shading metadata for inequality solutions."""

    min_value: float
    max_value: float
    boundary: float
    boundary_high: float
    direction: str
    inclusive: bool
    tick_interval: float
    show_zero: bool
    blank: bool


class DiagramSpec(TypedDict, total=False):
    """Geometry figure summary; pair with ``diagram_svg`` / ``diagram_latex``.

    Generators should prefer ``GeometryFigure.to_metadata()`` from
    ``question_engine.diagrams``, which fills ``diagram_spec``,
    ``diagram_svg`` (web), and ``diagram_latex`` (TikZ export).
    """

    kind: str
    labels: list[str]
    segments: list[tuple[str, str]]
    angles: list[str | float]
    points: dict[str, dict[str, float | str | None]]


class MultipleChoiceChoice(TypedDict):
    """One shuffled multiple-choice option."""

    id: str
    latex: str
    correct: bool


class MultipleChoiceMetadata(TypedDict, total=False):
    """Multiple-choice presentation attached by enrichment or frameworks."""

    choices: list[MultipleChoiceChoice]
    answer_mode: str


@dataclass
class QuestionMetadata:
    """Documented optional metadata fields for hand-written generators."""

    scaffolded: bool = False
    generation_settings: dict[str, Any] = field(default_factory=dict)
    instruction_latex: str | None = None
    graph_spec: GraphSpec | None = None
    answer_graph_spec: GraphSpec | None = None
    number_line_spec: NumberLineSpecDict | None = None
    answer_number_line_spec: NumberLineSpecDict | None = None
    graph_role: str | None = None
    diagram_spec: DiagramSpec | None = None
    diagram_svg: str | None = None
    diagram_latex: str | None = None
    choices: list[MultipleChoiceChoice] | None = None
    answer_mode: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {}
        if self.scaffolded:
            data["scaffolded"] = True
        if self.generation_settings:
            data["generation_settings"] = self.generation_settings
        if self.instruction_latex is not None:
            data["instruction_latex"] = self.instruction_latex
        if self.graph_spec is not None:
            data["graph_spec"] = self.graph_spec
        if self.answer_graph_spec is not None:
            data["answer_graph_spec"] = self.answer_graph_spec
        if self.number_line_spec is not None:
            data["number_line_spec"] = self.number_line_spec
        if self.answer_number_line_spec is not None:
            data["answer_number_line_spec"] = self.answer_number_line_spec
        if self.graph_role is not None:
            data["graph_role"] = self.graph_role
        if self.diagram_spec is not None:
            data["diagram_spec"] = self.diagram_spec
        if self.diagram_svg is not None:
            data["diagram_svg"] = self.diagram_svg
        if self.diagram_latex is not None:
            data["diagram_latex"] = self.diagram_latex
        if self.choices is not None:
            data["choices"] = self.choices
        if self.answer_mode is not None:
            data["answer_mode"] = self.answer_mode
        data.update(self.extra)
        return data


def question_metadata(**kwargs: Any) -> dict[str, Any]:
    """Build a metadata dict with consistent, documented keys."""
    return {key: value for key, value in kwargs.items() if value is not None}


def scaffold_metadata() -> dict[str, bool]:
    return question_metadata(scaffolded=True)
