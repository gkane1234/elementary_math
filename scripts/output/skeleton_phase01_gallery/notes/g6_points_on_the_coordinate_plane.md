# `g6_points_on_the_coordinate_plane` — Points on the coordinate plane

Old path was an identity dump (`(x,y)` → `(x,y)`). Default now plots or identifies a labeled point (OpenStax 11.1).

Steps 1–3 only (old live samples, intended look, OpenStax). No engine implementation.

## What the question should look like (D=0 vs high D)

**D=0:** Quadrant I small integers; either *plot* `(3,2)` or *name* a labeled point. Instruction in catalog is “Identify the point.”

**High D:** four quadrants and axis intercepts (OpenStax 11.1). Still one ordered pair, not graphing lines.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22, `include_answer_key=True`, seeds 101 and 202. Default path **is** the old path (these leaves are not on equation/poly skeletons). One sample per D below (seed 101).

| D | Prompt (latex) | Answer |
|--:|----------------|--------|
| 0 | `$(4, -2)$` | `$(4, -2)$` |
| 8 | `$(-2, 3)$` | `$(-2, 3)$` |
| 16 | `$(6, -6)$` | `$(6, -6)$` |
| 22 | `$(6, -6)$` | `$(6, -6)$` |

Second seed (202) at D=0 and D=22:

- D=0: `$(1, 5)$` → `$(1, 5)$`
- D=22: `$(12, 0)$` → `$(12, 0)$`

## OpenStax examples + chapter/section

**OpenStax Prealgebra 2e §11.1** *Use the Rectangular Coordinate System* ([link](https://openstax.org/books/prealgebra-2e/pages/11-1-use-the-rectangular-coordinate-system)).

- Plot points; identify quadrants I–IV.
- “Identify points on a graph” (read a labeled point’s ordered pair).
- Campus-map grid (letter/number) as a pre-coordinate warm-up.
- Later objectives in 11.1 (table of solutions, graph `y=mx+b`) are **PA/A1**, not this G6 leaf.

Also **Elementary Algebra 2e §4.1** (same plot/read skill).
G6 all-four-quadrants: **IM Grade 6 Unit 7**.

## Variety notes

Old live prompt was a bare ordered pair. GeometryMeasure now mixes **plot** (blank plane) and **identify** (labeled point A). D=0 stays Q1; later D uses four quadrants and intercepts.

## Limitations

- Old live prompt was a bare ordered pair. GeometryMeasure now mixes **plot** (blank plane) and **identify** (labeled point A). D=0 stays Q1; later D uses four quadrants and intercepts.

## Proposed engine (proposal only)

geometry / coordinate-plane graph spec (`plotting_points`). Fix the stem in a later engine pass: plot **or** read a labeled point, not identity `(x,y)→(x,y)`.

Generator (catalog): see `question_engine/catalogs/grade_6.py`.
