# `graphing_linear_inequalities` — Graphing linear inequalities

- **Course:** Algebra 1
- **Category:** Pre-Algebra — Linear Equations and Inequalities
- **Generator:** `graph_linear_inequality`
- **Already on skeleton?** yes (`GraphLinearIneq`)
- **Old-path extra settings:** none (live is the graph-linear skeleton).

## What the question should look like (D=0 vs high D)

Graph Ax+By≤C (solid/dashed + shade). D=0: y<x+1. High D: rearrange first; test point.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{Graph the inequality: } y \le x`
  - answer: `y \le x`
- seed 207:
  - prompt: `\text{Graph the inequality: } y > 3x`
  - answer: `y > 3x`

### D=8

- seed 101:
  - prompt: `\text{Graph the inequality: } y \le x`
  - answer: `y \le x`
- seed 207:
  - prompt: `\text{Graph the inequality: } y > 3x`
  - answer: `y > 3x`

### D=16

- seed 101:
  - prompt: `\text{Graph the inequality: } y \le 2x + 3`
  - answer: `y \le 2x + 3`
- seed 207:
  - prompt: `\text{Graph the inequality: } y > 3x`
  - answer: `y > 3x`

### D=22

- seed 101:
  - prompt: `\text{Graph the inequality: } y \le 2x + 3`
  - answer: `y \le 2x + 3`
- seed 207:
  - prompt: `\text{Graph the inequality: } y > 3x`
  - answer: `y > 3x`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 4.7 Graphs of Linear Inequalities

- https://openstax.org/books/elementary-algebra-2e/pages/4-7-graphs-of-linear-inequalities
- Mined examples:
  - Example 4.69: Determine whether each ordered pair is a solution to the inequality $y > x + 4$ : ⓐ $(0 , 0)$ ⓑ $(1 , 6)$ ⓒ $(2 , 6)$ ⓓ $(−5 , −15)$ ⓔ $(−8 , 12)$
  - Example 4.70: The boundary line shown is $y = 2 x - 1$ . Write the inequality shown by the graph.
  - Example 4.71: The boundary line shown is $2 x + 3 y = 6$ . Write the inequality shown by the graph.
  - Example 4.72: How to Graph Linear Inequalities Graph the linear inequality $y \geq \frac{3}{4} x - 2$ .

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Gallery section slug: `graphing_linear_inequalities` (type_id or alias).

## Proposed engine (reuse vs new)

Reuse graph_linear_inequality. Not the 1-variable number-line leaf.

_Proposal only. No engine implementation in this notes pass._
