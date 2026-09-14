# `g6_drawing_histograms` — Drawing histograms

> RED HEADER: **LOW_VARIETY**
>
> Ship samples anyway. Implementation must not treat a green checkbox as success if the old stem is a stub or a single template.

Steps 1–3 only (old live samples, intended look, OpenStax). No engine implementation.

## What the question should look like (D=0 vs high D)

**D=0:** tiny list, given axis, student draws bars for fixed bins.

**High D:** more data; student chooses/labels axis. Still construct, not read.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22, `include_answer_key=True`, seeds 101 and 202. Default path **is** the old path (these leaves are not on equation/poly skeletons). One sample per D below (seed 101).

| D | Prompt (latex) | Answer |
|--:|----------------|--------|
| 0 | `$\text{Create a histogram for the data set } \{3,\ 4,\ 1,\ 6,\ 5,\ 2\}. \text{Use the blank axis provided.}$` | `$\text{(see figure)}$` |
| 8 | `$\text{Create a histogram for the data set } \{8,\ 1,\ 9,\ 4,\ 10,\ 4,\ 5,\ 8\}. \text{Use the blank axis provided.}$` | `$\text{(see figure)}$` |
| 16 | `$\text{Create a histogram for the data set } \{11,\ 18,\ 10,\ 12,\ 18,\ 4,\ 11,\ 10,\ 9,\ 4,\ 18\}. \text{Draw and label your own axis.}$` | `$\text{(see figure)}$` |
| 22 | `$\text{Create a histogram for the data set } \{10,\ 15,\ 18,\ 7,\ 12,\ 10,\ 8,\ 7,\ 18,\ 19,\ 15,\ 10,\ 18,\ 15,\ 10\}. \text{Draw and label your own axis.}$` | `$\text{(see figure)}$` |

Second seed (202) at D=0 and D=22:

- D=0: `$\text{Create a histogram for the data set } \{4,\ 4,\ 2,\ 2,\ 6,\ 4\}. \text{Use the blank axis provided.}$` → `$\text{(see figure)}$`
- D=22: `$\text{Create a histogram for the data set } \{21,\ 2,\ 23,\ 16,\ 13,\ 13,\ 21,\ 23,\ 13,\ 20,\ 16,\ 21,\ 8,\ 20,\ 21,\ 2\}. \text{Draw and label your own axis.}$` → `$\text{(see figure)}$`

## OpenStax examples + chapter/section

**Intro Stats §2.2** “Create a histogram for the following data” (shoe sizes, books bought). That is the OpenStax shape. G6 should use fewer values and friendlier bins than college stats.

## Variety notes

**LOW_VARIETY:** same stem as drawing dot plots with “histogram” swapped. No given bin-width instruction in latex (OpenStax specifies interval, e.g. 10–19 first).

## Limitations

- Flags: **LOW_VARIETY**.
- **LOW_VARIETY:** same stem as drawing dot plots with “histogram” swapped. No given bin-width instruction in latex (OpenStax specifies interval, e.g. 10–19 first).

## Proposed engine (proposal only)

stats draw (`g6_drawing_histogram`).

Generator (catalog): see `question_engine/catalogs/grade_6.py`.
