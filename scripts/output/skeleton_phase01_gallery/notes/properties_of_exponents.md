# `properties_of_exponents` — Properties of exponents

- **Course:** Algebra 1
- **Category:** Pre-Algebra — Factors and Exponents
- **Generator:** `properties_of_exponents`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Simplify with product/quotient/power rules. D=0: x³·x². High D: negative exponents, multi-base.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `a^{2} \cdot a^{2}`
  - answer: `a^{4}`
- seed 207:
  - prompt: `a^{1} \cdot a^{1}`
  - answer: `a^{2}`

### D=8

- seed 101:
  - prompt: `\left(x^{5}\right)^{3}`
  - answer: `x^{15}`
- seed 207:
  - prompt: `\left(a^{5}\right)^{2}`
  - answer: `a^{10}`

### D=16

- seed 101:
  - prompt: `\frac{a^{7}}{a^{8}}`
  - answer: `a^{-1}`
- seed 207:
  - prompt: `\frac{a^{4}}{a^{1}}`
  - answer: `a^{3}`

### D=22

- seed 101:
  - prompt: `x^{9} - x^{6}`
  - answer: `x^{9} - x^{6}`
- seed 207:
  - prompt: `a^{11} + a^{10}`
  - answer: `a^{11} + a^{10}`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 6.2 Use Multiplication Properties of Exponents

- https://openstax.org/books/elementary-algebra-2e/pages/6-2-use-multiplication-properties-of-exponents
- Mined examples:
  - Example 6.16: Simplify: ⓐ $4^{3}$ ⓑ $7^{1}$ ⓒ $\left(\right. \frac{5}{6} \left.\right)^{2}$ ⓓ $(0.63)^{2} .$
  - Example 6.17: Simplify: ⓐ $(−5)^{4}$ ⓑ $− 5^{4} .$
  - Example 6.18: Simplify: $y^{5} \cdot y^{6} .$
  - Example 6.19: Simplify: ⓐ $2^{5} \cdot 2^{9}$ ⓑ $3 \cdot 3^{4} .$

### Elementary Algebra 2e — 6.7 Integer Exponents and Scientific Notation

- https://openstax.org/books/elementary-algebra-2e/pages/6-7-integer-exponents-and-scientific-notation
- Mined examples:
  - Example 6.89: Simplify: ⓐ $4^{−2}$ ⓑ $10^{−3} .$
  - Example 6.90: Simplify: ⓐ $\frac{1}{y^{−4}}$ ⓑ $\frac{1}{3^{−2}} .$
  - Example 6.91: Simplify: ⓐ $\left(\right. \frac{5}{7} \left.\right)^{−2}$ ⓑ $\left(\right. - \frac{2 x}{y} \left.\right)^{−3} .$
  - Example 6.92: Simplify: ⓐ $(−3)^{−2}$ ⓑ $− 3^{−2}$ ⓒ $\left(\right. - \frac{1}{3} \left.\right)^{−2}$ ⓓ $− \left(\right. \frac{1}{3} \left.\right)^{−2} .$

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- NOT_IMPLEMENTED: no phase-01 gallery section yet (stub added this pass) or generation not skeleton-wired.
- LIMITATIONS: gallery stub + notes only until an existing core can match old path honestly.

## Proposed engine (reuse vs new)

Reuse properties_of_exponents. Do not fold monomial division into polynomial_long_division.

_Proposal only. No engine implementation in this notes pass._
