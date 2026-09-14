# `radical_add_subtract` — Adding and subtracting

- **Course:** Algebra 1
- **Category:** Algebra 1 — Radical Expressions
- **Generator:** `radical_add_subtract`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Combine like radicals after simplifying. D=0: 2√3+5√3. High D: simplify first then combine.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `4\sqrt{14} + \sqrt{14}`
  - answer: `5\sqrt{14}`
- seed 207:
  - prompt: `3\sqrt{5} - 2\sqrt{5}`
  - answer: `\sqrt{5}`

### D=8

- seed 101:
  - prompt: `\sqrt{224} - \sqrt{56} - \sqrt{224}`
  - answer: `-2\sqrt{14}`
- seed 207:
  - prompt: `\sqrt{80} + \sqrt{20}`
  - answer: `6\sqrt{5}`

### D=16

- seed 101:
  - prompt: `5\sqrt{350} - 4\sqrt{126} - \sqrt{686} + \sqrt{504}`
  - answer: `12\sqrt{14}`
- seed 207:
  - prompt: `\sqrt{245} - \sqrt{245} + 2\sqrt{45}`
  - answer: `6\sqrt{5}`

### D=22

- seed 101:
  - prompt: `5\sqrt{350} - 4\sqrt{126} - \sqrt{686} + \sqrt{504}`
  - answer: `12\sqrt{14}`
- seed 207:
  - prompt: `\sqrt{245} - \sqrt{245} + 2\sqrt{45}`
  - answer: `6\sqrt{5}`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 9.3 Add and Subtract Square Roots

- https://openstax.org/books/elementary-algebra-2e/pages/9-3-add-and-subtract-square-roots
- Mined examples:
  - Example 9.29: Simplify: $2 \sqrt{2} - 7 \sqrt{2}$ .
  - Example 9.30: Simplify: $3 \sqrt{y} + 4 \sqrt{y}$ .
  - Example 9.31: Simplify: $4 \sqrt{x} - 2 \sqrt{y}$ .
  - Example 9.32: Simplify: $5 \sqrt{13} + 4 \sqrt{13} + 2 \sqrt{13}$ .

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Gallery section slug: `radical_add_subtract` (type_id or alias).

## Proposed engine (reuse vs new)

Reuse radical_add_subtract. Keep like-radical skill; do not become simplify-only.

_Proposal only. No engine implementation in this notes pass._
