"""Build gallery for enriched calculus derivative-rule generators.

Writes scripts/output/topic_fit/calculus_derivative_rules/:
  gallery.md, gallery.html, NOTES.md, samples.jsonl

Usage:
  $env:PYTHONPATH='.'
  python scripts/build_calculus_derivative_rules_gallery.py
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

OUT = ROOT / "scripts" / "output" / "topic_fit" / "calculus_derivative_rules"
TIERS = ("easy", "medium", "hard")
N_PER_TIER = 3

TYPE_IDS = (
    "calc_diff_average_rates_of_change",
    "calc_diff_definition_of_the_derivative",
    "calc_diff_instantaneous_rates_of_change",
    "calc_diff_power_rule",
    "calc_diff_higher_order_derivatives",
    "calc_diff_product_rule",
    "calc_diff_quotient_rule",
    "calc_diff_chain_rule",
    "calc_diff_trigonometric",
    "calc_diff_inverse_trigonometric",
    "calc_diff_natural_logarithms_and_exponentials",
    "calc_diff_other_base_logarithms_and_exponentials",
    "calc_diff_logarithmic",
    "calc_diff_implicit",
    "calc_diff_inverse_functions",
)

REMAINING = [
    "calc_diff_rules_using_tables (already dedicated; light enhancement optional)",
    "Applications of differentiation stubs still on calculus_foundations "
    "(concavity, extrema, optimization, curve sketching, motion, Newton, …)",
    "Integration / DE stubs outside this derivative-rules batch",
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
                    "tier": tier,
                    "sample_index": i,
                    "prompt_latex": q.prompt_latex or "",
                    "answer_latex": q.answer_latex or "",
                    "generator": getattr(qt, "generator", "") or "",
                }
            )
    return rows


def _write_md(all_rows: dict[str, list[dict]]) -> None:
    lines = [
        "# Calculus derivative-rules gallery",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Same approach as the calculus pilot: **expression orderings**, "
        "**function-family variety**, and **EMH within skill**, generalized from "
        "OpenStax Calculus Vol. 1 Ch. 3 patterns (paraphrased).",
        "",
        "## Types in this batch",
        "",
    ]
    for tid in TYPE_IDS:
        lines.append(f"- `{tid}`")
    lines.append("")
    for tid in TYPE_IDS:
        lines.append(f"### `{tid}`")
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
    lines.extend(["## Still remaining (not this batch)", ""])
    for item in REMAINING:
        lines.append(f"- {item}")
    lines.append("")
    (OUT / "gallery.md").write_text("\n".join(lines), encoding="utf-8")


def _write_html(all_rows: dict[str, list[dict]]) -> None:
    sections = []
    for tid in TYPE_IDS:
        blocks = [f"<section class='type'><h2><code>{html.escape(tid)}</code></h2>"]
        by_tier: dict[str, list[dict]] = defaultdict(list)
        for row in all_rows[tid]:
            by_tier[row["tier"]].append(row)
        for tier in TIERS:
            blocks.append(f"<h3>{tier.title()}</h3><ol>")
            for row in by_tier[tier]:
                blocks.append(
                    "<li><div class='stem'>\\("
                    + row["prompt_latex"]
                    + "\\)</div><div class='ans'>Answer: \\("
                    + row["answer_latex"]
                    + "\\)</div></li>"
                )
            blocks.append("</ol>")
        blocks.append("</section>")
        sections.append("\n".join(blocks))
    rem = "\n".join(f"<li>{html.escape(x)}</li>" for x in REMAINING)
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>Calculus derivative-rules gallery</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css"/>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body, {{delimiters:[
    {{left:'\\\\(', right:'\\\\)', display:false}},
    {{left:'$$', right:'$$', display:true}}
  ]}});"></script>
<style>
body {{ font-family: Georgia, 'Times New Roman', serif; margin: 1.5rem auto; max-width: 54rem;
  line-height: 1.45; color: #1a1a1a; padding: 0 1rem; }}
h1 {{ font-size: 1.55rem; }}
.type {{ border-top: 1px solid #ccc; padding-top: 1rem; margin-top: 1.25rem; }}
.stem {{ margin: 0.25rem 0; }}
.ans {{ color: #334; font-size: 0.95rem; margin-bottom: 0.55rem; }}
code {{ font-size: 0.88em; }}
.next {{ background: #f6f6f4; padding: 0.75rem 1rem; border-radius: 4px; }}
</style>
</head>
<body>
<h1>Calculus derivative-rules gallery</h1>
<p>Enriched Differentiation types: expression orderings + function families,
EMH within skill. OpenStax Vol.&nbsp;1 Ch.&nbsp;3 patterns generalized.</p>
{"".join(sections)}
<section class="next"><h2>Remaining (out of this batch)</h2><ul>{rem}</ul></section>
</body>
</html>
"""
    (OUT / "gallery.html").write_text(doc, encoding="utf-8")


def _write_notes() -> None:
    (OUT / "NOTES.md").write_text(
        """# Calculus derivative-rules batch

## What changed

- New module `question_engine/generators/calculus_derivative_rules.py` overrides
  thin derivative builders with ordering/family variety.
- New/fixed wirings:
  - `instantaneous_rate_of_change` (was `calculus_foundations`)
  - `derivative_inverse_functions` (was `calculus_foundations`)
  - `derivative_logarithmic` (was miswired to plain `derivative_ln_exp`)

## Variety examples

| Rule | Seed pattern | Added variants |
|------|--------------|----------------|
| Power | ∑ a_k x^k | reversed terms, x^{-n} vs 1/x^n, fractional powers, factored x(x+b) |
| Product | (ax+b)(cx+d) | · vs juxtaposition, factor order, x sin x / x e^x |
| Quotient | (ax+b)/(cx+d) | frac vs ( )( )^{-1}; sin/x; linear over quadratic |
| Chain | (ax+b)^n | b+ax inner; e^{inner}/exp; √; sin(a x^n); nested powers |
| Trig | sin x | cot/sec/csc; k·x vs kx; products; sin²x |
| Inv trig | arcsin x | sin^{-1} notation; arcsin(ax+b); arctan(x^k) |
| Ln/exp | ln(x^n), e^{kx} | exp(); e^{b+ax}; ln\\|ax+b\\|; e^{x²} |
| Other base | a^x, log_a x | a^{kx}; log_a(ax+b); x·a^x product |
| Log diff | — | products/quotients of powers; x^x; (sin x)^x |
| Implicit | x²+y²=a | term order; xy; ellipses; cubes; sin/cos |
| Rates / definition | x² | reciprocal/sqrt/trig/exp; limit forms h vs x→a |

## Regenerate

```powershell
$env:PYTHONPATH='.'
python scripts/build_calculus_derivative_rules_gallery.py
python -m pytest question_engine/tests/test_calculus_derivative_rules.py -q
```
""",
        encoding="utf-8",
    )


def main() -> int:
    random.seed(20260717)
    OUT.mkdir(parents=True, exist_ok=True)
    all_rows: dict[str, list[dict]] = {}
    flat: list[dict] = []
    for tid in TYPE_IDS:
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
    print(f"  {len(flat)} samples across {len(TYPE_IDS)} types")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
