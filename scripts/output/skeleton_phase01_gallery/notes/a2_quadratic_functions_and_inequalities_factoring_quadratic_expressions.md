# Notes — `a2_quadratic_functions_and_inequalities_factoring_quadratic_expressions`

> **LOW_VARIETY / UNCLEAR** — One template across seeds at D=0.

- **Display name:** Factoring quadratic expressions
- **Category:** Algebra 2 — Quadratic Functions and Inequalities
- **Generator:** `quadratic_factoring`
- **Already on skeleton?** yes (`factor_quadratic`)
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice factoring quadratic expressions (catalog: quadratic_factoring).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `{"use_factor_poly": true}`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $x^{2} + 7x + 12$ | $\left(x + 3\right)\left(x + 4\right)$ | — |
| 0 | 207 | $x^{2} + 3x + 2$ | $\left(x + 1\right)\left(x + 2\right)$ | — |
| 8 | 101 | $4x^{2} - 24x + 32$ | $4\left(x - 2\right)\left(x - 4\right)$ | — |
| 8 | 207 | $2x^{2} - 18x + 16$ | $2\left(x - 1\right)\left(x - 8\right)$ | — |
| 16 | 101 | $2\left(-24x + 32\right) + 8x^{2}$ | $8\left(x - 2\right)\left(x - 4\right)$ | — |
| 16 | 207 | $-2\left(-x^{2} + 6x - 9\right)$ | $2\left(x - 3\right)\left(x - 3\right)$ | — |
| 22 | 101 | $8x^{2} + 3x^{2} - 3x^{2} + 64 - 48x$ | $8\left(x - 2\right)\left(x - 4\right)$ | — |
| 22 | 207 | $-3\left(x^{2} + 1\right) + 3x^{2} + 2x^{2} - 12x + 21$ | $2\left(x - 3\right)\left(x - 3\right)$ | — |

Opt-out flag used: `{"use_factor_poly": true}`

## A1 alias comparison

- **A1 catalog twin:** `quadratic_factoring` (same generator `quadratic_factoring` unless noted).
- **Old path vs A1:** Differs from A1 alias at some D/seeds — see samples; verify catalog intent.
  - D=0.0 seed=101: A2 `x^{2} + 7x + 12` ≠ A1 `x^{2} + 6x + 8`
  - D=0.0 seed=207: A2 `x^{2} + 3x + 2` ≠ A1 `x^{2} + 4x + 3`
  - D=8.0 seed=101: A2 `4x^{2} - 24x + 32` ≠ A1 `x^{2} + 2x - 8`
  - D=8.0 seed=207: A2 `2x^{2} - 18x + 16` ≠ A1 `x^{2} - 3x + 2`
  - D=16.0 seed=101: A2 `2\left(-24x + 32\right) + 8x^{2}` ≠ A1 `2\left(-28x + 32\right) + 12x^{2}`
  - D=16.0 seed=207: A2 `-2\left(-x^{2} + 6x - 9\right)` ≠ A1 `-x^{2} + 3x^{2} + 12 - 14x`
  - D=22.0 seed=101: A2 `8x^{2} + 3x^{2} - 3x^{2} + 64 - 48x` ≠ A1 `-2\left(-6x^{2}\right) + 64 - 56x`
  - D=22.0 seed=207: A2 `-3\left(x^{2} + 1\right) + 3x^{2} + 2x^{2} - 12x + 21` ≠ A1 `5x + 7 - 2\left(x + 2\right) - 17x + 9 + 2x^{2}`

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

- **Reuse:** Existing skeleton slug `factor_quadratic` / shared `quadratic_factoring` family.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `quadratic_factoring`; equations/WP agent owns solve/WP siblings._
