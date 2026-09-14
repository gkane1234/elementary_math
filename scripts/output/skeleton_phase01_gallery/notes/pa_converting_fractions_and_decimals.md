# `pa_converting_fractions_and_decimals` — Converting fractions and decimals

- **Course:** Prealgebra (PA catalog)
- **Category:** Pre-Algebra — Integers, Decimals, and Fractions
- **Generator:** `converting_fractions_and_decimals`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

D=0: terminating tenths/hundredths (3/10 ↔ 0.3). High D: repeating or awkward terminating (3/8, 2/11).

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{Write } \frac{7}{10} \text{ as a decimal.}`
  - answer: `0.7`
- seed 207:
  - prompt: `\text{Write } \frac{3}{10} \text{ as a decimal.}`
  - answer: `0.3`

### D=8

- seed 101:
  - prompt: `\text{Write } 0.8 \text{ as a fraction in simplest form.}`
  - answer: `\frac{4}{5}`
- seed 207:
  - prompt: `\text{Write } \frac{1}{10} \text{ as a decimal.}`
  - answer: `0.1`

### D=16

- seed 101:
  - prompt: `\text{Write } 0.8 \text{ as a fraction in simplest form.}`
  - answer: `\frac{4}{5}`
- seed 207:
  - prompt: `\text{Write } \frac{11}{25} \text{ as a decimal.}`
  - answer: `0.44`

### D=22

- seed 101:
  - prompt: `\text{Write } \frac{9}{20} \text{ as a decimal.}`
  - answer: `0.45`
- seed 207:
  - prompt: `\text{Write } \frac{1}{16} \text{ as a decimal.}`
  - answer: `0.0625`

## OpenStax examples + chapter/section cites

### Prealgebra 2e — 5.3 Decimals and Fractions

- https://openstax.org/books/prealgebra-2e/pages/5-3-decimals-and-fractions
- Mined examples:
  - Example 5.28: Write the fraction $\frac{3}{4}$ as a decimal.
  - Example 5.29: Write the fraction $- \frac{7}{2}$ as a decimal.
  - Example 5.30: Write $\frac{43}{22}$ as a decimal.
  - Example 5.31: Simplify: $\frac{7}{8} + 6.4 .$

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Old path can dump a bare equation / identity instead of the named skill.
- Story variety thin (one Mad-Lib / single vehicle) vs OpenStax frames.

## Proposed engine (reuse vs new)

Reuse converting_fractions_and_decimals (number).

_Proposal only. No engine implementation in this notes pass._
