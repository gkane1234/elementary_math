"""Inventory Calculus catalog leaves vs Diff/expr_skeleton + Precalc aliases.

Writes CALC_INDEX.md. Does not implement generators.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from question_engine.catalogs.calculus import CATALOG as CALC_CATALOG
from question_engine.catalogs.calculus import CATEGORY_ORDER as CALC_CATEGORY_ORDER
from question_engine.catalogs.precalculus import CATALOG as PC_CATALOG
from question_engine.core.base import QUESTION_TYPES
from question_engine.frameworks.primitives.derivatives import (
    _TYPE_ID_TO_GENERATOR as DERIV_TYPE_TO_GEN,
)
from question_engine.frameworks.primitives.expr_skeleton import FORM_PATTERNS
from question_engine.frameworks.primitives.openstax_form_catalogs import load_form_catalog

NOTES = Path(__file__).resolve().parent
GALLERY = NOTES.parent

DIFF_TOPICS = {
    "power_rule": "Power rule",
    "product_rule": "Product rule",
    "quotient_rule": "Quotient rule",
    "chain_rule": "Chain rule",
    "trigonometric": "Trigonometric",
    "ln_exp": "Exp / ln",
    "inverse_trig": "Inverse trig",
    "higher_order": "Higher order",
    "general": "General / mixed",
}

DIFF_GEN_TO_SLUG = {
    "derivative_power_rule": "power_rule",
    "derivative_product_rule": "product_rule",
    "derivative_quotient_rule": "quotient_rule",
    "derivative_chain_rule": "chain_rule",
    "derivative_trigonometric": "trigonometric",
    "derivative_ln_exp": "ln_exp",
    "derivative_inverse_trig": "inverse_trig",
    "derivative_higher_order": "higher_order",
    "derivative_general": "general",
}

CALC2_IDS = frozenset(
    {
        "calc_indef_int_trigonometric_with_substitution",
        "calc_indef_int_integration_by_parts",
        "calc_indef_int_partial_fractions",
        "calc_indef_int_multi_trick",
    }
)

PC_ALIAS = {
    "calc_limits_by_direct_evaluation": "pc_limits_by_direct_evaluation",
    "calc_limits_at_jump_discontinuities_and_kinks": "pc_limits_at_kinks_and_jumps",
    "calc_limits_at_removable_discontinuities": "pc_limits_at_removable_discontinuities",
    "calc_limits_at_essential_discontinuities": "pc_limits_at_essential_discontinuities",
    "calc_limits_at_infinity": "pc_limits_at_infinity",
    "calc_diff_definition_of_the_derivative": "pc_definition_of_the_derivative",
    "calc_diff_instantaneous_rates_of_change": "pc_instantaneous_rates_of_change",
    "calc_diff_power_rule": "pc_power_rule_for_differentiation",
    "calc_app_diff_motion_along_a_line": "pc_motion_along_a_line",
    "calc_def_int_approximating_area_under_a_curve": "pc_approximating_area_under_a_curve",
    "calc_def_int_area_under_a_curve_by_limit_of_sums": "pc_area_under_a_curve_by_limit_of_sums",
    "calc_indef_int_power_rule": "pc_indefinite_integrals",
    "calc_app_diff_limits_in_form_of_definition_of_derivative": "pc_definition_of_the_derivative",
}


def load_gallery() -> dict[str, dict]:
    path = GALLERY / "gen_examples.py"
    spec = importlib.util.spec_from_file_location("phase01_gen", path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    out: dict[str, dict] = {}
    for sec in mod.SECTIONS:
        tid = str(sec.get("type_id") or "")
        rec = {
            "slug": sec.get("slug"),
            "engine": sec.get("engine") or "",
            "pattern": sec.get("pattern") or "",
            "canonical": tid,
        }
        if tid:
            out.setdefault(tid, rec)
        for a in sec.get("aliases") or []:
            out.setdefault(str(a), rec)
    return out


def gen_on_diff(generator: str) -> bool:
    if generator not in DIFF_GEN_TO_SLUG:
        return False
    cat = load_form_catalog("derivatives")
    for form in cat.get("forms") or []:
        if not isinstance(form, dict):
            continue
        if form.get("generation_status") != "implemented":
            continue
        keys = form.get("generator_keys") or form.get("leaves") or []
        fid = str(form.get("form_id") or "")
        if generator in keys and fid in FORM_PATTERNS:
            return True
    return False


def family(type_id: str, category: str, on_diff: bool) -> str:
    if on_diff:
        return "diff"
    low = category.lower()
    if "limit" in low or "continuity" in low:
        return "limit"
    if "integration" in low:
        return "integral"
    if "differential equation" in low:
        return "de"
    # DE ids are calc_diff_eq_* — check before bare calc_diff_*.
    if type_id.startswith("calc_diff_eq_"):
        return "de"
    if type_id.startswith("calc_diff_"):
        return "diff"
    if type_id.startswith("calc_app_diff_"):
        return "other"
    if type_id.startswith(("calc_indef_int_", "calc_def_int_", "calc_app_int_")):
        return "integral"
    if type_id.startswith("calc_limits_") or type_id.startswith("calc_continuity_"):
        return "limit"
    return "other"


def is_diff_leaf(type_id: str) -> bool:
    """True for Differentiation leaves (excludes calc_diff_eq_* DE leaves)."""
    return type_id.startswith("calc_diff_") and not type_id.startswith("calc_diff_eq_")


def pc_alias(type_id: str, generator: str, by_gen: dict[str, list[str]]) -> str:
    if type_id in PC_ALIAS:
        return PC_ALIAS[type_id]
    hits = [h for h in by_gen.get(generator, []) if h.startswith("pc_")]
    intro = [
        h
        for h in hits
        if any(
            k in h
            for k in (
                "limit",
                "deriv",
                "integral",
                "motion",
                "area_under",
                "approximat",
                "instantaneous",
                "power_rule",
            )
        )
    ]
    pool = intro or hits
    return pool[0] if pool else ""


def notes_ok(type_id: str, slug: str | None) -> tuple[bool, str]:
    paths: list[Path] = []
    if slug:
        paths.append(NOTES / f"{slug}.md")
    paths.append(NOTES / f"{type_id}.md")
    alias = PC_ALIAS.get(type_id)
    if alias:
        paths.append(NOTES / f"{alias}.md")
    for path in paths:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        good = ("openstax.org" in text) and (
            ("What old path actually produced" in text)
            or ("What old / live path actually produced" in text)
            or ("Live `_generate_for_type`" in text)
            or ("Live `_generate_for_type`" in text)
        )
        if good:
            return True, path.name
    for path in paths:
        if path.is_file():
            return False, path.name
    return False, ""


def main() -> None:
    gal = load_gallery()
    by_gen: dict[str, list[str]] = {}
    for e in PC_CATALOG:
        by_gen.setdefault(e.generator, []).append(e.id)
    qt = set(QUESTION_TYPES.keys())

    rows: list[dict] = []
    for entry in CALC_CATALOG:
        gen = str(entry.generator or "")
        mapped = DERIV_TYPE_TO_GEN.get(entry.id, gen)
        on_diff = gen_on_diff(mapped)
        if not on_diff and gen_on_diff(gen):
            on_diff = True
            mapped = gen
        slug = DIFF_GEN_TO_SLUG.get(mapped, "") if on_diff else ""
        phase = gal.get(entry.id) or gal.get(gen)
        alias = pc_alias(entry.id, gen, by_gen)
        filled, nfile = notes_ok(entry.id, slug or None)
        rows.append(
            {
                "id": entry.id,
                "name": entry.name,
                "category": entry.category,
                "generator": gen,
                "mapped": mapped,
                "on_diff": on_diff,
                "slug": slug,
                "on_phase01": phase is not None,
                "family": family(entry.id, entry.category, on_diff),
                "pc": alias,
                "band": "Calc2" if entry.id in CALC2_IDS else "Calc1",
                "in_qt": entry.id in qt,
                "notes_ok": filled,
                "notes_file": nfile,
            }
        )

    n = len(rows)
    n_diff = sum(1 for r in rows if r["on_diff"])
    n_c1 = sum(1 for r in rows if r["band"] == "Calc1")
    n_c2 = sum(1 for r in rows if r["band"] == "Calc2")
    n_p01 = sum(1 for r in rows if r["on_phase01"])
    missing = [r["id"] for r in rows if not r["in_qt"]]

    lines: list[str] = [
        "# Calculus type index",
        "",
        "Inventory of question **type_ids** for Calculus.",
        "Setup-only: suggested engine family is a proposal, not a wiring change.",
        "Notes pass is **steps 1–3 only** (old path, `notes/<slug>.md`, OpenStax).",
        "Do **not** implement Calculus generators in this wave unless the leaf is",
        "already on Diff / `expr_skeleton` (then notes/gallery only).",
        "",
        "## Course layout",
        "",
        "- **Single catalog:** `question_engine/catalogs/calculus.py`",
        "  (`COURSE_ID = \"calculus\"`). No `calculus_1` / `calculus_2` catalog modules.",
        "- **`lib/curriculum.ts`:** one `calculus` level (Limits → DE).",
        "- **Settings:** many calc leaves use `setting_profile=\"derivatives\"` in",
        "  `question_engine/settings/generator_profiles.py`; presets under",
        "  `\"derivatives\"` in `presets.py` / `domains/calculus.py`.",
        "- **Diff live path:** `generators/calculus_derivative_rules.py` →",
        "  `frameworks/primitives/derivatives.py` → `expr_skeleton` when the",
        "  OpenStax form_id is in `FORM_PATTERNS`. Gallery:",
        "  `scripts/output/diff_skeleton_gallery/`.",
        "",
        "## Counts",
        "",
        "| Source | Count |",
        "|---|---:|",
        f"| Catalog (`question_engine/catalogs/calculus.py`) = Calculus `QUESTION_TYPES` leaves | {n} |",
        f"| Heuristic **Calc1** band (Vol 1 / AB spine) | {n_c1} |",
        f"| Heuristic **Calc2** band (technique-heavy integration) | {n_c2} |",
        f"| Already on **Diff** `expr_skeleton` (live + `diff_skeleton_gallery`) | {n_diff} |",
        f"| Already on phase-01 gallery (`skeleton_phase01_gallery` SECTIONS) | {n_p01} |",
        "",
        "**Already-on-Diff-skeleton** = catalog leaf whose generator is one of the",
        "nine Diff gallery topics **and** has implemented `derivatives.json` forms",
        "mapped in `expr_skeleton.FORM_PATTERNS` (power / product / quotient / chain /",
        "trig / ln·exp / invtrig / higher_order / general).",
        "",
        "**Calc2 heuristic** (inside the unified catalog) =",
        "`calc_indef_int_trigonometric_with_substitution`,",
        "`calc_indef_int_integration_by_parts`,",
        "`calc_indef_int_partial_fractions`,",
        "`calc_indef_int_multi_trick`. All other leaves are tagged Calc1-band.",
        "",
        "Engine family is one of: `diff` / `limit` / `integral` / `de` / `other`",
        "(proposal only; differs from G6–PA’s number/affine/solve set).",
        "",
        "Also checked: `lib/curriculum.ts`, `question_engine/core/registry.py`,",
        "`QUESTION_TYPES`, `question_engine/settings/`, Diff gallery,",
        "`derivatives.py` `_TYPE_ID_TO_GENERATOR`, Precalc intro-to-calc aliases.",
        "",
    ]

    if missing:
        lines += ["## `QUESTION_TYPES` gaps", "", "Catalog ids missing from `QUESTION_TYPES`:", ""]
        lines += [f"- `{tid}`" for tid in missing]
        lines.append("")
    else:
        lines += [
            "## `QUESTION_TYPES` vs catalog",
            "",
            "Every Calculus catalog `id` is registered in `QUESTION_TYPES`.",
            "",
        ]

    lines += [
        "## Already on Diff `expr_skeleton`",
        "",
        f"These Differentiation leaves are live on Diff / `expr_skeleton` ({n_diff} / {n}).",
        "Per-leaf notes already exist for all Diff leaves when backfill is complete.",
        "",
        "| type_id | display name | generator | diff gallery slug | Precalc alias |",
        "|---|---|---|---|---|",
    ]
    for r in rows:
        if not r["on_diff"]:
            continue
        pc = f"`{r['pc']}`" if r["pc"] else "—"
        lines.append(
            f"| `{r['id']}` | {r['name']} | `{r['mapped']}` | `{r['slug']}` | {pc} |"
        )
    lines.append("")

    filled = [r for r in rows if r["on_diff"] and r["notes_ok"]]
    miss = [r for r in rows if r["on_diff"] and not r["notes_ok"]]
    lines += [
        "### Notes backfill (already-on-Diff)",
        "",
        "Filled if notes have an `openstax.org` cite **and** a live old-path section",
        "(`What old / live path actually produced` or `Live `_generate_for_type``).",
        "",
        f"Filled: **{len(filled)}** / {n_diff}. Still need backfill: **{len(miss)}**.",
        "",
    ]
    if miss:
        lines += ["| type_id | suggested notes slug | existing file |", "|---|---|---|"]
        for r in miss:
            lines.append(
                f"| `{r['id']}` | `{r['slug'] or r['id']}` | {r['notes_file'] or '—'} |"
            )
        lines.append("")

    lines += [
        "## Differentiation leaves **not** on Diff skeleton yet",
        "",
        "Still Differentiation `calc_diff_*` (excludes `calc_diff_eq_*` DE leaves),",
        "but not in the nine expr_skeleton gallery topics (or forms are stub-only).",
        "",
        "| type_id | display name | generator | suggested family | notes |",
        "|---|---|---|---|---|",
    ]
    stubs = {"derivative_implicit", "derivative_logarithmic"}
    for r in rows:
        if not is_diff_leaf(r["id"]) or r["on_diff"]:
            continue
        if r["generator"] in stubs:
            note = "stub forms"
        elif r["generator"] == "derivative_other_base":
            note = "other_base / not in Diff gallery"
        else:
            note = "other path"
        lines.append(
            f"| `{r['id']}` | {r['name']} | `{r['generator']}` | {r['family']} | {note} |"
        )
    lines.append("")

    lines += [
        "## Precalc intro-to-calc aliases",
        "",
        "Precalculus Introduction-to-Calculus leaves sharing a generator or explicit",
        "skill pair with a Calculus leaf. See `PRECALC_INDEX.md`.",
        "",
        "| calc type_id | Precalc alias | shared generator | on Diff? |",
        "|---|---|---|---|",
    ]
    for r in rows:
        if not r["pc"]:
            continue
        lines.append(
            f"| `{r['id']}` | `{r['pc']}` | `{r['generator']}` | "
            f"{'yes' if r['on_diff'] else 'no'} |"
        )
    lines.append("")

    lines += [
        "## Calculus catalog",
        "",
        "| type_id | display name | band | already-on-Diff? | suggested engine family | Precalc alias |",
        "|---|---|---|---|---|---|",
    ]
    by_cat: dict[str, list[dict]] = {}
    for r in rows:
        by_cat.setdefault(r["category"], []).append(r)
    for cat in CALC_CATEGORY_ORDER:
        if cat not in by_cat:
            continue
        lines.append(f"|  | **{cat}** |  |  |  |  |")
        for r in by_cat[cat]:
            pc = f"`{r['pc']}`" if r["pc"] else "—"
            lines.append(
                f"| `{r['id']}` | {r['name']} | {r['band']} | "
                f"{'yes' if r['on_diff'] else 'no'} | {r['family']} | {pc} |"
            )
    for cat, items in by_cat.items():
        if cat in CALC_CATEGORY_ORDER:
            continue
        lines.append(f"|  | **{cat}** |  |  |  |  |")
        for r in items:
            pc = f"`{r['pc']}`" if r["pc"] else "—"
            lines.append(
                f"| `{r['id']}` | {r['name']} | {r['band']} | "
                f"{'yes' if r['on_diff'] else 'no'} | {r['family']} | {pc} |"
            )

    lines += [
        "",
        "## Appendix — generator keys",
        "",
        "| type_id | catalog generator | Diff-mapped generator |",
        "|---|---|---|",
    ]
    for r in rows:
        mapped = f"`{r['mapped']}`" if r["mapped"] != r["generator"] else "—"
        lines.append(f"| `{r['id']}` | `{r['generator']}` | {mapped} |")

    lines += [
        "",
        "## Appendix — Diff gallery topics",
        "",
        "From `scripts/output/diff_skeleton_gallery/gen_examples.py` `TOPICS`:",
        "",
        "| slug | display | generator key |",
        "|---|---|---|",
    ]
    inv = {v: k for k, v in DIFF_GEN_TO_SLUG.items()}
    for slug, title in DIFF_TOPICS.items():
        lines.append(f"| `{slug}` | {title} | `{inv.get(slug, '')}` |")

    lines += [
        "",
        "Per-type notes: copy `_TEMPLATE.md` → `notes/<gallery-slug>.md` (or",
        "`<type_id>.md`). Process: `.cursor/rules/topic-notes-process.mdc`,",
        "`benchmark-old-path.mdc`, `regenerate-galleries.mdc`,",
        "`gallery-html-katex.mdc`.",
        "",
    ]

    out = NOTES / "CALC_INDEX.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(
        f"Wrote {out} | total={n} Calc1={n_c1} Calc2={n_c2} "
        f"on_diff={n_diff} phase01={n_p01}"
    )
    print("on_diff:", [r["id"] for r in rows if r["on_diff"]])


if __name__ == "__main__":
    main()
