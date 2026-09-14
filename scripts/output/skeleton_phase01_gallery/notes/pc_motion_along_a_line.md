# Notes — `pc_motion_along_a_line` (`Motion along a line`)

- **Course:** Precalculus
- **Category:** Precalculus — Introduction to Calculus
- **Generator:** `precalc_foundations`
- **Suggested family:** wp

---

## What the question should look like (D=0 vs high D)

- **Skill:** Student solve the problem for motion along a line.
- **D=0:** velocity from s(t); simplest numeric/instance (per OpenStax § easy exercises).
- **High D (≈16–22):** harder coefficients, more factors/steps, or extra format (e.g. general solution for trig, higher-degree PFD).
- **Must not:** wrong-topic shapes, equation dump without context on WP leaves, calc topics on algebra-only skeletons.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for Precalc leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$s(t)=t^2+6t.\quad\text{Find }v(2).$` | `$10$` | evaluate/rewrite |
| 8 | 101 | `$s(t)=t^2+6t.\quad\text{Find }v(2).$` | `$10$` | evaluate/rewrite |
| 16 | 101 | `$s(t)=t^2+5t.\quad\text{Find }v(2).$` | `$9$` | evaluate/rewrite |
| 22 | 101 | `$s(t)=t^2+6t.\quad\text{Find }v(2).$` | `$10$` | evaluate/rewrite |

Opt-out flag used: _none (default live generator)_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Precalculus 2e §12.3 | https://openstax.org/books/precalculus-2e/pages/12-3-derivatives | velocity from s(t) |

Local HTML (if mined): `textbooks/openstax/html/precalculus-2e/…` or `scripts/output/example_mining/precalculus-2e/stage1/12-3-derivatives.md`

## Variety notes / flags

- Uses `precalc_foundations` topic branch (thin but topic-shaped).

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Keep live `precalc_foundations` until dedicated skeleton; split topic branches per OpenStax section. Topic key `pc_motion_along_a_line`.
- **New:** only if no honest skeleton match — otherwise leave leaf (see `benchmark-old-path.mdc`).
- **Not this pass:** notes only — no generator wiring.



## Limitations

> **LIMITATIONS**

- **Variety:** Only 2 distinct prompts across D=0/8/16/22 in notes table — limited stem rotation at fixed seed.
- **OpenStax:** Cite present; gold shapes in cite column — do not invent new algebra beyond old-path + cite.
- **Engine:** Notes still say notes-only / not this pass, but catalog generator is live (old path = default). No new skeleton this audit unless gold locks.
- **This pass:** Gallery + Limitations audit only. Implement leftover only if notes lock gold (not for flat-D / red-header variety leaves).

_topic-fit galleries: `scripts/output/topic_fit/pc_algebraic_gallery/` (log/exp/pfd/function ops/rational); `scripts/output/topic_fit/difficulty_sweep/by_course/precalculus.html` (continuous-D subset)._
