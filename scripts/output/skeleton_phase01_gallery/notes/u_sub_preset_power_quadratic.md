# Notes — `u_sub_preset_power_quadratic` (`calc_indef_int_power_rule_with_substitution`)

Showcase gallery for a **named u-sub knob**, not a separate catalog leaf.
Forces `u_sub_form_preset=power_quadratic` and `u_sub_construction=catalog` via
`extra_settings` in `gen_examples.py` SECTIONS.

- **Skill:** quad / root-of-quad with x du factor
- **Host leaf:** `calc_indef_int_power_rule_with_substitution`
- **OpenStax:** Calculus Volume 1 §5.5–5.7 —
  https://openstax.org/books/calculus-volume-1/pages/5-5-substitution

## Limitations

- **Status:** showcase — live generate on host leaf with forced knobs
- **LIMITATIONS:** Host-leaf flavor still intersects the preset form set
  (power leaf + `challenging` only hits power-eligible forms unless the
  preset falls through to the full set). Reverse-chain latex follows Diff
  AST rendering (extra `x^{1}` factors possible). Not a full OpenStax
  exercise bank.

## What the question should look like

- **D=0–8:** Forced family shapes only (catalog) or reverse-chain F∘g.
- **High D:** Same family; numeric hardness via skeleton tiers — no fake
  cost pads.

## Proposed engine

Reuse `integrals.py` + `u_substitution.py` / `u_substitution.json`. No new type_id.
