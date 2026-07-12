"""Generate worksheet-style examples PDF with Easy/Medium/Hard for every Ready type.

Default output:
  scripts/output/all_types_examples.pdf
  scripts/output/all_types_examples.html

Filter to one course with --course grade_6 (etc.), or use
scripts/generate_grade6_examples_pdf.py for Grade 6 only.

Renders prompt graphs (blank planes / stimulus lines / number lines) and geometry
diagrams the same way the React worksheet does, then prints HTML → PDF via
Playwright / Edge headless (KaTeX + CSS).
"""

from __future__ import annotations

import argparse
import html
import subprocess
import sys
import time
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import question_engine.types  # noqa: F401 — register types
from question_engine.catalogs.algebra_1 import CATALOG as A1
from question_engine.catalogs.algebra_2 import CATALOG as A2
from question_engine.catalogs.calculus import CATALOG as CALC
from question_engine.catalogs.geometry import CATALOG as GEO
from question_engine.catalogs.grade_6 import CATALOG as G6
from question_engine.catalogs.pre_algebra import CATALOG as PA
from question_engine.catalogs.precalculus import CATALOG as PC
from question_engine.core.base import QUESTION_TYPES
from question_engine.settings.presets import apply_difficulty_presets
from question_engine.type_readiness import type_not_ready
from question_engine.utils.instruction_latex import repair_instruction_latex
from render_graph_svg import has_visuals, render_answer_visuals, render_prompt_visuals

OUT_DIR = ROOT / "scripts" / "output"
PDF_PATH = OUT_DIR / "all_types_examples.pdf"
HTML_PATH = OUT_DIR / "all_types_examples.html"
TIERS = ("easy", "medium", "hard")
TIER_LABEL = {"easy": "Easy", "medium": "Medium", "hard": "Hard"}

COURSE_CATALOGS = {
    "all": None,  # combined below
    "grade_6": G6,
    "g6": G6,
    "pre_algebra": PA,
    "pa": PA,
    "algebra_1": A1,
    "a1": A1,
    "algebra_2": A2,
    "a2": A2,
    "geometry": GEO,
    "geo": GEO,
    "precalculus": PC,
    "pc": PC,
    "calculus": CALC,
    "calc": CALC,
}

COURSE_TITLES = {
    "grade_6": "Grade 6",
    "g6": "Grade 6",
    "pre_algebra": "Pre-Algebra",
    "pa": "Pre-Algebra",
    "algebra_1": "Algebra 1",
    "a1": "Algebra 1",
    "algebra_2": "Algebra 2",
    "a2": "Algebra 2",
    "geometry": "Geometry",
    "geo": "Geometry",
    "precalculus": "Precalculus",
    "pc": "Precalculus",
    "calculus": "Calculus",
    "calc": "Calculus",
    "all": "All Courses",
}

WORKSHEET_CSS = """
:root { color-scheme: light; }
* { box-sizing: border-box; }
body {
  margin: 0;
  padding: 0.75in 0.7in;
  font-family: "Times New Roman", Times, Georgia, serif;
  font-size: 12pt;
  line-height: 1.35;
  color: #111827;
  background: #fff;
}
.doc-title { text-align: center; font-size: 1.35rem; margin: 0 0 0.35rem; }
.doc-subtitle { text-align: center; color: #4b5563; margin: 0 0 1.25rem; font-size: 0.95rem; }
.type-section {
  margin: 0 0 1.75rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e5e7eb;
}
.type-section:last-of-type { border-bottom: none; }
.worksheet-header h2 {
  margin: 0 0 0.35rem;
  text-align: center;
  font-size: 1.15rem;
}
.worksheet-meta { margin: 0 0 0.65rem; font-size: 0.95rem; }
.worksheet-instruction {
  margin: 0 0 0.85rem;
  font-size: 1.05rem;
}
.type-id {
  text-align: center;
  color: #6b7280;
  font-size: 0.78rem;
  margin: 0 0 0.5rem;
  font-family: ui-monospace, Consolas, monospace;
}
.difficulty-block { margin: 0.85rem 0 1rem; }
.difficulty-label {
  display: inline-block;
  font-weight: 700;
  font-size: 0.85rem;
  letter-spacing: 0.02em;
  text-transform: uppercase;
  color: #1f2937;
  background: #f3f4f6;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  padding: 0.12rem 0.45rem;
  margin: 0 0 0.45rem;
}
.question-list {
  margin: 0;
  padding-left: 1.5rem;
  min-width: 0;
  max-width: 100%;
}
.question-list li {
  margin-bottom: 1.15rem;
  min-width: 0;
  max-width: 100%;
  overflow-wrap: break-word;
  word-break: break-word;
}
.question-prompt { display: inline; min-width: 0; max-width: 100%; }
.question-list li .katex,
.worksheet-instruction .katex,
.mc-choice .katex {
  white-space: normal;
  max-width: 100%;
}
.question-list li .katex .base,
.worksheet-instruction .katex .base,
.mc-choice .katex .base {
  display: inline;
  white-space: normal;
  width: auto;
  max-width: 100%;
}
.question-list li .katex-html,
.worksheet-instruction .katex-html,
.mc-choice .katex-html {
  white-space: normal;
  max-width: 100%;
}
.question-list li .katex .text,
.question-list li .katex .text > .mord,
.worksheet-instruction .katex .text,
.worksheet-instruction .katex .text > .mord,
.mc-choice .katex .text,
.mc-choice .katex .text > .mord {
  white-space: normal;
  overflow-wrap: break-word;
  word-wrap: break-word;
  hyphens: none;
}
.question-graph {
  display: block;
  clear: both;
  width: 100%;
  max-width: min(280px, 100%);
  height: auto;
  margin-top: 0.45rem;
}
.question-diagram {
  margin-top: 0.45rem;
  max-width: min(320px, 100%);
}
.question-diagram svg {
  max-width: 100%;
  height: auto;
  display: block;
}
.question-graph .graph-axis { stroke: #374151; stroke-width: 1.5; }
.question-graph .graph-grid { stroke: #e5e7eb; stroke-width: 1; }
.question-graph .graph-tick { stroke: #6b7280; stroke-width: 1; }
.question-graph .graph-label { fill: #4b5563; font-size: 11px; font-family: system-ui, sans-serif; }
.question-graph .graph-shade { fill: #93c5fd; opacity: 0.55; }
.question-graph .graph-boundary-filled { fill: #111827; stroke: #111827; }
.question-graph .graph-boundary-open { fill: #ffffff; stroke: #111827; stroke-width: 1.5; }
.question-graph .graph-line { stroke: #2563eb; stroke-width: 2; }
.question-graph .graph-point { fill: #111827; }
.mc-choices {
  list-style: none;
  margin: 0.4rem 0 0;
  padding: 0;
  display: grid;
  gap: 0.2rem;
}
.mc-choice {
  display: grid;
  grid-template-columns: 1.25rem 1fr;
  gap: 0.35rem;
  align-items: start;
}
.mc-choice-letter { font-weight: 600; }
.answer-key {
  margin-top: 0.85rem;
  padding-top: 0.65rem;
  border-top: 2px dashed #d1d5db;
}
.answer-key h3 {
  margin: 0 0 0.5rem;
  font-size: 1rem;
}
.answer-list { margin: 0; padding-left: 1.5rem; }
.answer-list li { margin-bottom: 0.55rem; }
.err { color: #b91c1c; font-size: 0.9rem; }
.question-columns {
  display: grid;
  gap: 1.25rem 1.5rem;
  align-items: start;
  width: 100%;
}
.question-columns > * {
  min-width: 0;
  max-width: 100%;
}
.question-columns[data-columns="2"] { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.question-columns[data-columns="1"] { grid-template-columns: minmax(0, 1fr); }
.question-columns[data-columns="2"] .question-graph { max-width: min(240px, 100%); }
@media print {
  body { padding: 0.55in 0.55in; }
  .difficulty-block { break-inside: avoid; page-break-inside: avoid; }
  .answer-key { break-inside: avoid; page-break-inside: avoid; }
  .worksheet-header { break-after: avoid; }
}
"""


def ready_entries(*, course: str = "all"):
    key = (course or "all").strip().lower().replace("-", "_")
    if key not in COURSE_CATALOGS:
        raise ValueError(
            f"Unknown course {course!r}. "
            f"Choose from: {', '.join(sorted(COURSE_CATALOGS))}"
        )
    catalog = COURSE_CATALOGS[key]
    if catalog is None:
        catalog = A1 + G6 + PA + A2 + GEO + PC + CALC
    return [
        e
        for e in sorted(catalog, key=lambda x: (x.category, x.name, x.id))
        if e.generator != "scaffold" and not type_not_ready(e.id)
    ]


def _mc_choices(metadata: dict | None) -> list[dict] | None:
    if not metadata:
        return None
    raw = metadata.get("choices")
    if not isinstance(raw, list) or not raw:
        return None
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    choices = []
    for i, entry in enumerate(raw):
        if isinstance(entry, str):
            choices.append({"letter": letters[i], "latex": entry, "correct": False})
        elif isinstance(entry, dict) and isinstance(entry.get("latex"), str):
            cid = str(entry.get("id") or letters[i]).strip().upper()
            letter = cid if len(cid) == 1 and cid.isalpha() else letters[i]
            choices.append(
                {
                    "letter": letter,
                    "latex": entry["latex"],
                    "correct": bool(entry.get("correct")),
                }
            )
    if not choices:
        return None
    if not any(c["correct"] for c in choices) and isinstance(metadata.get("correct_index"), int):
        idx = metadata["correct_index"]
        if 0 <= idx < len(choices):
            choices[idx]["correct"] = True
    return choices


def generate_samples(entry):
    samples = []
    errors = []
    qt = QUESTION_TYPES.get(entry.id)
    if qt is None:
        return samples, [f"type not registered: {entry.id}"]
    instruction = repair_instruction_latex(getattr(qt, "instruction_latex", None)) or ""
    for tier in TIERS:
        settings = apply_difficulty_presets(
            {
                "count": 1,
                "difficulty_tier": tier,
                "include_answer_key": True,
                "include_diagram": True,
                "include_graph_metadata": True,
            },
            type_id=entry.id,
            setting_profile=getattr(qt, "setting_profile", None),
        )
        try:
            questions = qt.generate(settings)
            if not questions:
                errors.append(f"{tier}: empty")
                continue
            q = questions[0]
            # Match API annotation so worksheet headers work.
            meta = dict(q.metadata or {})
            meta["instruction_latex"] = instruction
            q.metadata = meta
            samples.append((tier, q, instruction))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{tier}: {exc}")
            traceback.print_exc()
    return samples, errors


def _latex_span(content: str, *, css_class: str = "") -> str:
    cls = f' class="{css_class}"' if css_class else ""
    return f'<span{cls} data-latex="{html.escape(content, quote=True)}"></span>'


def _render_question_body(q, *, number: int) -> str:
    meta = q.metadata or {}
    parts = [f"<li value=\"{number}\">"]
    parts.append(_latex_span(q.prompt_latex or "", css_class="question-prompt"))
    parts.append(render_prompt_visuals(meta))
    choices = _mc_choices(meta)
    if choices:
        parts.append('<ul class="mc-choices">')
        for choice in choices:
            parts.append(
                '<li class="mc-choice">'
                f'<span class="mc-choice-letter">{html.escape(choice["letter"])}.</span>'
                f'{_latex_span(choice["latex"])}'
                "</li>"
            )
        parts.append("</ul>")
    parts.append("</li>")
    return "".join(parts)


def _render_answer_item(q, *, number: int, tier: str) -> str:
    meta = q.metadata or {}
    choices = _mc_choices(meta)
    letter = None
    if choices:
        for choice in choices:
            if choice["correct"]:
                letter = choice["letter"]
                break
    parts = [f'<li value="{number}"><strong>{TIER_LABEL[tier]}:</strong> ']
    if letter:
        parts.append(html.escape(letter))
        if q.answer_latex:
            parts.append(" · ")
    if q.answer_latex:
        parts.append(_latex_span(q.answer_latex))
    elif not letter:
        parts.append("<em>(no answer)</em>")
    parts.append(render_answer_visuals(meta))
    parts.append("</li>")
    return "".join(parts)


def build_html(
    entries_with_samples,
    *,
    html_path: Path | None = None,
    title: str | None = None,
    subtitle: str | None = None,
) -> None:
    katex_css = (ROOT / "node_modules" / "katex" / "dist" / "katex.min.css").resolve()
    katex_js = (ROOT / "node_modules" / "katex" / "dist" / "katex.min.js").resolve()
    if katex_css.exists() and katex_js.exists():
        katex_css_href = katex_css.as_uri()
        katex_js_src = katex_js.as_uri()
    else:
        katex_css_href = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css"
        katex_js_src = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"

    doc_title = title or "Polynomial — Ready Type Examples"
    doc_subtitle = subtitle or (
        "One Easy, Medium, and Hard sample per Ready type, "
        "formatted like printable worksheets (shared instructions, graphs, and diagrams)."
    )
    out_html = html_path or HTML_PATH

    parts = [
        "<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'/>",
        f"<title>{html.escape(doc_title)} (E/M/H)</title>",
        f"<link rel='stylesheet' href='{katex_css_href}'/>",
        f"<style>{WORKSHEET_CSS}</style>",
        "</head><body>",
        f"<h1 class='doc-title'>{html.escape(doc_title)}</h1>",
        f"<p class='doc-subtitle'>{html.escape(doc_subtitle)}</p>",
    ]

    for entry, samples, errors in entries_with_samples:
        instruction = ""
        if samples:
            instruction = samples[0][2] or ""
        qt = QUESTION_TYPES.get(entry.id)
        if not instruction and qt is not None:
            instruction = repair_instruction_latex(getattr(qt, "instruction_latex", None)) or ""

        section_has_visual = any(has_visuals(q.metadata) for _, q, _ in samples)
        columns = 1 if section_has_visual else 2

        parts.append("<section class='type-section'>")
        parts.append("<header class='worksheet-header'>")
        parts.append(f"<h2>{html.escape(entry.name)}</h2>")
        parts.append(
            f"<p class='type-id'><code>{html.escape(entry.id)}</code> · "
            f"{html.escape(entry.category)} · gen=<code>{html.escape(entry.generator)}</code></p>"
        )
        parts.append(
            '<p class="worksheet-meta">Name: ________________________________ '
            "Date: ____________</p>"
        )
        if instruction:
            parts.append(
                f'<p class="worksheet-instruction">{_latex_span(instruction)}</p>'
            )
        parts.append("</header>")

        if errors and len(samples) < 3:
            parts.append(f"<p class='err'>Issues: {html.escape('; '.join(errors))}</p>")

        # Difficulty subsections, worksheet-numbered within the type.
        q_blocks = []
        for idx, (tier, q, _) in enumerate(samples, start=1):
            block = [
                "<div class='difficulty-block'>",
                f"<div class='difficulty-label'>{TIER_LABEL[tier]}</div>",
                f'<ol class="question-list" start="{idx}">',
                _render_question_body(q, number=idx),
                "</ol></div>",
            ]
            q_blocks.append("".join(block))

        if columns == 2 and len(q_blocks) >= 2:
            # Put Easy+Medium in a 2-col grid, Hard full width if present.
            parts.append('<div class="question-columns" data-columns="2">')
            parts.append(q_blocks[0])
            parts.append(q_blocks[1] if len(q_blocks) > 1 else "")
            parts.append("</div>")
            for extra in q_blocks[2:]:
                parts.append(extra)
        else:
            for block in q_blocks:
                parts.append(block)

        if samples:
            parts.append('<div class="answer-key"><h3>Answer Key</h3>')
            parts.append('<ol class="answer-list">')
            for idx, (tier, q, _) in enumerate(samples, start=1):
                parts.append(_render_answer_item(q, number=idx, tier=tier))
            parts.append("</ol></div>")

        parts.append("</section>")

    parts.append(f"<script src='{katex_js_src}'></script>")
    parts.append(
        """
<script>
(function () {
  function enableKatexSoftWrap(root) {
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    var nodes = [];
    var node;
    while ((node = walker.nextNode())) {
      if (node.nodeValue && node.nodeValue.indexOf('\\u00a0') !== -1) {
        nodes.push(node);
      }
    }
    for (var i = 0; i < nodes.length; i++) {
      nodes[i].nodeValue = nodes[i].nodeValue.replace(/\\u00a0/g, ' ');
    }
  }
  function renderAll() {
    if (typeof katex === 'undefined') return false;
    document.querySelectorAll('[data-latex]').forEach(function (el) {
      var latex = el.getAttribute('data-latex') || '';
      try {
        katex.render(latex, el, { throwOnError: false, displayMode: false });
        enableKatexSoftWrap(el);
      } catch (err) {
        el.textContent = latex;
      }
    });
    document.documentElement.setAttribute('data-math-ready', '1');
    return true;
  }
  function boot() {
    if (renderAll()) return;
    var tries = 0;
    var timer = setInterval(function () {
      tries += 1;
      if (renderAll() || tries > 80) clearInterval(timer);
    }, 50);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
</script>
"""
    )
    parts.append("</body></html>")
    out_html.parent.mkdir(parents=True, exist_ok=True)
    out_html.write_text("\n".join(parts), encoding="utf-8")


def _edge_exe() -> Path | None:
    candidates = [
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    ]
    for path in candidates:
        if path.exists():
            return path
    return None


def html_to_pdf(*, html_path: Path | None = None, pdf_path: Path | None = None) -> None:
    """Print the companion HTML to PDF (Playwright preferred; Edge fallback)."""
    src_html = html_path or HTML_PATH
    dest_pdf = pdf_path or PDF_PATH
    playwright_script = Path(__file__).resolve().parent / "print_examples_pdf.cjs"
    if playwright_script.exists():
        print("Printing PDF via Playwright...")
        result = subprocess.run(
            [
                "node",
                str(playwright_script),
                str(src_html.resolve()),
                str(dest_pdf.resolve()),
            ],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=600,
        )
        if result.stdout:
            print(result.stdout.encode("ascii", "replace").decode("ascii"))
        if result.returncode == 0 and dest_pdf.exists() and dest_pdf.stat().st_size >= 1000:
            return
        if result.stderr:
            print(result.stderr.encode("ascii", "replace").decode("ascii"))
        print("Playwright print unavailable or failed; falling back to Edge/Chrome...")

    browser = _edge_exe()
    if browser is None:
        raise RuntimeError("No Playwright browsers and no Edge/Chrome found for HTML→PDF print")

    html_uri = src_html.resolve().as_uri()
    cmd = [
        str(browser),
        "--headless=new",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=120000",
        f"--print-to-pdf={dest_pdf.resolve()}",
        html_uri,
    ]
    print("Printing PDF via", browser.name, "...")
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=600,
    )
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)
        raise RuntimeError(f"PDF print failed with code {result.returncode}")
    if not dest_pdf.exists() or dest_pdf.stat().st_size < 1000:
        raise RuntimeError("PDF was not created or is empty")


def _pdf_page_estimate(size_bytes: int) -> str:
    # Rough heuristic for letter PDFs with mixed text/graphics.
    approx = max(1, size_bytes // 18_000)
    return f"~{approx} pages (estimate from size)"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate E/M/H worksheet examples PDF for Ready question types."
    )
    parser.add_argument(
        "--course",
        default="all",
        help="Catalog filter: all, grade_6 (g6), pre_algebra (pa), algebra_1 (a1), "
        "algebra_2 (a2), geometry (geo), precalculus (pc), calculus (calc).",
    )
    parser.add_argument(
        "--output-stem",
        default=None,
        help="Basename under scripts/output (default: all_types_examples, or "
        "grade6_all_types_examples when --course is grade_6).",
    )
    return parser.parse_args(argv)


def _resolve_paths(course: str, output_stem: str | None) -> tuple[Path, Path, str]:
    key = (course or "all").strip().lower().replace("-", "_")
    if output_stem:
        stem = output_stem
    elif key in ("grade_6", "g6"):
        stem = "grade6_all_types_examples"
    elif key == "all":
        stem = "all_types_examples"
    else:
        stem = f"{key}_all_types_examples"
    html_path = OUT_DIR / f"{stem}.html"
    pdf_path = OUT_DIR / f"{stem}.pdf"
    course_label = COURSE_TITLES.get(key, key)
    return html_path, pdf_path, course_label


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    html_path, pdf_path, course_label = _resolve_paths(args.course, args.output_stem)
    entries = ready_entries(course=args.course)
    print(f"Course: {course_label} ({args.course})")
    print(f"Ready types: {len(entries)}")
    print(f"Output: {pdf_path.name}")
    rows = []
    complete = 0
    visual_count = 0
    for i, entry in enumerate(entries, 1):
        samples, errors = generate_samples(entry)
        if len(samples) == 3:
            complete += 1
        if any(has_visuals(q.metadata) for _, q, _ in samples):
            visual_count += 1
        rows.append((entry, samples, errors))
        if i % 25 == 0 or i == len(entries):
            print(
                f"  generated {i}/{len(entries)} "
                f"(complete E/M/H: {complete}, with visuals: {visual_count})"
            )

    title = f"Polynomial — {course_label} Ready Type Examples"
    subtitle = (
        f"One Easy, Medium, and Hard sample per Ready {course_label} type, "
        "formatted like printable worksheets (shared instructions, graphs, and diagrams)."
    )
    print("Building HTML...")
    t0 = time.time()
    build_html(rows, html_path=html_path, title=title, subtitle=subtitle)
    print(f"  HTML written in {time.time() - t0:.1f}s -> {html_path}")

    print("Building PDF...")
    t1 = time.time()
    html_to_pdf(html_path=html_path, pdf_path=pdf_path)
    size = pdf_path.stat().st_size
    print(f"  PDF written in {time.time() - t1:.1f}s")
    print(f"PDF: {pdf_path} ({size:,} bytes; {_pdf_page_estimate(size)})")
    print(f"HTML: {html_path} ({html_path.stat().st_size:,} bytes)")
    print(f"Types included: {len(entries)}")
    print(f"Types with full E/M/H: {complete}/{len(entries)}")
    print(f"Types with graphs/diagrams: {visual_count}/{len(entries)}")
    incomplete = [(e.id, errs) for e, s, errs in rows if len(s) < 3]
    if incomplete:
        print(f"Incomplete ({len(incomplete)}):")
        for tid, errs in incomplete[:30]:
            print(f"  {tid}: {errs}")


if __name__ == "__main__":
    main()
