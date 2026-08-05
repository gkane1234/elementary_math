"""Build KaTeX galleries for verified / done continuous-difficulty topics.

Writes under scripts/output/topic_fit/:
  by_topic/<course_prefix><type_id>/gallery.md  (prefix omitted if type_id already has one)
  by_topic/<…>/gallery.html
  by_topic/<…>/samples.jsonl
  INDEX.md  — master index of all topic_fit galleries

Sources of “done” topics (priority):
  1. g6_difficulty/TRACKING.json status == verified_ramp
  2. pa_difficulty first-tranche verified_ramp (+ optional second tranche)
  3. A1 continuous types with effort scorers (a1_export_types.json)
  4. Existing audit folders (listed in INDEX; not regenerated here)

OOO by_topic types are skipped by default; pass --include-ooo after the
bare-number fix (test_ooo_no_bare_number), or --only-ooo to refresh just
those type_ids. Separate ooo_audit / constructive_ooo_audit folders are
rebuilt via build_layer1_primitive_audits.py and build_constructive_audits.py.

All by_topic samples use the live continuous-D generate API path
(``question_engine.api.handler._generate_for_type``), same as WorksheetGenerator.

Usage:
  $env:PYTHONPATH='.'
  python scripts/build_verified_topic_galleries.py
  python scripts/build_verified_topic_galleries.py --course all --force-live
  python scripts/build_verified_topic_galleries.py --course g6
  python scripts/build_verified_topic_galleries.py --course pa --include-second-tranche
  python scripts/build_verified_topic_galleries.py --course a1
  python scripts/build_verified_topic_galleries.py --type-id g6_decimal_addition --type-id quadratic_formula
  python scripts/build_verified_topic_galleries.py --include-ooo
  python scripts/build_verified_topic_galleries.py --only-ooo
  python scripts/build_verified_topic_galleries.py --index-only
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import question_engine.types  # noqa: F401
from question_engine.core.base import QUESTION_TYPES
from question_engine.topic_labels import format_topic_label

import importlib.util

_render_spec = importlib.util.spec_from_file_location(
    "render_topic_fit_gallery_html",
    ROOT / "scripts" / "render_topic_fit_gallery_html.py",
)
_render_mod = importlib.util.module_from_spec(_render_spec)
assert _render_spec.loader is not None
_render_spec.loader.exec_module(_render_mod)
wrap_gallery_html = _render_mod.wrap_gallery_html

_naming_spec = importlib.util.spec_from_file_location(
    "topic_fit_naming",
    ROOT / "scripts" / "topic_fit_naming.py",
)
_naming_mod = importlib.util.module_from_spec(_naming_spec)
assert _naming_spec.loader is not None
_naming_spec.loader.exec_module(_naming_mod)
gallery_folder_name = _naming_mod.gallery_folder_name
type_id_from_folder = _naming_mod.type_id_from_folder

_struct_spec = importlib.util.spec_from_file_location(
    "topic_fit_structure",
    ROOT / "scripts" / "topic_fit_structure.py",
)
_struct_mod = importlib.util.module_from_spec(_struct_spec)
assert _struct_spec.loader is not None
_struct_spec.loader.exec_module(_struct_mod)
extract_structure_meta = _struct_mod.extract_structure_meta
format_structure_cell = _struct_mod.format_structure_cell
inventory_counts = _struct_mod.inventory_counts
inventory_markdown = _struct_mod.inventory_markdown

TOPIC_FIT = ROOT / "scripts" / "output" / "topic_fit"
BY_TOPIC = TOPIC_FIT / "by_topic"
G6_TRACKING = TOPIC_FIT / "g6_difficulty" / "TRACKING.json"
PA_TRACKING = TOPIC_FIT / "pa_difficulty" / "TRACKING.json"
A1_EXPORT = ROOT / "scripts" / "output" / "ml" / "a1_export_types.json"

DIFFS = (0.0, 5.0, 10.0, 15.0, 20.0, 25.0)
N_PER = 2

# OOO by_topic — skipped unless --include-ooo / --only-ooo (bare-number fix landed).
OOO_TYPE_IDS = frozenset(
    {
        "order_of_operations",
        "g6_numeric_expressions_and_order_of_operations",
        "g6_writing_numeric_expressions",
        "g6_numeric_expressions_with_exponents",
    }
)
OOO_FOLDER_MARKERS = ("ooo_audit", "constructive_ooo")


def _load_g6_verified() -> list[tuple[str, str]]:
    data = json.loads(G6_TRACKING.read_text(encoding="utf-8"))
    out: list[tuple[str, str]] = []
    for t in data.get("topics") or []:
        if t.get("status") == "verified_ramp":
            out.append((t["type_id"], t.get("name") or t["type_id"]))
    return out


def _load_pa_topics(*, include_second: bool) -> list[tuple[str, str]]:
    data = json.loads(PA_TRACKING.read_text(encoding="utf-8"))
    # First tranche: listed in TRACKING.md / export; prefer explicit list if present.
    first = data.get("first_tranche") or []
    if not first:
        # Fall back to PA_DIFFICULTY TRACKING.md table via known list from summary export.
        first = [
            "pa_naming_decimal_places_and_rounding",
            "pa_writing_numbers_with_words",
            "pa_integers_adding_and_subtracting",
            "pa_integers_multiplying",
            "pa_integers_dividing",
            "pa_factoring",
            "pa_greatest_common_factor",
            "pa_least_common_multiple",
            "pa_simplifying_fractions",
            "pa_converting_fractions_and_decimals",
            "pa_fractions_decimals_and_percents",
            "pa_simple_and_compound_interest",
            "pa_squares_and_square_roots",
        ]
    ids = list(first)
    if include_second:
        ids.extend(data.get("second_tranche") or [])
    out: list[tuple[str, str]] = []
    for tid in ids:
        qt = QUESTION_TYPES.get(tid)
        name = getattr(qt, "name", None) or tid
        out.append((tid, name))
    return out


def _load_a1_topics() -> list[tuple[str, str]]:
    """A1 continuous-D types with registered effort scorers (export list)."""
    from question_engine.ml.effort import has_effort_scorer

    data = json.loads(A1_EXPORT.read_text(encoding="utf-8"))
    out: list[tuple[str, str]] = []
    for tid in data.get("type_ids") or []:
        if not has_effort_scorer(tid):
            continue
        qt = QUESTION_TYPES.get(tid)
        name = getattr(qt, "name", None) or tid
        out.append((tid, name))
    return out


def _sample_topic(tid: str) -> list[dict[str, Any]]:
    """Sample via live ``_generate_for_type`` (same path as WorksheetGenerator API)."""
    from question_engine.api.handler import _generate_for_type

    rows: list[dict[str, Any]] = []
    for d in DIFFS:
        try:
            settings = {
                "difficulty": d,
                "count": N_PER,
                "seed": 40 + int(d) * 13 + (hash(tid) % 997),
                "include_answer_key": True,
                "include_diagram": True,
                "include_graph_metadata": True,
            }
            qs = _generate_for_type(tid, settings)
        except Exception as exc:  # noqa: BLE001
            rows.append(
                {
                    "type_id": tid,
                    "difficulty": d,
                    "index": 0,
                    "prompt_latex": "",
                    "prompt_text": "",
                    "answer_latex": "",
                    "error": str(exc),
                }
            )
            continue
        for i, q in enumerate(qs):
            meta = q.metadata or {}
            struct = extract_structure_meta(meta)
            if struct.get("difficulty") is None:
                struct["difficulty"] = d
            rows.append(
                {
                    "type_id": tid,
                    "difficulty": d,
                    "index": i,
                    "prompt_latex": (q.prompt_latex or "").strip(),
                    "prompt_text": (q.prompt_text or "").strip(),
                    "answer_latex": (q.answer_latex or "").strip(),
                    "error": None,
                    # Live-path fingerprint from ``_annotate_questions``.
                    "generation_settings": meta.get("generation_settings"),
                    "primitive_engine": meta.get("primitive_engine"),
                    "spend": meta.get("spend"),
                    "upgrades": meta.get("upgrades"),
                    "n_ops": meta.get("n_ops"),
                    "nest_depth": meta.get("nest_depth"),
                    "shape_id": meta.get("shape_id"),
                    "sample_log": meta.get("sample_log"),
                    "structure": struct,
                    "family": meta.get("family"),
                    "structure_id": meta.get("structure_id"),
                    "function_classes": meta.get("function_classes"),
                    "methods_used": meta.get("methods_used"),
                    "chain_depth": meta.get("chain_depth"),
                }
            )
    return rows


def _build_md(tid: str, name: str, rows: list[dict[str, Any]]) -> str:
    label = format_topic_label(tid, name)
    lines = [
        f"# {label}",
        "",
        f"`{tid}` — continuous difficulty samples for topic-fit / ramp review.",
        "",
        "Samples via the **live continuous-D API path** "
        "(`QUESTION_TYPES` / `_generate_for_type` / seed / `include_answer_key`).",
        "",
        "Open [gallery.html](gallery.html) in a browser for **KaTeX-rendered math** "
        "(markdown preview leaves `$...$` as raw LaTeX).",
        "",
        f"Difficulties: {', '.join(str(int(d)) if d == int(d) else str(d) for d in DIFFS)} "
        f"· {N_PER} sample(s) each.",
        "",
    ]
    lines.extend(inventory_markdown(rows))
    lines.extend(
        [
            "| D | Prompt | Answer | Structure |",
            "|--:|--------|--------|-----------|",
        ]
    )
    for r in rows:
        d = r["difficulty"]
        d_s = f"{d:g}" if isinstance(d, float) else str(d)
        if r.get("error"):
            lines.append(f"| {d_s} | ERROR: {r['error']} | — | — |")
            continue
        pl = (r.get("prompt_latex") or r.get("prompt_text") or "").replace("|", "\\|")
        al = (r.get("answer_latex") or "").replace("|", "\\|")
        if not pl.startswith("$"):
            pl = f"${pl}$"
        if al and not al.startswith("$"):
            al = f"${al}$"
        st = format_structure_cell(
            r.get("structure"), difficulty=r.get("difficulty")
        ).replace("|", "\\|")
        lines.append(f"| {d_s} | {pl} | {al or '—'} | `{st}` |")
    lines.append("")
    return "\n".join(lines)


def write_topic_gallery(tid: str, name: str) -> Path:
    out = BY_TOPIC / gallery_folder_name(tid)
    out.mkdir(parents=True, exist_ok=True)
    rows = _sample_topic(tid)
    (out / "samples.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n",
        encoding="utf-8",
    )
    label = format_topic_label(tid, name)
    md = _build_md(tid, name, rows)
    (out / "gallery.md").write_text(md, encoding="utf-8")
    html_path = out / "gallery.html"
    html_path.write_text(
        wrap_gallery_html(md, title=label, html_path=html_path), encoding="utf-8"
    )
    counts = inventory_counts(rows)
    (out / "structure_inventory.json").write_text(
        json.dumps(
            {
                "sample_count": len([r for r in rows if not r.get("error")]),
                "distinct_structures": [
                    {"structure": label, "count": n}
                    for label, n in counts
                    if label != "(unlabeled)"
                ],
                "unlabeled_count": next(
                    (n for label, n in counts if label == "(unlabeled)"), 0
                ),
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    return out


def _is_dated_folder(name: str) -> bool:
    return bool(re.match(r"^\d{8}T", name)) or bool(re.search(r"_20\d{6}T", name))


def _is_ooo_folder(name: str) -> bool:
    return any(m in name for m in OOO_FOLDER_MARKERS)


def discover_existing_galleries() -> list[dict[str, str]]:
    """Find folders (and by_topic children) with gallery.html."""
    found: list[dict[str, str]] = []
    seen: set[str] = set()

    def add(rel: str, title: str, kind: str) -> None:
        if rel in seen:
            return
        seen.add(rel)
        found.append({"rel": rel, "title": title, "kind": kind})

    # by_topic first
    if BY_TOPIC.is_dir():
        for p in sorted(BY_TOPIC.iterdir()):
            if not p.is_dir():
                continue
            html = p / "gallery.html"
            if html.is_file():
                tid = type_id_from_folder(
                    p.name, known_ids=frozenset(QUESTION_TYPES)
                )
                qt = QUESTION_TYPES.get(tid)
                name = getattr(qt, "name", None) or tid
                add(
                    f"by_topic/{p.name}/gallery.html",
                    format_topic_label(tid, name),
                    "by_topic",
                )

    for p in sorted(TOPIC_FIT.iterdir()):
        if not p.is_dir() or p.name == "by_topic":
            continue
        if _is_dated_folder(p.name):
            continue
        html = p / "gallery.html"
        if html.is_file():
            kind = "ooo_audit" if _is_ooo_folder(p.name) else "audit"
            add(f"{p.name}/gallery.html", p.name, kind)
        # nested lane galleries
        for nested in sorted(p.rglob("gallery.html")):
            if nested.parent == p:
                continue
            rel = nested.relative_to(TOPIC_FIT).as_posix()
            add(rel, rel.rsplit("/", 1)[0], "nested")

    return found


def write_index(
    *,
    generated: list[tuple[str, str]],
    skipped_ooo: list[str],
    failures: list[str],
    remaining_notes: list[str],
) -> Path:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    galleries = discover_existing_galleries()

    lines = [
        "# Topic-fit galleries INDEX",
        "",
        f"Generated: `{now}`",
        "",
        "Topic labels use a short **course prefix** + human name "
        "(`g6: ...`, `pa: ...`, `a1: ...`, `ge: ...`, `a2: ...`, `pc: ...`, "
        "`c1`/`c2`/`c3: ...`). "
        "See [`lib/topic-labels.ts`](../../../lib/topic-labels.ts) / "
        "[`question_engine/topic_labels.py`](../../../question_engine/topic_labels.py). "
        "Internal `type_id`s are unchanged.",
        "",
        "All **by_topic** samples use the **live continuous-D generate API path** "
        "(`QUESTION_TYPES` → `_generate_for_type` → presets / annotation), same as "
        "WorksheetGenerator. Open any **gallery.html** in a browser (KaTeX). "
        "Cursor markdown preview does not render `$...$` math.",
        "",
        "## How to open",
        "",
        "```powershell",
        "# From repo root — example",
        "start scripts/output/topic_fit/INDEX.md",
        "start scripts/output/topic_fit/by_topic/g6_decimal_addition/gallery.html",
        "start scripts/output/topic_fit/by_topic/a1_coin_word_problems/gallery.html",
        "start scripts/output/topic_fit/ooo_audit/gallery.html",
        "```",
        "",
        "## Regenerate",
        "",
        "```powershell",
        "$env:PYTHONPATH='.'",
        "python scripts/build_verified_topic_galleries.py --course all --force-live",
        "python scripts/build_verified_topic_galleries.py --course pa --include-second-tranche --force-live",
        "python scripts/build_verified_topic_galleries.py --course a1 --force-live",
        "python scripts/build_verified_topic_galleries.py --include-ooo",
        "python scripts/build_verified_topic_galleries.py --only-ooo",
        "python scripts/build_layer1_primitive_audits.py  # refreshes ooo_audit via live path",
        "python scripts/render_topic_fit_gallery_html.py --all-missing",
        "python scripts/relabel_topic_fit_galleries.py  # titles/h1 + INDEX only",
        "```",
        "",
        f"## Summary",
        "",
        f"| Existing HTML galleries (indexed) | {len(galleries)} |",
        f"| by_topic galleries written this run | {len(generated)} |",
        f"| OOO skipped this run | {len(skipped_ooo)} |",
        f"| Failures this run | {len(failures)} |",
        "",
    ]

    if remaining_notes:
        lines.append("## Done vs remaining")
        lines.append("")
        for note in remaining_notes:
            lines.append(f"- {note}")
        lines.append("")

    if skipped_ooo:
        lines.append("## OOO — skipped this run")
        lines.append("")
        lines.append(
            "Pass `--include-ooo` to regenerate these by_topic type_ids "
            "(bare-number fix is in; also refresh `ooo_audit` / "
            "`constructive_ooo_audit` via the layer1 / constructive audit scripts):"
        )
        lines.append("")
        for tid in skipped_ooo:
            lines.append(f"- `{tid}`")
        lines.append("")

    # Group index
    by_topic = [g for g in galleries if g["kind"] == "by_topic"]
    audits = [g for g in galleries if g["kind"] in ("audit", "ooo_audit")]
    nested = [g for g in galleries if g["kind"] == "nested"]

    lines.append("## Per-topic continuous galleries (`by_topic/`)")
    lines.append("")
    if by_topic:
        lines.append("| Topic | HTML |")
        lines.append("|-------|------|")
        for g in by_topic:
            lines.append(f"| {g['title']} | [{g['rel']}]({g['rel']}) |")
    else:
        lines.append("_None yet — run this script without `--index-only`._")
    lines.append("")

    lines.append("## Audit / family galleries")
    lines.append("")
    lines.append("| Folder | HTML | Notes |")
    lines.append("|--------|------|-------|")
    for g in audits:
        note = "OOO family audit" if g["kind"] == "ooo_audit" else ""
        lines.append(f"| `{g['title']}` | [{g['rel']}]({g['rel']}) | {note} |")
    lines.append("")

    if nested:
        lines.append("## Nested galleries")
        lines.append("")
        for g in nested:
            lines.append(f"- [{g['rel']}]({g['rel']})")
        lines.append("")

    if failures:
        lines.append("## Failures this run")
        lines.append("")
        for msg in failures:
            lines.append(f"- {msg}")
        lines.append("")

    path = TOPIC_FIT / "INDEX.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--course",
        choices=("all", "g6", "pa", "a1"),
        default="all",
        help="Which verified sets to sample (default: all = g6+pa; use a1 for Algebra 1)",
    )
    ap.add_argument(
        "--include-second-tranche",
        action="store_true",
        help="Also sample PA second-tranche type_ids (scorers wired; ramp QA pending)",
    )
    ap.add_argument(
        "--include-ooo",
        action="store_true",
        help="Regenerate OOO-related type_ids (default: skip until bugfix)",
    )
    ap.add_argument(
        "--only-ooo",
        action="store_true",
        help="Only regenerate OOO_TYPE_IDS (implies --include-ooo); skip other topics",
    )
    ap.add_argument(
        "--force-live",
        action="store_true",
        help=(
            "Documented regenerate flag: all by_topic sampling already uses "
            "live _generate_for_type (no-op; accepted for CLI compatibility)"
        ),
    )
    ap.add_argument(
        "--type-id",
        action="append",
        dest="type_ids",
        default=[],
        help="Regenerate only these type_ids (repeatable); skips course topic lists",
    )
    ap.add_argument(
        "--index-only",
        action="store_true",
        help="Only rebuild INDEX.md from existing galleries",
    )
    ap.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Max topics to generate (0 = no limit)",
    )
    args = ap.parse_args()

    topics: list[tuple[str, str]] = []
    if not args.index_only:
        if args.type_ids:
            for tid in args.type_ids:
                qt = QUESTION_TYPES.get(tid)
                name = getattr(qt, "name", None) or tid
                topics.append((tid, name))
        else:
            if args.course in ("all", "g6"):
                topics.extend(_load_g6_verified())
            if args.course in ("all", "pa"):
                topics.extend(
                    _load_pa_topics(include_second=args.include_second_tranche)
                )
            if args.course in ("a1",):
                topics.extend(_load_a1_topics())
        # `--course all` historically meant g6+pa; A1 is opt-in via --course a1
        # so a full refresh of G6/PA does not re-sample all A1 leaves.

    # Dedupe preserving order
    seen: set[str] = set()
    uniq: list[tuple[str, str]] = []
    for tid, name in topics:
        if tid in seen:
            continue
        seen.add(tid)
        uniq.append((tid, name))

    skipped_ooo: list[str] = []
    generated: list[tuple[str, str]] = []
    failures: list[str] = []

    if not args.index_only:
        if args.only_ooo:
            # Focused refresh: known OOO family type_ids only.
            to_run = []
            for tid in sorted(OOO_TYPE_IDS):
                qt = QUESTION_TYPES.get(tid)
                name = getattr(qt, "name", None) or tid
                to_run.append((tid, name))
        else:
            to_run = uniq
            if not args.include_ooo:
                filtered = []
                for tid, name in to_run:
                    if tid in OOO_TYPE_IDS:
                        skipped_ooo.append(tid)
                    else:
                        filtered.append((tid, name))
                to_run = filtered
        if args.limit and args.limit > 0:
            to_run = to_run[: args.limit]

        BY_TOPIC.mkdir(parents=True, exist_ok=True)
        for i, (tid, name) in enumerate(to_run, 1):
            try:
                path = write_topic_gallery(tid, name)
                generated.append((tid, name))
                print(f"[{i}/{len(to_run)}] wrote {path.relative_to(ROOT)}")
            except Exception as exc:  # noqa: BLE001
                msg = f"{tid}: {exc}"
                failures.append(msg)
                print(f"[{i}/{len(to_run)}] FAIL {msg}")

    a1_n = len(_load_a1_topics()) if A1_EXPORT.is_file() else 0
    a1_gallery_n = sum(
        1
        for tid, _ in (_load_a1_topics() if A1_EXPORT.is_file() else [])
        if (BY_TOPIC / gallery_folder_name(tid) / "gallery.html").is_file()
    )
    remaining = [
        "G6 weak/failed ramp topics (6) — not gallery-verified until fixed "
        "(see g6_difficulty/TRACKING.md).",
        "PA galleries cover first + second tranche (33). Remaining PA: "
        "extend_primitive / hard geo / blocked markup (see pa_difficulty/TRACKING.md).",
        f"A1 continuous effort — `{a1_gallery_n}`/`{a1_n}` by_topic galleries "
        "(a1_export_types.json scorers); refresh via `--course a1`. "
        "Family audit folders remain for deeper reviews.",
        "OOO by_topic + `ooo_audit` use the same live continuous-D path "
        "(`_generate_for_type`); refresh via `--only-ooo` / layer1 script.",
        "Full refresh: `python scripts/build_verified_topic_galleries.py "
        "--course all --force-live` (g6+pa verified; add `--course a1` "
        "and/or `--include-second-tranche` / `--include-ooo` as needed).",
        "Dated one-off folders (`20260713T…`) skipped from INDEX.",
    ]
    if skipped_ooo:
        remaining.insert(
            1,
            "OOO by_topic type_ids skipped this run; use `--include-ooo` "
            "(bare-number fix is in).",
        )

    index_path = write_index(
        generated=generated,
        skipped_ooo=skipped_ooo,
        failures=failures,
        remaining_notes=remaining,
    )
    print(f"INDEX: {index_path}")
    print(f"generated={len(generated)} skipped_ooo={len(skipped_ooo)} failures={len(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
