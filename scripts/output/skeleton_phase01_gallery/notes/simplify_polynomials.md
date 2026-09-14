# `simplify_polynomials` — Simplifying polynomials

- **Course:** Algebra 1
- **Category:** Algebra 1 — Polynomials
- **Generator:** `simplify_polynomials`
- **Already on skeleton?** yes
- **Old-path extra settings: `{"use_sample_expand_simplify": true}`.**

## What the question should look like (D=0 vs high D)

Combine like terms to standard form (one polynomial, not a sum of two grouped polys). D=0: 3x²+5x². High D: distribute leftover then combine.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101 (pattern=`PolySimplify`):
  - prompt: `2 + x^{2}`
  - answer: `x^{2} + 2`
- seed 207 (pattern=`PolySimplify`):
  - prompt: `2x^{2} + 2`
  - answer: `2x^{2} + 2`

### D=8

- seed 101 (pattern=`PolySimplify`):
  - prompt: `5x^{3} + 2x^{2} - x - 3x^{3}`
  - answer: `2x^{3} + 2x^{2} - x`
- seed 207 (pattern=`PolySimplify`):
  - prompt: `-5 + 6 - x^{2} + 3x^{3}`
  - answer: `3x^{3} - x^{2} + 1`

### D=16

- seed 101 (pattern=`PolySimplify`):
  - prompt: `x^{4} + 3x^{3} + x^{2} + 7 + 3\left(x^{4} - 1\right)`
  - answer: `4x^{4} + 3x^{3} + x^{2} + 4`
- seed 207 (pattern=`PolySimplify`):
  - prompt: `2\left(x^{4} + 1\right) - 2\left(x^{4} + 2\right) + x^{4} + x^{3} - 2x + 5`
  - answer: `x^{4} + x^{3} - 2x + 3`

### D=22

- seed 101 (pattern=`PolySimplify`):
  - prompt: `x^{4} + 3x^{3} + x^{2} + 7 + 3\left(x^{4} - 1\right)`
  - answer: `4x^{4} + 3x^{3} + x^{2} + 4`
- seed 207 (pattern=`PolySimplify`):
  - prompt: `2\left(x^{4} + 1\right) - 2\left(x^{4} + 2\right) + x^{4} + x^{3} - 2x + 5`
  - answer: `x^{4} + x^{3} - 2x + 3`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 6.1 Add and Subtract Polynomials

- https://openstax.org/books/elementary-algebra-2e/pages/6-1-add-and-subtract-polynomials
- Mined examples:
  - Example 6.1: Determine whether each polynomial is a monomial, binomial, trinomial, or other polynomial. ⓐ $4 y^{2} - 8 y - 6$ ⓑ $−5 a^{4} b^{2}$ ⓒ $2 x^{5} - 5 x^{3} - 9 x^{2} + 3 x + 4$ ⓓ $13 - 5 m^{3}$ ⓔ $q$
  - Example 6.2: Find the degree of the following polynomials. ⓐ $10 y$ ⓑ $4 x^{3} - 7 x + 5$ ⓒ $−15$ ⓓ $−8 b^{2} + 9 b - 2$ ⓔ $8 x y^{2} + 2 y$
  - Example 6.3: Add: $25 y^{2} + 15 y^{2}$ .
  - Example 6.4: Subtract: $16 p - (−7 p)$ .
- Shape: Add: 25y²+15y²; combine like terms before grouping two polynomials.

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Gallery section slug: `simplify_polynomials` (type_id or alias).

## Proposed engine (reuse vs new)

Reuse AffineInflate expand/simplify or PolyAddSub leftover. Already on skeleton as simplify_polynomials.

_Proposal only. No engine implementation in this notes pass._
