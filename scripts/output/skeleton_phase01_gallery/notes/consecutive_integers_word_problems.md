# `consecutive_integers_word_problems` — Consecutive integers word problems

- **Course:** Algebra 1 (A1 catalog)
- **Category:** Algebra 1 — Equations
- **Generator:** `wp_consecutive_integers`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

D=0: two or three consecutive integers, sum. High D: consecutive even/odd, or first+last. Translate the phrase; do not dump $n+(n+1)+(n+2)=S$.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{The sum of two consecutive integers is 37. Find the smallest integer.}`
  - answer: `18`
- seed 207:
  - prompt: `\text{The sum of two consecutive integers is 17. Find the smallest integer.}`
  - answer: `8`

### D=8

- seed 101:
  - prompt: `\text{The sum of the first and last of four consecutive odd integers is 40. Find the smallest integer.}`
  - answer: `17`
- seed 207:
  - prompt: `\text{The sum of the first and last of three consecutive odd integers is 54. Find the smallest integer.}`
  - answer: `25`

### D=16

- seed 101:
  - prompt: `\text{The product of the first and last of five consecutive odd integers is 425. Find the smallest integer.}`
  - answer: `17`
- seed 207:
  - prompt: `\text{The product of the first and last of four consecutive odd integers is 775. Find the smallest integer.}`
  - answer: `25`

### D=22

- seed 101:
  - prompt: `\text{The product of the first and last of five consecutive odd integers is 425. Find the smallest integer.}`
  - answer: `17`
- seed 207:
  - prompt: `\text{The product of the first and last of four consecutive odd integers is 775. Find the smallest integer.}`
  - answer: `25`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 3.1 Use a Problem-Solving Strategy

- https://openstax.org/books/elementary-algebra-2e/pages/3-1-use-a-problem-solving-strategy
- Shape: Consecutive integer number problems (sum of three consecutive…).

### Intermediate Algebra 2e — 2.2 Use a Problem Solving Strategy

- https://openstax.org/books/intermediate-algebra-2e/pages/2-2-use-a-problem-solving-strategy
- Mined examples:
  - Example 2.14: Normal yearly snowfall at the local ski resort is 12 inches more than twice the amount it received last season. The normal yearly snowfall is 62 inches. What was the snowfall last season at the ski resort?
  - Example 2.15: The sum of seven times a number and eight is thirty-six. Find the number.
  - Example 2.16: The sum of two numbers is negative fifteen. One number is nine less than the other. Find the numbers.
  - Example 2.17: Find three consecutive integers whose sum is $−54 .$

## Variety notes

D=0 is one OpenStax-like sum-of-two-consecutive frame (IA 2.2 Example 2.17). High D already unlocks odd integers, first+last, and product — not a dump stub. Keep the one-skill phrase family.

## Limitations

- Gallery section slug: `consecutive_integers_word_problems` (type_id or alias).

## Proposed engine (reuse vs new)

Reuse ConsecutiveIntegersFramework / narrative_wp. SolveLinear only as reverse algebra after a real stem.

_Proposal only. No engine implementation in this notes pass._
