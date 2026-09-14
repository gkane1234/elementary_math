# Notes — `pc_approximating_area_under_a_curve` (`Approximating area under a curve`)

> **LOW_VARIETY**

- **Course:** Precalculus
- **Category:** Precalculus — Introduction to Calculus
- **Generator:** `riemann_approximate_area`
- **Suggested family:** other

---

## What the question should look like (D=0 vs high D)

- **Skill:** Approximate area with a midpoint Riemann sum (fixed rule; vary $n$ / $f$).
- **D=0:** Midpoint sum, small $n$ (e.g. $n=2$) on a simple $f$ like $f(x)=x$.
- **High D (≈16–22):** Larger $n$ and/or richer $f$ on the same midpoint stem.
- **Must not:** Exact definite-integral answers as the only path (that is the limit-of-sums / indefinite leaves).

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for Precalc leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\text{Use a midpoint Riemann sum with }2\text{ equal intervals to approximate the area under }f(x)=x\text{ on }[0,4].$` | `$8$` | evaluate/rewrite |
| 8 | 101 | `$\text{Use a midpoint Riemann sum with }2\text{ equal intervals to approximate the area under }f(x)=x\text{ on }[0,4].$` | `$8$` | evaluate/rewrite |
| 16 | 101 | `$\text{Use a midpoint Riemann sum with }4\text{ equal intervals to approximate the area under }f(x)=x\text{ on }[0,4].$` | `$8$` | evaluate/rewrite |
| 22 | 101 | `$\text{Use a midpoint Riemann sum with }4\text{ equal intervals to approximate the area under }f(x)=x\text{ on }[0,4].$` | `$8$` | evaluate/rewrite |

Opt-out flag used: _none (default live generator)_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Precalculus 2e §12.5 | https://openstax.org/books/precalculus-2e/pages/12-5-definite-integrals | Riemann sum midpoint |

Local HTML (if mined): `textbooks/openstax/html/precalculus-2e/…` or `scripts/output/example_mining/precalculus-2e/stage1/12-5-definite-integrals.md`

## Variety notes / flags

- `LOW_VARIETY`: live old path keeps the same midpoint wording; D mainly changes $n$ (2→4) on $f(x)=x$ — OpenStax §12.5 has more $f$ / endpoint variants. Answer shape is also flat across D.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Riemann sum constructive.
- **New:** only if no honest skeleton match — otherwise leave leaf (see `benchmark-old-path.mdc`).
- **Not this pass:** notes only — no generator wiring.



## Limitations

> **LIMITATIONS**

- **Variety:** Only 2 distinct prompts across D=0/8/16/22 in notes table — limited stem rotation at fixed seed.
- **Difficulty scaling:** Answer latex flat across D in notes table — D may be cosmetic until form unlocks change the student-visible stem.
- **OpenStax:** Cite present; gold shapes in cite column — do not invent new algebra beyond old-path + cite.
- **Engine:** Notes still say notes-only / not this pass, but catalog generator is live (old path = default). No new skeleton this audit unless gold locks.
- **This pass:** Gallery + Limitations audit only. Implement leftover only if notes lock gold (not for flat-D / red-header variety leaves).

_topic-fit galleries: `scripts/output/topic_fit/pc_algebraic_gallery/` (log/exp/pfd/function ops/rational); `scripts/output/topic_fit/difficulty_sweep/by_course/precalculus.html` (continuous-D subset)._
