# Notes — `calc_diff_inverse_functions`

- **Course:** Calculus
- **Category:** Calculus — Differentiation
- **Generator:** `derivative_inverse_functions`
- **Suggested family:** other (calc limits / Diff)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Inverse Function Theorem \((f^{-1})'(f(a))=1/f'(a)\) (not the \(\arcsin\) formula leaf).
- **D=0:** Power \(x^n\) only (old easy).
- **Mid D (≈8):** Table values and linear \(mx+c\). Not leftover \(x^n\).
- **High D (≈16–22):** \(\ln x\), \(x^3+x\), \(\sin x\) (OpenStax §3.7 exercise 267). \(e^x\) locked out at D=22 (`d_max=18`).
- **Must not:** Bare \(\frac{d}{dx}\arcsin\) (that is `calc_diff_inverse_trigonometric`); invented cube-root IFT prompt.

## What old / live path actually produced (real latex, D=0/8/16/22)

**Old (pre-catalog routing):** D=0 power only; D=8 linear / table / power leftovers; D=16/22 mixed power leftovers with \(e^x\), \(\ln\), \(x^3+x\). Two-seed notes looked \(e^x\)-stuck; 36-seed sample was mixed but \(x^n\) leftovers still ~1/3 of high D.

**Live now** (`_generate_for_type`):

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$f(x)=x^{2};\quad f'(3)=6.\quad\text{Find }(f^{-1})'(9).$` | `$\frac{1}{6}$` | form=`invfn_power` |
| 0 | 207 | `$f(x)=x^{4};\quad f'(3)=108.\quad\text{Find }(f^{-1})'(81).$` | `$\frac{1}{108}$` | form=`invfn_power` |
| 8 | 101 | `$f(x)=3x + 1.\quad\text{Find }(f^{-1})'(x).$` | `$\frac{1}{3}$` | form=`invfn_linear` |
| 8 | 1 | `$f(1)=4,\ f'(1)=-5.\quad\text{Find }(f^{-1})'(4).$` | `$-\frac{1}{5}$` | form=`invfn_table` |
| 16 | 0 | `$f(x)=\sin(x);\quad f(0)=0,\ f'(0)=1.\quad\text{Find }(f^{-1})'(0).$` | `$1$` | form=`invfn_trig` |
| 16 | 1 | `$f(x)=e^{x};\quad f(0)=1,\ f'(0)=1.\quad\text{Find }(f^{-1})'(1).$` | `$1$` | form=`invfn_exp` (still at D=16) |
| 16 | 3 | `$f(x)=\ln(x);\quad f(e)=1,\ f'(e)=\frac{1}{e}.\quad\text{Find }(f^{-1})'(1).$` | `$e$` | form=`invfn_ln` |
| 22 | 0 | `$f(x)=\sin(x);\quad f(0)=0,\ f'(0)=1.\quad\text{Find }(f^{-1})'(0).$` | `$1$` | form=`invfn_trig` |
| 22 | 1 | `$f(x)=\ln(x);\quad f(e)=1,\ f'(e)=\frac{1}{e}.\quad\text{Find }(f^{-1})'(1).$` | `$e$` | form=`invfn_ln` |
| 22 | 101 | `$f(x)=x^{3}+x;\quad f'(1)=4.\quad\text{Find }(f^{-1})'(2).$` | `$\frac{1}{4}$` | form=`invfn_cubic` |

Opt-out flag used: _none — structured catalog on the existing IFT Mad-Lib builders_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §3.7 Derivatives of Inverse Functions | https://openstax.org/books/calculus-volume-1/pages/3-7-derivatives-of-inverse-functions | IFT on \(x^n\); linear \(6x-1\); cubic \(x^3+2x+3\); exercise 267 \(f(x)=\sin x\) at \(x=0\) |

Local HTML / mining: `scripts/output/example_mining/calculus-volume-1/stage1/3-7-derivatives-of-inverse-functions.md`

Catalog forms: `invfn_power`, `invfn_table`, `invfn_linear`, `invfn_exp`, `invfn_ln`, `invfn_cubic`, `invfn_trig`.

## Variety notes

D=0 stays one easy frame (power). Mid D table + linear. High D rotates OpenStax IFT shapes including \(\sin x\); \(e^x\) is mid-high only (`d_max=18`). Formula \(\frac{d}{dx}\sin^{-1}\) stays on the inverse-trig leaf. Cube-root Example 3.61 is **not** a new core this pass.

## Limitations

- **Status:** shipped — catalog-routed IFT families. Remaining `LIMITATIONS`: closed numeric IFT template (scaffolded \(f(a)\) and \(f'(a)\)); not a general inverse AST; Example 3.61 cube-root and mixed \(\tan x+3x^2\) not invented.
- **Generator:** `derivative_inverse_functions`

## Proposed engine (reuse vs new)

**Reuse:** existing IFT Mad-Lib builders + `derivatives.json` form_ids with `d_min`/`d_max`. `invfn_trig` is the same template with \(f(x)=\sin x\) (OpenStax 267), not a new sampler.

- **Shipped this pass:** catalog routing; D=0 power-only; high D cannot emit `invfn_power` or leftover `invfn_exp`.
