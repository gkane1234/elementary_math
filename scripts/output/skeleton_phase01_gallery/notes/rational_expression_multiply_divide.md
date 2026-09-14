# `rational_expression_multiply_divide` — Multiplying and dividing rational expressions

- **Course:** Algebra 1
- **Category:** Algebra 1 — Rational Expressions
- **Generator:** `rational_expression_multiply_divide`
- **Already on skeleton?** yes
- **Old-path extra settings: `{"use_constructive_rational": true}`.**

## What the question should look like (D=0 vs high D)

Multiply or divide rationals; factor then cancel across. D=0: monomials or two linears. High D: quadratic factors.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\frac{\left(x-4\right)\left(x+3\right)}{x+4} \div \frac{\left(x-1\right)\left(x+3\right)}{x+1}`
  - answer: `\frac{x^{2}-3x-4}{x^{2}+3x-4},\; x \neq -4, -3, -1, 1`
- seed 207:
  - prompt: `\frac{\left(x+1\right)\left(x-4\right)}{x-2} \cdot \frac{x+3}{\left(x-3\right)\left(x-4\right)}`
  - answer: `\frac{x^{2}+4x+3}{x^{2}-5x+6},\; x \neq 2, 3, 4`

### D=8

- seed 101:
  - prompt: `\frac{\left(5x-1\right)\left(4x-7\right)}{\left(3x+7\right)\left(5x-2\right)} \div \frac{\left(3x-2\right)\left(4x-7\right)}{\left(4x+3\right)\left(5x-2\right)}`
  - answer: `\frac{20x^{2}+11x-3}{9x^{2}+15x-14},\; x \neq -\frac{7}{3}, -\frac{3}{4}, \frac{2}{5}, \frac{2}{3}, \frac{7}{4}`
- seed 207:
  - prompt: `\frac{\left(5x-4\right)\left(3x-4\right)}{\left(x+8\right)\left(x+2\right)} \cdot \frac{\left(2x-5\right)\left(x+2\right)}{\left(3x+7\right)\left(3x-4\right)}`
  - answer: `\frac{10x^{2}-33x+20}{3x^{2}+31x+56},\; x \neq -8, -\frac{7}{3}, -2, \frac{4}{3}`

### D=16

- seed 101:
  - prompt: `\frac{20x^{2}-57x+27}{15x^{2}+13x-20} \div \frac{4x^{2}-17x+18}{10x^{2}-33x+20}`
  - answer: `\frac{10x^{2}-31x+15}{3x^{2}-x-10},\; x \neq -\frac{5}{3}, \frac{4}{5}, 2, \frac{9}{4}, \frac{5}{2}`
- seed 207:
  - prompt: `\frac{x^{2}+9x+8}{4x^{2}+4x-35} \cdot \frac{4x^{2}-24x+35}{x^{2}-x-2}`
  - answer: `\frac{2x^{2}+9x-56}{2x^{2}+3x-14},\; x \neq -\frac{7}{2}, -1, 2, \frac{5}{2}`

### D=22

- seed 101:
  - prompt: `\frac{20x^{2}-57x+27}{15x^{2}+13x-20} \div \frac{4x^{2}-17x+18}{10x^{2}-33x+20}`
  - answer: `\frac{10x^{2}-31x+15}{3x^{2}-x-10},\; x \neq -\frac{5}{3}, \frac{4}{5}, 2, \frac{9}{4}, \frac{5}{2}`
- seed 207:
  - prompt: `\frac{x^{2}+9x+8}{4x^{2}+4x-35} \cdot \frac{4x^{2}-24x+35}{x^{2}-x-2}`
  - answer: `\frac{2x^{2}+9x-56}{2x^{2}+3x-14},\; x \neq -\frac{7}{2}, -1, 2, \frac{5}{2}`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 8.2 Multiply and Divide Rational Expressions

- https://openstax.org/books/elementary-algebra-2e/pages/8-2-multiply-and-divide-rational-expressions
- Mined examples:
  - Example 8.17: Multiply: $\frac{10}{28} \cdot \frac{8}{15} .$
  - Example 8.18: Mulitply: $\frac{2 x}{3 y^{2}} \cdot \frac{6 x y^{3}}{x^{2} y} .$
  - Example 8.19: How to Multiply Rational Expressions Mulitply: $\frac{2 x}{x^{2} - 7 x + 12} \cdot \frac{x^{2} - 9}{6 x^{2}} .$
  - Example 8.20: Multiply: $\frac{n^{2} - 7 n}{n^{2} + 2 n + 1} \cdot \frac{n + 1}{2 n} .$

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Proposed engine (reuse vs new)

Reuse MulDivCancel / rational_skeleton (already skeletoned).

_Proposal only. No engine implementation in this notes pass._
