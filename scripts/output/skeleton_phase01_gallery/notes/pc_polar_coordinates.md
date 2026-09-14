# Notes — `pc_polar_coordinates` (`Polar coordinates`)

- **Course:** Precalculus
- **Category:** Precalculus — Polar Coordinates
- **Generator:** `polar_coordinates`
- **Suggested family:** other

---

## What the question should look like (D=0 vs high D)

- **Skill:** Student convert or plot for polar coordinates.
- **D=0:** rect↔polar point conversion; simplest numeric/instance (per OpenStax § easy exercises).
- **High D (≈16–22):** harder coefficients, more factors/steps, or extra format (e.g. general solution for trig, higher-degree PFD).
- **Must not:** wrong-topic shapes, equation dump without context on WP leaves, calc topics on algebra-only skeletons.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for Precalc leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\text{Convert } (7, 150^\circ) \text{ from polar to rectangular coordinates.}$` | `$(-6.06, 3.50)$` | evaluate/rewrite |
| 8 | 101 | `$\text{Convert } (4, 150^\circ) \text{ from polar to rectangular coordinates.}$` | `$(-3.46, 2.00)$` | evaluate/rewrite |
| 16 | 101 | `$\text{Convert } (10, 90^\circ) \text{ from polar to rectangular coordinates.}$` | `$(0.00, 10.00)$` | evaluate/rewrite |
| 22 | 101 | `$\text{Convert } (4, 180^\circ) \text{ from polar to rectangular coordinates.}$` | `$(-4.00, 0.00)$` | evaluate/rewrite |

Opt-out flag used: _none (default live generator)_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Precalculus 2e §8.4 | https://openstax.org/books/precalculus-2e/pages/8-4-polar-coordinates | rect↔polar point conversion |

Local HTML (if mined): `textbooks/openstax/html/precalculus-2e/…` or `scripts/output/example_mining/precalculus-2e/stage1/8-4-polar-coordinates.md`

## Variety notes / flags

- Live generator produces topic-shaped prompts; OpenStax frames for WP/application leaves.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Polar coord constructive (rect↔polar).
- **New:** only if no honest skeleton match — otherwise leave leaf (see `benchmark-old-path.mdc`).
- **Not this pass:** notes only — no generator wiring.



## Limitations

- **Variety:** Notes claim topic-shaped live stems; re-check seed diversity beyond seed=101 before treating as gold-locked.
- **Difficulty scaling:** Notes table shows stem changes with D at seed=101; confirm numeric hardness before format unlocks.
- **OpenStax:** Cite present; gold shapes in cite column — do not invent new algebra beyond old-path + cite.
- **Engine:** Notes still say notes-only / not this pass, but catalog generator is live (old path = default). No new skeleton this audit unless gold locks.
- **This pass:** Gallery + Limitations audit only. Implement leftover only if notes lock gold (not for flat-D / red-header variety leaves).

_topic-fit galleries: `scripts/output/topic_fit/pc_algebraic_gallery/` (log/exp/pfd/function ops/rational); `scripts/output/topic_fit/difficulty_sweep/by_course/precalculus.html` (continuous-D subset)._
