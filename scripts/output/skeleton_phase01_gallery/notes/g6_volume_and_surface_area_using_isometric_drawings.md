# `g6_volume_and_surface_area_using_isometric_drawings` — Volume and surface area using isometric drawings

> RED HEADER: **UNCLEAR** · **LOW_VARIETY**
>
> Ship samples anyway. Implementation must not treat a green checkbox as success if the old stem is a stub or a single template.

Steps 1–3 only (old live samples, intended look, OpenStax). No engine implementation.

## What the question should look like (D=0 vs high D)

**D=0:** isometric unit-cube rectangular prism; count cubes for volume (e.g. 2×3×3=18).

**High D:** ask surface area (count exposed faces), larger dimensions. Still a rectangular stack, not spheres/cylinders (those are OpenStax 9.6 extras, PA+).

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22, `include_answer_key=True`, seeds 101 and 202. Default path **is** the old path (these leaves are not on equation/poly skeletons). One sample per D below (seed 101).

| D | Prompt (latex) | Answer |
|--:|----------------|--------|
| 0 | `$\text{Use the drawing to find the volume.}$` | `$18\text{ cubic units}$` |
| 8 | `$\text{Use the drawing to find the volume.}$` | `$36\text{ cubic units}$` |
| 16 | `$\text{Use the drawing to find the surface area.}$` | `$126\text{ square units}$` |
| 22 | `$\text{Use the drawing to find the surface area.}$` | `$126\text{ square units}$` |

Second seed (202) at D=0 and D=22:

- D=0: `$\text{Use the drawing to find the volume.}$` → `$18\text{ cubic units}$`
- D=22: `$\text{Use the drawing to find the volume.}$` → `$144\text{ cubic units}$`

## OpenStax examples + chapter/section

**Prealgebra 2e §9.6** *Volume and Surface Area* ([link](https://openstax.org/books/prealgebra-2e/pages/9-6-solve-geometry-applications-volume-and-surface-area)).

- Figure 9.29: 4×2×3 rectangular solid broken into layers → `V=LWH=24`.
- Surface area by summing faces (crate-painting story).
- Cube formulas `V=s^3`, `S=6s^2` (sibling leaf).

OpenStax uses **perspective rectangular solids**, not isometric unit-cube drawings. Isometric counting is **IM Grade 6 Unit 1**.

**UNCLEAR:** emulate IM isometric counts, or OpenStax labeled `L,W,H`? Old path is isometric (`Use the drawing to find the volume`). Gold for G6 is IM counting; OpenStax 9.6 is the formula sibling.

## Variety notes

**LOW_VARIETY:** two stems (`volume` vs `surface area`). D=0 always volume in this pack. No L-shaped buildings, no missing-cube figures.

## Limitations

- Flags: **UNCLEAR**, **LOW_VARIETY**.
- **LOW_VARIETY:** two stems (`volume` vs `surface area`). D=0 always volume in this pack. No L-shaped buildings, no missing-cube figures.

## Proposed engine (proposal only)

geometry isometric / unit-cube (`g6_isometric_measure`). Separate from symbolic cube formula leaf.

Generator (catalog): see `question_engine/catalogs/grade_6.py`.
