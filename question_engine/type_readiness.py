"""Curriculum-picker readiness demotions beyond missing generators.

A catalog type can be wired to a generator and still must not show as Ready when:

- it needs a figure the UI does not render yet (see ``diagram_readiness``), or
- the wired generator implements the wrong skill for the curriculum topic.

The question-types API exposes ``requires_diagram``, ``incorrect_implementation``,
and umbrella ``not_ready``. The curriculum picker treats ``not_ready`` types as
**Coming soon** (not selectable) even when a generator exists.

Re-enable later
---------------
1. Fix the underlying gap (render the figure, or replace the generator).
2. Remove the type id from the matching denylist below / in ``diagram_readiness``.
3. Confirm the picker shows Ready and a sample worksheet matches the topic.
"""

from __future__ import annotations

from .diagram_readiness import REQUIRES_DIAGRAM_TYPE_IDS, type_requires_diagram

# Generators exist but do not match the curriculum topic (wrong skill / stand-in).
INCORRECT_IMPLEMENTATION_TYPE_IDS: frozenset[str] = frozenset(
    {
        # Grade 6 — should be word problems that write numeric expressions;
        # currently mapped to g6_integer_add_subtract.
        "g6_writing_numeric_expressions",
    }
)


def type_incorrect_implementation(type_id: str) -> bool:
    return type_id in INCORRECT_IMPLEMENTATION_TYPE_IDS


def type_not_ready(type_id: str) -> bool:
    """True when the curriculum picker must not treat this type as Ready."""
    return type_requires_diagram(type_id) or type_incorrect_implementation(type_id)


__all__ = [
    "INCORRECT_IMPLEMENTATION_TYPE_IDS",
    "REQUIRES_DIAGRAM_TYPE_IDS",
    "type_incorrect_implementation",
    "type_not_ready",
    "type_requires_diagram",
]
