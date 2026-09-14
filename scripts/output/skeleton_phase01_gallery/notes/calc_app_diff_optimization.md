# Notes — `calc_app_diff_optimization` (`Optimization`)

- **Display name:** Optimization
- **Category:** Calculus — Applications of Differentiation
- **Generator:** `optimization_applied`
- **Suggested family:** other (WP frames over closed-form first-derivative max)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Set up a one-variable max/min from a story and report the optimizing dimensions or price.
- **D=0:** Rectangle of fixed perimeter (old easy) — square. Story may be a generic rectangle or an OpenStax fencing pen.
- **Mid D (≈8):** Rectangle leftover still allowed, plus three-sided garden / river pen (Ex. 4.32 / Ex. 320).
- **High D (≈16):** Lock out four-sided rectangle leftover. Garden leftover, square open box, linear revenue \(R=p(N-kp)\) (Ex. 4.35).
- **Expert (≈22):** Lock out garden leftover. Inscribed rectangle in a circle/ellipse, closed cylinder min surface, triangle-inscribed rectangle, rectangular-sheet open box (Ex. 4.33).
- **Must not:** Equation dumps without a story; padded `difficulty_costs`; a new numerical optimizer.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out** (catalog `optimization_applied` **is** the old path). Pre-lockout: D=16 and D=22 were the same garden/open-box pool; D=22 still emitted the D=16 garden leftover. `generator` was unstamped.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{A rectangle has perimeter }44.\text{ What dimensions maximize area?}$ | $11 by 11$ | `rectangle_perimeter` |
| 0 | 207 | $\text{A rectangle has perimeter }20.\text{ What dimensions maximize area?}$ | $5 by 5$ | `rectangle_perimeter` |
| 8 | 101 | $\text{A rectangle has perimeter }44.\text{ What dimensions maximize area?}$ | $11 by 11$ | leftover rectangle (same as D=0) |
| 16 | 101 | $\text{A rectangular garden uses a wall as one side and }32\text{ ft of fence for the other three. What dimensions maximize area?}$ | $8\text{ (sides) by }16\text{ (along wall)}$ | `garden_three_sides` |
| 22 | 101 | $\text{A rectangular garden uses a wall as one side and }32\text{ ft of fence for the other three. What dimensions maximize area?}$ | $8\text{ (sides) by }16\text{ (along wall)}$ | same pool as D=16 |

Opt-out flag used: _(none — live catalog is the old path)_

## Live now (`_generate_for_type`)

Easy leftover lockout + extra OpenStax §4.7 frames on the same closed-form core. Gallery seeds 101/207/313 can still collide on one frame; rotation is across seeds.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{You have }24\text{ ft of fencing to construct a rectangular pen. What dimensions maximize the area?}$ | $6 by 6$ | `rectangle_perimeter` (Ex. 319 story) |
| 0 | 207 | $\text{A rectangle has perimeter }48.\text{ What dimensions maximize area?}$ | $12 by 12$ | `rectangle_perimeter` |
| 8 | 101 | $\text{You have }20\text{ ft of fencing to make a rectangular pen along a river (no fence on the river side). What dimensions maximize area?}$ | $5\text{ (sides) by }10\text{ (along river)}$ | `garden_three_sides` |
| 8 | 7 | $\text{You have }20\text{ ft of fencing to construct a rectangular pen. What dimensions maximize the area?}$ | $5 by 5$ | rectangle leftover |
| 16 | 101 | $\text{An open box is made from a }18\text{ by }18\text{ square sheet by cutting equal squares from each corner. What cut size }x\text{ maximizes volume?}$ | $3$ | `open_box` |
| 16 | 0 | $\text{A rental company rents }n(p)=320-2p\text{ cars per day at price }p\text{ dollars. What price maximizes revenue }R=p\,n(p)?$ | $80$ | `linear_revenue` |
| 22 | 101 | $\text{A rectangle is inscribed in the circle }x^{2}+y^{2}=9.\text{ What dimensions maximize its area?}$ | $3\sqrt{2}\text{ by }3\sqrt{2}$ | `inscribed_ellipse` |
| 22 | 5 | $\text{Find the dimensions of the closed cylinder of volume }54\pi\text{ that has the least surface area.}$ | $r=3,\ h=6$ | `closed_cylinder` |
| 22 | 7 | $\text{An open-top box is made from a }24\text{ in. by }36\text{ in. sheet by cutting equal squares from each corner. What cut size }x\text{ maximizes volume?}$ | $6$ | `open_box_rect` (Ex. 4.33) |

40-seed counts **after**: D=0 rectangle-only; D=8 rectangle/garden; D=16 garden/open-box/revenue (no four-sided leftover); D=22 inscribed/cylinder/rect-box (no garden).

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §4.7 | https://openstax.org/books/calculus-volume-1/pages/4-7-applied-optimization-problems | Ex. 4.32 garden+wall; Ex. 4.33 24×36 open box; Ex. 4.35 linear revenue; Ex. 4.36 inscribed ellipse / Checkpoint 4.35 circle; Ex. 345 closed cylinder \(V=16\pi\); Ex. 319 fencing pen; Ex. 320 river; Ex. 343 triangle-inscribed rectangle |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-1/` · `scripts/output/example_mining/calculus-volume-1/stage1/4-7-applied-optimization-problems.md`.

## Variety notes

Frames in `optimization_frames.py`. D=0 one easy frame (square from perimeter). Same-D rotation: medium rectangle/garden-or-river; D=16 garden/box/revenue; D=22 inscribed/cylinder/24×36 box. Algebra shapes stay integer \(L=4n\), \(x=S/6\), \(p=N/(2k)\), \(h=2r\) — not a numerical solver.

## Limitations

- **Status:** shipped — leftover lockout + extra OpenStax frames. Remaining `LIMITATIONS`: no island/swim travel-time (Ex. 4.34); no Norman window; no cylinder-in-sphere / cone-in-sphere; no hallway-corner ladder; no weighted-least-squares pulse; no adjacent-pens fencing; diagram is not a garden/box figure.
- **Live pairwise:** each item stamps `form_id` (= frame id), shared `generator=optimization_applied`, and `family`; copies `form_id` onto `spec_snapshot` / θ. Frame pick uses `select_form_id` so `live_quality_form_weights` can tilt; cold start is still the D-band OpenStax mix (equal weights among `optimization_frames_for_difficulty`). Not a JSON `openstax_form_catalogs/*.json` — WP Python frames.
- **Generator:** `optimization_applied`

## Proposed engine (reuse vs new)

- **Reuse:** existing closed-form `sample_optimization` / `optimization_applied`. Depth = real structure (lock out easy leftovers; add inscribed / cylinder / revenue) — not padded `difficulty_costs`.
- **Not this pass:** travel-time; Norman window; solids-in-solids; matching SVG figures.
