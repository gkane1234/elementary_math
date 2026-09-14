# `graphing_exponential_functions` — Graphing exponential functions

> **UNCLEAR** — Not in Elementary Algebra TOC; gold is IA 10.2 + old-path table/graph.

- **Course:** Algebra 1
- **Category:** Algebra 1 — Exponents
- **Generator:** `graph_exponential`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Graph y=a·b^x. D=0: y=2^x integer table. High D: y=a·b^{x−h}+k or decay 0<b<1.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `y = 2^{x}`
  - answer: `y = 2^{x}`
- seed 207:
  - prompt: `y = 2^{x}`
  - answer: `y = 2^{x}`

### D=8

- seed 101:
  - prompt: `y = 3 \cdot \left(\frac{1}{4}\right)^{x} + 3`
  - answer: `y = 3 \cdot \left(\frac{1}{4}\right)^{x} + 3`
- seed 207:
  - prompt: `y = 3 \cdot \left(\frac{1}{4}\right)^{x - 1} + 1`
  - answer: `y = 3 \cdot \left(\frac{1}{4}\right)^{x - 1} + 1`

### D=16

- seed 101:
  - prompt: `y = -3^{x + 1} - 1`
  - answer: `y = -3^{x + 1} - 1`
- seed 207:
  - prompt: `y = -3 \cdot \left(\frac{1}{3}\right)^{x - 1} + 1`
  - answer: `y = -3 \cdot \left(\frac{1}{3}\right)^{x - 1} + 1`

### D=22

- seed 101:
  - prompt: `y = -3^{x + 1} - 1`
  - answer: `y = -3^{x + 1} - 1`
- seed 207:
  - prompt: `y = -3 \cdot \left(\frac{1}{3}\right)^{x - 1} + 1`
  - answer: `y = -3 \cdot \left(\frac{1}{3}\right)^{x - 1} + 1`

## OpenStax examples + chapter/section cites

### Intermediate Algebra 2e — 10.2 Evaluate and Graph Exponential Functions

- https://openstax.org/books/intermediate-algebra-2e/pages/10-2-evaluate-and-graph-exponential-functions
- Mined examples:
  - Example 10.10: On the same coordinate system graph $f (x) = 2^{x}$ and $g (x) = 3^{x} .$
  - Example 10.11: On the same coordinate system, graph $f (x) = \left(\right. \frac{1}{2} \left.\right)^{x}$ and $g (x) = \left(\right. \frac{1}{3} \left.\right)^{x} .$
  - Example 10.12: On the same coordinate system graph $f (x) = 2^{x}$ and $g (x) = 2^{x + 1} .$
  - Example 10.13: On the same coordinate system graph $f (x) = 3^{x}$ and $g (x) = 3^{x} - 2 .$

## Variety notes

Not in Elementary Algebra TOC; gold is IA 10.2 + old-path table/graph.

## Limitations

- UNCLEAR / LIMITATIONS: not in EA TOC; IA §10.2 table/graph. Red-header / deferred skeleton.

## Proposed engine (reuse vs new)

Reuse graph_exponential. EA has no exponential-graph chapter — copy old path, do not invent logs.

_Proposal only. No engine implementation in this notes pass._
