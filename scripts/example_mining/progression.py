"""Build a cross-section progression graph from mirrored OpenStax HTML.

Two graph views:
  1. Reading order — textbook chapter/section sequence (reference only).
  2. Prerequisite DAG — curated actual prerequisites from prerequisites/*.json.

Chapter-intro nodes appear in reading order only, not in the prerequisite DAG.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from pathlib import Path

from bs4 import BeautifulSoup

from scripts.example_mining.prerequisite_loader import (
    build_prerequisite_edges,
    full_node_id,
    load_prerequisite_map,
    split_full_node_id,
    validate_prerequisite_map,
)
ROOT = Path(__file__).resolve().parents[2]

_WS = re.compile(r"\s+")
_SECTION_SLUG = re.compile(r"^(\d+)-(\d+)-(.+)$")
_INTRO_SLUG = re.compile(r"^(\d+)-introduction$")
_OBJECTIVE_LEAD = re.compile(r"^\d+(\.\d+)+\s*")

# Chapter titles in the embedded TOC render as:
#   <span class="os-number">2</span> <span class="os-divider"> </span>
#   <span class="os-text">Limits</span>
_CHAPTER_TITLE = re.compile(
    r'os-number\\">(\d+)\\u003c.*?os-text\\"[^>]*>([^<\\]{2,60})\\u003c',
    re.S,
)


def extract_chapter_titles(html: str) -> dict[int, str]:
    """Map chapter number -> chapter name from a page's embedded TOC JSON."""
    titles: dict[int, str] = {}
    for num, name in _CHAPTER_TITLE.findall(html):
        n = int(num)
        clean = _WS.sub(" ", name).strip()
        if n not in titles and clean:
            titles[n] = clean
    return titles


def _norm(text: str) -> str:
    return _WS.sub(" ", text).strip()


@dataclass
class SectionNode:
    node_id: str  # e.g. c1s2
    book: str
    chapter: int
    section: int | None  # None for chapter intro
    slug: str
    title: str
    objectives: list[str] = field(default_factory=list)


@dataclass
class BookProgression:
    book: str
    display_name: str
    nodes: list[SectionNode] = field(default_factory=list)
    chapter_titles: dict[int, str] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "book": self.book,
            "display_name": self.display_name,
            "chapter_titles": {str(k): v for k, v in self.chapter_titles.items()},
            "nodes": [asdict(n) for n in self.nodes],
        }


def _extract_title_objectives(html_path: Path) -> tuple[str, list[str]]:
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8", errors="replace"), "html.parser")
    main = soup.find(id="main-content") or soup

    title = html_path.stem
    for sel in ("h1", "[data-type=document-title]", "h2"):
        el = main.select_one(sel)
        if el:
            cand = _norm(el.get_text(" ", strip=True))
            if cand and cand.lower() != "none":
                title = cand
                break

    objectives: list[str] = []
    abstract = main.select_one("[data-type=abstract]")
    if abstract:
        for li in abstract.select("li"):
            t = _norm(li.get_text(" ", strip=True))
            if t:
                objectives.append(t)
    return title, objectives


def _clean_objective(obj: str) -> str:
    return _OBJECTIVE_LEAD.sub("", obj).strip()


_TITLE_LEAD_NUM = re.compile(r"^\d+(\.\d+)?\s+")


def _strip_leading_number(title: str) -> str:
    return _TITLE_LEAD_NUM.sub("", title).strip()


def _build_curriculum_unit_progression(
    book_id: str,
    display_name: str,
    units: list[tuple[str, int, str]],
) -> BookProgression:
    prog = BookProgression(book=book_id, display_name=display_name)
    for node_id, chapter, title in units:
        prog.chapter_titles[chapter] = title
        prog.nodes.append(
            SectionNode(
                node_id=node_id,
                book=book_id,
                chapter=chapter,
                section=1,
                slug=node_id,
                title=title,
                objectives=[],
            )
        )
    return prog


def build_grade_6_progression() -> BookProgression:
    """Build Grade 6 nodes from curriculum units (no OpenStax HTML book)."""
    from scripts.example_mining.grade_6_units import BOOK_ID, DISPLAY_NAME, GRADE_6_UNITS

    return _build_curriculum_unit_progression(BOOK_ID, DISPLAY_NAME, GRADE_6_UNITS)


def build_foundations_progression() -> BookProgression:
    """Build pre-grade-6 foundation nodes for number/fraction prerequisites."""
    from scripts.example_mining.grade_6_units import (
        FOUNDATIONS_BOOK_ID,
        FOUNDATIONS_DISPLAY_NAME,
        FOUNDATIONS_UNITS,
    )

    return _build_curriculum_unit_progression(
        FOUNDATIONS_BOOK_ID, FOUNDATIONS_DISPLAY_NAME, FOUNDATIONS_UNITS
    )


def build_geometry_progression() -> BookProgression:
    """Build Geometry nodes from curriculum units (no OpenStax HTML book)."""
    from scripts.example_mining.grade_6_units import (
        GEOMETRY_BOOK_ID,
        GEOMETRY_DISPLAY_NAME,
        GEOMETRY_UNITS,
    )

    return _build_curriculum_unit_progression(GEOMETRY_BOOK_ID, GEOMETRY_DISPLAY_NAME, GEOMETRY_UNITS)


def build_book_progression(book: str, display_name: str, html_root: Path) -> BookProgression:
    book_dir = html_root / book
    prog = BookProgression(book=book, display_name=display_name)

    intro_files: dict[int, Path] = {}
    section_files: dict[tuple[int, int], tuple[str, Path]] = {}

    for path in book_dir.glob("*.html"):
        slug = path.stem
        m = _SECTION_SLUG.match(slug)
        if m:
            chapter = int(m.group(1))
            section = int(m.group(2))
            section_files[(chapter, section)] = (slug, path)
            continue
        mi = _INTRO_SLUG.match(slug)
        if mi:
            intro_files[int(mi.group(1))] = path

    # Chapter names from the embedded TOC on any mirrored page.
    for probe in list(intro_files.values()) + [pth for _, pth in section_files.values()]:
        try:
            prog.chapter_titles = extract_chapter_titles(
                probe.read_text(encoding="utf-8", errors="replace")
            )
        except Exception:
            prog.chapter_titles = {}
        if prog.chapter_titles:
            break

    chapters = sorted({c for c, _ in section_files} | set(intro_files))
    for chapter in chapters:
        if chapter in intro_files:
            path = intro_files[chapter]
            title, objs = _extract_title_objectives(path)
            ch_name = prog.chapter_titles.get(chapter)
            intro_title = f"{ch_name} (overview)" if ch_name else title
            prog.nodes.append(
                SectionNode(
                    node_id=f"c{chapter}intro",
                    book=book,
                    chapter=chapter,
                    section=None,
                    slug=path.stem,
                    title=intro_title,
                    objectives=[_clean_objective(o) for o in objs],
                )
            )
        sections = sorted(s for (c, s) in section_files if c == chapter)
        for section in sections:
            slug, path = section_files[(chapter, section)]
            title, objs = _extract_title_objectives(path)
            prog.nodes.append(
                SectionNode(
                    node_id=f"c{chapter}s{section}",
                    book=book,
                    chapter=chapter,
                    section=section,
                    slug=slug,
                    title=_strip_leading_number(title),
                    objectives=[_clean_objective(o) for o in objs],
                )
            )
    return prog


def _mermaid_id(node_id: str) -> str:
    return node_id


def _mermaid_node_ref(book: str, node_id: str) -> str:
    return f"{book.replace('-', '_')}_{node_id}"


def build_reading_order_edges(progs: list[BookProgression]) -> list[tuple[str, str]]:
    """Textbook sequence edges as (from_full_id, to_full_id)."""
    edges: list[tuple[str, str]] = []
    prev_book_last: str | None = None
    for prog in progs:
        ordered = prog.nodes
        for a, b in zip(ordered, ordered[1:]):
            edges.append((full_node_id(prog.book, a.node_id), full_node_id(prog.book, b.node_id)))
        if prev_book_last and ordered:
            edges.append((prev_book_last, full_node_id(prog.book, ordered[0].node_id)))
        if ordered:
            prev_book_last = full_node_id(prog.book, ordered[-1].node_id)
    return edges


def _node_lookup(progs: list[BookProgression]) -> dict[str, SectionNode]:
    out: dict[str, SectionNode] = {}
    for prog in progs:
        for n in prog.nodes:
            out[full_node_id(prog.book, n.node_id)] = n
    return out


def _prereq_dag_node_ids(
    prereq_edges: list[tuple[str, str]],
    maps: dict[str, dict],
) -> set[str]:
    ids: set[str] = set()
    for a, b in prereq_edges:
        ids.add(a)
        ids.add(b)
    for book, book_map in maps.items():
        for dependent, entry in book_map.items():
            ids.add(dependent)
            ids.update(entry.requires)
    return ids


def reading_order_to_mermaid(progs: list[BookProgression]) -> str:
    lines = ["```mermaid", "flowchart LR"]
    for prog in progs:
        safe_book = prog.book.replace("-", "_")
        lines.append(f"  subgraph {safe_book} [{prog.display_name}]")
        chapters: dict[int, list[SectionNode]] = {}
        for n in prog.nodes:
            chapters.setdefault(n.chapter, []).append(n)
        for chapter in sorted(chapters):
            nodes = chapters[chapter]
            ch_id = f"{safe_book}_ch{chapter}"
            ch_title = prog.chapter_titles.get(chapter) or f"Chapter {chapter}"
            lines.append(f"    subgraph {ch_id} [\"Ch {chapter}: {_mermaid_label(ch_title)}\"]")
            for n in nodes:
                label = _mermaid_label(n.title)
                lines.append(f"      {_mermaid_node_ref(prog.book, n.node_id)}[\"{label}\"]")
            lines.append("    end")
        lines.append("  end")
    for a, b in build_reading_order_edges(progs):
        book_a, id_a = split_full_node_id(a)
        book_b, id_b = split_full_node_id(b)
        lines.append(f"  {_mermaid_node_ref(book_a, id_a)} --> {_mermaid_node_ref(book_b, id_b)}")
    lines.append("```")
    return "\n".join(lines)


def _prereq_depth(full_id: str, edges: list[tuple[str, str]], memo: dict[str, int]) -> int:
    """Longest path length from a root (for left-to-right mermaid ordering)."""
    if full_id in memo:
        return memo[full_id]
    preds = [a for a, b in edges if b == full_id]
    if not preds:
        memo[full_id] = 0
        return 0
    memo[full_id] = 1 + max(_prereq_depth(p, edges, memo) for p in preds)
    return memo[full_id]


def prerequisite_dag_to_mermaid(
    progs: list[BookProgression],
    prereq_edges: list[tuple[str, str]],
    maps: dict[str, dict],
) -> str:
    """Render prerequisite → dependent left-to-right (flowchart LR)."""
    lookup = _node_lookup(progs)
    active = _prereq_dag_node_ids(prereq_edges, maps)
    depth_memo: dict[str, int] = {}
    ordered = sorted(
        (fid for fid in active if fid in lookup),
        key=lambda fid: (
            _prereq_depth(fid, prereq_edges, depth_memo),
            split_full_node_id(fid)[0],
            fid,
        ),
    )
    lines = ["```mermaid", "flowchart LR"]
    for full_id in ordered:
        n = lookup[full_id]
        label = _mermaid_label(n.title)
        lines.append(f"  {_mermaid_node_ref(n.book, n.node_id)}[\"{label}\"]")
    for prereq, dependent in prereq_edges:
        if prereq in lookup and dependent in lookup:
            book_p, id_p = split_full_node_id(prereq)
            book_d, id_d = split_full_node_id(dependent)
            lines.append(
                f"  {_mermaid_node_ref(book_p, id_p)} --> {_mermaid_node_ref(book_d, id_d)}"
            )
    lines.append("```")
    return "\n".join(lines)


def progression_to_mermaid(progs: list[BookProgression]) -> str:
    """Legacy single-graph export: reading order only."""
    return reading_order_to_mermaid(progs)


def _mermaid_label(text: str) -> str:
    t = text.replace('"', "'")
    t = re.sub(r"^\d+(\.\d+)?\s*", "", t)  # drop leading numbering
    if len(t) > 46:
        t = t[:43] + "..."
    return t


def progression_to_markdown(
    progs: list[BookProgression],
    prereq_edges: list[tuple[str, str]] | None = None,
    prereq_reasons: dict[str, str] | None = None,
    maps: dict[str, dict] | None = None,
) -> str:
    lines: list[str] = []
    title_books = ", ".join(p.display_name for p in progs)
    lines.append(f"# Cross-section progression — {title_books}")
    lines.append("")
    lines.append("Two views: **reading order** (textbook sequence) and **prerequisite DAG** (curated actual dependencies).")
    lines.append("Chapter intros and motivational sections (e.g. Preview of Calculus) appear in reading order only.")
    lines.append("")

    if prereq_edges is not None and maps is not None:
        lines.append("## Prerequisite DAG")
        lines.append("")
        lines.append(
            "Edges show actual prerequisites only — sibling topics are not chained by textbook order. "
            "Layout is left-to-right: prerequisites on the left, dependents on the right."
        )
        lines.append("")
        lines.append(prerequisite_dag_to_mermaid(progs, prereq_edges, maps))
        lines.append("")
        if prereq_reasons:
            lines.append("### Prerequisite notes")
            lines.append("")
            lookup = _node_lookup(progs)
            for dep in sorted(prereq_reasons):
                if dep not in lookup:
                    continue
                n = lookup[dep]
                if n.book in {"foundations_math", "grade_6_math", "geometry"}:
                    tag = _mermaid_label(n.title)
                elif n.section is None:
                    tag = f"intro {_mermaid_label(n.title)}"
                else:
                    tag = f"{n.chapter}.{n.section} {_mermaid_label(n.title)}"
                lines.append(f"- **{tag}**: {prereq_reasons[dep]}")
            lines.append("")

    lines.append("## Reading order")
    lines.append("")
    lines.append("Textbook chapter/section sequence for reference.")
    lines.append("")
    lines.append(reading_order_to_mermaid(progs))
    lines.append("")

    for prog in progs:
        lines.append(f"## {prog.display_name} (`{prog.book}`)")
        lines.append("")
        current_ch: int | None = None
        for n in prog.nodes:
            if n.chapter != current_ch:
                current_ch = n.chapter
                lines.append(f"### Chapter {n.chapter}")
                lines.append("")
            tag = "intro" if n.section is None else f"{n.chapter}.{n.section}"
            lines.append(f"- **{tag} {_strip_leading_number(n.title) if n.section else n.title}**")
            for o in n.objectives:
                lines.append(f"  - {o}")
        lines.append("")
    return "\n".join(lines)


def build_progression_output(progs: list[BookProgression]) -> dict:
    """Build full JSON-serializable output with both edge types."""
    maps: dict[str, dict] = {}
    for prog in progs:
        book_map = load_prerequisite_map(prog.book)
        if book_map:
            maps[prog.book] = book_map

    prereq_edges, prereq_reasons = build_prerequisite_edges(maps)
    reading_edges = build_reading_order_edges(progs)

    known_full = {full_node_id(p.book, n.node_id) for p in progs for n in p.nodes}
    warnings: list[str] = []
    for prog in progs:
        if prog.book in maps:
            known = {n.node_id for n in prog.nodes}
            warnings.extend(
                validate_prerequisite_map(prog.book, known, maps[prog.book], known_full)
            )

    return {
        "books": [pr.to_dict() for pr in progs],
        "reading_order_edges": [[a, b] for a, b in reading_edges],
        "prerequisite_edges": [[a, b] for a, b in prereq_edges],
        "prerequisite_reasons": prereq_reasons,
        "validation_warnings": warnings,
    }
