# `continuous_relations` — Continuous relations

> **UNCLEAR / LOW_VARIETY** — Old path is only “given y=mx+b, find y when x=a” — same skill as `evaluating_graphing_functions` without f(x) notation. No graph.

- **Course:** Algebra 1
- **Category:** Algebra 1 — Relations and Introduction to Functions
- **Generator:** `continuous_relations`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Function from an equation/graph: evaluate f(a) or read a graph. D=0: f(x)=2x+1, f(3). High D: piecewise-looking graph read.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{Given } y = x - 1, \text{ find } y \text{ when } x = 3.`
  - answer: `2`
- seed 207:
  - prompt: `\text{Given } y = x - 1, \text{ find } y \text{ when } x = -3.`
  - answer: `-4`

### D=8

- seed 101:
  - prompt: `\text{Given } y = 3x - 2, \text{ find } y \text{ when } x = 3.`
  - answer: `7`
- seed 207:
  - prompt: `\text{Given } y = 2x - 1, \text{ find } y \text{ when } x = -3.`
  - answer: `-7`

### D=16

- seed 101:
  - prompt: `\text{Given } y = -2x + 3, \text{ find } y \text{ when } x = 6.`
  - answer: `-9`
- seed 207:
  - prompt: `\text{Given } y = 8x - 1, \text{ find } y \text{ when } x = -3.`
  - answer: `-25`

### D=22

- seed 101:
  - prompt: `\text{Given } y = 8x - 4, \text{ find } y \text{ when } x = 7.`
  - answer: `52`
- seed 207:
  - prompt: `\text{Given } y = 6x + 9, \text{ find } y \text{ when } x = -3.`
  - answer: `-9`

## OpenStax examples + chapter/section cites

### Intermediate Algebra 2e — 3.5 Relations and Functions

- https://openstax.org/books/intermediate-algebra-2e/pages/3-5-relations-and-functions
- Shape: Evaluate f(x)=3x−5 at a value; use a graph to find f(a).

## Variety notes

**UNCLEAR / LOW_VARIETY** — Old path is only “given y=mx+b, find y when x=a” — same skill as `evaluating_graphing_functions` without f(x) notation. No graph.

## Limitations

- UNCLEAR / LOW_VARIETY / LIMITATIONS: old path is y when x=a for y=mx+b — same skill as evaluate-without-graph.
- No continuous-graph / domain-range gold locked from old path.
- NOT_IMPLEMENTED beyond red-header live samples.

## Proposed engine (reuse vs new)

Reuse continuous_relations / evaluating_graphing_functions overlap — confirm old path does not duplicate the sibling.

_Proposal only. No engine implementation in this notes pass._
