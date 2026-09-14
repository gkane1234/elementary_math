# Notes — `pc_definition_of_the_derivative` (`Definition of the derivative`)

- **Course:** Precalculus
- **Category:** Precalculus — Introduction to Calculus
- **Generator:** `definition_of_derivative`
- **Suggested family:** other

---

## What the question should look like (D=0 vs high D)

- **Skill:** Use the limit definition of $f'(a)$ (difference quotient), or a canceling secant limit that motivates it.
- **D=0:** Simple canceling rational limit, e.g. $\lim_{x\to 1}\frac{x^{2}-1}{x-1}$, or $f'(a)$ for $f(x)=cx^{2}$.
- **High D (≈16–22):** Explicit $\lim_{h\to 0}\frac{f(a+h)-f(a)}{h}$ with larger coefficients / quadratic $f$.
- **Must not:** Pure power-rule “find $f'$” without a limit / definition stem.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for Precalc leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\lim_{x\to 1}\frac{x^{2}-1}{x-1}$` | `$2$` | limit |
| 8 | 101 | `$\text{Use the definition to find }f'(2)\text{ for }f(x)=3x^{2}.$` | `$12$` | evaluate/rewrite |
| 16 | 101 | `$\lim_{h\to 0}\frac{4(5+h)^{2}-100}{h}$` | `$40$` | limit |
| 22 | 101 | `$\lim_{h\to 0}\frac{4(5+h)^{2}-100}{h}$` | `$40$` | limit |

Opt-out flag used: _none (default live generator)_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Precalculus 2e §12.3 | https://openstax.org/books/precalculus-2e/pages/12-3-derivatives | limit definition f'(a) |

Local HTML (if mined): `textbooks/openstax/html/precalculus-2e/…` or `scripts/output/example_mining/precalculus-2e/stage1/12-3-derivatives.md`

## Variety notes / flags

- Live generator produces topic-shaped prompts; OpenStax frames for WP/application leaves.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Derivative definition limit skeleton.
- **New:** only if no honest skeleton match — otherwise leave leaf (see `benchmark-old-path.mdc`).
- **Not this pass:** notes only — no generator wiring.



## Limitations

- **Variety:** Notes claim topic-shaped live stems; re-check seed diversity beyond seed=101 before treating as gold-locked.
- **Difficulty scaling:** Notes table shows stem changes with D at seed=101; confirm numeric hardness before format unlocks.
- **OpenStax:** Cite present; gold shapes in cite column — do not invent new algebra beyond old-path + cite.
- **Engine:** Notes still say notes-only / not this pass, but catalog generator is live (old path = default). No new skeleton this audit unless gold locks.
- **This pass:** Gallery + Limitations audit only. Implement leftover only if notes lock gold (not for flat-D / red-header variety leaves).

_topic-fit galleries: `scripts/output/topic_fit/pc_algebraic_gallery/` (log/exp/pfd/function ops/rational); `scripts/output/topic_fit/difficulty_sweep/by_course/precalculus.html` (continuous-D subset)._
