# Notes — `similar_figures_wp` (`pa_similar_figures`)

Also covers: `pa_similar_figures`, `pa_similar_figures_word_problems`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Similar figures: scale factor + missing side from a pair diagram / correspondence.
- **D=0:** Two similar triangles; one pair of corresponding sides and one missing side.
- **High D (≈16–22):** Quadrilaterals; find a side (not only “scale factor”).
- **Must not:** Dump $a/b=x/c$ with no figure story.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `use_legacy_similar_figures=True`, `prompt_style=diagram`.

- **D=0 seed=101:** $ABCD \sim EFGH.\ \text{Find the length of } EH.$ → $32$
- **D=0 seed=207:** $\triangle ABC \sim \triangle DEF.\ \text{The figures are similar. Find the scale factor from the smaller to the larger.}$ → $4$
- **D=8 seed=101:** $ABCD \sim EFGH.\ \text{Find the length of } EH.$ → $32$
- **D=8 seed=207:** $\triangle ABC \sim \triangle DEF.\ \text{The figures are similar. Find the scale factor from the smaller to the larger.}$ → $4$
- **D=16 seed=101:** $ABCD \sim EFGH.\ \text{Find the length of } EH.$ → $32$
- **D=16 seed=207:** $\triangle ABC \sim \triangle DEF.\ \text{The figures are similar. Find the scale factor from the smaller to the larger.}$ → $4$
- **D=22 seed=101:** $ABCD \sim EFGH.\ \text{Find the length of } EH.$ → $32$
- **D=22 seed=207:** $\triangle ABC \sim \triangle DEF.\ \text{The figures are similar. Find the scale factor from the smaller to the larger.}$ → $4$

## Current default (same D/seeds)

- **D=0 seed=101:** $\triangle ABC \sim \triangle DEF.\ \text{The figures are similar. Corresponding sides BC and EF measure 2 cm and 4 cm. If AB is 3 cm, find DE.}$ → $6\text{ cm}$ — frame_id=similar_triangles, scale=2
- **D=0 seed=207:** $\triangle ABC \sim \triangle DEF.\ \text{The figures are similar. Corresponding sides AB and DE measure 3 cm and 6 cm. If AC is 4 cm, find DF.}$ → $8\text{ cm}$ — frame_id=similar_triangles, scale=2
- **D=8 seed=101:** $\triangle ABC \sim \triangle DEF.\ \text{The figures are similar. Corresponding sides BC and EF measure 6 cm and 18 cm. If AB is 3 cm, find DE.}$ → $9\text{ cm}$ — frame_id=similar_triangles, scale=3
- **D=8 seed=207:** $\triangle ABC \sim \triangle XYZ.\ \text{The figures are similar. Corresponding sides AB and XY measure 3 cm and 12 cm. If AC is 7 cm, find XZ.}$ → $28\text{ cm}$ — frame_id=similar_triangles, scale=4
- **D=16 seed=101:** $ABCD \sim EFGH.\ \text{The figures are similar. Corresponding sides AB and EF measure 4 cm and 12 cm. If AD is 5 cm, find EH.}$ → $15\text{ cm}$ — frame_id=similar_quad, scale=3
- **D=16 seed=207:** $ABCD \sim EFGH.\ \text{The figures are similar. Corresponding sides AB and EF measure 2 cm and 10 cm. If BC is 3 cm, find FG.}$ → $15\text{ cm}$ — frame_id=similar_quad, scale=5
- **D=22 seed=101:** $ABCD \sim EFGH.\ \text{The figures are similar. Corresponding sides AB and EF measure 4 cm and 12 cm. If AD is 9 cm, find EH.}$ → $27\text{ cm}$ — frame_id=similar_quad, scale=3
- **D=22 seed=207:** $ABCD \sim EFGH.\ \text{The figures are similar. Corresponding sides AD and EH measure 8 cm and 40 cm. Find the scale factor from the smaller to the larger.}$ → $5$ — frame_id=similar_quad, ask=scale_factor, scale=5

## OpenStax examples + chapter/section cites

- **OpenStax Elementary Algebra 2e §8.7** — Similar figure applications (triangles / corresponding sides) — https://openstax.org/books/elementary-algebra-2e/pages/8-7-solve-proportion-and-similar-figure-applications

Local mining: `scripts/output/example_mining/` (EA 2e Ch. 2 / 6 / 7 / 8.7; PA 2e Ch. 3–6).

## Variety notes

Old seed 101 is the same “Find EH → 32” at every D; seed 207 always “find the scale factor → 4”. Default D=0 is similar triangles with scale 2 and a missing side (EA §8.7 Ex 8.78). Higher D widens scale, switches to quadrilaterals, varies the missing side, and sometimes asks for the scale factor.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** SimilarFigures + `wp_packaging` (wired; scale/shape follow D).
- **New:** not this pass (already on skeleton).
- **Not this pass:** do not re-implement generators.

Suggested family from `G6_PA_INDEX.md`: `geometry`
