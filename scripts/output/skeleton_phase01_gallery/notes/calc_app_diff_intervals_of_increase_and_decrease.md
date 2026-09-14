# Notes — `calc_app_diff_intervals_of_increase_and_decrease` (`Intervals of increase and decrease`)

- **Display name:** Intervals of increase and decrease
- **Category:** Calculus — Applications of Differentiation
- **Generator:** `intervals_increase_decrease`
- **Suggested family:** other (first-derivative sign chart on constructive polynomials)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Use the sign of \(f'\) to list increase/decrease intervals.
- **D=0:** Upward parabola \(x^{2}+bx+c\) (old easy) — increasing on \((-b/2,\infty)\).
- **Mid D (≈8):** Parabola leftover still allowed, plus odd cubic \(x^{3}-3a^{2}x+c\) (same family as relative extrema).
- **High D (≈16):** Lock out the parabola. Odd-cubic leftover plus shifted cubics with integer crits (Ex. 4.17 \(x^{3}-3x^{2}-9x\)).
- **Expert (≈22):** Lock out the odd-cubic leftover. Shifted cubics only.
- **Must not:** Wrong-topic extrema-only prompts with no interval answer; padded `difficulty_costs`; a general AST differentiator.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**. The old generator ignored D: every band was \(x^{2}+bx+c\), increasing only. No `form_id` / `generator` stamp.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find the intervals where } f(x) = x^{2} - 3x- 5 \text{ is increasing.}$ | $(1.5, \infty)$ | parabola only |
| 0 | 207 | $\text{Find the intervals where } f(x) = x^{2} + 3x- 3 \text{ is increasing.}$ | $(-1.5, \infty)$ | parabola only |
| 8 | 101 | $\text{Find the intervals where } f(x) = x^{2} + 7x- 4 \text{ is increasing.}$ | $(-3.5, \infty)$ | same family |
| 16 | 101 | $\text{Find the intervals where } f(x) = x^{2} + 3x- 3 \text{ is increasing.}$ | $(-1.5, \infty)$ | same family |
| 22 | 101 | $\text{Find the intervals where } f(x) = x^{2} + 2x+ 4 \text{ is increasing.}$ | $(-1, \infty)$ | same family |

Opt-out flag used: _(none — live catalog is the old path)_

## Live now (`_generate_for_type`)

Reuses the extrema cubic core (`_cubic_odd`) plus Ex. 4.17 shifted crits. D=0 stays the old parabola.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find the intervals where }f(x)=x^{2} - 2x + 3\text{ is increasing.}$ | $\left(1,\infty\right)$ | `parabola_increasing` |
| 8 | 7 | $\text{Find the intervals where }f(x)=x^{2} - 4x + 1\text{ is increasing.}$ | $\left(2,\infty\right)$ | parabola leftover |
| 8 | 2 | $\text{Find the intervals of increase and decrease of }f(x)=x^{3}-3x.$ | $\text{increasing on }(-\infty,-1)\cup(1,\infty);\text{ decreasing on }(-1,1)$ | `cubic_odd_sign_chart` |
| 16 | 7 | $\text{Find the intervals of increase and decrease of }f(x)=x^{3}-12x+2.$ | $\text{increasing on }(-\infty,-2)\cup(2,\infty);\text{ decreasing on }(-2,2)$ | odd-cubic leftover |
| 16 | 101 | $\text{Find the intervals of increase and decrease of }f(x)=x^{3} - 3x^{2} - 24x - 1.$ | $\text{increasing on }(-\infty,-2)\cup(4,\infty);\text{ decreasing on }(-2,4)$ | `cubic_shifted_sign_chart` |
| 22 | 2 | $\text{Find the intervals of increase and decrease of }f(x)=x^{3} - 3x^{2} - 9x.$ | $\text{increasing on }(-\infty,-1)\cup(3,\infty);\text{ decreasing on }(-1,3)$ | Ex. 4.17 shape |

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §4.5 | https://openstax.org/books/calculus-volume-1/pages/4-5-derivatives-and-the-shape-of-a-graph | Sign chart of \(f'\); Ex. 4.17 \(f(x)=x^{3}-3x^{2}-9x-1\) (crits \(-1,3\)); Checkpoint 4.16 another cubic |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/4-5-derivatives-and-the-shape-of-a-graph.md`.

## Variety notes

Not a WP. D=0 one easy parabola (old). Same-D rotation at mid D: parabola leftover vs odd cubic. High D shifted integer-crit cubics. Algebra shapes copy the existing `_cubic_odd` extrema family; shifted cubics keep \(p+q\) even so coefficients stay integers.

## Limitations

- **Status:** shipped — leftover lockout + Ex. 4.17 cubics. Remaining `LIMITATIONS`: no fractional-power first-derivative test (Ex. 4.18 \(5x^{1/3}-x^{5/3}\)); no cube-root kink (Checkpoint 4.17); no asking decrease-only on the D=0 parabola.
- **Live pairwise:** each item stamps `form_id`, shared `generator=intervals_increase_decrease`, and `family`; copies `form_id` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `intervals_increase_decrease`

## Proposed engine (reuse vs new)

- **Reuse:** extrema polynomial families in `calc_app_diff.py` (`_cubic_odd` + parabola). Depth = real structure (lock out parabola leftovers; unlock shifted cubics) — not padded `difficulty_costs`.
- **Not this pass:** fractional powers; general computer-algebra sign charts.
