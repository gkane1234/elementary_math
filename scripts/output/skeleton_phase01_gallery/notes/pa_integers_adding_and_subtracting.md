# `pa_integers_adding_and_subtracting` — Adding and subtracting

- **Course:** Prealgebra (PA catalog)
- **Category:** Pre-Algebra — Integers, Decimals, and Fractions
- **Generator:** `pa_integers_adding_and_subtracting`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

D=0: two small same-sign addends (5+3 or −2+(−4)). High D: unlike signs, subtract as add-opposite, 3+ addends, parentheses, evaluate a variable expression.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `3 + 6`
  - answer: `9`
- seed 207:
  - prompt: `-3 - 8`
  - answer: `-11`

### D=8

- seed 101:
  - prompt: `29 + 5`
  - answer: `34`
- seed 207:
  - prompt: `-20 - 37`
  - answer: `-57`

### D=16

- seed 101:
  - prompt: `39 - 8`
  - answer: `31`
- seed 207:
  - prompt: `90 - 59`
  - answer: `31`

### D=22

- seed 101:
  - prompt: `117 + 24`
  - answer: `141`
- seed 207:
  - prompt: `-78 - 147`
  - answer: `-225`

## OpenStax examples + chapter/section cites

### Prealgebra 2e — 3.2 Add Integers

- https://openstax.org/books/prealgebra-2e/pages/3-2-add-integers
- Mined examples:
  - Example 3.14: Model: $5 + 3 .$
  - Example 3.15: Model: $−5 + (−3) .$
  - Example 3.16: Model: $−5 + 3 .$
  - Example 3.17: Model: $5 + (−3) .$

### Prealgebra 2e — 3.3 Subtract Integers

- https://openstax.org/books/prealgebra-2e/pages/3-3-subtract-integers
- Mined examples:
  - Example 3.30: Model: $5 - 3 .$
  - Example 3.31: Model: $−5 - (−3) .$
  - Example 3.32: Model: $−5 - 3 .$
  - Example 3.33: Model: $5 - (−3) .$

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Old path can dump a bare equation / identity instead of the named skill.
- Story variety thin (one Mad-Lib / single vehicle) vs OpenStax frames.

## Proposed engine (reuse vs new)

Reuse integer-ops number engine (pa_integers_adding_and_subtracting). Do not fold into affine.

_Proposal only. No engine implementation in this notes pass._
