# Notes — `a2_polynomial_functions_adding_and_subtracting`

> **UNCLEAR** — A2 type_id samples differ from A1 alias at same D/seeds — verify intended divergence.

- **Display name:** Adding and subtracting
- **Category:** Algebra 2 — Polynomial Functions
- **Generator:** `polynomial_add_subtract`
- **Already on skeleton?** yes (`poly_add_sub`)
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice adding and subtracting (catalog: polynomial_add_subtract).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `{"use_sample_polynomial_add_subtract": true}`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Simplify: } \left(x^{2} + 2\right) + \left(2x^{2} + 2\right)$ | $3x^{2} + 4$ | form=poly_add |
| 0 | 207 | $\text{Simplify: } \left(2x^{2} + 3\right) + \left(-2x + 1\right)$ | $2x^{2} - 2x + 4$ | form=poly_add |
| 8 | 101 | $\text{Simplify: } \left(2x^{3} + x^{2} + 2\right) - \left(x^{2} + 2\right)$ | $2x^{3}$ | form=poly_subtract |
| 8 | 207 | $\text{Simplify: } \left(x^{3} + 2x^{2} + 2\right) - \left(3x^{3} + 3\right)$ | $-2x^{3} + 2x^{2} - 1$ | form=poly_subtract |
| 16 | 101 | $\text{Simplify: } \left(3x^{4} + 2x^{3} + x + 4\right) - \left(x^{4} + x^{2} + 1\right)$ | $2x^{4} + 2x^{3} - x^{2} + x + 3$ | form=poly_subtract |
| 16 | 207 | $\text{Simplify: } \left(x^{4} + 3x^{3} + x - 1\right) - \left(3x^{4} + 3x^{3} + 1\right)$ | $-2x^{4} + x - 2$ | form=poly_subtract |
| 22 | 101 | $\text{Simplify: } \left(3x^{4} + 2x^{3} + x + 4\right) - \left(x^{4} + x^{2} + 1\right)$ | $2x^{4} + 2x^{3} - x^{2} + x + 3$ | form=poly_subtract |
| 22 | 207 | $\text{Simplify: } \left(x^{4} + 3x^{3} + x - 1\right) - \left(3x^{4} + 3x^{3} + 1\right)$ | $-2x^{4} + x - 2$ | form=poly_subtract |

Opt-out flag used: `{"use_sample_polynomial_add_subtract": true}`

## A1 alias comparison

- **A1 catalog twin:** `polynomial_add_subtract` (same generator `polynomial_add_subtract` unless noted).
- **Old path vs A1:** Differs from A1 alias at some D/seeds — see samples; verify catalog intent.
  - D=8.0 seed=101: A2 `\text{Simplify: } \left(2x^{3} + x^{2} + 2\right) - \left(x^{2} + 2\right)` ≠ A1 `\text{Simplify: } \left(2x^{3} + x^{2} + 2\right) + \left(x^{2} + 2\right)`
  - D=16.0 seed=207: A2 `\text{Simplify: } \left(x^{4} + 3x^{3} + x - 1\right) - \left(3x^{4} + 3x^{3} +…` ≠ A1 `\text{Simplify: } \left(x^{4} + 3x^{3} + x - 1\right) + \left(3x^{4} + 3x^{3} +…`
  - D=22.0 seed=207: A2 `\text{Simplify: } \left(x^{4} + 3x^{3} + x - 1\right) - \left(3x^{4} + 3x^{3} +…` ≠ A1 `\text{Simplify: } \left(x^{4} + 3x^{3} + x - 1\right) + \left(3x^{4} + 3x^{3} +…`

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

- **Reuse:** Existing skeleton slug `poly_add_sub` / shared `polynomial_add_subtract` family.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `polynomial_add_subtract`; equations/WP agent owns solve/WP siblings._
