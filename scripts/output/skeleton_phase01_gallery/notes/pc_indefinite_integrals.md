# Notes — `pc_indefinite_integrals` (`Indefinite integrals`)

- **Course:** Precalculus
- **Category:** Precalculus — Introduction to Calculus
- **Generator:** `integral_power_rule`
- **Suggested family:** other

---

## What the question should look like (D=0 vs high D)

- **Skill:** Antiderivative via the power rule; include $+C$.
- **D=0:** Constant or single monomial, e.g. $\int 3\,dx$.
- **High D (≈16–22):** Multi-term polynomials (still power rule — no parts / trig sub).
- **Must not:** Definite-integral numeric area as the only ask; advanced techniques.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for Precalc leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\int 3 \, dx$` | `$3x+C$` | evaluate/rewrite |
| 8 | 101 | `$\int -3x^{4} + 3 \, dx$` | `$3x-\frac{3}{5}x^{5}+C$` | evaluate/rewrite |
| 16 | 101 | `$\int 6x^{4} + 2 \, dx$` | `$2x+\frac{6}{5}x^{5}+C$` | evaluate/rewrite |
| 22 | 101 | `$\int 3x^{4} - 2 \, dx$` | `$-2x+\frac{3}{5}x^{5}+C$` | evaluate/rewrite |

Opt-out flag used: _none (default live generator)_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Precalculus 2e §12.5 | https://openstax.org/books/precalculus-2e/pages/12-5-definite-integrals | antiderivative power rule |

Local HTML (if mined): `textbooks/openstax/html/precalculus-2e/…` or `scripts/output/example_mining/precalculus-2e/stage1/12-5-definite-integrals.md`

## Variety notes / flags

- Live generator produces topic-shaped prompts; OpenStax frames for WP/application leaves.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Integral power-rule skeleton.
- **New:** only if no honest skeleton match — otherwise leave leaf (see `benchmark-old-path.mdc`).
- **Not this pass:** notes only — no generator wiring.



## Limitations

- **Variety:** Notes claim topic-shaped live stems; re-check seed diversity beyond seed=101 before treating as gold-locked.
- **Difficulty scaling:** Notes table shows stem changes with D at seed=101; confirm numeric hardness before format unlocks.
- **OpenStax:** Cite present; gold shapes in cite column — do not invent new algebra beyond old-path + cite.
- **Engine:** Notes still say notes-only / not this pass, but catalog generator is live (old path = default). No new skeleton this audit unless gold locks.
- **This pass:** Gallery + Limitations audit only. Implement leftover only if notes lock gold (not for flat-D / red-header variety leaves).

_topic-fit galleries: `scripts/output/topic_fit/pc_algebraic_gallery/` (log/exp/pfd/function ops/rational); `scripts/output/topic_fit/difficulty_sweep/by_course/precalculus.html` (continuous-D subset)._
