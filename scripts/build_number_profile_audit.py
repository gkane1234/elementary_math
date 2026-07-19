"""Emit audit galleries for Layer 0 number lanes.

Two views under scripts/output/topic_fit/number_profile_audit/:

1. **lane_from_d/** — primary: overall D + constraints → which lane is selected,
   with sample numbers. This matches the product mental model.
2. **per_profile/** — legacy forced-profile samples (within-lane escalation only).

Also writes root gallery.md / gallery.html pointing at the D-selects-lane view.

Usage:
  $env:PYTHONPATH='.'
  python scripts/build_number_profile_audit.py
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

from question_engine.frameworks.primitives.numbers import (
    LANE_MIN_D,
    NUMBER_PROFILES,
    PROFILE_CATALOG,
    audit_lane_selection,
    audit_samples,
    eligible_lanes,
    resolve_constraints,
)

OUT = ROOT / "scripts" / "output" / "topic_fit" / "number_profile_audit"
LANE_FROM_D = OUT / "lane_from_d"
PER_PROFILE = OUT / "per_profile"

DIFFICULTIES = (0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0)
PROFILE_DIFFICULTIES = (0.0, 3.0, 6.0, 10.0, 14.0)
N_PER = 8

CONSTRAINT_SETS: dict[str, dict[str, Any]] = {
    "default": {},
    "integers_only": {"integers_only": True},
    "no_decimals": {"allow_decimals": False},
    "no_fractions": {"allow_fractions": False},
    "positives_only": {"allow_negatives": False},
    "integers_no_negatives": {"integers_only": True, "allow_negatives": False},
}


def _escape_md_latex(s: str) -> str:
    return s.replace("|", "\\|")


def _constraint_label(name: str, settings: dict[str, Any]) -> str:
    c = resolve_constraints(settings)
    parts = [name]
    flags = []
    if c.integers_only:
        flags.append("integers_only")
    if not c.allow_negatives:
        flags.append("no negatives")
    if not c.allow_fractions:
        flags.append("no fractions")
    if not c.allow_decimals:
        flags.append("no decimals")
    if flags:
        parts.append(f"({', '.join(flags)})")
    return " ".join(parts)


def build_lane_from_d_markdown(rows: list[dict]) -> str:
    lines = [
        "# Difficulty → lane selection audit",
        "",
        "Overall topic **difficulty D** plus **constraints** choose the number lane; "
        "values are then sampled inside that lane at the same effective D.",
        "",
        "## Lane unlock thresholds (min D)",
        "",
        "| Lane | min D |",
        "|------|------:|",
    ]
    for pid in NUMBER_PROFILES:
        lines.append(f"| `{pid}` | {LANE_MIN_D[pid]:g} |")
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
        lines.append("| D | Eligible lanes | Selected (counts) | Sample values |")
        lines.append("|--:|----------------|-------------------|---------------|")
        for d in DIFFICULTIES:
            at_d = [r for r in group if float(r["difficulty"]) == d]
            if not at_d:
                continue
            eligible = at_d[0].get("eligible") or []
            counts = Counter(r["selected"] for r in at_d)
            count_str = ", ".join(f"`{k}`×{v}" for k, v in counts.most_common())
            samples = ", ".join(
                f"${_escape_md_latex(r['latex'])}$" for r in at_d[:6]
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
    h3 { margin-top: 1.25rem; }
    .lede { max-width: 52rem; color: #444; }
    .code { font-family: ui-monospace, Consolas, monospace; font-size: 0.85em; }
    .samples { font-family: "Cambria Math", "Times New Roman", serif; font-size: 1.05rem; }
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
        "<title>D → lane selection audit</title>",
        f"<style>{css}</style>",
        katex_head,
        "</head><body>",
        "<h1>Difficulty → lane selection</h1>",
        '<p class="lede">Topic <strong>difficulty D</strong> plus <strong>constraints</strong> '
        "choose the number lane; samples below are drawn inside the selected lane.</p>",
        "<h2>Unlock thresholds</h2>",
        '<table class="thresholds"><thead><tr><th>Lane</th><th>min D</th>'
        "<th>Summary</th></tr></thead><tbody>",
    ]
    for pid in NUMBER_PROFILES:
        meta = PROFILE_CATALOG[pid]
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
            "<th>D</th><th>Eligible</th><th>Selected counts</th><th>Samples</th>"
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


def build_per_profile_markdown(by_profile: dict[str, list[dict]]) -> str:
    lines = [
        "# Forced-profile audit (within-lane only)",
        "",
        "Each profile is forced. Difficulty only escalates *within* the lane. "
        "Prefer the **lane_from_d** gallery for the product path (D + constraints).",
        "",
    ]
    for pid in NUMBER_PROFILES:
        meta = PROFILE_CATALOG[pid]
        lines.append(f"## {meta['label']} (`{pid}`)")
        lines.append("")
        rows = by_profile[pid]
        by_d: dict[float, list] = {}
        for row in rows:
            by_d.setdefault(float(row["difficulty"]), []).append(row)
        for d in PROFILE_DIFFICULTIES:
            group = by_d.get(d, [])
            samples = ", ".join(f"${_escape_md_latex(r['latex'])}$" for r in group)
            lines.append(f"- **D={d:g}:** {samples}")
        lines.append("")
    return "\n".join(lines) + "\n"


def build_index_markdown() -> str:
    return (
        "# Number lane audit\n\n"
        "Primary view: **[lane_from_d/gallery.md](lane_from_d/gallery.md)** "
        "(also [HTML](lane_from_d/gallery.html)) — overall D + constraints → selected lane.\n\n"
        "Legacy forced-profile view: "
        "[per_profile/gallery.md](per_profile/gallery.md).\n\n"
        "## Thresholds\n\n"
        "| Lane | min D |\n|------|------:|\n"
        + "\n".join(f"| `{p}` | {LANE_MIN_D[p]:g} |" for p in NUMBER_PROFILES)
        + "\n"
    )


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    LANE_FROM_D.mkdir(parents=True, exist_ok=True)
    PER_PROFILE.mkdir(parents=True, exist_ok=True)

    # --- D → lane ---
    lane_rows = audit_lane_selection(
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
        json.dumps(lane_rows, indent=2) + "\n", encoding="utf-8"
    )

    # Eligibility snapshot for quick asserts / docs
    eligibility: dict[str, dict[str, list[str]]] = {}
    for cname, csettings in CONSTRAINT_SETS.items():
        constraints = resolve_constraints(csettings)
        eligibility[cname] = {
            str(int(d) if d == int(d) else d): eligible_lanes(d, constraints)
            for d in DIFFICULTIES
        }
    (LANE_FROM_D / "eligibility.json").write_text(
        json.dumps(eligibility, indent=2) + "\n", encoding="utf-8"
    )

    # --- forced per-profile ---
    by_profile: dict[str, list[dict]] = {}
    all_forced: list[dict] = []
    for pid in NUMBER_PROFILES:
        rows = audit_samples(
            pid, difficulties=PROFILE_DIFFICULTIES, n_per=N_PER, seed=1
        )
        by_profile[pid] = rows
        all_forced.extend(rows)
    (PER_PROFILE / "gallery.md").write_text(
        build_per_profile_markdown(by_profile), encoding="utf-8"
    )
    (PER_PROFILE / "samples.json").write_text(
        json.dumps(all_forced, indent=2) + "\n", encoding="utf-8"
    )

    # Root index + mirror primary gallery at root for older links
    (OUT / "gallery.md").write_text(build_index_markdown(), encoding="utf-8")
    (OUT / "gallery.html").write_text(
        build_lane_from_d_html(lane_rows), encoding="utf-8"
    )
    (OUT / "samples.json").write_text(
        json.dumps(lane_rows, indent=2) + "\n", encoding="utf-8"
    )

    print(f"Wrote {LANE_FROM_D.relative_to(ROOT)}/gallery.{{md,html}}")
    print(f"Wrote {PER_PROFILE.relative_to(ROOT)}/gallery.md")
    print(f"Wrote {OUT.relative_to(ROOT)}/gallery.{{md,html}} (index / primary)")
    print(
        f"Constraint sets: {len(CONSTRAINT_SETS)}  "
        f"Ds: {DIFFICULTIES}  Lane samples: {len(lane_rows)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
