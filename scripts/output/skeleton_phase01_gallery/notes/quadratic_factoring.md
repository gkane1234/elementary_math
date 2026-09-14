# `quadratic_factoring` — Quadratic expressions

- **Course:** Algebra 1
- **Category:** Algebra 1 — Polynomials
- **Generator:** `quadratic_factoring`
- **Already on skeleton?** yes
- **Old-path extra settings: `{"use_factor_poly": true}`.**

## What the question should look like (D=0 vs high D)

Factor ax²+bx+c (not solve). D=0: monic x²+5x+6. High D: a≠1 (ac), then unsimplified stem.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101 (form=`trinomial_x2_bx_c`):
  - prompt: `x^{2} + 6x + 8`
  - answer: `\left(x + 4\right)\left(x + 2\right)`
- seed 207 (form=`trinomial_x2_bx_c`):
  - prompt: `x^{2} + 4x + 3`
  - answer: `\left(x + 1\right)\left(x + 3\right)`

### D=8

- seed 101 (form=`trinomial_x2_bx_c`):
  - prompt: `x^{2} + 2x - 8`
  - answer: `\left(x + 4\right)\left(x - 2\right)`
- seed 207 (form=`trinomial_x2_bx_c`):
  - prompt: `x^{2} - 3x + 2`
  - answer: `\left(x - 1\right)\left(x - 2\right)`

### D=16

- seed 101 (form=`trinomial_ax2_bx_c`):
  - prompt: `2\left(-28x + 32\right) + 12x^{2}`
  - answer: `4\left(x - 2\right)\left(3x - 8\right)`
- seed 207 (form=`trinomial_ax2_bx_c`):
  - prompt: `-x^{2} + 3x^{2} + 12 - 14x`
  - answer: `2\left(x - 6\right)\left(x - 1\right)`

### D=22

- seed 101 (form=`trinomial_ax2_bx_c`):
  - prompt: `-2\left(-6x^{2}\right) + 64 - 56x`
  - answer: `4\left(x - 2\right)\left(3x - 8\right)`
- seed 207 (form=`trinomial_ax2_bx_c`):
  - prompt: `5x + 7 - 2\left(x + 2\right) - 17x + 9 + 2x^{2}`
  - answer: `2\left(x - 6\right)\left(x - 1\right)`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 7.2 Factor Trinomials of the Form x²+bx+c

- https://openstax.org/books/elementary-algebra-2e/pages/7-2-factor-trinomials-of-the-form-x2-bx-c
- Mined examples:
  - Example 7.17: How to Factor Trinomials of the Form $x^{2} + b x + c$ Factor: $x^{2} + 7 x + 12$ .
  - Example 7.18: Factor: $u^{2} + 11 u + 24$ .
  - Example 7.19: Factor: $y^{2} + 17 y + 60$ .
  - Example 7.20: Factor: $t^{2} - 11 t + 28$ .

### Elementary Algebra 2e — 7.3 Factor Trinomials of the Form ax²+bx+c

- https://openstax.org/books/elementary-algebra-2e/pages/7-3-factor-trinomials-of-the-form-ax2-bx-c
- Mined examples:
  - Example 7.29: Identify the best method to use to factor each polynomial. ⓐ $6 y^{2} - 72$ ⓑ $r^{2} - 10 r - 24$ ⓒ $p^{2} + 5 p + p q + 5 q$
  - Example 7.30: Factor completely: $2 n^{2} - 8 n - 42$ .
  - Example 7.31: Factor completely: $4 y^{2} - 36 y + 56$ .
  - Example 7.32: Factor completely: $4 u^{3} + 16 u^{2} - 20 u$ .

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Proposed engine (reuse vs new)

Reuse FactorProduct (already skeletoned). D=0 must stay monic; a≠1 is a D unlock.

_Proposal only. No engine implementation in this notes pass._
