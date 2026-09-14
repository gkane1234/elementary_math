# Notes — `a2_conic_sections_classifying`

> **LOW_VARIETY** — One template across seeds at D=0.

- **Display name:** Classifying
- **Category:** Algebra 2 — Conic Sections
- **Generator:** `conic_sections`
- **Already on skeleton?** no
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice classifying (catalog: conic_sections).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `(none — live default is old path)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Classify the conic: } \frac{x^2}{25}+\frac{y^2}{9}=1.$ | $ellipse$ | — |
| 0 | 207 | $\text{Classify the conic: } \frac{x^2}{25}+\frac{y^2}{4}=1.$ | $ellipse$ | — |
| 8 | 101 | $\text{Classify the conic: } \frac{x^2}{49}+\frac{y^2}{16}=1.$ | $ellipse$ | — |
| 8 | 207 | $\text{Classify the conic: } \frac{x^2}{16}+\frac{y^2}{4}=1.$ | $ellipse$ | — |
| 16 | 101 | $\text{Classify the conic: } \frac{x^2}{49}+\frac{y^2}{16}=1.$ | $ellipse$ | — |
| 16 | 207 | $\text{Classify the conic: } \frac{x^2}{64}+\frac{y^2}{9}=1.$ | $ellipse$ | — |
| 22 | 101 | $\text{Classify the conic: } \frac{x^2}{121}+\frac{y^2}{49}=1.$ | $ellipse$ | — |
| 22 | 207 | $\text{Classify the conic: } \frac{x^2}{25}+\frac{y^2}{4}=1.$ | $ellipse$ | — |

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

One template across seeds at D=0.
Flags: `LOW_VARIETY`.

## Limitations

Flags for gallery red header: `LOW_VARIETY`.

- **Variety:** one template / Mad-Lib across seeds at easy D — rotate OpenStax-derived frames or algebraic shapes before claiming shipped variety.
- **Difficulty scaling:** Variety thin at fixed D; D may still bump coeffs — check live ladder.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Existing `conic_sections` hand path until a skeleton exists.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `conic_sections`; equations/WP agent owns solve/WP siblings._
