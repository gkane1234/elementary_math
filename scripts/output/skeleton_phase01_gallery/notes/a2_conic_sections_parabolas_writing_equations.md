# Notes — `a2_conic_sections_parabolas_writing_equations`

> **LOW_VARIETY** — One template across seeds at D=0.

- **Display name:** Parabolas writing equations
- **Category:** Algebra 2 — Conic Sections
- **Generator:** `quadratic_vertex_form_write`
- **Already on skeleton?** no
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice parabolas writing equations (catalog: quadratic_vertex_form_write).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `(none — live default is old path)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Write the equation in vertex form for a parabola with vertex } (2, 0) \text{ and } a = 1.$ | $(x - 2)^2$ | — |
| 0 | 207 | $\text{Write the equation in vertex form for a parabola with vertex } (2, 2) \text{ and } a = 1.$ | $(x - 2)^2 + 2$ | — |
| 8 | 101 | $\text{Write the equation in vertex form for a parabola with vertex } (-4, -1) \text{ and } a = 2.$ | $2(x + 4)^2 - 1$ | — |
| 8 | 207 | $\text{Write the equation in vertex form for a parabola with vertex } (1, -2) \text{ and } a = -2.$ | $-2(x - 1)^2 - 2$ | — |
| 16 | 101 | $\text{Write the equation in vertex form for a parabola with vertex } (4, 4) \text{ and } a = 3.$ | $3(x - 4)^2 + 4$ | — |
| 16 | 207 | $\text{Write the equation in vertex form for a parabola with vertex } (-3, -6) \text{ and } a = -3.$ | $-3(x + 3)^2 - 6$ | — |
| 22 | 101 | $\text{Write the equation in vertex form for a parabola with vertex } (1, -2) \text{ and } a = -3.$ | $-3(x - 1)^2 - 2$ | — |
| 22 | 207 | $\text{Write the equation in vertex form for a parabola with vertex } (-4, 1) \text{ and } a = 3.$ | $3(x + 4)^2 + 1$ | — |

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

- **Reuse:** Existing `quadratic_vertex_form_write` hand path until a skeleton exists.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `quadratic_vertex_form_write`; equations/WP agent owns solve/WP siblings._
