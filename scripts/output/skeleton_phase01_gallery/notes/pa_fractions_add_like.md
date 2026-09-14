# `pa_fractions_add_like` — Adding fractions (like denominators)

- **Course:** Prealgebra (PA catalog)
- **Category:** Pre-Algebra — Integers, Decimals, and Fractions
- **Generator:** `g6_fraction_add_like`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

D=0: two unit-ish fractions same denom, already simplified or one cancel after. High D: larger numerators, simplify after, maybe three terms. No mixed numbers (4.6 gap).

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `1 + \frac{3}{2}`
  - answer: `\frac{5}{2}`
- seed 207:
  - prompt: `1 + \frac{3}{4}`
  - answer: `\frac{7}{4}`

### D=8

- seed 101:
  - prompt: `-\frac{8}{3} + \frac{29}{6}`
  - answer: `\frac{13}{6}`
- seed 207:
  - prompt: `\frac{37}{6} - 2`
  - answer: `\frac{25}{6}`

### D=16

- seed 101:
  - prompt: `-\frac{50}{11} + \frac{39}{11}`
  - answer: `-1`
- seed 207:
  - prompt: `\frac{69}{10} + \frac{36}{5}`
  - answer: `\frac{141}{10}`

### D=22

- seed 101:
  - prompt: `-\frac{60}{11} + \frac{117}{11}`
  - answer: `\frac{57}{11}`
- seed 207:
  - prompt: `\frac{151}{10} - \frac{23}{5}`
  - answer: `\frac{21}{2}`

## OpenStax examples + chapter/section cites

### Prealgebra 2e — 4.4 Add and Subtract Fractions with Common Denominators

- https://openstax.org/books/prealgebra-2e/pages/4-4-add-and-subtract-fractions-with-common-denominators
- Mined examples:
  - Example 4.52: Use a model to find the sum $\frac{3}{8} + \frac{2}{8} .$
  - Example 4.53: Find the sum: $\frac{3}{5} + \frac{1}{5} .$
  - Example 4.54: Find the sum: $\frac{x}{3} + \frac{2}{3} .$
  - Example 4.55: Find the sum: $- \frac{9}{d} + \frac{3}{d} .$

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Old path can dump a bare equation / identity instead of the named skill.
- Story variety thin (one Mad-Lib / single vehicle) vs OpenStax frames.

## Proposed engine (reuse vs new)

Reuse g6_fraction_add_like (number). PA is a thin alias.

_Proposal only. No engine implementation in this notes pass._
