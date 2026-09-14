# Notes — `pc_law_of_sines` (`The Law of Sines`)

- **Course:** Precalculus
- **Category:** Precalculus — Trigonometry
- **Generator:** `law_of_sines`
- **Suggested family:** geometry

---

## What the question should look like (D=0 vs high D)

- **Skill:** Student find the missing measure for the law of sines.
- **D=0:** ASA/AAS/SSA solve triangle; simplest numeric/instance (per OpenStax § easy exercises).
- **High D (≈16–22):** harder coefficients, more factors/steps, or extra format (e.g. general solution for trig, higher-degree PFD).
- **Must not:** wrong-topic shapes, equation dump without context on WP leaves, calc topics on algebra-only skeletons.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for Precalc leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\text{In } \triangle ABC,\ m\angle A = 60^\circ,\ m\angle B = 30^\circ,\ a = 10.\ \text{Find } b \text{ (Law of Sines).}$` | `$5.77$` | triangle |
| 8 | 101 | `$\text{In } \triangle ABC,\ m\angle A = 50^\circ,\ m\angle B = 30^\circ,\ a = 15.\ \text{Find } b \text{ (Law of Sines).}$` | `$9.79$` | triangle |
| 16 | 101 | `$\text{In } \triangle ABC,\ m\angle A = 120^\circ,\ m\angle B = 40^\circ,\ a = 13.\ \text{Find } b \text{ (Law of Sines).}$` | `$9.65$` | triangle |
| 22 | 101 | `$\text{In } \triangle ABC,\ m\angle A = 50^\circ,\ m\angle B = 45^\circ,\ a = 7.\ \text{Find } b \text{ (Law of Sines).}$` | `$6.46$` | triangle |

Opt-out flag used: _none (default live generator)_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Precalculus 2e §8.1 | https://openstax.org/books/precalculus-2e/pages/8-1-non-right-triangles-law-of-sines | ASA/AAS/SSA solve triangle |

Local HTML (if mined): `textbooks/openstax/html/precalculus-2e/…` or `scripts/output/example_mining/precalculus-2e/stage1/8-1-non-right-triangles-law-of-sines.md`

## Variety notes / flags

- Live generator produces topic-shaped prompts; OpenStax frames for WP/application leaves.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Geometry skeleton (non-right triangle).
- **New:** only if no honest skeleton match — otherwise leave leaf (see `benchmark-old-path.mdc`).
- **Not this pass:** notes only — no generator wiring.



## Limitations

- **Variety:** Notes claim topic-shaped live stems; re-check seed diversity beyond seed=101 before treating as gold-locked.
- **Difficulty scaling:** Notes table shows stem changes with D at seed=101; confirm numeric hardness before format unlocks.
- **OpenStax:** Cite present; gold shapes in cite column — do not invent new algebra beyond old-path + cite.
- **Engine:** Notes still say notes-only / not this pass, but catalog generator is live (old path = default). No new skeleton this audit unless gold locks.
- **This pass:** Gallery + Limitations audit only. Implement leftover only if notes lock gold (not for flat-D / red-header variety leaves).

_topic-fit galleries: `scripts/output/topic_fit/pc_algebraic_gallery/` (log/exp/pfd/function ops/rational); `scripts/output/topic_fit/difficulty_sweep/by_course/precalculus.html` (continuous-D subset)._
