# Notes — `calc_def_int_substitution_with_change_of_variables`

- **Display name:** Substitution with change of variables
- **Category:** Calculus — Definite Integration
- **Generator:** `integral_definite_substitution`
- **Suggested family:** `integral`

---

## Limitations

- **Status:** shipped — live generator
- **Generator:** `integral_definite_substitution`
- **Remaining limits:** D=0 linear changed-limits is solid. High D unlocks quad / $du/u$, but some seeds still draw `definite_power_linear_du` at D=16–22 (uniform family pick, not a padded cost). Named EMH presets on this leaf lock power/challenging families that the definite sampler does not fully consume.

## What the question should look like (D=0 vs high D)

- **Skill:** Definite u-sub with changed limits (not indefinite +C).
- **D=0:** $\int_0^b p(px+q)^n\,dx$ linear u.
- **High D:** quadratic inner / $du/u$ forms.
- **Must not:** Indefinite-only prompts on this leaf (see `calc_indef_int_power_rule_with_substitution`).

## What live path actually produced (real latex, D=0/8/16/22)

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int_{0}^{3} 2\left(2x + 2\right)^{2}\,dx$ | $168$ | form=`definite_power_linear_du` |
| 0 | 207 | $\int_{0}^{1} 2\left(2x\right)^{2}\,dx$ | $\frac{8}{3}$ | form=`definite_power_linear_du` |
| 8 | 101 | $\int_{0}^{3} 2\left(2x + 2\right)^{2}\,dx$ | $168$ | form=`definite_power_linear_du` |
| 8 | 207 | $\int_{0}^{1} 2x\left(x^{2}+1\right)^{2}\,dx$ | $\frac{7}{3}$ | form=`definite_power_quad_x_du` |
| 16 | 101 | $\int_{0}^{3} 2\left(2x + 2\right)^{2}\,dx$ | $168$ | form=`definite_power_linear_du` |
| 16 | 207 | $\int_{0}^{3} \frac{2x}{x^{2}+1}\,dx$ | $\ln(10)$ | form=`definite_du_over_u` |
| 22 | 101 | $\int_{0}^{3} 2\left(2x + 2\right)^{2}\,dx$ | $168$ | form=`definite_power_linear_du` |
| 22 | 207 | $\int_{0}^{3} \frac{2x}{x^{2}+1}\,dx$ | $\ln(10)$ | form=`definite_du_over_u` |

Opt-out flag used: `(none)`

## OpenStax examples + chapter/section cites

| Cite | URL | What to copy (shape / frame, not wording) |
|------|-----|-------------------------------------------|
| OpenStax Calculus Volume 1 §5.5 | https://openstax.org/books/calculus-volume-1/pages/5-5-substitution | Definite substitution; change limits with $u$ |

## Variety notes

Clear gold after split from indefinite `integral_substitution`.

## Proposed engine (reuse vs new)

- **Proposal:** `integrals.py` pack `integral_u_sub_definite` / generator `integral_definite_substitution`.
- **New Integral skeleton?** no.
- **Shipped:** definite sampler + catalog wiring.

_Catalog generator `integral_definite_substitution`._
