"""Build an inspectable gallery for calculus pilot generators.

Writes under scripts/output/topic_fit/calculus_pilot/:
  gallery.md   — markdown review pack
  gallery.html — KaTeX-rendered HTML
  PILOT_NOTES.md — textbook patterns → variant expansion + proposed next batch

Usage:
  $env:PYTHONPATH='.'
  python scripts/build_calculus_pilot_gallery.py
"""

from __future__ import annotations

import html
import json
import random
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import question_engine.types  # noqa: F401
from question_engine.core.base import QUESTION_TYPES
from question_engine.settings.presets import apply_difficulty_presets

OUT = ROOT / "scripts" / "output" / "topic_fit" / "calculus_pilot"
TIERS = ("easy", "medium", "hard")
N_PER_TIER = 4

PILOT_TYPE_IDS = (
    "calc_app_diff_slope_tangent_and_normal_lines",
    "calc_app_diff_differentials",
    "calc_indef_int_logarithmic_rule_and_exponentials_with_substitution",
)

TEXTBOOK_ANCHORS = {
    "calc_app_diff_slope_tangent_and_normal_lines": {
        "sections": ["3.1 Defining the Derivative"],
        "seed_examples": [
            "Ex 3.1 / 3.2: tangent to f(x)=x² at x=3",
            "Ex 3.3: tangent to f(x)=1/x at x=2",
            "Ex 3.5: derivative of 3x²−4x+1 (feeds tangent slope)",
        ],
        "variety_added": [
            "Polynomial term order: standard vs reversed vs factored x(x+b)",
            "Function families: mono/quad/cubic poly, reciprocal (1/x and x^{-1}), radical, trig, exp/exp(), ln, rational linear",
            "Ask tangent or normal (hard mixes both)",
        ],
    },
    "calc_app_diff_differentials": {
        "sections": ["4.2 Linear Approximations and Differentials"],
        "seed_examples": [
            "Ex 4.8: dy for y=x²+2x and y=cos x; evaluate at x=3, dx=0.1",
            "Ex 4.9: compare Δy vs dy for y=x²+2x",
        ],
        "variety_added": [
            "Same OpenStax poly with reversed / factored display",
            "Families: power, poly, sin/cos/tan, e^{kx}/exp(kx), √x / x^{1/2}, 1/x, product, quotient, e^{x²}, ln",
            "Hard includes evaluate-dy-at-(x,dx) items",
        ],
    },
    "calc_indef_int_logarithmic_rule_and_exponentials_with_substitution": {
        "sections": [
            "5.5 Substitution",
            "5.6 Integrals Involving Exponential and Logarithmic Functions",
        ],
        "seed_examples": [
            "Ex 5.37: ∫ e^{−x} dx",
            "Ex 5.38: ∫ e^x/(1+e^x) dx",
            "Ex 5.39: ∫ 3x² e^{2x³} dx",
            "Ex 5.30–5.31: u-sub power / rewrite forms",
        ],
        "variety_added": [
            "Integrand order: frac vs ( )^{-1}·factor vs factor·( )^{-1}",
            "Denominator order: x²+c vs c+x²; exponent ax+b vs b+ax",
            "Families: e^{kx}, e^{ax+b}, 1/(ax+b), du/u log forms, e^{xⁿ} chains, e^{2x}/(e^{2x}+c)",
        ],
    },
}

NEXT_BATCH = [
    "calc_diff_instantaneous_rates_of_change",
    "calc_diff_inverse_functions",
    "calc_app_diff_intervals_of_concavity",
    "calc_app_diff_relative_extrema",
    "calc_app_diff_absolute_extrema",
    "calc_app_diff_optimization",
    "calc_app_diff_newtons_method",
    "calc_indef_int_trigonometric_with_substitution",
    "calc_indef_int_inverse_trigonometric_with_substitution",
]


def _sample(type_id: str) -> list[dict]:
    qt = QUESTION_TYPES[type_id]
    profile = getattr(qt, "setting_profile", None)
    rows: list[dict] = []
    for tier in TIERS:
        for i in range(N_PER_TIER):
            settings = apply_difficulty_presets(
                {
                    "count": 1,
                    "difficulty_tier": tier,
                    "include_answer_key": True,
                },
                type_id=type_id,
                setting_profile=profile,
            )
            q = qt.generate(settings)[0]
            rows.append(
                {
                    "type_id": type_id,
                    "name": qt.name if hasattr(qt, "name") else type_id,
                    "generator": getattr(qt, "generator", "") or "",
                    "tier": tier,
                    "sample_index": i,
                    "prompt_latex": q.prompt_latex or "",
                    "answer_latex": q.answer_latex or "",
                    "instruction_latex": getattr(q, "instruction_latex", "") or "",
                }
            )
    return rows


def _write_md(all_rows: dict[str, list[dict]]) -> None:
    lines = [
        "# Calculus stub pilot gallery",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Pilot only — 3 former `calculus_foundations` stubs, expanded for "
        "**expression ordering** and **function-family** variety. Not a full stub rollout.",
        "",
        "## Pilot topics",
        "",
    ]
    for tid in PILOT_TYPE_IDS:
        meta = TEXTBOOK_ANCHORS[tid]
        lines.append(f"### `{tid}`")
        lines.append("")
        lines.append(f"- **OpenStax:** {', '.join(meta['sections'])}")
        lines.append("- **Seed examples:**")
        for s in meta["seed_examples"]:
            lines.append(f"  - {s}")
        lines.append("- **Variety added:**")
        for v in meta["variety_added"]:
            lines.append(f"  - {v}")
        lines.append("")
        by_tier: dict[str, list[dict]] = defaultdict(list)
        for row in all_rows[tid]:
            by_tier[row["tier"]].append(row)
        for tier in TIERS:
            lines.append(f"#### {tier.title()}")
            lines.append("")
            for row in by_tier[tier]:
                lines.append(f"- Stem: `${row['prompt_latex']}$`")
                lines.append(f"  - Answer: `${row['answer_latex']}$`")
            lines.append("")

    lines.extend(
        [
            "## Proposed next batch (after approval)",
            "",
            "Still on `calculus_foundations` (or thin), same variety treatment:",
            "",
        ]
    )
    for tid in NEXT_BATCH:
        lines.append(f"- `{tid}`")
    lines.append("")
    lines.append(
        "Deferred for later review: curve sketching, graphical f/f'/f'', "
        "motion revisited, DE introduction (need diagram/word-problem design)."
    )
    lines.append("")
    (OUT / "gallery.md").write_text("\n".join(lines), encoding="utf-8")


def _write_notes() -> None:
    text = """# Calculus pilot — approach notes

## Goal

Show what “generalize from textbook examples” looks like **before** wiring every
remaining calculus stub. Emphasis: many orderings of the same expression, and
several function families, under the **same skill** with easy/medium/hard.

## Pilot set (3)

| Type id | Skill | OpenStax anchors |
|---------|-------|------------------|
| `calc_app_diff_slope_tangent_and_normal_lines` | Tangent / normal line | §3.1 Ex 3.1–3.3, 3.5 |
| `calc_app_diff_differentials` | Find / evaluate `dy` | §4.2 Ex 4.8–4.9 |
| `calc_indef_int_logarithmic_rule_and_exponentials_with_substitution` | Log/exp + u-sub | §§5.5–5.6 Ex 5.30–5.39 |

## Textbook → variants (examples)

### Tangent line

| Textbook seed | Generalized variants |
|---------------|----------------------|
| `f(x)=x²` at `x=3` | `x^n`, reordered quads `2x+x²` / `x(x+2)`, cubics |
| `f(x)=1/x` at `x=2` | also `x^{-1}`; normals as well as tangents |
| `3x²−4x+1` | random quads; radicals, sin/cos, `e^{kx}` / `\\exp(kx)`, ln, `(x+p)/(x+q)` |

### Differentials

| Textbook seed | Generalized variants |
|---------------|----------------------|
| `y=x²+2x` | reversed / factored display; powers; product/quotient |
| `y=\\cos x` | sin/cos/tan; `e^{kx}`; `√x` vs `x^{1/2}`; evaluate at `(x,dx)` |

### Log/exp substitution

| Textbook seed | Generalized variants |
|---------------|----------------------|
| `∫ e^{-x} dx` | `e^{kx}`, `e^{ax+b}` vs `e^{b+ax}` |
| `∫ e^x/(1+e^x) dx` | also `e^x(1+e^x)^{-1}` |
| `∫ 3x² e^{2x³} dx` | factor on left or right of exp; `2x e^{x²}` family |
| du/u forms | `2x/(x²+c)`, `(x²+c)^{-1}·2x`, `2x/(c+x²)`, missing-constant factor |

## What we did **not** do yet

- Remaining ~14 `calculus_foundations` stubs stay thin.
- No commit of a full calculus stub sweep.
- Curve sketching / graphical comparison need richer diagram specs — better as their own design pass.

## How to regenerate

```powershell
$env:PYTHONPATH='.'
python scripts/build_calculus_pilot_gallery.py
python -m pytest question_engine/tests/test_calculus_pilot.py -q
```
"""
    (OUT / "PILOT_NOTES.md").write_text(text, encoding="utf-8")


def _write_html(all_rows: dict[str, list[dict]]) -> None:
    sections = []
    for tid in PILOT_TYPE_IDS:
        meta = TEXTBOOK_ANCHORS[tid]
        blocks = [
            f"<section class='type'><h2><code>{html.escape(tid)}</code></h2>",
            f"<p class='meta'><strong>OpenStax:</strong> {html.escape(', '.join(meta['sections']))}</p>",
            "<ul class='seeds'>",
        ]
        for s in meta["seed_examples"]:
            blocks.append(f"<li>{html.escape(s)}</li>")
        blocks.append("</ul><p><strong>Variety:</strong></p><ul>")
        for v in meta["variety_added"]:
            blocks.append(f"<li>{html.escape(v)}</li>")
        blocks.append("</ul>")
        by_tier: dict[str, list[dict]] = defaultdict(list)
        for row in all_rows[tid]:
            by_tier[row["tier"]].append(row)
        for tier in TIERS:
            blocks.append(f"<h3>{tier.title()}</h3><ol>")
            for row in by_tier[tier]:
                blocks.append(
                    "<li><div class='stem'>\\("
                    + row["prompt_latex"]
                    + "\\)</div>"
                    "<div class='ans'>Answer: \\("
                    + row["answer_latex"]
                    + "\\)</div></li>"
                )
            blocks.append("</ol>")
        blocks.append("</section>")
        sections.append("\n".join(blocks))

    next_items = "\n".join(f"<li><code>{html.escape(t)}</code></li>" for t in NEXT_BATCH)
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>Calculus stub pilot gallery</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css"/>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body, {{delimiters:[
    {{left:'\\\\(', right:'\\\\)', display:false}},
    {{left:'$$', right:'$$', display:true}}
  ]}});"></script>
<style>
body {{ font-family: Georgia, 'Times New Roman', serif; margin: 1.5rem auto; max-width: 52rem;
  line-height: 1.45; color: #1a1a1a; padding: 0 1rem; }}
h1 {{ font-size: 1.6rem; }}
.type {{ border-top: 1px solid #ccc; padding-top: 1rem; margin-top: 1.5rem; }}
.stem {{ margin: 0.25rem 0; }}
.ans {{ color: #334; font-size: 0.95rem; margin-bottom: 0.6rem; }}
.meta, .seeds {{ color: #333; }}
code {{ font-size: 0.9em; }}
.next {{ background: #f6f6f4; padding: 0.75rem 1rem; border-radius: 4px; }}
</style>
</head>
<body>
<h1>Calculus stub pilot gallery</h1>
<p>Three former thin stubs, expanded for expression ordering and function-family
variety (OpenStax Vol.&nbsp;1 patterns). Review before approving a wider batch.</p>
{"".join(sections)}
<section class="next">
<h2>Proposed next batch</h2>
<ul>{next_items}</ul>
</section>
</body>
</html>
"""
    (OUT / "gallery.html").write_text(doc, encoding="utf-8")


def main() -> int:
    random.seed(20260717)
    OUT.mkdir(parents=True, exist_ok=True)
    all_rows: dict[str, list[dict]] = {}
    flat: list[dict] = []
    for tid in PILOT_TYPE_IDS:
        rows = _sample(tid)
        all_rows[tid] = rows
        flat.extend(rows)
    _write_md(all_rows)
    _write_html(all_rows)
    _write_notes()
    (OUT / "samples.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in flat) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUT}")
    print(f"  gallery.md / gallery.html / PILOT_NOTES.md / samples.jsonl")
    print(f"  {len(flat)} samples across {len(PILOT_TYPE_IDS)} types")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
