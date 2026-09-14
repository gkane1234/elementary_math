# `pa_transformations` — Transformations

> **UNCLEAR** — No Prealgebra/EA OpenStax chapter for transformations. Gold is old path + a geometry text, not PA 11.

- **Course:** Prealgebra (PA catalog)
- **Category:** Pre-Algebra — Plane Figures
- **Generator:** `geo_transformations`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Translate / reflect / rotate / dilate a figure on a grid. OpenStax **Prealgebra and Elementary Algebra do not teach this** — it is a middle-school / geometry topic. Copy old-path shapes; do not invent from PA text.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\triangle ABC\text{ shown on the coordinate plane is } \text{translated 1 unit left and 1 unit up}\text{. Graph the image.}`
  - answer: `A'(3, 2),\ B'(2, -3),\ C'(3, 0)`
- seed 207:
  - prompt: `\triangle ABC\text{ shown on the coordinate plane is } \text{translated 2 units right and 4 units up}\text{. Graph the image.}`
  - answer: `A'(0, 0),\ B'(3, 2),\ C'(5, 1)`

### D=8

- seed 101:
  - prompt: `\text{A square has vertices } A(-2, -1),\ B(1, -1),\ C(1, 2),\ D(-2, 2)\text{. The figure is } \text{rotated }90^\circ\text{ counterclockwise about the origin}\text{. Graph the image.}`
  - answer: `A'(1, -2),\ B'(1, 1),\ C'(-2, 1),\ D'(-2, -2)`
- seed 207:
  - prompt: `\text{A square has vertices } A(-3, -4),\ B(0, -4),\ C(0, -1),\ D(-3, -1)\text{. The figure is } \text{reflected across the }x\text{-axis}\text{. Graph the image.}`
  - answer: `A'(-3, 4),\ B'(0, 4),\ C'(0, 1),\ D'(-3, 1)`

### D=16

- seed 101:
  - prompt: `\text{The parallelogram shown on the coordinate plane is } \text{translated 1 unit left and 1 unit up}\text{, then reflected across the }x\text{-axis}\text{. Graph the image.}`
  - answer: `A'(-1, 1),\ B'(2, 1),\ C'(3, -1),\ D'(0, -1)`
- seed 207:
  - prompt: `\triangle ABC\text{ has vertices } A(0, 2),\ B(1, -1),\ C(1, 1)\text{. The figure is } \text{dilated by a factor of } 2\text{ centered at the origin}\text{. Graph the image.}`
  - answer: `A'(0, 4),\ B'(2, -2),\ C'(2, 2)`

### D=22

- seed 101:
  - prompt: `\text{The parallelogram shown on the coordinate plane is } \text{translated 1 unit left and 1 unit up}\text{, then reflected across the }x\text{-axis}\text{. Graph the image.}`
  - answer: `A'(-1, 1),\ B'(2, 1),\ C'(3, -1),\ D'(0, -1)`
- seed 207:
  - prompt: `\triangle ABC\text{ has vertices } A(0, 2),\ B(1, -1),\ C(1, 1)\text{. The figure is } \text{dilated by a factor of } 2\text{ centered at the origin}\text{. Graph the image.}`
  - answer: `A'(0, 4),\ B'(2, -2),\ C'(2, 2)`

## OpenStax examples + chapter/section cites

### Prealgebra 2e — 11.1 Use the Rectangular Coordinate System

- https://openstax.org/books/prealgebra-2e/pages/11-1-use-the-rectangular-coordinate-system
- Shape: Nearest PA content is plotting points — not rigid motions.

## Variety notes

No Prealgebra/EA OpenStax chapter for transformations. Gold is old path + a geometry text, not PA 11.

## Limitations

- Flags: **UNCLEAR**.
- No Prealgebra/EA OpenStax chapter for transformations. Gold is old path + a geometry text, not PA 11.

## Proposed engine (reuse vs new)

Reuse geo_transformations. No PA/EA OpenStax chapter — keep old shapes; do not force a SolveLinear rewrite.

_Proposal only. No engine implementation in this notes pass._
