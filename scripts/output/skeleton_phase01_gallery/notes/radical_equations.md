# `radical_equations` — Equations

- **Course:** Algebra 1
- **Category:** Algebra 1 — Radical Expressions
- **Generator:** `radical_equations`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Solve √(expr)=k; isolate then square; check extraneous. D=0: √x=4. High D: √(ax+b)=cx+d.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\sqrt{4x + 9} = 3`
  - answer: `x = 0`
- seed 207:
  - prompt: `\sqrt{3x + 21} + 4 = 10`
  - answer: `x = 5`

### D=8

- seed 101:
  - prompt: `3\sqrt{3x + 4} + 4 = 19`
  - answer: `x = 7`
- seed 207:
  - prompt: `5\sqrt{2x + 26} + 2 = 32`
  - answer: `x = 5`

### D=16

- seed 101:
  - prompt: `\sqrt{x + 18} + \sqrt{x + 2} = 8`
  - answer: `x = 7`
- seed 207:
  - prompt: `\sqrt{3x + 25} = \sqrt{3x + 1} + 4`
  - answer: `x = 0`

### D=22

- seed 101:
  - prompt: `\sqrt{x + 18} + \sqrt{x + 2} = 8`
  - answer: `x = 7`
- seed 207:
  - prompt: `\sqrt{3x + 25} = \sqrt{3x + 1} + 4`
  - answer: `x = 0`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 9.6 Solve Equations with Square Roots

- https://openstax.org/books/elementary-algebra-2e/pages/9-6-solve-equations-with-square-roots
- Mined examples:
  - Example 9.74: For the equation $\sqrt{x + 2} = x$ : ⓐ Is $x = 2$ a solution? ⓑ Is $x = −1$ a solution?
  - Example 9.75: How to Solve Radical Equations Solve: $\sqrt{2 x - 1} = 7$ .
  - Example 9.76: Solve: $\sqrt{5 n - 4} - 9 = 0$ .
  - Example 9.77: Solve: $\sqrt{3 y + 5} + 2 = 5$ .

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Gallery section slug: `radical_equations` (type_id or alias).

## Proposed engine (reuse vs new)

Reuse radical_equations. Not EqCancel (that's rational dens).

_Proposal only. No engine implementation in this notes pass._
