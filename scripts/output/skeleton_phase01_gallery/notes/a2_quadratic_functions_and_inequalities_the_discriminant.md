# Notes — `a2_quadratic_functions_and_inequalities_the_discriminant`

- **Display name:** The discriminant
- **Category:** Algebra 2 — Quadratic Functions and Inequalities
- **Generator:** `quadratic_discriminant`
- **Already on skeleton?** yes (`quadratic_discriminant`)
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice the discriminant (catalog: quadratic_discriminant).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `(none — live default is old path)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find the discriminant of } x^{2} + 2x - 1.$ | $D = 8; \text{two real roots}$ | pattern=QuadraticDiscriminant |
| 0 | 207 | $\text{Find the discriminant of } x^{2} + 2x + 2.$ | $D = -4; \text{no real roots}$ | pattern=QuadraticDiscriminant |
| 8 | 101 | $\text{Find the discriminant of } 4x^{2} - 6x + 5.$ | $D = -44; \text{no real roots}$ | pattern=QuadraticDiscriminant |
| 8 | 207 | $\text{Find the discriminant of } 4x^{2} + 9x + 9.$ | $D = -63; \text{no real roots}$ | pattern=QuadraticDiscriminant |
| 16 | 101 | $\text{Find the discriminant of } 4x^{2} - 10x + 12.$ | $D = -92; \text{no real roots}$ | pattern=QuadraticDiscriminant |
| 16 | 207 | $\text{Find the discriminant of } 4x^{2} + 20x + 20.$ | $D = 80; \text{two real roots}$ | pattern=QuadraticDiscriminant |
| 22 | 101 | $\text{Find the discriminant of } 4x^{2} - 11x + 11.$ | $D = -55; \text{no real roots}$ | pattern=QuadraticDiscriminant |
| 22 | 207 | $\text{Find the discriminant of } 4x^{2} + 19x + 19.$ | $D = 57; \text{two real roots}$ | pattern=QuadraticDiscriminant |

Opt-out flag used: `(none — live default is old path)`

## A1 alias comparison

- **A1 catalog twin:** `quadratic_discriminant` (same generator `quadratic_discriminant` unless noted).
- **Old path vs A1:** Identical prompts at all sampled D/seeds (shared generator).

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| Intermediate Algebra 2e §9.6 | https://openstax.org/books/intermediate-algebra-2e/pages/9-6-graph-quadratic-functions-using-properties | 9.6 Graph Quadratic Functions Using Properties — e.g. Example 9.42: Graph $f (x) = x^{2} - 1 .$; Example 9.43: Determine whether each parabola opens upward or downward: ⓐ $f (x) = −3 x^{2} + 2 x - 4$ ⓑ $f (x) = 6 x^{2} + 7 x - 9 .$ |
| Intermediate Algebra 2e §9.2 | https://openstax.org/books/intermediate-algebra-2e/pages/9-2-solve-quadratic-equations-by-completing-the-square | 9.2 Solve Quadratic Equations by Completing the Square — e.g. Example 9.11: Complete the square to make a perfect square trinomial. Then write the result as a binomial squared. ⓐ $x^{2} - 26 x$ ⓑ $y^{2} - 9 y$ ⓒ $n^{2} + \frac{1}{2} n$; Example 9.12: How to Solve a Quadratic Equation of the Form $x^{2} + b x + c = 0$ by Completing the Square Solve by completing the square: $x^{2} + 8 x = 48 .$ |

Local HTML (if mined): `textbooks/openstax/html/intermediate-algebra-2e/` or `college-algebra-2e/`.

## Variety notes / UNCLEAR flag

Not a WP leaf unless the generator is story-based. Algebra shapes follow old path samples above.

## Limitations

- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Existing skeleton slug `quadratic_discriminant` / shared `quadratic_discriminant` family.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `quadratic_discriminant`; equations/WP agent owns solve/WP siblings._
