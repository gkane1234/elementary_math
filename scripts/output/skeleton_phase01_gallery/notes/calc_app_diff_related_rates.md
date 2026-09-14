# Notes — `calc_app_diff_related_rates`

- **Display name:** Related rates
- **Category:** Calculus — Applications of Differentiation
- **Generator:** `related_rates_simple`
- **Suggested family:** `other`

---

## Limitations

- **Status:** shipped — live generator
- **Generator:** `related_rates_simple`
- **Remaining limits:** Constructive app generators with continuous-D structure knobs. Gaps: story frame banks thinner than OpenStax for related rates / growth; volumes mostly axis-of-rotation textbook templates; no interactive figures.

## What the question should look like (D=0 vs high D)

- **Skill:** Implicit differentiate related quantities; plug rates.
- **D=0:** Expanding circle only (old easy).
- **High D (≈10–22):** OpenStax §4.1 frame rotation — balloon, cone, ladder, lamp shadow, airplane — not circle/sphere/cone Mad-Lib only.
- **Must not:** Wrong-topic shapes; equation dumps without story.

## What live path actually produced (real latex, D=0/8/16/22)

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{The radius of a circle increases at } 2\text{ cm/s. How fast is the area increasing when } r = 4\text{ cm?}$ | $16\pi$ | frame=`expanding_circle` |
| 0 | 207 | $\text{The radius of a circle increases at } 1\text{ cm/s. How fast is the area increasing when } r = 3\text{ cm?}$ | $6\pi$ | frame=`expanding_circle` |
| 8 | 101 | $\text{A spherical balloon is filled with air at } 512\pi\text{ cm}^{3}\text{/s. How fast is the radius increasing when } r = 8\text{ cm?}$ | $2$ | frame=`balloon_radius` |
| 8 | 207 | $\text{A spherical balloon is filled with air at } 980\pi\text{ cm}^{3}\text{/s. How fast is the radius increasing when } r = 7\text{ cm?}$ | $5$ | frame=`balloon_radius` |
| 16 | 101 | $\text{A }10\text{-ft ladder leans against a wall. The base slides away at } 5\text{ ft/s. How fast is the top sliding down when the base is } 6\text{ ft from the wall?}$ | $\frac{15}{4}$ | frame=`sliding_ladder` |
| 16 | 207 | $\text{A }25\text{-ft ladder leans against a wall. The base slides away at } 2\text{ ft/s. How fast is the top sliding down when the base is } 7\text{ ft from the wall?}$ | $\frac{7}{12}$ | frame=`sliding_ladder` |
| 22 | 101 | $\text{A }10\text{-ft ladder leans against a wall. The base slides away at } 5\text{ ft/s. How fast is the top sliding down when the base is } 6\text{ ft from the wall?}$ | $\frac{15}{4}$ | frame=`sliding_ladder` |
| 22 | 207 | $\text{A }25\text{-ft ladder leans against a wall. The base slides away at } 6\text{ ft/s. How fast is the top sliding down when the base is } 15\text{ ft from the wall?}$ | $\frac{9}{2}$ | frame=`sliding_ladder` |

Opt-out flag used: `(none)`

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §4.1 | https://openstax.org/books/calculus-volume-1/pages/4-1-related-rates | Rotate frames: expanding circle/sphere, balloon (given dV/dt), ladder, similar-triangles cone, lamp-post shadow, airplane at constant elevation |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/`.

## Variety notes

OpenStax §4.1 frames wired in `related_rates_frames.py` (`expanding_circle`, `expanding_sphere`, `balloon_radius`, `cone_similar`, `sliding_ladder`, `lamp_shadow`, `airplane_distance`). D=0 stays circle-only.

## Proposed engine (reuse vs new)

- **Proposal:** WP frames over Diff/implicit core; several OpenStax frames at same D.
- **Reuse Diff?** only if needed for derivatives inside apps — current frames use closed-form related-rate algebra.
- **Shipped:** frame catalog + `related_rates_simple` wiring.

_Catalog generator `related_rates_simple`._
