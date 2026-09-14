# `g6_interpreting_dot_plots` — Interpreting dot plots

> RED HEADER: **UNCLEAR**
>
> Ship samples anyway. Implementation must not treat a green checkbox as success if the old stem is a stub or a single template.

Steps 1–3 only (old live samples, intended look, OpenStax). No engine implementation.

## What the question should look like (D=0 vs high D)

**D=0:** small data set; read “how many dots at 4?” from a **plot**, not from a dumped list.

**High D:** mode / “how many more at a than b”; **not** mean of 12 values (that is `g6_data_center_and_spread`). IM Unit 8: shape, center, typical value from the display.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22, `include_answer_key=True`, seeds 101 and 202. Default path **is** the old path (these leaves are not on equation/poly skeletons). One sample per D below (seed 101).

| D | Prompt (latex) | Answer |
|--:|----------------|--------|
| 0 | `$\text{The dot plot shows the data set below. How many dots are at } 6\text{?}\\\text{Data: } \{4,\ 6,\ 8,\ 1,\ 4,\ 4\}$` | `$1$` |
| 8 | `$\text{The dot plot shows the data set below. How many dots are at } 17\text{?}\\\text{Data: } \{7,\ 18,\ 12,\ 15,\ 2,\ 22,\ 17,\ 7,\ 20\}$` | `$1$` |
| 16 | `$\text{The dot plot shows the data set below. How many dots are there in all?}\\\text{Data: } \{35,\ 23,\ 30,\ 4,\ 33,\ 14,\ 15,\ 19,\ 32,\ 14,\ 22\}$` | `$11$` |
| 22 | `$\text{The dot plot shows the data set below. What is the mean?}\\\text{Data: } \{35,\ 23,\ 30,\ 4,\ 43,\ 33,\ 14,\ 39,\ 15,\ 19,\ 32,\ 45\}$` | `$27.67$` |

Second seed (202) at D=0 and D=22:

- D=0: `$\text{The dot plot shows the data set below. How many dots are at } 4\text{?}\\\text{Data: } \{8,\ 7,\ 4,\ 4,\ 7\}$` → `$2$`
- D=22: `$\text{The dot plot shows the data set below. How many more dots are at } 31\text{ than at } 27\text{?}\\\text{Data: } \{13,\ 31,\ 13,\ 13,\ 13,\ 31,\ 44,\ 13,\ 27,\ 27,\ 13,\ 44,\ 44,\ 27\}$` → `$1$`

## OpenStax examples + chapter/section

OpenStax **Prealgebra 2e has no dot plots** (ch. 5.5 is mean/probability). **Introductory Statistics §2.1** stem-and-leaf / line / bar graphs ([link](https://openstax.org/books/introductory-statistics/pages/2-1-stem-and-leaf-graphs-line-graphs-and-bar-graphs)).

G6 gold: **IM Grade 6 Unit 8** Statistical Questions / dot plots.

**UNCLEAR:** old prompt dumps `Data: {…}` so the student can ignore the figure. OpenStax/IM interpret **from the display**. Also D=16 seed 202 asked “what value has the most dots?” and answered `27` on a list where 13 and 29 also appear twice — mode is ambiguous (topic-fit / key worry).

## Variety notes

Asks do rotate (count at a value, total, mode, mean). Mean-from-dot-plot at D=22 may change topic toward center/spread. Prefer stay-on-plot reading.

## Limitations

- Flags: **UNCLEAR**.
- Asks do rotate (count at a value, total, mode, mean). Mean-from-dot-plot at D=22 may change topic toward center/spread. Prefer stay-on-plot reading.
- Weak / missing OpenStax chapter match for this leaf.

## Proposed engine (proposal only)

stats / other (`stats_dot_plot_read`). Hide the raw list in the student stem; keep it in metadata.

Generator (catalog): see `question_engine/catalogs/grade_6.py`.
