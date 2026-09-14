# `g6_equations_tape_diagrams` — Tape diagrams

> RED HEADER: **UNCLEAR** · **LOW_VARIETY**
>
> Ship samples anyway. Implementation must not treat a green checkbox as success if the old stem is a stub or a single template.

Steps 1–3 only (old live samples, intended look, OpenStax). No engine implementation.

## What the question should look like (D=0 vs high D)

**D=0:** one-step part–whole tape: equal bars totaling a small integer; find `x` (e.g. 5 equal parts = 25 → `x=5`). Prompt is only “use the tape diagram”.

**High D (intended):** still *read the tape*, not a dumped `nx=k`. IM-style: comparison tapes, two-step (equal parts plus a remainder), labeled vs unlabeled. Old path does **not** do that — numbers in the answer grow, prompt text does not.

## What old path actually produced

Live `_generate_for_type` at D=0 / 8 / 16 / 22, `include_answer_key=True`, seeds 101 and 202. Default path **is** the old path (these leaves are not on equation/poly skeletons). One sample per D below (seed 101).

| D | Prompt (latex) | Answer |
|--:|----------------|--------|
| 0 | `$\text{Use the tape diagram to find } x.$` | `$5$` |
| 8 | `$\text{Use the tape diagram to find the missing value.}$` | `$12$` |
| 16 | `$\text{Use the tape diagram to find the missing value.}$` | `$9$` |
| 22 | `$\text{Use the tape diagram to find the missing value.}$` | `$20$` |

Second seed (202) at D=0 and D=22:

- D=0: `$\text{Use the tape diagram to find } x.$` → `$5$`
- D=22: `$\text{Use the tape diagram to find the missing value.}$` → `$19$`

## OpenStax examples + chapter/section

**OpenStax has no tape-diagram chapter.** Closest algebra: **Prealgebra 2e §8.1–8.2** (one-step +/− and ×/÷ equations) and §2.3 bar-model-ish *translate and solve*, but those are symbolic.

G6 gold for tapes is **Illustrative Mathematics Grade 6 Unit 6** (Expressions and Equations — tape diagrams for `x+p=q` and `px=q`).

**UNCLEAR:** without IM-style frame variety, this leaf is a SolveLinear one-step with a picture. Confirm whether we emulate IM tapes or treat this as optional diagram skin on one-step equations.

## Variety notes

**LOW_VARIETY:** prompt is always “Use the tape diagram to find `x` / the missing value.” SVG exists (`diagram_svg`) but latex does not describe the tape. D=0 and D=22 look the same in the stem.

## Limitations

- Flags: **UNCLEAR**, **LOW_VARIETY**.
- **LOW_VARIETY:** prompt is always “Use the tape diagram to find `x` / the missing value.” SVG exists (`diagram_svg`) but latex does not describe the tape. D=0 and D=22 look the same in the stem.
- Diagram-named leaf: stem/latex often lacks a readable diagram (or diagram is metadata-only).
- Difficulty scaling flat in the stem across D (answers/numbers may grow only).
- Weak / missing OpenStax chapter match for this leaf.

## Proposed engine (proposal only)

New diagram wrapper around SolveLinear one-step (addition or multiplication tape). Do not invent two-step/distribute unless old SVG actually shows it — inspect SVG in implementation.

Generator (catalog): see `question_engine/catalogs/grade_6.py`.
