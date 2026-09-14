# Notes — `calc_app_diff_differentials` (`Differentials`)

- **Display name:** Differentials
- **Category:** Calculus — Applications of Differentiation
- **Generator:** `differentials`
- **Suggested family:** other (find \(dy=f'(x)\,dx\); not linearization \(L(x)\), not a WP)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Compute the differential \(dy=f'(x)\,dx\), or evaluate it at a given \(x\) and \(dx\).
- **D=0:** Easy leftover mix: \(y=x^n\), \(y=x^{2}+bx\), trig, \(e^{kx}\), \(\ln x/\log x\) (old easy; OpenStax Ex. 4.8 includes \(x^{2}+2x\) and \(\cos x\)).
- **Mid D (≈8):** Easy leftover still allowed, plus \(\sqrt{x}\) and \(1/x\).
- **High D (≈16):** Lock out D=0 log/power/trig/exp leftovers. Radical/reciprocal leftover plus product / quotient / \(e^{x^{2}}\) / evaluate-\(dy\).
- **Expert (≈22):** Nested only (product, quotient, chain-exp, eval \(dx\)).
- **Must not:** Linearization \(L(x)\) (other leaf); cube-volume / percent-error stories; padded `difficulty_costs`; figure bank.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**, before leftover bands. Accumulating unlocks: D=0 always poly/trig/exp/ln; D=8 added radical/reciprocal; D≥14 added product/quotient/chain_exp/eval_dx **without locking easy leftovers**. D=16 and D=22 were the same 11-family pool. `form_id` unstamped; top-level `generator` unstamped. 40-seed counts: D=0 exp 8 / poly_quad 11 / poly_power 6 / ln 10 / trig 5; D=8 same plus reciprocal 8 / radical 4; D=16 and D=22 identical (ln 3, trig 4, poly_power 2, radical 6, chain_exp 4, exp 3, product 3, reciprocal 2, poly_quad 3, quotient 5, eval_dx 5).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{For }y=\log(x),\text{ find }dy.$ | $dy=\frac{1}{x}\,dx$ | `ln` leftover |
| 0 | 1 | $\text{For }y=x^{2},\text{ find }dy.$ | $dy=2x\,dx$ | `poly_power` |
| 0 | 7 | $\text{For }y=\sin x,\text{ find }dy.$ | $dy=\cos(x)\,dx$ | `trig`; OpenStax Ex. 4.8 |
| 8 | 101 | $\text{For }y=x^{-1},\text{ find }dy.$ | $dy=-\frac{1}{x^{2}}\,dx$ | `reciprocal` unlock |
| 8 | 207 | $\text{For }y=\frac{1}{x},\text{ find }dy.$ | $dy=-\frac{1}{x^{2}}\,dx$ | same family, frac display |
| 16 | 101 | $\text{For }y=\exp(x^{2}),\text{ find }dy.$ | $dy=2xe^{x^{2}}\,dx$ | `chain_exp`; Checkpoint 4.8 |
| 16 | 207 | $\text{For }y=\frac{x}{x+1},\text{ find }dy.$ | $dy=\frac{1}{\left(x+1\right)^{2}}\,dx$ | `quotient` |
| 22 | 101 | $\text{For }y=\exp(x^{2}),\text{ find }dy.$ | $dy=2xe^{x^{2}}\,dx$ | D=22 == D=16 pool |
| 22 | 2 | $\text{For }y=x^{2},\text{ find }dy.$ | $dy=2x\,dx$ | power leftover at expert (old accumulating) |

Opt-out flag used: _(none — live catalog is the old path)_

## Live now (`_generate_for_type`)

Leftover lockout on the same eleven family builders. D=0 stays the old five-family easy mix. Gallery seeds 101/207/313 can collide on one form at a band; rotation is across seeds.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{For }y=\sin x,\text{ find }dy.$ | $dy=\cos(x)\,dx$ | `trig` |
| 0 | 1 | $\text{For }y=x^{2},\text{ find }dy.$ | $dy=2x\,dx$ | `poly_power` |
| 0 | 0 | $\text{For }y=\ln(x),\text{ find }dy.$ | $dy=\frac{1}{x}\,dx$ | `ln` leftover |
| 8 | 101 | $\text{For }y=\log(x),\text{ find }dy.$ | $dy=\frac{1}{x}\,dx$ | ln leftover |
| 8 | 0 | $\text{For }y=\sqrt{x},\text{ find }dy.$ | $dy=\frac{1}{2\sqrt{x}}\,dx$ | `radical` |
| 16 | 1 | $\text{For }y=x^{1/2},\text{ find }dy.$ | $dy=\frac{1}{2\sqrt{x}}\,dx$ | radical leftover (no ln/power) |
| 16 | 101 | $\text{For }y=x(x+1)^{-1},\text{ find }dy.$ | $dy=\frac{1}{\left(x+1\right)^{2}}\,dx$ | `quotient` |
| 16 | 0 | $\text{For }y=x\left(x + 3\right),\text{ find }dy\text{ when }x=5\text{ and }dx=\frac{1}{10}.$ | $\frac{13}{10}$ | `eval_dx`; Ex. 4.8 evaluate |
| 22 | 101 | $\text{For }y=\exp(x^{2}),\text{ find }dy.$ | $dy=2xe^{x^{2}}\,dx$ | `chain_exp` only (plus product/quotient/eval) |
| 22 | 1 | $\text{For }y=\sin(x)\,x,\text{ find }dy.$ | $dy=\left(\sin(x)+x\cos(x)\right)\,dx$ | `product` |

40-seed counts **after**: D=0 ln 6 / poly_power 7 / poly_quad 9 / exp 8 / trig 10; D=8 leftover easy + radical 3 / reciprocal 5; D=16 radical 6 / reciprocal 8 + nested (no ln/power/trig/exp); D=22 eval_dx 7 / product 11 / chain_exp 14 / quotient 8 only.

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §4.2 Example 4.8 | https://openstax.org/books/calculus-volume-1/pages/4-2-linear-approximations-and-differentials | Find \(dy\) for \(y=x^{2}+2x\) and \(y=\cos x\); also evaluate at \(x=3\), \(dx=0.1\). D=0 keeps find-\(dy\) (old easy); eval-\(dx\) stays high D as in the old nested unlock. |
| Same §4.2 Checkpoint 4.8 | same | \(y=e^{x^{2}}\), find \(dy\) — old nested `chain_exp`, now expert. |
| Same §4.2 Example 4.9 / 4.10 / 4.11 | same | \(\Delta y\) vs \(dy\); cube-volume error; relative/percentage error — **not this pass** (leave on LIMITATIONS) |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/4-2-linear-approximations-and-differentials.md`.

## Variety notes

Not a WP. Same-D rotation at D=0: power vs quad vs trig vs exp vs ln (old mix — do not shrink D=0). Mid D adds radical/reciprocal. High D keeps old nested builders (product, quotient, \(e^{x^{2}}\), eval \(dx\)) — do not invent cube-error cores.

## Limitations

- **Status:** shipped — leftover lockout of D=0 log/power/trig/exp. Remaining `LIMITATIONS`: no \(\Delta y\) vs \(dy\) (Ex. 4.9); no cube-volume / sphere-radius measurement error (Ex. 4.10); no relative/percentage error (Ex. 4.11); D=16 can still emit radical/reciprocal leftover (intentional); no diagram of \(dy\) vs \(\Delta y\).
- **Live pairwise:** each item stamps `form_id`, shared `generator=differentials`, and `family`; copies `form_id` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `differentials`

## Proposed engine (reuse vs new)

- **Reuse:** existing eleven family builders (now in `calc_app_diff.py`). Depth = real structure (lock out easy log/power; mix leftover at D=8 / D=16; D=22 nested only) — not padded `difficulty_costs`.
- **Not this pass:** \(\Delta y\) comparison; applied error estimates; linearization (other leaf).
