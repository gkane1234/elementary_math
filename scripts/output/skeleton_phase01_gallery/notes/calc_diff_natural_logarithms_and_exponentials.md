# Notes — `calc_diff_natural_logarithms_and_exponentials` (`Natural logarithms and exponentials`)

- **Course:** Calculus
- **Category:** Calculus — Differentiation
- **Generator:** `derivative_ln_exp`
- **Suggested family:** other (calc limits / Diff)

---

## Limitations

- **Status:** shipped — Diff expr_skeleton
- **Generator:** `derivative_ln_exp`
- **Remaining limits:** Live on Diff `expr_skeleton` + derivatives.json forms. Gaps: allow_* checkboxes gate class unlocks; some leaves still stamp soft patterns; OpenStax mixed-rule drill richer than general pack at mid-D.

## What the question should look like (D=0 vs high D)

- **Skill:** Differentiate e^{u} and ln(u) (and products/quotients of them when allowed).
- **D=0:** e^{affine}.
- **High D (≈16–22):** ln of poly / nested ln; ln·exp product; optional quotient of ln/poly.
- **Must not:** Other-base logs (separate leaf); pure algebraic power without exp/ln.

## What old / live path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path (Diff leaves → `expr_skeleton` when form maps; limits → LimitSpec packs). No `use_sample_*` / Mad-Lib opt-out found for these generators.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\text{Find }\frac{d}{dx}\left(e^{3x + 3}\right)$` | `$e^{3x + 3}\left(3\right)$` | form=`exp_basic`; skel=`Diff(Apply(exp,u))`; pack=`expr_skeleton` |
| 8 | 101 | `$\frac{d}{dx}\left[\frac{\ln\left(5x^{3} + 5x^{2} + x + 3\right)}{-2x + 2}\right]$` | `$\frac{3x^{2}\left(5\right) + 2x^{1}\left(5\right) + 1}{\left(5x^{3} + 5x^{2} + x + 3\right)\left(-2x + 2\right)} - \left(-2x + 2\right)^{-2}\left(-2\right)\ln\left(5x^{3} + 5x^{2} + x + 3\right)$` | form=`quotient_log_poly`; skel=`Diff(Quot(F,G)) log/…`; pack=`expr_skeleton` |
| 16 | 101 | `$\text{Find }\frac{d}{dx}\left(\ln\left(\ln\left(x^{4} + 7x^{3} + 2x^{2} + 3x - 5\right)\right)\right)$` | `$\frac{\frac{4x^{3} + 3x^{2}\left(7\right) + 2x^{1}\left(2\right) + 3}{x^{4} + 7x^{3} + 2x^{2} + 3x - 5}}{\ln\left(x^{4} + 7x^{3} + 2x^{2} + 3x - 5\right)}$` | form=`ln_basic`; skel=`Diff(Apply(ln,u))`; pack=`expr_skeleton` |
| 22 | 101 | `$\frac{d^{2}}{dx^{2}}\left[\ln\left(4x + 3\right)\right]$` | `$-\left(4x + 3\right)^{-2}\left(4\right)\left(4\right)$` | form=`ln_basic`; skel=`Diff(Apply(ln,u))`; pack=`expr_skeleton` |

Opt-out flag used: _none — expr_skeleton default_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §3.9 Derivatives of Exponential and Logarithmic Functions | https://openstax.org/books/calculus-volume-1/pages/3-9-derivatives-of-exponential-and-logarithmic-functions | e^u, ln u, products |

Local HTML / mining: `diff_skeleton_gallery/ln_exp/; 3-9-….md`

## Variety notes / flags

D=0 exp_basic good; mid mixes quotient_log_poly. Fixed former issue: D=22 second deriv of ln(affine).

## Proposed engine (reuse vs new) — proposal only

**Reuse:** `expr_skeleton` `Diff(Apply(exp,u))` / `Diff(Apply(ln,u))` / `Diff(Prod(F,G)(u))` ln×exp. Gallery: `diff_skeleton_gallery/ln_exp/`.

- **Shipped:** first-deriv order lock + form/flesh gates; phase-01 gallery wired.

Coverage: Diff algebraic families also cataloged in `scripts/output/diff_skeleton_gallery/` (power, product, quotient, chain, trig, invtrig, ln/exp, general, higher_order).
