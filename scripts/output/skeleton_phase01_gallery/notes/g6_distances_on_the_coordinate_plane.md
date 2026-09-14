# `g6_distances_on_the_coordinate_plane` — Distances on the coordinate plane

Steps 1–3 only (old live samples, intended look, OpenStax). No engine implementation.

## What the question should look like (D=0 vs high D)

**D=0:** two points that share a y-coordinate (horizontal); distance `|x2-x1|` small.

**High D:** still **axis-aligned only** (G6 — no Pythagorean). Unlock vertical segments, then mixed H/V, then points in other quadrants. Numbers can grow; do not introduce diagonal distance.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22, `include_answer_key=True`, seeds 101 and 202. Default path **is** the old path (these leaves are not on equation/poly skeletons). One sample per D below (seed 101).

| D | Prompt (latex) | Answer |
|--:|----------------|--------|
| 0 | `$\text{Find the distance between } (4, -2) \text{ and } (2, -2).$` | `$2$` |
| 8 | `$\text{Find the distance between } (-2, 3) \text{ and } (-7, 3).$` | `$5$` |
| 16 | `$\text{Find the distance between } (8, -4) \text{ and } (4, -4).$` | `$4$` |
| 22 | `$\text{Find the distance between } (7, -5) \text{ and } (3, -5).$` | `$4$` |

Second seed (202) at D=0 and D=22:

- D=0: `$\text{Find the distance between } (1, 5) \text{ and } (-2, 5).$` → `$3$`
- D=22: `$\text{Find the distance between } (1, 9) \text{ and } (2, 9).$` → `$1$`

## OpenStax examples + chapter/section

OpenStax **Prealgebra 2e §11.1** plots points but does **not** teach distance. Diagonal distance would be **§9.3 Pythagorean Theorem** (out of G6 band).

G6 gold: **IM Grade 6 Unit 7** — distance between points with the same `x` or same `y` using absolute value / counting units.

Story versions belong on `g6_coordinate_plane_distances_word_problems`.

## Variety notes

Old samples were all horizontal. GeometryMeasure D=0 stays horizontal; vertical unlocks by D=8–16. Stem is still one sentence plus a diagram.

## Limitations

- Old samples were all horizontal. GeometryMeasure D=0 stays horizontal; vertical unlocks by D=8–16. Stem is still one sentence plus a diagram.

## Proposed engine (proposal only)

geometry coordinate: sample two axis-aligned points. Reuse graph spec. Not SolveLinear.

Generator (catalog): see `question_engine/catalogs/grade_6.py`.
