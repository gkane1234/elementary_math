# `scientific_notation_operations` — Operations and scientific notation

- **Course:** Algebra 1
- **Category:** Pre-Algebra — Factors and Exponents
- **Generator:** `scientific_notation_operations`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Multiply/divide numbers in scientific notation; leave answer in sci form. D=0: (2×10³)(3×10²). High D: ÷ and negative exponents.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101 (pattern=`NumberCore`):
  - prompt: `(7.9 \times 10^{1}) \times (6.9 \times 10^{2})`
  - answer: `5.451 \times 10^{4}`
- seed 207 (pattern=`NumberCore`):
  - prompt: `(3 \times 10^{1}) \times (9.6 \times 10^{1})`
  - answer: `2.88 \times 10^{3}`

### D=8

- seed 101 (pattern=`NumberCore`):
  - prompt: `(8.39 \times 10^{5}) \times (7.57 \times 10^{4})`
  - answer: `6.35123 \times 10^{10}`
- seed 207 (pattern=`NumberCore`):
  - prompt: `(5.77 \times 10^{-1}) \times (8.55 \times 10^{7})`
  - answer: `4.93335 \times 10^{7}`

### D=16

- seed 101 (pattern=`NumberCore`):
  - prompt: `(6.757 \times 10^{3}) \times (9.931 \times 10^{-7})`
  - answer: `6.71038 \times 10^{-3}`
- seed 207 (pattern=`NumberCore`):
  - prompt: `(8.975 \times 10^{-3}) \times (5.697 \times 10^{3})`
  - answer: `5.11306 \times 10^{1}`

### D=22

- seed 101 (pattern=`NumberCore`):
  - prompt: `(9.124 \times 10^{6}) \times (6.757 \times 10^{3})`
  - answer: `6.16509 \times 10^{10}`
- seed 207 (pattern=`NumberCore`):
  - prompt: `(6.247 \times 10^{-6}) \times (8.975 \times 10^{10})`
  - answer: `5.60668 \times 10^{5}`

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

Reuse scientific_notation_operations.

_Proposal only. No engine implementation in this notes pass._
