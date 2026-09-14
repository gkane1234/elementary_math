# Notes — `calc_diff_eq_slope_fields`

- **Display name:** Slope fields
- **Category:** Calculus — Differential Equations
- **Generator:** `slope_field_interpret`
- **Suggested family:** `other`

---

## Limitations

- **Status:** shipped — constructive (gallery-wired this wave)
- **Generator:** `slope_field_interpret`
- **Remaining limits:** Constructive app generators with continuous-D structure knobs. Gaps: story frame banks thinner than OpenStax for related rates / growth; volumes mostly axis-of-rotation textbook templates; no interactive figures.

## What the question should look like (D=0 vs high D)

- **Skill:** Practice slope fields.
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; technique/format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; derivative-only prompts on integral leaves; equation dumps without story on WP/optimization/related-rates.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for these Calculus leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{For }y'=x,\text{ what is the slope at }(-2,1)?$ | $-2$ | — |
| 0 | 207 | $\text{For }y'=x,\text{ what is the slope at }(2,0)?$ | $2$ | — |
| 8 | 101 | $\text{For }y'=x+y,\text{ what is the slope at }(0,1)?$ | $1$ | — |
| 8 | 207 | $\text{For }y'=x,\text{ what is the slope at }(-3,-3)?$ | $-3$ | — |
| 16 | 101 | $\text{For }y'=x,\text{ what is the slope at }(2,3)?$ | $2$ | — |
| 16 | 207 | $\text{For }y'=x+y,\text{ what is the slope at }(0,-3)?$ | $-3$ | — |
| 22 | 101 | $\text{For }y'=xy,\text{ what is the slope at }(-1,-2)?$ | $2$ | — |
| 22 | 207 | $\text{For }y'=xy,\text{ what is the slope at }(0,0)?$ | $0$ | — |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 / 2 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 2 §4.1 | https://openstax.org/books/calculus-volume-2/pages/4-1-basics-of-differential-equations | match/interpret slope field |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (and volume-2).

## Variety notes

Not a Mad-Lib WP unless related-rates / optimization / growth-decay. Algebra/technique shapes follow old path samples above; OpenStax frames win for story variety.

## Proposed engine (reuse vs new) — proposal only

- **Proposal:** Keep DE constructive/pilot path; not Diff skeleton.
- **New Integral skeleton?** only if shared definite/indefinite cores need one API; otherwise keep `integrals.py` + form catalogs.
- **Reuse Diff?** only for computing derivatives inside apps (related rates, MVT, L'Hôpital); not for integral leaves.
- **Not this pass:** notes only — no generator wiring.

_Catalog generator `slope_field_interpret`; limits/differentiation owned by other agent._
