# Notes — `pc_partial_fraction_decomposition` (`Partial fraction decomposition`)

- **Course:** Precalculus
- **Category:** Precalculus — Matrices and Systems
- **Generator:** `partial_fraction_decomposition`
- **Suggested family:** other

---

## What the question should look like (D=0 vs high D)

- **Skill:** Student decompose the expression for partial fraction decomposition.
- **D=0:** decompose proper rational; simplest numeric/instance (per OpenStax § easy exercises).
- **High D (≈16–22):** harder coefficients, more factors/steps, or extra format (e.g. general solution for trig, higher-degree PFD).
- **Must not:** wrong-topic shapes, equation dump without context on WP leaves, calc topics on algebra-only skeletons.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for Precalc leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\text{Decompose } \frac{x + 5}{x^{2} + x - 2}$` | `$\frac{-1}{x + 2}+\frac{2}{x - 1}$` | PFD |
| 8 | 101 | `$\text{Decompose } \frac{6x^{2} - 3x - 75}{3\left(x + 2\right)\left(x - 1\right)\left(x - 3\right)}$` | `$\frac{-1}{x + 2}+\frac{4}{x - 1}+\frac{-1}{x - 3}$` | PFD |
| 16 | 101 | `$\text{Decompose } \frac{3x^{2} + 24x + 96}{3x^{3} + 6x^{2} + 48x + 96}$` | `$\frac{1}{x + 2}+\frac{8}{x^{2} + 16}$` | PFD |
| 22 | 101 | `$\text{Decompose } \frac{-3x^{2} + 24x + 48}{3x^{3} + 12x^{2} + 48x + 192}$` | `$\frac{-1}{x + 4}+\frac{8}{x^{2} + 16}$` | PFD |

Opt-out flag used: _none (default live generator)_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Precalculus 2e §3.7 | https://openstax.org/books/precalculus-2e/pages/3-7-rational-functions | decompose proper rational |

Local HTML (if mined): `textbooks/openstax/html/precalculus-2e/…` or `scripts/output/example_mining/precalculus-2e/stage1/3-7-rational-functions.md`

## Variety notes / flags

- Live generator produces topic-shaped prompts; OpenStax frames for WP/application leaves.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Reuse constructive_pfd / rational reverse.
- **New:** only if no honest skeleton match — otherwise leave leaf (see `benchmark-old-path.mdc`).
- **Not this pass:** notes only — no generator wiring.



## Limitations

- **Variety:** Notes claim topic-shaped live stems; re-check seed diversity beyond seed=101 before treating as gold-locked.
- **Difficulty scaling:** Notes table shows stem changes with D at seed=101; confirm numeric hardness before format unlocks.
- **OpenStax:** Cite present; gold shapes in cite column — do not invent new algebra beyond old-path + cite.
- **Engine:** Notes still say notes-only / not this pass, but catalog generator is live (old path = default). No new skeleton this audit unless gold locks.
- **This pass:** Gallery + Limitations audit only. Implement leftover only if notes lock gold (not for flat-D / red-header variety leaves).

_topic-fit galleries: `scripts/output/topic_fit/pc_algebraic_gallery/` (log/exp/pfd/function ops/rational); `scripts/output/topic_fit/difficulty_sweep/by_course/precalculus.html` (continuous-D subset)._
