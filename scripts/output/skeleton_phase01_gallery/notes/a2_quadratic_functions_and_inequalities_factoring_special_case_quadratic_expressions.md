# Notes — `a2_quadratic_functions_and_inequalities_factoring_special_case_quadratic_expressions`

> **LOW_VARIETY / UNCLEAR** — One template across seeds at D=0.

- **Display name:** Factoring special case quadratic expressions
- **Category:** Algebra 2 — Quadratic Functions and Inequalities
- **Generator:** `polynomial_factoring_special_cases`
- **Already on skeleton?** yes (`factor_special`)
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice factoring special case quadratic expressions (catalog: polynomial_factoring_special_cases).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `{"use_factor_poly": true}`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $x^{2} - 9$ | $\left(x + 3\right)\left(x - 3\right)$ | — |
| 0 | 207 | $x^{2} - 1$ | $\left(x + 1\right)\left(x - 1\right)$ | — |
| 8 | 101 | $4x^{2} - 36$ | $4\left(x + 3\right)\left(x - 3\right)$ | — |
| 8 | 207 | $x^{2} + 6x + 9$ | $\left(x + 3\right)^{2}$ | — |
| 16 | 101 | $3 - 39 + 4x^{2}$ | $4\left(x + 3\right)\left(x - 3\right)$ | — |
| 16 | 207 | $3x^{2} - 2x^{2} + 9 + 6x$ | $\left(x + 3\right)^{2}$ | — |
| 22 | 101 | $7x^{2} - 3x^{2} + 1 - 37$ | $4\left(x + 3\right)\left(x - 3\right)$ | — |
| 22 | 207 | $5x^{2} + 6x + 9 - 2x^{2} - 2x^{2}$ | $\left(x + 3\right)^{2}$ | — |

Opt-out flag used: `{"use_factor_poly": true}`

## A1 alias comparison

- **A1 catalog twin:** `polynomial_factoring_special_cases` (same generator `polynomial_factoring_special_cases` unless noted).
- **Old path vs A1:** Differs from A1 alias at some D/seeds — see samples; verify catalog intent.
  - D=0.0 seed=101: A2 `x^{2} - 9` ≠ A1 `x^{2} - 16`
  - D=8.0 seed=101: A2 `4x^{2} - 36` ≠ A1 `x^{2} - 49`
  - D=8.0 seed=207: A2 `x^{2} + 6x + 9` ≠ A1 `x^{2} - 9`
  - D=16.0 seed=101: A2 `3 - 39 + 4x^{2}` ≠ A1 `-3x^{2} + 4x^{2} - 49`
  - D=16.0 seed=207: A2 `3x^{2} - 2x^{2} + 9 + 6x` ≠ A1 `-x^{2} - 11 + 2\left(x^{2} + 1\right)`
  - D=22.0 seed=101: A2 `7x^{2} - 3x^{2} + 1 - 37` ≠ A1 `3 - 54 + 2 + x^{2}`
  - D=22.0 seed=207: A2 `5x^{2} + 6x + 9 - 2x^{2} - 2x^{2}` ≠ A1 `x^{2} - 11 + 2x^{2} - 2\left(x^{2} - 1\right)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| Intermediate Algebra 2e §9.6 | https://openstax.org/books/intermediate-algebra-2e/pages/9-6-graph-quadratic-functions-using-properties | 9.6 Graph Quadratic Functions Using Properties — e.g. Example 9.42: Graph $f (x) = x^{2} - 1 .$; Example 9.43: Determine whether each parabola opens upward or downward: ⓐ $f (x) = −3 x^{2} + 2 x - 4$ ⓑ $f (x) = 6 x^{2} + 7 x - 9 .$ |
| Intermediate Algebra 2e §9.2 | https://openstax.org/books/intermediate-algebra-2e/pages/9-2-solve-quadratic-equations-by-completing-the-square | 9.2 Solve Quadratic Equations by Completing the Square — e.g. Example 9.11: Complete the square to make a perfect square trinomial. Then write the result as a binomial squared. ⓐ $x^{2} - 26 x$ ⓑ $y^{2} - 9 y$ ⓒ $n^{2} + \frac{1}{2} n$; Example 9.12: How to Solve a Quadratic Equation of the Form $x^{2} + b x + c = 0$ by Completing the Square Solve by completing the square: $x^{2} + 8 x = 48 .$ |

Local HTML (if mined): `textbooks/openstax/html/intermediate-algebra-2e/` or `college-algebra-2e/`.

## Variety notes / UNCLEAR flag

One template across seeds at D=0.
Flags: `LOW_VARIETY`, `UNCLEAR`.

## Limitations

Flags for gallery red header: `UNCLEAR`, `LOW_VARIETY`.

- **Variety:** one template / Mad-Lib across seeds at easy D — rotate OpenStax-derived frames or algebraic shapes before claiming shipped variety.
- **UNCLEAR gold:** old path and OpenStax skill intent diverge, or dump/wrong-skill shapes — do not wire a new core until notes lock.
- **Difficulty scaling:** Variety thin at fixed D; D may still bump coeffs — check live ladder.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Existing skeleton slug `factor_special` / shared `polynomial_factoring_special_cases` family.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `polynomial_factoring_special_cases`; equations/WP agent owns solve/WP siblings._
