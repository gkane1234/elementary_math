# Notes — `calc_diff_higher_order_derivatives` (`Higher order derivatives`)

- **Course:** Calculus
- **Category:** Calculus — Differentiation
- **Generator:** `derivative_higher_order`
- **Suggested family:** other (calc limits / Diff)

---

## Limitations

- **Status:** shipped — Diff expr_skeleton
- **Generator:** `derivative_higher_order`
- **Remaining limits:** Live on Diff `expr_skeleton` + derivatives.json forms. Gaps: allow_* checkboxes gate class unlocks; some leaves still stamp soft patterns; OpenStax mixed-rule drill richer than general pack at mid-D.

## What the question should look like (D=0 vs high D)

- **Skill:** Compute second (or higher) derivatives of power/chain-style expressions.
- **D=0:** d²/dx² of a simple monomial/power, e.g. x².
- **High D (≈16–22):** d² of (poly)^n or richer inners; optional order 3 forms.
- **Must not:** First-derivative-only prompts on this leaf; steal all high-D from other leaves via order=2.

## What old / live path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path (Diff leaves → `expr_skeleton` when form maps; limits → LimitSpec packs). No `use_sample_*` / Mad-Lib opt-out found for these generators.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\frac{d^{2}}{dx^{2}}\left[x^{2}\right]$` | `$x^{0}\left(2\right)$` | form=`power_poly`; skel=`Diff(Pow(H,n))`; pack=`expr_skeleton` |
| 8 | 101 | `$\frac{d^{2}}{dx^{2}}\left[\left(2x - 3\right)^{3}\right]$` | `$2\left(2x - 3\right)^{1}\left(2\right)\left(3\right)\left(2\right)$` | form=`higher_order_2`; skel=`Diff(Pow(H,n)) order2`; pack=`expr_skeleton` |
| 16 | 101 | `$\frac{d^{2}}{dx^{2}}\left[\left(4x + 3\right)^{2}\right]$` | `$\left(4x + 3\right)^{0}\left(4\right)\left(2\right)\left(4\right)$` | form=`higher_order_2`; skel=`Diff(Pow(H,n)) order2`; pack=`expr_skeleton` |
| 22 | 101 | `$\frac{d^{2}}{dx^{2}}\left[\left(9x^{3} + 9x^{2} + 2x + 6\right)^{4}\right]$` | `$3\left(9x^{3} + 9x^{2} + 2x + 6\right)^{2}\left(3x^{2}\left(9\right) + 2x^{1}\left(9\right) + 2\right)\left(4\right)\left(3x^{2}\left(9\right) + 2x^{1}\left(9\right) + 2\right) + \left(2x^{1}\left(3\right)\left(9\right) + x^{0}\left(2\right)\left(9\right)\right)\left(4\right)\left(9x^{3} + 9x^{2} + 2x + 6\right)^{3}$` | form=`higher_order_2`; skel=`Diff(Pow(H,n)) order2`; pack=`expr_skeleton` |

Opt-out flag used: _none — expr_skeleton default_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §3.2 The Derivative as a Function | https://openstax.org/books/calculus-volume-1/pages/3-2-the-derivative-as-a-function | higher-order derivatives notation |
| OpenStax Calculus Volume 1 §3.3 Differentiation Rules | https://openstax.org/books/calculus-volume-1/pages/3-3-differentiation-rules | repeated differentiation of powers |

Local HTML / mining: `diff_skeleton_gallery/higher_order/; forms higher_order_2 / higher_order_3`

## Variety notes / flags

Correctly order≥2 from D=0. Good power/chain ladder.

## Proposed engine (reuse vs new) — proposal only

**Reuse:** `expr_skeleton` with `derivative_order≥2` + `Diff(Pow(H,n))` order2 patterns. Gallery: `diff_skeleton_gallery/higher_order/`.

- **Not this pass:** notes only — no generator changes.

Coverage: Diff algebraic families also cataloged in `scripts/output/diff_skeleton_gallery/` (power, product, quotient, chain, trig, invtrig, ln/exp, general, higher_order).
