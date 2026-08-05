"""Build master G6 difficulty TRACKING.md / TRACKING.json from curriculum + batch files."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
import sys

sys.path.insert(0, str(ROOT))

from question_engine.catalogs.grade_6 import CATALOG  # noqa: E402
from question_engine.generators import GENERATORS  # noqa: E402
from question_engine.type_readiness import type_not_ready  # noqa: E402

OUT = ROOT / "scripts" / "output" / "topic_fit" / "g6_difficulty"
SKIP11 = [
    "g6_introduction_to_ratios",
    "g6_equivalent_ratios",
    "g6_part_part_whole_ratios",
    "g6_comparing_ratios",
    "g6_unit_rates_and_equivalent_rates",
    "g6_comparing_rates",
    "g6_converting_units",
    "g6_introduction_to_percents",
    "g6_relating_percents_fractions_and_decimals",
    "g6_finding_percents_with_equivalent_fractions",
    "g6_solving_percent_problems_with_formulas",
]
BATCH_RANGES = {
    0: (0, 10),
    1: (10, 20),
    2: (20, 30),
    3: (30, 40),
    4: (40, 50),
    5: (50, 60),
    6: (60, None),
}


def ready_g6_in_curriculum_order() -> list[dict]:
    text = (ROOT / "lib" / "curriculum.ts").read_text(encoding="utf-8")
    ids = re.findall(r'type_id:\s*"(g6_[^"]+)"', text)
    by_id = {e.id: e for e in CATALOG}
    ready = []
    for tid in ids:
        e = by_id.get(tid)
        if e is None or type_not_ready(tid):
            continue
        if getattr(e, "generator", None) == "scaffold":
            continue
        gen = e.generator or tid
        if tid not in GENERATORS and gen not in GENERATORS:
            continue
        ready.append({"type_id": tid, "name": e.name, "generator": gen})
    return ready


def load_batch_topics(batch: int) -> dict[str, dict] | None:
    path = OUT / f"batch_{batch}_verification.json"
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        topics = data
    elif isinstance(data, dict):
        topics = data.get("topics", data)
    else:
        return {}

    out: dict[str, dict] = {}
    if isinstance(topics, dict):
        for k, v in topics.items():
            if isinstance(v, dict) and ("status" in v or "mean_effort_by_D" in v or "means" in v):
                row = dict(v)
                row.setdefault("type_id", k)
                out[k] = row
        return out
    if not isinstance(topics, list):
        return {}
    for t in topics:
        if isinstance(t, dict) and "type_id" in t:
            out[t["type_id"]] = t
    return out


def topic_means(t: dict) -> dict | None:
    if t.get("mean_effort_by_D"):
        return t["mean_effort_by_D"]
    if t.get("means"):
        return t["means"]
    return None


def main() -> None:
    ready = ready_g6_in_curriculum_order()
    remaining = [t for t in ready if t["type_id"] not in SKIP11]
    batch_topics: dict[int, dict[str, dict] | None] = {
        b: load_batch_topics(b) for b in BATCH_RANGES
    }
    batch_file_status = {
        str(b): ("complete" if batch_topics[b] is not None else "in_progress")
        for b in BATCH_RANGES
    }

    entries = []
    needs_fix = []
    for i, t in enumerate(ready):
        tid = t["type_id"]
        if tid in SKIP11:
            entries.append(
                {
                    **t,
                    "curriculum_index": i,
                    "batch": "prior_11",
                    "status": "verified_ramp",
                    "source": "g6_difficulty_effort_specs.md",
                    "mean_effort_by_D": None,
                }
            )
            continue
        rem_i = next(j for j, r in enumerate(remaining) if r["type_id"] == tid)
        batch = next(
            b
            for b, (lo, hi) in BATCH_RANGES.items()
            if lo <= rem_i < (len(remaining) if hi is None else hi)
        )
        loaded = batch_topics[batch]
        if loaded is None:
            status = "in_progress"
            source = None
            means = None
        elif tid in loaded:
            row = loaded[tid]
            status = row.get("status", "pending")
            source = f"batch_{batch}_verification.json"
            means = topic_means(row)
            if status in {"weak_ramp", "failed_ramp", "blocked"}:
                needs_fix.append(
                    {
                        "type_id": tid,
                        "name": t["name"],
                        "batch": batch,
                        "status": status,
                        "notes": row.get("notes") or "",
                        "mean_effort_by_D": means,
                    }
                )
        else:
            status = "pending"
            source = f"batch_{batch}_verification.json"
            means = None
        entries.append(
            {
                **t,
                "curriculum_index": i,
                "remaining_index": rem_i,
                "batch": batch,
                "status": status,
                "source": source,
                "mean_effort_by_D": means,
            }
        )

    tracking = {
        "branch": "experiment/difficulty-slider",
        "date": "2026-07-27",
        "ready_count": len(ready),
        "remaining_after_skip11": len(remaining),
        "skip11": SKIP11,
        "batch_index_ranges_on_remaining": {
            str(k): {"lo": v[0], "hi": v[1]} for k, v in BATCH_RANGES.items()
        },
        "batch_file_status": batch_file_status,
        "needs_fix_later": needs_fix,
        "topics": entries,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "TRACKING.json").write_text(json.dumps(tracking, indent=2), encoding="utf-8")

    # Markdown
    lines = [
        "# G6 continuous-difficulty TRACKING",
        "",
        f"**Branch:** `{tracking['branch']}`  ",
        f"**Date:** {tracking['date']}  ",
        f"**Ready G6 topics:** {tracking['ready_count']}  ",
        f"**After SKIP first 11:** {tracking['remaining_after_skip11']} remaining → batches 0–6",
        "",
        "## Batch file status",
        "",
        "| Batch | Remaining indices | Verification file | Status |",
        "|---|---|---|---|",
    ]
    for b, (lo, hi) in BATCH_RANGES.items():
        end = "end" if hi is None else hi
        vf = f"`batch_{b}_verification.json`"
        lines.append(
            f"| {b} | [{lo}, {end}) | {vf} | {batch_file_status[str(b)]} |"
        )
    lines += [
        "",
        "## Prior pass (first 11 Ready)",
        "",
        "All marked **verified_ramp** from `g6_difficulty_effort_specs.md`.",
        "",
    ]
    for tid in SKIP11:
        lines.append(f"- `{tid}`")
    lines += [
        "",
        "## Needs fix later",
        "",
    ]
    if not needs_fix:
        lines.append("_None from batch files present so far (batch 6 has no weak/failed/blocked)._")
    else:
        lines.append("| type_id | batch | status | notes |")
        lines.append("|---|---|---|---|")
        for n in needs_fix:
            note = str(n.get("notes") or "").replace("|", "/").replace("\n", " ")[:80]
            lines.append(
                f"| `{n['type_id']}` | {n['batch']} | {n['status']} | {note} |"
            )
    lines += [
        "",
        "## All Ready topics (curriculum order)",
        "",
        "| # | type_id | batch | status |",
        "|---|---|---|---|",
    ]
    for e in entries:
        lines.append(
            f"| {e['curriculum_index']} | `{e['type_id']}` | {e['batch']} | {e['status']} |"
        )
    lines.append("")
    (OUT / "TRACKING.md").write_text("\n".join(lines), encoding="utf-8")
    print("batch_file_status", batch_file_status)
    print("needs_fix_later", len(needs_fix))
    for n in needs_fix:
        print(" ", n["status"], n["type_id"], "batch", n["batch"])
    print("Wrote", OUT / "TRACKING.json")
    print("Wrote", OUT / "TRACKING.md")


if __name__ == "__main__":
    main()
