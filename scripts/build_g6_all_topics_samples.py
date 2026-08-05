"""Generate sample problems for every Ready Grade 6 topic.

Writes:
  scripts/output/topic_fit/g6_all_topics_samples.md
  scripts/output/topic_fit/g6_all_topics_samples.jsonl

Uses curriculum order from ``ready_g6_in_curriculum_order`` and the live
``_generate_for_type`` / preset path (same as the worksheet API).
"""

from __future__ import annotations

import json
import sys
import traceback
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FuturesTimeout
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import re

import question_engine.types  # noqa: F401
from question_engine.api.handler import _generate_for_type
from question_engine.catalogs.grade_6 import CATALOG
from question_engine.core.base import QUESTION_TYPES
from question_engine.generators import GENERATORS
from question_engine.type_readiness import type_not_ready

OUT_DIR = ROOT / "scripts" / "output" / "topic_fit"
MD_PATH = OUT_DIR / "g6_all_topics_samples.md"
JSONL_PATH = OUT_DIR / "g6_all_topics_samples.jsonl"

CONTINUOUS_D = (5.0, 15.0, 25.0)
EMH_TIERS = ("easy", "medium", "hard")
TIMEOUT_S = 45.0
CONTINUOUS_FIELD_TYPES = frozenset({"int", "float", "number", "range"})


def ready_g6_in_curriculum_order() -> list[dict]:
    """Same filter/order as scripts/build_g6_difficulty_tracking.py."""
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


def _has_continuous_difficulty(type_id: str) -> bool:
    qt = QUESTION_TYPES.get(type_id)
    if qt is None:
        return False
    try:
        fields = qt.settings_schema()
    except Exception:  # noqa: BLE001
        return False
    for field in fields:
        if getattr(field, "key", None) != "difficulty":
            continue
        return getattr(field, "type", None) in CONTINUOUS_FIELD_TYPES
    return False


def _one_question(type_id: str, settings: dict[str, Any]) -> dict[str, Any]:
    qs = _generate_for_type(type_id, settings)
    if not qs:
        raise RuntimeError("empty generation result")
    q = qs[0]
    meta = q.metadata if isinstance(q.metadata, dict) else {}
    return {
        "prompt_latex": (q.prompt_latex or "").strip(),
        "prompt_text": (q.prompt_text or "").strip(),
        "answer_latex": (q.answer_latex or "").strip(),
        "answer_text": (getattr(q, "answer_text", None) or "").strip(),
        "instruction_latex": (meta.get("instruction_latex") or "").strip(),
    }


def _generate_with_timeout(
    type_id: str, settings: dict[str, Any], timeout: float
) -> tuple[dict[str, Any] | None, str | None]:
    with ThreadPoolExecutor(max_workers=1) as pool:
        fut = pool.submit(_one_question, type_id, settings)
        try:
            return fut.result(timeout=timeout), None
        except FuturesTimeout:
            return None, f"timeout after {timeout:g}s"
        except Exception as exc:  # noqa: BLE001
            return None, f"{type(exc).__name__}: {exc}"


def sample_topic(topic: dict[str, str], index: int) -> dict[str, Any]:
    tid = topic["type_id"]
    name = topic["name"]
    continuous = _has_continuous_difficulty(tid)
    samples: list[dict[str, Any]] = []
    topic_error: str | None = None

    if tid not in QUESTION_TYPES:
        return {
            "curriculum_index": index,
            "type_id": tid,
            "name": name,
            "generator": topic.get("generator"),
            "difficulty_mode": "error",
            "samples": [],
            "error": f"type_id not in QUESTION_TYPES",
        }

    if continuous:
        mode = "continuous"
        levels: list[tuple[str, dict[str, Any]]] = [
            (
                f"D={int(d) if d == int(d) else d}",
                {
                    "count": 1,
                    "difficulty": float(d),
                    "include_answer_key": True,
                    "include_diagram": True,
                    "include_graph_metadata": True,
                    "seed": 4200 + int(d) * 17 + (hash(tid) % 97) + index,
                },
            )
            for d in CONTINUOUS_D
        ]
    else:
        mode = "tier"
        levels = [
            (
                tier,
                {
                    "count": 1,
                    "difficulty_tier": tier,
                    "include_answer_key": True,
                    "include_diagram": True,
                    "include_graph_metadata": True,
                    "seed": 4200 + i * 31 + (hash(tid) % 97) + index,
                },
            )
            for i, tier in enumerate(EMH_TIERS)
        ]

    for label, settings in levels:
        row: dict[str, Any] = {
            "difficulty_label": label,
            "settings": {k: v for k, v in settings.items() if k != "count"},
            "prompt_latex": "",
            "prompt_text": "",
            "answer_latex": "",
            "answer_text": "",
            "instruction_latex": "",
            "error": None,
        }
        q, err = _generate_with_timeout(tid, settings, TIMEOUT_S)
        if err:
            row["error"] = err
        elif q is None:
            row["error"] = "no result"
        else:
            row.update(q)
        samples.append(row)

    if all(s.get("error") for s in samples):
        topic_error = "; ".join(
            f"{s['difficulty_label']}: {s['error']}" for s in samples
        )

    return {
        "curriculum_index": index,
        "type_id": tid,
        "name": name,
        "generator": topic.get("generator"),
        "difficulty_mode": mode,
        "samples": samples,
        "error": topic_error,
    }


def _md_escape_fence(s: str) -> str:
    # Avoid breaking fenced blocks if prompt contains ``` 
    return (s or "").replace("```", "'''")


def write_markdown(topics: list[dict[str, Any]], path: Path) -> None:
    n = len(topics)
    n_fail = sum(1 for t in topics if t.get("error") or not t.get("samples"))
    n_sample_fail = sum(
        1 for t in topics for s in t.get("samples", []) if s.get("error")
    )
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Grade 6 Ready topics — sample problems",
        "",
        f"Generated {stamp} on branch with G6 continuous-difficulty work.",
        "",
        f"**Topics:** {n} Ready G6 type_ids in curriculum order "
        f"(from `lib/curriculum.ts` + catalog readiness).",
        "",
        "For each topic: **3 samples** at continuous **D=5, 15, 25** when the "
        "type exposes numeric `difficulty`, otherwise **easy / medium / hard** "
        "via `difficulty_tier`. Generation uses the live `_generate_for_type` "
        "path (presets applied).",
        "",
        f"**Topic-level failures:** {n_fail}  ",
        f"**Sample-level failures:** {n_sample_fail}",
        "",
        "---",
        "",
    ]

    for t in topics:
        idx = t["curriculum_index"] + 1
        tid = t["type_id"]
        name = t["name"]
        mode = t.get("difficulty_mode", "?")
        lines.append(f"## {idx}. `{tid}` — {name}")
        lines.append("")
        lines.append(f"*Difficulty mode:* `{mode}`  ")
        if t.get("generator"):
            lines.append(f"*Generator:* `{t['generator']}`")
        lines.append("")

        if t.get("error") and not t.get("samples"):
            lines.append(f"**Error:** {t['error']}")
            lines.append("")
            continue

        for s in t.get("samples", []):
            label = s["difficulty_label"]
            lines.append(f"### {label}")
            lines.append("")
            if s.get("error"):
                lines.append(f"**Generation error:** {s['error']}")
                lines.append("")
                continue
            prompt = s.get("prompt_latex") or s.get("prompt_text") or "(empty prompt)"
            lines.append("**Prompt:**")
            lines.append("")
            lines.append("```")
            lines.append(_md_escape_fence(prompt))
            lines.append("```")
            lines.append("")
            ans = s.get("answer_latex") or s.get("answer_text") or ""
            if ans:
                lines.append("**Answer:**")
                lines.append("")
                lines.append("```")
                lines.append(_md_escape_fence(ans))
                lines.append("```")
                lines.append("")
            else:
                lines.append("*Answer:* _(none)_")
                lines.append("")

        if t.get("error"):
            lines.append(f"**Note:** all samples failed — {t['error']}")
            lines.append("")

        lines.append("---")
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def write_jsonl(topics: list[dict[str, Any]], path: Path) -> None:
    with path.open("w", encoding="utf-8") as f:
        for t in topics:
            for s in t.get("samples", []) or [
                {
                    "difficulty_label": "n/a",
                    "error": t.get("error") or "no samples",
                    "prompt_latex": "",
                    "prompt_text": "",
                    "answer_latex": "",
                    "answer_text": "",
                }
            ]:
                row = {
                    "curriculum_index": t["curriculum_index"],
                    "type_id": t["type_id"],
                    "name": t["name"],
                    "generator": t.get("generator"),
                    "difficulty_mode": t.get("difficulty_mode"),
                    "difficulty_label": s.get("difficulty_label"),
                    "prompt_latex": s.get("prompt_latex", ""),
                    "prompt_text": s.get("prompt_text", ""),
                    "answer_latex": s.get("answer_latex", ""),
                    "answer_text": s.get("answer_text", ""),
                    "error": s.get("error") or (
                        t.get("error") if not t.get("samples") else None
                    ),
                }
                f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ready = ready_g6_in_curriculum_order()
    print(f"Ready G6 topics: {len(ready)}", flush=True)

    results: list[dict[str, Any]] = []
    failures: list[str] = []

    for i, topic in enumerate(ready):
        tid = topic["type_id"]
        print(f"[{i + 1}/{len(ready)}] {tid} ...", flush=True)
        try:
            row = sample_topic(topic, i)
        except Exception as exc:  # noqa: BLE001
            row = {
                "curriculum_index": i,
                "type_id": tid,
                "name": topic["name"],
                "generator": topic.get("generator"),
                "difficulty_mode": "error",
                "samples": [],
                "error": f"{type(exc).__name__}: {exc}\n{traceback.format_exc()}",
            }
        results.append(row)
        sample_errs = [s for s in row.get("samples", []) if s.get("error")]
        if row.get("error") or sample_errs:
            failures.append(tid)
            detail = row.get("error") or "; ".join(
                f"{s['difficulty_label']}: {s['error']}" for s in sample_errs
            )
            print(f"  FAIL: {detail[:200]}", flush=True)
        else:
            print("  ok", flush=True)

    write_markdown(results, MD_PATH)
    write_jsonl(results, JSONL_PATH)

    print(f"\nWrote {MD_PATH}")
    print(f"Wrote {JSONL_PATH}")
    print(f"Topics: {len(results)}")
    print(f"Topics with any failure: {len(failures)}")
    if failures:
        print("Failures:", ", ".join(failures))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
