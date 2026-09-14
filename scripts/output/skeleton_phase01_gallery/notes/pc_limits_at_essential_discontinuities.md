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

- **Status:** leftover lockout of D=0 \(1/x\) ships on the shared `limit_essential` generator (see `calc_limits_at_essential_discontinuities.md`). Remaining: D=16===D=22 osc/VA/tan mix; D=8 can still emit leftover \(1/x\); tan is frozen \(x\to\pi/2\); no figure-bank graphs.
- **Variety:** Multi-seed pool now spans leftover \(1/x\) at D=8 plus osc/VA/tan; fixed seed 101 is still the same shifted \(\cos(1/x)\) from D=8 through D=22.
- **OpenStax:** Cite present; gold shapes in cite column — do not invent new algebra beyond old-path + cite.
- **Engine:** Live catalog generator; leftover lockout is on the shared calc leaf.
