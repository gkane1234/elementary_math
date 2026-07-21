"""Focused continuous-D gallery for g6_dividing_whole_numbers_by_decimals."""

from __future__ import annotations

import html
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import question_engine.types  # noqa: F401
from question_engine.api.handler import _resolve_generation_settings
from question_engine.generators import GENERATORS

OUT = ROOT / "scripts" / "output" / "topic_fit" / "g6_pa_continuous"
TID = "g6_dividing_whole_numbers_by_decimals"
DIFFS = (0, 10, 20, 40)
N = 6


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    gen = GENERATORS["g6_whole_by_decimal_divide"]
    parts = [
        "<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'/>",
        "<title>Whole ÷ decimal continuous D</title>",
        '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css"/>',
        "<script defer src='https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js'></script>",
        "<script defer src='https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js'",
        " onload=\"renderMathInElement(document.body,{delimiters:[{left:'$$',right:'$$',display:true},{left:'$',right:'$',display:false}]})\"></script>",
        "<style>body{font-family:Georgia,serif;max-width:820px;margin:2rem auto;padding:0 1rem}",
        "h1{font-size:1.4rem}h2{margin-top:1.6rem}.card{border:1px solid #ddd;padding:.6rem .9rem;margin:.4rem 0}",
        ".ans{color:#1a5c2e}.meta{font-size:.85rem;color:#666}</style></head><body>",
        "<h1>Dividing whole numbers by decimals</h1>",
        f"<p class='meta'>{html.escape(TID)} · "
        f"{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}</p>",
    ]
    for d in DIFFS:
        parts.append(f"<h2>D = {d}</h2>")
        settings = _resolve_generation_settings(
            TID,
            {
                "difficulty": d,
                "count": N,
                "seed": 200 + d,
                "include_answer_key": True,
            },
        )
        parts.append(
            "<p class='meta'>"
            f"allow_negative={settings.get('allow_negative')} · "
            f"divisor_ge_one={settings.get('divisor_ge_one')} · "
            f"decimal_places={settings.get('decimal_places')}"
            "</p>"
        )
        for i, q in enumerate(gen(TID, settings)):
            parts.append("<div class='card'>")
            parts.append(f"<div class='meta'>#{i + 1}</div>")
            parts.append(f"<div>$${html.escape(q.prompt_latex or '')}$$</div>")
            parts.append(f"<div class='ans'>→ $${html.escape(q.answer_latex or '')}$$</div>")
            parts.append("</div>")
    parts.append("</body></html>")
    path = OUT / "whole_by_decimal_gallery.html"
    path.write_text("\n".join(parts), encoding="utf-8")
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
