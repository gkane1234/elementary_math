# Notes — `pc_extrema_intervals_of_increase_and_decrease` (`Extrema, intervals of increase and decrease`)

- **Course:** Precalculus
- **Category:** Precalculus — Functions
- **Generator:** `pc_extrema_intervals`
- **Suggested family:** other

---

## What the question should look like (D=0 vs high D)

- **Skill:** Find extrema and intervals of increase for a quadratic.
- **D=0:** $ax^2$ with $a>0$, minimum at origin (OpenStax PC §1.3).
- **High D (≈16–22):** vertex form $a(x-h)^2+k$, including maxima ($a<0$).
- **Must not:** calculus derivative tests on this leaf.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with `pc_extrema_intervals`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\text{Find the extrema and intervals of increase for }f(x)=3x^2.$` | `$\text{minimum }0\text{ at }x=0;\ \text{increasing on }(0,\infty)$` | $ax^2$ |
| 8 | 101 | `$\text{Find the extrema and intervals of increase for }f(x)=-(x+1)^2.$` | `$\text{maximum }0\text{ at }x=-1;\ \text{increasing on }(-\infty,-1)$` | shifted max |
| 16 | 101 | `$\text{Find the extrema and intervals of increase for }f(x)=-(x+1)^2+1.$` | `$\text{maximum }1\text{ at }x=-1;\ \text{increasing on }(-\infty,-1)$` | vertex $+k$ |
| 22 | 101 | `$\text{Find the extrema and intervals of increase for }f(x)=-(x+1)^2+1.$` | `$\text{maximum }1\text{ at }x=-1;\ \text{increasing on }(-\infty,-1)$` | vertex $+k$ |

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Precalculus 2e §1.3 | https://openstax.org/books/precalculus-2e/pages/1-3-rates-of-change-and-behavior-of-graphs | local extrema + increasing intervals on quadratics |

## Proposed engine

- **Named:** `pc_extrema_intervals` — quadratic vertex / increase intervals.

## Limitations

- **Difficulty scaling:** Notes table shows stem changes with D at seed=101; confirm numeric hardness before format unlocks.
- **OpenStax:** Cite present; gold shapes in cite column — do not invent new algebra beyond old-path + cite.
- **Engine:** Live catalog generator; no deferred precalc_foundations stub (PC_DEFERRED empty).
- **This pass:** Gallery + Limitations audit only. Implement leftover only if notes lock gold (not for flat-D / red-header variety leaves).
