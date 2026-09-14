# `g6_right_rectangular_prisms_with_fraction_side_lengths` — Right rectangular prisms with fraction side lengths


Steps 1–3 only (old live samples, intended look, OpenStax). No engine implementation.

## What the question should look like (D=0 vs high D)

**D=0:** `V=ℓwh` with two whole numbers and one unit fraction (old: `2, 1/2, 1` → 1 cm³).

**High D:** three fractions, unlike denoms. Cube-of-fractions is fine; do not jump to cylinders.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22, `include_answer_key=True`, seeds 101 and 202. Default path **is** the old path (these leaves are not on equation/poly skeletons). One sample per D below (seed 101).

| D | Prompt (latex) | Answer |
|--:|----------------|--------|
| 0 | `$\text{Find the volume of the right rectangular prism with side lengths } 2\text{ cm},\ \frac{1}{2}\text{ cm},\ 1\text{ cm}.$` | `$1\text{ cm}^{3}$` |
| 8 | `$\text{Find the volume of the right rectangular prism with side lengths } \frac{3}{2}\text{ cm},\ 3\text{ cm},\ \frac{4}{3}\text{ cm}.$` | `$6\text{ cm}^{3}$` |
| 16 | `$\text{Find the volume of the right rectangular prism with side lengths } \frac{3}{2}\text{ cm},\ \frac{17}{10}\text{ cm},\ \frac{4}{5}\text{ cm}.$` | `$\frac{51}{25}\text{ cm}^{3}$` |
| 22 | `$\text{Find the volume of the right rectangular prism with side lengths } \frac{11}{6}\text{ cm},\ \frac{5}{2}\text{ cm},\ \frac{7}{6}\text{ cm}.$` | `$\frac{385}{72}\text{ cm}^{3}$` |

Second seed (202) at D=0 and D=22:

- D=0: `$\text{Find the volume of the right rectangular prism with side lengths } 1\text{ in},\ 2\text{ in},\ \frac{1}{2}\text{ in}.$` → `$1\text{ in}^{3}$`
- D=22: `$\text{Find the volume of the right rectangular prism with side lengths } \frac{5}{2}\text{ in},\ \frac{1}{4}\text{ in},\ \frac{17}{10}\text{ in}.$` → `$\frac{17}{16}\text{ in}^{3}$`

## OpenStax examples + chapter/section

**Prealgebra 2e §9.6** `V=LWH` with whole numbers, combined with **§4.2** fraction products. IM G6 Unit 4 packing cubes with fraction edges is the pedagogical picture; old path is already the formula version.

## Variety notes

Numeric ramp is real. Stem always lists three side lengths. OK.

## Limitations

- Numeric ramp is real. Stem always lists three side lengths. OK.

## Proposed engine (proposal only)

geometry prism volume + fractions (`g6_fraction_prism_volume`).

Generator (catalog): see `question_engine/catalogs/grade_6.py`.
