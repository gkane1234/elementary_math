# `scientific_notation_add_subtract` — Addition/Subtraction and scientific notation

- **Course:** Algebra 1
- **Category:** Algebra 1 — Exponents
- **Generator:** `scientific_notation_add_subtract`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Add/subtract in scientific notation (align powers of 10). D=0: same exponent. High D: rewrite one power first.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101 (pattern=`NumberCore`):
  - prompt: `(6.9 \times 10^{2}) + (1.6 \times 10^{2})`
  - answer: `8.5 \times 10^{2}`
- seed 207 (pattern=`NumberCore`):
  - prompt: `(1.3 \times 10^{1}) - (9.6 \times 10^{1})`
  - answer: `-8.3 \times 10^{1}`

### D=8

- seed 101 (pattern=`NumberCore`):
  - prompt: `(4.67 \times 10^{6}) + (5.78 \times 10^{5})`
  - answer: `5.248 \times 10^{6}`
- seed 207 (pattern=`NumberCore`):
  - prompt: `(1.24 \times 10^{0}) - (7.89 \times 10^{-1})`
  - answer: `4.51 \times 10^{-1}`

### D=16

- seed 101 (pattern=`NumberCore`):
  - prompt: `(9.834 \times 10^{-1}) - (6.876 \times 10^{-5})`
  - answer: `9.83331 \times 10^{-1}`
- seed 207 (pattern=`NumberCore`):
  - prompt: `(4.633 \times 10^{6}) + (3.621 \times 10^{2})`
  - answer: `4.63336 \times 10^{6}`

### D=22

- seed 101 (pattern=`NumberCore`):
  - prompt: `(6.876 \times 10^{10}) + (8.653 \times 10^{6})`
  - answer: `6.87687 \times 10^{10}`
- seed 207 (pattern=`NumberCore`):
  - prompt: `(1.397 \times 10^{-2}) + (6.678 \times 10^{-6})`
  - answer: `1.39767 \times 10^{-2}`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 6.7 Integer Exponents and Scientific Notation

- https://openstax.org/books/elementary-algebra-2e/pages/6-7-integer-exponents-and-scientific-notation
- Mined examples:
  - Example 6.89: Simplify: ⓐ $4^{−2}$ ⓑ $10^{−3} .$
  - Example 6.90: Simplify: ⓐ $\frac{1}{y^{−4}}$ ⓑ $\frac{1}{3^{−2}} .$
  - Example 6.91: Simplify: ⓐ $\left(\right. \frac{5}{7} \left.\right)^{−2}$ ⓑ $\left(\right. - \frac{2 x}{y} \left.\right)^{−3} .$
  - Example 6.92: Simplify: ⓐ $(−3)^{−2}$ ⓑ $− 3^{−2}$ ⓒ $\left(\right. - \frac{1}{3} \left.\right)^{−2}$ ⓓ $− \left(\right. \frac{1}{3} \left.\right)^{−2} .$
- Shape: Add/subtract after writing both with the same power of 10.

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- NOT_IMPLEMENTED: no phase-01 gallery section yet (stub added this pass) or generation not skeleton-wired.
- LIMITATIONS: gallery stub + notes only until an existing core can match old path honestly.

## Proposed engine (reuse vs new)

Reuse scientific_notation_add_subtract.

_Proposal only. No engine implementation in this notes pass._
