# Notes — `pc_continuity` (`Continuity`)

- **Course:** Precalculus
- **Category:** Precalculus — Functions
- **Generator:** `pc_continuity`
- **Suggested family:** other

---

## What the question should look like (D=0 vs high D)

- **Skill:** Decide if a piecewise function is continuous at a point.
- **D=0:** Matching one-sided values at $0$ → Yes (OpenStax PC §1.3).
- **High D (≈16–22):** include discontinuous jumps (No).
- **Must not:** full Calc-style discontinuity classification taxonomy on this leaf.

## What live path produced (real latex, D=0/8/16/22)

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$f(x)=\begin{cases}x+1,&x<0\\1,&x\ge0\end{cases}.\quad\text{Is }f\text{ continuous at }0?$` | `$Yes$` | continuous |
| 8 | 101 | `$f(x)=\begin{cases}x-1,&x<0\\0,&x\ge0\end{cases}.\quad\text{Is }f\text{ continuous at }0?$` | `$No$` | jump |
| 16 | 101 | `$f(x)=\begin{cases}x+3,&x<0\\4,&x\ge0\end{cases}.\quad\text{Is }f\text{ continuous at }0?$` | `$No$` | jump |
| 22 | 101 | `$f(x)=\begin{cases}x+3,&x<0\\4,&x\ge0\end{cases}.\quad\text{Is }f\text{ continuous at }0?$` | `$No$` | jump |

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Precalculus 2e §1.3 | https://openstax.org/books/precalculus-2e/pages/1-3-rates-of-change-and-behavior-of-graphs | continuity at a point from piecewise |

## Proposed engine

- **Named:** `pc_continuity` — yes/no continuous at breakpoint (PC-shaped, not Calc classify).

## Limitations

- **Difficulty scaling:** Notes table shows stem changes with D at seed=101; confirm numeric hardness before format unlocks.
- **OpenStax:** Cite present; gold shapes in cite column — do not invent new algebra beyond old-path + cite.
- **Engine:** Live catalog generator; no deferred precalc_foundations stub (PC_DEFERRED empty).
- **This pass:** Gallery + Limitations audit only. Implement leftover only if notes lock gold (not for flat-D / red-header variety leaves).
