# Notes — `calc_app_diff_curve_sketching` (`Curve sketching`)

- **Display name:** Curve sketching
- **Category:** Calculus — Applications of Differentiation
- **Generator:** `curve_sketching`
- **Suggested family:** other (checklist of vertex / extrema / inflection — not a drawn graph)

---

## What the question should look like (D=0 vs high D)

- **Skill:** List the features needed to sketch \(f\) (vertex, relative extrema, inflection).
- **D=0:** Shifted parabola \(f(x)=(x-h)^{2}\) (old easy) — vertex and concavity.
- **Mid D (≈8):** Parabola leftover still allowed, plus odd cubic \(x^{3}-3a^{2}x+c\) (same family as relative extrema; inflects at 0).
- **High D (≈16):** Lock out the parabola. Odd-cubic leftover plus a horizontal translate of that cubic so the inflection is at \(h\neq 0\) (same shifted-inflection idea as Ex. 4.19).
- **Expert (≈22):** Lock out the inflect-at-0 leftover. Shifted cubics only.
- **Must not:** A drawn graph / SVG; padded `difficulty_costs`; high D still inflecting at 0.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**. D≥8 was always the odd cubic, so high D **always inflected at 0**. `generator` was unstamped on the `_framework` wrapper.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{For }f(x)=(x-2)^{2},\text{ list the vertex and concavity.}$ | $\text{vertex }(2,0);\text{ concave up}$ | parabola |
| 8 | 101 | $\text{For }f(x)=x^{3}-12x-2,\text{ list relative extrema and the inflection point.}$ | $\text{rel max }14\text{ at }x=-2;\text{ rel min }-18\text{ at }x=2;\text{ inflection at }x=0$ | inflect at 0 |
| 16 | 101 | $\text{For }f(x)=x^{3}-12x-2,\text{ list relative extrema and the inflection point.}$ | $\text{rel max }14\text{ at }x=-2;\text{ rel min }-18\text{ at }x=2;\text{ inflection at }x=0$ | still inflect at 0 |
| 22 | 101 | $\text{For }f(x)=x^{3}-12x-2,\text{ list relative extrema and the inflection point.}$ | $\text{rel max }14\text{ at }x=-2;\text{ rel min }-18\text{ at }x=2;\text{ inflection at }x=0$ | still inflect at 0 |

Opt-out flag used: _(none — live catalog is the old path)_

## Live now (`_generate_for_type`)

Leftover lockout + translate of `_cubic_odd` so \(f''=0\) at \(h\neq 0\). Extrema y-values stay \(2a^{3}+k\) / \(-2a^{3}+k\); x-locations shift to \(h\pm a\).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{For }f(x)=(x-2)^{2},\text{ list the vertex and concavity.}$ | $\text{vertex }(2,0);\text{ concave up}$ | `parabola_sketch` |
| 8 | 7 | $\text{For }f(x)=(x-2)^{2},\text{ list the vertex and concavity.}$ | $\text{vertex }(2,0);\text{ concave up}$ | parabola leftover |
| 8 | 101 | $\text{For }f(x)=x^{3}-12x-2,\text{ list relative extrema and the inflection point.}$ | $\text{rel max }14\text{ at }x=-2;\text{ rel min }-18\text{ at }x=2;\text{ inflection at }x=0$ | inflect-at-0 leftover |
| 16 | 7 | $\text{For }f(x)=x^{3}-12x+2,\text{ list relative extrema and the inflection point.}$ | $\text{rel max }18\text{ at }x=-2;\text{ rel min }-14\text{ at }x=2;\text{ inflection at }x=0$ | inflect-at-0 leftover |
| 16 | 101 | $\text{For }f(x)=x^{3} + 3x^{2} - 9x - 13,\text{ list relative extrema and the inflection point.}$ | $\text{rel max }14\text{ at }x=-3;\text{ rel min }-18\text{ at }x=1;\text{ inflection at }x=-1$ | `cubic_shifted_sketch` |
| 22 | 101 | $\text{For }f(x)=x^{3} + 3x^{2} - 9x - 13,\text{ list relative extrema and the inflection point.}$ | $\text{rel max }14\text{ at }x=-3;\text{ rel min }-18\text{ at }x=1;\text{ inflection at }x=-1$ | shifted only |
| 22 | 7 | $\text{For }f(x)=x^{3} - 9x^{2} + 15x + 11,\text{ list relative extrema and the inflection point.}$ | $\text{rel max }18\text{ at }x=1;\text{ rel min }-14\text{ at }x=5;\text{ inflection at }x=3$ | Ex. 4.19-style \(h\neq 0\) |

40-seed counts **after**: D=0 parabola-only; D=8 parabola leftover + odd cubic; D=16 odd-cubic leftover + shifted (no parabola); D=22 shifted only (0/40 inflect at 0).

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §4.5 | https://openstax.org/books/calculus-volume-1/pages/4-5-derivatives-and-the-shape-of-a-graph | Combine extrema + concavity / inflection (Ex. 4.19 shifted cubic) into a sketch checklist |
| OpenStax Calculus Volume 1 §4.6 | https://openstax.org/books/calculus-volume-1/pages/4-6-limits-at-infinity-and-asymptotes | End behavior / HA–VA — not on this checklist yet |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/4-5-derivatives-and-the-shape-of-a-graph.md`.

## Variety notes

Not a WP. D=0 one easy parabola. Same-D rotation at mid D: parabola leftover vs odd cubic. High D is a translate of the existing `_cubic_odd` sketching core (integer inflection \(h\neq 0\)). Algebra shapes copy `_cubic_odd`; shift is \(f(x)=(x-h)^{3}-3a^{2}(x-h)+k\).

## Limitations

- **Status:** shipped — leftover lockout + shifted inflections. Remaining `LIMITATIONS`: no SVG / drawn graph; no asymptotes / end behavior (§4.6); no intercepts-and-holes checklist; D=16 can still emit the inflect-at-0 leftover (intentional, like concavity).
- **Live pairwise:** each item stamps `form_id`, shared `generator=curve_sketching`, and `family`; copies `form_id` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `curve_sketching`

## Proposed engine (reuse vs new)

- **Reuse:** existing parabola + `_cubic_odd` sketching core; same shifted-inflection idea as concavity Ex. 4.19. Depth = real structure (lock out inflect-at-0 leftovers; unlock \(h\neq 0\)) — not padded `difficulty_costs`.
- **Not this pass:** drawn graphs; rational sketches with VA/HA.
