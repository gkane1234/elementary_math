# `find_missing_sides_of_triangles` — Find missing sides of triangles

> **UNCLEAR** — Not in EA TOC. Must not become pythagorean_theorem.

- **Course:** Algebra 1
- **Category:** Algebra 1 — Beginning Trigonometry
- **Generator:** `geo_right_triangle_trig_side`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Right triangle: missing side via sin/cos/tan (not only Pythagorean). D=0: 30-60-90 or given one acute + one side.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{In right } \triangle ABC,\ m\angle A = 60^\circ,\ BC = 5\text{ cm}.\ \text{Find } AC.`
  - answer: `\frac{5}{\tan 60^\circ}`
- seed 207:
  - prompt: `\text{In right } \triangle ABC,\ m\angle A = 60^\circ,\ AC = 12\text{ cm}.\ \text{Find } BC.`
  - answer: `12\tan 60^\circ`

### D=8

- seed 101:
  - prompt: `\text{In right } \triangle ABC,\ m\angle A = 30^\circ,\ BC = 9\text{ cm}.\ \text{Find } AB.`
  - answer: `\frac{9}{\sin 30^\circ}`
- seed 207:
  - prompt: `\text{In right } \triangle ABC,\ m\angle A = 60^\circ,\ BC = 9\text{ cm}.\ \text{Find } AB.`
  - answer: `\frac{9}{\sin 60^\circ}`

### D=16

- seed 101:
  - prompt: `\text{In right } \triangle ABC,\ m\angle A = 60^\circ,\ BC = 7\text{ cm}.\ \text{Find } AC.`
  - answer: `\frac{7}{\tan 60^\circ}`
- seed 207:
  - prompt: `\text{In right } \triangle ABC,\ m\angle A = 60^\circ,\ AC = 24\text{ cm}.\ \text{Find } BC.`
  - answer: `24\tan 60^\circ`

### D=22

- seed 101:
  - prompt: `\text{In right } \triangle ABC,\ m\angle A = 60^\circ,\ BC = 7\text{ cm}.\ \text{Find } AC.`
  - answer: `\frac{7}{\tan 60^\circ}`
- seed 207:
  - prompt: `\text{In right } \triangle ABC,\ m\angle A = 60^\circ,\ AC = 24\text{ cm}.\ \text{Find } BC.`
  - answer: `24\tan 60^\circ`

## OpenStax examples + chapter/section cites

### Algebra and Trigonometry 2e — 7.2 Right Triangle Trigonometry

- https://openstax.org/books/algebra-and-trigonometry-2e/pages/7-2-right-triangle-trigonometry
- Shape: Given an acute angle and a side, find another side.

### Prealgebra 2e — 9.3 Use Properties of Angles, Triangles, and the Pythagorean Theorem

- https://openstax.org/books/prealgebra-2e/pages/9-3-use-properties-of-angles-triangles-and-the-pythagorean-theorem
- Shape: Pythagorean is a different leaf; this one is trig.

## Variety notes

Not in EA TOC. Must not become pythagorean_theorem.

## Limitations

- UNCLEAR / LIMITATIONS: must not become `pythagorean_theorem` leaf.

## Proposed engine (reuse vs new)

Reuse geo_right_triangle_trig_side. Do not dump Pythagorean-only items here.

_Proposal only. No engine implementation in this notes pass._
