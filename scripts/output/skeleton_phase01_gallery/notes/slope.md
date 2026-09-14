# `slope` — Slope

- **Course:** Algebra 1
- **Category:** Pre-Algebra — Linear Equations and Inequalities
- **Generator:** `slope`
- **Already on skeleton?** yes (`Slope`; shared with `pa_slope`)
- **Old-path extra settings:** none (live is linear_forms).

## What the question should look like (D=0 vs high D)

Slope between two points (or from an equation). D=0: integer rise/run. High D: negative / 0 / undefined.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{Find the slope of the line through } (3, 0) \text{ and } (5, -5).`
  - answer: `-\frac{5}{2}`
- seed 207:
  - prompt: `\text{Find the slope of the line through } (-3, -5) \text{ and } (2, -8).`
  - answer: `-\frac{3}{5}`

### D=8

- seed 101:
  - prompt: `\text{Find the slope of the line through } (3, 6) \text{ and } (-2, 11).`
  - answer: `-1`
- seed 207:
  - prompt: `\text{Find the slope of the line through } (-3, -8) \text{ and } (2, -11).`
  - answer: `-\frac{3}{5}`

### D=16

- seed 101:
  - prompt: `\text{Find the slope of the line through } (5, -1) \text{ and } (7, -6).`
  - answer: `-\frac{5}{2}`
- seed 207:
  - prompt: `\text{Find the slope of the line through } (11, -7) \text{ and } (6, -2).`
  - answer: `-1`

### D=22

- seed 101:
  - prompt: `\text{Find the slope of the line through } (5, -1) \text{ and } (7, -6).`
  - answer: `-\frac{5}{2}`
- seed 207:
  - prompt: `\text{Find the slope of the line through } (11, -7) \text{ and } (6, -2).`
  - answer: `-1`

## OpenStax examples + chapter/section cites

### Elementary Algebra 2e — 4.4 Understand Slope of a Line

- https://openstax.org/books/elementary-algebra-2e/pages/4-4-understand-slope-of-a-line
- Mined examples:
  - Example 4.25: What is the slope of the line on the geoboard shown?
  - Example 4.26: What is the slope of the line on the geoboard shown?
  - Example 4.27: Use a geoboard to model a line with slope $\frac{1}{2}$ .
  - Example 4.28: Use a geoboard to model a line with slope $\frac{−1}{4} .$

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- LIMITATIONS: shared gallery with `pa_slope`; A1 notes live here. Geoboard OpenStax examples not in engine.
- Must stay distinct from `more_on_slope` (parallel/perp).
- D≈16–22 can look flat (same fractional slopes) — audit numeric hardness before format unlocks.

## Proposed engine (reuse vs new)

Reuse slope generator. Graph-from-slope is a different leaf.

_Proposal only. No engine implementation in this notes pass._
