"""Load curated prerequisite maps and build prerequisite edges."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

PREREQ_DIR = Path(__file__).resolve().parent / "prerequisites"


def full_node_id(book: str, node_id: str) -> str:
    return f"{book}:{node_id}"


def split_full_node_id(full_id: str) -> tuple[str, str]:
    book, node_id = full_id.split(":", 1)
    return book, node_id


@dataclass
class PrereqEntry:
    requires: list[str]
    reason: str = ""


def load_prerequisite_map(book: str) -> dict[str, PrereqEntry]:
    path = PREREQ_DIR / f"{book}.json"
    if not path.is_file():
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    out: dict[str, PrereqEntry] = {}
    for key, val in raw.items():
        out[key] = PrereqEntry(
            requires=list(val.get("requires", [])),
            reason=str(val.get("reason", "")),
        )
    return out


def build_prerequisite_edges(
    maps: dict[str, dict[str, PrereqEntry]],
) -> tuple[list[tuple[str, str]], dict[str, str]]:
    """Return directed edges (prerequisite -> dependent) and reasons keyed by dependent."""
    edges: list[tuple[str, str]] = []
    reasons: dict[str, str] = {}
    seen_edges: set[tuple[str, str]] = set()

    for _book, book_map in maps.items():
        for dependent, entry in book_map.items():
            if entry.reason:
                reasons[dependent] = entry.reason
            for prereq in entry.requires:
                edge = (prereq, dependent)
                if edge not in seen_edges:
                    seen_edges.add(edge)
                    edges.append(edge)
    return edges, reasons


def validate_prerequisite_map(
    book: str,
    known_node_ids: set[str],
    book_map: dict[str, PrereqEntry],
    known_full_ids: set[str] | None = None,
) -> list[str]:
    """Return validation warnings for unknown node references.

    ``known_full_ids`` may include nodes from other books for cross-course edges.
    Dependents must still belong to ``book``.
    """
    warnings: list[str] = []
    book_full = {full_node_id(book, nid) for nid in known_node_ids}
    known_full = known_full_ids if known_full_ids is not None else book_full
    for dependent, entry in book_map.items():
        if dependent not in book_full:
            warnings.append(f"Unknown dependent: {dependent}")
        for prereq in entry.requires:
            if prereq not in known_full:
                warnings.append(f"{dependent} references unknown prerequisite: {prereq}")
    return warnings
