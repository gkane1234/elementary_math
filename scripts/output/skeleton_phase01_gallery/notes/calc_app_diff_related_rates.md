# Notes — `calc_app_diff_related_rates` (`Related rates`)

- **Display name:** Related rates
- **Category:** Calculus — Applications of Differentiation
- **Generator:** `related_rates_simple`
- **Suggested family:** other (WP frames over closed-form related-rate algebra)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Implicit-differentiate related quantities and plug in given rates.
- **D=0:** Expanding circle only (old easy) — given \(dr/dt\), find \(dA/dt\).
- **Mid D (≈8):** Rotate circle / sphere / balloon (inverse volume → \(dr/dt\)). Circle leftovers still allowed.
- **High D (≈16):** Lock out circle/sphere/balloon. Ladder, lamp-shadow, airplane, inverse similar-triangle cone (gravel/funnel).
- **Expert (≈22):** Lock out ladder leftover. Two given rates (bikes/cars/planes/helicopter) and rocket/camera elevation angle, plus shadow / airplane / cone-drain.
- **Must not:** Equation dumps without a story; one-vehicle Mad-Lib; padded `difficulty_costs`; a new physics engine.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out** (catalog `related_rates_simple` **is** the old path). Pre-lockout: D=16 and D=22 were the same 7-frame pool, including expanding-circle leftovers.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{The radius of a circle increases at } 2\text{ cm/s. How fast is the area increasing when } r = 4\text{ cm?}$ | $16\pi$ | frame=`expanding_circle` |
| 0 | 207 | $\text{The radius of a circle increases at } 1\text{ cm/s. How fast is the area increasing when } r = 3\text{ cm?}$ | $6\pi$ | frame=`expanding_circle` |
| 8 | 101 | $\text{A spherical balloon is filled with air at } 512\pi\text{ cm}^{3}\text{/s. How fast is the radius increasing when } r = 8\text{ cm?}$ | $2$ | frame=`balloon_radius` |
| 8 | 207 | $\text{A spherical balloon is filled with air at } 980\pi\text{ cm}^{3}\text{/s. How fast is the radius increasing when } r = 7\text{ cm?}$ | $5$ | frame=`balloon_radius` |
| 16 | 101 | $\text{A }10\text{-ft ladder leans against a wall. The base slides away at } 5\text{ ft/s. How fast is the top sliding down when the base is } 6\text{ ft from the wall?}$ | $\frac{15}{4}$ | frame=`sliding_ladder` |
| 16 | 207 | $\text{A }25\text{-ft ladder leans against a wall. The base slides away at } 2\text{ ft/s. How fast is the top sliding down when the base is } 7\text{ ft from the wall?}$ | $\frac{7}{12}$ | frame=`sliding_ladder` |
| 22 | 101 | $\text{A }10\text{-ft ladder leans against a wall. The base slides away at } 5\text{ ft/s. How fast is the top sliding down when the base is } 6\text{ ft from the wall?}$ | $\frac{15}{4}$ | same pool as D=16 |
| 22 | 207 | $\text{A }25\text{-ft ladder leans against a wall. The base slides away at } 6\text{ ft/s. How fast is the top sliding down when the base is } 15\text{ ft from the wall?}$ | $\frac{9}{2}$ | same pool as D=16 |

Opt-out flag used: _(none — live catalog is the old path)_

40-seed counts **before** this pass: D=16 and D=22 identical (`airplane` 4, `sphere` 9, `ladder` 8, `balloon` 4, `cone` 4, `circle` 4, `shadow` 7).

## Live now (`_generate_for_type`)

Easy leftover lockout + extra-chain frames on the same closed-form core. Gallery seeds 101/207/313 can still collide on one frame; rotation is across seeds.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{The radius of a circle increases at } 2\text{ cm/s. How fast is the area increasing when } r = 4\text{ cm?}$ | $16\pi$ | `expanding_circle` |
| 8 | 101 | $\text{A spherical balloon is filled with air at } 512\pi\text{ cm}^{3}\text{/s. How fast is the radius increasing when } r = 8\text{ cm?}$ | $2$ | `balloon_radius` |
| 16 | 101 | $\text{A }20\text{-ft lamp post casts a shadow of a }6\text{-ft person walking away at } 5\text{ ft/s. How fast is the tip of the shadow moving away from the post when the person is } 4\text{ ft from the post?}$ | $\frac{50}{7}$ | `lamp_shadow` |
| 16 | 0 | $\text{Water drains from a conical tank (similar shape, } r=3h\text{) at } 108\pi\text{ ft}^{3}\text{/s. How fast is the water height falling when } h = 2\text{ ft?}$ | $3$ | `cone_drain` (inverse similar) |
| 16 | 2 | $\text{A }5\text{-ft ladder leans against a wall. The base slides away at } 1\text{ ft/s. How fast is the top sliding down when the base is } 3\text{ ft from the wall?}$ | $\frac{3}{4}$ | `sliding_ladder` |
| 22 | 101 | $\text{A bottle rocket rises at } 7\text{ ft/s. You stand } 5\text{ ft from the launch point. How fast is the angle of elevation changing when the rocket is } 12\text{ ft in the air?}$ | $\frac{35}{169}$ | `rocket_angle` |
| 22 | 0 | $\text{A helicopter rises at } 4\text{ ft/s while you run along the ground at } 2\text{ ft/s starting from under it. How fast is the distance between you changing when the helicopter is } 12\text{ ft up and you are } 9\text{ ft away?}$ | $\frac{22}{5}$ | `two_rate_distance` |
| 22 | 7 | $\text{Gravel falls onto a conical pile with radius } 2\text{ times the height at } 600\pi\text{ ft}^{3}\text{/min. How fast is the height increasing when } h = 5\text{ ft?}$ | $6$ | `cone_drain` |

40-seed counts **after**: D=0 circle-only; D=8 circle/sphere/balloon; D=16 ladder/shadow/airplane/`cone_drain` (no circle); D=22 two-rate/rocket/shadow/airplane/`cone_drain` (no ladder/circle).

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §4.1 Related Rates | https://openstax.org/books/calculus-volume-1/pages/4-1-related-rates | Ex 4.1 balloon (given \(dV/dt\)); Ex 4.2 airplane constant elevation; Ex 4.3 rocket/camera angle; Ex 4.4 funnel similar-triangle inverse; exercises: ladder, lamp shadow, two bikes/planes, gravel pile \(r=kh\), helicopter + runner |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/4-1-related-rates.md`.

## Variety notes

Frames in `related_rates_frames.py`. D=0 one easy frame. Same-D rotation: medium circle/sphere/balloon; D=16 ladder/shadow/airplane/cone-drain; D=22 two-rate stories rotate bikes/cars/planes/helicopter (not one-vehicle Mad-Lib). Algebra shapes stay 3-4-5 triples / integer \(k\) similar cones — not a new physics engine.

## Limitations

- **Status:** shipped — leftover lockout + extra-chain frames. Remaining `LIMITATIONS`: no trough / square-pyramid / leaking-cylinder tanks (OpenStax ex. 28–31); no lighthouse beam; no law-of-cosines baseball; no opposite-sign two-rate (approaching); diagram is still a generic `function_sketch` (parabola overlay), not a ladder/cone figure; airplane prompt uses km/s (closed-form leftover); D=8 still emits expanding-circle leftovers (intentional, like PFD two-linear at mid D); gallery seeds 101/207/313 can collide on one frame at a given D.
- **Generator:** `related_rates_simple`

## Proposed engine (reuse vs new)

- **Reuse:** existing `related_rates_frames.py` closed-form catalog + `related_rates_simple`. Depth = real structure (lock out easy leftovers; add similar-triangle inverse, two given rates, angle chain) — not padded `difficulty_costs`.
- **Not this pass:** trough/pyramid/cylinder volumes; lighthouse; signed approaching rates; matching SVG figures.
