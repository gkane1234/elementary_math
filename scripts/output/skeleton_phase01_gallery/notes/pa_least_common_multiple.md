# `pa_least_common_multiple` — Least common multiple

- **Course:** Prealgebra (PA catalog)
- **Category:** Pre-Algebra — Integers, Decimals, and Fractions
- **Generator:** `g6_least_common_multiple`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

D=0: LCM of two small positives (4 and 6 → 12). High D: three numbers or larger.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{Find the LCM of } 3, 6`
  - answer: `6`
- seed 207:
  - prompt: `\text{Find the LCM of } 2, 8`
  - answer: `8`

### D=8

- seed 101:
  - prompt: `\text{Find the LCM of } 12, 18, 30`
  - answer: `180`
- seed 207:
  - prompt: `\text{Find the LCM of } 12, 18, 30`
  - answer: `180`

### D=16

- seed 101:
  - prompt: `\text{Find the LCM of } 20, 30, 50`
  - answer: `300`
- seed 207:
  - prompt: `\text{Find the LCM of } 12, 18, 30`
  - answer: `180`

### D=22

- seed 101:
  - prompt: `\text{Find the LCM of } 30, 45, 75`
  - answer: `450`
- seed 207:
  - prompt: `\text{Find the LCM of } 12, 18, 30`
  - answer: `180`

## OpenStax examples + chapter/section cites

### Prealgebra 2e — 2.5 Prime Factorization and the Least Common Multiple

- https://openstax.org/books/prealgebra-2e/pages/2-5-prime-factorization-and-the-least-common-multiple
- Shape: LCM(12,18)=36 via primes or listing multiples.

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Old path can dump a bare equation / identity instead of the named skill.
- Story variety thin (one Mad-Lib / single vehicle) vs OpenStax frames.

## Proposed engine (reuse vs new)

Reuse g6_least_common_multiple (number).

_Proposal only. No engine implementation in this notes pass._
