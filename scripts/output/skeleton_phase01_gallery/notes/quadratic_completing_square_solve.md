# `quadratic_completing_square_solve` — Solving equations by completing the square

- **Course:** Algebra 1
- **Category:** Algebra 1 — Quadratic Functions
- **Generator:** `quadratic_completing_square_solve`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Solve by completing the square. D=0: a=1, even b. High D: a≠1 (divide first).

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `x^{2} + 4x + 4 = 0`
  - answer: `x = -2`
- seed 207:
  - prompt: `x^{2} + 4x = 0`
  - answer: `x = -2 \pm 2`

### D=8

- seed 101:
  - prompt: `4x^{2} - 16x + 272 = 0`
  - answer: `\text{no real solutions}`
- seed 207:
  - prompt: `4x^{2} - 8x - 12 = 0`
  - answer: `x = 1 \pm 2`

### D=16

- seed 101:
  - prompt: `4x^{2} - 16x + 43 = 0`
  - answer: `\text{no real solutions}`
- seed 207:
  - prompt: `4x^{2} - 8x - 20 = 0`
  - answer: `x = 1 \pm \sqrt{6}`

### D=22

- seed 101:
  - prompt: `4x^{2} - 16x + 43 = 0`
  - answer: `\text{no real solutions}`
- seed 207:
  - prompt: `4x^{2} - 8x - 20 = 0`
  - answer: `x = 1 \pm \sqrt{6}`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 10.2 Solve Quadratic Equations by Completing the Square

- https://openstax.org/books/elementary-algebra-2e/pages/10-2-solve-quadratic-equations-by-completing-the-square
- Mined examples:
  - Example 10.14: Complete the square to make a perfect square trinomial. Then, write the result as a binomial square. $x^{2} + 14 x$
  - Example 10.15: Complete the square to make a perfect square trinomial. Then, write the result as a binomial squared. $m^{2} - 26 m$
  - Example 10.16: Complete the square to make a perfect square trinomial. Then, write the result as a binomial squared. $u^{2} - 9 u$
  - Example 10.17: Complete the square to make a perfect square trinomial. Then, write the result as a binomial squared. $p^{2} + \frac{1}{2} p$

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Gallery section slug: `quadratic_completing_square_solve` (type_id or alias).

## Proposed engine (reuse vs new)

Reuse quadratic_completing_square_solve. Do not replace with quadratic formula.

_Proposal only. No engine implementation in this notes pass._
