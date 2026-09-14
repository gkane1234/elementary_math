# `g6_polygons_and_shaded_regions` — Polygons and shaded regions

Old path prefixed “shaded” on the same grid-polygon generator. Default is now outer − inner composite (OpenStax 9.5).

Steps 1–3 only (old live samples, intended look, OpenStax). No engine implementation.

## What the question should look like (D=0 vs high D)

**D=0 (intended):** shaded region = rectangle minus a corner triangle, or shaded frame (outer − inner). Small grid.

**Old path:** same generator family as grid polygons with the word “shaded” prefixed. D=0 is a shaded triangle/rectangle, not outer-minus-inner.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22, `include_answer_key=True`, seeds 101 and 202. Default path **is** the old path (these leaves are not on equation/poly skeletons). One sample per D below (seed 101).

| D | Prompt (latex) | Answer |
|--:|----------------|--------|
| 0 | `$\text{Find the area of the shaded triangle on the grid.}$` | `$6\text{ square units}$` |
| 8 | `$\text{Find the area of the shaded parallelogram on the grid.}$` | `$9\text{ square units}$` |
| 16 | `$\text{Find the area of the shaded L-shaped polygon on the grid.}$` | `$13\text{ square units}$` |
| 22 | `$\text{Find the area of the shaded irregular quadrilateral on the grid.}$` | `$3\text{ square units}$` |

Second seed (202) at D=0 and D=22:

- D=0: `$\text{Find the area of the shaded rectangle on the grid.}$` → `$10\text{ square units}$`
- D=22: `$\text{Find the area of the shaded irregular quadrilateral on the grid.}$` → `$\frac{9}{2}\text{ square units}$`

## OpenStax examples + chapter/section

**Prealgebra 2e §9.5** irregular / composite: e.g. L-shaped patio = two rectangles, or shaded region around a square. That **is** the OpenStax shape this leaf should copy.

Shipped as composite: rectangle minus a corner triangle, frame (outer − inner), or L-cut. Distinct from the grid-polygon sibling.

## Variety notes

Construction mix ramps with D (`rect_minus_triangle` → `frame` / `l_cut`). Stem is still “shaded region on the grid.”

## Limitations

- Construction mix ramps with D (`rect_minus_triangle` → `frame` / `l_cut`). Stem is still “shaded region on the grid.”

## Proposed engine (proposal only)

geometry composite (outer − inner or two rectangles). Reuse grid diagram; change the ask.

Generator (catalog): see `question_engine/catalogs/grade_6.py`.
