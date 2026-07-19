"""Build audits for constructive L1–L4 (OOO, expand, rational, PFD)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "scripts" / "output" / "topic_fit"


def _gallery(title: str, rows: list[dict], path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    lines = [
        "<!DOCTYPE html><html><head><meta charset='utf-8'>",
        "<script src='https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js'></script>",
        "<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css'>",
        f"<title>{title}</title>",
        "<style>body{font-family:system-ui;margin:1.5rem} .row{margin:1rem 0;padding:.75rem;border-bottom:1px solid #ddd}</style>",
        "</head><body>",
        f"<h1>{title}</h1>",
    ]
    md = [f"# {title}", ""]
    for r in rows:
        lines.append("<div class='row'>")
        lines.append(f"<div><b>D={r.get('d')}</b> level={r.get('level')} inflators={r.get('inflators')}</div>")
        lines.append(f"<div>Prompt: <span class='tex'>{r['prompt']}</span></div>")
        if r.get("answer"):
            lines.append(f"<div>Answer: <span class='tex'>{r['answer']}</span></div>")
        lines.append("</div>")
        md.append(f"- **D={r.get('d')}** `{r.get('level')}`: `{r['prompt']}` → `{r.get('answer')}`")
    lines.append(
        "<script>document.querySelectorAll('.tex').forEach(el=>{"
        "try{katex.render(el.textContent, el, {throwOnError:false})}catch(e){}"
        "})</script></body></html>"
    )
    (path / "gallery.html").write_text("\n".join(lines), encoding="utf-8")
    (path / "gallery.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    (path / "samples.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")


def main() -> None:
    from question_engine.frameworks.primitives.constructive import (
        construct_affine,
        construct_numeric,
        construct_pfd,
        construct_rational_sum,
    )
    from question_engine.frameworks.primitives.registry import (
        PRIM_EXPAND_SIMPLIFY,
        PRIM_NUMBERS,
        PRIM_OOO,
        PRIM_VARIABLE,
        build_context,
    )

    ooo_rows = []
    expand_rows = []
    rat_rows = []
    pfd_rows = []
    for d in (0, 2, 4, 6, 8, 10, 14, 20):
        ctx = build_context(
            {"difficulty": d, "integers_only": True, "only_x": True, "lock_variable": "x"},
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_OOO, PRIM_EXPAND_SIMPLIFY],
        )
        n = construct_numeric(ctx, d=d)
        ooo_rows.append(
            {
                "d": d,
                "level": n.level,
                "inflators": list(n.inflators_applied),
                "prompt": n.latex,
                "answer": str(n.value),
            }
        )
        a = construct_affine(ctx, d=d)
        expand_rows.append(
            {
                "d": d,
                "level": a.level,
                "inflators": list(a.inflators_applied),
                "prompt": a.latex,
                "answer": a.simplified_latex,
            }
        )
        r = construct_rational_sum(ctx, d=d, cancel_count=0 if d < 5 else 0)
        rat_rows.append(
            {
                "d": d,
                "level": r.level,
                "inflators": list(r.inflators_applied),
                "prompt": r.latex,
                "answer": r.simplified_latex,
            }
        )
        if d >= 3:
            s = construct_rational_sum(ctx, d=d, cancel_count=1)
            rat_rows.append(
                {
                    "d": d,
                    "level": s.level,
                    "inflators": list(s.inflators_applied),
                    "prompt": s.latex,
                    "answer": s.simplified_latex,
                }
            )
        p = construct_pfd(ctx, d=d)
        pfd_rows.append(
            {
                "d": d,
                "level": p.level,
                "inflators": list(p.inflators_applied),
                "prompt": p.latex,
                "answer": p.simplified_latex,
            }
        )

    _gallery("Constructive OOO (L1 numeric)", ooo_rows, OUT / "constructive_ooo_audit")
    _gallery("Constructive expand/simplify (L1 affine)", expand_rows, OUT / "constructive_expand_audit")
    _gallery("Constructive rationals (L2/L3)", rat_rows, OUT / "constructive_rational_audit")
    _gallery("Constructive PFD (L4)", pfd_rows, OUT / "constructive_pfd_audit")
    print("Wrote constructive audits under", OUT)


if __name__ == "__main__":
    main()
