# Notes — `pc_right_triangle_trig_finding_angles_and_sides` (`Right triangle trig, finding angles and sides`)

- **Course:** Precalculus
- **Category:** Precalculus — Trigonometry
- **Generator:** `geo_right_triangle_trig`
- **Suggested family:** geometry

---

## What the question should look like (D=0 vs high D)

- **Skill:** Student find the missing measure for right triangle trig, finding angles and sides.
- **D=0:** solve triangle for angle or side; simplest numeric/instance (per OpenStax § easy exercises).
- **High D (≈16–22):** harder coefficients, more factors/steps, or extra format (e.g. general solution for trig, higher-degree PFD).
- **Must not:** wrong-topic shapes, equation dump without context on WP leaves, calc topics on algebra-only skeletons.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for Precalc leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\text{In right } \triangle ABC,\ m\angle A = 45^\circ,\ BC = 5\text{ cm}.\ \text{Find } AC.$` | `$\frac{5}{\tan 45^\circ}$` | triangle |
| 8 | 101 | `$\text{In right } \triangle ABC \text{ with right angle at } C,\ \text{find } \tan A.$` | `$\frac{9}{12}$` | triangle |
| 16 | 101 | `$\text{In right } \triangle ABC,\ m\angle A = 45^\circ,\ BC = 7\text{ cm}.\ \text{Find } AC.$` | `$\frac{7}{\tan 45^\circ}$` | triangle |
| 22 | 101 | `$\text{In right } \triangle ABC,\ m\angle A = 45^\circ,\ BC = 7\text{ cm}.\ \text{Find } AC.$` | `$\frac{7}{\tan 45^\circ}$` | triangle |

Opt-out flag used: _none (default live generator)_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Precalculus 2e §5.4 | https://openstax.org/books/precalculus-2e/pages/5-4-right-triangle-trigonometry | solve triangle for angle or side |

Local HTML (if mined): `textbooks/openstax/html/precalculus-2e/…` or `scripts/output/example_mining/precalculus-2e/stage1/5-4-right-triangle-trigonometry.md`

## Variety notes / flags

- Live generator produces topic-shaped prompts; OpenStax frames for WP/application leaves.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Geometry skeleton (solve triangle).
- **New:** only if no honest skeleton match — otherwise leave leaf (see `benchmark-old-path.mdc`).
- **Not this pass:** notes only — no generator wiring.



## Limitations

- **Variety:** Notes claim topic-shaped live stems; re-check seed diversity beyond seed=101 before treating as gold-locked.
- **Difficulty scaling:** Notes table shows stem changes with D at seed=101; confirm numeric hardness before format unlocks.
- **OpenStax:** Cite present; gold shapes in cite column — do not invent new algebra beyond old-path + cite.
- **Engine:** Notes still say notes-only / not this pass, but catalog generator is live (old path = default). No new skeleton this audit unless gold locks.
- **This pass:** Gallery + Limitations audit only. Implement leftover only if notes lock gold (not for flat-D / red-header variety leaves).

_topic-fit galleries: `scripts/output/topic_fit/pc_algebraic_gallery/` (log/exp/pfd/function ops/rational); `scripts/output/topic_fit/difficulty_sweep/by_course/precalculus.html` (continuous-D subset)._
