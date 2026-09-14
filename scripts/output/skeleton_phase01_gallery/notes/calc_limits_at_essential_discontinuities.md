# Notes — `calc_limits_at_essential_discontinuities` (`At essential discontinuities`)

- **Course:** Calculus
- **Category:** Calculus — Limits
- **Generator:** `limit_essential`
- **Suggested family:** other (calc limits / Diff)

---

## Limitations

- **Status:** shipped — live generator
- **Generator:** `limit_essential`
- **Remaining limits:** LimitSpec packs ship. Remaining gaps: form_id metadata sometimes mismatches latex (e.g. `direct_sqrt` stamp on rational plug-in); one-sided / piecewise story variety thinner than OpenStax §2.2–2.4 exercise banks; no dedicated limit-skeleton patterns beyond packs.

## What the question should look like (D=0 vs high D)

- **Skill:** Recognize limits that DNE at vertical asymptotes / wild oscillation (essential).
- **D=0:** lim_{x→0} 1/x → DNE.
- **High D (≈16–22):** 1/x², sin(1/x), cos(1/x), tan asymptotes — still DNE or ±∞ per OpenStax; Spec dress (shift / scale / cancel).
- **Must not:** Removable cancel that exists; ordinary rational plug-in.

## What old / live path actually produced (real latex, D=0/8/16/22)

Live LimitSpec after flesh fix (2026-08-20).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\lim_{x \to 0} \frac{1}{x}$` | `$\text{DNE}$` | form=`essential_1_over_x` |
| 8 | 101 | `$\lim_{x \to -4} \cos\left(\frac{1}{(x+4)}\right)$` | `$\text{DNE}$` | form=`essential_cos_1_over_x`; wrap=shift |
| 16 | 101 | `$\lim_{x \to -4} \cos\left(\frac{1}{(x+4)}\right)$` | `$\text{DNE}$` | same catalog form + wraps |
| 22 | 101 | `$\lim_{x \to -4} \cos\left(\frac{1}{(x+4)}\right)$` | `$\text{DNE}$` | same |

Opt-out flag used: _none found (LimitSpec default)_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §2.2 The Limit of a Function | https://openstax.org/books/calculus-volume-1/pages/2-2-the-limit-of-a-function | infinite / oscillating behavior near asymptotes |
| OpenStax Calculus Volume 1 §2.4 Continuity | https://openstax.org/books/calculus-volume-1/pages/2-4-continuity | essential discontinuity classification |

Local HTML / mining: `scripts/output/example_mining/calculus-volume-1/stage1/2-4-continuity.md; limits.json essential_*`

## Variety notes / flags

Shipped: catalog forms fleshed (1/x, 1/x², rational VA, sin/cos(1/x), tan asymptote). Multi-seed pool spans ≥5 form_ids. CoreExpr Spec dress at mid/high D.

## Proposed engine (reuse vs new)

**Reuse:** LimitSpec `limit_essential` + `complexity_wrap.CoreExpr`. No Diff skeleton.
