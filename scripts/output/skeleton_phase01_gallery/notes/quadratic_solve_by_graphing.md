# `quadratic_solve_by_graphing` — Solving equations by graphing

- **Course:** Algebra 1
- **Category:** Algebra 1 — Quadratic Functions
- **Generator:** `solve_polynomial_by_graphing`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Solve ax²+bx+c=0 by reading intercepts of the parabola. D=0: integer roots. High D: one root / none.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `x^{2} - 1 = 0`
  - answer: `x = -1, x = 1`
- seed 207:
  - prompt: `x^{2} - 4 = 0`
  - answer: `x = -2, x = 2`

### D=8

- seed 101:
  - prompt: `3x(x - 3) = 0`
  - answer: `x = 0, x = 3`
- seed 207:
  - prompt: `-2(x + 5)(x + 3) = 0`
  - answer: `x = -5, x = -3`

### D=16

- seed 101:
  - prompt: `4x^{2} - 32x + 28 = 0`
  - answer: `x = 1, x = 7`
- seed 207:
  - prompt: `-x^{2} - x + 20 = 0`
  - answer: `x = -5, x = 4`

### D=22

- seed 101:
  - prompt: `5(x - 2)(x - 8) = 0`
  - answer: `x = 2, x = 8`
- seed 207:
  - prompt: `4(x + 9)(x + 4) = 0`
  - answer: `x = -9, x = -4`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 10.5 Graphing Quadratic Equations in Two Variables

- https://openstax.org/books/elementary-algebra-2e/pages/10-5-graphing-quadratic-equations-in-two-variables
- Mined examples:
  - Example 10.43: Graph $y = x^{2} - 1$ .
  - Example 10.44: Determine whether each parabola opens upward or downward: ⓐ $y = −3 x^{2} + 2 x - 4$ ⓑ $y = 6 x^{2} + 7 x - 9$
  - Example 10.45: For the parabola $y = 3 x^{2} - 6 x + 2$ find: ⓐ the axis of symmetry and ⓑ the vertex.
  - Example 10.46: Find the intercepts of the parabola $y = x^{2} - 2 x - 8$ .
- Shape: x-intercepts of y=x²−x−6 are the solutions of x²−x−6=0.

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- LIMITATIONS: graph-read roots, not formula; UNCLEAR fidelity of interactive/diagram vs algebraic answer.

## Proposed engine (reuse vs new)

Reuse solve_polynomial_by_graphing. Must stay graph-read, not quadratic formula.

_Proposal only. No engine implementation in this notes pass._
