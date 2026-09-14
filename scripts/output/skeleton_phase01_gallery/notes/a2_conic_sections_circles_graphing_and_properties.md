# Notes — `a2_conic_sections_circles_graphing_and_properties`

> **UNCLEAR / LOW_VARIETY / NOT_IMPLEMENTED** — Circle graph vs standard form — College Algebra §11.1.

- **Display name:** Circles graphing & properties
- **Category:** Algebra 2 — Conic Sections
- **Generator:** `conic_sections`
- **Already on skeleton?** no
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice circles graphing & properties (catalog: conic_sections).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `(none — live default is old path)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $x^2+y^2=16$ | $\text{center }(0,0),\ \text{radius }4$ | — |
| 0 | 207 | $x^2+y^2=16$ | $\text{center }(0,0),\ \text{radius }4$ | — |
| 8 | 101 | $(x-(1))^2+(y-(3))^2=9$ | $\text{center }(1,3),\ \text{radius }3$ | — |
| 8 | 207 | $(x-(1))^2+(y-(2))^2=36$ | $\text{center }(1,2),\ \text{radius }6$ | — |
| 16 | 101 | $(x-(4))^2+(y-(-2))^2=36$ | $\text{center }(4,-2),\ \text{radius }6$ | — |
| 16 | 207 | $(x-(3))^2+(y-(5))^2=49$ | $\text{center }(3,5),\ \text{radius }7$ | — |
| 22 | 101 | $(x-(3))^2+(y-(-3))^2=49$ | $\text{center }(3,-3),\ \text{radius }7$ | — |
| 22 | 207 | $(x-(2))^2+(y-(4))^2=25$ | $\text{center }(2,4),\ \text{radius }5$ | — |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| College Algebra 2e §11.1 | https://openstax.org/books/college-algebra-2e/pages/11-1-distance-and-midpoint-formulas-circles | 11.1 Distance and Midpoint Formulas; Circles |
| College Algebra 2e §11.2 | https://openstax.org/books/college-algebra-2e/pages/11-2-parabolas | 11.2 Parabolas |
| College Algebra 2e §11.3 | https://openstax.org/books/college-algebra-2e/pages/11-3-ellipses | 11.3 Ellipses |

Local HTML (if mined): `textbooks/openstax/html/intermediate-algebra-2e/` or `college-algebra-2e/`.

## Variety notes / UNCLEAR flag

Circle graph vs standard form — College Algebra §11.1.
Flags: `UNCLEAR`, `LOW_VARIETY`.

## Limitations

Flags for gallery red header: `NOT_IMPLEMENTED`, `UNCLEAR`, `LOW_VARIETY`.

- **Not implemented on an algebraic skeleton** — graph / figure engine outside SolveLinear / poly / rational cores; leave leaf until a graph core can match OpenStax shapes honestly (`benchmark-old-path` skip).
- **Why stubbed:** live old path may still sample, but gold (transforms, asymptotes, focus/directrix, amplitude/period, shading) is not locked — red-header gallery only.
- **Variety:** one template / Mad-Lib across seeds at easy D — rotate OpenStax-derived frames or algebraic shapes before claiming shipped variety.
- **Difficulty scaling:** Variety thin at fixed D; D may still bump coeffs — check live ladder.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Existing `conic_sections` hand path until a skeleton exists.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `conic_sections`; equations/WP agent owns solve/WP siblings._
