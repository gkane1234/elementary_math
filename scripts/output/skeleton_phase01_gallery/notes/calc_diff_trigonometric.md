# Notes — `calc_diff_trigonometric` (`Trigonometric`)

- **Course:** Calculus
- **Category:** Calculus — Differentiation
- **Generator:** `derivative_trigonometric`
- **Suggested family:** other (calc limits / Diff)

---

## Limitations

- **Status:** shipped — Diff expr_skeleton
- **Generator:** `derivative_trigonometric`
- **Remaining limits:** Live on Diff `expr_skeleton` + derivatives.json forms. Gaps: allow_* checkboxes gate class unlocks; some leaves still stamp soft patterns; OpenStax mixed-rule drill richer than general pack at mid-D.

## What the question should look like (D=0 vs high D)

- **Skill:** Differentiate trig functions (with chain / product-of-trig as D rises).
- **D=0:** Basic trig of affine, e.g. tan(3x+3).
- **High D (≈16–22):** Powered trig of poly; product of trig compositions; first derivative preferred.
- **Must not:** Invtrig-only; second derivative as the main D=22 unlock.

## What old / live path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path (Diff leaves → `expr_skeleton` when form maps; limits → LimitSpec packs). No `use_sample_*` / Mad-Lib opt-out found for these generators.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\text{Find }\frac{d}{dx}\left(\tan\left(3x + 3\right)\right)$` | `$\sec^{2}(3x + 3)\left(3\right)$` | form=`trig_basic`; skel=`Diff(Apply(fn,u))`; pack=`expr_skeleton` |
| 8 | 101 | `$\text{Find }\frac{d}{dx}\left(\cos^{3}\left(-x^{3} + 3x^{2} + 4\right)\right)$` | `$-3\cos^{2}\left(-x^{3} + 3x^{2} + 4\right)\sin\left(-x^{3} + 3x^{2} + 4\right)\left(3x^{2}\left(-1\right) + 2x^{1}\left(3\right)\right)$` | form=`trig_basic`; skel=`Diff(Apply(fn,u))`; pack=`expr_skeleton` |
| 16 | 101 | `$\text{Find }\frac{d}{dx}\left(\cos\left(\cos\left(x^{4} + 7x^{3} + 2x^{2} + 3x - 5\right)\right)\sin\left(\cos\left(x^{4} + 7x^{3} + 2x^{2} + 3x - 5\right)\right)\right)$` | `$\sin\left(\cos\left(x^{4} + 7x^{3} + 2x^{2} + 3x - 5\right)\right)\sin\left(x^{4} + 7x^{3} + 2x^{2} + 3x - 5\right)\left(4x^{3} + 3x^{2}\left(7\right) + 2x^{1}\left(2\right) + 3\right)\sin\left(\cos\left(x^{4} + 7x^{3} + 2x^{2} + 3x - 5\right)\right) - \cos\left(\cos\left(x^{4} + 7x^{3} + 2x^{2} + 3x - 5\right)\right)\sin\left(x^{4} + 7x^{3} + 2x^{2} + 3x - 5\right)\left(4x^{3} + 3x^{2}\left(7\right) + 2x^{1}\left(2\right) + 3\right)\cos\left(\cos\left(x^{4} + 7x^{3} + 2x^{2} + 3x - 5\right)\right)$` | form=`trig_product_chain`; skel=`Diff(Prod(F,G)(u)) trig×trig`; pack=`expr_skeleton` |
| 22 | 101 | `$\frac{d^{2}}{dx^{2}}\left[\cos(x)\cos(x)\right]$` | `$-\cos(x)\cos(x) + \sin(x)\sin(x) - \cos(x)\cos(x) + \sin(x)\sin(x)$` | form=`trig_product_chain`; skel=`Diff(Prod(F,G)(u)) trig×trig`; pack=`expr_skeleton` |

Opt-out flag used: _none — expr_skeleton default_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §3.5 Derivatives of Trigonometric Functions | https://openstax.org/books/calculus-volume-1/pages/3-5-derivatives-of-trigonometric-functions | sin/cos/tan/… + chain |
| OpenStax Calculus Volume 1 §3.6 The Chain Rule | https://openstax.org/books/calculus-volume-1/pages/3-6-the-chain-rule | trig compositions |

Local HTML / mining: `diff_skeleton_gallery/trigonometric/; 3-5-….md`

## Variety notes / flags

Good mid/high trig variety. Fixed former issue: D=22 second derivative of cos·cos — prefer nest richness on first deriv.

## Proposed engine (reuse vs new) — proposal only

**Reuse:** `expr_skeleton` `Diff(Apply(fn,u))` + `Diff(Prod(F,G)(u))` trig×trig. Gallery: `diff_skeleton_gallery/trigonometric/`.

- **Shipped:** first-deriv order lock + form/flesh gates; phase-01 gallery wired.

Coverage: Diff algebraic families also cataloged in `scripts/output/diff_skeleton_gallery/` (power, product, quotient, chain, trig, invtrig, ln/exp, general, higher_order).
