# Notes — `calc_app_diff_intervals_of_concavity` (`Intervals of concavity`)

- **Display name:** Intervals of concavity
- **Category:** Calculus — Applications of Differentiation
- **Generator:** `intervals_concavity`
- **Suggested family:** other (second-derivative sign chart on constructive polynomials)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Use the sign of \(f''\) to list concavity intervals (and the inflection point at high D).
- **D=0:** Odd power \(x^{3}\) or \(x^{5}\) on \((0,\infty)\) (old easy) — concave up.
- **Mid D (≈8):** Odd-power leftover still allowed, plus odd cubic \(x^{3}-3a^{2}x+c\) (same family as relative extrema; inflects at 0).
- **High D (≈16):** Lock out the odd-power ray. Odd-cubic leftover plus shifted cubics with inflection \(h\neq 0\) (Ex. 4.19 \(x^{3}-6x^{2}+9x+30\)).
- **Expert (≈22):** Lock out the inflect-at-0 leftover. Shifted cubics only.
- **Must not:** Wrong-topic first-derivative-only prompts; padded `difficulty_costs`; a general AST second-differentiator.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**. Pre-lockout: D≥8 was always the odd cubic, so high D **always inflected at 0**. `generator` was unstamped.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Determine the concavity of }f(x)=x^{3}\text{ on }(0,\infty).$ | $\text{concave up}$ | odd-power ray |
| 0 | 207 | $\text{Determine the concavity of }f(x)=x^{3}\text{ on }(0,\infty).$ | $\text{concave up}$ | same family |
| 8 | 101 | $\text{Find the intervals of concavity of }f(x)=x^{3}-12x-2.$ | $\text{concave down on }(-\infty,0);\text{ concave up on }(0,\infty)$ | inflect at 0 |
| 16 | 101 | $\text{Find the intervals of concavity of }f(x)=x^{3}-12x-2.$ | $\text{concave down on }(-\infty,0);\text{ concave up on }(0,\infty)$ | same as D=8 |
| 22 | 101 | $\text{Find the intervals of concavity of }f(x)=x^{3}-12x-2.$ | $\text{concave down on }(-\infty,0);\text{ concave up on }(0,\infty)$ | still inflect at 0 |
| 22 | 207 | $\text{Find the intervals of concavity of }f(x)=x^{3}-12x+1.$ | $\text{concave down on }(-\infty,0);\text{ concave up on }(0,\infty)$ | 40/40 seeds inflect at 0 |

Opt-out flag used: _(none — live catalog is the old path)_

## Live now (`_generate_for_type`)

Reuses the extrema cubic core (`_cubic_odd`) plus Ex. 4.19 shifted inflections. D=0 stays the old odd-power ray.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Determine the concavity of }f(x)=x^{3}\text{ on }(0,\infty).$ | $\text{concave up}$ | `odd_power_positive_ray` |
| 8 | 7 | $\text{Determine the concavity of }f(x)=x^{3}\text{ on }(0,\infty).$ | $\text{concave up}$ | odd-power leftover |
| 8 | 101 | $\text{Find the intervals of concavity of }f(x)=x^{3}-12x-2.$ | $\text{concave down on }(-\infty,0);\text{ concave up on }(0,\infty)$ | `cubic_second_derivative` |
| 16 | 7 | $\text{Find the intervals of concavity of }f(x)=x^{3}-12x+2.$ | $\text{concave down on }(-\infty,0);\text{ concave up on }(0,\infty)$ | inflect-at-0 leftover |
| 16 | 207 | $\text{Find the intervals of concavity of }f(x)=x^{3} - 9x^{2} + 9x + 1\text{ and the inflection point.}$ | $\text{concave down on }(-\infty,3);\text{ concave up on }(3,\infty);\text{ inflection at }x=3$ | `cubic_shifted_inflection` |
| 22 | 2 | $\text{Find the intervals of concavity of }f(x)=x^{3} - 12x^{2} - 9x\text{ and the inflection point.}$ | $\text{concave down on }(-\infty,4);\text{ concave up on }(4,\infty);\text{ inflection at }x=4$ | Ex. 4.19 shape |
| 22 | 101 | $\text{Find the intervals of concavity of }f(x)=-x^{3} - 6x^{2} + 9x - 1\text{ and the inflection point.}$ | $\text{concave down on }(-2,\infty);\text{ concave up on }(-\infty,-2);\text{ inflection at }x=-2$ | negative leading (Checkpoint 4.18 sign) |

40-seed counts **after**: D=0 ray-only; D=8 ray/odd-cubic; D=16 odd-cubic leftover + shifted (no ray); D=22 shifted only (0/40 inflect at 0).

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §4.5 | https://openstax.org/books/calculus-volume-1/pages/4-5-derivatives-and-the-shape-of-a-graph | Ex. 4.19 \(f(x)=x^{3}-6x^{2}+9x+30\) (inflect at 2); Checkpoint 4.18 negative cubic |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/4-5-derivatives-and-the-shape-of-a-graph.md`.

## Variety notes

Not a WP. D=0 one easy ray (old). Same-D rotation at mid D: ray leftover vs odd cubic. High D shifted integer inflections \(h\neq 0\), including leading-sign flip. Algebra shapes copy `_cubic_odd` plus \(f=\pm(x^{3}-3hx^{2})+bx+c\).

## Limitations

- **Status:** shipped — leftover lockout + Ex. 4.19 shifted inflections. Remaining `LIMITATIONS`: no quintic second-derivative test (Ex. 4.20 \(x^{5}-5x^{3}\)); no fractional-power concavity; D=16 can still emit the inflect-at-0 odd-cubic leftover (intentional, like increase/decrease).
- **Live pairwise:** each item stamps `form_id`, shared `generator=intervals_concavity`, and `family`; copies `form_id` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `intervals_concavity`

## Proposed engine (reuse vs new)

- **Reuse:** extrema polynomial families in `calc_app_diff.py` (`_cubic_odd` + odd-power ray). Depth = real structure (lock out inflect-at-0 leftovers; unlock shifted inflections) — not padded `difficulty_costs`.
- **Not this pass:** quintics; general computer-algebra sign charts.
