# `pa_naming_decimal_places_and_rounding` — Naming decimal places and rounding

- **Course:** Prealgebra (PA catalog)
- **Category:** Pre-Algebra — Integers, Decimals, and Fractions
- **Generator:** `place_value_and_rounding`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

D=0: name tenths/hundredths of a short decimal (e.g. 4.7 → tenths) or round to nearest whole/tenth. High D: thousandths–millionths, round to a named place, or expanded form.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{Round } 18.8 \text{ to the nearest whole number.}`
  - answer: `19`
- seed 207:
  - prompt: `\text{What digit is in the tenths place of } 4.6\text{?}`
  - answer: `6`

### D=8

- seed 101:
  - prompt: `\text{Round } 789.995 \text{ to the nearest hundredth.}`
  - answer: `790.00`
- seed 207:
  - prompt: `\text{What digit is in the hundredths place of } 170.12\text{?}`
  - answer: `2`

### D=16

- seed 101:
  - prompt: `\text{Round } 8336.094 \text{ to the nearest hundredth.}`
  - answer: `8336.09`
- seed 207:
  - prompt: `\text{What digit is in the thousandths place of } 2262.252\text{?}`
  - answer: `2`

### D=22

- seed 101:
  - prompt: `\text{What digit is in the hundredths place of } 4954.981\text{?}`
  - answer: `8`
- seed 207:
  - prompt: `\text{Round } 1468.849 \text{ to the nearest tenth.}`
  - answer: `1468.8`

## OpenStax examples + chapter/section cites

### Prealgebra 2e — 5.1 Decimals

- https://openstax.org/books/prealgebra-2e/pages/5-1-decimals
- Mined examples:
  - Example 5.1: Name each decimal: ⓐ $4.3$ ⓑ $2.45$ ⓒ $0.009$ ⓓ $−15.571 .$
  - Example 5.2: Write fourteen and thirty-seven hundredths as a decimal.
  - Example 5.3: Write twenty-four thousandths as a decimal.
  - Example 5.4: Write each of the following decimal numbers as a fraction or a mixed number: ⓐ $4.09$ ⓑ $3.7$ ⓒ $−0.286$

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Old path can dump a bare equation / identity instead of the named skill.
- Story variety thin (one Mad-Lib / single vehicle) vs OpenStax frames.

## Proposed engine (reuse vs new)

Reuse number/place-value generator. No new skeleton. Difficulty already magnitude + place-depth.

_Proposal only. No engine implementation in this notes pass._
