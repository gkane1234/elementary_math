# `pa_angle_relationships` — Angle relationships

- **Course:** Prealgebra (PA catalog)
- **Category:** Pre-Algebra — Plane Figures
- **Generator:** `geo_angle_relationships`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

D=0: complementary (x+40=90) or supplementary. High D: vertical / adjacent / triangle-sum. Keep PA-level (no parallel-line transveral soup unless the old path already has it).

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{The diagram shows vertical angles formed by intersecting lines. Find the measure of the unmarked angle.}`
  - answer: `50^\circ`
- seed 207:
  - prompt: `\text{The diagram shows vertical angles formed by intersecting lines. Find the measure of the unmarked angle.}`
  - answer: `100^\circ`

### D=8

- seed 101:
  - prompt: `\text{The diagram shows vertical angles formed by intersecting lines. Find the measure of the unmarked angle.}`
  - answer: `50^\circ`
- seed 207:
  - prompt: `\text{The diagram shows vertical angles formed by intersecting lines. Find the measure of the unmarked angle.}`
  - answer: `100^\circ`

### D=16

- seed 101:
  - prompt: `\text{The diagram shows vertical angles formed by intersecting lines. Find the measure of the unmarked angle.}`
  - answer: `50^\circ`
- seed 207:
  - prompt: `\text{The diagram shows vertical angles formed by intersecting lines. Find the measure of the unmarked angle.}`
  - answer: `100^\circ`

### D=22

- seed 101:
  - prompt: `\text{The diagram shows vertical angles formed by intersecting lines. Find the measure of the unmarked angle.}`
  - answer: `50^\circ`
- seed 207:
  - prompt: `\text{The diagram shows vertical angles formed by intersecting lines. Find the measure of the unmarked angle.}`
  - answer: `100^\circ`

## OpenStax examples + chapter/section cites

### Prealgebra 2e — 9.3 Use Properties of Angles, Triangles, and the Pythagorean Theorem

- https://openstax.org/books/prealgebra-2e/pages/9-3-use-properties-of-angles-triangles-and-the-pythagorean-theorem
- Shape: Complementary, supplementary, triangle angle sum.

## Variety notes

Old path shapes at D=0 vs D=22 are recorded above. Flag if a WP dump stub or a single Mad-Lib.

## Limitations

- Old path can dump a bare equation / identity instead of the named skill.
- Story variety thin (one Mad-Lib / single vehicle) vs OpenStax frames.

## Proposed engine (reuse vs new)

Reuse geo_angle_relationships. Optional SolveLinear for the algebra once the diagram exists — same geometry primitive.

_Proposal only. No engine implementation in this notes pass._
