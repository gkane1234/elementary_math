# Notes — `pc_law_of_cosines` (`The Law of Cosines`)

- **Course:** Precalculus
- **Category:** Precalculus — Trigonometry
- **Generator:** `law_of_cosines`
- **Suggested family:** geometry

---

## What the question should look like (D=0 vs high D)

- **Skill:** Student find the missing measure for the law of cosines.
- **D=0:** SAS/SSS side or angle; simplest numeric/instance (per OpenStax § easy exercises).
- **High D (≈16–22):** harder coefficients, more factors/steps, or extra format (e.g. general solution for trig, higher-degree PFD).
- **Must not:** wrong-topic shapes, equation dump without context on WP leaves, calc topics on algebra-only skeletons.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for Precalc leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\text{In } \triangle ABC,\ a = 12,\ b = 10,\ m\angle C = 30^\circ.\ \text{Find } c \text{ (Law of Cosines).}$` | `$6.01$` | triangle |
| 8 | 101 | `$\text{In } \triangle ABC,\ a = 12,\ b = 17,\ m\angle C = 45^\circ.\ \text{Find } c \text{ (Law of Cosines).}$` | `$12.02$` | triangle |
| 16 | 101 | `$\text{In } \triangle ABC,\ a = 12,\ b = 17,\ m\angle C = 80^\circ.\ \text{Find } c \text{ (Law of Cosines).}$` | `$19.03$` | triangle |
| 22 | 101 | `$\text{In } \triangle ABC,\ a = 11,\ b = 7,\ m\angle C = 80^\circ.\ \text{Find } c \text{ (Law of Cosines).}$` | `$11.97$` | triangle |

Opt-out flag used: _none (default live generator)_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Precalculus 2e §8.2 | https://openstax.org/books/precalculus-2e/pages/8-2-non-right-triangles-law-of-cosines | SAS/SSS side or angle |

Local HTML (if mined): `textbooks/openstax/html/precalculus-2e/…` or `scripts/output/example_mining/precalculus-2e/stage1/8-2-non-right-triangles-law-of-cosines.md`

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
