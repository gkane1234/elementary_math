# `g6_data_center_and_spread` — Center and spread


Steps 1–3 only (old live samples, intended look, OpenStax). No engine implementation.

## What the question should look like (D=0 vs high D)

**D=0:** 4–6 small integers; **range** or **mode** (old D=0 was range/mode).

**High D:** median (even n → half), then mean. Stay one measure per item. Do not jump to MAD/standard deviation (not G6 catalog).

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22, `include_answer_key=True`, seeds 101 and 202. Default path **is** the old path (these leaves are not on equation/poly skeletons). One sample per D below (seed 101).

| D | Prompt (latex) | Answer |
|--:|----------------|--------|
| 0 | `$\text{Find the range of the data set: } \{4,\ 6,\ 8,\ 1,\ 4,\ 4\}.$` | `$7$` |
| 8 | `$\text{Find the median of the data set: } \{7,\ 18,\ 12,\ 15,\ 2,\ 22,\ 17,\ 7,\ 20\}.$` | `$15$` |
| 16 | `$\text{Find the mean of the data set: } \{35,\ 23,\ 30,\ 4,\ 33,\ 14,\ 15,\ 19,\ 32,\ 14,\ 22\}.$` | `$21.91$` |
| 22 | `$\text{Find the mean of the data set: } \{35,\ 23,\ 30,\ 4,\ 43,\ 33,\ 14,\ 39,\ 15,\ 19,\ 32,\ 45\}.$` | `$27.67$` |

Second seed (202) at D=0 and D=22:

- D=0: `$\text{Find the range of the data set: } \{8,\ 7,\ 4,\ 4,\ 7\}.$` → `$4$`
- D=22: `$\text{Find the median of the data set: } \{13,\ 31,\ 13,\ 13,\ 13,\ 31,\ 44,\ 13,\ 27,\ 27,\ 13,\ 44,\ 44,\ 27\}.$` → `$27$`

## OpenStax examples + chapter/section

**Prealgebra 2e §5.5** *Averages and Probability* — mean of a short list ([link](https://openstax.org/books/prealgebra-2e/pages/5-5-averages-and-probability)).
**Introductory Statistics §2.5–2.7** mean / median / mode / range / IQR.
G6 IM Unit 8: mean, median, MAD (we do not have MAD on this leaf).

Old path matches OpenStax 5.5 + Stats 2.5 more than IM MAD.

## Variety notes

Measure rotates (range → median → mean). That is real. No story context (quiz scores, plant heights) — optional OpenStax frames later.

## Limitations

- Measure rotates (range → median → mean). That is real. No story context (quiz scores, plant heights) — optional OpenStax frames later.

## Proposed engine (proposal only)

stats (`stats_center_spread`). Number-list engine, not geometry.

Generator (catalog): see `question_engine/catalogs/grade_6.py`.
