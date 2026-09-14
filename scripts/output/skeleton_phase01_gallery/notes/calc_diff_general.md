# Notes — `calc_diff_general` (`General derivatives`)

- **Course:** Calculus
- **Category:** Calculus — Differentiation
- **Generator:** `derivative_general`
- **Suggested family:** other (calc limits / Diff)

---

## Limitations

- **Status:** shipped — Diff expr_skeleton
- **Generator:** `derivative_general`
- **Remaining limits:** Live on Diff `expr_skeleton` + derivatives.json forms. Gaps: allow_* checkboxes gate class unlocks; some leaves still stamp soft patterns; OpenStax mixed-rule drill richer than general pack at mid-D.

## What the question should look like (D=0 vs high D)

- **Skill:** Differentiate mixed expressions drawing on several rules (trig/exp/log/product/quotient/chain).
- **D=0:** Still simple single-class (e.g. sin(affine)) — mixed unlocks with D.
- **High D (≈16–22):** Mixed quotient/product/chain across function classes; first derivative preferred.
- **Must not:** Force one rule leaf’s exclusivity; second-deriv bleed.

## What old / live path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path (Diff leaves → `expr_skeleton` when form maps; limits → LimitSpec packs). No `use_sample_*` / Mad-Lib opt-out found for these generators.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\text{Find }\frac{d}{dx}\left(\sin\left(x - 1\right)\right)$` | `$\cos\left(x - 1\right)$` | form=`trig_basic`; skel=`Diff(Apply(fn,u))`; pack=`expr_skeleton` |
| 8 | 101 | `$\text{Find }\frac{d}{dx}\left(\frac{\ln\left(5x^{3} + 5x^{2} + x + 3\right)}{\sin\left(4x - 2\right)}\right)$` | `$\frac{3x^{2}\left(5\right) + 2x^{1}\left(5\right) + 1}{\left(5x^{3} + 5x^{2} + x + 3\right)\sin\left(4x - 2\right)} - \sin^{-2}\left(4x - 2\right)\cos\left(4x - 2\right)\left(4\right)\ln\left(5x^{3} + 5x^{2} + x + 3\right)$` | form=`quotient_log_poly`; skel=`Diff(Quot(F,G)) log/…`; pack=`expr_skeleton` |
| 16 | 101 | `$\frac{d}{dx}\left[\left(4x^{3} + 8x^{2} + 5x - 3\right)^{5}\right]$` | `$5\left(4x^{3} + 8x^{2} + 5x - 3\right)^{4}\left(3x^{2}\left(4\right) + 2x^{1}\left(8\right) + 5\right)$` | form=`chain_power_linear`; skel=`Diff(Pow(H,n)) chain-linear`; pack=`expr_skeleton` |
| 22 | 101 | `$\frac{d^{2}}{dx^{2}}\left[\left(4x\right)^{5}\right]$` | `$4\left(4x\right)^{3}\left(4\right)\left(5\right)\left(4\right)$` | form=`chain_power_linear`; skel=`Diff(Pow(H,n)) chain-linear`; pack=`expr_skeleton` |

Opt-out flag used: _none — expr_skeleton default_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §3.3–3.9 (mixed practice) | https://openstax.org/books/calculus-volume-1/pages/3-3-differentiation-rules | combine power/product/quotient/chain/trig/exp/ln |

Local HTML / mining: `diff_skeleton_gallery/general/; form general_mixed + shared forms`

## Variety notes / flags

Rotates forms (trig → quotient log/trig → chain power). Fixed former issue: D=22 second derivative.

## Proposed engine (reuse vs new) — proposal only

**Reuse:** `expr_skeleton` with broad allows + `general_mixed` / shared Diff patterns. Gallery: `diff_skeleton_gallery/general/`.

- **Shipped:** first-deriv order lock + form/flesh gates; phase-01 gallery wired.

Coverage: Diff algebraic families also cataloged in `scripts/output/diff_skeleton_gallery/` (power, product, quotient, chain, trig, invtrig, ln/exp, general, higher_order).
