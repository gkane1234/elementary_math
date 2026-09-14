# `pa_circles` — Circles

- **Course:** Prealgebra (PA catalog)
- **Category:** Pre-Algebra — Plane Figures
- **Generator:** `geo_circle_measure`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

D=0: circumference or area with integer r and π left in the answer (or 3.14). High D: given diameter, or find r from C/A.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{Find the circumference of a circle with radius } 6\text{ cm}.`
  - answer: `12\pi\text{ cm}`
- seed 207:
  - prompt: `\text{Find the circumference of a circle with radius } 6\text{ cm}.`
  - answer: `12\pi\text{ cm}`

### D=8

- seed 101:
  - prompt: `\text{Find the circumference of a circle with radius } 6\text{ cm}.`
  - answer: `12\pi\text{ cm}`
- seed 207:
  - prompt: `\text{Find the circumference of a circle with radius } 6\text{ cm}.`
  - answer: `12\pi\text{ cm}`

### D=16

- seed 101:
  - prompt: `\text{Find the area of a circle with radius } 8\text{ cm}.`
  - answer: `64\pi\text{ cm}^{2}`
- seed 207:
  - prompt: `\text{Find the circumference of a circle with radius } 18\text{ cm}.`
  - answer: `36\pi\text{ cm}`

### D=22

- seed 101:
  - prompt: `\text{Find the circumference of a circle with radius } 20\text{ cm}.`
  - answer: `40\pi\text{ cm}`
- seed 207:
  - prompt: `\text{Find the circumference of a circle with radius } 18\text{ cm}.`
  - answer: `36\pi\text{ cm}`

## OpenStax examples + chapter/section cites

### Prealgebra 2e — 9.5 Solve Geometry Applications: Circles and Irregular Figures

- https://openstax.org/books/prealgebra-2e/pages/9-5-solve-geometry-applications-circles-and-irregular-figures
- Shape: C=2πr, A=πr²; irregular figures as optional extra.

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Old path can dump a bare equation / identity instead of the named skill.
- Story variety thin (one Mad-Lib / single vehicle) vs OpenStax frames.

## Proposed engine (reuse vs new)

Reuse geo_circle_measure.

_Proposal only. No engine implementation in this notes pass._
