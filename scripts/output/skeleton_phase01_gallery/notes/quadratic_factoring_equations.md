# `quadratic_factoring_equations` — Solving equations by factoring

- **Course:** Algebra 1
- **Category:** Algebra 1 — Quadratic Functions
- **Generator:** `quadratic_factoring_equations`
- **Already on skeleton?** yes
- **Old-path extra settings: `{"use_factor_poly": true}`.**

## What the question should look like (D=0 vs high D)

Solve by factoring (set =0, zero product). D=0: x²+7x+12=0 monic. High D: a≠1 then unsimplified.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `x^{2} + 7x + 12 = 0`
  - answer: `x = -4, x = -3`
- seed 207:
  - prompt: `x^{2} + 3x + 2 = 0`
  - answer: `x = -2, x = -1`

### D=8

- seed 101:
  - prompt: `4x^{2} - 24x + 32 = 0`
  - answer: `x = 2, x = 4`
- seed 207:
  - prompt: `2x^{2} - 18x + 16 = 0`
  - answer: `x = 1, x = 8`

### D=16

- seed 101:
  - prompt: `2\left(-24x + 32\right) + 8x^{2} = 0`
  - answer: `x = 2, x = 4`
- seed 207:
  - prompt: `-2\left(-x^{2} + 6x - 9\right) = 0`
  - answer: `x = 3`

### D=22

- seed 101:
  - prompt: `8x^{2} + 3x^{2} - 3x^{2} + 64 - 48x = 0`
  - answer: `x = 2, x = 4`
- seed 207:
  - prompt: `-3\left(x^{2} + 1\right) + 3x^{2} + 2x^{2} - 12x + 21 = 0`
  - answer: `x = 3`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 7.6 Quadratic Equations

- https://openstax.org/books/elementary-algebra-2e/pages/7-6-quadratic-equations
- Mined examples:
  - Example 7.69: How to Use the Zero Product Property to Solve a Quadratic Equation Solve: $(x + 1) (x - 4) = 0$ .
  - Example 7.70: Solve: $(5 n - 2) (6 n - 1) = 0$ .
  - Example 7.71: Solve: $3 p (10 p + 7) = 0$ .
  - Example 7.72: Solve: $(y - 8)^{2} = 0$ .

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Proposed engine (reuse vs new)

Reuse FactorProduct solve task (already skeletoned).

_Proposal only. No engine implementation in this notes pass._
