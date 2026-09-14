# Notes — `u_sub_preset_challenging_ln_exp` (`calc_indef_int_logarithmic_rule_and_exponentials_with_substitution`)

Showcase gallery for a **named u-sub knob**, not a separate catalog leaf.
Forces `u_sub_form_preset=challenging` and `u_sub_construction=catalog` via
`extra_settings` in `gen_examples.py` SECTIONS.

- **Skill:** EMH-hard ln/exp u-sub (exp-cubic, exp-quartic, exp-root, (ln)², nested e^{trig})
- **Host leaf:** `calc_indef_int_logarithmic_rule_and_exponentials_with_substitution`
- **OpenStax:** Calculus Volume 1 §5.6 —
  https://openstax.org/books/calculus-volume-1/pages/5-6-integrals-involving-exponential-and-logarithmic-functions
  Example 5.38 ∫ e^x √(1+e^x); Example 5.39 ∫ 3x² e^{2x³}; Checkpoint 5.32 ∫ e^x (3e^x−2)²;
  Checkpoint 5.33 ∫ 2x³ e^{x⁴}

## Limitations

- **Status:** showcase — live generate on host leaf with forced knobs
- **LIMITATIONS:** Forced `challenging` at D=0 still falls back to high-d_min
  forms (select_form_id). Not a full §5.6 exercise bank.

## What the question should look like

Live `_generate_for_type` with forced knobs:

| D | seed | prompt_latex | answer_latex | shape notes |
|---|------|--------------|--------------|-------------|
| 0 | 101 | $\int 3x^{2}e^{x^{3}}\,dx$ | $e^{x^{3}}+C$ | `exp_of_cubic` (forced challenging fallback) |
| 0 | 207 | $\int e^{x}\sqrt{1+e^{x}}\,dx$ | $\frac{2}{3}\left(1+e^{x}\right)^{\frac{3}{2}}+C$ | `exp_root_chain` Example 5.38 |
| 8 | 207 | $\int 2x^{3}e^{-2x^{4}}\,dx$ | $-\frac{1}{4}e^{-2x^{4}}+C$ | `exp_of_quartic` |
| 8 | 313 | $\int 2x^{3}e^{x^{4}}\,dx$ | $\frac{1}{2}e^{x^{4}}+C$ | Checkpoint 5.33 exact |
| 16 | 207 | $\int e^{\cos(2x)}\sin(2x)\,dx$ | $-\frac{1}{2}e^{\cos(2x)}+C$ | `nested_trig_exp` |

Example 5.38 shape (D=16, other seeds): $\int e^{x}\sqrt{1+e^{x}}\,dx$ → $\frac{2}{3}\left(1+e^{x}\right)^{\frac{3}{2}}+C$.

## Proposed engine

Reuse `integrals.py` + `u_substitution.json`. No new type_id.
