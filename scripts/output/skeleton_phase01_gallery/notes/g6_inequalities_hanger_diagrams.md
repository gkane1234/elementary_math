# `g6_inequalities_hanger_diagrams` — Hanger diagrams (inequalities)

> RED HEADER: **UNCLEAR** · **LOW_VARIETY**
>
> Ship samples anyway. Implementation must not treat a green checkbox as success if the old stem is a stub or a single template.

Steps 1–3 only (old live samples, intended look, OpenStax). No engine implementation.

## What the question should look like (D=0 vs high D)

**D=0:** same hanger as equations but `nx ≤ k` with small positives; answer `x ≤ k/n`.

**High D:** flip to `≥`; larger multiples. Still one-step. Do **not** reverse-inequality with negatives at G6 unless old SVG does (it does not).

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22, `include_answer_key=True`, seeds 101 and 202. Default path **is** the old path (these leaves are not on equation/poly skeletons). One sample per D below (seed 101).

| D | Prompt (latex) | Answer |
|--:|----------------|--------|
| 0 | `$\text{Use the diagram to solve } 3x \le 15.$` | `$x \le 5$` |
| 8 | `$\text{Use the diagram to solve } 4x \ge 32.$` | `$x \ge 8$` |
| 16 | `$\text{Use the diagram to solve } 6x \le 72.$` | `$x \le 12$` |
| 22 | `$\text{Use the diagram to solve } 9x \ge 153.$` | `$x \ge 17$` |

Second seed (202) at D=0 and D=22:

- D=0: `$\text{Use the diagram to solve } 3x \le 15.$` → `$x \le 5$`
- D=22: `$\text{Use the diagram to solve } 8x \le 152.$` → `$x \le 19$`

## OpenStax examples + chapter/section

OpenStax **Prealgebra 2e** inequalities are thin; **Elementary Algebra 2e §2.7** *Solve Linear Inequalities* has `4x ≤ 20` but no hangers.

G6 hangers: **IM Grade 6 Unit 6** (balanced vs unbalanced mobiles).

**UNCLEAR:** OpenStax never uses hangers for inequalities. Old path already prints `3x ≤ 15`, so the diagram is not required to do the math.

## Variety notes

**LOW_VARIETY:** only `nx ≤ k` or `nx ≥ k`. Prompt template is one sentence. No `x+a < b`, no graph-on-number-line (that is `g6_solving_and_graphing_one_step_inequalities`, backfill-owned).

## Limitations

- Flags: **UNCLEAR**, **LOW_VARIETY**.
- **LOW_VARIETY:** only `nx ≤ k` or `nx ≥ k`. Prompt template is one sentence. No `x+a < b`, no graph-on-number-line (that is `g6_solving_and_graphing_one_step_inequalities`, backfill-owned).

## Proposed engine (proposal only)

SolveInequality one-step multiplication + hanger SVG. Same caution as equation hangers.

Generator (catalog): see `question_engine/catalogs/grade_6.py`.
