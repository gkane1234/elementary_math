# Notes — `pc_limits_at_infinity` (`Limits at infinity`)

> **LOW_VARIETY**

- **Course:** Precalculus
- **Category:** Precalculus — Introduction to Calculus
- **Generator:** `limit_at_infinity`
- **Suggested family:** other

---

## What the question should look like (D=0 vs high D)

- **Skill:** Evaluate $\lim_{x\to\pm\infty} f(x)$ (end behavior / degree comparison for rationals).
- **D=0:** Simple rational or poly end behavior with an obvious horizontal asymptote.
- **High D (≈16–22):** Higher-degree numerator/denominator; still $\pm\infty$ approach (not finite $a$).
- **Must not:** Finite-$a$ removable/direct limits.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for Precalc leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\lim_{x \to \infty} \frac{3x^{2} - 3x}{5x^{2}}$` | `$\frac{3}{5}$` | limit |
| 8 | 101 | `$\lim_{x \to \infty} \frac{e^{x}}{x^{2}}$` | `$\infty$` | limit |
| 16 | 101 | `$\lim_{x \to \infty} \frac{e^{x}}{x^{2}}$` | `$\infty$` | limit |
| 22 | 101 | `$\lim_{x \to \infty} \frac{e^{x}}{x^{2}}$` | `$\infty$` | limit |

Opt-out flag used: _none (default live generator)_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Precalculus 2e §12.2 | https://openstax.org/books/precalculus-2e/pages/12-2-finding-limits-algebraic-approaches | end behavior rational |

Local HTML (if mined): `textbooks/openstax/html/precalculus-2e/…` or `scripts/output/example_mining/precalculus-2e/stage1/12-2-finding-limits-algebraic-approaches.md`

## Variety notes / flags

- `LOW_VARIETY`: D≥8 often repeats the same $\frac{e^{x}}{x^{2}}$ stem (seed=101); OpenStax §12.2 has more rational degree-compare shapes.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Limit skeleton (end behavior).
- **New:** only if no honest skeleton match — otherwise leave leaf (see `benchmark-old-path.mdc`).
- **Not this pass:** notes only — no generator wiring.



## Limitations

> **LIMITATIONS**

- **Variety:** Only 2 distinct prompts across D=0/8/16/22 in notes table — limited stem rotation at fixed seed.
- **OpenStax:** Cite present; gold shapes in cite column — do not invent new algebra beyond old-path + cite.
- **Engine:** Notes still say notes-only / not this pass, but catalog generator is live (old path = default). No new skeleton this audit unless gold locks.
- **This pass:** Gallery + Limitations audit only. Implement leftover only if notes lock gold (not for flat-D / red-header variety leaves).

_topic-fit galleries: `scripts/output/topic_fit/pc_algebraic_gallery/` (log/exp/pfd/function ops/rational); `scripts/output/topic_fit/difficulty_sweep/by_course/precalculus.html` (continuous-D subset)._
