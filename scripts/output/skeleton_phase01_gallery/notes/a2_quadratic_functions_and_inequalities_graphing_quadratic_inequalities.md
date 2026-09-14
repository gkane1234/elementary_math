# Notes — `a2_quadratic_functions_and_inequalities_graphing_quadratic_inequalities`

> **UNCLEAR / NOT_IMPLEMENTED** — Graph-shade skill; old path vs OpenStax IA §9.8 interval form not locked.

- **Display name:** Graphing quadratic inequalities
- **Category:** Algebra 2 — Quadratic Functions and Inequalities
- **Generator:** `quadratic_graph_inequality`
- **Already on skeleton?** no
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice graphing quadratic inequalities (catalog: quadratic_graph_inequality).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `(none — live default is old path)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $y > (x - 3)^2$ | $y > (x - 3)^2 \text{ (dashed boundary)}$ | figure |
| 0 | 207 | $y < (x + 2)^2$ | $y < (x + 2)^2 \text{ (dashed boundary)}$ | figure |
| 8 | 101 | $y > -2(x - 2)^2 - 2$ | $y > -2(x - 2)^2 - 2 \text{ (dashed boundary)}$ | figure |
| 8 | 207 | $y \geq -x^{2} + 6x - 12$ | $y \geq -x^{2} + 6x - 12 \text{ (solid boundary)}$ | figure |
| 16 | 101 | $y < -3x^{2} - 18x - 32$ | $y < -3x^{2} - 18x - 32 \text{ (dashed boundary)}$ | figure |
| 16 | 207 | $y \leq -2(x^2 - 14x) - 102$ | $y \leq -2(x^2 - 14x) - 102 \text{ (solid boundary)}$ | figure |
| 22 | 101 | $-3x^{2} + 18x + y \leq 30$ | $-3x^{2} + 18x + y \leq 30 \text{ (solid boundary)}$ | figure |
| 22 | 207 | $y \leq 2(x^2 + 4x) + 7$ | $y \leq 2(x^2 + 4x) + 7 \text{ (solid boundary)}$ | figure |

Opt-out flag used: `(none — live default is old path)`

## A1 alias comparison

- **A1 catalog twin:** `graphing_quadratic_inequalities` (same generator `quadratic_graph_inequality` unless noted).
- **Old path vs A1:** Differs from A1 alias at some D/seeds — see samples; verify catalog intent.
  - D=0.0 seed=101: A2 `y > (x - 3)^2` ≠ A1 `y < x^2 - 1`
  - D=0.0 seed=207: A2 `y < (x + 2)^2` ≠ A1 `y < x^2`
  - D=8.0 seed=101: A2 `y > -2(x - 2)^2 - 2` ≠ A1 `y + 5 > -2(x - 3)^2`
  - D=8.0 seed=207: A2 `y \geq -x^{2} + 6x - 12` ≠ A1 `y > -(x + 4)(x - 2)`
  - D=16.0 seed=101: A2 `y < -3x^{2} - 18x - 32` ≠ A1 `y - 6 > -3(x - 3)^2`
  - D=16.0 seed=207: A2 `y \leq -2(x^2 - 14x) - 102` ≠ A1 `y > -x(x - 6)`
  - D=22.0 seed=101: A2 `-3x^{2} + 18x + y \leq 30` ≠ A1 `y > -3(x - 3)^2 + 6`
  - D=22.0 seed=207: A2 `y \leq 2(x^2 + 4x) + 7` ≠ A1 `y > \frac{1}{2}x(x - 6)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| Intermediate Algebra 2e §9.6 | https://openstax.org/books/intermediate-algebra-2e/pages/9-6-graph-quadratic-functions-using-properties | 9.6 Graph Quadratic Functions Using Properties — e.g. Example 9.42: Graph $f (x) = x^{2} - 1 .$; Example 9.43: Determine whether each parabola opens upward or downward: ⓐ $f (x) = −3 x^{2} + 2 x - 4$ ⓑ $f (x) = 6 x^{2} + 7 x - 9 .$ |
| Intermediate Algebra 2e §9.2 | https://openstax.org/books/intermediate-algebra-2e/pages/9-2-solve-quadratic-equations-by-completing-the-square | 9.2 Solve Quadratic Equations by Completing the Square — e.g. Example 9.11: Complete the square to make a perfect square trinomial. Then write the result as a binomial squared. ⓐ $x^{2} - 26 x$ ⓑ $y^{2} - 9 y$ ⓒ $n^{2} + \frac{1}{2} n$; Example 9.12: How to Solve a Quadratic Equation of the Form $x^{2} + b x + c = 0$ by Completing the Square Solve by completing the square: $x^{2} + 8 x = 48 .$ |

Local HTML (if mined): `textbooks/openstax/html/intermediate-algebra-2e/` or `college-algebra-2e/`.

## Variety notes / UNCLEAR flag

Graph-shade skill; old path vs OpenStax IA §9.8 interval form not locked.
Flags: `UNCLEAR`.

## Limitations

Flags for gallery red header: `NOT_IMPLEMENTED`, `UNCLEAR`.

- **Not implemented on an algebraic skeleton** — graph / figure engine outside SolveLinear / poly / rational cores; leave leaf until a graph core can match OpenStax shapes honestly (`benchmark-old-path` skip).
- **Why stubbed:** live old path may still sample, but gold (transforms, asymptotes, focus/directrix, amplitude/period, shading) is not locked — red-header gallery only.
- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).
- **Diagram:** figure/stimulus may be named in answers — verify SVG/stimulus actually renders on worksheets.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Share A1 `graphing_quadratic_inequalities` generator; wire A2 catalog id when skeleton lands.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `quadratic_graph_inequality`; equations/WP agent owns solve/WP siblings._
