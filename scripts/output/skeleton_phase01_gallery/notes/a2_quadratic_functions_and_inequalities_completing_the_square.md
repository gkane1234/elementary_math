# Notes — `a2_quadratic_functions_and_inequalities_completing_the_square`

> **LOW_VARIETY** — One template across seeds at D=0.

- **Display name:** Completing the square
- **Category:** Algebra 2 — Quadratic Functions and Inequalities
- **Generator:** `quadratic_completing_square_constant`
- **Already on skeleton?** yes (`quadratic_completing_square_constant`)
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice completing the square (catalog: quadratic_completing_square_constant).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `(none — live default is old path)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $x^{2} + 4x + c \text{ is a perfect square trinomial. Find } c.$ | $4$ | pattern=CompleteSquareConst |
| 0 | 207 | $x^{2} + 4x + c \text{ is a perfect square trinomial. Find } c.$ | $4$ | pattern=CompleteSquareConst |
| 8 | 101 | $x^{2} + 12x + c \text{ is a perfect square trinomial. Find } c.$ | $36$ | pattern=CompleteSquareConst |
| 8 | 207 | $x^{2} + 8x + c \text{ is a perfect square trinomial. Find } c.$ | $16$ | pattern=CompleteSquareConst |
| 16 | 101 | $x^{2} + 15x + c \text{ is a perfect square trinomial. Find } c.$ | $\frac{225}{4}$ | pattern=CompleteSquareConst |
| 16 | 207 | $x^{2} + 10x + c \text{ is a perfect square trinomial. Find } c.$ | $25$ | pattern=CompleteSquareConst |
| 22 | 101 | $x^{2} + 14x + c \text{ is a perfect square trinomial. Find } c.$ | $49$ | pattern=CompleteSquareConst |
| 22 | 207 | $x^{2} + 9x + c \text{ is a perfect square trinomial. Find } c.$ | $\frac{81}{4}$ | pattern=CompleteSquareConst |

Opt-out flag used: `(none — live default is old path)`

## A1 alias comparison

- **A1 catalog twin:** `quadratic_completing_square_constant` (same generator `quadratic_completing_square_constant` unless noted).
- **Old path vs A1:** Identical prompts at all sampled D/seeds (shared generator).

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| Intermediate Algebra 2e §9.6 | https://openstax.org/books/intermediate-algebra-2e/pages/9-6-graph-quadratic-functions-using-properties | 9.6 Graph Quadratic Functions Using Properties — e.g. Example 9.42: Graph $f (x) = x^{2} - 1 .$; Example 9.43: Determine whether each parabola opens upward or downward: ⓐ $f (x) = −3 x^{2} + 2 x - 4$ ⓑ $f (x) = 6 x^{2} + 7 x - 9 .$ |
| Intermediate Algebra 2e §9.2 | https://openstax.org/books/intermediate-algebra-2e/pages/9-2-solve-quadratic-equations-by-completing-the-square | 9.2 Solve Quadratic Equations by Completing the Square — e.g. Example 9.11: Complete the square to make a perfect square trinomial. Then write the result as a binomial squared. ⓐ $x^{2} - 26 x$ ⓑ $y^{2} - 9 y$ ⓒ $n^{2} + \frac{1}{2} n$; Example 9.12: How to Solve a Quadratic Equation of the Form $x^{2} + b x + c = 0$ by Completing the Square Solve by completing the square: $x^{2} + 8 x = 48 .$ |

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

- **Reuse:** Existing skeleton slug `quadratic_completing_square_constant` / shared `quadratic_completing_square_constant` family.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `quadratic_completing_square_constant`; equations/WP agent owns solve/WP siblings._
