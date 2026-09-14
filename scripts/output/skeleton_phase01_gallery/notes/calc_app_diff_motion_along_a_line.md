# Notes — `calc_app_diff_motion_along_a_line` (`Motion along a line`)

- **Display name:** Motion along a line
- **Category:** Calculus — Applications of Differentiation
- **Generator:** `motion_along_a_line`
- **Suggested family:** other (s(t) → v/a on constructive polynomials)

---

## What the question should look like (D=0 vs high D)

- **Skill:** From a position polynomial \(s(t)\), find velocity / when the particle is at rest / direction and speeding up vs slowing down.
- **D=0:** Quadratic \(s(t)=t^{2}-nt\), evaluate \(v(n)\) (old easy).
- **Mid D (≈8):** Quadratic leftover still allowed, plus “when is the particle at rest?” (old mid; rest at \(t=n/2\)).
- **High D (≈16):** Lock out eval-velocity leftover. Quadratic rest leftover plus OpenStax Ex. 3.36 cubics (two positive rest times).
- **Expert (≈22):** Lock out all \(t^{2}-nt\) leftovers. Cubic rest leftover plus Ex. 3.35 speed/direction (\(s=t^{3}-kt+c\)).
- **Must not:** Generic \(\frac{d}{dx}\) dump; padded `difficulty_costs`; free-fall \(-16t^{2}\) / piecewise / trig this pass; using `Find a(t)` (always 2) as high D — that ask is easier than rest.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**, before leftover lockout. Same \(s(t)=t^{2}-nt\) at every D; only the ask changed. `generator` was unstamped on the `_framework` wrapper. D≥16 was `Find a(t)` with answer \(2\).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $s(t)=t^{2}-6t.\quad\text{Find }v(6).$ | $6$ | `eval_velocity`; \(v(n)=n\) |
| 0 | 207 | $s(t)=t^{2}-6t.\quad\text{Find }v(6).$ | $6$ | same quadratic |
| 8 | 101 | $s(t)=t^{2}-2t.\quad\text{When is the particle at rest?}$ | $t=1$ | rest at \(n/2\) |
| 8 | 207 | $s(t)=t^{2}-6t.\quad\text{When is the particle at rest?}$ | $t=3$ | still \(t^{2}-nt\) |
| 16 | 101 | $s(t)=t^{2}-6t.\quad\text{Find }a(t).$ | $2$ | `acceleration_const`; inverted (easier than rest) |
| 22 | 101 | $s(t)=t^{2}-6t.\quad\text{Find }a(t).$ | $2$ | same quadratic |

Opt-out flag used: _(none — live catalog is the old path)_

## Live now (`_generate_for_type`)

Leftover lockout + OpenStax §3.4 cubics on the same motion core. D=0 stays old eval-velocity. Old high-D `Find a(t)` is not a leftover (too easy). 40-seed counts after: D=0 eval-velocity only; D=8 eval leftover + quadratic rest; D=16 quadratic-rest leftover + cubic rest (no eval-velocity); D=22 cubics only.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $s(t)=t^{2}-3t.\quad\text{Find }v(3).$ | $3$ | `eval_velocity` |
| 0 | 207 | $s(t)=t^{2}-6t.\quad\text{Find }v(6).$ | $6$ | old easy quadratic |
| 8 | 7 | $s(t)=t^{2}-3t.\quad\text{Find }v(3).$ | $3$ | eval leftover |
| 8 | 101 | $s(t)=t^{2}-2t.\quad\text{When is the particle at rest?}$ | $t=1$ | quadratic rest leftover |
| 16 | 7 | $s(t)=t^{2}-2t.\quad\text{When is the particle at rest?}$ | $t=1$ | rest leftover |
| 16 | 101 | $s(t)=t^{3} - 9t^{2} + 24t + 4.\quad\text{When is the particle at rest?}$ | $t=2,\,t=4$ | Ex. 3.36 shape |
| 22 | 7 | $s(t)=t^{3} - 9t^{2} + 24t + 2.\quad\text{When is the particle at rest?}$ | $t=2,\,t=4$ | cubic rest leftover |
| 22 | 101 | $s(t)=t^{3} - 8t + 2.\quad\text{Find }v(1)\text{ and }a(1).\text{ Is the particle moving left to right or right to left? Speeding up or slowing down?}$ | $v(1)=-5,\,a(1)=6;\text{ right to left; slowing down}$ | Ex. 3.35 speed-sign |
| 22 | 207 | $s(t)=t^{3} - 4t.\quad\text{Find }v(1)\text{ and }a(1).\text{ Is the particle moving left to right or right to left? Speeding up or slowing down?}$ | $v(1)=-1,\,a(1)=6;\text{ right to left; slowing down}$ | Ex. 3.35 \(t^{3}-4t\) |

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §3.4 Checkpoint 3.22 | https://openstax.org/books/calculus-volume-1/pages/3-4-derivatives-as-rates-of-change | Quadratic \(s(t)=t^{2}-5t+1\); direction / velocity at a time (D=0 eval-velocity is the old-easy sibling) |
| OpenStax Calculus Volume 1 §3.4 Example 3.36 | same | \(s(t)=t^{3}-9t^{2}+24t+4\); rest at two times (\(v=3(t-2)(t-4)\)) |
| OpenStax Calculus Volume 1 §3.4 Example 3.35 | same | \(s(t)=t^{3}-4t+2\); \(v(1)\), \(a(1)\); left/right and speeding up / slowing down |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/3-4-derivatives-as-rates-of-change.md`.

## Variety notes

Not a WP. D=0 one easy eval-velocity quadratic (old). Same-D rotation at mid D: eval leftover vs rest. High D cubics with integer rest times (\(p+q\) even). Algebra shapes copy the old \(t^{2}-nt\) family; cubics keep integer coeffs (same even-sum idea as shifted extrema).

## Limitations

- **Status:** shipped — leftover lockout + Ex. 3.36 / 3.35 cubics. Remaining `LIMITATIONS`: no free-fall \(-16t^{2}\) (Ex. 3.34 / rocket / potato); no \(s=t/(1+t^{2})\); no graph of \(s(t)\) (Ex. 159); no hummingbird \(3t^{3}-7t\) as a separate form; D=16 can still emit quadratic rest leftover (intentional).
- **Live pairwise:** each item stamps `form_id`, shared `generator=motion_along_a_line`, and `family`; copies `form_id` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `motion_along_a_line`

## Proposed engine (reuse vs new)

- **Reuse:** quadratic \(s=t^{2}-nt\) plus cubic rest/speed builders in `calc_app_diff.py`. Depth = real structure (lock out \(t^{2}-nt\); unlock cubics) — not padded `difficulty_costs`.
- **Not this pass:** free-fall / piecewise / trig motion; integral net-change (sibling leaf); figure bank.
