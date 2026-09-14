"""Inventory Algebra 2 + Precalc catalog leaves vs phase-01 gallery skeletons.

Writes ``A2_INDEX.md`` and ``PRECALC_INDEX.md``. Does not implement generators.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[4]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from question_engine.catalogs.algebra_1 import CATALOG as A1_CATALOG
from question_engine.catalogs.algebra_2 import CATALOG as A2_CATALOG, CATEGORY_ORDER as A2_CATEGORY_ORDER
from question_engine.catalogs.precalculus import CATALOG as PC_CATALOG, CATEGORY_ORDER as PC_CATEGORY_ORDER
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


def a1_by_generator() -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    for entry in A1_CATALOG:
        out.setdefault(entry.generator, []).append(entry.id)
    return out


def a1_alias_for(type_id: str, generator: str, gal: dict | None, gen_to_a1: dict[str, list[str]]) -> str:
    """Best A1 (or shared unprefixed) alias when this leaf reuses an A1 skeleton."""
    if gal:
        canon = str(gal.get("canonical") or "")
        if canon and not canon.startswith(("a2_", "pc_")):
            return canon
    if generator in gen_to_a1:
        ids = gen_to_a1[generator]
        if len(ids) == 1:
            return ids[0]
        # Prefer the id that matches generator name when multiple share a generator.
        if generator in ids:
            return generator
        return ids[0]
    if not type_id.startswith(("a2_", "pc_")):
        return ""
    return ""


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
        if eng in mapping:
            return mapping[eng]
        if "Solve" in pat or "Inequality" in pat or "Abs" in pat or "Compound" in pat:
            return "solve"
        if "Factor" in pat or "Poly" in pat:
            return "other"
        if "Cancel" in pat:
            return "other"

    tid = type_id
    if tid.endswith("_word_problems") or "word_problems" in tid:
        return "wp"
    if any(
        k in tid
        for k in (
            "_equations",
            "_inequalities",
            "absolute_value",
            "compound_",
            "literal_",
            "radical_equations",
            "rational_equations",
            "logarithmic_equations",
            "trig_equations",
        )
    ):
        return "solve"
    if "simplifying_algebraic" in tid or "order_of_operations" in tid:
        return tid.endswith("order_of_operations") and "number" or "affine"
    if "order_of_operations" in tid:
        return "number"
    if "trigonometry" in category.lower() or tid.startswith(("a2_trigonometry", "pc_")) and any(
        x in tid for x in ("right_triangle", "law_of_", "angle", "radian", "trig_")
    ):
        return "geometry"
    if "Probability" in category or "Discrete Mathematics" in category:
        return "other"
    if "Matrices" in category or "Vectors" in category or "Three-Dimensional" in category:
        return "other"
    if "Introduction to Calculus" in category:
        return "other"
    return "other"


def notes_status(type_id: str, gal: dict | None) -> tuple[str, str]:
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
    if has_os and has_old:
        return "ok", found.name
    return "stub", found.name


def inventory_catalog(
    catalog: tuple,
    category_order: tuple[str, ...],
    course_label: str,
    prefix: str,
    sections: list[dict],
    gal_map: dict[str, dict],
    gallery_type_ids: set[str],
    gen_to_a1: dict[str, list[str]],
) -> tuple[list[dict], str]:
    rows = []
    for entry in catalog:
        gal = gal_map.get(entry.id)
        gen_is_gallery = entry.generator in gallery_type_ids
        on_skel = gal is not None or gen_is_gallery
        if gal is None and gen_is_gallery:
            gal = gal_map.get(entry.generator)
        a1_alias = a1_alias_for(entry.id, entry.generator, gal, gen_to_a1)
        thin_a1 = bool(on_skel and a1_alias and entry.id.startswith(prefix))
        fam = engine_family(entry.id, entry.category, on_skel, gal)
        nstat, npath = notes_status(entry.id, gal)
        rows.append(
            {
                "id": entry.id,
                "name": entry.name,
                "category": entry.category,
                "generator": entry.generator,
                "on_skel": on_skel,
                "family": fam,
                "a1_alias": a1_alias,
                "thin_a1": thin_a1,
                "notes": nstat,
                "notes_file": npath,
                "slug": (gal or {}).get("slug") or "",
                "in_qt": entry.id in QUESTION_TYPES,
            }
        )

    on_n = sum(1 for r in rows if r["on_skel"])
    thin_n = [r for r in rows if r["thin_a1"]]

    lines = [
        f"# {course_label} type index",
        "",
        f"Inventory of question **type_ids** for {course_label}.",
        "Setup-only: suggested engine family is a proposal, not a wiring change.",
        "Notes pass is **steps 1–3 only** (old path, `notes/<slug>.md`, OpenStax).",
        f"Do not implement {course_label} generators in this wave unless the leaf is already on a skeleton.",
        "",
        "## Counts",
        "",
        f"| Source | {'A2' if prefix == 'a2_' else 'Precalc'} |",
        "|---|---:|",
        f"| Catalog (`question_engine/catalogs/{'algebra_2' if prefix == 'a2_' else 'precalculus'}.py`) = {course_label} `QUESTION_TYPES` leaves | {len(rows)} |",
        f"| Already on a phase-01 skeleton (gallery `type_id` / alias, or catalog generator is a gallery type) | {on_n} |",
        f"| Thin A1 aliases (prefixed id on skeleton via shared A1/unprefixed canonical) | {len(thin_n)} |",
        "",
        "**Already-on-skeleton** = yes if the leaf is a `SECTIONS` `type_id` or alias in",
        "`scripts/output/skeleton_phase01_gallery/gen_examples.py`, **or** its catalog",
        "`generator` is itself a gallery type (shared family already on that engine).",
        "",
        "**A1 alias** = unprefixed (or A1-catalog) `type_id` whose skeleton engine this leaf",
        "reuses — gallery alias, or same `generator=` as an A1 catalog entry already on skeleton.",
        "",
        "Engine family is one of: `number` / `affine` / `solve` / `wp` / `proportion` / `geometry` / `other`.",
        "",
        "Also checked: `lib/curriculum.ts`, `question_engine/core/registry.py`,",
        "`QUESTION_TYPES`, `question_engine/settings/` (including `domains/`),",
        "`question_engine/generators/`.",
        "",
    ]

    if thin_n:
        lines.extend(
            [
                "## Thin A1 skeleton aliases",
                "",
                "These prefixed leaves are already on a phase-01 skeleton by alias or shared",
                "`generator=` with an A1 (or unprefixed shared) canonical. Notes/process follow",
                "the A1 gallery slug unless the A2/PC old path diverges.",
                "",
                "| type_id | display name | A1 alias | gallery slug | engine family |",
                "|---|---|---|---|---|",
            ]
        )
        for r in thin_n:
            lines.append(
                f"| `{r['id']}` | {r['name']} | `{r['a1_alias']}` | `{r['slug'] or '—'}` | {r['family']} |"
            )
        lines.append("")

    filled_sk = [r for r in rows if r["on_skel"] and r["notes"] == "ok"]
    miss_n = [r for r in rows if r["on_skel"] and r["notes"] != "ok"]
    lines.extend(
        [
            "## Notes backfill (already-on-skeleton)",
            "",
            "Already-skeletoned leaves still need notes before wiring changes.",
            "A notes file counts as filled if it has an `openstax.org` cite **and** a",
            "`What old path actually produced` section (same skip rule as `_sample_pa.py`).",
            "",
            f"Filled: **{len(filled_sk)}** / {on_n}. Still need backfill: **{len(miss_n)}**.",
            "",
        ]
    )
    if miss_n:
        lines.append("| type_id | gallery slug | notes status | existing file |")
        lines.append("|---|---|---|---|")
        for r in miss_n:
            lines.append(
                f"| `{r['id']}` | `{r['slug'] or '—'}` | {r['notes']} | {r['notes_file'] or '—'} |"
            )
        lines.append("")
    if filled_sk:
        lines.append("Filled already-on-skeleton notes:")
        lines.append("")
        lines.append("| type_id | gallery slug | notes file |")
        lines.append("|---|---|---|")
        for r in filled_sk:
            lines.append(f"| `{r['id']}` | `{r['slug'] or '—'}` | `{r['notes_file']}` |")
        lines.append("")

    by_cat: dict[str, list] = {}
    for r in rows:
        by_cat.setdefault(r["category"], []).append(r)

    lines.append(f"## {course_label} catalog")
    lines.append("")
    lines.append(
        "| type_id | display name | already-on-skeleton? | suggested engine family | A1 alias |"
    )
    lines.append("|---|---|---|---|---|")

    extra_cats = [c for c in by_cat if c not in category_order]
    for cat in list(category_order) + extra_cats:
        recs = by_cat.get(cat)
        if not recs:
            continue
        lines.append(f"|  | **{cat}** |  |  |  |")
        for r in recs:
            yes = "yes" if r["on_skel"] else "no"
            alias = f"`{r['a1_alias']}`" if r["a1_alias"] else "—"
            lines.append(f"| `{r['id']}` | {r['name']} | {yes} | {r['family']} | {alias} |")

    qt_missing = [r["id"] for r in rows if not r["in_qt"]]
    diffs = [r for r in rows if r["generator"] != r["id"]]

    lines.extend(
        [
            "",
            "## Appendix — not extra catalog leaves",
            "",
            "### Generator keys that differ from catalog `id`",
            "",
        ]
    )
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
        lines.append(
            "Catalog ids **not** registered in `QUESTION_TYPES`: "
            + ", ".join(f"`{t}`" for t in qt_missing)
            + "."
        )
    else:
        lines.append(f"Every {course_label} catalog `id` is registered in `QUESTION_TYPES`.")
    lines.extend(
        [
            "",
            "Per-type notes: copy `_TEMPLATE.md` → `notes/<gallery-slug>.md` (or",
            "`<type_id>.md` / `<slug>/NOTES.md`). Process: `.cursor/rules/topic-notes-process.mdc`.",
            "",
        ]
    )

    fname = "A2_INDEX.md" if prefix == "a2_" else "PRECALC_INDEX.md"
    return rows, "\n".join(lines), fname


def main() -> None:
    sections = _load_sections()
    gal_map = gallery_ids(sections)
    gallery_type_ids = {str(s.get("type_id") or "") for s in sections}
    gallery_type_ids |= {str(a) for s in sections for a in (s.get("aliases") or [])}
    gen_to_a1 = a1_by_generator()

    summaries = []
    for catalog, order, label, prefix in (
        (A2_CATALOG, A2_CATEGORY_ORDER, "Algebra 2", "a2_"),
        (PC_CATALOG, PC_CATEGORY_ORDER, "Precalculus", "pc_"),
    ):
        rows, text, fname = inventory_catalog(
            catalog, order, label, prefix, sections, gal_map, gallery_type_ids, gen_to_a1
        )
        out = NOTES / fname
        out.write_text(text, encoding="utf-8")
        on_n = sum(1 for r in rows if r["on_skel"])
        thin_n = sum(1 for r in rows if r["thin_a1"])
        summaries.append((label, len(rows), on_n, thin_n, fname))
        print(f"wrote {out}")
        print(f"  {label} count: {len(rows)}, skeletoned: {on_n}, thin A1 aliases: {thin_n}")

    print("\nSummary:")
    for label, total, on_n, thin_n, fname in summaries:
        print(f"  {label}: {total} types, {on_n} on skeleton, {thin_n} thin A1 aliases -> {fname}")


if __name__ == "__main__":
    main()
