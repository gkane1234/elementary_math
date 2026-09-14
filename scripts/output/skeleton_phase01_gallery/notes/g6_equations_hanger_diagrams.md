# `g6_equations_hanger_diagrams` — Hanger diagrams (equations)

> RED HEADER: **UNCLEAR** · **LOW_VARIETY**
>
> Ship samples anyway. Implementation must not treat a green checkbox as success if the old stem is a stub or a single template.

Steps 1–3 only (old live samples, intended look, OpenStax). No engine implementation.

## What the question should look like (D=0 vs high D)

**D=0:** balanced hanger for `nx = k` with tiny `n` (2 or 3) and `k` a multiple. “Use the diagram to solve `3x=15`.”

**High D (intended):** still one-step multiplication; maybe `x+a=b` hangers (circles vs squares). Old path only scales `n` and `k` (`9x=153`).

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22, `include_answer_key=True`, seeds 101 and 202. Default path **is** the old path (these leaves are not on equation/poly skeletons). One sample per D below (seed 101).

| D | Prompt (latex) | Answer |
|--:|----------------|--------|
| 0 | `$\text{Use the diagram to solve } 3x = 15.$` | `$5$` |
| 8 | `$\text{Use the diagram to solve } 4x = 32.$` | `$8$` |
| 16 | `$\text{Use the diagram to solve } 6x = 72.$` | `$12$` |
| 22 | `$\text{Use the diagram to solve } 9x = 153.$` | `$17$` |

Second seed (202) at D=0 and D=22:

- D=0: `$\text{Use the diagram to solve } 3x = 15.$` → `$5$`
- D=22: `$\text{Use the diagram to solve } 8x = 152.$` → `$19$`

## OpenStax examples + chapter/section

**OpenStax has no hanger diagrams.** Closest: **Prealgebra 2e §8.2** *Solve Equations Using the Division and Multiplication Properties of Equality* ([link](https://openstax.org/books/prealgebra-2e/pages/8-2-solve-equations-using-the-division-and-multiplication-properties-of-equality)) — exercises like `4x=32`.

G6 gold: **IM Grade 6 Unit 6** hangers (balanced mobile: circles = squares).

**UNCLEAR:** is the skill “read a hanger” or “solve `nx=k` with a picture?” Old latex already prints the equation, so the hanger is optional decoration.

## Variety notes

**LOW_VARIETY:** 8/8 samples are `Use the diagram to solve nx = k`. No addition hangers, no both-sides, no inequality mix (that is a sibling leaf).

## Limitations

- Flags: **UNCLEAR**, **LOW_VARIETY**.
- **LOW_VARIETY:** 8/8 samples are `Use the diagram to solve nx = k`. No addition hangers, no both-sides, no inequality mix (that is a sibling leaf).
- Weak / missing OpenStax chapter match for this leaf.

## Proposed engine (proposal only)

SolveLinear one-step multiplication + hanger SVG. Skip if we cannot match IM hangers honestly — then leave leaf / document skip (benchmark-old-path rule 6).

Generator (catalog): see `question_engine/catalogs/grade_6.py`.
