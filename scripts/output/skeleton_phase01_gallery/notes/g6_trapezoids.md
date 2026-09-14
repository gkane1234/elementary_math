# `g6_trapezoids` — Trapezoids

> RED HEADER: **LOW_VARIETY**
>
> Ship samples anyway. Implementation must not treat a green checkbox as success if the old stem is a stub or a single template.

Steps 1–3 only (old live samples, intended look, OpenStax). No engine implementation.

## What the question should look like (D=0 vs high D)

**D=0:** one trapezoid; integer bases `b,B` and height `h`; `A=½h(b+B)` with a friendly even sum.

**High D:** larger integers then halves. Still one trapezoid, not irregular composites.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22, `include_answer_key=True`, seeds 101 and 202. Default path **is** the old path (these leaves are not on equation/poly skeletons). One sample per D below (seed 101).

| D | Prompt (latex) | Answer |
|--:|----------------|--------|
| 0 | `$\text{Find the area of the trapezoid.}$` | `$18\text{ cm}^2$` |
| 8 | `$\text{Find the area of the trapezoid.}$` | `$119\text{ cm}^2$` |
| 16 | `$\text{Find the area of the trapezoid.}$` | `$256.5\text{ cm}^2$` |
| 22 | `$\text{Find the area of the trapezoid.}$` | `$333.5\text{ cm}^2$` |

Second seed (202) at D=0 and D=22:

- D=0: `$\text{Find the area of the trapezoid.}$` → `$21\text{ cm}^2$`
- D=22: `$\text{Find the area of the trapezoid.}$` → `$122.5\text{ cm}^2$`

## OpenStax examples + chapter/section

**Prealgebra 2e §9.4** trapezoid: parallel bases `b` and `B`, height `h`, `A=½h(b+B)` (Figure 9.25). Exercises compute area from three lengths. Story apps (deck, garden) appear in the section exercises — optional later frames.

## Variety notes

**LOW_VARIETY:** `Find the area of the trapezoid.` only. Difficulty = bigger cm² (18 → 333.5 in this pack).

## Limitations

- Flags: **LOW_VARIETY**.
- **LOW_VARIETY:** `Find the area of the trapezoid.` only. Difficulty = bigger cm² (18 → 333.5 in this pack).

## Proposed engine (proposal only)

geometry_basic (`geo_trapezoid_area`).

Generator (catalog): see `question_engine/catalogs/grade_6.py`.
