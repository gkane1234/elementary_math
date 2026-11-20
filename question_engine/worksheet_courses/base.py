"""Shared curriculum index, slot assignment, and course dispatcher.

Grade 6 and Geometry worksheets are templates (lesson, procedure drill, or
spiral). Every other course stays on ``select_coherent_topics``.

``geometry.plan_topics`` and ``grade_6.plan_topics`` share this signature::

    plan_topics(
        seeds,
        *,
        pairing="lesson",
        scope="topic",
        topics=None,
        max_topics=4,
        include_related=True,
    ) -> dict

Return keys are ``focus``, ``warmup``, ``drill``, ``stretch``, ``omitted``,
``spiral_suggestion``, and ``course_id``. ``omitted`` stays empty here; the
assigner in this module fills ``omitted_topics`` when the question count cannot
place every focus topic.

This module does not import ``question_engine.progressive`` (that module
imports the dispatcher).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache
from math import floor
from pathlib import Path
from typing import Any, Callable

from question_engine.core.base import QUESTION_TYPES
from question_engine.type_readiness import type_not_ready

TEMPLATE_COURSES = ("grade_6_math", "geometry")

COURSE_IDS = (
    "foundations_math",
    "grade_6_math",
    "pre_algebra",
    "algebra_1",
    "geometry",
    "algebra_2",
    "precalculus",
    "calculus",
)

_CONTINUOUS_FIELD_TYPES = frozenset({"int", "float", "number", "range"})
_COURSE_ID_SET = frozenset(COURSE_IDS)

_REPO = Path(__file__).resolve().parents[2]
_CURRICULUM_PATH = _REPO / "lib" / "curriculum.ts"

_COURSE_RE = re.compile(
    rf'id:\s*"({"|".join(COURSE_IDS)})"\s*,\s*\n\s*name:\s*"([^"]+)"'
)
_CHAPTER_RE = re.compile(
    r'\{\s*id:\s*"([^"]+)"\s*,\s*name:\s*"([^"]+)"\s*,\s*topics:\s*\['
)
_LEAF_RE = re.compile(
    r'\{\s*id:\s*"([^"]+)"\s*,\s*name:\s*"([^"]+)"\s*,\s*type_id:\s*"([^"]+)"\s*\}'
)

_types_ready = False


def ensure_question_types() -> None:
    """Load catalog registration the first time a plan or eligibility check runs."""
    global _types_ready
    if _types_ready:
        return
    import question_engine.types  # noqa: F401 — populate QUESTION_TYPES

    _types_ready = True


def has_continuous_difficulty(type_id: str) -> bool:
    """True when the type schema exposes a numeric continuous ``difficulty`` knob.

    Same rule as ``question_engine.progressive.has_continuous_difficulty``.
    Kept here so course planners do not import ``progressive`` (import cycle).
    """
    ensure_question_types()
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


def is_eligible(type_id: str) -> bool:
    """Registered, not demoted, and continuous-difficulty."""
    ensure_question_types()
    if type_id not in QUESTION_TYPES:
        return False
    if type_not_ready(type_id):
        return False
    return has_continuous_difficulty(type_id)


@dataclass(frozen=True)
class Chapter:
    chapter_id: str
    title: str
    index: int


@dataclass(frozen=True)
class Leaf:
    topic_id: str
    title: str
    type_id: str
    chapter_id: str
    chapter_title: str
    chapter_index: int
    leaf_index: int


@dataclass(frozen=True)
class Course:
    course_id: str
    name: str
    chapters: tuple[Chapter, ...]
    leaves: tuple[Leaf, ...]
    by_type: dict[str, Leaf]
    by_topic: dict[str, str]


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


@lru_cache(maxsize=1)
def curriculum_index() -> dict[str, Course]:
    """Parse ``lib/curriculum.ts`` with the same chapter/leaf regex as the prereq export.

    A type_id keeps its first leaf inside a course. The same type may also
    appear in another course (for example the midpoint formula).
    """
    src = ""
    if _CURRICULUM_PATH.is_file():
        src = _CURRICULUM_PATH.read_text(encoding="utf-8")

    events: list[tuple[Any, ...]] = []
    for match in _COURSE_RE.finditer(src):
        events.append((match.start(), "course", match.group(1), match.group(2)))
    for match in _CHAPTER_RE.finditer(src):
        events.append((match.start(), "chapter", match.group(1), match.group(2)))
    for match in _LEAF_RE.finditer(src):
        events.append(
            (match.start(), "leaf", match.group(1), match.group(2), match.group(3))
        )
    events.sort(key=lambda item: item[0])

    courses: dict[str, Course] = {}
    chapters: dict[str, list[Chapter]] = {}
    leaves: dict[str, list[Leaf]] = {}
    course_id: str | None = None
    course_name: str | None = None
    current: Chapter | None = None
    leaf_index = 0

    def _ensure(cid: str, name: str) -> None:
        if cid not in courses:
            chapters[cid] = []
            leaves[cid] = []
            courses[cid] = Course(
                course_id=cid,
                name=name,
                chapters=(),
                leaves=(),
                by_type={},
                by_topic={},
            )

    for event in events:
        kind = event[1]
        if kind == "course":
            course_id = event[2]
            course_name = event[3]
            _ensure(course_id, course_name)
            current = None
            leaf_index = 0
            continue
        if kind == "chapter":
            # The course object itself matches the chapter regex (`{ id, name, topics`).
            # Its id is a course id, and it fires before the course event. Skip it.
            if event[2] in _COURSE_ID_SET or course_id is None:
                continue
            current = Chapter(
                chapter_id=event[2],
                title=event[3],
                index=len(chapters[course_id]),
            )
            chapters[course_id].append(current)
            leaf_index = 0
            continue
        if current is None or course_id is None:
            continue
        leaves[course_id].append(
            Leaf(
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

    built: dict[str, Course] = {}
    for cid, course in courses.items():
        by_type: dict[str, Leaf] = {}
        by_topic: dict[str, str] = {}
        for leaf in leaves.get(cid, []):
            by_type.setdefault(leaf.type_id, leaf)
            by_topic.setdefault(leaf.topic_id, leaf.type_id)
        built[cid] = Course(
            course_id=cid,
            name=course.name,
            chapters=tuple(chapters.get(cid, [])),
            leaves=tuple(leaves.get(cid, [])),
            by_type=by_type,
            by_topic=by_topic,
        )
    return built


def load_course(course_id: str) -> Course | None:
    return curriculum_index().get(course_id)


def template_course_of(type_id: str) -> str | None:
    """``grade_6_math`` or ``geometry`` when ``type_id`` is a leaf in that course.

    Grade 6 wins when a type is listed in both template courses. A type that
    is also taught in another course (midpoint formula, solving proportions)
    still counts as Geometry, because that leaf is on the Geometry template.
    """
    index = curriculum_index()
    found: list[str] = []
    for course_id in TEMPLATE_COURSES:
        course = index.get(course_id)
        if course is not None and type_id in course.by_type:
            found.append(course_id)
    if "grade_6_math" in found:
        return "grade_6_math"
    if "geometry" in found:
        return "geometry"
    return None


def _load_planner(course_id: str) -> Callable[..., dict[str, Any]] | None:
    if course_id == "grade_6_math":
        from question_engine.worksheet_courses.grade_6 import plan_topics

        return plan_topics
    if course_id == "geometry":
        try:
            from question_engine.worksheet_courses.geometry import plan_topics
        except ImportError:
            return None
        return plan_topics
    return None


def plan_topics_for_seeds(
    seeds: Any,
    *,
    pairing: str = "lesson",
    scope: str = "topic",
    topics: Any = None,
    max_topics: int = 4,
    include_related: bool = True,
) -> dict[str, Any] | None:
    """Plan a Grade 6 or Geometry sheet. ``None`` means use the old expander.

    Returns ``None`` when any seed is outside both template courses, when the
    seeds come from both courses, or when the Geometry planner cannot be
    imported yet. Grade 6 still plans if Geometry is missing.
    """
    seed_list = _coerce_strings(seeds)
    if not seed_list:
        return None
    courses: list[str] = []
    for seed in seed_list:
        course_id = template_course_of(seed)
        if course_id is None:
            return None
        courses.append(course_id)
    if len(set(courses)) != 1:
        return None
    planner = _load_planner(courses[0])
    if planner is None:
        return None
    return planner(
        seed_list,
        pairing=pairing,
        scope=scope,
        topics=topics,
        max_topics=max_topics,
        include_related=include_related,
    )


def _portion(count: int, fraction: float) -> int:
    if count <= 0:
        return 0
    return int(floor(count * fraction + 0.5))


def _difficulty_values(count: int, d_min: float, d_max: float) -> list[float]:
    """Monotone ramp. Same endpoints as ``progressive.difficulty_ramp``."""
    if count < 1:
        return []
    lo = float(d_min)
    hi = float(d_max)
    if count == 1:
        return [lo]
    if hi < lo:
        lo, hi = hi, lo
    return [lo + (hi - lo) * (i / (count - 1)) for i in range(count)]


def _phase_question_counts(
    count: int,
    *,
    has_warmup: bool,
    has_stretch: bool,
    has_drill: bool,
    n_focus: int,
) -> tuple[int, int, int, int]:
    """Return ``(warmup, focus, drill, stretch)`` counts that sum to ``count``.

    Warm-up is about 20% (at least 1 when ``count >= 4`` and a warm-up exists).
    Stretch is about 15% (at least 1 when ``count >= 6`` and a stretch exists).
    Drill is about 20% of what remains. The rest is focus. Minimums shrink when
    the focus topics would otherwise not fit.
    """
    if count < 1 or n_focus < 1:
        return 0, 0, 0, 0
    if count < n_focus:
        return 0, count, 0, 0

    warmup_n = _portion(count, 0.20) if has_warmup else 0
    if has_warmup and count >= 4:
        warmup_n = max(1, warmup_n)
    stretch_n = _portion(count, 0.15) if has_stretch else 0
    if has_stretch and count >= 6:
        stretch_n = max(1, stretch_n)

    warmup_floor = 1 if has_warmup and count >= 4 else 0
    stretch_floor = 1 if has_stretch and count >= 6 else 0

    def _fits(warmup_count: int, stretch_count: int) -> bool:
        return count - warmup_count - stretch_count >= n_focus

    while not _fits(warmup_n, stretch_n):
        if warmup_n > warmup_floor:
            warmup_n -= 1
        elif stretch_n > stretch_floor:
            stretch_n -= 1
        elif warmup_n > 0:
            warmup_n -= 1
        elif stretch_n > 0:
            stretch_n -= 1
        else:
            break

    remaining = count - warmup_n - stretch_n
    if remaining < n_focus:
        warmup_n = 0
        stretch_n = 0
        remaining = count

    drill_n = _portion(remaining, 0.20) if has_drill else 0
    drill_n = min(drill_n, max(0, remaining - n_focus))
    focus_n = remaining - drill_n
    return warmup_n, focus_n, drill_n, stretch_n


def _round_robin(topics: list[str], count: int) -> list[str]:
    if count <= 0 or not topics:
        return []
    return [topics[i % len(topics)] for i in range(count)]


def _blocks(topics: list[str], count: int) -> list[str]:
    """Contiguous equal split, extras on the earlier topics."""
    if count <= 0 or not topics:
        return []
    base, extra = divmod(count, len(topics))
    out: list[str] = []
    for index, type_id in enumerate(topics):
        out.extend([type_id] * (base + (1 if index < extra else 0)))
    return out


def _warmup_ids(topics: list[str], count: int) -> list[str]:
    if count <= 0 or not topics:
        return []
    # Fewer slots than warm-up skills: keep the closest ones (end of the list).
    if count < len(topics):
        topics = topics[-count:]
    return _round_robin(topics, count)


def _slot(type_id: str, difficulty: float, index: int, phase: str) -> dict[str, Any]:
    return {
        "type_id": type_id,
        "difficulty": round(float(difficulty), 4),
        "index": index,
        "phase": phase,
    }


def assign_template_slots(
    plan: dict[str, Any],
    count: int,
    *,
    d_min: float = 0.0,
    d_max: float = 18.0,
    style: str = "ramp",
    ramp_each_topic: bool = False,
) -> tuple[list[dict[str, Any]], list[str]]:
    """Assign question slots for a course plan.

    ``straight`` uses the focus topics only, split evenly, at the midpoint of
    ``d_min`` and ``d_max``, phase ``focus``.

    ``ramp`` walks warm-up, focus, drill, then stretch. Difficulty is one
    monotone ramp from ``d_min`` to ``d_max`` across every slot.
    ``ramp_each_topic`` groups the focus slice so each focus topic occupies a
    contiguous band of that ramp. When ``count`` is smaller than the focus
    list, the earlier focus topics are placed and the rest are returned as
    omitted topic ids.
    """
    focus = [str(type_id) for type_id in (plan.get("focus") or []) if type_id]
    warmup = [str(type_id) for type_id in (plan.get("warmup") or []) if type_id]
    drill_topics = [str(type_id) for type_id in (plan.get("drill") or []) if type_id]
    stretch = [str(type_id) for type_id in (plan.get("stretch") or []) if type_id]
    try:
        count = int(count)
    except (TypeError, ValueError):
        count = 0
    if count < 1 or not focus:
        return [], list(focus)

    style_key = str(style or "ramp").strip().lower()
    if style_key == "straight":
        placed = focus if count >= len(focus) else focus[:count]
        omitted = focus[len(placed) :]
        midpoint = round((float(d_min) + float(d_max)) / 2.0, 4)
        sequence = _blocks(placed, count)
        slots = [
            _slot(type_id, midpoint, index, "focus")
            for index, type_id in enumerate(sequence)
        ]
        return slots, omitted

    if count < len(focus):
        placed = focus[:count]
        omitted = focus[count:]
        values = _difficulty_values(count, d_min, d_max)
        slots = [
            _slot(placed[index], values[index], index, "focus")
            for index in range(count)
        ]
        return slots, omitted

    warmup_n, focus_n, drill_n, stretch_n = _phase_question_counts(
        count,
        has_warmup=bool(warmup),
        has_stretch=bool(stretch),
        has_drill=bool(drill_topics),
        n_focus=len(focus),
    )
    if ramp_each_topic:
        focus_ids = _blocks(focus, focus_n)
    else:
        focus_ids = _round_robin(focus, focus_n)
    sequence: list[tuple[str, str]] = []
    sequence.extend(("warmup", type_id) for type_id in _warmup_ids(warmup, warmup_n))
    sequence.extend(("focus", type_id) for type_id in focus_ids)
    sequence.extend(("drill", type_id) for type_id in _round_robin(drill_topics, drill_n))
    sequence.extend(("stretch", type_id) for type_id in _round_robin(stretch, stretch_n))
    # Guard a rounding miss so the sheet length stays ``count``.
    if len(sequence) < count and focus:
        sequence.extend(("focus", focus[i % len(focus)]) for i in range(count - len(sequence)))
    sequence = sequence[:count]
    values = _difficulty_values(len(sequence), d_min, d_max)
    slots = [
        _slot(type_id, values[index], index, phase)
        for index, (phase, type_id) in enumerate(sequence)
    ]
    return slots, []


__all__ = [
    "TEMPLATE_COURSES",
    "Chapter",
    "Course",
    "Leaf",
    "assign_template_slots",
    "curriculum_index",
    "ensure_question_types",
    "has_continuous_difficulty",
    "is_eligible",
    "load_course",
    "plan_topics_for_seeds",
    "template_course_of",
]
