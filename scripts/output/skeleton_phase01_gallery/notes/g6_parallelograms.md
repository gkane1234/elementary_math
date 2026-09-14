# `g6_parallelograms` — Parallelograms

> RED HEADER: **LOW_VARIETY**
>
> Ship samples anyway. Implementation must not treat a green checkbox as success if the old stem is a stub or a single template.

Steps 1–3 only (old live samples, intended look, OpenStax). No engine implementation.

## What the question should look like (D=0 vs high D)

**D=0:** diagram of a parallelogram; labeled integer base and height; `A=bh`; small product (e.g. 6×3=18).

**High D:** larger integers, then one decimal/half; still `bh` with height perpendicular (not the slanted side as a trap unless OpenStax/IM has it — IM does).

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22, `include_answer_key=True`, seeds 101 and 202. Default path **is** the old path (these leaves are not on equation/poly skeletons). One sample per D below (seed 101).

| D | Prompt (latex) | Answer |
|--:|----------------|--------|
| 0 | `$\text{Find the area of the parallelogram.}$` | `$18\text{ cm}^2$` |
| 8 | `$\text{Find the area of the parallelogram.}$` | `$84\text{ cm}^2$` |
| 16 | `$\text{Find the area of the parallelogram.}$` | `$165\text{ cm}^2$` |
| 22 | `$\text{Find the area of the parallelogram.}$` | `$315\text{ cm}^2$` |

Second seed (202) at D=0 and D=22:

- D=0: `$\text{Find the area of the parallelogram.}$` → `$40\text{ cm}^2$`
- D=22: `$\text{Find the area of the parallelogram.}$` → `$399\text{ cm}^2$`

## OpenStax examples + chapter/section

No parallelogram section in OpenStax Prealgebra. Closest formulas: **§9.4** rectangles `A=LW` (same multiplication). G6: **IM Grade 6 Unit 1** parallelogram area.

Do not pull trapezoid/kite work onto this leaf.

## Variety notes

**LOW_VARIETY:** every stem is `Find the area of the parallelogram.` Difficulty = bigger product. Diagram SVG is the only non-text variety.

## Limitations

- Flags: **LOW_VARIETY**.
- **LOW_VARIETY:** every stem is `Find the area of the parallelogram.` Difficulty = bigger product. Diagram SVG is the only non-text variety.

## Proposed engine (proposal only)

geometry_basic (`geo_parallelogram_area`). Keep diagram. Numeric hardness before asking for missing side (that’s the understanding leaf).

Generator (catalog): see `question_engine/catalogs/grade_6.py`.
