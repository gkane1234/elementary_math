# `pa_plane_figures_triangles` — Triangles

- **Course:** Prealgebra (PA catalog)
- **Category:** Pre-Algebra — Plane Figures
- **Generator:** `geo_triangle_area`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Triangle measures: perimeter, area (½bh), maybe classify by sides. D=0 integer b,h. High D: missing height via a diagram, not trig.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{Find the area of } \triangle ABC.`
  - answer: `9\text{ cm}^{2}`
- seed 207:
  - prompt: `\text{Find the area of } \triangle ABC.`
  - answer: `21\text{ cm}^{2}`

### D=8

- seed 101:
  - prompt: `\text{Find the area of } \triangle ABC.`
  - answer: `42\text{ cm}^{2}`
- seed 207:
  - prompt: `\text{Find the area of } \triangle ABC.`
  - answer: `91\text{ cm}^{2}`

### D=16

- seed 101:
  - prompt: `\text{Find the area of } \triangle ABC.`
  - answer: `82.5\text{ cm}^{2}`
- seed 207:
  - prompt: `\text{Find the area of } \triangle ABC.`
  - answer: `52.5\text{ cm}^{2}`

### D=22

- seed 101:
  - prompt: `\text{Find the area of } \triangle ABC.`
  - answer: `157.5\text{ cm}^{2}`
- seed 207:
  - prompt: `\text{Find the area of } \triangle ABC.`
  - answer: `71.5\text{ cm}^{2}`

## OpenStax examples + chapter/section cites

### Prealgebra 2e — 9.4 Use Properties of Rectangles, Triangles, and Trapezoids

- https://openstax.org/books/prealgebra-2e/pages/9-4-use-properties-of-rectangles-triangles-and-trapezoids
- Shape: Triangle area A=½bh; perimeter as sum of sides.

### Prealgebra 2e — 9.3 Use Properties of Angles, Triangles, and the Pythagorean Theorem

- https://openstax.org/books/prealgebra-2e/pages/9-3-use-properties-of-angles-triangles-and-the-pythagorean-theorem
- Shape: Triangle angle sum 180°.

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Old path can dump a bare equation / identity instead of the named skill.
- Story variety thin (one Mad-Lib / single vehicle) vs OpenStax frames.

## Proposed engine (reuse vs new)

Reuse geo_triangle_area. Geometry — do not invent a poly engine.

_Proposal only. No engine implementation in this notes pass._
