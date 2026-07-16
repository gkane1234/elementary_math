"""Parse a local OpenStax HTML page into an inspectable question inventory."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

from scripts.example_mining.mathml_to_latex import mathml_to_latex

ROOT = Path(__file__).resolve().parents[2]


@dataclass
class ExtractedItem:
    item_id: str
    kind: str  # example | checkpoint | section_exercise | other_exercise
    title: str | None
    position: int
    nearest_heading: str | None
    prompt_text: str
    prompt_latex_bits: list[str]
    has_solution: bool
    source_anchor: str | None
    notes: str = ""


@dataclass
class SectionInventory:
    book: str
    slug: str
    title: str
    source_url: str
    local_path: str
    objectives: list[str]
    headings: list[str]
    items: list[ExtractedItem] = field(default_factory=list)
    extracted_at: str = ""
    stage: str = "1_inventory"

    def to_dict(self) -> dict:
        d = asdict(self)
        return d


def _norm_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _replace_math_with_latex(root: Tag) -> tuple[str, list[str]]:
    """Clone-like: mutate a soup subtree, replace <math> with $latex$, return text + latex list."""
    latex_bits: list[str] = []
    for math in list(root.find_all("math")):
        raw = str(math)
        latex = mathml_to_latex(raw)
        if latex:
            latex_bits.append(latex)
            math.replace_with(NavigableString(f" ${latex}$ "))
        else:
            math.replace_with(NavigableString(" [math] "))
    # Drop solutions / answers if present inside the subtree
    for sol in list(root.select("[data-type=solution], .os-solution-container, [data-type=commentary]")):
        sol.decompose()
    return _norm_ws(root.get_text(" ", strip=True)), latex_bits


_SKIP_HEADINGS = re.compile(
    r"^(learning objectives|solution|media|try it|hint|answer|"
    r"example\s+\d+(\.\d+)?|checkpoint\s+\d+(\.\d+)?)$",
    re.I,
)


def _nearest_heading(node: Tag) -> str | None:
    for prev in node.find_all_previous(["h2", "h3", "h4"]):
        t = _norm_ws(prev.get_text(" ", strip=True))
        if not t or _SKIP_HEADINGS.match(t):
            continue
        return t
    return None


def _problem_root_from_example(example: Tag) -> Tag:
    """Prefer the example's problem section; strip solutions."""
    # OpenStax examples are often: header + section(problem) + details(solution)
    for child in example.children:
        if isinstance(child, Tag) and child.name == "section":
            return child
    exercise = example.select_one("[data-type=exercise]")
    if exercise is not None:
        section = None
        for child in exercise.children:
            if isinstance(child, Tag) and child.name == "section":
                section = child
                break
        return section or exercise
    return example


def _item_kind(exercise: Tag) -> tuple[str, str | None]:
    """Return (kind, title) for an exercise node."""
    for a in exercise.parents:
        if not isinstance(a, Tag):
            continue
        dt = a.get("data-type")
        classes = a.get("class") or []
        if dt == "example":
            title_el = a.select_one(".os-title, [data-type=title], header")
            title = _norm_ws(title_el.get_text(" ", strip=True)) if title_el else None
            return "example", title
        if dt == "note" and "checkpoint" in classes:
            title_el = a.select_one(".os-title, [data-type=title], header")
            title = _norm_ws(title_el.get_text(" ", strip=True)) if title_el else None
            return "checkpoint", title
        if dt == "note":
            title_el = a.select_one(".os-title, [data-type=title], header")
            title = _norm_ws(title_el.get_text(" ", strip=True)) if title_el else None
            return "other_exercise", title
    return "section_exercise", None


def parse_section_html(
    html_path: Path,
    *,
    book: str,
    slug: str,
) -> SectionInventory:
    html = html_path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find(id="main-content") or soup.find("main") or soup

    title = slug
    for sel in ("h1", "[data-type=document-title]", "h2"):
        title_el = main.select_one(sel)
        if title_el:
            cand = _norm_ws(title_el.get_text(" ", strip=True))
            if cand and cand.lower() != "none":
                title = cand
                break

    objectives: list[str] = []
    abstract = main.select_one("[data-type=abstract]")
    if abstract:
        for li in abstract.select("li"):
            objectives.append(_norm_ws(li.get_text(" ", strip=True)))

    headings = [
        _norm_ws(h.get_text(" ", strip=True))
        for h in main.select("h2, h3")
        if _norm_ws(h.get_text(" ", strip=True))
    ]

    items: list[ExtractedItem] = []
    seen_ids: set[str] = set()
    position = 0

    # Walk examples first (worked examples include an inner exercise)
    for example in main.select("[data-type=example]"):
        position += 1
        title_el = example.select_one(".os-title, [data-type=title]")
        ex_title = _norm_ws(title_el.get_text(" ", strip=True)) if title_el else f"Example@{position}"
        body = _problem_root_from_example(example)
        clone = BeautifulSoup(str(body), "html.parser")
        root = clone.body if clone.body else clone
        if isinstance(root, Tag):
            for sol in root.select("[data-type=solution], details, .os-solution-container"):
                sol.decompose()
        prompt_text, latex_bits = _replace_math_with_latex(root if isinstance(root, Tag) else clone)
        has_sol = bool(example.select_one("[data-type=solution], .os-solution-container"))
        eid = example.get("id") or f"example-{position}"
        items.append(
            ExtractedItem(
                item_id=str(eid),
                kind="example",
                title=ex_title,
                position=position,
                nearest_heading=_nearest_heading(example),
                prompt_text=prompt_text,
                prompt_latex_bits=latex_bits,
                has_solution=has_sol,
                source_anchor=str(eid) if example.get("id") else None,
            )
        )
        seen_ids.add(str(eid))
        # Mark inner exercises as consumed
        for inner in example.select("[data-type=exercise]"):
            if inner.get("id"):
                seen_ids.add(str(inner.get("id")))

    # Checkpoints
    for note in main.select("[data-type=note].checkpoint"):
        position += 1
        title_el = note.select_one(".os-title, [data-type=title]")
        cp_title = _norm_ws(title_el.get_text(" ", strip=True)) if title_el else f"Checkpoint@{position}"
        body = note.select_one("[data-type=exercise]") or note
        clone = BeautifulSoup(str(body), "html.parser")
        root = clone.body if clone.body else clone
        prompt_text, latex_bits = _replace_math_with_latex(root if isinstance(root, Tag) else clone)
        has_sol = bool(note.select_one("[data-type=solution], .os-solution-container"))
        eid = note.get("id") or (body.get("id") if isinstance(body, Tag) else None) or f"checkpoint-{position}"
        items.append(
            ExtractedItem(
                item_id=str(eid),
                kind="checkpoint",
                title=cp_title,
                position=position,
                nearest_heading=_nearest_heading(note),
                prompt_text=prompt_text,
                prompt_latex_bits=latex_bits,
                has_solution=has_sol,
                source_anchor=str(eid),
            )
        )
        seen_ids.add(str(eid))
        for inner in note.select("[data-type=exercise]"):
            if inner.get("id"):
                seen_ids.add(str(inner.get("id")))

    # Remaining section / other exercises
    for exercise in main.select("[data-type=exercise]"):
        eid = exercise.get("id")
        if eid and str(eid) in seen_ids:
            continue
        # Skip if nested under already-handled example/checkpoint (belt-and-suspenders)
        skip = False
        for a in exercise.parents:
            if not isinstance(a, Tag):
                continue
            if a.get("data-type") == "example":
                skip = True
                break
            if a.get("data-type") == "note" and "checkpoint" in (a.get("class") or []):
                skip = True
                break
        if skip:
            continue

        position += 1
        kind, item_title = _item_kind(exercise)
        if kind == "example":
            kind = "section_exercise"  # should not happen after skip
        clone = BeautifulSoup(str(exercise), "html.parser")
        root = clone.body if clone.body else clone
        prompt_text, latex_bits = _replace_math_with_latex(root if isinstance(root, Tag) else clone)
        has_sol = bool(exercise.select_one("[data-type=solution], .os-solution-container"))
        item_id = str(eid) if eid else f"exercise-{position}"
        items.append(
            ExtractedItem(
                item_id=item_id,
                kind=kind if kind != "other_exercise" else "other_exercise",
                title=item_title,
                position=position,
                nearest_heading=_nearest_heading(exercise),
                prompt_text=prompt_text,
                prompt_latex_bits=latex_bits,
                has_solution=has_sol,
                source_anchor=str(eid) if eid else None,
            )
        )

    # Re-number positions in document-ish order: examples/checkpoints interleaved by DOM order
    # Rebuild by walking DOM once for stable order.
    items = _reorder_by_dom(main, items)

    rel = html_path
    try:
        rel_s = str(html_path.resolve().relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        rel_s = str(html_path)

    return SectionInventory(
        book=book,
        slug=slug,
        title=title,
        source_url=f"https://openstax.org/books/{book}/pages/{slug}",
        local_path=rel_s,
        objectives=objectives,
        headings=headings,
        items=items,
        extracted_at=datetime.now(timezone.utc).isoformat(),
        stage="1_inventory",
    )


def _reorder_by_dom(main: Tag, items: list[ExtractedItem]) -> list[ExtractedItem]:
    """Order items by first appearance of their source_anchor / node in the DOM."""
    by_id = {it.item_id: it for it in items}
    ordered: list[ExtractedItem] = []
    used: set[str] = set()

    for node in main.select("[data-type=example], [data-type=note].checkpoint, [data-type=exercise]"):
        nid = node.get("id")
        # Match example/checkpoint containers
        if node.get("data-type") == "example" and nid and str(nid) in by_id and str(nid) not in used:
            ordered.append(by_id[str(nid)])
            used.add(str(nid))
            continue
        if node.get("data-type") == "note" and "checkpoint" in (node.get("class") or []):
            # Prefer note id, else inner exercise id matching our items
            candidates = [str(nid)] if nid else []
            for inner in node.select("[data-type=exercise]"):
                if inner.get("id"):
                    candidates.append(str(inner.get("id")))
            matched = next((c for c in candidates if c in by_id and c not in used), None)
            # Also match by title if ids differ
            if matched:
                ordered.append(by_id[matched])
                used.add(matched)
                continue
            for it in items:
                if it.kind == "checkpoint" and it.item_id not in used:
                    # fallback: first unused checkpoint in order of encounter
                    # only if this note's text overlaps
                    ordered.append(it)
                    used.add(it.item_id)
                    break
            continue
        if node.get("data-type") == "exercise" and nid and str(nid) in by_id and str(nid) not in used:
            ordered.append(by_id[str(nid)])
            used.add(str(nid))

    # Append any leftovers
    for it in items:
        if it.item_id not in used:
            ordered.append(it)

    for i, it in enumerate(ordered, start=1):
        it.position = i
    return ordered


def inventory_to_markdown(inv: SectionInventory) -> str:
    lines: list[str] = []
    lines.append(f"# Stage 1 inventory — `{inv.slug}`")
    lines.append("")
    lines.append(f"- **Book:** `{inv.book}`")
    lines.append(f"- **Title:** {inv.title}")
    lines.append(f"- **Source:** {inv.source_url}")
    lines.append(f"- **Local:** `{inv.local_path}`")
    lines.append(f"- **Extracted:** {inv.extracted_at}")
    lines.append(f"- **Items:** {len(inv.items)}")
    lines.append("")
    lines.append("## Learning objectives")
    lines.append("")
    if inv.objectives:
        for o in inv.objectives:
            lines.append(f"- {o}")
    else:
        lines.append("- _(none found)_")
    lines.append("")
    lines.append("## Counts by kind")
    lines.append("")
    counts: dict[str, int] = {}
    for it in inv.items:
        counts[it.kind] = counts.get(it.kind, 0) + 1
    for k, v in sorted(counts.items()):
        lines.append(f"- `{k}`: {v}")
    lines.append("")
    lines.append("## Items (document order)")
    lines.append("")
    for it in inv.items:
        label = it.title or it.item_id
        lines.append(f"### {it.position}. [{it.kind}] {label}")
        lines.append("")
        if it.nearest_heading:
            lines.append(f"- **Near heading:** {it.nearest_heading}")
        lines.append(f"- **Has solution:** {it.has_solution}")
        lines.append(f"- **Anchor:** `{it.source_anchor or '—'}`")
        lines.append(f"- **Prompt:** {it.prompt_text}")
        if it.prompt_latex_bits:
            lines.append("- **LaTeX bits:**")
            for bit in it.prompt_latex_bits[:12]:
                lines.append(f"  - `${bit}$`")
            if len(it.prompt_latex_bits) > 12:
                lines.append(f"  - _…+{len(it.prompt_latex_bits) - 12} more_")
        lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("_Stage 1 only: inventory. No family tags or EMH yet._")
    lines.append("")
    return "\n".join(lines)
