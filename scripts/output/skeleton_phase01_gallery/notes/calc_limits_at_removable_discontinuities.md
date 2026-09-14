# Notes — `calc_limits_at_removable_discontinuities` (`At removable discontinuities`)

- **Course:** Calculus
- **Category:** Calculus — Limits
- **Generator:** `limit_removable`
- **Suggested family:** other (calc limits / Diff)

---

## Limitations

- **Status:** shipped — live generator
- **Generator:** `limit_removable`
- **Remaining limits:** LimitSpec packs ship. Remaining gaps: form_id metadata sometimes mismatches latex (e.g. `direct_sqrt` stamp on rational plug-in); one-sided / piecewise story variety thinner than OpenStax §2.2–2.4 exercise banks; no dedicated limit-skeleton patterns beyond packs.

## What the question should look like (D=0 vs high D)

- **Skill:** Evaluate 0/0 limits by canceling a common factor (or rationalizing) at a hole.
- **D=0:** Difference of squares cancel: (x²−a²)/(x−a).
- **High D (≈16–22):** Shared quadratic factor; rationalize √x−√a over x−a.
- **Must not:** Direct plug-in with nonzero den; L'Hôpital as first method on this leaf.

## What old / live path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path (Diff leaves → `expr_skeleton` when form maps; limits → LimitSpec packs). No `use_sample_*` / Mad-Lib opt-out found for these generators.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\lim_{x \to 2} \frac{x^{2}-4}{x-2}$` | `$4$` | form=`removable_diff_sq`; skel=`—`; pack=`limit_removable` |
| 8 | 101 | `$\lim_{x \to 2} \frac{x^{2}-5x+6}{x-2}$` | `$-1$` | form=`removable_quad_shared`; skel=`—`; pack=`limit_removable` |
| 16 | 101 | `$\lim_{x \to 2} \frac{\sqrt{x}-\sqrt{2}}{x-2}$` | `$\frac{1}{2\sqrt{2}}$` | form=`removable_rationalize`; skel=`—`; pack=`limit_removable` |
| 22 | 101 | `$\lim_{x \to 2} \frac{\sqrt{x}-\sqrt{2}}{x-2}$` | `$\frac{1}{2\sqrt{2}}$` | form=`removable_rationalize`; skel=`—`; pack=`limit_removable` |

Opt-out flag used: _none found (LimitSpec default)_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §2.3 The Limit Laws | https://openstax.org/books/calculus-volume-1/pages/2-3-the-limit-laws | algebraic cancel / factor for 0/0 |
| OpenStax Calculus Volume 1 §2.4 Continuity | https://openstax.org/books/calculus-volume-1/pages/2-4-continuity | removable discontinuity / redefine at hole |

Local HTML / mining: `scripts/output/example_mining/calculus-volume-1/stage1/2-3-the-limit-laws.md; limits.json removable_*`

## Variety notes / flags

Good D ladder (diff sq → quad shared → rationalize). D=16 and 22 same seed shape — acceptable. LimitSpec, not Diff.

## Proposed engine (reuse vs new) — proposal only

**Reuse:** LimitSpec `limit_removable`. Keep factor_cancel / rationalize strategies.

- **Not this pass:** notes only — no generator changes.

Coverage: Diff algebraic families also cataloged in `scripts/output/diff_skeleton_gallery/` (power, product, quotient, chain, trig, invtrig, ln/exp, general, higher_order).
