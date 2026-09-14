# Notes — `a2_conic_sections_hyperbolas_graphing_and_properties`

> **UNCLEAR / NOT_IMPLEMENTED** — Hyperbola graph engine TBD vs CA §11.3.

- **Display name:** Hyperbolas graphing & properties
- **Category:** Algebra 2 — Conic Sections
- **Generator:** `conic_sections`
- **Already on skeleton?** no
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice hyperbolas graphing & properties (catalog: conic_sections).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `(none — live default is old path)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\frac{y^2}{9}-\frac{x^2}{16}=1$ | $a=3,\ b=4,\ \text{vertical}$ | — |
| 0 | 207 | $\frac{x^2}{9}-\frac{y^2}{9}=1$ | $a=3,\ b=3,\ \text{horizontal}$ | — |
| 8 | 101 | $\frac{y^2}{36}-\frac{x^2}{9}=1$ | $a=6,\ b=3,\ \text{vertical}$ | — |
| 8 | 207 | $\frac{x^2}{36}-\frac{y^2}{49}=1$ | $a=6,\ b=7,\ \text{horizontal}$ | — |
| 16 | 101 | $\frac{y^2}{25}-\frac{x^2}{49}=1$ | $a=5,\ b=7,\ \text{vertical}$ | — |
| 16 | 207 | $\frac{x^2}{25}-\frac{y^2}{16}=1$ | $a=5,\ b=4,\ \text{horizontal}$ | — |
| 22 | 101 | $\frac{y^2}{121}-\frac{x^2}{25}=1$ | $a=11,\ b=5,\ \text{vertical}$ | — |
| 22 | 207 | $\frac{x^2}{100}-\frac{y^2}{121}=1$ | $a=10,\ b=11,\ \text{horizontal}$ | — |

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

Hyperbola graph engine TBD vs CA §11.3.
Flags: `UNCLEAR`.

## Limitations

Flags for gallery red header: `NOT_IMPLEMENTED`, `UNCLEAR`.

- **Not implemented on an algebraic skeleton** — graph / figure engine outside SolveLinear / poly / rational cores; leave leaf until a graph core can match OpenStax shapes honestly (`benchmark-old-path` skip).
- **Why stubbed:** live old path may still sample, but gold (transforms, asymptotes, focus/directrix, amplitude/period, shading) is not locked — red-header gallery only.
- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Existing `conic_sections` hand path until a skeleton exists.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `conic_sections`; equations/WP agent owns solve/WP siblings._
