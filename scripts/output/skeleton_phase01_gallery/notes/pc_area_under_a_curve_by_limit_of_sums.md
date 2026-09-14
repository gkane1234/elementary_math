# Notes — `pc_area_under_a_curve_by_limit_of_sums` (`Area under a curve by limit of sums`)

- **Course:** Precalculus
- **Category:** Precalculus — Introduction to Calculus
- **Generator:** `area_under_curve`
- **Suggested family:** other

---

## What the question should look like (D=0 vs high D)

- **Skill:** Exact area as a definite integral / limit of Riemann sums (not a midpoint approximation drill).
- **D=0:** Simple continuous $f$ on a short interval; exact value via FTC / power antiderivative.
- **High D (≈16–22):** Higher-degree $f$ or longer setup toward $\lim_{n\to\infty}$ sum notation.
- **Must not:** Midpoint-only approximation stems (that is `pc_approximating_area_under_a_curve`).

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for Precalc leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\text{Find the area under }y=x\text{ from }x=0\text{ to }x=3.$` | `$\frac{9}{2}$` | evaluate/rewrite |
| 8 | 101 | `$\text{Find the area under }y=x\text{ from }x=0\text{ to }x=2.$` | `$2$` | evaluate/rewrite |
| 16 | 101 | `$\text{Find the area under }y=x\text{ from }x=0\text{ to }x=6.$` | `$18$` | evaluate/rewrite |
| 22 | 101 | `$\text{Find the area under }y=x^{2}\text{ from }x=0\text{ to }x=4.$` | `$\frac{64}{3}$` | evaluate/rewrite |

Opt-out flag used: _none (default live generator)_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Precalculus 2e §12.5 | https://openstax.org/books/precalculus-2e/pages/12-5-definite-integrals | exact area ∫ or limit of sums |

Local HTML (if mined): `textbooks/openstax/html/precalculus-2e/…` or `scripts/output/example_mining/precalculus-2e/stage1/12-5-definite-integrals.md`

## Variety notes / flags

- Live generator produces topic-shaped prompts; OpenStax frames for WP/application leaves.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Area under curve constructive.
- **New:** only if no honest skeleton match — otherwise leave leaf (see `benchmark-old-path.mdc`).
- **Not this pass:** notes only — no generator wiring.



## Limitations

- **Variety:** Notes claim topic-shaped live stems; re-check seed diversity beyond seed=101 before treating as gold-locked.
- **Difficulty scaling:** Notes table shows stem changes with D at seed=101; confirm numeric hardness before format unlocks.
- **OpenStax:** Cite present; gold shapes in cite column — do not invent new algebra beyond old-path + cite.
- **Engine:** Notes still say notes-only / not this pass, but catalog generator is live (old path = default). No new skeleton this audit unless gold locks.
- **This pass:** Gallery + Limitations audit only. Implement leftover only if notes lock gold (not for flat-D / red-header variety leaves).

_topic-fit galleries: `scripts/output/topic_fit/pc_algebraic_gallery/` (log/exp/pfd/function ops/rational); `scripts/output/topic_fit/difficulty_sweep/by_course/precalculus.html` (continuous-D subset)._
