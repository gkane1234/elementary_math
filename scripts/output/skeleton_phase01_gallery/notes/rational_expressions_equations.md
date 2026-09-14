# `rational_expressions_equations` — Rational equations

- **Course:** Algebra 1
- **Category:** Algebra 1 — Rational Expressions
- **Generator:** `rational_equations`
- **Already on skeleton?** yes
- **Old-path extra settings: `{"use_constructive_rational": true}`.**

## What the question should look like (D=0 vs high D)

Solve a rational equation; check extraneous. D=0: 1/x=1/2 or a/x=b. High D: LCD of two binomials.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\frac{x - 6}{4} = 1`
  - answer: `x = 10`
- seed 207:
  - prompt: `\frac{x + 4}{3} = -6`
  - answer: `x = -22`

### D=8

- seed 101:
  - prompt: `\frac{15}{x} = \frac{5}{3}`
  - answer: `x = 9`
- seed 207:
  - prompt: `\frac{-15}{x - 6} - 5 = -10`
  - answer: `x = 9`

### D=16

- seed 101:
  - prompt: `\frac{-4}{x + 10} + \frac{4}{x - 6} = -1`
  - answer: `x = -2`
- seed 207:
  - prompt: `\frac{-3}{x + 7} - \frac{5}{x - 1} = 2`
  - answer: `x = -9 \text{ or } x = -1`

### D=22

- seed 101:
  - prompt: `\frac{-4}{x + 10} + \frac{4}{x - 6} = -1`
  - answer: `x = -2`
- seed 207:
  - prompt: `\frac{-3}{x + 7} - \frac{5}{x - 1} = 2`
  - answer: `x = -9 \text{ or } x = -1`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 8.6 Solve Rational Equations

- https://openstax.org/books/elementary-algebra-2e/pages/8-6-solve-rational-equations
- Mined examples:
  - Example 8.59: How to Solve Equations with Rational Expressions Solve: $\frac{1}{x} + \frac{1}{3} = \frac{5}{6} .$
  - Example 8.60: Solve: $1 - \frac{5}{y} = - \frac{6}{y^{2}} .$
  - Example 8.61: Solve: $\frac{5}{3 u - 2} = \frac{3}{2 u} .$
  - Example 8.62: Solve: $\frac{2}{p + 2} + \frac{4}{p - 2} = \frac{p - 1}{p^{2} - 4} .$

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Proposed engine (reuse vs new)

Reuse EqCancel / rational_skeleton (already skeletoned).

_Proposal only. No engine implementation in this notes pass._
