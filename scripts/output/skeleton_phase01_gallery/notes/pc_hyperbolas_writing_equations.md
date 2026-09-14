# Notes — `pc_hyperbolas_writing_equations` (`Hyperbolas, writing equations`)

- **Course:** Precalculus
- **Category:** Precalculus — Conic Sections
- **Generator:** `conic_sections`
- **Suggested family:** other

---

## What the question should look like (D=0 vs high D)

- **Skill:** Student write the equation of the hyperbola for hyperbolas, writing equations.
- **D=0:** write hyperbola from foci; simplest numeric/instance (per OpenStax § easy exercises).
- **High D (≈16–22):** harder coefficients, more factors/steps, or extra format (e.g. general solution for trig, higher-degree PFD).
- **Must not:** wrong-topic shapes, equation dump without context on WP leaves, calc topics on algebra-only skeletons.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for Precalc leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\text{Write the equation of a vertical hyperbola centered at the origin with }a=3\text{ and }b=4.$` | `$\frac{y^2}{9}-\frac{x^2}{16}=1$` | evaluate/rewrite |
| 8 | 101 | `$\text{Write the equation of a vertical hyperbola centered at the origin with }a=6\text{ and }b=3.$` | `$\frac{y^2}{36}-\frac{x^2}{9}=1$` | evaluate/rewrite |
| 16 | 101 | `$\text{Write the equation of a vertical hyperbola centered at the origin with }a=5\text{ and }b=7.$` | `$\frac{y^2}{25}-\frac{x^2}{49}=1$` | evaluate/rewrite |
| 22 | 101 | `$\text{Write the equation of a vertical hyperbola centered at the origin with }a=11\text{ and }b=5.$` | `$\frac{y^2}{121}-\frac{x^2}{25}=1$` | evaluate/rewrite |

Opt-out flag used: _none (default live generator)_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Precalculus 2e §10.4 | https://openstax.org/books/precalculus-2e/pages/10-4-the-hyperbola | write hyperbola from foci |

Local HTML (if mined): `textbooks/openstax/html/precalculus-2e/…` or `scripts/output/example_mining/precalculus-2e/stage1/10-4-the-hyperbola.md`

## Variety notes / flags

- Live generator produces topic-shaped prompts; OpenStax frames for WP/application leaves.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Conic write/graph constructive.
- **New:** only if no honest skeleton match — otherwise leave leaf (see `benchmark-old-path.mdc`).
- **Not this pass:** notes only — no generator wiring.



## Limitations

- **Variety:** Notes claim topic-shaped live stems; re-check seed diversity beyond seed=101 before treating as gold-locked.
- **Difficulty scaling:** Notes table shows stem changes with D at seed=101; confirm numeric hardness before format unlocks.
- **OpenStax:** Cite present; gold shapes in cite column — do not invent new algebra beyond old-path + cite.
- **Engine:** Notes still say notes-only / not this pass, but catalog generator is live (old path = default). No new skeleton this audit unless gold locks.
- **This pass:** Gallery + Limitations audit only. Implement leftover only if notes lock gold (not for flat-D / red-header variety leaves).

_topic-fit galleries: `scripts/output/topic_fit/pc_algebraic_gallery/` (log/exp/pfd/function ops/rational); `scripts/output/topic_fit/difficulty_sweep/by_course/precalculus.html` (continuous-D subset)._
