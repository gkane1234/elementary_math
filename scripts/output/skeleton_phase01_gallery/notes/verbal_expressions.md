# `verbal_expressions` — Verbal expressions

- **Course:** Algebra 1
- **Category:** Pre-Algebra — Beginning Algebra
- **Generator:** `verbal_expressions`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Translate a phrase to algebra. D=0: '3 more than x'. High D: product-of-sum, consecutive integers language.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{the quotient of a number and } 5`
  - answer: `\frac{x}{5}`
- seed 207:
  - prompt: `\text{} 5 \text{ fewer than a number}`
  - answer: `x - 5`

### D=8

- seed 101:
  - prompt: `\text{} 11 \text{ less than twice the quantity of a number plus } 5`
  - answer: `2(x + 5) - 11`
- seed 207:
  - prompt: `\text{} 10 \text{ more than the product of } 12 \text{ and a number}`
  - answer: `12x + 10`

### D=16

- seed 101:
  - prompt: `\text{} 11 \text{ times the difference of a number and } 15`
  - answer: `11(x - 15)`
- seed 207:
  - prompt: `\text{the sum of three consecutive odd integers starting with a number}`
  - answer: `x + (x + 2) + (x + 4)`

### D=22

- seed 101:
  - prompt: `\text{} 11 \text{ times the quantity of a number squared plus } 15`
  - answer: `11(x^{2} + 15)`
- seed 207:
  - prompt: `\text{twice the quantity of a number increased by } 10`
  - answer: `2(x + 10)`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 1.2 Use the Language of Algebra

- https://openstax.org/books/elementary-algebra-2e/pages/1-2-use-the-language-of-algebra
- Shape: 3 more than n; twice a number decreased by 7; product of 5 and x+2.

### Prealgebra 2e — 2.2 Evaluate, Simplify, and Translate Expressions

- https://openstax.org/books/prealgebra-2e/pages/2-2-evaluate-simplify-and-translate-expressions
- (no local mine items; use the section URL)

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- LIMITATIONS: may lack dedicated skeleton section; check live generator vs OpenStax translate-words.
- Must not become binomial-product / cube verbal dumps from A2.

## Proposed engine (reuse vs new)

Reuse verbal_expressions (affine/translate). Not SolveLinear.

_Proposal only. No engine implementation in this notes pass._
