# `pa_fractions_multiply` — Multiplying fractions

- **Course:** Prealgebra (PA catalog)
- **Category:** Pre-Algebra — Integers, Decimals, and Fractions
- **Generator:** `g6_fraction_multiply`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

D=0: two unit fractions or no cancel (1/2·1/3). High D: cancel-before-multiply, improper intermediates. Mixed × and complex fractions (4.3) are a catalog gap.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\frac{3}{4} \cdot \frac{2}{3}`
  - answer: `\frac{1}{2}`
- seed 207:
  - prompt: `\frac{3}{4} \cdot \frac{1}{2}`
  - answer: `\frac{3}{8}`

### D=8

- seed 101:
  - prompt: `5\frac{5}{6} \cdot 4\frac{3}{4}`
  - answer: `\frac{665}{24}`
- seed 207:
  - prompt: `6\frac{1}{2} \cdot 1\frac{3}{8}`
  - answer: `\frac{143}{16}`

### D=16

- seed 101:
  - prompt: `6\frac{4}{11} \cdot 4\frac{5}{7}`
  - answer: `30`
- seed 207:
  - prompt: `7\frac{4}{5} \cdot \frac{4}{5}`
  - answer: `\frac{156}{25}`

### D=22

- seed 101:
  - prompt: `12\frac{7}{11} \cdot 4\frac{5}{7}`
  - answer: `\frac{417}{7}`
- seed 207:
  - prompt: `15\frac{3}{5} \cdot 2\frac{11}{15}`
  - answer: `\frac{1066}{25}`

## OpenStax examples + chapter/section cites

### Prealgebra 2e — 4.2 Multiply and Divide Fractions

- https://openstax.org/books/prealgebra-2e/pages/4-2-multiply-and-divide-fractions
- Mined examples:
  - Example 4.19: Simplify: $\frac{10}{15} .$
  - Example 4.20: Simplify: $- \frac{18}{24} .$
  - Example 4.21: Simplify: $- \frac{56}{32} .$
  - Example 4.22: Simplify: $\frac{210}{385} .$

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Old path can dump a bare equation / identity instead of the named skill.
- Story variety thin (one Mad-Lib / single vehicle) vs OpenStax frames.

## Proposed engine (reuse vs new)

Reuse g6_fraction_multiply (number).

_Proposal only. No engine implementation in this notes pass._
