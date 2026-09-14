# `graphing_quadratic_inequalities` — Graphing quadratic inequalities

> **UNCLEAR** — No Elementary Algebra section for quadratic inequalities; gold is IA 9.8 / old path.

- **Course:** Algebra 1
- **Category:** Algebra 1 — Quadratic Functions
- **Generator:** `graph_quadratic_inequality`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Graph y≤ax²+bx+c (shade). D=0: y≤x² integer vertex. High D: dashed vs solid; test point.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `y < x^2 - 1`
  - answer: `y < x^2 - 1 \text{ (dashed boundary)}`
- seed 207:
  - prompt: `y < x^2`
  - answer: `y < x^2 \text{ (dashed boundary)}`

### D=8

- seed 101:
  - prompt: `y + 5 > -2(x - 3)^2`
  - answer: `y + 5 > -2(x - 3)^2 \text{ (dashed boundary)}`
- seed 207:
  - prompt: `y > -(x + 4)(x - 2)`
  - answer: `y > -(x + 4)(x - 2) \text{ (dashed boundary)}`

### D=16

- seed 101:
  - prompt: `y - 6 > -3(x - 3)^2`
  - answer: `y - 6 > -3(x - 3)^2 \text{ (dashed boundary)}`
- seed 207:
  - prompt: `y > -x(x - 6)`
  - answer: `y > -x(x - 6) \text{ (dashed boundary)}`

### D=22

- seed 101:
  - prompt: `y > -3(x - 3)^2 + 6`
  - answer: `y > -3(x - 3)^2 + 6 \text{ (dashed boundary)}`
- seed 207:
  - prompt: `y > \frac{1}{2}x(x - 6)`
  - answer: `y > \frac{1}{2}x(x - 6) \text{ (dashed boundary)}`

## OpenStax examples + chapter/section cites

### Intermediate Algebra 2e — 9.8 Solve Quadratic Inequalities

- https://openstax.org/books/intermediate-algebra-2e/pages/9-8-solve-quadratic-inequalities
- Shape: EA has no dedicated quadratic-inequality graph section; IA 9.8 is the closest.

## Variety notes

No Elementary Algebra section for quadratic inequalities; gold is IA 9.8 / old path.

## Limitations

- UNCLEAR / LIMITATIONS: no EA section; gold is IA §9.8 / old path. Red-header only.

## Proposed engine (reuse vs new)

Reuse graph_quadratic_inequality. Leave the leaf if old path is a linear-inequality dump.

_Proposal only. No engine implementation in this notes pass._
