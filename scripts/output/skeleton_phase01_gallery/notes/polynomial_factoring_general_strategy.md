# `polynomial_factoring_general_strategy` — General strategy

- **Course:** Algebra 1
- **Category:** Algebra 1 — Polynomials
- **Generator:** `polynomial_factoring_general_strategy`
- **Already on skeleton?** yes
- **Old-path extra settings: `{"use_factor_poly": true}`.**

## What the question should look like (D=0 vs high D)

Factor completely — student chooses method. D=0: one clear pattern. High D: GCF then a second pattern / mixed bank.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101 (form=`trinomial_x2_bx_c`):
  - prompt: `x^{2} + 7x + 12`
  - answer: `\left(x + 3\right)\left(x + 4\right)`
- seed 207 (form=`difference_of_squares`):
  - prompt: `x^{2} - 4`
  - answer: `\left(x + 2\right)\left(x - 2\right)`

### D=8

- seed 101 (form=`trinomial_x2_bx_c`):
  - prompt: `x^{2} + 2x - 3`
  - answer: `\left(x + 3\right)\left(x - 1\right)`
- seed 207 (form=`perfect_square_trinomial`):
  - prompt: `x^{2} + 2x + 1`
  - answer: `\left(x + 1\right)^{2}`

### D=16

- seed 101 (form=`trinomial_ax2_bx_c`):
  - prompt: `7x^{2} - 10x + 6 - 3x^{2}`
  - answer: `2\left(x - 1\right)\left(2x - 3\right)`
- seed 207 (form=`gcf_then_pattern`):
  - prompt: `10x^{2} - 90x + 77 + 3`
  - answer: `10\left(x - 1\right)\left(x - 8\right)`

### D=22

- seed 101 (form=`trinomial_ax2_bx_c`):
  - prompt: `22x^{2} - 7x - 3x + 6`
  - answer: `2\left(x - 1\right)\left(2x - 3\right)`
- seed 207 (form=`gcf_then_pattern`):
  - prompt: `10y^{2} - 90y + 82 + 1 - 3`
  - answer: `10\left(y - 1\right)\left(y - 8\right)`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 7.5 General Strategy for Factoring Polynomials

- https://openstax.org/books/elementary-algebra-2e/pages/7-5-general-strategy-for-factoring-polynomials
- Mined examples:
  - Example 7.59: Factor completely: $4 x^{5} + 12 x^{4}$ .
  - Example 7.60: Factor completely: $12 x^{2} - 11 x + 2$ .
  - Example 7.61: Factor completely: $g^{3} + 25 g$ .
  - Example 7.62: Factor completely: $12 y^{2} - 75$ .

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Proposed engine (reuse vs new)

Reuse FactorProduct mixed bank (already skeletoned). Must not prompt a named single method only.

_Proposal only. No engine implementation in this notes pass._
