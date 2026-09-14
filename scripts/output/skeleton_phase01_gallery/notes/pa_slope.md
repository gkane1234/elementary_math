# `pa_slope` — Slope

- **Course:** Prealgebra (PA catalog)
- **Category:** Pre-Algebra — Linear Equations and Inequalities
- **Generator:** `slope`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

D=0: slope between two lattice points with integer rise/run, maybe already reduced. High D: negative / zero / undefined; or from slope-intercept identification.

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

### Prealgebra 2e — 11.4 Understand Slope of a Line

- https://openstax.org/books/prealgebra-2e/pages/11-4-understand-slope-of-a-line
- Shape: m=(y2−y1)/(x2−x1); horizontal m=0; vertical undefined.

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

- Old path can dump a bare equation / identity instead of the named skill.
- Story variety thin (one Mad-Lib / single vehicle) vs OpenStax frames.

## Proposed engine (reuse vs new)

Reuse slope generator (already on PRIM_EQUATIONS map). No new engine; graphing-from-slope is a different skill.

_Proposal only. No engine implementation in this notes pass._
