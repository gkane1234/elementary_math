# Notes — `calc_diff_eq_introduction` (`Introduction`)

- **Display name:** Introduction
- **Category:** Calculus — Differential Equations
- **Generator:** `de_introduction`
- **Suggested family:** other (constructive verify-solution on \(y=Ce^{kx}\) / \(y=Cx^{n}\))

---

## What the question should look like (D=0 vs high D)

- **Skill:** Verify that a proposed family solves a first-order DE by differentiating and substituting.
- **D=0:** Exponential leftover \(y=Ce^{kx}\) solves \(y'=ky\) (old easy; OpenStax Vol 2 §4.1 verify).
- **Mid D (≈8):** Exponential leftover still allowed, plus Euler \(y=Cx^{n}\) solves \(x\,y'=ny\) for \(x>0\).
- **High D (≈16):** Lock out exponential leftover. Euler only.
- **Expert (≈22):** Euler only (no third old form).
- **Must not:** Generic \(\frac{d}{dx}\) dump; padded `difficulty_costs`; classify-order / linear-vs-nonlinear stems this pass; IVP find-\(C\); trig verify.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**, before leftover bands. Exclusive cliff: D=0 always `verify_exp`; D≥8 always `verify_euler`. D=8, D=16, and D=22 were the same Euler family. `generator` was unstamped on the `_framework` wrapper. No `spec_snapshot`. 40-seed counts: D=0 all `verify_exp`; D=8/16/22 all `verify_euler`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Verify that }y=Ce^{3x}\text{ solves }y'=3y.$ | $y'=3Ce^{3x}=3y$ | `verify_exp` |
| 0 | 0 | $\text{Verify that }y=Ce^{5x}\text{ solves }y'=5y.$ | $y'=5Ce^{5x}=5y$ | same exponential |
| 8 | 101 | $\text{Verify that }y=Cx^{4}\text{ solves }x\,y'=4y\text{ for }x>0.$ | $y'=4Cx^{3}\Rightarrow x y'=4y$ | `verify_euler`; exclusive (no exp leftover) |
| 8 | 1 | $\text{Verify that }y=Cx^{2}\text{ solves }x\,y'=2y\text{ for }x>0.$ | $y'=2Cx^{1}\Rightarrow x y'=2y$ | D=8 == D=16 Euler |
| 16 | 101 | $\text{Verify that }y=Cx^{4}\text{ solves }x\,y'=4y\text{ for }x>0.$ | $y'=4Cx^{3}\Rightarrow x y'=4y$ | same as D=8 |
| 22 | 101 | $\text{Verify that }y=Cx^{4}\text{ solves }x\,y'=4y\text{ for }x>0.$ | $y'=4Cx^{3}\Rightarrow x y'=4y$ | same as D=16 |

Opt-out flag used: _(none — live catalog is the old path)_

## Live now (`_generate_for_type`)

Leftover lockout on the same two verify builders. D=0 stays old exponential. Gallery seeds 101/207/313 can collide on one form; rotation is across seeds.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Verify that }y=Ce^{3x}\text{ solves }y'=3y.$ | $y'=3Ce^{3x}=3y$ | `verify_exp` |
| 0 | 1 | $\text{Verify that }y=Ce^{2x}\text{ solves }y'=2y.$ | $y'=2Ce^{2x}=2y$ | old easy exponential |
| 8 | 1 | $\text{Verify that }y=Ce^{2x}\text{ solves }y'=2y.$ | $y'=2Ce^{2x}=2y$ | exp leftover |
| 8 | 101 | $\text{Verify that }y=Cx^{2}\text{ solves }x\,y'=2y\text{ for }x>0.$ | $y'=2Cx^{1}\Rightarrow x y'=2y$ | Euler |
| 16 | 0 | $\text{Verify that }y=Cx^{3}\text{ solves }x\,y'=3y\text{ for }x>0.$ | $y'=3Cx^{2}\Rightarrow x y'=3y$ | Euler only |
| 16 | 101 | $\text{Verify that }y=Cx^{2}\text{ solves }x\,y'=2y\text{ for }x>0.$ | $y'=2Cx^{1}\Rightarrow x y'=2y$ | no exp leftover |
| 22 | 0 | $\text{Verify that }y=Cx^{3}\text{ solves }x\,y'=3y\text{ for }x>0.$ | $y'=3Cx^{2}\Rightarrow x y'=3y$ | Euler only |
| 22 | 101 | $\text{Verify that }y=Cx^{2}\text{ solves }x\,y'=2y\text{ for }x>0.$ | $y'=2Cx^{1}\Rightarrow x y'=2y$ | Euler only |
| 22 | 207 | $\text{Verify that }y=Cx^{4}\text{ solves }x\,y'=4y\text{ for }x>0.$ | $y'=4Cx^{3}\Rightarrow x y'=4y$ | Euler |

40-seed counts **after**: D=0 exp only; D=8 exp leftover + Euler (19/21); D=16 Euler only (no exp); D=22 Euler only.

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 2 §4.1 Basics of Differential Equations | https://openstax.org/books/calculus-volume-2/pages/4-1-basics-of-differential-equations | Verify a proposed \(y\) is a solution (exponential \(y=Ce^{kx}\) / power \(y=Cx^{n}\)); D=0 is the exponential verify (old easy) |
| Same §4.1 learning objectives | same | Identify order; general vs particular; IVP — **not this pass** (leave on LIMITATIONS) |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-2/` · Vol 2 Ch.4 not in `scripts/output/example_mining/calculus-volume-2/stage1/` (mining stops before DE). Learning-objective spine: `scripts/output/example_mining/progression/full_spine.md` (Vol 2 §4.1).

## Variety notes

Not a WP. D=0 one easy exponential verify (old). Same-D rotation at mid D: leftover \(y=Ce^{kx}\) vs Euler \(y=Cx^{n}\). High D Euler keeps integer \(n\in\{2,3,4\}\) from the old builder (including \(Cx^{1}\) in the \(n=2\) derivative line). Two old forms only, so D=16 and D=22 are both Euler-only.

## Limitations

- **Status:** shipped — leftover lockout of exponential verify. Remaining `LIMITATIONS`: no classify order / linear vs nonlinear; no IVP find-\(C\) / particular solution; no trig verify (\(y=\sin kx\)); D=16 and D=22 are the same Euler-only band (no third old form).
- **Live pairwise:** each item stamps `form_id`, shared `generator=de_introduction`, and `family`; copies `form_id` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `de_introduction`

## Proposed engine (reuse vs new)

- **Reuse:** existing `verify_exp` / `verify_euler` builders in `calc_app_diff.py`. Depth = real structure (lock out \(y=Ce^{kx}\); mix leftover at D=8) — not padded `difficulty_costs`.
- **Not this pass:** classify-order stems; IVP particular \(C\); trig/second-order verify; slope-field figures (other leaf).
