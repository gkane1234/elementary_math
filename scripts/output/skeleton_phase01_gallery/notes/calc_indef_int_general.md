# Notes — `calc_indef_int_general` (`calc_indef_int_general`)

Mixed-technique indefinite integral leaf, analogous to `calc_diff_general`.
Teacher `allow_*` checkboxes drop catalog forms whose `requires_allows` /
`tricks` are not all on. OpenStax table/power at low D; BC-bank families and
parts/PFD/trig-sub unlock mid/high D.

- **Skill:** choose and apply an allowed antiderivative technique
- **Generator:** `integral_general`
- **OpenStax:** Calculus Volume 1 §4.10 / §5.5–5.7 and Volume 2 §3.1–3.4
- **Bank extra families:** `scripts/output/example_mining/challenging_indefinite_integrals_bc.tex`

## Limitations

- **LIMITATIONS:** D=0 still rotates easy table trig (`∫ sin(kx)`, `∫ sec tan`)
  when `allow_trig` is on (default). Seed 101 at mid/high D can stay on the
  power rewrite form; other seeds pick parts / PFD / trig-sub. Reverse-chain
  u-sub may appear when substitution is on. Deferred bank items (`x^4+1`,
  Weierstrass, `ln(cos x)`) are not invented.

## What the question should look like (D=0 vs high D)

Live `sample_integral_expression` / `_generate_for_type` (seed=101/207/313):

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int \sqrt{x}\,dx$ | $\frac{2}{3}x^{\frac{3}{2}}+C$ | power / `sqrt_x` |
| 0 | 207 | $\int \sec(x)\tan(x)\,dx$ | $\sec(x)+C$ | table trig |
| 8 | 207 | $\int x\cos(3x)\,dx$ | $\frac{1}{3}x\sin(3x)+\frac{1}{9}\cos(3x)+C$ | parts (unlocked ≥8) |
| 16 | 207 | $\int \frac{-4x + 4}{\left(x - 2\right)^{2}}\,dx$ | $-4\ln\|x - 2\|+4\frac{1}{x - 2}+C$ | PFD |
| 16 | 313 | $\int \frac{x^{2}}{\sqrt{4-x^{2}}}\,dx$ | $-\frac{1}{2}x\sqrt{4-x^{2}}+2\arcsin\left(\frac{x}{2}\right)+C$ | trig-sub |

Opt-out flag used: none (this is a new mixed leaf; technique leaves still have old-path flags).

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy |
|------|-----|----------------|
| OpenStax Calculus Volume 1 §4.10 | https://openstax.org/books/calculus-volume-1/pages/4-10-antiderivatives | D=0 power / table |
| OpenStax Calculus Volume 1 §5.5 | https://openstax.org/books/calculus-volume-1/pages/5-5-substitution | u-sub families |
| OpenStax Calculus Volume 2 §3.1–3.4 | https://openstax.org/books/calculus-volume-2/pages/3-1-integration-by-parts | parts / trig / PFD / trig-sub |

## Variety notes

Toggles: `allow_parts` off → no `cyclic_exp_*` / tabular parts. `allow_pfd` off →
no distinct-linear / mixed PFD. `allow_trig` off → no trig catalog or trig u-sub
bank families (`trig_over_linear_trig_power`, `sin_of_sqrt`, …). Multi-trick
forms need every listed skill.

## Proposed engine

Reuse `integrals.py` catalogs + `filter_forms_by_allows`. No fake `difficulty_costs`.
