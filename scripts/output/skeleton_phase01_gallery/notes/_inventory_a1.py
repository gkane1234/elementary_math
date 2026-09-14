"""Inventory Algebra 1 catalog leaves vs phase-01 gallery skeletons + notes.

Writes ``A1_INDEX.md``. Does not implement generators.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[4]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from question_engine.catalogs.algebra_1 import CATALOG, CATEGORY_ORDER
from question_engine.core.base import QUESTION_TYPES

NOTES = Path(__file__).resolve().parent
GALLERY = NOTES.parent


def _load_sections() -> list[dict]:
    ge_path = GALLERY / "gen_examples.py"
    spec = importlib.util.spec_from_file_location("phase01_gen_examples", ge_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {ge_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return list(mod.SECTIONS)


def gallery_ids(sections: list[dict]) -> dict[str, dict]:
    """type_id or alias → section record."""
    out: dict[str, dict] = {}
    for sec in sections:
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


def engine_family(type_id: str, category: str, on_skel: bool, gal: dict | None) -> str:
    """Suggested family (proposal only). Prefer gallery engine when already on skeleton."""
    if gal:
        eng = str(gal.get("engine") or "")
        pat = str(gal.get("pattern") or "")
        mapping = {
            "equation_skeleton": "solve",
            "compound_inequalities": "solve",
            "rational_skeleton": "other",
            "poly_skeleton": "other",
            "construct_poly": "other",
            "affine_skeleton": "affine",
            "wp_packaging": "wp",
            "geometry_skeleton": "geometry",
            "geometry_reuse": "geometry",
            "number": "number",
            "number_reuse": "number",
            "percent_wp": "wp",
            "interest_wp": "wp",
            "linear_forms": "other",
            "systems": "other",
            "plotting_points": "geometry",
        }
        if type_id == "solving_proportions":
            return "proportion"
        if eng in mapping:
            return mapping[eng]
        if "Solve" in pat or "Inequality" in pat or "Abs" in pat or "Compound" in pat:
            return "solve"
        if "Factor" in pat or "Poly" in pat:
            return "other"
        if "Cancel" in pat:
            return "other"

    tid = type_id
    cat = category
    wp_ids = {
        "mixture_word_problems",
        "distance_rate_time_word_problems",
        "work_word_problems",
        "age_word_problems",
        "coin_word_problems",
        "consecutive_integers_word_problems",
        "percent_word_problems",
        "systems_word_problems",
        "exponential_growth_decay",
    }
    if tid in wp_ids or tid.endswith("_word_problems"):
        return "wp"
    if tid == "solving_proportions":
        return "proportion"
    if tid in {
        "one_step_equations",
        "two_step_equations",
        "multi_step_equations",
        "absolute_value_equations",
        "literal_equations",
        "one_step_inequalities",
        "two_step_inequalities",
        "multi_step_inequalities",
        "compound_inequalities",
        "absolute_value_inequalities",
        "rational_expressions_equations",
        "radical_equations",
        "quadratic_square_roots",
        "quadratic_factoring_equations",
        "quadratic_formula",
        "quadratic_completing_square_solve",
        "quadratic_completing_square_constant",
        "quadratic_discriminant",
    }:
        return "solve"
    if tid in {
        "verbal_expressions",
        "distributive_property",
        "simplify_polynomials",
    }:
        return "affine"
    if tid in {
        "order_of_operations",
        "sets_of_numbers",
        "rational_add_subtract",
        "rational_multiply",
        "rational_divide",
        "percents",
        "percent_of_change",
        "properties_of_exponents",
        "scientific_notation_write",
        "scientific_notation_operations",
        "scientific_notation_add_subtract",
    }:
        return "number"
    if tid in {
        "finding_sine_cosine_tangent",
        "finding_angles",
        "find_missing_sides_of_triangles",
        "radical_distance_formula",
        "radical_midpoint_formula",
    }:
        return "geometry"
    if "Trigonometry" in cat or "Statistics" in cat:
        return "geometry" if "Trigonometry" in cat else "other"
    return "other"


def notes_status(type_id: str, gal: dict | None) -> tuple[str, str]:
    """Return (status, path_or_reason). status: ok / missing / stub."""
    names = [type_id]
    if gal:
        slug = gal.get("slug")
        if slug:
            names.insert(0, str(slug))
        canon = gal.get("canonical")
        if canon and canon not in names:
            names.append(str(canon))
    paths = [NOTES / f"{n}.md" for n in names if n]
    if gal and gal.get("slug"):
        paths.append(GALLERY / str(gal["slug"]) / "NOTES.md")
    found = next((p for p in paths if p.is_file()), None)
    if found is None:
        return "missing", ""
    text = found.read_text(encoding="utf-8")
    has_os = "openstax.org" in text
    has_old = "What old path actually produced" in text
    rel = found.relative_to(NOTES.parent.parent.parent.parent) if False else found.name
    if has_os and has_old:
        return "ok", found.name
    return "stub", found.name


def main() -> None:
    sections = _load_sections()
    gal_map = gallery_ids(sections)
    gallery_type_ids = {str(s.get("type_id") or "") for s in sections}
    gallery_type_ids |= {
        str(a) for s in sections for a in (s.get("aliases") or [])
    }

    rows = []
    for entry in CATALOG:
        gal = gal_map.get(entry.id)
        gen_is_gallery = entry.generator in gallery_type_ids
        on_skel = gal is not None or gen_is_gallery
        if gal is None and gen_is_gallery:
            gal = gal_map.get(entry.generator)
        fam = engine_family(entry.id, entry.category, on_skel, gal)
        nstat, npath = notes_status(entry.id, gal)
        in_qt = entry.id in QUESTION_TYPES
        rows.append(
            {
                "id": entry.id,
                "name": entry.name,
                "category": entry.category,
                "subcategory": entry.subcategory,
                "generator": entry.generator,
                "on_skel": on_skel,
                "family": fam,
                "notes": nstat,
                "notes_file": npath,
                "slug": (gal or {}).get("slug") or "",
                "in_qt": in_qt,
            }
        )

    on_n = sum(1 for r in rows if r["on_skel"])
    miss_n = [r for r in rows if r["on_skel"] and r["notes"] != "ok"]
    stub_n = [r for r in rows if r["on_skel"] and r["notes"] == "stub"]
    missing_n = [r for r in rows if r["on_skel"] and r["notes"] == "missing"]
    qt_missing = [r["id"] for r in rows if not r["in_qt"]]

    lines = [
        "# Algebra 1 type index",
        "",
        "Inventory of question **type_ids** for Algebra 1.",
        "Setup-only: suggested engine family is a proposal, not a wiring change.",
        "Notes pass is **steps 1–3 only** (old path, `notes/<slug>.md`, OpenStax).",
        "Do not implement A1 generators in this wave unless the leaf is already on a skeleton.",
        "",
        "## Counts",
        "",
        "| Source | A1 |",
        "|---|---:|",
        f"| Catalog (`question_engine/catalogs/algebra_1.py`) = A1 `QUESTION_TYPES` leaves | {len(rows)} |",
        f"| Already on a phase-01 skeleton (gallery `type_id` / alias, or catalog generator is a gallery type) | {on_n} |",
        "",
        "**Already-on-skeleton** = yes if the leaf is a `SECTIONS` `type_id` or alias in",
        "`scripts/output/skeleton_phase01_gallery/gen_examples.py`, **or** its catalog",
        "`generator` is itself a gallery type (shared family already on that engine).",
        "",
        "Engine family is one of: `number` / `affine` / `solve` / `wp` / `proportion` / `geometry` / `other`.",
        "",
        "Also checked: `lib/curriculum.ts`, `question_engine/core/registry.py` (`ALGEBRA1_CATALOG`),",
        "`QUESTION_TYPES`. Catalog ids match the A1 curriculum tree; extras vs G6/PA shared ids",
        "are listed in the appendix.",
        "",
        "## Notes backfill (already-on-skeleton)",
        "",
        "Already-skeletoned leaves still need notes (may exist from the G6/PA wave).",
        "A notes file counts as filled if it has an `openstax.org` cite **and** a",
        "`What old path actually produced` section (same skip rule as `_sample_pa.py`).",
        "",
    ]

    filled_sk = [r for r in rows if r["on_skel"] and r["notes"] == "ok"]
    lines.append(
        f"Filled: **{len(filled_sk)}** / {on_n}. Still need backfill: **{len(miss_n)}**."
    )
    lines.append("")
    if miss_n:
        lines.append("| type_id | gallery slug | notes status | existing file |")
        lines.append("|---|---|---|---|")
        for r in miss_n:
            lines.append(
                f"| `{r['id']}` | `{r['slug'] or '—'}` | {r['notes']} | {r['notes_file'] or '—'} |"
            )
        lines.append("")
    lines.append("Gallery loads `notes/<slug>.md` first, then `notes/<type_id>.md`.")
    lines.append("")
    lines.append("Filled already-on-skeleton notes:")
    lines.append("")
    lines.append("| type_id | gallery slug | notes file |")
    lines.append("|---|---|---|")
    for r in filled_sk:
        lines.append(f"| `{r['id']}` | `{r['slug'] or '—'}` | `{r['notes_file']}` |")
    lines.append("")
    noskel_miss = [r for r in rows if not r["on_skel"] and r["notes"] != "ok"]
    noskel_ok = [r for r in rows if not r["on_skel"] and r["notes"] == "ok"]
    lines.append(
        f"Non-skeletoned A1 leaves: {len(noskel_ok)} already have notes; "
        f"{len(noskel_miss)} do not (fill when that leaf is taken up — no new engines)."
    )
    lines.append("")

    # Group by CATEGORY_ORDER then category as it appears
    by_cat: dict[str, list] = {}
    for r in rows:
        by_cat.setdefault(r["category"], []).append(r)

    lines.append("## Algebra 1 catalog")
    lines.append("")
    lines.append("| type_id | display name | already-on-skeleton? | suggested engine family |")
    lines.append("|---|---|---|---|")

    seen_cats = set()
    cat_order = list(CATEGORY_ORDER)
    extra_cats = [c for c in by_cat if c not in cat_order]
    for cat in cat_order + extra_cats:
        recs = by_cat.get(cat)
        if not recs:
            continue
        seen_cats.add(cat)
        lines.append(f"|  | **{cat}** |  |  |")
        last_sub = None
        for r in recs:
            sub = r.get("subcategory")
            if sub and sub != last_sub:
                lines.append(f"|  | *{cat} — {sub}* |  |  |")
                last_sub = sub
            yes = "yes" if r["on_skel"] else "no"
            lines.append(f"| `{r['id']}` | {r['name']} | {yes} | {r['family']} |")

    lines.extend(
        [
            "",
            "## Appendix — not extra catalog leaves",
            "",
            "### Shared with Pre-Algebra / G6 (A1 catalog owns the unprefixed id)",
            "",
            "These sit in `algebra_1.py` (often under a `Pre-Algebra — …` category) and also",
            "appear on the PA curriculum tree in `lib/curriculum.ts`. They are **A1 catalog",
            "leaves**, not extras. G6/PA notes may already exist under the same `type_id` or a",
            "gallery slug.",
            "",
        ]
    )

    shared = [
        r
        for r in rows
        if r["category"].startswith("Pre-Algebra")
        or r["id"]
        in {
            "verbal_expressions",
            "order_of_operations",
            "distributive_property",
            "one_step_equations",
            "two_step_equations",
            "graphing_single_variable_inequalities",
            "one_step_inequalities",
            "two_step_inequalities",
            "solving_proportions",
            "percents",
            "percent_of_change",
            "slope",
            "graphing_linear_equations",
            "writing_linear_equations",
            "graphing_linear_inequalities",
            "properties_of_exponents",
            "scientific_notation_write",
            "scientific_notation_operations",
            "radical_distance_formula",
            "radical_midpoint_formula",
            "visualizing_data",
            "center_and_spread",
            "scatter_plots",
        }
    ]
    lines.append(
        ", ".join(f"`{r['id']}`" for r in shared) + "."
    )
    lines.extend(
        [
            "",
            "### Generator keys that differ from catalog `id`",
            "",
            "Catalog `generator=` is a producer, not an extra picker type_id:",
            "",
        ]
    )
    diffs = [r for r in rows if r["generator"] != r["id"]]
    if diffs:
        lines.append("| type_id | generator |")
        lines.append("|---|---|")
        for r in diffs:
            lines.append(f"| `{r['id']}` | `{r['generator']}` |")
        lines.append("")
    else:
        lines.append("_None._")
        lines.append("")

    lines.extend(
        [
            "### `QUESTION_TYPES` vs catalog",
            "",
        ]
    )
    if qt_missing:
        lines.append("Catalog ids **not** registered in `QUESTION_TYPES`: " + ", ".join(f"`{t}`" for t in qt_missing) + ".")
    else:
        lines.append("Every A1 catalog `id` is registered in `QUESTION_TYPES`.")
    lines.extend(
        [
            "",
            "Per-type notes: copy `_TEMPLATE.md` → `notes/<gallery-slug>.md` (or",
            "`<type_id>.md` / `<slug>/NOTES.md`). Process: `.cursor/rules/topic-notes-process.mdc`.",
            "",
        ]
    )

    out = NOTES / "A1_INDEX.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out}")
    print(f"A1 type count: {len(rows)}")
    print(f"already-skeletoned: {on_n}")
    print(f"need notes backfill: {len(miss_n)}")
    print("missing:", [r["id"] for r in missing_n])
    print("stub:", [r["id"] for r in stub_n])
    print("filled:", [r["id"] for r in rows if r["on_skel"] and r["notes"] == "ok"])


if __name__ == "__main__":
    main()
