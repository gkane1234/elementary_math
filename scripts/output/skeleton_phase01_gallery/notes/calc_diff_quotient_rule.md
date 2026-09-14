# Notes — `calc_diff_quotient_rule` (`Quotient Rule`)

- **Course:** Calculus
- **Category:** Calculus — Differentiation
- **Generator:** `derivative_quotient_rule`
- **Suggested family:** other (calc limits / Diff)

---

## Limitations

- **Status:** shipped — Diff expr_skeleton
- **Generator:** `derivative_quotient_rule`
- **Remaining limits:** Live on Diff `expr_skeleton` + derivatives.json forms. Gaps: allow_* checkboxes gate class unlocks; some leaves still stamp soft patterns; OpenStax mixed-rule drill richer than general pack at mid-D.

## What the question should look like (D=0 vs high D)

- **Skill:** Differentiate a quotient f/g with the quotient rule.
- **D=0:** Simple poly/poly, e.g. x/(2x).
- **High D (≈16–22):** Higher-degree num/den; chain on powered pieces; keep algebraic unless checkboxes allow specials.
- **Must not:** Product-only; trig/log quotients unless allow_* enabled.

## What old / live path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path (Diff leaves → `expr_skeleton` when form maps; limits → LimitSpec packs). No `use_sample_*` / Mad-Lib opt-out found for these generators.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\text{Find }\frac{d}{dx}\left(\frac{x}{2x}\right)$` | `$\frac{1}{2x} - \left(2x\right)^{-2}\left(2\right)x$` | form=`quotient_poly`; skel=`Diff(Quot(F,G)) poly/poly`; pack=`expr_skeleton` |
| 8 | 101 | `$\frac{d}{dx}\left[\frac{5x^{3} + 5x^{2} + x + 3}{-2x + 2}\right]$` | `$\frac{3x^{2}\left(5\right) + 2x^{1}\left(5\right) + 1}{-2x + 2} - \left(-2x + 2\right)^{-2}\left(-2\right)\left(5x^{3} + 5x^{2} + x + 3\right)$` | form=`quotient_exp_poly`; skel=`Diff(Quot(F,G)) exp/poly`; pack=`expr_skeleton` |
| 16 | 101 | `$\frac{d}{dx}\left[\frac{-2\left(8x^{3} + 5x^{2} - 3x - 3\right)^{3}}{7x^{3} + 6x - 4}\right]$` | `$\frac{3\left(8x^{3} + 5x^{2} - 3x - 3\right)^{2}\left(3x^{2}\left(8\right) + 2x^{1}\left(5\right) - 3\right)\left(-2\right)}{7x^{3} + 6x - 4} - \left(7x^{3} + 6x - 4\right)^{-2}\left(3x^{2}\left(7\right) + 6\right)\left(-2\right)\left(8x^{3} + 5x^{2} - 3x - 3\right)^{3}$` | form=`quotient_log_poly`; skel=`Diff(Quot(F,G)) log/…`; pack=`expr_skeleton` |
| 22 | 101 | `$\frac{d}{dx}\left[\frac{-10x^{4} + 2x^{3} + 2x^{2} + 6x - 6}{6\left(-5x^{4} - 4x^{3} + x + 4\right)^{4}}\right]$` | `$\frac{4x^{3}\left(-10\right) + 3x^{2}\left(2\right) + 2x^{1}\left(2\right) + 6}{6\left(-5x^{4} - 4x^{3} + x + 4\right)^{4}} - \left(6\left(-5x^{4} - 4x^{3} + x + 4\right)^{4}\right)^{-2}\left(4\right)\left(-5x^{4} - 4x^{3} + x + 4\right)^{3}\left(4x^{3}\left(-5\right) + 3x^{2}\left(-4\right) + 1\right)\left(6\right)\left(-10x^{4} + 2x^{3} + 2x^{2} + 6x - 6\right)$` | form=`quotient_log_poly`; skel=`Diff(Quot(F,G)) log/…`; pack=`expr_skeleton` |

Opt-out flag used: _none — expr_skeleton default_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §3.3 Differentiation Rules | https://openstax.org/books/calculus-volume-1/pages/3-3-differentiation-rules | quotient rule (f/g)' |

Local HTML / mining: `diff_skeleton_gallery/quotient_rule/; derivatives.json quotient_*`

## Variety notes / flags

Fixed — was: D≥8 form_id/`skeleton_pattern` say exp/log quotient while latex stays algebraic poly quotients. Student-facing shapes escalate ok; stamp form_id to match flesh.

## Proposed engine (reuse vs new) — proposal only

**Reuse:** `expr_skeleton` `Diff(Quot(F,G))`. Gallery: `diff_skeleton_gallery/quotient_rule/`.

- **Shipped:** first-deriv order lock + form/flesh gates; phase-01 gallery wired.

Coverage: Diff algebraic families also cataloged in `scripts/output/diff_skeleton_gallery/` (power, product, quotient, chain, trig, invtrig, ln/exp, general, higher_order).
