# Notes — `pc_limits_at_kinks_and_jumps` (`Limits at kinks and jumps`)

- **Course:** Precalculus
- **Category:** Precalculus — Introduction to Calculus
- **Generator:** `limit_jump`
- **Suggested family:** other

---

## What the question should look like (D=0 vs high D)

- **Skill:** Decide whether a two-sided (or one-sided) limit exists at a piecewise jump/kink.
- **D=0:** Constant-vs-constant piecewise; answer DNE (OpenStax-style jump).
- **High D (≈16–22):** linear/poly pieces; occasional one-sided prompts.
- **Must not:** removable cancel / essential $1/x^p$ (other leaves).

## What live path produced (real latex, D=0/8/16/22)

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\lim_{x \to 5} f(x)\text{ where }f(x)=\begin{cases}3&x<5\\-3&x\ge 5\end{cases}$` | `$\text{DNE}$` | const jump |
| 8 | 101 | `$\lim_{x \to 5} f(x)\text{ where }f(x)=\begin{cases}3x - 3&x<5\\2&x\ge 5\end{cases}$` | `$\text{DNE}$` | linear vs const |
| 16 | 101 | `$\lim_{x \to 5^{+}} f(x)\text{ where }f(x)=\begin{cases}2x^{2} + x + 6&x<5\\-4&x\ge 5\end{cases}$` | `$-4$` | one-sided |
| 22 | 101 | `$\lim_{x \to 5^{+}} f(x)\text{ where }f(x)=\begin{cases}2x^{2} - x + 3&x<5\\6&x\ge 5\end{cases}$` | `$6$` | one-sided |

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Precalculus 2e §12.1 | https://openstax.org/books/precalculus-2e/pages/12-1-finding-limits-numerical-and-graphical-approaches | one-sided / jump at piecewise |
| OpenStax Calculus Volume 1 §2.4 | https://openstax.org/books/calculus-volume-1/pages/2-4-continuity | piecewise jump continuity |

## Proposed engine

- **Reuse:** LimitSpec `limit_jump` (shared with Calc).

## Limitations

- **Difficulty scaling:** Notes table shows stem changes with D at seed=101; confirm numeric hardness before format unlocks.
- **OpenStax:** Cite present; gold shapes in cite column — do not invent new algebra beyond old-path + cite.
- **Engine:** Live catalog generator; no deferred precalc_foundations stub (PC_DEFERRED empty).
- **This pass:** Gallery + Limitations audit only. Implement leftover only if notes lock gold (not for flat-D / red-header variety leaves).
