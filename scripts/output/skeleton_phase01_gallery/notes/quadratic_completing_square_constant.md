# `quadratic_completing_square_constant` — Completing the square by finding the constant

- **Course:** Algebra 1
- **Category:** Algebra 1 — Quadratic Functions
- **Generator:** `quadratic_completing_square_constant`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Find c so x²+bx+c is a perfect square. D=0: even b (x²+6x+c). High D: odd b → fraction.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `x^{2} + 4x + c \text{ is a perfect square trinomial. Find } c.`
  - answer: `4`
- seed 207:
  - prompt: `x^{2} + 4x + c \text{ is a perfect square trinomial. Find } c.`
  - answer: `4`

### D=8

- seed 101:
  - prompt: `x^{2} + 12x + c \text{ is a perfect square trinomial. Find } c.`
  - answer: `36`
- seed 207:
  - prompt: `x^{2} + 8x + c \text{ is a perfect square trinomial. Find } c.`
  - answer: `16`

### D=16

- seed 101:
  - prompt: `x^{2} + 15x + c \text{ is a perfect square trinomial. Find } c.`
  - answer: `\frac{225}{4}`
- seed 207:
  - prompt: `x^{2} + 10x + c \text{ is a perfect square trinomial. Find } c.`
  - answer: `25`

### D=22

- seed 101:
  - prompt: `x^{2} + 14x + c \text{ is a perfect square trinomial. Find } c.`
  - answer: `49`
- seed 207:
  - prompt: `x^{2} + 9x + c \text{ is a perfect square trinomial. Find } c.`
  - answer: `\frac{81}{4}`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 10.2 Solve Quadratic Equations by Completing the Square

- https://openstax.org/books/elementary-algebra-2e/pages/10-2-solve-quadratic-equations-by-completing-the-square
- Mined examples:
  - Example 10.14: Complete the square to make a perfect square trinomial. Then, write the result as a binomial square. $x^{2} + 14 x$
  - Example 10.15: Complete the square to make a perfect square trinomial. Then, write the result as a binomial squared. $m^{2} - 26 m$
  - Example 10.16: Complete the square to make a perfect square trinomial. Then, write the result as a binomial squared. $u^{2} - 9 u$
  - Example 10.17: Complete the square to make a perfect square trinomial. Then, write the result as a binomial squared. $p^{2} + \frac{1}{2} p$
- Shape: What constant completes x²+8x+__ ?

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Gallery section slug: `quadratic_completing_square_constant` (type_id or alias).

## Proposed engine (reuse vs new)

Reuse quadratic_completing_square_constant. Keep this leaf as 'find c' — solving is the sibling.

_Proposal only. No engine implementation in this notes pass._
