# Notes — `pc_rotations_of_conic_sections` (`Rotations of conic sections`)

- **Course:** Precalculus
- **Category:** Precalculus — Conic Sections
- **Generator:** `conic_rotation_identify`
- **Suggested family:** other

---

## What the question should look like (D=0 vs high D)

- **Skill:** Student identify or write the equation for rotations of conic sections.
- **D=0:** cot 2θ from Bxy term; simplest numeric/instance (per OpenStax § easy exercises).
- **High D (≈16–22):** harder coefficients, more factors/steps, or extra format (e.g. general solution for trig, higher-degree PFD).
- **Must not:** wrong-topic shapes, equation dump without context on WP leaves, calc topics on algebra-only skeletons.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for Precalc leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\text{Does } 4x^{2} + 5y^{2} = 1 \text{ require a rotation of axes to eliminate an } xy \text{ term?}$` | `$no$` | limit |
| 8 | 101 | `$\text{For } 2x^{2} + 2xy + 3y^{2} = 1,\ \text{find } \cot 2\theta \text{ used to eliminate the } xy \text{ term.}$` | `$\frac{-1}{2}$` | limit |
| 16 | 101 | `$\text{For } 4x^{2} + 2xy + 3y^{2} = 1,\ \text{find } \cot 2\theta \text{ used to eliminate the } xy \text{ term.}$` | `$\frac{1}{2}$` | limit |
| 22 | 101 | `$\text{Does } 4x^{2} + 3y^{2} = 1 \text{ require a rotation of axes to eliminate an } xy \text{ term?}$` | `$no$` | limit |

Opt-out flag used: _none (default live generator)_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Precalculus 2e §10.6 | https://openstax.org/books/precalculus-2e/pages/10-6-rotation-of-axes | cot 2θ from Bxy term |

Local HTML (if mined): `textbooks/openstax/html/precalculus-2e/…` or `scripts/output/example_mining/precalculus-2e/stage1/10-6-rotation-of-axes.md`

## Variety notes / flags

- Live generator produces topic-shaped prompts; OpenStax frames for WP/application leaves.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Conic rotation identify (keep specialized).
- **New:** only if no honest skeleton match — otherwise leave leaf (see `benchmark-old-path.mdc`).
- **Not this pass:** notes only — no generator wiring.



## Limitations

- **Variety:** Notes claim topic-shaped live stems; re-check seed diversity beyond seed=101 before treating as gold-locked.
- **Difficulty scaling:** Notes table shows stem changes with D at seed=101; confirm numeric hardness before format unlocks.
- **OpenStax:** Cite present; gold shapes in cite column — do not invent new algebra beyond old-path + cite.
- **Engine:** Notes still say notes-only / not this pass, but catalog generator is live (old path = default). No new skeleton this audit unless gold locks.
- **This pass:** Gallery + Limitations audit only. Implement leftover only if notes lock gold (not for flat-D / red-header variety leaves).

_topic-fit galleries: `scripts/output/topic_fit/pc_algebraic_gallery/` (log/exp/pfd/function ops/rational); `scripts/output/topic_fit/difficulty_sweep/by_course/precalculus.html` (continuous-D subset)._
