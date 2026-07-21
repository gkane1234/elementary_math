"""Difficulty-slider sweep gallery for continuous-difficulty Ready types only.

Includes Ready (non-scaffold) catalog types whose settings schema exposes a
numeric continuous ``difficulty`` field (int/float/range) — the same signal the
worksheet UI uses for the difficulty slider. Excludes discrete EMH-only types,
select-style difficulty, stubs, and types that ignore continuous D.

Samples 5 questions at each of D ∈ {0, 5, 10, 15, 20, 25, 50} via the same
settings path the worksheet generate API uses.

Writes under scripts/output/topic_fit/difficulty_sweep/:
  INDEX.md          — short markdown index + regenerate instructions
  index.html        — browsable TOC + summary
  gallery.html      — full KaTeX gallery (all courses)
  by_course/*.html  — per-course slices
  samples.jsonl     — full prompts/answers (untruncated)
  summary.json      — counts + failed/skipped + include/exclude
  failed.jsonl      — per-(type, D) failures
  excluded.jsonl    — Ready types excluded (not continuous difficulty)

Usage:
  $env:PYTHONPATH='.'
  python scripts/build_difficulty_sweep_gallery.py
  python scripts/build_difficulty_sweep_gallery.py --limit 20   # smoke
  python scripts/build_difficulty_sweep_gallery.py --timeout 30
"""

from __future__ import annotations

import argparse
import html
import json
import sys
import time
import traceback
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import question_engine.types  # noqa: F401
from question_engine.api.handler import _resolve_generation_settings
from question_engine.catalogs.algebra_1 import CATALOG as A1
from question_engine.catalogs.algebra_2 import CATALOG as A2
from question_engine.catalogs.calculus import CATALOG as CALC
from question_engine.catalogs.geometry import CATALOG as GEO
from question_engine.catalogs.grade_6 import CATALOG as G6
from question_engine.catalogs.pre_algebra import CATALOG as PA
from question_engine.catalogs.precalculus import CATALOG as PC
from question_engine.core.base import QUESTION_TYPES
from question_engine.type_readiness import type_not_ready

OUT = ROOT / "scripts" / "output" / "topic_fit" / "difficulty_sweep"
DIFFICULTIES = (0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 50.0)
N_PER = 5
DISPLAY_TRUNCATE = 420  # chars of latex shown in HTML; full kept in jsonl

COURSE_CATALOGS: list[tuple[str, list]] = [
    ("grade_6", G6),
    ("pre_algebra", PA),
    ("algebra_1", A1),
    ("algebra_2", A2),
    ("geometry", GEO),
    ("precalculus", PC),
    ("calculus", CALC),
]

HINT_KEYS = (
    "n_ops",
    "n_terms",
    "n_parens",
    "nest_depth",
    "n_groups",
    "n_lone",
    "shape",
    "steps",
    "form",
    "mode",
    "method",
    "spend",
    "upgrades",
    "primitive_engine",
    "expression_policy",
    "op_pool",
    "nested",
    "flipped",
)

CONTINUOUS_DIFFICULTY_FIELD_TYPES = frozenset({"int", "float", "number", "range"})


def _continuous_difficulty_field(type_id: str):
    """Return the numeric continuous ``difficulty`` SettingField, or None."""
    qt = QUESTION_TYPES.get(type_id)
    if qt is None:
        return None
    try:
        fields = qt.settings_schema()
    except Exception:  # noqa: BLE001
        return None
    for field in fields:
        if getattr(field, "key", None) != "difficulty":
            continue
        if getattr(field, "type", None) in CONTINUOUS_DIFFICULTY_FIELD_TYPES:
            return field
        return None  # e.g. select easy/medium/hard — discrete only
    return None


def _has_continuous_difficulty(type_id: str) -> bool:
    return _continuous_difficulty_field(type_id) is not None


def _ready_entries(
    limit: int = 0,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Return (continuous-difficulty entries, excluded Ready entries)."""
    rows: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []
    seen: set[str] = set()
    for course, catalog in COURSE_CATALOGS:
        for entry in catalog:
            if entry.id in seen:
                continue
            seen.add(entry.id)
            if entry.generator == "scaffold":
                continue
            if type_not_ready(entry.id):
                continue
            if entry.id not in QUESTION_TYPES:
                continue
            base = {
                "type_id": entry.id,
                "name": entry.name or entry.id,
                "generator": entry.generator,
                "category": entry.category,
                "course": course,
                "setting_profile": getattr(
                    QUESTION_TYPES[entry.id], "setting_profile", None
                ),
            }
            if not _has_continuous_difficulty(entry.id):
                # Classify why excluded for the index.
                qt = QUESTION_TYPES[entry.id]
                try:
                    fields = qt.settings_schema()
                except Exception as exc:  # noqa: BLE001
                    reason = f"settings_schema error: {exc}"
                else:
                    keys = {f.key: f for f in fields}
                    if "difficulty" in keys:
                        reason = (
                            f"discrete difficulty field "
                            f"(type={keys['difficulty'].type})"
                        )
                    elif "difficulty_tier" in keys:
                        reason = "difficulty_tier only (easy/medium/hard)"
                    else:
                        reason = "no difficulty / difficulty_tier field"
                excluded.append({**base, "exclude_reason": reason})
                continue
            rows.append(base)
    rows.sort(key=lambda r: (r["course"], r["category"], r["type_id"]))
    excluded.sort(key=lambda r: (r["course"], r["type_id"]))
    if limit:
        rows = rows[:limit]
    return rows, excluded


def _hints(meta: dict[str, Any] | None) -> dict[str, Any]:
    m = meta if isinstance(meta, dict) else {}
    out: dict[str, Any] = {}
    for key in HINT_KEYS:
        if key in m and m[key] is not None:
            out[key] = m[key]
    return out


def _generate_batch(type_id: str, difficulty: float, n: int) -> list[dict[str, Any]]:
    qt = QUESTION_TYPES[type_id]
    settings = _resolve_generation_settings(
        type_id,
        {
            "count": n,
            "difficulty": float(difficulty),
            "include_answer_key": True,
            "include_diagram": True,
            "include_graph_metadata": True,
        },
    )
    qs = qt.generate(settings)
    rows: list[dict[str, Any]] = []
    for i, q in enumerate(qs):
        meta = q.metadata if isinstance(q.metadata, dict) else {}
        rows.append(
            {
                "type_id": type_id,
                "difficulty": float(difficulty),
                "sample_index": i,
                "prompt_latex": (q.prompt_latex or "").strip(),
                "prompt_text": (q.prompt_text or "").strip(),
                "answer_latex": (q.answer_latex or "").strip(),
                "instruction_latex": (
                    meta.get("instruction_latex")
                    or getattr(qt, "instruction_latex", "")
                    or ""
                ).strip(),
                "hints": _hints(meta),
            }
        )
    return rows


def _generate_batch_with_timeout(
    type_id: str, difficulty: float, n: int, timeout: float
) -> tuple[list[dict[str, Any]] | None, str | None]:
    with ThreadPoolExecutor(max_workers=1) as pool:
        fut = pool.submit(_generate_batch, type_id, difficulty, n)
        try:
            return fut.result(timeout=timeout), None
        except FuturesTimeout:
            return None, f"timeout after {timeout:g}s"
        except Exception as exc:  # noqa: BLE001
            return None, f"{type(exc).__name__}: {exc}"


def _clip(s: str, n: int = DISPLAY_TRUNCATE) -> str:
    s = (s or "").replace("\n", " ").strip()
    if len(s) <= n:
        return s
    return s[: n - 1] + "…"


def _esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def _katex_head(title: str) -> list[str]:
    return [
        "<!DOCTYPE html>",
        '<html lang="en"><head><meta charset="utf-8"/>',
        f"<title>{_esc(title)}</title>",
        "<style>",
        """
    :root { color-scheme: light; }
    body { font-family: Georgia, "Times New Roman", serif; margin: 1.25rem 1.5rem 3rem;
           line-height: 1.45; color: #1a1a1a; background: #faf9f7; }
    h1 { font-size: 1.65rem; margin-bottom: 0.2rem; }
    h2 { margin-top: 1.75rem; border-bottom: 1px solid #ccc; padding-bottom: 0.2rem; }
    h3 { margin-top: 1.1rem; font-size: 1.05rem; }
    .lede { max-width: 56rem; color: #444; }
    .code { font-family: ui-monospace, Consolas, monospace; font-size: 0.82em; }
    .meta { color: #555; font-size: 0.9rem; margin: 0.2rem 0 0.6rem; }
    .pill { display: inline-block; background: #eef2f7; border: 1px solid #c5d0de;
            border-radius: 3px; padding: 0.05rem 0.35rem; margin: 0.08rem; font-size: 0.78rem; }
    .pill.fail { background: #fde8e8; border-color: #e8b0b0; }
    .pill.ok { background: #e6f4ea; border-color: #b7dfc3; }
    .pill.warn { background: #fff4d6; border-color: #e6d39a; }
    table.compare { border-collapse: collapse; width: 100%; font-size: 0.86rem; margin: 0.4rem 0 1.2rem; }
    table.compare th, table.compare td { border: 1px solid #ccc; padding: 0.35rem 0.45rem; vertical-align: top; }
    table.compare th { background: #e8e6e1; position: sticky; top: 0; }
    .samples { font-family: "Cambria Math", "Times New Roman", serif; font-size: 0.98rem; }
    .ans { color: #255; }
    .toc a { margin-right: 0.65rem; white-space: nowrap; }
    .nav { margin: 0.75rem 0 1.25rem; }
    .nav a { margin-right: 0.85rem; }
    .truncated { color: #888; font-size: 0.8rem; }
    .type-block { scroll-margin-top: 0.75rem; }
        """,
        "</style>",
        '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css"/>',
        '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>',
        (
            '<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js" '
            "onload=\"renderMathInElement(document.body,{delimiters:["
            "{left:'$',right:'$',display:false},{left:'$$',right:'$$',display:true}],"
            "throwOnError:false})\"></script>"
        ),
        "</head><body>",
    ]


def _hints_html(hints: dict[str, Any]) -> str:
    if not hints:
        return "—"
    bits = []
    for k, v in hints.items():
        if isinstance(v, (dict, list)):
            text = json.dumps(v, separators=(",", ":"))
            if len(text) > 80:
                text = text[:79] + "…"
        else:
            text = str(v)
        bits.append(f'<span class="pill code">{_esc(k)}={_esc(text)}</span>')
    return " ".join(bits)


def _sample_cell(rows: list[dict[str, Any]]) -> str:
    parts = []
    for r in rows:
        pl_full = r.get("prompt_latex") or r.get("prompt_text") or ""
        al_full = r.get("answer_latex") or ""
        pl = _clip(pl_full)
        al = _clip(al_full, 200)
        trunc = ""
        if len(pl_full) > DISPLAY_TRUNCATE or len(al_full) > 200:
            trunc = ' <span class="truncated">(truncated; full in samples.jsonl)</span>'
        ans = (
            f' <span class="ans">→ ${_esc(al)}$</span>' if al else ""
        )
        if pl:
            parts.append(f'<div class="samples">${_esc(pl)}${ans}{trunc}</div>')
        else:
            parts.append(
                f'<div class="samples"><em>empty prompt</em>{ans}{trunc}</div>'
            )
    return "".join(parts) or "—"


def _build_course_html(
    title: str,
    lede: str,
    entries: list[dict[str, Any]],
    samples_by_type: dict[str, list[dict[str, Any]]],
    fails_by_type: dict[str, list[dict[str, Any]]],
    *,
    nav_extra: str = "",
) -> str:
    parts = _katex_head(title)
    parts.append(f"<h1>{_esc(title)}</h1>")
    parts.append(f'<p class="lede">{lede}</p>')
    if nav_extra:
        parts.append(f'<p class="nav">{nav_extra}</p>')

    parts.append('<p class="toc"><strong>Jump:</strong> ')
    for e in entries:
        tid = e["type_id"]
        ok = tid in samples_by_type and tid not in fails_by_type
        cls = "ok" if ok and tid not in fails_by_type else ("warn" if tid in samples_by_type else "fail")
        if tid in fails_by_type and tid in samples_by_type:
            cls = "warn"
        elif tid in fails_by_type:
            cls = "fail"
        parts.append(
            f'<a class="pill {cls}" href="#t-{_esc(tid)}">{_esc(tid)}</a> '
        )
    parts.append("</p>")

    for e in entries:
        tid = e["type_id"]
        parts.append(f'<div class="type-block" id="t-{_esc(tid)}">')
        parts.append(f"<h2><span class=\"code\">{_esc(tid)}</span></h2>")
        parts.append(
            f'<p class="meta">{_esc(e.get("name") or "")} · generator='
            f'<span class="code">{_esc(e.get("generator") or "")}</span> · '
            f'{_esc(e.get("category") or "")}</p>'
        )
        fails = fails_by_type.get(tid) or []
        if fails:
            for f in fails:
                parts.append(
                    f'<p><span class="pill fail">D={f["difficulty"]:g} FAILED</span> '
                    f'{_esc(f.get("error") or "")}</p>'
                )
        rows = samples_by_type.get(tid) or []
        if not rows and not fails:
            parts.append('<p><span class="pill fail">no samples</span></p>')
            parts.append("</div>")
            continue
        if rows:
            by_d: dict[float, list[dict]] = defaultdict(list)
            for r in rows:
                by_d[float(r["difficulty"])].append(r)
            parts.append(
                '<table class="compare"><thead><tr>'
                "<th>D</th><th>Hints</th><th>Samples (prompt → answer)</th>"
                "</tr></thead><tbody>"
            )
            for d in DIFFICULTIES:
                at = by_d.get(float(d), [])
                if not at:
                    fail_msg = next(
                        (f.get("error") for f in fails if float(f["difficulty"]) == float(d)),
                        "missing",
                    )
                    parts.append(
                        f'<tr><td>{d:g}</td><td>—</td>'
                        f'<td><span class="pill fail">{_esc(str(fail_msg))}</span></td></tr>'
                    )
                    continue
                hints = at[0].get("hints") or {}
                parts.append(
                    f"<tr><td>{d:g}</td><td>{_hints_html(hints)}</td>"
                    f"<td>{_sample_cell(at)}</td></tr>"
                )
            parts.append("</tbody></table>")
        parts.append("</div>")

    parts.append("</body></html>")
    return "\n".join(parts)


def _write_index_md(
    path: Path,
    *,
    generated: str,
    n_included: int,
    n_excluded: int,
    n_unique_generators: int,
    n_ok: int,
    n_partial: int,
    n_failed: int,
    n_skipped: int,
    skipped: list[dict[str, Any]],
    explode_notes: list[str],
    elapsed_s: float,
    exclude_reason_counts: dict[str, int],
) -> None:
    lines = [
        "# Difficulty sweep gallery (continuous difficulty only)",
        "",
        f"Generated: `{generated}`",
        "",
        "Five samples at each difficulty **0, 5, 10, 15, 20, 25, 50** for Ready "
        "catalog types that expose a **continuous numeric `difficulty`** setting "
        "(int/float/range) — the same field that drives the worksheet difficulty slider.",
        "",
        "Excluded: Ready types with only `difficulty_tier` (easy/medium/hard), "
        "select-style discrete `difficulty`, missing difficulty fields, scaffolds, "
        "or not-ready demotions.",
        "",
        "## Open",
        "",
        "- [index.html](index.html) — TOC + summary",
        "- [gallery.html](gallery.html) — full KaTeX gallery",
        "- [by_course/](by_course/) — per-course HTML slices",
        "- [samples.jsonl](samples.jsonl) — full (untruncated) prompts/answers",
        "- [summary.json](summary.json) — machine-readable counts",
        "- [failed.jsonl](failed.jsonl) — failures",
        "- [excluded.jsonl](excluded.jsonl) — Ready types excluded (not continuous)",
        "",
        "## Counts",
        "",
        f"| Continuous-difficulty types included | {n_included} |",
        f"| Unique generators among included | {n_unique_generators} |",
        f"| Ready types excluded (no continuous D) | {n_excluded} |",
        f"| Fully succeeded (all D) | {n_ok} |",
        f"| Partial (some D failed) | {n_partial} |",
        f"| Fully failed | {n_failed} |",
        f"| Skipped before generate | {n_skipped} |",
        f"| Elapsed | {elapsed_s:.1f}s |",
        "",
        "### Exclude reasons",
        "",
    ]
    for reason, count in sorted(exclude_reason_counts.items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"- {reason}: **{count}**")
    lines.extend(
        [
            "",
            "## Regenerate",
            "",
            "```powershell",
            "$env:PYTHONPATH='.'",
            "python scripts/build_difficulty_sweep_gallery.py",
            "# optional: python scripts/build_difficulty_sweep_gallery.py --timeout 45 --limit 0",
            "```",
            "",
        ]
    )
    if explode_notes:
        lines.extend(["## High-D notes", ""])
        for note in explode_notes:
            lines.append(f"- {note}")
        lines.append("")
    if skipped:
        lines.extend(["## Skipped", ""])
        for s in skipped:
            lines.append(f"- `{s.get('type_id')}`: {s.get('reason')}")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0, help="Limit types (smoke test)")
    parser.add_argument(
        "--timeout",
        type=float,
        default=45.0,
        help="Per (type, difficulty) generate timeout in seconds",
    )
    parser.add_argument(
        "--n",
        type=int,
        default=N_PER,
        help="Samples per difficulty (default 5)",
    )
    args = parser.parse_args()

    entries, excluded = _ready_entries(args.limit)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "by_course").mkdir(parents=True, exist_ok=True)

    samples: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    t0 = time.time()
    generated = datetime.now(timezone.utc).isoformat()
    n_unique_generators = len({e["generator"] for e in entries})
    exclude_reason_counts: dict[str, int] = defaultdict(int)
    for row in excluded:
        exclude_reason_counts[row.get("exclude_reason") or "unknown"] += 1

    print(
        f"Continuous-difficulty types: {len(entries)} included, "
        f"{len(excluded)} Ready excluded × {len(DIFFICULTIES)} D × {args.n}…"
    )
    for i, entry in enumerate(entries, 1):
        tid = entry["type_id"]
        if tid not in QUESTION_TYPES:
            skipped.append({"type_id": tid, "reason": "not registered in QUESTION_TYPES"})
            continue
        for d in DIFFICULTIES:
            batch, err = _generate_batch_with_timeout(tid, d, args.n, args.timeout)
            if err or batch is None:
                failures.append(
                    {
                        "type_id": tid,
                        "generator": entry["generator"],
                        "course": entry["course"],
                        "difficulty": float(d),
                        "error": err or "unknown",
                    }
                )
                continue
            if not batch:
                failures.append(
                    {
                        "type_id": tid,
                        "generator": entry["generator"],
                        "course": entry["course"],
                        "difficulty": float(d),
                        "error": "empty result",
                    }
                )
                continue
            for row in batch:
                row["name"] = entry["name"]
                row["generator"] = entry["generator"]
                row["category"] = entry["category"]
                row["course"] = entry["course"]
                row["setting_profile"] = entry.get("setting_profile")
                row["prompt_len"] = len(row.get("prompt_latex") or "")
                samples.append(row)
        if i % 10 == 0 or i == len(entries):
            elapsed = time.time() - t0
            print(
                f"  {i}/{len(entries)}  samples={len(samples)}  "
                f"fails={len(failures)}  {elapsed:.1f}s"
            )

    samples_by_type: dict[str, list[dict]] = defaultdict(list)
    for r in samples:
        samples_by_type[r["type_id"]].append(r)
    fails_by_type: dict[str, list[dict]] = defaultdict(list)
    for f in failures:
        fails_by_type[f["type_id"]].append(f)

    attempted = [e for e in entries if e["type_id"] not in {s["type_id"] for s in skipped}]
    n_ok = 0
    n_partial = 0
    n_failed = 0
    for e in attempted:
        tid = e["type_id"]
        has_s = tid in samples_by_type
        has_f = tid in fails_by_type
        if has_s and not has_f:
            n_ok += 1
        elif has_s and has_f:
            n_partial += 1
        else:
            n_failed += 1

    # High-D explosion / oddity notes (heuristic from prompt lengths)
    explode_notes: list[str] = []
    by_type_d_len: dict[str, dict[float, float]] = defaultdict(dict)
    for r in samples:
        tid = r["type_id"]
        d = float(r["difficulty"])
        plen = float(r.get("prompt_len") or 0)
        prev = by_type_d_len[tid].get(d)
        by_type_d_len[tid][d] = max(prev or 0.0, plen)
    for tid, dmap in sorted(by_type_d_len.items()):
        d0 = dmap.get(0.0, 0.0)
        d50 = dmap.get(50.0, 0.0)
        if d50 >= 800:
            explode_notes.append(
                f"`{tid}`: very long prompt at D=50 (len≈{d50:.0f}; D=0≈{d0:.0f})"
            )
        elif d50 >= 400 and d0 > 0 and d50 / max(d0, 1) >= 8:
            explode_notes.append(
                f"`{tid}`: grows sharply by D=50 (len≈{d50:.0f} vs D=0≈{d0:.0f})"
            )
    explode_notes = explode_notes[:80]

    elapsed_s = time.time() - t0
    summary = {
        "generated": generated,
        "filter": "continuous_difficulty_only",
        "filter_rule": (
            "Ready non-scaffold catalog types whose settings_schema includes "
            "a difficulty field with type in {int,float,number,range}"
        ),
        "difficulties": list(DIFFICULTIES),
        "n_per": args.n,
        "timeout_s": args.timeout,
        "included": len(attempted),
        "excluded_ready": len(excluded),
        "unique_generators": n_unique_generators,
        "exclude_reason_counts": dict(exclude_reason_counts),
        "fully_ok": n_ok,
        "partial": n_partial,
        "fully_failed": n_failed,
        "skipped": len(skipped),
        "sample_rows": len(samples),
        "failure_rows": len(failures),
        "elapsed_s": round(elapsed_s, 2),
        "explode_notes": explode_notes,
        "included_type_ids": [e["type_id"] for e in attempted],
        "included_generators": sorted({e["generator"] for e in attempted}),
        "skipped_detail": skipped,
    }

    with (OUT / "samples.jsonl").open("w", encoding="utf-8") as fh:
        for row in samples:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    with (OUT / "failed.jsonl").open("w", encoding="utf-8") as fh:
        for row in failures:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    with (OUT / "excluded.jsonl").open("w", encoding="utf-8") as fh:
        for row in excluded:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    (OUT / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    d_list = ", ".join(
        str(int(d)) if d == int(d) else str(d) for d in DIFFICULTIES
    )
    lede = (
        f"Generated {generated}. "
        f"<strong>Continuous-difficulty only:</strong> included "
        f"<strong>{len(attempted)}</strong> Ready types "
        f"({n_unique_generators} unique generators); "
        f"excluded <strong>{len(excluded)}</strong> Ready types without a numeric "
        f"<span class='code'>difficulty</span> slider field. "
        f"Generation: fully OK {n_ok}, partial {n_partial}, failed {n_failed}, "
        f"skipped {len(skipped)}. "
        f"D ∈ {{{d_list}}}, {args.n} samples each. "
        f"Display latex truncated at {DISPLAY_TRUNCATE} chars; "
        f"full text in <span class='code'>samples.jsonl</span>."
    )

    course_links = []
    for course, _ in COURSE_CATALOGS:
        course_entries = [e for e in entries if e["course"] == course]
        if not course_entries:
            continue
        course_html = _build_course_html(
            f"Difficulty sweep (continuous) — {course}",
            lede,
            course_entries,
            samples_by_type,
            fails_by_type,
            nav_extra='<a href="../index.html">← Index</a> <a href="../gallery.html">Full gallery</a>',
        )
        (OUT / "by_course" / f"{course}.html").write_text(course_html, encoding="utf-8")
        course_links.append(
            f'<a class="pill" href="by_course/{_esc(course)}.html">{_esc(course)}</a> '
            f"({len(course_entries)})"
        )

    gallery = _build_course_html(
        "Difficulty sweep — continuous difficulty types",
        lede,
        entries,
        samples_by_type,
        fails_by_type,
        nav_extra='<a href="index.html">← Index</a>',
    )
    (OUT / "gallery.html").write_text(gallery, encoding="utf-8")

    index_parts = _katex_head("Difficulty sweep index (continuous only)")
    index_parts.extend(
        [
            "<h1>Difficulty sweep gallery (continuous only)</h1>",
            f'<p class="lede">{lede}</p>',
            "<h2>Open</h2>",
            '<p class="nav">',
            '<a href="gallery.html"><strong>Full gallery</strong></a>',
            '<a href="INDEX.md">INDEX.md</a>',
            '<a href="samples.jsonl">samples.jsonl</a>',
            '<a href="failed.jsonl">failed.jsonl</a>',
            '<a href="excluded.jsonl">excluded.jsonl</a>',
            '<a href="summary.json">summary.json</a>',
            "</p>",
            "<h2>By course</h2>",
            f"<p>{' '.join(course_links) if course_links else '—'}</p>",
            "<h2>Summary</h2>",
            "<table class='compare'><thead><tr><th>Metric</th><th>Value</th></tr></thead><tbody>",
            f"<tr><td>Included (continuous difficulty)</td><td><span class='pill ok'>{len(attempted)}</span></td></tr>",
            f"<tr><td>Unique generators</td><td>{n_unique_generators}</td></tr>",
            f"<tr><td>Excluded Ready (no continuous D)</td><td><span class='pill warn'>{len(excluded)}</span></td></tr>",
            f"<tr><td>Fully succeeded</td><td><span class='pill ok'>{n_ok}</span></td></tr>",
            f"<tr><td>Partial</td><td><span class='pill warn'>{n_partial}</span></td></tr>",
            f"<tr><td>Fully failed</td><td><span class='pill fail'>{n_failed}</span></td></tr>",
            f"<tr><td>Sample rows</td><td>{len(samples)}</td></tr>",
            f"<tr><td>Elapsed</td><td>{elapsed_s:.1f}s</td></tr>",
            "</tbody></table>",
            "<h2>Exclude reasons</h2><ul>",
        ]
    )
    for reason, count in sorted(
        exclude_reason_counts.items(), key=lambda kv: (-kv[1], kv[0])
    ):
        index_parts.append(f"<li>{_esc(reason)}: <strong>{count}</strong></li>")
    index_parts.append("</ul>")

    if explode_notes:
        index_parts.append("<h2>High-D notes</h2><ul>")
        for note in explode_notes:
            index_parts.append(f"<li>{_esc(note)}</li>")
        index_parts.append("</ul>")
    if failures:
        index_parts.append("<h2>Failures (first 40)</h2><ul>")
        for f in failures[:40]:
            index_parts.append(
                f"<li><span class='code'>{_esc(f['type_id'])}</span> "
                f"D={f['difficulty']:g}: {_esc(f.get('error') or '')}</li>"
            )
        if len(failures) > 40:
            index_parts.append(
                f"<li>… and {len(failures) - 40} more (see failed.jsonl)</li>"
            )
        index_parts.append("</ul>")
    index_parts.append("</body></html>")
    (OUT / "index.html").write_text("\n".join(index_parts), encoding="utf-8")

    _write_index_md(
        OUT / "INDEX.md",
        generated=generated,
        n_included=len(attempted),
        n_excluded=len(excluded),
        n_unique_generators=n_unique_generators,
        n_ok=n_ok,
        n_partial=n_partial,
        n_failed=n_failed,
        n_skipped=len(skipped),
        skipped=skipped,
        explode_notes=explode_notes,
        elapsed_s=elapsed_s,
        exclude_reason_counts=dict(exclude_reason_counts),
    )

    print()
    print(f"Done in {elapsed_s:.1f}s")
    print(
        f"  included={len(attempted)} excluded={len(excluded)} "
        f"OK={n_ok} partial={n_partial} failed={n_failed}"
    )
    print(f"  samples={len(samples)} failure_rows={len(failures)}")
    print(f"  Gallery: {OUT / 'gallery.html'}")
    print(f"  Index:   {OUT / 'index.html'}")


if __name__ == "__main__":
    main()
