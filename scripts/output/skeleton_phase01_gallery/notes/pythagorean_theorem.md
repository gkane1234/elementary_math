# `pythagorean_theorem` — The Pythagorean Theorem

- **Course:** Prealgebra (PA catalog)
- **Category:** Pre-Algebra — Right Triangles
- **Generator:** `geo_pythagorean_theorem`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

D=0: 3-4-5 missing hypotenuse. High D: missing a leg, or a short application (ladder / TV diagonal) if old path has it. No trig.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{In right } \triangle ABC,\ \text{find } AC.`
  - answer: `13\text{ cm}`
- seed 207:
  - prompt: `\text{In right } \triangle ABC,\ \text{find } AC.`
  - answer: `13\text{ cm}`

### D=8

- seed 101:
  - prompt: `\text{In right } \triangle ABC,\ \text{find } AB.`
  - answer: `9\text{ cm}`
- seed 207:
  - prompt: `\text{In right } \triangle ABC,\ \text{find } AC.`
  - answer: `15\text{ cm}`

### D=16

- seed 101:
  - prompt: `\text{In right } \triangle ABC,\ \text{find } AB.`
  - answer: `7\text{ cm}`
- seed 207:
  - prompt: `\text{In right } \triangle ABC,\ \text{find } AC.`
  - answer: `25\text{ cm}`

### D=22

- seed 101:
  - prompt: `\text{In right } \triangle ABC,\ \text{find } AB.`
  - answer: `7\text{ cm}`
- seed 207:
  - prompt: `\text{In right } \triangle ABC,\ \text{find } AC.`
  - answer: `25\text{ cm}`

## OpenStax examples + chapter/section cites

### Prealgebra 2e — 9.3 Use Properties of Angles, Triangles, and the Pythagorean Theorem

- https://openstax.org/books/prealgebra-2e/pages/9-3-use-properties-of-angles-triangles-and-the-pythagorean-theorem
- Shape: a²+b²=c²; 5-12-13 and 6-8-10 families.

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Old path can dump a bare equation / identity instead of the named skill.
- Story variety thin (one Mad-Lib / single vehicle) vs OpenStax frames.
- Weak / missing OpenStax chapter match for this leaf.

## Proposed engine (reuse vs new)

Reuse geo_pythagorean_theorem. Catalog id has no pa_ prefix but it is a PA leaf.

_Proposal only. No engine implementation in this notes pass._
