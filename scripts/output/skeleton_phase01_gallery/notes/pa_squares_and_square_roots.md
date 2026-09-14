# `pa_squares_and_square_roots` — Squares and square roots

- **Course:** Prealgebra (PA catalog)
- **Category:** Pre-Algebra — Factors and Exponents
- **Generator:** `pa_squares_and_square_roots`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

D=0: perfect squares / √n for 1–12. High D: estimate non-perfects or simplify √(a²b) at PA level (not full radical algebra).

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\sqrt{100}`
  - answer: `10`
- seed 207:
  - prompt: `\sqrt{16}`
  - answer: `4`

### D=8

- seed 101:
  - prompt: `\sqrt{256}`
  - answer: `16`
- seed 207:
  - prompt: `\sqrt{361}`
  - answer: `19`

### D=16

- seed 101:
  - prompt: `\sqrt{30}`
  - answer: `\sqrt{30}`
- seed 207:
  - prompt: `\sqrt{2}`
  - answer: `\sqrt{2}`

### D=22

- seed 101:
  - prompt: `\sqrt{30}`
  - answer: `\sqrt{30}`
- seed 207:
  - prompt: `\sqrt{2}`
  - answer: `\sqrt{2}`

## OpenStax examples + chapter/section cites

### Prealgebra 2e — 5.7 Simplify and Use Square Roots

- https://openstax.org/books/prealgebra-2e/pages/5-7-simplify-and-use-square-roots
- Shape: √36=6; approximate √5; simplify √48 → 4√3 (PA-lite).

### Elementary Algebra 2e — 9.1 Simplify and Use Square Roots

- https://openstax.org/books/elementary-algebra-2e/pages/9-1-simplify-and-use-square-roots
- Mined examples:
  - Example 9.1: Simplify: ⓐ $\sqrt{36}$ ⓑ $\sqrt{196}$ ⓒ $− \sqrt{81}$ ⓓ $− \sqrt{289}$ .
  - Example 9.2: Simplify: ⓐ $\sqrt{−169}$ ⓑ $− \sqrt{64}$ .
  - Example 9.3: Simplify: ⓐ $\sqrt{25} + \sqrt{144}$ ⓑ $\sqrt{25 + 144}$ .
  - Example 9.4: Estimate $\sqrt{60}$ between two consecutive whole numbers.

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Old path can dump a bare equation / identity instead of the named skill.
- Story variety thin (one Mad-Lib / single vehicle) vs OpenStax frames.

## Proposed engine (reuse vs new)

Reuse pa_squares_and_square_roots (number). Do not jump to A1 radical engine.

_Proposal only. No engine implementation in this notes pass._
