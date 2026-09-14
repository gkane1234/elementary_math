# Notes — `a2_polynomial_functions_conjugate_roots_and_writing_functions`

> **UNCLEAR / LOW_VARIETY** — Write poly from conjugate roots — A2-only generator `polynomial_conjugate_writing`.

- **Display name:** Conjugate roots & writing functions
- **Category:** Algebra 2 — Polynomial Functions
- **Generator:** `polynomial_conjugate_writing`
- **Already on skeleton?** no
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice conjugate roots & writing functions (catalog: polynomial_conjugate_writing).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `(none — live default is old path)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Write a monic quadratic with roots } 1 + 3i \text{ and } 1 - 3i.$ | $x^{2} - 2x + 10$ | — |
| 0 | 207 | $\text{Write a monic quadratic with roots } 2 + 3i \text{ and } 2 - 3i.$ | $x^{2} - 4x + 13$ | — |
| 8 | 101 | $\text{Write a monic quadratic with roots } -2 - 2i \text{ and } -2 + 2i.$ | $x^{2} + 4x + 8$ | — |
| 8 | 207 | $\text{Write a monic quadratic with roots } -5 - 3i \text{ and } -5 + 3i.$ | $x^{2} + 10x + 34$ | — |
| 16 | 101 | $\text{Write a monic quadratic with roots } -4 - 4i \text{ and } -4 + 4i.$ | $x^{2} + 8x + 32$ | — |
| 16 | 207 | $\text{Write a monic quadratic with roots } -5 - 1i \text{ and } -5 + 1i.$ | $x^{2} + 10x + 26$ | — |
| 22 | 101 | $\text{Write a monic quadratic with roots } -2 - 3i \text{ and } -2 + 3i.$ | $x^{2} + 4x + 13$ | — |
| 22 | 207 | $\text{Write a monic quadratic with roots } -5 - 2i \text{ and } -5 + 2i.$ | $x^{2} + 10x + 29$ | — |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| Intermediate Algebra 2e §5.1 | https://openstax.org/books/intermediate-algebra-2e/pages/5-1-add-and-subtract-polynomials | 5.1 Add and Subtract Polynomials — e.g. Example 5.1: Determine whether each polynomial is a monomial, binomial, trinomial, or other polynomial. Then, find the degree of each polynomial. ⓐ $7 y^{2} - 5 y + 3$ ⓑ $−2 a^{4} b^{2}$ ⓒ $3 x^{5} - 4 x^{3} - …; Example 5.2: Add or subtract: ⓐ $25 y^{2} + 15 y^{2}$ ⓑ $16 p q^{3} - \left(\right. −7 p q^{3} \left.\right) .$ |
| Intermediate Algebra 2e §5.3 | https://openstax.org/books/intermediate-algebra-2e/pages/5-3-multiply-polynomials | 5.3 Multiply Polynomials — e.g. Example 5.25: Multiply: ⓐ $\left(\right. 3 x^{2} \left.\right) \left(\right. −4 x^{3} \left.\right)$ ⓑ $\left(\right. \frac{5}{6} x^{3} y \left.\right) \left(\right. 12 x y^{2} \left.\right) .$; Example 5.26: Multiply: ⓐ $−2 y \left(\right. 4 y^{2} + 3 y - 5 \left.\right)$ ⓑ $3 x^{3} y \left(\right. x^{2} - 8 x y + y^{2} \left.\right) .$ |
| Intermediate Algebra 2e §5.4 | https://openstax.org/books/intermediate-algebra-2e/pages/5-4-dividing-polynomials | 5.4 Divide Polynomials — e.g. Example 5.36: Find the quotient: $54 a^{2} b^{3} \div \left(\right. −6 a b^{5} \left.\right) .$; Example 5.37: Find the quotient: $\frac{14 x^{7} y^{12}}{21 x^{11} y^{6}} .$ |

Local HTML (if mined): `textbooks/openstax/html/intermediate-algebra-2e/` or `college-algebra-2e/`.

## Variety notes / UNCLEAR flag

Write poly from conjugate roots — A2-only generator `polynomial_conjugate_writing`.
Flags: `UNCLEAR`, `LOW_VARIETY`.

## Limitations

Flags for gallery red header: `UNCLEAR`, `LOW_VARIETY`.

- **Variety:** one template / Mad-Lib across seeds at easy D — rotate OpenStax-derived frames or algebraic shapes before claiming shipped variety.
- **UNCLEAR gold:** old path and OpenStax skill intent diverge, or dump/wrong-skill shapes — do not wire a new core until notes lock.
- **Difficulty scaling:** Variety thin at fixed D; D may still bump coeffs — check live ladder.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Existing `polynomial_conjugate_writing` hand path until a skeleton exists.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `polynomial_conjugate_writing`; equations/WP agent owns solve/WP siblings._
