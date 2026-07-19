"""Emit audit gallery for Layer 0 variable lanes (D + constraints → pool).

Writes under scripts/output/topic_fit/variable_lane_audit/lane_from_d/:
  gallery.html, gallery.md, samples.json, eligibility.json

Usage:
  $env:PYTHONPATH='.'
  python scripts/build_variable_lane_audit.py
"""

from __future__ import annotations

import html
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from question_engine.frameworks.primitives.variables import (
    LANE_CATALOG,
    LANE_MIN_D,
    VARIABLE_LANES,
    audit_variable_lane_selection,
    eligible_variable_lanes,
    resolve_variable_constraints,
)

OUT = ROOT / "scripts" / "output" / "topic_fit" / "variable_lane_audit"
LANE_FROM_D = OUT / "lane_from_d"

DIFFICULTIES = (0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0)
N_PER = 8

CONSTRAINT_SETS: dict[str, dict[str, Any]] = {
    "default": {},
    "only_x": {"only_x": True},
    "no_greek": {"allow_greek": False},
    "max_xyz": {"max_variable_lane": "xyz"},
    "max_common": {"max_variable_lane": "abctuvwxyz"},
    "legacy_no_other_letters": {"allow_other_letters": False},
}


def _escape_md_latex(s: str) -> str:
    return s.replace("|", "\\|")


def _constraint_label(name: str, settings: dict[str, Any]) -> str:
    c = resolve_variable_constraints(settings)
    parts = [name]
    flags = []
    if c.only_x:
        flags.append("only_x")
    if not c.allow_greek:
        flags.append("no greek")
    if c.max_variable_lane:
        flags.append(f"max={c.max_variable_lane}")
    if flags:
        parts.append(f"({', '.join(flags)})")
    return " ".join(parts)


def build_lane_from_d_markdown(rows: list[dict]) -> str:
    lines = [
        "# Difficulty → variable lane selection audit",
        "",
        "Overall topic **difficulty D** plus **constraints** choose the variable "
        "lane; letters are then sampled inside that lane.",
        "",
        "## Lane unlock thresholds (min D)",
        "",
        "| Lane | min D | Pool sketch |",
        "|------|------:|-------------|",
    ]
    for pid in VARIABLE_LANES:
        meta = LANE_CATALOG[pid]
        lines.append(f"| `{pid}` | {LANE_MIN_D[pid]:g} | {meta['summary']} |")
    lines.append("")
    lines.append("Also open `gallery.html` for a browsable view.")
    lines.append("")

    by_constraint: dict[str, list[dict]] = {}
    for row in rows:
        by_constraint.setdefault(row["constraint_set"], []).append(row)

    for cname, csettings in CONSTRAINT_SETS.items():
        group = by_constraint.get(cname, [])
        lines.append(f"## {_constraint_label(cname, csettings)}")
        lines.append("")
        lines.append(
            f"Settings: `{json.dumps(csettings) if csettings else '{}'}`"
        )
        lines.append("")
        lines.append("| D | Eligible lanes | Selected (counts) | Sample letters |")
        lines.append("|--:|----------------|-------------------|----------------|")
        for d in DIFFICULTIES:
            at_d = [r for r in group if float(r["difficulty"]) == d]
            if not at_d:
                continue
            eligible = at_d[0].get("eligible") or []
            counts = Counter(r["selected"] for r in at_d)
            count_str = ", ".join(f"`{k}`×{v}" for k, v in counts.most_common())
            samples = ", ".join(
                f"${_escape_md_latex(r['latex'])}$" for r in at_d[:8]
            )
            elig_str = ", ".join(f"`{e}`" for e in eligible)
            lines.append(
                f"| {d:g} | {elig_str} | {count_str} | {samples} |"
            )
        lines.append("")

    return "\n".join(lines) + "\n"


def build_lane_from_d_html(rows: list[dict]) -> str:
    css = """
    :root { color-scheme: light; }
    body { font-family: Georgia, "Times New Roman", serif; margin: 1.5rem 2rem; line-height: 1.45;
           color: #1a1a1a; background: #faf9f7; }
    h1 { font-size: 1.75rem; margin-bottom: 0.25rem; }
    h2 { margin-top: 2rem; border-bottom: 1px solid #ccc; padding-bottom: 0.25rem; }
    .lede { max-width: 52rem; color: #444; }
    .code { font-family: ui-monospace, Consolas, monospace; font-size: 0.85em; }
    .samples { font-family: "Cambria Math", "Times New Roman", serif; font-size: 1.15rem; }
    table.compare { border-collapse: collapse; width: 100%; font-size: 0.88rem; margin: 0.5rem 0 1.5rem; }
    table.compare th, table.compare td { border: 1px solid #ccc; padding: 0.4rem 0.5rem; vertical-align: top; }
    table.compare th { background: #e8e6e1; }
    .pill { display: inline-block; background: #eef2f7; border: 1px solid #c5d0de;
            border-radius: 3px; padding: 0.05rem 0.35rem; margin: 0.1rem; font-size: 0.8rem; }
    .thresholds { border-collapse: collapse; font-size: 0.9rem; margin-bottom: 1rem; }
    .thresholds th, .thresholds td { border: 1px solid #ccc; padding: 0.3rem 0.5rem; }
    """
    katex_head = (
        '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css"/>\n'
        '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>\n'
        '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js" '
        "onload=\"renderMathInElement(document.body,{delimiters:["
        "{left:'$',right:'$',display:false},{left:'$$',right:'$$',display:true}"
        ']})"></script>'
    )
    parts = [
        "<!DOCTYPE html>",
        '<html lang="en"><head><meta charset="utf-8"/>',
        "<title>D → variable lane audit</title>",
        f"<style>{css}</style>",
        katex_head,
        "</head><body>",
        "<h1>Difficulty → variable lane selection</h1>",
        '<p class="lede">Topic <strong>difficulty D</strong> plus <strong>constraints</strong> '
        "choose the variable lane; samples below are letters drawn inside that lane.</p>",
        "<h2>Unlock thresholds</h2>",
        '<table class="thresholds"><thead><tr><th>Lane</th><th>min D</th>'
        "<th>Summary</th></tr></thead><tbody>",
    ]
    for pid in VARIABLE_LANES:
        meta = LANE_CATALOG[pid]
        parts.append(
            "<tr>"
            f'<td class="code">{html.escape(pid)}</td>'
            f"<td>{LANE_MIN_D[pid]:g}</td>"
            f"<td>{html.escape(meta['summary'])}</td>"
            "</tr>"
        )
    parts.append("</tbody></table>")

    by_constraint: dict[str, list[dict]] = {}
    for row in rows:
        by_constraint.setdefault(row["constraint_set"], []).append(row)

    for cname, csettings in CONSTRAINT_SETS.items():
        group = by_constraint.get(cname, [])
        parts.append(f"<h2>{html.escape(_constraint_label(cname, csettings))}</h2>")
        parts.append(
            f'<p class="code">{html.escape(json.dumps(csettings) if csettings else "{}")}</p>'
        )
        parts.append('<table class="compare"><thead><tr>')
        parts.append(
            "<th>D</th><th>Eligible</th><th>Selected counts</th><th>Sample letters</th>"
        )
        parts.append("</tr></thead><tbody>")
        for d in DIFFICULTIES:
            at_d = [r for r in group if float(r["difficulty"]) == d]
            if not at_d:
                continue
            eligible = at_d[0].get("eligible") or []
            counts = Counter(r["selected"] for r in at_d)
            elig_html = " ".join(
                f'<span class="pill code">{html.escape(e)}</span>' for e in eligible
            )
            count_html = ", ".join(
                f'<span class="code">{html.escape(k)}</span>×{v}'
                for k, v in counts.most_common()
            )
            sample_html = ", ".join(f"${html.escape(r['latex'])}$" for r in at_d)
            parts.append(
                "<tr>"
                f"<td>{d:g}</td>"
                f"<td>{elig_html}</td>"
                f"<td>{count_html}</td>"
                f'<td class="samples">{sample_html}</td>'
                "</tr>"
            )
        parts.append("</tbody></table>")

    parts.append("</body></html>")
    return "\n".join(parts) + "\n"


def build_index_markdown() -> str:
    return (
        "# Variable lane audit\n\n"
        "Primary view: **[lane_from_d/gallery.md](lane_from_d/gallery.md)** "
        "(also [HTML](lane_from_d/gallery.html)) — overall D + constraints → "
        "selected variable lane.\n\n"
        "## Thresholds\n\n"
        "| Lane | min D |\n|------|------:|\n"
        + "\n".join(f"| `{p}` | {LANE_MIN_D[p]:g} |" for p in VARIABLE_LANES)
        + "\n"
    )


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    LANE_FROM_D.mkdir(parents=True, exist_ok=True)

    lane_rows = audit_variable_lane_selection(
        difficulties=DIFFICULTIES,
        constraint_sets=CONSTRAINT_SETS,
        n_per=N_PER,
        seed=1,
    )
    (LANE_FROM_D / "gallery.md").write_text(
        build_lane_from_d_markdown(lane_rows), encoding="utf-8"
    )
    (LANE_FROM_D / "gallery.html").write_text(
        build_lane_from_d_html(lane_rows), encoding="utf-8"
    )
    (LANE_FROM_D / "samples.json").write_text(
        json.dumps(lane_rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    eligibility: dict[str, dict[str, list[str]]] = {}
    for cname, csettings in CONSTRAINT_SETS.items():
        constraints = resolve_variable_constraints(csettings)
        eligibility[cname] = {
            str(int(d) if d == int(d) else d): eligible_variable_lanes(d, constraints)
            for d in DIFFICULTIES
        }
    (LANE_FROM_D / "eligibility.json").write_text(
        json.dumps(eligibility, indent=2) + "\n", encoding="utf-8"
    )

    (OUT / "gallery.md").write_text(build_index_markdown(), encoding="utf-8")
    (OUT / "gallery.html").write_text(
        build_lane_from_d_html(lane_rows), encoding="utf-8"
    )
    (OUT / "samples.json").write_text(
        json.dumps(lane_rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    print(f"Wrote {LANE_FROM_D.relative_to(ROOT)}/gallery.{{md,html}}")
    print(f"Wrote {OUT.relative_to(ROOT)}/gallery.{{md,html}} (index / primary)")
    print(
        f"Constraint sets: {len(CONSTRAINT_SETS)}  "
        f"Ds: {DIFFICULTIES}  Lane samples: {len(lane_rows)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
