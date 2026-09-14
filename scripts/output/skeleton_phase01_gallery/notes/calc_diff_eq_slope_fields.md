# Notes — `calc_diff_eq_slope_fields` (`Slope fields`)

- **Display name:** Slope fields
- **Category:** Calculus — Differential Equations
- **Generator:** `slope_field_interpret`
- **Suggested family:** other (eval \(y'=F(x,y)\) at a lattice point; no figure bank)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Evaluate \(F(x,y)\) at a lattice point — the hash a direction field would draw there.
- **D=0:** Autonomous leftover \(y'=x\) at \((p_x,p_y)\) with \(p_x,p_y\in\{-3,\ldots,3\}\) (old easy).
- **Mid D (≈8):** \(y'=x\) leftover still allowed, plus \(y'=x+y\).
- **High D (≈16):** Lock out \(y'=x\). \(y'=x+y\) leftover plus \(y'=xy\).
- **Expert (≈22):** \(y'=xy\) only.
- **Must not:** Slope-field SVG / match-the-sketch; padded `difficulty_costs`; new RHS cores (\(y'=x-y\), \(y'=x^{2}\), autonomous \(y'=y\), …) this pass.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` with **no opt-out**, before leftover bands. `_pick_family` accumulated unlocks, so high D still mixed \(y'=x\). `generator` / `form_id` unstamped. No `spec_snapshot`. 40-seed counts: D=0 all \(y'=x\); D=8 leftover \(x\) + \(x+y\) (19/21); D=16 still \(y'=x\) (12) + \(x+y\) (17) + \(xy\) (11); D=22 still \(y'=x\) (13) + \(x+y\) (11) + \(xy\) (16).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{For }y'=x,\text{ what is the slope at }(-1,-1)?$ | $-1$ | \(y'=x\) only |
| 0 | 207 | $\text{For }y'=x,\text{ what is the slope at }(-2,-2)?$ | $-2$ | \(p_x,p_y\in\{-3,\ldots,3\}\) |
| 8 | 101 | $\text{For }y'=x+y,\text{ what is the slope at }(1,3)?$ | $4$ | \(x+y\) |
| 8 | 207 | $\text{For }y'=x,\text{ what is the slope at }(3,2)?$ | $3$ | \(y'=x\) leftover |
| 16 | 101 | $\text{For }y'=x+y,\text{ what is the slope at }(-3,1)?$ | $-2$ | still mixes easy leftover |
| 16 | 207 | $\text{For }y'=x,\text{ what is the slope at }(-2,-3)?$ | $-2$ | \(y'=x\) at D=16 |
| 22 | 101 | $\text{For }y'=xy,\text{ what is the slope at }(1,0)?$ | $0$ | \(xy\) |
| 22 | 207 | $\text{For }y'=x+y,\text{ what is the slope at }(2,-3)?$ | $-1$ | \(x+y\) leftover at expert |

Opt-out flag used: _(none — live catalog is the old path)_

## Live now (`_generate_for_type`)

Leftover lockout on the same three builders. D=0 stays old \(y'=x\). Gallery seeds 101/207/313 can collide on one form at mid D; rotation is across seeds.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\text{For }y'=x,\text{ what is the slope at }(-2,1)?$ | $-2$ | `sf_x` |
| 0 | 0 | $\text{For }y'=x,\text{ what is the slope at }(3,0)?$ | $3$ | old easy |
| 8 | 1 | $\text{For }y'=x,\text{ what is the slope at }(3,3)?$ | $3$ | \(y'=x\) leftover |
| 8 | 101 | $\text{For }y'=x+y,\text{ what is the slope at }(-2,1)?$ | $-1$ | `sf_x_plus_y` |
| 16 | 1 | $\text{For }y'=x+y,\text{ what is the slope at }(3,3)?$ | $6$ | \(x+y\) leftover |
| 16 | 101 | $\text{For }y'=xy,\text{ what is the slope at }(-2,1)?$ | $-2$ | no \(y'=x\) leftover |
| 22 | 0 | $\text{For }y'=xy,\text{ what is the slope at }(3,0)?$ | $0$ | `sf_xy` only |
| 22 | 101 | $\text{For }y'=xy,\text{ what is the slope at }(-2,1)?$ | $-2$ | `sf_xy` only |
| 22 | 207 | $\text{For }y'=xy,\text{ what is the slope at }(2,1)?$ | $2$ | `sf_xy` only |

40-seed counts **after**: D=0 `sf_x` only; D=8 leftover `sf_x` + `sf_x_plus_y` (19/21); D=16 leftover `sf_x_plus_y` + `sf_xy` (19/21, no `sf_x`); D=22 `sf_xy` only.

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 2 §4.2 Direction Fields and Numerical Methods | https://openstax.org/books/calculus-volume-2/pages/4-2-direction-fields-and-numerical-methods | At \((x_0,y_0)\) the hash has slope \(F(x_0,y_0)\). D=0 is \(y'=x\) (old easy). |
| Same §4.2 | same | Mid/high: \(y'=x+y\), \(y'=xy\) (old unlocks). Match-the-sketch / Euler step / SVG direction field — **not this pass** (leave on LIMITATIONS) |

Local HTML / mine: `textbooks/openstax/html/calculus-volume-2/` · Vol 2 Ch.4 not in `scripts/output/example_mining/calculus-volume-2/stage1/` (mining stops before DE). Learning-objective spine: `scripts/output/example_mining/progression/full_spine.md` (Vol 2 §4.2).

## Variety notes

Not a WP. D=0 one easy eval \(y'=x\) (old). Same-D rotation at mid D: leftover \(y'=x\) vs \(y'=x+y\). High D keeps the old \(y'=xy\) builder (do not invent \(y'=x-y\)). Three old forms, so D=16 mixes \(x+y\) leftover + \(xy\) and D=22 is \(xy\)-only.

## Limitations

- **Status:** shipped — leftover lockout of \(y'=x\). Remaining `LIMITATIONS`: eval-at-a-point only (no direction-field figure / match-the-sketch / Euler); three frozen RHSs (\(x\), \(x+y\), \(xy\)); D=16 can still emit \(y'=x+y\) leftover (intentional).
- **Live pairwise:** each item stamps `form_id`, shared `generator=slope_field_interpret`, and `family`; copies `form_id` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt.
- **Generator:** `slope_field_interpret`

## Proposed engine (reuse vs new)

- **Reuse:** existing eval-at-a-point builders (now in `calc_app_diff.py`). Depth = real structure (lock out \(y'=x\); mix leftover at D=8 / D=16) — not padded `difficulty_costs`.
- **Not this pass:** slope-field figures / SVG; new RHS cores; Euler numerical step (other leaf / later).
