# `rational_divide` — Dividing rational numbers

- **Course:** Algebra 1
- **Category:** Algebra 1 — Beginning Algebra
- **Generator:** `rational_divide`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Numeric ÷ via reciprocal. D=0: ÷ a unit fraction. High D: cancel across the reciprocal.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101 (pattern=`FractionDiv`):
  - prompt: `\frac{1}{3} \div \frac{1}{6}`
  - answer: `2`
- seed 207 (pattern=`FractionDiv`):
  - prompt: `\frac{1}{3} \div \frac{1}{6}`
  - answer: `2`

### D=8

- seed 101 (pattern=`FractionDiv`):
  - prompt: `\frac{6}{35} \div \frac{2}{21}`
  - answer: `\frac{9}{5}`
- seed 207 (pattern=`FractionDiv`):
  - prompt: `\left(\frac{21}{10}\right) / \left(\frac{14}{10}\right)`
  - answer: `\frac{3}{2}`

### D=16

- seed 101 (pattern=`FractionDiv`):
  - prompt: `\frac{\frac{8}{42}}{\frac{14}{18}}`
  - answer: `\frac{12}{49}`
- seed 207 (pattern=`FractionDiv`):
  - prompt: `\frac{78}{70} \div \frac{91}{28}`
  - answer: `\frac{12}{35}`

### D=22

- seed 101 (pattern=`FractionDiv`):
  - prompt: `\frac{\frac{20}{24}}{\frac{12}{16}}`
  - answer: `\frac{10}{9}`
- seed 207 (pattern=`FractionDiv`):
  - prompt: `\frac{26}{108} \div \frac{78}{126}`
  - answer: `\frac{7}{18}`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 1.5 Visualize Fractions

- https://openstax.org/books/elementary-algebra-2e/pages/1-5-visualize-fractions
- Shape: Divide fractions: (2/3)÷(4/5) = (2/3)·(5/4).

### Prealgebra 2e — 4.2 Multiply and Divide Fractions

- https://openstax.org/books/prealgebra-2e/pages/4-2-multiply-and-divide-fractions
- (no local mine items; use the section URL)

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Gallery section slug: `rational_divide` (type_id or alias).

## Proposed engine (reuse vs new)

Reuse numeric fraction ÷ (number). Not rational_skeleton.

_Proposal only. No engine implementation in this notes pass._
