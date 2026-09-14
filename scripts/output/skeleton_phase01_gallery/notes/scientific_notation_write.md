# `scientific_notation_write` — Writing scientific notation

- **Course:** Algebra 1
- **Category:** Pre-Algebra — Factors and Exponents
- **Generator:** `scientific_notation_write`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Write a number in scientific notation (or expand). D=0: 4500 → 4.5×10³. High D: tiny decimals.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101 (pattern=`NumberCore`):
  - prompt: `\text{Write in scientific notation: } 79`
  - answer: `7.9 \times 10^{1}`
- seed 207 (pattern=`NumberCore`):
  - prompt: `\text{Write in scientific notation: } 30`
  - answer: `3 \times 10^{1}`

### D=8

- seed 101 (pattern=`NumberCore`):
  - prompt: `\text{Write in scientific notation: } 467000`
  - answer: `4.67 \times 10^{5}`
- seed 207 (pattern=`NumberCore`):
  - prompt: `\text{Write in scientific notation: } 0.124`
  - answer: `1.24 \times 10^{-1}`

### D=16

- seed 101 (pattern=`NumberCore`):
  - prompt: `\text{Write in scientific notation: } 8653`
  - answer: `8.653 \times 10^{3}`
- seed 207 (pattern=`NumberCore`):
  - prompt: `\text{Write in scientific notation: } 0.001397`
  - answer: `1.397 \times 10^{-3}`

### D=22

- seed 101 (pattern=`NumberCore`):
  - prompt: `\text{Write in scientific notation: } 6876000`
  - answer: `6.876 \times 10^{6}`
- seed 207 (pattern=`NumberCore`):
  - prompt: `\text{Write in scientific notation: } 0.000001397`
  - answer: `1.397 \times 10^{-6}`

## OpenStax examples + chapter/section cites

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

Reuse scientific_notation_write (number).

_Proposal only. No engine implementation in this notes pass._
