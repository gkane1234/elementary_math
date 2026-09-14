# `graphing_absolute_value_equations` — Graphing absolute value equations

> **UNCLEAR** — Not in Elementary Algebra TOC; gold is College Algebra 3.6 + old vertex/V-shape.

- **Course:** Algebra 1
- **Category:** Algebra 1 — Linear Equations and Inequalities
- **Generator:** `graph_absolute_value`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Graph y=a|x−h|+k. D=0: y=|x|. High D: vertex shift and a≠1.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `y = |x + 2|`
  - answer: `y = |x + 2|`
- seed 207:
  - prompt: `y = |x - 5|`
  - answer: `y = |x - 5|`

### D=8

- seed 101:
  - prompt: `y = |x| + 3`
  - answer: `y = |x| + 3`
- seed 207:
  - prompt: `y = |x + 6| + 5`
  - answer: `y = |x + 6| + 5`

### D=16

- seed 101:
  - prompt: `y = |x| + 3`
  - answer: `y = |x| + 3`
- seed 207:
  - prompt: `y = |x + 8| + 3`
  - answer: `y = |x + 8| + 3`

### D=22

- seed 101:
  - prompt: `y = \frac{3}{2}|x - 3| + 6`
  - answer: `y = \frac{3}{2}|x - 3| + 6`
- seed 207:
  - prompt: `y = \frac{3}{2}|x + 3| - 8`
  - answer: `y = \frac{3}{2}|x + 3| - 8`

## OpenStax examples + chapter/section cites

### College Algebra 2e — 3.6 Absolute Value Functions

- https://openstax.org/books/college-algebra-2e/pages/3-6-absolute-value-functions
- Shape: Graph y=|x−2|−1; vertex (h,k), V shape.

### Intermediate Algebra 2e — 3.6 Graphs of Functions

- https://openstax.org/books/intermediate-algebra-2e/pages/3-6-graphs-of-functions
- Shape: IA graphs functions; dedicated abs-value graph is College Algebra.

## Variety notes

Not in Elementary Algebra TOC; gold is College Algebra 3.6 + old vertex/V-shape.

## Limitations

- UNCLEAR / LIMITATIONS: not in EA TOC; College Algebra §3.6 vertex/V-shape. Red-header samples.

## Proposed engine (reuse vs new)

Reuse graph_absolute_value. EA has no abs-value graph section — copy old path.

_Proposal only. No engine implementation in this notes pass._
