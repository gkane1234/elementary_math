# `pa_classifying_volume_and_surface_area` — Classifying, volume, and surface area

- **Course:** Prealgebra (PA catalog)
- **Category:** Pre-Algebra — Solid Figures
- **Generator:** `geo_solid_volume_surface`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

D=0: rectangular prism volume lwh. High D: surface area, cylinder, or classify the solid. PA 9.6 is the gold.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{Find the volume of a cylinder with radius } 3\text{ cm} \text{ and height } 10\text{ cm}.`
  - answer: `9\pi \cdot 10\text{ cm}^{3}`
- seed 207:
  - prompt: `\text{Find the volume of a cylinder with radius } 2\text{ cm} \text{ and height } 5\text{ cm}.`
  - answer: `4\pi \cdot 5\text{ cm}^{3}`

### D=8

- seed 101:
  - prompt: `\text{Find the volume of a cylinder with radius } 4\text{ cm} \text{ and height } 10\text{ cm}.`
  - answer: `16\pi \cdot 10\text{ cm}^{3}`
- seed 207:
  - prompt: `\text{Find the volume of a cylinder with radius } 3\text{ cm} \text{ and height } 5\text{ cm}.`
  - answer: `9\pi \cdot 5\text{ cm}^{3}`

### D=16

- seed 101:
  - prompt: `\text{Find the volume of a cylinder with radius } 6\text{ cm} \text{ and height } 16\text{ cm}.`
  - answer: `36\pi \cdot 16\text{ cm}^{3}`
- seed 207:
  - prompt: `\text{Find the volume of a cylinder with radius } 6\text{ cm} \text{ and height } 12\text{ cm}.`
  - answer: `36\pi \cdot 12\text{ cm}^{3}`

### D=22

- seed 101:
  - prompt: `\text{Find the volume of a cylinder with radius } 7\text{ cm} \text{ and height } 19\text{ cm}.`
  - answer: `49\pi \cdot 19\text{ cm}^{3}`
- seed 207:
  - prompt: `\text{Find the volume of a cylinder with radius } 5\text{ cm} \text{ and height } 28\text{ cm}.`
  - answer: `25\pi \cdot 28\text{ cm}^{3}`

## OpenStax examples + chapter/section cites

### Prealgebra 2e — 9.6 Solve Geometry Applications: Volume and Surface Area

- https://openstax.org/books/prealgebra-2e/pages/9-6-solve-geometry-applications-volume-and-surface-area
- Shape: Rectangular solid V=lwh; cylinder V=πr²h; SA of a box.

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Old path can dump a bare equation / identity instead of the named skill.
- Story variety thin (one Mad-Lib / single vehicle) vs OpenStax frames.

## Proposed engine (reuse vs new)

Reuse geo_solid_volume_surface.

_Proposal only. No engine implementation in this notes pass._
