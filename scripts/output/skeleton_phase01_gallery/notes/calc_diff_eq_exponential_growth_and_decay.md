# Notes — `calc_diff_eq_exponential_growth_and_decay`

- **Display name:** Exponential growth and decay
- **Category:** Calculus — Differential Equations
- **Generator:** `exponential_growth_decay`
- **Suggested family:** `other`

---

## Limitations

- **Status:** shipped — constructive (gallery-wired this wave)
- **Generator:** `calc_continuous_growth_decay`
- **Remaining limits:** Constructive app generators with continuous-D structure knobs. Gaps: story frame banks thinner than OpenStax for related rates / growth; volumes mostly axis-of-rotation textbook templates; no interactive figures.

## What the question should look like (D=0 vs high D)

- **Skill:** Practice exponential growth and decay.
- **D=0:** As simple as old easy at D=0 — copy live samples below.
- **High D (≈16–22):** Numeric hardness first; technique/format unlocks by D≈16–22.
- **Must not:** Wrong-topic shapes; derivative-only prompts on integral leaves; equation dumps without story on WP/optimization/related-rates.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for these Calculus leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{An investment of }50\text{ dollars grows continuously according to }y'=1y.\text{ Find }y(1)\text{ (years).}$ | $50e^{1}$ | — |
| 0 | 207 | $\text{A bacterial culture of }10\text{ cells grows continuously according to }y'=2y.\text{ Find }y(1)\text{ (hours).}$ | $10e^{2}$ | — |
| 8 | 101 | $\text{Solve }y'=2y,\ y(0)=3.$ | $y=3e^{2x}$ | — |
| 8 | 207 | $\text{A radioactive sample of }200\text{ grams decays continuously according to }y'=-2y.\text{ Find }y(4)\text{ (years).}$ | $200e^{-8}$ | — |
| 16 | 101 | $\text{A population of }128\text{ people has continuous half-life }T.\text{ How much remains after }2T?$ | $32$ | — |
| 16 | 207 | $\text{A population of }50\text{ people doubles continuously every }T\text{ years. How much is present after }3T\text{ years?}$ | $400$ | — |
| 22 | 101 | $\text{A bacterial culture of }200\text{ cells doubles continuously every }T\text{ years. How much is present after }2T\text{ years?}$ | $800$ | — |
| 22 | 207 | $\text{A radioactive sample of }128\text{ grams has continuous half-life }T.\text{ How much remains after }4T?$ | $8$ | — |

Opt-out flag used: `(none — live default is old path)`

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 / 2 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 2 §4.2 | https://openstax.org/books/calculus-volume-2/pages/4-2-direction-fields-and-numerical-methods | growth/decay IVP frames |
| OpenStax Calculus Volume 1 §6.8 | https://openstax.org/books/calculus-volume-1/pages/6-8-exponential-growth-and-decay | y'=ky applications (Vol 1 if present) |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (and volume-2).

## Variety notes

Not a Mad-Lib WP unless related-rates / optimization / growth-decay. Algebra/technique shapes follow old path samples above; OpenStax frames win for story variety.

## Proposed engine (reuse vs new) — proposal only

- **Proposal:** Keep DE constructive/pilot path; not Diff skeleton.
- **New Integral skeleton?** only if shared definite/indefinite cores need one API; otherwise keep `integrals.py` + form catalogs.
- **Reuse Diff?** only for computing derivatives inside apps (related rates, MVT, L'Hôpital); not for integral leaves.
- **Not this pass:** notes only — no generator wiring.

_Catalog generator `exponential_growth_decay`; limits/differentiation owned by other agent._
