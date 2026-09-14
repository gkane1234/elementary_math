# `radical_divide` — Dividing

- **Course:** Algebra 1
- **Category:** Algebra 1 — Radical Expressions
- **Generator:** `radical_divide`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Quotient rule and/or rationalize a monomial (then conjugate) denominator. D=0: √8/√2. High D: conjugate.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\frac{\sqrt{224}}{\sqrt{14}}`
  - answer: `4`
- seed 207:
  - prompt: `\frac{\sqrt{32}}{\sqrt{2}}`
  - answer: `4`

### D=8

- seed 101:
  - prompt: `\frac{3\sqrt{1260}}{3\sqrt{10}}`
  - answer: `3\sqrt{14}`
- seed 207:
  - prompt: `\frac{2\sqrt{160}}{\sqrt{2}}`
  - answer: `8\sqrt{5}`

### D=16

- seed 101:
  - prompt: `\frac{4\sqrt{40}}{4\sqrt{637}}`
  - answer: `\frac{2\sqrt{130}}{91}`
- seed 207:
  - prompt: `\frac{8\sqrt{245}}{3\sqrt{32}}`
  - answer: `\frac{7\sqrt{10}}{3}`

### D=22

- seed 101:
  - prompt: `\frac{4\sqrt{40}}{9\sqrt{637}}`
  - answer: `\frac{8\sqrt{130}}{819}`
- seed 207:
  - prompt: `\frac{8\sqrt{245}}{3\sqrt{32}}`
  - answer: `\frac{7\sqrt{10}}{3}`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 9.5 Divide Square Roots

- https://openstax.org/books/elementary-algebra-2e/pages/9-5-divide-square-roots
- Mined examples:
  - Example 9.60: Simplify: $\frac{\sqrt{54}}{6}$ .
  - Example 9.61: Simplify: $\frac{6 - \sqrt{24}}{12}$ .
  - Example 9.62: Simplify: $\frac{\sqrt{27}}{\sqrt{75}}$ .
  - Example 9.63: Simplify: $\frac{\sqrt{6 y^{5}}}{\sqrt{2 y}}$ .

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Gallery section slug: `radical_divide` (type_id or alias).

## Proposed engine (reuse vs new)

Reuse radical_divide. Conjugate rationalizing is a D unlock, not a new engine.

_Proposal only. No engine implementation in this notes pass._
