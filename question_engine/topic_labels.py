"""Display labels for question type_ids: short course prefix + human name.

Internal type_ids are unchanged. UI / gallery / INDEX surfaces use
``format_topic_label`` → e.g. ``a1: Slope``, ``g6: Decimal addition``.

Prefixes: g6 | pa | a1 | ge | a2 | pc | c1 | c2 | c3
"""

from __future__ import annotations

from typing import Optional

TopicCoursePrefix = str  # g6|pa|a1|ge|a2|pc|c1|c2|c3

_TYPE_ID_PREFIX_TO_COURSE: tuple[tuple[str, str], ...] = (
    ("g6_", "g6"),
    ("pa_", "pa"),
    ("geo_", "ge"),
    ("a2_", "a2"),
    ("pc_", "pc"),
)

_CATEGORY_TO_COURSE: tuple[tuple[str, str], ...] = (
    ("Grade 6", "g6"),
    ("Pre-Algebra", "pa"),
    ("Algebra 1", "a1"),
    ("Geometry", "ge"),
    ("Algebra 2", "a2"),
    ("Precalculus", "pc"),
)

_COURSE_ID_TO_PREFIX: dict[str, str] = {
    "grade_6": "g6",
    "pre_algebra": "pa",
    "algebra_1": "a1",
    "geometry": "ge",
    "algebra_2": "a2",
    "precalculus": "pc",
    "calculus": "c1",  # refined per type_id via calc_volume_prefix
}

# Lazy type_id → catalog COURSE_ID (built once from per-course catalogs).
_TYPE_TO_COURSE_ID: dict[str, str] | None = None


def calc_volume_prefix(type_id: str) -> str:
    """Map calc_* type_ids to c1 / c2 / c3 (OpenStax volumes)."""
    if not type_id.startswith("calc_"):
        return "c1"
    if type_id.startswith("calc_diff_eq_"):
        return "c2"
    if any(
        needle in type_id
        for needle in ("_multivariable", "_vector", "_parametric", "_polar")
    ):
        return "c3"
    return "c1"


def _course_from_category(category: str | None) -> str | None:
    if not category:
        return None
    head = category.split("—", 1)[0].strip()
    for needle, course in _CATEGORY_TO_COURSE:
        if head == needle or head.startswith(needle):
            return course
    if head == "Calculus" or head.startswith("Calculus"):
        return None
    return None


def _ensure_course_map() -> dict[str, str]:
    global _TYPE_TO_COURSE_ID
    if _TYPE_TO_COURSE_ID is not None:
        return _TYPE_TO_COURSE_ID
    mapping: dict[str, str] = {}
    try:
        from .catalogs import (
            algebra_1,
            algebra_2,
            calculus,
            geometry,
            grade_6,
            pre_algebra,
            precalculus,
        )

        for mod in (
            grade_6,
            pre_algebra,
            algebra_1,
            geometry,
            algebra_2,
            precalculus,
            calculus,
        ):
            course_id = getattr(mod, "COURSE_ID", None)
            if not course_id:
                continue
            for entry in getattr(mod, "CATALOG", ()):
                mapping[entry.id] = course_id
    except Exception:  # noqa: BLE001 — labels still work via type_id heuristics
        pass
    _TYPE_TO_COURSE_ID = mapping
    return mapping


def course_prefix_for_type_id(
    type_id: str,
    *,
    category: str | None = None,
    course_id: str | None = None,
) -> str:
    """Map type_id (+ optional catalog category / COURSE_ID) → short course prefix."""
    if type_id.startswith("calc_"):
        return calc_volume_prefix(type_id)

    for prefix, course in _TYPE_ID_PREFIX_TO_COURSE:
        if type_id.startswith(prefix):
            return course

    if course_id and course_id in _COURSE_ID_TO_PREFIX:
        if course_id == "calculus":
            return calc_volume_prefix(type_id)
        return _COURSE_ID_TO_PREFIX[course_id]

    cmap = _ensure_course_map()
    owned = cmap.get(type_id)
    if owned:
        if owned == "calculus":
            return calc_volume_prefix(type_id)
        return _COURSE_ID_TO_PREFIX.get(owned, "a1")

    from_cat = _course_from_category(category)
    if from_cat:
        return from_cat

    return "a1"


def humanize_type_id(type_id: str) -> str:
    """Strip known course prefixes and title-case remaining snake_case."""
    rest = type_id
    for p in ("g6_", "pa_", "geo_", "a2_", "pc_", "calc_"):
        if rest.startswith(p):
            rest = rest[len(p) :]
            break
    words = [w for w in rest.split("_") if w]
    return " ".join(w[:1].upper() + w[1:] for w in words)


def format_topic_label(
    type_id: str,
    name: Optional[str] = None,
    *,
    category: str | None = None,
    course_id: str | None = None,
) -> str:
    """Return ``{prefix}: {Name}`` — e.g. ``g6: Introduction to ratios``."""
    prefix = course_prefix_for_type_id(
        type_id, category=category, course_id=course_id
    )
    raw = (name or "").strip()
    looks_like_id = bool(raw) and raw.replace("_", "").isalnum() and "_" in raw
    if raw and raw != type_id and not looks_like_id:
        title = raw
    else:
        title = humanize_type_id(type_id)
    return f"{prefix}: {title}"
