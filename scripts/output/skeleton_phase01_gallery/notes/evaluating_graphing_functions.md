# `evaluating_graphing_functions` — Evaluating and graphing functions

> **UNCLEAR / LOW_VARIETY** — Old path is only f(a) for a linear f(x)=mx+b; same items across D. No graphing. Overlaps `continuous_relations` (y when x=a).

- **Course:** Algebra 1
- **Category:** Algebra 1 — Relations and Introduction to Functions
- **Generator:** `evaluating_graphing_functions`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Evaluate f(x) and/or sketch a simple function. D=0: linear f(2). High D: quadratic evaluate or a tiny table+graph.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{Given } f(x) = 3x - 2, \text{ find } f(3).`
  - answer: `7`
- seed 207:
  - prompt: `\text{Given } f(x) = 2x - 1, \text{ find } f(-3).`
  - answer: `-7`

### D=8

- seed 101:
  - prompt: `\text{Given } f(x) = 3x - 2, \text{ find } f(3).`
  - answer: `7`
- seed 207:
  - prompt: `\text{Given } f(x) = 2x - 1, \text{ find } f(-3).`
  - answer: `-7`

### D=16

- seed 101:
  - prompt: `\text{Given } f(x) = 3x - 2, \text{ find } f(3).`
  - answer: `7`
- seed 207:
  - prompt: `\text{Given } f(x) = 2x - 1, \text{ find } f(-3).`
  - answer: `-7`

### D=22

- seed 101:
  - prompt: `\text{Given } f(x) = 3x - 2, \text{ find } f(3).`
  - answer: `7`
- seed 207:
  - prompt: `\text{Given } f(x) = 2x - 1, \text{ find } f(-3).`
  - answer: `-7`

## OpenStax examples + chapter/section cites

### Intermediate Algebra 2e — 3.6 Graphs of Functions

- https://openstax.org/books/intermediate-algebra-2e/pages/3-6-graphs-of-functions
- Shape: Evaluate and graph a basic function.

## Variety notes

**UNCLEAR / LOW_VARIETY** — Old path is only f(a) for a linear f(x)=mx+b; same items across D. No graphing. Overlaps `continuous_relations` (y when x=a).

## Limitations

- UNCLEAR / LOW_VARIETY / LIMITATIONS: name says graphing; old path is only f(a) for linear f, flat across D.
- Overlaps `continuous_relations` (y when x=a) and lacks IA §3.6 graph skill.
- NOT_IMPLEMENTED as evaluate+graph until gold locked (OpenStax graph + old evaluate shapes).

## Proposed engine (reuse vs new)

Reuse evaluating_graphing_functions. Prefer evaluate-at-a-point at D=0 if old path does that.

_Proposal only. No engine implementation in this notes pass._
