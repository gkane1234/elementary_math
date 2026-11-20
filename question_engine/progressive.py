"""Progressive practice worksheets: coherent topic selection + global D ramp.

Given seed type_id(s), expand to a small related set (same catalog family /
curriculum neighbors, topic_leaves prereqs & immediate postreqs), then assign
each question an increasing continuous ``difficulty`` while rotating topics with
an early bias toward prerequisites.
"""

from __future__ import annotations

import json
from functools import lru_cache
from math import ceil
from pathlib import Path
from typing import Any

from .core.base import QUESTION_TYPES
from .core.registry import TYPE_CATALOG, get_catalog_entry
from .type_readiness import type_not_ready

CONTINUOUS_FIELD_TYPES = frozenset({"int", "float", "number", "range"})

_TOPIC_LEAVES_PATH = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "example_mining"
    / "prerequisites"
    / "topic_leaves.json"
)


def has_continuous_difficulty(type_id: str) -> bool:
    """True when the type schema exposes a numeric continuous ``difficulty`` knob."""
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
        return getattr(field, "type", None) in CONTINUOUS_FIELD_TYPES
    return False


def _eligible(type_id: str, *, continuous_only: bool) -> bool:
    if type_id not in QUESTION_TYPES:
        return False
    if type_not_ready(type_id):
        return False
    if continuous_only and not has_continuous_difficulty(type_id):
        return False
    return True


@lru_cache(maxsize=1)
def _topic_leaf_edges() -> tuple[dict[str, tuple[str, ...]], dict[str, tuple[str, ...]]]:
    """Return (prereqs_by_type, postreqs_by_type) from topic_leaves.json."""
    prereqs: dict[str, tuple[str, ...]] = {}
    postreqs: dict[str, list[str]] = {}
    if not _TOPIC_LEAVES_PATH.is_file():
        return prereqs, {k: tuple(v) for k, v in postreqs.items()}
    raw = json.loads(_TOPIC_LEAVES_PATH.read_text(encoding="utf-8"))
    for key, value in raw.items():
        if key.startswith("_") or not isinstance(value, dict):
            continue
        reqs = value.get("requires") or []
        if not isinstance(reqs, list):
            continue
        cleaned = tuple(str(r) for r in reqs if isinstance(r, str) and r)
        prereqs[str(key)] = cleaned
        for req in cleaned:
            postreqs.setdefault(req, []).append(str(key))
    return prereqs, {k: tuple(v) for k, v in postreqs.items()}


@lru_cache(maxsize=1)
def _category_members() -> dict[str, tuple[str, ...]]:
    """Ordered type_ids grouped by catalog category (chapter/family)."""
    by_cat: dict[str, list[str]] = {}
    for entry in TYPE_CATALOG:
        by_cat.setdefault(entry.category, []).append(entry.id)
    return {cat: tuple(ids) for cat, ids in by_cat.items()}


_AFFINITY_KEYWORDS = (
    "ratio",
    "rate",
    "percent",
    "fraction",
    "decimal",
    "integer",
    "equation",
    "inequalit",
    "exponent",
    "polynomial",
    "radical",
    "trig",
    "limit",
    "derivative",
    "integral",
)


def _keyword_tokens(type_id: str) -> set[str]:
    return {k for k in _AFFINITY_KEYWORDS if k in type_id}


def _affinity_score(seed: str, other: str) -> int:
    """Higher = more related by shared skill keywords in the type_id."""
    return len(_keyword_tokens(seed) & _keyword_tokens(other))


def _family_neighbors(type_id: str, *, radius: int = 3) -> list[str]:
    """Same-category neighbors within ``radius`` index steps (closest first).

    When keyword affinity differs, prefer neighbors that share skill keywords
    with the seed (e.g. fraction seeds prefer ``*_fraction_*`` over LCM/GCF).
    """
    try:
        entry = get_catalog_entry(type_id)
    except KeyError:
        return []
    members = _category_members().get(entry.category, ())
    if type_id not in members:
        return []
    idx = members.index(type_id)
    ordered: list[str] = []
    for dist in range(1, radius + 1):
        for pos in (idx - dist, idx + dist):
            if 0 <= pos < len(members):
                ordered.append(members[pos])
    ordered.sort(
        key=lambda tid: (
            -_affinity_score(type_id, tid),
            abs(members.index(tid) - idx),
        )
    )
    return ordered


def _direct_prereqs(type_id: str) -> list[str]:
    prereqs, _ = _topic_leaf_edges()
    return list(prereqs.get(type_id, ()))


def _direct_postreqs(type_id: str) -> list[str]:
    _, postreqs = _topic_leaf_edges()
    return list(postreqs.get(type_id, ()))


def _curriculum_rank(type_id: str) -> tuple[int, int]:
    """Stable sort key: catalog order (earlier = prerequisite-leaning)."""
    for i, entry in enumerate(TYPE_CATALOG):
        if entry.id == type_id:
            return (0, i)
    return (1, 0)


def select_coherent_topics(
    seed: str | list[str] | tuple[str, ...] | None = None,
    n: int = 4,
    *,
    seeds: list[str] | None = None,
    continuous_only: bool = True,
    include_related: bool = True,
) -> list[str]:
    """Expand seed type_id(s) to a coherent set of up to ``n`` continuous-ready topics.

    Selection order preference:
    1. Eligible seeds (as given)
    2. Direct topic_leaves prerequisites (curriculum-earlier first)
    3. Same-family catalog neighbors (closest first)
    4. Immediate topic_leaves postrequisites

    Types lacking continuous difficulty are skipped when ``continuous_only`` is True.
    """
    if n < 1:
        return []

    raw_seeds: list[str] = []
    if seeds:
        raw_seeds.extend(str(s) for s in seeds if s)
    if seed is not None:
        if isinstance(seed, (list, tuple)):
            raw_seeds.extend(str(s) for s in seed if s)
        elif str(seed).strip():
            raw_seeds.append(str(seed).strip())

    # Dedupe preserving order.
    seen: set[str] = set()
    seed_list: list[str] = []
    for tid in raw_seeds:
        if tid in seen:
            continue
        seen.add(tid)
        seed_list.append(tid)

    eligible_seeds = [tid for tid in seed_list if _eligible(tid, continuous_only=continuous_only)]
    if not eligible_seeds and seed_list:
        # Fall back: if seeds exist but none continuous, still try non-continuous
        # only when continuous_only is False; otherwise return empty.
        if continuous_only:
            return []
        eligible_seeds = [tid for tid in seed_list if tid in QUESTION_TYPES]

    if not include_related:
        return eligible_seeds[:n]

    # Gather related candidates; final order is prereqs → seeds → neighbors → postreqs.
    prereq_bucket: list[str] = []
    neighbor_bucket: list[str] = []
    postreq_bucket: list[str] = []
    seen_cand: set[str] = set(eligible_seeds)

    for tid in eligible_seeds:
        for req in _direct_prereqs(tid):
            if req not in seen_cand:
                seen_cand.add(req)
                prereq_bucket.append(req)
        for neigh in _family_neighbors(tid):
            if neigh not in seen_cand:
                seen_cand.add(neigh)
                neighbor_bucket.append(neigh)
        for post in _direct_postreqs(tid):
            if post not in seen_cand:
                seen_cand.add(post)
                postreq_bucket.append(post)

    prereq_bucket.sort(key=_curriculum_rank)

    selected: list[str] = []
    selected_set: set[str] = set()

    def _add(tid: str) -> bool:
        if tid in selected_set:
            return False
        if not _eligible(tid, continuous_only=continuous_only):
            return False
        selected.append(tid)
        selected_set.add(tid)
        return len(selected) >= n

    for tid in prereq_bucket + eligible_seeds + neighbor_bucket + postreq_bucket:
        if _add(tid):
            return selected

    # If still short, widen to full same-category membership (catalog order).
    if len(selected) < n:
        for tid in eligible_seeds:
            try:
                entry = get_catalog_entry(tid)
            except KeyError:
                continue
            for member in _category_members().get(entry.category, ()):
                if _add(member):
                    return selected

    return selected


def difficulty_ramp(count: int, d_min: float = 0.0, d_max: float = 18.0) -> list[float]:
    """Monotone non-decreasing difficulties from d_min → d_max across ``count`` slots."""
    if count < 1:
        return []
    lo = float(d_min)
    hi = float(d_max)
    if count == 1:
        return [lo]
    if hi < lo:
        lo, hi = hi, lo
    return [lo + (hi - lo) * (i / (count - 1)) for i in range(count)]


def assign_progressive_slots(
    topics: list[str],
    count: int,
    *,
    d_min: float = 0.0,
    d_max: float = 18.0,
) -> list[dict[str, Any]]:
    """Global D ramp with early bias toward earlier (prereq-leaning) topics.

    Question ``i`` of ``N`` gets ``D = lerp(d_min, d_max, i/(N-1))``. Topic is
    chosen from the prefix of ``topics`` that grows with ``i`` (earlier questions
    stick to earlier/prereq topics), round-robin within that prefix.
    """
    if not topics or count < 1:
        return []
    difficulties = difficulty_ramp(count, d_min, d_max)
    slots: list[dict[str, Any]] = []
    for i, d in enumerate(difficulties):
        prefix_len = max(1, min(len(topics), ceil((i + 1) / count * len(topics))))
        prefix = topics[:prefix_len]
        type_id = prefix[i % len(prefix)]
        slots.append({"type_id": type_id, "difficulty": round(d, 4), "index": i})
    return slots


def _section_question_count(section: dict[str, Any], settings: dict[str, Any]) -> int:
    raw = section.get("count", settings.get("count", 1))
    try:
        count = int(raw)
    except (TypeError, ValueError):
        return 1
    return max(count, 1)


def assign_slot_seeds(sections: list[dict[str, Any]]) -> None:
    """Give each section a distinct seed when they all share one worksheet seed.

    Gallery and progressive requests copy one ``seed`` onto every section, and
    each section is generated with ``count=1``. ``apply_batch_seed`` then does
    ``random.seed(seed + batch_index * 1009)`` with ``batch_index`` 0, so every
    slot replays the same draw.

    Question ``k`` (across sections, not just the section index) receives
    ``mix_batch_seed(seed, k)``, the same mix a count=N batch already uses.
    The first question keeps the worksheet seed. A single section is unchanged,
    so a count=N generate still varies inside ``apply_batch_seed``. Sections
    that already carry distinct seeds are unchanged, so saving those sections
    and generating again replays the same worksheet.
    """
    if not isinstance(sections, list) or len(sections) < 2:
        return
    parsed: list[tuple[dict[str, Any], dict[str, Any], int, int]] = []
    for section in sections:
        if not isinstance(section, dict):
            return
        settings = section.get("settings")
        if not isinstance(settings, dict) or "seed" not in settings:
            return
        try:
            seed = int(settings["seed"])
        except (TypeError, ValueError):
            return
        parsed.append((section, settings, seed, _section_question_count(section, settings)))
    if len({seed for _, _, seed, _ in parsed}) != 1:
        return
    from .diagrams.figure_families import mix_batch_seed

    base = parsed[0][2]
    cursor = 0
    for section, settings, _seed, count in parsed:
        if cursor:
            updated = dict(settings)
            updated["seed"] = mix_batch_seed(base, cursor)
            section["settings"] = updated
        cursor += count


def _checked_topics(topics: Any) -> list[str] | None:
    """``None`` when the caller did not send a topic list. Empty stays empty."""
    if topics is None:
        return None
    if isinstance(topics, str):
        text = topics.strip()
        return [text] if text else []
    if not isinstance(topics, list):
        return None
    return [str(item) for item in topics if item]


def _choice(value: Any, allowed: frozenset[str], default: str) -> str:
    text = str(value or "").strip().lower()
    return text if text in allowed else default


def _placed_topics(slots: list[dict[str, Any]], phase: str) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for slot in slots:
        if slot.get("phase") != phase:
            continue
        type_id = str(slot.get("type_id") or "")
        if not type_id or type_id in seen:
            continue
        seen.add(type_id)
        out.append(type_id)
    return out


def _sections_from_slots(
    slots: list[dict[str, Any]],
    base_settings: dict[str, Any] | None,
) -> list[dict[str, Any]]:
    base = dict(base_settings or {})
    sections: list[dict[str, Any]] = []
    for slot in slots:
        settings = {**base, "difficulty": slot["difficulty"], "count": 1}
        sections.append(
            {
                "type_id": slot["type_id"],
                "count": 1,
                "settings": settings,
            }
        )
    # Each section is generated with count=1, so apply_batch_seed would otherwise
    # replay batch index 0 for every slot that shares this worksheet seed.
    assign_slot_seeds(sections)
    return sections


def build_progressive_sections(
    *,
    seeds: list[str] | None = None,
    seed: str | None = None,
    count: int = 10,
    d_min: float = 0.0,
    d_max: float = 18.0,
    include_related: bool = True,
    max_topics: int = 4,
    continuous_only: bool = True,
    base_settings: dict[str, Any] | None = None,
    pairing: str = "lesson",
    scope: str = "topic",
    topics: list[str] | None = None,
    style: str = "ramp",
    ramp_each_topic: bool = False,
) -> dict[str, Any]:
    """Build count=1 sections with rising D for ``handle_generate``.

    Grade 6 and Geometry seeds use ``plan_topics_for_seeds``
    (``grade_6.plan_topics`` / ``geometry.plan_topics``): lesson order, an
    optional procedure-drill block, and a follow-on skill. Calls that omit
    ``pairing``, ``scope``, and ``style`` still default to lesson + ramp +
    scope ``topic``. Every other course keeps ``select_coherent_topics``.

    Returns ``{topics, slots, sections, plan}``.
    """
    from question_engine.worksheet_courses.base import (
        assign_template_slots,
        plan_topics_for_seeds,
    )

    pairing = _choice(pairing, frozenset({"lesson", "drill", "spiral"}), "lesson")
    scope = _choice(scope, frozenset({"topic", "unit", "adjacent"}), "topic")
    style = _choice(style, frozenset({"ramp", "straight"}), "ramp")
    checked = _checked_topics(topics)
    cap = max(1, int(max_topics))

    raw_seeds: list[str] = []
    if seeds:
        raw_seeds.extend(str(item) for item in seeds if item)
    if seed is not None and str(seed).strip():
        raw_seeds.append(str(seed).strip())

    course_plan = plan_topics_for_seeds(
        raw_seeds,
        pairing=pairing,
        scope=scope,
        topics=checked,
        max_topics=cap,
        include_related=include_related,
    )

    if course_plan is None:
        selected = select_coherent_topics(
            seed,
            cap,
            seeds=seeds,
            continuous_only=continuous_only,
            include_related=include_related,
        )
        if not selected:
            raise ValueError(
                "No continuous-difficulty topics available for the given seed(s). "
                "Pick a type with a numeric difficulty setting."
            )
        slots = assign_progressive_slots(selected, int(count), d_min=d_min, d_max=d_max)
        for slot in slots:
            slot.setdefault("phase", "focus")
        omitted: list[str] = []
        spiral_suggestion = None
        course_id = None
        focus = list(selected)
        warmup: list[str] = []
        drill: list[str] = []
        stretch: list[str] = []
    else:
        if not course_plan.get("focus"):
            raise ValueError(
                "No continuous-difficulty topics available for the given seed(s). "
                "Pick a type with a numeric difficulty setting."
            )
        slots, omitted = assign_template_slots(
            course_plan,
            int(count),
            d_min=d_min,
            d_max=d_max,
            style=style,
            ramp_each_topic=bool(ramp_each_topic),
        )
        if not slots and int(count) > 0:
            raise ValueError(
                "No continuous-difficulty topics available for the given seed(s). "
                "Pick a type with a numeric difficulty setting."
            )
        selected = []
        seen_topics: set[str] = set()
        for slot in slots:
            type_id = slot["type_id"]
            if type_id not in seen_topics:
                seen_topics.add(type_id)
                selected.append(type_id)
        spiral_suggestion = course_plan.get("spiral_suggestion")
        course_id = course_plan.get("course_id")
        focus = _placed_topics(slots, "focus")
        warmup = _placed_topics(slots, "warmup")
        drill = _placed_topics(slots, "drill")
        stretch = _placed_topics(slots, "stretch")

    sections = _sections_from_slots(slots, base_settings)
    difficulties = [slot["difficulty"] for slot in slots]
    phases = [slot.get("phase", "focus") for slot in slots]
    return {
        "topics": selected,
        "slots": slots,
        "sections": sections,
        "plan": {
            "seeds": seeds or ([seed] if seed else []),
            "count": int(count),
            "d_min": float(d_min),
            "d_max": float(d_max),
            "include_related": bool(include_related),
            "max_topics": int(max_topics),
            "topics": selected,
            "difficulties": difficulties,
            "pairing": pairing,
            "scope": scope,
            "style": style,
            "ramp_each_topic": bool(ramp_each_topic),
            "checked_topics": list(checked or []),
            "phases": phases,
            "omitted_topics": list(omitted),
            "focus": focus,
            "warmup": warmup,
            "drill": drill,
            "stretch": stretch,
            "spiral_suggestion": spiral_suggestion,
            "course_id": course_id,
        },
    }


def parse_progressive_body(progressive: dict[str, Any]) -> dict[str, Any]:
    """Normalize a ``progressive`` request dict into ``build_progressive_sections`` kwargs."""
    from question_engine.worksheet_difficulty import apply_worksheet_difficulty

    # Worksheet-level difficulty fills d_min/d_max when provided.
    progressive = apply_worksheet_difficulty(progressive)

    seeds_raw = progressive.get("seeds")
    seeds: list[str] | None = None
    if isinstance(seeds_raw, list):
        seeds = [str(s) for s in seeds_raw if s]
    elif isinstance(seeds_raw, str) and seeds_raw.strip():
        seeds = [seeds_raw.strip()]

    seed = progressive.get("seed")
    if seed is not None:
        seed = str(seed).strip() or None

    if "topics" in progressive and progressive.get("topics") is not None:
        checked = _checked_topics(progressive.get("topics"))
    else:
        checked = None

    return {
        "seeds": seeds,
        "seed": seed,
        "count": int(progressive.get("count", 10)),
        "d_min": float(progressive.get("d_min", 0)),
        "d_max": float(progressive.get("d_max", 18)),
        "include_related": bool(progressive.get("include_related", True)),
        "max_topics": int(progressive.get("max_topics", 4)),
        "continuous_only": bool(progressive.get("continuous_only", True)),
        "base_settings": dict(progressive.get("base_settings") or {}),
        "pairing": _choice(
            progressive.get("pairing", "lesson"),
            frozenset({"lesson", "drill", "spiral"}),
            "lesson",
        ),
        "scope": _choice(
            progressive.get("scope", "topic"),
            frozenset({"topic", "unit", "adjacent"}),
            "topic",
        ),
        "topics": checked,
        "style": _choice(
            progressive.get("style", "ramp"),
            frozenset({"ramp", "straight"}),
            "ramp",
        ),
        "ramp_each_topic": bool(progressive.get("ramp_each_topic", False)),
    }
