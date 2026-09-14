# Notes — `pc_limits_by_direct_evaluation` (`Limits by direct evaluation`)

> **LOW_VARIETY**

- **Course:** Precalculus
- **Category:** Precalculus — Introduction to Calculus
- **Generator:** `limit_direct_evaluation`
- **Suggested family:** other

---

## What the question should look like (D=0 vs high D)

- **Skill:** Evaluate $\lim_{x\to a} f(x)$ by direct substitution (continuous at $a$).
- **D=0:** Low-degree polynomial plug-in, e.g. $\lim_{x\to 1}(2x^{2}-3x+3)$.
- **High D (≈16–22):** Products / roots still defined at $a$ (harder arithmetic), not removable holes.
- **Must not:** Removable / jump / infinity limits (other PC limit leaves).

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for Precalc leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\lim_{x \to 1} \left(2x^{2} - 3x + 3\right)$` | `$2$` | limit |
| 8 | 101 | `$\lim_{x \to 6} (2x-1)\sqrt{x+4}$` | `$11\sqrt{10}$` | limit |
| 16 | 101 | `$\lim_{x \to 6} (2x-1)\sqrt{x+4}$` | `$11\sqrt{10}$` | limit |
| 22 | 101 | `$\lim_{x \to 6} (2x-1)\sqrt{x+4}$` | `$11\sqrt{10}$` | limit |

Opt-out flag used: _none (default live generator)_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Precalculus 2e §12.1 | https://openstax.org/books/precalculus-2e/pages/12-1-finding-limits-numerical-and-graphical-approaches | plug-in limit polynomial/rational |

Local HTML (if mined): `textbooks/openstax/html/precalculus-2e/…` or `scripts/output/example_mining/precalculus-2e/stage1/12-1-finding-limits-numerical-and-graphical-approaches.md`

## Variety notes / flags

- `LOW_VARIETY`: live D=8/16/22 often repeat the same prompt (seed=101); gold should vary poly/root products at the same D.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Limit skeleton (direct plug-in).
- **New:** only if no honest skeleton match — otherwise leave leaf (see `benchmark-old-path.mdc`).
- **Not this pass:** notes only — no generator wiring.



## Limitations

> **LIMITATIONS**

- **Variety:** Only 2 distinct prompts across D=0/8/16/22 in notes table — limited stem rotation at fixed seed.
- **OpenStax:** Cite present; gold shapes in cite column — do not invent new algebra beyond old-path + cite.
- **Engine:** Notes still say notes-only / not this pass, but catalog generator is live (old path = default). No new skeleton this audit unless gold locks.
- **This pass:** Gallery + Limitations audit only. Implement leftover only if notes lock gold (not for flat-D / red-header variety leaves).

_topic-fit galleries: `scripts/output/topic_fit/pc_algebraic_gallery/` (log/exp/pfd/function ops/rational); `scripts/output/topic_fit/difficulty_sweep/by_course/precalculus.html` (continuous-D subset)._
