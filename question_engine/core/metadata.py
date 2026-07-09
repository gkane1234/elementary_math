"""Typed metadata contracts for Question.metadata."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, TypedDict


class ScaffoldMetadata(TypedDict, total=False):
    scaffolded: bool


class GenerationSettingsMetadata(TypedDict, total=False):
    generation_settings: dict[str, Any]
    instruction_latex: str


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


class NumberLineSpecDict(TypedDict, total=False):
    """Number-line shading metadata for inequality solutions."""

    min_value: float
    max_value: float
    boundary: float
    boundary_high: float
    direction: str
    inclusive: bool
    tick_interval: float


class DiagramSpec(TypedDict, total=False):
    """Minimal figure spec for future diagram renderers."""

    kind: str
    labels: list[str]
    segments: list[tuple[str, str]]
    angles: list[float]


class MultipleChoiceMetadata(TypedDict, total=False):
    choices: list[str]
    correct_index: int


@dataclass
class QuestionMetadata:
    """Documented optional metadata fields for hand-written generators."""

    scaffolded: bool = False
    generation_settings: dict[str, Any] = field(default_factory=dict)
    instruction_latex: str | None = None
    graph_spec: GraphSpec | None = None
    diagram_spec: DiagramSpec | None = None
    choices: list[str] | None = None
    correct_index: int | None = None
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
        if self.diagram_spec is not None:
            data["diagram_spec"] = self.diagram_spec
        if self.choices is not None:
            data["choices"] = self.choices
        if self.correct_index is not None:
            data["correct_index"] = self.correct_index
        data.update(self.extra)
        return data


def question_metadata(**kwargs: Any) -> dict[str, Any]:
    """Build a metadata dict with consistent, documented keys."""
    return {key: value for key, value in kwargs.items() if value is not None}


def scaffold_metadata() -> dict[str, bool]:
    return question_metadata(scaffolded=True)
