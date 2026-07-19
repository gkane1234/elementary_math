"""Audit galleries for linear-finish primitives (abs → systems → WP).

Writes under scripts/output/topic_fit/:
  absolute_value_equations_audit/
  absolute_value_inequalities_audit/
  compound_inequalities_audit/
  proportions_audit/
  literal_equations_audit/
  slope_audit/
  writing_linear_equations_audit/
  graph_linear_audit/
  systems_audit/
  word_problems_linear_audit/
  factor_gcf_linear_policy_audit/

Usage:
  $env:PYTHONPATH='.'
  python scripts/build_linear_finish_audits.py
"""

from __future__ import annotations

import html
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from question_engine.generators import GENERATORS

OUT_ROOT = ROOT / "scripts" / "output" / "topic_fit"
DIFFICULTIES = (0.0, 3.0, 6.0, 10.0, 14.0, 20.0)
N_PER = 3

AUDITS: list[tuple[str, str, str, dict[str, Any]]] = [
    ("absolute_value_equations_audit", "absolute_value_equations", "Absolute value equations", {}),
    ("absolute_value_inequalities_audit", "absolute_value_inequalities", "Absolute value inequalities", {}),
    ("compound_inequalities_audit", "compound_inequalities", "Compound inequalities", {}),
    ("proportions_audit", "solving_proportions", "Proportions", {}),
    ("literal_equations_audit", "literal_equations", "Literal equations", {}),
    ("slope_audit", "slope", "Slope", {}),
    ("writing_linear_equations_audit", "writing_linear_equations", "Writing linear equations", {}),
    ("graph_linear_audit", "graphing_linear_equations", "Graph linear equations", {}),
    ("systems_elim_audit", "systems_elimination", "Systems (elimination)", {}),
    ("systems_sub_audit", "systems_substitution", "Systems (substitution)", {}),
    ("systems_graph_audit", "systems_graphing", "Systems (graphing)", {}),
    ("word_problems_linear_audit", "wp_mixture", "Word problems (mixture→equation)", {}),
    ("wp_systems_audit", "wp_systems", "Word problems (systems)", {}),
    ("factor_gcf_linear_policy_audit", "factor_gcf", "Factor GCF (linear policy)", {}),
    ("factor_gcf_poly_policy_audit", "polynomial_factoring_common_factor", "Factor GCF (poly policy)", {}),
]


def _sample(gen_key: str, extra: dict[str, Any]) -> list[dict[str, Any]]:
    gen = GENERATORS[gen_key]
    rows: list[dict[str, Any]] = []
    for d in DIFFICULTIES:
        qs = gen(
            gen_key,
            {
                "count": N_PER,
                "include_answer_key": True,
                "difficulty": d,
                "integers_only": True,
                "only_x": True,
                **extra,
            },
        )
        for i, q in enumerate(qs):
            meta = q.metadata or {}
            rows.append(
                {
                    "difficulty": d,
                    "index": i,
                    "prompt_latex": q.prompt_latex,
                    "prompt_text": q.prompt_text,
                    "answer_latex": q.answer_latex,
                    "spend": meta.get("spend"),
                    "upgrades": meta.get("upgrades"),
                    "primitive_engine": meta.get("primitive_engine"),
                    "expression_policy": meta.get("expression_policy"),
                    "solution_kind": meta.get("solution_kind"),
                    "form": meta.get("form"),
                    "mode": meta.get("mode"),
                    "method": meta.get("method"),
                    "wp_kind": meta.get("wp_kind"),
                }
            )
    return rows


def _html(title: str, lede: str, rows: list[dict[str, Any]]) -> str:
    parts = [
        "<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'/>",
        f"<title>{html.escape(title)}</title>",
        "<style>body{font-family:Georgia,serif;margin:1.5rem 2rem;background:#faf9f7}"
        "table{border-collapse:collapse;width:100%;font-size:0.9rem}"
        "th,td{border:1px solid #ccc;padding:0.4rem;vertical-align:top}"
        "th{background:#e8e6e1}.pill{display:inline-block;background:#eef2f7;"
        "border:1px solid #c5d0de;border-radius:3px;padding:0.05rem 0.35rem;margin:0.1rem;"
        "font-size:0.8rem}.ans{color:#255}</style>",
        '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css"/>',
        '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>',
        (
            '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js" '
            "onload=\"renderMathInElement(document.body,{delimiters:["
            "{left:'$',right:'$',display:false},{left:'$$',right:'$$',display:true}]})\"></script>"
        ),
        f"</head><body><h1>{html.escape(title)}</h1><p>{html.escape(lede)}</p>",
        "<table><thead><tr><th>D</th><th>Meta</th><th>Samples</th></tr></thead><tbody>",
    ]
    by_d: dict[float, list[dict]] = {}
    for r in rows:
        by_d.setdefault(float(r["difficulty"]), []).append(r)
    for d in sorted(by_d):
        samples = by_d[d]
        meta_bits = []
        pol = samples[0].get("expression_policy") or {}
        if pol:
            meta_bits.append(
                f"<span class='pill'>max_degree={html.escape(str(pol.get('max_degree')))}</span>"
            )
        for key in ("upgrades", "form", "mode", "method", "solution_kind", "wp_kind"):
            val = samples[0].get(key)
            if val:
                meta_bits.append(
                    f"<span class='pill'>{html.escape(key)}={html.escape(str(val))}</span>"
                )
        sample_html = []
        for s in samples:
            pl = html.escape(s.get("prompt_latex") or "")
            al = html.escape(s.get("answer_latex") or "")
            sample_html.append(f"<div>${pl}$ <span class='ans'>→ ${al}$</span></div>")
        parts.append(
            f"<tr><td>{d:g}</td><td>{' '.join(meta_bits) or '—'}</td>"
            f"<td>{''.join(sample_html)}</td></tr>"
        )
    parts.append("</tbody></table></body></html>")
    return "\n".join(parts)


def _md(title: str, lede: str, rows: list[dict[str, Any]]) -> str:
    lines = [f"# {title}", "", lede, "", "| D | Prompt | Answer | Upgrades |", "|--:|--------|--------|----------|"]
    for r in rows:
        ups = ", ".join(str(u) for u in (r.get("upgrades") or [])) or "—"
        pl = (r.get("prompt_latex") or "").replace("|", "\\|")
        al = (r.get("answer_latex") or "").replace("|", "\\|")
        lines.append(f"| {r['difficulty']:g} | ${pl}$ | ${al}$ | {ups} |")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    for folder, gen_key, title, extra in AUDITS:
        print(f"Building {folder} ({gen_key})...")
        rows = _sample(gen_key, extra)
        out = OUT_ROOT / folder
        out.mkdir(parents=True, exist_ok=True)
        (out / "samples.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
        lede = f"Primitive-linear audit for `{gen_key}` across D={list(DIFFICULTIES)}."
        (out / "gallery.html").write_text(_html(title, lede, rows), encoding="utf-8")
        (out / "gallery.md").write_text(_md(title, lede, rows), encoding="utf-8")
        # Degree gate check for linear audits
        if "poly" not in folder:
            for r in rows:
                blob = (r.get("prompt_latex") or "") + (r.get("answer_latex") or "")
                if "^{2}" in blob or "^2" in blob:
                    raise SystemExit(f"Degree leak in {folder}: {blob}")
    print("Done.")


if __name__ == "__main__":
    main()
