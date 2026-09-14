# `rational_multiply` — Multiplying rational numbers

- **Course:** Algebra 1
- **Category:** Algebra 1 — Beginning Algebra
- **Generator:** `rational_multiply`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Numeric × of fractions/decimals. D=0: two unit fractions. High D: cancel-before-multiply.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101 (pattern=`FractionMul`):
  - prompt: `\frac{3}{4} \cdot \frac{2}{3}`
  - answer: `\frac{1}{2}`
- seed 207 (pattern=`FractionMul`):
  - prompt: `\frac{3}{4} \cdot \frac{1}{2}`
  - answer: `\frac{3}{8}`

### D=8

- seed 101 (pattern=`FractionMul`):
  - prompt: `5\frac{5}{6} \cdot 4\frac{3}{4}`
  - answer: `\frac{665}{24}`
- seed 207 (pattern=`FractionMul`):
  - prompt: `6\frac{1}{2} \cdot 1\frac{3}{8}`
  - answer: `\frac{143}{16}`

### D=16

- seed 101 (pattern=`FractionMul`):
  - prompt: `6\frac{4}{11} \cdot 4\frac{5}{7}`
  - answer: `30`
- seed 207 (pattern=`FractionMul`):
  - prompt: `7\frac{4}{5} \cdot \frac{4}{5}`
  - answer: `\frac{156}{25}`

### D=22

- seed 101 (pattern=`FractionMul`):
  - prompt: `12\frac{7}{11} \cdot 4\frac{5}{7}`
  - answer: `\frac{417}{7}`
- seed 207 (pattern=`FractionMul`):
  - prompt: `15\frac{3}{5} \cdot 2\frac{11}{15}`
  - answer: `\frac{1066}{25}`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 1.5 Visualize Fractions

- https://openstax.org/books/elementary-algebra-2e/pages/1-5-visualize-fractions
- Shape: Multiply fractions (2/3)·(3/4); mixed× later if old path has it.

### Prealgebra 2e — 4.2 Multiply and Divide Fractions

- https://openstax.org/books/prealgebra-2e/pages/4-2-multiply-and-divide-fractions
- (no local mine items; use the section URL)

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Gallery section slug: `rational_multiply` (type_id or alias).

## Proposed engine (reuse vs new)

Reuse numeric fraction × (number). Not rational_skeleton.

_Proposal only. No engine implementation in this notes pass._
