# Notes — `u_sub_preset_bc_bank_ln_exp` (`calc_indef_int_logarithmic_rule_and_exponentials_with_substitution`)

Showcase gallery for a **named u-sub knob**, not a separate catalog leaf.
Forces `u_sub_form_preset=bc_bank` and `u_sub_construction=catalog` on the ln/exp host.

- **Skill:** BC drill-bank §1 ln/exp u-sub (`(ln x)^n/x`, `e^x/(a+e^x)^n`, nested ln)
- **Host leaf:** `calc_indef_int_logarithmic_rule_and_exponentials_with_substitution`
- **Bank:** `scripts/output/example_mining/challenging_indefinite_integrals_bc.tex`
- **OpenStax:** Calculus Volume 1 §5.6 —
  https://openstax.org/books/calculus-volume-1/pages/5-6-integrals-involving-exponential-and-logarithmic-functions

## Limitations

- **Status:** showcase — live generate on host leaf with forced knobs
- **LIMITATIONS:** Host flavor intersects `bc_bank`, so this page is ln/exp
  families only (algebraic bank forms stay on the power host). Forced
  challenging-bank at D=0 still shows high-`d_min` shapes via fallback.
  Checkpoint 5.33 (`exp_of_quartic`) is OpenStax, not this preset.

## What the question should look like

Live `_generate_for_type` with forced `bc_bank` + catalog (seed=101/207):

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int \frac{\left(\ln x\right)^{3}}{x}\,dx$ | $\frac{1}{4}\left(\ln x\right)^{4}+C$ | fallback `ln_power_over_x` (bank §1.6) |
| 0 | 207 | $\int \frac{\sin(\ln x)}{x}\,dx$ | $-\cos(\ln x)+C$ | fallback `cos_of_ln_over_x` (bank §1.19) |
| 8 | 101 | $\int \frac{\left(\ln x\right)^{3}}{x}\,dx$ | $\frac{1}{4}\left(\ln x\right)^{4}+C$ | `ln_power_over_x` |
| 16 | 207 | $\int \frac{1}{\left(x+1\right)\sqrt{\ln(x+1)}}\,dx$ | $2\sqrt{\ln(x+1)}+C$ | `root_ln_of_linear` (bank §1.22) |
| 22 | 101 | $\int \frac{\left(\ln x\right)^{2}}{x}\,dx$ | $\frac{1}{3}\left(\ln x\right)^{3}+C$ | `ln_power_over_x` |

## Proposed engine

Reuse `integrals.py` + `u_substitution.json`. No new type_id.
