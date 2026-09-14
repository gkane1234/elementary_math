# `pa_integers_multiplying` — Multiplying

- **Course:** Prealgebra (PA catalog)
- **Category:** Pre-Algebra — Integers, Decimals, and Fractions
- **Generator:** `g6_integer_multiply`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

D=0: two small integers with an obvious sign (−3)(4). High D: three+ factors, or evaluate a product expression with a substituted integer.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `-2 \cdot 3`
  - answer: `-6`
- seed 207:
  - prompt: `8 \cdot (-1)`
  - answer: `-8`

### D=8

- seed 101:
  - prompt: `34 \cdot (-16)`
  - answer: `-544`
- seed 207:
  - prompt: `24 \cdot 37`
  - answer: `888`

### D=16

- seed 101:
  - prompt: `49 \cdot (-50)`
  - answer: `-2450`
- seed 207:
  - prompt: `30 \cdot 69`
  - answer: `2070`

### D=22

- seed 101:
  - prompt: `138 \cdot (-60)`
  - answer: `-8280`
- seed 207:
  - prompt: `100 \cdot 151`
  - answer: `15100`

## OpenStax examples + chapter/section cites

### Prealgebra 2e — 3.4 Multiply and Divide Integers

- https://openstax.org/books/prealgebra-2e/pages/3-4-multiply-and-divide-integers
- Mined examples:
  - Example 3.47: Multiply each of the following: ⓐ $−9 \cdot 3$ ⓑ $−2 (−5)$ ⓒ $4 (−8)$ ⓓ $7 \cdot 6$
  - Example 3.48: Multiply each of the following: ⓐ $−1 \cdot 7$ ⓑ $−1 (−11)$
  - Example 3.49: Divide each of the following: ⓐ $−27 \div 3$ ⓑ $−100 \div (−4)$
  - Example 3.50: Divide each of the following: ⓐ $16 \div (−1)$ ⓑ $−20 \div (−1)$

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Old path can dump a bare equation / identity instead of the named skill.
- Story variety thin (one Mad-Lib / single vehicle) vs OpenStax frames.

## Proposed engine (reuse vs new)

Reuse g6_integer_multiply. Shared G6/PA number engine.

_Proposal only. No engine implementation in this notes pass._
