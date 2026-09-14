# `quadratic_discriminant` — Understanding the discriminant

- **Course:** Algebra 1
- **Category:** Algebra 1 — Quadratic Functions
- **Generator:** `quadratic_discriminant`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Compute D=b²−4ac and classify two real / one real / none. D=0: small ints, obvious sign. High D: need to compute carefully.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{Find the discriminant of } x^{2} + 2x - 1.`
  - answer: `D = 8; \text{two real roots}`
- seed 207:
  - prompt: `\text{Find the discriminant of } x^{2} + 2x + 2.`
  - answer: `D = -4; \text{no real roots}`

### D=8

- seed 101:
  - prompt: `\text{Find the discriminant of } 4x^{2} - 6x + 5.`
  - answer: `D = -44; \text{no real roots}`
- seed 207:
  - prompt: `\text{Find the discriminant of } 4x^{2} + 9x + 9.`
  - answer: `D = -63; \text{no real roots}`

### D=16

- seed 101:
  - prompt: `\text{Find the discriminant of } 4x^{2} - 10x + 12.`
  - answer: `D = -92; \text{no real roots}`
- seed 207:
  - prompt: `\text{Find the discriminant of } 4x^{2} + 20x + 20.`
  - answer: `D = 80; \text{two real roots}`

### D=22

- seed 101:
  - prompt: `\text{Find the discriminant of } 4x^{2} - 11x + 11.`
  - answer: `D = -55; \text{no real roots}`
- seed 207:
  - prompt: `\text{Find the discriminant of } 4x^{2} + 19x + 19.`
  - answer: `D = 57; \text{two real roots}`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 10.3 Solve Quadratic Equations Using the Quadratic Formula

- https://openstax.org/books/elementary-algebra-2e/pages/10-3-solve-quadratic-equations-using-the-quadratic-formula
- Mined examples:
  - Example 10.28: How to Solve a Quadratic Equation Using the Quadratic Formula Solve $2 x^{2} + 9 x - 5 = 0$ by using the Quadratic Formula.
  - Example 10.29: Solve $x^{2} - 6 x + 5 = 0$ by using the Quadratic Formula.
  - Example 10.30: Solve $4 y^{2} - 5 y - 3 = 0$ by using the Quadratic Formula.
  - Example 10.31: Solve $2 x^{2} + 10 x + 11 = 0$ by using the Quadratic Formula.
- Shape: Use the discriminant to determine the number and type of solutions.

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Gallery section slug: `quadratic_discriminant` (type_id or alias).

## Proposed engine (reuse vs new)

Reuse quadratic_discriminant. Same a,b,c sampler as the formula leaf; different ask.

_Proposal only. No engine implementation in this notes pass._
