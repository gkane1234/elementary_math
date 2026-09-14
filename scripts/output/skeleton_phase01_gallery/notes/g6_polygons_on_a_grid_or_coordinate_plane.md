# `g6_polygons_on_a_grid_or_coordinate_plane` — Polygons on a grid or coordinate plane


Steps 1–3 only (old live samples, intended look, OpenStax). No engine implementation.

## What the question should look like (D=0 vs high D)

**D=0:** unit-grid square or rectangle; count square units (or `ℓ×w`).

**High D:** parallelogram / triangle on grid, then trapezoid, then L-shape or irregular quad (subtract triangles). Areas may be halves. Still counting / decompose, not Pick’s theorem.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22, `include_answer_key=True`, seeds 101 and 202. Default path **is** the old path (these leaves are not on equation/poly skeletons). One sample per D below (seed 101).

| D | Prompt (latex) | Answer |
|--:|----------------|--------|
| 0 | `$\text{Find the area of the triangle on the grid.}$` | `$6\text{ square units}$` |
| 8 | `$\text{Find the area of the parallelogram on the grid.}$` | `$9\text{ square units}$` |
| 16 | `$\text{Find the area of the L-shaped polygon on the grid.}$` | `$13\text{ square units}$` |
| 22 | `$\text{Find the area of the irregular quadrilateral on the grid.}$` | `$3\text{ square units}$` |

Second seed (202) at D=0 and D=22:

- D=0: `$\text{Find the area of the rectangle on the grid.}$` → `$10\text{ square units}$`
- D=22: `$\text{Find the area of the irregular quadrilateral on the grid.}$` → `$\frac{9}{2}\text{ square units}$`

## OpenStax examples + chapter/section

**Prealgebra 2e §9.5** *Circles and Irregular Figures* ([link](https://openstax.org/books/prealgebra-2e/pages/9-5-solve-geometry-applications-circles-and-irregular-figures)) — add/subtract rectangular (and triangular) pieces.
**§9.4** for the component formulas. Coordinates from **§11.1** if vertices are named.

G6 classroom: **IM Grade 6 Unit 1** polygons on grids.

## Variety notes

Old path actually rotates shapes (square/rect → parallelogram → trapezoid → L / irregular). That is enough variety; keep it. Stem is still “Find the area of the ___ on the grid.”

## Limitations

- Old path actually rotates shapes (square/rect → parallelogram → trapezoid → L / irregular). That is enough variety; keep it. Stem is still “Find the area of the ___ on the grid.”

## Proposed engine (proposal only)

geometry grid-area (existing `g6_polygon_grid_area`). Not affine.

Generator (catalog): see `question_engine/catalogs/grade_6.py`.
