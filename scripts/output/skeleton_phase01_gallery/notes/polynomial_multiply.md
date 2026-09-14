# `polynomial_multiply` — Multiplying

- **Course:** Algebra 1
- **Category:** Algebra 1 — Polynomials
- **Generator:** `polynomial_multiply`
- **Already on skeleton?** yes
- **Old-path extra settings: `{"use_factor_poly": true}`.**

## What the question should look like (D=0 vs high D)

D=0: monomial×binomial or two linear binomials (FOIL). High D: binomial×trinomial. Special products wait for the sibling leaf.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{Multiply: } \left(-x - 3\right)\left(x\right)`
  - answer: `-x^{2} - 3x`
- seed 207:
  - prompt: `\text{Multiply: } \left(x + 1\right)\left(x + 3\right)`
  - answer: `x^{2} + 4x + 3`

### D=8

- seed 101:
  - prompt: `\text{Multiply: } \left(2x^{2} + x + 2\right)\left(-x\right)`
  - answer: `-2x^{3} - x^{2} - 2x`
- seed 207:
  - prompt: `\text{Multiply: } \left(x^{2} + 3\right)\left(-2x + 1\right)`
  - answer: `-2x^{3} + x^{2} - 6x + 3`

### D=16

- seed 101:
  - prompt: `\text{Multiply: } \left(4x^{2} + 2x + 4\right)\left(x^{2}\right)`
  - answer: `4x^{4} + 2x^{3} + 4x^{2}`
- seed 207:
  - prompt: `\text{Multiply: } \left(x^{2} + 3\right)\left(2x + 1\right)`
  - answer: `2x^{3} + x^{2} + 6x + 3`

### D=22

- seed 101:
  - prompt: `\text{Multiply: } \left(4x^{2} + 2x + 4\right)\left(x^{2}\right)`
  - answer: `4x^{4} + 2x^{3} + 4x^{2}`
- seed 207:
  - prompt: `\text{Multiply: } \left(x^{2} + 3\right)\left(2x + 1\right)`
  - answer: `2x^{3} + x^{2} + 6x + 3`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 6.3 Multiply Polynomials

- https://openstax.org/books/elementary-algebra-2e/pages/6-3-multiply-polynomials
- Mined examples:
  - Example 6.28: Multiply: $4 (x + 3) .$
  - Example 6.29: Multiply: $y (y - 2) .$
  - Example 6.30: Multiply: $7 x (2 x + y) .$
  - Example 6.31: Multiply: $−2 y \left(\right. 4 y^{2} + 3 y - 5 \left.\right) .$

### Prealgebra 2e — 10.3 Multiply Polynomials

- https://openstax.org/books/prealgebra-2e/pages/10-3-multiply-polynomials
- (no local mine items; use the section URL)

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Proposed engine (reuse vs new)

Reuse FactorProduct multiply task (already skeletoned).

_Proposal only. No engine implementation in this notes pass._
