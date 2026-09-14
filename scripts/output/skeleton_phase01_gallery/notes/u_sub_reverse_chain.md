# Notes — `u_sub_reverse_chain` (`calc_indef_int_power_rule_with_substitution`)

Showcase gallery for a **named u-sub knob**, not a separate catalog leaf.
Forces `u_sub_form_preset=auto` and `u_sub_construction=reverse_chain` via
`extra_settings` in `gen_examples.py` SECTIONS.

- **Skill:** Diff F∘g sampled; prompt is F′; answer F+C
- **Host leaf:** `calc_indef_int_power_rule_with_substitution`
- **OpenStax:** Calculus Volume 1 §5.5–5.7 —
  https://openstax.org/books/calculus-volume-1/pages/5-5-substitution

## Limitations

- **Status:** showcase — live generate on host leaf with forced knobs
- **LIMITATIONS:** Reverse-chain now elides Diff AST `x^{1}` in the integrand
  (this consumer only; chain-rule leaves keep pedagogical `^{1}`). Remaining:
  unsimplified juxtaposition (`2x\left(-4\right)`), D=0 extra chain-constant
  factors, high-D inner polys. Not a full OpenStax exercise bank.

## What the question should look like

Live `_generate_for_type` with forced knobs (seed=101/207):

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int 2\left(-2x\right)\left(-2\right)\,dx$ | $\left(-2x\right)^{2}+C$ | no `x^{1}` |
| 8 | 101 | $\int 3\left(3x + 4\right)^{2}\left(3\right)\,dx$ | $\left(3x + 4\right)^{3}+C$ | linear inner |
| 16 | 101 | $\int \left(3x + 4\right)^{2}\,dx$ | $\frac{1}{9}\left(3x + 4\right)^{3}+C$ | omit leading const |
| 16 | 207 | $\int \left(-4x^{3} + 4x - 3\right)^{2}\left(3x^{2}\left(-4\right) + 4\right)\,dx$ | $\frac{1}{3}\left(-4x^{3} + 4x - 3\right)^{3}+C$ | poly inner |

## Proposed engine

Reuse `integrals.py` + `u_substitution.py` / `u_substitution.json`. No new type_id.
