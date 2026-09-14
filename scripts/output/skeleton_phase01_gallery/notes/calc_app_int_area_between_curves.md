# Notes — `calc_app_int_area_between_curves` (`Area between curves`)

- **Display name:** Area between curves
- **Category:** Calculus — Applications of Integration
- **Generator:** `area_between_curves`
- **Suggested family:** other (∫(top−bottom); no figure bank)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Find the area of the region between two graphs via \(\int(\text{top}-\text{bottom})\,dx\).
- **D=0:** Linear leftover \(y=x\) vs \(y=0\) on \([0,b]\) (old easy triangle).
- **Mid D (≈8):** \(y=x\) leftover still allowed, plus \(y=x^{2}\) vs \(y=0\), bounded \(y=k,\,y=x,\,x=0\), and leftover \(y=k-x\) vs \(y=0\) (old hard-band triangle, demoted).
- **High D (≈16):** Lock out both axis-triangles (\(y=x\) vs \(0\), \(y=k-x\) vs \(0\)). Leftover \(x^{2}\) vs \(0\) and \(y=k,\,y=x,\,x=0\), plus two-curve \(y=x\) vs \(y=x^{2}\).
- **Expert (≈22):** \(y=x\) vs \(y=x^{2}\) only.
- **Must not:** padded `difficulty_costs`; new cores (OpenStax Ex. 6.1 two-line with unequal slopes, Ex. 6.2 parabola-vs-line, \(x^4\), \(\sin/\cos\) crossing, \(dy\), start at \(a\neq 0\)).

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**, before leftover bands. Exclusive cliffs (`if band == easy/medium/hard`), so high D never mixed D=0 leftover — it mixed the two-curve with a D=0-easy triangle \(y=k-x\) vs \(y=0\). `generator` / `form_id` unstamped. No `spec_snapshot`. 40-seed counts: D=0 all \(y=x\) vs \(0\); D=8 exclusive \(x^{2}\) vs \(0\) (20) + \(y=k,\,y=x,\,x=0\) (20); D=16 \(y=x\) vs \(x^{2}\) (18) + \(y=k-x\) vs \(0\) (22); D=22 still \(y=k-x\) vs \(0\) (16) + two-curve (24).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find the area between }y=x\text{ and }y=0\text{ from }x=0\text{ to }x=3.$ | $\frac{9}{2}$ | \(y=x\) vs \(0\) only |
| 0 | 0 | $\text{Find the area between }y=x\text{ and }y=0\text{ from }x=0\text{ to }x=2.$ | $2$ | \(b\in\{2,3,\ldots\}\) |
| 8 | 101 | $\text{Find the area between }y=x^{2}\text{ and }y=0\text{ from }x=0\text{ to }x=2.$ | $\frac{8}{3}$ | \(x^{2}\) vs \(0\) (exclusive cliff, no leftover \(y=x\)) |
| 8 | 1 | $\text{Find the area of the region bounded by }y=3,\ y=x,\text{ and }x=0.$ | $\frac{9}{2}$ | three-line triangle |
| 16 | 101 | $\text{Find the area of the region bounded by }y=x\text{ and }y=x^{2}.$ | $\frac{1}{6}$ | true two-curve |
| 16 | 0 | $\text{Find the area between }y=4-x\text{ and }y=0\text{ from }x=0\text{ to }x=4.$ | $8$ | D=0-easy triangle in the hard band |
| 22 | 207 | $\text{Find the area between }y=4-x\text{ and }y=0\text{ from }x=0\text{ to }x=4.$ | $8$ | \(y=k-x\) leftover at expert |
| 22 | 7 | $\text{Find the area of the region bounded by }y=x\text{ and }y=x^{2}.$ | $\frac{1}{6}$ | two-curve |

Opt-out flag used: _(none — live catalog is the old path)_

## Live now (`_generate_for_type`)

Leftover lockout on the same five builders. D=0 stays old \(y=x\) vs \(0\). Gallery seeds 101/207/313 can collide on one form at mid D; rotation is across seeds.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{Find the area between }y=x\text{ and }y=0\text{ from }x=0\text{ to }x=2.$ | $2$ | `abc_linear_axis` |
| 0 | 0 | $\text{Find the area between }y=x\text{ and }y=0\text{ from }x=0\text{ to }x=3.$ | $\frac{9}{2}$ | old easy |
| 8 | 1 | $\text{Find the area between }y=x\text{ and }y=0\text{ from }x=0\text{ to }x=2.$ | $2$ | \(y=x\) leftover |
| 8 | 7 | $\text{Find the area between }y=x^{2}\text{ and }y=0\text{ from }x=0\text{ to }x=3.$ | $9$ | `abc_quad_axis` |
| 8 | 101 | $\text{Find the area of the region bounded by }y=3,\ y=x,\text{ and }x=0.$ | $\frac{9}{2}$ | `abc_hline_linear` |
| 8 | 0 | $\text{Find the area between }y=3-x\text{ and }y=0\text{ from }x=0\text{ to }x=3.$ | $\frac{9}{2}$ | `abc_diag_axis` leftover (not at D=16+) |
| 16 | 1 | $\text{Find the area between }y=x^{2}\text{ and }y=0\text{ from }x=0\text{ to }x=2.$ | $\frac{8}{3}$ | \(x^{2}\) leftover |
| 16 | 0 | $\text{Find the area of the region bounded by }y=x\text{ and }y=x^{2}.$ | $\frac{1}{6}$ | no axis-triangle leftover |
| 22 | 101 | $\text{Find the area of the region bounded by }y=x\text{ and }y=x^{2}.$ | $\frac{1}{6}$ | `abc_linear_quad` only |
| 22 | 207 | $\text{Find the area of the region bounded by }y=x\text{ and }y=x^{2}.$ | $\frac{1}{6}$ | `abc_linear_quad` only |

40-seed counts **after**: D=0 `abc_linear_axis` only; D=8 leftover mix `abc_linear_axis` + `abc_quad_axis` + `abc_hline_linear` + `abc_diag_axis` (11/8/14/7); D=16 leftover `abc_quad_axis` + `abc_hline_linear` + `abc_linear_quad` (14/15/11, no axis-triangles); D=22 `abc_linear_quad` only.

## OpenStax examples + chapter/section cites

Paraphrase stems; cite Calculus Volume 1 + URL. Do not dump copyrighted text wholesale.

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §6.1 Areas Between Curves | https://openstax.org/books/calculus-volume-1/pages/6-1-areas-between-curves | \(\int(\text{top}-\text{bottom})\,dx\) (or \(dy\)); region bounded by two graphs |
| OpenStax Calculus Volume 1 §6.1 Example 6.1 | https://openstax.org/books/calculus-volume-1/pages/6-1-areas-between-curves | Two lines on a closed interval (not invented here — old path has no unequal-slope pair) |
| OpenStax Calculus Volume 1 §6.1 Example 6.2 | https://openstax.org/books/calculus-volume-1/pages/6-1-areas-between-curves | Parabola above a line (not invented here) |
| OpenStax Calculus Volume 1 §6.1 Checkpoint 6.2 | https://openstax.org/books/calculus-volume-1/pages/6-1-areas-between-curves | \(y=x\) vs \(y=x^{4}\) — old path is \(y=x\) vs \(y=x^{2}\) (copy that shape, do not invent \(x^{4}\)) |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/` (6-1).

## Variety notes

Not a WP. D=0 one easy triangle \(y=x\) vs \(y=0\) (old). Same-D rotation at mid D: leftover axis-triangles vs \(x^{2}\) vs \(0\) vs three-line region. High D keeps the old two-curve \(y=x\) vs \(y=x^{2}\) (do not invent Ex. 6.1/6.2 / \(\sin x\)). Five old forms, so D=16 mixes mid leftover + two-curve and D=22 is two-curve-only.

## Limitations

- **Status:** shipped — leftover lockout of exclusive cliffs and of \(y=k-x\) vs \(y=0\) at expert. Remaining `LIMITATIONS`: five frozen old builders (no Ex. 6.1 two-line, no Ex. 6.2 parabola-vs-line, no \(x^{4}\), no \(\sin/\cos\) crossing, no \(dy\), no \(a\neq 0\)); no figure / shaded region; D=16 can still emit \(x^{2}\) vs \(0\) and three-line triangle leftover (intentional); D=22 is frozen \(y=x\) vs \(y=x^{2}\) (answer always \(\frac{1}{6}\)).
- **Live pairwise:** each item stamps `form_id`, shared `generator=area_between_curves`, and `family`; copies `form_id` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `area_between_curves`

## Proposed engine (reuse vs new)

- **Reuse:** existing linear-vs-axis / quad-vs-axis / three-line / diag-vs-axis / linear-vs-quad builders (now in `calc_app_diff.py`). Depth = real structure (lock out axis-triangles; mix leftover at D=8 / D=16) — not padded `difficulty_costs`.
- **Not this pass:** OpenStax Ex. 6.1/6.2 cores; \(dy\); crossing / compound regions; shaded SVG.
