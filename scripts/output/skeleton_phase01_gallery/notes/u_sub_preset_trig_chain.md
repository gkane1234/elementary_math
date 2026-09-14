# Notes — `u_sub_preset_trig_chain` (`calc_indef_int_power_rule_with_substitution`)

Showcase gallery for a **named u-sub knob**, not a separate catalog leaf.
Forces `u_sub_form_preset=trig_chain` and `u_sub_construction=catalog` via
`extra_settings` in `gen_examples.py` SECTIONS.

- **Skill:** sin/cos/sec² of an inner u, plus cot/tan rewrite (∫ cot = ln|sin|)
- **Host leaf:** `calc_indef_int_power_rule_with_substitution`
- **OpenStax:** Calculus Volume 1 §5.5–5.7 —
  https://openstax.org/books/calculus-volume-1/pages/5-5-substitution

## Limitations

- **Status:** showcase — live generate on host leaf with forced knobs
- **LIMITATIONS:** Empty flavor∩preset on this power host falls through to the
  full `trig_chain` set (including `composite_ln_of_trig`). Checkpoint 5.28
  (∫ cos³ t sin t) is still covered only partly by `du_over_u_trig`. Not a
  full OpenStax exercise bank.

## What the question should look like

- **D=0–8:** Forced family shapes only (catalog) or reverse-chain F∘g.
- **High D:** Same family; numeric hardness via skeleton tiers — no fake
  cost pads.

## Proposed engine

Reuse `integrals.py` + `u_substitution.py` / `u_substitution.json`. No new type_id.
