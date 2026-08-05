"""Multi-difficulty HTML galleries for Calc1 + A1/A2/PC algebraic topics.

Live-samples via ``_generate_for_type`` (same path as WorksheetGenerator).
Shows continuous D only (no Easy/Medium/Hard), plus ``tricks_required`` /
``spec_snapshot`` pack when present.

Usage:
  $env:PYTHONPATH='.'
  python scripts/build_algebraic_topic_galleries.py
  python scripts/build_algebraic_topic_galleries.py --only calc1
  python scripts/build_algebraic_topic_galleries.py --only a1 --only a2
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import Counter
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
inventory_markdown = _struct_mod.inventory_markdown

TOPIC_FIT = ROOT / "scripts" / "output" / "topic_fit"
RATINGS = ROOT / "scripts" / "output" / "ml" / "ratings"

DIFFS = (0.0, 3.0, 6.0, 8.0, 12.0, 16.0, 20.0, 25.0)
SEEDS = (41, 107, 233)

# (pack_id, title, type_id) — Calc 1 algebraic leaves from recent Spec work.
CALC1_PACKS: tuple[tuple[str, str, str], ...] = (
    # Limits + continuity
    ("direct", "Limits — direct evaluation", "calc_limits_by_direct_evaluation"),
    ("removable", "Limits — removable discontinuities", "calc_limits_at_removable_discontinuities"),
    ("jump", "Limits — jump discontinuities / kinks", "calc_limits_at_jump_discontinuities_and_kinks"),
    ("essential", "Limits — essential discontinuities", "calc_limits_at_essential_discontinuities"),
    ("infinity", "Limits — at infinity", "calc_limits_at_infinity"),
    ("continuity", "Continuity — classify", "calc_continuity_determining_and_classifying"),
    ("lhopital", "L'Hôpital's rule", "calc_app_diff_lhopitals_rule"),
    # Derivatives (OpenStax Vol.1 Ch.3)
    ("deriv_power", "Derivatives — power rule", "calc_diff_power_rule"),
    ("deriv_product", "Derivatives — product rule", "calc_diff_product_rule"),
    ("deriv_quotient", "Derivatives — quotient rule", "calc_diff_quotient_rule"),
    ("deriv_chain", "Derivatives — chain rule", "calc_diff_chain_rule"),
    ("deriv_trig", "Derivatives — trigonometric", "calc_diff_trigonometric"),
    ("deriv_ln_exp", "Derivatives — ln / exp", "calc_diff_natural_logarithms_and_exponentials"),
    ("deriv_invtrig", "Derivatives — inverse trig", "calc_diff_inverse_trigonometric"),
    ("deriv_higher", "Derivatives — higher order", "calc_diff_higher_order_derivatives"),
    ("deriv_general", "Derivatives — general", "calc_diff_general"),
    # Linear approx / differentials
    ("linear_approx", "Linear approximations", "calc_app_diff_linear_approximations"),
    ("differentials", "Differentials", "calc_app_diff_differentials"),
    # Indefinite integrals
    ("int_power", "Integrals — power rule", "calc_indef_int_power_rule"),
    ("int_trig", "Integrals — trigonometric", "calc_indef_int_trigonometric"),
    ("int_log_exp", "Integrals — log / exp", "calc_indef_int_logarithmic_rule_and_exponentials"),
    ("int_invtrig", "Integrals — inverse trig", "calc_indef_int_inverse_trigonometric"),
    ("int_sub", "Integrals — substitution (power)", "calc_indef_int_power_rule_with_substitution"),
    (
        "int_log_exp_sub",
        "Integrals — log/exp with substitution",
        "calc_indef_int_logarithmic_rule_and_exponentials_with_substitution",
    ),
    (
        "int_trig_sub",
        "Integrals — trigonometric substitution",
        "calc_indef_int_trigonometric_with_substitution",
    ),
    (
        "int_invtrig_sub",
        "Integrals — invtrig with substitution",
        "calc_indef_int_inverse_trigonometric_with_substitution",
    ),
    ("int_parts", "Integrals — integration by parts", "calc_indef_int_integration_by_parts"),
    ("int_pfd", "Integrals — partial fractions", "calc_indef_int_partial_fractions"),
    ("int_multi", "Integrals — multi-trick", "calc_indef_int_multi_trick"),
    # FTC / definite (algebraic when available)
    ("ftc1", "FTC — first", "calc_def_int_first_fundamental_theorem_of_calculus"),
    ("ftc2", "FTC — second", "calc_def_int_second_fundamental_theorem_of_calculus"),
    (
        "def_sub",
        "Definite — substitution / change of variables",
        "calc_def_int_substitution_with_change_of_variables",
    ),
)

GALLERY_SPECS: dict[str, dict[str, Any]] = {
    "calc1": {
        "folder": "calc1_algebraic_gallery",
        "title": "Calc 1 algebraic gallery",
        "campaign": None,
        "packs": CALC1_PACKS,
    },
    "a1": {
        "folder": "a1_algebraic_gallery",
        "title": "Algebra 1 algebraic gallery",
        "campaign": "algebra_1",
        "packs": None,
    },
    "a2": {
        "folder": "a2_algebraic_gallery",
        "title": "Algebra 2 algebraic gallery",
        "campaign": "algebra_2",
        "packs": None,
    },
    "pc": {
        "folder": "pc_algebraic_gallery",
        "title": "Precalculus algebraic gallery",
        "campaign": "precalc_algebraic",
        "packs": None,
    },
}


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


def _extract_form_id(meta: dict[str, Any], struct: dict[str, Any] | None = None) -> str | None:
    """Prefer OpenStax catalog form_id when present."""
    for src in (meta, struct or {}):
        if not isinstance(src, dict):
            continue
        for key in ("form_id", "openstax_form", "form", "family", "shape_id", "structure_id"):
            val = src.get(key)
            if val is None or val == "":
                continue
            return str(val)
    return None


def _load_campaign_packs(campaign: str) -> list[tuple[str, str, str]]:
    """Return (pack_id, title, type_id) from CAMPAIGN.json packs."""
    path = RATINGS / campaign / "CAMPAIGN.json"
    if not path.is_file():
        print(f"WARN missing campaign {path}")
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    packs = data.get("packs") if isinstance(data, dict) else None
    if not isinstance(packs, list):
        return []
    out: list[tuple[str, str, str]] = []
    for p in packs:
        if not isinstance(p, dict):
            continue
        tid = str(p.get("type_id") or "").strip()
        pack = str(p.get("pack") or tid).strip()
        if not tid:
            continue
        openstax = str(p.get("openstax") or "").strip()
        title = openstax or pack.replace("_", " ")
        out.append((pack, title, tid))
    return out


def _meta_summary(meta: dict[str, Any], *, pack_hint: str, difficulty: float) -> str:
    bits: list[str] = []
    snap = meta.get("spec_snapshot")
    snap_pack = None
    if isinstance(snap, dict):
        snap_pack = snap.get("pack") or snap.get("technique") or snap.get("key")
    if snap_pack:
        bits.append(f"spec_pack={snap_pack}")
    elif pack_hint:
        bits.append(f"pack={pack_hint}")

    tricks = meta.get("tricks_required")
    if not tricks and isinstance(snap, dict):
        tricks = snap.get("tricks_required")
    if not tricks and isinstance(meta.get("pipeline"), dict):
        tricks = meta["pipeline"].get("tricks_required")
    t_s = _fmt_list(tricks)
    if t_s:
        bits.append(f"tricks=[{t_s}]")

    methods = _fmt_list(meta.get("methods_used"))
    if methods and methods != t_s:
        bits.append(f"methods={methods}")

    form = (
        meta.get("form_id")
        or meta.get("openstax_form")
        or meta.get("form")
        or meta.get("family")
        or meta.get("structure_id")
    )
    if form:
        bits.append(f"form_id={form}")

    core = meta.get("core_form_id")
    if core and str(core) != str(form):
        bits.append(f"core={core}")

    wraps = meta.get("wrappers_applied")
    if wraps:
        bits.append(f"dress=[{_fmt_list(wraps)}]")

    indet = meta.get("indeterminate_form") or meta.get("indet_form")
    if indet:
        bits.append(f"indet={indet}")

    shape = meta.get("shape_id")
    if shape and str(shape) != str(form):
        bits.append(f"shape={shape}")

    costs = meta.get("difficulty_costs")
    if isinstance(costs, list) and costs:
        parts = []
        for c in costs:
            if not isinstance(c, dict):
                continue
            feat = c.get("feature")
            cost = c.get("cost")
            src = c.get("source") or "?"
            if feat is None or cost is None:
                continue
            try:
                cost_s = f"{float(cost):g}"
            except (TypeError, ValueError):
                cost_s = str(cost)
            parts.append(f"{src}:{feat}={cost_s}")
        if parts:
            total = meta.get("difficulty_cost_total")
            try:
                total_s = f"{float(total):g}" if total is not None else ""
            except (TypeError, ValueError):
                total_s = str(total) if total is not None else ""
            cost_line = " + ".join(parts)
            if total_s:
                cost_line += f" ⇒ {total_s}"
            bits.append(f"costs[{cost_line}]")

    bits.append(f"D={float(difficulty):g}")
    return " · ".join(bits) if bits else f"D={float(difficulty):g}"


def _sample_type(
    tid: str,
    *,
    pack_id: str,
    section_id: str,
) -> list[dict[str, Any]]:
    qt = QUESTION_TYPES.get(tid)
    name = (getattr(qt, "name", None) if qt else None) or tid
    gen = (
        (getattr(qt, "generator", None) if qt else None)
        or (getattr(qt, "_generator_key", None) if qt else None)
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
                        "pack": pack_id,
                        "type_id": tid,
                        "name": name,
                        "generator": gen,
                        "difficulty": d,
                        "seed": settings["seed"],
                        "index": seed_i,
                        "prompt_latex": "",
                        "answer_latex": "",
                        "error": f"{type(exc).__name__}: {exc}",
                        "structure": {},
                        "tricks_required": [],
                        "spec_pack": None,
                        "meta_summary": "—",
                    }
                )
                continue
            for q in qs[:1]:
                meta = q.metadata if isinstance(q.metadata, dict) else {}
                struct = extract_structure_meta(meta)
                if struct.get("difficulty") is None:
                    struct["difficulty"] = d
                snap = meta.get("spec_snapshot")
                snap_pack = None
                if isinstance(snap, dict):
                    snap_pack = snap.get("pack") or snap.get("technique")
                tricks = meta.get("tricks_required") or []
                if not tricks and isinstance(snap, dict):
                    tricks = snap.get("tricks_required") or []
                if not tricks and isinstance(meta.get("pipeline"), dict):
                    tricks = meta["pipeline"].get("tricks_required") or []
                form_id = _extract_form_id(meta, struct)
                rows.append(
                    {
                        "section_id": section_id,
                        "pack": pack_id,
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
                        "tricks_required": list(tricks) if tricks else [],
                        "spec_pack": snap_pack,
                        "spec_snapshot": snap if isinstance(snap, dict) else None,
                        "form_id": form_id,
                        "openstax_form": meta.get("openstax_form") or meta.get("form_id"),
                        "form": meta.get("form") or meta.get("family"),
                        "shape_id": meta.get("shape_id"),
                        "methods_used": meta.get("methods_used"),
                        "meta_summary": _meta_summary(
                            meta, pack_hint=pack_id, difficulty=d
                        ),
                    }
                )
    return rows


def _build_md(
    *,
    title: str,
    packs: list[tuple[str, str, str]],
    by_section: dict[str, list[dict[str, Any]]],
    skipped: list[tuple[str, str, str]],
) -> str:
    d_s = ", ".join(str(int(d)) if d == int(d) else str(d) for d in DIFFS)
    all_rows = [r for rows in by_section.values() for r in rows]
    ok = sum(1 for r in all_rows if not r.get("error"))
    err = sum(1 for r in all_rows if r.get("error"))
    lines = [
        f"# {title}",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        f"Live samples via `_generate_for_type` "
        f"(D = {d_s}; {len(SEEDS)} seeds each). "
        "No Easy/Medium/Hard labels — continuous **D=** only.",
        "",
        "Open [gallery.html](gallery.html) in a browser for KaTeX "
        "(local `_assets/katex`).",
        "",
        f"- topics ok: **{len(by_section)}** · skipped missing: **{len(skipped)}**",
        f"- samples ok: **{ok}** · errors: **{err}**",
        "- metadata: `form_id` / `openstax_form`, `tricks_required`, "
        "`spec_snapshot` pack, shape when present",
        "- difficulty: `difficulty_costs` breakdown "
        "(`form` / `dress` / `spec` → cost) in Metadata column "
        "(heuristic sum; correlates with D, not a calibrated effort model)",
        "- form diversity: see [FORM_ID_INDEX.md](FORM_ID_INDEX.md)",
        "",
    ]
    if skipped:
        lines.append("## Skipped (missing type_id)")
        lines.append("")
        for pack_id, pack_title, tid in skipped:
            lines.append(f"- `{tid}` ({pack_id}: {pack_title})")
        lines.append("")

    lines.extend(inventory_markdown(all_rows, heading="## Structure inventory"))
    lines.append("## Topics")
    lines.append("")
    for pack_id, pack_title, tid in packs:
        if pack_id not in by_section:
            continue
        lines.append(f"- [{pack_title}](#{pack_id}) — `{tid}`")
    lines.append("")

    for pack_id, pack_title, tid in packs:
        rows = by_section.get(pack_id)
        if not rows:
            continue
        name = rows[0].get("name") or tid
        label = format_topic_label(tid, name)
        n_ok = sum(1 for r in rows if not r.get("error"))
        n_err = sum(1 for r in rows if r.get("error"))
        lines.append(f"## {pack_title}")
        lines.append("")
        lines.append(f'<a id="{pack_id}"></a>')
        lines.append("")
        lines.append(
            f"`{tid}` · pack `{pack_id}` · topic label: {label} · "
            f"ok {n_ok}/{len(rows)}"
            + (f" · errors {n_err}" if n_err else "")
        )
        lines.append("")
        lines.extend(inventory_markdown(rows, heading="### Structures in this topic"))
        lines.append("| D | Prompt | Answer | tricks | Metadata |")
        lines.append("|--:|--------|--------|--------|----------|")
        for r in rows:
            d = r["difficulty"]
            ds = f"{d:g}" if isinstance(d, float) else str(d)
            if r.get("error"):
                err_s = str(r["error"]).replace("|", "\\|")[:120]
                lines.append(f"| {ds} | ERROR: {err_s} | — | — | — |")
                continue
            pl = _dollar(r.get("prompt_latex") or r.get("prompt_text") or "")
            al = _dollar(r.get("answer_latex") or "")
            tricks = _fmt_list(r.get("tricks_required")) or "—"
            meta_s = str(r.get("meta_summary") or "—").replace("|", "\\|")
            # Avoid bare | inside TeX breaking the markdown table.
            pl = pl.replace("|", "\\|")
            al = al.replace("|", "\\|")
            lines.append(f"| {ds} | {pl} | {al} | `{tricks}` | `{meta_s}` |")
        lines.append("")
    return "\n".join(lines)


def _form_id_counts(
    by_section: dict[str, list[dict[str, Any]]],
) -> tuple[Counter[str], dict[str, Counter[str]]]:
    overall: Counter[str] = Counter()
    per_section: dict[str, Counter[str]] = {}
    for section_id, rows in by_section.items():
        c: Counter[str] = Counter()
        for r in rows:
            if r.get("error"):
                continue
            fid = r.get("form_id")
            if not fid:
                fid = _extract_form_id({}, r.get("structure") if isinstance(r.get("structure"), dict) else {})
            if not fid:
                continue
            c[str(fid)] += 1
            overall[str(fid)] += 1
        per_section[section_id] = c
    return overall, per_section


def _write_form_id_index(
    folder: Path,
    *,
    title: str,
    packs: list[tuple[str, str, str]],
    by_section: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    overall, per_section = _form_id_counts(by_section)
    lines = [
        f"# {title} — form_id diversity",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        f"- distinct form_ids (overall): **{len(overall)}**",
        f"- samples with form_id: **{sum(overall.values())}**",
        "",
        "## Per section",
        "",
        "| Section | Distinct form_ids | Top forms |",
        "|---------|------------------:|-----------|",
    ]
    section_stats: list[dict[str, Any]] = []
    for pack_id, pack_title, tid in packs:
        c = per_section.get(pack_id) or Counter()
        if not c and pack_id not in by_section:
            continue
        top = ", ".join(f"`{fid}`×{n}" for fid, n in c.most_common(5)) or "—"
        lines.append(
            f"| [{pack_title}](gallery.html#{pack_id}) (`{pack_id}`) | "
            f"{len(c)} | {top} |"
        )
        section_stats.append(
            {
                "pack": pack_id,
                "title": pack_title,
                "type_id": tid,
                "distinct_form_ids": len(c),
                "counts": dict(c.most_common()),
            }
        )
    lines.append("")
    lines.append("## Overall top form_ids")
    lines.append("")
    for fid, n in overall.most_common(40):
        lines.append(f"- `{fid}`: {n}")
    lines.append("")
    path = folder / "FORM_ID_INDEX.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    return {
        "distinct_form_ids": len(overall),
        "samples_with_form_id": sum(overall.values()),
        "overall_top": overall.most_common(40),
        "sections": section_stats,
    }


def _build_gallery(key: str) -> dict[str, Any]:
    spec = GALLERY_SPECS[key]
    folder = TOPIC_FIT / spec["folder"]
    title = spec["title"]
    if spec["packs"] is not None:
        packs = list(spec["packs"])
    else:
        packs = _load_campaign_packs(spec["campaign"])

    by_section: dict[str, list[dict[str, Any]]] = {}
    all_rows: list[dict[str, Any]] = []
    skipped: list[tuple[str, str, str]] = []
    failures: list[dict[str, Any]] = []

    for pack_id, pack_title, tid in packs:
        if tid not in QUESTION_TYPES:
            print(f"  SKIP missing type {tid}")
            skipped.append((pack_id, pack_title, tid))
            failures.append(
                {"gallery": key, "pack": pack_id, "type_id": tid, "reason": "missing_type"}
            )
            continue
        try:
            rows = _sample_type(tid, pack_id=pack_id, section_id=pack_id)
        except Exception as exc:  # noqa: BLE001
            print(f"  FAIL {tid}: {exc}")
            failures.append(
                {
                    "gallery": key,
                    "pack": pack_id,
                    "type_id": tid,
                    "reason": f"{type(exc).__name__}: {exc}",
                }
            )
            continue
        by_section[pack_id] = rows
        all_rows.extend(rows)
        n_ok = sum(1 for r in rows if not r.get("error"))
        n_err = len(rows) - n_ok
        print(f"  sampled {pack_id} ({tid}): {n_ok}/{len(rows)} ok" + (f" ({n_err} err)" if n_err else ""))
        if n_ok == 0 and rows:
            failures.append(
                {
                    "gallery": key,
                    "pack": pack_id,
                    "type_id": tid,
                    "reason": "all_samples_failed",
                    "sample_error": rows[0].get("error"),
                }
            )

    folder.mkdir(parents=True, exist_ok=True)
    result: dict[str, Any] = {
        "key": key,
        "folder": str(folder.relative_to(ROOT)).replace("\\", "/"),
        "html": None,
        "topics_ok": len(by_section),
        "topics_total": len(packs),
        "skipped": skipped,
        "failures": failures,
        "samples_ok": sum(1 for r in all_rows if not r.get("error")),
        "samples_err": sum(1 for r in all_rows if r.get("error")),
    }
    if not by_section:
        print(f"  No sections for {key}")
        (folder / "FAILURES.md").write_text(
            "# Failures\n\n" + "\n".join(f"- `{f}`" for f in failures) + "\n",
            encoding="utf-8",
        )
        return result

    md = _build_md(
        title=title,
        packs=packs,
        by_section=by_section,
        skipped=skipped,
    )
    (folder / "gallery.md").write_text(md, encoding="utf-8")
    html_path = folder / "gallery.html"
    html_path.write_text(
        wrap_gallery_html(md, title=title, html_path=html_path),
        encoding="utf-8",
    )
    (folder / "samples.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False, default=str) for r in all_rows)
        + "\n",
        encoding="utf-8",
    )
    form_stats = _write_form_id_index(
        folder,
        title=title,
        packs=packs,
        by_section=by_section,
    )
    summary = {
        "gallery": key,
        "title": title,
        "generated": datetime.now(timezone.utc).isoformat(),
        "difficulties": list(DIFFS),
        "seeds": list(SEEDS),
        "path": str(folder.relative_to(ROOT)).replace("\\", "/"),
        "open": str((folder / "gallery.html").resolve()),
        "topics": [
            {
                "pack": pid,
                "title": ptitle,
                "type_id": tid,
                "ok": sum(1 for r in by_section[pid] if not r.get("error")),
                "err": sum(1 for r in by_section[pid] if r.get("error")),
            }
            for pid, ptitle, tid in packs
            if pid in by_section
        ],
        "skipped": [
            {"pack": p, "title": t, "type_id": tid} for p, t, tid in skipped
        ],
        "failures": failures,
        "form_id_index": form_stats,
    }
    (folder / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    if failures:
        fail_lines = ["# Failures / skips", ""]
        for f in failures:
            fail_lines.append(
                f"- `{f.get('type_id')}` ({f.get('pack')}): {f.get('reason')}"
                + (f" — {f['sample_error']}" if f.get("sample_error") else "")
            )
        (folder / "FAILURES.md").write_text("\n".join(fail_lines) + "\n", encoding="utf-8")

    result["html"] = str(html_path.relative_to(ROOT)).replace("\\", "/")
    result["distinct_form_ids"] = form_stats.get("distinct_form_ids", 0)
    print(
        f"  wrote {html_path} · distinct form_ids={result['distinct_form_ids']}"
    )
    return result


def _write_master_index(results: list[dict[str, Any]]) -> Path:
    path = TOPIC_FIT / "algebraic_galleries_INDEX.md"
    lines = [
        "# Algebraic topic galleries (Calc1 + A1/A2/PC)",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "Live multi-D samples (`D ∈ {0,3,6,8,12,16,20,25}`, 3 seeds each) "
        "via `_generate_for_type`. Open each **gallery.html** in a browser "
        "(local KaTeX under `_assets/katex`).",
        "",
        "## Open these",
        "",
        "| Gallery | Topics ok | Samples ok | HTML |",
        "|---------|----------:|-----------:|------|",
    ]
    for r in results:
        html = r.get("html") or "—"
        link = f"[{html}]({html.split('/')[-2] + '/gallery.html'})" if r.get("html") else "—"
        # Prefer relative link from TOPIC_FIT
        if r.get("html"):
            rel = Path(r["html"]).relative_to(TOPIC_FIT.relative_to(ROOT)).as_posix()
            link = f"[gallery.html]({rel})"
        lines.append(
            f"| {r['key']} | {r['topics_ok']}/{r['topics_total']} | "
            f"{r['samples_ok']} (+{r['samples_err']} err) | {link} |"
        )
    lines.append("")
    lines.append("## Absolute paths (Windows)")
    lines.append("")
    lines.append("```")
    for r in results:
        if r.get("html"):
            abs_p = (ROOT / r["html"]).resolve()
            lines.append(str(abs_p))
    lines.append("```")
    lines.append("")
    lines.append("## Regenerate")
    lines.append("")
    lines.append("```powershell")
    lines.append("$env:PYTHONPATH='.'")
    lines.append("python scripts/build_algebraic_topic_galleries.py")
    lines.append("```")
    lines.append("")
    lines.append("## Related")
    lines.append("")
    lines.append(
        "- Spec derivative packs: "
        "[poly_expression_spec_gallery/gallery.html]"
        "(poly_expression_spec_gallery/gallery.html)"
    )
    lines.append("- Full topic-fit INDEX: [INDEX.md](INDEX.md)")
    lines.append("")

    all_failures = [f for r in results for f in r.get("failures") or []]
    if all_failures:
        lines.append("## Failures / skips")
        lines.append("")
        for f in all_failures:
            lines.append(
                f"- **{f.get('gallery')}** `{f.get('type_id')}` "
                f"({f.get('pack')}): {f.get('reason')}"
            )
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {path}")
    return path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--only",
        action="append",
        dest="only",
        default=[],
        choices=sorted(GALLERY_SPECS.keys()),
        help="Only these galleries (repeatable): calc1, a1, a2, pc",
    )
    args = ap.parse_args()
    keys = args.only or list(GALLERY_SPECS.keys())

    results: list[dict[str, Any]] = []
    for key in keys:
        print(f"\n=== {key} ===")
        try:
            results.append(_build_gallery(key))
        except Exception as exc:  # noqa: BLE001
            print(f"GALLERY FAIL {key}: {exc}")
            results.append(
                {
                    "key": key,
                    "folder": GALLERY_SPECS[key]["folder"],
                    "html": None,
                    "topics_ok": 0,
                    "topics_total": 0,
                    "skipped": [],
                    "failures": [
                        {"gallery": key, "pack": "*", "type_id": "*", "reason": str(exc)}
                    ],
                    "samples_ok": 0,
                    "samples_err": 0,
                }
            )

    master = _write_master_index(results)
    print("\n=== DONE ===")
    for r in results:
        print(
            f"{r['key']}: topics {r['topics_ok']}/{r['topics_total']} · "
            f"samples {r['samples_ok']} ok / {r['samples_err']} err · "
            f"form_ids={r.get('distinct_form_ids', '?')} · "
            f"{r.get('html') or 'NO HTML'}"
        )
    print(f"master: {master.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
