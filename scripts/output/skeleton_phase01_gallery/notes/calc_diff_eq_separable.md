# Notes — `calc_diff_eq_separable` (`Separable`)

- **Display name:** Separable
- **Category:** Calculus — Differential Equations
- **Generator:** `separable_diff_eq`
- **Suggested family:** other (constructive separable IVP on \(dy/dx=ax\) / \(ky\) / \(y/x\))

---

## What the question should look like (D=0 vs high D)

- **Skill:** Separate variables, integrate both sides, apply the initial condition.
- **D=0:** Polynomial leftover \(\frac{dy}{dx}=ax\), \(y(0)=c_0\) (old easy; OpenStax Vol 2 §4.3 separate+integrate).
- **Mid D (≈8):** Polynomial leftover still allowed, plus exponential \(\frac{dy}{dx}=ky\), \(y(0)=c_0\).
- **High D (≈16):** Lock out polynomial leftover. Exponential leftover plus homogeneous \(\frac{dy}{dx}=\frac{y}{x}\) for \(x>0\), \(y(1)=4\).
- **Expert (≈22):** Homogeneous only.
- **Must not:** Generic \(\frac{d}{dx}\) dump; padded `difficulty_costs`; new mixed \(g(x)h(y)\) cores this pass; slope-field figures.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**, before leftover bands. Exclusive cliff: D=0 always poly; D=8 always exp; D≥16 always homogeneous \(y/x\). D=16 and D=22 were the same single IVP. `generator` / `form_id` unstamped. No `spec_snapshot`. 40-seed counts: D=0 all poly; D=8 all exp; D=16/20/22 all homogeneous.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Solve }\frac{dy}{dx}=3x,\ y(0)=3.$ | $y=\frac{3}{2}x^2+3$ | poly; \(a\in\{1,2,3\}\), \(c_0\in\{1,\ldots,5\}\) |
| 0 | 7 | $\text{Solve }\frac{dy}{dx}=x,\ y(0)=5.$ | $y=\frac{1}{2}x^2+5$ | \(a=1\) |
| 0 | 1 | $\text{Solve }\frac{dy}{dx}=2x,\ y(0)=1.$ | $y=x^2+1$ | sibling-reported easy shape |
| 8 | 101 | $\text{Solve }\frac{dy}{dx}=4y,\ y(0)=3.$ | $y=3e^{4x}$ | `sep_exp`; exclusive (no poly leftover) |
| 8 | 207 | $\text{Solve }\frac{dy}{dx}=2y,\ y(0)=3.$ | $y=3e^{2x}$ | \(k\in\{2,3,4\}\) |
| 16 | 101 | $\text{Solve }\frac{dy}{dx}=\frac{y}{x}\text{ for }x>0,\ y(1)=4.$ | $y=4x$ | same IVP every seed |
| 22 | 101 | $\text{Solve }\frac{dy}{dx}=\frac{y}{x}\text{ for }x>0,\ y(1)=4.$ | $y=4x$ | D=22 == D=16 |

Opt-out flag used: _(none — live catalog is the old path)_

## Live now (`_generate_for_type`)

Leftover lockout on the same three builders. D=0 stays old poly. Gallery seeds 101/207/313 can collide on one form; rotation is across seeds.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Solve }\frac{dy}{dx}=x,\ y(0)=5.$ | $y=\frac{1}{2}x^2+5$ | `sep_poly` |
| 0 | 0 | $\text{Solve }\frac{dy}{dx}=2x,\ y(0)=1.$ | $y=x^2+1$ | old easy poly |
| 8 | 1 | $\text{Solve }\frac{dy}{dx}=x,\ y(0)=3.$ | $y=\frac{1}{2}x^2+3$ | poly leftover |
| 8 | 101 | $\text{Solve }\frac{dy}{dx}=2y,\ y(0)=5.$ | $y=5e^{2x}$ | exp |
| 16 | 1 | $\text{Solve }\frac{dy}{dx}=2y,\ y(0)=3.$ | $y=3e^{2x}$ | exp leftover |
| 16 | 101 | $\text{Solve }\frac{dy}{dx}=\frac{y}{x}\text{ for }x>0,\ y(1)=4.$ | $y=4x$ | no poly leftover |
| 22 | 0 | $\text{Solve }\frac{dy}{dx}=\frac{y}{x}\text{ for }x>0,\ y(1)=4.$ | $y=4x$ | homogeneous only |
| 22 | 101 | $\text{Solve }\frac{dy}{dx}=\frac{y}{x}\text{ for }x>0,\ y(1)=4.$ | $y=4x$ | homogeneous only |
| 22 | 207 | $\text{Solve }\frac{dy}{dx}=\frac{y}{x}\text{ for }x>0,\ y(1)=4.$ | $y=4x$ | frozen IVP |

40-seed counts **after**: D=0 poly only; D=8 poly leftover + exp (19/21); D=16 exp leftover + homogeneous (19/21, no poly); D=22 homogeneous only.

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 2 §4.3 Separable Equations | https://openstax.org/books/calculus-volume-2/pages/4-3-separable-equations | Separate \(g(x)\,dx = h(y)\,dy\), integrate, apply IVP; D=0 is \(\int ax\,dx\) (old easy) |
| Same §4.3 | same | Exponential \(y'=ky\); homogeneous \(y'=y/x\) (old mid / high). Mixes like \(x/y\), \((2x+3)y'=y\), logistic — **not this pass** (leave on LIMITATIONS) |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-2/` · Vol 2 Ch.4 not in `scripts/output/example_mining/calculus-volume-2/stage1/` (mining stops before DE). Learning-objective spine: `scripts/output/example_mining/progression/full_spine.md` (Vol 2 §4.3).

## Variety notes

Not a WP. D=0 one easy poly IVP (old). Same-D rotation at mid D: leftover \(dy/dx=ax\) vs \(ky\). High D homogeneous keeps the old single IVP \(y(1)=4\) (do not invent \(ky/x\)). Three old forms, so D=16 mixes exp leftover + homogeneous and D=22 is homogeneous-only.

## Limitations

- **Status:** shipped — leftover lockout of poly \(dy/dx=ax\). Remaining `LIMITATIONS`: homogeneous is one frozen IVP (\(y/x\), \(y(1)=4\)); no OpenStax mixes (\(x/y\), linear-in-\(x\) times \(y'\), logistic); no implicit \(\ln|y|\) answers beyond \(y=4x\); D=16 can still emit exp leftover (intentional).
- **Live pairwise:** each item stamps `form_id`, shared `generator=separable_diff_eq`, and `family`; copies `form_id` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `separable_diff_eq`

## Proposed engine (reuse vs new)

- **Reuse:** existing poly / exp / homogeneous builders (now in `calc_app_diff.py`). Depth = real structure (lock out \(dy/dx=ax\); mix leftover at D=8 / D=16) — not padded `difficulty_costs`.
- **Not this pass:** mixed \(g(x)h(y)\) cores; logistic; slope-field figures (other leaf).
