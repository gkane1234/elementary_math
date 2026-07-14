"""Export a topic-fit sample pack for hand or agent review.

Usage:
  $env:PYTHONPATH='.'
  python scripts/topic_fit_sample.py --family poly_quad --tiers easy,medium,hard --n 3
  python scripts/topic_fit_sample.py --type-id quadratic_factoring --n 5
  python scripts/topic_fit_sample.py --prefix radical_ --n 2

Writes under scripts/output/topic_fit/<run_id>/:
  samples.jsonl  — one row per generated question
  gallery.md     — compact E/M/H prompts per type
  auto_flags.json — heuristic pre-flags (not a substitute for judgment)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import question_engine.types  # noqa: F401
from question_engine.core.base import QUESTION_TYPES
from question_engine.qa.topic_fit import (
    FAMILIES,
    evaluate_topic_fit,
    resolve_type_ids,
)
from question_engine.settings.presets import apply_difficulty_presets

OUT_ROOT = ROOT / "scripts" / "output" / "topic_fit"
DEFAULT_TIERS = ("easy", "medium", "hard")


def _meta_flags(meta: dict | None) -> dict:
    m = meta if isinstance(meta, dict) else {}
    return {
        "scaffolded": bool(m.get("scaffolded")),
        "has_graph": bool(m.get("graph_spec") or m.get("answer_graph_spec")),
        "has_diagram": bool(m.get("diagram_svg") or m.get("diagram_spec")),
        "has_number_line": bool(m.get("number_line_spec") or m.get("answer_number_line_spec")),
        "has_choices": bool(m.get("choices")),
    }


def generate_for_entry(entry, tiers: tuple[str, ...], n: int) -> list[dict]:
    qt = QUESTION_TYPES[entry.id]
    profile = getattr(qt, "setting_profile", None)
    rows: list[dict] = []
    for tier in tiers:
        for i in range(n):
            settings = apply_difficulty_presets(
                {
                    "count": 1,
                    "difficulty_tier": tier,
                    "include_answer_key": True,
                    "include_diagram": True,
                    "include_graph_metadata": True,
                },
                type_id=entry.id,
                setting_profile=profile,
            )
            row: dict = {
                "type_id": entry.id,
                "name": entry.name or entry.id,
                "generator": entry.generator,
                "tier": tier,
                "sample_index": i,
                "prompt_latex": "",
                "prompt_text": "",
                "instruction_latex": "",
                "answer_latex": "",
                "error": None,
                "metadata_flags": {},
            }
            try:
                qs = qt.generate(settings)
                if not qs:
                    row["error"] = "empty"
                    rows.append(row)
                    continue
                q = qs[0]
                meta = q.metadata if isinstance(q.metadata, dict) else {}
                row["prompt_latex"] = (q.prompt_latex or "").strip()
                row["prompt_text"] = (q.prompt_text or "").strip()
                row["instruction_latex"] = (meta.get("instruction_latex") or "").strip()
                # Included for incidental context only — not used by auto topic-fit flags.
                row["answer_latex"] = (q.answer_latex or "").strip()
                row["metadata_flags"] = _meta_flags(meta)
            except Exception as exc:  # noqa: BLE001
                row["error"] = str(exc)
            rows.append(row)
    return rows


def _clip(s: str, n: int = 180) -> str:
    s = re.sub(r"\s+", " ", s).strip() if s else ""
    return s if len(s) <= n else s[: n - 1] + "…"


def write_gallery(path: Path, rows: list[dict], flags: list[dict]) -> None:
    by_type: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_type[r["type_id"]].append(r)
    flag_by_id = {f["type_id"]: f for f in flags}

    lines = [
        "# Topic-fit sample gallery",
        "",
        "Review prompts for **topic / method / difficulty shape** — not answer correctness.",
        "",
    ]
    for tid, type_rows in by_type.items():
        name = type_rows[0].get("name") or tid
        gen = type_rows[0].get("generator") or ""
        fr = flag_by_id.get(tid, {})
        status = fr.get("status", "?")
        lines.append(f"## `{tid}` — {name}")
        lines.append("")
        lines.append(f"- generator: `{gen}`")
        lines.append(f"- auto status: **{status}**")
        if fr.get("hard_fails"):
            lines.append(f"- auto fails: {', '.join(fr['hard_fails'])}")
        if fr.get("notes"):
            lines.append(f"- auto notes: {', '.join(fr['notes'])}")
        lines.append("")
        for tier in ("easy", "medium", "hard"):
            tier_rows = [r for r in type_rows if r["tier"] == tier]
            if not tier_rows:
                continue
            lines.append(f"### {tier}")
            lines.append("")
            for r in tier_rows:
                if r.get("error"):
                    lines.append(f"- ERROR: {r['error']}")
                    continue
                prompt = r.get("prompt_latex") or r.get("prompt_text") or ""
                lines.append(f"- `{_clip(prompt)}`")
            lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Export topic-fit sample pack")
    parser.add_argument(
        "--family",
        choices=sorted(FAMILIES.keys()),
        help="Preset family of type_ids",
    )
    parser.add_argument(
        "--type-id",
        action="append",
        dest="type_ids",
        default=[],
        help="Type id (repeatable)",
    )
    parser.add_argument("--prefix", help="Include Ready types with this id prefix")
    parser.add_argument(
        "--tiers",
        default="easy,medium,hard",
        help="Comma-separated difficulty tiers (default: easy,medium,hard)",
    )
    parser.add_argument(
        "-n",
        "--n",
        type=int,
        default=3,
        dest="n",
        help="Samples per tier (default: 3)",
    )
    parser.add_argument(
        "--run-id",
        help="Output folder name under scripts/output/topic_fit/ (default: timestamp)",
    )
    parser.add_argument(
        "--include-not-ready",
        action="store_true",
        help="Do not require Ready filter when resolving --type-id / --family",
    )
    args = parser.parse_args()

    if not args.family and not args.type_ids and not args.prefix:
        parser.error("Provide --family, --type-id, and/or --prefix")

    tiers = tuple(t.strip() for t in args.tiers.split(",") if t.strip())
    if not tiers:
        parser.error("No tiers specified")

    try:
        entries = resolve_type_ids(
            family=args.family,
            type_ids=args.type_ids or None,
            prefix=args.prefix,
            ready_only=not args.include_not_ready,
        )
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 2

    if not entries:
        print("No matching types resolved.", file=sys.stderr)
        return 1

    run_id = args.run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    if args.family and not args.run_id:
        run_id = f"{args.family}_{run_id}"
    out_dir = OUT_ROOT / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    all_rows: list[dict] = []
    flags: list[dict] = []

    for entry in entries:
        rows = generate_for_entry(entry, tiers, args.n)
        all_rows.extend(rows)

        prompts_by_tier: dict[str, list[str]] = defaultdict(list)
        errors_by_tier: dict[str, list[str]] = defaultdict(list)
        scaffolded_by_tier: dict[str, list[bool]] = defaultdict(list)
        answers_by_tier: dict[str, list[str]] = defaultdict(list)
        for r in rows:
            tier = r["tier"]
            prompts_by_tier[tier].append(r.get("prompt_latex") or r.get("prompt_text") or "")
            errors_by_tier[tier].append(r.get("error") or "")
            scaffolded_by_tier[tier].append(bool(r.get("metadata_flags", {}).get("scaffolded")))
            answers_by_tier[tier].append(r.get("answer_latex") or "")

        result = evaluate_topic_fit(
            entry,
            dict(prompts_by_tier),
            errors_by_tier=dict(errors_by_tier),
            scaffolded_by_tier=dict(scaffolded_by_tier),
            answers_by_tier=dict(answers_by_tier),
        )
        flags.append(
            {
                "type_id": result.type_id,
                "name": result.name,
                "generator": result.generator,
                "status": result.status,
                "hard_fails": result.hard_fails,
                "notes": result.notes,
            }
        )

    samples_path = out_dir / "samples.jsonl"
    with samples_path.open("w", encoding="utf-8") as fh:
        for row in all_rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    flags_path = out_dir / "auto_flags.json"
    flags_path.write_text(
        json.dumps(
            {
                "run_id": run_id,
                "family": args.family,
                "tiers": list(tiers),
                "n_per_tier": args.n,
                "type_count": len(entries),
                "sample_count": len(all_rows),
                "results": flags,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    gallery_path = out_dir / "gallery.md"
    write_gallery(gallery_path, all_rows, flags)

    fail_n = sum(1 for f in flags if f["status"] == "FAIL")
    note_n = sum(1 for f in flags if f["status"] == "NOTE")
    pass_n = sum(1 for f in flags if f["status"] == "PASS")
    print(f"Wrote {out_dir}")
    print(f"  types={len(entries)} samples={len(all_rows)} PASS={pass_n} NOTE={note_n} FAIL={fail_n}")
    print(f"  {samples_path.name}  {gallery_path.name}  {flags_path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
