# `rational_add_subtract` — Adding and subtracting rational numbers

> **UNCLEAR** — Leaf name sounds like rational expressions; gold is numeric fractions/decimals (EA 1.6).

- **Course:** Algebra 1
- **Category:** Algebra 1 — Beginning Algebra
- **Generator:** `rational_add_subtract`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Numeric rationals, not rational *expressions*. D=0: like-denom fractions or two small decimals. High D: unlike denoms / mixed signed.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101 (pattern=`FractionAddSub`):
  - prompt: `\frac{3}{2} + \frac{1}{3}`
  - answer: `\frac{11}{6}`
- seed 207 (pattern=`FractionAddSub`):
  - prompt: `\frac{3}{4} + \frac{1}{2}`
  - answer: `\frac{5}{4}`

### D=8

- seed 101 (pattern=`FractionAddSub`):
  - prompt: `\frac{5}{6} - \frac{34}{5}`
  - answer: `-\frac{179}{30}`
- seed 207 (pattern=`FractionAddSub`):
  - prompt: `-\frac{20}{7} + \frac{22}{3}`
  - answer: `\frac{94}{21}`

### D=16

- seed 101 (pattern=`FractionAddSub`):
  - prompt: `-\frac{4}{5} - \frac{29}{3}`
  - answer: `-\frac{157}{15}`
- seed 207 (pattern=`FractionAddSub`):
  - prompt: `-\frac{93}{4} - \frac{11}{12}`
  - answer: `-\frac{145}{6}`

### D=22

- seed 101 (pattern=`FractionAddSub`):
  - prompt: `\frac{12}{5} + \frac{49}{6}`
  - answer: `\frac{317}{30}`
- seed 207 (pattern=`FractionAddSub`):
  - prompt: `\frac{89}{4} - \frac{116}{15}`
  - answer: `\frac{871}{60}`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 1.6 Add and Subtract Fractions

- https://openstax.org/books/elementary-algebra-2e/pages/1-6-add-and-subtract-fractions
- Shape: 3/8+1/8; unlike LCD 1/2+1/6; signed fractions.

### Prealgebra 2e — 4.5 Add and Subtract Fractions with Different Denominators

- https://openstax.org/books/prealgebra-2e/pages/4-5-add-and-subtract-fractions-with-different-denominators
- Shape: Same numeric skill; A1 leaf should stay arithmetic.

## Variety notes

Leaf name sounds like rational expressions; gold is numeric fractions/decimals (EA 1.6).

## Limitations

- UNCLEAR / LIMITATIONS: leaf name sounds like rational *expressions*; gold is numeric ± (EA §1.6).
- Must not wire rational-expression ± cancel here.

## Proposed engine (reuse vs new)

Reuse numeric fraction ± (number). Do not wire rational_skeleton (that's expressions).

_Proposal only. No engine implementation in this notes pass._
