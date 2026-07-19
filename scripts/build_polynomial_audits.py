"""Audit galleries for polynomial expression primitives.

Writes under scripts/output/topic_fit/:
  polynomial_naming_audit/
  polynomial_add_subtract_audit/
  polynomial_multiply_audit/
  polynomial_multiply_special_audit/
  evaluate_polynomial_audit/
  poly_combine_like_terms_audit/
  poly_expand_simplify_audit/
  factor_gcf_poly_policy_audit/
  quadratic_factoring_audit/
  polynomial_factoring_special_audit/
  polynomial_factoring_grouping_audit/

Also re-checks a linear leaf for no degree leak.

Usage:
  $env:PYTHONPATH='.'
  python scripts/build_polynomial_audits.py
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
    ("polynomial_naming_audit", "polynomial_naming", "Polynomial naming / classify", {}),
    ("polynomial_add_subtract_audit", "polynomial_add_subtract", "Add/subtract polynomials", {}),
    ("polynomial_multiply_audit", "polynomial_multiply", "Multiply polynomials", {}),
    (
        "polynomial_multiply_special_audit",
        "polynomial_multiply_special",
        "Multiply special products",
        {},
    ),
    ("evaluate_polynomial_audit", "evaluate_polynomial", "Evaluate polynomials", {}),
    (
        "poly_combine_like_terms_audit",
        "poly_combine_like_terms",
        "Combine like terms (poly policy)",
        {},
    ),
    (
        "poly_expand_simplify_audit",
        "poly_expand_simplify",
        "Expand then simplify (poly / FOIL)",
        {},
    ),
    (
        "factor_gcf_poly_policy_audit",
        "polynomial_factoring_common_factor",
        "Factor GCF (poly policy)",
        {},
    ),
    ("quadratic_factoring_audit", "quadratic_factoring", "Quadratic factoring", {"max_degree": 2}),
    (
        "polynomial_factoring_special_audit",
        "polynomial_factoring_special_cases",
        "Special product factoring",
        {},
    ),
    (
        "polynomial_factoring_grouping_audit",
        "polynomial_factoring_grouping",
        "Factoring by grouping",
        {},
    ),
    # Control: linear leaf must stay degree ≤ 1
    ("combine_like_terms_linear_gate_audit", "combining_like_terms", "Like terms (linear gate)", {}),
]


def _sample(gen_key: str, extra: dict[str, Any], *, linear: bool = False) -> list[dict[str, Any]]:
    gen = GENERATORS[gen_key]
    rows: list[dict[str, Any]] = []
    for d in DIFFICULTIES:
        settings: dict[str, Any] = {
            "count": N_PER,
            "include_answer_key": True,
            "difficulty": d,
            "integers_only": True,
            "only_x": True,
            **extra,
        }
        if not linear:
            settings.setdefault("max_degree", 3)
            settings.setdefault("expression_family", "polynomial")
        qs = gen(gen_key, settings)
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
                    "degree": meta.get("degree") or meta.get("max_degree"),
                    "method": meta.get("method"),
                    "pattern": meta.get("pattern"),
                    "op": meta.get("op"),
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
            meta_bits.append(
                f"<span class='pill'>family={html.escape(str(pol.get('family')))}</span>"
            )
        for key in ("degree", "upgrades", "method", "pattern", "op"):
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
    lines = [
        f"# {title}",
        "",
        lede,
        "",
        "| D | Prompt | Answer | Degree | Upgrades |",
        "|--:|--------|--------|--------|----------|",
    ]
    for r in rows:
        ups = ", ".join(str(u) for u in (r.get("upgrades") or [])) or "—"
        pl = (r.get("prompt_latex") or "").replace("|", "\\|")
        al = (r.get("answer_latex") or "").replace("|", "\\|")
        deg = r.get("degree") if r.get("degree") is not None else "—"
        lines.append(f"| {r['difficulty']:g} | ${pl}$ | ${al}$ | {deg} | {ups} |")
    lines.append("")
    return "\n".join(lines)


def _has_high_degree(blob: str) -> bool:
    return "^{2}" in blob or "^2" in blob or "^{3}" in blob or "^3" in blob


def main() -> None:
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    for folder, gen_key, title, extra in AUDITS:
        print(f"Building {folder} ({gen_key})...")
        is_linear = "linear" in folder
        rows = _sample(gen_key, extra, linear=is_linear)
        out = OUT_ROOT / folder
        out.mkdir(parents=True, exist_ok=True)
        (out / "samples.json").write_text(json.dumps(rows, indent=2, default=str), encoding="utf-8")
        lede = (
            f"Polynomial-primitive audit for `{gen_key}` across D={list(DIFFICULTIES)}. "
            "Degree grows as min(policy.max_degree, 2 + floor(log2(1 + D/4)))."
        )
        if "linear" in folder:
            lede = f"Linear control audit for `{gen_key}` — must stay degree ≤ 1."
        (out / "gallery.html").write_text(_html(title, lede, rows), encoding="utf-8")
        (out / "gallery.md").write_text(_md(title, lede, rows), encoding="utf-8")

        if "linear" in folder:
            for r in rows:
                blob = (r.get("prompt_latex") or "") + (r.get("answer_latex") or "")
                if _has_high_degree(blob):
                    raise SystemExit(f"Degree leak in {folder}: {blob}")
        else:
            # At least one sample at D≥6 should show degree > 1 (except pure naming words).
            high = [r for r in rows if float(r["difficulty"]) >= 6.0]
            if gen_key == "polynomial_naming":
                if not any(int(r.get("degree") or 0) >= 2 for r in high):
                    raise SystemExit(f"No degree≥2 metadata in {folder}")
            else:
                if not any(
                    _has_high_degree((r.get("prompt_latex") or "") + (r.get("answer_latex") or ""))
                    or int(r.get("degree") or 0) >= 2
                    for r in high
                ):
                    raise SystemExit(f"No degree>1 signal in {folder}")
    print("Done.")


if __name__ == "__main__":
    main()
