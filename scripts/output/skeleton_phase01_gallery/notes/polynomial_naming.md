# `polynomial_naming` — Naming

> **UNCLEAR** — Old path names by degree only (quadratic/cubic/quartic). OpenStax EA 6.1 also classifies monomial/binomial/trinomial and finds degree of a given polynomial.

- **Course:** Algebra 1
- **Category:** Algebra 1 — Polynomials
- **Generator:** `polynomial_naming`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Name monomial/binomial/trinomial and/or degree. D=0: 3x+1 → binomial degree 1. High D: more terms, two variables, constant as degree 0.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{Name the polynomial: } x^{2} + 2`
  - answer: `\text{quadratic}`
- seed 207:
  - prompt: `\text{Name the polynomial: } 2x^{2} + 3`
  - answer: `\text{quadratic}`

### D=8

- seed 101:
  - prompt: `\text{Name the polynomial: } 2x^{3} + x^{2} + 2`
  - answer: `\text{cubic}`
- seed 207:
  - prompt: `\text{Name the polynomial: } x^{3} + 2x^{2} + 2`
  - answer: `\text{cubic}`

### D=16

- seed 101:
  - prompt: `\text{Name the polynomial: } 3x^{4} + 2x^{3} + x + 4`
  - answer: `\text{quartic}`
- seed 207:
  - prompt: `\text{Name the polynomial: } x^{4} + 3x^{3} + x - 1`
  - answer: `\text{quartic}`

### D=22

- seed 101:
  - prompt: `\text{Name the polynomial: } 3x^{4} + 2x^{3} + x + 4`
  - answer: `\text{quartic}`
- seed 207:
  - prompt: `\text{Name the polynomial: } x^{4} + 3x^{3} + x - 1`
  - answer: `\text{quartic}`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 6.1 Add and Subtract Polynomials

- https://openstax.org/books/elementary-algebra-2e/pages/6-1-add-and-subtract-polynomials
- Mined examples:
  - Example 6.1: Determine whether each polynomial is a monomial, binomial, trinomial, or other polynomial. ⓐ $4 y^{2} - 8 y - 6$ ⓑ $−5 a^{4} b^{2}$ ⓒ $2 x^{5} - 5 x^{3} - 9 x^{2} + 3 x + 4$ ⓓ $13 - 5 m^{3}$ ⓔ $q$
  - Example 6.2: Find the degree of the following polynomials. ⓐ $10 y$ ⓑ $4 x^{3} - 7 x + 5$ ⓒ $−15$ ⓓ $−8 b^{2} + 9 b - 2$ ⓔ $8 x y^{2} + 2 y$
  - Example 6.3: Add: $25 y^{2} + 15 y^{2}$ .
  - Example 6.4: Subtract: $16 p - (−7 p)$ .
- Shape: Classify 4y²−8y−6; find degree of −8b²+9b−2.

## Variety notes

**UNCLEAR** — Old path names by degree only (quadratic/cubic/quartic). OpenStax EA 6.1 also classifies monomial/binomial/trinomial and finds degree of a given polynomial.

## Limitations

- UNCLEAR / LIMITATIONS: degree-only naming; OpenStax also monomial/binomial/trinomial.
- NOT_IMPLEMENTED term-count classification until gold locked.

## Proposed engine (reuse vs new)

Reuse polynomial_naming. Thin classifier — not PolyAddSub.

_Proposal only. No engine implementation in this notes pass._
