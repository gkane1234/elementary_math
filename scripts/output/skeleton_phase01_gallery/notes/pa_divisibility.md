# `pa_divisibility` — Divisibility

> **LOW_VARIETY** — These seeds are all “Is n divisible by 6?” with answer Yes. OpenStax 2.4 tests 2, 3, 5, 6, 10 (including No).

- **Course:** Prealgebra (PA catalog)
- **Category:** Pre-Algebra — Factors and Exponents
- **Generator:** `g6_divisibility`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

D=0: even/odd or divisible-by-2/5/10 on a small n. High D: 3/6/9 tests on larger n. Yes/no (or which rules), not list-all-factors (that's pa_factoring).

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{Is } 12 \text{ divisible by 6?}`
  - answer: `\text{Yes}`
- seed 207:
  - prompt: `\text{Is } 6 \text{ divisible by 6?}`
  - answer: `\text{Yes}`

### D=8

- seed 101:
  - prompt: `\text{Is } 36 \text{ divisible by 6?}`
  - answer: `\text{Yes}`
- seed 207:
  - prompt: `\text{Is } 12 \text{ divisible by 6?}`
  - answer: `\text{Yes}`

### D=16

- seed 101:
  - prompt: `\text{Is } 72 \text{ divisible by 6?}`
  - answer: `\text{Yes}`
- seed 207:
  - prompt: `\text{Is } 96 \text{ divisible by 6?}`
  - answer: `\text{Yes}`

### D=22

- seed 101:
  - prompt: `\text{Is } 144 \text{ divisible by 6?}`
  - answer: `\text{Yes}`
- seed 207:
  - prompt: `\text{Is } 42 \text{ divisible by 6?}`
  - answer: `\text{Yes}`

## OpenStax examples + chapter/section cites

### Prealgebra 2e — 2.4 Find Multiples and Factors

- https://openstax.org/books/prealgebra-2e/pages/2-4-find-multiples-and-factors
- Shape: Divisibility tests for 2,3,5,6,10 on a whole number (e.g. is 5,625 divisible by 3?).

## Variety notes

These seeds are all “Is n divisible by 6?” → Yes. OpenStax 2.4 rotates 2, 3, 5, 6, 10 and includes No answers. Reuse the number engine but widen the rule pool.

## Limitations

- Flags: **LOW_VARIETY**.
- These seeds are all “Is n divisible by 6?” → Yes. OpenStax 2.4 rotates 2, 3, 5, 6, 10 and includes No answers. Reuse the number engine but widen the rule pool.

## Proposed engine (reuse vs new)

Reuse g6_divisibility (number). No skeleton needed.

_Proposal only. No engine implementation in this notes pass._
