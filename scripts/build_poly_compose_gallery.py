"""Build HTML gallery for compositional poly simplify topics.

Covers:
  - simplify_polynomials (A1)
  - pa_polynomials_simplifying (deg 2, ≤3 terms)
  - a2_polynomial_functions_simplifying (higher deg, multi-hot)

Usage:
  $env:PYTHONPATH='.'
  python scripts/build_poly_compose_gallery.py
"""

from __future__ import annotations

import html
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from question_engine.frameworks.primitives.difficulty_knobs import reload_knobs
from question_engine.generators import GENERATORS

OUT = ROOT / "scripts" / "output" / "topic_fit" / "poly_compose"
DIFFICULTIES = (0, 3, 5, 8, 10, 15, 20, 25, 50)
N_PER = 4

TOPICS: list[tuple[str, str, dict]] = [
    (
        "simplify_polynomials",
        "Algebra 1 — Simplifying polynomials (general target)",
        {"max_degree": 4},
    ),
    (
        "pa_polynomials_simplifying",
        "Pre-Algebra — Simplifying (deg 2, ≤3 terms, single-hot)",
        {
            "max_degree": 2,
            "min_degree": 2,
            "max_terms": 3,
            "prefer_single_hot": True,
        },
    ),
    (
        "a2_polynomial_functions_simplifying",
        "Algebra 2 — Simplifying (max deg 5, multi-hot)",
        {"max_degree": 5, "prefer_single_hot": False},
    ),
]


def _sample(topic: str, constraints: dict, d: int, seed: int) -> list[dict]:
    gen = GENERATORS["simplify_polynomials"]
    qs = gen(
        topic,
        {
            "difficulty": d,
            "count": N_PER,
            "seed": seed,
            "integers_only": True,
            "only_x": True,
            "include_answer_key": True,
            **constraints,
        },
    )
    rows = []
    for q in qs:
        meta = q.metadata or {}
        rows.append(
            {
                "prompt": q.prompt_latex or "",
                "answer": q.answer_latex or "",
                "deg": meta.get("poly_degree"),
                "hot": meta.get("n_hot_terms"),
                "terms": meta.get("n_terms"),
                "depths": meta.get("compose_depth_counts")
                or (meta.get("constructive") or {}).get("compose_depth_counts"),
            }
        )
    return rows


def _html_page(sections: list[tuple[str, str, dict[int, list[dict]]]]) -> str:
    parts: list[str] = [
        "<!DOCTYPE html>",
        '<html lang="en"><head><meta charset="utf-8"/>',
        "<title>Poly compose simplify gallery</title>",
        '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css"/>',
        "<script defer src=\"https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js\"></script>",
        "<script defer src=\"https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js\"",
        '  onload="renderMathInElement(document.body,{delimiters:['
        "{left:'$$',right:'$$',display:true},"
        "{left:'$',right:'$',display:false}"
        "]})"
        '"></script>',
        "<style>",
        "body{font-family:Georgia,serif;max-width:960px;margin:2rem auto;padding:0 1.25rem;",
        "background:#f7f4ef;color:#1a1a1a;line-height:1.45}",
        "h1{font-size:1.75rem;margin-bottom:0.25rem}",
        "h2{font-size:1.25rem;margin-top:2.5rem;border-bottom:1px solid #ccc;padding-bottom:0.35rem}",
        "h3{font-size:1.05rem;margin-top:1.5rem;color:#444}",
        ".meta{color:#666;font-size:0.9rem;margin-bottom:1.5rem}",
        ".card{background:#fff;border:1px solid #ddd;border-radius:6px;padding:0.85rem 1rem;",
        "margin:0.6rem 0}",
        ".label{font-size:0.75rem;color:#666;margin-bottom:0.35rem}",
        ".prompt{font-size:1.05rem;margin:0.4rem 0}",
        ".answer{color:#1a5c2e;margin-top:0.35rem}",
        ".tags{font-size:0.75rem;color:#777;margin-top:0.4rem}",
        "nav a{margin-right:1rem;color:#234}",
        "</style></head><body>",
        "<h1>Compositional polynomial simplify</h1>",
        f'<p class="meta">Generated {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")} · '
        "answer-first construct_poly (subset inflate, hierarchical budget)</p>",
        "<nav>",
    ]
    for tid, title, _ in sections:
        parts.append(f'<a href="#{html.escape(tid)}">{html.escape(tid)}</a>')
    parts.append("</nav>")

    for tid, title, by_d in sections:
        parts.append(f'<h2 id="{html.escape(tid)}">{html.escape(title)}</h2>')
        parts.append(f'<p class="meta"><code>{html.escape(tid)}</code></p>')
        for d in DIFFICULTIES:
            rows = by_d.get(d, [])
            parts.append(f"<h3>D = {d}</h3>")
            for i, row in enumerate(rows):
                depths = row.get("depths") or {}
                parts.append('<div class="card">')
                parts.append(
                    f'<div class="label">#{i + 1} · deg={row.get("deg")} · '
                    f'hot={row.get("hot")} · terms={row.get("terms")} · '
                    f"depths={html.escape(str(depths))}</div>"
                )
                parts.append(
                    f'<div class="prompt">$${html.escape(row["prompt"])}$$</div>'
                )
                parts.append(
                    f'<div class="answer">→ $${html.escape(row["answer"])}$$</div>'
                )
                parts.append("</div>")

    parts.append("</body></html>")
    return "\n".join(parts)


def main() -> None:
    reload_knobs()
    OUT.mkdir(parents=True, exist_ok=True)
    sections: list[tuple[str, str, dict[int, list[dict]]]] = []
    for tid, title, constraints in TOPICS:
        by_d: dict[int, list[dict]] = {}
        for d in DIFFICULTIES:
            by_d[d] = _sample(tid, constraints, d, seed=hash(tid) % 100000 + d * 17)
        sections.append((tid, title, by_d))

    html_path = OUT / "gallery.html"
    html_path.write_text(_html_page(sections), encoding="utf-8")
    print(f"Wrote {html_path}")


if __name__ == "__main__":
    main()
