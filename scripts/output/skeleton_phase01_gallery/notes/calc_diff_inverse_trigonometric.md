# Notes — `calc_diff_inverse_trigonometric` (`Inverse trigonometric`)

- **Course:** Calculus
- **Category:** Calculus — Differentiation
- **Generator:** `derivative_inverse_trig`
- **Suggested family:** other (calc limits / Diff)

---

## Limitations

- **Status:** shipped — Diff expr_skeleton
- **Generator:** `derivative_inverse_trig`
- **Remaining limits:** Live on Diff `expr_skeleton` + derivatives.json forms. Gaps: allow_* checkboxes gate class unlocks; some leaves still stamp soft patterns; OpenStax mixed-rule drill richer than general pack at mid-D.

## What the question should look like (D=0 vs high D)

- **Skill:** Differentiate arcsin/arctan/… of an inner.
- **D=0:** arctan(affine).
- **High D (≈16–22):** arctan(poly); nested invtrig; first derivative preferred.
- **Must not:** Plain trig without inv; second-deriv-only unlock.

## What old / live path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path (Diff leaves → `expr_skeleton` when form maps; limits → LimitSpec packs). No `use_sample_*` / Mad-Lib opt-out found for these generators.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\text{Find }\frac{d}{dx}\left(\arctan\left(3x + 3\right)\right)$` | `$\frac{1}{1+(3x + 3)^{2}}\left(3\right)$` | form=`invtrig_arctan`; skel=`Diff(Apply(arctan,u))`; pack=`expr_skeleton` |
| 8 | 101 | `$\text{Find }\frac{d}{dx}\left(\arctan\left(-x^{3} + 3x^{2} + 4\right)\right)$` | `$\frac{1}{1+(-x^{3} + 3x^{2} + 4)^{2}}\left(3x^{2}\left(-1\right) + 2x^{1}\left(3\right)\right)$` | form=`invtrig_arctan`; skel=`Diff(Apply(arctan,u))`; pack=`expr_skeleton` |
| 16 | 101 | `$\text{Find }\frac{d}{dx}\left(\arctan\left(\arctan\left(x^{4} + 7x^{3} + 2x^{2} + 3x - 5\right)\right)\right)$` | `$\frac{1}{1+(\arctan\left(x^{4} + 7x^{3} + 2x^{2} + 3x - 5\right))^{2}}\frac{1}{1+(x^{4} + 7x^{3} + 2x^{2} + 3x - 5)^{2}}\left(4x^{3} + 3x^{2}\left(7\right) + 2x^{1}\left(2\right) + 3\right)$` | form=`invtrig_chained`; skel=`Diff(Apply(invtrig,u)) chain`; pack=`expr_skeleton` |
| 22 | 101 | `$\frac{d^{2}}{dx^{2}}\left[\arctan\left(4x + 3\right)\right]$` | `$-2\left(4x + 3\right)\left(1 + \left(4x + 3\right)^{2}\right)^{-2}\left(4\right)\left(4\right)$` | form=`invtrig_chained`; skel=`Diff(Apply(invtrig,u)) chain`; pack=`expr_skeleton` |

Opt-out flag used: _none — expr_skeleton default_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §3.7 Derivatives of Inverse Functions | https://openstax.org/books/calculus-volume-1/pages/3-7-derivatives-of-inverse-functions | arcsin/arctan formulas + chain |

Local HTML / mining: `diff_skeleton_gallery/inverse_trig/; 3-7-….md`

## Variety notes / flags

Good D=0→16. Fixed former issue: D=22 second derivative — keep on higher-order or deepen nest.

## Proposed engine (reuse vs new) — proposal only

**Reuse:** `expr_skeleton` `Diff(Apply(arctan,u))` / invtrig chained. Gallery: `diff_skeleton_gallery/inverse_trig/`.

- **Shipped:** first-deriv order lock + form/flesh gates; phase-01 gallery wired.

Coverage: Diff algebraic families also cataloged in `scripts/output/diff_skeleton_gallery/` (power, product, quotient, chain, trig, invtrig, ln/exp, general, higher_order).
