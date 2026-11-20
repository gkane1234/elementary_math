"""Grade 6 topic plans for progressive worksheets.

Lesson order is the ``grade_6_math`` course in ``lib/curriculum.ts``. Unit
prerequisites come from ``scripts/example_mining/prerequisites/grade_6_math.json``.
When a ``type_id`` has ``requires`` in ``topic_leaves.json``, those skill edges
are the lesson warm-up for a single-topic scope.

This module does not import ``question_engine.progressive`` (that package
imports the course dispatcher).
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

from question_engine.worksheet_courses.base import (
    Course,
    Leaf,
    ensure_question_types,
    is_eligible,
    load_course,
)

COURSE_ID = "grade_6_math"

_REPO = Path(__file__).resolve().parents[2]
_PREREQS_PATH = _REPO / "scripts" / "example_mining" / "prerequisites" / "grade_6_math.json"
_TOPIC_LEAVES_PATH = (
    _REPO / "scripts" / "example_mining" / "prerequisites" / "topic_leaves.json"
)

_PAIRINGS = frozenset({"lesson", "drill", "spiral"})
_SCOPES = frozenset({"topic", "unit", "adjacent"})


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


def _course() -> Course:
    course = load_course(COURSE_ID)
    if course is None:
        return Course(
            course_id=COURSE_ID,
            name="Grade 6 Math",
            chapters=(),
            leaves=(),
            by_type={},
            by_topic={},
        )
    return course


def _chapter(course: Course, chapter_id: str | None):
    if not chapter_id:
        return None
    for chapter in course.chapters:
        if chapter.chapter_id == chapter_id:
            return chapter
    return None


def _locate(course: Course, token: str) -> Leaf | None:
    """Resolve a Grade 6 type_id or topic id. Other courses stay unresolved."""
    if token in course.by_type:
        return course.by_type[token]
    type_id = course.by_topic.get(token)
    if type_id is None:
        return None
    return course.by_type.get(type_id)


@lru_cache(maxsize=1)
def _unit_requires() -> dict[str, tuple[str, ...]]:
    """In-course chapter ids required by each Grade 6 chapter, JSON order."""
    if not _PREREQS_PATH.is_file():
        return {}
    raw = json.loads(_PREREQS_PATH.read_text(encoding="utf-8"))
    out: dict[str, tuple[str, ...]] = {}
    if not isinstance(raw, dict):
        return out
    prefix = COURSE_ID + ":"
    for key, value in raw.items():
        if not isinstance(key, str) or not key.startswith(prefix):
            continue
        if not isinstance(value, dict):
            continue
        reqs = value.get("requires") or []
        if not isinstance(reqs, list):
            continue
        same_course: list[str] = []
        for req in reqs:
            if isinstance(req, str) and req.startswith(prefix):
                same_course.append(req.split(":", 1)[1])
        out[key.split(":", 1)[1]] = tuple(same_course)
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


def _order_like_course(course: Course, ids: list[str]) -> list[str]:
    rank = {leaf.type_id: index for index, leaf in enumerate(course.leaves)}
    deduped = _dedupe(ids)
    in_course = [type_id for type_id in deduped if type_id in rank]
    outside = [type_id for type_id in deduped if type_id not in rank]
    in_course.sort(key=lambda type_id: rank[type_id])
    return in_course + outside


def _eligible_ids_for_chapters(course: Course, chapter_ids: list[str]) -> list[str]:
    wanted = set(chapter_ids)
    out: list[str] = []
    seen: set[str] = set()
    for leaf in course.leaves:
        if leaf.chapter_id not in wanted or leaf.type_id in seen:
            continue
        if not is_eligible(leaf.type_id):
            continue
        seen.add(leaf.type_id)
        out.append(leaf.type_id)
    return out


def _unique_chapters(course: Course, chapter_ids: list[str]) -> list[str]:
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


def _next_chapter_id(course: Course, chapter_id: str | None) -> str | None:
    chapter = _chapter(course, chapter_id)
    if chapter is None:
        return None
    nxt = chapter.index + 1
    if nxt >= len(course.chapters):
        return None
    return course.chapters[nxt].chapter_id


def _prev_chapter_id(course: Course, chapter_id: str | None) -> str | None:
    chapter = _chapter(course, chapter_id)
    if chapter is None or chapter.index == 0:
        return None
    return course.chapters[chapter.index - 1].chapter_id


def _lesson_prereq_chapter(course: Course, chapter_id: str) -> str | None:
    """Latest same-course prerequisite that is an earlier chapter."""
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


def _chapters_of_ids(course: Course, ids: list[str]) -> list[str]:
    found: list[str] = []
    for type_id in ids:
        leaf = course.by_type.get(type_id)
        if leaf is not None:
            found.append(leaf.chapter_id)
    return _unique_chapters(course, found)


def _tail_chapter(
    course: Course,
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


def _head_chapter(course: Course, chapter_id: str | None, banned: set[str]) -> list[str]:
    if not chapter_id:
        return []
    for type_id in _eligible_ids_for_chapters(course, [chapter_id]):
        if type_id not in banned:
            return [type_id]
    return []


def _drill_neighborhood(course: Course, seed_ids: list[str]) -> list[str]:
    """Seed plus the previous and next eligible leaf in the same chapter."""
    picked: list[str] = []
    for seed in seed_ids:
        leaf = course.by_type.get(seed)
        if leaf is None or not is_eligible(seed):
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


def _warmup_lesson_topic(course: Course, focus: list[str], anchor_id: str | None) -> list[str]:
    focus_set = set(focus)
    seed = anchor_id if anchor_id in focus_set else (focus[0] if focus else None)
    if seed is None:
        return []
    reqs = _requires_for(seed)
    if reqs:
        chosen: list[str] = []
        for type_id in reqs:
            if type_id in focus_set or type_id in chosen or not is_eligible(type_id):
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
        if item.type_id in focus_set or not is_eligible(item.type_id):
            continue
        earlier.append(item.type_id)
    return _dedupe(earlier)[-2:]


def _stretch_lesson_topic(course: Course, focus: list[str], anchor_id: str | None) -> list[str]:
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
        if item.type_id in banned or not is_eligible(item.type_id):
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
        # Checked topics stay even when they exceed max_topics. Auto warm-up
        # and stretch only fill the room left under max_topics.
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


def _spiral_suggestion(course: Course, focus: list[str], anchor_chapter: str) -> str | None:
    """Name the previous unit when this unit is not the first in the course."""
    chapters = _chapters_of_ids(course, focus) or [anchor_chapter]
    current = _chapter(course, chapters[0])
    if current is None or current.index <= 0:
        return None
    prev = _chapter(course, _prev_chapter_id(course, current.chapter_id))
    if prev is None:
        return None
    return prev.title


def plan_topics(
    seeds: Any,
    *,
    pairing: str = "lesson",
    scope: str = "topic",
    topics: Any = None,
    max_topics: int = 4,
    include_related: bool = True,
) -> dict[str, Any]:
    """Plan Grade 6 focus, warm-up, drill, and stretch type ids.

    Keyword signature matches ``geometry.plan_topics``. ``seeds`` may be a
    type id or a curriculum topic id. Types outside this course are ignored.
    ``omitted`` stays empty; the shared assigner trims by question count.

    When ``topics`` is omitted, ``len(focus) + len(warmup) + len(stretch)`` is
    kept at or below ``max_topics`` by dropping stretch, then warm-up, then
    extra focus leaves. The seed is kept. A non-empty ``topics`` list is the
    focus intersection with the scope and is not trimmed to satisfy the cap.
    ``spiral_suggestion`` names the previous unit whenever this unit is not
    first in the course, including when pairing is still lesson.
    """
    ensure_question_types()
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

    located: list[Leaf] = []
    seen_seeds: set[str] = set()
    for token in _coerce_strings(seeds):
        leaf = _locate(course, token)
        if leaf is None or leaf.type_id in seen_seeds:
            continue
        seen_seeds.add(leaf.type_id)
        located.append(leaf)
    if not located:
        return plan

    eligible_seed_ids = [leaf.type_id for leaf in located if is_eligible(leaf.type_id)]
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
            if leaf is not None and is_eligible(leaf.type_id):
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

    plan["focus"] = focus
    plan["warmup"] = warmup
    plan["drill"] = drill
    plan["stretch"] = stretch
    plan["omitted"] = []
    plan["spiral_suggestion"] = _spiral_suggestion(course, focus, anchor_chapter)
    plan["course_id"] = COURSE_ID
    return plan


__all__ = ["plan_topics"]
