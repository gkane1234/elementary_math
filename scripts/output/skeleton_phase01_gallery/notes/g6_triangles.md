# `g6_triangles` — Triangles

> RED HEADER: **LOW_VARIETY**
>
> Ship samples anyway. Implementation must not treat a green checkbox as success if the old stem is a stub or a single template.

Steps 1–3 only (old live samples, intended look, OpenStax). No engine implementation.

## What the question should look like (D=0 vs high D)

**D=0:** right or acute triangle diagram; integer b,h; `A=½bh` whole-number area (even b or h).

**High D:** half-integers (`.5` in old samples), larger products. Still one triangle, not composite figures (shaded-region leaf).

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22, `include_answer_key=True`, seeds 101 and 202. Default path **is** the old path (these leaves are not on equation/poly skeletons). One sample per D below (seed 101).

| D | Prompt (latex) | Answer |
|--:|----------------|--------|
| 0 | `$\text{Find the area of } \triangle ABC.$` | `$9\text{ cm}^{2}$` |
| 8 | `$\text{Find the area of } \triangle ABC.$` | `$42\text{ cm}^{2}$` |
| 16 | `$\text{Find the area of } \triangle ABC.$` | `$82.5\text{ cm}^{2}$` |
| 22 | `$\text{Find the area of } \triangle ABC.$` | `$157.5\text{ cm}^{2}$` |

Second seed (202) at D=0 and D=22:

- D=0: `$\text{Find the area of } \triangle ABC.$` → `$20\text{ cm}^{2}$`
- D=22: `$\text{Find the area of } \triangle ABC.$` → `$199.5\text{ cm}^{2}$`

## OpenStax examples + chapter/section

**Prealgebra 2e §9.4** triangle area `A=½bh`. Example shape: given base and height on a sketched triangle, find area. Applications (sail, garden plot) exist in the exercise set — optional WP skin, not required for this compute leaf.

## Variety notes

**LOW_VARIETY:** stem always `Find the area of △ABC.` Numbers grow; some half-cm². No “height outside the triangle”, no non-right diagrams called out in latex.

## Limitations

- Flags: **LOW_VARIETY**.
- **LOW_VARIETY:** stem always `Find the area of △ABC.` Numbers grow; some half-cm². No “height outside the triangle”, no non-right diagrams called out in latex.

## Proposed engine (proposal only)

geometry_basic (`geo_triangle_area`).

Generator (catalog): see `question_engine/catalogs/grade_6.py`.
