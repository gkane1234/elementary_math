# `g6_triangles_with_fraction_side_lengths` — Triangles with fraction side lengths


Steps 1–3 only (old live samples, intended look, OpenStax). No engine implementation.

## What the question should look like (D=0 vs high D)

**D=0:** right triangle; one of b,h a unit fraction; `A=½bh`.

**High D:** both b and h fractions. Stay right-triangle / labeled height. Same ramp as the rectangle sibling with the extra ½.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22, `include_answer_key=True`, seeds 101 and 202. Default path **is** the old path (these leaves are not on equation/poly skeletons). One sample per D below (seed 101).

| D | Prompt (latex) | Answer |
|--:|----------------|--------|
| 0 | `$\text{Find the area of the right triangle with base } \frac{1}{2}\text{ cm} \text{ and height } 1\text{ cm}.$` | `$\frac{1}{4}\text{ cm}^{2}$` |
| 8 | `$\text{Find the area of the right triangle with base } 1\text{ cm} \text{ and height } \frac{1}{5}\text{ cm}.$` | `$\frac{1}{10}\text{ cm}^{2}$` |
| 16 | `$\text{Find the area of the right triangle with base } \frac{11}{8}\text{ cm} \text{ and height } \frac{4}{3}\text{ cm}.$` | `$\frac{11}{12}\text{ cm}^{2}$` |
| 22 | `$\text{Find the area of the right triangle with base } \frac{6}{5}\text{ cm} \text{ and height } \frac{19}{8}\text{ cm}.$` | `$\frac{57}{40}\text{ cm}^{2}$` |

Second seed (202) at D=0 and D=22:

- D=0: `$\text{Find the area of the right triangle with base } \frac{1}{3}\text{ in} \text{ and height } 2\text{ in}.$` → `$\frac{1}{3}\text{ in}^{2}$`
- D=22: `$\text{Find the area of the right triangle with base } \frac{23}{9}\text{ in} \text{ and height } \frac{27}{10}\text{ in}.$` → `$\frac{69}{20}\text{ in}^{2}$`

## OpenStax examples + chapter/section

**§9.4** `A=½bh` + **§4.2** fraction multiplication. No dedicated OpenStax “fraction-side triangle” set; the combination is standard G6.

## Variety notes

Same as rectangle-fraction: one stem, real fraction hardness. OK.

## Limitations

- Same as rectangle-fraction: one stem, real fraction hardness. OK.

## Proposed engine (proposal only)

geometry triangle + fractions (`g6_fraction_triangle_area`).

Generator (catalog): see `question_engine/catalogs/grade_6.py`.
