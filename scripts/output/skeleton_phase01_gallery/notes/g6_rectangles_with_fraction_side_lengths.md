# `g6_rectangles_with_fraction_side_lengths` — Rectangles with fraction side lengths


Steps 1–3 only (old live samples, intended look, OpenStax). No engine implementation.

## What the question should look like (D=0 vs high D)

**D=0:** one side unit fraction (`1/2` or `1/3`), other side a small whole; `A=ℓw`.

**High D:** both sides proper/improper fractions, unlike denominators. Still a rectangle (OpenStax 9.4 × fraction ops from ch. 4).

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22, `include_answer_key=True`, seeds 101 and 202. Default path **is** the old path (these leaves are not on equation/poly skeletons). One sample per D below (seed 101).

| D | Prompt (latex) | Answer |
|--:|----------------|--------|
| 0 | `$\text{Find the area of the rectangle with base } \frac{1}{2}\text{ cm} \text{ and height } 1\text{ cm}.$` | `$\frac{1}{2}\text{ cm}^{2}$` |
| 8 | `$\text{Find the area of the rectangle with base } 1\text{ cm} \text{ and height } \frac{1}{5}\text{ cm}.$` | `$\frac{1}{5}\text{ cm}^{2}$` |
| 16 | `$\text{Find the area of the rectangle with base } \frac{11}{8}\text{ cm} \text{ and height } \frac{4}{3}\text{ cm}.$` | `$\frac{11}{6}\text{ cm}^{2}$` |
| 22 | `$\text{Find the area of the rectangle with base } \frac{6}{5}\text{ cm} \text{ and height } \frac{19}{8}\text{ cm}.$` | `$\frac{57}{20}\text{ cm}^{2}$` |

Second seed (202) at D=0 and D=22:

- D=0: `$\text{Find the area of the rectangle with base } \frac{1}{3}\text{ in} \text{ and height } 2\text{ in}.$` → `$\frac{2}{3}\text{ in}^{2}$`
- D=22: `$\text{Find the area of the rectangle with base } \frac{23}{9}\text{ in} \text{ and height } \frac{27}{10}\text{ in}.$` → `$\frac{69}{10}\text{ in}^{2}$`

## OpenStax examples + chapter/section

**Prealgebra 2e §9.4** rectangle `A=LW` plus **§4.2** multiply fractions. Classroom G6 (IM Unit 4 / Unit 1) multiplies mixed/fraction side lengths. Example shape: ½ in by 1 in → ½ in² (matches old D=0).

## Variety notes

Honest numeric ramp (unit fraction → two fractions). Stem is one template but the math changes. Not flagged LOW_VARIETY.

## Limitations

- Flags: **LOW_VARIETY**.
- Honest numeric ramp (unit fraction → two fractions). Stem is one template but the math changes. Not flagged LOW_VARIETY.

## Proposed engine (proposal only)

geometry rectangle + numbers/fractions primitive. Existing `g6_fraction_rectangle_area`.

Generator (catalog): see `question_engine/catalogs/grade_6.py`.
