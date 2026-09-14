# Notes — `pc_power_rule_for_differentiation` (`Power rule for differentiation`)

- **Course:** Precalculus
- **Category:** Precalculus — Introduction to Calculus
- **Generator:** `derivative_power_rule`
- **Suggested family:** other

---

## What the question should look like (D=0 vs high D)

- **Skill:** Differentiate a power / polynomial with the power rule (first derivative).
- **D=0:** Single monomial, e.g. $\frac{d}{dx}(2x^{2})$.
- **High D (≈16–22):** Fractional powers / multi-term polys; stay first-derivative (second derivative belongs on a higher-order calc leaf).
- **Must not:** Product/quotient/trig as the primary skill; equation dumps.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for Precalc leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\text{Find }\frac{d}{dx}\left(2x^{2}\right)$` | `$2x^{1}\left(2\right)$` | evaluate/rewrite |
| 8 | 101 | `$\text{Find }\frac{d}{dx}\left(5x^{3} + 5x^{2} + x + 3\right)$` | `$3x^{2}\left(5\right) + 2x^{1}\left(5\right) + 1$` | evaluate/rewrite |
| 16 | 101 | `$\frac{d}{dx}\left[x^{\frac{5}{2}}\right]$` | `$\frac{5}{2}x^{\frac{3}{2}}$` | evaluate/rewrite |
| 22 | 101 | `$\frac{d^{2}}{dx^{2}}\left[9x^{3} + 9x^{2} + 2x + 6\right]$` | `$2x^{1}\left(3\right)\left(9\right) + x^{0}\left(2\right)\left(9\right)$` | evaluate/rewrite |

Opt-out flag used: _none (default live generator)_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Precalculus 2e §12.3 | https://openstax.org/books/precalculus-2e/pages/12-3-derivatives | nx^{n-1} power rule |

Local HTML (if mined): `textbooks/openstax/html/precalculus-2e/…` or `scripts/output/example_mining/precalculus-2e/stage1/12-3-derivatives.md`

## Variety notes / flags

- Live generator produces topic-shaped prompts; OpenStax frames for WP/application leaves.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Reuse calc diff skeleton (power rule).
- **New:** only if no honest skeleton match — otherwise leave leaf (see `benchmark-old-path.mdc`).
- **Not this pass:** notes only — no generator wiring.



## Limitations

- **Variety:** Notes claim topic-shaped live stems; re-check seed diversity beyond seed=101 before treating as gold-locked.
- **Difficulty scaling:** Notes table shows stem changes with D at seed=101; confirm numeric hardness before format unlocks.
- **OpenStax:** Cite present; gold shapes in cite column — do not invent new algebra beyond old-path + cite.
- **Engine:** Notes still say notes-only / not this pass, but catalog generator is live (old path = default). No new skeleton this audit unless gold locks.
- **This pass:** Gallery + Limitations audit only. Implement leftover only if notes lock gold (not for flat-D / red-header variety leaves).

_topic-fit galleries: `scripts/output/topic_fit/pc_algebraic_gallery/` (log/exp/pfd/function ops/rational); `scripts/output/topic_fit/difficulty_sweep/by_course/precalculus.html` (continuous-D subset)._
