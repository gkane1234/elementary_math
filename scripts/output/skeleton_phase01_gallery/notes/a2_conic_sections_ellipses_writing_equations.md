# Notes — `a2_conic_sections_ellipses_writing_equations`

> **LOW_VARIETY** — One template across seeds at D=0.

- **Display name:** Ellipses writing equations
- **Category:** Algebra 2 — Conic Sections
- **Generator:** `conic_sections`
- **Already on skeleton?** no
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice ellipses writing equations (catalog: conic_sections).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `(none — live default is old path)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Write the equation of an ellipse centered at the origin with }a=5\text{ and }b=2.$ | $\frac{x^2}{25}+\frac{y^2}{4}=1$ | — |
| 0 | 207 | $\text{Write the equation of an ellipse centered at the origin with }a=5\text{ and }b=4.$ | $\frac{x^2}{25}+\frac{y^2}{16}=1$ | — |
| 8 | 101 | $\text{Write the equation of an ellipse centered at }(1,-1)\text{ with }a=7\text{ and }b=3.$ | $\frac{(x-(1))^2}{49}+\frac{(y-(-1))^2}{9}=1$ | — |
| 8 | 207 | $\text{Write the equation of an ellipse centered at }(3,-2)\text{ with }a=7\text{ and }b=6.$ | $\frac{(x-(3))^2}{49}+\frac{(y-(-2))^2}{36}=1$ | — |
| 16 | 101 | $\text{Write the equation of an ellipse centered at }(-2,3)\text{ with }a=7\text{ and }b=8.$ | $\frac{(x-(-2))^2}{49}+\frac{(y-(3))^2}{64}=1$ | — |
| 16 | 207 | $\text{Write the equation of an ellipse centered at }(-2,-3)\text{ with }a=7\text{ and }b=6.$ | $\frac{(x-(-2))^2}{49}+\frac{(y-(-3))^2}{36}=1$ | — |
| 22 | 101 | $\text{Write the equation of an ellipse centered at }(-1,1)\text{ with }a=6\text{ and }b=10.$ | $\frac{(x-(-1))^2}{36}+\frac{(y-(1))^2}{100}=1$ | — |
| 22 | 207 | $\text{Write the equation of an ellipse centered at }(5,-4)\text{ with }a=11\text{ and }b=5.$ | $\frac{(x-(5))^2}{121}+\frac{(y-(-4))^2}{25}=1$ | — |

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
