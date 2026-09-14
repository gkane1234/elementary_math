# Notes — `calc_diff_logarithmic` (`Logarithmic`)

- **Course:** Calculus
- **Category:** Calculus — Differentiation
- **Generator:** `derivative_logarithmic`
- **Suggested family:** other (calc limits / Diff)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Use logarithmic differentiation to find \(y'\) (not the plain \(\frac{d}{dx}\ln u\) rule).
- **D=0:** Power \(x^n\) only (old easy — “use log diff” on a monomial).
- **Mid D (≈8):** Product of powers \(x^n(x+1)^m\), quotient \(x^n/(x+1)\), root \(\sqrt{x(x+1)}\). Not \(x^n\) leftovers.
- **High D (≈16–22):** Variable-exponent families — \(x^x\), \((x+1)^x\), \((\sin x)^x\). OpenStax §3.9 checkpoint \(x^x\).
- **Must not:** Plain \(\ln(u)\) / \(e^u\) rule leaf; implicit \(F(x,y)=c\).

## What old / live path actually produced (real latex, D=0/8/16/22)

**Old (pre-catalog routing):** D=0 power \(x^n\); D=8 product/root; D=16/22 mix of \(x^x\) with product/root leftovers (no `form_id`).

**Live now** (`_generate_for_type`):

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 207 | `$\text{Use logarithmic differentiation to find }\frac{d}{dx}\left[x^{4}\right].$` | `$4x^{3}$` | form=`logdiff_power` |
| 0 | 0 | `$\text{Use logarithmic differentiation to find }\frac{d}{dx}\left[x^{3}\right].$` | `$3x^{2}$` | power only |
| 8 | 101 | `$\text{Use logarithmic differentiation: }y=\frac{x^{2}}{x+1}.\ \text{Find }y'.$` | `$\frac{x^{2}}{x+1}\left(\frac{2}{x}-\frac{1}{x+1}\right)$` | form=`logdiff_quotient_powers` |
| 8 | 3 | `$\text{Use logarithmic differentiation: }y=x^{4}(x+1)^{2}.\ \text{Find }y'.$` | `$x^{4}(x+1)^{2}\left(\frac{4}{x}+\frac{2}{x+1}\right)$` | form=`logdiff_product_powers` |
| 8 | 0 | `$\text{Use logarithmic differentiation: }y=\sqrt{x(x+1)}.\ \text{Find }y'.$` | `$\sqrt{x(x+1)}\cdot\frac{1}{2}\left(\frac{1}{x}+\frac{1}{x+1}\right)$` | form=`logdiff_root` |
| 16 | 3 | `$\text{Use logarithmic differentiation: }y=x^{x}.\ \text{Find }y'.$` | `$x^{x}\left(\ln(x)+1\right)$` | form=`logdiff_x_x` |
| 16 | 101 | `$\text{Use logarithmic differentiation: }y=(x+1)^{x}.\ \text{Find }y'.$` | `$(x+1)^{x}\left(\ln(x+1)+\frac{x}{x+1}\right)$` | form=`logdiff_a_x` |
| 16 | 0 | `$\text{Use logarithmic differentiation: }y=\left(\sin(x)\right)^{x}.\ \text{Find }y'.$` | `$\left(\sin(x)\right)^{x}\left(\ln(\sin(x))+x\cot(x)\right)$` | form=`logdiff_trig_x` |
| 22 | 3 | `$\text{Use logarithmic differentiation: }y=x^{x}.\ \text{Find }y'.$` | `$x^{x}\left(\ln(x)+1\right)$` | form=`logdiff_x_x` |

Opt-out flag used: _none — structured catalog on the existing Mad-Lib builders_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §3.9 Derivatives of Exponential and Logarithmic Functions | https://openstax.org/books/calculus-volume-1/pages/3-9-derivatives-of-exponential-and-logarithmic-functions | Log-diff: \(x^r\); checkpoint \(x^x\); \((\tan x)^\pi\); product of powers; mixed quotient with root/trig/exp |

Local HTML / mining: `scripts/output/example_mining/calculus-volume-1/stage1/3-9-derivatives-of-exponential-and-logarithmic-functions.md`

Catalog forms: `logdiff_power`, `logdiff_product_powers`, `logdiff_quotient_powers`, `logdiff_root`, `logdiff_x_x`, `logdiff_a_x`, `logdiff_trig_x`.

## Variety notes

D=0 stays one easy frame (power). Mid/high D rotate several §3.9 algebraic / \(x^x\) / trig-power shapes. Not a WP. OpenStax Example 3.81 \((2x^4+1)^{\tan x}\) and Example 3.82 mixed quotient are **not** in the old pack — not invented this pass.

## Limitations

- **Status:** shipped — catalog-routed closed-form families. Remaining `LIMITATIONS`: not a general \(u(x)^{v(x)}\) AST / `expr_skeleton` sampler; templates cover listed old-pack / §3.9 checkpoint shapes only (no Example 3.81 poly-tan or 3.82 mixed exp-trig quotient).
- **Generator:** `derivative_logarithmic`

## Proposed engine (reuse vs new)

**Reuse:** existing `structured_logarithmic` builders + `derivatives.json` form_ids with `d_min`/`d_max` (same pattern as implicit / parts). No padded costs. Plain \(\ln/\exp\) stays on `calc_diff_natural_logarithms_and_exponentials`.

- **Shipped this pass:** catalog routing; D=0 power-only; high D cannot emit `logdiff_power`.
