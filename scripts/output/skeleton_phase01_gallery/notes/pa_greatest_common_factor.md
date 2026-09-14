# `pa_greatest_common_factor` — Greatest common factor

- **Course:** Prealgebra (PA catalog)
- **Category:** Pre-Algebra — Integers, Decimals, and Fractions
- **Generator:** `g6_greatest_common_factor`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

D=0: GCF of two small positives (12 and 18 → 6). High D: three numbers or larger composites; still numeric, not monomial GCF of polynomials.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{Find the GCF of } 7, 14`
  - answer: `7`
- seed 207:
  - prompt: `\text{Find the GCF of } 4, 6`
  - answer: `2`

### D=8

- seed 101:
  - prompt: `\text{Find the GCF of } 28, 42, 14`
  - answer: `14`
- seed 207:
  - prompt: `\text{Find the GCF of } 42, 14, 28`
  - answer: `14`

### D=16

- seed 101:
  - prompt: `\text{Find the GCF of } 96, 12, 72`
  - answer: `12`
- seed 207:
  - prompt: `\text{Find the GCF of } 28, 84, 56`
  - answer: `28`

### D=22

- seed 101:
  - prompt: `\text{Find the GCF of } 72, 144, 216`
  - answer: `72`
- seed 207:
  - prompt: `\text{Find the GCF of } 72, 144, 216`
  - answer: `72`

## OpenStax examples + chapter/section cites

### Prealgebra 2e — 2.5 Prime Factorization and the Least Common Multiple

- https://openstax.org/books/prealgebra-2e/pages/2-5-prime-factorization-and-the-least-common-multiple
- Shape: GCF via prime factors (e.g. GCF(24,36)=12). LCM lives on the sibling leaf.

### Elementary Algebra 2e — 7.1 Greatest Common Factor and Factor by Grouping

- https://openstax.org/books/elementary-algebra-2e/pages/7-1-greatest-common-factor-and-factor-by-grouping
- Mined examples:
  - Example 7.1: How to Find the Greatest Common Factor of Two or More Expressions Find the GCF of 54 and 36.
  - Example 7.2: Find the greatest common factor of $27 x^{3} \text{and} 18 x^{4}$ .
  - Example 7.3: Find the GCF of $4 x^{2} y , 6 x y^{3}$ .
  - Example 7.4: Find the GCF of: $21 x^{3} , 9 x^{2} , 15 x$ .

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Old path can dump a bare equation / identity instead of the named skill.
- Story variety thin (one Mad-Lib / single vehicle) vs OpenStax frames.

## Proposed engine (reuse vs new)

Reuse g6_greatest_common_factor (number). Polynomial monomial GCF is a different leaf (FactorGcf).

_Proposal only. No engine implementation in this notes pass._
