# `sets_of_numbers` — Sets of numbers

> **UNCLEAR / LOW_VARIETY** — Old path is T/F “is an integer/whole” (often the same −5 at D=0). OpenStax EA 1.8 asks which sets a number belongs to (N/W/Z/Q/irrational/R).

- **Course:** Algebra 1
- **Category:** Algebra 1 — Beginning Algebra
- **Generator:** `sets_of_numbers`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Classify a number into N/W/Z/Q/irrational/R. D=0: a small integer or a simple fraction. High D: repeating decimals, √n non-perfect, π.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101 (pattern=`NumberCore`):
  - prompt: `-5`
  - answer: `\text{integer}`
- seed 207 (pattern=`NumberCore`):
  - prompt: `-5`
  - answer: `\text{integer}`

### D=8

- seed 101 (pattern=`NumberCore`):
  - prompt: `\text{True or false: } 35\text{ is an integer number.}`
  - answer: `\text{True}`
- seed 207 (pattern=`NumberCore`):
  - prompt: `\text{True or false: } 2\text{ is an integer number.}`
  - answer: `\text{True}`

### D=16

- seed 101 (pattern=`NumberCore`):
  - prompt: `\text{True or false: } 70\text{ is an integer number.}`
  - answer: `\text{True}`
- seed 207 (pattern=`NumberCore`):
  - prompt: `\text{True or false: } \sqrt{7}\text{ is a whole number.}`
  - answer: `\text{False}`

### D=22

- seed 101 (pattern=`NumberCore`):
  - prompt: `\text{True or false: } 139\text{ is an integer number.}`
  - answer: `\text{True}`
- seed 207 (pattern=`NumberCore`):
  - prompt: `\text{True or false: } \sqrt{7}\text{ is a whole number.}`
  - answer: `\text{False}`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 1.8 The Real Numbers

- https://openstax.org/books/elementary-algebra-2e/pages/1-8-the-real-numbers
- Shape: Identify which sets 7, −3, 2/5, √2, π belong to (natural/whole/integer/rational/irrational/real).

## Variety notes

**UNCLEAR / LOW_VARIETY** — Old path is T/F “is an integer/whole” (often the same −5 at D=0). OpenStax EA 1.8 asks which sets a number belongs to (N/W/Z/Q/irrational/R).

## Limitations

- UNCLEAR / LOW_VARIETY / LIMITATIONS: old T/F integer/whole vs EA §1.8 multi-set classification.
- NOT_IMPLEMENTED reclassification engine — red-header samples only.

## Proposed engine (reuse vs new)

Reuse sets_of_numbers (number). No FactorProduct / rational_skeleton.

_Proposal only. No engine implementation in this notes pass._
