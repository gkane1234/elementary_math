# `polynomial_factoring_special_cases` — Special cases

- **Course:** Algebra 1
- **Category:** Algebra 1 — Polynomials
- **Generator:** `polynomial_factoring_special_cases`
- **Already on skeleton?** yes
- **Old-path extra settings: `{"use_factor_poly": true}`.**

## What the question should look like (D=0 vs high D)

Difference of squares / perfect-square trinomials (A1; cubes are A2). D=0: x²−9. High D: a≠1 or GCF then special.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101 (form=`difference_of_squares`):
  - prompt: `x^{2} - 16`
  - answer: `\left(x + 4\right)\left(x - 4\right)`
- seed 207 (form=`difference_of_squares`):
  - prompt: `x^{2} - 1`
  - answer: `\left(x + 1\right)\left(x - 1\right)`

### D=8

- seed 101 (form=`difference_of_squares`):
  - prompt: `x^{2} - 49`
  - answer: `\left(x + 7\right)\left(x - 7\right)`
- seed 207 (form=`difference_of_squares`):
  - prompt: `x^{2} - 9`
  - answer: `\left(x + 3\right)\left(x - 3\right)`

### D=16

- seed 101 (form=`difference_of_squares`):
  - prompt: `-3x^{2} + 4x^{2} - 49`
  - answer: `\left(x + 7\right)\left(x - 7\right)`
- seed 207 (form=`difference_of_squares`):
  - prompt: `-x^{2} - 11 + 2\left(x^{2} + 1\right)`
  - answer: `\left(x + 3\right)\left(x - 3\right)`

### D=22

- seed 101 (form=`difference_of_squares`):
  - prompt: `3 - 54 + 2 + x^{2}`
  - answer: `\left(x + 7\right)\left(x - 7\right)`
- seed 207 (form=`difference_of_squares`):
  - prompt: `x^{2} - 11 + 2x^{2} - 2\left(x^{2} - 1\right)`
  - answer: `\left(x + 3\right)\left(x - 3\right)`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 7.4 Factor Special Products

- https://openstax.org/books/elementary-algebra-2e/pages/7-4-factor-special-products
- Mined examples:
  - Example 7.42: How to Factor Perfect Square Trinomials Factor: $9 x^{2} + 12 x + 4$ .
  - Example 7.43: Factor: $81 y^{2} - 72 y + 16$ .
  - Example 7.44: Factor: $36 x^{2} + 84 x y + 49 y^{2}$ .
  - Example 7.45: Factor: $9 x^{2} + 50 x + 25$ .

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Proposed engine (reuse vs new)

Reuse FactorProduct special-factor (already skeletoned). Do not mix grouping/ac.

_Proposal only. No engine implementation in this notes pass._
