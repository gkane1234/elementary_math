# Notes — `calc_diff_power_rule` (`Power Rule`)

- **Course:** Calculus
- **Category:** Calculus — Differentiation
- **Generator:** `derivative_power_rule`
- **Suggested family:** other (calc limits / Diff)

---

## Limitations

- **Status:** shipped — Diff expr_skeleton
- **Generator:** `derivative_power_rule`
- **Remaining limits:** Live on Diff `expr_skeleton` + derivatives.json forms. Gaps: allow_* checkboxes gate class unlocks; some leaves still stamp soft patterns; OpenStax mixed-rule drill richer than general pack at mid-D.

## What the question should look like (D=0 vs high D)

- **Skill:** Differentiate polynomial / power / root expressions with the power rule (and sum).
- **D=0:** Single monomial c x^n, e.g. d/dx(2x²).
- **High D (≈16–22):** Fractional/negative powers, multi-term polys; stay first derivative on this leaf.
- **Must not:** Product/quotient/trig as primary skill; second derivative belongs on higher-order leaf.

## What old / live path actually produced (real latex, D=0/8/16/22)

Live `_generate_for_type` at default path (Diff leaves → `expr_skeleton` when form maps; limits → LimitSpec packs). No `use_sample_*` / Mad-Lib opt-out found for these generators.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\text{Find }\frac{d}{dx}\left(2x^{2}\right)$` | `$2x^{1}\left(2\right)$` | form=`power_poly`; skel=`Diff(Pow(H,n))`; pack=`expr_skeleton` |
| 8 | 101 | `$\text{Find }\frac{d}{dx}\left(5x^{3} + 5x^{2} + x + 3\right)$` | `$3x^{2}\left(5\right) + 2x^{1}\left(5\right) + 1$` | form=`power_root`; skel=`Diff(Pow(H,n)) roots`; pack=`expr_skeleton` |
| 16 | 101 | `$\frac{d}{dx}\left[x^{\frac{5}{2}}\right]$` | `$\frac{5}{2}x^{\frac{3}{2}}$` | form=`power_root`; skel=`Diff(Pow(H,n)) roots`; pack=`expr_skeleton` |
| 22 | 101 | `$\frac{d^{2}}{dx^{2}}\left[9x^{3} + 9x^{2} + 2x + 6\right]$` | `$2x^{1}\left(3\right)\left(9\right) + x^{0}\left(2\right)\left(9\right)$` | form=`power_root`; skel=`Diff(Pow(H,n)) roots`; pack=`expr_skeleton` |

Opt-out flag used: _none — Diff/`expr_skeleton` is default when catalog form has FORM_PATTERNS entry_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §3.3 Differentiation Rules | https://openstax.org/books/calculus-volume-1/pages/3-3-differentiation-rules | power / sum / constant multiple |

Local HTML / mining: `scripts/output/example_mining/calculus-volume-1/stage1/3-3-differentiation-rules.md; diff_skeleton_gallery/power_rule/`

## Variety notes / flags

Fixed — was: D=22 emitted d²/dx² of a poly while form_id stayed `power_root`. Gold: first-derivative power/roots only; higher order → `calc_diff_higher_order_derivatives`.

## Proposed engine (reuse vs new) — proposal only

**Reuse:** `expr_skeleton` Diff patterns `Diff(Pow(H,n))` / roots / neg via OpenStax forms `power_*`. Covered in `scripts/output/diff_skeleton_gallery/`. No separate opt-out flag — skeleton is default when form maps.

- **Shipped:** first-deriv order lock + form/flesh gates; phase-01 gallery wired.

Coverage: Diff algebraic families also cataloged in `scripts/output/diff_skeleton_gallery/` (power, product, quotient, chain, trig, invtrig, ln/exp, general, higher_order).
