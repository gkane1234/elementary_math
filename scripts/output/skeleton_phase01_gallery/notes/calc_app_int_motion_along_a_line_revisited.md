# Notes — `calc_app_int_motion_along_a_line_revisited` (`Motion along a line revisited`)

- **Display name:** Motion along a line revisited
- **Category:** Calculus — Applications of Integration
- **Generator:** `motion_along_a_line_integral`
- **Suggested family:** other (net change / displacement from \(v(t)\))

---

## What the question should look like (D=0 vs high D)

- **Skill:** From a velocity \(v(t)\), find net displacement \(\int_a^b v(t)\,dt\) (FTC / net change).
- **D=0:** Linear \(v(t)=2t\) on \([0,b]\) (old easy).
- **Mid D (≈8):** Linear leftover still allowed, plus constant \(v(t)=b\) (old exclusive mid).
- **High D (≈16):** Lock out linear leftover. Constant leftover plus sign-change \(v(t)=2t-2c\) on \([0,2c]\) (net 0).
- **Expert (≈22):** Lock out all leftovers. Sign-change only.
- **Must not:** Generic \(\frac{d}{dx}\) dump; padded `difficulty_costs`; distance traveled / \(|v|\) this pass; free-fall / piecewise / trig \(v(t)\).

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

Leftover lockout on the same three \(v(t)\) builders. D=0 stays old linear. Gallery seeds 101/207/313 can collide on one form; rotation is across seeds.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $v(t)=2t.\quad\text{Find the displacement from }t=0\text{ to }t=3.$ | $9$ | `disp_linear_v` |
| 0 | 1 | $v(t)=2t.\quad\text{Find the displacement from }t=0\text{ to }t=2.$ | $4$ | old easy linear |
| 8 | 1 | $v(t)=2t.\quad\text{Find the displacement from }t=0\text{ to }t=2.$ | $4$ | linear leftover |
| 8 | 101 | $v(t)=3.\quad\text{Find the displacement from }t=0\text{ to }t=3.$ | $9$ | const leftover |
| 16 | 1 | $v(t)=2.\quad\text{Find the displacement from }t=0\text{ to }t=2.$ | $4$ | const leftover |
| 16 | 101 | $v(t)=2t-2.\quad\text{Find the displacement from }t=0\text{ to }t=2.$ | $0$ | sign-change |
| 22 | 0 | $v(t)=2t-4.\quad\text{Find the displacement from }t=0\text{ to }t=4.$ | $0$ | sign-change |
| 22 | 101 | $v(t)=2t-2.\quad\text{Find the displacement from }t=0\text{ to }t=2.$ | $0$ | sign-change only |
| 22 | 207 | $v(t)=2t-6.\quad\text{Find the displacement from }t=0\text{ to }t=6.$ | $0$ | sign-change |

40-seed counts **after**: D=0 linear only; D=8 linear leftover + const (19/21); D=16 const leftover + sign-change (19/21, no linear); D=22 sign-change only.

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §5.4 Example 5.24 | https://openstax.org/books/calculus-volume-1/pages/5-4-integration-formulas-and-the-net-change-theorem | Linear \(v(t)=3t-5\) on \([0,3]\); net displacement (sign-change sibling of \(v=2t-2c\)) |
| OpenStax Calculus Volume 1 §5.4 Example 5.25 | same | Same \(v(t)\); **total distance** (absolute integral) — **not this pass** |
| OpenStax Calculus Volume 1 §5.4 Exercise 223 | same | \(v(t)=4-2t\) on \([0,2]\); displacement and distance |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/5-4-integration-formulas-and-the-net-change-theorem.md`.

## Variety notes

Not a WP. D=0 one easy linear \(v=2t\) (old). Same-D rotation at mid D: leftover linear vs const. High D sign-change keeps integer \(c\in\{1,2,3\}\) from the old builder. Old exclusive D=8 const is easier than D=0 linear (inverted exclusive cliff); leftover lockout still mixes it at D=8 as the old mid form and leftovers it at D=16.

## Limitations

- **Status:** shipped — leftover lockout of linear \(v=2t\). Remaining `LIMITATIONS`: no total distance (Ex. 5.25 absolute integral); no OpenStax \(v=3t-5\) with nonzero net; no quadratic \(v(t)=t^{2}-3t-18\) (Ex. 224); no \(|2t-6|\) / free-fall / piecewise; D=16 can still emit const leftover (intentional; old mid is easier than linear).
- **Live pairwise:** each item stamps `form_id`, shared `generator=motion_along_a_line_integral`, and `family`; copies `form_id` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `motion_along_a_line_integral`

## Proposed engine (reuse vs new)

- **Reuse:** existing linear / const / sign-change builders in `calc_app_diff.py`. Depth = real structure (lock out \(v=2t\); unlock sign-change) — not padded `difficulty_costs`.
- **Not this pass:** distance traveled; Ex. 5.24 nonzero net; quadratic / exponential \(v(t)\); figure bank.
