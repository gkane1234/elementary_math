# Notes — `calc_indef_int_multi_trick`

- **Display name:** Multi-technique (u-sub then PFD)
- **Category:** Calculus — Indefinite Integration
- **Generator:** `integral_multi_trick`
- **Suggested family:** `other`

---

## What the question should look like (D=0 vs high D)

- **Skill:** Indefinite integral that needs u-sub first, then partial fractions in \(u\) (OpenStax Vol. 2 §3.4 after a Vol. 1 §5.5 wrap).
- **D=0:** Old easy leftover is two-linear PFD after \(u=ax+b\) / \(e^{kx}\) / \(\sin,\cos\) (`u_sub_then_pfd_linear` / `_exp` / `_trig`).
- **Mid D (≈8):** Leftover exp/trig + log wrap; quadratic PFD in \(u\) (arctan). No linear \(u=ax+b\).
- **High D (≈16–22):** Log wrap only (`u_sub_then_pfd_log`) — \(\int R(\ln|ax+b|)/(ax+b)\,dx\).
- **Must not:** Bare PFD-in-\(x\) (that is the PFD sibling); padded `difficulty_costs`; new u-sub-then-parts / three-trick cores.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**. Live path is `calculus_integrals` → `_sample_pipeline_u_sub_then_pfd`. **Before leftover lockout:** D=0 mixed poly-linear (mis-stamped as `u_sub_then_pfd_exp`) / exp / trig; D=8–22 mixed exp / trig / log (all quadratic PFD at D≥8); linear wrap already dropped at D≥6 by the prefer heuristic.

**Live now** (`select_form_id` leftover bands; poly wrap stamped `u_sub_then_pfd_linear`):

40-seed counts: D=0 `u_sub_then_pfd_exp` 14 / `linear` 13 / `trig` 13; D=8 `log` 14 / `trig` 13 / `exp` 13 (no linear); D=16/22 `log` 40.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int \frac{3\left(e^{3x}\right)-1}{\left(e^{3x}\right)\left(e^{3x}-1\right)}\cdot 3e^{3x}\,dx$ | $\ln|\left(e^{3x}\right)|+2\ln|\left(e^{3x}-1\right)|+C$ | `u_sub_then_pfd_exp` two-linear |
| 0 | 207 | $\int \frac{0\left(\sin(2x)\right)+1}{\left(\sin(2x)-1\right)\left(\sin(2x)-2\right)}\cdot 2\cos(2x)\,dx$ | $-\ln|\left(\sin(2x)-1\right)|+\ln|\left(\sin(2x)-2\right)|+C$ | `u_sub_then_pfd_trig` two-linear |
| 0 | 0 | $\int 3\frac{-3x-4}{\left(3x+2\right)\left(3x\right)}\,dx$ | $\ln|\left(3x+2\right)|-2\ln|\left(3x\right)|+C$ | `u_sub_then_pfd_linear` old easy \(u=ax+b\) |
| 8 | 101 | $\int \frac{2\left(\cos(x)\right)+3}{\left(\cos(x)\right)^{2}+9}\left(-\sin(x)\right)\,dx$ | $\ln|\cos(x) - 2|+\ln|\cos(x)^{2}+9|+\arctan(\frac{\cos(x)}{3})+C$ | leftover trig + quad PFD |
| 8 | 207 | $\int \frac{-7}{\left(\ln|x + 2|\right)^{2}+9}\frac{1}{x + 2}\,dx$ | $-2\ln|\ln|x + 2| - 1|-\frac{7}{3}\arctan(\frac{\ln|x + 2|}{3})+C$ | `u_sub_then_pfd_log` unlock |
| 16 | 101 | $\int \frac{-2\left(\ln|x + 2|\right)+6}{\left(\ln|x + 2|\right)^{2}+9}\frac{1}{x + 2}\,dx$ | $3\ln|\ln|x + 2| - 2|-\ln|\ln|x + 2|^{2}+9|+2\arctan(\frac{\ln|x + 2|}{3})+C$ | log only (no exp/trig leftover) |
| 16 | 207 | $\int \frac{2}{\left(\ln|x + 1|\right)^{2}+4}\frac{1}{x + 1}\,dx$ | $-2\ln|\ln|x + 1| - 4|+\arctan(\frac{\ln|x + 1|}{2})+C$ | same hard band as D=22 |
| 22 | 101 | $\int \frac{3}{\left(\ln|x - 2|\right)^{2}+9}\frac{1}{x - 2}\,dx$ | $2\ln|\ln|x - 2| - 2|+\arctan(\frac{\ln|x - 2|}{3})+C$ | `u_sub_then_pfd_log` only |
| 22 | 207 | $\int \frac{2\left(\ln|x + 8|\right)-7}{\left(\ln|x + 8|\right)^{2}+16}\frac{1}{x + 8}\,dx$ | $14\ln|\ln|x + 8| + 13|+\ln|\ln|x + 8|^{2}+16|-\frac{7}{4}\arctan(\frac{\ln|x + 8|}{4})+C$ | no D=0 leftover |

Opt-out flag used: _(none — live generator is the old path)_

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 / 2 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §5.5 | https://openstax.org/books/calculus-volume-1/pages/5-5-substitution | u-sub with a visible \(du\) factor wrapping a rational in \(u\) (not table \(\int x^n\)). Linear \(u=ax+b\) is the D=0 leftover. |
| OpenStax Calculus Volume 2 §3.4 | https://openstax.org/books/calculus-volume-2/pages/3-4-partial-fractions | After the wrap, decompose \(R(u)\) (two linears at easy; irreducible quadratic \(\to\) arctan at mid/high). Bare PFD-in-\(x\) stays on the PFD sibling. |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `textbooks/openstax/html/calculus-volume-2/` · `scripts/output/example_mining/challenging_indefinite_integrals_bc.md` §8 pipeline lookalikes.

## Variety notes

Not a WP. D=0 rotates the three old easy wraps (linear / exp / trig) with two-linear PFD. Mid D drops linear and unlocks log + quadratic PFD. High D is log-only. Do not invent a u-sub-then-parts / \(R(e^{x^{2}})\) / three-trick core.

## Limitations

- **Status:** leftover lockout of D=0 linear/exp/trig shipped. Remaining `LIMITATIONS`: D=16 and D=22 are the same log-only mix (no fourth existing wrap); linear wrap can still look like scaled PFD-in-\(x\) after \(u=ax+b\); quadratic display can juxtapose \(e^{2x}^{2}\); no u-sub-then-parts / three-trick / BC-bank extra pipeline; named `pfd_form_preset` is unused by this sampler; no diagram.
- **Live pairwise:** each item stamps `form_id`, `generator=integral_multi_trick`, and `family`; copies `form_id` / `generator` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `integral_multi_trick`

## Proposed engine (reuse vs new)

- **Reuse:** existing `_sample_pipeline_u_sub_then_pfd` + four old wraps (`linear` / `exp` / `trig` / `log`). `u_sub_then_pfd_linear` is a stamp of the existing poly wrap (was mislabeled `exp`), not a new core.
- **Not this pass:** u-sub-then-parts; three-trick pipelines; a fourth expert wrap.
