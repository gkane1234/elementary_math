# `g6_drawing_box_plots` — Drawing box plots

> RED HEADER: **UNCLEAR** · **LOW_VARIETY**
>
> Ship samples anyway. Implementation must not treat a green checkbox as success if the old stem is a stub or a single template.

Steps 1–3 only (old live samples, intended look, OpenStax). No engine implementation.

## What the question should look like (D=0 vs high D)

**D=0 (intended):** given a short list, student draws a box plot (compute five-number summary, then sketch).

**Old path:** **identical** to `g6_interpreting_box_plots` (same generator `stats_box_plot_basics`). Prompts are “From the box plot, find the median.” This is a miswire, not a drawing skill.

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

**Intro Stats §2.4** includes constructing a box plot from a data set (find five-number summary, draw). That is what this leaf **should** be.

**UNCLEAR:** catalog name vs live output. Do not implement “drawing” as interpret-again.

## Variety notes

**LOW_VARIETY / duplicate:** 8/8 samples match the interpret leaf exactly (same answers for the same seeds).

## Limitations

- Flags: **UNCLEAR**, **LOW_VARIETY**.
- **LOW_VARIETY / duplicate:** 8/8 samples match the interpret leaf exactly (same answers for the same seeds).
- Possible miswire / off-skill emission at some D.

## Proposed engine (proposal only)

stats box-plot **construct** mode (list → five-number → figure). New mode on existing stats engine; do not alias to interpret.

Generator (catalog): see `question_engine/catalogs/grade_6.py`.
