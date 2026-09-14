# Notes — `a2_quadratic_functions_and_inequalities_graphing_quadratic_functions`

> **UNCLEAR / NOT_IMPLEMENTED** — Graph engine outside algebraic skeleton cores; verify against OpenStax §9.6–9.7.

- **Display name:** Graphing quadratic functions
- **Category:** Algebra 2 — Quadratic Functions and Inequalities
- **Generator:** `quadratic_graph_vertex`
- **Already on skeleton?** no
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Practice graphing quadratic functions (catalog: quadratic_graph_vertex).
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; equation dumps in story leaves.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with opt-out `(none — live default is old path)`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Graph } y = (x + 2)^2$ | $\text{vertex } (-2, 0)$ | — |
| 0 | 207 | $\text{Graph } y = x^2 + 2$ | $\text{vertex } (0, 2)$ | — |
| 8 | 101 | $\text{Graph } y = 2(x^2 - 8x) + 29$ | $\text{vertex } (4, -3)$ | — |
| 8 | 207 | $\text{Graph } y = 2(x + 7)(x + 1)$ | $\text{vertex } (-4, -18)$ | — |
| 16 | 101 | $\text{Graph } y = 2x^{2} + 20x + 55$ | $\text{vertex } (-5, 5)$ | — |
| 16 | 207 | $\text{Graph } y = -3(x^2 + 14x) - 154$ | $\text{vertex } (-7, -7)$ | — |
| 22 | 101 | $\text{Graph } y = 2x^{2} - 24x + 76$ | $\text{vertex } (6, 4)$ | — |
| 22 | 207 | $\text{Graph } x^{2} - 12x + y = -37$ | $\text{vertex } (6, -1)$ | — |

Opt-out flag used: `(none — live default is old path)`

## A1 alias comparison

- **A1 catalog twin:** `graphing_quadratic_functions` (same generator `quadratic_graph_vertex` unless noted).
- **Old path vs A1:** Differs from A1 alias at some D/seeds — see samples; verify catalog intent.
  - D=0.0 seed=101: A2 `\text{Graph } y = (x + 2)^2` ≠ A1 `y = x^2`
  - D=0.0 seed=207: A2 `\text{Graph } y = x^2 + 2` ≠ A1 `y = x^2 + 1`
  - D=8.0 seed=101: A2 `\text{Graph } y = 2(x^2 - 8x) + 29` ≠ A1 `y = -(x - 2)(x - 4)`
  - D=8.0 seed=207: A2 `\text{Graph } y = 2(x + 7)(x + 1)` ≠ A1 `y = -2x^{2} + 16x - 34`
  - D=16.0 seed=101: A2 `\text{Graph } y = 2x^{2} + 20x + 55` ≠ A1 `y = 2(x - 2)(x - 4)`
  - D=16.0 seed=207: A2 `\text{Graph } y = -3(x^2 + 14x) - 154` ≠ A1 `y = -3x^{2} - 6x - 6`
  - D=22.0 seed=101: A2 `\text{Graph } y = 2x^{2} - 24x + 76` ≠ A1 `y = -\frac{3}{2}x^{2} + 9x - \frac{15}{2}`
  - D=22.0 seed=207: A2 `\text{Graph } x^{2} - 12x + y = -37` ≠ A1 `y = -\frac{3}{2}x^{2} - 9x - \frac{43}{2}`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite book + chapter/section + URL.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| Intermediate Algebra 2e §9.6 | https://openstax.org/books/intermediate-algebra-2e/pages/9-6-graph-quadratic-functions-using-properties | 9.6 Graph Quadratic Functions Using Properties — e.g. Example 9.42: Graph $f (x) = x^{2} - 1 .$; Example 9.43: Determine whether each parabola opens upward or downward: ⓐ $f (x) = −3 x^{2} + 2 x - 4$ ⓑ $f (x) = 6 x^{2} + 7 x - 9 .$ |
| Intermediate Algebra 2e §9.2 | https://openstax.org/books/intermediate-algebra-2e/pages/9-2-solve-quadratic-equations-by-completing-the-square | 9.2 Solve Quadratic Equations by Completing the Square — e.g. Example 9.11: Complete the square to make a perfect square trinomial. Then write the result as a binomial squared. ⓐ $x^{2} - 26 x$ ⓑ $y^{2} - 9 y$ ⓒ $n^{2} + \frac{1}{2} n$; Example 9.12: How to Solve a Quadratic Equation of the Form $x^{2} + b x + c = 0$ by Completing the Square Solve by completing the square: $x^{2} + 8 x = 48 .$ |

Local HTML (if mined): `textbooks/openstax/html/intermediate-algebra-2e/` or `college-algebra-2e/`.

## Variety notes / UNCLEAR flag

Graph engine outside algebraic skeleton cores; verify against OpenStax §9.6–9.7.
Flags: `UNCLEAR`.

## Limitations

Flags for gallery red header: `NOT_IMPLEMENTED`, `UNCLEAR`.

- **Not implemented on an algebraic skeleton** — graph / figure engine outside SolveLinear / poly / rational cores; leave leaf until a graph core can match OpenStax shapes honestly (`benchmark-old-path` skip).
- **Why stubbed:** live old path may still sample, but gold (transforms, asymptotes, focus/directrix, amplitude/period, shading) is not locked — red-header gallery only.
- **Difficulty scaling:** D ladder present in notes; verify numeric hardness before format unlocks.
- **OpenStax:** cites present — confirm section matches the skill (not a neighboring chapter dump).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Share A1 `graphing_quadratic_functions` generator; wire A2 catalog id when skeleton lands.
- **New:** only if no honest match — leave leaf and document skip.
- **Not this pass:** notes only; no generator implementation.

_Catalog generator `quadratic_graph_vertex`; equations/WP agent owns solve/WP siblings._
