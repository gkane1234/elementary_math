# Notes — `calc_app_diff_relative_extrema` (`Relative extrema`)

- **Display name:** Relative extrema
- **Category:** Calculus — Applications of Differentiation
- **Generator:** `relative_extrema`
- **Suggested family:** other (first-derivative test on constructive polynomials)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Locate relative max/min via vertex or first-derivative test.
- **D=0:** Parabola \((x-h)^{2}-k\) (old easy) — relative minimum at the vertex.
- **Mid D (≈8):** Parabola leftover still allowed, plus odd cubic \(x^{3}-3a^{2}x+c\) (crits at \(\pm a\)).
- **High D (≈16):** Lock out the parabola. Odd-cubic leftover plus shifted cubics with integer crits (Ex. 4.17 \(x^{3}-3x^{2}-9x\)).
- **Expert (≈22):** Lock out the odd-cubic leftover. Shifted cubics only.
- **Must not:** Closed-interval absolute extrema; padded `difficulty_costs`; a general AST differentiator; fractional-power first-derivative test this pass.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**, before leftover lockout. D≥8 was always the odd cubic \(x^{3}-3a^{2}x+c\), so high D **always had crits at \(\pm a\)**. `generator` was unstamped on the `_framework` wrapper.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find the relative minimum of }f(x)=(x-5)^{2}-2.$ | $\text{relative minimum }-2\text{ at }x=5$ | parabola vertex |
| 0 | 207 | $\text{Find the relative minimum of }f(x)=(x-5)^{2}-6.$ | $\text{relative minimum }-6\text{ at }x=5$ | parabola vertex |
| 8 | 101 | $\text{Find the relative extrema of }f(x)=x^{3}-12x-2.$ | $\text{rel max }14\text{ at }x=-2;\text{ rel min }-18\text{ at }x=2$ | crits \(\pm 2\) |
| 16 | 101 | $\text{Find the relative extrema of }f(x)=x^{3}-12x-2.$ | $\text{rel max }14\text{ at }x=-2;\text{ rel min }-18\text{ at }x=2$ | still \(\pm a\) |
| 22 | 101 | $\text{Find the relative extrema of }f(x)=x^{3}-12x-2.$ | $\text{rel max }14\text{ at }x=-2;\text{ rel min }-18\text{ at }x=2$ | still \(\pm a\) |

Opt-out flag used: _(none — live catalog is the old path)_

## Live now (`_generate_for_type`)

Leftover lockout + Ex. 4.17 shifted crits on the same cubic core (`_cubic_odd` leftover; `_shifted_cubic_integer_crits` for high D). D=0 stays the old vertex parabola.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find the relative minimum of }f(x)=(x-2)^{2}-5.$ | $\text{relative minimum }-5\text{ at }x=2$ | `parabola_vertex` |
| 8 | 7 | $\text{Find the relative minimum of }f(x)=(x-2)^{2}-4.$ | $\text{relative minimum }-4\text{ at }x=2$ | parabola leftover |
| 8 | 101 | $\text{Find the relative extrema of }f(x)=x^{3}-12x-2.$ | $\text{rel max }14\text{ at }x=-2;\text{ rel min }-18\text{ at }x=2$ | odd-cubic leftover |
| 16 | 7 | $\text{Find the relative extrema of }f(x)=x^{3}-12x+2.$ | $\text{rel max }18\text{ at }x=-2;\text{ rel min }-14\text{ at }x=2$ | odd-cubic leftover |
| 16 | 101 | $\text{Find the relative extrema of }f(x)=x^{3} - 3x^{2} - 24x - 1.$ | $\text{rel max }27\text{ at }x=-2;\text{ rel min }-81\text{ at }x=4$ | `cubic_shifted_extrema` |
| 22 | 2 | $\text{Find the relative extrema of }f(x)=x^{3} - 3x^{2} - 9x.$ | $\text{rel max }5\text{ at }x=-1;\text{ rel min }-27\text{ at }x=3$ | Ex. 4.17 shape |
| 22 | 101 | $\text{Find the relative extrema of }f(x)=x^{3} - 3x^{2} - 24x - 1.$ | $\text{rel max }27\text{ at }x=-2;\text{ rel min }-81\text{ at }x=4$ | shifted only |

40-seed counts **after**: D=0 parabola-only; D=8 parabola leftover + odd cubic; D=16 odd-cubic leftover + shifted (no parabola); D=22 shifted only (0/40 crits at \(\pm a\)).

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §4.3 | https://openstax.org/books/calculus-volume-1/pages/4-3-maxima-and-minima | Critical points; relative vs absolute (this leaf is relative only) |
| OpenStax Calculus Volume 1 §4.5 | https://openstax.org/books/calculus-volume-1/pages/4-5-derivatives-and-the-shape-of-a-graph | First-derivative test; Ex. 4.17 \(f(x)=x^{3}-3x^{2}-9x-1\) (crits \(-1,3\)); Checkpoint 4.16 another cubic |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/4-5-derivatives-and-the-shape-of-a-graph.md`.

## Variety notes

Not a WP. D=0 one easy vertex parabola (old). Same-D rotation at mid D: parabola leftover vs odd cubic. High D shifted integer-crit cubics. Algebra shapes copy the existing `_cubic_odd` extrema family; shifted cubics keep \(p+q\) even so coefficients stay integers (same helper as increase/decrease).

## Limitations

- **Status:** shipped — leftover lockout + Ex. 4.17 cubics. Remaining `LIMITATIONS`: no fractional-power first-derivative test (Ex. 4.18 \(5x^{1/3}-x^{5/3}\)); no cube-root kink (Checkpoint 4.17); no leading-negative Checkpoint 4.16 cubic; D=16 can still emit the odd-cubic leftover (intentional, like increase/decrease).
- **Live pairwise:** each item stamps `form_id`, shared `generator=relative_extrema`, and `family`; copies `form_id` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `relative_extrema`

## Proposed engine (reuse vs new)

- **Reuse:** extrema polynomial families in `calc_app_diff.py` (`_cubic_odd` + parabola + `_shifted_cubic_integer_crits`). Depth = real structure (lock out \(\pm a\) leftovers; unlock shifted cubics) — not padded `difficulty_costs`.
- **Not this pass:** fractional powers; leading-negative cubics; closed-interval absolute extrema (sibling leaf).
