# Notes — `calc_indef_int_partial_fractions` (`Partial fractions`)

- **Course:** Calculus
- **Category:** Calculus — Indefinite Integration
- **Generator:** `integral_partial_fractions`
- **Suggested family:** other (integrals)

---

## What the question should look like (D=0 vs high D)

- **Skill:** Decompose a rational integrand by partial fractions and integrate termwise.
- **D=0:** Two distinct linear factors only (old easy) — \(\int (Ax+B)/((x-r_1)(x-r_2))\).
- **Mid D (≈8):** Leftover two-linear plus three linears and irreducible quadratic \(\to\) arctan or \(\ln(x^2+a^2)\).
- **High D (≈16–22):** Repeated linear \((x-a)^2\), mixed linear+quad, three distinct linears. Not two-linear leftovers. Not single-term \(\int C/(x^2+a^2)\).
- **Must not:** u-sub-then-PFD pipelines (multi-trick leaf); fake difficulty via cost pads; invent cube / improper / \((x^2+1)^2\) / \(x^4+1\) cores.

## What old / live path actually produced (real latex, D=0/8/16/22)

**Old (pre-`d_max` on `distinct_linear_2`):** D=16/22 seed 101 still two distinct linears.

**Before this leftover pass** (`_generate_for_type`): D=0 two-linear; D=8 leftover mix including single-term quad; D=16/22 named `pfd_form_preset=bc_bank` still 12/40 single-term `irreducible_quad_*` (not a decomposition). Stamps already `form_id` + `generator=integral_partial_fractions`.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int \frac{6x}{x^{2} - 9}\,dx$ | $3\ln\lvert x - 3\rvert+3\ln\lvert x + 3\rvert+C$ | form=`distinct_linear_2` |
| 0 | 207 | $\int \frac{5x - 3}{x^{2} - 9}\,dx$ | $2\ln\lvert x - 3\rvert+3\ln\lvert x + 3\rvert+C$ | two linears only |
| 8 | 101 | $\int \frac{16x - 32}{2x^{2} - 8x + 6}\,dx$ | $4\ln\lvert x - 3\rvert+4\ln\lvert x - 1\rvert+C$ | leftover `distinct_linear_2` |
| 8 | 207 | $\int \frac{-4x}{x^{2} + 1}\,dx$ | $-2\ln\lvert x^{2}+1\rvert+C$ | form=`irreducible_quad_ln` leftover |
| 16 | 101 | $\int \frac{9x^{2} - 51x + 68}{\left(x - 2\right)\left(x - 3\right)\left(x - 4\right)}\,dx$ | $\ln\lvert x - 2\rvert+4\ln\lvert x - 3\rvert+4\ln\lvert x - 4\rvert+C$ | form=`distinct_linear_3` |
| 16 | 207 | $\int \frac{-4x - 12}{\left(x + 2\right)^{2}}\,dx$ | $-4\ln\lvert x + 2\rvert+4\frac{1}{x + 2}+C$ | form=`repeated_linear_square` |

Opt-out flag used: _none — live catalog on `integrals.py` PFD sampler_

## What live path produces now (real latex)

Leftover lockout of D=0 two-linear and of single-term quad at D≥16 on the existing core. Catalog `d_max=15` on `irreducible_quad_*`; exclusive leftover bands; EMH-hard still stamps `pfd_form_preset=bc_bank` (intersects the band). 40-seed counts: D=0 two-linear-only; D=8 leftover two-linear (10) + 3-linear (8) + irred (22); D=16/22 three-linear (15) / mixed (11) / repeated (14) — no two-linear, no single-term quad.

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int \frac{6x}{x^{2} - 9}\,dx$ | $3\ln\lvert x - 3\rvert+3\ln\lvert x + 3\rvert+C$ | `distinct_linear_2` leftover |
| 0 | 207 | $\int \frac{5x - 3}{x^{2} - 9}\,dx$ | $2\ln\lvert x - 3\rvert+3\ln\lvert x + 3\rvert+C$ | two linears only |
| 8 | 101 | $\int \frac{16x - 32}{2x^{2} - 8x + 6}\,dx$ | $4\ln\lvert x - 3\rvert+4\ln\lvert x - 1\rvert+C$ | two-linear leftover |
| 8 | 207 | $\int \frac{-4x}{x^{2} + 1}\,dx$ | $-2\ln\lvert x^{2}+1\rvert+C$ | irred-quad leftover (mid) |
| 16 | 101 | $\int \frac{9x^{2} - 51x + 68}{\left(x - 2\right)\left(x - 3\right)\left(x - 4\right)}\,dx$ | $\ln\lvert x - 2\rvert+4\ln\lvert x - 3\rvert+4\ln\lvert x - 4\rvert+C$ | `distinct_linear_3` |
| 16 | 207 | $\int \frac{-4x - 12}{\left(x + 2\right)^{2}}\,dx$ | $-4\ln\lvert x + 2\rvert+4\frac{1}{x + 2}+C$ | `repeated_linear_square` |
| 22 | 101 | $\int \frac{10x^{2} - 18x + 4}{2\left(x - 1\right)\left(x - 2\right)\left(x\right)}\,dx$ | $2\ln\lvert x - 1\rvert+2\ln\lvert x - 2\rvert+\ln\lvert x\rvert+C$ | `distinct_linear_3` leftover |
| 22 | 207 | $\int \frac{-4x - 12}{\left(x + 2\right)^{2}}\,dx$ | $-4\ln\lvert x + 2\rvert+4\frac{1}{x + 2}+C$ | repeated; no single-term quad |

Opt-out flag used: _none — live catalog on `integrals.py` PFD sampler_

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 2 §3.4 Partial Fractions | https://openstax.org/books/calculus-volume-2/pages/3-4-partial-fractions | Distinct linear; repeated linear; irreducible quadratic \(\to\) arctan/ln; mixed; improper (long division) |

Catalog forms: `distinct_linear_2` (`d_max=10`), `distinct_linear_3`, `irreducible_quad_arctan` / `irreducible_quad_ln` (`d_max=15`), `mixed_linear_quad`, `repeated_linear_square`. Named preset `pfd_form_preset=bc_bank`. Stubs/deferred: `repeated_linear_cube`, `improper_long_division`, `repeated_quad_square` (\((x^2+1)^2\)), `x4_plus_1` (\(1/(x^4+1)\)).

## Variety notes

D=0 stays one easy frame (two linears). D=8 leftover two-linear + unlocks. High D cannot emit two-linear or single-term quad. Not a WP. u-sub\(\to\)PFD stays on `calc_indef_int_multi_trick`.

## Limitations

- **Status:** leftover lockout of D=0 two-linear and of single-term quad \(\int C/(x^2+a^2)\) shipped. Remaining `LIMITATIONS`: `repeated_linear_cube` and `improper_long_division` still stubs; `repeated_quad_square` / `x4_plus_1` deferred (no repeated-quad spine / no honest \(x^4+1\) factorization); D=16 and D=22 are the same 3-linear / mixed / repeated mix; D=8 can still emit two-linear and single-term quad leftover (intentional); mixed-form latex can look over-parenthesized.
- **Live pairwise:** each item stamps `form_id`, `generator=integral_partial_fractions`, and `family`; copies `form_id` / `generator` onto `spec_snapshot`. Form pick uses `select_form_id` so `live_quality_form_weights` can tilt inside the leftover band.
- **Generator:** `integral_partial_fractions`

## Proposed engine (reuse vs new)

- **Reuse:** existing `integrals.py` `_sample_pfd_integral` + `partial_fractions.json`. Exclusive leftover bands + catalog `d_max` on two-linear / single-term quad. No padded `difficulty_costs`. Did not invent cube / improper / repeated-quad / \(x^4+1\) cores.
- **Shipped this pass:** leftover lockout of D=0 two-linear and of single-term quad at D≥16; `pfd_forms_for_difficulty`; leaf `generator` stamp on `spec_snapshot`.
