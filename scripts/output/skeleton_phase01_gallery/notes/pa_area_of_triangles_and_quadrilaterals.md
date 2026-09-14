# `pa_area_of_triangles_and_quadrilaterals` — Area of triangles and quadrilaterals

- **Course:** Prealgebra (PA catalog)
- **Category:** Pre-Algebra — Plane Figures
- **Generator:** `geo_triangles_and_quadrilaterals_area`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Find area. D=0: rectangle or right triangle with integer sides. High D: parallelogram / trapezoid; composite later only if old path already does.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{Find the area of the parallelogram.}`
  - answer: `24\text{ cm}^2`
- seed 207:
  - prompt: `\text{Find the area of the parallelogram.}`
  - answer: `48\text{ cm}^2`

### D=8

- seed 101:
  - prompt: `\text{Find the area of the square.}`
  - answer: `144\text{ cm}^2`
- seed 207:
  - prompt: `\text{Find the area of the kite.}`
  - answer: `12\text{ cm}^2`

### D=16

- seed 101:
  - prompt: `\text{Find the area of the square.}`
  - answer: `256\text{ cm}^2`
- seed 207:
  - prompt: `\text{Find the area of the kite.}`
  - answer: `52.5\text{ cm}^2`

### D=22

- seed 101:
  - prompt: `\text{Find the area of the square.}`
  - answer: `400\text{ cm}^2`
- seed 207:
  - prompt: `\text{Find the area of the kite.}`
  - answer: `71.5\text{ cm}^2`

## OpenStax examples + chapter/section cites

### Prealgebra 2e — 9.4 Use Properties of Rectangles, Triangles, and Trapezoids

- https://openstax.org/books/prealgebra-2e/pages/9-4-use-properties-of-rectangles-triangles-and-trapezoids
- Shape: A=bh, A=½bh, trapezoid formula.

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Old path can dump a bare equation / identity instead of the named skill.
- Story variety thin (one Mad-Lib / single vehicle) vs OpenStax frames.

## Proposed engine (reuse vs new)

Reuse geo_triangles_and_quadrilaterals_area.

_Proposal only. No engine implementation in this notes pass._
