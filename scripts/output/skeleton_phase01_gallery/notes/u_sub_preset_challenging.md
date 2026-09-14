# Notes — `u_sub_preset_challenging` (`calc_indef_int_power_rule_with_substitution`)

Showcase gallery for a **named u-sub knob**, not a separate catalog leaf.
Forces `u_sub_form_preset=challenging` and `u_sub_construction=catalog` via
`extra_settings` in `gen_examples.py` SECTIONS.

- **Skill:** EMH-hard algebraic challenging set (cubic, root-quad, alteration)
- **Host leaf:** `calc_indef_int_power_rule_with_substitution`
- **OpenStax:** Calculus Volume 1 §5.5–5.7 —
  https://openstax.org/books/calculus-volume-1/pages/5-5-substitution

## Limitations

- **Status:** showcase — live generate on host leaf with forced knobs
- **LIMITATIONS:** Host-leaf flavor intersects the preset, so this power host
  only emits `power_cubic_x2_du` / `root_quad_x_du` /
  `alteration_linear_over_root` (trig/exp challenging forms stay on the ln/exp
  host). Forced challenging at D=0 still shows high-d_min shapes via
  select_form_id fallback. Not a full OpenStax exercise bank.

## What the question should look like

Live `_generate_for_type` with forced knobs (seed=101/207):

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int x\sqrt{x^{2}+3}\,dx$ | $\frac{1}{3}\left(x^{2}+3\right)^{\frac{3}{2}}+C$ | `root_quad_x_du` |
| 8 | 101 | $\int 3x^{2}\left(x^{3}+5\right)^{2}\,dx$ | $\frac{1}{3}\left(x^{3}+5\right)^{3}+C$ | Checkpoint 5.25 cubic |
| 16 | 101 | $\int x^{2}\left(x^{3}+9\right)^{2}\,dx$ | $\frac{1}{9}\left(x^{3}+9\right)^{3}+C$ | cubic omit-3 |
| 16 | 207 | $\int \frac{x}{\sqrt{x-1}}\,dx$ | $\frac{2}{3}\left(x-1\right)^{\frac{3}{2}}+2\sqrt{x-1}+C$ | Example 5.33 |

## Proposed engine

Reuse `integrals.py` + `u_substitution.py` / `u_substitution.json`. No new type_id.
