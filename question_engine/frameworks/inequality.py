"""Inequality generator framework — solving and graphing on number lines."""

from __future__ import annotations

from .base import QuestionFramework
from .graphing import (
    NumberLineSpec,
    include_graph_metadata,
    number_line_metadata,
    number_line_spec_from_settings,
)

__all__ = [
    "InequalityFramework",
    "NumberLineSpec",
    "number_line_spec_from_settings",
    "include_graph_metadata",
    "number_line_metadata",
]


class InequalityFramework(QuestionFramework):
    """Shared batch generation for inequality-solving and graphing types."""

    steps: int = 1

    def __init__(self, steps: int = 1):
        self.steps = max(1, min(3, steps))

    def build_metadata(self, settings: dict) -> dict:
        meta: dict = {"steps": self.steps}
        if not include_graph_metadata(settings):
            return meta
        nls = number_line_spec_from_settings(settings)
        if nls is not None:
            return number_line_metadata(None, settings) | meta
        return meta

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        raise NotImplementedError(
            "InequalityFramework.build_prompt is a Tier 2 skeleton. "
            "Delegate to generators/basic._inequality or implement graph-aware prompts."
        )
