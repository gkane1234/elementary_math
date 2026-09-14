# `rational_expression_simplification` — Adding and subtracting rational expressions

- **Course:** Algebra 1
- **Category:** Algebra 1 — Rational Expressions
- **Generator:** `rational_expression_simplification`
- **Already on skeleton?** yes
- **Old-path extra settings: `{"use_constructive_rational": true}`.**

## What the question should look like (D=0 vs high D)

Add/subtract rational expressions. D=0: common denominator. High D: unlike dens / LCD of linears.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\frac{-3}{x} + \frac{-2}{x}`
  - answer: `\frac{-5}{x}`
- seed 207:
  - prompt: `\frac{4}{x-1} + \frac{1}{x-1}`
  - answer: `\frac{5}{x-1}`

### D=8

- seed 101:
  - prompt: `\frac{2}{9x^{2}+12x-5} + \frac{-17x-9}{(4x-3)(3x-1)(3x+5)}`
  - answer: `\frac{-3}{(4x-3)(3x-1)},\; x \neq -\frac{5}{3}`
- seed 207:
  - prompt: `\frac{-x-23}{6x^{2}-13x-5} + \frac{-4}{3x+1}`
  - answer: `\frac{-3}{2x-5},\; x \neq -\frac{1}{3}`

### D=16

- seed 101:
  - prompt: `\frac{1}{(2x-1)(4x+5)(2x+3)(3x-1)(4x+3)} + \frac{30x^{2}+35x-16}{(2x-1)(4x+5)(2x+3)(3x-1)(4x+3)}`
  - answer: `\frac{5}{(2x-1)(4x+5)(4x+3)},\; x \neq -\frac{3}{2}, \frac{1}{3}`
- seed 207:
  - prompt: `\frac{-2}{6x^{2}+7x+2} + \frac{18x^{2}+27x+14}{(3x+2)(3x+4)(2x+1)}`
  - answer: `\frac{3}{3x+4},\; x \neq -\frac{2}{3}, -\frac{1}{2}`

### D=22

- seed 101:
  - prompt: `\frac{-18x^{2}+30x-16}{(4x-1)(3x-4)(3x+2)(3x+4)(2x-1)(2x-5)} + \frac{1}{(4x-1)(3x-4)(3x+2)(2x-1)(2x-5)}`
  - answer: `\frac{-3}{(4x-1)(3x+2)(3x+4)(2x-5)},\; x \neq \frac{1}{2}, \frac{4}{3}`
- seed 207:
  - prompt: `\frac{1}{3x-1} + \frac{-6x^{2}+4x+5}{(3x-1)(3x-2)(2x+5)}`
  - answer: `\frac{5}{(3x-2)(2x+5)},\; x \neq \frac{1}{3}, \frac{3}{2}`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 8.3 Add and Subtract Rational Expressions with a Common Denominator

- https://openstax.org/books/elementary-algebra-2e/pages/8-3-add-and-subtract-rational-expressions-with-a-common-denominator
- Mined examples:
  - Example 8.30: Add: $\frac{5}{18} + \frac{7}{18} .$
  - Example 8.31: Add: $\frac{3 y}{4 y - 3} + \frac{7}{4 y - 3} .$
  - Example 8.32: Add: $\frac{7 x + 12}{x + 3} + \frac{x^{2}}{x + 3} .$
  - Example 8.33: Subtract: $\frac{n^{2}}{n - 10} - \frac{100}{n - 10} .$

### Elementary Algebra 2e — 8.4 Add and Subtract Rational Expressions with Unlike Denominators

- https://openstax.org/books/elementary-algebra-2e/pages/8-4-add-and-subtract-rational-expressions-with-unlike-denominators
- Mined examples:
  - Example 8.38: Find the LCD for $\frac{8}{x^{2} - 2 x - 3} , \frac{3 x}{x^{2} + 4 x + 3}$ .
  - Example 8.39: Rewrite as equivalent rational expressions with denominator $(x + 1) (x - 3) (x + 3)$ : $\frac{8}{x^{2} - 2 x - 3} , \frac{3 x}{x^{2} + 4 x + 3} .$
  - Example 8.40: Add: $\frac{7}{12} + \frac{5}{18} .$
  - Example 8.41: Add: $\frac{5}{12 x^{2} y} + \frac{4}{21 x y^{2}} .$

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Proposed engine (reuse vs new)

Reuse AddSubCancel / rational_skeleton (already skeletoned). One leaf covers 8.3+8.4 — D unlocks unlike dens.

_Proposal only. No engine implementation in this notes pass._
