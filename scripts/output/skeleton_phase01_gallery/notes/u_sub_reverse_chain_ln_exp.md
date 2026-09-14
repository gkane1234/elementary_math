# Notes — `u_sub_reverse_chain_ln_exp` (`calc_indef_int_logarithmic_rule_and_exponentials_with_substitution`)

Showcase gallery for a **named u-sub knob**, not a separate catalog leaf.
Forces `u_sub_form_preset=auto` and `u_sub_construction=reverse_chain` via
`extra_settings` in `gen_examples.py` SECTIONS.

- **Skill:** reverse-chain on the ln/exp substitution leaf
- **Host leaf:** `calc_indef_int_logarithmic_rule_and_exponentials_with_substitution`
- **OpenStax:** Calculus Volume 1 §5.5–5.7 —
  https://openstax.org/books/calculus-volume-1/pages/5-5-substitution

## Limitations

- **Status:** showcase — live generate on host leaf with forced knobs
- **LIMITATIONS:** `x^{1}` elided in reverse-chain display. High-D
  `chain_nested` can still emit e^{ln(…)} / sin(e^{poly}) compositions that are
  valid F′g′ but richer than typical OpenStax §5.6 drills. Not a full exercise
  bank.

## What the question should look like

Live `_generate_for_type` with forced knobs (seed=101/207):

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int e^{-x}\left(-1\right)\,dx$ | $e^{-x}+C$ | `exp_basic` |
| 0 | 207 | $\int \frac{-3}{-3x - 3}\,dx$ | $\ln\left(-3x - 3\right)+C$ | `ln_basic` |
| 16 | 207 | $\int \left(-\sin\left(e^{-5x^{2} + 5}\right)\right)e^{-5x^{2} + 5}\left(2x\left(-5\right)\right)\,dx$ | $\cos\left(e^{-5x^{2} + 5}\right)+C$ | nested; no `x^{1}` |

## Proposed engine

Reuse `integrals.py` + `u_substitution.py` / `u_substitution.json`. No new type_id.
