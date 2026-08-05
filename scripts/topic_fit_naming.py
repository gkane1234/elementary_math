"""Course-prefixed folder names for topic_fit galleries.

Folder names should start with the course they come from:
  g6_ / pa_ / a1_ / ge_ / a2_ / pc_ / c1_ / c2_ / c3_

Python type_ids are left unchanged. Gallery dirs use:
  - type_id as-is when it already has a course prefix
  - ``{course_prefix}{type_id}`` otherwise (calc_* defaults to c1_)
"""
from __future__ import annotations

from collections import defaultdict
from functools import lru_cache
from typing import Iterable

COURSE_PREFIX: dict[str, str] = {
    "grade_6": "g6_",
    "pre_algebra": "pa_",
    "algebra_1": "a1_",
    "geometry": "ge_",
    "algebra_2": "a2_",
    "precalculus": "pc_",
    "calculus": "c1_",
}

# Prefer earlier courses when a type_id appears in multiple catalogs.
COURSE_PRIORITY: tuple[str, ...] = (
    "grade_6",
    "pre_algebra",
    "algebra_1",
    "geometry",
    "algebra_2",
    "precalculus",
    "calculus",
)

KNOWN_PREFIXES: tuple[str, ...] = (
    "g6_",
    "pa_",
    "a1_",
    "ge_",
    "a2_",
    "pc_",
    "c1_",
    "c2_",
    "c3_",
)


def has_course_prefix(name: str) -> bool:
    return any(name.startswith(p) for p in KNOWN_PREFIXES)


def type_id_from_folder(folder: str, *, known_ids: frozenset[str] | None = None) -> str:
    """Invert ``gallery_folder_name`` when possible.

    Prefer the folder name itself when it is a registered type_id (e.g. ``g6_foo``).
    Otherwise strip a course prefix and return the remainder if that is a type_id
    (e.g. ``a1_coin_word_problems`` → ``coin_word_problems``).
    """
    if known_ids is not None:
        if folder in known_ids:
            return folder
        for p in KNOWN_PREFIXES:
            if folder.startswith(p):
                rest = folder[len(p) :]
                if rest in known_ids:
                    return rest
        return folder
    # Lazy catalog lookup without requiring QUESTION_TYPES.
    courses = _type_courses()
    if folder in courses:
        return folder
    for p in KNOWN_PREFIXES:
        if folder.startswith(p):
            rest = folder[len(p) :]
            if rest in courses or rest.startswith("calc_"):
                return rest
    if folder.startswith("calc_"):
        return folder
    return folder


@lru_cache(maxsize=1)
def _type_courses() -> dict[str, tuple[str, ...]]:
    from question_engine.catalogs.algebra_1 import CATALOG as A1
    from question_engine.catalogs.algebra_1 import COURSE_ID as A1C
    from question_engine.catalogs.algebra_2 import CATALOG as A2
    from question_engine.catalogs.algebra_2 import COURSE_ID as A2C
    from question_engine.catalogs.calculus import CATALOG as C1
    from question_engine.catalogs.calculus import COURSE_ID as C1C
    from question_engine.catalogs.geometry import CATALOG as GE
    from question_engine.catalogs.geometry import COURSE_ID as GEC
    from question_engine.catalogs.grade_6 import CATALOG as G6
    from question_engine.catalogs.grade_6 import COURSE_ID as G6C
    from question_engine.catalogs.pre_algebra import CATALOG as PA
    from question_engine.catalogs.pre_algebra import COURSE_ID as PAC
    from question_engine.catalogs.precalculus import CATALOG as PC
    from question_engine.catalogs.precalculus import COURSE_ID as PCC

    catalogs: list[tuple[str, Iterable]] = [
        (G6C, G6),
        (PAC, PA),
        (A1C, A1),
        (GEC, GE),
        (A2C, A2),
        (PCC, PC),
        (C1C, C1),
    ]
    out: dict[str, list[str]] = defaultdict(list)
    for course, cat in catalogs:
        for e in cat:
            if course not in out[e.id]:
                out[e.id].append(course)
    return {k: tuple(v) for k, v in out.items()}


def course_prefix_for_type(type_id: str) -> str | None:
    """Return course folder prefix for a type_id, or None if unknown."""
    if has_course_prefix(type_id):
        for p in KNOWN_PREFIXES:
            if type_id.startswith(p):
                return p
    if type_id.startswith("calc_"):
        return "c1_"
    courses = _type_courses().get(type_id, ())
    for c in COURSE_PRIORITY:
        if c in courses:
            return COURSE_PREFIX[c]
    if courses:
        return COURSE_PREFIX[courses[0]]
    return None


def gallery_folder_name(type_id: str) -> str:
    """Folder name under by_topic/ (or one-topic gallery root) for a type_id."""
    if has_course_prefix(type_id):
        return type_id
    pref = course_prefix_for_type(type_id)
    if pref is None:
        return type_id
    return f"{pref}{type_id}"
