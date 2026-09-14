# `polynomial_factoring_grouping` — By grouping

- **Course:** Algebra 1
- **Category:** Algebra 1 — Polynomials
- **Generator:** `polynomial_factoring_grouping`
- **Already on skeleton?** yes
- **Old-path extra settings: `{"use_factor_poly": true}`.**

## What the question should look like (D=0 vs high D)

Four-term grouping. D=0: x³+3x²+2x+6 with an obvious split. High D: GCF first, or rearrange.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `3x^{2} + 10x + 8`
  - answer: `\left(x + 2\right)\left(3x + 4\right)`
- seed 207:
  - prompt: `x^{2} + 4x + 3`
  - answer: `\left(x + 3\right)\left(x + 1\right)`

### D=8

- seed 101:
  - prompt: `3x^{3} - 6x^{2} + 4x - 8`
  - answer: `\left(x - 2\right)\left(3x^{2} + 4\right)`
- seed 207:
  - prompt: `x^{3} - 2x^{2} - x + 2`
  - answer: `\left(x - 2\right)\left(x^{2} - 1\right)`

### D=16

- seed 101:
  - prompt: `22x - 8 - 6x^{2} + 3x^{3}`
  - answer: `\left(x - 2\right)\left(3x^{2} + 4\right)`
- seed 207:
  - prompt: `-2x^{2} + 2 - x + x^{3}`
  - answer: `\left(x - 2\right)\left(x^{2} - 1\right)`

### D=22

- seed 101:
  - prompt: `-x^{3} - 6x^{2} + 4x + 4\left(x^{3} - 2\right)`
  - answer: `\left(x - 2\right)\left(3x^{2} + 4\right)`
- seed 207:
  - prompt: `x^{3} + 2\left(x^{3} + 1\right) - 2x^{3} - x - 2x^{2}`
  - answer: `\left(x - 2\right)\left(x^{2} - 1\right)`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 7.1 Greatest Common Factor and Factor by Grouping

- https://openstax.org/books/elementary-algebra-2e/pages/7-1-greatest-common-factor-and-factor-by-grouping
- Mined examples:
  - Example 7.1: How to Find the Greatest Common Factor of Two or More Expressions Find the GCF of 54 and 36.
  - Example 7.2: Find the greatest common factor of $27 x^{3} \text{and} 18 x^{4}$ .
  - Example 7.3: Find the GCF of $4 x^{2} y , 6 x y^{3}$ .
  - Example 7.4: Find the GCF of: $21 x^{3} , 9 x^{2} , 15 x$ .
- Shape: Factor 4x³+12x²+x+3 by grouping.

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Proposed engine (reuse vs new)

Reuse FactorProduct grouping (already skeletoned).

_Proposal only. No engine implementation in this notes pass._
