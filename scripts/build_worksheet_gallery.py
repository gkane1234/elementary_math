"""Build example worksheet gallery snapshots + INDEX.

Reads ``config/worksheet-gallery.json``, generates progressive worksheets for each
entry (using worksheet-level difficulty → D ramp), and writes:

  scripts/output/worksheet_gallery/
    INDEX.md
    INDEX.json
    <id>.json
    <id>.html   (lightweight text preview)
  public/gallery/
    index.json
    snapshots/<id>.json

Usage:
  $env:PYTHONPATH='.'
  python scripts/build_worksheet_gallery.py
  python scripts/build_worksheet_gallery.py --ids g6-ratios-level-1,systems-intro-level-2
"""

from __future__ import annotations

import argparse
import html
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import question_engine.types  # noqa: F401
from question_engine.api.handler import handle_generate
from question_engine.worksheet_difficulty import worksheet_difficulty_to_ramp

CONFIG_PATH = ROOT / "config" / "worksheet-gallery.json"
OUT_DIR = ROOT / "scripts" / "output" / "worksheet_gallery"
PUBLIC_DIR = ROOT / "public" / "gallery"
PUBLIC_SNAP = PUBLIC_DIR / "snapshots"


def _load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def _prompt_preview(q: dict) -> str:
    text = (q.get("prompt_text") or q.get("prompt_latex") or "").strip()
    text = text.replace("\n", " ")
    return text[:120]


def _build_entry(entry: dict) -> dict:
    ramp = worksheet_difficulty_to_ramp(entry["worksheetDifficulty"])
    seeds = list(entry.get("seeds") or [])
    if not seeds:
        raise ValueError(f"Gallery entry {entry.get('id')!r} has no seeds")

    rng_seed = entry.get("seed")
    base_settings: dict = {}
    if rng_seed is not None:
        base_settings["seed"] = int(rng_seed)

    status, _, body = handle_generate(
        {
            "title": entry["title"],
            "progressive": {
                "seeds": seeds,
                "count": int(entry.get("count", 10)),
                "worksheet_difficulty": entry["worksheetDifficulty"],
                "include_related": bool(entry.get("includeRelated", True)),
                "max_topics": int(entry.get("maxTopics", 4)),
                "base_settings": base_settings,
            },
        }
    )
    data = json.loads(body)
    if status != 200:
        raise RuntimeError(
            f"Generate failed for {entry['id']}: status={status} error={data.get('error')}"
        )

    plan = data.get("progressive") or {}
    difficulties = plan.get("difficulties") or []
    topics = plan.get("topics") or []

    snapshot = {
        "id": entry["id"],
        "title": entry["title"],
        "description": entry.get("description", ""),
        "course": entry.get("course", ""),
        "lesson": entry.get("lesson", ""),
        "seeds": seeds,
        "worksheetDifficulty": entry["worksheetDifficulty"],
        "ramp": ramp,
        "count": int(entry.get("count", 10)),
        "seed": rng_seed,
        "includeRelated": bool(entry.get("includeRelated", True)),
        "maxTopics": int(entry.get("maxTopics", 4)),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "progressive": plan,
        "topics": topics,
        "difficulties": difficulties,
        "questions": data.get("questions") or [],
        "settings_snapshot": data.get("settings_snapshot"),
        "open_in_generator": {
            "mode": "progressive",
            "seed": seeds[0],
            "count": int(entry.get("count", 10)),
            "d_min": ramp["d_min"],
            "d_max": ramp["d_max"],
            "worksheetDifficulty": entry["worksheetDifficulty"],
        },
    }
    return snapshot


def _write_html_preview(snapshot: dict, path: Path) -> None:
    rows = []
    for i, q in enumerate(snapshot.get("questions") or []):
        d = None
        meta = q.get("metadata") or {}
        gs = meta.get("generation_settings") or {}
        d = gs.get("difficulty")
        if d is None and i < len(snapshot.get("difficulties") or []):
            d = snapshot["difficulties"][i]
        rows.append(
            "<tr>"
            f"<td>{i + 1}</td>"
            f"<td>{html.escape(str(q.get('topic', '')))}</td>"
            f"<td>{html.escape('' if d is None else str(d))}</td>"
            f"<td><code>{html.escape(_prompt_preview(q))}</code></td>"
            "</tr>"
        )
    ramp = snapshot.get("ramp") or {}
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>{html.escape(snapshot['title'])}</title>
<style>
body {{ font-family: Georgia, serif; margin: 2rem; color: #1f2937; }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid #d1d5db; padding: 0.4rem 0.6rem; text-align: left; vertical-align: top; }}
th {{ background: #f3f4f6; }}
.meta {{ color: #4b5563; margin-bottom: 1rem; }}
code {{ font-size: 0.9em; }}
</style>
</head>
<body>
<h1>{html.escape(snapshot['title'])}</h1>
<p class="meta">{html.escape(snapshot.get('course', ''))} · {html.escape(snapshot.get('lesson', ''))} ·
Worksheet difficulty: <strong>{html.escape(str(ramp.get('label', snapshot.get('worksheetDifficulty'))))}</strong>
(D {ramp.get('d_min')}→{ramp.get('d_max')}, {html.escape(str(ramp.get('schedule', '')))})</p>
<p>{html.escape(snapshot.get('description', ''))}</p>
<p class="meta">Topics: {html.escape(', '.join(snapshot.get('topics') or []))}</p>
<table>
<thead><tr><th>#</th><th>Topic</th><th>D</th><th>Prompt</th></tr></thead>
<tbody>
{''.join(rows)}
</tbody>
</table>
</body>
</html>
"""
    path.write_text(doc, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build worksheet gallery snapshots")
    parser.add_argument(
        "--ids",
        default="",
        help="Comma-separated entry ids to build (default: all)",
    )
    args = parser.parse_args()
    only = {s.strip() for s in args.ids.split(",") if s.strip()}

    config = _load_config()
    entries = list(config.get("entries") or [])
    if only:
        entries = [e for e in entries if e.get("id") in only]
        missing = only - {e.get("id") for e in entries}
        if missing:
            raise SystemExit(f"Unknown gallery ids: {sorted(missing)}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    PUBLIC_SNAP.mkdir(parents=True, exist_ok=True)

    built: list[dict] = []
    errors: list[str] = []

    for entry in entries:
        eid = entry["id"]
        print(f"Building {eid} …", flush=True)
        try:
            snapshot = _build_entry(entry)
        except Exception as exc:  # noqa: BLE001 — collect per-entry failures
            errors.append(f"{eid}: {exc}")
            print(f"  ERROR: {exc}", flush=True)
            continue

        diffs = snapshot.get("difficulties") or []
        monotone = all(diffs[i] <= diffs[i + 1] for i in range(len(diffs) - 1)) if diffs else True
        print(
            f"  ok n={len(snapshot['questions'])} topics={snapshot['topics']} "
            f"D={diffs} monotone={monotone}",
            flush=True,
        )

        (OUT_DIR / f"{eid}.json").write_text(
            json.dumps(snapshot, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        _write_html_preview(snapshot, OUT_DIR / f"{eid}.html")
        (PUBLIC_SNAP / f"{eid}.json").write_text(
            json.dumps(snapshot, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        built.append(
            {
                "id": eid,
                "title": snapshot["title"],
                "course": snapshot.get("course"),
                "lesson": snapshot.get("lesson"),
                "worksheetDifficulty": snapshot["worksheetDifficulty"],
                "ramp": snapshot["ramp"],
                "topics": snapshot["topics"],
                "difficulties": diffs,
                "count": len(snapshot["questions"]),
                "snapshot": f"snapshots/{eid}.json",
                "html": f"{eid}.html",
            }
        )

    index = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "difficulty_mapping": config.get("difficulty_mapping"),
        "entries": built,
        "errors": errors,
    }
    (OUT_DIR / "INDEX.json").write_text(json.dumps(index, indent=2), encoding="utf-8")
    (PUBLIC_DIR / "index.json").write_text(json.dumps(index, indent=2), encoding="utf-8")

    md_lines = [
        "# Worksheet gallery",
        "",
        f"Generated {index['generated_at']}",
        "",
        "## Difficulty mapping",
        "",
        "| Level | d_min | d_max | schedule |",
        "|-------|-------|-------|----------|",
        "| Level 0 | 0 | 3 | intro |",
        "| Level 1 | 0 | 8 | gentle |",
        "| Level 2 | 3 | 20 | moderate |",
        "| Level 3 | 8 | 25 | steep |",
        "| Level 4 | 20 | 25 | intense |",
        "",
        "Numeric worksheet D 0–24 interpolates between Level 0 and Level 4.",
        "",
        "## Entries",
        "",
        "| Id | Title | Course | Level | Topics | D ramp |",
        "|----|-------|--------|-------|--------|--------|",
    ]
    for row in built:
        ramp = row["ramp"]
        label = ramp.get("label", row["worksheetDifficulty"])
        md_lines.append(
            f"| `{row['id']}` | {row['title']} | {row['course']} | "
            f"{label} ({ramp['d_min']}→{ramp['d_max']}) | "
            f"{', '.join(row['topics'])} | {row['difficulties']} |"
        )
    if errors:
        md_lines.extend(["", "## Errors", ""])
        for err in errors:
            md_lines.append(f"- {err}")
    (OUT_DIR / "INDEX.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    print(f"\nWrote {len(built)} snapshots to {OUT_DIR}")
    if errors:
        raise SystemExit(f"{len(errors)} entries failed")


if __name__ == "__main__":
    main()
