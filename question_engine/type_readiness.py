"""Curriculum-picker readiness demotions beyond missing generators."""

from __future__ import annotations

from .diagram_readiness import REQUIRES_DIAGRAM_TYPE_IDS, type_requires_diagram

# Generators exist but do not match the curriculum topic (wrong skill / stand-in).
# Prefer REQUIRES_DIAGRAM_TYPE_IDS when the gap is a missing figure; use this set
# when a wired generator is the wrong skill entirely.
INCORRECT_IMPLEMENTATION_TYPE_IDS: frozenset[str] = frozenset(
    {
        # Wired to plain divisibility, not numeric area-model distributive.
        "g6_distributive_property_area_diagrams_numeric",
        # Product-disabled thin fraction-division word aliases (catalog/generators kept;
        # removed from curriculum.ts so they do not appear in the topics list).
        "g6_how_many_groups_times",
        "g6_what_fraction_of_a_whole",
        "g6_how_much_in_each_group_time",
        # Product-disabled (catalog/generators kept; removed from curriculum.ts).
        "g6_opposites_of_numbers",
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
