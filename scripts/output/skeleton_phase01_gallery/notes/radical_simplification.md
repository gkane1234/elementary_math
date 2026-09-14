# `radical_simplification` — Simplifying single radicals

- **Course:** Algebra 1
- **Category:** Algebra 1 — Radical Expressions
- **Generator:** `radical_simplification`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Simplify √n or √(a²b). D=0: √36 or √8→2√2. High D: variables under the radical.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\sqrt{96}`
  - answer: `4\sqrt{6}`
- seed 207:
  - prompt: `\sqrt{96}`
  - answer: `4\sqrt{6}`

### D=8

- seed 101:
  - prompt: `\sqrt{80}`
  - answer: `4\sqrt{5}`
- seed 207:
  - prompt: `\sqrt{72}`
  - answer: `6\sqrt{2}`

### D=16

- seed 101:
  - prompt: `\sqrt{108}`
  - answer: `6\sqrt{3}`
- seed 207:
  - prompt: `\sqrt{368}`
  - answer: `4\sqrt{23}`

### D=22

- seed 101:
  - prompt: `\sqrt{160}`
  - answer: `4\sqrt{10}`
- seed 207:
  - prompt: `\sqrt{288}`
  - answer: `12\sqrt{2}`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 9.1 Simplify and Use Square Roots

- https://openstax.org/books/elementary-algebra-2e/pages/9-1-simplify-and-use-square-roots
- Mined examples:
  - Example 9.1: Simplify: ⓐ $\sqrt{36}$ ⓑ $\sqrt{196}$ ⓒ $− \sqrt{81}$ ⓓ $− \sqrt{289}$ .
  - Example 9.2: Simplify: ⓐ $\sqrt{−169}$ ⓑ $− \sqrt{64}$ .
  - Example 9.3: Simplify: ⓐ $\sqrt{25} + \sqrt{144}$ ⓑ $\sqrt{25 + 144}$ .
  - Example 9.4: Estimate $\sqrt{60}$ between two consecutive whole numbers.

### Elementary Algebra 2e — 9.2 Simplify Square Roots

- https://openstax.org/books/elementary-algebra-2e/pages/9-2-simplify-square-roots
- Mined examples:
  - Example 9.12: How To Use the Product Property to Simplify a Square Root Simplify: $\sqrt{50}$ .
  - Example 9.13: Simplify: $\sqrt{500}$ .
  - Example 9.14: Simplify: $\sqrt{x^{3}}$ .
  - Example 9.15: Simplify: $\sqrt{25 y^{5} .}$

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Gallery section slug: `radical_simplification` (type_id or alias).

## Proposed engine (reuse vs new)

Reuse radical_simplification. New radical skeleton only if later unification needs it — not this pass.

_Proposal only. No engine implementation in this notes pass._
