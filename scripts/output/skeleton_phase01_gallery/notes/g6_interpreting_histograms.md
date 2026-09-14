# `g6_interpreting_histograms` — Interpreting histograms

> RED HEADER: **UNCLEAR**
>
> Ship samples anyway. Implementation must not treat a green checkbox as success if the old stem is a stub or a single template.

Steps 1–3 only (old live samples, intended look, OpenStax). No engine implementation.

## What the question should look like (D=0 vs high D)

**D=0:** 4–6 values; “how many in `[6,8)`?” from the **bars**, not by scanning a dumped list.

**High D:** modal class; compare two bins. Bin width stays friendly (5s). Not relative frequency percents (Intro Stats does that; G6 IM usually stays counts).

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22, `include_answer_key=True`, seeds 101 and 202. Default path **is** the old path (these leaves are not on equation/poly skeletons). One sample per D below (seed 101).

| D | Prompt (latex) | Answer |
|--:|----------------|--------|
| 0 | `$\text{How many values fall in the interval } [6,\ 8)\text{?}\\\text{Data: } \{4,\ 6,\ 8,\ 1,\ 4,\ 4\}$` | `$2$` |
| 8 | `$\text{How many values fall in the interval } [12,\ 16)\text{?}\\\text{Data: } \{7,\ 18,\ 12,\ 15,\ 2,\ 22,\ 17,\ 7,\ 20\}$` | `$2$` |
| 16 | `$\text{How many more values fall in } [0,\ 5)\text{ than in } [15,\ 20)\text{?}\\\text{Data: } \{35,\ 23,\ 30,\ 4,\ 33,\ 14,\ 15,\ 19,\ 32,\ 14,\ 22\}$` | `$1$` |
| 22 | `$\text{How many more values fall in } [35,\ 40)\text{ than in } [20,\ 25)\text{?}\\\text{Data: } \{35,\ 23,\ 30,\ 4,\ 43,\ 33,\ 14,\ 39,\ 15,\ 19,\ 32,\ 45\}$` | `$1$` |

Second seed (202) at D=0 and D=22:

- D=0: `$\text{How many values fall in the interval } [4,\ 6)\text{?}\\\text{Data: } \{8,\ 7,\ 4,\ 4,\ 7\}$` → `$2$`
- D=22: `$\text{Which interval contains the most values?}\\\text{Data: } \{13,\ 31,\ 13,\ 13,\ 13,\ 31,\ 44,\ 13,\ 27,\ 27,\ 13,\ 44,\ 44,\ 27\}$` → `$[10, 15)$`

## OpenStax examples + chapter/section

**Introductory Statistics §2.2** *Histograms, Frequency Polygons, and Time Series Graphs* ([link](https://openstax.org/books/introductory-statistics/pages/2-2-histograms-frequency-polygons-and-time-series-graphs)).

- Example: count frequencies in class intervals; left-closed / right-open note.
- G6 IM Unit 8 histograms are smaller-n classroom versions.
- Prealgebra 2e does **not** have histograms.

**UNCLEAR:** old stem dumps `Data: {…}` so interval counts can be done without the histogram.

## Variety notes

Asks rotate (one bin count → compare bins → modal interval). Good if the figure is required.

## Limitations

- Flags: **UNCLEAR**.
- Asks rotate (one bin count → compare bins → modal interval). Good if the figure is required.

## Proposed engine (proposal only)

stats (`stats_histogram_read`). Do not print the raw list in prompt_latex.

Generator (catalog): see `question_engine/catalogs/grade_6.py`.
