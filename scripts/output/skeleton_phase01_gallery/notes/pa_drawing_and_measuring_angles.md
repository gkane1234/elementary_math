# `pa_drawing_and_measuring_angles` — Drawing and measuring angles

> **UNCLEAR** — OpenStax PA 9.3 is angle *properties* more than drawing/measuring with a protractor. Confirm old path matches the leaf name.

- **Course:** Prealgebra (PA catalog)
- **Category:** Pre-Algebra — Plane Figures
- **Generator:** `geo_angles`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

D=0: name/measure an acute angle from a diagram, or classify acute/right/obtuse. High D: draw to a given measure. PA 9.3 is properties more than protractor skill.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{Find } m\angle CDB\text{ using the diagram.}`
  - answer: `108^\circ`
- seed 207:
  - prompt: `\text{Ray } DF\text{ is drawn. Draw ray } DB\text{ so that } m\angle FDB = 20^\circ.`
  - answer: `20^\circ`

### D=8

- seed 101:
  - prompt: `\text{Find } m\angle DEC\text{ using the diagram.}`
  - answer: `120^\circ`
- seed 207:
  - prompt: `\text{Find } m\angle GHF\text{ using the diagram.}`
  - answer: `145^\circ`

### D=16

- seed 101:
  - prompt: `\text{Find } m\angle AFB\text{ using the diagram.}`
  - answer: `52^\circ`
- seed 207:
  - prompt: `\text{Find } m\angle BFA\text{ using the diagram.}`
  - answer: `47^\circ`

### D=22

- seed 101:
  - prompt: `\text{Find } m\angle AFB\text{ using the diagram.}`
  - answer: `52^\circ`
- seed 207:
  - prompt: `\text{Find } m\angle BFA\text{ using the diagram.}`
  - answer: `47^\circ`

## OpenStax examples + chapter/section cites

### Prealgebra 2e — 9.3 Use Properties of Angles, Triangles, and the Pythagorean Theorem

- https://openstax.org/books/prealgebra-2e/pages/9-3-use-properties-of-angles-triangles-and-the-pythagorean-theorem
- Shape: Classify angles; complementary/supplementary as a related skill (sibling leaf).

## Variety notes

OpenStax PA 9.3 is angle *properties* more than drawing/measuring with a protractor. Confirm old path matches the leaf name.

## Limitations

- Flags: **UNCLEAR**.
- OpenStax PA 9.3 is angle *properties* more than drawing/measuring with a protractor. Confirm old path matches the leaf name.

## Proposed engine (reuse vs new)

Reuse geo_angles. Geometry engine — not affine.

_Proposal only. No engine implementation in this notes pass._
