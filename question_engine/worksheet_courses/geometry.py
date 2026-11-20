"""Geometry topic plans for progressive worksheets.

Lesson order is the ``geometry`` course in ``lib/curriculum.ts``. Unit
prerequisites come from ``scripts/example_mining/prerequisites/geometry.json``.
When a ``type_id`` has ``requires`` in ``topic_leaves.json``, those skill edges
are the lesson warm-up for a single-topic scope.

This module does not import ``question_engine.progressive`` (that package
lazy-imports course planners).
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from question_engine.core.base import QUESTION_TYPES
from question_engine.type_readiness import type_not_ready

COURSE_ID = "geometry"

_CONTINUOUS_FIELD_TYPES = frozenset({"int", "float", "number", "range"})
_PAIRINGS = frozenset({"lesson", "drill", "spiral"})
_SCOPES = frozenset({"topic", "unit", "adjacent"})

_REPO = Path(__file__).resolve().parents[2]
_CURRICULUM_PATH = _REPO / "lib" / "curriculum.ts"
_GEOMETRY_PREREQS_PATH = (
    _REPO / "scripts" / "example_mining" / "prerequisites" / "geometry.json"
)
_TOPIC_LEAVES_PATH = (
    _REPO / "scripts" / "example_mining" / "prerequisites" / "topic_leaves.json"
)

_CHAPTER_RE = re.compile(
    r'\{\s*id:\s*"([^"]+)"\s*,\s*name:\s*"([^"]+)"\s*,\s*topics:\s*\['
)
_LEAF_RE = re.compile(
    r'\{\s*id:\s*"([^"]+)"\s*,\s*name:\s*"([^"]+)"\s*,\s*type_id:\s*"([^"]+)"\s*\}'
)

_types_ready = False


def _ensure_registered() -> None:
    """Load catalog registration the first time a plan is built."""
    global _types_ready
    if _types_ready:
        return
    import question_engine.types  # noqa: F401 — populate QUESTION_TYPES

    _types_ready = True


def _has_numeric_difficulty(type_id: str) -> bool:
    """Local copy of the continuous-difficulty check (no progressive import)."""
    qt = QUESTION_TYPES.get(type_id)
    if qt is None:
        return False
    try:
        fields = qt.settings_schema()
    except Exception:  # noqa: BLE001 — schema failures are not continuous-ready
        return False
    for field in fields:
        if getattr(field, "key", None) != "difficulty":
            continue
        return getattr(field, "type", None) in _CONTINUOUS_FIELD_TYPES
    return False


def _eligible(type_id: str) -> bool:
    if type_id not in QUESTION_TYPES:
        return False
    if type_not_ready(type_id):
        return False
    return _has_numeric_difficulty(type_id)


@dataclass(frozen=True)
class _Chapter:
    chapter_id: str
    title: str
    index: int


@dataclass(frozen=True)
class _Leaf:
    topic_id: str
    title: str
    type_id: str
    chapter_id: str
    chapter_title: str
    chapter_index: int
    leaf_index: int


@dataclass(frozen=True)
class _Course:
    chapters: tuple[_Chapter, ...]
    leaves: tuple[_Leaf, ...]
    by_type: dict[str, _Leaf]
    by_topic: dict[str, str]


def _empty_plan() -> dict[str, Any]:
    return {
        "focus": [],
        "warmup": [],
        "drill": [],
        "stretch": [],
        "omitted": [],
        "spiral_suggestion": None,
        "course_id": COURSE_ID,
    }


def _dedupe(ids: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for type_id in ids:
        if type_id in seen:
            continue
        seen.add(type_id)
        out.append(type_id)
    return out


def _coerce_strings(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        text = value.strip()
        return [text] if text else []
    out: list[str] = []
    for item in value:
        if item is None:
            continue
        text = str(item).strip()
        if text:
            out.append(text)
    return out


def _geometry_slice(src: str) -> str:
    marker = 'id: "geometry"'
    start = src.find(marker)
    if start < 0:
        return ""
    end = src.find('id: "precalculus"', start + len(marker))
    if end < 0:
        end = len(src)
    return src[start:end]


@lru_cache(maxsize=1)
def _course() -> _Course:
    """Parse the geometry course only, in curriculum chapter order."""
    src = ""
    if _CURRICULUM_PATH.is_file():
        src = _geometry_slice(_CURRICULUM_PATH.read_text(encoding="utf-8"))

    events: list[tuple[Any, ...]] = []
    for match in _CHAPTER_RE.finditer(src):
        events.append((match.start(), "chapter", match.group(1), match.group(2)))
    for match in _LEAF_RE.finditer(src):
        events.append(
            (match.start(), "leaf", match.group(1), match.group(2), match.group(3))
        )
    events.sort(key=lambda item: item[0])

    chapters: list[_Chapter] = []
    leaves: list[_Leaf] = []
    current: _Chapter | None = None
    leaf_index = 0
    for event in events:
        kind = event[1]
        if kind == "chapter":
            current = _Chapter(chapter_id=event[2], title=event[3], index=len(chapters))
            chapters.append(current)
            leaf_index = 0
            continue
        if current is None:
            continue
        leaves.append(
            _Leaf(
                topic_id=event[2],
                title=event[3],
                type_id=event[4],
                chapter_id=current.chapter_id,
                chapter_title=current.title,
                chapter_index=current.index,
                leaf_index=leaf_index,
            )
        )
        leaf_index += 1

    by_type: dict[str, _Leaf] = {}
    by_topic: dict[str, str] = {}
    for leaf in leaves:
        by_type.setdefault(leaf.type_id, leaf)
        by_topic.setdefault(leaf.topic_id, leaf.type_id)
    return _Course(
        chapters=tuple(chapters),
        leaves=tuple(leaves),
        by_type=by_type,
        by_topic=by_topic,
    )


def _chapter(course: _Course, chapter_id: str | None) -> _Chapter | None:
    if not chapter_id:
        return None
    for chapter in course.chapters:
        if chapter.chapter_id == chapter_id:
            return chapter
    return None


def _locate(course: _Course, token: str) -> _Leaf | None:
    """Resolve a geometry type_id or topic id. Other courses stay unresolved."""
    if token in course.by_type:
        return course.by_type[token]
    type_id = course.by_topic.get(token)
    if type_id is None:
        return None
    return course.by_type.get(type_id)


@lru_cache(maxsize=1)
def _unit_requires() -> dict[str, tuple[str, ...]]:
    """In-course chapter ids required by each geometry chapter, JSON order."""
    if not _GEOMETRY_PREREQS_PATH.is_file():
        return {}
    raw = json.loads(_GEOMETRY_PREREQS_PATH.read_text(encoding="utf-8"))
    out: dict[str, tuple[str, ...]] = {}
    if not isinstance(raw, dict):
        return out
    for key, value in raw.items():
        if not isinstance(key, str) or not key.startswith("geometry:"):
            continue
        if not isinstance(value, dict):
            continue
        reqs = value.get("requires") or []
        if not isinstance(reqs, list):
            continue
        geo: list[str] = []
        for req in reqs:
            if isinstance(req, str) and req.startswith("geometry:"):
                geo.append(req.split(":", 1)[1])
        out[key.split(":", 1)[1]] = tuple(geo)
    return out


@lru_cache(maxsize=1)
def _topic_leaf_requires() -> dict[str, tuple[str, ...]]:
    if not _TOPIC_LEAVES_PATH.is_file():
        return {}
    raw = json.loads(_TOPIC_LEAVES_PATH.read_text(encoding="utf-8"))
    out: dict[str, tuple[str, ...]] = {}
    if not isinstance(raw, dict):
        return out
    for key, value in raw.items():
        if not isinstance(key, str) or key.startswith("_") or not isinstance(value, dict):
            continue
        reqs = value.get("requires") or []
        if not isinstance(reqs, list):
            continue
        cleaned = tuple(str(req) for req in reqs if isinstance(req, str) and req)
        if cleaned:
            out[key] = cleaned
    return out


def _requires_for(type_id: str) -> tuple[str, ...]:
    """Skill edges for ``type_id``. Empty when topic_leaves has no requires."""
    return _topic_leaf_requires().get(type_id, ())


def _order_like_course(course: _Course, ids: list[str]) -> list[str]:
    rank = {leaf.type_id: index for index, leaf in enumerate(course.leaves)}
    deduped = _dedupe(ids)
    in_course = [type_id for type_id in deduped if type_id in rank]
    outside = [type_id for type_id in deduped if type_id not in rank]
    in_course.sort(key=lambda type_id: rank[type_id])
    return in_course + outside


def _eligible_ids_for_chapters(course: _Course, chapter_ids: list[str]) -> list[str]:
    wanted = set(chapter_ids)
    out: list[str] = []
    seen: set[str] = set()
    for leaf in course.leaves:
        if leaf.chapter_id not in wanted or leaf.type_id in seen:
            continue
        if not _eligible(leaf.type_id):
            continue
        seen.add(leaf.type_id)
        out.append(leaf.type_id)
    return out


def _unique_chapters(course: _Course, chapter_ids: list[str]) -> list[str]:
    rank = {chapter.chapter_id: chapter.index for chapter in course.chapters}
    seen: set[str] = set()
    uniq: list[str] = []
    for chapter_id in chapter_ids:
        if chapter_id in seen or chapter_id not in rank:
            continue
        seen.add(chapter_id)
        uniq.append(chapter_id)
    uniq.sort(key=lambda chapter_id: rank[chapter_id])
    return uniq


def _next_chapter_id(course: _Course, chapter_id: str | None) -> str | None:
    chapter = _chapter(course, chapter_id)
    if chapter is None:
        return None
    nxt = chapter.index + 1
    if nxt >= len(course.chapters):
        return None
    return course.chapters[nxt].chapter_id


def _prev_chapter_id(course: _Course, chapter_id: str | None) -> str | None:
    chapter = _chapter(course, chapter_id)
    if chapter is None or chapter.index == 0:
        return None
    return course.chapters[chapter.index - 1].chapter_id


def _lesson_prereq_chapter(course: _Course, chapter_id: str) -> str | None:
    """Latest geometry.json prerequisite that is an earlier chapter in this course."""
    chapter = _chapter(course, chapter_id)
    if chapter is None:
        return None
    best_id: str | None = None
    best_index = -1
    for req in _unit_requires().get(chapter_id, ()):
        req_chapter = _chapter(course, req)
        if req_chapter is None or req_chapter.index >= chapter.index:
            continue
        if req_chapter.index > best_index:
            best_index = req_chapter.index
            best_id = req_chapter.chapter_id
    return best_id


def _chapters_of_ids(course: _Course, ids: list[str]) -> list[str]:
    found: list[str] = []
    for type_id in ids:
        leaf = course.by_type.get(type_id)
        if leaf is not None:
            found.append(leaf.chapter_id)
    return _unique_chapters(course, found)


def _tail_chapter(
    course: _Course,
    chapter_id: str | None,
    count: int,
    banned: set[str],
) -> list[str]:
    if not chapter_id or count <= 0:
        return []
    ids = [
        type_id
        for type_id in _eligible_ids_for_chapters(course, [chapter_id])
        if type_id not in banned
    ]
    return ids[-count:]


def _head_chapter(course: _Course, chapter_id: str | None, banned: set[str]) -> list[str]:
    if not chapter_id:
        return []
    for type_id in _eligible_ids_for_chapters(course, [chapter_id]):
        if type_id not in banned:
            return [type_id]
    return []


def _drill_neighborhood(course: _Course, seed_ids: list[str]) -> list[str]:
    """Seed plus the previous and next eligible leaf in the same chapter."""
    picked: list[str] = []
    for seed in seed_ids:
        leaf = course.by_type.get(seed)
        if leaf is None or not _eligible(seed):
            continue
        chapter_ids = _eligible_ids_for_chapters(course, [leaf.chapter_id])
        if seed not in chapter_ids:
            continue
        index = chapter_ids.index(seed)
        if index > 0:
            picked.append(chapter_ids[index - 1])
        picked.append(seed)
        if index + 1 < len(chapter_ids):
            picked.append(chapter_ids[index + 1])
    return _order_like_course(course, picked)


def _warmup_lesson_topic(course: _Course, focus: list[str], anchor_id: str | None) -> list[str]:
    focus_set = set(focus)
    seed = anchor_id if anchor_id in focus_set else (focus[0] if focus else None)
    if seed is None:
        return []
    reqs = _requires_for(seed)
    if reqs:
        chosen: list[str] = []
        for type_id in reqs:
            if type_id in focus_set or type_id in chosen or not _eligible(type_id):
                continue
            chosen.append(type_id)
            if len(chosen) == 2:
                break
        return chosen

    leaf = course.by_type.get(seed)
    if leaf is None:
        return []
    indexes = [
        course.by_type[type_id].leaf_index
        for type_id in focus
        if type_id in course.by_type and course.by_type[type_id].chapter_id == leaf.chapter_id
    ]
    cutoff = min(indexes) if indexes else leaf.leaf_index
    earlier: list[str] = []
    for item in course.leaves:
        if item.chapter_id != leaf.chapter_id or item.leaf_index >= cutoff:
            continue
        if item.type_id in focus_set or not _eligible(item.type_id):
            continue
        earlier.append(item.type_id)
    return _dedupe(earlier)[-2:]


def _stretch_lesson_topic(course: _Course, focus: list[str], anchor_id: str | None) -> list[str]:
    seed = anchor_id if anchor_id in course.by_type else None
    if seed is None:
        for type_id in focus:
            if type_id in course.by_type:
                seed = type_id
                break
    if seed is None:
        return []
    leaf = course.by_type[seed]
    indexes = [
        course.by_type[type_id].leaf_index
        for type_id in focus
        if type_id in course.by_type and course.by_type[type_id].chapter_id == leaf.chapter_id
    ]
    cutoff = max(indexes) if indexes else leaf.leaf_index
    banned = set(focus)
    for item in course.leaves:
        if item.chapter_id != leaf.chapter_id or item.leaf_index <= cutoff:
            continue
        if item.type_id in banned or not _eligible(item.type_id):
            continue
        return [item.type_id]
    return _head_chapter(course, _next_chapter_id(course, leaf.chapter_id), banned)


def _trim_focus(focus: list[str], protected: list[str], limit: int) -> list[str]:
    """Keep the seed, then the earliest other focus leaves, within ``limit``."""
    if limit <= 0:
        return []
    if len(focus) <= limit:
        return list(focus)
    protected_set = set(protected)
    kept_protected = [type_id for type_id in focus if type_id in protected_set]
    if len(kept_protected) >= limit:
        keep = set(kept_protected[:limit])
    else:
        need = limit - len(kept_protected)
        extras = [type_id for type_id in focus if type_id not in protected_set][:need]
        keep = set(kept_protected) | set(extras)
    return [type_id for type_id in focus if type_id in keep]


def _trim(
    focus: list[str],
    warmup: list[str],
    stretch: list[str],
    protected: list[str],
    max_topics: int,
    explicit: bool,
) -> tuple[list[str], list[str], list[str]]:
    focus = _dedupe(focus)
    focus_set = set(focus)
    warmup = [type_id for type_id in _dedupe(warmup) if type_id not in focus_set]
    warmup_set = set(warmup)
    stretch = [
        type_id
        for type_id in _dedupe(stretch)
        if type_id not in focus_set and type_id not in warmup_set
    ]
    if max_topics < 0:
        max_topics = 0

    if explicit:
        # Checked topics stay even when they exceed max_topics. The cap only
        # limits warm-up and stretch that the planner added on its own.
        room = max(0, max_topics - len(focus))
        if len(warmup) > room:
            warmup = warmup[-room:] if room else []
        stretch = stretch[: max(0, room - len(warmup))]
        return focus, warmup, stretch

    while len(focus) + len(warmup) + len(stretch) > max_topics and stretch:
        stretch.pop()
    while len(focus) + len(warmup) + len(stretch) > max_topics and warmup:
        warmup.pop(0)
    if len(focus) > max_topics:
        focus = _trim_focus(focus, protected, max_topics)
    return focus, warmup, stretch


def plan_topics(
    seeds: Any,
    *,
    pairing: str = "lesson",
    scope: str = "topic",
    topics: Any = None,
    max_topics: int = 4,
    include_related: bool = True,
) -> dict[str, Any]:
    """Plan Geometry focus, warm-up, drill, and stretch type ids.

    ``seeds`` may be a type id or a curriculum topic id (for example
    ``radical_distance_formula`` resolves to ``geo_parallel_distance_formula``).
    Types outside this course are ignored. ``omitted`` stays empty; the shared
    assigner trims by question count.

    When ``topics`` is omitted, ``len(focus) + len(warmup) + len(stretch)`` is
    kept at or below ``max_topics`` by dropping stretch, then warm-up, then
    extra focus leaves. The seed is kept. A non-empty ``topics`` list is the
    focus intersection with the scope and is not trimmed to satisfy the cap.
    """
    _ensure_registered()
    course = _course()
    plan = _empty_plan()

    pairing_key = str(pairing or "lesson").strip().lower()
    if pairing_key not in _PAIRINGS:
        pairing_key = "lesson"
    scope_key = str(scope or "topic").strip().lower()
    if scope_key not in _SCOPES:
        scope_key = "topic"
    try:
        cap = int(max_topics)
    except (TypeError, ValueError):
        cap = 4

    located: list[_Leaf] = []
    seen_seeds: set[str] = set()
    for token in _coerce_strings(seeds):
        leaf = _locate(course, token)
        if leaf is None or leaf.type_id in seen_seeds:
            continue
        seen_seeds.add(leaf.type_id)
        located.append(leaf)
    if not located:
        return plan

    eligible_seed_ids = [leaf.type_id for leaf in located if _eligible(leaf.type_id)]
    anchor = located[0]
    anchor_chapter = anchor.chapter_id
    anchor_id = eligible_seed_ids[0] if eligible_seed_ids else None

    if scope_key == "unit":
        chapter_ids = _unique_chapters(course, [leaf.chapter_id for leaf in located])
        selected = _eligible_ids_for_chapters(course, chapter_ids)
    elif scope_key == "adjacent":
        chapter_ids = []
        for leaf in located:
            chapter_ids.append(leaf.chapter_id)
            nxt = _next_chapter_id(course, leaf.chapter_id)
            if nxt:
                chapter_ids.append(nxt)
        selected = _eligible_ids_for_chapters(course, _unique_chapters(course, chapter_ids))
    elif pairing_key == "drill":
        selected = _drill_neighborhood(course, eligible_seed_ids)
    else:
        selected = list(eligible_seed_ids)

    topic_tokens = _coerce_strings(topics)
    explicit = bool(topic_tokens)
    if explicit:
        allowed: set[str] = set()
        for token in topic_tokens:
            leaf = _locate(course, token)
            if leaf is not None and _eligible(leaf.type_id):
                allowed.add(leaf.type_id)
        selected_set = set(selected)
        selected = [
            type_id
            for type_id in _order_like_course(course, list(selected_set | allowed))
            if type_id in selected_set and type_id in allowed
        ]

    focus = list(selected)
    warmup: list[str] = []
    stretch: list[str] = []
    suggestion: str | None = None

    if pairing_key == "drill":
        warmup = []
        stretch = []
    elif pairing_key == "spiral":
        chapters = _chapters_of_ids(course, focus) or [anchor_chapter]
        current = chapters[0]
        prev_id = _prev_chapter_id(course, current)
        banned = set(focus)
        warmup = _tail_chapter(course, prev_id, 2, banned)
        stretch = _head_chapter(
            course,
            _next_chapter_id(course, chapters[-1]),
            banned | set(warmup),
        )
        prev = _chapter(course, prev_id)
        current_chapter = _chapter(course, current)
        if prev is not None and current_chapter is not None and current_chapter.index > 0:
            suggestion = f"Review the previous unit, {prev.title}."
    elif scope_key == "topic":
        warmup = _warmup_lesson_topic(course, focus, anchor_id)
        stretch = _stretch_lesson_topic(course, focus, anchor_id)
    else:
        warmup = _tail_chapter(
            course,
            _lesson_prereq_chapter(course, anchor_chapter),
            2,
            set(focus),
        )
        stretch = _head_chapter(
            course,
            _next_chapter_id(course, (_chapters_of_ids(course, focus) or [anchor_chapter])[-1]),
            set(focus) | set(warmup),
        )

    if not include_related:
        warmup = []
        stretch = []

    protected = [type_id for type_id in eligible_seed_ids if type_id in set(focus)]
    focus, warmup, stretch = _trim(focus, warmup, stretch, protected, cap, explicit)

    if pairing_key == "spiral":
        drill: list[str] = []
    else:
        drill = list(focus)

    if pairing_key != "spiral":
        suggestion = None

    plan["focus"] = focus
    plan["warmup"] = warmup
    plan["drill"] = drill
    plan["stretch"] = stretch
    plan["omitted"] = []
    plan["spiral_suggestion"] = suggestion
    plan["course_id"] = COURSE_ID
    return plan


__all__ = ["plan_topics"]
