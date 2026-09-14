# `g6_kites` — Kites

> RED HEADER: **UNCLEAR** · **LOW_VARIETY**
>
> Ship samples anyway. Implementation must not treat a green checkbox as success if the old stem is a stub or a single template.

Steps 1–3 only (old live samples, intended look, OpenStax). No engine implementation.

## What the question should look like (D=0 vs high D)

**D=0:** kite diagram; integer diagonals `d1,d2`; `A=½ d1 d2`; small product.

**High D:** larger diagonals / halves. Same formula.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22, `include_answer_key=True`, seeds 101 and 202. Default path **is** the old path (these leaves are not on equation/poly skeletons). One sample per D below (seed 101).

| D | Prompt (latex) | Answer |
|--:|----------------|--------|
| 0 | `$\text{Find the area of the kite.}$` | `$9\text{ cm}^2$` |
| 8 | `$\text{Find the area of the kite.}$` | `$42\text{ cm}^2$` |
| 16 | `$\text{Find the area of the kite.}$` | `$82.5\text{ cm}^2$` |
| 22 | `$\text{Find the area of the kite.}$` | `$157.5\text{ cm}^2$` |

Second seed (202) at D=0 and D=22:

- D=0: `$\text{Find the area of the kite.}$` → `$20\text{ cm}^2$`
- D=22: `$\text{Find the area of the kite.}$` → `$199.5\text{ cm}^2$`

## OpenStax examples + chapter/section

**OpenStax Prealgebra does not teach kite area.** §9.4 is rectangle / triangle / trapezoid. Kite `A=½d_1 d_2` is typical **IM Grade 6 Unit 1** / some middle-school geometry, not OpenStax PA.

**UNCLEAR:** keep as IM-shaped G6, or skip until we have a textbook example we want to copy. Do not pretend it is OpenStax 9.4.

## Variety notes

**LOW_VARIETY:** `Find the area of the kite.` at every D. Answers in this pack match the triangle-area sequence (9, 20, 42, …) — likely the same `½bh` sampler with a kite SVG.

## Limitations

- Flags: **UNCLEAR**, **LOW_VARIETY**.
- **LOW_VARIETY:** `Find the area of the kite.` at every D. Answers in this pack match the triangle-area sequence (9, 20, 42, …) — likely the same `½bh` sampler with a kite SVG.
- Weak / missing OpenStax chapter match for this leaf.

## Proposed engine (proposal only)

geometry_basic kite diagonals. If we cannot distinguish from triangle honestly, leave leaf / document skip.

Generator (catalog): see `question_engine/catalogs/grade_6.py`.
