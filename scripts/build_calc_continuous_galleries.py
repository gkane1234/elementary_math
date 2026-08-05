"""Regenerate c1_calc_* / c1_calculus_* galleries on continuous D grid.

Uses live ``_generate_for_type`` (same path as WorksheetGenerator / ooo_audit).
Writes gallery.md + gallery.html + samples.jsonl (+ structure_inventory.json)
into course-prefixed folders.

Usage:
  $env:PYTHONPATH='.'
  python scripts/build_calc_continuous_galleries.py
  python scripts/build_calc_continuous_galleries.py --only calc_app_diff_differentials
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import importlib.util

import question_engine.types  # noqa: F401
from question_engine.api.handler import _generate_for_type
from question_engine.core.base import QUESTION_TYPES
from question_engine.topic_labels import format_topic_label

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

OUT_ROOT = ROOT / "scripts" / "output" / "topic_fit"
# Live worksheet D grid (matches by_topic / ooo_audit LIVE_DIFFICULTIES).
DIFFS = (0.0, 5.0, 10.0, 15.0, 20.0, 25.0)
N_PER = 2

# Folder name -> type_id (course-prefixed gallery roots).
CALC_DERIV_TYPE_IDS: tuple[str, ...] = (
    "calc_diff_average_rates_of_change",
    "calc_diff_chain_rule",
    "calc_diff_definition_of_the_derivative",
    "calc_diff_higher_order_derivatives",
    "calc_diff_implicit",
    "calc_diff_instantaneous_rates_of_change",
    "calc_diff_inverse_functions",
    "calc_diff_inverse_trigonometric",
    "calc_diff_logarithmic",
    "calc_diff_natural_logarithms_and_exponentials",
    "calc_diff_other_base_logarithms_and_exponentials",
    "calc_diff_power_rule",
    "calc_diff_product_rule",
    "calc_diff_quotient_rule",
    "calc_diff_trigonometric",
)
CALC_DERIV_FOLDERS: dict[str, str] = {
    gallery_folder_name(tid): tid for tid in CALC_DERIV_TYPE_IDS
}

PILOT_TYPE_IDS: tuple[str, ...] = (
    "calc_app_diff_differentials",
    "calc_app_diff_slope_tangent_and_normal_lines",
    "calc_indef_int_logarithmic_rule_and_exponentials_with_substitution",
)
PILOT_FOLDERS: dict[str, str] = {
    gallery_folder_name(tid): tid for tid in PILOT_TYPE_IDS
}

# Multi-type aggregate galleries (continuous D per type section).
AGGREGATE: dict[str, tuple[str, ...]] = {
    "c1_calculus_derivative_rules": CALC_DERIV_TYPE_IDS,
    "c1_calculus_pilot": (
        "calc_app_diff_slope_tangent_and_normal_lines",
        "calc_app_diff_differentials",
        "calc_indef_int_logarithmic_rule_and_exponentials_with_substitution",
    ),
}


def _sample(tid: str) -> list[dict[str, Any]]:
    qt = QUESTION_TYPES[tid]
    name = getattr(qt, "name", None) or tid
    gen = (
        getattr(qt, "generator", None)
        or getattr(qt, "_generator_key", None)
        or ""
    )
    rows: list[dict[str, Any]] = []
    for d in DIFFS:
        settings = {
            "difficulty": d,
            "count": N_PER,
            "seed": 40 + int(d) * 13 + (hash(tid) % 997),
            "include_answer_key": True,
        }
        try:
            qs = _generate_for_type(tid, settings)
        except Exception as exc:  # noqa: BLE001
            rows.append(
                {
                    "type_id": tid,
                    "name": name,
                    "generator": gen,
                    "difficulty": d,
                    "index": 0,
                    "prompt_latex": "",
                    "answer_latex": "",
                    "error": str(exc),
                    "structure": {},
                }
            )
            continue
        for i, q in enumerate(qs):
            meta = q.metadata if isinstance(q.metadata, dict) else {}
            struct = extract_structure_meta(meta)
            if struct.get("difficulty") is None:
                struct["difficulty"] = d
            rows.append(
                {
                    "type_id": tid,
                    "name": name,
                    "generator": gen,
                    "difficulty": d,
                    "index": i,
                    "prompt_latex": (q.prompt_latex or "").strip(),
                    "prompt_text": (q.prompt_text or "").strip(),
                    "answer_latex": (q.answer_latex or "").strip(),
                    "error": None,
                    "structure": struct,
                    # Keep raw useful fields for jsonl consumers.
                    "family": meta.get("family"),
                    "structure_id": meta.get("structure_id"),
                    "function_classes": meta.get("function_classes"),
                    "methods_used": meta.get("methods_used"),
                    "chain_depth": meta.get("chain_depth"),
                    "upgrades": meta.get("upgrades") or meta.get("upgrades_applied"),
                    "variant": meta.get("variant"),
                    "band": meta.get("band"),
                }
            )
    return rows


def _dollar(s: str) -> str:
    s = (s or "").strip()
    if not s:
        return "—"
    if s.startswith("$") and s.endswith("$"):
        return s
    return f"${s}$"


def _build_single_md(tid: str, rows: list[dict[str, Any]]) -> str:
    name = rows[0].get("name") or tid if rows else tid
    label = format_topic_label(tid, name)
    gen = rows[0].get("generator") or "" if rows else ""
    d_s = ", ".join(str(int(d)) if d == int(d) else str(d) for d in DIFFS)
    lines = [
        f"# {label}",
        "",
        f"`{tid}` — continuous difficulty samples for topic-fit / ramp review.",
        "",
        "Samples via the **live continuous-D API path** "
        "(`QUESTION_TYPES` → `_generate_for_type`).",
        "",
        "Open [gallery.html](gallery.html) in a browser for **KaTeX-rendered math** "
        "(markdown preview leaves `$...$` as raw LaTeX).",
        "",
        f"- generator: `{gen}`",
        f"- difficulties: {d_s} · {N_PER} sample(s) each",
        f"- generated: {datetime.now(timezone.utc).isoformat()}",
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
        ds = f"{d:g}" if isinstance(d, float) else str(d)
        if r.get("error"):
            lines.append(f"| {ds} | ERROR: {r['error']} | — | — |")
            continue
        pl = _dollar(r.get("prompt_latex") or r.get("prompt_text") or "").replace("|", "\\|")
        al = _dollar(r.get("answer_latex") or "").replace("|", "\\|")
        st = format_structure_cell(
            r.get("structure"), difficulty=r.get("difficulty")
        ).replace("|", "\\|")
        lines.append(f"| {ds} | {pl} | {al} | `{st}` |")
    lines.append("")
    return "\n".join(lines)


def _build_aggregate_md(title: str, by_tid: dict[str, list[dict[str, Any]]]) -> str:
    d_s = ", ".join(str(int(d)) if d == int(d) else str(d) for d in DIFFS)
    all_rows = [r for rows in by_tid.values() for r in rows]
    lines = [
        f"# {title}",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Continuous-D samples via live `_generate_for_type` "
        f"(D = {d_s}, {N_PER}/level).",
        "",
        "Open [gallery.html](gallery.html) in a browser for KaTeX.",
        "",
    ]
    lines.extend(inventory_markdown(all_rows, heading="## Structure inventory (all types)"))
    for tid, rows in by_tid.items():
        name = rows[0].get("name") or tid if rows else tid
        label = format_topic_label(tid, name)
        lines.append(f"## {label}")
        lines.append("")
        lines.append(f"`{tid}`")
        lines.append("")
        lines.extend(inventory_markdown(rows, heading="### Structures in this type"))
        lines.append("| D | Prompt | Answer | Structure |")
        lines.append("|--:|--------|--------|-----------|")
        for r in rows:
            d = r["difficulty"]
            ds = f"{d:g}" if isinstance(d, float) else str(d)
            if r.get("error"):
                lines.append(f"| {ds} | ERROR: {r['error']} | — | — |")
                continue
            pl = _dollar(r.get("prompt_latex") or "").replace("|", "\\|")
            al = _dollar(r.get("answer_latex") or "").replace("|", "\\|")
            st = format_structure_cell(
                r.get("structure"), difficulty=r.get("difficulty")
            ).replace("|", "\\|")
            lines.append(f"| {ds} | {pl} | {al} | `{st}` |")
        lines.append("")
    return "\n".join(lines)


def _write_inventory_json(folder: Path, rows: list[dict[str, Any]]) -> None:
    counts = inventory_counts(rows)
    payload = {
        "sample_count": len([r for r in rows if not r.get("error")]),
        "distinct_structures": [
            {"structure": label, "count": n} for label, n in counts if label != "(unlabeled)"
        ],
        "unlabeled_count": next((n for label, n in counts if label == "(unlabeled)"), 0),
    }
    (folder / "structure_inventory.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _write_gallery(folder: Path, md: str, title: str, rows: list[dict[str, Any]]) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "gallery.md").write_text(md, encoding="utf-8")
    html_path = folder / "gallery.html"
    html_path.write_text(
        wrap_gallery_html(md, title=title, html_path=html_path), encoding="utf-8"
    )
    (folder / "samples.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n",
        encoding="utf-8",
    )
    _write_inventory_json(folder, rows)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--only",
        action="append",
        dest="only",
        default=[],
        help="Only regenerate these type_ids or folder names (repeatable)",
    )
    ap.add_argument(
        "--skip-aggregates",
        action="store_true",
        help="Skip multi-type aggregate galleries",
    )
    args = ap.parse_args()
    only = {s.strip() for s in args.only if s.strip()}

    def _wanted_tid(tid: str, folder_name: str) -> bool:
        if not only:
            return True
        return tid in only or folder_name in only

    written: list[str] = []

    for folder_name, tid in {**CALC_DERIV_FOLDERS, **PILOT_FOLDERS}.items():
        if not _wanted_tid(tid, folder_name):
            continue
        if tid not in QUESTION_TYPES:
            print(f"SKIP missing type {tid}")
            continue
        rows = _sample(tid)
        md = _build_single_md(tid, rows)
        name = getattr(QUESTION_TYPES[tid], "name", None) or tid
        label = format_topic_label(tid, name)
        _write_gallery(OUT_ROOT / folder_name, md, label, rows)
        written.append(folder_name)
        print(f"wrote {folder_name} ({tid}, {len(rows)} rows)")

    if not args.skip_aggregates:
        for folder_name, tids in AGGREGATE.items():
            if only and folder_name not in only and not any(
                _wanted_tid(t, gallery_folder_name(t)) for t in tids
            ):
                continue
            by_tid: dict[str, list[dict[str, Any]]] = {}
            all_rows: list[dict[str, Any]] = []
            for tid in tids:
                if tid not in QUESTION_TYPES:
                    print(f"SKIP missing type {tid}")
                    continue
                rows = _sample(tid)
                by_tid[tid] = rows
                all_rows.extend(rows)
            title = (
                "Calculus derivative-rules gallery"
                if folder_name == "c1_calculus_derivative_rules"
                else "Calculus pilot gallery"
            )
            md = _build_aggregate_md(title, by_tid)
            _write_gallery(OUT_ROOT / folder_name, md, title, all_rows)
            written.append(folder_name)
            print(f"wrote {folder_name} ({len(by_tid)} types, {len(all_rows)} rows)")

    print(f"DONE {len(written)} galleries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
