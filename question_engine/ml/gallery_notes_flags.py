"""Write gallery notes flag tokens from the live rater (not a fifth token).

Whole-word all-caps tokens that turn the phase-01 gallery red header on:

- ``UNCLEAR``
- ``LOW_VARIETY``
- ``LIMITATIONS``
- ``NOT_IMPLEMENTED``

Notes live at ``scripts/output/skeleton_phase01_gallery/notes/<type_id>.md``.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
NOTES_DIR = ROOT / "scripts" / "output" / "skeleton_phase01_gallery" / "notes"

FLAG_TOKENS: tuple[str, ...] = (
    "UNCLEAR",
    "LOW_VARIETY",
    "LIMITATIONS",
    "NOT_IMPLEMENTED",
)
FLAG_RE = re.compile(r"\b(UNCLEAR|LOW_VARIETY|LIMITATIONS|NOT_IMPLEMENTED)\b")
_TYPE_ID_RE = re.compile(r"^[A-Za-z0-9_]+$")
_GALLERY_FLAG_LINE_RE = re.compile(r"^Gallery UI flag:.*$", re.MULTILINE)
_GRAPH_GOLD_RE = re.compile(
    r"graph-match|gold is graph|no graph-match|no figure bank|"
    r"diagram missing|text-only graph",
    re.IGNORECASE,
)

ACTIONS = frozenset(
    {"too_unvaried", "low_variety", "varied_enough", "wrong_skill", "needs_figures"}
)


def notes_flags(md: str) -> list[str]:
    found: list[str] = []
    for match in FLAG_RE.finditer(md or ""):
        token = match.group(1)
        if token not in found:
            found.append(token)
    return found


def has_token(md: str, token: str) -> bool:
    if token not in FLAG_TOKENS:
        raise ValueError(f"unknown flag token: {token}")
    return bool(re.search(rf"\b{token}\b", md or ""))


def gold_is_graph_live_is_text(
    md: str,
    type_id: str,
    *,
    has_svg: bool = False,
) -> bool:
    """True when gold is graph-match / figures and live stems are text-only."""
    if has_svg:
        return False
    if _GRAPH_GOLD_RE.search(md or ""):
        return True
    low = (type_id or "").lower()
    return any(key in low for key in ("graph", "figure", "diagram", "sketch"))


def resolve_notes_path(type_id: str, *, create: bool = False) -> Path:
    """Prefer ``notes/<type_id>.md``; never write index / template files."""
    tid = _safe_type_id(type_id)
    preferred = NOTES_DIR / f"{tid}.md"
    if preferred.is_file():
        return preferred
    colocated = NOTES_DIR.parent / tid / "NOTES.md"
    if colocated.is_file():
        return colocated
    if create:
        NOTES_DIR.mkdir(parents=True, exist_ok=True)
        return preferred
    raise FileNotFoundError(f"no notes file for type_id={tid}")


def apply_notes_action(
    type_id: str,
    action: str,
    *,
    has_core: bool = True,
    has_svg: bool = False,
    create_if_missing: bool = True,
) -> dict[str, Any]:
    """Add/remove flag tokens in the leaf notes markdown.

    ``too_unvaried`` / ``low_variety`` → add ``LOW_VARIETY``.
    ``varied_enough`` → remove ``LOW_VARIETY`` only (keep ``LIMITATIONS``).
    ``wrong_skill`` → add ``UNCLEAR``; add ``NOT_IMPLEMENTED`` if no honest core.
    ``needs_figures`` → ensure ``LIMITATIONS``; add ``UNCLEAR`` if graph-match gold
    vs text live.
    """
    tid = _safe_type_id(type_id)
    act = str(action or "").strip().lower()
    if act not in ACTIONS:
        raise ValueError(f"unknown notes action: {action}")

    path = resolve_notes_path(tid, create=create_if_missing)
    created = False
    if not path.is_file():
        if not create_if_missing:
            raise FileNotFoundError(str(path))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(_minimal_notes(tid), encoding="utf-8")
        created = True

    before = path.read_text(encoding="utf-8")
    before_flags = notes_flags(before)
    md = before

    if act in {"too_unvaried", "low_variety"}:
        md = _ensure_token(
            md,
            "LOW_VARIETY",
            section_prefixes=("Variety notes",),
            reason="too unvaried (live rater)",
        )
    elif act == "varied_enough":
        md = _remove_token(md, "LOW_VARIETY")
    elif act == "wrong_skill":
        md = _ensure_token(
            md,
            "UNCLEAR",
            section_prefixes=("Variety notes",),
            reason="wrong skill (live rater)",
        )
        if not has_core:
            md = _ensure_token(
                md,
                "NOT_IMPLEMENTED",
                section_prefixes=("Limitations",),
                reason="no honest core (live rater)",
            )
    elif act == "needs_figures":
        md = _ensure_token(
            md,
            "LIMITATIONS",
            section_prefixes=("Limitations",),
            reason="needs figures (live rater)",
        )
        if gold_is_graph_live_is_text(md, tid, has_svg=has_svg):
            md = _ensure_token(
                md,
                "UNCLEAR",
                section_prefixes=("Variety notes",),
                reason="graph-match gold / live is text (live rater)",
            )

    if md != before:
        path.write_text(md if md.endswith("\n") else md + "\n", encoding="utf-8")

    after_flags = notes_flags(md)
    return {
        "ok": True,
        "type_id": tid,
        "path": str(path),
        "action": act,
        "tokens": after_flags,
        "added": [t for t in after_flags if t not in before_flags],
        "removed": [t for t in before_flags if t not in after_flags],
        "created": created,
    }


def read_notes_flags(type_id: str) -> dict[str, Any]:
    tid = _safe_type_id(type_id)
    try:
        path = resolve_notes_path(tid, create=False)
    except FileNotFoundError:
        return {
            "ok": True,
            "type_id": tid,
            "path": str(NOTES_DIR / f"{tid}.md"),
            "tokens": [],
            "exists": False,
        }
    md = path.read_text(encoding="utf-8")
    return {
        "ok": True,
        "type_id": tid,
        "path": str(path),
        "tokens": notes_flags(md),
        "exists": True,
    }


def _safe_type_id(type_id: str) -> str:
    tid = str(type_id or "").strip()
    if not _TYPE_ID_RE.fullmatch(tid):
        raise ValueError(f"invalid type_id: {type_id!r}")
    if tid.startswith("_"):
        raise ValueError(f"refusing notes path for {tid!r}")
    return tid


def _minimal_notes(type_id: str) -> str:
    return (
        f"# Notes — `{type_id}`\n\n"
        "Created by the live rater flag buttons. Fill old-path samples "
        "and OpenStax cites when wiring the leaf.\n\n"
        "## Variety notes\n\n"
        "_Add variety or skill notes here._\n\n"
        "## Limitations\n\n"
        "- **Status:** _none yet_\n"
    )


def _heading_index(lines: list[str], prefixes: tuple[str, ...]) -> int | None:
    lowered = tuple(p.lower() for p in prefixes)
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("## "):
            continue
        title = stripped[3:].strip().lower()
        if any(title.startswith(p) for p in lowered):
            return i
    return None


def _ensure_section(md: str, heading: str) -> str:
    lines = md.splitlines()
    if _heading_index(lines, (heading,)) is not None:
        return md
    block = f"\n## {heading}\n"
    return md.rstrip() + "\n" + block + "\n"


def _ensure_token(
    md: str,
    token: str,
    *,
    section_prefixes: tuple[str, ...],
    reason: str,
) -> str:
    if has_token(md, token):
        return md
    heading = section_prefixes[0]
    md = _ensure_section(md, heading)
    lines = md.splitlines()
    idx = _heading_index(lines, section_prefixes)
    if idx is None:
        idx = _heading_index(lines, (heading,))
    insert_at = (idx + 1) if idx is not None else len(lines)
    lines.insert(insert_at, f"Gallery UI flag: `{token}` — {reason}.")
    return "\n".join(lines)


def _remove_token(md: str, token: str) -> str:
    if not has_token(md, token):
        return md

    def scrub_line(line: str) -> str | None:
        if line.startswith("Gallery UI flag:"):
            stripped = re.sub(rf"`{token}`", "", line)
            stripped = re.sub(rf"\b{token}\b", "", stripped)
            if not FLAG_RE.search(stripped):
                return None
            stripped = re.sub(r"\s+·\s+", " · ", stripped)
            stripped = re.sub(r" ·\s*$", "", stripped)
            return stripped.rstrip()
        return line

    kept: list[str] = []
    for line in md.splitlines():
        new = scrub_line(line)
        if new is None:
            continue
        kept.append(new)
    text = "\n".join(kept)

    text = re.sub(rf"`{token}`", "", text)
    text = re.sub(rf"\b{token}\b", "", text)
    text = re.sub(r"·\s*·", "·", text)
    text = re.sub(r"Flags:\s*·", "Flags:", text)
    text = re.sub(r"Flags for gallery red header:\s*·", "Flags for gallery red header:", text)
    text = re.sub(r"^> \*\*\s*\*\*(?: — .*)?\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^> \*\*\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.rstrip() + "\n"
