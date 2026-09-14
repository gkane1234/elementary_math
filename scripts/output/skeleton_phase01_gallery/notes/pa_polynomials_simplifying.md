# `pa_polynomials_simplifying` — Simplifying

- **Course:** Prealgebra (PA catalog)
- **Category:** Pre-Algebra — Beginning Polynomials
- **Generator:** `simplify_polynomials`
- **Already on skeleton?** yes
- **Old-path extra settings: `{"use_sample_expand_simplify": true}`.**

## What the question should look like (D=0 vs high D)

Combine like terms in a polynomial (degree may be 2+). D=0: 3x²+5x² or a few linear+const terms. High D: more terms / subtraction of a grouped polynomial.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `2 + 3x - x^{2}`
  - answer: `-x^{2} + 3x + 2`
- seed 207:
  - prompt: `1 - 2x - 3x^{2}`
  - answer: `-3x^{2} - 2x + 1`

### D=8

- seed 101:
  - prompt: `-4x^{3} + 3x^{3} + 2 + 3x`
  - answer: `-x^{3} + 3x + 2`
- seed 207:
  - prompt: `2 - 1 - 2x - 3x^{3}`
  - answer: `-3x^{3} - 2x + 1`

### D=16

- seed 101:
  - prompt: `-x^{4} - 3x + 4x^{4}`
  - answer: `3x^{4} - 3x`
- seed 207:
  - prompt: `-5x^{4} + 3x^{4} - x^{4} + 1 - 2x`
  - answer: `-3x^{4} - 2x + 1`

### D=22

- seed 101:
  - prompt: `-x^{4} - 3x + 4x^{4}`
  - answer: `3x^{4} - 3x`
- seed 207:
  - prompt: `-5x^{4} + 3x^{4} - x^{4} + 1 - 2x`
  - answer: `-3x^{4} - 2x + 1`

## OpenStax examples + chapter/section cites

### Prealgebra 2e — 10.1 Add and Subtract Polynomials

- https://openstax.org/books/prealgebra-2e/pages/10-1-add-and-subtract-polynomials
- Shape: Simplify by combining like terms before add/sub of two polynomials.

### Elementary Algebra 2e — 6.1 Add and Subtract Polynomials

- https://openstax.org/books/elementary-algebra-2e/pages/6-1-add-and-subtract-polynomials
- Mined examples:
  - Example 6.1: Determine whether each polynomial is a monomial, binomial, trinomial, or other polynomial. ⓐ $4 y^{2} - 8 y - 6$ ⓑ $−5 a^{4} b^{2}$ ⓒ $2 x^{5} - 5 x^{3} - 9 x^{2} + 3 x + 4$ ⓓ $13 - 5 m^{3}$ ⓔ $q$
  - Example 6.2: Find the degree of the following polynomials. ⓐ $10 y$ ⓑ $4 x^{3} - 7 x + 5$ ⓒ $−15$ ⓓ $−8 b^{2} + 9 b - 2$ ⓔ $8 x y^{2} + 2 y$
  - Example 6.3: Add: $25 y^{2} + 15 y^{2}$ .
  - Example 6.4: Subtract: $16 p - (−7 p)$ .

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Old path can dump a bare equation / identity instead of the named skill.
- Story variety thin (one Mad-Lib / single vehicle) vs OpenStax frames.

## Proposed engine (reuse vs new)

Reuse AffineInflate expand/simplify if old path is linear; else poly_skeleton / construct_poly. Check live samples before choosing.

_Proposal only. No engine implementation in this notes pass._
