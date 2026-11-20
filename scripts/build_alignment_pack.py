"""Representative published problems vs what we generate, for every wired topic.

For each curriculum leaf with a type_id this writes an HTML review pack:

  scripts/output/alignment_pack/index.html

Each topic gets two generated items at easy, medium, and hard, next to a
small published ladder (or a task set, when the source has no ladder).
OpenStax and Illustrative Mathematics / Open Up text is quoted with attribution.
Figure stems include the source image. Anything not under an open license
is not copied.

Usage:
  QE_LOG_GENERATED=0 PYTHONPATH=. python scripts/build_alignment_pack.py
  QE_LOG_GENERATED=0 PYTHONPATH=. python scripts/build_alignment_pack.py --only g6_equations_hanger_diagrams,quadratic_factoring
  QE_LOG_GENERATED=0 PYTHONPATH=. python scripts/build_alignment_pack.py --phase match
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.alignment_skill import (  # noqa: E402
    filename_score,
    in_topic_not_generated,
    item_matches,
    section_slug_score,
    skill_profile,
)
from scripts.example_mining.openstax_html_parse import parse_section_html  # noqa: E402
from scripts.mirror_openstax import discover_slugs  # noqa: E402

OUT = ROOT / "scripts" / "output" / "alignment_pack"
CACHE = ROOT / "textbooks" / "alignment_cache"
ASSETS = OUT / "assets"
GEN_DIR = ASSETS / "gen"
IMG_DIR = ASSETS / "img"

CONSULTED = "2026-11-19"
TIERS = ("easy", "medium", "hard")
SEEDS = (101, 207)
WAIT = 0.35

UA_OPENSTAX = "PolynomialLocalMirror/1.0 (+local research; polite crawl)"
UA_BROWSER = "Mozilla/5.0 (compatible; PolynomialAlignment/1.0; research)"

BOOKS_FOR_COURSE = {
    "grade_6_math": ["prealgebra-2e", "elementary-algebra-2e"],
    "pre_algebra": ["prealgebra-2e", "elementary-algebra-2e"],
    "algebra_1": ["elementary-algebra-2e", "intermediate-algebra-2e", "prealgebra-2e"],
    "algebra_2": ["intermediate-algebra-2e", "precalculus-2e", "elementary-algebra-2e"],
    "geometry": ["elementary-algebra-2e", "prealgebra-2e", "precalculus-2e"],
    "precalculus": ["precalculus-2e", "calculus-volume-1", "intermediate-algebra-2e"],
    "calculus": ["calculus-volume-1", "calculus-volume-2", "calculus-volume-3", "precalculus-2e"],
}

BOOK_TITLE = {
    "prealgebra-2e": "OpenStax Prealgebra 2e",
    "elementary-algebra-2e": "OpenStax Elementary Algebra 2e",
    "intermediate-algebra-2e": "OpenStax Intermediate Algebra 2e",
    "precalculus-2e": "OpenStax Precalculus 2e",
    "calculus-volume-1": "OpenStax Calculus Volume 1",
    "calculus-volume-2": "OpenStax Calculus Volume 2",
    "calculus-volume-3": "OpenStax Calculus Volume 3",
}

OPENSTAX_LICENSE = "CC BY-NC-SA 4.0"
OUR_LICENSE = "CC BY 4.0 (Open Up Resources and Illustrative Mathematics)"
IM_LICENSE = "CC BY-NC-SA 4.0 (Illustrative Mathematics)"

# Explicit section pins where the slug does not share the leaf's words.
# Values are (book, slug-substring) in easy-to-hard section order.
OPENSTAX_PINS: list[tuple[str, str, list[tuple[str, str]]]] = [
    (r"one_step_equation", "*", [
        ("prealgebra-2e", "8-1-solve-equations-using-the-subtraction"),
        ("prealgebra-2e", "8-2-solve-equations-using-the-division"),
    ]),
    (r"two_step_equation|multi_step_equation", "pre_algebra", [
        ("prealgebra-2e", "8-3-solve-equations-with-variables"),
    ]),
    (r"verbal_expression|translate", "pre_algebra", [
        ("prealgebra-2e", "2-2-evaluate-simplify-and-translate"),
    ]),
    (r"absolute_value_inequal", "*", [
        ("intermediate-algebra-2e", "2-7-solve-absolute-value-inequalities"),
    ]),
    (r"unit_rate|comparing_rates|converting_units", "*", [
        ("prealgebra-2e", "5-6-ratios-and-rate"),
        ("prealgebra-2e", "6-5-solve-proportions"),
    ]),
    (r"introduction_to_ratios|equivalent_ratios|part_part_whole|comparing_ratios", "*", [
        ("prealgebra-2e", "5-6-ratios-and-rate"),
    ]),
    (r"percent", "pre_algebra", [
        ("prealgebra-2e", "6-1-understand-percent"),
        ("prealgebra-2e", "6-2-solve-general-applications-of-percent"),
    ]),
    (r"gcf|greatest_common|lcm|least_common|g6_factoring", "*", [
        ("prealgebra-2e", "2-4-find-multiples-and-factors"),
        ("prealgebra-2e", "2-5-prime-factorization"),
    ]),
    (r"permutation|combination", "*", [
        ("precalculus-2e", "11-5-counting-principles"),
        ("precalculus-2e", "11-7-probability"),
    ]),
    (r"probability", "geometry", [
        ("precalculus-2e", "11-7-probability"),
    ]),
    (r"pythagorean", "*", [
        ("prealgebra-2e", "9-3-use-properties-of-angles-triangles-and-the-pythagorean"),
        ("elementary-algebra-2e", "3-4-solve-geometry-applications-triangles"),
    ]),
    (r"circumference|area_of_circles|equations_of_circles|writing_equations_of_circles", "geometry", [
        ("prealgebra-2e", "9-5-solve-geometry-applications-circles"),
    ]),
    (r"volume|surface_area|solid_figure|similar_solids", "geometry", [
        ("prealgebra-2e", "9-6-solve-geometry-applications-volume"),
    ]),
    (r"distance_formula|midpoint", "*", [
        ("intermediate-algebra-2e", "11-1-distance-and-midpoint"),
    ]),
    (r"product_rule|quotient_rule", "*", [
        ("calculus-volume-1", "3-3-differentiation-rules"),
    ]),
    (r"differentials", "*", [
        ("calculus-volume-1", "4-2-linear-approximations-and-differentials"),
    ]),
    (r"diff_eq|differential_equation", "*", [
        ("calculus-volume-2", "4-1-basics-of-differential-equations"),
    ]),
    (r"partial_fraction", "*", [
        ("precalculus-2e", "9-4-partial-fractions"),
        ("calculus-volume-2", "3-4-partial-fractions"),
    ]),
    (r"riemann", "*", [
        ("calculus-volume-1", "5-1-approximating-areas"),
    ]),
    (r"ellipses_", "*", [
        ("precalculus-2e", "10-1-the-ellipse"),
    ]),
    (r"hyperbolas_", "*", [
        ("precalculus-2e", "10-2-the-hyperbola"),
    ]),
    (r"parabolas_", "precalculus", [
        ("precalculus-2e", "10-3-the-parabola"),
    ]),
    (r"conic.*parabola|parabolas_graphing|parabolas_writing", "algebra_2", [
        ("intermediate-algebra-2e", "11-2-parabolas"),
    ]),
    (r"polynomial_functions_graphing|graphs_of_polynomial", "*", [
        ("precalculus-2e", "3-4-graphs-of-polynomial-functions"),
    ]),
    (r"functions_operations|function_operations", "*", [
        ("precalculus-2e", "1-4-composition-of-functions"),
    ]),
    (r"law_of_sines|law_of_cosines|area_and_laws", "*", [
        ("precalculus-2e", "8-1-non-right-triangles-law-of-sines"),
        ("precalculus-2e", "8-2-non-right-triangles-law-of-cosines"),
    ]),
    (r"systems_word|word_problems$", "pre_algebra", [
        ("elementary-algebra-2e", "5-4-solve-applications-with-systems-of-equations"),
    ]),
    (r"graphing_systems|systems_by_graphing", "*", [
        ("elementary-algebra-2e", "5-1-solve-systems-of-equations-by-graphing"),
    ]),
    (r"single_variable_inequal|graphing_single_variable", "*", [
        ("elementary-algebra-2e", "2-7-solve-linear-inequalities"),
    ]),
    (r"slope_and_lines|graphing_linear|writing_linear", "geometry", [
        ("elementary-algebra-2e", "4-2-graph-linear-equations"),
        ("elementary-algebra-2e", "4-1-use-the-rectangular-coordinate"),
    ]),
    (r"quadratic_factoring", "*", [
        ("elementary-algebra-2e", "7-2-factor-trinomials-of-the-form-x2"),
        ("elementary-algebra-2e", "7-3-factor-trinomials-of-the-form-ax2"),
    ]),
    (r"special_right", "*", [
        ("precalculus-2e", "5-4-right-triangle-trigonometry"),
    ]),
    (r"finding_trig_ratios|finding_angle_measures|solving_right_triangles|multi_step_trig", "geometry", [
        ("precalculus-2e", "5-4-right-triangle-trigonometry"),
    ]),
]

OUR_LESSON_PINS: dict[str, tuple[int, int]] = {
    "g6_equations_tape_diagrams": (6, 1),
    "g6_equations_hanger_diagrams": (6, 3),
    "g6_inequalities_hanger_diagrams": (6, 3),
    "g6_solutions_to_equations": (6, 2),
    "g6_distributive_property_area_diagrams_numeric": (6, 9),
    "g6_distributive_property_area_diagrams_algebraic": (6, 9),
    "g6_distributive_property_numeric": (6, 10),
    "g6_distributive_property_algebraic": (6, 10),
    "g6_equivalent_ratio_equations": (6, 16),
    "g6_constant_rate_equations": (6, 17),
    "g6_equations_for_other_relationships": (6, 18),
}

OUR_UNIT_HINT = {
    "ratios": 2,
    "rates": 3,
    "percents": 3,
    "dividing_fractions": 4,
    "decimal_arithmetic": 5,
    "common_factors_and_common_multiples": 6,
    "negative_numbers_and_absolute_value": 7,
    "coordinate_plane": 7,
    "numeric_expressions_exponents_and_order_of_operations": 6,
    "variables_and_algebraic_expressions": 6,
    "equivalent_expressions": 6,
    "equations": 6,
    "inequalities": 7,
    "equations_as_relationships_between_two_variables": 6,
    "polygons": 1,
    "polyhedra": 1,
    "area_and_volume_with_fractions": 1,
    "data_sets_and_distributions": 8,
}

WEAK_TOKEN = {
    "equations", "equation", "expressions", "expression", "problems", "problem",
    "functions", "function", "numbers", "number", "values", "value", "using",
    "find", "write", "linear", "basic",
    "basics", "review", "multi", "step", "word", "simple", "introduction",
    "properties", "property", "relations", "relation", "general", "other",
    "practice", "understanding", "formula", "formulas", "applications",
    # Kept out of the strong-token set on purpose: "function" matches almost every section.
    "function", "functions",
}

VISUAL_RE = re.compile(
    r"graph|plot|diagram|figure|number line|hanger|tape|histogram|dot plot|"
    r"box plot|triangle|circle|angle|polygon|parallelogram|trapezoid|kite|"
    r"prism|volume|area|coordinate|transform|shade|sketch|draw|geometry|"
    r"pyramid|cylinder|cone|sphere|net|isometric|sector|arc|tangent|"
    r"congruent|similar|construction|reflection|rotation|translation|dilation|"
    r"slope|intercept|asymptote|vector|polar|region",
    re.I,
)

APP_HEAD = re.compile(
    r"application|everyday|writing exercise|self check|key concept|key term",
    re.I,
)


def log(msg: str) -> None:
    print(msg, flush=True)


def ensure_dirs() -> None:
    for path in (OUT, CACHE, ASSETS, GEN_DIR, IMG_DIR):
        path.mkdir(parents=True, exist_ok=True)


def http_get(url: str, dest: Path | None = None, ua: str = UA_OPENSTAX, retries: int = 2) -> bytes:
    if dest is not None and dest.exists() and dest.stat().st_size > 400:
        return dest.read_bytes()
    last: Exception | None = None
    for attempt in range(retries + 1):
        try:
            if attempt:
                time.sleep(WAIT * 2)
            req = urllib.request.Request(url, headers={"User-Agent": ua})
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read()
            if dest is not None:
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(data)
            return data
        except Exception as exc:  # noqa: BLE001
            last = exc
    raise RuntimeError(f"GET failed {url}: {last}")


def tokens(text: str, *, keep_weak: bool = False) -> list[str]:
    raw = text.lower().replace("_", " ").replace("-", " ")
    raw = re.sub(r"[^a-z0-9 ]", " ", raw)
    out = []
    for part in raw.split():
        if part.isdigit() or len(part) <= 2:
            continue
        if not keep_weak and part in WEAK_TOKEN:
            continue
        out.append(part)
    return out


def token_set(text: str) -> set[str]:
    return set(tokens(text))


def clip(text: str, limit: int = 320) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def parse_curriculum() -> list[dict]:
    src = (ROOT / "lib" / "curriculum.ts").read_text(encoding="utf-8")
    course_id = course_name = ""
    chapter_id = chapter_name = ""
    topics: list[dict] = []
    foundations: list[str] = []
    for line in src.splitlines():
        m = re.match(r'^    id: "([^"]+)"', line)
        if m:
            course_id = m.group(1)
            course_name = ""
            chapter_id = ""
            chapter_name = ""
            continue
        m = re.match(r'^    name: "([^"]+)"', line)
        if m and course_id and not chapter_id:
            course_name = m.group(1)
            continue
        m = re.match(r'^        id: "([^"]+)",\s*$', line)
        if m:
            chapter_id = m.group(1)
            chapter_name = ""
            continue
        m = re.match(r'^        name: "([^"]+)"', line)
        if m and chapter_id and not chapter_name:
            chapter_name = m.group(1)
            continue
        m = re.search(r'id:\s*"([^"]+)",\s*name:\s*"([^"]+)"(?:,\s*type_id:\s*"([^"]+)")?', line)
        if m and course_id == "foundations_math" and not m.group(3):
            foundations.append(m.group(1))
        if m and m.group(3):
            topics.append(
                {
                    "course_id": course_id,
                    "course_name": course_name,
                    "chapter_id": chapter_id,
                    "chapter_name": chapter_name,
                    "leaf_id": m.group(1),
                    "name": m.group(2),
                    "type_id": m.group(3),
                }
            )
    topics.append({"_foundations_without_type": foundations})
    return topics


def wired_topics(rows: list[dict]) -> tuple[list[dict], list[str]]:
    foundations: list[str] = []
    topics: list[dict] = []
    for row in rows:
        if "_foundations_without_type" in row:
            foundations = list(row["_foundations_without_type"])
        else:
            topics.append(row)
    return topics, foundations


# ---------------------------------------------------------------------------
# Generation
# ---------------------------------------------------------------------------

def _numbers(text: str) -> dict:
    nums = [int(n) for n in re.findall(r"\d+", text or "")]
    abs_nums = [n for n in nums if n < 10_000]
    return {
        "max_abs": max(abs_nums) if abs_nums else 0,
        "n_frac": len(re.findall(r"\\frac|/", text or "")),
        "neg": bool(re.search(r"(?<![\w\\])-\d|−", text or "")),
        "dec": bool(re.search(r"\d+\.\d+", text or "")),
    }


def _template(text: str) -> str:
    s = text or ""
    s = re.sub(r"\\frac\{[^{}]*\}\{[^{}]*\}", "FRAC", s)
    s = re.sub(r"-?\d+\.\d+", "DEC", s)
    s = re.sub(r"-?\d+", "N", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def _svg_descriptor(svg: str) -> str:
    if not svg:
        return ""
    counts = {
        "rect": len(re.findall(r"<rect\b", svg)),
        "circle": len(re.findall(r"<circle\b", svg)),
        "ellipse": len(re.findall(r"<ellipse\b", svg)),
        "polygon": len(re.findall(r"<polygon\b", svg)),
        "polyline": len(re.findall(r"<polyline\b", svg)),
        "path": len(re.findall(r"<path\b", svg)),
        "line": len(re.findall(r"<line\b", svg)),
        "text": len(re.findall(r"<text\b", svg)),
    }
    return ",".join(f"{k}{v}" for k, v in counts.items() if v)


def _write_svg(type_id: str, tier: str, seed: int, kind: str, fragment: str) -> str:
    if not fragment or "<svg" not in fragment:
        return ""
    dest_dir = GEN_DIR / type_id
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{tier}-{seed}-{kind}.svgfrag"
    dest.write_text(fragment, encoding="utf-8")
    return str(dest.relative_to(OUT)).replace("\\", "/")


def generate_topic(topic: dict) -> dict:
    from question_engine.api.handler import _generate_for_type
    from scripts.render_graph_svg import (
        extract_answer_graph,
        extract_prompt_graph,
        render_graph_from_extracted,
    )

    samples = []
    for tier in TIERS:
        for seed in SEEDS:
            row = {
                "tier": tier,
                "seed": seed,
                "prompt_latex": "",
                "prompt_text": "",
                "instruction_latex": "",
                "answer_latex": "",
                "difficulty": None,
                "error": None,
                "visuals": [],
                "descriptors": [],
                "numbers": {},
                "template": "",
            }
            try:
                qs = _generate_for_type(
                    topic["type_id"],
                    {
                        "count": 1,
                        "difficulty_tier": tier,
                        "seed": seed,
                        "include_answer_key": True,
                        "include_diagram": True,
                        "include_graph_metadata": True,
                    },
                )
                if not qs:
                    row["error"] = "empty"
                    samples.append(row)
                    continue
                q = qs[0]
                meta = q.metadata if isinstance(q.metadata, dict) else {}
                row["prompt_latex"] = (q.prompt_latex or "").strip()
                row["prompt_text"] = (q.prompt_text or "").strip()
                row["instruction_latex"] = str(meta.get("instruction_latex") or "").strip()
                row["answer_latex"] = (q.answer_latex or "").strip()
                settings = meta.get("generation_settings") if isinstance(meta.get("generation_settings"), dict) else {}
                row["difficulty"] = settings.get("difficulty")
                visuals: list[tuple[str, str]] = []
                diagram = meta.get("diagram_svg")
                if isinstance(diagram, str) and "<svg" in diagram:
                    visuals.append(("diagram", diagram))
                try:
                    prompt_graph = render_graph_from_extracted(extract_prompt_graph(meta))
                except Exception as exc:  # noqa: BLE001
                    prompt_graph = ""
                    row["error"] = f"graph render: {exc}"
                if prompt_graph and "<svg" in prompt_graph:
                    visuals.append(("prompt-graph", prompt_graph))
                try:
                    answer_graph = render_graph_from_extracted(extract_answer_graph(meta))
                except Exception:
                    answer_graph = ""
                if answer_graph and "<svg" in answer_graph and answer_graph != prompt_graph:
                    visuals.append(("answer-graph", answer_graph))
                for kind, frag in visuals:
                    rel = _write_svg(topic["type_id"], tier, seed, kind, frag)
                    if rel:
                        row["visuals"].append({"kind": kind, "path": rel})
                        row["descriptors"].append(_svg_descriptor(frag))
                blob = " ".join(
                    [row["instruction_latex"], row["prompt_latex"], row["prompt_text"], row["answer_latex"]]
                )
                row["numbers"] = _numbers(blob)
                row["template"] = _template(row["instruction_latex"] + " " + row["prompt_latex"])
            except Exception as exc:  # noqa: BLE001
                row["error"] = f"{type(exc).__name__}: {exc}"
            samples.append(row)
    return {"type_id": topic["type_id"], "samples": samples}


def generate_all(topics: list[dict], force: bool = False) -> dict[str, dict]:
    cache_path = CACHE / "generated.json"
    cached: dict[str, dict] = {}
    if cache_path.exists() and not force:
        cached = json.loads(cache_path.read_text(encoding="utf-8"))
    os.environ["QE_LOG_GENERATED"] = "0"
    import question_engine.types  # noqa: F401

    missing = [t for t in topics if t["type_id"] not in cached]
    log(f"generate {len(missing)} topics ({len(topics) - len(missing)} cached)")
    for i, topic in enumerate(missing, 1):
        cached[topic["type_id"]] = generate_topic(topic)
        if i % 25 == 0 or i == len(missing):
            cache_path.write_text(json.dumps(cached), encoding="utf-8")
            log(f"  generated {i}/{len(missing)}")
    cache_path.write_text(json.dumps(cached), encoding="utf-8")
    return cached


# ---------------------------------------------------------------------------
# OpenStax
# ---------------------------------------------------------------------------

def slug_index() -> dict[str, list[str]]:
    path = CACHE / "openstax_slugs.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    data = {}
    books = sorted({b for bs in BOOKS_FOR_COURSE.values() for b in bs})
    for book in books:
        data[book] = discover_slugs(book)
        log(f"  slugs {book}: {len(data[book])}")
    path.write_text(json.dumps(data), encoding="utf-8")
    return data


def _resolve_slug(book: str, needle: str, slugs: dict[str, list[str]]) -> str | None:
    hits = [s for s in slugs.get(book, []) if needle in s and "introduction" not in s.split("-", 2)[-1:]]
    # keep introductions only if nothing else matches
    if not hits:
        hits = [s for s in slugs.get(book, []) if needle in s]
    if not hits:
        return None
    hits.sort(key=len)
    return hits[0]


def pin_sections(topic: dict, slugs: dict[str, list[str]]) -> list[tuple[str, str]] | None:
    hay = f"{topic['type_id']} {topic['name']}"
    for pattern, course, pairs in OPENSTAX_PINS:
        if course not in {"*", topic["course_id"]}:
            continue
        if not re.search(pattern, hay):
            continue
        resolved = []
        for book, needle in pairs:
            slug = _resolve_slug(book, needle, slugs)
            if slug:
                resolved.append((book, slug))
        if resolved:
            return resolved
    return None


def anchor_groups(topic: dict) -> list[list[str]]:
    """Substrings the section slug must contain, one group at a time."""
    name = f"{topic['name']} {topic['type_id']}".lower().replace("_", " ")
    groups: list[list[str]] = []
    rules = [
        (r"ellipse", ["ellipse"]),
        (r"hyperbola", ["hyperbola"]),
        (r"parabola", ["parabola"]),
        (r"\bcircle", ["circle"]),
        (r"polar", ["polar"]),
        (r"parametric", ["parametric"]),
        (r"vector", ["vector"]),
        (r"matrix|matrices|determinant|cramer", ["matrix", "determinant", "cramer"]),
        (r"partial fraction", ["partial"]),
        (r"chain rule", ["chain"]),
        (r"product rule|quotient rule", ["differentiation-rules", "product", "quotient"]),
        (r"implicit", ["implicit"]),
        (r"riemann", ["approximat", "riemann", "sum"]),
        (r"lhopital|l'hospital", ["lhopital"]),
        (r"differential equation", ["differential-equation"]),
        (r"related rate", ["related-rate"]),
        (r"\bsequence", ["sequence"]),
        (r"\bseries\b", ["series"]),
        (r"logarithm", ["logarithm"]),
        (r"exponential", ["exponential"]),
        (r"inequal", ["inequal"]),
        (r"absolute value", ["absolute"]),
        (r"pythagorean", ["pythagorean"]),
        (r"\bgraph", ["graph"]),
        (r"\bsystem", ["system"]),
        (r"trigonometr|\btrig\b", ["trig", "sine", "cosine", "triangle"]),
        (r"composition|operations of function|function operation", ["compos", "operation"]),
    ]
    for pattern, words in rules:
        if re.search(pattern, name):
            groups.append(words)
    return groups


def slug_ok(topic: dict, slug: str) -> bool:
    """Reject chapter intros and sections about a different skill."""
    name = f"{topic['name']} {topic['type_id']}".lower()
    if re.search(r"introduction|key-terms|key-concepts|key-equations|review-exercises", slug):
        return False
    if "measurement" in slug and "measurement" not in name:
        return False
    if re.search(r"matrix|matrices", slug) and not re.search(r"matrix|matrices", name):
        return False
    if "mixture" in slug and "mixture" not in name:
        return False
    if "system" in slug and not re.search(r"system", name):
        return False
    if "determinant" in slug and not re.search(r"determinant|cramer", name):
        return False
    for group in anchor_groups(topic):
        if not any(word in slug for word in group):
            return False
    return True


def score_slug(topic: dict, book: str, slug: str, book_rank: int) -> float:
    tt = token_set(topic["name"] + " " + topic["type_id"] + " " + topic["chapter_name"])
    st = token_set(slug)
    inter = tt & st
    if not inter:
        return 0.0
    base = len(inter) * 2.2 + (len(inter) / max(len(tt), 1)) * 3
    base += sum(0.35 for t in inter if len(t) >= 7)
    if book_rank == 0:
        base += 1.3
    elif book_rank >= 2:
        base -= 0.4
    if "introduction" in slug and not slug[:1].isdigit():
        base -= 2
    if re.search(r"introduction|key-terms|key-concepts|key-equations|review-exercises", slug):
        base -= 8
    return base


def best_openstax(topic: dict, slugs: dict[str, list[str]]) -> tuple[list[tuple[str, str]], float, str]:
    pinned = pin_sections(topic, slugs)
    if pinned:
        return pinned, 9.0, "pin"
    ranked: list[tuple[float, str, str]] = []
    for rank, book in enumerate(BOOKS_FOR_COURSE.get(topic["course_id"], [])):
        for slug in slugs.get(book, []):
            ranked.append((score_slug(topic, book, slug, rank), book, slug))
    ranked.sort(key=lambda row: -row[0])
    fitting = [row for row in ranked if row[0] > 0 and slug_ok(topic, row[2])]
    if fitting:
        best = fitting[0]
        quality = "strong" if best[0] >= 4.6 else "ok" if best[0] >= 3.2 else "weak"
        return [(best[1], best[2])], best[0], quality
    if ranked and ranked[0][0] > 0:
        best = ranked[0]
        return [(best[1], best[2])], best[0], "weak"
    return [], 0.0, "none"


def _abs_openstax_url(src: str) -> str:
    if src.startswith("http"):
        return src
    if src.startswith("//"):
        return "https:" + src
    return "https://openstax.org" + (src if src.startswith("/") else "/" + src)


def image_index_from_html(html_text: str) -> dict[str, list[dict]]:
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html_text, "html.parser")
    main = soup.find(id="main-content") or soup
    found: dict[str, list[dict]] = {}
    for node in main.select("[data-type=example], [data-type=exercise], [data-type=note]"):
        nid = node.get("id")
        if not nid:
            continue
        imgs = []
        for img in node.select("img"):
            src = img.get("src") or ""
            if "image-cdn" not in src and "/resources/" not in src and "cnx.org" not in src:
                continue
            alt = re.sub(r"\s+", " ", img.get("alt") or "").strip()
            imgs.append({"url": _abs_openstax_url(src), "alt": alt})
        # de-dupe urls
        dedup = []
        seen = set()
        for img in imgs:
            if img["url"] in seen:
                continue
            seen.add(img["url"])
            dedup.append(img)
        if dedup:
            found[str(nid)] = dedup
    return found


def load_openstax_section(book: str, slug: str) -> dict:
    cache_json = CACHE / "openstax_parsed" / f"{book}__{slug}.json"
    if cache_json.exists():
        return json.loads(cache_json.read_text(encoding="utf-8"))
    dest = CACHE / "openstax_html" / book / f"{slug}.html"
    url = f"https://openstax.org/books/{book}/pages/{slug}"
    if not (dest.exists() and dest.stat().st_size > 400):
        time.sleep(WAIT)
        log(f"  fetch {book}/{slug}")
    raw = http_get(url, dest, ua=UA_OPENSTAX)
    html_text = raw.decode("utf-8", errors="replace")
    inv = parse_section_html(dest, book=book, slug=slug)
    images = image_index_from_html(html_text)
    items = []
    for it in inv.items:
        imgs = images.get(it.item_id, [])
        if not imgs and it.source_anchor:
            imgs = images.get(it.source_anchor, [])
        items.append(
            {
                "item_id": it.item_id,
                "kind": it.kind,
                "title": it.title or "",
                "position": it.position,
                "heading": it.nearest_heading or "",
                "text": it.prompt_text or "",
                "latex": it.prompt_latex_bits or [],
                "images": imgs[:3],
            }
        )
    data = {
        "book": book,
        "slug": slug,
        "title": inv.title,
        "url": inv.source_url,
        "items": items,
    }
    cache_json.parent.mkdir(parents=True, exist_ok=True)
    cache_json.write_text(json.dumps(data), encoding="utf-8")
    return data


def usable_item(item: dict) -> bool:
    text = (item.get("text") or "").strip()
    low = text.lower()
    if re.fullmatch(r"\d+\s*\.?", text):
        return False
    if "if you missed this problem" in low or low.startswith("be prepared"):
        return False
    if re.search(r"easiest for you|which is the hardest|explain your answers", low):
        return False
    if "$" in text and len(text) >= 8:
        return True
    if len(text) < 28:
        return False
    return True


def structure_bonus(topic: dict, text: str) -> int:
    """Prefer items that are actually this skill when a section mixes several."""
    name = (topic["name"] + " " + topic["type_id"]).lower()
    bonus = 0
    if re.search(r"quadratic|trinomial", name):
        if re.search(r"\^\{?2\}?", text) and not re.search(r"\^\{?[3-9]", text):
            bonus += 4
    if re.search(r"graph", name) and re.search(r"graph|sketch|plot", text, re.I):
        bonus += 4
    if re.search(r"simplif", name) and re.search(r"simplif", text, re.I):
        bonus += 3
    if re.search(r"\bsolve", name) and re.search(r"\bsolve", text, re.I):
        bonus += 2
    if re.search(r"inequal", name) and re.search(r"<|>|\\le|\\ge|≤|≥", text):
        bonus += 3
    if re.search(r"log", name) and re.search(r"\\log|\\ln", text):
        bonus += 4
    if re.search(r"derivative|differenti", name) and re.search(r"deriv", text, re.I):
        bonus += 4
    if re.search(r"integral", name) and re.search(r"\\int|integrat", text, re.I):
        bonus += 4
    if re.search(r"\blimit", name) and re.search(r"\\lim|\blimit", text, re.I):
        bonus += 4
    if re.search(r"trig", name) and re.search(r"\\sin|\\cos|\\tan", text):
        bonus += 3
    if re.search(r"factor", name) and re.search(r"factor", text, re.I):
        bonus += 2
    return bonus


def focus_items(items: list[dict], topic: dict, generated: dict | None = None) -> list[dict]:
    """Keep items that are this skill. A short list is not a reason to put the rest back."""
    profile = skill_profile(topic, generated)
    return [
        it
        for it in items
        if item_matches(
            it.get("text") or "",
            profile,
            heading=it.get("heading") or "",
            source_text=it.get("section_title") or "",
        )
    ]


def heading_allowed(heading: str, topic: dict) -> bool:
    if APP_HEAD.search(heading or ""):
        name = topic["name"] + " " + topic["type_id"]
        if not re.search(r"word|application|model|translat|story", name, re.I):
            return False
    return True


def prefer_heading_group(items: list[dict], topic: dict) -> list[dict]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for it in items:
        groups[it.get("heading") or ""].append(it)
    if len(groups) <= 1:
        return items
    tt = token_set(topic["name"] + " " + topic["type_id"])
    def score(heading: str) -> float:
        inter = tt & token_set(heading)
        return len(inter) + (0.5 if re.search(r"practice makes perfect", heading, re.I) else 0)
    best = max(groups, key=score)
    if score(best) > 0:
        return groups[best]
    return items


def split_ladder(items: list[dict]) -> dict[str, list[dict]]:
    """Document order is the source's easy → hard order."""
    if not items:
        return {tier: [] for tier in TIERS}
    n = len(items)
    if n == 1:
        return {"easy": items[:1], "medium": [], "hard": []}
    if n == 2:
        return {"easy": items[:1], "medium": [], "hard": items[-1:]}
    if n < 6:
        return {
            "easy": items[:1],
            "medium": items[n // 2 : n // 2 + 1],
            "hard": items[-1:],
        }
    mid = n // 2
    return {
        "easy": items[:2],
        "medium": items[mid - 1 : mid + 1],
        "hard": items[-2:],
    }


# Slug needles for textbook wording that does not repeat the topic's word.
# These only add candidates. The item gate still has to accept each exercise.
VOCAB_SLUG_HINTS: list[tuple[str, list[str], float]] = [
    (r"concav", ["shape-of-a-graph"], 9.0),
    (r"extrem|absolute max|absolute min", ["maxima-and-minima"], 9.0),
    (r"disk|washer", ["volumes-by-slicing"], 8.0),
    (r"cylindrical shell|shell method", ["cylindrical-shell"], 8.0),
    (r"arc length", ["arc-length"], 8.0),
    (r"area between", ["areas-between"], 8.0),
    (r"related rate", ["related-rate"], 9.0),
    (r"mean value", ["mean-value"], 9.0),
    (r"chain rule", ["chain-rule"], 9.0),
    (r"quotient rule|product rule|power rule", ["differentiation-rules"], 8.0),
    (r"implicit", ["implicit"], 8.0),
    (r"linear approximation|differential", ["linear-approximation"], 8.0),
    (r"lhopital|l'hospital|lhospital", ["lhopital"], 8.0),
    (r"riemann", ["approximating-area"], 8.0),
    (r"fundamental theorem", ["fundamental-theorem"], 8.0),
    (r"graph\w* linear|writing linear equation", ["graph-linear", "graphing-linear"], 8.0),
    (r"solv\w* linear equation|multi.step equation|one.step equation|two.step equation", ["solve-linear-equations"], 8.0),
]


def _cached_section(book: str, slug: str, section_cache: dict, *, fetch: bool) -> dict | None:
    key = (book, slug)
    if key in section_cache:
        return section_cache[key]
    path = CACHE / "openstax_parsed" / f"{book}__{slug}.json"
    if path.exists():
        section_cache[key] = json.loads(path.read_text(encoding="utf-8"))
        return section_cache[key]
    if not fetch:
        return None
    try:
        section_cache[key] = load_openstax_section(book, slug)
    except Exception as exc:  # noqa: BLE001
        log(f"  openstax fail {book}/{slug}: {exc}")
        return None
    return section_cache[key]


def _matching_item_count(section: dict, profile, topic: dict) -> int:
    source = section.get("title") or ""
    count = 0
    for it in section.get("items") or []:
        if it.get("kind") not in {"section_exercise", "other_exercise", "checkpoint"}:
            continue
        if not usable_item(it):
            continue
        if item_matches(it.get("text") or "", profile, heading=it.get("heading") or "", source_text=source):
            count += 1
    return count


def openstax_candidates(topic: dict, slugs: dict[str, list[str]], profile) -> list[tuple[float, str, str]]:
    ranked: list[tuple[float, str, str]] = []
    seen: set[tuple[str, str]] = set()

    def add(score: float, book: str, slug: str) -> None:
        if score <= 0 or (book, slug) in seen:
            return
        if not slug_ok(topic, slug):
            return
        if re.search(r"application|everyday", slug) and not profile.word_problem:
            return
        seen.add((book, slug))
        ranked.append((score, book, slug))

    for rank, book in enumerate(BOOKS_FOR_COURSE.get(topic["course_id"], [])):
        for slug in slugs.get(book, []):
            add(section_slug_score(slug, profile, book_rank=rank), book, slug)
    name = f"{topic['name']} {topic['type_id']}"
    for pattern, needles, bonus in VOCAB_SLUG_HINTS:
        if not re.search(pattern, name, re.I):
            continue
        for book in BOOKS_FOR_COURSE.get(topic["course_id"], []):
            for slug in slugs.get(book, []):
                if any(needle in slug for needle in needles):
                    add(bonus, book, slug)
    ranked.sort(key=lambda row: -row[0])
    return ranked[:8]


def choose_openstax_sections(
    topic: dict,
    generated: dict,
    slugs: dict[str, list[str]],
    section_cache: dict,
) -> list[dict]:
    """Pick the section whose exercises are this skill. Do not pad from a neighbor."""
    profile = skill_profile(topic, generated)

    def consider(pairs: list[tuple[str, str]], *, fetch: bool) -> tuple[int, list[dict]]:
        sections = []
        for book, slug in pairs:
            section = _cached_section(book, slug, section_cache, fetch=fetch)
            if section is not None:
                sections.append(section)
        return sum(_matching_item_count(section, profile, topic) for section in sections), sections

    pinned = pin_sections(topic, slugs)
    if pinned:
        count, sections = consider(pinned, fetch=True)
        if count >= 1:
            return sections

    candidates = openstax_candidates(topic, slugs, profile)
    best: tuple[int, float, dict] | None = None
    for score, book, slug in candidates:
        section = _cached_section(book, slug, section_cache, fetch=False)
        if section is None:
            continue
        count = _matching_item_count(section, profile, topic)
        if best is None or (count, score) > (best[0], best[1]):
            best = (count, score, section)
    if best is not None and best[0] >= 2:
        return [best[2]]

    fetches = 0
    for score, book, slug in candidates:
        if _cached_section(book, slug, section_cache, fetch=False) is not None:
            continue
        if fetches >= 3:
            break
        fetches += 1
        section = _cached_section(book, slug, section_cache, fetch=True)
        if section is None:
            continue
        count = _matching_item_count(section, profile, topic)
        if best is None or (count, score) > (best[0], best[1]):
            best = (count, score, section)
        if best[0] >= 4:
            break
    if best is not None and best[0] >= 1:
        return [best[2]]
    return []


def select_openstax_items(sections: list[dict], topic: dict, generated: dict | None = None) -> dict[str, list[dict]]:
    profile = skill_profile(topic, generated)
    pool: list[dict] = []
    for section in sections:
        source = section.get("title") or ""

        def matches(it: dict, source: str = source) -> bool:
            return usable_item(it) and item_matches(
                it.get("text") or "",
                profile,
                heading=it.get("heading") or "",
                source_text=source,
            )

        exercises = [it for it in section["items"] if it["kind"] == "section_exercise" and matches(it)]
        if len(exercises) < 2:
            exercises = [
                it
                for it in section["items"]
                if it["kind"] in {"section_exercise", "other_exercise", "checkpoint"} and matches(it)
            ]
        chosen = exercises
        for it in chosen:
            it = dict(it)
            it["section_title"] = section["title"]
            it["section_url"] = section["url"]
            it["book"] = section["book"]
            pool.append(it)
    # Drop near-duplicate stems
    deduped = []
    seen = set()
    for it in pool:
        key = _template(it.get("text") or "")[:180]
        if key in seen:
            continue
        seen.add(key)
        deduped.append(it)
    return split_ladder(deduped)


def section_example_figures(sections: list[dict], limit: int = 3) -> list[dict]:
    figs = []
    for section in sections:
        for it in section["items"]:
            if it["kind"] != "example":
                continue
            for img in it.get("images") or []:
                figs.append(
                    {
                        "url": img["url"],
                        "alt": img.get("alt") or "",
                        "caption": it.get("title") or section["title"],
                        "text": clip(it.get("text") or "", 240),
                        "page_url": section["url"],
                    }
                )
                if len(figs) >= limit:
                    return figs
    return figs


# ---------------------------------------------------------------------------
# Open Up Resources (Grade 6 IM lessons)
# ---------------------------------------------------------------------------

OUR_BASE = "https://access.openupresources.org/curricula/our6-8math/en/grade-6"


def our_lesson_catalog() -> list[dict]:
    path = CACHE / "our_g6_catalog.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    from bs4 import BeautifulSoup

    lessons = []
    for unit in range(1, 10):
        url = f"{OUR_BASE}/unit-{unit}/index.html"
        dest = CACHE / "our_html" / f"unit-{unit}.html"
        if not (dest.exists() and dest.stat().st_size > 400):
            time.sleep(WAIT)
        raw = http_get(url, dest, ua=UA_BROWSER)
        soup = BeautifulSoup(raw, "html.parser")
        by_href: dict[str, list[str]] = defaultdict(list)
        for a in soup.select("a"):
            href = a.get("href") or ""
            if not re.search(r"lesson-\d+/index\.html", href):
                continue
            text = re.sub(r"\s+", " ", a.get_text(" ", strip=True)).strip()
            if text:
                by_href[href].append(text)
        for href, texts in by_href.items():
            m = re.search(r"lesson-(\d+)", href)
            if not m:
                continue
            title = max(texts, key=len)
            if re.fullmatch(r"Lesson \d+", title) and len(texts) > 1:
                title = max((t for t in texts if not t.startswith("Lesson ")), key=len, default=title)
            lessons.append(
                {
                    "unit": unit,
                    "lesson": int(m.group(1)),
                    "title": title,
                    "url": urljoin(url, href),
                }
            )
        log(f"  OUR unit {unit}: {sum(1 for les in lessons if les['unit']==unit)} lessons")
    # unique
    uniq = {(les["unit"], les["lesson"]): les for les in lessons}
    lessons = [uniq[k] for k in sorted(uniq)]
    path.write_text(json.dumps(lessons), encoding="utf-8")
    return lessons


def fetch_our_lesson(lesson: dict) -> dict:
    key = f"u{lesson['unit']}-l{lesson['lesson']}"
    dest_json = CACHE / "our_parsed" / f"{key}.json"
    if dest_json.exists():
        return json.loads(dest_json.read_text(encoding="utf-8"))
    from bs4 import BeautifulSoup

    dest = CACHE / "our_html" / f"{key}.html"
    if not (dest.exists() and dest.stat().st_size > 400):
        time.sleep(WAIT)
        log(f"  fetch OUR {key} {lesson['title']}")
    raw = http_get(lesson["url"], dest, ua=UA_BROWSER)
    soup = BeautifulSoup(raw, "html.parser")
    blocks = []
    for kind, sel in (("activity", ".c-activity"), ("practice", ".c-problem")):
        for i, node in enumerate(soup.select(sel), 1):
            heading = node.find(["h2", "h3", "h4"])
            title = re.sub(r"\s+", " ", heading.get_text(" ", strip=True)).strip() if heading else ""
            text = re.sub(r"\s+", " ", node.get_text(" ", strip=True)).strip()
            images = []
            for img in node.select("img"):
                src = img.get("src") or ""
                if not src or src.startswith("data:"):
                    continue
                alt = re.sub(r"\s+", " ", img.get("alt") or "").strip()
                images.append({"url": urljoin(lesson["url"], src), "alt": alt})
            blocks.append(
                {
                    "kind": kind,
                    "index": i,
                    "title": title,
                    "text": text[:1500],
                    "images": images[:3],
                }
            )
    data = {**lesson, "blocks": blocks}
    dest_json.parent.mkdir(parents=True, exist_ok=True)
    dest_json.write_text(json.dumps(data), encoding="utf-8")
    return data


def score_our_lesson(topic: dict, lesson: dict) -> float:
    pin = OUR_LESSON_PINS.get(topic["type_id"])
    if pin and (lesson["unit"], lesson["lesson"]) == pin:
        return 50.0
    tt = token_set(topic["name"] + " " + topic["type_id"])
    lt = token_set(lesson["title"])
    inter = tt & lt
    score = len(inter) * 3 + sum(0.4 for t in inter if len(t) >= 6)
    hint = OUR_UNIT_HINT.get(topic["chapter_id"])
    if hint and lesson["unit"] == hint:
        score += 1.6
    elif hint:
        score -= 0.8
    # keyword boosts
    name = topic["name"].lower() + " " + topic["type_id"]
    title = lesson["title"].lower()
    pairs = [
        ("hanger", "balance"),
        ("hanger", "hanger"),
        ("tape", "tape"),
        ("dot plot", "dot"),
        ("histogram", "histogram"),
        ("box plot", "box"),
        ("percent", "percent"),
        ("ratio", "ratio"),
        ("rate", "rate"),
        ("area", "area"),
        ("triangle", "triangle"),
        ("parallelogram", "parallelogram"),
        ("surface", "surface"),
        ("exponent", "exponent"),
        ("distribut", "distribut"),
        ("inequal", "inequal"),
        ("number line", "number line"),
        ("coordinate", "coordinate"),
        ("decimal", "decimal"),
        ("divid", "divid"),
        ("fraction", "fraction"),
        ("absolute", "absolute"),
        ("negative", "negative"),
        ("factor", "factor"),
        ("prism", "prism"),
        ("volume", "volume"),
    ]
    for a, b in pairs:
        if a in name and b in title:
            score += 2.5
    return score


def best_our_lesson(topic: dict, catalog: list[dict]) -> tuple[dict | None, float]:
    best: tuple[float, dict | None] = (-1.0, None)
    for lesson in catalog:
        sc = score_our_lesson(topic, lesson)
        if sc > best[0]:
            best = (sc, lesson)
    return best[1], best[0]


def topic_keys(topic: dict) -> list[str]:
    name = (topic["name"] + " " + topic["type_id"]).lower()
    keys: list[str] = []
    table = [
        ("hanger", ["hanger", "balance"]),
        ("tape", ["tape"]),
        ("histogram", ["histogram"]),
        ("dot plot", ["dot plot", "dot"]),
        ("box plot", ["box plot"]),
        ("percent", ["percent", "%"]),
        ("ratio", ["ratio"]),
        ("rate", ["rate"]),
        ("decimal", ["decimal"]),
        ("fraction", ["fraction"]),
        ("exponent", ["exponent"]),
        ("distribut", ["distribut"]),
        ("inequal", ["inequal"]),
        ("absolute", ["absolute"]),
        ("coordinate", ["coordinate"]),
        ("number line", ["number line"]),
        ("parallelogram", ["parallelogram"]),
        ("triangle", ["triangle"]),
        ("trapezoid", ["trapezoid"]),
        ("prism", ["prism"]),
        ("surface", ["surface"]),
        ("area", ["area"]),
    ]
    for needle, words in table:
        if needle in name:
            keys.extend(words)
    return keys


def select_our_items(lesson: dict, topic: dict, generated: dict | None = None) -> dict[str, list[dict]]:
    """Practice problems that are this skill. Spiral review at the end is not the hard tier."""
    profile = skill_profile(topic, generated)
    source = lesson.get("title") or ""

    def matches(block: dict) -> bool:
        if len(block.get("text") or "") <= 40:
            return False
        alt = " ".join(img.get("alt") or "" for img in block.get("images") or [])
        return item_matches(
            block.get("text") or "",
            profile,
            heading=block.get("title") or "",
            source_text=source,
            alt=alt,
        )

    practice = [b for b in lesson.get("blocks", []) if b.get("kind") == "practice" and matches(b)]
    # The lesson activities are the same skill when practice itself is thin.
    # They are not a place to put an unrelated problem back in.
    if len(practice) < 2:
        for block in lesson.get("blocks", []):
            if block.get("kind") == "activity" and matches(block) and block not in practice:
                practice.append(block)
    return split_ladder(practice)


# ---------------------------------------------------------------------------
# Illustrative Mathematics task PDFs
# ---------------------------------------------------------------------------

IM_ZIPS = {
    "HSG": "https://s3.amazonaws.com/illustrativemathematics/attachments/zipped_files/grade_HSG.zip",
    "HSS": "https://s3.amazonaws.com/illustrativemathematics/attachments/zipped_files/grade_HSS.zip",
    "HSF": "https://s3.amazonaws.com/illustrativemathematics/attachments/zipped_files/grade_HSF.zip",
    "HSA": "https://s3.amazonaws.com/illustrativemathematics/attachments/zipped_files/grade_HSA.zip",
    "G6": "https://s3.amazonaws.com/illustrativemathematics/attachments/zipped_files/grade_6.zip",
    "G7": "https://s3.amazonaws.com/illustrativemathematics/attachments/zipped_files/grade_7.zip",
    "G8": "https://s3.amazonaws.com/illustrativemathematics/attachments/zipped_files/grade_8.zip",
}


def ensure_im_filenames() -> list[dict]:
    """Download zips and list PDFs. Text extraction happens for the chosen files."""
    path = CACHE / "im_files.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    files = []
    for key, url in IM_ZIPS.items():
        dest = CACHE / "im" / f"grade_{key}.zip"
        if not (dest.exists() and dest.stat().st_size > 1000):
            log(f"  download IM {key}")
            http_get(url, dest, ua=UA_BROWSER)
        out_dir = CACHE / "im" / key
        if not any(out_dir.glob("*.pdf")):
            out_dir.mkdir(parents=True, exist_ok=True)
            subprocess.check_call(["unzip", "-qo", str(dest), "-d", str(out_dir)])
        for pdf in out_dir.rglob("*.pdf"):
            files.append({"pack": key, "name": pdf.name, "path": str(pdf)})
        log(f"  IM {key}: {sum(1 for f in files if f['pack']==key)} pdfs")
    path.write_text(json.dumps(files), encoding="utf-8")
    return files


def score_im_file(topic: dict, info: dict, pack_bias: set[str], generated: dict | None = None) -> float:
    profile = skill_profile(topic, generated)
    score = filename_score(info["name"].replace("_", " "), profile)
    if score <= 0:
        return 0.0
    if info["pack"] in pack_bias:
        score += 0.3
    return score


def best_im_files(topic: dict, files: list[dict], k: int = 3, generated: dict | None = None) -> list[dict]:
    course = topic["course_id"]
    if course == "geometry":
        bias = {"HSG"}
    elif course == "grade_6_math":
        bias = {"G6"}
    elif course in {"precalculus", "algebra_2"}:
        bias = {"HSF", "HSA", "HSS"}
    elif course == "calculus":
        bias = {"HSF"}
    else:
        bias = {"HSA", "G8", "G7", "HSF"}
    ranked = []
    for info in files:
        sc = score_im_file(topic, info, bias, generated)
        if sc > 0:
            ranked.append((sc, info))
    ranked.sort(key=lambda pair: -pair[0])
    # Keep a spread: best, then next that is not the same stem prefix.
    chosen = []
    used_prefix = set()
    for sc, info in ranked:
        prefix = info["name"].split("_", 1)[0]
        if prefix in used_prefix and len(chosen) >= 1:
            continue
        chosen.append({**info, "score": sc})
        used_prefix.add(prefix)
        if len(chosen) >= k:
            break
    if not chosen and ranked:
        chosen = [{**ranked[0][1], "score": ranked[0][0]}]
    return chosen


def im_excerpt_and_png(info: dict) -> dict:
    pdf = Path(info["path"])
    text_path = CACHE / "im_text" / (pdf.stem + ".txt")
    if not text_path.exists():
        text_path.parent.mkdir(parents=True, exist_ok=True)
        subprocess.check_call(
            ["pdftotext", "-f", "1", "-l", "1", "-layout", str(pdf), str(text_path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    text = text_path.read_text(encoding="utf-8", errors="replace")
    text = re.sub(r"\s+", " ", text).strip()
    png_rel = ""
    png = IMG_DIR / "im" / f"{pdf.stem}.png"
    if not (png.exists() and png.stat().st_size > 500):
        png.parent.mkdir(parents=True, exist_ok=True)
        prefix = png.with_suffix("")
        subprocess.check_call(
            ["pdftoppm", "-png", "-f", "1", "-l", "1", "-r", "80", str(pdf), str(prefix)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        produced = Path(str(prefix) + "-1.png")
        if produced.exists():
            produced.replace(png)
    if png.exists():
        png_rel = str(png.relative_to(OUT)).replace("\\", "/")
    return {
        "title": pdf.stem.replace("_", " "),
        "text": clip(text, 500),
        "image": png_rel,
        "pack": info["pack"],
        "score": info.get("score", 0),
    }


# ---------------------------------------------------------------------------
# Images shared by OpenStax / OUR
# ---------------------------------------------------------------------------

def cache_remote_image(url: str) -> str:
    if not url:
        return ""
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:16]
    # extension guess
    ext = ".img"
    low = url.lower()
    for candidate in (".png", ".jpg", ".jpeg", ".webp", ".gif"):
        if candidate in low:
            ext = ".jpg" if candidate == ".jpeg" else candidate
            break
    dest = IMG_DIR / "remote" / f"{digest}{ext}"
    if dest.exists() and dest.stat().st_size > 400:
        return str(dest.relative_to(OUT)).replace("\\", "/")
    try:
        data = http_get(url, ua=UA_BROWSER)
    except Exception as exc:  # noqa: BLE001
        log(f"  image miss {exc}")
        return ""
    if len(data) < 400:
        return ""
    dest.parent.mkdir(parents=True, exist_ok=True)
    # sniff
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        dest = dest.with_suffix(".png")
    elif data[:2] == b"\xff\xd8":
        dest = dest.with_suffix(".jpg")
    elif data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        dest = dest.with_suffix(".webp")
    dest.write_bytes(data[:2_500_000])
    return str(dest.relative_to(OUT)).replace("\\", "/")


def materialize_images(items: list[dict]) -> list[dict]:
    out = []
    for it in items:
        it = dict(it)
        saved = []
        for img in it.get("images") or []:
            rel = cache_remote_image(img.get("url") or "")
            if rel:
                saved.append({"path": rel, "alt": img.get("alt") or ""})
        it["saved_images"] = saved
        out.append(it)
    return out


# ---------------------------------------------------------------------------
# Reference assembly
# ---------------------------------------------------------------------------

def topic_is_visual(topic: dict, generated: dict | None = None) -> bool:
    blob = f"{topic['name']} {topic['type_id']} {topic['chapter_name']}"
    if VISUAL_RE.search(blob):
        return True
    if generated:
        for sample in generated.get("samples") or []:
            if sample.get("visuals"):
                return True
    return False


def source_kind(topic: dict) -> str:
    if topic["course_id"] == "grade_6_math":
        return "our"
    if topic["course_id"] == "geometry":
        chapter = topic["chapter_id"]
        name = topic["name"].lower()
        if chapter == "review_of_algebra":
            return "openstax"
        if chapter == "probability_and_statistics":
            return "openstax"
        if any(
            k in name
            for k in (
                "pythagorean",
                "circumference",
                "volume",
                "surface",
                "slope",
                "distance",
                "midpoint",
                "graphing linear",
                "writing linear",
                "equation",
                "trig",
            )
        ):
            return "openstax"
        return "im"
    return "openstax"


def build_reference(
    topic: dict,
    generated: dict,
    slugs: dict[str, list[str]],
    our_catalog: list[dict],
    im_files: list[dict],
    section_cache: dict[tuple[str, str], dict],
) -> dict:
    kind = source_kind(topic)
    visual = topic_is_visual(topic, generated)
    ref: dict = {
        "kind": kind,
        "match": "weak",
        "ladder": False,
        "title": "",
        "url": "",
        "license": "",
        "source_name": "",
        "tiers": {tier: [] for tier in TIERS},
        "figures": [],
        "note_bits": [],
    }

    def attach_sections(sections: list[dict]) -> None:
        if not sections:
            return
        tiers = select_openstax_items(sections, topic, generated)
        for tier, items in tiers.items():
            ref["tiers"][tier] = materialize_images(items)
        ref["title"] = " · ".join(s["title"] for s in sections)
        ref["url"] = sections[0]["url"]
        ref["license"] = OPENSTAX_LICENSE
        ref["source_name"] = " + ".join(BOOK_TITLE.get(s["book"], s["book"]) for s in sections)
        n_items = sum(len(v) for v in tiers.values())
        ref["match"] = "strong" if n_items >= 4 else "ok" if n_items else "weak"
        ref["ladder"] = n_items >= 2
        if visual:
            figs = section_example_figures(sections)
            saved_figs = []
            for fig in figs:
                rel = cache_remote_image(fig["url"])
                if rel:
                    saved_figs.append({**fig, "path": rel})
            ref["figures"] = saved_figs

    def matching_im_cards(limit: int = 3) -> list[dict]:
        profile = skill_profile(topic, generated)
        chosen = best_im_files(topic, im_files, k=6, generated=generated)
        cards = []
        for info in chosen:
            card = im_excerpt_and_png(info)
            if item_matches(
                card.get("text") or "",
                profile,
                heading=card.get("title") or "",
                source_text=card.get("title") or "",
            ):
                cards.append(card)
            if len(cards) >= limit:
                break
        cards.sort(key=lambda card: len(card.get("text") or ""))
        return cards

    def place_im_cards(cards: list[dict]) -> None:
        slots = ["easy", "medium", "hard"]
        if len(cards) == 1:
            ref["tiers"]["medium"] = [_im_card(cards[0])]
        elif len(cards) == 2:
            ref["tiers"]["easy"] = [_im_card(cards[0])]
            ref["tiers"]["hard"] = [_im_card(cards[1])]
        else:
            for slot, card in zip(slots, cards[:3]):
                ref["tiers"][slot] = [_im_card(card)]
        ref["kind"] = "im"
        ref["title"] = "; ".join(c["title"] for c in cards[:3])
        ref["url"] = "https://tasks.illustrativemathematics.org/content-standards"
        ref["license"] = IM_LICENSE
        ref["source_name"] = "Illustrative Mathematics task bank"
        ref["match"] = "ok"
        ref["ladder"] = False

    if kind == "our":
        ranked = sorted(our_catalog, key=lambda lesson: -score_our_lesson(topic, lesson))
        ordered: list[dict] = []
        pin = OUR_LESSON_PINS.get(topic["type_id"])
        if pin:
            for lesson in our_catalog:
                if (lesson["unit"], lesson["lesson"]) == pin:
                    ordered.append(lesson)
        for lesson in ranked:
            if score_our_lesson(topic, lesson) <= 0:
                break
            if lesson not in ordered:
                ordered.append(lesson)
            if len(ordered) >= 4:
                break
        picked: tuple[dict, dict[str, list[dict]], float] | None = None
        for lesson in ordered:
            full = fetch_our_lesson(lesson)
            tiers = select_our_items(full, topic, generated)
            n_items = sum(len(v) for v in tiers.values())
            score = score_our_lesson(topic, lesson)
            if picked is None or n_items > picked[0]:
                picked = (n_items, score, full, tiers)  # type: ignore[assignment]
            if n_items >= 2:
                picked = (n_items, score, full, tiers)  # type: ignore[assignment]
                break
        if picked is None:
            ref["match"] = "weak"
            return ref
        _n, score, full, tiers = picked
        for tier, items in tiers.items():
            prepared = []
            for it in items:
                prepared.append(
                    {
                        "text": it.get("text") or "",
                        "title": it.get("title") or f"{it.get('kind')} {it.get('index')}",
                        "heading": full.get("title") or "",
                        "images": it.get("images") or [],
                        "kind": it.get("kind"),
                    }
                )
            ref["tiers"][tier] = materialize_images(prepared)
        ref["title"] = f"Grade 6 Unit {full['unit']} Lesson {full['lesson']}: {full['title']}"
        ref["url"] = full["url"]
        ref["license"] = OUR_LICENSE
        ref["source_name"] = "Open Up Resources Grade 6 (Illustrative Mathematics)"
        n_items = sum(len(v) for v in tiers.values())
        ref["ladder"] = n_items >= 2
        ref["match"] = "strong" if n_items >= 2 and score >= 4 else "ok" if n_items else "weak"
        if topic["type_id"] == "g6_inequalities_hanger_diagrams":
            ref["note_bits"].append(
                "Open Up Grade 6 hangers are equality balances (Lesson 3, Staying in Balance). "
                "There is not a separate inequality-hanger ladder in that lesson; the comparison is the figure family, not the relation symbol."
            )
        return ref

    if kind == "im":
        cards = matching_im_cards()
        if cards:
            place_im_cards(cards)
            ref["note_bits"].append(
                "These are separate published tasks of the same skill, ordered only by how long the first page is. "
                "They are not a textbook easy/medium/hard exercise list. Hard here may use an earlier theorem; it should not become a different skill."
            )
            return ref
        sections = choose_openstax_sections(topic, generated, slugs, section_cache)
        if sections:
            attach_sections(sections)
            ref["note_bits"].append(
                "No Illustrative Mathematics task was this skill, so the comparison is the OpenStax section whose exercises match."
            )
            return ref
        ref["match"] = "weak"
        return ref

    sections = choose_openstax_sections(topic, generated, slugs, section_cache)
    if not sections:
        cards = matching_im_cards()
        if cards:
            place_im_cards(cards)
            ref["note_bits"].append(
                "No OpenStax section exercise was this skill, so these Illustrative Mathematics tasks are the comparison set."
            )
            return ref
        ref["match"] = "weak"
        return ref
    attach_sections(sections)
    if visual and kind == "openstax":
        has_item_img = any(card.get("saved_images") for cards in ref["tiers"].values() for card in cards)
        if not has_item_img:
            cards = matching_im_cards(limit=1)
            if cards and cards[0].get("image"):
                card = cards[0]
                ref["figures"].append(
                    {
                        "path": card["image"],
                        "alt": card["title"],
                        "caption": "Illustrative Mathematics task (figure sample, not the exercise ladder)",
                        "text": card["text"],
                    }
                )
    return ref


def _im_card(card: dict) -> dict:
    images = []
    if card.get("image"):
        images = [{"path": card["image"], "alt": card.get("title") or ""}]
    return {
        "text": card.get("text") or "",
        "title": card.get("title") or "",
        "heading": card.get("pack") or "",
        "saved_images": images,
        "kind": "im_task",
    }


# ---------------------------------------------------------------------------
# Assessment
# ---------------------------------------------------------------------------

VERB_RE = [
    ("simplify", r"\bsimplif"),
    ("factor", r"\bfactor"),
    ("solve", r"\bsolve"),
    ("graph", r"\bgraph|\bsketch|\bplot"),
    ("evaluate", r"\bevaluat"),
    ("convert", r"\bconvert"),
    ("expand", r"\bexpand"),
    ("prove", r"\bprove"),
    ("construct", r"\bconstruct"),
    ("classify", r"\bclassif"),
    ("compare", r"\bcompare"),
    ("order", r"\border"),
    ("identify", r"\bidentif"),
    ("write", r"\bwrite"),
    ("find", r"\bfind"),
    ("compute", r"\bcomput|\bcalculate"),
]


def primary_verb(text: str) -> str:
    low = (text or "").lower()
    for label, pat in VERB_RE:
        if re.search(pat, low):
            return label
    return ""


def sample_blob(sample: dict) -> str:
    """Student-facing stem only. The answer is shown on the card, not scored as the given."""
    instr = (sample.get("instruction_latex") or "").strip()
    prompt = (sample.get("prompt_latex") or sample.get("prompt_text") or "").strip()
    if instr and instr not in prompt:
        return f"{instr} {prompt}"
    return prompt


def generated_blob(samples: list[dict], tier: str | None = None) -> str:
    rows = samples if tier is None else [s for s in samples if s.get("tier") == tier and not s.get("error")]
    return "\n".join(sample_blob(s) for s in rows)


def ref_blob(ref: dict, tier: str | None = None) -> str:
    tiers = [tier] if tier else list(TIERS)
    parts = []
    for name in tiers:
        for card in ref.get("tiers", {}).get(name) or []:
            parts.append(card.get("text") or "")
    return "\n".join(parts)


def _max_num(text: str) -> int:
    """Largest integer in a stem. Leading exercise numbers like ``63 .`` are not values."""
    cleaned = re.sub(r"(?<![\d.])\d{1,4}\s*\.", " ", text or "")
    nums = [int(n) for n in re.findall(r"\d+", cleaned) if 0 < int(n) < 1000]
    return max(nums) if nums else 0


def _form_adds(easy: str, hard: str) -> list[str]:
    """Ways hard is a heavier form of the same skill, not just a bigger integer."""
    adds = []
    lead = re.compile(r"(?<![\d.])[2-9]\s*[a-zA-Z]\s*\^")
    if lead.search(hard or "") and not lead.search(easy or ""):
        adds.append("a leading coefficient greater than 1")
    if _frac_count(hard) > _frac_count(easy) and _frac_count(easy) == 0:
        adds.append("fractions")
    if re.search(r"\^\s*\{?\s*[3-9]", hard or "") and not re.search(r"\^\s*\{?\s*[3-9]", easy or ""):
        adds.append("a higher power")
    if re.search(r"\\sqrt|\\frac", hard or "") and not re.search(r"\\sqrt|\\frac", easy or ""):
        if "a root or a fraction" not in adds:
            adds.append("a root or a fraction")
    return adds


def _frac_count(text: str) -> int:
    return len(re.findall(r"\\frac|/", text or ""))


def shape_flags(topic: dict, samples: list[dict]) -> list[tuple[str, str]]:
    ok = [s for s in samples if not s.get("error")]
    blob = generated_blob(ok).lower()
    name = (topic["name"] + " " + topic["type_id"]).lower()
    flags: list[tuple[str, str]] = []

    def has(pat: str) -> bool:
        return re.search(pat, blob) is not None

    if re.search(r"logarithm|log_", name) and not has(r"\\log|\\ln|\blog\b"):
        flags.append(("off", "None of the generated prompts use a logarithm."))
    if re.search(r"trigonometr|trig_", name) and not has(r"\\sin|\\cos|\\tan|\bsin\b|\bcos\b|\btan\b"):
        flags.append(("off", "None of the generated prompts use a sine, cosine, or tangent."))
    if re.search(r"derivative|differenti", name) and not has(r"deriv|\\frac\{d|d/dx|f'"):
        flags.append(("off", "None of the generated prompts ask for a derivative."))
    if re.search(r"integral|antideriv", name) and not has(r"\\int|integrat|antideriv"):
        flags.append(("off", "None of the generated prompts ask for an integral."))
    if re.search(r"\blimit", name) and not has(r"\\lim|\blimit\b"):
        flags.append(("off", "None of the generated prompts are limit statements."))
    if re.search(r"matrix|matrices|determinant|cramer", name) and not has(r"matrix|determinant|\\begin\{[pbv]?matrix"):
        flags.append(("partial", "Generated prompts do not show a matrix or a determinant."))
    if re.search(r"inequal", name) and not has(r"\\le|\\ge|\\neq|<|>|≤|≥"):
        flags.append(("off", "The leaf is an inequality, but the generated stems have no inequality sign."))
    if re.search(r"word", name):
        words = re.findall(r"[A-Za-z]{5,}", blob)
        if len(words) < 12:
            flags.append(("partial", "The word-problem leaf is generating mostly bare algebra, not a short situation."))
    if re.search(r"system", name) and not has(r"\\begin\{cases|system"):
        eq = blob.count("=")
        if eq < 2:
            flags.append(("partial", "A system leaf is not showing two equations together."))
    if re.search(r"polynomial", name) and re.search(r"graph", name):
        degs = [int(n) for n in re.findall(r"\^\s*\{?\s*(\d+)", blob)]
        max_deg = max(degs) if degs else (2 if re.search(r"x\^2|x\^\{2\}", blob) else 1)
        if max_deg <= 2:
            flags.append(("partial", "Graphing samples stay at degree 2, so cubics and higher never appear."))
    if re.search(r"hanger|tape|area diagram", name):
        if re.search(r"=|\\le|\\ge", blob) and "diagram" in blob:
            flags.append((
                "partial",
                "The stem prints the equation and also says to use the diagram, so a student can ignore the figure. "
                "The published figure task makes the figure the only place the relationship is written.",
            ))
    return flags


def method_drift(topic: dict, samples: list[dict]) -> str:
    easy = generated_blob(samples, "easy").lower()
    hard = generated_blob(samples, "hard").lower()
    name = (topic["name"] + " " + topic["type_id"]).lower()
    markers = [
        (r"\\log|\\ln", "logarithms"),
        (r"\\sin|\\cos|\\tan", "trigonometry"),
        (r"\\int|\\oint", "integration"),
        (r"\\lim", "limits"),
        (r"\\det|determinant", "determinants"),
        (r"quadratic formula", "the quadratic formula"),
        (r"complet\w* the square", "completing the square"),
    ]
    drifted = []
    for pat, label in markers:
        in_hard = re.search(pat, hard) is not None
        in_easy = re.search(pat, easy) is not None
        in_name = label.split()[-1] in name or label in name
        if in_hard and not in_easy and not in_name:
            drifted.append(label)
    if drifted:
        return "Hard brings in " + ", ".join(drifted) + ", which is a different skill, not a prerequisite of this one."
    # degree jump
    def max_deg(text: str) -> int:
        degs = [int(n) for n in re.findall(r"\^\s*\{?\s*(\d+)", text)]
        return max(degs) if degs else 0
    degree_ok = any(k in name for k in ("deriv", "integrat", "limit", "quadratic", "polynomial"))
    if (
        not degree_ok
        and max_deg(hard) >= max_deg(easy) + 2
        and max_deg(easy) <= 1
    ):
        return "Hard jumps the polynomial degree well past the easy items, so it may have left the skill."
    return ""


def assess(topic: dict, generated: dict, ref: dict) -> dict:
    samples = generated.get("samples") or []
    ok = [s for s in samples if not s.get("error")]
    dims = {
        "skill": "close",
        "given_find": "close",
        "range": "close",
        "variance": "close",
        "graphic": "n/a",
        "hard_same_topic": "close",
    }
    sentences: list[str] = []

    if samples and not ok:
        return {
            "verdict": "generate_failed",
            "dimensions": dims,
            "note": "Every sample failed: " + (samples[0].get("error") or "unknown error"),
        }

    n_published = sum(len(ref.get("tiers", {}).get(t) or []) for t in TIERS)
    if n_published == 0:
        ref["match"] = "weak"
        ref["ladder"] = False
        ref.setdefault("note_bits", []).append(
            "No published item in the matched source is this skill. The ladder is empty instead of being filled with a different task."
        )
    elif n_published < 2:
        ref["ladder"] = False
        ref.setdefault("note_bits", []).append(
            "The published ladder is short: only 1 item is this skill. Unrelated problems were left out."
        )
    sentences.extend(ref.get("note_bits") or [])

    if ref.get("match") == "weak" or n_published == 0:
        # Still describe internal generation so the page is useful.
        templates = {s.get("template") for s in ok if s.get("template")}
        sentences.append(
            "The published match is weak, so this note does not treat the reference as the definition of the skill. "
            f"Across the six generated items there are {len(templates)} stem templates."
        )
        flags = shape_flags(topic, ok)
        for level, text in flags:
            sentences.append(text)
            if level == "off":
                dims["skill"] = "off"
        verdict = "weak_reference" if dims["skill"] != "off" else "off"
        return {"verdict": verdict, "dimensions": dims, "note": " ".join(sentences)}

    gen_easy = generated_blob(ok, "easy")
    gen_hard = generated_blob(ok, "hard")
    ref_easy = ref_blob(ref, "easy") or ref_blob(ref, "medium")
    ref_hard = ref_blob(ref, "hard") or ref_blob(ref, "medium")
    gen_verb = primary_verb(generated_blob(ok))
    ref_verb = primary_verb(ref_blob(ref) + " " + (ref.get("title") or ""))
    flags = shape_flags(topic, ok)

    # Skill. Do not say the skill lines up when a shown card is a different task.
    profile = skill_profile(topic, {"samples": ok})
    published_cards = [card for tier in TIERS for card in (ref.get("tiers", {}).get(tier) or [])]
    mismatched = [
        card
        for card in published_cards
        if not item_matches(
            card.get("text") or "",
            profile,
            heading=card.get("title") or card.get("heading") or "",
            source_text=ref.get("title") or "",
        )
    ]
    if published_cards and len(mismatched) == len(published_cards):
        dims["skill"] = "off"
        sentences.append(
            "The published cards are a different task from the generated question, so this note does not say the skill lines up."
        )
        return {"verdict": "weak_reference", "dimensions": dims, "note": " ".join(sentences)}
    if flags and any(level == "off" for level, _ in flags):
        dims["skill"] = "off"
    elif flags or mismatched:
        dims["skill"] = "partial"
        if mismatched:
            sentences.append(
                "Some published cards are a different task from the generated question, so the skill does not fully line up."
            )
    elif gen_verb and ref_verb and gen_verb != ref_verb and {gen_verb, ref_verb} <= {"solve", "simplify", "factor", "graph", "evaluate", "prove"}:
        dims["skill"] = "partial"
        sentences.append(
            f"Generated items mostly ask the student to {gen_verb}, while the published set mostly asks them to {ref_verb}."
        )
    else:
        sentences.append(
            f"The skill lines up with {ref.get('title') or 'the published set'}: both are about {topic['name'].lower()}."
        )
    for _, text in flags:
        sentences.append(text)

    # Given / find
    first_easy = next((s for s in ok if s.get("tier") == "easy"), ok[0] if ok else None)
    first_ref = None
    for tier_name in TIERS:
        cards = ref.get("tiers", {}).get(tier_name) or []
        if cards:
            first_ref = cards[0]
            break
    gen_preview = clip(sample_blob(first_easy), 160) if first_easy else ""
    ref_preview = clip((first_ref or {}).get("text") or "", 160)
    if any("prints the equation" in text for _, text in flags):
        dims["given_find"] = "partial"
    elif gen_verb == "graph" and ref_verb == "graph":
        sentences.append("Both sides ask for a graph of the same kind of relation. The equation is the given; the graph is what to find.")
    elif ref_preview and gen_preview:
        sentences.append(f"Published easy stem: “{ref_preview}” Generated easy stem: “{gen_preview}”")

    # Range
    g_easy_max, g_hard_max = _max_num(gen_easy), _max_num(gen_hard)
    r_easy_max, r_hard_max = _max_num(ref_easy), _max_num(ref_hard)
    g_forms = _form_adds(gen_easy, gen_hard)
    r_forms = _form_adds(ref_easy, ref_hard)
    g_scales = g_hard_max > max(g_easy_max, 1) * 1.4 or bool(g_forms)
    r_scales = r_hard_max > max(r_easy_max, 1) * 1.4 or bool(r_forms)
    if n_published < 2:
        dims["range"] = "partial"
        sentences.append("The published sample does not span an easy-to-hard ladder of this skill.")
    elif ref.get("ladder"):
        if g_scales and r_scales:
            extra = ""
            if g_forms or r_forms:
                extra = " Hard adds " + ", ".join(g_forms or r_forms) + " rather than only a bigger integer."
            sentences.append(
                f"Difficulty moves on both sides (generated values about {g_easy_max} → {g_hard_max}; "
                f"published values about {r_easy_max} → {r_hard_max}).{extra} "
                "That can include an earlier skill such as fractions or a larger leading coefficient."
            )
        elif r_scales and not g_scales:
            dims["range"] = "partial"
            sentences.append(
                f"Published hard items get heavier (max about {r_easy_max} → {r_hard_max}), "
                f"but generated hard stays near the easy range (max about {g_easy_max} → {g_hard_max})."
            )
        elif g_scales and not r_scales:
            dims["range"] = "partial"
            sentences.append(
                f"Generated numbers grow (max about {g_easy_max} → {g_hard_max}), "
                "while the published hard items change form or context more than the size of the numbers."
            )
        else:
            dims["range"] = "partial"
            sentences.append(
                f"Neither side moves the integers much (generated max {g_easy_max} → {g_hard_max}). "
                "If hard is real, it has to show up as a new form, not as a bigger coefficient."
            )
    else:
        sentences.append(
            "The published items are separate tasks, so there is no numbered easy/medium/hard range to match. "
            f"Generated numbers go from about {g_easy_max} on easy to about {g_hard_max} on hard."
        )
        if not g_scales:
            dims["range"] = "partial"

    # Variance
    templates = {s.get("template") for s in ok if s.get("template")}
    descriptors = {d for s in ok for d in (s.get("descriptors") or []) if d}
    ref_templates = set()
    for tier in TIERS:
        for card in ref.get("tiers", {}).get(tier) or []:
            ref_templates.add(_template(card.get("text") or "")[:160])
    if len(templates) <= 1:
        dims["variance"] = "partial"
        sentences.append(
            f"All generated stems share one template. The published sample has {len(ref_templates)} distinct stems."
        )
    elif len(templates) <= 3 and len(ref_templates) >= 5:
        dims["variance"] = "partial"
        sentences.append(
            f"Generated stems use {len(templates)} templates; the published sample uses about {len(ref_templates)}."
        )
    else:
        sentences.append(
            f"Generated stems use {len(templates)} templates across six items"
            + (f"; figure descriptors: {len(descriptors)}." if descriptors else ".")
        )

    # Graphic
    gen_figs = sum(len(s.get("visuals") or []) for s in ok)
    ref_figs = 0
    ref_alts = set()
    for tier in TIERS:
        for card in ref.get("tiers", {}).get(tier) or []:
            for img in card.get("saved_images") or []:
                ref_figs += 1
                if img.get("alt"):
                    ref_alts.add(img["alt"][:80])
    ref_figs += len(ref.get("figures") or [])
    visual = topic_is_visual(topic, generated) or ref_figs > 0
    if visual:
        if gen_figs and ref_figs:
            dims["graphic"] = "close" if (len(descriptors) >= 2 or not descriptors) else "partial"
            if len(descriptors) <= 1 and gen_figs >= 4:
                dims["graphic"] = "partial"
                sentences.append(
                    "A figure is present on the generated items and on the published items, "
                    "but the generated figures barely change shape from seed to seed."
                )
            else:
                sentences.append(
                    "Both sides use a figure. Compare the published images with the generated drawings for the same kind of object "
                    "(what is labeled, what is given, and how many variants appear)."
                )
                if ref_alts:
                    sentences.append("Published figure notes include: " + "; ".join(list(ref_alts)[:2]) + ".")
        elif ref_figs and not gen_figs:
            dims["graphic"] = "off"
            sentences.append("The published question is carried by a figure. The generated stem is text only.")
        elif gen_figs and not ref_figs:
            dims["graphic"] = "partial"
            sentences.append(
                "We draw a figure, but the excerpt captured from the source did not include a stem image. "
                "Worked-example figures are shown when the section had them."
            )
        else:
            dims["graphic"] = "partial"
            sentences.append("This leaf looks visual, and neither the generated sample nor the captured source excerpt shows a figure.")

    # Hard stays on the skill
    drift = method_drift(topic, ok)
    if drift:
        dims["hard_same_topic"] = "off"
        sentences.append(drift)
    else:
        if g_scales:
            sentences.append(
                "Hard does not switch to a different method. Extra fractions, negatives, or larger coefficients count as earlier skills, not a new topic."
            )
        else:
            sentences.append(
                "Hard stays on the same method as easy. It does not add an earlier skill either (a fraction, a negative, or a second step)."
            )
    # A hard tier that is not ordered (a hard seed easier than a medium seed) is not a ladder.
    def tier_max(tier: str) -> int:
        vals = [_max_num(sample_blob(s)) for s in ok if s.get("tier") == tier]
        return max(vals) if vals else 0
    if tier_max("hard") + 1 < tier_max("medium") and tier_max("medium") > 0:
        dims["range"] = "partial"
        sentences.append(
            f"The tiers are not ordered: medium reaches about {tier_max('medium')}, hard only about {tier_max('hard')}."
        )

    # Roll up. A weak-but-usable match caps the verdict at partial unless everything is close
    # and the match itself is ok/strong.
    rank = {"n/a": 0, "close": 0, "partial": 1, "off": 2}
    worst = max(rank.get(v, 0) for v in dims.values())
    if worst >= 2:
        verdict = "off"
    elif worst == 1:
        verdict = "partial"
    else:
        verdict = "close"
    if ref.get("match") not in {"strong", "ok", "pin"} and verdict == "close":
        verdict = "partial"
    return {"verdict": verdict, "dimensions": dims, "note": " ".join(sentences)}


# ---------------------------------------------------------------------------
# HTML
# ---------------------------------------------------------------------------

def esc(text: str) -> str:
    return html.escape(text or "", quote=True)


def latex_block(src: str) -> str:
    src = (src or "").strip()
    if not src:
        return ""
    if "$" in src:
        return f"<div class='mixed'>{esc(src)}</div>"
    return f"<div class='mixed'>$${esc(src)}$$</div>"


def img_tag(path: str, alt: str) -> str:
    if not path:
        return ""
    return f"<figure><img src='{esc(path)}' alt='{esc(alt)}'/><figcaption>{esc(clip(alt, 220))}</figcaption></figure>"


def render_ref_card(card: dict) -> str:
    bits = ["<div class='card ref'>"]
    title = card.get("title") or card.get("heading") or ""
    if title:
        bits.append(f"<div class='kicker'>{esc(clip(title, 140))}</div>")
    text = card.get("text") or ""
    if text:
        if "$" in text or "\\" in text:
            bits.append(f"<div class='mixed'>{esc(clip(text, 700))}</div>")
        else:
            bits.append(f"<p>{esc(clip(text, 700))}</p>")
    for img in card.get("saved_images") or []:
        bits.append(img_tag(img.get("path") or "", img.get("alt") or title))
    bits.append("</div>")
    return "".join(bits)


def render_gen_card(sample: dict) -> str:
    bits = ["<div class='card gen'>"]
    err = sample.get("error")
    if err:
        bits.append(f"<p class='err'>{esc(err)}</p></div>")
        return "".join(bits)
    diff = sample.get("difficulty")
    diff_s = f" · D={diff}" if diff is not None else ""
    bits.append(f"<div class='kicker'>seed {sample.get('seed')}{esc(str(diff_s))}</div>")
    instr = sample.get("instruction_latex") or ""
    prompt = sample.get("prompt_latex") or sample.get("prompt_text") or ""
    if instr and instr not in prompt:
        bits.append(latex_block(instr))
    bits.append(latex_block(prompt))
    if sample.get("answer_latex"):
        bits.append(f"<div class='ans'>Answer: {latex_block(sample['answer_latex'])}</div>")
    for vis in sample.get("visuals") or []:
        path = OUT / vis["path"]
        if path.exists():
            frag = path.read_text(encoding="utf-8", errors="replace")
            kind = vis.get("kind") or "figure"
            bits.append(f"<div class='fig'><div class='kicker'>{esc(kind)}</div>{frag}</div>")
    bits.append("</div>")
    return "".join(bits)


def render_topic_html(topic: dict, generated: dict, ref: dict, assessment: dict) -> str:
    verdict = assessment.get("verdict") or "partial"
    dims = assessment.get("dimensions") or {}
    dim_html = "".join(
        f"<li><span>{esc(name.replace('_', ' '))}</span> <b>{esc(value)}</b></li>"
        for name, value in dims.items()
        if value != "n/a"
    )
    tier_html = []
    by_tier: dict[str, list[dict]] = defaultdict(list)
    for sample in generated.get("samples") or []:
        by_tier[sample["tier"]].append(sample)
    for tier in TIERS:
        refs = "".join(render_ref_card(c) for c in ref.get("tiers", {}).get(tier) or []) or "<p class='muted'>No published item in this band.</p>"
        gens = "".join(render_gen_card(s) for s in by_tier.get(tier) or []) or "<p class='muted'>No generated item.</p>"
        tier_html.append(
            f"<section class='tier'><h3>{tier}</h3><div class='cols'><div><h4>Published</h4>{refs}</div>"
            f"<div><h4>Generated</h4>{gens}</div></div></section>"
        )
    figures = []
    for fig in ref.get("figures") or []:
        figures.append(
            "<div class='card ref'>"
            + img_tag(fig.get("path") or "", fig.get("alt") or fig.get("caption") or "")
            + f"<p>{esc(clip(fig.get('text') or '', 280))}</p></div>"
        )
    fig_block = ""
    if figures:
        fig_block = "<section class='tier'><h3>Worked figures from the same source</h3><div class='cols'>" + "".join(figures) + "</div></section>"
    ladder = "exercise ladder" if ref.get("ladder") else "task set, not a numbered ladder"
    src = (
        f"<p class='src'><b>{esc(ref.get('source_name') or 'No source')}</b> · {esc(ladder)} · "
        f"match {esc(ref.get('match') or '')} · {esc(ref.get('license') or '')} · consulted {CONSULTED}<br>"
        f"{esc(ref.get('title') or '')}<br>"
        f"<a href='{esc(ref.get('url') or '')}'>{esc(ref.get('url') or '')}</a></p>"
    )
    return (
        f"<article id='{esc(topic['type_id'])}' class='topic v-{esc(verdict)}'>"
        f"<header><h2>{esc(topic['name'])} <code>{esc(topic['type_id'])}</code></h2>"
        f"<p class='meta'>{esc(topic['course_name'])} · {esc(topic['chapter_name'])} · "
        f"<b class='badge'>{esc(verdict)}</b></p>"
        f"<ul class='dims'>{dim_html}</ul>"
        f"<p class='note'>{esc(assessment.get('note') or '')}</p>"
        f"<p class='gap'>{esc((assessment.get('in_topic_gap') or {}).get('note') or '')}</p>"
        f"{src}</header>"
        + "".join(tier_html)
        + fig_block
        + "</article>"
    )


CSS = """
body { font: 16px/1.45 Georgia, serif; margin: 0; color: #1c1917; background: #fafaf9; }
header.top, main { max-width: 1100px; margin: 0 auto; padding: 24px; }
h1 { font: 600 28px/1.2 system-ui, sans-serif; }
h2 { font: 600 20px/1.3 system-ui, sans-serif; margin: 0 0 6px; }
h3 { font: 600 15px/1.2 system-ui, sans-serif; text-transform: uppercase; letter-spacing: .04em; }
h4 { font: 600 13px/1.2 system-ui, sans-serif; margin: 0 0 6px; color: #57534e; }
code { font-size: 13px; }
a { color: #1d4ed8; }
.topic { background: white; border: 1px solid #e7e5e4; border-left: 6px solid #a8a29e; margin: 18px 0; padding: 16px 18px 8px; }
.v-close { border-left-color: #15803d; }
.v-partial { border-left-color: #b45309; }
.v-off { border-left-color: #b91c1c; }
.v-weak_reference { border-left-color: #6d28d9; }
.v-generate_failed { border-left-color: #111; }
.badge { text-transform: uppercase; letter-spacing: .04em; font-size: 12px; }
.note { background: #f5f5f4; padding: 10px 12px; }
.gap { background: #fff7ed; border: 1px solid #fed7aa; padding: 8px 12px; margin: 8px 0; }
.dims { display: flex; flex-wrap: wrap; gap: 8px 14px; padding: 0; list-style: none; font: 13px system-ui, sans-serif; }
.dims li { background: #f5f5f4; padding: 3px 8px; }
.cols { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.card { border: 1px solid #e7e5e4; padding: 8px 10px; margin: 0 0 8px; background: #fff; overflow: auto; }
.card.ref { background: #f8fafc; }
.kicker { font: 12px system-ui, sans-serif; color: #57534e; margin-bottom: 4px; }
.muted, .src, .meta { color: #44403c; font: 14px/1.4 system-ui, sans-serif; }
.err { color: #b91c1c; }
img, svg { max-width: 100%; height: auto; }
figure { margin: 8px 0; }
figcaption { font: 12px/1.35 system-ui, sans-serif; color: #44403c; }
table { border-collapse: collapse; width: 100%; font: 14px system-ui, sans-serif; }
td, th { border-bottom: 1px solid #e7e5e4; text-align: left; padding: 4px 6px; vertical-align: top; }
.counts { display: flex; gap: 12px; flex-wrap: wrap; }
.counts div { background: white; border: 1px solid #e7e5e4; padding: 8px 12px; }
@media (max-width: 800px) { .cols { grid-template-columns: 1fr; } }
"""


def katex_tags(html_path: Path) -> str:
    from scripts.topic_fit_katex import katex_head_html

    return katex_head_html(html_path)


def write_html_page(path: Path, title: str, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    doc = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/>
<title>{esc(title)}</title>
{katex_tags(path)}
<style>{CSS}</style>
</head><body>
{body}
</body></html>
"""
    path.write_text(doc, encoding="utf-8")


def write_pack(
    topics: list[dict],
    generated: dict[str, dict],
    refs: dict[str, dict],
    assessments: dict[str, dict],
    foundations: list[str],
) -> None:
    by_course: dict[str, list[dict]] = defaultdict(list)
    for topic in topics:
        by_course[topic["course_id"]].append(topic)
    counts: dict[str, int] = defaultdict(int)
    visual_n = 0
    for topic in topics:
        verdict = assessments[topic["type_id"]]["verdict"]
        counts[verdict] += 1
        if topic_is_visual(topic, generated.get(topic["type_id"])):
            visual_n += 1

    course_links = []
    for course_id, rows in by_course.items():
        page = OUT / f"{course_id}.html"
        parts = [
            "<header class='top'>",
            f"<p><a href='index.html'>All courses</a></p>",
            f"<h1>{esc(rows[0]['course_name'])}</h1>",
            f"<p class='meta'>{len(rows)} topics. Open a topic and compare the published column with the generated column at easy, medium, and hard.</p>",
            "</header><main>",
        ]
        rows_sorted = sorted(rows, key=lambda t: (t["chapter_name"], t["name"]))
        for topic in rows_sorted:
            parts.append(
                render_topic_html(
                    topic,
                    generated[topic["type_id"]],
                    refs[topic["type_id"]],
                    assessments[topic["type_id"]],
                )
            )
        parts.append("</main>")
        write_html_page(page, rows[0]["course_name"], "".join(parts))
        course_links.append((rows[0]["course_name"], f"{course_id}.html", len(rows)))

    # Spotlight: a few topics a person can open first.
    spotlight_ids = [
        "g6_equations_hanger_diagrams",
        "g6_equations_tape_diagrams",
        "g6_interpreting_histograms",
        "g6_decimal_addition_with_diagrams",
        "quadratic_factoring",
        "a2_polynomial_functions_graphing",
        "geo_congruent_proving_triangles_congruent",
        "geo_right_pythagorean_theorem",
    ]
    by_id = {t["type_id"]: t for t in topics}
    spot_topics = [by_id[i] for i in spotlight_ids if i in by_id]
    # plus first off and first close if not already included
    for want in ("off", "close", "partial"):
        for topic in topics:
            if assessments[topic["type_id"]]["verdict"] == want and topic not in spot_topics:
                spot_topics.append(topic)
                break
    spot_body = [
        "<header class='top'><p><a href='index.html'>All courses</a></p>",
        "<h1>Spotlight</h1>",
        "<p class='meta'>A short set: hanger and tape figures, a data plot, factoring, polynomial graphing, a congruence task, and the Pythagorean theorem.</p>",
        "</header><main>",
    ]
    for topic in spot_topics:
        spot_body.append(
            render_topic_html(
                topic,
                generated[topic["type_id"]],
                refs[topic["type_id"]],
                assessments[topic["type_id"]],
            )
        )
    spot_body.append("</main>")
    write_html_page(OUT / "spotlight.html", "Alignment spotlight", "".join(spot_body))

    gap_rows = []
    for topic in topics:
        gap = assessments[topic["type_id"]].get("in_topic_gap") or {}
        missing = gap.get("missing") or []
        if missing:
            gap_rows.append((len(missing), topic, gap))
    gap_rows.sort(key=lambda row: (-row[0], row[1]["name"]))
    clearest = [
        {
            "type_id": topic["type_id"],
            "name": topic["name"],
            "course": topic["course_name"],
            "generated": gap.get("generated") or [],
            "missing": gap.get("missing") or [],
        }
        for _, topic, gap in gap_rows[:12]
    ]
    gap_list = "".join(
        f"<li><a href='{esc(topic['course_id'])}.html#{esc(topic['type_id'])}'>{esc(topic['name'])}</a> "
        f"({esc(topic['course_name'])}): {esc('; '.join(gap.get('missing') or []))}</li>"
        for _, topic, gap in gap_rows[:12]
    )
    count_boxes = "".join(f"<div><b>{n}</b><br>{esc(k)}</div>" for k, n in sorted(counts.items()))
    count_boxes += f"<div><b>{len(gap_rows)}</b><br>in-topic forms not generated</div>"
    rows_html = []
    for topic in topics:
        verdict = assessments[topic["type_id"]]["verdict"]
        visual = "figure" if topic_is_visual(topic, generated.get(topic["type_id"])) else ""
        href = f"{topic['course_id']}.html#{topic['type_id']}"
        rows_html.append(
            f"<tr><td><a href='{esc(href)}'>{esc(topic['name'])}</a><br><code>{esc(topic['type_id'])}</code></td>"
            f"<td>{esc(topic['course_name'])}</td><td>{esc(topic['chapter_name'])}</td>"
            f"<td>{esc(verdict)}</td><td>{esc(visual)}</td></tr>"
        )
    index_body = f"""
<header class='top'>
<h1>Published problems vs generated problems</h1>
<p>Every wired curriculum leaf, two generated items at easy, medium, and hard, next to a small published sample.
OpenStax and Illustrative Mathematics / Open Up text is quoted (those licenses allow it). Figure stems include the source image.
Hard means the same skill, and it may use an earlier prerequisite. It does not mean the next chapter.</p>
<p class='meta'>Foundations leaves with no <code>type_id</code> are not generated: {esc(", ".join(foundations) or "none")}.</p>
<div class='counts'>{count_boxes}<div><b>{visual_n}</b><br>visual leaves</div></div>
<p><a href='spotlight.html'>Open the spotlight first</a> (hangers, tape diagrams, histograms, factoring, graphing, congruence).</p>
<p><b>{len(gap_rows)}</b> topics have at least one in-topic form the generator does not emit. Clearest gaps:</p>
<ul>
{gap_list or "<li>none seen</li>"}
</ul>
<ul>
{''.join(f"<li><a href='{esc(href)}'>{esc(name)}</a> ({n})</li>" for name, href, n in course_links)}
</ul>
</header>
<main>
<table>
<thead><tr><th>Topic</th><th>Course</th><th>Chapter</th><th>Verdict</th><th>Figure</th></tr></thead>
<tbody>
{''.join(rows_html)}
</tbody>
</table>
</main>
"""
    write_html_page(OUT / "index.html", "Alignment pack", index_body)

    summary = {
        "consulted": CONSULTED,
        "topics": len(topics),
        "counts": dict(counts),
        "visual_leaves": visual_n,
        "foundations_without_type": foundations,
        "courses": {name: n for name, _, n in course_links},
        "in_topic_not_generated": {
            "topics_with_a_gap": len(gap_rows),
            "topics_none_seen": len(topics) - len(gap_rows),
            "clearest_gaps": clearest,
        },
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    readme = f"""# Published vs generated

Open `index.html` (or `spotlight.html` for a short visual pass).

{len(topics)} wired leaves. Verdict counts: {json.dumps(dict(counts))}.
Visual leaves (name or a generated figure): {visual_n}.
Topics with an in-topic form the generator does not emit: {len(gap_rows)}.

## What a row is

- **Published:** two items at easy, medium, and hard when the source has an exercise ladder
  (OpenStax section order, or Open Up practice-problem order). Illustrative Mathematics
  geometry tasks are a task set, not a numbered ladder; the note says so.
- **Generated:** live `_generate_for_type` at easy / medium / hard, seeds 101 and 207,
  with diagrams and graph metadata turned on.
- **Verdict:** `close`, `partial`, `off`, `weak_reference`, or `generate_failed`.
  Hard must stay on the same skill. Fractions, negatives, and larger coefficients
  count as earlier prerequisites.

## Sources (consulted {CONSULTED})

| Source | License | Used for |
| --- | --- | --- |
| OpenStax Prealgebra, Elementary Algebra, Intermediate Algebra, Precalculus, Calculus Volumes 1–3 | {OPENSTAX_LICENSE} | Algebra, prealgebra, precalculus, calculus, and computational geometry |
| Open Up Resources Grade 6 (Illustrative Mathematics lessons) | {OUR_LICENSE} | Grade 6, including hanger, tape, area, and data figures |
| Illustrative Mathematics task PDFs | {IM_LICENSE} | Geometry figures and proofs, and a fallback when an OpenStax section match is weak |

Foundations leaves have no `type_id`, so they are listed and not generated.

Regenerate:

```
QE_LOG_GENERATED=0 PYTHONPATH=. python scripts/build_alignment_pack.py
```

Downloaded pages and PDFs stay in `textbooks/alignment_cache/` (gitignored). The HTML pack quotes short excerpts and stores the figures it shows.
"""
    (OUT / "README.md").write_text(readme, encoding="utf-8")
    log(
        f"wrote {OUT / 'index.html'} counts={dict(counts)} visual={visual_n} "
        f"in_topic_gaps={len(gap_rows)}"
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--only", default="", help="Comma-separated type_ids")
    parser.add_argument("--phase", choices=["match", "all"], default="all")
    parser.add_argument("--force-generate", action="store_true")
    args = parser.parse_args(argv)

    ensure_dirs()
    topics, foundations = wired_topics(parse_curriculum())
    if args.only:
        want = {p.strip() for p in args.only.split(",") if p.strip()}
        topics = [t for t in topics if t["type_id"] in want]
        missing = want - {t["type_id"] for t in topics}
        if missing:
            log(f"unknown type_ids: {sorted(missing)}")
    log(f"{len(topics)} topics")

    slugs = slug_index()
    our_catalog = our_lesson_catalog()
    # IM filenames are only needed when a topic's plan uses them or as a weak-match rescue.
    # Download during all-phase; match-phase uses filenames if the cache exists.
    im_files: list[dict] = []
    if args.phase == "all" or (CACHE / "im_files.json").exists():
        im_files = ensure_im_filenames()

    if args.phase == "match":
        weak = 0
        for topic in topics:
            kind = source_kind(topic)
            if kind == "our":
                lesson, score = best_our_lesson(topic, our_catalog)
                title = lesson["title"] if lesson else "—"
                quality = "strong" if score >= 4 else "ok" if score >= 2.2 else "weak"
                log(f"{quality:6} OUR {score:5.1f} {topic['type_id'][:48]:48} u{lesson['unit'] if lesson else '?'}-l{lesson['lesson'] if lesson else '?'} {title}")
            elif kind == "im":
                chosen = best_im_files(topic, im_files, k=1) if im_files else []
                if chosen:
                    log(f"im     {chosen[0]['score']:5.1f} {topic['type_id'][:48]:48} {chosen[0]['name']}")
                else:
                    spec, score, quality = best_openstax(topic, slugs)
                    log(f"im→os  {quality:6} {score:5.1f} {topic['type_id'][:48]:48} {spec[:1]}")
            else:
                spec, score, quality = best_openstax(topic, slugs)
                if quality == "weak":
                    weak += 1
                log(f"{quality:6} {score:5.1f} {topic['type_id'][:48]:48} {spec[:1]}")
        log(f"weak openstax pins among printed rows: see weak lines")
        return 0

    generated = generate_all(topics, force=args.force_generate)
    section_cache: dict[tuple[str, str], dict] = {}
    refs: dict[str, dict] = {}
    assessments: dict[str, dict] = {}
    for i, topic in enumerate(topics, 1):
        ref = build_reference(topic, generated.get(topic["type_id"], {}), slugs, our_catalog, im_files, section_cache)
        assessment = assess(topic, generated.get(topic["type_id"], {"samples": []}), ref)
        cards = [card for tier in TIERS for card in (ref.get("tiers", {}).get(tier) or [])]
        assessment["in_topic_gap"] = in_topic_not_generated(
            topic,
            (generated.get(topic["type_id"]) or {}).get("samples") or [],
            cards,
        )
        refs[topic["type_id"]] = ref
        assessments[topic["type_id"]] = assessment
        if i % 20 == 0 or i == len(topics):
            log(f"  assessed {i}/{len(topics)} last={topic['type_id']} {assessment['verdict']}")
    # Drop bulky item image URLs before optional debug dump
    write_pack(topics, generated, refs, assessments, foundations)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
