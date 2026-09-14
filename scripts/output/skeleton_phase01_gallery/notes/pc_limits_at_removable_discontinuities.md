# Notes — `pc_limits_at_removable_discontinuities` (`Limits at removable discontinuities`)

- **Course:** Precalculus
- **Category:** Precalculus — Introduction to Calculus
- **Generator:** `limit_removable`
- **Suggested family:** other

---

## What the question should look like (D=0 vs high D)

- **Skill:** Evaluate a limit at a removable hole by canceling a common factor, then substituting.
- **D=0:** Simple $\frac{(x-a)(\cdots)}{x-a}$ cancel, then plug in.
- **High D (≈16–22):** Higher-degree factors / messier cancel algebra (still removable, not essential).
- **Must not:** Direct-plug continuous limits; jump/essential discontinuities.

## What old path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path. No skeleton opt-out — live generator **is** the old path for Precalc leaves.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\lim_{x \to 2} \frac{x^{2}-4}{x-2}$` | `$4$` | limit |
| 8 | 101 | `$\lim_{x \to 2} \frac{x^{2}-5x+6}{x-2}$` | `$-1$` | limit |
| 16 | 101 | `$\lim_{x \to 2} \frac{\sqrt{x}-\sqrt{2}}{x-2}$` | `$\frac{1}{2\sqrt{2}}$` | limit |
| 22 | 101 | `$\lim_{x \to 2} \frac{\sqrt{x}-\sqrt{2}}{x-2}$` | `$\frac{1}{2\sqrt{2}}$` | limit |

Opt-out flag used: _none (default live generator)_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Precalculus 2e §12.1 | https://openstax.org/books/precalculus-2e/pages/12-1-finding-limits-numerical-and-graphical-approaches | hole / cancel factor |

Local HTML (if mined): `textbooks/openstax/html/precalculus-2e/…` or `scripts/output/example_mining/precalculus-2e/stage1/12-1-finding-limits-numerical-and-graphical-approaches.md`

## Variety notes / flags

- Live generator produces topic-shaped prompts; OpenStax frames for WP/application leaves.

## Proposed engine (reuse vs new) — proposal only

- **Reuse:** Limit skeleton (factor cancel).
- **New:** only if no honest skeleton match — otherwise leave leaf (see `benchmark-old-path.mdc`).
- **Not this pass:** notes only — no generator wiring.



## Limitations

- **Variety:** Notes claim topic-shaped live stems; re-check seed diversity beyond seed=101 before treating as gold-locked.
- **Difficulty scaling:** Notes table shows stem changes with D at seed=101; confirm numeric hardness before format unlocks.
- **OpenStax:** Cite present; gold shapes in cite column — do not invent new algebra beyond old-path + cite.
- **Engine:** Notes still say notes-only / not this pass, but catalog generator is live (old path = default). No new skeleton this audit unless gold locks.
- **This pass:** Gallery + Limitations audit only. Implement leftover only if notes lock gold (not for flat-D / red-header variety leaves).

_topic-fit galleries: `scripts/output/topic_fit/pc_algebraic_gallery/` (log/exp/pfd/function ops/rational); `scripts/output/topic_fit/difficulty_sweep/by_course/precalculus.html` (continuous-D subset)._
