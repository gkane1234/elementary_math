"""Audit Ready types: generate Easy/Medium/Hard samples and flag nonsense.

Run after scaffold wiring is complete. Does NOT write the PDF.

Usage:
  PYTHONPATH=. python scripts/audit_ready_types.py
  PYTHONPATH=. python scripts/audit_ready_types.py --only-prefix geo_
  PYTHONPATH=. python scripts/audit_ready_types.py --limit 20
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import question_engine.types  # noqa: F401
from question_engine.catalogs.algebra_1 import CATALOG as A1
from question_engine.catalogs.algebra_2 import CATALOG as A2
from question_engine.catalogs.calculus import CATALOG as CALC
from question_engine.catalogs.geometry import CATALOG as GEO
from question_engine.catalogs.grade_6 import CATALOG as G6
from question_engine.catalogs.pre_algebra import CATALOG as PA
from question_engine.catalogs.precalculus import CATALOG as PC
from question_engine.core.base import QUESTION_TYPES
from question_engine.settings.presets import apply_difficulty_presets
from question_engine.type_readiness import type_not_ready

TIERS = ("easy", "medium", "hard")
OUT = ROOT / "scripts" / "output" / "audit_ready_report.txt"


def ready_entries(prefix: str | None = None):
    catalog = A1 + G6 + PA + A2 + GEO + PC + CALC
    rows = [
        e
        for e in sorted(catalog, key=lambda x: (x.category, x.id))
        if e.generator != "scaffold" and not type_not_ready(e.id)
    ]
    if prefix:
        rows = [e for e in rows if e.id.startswith(prefix)]
    return rows


def looks_scaffolded(prompt: str) -> bool:
    return bool(re.search(r"\bscaffolded\b|placeholder|TODO|FIXME", prompt, re.I))


def audit_one(entry) -> list[str]:
    issues: list[str] = []
    qt = QUESTION_TYPES.get(entry.id)
    if qt is None:
        return ["not registered"]
    for tier in TIERS:
        settings = apply_difficulty_presets(
            {
                "count": 1,
                "difficulty_tier": tier,
                "include_answer_key": True,
                "include_diagram": True,
            },
            type_id=entry.id,
            setting_profile=getattr(qt, "setting_profile", None),
        )
        try:
            qs = qt.generate(settings)
        except Exception as exc:  # noqa: BLE001
            issues.append(f"{tier}: EXC {exc}")
            continue
        if not qs:
            issues.append(f"{tier}: empty")
            continue
        q = qs[0]
        if not (q.prompt_latex or q.prompt_text):
            issues.append(f"{tier}: blank prompt")
        if looks_scaffolded(q.prompt_latex or "") or looks_scaffolded(q.prompt_text or ""):
            issues.append(f"{tier}: scaffold-like prompt")
        if settings.get("include_answer_key") and not q.answer_latex:
            issues.append(f"{tier}: missing answer")
        # Soft diagram hint only for clearly figure-first geo/g6 visual ids.
        name = entry.id.lower()
        wants_fig = any(
            tok in name
            for tok in (
                "dot_plot",
                "histogram",
                "box_plot",
                "pythag",
                "parallelogram",
                "trapezoid",
                "right_triangle_trig",
                "geo_basics_angles",
                "geo_congruent_triangle",
                "geo_circles_circumference",
            )
        )
        if wants_fig and not (q.metadata or {}).get("diagram_svg"):
            if not (q.metadata or {}).get("graph_spec"):
                issues.append(f"{tier}: expected diagram_svg/graph_spec")
    return issues


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only-prefix", default=None)
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()
    entries = ready_entries(args.only_prefix)
    if args.limit:
        entries = entries[: args.limit]

    print(f"Auditing {len(entries)} Ready types…")
    bad: list[tuple[str, list[str]]] = []
    ok = 0
    for i, entry in enumerate(entries, 1):
        issues = audit_one(entry)
        if issues:
            bad.append((entry.id, issues))
        else:
            ok += 1
        if i % 40 == 0:
            print(f"  {i}/{len(entries)} (ok={ok}, bad={len(bad)})")

    lines = [
        f"Ready audited: {len(entries)}",
        f"OK: {ok}",
        f"Issues: {len(bad)}",
        "",
    ]
    for tid, issues in bad:
        lines.append(f"{tid}")
        for issue in issues:
            lines.append(f"  - {issue}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"OK={ok} issues={len(bad)}")
    print(f"Report: {OUT}")
    if bad:
        print("First issues:")
        for tid, issues in bad[:15]:
            print(f"  {tid}: {issues}")


if __name__ == "__main__":
    main()
