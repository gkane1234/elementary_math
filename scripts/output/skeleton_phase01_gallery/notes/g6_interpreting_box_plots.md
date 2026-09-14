# `g6_interpreting_box_plots` — Interpreting box plots

> RED HEADER: **LOW_VARIETY**
>
> Ship samples anyway. Implementation must not treat a green checkbox as success if the old stem is a stub or a single template.

Steps 1–3 only (old live samples, intended look, OpenStax). No engine implementation.

## What the question should look like (D=0 vs high D)

**D=0:** read **median** off a box plot (five-number summary visible).

**High D:** range, then Q1/Q3, then IQR. Student should **not** need a dumped data list (old interpreting-box latex is better than dot plots — no `Data:` in the stem).

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22, `include_answer_key=True`, seeds 101 and 202. Default path **is** the old path (these leaves are not on equation/poly skeletons). One sample per D below (seed 101).

| D | Prompt (latex) | Answer |
|--:|----------------|--------|
| 0 | `$\text{From the box plot, find the median.}$` | `$4$` |
| 8 | `$\text{From the box plot, find the median.}$` | `$15$` |
| 16 | `$\text{From the box plot, find the third quartile (Q3).}$` | `$32$` |
| 22 | `$\text{From the box plot, find the interquartile range.}$` | `$20$` |

Second seed (202) at D=0 and D=22:

- D=0: `$\text{From the box plot, find the median.}$` → `$7$`
- D=22: `$\text{From the box plot, find the third quartile (Q3).}$` → `$31$`

## OpenStax examples + chapter/section

**Introductory Statistics §2.4** *Box Plots* ([link](https://openstax.org/books/introductory-statistics/pages/2-4-box-plots)) — min, Q1, median, Q3, max; IQR = Q3−Q1.
Prealgebra 2e: none. IM Grade 6 Unit 8 box plots for comparing groups (we only ask one plot’s numbers).

## Variety notes

**LOW_VARIETY:** one sentence `From the box plot, find the ___`. The statistic rotates, which is the intended ramp. No compare-two-plots.

## Limitations

- Flags: **LOW_VARIETY**.
- **LOW_VARIETY:** one sentence `From the box plot, find the ___`. The statistic rotates, which is the intended ramp. No compare-two-plots.

## Proposed engine (proposal only)

stats (`stats_box_plot_basics`) interpret mode.

Generator (catalog): see `question_engine/catalogs/grade_6.py`.
