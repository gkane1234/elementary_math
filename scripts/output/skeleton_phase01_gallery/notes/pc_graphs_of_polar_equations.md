# Notes — `pc_graphs_of_polar_equations` (`Graphs of polar equations`)

> **LOW_VARIETY**

- **Course:** Precalculus
- **Category:** Precalculus — Polar Coordinates
- **Generator:** `polar_graphs`
- **Suggested family:** other

---

## What the question should look like (D=0 vs high D)

- **Skill:** Student graph the following equations for graphs of polar equations.
- **D=0:** identify rose/circle/cardiod from eqn; simplest numeric/instance (per OpenStax § easy exercises).
- **High D (≈16–22):** harder coefficients, more factors/steps, or extra format (e.g. general solution for trig, higher-degree PFD).
- **Must not:** wrong-topic shapes, equation dump without context on WP leaves, calc topics on algebra-only skeletons.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for Precalc leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$r=3+2\cos\theta$` | `$\text{limacon}$` | evaluate/rewrite |
| 8 | 101 | `$r=3+2\cos\theta$` | `$\text{limacon}$` | evaluate/rewrite |
| 16 | 101 | `$r=3+2\cos\theta$` | `$\text{limacon}$` | evaluate/rewrite |
| 22 | 101 | `$r=3+2\cos\theta$` | `$\text{limacon}$` | evaluate/rewrite |

Opt-out flag used: _none (default live generator)_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Precalculus 2e §8.5 | https://openstax.org/books/precalculus-2e/pages/8-5-polar-coordinates-graphs | identify rose/circle/cardiod from eqn |

Local HTML (if mined): `textbooks/openstax/html/precalculus-2e/…` or `scripts/output/example_mining/precalculus-2e/stage1/8-5-polar-coordinates-graphs.md`

## Variety notes / flags

- Identical prompt across all D bands sampled.
- Answer shape flat across D — difficulty may be cosmetic.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Polar graph identify framework.
- **New:** only if no honest skeleton match — otherwise leave leaf (see `benchmark-old-path.mdc`).
- **Not this pass:** notes only — no generator wiring.



## Limitations

> **LIMITATIONS**

- **Variety:** Old-path table shows one prompt shape across D bands sampled (seed=101) — `$r=3+2\cos\theta$`.
- **Difficulty scaling:** Answer latex flat across D in notes table — D may be cosmetic until form unlocks change the student-visible stem.
- **OpenStax:** Cite present; gold shapes in cite column — do not invent new algebra beyond old-path + cite.
- **Graphing:** Prompt asks to graph / describe amplitude-period, but gallery is text-only (no axes SVG). Treat as property/describe task until graph renderer ships.
- **Engine:** Notes still say notes-only / not this pass, but catalog generator is live (old path = default). No new skeleton this audit unless gold locks.
- **This pass:** Gallery + Limitations audit only. Implement leftover only if notes lock gold (not for flat-D / red-header variety leaves).

_topic-fit galleries: `scripts/output/topic_fit/pc_algebraic_gallery/` (log/exp/pfd/function ops/rational); `scripts/output/topic_fit/difficulty_sweep/by_course/precalculus.html` (continuous-D subset)._
