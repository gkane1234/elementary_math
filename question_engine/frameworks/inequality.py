"""Inequality generator framework — solving and graphing on number lines.

Tier 2 plan
-----------
Existing ``_inequality()`` in ``generators/basic.py`` covers 1–3 step symbolic
solving for five Tier 1 types. ``InequalityFramework`` will extend that pipeline
with optional ``number_line_spec`` / ``graph_spec`` metadata so client renderers
can shade solution sets. Compound and absolute-value variants will share the same
base class with step-count and symbol-family configuration.

Catalog families unlocked (44 total, ~30 Tier 2):
- Pre-Algebra / Algebra 1 one- through multi-step inequalities (done via basic.py)
- Grade 6 writing & graphing inequalities, number-line word problems
- Graphing linear / quadratic / absolute-value inequalities (metadata-first)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from .base import QuestionFramework
from ..core.metadata import GraphSpec, question_metadata

NumberLineDirection = Literal["left", "right", "both"]


@dataclass(frozen=True)
class NumberLineSpec:
    """Placeholder metadata for number-line inequality shading."""

    min_value: float
    max_value: float
    boundary: float
    direction: NumberLineDirection
    inclusive: bool = False
    tick_interval: float = 1.0


def number_line_spec_from_settings(settings: dict) -> NumberLineSpec | None:
    """Build a number-line spec when ``include_graph_metadata`` is enabled."""
    if not bool(settings.get("include_graph_metadata", False)):
        return None
    steps = int(settings.get("steps", 1))
    span = 12 + steps * 4
    return NumberLineSpec(
        min_value=-span,
        max_value=span,
        boundary=0.0,
        direction="both",
        inclusive=False,
    )


class InequalityFramework(QuestionFramework):
    """Shared batch generation for inequality-solving and graphing types.

  Settings (via ``inequality_settings()``):
  - ``steps`` — 1, 2, or 3 symbolic manipulation steps
  - ``include_graph_metadata`` — attach ``number_line_spec`` / ``graph_spec`` to metadata
  """

    steps: int = 1

    def __init__(self, steps: int = 1):
        self.steps = max(1, min(3, steps))

    def build_metadata(self, settings: dict) -> dict[str, Any]:
        meta: dict[str, Any] = {"steps": self.steps}
        if not bool(settings.get("include_graph_metadata", False)):
            return meta

        nls = number_line_spec_from_settings(settings)
        if nls is not None:
            meta["number_line_spec"] = {
                "min_value": nls.min_value,
                "max_value": nls.max_value,
                "boundary": nls.boundary,
                "direction": nls.direction,
                "inclusive": nls.inclusive,
                "tick_interval": nls.tick_interval,
            }

        graph: GraphSpec = {
            "x_min": nls.min_value if nls else -10,
            "x_max": nls.max_value if nls else 10,
            "y_min": -1,
            "y_max": 1,
            "functions": [],
            "points": [],
        }
        meta["graph_spec"] = graph
        return question_metadata(**meta)

    def build_prompt(self, settings: dict) -> tuple[str, str, str | None]:
        raise NotImplementedError(
            "InequalityFramework.build_prompt is a Tier 2 skeleton. "
            "Delegate to generators/basic._inequality or implement graph-aware prompts."
        )
