# `pa_fractions_add_unlike` — Adding fractions (unlike denominators)

- **Course:** Prealgebra (PA catalog)
- **Category:** Pre-Algebra — Integers, Decimals, and Fractions
- **Generator:** `g6_fraction_add_unlike`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

D=0: two fractions whose LCD is one of the denoms (1/2+1/6). High D: LCD is a product, 3+ terms, cancel after.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\frac{3}{2} + \frac{1}{3}`
  - answer: `\frac{11}{6}`
- seed 207:
  - prompt: `\frac{3}{4} + \frac{1}{2}`
  - answer: `\frac{5}{4}`

### D=8

- seed 101:
  - prompt: `-\frac{8}{3} + \frac{5}{6}`
  - answer: `-\frac{11}{6}`
- seed 207:
  - prompt: `\frac{37}{6} - \frac{3}{2}`
  - answer: `\frac{14}{3}`

### D=16

- seed 101:
  - prompt: `-\frac{50}{11} - \frac{4}{5}`
  - answer: `-\frac{294}{55}`
- seed 207:
  - prompt: `\frac{69}{10} + \frac{14}{3}`
  - answer: `\frac{347}{30}`

### D=22

- seed 101:
  - prompt: `-\frac{60}{11} + \frac{12}{5}`
  - answer: `-\frac{168}{55}`
- seed 207:
  - prompt: `\frac{151}{10} - \frac{46}{15}`
  - answer: `\frac{361}{30}`

## OpenStax examples + chapter/section cites

### Prealgebra 2e — 4.5 Add and Subtract Fractions with Different Denominators

- https://openstax.org/books/prealgebra-2e/pages/4-5-add-and-subtract-fractions-with-different-denominators
- Mined examples:
  - Example 4.63: Find the LCD for the fractions $\frac{7}{12}$ and $\frac{5}{18} .$
  - Example 4.64: Find the least common denominator for the fractions $\frac{8}{15}$ and $\frac{11}{24} .$
  - Example 4.65: Convert $\frac{1}{4}$ and $\frac{1}{6}$ to equivalent fractions with denominator $12 ,$ their LCD.
  - Example 4.66: Convert $\frac{8}{15}$ and $\frac{11}{24}$ to equivalent fractions with denominator $120 ,$ their LCD.

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Old path can dump a bare equation / identity instead of the named skill.
- Story variety thin (one Mad-Lib / single vehicle) vs OpenStax frames.

## Proposed engine (reuse vs new)

Reuse g6_fraction_add_unlike (number).

_Proposal only. No engine implementation in this notes pass._
