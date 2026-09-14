# `g6_drawing_dot_plots` — Drawing dot plots

> RED HEADER: **LOW_VARIETY**
>
> Ship samples anyway. Implementation must not treat a green checkbox as success if the old stem is a stub or a single template.

Steps 1–3 only (old live samples, intended look, OpenStax). No engine implementation.

## What the question should look like (D=0 vs high D)

**D=0:** 4–6 small integers; “use the blank axis provided.”

**High D:** longer lists; “draw and label your own axis.” Still *construct a dot plot*, not interpret.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22, `include_answer_key=True`, seeds 101 and 202. Default path **is** the old path (these leaves are not on equation/poly skeletons). One sample per D below (seed 101).

| D | Prompt (latex) | Answer |
|--:|----------------|--------|
| 0 | `$\text{Create a dot plot for the data set } \{3,\ 4,\ 1,\ 6,\ 5,\ 2\}. \text{Use the blank axis provided.}$` | `$\text{(see figure)}$` |
| 8 | `$\text{Create a dot plot for the data set } \{8,\ 1,\ 9,\ 4,\ 10,\ 4,\ 5,\ 8\}. \text{Use the blank axis provided.}$` | `$\text{(see figure)}$` |
| 16 | `$\text{Create a dot plot for the data set } \{11,\ 18,\ 10,\ 12,\ 18,\ 4,\ 11,\ 10,\ 9,\ 4,\ 18\}. \text{Draw and label your own axis.}$` | `$\text{(see figure)}$` |
| 22 | `$\text{Create a dot plot for the data set } \{10,\ 15,\ 18,\ 7,\ 12,\ 10,\ 8,\ 7,\ 18,\ 19,\ 15,\ 10,\ 18,\ 15,\ 10\}. \text{Draw and label your own axis.}$` | `$\text{(see figure)}$` |

Second seed (202) at D=0 and D=22:

- D=0: `$\text{Create a dot plot for the data set } \{4,\ 4,\ 2,\ 2,\ 6,\ 4\}. \text{Use the blank axis provided.}$` → `$\text{(see figure)}$`
- D=22: `$\text{Create a dot plot for the data set } \{21,\ 2,\ 23,\ 16,\ 13,\ 13,\ 21,\ 23,\ 13,\ 20,\ 16,\ 21,\ 8,\ 20,\ 21,\ 2\}. \text{Draw and label your own axis.}$` → `$\text{(see figure)}$`

## OpenStax examples + chapter/section

No OpenStax Prealgebra construct-a-dot-plot. **Intro Stats §2.1** is related (construct bar/line). IM Grade 6 Unit 8 asks students to make a dot plot from a list.

## Variety notes

**LOW_VARIETY:** one stem; only n and axis-scaffold change. That may be enough for a drawing skill. Context (class scores vs plant heights) is missing vs IM.

## Limitations

- Flags: **LOW_VARIETY**.
- **LOW_VARIETY:** one stem; only n and axis-scaffold change. That may be enough for a drawing skill. Context (class scores vs plant heights) is missing vs IM.
- Weak / missing OpenStax chapter match for this leaf.

## Proposed engine (proposal only)

stats draw (`g6_drawing_dot_plot`). UI-heavy; keep as drawing, don’t alias to interpret.

Generator (catalog): see `question_engine/catalogs/grade_6.py`.
