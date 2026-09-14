# Notes — `calc_diff_other_base_logarithms_and_exponentials`

- **Course:** Calculus
- **Category:** Calculus — Differentiation
- **Generator:** `derivative_other_base`
- **Suggested family:** other (calc limits / Diff)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Differentiate \(a^x\) and \(\log_a u\) (not \(\ln\)/\(e^u\), not log-diff \(x^x\)).
- **D=0:** \(a^x\) or \(\log_a x\) only (old easy).
- **Mid D (≈8):** Chain \(a^{kx}\) and \(\log_a(ax+b)\) (OpenStax Example 3.80 shape). Not leftover \(a^x\) / \(\log_a x\).
- **High D (≈16–22):** \(k\log_a x\) / \(\log_a(x^k)\), \(a^{x^2}\), \(x\cdot a^x\).
- **Must not:** Natural \(\ln\)/\(e^x\) leaf; log-diff \(x^x\); invented quotient \(a^x/(a^x+c)\).

## What old / live path actually produced (real latex, D=0/8/16/22)

**Old (pre-catalog routing):** D=0 \(a^x\) / \(\log_a x\); D=8 still dumped those leftovers plus \(a^{kx}\) / \(\log_a(ax+b)\); D=16/22 mixed all families including leftovers. \(a^{kx}\) answers concatenated (`23^{2x}` for \(2\cdot 3^{2x}\)).

**Live now** (`_generate_for_type`):

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\frac{d}{dx}\log_{2}(x)$` | `$\frac{1}{x\ln(2)}$` | form=`other_base_log_x` |
| 0 | 1 | `$\frac{d}{dx}\left[2^{x}\right]$` | `$2^{x}\ln(2)$` | form=`other_base_a_x` |
| 8 | 101 | `$\frac{d}{dx}\log_{3}(3x - 1)$` | `$\frac{3}{\left(3x - 1\right)\ln(3)}$` | form=`other_base_log_linear` |
| 8 | 1 | `$\frac{d}{dx}2^{4x}$` | `$4\cdot 2^{4x}\ln(2)$` | form=`other_base_a_kx` |
| 16 | 0 | `$\frac{d}{dx}\left[x\cdot 5^{x}\right]$` | `$5^{x}+x5^{x}\ln(5)$` | form=`other_base_product` |
| 16 | 1 | `$\frac{d}{dx}\left[\log_{2}(x^{3})\right]$` | `$\frac{3}{x\ln(2)}$` | form=`other_base_log_power` |
| 16 | 101 | `$\frac{d}{dx}3^{x^{2}}$` | `$2x3^{x^{2}}\ln(3)$` | form=`other_base_a_poly` |
| 22 | 0 | `$\frac{d}{dx}\left[x\cdot 5^{x}\right]$` | `$5^{x}+x5^{x}\ln(5)$` | form=`other_base_product` |

Opt-out flag used: _none — structured catalog on the existing Mad-Lib builders_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §3.9 Derivatives of Exponential and Logarithmic Functions | https://openstax.org/books/calculus-volume-1/pages/3-9-derivatives-of-exponential-and-logarithmic-functions | Checkpoint 3.53 \(y=3^x\); Example 3.80 \(\log_2(3x+1)\); \(a^{kx}\); \(x\cdot a^x\) |

Local HTML / mining: `scripts/output/example_mining/calculus-volume-1/stage1/3-9-derivatives-of-exponential-and-logarithmic-functions.md`

Catalog forms: `other_base_a_x`, `other_base_log_x`, `other_base_a_kx`, `other_base_log_linear`, `other_base_log_power`, `other_base_a_poly`, `other_base_product`.

## Variety notes

D=0 stays two easy frames (\(a^x\) and \(\log_a x\)), matching old easy. Mid/high rotate §3.9 chain / product shapes. Not a WP. Example 3.79 \(\frac{3^x}{3^x+2}\) and \(3^{\sin 3x}\) are **not** in the old pack — not invented this pass.

## Limitations

- **Status:** shipped — catalog-routed closed-form families. Remaining `LIMITATIONS`: not a general \(a^{g(x)}\) AST; no Example 3.79 quotient; no trig-in-exponent \(a^{\sin x}\).
- **Generator:** `derivative_other_base`

## Proposed engine (reuse vs new)

**Reuse:** existing `structured_other_base` builders + `derivatives.json` form_ids with `d_min`/`d_max` (same pattern as log-diff). No padded costs. Natural \(\ln/e^x\) stays on `calc_diff_natural_logarithms_and_exponentials`.

- **Shipped this pass:** catalog routing; D=0 \(a^x\)/\(\log_a x\) only; high D cannot emit those leftovers; `a^{kx}\) answer uses `\cdot`.
