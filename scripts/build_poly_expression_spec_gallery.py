"""Aggregate HTML gallery for ExpressionSpec / constraint-pack derivatives (Phases 0–3).

Live-samples via ``_generate_for_type`` (same path as WorksheetGenerator) for the
six Spec-driven packs: power, product, algebraic chain, trig, ln/exp, invtrig.

Shows continuous D (no Easy/Medium/Hard labels) plus structure inventory fields
(``shape_id``, ops, nest, methods, function_classes, paren_style).

Usage:
  $env:PYTHONPATH='.'
  python scripts/build_poly_expression_spec_gallery.py
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

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

_struct_spec = importlib.util.spec_from_file_location(
    "topic_fit_structure",
    ROOT / "scripts" / "topic_fit_structure.py",
)
_struct_mod = importlib.util.module_from_spec(_struct_spec)
assert _struct_spec.loader is not None
_struct_spec.loader.exec_module(_struct_mod)
extract_structure_meta = _struct_mod.extract_structure_meta
inventory_counts = _struct_mod.inventory_counts
inventory_markdown = _struct_mod.inventory_markdown

OUT_DIR = ROOT / "scripts" / "output" / "topic_fit" / "poly_expression_spec_gallery"
DIFFS = (0.0, 3.0, 8.0, 12.0, 20.0, 25.0)
SEEDS = (41, 107, 233)  # several independent seeds per D

# Pack demo sections: (section_id, title, type_id, pack_name, paren_style)
PACK_SECTIONS: tuple[tuple[str, str, str, str, str], ...] = (
    (
        "power",
        "Power rule",
        "calc_diff_power_rule",
        "pack_power_rule",
        "minimal",
    ),
    (
        "product",
        "Product rule",
        "calc_diff_product_rule",
        "pack_product_rule",
        "minimal",
    ),
    (
        "alg_chain",
        "Algebraic chain",
        "calc_diff_chain_rule",
        "pack_algebraic_chain",
        "always_powers",
    ),
    (
        "trig",
        "Trigonometric",
        "calc_diff_trigonometric",
        "pack_special_atom (trig)",
        "minimal",
    ),
    (
        "ln_exp",
        "Natural logarithms & exponentials",
        "calc_diff_natural_logarithms_and_exponentials",
        "pack_special_atom (ln/exp)",
        "minimal",
    ),
    (
        "invtrig",
        "Inverse trigonometric",
        "calc_diff_inverse_trigonometric",
        "pack_special_atom (invtrig)",
        "minimal",
    ),
    (
        "general",
        "General derivatives",
        "calc_diff_general",
        "pack_general_derivatives",
        "minimal",
    ),
)


def _dollar(s: str) -> str:
    s = (s or "").strip()
    if not s:
        return "—"
    if s.startswith("$") and s.endswith("$"):
        return s
    return f"${s}$"


def _fmt_list(val: Any) -> str:
    if val is None:
        return ""
    if isinstance(val, (list, tuple)):
        return ",".join(str(x) for x in val if x is not None and str(x) != "")
    return str(val)


def _inventory_summary(
    meta: dict[str, Any],
    *,
    paren_style: str,
    difficulty: float | None = None,
) -> str:
    """Compact Spec / Phase-2 inventory line for gallery cells."""
    bits: list[str] = []
    shape = meta.get("shape_id")
    if shape:
        bits.append(f"shape={shape}")
    ops = _fmt_list(meta.get("ops"))
    if ops:
        bits.append(f"ops=[{ops}]")
    nest = meta.get("nest_depth")
    if nest is not None and nest != "":
        bits.append(f"nest={nest}")
    methods = _fmt_list(meta.get("methods_used"))
    if methods:
        bits.append(f"methods={methods}")
    classes = _fmt_list(meta.get("function_classes"))
    if classes:
        bits.append(f"classes={classes}")
    bits.append(f"paren={paren_style}")
    if difficulty is not None:
        d = float(difficulty)
        bits.append(f"D={d:g}")
    n_terms = meta.get("n_terms")
    n_factors = meta.get("n_factors")
    if n_terms not in (None, "", 0, "0"):
        bits.append(f"terms={n_terms}")
    if n_factors not in (None, "", 0, "0"):
        bits.append(f"factors={n_factors}")
    return " · ".join(bits) if bits else "—"


def _sample_pack(
    tid: str,
    *,
    paren_style: str,
    pack_name: str,
    section_id: str,
) -> list[dict[str, Any]]:
    qt = QUESTION_TYPES[tid]
    name = getattr(qt, "name", None) or tid
    gen = (
        getattr(qt, "generator", None)
        or getattr(qt, "_generator_key", None)
        or ""
    )
    rows: list[dict[str, Any]] = []
    for d in DIFFS:
        for seed_i, seed in enumerate(SEEDS):
            settings = {
                "difficulty": d,
                "count": 1,
                "seed": int(seed) + int(d) * 17 + (hash(tid) % 997),
                "include_answer_key": True,
            }
            try:
                qs = _generate_for_type(tid, settings)
            except Exception as exc:  # noqa: BLE001
                rows.append(
                    {
                        "section_id": section_id,
                        "pack": pack_name,
                        "paren_style": paren_style,
                        "type_id": tid,
                        "name": name,
                        "generator": gen,
                        "difficulty": d,
                        "seed": settings["seed"],
                        "index": seed_i,
                        "prompt_latex": "",
                        "answer_latex": "",
                        "error": str(exc),
                        "structure": {},
                        "shape_id": None,
                        "inventory_summary": "—",
                    }
                )
                continue
            for i, q in enumerate(qs[:1]):
                meta = q.metadata if isinstance(q.metadata, dict) else {}
                struct = extract_structure_meta(meta)
                if struct.get("difficulty") is None:
                    struct["difficulty"] = d
                # Prefer live inventory fields for Spec Phase-2 display.
                for key in (
                    "shape_id",
                    "ops",
                    "nest_depth",
                    "n_terms",
                    "n_factors",
                    "degree_max",
                ):
                    if key in meta and key not in struct:
                        struct[key] = meta[key]
                inv_summary = _inventory_summary(
                    {**meta, **struct},
                    paren_style=paren_style,
                    difficulty=d,
                )
                rows.append(
                    {
                        "section_id": section_id,
                        "pack": pack_name,
                        "paren_style": paren_style,
                        "type_id": tid,
                        "name": name,
                        "generator": gen,
                        "difficulty": d,
                        "seed": settings["seed"],
                        "index": seed_i,
                        "prompt_latex": (q.prompt_latex or "").strip(),
                        "prompt_text": (q.prompt_text or "").strip(),
                        "answer_latex": (q.answer_latex or "").strip(),
                        "error": None,
                        "structure": struct,
                        "shape_id": meta.get("shape_id") or struct.get("shape_id"),
                        "structure_id": meta.get("structure_id")
                        or struct.get("structure_id"),
                        "ops": meta.get("ops"),
                        "nest_depth": meta.get("nest_depth"),
                        "function_classes": meta.get("function_classes")
                        or struct.get("function_classes"),
                        "methods_used": meta.get("methods_used")
                        or struct.get("methods_used"),
                        "chain_depth": meta.get("chain_depth")
                        or struct.get("chain_depth"),
                        "upgrades": meta.get("upgrades")
                        or meta.get("upgrades_applied"),
                        "inventory_summary": inv_summary,
                    }
                )
    return rows


def _build_md(by_section: dict[str, list[dict[str, Any]]]) -> str:
    d_s = ", ".join(str(int(d)) if d == int(d) else str(d) for d in DIFFS)
    all_rows = [r for rows in by_section.values() for r in rows]
    ok = sum(1 for r in all_rows if not r.get("error"))
    err = sum(1 for r in all_rows if r.get("error"))
    lines = [
        "# ExpressionSpec / constraint-pack gallery (Phases 0–3)",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Live samples via `_generate_for_type` for Spec-driven derivative packs "
        f"(D = {d_s}; {len(SEEDS)} seeds each). "
        "No Easy/Medium/Hard band labels — continuous **D=** only.",
        "",
        "Open [gallery.html](gallery.html) in a browser for KaTeX "
        "(local `_assets/katex`).",
        "",
        f"- samples ok: **{ok}** · errors: **{err}**",
        "- inventory: `shape_id`, ops, nest, methods, function_classes, "
        "`paren_style` (from pack)",
        "",
    ]
    lines.extend(
        inventory_markdown(all_rows, heading="## Structure inventory (all packs)")
    )
    lines.append("## Packs")
    lines.append("")
    for section_id, title, tid, pack_name, paren_style in PACK_SECTIONS:
        lines.append(f"- [{title}](#{section_id}) — `{pack_name}`, paren=`{paren_style}`")
    lines.append("")

    for section_id, title, tid, pack_name, paren_style in PACK_SECTIONS:
        rows = by_section.get(section_id, [])
        name = rows[0].get("name") or tid if rows else tid
        label = format_topic_label(tid, name)
        lines.append(f"## {title}")
        lines.append("")
        lines.append(f'<a id="{section_id}"></a>')
        lines.append("")
        lines.append(
            f"`{tid}` · Spec pack `{pack_name}` · `paren_style={paren_style}` · "
            f"topic label: {label}"
        )
        lines.append("")
        lines.extend(inventory_markdown(rows, heading="### Structures in this pack"))
        lines.append(
            "| D | Prompt | Answer | shape_id | Inventory |"
        )
        lines.append("|--:|--------|--------|----------|-----------|")
        for r in rows:
            d = r["difficulty"]
            ds = f"{d:g}" if isinstance(d, float) else str(d)
            if r.get("error"):
                lines.append(f"| {ds} | ERROR: {r['error']} | — | — | — |")
                continue
            pl = _dollar(r.get("prompt_latex") or r.get("prompt_text") or "")
            al = _dollar(r.get("answer_latex") or "")
            shape = str(r.get("shape_id") or "—")
            inv = str(r.get("inventory_summary") or "—")
            # HTML renderer splits only outside $...$; avoid bare `|` in TeX
            # (poly_expression uses \\ln\\left(...\\right) not abs bars).
            lines.append(f"| {ds} | {pl} | {al} | `{shape}` | `{inv}` |")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--only",
        action="append",
        dest="only",
        default=[],
        help="Only these section ids or type_ids (repeatable)",
    )
    args = ap.parse_args()
    only = {s.strip() for s in args.only if s.strip()}

    by_section: dict[str, list[dict[str, Any]]] = {}
    all_rows: list[dict[str, Any]] = []
    for section_id, title, tid, pack_name, paren_style in PACK_SECTIONS:
        if only and section_id not in only and tid not in only:
            continue
        if tid not in QUESTION_TYPES:
            print(f"SKIP missing type {tid}")
            continue
        rows = _sample_pack(
            tid,
            paren_style=paren_style,
            pack_name=pack_name,
            section_id=section_id,
        )
        by_section[section_id] = rows
        all_rows.extend(rows)
        ok = sum(1 for r in rows if not r.get("error"))
        print(f"sampled {section_id} ({tid}): {ok}/{len(rows)} ok")

    if not by_section:
        print("No sections sampled", file=sys.stderr)
        return 1

    md = _build_md(by_section)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "gallery.md").write_text(md, encoding="utf-8")
    html_path = OUT_DIR / "gallery.html"
    html_path.write_text(
        wrap_gallery_html(
            md,
            title="ExpressionSpec / constraint-pack gallery",
            html_path=html_path,
        ),
        encoding="utf-8",
    )
    (OUT_DIR / "samples.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in all_rows) + "\n",
        encoding="utf-8",
    )
    counts = inventory_counts(all_rows)
    payload = {
        "sample_count": len([r for r in all_rows if not r.get("error")]),
        "packs": [
            {
                "section_id": sid,
                "type_id": tid,
                "pack": pack,
                "paren_style": paren,
            }
            for sid, _title, tid, pack, paren in PACK_SECTIONS
            if sid in by_section
        ],
        "difficulties": list(DIFFS),
        "distinct_structures": [
            {"structure": label, "count": n}
            for label, n in counts
            if label != "(unlabeled)"
        ],
        "unlabeled_count": next(
            (n for label, n in counts if label == "(unlabeled)"), 0
        ),
    }
    (OUT_DIR / "structure_inventory.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {html_path}")
    print(f"DONE {len(all_rows)} rows across {len(by_section)} packs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
