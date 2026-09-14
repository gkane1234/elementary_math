# `g6_shapes_and_perimeter_on_the_coordinate_plane` — Shapes and perimeter on the coordinate plane

> RED HEADER: **LOW_VARIETY**
>
> Ship samples anyway. Implementation must not treat a green checkbox as success if the old stem is a stub or a single template.

Steps 1–3 only (old live samples, intended look, OpenStax). No engine implementation.

## What the question should look like (D=0 vs high D)

**D=0:** axis-aligned rectangle in Q1; vertices listed; find **perimeter** (count units / `|Δx|+|Δy|` twice).

**High D:** still perimeter (or area if we split — old path is perimeter-only). Unlock Q2–Q4 vertices, then maybe a right triangle / square. Not irregular polygons (that is the grid-area leaf).

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22, `include_answer_key=True`, seeds 101 and 202. Default path **is** the old path (these leaves are not on equation/poly skeletons). One sample per D below (seed 101).

| D | Prompt (latex) | Answer |
|--:|----------------|--------|
| 0 | `$\text{A rectangle on the coordinate plane has vertices } A(2, 2),\ B(6, 2),\ C(6, 4),\ D(2, 4)\text{. Find the perimeter.}$` | `$12$` |
| 8 | `$\text{A rectangle on the coordinate plane has vertices } A(4, -3),\ B(7, -3),\ C(7, 1),\ D(4, 1)\text{. Find the perimeter.}$` | `$14$` |
| 16 | `$\text{A rectangle on the coordinate plane has vertices } A(0, 2),\ B(3, 2),\ C(3, 8),\ D(0, 8)\text{. Find the perimeter.}$` | `$18$` |
| 22 | `$\text{A rectangle on the coordinate plane has vertices } A(0, 2),\ B(3, 2),\ C(3, 8),\ D(0, 8)\text{. Find the perimeter.}$` | `$18$` |

Second seed (202) at D=0 and D=22:

- D=0: `$\text{A rectangle on the coordinate plane has vertices } A(3, 1),\ B(6, 1),\ C(6, 5),\ D(3, 5)\text{. Find the perimeter.}$` → `$14$`
- D=22: `$\text{A rectangle on the coordinate plane has vertices } A(-2, 5),\ B(3, 5),\ C(3, 8),\ D(-2, 8)\text{. Find the perimeter.}$` → `$16$`

## OpenStax examples + chapter/section

Perimeter formulas: **Prealgebra 2e §9.4** (`P=2L+2W` for rectangles). Coordinates: **§11.1**. Combining them is G6/IM: plot a rectangle from vertices, then `P`.

OpenStax does not have a dedicated “polygon on the coordinate plane” exercise set; IM Grade 6 Unit 7 + Unit 1 is the classroom shape.

## Variety notes

**LOW_VARIETY:** every sample is “A rectangle on the coordinate plane has vertices A,B,C,D. Find the perimeter.” D=16 and D=22 identical in this pack. No triangles, no area ask, no “draw then measure”.

## Limitations

- Flags: **LOW_VARIETY**.
- **LOW_VARIETY:** every sample is “A rectangle on the coordinate plane has vertices A,B,C,D. Find the perimeter.” D=16 and D=22 identical in this pack. No triangles, no area ask, no “draw then measure”.

## Proposed engine (proposal only)

geometry: rectangle (later square) from integer vertices + perimeter. Diagram SVG already present.

Generator (catalog): see `question_engine/catalogs/grade_6.py`.
