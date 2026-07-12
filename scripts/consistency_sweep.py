"""Consistency / consolidation sweep across Ready catalog types.

Reports:
- generators used by many types (canonical skills)
- missing generator_profiles
- suspicious instruction defaults (\"Solve.\" on non-solve topics)
- denylist mismatches (demoted but diagram_svg works / Ready but no figure when promised)
- duplicate catalog ids with conflicting generators

Does not write the PDF.
"""

from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import question_engine.types  # noqa: F401
from question_engine.core.base import QUESTION_TYPES
from question_engine.core.registry import TYPE_CATALOG, get_catalog_entry
from question_engine.diagram_readiness import REQUIRES_DIAGRAM_TYPE_IDS
from question_engine.generators import GENERATORS
from question_engine.settings.generator_profiles import config_for_generator
from question_engine.settings.presets import apply_difficulty_presets, lookup_difficulty_preset
from question_engine.type_readiness import INCORRECT_IMPLEMENTATION_TYPE_IDS, type_not_ready

OUT = ROOT / "scripts" / "output" / "consistency_sweep_report.txt"


def unique_entries():
    by: dict[str, object] = {}
    for e in TYPE_CATALOG:
        by[e.id] = e
    return by


def main() -> None:
    by = unique_entries()
    lines: list[str] = []
    ready = [
        e
        for e in by.values()
        if e.generator != "scaffold" and not type_not_ready(e.id)  # type: ignore[attr-defined]
    ]

    lines.append(f"Unique catalog ids: {len(by)}")
    lines.append(f"Ready: {len(ready)}")
    lines.append(f"Registered QUESTION_TYPES: {len(QUESTION_TYPES)}")
    lines.append(f"GENERATORS keys: {len(GENERATORS)}")
    lines.append("")

    # Duplicate ids with conflicting generators in TYPE_CATALOG
    gens_by_id: dict[str, set[str]] = defaultdict(set)
    for e in TYPE_CATALOG:
        gens_by_id[e.id].add(e.generator)
    conflicts = {tid: gens for tid, gens in gens_by_id.items() if len(gens) > 1}
    lines.append(f"## Conflicting catalog generators ({len(conflicts)})")
    for tid, gens in sorted(conflicts.items()):
        lines.append(f"  {tid}: {sorted(gens)}")
    lines.append("")

    # Missing profiles
    missing_profiles = sorted(
        {
            e.generator
            for e in ready
            if e.generator in GENERATORS and config_for_generator(e.generator) is None
        }
    )
    lines.append(f"## Ready generators missing TypeSettingConfig ({len(missing_profiles)})")
    for g in missing_profiles[:80]:
        lines.append(f"  {g}")
    lines.append("")

    # Suspicious instructions
    suspicious_instr: list[str] = []
    for e in ready:
        text = (e.instruction_text or "").strip().lower()
        name = e.name.lower()
        if text in {"solve.", "solve"} and not any(
            tok in name for tok in ("equation", "solve", "inequality", "system")
        ):
            suspicious_instr.append(f"{e.id}: instruction={e.instruction_text!r} name={e.name}")
    lines.append(f"## Suspicious Solve. instructions ({len(suspicious_instr)})")
    for row in suspicious_instr[:40]:
        lines.append(f"  {row}")
    lines.append("")

    # Denylist vs sample diagram emission
    demote_but_works: list[str] = []
    ready_but_missing_fig: list[str] = []
    for tid in sorted(REQUIRES_DIAGRAM_TYPE_IDS):
        e = by.get(tid)
        if e is None or e.generator == "scaffold" or e.generator not in GENERATORS:
            continue
        qt = QUESTION_TYPES.get(tid)
        if qt is None:
            continue
        try:
            qs = qt.generate(
                {
                    "count": 1,
                    "include_answer_key": True,
                    "include_diagram": True,
                    "difficulty_tier": "medium",
                }
            )
            meta = qs[0].metadata or {}
            if meta.get("diagram_svg") or meta.get("graph_spec"):
                demote_but_works.append(tid)
        except Exception:
            pass
    # Spot-check a few Ready figure-ish types
    for e in ready:
        if not any(
            tok in e.id
            for tok in (
                "geo_basics_angles",
                "geo_right_pythagorean",
                "g6_interpreting_dot",
                "finding_sine",
            )
        ):
            continue
        qt = QUESTION_TYPES.get(e.id)
        if not qt:
            continue
        qs = qt.generate({"count": 1, "include_diagram": True, "include_answer_key": True})
        meta = qs[0].metadata or {}
        if not (meta.get("diagram_svg") or meta.get("graph_spec") or meta.get("number_line_spec")):
            ready_but_missing_fig.append(e.id)

    lines.append(f"## Demoted but emits diagram/graph ({len(demote_but_works)})")
    for tid in demote_but_works:
        lines.append(f"  {tid}")
    lines.append("")
    lines.append(f"## Ready figure types missing metadata ({len(ready_but_missing_fig)})")
    for tid in ready_but_missing_fig:
        lines.append(f"  {tid}")
    lines.append("")

    # Popular generators (consolidation candidates)
    gen_counts = Counter(e.generator for e in ready)
    lines.append("## Top generators by Ready type count")
    for gen, n in gen_counts.most_common(25):
        lines.append(f"  {n:3d}  {gen}")
    lines.append("")

    # Profiles without difficulty presets
    missing_presets: list[str] = []
    for e in ready:
        cfg = config_for_generator(e.generator)
        profile = cfg.setting_profile if cfg else None
        if not profile:
            continue
        if lookup_difficulty_preset("medium", setting_profile=profile) is None:
            missing_presets.append(f"{e.id} profile={profile}")
    lines.append(f"## Ready types whose profile lacks difficulty presets ({len(set(missing_presets))})")
    for row in sorted(set(missing_presets))[:40]:
        lines.append(f"  {row}")
    lines.append("")

    lines.append(f"## INCORRECT_IMPLEMENTATION size: {len(INCORRECT_IMPLEMENTATION_TYPE_IDS)}")
    lines.append(f"## REQUIRES_DIAGRAM size: {len(REQUIRES_DIAGRAM_TYPE_IDS)}")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines[:80]))
    print(f"\nFull report: {OUT}")


if __name__ == "__main__":
    main()
