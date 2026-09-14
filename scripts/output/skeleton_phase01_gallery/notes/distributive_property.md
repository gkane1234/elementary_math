# `distributive_property` — The Distributive Property

- **Course:** Algebra 1
- **Category:** Pre-Algebra — Beginning Algebra
- **Generator:** `distributive_property`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Rewrite a(b±c) as ab±ac (or reverse). D=0: 3(x+2). High D: negative a, two-term inside with x².

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101 (form=`scaled_sum`):
  - prompt: `\left(1 + 2\right)\left(-2\right)`
  - answer: `-2\cdot 2 - 2\cdot 1`
- seed 207 (form=`scaled_sum`):
  - prompt: `-1\left(1 + 2\right)`
  - answer: `-1\cdot 2 - 1\cdot 1`

### D=8

- seed 101 (form=`scaled_sum`):
  - prompt: `\left(-1 + 2 + 4\right)\left(-2\right)`
  - answer: `- -2\cdot 1 - 2\cdot 2 - 2\cdot 4`
- seed 207 (form=`scaled_sum`):
  - prompt: `1.56\left(\frac{1}{4} + \frac{1}{2} + \frac{4}{5}\right)`
  - answer: `1.56\cdot \frac{1}{4} + 1.56\cdot \frac{1}{2} + 1.56\cdot \frac{4}{5}`

### D=16

- seed 101 (form=`scaled_sum`):
  - prompt: `7.8\left(2 + \frac{1}{5} + \frac{1}{3}\right)`
  - answer: `7.8\cdot 2 + 7.8\cdot \frac{1}{3} + 7.8\cdot \frac{1}{5}`
- seed 207 (form=`scaled_sum`):
  - prompt: `-\frac{10}{18}\left(-\frac{9}{18} - \frac{92}{24} - \frac{36}{14}\right)`
  - answer: `- -\frac{10}{18}\cdot \frac{9}{18} + \frac{10}{18}\cdot \frac{36}{14} + \frac{10}{18}\cdot \frac{92}{24}`

### D=22

- seed 101 (form=`scaled_sum`):
  - prompt: `7.8\left(\frac{1}{5} + \frac{1}{9} + 2\right)`
  - answer: `7.8\cdot 2 + 7.8\cdot \frac{1}{5} + 7.8\cdot \frac{1}{9}`
- seed 207 (form=`scaled_sum`):
  - prompt: `2.496\left(-6.45 + \frac{90}{27} - 6.93\right)`
  - answer: `- 2.496\cdot 6.45 + 2.496\cdot \frac{90}{27} - 2.496\cdot 6.93`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 1.9 Properties of Real Numbers

- https://openstax.org/books/elementary-algebra-2e/pages/1-9-properties-of-real-numbers
- Shape: Distribute 6(x+4); −2(3x−5).

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- LIMITATIONS: distinct from G6 area-diagram distributive; algebraic a(b+c) shapes.

## Proposed engine (reuse vs new)

Reuse AffineInflate distributive (already on G6/PA). No FactorProduct.

_Proposal only. No engine implementation in this notes pass._
