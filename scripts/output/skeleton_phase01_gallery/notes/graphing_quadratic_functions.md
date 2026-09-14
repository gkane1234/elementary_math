# `graphing_quadratic_functions` — Graphing

- **Course:** Algebra 1
- **Category:** Algebra 1 — Quadratic Functions
- **Generator:** `graph_quadratic`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Graph y=ax²+bx+c (or vertex form). D=0: y=x² or y=x²+k. High D: vertex not on axis, a≠1.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `y = x^2`
  - answer: `y = x^2`
- seed 207:
  - prompt: `y = x^2 + 1`
  - answer: `y = x^2 + 1`

### D=8

- seed 101:
  - prompt: `y = -(x - 2)(x - 4)`
  - answer: `y = -(x - 2)(x - 4)`
- seed 207:
  - prompt: `y = -2x^{2} + 16x - 34`
  - answer: `y = -2x^{2} + 16x - 34`

### D=16

- seed 101:
  - prompt: `y = 2(x - 2)(x - 4)`
  - answer: `y = 2(x - 2)(x - 4)`
- seed 207:
  - prompt: `y = -3x^{2} - 6x - 6`
  - answer: `y = -3x^{2} - 6x - 6`

### D=22

- seed 101:
  - prompt: `y = -\frac{3}{2}x^{2} + 9x - \frac{15}{2}`
  - answer: `y = -\frac{3}{2}x^{2} + 9x - \frac{15}{2}`
- seed 207:
  - prompt: `y = -\frac{3}{2}x^{2} - 9x - \frac{43}{2}`
  - answer: `y = -\frac{3}{2}x^{2} - 9x - \frac{43}{2}`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 10.5 Graphing Quadratic Equations in Two Variables

- https://openstax.org/books/elementary-algebra-2e/pages/10-5-graphing-quadratic-equations-in-two-variables
- Mined examples:
  - Example 10.43: Graph $y = x^{2} - 1$ .
  - Example 10.44: Determine whether each parabola opens upward or downward: ⓐ $y = −3 x^{2} + 2 x - 4$ ⓑ $y = 6 x^{2} + 7 x - 9$
  - Example 10.45: For the parabola $y = 3 x^{2} - 6 x + 2$ find: ⓐ the axis of symmetry and ⓑ the vertex.
  - Example 10.46: Find the intercepts of the parabola $y = x^{2} - 2 x - 8$ .

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- LIMITATIONS: graph engine outside algebraic FactorProduct cores; samples are red-header live graph path.
- OpenStax EA §10.5 shapes (vertex, axis) vs engine fidelity still audit-only.

## Proposed engine (reuse vs new)

Reuse graph_quadratic. Geometry/graph engine — not FactorProduct. UX thin; copy old vertex/intercept asks.

_Proposal only. No engine implementation in this notes pass._
