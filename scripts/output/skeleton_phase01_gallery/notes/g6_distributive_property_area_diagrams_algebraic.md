# `g6_distributive_property_area_diagrams_algebraic` — Distributive property with area diagrams, algebraic

> RED HEADER: **LOW_VARIETY**
>
> Ship samples anyway. Implementation must not treat a green checkbox as success if the old stem is a stub or a single template.

Steps 1–3 only (old live samples, intended look, OpenStax). No engine implementation.

## What the question should look like (D=0 vs high D)

**D=0:** area-model for `a(x+b)` with small positive `a,b` (OpenStax 7.17 style `3(x+4)`). Student fills/reads a rectangle split into `ax` and `ab`.

**High D:** still one-factor distribute. Unlock `a(x-b)`, then negative `a`, not a second binomial or FOIL. Diagram stays a 1×2 (or 2×1) area model.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22, `include_answer_key=True`, seeds 101 and 202. Default path **is** the old path (these leaves are not on equation/poly skeletons). One sample per D below (seed 101).

| D | Prompt (latex) | Answer |
|--:|----------------|--------|
| 0 | `$\text{Use the area model to expand } 4(x + 3).$` | `$4x + 12$` |
| 8 | `$\text{Use the area model to expand } 6(x + 7).$` | `$6x + 42$` |
| 16 | `$\text{Use the area model to expand } 12(x - 8).$` | `$12x - 96$` |
| 22 | `$\text{Use the area model to expand } 13(x - 11).$` | `$13x - 143$` |

Second seed (202) at D=0 and D=22:

- D=0: `$\text{Use the area model to expand } 4(x + 4).$` → `$4x + 16$`
- D=22: `$\text{Use the area model to expand } -15(x - 17).$` → `$-15x + 255$`

## OpenStax examples + chapter/section

**OpenStax Prealgebra 2e §7.3** *Distributive Property* ([link](https://openstax.org/books/prealgebra-2e/pages/7-3-distributive-property)).

- Example 7.17: simplify `3(x+4)` → `3x+12` (also Try It `4(x+2)`, `6(x+7)`).
- Other forms in the same section: `2(x-3)`, `−2(4y+1)`, `(x+8)p`, fraction factor `3/4(n+12)`, and “model distribution” (area picture).
- OpenStax **does** treat area as a teaching picture; it also has many **non-area** algebraic forms. This leaf should keep the area model; `g6_distributive_property_algebraic` owns the non-diagram forms.

## Variety notes

**LOW_VARIETY:** every old sample is `Use the area model to expand a(x±b)`. Only coefficients grow (then a sign flip). OpenStax 7.3 has factor-on-the-right, variable factor, and fraction factor — those should **not** all dump onto this diagram leaf, but two-term `a(x±b)` with ± and later negative `a` is the honest ramp.

## Limitations

- Flags: **LOW_VARIETY**.
- **LOW_VARIETY:** every old sample is `Use the area model to expand a(x±b)`. Only coefficients grow (then a sign flip). OpenStax 7.3 has factor-on-the-right, variable factor, and fraction factor — those should **not** all dump onto this diagram leaf, but two-term `a(x±b)` with ± and later negative `a` is the honest ramp.

## Proposed engine (proposal only)

Reuse AffineInflate / distributive algebraic + area-model diagram. Same core as `g6_distributive_property_algebraic`, presentation = area diagram.

Generator (catalog): see `question_engine/catalogs/grade_6.py`.
