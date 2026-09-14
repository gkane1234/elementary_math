# `g6_parallelograms_understanding_area_formula` — Parallelograms, understanding area formula

> RED HEADER: **UNCLEAR** · **LOW_VARIETY**
>
> Ship samples anyway. Implementation must not treat a green checkbox as success if the old stem is a stub or a single template.

Steps 1–3 only (old live samples, intended look, OpenStax). No engine implementation.

## What the question should look like (D=0 vs high D)

**D=0 (intended):** show why `A=bh` (cut-and-rearrange to a rectangle). Tiny integer base/height; maybe “which length is the height?”

**What old actually does:** same as `g6_parallelograms` at D=0 (`Find the area`), then sometimes “given A and b, find h”. That is formula use, not “understanding”.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22, `include_answer_key=True`, seeds 101 and 202. Default path **is** the old path (these leaves are not on equation/poly skeletons). One sample per D below (seed 101).

| D | Prompt (latex) | Answer |
|--:|----------------|--------|
| 0 | `$\text{Find the area of the parallelogram.}$` | `$18\text{ cm}^2$` |
| 8 | `$\text{Find the area of the parallelogram.}$` | `$84\text{ cm}^2$` |
| 16 | `$\text{Find the area of the parallelogram.}$` | `$165\text{ cm}^2$` |
| 22 | `$\text{A parallelogram has area } 315\text{ cm}^2\text{ and base } 15\text{ cm. Find the height.}$` | `$21\text{ cm}$` |

Second seed (202) at D=0 and D=22:

- D=0: `$\text{Find the area of the parallelogram.}$` → `$40\text{ cm}^2$`
- D=22: `$\text{A parallelogram has area } 399\text{ cm}^2\text{ and base } 21\text{ cm. Find the height.}$` → `$19\text{ cm}$`

## OpenStax examples + chapter/section

OpenStax **Prealgebra 2e §9.4** develops **triangle** area as half a rectangle (`A=½bh`) but **does not treat parallelograms**. G6 gold: **IM Grade 6 Unit 1** Lessons on decomposing parallelograms.

**UNCLEAR:** catalog name ≠ old generator. Sibling `g6_parallelograms` is the compute-area leaf. This one should stay “why bh” / missing-dimension, or we collapse the two leaves.

## Variety notes

**LOW_VARIETY:** mix of identical “find the area” stems and missing-side. No “draw the height”, no “base vs slanted side” distractor.

## Limitations

- Flags: **UNCLEAR**, **LOW_VARIETY**.
- **LOW_VARIETY:** mix of identical “find the area” stems and missing-side. No “draw the height”, no “base vs slanted side” distractor.

## Proposed engine (proposal only)

geometry_basic parallelogram. Distinct mode: missing side + (later) identify base/height on a diagram. Do not pad difficulty with bigger cm² only.

Generator (catalog): see `question_engine/catalogs/grade_6.py`.
