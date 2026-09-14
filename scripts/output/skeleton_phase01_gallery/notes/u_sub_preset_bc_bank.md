# Notes — `u_sub_preset_bc_bank` (`calc_indef_int_power_rule_with_substitution`)

Showcase gallery for a **named u-sub knob**, not a separate catalog leaf.
Forces `u_sub_form_preset=bc_bank` and `u_sub_construction=catalog`.

- **Skill:** BC drill-bank §1 algebraic u-sub (negative powers of quadratic/cubic/hex, roots)
- **Host leaf:** `calc_indef_int_power_rule_with_substitution`
- **Bank:** `scripts/output/example_mining/challenging_indefinite_integrals_bc.tex`
- **OpenStax:** Calculus Volume 1 §5.5 —
  https://openstax.org/books/calculus-volume-1/pages/5-5-substitution
  (shapes first; bank is extra high-D families)

## Limitations

- **Status:** showcase — live generate on host leaf with forced knobs
- **LIMITATIONS:** Host flavor ∩ `bc_bank` is algebraic (quad/cubic/hex/root).
  Trig bank families (`trig_over_linear_trig_power`, `sin_of_sqrt`) need
  `allow_trig` on this power host (default off). Forced `bc_bank` at D=0 still
  shows high-`d_min` shapes via `select_form_id` fallback. Families are
  parameterized lookalikes (`∫ ax/(bx^{2}+c)^{n}`), not only the exact bank
  line `∫ x/(x^{2}+1)^{4}`. Not the full bank (parts / PFD / Weierstrass live
  on other leaves).

## What the question should look like

Live `_generate_for_type` with forced `bc_bank` + catalog (seed=101/207):

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int \frac{2x+2}{x^{2}+2x+4}\,dx$ | $\ln|x^{2}+2x+4|+C$ | fallback `du_over_u_quadratic` |
| 0 | 207 | $\int \frac{x}{\sqrt{4-x^{2}}}\,dx$ | $-\sqrt{4-x^{2}}+C$ | fallback `root_quad_minus` (bank §1.4) |
| 8 | 101 | $\int \frac{2x+2}{x^{2}+2x+6}\,dx$ | $\ln|x^{2}+2x+6|+C$ | `du_over_u_quadratic` |
| 16 | 101 | $\int \frac{x}{\left(x^{2}+9\right)^{2}}\,dx$ | $-\frac{1}{2\left(x^{2}+9\right)}+C$ | `power_quad_neg` lookalike |
| 16 | 6 | $\int \frac{x}{\left(2x^{2}+1\right)^{3}}\,dx$ | $-\frac{1}{8\left(2x^{2}+1\right)^{2}}+C$ | sampled $b=2$, $n=3$ |
| 22 | 101 | $\int \frac{x}{\left(x^{2}+1\right)^{4}}\,dx$ | $-\frac{1}{6\left(x^{2}+1\right)^{3}}+C$ | exact bank §1.1 (one draw) |
| 22 | 207 | $\int \frac{x^{5}}{\left(x^{6}+6\right)^{2}}\,dx$ | $-\frac{1}{6\left(x^{6}+6\right)}+C$ | `power_hex_neg` |

## Proposed engine

Reuse `integrals.py` + `u_substitution.json`. No new type_id. No fake `difficulty_costs`.
