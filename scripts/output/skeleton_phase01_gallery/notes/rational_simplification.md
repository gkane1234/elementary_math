# `rational_simplification` — Simplifying and excluded values

- **Course:** Algebra 1
- **Category:** Algebra 1 — Rational Expressions
- **Generator:** `rational_simplification`
- **Already on skeleton?** yes
- **Old-path extra settings: `{"use_constructive_rational": true}`.**

## What the question should look like (D=0 vs high D)

Simplify one rational expression; state excluded values of cancelled factors. D=0: monomial cancel or (x+1)/(x+1). High D: factor quadratic then cancel.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101 (form=`simplify_cancel`):
  - prompt: `\text{Simplify: } \frac{2x^{2} - 4x - 6}{x^{2} - 4x + 3}`
  - answer: `\frac{2x + 2}{x - 1},\; x \neq 3`
- seed 207 (form=`simplify_cancel`):
  - prompt: `\text{Simplify: } \frac{x^{2} - 5x + 6}{x^{2} + x - 6}`
  - answer: `\frac{x - 3}{x + 3},\; x \neq 2`

### D=8

- seed 101 (form=`simplify_cancel`):
  - prompt: `\text{Simplify: } \frac{4x^{2} - 12x + 8}{x^{2} + x - 2}`
  - answer: `\frac{4x - 8}{x + 2},\; x \neq 1`
- seed 207 (form=`simplify_cancel`):
  - prompt: `\text{Simplify: } \frac{y^{2} - 2y - 3}{y^{2} - y - 6}`
  - answer: `\frac{y + 1}{y + 2},\; y \neq 3`

### D=16

- seed 101 (form=`simplify_cancel`):
  - prompt: `\text{Simplify: } \frac{-2\left(g - 2\right)\left(g + 2\right)\left(g + 3\right)}{\left(g + 1\right)\left(g + 4\right)\left(g + 2\right)\left(g + 3\right)}`
  - answer: `\frac{-2g + 4}{g^{2} + 5g + 4},\; g \neq -3, -2`
- seed 207 (form=`simplify_cancel`):
  - prompt: `\text{Simplify: } \frac{12\left(t - 2\right)\left(t - 1\right)\left(t - 9\right)}{\left(t + 2\right)\left(t + 1\right)\left(t - 1\right)\left(t - 9\right)}`
  - answer: `\frac{12t - 24}{t^{2} + 3t + 2},\; t \neq 1, 9`

### D=22

- seed 101 (form=`simplify_cancel`):
  - prompt: `\text{Simplify: } \frac{-8\left(\delta - 2\right)\left(\delta + 2\right)\left(\delta + 5\right)}{\left(\delta + 1\right)\left(\delta - 3\right)\left(\delta + 2\right)\left(\delta + 5\right)}`
  - answer: `\frac{-8\delta + 16}{\delta^{2} - 2\delta - 3},\; \delta \neq -5, -2`
- seed 207 (form=`simplify_cancel`):
  - prompt: `\text{Simplify: } \frac{\left(\left(-4 + 6\right)\right)\left(6\left(l + 5\right)\left(l - 5\right)\left(l - 7\right)\right)}{\left(\left(-4 + 6\right)\right)\left(\left(l - 1\right)\left(l\right)\left(l - 5\right)\left(l - 7\right)\right)}`
  - answer: `\frac{6l + 30}{l^{2} - l},\; l \neq 5, 7`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 8.1 Simplify Rational Expressions

- https://openstax.org/books/elementary-algebra-2e/pages/8-1-simplify-rational-expressions
- Mined examples:
  - Example 8.1: Determine the values for which the rational expression is undefined: ⓐ $\frac{9 y}{x}$ ⓑ $\frac{4 b - 3}{2 b + 5}$ ⓒ $\frac{x + 4}{x^{2} + 5 x + 6}$
  - Example 8.2: Evaluate $\frac{2 x + 3}{3 x - 5}$ for each value: ⓐ $x = 0$ ⓑ $x = 2$ ⓒ $x = −3$
  - Example 8.3: Evaluate $\frac{x^{2} + 8 x + 7}{x^{2} - 4}$ for each value: ⓐ $x = 0$ ⓑ $x = 2$ ⓒ $x = −1$
  - Example 8.4: Evaluate $\frac{a^{2} + 2 a b + b^{2}}{3 a b^{2}}$ for each value: ⓐ $a = 1 , b = 2$ ⓑ $a = −2 , b = −1$ ⓒ $a = \frac{1}{3} , b = 0$

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Proposed engine (reuse vs new)

Reuse SimplifyCancel / rational_skeleton (already skeletoned). Opt-out is constructive.

_Proposal only. No engine implementation in this notes pass._
