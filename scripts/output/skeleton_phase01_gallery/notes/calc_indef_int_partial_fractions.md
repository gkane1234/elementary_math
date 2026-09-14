# Notes — `calc_indef_int_partial_fractions` (`Partial fractions`)

- **Course:** Calculus
- **Category:** Calculus — Indefinite Integration
- **Generator:** `integral_partial_fractions`
- **Suggested family:** other (integrals)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Decompose a rational integrand by partial fractions and integrate termwise.
- **D=0:** Two distinct linear factors only (old easy) — \(\int (Ax+B)/((x-r_1)(x-r_2))\).
- **Mid D (≈8):** Unlock three linears, irreducible quadratic \(\to\) arctan or \(\ln(x^2+a^2)\). Two-linear leftovers still allowed.
- **High D (≈16–22):** Repeated linear \((x-a)^2\), mixed linear+quad, three distinct linears. Not two-linear leftovers.
- **Must not:** u-sub-then-PFD pipelines (multi-trick leaf); fake difficulty via cost pads.

## What old / live path actually produced (real latex, D=0/8/16/22)

**Old (pre-`d_max` on `distinct_linear_2`):** D=16/22 seed 101 still two distinct linears.

**Live now** (`_generate_for_type`):

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | `$\int \frac{6x}{x^{2} - 9}\,dx$` | `$3\ln\lvert x - 3\rvert+3\ln\lvert x + 3\rvert+C$` | form=`distinct_linear_2` |
| 0 | 207 | `$\int \frac{5x - 3}{x^{2} - 9}\,dx$` | `$2\ln\lvert x - 3\rvert+3\ln\lvert x + 3\rvert+C$` | two linears only |
| 8 | 101 | `$\int \frac{16x - 32}{2x^{2} - 8x + 6}\,dx$` | `$4\ln\lvert x - 3\rvert+4\ln\lvert x - 1\rvert+C$` | still `distinct_linear_2` (D≤10) |
| 8 | 207 | `$\int \frac{-4x}{x^{2} + 1}\,dx$` | `$-2\ln\lvert x^{2}+1\rvert+C$` | form=`irreducible_quad_ln` |
| 16 | 101 | `$\int \frac{9x^{2} - 51x + 68}{\left(x - 2\right)\left(x - 3\right)\left(x - 4\right)}\,dx$` | `$\ln\lvert x - 2\rvert+4\ln\lvert x - 3\rvert+4\ln\lvert x - 4\rvert+C$` | form=`distinct_linear_3` |
| 16 | 207 | `$\int \frac{-4x - 12}{\left(x + 2\right)^{2}}\,dx$` | `$-4\ln\lvert x + 2\rvert+4\frac{1}{x + 2}+C$` | form=`repeated_linear_square` |
| 22 | 101 | `$\int \frac{10x^{2} - 18x + 4}{2\left(x - 1\right)\left(x - 2\right)\left(x\right)}\,dx$` | `$2\ln\lvert x - 1\rvert+2\ln\lvert x - 2\rvert+\ln\lvert x\rvert+C$` | form=`distinct_linear_3` |
| 22 | 207 | `$\int \frac{-4x - 12}{\left(x + 2\right)^{2}}\,dx$` | `$-4\ln\lvert x + 2\rvert+4\frac{1}{x + 2}+C$` | form=`repeated_linear_square` |

Opt-out flag used: _none — live catalog on `integrals.py` PFD sampler_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 2 §3.4 Partial Fractions | https://openstax.org/books/calculus-volume-2/pages/3-4-partial-fractions | Distinct linear; repeated linear; irreducible quadratic \(\to\) arctan/ln; mixed; improper (long division) |

Catalog forms: `distinct_linear_2` (`d_max=10`), `distinct_linear_3`, `irreducible_quad_arctan`, `irreducible_quad_ln`, `mixed_linear_quad`, `repeated_linear_square`. Named preset `pfd_form_preset=bc_bank`. Stubs/deferred: `repeated_linear_cube`, `improper_long_division`, `repeated_quad_square` (\((x^2+1)^2\)), `x4_plus_1` (\(1/(x^4+1)\)).

## Variety notes

D=0 stays one easy frame (two linears). Mid/high D rotate §3.4 families. Not a WP. u-sub\(\to\)PFD stays on `calc_indef_int_multi_trick`.

## Limitations

- **Status:** shipped — catalog `d_max` lockout of two-linear leftovers at high D; `pfd_form_preset=bc_bank` for §4 lookalikes the existing core can emit. Remaining `LIMITATIONS`: `repeated_linear_cube` and `improper_long_division` still stubs; `repeated_quad_square` / `x4_plus_1` deferred (no repeated-quad spine / no honest \(x^4+1\) factorization); high D can still emit single-term quad \(\int C/(x^2+a^2)\) (not a decomposition); mixed-form latex can look over-parenthesized.
- **Generator:** `integral_partial_fractions`

## Proposed engine (reuse vs new)

**Reuse:** existing `integrals.py` `_sample_pfd_integral` + `partial_fractions.json` `d_min`/`d_max` (same pattern as parts `ln_alone` / implicit `implicit_basic`). No padded costs. Do not invent a cube/improper differentiator this pass.

- **Shipped this pass:** `distinct_linear_2` `d_max=10`; D=0 still two-linear-only; high D cannot emit `distinct_linear_2`.
