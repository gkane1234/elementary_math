# `quadratic_formula` — Solving equations with the Quadratic Formula

- **Course:** Algebra 1
- **Category:** Algebra 1 — Quadratic Functions
- **Generator:** `quadratic_formula`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Solve with the quadratic formula. D=0: integer roots, a=1. High D: simplify a radical / fractions.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `x^{2} - x - 2 = 0`
  - answer: `x = 2, -1`
- seed 207:
  - prompt: `x^{2} - 4x + 4 = 0`
  - answer: `x = 2`

### D=8

- seed 101:
  - prompt: `4x^{2} + 4x - 120 = 0`
  - answer: `x = 5, -6`
- seed 207:
  - prompt: `4x^{2} - 72x + 324 = 0`
  - answer: `x = 9`

### D=16

- seed 101:
  - prompt: `3x^{2} + 12x = 0`
  - answer: `x = 0, -4`
- seed 207:
  - prompt: `3x^{2} - 12x - 21 = 0`
  - answer: `x = 2 \pm \sqrt{11}`

### D=22

- seed 101:
  - prompt: `3x^{2} + 11x - 1 = 0`
  - answer: `x = \frac{-11 \pm \sqrt{133}}{6}`
- seed 207:
  - prompt: `3x^{2} - 13x - 22 = 0`
  - answer: `x = \frac{13 \pm \sqrt{433}}{6}`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 10.3 Solve Quadratic Equations Using the Quadratic Formula

- https://openstax.org/books/elementary-algebra-2e/pages/10-3-solve-quadratic-equations-using-the-quadratic-formula
- Mined examples:
  - Example 10.28: How to Solve a Quadratic Equation Using the Quadratic Formula Solve $2 x^{2} + 9 x - 5 = 0$ by using the Quadratic Formula.
  - Example 10.29: Solve $x^{2} - 6 x + 5 = 0$ by using the Quadratic Formula.
  - Example 10.30: Solve $4 y^{2} - 5 y - 3 = 0$ by using the Quadratic Formula.
  - Example 10.31: Solve $2 x^{2} + 10 x + 11 = 0$ by using the Quadratic Formula.

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Gallery section slug: `quadratic_formula` (type_id or alias).

## Proposed engine (reuse vs new)

Reuse quadratic_formula. New engine only if we later unify with FactorProduct goals — not this pass.

_Proposal only. No engine implementation in this notes pass._
