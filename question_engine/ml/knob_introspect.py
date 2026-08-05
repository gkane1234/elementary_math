"""Tiny helpers for continuous-difficulty / knob capability checks.

v1 of the live rating loop only needs ``has_continuous_difficulty``.
Full multi-knob introspection / BO registry is deferred to v2.
"""

from __future__ import annotations

from typing import Any

from question_engine.core.base import QUESTION_TYPES
from question_engine.generators import GENERATORS
from question_engine.type_readiness import type_not_ready

_NUMERIC_FIELD_TYPES = frozenset({"int", "float", "number", "range"})


def has_continuous_difficulty(type_id: str) -> bool:
    """True when the type's settings schema exposes a numeric ``difficulty`` field."""
    qt = QUESTION_TYPES.get(type_id)
    if qt is None:
        return False
    try:
        fields = qt.settings_schema()
    except Exception:  # noqa: BLE001 — treat schema failures as not continuous-D
        return False
    for field in fields:
        if getattr(field, "key", None) != "difficulty":
            continue
        if getattr(field, "type", None) in _NUMERIC_FIELD_TYPES:
            return True
    return False


def _generator_key(qt: Any) -> str | None:
    key = getattr(qt, "_generator_key", None)
    if key:
        return str(key)
    return None


def is_scaffold_type(type_id: str) -> bool:
    """True when the type is unwired / still on the scaffold generator."""
    qt = QUESTION_TYPES.get(type_id)
    if qt is None:
        return True
    key = _generator_key(qt)
    if key is None:
        return False
    return key == "scaffold" or key not in GENERATORS


def list_continuous_difficulty_types(
    *,
    ready_only: bool = True,
    include_scaffolds: bool = False,
) -> list[dict[str, Any]]:
    """List type_ids that accept continuous difficulty (pragmatic Ready filter)."""
    out: list[dict[str, Any]] = []
    for type_id, qt in sorted(QUESTION_TYPES.items(), key=lambda kv: kv[0]):
        if ready_only and type_not_ready(type_id):
            continue
        if not has_continuous_difficulty(type_id):
            continue
        scaffold = is_scaffold_type(type_id)
        if scaffold and not include_scaffolds:
            continue
        out.append(
            {
                "type_id": type_id,
                "name": getattr(qt, "name", type_id),
                "category": getattr(qt, "category", None),
                "subcategory": getattr(qt, "subcategory", None),
                "generator": _generator_key(qt),
                "has_continuous_difficulty": True,
                "scaffold": scaffold,
                "not_ready": type_not_ready(type_id),
            }
        )
    return out


__all__ = [
    "has_continuous_difficulty",
    "is_scaffold_type",
    "list_continuous_difficulty_types",
]
