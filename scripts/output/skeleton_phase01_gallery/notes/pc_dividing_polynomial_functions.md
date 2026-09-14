# Notes — `pc_dividing_polynomial_functions` (`Dividing polynomial functions`)

- **Course:** Precalculus
- **Category:** Precalculus — Power, Polynomial, and Rational Functions
- **Generator:** `polynomial_long_division`
- **Suggested family:** other

---

## What the question should look like (D=0 vs high D)

- **Skill:** Student divide for dividing polynomial functions.
- **D=0:** long/synthetic division; simplest numeric/instance (per OpenStax § easy exercises).
- **High D (≈16–22):** harder coefficients, more factors/steps, or extra format (e.g. general solution for trig, higher-degree PFD).
- **Must not:** wrong-topic shapes, equation dump without context on WP leaves, calc topics on algebra-only skeletons.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for Precalc leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\frac{4x^{3}-3x^{2}-6x-8}{x-2}$` | `$4x^{2}+5x+4$` | evaluate/rewrite |
| 8 | 101 | `$\frac{6x^{4}+12x^{3}-4x^{2}-10x-16}{2x^{2}+2x+2}$` | `$3x^{2}+3x-8$` | evaluate/rewrite |
| 16 | 101 | `$\frac{24x^{5}-146x^{4}-54x^{3}+232x^{2}+26x-75}{12x^{2}-x-9}$` | `$2x^{3}-12x^{2}-4x+10+\frac{15}{12x^{2}-x-9}$` | evaluate/rewrite |
| 22 | 101 | `$\frac{77x^{4}-65x^{3}+65x^{2}-160x-12}{7x^{2}+3x+11}$` | `$11x^{2}-14x-2+\frac{10}{7x^{2}+3x+11}$` | evaluate/rewrite |

Opt-out flag used: _none (default live generator)_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Precalculus 2e §3.5 | https://openstax.org/books/precalculus-2e/pages/3-5-dividing-polynomials | long/synthetic division |

Local HTML (if mined): `textbooks/openstax/html/precalculus-2e/…` or `scripts/output/example_mining/precalculus-2e/stage1/3-5-dividing-polynomials.md`

## Variety notes / flags

- Live generator produces topic-shaped prompts; OpenStax frames for WP/application leaves.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Reuse poly long-division skeleton.
- **New:** only if no honest skeleton match — otherwise leave leaf (see `benchmark-old-path.mdc`).
- **Not this pass:** notes only — no generator wiring.



## Limitations

- **Variety:** Notes claim topic-shaped live stems; re-check seed diversity beyond seed=101 before treating as gold-locked.
- **Difficulty scaling:** Notes table shows stem changes with D at seed=101; confirm numeric hardness before format unlocks.
- **OpenStax:** Cite present; gold shapes in cite column — do not invent new algebra beyond old-path + cite.
- **Engine:** Notes still say notes-only / not this pass, but catalog generator is live (old path = default). No new skeleton this audit unless gold locks.
- **This pass:** Gallery + Limitations audit only. Implement leftover only if notes lock gold (not for flat-D / red-header variety leaves).

_topic-fit galleries: `scripts/output/topic_fit/pc_algebraic_gallery/` (log/exp/pfd/function ops/rational); `scripts/output/topic_fit/difficulty_sweep/by_course/precalculus.html` (continuous-D subset)._
