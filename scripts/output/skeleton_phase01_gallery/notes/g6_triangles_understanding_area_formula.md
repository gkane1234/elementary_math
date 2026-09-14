# `g6_triangles_understanding_area_formula` — Triangles, understanding area formula

> RED HEADER: **UNCLEAR**
>
> Ship samples anyway. Implementation must not treat a green checkbox as success if the old stem is a stub or a single template.

Steps 1–3 only (old live samples, intended look, OpenStax). No engine implementation.

## What the question should look like (D=0 vs high D)

**D=0 (intended):** two congruent triangles make a rectangle, so `A=½bh`. Tiny b,h.

**Old path:** mix of `Find the area of △ABC` and “A triangle has area 20 cm² and height 8 cm. Find the base.” The missing-side items *are* the formula-understanding ramp.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22, `include_answer_key=True`, seeds 101 and 202. Default path **is** the old path (these leaves are not on equation/poly skeletons). One sample per D below (seed 101).

| D | Prompt (latex) | Answer |
|--:|----------------|--------|
| 0 | `$\text{Find the area of } \triangle ABC.$` | `$9\text{ cm}^{2}$` |
| 8 | `$\text{Find the area of } \triangle ABC.$` | `$42\text{ cm}^{2}$` |
| 16 | `$\text{Find the area of } \triangle ABC.$` | `$82.5\text{ cm}^{2}$` |
| 22 | `$\text{A triangle has area } 157.5\text{ cm}^2\text{ and height } 21\text{ cm. Find the base.}$` | `$15\text{ cm}$` |

Second seed (202) at D=0 and D=22:

- D=0: `$\text{A triangle has area } 20\text{ cm}^2\text{ and height } 8\text{ cm. Find the base.}$` → `$5\text{ cm}$`
- D=22: `$\text{A triangle has area } 199.5\text{ cm}^2\text{ and base } 21\text{ cm. Find the height.}$` → `$19\text{ cm}$`

## OpenStax examples + chapter/section

**OpenStax Prealgebra 2e §9.4** *Use Properties of Rectangles, Triangles, and Trapezoids* ([link](https://openstax.org/books/prealgebra-2e/pages/9-4-use-properties-of-rectangles-triangles-and-trapezoids)).

- Figure 9.22: rectangle split into two congruent triangles → `A=½bh`.
- Exercises: find triangle area given b,h; also perimeter of triangles (not this leaf).
- Missing-side (`A` and `h` → `b`) is the same algebra as §9.7 “solve a formula”, but IM G6 Unit 1 does this without calling it literal equations.

## Variety notes

**UNCLEAR:** overlaps `g6_triangles`. Old D=0 already mixes compute-area and missing-side. If we keep two leaves, this one should prefer missing-side + “which is the height?” and the sibling should stay compute-from-diagram.

## Limitations

- Flags: **UNCLEAR**.
- **UNCLEAR:** overlaps `g6_triangles`. Old D=0 already mixes compute-area and missing-side. If we keep two leaves, this one should prefer missing-side + “which is the height?” and the sibling should stay compute-from-diagram.

## Proposed engine (proposal only)

geometry_basic triangle. Mode: missing base or height. Reuse diagram family.

Generator (catalog): see `question_engine/catalogs/grade_6.py`.
