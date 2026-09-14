# Notes — `calc_continuity_determining_and_classifying` (`Determining and classifying`)

- **Course:** Calculus
- **Category:** Calculus — Continuity
- **Generator:** `limit_continuity`
- **Suggested family:** other (calc limits / Diff)

---

## Limitations

- **Status:** shipped — live generator
- **Generator:** `limit_continuity`
- **Remaining limits:** LimitSpec packs ship. Remaining gaps: form_id metadata sometimes mismatches latex (e.g. `direct_sqrt` stamp on rational plug-in); one-sided / piecewise story variety thinner than OpenStax §2.2–2.4 exercise banks; no dedicated limit-skeleton patterns beyond packs.

## What the question should look like (D=0 vs high D)

- **Skill:** Classify continuity at a point (continuous / removable / jump / essential).
- **D=0:** Removable hole or continuous poly/linear.
- **High D (≈16–22):** Mix jump piecewise, essential VA, continuous polys, removable — several OpenStax cases.
- **Must not:** Only evaluate a numeric limit without classifying.

## What old / live path actually produced (real latex, D=0/8/16/22)

Live LimitSpec after case-sampler expand (2026-08-20).

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\text{Classify the continuity of }f(x)=-5x\text{ at }x=4.$` | `$\text{continuous}$` | continuous |
| 8 | 101 | `$\text{Classify the continuity of }f(x)=-5x + 5\text{ at }x=4.$` | `$\text{continuous}$` | continuous |
| 16 | 101 | `$\text{Classify the continuity of }f(x)=\frac{1}{x-4}\text{ at }x=4.$` | `$\text{essential discontinuity}$` | essential |
| 22 | 101 | `$\text{Classify the continuity of }f(x)=\frac{1}{x-4}\text{ at }x=4.$` | `$\text{essential discontinuity}$` | essential |

Opt-out flag used: _none found (LimitSpec default)_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §2.4 Continuity | https://openstax.org/books/calculus-volume-1/pages/2-4-continuity | types of discontinuity; continuity checklist |

Local HTML / mining: `scripts/output/example_mining/calculus-volume-1/stage1/2-4-continuity.md; limits.json continuity_classify`

## Variety notes / flags

Shipped: D-gated case sampler — continuous / removable / jump / essential. Multi-seed pool hits all four.

## Proposed engine (reuse vs new)

**Reuse:** LimitSpec `limit_continuity`. Related to limit leaves, not Diff.
