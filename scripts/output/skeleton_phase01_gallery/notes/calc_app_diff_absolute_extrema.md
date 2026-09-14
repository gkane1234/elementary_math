# Notes — `calc_app_diff_absolute_extrema` (`Absolute extrema`)

- **Display name:** Absolute extrema
- **Category:** Calculus — Applications of Differentiation
- **Generator:** `absolute_extrema`
- **Suggested family:** other (closed-interval EVT on constructive polynomials)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Locate absolute max/min on a closed interval by comparing critical points and endpoints.
- **D=0:** Parabola \(x^{2}\) on \([0,b]\) (old easy) — vertex at the left endpoint.
- **Mid D (≈8):** Parabola leftover still allowed, plus odd cubic \(x^{3}-3a^{2}x+c\) on \([-2a,2a]\) (crits at \(\pm a\)).
- **High D (≈16):** Lock out the parabola. Odd-cubic leftover plus shifted cubics with integer crits (Ex. 4.17 \(x^{3}-3x^{2}-9x\)) on an interval that contains both crits and pads one side so an endpoint wins.
- **Expert (≈22):** Lock out the odd-cubic leftover. Shifted cubics only.
- **Must not:** Relative-extrema stems (no interval); padded `difficulty_costs`; fractional-power EVT this pass (Ex. 4.13 \(x^{2}-3x^{2/3}\)); diagrams / figure bank.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**, before leftover lockout. D≥8 was always the odd cubic \(x^{3}-3a^{2}x+c\) on \([-2a,2a]\), so high D **always had crits at \(\pm a\)**. `generator` was unstamped on the `_framework` wrapper.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find the absolute extrema of }f(x)=x^{2}\text{ on }[0,3].$ | $\text{abs min }0\text{ at }x=0;\text{ abs max }9\text{ at }x=3$ | parabola, vertex at endpoint |
| 0 | 207 | $\text{Find the absolute extrema of }f(x)=x^{2}\text{ on }[0,3].$ | $\text{abs min }0\text{ at }x=0;\text{ abs max }9\text{ at }x=3$ | parabola |
| 8 | 101 | $\text{Find the absolute extrema of }f(x)=x^{3}-12x-2\text{ on }[-4,4].$ | $\text{abs min }-18\text{ at }x=-4;\text{ abs max }14\text{ at }x=-2$ | crits \(\pm 2\); endpoint = local min |
| 16 | 101 | $\text{Find the absolute extrema of }f(x)=x^{3}-12x-2\text{ on }[-4,4].$ | $\text{abs min }-18\text{ at }x=-4;\text{ abs max }14\text{ at }x=-2$ | still \(\pm a\) |
| 22 | 101 | $\text{Find the absolute extrema of }f(x)=x^{3}-12x-2\text{ on }[-4,4].$ | $\text{abs min }-18\text{ at }x=-4;\text{ abs max }14\text{ at }x=-2$ | still \(\pm a\) |

Opt-out flag used: _(none — live catalog is the old path)_

## Live now (`_generate_for_type`)

Leftover lockout + Ex. 4.17 shifted crits on the same cubic core (`_cubic_odd` leftover on \([-2a,2a]\); `_shifted_cubic_integer_crits` for high D, interval padded so one endpoint strictly beats the matching local extremum). D=0 stays the old \(x^{2}\) on \([0,b]\).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find the absolute extrema of }f(x)=x^{2}\text{ on }[0,3].$ | $\text{abs min }0\text{ at }x=0;\text{ abs max }9\text{ at }x=3$ | `closed_interval_parabola` |
| 8 | 7 | $\text{Find the absolute extrema of }f(x)=x^{2}\text{ on }[0,3].$ | $\text{abs min }0\text{ at }x=0;\text{ abs max }9\text{ at }x=3$ | parabola leftover |
| 8 | 101 | $\text{Find the absolute extrema of }f(x)=x^{3}-12x-2\text{ on }[-4,4].$ | $\text{abs min }-18\text{ at }x=-4;\text{ abs max }14\text{ at }x=-2$ | odd-cubic leftover |
| 16 | 7 | $\text{Find the absolute extrema of }f(x)=x^{3}-12x+2\text{ on }[-4,4].$ | $\text{abs min }-14\text{ at }x=-4;\text{ abs max }18\text{ at }x=-2$ | odd-cubic leftover |
| 16 | 101 | $\text{Find the absolute extrema of }f(x)=x^{3} - 3x^{2} - 24x - 1\text{ on }[-3,8].$ | $\text{abs min }-81\text{ at }x=4;\text{ abs max }127\text{ at }x=8$ | `closed_interval_shifted_cubic`; abs max at endpoint |
| 22 | 2 | $\text{Find the absolute extrema of }f(x)=x^{3} - 3x^{2} - 9x\text{ on }[-4,4].$ | $\text{abs min }-76\text{ at }x=-4;\text{ abs max }5\text{ at }x=-1$ | Ex. 4.17 shape; abs min at endpoint |
| 22 | 101 | $\text{Find the absolute extrema of }f(x)=x^{3} - 3x^{2} - 24x - 1\text{ on }[-3,8].$ | $\text{abs min }-81\text{ at }x=4;\text{ abs max }127\text{ at }x=8$ | shifted only |

40-seed counts **after**: D=0 parabola-only; D=8 parabola leftover + odd cubic; D=16 odd-cubic leftover + shifted (no parabola); D=22 shifted only (0/40 crits at \(\pm a\)).

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §4.3 | https://openstax.org/books/calculus-volume-1/pages/4-3-maxima-and-minima | EVT / closed-interval method: compare crits and endpoints |
| OpenStax Calculus Volume 1 §4.3 Ex. 4.13 | same | Downward parabola on \([1,3]\); fractional-power \(x^{2}-3x^{2/3}\) on \([0,2]\) (deferred) |
| OpenStax Calculus Volume 1 §4.3 Checkpoint 4.13 | same | \(x^{2}-4x+3\) on \([1,4]\) — vertex inside; D=0 keeps the easier old \(x^{2}\) on \([0,b]\) |
| OpenStax Calculus Volume 1 §4.5 Ex. 4.17 | https://openstax.org/books/calculus-volume-1/pages/4-5-derivatives-and-the-shape-of-a-graph | Shifted cubic \(x^{3}-3x^{2}-9x-1\) (crits \(-1,3\)) reused on a closed interval |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/4-3-maxima-and-minima.md`.

## Variety notes

Not a WP. D=0 one easy parabola on an interval (old). Same-D rotation at mid D: parabola leftover vs odd cubic. High D shifted integer-crit cubics with an asymmetric pad so the closed-interval method is not interior-only. Algebra shapes copy the existing `_cubic_odd` extrema family; shifted cubics keep \(p+q\) even so coefficients stay integers (same helper as relative extrema).

## Limitations

- **Status:** shipped — leftover lockout + Ex. 4.17 cubics on a closed interval. Remaining `LIMITATIONS`: no fractional-power EVT (Ex. 4.13 \(x^{2}-3x^{2/3}\), kink where \(f'\) is undefined); no downward-parabola Checkpoint 4.13 as a separate D=0 form (old easy is \(x^{2}\) on \([0,b]\)); odd-cubic leftover on \([-2a,2a]\) still ties endpoint = local min (report one location); D=16 can still emit the odd-cubic leftover (intentional, like relative extrema).
- **Live pairwise:** each item stamps `form_id`, shared `generator=absolute_extrema`, and `family`; copies `form_id` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `absolute_extrema`

## Proposed engine (reuse vs new)

- **Reuse:** extrema polynomial families in `calc_app_diff.py` (`_cubic_odd` + parabola + `_shifted_cubic_integer_crits`) evaluated at endpoints and interior crits. Depth = real structure (lock out \(\pm a\) leftovers; unlock shifted cubics on a closed interval) — not padded `difficulty_costs`.
- **Not this pass:** fractional powers; diagrams / figure bank; relative-extrema stems.
