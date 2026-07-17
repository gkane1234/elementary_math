"""Export a curriculum-facing prerequisite index for the topic picker UI.

Writes lib/data/prerequisite-index.json keyed by courseId:chapterId (chapter overview)
and courseId:chapterId:topicId (topic/leaf skill deps from topic_leaves.json).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.example_mining.progression import (  # noqa: E402
    build_book_progression,
    build_foundations_progression,
    build_geometry_progression,
    build_grade_6_progression,
)
from scripts.example_mining.prerequisite_loader import (  # noqa: E402
    build_prerequisite_edges,
    full_node_id,
    load_prerequisite_map,
    split_full_node_id,
)

HTML_ROOT = ROOT / "textbooks" / "openstax" / "html"
OUT_PATH = ROOT / "lib" / "data" / "prerequisite-index.json"
TOPIC_LEAVES_PATH = (
    ROOT / "scripts" / "example_mining" / "prerequisites" / "topic_leaves.json"
)
CURRICULUM_PATH = ROOT / "lib" / "curriculum.ts"

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

# Graph book → curriculum course id
BOOK_TO_COURSE = {
    "foundations_math": "foundations_math",
    "grade_6_math": "grade_6_math",
    "geometry": "geometry",
    "prealgebra-2e": "pre_algebra",
    "elementary-algebra-2e": "algebra_1",
    "intermediate-algebra-2e": "algebra_2",
    "precalculus-2e": "precalculus",
    "calculus-volume-1": "calculus",
    "calculus-volume-2": "calculus",
    "calculus-volume-3": "calculus",
}

# OpenStax chapter number → curriculum chapter id (best-effort)
OPENSTAX_CHAPTER_MAP: dict[str, dict[int, str]] = {
    "prealgebra-2e": {
        2: "the_language_of_algebra",
        3: "integers",
        4: "fractions",
        5: "decimals",
        6: "percents",
        7: "factors_and_exponents",
        8: "solving_linear_equations",
        9: "math_models_and_geometry",
        10: "polynomials",
        11: "graphs",
    },
    "elementary-algebra-2e": {
        2: "solving_linear_equations_and_inequalities",
        3: "math_models",
        4: "graphs",
        5: "systems_of_linear_equations",
        6: "polynomials",
        7: "factoring",
        8: "rational_expressions_and_equations",
        9: "roots_and_radicals",
        10: "quadratic_equations",
    },
    "intermediate-algebra-2e": {
        2: "solving_linear_equations_and_inequalities",
        3: "graphs_and_functions",
        4: "systems_of_linear_equations",
        5: "polynomials_and_polynomial_functions",
        6: "factoring",
        7: "rational_expressions_and_functions",
        8: "roots_and_radicals",
        9: "quadratic_equations_and_functions",
        10: "exponential_and_logarithmic_functions",
        11: "conics",
        12: "sequences_series_and_the_binomial_theorem",
    },
    "precalculus-2e": {
        1: "functions",
        2: "functions",
        3: "polynomial_and_rational_functions",
        4: "exponential_and_logarithmic_functions",
        5: "trigonometric_functions",
        6: "periodic_functions",
        7: "trigonometric_identities_and_equations",
        8: "further_applications_of_trigonometry",
        9: "systems_of_equations_and_inequalities",
        10: "analytic_geometry",
        11: "sequences_probability_and_counting_theory",
        12: "introduction_to_calculus",
    },
    "calculus-volume-1": {
        2: "limits",
        3: "derivatives",
        4: "applications_of_derivatives",
        5: "integration",
        6: "applications_of_integration",
    },
    "calculus-volume-2": {
        1: "integration",
        2: "applications_of_integration",
        3: "integration",
        4: "differential_equations",
        5: "differential_equations",
        6: "differential_equations",
        7: "differential_equations",
    },
    "calculus-volume-3": {
        1: "differential_equations",
        2: "differential_equations",
        3: "differential_equations",
        4: "differential_equations",
        5: "differential_equations",
        6: "differential_equations",
        7: "differential_equations",
    },
}

CURRICULUM_UNIT_BOOKS = {"foundations_math", "grade_6_math", "geometry"}


def _parse_curriculum_by_type_id(src: str) -> dict[str, dict[str, str]]:
    """Map type_id → {courseId, chapterId, topicId, title} from lib/curriculum.ts."""
    by_type: dict[str, dict[str, str]] = {}
    course_id: str | None = None
    chapter_id: str | None = None
    chapter_name: str | None = None

    # Course block: id: "calculus", name: "Calculus",
    course_re = re.compile(
        rf'id:\s*"({"|".join(COURSE_IDS)})"\s*,\s*\n\s*name:\s*"([^"]+)"'
    )
    # Chapter: id + name followed by topics: [
    chapter_re = re.compile(
        r'\{\s*id:\s*"([^"]+)"\s*,\s*name:\s*"([^"]+)"\s*,\s*topics:\s*\['
    )
    # Leaf with type_id
    leaf_re = re.compile(
        r'\{\s*id:\s*"([^"]+)"\s*,\s*name:\s*"([^"]+)"\s*,\s*type_id:\s*"([^"]+)"\s*\}'
    )

    events: list[tuple[int, str, tuple]] = []
    for m in course_re.finditer(src):
        events.append((m.start(), "course", (m.group(1), m.group(2))))
    for m in chapter_re.finditer(src):
        events.append((m.start(), "chapter", (m.group(1), m.group(2))))
    for m in leaf_re.finditer(src):
        events.append((m.start(), "leaf", (m.group(1), m.group(2), m.group(3))))
    events.sort(key=lambda e: e[0])

    for _start, kind, payload in events:
        if kind == "course":
            course_id = payload[0]
            chapter_id = None
            chapter_name = None
        elif kind == "chapter":
            chapter_id, chapter_name = payload
        elif kind == "leaf" and course_id and chapter_id:
            topic_id, title, type_id = payload
            # Prefer first curriculum placement for a type_id.
            by_type.setdefault(
                type_id,
                {
                    "courseId": course_id,
                    "chapterId": chapter_id,
                    "topicId": topic_id,
                    "title": title,
                    "chapterTitle": chapter_name or chapter_id,
                },
            )
    return by_type


def _load_topic_leaves() -> dict[str, dict]:
    if not TOPIC_LEAVES_PATH.is_file():
        return {}
    raw = json.loads(TOPIC_LEAVES_PATH.read_text(encoding="utf-8"))
    return {k: v for k, v in raw.items() if not k.startswith("_") and isinstance(v, dict)}


def _load_progs():
    books = [
        "foundations_math",
        "grade_6_math",
        "prealgebra-2e",
        "elementary-algebra-2e",
        "geometry",
        "intermediate-algebra-2e",
        "precalculus-2e",
        "calculus-volume-1",
        "calculus-volume-2",
        "calculus-volume-3",
    ]
    progs = []
    for book in books:
        if book == "foundations_math":
            progs.append(build_foundations_progression())
        elif book == "grade_6_math":
            progs.append(build_grade_6_progression())
        elif book == "geometry":
            progs.append(build_geometry_progression())
        elif (HTML_ROOT / book).is_dir():
            progs.append(build_book_progression(book, book, HTML_ROOT))
    return progs


def _browser_key_for_node(book: str, node_id: str, chapter: int | None) -> str | None:
    course = BOOK_TO_COURSE.get(book)
    if not course:
        return None
    if book in CURRICULUM_UNIT_BOOKS:
        return f"{course}:{node_id}"
    if chapter is None:
        return None
    chap = OPENSTAX_CHAPTER_MAP.get(book, {}).get(chapter)
    if not chap:
        return None
    return f"{course}:{chap}"


def main() -> int:
    progs = _load_progs()
    lookup = {}
    for prog in progs:
        for n in prog.nodes:
            lookup[full_node_id(prog.book, n.node_id)] = n

    maps = {}
    for prog in progs:
        m = load_prerequisite_map(prog.book)
        if m:
            maps[prog.book] = m
    edges, reasons = build_prerequisite_edges(maps)

    # Aggregate graph edges onto curriculum chapter keys.
    chapter_requires: dict[str, set[str]] = {}
    chapter_titles: dict[str, str] = {}
    chapter_reasons: dict[str, str] = {}

    for full_id, node in lookup.items():
        key = _browser_key_for_node(node.book, node.node_id, node.chapter)
        if key:
            chapter_titles.setdefault(key, node.title)

    for prereq, dependent in edges:
        dep_node = lookup.get(dependent)
        pre_node = lookup.get(prereq)
        if not dep_node or not pre_node:
            continue
        dep_key = _browser_key_for_node(dep_node.book, dep_node.node_id, dep_node.chapter)
        pre_key = _browser_key_for_node(pre_node.book, pre_node.node_id, pre_node.chapter)
        if not dep_key or not pre_key or dep_key == pre_key:
            continue
        chapter_requires.setdefault(dep_key, set()).add(pre_key)
        if dependent in reasons and dep_key not in chapter_reasons:
            chapter_reasons[dep_key] = reasons[dependent]

    # Direct unit maps already use curriculum keys; prefer their reasons.
    for book, book_map in maps.items():
        if book not in CURRICULUM_UNIT_BOOKS:
            continue
        for dependent, entry in book_map.items():
            _b, node_id = split_full_node_id(dependent)
            key = f"{BOOK_TO_COURSE[book]}:{node_id}"
            chapter_requires.setdefault(key, set())
            for req in entry.requires:
                _rb, rid = split_full_node_id(req)
                rcourse = BOOK_TO_COURSE.get(_rb)
                if not rcourse:
                    continue
                if _rb in CURRICULUM_UNIT_BOOKS:
                    chapter_requires[key].add(f"{rcourse}:{rid}")
                else:
                    rn = lookup.get(req)
                    if rn:
                        rk = _browser_key_for_node(rn.book, rn.node_id, rn.chapter)
                        if rk:
                            chapter_requires[key].add(rk)
            if entry.reason:
                chapter_reasons[key] = entry.reason
            if dependent in lookup:
                chapter_titles[key] = lookup[dependent].title

    entries = {}
    for key, reqs in sorted(chapter_requires.items()):
        course_id, chapter_id = key.split(":", 1)
        requires = []
        for rk in sorted(reqs):
            rc, rch = rk.split(":", 1)
            requires.append(
                {
                    "key": rk,
                    "courseId": rc,
                    "chapterId": rch,
                    "title": chapter_titles.get(rk, rch.replace("_", " ").title()),
                }
            )
        entries[key] = {
            "key": key,
            "courseId": course_id,
            "chapterId": chapter_id,
            "title": chapter_titles.get(key, chapter_id.replace("_", " ").title()),
            "reason": chapter_reasons.get(key, ""),
            "requires": requires,
        }

    # Also expose graph-node → curriculum key for debugging / future leaf maps.
    node_to_key = {}
    for full_id, node in lookup.items():
        key = _browser_key_for_node(node.book, node.node_id, node.chapter)
        if key:
            node_to_key[full_id] = key

    # Topic/leaf skill deps (intra-chapter) authored in topic_leaves.json.
    curriculum_src = CURRICULUM_PATH.read_text(encoding="utf-8")
    by_type = _parse_curriculum_by_type_id(curriculum_src)
    topic_leaves = _load_topic_leaves()
    topic_entries: dict[str, dict] = {}
    type_to_topic_key: dict[str, str] = {}
    leaf_warnings: list[str] = []

    for type_id, leaf in topic_leaves.items():
        loc = by_type.get(type_id)
        if not loc:
            leaf_warnings.append(f"Unknown type_id in topic_leaves: {type_id}")
            continue
        key = f"{loc['courseId']}:{loc['chapterId']}:{loc['topicId']}"
        type_to_topic_key[type_id] = key
        requires_refs = []
        for req_type in leaf.get("requires", []):
            req_loc = by_type.get(req_type)
            if not req_loc:
                leaf_warnings.append(
                    f"{type_id} references unknown prerequisite type_id: {req_type}"
                )
                continue
            rk = f"{req_loc['courseId']}:{req_loc['chapterId']}:{req_loc['topicId']}"
            requires_refs.append(
                {
                    "key": rk,
                    "courseId": req_loc["courseId"],
                    "chapterId": req_loc["chapterId"],
                    "topicId": req_loc["topicId"],
                    "typeId": req_type,
                    "title": req_loc["title"],
                }
            )
        topic_entries[key] = {
            "key": key,
            "courseId": loc["courseId"],
            "chapterId": loc["chapterId"],
            "topicId": loc["topicId"],
            "typeId": type_id,
            "title": loc["title"],
            "reason": str(leaf.get("reason", "")),
            "requires": requires_refs,
        }

    payload = {
        "version": 2,
        "entries": entries,
        "topicEntries": topic_entries,
        "typeIdToTopicKey": type_to_topic_key,
        "nodeToCurriculumKey": node_to_key,
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        f"Wrote {OUT_PATH.relative_to(ROOT)} "
        f"({len(entries)} chapter entries, {len(topic_entries)} topic entries)"
    )
    for warning in leaf_warnings:
        print(f"  warning: {warning}")
    return 1 if leaf_warnings else 0


if __name__ == "__main__":
    raise SystemExit(main())
