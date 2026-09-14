# Notes — `a2_polynomial_functions_factoring_all_techniques`

> **UNCLEAR** — A2 type_id samples differ from A1 alias at same D/seeds — verify intended divergence.

- **Display name:** Factoring all techniques
- **Category:** Algebra 2 — Polynomial Functions
- **Generator:** `a2_polynomial_functions_factoring_all_techniques`
- **Already on skeleton?** yes (`factor_all_techniques`)
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice factoring all techniques (catalog: a2_polynomial_functions_factoring_all_techniques).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `{"use_factor_poly": true}`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $x^{2} + 7x + 12$ | $\left(x + 3\right)\left(x + 4\right)$ | — |
| 0 | 207 | $x^{3} - 1$ | $\left(x - 1\right)\left(x^{2} + x + 1\right)$ | — |
| 8 | 101 | $2x^{2} - 13x + 18$ | $\left(x - 2\right)\left(2x - 9\right)$ | — |
| 8 | 207 | $x^{3} + 1$ | $\left(x + 1\right)\left(x^{2} - x + 1\right)$ | — |
| 16 | 101 | $7x^{2} - 10x + 6 - 3x^{2}$ | $2\left(x - 1\right)\left(2x - 3\right)$ | — |
| 16 | 207 | $1 - 2x^{3} + 3x^{3}$ | $\left(x + 1\right)\left(x^{2} - x + 1\right)$ | — |
| 22 | 101 | $22x^{2} - 7x - 3x + 6$ | $2\left(x - 1\right)\left(2x - 3\right)$ | — |
| 22 | 207 | $1 + 4y^{3} + 2y^{3} - 5y^{3}$ | $\left(y + 1\right)\left(y^{2} - y + 1\right)$ | — |

Opt-out flag used: `{"use_factor_poly": true}`

## A1 alias comparison

- **A1 catalog twin:** `polynomial_factoring_general_strategy` (same generator `a2_polynomial_functions_factoring_all_techniques` unless noted).
- **Note:** A2 mixer pool may include cubes/grouping beyond A1 general strategy.
- **Old path vs A1:** Differs from A1 alias at some D/seeds — see samples; verify catalog intent.
  - D=0.0 seed=101: A2 `x^{2} + 7x + 12` ≠ A1 `3x^{3} + 3x^{2} + 4x + 4`
  - D=0.0 seed=207: A2 `x^{3} - 1` ≠ A1 `x^{2} - 4`
  - D=8.0 seed=101: A2 `2x^{2} - 13x + 18` ≠ A1 `x^{2} + 2x - 3`
  - D=8.0 seed=207: A2 `x^{3} + 1` ≠ A1 `x^{2} + 2x + 1`
  - D=16.0 seed=207: A2 `1 - 2x^{3} + 3x^{3}` ≠ A1 `10x^{2} - 90x + 77 + 3`
  - D=22.0 seed=207: A2 `1 + 4y^{3} + 2y^{3} - 5y^{3}` ≠ A1 `10y^{2} - 90y + 82 + 1 - 3`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| Intermediate Algebra 2e §5.1 | https://openstax.org/books/intermediate-algebra-2e/pages/5-1-add-and-subtract-polynomials | 5.1 Add and Subtract Polynomials — e.g. Example 5.1: Determine whether each polynomial is a monomial, binomial, trinomial, or other polynomial. Then, find the degree of each polynomial. ⓐ $7 y^{2} - 5 y + 3$ ⓑ $−2 a^{4} b^{2}$ ⓒ $3 x^{5} - 4 x^{3} - …; Example 5.2: Add or subtract: ⓐ $25 y^{2} + 15 y^{2}$ ⓑ $16 p q^{3} - \left(\right. −7 p q^{3} \left.\right) .$ |
| Intermediate Algebra 2e §5.3 | https://openstax.org/books/intermediate-algebra-2e/pages/5-3-multiply-polynomials | 5.3 Multiply Polynomials — e.g. Example 5.25: Multiply: ⓐ $\left(\right. 3 x^{2} \left.\right) \left(\right. −4 x^{3} \left.\right)$ ⓑ $\left(\right. \frac{5}{6} x^{3} y \left.\right) \left(\right. 12 x y^{2} \left.\right) .$; Example 5.26: Multiply: ⓐ $−2 y \left(\right. 4 y^{2} + 3 y - 5 \left.\right)$ ⓑ $3 x^{3} y \left(\right. x^{2} - 8 x y + y^{2} \left.\right) .$ |
| Intermediate Algebra 2e §5.4 | https://openstax.org/books/intermediate-algebra-2e/pages/5-4-dividing-polynomials | 5.4 Divide Polynomials — e.g. Example 5.36: Find the quotient: $54 a^{2} b^{3} \div \left(\right. −6 a b^{5} \left.\right) .$; Example 5.37: Find the quotient: $\frac{14 x^{7} y^{12}}{21 x^{11} y^{6}} .$ |

Local HTML (if mined): `textbooks/openstax/html/intermediate-algebra-2e/` or `college-algebra-2e/`.

## Variety notes / UNCLEAR flag

A2 type_id samples differ from A1 alias at same D/seeds — verify intended divergence.
Flags: `UNCLEAR`.

## Limitations

Flags for gallery red header: `UNCLEAR`.

- **UNCLEAR gold:** old path and OpenStax skill intent diverge, or dump/wrong-skill shapes — do not wire a new core until notes lock.
- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Existing skeleton slug `factor_all_techniques` / shared `a2_polynomial_functions_factoring_all_techniques` family.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `a2_polynomial_functions_factoring_all_techniques`; equations/WP agent owns solve/WP siblings._
