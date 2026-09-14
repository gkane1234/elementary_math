# `radical_multiply` — Multiplying

- **Course:** Algebra 1
- **Category:** Algebra 1 — Radical Expressions
- **Generator:** `radical_multiply`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Product rule / FOIL with square roots. D=0: √3·√12 or √2(√8). High D: (√a±√b)(√c±√d).

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\sqrt{18} \cdot \sqrt{14}`
  - answer: `6\sqrt{7}`
- seed 207:
  - prompt: `\sqrt{8} \cdot \sqrt{5}`
  - answer: `2\sqrt{10}`

### D=8

- seed 101:
  - prompt: `\sqrt{12} \cdot 5\sqrt{27}`
  - answer: `90`
- seed 207:
  - prompt: `3\sqrt{10} \cdot 2\sqrt{2}`
  - answer: `12\sqrt{5}`

### D=16

- seed 101:
  - prompt: `\left(4\sqrt{14} + \sqrt{10}\right)\left(5\sqrt{14} - 2\sqrt{10}\right)`
  - answer: `260 - 6\sqrt{35}`
- seed 207:
  - prompt: `\left(3\sqrt{5} + 2\sqrt{2}\right)\left(4\sqrt{5} - \sqrt{2}\right)`
  - answer: `56 + 5\sqrt{10}`

### D=22

- seed 101:
  - prompt: `\left(4\sqrt{14} + \sqrt{10}\right)\left(5\sqrt{14} - 2\sqrt{10}\right)`
  - answer: `260 - 6\sqrt{35}`
- seed 207:
  - prompt: `\left(3\sqrt{5} + 2\sqrt{2}\right)\left(4\sqrt{5} - \sqrt{2}\right)`
  - answer: `56 + 5\sqrt{10}`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 9.4 Multiply Square Roots

- https://openstax.org/books/elementary-algebra-2e/pages/9-4-multiply-square-roots
- Mined examples:
  - Example 9.44: Simplify: ⓐ $\sqrt{2} \cdot \sqrt{6}$ ⓑ $\left(\right. 4 \sqrt{3} \left.\right) \left(\right. 2 \sqrt{12} \left.\right)$ .
  - Example 9.45: Simplify: $\left(\right. 6 \sqrt{2} \left.\right) \left(\right. 3 \sqrt{10} \left.\right)$ .
  - Example 9.46: Simplify: ⓐ $\left(\right. \sqrt{8 x^{3}} \left.\right) \left(\right. \sqrt{3 x} \left.\right)$ ⓑ $\left(\right. \sqrt{20 y^{2}} \left.\right) \left(\right. \sqrt{5 y^{3}} \left.\right)$ .
  - Example 9.47: Simplify: $\left(\right. 10 \sqrt{6 p^{3}} \left.\right) \left(\right. 3 \sqrt{18 p} \left.\right)$ .

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Gallery section slug: `radical_multiply` (type_id or alias).

## Proposed engine (reuse vs new)

Reuse radical_multiply.

_Proposal only. No engine implementation in this notes pass._
