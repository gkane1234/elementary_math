# Notes — `u_sub_reverse_chain_invtrig` (`calc_indef_int_inverse_trigonometric_with_substitution`)

Showcase gallery for a **named u-sub knob**, not a separate catalog leaf.
Forces `u_sub_form_preset=arctan_chain` and `u_sub_construction=reverse_chain` via
`extra_settings` in `gen_examples.py` SECTIONS.

- **Skill:** reverse-chain on the invtrig substitution leaf
- **Host leaf:** `calc_indef_int_inverse_trigonometric_with_substitution`
- **OpenStax:** Calculus Volume 1 §5.5–5.7 —
  https://openstax.org/books/calculus-volume-1/pages/5-5-substitution

## Limitations

- **Status:** showcase — live generate on host leaf with forced knobs
- **LIMITATIONS:** Reverse-chain elides Diff AST `x^{1}` on this consumer.
  Remaining unsimplified juxtaposition possible. Not a full OpenStax
  exercise bank.

## What the question should look like

- **D=0–8:** Forced family shapes only (catalog) or reverse-chain F∘g.
- **High D:** Same family; numeric hardness via skeleton tiers — no fake
  cost pads.

## Proposed engine

Reuse `integrals.py` + `u_substitution.py` / `u_substitution.json`. No new type_id.
