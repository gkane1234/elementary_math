"""Register a catalog entry that uses a real generator from generators/basic.py."""

from __future__ import annotations

from ..core.base import register
from ..core.registry import get_catalog_entry
from ..core.scaffold import make_catalog_type


def register_from_catalog(type_id: str) -> None:
    entry = get_catalog_entry(type_id)
    if entry.generator == "scaffold":
        raise ValueError(
            f"{type_id} uses scaffold generator; register via register_catalog_types()"
        )
    register(make_catalog_type(entry))
