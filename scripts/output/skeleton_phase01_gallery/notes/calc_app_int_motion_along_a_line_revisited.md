# Notes — `calc_app_int_motion_along_a_line_revisited` (`Motion along a line revisited`)

- **Display name:** Motion along a line revisited
- **Category:** Calculus — Applications of Integration
- **Generator:** `motion_along_a_line_integral`
- **Suggested family:** other (net change / displacement from \(v(t)\))

---

## What the question should look like (D=0 vs high D)

- **Skill:** From a velocity \(v(t)\), find net displacement \(\int_a^b v(t)\,dt\) or (high D) total distance \(\int_a^b \lvert v\rvert\,dt\).
- **D=0:** Linear \(v(t)=2t\) on \([0,b]\) (old easy).
- **Mid D (≈8):** Linear leftover still allowed, plus constant \(v(t)=b\) (old exclusive mid).
- **High D (≈16):** Lock out linear leftover. Constant leftover plus sign-change displacement \(v(t)=2t-2c\) on \([0,2c]\) (net 0) plus total distance on the same \(v\).
- **Expert (≈22):** Total distance only on the existing sign-change \(v\).
- **Must not:** Generic \(\frac{d}{dx}\) dump; padded `difficulty_costs`; free-fall / piecewise / trig \(v(t)\); OpenStax \(v=3t-5\) nonzero net as a new \(v\).

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**, before leftover bands. Exclusive cliffs: D=0 always linear, D=8 always const, D≥16 always sign-change. D=16 and D=22 were the same. `generator` was unstamped on the `_framework` wrapper. No `spec_snapshot`. 40-seed counts: D=0 all `disp_linear_v`; D=8 all `disp_const_v`; D=16/22 all `disp_sign_change`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $v(t)=2t.\quad\text{Find the displacement from }t=0\text{ to }t=3.$ | $9$ | `disp_linear_v` |
| 0 | 7 | $v(t)=2t.\quad\text{Find the displacement from }t=0\text{ to }t=4.$ | $16$ | same \(v=2t\); \(b\) varies |
| 8 | 101 | $v(t)=3.\quad\text{Find the displacement from }t=0\text{ to }t=3.$ | $9$ | `disp_const_v`; exclusive (no linear leftover) |
| 8 | 7 | $v(t)=4.\quad\text{Find the displacement from }t=0\text{ to }t=4.$ | $16$ | still constant \(v=b\) |
| 16 | 101 | $v(t)=2t-6.\quad\text{Find the displacement from }t=0\text{ to }t=6.$ | $0$ | `disp_sign_change`; net 0 |
| 22 | 101 | $v(t)=2t-6.\quad\text{Find the displacement from }t=0\text{ to }t=6.$ | $0$ | same as D=16 |
| 22 | 7 | $v(t)=2t-2.\quad\text{Find the displacement from }t=0\text{ to }t=2.$ | $0$ | same family |

Opt-out flag used: _(none — live catalog is the old path)_

## Live now (`_generate_for_type`)

Leftover lockout on the same three \(v(t)\) builders, plus Ex. 5.25 / Ex. 225 total distance \(\int\lvert v\rvert\) on the existing sign-change \(v=2t-2c\). D=0 stays old linear. Gallery seeds 101/207/313 can collide on one form; rotation is across seeds.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $v(t)=2t.\quad\text{Find the displacement from }t=0\text{ to }t=3.$ | $9$ | `disp_linear_v` |
| 0 | 1 | $v(t)=2t.\quad\text{Find the displacement from }t=0\text{ to }t=2.$ | $4$ | old easy linear |
| 8 | 1 | $v(t)=2t.\quad\text{Find the displacement from }t=0\text{ to }t=2.$ | $4$ | linear leftover |
| 8 | 101 | $v(t)=3.\quad\text{Find the displacement from }t=0\text{ to }t=3.$ | $9$ | const leftover |
| 16 | 1 | $v(t)=2.\quad\text{Find the displacement from }t=0\text{ to }t=2.$ | $4$ | const leftover |
| 16 | 101 | $v(t)=2t-2.\quad\text{Find the displacement from }t=0\text{ to }t=2.$ | $0$ | sign-change leftover |
| 16 | 0 | $v(t)=2t-4.\quad\text{Find the total distance traveled from }t=0\text{ to }t=4.$ | $8$ | `disp_distance` (Ex. 5.25) |
| 22 | 0 | $v(t)=2t-4.\quad\text{Find the total distance traveled from }t=0\text{ to }t=4.$ | $8$ | `disp_distance` |
| 22 | 101 | $v(t)=2t-2.\quad\text{Find the total distance traveled from }t=0\text{ to }t=2.$ | $2$ | distance only |
| 22 | 207 | $v(t)=2t-6.\quad\text{Find the total distance traveled from }t=0\text{ to }t=6.$ | $18$ | Ex. 225 \(c=3\) |

40-seed counts **after**: D=0 linear only; D=8 linear leftover + const (19/21); D=16 const leftover + sign-change leftover + distance (14/15/11, no linear); D=22 distance only.

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §5.4 Example 5.24 | https://openstax.org/books/calculus-volume-1/pages/5-4-integration-formulas-and-the-net-change-theorem | Linear \(v(t)=3t-5\) on \([0,3]\); net displacement (nonzero) — **not this pass** (old sign-change sibling is \(v=2t-2c\), net 0) |
| OpenStax Calculus Volume 1 §5.4 Example 5.25 | same | Same \(v(t)\); **total distance** (absolute integral) — shipped on the existing sign-change \(v=2t-2c\) (`disp_distance`) |
| OpenStax Calculus Volume 1 §5.4 Exercise 223 / 225 | same | \(v(t)=4-2t\) on \([0,2]\); Ex. 225 \(v=\lvert 2t-6\rvert\) on \([0,6]\) is the same \(v\) with \(c=3\) |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/5-4-integration-formulas-and-the-net-change-theorem.md`.

## Variety notes

Not a WP. D=0 one easy linear \(v=2t\) (old). Same-D rotation at mid D: leftover linear vs const. High D sign-change keeps integer \(c\in\{1,2,3\}\) from the old builder; total distance is \(\int\lvert v\rvert=2c^{2}\) on that same \(v\). Old exclusive D=8 const is easier than D=0 linear (inverted exclusive cliff); leftover lockout still mixes it at D=8 as the old mid form and leftovers it at D=16.

## Limitations

- **Status:** shipped — leftover lockout of linear \(v=2t\) plus total distance \(\int\lvert v\rvert\) on the existing sign-change \(v\). Remaining `LIMITATIONS`: no OpenStax \(v=3t-5\) with nonzero net (Ex. 5.24); no quadratic \(v(t)=t^{2}-3t-18\) (Ex. 224); no free-fall / piecewise / trig; D=16 can still emit const leftover and net-0 displacement leftover (intentional; old mid is easier than linear).
- **Live pairwise:** each item stamps `form_id`, shared `generator=motion_along_a_line_integral`, and `family`; copies `form_id` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `motion_along_a_line_integral`

## Proposed engine (reuse vs new)

- **Reuse:** existing linear / const / sign-change \(v(t)\) builders in `calc_app_diff.py`. Distance is the same \(v=2t-2c\) with \(\int\lvert v\rvert=2c^{2}\) (Ex. 5.25 / Ex. 225). Depth = real structure (lock out \(v=2t\); unlock distance at high D) — not padded `difficulty_costs`.
- **Not this pass:** Ex. 5.24 nonzero net \(v=3t-5\); quadratic / exponential \(v(t)\); figure bank.
