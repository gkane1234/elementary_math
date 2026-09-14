# `pa_writing_numbers_with_words` — Writing numbers with words

- **Course:** Prealgebra (PA catalog)
- **Category:** Pre-Algebra — Integers, Decimals, and Fractions
- **Generator:** `writing_numbers_with_words`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

D=0: two- or three-digit whole numbers in words. High D: decimals (and/or large place names) matching OpenStax 5.1 write-in-words items.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{Write } 4 \text{ in words.}`
  - answer: `\text{four}`
- seed 207:
  - prompt: `\text{Write } 1 \text{ in words.}`
  - answer: `\text{one}`

### D=8

- seed 101:
  - prompt: `\text{Write } 934 \text{ in words.}`
  - answer: `\text{nine hundred thirty-four}`
- seed 207:
  - prompt: `\text{Write } 313 \text{ in words.}`
  - answer: `\text{three hundred thirteen}`

### D=16

- seed 101:
  - prompt: `\text{Write } 30578 \text{ in words.}`
  - answer: `\text{thirty thousand five hundred seventy-eight}`
- seed 207:
  - prompt: `\text{Write } 67634 \text{ in words.}`
  - answer: `\text{sixty-seven thousand six hundred thirty-four}`

### D=22

- seed 101:
  - prompt: `\text{Write in numerals: } \text{nine hundred twenty-one thousand five hundred eighteen}`
  - answer: `921518`
- seed 207:
  - prompt: `\text{Write in numerals: } \text{eight hundred fifty-three thousand nine hundred one}`
  - answer: `853901`

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

Reuse writing_numbers_with_words. No new engine.

_Proposal only. No engine implementation in this notes pass._
