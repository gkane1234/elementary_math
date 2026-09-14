# Notes — `calc_diff_eq_exponential_growth_and_decay` (`Exponential growth and decay`)

- **Display name:** Exponential growth and decay
- **Category:** Calculus — Differential Equations
- **Generator:** `calc_continuous_growth_decay`
- **Suggested family:** other (continuous \(y'=ky\) stories / IVP / half-life; not Algebra discrete %)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Solve continuous \(y'=ky\) models: evaluate \(y(t)=y_0 e^{kt}\), write the IVP solution, or count doubling / half-life steps.
- **D=0:** Story leftover: find \(y(t)\) from \(y'=ky\) (growth; old easy). Contexts rotate population / bacteria / investment.
- **Mid D (≈8):** Growth leftover still allowed, plus story decay \(y'=-ky\) and solve \(y'=ky,\ y(0)=y_0\).
- **High D (≈16):** Lock out easy growth story. Decay leftover + IVP leftover plus doubling / half-life (integer \(nT\)).
- **Expert (≈22):** Doubling / half-life only.
- **Must not:** Algebra discrete % per period; Newton's law of cooling / logistic (new cores); padded `difficulty_costs`; figure bank.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**, before leftover bands. Exclusive cliff: D=0 always growth story; D=8 mix of decay story and IVP (no growth leftover); D≥16 mix of doubling and half-life. D=16 and D=22 were the same pool. `generator` / `form_id` unstamped. No `spec_snapshot`. 40-seed counts: D=0 all growth story; D=8 decay 23 / IVP 17; D=16 doubling 29 / half-life 11; D=22 half-life 18 / doubling 22.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{A population of }10\text{ people grows continuously according to }y'=3y.\text{ Find }y(1)\text{ (years).}$ | $10e^{3}$ | growth story; \(k\in\{1,2,3\}\), \(t\in\{1,2,3\}\) |
| 0 | 207 | $\text{A bacterial culture of }50\text{ cells grows continuously according to }y'=2y.\text{ Find }y(1)\text{ (hours).}$ | $50e^{2}$ | \(y_0\in\{10,20,50,100\}\) |
| 8 | 101 | $\text{Solve }y'=2y,\ y(0)=6.$ | $y=6e^{2x}$ | `egd_ivp`; exclusive (no growth leftover) |
| 8 | 207 | $\text{A radioactive sample of }80\text{ grams decays continuously according to }y'=-1y.\text{ Find }y(3)\text{ (years).}$ | $80e^{-3}$ | decay story; \(k=1\) writes \(y'=-1y\) |
| 16 | 101 | $\text{A population of }50\text{ people doubles continuously every }T\text{ years. How much is present after }2T\text{ years?}$ | $200$ | doubling; \(n\in\{2,3,4\}\) |
| 16 | 207 | $\text{A population of }128\text{ people has continuous half-life }T.\text{ How much remains after }4T?$ | $8$ | half-life; \(y_0\in\{64,128,256\}\) |
| 22 | 101 | $\text{A population of }64\text{ people has continuous half-life }T.\text{ How much remains after }2T?$ | $16$ | D=22 == D=16 pool |
| 22 | 207 | $\text{An investment of }50\text{ dollars doubles continuously every }T\text{ years. How much is present after }3T\text{ years?}$ | $400$ | doubling leftover at expert (old exclusive) |

Opt-out flag used: _(none — live catalog is the old path)_

## Live now (`_generate_for_type`)

Leftover lockout on the same five builders. D=0 stays old growth story. Gallery seeds 101/207/313 can collide on one form at mid/high D; rotation is across seeds.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{A population of }50\text{ people grows continuously according to }y'=1y.\text{ Find }y(2)\text{ (years).}$ | $50e^{2}$ | `egd_growth_story` |
| 0 | 1 | $\text{A bacterial culture of }50\text{ cells grows continuously according to }y'=1y.\text{ Find }y(1)\text{ (hours).}$ | $50e^{1}$ | old easy |
| 8 | 1 | $\text{A bacterial culture of }50\text{ cells grows continuously according to }y'=1y.\text{ Find }y(1)\text{ (hours).}$ | $50e^{1}$ | growth leftover |
| 8 | 0 | $\text{Solve }y'=3y,\ y(0)=2.$ | $y=2e^{3x}$ | `egd_ivp` |
| 8 | 101 | $\text{A medicine dose of }200\text{ mg decays continuously according to }y'=-1y.\text{ Find }y(3)\text{ (hours).}$ | $200e^{-3}$ | `egd_decay_story` |
| 16 | 1 | $\text{A medicine dose of }100\text{ mg decays continuously according to }y'=-1y.\text{ Find }y(1)\text{ (hours).}$ | $100e^{-1}$ | decay leftover |
| 16 | 7 | $\text{Solve }y'=2y,\ y(0)=5.$ | $y=5e^{2x}$ | IVP leftover |
| 16 | 101 | $\text{A bacterial culture of }50\text{ cells doubles continuously every }T\text{ years. How much is present after }4T\text{ years?}$ | $800$ | no growth leftover |
| 22 | 1 | $\text{A population of }50\text{ people doubles continuously every }T\text{ years. How much is present after }3T\text{ years?}$ | $400$ | `egd_doubling` only (plus half-life) |
| 22 | 101 | $\text{A medicine dose of }64\text{ mg has continuous half-life }T.\text{ How much remains after }4T?$ | $4$ | `egd_half_life` |

40-seed counts **after**: D=0 growth only; D=8 leftover growth + decay + IVP (14/15/11); D=16 leftover decay + IVP + doubling + half-life (11/8/14/7, no growth); D=22 doubling + half-life only (19/21).

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §6.8 Exponential Growth and Decay | https://openstax.org/books/calculus-volume-1/pages/6-8-exponential-growth-and-decay | \(y'=ky\), \(y(t)=y_0 e^{kt}\). D=0 is story-evaluate \(y(t)\) (old easy). Half-life / doubling as \(nT\) counts at high D. |
| Same §6.8 | same | Cooling (\(T'=k(T-T_a)\)), find \(k\) from two data points, carbon dating — **not this pass** (leave on LIMITATIONS) |
| OpenStax Calculus Volume 2 §4.2 Direction Fields and Numerical Methods | https://openstax.org/books/calculus-volume-2/pages/4-2-direction-fields-and-numerical-methods | Autonomous \(y'=ky\) IVP write-the-formula (old mid). Direction-field sketches — other leaf. |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · Vol 1 §6.8 not in `scripts/output/example_mining/calculus-volume-1/stage1/` (mining stops before apps-of-int / DE). Learning-objective spine: `scripts/output/example_mining/progression/full_spine.md` (Vol 1 §6.8 / Vol 2 §4.2).

## Variety notes

WP stories: several OpenStax-derived frames at the same D (population / bacteria / investment / radioactive / medicine) — not one vehicle. Algebra/technique shapes follow old path (integer \(k\), \(y'=1y\) not \(y'=y\), integer \(nT\) half-life). Same-D rotation at mid D: leftover growth vs decay vs IVP. High D keeps old doubling / half-life builders (do not invent cooling).

## Limitations

- **Status:** shipped — leftover lockout of story \(y'=ky\). Remaining `LIMITATIONS`: no Newton's cooling / logistic / find-\(k\) from data / carbon dating; half-life and doubling are integer \(nT\) counts (not solve for \(T\) or \(k=\ln 2/T\)); D=16 can still emit decay/IVP leftover (intentional).
- **Live pairwise:** each item stamps `form_id`, shared `generator=calc_continuous_growth_decay`, and `family`; copies `form_id` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `calc_continuous_growth_decay`

## Proposed engine (reuse vs new)

- **Reuse:** existing growth-story / decay-story / IVP / doubling / half-life builders (now in `calc_app_diff.py`). Depth = real structure (lock out easy growth; mix leftover at D=8 / D=16) — not padded `difficulty_costs`.
- **Not this pass:** Newton's cooling; logistic; two-point fit for \(k\); Algebra discrete % (other leaf).
