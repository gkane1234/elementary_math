# `polynomial_multiply_special` — Multiplying special cases

- **Course:** Algebra 1
- **Category:** Algebra 1 — Polynomials
- **Generator:** `polynomial_multiply_special`
- **Already on skeleton?** yes
- **Old-path extra settings: `{"use_factor_poly": true}`.**

## What the question should look like (D=0 vs high D)

Only special products: (a±b)² or (a−b)(a+b). D=0: (x+3)² or (x−2)(x+2). High D: (2x−5)², two-variable, or leftover inflate.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{Multiply: } \left(x + 1\right)\left(x - 1\right)`
  - answer: `x^{2} - 1`
- seed 207:
  - prompt: `\text{Multiply: } \left(x + 3\right)\left(x - 3\right)`
  - answer: `x^{2} - 9`

### D=8

- seed 101:
  - prompt: `\text{Multiply: } \left(3x + 3\right)\left(3x - 3\right)`
  - answer: `9x^{2} - 9`
- seed 207:
  - prompt: `\text{Multiply: } \left(2x + 1\right)\left(2x - 1\right)`
  - answer: `4x^{2} - 1`

### D=16

- seed 101:
  - prompt: `\text{Multiply: } \left(2x + 4\right)^{2}`
  - answer: `4x^{2} + 16x + 16`
- seed 207:
  - prompt: `\text{Multiply: } \left(2x + 1\right)\left(2x - 1\right)`
  - answer: `4x^{2} - 1`

### D=22

- seed 101:
  - prompt: `\text{Multiply: } \left(2x + 4\right)^{2}`
  - answer: `4x^{2} + 16x + 16`
- seed 207:
  - prompt: `\text{Multiply: } \left(2x + 1\right)\left(2x - 1\right)`
  - answer: `4x^{2} - 1`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 6.4 Special Products

- https://openstax.org/books/elementary-algebra-2e/pages/6-4-special-products
- Mined examples:
  - Example 6.47: Multiply: $(x + 5)^{2} .$
  - Example 6.48: Multiply: $(y - 3)^{2} .$
  - Example 6.49: Multiply: $(4 x + 6)^{2} .$
  - Example 6.50: Multiply: $(2 x - 3 y)^{2} .$

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Proposed engine (reuse vs new)

Reuse FactorProduct special-multiply (already skeletoned). Must not become generic FOIL.

_Proposal only. No engine implementation in this notes pass._
