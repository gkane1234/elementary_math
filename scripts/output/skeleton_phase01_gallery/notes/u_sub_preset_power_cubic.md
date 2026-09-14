# Notes — `u_sub_preset_power_cubic` (`calc_indef_int_power_rule_with_substitution`)

Showcase gallery for a **named u-sub knob**, not a separate catalog leaf.
Forces `u_sub_form_preset=power_cubic` and `u_sub_construction=catalog` via
`extra_settings` in `gen_examples.py` SECTIONS.

- **Skill:** ∫ 3x² (x³±c)^n (omit the 3 at high format tier)
- **Host leaf:** `calc_indef_int_power_rule_with_substitution`
- **OpenStax:** Calculus Volume 1 §5.5 —
  https://openstax.org/books/calculus-volume-1/pages/5-5-substitution
  Checkpoint 5.25 ∫ 3x²(x³−3)²; Checkpoint 5.26 ∫ x²(x³+5)⁹

## Limitations

- **Status:** showcase — live generate on host leaf with forced knobs
- **LIMITATIONS:** High-D omit-3 matches Checkpoint 5.26’s missing constant, but
  exponents follow numeric-tier (n≤6) rather than the textbook’s n=9. Not the
  full §5.5 exercise set.

## What the question should look like

Live `_generate_for_type` with forced knobs (seed=101/207):

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int 3x^{2}\left(x^{3}+3\right)^{2}\,dx$ | $\frac{1}{3}\left(x^{3}+3\right)^{3}+C$ | visible 3x² du |
| 8 | 207 | $\int 3x^{2}\left(x^{3}-1\right)^{3}\,dx$ | $\frac{1}{4}\left(x^{3}-1\right)^{4}+C$ | signed shift |
| 16 | 101 | $\int x^{2}\left(x^{3}+9\right)^{2}\,dx$ | $\frac{1}{9}\left(x^{3}+9\right)^{3}+C$ | omit 3 (format_tier≥2) |
| 22 | 207 | $\int x^{2}\left(x^{3}+6\right)^{6}\,dx$ | $\frac{1}{21}\left(x^{3}+6\right)^{7}+C$ | higher n |

## Proposed engine

Reuse `integrals.py` + `u_substitution.json` form `power_cubic_x2_du`. No new type_id.
