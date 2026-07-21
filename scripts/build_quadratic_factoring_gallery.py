"""HTML gallery for factors-first quadratic / special / cubes / quadratic-form / mixer."""

from __future__ import annotations

import html
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from question_engine.frameworks.primitives.difficulty_knobs import reload_knobs
from question_engine.generators import GENERATORS

OUT = ROOT / "scripts" / "output" / "topic_fit" / "quadratic_factoring"
DIFFS = (0, 3, 6, 8, 10, 12, 15, 20, 25)
N = 4

TOPICS = (
    ("quadratic_factoring", "Factor quadratic expressions", 2),
    ("polynomial_factoring_special_cases", "Special products (DOS/PST)", 2),
    ("quadratic_factoring_equations", "Solve by factoring", 2),
    (
        "a2_polynomial_functions_factoring_sum_difference_of_cubes",
        "Sum/difference of cubes",
        3,
    ),
    (
        "a2_polynomial_functions_factoring_quadratic_form",
        "Quadratic form",
        4,
    ),
    (
        "a2_polynomial_functions_factoring_all_techniques",
        "All techniques (A2 mixer)",
        3,
    ),
    (
        "polynomial_factoring_general_strategy",
        "General strategy (A1 mixer)",
        3,
    ),
)


def main() -> None:
    reload_knobs()
    OUT.mkdir(parents=True, exist_ok=True)
    parts = [
        "<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'/>",
        "<title>Quadratic factoring</title>",
        '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css"/>',
        "<script defer src='https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js'></script>",
        "<script defer src='https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js'",
        " onload=\"renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}]})\"></script>",
        "<style>body{font-family:Georgia,serif;max-width:980px;margin:2rem auto;padding:0 1rem;background:#f7f4ef}",
        "h1{font-size:1.6rem}h2{margin-top:2rem;border-bottom:1px solid #ccc}",
        "h3{color:#444}.card{background:#fff;border:1px solid #ddd;border-radius:6px;padding:.75rem 1rem;margin:.5rem 0}",
        ".ans{color:#1a5c2e}.meta{font-size:.8rem;color:#666}</style></head><body>",
        "<h1>Factors-first quadratic factoring (+ cubes, quadratic form, mixers)</h1>",
        f"<p class='meta'>Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} · "
        "Low D: bedraggled-simple · D&gt;10 unsimplified stems where applicable</p>",
    ]
    for tid, title, max_degree in TOPICS:
        parts.append(f"<h2 id='{html.escape(tid)}'>{html.escape(title)}</h2>")
        parts.append(f"<p class='meta'><code>{html.escape(tid)}</code></p>")
        gen = GENERATORS[tid]
        for d in DIFFS:
            parts.append(f"<h3>D = {d}</h3>")
            qs = gen(
                tid,
                {
                    "difficulty": d,
                    "count": N,
                    "seed": 50 + d * 11 + hash(tid) % 1000,
                    "integers_only": True,
                    "only_x": True,
                    "include_answer_key": True,
                    "max_degree": max_degree,
                },
            )
            for i, q in enumerate(qs):
                meta = q.metadata or {}
                parts.append("<div class='card'>")
                parts.append(
                    f"<div class='meta'>#{i+1} · method={html.escape(str(meta.get('method')))} · "
                    f"upgrades={html.escape(str(meta.get('upgrades')))}</div>"
                )
                parts.append(f"<div>$${html.escape(q.prompt_latex or '')}$$</div>")
                parts.append(
                    f"<div class='ans'>→ $${html.escape(q.answer_latex or '')}$$</div>"
                )
                parts.append("</div>")
    parts.append("</body></html>")
    path = OUT / "gallery.html"
    path.write_text("\n".join(parts), encoding="utf-8")
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
