"""Add ## Limitations to all A2 notes; create missing notes; list stub needs.

Does not regenerate galleries — run gen_examples.py after.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from question_engine.catalogs.algebra_2 import CATALOG as A2_CATALOG  # noqa: E402

NOTES = Path(__file__).resolve().parent
SUMMARY = NOTES / "_a2_summary.json"

# Type_ids that are graph / figure / spatial-display heavy (stub, not algebraic core).
GRAPH_TYPE_SUBSTR = (
    "_graphing_",
    "_graphing",
    "graphing_",
    "numbers_graphing",
    "expressions_graphing",
    "functions_graphing",
    "end_behavior_and_general_graph_shape",
    "solving_equations_by_graphing",
    "solving_systems_by_graphing",
    "graphing_and_properties",
    "matrix_geometric_transformations",
    "points_in_three_dimensions",
    "systems_of_equations_and_inequalities_planes",
)

# Thin A1 aliases that should point at shared gallery notes (not a2_*.md).
# Still ensure a2-named notes exist for type_id-first lookup when stubbed.
MISSING_NOTE_OPENSTAX: dict[str, tuple[str, str, str]] = {
    # type_id -> (cite, url, shape)
    "a2_matrices_cramers_rule": (
        "OpenStax Intermediate Algebra 2e §4.6 (systems; Cramer's Rule is CA/supplement)",
        "https://openstax.org/books/intermediate-algebra-2e/pages/4-6-solve-systems-of-equations-using-matrices",
        "2×2 / 3×3 Cramer's Rule determinants — not locked to IA matrix chapter alone",
    ),
    "a2_matrices_equations": (
        "OpenStax Intermediate Algebra 2e §4.6",
        "https://openstax.org/books/intermediate-algebra-2e/pages/4-6-solve-systems-of-equations-using-matrices",
        "Matrix equations AX=B — gold vs ops leaf still separate",
    ),
    "a2_quadratic_functions_and_inequalities_solving_equations_by_graphing": (
        "OpenStax Intermediate Algebra 2e §9.5",
        "https://openstax.org/books/intermediate-algebra-2e/pages/9-5-solve-quadratic-equations-in-one-variable-using-the-square-root-property",
        "Solve by graphing / intercepts — graph engine; algebraic cores do not cover",
    ),
    "a2_quadratic_functions_and_inequalities_solving_equations_by_taking_square_roots": (
        "OpenStax Intermediate Algebra 2e §9.1",
        "https://openstax.org/books/intermediate-algebra-2e/pages/9-1-solve-quadratic-equations-using-the-square-root-property",
        "Isolate then ±√; a≠1 later",
    ),
    "a2_quadratic_functions_and_inequalities_solving_equations_by_factoring": (
        "OpenStax Intermediate Algebra 2e §6.5",
        "https://openstax.org/books/intermediate-algebra-2e/pages/6-5-general-strategy-for-factoring-polynomials",
        "Factor then zero-product",
    ),
    "a2_quadratic_functions_and_inequalities_solving_equations_by_completing_the_square": (
        "OpenStax Intermediate Algebra 2e §9.2",
        "https://openstax.org/books/intermediate-algebra-2e/pages/9-2-solve-quadratic-equations-by-completing-the-square",
        "CTS solve path",
    ),
    "a2_quadratic_functions_and_inequalities_solving_equations_with_the_quadratic_formula": (
        "OpenStax Intermediate Algebra 2e §9.3",
        "https://openstax.org/books/intermediate-algebra-2e/pages/9-3-solve-quadratic-equations-using-the-quadratic-formula",
        "Quadratic formula",
    ),
    "a2_polynomial_functions_solving_polynomial_equations": (
        "OpenStax Intermediate Algebra 2e §6.5 / §9.5",
        "https://openstax.org/books/intermediate-algebra-2e/pages/6-5-general-strategy-for-factoring-polynomials",
        "Factor polynomial equations (may alias quadratic factor-to-solve)",
    ),
    "a2_radical_functions_and_rational_exponents_radical_equations": (
        "OpenStax Intermediate Algebra 2e §8.6",
        "https://openstax.org/books/intermediate-algebra-2e/pages/8-6-solve-radical-equations",
        "Isolate radical then square",
    ),
    "a2_radical_functions_and_rational_exponents_rational_exponent_equations": (
        "OpenStax Intermediate Algebra 2e §8.6",
        "https://openstax.org/books/intermediate-algebra-2e/pages/8-6-solve-radical-equations",
        "Rational-exponent equations (often shares radical_equations generator)",
    ),
    "a2_conic_sections_systems_of_quadratic_equations": (
        "OpenStax Intermediate Algebra 2e §11.1–11.4 (conics) + systems",
        "https://openstax.org/books/intermediate-algebra-2e/pages/11-1-distance-and-midpoint-formulas-and-circles",
        "Quadratic systems — graph + algebra; no honest single core yet",
    ),
    "a2_exponential_and_logarithmic_expressions_exponential_equations_not_requiring_logarithms": (
        "OpenStax Intermediate Algebra 2e §10.2",
        "https://openstax.org/books/intermediate-algebra-2e/pages/10-2-evaluate-and-graph-exponential-functions",
        "Same-base exponential equations",
    ),
    "a2_exponential_and_logarithmic_expressions_exponential_equations_requiring_logarithms": (
        "OpenStax Intermediate Algebra 2e §10.5",
        "https://openstax.org/books/intermediate-algebra-2e/pages/10-5-solve-exponential-and-logarithmic-equations",
        "Take log both sides",
    ),
    "a2_exponential_and_logarithmic_expressions_logarithmic_equations_simple": (
        "OpenStax Intermediate Algebra 2e §10.5",
        "https://openstax.org/books/intermediate-algebra-2e/pages/10-5-solve-exponential-and-logarithmic-equations",
        "Simple log equations",
    ),
    "a2_exponential_and_logarithmic_expressions_logarithmic_equations_hard": (
        "OpenStax Intermediate Algebra 2e §10.5",
        "https://openstax.org/books/intermediate-algebra-2e/pages/10-5-solve-exponential-and-logarithmic-equations",
        "Harder log equations (extraneous / multi-log)",
    ),
    "a2_trigonometry_equations": (
        "OpenStax College Algebra 2e §8.1 / Precalculus §7",
        "https://openstax.org/books/college-algebra-2e/pages/8-1-graphs-of-the-sine-and-cosine-functions",
        "Simple trig equations — variety/OpenStax lock TBD",
    ),
    "a2_probability_and_statistics_probability_of_independent_and_dependent_events_word_problems": (
        "OpenStax Statistics / Elementary Algebra probability applications",
        "https://openstax.org/books/statistics/pages/3-1-terminology",
        "WP frames for independent/dependent — LOW_VARIETY risk if one Mad-Lib",
    ),
    "a2_probability_and_statistics_probability_of_mutually_exclusive_events_word_problems": (
        "OpenStax Statistics Ch 3",
        "https://openstax.org/books/statistics/pages/3-1-terminology",
        "WP frames for mutually exclusive events",
    ),
}


def _load_flags() -> dict[str, list[str]]:
    if not SUMMARY.is_file():
        return {}
    data = json.loads(SUMMARY.read_text(encoding="utf-8"))
    return dict(data.get("flags") or {})


def _banner_flags(txt: str) -> list[str]:
    m = re.search(r"^>\s*\*\*([^*]+)\*\*", txt, re.M)
    if not m:
        return []
    raw = m.group(1)
    out: list[str] = []
    for tok in ("UNCLEAR", "LOW_VARIETY", "LIMITATIONS", "NOT_IMPLEMENTED"):
        if tok in raw:
            out.append(tok)
    return out


def _is_graphing(tid: str, txt: str) -> bool:
    low = tid.lower()
    if any(h in low for h in GRAPH_TYPE_SUBSTR):
        return True
    # Bare "..._graphing" suffix (e.g. a2_polynomial_functions_graphing)
    if low.endswith("_graphing") or low.endswith("_graph"):
        return True
    head = txt[:800].lower()
    return (
        "graph engine outside" in head
        or "graphing-only" in head
        or "no skeleton core yet" in head
        or "no algebraic skeleton" in head
    )


def _openstax_gap(txt: str) -> str | None:
    """Heuristic: OpenStax table cites wrong chapter family vs skill."""
    if "OpenStax" not in txt and "openstax.org" not in txt:
        return "No OpenStax cite yet — fill chapter/section + URL."
    # binomial theorem notes citing add/subtract poly
    if "binomial_theorem" in txt and "5.1 Add and Subtract" in txt:
        return "OpenStax cite points at §5.1 add/subtract — need binomial / Pascal (§5.4 or CA) shapes."
    return None


def _d_scaling_note(txt: str) -> str:
    table = re.search(
        r"## What old path actually produced.*?\| D \|.*?\n(?:\|[^\n]+\n){2,}(.*?)(?:\n\n|\nOpt-out)",
        txt,
        re.S,
    )
    if not table:
        return "Old-path D ladder not recorded — confirm D=0 simple vs D≈16–22 hardness."
    body = table.group(0)
    prompts = re.findall(r"\| 0 \|.*?\| (\$[^|]+\$)", body)
    prompts16 = re.findall(r"\| 16 \|.*?\| (\$[^|]+\$)", body)
    if prompts and prompts16 and prompts[0] == prompts16[0]:
        return "D-scaling may be flat — D=0 and D=16 prompts look identical in notes samples."
    if "One template across seeds" in txt or "LOW_VARIETY" in txt:
        return "Variety thin at fixed D; D may still bump coeffs — check live ladder."
    return "D ladder present in notes; verify numeric hardness before format unlocks."


def _limitations_block(
    tid: str,
    txt: str,
    flags: list[str],
    *,
    create: bool = False,
) -> str:
    graph = _is_graphing(tid, txt)
    banner = _banner_flags(txt)
    all_flags = list(dict.fromkeys([*banner, *flags]))
    ox = _openstax_gap(txt)
    lines: list[str] = ["## Limitations", ""]

    tokens: list[str] = []
    if graph and "UNCLEAR" not in all_flags:
        tokens.append("UNCLEAR")
    if graph:
        tokens.append("NOT_IMPLEMENTED")
    if create and not all_flags:
        tokens.append("LIMITATIONS")
    for t in ("UNCLEAR", "LOW_VARIETY", "NOT_IMPLEMENTED", "LIMITATIONS"):
        if t in all_flags and t not in tokens:
            tokens.append(t)
    if tokens:
        lines.append(
            "Flags for gallery red header: "
            + ", ".join(f"`{t}`" for t in tokens)
            + "."
        )
        lines.append("")

    bullets: list[str] = []
    if graph:
        bullets.append(
            "**Not implemented on an algebraic skeleton** — graph / figure engine "
            "outside SolveLinear / poly / rational cores; leave leaf until a graph "
            "core can match OpenStax shapes honestly (`benchmark-old-path` skip)."
        )
        bullets.append(
            "**Why stubbed:** live old path may still sample, but gold "
            "(transforms, asymptotes, focus/directrix, amplitude/period, shading) "
            "is not locked — red-header gallery only."
        )
    if "LOW_VARIETY" in all_flags or "One template" in txt:
        bullets.append(
            "**Variety:** one template / Mad-Lib across seeds at easy D — rotate "
            "OpenStax-derived frames or algebraic shapes before claiming shipped variety."
        )
    if "UNCLEAR" in all_flags and not graph:
        bullets.append(
            "**UNCLEAR gold:** old path and OpenStax skill intent diverge, or dump/"
            "wrong-skill shapes — do not wire a new core until notes lock."
        )
    bullets.append(f"**Difficulty scaling:** {_d_scaling_note(txt)}")
    if ox:
        bullets.append(f"**OpenStax gap:** {ox}")
    else:
        bullets.append(
            "**OpenStax:** cites present — confirm section matches the skill "
            "(not a neighboring chapter dump)."
        )
    if "figure" in txt.lower() and "diagram" not in txt.lower()[:500]:
        bullets.append(
            "**Diagram:** figure/stimulus may be named in answers — verify SVG/"
            "stimulus actually renders on worksheets."
        )
    if create:
        bullets.append(
            "**Notes backfill:** created as stub; paste live old-path LaTeX at "
            "D=0/8/16/22 before any engine work."
        )

    for b in bullets:
        lines.append(f"- {b}")
    lines.append("")
    return "\n".join(lines)


def _insert_or_replace_limitations(txt: str, block: str) -> str:
    if re.search(r"^##\s+Limitations\b", txt, re.M):
        return re.sub(
            r"^##\s+Limitations\b.*?(?=^##\s|\Z)",
            block.rstrip() + "\n\n",
            txt,
            count=1,
            flags=re.M | re.S,
        )
    # Insert before Proposed engine, else Variety notes, else append
    m = re.search(r"^##\s+Proposed engine\b", txt, re.M)
    if m:
        return txt[: m.start()] + block + "\n" + txt[m.start() :]
    m = re.search(r"^##\s+Variety notes", txt, re.M)
    if m:
        # after variety section — find next ## or end
        nxt = re.search(r"^##\s+", txt[m.end() :], re.M)
        if nxt:
            pos = m.end() + nxt.start()
            return txt[:pos] + "\n" + block + txt[pos:]
        return txt.rstrip() + "\n\n" + block
    return txt.rstrip() + "\n\n" + block


def _ensure_banner_tokens(txt: str, need: list[str]) -> str:
    """Ensure graphing stubs show UNCLEAR / NOT_IMPLEMENTED in the lead quote."""
    if not need:
        return txt
    m = re.search(r"^>\s*\*\*([^*]+)\*\*\s*—\s*(.*)$", txt, re.M)
    if m:
        existing = m.group(1)
        parts = [p.strip() for p in re.split(r"[·/,]", existing) if p.strip()]
        # normalize tokens
        tokens = []
        for p in parts:
            up = p.upper().replace(" ", "_")
            if up in ("UNCLEAR", "LOW_VARIETY", "LIMITATIONS", "NOT_IMPLEMENTED"):
                if up not in tokens:
                    tokens.append(up)
            else:
                # keep non-token prose out of flag slot
                pass
        for t in need:
            if t not in tokens:
                tokens.append(t)
        if not tokens:
            tokens = list(need)
        label = " / ".join(tokens)
        rest = m.group(2).strip()
        # strip duplicate flag words from rest
        for t in tokens:
            rest = re.sub(rf"\b{t}\b", "", rest, flags=re.I)
        rest = re.sub(r"\s{2,}", " ", rest).strip(" —;")
        new_line = f"> **{label}** — {rest}" if rest else f"> **{label}** — see Limitations."
        return txt[: m.start()] + new_line + txt[m.end() :]
    # insert after title
    lines = txt.splitlines()
    if lines and lines[0].startswith("#"):
        insert = "> **" + " / ".join(need) + "** — see Limitations.\n"
        return lines[0] + "\n\n" + insert + "\n" + "\n".join(lines[1:]) + (
            "\n" if txt.endswith("\n") else ""
        )
    return (
        "> **"
        + " / ".join(need)
        + "** — see Limitations.\n\n"
        + txt
    )


def _create_stub_note(entry, flags: list[str]) -> str:
    tid = entry.id
    cite, url, shape = MISSING_NOTE_OPENSTAX.get(
        tid,
        (
            "OpenStax Intermediate Algebra 2e (section TBD)",
            "https://openstax.org/books/intermediate-algebra-2e/pages/1-introduction",
            "Shape TBD from live old path",
        ),
    )
    graph = _is_graphing(tid, tid)
    lead_flags = []
    if graph:
        lead_flags = ["UNCLEAR", "NOT_IMPLEMENTED"]
    elif "UNCLEAR" in flags:
        lead_flags = ["UNCLEAR"]
    elif "LOW_VARIETY" in flags:
        lead_flags = ["LOW_VARIETY"]
    else:
        lead_flags = ["LIMITATIONS"]
    lead = " / ".join(lead_flags)
    body = f"""# Notes — `{tid}`

> **{lead}** — Gallery stub; Limitations below. Live old-path samples not yet pasted.

- **Display name:** {entry.name}
- **Category:** {entry.category}
- **Generator:** `{entry.generator}`
- **Already on skeleton?** no (stub gallery)
- **Suggested family:** other

---

## What the question should look like (D=0 vs high D)

- **Skill:** {entry.name} (catalog: `{entry.generator}`).
- **D=0:** As simple as old easy — paste live samples below before wiring.
- **High D (≈16–22):** Numeric hardness first; format unlocks later.
- **Must not:** Wrong-topic shapes; equation dumps on WP leaves.

## What old path actually produced (real latex, D=0/8/16/22)

_Live `_generate_for_type` samples TBD — do not invent TeX._

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 |  |  |  |  |
| 8 |  |  |  |  |
| 16 |  |  |  |  |
| 22 |  |  |  |  |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| {cite} | {url} | {shape} |

## Variety notes / UNCLEAR flag

Stub notes for gallery Limitations header. Flags: {", ".join(f"`{f}`" for f in lead_flags)}.

"""
    body += _limitations_block(tid, body, flags, create=True)
    body += """## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Existing catalog generator / A1 alias if any — proposal only.
- **New:** only if no honest match; otherwise leave the leaf.
- **Not this pass:** stub gallery + Limitations only.
"""
    return body


def main() -> None:
    flag_map = _load_flags()
    by_id = {e.id: e for e in A2_CATALOG}
    updated = 0
    created = 0

    for entry in A2_CATALOG:
        tid = entry.id
        path = NOTES / f"{tid}.md"
        flags = list(flag_map.get(tid) or [])
        if not path.is_file():
            path.write_text(_create_stub_note(entry, flags), encoding="utf-8")
            created += 1
            continue
        txt = path.read_text(encoding="utf-8")
        need_banner: list[str] = []
        if _is_graphing(tid, txt):
            need_banner = ["UNCLEAR", "NOT_IMPLEMENTED"]
        txt2 = _ensure_banner_tokens(txt, need_banner) if need_banner else txt
        block = _limitations_block(tid, txt2, flags)
        txt3 = _insert_or_replace_limitations(txt2, block)
        if txt3 != txt:
            path.write_text(txt3, encoding="utf-8")
            updated += 1

    # Also patch a2_* notes that aren't catalog? all catalog covered.
    print(f"updated Limitations: {updated}")
    print(f"created stub notes: {created}")
    print(f"catalog size: {len(by_id)}")


if __name__ == "__main__":
    main()
