# `order_of_operations` — Order of operations

- **Course:** Algebra 1
- **Category:** Pre-Algebra — Beginning Algebra
- **Generator:** `order_of_operations`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Evaluate a numeric expression. D=0: two ops, maybe one grouping. High D: exponents + nested parens.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101 (pattern=`OrderOfOperations`):
  - prompt: `2 \times 2 - 3`
  - answer: `1`
- seed 207 (pattern=`OrderOfOperations`):
  - prompt: `2 \times 2 - 1`
  - answer: `3`

### D=8

- seed 101 (pattern=`OrderOfOperations`):
  - prompt: `2 \times 3 - 8 \div 4 - 2 \times 2 + 1`
  - answer: `1`
- seed 207 (pattern=`OrderOfOperations`):
  - prompt: `4 \div 2 + 3 \times 2 + 2 \times 2 - 3 \times 3`
  - answer: `3`

### D=16

- seed 101 (pattern=`OrderOfOperations`):
  - prompt: `9 \div 3 - 3 \times 3 - 8^{2} \div 2 + \left(4 - 2\right) \times 2 - 2 - 3 \times 3 + 46`
  - answer: `1`
- seed 207 (pattern=`OrderOfOperations`):
  - prompt: `12 \div 6 + 2 \times 3 + 18 \div 6 - 2 \times 2 - 12^{2} \div 6 - 3 \times 2 + 26`
  - answer: `3`

### D=22

- seed 101 (pattern=`OrderOfOperations`):
  - prompt: `9 \div 3 - 4 \times 4 - \left(4 - 2\right) \times 2 - 3 \times 2 + 24 \div 6 + 2 \times 4 + 15 \div 5 + 6 \div 3 + 7`
  - answer: `1`
- seed 207 (pattern=`OrderOfOperations`):
  - prompt: `\left(3 - 2\right) \times 2 + 18 \div 6 - 2 \times 2 - 12^{2} \div 6 - 3 \times 2 - 2 \times 2 - 3 \times 3 + \left(2 + 3\right) \times 2 + 2 \times 3 + 29`
  - answer: `3`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 1.2 Use the Language of Algebra

- https://openstax.org/books/elementary-algebra-2e/pages/1-2-use-the-language-of-algebra
- Shape: PEMDAS; 2+3·4; (2+3)².

### Prealgebra 2e — 2.1 Use the Language of Algebra

- https://openstax.org/books/prealgebra-2e/pages/2-1-use-the-language-of-algebra
- (no local mine items; use the section URL)

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- LIMITATIONS: shared skill with G6/PA numeric OO; A1 leaf should stay numeric (not algebra rewrite).

## Proposed engine (reuse vs new)

Reuse order_of_operations (number). No new engine.

_Proposal only. No engine implementation in this notes pass._
