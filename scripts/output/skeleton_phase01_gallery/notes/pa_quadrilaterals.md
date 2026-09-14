# `pa_quadrilaterals` — Quadrilaterals

> **UNCLEAR** — Leaf vs pa_area_of_triangles_and_quadrilaterals may duplicate area. Confirm old-path task (classify vs area vs perimeter).

- **Course:** Prealgebra (PA catalog)
- **Category:** Pre-Algebra — Plane Figures
- **Generator:** `geo_quadrilateral_area`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Rectangle/square/parallelogram/trapezoid: name, perimeter, or a missing side. Area can overlap the dedicated area leaf — prefer properties/perimeter here if old path does.

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
  - prompt: `\text{Find the area of the trapezoid.}`
  - answer: `132\text{ cm}^2`
- seed 207:
  - prompt: `\text{Find the area of the trapezoid.}`
  - answer: `70\text{ cm}^2`

### D=16

- seed 101:
  - prompt: `\text{Find the area of the trapezoid.}`
  - answer: `72\text{ cm}^2`
- seed 207:
  - prompt: `\text{Find the area of the trapezoid.}`
  - answer: `142.5\text{ cm}^2`

### D=22

- seed 101:
  - prompt: `\text{Find the area of the trapezoid.}`
  - answer: `333.5\text{ cm}^2`
- seed 207:
  - prompt: `\text{Find the area of the trapezoid.}`
  - answer: `262.5\text{ cm}^2`

## OpenStax examples + chapter/section cites

### Prealgebra 2e — 9.4 Use Properties of Rectangles, Triangles, and Trapezoids

- https://openstax.org/books/prealgebra-2e/pages/9-4-use-properties-of-rectangles-triangles-and-trapezoids
- Shape: Rectangle P=2L+2W; trapezoid area ½(b1+b2)h.

## Variety notes

Leaf vs pa_area_of_triangles_and_quadrilaterals may duplicate area. Confirm old-path task (classify vs area vs perimeter).

## Limitations

- Flags: **UNCLEAR**.
- Leaf vs pa_area_of_triangles_and_quadrilaterals may duplicate area. Confirm old-path task (classify vs area vs perimeter).

## Proposed engine (reuse vs new)

Reuse geo_quadrilateral_area. Check overlap with pa_area_of_triangles_and_quadrilaterals.

_Proposal only. No engine implementation in this notes pass._
