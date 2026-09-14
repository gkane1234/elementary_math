# Notes — `pc_equations_with_factoring_and_fundamental_identities` (`Equations with factoring and fundamental identities`)

> **LOW_VARIETY**

- **Course:** Precalculus
- **Category:** Precalculus — Trigonometry
- **Generator:** `trig_factoring_equations`
- **Suggested family:** other

---

## What the question should look like (D=0 vs high D)

- **Skill:** Student solve for x for equations with factoring and fundamental identities.
- **D=0:** factor after identity rewrite; simplest numeric/instance (per OpenStax § easy exercises).
- **High D (≈16–22):** harder coefficients, more factors/steps, or extra format (e.g. general solution for trig, higher-degree PFD).
- **Must not:** wrong-topic shapes, equation dump without context on WP leaves, calc topics on algebra-only skeletons.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for Precalc leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\text{Solve }2\sin^2\theta-\sin\theta=0\text{ for }0\le\theta<2\pi.$` | `$\theta=0,\frac{\pi}{6},\pi,\frac{5\pi}{6}$` | solve |
| 8 | 101 | `$\text{Solve }\cos(2\theta)=0\text{ for }0\le\theta<\pi.$` | `$\theta=\frac{\pi}{4},\frac{3\pi}{4}$` | solve |
| 16 | 101 | `$\text{Solve }2\sin^2\theta-\sin\theta=0\text{ for }0\le\theta<2\pi.$` | `$\theta=0,\frac{\pi}{6},\pi,\frac{5\pi}{6}$` | solve |
| 22 | 101 | `$\text{Solve }2\sin\theta\cos\theta=0\text{ for }0\le\theta<2\pi.$` | `$\theta=0,\frac{\pi}{2},\pi,\frac{3\pi}{2}$` | solve |

Opt-out flag used: _none (default live generator)_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Precalculus 2e §7.5 | https://openstax.org/books/precalculus-2e/pages/7-5-solving-trigonometric-equations | factor after identity rewrite |

Local HTML (if mined): `textbooks/openstax/html/precalculus-2e/…` or `scripts/output/example_mining/precalculus-2e/stage1/7-5-solving-trigonometric-equations.md`

## Variety notes / flags

- Live generator produces topic-shaped prompts; OpenStax frames for WP/application leaves.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Trig eqn skeleton with factor step.
- **Wired:** `trig_skeleton.TrigFactorEq` is live default for this leaf; opt-out `use_sample_trig_equations=True`.
- D=0 quadratic-in-trig; factor / double-angle unlock at higher D.



## Limitations

> **LIMITATIONS**

- **Variety:** Notes claim topic-shaped live stems; re-check seed diversity beyond seed=101 before treating as gold-locked.
- **Trig equations:** OpenStax PC §7.5 wants sin/cos/tan = k, factoring, and multiple-angle forms across seeds; flat D (same stem) stays red-header until the equation catalog expands.
- **Difficulty scaling:** Notes table shows stem changes with D at seed=101; confirm numeric hardness before format unlocks.
- **OpenStax:** Cite present; gold shapes in cite column — do not invent new algebra beyond old-path + cite.
- **Engine:** Live skeleton/reuse default — limitations are variety/D/OpenStax coverage, not a missing engine.
- **This pass:** Gallery + Limitations audit only. Implement leftover only if notes lock gold (not for flat-D / red-header variety leaves).

_topic-fit galleries: `scripts/output/topic_fit/pc_algebraic_gallery/` (log/exp/pfd/function ops/rational); `scripts/output/topic_fit/difficulty_sweep/by_course/precalculus.html` (continuous-D subset)._
