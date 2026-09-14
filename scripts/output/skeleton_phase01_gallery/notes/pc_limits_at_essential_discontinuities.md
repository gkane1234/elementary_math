# Notes — `pc_limits_at_essential_discontinuities` (`Limits at essential discontinuities`)

- **Course:** Precalculus
- **Category:** Precalculus — Introduction to Calculus
- **Generator:** `limit_essential`
- **Suggested family:** other

---

## What the question should look like (D=0 vs high D)

- **Skill:** Recognize limits that do not exist at essential discontinuities.
- **D=0:** $\lim_{x\to0}1/x$ → DNE.
- **High D (≈16–22):** oscillatory essentials (e.g. $\cos(1/(x-a))$).
- **Must not:** removable factor / jump piecewise (other leaves).

## What live path produced (real latex, D=0/8/16/22)

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\lim_{x \to 0} \frac{1}{x}$` | `$\text{DNE}$` | $1/x$ |
| 8 | 101 | `$\lim_{x \to -4} \cos\left(\frac{1}{(x+4)}\right)$` | `$\text{DNE}$` | oscillatory |
| 16 | 101 | `$\lim_{x \to -4} \cos\left(\frac{1}{(x+4)}\right)$` | `$\text{DNE}$` | oscillatory |
| 22 | 101 | `$\lim_{x \to -4} \cos\left(\frac{1}{(x+4)}\right)$` | `$\text{DNE}$` | oscillatory |

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Precalculus 2e §12.2 | https://openstax.org/books/precalculus-2e/pages/12-2-finding-limits-properties-of-limits | essential / infinite / oscillatory DNE |

## Proposed engine

- **Reuse:** LimitSpec `limit_essential`.

## Limitations

> **LIMITATIONS**

- **Variety:** Only 2 distinct prompts across D=0/8/16/22 in notes table — limited stem rotation at fixed seed.
- **Difficulty scaling:** Answer latex flat across D in notes table — D may be cosmetic until form unlocks change the student-visible stem.
- **OpenStax:** Cite present; gold shapes in cite column — do not invent new algebra beyond old-path + cite.
- **Engine:** Live catalog generator; no deferred precalc_foundations stub (PC_DEFERRED empty).
- **This pass:** Gallery + Limitations audit only. Implement leftover only if notes lock gold (not for flat-D / red-header variety leaves).
