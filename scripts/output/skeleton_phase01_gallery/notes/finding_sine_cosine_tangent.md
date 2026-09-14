# `finding_sine_cosine_tangent` — Finding sine, cosine, tangent

> **UNCLEAR** — Trig is extra vs Elementary Algebra TOC. Gold is Algebra and Trigonometry 7.2 + old path.

- **Course:** Algebra 1
- **Category:** Algebra 1 — Beginning Trigonometry
- **Generator:** `geo_right_triangle_trig_ratio`
- **Already on skeleton?** no
- **No skeleton opt-out (old path is the live default).**

## What the question should look like (D=0 vs high D)

Right-triangle trig ratio from two sides. D=0: identfy opp/adj/hyp on a labeled 3-4-5. High D: simplify a fraction.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22 (seeds 101 and 207).

### D=0

- seed 101:
  - prompt: `\text{In right } \triangle ABC \text{ with right angle at } C,\ \text{find } \tan A.`
  - answer: `\frac{5}{12}`
- seed 207:
  - prompt: `\text{In right } \triangle ABC \text{ with right angle at } C,\ \text{find } \tan A.`
  - answer: `\frac{5}{12}`

### D=8

- seed 101:
  - prompt: `\text{In right } \triangle ABC \text{ with right angle at } C,\ \text{find } \sin A.`
  - answer: `\frac{9}{15}`
- seed 207:
  - prompt: `\text{In right } \triangle ABC \text{ with right angle at } C,\ \text{find } \tan A.`
  - answer: `\frac{9}{12}`

### D=16

- seed 101:
  - prompt: `\text{In right } \triangle ABC \text{ with right angle at } C,\ \text{find } \tan A.`
  - answer: `\frac{7}{24}`
- seed 207:
  - prompt: `\text{In right } \triangle ABC \text{ with right angle at } C,\ \text{find } \tan A.`
  - answer: `\frac{7}{24}`

### D=22

- seed 101:
  - prompt: `\text{In right } \triangle ABC \text{ with right angle at } C,\ \text{find } \tan A.`
  - answer: `\frac{7}{24}`
- seed 207:
  - prompt: `\text{In right } \triangle ABC \text{ with right angle at } C,\ \text{find } \tan A.`
  - answer: `\frac{7}{24}`

## OpenStax examples + chapter/section cites

### Algebra and Trigonometry 2e — 7.2 Right Triangle Trigonometry

- https://openstax.org/books/algebra-and-trigonometry-2e/pages/7-2-right-triangle-trigonometry
- Shape: sin=opp/hyp, cos=adj/hyp, tan=opp/adj on a right triangle.

### Prealgebra 2e — 9.3 Use Properties of Angles, Triangles, and the Pythagorean Theorem

- https://openstax.org/books/prealgebra-2e/pages/9-3-use-properties-of-angles-triangles-and-the-pythagorean-theorem
- Shape: Nearest PA/EA content is Pythagorean — not trig ratios.

## Variety notes

Trig is extra vs Elementary Algebra TOC. Gold is Algebra and Trigonometry 7.2 + old path.

## Limitations

- UNCLEAR / LIMITATIONS: trig extra vs EA TOC; gold Algebra and Trigonometry + old path. Must not become Pythagorean.

## Proposed engine (reuse vs new)

Reuse geo_right_triangle_trig_ratio. No EA chapter — copy old diagrams.

_Proposal only. No engine implementation in this notes pass._
