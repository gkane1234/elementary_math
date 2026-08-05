# Calc 1 algebraic gallery

Generated: 2026-08-05T01:56:31.131582+00:00

Live samples via `_generate_for_type` (D = 0, 3, 6, 8, 12, 16, 20, 25; 3 seeds each). No Easy/Medium/Hard labels — continuous **D=** only.

Open [gallery.html](gallery.html) in a browser for KaTeX (local `_assets/katex`).

- topics ok: **32** · skipped missing: **0**
- samples ok: **768** · errors: **0**
- metadata: `form_id` / `openstax_form`, `tricks_required`, `spec_snapshot` pack, shape when present
- difficulty: `difficulty_costs` breakdown (`form` / `dress` / `spec` → cost) in Metadata column (heuristic sum; correlates with D, not a calibrated effort model)
- form diversity: see [FORM_ID_INDEX.md](FORM_ID_INDEX.md)

## Structure inventory

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **150** · samples: **768**

| Structure / family | Count |
|--------|------:|
| `du_over_u_linear` | 29 |
| `power_linear_du` | 26 |
| `product_two_poly` | 26 |
| `quotient_poly` | 26 |
| `chain_power_linear` | 23 |
| `power_poly` | 18 |
| `linear` | 16 |
| `piecewise_jump_poly` | 15 |
| `sin` | 15 |
| `u_sub_then_pfd_trig` | 14 |
| `invtrig_arctan` | 13 |
| `removable_linear_factor` | 12 |
| `inf_rational` | 11 |
| `linear_approximation:quad` | 11 |
| `chain_nested` | 10 |
| `distinct_linear_2` | 10 |
| `product_poly_exp` | 10 |
| `removable_rationalize` | 10 |
| `chain_trig_poly` | 9 |
| `piecewise_jump` | 9 |
| `sqrt` | 9 |
| `lhopital_0_0_poly` | 8 |
| `ln_alone` | 8 |
| `quad` | 8 |
| `removable_diff_sq` | 8 |
| `root_quad_x_du` | 8 |
| `sqrt_a2_minus_x2` | 8 |
| `continuity_poly` | 7 |
| `essential_1_over_x` | 7 |
| `exp_k` | 7 |
| `higher_order_3` | 7 |
| `invtrig_chained` | 7 |
| `power_quad_x_du` | 7 |
| `power_root` | 7 |
| `product_poly_trig` | 7 |
| `alteration_linear_over_root` | 6 |
| `arctan_basic` | 6 |
| `arctan_of_linear` | 6 |
| `higher_order_2` | 6 |
| `linear_approximation:sqrt` | 6 |
| `ln` | 6 |
| `piecewise_jump_linear` | 6 |
| `rational_direct` | 6 |
| `sqrt_x` | 6 |
| `trig_basic` | 6 |
| `arcsin_a2` | 5 |
| `arcsin_basic` | 5 |
| `base_a` | 5 |
| `differentials:ln` | 5 |
| `essential_rational_va` | 5 |
| `exp_basic` | 5 |
| `poly_sum` | 5 |
| `power_negative` | 5 |
| `quotient_log_poly` | 5 |
| `quotient_trig_poly` | 5 |
| `u_sub_then_pfd_exp` | 5 |
| `u_sub_then_pfd_log` | 5 |
| `x_sqrt_x` | 5 |
| `arctan_a2` | 4 |
| `basic_cos_kx` | 4 |
| `differentials:radical` | 4 |
| `direct_sin_shift` | 4 |
| `distinct_linear_3` | 4 |
| `du_over_u_trig` | 4 |
| `essential_cos_1_over_x` | 4 |
| `exp` | 4 |
| `exp_of_poly` | 4 |
| `general_mixed` | 4 |
| `inf_arctan` | 4 |
| `inf_sin_over_x` | 4 |
| `invtrig_arcsin` | 4 |
| `linear_approximation:reciprocal` | 4 |
| `one_over_sqrt_x2_minus_a2` | 4 |
| `poly1_sin` | 4 |
| `poly_direct` | 4 |
| `quotient_exp_poly` | 4 |
| `rewrite_over_x` | 4 |
| `arctan_scaled` | 3 |
| `continuity_linear` | 3 |
| `differentials:poly_power` | 3 |
| `differentials:poly_quad` | 3 |
| `differentials:trig` | 3 |
| `direct_ln` | 3 |
| `essential_1_over_x_sq` | 3 |
| `essential_sin_1_over_x` | 3 |
| `exp_of_trig` | 3 |
| `inf_ln_over_poly` | 3 |
| `irreducible_quad_ln` | 3 |
| `lhopital_inf_inf_poly` | 3 |
| `linear_approximation:exp` | 3 |
| `ln_basic` | 3 |
| `ln_exp_product` | 3 |
| `mixed_linear_quad` | 3 |
| `neg_power` | 3 |
| `nested_trig_exp` | 3 |
| `one_over_sqrt_x2_plus_a2` | 3 |
| `poly2_exp` | 3 |
| `repeated_linear_square` | 3 |
| `sin_j_cos` | 3 |
| `sqrt_a2_plus_x2` | 3 |
| `tan_even_reduction` | 3 |
| `x2_over_sqrt_a2_minus_x2` | 3 |
| `arctan_alone` | 2 |
| `cos_j_sin` | 2 |
| `cyclic_exp_sin` | 2 |
| `differentials:reciprocal` | 2 |
| `direct_arctan` | 2 |
| `essential_tan_asymptote` | 2 |
| `inf_exp_ratio` | 2 |
| `lhopital_0_0_power` | 2 |
| `lhopital_0_inf_product` | 2 |
| `lhopital_inf_minus_inf` | 2 |
| `lhopital_multipass_trig` | 2 |
| `lhopital_poly_over_exp` | 2 |
| `ln_linear` | 2 |
| `poly1_cos` | 2 |
| `quotient_mixed_special` | 2 |
| `removable_quad_shared` | 2 |
| `sec_j_tan` | 2 |
| `sin_even_power` | 2 |
| `arcsin_scaled` | 1 |
| `basic_sec_tan` | 1 |
| `basic_sin_kx` | 1 |
| `basic_tan` | 1 |
| `cos_even_power` | 1 |
| `differentials:chain_exp` | 1 |
| `differentials:eval_dx` | 1 |
| `differentials:exp` | 1 |
| `differentials:product` | 1 |
| `direct_exp` | 1 |
| `direct_sin_pi_over` | 1 |
| `direct_spec` | 1 |
| `direct_sqrt` | 1 |
| `irreducible_quad_arctan` | 1 |
| `lhopital_0_0_trig` | 1 |
| `lhopital_0_inf_power` | 1 |
| `lhopital_multipass_exp` | 1 |
| `one_over_sqrt_x` | 1 |
| `poly1_exp` | 1 |
| `poly1_ln` | 1 |
| `poly2_sin` | 1 |
| `pow_5_2_a2_minus` | 1 |
| `pow_m3_2_a2_minus` | 1 |
| `pow_m3_2_a2_plus` | 1 |
| `product_sin_a_cos_b` | 1 |
| `squeeze_sin_over_x` | 1 |
| `tan_odd_alone` | 1 |
| `tan_odd_sec_any` | 1 |
| `tan_sec_sec_even` | 1 |
| `trig_product_chain` | 1 |

## Topics

- [Limits — direct evaluation](#direct) — `calc_limits_by_direct_evaluation`
- [Limits — removable discontinuities](#removable) — `calc_limits_at_removable_discontinuities`
- [Limits — jump discontinuities / kinks](#jump) — `calc_limits_at_jump_discontinuities_and_kinks`
- [Limits — essential discontinuities](#essential) — `calc_limits_at_essential_discontinuities`
- [Limits — at infinity](#infinity) — `calc_limits_at_infinity`
- [Continuity — classify](#continuity) — `calc_continuity_determining_and_classifying`
- [L'Hôpital's rule](#lhopital) — `calc_app_diff_lhopitals_rule`
- [Derivatives — power rule](#deriv_power) — `calc_diff_power_rule`
- [Derivatives — product rule](#deriv_product) — `calc_diff_product_rule`
- [Derivatives — quotient rule](#deriv_quotient) — `calc_diff_quotient_rule`
- [Derivatives — chain rule](#deriv_chain) — `calc_diff_chain_rule`
- [Derivatives — trigonometric](#deriv_trig) — `calc_diff_trigonometric`
- [Derivatives — ln / exp](#deriv_ln_exp) — `calc_diff_natural_logarithms_and_exponentials`
- [Derivatives — inverse trig](#deriv_invtrig) — `calc_diff_inverse_trigonometric`
- [Derivatives — higher order](#deriv_higher) — `calc_diff_higher_order_derivatives`
- [Derivatives — general](#deriv_general) — `calc_diff_general`
- [Linear approximations](#linear_approx) — `calc_app_diff_linear_approximations`
- [Differentials](#differentials) — `calc_app_diff_differentials`
- [Integrals — power rule](#int_power) — `calc_indef_int_power_rule`
- [Integrals — trigonometric](#int_trig) — `calc_indef_int_trigonometric`
- [Integrals — log / exp](#int_log_exp) — `calc_indef_int_logarithmic_rule_and_exponentials`
- [Integrals — inverse trig](#int_invtrig) — `calc_indef_int_inverse_trigonometric`
- [Integrals — substitution (power)](#int_sub) — `calc_indef_int_power_rule_with_substitution`
- [Integrals — log/exp with substitution](#int_log_exp_sub) — `calc_indef_int_logarithmic_rule_and_exponentials_with_substitution`
- [Integrals — trigonometric substitution](#int_trig_sub) — `calc_indef_int_trigonometric_with_substitution`
- [Integrals — invtrig with substitution](#int_invtrig_sub) — `calc_indef_int_inverse_trigonometric_with_substitution`
- [Integrals — integration by parts](#int_parts) — `calc_indef_int_integration_by_parts`
- [Integrals — partial fractions](#int_pfd) — `calc_indef_int_partial_fractions`
- [Integrals — multi-trick](#int_multi) — `calc_indef_int_multi_trick`
- [FTC — first](#ftc1) — `calc_def_int_first_fundamental_theorem_of_calculus`
- [FTC — second](#ftc2) — `calc_def_int_second_fundamental_theorem_of_calculus`
- [Definite — substitution / change of variables](#def_sub) — `calc_def_int_substitution_with_change_of_variables`

## Limits — direct evaluation

<a id="direct"></a>

`calc_limits_by_direct_evaluation` · pack `direct` · topic label: c1: By direct evaluation · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **10** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `rational_direct` | 6 |
| `direct_sin_shift` | 4 |
| `poly_direct` | 4 |
| `direct_ln` | 3 |
| `direct_arctan` | 2 |
| `direct_exp` | 1 |
| `direct_sin_pi_over` | 1 |
| `direct_spec` | 1 |
| `direct_sqrt` | 1 |
| `squeeze_sin_over_x` | 1 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\lim_{x \to 3} \left(4x^{2} + 6\right)$ | $42$ | `—` | `spec_pack=limit_direct · methods=direct_eval · form_id=poly_direct · costs[form:poly_direct=0 ⇒ 0] · D=0` |
| 0 | $\lim_{x \to -2} \left(x^{2} + 2x - 5\right)$ | $-5$ | `—` | `spec_pack=limit_direct · methods=direct_eval · form_id=poly_direct · costs[form:poly_direct=0 ⇒ 0] · D=0` |
| 0 | $\lim_{x \to -1} \left(3x - 6\right)$ | $-9$ | `—` | `spec_pack=limit_direct · methods=direct_eval · form_id=poly_direct · costs[form:poly_direct=0 ⇒ 0] · D=0` |
| 3 | $\lim_{x \to -3} \frac{4x^{2} + 6}{2x - 2}$ | $-\frac{21}{4}$ | `—` | `spec_pack=limit_direct · methods=direct_eval · form_id=rational_direct · costs[form:rational_direct=2 ⇒ 2] · D=3` |
| 3 | $\lim_{x \to -1} \frac{6x^{2} + 4x}{3x + 1}$ | $-1$ | `—` | `spec_pack=limit_direct · methods=direct_eval · form_id=rational_direct · costs[form:rational_direct=2 ⇒ 2] · D=3` |
| 3 | $\lim_{x \to 1} \frac{6x^{2} + 6x}{6x - 5}$ | $12$ | `—` | `spec_pack=limit_direct · methods=direct_eval · form_id=rational_direct · costs[form:rational_direct=2 ⇒ 2] · D=3` |
| 6 | $\lim_{x \to 0} -\arctan(x)$ | $0$ | `—` | `spec_pack=limit_direct · methods=direct_eval · form_id=direct_arctan · dress=[sign] · shape=expr_direct · costs[form:direct_arctan=6 + dress:spec_sign=0.5 + spec:allow_invtrig=2 ⇒ 8.5] · D=6` |
| 6 | $\lim_{x \to \pi} \frac{\sin(x)}{\tan(x)}$ | $-1$ | `—` | `spec_pack=limit_direct · methods=direct_eval · form_id=direct_sin_pi_over · shape=expr_direct · costs[form:direct_sin_pi_over=4 + spec:allow_trig=1.5 ⇒ 5.5] · D=6` |
| 6 | $\lim_{x \to 4} -\frac{-x + 6}{-5x - 1}$ | $\frac{2}{21}$ | `—` | `spec_pack=limit_direct · methods=direct_eval · form_id=direct_sin_shift · dress=[sign] · shape=rational_direct · costs[form:direct_sin_shift=4 + dress:spec_sign=0.5 ⇒ 4.5] · D=6` |
| 8 | $\lim_{x \to 1} -3\frac{-x^{3} - x}{4x + 2}$ | $1$ | `—` | `spec_pack=limit_direct · methods=direct_eval · form_id=rational_direct · dress=[constant_multiple] · costs[form:rational_direct=2 + dress:spec_scale=1.5 ⇒ 3.5] · D=8` |
| 8 | $\lim_{x \to 4} -\frac{-2x^{3} - 4}{-5x + 6}$ | $-\frac{66}{7}$ | `—` | `spec_pack=limit_direct · methods=direct_eval · form_id=rational_direct · dress=[sign] · costs[form:rational_direct=2 + dress:spec_sign=0.5 ⇒ 2.5] · D=8` |
| 8 | $\lim_{x \to -5} 4\frac{x^{3} - 2x}{4x + 1}$ | $\frac{460}{19}$ | `—` | `spec_pack=limit_direct · methods=direct_eval · form_id=rational_direct · dress=[constant_multiple] · costs[form:rational_direct=2 + dress:spec_scale=1.5 ⇒ 3.5] · D=8` |
| 12 | $\lim_{x \to 2} -\frac{3x^{2} + 5x}{-5x + 1}$ | $\frac{22}{9}$ | `—` | `spec_pack=limit_direct · methods=direct_eval · form_id=direct_sin_shift · dress=[sign] · shape=rational_direct · costs[form:direct_sin_shift=4 + dress:spec_sign=0.5 ⇒ 4.5] · D=12` |
| 12 | $\lim_{x \to -5} \left(\arctan(x)e^{5x - 6}\right)$ | $0$ | `—` | `spec_pack=limit_direct · methods=direct_eval · form_id=direct_ln · dress=[compose_inner,product_dress] · shape=expr_direct · costs[form:direct_ln=4 + dress:compose_inner=1 + dress:product_dress=1 + spec:allow_exp=1.5 + spec:allow_invtrig=2 ⇒ 9.5] · D=12` |
| 12 | $\lim_{x \to \frac{\pi}{4}} -\left(\sin\left(x-\frac{\pi}{4}\right)\right)$ | $0$ | `—` | `spec_pack=limit_direct · methods=direct_eval · form_id=direct_sin_shift · dress=[sign] · shape=expr_direct · costs[form:direct_sin_shift=4 + dress:spec_sign=0.5 + spec:allow_trig=1.5 ⇒ 6] · D=12` |
| 16 | $\lim_{x \to \frac{\pi}{6}} -4\sin(x)$ | $-2$ | `—` | `spec_pack=limit_direct · methods=direct_eval · form_id=direct_sin_shift · dress=[sign,constant_multiple] · shape=expr_direct · costs[form:direct_sin_shift=2 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:allow_trig=1.5 ⇒ 5.5] · D=16` |
| 16 | $\lim_{x \to -3} -\frac{7x^{3} + 2x^{2}}{7x - 1}$ | $-\frac{171}{22}$ | `—` | `spec_pack=limit_direct · methods=direct_eval · form_id=direct_arctan · dress=[sign] · shape=rational_direct · costs[form:direct_arctan=6 + dress:spec_sign=0.5 ⇒ 6.5] · D=16` |
| 16 | $\lim_{x \to 0} 4\left(\ln(x+1)\right)$ | $0$ | `—` | `spec_pack=limit_direct · methods=direct_eval · form_id=direct_ln · dress=[constant_multiple,sign] · shape=expr_direct · costs[form:direct_ln=4 + dress:spec_scale=1.5 + dress:spec_sign=0.5 + spec:allow_log=1.5 ⇒ 7.5] · D=16` |
| 20 | $\lim_{x \to -4} 4\frac{4x^{2} - 2}{7x - 8}$ | $-\frac{62}{9}$ | `—` | `spec_pack=limit_direct · methods=direct_eval · form_id=direct_sqrt · dress=[sign,constant_multiple] · shape=rational_direct · costs[form:direct_sqrt=6 + dress:spec_sign=0.5 + dress:spec_scale=1.5 ⇒ 8] · D=20` |
| 20 | $\lim_{x \to -5} 3\frac{8x^{3} + 4x}{-8x + 6}$ | $-\frac{1530}{23}$ | `—` | `spec_pack=limit_direct · methods=direct_eval · form_id=direct_ln · dress=[constant_multiple] · shape=rational_direct · costs[form:direct_ln=4 + dress:spec_scale=1.5 ⇒ 5.5] · D=20` |
| 20 | $\lim_{x \to 0} -4\frac{\sin(3x)}{x}$ | $-12$ | `—` | `spec_pack=limit_direct · methods=squeeze_trig · form_id=squeeze_sin_over_x · dress=[constant_multiple] · shape=trig_squeeze · costs[form:squeeze_sin_over_x=8 + dress:spec_scale=1.5 + spec:allow_trig=1.5 ⇒ 11] · D=20` |
| 25 | $\lim_{x \to -1} \left(\sqrt{4x + 4}\cos(8x)\right)$ | $0$ | `—` | `spec_pack=limit_direct · methods=direct_eval · form_id=direct_spec · dress=[product_dress,compose_inner,awkward_parens,affine_stretch] · shape=expr_direct · costs[form:direct_spec=2 + dress:product_dress=1 + dress:compose_inner=1 + dress:awkward_parens=1 + dress:affine_stretch=1 + spec:allow_roots=1 + spec:allow_trig=1.5 ⇒ 8.5] · D=25` |
| 25 | $\lim_{x \to -1} -\frac{-3x^{2} - 3x}{4x - 3}$ | $0$ | `—` | `spec_pack=limit_direct · methods=direct_eval · form_id=poly_direct · dress=[sign] · shape=rational_direct · costs[form:poly_direct=0 + dress:spec_sign=0.5 ⇒ 0.5] · D=25` |
| 25 | $\lim_{x \to 2} -\frac{-5x^{3} + 2}{-8x + 6}$ | $-\frac{19}{5}$ | `—` | `spec_pack=limit_direct · methods=direct_eval · form_id=direct_exp · dress=[sign] · shape=rational_direct · costs[form:direct_exp=4 + dress:spec_sign=0.5 ⇒ 4.5] · D=25` |

## Limits — removable discontinuities

<a id="removable"></a>

`calc_limits_at_removable_discontinuities` · pack `removable` · topic label: c1: At removable discontinuities · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **4** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `removable_rationalize` | 10 |
| `removable_diff_sq` | 6 |
| `removable_linear_factor` | 6 |
| `removable_quad_shared` | 2 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\lim_{x \to 5} \frac{x^{2}-25}{x-5}$ | $10$ | `—` | `spec_pack=limit_removable · methods=factor_cancel · form_id=removable_diff_sq · shape=removable_factor · costs[form:removable_diff_sq=3 ⇒ 3] · D=0` |
| 0 | $\lim_{x \to 1} \frac{x^{2}-1}{x-1}$ | $2$ | `—` | `spec_pack=limit_removable · methods=factor_cancel · form_id=removable_diff_sq · shape=removable_factor · costs[form:removable_diff_sq=3 ⇒ 3] · D=0` |
| 0 | $\lim_{x \to 3} \frac{x^{2}-9}{x-3}$ | $6$ | `—` | `spec_pack=limit_removable · methods=factor_cancel · form_id=removable_diff_sq · shape=removable_factor · costs[form:removable_diff_sq=3 ⇒ 3] · D=0` |
| 3 | $\lim_{x \to 4} \frac{x^{2} - 9x + 20}{x-4}$ | $-1$ | `—` | `spec_pack=limit_removable · methods=factor_cancel · form_id=removable_linear_factor · shape=removable_factor · costs[form:removable_linear_factor=3 ⇒ 3] · D=3` |
| 3 | $\lim_{x \to 5} \frac{x^{2} - 11x + 30}{x-5}$ | $-1$ | `—` | `spec_pack=limit_removable · methods=factor_cancel · form_id=removable_linear_factor · shape=removable_factor · costs[form:removable_linear_factor=3 ⇒ 3] · D=3` |
| 3 | $\lim_{x \to 4} \frac{x^{2} - 7x + 12}{x-4}$ | $1$ | `—` | `spec_pack=limit_removable · methods=factor_cancel · form_id=removable_linear_factor · shape=removable_factor · costs[form:removable_linear_factor=3 ⇒ 3] · D=3` |
| 6 | $\lim_{x \to 2} \frac{x^{2} - 8x + 12}{x-2}$ | $-4$ | `—` | `spec_pack=limit_removable · methods=factor_cancel · form_id=removable_linear_factor · shape=removable_factor · costs[form:removable_linear_factor=3 ⇒ 3] · D=6` |
| 6 | $\lim_{x \to 1} \frac{x^{2} + 2x - 3}{x-1}$ | $4$ | `—` | `spec_pack=limit_removable · methods=factor_cancel · form_id=removable_linear_factor · shape=removable_factor · costs[form:removable_linear_factor=3 ⇒ 3] · D=6` |
| 6 | $\lim_{x \to 5} \frac{x^{2}-25}{x-5}$ | $10$ | `—` | `spec_pack=limit_removable · methods=factor_cancel · form_id=removable_diff_sq · shape=removable_factor · costs[form:removable_diff_sq=3 ⇒ 3] · D=6` |
| 8 | $\lim_{x \to 4} \frac{\sqrt{x}-\sqrt{4}}{x-4}$ | $\frac{1}{2\sqrt{4}}$ | `—` | `spec_pack=limit_removable · methods=rationalize · form_id=removable_rationalize · costs[form:removable_rationalize=3 + spec:allow_roots=1 ⇒ 4] · D=8` |
| 8 | $\lim_{x \to 5} \frac{x^{3} + 6x^{2} - 25x - 150}{x-5}$ | $110$ | `—` | `spec_pack=limit_removable · methods=factor_cancel · form_id=removable_diff_sq · dress=[removable_extra_factor,removable_expand] · shape=removable_factor · costs[form:removable_diff_sq=3 + dress:removable_extra_factor=3 + dress:removable_expand=2 ⇒ 8] · D=8` |
| 8 | $\lim_{x \to 2} \frac{\sqrt{x}-\sqrt{2}}{x-2}$ | $\frac{1}{2\sqrt{2}}$ | `—` | `spec_pack=limit_removable · methods=rationalize · form_id=removable_rationalize · costs[form:removable_rationalize=8 + spec:allow_roots=1 ⇒ 9] · D=8` |
| 12 | $\lim_{x \to 2} \frac{\sqrt{x}-\sqrt{2}}{x-2}$ | $\frac{1}{2\sqrt{2}}$ | `—` | `spec_pack=limit_removable · methods=rationalize · form_id=removable_rationalize · costs[form:removable_rationalize=6 + spec:allow_roots=1 ⇒ 7] · D=12` |
| 12 | $\lim_{x \to 4} \frac{x^{2}-16}{x-4}$ | $8$ | `—` | `spec_pack=limit_removable · methods=factor_cancel · form_id=removable_diff_sq · shape=removable_factor · costs[form:removable_diff_sq=3 ⇒ 3] · D=12` |
| 12 | $\lim_{x \to 1} \frac{\sqrt{x}-\sqrt{1}}{x-1}$ | $\frac{1}{2\sqrt{1}}$ | `—` | `spec_pack=limit_removable · methods=rationalize · form_id=removable_rationalize · costs[form:removable_rationalize=8 + spec:allow_roots=1 ⇒ 9] · D=12` |
| 16 | $\lim_{x \to 2} \frac{x^{2} + 2x - 8}{x^{2} - 10x + 16}$ | $-1$ | `—` | `spec_pack=limit_removable · methods=factor_cancel · form_id=removable_linear_factor · dress=[removable_extra_factor,removable_expand] · shape=removable_factor · costs[form:removable_linear_factor=3 + dress:removable_extra_factor=3 + dress:removable_expand=2 ⇒ 8] · D=16` |
| 16 | $\lim_{x \to 2} \frac{\sqrt{x}-\sqrt{2}}{x-2}$ | $\frac{1}{2\sqrt{2}}$ | `—` | `spec_pack=limit_removable · methods=rationalize · form_id=removable_rationalize · costs[form:removable_rationalize=8 + spec:allow_roots=1 ⇒ 9] · D=16` |
| 16 | $\lim_{x \to 3} \frac{\sqrt{x}-\sqrt{3}}{x-3}$ | $\frac{1}{2\sqrt{3}}$ | `—` | `spec_pack=limit_removable · methods=rationalize · form_id=removable_rationalize · costs[form:removable_rationalize=3 + spec:allow_roots=1 ⇒ 4] · D=16` |
| 20 | $\lim_{x \to 4} \frac{\sqrt{x}-\sqrt{4}}{x-4}$ | $\frac{1}{2\sqrt{4}}$ | `—` | `spec_pack=limit_removable · methods=rationalize · form_id=removable_rationalize · costs[form:removable_rationalize=3 + spec:allow_roots=1 ⇒ 4] · D=20` |
| 20 | $\lim_{x \to 2} \frac{\sqrt{x}-\sqrt{2}}{x-2}$ | $\frac{1}{2\sqrt{2}}$ | `—` | `spec_pack=limit_removable · methods=rationalize · form_id=removable_rationalize · costs[form:removable_rationalize=3 + spec:allow_roots=1 ⇒ 4] · D=20` |
| 20 | $\lim_{x \to 2} \frac{x^{2} - 8x + 12}{x-2}$ | $-4$ | `—` | `spec_pack=limit_removable · methods=factor_cancel · form_id=removable_quad_shared · shape=removable_factor · costs[form:removable_quad_shared=6 ⇒ 6] · D=20` |
| 25 | $\lim_{x \to 3} \frac{x^{2} - 6x + 9}{x-3}$ | $0$ | `—` | `spec_pack=limit_removable · methods=factor_cancel · form_id=removable_quad_shared · shape=removable_factor · costs[form:removable_quad_shared=6 ⇒ 6] · D=25` |
| 25 | $\lim_{x \to 4} \frac{\sqrt{x}-\sqrt{4}}{x-4}$ | $\frac{1}{2\sqrt{4}}$ | `—` | `spec_pack=limit_removable · methods=rationalize · form_id=removable_rationalize · costs[form:removable_rationalize=8 + spec:allow_roots=1 ⇒ 9] · D=25` |
| 25 | $\lim_{x \to 3} \frac{\sqrt{x}-\sqrt{3}}{x-3}$ | $\frac{1}{2\sqrt{3}}$ | `—` | `spec_pack=limit_removable · methods=rationalize · form_id=removable_rationalize · costs[form:removable_rationalize=8 + spec:allow_roots=1 ⇒ 9] · D=25` |

## Limits — jump discontinuities / kinks

<a id="jump"></a>

`calc_limits_at_jump_discontinuities_and_kinks` · pack `jump` · topic label: c1: At jump discontinuities and kinks · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **3** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `piecewise_jump_poly` | 13 |
| `piecewise_jump` | 6 |
| `piecewise_jump_linear` | 5 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\lim_{x \to -5} f(x)\text{ where }f(x)=\begin{cases}1&x<-5\\0&x\ge -5\end{cases}$ | $\text{DNE}$ | `—` | `spec_pack=limit_jump · methods=two_sided_compare · form_id=piecewise_jump · costs[form:piecewise_jump=0 ⇒ 0] · D=0` |
| 0 | $\lim_{x \to 3} f(x)\text{ where }f(x)=\begin{cases}-2&x<3\\-3&x\ge 3\end{cases}$ | $\text{DNE}$ | `—` | `spec_pack=limit_jump · methods=two_sided_compare · form_id=piecewise_jump · costs[form:piecewise_jump=0 ⇒ 0] · D=0` |
| 0 | $\lim_{x \to -3} f(x)\text{ where }f(x)=\begin{cases}-1&x<-3\\5&x\ge -3\end{cases}$ | $\text{DNE}$ | `—` | `spec_pack=limit_jump · methods=two_sided_compare · form_id=piecewise_jump · costs[form:piecewise_jump=0 ⇒ 0] · D=0` |
| 3 | $\lim_{x \to 3} f(x)\text{ where }f(x)=\begin{cases}4&x<3\\-3&x\ge 3\end{cases}$ | $\text{DNE}$ | `—` | `spec_pack=limit_jump · methods=two_sided_compare · form_id=piecewise_jump · costs[form:piecewise_jump=0 ⇒ 0] · D=3` |
| 3 | $\lim_{x \to -4} f(x)\text{ where }f(x)=\begin{cases}-3&x<-4\\0&x\ge -4\end{cases}$ | $\text{DNE}$ | `—` | `spec_pack=limit_jump · methods=two_sided_compare · form_id=piecewise_jump · costs[form:piecewise_jump=0 ⇒ 0] · D=3` |
| 3 | $\lim_{x \to -5^{+}} f(x)\text{ where }f(x)=\begin{cases}-3&x<-5\\2&x\ge -5\end{cases}$ | $2$ | `—` | `spec_pack=limit_jump · methods=one_sided · form_id=piecewise_jump · costs[form:piecewise_jump=0 ⇒ 0] · D=3` |
| 6 | $\lim_{x \to -2^{+}} f(x)\text{ where }f(x)=\begin{cases}-5x - 2&x<-2\\-4x - 1&x\ge -2\end{cases}$ | $7$ | `—` | `spec_pack=limit_jump · methods=one_sided · form_id=piecewise_jump_linear · shape=piecewise_jump · costs[form:piecewise_jump_linear=6 ⇒ 6] · D=6` |
| 6 | $\lim_{x \to 2} f(x)\text{ where }f(x)=\begin{cases}5x + 1&x<2\\-x&x\ge 2\end{cases}$ | $\text{DNE}$ | `—` | `spec_pack=limit_jump · methods=two_sided_compare · form_id=piecewise_jump_linear · shape=piecewise_jump · costs[form:piecewise_jump_linear=6 ⇒ 6] · D=6` |
| 6 | $\lim_{x \to 2} f(x)\text{ where }f(x)=\begin{cases}-2x + 3&x<2\\2&x\ge 2\end{cases}$ | $\text{DNE}$ | `—` | `spec_pack=limit_jump · methods=two_sided_compare · form_id=piecewise_jump_linear · shape=piecewise_jump · costs[form:piecewise_jump_linear=6 ⇒ 6] · D=6` |
| 8 | $\lim_{x \to 2^{-}} f(x)\text{ where }f(x)=\begin{cases}-5x + 4&x<2\\-x + 5&x\ge 2\end{cases}$ | $-6$ | `—` | `spec_pack=limit_jump · methods=one_sided · form_id=piecewise_jump_linear · shape=piecewise_jump · costs[form:piecewise_jump_linear=6 ⇒ 6] · D=8` |
| 8 | $\lim_{x \to 0^{-}} f(x)\text{ where }f(x)=\begin{cases}5x + 1&x<0\\-4x + 5&x\ge 0\end{cases}$ | $1$ | `—` | `spec_pack=limit_jump · methods=one_sided · form_id=piecewise_jump_linear · shape=piecewise_jump · costs[form:piecewise_jump_linear=6 ⇒ 6] · D=8` |
| 8 | $\lim_{x \to 3} f(x)\text{ where }f(x)=\begin{cases}2x^{2} + 3&x<3\\-2x - 1&x\ge 3\end{cases}$ | $\text{DNE}$ | `—` | `spec_pack=limit_jump · methods=two_sided_compare · form_id=piecewise_jump_poly · shape=piecewise_jump · costs[form:piecewise_jump_poly=10 ⇒ 10] · D=8` |
| 12 | $\lim_{x \to 1^{+}} f(x)\text{ where }f(x)=\begin{cases}\left(-6x + 3\right)\left(5x\right)&x<1\\-18&x=1\\\left(-4x - 5\right)\left(3x - 2\right)&x>1\end{cases}$ | $-9$ | `—` | `spec_pack=limit_jump · methods=one_sided · form_id=piecewise_jump_poly · dress=[jump_side_factored,jump_side_factored#2,jump_three_piece,jump_point_value] · shape=piecewise_jump · costs[form:piecewise_jump_poly=10 + dress:jump_side_factored=2.5 + dress:jump_side_factored#2=2.5 + dress:jump_three_piece=4 + dress:jump_point_value=1.5 ⇒ 20.5] · D=12` |
| 12 | $\lim_{x \to -1} f(x)\text{ where }f(x)=\begin{cases}-5x^{2} + 3x - 2&x<-1\\-10&x=-1\\-5x^{2} + 4x - 4&x>-1\end{cases}$ | $\text{DNE}$ | `—` | `spec_pack=limit_jump · methods=two_sided_compare · form_id=piecewise_jump_poly · dress=[jump_three_piece,jump_point_value] · shape=piecewise_jump · costs[form:piecewise_jump_poly=10 + dress:jump_three_piece=4 + dress:jump_point_value=1.5 ⇒ 15.5] · D=12` |
| 12 | $\lim_{x \to -3^{+}} f(x)\text{ where }f(x)=\begin{cases}\left(5x - 6\right)\left(3x + 2\right)&x<-3\\141&x=-3\\\left(-2x - 1\right)\left(3x + 3\right)&x>-3\end{cases}$ | $-30$ | `—` | `spec_pack=limit_jump · methods=one_sided · form_id=piecewise_jump_poly · dress=[jump_side_factored,jump_side_factored#2,jump_three_piece,jump_point_value] · shape=piecewise_jump · costs[form:piecewise_jump_poly=10 + dress:jump_side_factored=2.5 + dress:jump_side_factored#2=2.5 + dress:jump_three_piece=4 + dress:jump_point_value=1.5 ⇒ 20.5] · D=12` |
| 16 | $\lim_{x \to 5^{-}} f(x)\text{ where }f(x)=\begin{cases}\left(6x + 6\right)\left(x + 5\right)&x<5\\359&x=5\\-2x^{2} - x + 2&x>5\end{cases}$ | $360$ | `—` | `spec_pack=limit_jump · methods=one_sided · form_id=piecewise_jump_poly · dress=[jump_side_factored,jump_three_piece,jump_point_value] · shape=piecewise_jump · costs[form:piecewise_jump_poly=10 + dress:jump_side_factored=2.5 + dress:jump_three_piece=4 + dress:jump_point_value=1.5 ⇒ 18] · D=16` |
| 16 | $\lim_{x \to -2} f(x)\text{ where }f(x)=\begin{cases}\left(3x - 1\right)\left(3x - 4\right)&x<-2\\70&x=-2\\-4x^{2} - 4x + 3&x>-2\end{cases}$ | $\text{DNE}$ | `—` | `spec_pack=limit_jump · methods=two_sided_compare · form_id=piecewise_jump_poly · dress=[jump_side_factored,jump_three_piece,jump_point_value] · shape=piecewise_jump · costs[form:piecewise_jump_poly=10 + dress:jump_side_factored=2.5 + dress:jump_three_piece=4 + dress:jump_point_value=1.5 ⇒ 18] · D=16` |
| 16 | $\lim_{x \to 2^{+}} f(x)\text{ where }f(x)=\begin{cases}-x^{3} - 4x + 3&x<2\\-20&x=2\\\left(-6x + 7\right)\left(-2x - 3\right)&x>2\end{cases}$ | $35$ | `—` | `spec_pack=limit_jump · methods=one_sided · form_id=piecewise_jump_poly · dress=[jump_side_cubic,jump_side_factored,jump_three_piece,jump_point_value] · shape=piecewise_jump · costs[form:piecewise_jump_poly=10 + dress:jump_side_cubic=4 + dress:jump_side_factored=2.5 + dress:jump_three_piece=4 + dress:jump_point_value=1.5 ⇒ 22] · D=16` |
| 20 | $\lim_{x \to 4^{+}} f(x)\text{ where }f(x)=\begin{cases}\left(3x + 7\right)\left(8x + 2\right)&x<4\\654&x=4\\5x^{2} - x - 4&x>4\end{cases}$ | $72$ | `—` | `spec_pack=limit_jump · methods=one_sided · form_id=piecewise_jump_poly · dress=[jump_side_factored,jump_three_piece,jump_point_value] · shape=piecewise_jump · costs[form:piecewise_jump_poly=10 + dress:jump_side_factored=2.5 + dress:jump_three_piece=4 + dress:jump_point_value=1.5 ⇒ 18] · D=20` |
| 20 | $\lim_{x \to -4} f(x)\text{ where }f(x)=\begin{cases}\left(-7x - 8\right)\left(-3x + 7\right)&x<-4\\387&x=-4\\\left(-2x - 4\right)\left(6x + 2\right)&x>-4\end{cases}$ | $\text{DNE}$ | `—` | `spec_pack=limit_jump · methods=two_sided_compare · form_id=piecewise_jump_poly · dress=[jump_side_factored,jump_side_factored#2,jump_three_piece,jump_point_value] · shape=piecewise_jump · costs[form:piecewise_jump_poly=10 + dress:jump_side_factored=2.5 + dress:jump_side_factored#2=2.5 + dress:jump_three_piece=4 + dress:jump_point_value=1.5 ⇒ 20.5] · D=20` |
| 20 | $\lim_{x \to 3} f(x)\text{ where }f(x)=\begin{cases}\left(-7x - 8\right)\left(-8x - 4\right)&x<3\\813&x=3\\\left(8x - 3\right)\left(x - 8\right)&x>3\end{cases}$ | $\text{DNE}$ | `—` | `spec_pack=limit_jump · methods=two_sided_compare · form_id=piecewise_jump_poly · dress=[jump_side_factored,jump_side_factored#2,jump_three_piece,jump_point_value] · shape=piecewise_jump · costs[form:piecewise_jump_poly=10 + dress:jump_side_factored=2.5 + dress:jump_side_factored#2=2.5 + dress:jump_three_piece=4 + dress:jump_point_value=1.5 ⇒ 20.5] · D=20` |
| 25 | $\lim_{x \to -1^{+}} f(x)\text{ where }f(x)=\begin{cases}\left(-9x + 5\right)\left(-5x - 2\right)&x<-1\\45&x=-1\\\left(-x + 9\right)\left(-8x - 6\right)&x>-1\end{cases}$ | $20$ | `—` | `spec_pack=limit_jump · methods=one_sided · form_id=piecewise_jump_poly · dress=[jump_side_factored,jump_side_factored#2,jump_three_piece,jump_point_value] · shape=piecewise_jump · costs[form:piecewise_jump_poly=10 + dress:jump_side_factored=2.5 + dress:jump_side_factored#2=2.5 + dress:jump_three_piece=4 + dress:jump_point_value=1.5 ⇒ 20.5] · D=25` |
| 25 | $\lim_{x \to -3} f(x)\text{ where }f(x)=\begin{cases}5x^{3} + x^{2} + x - 1&x<-3\\-129&x=-3\\4x^{3} - x^{2} + 2x - 2&x>-3\end{cases}$ | $\text{DNE}$ | `—` | `spec_pack=limit_jump · methods=two_sided_compare · form_id=piecewise_jump_poly · dress=[jump_side_cubic,jump_side_cubic#2,jump_three_piece,jump_point_value] · shape=piecewise_jump · costs[form:piecewise_jump_poly=10 + dress:jump_side_cubic=4 + dress:jump_side_cubic#2=4 + dress:jump_three_piece=4 + dress:jump_point_value=1.5 ⇒ 23.5] · D=25` |
| 25 | $\lim_{x \to 0} f(x)\text{ where }f(x)=\begin{cases}2x^{3} - x^{2} - x + 4&x<0\\4&x=0\\\left(-8x - 8\right)\left(2x\right)&x>0\end{cases}$ | $\text{DNE}$ | `—` | `spec_pack=limit_jump · methods=two_sided_compare · form_id=piecewise_jump_poly · dress=[jump_side_cubic,jump_side_factored,jump_three_piece,jump_point_value] · shape=piecewise_jump · costs[form:piecewise_jump_poly=10 + dress:jump_side_cubic=4 + dress:jump_side_factored=2.5 + dress:jump_three_piece=4 + dress:jump_point_value=1.5 ⇒ 22] · D=25` |

## Limits — essential discontinuities

<a id="essential"></a>

`calc_limits_at_essential_discontinuities` · pack `essential` · topic label: c1: At essential discontinuities · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **6** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `essential_1_over_x` | 7 |
| `essential_rational_va` | 5 |
| `essential_cos_1_over_x` | 4 |
| `essential_1_over_x_sq` | 3 |
| `essential_sin_1_over_x` | 3 |
| `essential_tan_asymptote` | 2 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\lim_{x \to 0^{-}} \frac{1}{x}$ | $-\infty$ | `—` | `spec_pack=limit_essential · methods=essential_dne · form_id=essential_1_over_x · shape=essential · costs[form:essential_1_over_x=3 ⇒ 3] · D=0` |
| 0 | $\lim_{x \to 0^{+}} \frac{1}{x}$ | $\infty$ | `—` | `spec_pack=limit_essential · methods=essential_dne · form_id=essential_1_over_x · shape=essential · costs[form:essential_1_over_x=3 ⇒ 3] · D=0` |
| 0 | $\lim_{x \to 0} \frac{1}{x}$ | $\text{DNE}$ | `—` | `spec_pack=limit_essential · methods=essential_dne · form_id=essential_1_over_x · shape=essential · costs[form:essential_1_over_x=3 ⇒ 3] · D=0` |
| 3 | $\lim_{x \to 0} \frac{1}{x^{2}}$ | $\infty$ | `—` | `spec_pack=limit_essential · methods=essential_dne · form_id=essential_1_over_x_sq · shape=essential · costs[form:essential_1_over_x_sq=4 ⇒ 4] · D=3` |
| 3 | $\lim_{x \to 0} \frac{1}{x^{2}}$ | $\infty$ | `—` | `spec_pack=limit_essential · methods=essential_dne · form_id=essential_1_over_x_sq · shape=essential · costs[form:essential_1_over_x_sq=4 ⇒ 4] · D=3` |
| 3 | $\lim_{x \to 0} \frac{1}{x}$ | $\text{DNE}$ | `—` | `spec_pack=limit_essential · methods=essential_dne · form_id=essential_1_over_x · shape=essential · costs[form:essential_1_over_x=3 ⇒ 3] · D=3` |
| 6 | $\lim_{x \to 0} \sin\left(\frac{1}{x}\right)$ | $\text{DNE}$ | `—` | `spec_pack=limit_essential · methods=essential_dne · form_id=essential_sin_1_over_x · shape=essential · costs[form:essential_sin_1_over_x=6 + spec:allow_trig=1.5 ⇒ 7.5] · D=6` |
| 6 | $\lim_{x \to 1^{+}} \frac{2}{(x-1)^{3}}$ | $\infty$ | `—` | `spec_pack=limit_essential · methods=essential_dne · form_id=essential_rational_va · shape=essential · costs[form:essential_rational_va=4 ⇒ 4] · D=6` |
| 6 | $\lim_{x \to 3} \cos\left(\frac{1}{(x-3)}\right)$ | $\text{DNE}$ | `—` | `spec_pack=limit_essential · methods=essential_dne · form_id=essential_cos_1_over_x · dress=[horizontal_shift] · shape=essential · costs[form:essential_cos_1_over_x=6 + dress:horizontal_shift=2 + spec:allow_trig=1.5 ⇒ 9.5] · D=6` |
| 8 | $\lim_{x \to 4} \frac{2}{(x-4)}$ | $\text{DNE}$ | `—` | `spec_pack=limit_essential · methods=essential_dne · form_id=essential_rational_va · dress=[horizontal_shift] · shape=essential · costs[form:essential_rational_va=4 + dress:horizontal_shift=2 ⇒ 6] · D=8` |
| 8 | $\lim_{x \to 0} \frac{x}{x^{2}}$ | $\text{DNE}$ | `—` | `spec_pack=limit_essential · methods=essential_dne · form_id=essential_1_over_x · dress=[unfactored_form] · shape=essential · costs[form:essential_1_over_x=3 + dress:unfactored_form=1.5 ⇒ 4.5] · D=8` |
| 8 | $\lim_{x \to -5} \sin\left(\frac{1}{(x+5)}\right)$ | $\text{DNE}$ | `—` | `spec_pack=limit_essential · methods=essential_dne · form_id=essential_sin_1_over_x · dress=[horizontal_shift] · shape=essential · costs[form:essential_sin_1_over_x=6 + dress:horizontal_shift=2 + spec:allow_trig=1.5 ⇒ 9.5] · D=8` |
| 12 | $\lim_{x \to 0} -\cos\left(\frac{1}{x}\right)$ | $\text{DNE}$ | `—` | `spec_pack=limit_essential · methods=essential_dne · form_id=essential_cos_1_over_x · dress=[sign] · shape=essential · costs[form:essential_cos_1_over_x=6 + dress:spec_sign=0.5 + spec:allow_trig=1.5 ⇒ 8] · D=12` |
| 12 | $\lim_{x \to -3} \frac{3}{(x+3)}$ | $\text{DNE}$ | `—` | `spec_pack=limit_essential · methods=essential_dne · form_id=essential_rational_va · dress=[constant_multiple] · shape=essential · costs[form:essential_rational_va=4 + dress:spec_scale=1.5 ⇒ 5.5] · D=12` |
| 12 | $\lim_{x \to 0} \frac{1}{x}$ | $\text{DNE}$ | `—` | `spec_pack=limit_essential · methods=essential_dne · form_id=essential_1_over_x · shape=essential · costs[form:essential_1_over_x=3 ⇒ 3] · D=12` |
| 16 | $\lim_{x \to -1} \frac{1}{(x+1)^{2}}$ | $\infty$ | `—` | `spec_pack=limit_essential · methods=essential_dne · form_id=essential_1_over_x_sq · dress=[horizontal_shift] · shape=essential · costs[form:essential_1_over_x_sq=4 + dress:horizontal_shift=2 ⇒ 6] · D=16` |
| 16 | $\lim_{x \to 5} \frac{1}{(x-5)}$ | $\text{DNE}$ | `—` | `spec_pack=limit_essential · methods=essential_dne · form_id=essential_rational_va · dress=[horizontal_shift] · shape=essential · costs[form:essential_rational_va=4 + dress:horizontal_shift=2 ⇒ 6] · D=16` |
| 16 | $\lim_{x \to -4} \cos\left(\frac{1}{(x+4)}\right)$ | $\text{DNE}$ | `—` | `spec_pack=limit_essential · methods=essential_dne · form_id=essential_cos_1_over_x · dress=[horizontal_shift] · shape=essential · costs[form:essential_cos_1_over_x=6 + dress:horizontal_shift=2 + spec:allow_trig=1.5 ⇒ 9.5] · D=16` |
| 20 | $\lim_{x \to 4} -\cos\left(\frac{1}{(x-4)}\right)$ | $\text{DNE}$ | `—` | `spec_pack=limit_essential · methods=essential_dne · form_id=essential_cos_1_over_x · dress=[horizontal_shift,sign] · shape=essential · costs[form:essential_cos_1_over_x=6 + dress:horizontal_shift=2 + dress:spec_sign=0.5 + spec:allow_trig=1.5 ⇒ 10] · D=20` |
| 20 | $\lim_{x \to -3} \frac{-2}{(x+3)^{2}}$ | $-\infty$ | `—` | `spec_pack=limit_essential · methods=essential_dne · form_id=essential_rational_va · dress=[constant_multiple] · shape=essential · costs[form:essential_rational_va=4 + dress:spec_scale=1.5 ⇒ 5.5] · D=20` |
| 20 | $\lim_{x \to \frac{\pi}{2}} -\tan(x)$ | $\text{DNE}$ | `—` | `spec_pack=limit_essential · methods=essential_dne · form_id=essential_tan_asymptote · dress=[sign] · shape=essential · costs[form:essential_tan_asymptote=8 + dress:spec_sign=0.5 + spec:allow_trig=1.5 ⇒ 10] · D=20` |
| 25 | $\lim_{x \to 0} \frac{x}{x^{2}}$ | $\text{DNE}$ | `—` | `spec_pack=limit_essential · methods=essential_dne · form_id=essential_1_over_x · dress=[unfactored_form] · shape=essential · costs[form:essential_1_over_x=3 + dress:unfactored_form=1.5 ⇒ 4.5] · D=25` |
| 25 | $\lim_{x \to 5} \sin\left(\frac{1}{(x-5)}\right)$ | $\text{DNE}$ | `—` | `spec_pack=limit_essential · methods=essential_dne · form_id=essential_sin_1_over_x · dress=[horizontal_shift] · shape=essential · costs[form:essential_sin_1_over_x=6 + dress:horizontal_shift=2 + spec:allow_trig=1.5 ⇒ 9.5] · D=25` |
| 25 | $\lim_{x \to \frac{\pi}{2}} -\tan(x)$ | $\text{DNE}$ | `—` | `spec_pack=limit_essential · methods=essential_dne · form_id=essential_tan_asymptote · dress=[sign] · shape=essential · costs[form:essential_tan_asymptote=8 + dress:spec_sign=0.5 + spec:allow_trig=1.5 ⇒ 10] · D=25` |

## Limits — at infinity

<a id="infinity"></a>

`calc_limits_at_infinity` · pack `infinity` · topic label: c1: At infinity · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **5** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `inf_rational` | 11 |
| `inf_arctan` | 4 |
| `inf_sin_over_x` | 4 |
| `inf_ln_over_poly` | 3 |
| `inf_exp_ratio` | 2 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\lim_{x \to \infty} \frac{-2x - 2}{3}$ | $-\infty$ | `—` | `spec_pack=limit_infinity · methods=compare_degrees · form_id=inf_rational · shape=rational_inf · costs[form:inf_rational=5 ⇒ 5] · D=0` |
| 0 | $\lim_{x \to \infty} \frac{-5x^{2} - 3}{2x}$ | $-\infty$ | `—` | `spec_pack=limit_infinity · methods=compare_degrees · form_id=inf_rational · shape=rational_inf · costs[form:inf_rational=5 ⇒ 5] · D=0` |
| 0 | $\lim_{x \to -\infty} \frac{-2x - 5}{5x}$ | $-\frac{2}{5}$ | `—` | `spec_pack=limit_infinity · methods=compare_degrees · form_id=inf_rational · shape=rational_inf · costs[form:inf_rational=5 ⇒ 5] · D=0` |
| 3 | $\lim_{x \to -\infty} \frac{-5x - 1}{3}$ | $\infty$ | `—` | `spec_pack=limit_infinity · methods=compare_degrees · form_id=inf_rational · shape=rational_inf · costs[form:inf_rational=5 ⇒ 5] · D=3` |
| 3 | $\lim_{x \to -\infty} \frac{-6x - 3}{x}$ | $-6$ | `—` | `spec_pack=limit_infinity · methods=compare_degrees · form_id=inf_rational · shape=rational_inf · costs[form:inf_rational=5 ⇒ 5] · D=3` |
| 3 | $\lim_{x \to -\infty} \frac{-3x - 3}{5}$ | $\infty$ | `—` | `spec_pack=limit_infinity · methods=compare_degrees · form_id=inf_rational · shape=rational_inf · costs[form:inf_rational=5 ⇒ 5] · D=3` |
| 6 | $\lim_{x \to \infty} \frac{\sin(x)}{x}$ | $0$ | `—` | `spec_pack=limit_infinity · methods=end_behavior · form_id=inf_sin_over_x · shape=trig_inf · costs[form:inf_sin_over_x=6 + spec:allow_trig=1.5 ⇒ 7.5] · D=6` |
| 6 | $\lim_{x \to \infty} \frac{\cos(x)}{x^{3}}$ | $0$ | `—` | `spec_pack=limit_infinity · methods=end_behavior · form_id=inf_sin_over_x · shape=trig_inf · costs[form:inf_sin_over_x=6 + spec:allow_trig=1.5 ⇒ 7.5] · D=6` |
| 6 | $\lim_{x \to -\infty} -\frac{5x^{4} + 4x^{2}}{3}$ | $-\infty$ | `—` | `spec_pack=limit_infinity · methods=compare_degrees · form_id=inf_rational · dress=[sign] · shape=rational_inf · costs[form:inf_rational=5 + dress:spec_sign=0.5 ⇒ 5.5] · D=6` |
| 8 | $\lim_{x \to -\infty} -\frac{-5x^{4} - 5x^{2}}{6x}$ | $\infty$ | `—` | `spec_pack=limit_infinity · methods=compare_degrees · form_id=inf_rational · dress=[sign] · shape=rational_inf · costs[form:inf_rational=5 + dress:spec_sign=0.5 ⇒ 5.5] · D=8` |
| 8 | $\lim_{x \to -\infty} 4\frac{3x^{4} + 6x^{3}}{2}$ | $\infty$ | `—` | `spec_pack=limit_infinity · methods=compare_degrees · form_id=inf_rational · dress=[constant_multiple] · shape=rational_inf · costs[form:inf_rational=5 + dress:spec_scale=1.5 ⇒ 6.5] · D=8` |
| 8 | $\lim_{x \to \infty} -\frac{\ln(x)}{x^{1}}$ | $0$ | `—` | `spec_pack=limit_infinity · methods=end_behavior · form_id=inf_ln_over_poly · dress=[sign] · shape=log_inf · costs[form:inf_ln_over_poly=8 + dress:spec_sign=0.5 + spec:allow_log=1.5 ⇒ 10] · D=8` |
| 12 | $\lim_{x \to \infty} -\arctan(x)$ | $-\frac{\pi}{2}$ | `—` | `spec_pack=limit_infinity · methods=end_behavior · form_id=inf_arctan · dress=[sign] · shape=invtrig_inf · costs[form:inf_arctan=6 + dress:spec_sign=0.5 + spec:allow_invtrig=2 ⇒ 8.5] · D=12` |
| 12 | $\lim_{x \to -\infty} -\frac{-x^{5} + x}{4x}$ | $-\infty$ | `—` | `spec_pack=limit_infinity · methods=compare_degrees · form_id=inf_rational · dress=[sign] · shape=rational_inf · costs[form:inf_rational=5 + dress:spec_sign=0.5 ⇒ 5.5] · D=12` |
| 12 | $\lim_{x \to \infty} -3\frac{2+2e^{x}}{3+3e^{x}}$ | $-2$ | `—` | `spec_pack=limit_infinity · methods=end_behavior · form_id=inf_exp_ratio · dress=[constant_multiple] · shape=exp_inf · costs[form:inf_exp_ratio=8 + dress:spec_scale=1.5 + spec:allow_exp=1.5 ⇒ 11] · D=12` |
| 16 | $\lim_{x \to \infty} -\arctan(x)$ | $-\frac{\pi}{2}$ | `—` | `spec_pack=limit_infinity · methods=end_behavior · form_id=inf_arctan · dress=[sign] · shape=invtrig_inf · costs[form:inf_arctan=6 + dress:spec_sign=0.5 + spec:allow_invtrig=2 ⇒ 8.5] · D=16` |
| 16 | $\lim_{x \to \infty} -2\frac{\ln(x)}{x^{2}}$ | $0$ | `—` | `spec_pack=limit_infinity · methods=end_behavior · form_id=inf_ln_over_poly · dress=[constant_multiple,sign] · shape=log_inf · costs[form:inf_ln_over_poly=8 + dress:spec_scale=1.5 + dress:spec_sign=0.5 + spec:allow_log=1.5 ⇒ 11.5] · D=16` |
| 16 | $\lim_{x \to -\infty} -\frac{\cos(x)}{x^{1}}$ | $0$ | `—` | `spec_pack=limit_infinity · methods=end_behavior · form_id=inf_sin_over_x · dress=[sign] · shape=trig_inf · costs[form:inf_sin_over_x=6 + dress:spec_sign=0.5 + spec:allow_trig=1.5 ⇒ 8] · D=16` |
| 20 | $\lim_{x \to -\infty} -\frac{\cos(x)}{x^{3}}$ | $0$ | `—` | `spec_pack=limit_infinity · methods=end_behavior · form_id=inf_sin_over_x · dress=[sign] · shape=trig_inf · costs[form:inf_sin_over_x=6 + dress:spec_sign=0.5 + spec:allow_trig=1.5 ⇒ 8] · D=20` |
| 20 | $\lim_{x \to \infty} 2\frac{-8x^{2} + 2}{8x}$ | $-\infty$ | `—` | `spec_pack=limit_infinity · methods=compare_degrees · form_id=inf_rational · dress=[constant_multiple] · shape=rational_inf · costs[form:inf_rational=5 + dress:spec_scale=1.5 ⇒ 6.5] · D=20` |
| 20 | $\lim_{x \to \infty} -4\arctan(x)$ | $-4\frac{\pi}{2}$ | `—` | `spec_pack=limit_infinity · methods=end_behavior · form_id=inf_arctan · dress=[sign,constant_multiple] · shape=invtrig_inf · costs[form:inf_arctan=6 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:allow_invtrig=2 ⇒ 10] · D=20` |
| 25 | $\lim_{x \to -\infty} -4\arctan(x)$ | $4\frac{\pi}{2}$ | `—` | `spec_pack=limit_infinity · methods=end_behavior · form_id=inf_arctan · dress=[sign,constant_multiple] · shape=invtrig_inf · costs[form:inf_arctan=6 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:allow_invtrig=2 ⇒ 10] · D=25` |
| 25 | $\lim_{x \to \infty} -4\frac{\ln(x)}{x^{3}}$ | $0$ | `—` | `spec_pack=limit_infinity · methods=end_behavior · form_id=inf_ln_over_poly · dress=[constant_multiple] · shape=log_inf · costs[form:inf_ln_over_poly=8 + dress:spec_scale=1.5 + spec:allow_log=1.5 ⇒ 11] · D=25` |
| 25 | $\lim_{x \to -\infty} -3\frac{e^{x}}{x^{3}}$ | $0$ | `—` | `spec_pack=limit_infinity · methods=end_behavior · form_id=inf_exp_ratio · dress=[constant_multiple,sign] · shape=exp_inf · costs[form:inf_exp_ratio=8 + dress:spec_scale=1.5 + dress:spec_sign=0.5 + spec:allow_exp=1.5 ⇒ 11.5] · D=25` |

## Continuity — classify

<a id="continuity"></a>

`calc_continuity_determining_and_classifying` · pack `continuity` · topic label: c1: Determining and classifying · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **7** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `continuity_poly` | 7 |
| `removable_linear_factor` | 6 |
| `continuity_linear` | 3 |
| `piecewise_jump` | 3 |
| `piecewise_jump_poly` | 2 |
| `removable_diff_sq` | 2 |
| `piecewise_jump_linear` | 1 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\text{Classify the continuity of }f(x)=\begin{cases}-5&x<-3\\-4&x\ge -3\end{cases}\text{ at }x=-3.$ | $\text{jump discontinuity}$ | `—` | `spec_pack=limit_continuity · methods=classify_jump · form_id=piecewise_jump · costs[form:piecewise_jump=0 ⇒ 0] · D=0` |
| 0 | $\text{Classify the continuity of }f(x)=\begin{cases}1&x<-4\\-2&x\ge -4\end{cases}\text{ at }x=-4.$ | $\text{jump discontinuity}$ | `—` | `spec_pack=limit_continuity · methods=classify_jump · form_id=piecewise_jump · costs[form:piecewise_jump=0 ⇒ 0] · D=0` |
| 0 | $\text{Classify the continuity of }f(x)=-6x - 2\text{ at }x=-2.$ | $\text{continuous}$ | `—` | `spec_pack=limit_continuity · methods=classify_continuous · form_id=continuity_linear · shape=poly_direct · costs[form:continuity_linear=2 ⇒ 2] · D=0` |
| 3 | $\text{Classify the continuity of }f(x)=\frac{x^{2}-16}{x-4}\text{ at }x=4.$ | $\text{removable discontinuity}$ | `—` | `spec_pack=limit_continuity · methods=classify_removable · form_id=removable_diff_sq · shape=removable_factor · costs[form:removable_diff_sq=3 ⇒ 3] · D=3` |
| 3 | $\text{Classify the continuity of }f(x)=\frac{x^{2}-25}{x+5}\text{ at }x=-5.$ | $\text{removable discontinuity}$ | `—` | `spec_pack=limit_continuity · methods=classify_removable · form_id=removable_diff_sq · shape=removable_factor · costs[form:removable_diff_sq=3 ⇒ 3] · D=3` |
| 3 | $\text{Classify the continuity of }f(x)=\begin{cases}-3&x<5\\4&x\ge 5\end{cases}\text{ at }x=5.$ | $\text{jump discontinuity}$ | `—` | `spec_pack=limit_continuity · methods=classify_jump · form_id=piecewise_jump · costs[form:piecewise_jump=0 ⇒ 0] · D=3` |
| 6 | $\text{Classify the continuity of }f(x)=x + 6\text{ at }x=-1.$ | $\text{continuous}$ | `—` | `spec_pack=limit_continuity · methods=classify_continuous · form_id=continuity_linear · dress=[jump_side_linear] · shape=poly_direct · costs[form:continuity_linear=2 + dress:jump_side_linear=2 ⇒ 4] · D=6` |
| 6 | $\text{Classify the continuity of }f(x)=-5x + 6\text{ at }x=-1.$ | $\text{continuous}$ | `—` | `spec_pack=limit_continuity · methods=classify_continuous · form_id=continuity_linear · dress=[jump_side_linear] · shape=poly_direct · costs[form:continuity_linear=2 + dress:jump_side_linear=2 ⇒ 4] · D=6` |
| 6 | $\text{Classify the continuity of }f(x)=\frac{x^{2} + 8x + 15}{x+5}\text{ at }x=-5.$ | $\text{removable discontinuity}$ | `—` | `spec_pack=limit_continuity · methods=classify_removable · form_id=removable_linear_factor · dress=[removable_expand] · shape=removable_factor · costs[form:removable_linear_factor=3 + dress:removable_expand=2 ⇒ 5] · D=6` |
| 8 | $\text{Classify the continuity of }f(x)=3x^{2} - 3x + 3\text{ at }x=0.$ | $\text{continuous}$ | `—` | `spec_pack=limit_continuity · methods=classify_continuous · form_id=continuity_poly · dress=[jump_side_quad] · shape=poly_direct · costs[form:continuity_poly=2 + dress:jump_side_quad=3 ⇒ 5] · D=8` |
| 8 | $\text{Classify the continuity of }f(x)=4x^{2} + 3x + 3\text{ at }x=-4.$ | $\text{continuous}$ | `—` | `spec_pack=limit_continuity · methods=classify_continuous · form_id=continuity_poly · dress=[jump_side_quad] · shape=poly_direct · costs[form:continuity_poly=2 + dress:jump_side_quad=3 ⇒ 5] · D=8` |
| 8 | $\text{Classify the continuity of }f(x)=-5x^{2} + x + 4\text{ at }x=0.$ | $\text{continuous}$ | `—` | `spec_pack=limit_continuity · methods=classify_continuous · form_id=continuity_poly · dress=[jump_side_quad] · shape=poly_direct · costs[form:continuity_poly=2 + dress:jump_side_quad=3 ⇒ 5] · D=8` |
| 12 | $\text{Classify the continuity of }f(x)=4x^{2} - x - 1\text{ at }x=-3.$ | $\text{continuous}$ | `—` | `spec_pack=limit_continuity · methods=classify_continuous · form_id=continuity_poly · dress=[jump_side_quad] · shape=poly_direct · costs[form:continuity_poly=2 + dress:jump_side_quad=3 ⇒ 5] · D=12` |
| 12 | $\text{Classify the continuity of }f(x)=2x^{2} + 3\text{ at }x=4.$ | $\text{continuous}$ | `—` | `spec_pack=limit_continuity · methods=classify_continuous · form_id=continuity_poly · dress=[jump_side_quad] · shape=poly_direct · costs[form:continuity_poly=2 + dress:jump_side_quad=3 ⇒ 5] · D=12` |
| 12 | $\text{Classify the continuity of }f(x)=\frac{x^{2} + 10x + 25}{x+5}\text{ at }x=-5.$ | $\text{removable discontinuity}$ | `—` | `spec_pack=limit_continuity · methods=classify_removable · form_id=removable_linear_factor · dress=[removable_expand] · shape=removable_factor · costs[form:removable_linear_factor=3 + dress:removable_expand=2 ⇒ 5] · D=12` |
| 16 | $\text{Classify the continuity of }f(x)=\begin{cases}x^{2} - 3x + 2&x<-3\\-2x^{3} - 2x^{2} - 4x - 3&x\ge -3\end{cases}\text{ at }x=-3.$ | $\text{jump discontinuity}$ | `—` | `spec_pack=limit_continuity · methods=classify_jump · form_id=piecewise_jump_poly · dress=[jump_side_cubic] · shape=piecewise_jump · costs[form:piecewise_jump_poly=10 + dress:jump_side_cubic=4 ⇒ 14] · D=16` |
| 16 | $\text{Classify the continuity of }f(x)=-3x^{2} - 4x\text{ at }x=-5.$ | $\text{continuous}$ | `—` | `spec_pack=limit_continuity · methods=classify_continuous · form_id=continuity_poly · dress=[jump_side_quad] · shape=poly_direct · costs[form:continuity_poly=2 + dress:jump_side_quad=3 ⇒ 5] · D=16` |
| 16 | $\text{Classify the continuity of }f(x)=\frac{x^{2} - x - 12}{x-4}\text{ at }x=4.$ | $\text{removable discontinuity}$ | `—` | `spec_pack=limit_continuity · methods=classify_removable · form_id=removable_linear_factor · dress=[removable_expand] · shape=removable_factor · costs[form:removable_linear_factor=3 + dress:removable_expand=2 ⇒ 5] · D=16` |
| 20 | $\text{Classify the continuity of }f(x)=\frac{x^{2} + 2x}{x-0}\text{ at }x=0.$ | $\text{removable discontinuity}$ | `—` | `spec_pack=limit_continuity · methods=classify_removable · form_id=removable_linear_factor · dress=[removable_expand] · shape=removable_factor · costs[form:removable_linear_factor=3 + dress:removable_expand=2 ⇒ 5] · D=20` |
| 20 | $\text{Classify the continuity of }f(x)=-2x^{2} + 2x - 2\text{ at }x=4.$ | $\text{continuous}$ | `—` | `spec_pack=limit_continuity · methods=classify_continuous · form_id=continuity_poly · dress=[jump_side_quad] · shape=poly_direct · costs[form:continuity_poly=2 + dress:jump_side_quad=3 ⇒ 5] · D=20` |
| 20 | $\text{Classify the continuity of }f(x)=\begin{cases}-x - 4&x<-5\\2x - 3&x\ge -5\end{cases}\text{ at }x=-5.$ | $\text{jump discontinuity}$ | `—` | `spec_pack=limit_continuity · methods=classify_jump · form_id=piecewise_jump_linear · shape=piecewise_jump · costs[form:piecewise_jump_linear=6 ⇒ 6] · D=20` |
| 25 | $\text{Classify the continuity of }f(x)=\begin{cases}3x^{2} - x + 2&x<-4\\3x^{2} - 3x - 2&x\ge -4\end{cases}\text{ at }x=-4.$ | $\text{jump discontinuity}$ | `—` | `spec_pack=limit_continuity · methods=classify_jump · form_id=piecewise_jump_poly · shape=piecewise_jump · costs[form:piecewise_jump_poly=10 ⇒ 10] · D=25` |
| 25 | $\text{Classify the continuity of }f(x)=\frac{x^{2} + 6x + 8}{x+2}\text{ at }x=-2.$ | $\text{removable discontinuity}$ | `—` | `spec_pack=limit_continuity · methods=classify_removable · form_id=removable_linear_factor · dress=[removable_expand] · shape=removable_factor · costs[form:removable_linear_factor=3 + dress:removable_expand=2 ⇒ 5] · D=25` |
| 25 | $\text{Classify the continuity of }f(x)=\frac{x^{2} - 4}{x-2}\text{ at }x=2.$ | $\text{removable discontinuity}$ | `—` | `spec_pack=limit_continuity · methods=classify_removable · form_id=removable_linear_factor · dress=[removable_expand] · shape=removable_factor · costs[form:removable_linear_factor=3 + dress:removable_expand=2 ⇒ 5] · D=25` |

## L'Hôpital's rule

<a id="lhopital"></a>

`calc_app_diff_lhopitals_rule` · pack `lhopital` · topic label: c1: L'Hôpital's Rule · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **10** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `lhopital_0_0_poly` | 8 |
| `lhopital_inf_inf_poly` | 3 |
| `lhopital_0_0_power` | 2 |
| `lhopital_0_inf_product` | 2 |
| `lhopital_inf_minus_inf` | 2 |
| `lhopital_multipass_trig` | 2 |
| `lhopital_poly_over_exp` | 2 |
| `lhopital_0_0_trig` | 1 |
| `lhopital_0_inf_power` | 1 |
| `lhopital_multipass_exp` | 1 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\lim_{x \to 4} \frac{x^{2}-16}{x-4}$ | $8$ | `—` | `spec_pack=limit_lhopital · methods=lhopital · form_id=lhopital_0_0_poly · indet=0/0 · shape=indet_0_0 · costs[form:lhopital_0_0_poly=4 + spec:lhopital_steps=3 ⇒ 7] · D=0` |
| 0 | $\lim_{x \to 3} \frac{x^{2}-9}{x-3}$ | $6$ | `—` | `spec_pack=limit_lhopital · methods=lhopital · form_id=lhopital_0_0_poly · indet=0/0 · shape=indet_0_0 · costs[form:lhopital_0_0_poly=4 + spec:lhopital_steps=3 ⇒ 7] · D=0` |
| 0 | $\lim_{x \to 2} \frac{x^{2}-4}{x-2}$ | $4$ | `—` | `spec_pack=limit_lhopital · methods=lhopital · form_id=lhopital_0_0_poly · indet=0/0 · shape=indet_0_0 · costs[form:lhopital_0_0_poly=4 + spec:lhopital_steps=3 ⇒ 7] · D=0` |
| 3 | $\lim_{x \to 2} \frac{x^{2}-4}{x-2}$ | $4$ | `—` | `spec_pack=limit_lhopital · methods=lhopital · form_id=lhopital_0_0_poly · indet=0/0 · shape=indet_0_0 · costs[form:lhopital_0_0_poly=4 + spec:lhopital_steps=3 ⇒ 7] · D=3` |
| 3 | $\lim_{x \to 3} \frac{x^{2}-9}{x-3}$ | $6$ | `—` | `spec_pack=limit_lhopital · methods=lhopital · form_id=lhopital_0_0_poly · indet=0/0 · shape=indet_0_0 · costs[form:lhopital_0_0_poly=4 + spec:lhopital_steps=3 ⇒ 7] · D=3` |
| 3 | $\lim_{x \to 1} \frac{x^{2}-1}{x-1}$ | $2$ | `—` | `spec_pack=limit_lhopital · methods=lhopital · form_id=lhopital_0_0_poly · indet=0/0 · shape=indet_0_0 · costs[form:lhopital_0_0_poly=4 + spec:lhopital_steps=3 ⇒ 7] · D=3` |
| 6 | $\lim_{x \to \infty} -\frac{3x^{2}+6}{1x^{2}-4}$ | $-3$ | `—` | `spec_pack=limit_lhopital · methods=lhopital · form_id=lhopital_inf_inf_poly · dress=[sign] · indet=∞/∞ · shape=indet_inf_inf · costs[form:lhopital_inf_inf_poly=8 + dress:spec_sign=0.5 + spec:lhopital_steps=3 ⇒ 11.5] · D=6` |
| 6 | $\lim_{x \to 2} -4\frac{x^{2}-4}{x-2}$ | $-16$ | `—` | `spec_pack=limit_lhopital · methods=lhopital · form_id=lhopital_0_0_poly · dress=[constant_multiple] · indet=0/0 · shape=indet_0_0 · costs[form:lhopital_0_0_poly=4 + dress:spec_scale=1.5 + spec:lhopital_steps=3 ⇒ 8.5] · D=6` |
| 6 | $\lim_{x \to \infty} \frac{3x^{2}+3}{6x^{2}-4}$ | $\frac{1}{2}$ | `—` | `spec_pack=limit_lhopital · methods=lhopital · form_id=lhopital_inf_inf_poly · indet=∞/∞ · shape=indet_inf_inf · costs[form:lhopital_inf_inf_poly=8 + spec:lhopital_steps=3 ⇒ 11] · D=6` |
| 8 | $\lim_{x \to 0^{+}} \left(\frac{1}{x}-\frac{1}{\sin(x)}\right)$ | $-\frac{1}{6}$ | `—` | `spec_pack=limit_lhopital · methods=lhopital · form_id=lhopital_inf_minus_inf · indet=∞−∞ · shape=indet_inf_minus_inf · costs[form:lhopital_inf_minus_inf=8 + spec:allow_trig=1.5 + spec:lhopital_twice=4 ⇒ 13.5] · D=8` |
| 8 | $\lim_{x \to \infty} -\frac{1x^{2}+3}{2x^{2}+1}$ | $-\frac{1}{2}$ | `—` | `spec_pack=limit_lhopital · methods=lhopital · form_id=lhopital_inf_inf_poly · dress=[sign] · indet=∞/∞ · shape=indet_inf_inf · costs[form:lhopital_inf_inf_poly=8 + dress:spec_sign=0.5 + spec:lhopital_steps=3 ⇒ 11.5] · D=8` |
| 8 | $\lim_{x \to 0^{+}} -x \ln(x)$ | $0$ | `—` | `spec_pack=limit_lhopital · methods=lhopital · form_id=lhopital_0_inf_product · dress=[sign] · indet=0·∞ · shape=indet_0_inf · costs[form:lhopital_0_inf_product=8 + dress:spec_sign=0.5 + spec:allow_log=1.5 + spec:lhopital_steps=3 ⇒ 13] · D=8` |
| 12 | $\lim_{x \to 0} 2\frac{\sin(x)-x}{x^{2}}$ | $0$ | `—` | `spec_pack=limit_lhopital · methods=lhopital · form_id=lhopital_multipass_trig · dress=[sign,constant_multiple] · indet=0/0 · shape=indet_0_0 · costs[form:lhopital_multipass_trig=12 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:allow_trig=1.5 + spec:lhopital_twice=4 ⇒ 19.5] · D=12` |
| 12 | $\lim_{x \to 0} -\left(\left(\csc(x)-\cot(x)\right)\right)$ | $0$ | `—` | `spec_pack=limit_lhopital · methods=lhopital · form_id=lhopital_inf_minus_inf · dress=[sign] · indet=∞−∞ · shape=indet_inf_minus_inf · costs[form:lhopital_inf_minus_inf=8 + dress:spec_sign=0.5 + spec:allow_trig=1.5 + spec:lhopital_steps=3 ⇒ 13] · D=12` |
| 12 | $\lim_{x \to 0} -\frac{\sin(6x)}{x}$ | $-6$ | `—` | `spec_pack=limit_lhopital · methods=lhopital · form_id=lhopital_0_0_trig · dress=[sign] · indet=0/0 · shape=indet_0_0 · costs[form:lhopital_0_0_trig=4 + dress:spec_sign=0.5 + spec:allow_trig=1.5 + spec:lhopital_steps=3 ⇒ 9] · D=12` |
| 16 | $\lim_{x \to 0^{+}} -x^{\sin(x)}$ | $-1$ | `—` | `spec_pack=limit_lhopital · methods=lhopital · form_id=lhopital_0_0_power · dress=[sign] · indet=0^0 · shape=indet_0_0_pow · costs[form:lhopital_0_0_power=10 + dress:spec_sign=0.5 + spec:allow_log=1.5 + spec:allow_exp=1.5 + spec:lhopital_steps=3 ⇒ 16.5] · D=16` |
| 16 | $\lim_{x \to 0} 4\frac{e^{x}-1-x}{x^{2}}$ | $2$ | `—` | `spec_pack=limit_lhopital · methods=lhopital · form_id=lhopital_multipass_exp · dress=[sign,constant_multiple] · indet=0/0 · shape=indet_0_0 · costs[form:lhopital_multipass_exp=12 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:allow_exp=1.5 + spec:lhopital_twice=4 ⇒ 19.5] · D=16` |
| 16 | $\lim_{x \to \infty} -4\frac{x^{2}}{e^{x}}$ | $0$ | `—` | `spec_pack=limit_lhopital · methods=lhopital · form_id=lhopital_poly_over_exp · dress=[sign,constant_multiple] · indet=∞/∞ · shape=indet_inf_inf · costs[form:lhopital_poly_over_exp=14 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:allow_exp=1.5 + spec:lhopital_twice=4 ⇒ 21.5] · D=16` |
| 20 | $\lim_{x \to 0^{+}} 3x^{2/x}$ | $0$ | `—` | `spec_pack=limit_lhopital · methods=lhopital · form_id=lhopital_0_inf_power · dress=[sign,constant_multiple] · indet=0^∞ · shape=indet_0_inf_pow · costs[form:lhopital_0_inf_power=12 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:lhopital_twice=4 + spec:allow_log=1.5 + spec:allow_exp=1.5 ⇒ 21] · D=20` |
| 20 | $\lim_{x \to 0^{+}} -3x^{1} \ln(x)$ | $0$ | `—` | `spec_pack=limit_lhopital · methods=lhopital · form_id=lhopital_0_inf_product · dress=[sign,constant_multiple] · indet=0·∞ · shape=indet_0_inf · costs[form:lhopital_0_inf_product=8 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:lhopital_twice=4 + spec:allow_log=1.5 ⇒ 15.5] · D=20` |
| 20 | $\lim_{x \to 0} -3\frac{\sin(x)-x}{x^{2}}$ | $0$ | `—` | `spec_pack=limit_lhopital · methods=lhopital · form_id=lhopital_multipass_trig · dress=[constant_multiple] · indet=0/0 · shape=indet_0_0 · costs[form:lhopital_multipass_trig=12 + dress:spec_scale=1.5 + spec:lhopital_twice=4 + spec:allow_trig=1.5 ⇒ 19] · D=20` |
| 25 | $\lim_{x \to 4} -\frac{x^{2}-16}{x-4}$ | $-8$ | `—` | `spec_pack=limit_lhopital · methods=lhopital · form_id=lhopital_0_0_poly · dress=[sign] · indet=0/0 · shape=indet_0_0 · costs[form:lhopital_0_0_poly=4 + dress:spec_sign=0.5 + spec:lhopital_steps=3 ⇒ 7.5] · D=25` |
| 25 | $\lim_{x \to \infty} -\frac{x^{2}}{e^{x}}$ | $0$ | `—` | `spec_pack=limit_lhopital · methods=lhopital · form_id=lhopital_poly_over_exp · dress=[sign] · indet=∞/∞ · shape=indet_inf_inf · costs[form:lhopital_poly_over_exp=14 + dress:spec_sign=0.5 + spec:allow_exp=1.5 + spec:lhopital_twice=4 ⇒ 20] · D=25` |
| 25 | $\lim_{x \to 0^{+}} 4x^{1x}$ | $4$ | `—` | `spec_pack=limit_lhopital · methods=lhopital · form_id=lhopital_0_0_power · dress=[constant_multiple] · indet=0^0 · shape=indet_0_0_pow · costs[form:lhopital_0_0_power=10 + dress:spec_scale=1.5 + spec:allow_log=1.5 + spec:allow_exp=1.5 + spec:lhopital_steps=3 ⇒ 17.5] · D=25` |

## Derivatives — power rule

<a id="deriv_power"></a>

`calc_diff_power_rule` · pack `deriv_power` · topic label: c1: Power Rule · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **4** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `power_poly` | 7 |
| `power_root` | 7 |
| `chain_power_linear` | 5 |
| `power_negative` | 5 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\frac{d}{dx}\left[-x^{2}\right]$ | $-2x$ | `—` | `pack=deriv_power · methods=power · form_id=power_poly · shape=power · costs[form:power_poly=0 ⇒ 0] · D=0` |
| 0 | $\text{Find }\frac{d}{dx}\left(2x^{2}\right)$ | $4x$ | `—` | `pack=deriv_power · methods=power · form_id=power_poly · shape=power · costs[form:power_poly=0 ⇒ 0] · D=0` |
| 0 | $\frac{d}{dx}\left[2x^{2}\right]$ | $4x$ | `—` | `pack=deriv_power · methods=power · form_id=power_poly · shape=power · costs[form:power_poly=0 ⇒ 0] · D=0` |
| 3 | $\frac{d}{dx}\left[\left(x^{2} - 3\right)^{2}\right]$ | $2\left(x^{2} - 3\right)\left(2x\right)$ | `—` | `pack=deriv_power · methods=chain,power · form_id=chain_power_linear · shape=sum+power · costs[form:chain_power_linear=4 + spec:use_chain=2 + spec:chain=2 ⇒ 8] · D=3` |
| 3 | $\frac{d}{dx}\left[2x^{2} + x - 2\right]$ | $4x + 1$ | `—` | `pack=deriv_power · methods=power,sum · form_id=power_poly · shape=sum+power · costs[form:power_poly=0 ⇒ 0] · D=3` |
| 3 | $\frac{d}{dx}\left[\sqrt{x + 2}\right]$ | $\frac{1}{2\sqrt{\left(x + 2\right)}}$ | `—` | `pack=deriv_power · methods=chain,power · form_id=chain_power_linear · shape=fn:sqrt+sum · costs[form:chain_power_linear=4 + spec:use_chain=2 + spec:chain=2 + spec:allow_roots=1 ⇒ 9] · D=3` |
| 6 | $\text{Find }\frac{d}{dx}\left(+x^{\frac{7}{2}}\right)$ | $\frac{7}{2}x^{\frac{5}{2}}$ | `—` | `pack=deriv_power · methods=power · form_id=power_negative · dress=[sign] · shape=power · costs[form:power_negative=6 + dress:spec_sign=0.5 + spec:allow_roots=1 ⇒ 7.5] · D=6` |
| 6 | $\frac{d}{dx}\left[-x^{2} + 5x - 1\right]$ | $-2x + 5$ | `—` | `pack=deriv_power · methods=power,sum · form_id=power_poly · dress=[sign] · shape=sum+power · costs[form:power_poly=0 + dress:spec_sign=0.5 ⇒ 0.5] · D=6` |
| 6 | $\text{Find }\frac{d}{dx}\left(-x^{-\frac{3}{2}}\right)$ | $\frac{3}{2}x^{-\frac{5}{2}}$ | `—` | `pack=deriv_power · methods=power · form_id=power_negative · shape=power · costs[form:power_negative=6 + spec:allow_roots=1 ⇒ 7] · D=6` |
| 8 | $\frac{d}{dx}\left[-x^{-3}\right]$ | $3x^{-4}$ | `—` | `pack=deriv_power · methods=power · form_id=power_poly · shape=power · costs[form:power_poly=0 + spec:fn_power=1.5 ⇒ 1.5] · D=8` |
| 8 | $\frac{d}{dx}\left[-\left(3x^{2} - 4\right)^{\frac{5}{2}}\right]$ | $-6\frac{5}{2}\left(3x^{2} - 4\right)^{\frac{3}{2}}x$ | `—` | `pack=deriv_power · methods=chain,power · form_id=power_negative · dress=[sign] · shape=sum+power · costs[form:power_negative=6 + dress:spec_sign=0.5 + spec:fn_power=1.5 + spec:chain=2 + spec:allow_roots=1 ⇒ 11] · D=8` |
| 8 | $\text{Find }\frac{d}{dx}\left(\sqrt{4x + 5}\right)$ | $\frac{1}{2\sqrt{4x + 5}}\left(4\right)$ | `—` | `pack=deriv_power · methods=chain,power · form_id=chain_power_linear · shape=fn:sqrt+sum · costs[form:chain_power_linear=4 + spec:use_chain=2 + spec:chain=2 + spec:allow_roots=1 ⇒ 9] · D=8` |
| 12 | $\text{Find }\frac{d}{dx}\left(-\sqrt{x}\right)$ | $-\frac{1}{2\sqrt{x}}$ | `—` | `pack=deriv_power · methods=power · form_id=power_root · dress=[sign] · shape=fn:sqrt · costs[form:power_root=4 + dress:spec_sign=0.5 + spec:fn_power=1.5 + spec:use_roots=1 + spec:allow_roots=1 ⇒ 8] · D=12` |
| 12 | $\text{Find }\frac{d}{dx}\left(-\sqrt{4x + 1}\right)$ | $-4\frac{1}{2\sqrt{4x + 1}}$ | `—` | `pack=deriv_power · methods=chain,power · form_id=power_negative · dress=[sign] · shape=fn:sqrt+sum · costs[form:power_negative=6 + dress:spec_sign=0.5 + spec:fn_power=1.5 + spec:chain=2 + spec:allow_roots=1 ⇒ 11] · D=12` |
| 12 | $\frac{d^{2}}{dx^{2}}\left[2x^{2} + 4x - 4\right]$ | $4$ | `—` | `pack=deriv_power · methods=power,sum · form_id=power_root · shape=sum+power · costs[form:power_root=4 + spec:fn_power=1.5 + spec:use_roots=1 ⇒ 6.5] · D=12` |
| 16 | $\frac{d^{2}}{dx^{2}}\left[-3x^{3} + 3x^{2} + x - 6\right]$ | $-18x + 6$ | `—` | `pack=deriv_power · methods=power,sum · form_id=power_root · dress=[sign] · shape=sum+power · costs[form:power_root=4 + dress:spec_sign=0.5 + spec:fn_power=1.5 + spec:use_roots=1 ⇒ 7] · D=16` |
| 16 | $\frac{d^{2}}{dx^{2}}\left[4x^{3} - 4x^{2} + 10x + 10\right]$ | $46x - 8$ | `—` | `pack=deriv_power · methods=power,sum · form_id=power_negative · dress=[sign,constant_multiple] · shape=sum+power · costs[form:power_negative=6 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:fn_power=1.5 ⇒ 9.5] · D=16` |
| 16 | $\frac{d^{2}}{dx^{2}}\left[+x^{\frac{5}{3}}\right]$ | $\frac{2}{3}x^{-\frac{1}{3}}\frac{5}{3}$ | `—` | `pack=deriv_power · methods=power · form_id=power_poly · dress=[sign] · shape=power · costs[form:power_poly=0 + dress:spec_sign=0.5 + spec:fn_power=1.5 + spec:allow_roots=1 ⇒ 3] · D=16` |
| 20 | $\frac{d}{dx}\left[-\left(3x^{2} + 4\right)^{\sqrt{3}}\right]$ | $-6\sqrt{3}\left(3x^{2} + 4\right)^{\sqrt{3}-1}x$ | `—` | `pack=deriv_power · methods=chain,power · form_id=power_root · dress=[sign] · shape=sum+power · costs[form:power_root=4 + dress:spec_sign=0.5 + spec:fn_power=1.5 + spec:use_roots=1 + spec:chain=2 ⇒ 9] · D=20` |
| 20 | $\frac{d}{dx}\left[-\sqrt{9x + 2}\sqrt{4x + 8}\right]$ | $-9\frac{1}{2\sqrt{9x + 2}}\sqrt{4x + 8} + 4\frac{1}{2\sqrt{4x + 8}}\sqrt{9x + 2}$ | `—` | `pack=deriv_power · methods=chain,power,product · form_id=chain_power_linear · dress=[sign] · shape=fn:sqrt+product+sum · costs[form:chain_power_linear=4 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:fn_power=1.5 + spec:use_chain=2 + spec:chain=2 + spec:product=2 + spec:allow_roots=1 ⇒ 14.5] · D=20` |
| 20 | $\frac{d^{2}}{dx^{2}}\left[-\left(\left(3x^{2} - 2\right)^{2}\right)^{3}\right]$ | $-864\left(3x^{2} - 2\right)^{2}\left(3x^{2} - 2\right)x\left(3x^{2} - 2\right)x - 216x\left(\left(3x^{2} - 2\right)^{2}\right)^{2}x - 36\left(\left(3x^{2} - 2\right)^{2}\right)^{2}\left(3x^{2} - 2\right)$ | `—` | `pack=deriv_power · methods=chain,power · form_id=power_root · dress=[sign] · shape=sum+power · costs[form:power_root=4 + dress:spec_sign=0.5 + spec:fn_power=1.5 + spec:use_roots=1 + spec:chain=2 + spec:nest_depth=2 ⇒ 11] · D=20` |
| 25 | $\frac{d^{2}}{dx^{2}}\left[-23x^{3}\right]$ | $-36x$ | `—` | `pack=deriv_power · methods=power · form_id=power_root · dress=[sign,constant_multiple] · shape=power · costs[form:power_root=4 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:fn_power=1.5 + spec:use_roots=1 ⇒ 8.5] · D=25` |
| 25 | $\frac{d^{2}}{dx^{2}}\left[+7x^{\frac{4}{3}}\right]$ | $7\frac{1}{3}x^{-\frac{2}{3}}\frac{4}{3}$ | `—` | `pack=deriv_power · methods=power · form_id=power_root · dress=[sign] · shape=power · costs[form:power_root=4 + dress:spec_sign=0.5 + spec:fn_power=1.5 + spec:use_roots=1 + spec:allow_roots=1 ⇒ 8] · D=25` |
| 25 | $\frac{d^{2}}{dx^{2}}\left[-\sqrt{x + 1}\right]$ | $+\frac{1}{4}\left(x + 1\right)^{-\frac{3}{2}}$ | `—` | `pack=deriv_power · methods=chain,power · form_id=chain_power_linear · dress=[sign] · shape=fn:sqrt+sum · costs[form:chain_power_linear=4 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:fn_power=1.5 + spec:use_chain=2 + spec:chain=2 + spec:allow_roots=1 ⇒ 12.5] · D=25` |

## Derivatives — product rule

<a id="deriv_product"></a>

`calc_diff_product_rule` · pack `deriv_product` · topic label: c1: Product Rule · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **1** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `product_two_poly` | 24 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\text{Find }\frac{d}{dx}\left(\left(-2x\right)x^{2}\right)$ | $\left(-2\right)x^{2}+\left(-2x\right)\left(2x\right)$ | `—` | `pack=deriv_product · methods=power,product · form_id=product_two_poly · shape=product+power · costs[form:product_two_poly=0 ⇒ 0] · D=0` |
| 0 | $\frac{d}{dx}\left[x^{2}x\right]$ | $2xx+x^{2}\left(1\right)$ | `—` | `pack=deriv_product · methods=power,product · form_id=product_two_poly · shape=product+power · costs[form:product_two_poly=0 ⇒ 0] · D=0` |
| 0 | $\text{Find }\frac{d}{dx}\left(\left(-2x^{2}\right)\left(-2x\right)\right)$ | $\left(-4x\right)\left(-2x\right)+\left(-2x^{2}\right)\left(-2\right)$ | `—` | `pack=deriv_product · methods=power,product · form_id=product_two_poly · shape=product+power · costs[form:product_two_poly=0 ⇒ 0] · D=0` |
| 3 | $\frac{d}{dx}\left[2x^{2}\left(2x^{2}\right)\right]$ | $4x\left(2x^{2}\right)+2x^{2}\left(4x\right)$ | `—` | `pack=deriv_product · methods=power,product · form_id=product_two_poly · shape=product+power · costs[form:product_two_poly=0 ⇒ 0] · D=3` |
| 3 | $\frac{d}{dx}\left[\left(-2x\right)\left(-2x^{3}\right)\right]$ | $\left(-2\right)\left(-2x^{3}\right)+\left(-2x\right)\left(-6x^{2}\right)$ | `—` | `pack=deriv_product · methods=power,product · form_id=product_two_poly · shape=product+power · costs[form:product_two_poly=0 ⇒ 0] · D=3` |
| 3 | $\frac{d}{dx}\left[\left(-x\right)\left(-2x\right)\right]$ | $\left(-1\right)\left(-2x\right)+\left(-x\right)\left(-2\right)$ | `—` | `pack=deriv_product · methods=power,product · form_id=product_two_poly · shape=product · costs[form:product_two_poly=0 ⇒ 0] · D=3` |
| 6 | $\frac{d}{dx}\left[\left(x^{2} + 3x - 3\right)\left(5x\right)\right]$ | $\left(2x + 3\right)\left(5x\right)+\left(x^{2} + 3x - 3\right)\left(5\right)$ | `—` | `pack=deriv_product · methods=power,product · form_id=product_two_poly · shape=product+sum+power · costs[form:product_two_poly=0 ⇒ 0] · D=6` |
| 6 | $\text{Find }\frac{d}{dx}\left(\left(x + 1\right)\left(4x^{3}\left(x^{2} + x + 1\right)\right)\right)$ | $4x^{3}\left(x^{2} + x + 1\right) + \left(12x^{2}\left(x^{2} + x + 1\right) + 4\left(2x + 1\right)x^{3}\right)\left(x + 1\right)$ | `—` | `pack=deriv_product · methods=power,product · form_id=product_two_poly · dress=[spec_product_dress] · shape=product+sum+power · costs[form:product_two_poly=0 + dress:spec_product_dress=3 ⇒ 3] · D=6` |
| 6 | $\text{Find }\frac{d}{dx}\left(-5x^{3}\left(5x^{2}\right)\right)$ | $-75x^{2}x^{2} + 50xx^{3}$ | `—` | `pack=deriv_product · methods=power,product · form_id=product_two_poly · dress=[sign] · shape=product+power · costs[form:product_two_poly=0 + dress:spec_sign=0.5 ⇒ 0.5] · D=6` |
| 8 | $\text{Find }\frac{d}{dx}\left(3\left(-4x^{2}\right)\left(-4x^{3}\right)\right)$ | $332xx^{3} + 48x^{2}x^{2}$ | `—` | `pack=deriv_product · methods=power,product · form_id=product_two_poly · dress=[constant_multiple] · shape=product+power · costs[form:product_two_poly=0 + dress:spec_scale=1.5 + spec:use_chain=2 ⇒ 3.5] · D=8` |
| 8 | $\text{Find }\frac{d}{dx}\left(\left(x - 2\right)x\left(3x\right)\right)$ | $3xx + \left(6x\right)\left(x - 2\right)$ | `—` | `pack=deriv_product · methods=power,product · form_id=product_two_poly · dress=[spec_product_dress] · shape=product · costs[form:product_two_poly=0 + dress:spec_product_dress=3 + spec:use_chain=2 ⇒ 5] · D=8` |
| 8 | $\text{Find }\frac{d}{dx}\left(-\left(-3x^{4}\right)\left(4x^{3}\right)\right)$ | $+48x^{3}x^{3} - 36x^{2}x^{4}$ | `—` | `pack=deriv_product · methods=power,product · form_id=product_two_poly · dress=[sign] · shape=product+power · costs[form:product_two_poly=0 + dress:spec_sign=0.5 + spec:use_chain=2 ⇒ 2.5] · D=8` |
| 12 | $\text{Find }\frac{d}{dx}\left(\left(x + 1\right)\left(4x\left(3x\right)\right)\right)$ | $12xx + \left(24x\right)\left(x + 1\right)$ | `—` | `pack=deriv_product · methods=power,product · form_id=product_two_poly · dress=[spec_product_dress] · shape=product · costs[form:product_two_poly=0 + dress:spec_product_dress=3 + spec:chain_depth_2=1.5 + spec:use_chain=2 ⇒ 6.5] · D=12` |
| 12 | $\text{Find }\frac{d}{dx}\left(\left(x - 1\right)\left(-4x^{2}\right)\left(2x^{2}\right)\right)$ | $-8x^{2}x^{2} + \left(-16xx^{2} - 16xx^{2}\right)\left(x - 1\right)$ | `—` | `pack=deriv_product · methods=power,product · form_id=product_two_poly · dress=[spec_product_dress] · shape=product+power · costs[form:product_two_poly=0 + dress:spec_product_dress=3 + spec:chain_depth_2=1.5 + spec:use_chain=2 ⇒ 6.5] · D=12` |
| 12 | $\frac{d}{dx}\left[\left(x - 2\right)\left(2x^{3} - 6x^{2} + 5x - 3\right)\left(3x^{2} + 5x - 1\right)\right]$ | $\left(2x^{3} - 6x^{2} + 5x - 3\right)\left(3x^{2} + 5x - 1\right) + \left(\left(6x^{2} - 12x + 5\right)\left(3x^{2} + 5x - 1\right) + \left(6x + 5\right)\left(2x^{3} - 6x^{2} + 5x - 3\right)\right)\left(x - 2\right)$ | `—` | `pack=deriv_product · methods=power,product · form_id=product_two_poly · dress=[spec_product_dress] · shape=product+sum+power · costs[form:product_two_poly=0 + dress:spec_product_dress=3 + spec:chain_depth_2=1.5 + spec:use_chain=2 ⇒ 6.5] · D=12` |
| 16 | $\text{Find }\frac{d}{dx}\left(\left(x + 2\right)\left(3x - 2\right)\left(2x^{3} - 8x^{2} + 5x + 1\right)\left(-10x^{\frac{7}{2}}\right)\right)$ | $-10\left(3x - 2\right)\left(2x^{3} - 8x^{2} + 5x + 1\right)x^{\frac{7}{2}} + \left(-30\left(2x^{3} - 8x^{2} + 5x + 1\right)x^{\frac{7}{2}} + \left(-10\left(6x^{2} - 16x + 5\right)x^{\frac{7}{2}} - 10\frac{7}{2}x^{\frac{5}{2}}\left(2x^{3} - 8x^{2} + 5x + 1\right)\right)\left(3x - 2\right)\right)\left(x + 2\right)$ | `—` | `pack=deriv_product · methods=power,product · form_id=product_two_poly · dress=[spec_product_dress,spec_product_dress#2] · shape=product+sum+power · costs[form:product_two_poly=0 + dress:spec_product_dress=3 + dress:spec_product_dress#2=3 + spec:chain_depth_2=1.5 + spec:fn_power=1.5 + spec:use_chain=2 + spec:allow_roots=1 ⇒ 12] · D=16` |
| 16 | $\frac{d}{dx}\left[\left(2x + 2\right)x^{\frac{4}{5}}\left(-5x^{\frac{4}{3}}\right)\right]$ | $-10x^{\frac{4}{5}}x^{\frac{4}{3}} + \left(-5\frac{4}{5}x^{-\frac{1}{5}}x^{\frac{4}{3}} - 5\frac{4}{3}x^{\frac{1}{3}}x^{\frac{4}{5}}\right)\left(2x + 2\right)$ | `—` | `pack=deriv_product · methods=power,product · form_id=product_two_poly · dress=[spec_product_dress] · shape=product+power · costs[form:product_two_poly=0 + dress:spec_product_dress=3 + spec:chain_depth_2=1.5 + spec:fn_power=1.5 + spec:use_chain=2 + spec:allow_roots=1 ⇒ 9] · D=16` |
| 16 | $\frac{d}{dx}\left[\left(2x - 1\right)\left(3x^{3} + 6x^{2} + 10x - 2\right)\left(x^{2} + 7x - 9\right)\right]$ | $2\left(3x^{3} + 6x^{2} + 10x - 2\right)\left(x^{2} + 7x - 9\right) + \left(\left(9x^{2} + 12x + 10\right)\left(x^{2} + 7x - 9\right) + \left(2x + 7\right)\left(3x^{3} + 6x^{2} + 10x - 2\right)\right)\left(2x - 1\right)$ | `—` | `pack=deriv_product · methods=power,product · form_id=product_two_poly · dress=[spec_product_dress] · shape=product+sum+power · costs[form:product_two_poly=0 + dress:spec_product_dress=3 + spec:chain_depth_2=1.5 + spec:fn_power=1.5 + spec:use_chain=2 ⇒ 8] · D=16` |
| 20 | $\text{Find }\frac{d}{dx}\left(-\left(3x - 3\right)\left(2x^{\frac{2}{3}}\left(3x^{2}\right)\right)\right)$ | $-18x^{\frac{2}{3}}x^{2} + \left(6\frac{2}{3}x^{-\frac{1}{3}}x^{2} + 12xx^{\frac{2}{3}}\right)\left(3x - 3\right)$ | `—` | `pack=deriv_product · methods=power,product · form_id=product_two_poly · dress=[sign,spec_product_dress] · shape=product+power · costs[form:product_two_poly=0 + dress:spec_sign=0.5 + dress:spec_product_dress=3 + spec:chain_depth_2=1.5 + spec:fn_power=1.5 + spec:use_chain=2 + spec:allow_roots=1 ⇒ 9.5] · D=20` |
| 20 | $\text{Find }\frac{d}{dx}\left(-\left(2x^{3} + 3x^{2} - 5\right)\left(8x^{4}\right)\right)$ | $-8\left(6x^{2} + 6x\right)x^{4} + 32x^{3}\left(2x^{3} + 3x^{2} - 5\right)$ | `—` | `pack=deriv_product · methods=power,product · form_id=product_two_poly · dress=[sign] · shape=product+sum+power · costs[form:product_two_poly=0 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:fn_power=1.5 + spec:use_chain=2 ⇒ 5.5] · D=20` |
| 20 | $\frac{d}{dx}\left[\left(x + 3\right)\left(2x + 2\right)x^{\frac{5}{2}}\left(x^{3} + 7x^{2} - 2x + 8\right)\right]$ | $\left(2x + 2\right)x^{\frac{5}{2}}\left(x^{3} + 7x^{2} - 2x + 8\right) + \left(2x^{\frac{5}{2}}\left(x^{3} + 7x^{2} - 2x + 8\right) + \left(\frac{5}{2}x^{\frac{3}{2}}\left(x^{3} + 7x^{2} - 2x + 8\right) + \left(3x^{2} + 14x - 2\right)x^{\frac{5}{2}}\right)\left(2x + 2\right)\right)\left(x + 3\right)$ | `—` | `pack=deriv_product · methods=power,product · form_id=product_two_poly · dress=[spec_product_dress,spec_product_dress#2] · shape=product+sum+power · costs[form:product_two_poly=0 + dress:spec_product_dress=3 + dress:spec_product_dress#2=3 + spec:chain_depth_2=1.5 + spec:fn_power=1.5 + spec:use_chain=2 + spec:allow_roots=1 ⇒ 12] · D=20` |
| 25 | $\frac{d}{dx}\left[\left(x - 2\right)\left(-8x^{\frac{1}{2}}\right)\left(-2x^{\frac{2}{3}}\right)\right]$ | $16x^{\frac{1}{2}}x^{\frac{2}{3}} + \left(16\frac{1}{2}x^{-\frac{1}{2}}x^{\frac{2}{3}} + 16\frac{2}{3}x^{-\frac{1}{3}}x^{\frac{1}{2}}\right)\left(x - 2\right)$ | `—` | `pack=deriv_product · methods=power,product · form_id=product_two_poly · dress=[spec_product_dress] · shape=product+power · costs[form:product_two_poly=0 + dress:spec_product_dress=3 + spec:chain_depth_2=1.5 + spec:fn_power=1.5 + spec:use_chain=2 + spec:allow_roots=1 ⇒ 9] · D=25` |
| 25 | $\frac{d}{dx}\left[-12x^{\frac{5}{2}}\left(2x^{3} - 2x^{2} - 12x - 4\right)\right]$ | $-12\frac{5}{2}x^{\frac{3}{2}}\left(2x^{3} - 2x^{2} - 12x - 4\right) + 12\left(6x^{2} - 4x - 12\right)x^{\frac{5}{2}}$ | `—` | `pack=deriv_product · methods=power,product · form_id=product_two_poly · dress=[sign] · shape=product+sum+power · costs[form:product_two_poly=0 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:fn_power=1.5 + spec:use_chain=2 + spec:allow_roots=1 ⇒ 6.5] · D=25` |
| 25 | $\text{Find }\frac{d}{dx}\left(\left(x - 2\right)\left(3x - 3\right)\left(-13x^{\frac{7}{2}}\right)\left(10x^{\frac{2}{3}}\right)\right)$ | $-130\left(3x - 3\right)x^{\frac{7}{2}}x^{\frac{2}{3}} + \left(-390x^{\frac{7}{2}}x^{\frac{2}{3}} + \left(-130\frac{7}{2}x^{\frac{5}{2}}x^{\frac{2}{3}} - 130\frac{2}{3}x^{-\frac{1}{3}}x^{\frac{7}{2}}\right)\left(3x - 3\right)\right)\left(x - 2\right)$ | `—` | `pack=deriv_product · methods=power,product · form_id=product_two_poly · dress=[spec_product_dress,spec_product_dress#2] · shape=product+power · costs[form:product_two_poly=0 + dress:spec_product_dress=3 + dress:spec_product_dress#2=3 + spec:chain_depth_2=1.5 + spec:fn_power=1.5 + spec:use_chain=2 + spec:allow_roots=1 ⇒ 12] · D=25` |

## Derivatives — quotient rule

<a id="deriv_quotient"></a>

`calc_diff_quotient_rule` · pack `deriv_quotient` · topic label: c1: Quotient Rule · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **1** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `quotient_poly` | 24 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\frac{d}{dx}\left[\frac{2x - 1}{2x - 2}\right]$ | $\frac{\left(2\right)\left(2x - 2\right)-\left(2x - 1\right)\left(2\right)}{\left(2x - 2\right)^{2}}$ | `—` | `pack=deriv_quotient · methods=power,quotient,sum · form_id=quotient_poly · shape=quotient · costs[form:quotient_poly=0 ⇒ 0] · D=0` |
| 0 | $\text{Find }\frac{d}{dx}\left(\frac{2x + 1}{2x + 2}\right)$ | $\frac{\left(2\right)\left(2x + 2\right)-\left(2x + 1\right)\left(2\right)}{\left(2x + 2\right)^{2}}$ | `—` | `pack=deriv_quotient · methods=power,quotient,sum · form_id=quotient_poly · shape=quotient · costs[form:quotient_poly=0 ⇒ 0] · D=0` |
| 0 | $\frac{d}{dx}\left[\frac{x - 1}{x - 2}\right]$ | $\frac{\left(1\right)\left(x - 2\right)-\left(x - 1\right)\left(1\right)}{\left(x - 2\right)^{2}}$ | `—` | `pack=deriv_quotient · methods=power,quotient,sum · form_id=quotient_poly · shape=quotient · costs[form:quotient_poly=0 ⇒ 0] · D=0` |
| 3 | $\text{Find }\frac{d}{dx}\left(\frac{-2x^{4}}{x - 2}\right)$ | $\frac{\left(-8x^{3}\right)\left(x - 2\right)-\left(-2x^{4}\right)\left(1\right)}{\left(x - 2\right)^{2}}$ | `—` | `pack=deriv_quotient · methods=power,quotient,sum · form_id=quotient_poly · shape=quotient · costs[form:quotient_poly=0 ⇒ 0] · D=3` |
| 3 | $\text{Find }\frac{d}{dx}\left(\frac{-2x}{x + 2}\right)$ | $\frac{\left(-2\right)\left(x + 2\right)-\left(-2x\right)\left(1\right)}{\left(x + 2\right)^{2}}$ | `—` | `pack=deriv_quotient · methods=power,quotient,sum · form_id=quotient_poly · shape=quotient · costs[form:quotient_poly=0 ⇒ 0] · D=3` |
| 3 | $\frac{d}{dx}\left[\frac{x^{2} + 3x + 1}{x + 1}\right]$ | $\frac{\left(2x + 3\right)\left(x + 1\right)-\left(x^{2} + 3x + 1\right)\left(1\right)}{\left(x + 1\right)^{2}}$ | `—` | `pack=deriv_quotient · methods=power,quotient,sum · form_id=quotient_poly · shape=quotient · costs[form:quotient_poly=0 ⇒ 0] · D=3` |
| 6 | $\text{Find }\frac{d}{dx}\left(\frac{3x^{3} - x^{2} + 5x + 2}{5x + 5}\right)$ | $\frac{\left(9x^{2} - 2x + 5\right)\left(5x + 5\right)-\left(3x^{3} - x^{2} + 5x + 2\right)\left(5\right)}{\left(5x + 5\right)^{2}}$ | `—` | `pack=deriv_quotient · methods=power,quotient,sum · form_id=quotient_poly · shape=quotient · costs[form:quotient_poly=0 ⇒ 0] · D=6` |
| 6 | $\text{Find }\frac{d}{dx}\left(\frac{3x^{3} + 2x^{2} - x + 1}{5x - 1}\right)$ | $\frac{\left(9x^{2} + 4x - 1\right)\left(5x - 1\right)-\left(3x^{3} + 2x^{2} - x + 1\right)\left(5\right)}{\left(5x - 1\right)^{2}}$ | `—` | `pack=deriv_quotient · methods=power,quotient,sum · form_id=quotient_poly · shape=quotient · costs[form:quotient_poly=0 ⇒ 0] · D=6` |
| 6 | $\frac{d}{dx}\left[\frac{-5x^{4}}{5x + 3}\right]$ | $\frac{\left(-20x^{3}\right)\left(5x + 3\right)-\left(-5x^{4}\right)\left(5\right)}{\left(5x + 3\right)^{2}}$ | `—` | `pack=deriv_quotient · methods=power,quotient,sum · form_id=quotient_poly · shape=quotient · costs[form:quotient_poly=0 ⇒ 0] · D=6` |
| 8 | $\frac{d}{dx}\left[\frac{3x^{3} + 2x^{2} - 5x + 3}{5x + 5}\right]$ | $\frac{\left(9x^{2} + 4x - 5\right)\left(5x + 5\right)-\left(3x^{3} + 2x^{2} - 5x + 3\right)\left(5\right)}{\left(5x + 5\right)^{2}}$ | `—` | `pack=deriv_quotient · methods=power,quotient,sum · form_id=quotient_poly · shape=quotient · costs[form:quotient_poly=0 ⇒ 0] · D=8` |
| 8 | $\text{Find }\frac{d}{dx}\left(\frac{-2x}{4x + 1}\right)$ | $\frac{\left(-2\right)\left(4x + 1\right)-\left(-2x\right)\left(4\right)}{\left(4x + 1\right)^{2}}$ | `—` | `pack=deriv_quotient · methods=power,quotient,sum · form_id=quotient_poly · shape=quotient · costs[form:quotient_poly=0 ⇒ 0] · D=8` |
| 8 | $\text{Find }\frac{d}{dx}\left(\frac{x^{2} - x - 4}{2x + 1}\right)$ | $\frac{\left(2x - 1\right)\left(2x + 1\right)-\left(x^{2} - x - 4\right)\left(2\right)}{\left(2x + 1\right)^{2}}$ | `—` | `pack=deriv_quotient · methods=power,quotient,sum · form_id=quotient_poly · shape=quotient · costs[form:quotient_poly=0 ⇒ 0] · D=8` |
| 12 | $\frac{d}{dx}\left[\frac{x^{3} - x^{2} + 2x - 5}{x + 3}\right]$ | $\frac{\left(3x^{2} - 2x + 2\right)\left(x + 3\right)-\left(x^{3} - x^{2} + 2x - 5\right)\left(1\right)}{\left(x + 3\right)^{2}}$ | `—` | `pack=deriv_quotient · methods=power,quotient,sum · form_id=quotient_poly · shape=quotient · costs[form:quotient_poly=0 + spec:fn_power=1.5 + spec:use_chain=2 ⇒ 3.5] · D=12` |
| 12 | $\text{Find }\frac{d}{dx}\left(\frac{2x^{3} + 2x^{2} + 4}{4x - 1}\right)$ | $\frac{\left(6x^{2} + 4x\right)\left(4x - 1\right)-\left(2x^{3} + 2x^{2} + 4\right)\left(4\right)}{\left(4x - 1\right)^{2}}$ | `—` | `pack=deriv_quotient · methods=power,quotient,sum · form_id=quotient_poly · shape=quotient · costs[form:quotient_poly=0 + spec:fn_power=1.5 + spec:use_chain=2 ⇒ 3.5] · D=12` |
| 12 | $\frac{d}{dx}\left[\frac{2x^{2} + 5x + 3}{4x - 1}\right]$ | $\frac{\left(4x + 5\right)\left(4x - 1\right)-\left(2x^{2} + 5x + 3\right)\left(4\right)}{\left(4x - 1\right)^{2}}$ | `—` | `pack=deriv_quotient · methods=power,quotient,sum · form_id=quotient_poly · shape=quotient · costs[form:quotient_poly=0 + spec:fn_power=1.5 + spec:use_chain=2 ⇒ 3.5] · D=12` |
| 16 | $\text{Find }\frac{d}{dx}\left(\frac{-5x^{3}}{x + 3}\right)$ | $\frac{\left(-15x^{2}\right)\left(x + 3\right)-\left(-5x^{3}\right)\left(1\right)}{\left(x + 3\right)^{2}}$ | `—` | `pack=deriv_quotient · methods=power,quotient,sum · form_id=quotient_poly · shape=quotient · costs[form:quotient_poly=0 + spec:chain_depth_2=1.5 + spec:fn_power=1.5 + spec:use_chain=2 ⇒ 5] · D=16` |
| 16 | $\frac{d}{dx}\left[\frac{3x^{3} - x^{2} + 3x - 3}{2x - 4}\right]$ | $\frac{\left(9x^{2} - 2x + 3\right)\left(2x - 4\right)-\left(3x^{3} - x^{2} + 3x - 3\right)\left(2\right)}{\left(2x - 4\right)^{2}}$ | `—` | `pack=deriv_quotient · methods=power,quotient,sum · form_id=quotient_poly · shape=quotient · costs[form:quotient_poly=0 + spec:chain_depth_2=1.5 + spec:fn_power=1.5 + spec:use_chain=2 ⇒ 5] · D=16` |
| 16 | $\text{Find }\frac{d}{dx}\left(\frac{x^{2} - 5x - 1}{2x + 2}\right)$ | $\frac{\left(2x - 5\right)\left(2x + 2\right)-\left(x^{2} - 5x - 1\right)\left(2\right)}{\left(2x + 2\right)^{2}}$ | `—` | `pack=deriv_quotient · methods=power,quotient,sum · form_id=quotient_poly · shape=quotient · costs[form:quotient_poly=0 + spec:chain_depth_2=1.5 + spec:fn_power=1.5 + spec:use_chain=2 ⇒ 5] · D=16` |
| 20 | $\text{Find }\frac{d}{dx}\left(\frac{2x^{3} - x^{2} - 5x + 4}{3x - 1}\right)$ | $\frac{\left(6x^{2} - 2x - 5\right)\left(3x - 1\right)-\left(2x^{3} - x^{2} - 5x + 4\right)\left(3\right)}{\left(3x - 1\right)^{2}}$ | `—` | `pack=deriv_quotient · methods=power,quotient,sum · form_id=quotient_poly · shape=quotient · costs[form:quotient_poly=0 + spec:chain_depth_2=1.5 + spec:fn_power=1.5 + spec:use_chain=2 ⇒ 5] · D=20` |
| 20 | $\frac{d}{dx}\left[\frac{3x}{3x - 3}\right]$ | $\frac{\left(3\right)\left(3x - 3\right)-\left(3x\right)\left(3\right)}{\left(3x - 3\right)^{2}}$ | `—` | `pack=deriv_quotient · methods=power,quotient,sum · form_id=quotient_poly · shape=quotient · costs[form:quotient_poly=0 + spec:chain_depth_2=1.5 + spec:fn_power=1.5 + spec:use_chain=2 ⇒ 5] · D=20` |
| 20 | $\text{Find }\frac{d}{dx}\left(\frac{5x^{4}}{2x + 1}\right)$ | $\frac{\left(20x^{3}\right)\left(2x + 1\right)-\left(5x^{4}\right)\left(2\right)}{\left(2x + 1\right)^{2}}$ | `—` | `pack=deriv_quotient · methods=power,quotient,sum · form_id=quotient_poly · shape=quotient · costs[form:quotient_poly=0 + spec:chain_depth_2=1.5 + spec:fn_power=1.5 + spec:use_chain=2 ⇒ 5] · D=20` |
| 25 | $\text{Find }\frac{d}{dx}\left(\frac{2x^{3} - 3x^{2} - 6}{6x - 6}\right)$ | $\frac{\left(6x^{2} - 6x\right)\left(6x - 6\right)-\left(2x^{3} - 3x^{2} - 6\right)\left(6\right)}{\left(6x - 6\right)^{2}}$ | `—` | `pack=deriv_quotient · methods=power,quotient,sum · form_id=quotient_poly · shape=quotient · costs[form:quotient_poly=0 + spec:chain_depth_2=1.5 + spec:fn_power=1.5 + spec:use_chain=2 ⇒ 5] · D=25` |
| 25 | $\frac{d}{dx}\left[\frac{2x^{3} + 3x^{2} + 2x - 2}{6x + 4}\right]$ | $\frac{\left(6x^{2} + 6x + 2\right)\left(6x + 4\right)-\left(2x^{3} + 3x^{2} + 2x - 2\right)\left(6\right)}{\left(6x + 4\right)^{2}}$ | `—` | `pack=deriv_quotient · methods=power,quotient,sum · form_id=quotient_poly · shape=quotient · costs[form:quotient_poly=0 + spec:chain_depth_2=1.5 + spec:fn_power=1.5 + spec:use_chain=2 ⇒ 5] · D=25` |
| 25 | $\text{Find }\frac{d}{dx}\left(\frac{-4x^{3}}{4x - 2}\right)$ | $\frac{\left(-12x^{2}\right)\left(4x - 2\right)-\left(-4x^{3}\right)\left(4\right)}{\left(4x - 2\right)^{2}}$ | `—` | `pack=deriv_quotient · methods=power,quotient,sum · form_id=quotient_poly · shape=quotient · costs[form:quotient_poly=0 + spec:chain_depth_2=1.5 + spec:fn_power=1.5 + spec:use_chain=2 ⇒ 5] · D=25` |

## Derivatives — chain rule

<a id="deriv_chain"></a>

`calc_diff_chain_rule` · pack `deriv_chain` · topic label: c1: Chain Rule · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **2** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `chain_power_linear` | 15 |
| `chain_nested` | 9 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\frac{d}{dx}\left[\left(2x + 1\right)^{2}\right]$ | $2\left(2x + 1\right)\left(2\right)$ | `—` | `pack=deriv_chain · methods=chain,power · form_id=chain_nested · shape=sum+power · costs[form:chain_nested=12 + spec:chain_depth_2=1.5 ⇒ 13.5] · D=0` |
| 0 | $\text{Find }\frac{d}{dx}\left(\sqrt{9x + 1}\right)$ | $\frac{1}{2\sqrt{9x + 1}}\left(9\right)$ | `—` | `pack=deriv_chain · methods=chain,power · form_id=chain_power_linear · shape=fn:sqrt+sum · costs[form:chain_power_linear=4 + spec:allow_roots=1 ⇒ 5] · D=0` |
| 0 | $\frac{d}{dx}\left[\left(2x - 2\right)^{2}\right]$ | $2\left(2x - 2\right)\left(2\right)$ | `—` | `pack=deriv_chain · methods=chain,power · form_id=chain_nested · shape=sum+power · costs[form:chain_nested=12 + spec:chain_depth_2=1.5 ⇒ 13.5] · D=0` |
| 3 | $\text{Find }\frac{d}{dx}\left(\sqrt{4x + 1}\right)$ | $\frac{1}{2\sqrt{4x + 1}}\left(4\right)$ | `—` | `pack=deriv_chain · methods=chain,power · form_id=chain_power_linear · shape=fn:sqrt+sum · costs[form:chain_power_linear=4 + spec:allow_roots=1 ⇒ 5] · D=3` |
| 3 | $\text{Find }\frac{d}{dx}\left(\sqrt{3x}\right)$ | $\frac{3}{2\sqrt{3x}}$ | `—` | `pack=deriv_chain · methods=chain,power · form_id=chain_power_linear · shape=fn:sqrt · costs[form:chain_power_linear=4 + spec:allow_roots=1 ⇒ 5] · D=3` |
| 3 | $\frac{d}{dx}\left[\left(3x^{2} + 1\right)^{2}\right]$ | $2\left(3x^{2} + 1\right)\left(6x\right)$ | `—` | `pack=deriv_chain · methods=chain,power · form_id=chain_power_linear · shape=sum+power · costs[form:chain_power_linear=4 ⇒ 4] · D=3` |
| 6 | $\frac{d}{dx}\left[-\left(x^{2} + 1\right)^{\frac{3}{2}}\right]$ | $-2\frac{3}{2}\left(x^{2} + 1\right)^{\frac{1}{2}}x$ | `—` | `pack=deriv_chain · methods=chain,power · form_id=chain_power_linear · dress=[sign] · shape=sum+power · costs[form:chain_power_linear=4 + dress:spec_sign=0.5 + spec:use_product=2 + spec:allow_roots=1 ⇒ 7.5] · D=6` |
| 6 | $\frac{d}{dx}\left[-\sqrt{4x}\right]$ | $-4\frac{1}{2\sqrt{4x}}$ | `—` | `pack=deriv_chain · methods=chain,power · form_id=chain_power_linear · dress=[sign] · shape=fn:sqrt · costs[form:chain_power_linear=4 + dress:spec_sign=0.5 + spec:use_product=2 + spec:allow_roots=1 ⇒ 7.5] · D=6` |
| 6 | $\text{Find }\frac{d}{dx}\left(\sqrt{5x}\right)$ | $\frac{5}{2\sqrt{5x}}$ | `—` | `pack=deriv_chain · methods=chain,power · form_id=chain_power_linear · shape=fn:sqrt · costs[form:chain_power_linear=4 + spec:use_product=2 + spec:allow_roots=1 ⇒ 7] · D=6` |
| 8 | $\frac{d}{dx}\left[-3\left(x^{2} - 3\right)^{\pi}\right]$ | $-6\pi\left(x^{2} - 3\right)^{\pi-1}x$ | `—` | `pack=deriv_chain · methods=chain,power · form_id=chain_power_linear · dress=[constant_multiple] · shape=sum+power · costs[form:chain_power_linear=4 + dress:spec_scale=1.5 + spec:use_product=2 ⇒ 7.5] · D=8` |
| 8 | $\frac{d}{dx}\left[\sqrt{2x}\right]$ | $\frac{2}{2\sqrt{2x}}$ | `—` | `pack=deriv_chain · methods=chain,power · form_id=chain_power_linear · shape=fn:sqrt · costs[form:chain_power_linear=4 + spec:use_product=2 + spec:allow_roots=1 ⇒ 7] · D=8` |
| 8 | $\text{Find }\frac{d}{dx}\left(-\sqrt{4x + 1}\right)$ | $-4\frac{1}{2\sqrt{4x + 1}}$ | `—` | `pack=deriv_chain · methods=chain,power · form_id=chain_power_linear · dress=[sign] · shape=fn:sqrt+sum · costs[form:chain_power_linear=4 + dress:spec_sign=0.5 + spec:use_product=2 + spec:allow_roots=1 ⇒ 7.5] · D=8` |
| 12 | $\frac{d}{dx}\left[4\left(x^{2} - 4\right)^{\pi}\right]$ | $8\pi\left(x^{2} - 4\right)^{\pi-1}x$ | `—` | `pack=deriv_chain · methods=chain,power · form_id=chain_nested · dress=[sign,constant_multiple] · shape=sum+power · costs[form:chain_nested=12 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:chain_depth_2=1.5 + spec:use_product=2 ⇒ 17.5] · D=12` |
| 12 | $\frac{d}{dx}\left[-\left(2x^{2} + 5\right)^{-\frac{1}{2}}\right]$ | $-4\cdot\left(-\frac{1}{2}\left(2x^{2} + 5\right)^{-\frac{3}{2}}x\right)$ | `—` | `pack=deriv_chain · methods=chain,power · form_id=chain_nested · dress=[sign] · shape=sum+power · costs[form:chain_nested=12 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:use_product=2 + spec:allow_roots=1 ⇒ 17] · D=12` |
| 12 | $\frac{d^{2}}{dx^{2}}\left[-\left(2x^{2} - 6\right)^{2}\right]$ | $-32xx - 82x^{2} - 6$ | `—` | `pack=deriv_chain · methods=chain,power · form_id=chain_nested · dress=[sign] · shape=sum+power · costs[form:chain_nested=12 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:use_product=2 ⇒ 16] · D=12` |
| 16 | $\frac{d}{dx}\left[-\left(3x^{2} - 3\right)^{\sqrt{2}}\right]$ | $-6\sqrt{2}\left(3x^{2} - 3\right)^{\sqrt{2}-1}x$ | `—` | `pack=deriv_chain · methods=chain,power · form_id=chain_power_linear · dress=[sign] · shape=sum+power · costs[form:chain_power_linear=4 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:use_product=2 ⇒ 8] · D=16` |
| 16 | $\frac{d}{dx}\left[4\left(3x^{2} - 8\right)^{-\frac{1}{2}}\right]$ | $24\cdot\left(-\frac{1}{2}\left(3x^{2} - 8\right)^{-\frac{3}{2}}x\right)$ | `—` | `pack=deriv_chain · methods=chain,power · form_id=chain_nested · dress=[sign,constant_multiple] · shape=sum+power · costs[form:chain_nested=12 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:chain_depth_2=1.5 + spec:use_product=2 + spec:allow_roots=1 ⇒ 18.5] · D=16` |
| 16 | $\frac{d^{2}}{dx^{2}}\left[-\sqrt{9x + 4}\right]$ | $-81\cdot\left(-\frac{1}{4}\left(9x + 4\right)^{-\frac{3}{2}}\right)$ | `—` | `pack=deriv_chain · methods=chain,power · form_id=chain_nested · dress=[sign] · shape=fn:sqrt+sum · costs[form:chain_nested=12 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:use_product=2 + spec:allow_roots=1 ⇒ 17] · D=16` |
| 20 | $\text{Find }\frac{d}{dx}\left(-\left(2x^{2} - 9\right)^{\frac{5}{2}}\right)$ | $-4\frac{5}{2}\left(2x^{2} - 9\right)^{\frac{3}{2}}x$ | `—` | `pack=deriv_chain · methods=chain,power · form_id=chain_power_linear · dress=[sign] · shape=sum+power · costs[form:chain_power_linear=4 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:fn_power=1.5 + spec:use_product=2 + spec:allow_roots=1 ⇒ 10.5] · D=20` |
| 20 | $\text{Find }\frac{d}{dx}\left(-4\sqrt{\sqrt{9x + 8}}\right)$ | $-36\frac{1}{2\sqrt{\sqrt{9x + 8}}}\frac{1}{2\sqrt{9x + 8}}$ | `—` | `pack=deriv_chain · methods=chain,power · form_id=chain_nested · dress=[sign,constant_multiple] · shape=fn:sqrt+sum · costs[form:chain_nested=12 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:chain_depth_2=1.5 + spec:fn_power=1.5 + spec:use_product=2 + spec:allow_roots=1 + spec:nest_depth=2 ⇒ 22] · D=20` |
| 20 | $\text{Find }\frac{d}{dx}\left(-4\left(x^{2} - 7\right)^{\sqrt{3}}\right)$ | $-8\sqrt{3}\left(x^{2} - 7\right)^{\sqrt{3}-1}x$ | `—` | `pack=deriv_chain · methods=chain,power · form_id=chain_nested · dress=[sign,constant_multiple] · shape=sum+power · costs[form:chain_nested=12 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:chain_depth_2=1.5 + spec:fn_power=1.5 + spec:use_product=2 ⇒ 19] · D=20` |
| 25 | $\frac{d}{dx}\left[-\left(3x^{2} + 3\right)^{\frac{4}{3}}\right]$ | $-6\frac{4}{3}\left(3x^{2} + 3\right)^{\frac{1}{3}}x$ | `—` | `pack=deriv_chain · methods=chain,power · form_id=chain_power_linear · dress=[sign] · shape=sum+power · costs[form:chain_power_linear=4 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:fn_power=1.5 + spec:use_product=2 + spec:allow_roots=1 ⇒ 10.5] · D=25` |
| 25 | $\frac{d^{2}}{dx^{2}}\left[-\left(3x^{2} - 1\right)^{4}\right]$ | $-432\left(3x^{2} - 1\right)^{2}xx - 24\left(3x^{2} - 1\right)^{3}$ | `—` | `pack=deriv_chain · methods=chain,power · form_id=chain_power_linear · dress=[sign] · shape=sum+power · costs[form:chain_power_linear=4 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:fn_power=1.5 + spec:use_product=2 ⇒ 9.5] · D=25` |
| 25 | $\text{Find }\frac{d}{dx}\left(-4\left(x^{2} + 4\right)^{e}\right)$ | $-8e\left(x^{2} + 4\right)^{e-1}x$ | `—` | `pack=deriv_chain · methods=chain,power · form_id=chain_power_linear · dress=[sign,constant_multiple] · shape=sum+power · costs[form:chain_power_linear=4 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:chain_depth_2=1.5 + spec:fn_power=1.5 + spec:use_product=2 ⇒ 11] · D=25` |

## Derivatives — trigonometric

<a id="deriv_trig"></a>

`calc_diff_trigonometric` · pack `deriv_trig` · topic label: c1: Trigonometric · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **5** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `chain_trig_poly` | 9 |
| `trig_basic` | 6 |
| `product_poly_trig` | 5 |
| `quotient_trig_poly` | 3 |
| `trig_product_chain` | 1 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\frac{d}{dx}\left[\tan(2x)\right]$ | $2\sec^{2}(2x)$ | `—` | `pack=deriv_trig · methods=chain,power · form_id=trig_basic · shape=fn:tan · costs[form:trig_basic=0 + spec:chain=2 + spec:allow_trig=1.5 ⇒ 3.5] · D=0` |
| 0 | $\frac{d}{dx}\left[\tan(2x)\right]$ | $2\sec^{2}(2x)$ | `—` | `pack=deriv_trig · methods=chain,power · form_id=product_poly_trig · shape=fn:tan · costs[form:product_poly_trig=5 + spec:use_product=2 + spec:chain=2 + spec:allow_trig=1.5 ⇒ 10.5] · D=0` |
| 0 | $\text{Find }\frac{d}{dx}\left(\sin(2x)\right)$ | $2\cos(2x)$ | `—` | `pack=deriv_trig · methods=chain,power · form_id=quotient_trig_poly · shape=fn:sin · costs[form:quotient_trig_poly=6 + spec:class_trig=1.5 + spec:use_quotient=2.5 + spec:chain=2 + spec:allow_trig=1.5 ⇒ 13.5] · D=0` |
| 3 | $\text{Find }\frac{d}{dx}\left(\cos(3x)\right)$ | $-3\sin(3x)$ | `—` | `pack=deriv_trig · methods=chain,power · form_id=chain_trig_poly · shape=fn:cos · costs[form:chain_trig_poly=4 + spec:use_chain=2 + spec:chain=2 + spec:allow_trig=1.5 ⇒ 9.5] · D=3` |
| 3 | $\text{Find }\frac{d}{dx}\left(\cos(3x)\right)$ | $-3\sin(3x)$ | `—` | `pack=deriv_trig · methods=chain,power · form_id=trig_basic · shape=fn:cos · costs[form:trig_basic=0 + spec:chain=2 + spec:allow_trig=1.5 ⇒ 3.5] · D=3` |
| 3 | $\text{Find }\frac{d}{dx}\left(\sin(2x)\right)$ | $2\cos(2x)$ | `—` | `pack=deriv_trig · methods=chain,power · form_id=chain_trig_poly · shape=fn:sin · costs[form:chain_trig_poly=4 + spec:use_chain=2 + spec:chain=2 + spec:allow_trig=1.5 ⇒ 9.5] · D=3` |
| 6 | $\text{Find }\frac{d}{dx}\left(-\sin(2x)\right)$ | $-2\cos(2x)$ | `—` | `pack=deriv_trig · methods=chain,power · form_id=chain_trig_poly · dress=[sign] · shape=fn:sin · costs[form:chain_trig_poly=4 + dress:spec_sign=0.5 + spec:use_chain=2 + spec:use_product=2 + spec:chain=2 + spec:allow_trig=1.5 ⇒ 12] · D=6` |
| 6 | $\text{Find }\frac{d}{dx}\left(-\cos(4x)\right)$ | $4\sin(4x)$ | `—` | `pack=deriv_trig · methods=chain,power · form_id=chain_trig_poly · dress=[sign] · shape=fn:cos · costs[form:chain_trig_poly=4 + dress:spec_sign=0.5 + spec:use_chain=2 + spec:use_product=2 + spec:chain=2 + spec:allow_trig=1.5 ⇒ 12] · D=6` |
| 6 | $\frac{d}{dx}\left[-\sin(2x)\tan(3x)\right]$ | $-2\cos(2x)\tan(3x) + 3\sec^{2}(3x)\sin(2x)$ | `—` | `pack=deriv_trig · methods=chain,power,product · form_id=chain_trig_poly · dress=[sign] · shape=fn:sin+tan+product · costs[form:chain_trig_poly=4 + dress:spec_sign=0.5 + spec:use_chain=2 + spec:use_product=2 + spec:chain=2 + spec:product=2 + spec:allow_trig=1.5 ⇒ 14] · D=6` |
| 8 | $\frac{d}{dx}\left[\cos(4x)\sin(2x)\right]$ | $-4\sin(4x)\sin(2x) + 2\cos(2x)\cos(4x)$ | `—` | `pack=deriv_trig · methods=chain,power,product · form_id=trig_product_chain · shape=fn:cos+sin+product · costs[form:trig_product_chain=8 + spec:use_chain=2 + spec:use_product=2 + spec:chain=2 + spec:product=2 + spec:allow_trig=1.5 ⇒ 17.5] · D=8` |
| 8 | $\text{Find }\frac{d}{dx}\left(-\cos^{3}(3x)\right)$ | $9\cos^{2}(3x)\sin(3x)$ | `—` | `pack=deriv_trig · methods=chain,power · form_id=trig_basic · dress=[sign] · shape=fn:cos+fn_power+power · costs[form:trig_basic=0 + dress:spec_sign=0.5 + spec:use_chain=2 + spec:use_product=2 + spec:chain=2 + spec:allow_trig=1.5 + spec:nest_depth=2 ⇒ 10] · D=8` |
| 8 | $\text{Find }\frac{d}{dx}\left(-\tan\left(3x - 1\right)\right)$ | $-3\sec^{2}(3x - 1)$ | `—` | `pack=deriv_trig · methods=chain,power · form_id=product_poly_trig · dress=[sign] · shape=fn:tan+sum · costs[form:product_poly_trig=5 + dress:spec_sign=0.5 + spec:use_chain=2 + spec:use_product=2 + spec:chain=2 + spec:allow_trig=1.5 ⇒ 13] · D=8` |
| 12 | $\text{Find }\frac{d}{dx}\left(-\cos^{2}(x)\right)$ | $2\cos(x)\sin(x)$ | `—` | `pack=deriv_trig · methods=chain,power · form_id=trig_basic · dress=[sign] · shape=fn:cos+fn_power+power · costs[form:trig_basic=0 + dress:spec_sign=0.5 + spec:use_chain=2 + spec:use_product=2 + spec:use_quotient=2.5 + spec:chain=2 + spec:allow_trig=1.5 ⇒ 10.5] · D=12` |
| 12 | $\frac{d}{dx}\left[\left(3x - 2\right)\tan\left(\sin(2x)\right)\right]$ | $3\tan\left(\sin(2x)\right) + 2\sec^{2}(\sin(2x))\cos(2x)\left(3x - 2\right)$ | `—` | `pack=deriv_trig · methods=chain,power,product · form_id=product_poly_trig · dress=[spec_product_dress] · shape=fn:sin+tan · costs[form:product_poly_trig=5 + dress:spec_product_dress=3 + spec:use_chain=2 + spec:use_product=2 + spec:use_quotient=2.5 + spec:chain=2 + spec:product=2 + spec:allow_trig=1.5 + spec:nest_depth=2 ⇒ 22] · D=12` |
| 12 | $\text{Find }\frac{d}{dx}\left(-\tan(3x)\sin(2x)\right)$ | $-3\sec^{2}(3x)\sin(2x) + 2\cos(2x)\tan(3x)$ | `—` | `pack=deriv_trig · methods=chain,power,product · form_id=chain_trig_poly · dress=[sign] · shape=fn:sin+tan+product · costs[form:chain_trig_poly=4 + dress:spec_sign=0.5 + spec:use_chain=2 + spec:use_product=2 + spec:use_quotient=2.5 + spec:chain=2 + spec:product=2 + spec:allow_trig=1.5 ⇒ 16.5] · D=12` |
| 16 | $\frac{d}{dx}\left[2\cos(3x)\sin(4x)\left(-3x^{4}\right)\right]$ | $29\sin(3x)\sin(4x)x^{4} - 12\cos(4x)\cos(3x)x^{4} - 12x^{3}\cos(3x)\sin(4x)$ | `—` | `pack=deriv_trig · methods=chain,power,product · form_id=quotient_trig_poly · dress=[constant_multiple] · shape=fn:cos+sin+product+power · costs[form:quotient_trig_poly=6 + dress:spec_scale=1.5 + spec:chain_depth_2=1.5 + spec:class_trig=1.5 + spec:use_chain=2 + spec:use_product=2 + spec:use_quotient=2.5 + spec:chain=2 + spec:product=2 + spec:allow_trig=1.5 ⇒ 22.5] · D=16` |
| 16 | $\frac{d^{2}}{dx^{2}}\left[4\sin^{2}(x)\right]$ | $8\cos(x)\cos(x) - 8\sin(x)\sin(x)$ | `—` | `pack=deriv_trig · methods=chain,power · form_id=chain_trig_poly · dress=[sign,constant_multiple] · shape=fn:sin+fn_power+power · costs[form:chain_trig_poly=4 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:chain_depth_2=1.5 + spec:use_chain=2 + spec:use_product=2 + spec:use_quotient=2.5 + spec:chain=2 + spec:allow_trig=1.5 ⇒ 17.5] · D=16` |
| 16 | $\text{Find }\frac{d}{dx}\left(\left(x + 1\right)\left(2x - 1\right)\tan^{\frac{1}{2}}(10x)\right)$ | $\left(2x - 1\right)\tan^{\frac{1}{2}}(10x) + \left(2\tan^{\frac{1}{2}}(10x) + 10\frac{1}{2}\tan^{-\frac{1}{2}}(10x)\sec^{2}(10x)\left(2x - 1\right)\right)\left(x + 1\right)$ | `—` | `pack=deriv_trig · methods=chain,power,product · form_id=product_poly_trig · dress=[spec_product_dress,spec_product_dress#2] · shape=fn:tan+fn_power+power · costs[form:product_poly_trig=5 + dress:spec_product_dress=3 + dress:spec_product_dress#2=3 + spec:chain_depth_2=1.5 + spec:use_chain=2 + spec:use_product=2 + spec:use_quotient=2.5 + spec:chain=2 + spec:product=2 + spec:allow_roots=1 + spec:allow_trig=1.5 + spec:nest_depth=2 ⇒ 27.5] · D=16` |
| 20 | $\frac{d}{dx}\left[-2\cos^{3}(10x)\tan(9x)\right]$ | $-2\cdot\left(-30\cos^{2}(10x)\sin(10x)\tan(9x) + 9\sec^{2}(9x)\cos^{3}(10x)\right)$ | `—` | `pack=deriv_trig · methods=chain,power,product · form_id=quotient_trig_poly · dress=[sign,constant_multiple] · shape=fn:cos+tan+fn_power+product+power · costs[form:quotient_trig_poly=6 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:chain_depth_2=1.5 + spec:class_trig=1.5 + spec:use_chain=2 + spec:use_product=2 + spec:use_quotient=2.5 + spec:chain=2 + spec:product=2 + spec:allow_trig=1.5 + spec:nest_depth=2 ⇒ 25] · D=20` |
| 20 | $\frac{d^{2}}{dx^{2}}\left[-\tan\left(\cos(x)\right)\right]$ | $-2\sec^{2}(\cos(x))\tan\left(\cos(x)\right)\sin(x)\sin(x) + \cos(x)\sec^{2}(\cos(x))$ | `—` | `pack=deriv_trig · methods=chain,power · form_id=trig_basic · dress=[sign] · shape=fn:cos+tan · costs[form:trig_basic=0 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:class_trig=1.5 + spec:use_chain=2 + spec:use_product=2 + spec:use_quotient=2.5 + spec:chain=2 + spec:allow_trig=1.5 ⇒ 13.5] · D=20` |
| 20 | $\frac{d^{2}}{dx^{2}}\left[-\cos^{2}(x)\right]$ | $-2\sin(x)\sin(x) + 2\cos(x)\cos(x)$ | `—` | `pack=deriv_trig · methods=chain,power · form_id=trig_basic · dress=[sign] · shape=fn:cos+fn_power+power · costs[form:trig_basic=0 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:class_trig=1.5 + spec:use_chain=2 + spec:use_product=2 + spec:use_quotient=2.5 + spec:chain=2 + spec:allow_trig=1.5 ⇒ 13.5] · D=20` |
| 25 | $\frac{d}{dx}\left[-\cos^{4}\left(\cos(9x)\right)\tan^{2}(2x)\right]$ | $-36\cos^{3}\left(\cos(9x)\right)\sin\left(\cos(9x)\right)\sin(9x)\tan^{2}(2x) + 4\tan(2x)\sec^{2}(2x)\cos^{4}\left(\cos(9x)\right)$ | `—` | `pack=deriv_trig · methods=chain,power,product · form_id=product_poly_trig · dress=[sign] · shape=fn:cos+tan+fn_power+product+power · costs[form:product_poly_trig=5 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:class_trig=1.5 + spec:fn_power=1.5 + spec:use_chain=2 + spec:use_product=2 + spec:use_quotient=2.5 + spec:chain=2 + spec:product=2 + spec:allow_trig=1.5 + spec:nest_depth=3 ⇒ 25] · D=25` |
| 25 | $\text{Find }\frac{d}{dx}\left(-\tan^{2}\left(\sin(5x)\right)\right)$ | $-10\tan\left(\sin(5x)\right)\sec^{2}(\sin(5x))\cos(5x)$ | `—` | `pack=deriv_trig · methods=chain,power · form_id=chain_trig_poly · dress=[sign] · shape=fn:sin+tan+fn_power+power · costs[form:chain_trig_poly=4 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:class_trig=1.5 + spec:fn_power=1.5 + spec:use_chain=2 + spec:use_product=2 + spec:use_quotient=2.5 + spec:chain=2 + spec:allow_trig=1.5 + spec:nest_depth=3 ⇒ 22] · D=25` |
| 25 | $\frac{d^{2}}{dx^{2}}\left[2\cos(2x)\right]$ | $-8\cos(2x)$ | `—` | `pack=deriv_trig · methods=chain,power · form_id=chain_trig_poly · dress=[sign,constant_multiple] · shape=fn:cos · costs[form:chain_trig_poly=4 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:chain_depth_2=1.5 + spec:class_trig=1.5 + spec:fn_power=1.5 + spec:use_chain=2 + spec:use_product=2 + spec:use_quotient=2.5 + spec:chain=2 + spec:allow_trig=1.5 ⇒ 20.5] · D=25` |

## Derivatives — ln / exp

<a id="deriv_ln_exp"></a>

`calc_diff_natural_logarithms_and_exponentials` · pack `deriv_ln_exp` · topic label: c1: Natural logarithms and exponentials · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **6** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `product_poly_exp` | 8 |
| `exp_basic` | 5 |
| `ln_basic` | 3 |
| `ln_exp_product` | 3 |
| `quotient_log_poly` | 3 |
| `quotient_exp_poly` | 2 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\text{Find }\frac{d}{dx}\left(e^{x - 2}\right)$ | $e^{x - 2}$ | `—` | `pack=deriv_ln_exp · methods=chain,power · form_id=product_poly_exp · shape=fn:exp+sum · costs[form:product_poly_exp=5 + spec:use_product=2 + spec:chain=2 + spec:allow_exp=1.5 ⇒ 10.5] · D=0` |
| 0 | $\text{Find }\frac{d}{dx}\left(\ln\left(2x - 2\right)\right)$ | $\frac{1}{2x - 2}\left(2\right)$ | `—` | `pack=deriv_ln_exp · methods=chain,power · form_id=ln_basic · shape=fn:ln+sum · costs[form:ln_basic=0 + spec:chain=2 + spec:allow_log=1.5 ⇒ 3.5] · D=0` |
| 0 | $\frac{d}{dx}\left[e^{2x - 2}\right]$ | $e^{2x - 2}\left(2\right)$ | `—` | `pack=deriv_ln_exp · methods=chain,power · form_id=exp_basic · shape=fn:exp+sum · costs[form:exp_basic=0 + spec:chain=2 + spec:allow_exp=1.5 ⇒ 3.5] · D=0` |
| 3 | $\text{Find }\frac{d}{dx}\left(\ln\left(3x + 2\right)\right)$ | $\frac{1}{3x + 2}\left(3\right)$ | `—` | `pack=deriv_ln_exp · methods=chain,power · form_id=ln_basic · shape=fn:ln+sum · costs[form:ln_basic=0 + spec:chain=2 + spec:allow_log=1.5 ⇒ 3.5] · D=3` |
| 3 | $\text{Find }\frac{d}{dx}\left(\ln\left(x + 2\right)\right)$ | $\frac{1}{x + 2}$ | `—` | `pack=deriv_ln_exp · methods=chain,power · form_id=ln_basic · shape=fn:ln+sum · costs[form:ln_basic=0 + spec:chain=2 + spec:allow_log=1.5 ⇒ 3.5] · D=3` |
| 3 | $\frac{d}{dx}\left[e^{2x}\right]$ | $2e^{2x}$ | `—` | `pack=deriv_ln_exp · methods=chain,power · form_id=product_poly_exp · shape=fn:exp · costs[form:product_poly_exp=5 + spec:use_product=2 + spec:chain=2 + spec:allow_exp=1.5 ⇒ 10.5] · D=3` |
| 6 | $\text{Find }\frac{d}{dx}\left(e^{5x - 5}\ln\left(4x + 5\right)\right)$ | $5e^{5x - 5}\ln\left(4x + 5\right)+e^{5x - 5}\left(4\frac{1}{4x + 5}\right)$ | `—` | `pack=deriv_ln_exp · methods=chain,power,product · form_id=product_poly_exp · shape=fn:exp+ln+product+sum · costs[form:product_poly_exp=5 + spec:use_product=2 + spec:chain=2 + spec:product=2 + spec:allow_exp=1.5 + spec:allow_log=1.5 ⇒ 14] · D=6` |
| 6 | $\text{Find }\frac{d}{dx}\left(e^{x - 3}\right)$ | $e^{x - 3}$ | `—` | `pack=deriv_ln_exp · methods=chain,power · form_id=quotient_exp_poly · shape=fn:exp+sum · costs[form:quotient_exp_poly=6 + spec:class_exp=1.5 + spec:use_product=2 + spec:use_quotient=2.5 + spec:chain=2 + spec:allow_exp=1.5 ⇒ 15.5] · D=6` |
| 6 | $\frac{d}{dx}\left[\left(x + 3\right)e^{3x + 1}\right]$ | $e^{3x + 1} + 3e^{3x + 1}\left(x + 3\right)$ | `—` | `pack=deriv_ln_exp · methods=chain,power,product · form_id=product_poly_exp · dress=[spec_product_dress] · shape=fn:exp+sum · costs[form:product_poly_exp=5 + dress:spec_product_dress=3 + spec:use_product=2 + spec:chain=2 + spec:product=2 + spec:allow_exp=1.5 ⇒ 15.5] · D=6` |
| 8 | $\frac{d}{dx}\left[\ln^{2}\left(x - 2\right)\ln\left(4x - 3\right)\right]$ | $2\ln\left(x - 2\right)\frac{1}{x - 2}\ln\left(4x - 3\right)+\ln^{2}\left(x - 2\right)\left(4\frac{1}{4x - 3}\right)$ | `—` | `pack=deriv_ln_exp · methods=chain,power,product · form_id=product_poly_exp · shape=fn:ln+fn_power+product+sum+power · costs[form:product_poly_exp=5 + spec:use_chain=2 + spec:use_product=2 + spec:chain=2 + spec:product=2 + spec:allow_log=1.5 + spec:nest_depth=2 ⇒ 16.5] · D=8` |
| 8 | $\text{Find }\frac{d}{dx}\left(-\ln\left(3x - 4\right)\right)$ | $-3\frac{1}{3x - 4}$ | `—` | `pack=deriv_ln_exp · methods=chain,power · form_id=exp_basic · dress=[sign] · shape=fn:ln+sum · costs[form:exp_basic=0 + dress:spec_sign=0.5 + spec:use_chain=2 + spec:use_product=2 + spec:chain=2 + spec:allow_log=1.5 ⇒ 8] · D=8` |
| 8 | $\text{Find }\frac{d}{dx}\left(-\ln^{3}(2x)\right)$ | $-6\ln^{2}(2x)\frac{1}{2x}$ | `—` | `pack=deriv_ln_exp · methods=chain,power · form_id=exp_basic · dress=[sign] · shape=fn:ln+fn_power+power · costs[form:exp_basic=0 + dress:spec_sign=0.5 + spec:use_chain=2 + spec:use_product=2 + spec:chain=2 + spec:allow_log=1.5 + spec:nest_depth=2 ⇒ 10] · D=8` |
| 12 | $\text{Find }\frac{d}{dx}\left(-\ln\left(5x - 5\right)\right)$ | $-5\frac{1}{5x - 5}$ | `—` | `pack=deriv_ln_exp · methods=chain,power · form_id=quotient_log_poly · dress=[sign] · shape=fn:ln+sum · costs[form:quotient_log_poly=6 + dress:spec_sign=0.5 + spec:class_log=1.5 + spec:use_chain=2 + spec:use_product=2 + spec:use_quotient=2.5 + spec:chain=2 + spec:allow_log=1.5 ⇒ 18] · D=12` |
| 12 | $\frac{d}{dx}\left[-\ln\left(5x - 3\right)\ln^{3}\left(\ln\left(3x\right)\right)\right]$ | $-5\frac{1}{5x - 3}\ln^{3}\left(\ln\left(3x\right)\right) + 9\ln^{2}\left(\ln\left(3x\right)\right)\frac{1}{\ln\left(3x\right)}\frac{1}{3x}\ln\left(5x - 3\right)$ | `—` | `pack=deriv_ln_exp · methods=chain,power,product · form_id=exp_basic · dress=[sign] · shape=fn:ln+fn_power+product+sum+power · costs[form:exp_basic=0 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:use_chain=2 + spec:use_product=2 + spec:chain=2 + spec:product=2 + spec:allow_log=1.5 + spec:nest_depth=3 ⇒ 14.5] · D=12` |
| 12 | $\frac{d}{dx}\left[e^{2x - 4}e^{5x - 5}\right]$ | $2e^{2x - 4}e^{5x - 5} + 5e^{5x - 5}e^{2x - 4}$ | `—` | `pack=deriv_ln_exp · methods=chain,power,product · form_id=ln_exp_product · shape=fn:exp+product+sum · costs[form:ln_exp_product=10 + spec:chain_depth_2=1.5 + spec:use_chain=2 + spec:use_product=2 + spec:chain=2 + spec:product=2 + spec:allow_exp=1.5 ⇒ 21] · D=12` |
| 16 | $\frac{d}{dx}\left[2\ln^{\frac{1}{2}}\left(x + 9\right)\right]$ | $2\frac{1}{2}\ln^{-\frac{1}{2}}\left(x + 9\right)\frac{1}{x + 9}$ | `—` | `pack=deriv_ln_exp · methods=chain,power · form_id=quotient_log_poly · dress=[sign,constant_multiple] · shape=fn:ln+fn_power+sum+power · costs[form:quotient_log_poly=6 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:chain_depth_2=1.5 + spec:class_log=1.5 + spec:use_chain=2 + spec:use_product=2 + spec:use_quotient=2.5 + spec:chain=2 + spec:allow_log=1.5 + spec:allow_roots=1 + spec:nest_depth=2 ⇒ 24] · D=16` |
| 16 | $\frac{d}{dx}\left[-\ln^{2}(4x)\right]$ | $-8\ln\left(4x\right)\frac{1}{4x}$ | `—` | `pack=deriv_ln_exp · methods=chain,power · form_id=product_poly_exp · dress=[sign] · shape=fn:ln+fn_power+power · costs[form:product_poly_exp=5 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:class_exp=1.5 + spec:use_chain=2 + spec:use_product=2 + spec:chain=2 + spec:allow_log=1.5 + spec:nest_depth=2 ⇒ 18] · D=16` |
| 16 | $\text{Find }\frac{d}{dx}\left(\left(3x - 2\right)\left(x - 2\right)\ln^{2}\left(6x - 10\right)\right)$ | $3\left(x - 2\right)\ln^{2}\left(6x - 10\right) + \left(\ln^{2}\left(6x - 10\right) + 12\ln\left(6x - 10\right)\frac{1}{6x - 10}\left(x - 2\right)\right)\left(3x - 2\right)$ | `—` | `pack=deriv_ln_exp · methods=chain,power,product · form_id=product_poly_exp · dress=[spec_product_dress,spec_product_dress#2] · shape=fn:ln+fn_power+sum+power · costs[form:product_poly_exp=5 + dress:spec_product_dress=3 + dress:spec_product_dress#2=3 + spec:chain_depth_2=1.5 + spec:class_exp=1.5 + spec:use_chain=2 + spec:use_product=2 + spec:chain=2 + spec:product=2 + spec:allow_log=1.5 + spec:nest_depth=2 ⇒ 25.5] · D=16` |
| 20 | $\frac{d^{2}}{dx^{2}}\left[2\ln\left(8x - 3\right)e^{7x - 4}\right]$ | $2\cdot\left(-64\left(8x - 3\right)^{-2}e^{7x - 4} + 56e^{7x - 4}\frac{1}{8x - 3} + 49e^{7x - 4}\ln\left(8x - 3\right) + 56\frac{1}{8x - 3}e^{7x - 4}\right)$ | `—` | `pack=deriv_ln_exp · methods=chain,power,product · form_id=exp_basic · dress=[sign,constant_multiple] · shape=fn:exp+ln+product+sum · costs[form:exp_basic=0 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:chain_depth_2=1.5 + spec:class_exp=1.5 + spec:class_log=1.5 + spec:use_chain=2 + spec:use_product=2 + spec:chain=2 + spec:product=2 + spec:allow_exp=1.5 + spec:allow_log=1.5 ⇒ 17.5] · D=20` |
| 20 | $\frac{d}{dx}\left[-\ln\left(7x - 6\right)\ln^{4}\left(\ln\left(10x\right)\right)\right]$ | $-7\frac{1}{7x - 6}\ln^{4}\left(\ln\left(10x\right)\right) + 40\ln^{3}\left(\ln\left(10x\right)\right)\frac{1}{\ln\left(10x\right)}\frac{1}{10x}\ln\left(7x - 6\right)$ | `—` | `pack=deriv_ln_exp · methods=chain,power,product · form_id=quotient_log_poly · dress=[sign] · shape=fn:ln+fn_power+product+sum+power · costs[form:quotient_log_poly=6 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:class_exp=1.5 + spec:class_log=1.5 + spec:use_chain=2 + spec:use_product=2 + spec:use_quotient=2.5 + spec:chain=2 + spec:product=2 + spec:allow_log=1.5 + spec:nest_depth=3 ⇒ 26] · D=20` |
| 20 | $\text{Find }\frac{d}{dx}\left(\left(3x + 1\right)\left(2x + 1\right)\ln\left(\ln\left(x^{2}\right)\right)\right)$ | $3\left(2x + 1\right)\ln\left(\ln\left(x^{2}\right)\right) + \left(2\ln\left(\ln\left(x^{2}\right)\right) + 2\frac{1}{\ln\left(x^{2}\right)}\frac{1}{x^{2}}x\left(2x + 1\right)\right)\left(3x + 1\right)$ | `—` | `pack=deriv_ln_exp · methods=chain,power,product · form_id=product_poly_exp · dress=[spec_product_dress,spec_product_dress#2] · shape=fn:ln+power · costs[form:product_poly_exp=5 + dress:spec_product_dress=3 + dress:spec_product_dress#2=3 + spec:chain_depth_2=1.5 + spec:class_exp=1.5 + spec:class_log=1.5 + spec:use_chain=2 + spec:use_product=2 + spec:chain=2 + spec:product=2 + spec:allow_log=1.5 + spec:nest_depth=2 ⇒ 27] · D=20` |
| 25 | $\frac{d^{2}}{dx^{2}}\left[-2e^{10x - 4}e^{3x + 3}\right]$ | $-2100e^{10x - 4}e^{3x + 3} + 30e^{3x + 3}e^{10x - 4} + 9e^{3x + 3}e^{10x - 4} + 30e^{10x - 4}e^{3x + 3}$ | `—` | `pack=deriv_ln_exp · methods=chain,power,product · form_id=quotient_exp_poly · dress=[sign,constant_multiple] · shape=fn:exp+product+sum · costs[form:quotient_exp_poly=6 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:chain_depth_2=1.5 + spec:class_exp=1.5 + spec:class_log=1.5 + spec:mix_classes=1.5 + spec:use_chain=2 + spec:use_product=2 + spec:use_quotient=2.5 + spec:chain=2 + spec:product=2 + spec:allow_exp=1.5 ⇒ 26] · D=25` |
| 25 | $\text{Find }\frac{d}{dx}\left(-\left(2x - 3\right)e^{e^{x^{3}}}\right)$ | $-2e^{e^{x^{3}}} + 3e^{e^{x^{3}}}e^{x^{3}}x^{2}\left(2x - 3\right)$ | `—` | `pack=deriv_ln_exp · methods=chain,power,product · form_id=ln_exp_product · dress=[sign,spec_product_dress] · shape=fn:exp+power · costs[form:ln_exp_product=10 + dress:spec_sign=0.5 + dress:spec_product_dress=3 + spec:chain_depth_2=1.5 + spec:class_exp=1.5 + spec:class_log=1.5 + spec:fn_power=1.5 + spec:mix_classes=1.5 + spec:use_chain=2 + spec:use_product=2 + spec:chain=2 + spec:product=2 + spec:allow_exp=1.5 + spec:nest_depth=2 ⇒ 32.5] · D=25` |
| 25 | $\frac{d^{2}}{dx^{2}}\left[3e^{7x - 3}\right]$ | $147e^{7x - 3}$ | `—` | `pack=deriv_ln_exp · methods=chain,power · form_id=ln_exp_product · dress=[constant_multiple] · shape=fn:exp+sum · costs[form:ln_exp_product=10 + dress:spec_scale=1.5 + spec:chain_depth_2=1.5 + spec:class_exp=1.5 + spec:class_log=1.5 + spec:fn_power=1.5 + spec:mix_classes=1.5 + spec:use_chain=2 + spec:use_product=2 + spec:chain=2 + spec:allow_exp=1.5 ⇒ 26.5] · D=25` |

## Derivatives — inverse trig

<a id="deriv_invtrig"></a>

`calc_diff_inverse_trigonometric` · pack `deriv_invtrig` · topic label: c1: Inverse trigonometric · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **3** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `invtrig_arctan` | 13 |
| `invtrig_chained` | 7 |
| `invtrig_arcsin` | 4 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\frac{d}{dx}\left[\arccos(x)\right]$ | $-\frac{1}{\sqrt{1-x^{2}}}$ | `—` | `pack=deriv_invtrig · methods=power · form_id=invtrig_arctan · shape=fn:arccos · costs[form:invtrig_arctan=2 + spec:allow_invtrig=2 ⇒ 4] · D=0` |
| 0 | $\text{Find }\frac{d}{dx}\left(\arctan(x)\right)$ | $\frac{1}{1+x^{2}}$ | `—` | `pack=deriv_invtrig · methods=power · form_id=invtrig_arctan · shape=fn:arctan · costs[form:invtrig_arctan=2 + spec:allow_invtrig=2 ⇒ 4] · D=0` |
| 0 | $\text{Find }\frac{d}{dx}\left(\arctan(x)\right)$ | $\frac{1}{1+x^{2}}$ | `—` | `pack=deriv_invtrig · methods=power · form_id=invtrig_arctan · shape=fn:arctan · costs[form:invtrig_arctan=2 + spec:allow_invtrig=2 ⇒ 4] · D=0` |
| 3 | $\frac{d}{dx}\left[\arcsin(x)\right]$ | $\frac{1}{\sqrt{1-x^{2}}}$ | `—` | `pack=deriv_invtrig · methods=power · form_id=invtrig_arctan · shape=fn:arcsin · costs[form:invtrig_arctan=2 + spec:allow_invtrig=2 ⇒ 4] · D=3` |
| 3 | $\frac{d}{dx}\left[\arctan(x)\right]$ | $\frac{1}{1+x^{2}}$ | `—` | `pack=deriv_invtrig · methods=power · form_id=invtrig_arctan · shape=fn:arctan · costs[form:invtrig_arctan=2 + spec:allow_invtrig=2 ⇒ 4] · D=3` |
| 3 | $\text{Find }\frac{d}{dx}\left(\arctan(x)\right)$ | $\frac{1}{1+x^{2}}$ | `—` | `pack=deriv_invtrig · methods=power · form_id=invtrig_arctan · shape=fn:arctan · costs[form:invtrig_arctan=2 + spec:allow_invtrig=2 ⇒ 4] · D=3` |
| 6 | $\text{Find }\frac{d}{dx}\left(-\arcsin(x)\arccos(x)\right)$ | $-\frac{1}{\sqrt{1-(x)^{2}}}\arccos(x) + \left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\arcsin(x)$ | `—` | `pack=deriv_invtrig · methods=power,product · form_id=invtrig_arctan · dress=[sign] · shape=fn:arccos+arcsin+product · costs[form:invtrig_arctan=2 + dress:spec_sign=0.5 + spec:use_chain=2 + spec:product=2 + spec:allow_invtrig=2 ⇒ 8.5] · D=6` |
| 6 | $\frac{d}{dx}\left[\arctan(x)\arctan(x)\right]$ | $\frac{1}{1+(x)^{2}}\arctan(x) + \frac{1}{1+(x)^{2}}\arctan(x)$ | `—` | `pack=deriv_invtrig · methods=power,product · form_id=invtrig_arctan · shape=fn:arctan+product · costs[form:invtrig_arctan=2 + spec:use_chain=2 + spec:product=2 + spec:allow_invtrig=2 ⇒ 8] · D=6` |
| 6 | $\frac{d}{dx}\left[-\arccos(x)\arcsin(x)\right]$ | $-\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\arcsin(x) + \frac{1}{\sqrt{1-(x)^{2}}}\arccos(x)$ | `—` | `pack=deriv_invtrig · methods=power,product · form_id=invtrig_arctan · dress=[sign] · shape=fn:arccos+arcsin+product · costs[form:invtrig_arctan=2 + dress:spec_sign=0.5 + spec:use_chain=2 + spec:product=2 + spec:allow_invtrig=2 ⇒ 8.5] · D=6` |
| 8 | $\text{Find }\frac{d}{dx}\left(-\arccos^{2}(2x)\right)$ | $-4\arccos(2x)\left(-\frac{1}{\sqrt{1-(2x)^{2}}}\right)$ | `—` | `pack=deriv_invtrig · methods=chain,power · form_id=invtrig_chained · dress=[sign] · shape=fn:arccos+fn_power+power · costs[form:invtrig_chained=8 + dress:spec_sign=0.5 + spec:fn_power=1.5 + spec:use_chain=2 + spec:chain=2 + spec:allow_invtrig=2 + spec:nest_depth=2 ⇒ 18] · D=8` |
| 8 | $\text{Find }\frac{d}{dx}\left(\arcsin(x)\arccos^{3}(5x)\right)$ | $\frac{1}{\sqrt{1-(x)^{2}}}\arccos^{3}(5x) + 15\arccos^{2}(5x)\left(-\frac{1}{\sqrt{1-(5x)^{2}}}\right)\arcsin(x)$ | `—` | `pack=deriv_invtrig · methods=chain,power,product · form_id=invtrig_chained · shape=fn:arccos+arcsin+fn_power+product+power · costs[form:invtrig_chained=8 + spec:fn_power=1.5 + spec:use_chain=2 + spec:chain=2 + spec:product=2 + spec:allow_invtrig=2 + spec:nest_depth=2 ⇒ 19.5] · D=8` |
| 8 | $\frac{d}{dx}\left[\arctan^{3}(x)\right]$ | $3\left(\arctan(x)\right)^{2}\left(\frac{1}{1+x^{2}}\right)$ | `—` | `pack=deriv_invtrig · methods=chain,power · form_id=invtrig_arctan · shape=fn:arctan+fn_power+power · costs[form:invtrig_arctan=2 + spec:fn_power=1.5 + spec:use_chain=2 + spec:chain=2 + spec:allow_invtrig=2 ⇒ 9.5] · D=8` |
| 12 | $\frac{d}{dx}\left[-\arcsin(x)\arccos^{3}\left(\arcsin\left(x^{2}\right)\right)\right]$ | $-\frac{1}{\sqrt{1-(x)^{2}}}\arccos^{3}\left(\arcsin\left(x^{2}\right)\right) + 6\arccos^{2}\left(\arcsin\left(x^{2}\right)\right)\left(-\frac{1}{\sqrt{1-(\arcsin\left(x^{2}\right))^{2}}}\right)\frac{1}{\sqrt{1-(x^{2})^{2}}}x\arcsin(x)$ | `—` | `pack=deriv_invtrig · methods=chain,power,product · form_id=invtrig_arcsin · dress=[sign] · shape=fn:arccos+arcsin+fn_power+product+power · costs[form:invtrig_arcsin=2 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:fn_power=1.5 + spec:use_chain=2 + spec:chain=2 + spec:product=2 + spec:allow_invtrig=2 + spec:nest_depth=3 ⇒ 16.5] · D=12` |
| 12 | $\frac{d}{dx}\left[-\arctan^{3}(4x)\arcsin(x)\right]$ | $-12\arctan^{2}(4x)\frac{1}{1+(4x)^{2}}\arcsin(x) + \frac{1}{\sqrt{1-(x)^{2}}}\arctan^{3}(4x)$ | `—` | `pack=deriv_invtrig · methods=chain,power,product · form_id=invtrig_chained · dress=[sign] · shape=fn:arcsin+arctan+fn_power+product+power · costs[form:invtrig_chained=8 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:fn_power=1.5 + spec:use_chain=2 + spec:chain=2 + spec:product=2 + spec:allow_invtrig=2 + spec:nest_depth=2 ⇒ 21.5] · D=12` |
| 12 | $\text{Find }\frac{d}{dx}\left(\arccos^{2}(2x)\right)$ | $2\left(\arccos(2x)\right)\left(-\frac{2}{\sqrt{1-(2x)^{2}}}\right)$ | `—` | `pack=deriv_invtrig · methods=chain,power · form_id=invtrig_arcsin · shape=fn:arccos+fn_power+power · costs[form:invtrig_arcsin=2 + spec:chain_depth_2=1.5 + spec:fn_power=1.5 + spec:use_chain=2 + spec:chain=2 + spec:allow_invtrig=2 + spec:nest_depth=2 ⇒ 13] · D=12` |
| 16 | $\frac{d^{2}}{dx^{2}}\left[-\arccos(x)\arcsin(x)\right]$ | $+x\left(-x^{2} + 1\right)^{-\frac{3}{2}}\arcsin(x) + \frac{1}{\sqrt{1-(x)^{2}}}\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right) + x\left(-x^{2} + 1\right)^{-\frac{3}{2}}\arccos(x) + \left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\frac{1}{\sqrt{1-(x)^{2}}}$ | `—` | `pack=deriv_invtrig · methods=power,product · form_id=invtrig_arctan · dress=[sign] · shape=fn:arccos+arcsin+product · costs[form:invtrig_arctan=2 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:use_chain=2 + spec:product=2 + spec:allow_invtrig=2 ⇒ 10] · D=16` |
| 16 | $\frac{d}{dx}\left[-\arccos^{3}(2x)\arcsin(x)\right]$ | $-6\arccos^{2}(2x)\left(-\frac{1}{\sqrt{1-(2x)^{2}}}\right)\arcsin(x) + \frac{1}{\sqrt{1-(x)^{2}}}\arccos^{3}(2x)$ | `—` | `pack=deriv_invtrig · methods=chain,power,product · form_id=invtrig_arcsin · dress=[sign] · shape=fn:arccos+arcsin+fn_power+product+power · costs[form:invtrig_arcsin=2 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:use_chain=2 + spec:chain=2 + spec:product=2 + spec:allow_invtrig=2 + spec:nest_depth=2 ⇒ 14] · D=16` |
| 16 | $\frac{d}{dx}\left[-\arcsin(x)\left(-4x^{2}\right)\arctan^{2}(x)\right]$ | $+4\frac{1}{\sqrt{1-(x)^{2}}}x^{2}\arctan^{2}(x) - 8x\arcsin(x)\arctan^{2}(x) - 8\arctan(x)\frac{1}{1+(x)^{2}}\arcsin(x)x^{2}$ | `—` | `pack=deriv_invtrig · methods=chain,power,product · form_id=invtrig_arctan · dress=[sign] · shape=fn:arcsin+arctan+fn_power+product+power · costs[form:invtrig_arctan=2 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:use_chain=2 + spec:chain=2 + spec:product=2 + spec:allow_invtrig=2 ⇒ 12] · D=16` |
| 20 | $\frac{d}{dx}\left[-\arctan^{2}\left(\arctan\left(4x + 10\right)\right)\arcsin^{3}(4x)\right]$ | $-8\arctan\left(\arctan\left(4x + 10\right)\right)\frac{1}{1+(\arctan\left(4x + 10\right))^{2}}\frac{1}{1+(4x + 10)^{2}}\arcsin^{3}(4x) + 12\arcsin^{2}(4x)\frac{1}{\sqrt{1-(4x)^{2}}}\arctan^{2}\left(\arctan\left(4x + 10\right)\right)$ | `—` | `pack=deriv_invtrig · methods=chain,power,product · form_id=invtrig_chained · dress=[sign] · shape=fn:arcsin+arctan+fn_power+product+sum+power · costs[form:invtrig_chained=8 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:fn_power=1.5 + spec:use_chain=2 + spec:chain=2 + spec:product=2 + spec:allow_invtrig=2 + spec:nest_depth=3 ⇒ 22.5] · D=20` |
| 20 | $\frac{d}{dx}\left[-\arccos(x)\arccos(x)\right]$ | $-\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\arccos(x) + \left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\arccos(x)$ | `—` | `pack=deriv_invtrig · methods=power,product · form_id=invtrig_chained · dress=[sign] · shape=fn:arccos+product · costs[form:invtrig_chained=8 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:fn_power=1.5 + spec:use_chain=2 + spec:product=2 + spec:allow_invtrig=2 ⇒ 17.5] · D=20` |
| 20 | $\frac{d^{2}}{dx^{2}}\left[-\arctan^{2}(x)\right]$ | $-2\frac{1}{1+(x)^{2}}\frac{1}{1+(x)^{2}} + 4x\left(x^{2} + 1\right)^{-2}\arctan(x)$ | `—` | `pack=deriv_invtrig · methods=chain,power · form_id=invtrig_arcsin · dress=[sign] · shape=fn:arctan+fn_power+power · costs[form:invtrig_arcsin=2 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:fn_power=1.5 + spec:use_chain=2 + spec:chain=2 + spec:allow_invtrig=2 ⇒ 11.5] · D=20` |
| 25 | $\frac{d^{2}}{dx^{2}}\left[-3\arcsin^{2}(x)\right]$ | $-6\frac{1}{\sqrt{1-(x)^{2}}}\frac{1}{\sqrt{1-(x)^{2}}} - 6x\left(-x^{2} + 1\right)^{-\frac{3}{2}}\arcsin(x)$ | `—` | `pack=deriv_invtrig · methods=chain,power · form_id=invtrig_chained · dress=[sign,constant_multiple] · shape=fn:arcsin+fn_power+power · costs[form:invtrig_chained=8 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:chain_depth_2=1.5 + spec:fn_power=1.5 + spec:use_chain=2 + spec:chain=2 + spec:allow_invtrig=2 ⇒ 19] · D=25` |
| 25 | $\frac{d^{2}}{dx^{2}}\left[-\arccos^{\frac{1}{2}}(x)\right]$ | $+\frac{1}{2}\arccos^{-\frac{3}{2}}(x)\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\frac{1}{2}\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right) + x\left(-x^{2} + 1\right)^{-\frac{3}{2}}\frac{1}{2}\arccos^{-\frac{1}{2}}(x)$ | `—` | `pack=deriv_invtrig · methods=chain,power · form_id=invtrig_arctan · dress=[sign] · shape=fn:arccos+fn_power+power · costs[form:invtrig_arctan=2 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:fn_power=1.5 + spec:use_chain=2 + spec:chain=2 + spec:allow_invtrig=2 + spec:allow_roots=1 ⇒ 12.5] · D=25` |
| 25 | $\frac{d^{2}}{dx^{2}}\left[-2\arcsin^{2}(x)\right]$ | $-4\frac{1}{\sqrt{1-(x)^{2}}}\frac{1}{\sqrt{1-(x)^{2}}} - 4x\left(-x^{2} + 1\right)^{-\frac{3}{2}}\arcsin(x)$ | `—` | `pack=deriv_invtrig · methods=chain,power · form_id=invtrig_chained · dress=[sign,constant_multiple] · shape=fn:arcsin+fn_power+power · costs[form:invtrig_chained=8 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:chain_depth_2=1.5 + spec:fn_power=1.5 + spec:use_chain=2 + spec:chain=2 + spec:allow_invtrig=2 ⇒ 19] · D=25` |

## Derivatives — higher order

<a id="deriv_higher"></a>

`calc_diff_higher_order_derivatives` · pack `deriv_higher` · topic label: c1: Higher order derivatives · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **3** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `power_poly` | 11 |
| `higher_order_3` | 7 |
| `higher_order_2` | 6 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\frac{d^{2}}{dx^{2}}\left[2x^{2}\right]$ | $4$ | `—` | `pack=deriv_higher · methods=power · form_id=power_poly · shape=power · costs[form:power_poly=0 ⇒ 0] · D=0` |
| 0 | $\frac{d^{2}}{dx^{2}}\left[x^{2}\right]$ | $2$ | `—` | `pack=deriv_higher · methods=power · form_id=power_poly · shape=power · costs[form:power_poly=0 ⇒ 0] · D=0` |
| 0 | $\frac{d^{2}}{dx^{2}}\left[2x^{2}\right]$ | $4$ | `—` | `pack=deriv_higher · methods=power · form_id=power_poly · shape=power · costs[form:power_poly=0 ⇒ 0] · D=0` |
| 3 | $\frac{d^{2}}{dx^{2}}\left[3x^{3} + 2x^{2} - x - 1\right]$ | $18x + 4$ | `—` | `pack=deriv_higher · methods=power,sum · form_id=power_poly · shape=sum+power · costs[form:power_poly=0 ⇒ 0] · D=3` |
| 3 | $\frac{d^{2}}{dx^{2}}\left[2x^{3} + 3x^{2} - 2x\right]$ | $12x + 6$ | `—` | `pack=deriv_higher · methods=power,sum · form_id=power_poly · shape=sum+power · costs[form:power_poly=0 ⇒ 0] · D=3` |
| 3 | $\frac{d^{2}}{dx^{2}}\left[2x^{3} - 3x^{2} - 3x - 2\right]$ | $12x - 6$ | `—` | `pack=deriv_higher · methods=power,sum · form_id=power_poly · shape=sum+power · costs[form:power_poly=0 ⇒ 0] · D=3` |
| 6 | $\frac{d^{2}}{dx^{2}}\left[-\sin(2x)\right]$ | $4\sin(2x)$ | `—` | `pack=deriv_higher · methods=chain,power · form_id=higher_order_2 · dress=[sign] · shape=fn:sin · costs[form:higher_order_2=4 + dress:spec_sign=0.5 + spec:use_chain=2 + spec:chain=2 + spec:allow_trig=1.5 ⇒ 10] · D=6` |
| 6 | $\frac{d^{2}}{dx^{2}}\left[-e^{4x + 3}\right]$ | $-16e^{4x + 3}$ | `—` | `pack=deriv_higher · methods=chain,power · form_id=higher_order_2 · dress=[sign] · shape=fn:exp+sum · costs[form:higher_order_2=4 + dress:spec_sign=0.5 + spec:use_chain=2 + spec:chain=2 + spec:allow_exp=1.5 ⇒ 10] · D=6` |
| 6 | $\frac{d^{2}}{dx^{2}}\left[e^{2x + 2}\right]$ | $4e^{\left(2x + 2\right)}$ | `—` | `pack=deriv_higher · methods=chain,power · form_id=higher_order_2 · shape=fn:exp+sum · costs[form:higher_order_2=4 + spec:use_chain=2 + spec:chain=2 + spec:allow_exp=1.5 ⇒ 9.5] · D=6` |
| 8 | $\frac{d^{2}}{dx^{2}}\left[-\left(2x + 3\right)^{2}\right]$ | $-8$ | `—` | `pack=deriv_higher · methods=chain,power · form_id=power_poly · dress=[sign] · shape=sum+power · costs[form:power_poly=0 + dress:spec_sign=0.5 + spec:class_trig=1.5 + spec:use_chain=2 + spec:chain=2 ⇒ 6] · D=8` |
| 8 | $\frac{d^{2}}{dx^{2}}\left[-\sin(5x)e^{2x - 5}\right]$ | $+25\sin(5x)e^{2x - 5} + 10e^{2x - 5}\cos(5x) + 4e^{2x - 5}\sin(5x) + 10\cos(5x)e^{2x - 5}$ | `—` | `pack=deriv_higher · methods=chain,power,product · form_id=higher_order_2 · dress=[sign] · shape=fn:exp+sin+product+sum · costs[form:higher_order_2=4 + dress:spec_sign=0.5 + spec:class_trig=1.5 + spec:use_chain=2 + spec:chain=2 + spec:product=2 + spec:allow_exp=1.5 + spec:allow_trig=1.5 ⇒ 15] · D=8` |
| 8 | $\frac{d^{2}}{dx^{2}}\left[\tan^{2}(x)\right]$ | $2\sec^{2}(x)\sec^{2}(x) + 4\sec^{2}(x)\tan(x)\tan(x)$ | `—` | `pack=deriv_higher · methods=chain,power · form_id=power_poly · shape=fn:tan+fn_power+power · costs[form:power_poly=0 + spec:class_trig=1.5 + spec:use_chain=2 + spec:chain=2 + spec:allow_trig=1.5 ⇒ 7] · D=8` |
| 12 | $\frac{d^{3}}{dx^{3}}\left[e^{4x}\right]$ | $64e^{4x}$ | `—` | `pack=deriv_higher · methods=chain,power · form_id=higher_order_3 · shape=fn:exp · costs[form:higher_order_3=10 + spec:chain_depth_2=1.5 + spec:class_trig=1.5 + spec:use_chain=2 + spec:chain=2 + spec:allow_exp=1.5 ⇒ 18.5] · D=12` |
| 12 | $\frac{d^{2}}{dx^{2}}\left[-\cos(3x)\right]$ | $9\cos(3x)$ | `—` | `pack=deriv_higher · methods=chain,power · form_id=higher_order_2 · dress=[sign] · shape=fn:cos · costs[form:higher_order_2=4 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:class_trig=1.5 + spec:use_chain=2 + spec:chain=2 + spec:allow_trig=1.5 ⇒ 13] · D=12` |
| 12 | $\frac{d^{2}}{dx^{2}}\left[-\sin\left(e^{x}\right)\right]$ | $\sin\left(e^{x}\right)e^{x}e^{x} - e^{x}\cos\left(e^{x}\right)$ | `—` | `pack=deriv_higher · methods=chain,power · form_id=power_poly · dress=[sign] · shape=fn:exp+sin · costs[form:power_poly=0 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:class_trig=1.5 + spec:use_chain=2 + spec:chain=2 + spec:allow_exp=1.5 + spec:allow_trig=1.5 ⇒ 10.5] · D=12` |
| 16 | $\frac{d^{2}}{dx^{2}}\left[-e^{3x + 6}\right]$ | $-9e^{3x + 6}$ | `—` | `pack=deriv_higher · methods=chain,power · form_id=power_poly · dress=[sign] · shape=fn:exp+sum · costs[form:power_poly=0 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:class_exp=1.5 + spec:class_trig=1.5 + spec:use_chain=2 + spec:chain=2 + spec:allow_exp=1.5 ⇒ 10.5] · D=16` |
| 16 | $\frac{d^{3}}{dx^{3}}\left[3\left(3x^{2} - 3\right)^{3}\right]$ | $3888xxx + 648\left(3x^{2} - 3\right)x + 648\left(3x^{2} - 3\right)x + 648\left(3x^{2} - 3\right)x$ | `—` | `pack=deriv_higher · methods=chain,power · form_id=higher_order_3 · dress=[sign,constant_multiple] · shape=sum+power · costs[form:higher_order_3=10 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:chain_depth_2=1.5 + spec:class_exp=1.5 + spec:class_trig=1.5 + spec:use_chain=2 + spec:chain=2 ⇒ 20.5] · D=16` |
| 16 | $\frac{d^{3}}{dx^{3}}\left[3\cos(2x)\right]$ | $24\sin(2x)$ | `—` | `pack=deriv_higher · methods=chain,power · form_id=higher_order_3 · dress=[sign,constant_multiple] · shape=fn:cos · costs[form:higher_order_3=10 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:chain_depth_2=1.5 + spec:class_exp=1.5 + spec:class_trig=1.5 + spec:use_chain=2 + spec:chain=2 + spec:allow_trig=1.5 ⇒ 22] · D=16` |
| 20 | $\frac{d^{3}}{dx^{3}}\left[-e^{6x + 7}\right]$ | $-216e^{6x + 7}$ | `—` | `pack=deriv_higher · methods=chain,power · form_id=higher_order_3 · dress=[sign] · shape=fn:exp+sum · costs[form:higher_order_3=10 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:class_exp=1.5 + spec:class_trig=1.5 + spec:fn_power=1.5 + spec:mix_classes=1.5 + spec:use_chain=2 + spec:chain=2 + spec:allow_exp=1.5 ⇒ 23.5] · D=20` |
| 20 | $\frac{d^{2}}{dx^{2}}\left[-e^{\cos(x)}\right]$ | $-e^{\cos(x)}\sin(x)\sin(x) + \cos(x)e^{\cos(x)}$ | `—` | `pack=deriv_higher · methods=chain,power · form_id=higher_order_2 · dress=[sign] · shape=fn:cos+exp · costs[form:higher_order_2=4 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:class_exp=1.5 + spec:class_trig=1.5 + spec:fn_power=1.5 + spec:mix_classes=1.5 + spec:use_chain=2 + spec:chain=2 + spec:allow_exp=1.5 + spec:allow_trig=1.5 ⇒ 19] · D=20` |
| 20 | $\frac{d^{3}}{dx^{3}}\left[-e^{4x + 5}\right]$ | $-64e^{4x + 5}$ | `—` | `pack=deriv_higher · methods=chain,power · form_id=higher_order_3 · dress=[sign] · shape=fn:exp+sum · costs[form:higher_order_3=10 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:class_exp=1.5 + spec:class_trig=1.5 + spec:fn_power=1.5 + spec:mix_classes=1.5 + spec:use_chain=2 + spec:chain=2 + spec:allow_exp=1.5 ⇒ 23.5] · D=20` |
| 25 | $\frac{d^{3}}{dx^{3}}\left[-4\tan(12x)\right]$ | $-27648\sec^{2}(12x)\tan(12x)\tan(12x) - 13824\sec^{2}(12x)\sec^{2}(12x)$ | `—` | `pack=deriv_higher · methods=chain,power · form_id=higher_order_3 · dress=[sign,constant_multiple] · shape=fn:tan · costs[form:higher_order_3=10 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:chain_depth_2=1.5 + spec:class_exp=1.5 + spec:class_trig=1.5 + spec:fn_power=1.5 + spec:mix_classes=1.5 + spec:use_chain=2 + spec:chain=2 + spec:allow_trig=1.5 ⇒ 25] · D=25` |
| 25 | $\frac{d^{2}}{dx^{2}}\left[-e^{\sin(x)}\right]$ | $-e^{\sin(x)}\cos(x)\cos(x) + \sin(x)e^{\sin(x)}$ | `—` | `pack=deriv_higher · methods=chain,power · form_id=power_poly · dress=[sign] · shape=fn:exp+sin · costs[form:power_poly=0 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:class_exp=1.5 + spec:class_trig=1.5 + spec:fn_power=1.5 + spec:mix_classes=1.5 + spec:use_chain=2 + spec:chain=2 + spec:allow_exp=1.5 + spec:allow_trig=1.5 ⇒ 15] · D=25` |
| 25 | $\frac{d^{3}}{dx^{3}}\left[-4e^{8x + 8}\right]$ | $-2048e^{8x + 8}$ | `—` | `pack=deriv_higher · methods=chain,power · form_id=higher_order_3 · dress=[sign,constant_multiple] · shape=fn:exp+sum · costs[form:higher_order_3=10 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:chain_depth_2=1.5 + spec:class_exp=1.5 + spec:class_trig=1.5 + spec:fn_power=1.5 + spec:mix_classes=1.5 + spec:use_chain=2 + spec:chain=2 + spec:allow_exp=1.5 ⇒ 25] · D=25` |

## Derivatives — general

<a id="deriv_general"></a>

`calc_diff_general` · pack `deriv_general` · topic label: c1: General derivatives · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **11** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `general_mixed` | 4 |
| `chain_power_linear` | 3 |
| `product_poly_exp` | 2 |
| `product_poly_trig` | 2 |
| `product_two_poly` | 2 |
| `quotient_exp_poly` | 2 |
| `quotient_log_poly` | 2 |
| `quotient_mixed_special` | 2 |
| `quotient_poly` | 2 |
| `quotient_trig_poly` | 2 |
| `chain_nested` | 1 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\text{Find }\frac{d}{dx}\left(2x\right)$ | $2$ | `—` | `pack=deriv_general · methods=power · form_id=quotient_poly · shape=atom · costs[form:quotient_poly=0 + spec:use_quotient=2.5 ⇒ 2.5] · D=0` |
| 0 | $\frac{d}{dx}\left[\ln\left(x - 1\right)\right]$ | $\frac{1}{x - 1}$ | `—` | `pack=deriv_general · methods=chain,power · form_id=quotient_log_poly · shape=fn:ln+sum · costs[form:quotient_log_poly=6 + spec:class_log=1.5 + spec:use_quotient=2.5 + spec:chain=2 + spec:allow_log=1.5 ⇒ 13.5] · D=0` |
| 0 | $\text{Find }\frac{d}{dx}\left(\arccos(2x)\right)$ | $-\frac{2}{\sqrt{1-(2x)^{2}}}$ | `—` | `pack=deriv_general · methods=chain,power · form_id=product_poly_trig · shape=fn:arccos · costs[form:product_poly_trig=5 + spec:use_product=2 + spec:chain=2 + spec:allow_invtrig=2 ⇒ 11] · D=0` |
| 3 | $\frac{d}{dx}\left[\cosh\left(x - 1\right)\right]$ | $\sinh\left(x - 1\right)$ | `—` | `pack=deriv_general · methods=chain,power · form_id=product_two_poly · shape=fn:cosh+sum · costs[form:product_two_poly=0 + spec:use_product=2 + spec:chain=2 ⇒ 4] · D=3` |
| 3 | $\frac{d}{dx}\left[e^{3x}\right]$ | $3e^{3x}$ | `—` | `pack=deriv_general · methods=chain,power · form_id=quotient_exp_poly · shape=fn:exp · costs[form:quotient_exp_poly=6 + spec:class_exp=1.5 + spec:use_quotient=2.5 + spec:chain=2 + spec:allow_exp=1.5 ⇒ 13.5] · D=3` |
| 3 | $\text{Find }\frac{d}{dx}\left(\sqrt{3x}\right)$ | $\frac{3}{2\sqrt{3x}}$ | `—` | `pack=deriv_general · methods=chain,power · form_id=chain_power_linear · shape=fn:sqrt · costs[form:chain_power_linear=4 + spec:use_chain=2 + spec:chain=2 + spec:allow_roots=1 ⇒ 9] · D=3` |
| 6 | $\frac{d}{dx}\left[\sinh(2x)\sqrt{x + 3}\right]$ | $2\cosh(2x)\sqrt{x + 3}+\sinh(2x)\frac{1}{2\sqrt{x + 3}}$ | `—` | `pack=deriv_general · methods=chain,power,product · form_id=product_poly_trig · shape=fn:sinh+sqrt+product+sum · costs[form:product_poly_trig=5 + spec:use_product=2 + spec:chain=2 + spec:product=2 + spec:allow_roots=1 ⇒ 12] · D=6` |
| 6 | $\frac{d}{dx}\left[e^{2x - 1}\sin(3x)\right]$ | $2e^{2x - 1}\sin(3x)+e^{2x - 1}\left(3\cos(3x)\right)$ | `—` | `pack=deriv_general · methods=chain,power,product · form_id=quotient_mixed_special · shape=fn:exp+sin+product+sum · costs[form:quotient_mixed_special=6 + spec:class_exp=1.5 + spec:class_log=1.5 + spec:class_trig=1.5 + spec:mix_classes=1.5 + spec:use_product=2 + spec:use_quotient=2.5 + spec:chain=2 + spec:product=2 + spec:allow_exp=1.5 + spec:allow_trig=1.5 ⇒ 23.5] · D=6` |
| 6 | $\text{Find }\frac{d}{dx}\left(\cosh(4x)\right)$ | $4\sinh(4x)$ | `—` | `pack=deriv_general · methods=chain,power · form_id=general_mixed · shape=fn:cosh · costs[form:general_mixed=2 + spec:use_product=2 + spec:chain=2 ⇒ 6] · D=6` |
| 8 | $\frac{d}{dx}\left[-\cos^{2}(x)\right]$ | $2\cos(x)\sin(x)$ | `—` | `pack=deriv_general · methods=chain,power · form_id=quotient_trig_poly · dress=[sign] · shape=fn:cos+fn_power+power · costs[form:quotient_trig_poly=6 + dress:spec_sign=0.5 + spec:class_trig=1.5 + spec:use_chain=2 + spec:use_product=2 + spec:use_quotient=2.5 + spec:chain=2 + spec:allow_trig=1.5 ⇒ 18] · D=8` |
| 8 | $\frac{d}{dx}\left[-\sin(5x)\tan(3x)\right]$ | $-5\cos(5x)\tan(3x) + 3\sec^{2}(3x)\sin(5x)$ | `—` | `pack=deriv_general · methods=chain,power,product · form_id=quotient_trig_poly · dress=[sign] · shape=fn:sin+tan+product · costs[form:quotient_trig_poly=6 + dress:spec_sign=0.5 + spec:class_trig=1.5 + spec:use_chain=2 + spec:use_product=2 + spec:use_quotient=2.5 + spec:chain=2 + spec:product=2 + spec:allow_trig=1.5 ⇒ 20] · D=8` |
| 8 | $\text{Find }\frac{d}{dx}\left(-\sinh(2x)\cosh^{3}(3x)\right)$ | $-2\cosh(2x)\cosh^{3}(3x) + 9\cosh^{2}(3x)\sinh(3x)\sinh(2x)$ | `—` | `pack=deriv_general · methods=chain,power,product · form_id=general_mixed · dress=[sign] · shape=fn:cosh+sinh+fn_power+product+power · costs[form:general_mixed=2 + dress:spec_sign=0.5 + spec:use_chain=2 + spec:use_product=2 + spec:chain=2 + spec:product=2 + spec:nest_depth=2 ⇒ 12.5] · D=8` |
| 12 | $\text{Find }\frac{d}{dx}\left(-\left(x^{3} + 5x^{2} - 4x + 4\right)\left(-5x^{2}\right)\right)$ | $+5\left(3x^{2} + 10x - 4\right)x^{2} - 10x\left(x^{3} + 5x^{2} - 4x + 4\right)$ | `—` | `pack=deriv_general · methods=power,product · form_id=quotient_poly · dress=[sign] · shape=product+sum+power · costs[form:quotient_poly=0 + dress:spec_sign=0.5 + spec:use_chain=2 + spec:use_product=2 + spec:use_quotient=2.5 + spec:product=2 ⇒ 9] · D=12` |
| 12 | $\text{Find }\frac{d}{dx}\left(-\ln\left(x - 2\right)\ln^{2}(2x)\right)$ | $-\frac{1}{x - 2}\ln^{2}(2x) + 4\ln\left(2x\right)\frac{1}{2x}\ln\left(x - 2\right)$ | `—` | `pack=deriv_general · methods=chain,power,product · form_id=quotient_log_poly · dress=[sign] · shape=fn:ln+fn_power+product+sum+power · costs[form:quotient_log_poly=6 + dress:spec_sign=0.5 + spec:class_log=1.5 + spec:use_chain=2 + spec:use_product=2 + spec:use_quotient=2.5 + spec:chain=2 + spec:product=2 + spec:allow_log=1.5 + spec:nest_depth=2 ⇒ 22] · D=12` |
| 12 | $\frac{d}{dx}\left[-\ln\left(2x - 3\right)\right]$ | $-2\frac{1}{2x - 3}$ | `—` | `pack=deriv_general · methods=chain,power · form_id=general_mixed · dress=[sign] · shape=fn:ln+sum · costs[form:general_mixed=2 + dress:spec_sign=0.5 + spec:use_chain=2 + spec:use_product=2 + spec:use_quotient=2.5 + spec:chain=2 + spec:allow_log=1.5 ⇒ 12.5] · D=12` |
| 16 | $\text{Find }\frac{d}{dx}\left(-4\cos(8x)\arccos^{3}(x)\right)$ | $-4\cdot\left(-8\sin(8x)\arccos^{3}(x) + 3\arccos^{2}(x)\left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\cos(8x)\right)$ | `—` | `pack=deriv_general · methods=chain,power,product · form_id=general_mixed · dress=[sign,constant_multiple] · shape=fn:arccos+cos+fn_power+product+power · costs[form:general_mixed=2 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:chain_depth_2=1.5 + spec:use_chain=2 + spec:use_product=2 + spec:use_quotient=2.5 + spec:chain=2 + spec:product=2 + spec:allow_invtrig=2 + spec:allow_trig=1.5 ⇒ 19.5] · D=16` |
| 16 | $\text{Find }\frac{d}{dx}\left(2\ln\left(2x - 2\right)\cosh\left(\cos\left(6x - 7\right)\right)\right)$ | $22\frac{1}{2x - 2}\cosh\left(\cos\left(6x - 7\right)\right) - 6\sinh\left(\cos\left(6x - 7\right)\right)\sin\left(6x - 7\right)\ln\left(2x - 2\right)$ | `—` | `pack=deriv_general · methods=chain,power,product · form_id=chain_power_linear · dress=[sign,constant_multiple] · shape=fn:cos+cosh+ln+product+sum · costs[form:chain_power_linear=4 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:chain_depth_2=1.5 + spec:use_chain=2 + spec:use_product=2 + spec:use_quotient=2.5 + spec:chain=2 + spec:product=2 + spec:allow_log=1.5 + spec:allow_trig=1.5 + spec:nest_depth=2 ⇒ 23] · D=16` |
| 16 | $\text{Find }\frac{d}{dx}\left(4\cosh\left(e^{9x + 7}\right)\arccos(x)\right)$ | $49\sinh\left(e^{9x + 7}\right)e^{9x + 7}\arccos(x) + \left(-\frac{1}{\sqrt{1-(x)^{2}}}\right)\cosh\left(e^{9x + 7}\right)$ | `—` | `pack=deriv_general · methods=chain,power,product · form_id=chain_power_linear · dress=[sign,constant_multiple] · shape=fn:arccos+cosh+exp+product+sum · costs[form:chain_power_linear=4 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:chain_depth_2=1.5 + spec:use_chain=2 + spec:use_product=2 + spec:use_quotient=2.5 + spec:chain=2 + spec:product=2 + spec:allow_exp=1.5 + spec:allow_invtrig=2 + spec:nest_depth=2 ⇒ 23.5] · D=16` |
| 20 | $\frac{d}{dx}\left[-\ln^{2}(2x)\arctan(x)\right]$ | $-4\ln\left(2x\right)\frac{1}{2x}\arctan(x) + \frac{1}{1+(x)^{2}}\ln^{2}(2x)$ | `—` | `pack=deriv_general · methods=chain,power,product · form_id=product_poly_exp · dress=[sign] · shape=fn:arctan+ln+fn_power+product+power · costs[form:product_poly_exp=5 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:class_trig=1.5 + spec:use_chain=2 + spec:use_product=2 + spec:use_quotient=2.5 + spec:chain=2 + spec:product=2 + spec:allow_invtrig=2 + spec:allow_log=1.5 + spec:nest_depth=2 ⇒ 24.5] · D=20` |
| 20 | $\text{Find }\frac{d}{dx}\left(-\arccos^{3}(3x)\ln\left(6x + 2\right)\right)$ | $-9\arccos^{2}(3x)\left(-\frac{1}{\sqrt{1-(3x)^{2}}}\right)\ln\left(6x + 2\right) + 6\frac{1}{6x + 2}\arccos^{3}(3x)$ | `—` | `pack=deriv_general · methods=chain,power,product · form_id=product_poly_exp · dress=[sign] · shape=fn:arccos+ln+fn_power+product+sum+power · costs[form:product_poly_exp=5 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:class_trig=1.5 + spec:use_chain=2 + spec:use_product=2 + spec:use_quotient=2.5 + spec:chain=2 + spec:product=2 + spec:allow_invtrig=2 + spec:allow_log=1.5 + spec:nest_depth=2 ⇒ 24.5] · D=20` |
| 20 | $\text{Find }\frac{d}{dx}\left(2\arctan^{2}(x)\ln\left(5x - 3\right)\right)$ | $22\arctan(x)\frac{1}{1+(x)^{2}}\ln\left(5x - 3\right) + 5\frac{1}{5x - 3}\arctan^{2}(x)$ | `—` | `pack=deriv_general · methods=chain,power,product · form_id=chain_nested · dress=[sign,constant_multiple] · shape=fn:arctan+ln+fn_power+product+sum+power · costs[form:chain_nested=12 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:chain_depth_2=1.5 + spec:class_trig=1.5 + spec:use_chain=2 + spec:use_product=2 + spec:use_quotient=2.5 + spec:chain=2 + spec:product=2 + spec:allow_invtrig=2 + spec:allow_log=1.5 ⇒ 31] · D=20` |
| 25 | $\frac{d^{3}}{dx^{3}}\left[-e^{3x - 10}\right]$ | $-27e^{3x - 10}$ | `—` | `pack=deriv_general · methods=chain,power · form_id=quotient_exp_poly · dress=[sign] · shape=fn:exp+sum · costs[form:quotient_exp_poly=6 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:class_exp=1.5 + spec:class_trig=1.5 + spec:use_chain=2 + spec:use_product=2 + spec:use_quotient=2.5 + spec:chain=2 + spec:allow_exp=1.5 ⇒ 21] · D=25` |
| 25 | $\frac{d}{dx}\left[-2\tan(6x)\ln^{2}\left(\sin(5x)\right)\right]$ | $-26\sec^{2}(6x)\ln^{2}\left(\sin(5x)\right) + 10\ln\left(\sin(5x)\right)\frac{1}{\sin(5x)}\cos(5x)\tan(6x)$ | `—` | `pack=deriv_general · methods=chain,power,product · form_id=quotient_mixed_special · dress=[sign,constant_multiple] · shape=fn:ln+sin+tan+fn_power+product+power · costs[form:quotient_mixed_special=6 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:chain_depth_2=1.5 + spec:class_exp=1.5 + spec:class_log=1.5 + spec:class_trig=1.5 + spec:mix_classes=1.5 + spec:use_chain=2 + spec:use_product=2 + spec:use_quotient=2.5 + spec:chain=2 + spec:product=2 + spec:allow_log=1.5 + spec:allow_trig=1.5 + spec:nest_depth=3 ⇒ 32] · D=25` |
| 25 | $\frac{d^{3}}{dx^{3}}\left[-\left(x^{2} - 8\right)^{\frac{4}{5}}\right]$ | $-8\cdot\left(-\frac{6}{5}\left(x^{2} - 8\right)^{-\frac{11}{5}}x\left(-\frac{1}{5}\right)x\frac{4}{5}x\right) - 4\cdot\left(-\frac{1}{5}\left(x^{2} - 8\right)^{-\frac{6}{5}}\frac{4}{5}x\right) - 4\cdot\left(-\frac{1}{5}\left(x^{2} - 8\right)^{-\frac{6}{5}}x\frac{4}{5}\right) - 4\cdot\left(-\frac{1}{5}\left(x^{2} - 8\right)^{-\frac{6}{5}}x\frac{4}{5}\right)$ | `—` | `pack=deriv_general · methods=chain,power · form_id=product_two_poly · dress=[sign] · shape=sum+power · costs[form:product_two_poly=0 + dress:spec_sign=0.5 + spec:chain_depth_2=1.5 + spec:class_exp=1.5 + spec:class_trig=1.5 + spec:use_chain=2 + spec:use_product=2 + spec:use_quotient=2.5 + spec:chain=2 + spec:allow_roots=1 ⇒ 14.5] · D=25` |

## Linear approximations

<a id="linear_approx"></a>

`calc_app_diff_linear_approximations` · pack `linear_approx` · topic label: c1: Linear approximations · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **4** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `linear_approximation:quad` | 11 |
| `linear_approximation:sqrt` | 6 |
| `linear_approximation:reciprocal` | 4 |
| `linear_approximation:exp` | 3 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=1.$ | $L(x)=1+2(x-1)$ | `linearization` | `spec_pack=structured_linear_approximation · tricks=[linearization] · methods=differential · form_id=quad · D=0` |
| 0 | $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=1.$ | $L(x)=1+2(x-1)$ | `linearization` | `spec_pack=structured_linear_approximation · tricks=[linearization] · methods=differential · form_id=quad · D=0` |
| 0 | $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=4.$ | $L(x)=16+8(x-4)$ | `linearization` | `spec_pack=structured_linear_approximation · tricks=[linearization] · methods=differential · form_id=quad · D=0` |
| 3 | $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=3.$ | $L(x)=9+6(x-3)$ | `linearization` | `spec_pack=structured_linear_approximation · tricks=[linearization] · methods=differential · form_id=quad · D=3` |
| 3 | $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=2.$ | $L(x)=4+4(x-2)$ | `linearization` | `spec_pack=structured_linear_approximation · tricks=[linearization] · methods=differential · form_id=quad · D=3` |
| 3 | $\text{Find the linear approximation of }f(x)=\sqrt{x}\text{ at }x=9.$ | $L(x)=3+\frac{1}{6}(x-9)$ | `linearization` | `spec_pack=structured_linear_approximation · tricks=[linearization] · methods=differential · form_id=sqrt · D=3` |
| 6 | $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=1.$ | $L(x)=1+2(x-1)$ | `linearization` | `spec_pack=structured_linear_approximation · tricks=[linearization] · methods=differential · form_id=quad · D=6` |
| 6 | $\text{Find the linear approximation of }f(x)=\sqrt{x}\text{ at }x=4.$ | $L(x)=2+\frac{1}{4}(x-4)$ | `linearization` | `spec_pack=structured_linear_approximation · tricks=[linearization] · methods=differential · form_id=sqrt · D=6` |
| 6 | $\text{Find the linear approximation of }f(x)=\sqrt{x}\text{ at }x=4.$ | $L(x)=2+\frac{1}{4}(x-4)$ | `linearization` | `spec_pack=structured_linear_approximation · tricks=[linearization] · methods=differential · form_id=sqrt · D=6` |
| 8 | $\text{Use the linear approximation of }f(x)=x^{2}\text{ at }x=1\text{ to estimate }f(\frac{6}{5}).$ | $\frac{7}{5}$ | `linearization` | `spec_pack=structured_linear_approximation · tricks=[linearization] · methods=differential · form_id=quad · D=8` |
| 8 | $\text{Find the linear approximation of }f(x)=\sqrt{x}\text{ at }x=4.$ | $L(x)=2+\frac{1}{4}(x-4)$ | `linearization` | `spec_pack=structured_linear_approximation · tricks=[linearization] · methods=differential · form_id=sqrt · D=8` |
| 8 | $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=1.$ | $L(x)=1+2(x-1)$ | `linearization` | `spec_pack=structured_linear_approximation · tricks=[linearization] · methods=differential · form_id=quad · D=8` |
| 12 | $\text{Find the linear approximation of }f(x)=\frac{1}{x}\text{ at }x=4.$ | $L(x)=\frac{1}{4}-\frac{1}{16}(x-4)$ | `linearization` | `spec_pack=structured_linear_approximation · tricks=[linearization] · methods=differential · form_id=reciprocal · D=12` |
| 12 | $\text{Use the linear approximation of }f(x)=x^{2}\text{ at }x=4\text{ to estimate }f(\frac{21}{5}).$ | $\frac{88}{5}$ | `linearization` | `spec_pack=structured_linear_approximation · tricks=[linearization] · methods=differential · form_id=quad · D=12` |
| 12 | $\text{Find the linear approximation of }f(x)=e^{x}\text{ at }x=0.$ | $L(x)=1+x$ | `linearization` | `spec_pack=structured_linear_approximation · tricks=[linearization] · methods=differential · form_id=exp · D=12` |
| 16 | $\text{Find the linear approximation of }f(x)=\sqrt{x}\text{ at }x=4.$ | $L(x)=2+\frac{1}{4}(x-4)$ | `linearization` | `spec_pack=structured_linear_approximation · tricks=[linearization] · methods=differential · form_id=sqrt · D=16` |
| 16 | $\text{Find the linear approximation of }f(x)=\frac{1}{x}\text{ at }x=4.$ | $L(x)=\frac{1}{4}-\frac{1}{16}(x-4)$ | `linearization` | `spec_pack=structured_linear_approximation · tricks=[linearization] · methods=differential · form_id=reciprocal · D=16` |
| 16 | $\text{Find the linear approximation of }f(x)=\frac{1}{x}\text{ at }x=4.$ | $L(x)=\frac{1}{4}-\frac{1}{16}(x-4)$ | `linearization` | `spec_pack=structured_linear_approximation · tricks=[linearization] · methods=differential · form_id=reciprocal · D=16` |
| 20 | $\text{Find the linear approximation of }f(x)=e^{x}\text{ at }x=0.$ | $L(x)=1+x$ | `linearization` | `spec_pack=structured_linear_approximation · tricks=[linearization] · methods=differential · form_id=exp · D=20` |
| 20 | $\text{Find the linear approximation of }f(x)=\sqrt{x}\text{ at }x=4.$ | $L(x)=2+\frac{1}{4}(x-4)$ | `linearization` | `spec_pack=structured_linear_approximation · tricks=[linearization] · methods=differential · form_id=sqrt · D=20` |
| 20 | $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=1.$ | $L(x)=1+2(x-1)$ | `linearization` | `spec_pack=structured_linear_approximation · tricks=[linearization] · methods=differential · form_id=quad · D=20` |
| 25 | $\text{Find the linear approximation of }f(x)=e^{x}\text{ at }x=0.$ | $L(x)=1+x$ | `linearization` | `spec_pack=structured_linear_approximation · tricks=[linearization] · methods=differential · form_id=exp · D=25` |
| 25 | $\text{Find the linear approximation of }f(x)=\frac{1}{x}\text{ at }x=2.$ | $L(x)=\frac{1}{2}-\frac{1}{4}(x-2)$ | `linearization` | `spec_pack=structured_linear_approximation · tricks=[linearization] · methods=differential · form_id=reciprocal · D=25` |
| 25 | $\text{Find the linear approximation of }f(x)=x^{2}\text{ at }x=1.$ | $L(x)=1+2(x-1)$ | `linearization` | `spec_pack=structured_linear_approximation · tricks=[linearization] · methods=differential · form_id=quad · D=25` |

## Differentials

<a id="differentials"></a>

`calc_app_diff_differentials` · pack `differentials` · topic label: c1: Differentials · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **10** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `differentials:ln` | 5 |
| `differentials:radical` | 4 |
| `differentials:poly_power` | 3 |
| `differentials:poly_quad` | 3 |
| `differentials:trig` | 3 |
| `differentials:reciprocal` | 2 |
| `differentials:chain_exp` | 1 |
| `differentials:eval_dx` | 1 |
| `differentials:exp` | 1 |
| `differentials:product` | 1 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\text{For }y=\ln(x),\text{ find }dy.$ | $dy=\frac{1}{x}\,dx$ | `—` | `spec_pack=structured_differentials · methods=differential · form_id=ln · D=0` |
| 0 | $\text{For }y=\cos x,\text{ find }dy.$ | $dy=-\sin(x)\,dx$ | `—` | `spec_pack=structured_differentials · methods=differential · form_id=trig · D=0` |
| 0 | $\text{For }y=x\left(x + 5\right),\text{ find }dy.$ | $dy=\left(2x + 5\right)\,dx$ | `—` | `spec_pack=structured_differentials · methods=differential · form_id=poly_quad · D=0` |
| 3 | $\text{For }y=x\left(x + 4\right),\text{ find }dy.$ | $dy=\left(2x + 4\right)\,dx$ | `—` | `spec_pack=structured_differentials · methods=differential · form_id=poly_quad · D=3` |
| 3 | $\text{For }y=\ln\|x\|,\text{ find }dy.$ | $dy=\frac{1}{x}\,dx$ | `—` | `spec_pack=structured_differentials · methods=differential · form_id=ln · D=3` |
| 3 | $\text{For }y=x^{5},\text{ find }dy.$ | $dy=5x^{4}\,dx$ | `—` | `spec_pack=structured_differentials · methods=differential · form_id=poly_power · D=3` |
| 6 | $\text{For }y=\ln(x),\text{ find }dy.$ | $dy=\frac{1}{x}\,dx$ | `—` | `spec_pack=structured_differentials · methods=differential · form_id=ln · D=6` |
| 6 | $\text{For }y=x^{3},\text{ find }dy.$ | $dy=3x^{2}\,dx$ | `—` | `spec_pack=structured_differentials · methods=differential · form_id=poly_power · D=6` |
| 6 | $\text{For }y=x^{-1},\text{ find }dy.$ | $dy=-\frac{1}{x^{2}}\,dx$ | `—` | `spec_pack=structured_differentials · methods=differential · form_id=reciprocal · D=6` |
| 8 | $\text{For }y=\ln(x),\text{ find }dy.$ | $dy=\frac{1}{x}\,dx$ | `—` | `spec_pack=structured_differentials · methods=differential · form_id=ln · D=8` |
| 8 | $\text{For }y=\sqrt{x},\text{ find }dy.$ | $dy=\frac{1}{2\sqrt{x}}\,dx$ | `—` | `spec_pack=structured_differentials · methods=differential · form_id=radical · D=8` |
| 8 | $\text{For }y=x^{2},\text{ find }dy.$ | $dy=2x\,dx$ | `—` | `spec_pack=structured_differentials · methods=differential · form_id=poly_power · D=8` |
| 12 | $\text{For }y=\cos x,\text{ find }dy.$ | $dy=-\sin(x)\,dx$ | `—` | `spec_pack=structured_differentials · methods=differential · form_id=trig · D=12` |
| 12 | $\text{For }y=x\left(x + 3\right),\text{ find }dy.$ | $dy=\left(2x + 3\right)\,dx$ | `—` | `spec_pack=structured_differentials · methods=differential · form_id=poly_quad · D=12` |
| 12 | $\text{For }y=x^{1/2},\text{ find }dy.$ | $dy=\frac{1}{2\sqrt{x}}\,dx$ | `—` | `spec_pack=structured_differentials · methods=differential · form_id=radical · D=12` |
| 16 | $\text{For }y=e^{x^{2}},\text{ find }dy.$ | $dy=2xe^{x^{2}}\,dx$ | `—` | `spec_pack=structured_differentials · methods=differential,chain · form_id=chain_exp · D=16` |
| 16 | $\text{For }y=\ln(x),\text{ find }dy.$ | $dy=\frac{1}{x}\,dx$ | `—` | `spec_pack=structured_differentials · methods=differential · form_id=ln · D=16` |
| 16 | $\text{For }y=3x + x^{2},\text{ find }dy\text{ when }x=3\text{ and }dx=\frac{1}{2}.$ | $\frac{9}{2}$ | `—` | `spec_pack=structured_differentials · methods=differential · form_id=eval_dx · D=16` |
| 20 | $\text{For }y=\sqrt{x},\text{ find }dy.$ | $dy=\frac{1}{2\sqrt{x}}\,dx$ | `—` | `spec_pack=structured_differentials · methods=differential · form_id=radical · D=20` |
| 20 | $\text{For }y=x\cdot\sin(x),\text{ find }dy.$ | $dy=\left(\sin(x)+x\cos(x)\right)\,dx$ | `—` | `spec_pack=structured_differentials · methods=differential,product · form_id=product · D=20` |
| 20 | $\text{For }y=e^{4x},\text{ find }dy.$ | $dy=4e^{4x}\,dx$ | `—` | `spec_pack=structured_differentials · methods=differential · form_id=exp · D=20` |
| 25 | $\text{For }y=\tan(x),\text{ find }dy.$ | $dy=\sec^{2}(x)\,dx$ | `—` | `spec_pack=structured_differentials · methods=differential · form_id=trig · D=25` |
| 25 | $\text{For }y=\sqrt{x},\text{ find }dy.$ | $dy=\frac{1}{2\sqrt{x}}\,dx$ | `—` | `spec_pack=structured_differentials · methods=differential · form_id=radical · D=25` |
| 25 | $\text{For }y=\frac{1}{x},\text{ find }dy.$ | $dy=-\frac{1}{x^{2}}\,dx$ | `—` | `spec_pack=structured_differentials · methods=differential · form_id=reciprocal · D=25` |

## Integrals — power rule

<a id="int_power"></a>

`calc_indef_int_power_rule` · pack `int_power` · topic label: c1: Power Rule · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **6** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `sqrt_x` | 6 |
| `poly_sum` | 5 |
| `x_sqrt_x` | 5 |
| `rewrite_over_x` | 4 |
| `neg_power` | 3 |
| `one_over_sqrt_x` | 1 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\int \sqrt{x}\,dx$ | $\frac{2}{3}x^{\frac{3}{2}}+C$ | `power` | `spec_pack=integral_power · tricks=[power] · form_id=sqrt_x · costs[form:sqrt_x=1 ⇒ 1] · D=0` |
| 0 | $\int \sqrt{x}\,dx$ | $\frac{2}{3}x^{\frac{3}{2}}+C$ | `power` | `spec_pack=integral_power · tricks=[power] · form_id=sqrt_x · costs[form:sqrt_x=1 ⇒ 1] · D=0` |
| 0 | $\int \sqrt{x}\,dx$ | $\frac{2}{3}x^{\frac{3}{2}}+C$ | `power` | `spec_pack=integral_power · tricks=[power] · form_id=sqrt_x · costs[form:sqrt_x=1 ⇒ 1] · D=0` |
| 3 | $\int 6 \, dx$ | $6x+C$ | `power` | `spec_pack=integral_power · tricks=[power] · form_id=poly_sum · costs[form:poly_sum=0.5 ⇒ 0.5] · D=3` |
| 3 | $\int \frac{1}{\sqrt{x}}\,dx$ | $2\sqrt{x}+C$ | `power` | `spec_pack=integral_power · tricks=[power] · form_id=one_over_sqrt_x · costs[form:one_over_sqrt_x=1.5 ⇒ 1.5] · D=3` |
| 3 | $\int \sqrt{x}\,dx$ | $\frac{2}{3}x^{\frac{3}{2}}+C$ | `power` | `spec_pack=integral_power · tricks=[power] · form_id=sqrt_x · costs[form:sqrt_x=1 ⇒ 1] · D=3` |
| 6 | $\int \frac{6}{x^{2}}\,dx$ | $-6x^{-1}+C$ | `power` | `spec_pack=integral_power · tricks=[power] · form_id=neg_power · costs[form:neg_power=2 ⇒ 2] · D=6` |
| 6 | $\int  -\frac{5}{x^{3}}\,dx$ | $\frac{5}{2}x^{-2}+C$ | `power` | `spec_pack=integral_power · tricks=[power] · form_id=neg_power · dress=[sign] · costs[form:neg_power=2 + dress:spec_sign=0.5 ⇒ 2.5] · D=6` |
| 6 | $\int x\sqrt{x}\,dx$ | $\frac{2}{5}x^{\frac{5}{2}}+C$ | `power` | `spec_pack=integral_power · tricks=[power] · form_id=x_sqrt_x · costs[form:x_sqrt_x=2 ⇒ 2] · D=6` |
| 8 | $\int \sqrt{x}\,dx$ | $\frac{2}{3}x^{\frac{3}{2}}+C$ | `power` | `spec_pack=integral_power · tricks=[power] · form_id=sqrt_x · costs[form:sqrt_x=1 ⇒ 1] · D=8` |
| 8 | $\int 5x^{4} \, dx$ | $x^{5}+C$ | `power` | `spec_pack=integral_power · tricks=[power] · form_id=poly_sum · costs[form:poly_sum=0.5 ⇒ 0.5] · D=8` |
| 8 | $\int \frac{x^{2}+4\sqrt[3]{x}}{x}\,dx$ | $\frac{1}{2}x^{2}+12x^{\frac{1}{3}}+C$ | `power` | `spec_pack=integral_power · tricks=[power] · form_id=rewrite_over_x · costs[form:rewrite_over_x=3 ⇒ 3] · D=8` |
| 12 | $\int  -x\sqrt{x}\,dx$ | $-\frac{2}{5}x^{\frac{5}{2}}+C$ | `power` | `spec_pack=integral_power · tricks=[power] · form_id=x_sqrt_x · dress=[sign] · costs[form:x_sqrt_x=2 + dress:spec_sign=0.5 ⇒ 2.5] · D=12` |
| 12 | $\int -2 \, dx$ | $-2x+C$ | `power` | `spec_pack=integral_power · tricks=[power] · form_id=poly_sum · costs[form:poly_sum=0.5 ⇒ 0.5] · D=12` |
| 12 | $\int  -4x\sqrt{x}\,dx$ | $-4\frac{2}{5}x^{\frac{5}{2}}+C$ | `power` | `spec_pack=integral_power · tricks=[power] · form_id=x_sqrt_x · dress=[constant_multiple] · costs[form:x_sqrt_x=2 + dress:spec_scale=1.5 ⇒ 3.5] · D=12` |
| 16 | $\int  -\frac{x^{2}+3\sqrt[3]{x}}{x}\,dx$ | $-\left(\frac{1}{2}x^{2}+9x^{\frac{1}{3}}\right)+C$ | `power` | `spec_pack=integral_power · tricks=[power] · form_id=rewrite_over_x · dress=[sign] · costs[form:rewrite_over_x=3 + dress:spec_sign=0.5 ⇒ 3.5] · D=16` |
| 16 | $\int  2\sqrt{x}\,dx$ | $2\frac{2}{3}x^{\frac{3}{2}}+C$ | `power` | `spec_pack=integral_power · tricks=[power] · form_id=sqrt_x · dress=[sign,constant_multiple] · costs[form:sqrt_x=1 + dress:spec_sign=0.5 + dress:spec_scale=1.5 ⇒ 3] · D=16` |
| 16 | $\int  -4x\sqrt{x}\,dx$ | $-4\frac{2}{5}x^{\frac{5}{2}}+C$ | `power` | `spec_pack=integral_power · tricks=[power] · form_id=x_sqrt_x · dress=[sign,constant_multiple] · costs[form:x_sqrt_x=2 + dress:spec_sign=0.5 + dress:spec_scale=1.5 ⇒ 4] · D=16` |
| 20 | $\int -x^{4} - 4x^{3} \, dx$ | $-x^{4}-\frac{1}{5}x^{5}+C$ | `power` | `spec_pack=integral_power · tricks=[power] · form_id=poly_sum · costs[form:poly_sum=0.5 ⇒ 0.5] · D=20` |
| 20 | $\int  -2x\sqrt{x}\,dx$ | $-2\frac{2}{5}x^{\frac{5}{2}}+C$ | `power` | `spec_pack=integral_power · tricks=[power] · form_id=x_sqrt_x · dress=[sign,constant_multiple] · costs[form:x_sqrt_x=2 + dress:spec_sign=0.5 + dress:spec_scale=1.5 ⇒ 4] · D=20` |
| 20 | $\int  3\frac{x^{2}+3\sqrt[3]{x}}{x}\,dx$ | $3\left(\frac{1}{2}x^{2}+9x^{\frac{1}{3}}\right)+C$ | `power` | `spec_pack=integral_power · tricks=[power] · form_id=rewrite_over_x · dress=[constant_multiple] · costs[form:rewrite_over_x=3 + dress:spec_scale=1.5 ⇒ 4.5] · D=20` |
| 25 | $\int -x^{4} - 6x^{3} \, dx$ | $-\frac{1}{5}x^{5}-\frac{3}{2}x^{4}+C$ | `power` | `spec_pack=integral_power · tricks=[power] · form_id=poly_sum · costs[form:poly_sum=0.5 ⇒ 0.5] · D=25` |
| 25 | $\int  -\frac{x^{2}+3\sqrt[3]{x}}{x}\,dx$ | $-\left(\frac{1}{2}x^{2}+9x^{\frac{1}{3}}\right)+C$ | `power` | `spec_pack=integral_power · tricks=[power] · form_id=rewrite_over_x · dress=[sign] · costs[form:rewrite_over_x=3 + dress:spec_sign=0.5 ⇒ 3.5] · D=25` |
| 25 | $\int  2\frac{6}{x^{4}}\,dx$ | $-4x^{-3}+C$ | `power` | `spec_pack=integral_power · tricks=[power] · form_id=neg_power · dress=[constant_multiple] · costs[form:neg_power=2 + dress:spec_scale=1.5 ⇒ 3.5] · D=25` |

## Integrals — trigonometric

<a id="int_trig"></a>

`calc_indef_int_trigonometric` · pack `int_trig` · topic label: c1: Trigonometric · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **14** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `basic_cos_kx` | 4 |
| `sin_j_cos` | 3 |
| `tan_even_reduction` | 3 |
| `cos_j_sin` | 2 |
| `sec_j_tan` | 2 |
| `sin_even_power` | 2 |
| `basic_sec_tan` | 1 |
| `basic_sin_kx` | 1 |
| `basic_tan` | 1 |
| `cos_even_power` | 1 |
| `product_sin_a_cos_b` | 1 |
| `tan_odd_alone` | 1 |
| `tan_odd_sec_any` | 1 |
| `tan_sec_sec_even` | 1 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\int \cos(5x)\,dx$ | $\frac{1}{5}\sin(5x)+C$ | `trig` | `spec_pack=integral_trig · tricks=[trig] · form_id=basic_cos_kx · costs[form:basic_cos_kx=1 + spec:allow_trig=1.5 ⇒ 2.5] · D=0` |
| 0 | $\int \cos(5x)\,dx$ | $\frac{1}{5}\sin(5x)+C$ | `trig` | `spec_pack=integral_trig · tricks=[trig] · form_id=basic_cos_kx · costs[form:basic_cos_kx=1 + spec:allow_trig=1.5 ⇒ 2.5] · D=0` |
| 0 | $\int \sin(4x)\,dx$ | $-\frac{1}{4}\cos(4x)+C$ | `trig` | `spec_pack=integral_trig · tricks=[trig] · form_id=basic_sin_kx · costs[form:basic_sin_kx=1 + spec:allow_trig=1.5 ⇒ 2.5] · D=0` |
| 3 | $\int \cos(6x)\,dx$ | $\frac{1}{6}\sin(6x)+C$ | `trig` | `spec_pack=integral_trig · tricks=[trig] · form_id=basic_cos_kx · costs[form:basic_cos_kx=1 + spec:allow_trig=1.5 ⇒ 2.5] · D=3` |
| 3 | $\int \cos(6x)\,dx$ | $\frac{1}{6}\sin(6x)+C$ | `trig` | `spec_pack=integral_trig · tricks=[trig] · form_id=basic_cos_kx · costs[form:basic_cos_kx=1 + spec:allow_trig=1.5 ⇒ 2.5] · D=3` |
| 3 | $\int \sec(x)\tan(x)\,dx$ | $\sec(x)+C$ | `trig` | `spec_pack=integral_trig · tricks=[trig] · form_id=basic_sec_tan · costs[form:basic_sec_tan=1 + spec:allow_trig=1.5 ⇒ 2.5] · D=3` |
| 6 | $\int \tan(x)\,dx$ | $-\ln\|\cos(x)\|+C$ | `trig,u_sub` | `spec_pack=integral_trig · tricks=[trig,u_sub] · form_id=basic_tan · costs[form:basic_tan=1 + spec:allow_trig=1.5 ⇒ 2.5] · D=6` |
| 6 | $\int \cos^{2}(x)\,dx$ | $\frac{x}{2}+\frac{1}{4}\sin(2x)+C$ | `trig` | `spec_pack=integral_trig · tricks=[trig] · form_id=cos_even_power · costs[form:cos_even_power=2 + spec:allow_trig=1.5 ⇒ 3.5] · D=6` |
| 6 | $\int \sin^{2}(x)\,dx$ | $\frac{x}{2}-\frac{1}{4}\sin(2x)+C$ | `trig` | `spec_pack=integral_trig · tricks=[trig] · form_id=sin_even_power · costs[form:sin_even_power=2 + spec:allow_trig=1.5 ⇒ 3.5] · D=6` |
| 8 | $\int  4\sec^{4}(x)\tan(x)\,dx$ | $4\frac{1}{4}\sec^{4}(x)+C$ | `trig,u_sub` | `spec_pack=integral_trig · tricks=[trig,u_sub] · form_id=sec_j_tan · dress=[constant_multiple] · costs[form:sec_j_tan=2 + dress:spec_scale=1.5 + spec:allow_trig=1.5 ⇒ 5] · D=8` |
| 8 | $\int  -\cos^{2}(x)\sin(x)\,dx$ | $\frac{1}{3}\cos^{3}(x)+C$ | `trig,u_sub` | `spec_pack=integral_trig · tricks=[trig,u_sub] · form_id=cos_j_sin · dress=[sign] · costs[form:cos_j_sin=2 + dress:spec_sign=0.5 + spec:allow_trig=1.5 ⇒ 4] · D=8` |
| 8 | $\int \sin^{2}(x)\cos(x)\,dx$ | $\frac{1}{3}\sin^{3}(x)+C$ | `trig,u_sub` | `spec_pack=integral_trig · tricks=[trig,u_sub] · form_id=sin_j_cos · costs[form:sin_j_cos=2 + spec:allow_trig=1.5 ⇒ 3.5] · D=8` |
| 12 | $\int \tan^{3}(x)\,dx$ | $\frac{1}{2}\tan^{2}(x)+\ln\|\cos(x)\|+C$ | `trig,u_sub` | `spec_pack=integral_trig · tricks=[trig,u_sub] · form_id=tan_odd_alone · costs[form:tan_odd_alone=2 + spec:allow_trig=1.5 ⇒ 3.5] · D=12` |
| 12 | $\int \cos^{3}(x)\sin(x)\,dx$ | $-\frac{1}{4}\cos^{4}(x)+C$ | `trig,u_sub` | `spec_pack=integral_trig · tricks=[trig,u_sub] · form_id=cos_j_sin · costs[form:cos_j_sin=2 + spec:allow_trig=1.5 ⇒ 3.5] · D=12` |
| 12 | $\int  -3\sin^{2}(x)\,dx$ | $-3\left(\frac{x}{2}-\frac{1}{4}\sin(2x)\right)+C$ | `trig` | `spec_pack=integral_trig · tricks=[trig] · form_id=sin_even_power · dress=[constant_multiple] · costs[form:sin_even_power=2 + dress:spec_scale=1.5 + spec:allow_trig=1.5 ⇒ 5] · D=12` |
| 16 | $\int  -2\tan^{2}(x)\sec^{4}(x)\,dx$ | $-2\left(\frac{1}{3}\tan^{3}(x)+\frac{1}{5}\tan^{5}(x)\right)+C$ | `trig,u_sub` | `spec_pack=integral_trig · tricks=[trig,u_sub] · form_id=tan_sec_sec_even · dress=[sign,constant_multiple] · costs[form:tan_sec_sec_even=2 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:allow_trig=1.5 ⇒ 5.5] · D=16` |
| 16 | $\int  2\tan^{4}(x)\,dx$ | $2\left(\frac{1}{3}\tan^{3}(x)-\tan(x)+x\right)+C$ | `trig` | `spec_pack=integral_trig · tricks=[trig] · form_id=tan_even_reduction · dress=[sign,constant_multiple] · costs[form:tan_even_reduction=2 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:allow_trig=1.5 ⇒ 5.5] · D=16` |
| 16 | $\int  3\sin^{2}(x)\cos(x)\,dx$ | $3\frac{1}{3}\sin^{3}(x)+C$ | `trig,u_sub` | `spec_pack=integral_trig · tricks=[trig,u_sub] · form_id=sin_j_cos · dress=[constant_multiple,sign] · costs[form:sin_j_cos=2 + dress:spec_scale=1.5 + dress:spec_sign=0.5 + spec:allow_trig=1.5 ⇒ 5.5] · D=16` |
| 20 | $\int  -2\sin^{4}(x)\cos(x)\,dx$ | $-2\frac{1}{5}\sin^{5}(x)+C$ | `trig,u_sub` | `spec_pack=integral_trig · tricks=[trig,u_sub] · form_id=sin_j_cos · dress=[constant_multiple] · costs[form:sin_j_cos=2 + dress:spec_scale=1.5 + spec:allow_trig=1.5 ⇒ 5] · D=20` |
| 20 | $\int  -\sin(3x)\cos(5x)\,dx$ | $\frac{1}{16}\cos(8x)-\frac{1}{-4}\cos(-2x)+C$ | `trig` | `spec_pack=integral_trig · tricks=[trig] · form_id=product_sin_a_cos_b · dress=[sign] · costs[form:product_sin_a_cos_b=5 + dress:spec_sign=0.5 + spec:allow_trig=1.5 ⇒ 7] · D=20` |
| 20 | $\int  -\tan^{3}(x)\sec(x)\,dx$ | $-\left(\frac{1}{3}\sec^{3}(x)-\sec(x)\right)+C$ | `trig,u_sub` | `spec_pack=integral_trig · tricks=[trig,u_sub] · form_id=tan_odd_sec_any · dress=[sign] · costs[form:tan_odd_sec_any=2 + dress:spec_sign=0.5 + spec:allow_trig=1.5 ⇒ 4] · D=20` |
| 25 | $\int  -3\tan^{4}(x)\,dx$ | $-3\left(\frac{1}{3}\tan^{3}(x)-\tan(x)+x\right)+C$ | `trig` | `spec_pack=integral_trig · tricks=[trig] · form_id=tan_even_reduction · dress=[sign,constant_multiple] · costs[form:tan_even_reduction=2 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:allow_trig=1.5 ⇒ 5.5] · D=25` |
| 25 | $\int  3\tan^{4}(x)\,dx$ | $3\left(\frac{1}{3}\tan^{3}(x)-\tan(x)+x\right)+C$ | `trig` | `spec_pack=integral_trig · tricks=[trig] · form_id=tan_even_reduction · dress=[constant_multiple,sign] · costs[form:tan_even_reduction=2 + dress:spec_scale=1.5 + dress:spec_sign=0.5 + spec:allow_trig=1.5 ⇒ 5.5] · D=25` |
| 25 | $\int  -4\sec^{3}(x)\tan(x)\,dx$ | $-4\frac{1}{3}\sec^{3}(x)+C$ | `trig,u_sub` | `spec_pack=integral_trig · tricks=[trig,u_sub] · form_id=sec_j_tan · dress=[constant_multiple] · costs[form:sec_j_tan=2 + dress:spec_scale=1.5 + spec:allow_trig=1.5 ⇒ 5] · D=25` |

## Integrals — log / exp

<a id="int_log_exp"></a>

`calc_indef_int_logarithmic_rule_and_exponentials` · pack `int_log_exp` · topic label: c1: Logarithmic Rule and Exponentials · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **5** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `exp_k` | 7 |
| `ln` | 6 |
| `base_a` | 5 |
| `exp` | 4 |
| `ln_linear` | 2 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\int e^{4x}\,dx$ | $\frac{1}{4}e^{4x}+C$ | `ln_exp` | `spec_pack=integral_ln_exp · tricks=[ln_exp] · form_id=exp_k · costs[form:exp_k=2 + spec:allow_exp=1.5 ⇒ 3.5] · D=0` |
| 0 | $\int 3^{x}\,dx$ | $\frac{3^{x}}{\ln 3}+C$ | `ln_exp` | `spec_pack=integral_ln_exp · tricks=[ln_exp] · form_id=base_a · costs[form:base_a=2 + spec:allow_exp=1.5 ⇒ 3.5] · D=0` |
| 0 | $\int e^{x}\,dx$ | $e^{x}+C$ | `ln_exp` | `spec_pack=integral_ln_exp · tricks=[ln_exp] · form_id=exp · costs[form:exp=2 + spec:allow_exp=1.5 ⇒ 3.5] · D=0` |
| 3 | $\int 5^{x}\,dx$ | $\frac{5^{x}}{\ln 5}+C$ | `ln_exp` | `spec_pack=integral_ln_exp · tricks=[ln_exp] · form_id=base_a · costs[form:base_a=2 + spec:allow_exp=1.5 ⇒ 3.5] · D=3` |
| 3 | $\int e^{x}\,dx$ | $e^{x}+C$ | `ln_exp` | `spec_pack=integral_ln_exp · tricks=[ln_exp] · form_id=exp · costs[form:exp=2 + spec:allow_exp=1.5 ⇒ 3.5] · D=3` |
| 3 | $\int e^{4x}\,dx$ | $\frac{1}{4}e^{4x}+C$ | `ln_exp` | `spec_pack=integral_ln_exp · tricks=[ln_exp] · form_id=exp_k · costs[form:exp_k=2 + spec:allow_exp=1.5 ⇒ 3.5] · D=3` |
| 6 | $\int e^{5x}\,dx$ | $\frac{1}{5}e^{5x}+C$ | `ln_exp` | `spec_pack=integral_ln_exp · tricks=[ln_exp] · form_id=exp_k · costs[form:exp_k=2 + spec:allow_exp=1.5 ⇒ 3.5] · D=6` |
| 6 | $\int  4e^{5x}\,dx$ | $4\frac{1}{5}e^{5x}+C$ | `ln_exp` | `spec_pack=integral_ln_exp · tricks=[ln_exp] · form_id=exp_k · dress=[constant_multiple] · costs[form:exp_k=2 + dress:spec_scale=1.5 + spec:allow_exp=1.5 ⇒ 5] · D=6` |
| 6 | $\int  -\frac{1}{x}\,dx$ | $-\ln\|x\|+C$ | `ln_exp` | `spec_pack=integral_ln_exp · tricks=[ln_exp] · form_id=ln · dress=[sign] · costs[form:ln=2 + dress:spec_sign=0.5 + spec:allow_log=1.5 ⇒ 4] · D=6` |
| 8 | $\int  4\cdot 3^{x}\,dx$ | $4\frac{3^{x}}{\ln 3}+C$ | `ln_exp` | `spec_pack=integral_ln_exp · tricks=[ln_exp] · form_id=base_a · dress=[constant_multiple] · costs[form:base_a=2 + dress:spec_scale=1.5 + spec:allow_exp=1.5 ⇒ 5] · D=8` |
| 8 | $\int 5^{x}\,dx$ | $\frac{5^{x}}{\ln 5}+C$ | `ln_exp` | `spec_pack=integral_ln_exp · tricks=[ln_exp] · form_id=base_a · costs[form:base_a=2 + spec:allow_exp=1.5 ⇒ 3.5] · D=8` |
| 8 | $\int  4\cdot 2^{x}\,dx$ | $4\frac{2^{x}}{\ln 2}+C$ | `ln_exp` | `spec_pack=integral_ln_exp · tricks=[ln_exp] · form_id=base_a · dress=[constant_multiple] · costs[form:base_a=2 + dress:spec_scale=1.5 + spec:allow_exp=1.5 ⇒ 5] · D=8` |
| 12 | $\int  4\frac{1}{x}\,dx$ | $4\ln\|x\|+C$ | `ln_exp` | `spec_pack=integral_ln_exp · tricks=[ln_exp] · form_id=ln · dress=[constant_multiple] · costs[form:ln=2 + dress:spec_scale=1.5 + spec:allow_log=1.5 ⇒ 5] · D=12` |
| 12 | $\int  -2e^{5x}\,dx$ | $-2\frac{1}{5}e^{5x}+C$ | `ln_exp` | `spec_pack=integral_ln_exp · tricks=[ln_exp] · form_id=exp_k · dress=[constant_multiple] · costs[form:exp_k=2 + dress:spec_scale=1.5 + spec:allow_exp=1.5 ⇒ 5] · D=12` |
| 12 | $\int  -\frac{1}{x}\,dx$ | $-\ln\|x\|+C$ | `ln_exp` | `spec_pack=integral_ln_exp · tricks=[ln_exp] · form_id=ln · dress=[sign] · costs[form:ln=2 + dress:spec_sign=0.5 + spec:allow_log=1.5 ⇒ 4] · D=12` |
| 16 | $\int  -e^{5x}\,dx$ | $-\frac{1}{5}e^{5x}+C$ | `ln_exp` | `spec_pack=integral_ln_exp · tricks=[ln_exp] · form_id=exp_k · dress=[sign] · costs[form:exp_k=2 + dress:spec_sign=0.5 + spec:allow_exp=1.5 ⇒ 4] · D=16` |
| 16 | $\int  2e^{x}\,dx$ | $2e^{x}+C$ | `ln_exp` | `spec_pack=integral_ln_exp · tricks=[ln_exp] · form_id=exp · dress=[constant_multiple] · costs[form:exp=2 + dress:spec_scale=1.5 + spec:allow_exp=1.5 ⇒ 5] · D=16` |
| 16 | $\int  -2\frac{1}{x}\,dx$ | $-2\ln\|x\|+C$ | `ln_exp` | `spec_pack=integral_ln_exp · tricks=[ln_exp] · form_id=ln · dress=[sign,constant_multiple] · costs[form:ln=2 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:allow_log=1.5 ⇒ 5.5] · D=16` |
| 20 | $\int  -\frac{4}{4x + 4}\,dx$ | $-\left(\ln\|4x + 4\|\right)+C$ | `ln_exp` | `spec_pack=integral_ln_exp · tricks=[ln_exp] · form_id=ln_linear · dress=[sign] · costs[form:ln_linear=2 + dress:spec_sign=0.5 + spec:allow_log=1.5 ⇒ 4] · D=20` |
| 20 | $\int  2e^{2x}\,dx$ | $2\frac{1}{2}e^{2x}+C$ | `ln_exp` | `spec_pack=integral_ln_exp · tricks=[ln_exp] · form_id=exp_k · dress=[sign,constant_multiple] · costs[form:exp_k=2 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:allow_exp=1.5 ⇒ 5.5] · D=20` |
| 20 | $\int  3e^{x}\,dx$ | $3e^{x}+C$ | `ln_exp` | `spec_pack=integral_ln_exp · tricks=[ln_exp] · form_id=exp · dress=[sign,constant_multiple] · costs[form:exp=2 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:allow_exp=1.5 ⇒ 5.5] · D=20` |
| 25 | $\int  3\frac{4}{4x - 8}\,dx$ | $3\left(\ln\|4x - 8\|\right)+C$ | `ln_exp` | `spec_pack=integral_ln_exp · tricks=[ln_exp] · form_id=ln_linear · dress=[sign,constant_multiple] · costs[form:ln_linear=2 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:allow_log=1.5 ⇒ 5.5] · D=25` |
| 25 | $\int  -3\frac{1}{x}\,dx$ | $-3\ln\|x\|+C$ | `ln_exp` | `spec_pack=integral_ln_exp · tricks=[ln_exp] · form_id=ln · dress=[constant_multiple,sign] · costs[form:ln=2 + dress:spec_scale=1.5 + dress:spec_sign=0.5 + spec:allow_log=1.5 ⇒ 5.5] · D=25` |
| 25 | $\int  -\frac{1}{x}\,dx$ | $-\ln\|x\|+C$ | `ln_exp` | `spec_pack=integral_ln_exp · tricks=[ln_exp] · form_id=ln · dress=[sign] · costs[form:ln=2 + dress:spec_sign=0.5 + spec:allow_log=1.5 ⇒ 4] · D=25` |

## Integrals — inverse trig

<a id="int_invtrig"></a>

`calc_indef_int_inverse_trigonometric` · pack `int_invtrig` · topic label: c1: Inverse trigonometric · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **6** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `arctan_basic` | 6 |
| `arcsin_a2` | 5 |
| `arcsin_basic` | 5 |
| `arctan_a2` | 4 |
| `arctan_scaled` | 3 |
| `arcsin_scaled` | 1 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\int \frac{1}{1+x^{2}}\,dx$ | $\arctan(x)+C$ | `invtrig` | `spec_pack=integral_invtrig · tricks=[invtrig] · form_id=arctan_basic · costs[form:arctan_basic=2 + spec:allow_invtrig=2 ⇒ 4] · D=0` |
| 0 | $\int \frac{1}{1+x^{2}}\,dx$ | $\arctan(x)+C$ | `invtrig` | `spec_pack=integral_invtrig · tricks=[invtrig] · form_id=arctan_basic · costs[form:arctan_basic=2 + spec:allow_invtrig=2 ⇒ 4] · D=0` |
| 0 | $\int \frac{1}{1+x^{2}}\,dx$ | $\arctan(x)+C$ | `invtrig` | `spec_pack=integral_invtrig · tricks=[invtrig] · form_id=arctan_basic · costs[form:arctan_basic=2 + spec:allow_invtrig=2 ⇒ 4] · D=0` |
| 3 | $\int \frac{1}{\sqrt{1-x^{2}}}\,dx$ | $\arcsin(x)+C$ | `invtrig` | `spec_pack=integral_invtrig · tricks=[invtrig] · form_id=arcsin_basic · costs[form:arcsin_basic=2 + spec:allow_invtrig=2 ⇒ 4] · D=3` |
| 3 | $\int \frac{1}{\sqrt{1-x^{2}}}\,dx$ | $\arcsin(x)+C$ | `invtrig` | `spec_pack=integral_invtrig · tricks=[invtrig] · form_id=arcsin_basic · costs[form:arcsin_basic=2 + spec:allow_invtrig=2 ⇒ 4] · D=3` |
| 3 | $\int \frac{1}{1+x^{2}}\,dx$ | $\arctan(x)+C$ | `invtrig` | `spec_pack=integral_invtrig · tricks=[invtrig] · form_id=arctan_basic · costs[form:arctan_basic=2 + spec:allow_invtrig=2 ⇒ 4] · D=3` |
| 6 | $\int \frac{1}{\sqrt{25-x^{2}}}\,dx$ | $\arcsin\left(\frac{x}{5}\right)+C$ | `invtrig` | `spec_pack=integral_invtrig · tricks=[invtrig] · form_id=arcsin_a2 · costs[form:arcsin_a2=2 + spec:allow_invtrig=2 ⇒ 4] · D=6` |
| 6 | $\int \frac{1}{16+x^{2}}\,dx$ | $\frac{1}{4}\arctan\left(\frac{x}{4}\right)+C$ | `invtrig` | `spec_pack=integral_invtrig · tricks=[invtrig] · form_id=arctan_a2 · costs[form:arctan_a2=2 + spec:allow_invtrig=2 ⇒ 4] · D=6` |
| 6 | $\int  -3\frac{1}{\sqrt{16-x^{2}}}\,dx$ | $-3\arcsin\left(\frac{x}{4}\right)+C$ | `invtrig` | `spec_pack=integral_invtrig · tricks=[invtrig] · form_id=arcsin_a2 · dress=[constant_multiple] · costs[form:arcsin_a2=2 + dress:spec_scale=1.5 + spec:allow_invtrig=2 ⇒ 5.5] · D=6` |
| 8 | $\int \frac{1}{\sqrt{1-x^{2}}}\,dx$ | $\arcsin(x)+C$ | `invtrig` | `spec_pack=integral_invtrig · tricks=[invtrig] · form_id=arcsin_basic · costs[form:arcsin_basic=2 + spec:allow_invtrig=2 ⇒ 4] · D=8` |
| 8 | $\int  3\frac{1}{9+x^{2}}\,dx$ | $3\frac{1}{3}\arctan\left(\frac{x}{3}\right)+C$ | `invtrig` | `spec_pack=integral_invtrig · tricks=[invtrig] · form_id=arctan_a2 · dress=[constant_multiple] · costs[form:arctan_a2=2 + dress:spec_scale=1.5 + spec:allow_invtrig=2 ⇒ 5.5] · D=8` |
| 8 | $\int  3\frac{1}{\sqrt{4-x^{2}}}\,dx$ | $3\arcsin\left(\frac{x}{2}\right)+C$ | `invtrig` | `spec_pack=integral_invtrig · tricks=[invtrig] · form_id=arcsin_a2 · dress=[constant_multiple] · costs[form:arcsin_a2=2 + dress:spec_scale=1.5 + spec:allow_invtrig=2 ⇒ 5.5] · D=8` |
| 12 | $\int \frac{1}{\sqrt{1-x^{2}}}\,dx$ | $\arcsin(x)+C$ | `invtrig` | `spec_pack=integral_invtrig · tricks=[invtrig] · form_id=arcsin_basic · costs[form:arcsin_basic=2 + spec:allow_invtrig=2 ⇒ 4] · D=12` |
| 12 | $\int  -2\frac{1}{1+x^{2}}\,dx$ | $-2\arctan(x)+C$ | `invtrig` | `spec_pack=integral_invtrig · tricks=[invtrig] · form_id=arctan_basic · dress=[constant_multiple] · costs[form:arctan_basic=2 + dress:spec_scale=1.5 + spec:allow_invtrig=2 ⇒ 5.5] · D=12` |
| 12 | $\int  -\frac{1}{16+9x^{2}}\,dx$ | $-\frac{1}{12}\arctan\left(\frac{3x}{4}\right)+C$ | `invtrig` | `spec_pack=integral_invtrig · tricks=[invtrig] · form_id=arctan_scaled · dress=[sign] · costs[form:arctan_scaled=2 + dress:spec_sign=0.5 + spec:allow_invtrig=2 ⇒ 4.5] · D=12` |
| 16 | $\int  4\frac{1}{4+x^{2}}\,dx$ | $4\frac{1}{2}\arctan\left(\frac{x}{2}\right)+C$ | `invtrig` | `spec_pack=integral_invtrig · tricks=[invtrig] · form_id=arctan_a2 · dress=[constant_multiple] · costs[form:arctan_a2=2 + dress:spec_scale=1.5 + spec:allow_invtrig=2 ⇒ 5.5] · D=16` |
| 16 | $\int  3\frac{1}{\sqrt{4-16x^{2}}}\,dx$ | $3\frac{1}{4}\arcsin\left(\frac{4x}{2}\right)+C$ | `invtrig` | `spec_pack=integral_invtrig · tricks=[invtrig] · form_id=arcsin_scaled · dress=[constant_multiple] · costs[form:arcsin_scaled=2 + dress:spec_scale=1.5 + spec:allow_invtrig=2 ⇒ 5.5] · D=16` |
| 16 | $\int  -2\frac{1}{4+16x^{2}}\,dx$ | $-2\frac{1}{8}\arctan\left(\frac{4x}{2}\right)+C$ | `invtrig` | `spec_pack=integral_invtrig · tricks=[invtrig] · form_id=arctan_scaled · dress=[constant_multiple,sign] · costs[form:arctan_scaled=2 + dress:spec_scale=1.5 + dress:spec_sign=0.5 + spec:allow_invtrig=2 ⇒ 6] · D=16` |
| 20 | $\int  4\frac{1}{4+4x^{2}}\,dx$ | $4\frac{1}{4}\arctan\left(\frac{2x}{2}\right)+C$ | `invtrig` | `spec_pack=integral_invtrig · tricks=[invtrig] · form_id=arctan_scaled · dress=[constant_multiple,sign] · costs[form:arctan_scaled=2 + dress:spec_scale=1.5 + dress:spec_sign=0.5 + spec:allow_invtrig=2 ⇒ 6] · D=20` |
| 20 | $\int  -\frac{1}{1+x^{2}}\,dx$ | $-\arctan(x)+C$ | `invtrig` | `spec_pack=integral_invtrig · tricks=[invtrig] · form_id=arctan_basic · dress=[sign] · costs[form:arctan_basic=2 + dress:spec_sign=0.5 + spec:allow_invtrig=2 ⇒ 4.5] · D=20` |
| 20 | $\int  -2\frac{1}{\sqrt{9-x^{2}}}\,dx$ | $-2\arcsin\left(\frac{x}{3}\right)+C$ | `invtrig` | `spec_pack=integral_invtrig · tricks=[invtrig] · form_id=arcsin_a2 · dress=[sign,constant_multiple] · costs[form:arcsin_a2=2 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:allow_invtrig=2 ⇒ 6] · D=20` |
| 25 | $\int  -3\frac{1}{\sqrt{1-x^{2}}}\,dx$ | $-3\arcsin(x)+C$ | `invtrig` | `spec_pack=integral_invtrig · tricks=[invtrig] · form_id=arcsin_basic · dress=[constant_multiple] · costs[form:arcsin_basic=2 + dress:spec_scale=1.5 + spec:allow_invtrig=2 ⇒ 5.5] · D=25` |
| 25 | $\int  -2\frac{1}{\sqrt{25-x^{2}}}\,dx$ | $-2\arcsin\left(\frac{x}{5}\right)+C$ | `invtrig` | `spec_pack=integral_invtrig · tricks=[invtrig] · form_id=arcsin_a2 · dress=[constant_multiple,sign] · costs[form:arcsin_a2=2 + dress:spec_scale=1.5 + dress:spec_sign=0.5 + spec:allow_invtrig=2 ⇒ 6] · D=25` |
| 25 | $\int  -3\frac{1}{16+x^{2}}\,dx$ | $-3\frac{1}{4}\arctan\left(\frac{x}{4}\right)+C$ | `invtrig` | `spec_pack=integral_invtrig · tricks=[invtrig] · form_id=arctan_a2 · dress=[sign,constant_multiple] · costs[form:arctan_a2=2 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:allow_invtrig=2 ⇒ 6] · D=25` |

## Integrals — substitution (power)

<a id="int_sub"></a>

`calc_indef_int_power_rule_with_substitution` · pack `int_sub` · topic label: c1: Power rule with substitution · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **5** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `du_over_u_linear` | 7 |
| `power_linear_du` | 6 |
| `alteration_linear_over_root` | 4 |
| `power_quad_x_du` | 4 |
| `root_quad_x_du` | 3 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\int 4\left(4x - 3\right)^{3}\,dx$ | $\frac{1}{4}\left(4x - 3\right)^{4}+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=power_linear_du · costs[form:power_linear_du=1 ⇒ 1] · D=0` |
| 0 | $\int 4\left(4x + 5\right)^{2}\,dx$ | $\frac{1}{3}\left(4x + 5\right)^{3}+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=power_linear_du · costs[form:power_linear_du=1 ⇒ 1] · D=0` |
| 0 | $\int 3\left(3x - 5\right)^{2}\,dx$ | $\frac{1}{3}\left(3x - 5\right)^{3}+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=power_linear_du · costs[form:power_linear_du=1 ⇒ 1] · D=0` |
| 3 | $\int \frac{4}{4x + 3}\,dx$ | $\ln\|4x + 3\|+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=du_over_u_linear · costs[form:du_over_u_linear=2 + spec:allow_log=1.5 ⇒ 3.5] · D=3` |
| 3 | $\int 3\left(3x + 6\right)^{2}\,dx$ | $\frac{1}{3}\left(3x + 6\right)^{3}+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=power_linear_du · costs[form:power_linear_du=1 ⇒ 1] · D=3` |
| 3 | $\int \frac{4}{4x + 4}\,dx$ | $\ln\|4x + 4\|+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=du_over_u_linear · costs[form:du_over_u_linear=2 + spec:allow_log=1.5 ⇒ 3.5] · D=3` |
| 6 | $\int  -x\sqrt{x^{2}+5}\,dx$ | $-\left(\frac{1}{3}\left(x^{2}+5\right)^{\frac{3}{2}}\right)+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=root_quad_x_du · dress=[sign] · costs[form:root_quad_x_du=2 + dress:spec_sign=0.5 ⇒ 2.5] · D=6` |
| 6 | $\int  -3\frac{4}{4x + 2}\,dx$ | $-3\left(\ln\|4x + 2\|\right)+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=du_over_u_linear · dress=[constant_multiple] · costs[form:du_over_u_linear=2 + dress:spec_scale=1.5 + spec:allow_log=1.5 ⇒ 5] · D=6` |
| 6 | $\int  -4\left(2\left(2x - 6\right)^{4}\right)\,dx$ | $-4\left(\frac{1}{5}\left(2x - 6\right)^{5}\right)+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=power_linear_du · dress=[constant_multiple] · costs[form:power_linear_du=1 + dress:spec_scale=1.5 ⇒ 2.5] · D=6` |
| 8 | $\int  -\left(2\left(2x - 3\right)^{3}\right)\,dx$ | $-\left(\frac{1}{4}\left(2x - 3\right)^{4}\right)+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=power_linear_du · dress=[sign] · costs[form:power_linear_du=1 + dress:spec_sign=0.5 ⇒ 1.5] · D=8` |
| 8 | $\int  -\left(2x\left(x^{2}+3\right)^{3}\right)\,dx$ | $-\left(\frac{1}{4}\left(x^{2}+3\right)^{4}\right)+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=power_quad_x_du · dress=[sign] · costs[form:power_quad_x_du=1 + dress:spec_sign=0.5 ⇒ 1.5] · D=8` |
| 8 | $\int  -\left(2x\left(x^{2}+1\right)^{2}\right)\,dx$ | $-\left(\frac{1}{3}\left(x^{2}+1\right)^{3}\right)+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=power_quad_x_du · dress=[sign] · costs[form:power_quad_x_du=1 + dress:spec_sign=0.5 ⇒ 1.5] · D=8` |
| 12 | $\int  -\frac{x}{\sqrt{x-1}}\,dx$ | $-\left(\frac{2}{3}\left(x-1\right)^{\frac{3}{2}}+2\sqrt{x-1}\right)+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=alteration_linear_over_root · dress=[sign] · costs[form:alteration_linear_over_root=2 + dress:spec_sign=0.5 ⇒ 2.5] · D=12` |
| 12 | $\int  -\left(2x\left(x^{2}+6\right)^{2}\right)\,dx$ | $-\left(\frac{1}{3}\left(x^{2}+6\right)^{3}\right)+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=power_quad_x_du · dress=[sign] · costs[form:power_quad_x_du=1 + dress:spec_sign=0.5 ⇒ 1.5] · D=12` |
| 12 | $\int  -3x\sqrt{x^{2}+5}\,dx$ | $-3\left(\frac{1}{3}\left(x^{2}+5\right)^{\frac{3}{2}}\right)+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=root_quad_x_du · dress=[constant_multiple] · costs[form:root_quad_x_du=2 + dress:spec_scale=1.5 ⇒ 3.5] · D=12` |
| 16 | $\int  -\frac{4}{4x - 5}\,dx$ | $-\left(\ln\|4x - 5\|\right)+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=du_over_u_linear · dress=[sign] · costs[form:du_over_u_linear=2 + dress:spec_sign=0.5 + spec:allow_log=1.5 ⇒ 4] · D=16` |
| 16 | $\int  3\frac{2}{2x - 2}\,dx$ | $3\left(\ln\|2x - 2\|\right)+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=du_over_u_linear · dress=[constant_multiple,sign] · costs[form:du_over_u_linear=2 + dress:spec_scale=1.5 + dress:spec_sign=0.5 + spec:allow_log=1.5 ⇒ 5.5] · D=16` |
| 16 | $\int  -4\frac{4}{4x + 7}\,dx$ | $-4\left(\ln\|4x + 7\|\right)+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=du_over_u_linear · dress=[sign,constant_multiple] · costs[form:du_over_u_linear=2 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:allow_log=1.5 ⇒ 5.5] · D=16` |
| 20 | $\int  -\frac{3}{3x + 5}\,dx$ | $-\left(\ln\|3x + 5\|\right)+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=du_over_u_linear · dress=[sign] · costs[form:du_over_u_linear=2 + dress:spec_sign=0.5 + spec:allow_log=1.5 ⇒ 4] · D=20` |
| 20 | $\int  4\frac{x}{\sqrt{x-2}}\,dx$ | $4\left(\frac{2}{3}\left(x-2\right)^{\frac{3}{2}}+4\sqrt{x-2}\right)+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=alteration_linear_over_root · dress=[constant_multiple,sign] · costs[form:alteration_linear_over_root=2 + dress:spec_scale=1.5 + dress:spec_sign=0.5 ⇒ 4] · D=20` |
| 20 | $\int  4\frac{x}{\sqrt{x-1}}\,dx$ | $4\left(\frac{2}{3}\left(x-1\right)^{\frac{3}{2}}+2\sqrt{x-1}\right)+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=alteration_linear_over_root · dress=[sign,constant_multiple] · costs[form:alteration_linear_over_root=2 + dress:spec_sign=0.5 + dress:spec_scale=1.5 ⇒ 4] · D=20` |
| 25 | $\int  -\frac{x}{\sqrt{x-2}}\,dx$ | $-\left(\frac{2}{3}\left(x-2\right)^{\frac{3}{2}}+4\sqrt{x-2}\right)+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=alteration_linear_over_root · dress=[sign] · costs[form:alteration_linear_over_root=2 + dress:spec_sign=0.5 ⇒ 2.5] · D=25` |
| 25 | $\int  -x\sqrt{x^{2}+5}\,dx$ | $-\left(\frac{1}{3}\left(x^{2}+5\right)^{\frac{3}{2}}\right)+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=root_quad_x_du · dress=[sign] · costs[form:root_quad_x_du=2 + dress:spec_sign=0.5 ⇒ 2.5] · D=25` |
| 25 | $\int  -3\left(2x\left(x^{2}+5\right)^{3}\right)\,dx$ | $-3\left(\frac{1}{4}\left(x^{2}+5\right)^{4}\right)+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=power_quad_x_du · dress=[constant_multiple,sign] · costs[form:power_quad_x_du=1 + dress:spec_scale=1.5 + dress:spec_sign=0.5 ⇒ 3] · D=25` |

## Integrals — log/exp with substitution

<a id="int_log_exp_sub"></a>

`calc_indef_int_logarithmic_rule_and_exponentials_with_substitution` · pack `int_log_exp_sub` · topic label: c1: Logarithmic rule and exponentials with subs. · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **5** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `du_over_u_linear` | 10 |
| `du_over_u_trig` | 4 |
| `exp_of_poly` | 4 |
| `exp_of_trig` | 3 |
| `nested_trig_exp` | 3 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\int \frac{\cos(x)}{\sin^{2}(x)}\,dx$ | $-\frac{1}{\sin(x)}+C$ | `u_sub` | `spec_pack=integral_log_exp_sub · tricks=[u_sub] · form_id=du_over_u_trig · costs[form:du_over_u_trig=2 + spec:allow_trig=1.5 ⇒ 3.5] · D=0` |
| 0 | $\int 4e^{4x + 2}\,dx$ | $e^{4x + 2}+C$ | `u_sub` | `spec_pack=integral_log_exp_sub · tricks=[u_sub] · form_id=exp_of_poly · costs[form:exp_of_poly=2 + spec:allow_exp=1.5 ⇒ 3.5] · D=0` |
| 0 | $\int 4e^{4x - 2}\,dx$ | $e^{4x - 2}+C$ | `u_sub` | `spec_pack=integral_log_exp_sub · tricks=[u_sub] · form_id=exp_of_poly · costs[form:exp_of_poly=2 + spec:allow_exp=1.5 ⇒ 3.5] · D=0` |
| 3 | $\int \frac{4}{4x - 2}\,dx$ | $\ln\|4x - 2\|+C$ | `u_sub` | `spec_pack=integral_log_exp_sub · tricks=[u_sub] · form_id=du_over_u_linear · costs[form:du_over_u_linear=2 + spec:allow_log=1.5 ⇒ 3.5] · D=3` |
| 3 | $\int \frac{4}{4x}\,dx$ | $\ln\|4x\|+C$ | `u_sub` | `spec_pack=integral_log_exp_sub · tricks=[u_sub] · form_id=du_over_u_linear · costs[form:du_over_u_linear=2 + spec:allow_log=1.5 ⇒ 3.5] · D=3` |
| 3 | $\int \frac{2}{2x + 1}\,dx$ | $\ln\|2x + 1\|+C$ | `u_sub` | `spec_pack=integral_log_exp_sub · tricks=[u_sub] · form_id=du_over_u_linear · costs[form:du_over_u_linear=2 + spec:allow_log=1.5 ⇒ 3.5] · D=3` |
| 6 | $\int \frac{\cos(x)}{\sin^{2}(x)}\,dx$ | $-\frac{1}{\sin(x)}+C$ | `u_sub` | `spec_pack=integral_log_exp_sub · tricks=[u_sub] · form_id=du_over_u_trig · costs[form:du_over_u_trig=2 + spec:allow_trig=1.5 ⇒ 3.5] · D=6` |
| 6 | $\int \frac{\sin(x)}{\cos^{3}(x)}\,dx$ | $\frac{1}{2}\sec^{2}(x)+C$ | `u_sub` | `spec_pack=integral_log_exp_sub · tricks=[u_sub] · form_id=du_over_u_trig · costs[form:du_over_u_trig=2 + spec:allow_trig=1.5 ⇒ 3.5] · D=6` |
| 6 | $\int \frac{\cos(x)}{\sin^{2}(x)}\,dx$ | $-\frac{1}{\sin(x)}+C$ | `u_sub` | `spec_pack=integral_log_exp_sub · tricks=[u_sub] · form_id=du_over_u_trig · costs[form:du_over_u_trig=2 + spec:allow_trig=1.5 ⇒ 3.5] · D=6` |
| 8 | $\int  -e^{\cos(x)}\sin(x)\,dx$ | $e^{\cos(x)}+C$ | `u_sub` | `spec_pack=integral_log_exp_sub · tricks=[u_sub] · form_id=exp_of_trig · dress=[sign] · costs[form:exp_of_trig=2 + dress:spec_sign=0.5 + spec:allow_exp=1.5 + spec:allow_trig=1.5 ⇒ 5.5] · D=8` |
| 8 | $\int  -\frac{4}{4x + 1}\,dx$ | $-\left(\ln\|4x + 1\|\right)+C$ | `u_sub` | `spec_pack=integral_log_exp_sub · tricks=[u_sub] · form_id=du_over_u_linear · dress=[sign] · costs[form:du_over_u_linear=2 + dress:spec_sign=0.5 + spec:allow_log=1.5 ⇒ 4] · D=8` |
| 8 | $\int \frac{3}{3x - 3}\,dx$ | $\ln\|3x - 3\|+C$ | `u_sub` | `spec_pack=integral_log_exp_sub · tricks=[u_sub] · form_id=du_over_u_linear · costs[form:du_over_u_linear=2 + spec:allow_log=1.5 ⇒ 3.5] · D=8` |
| 12 | $\int  2e^{\sin(x)}\cos(x)\,dx$ | $2e^{\sin(x)}+C$ | `u_sub` | `spec_pack=integral_log_exp_sub · tricks=[u_sub] · form_id=exp_of_trig · dress=[constant_multiple] · costs[form:exp_of_trig=2 + dress:spec_scale=1.5 + spec:allow_exp=1.5 + spec:allow_trig=1.5 ⇒ 6.5] · D=12` |
| 12 | $\int  3\frac{2}{2x - 1}\,dx$ | $3\left(\ln\|2x - 1\|\right)+C$ | `u_sub` | `spec_pack=integral_log_exp_sub · tricks=[u_sub] · form_id=du_over_u_linear · dress=[constant_multiple] · costs[form:du_over_u_linear=2 + dress:spec_scale=1.5 + spec:allow_log=1.5 ⇒ 5] · D=12` |
| 12 | $\int  -\frac{3}{3x + 2}\,dx$ | $-\left(\ln\|3x + 2\|\right)+C$ | `u_sub` | `spec_pack=integral_log_exp_sub · tricks=[u_sub] · form_id=du_over_u_linear · dress=[sign] · costs[form:du_over_u_linear=2 + dress:spec_sign=0.5 + spec:allow_log=1.5 ⇒ 4] · D=12` |
| 16 | $\int  -16e^{4x + 1}\,dx$ | $-4e^{4x + 1}+C$ | `u_sub` | `spec_pack=integral_log_exp_sub · tricks=[u_sub] · form_id=exp_of_poly · dress=[constant_multiple,sign] · costs[form:exp_of_poly=2 + dress:spec_scale=1.5 + dress:spec_sign=0.5 + spec:allow_exp=1.5 ⇒ 5.5] · D=16` |
| 16 | $\int  2e^{\cos(3x)}\sin(3x)\,dx$ | $-2\frac{1}{3}e^{\cos(3x)}+C$ | `u_sub` | `spec_pack=integral_log_exp_sub · tricks=[u_sub] · form_id=nested_trig_exp · dress=[constant_multiple,sign] · costs[form:nested_trig_exp=2 + dress:spec_scale=1.5 + dress:spec_sign=0.5 + spec:allow_exp=1.5 + spec:allow_trig=1.5 ⇒ 7] · D=16` |
| 16 | $\int  -e^{\cos(3x)}\sin(3x)\,dx$ | $\frac{1}{3}e^{\cos(3x)}+C$ | `u_sub` | `spec_pack=integral_log_exp_sub · tricks=[u_sub] · form_id=nested_trig_exp · dress=[sign] · costs[form:nested_trig_exp=2 + dress:spec_sign=0.5 + spec:allow_exp=1.5 + spec:allow_trig=1.5 ⇒ 5.5] · D=16` |
| 20 | $\int  2\frac{3}{3x + 3}\,dx$ | $2\left(\ln\|3x + 3\|\right)+C$ | `u_sub` | `spec_pack=integral_log_exp_sub · tricks=[u_sub] · form_id=du_over_u_linear · dress=[constant_multiple,sign] · costs[form:du_over_u_linear=2 + dress:spec_scale=1.5 + dress:spec_sign=0.5 + spec:allow_log=1.5 ⇒ 5.5] · D=20` |
| 20 | $\int  3e^{\sin(x)}\cos(x)\,dx$ | $3e^{\sin(x)}+C$ | `u_sub` | `spec_pack=integral_log_exp_sub · tricks=[u_sub] · form_id=exp_of_trig · dress=[sign,constant_multiple] · costs[form:exp_of_trig=2 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:allow_exp=1.5 + spec:allow_trig=1.5 ⇒ 7] · D=20` |
| 20 | $\int  -3e^{\cos(3x)}\sin(3x)\,dx$ | $3\frac{1}{3}e^{\cos(3x)}+C$ | `u_sub` | `spec_pack=integral_log_exp_sub · tricks=[u_sub] · form_id=nested_trig_exp · dress=[constant_multiple,sign] · costs[form:nested_trig_exp=2 + dress:spec_scale=1.5 + dress:spec_sign=0.5 + spec:allow_exp=1.5 + spec:allow_trig=1.5 ⇒ 7] · D=20` |
| 25 | $\int  -3\frac{4}{4x + 8}\,dx$ | $-3\left(\ln\|4x + 8\|\right)+C$ | `u_sub` | `spec_pack=integral_log_exp_sub · tricks=[u_sub] · form_id=du_over_u_linear · dress=[constant_multiple,sign] · costs[form:du_over_u_linear=2 + dress:spec_scale=1.5 + dress:spec_sign=0.5 + spec:allow_log=1.5 ⇒ 5.5] · D=25` |
| 25 | $\int  4\frac{4}{4x - 9}\,dx$ | $4\left(\ln\|4x - 9\|\right)+C$ | `u_sub` | `spec_pack=integral_log_exp_sub · tricks=[u_sub] · form_id=du_over_u_linear · dress=[constant_multiple] · costs[form:du_over_u_linear=2 + dress:spec_scale=1.5 + spec:allow_log=1.5 ⇒ 5] · D=25` |
| 25 | $\int  6e^{3x - 3}\,dx$ | $2e^{3x - 3}+C$ | `u_sub` | `spec_pack=integral_log_exp_sub · tricks=[u_sub] · form_id=exp_of_poly · dress=[constant_multiple] · costs[form:exp_of_poly=2 + dress:spec_scale=1.5 + spec:allow_exp=1.5 ⇒ 5] · D=25` |

## Integrals — trigonometric substitution

<a id="int_trig_sub"></a>

`calc_indef_int_trigonometric_with_substitution` · pack `int_trig_sub` · topic label: c1: Trigonometric substitution · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **8** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `sqrt_a2_minus_x2` | 8 |
| `one_over_sqrt_x2_minus_a2` | 4 |
| `one_over_sqrt_x2_plus_a2` | 3 |
| `sqrt_a2_plus_x2` | 3 |
| `x2_over_sqrt_a2_minus_x2` | 3 |
| `pow_5_2_a2_minus` | 1 |
| `pow_m3_2_a2_minus` | 1 |
| `pow_m3_2_a2_plus` | 1 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\int \sqrt{16-x^{2}}\,dx$ | $\frac{1}{2}x\sqrt{16-x^{2}}+8\arcsin\left(\frac{x}{4}\right)+C$ | `trig_sub` | `spec_pack=integral_trig_sub · tricks=[trig_sub] · form_id=sqrt_a2_minus_x2 · costs[form:sqrt_a2_minus_x2=2 + spec:allow_trig=1.5 ⇒ 3.5] · D=0` |
| 0 | $\int \sqrt{4-x^{2}}\,dx$ | $\frac{1}{2}x\sqrt{4-x^{2}}+2\arcsin\left(\frac{x}{2}\right)+C$ | `trig_sub` | `spec_pack=integral_trig_sub · tricks=[trig_sub] · form_id=sqrt_a2_minus_x2 · costs[form:sqrt_a2_minus_x2=2 + spec:allow_trig=1.5 ⇒ 3.5] · D=0` |
| 0 | $\int \sqrt{16-x^{2}}\,dx$ | $\frac{1}{2}x\sqrt{16-x^{2}}+8\arcsin\left(\frac{x}{4}\right)+C$ | `trig_sub` | `spec_pack=integral_trig_sub · tricks=[trig_sub] · form_id=sqrt_a2_minus_x2 · costs[form:sqrt_a2_minus_x2=2 + spec:allow_trig=1.5 ⇒ 3.5] · D=0` |
| 3 | $\int \sqrt{25-x^{2}}\,dx$ | $\frac{1}{2}x\sqrt{25-x^{2}}+\frac{25}{2}\arcsin\left(\frac{x}{5}\right)+C$ | `trig_sub` | `spec_pack=integral_trig_sub · tricks=[trig_sub] · form_id=sqrt_a2_minus_x2 · costs[form:sqrt_a2_minus_x2=2 + spec:allow_trig=1.5 ⇒ 3.5] · D=3` |
| 3 | $\int \sqrt{25+x^{2}}\,dx$ | $\frac{1}{2}x\sqrt{25+x^{2}}+\frac{25}{2}\ln\left\|x+\sqrt{25+x^{2}}\right\|+C$ | `trig_sub` | `spec_pack=integral_trig_sub · tricks=[trig_sub] · form_id=sqrt_a2_plus_x2 · costs[form:sqrt_a2_plus_x2=2 + spec:allow_trig=1.5 ⇒ 3.5] · D=3` |
| 3 | $\int \sqrt{16-x^{2}}\,dx$ | $\frac{1}{2}x\sqrt{16-x^{2}}+8\arcsin\left(\frac{x}{4}\right)+C$ | `trig_sub` | `spec_pack=integral_trig_sub · tricks=[trig_sub] · form_id=sqrt_a2_minus_x2 · costs[form:sqrt_a2_minus_x2=2 + spec:allow_trig=1.5 ⇒ 3.5] · D=3` |
| 6 | $\int  -\frac{1}{\sqrt{x^{2}-25}}\,dx$ | $-\left(\ln\left\|x+\sqrt{x^{2}-25}\right\|\right)+C$ | `trig_sub` | `spec_pack=integral_trig_sub · tricks=[trig_sub] · form_id=one_over_sqrt_x2_minus_a2 · dress=[sign] · costs[form:one_over_sqrt_x2_minus_a2=2 + dress:spec_sign=0.5 + spec:allow_trig=1.5 ⇒ 4] · D=6` |
| 6 | $\int  -\sqrt{9-x^{2}}\,dx$ | $-\left(\frac{1}{2}x\sqrt{9-x^{2}}+\frac{9}{2}\arcsin\left(\frac{x}{3}\right)\right)+C$ | `trig_sub` | `spec_pack=integral_trig_sub · tricks=[trig_sub] · form_id=sqrt_a2_minus_x2 · dress=[sign] · costs[form:sqrt_a2_minus_x2=2 + dress:spec_sign=0.5 + spec:allow_trig=1.5 ⇒ 4] · D=6` |
| 6 | $\int  2\frac{1}{\sqrt{x^{2}+9}}\,dx$ | $2\left(\ln\left\|x+\sqrt{x^{2}+9}\right\|\right)+C$ | `trig_sub` | `spec_pack=integral_trig_sub · tricks=[trig_sub] · form_id=one_over_sqrt_x2_plus_a2 · dress=[constant_multiple] · costs[form:one_over_sqrt_x2_plus_a2=2 + dress:spec_scale=1.5 + spec:allow_trig=1.5 ⇒ 5] · D=6` |
| 8 | $\int  -\sqrt{4+x^{2}}\,dx$ | $-\left(\frac{1}{2}x\sqrt{4+x^{2}}+2\ln\left\|x+\sqrt{4+x^{2}}\right\|\right)+C$ | `trig_sub` | `spec_pack=integral_trig_sub · tricks=[trig_sub] · form_id=sqrt_a2_plus_x2 · dress=[sign] · costs[form:sqrt_a2_plus_x2=2 + dress:spec_sign=0.5 + spec:allow_trig=1.5 ⇒ 4] · D=8` |
| 8 | $\int \frac{x^{2}}{\sqrt{25-x^{2}}}\,dx$ | $-\frac{1}{2}x\sqrt{25-x^{2}}+\frac{25}{2}\arcsin\left(\frac{x}{5}\right)+C$ | `trig_sub` | `spec_pack=integral_trig_sub · tricks=[trig_sub] · form_id=x2_over_sqrt_a2_minus_x2 · costs[form:x2_over_sqrt_a2_minus_x2=2 + spec:allow_trig=1.5 ⇒ 3.5] · D=8` |
| 8 | $\int \sqrt{4-x^{2}}\,dx$ | $\frac{1}{2}x\sqrt{4-x^{2}}+2\arcsin\left(\frac{x}{2}\right)+C$ | `trig_sub` | `spec_pack=integral_trig_sub · tricks=[trig_sub] · form_id=sqrt_a2_minus_x2 · costs[form:sqrt_a2_minus_x2=2 + spec:allow_trig=1.5 ⇒ 3.5] · D=8` |
| 12 | $\int  -3\frac{1}{\sqrt{\left(x + 3\right)^{2}-25}}\,dx$ | $-3\left(\ln\left\|x + 3+\sqrt{\left(x + 3\right)^{2}-25}\right\|\right)+C$ | `u_sub,trig_sub` | `spec_pack=integral_trig_sub · tricks=[u_sub,trig_sub] · form_id=one_over_sqrt_x2_minus_a2 · dress=[constant_multiple] · costs[form:one_over_sqrt_x2_minus_a2=2 + dress:spec_scale=1.5 + spec:allow_trig=1.5 ⇒ 5] · D=12` |
| 12 | $\int  -4\frac{x^{2}}{\sqrt{4-x^{2}}}\,dx$ | $4\left(\frac{1}{2}x\sqrt{4-x^{2}}+2\arcsin\left(\frac{x}{2}\right)\right)+C$ | `trig_sub` | `spec_pack=integral_trig_sub · tricks=[trig_sub] · form_id=x2_over_sqrt_a2_minus_x2 · dress=[constant_multiple] · costs[form:x2_over_sqrt_a2_minus_x2=2 + dress:spec_scale=1.5 + spec:allow_trig=1.5 ⇒ 5] · D=12` |
| 12 | $\int  -4\frac{1}{\left(9+\left(x + 2\right)^{2}\right)^{\frac{3}{2}}}\,dx$ | $-4\frac{x + 2}{9\sqrt{9+\left(x + 2\right)^{2}}}+C$ | `u_sub,trig_sub` | `spec_pack=integral_trig_sub · tricks=[u_sub,trig_sub] · form_id=pow_m3_2_a2_plus · dress=[constant_multiple] · costs[form:pow_m3_2_a2_plus=2 + dress:spec_scale=1.5 + spec:allow_trig=1.5 ⇒ 5] · D=12` |
| 16 | $\int  -2\frac{1}{\sqrt{\left(x + 1\right)^{2}+16}}\,dx$ | $-2\left(\ln\left\|x + 1+\sqrt{\left(x + 1\right)^{2}+16}\right\|\right)+C$ | `u_sub,trig_sub` | `spec_pack=integral_trig_sub · tricks=[u_sub,trig_sub] · form_id=one_over_sqrt_x2_plus_a2 · dress=[sign,constant_multiple] · costs[form:one_over_sqrt_x2_plus_a2=2 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:allow_trig=1.5 ⇒ 5.5] · D=16` |
| 16 | $\int  -\frac{x^{2}}{\sqrt{16-x^{2}}}\,dx$ | $\frac{1}{2}x\sqrt{16-x^{2}}+8\arcsin\left(\frac{x}{4}\right)+C$ | `trig_sub` | `spec_pack=integral_trig_sub · tricks=[trig_sub] · form_id=x2_over_sqrt_a2_minus_x2 · dress=[sign] · costs[form:x2_over_sqrt_a2_minus_x2=2 + dress:spec_sign=0.5 + spec:allow_trig=1.5 ⇒ 4] · D=16` |
| 16 | $\int  -\left(\left(25-x^{2}\right)^{\frac{5}{2}}\right)\,dx$ | $-\left(\frac{x}{48}\left(8x^{2}^{2}+1025x^{2}+1525^{2}\right)\sqrt{25-x^{2}}+\frac{15625}{16}\arcsin\left(\frac{x}{5}\right)\right)+C$ | `trig_sub` | `spec_pack=integral_trig_sub · tricks=[trig_sub] · form_id=pow_5_2_a2_minus · dress=[sign] · costs[form:pow_5_2_a2_minus=2 + dress:spec_sign=0.5 + spec:allow_trig=1.5 ⇒ 4] · D=16` |
| 20 | $\int  -3\frac{1}{\sqrt{x^{2}+9}}\,dx$ | $-3\left(\ln\left\|x+\sqrt{x^{2}+9}\right\|\right)+C$ | `trig_sub` | `spec_pack=integral_trig_sub · tricks=[trig_sub] · form_id=one_over_sqrt_x2_plus_a2 · dress=[constant_multiple] · costs[form:one_over_sqrt_x2_plus_a2=2 + dress:spec_scale=1.5 + spec:allow_trig=1.5 ⇒ 5] · D=20` |
| 20 | $\int  -\sqrt{9+x^{2}}\,dx$ | $-\left(\frac{1}{2}x\sqrt{9+x^{2}}+\frac{9}{2}\ln\left\|x+\sqrt{9+x^{2}}\right\|\right)+C$ | `trig_sub` | `spec_pack=integral_trig_sub · tricks=[trig_sub] · form_id=sqrt_a2_plus_x2 · dress=[sign] · costs[form:sqrt_a2_plus_x2=2 + dress:spec_sign=0.5 + spec:allow_trig=1.5 ⇒ 4] · D=20` |
| 20 | $\int  -\sqrt{4-\left(x - 2\right)^{2}}\,dx$ | $-\left(\frac{1}{2}\left(x - 2\right)\sqrt{4-\left(x - 2\right)^{2}}+2\arcsin\left(\frac{x - 2}{2}\right)\right)+C$ | `u_sub,trig_sub` | `spec_pack=integral_trig_sub · tricks=[u_sub,trig_sub] · form_id=sqrt_a2_minus_x2 · dress=[sign] · costs[form:sqrt_a2_minus_x2=2 + dress:spec_sign=0.5 + spec:allow_trig=1.5 ⇒ 4] · D=20` |
| 25 | $\int  3\frac{1}{\left(4-\left(x + 3\right)^{2}\right)^{\frac{3}{2}}}\,dx$ | $3\frac{x + 3}{4\sqrt{4-\left(x + 3\right)^{2}}}+C$ | `u_sub,trig_sub` | `spec_pack=integral_trig_sub · tricks=[u_sub,trig_sub] · form_id=pow_m3_2_a2_minus · dress=[sign,constant_multiple] · costs[form:pow_m3_2_a2_minus=2 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:allow_trig=1.5 ⇒ 5.5] · D=25` |
| 25 | $\int  -\frac{1}{\sqrt{x^{2}-25}}\,dx$ | $-\left(\ln\left\|x+\sqrt{x^{2}-25}\right\|\right)+C$ | `trig_sub` | `spec_pack=integral_trig_sub · tricks=[trig_sub] · form_id=one_over_sqrt_x2_minus_a2 · dress=[sign] · costs[form:one_over_sqrt_x2_minus_a2=2 + dress:spec_sign=0.5 + spec:allow_trig=1.5 ⇒ 4] · D=25` |
| 25 | $\int  3\frac{1}{\sqrt{\left(x - 2\right)^{2}-4}}\,dx$ | $3\left(\ln\left\|x - 2+\sqrt{\left(x - 2\right)^{2}-4}\right\|\right)+C$ | `u_sub,trig_sub` | `spec_pack=integral_trig_sub · tricks=[u_sub,trig_sub] · form_id=one_over_sqrt_x2_minus_a2 · dress=[constant_multiple] · costs[form:one_over_sqrt_x2_minus_a2=2 + dress:spec_scale=1.5 + spec:allow_trig=1.5 ⇒ 5] · D=25` |

## Integrals — invtrig with substitution

<a id="int_invtrig_sub"></a>

`calc_indef_int_inverse_trigonometric_with_substitution` · pack `int_invtrig_sub` · topic label: c1: Inverse trigonometric with substitution · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **3** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `power_linear_du` | 12 |
| `arctan_of_linear` | 6 |
| `du_over_u_linear` | 6 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\int 4\left(4x + 1\right)^{2}\,dx$ | $\frac{1}{3}\left(4x + 1\right)^{3}+C$ | `u_sub` | `spec_pack=integral_invtrig_sub · tricks=[u_sub] · form_id=power_linear_du · costs[form:power_linear_du=1 ⇒ 1] · D=0` |
| 0 | $\int 4\left(4x - 3\right)^{2}\,dx$ | $\frac{1}{3}\left(4x - 3\right)^{3}+C$ | `u_sub` | `spec_pack=integral_invtrig_sub · tricks=[u_sub] · form_id=power_linear_du · costs[form:power_linear_du=1 ⇒ 1] · D=0` |
| 0 | $\int 4\left(4x - 4\right)^{2}\,dx$ | $\frac{1}{3}\left(4x - 4\right)^{3}+C$ | `u_sub` | `spec_pack=integral_invtrig_sub · tricks=[u_sub] · form_id=power_linear_du · costs[form:power_linear_du=1 ⇒ 1] · D=0` |
| 3 | $\int 2\left(2x + 4\right)^{3}\,dx$ | $\frac{1}{4}\left(2x + 4\right)^{4}+C$ | `u_sub` | `spec_pack=integral_invtrig_sub · tricks=[u_sub] · form_id=power_linear_du · costs[form:power_linear_du=1 ⇒ 1] · D=3` |
| 3 | $\int 3\left(3x - 1\right)^{2}\,dx$ | $\frac{1}{3}\left(3x - 1\right)^{3}+C$ | `u_sub` | `spec_pack=integral_invtrig_sub · tricks=[u_sub] · form_id=power_linear_du · costs[form:power_linear_du=1 ⇒ 1] · D=3` |
| 3 | $\int \frac{2}{2x - 2}\,dx$ | $\ln\|2x - 2\|+C$ | `u_sub` | `spec_pack=integral_invtrig_sub · tricks=[u_sub] · form_id=du_over_u_linear · costs[form:du_over_u_linear=2 + spec:allow_log=1.5 ⇒ 3.5] · D=3` |
| 6 | $\int 3\left(3x + 2\right)^{5}\,dx$ | $\frac{1}{6}\left(3x + 2\right)^{6}+C$ | `u_sub` | `spec_pack=integral_invtrig_sub · tricks=[u_sub] · form_id=power_linear_du · costs[form:power_linear_du=1 ⇒ 1] · D=6` |
| 6 | $\int \frac{2}{2x + 1}\,dx$ | $\ln\|2x + 1\|+C$ | `u_sub` | `spec_pack=integral_invtrig_sub · tricks=[u_sub] · form_id=du_over_u_linear · costs[form:du_over_u_linear=2 + spec:allow_log=1.5 ⇒ 3.5] · D=6` |
| 6 | $\int  -\frac{3}{3x + 5}\,dx$ | $-\left(\ln\|3x + 5\|\right)+C$ | `u_sub` | `spec_pack=integral_invtrig_sub · tricks=[u_sub] · form_id=du_over_u_linear · dress=[sign] · costs[form:du_over_u_linear=2 + dress:spec_sign=0.5 + spec:allow_log=1.5 ⇒ 4] · D=6` |
| 8 | $\int  3\left(4\left(4x - 3\right)^{2}\right)\,dx$ | $3\left(\frac{1}{3}\left(4x - 3\right)^{3}\right)+C$ | `u_sub` | `spec_pack=integral_invtrig_sub · tricks=[u_sub] · form_id=power_linear_du · dress=[constant_multiple] · costs[form:power_linear_du=1 + dress:spec_scale=1.5 ⇒ 2.5] · D=8` |
| 8 | $\int  3\left(4\left(4x + 2\right)^{4}\right)\,dx$ | $3\left(\frac{1}{5}\left(4x + 2\right)^{5}\right)+C$ | `u_sub` | `spec_pack=integral_invtrig_sub · tricks=[u_sub] · form_id=power_linear_du · dress=[constant_multiple] · costs[form:power_linear_du=1 + dress:spec_scale=1.5 ⇒ 2.5] · D=8` |
| 8 | $\int  -3\frac{3}{3x + 1}\,dx$ | $-3\left(\ln\|3x + 1\|\right)+C$ | `u_sub` | `spec_pack=integral_invtrig_sub · tricks=[u_sub] · form_id=du_over_u_linear · dress=[constant_multiple] · costs[form:du_over_u_linear=2 + dress:spec_scale=1.5 + spec:allow_log=1.5 ⇒ 5] · D=8` |
| 12 | $\int  -\left(3\left(3x - 6\right)^{2}\right)\,dx$ | $-\left(\frac{1}{3}\left(3x - 6\right)^{3}\right)+C$ | `u_sub` | `spec_pack=integral_invtrig_sub · tricks=[u_sub] · form_id=power_linear_du · dress=[sign] · costs[form:power_linear_du=1 + dress:spec_sign=0.5 ⇒ 1.5] · D=12` |
| 12 | $\int  -\frac{2}{1+(2x - 4)^{2}}\,dx$ | $-\left(\arctan(2x - 4)\right)+C$ | `u_sub` | `spec_pack=integral_invtrig_sub · tricks=[u_sub] · form_id=arctan_of_linear · dress=[sign] · costs[form:arctan_of_linear=2 + dress:spec_sign=0.5 + spec:allow_invtrig=2 ⇒ 4.5] · D=12` |
| 12 | $\int  -3\frac{4}{4x + 4}\,dx$ | $-3\left(\ln\|4x + 4\|\right)+C$ | `u_sub` | `spec_pack=integral_invtrig_sub · tricks=[u_sub] · form_id=du_over_u_linear · dress=[constant_multiple] · costs[form:du_over_u_linear=2 + dress:spec_scale=1.5 + spec:allow_log=1.5 ⇒ 5] · D=12` |
| 16 | $\int  3\frac{3}{1+(3x - 1)^{2}}\,dx$ | $3\left(\arctan(3x - 1)\right)+C$ | `u_sub` | `spec_pack=integral_invtrig_sub · tricks=[u_sub] · form_id=arctan_of_linear · dress=[sign,constant_multiple] · costs[form:arctan_of_linear=2 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:allow_invtrig=2 ⇒ 6] · D=16` |
| 16 | $\int  2\frac{2}{1+(2x)^{2}}\,dx$ | $2\arctan(2x)+C$ | `u_sub` | `spec_pack=integral_invtrig_sub · tricks=[u_sub] · form_id=arctan_of_linear · dress=[constant_multiple] · costs[form:arctan_of_linear=2 + dress:spec_scale=1.5 + spec:allow_invtrig=2 ⇒ 5.5] · D=16` |
| 16 | $\int  2\left(4\left(4x + 6\right)^{5}\right)\,dx$ | $2\left(\frac{1}{6}\left(4x + 6\right)^{6}\right)+C$ | `u_sub` | `spec_pack=integral_invtrig_sub · tricks=[u_sub] · form_id=power_linear_du · dress=[sign,constant_multiple] · costs[form:power_linear_du=1 + dress:spec_sign=0.5 + dress:spec_scale=1.5 ⇒ 3] · D=16` |
| 20 | $\int  3\left(4\left(4x + 2\right)^{2}\right)\,dx$ | $3\left(\frac{1}{3}\left(4x + 2\right)^{3}\right)+C$ | `u_sub` | `spec_pack=integral_invtrig_sub · tricks=[u_sub] · form_id=power_linear_du · dress=[sign,constant_multiple] · costs[form:power_linear_du=1 + dress:spec_sign=0.5 + dress:spec_scale=1.5 ⇒ 3] · D=20` |
| 20 | $\int  -3\left(4\left(4x + 7\right)^{2}\right)\,dx$ | $-3\left(\frac{1}{3}\left(4x + 7\right)^{3}\right)+C$ | `u_sub` | `spec_pack=integral_invtrig_sub · tricks=[u_sub] · form_id=power_linear_du · dress=[constant_multiple,sign] · costs[form:power_linear_du=1 + dress:spec_scale=1.5 + dress:spec_sign=0.5 ⇒ 3] · D=20` |
| 20 | $\int  -4\frac{4}{1+(4x - 1)^{2}}\,dx$ | $-4\left(\arctan(4x - 1)\right)+C$ | `u_sub` | `spec_pack=integral_invtrig_sub · tricks=[u_sub] · form_id=arctan_of_linear · dress=[constant_multiple] · costs[form:arctan_of_linear=2 + dress:spec_scale=1.5 + spec:allow_invtrig=2 ⇒ 5.5] · D=20` |
| 25 | $\int  2\frac{3}{3x}\,dx$ | $2\ln\|3x\|+C$ | `u_sub` | `spec_pack=integral_invtrig_sub · tricks=[u_sub] · form_id=du_over_u_linear · dress=[constant_multiple,sign] · costs[form:du_over_u_linear=2 + dress:spec_scale=1.5 + dress:spec_sign=0.5 + spec:allow_log=1.5 ⇒ 5.5] · D=25` |
| 25 | $\int  2\frac{3}{1+(3x + 8)^{2}}\,dx$ | $2\left(\arctan(3x + 8)\right)+C$ | `u_sub` | `spec_pack=integral_invtrig_sub · tricks=[u_sub] · form_id=arctan_of_linear · dress=[sign,constant_multiple] · costs[form:arctan_of_linear=2 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:allow_invtrig=2 ⇒ 6] · D=25` |
| 25 | $\int  -\frac{3}{1+(3x)^{2}}\,dx$ | $-\arctan(3x)+C$ | `u_sub` | `spec_pack=integral_invtrig_sub · tricks=[u_sub] · form_id=arctan_of_linear · dress=[sign] · costs[form:arctan_of_linear=2 + dress:spec_sign=0.5 + spec:allow_invtrig=2 ⇒ 4.5] · D=25` |

## Integrals — integration by parts

<a id="int_parts"></a>

`calc_indef_int_integration_by_parts` · pack `int_parts` · topic label: c1: Integration by parts · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **9** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `ln_alone` | 8 |
| `poly1_sin` | 4 |
| `poly2_exp` | 3 |
| `arctan_alone` | 2 |
| `cyclic_exp_sin` | 2 |
| `poly1_cos` | 2 |
| `poly1_exp` | 1 |
| `poly1_ln` | 1 |
| `poly2_sin` | 1 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\int \ln(x)\,dx$ | $x\ln(x)-x+C$ | `parts` | `spec_pack=integral_parts · tricks=[parts] · form_id=ln_alone · costs[form:ln_alone=2 + spec:allow_log=1.5 ⇒ 3.5] · D=0` |
| 0 | $\int \ln(x)\,dx$ | $x\ln(x)-x+C$ | `parts` | `spec_pack=integral_parts · tricks=[parts] · form_id=ln_alone · costs[form:ln_alone=2 + spec:allow_log=1.5 ⇒ 3.5] · D=0` |
| 0 | $\int \ln(x)\,dx$ | $x\ln(x)-x+C$ | `parts` | `spec_pack=integral_parts · tricks=[parts] · form_id=ln_alone · costs[form:ln_alone=2 + spec:allow_log=1.5 ⇒ 3.5] · D=0` |
| 3 | $\int \ln(x)\,dx$ | $x\ln(x)-x+C$ | `parts` | `spec_pack=integral_parts · tricks=[parts] · form_id=ln_alone · costs[form:ln_alone=2 + spec:allow_log=1.5 ⇒ 3.5] · D=3` |
| 3 | $\int x\cos(x)\,dx$ | $x\sin(x)+\cos(x)+C$ | `parts` | `spec_pack=integral_parts · tricks=[parts] · form_id=poly1_cos · costs[form:poly1_cos=4 + spec:allow_trig=1.5 ⇒ 5.5] · D=3` |
| 3 | $\int x\sin(x)\,dx$ | $-x\cos(x)+\sin(x)+C$ | `parts` | `spec_pack=integral_parts · tricks=[parts] · form_id=poly1_sin · costs[form:poly1_sin=4 + spec:allow_trig=1.5 ⇒ 5.5] · D=3` |
| 6 | $\int  2x\sin(x)\,dx$ | $-2\left(x\cos(x)+\sin(x)\right)+C$ | `parts` | `spec_pack=integral_parts · tricks=[parts] · form_id=poly1_sin · dress=[constant_multiple] · costs[form:poly1_sin=4 + dress:spec_scale=1.5 + spec:allow_trig=1.5 ⇒ 7] · D=6` |
| 6 | $\int  4x\sin(x)\,dx$ | $-4\left(x\cos(x)+\sin(x)\right)+C$ | `parts` | `spec_pack=integral_parts · tricks=[parts] · form_id=poly1_sin · dress=[constant_multiple] · costs[form:poly1_sin=4 + dress:spec_scale=1.5 + spec:allow_trig=1.5 ⇒ 7] · D=6` |
| 6 | $\int xe^{x}\,dx$ | $e^{x}(x-1)+C$ | `parts` | `spec_pack=integral_parts · tricks=[parts] · form_id=poly1_exp · costs[form:poly1_exp=4 + spec:allow_exp=1.5 ⇒ 5.5] · D=6` |
| 8 | $\int x\ln(x)\,dx$ | $\frac{1}{2}x^{2}\ln(x)-\frac{1}{4}x^{2}+C$ | `parts` | `spec_pack=integral_parts · tricks=[parts] · form_id=poly1_ln · costs[form:poly1_ln=4 + spec:allow_log=1.5 ⇒ 5.5] · D=8` |
| 8 | $\int \ln(x)\,dx$ | $x\ln(x)-x+C$ | `parts` | `spec_pack=integral_parts · tricks=[parts] · form_id=ln_alone · costs[form:ln_alone=2 + spec:allow_log=1.5 ⇒ 3.5] · D=8` |
| 8 | $\int  -x\cos(x)\,dx$ | $-\left(x\sin(x)+\cos(x)\right)+C$ | `parts` | `spec_pack=integral_parts · tricks=[parts] · form_id=poly1_cos · dress=[sign] · costs[form:poly1_cos=4 + dress:spec_sign=0.5 + spec:allow_trig=1.5 ⇒ 6] · D=8` |
| 12 | $\int  -x^{2}e^{x}\,dx$ | $-\left(e^{x}(x^{2}-2x+2)\right)+C$ | `parts` | `spec_pack=integral_parts · tricks=[parts] · form_id=poly2_exp · dress=[sign] · costs[form:poly2_exp=6 + dress:spec_sign=0.5 + spec:allow_exp=1.5 ⇒ 8] · D=12` |
| 12 | $\int  -\ln(x)\,dx$ | $-\left(x\ln(x)-x\right)+C$ | `parts` | `spec_pack=integral_parts · tricks=[parts] · form_id=ln_alone · dress=[sign] · costs[form:ln_alone=2 + dress:spec_sign=0.5 + spec:allow_log=1.5 ⇒ 4] · D=12` |
| 12 | $\int  -4x^{2}e^{x}\,dx$ | $-4\left(e^{x}(x^{2}-2x+2)\right)+C$ | `parts` | `spec_pack=integral_parts · tricks=[parts] · form_id=poly2_exp · dress=[constant_multiple] · costs[form:poly2_exp=6 + dress:spec_scale=1.5 + spec:allow_exp=1.5 ⇒ 9] · D=12` |
| 16 | $\int  -e^{x}\sin(x)\,dx$ | $-\left(\frac{1}{2}e^{x}(\sin(x)-\cos(x))\right)+C$ | `parts` | `spec_pack=integral_parts · tricks=[parts] · form_id=cyclic_exp_sin · dress=[sign] · costs[form:cyclic_exp_sin=8 + dress:spec_sign=0.5 + spec:allow_exp=1.5 + spec:allow_trig=1.5 ⇒ 11.5] · D=16` |
| 16 | $\int  2x\sin(x)\,dx$ | $-2\left(x\cos(x)+\sin(x)\right)+C$ | `parts` | `spec_pack=integral_parts · tricks=[parts] · form_id=poly1_sin · dress=[sign,constant_multiple] · costs[form:poly1_sin=4 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:allow_trig=1.5 ⇒ 7.5] · D=16` |
| 16 | $\int  -4x^{2}\sin(x)\,dx$ | $4\left(x^{2}\cos(x)+2x\sin(x)+2\cos(x)\right)+C$ | `parts` | `spec_pack=integral_parts · tricks=[parts] · form_id=poly2_sin · dress=[sign,constant_multiple] · costs[form:poly2_sin=6 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:allow_trig=1.5 ⇒ 9.5] · D=16` |
| 20 | $\int  -\ln(x)\,dx$ | $-\left(x\ln(x)-x\right)+C$ | `parts` | `spec_pack=integral_parts · tricks=[parts] · form_id=ln_alone · dress=[sign] · costs[form:ln_alone=2 + dress:spec_sign=0.5 + spec:allow_log=1.5 + spec:nest_depth=2 ⇒ 6] · D=20` |
| 20 | $\int  -2x^{2}e^{x}\,dx$ | $-2\left(e^{x}(x^{2}-2x+2)\right)+C$ | `parts` | `spec_pack=integral_parts · tricks=[parts] · form_id=poly2_exp · dress=[sign,constant_multiple] · costs[form:poly2_exp=6 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:allow_exp=1.5 + spec:nest_depth=2 ⇒ 11.5] · D=20` |
| 20 | $\int  4\arctan(x)\,dx$ | $4\left(x\arctan(x)-\frac{1}{2}\ln(1+x^{2})\right)+C$ | `parts` | `spec_pack=integral_parts · tricks=[parts] · form_id=arctan_alone · dress=[sign,constant_multiple] · costs[form:arctan_alone=3 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:allow_invtrig=2 + spec:nest_depth=2 ⇒ 9] · D=20` |
| 25 | $\int  3\ln(x)\,dx$ | $3\left(x\ln(x)-x\right)+C$ | `parts` | `spec_pack=integral_parts · tricks=[parts] · form_id=ln_alone · dress=[constant_multiple,sign] · costs[form:ln_alone=2 + dress:spec_scale=1.5 + dress:spec_sign=0.5 + spec:allow_log=1.5 + spec:nest_depth=2 ⇒ 7.5] · D=25` |
| 25 | $\int  4\arctan(x)\,dx$ | $4\left(x\arctan(x)-\frac{1}{2}\ln(1+x^{2})\right)+C$ | `parts` | `spec_pack=integral_parts · tricks=[parts] · form_id=arctan_alone · dress=[sign,constant_multiple] · costs[form:arctan_alone=3 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:allow_invtrig=2 + spec:nest_depth=2 ⇒ 9] · D=25` |
| 25 | $\int  2e^{x}\sin(x)\,dx$ | $2\left(\frac{1}{2}e^{x}(\sin(x)-\cos(x))\right)+C$ | `parts` | `spec_pack=integral_parts · tricks=[parts] · form_id=cyclic_exp_sin · dress=[constant_multiple] · costs[form:cyclic_exp_sin=8 + dress:spec_scale=1.5 + spec:allow_exp=1.5 + spec:allow_trig=1.5 + spec:nest_depth=2 ⇒ 14.5] · D=25` |

## Integrals — partial fractions

<a id="int_pfd"></a>

`calc_indef_int_partial_fractions` · pack `int_pfd` · topic label: c1: Partial fractions · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **6** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `distinct_linear_2` | 10 |
| `distinct_linear_3` | 4 |
| `irreducible_quad_ln` | 3 |
| `mixed_linear_quad` | 3 |
| `repeated_linear_square` | 3 |
| `irreducible_quad_arctan` | 1 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\int \frac{3x - 1}{x^{2} + x - 6}\,dx$ | $2\ln\|x + 3\|+\ln\|x - 2\|+C$ | `pfd` | `spec_pack=integral_pfd · tricks=[pfd] · form_id=distinct_linear_2 · costs[form:distinct_linear_2=2 + spec:allow_log=1.5 ⇒ 3.5] · D=0` |
| 0 | $\int \frac{6}{x^{2} - 4x + 3}\,dx$ | $-3\ln\|x - 1\|+3\ln\|x - 3\|+C$ | `pfd` | `spec_pack=integral_pfd · tricks=[pfd] · form_id=distinct_linear_2 · costs[form:distinct_linear_2=2 + spec:allow_log=1.5 ⇒ 3.5] · D=0` |
| 0 | $\int \frac{2x - 3}{x^{2} - 3x + 2}\,dx$ | $\ln\|x - 2\|+\ln\|x - 1\|+C$ | `pfd` | `spec_pack=integral_pfd · tricks=[pfd] · form_id=distinct_linear_2 · costs[form:distinct_linear_2=2 + spec:allow_log=1.5 ⇒ 3.5] · D=0` |
| 3 | $\int \frac{5x - 15}{x^{2} - 5x}\,dx$ | $2\ln\|x - 5\|+3\ln\|x\|+C$ | `pfd` | `spec_pack=integral_pfd · tricks=[pfd] · form_id=distinct_linear_2 · costs[form:distinct_linear_2=2 + spec:allow_log=1.5 ⇒ 3.5] · D=3` |
| 3 | $\int \frac{5x - 8}{x^{2} - 3x + 2}\,dx$ | $3\ln\|x - 1\|+2\ln\|x - 2\|+C$ | `pfd` | `spec_pack=integral_pfd · tricks=[pfd] · form_id=distinct_linear_2 · costs[form:distinct_linear_2=2 + spec:allow_log=1.5 ⇒ 3.5] · D=3` |
| 3 | $\int \frac{-x + 7}{x^{2} - 4x + 3}\,dx$ | $2\ln\|x - 3\|-3\ln\|x - 1\|+C$ | `pfd` | `spec_pack=integral_pfd · tricks=[pfd] · form_id=distinct_linear_2 · costs[form:distinct_linear_2=2 + spec:allow_log=1.5 ⇒ 3.5] · D=3` |
| 6 | $\int \frac{9x + 3}{3x^{2} + 3x}\,dx$ | $\ln\|x\|+2\ln\|x + 1\|+C$ | `pfd` | `spec_pack=integral_pfd · tricks=[pfd] · form_id=distinct_linear_2 · costs[form:distinct_linear_2=2 + spec:allow_log=1.5 ⇒ 3.5] · D=6` |
| 6 | $\int \frac{6x - 14}{x^{2} - x - 30}\,dx$ | $4\ln\|x + 5\|+2\ln\|x - 6\|+C$ | `pfd` | `spec_pack=integral_pfd · tricks=[pfd] · form_id=distinct_linear_2 · costs[form:distinct_linear_2=2 + spec:allow_log=1.5 ⇒ 3.5] · D=6` |
| 6 | $\int \frac{-5x + 2}{x^{2} - x}\,dx$ | $-2\ln\|x\|-3\ln\|x - 1\|+C$ | `pfd` | `spec_pack=integral_pfd · tricks=[pfd] · form_id=distinct_linear_2 · costs[form:distinct_linear_2=2 + spec:allow_log=1.5 ⇒ 3.5] · D=6` |
| 8 | $\int  2\frac{2x^{2} - 3x - 3}{\left(x - 3\right)\left(x\right)\left(x - 1\right)}\,dx$ | $2\left(\ln\|x - 3\|-\ln\|x\|+2\ln\|x - 1\|\right)+C$ | `pfd` | `spec_pack=integral_pfd · tricks=[pfd] · form_id=distinct_linear_3 · dress=[constant_multiple] · costs[form:distinct_linear_3=2 + dress:spec_scale=1.5 + spec:allow_log=1.5 ⇒ 5] · D=8` |
| 8 | $\int  -\frac{3x - 18}{3x^{2} - 9x}\,dx$ | $-\left(2\ln\|x\|-\ln\|x - 3\|\right)+C$ | `pfd` | `spec_pack=integral_pfd · tricks=[pfd] · form_id=distinct_linear_2 · dress=[sign] · costs[form:distinct_linear_2=2 + dress:spec_sign=0.5 + spec:allow_log=1.5 ⇒ 4] · D=8` |
| 8 | $\int  2\frac{-2x}{x^{2} + 1}\,dx$ | $-2\left(\ln\|x^{2}+1\|\right)+C$ | `pfd` | `spec_pack=integral_pfd · tricks=[pfd] · form_id=irreducible_quad_ln · dress=[constant_multiple] · costs[form:irreducible_quad_ln=2 + dress:spec_scale=1.5 + spec:allow_log=1.5 + spec:allow_invtrig=2 ⇒ 7] · D=8` |
| 12 | $\int  -3\frac{7x^{2} + 3x - 14}{\left(x - 2\right)\left(x + 3\right)\left(x - 1\right)}\,dx$ | $-3\left(4\ln\|x - 2\|+2\ln\|x + 3\|+\ln\|x - 1\|\right)+C$ | `pfd` | `spec_pack=integral_pfd · tricks=[pfd] · form_id=distinct_linear_3 · dress=[constant_multiple] · costs[form:distinct_linear_3=2 + dress:spec_scale=1.5 + spec:allow_log=1.5 ⇒ 5] · D=12` |
| 12 | $\int  -\frac{6x}{2x^{2} + 8}\,dx$ | $-\left(\frac{3}{2}\ln\|x^{2}+4\|\right)+C$ | `pfd` | `spec_pack=integral_pfd · tricks=[pfd] · form_id=irreducible_quad_ln · dress=[sign] · costs[form:irreducible_quad_ln=2 + dress:spec_sign=0.5 + spec:allow_log=1.5 + spec:allow_invtrig=2 ⇒ 6] · D=12` |
| 12 | $\int  -4\frac{-9x}{3x^{2} + 3}\,dx$ | $4\left(\frac{3}{2}\ln\|x^{2}+1\|\right)+C$ | `pfd` | `spec_pack=integral_pfd · tricks=[pfd] · form_id=irreducible_quad_ln · dress=[constant_multiple] · costs[form:irreducible_quad_ln=2 + dress:spec_scale=1.5 + spec:allow_log=1.5 + spec:allow_invtrig=2 ⇒ 7] · D=12` |
| 16 | $\int  -\frac{\left(((-\frac{1}{3})3 + 4)\right)\left(-3x^{2} - 9\right)}{\left(((-\frac{1}{3})3 + 4)\right)\left(3x^{3} + 3x\right)}\,dx$ | $3\ln\|x\|+\ln\|x^{2}+1\|+C$ | `pfd` | `spec_pack=integral_pfd · tricks=[pfd] · form_id=mixed_linear_quad · dress=[sign] · costs[form:mixed_linear_quad=2 + dress:spec_sign=0.5 + spec:allow_log=1.5 + spec:allow_invtrig=2 ⇒ 6] · D=16` |
| 16 | $\int  2\frac{-12}{3x^{2} + 12}\,dx$ | $-4\arctan(\frac{x}{2})+C$ | `pfd` | `spec_pack=integral_pfd · tricks=[pfd] · form_id=irreducible_quad_arctan · dress=[sign,constant_multiple] · costs[form:irreducible_quad_arctan=2 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:allow_log=1.5 + spec:allow_invtrig=2 ⇒ 7.5] · D=16` |
| 16 | $\int  -4\frac{3x + 7}{\left(x + 1\right)^{2}}\,dx$ | $-4\left(3\ln\|x + 1\|-4\frac{1}{x + 1}\right)+C$ | `pfd` | `spec_pack=integral_pfd · tricks=[pfd] · form_id=repeated_linear_square · dress=[sign,constant_multiple] · costs[form:repeated_linear_square=2 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:allow_log=1.5 ⇒ 5.5] · D=16` |
| 20 | $\int  2\frac{3x + 2}{\left(x + 2\right)^{2}}\,dx$ | $2\left(3\ln\|x + 2\|+4\frac{1}{x + 2}\right)+C$ | `pfd` | `spec_pack=integral_pfd · tricks=[pfd] · form_id=repeated_linear_square · dress=[constant_multiple] · costs[form:repeated_linear_square=2 + dress:spec_scale=1.5 + spec:allow_log=1.5 ⇒ 5] · D=20` |
| 20 | $\int  -\frac{4x - 11}{\left(x - 3\right)^{2}}\,dx$ | $-\left(4\ln\|x - 3\|-\frac{1}{x - 3}\right)+C$ | `pfd` | `spec_pack=integral_pfd · tricks=[pfd] · form_id=repeated_linear_square · dress=[sign] · costs[form:repeated_linear_square=2 + dress:spec_sign=0.5 + spec:allow_log=1.5 ⇒ 4] · D=20` |
| 20 | $\int  -2\frac{-x^{2} + 16x - 12}{\left(x + 2\right)\left(x\right)\left(x - 2\right)}\,dx$ | $2\left(6\ln\|x + 2\|+3\ln\|x\|+2\ln\|x - 2\|\right)+C$ | `pfd` | `spec_pack=integral_pfd · tricks=[pfd] · form_id=distinct_linear_3 · dress=[sign,constant_multiple] · costs[form:distinct_linear_3=2 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:allow_log=1.5 ⇒ 5.5] · D=20` |
| 25 | $\int  -\frac{6x^{2} + 6x - 12}{x^{3} - 3x^{2} + x - 3}\,dx$ | $-\left(6\ln\|x - 3\|+6\arctan(x)\right)+C$ | `pfd` | `spec_pack=integral_pfd · tricks=[pfd] · form_id=mixed_linear_quad · dress=[sign] · costs[form:mixed_linear_quad=2 + dress:spec_sign=0.5 + spec:allow_log=1.5 + spec:allow_invtrig=2 ⇒ 6] · D=25` |
| 25 | $\int  -\frac{-5x + 2}{\left(x - 1\right)\left(x - 2\right)\left(x + 2\right)}\,dx$ | $-\left(\ln\|x - 1\|-2\ln\|x - 2\|+\ln\|x + 2\|\right)+C$ | `pfd` | `spec_pack=integral_pfd · tricks=[pfd] · form_id=distinct_linear_3 · dress=[sign] · costs[form:distinct_linear_3=2 + dress:spec_sign=0.5 + spec:allow_log=1.5 ⇒ 4] · D=25` |
| 25 | $\int  -\frac{-9x^{2} - 6}{3x^{3} + 3x^{2} + 12x + 12}\,dx$ | $\ln\|x + 1\|-\ln\|x^{2}+4\|+\arctan(\frac{x}{2})+C$ | `pfd` | `spec_pack=integral_pfd · tricks=[pfd] · form_id=mixed_linear_quad · dress=[sign] · costs[form:mixed_linear_quad=2 + dress:spec_sign=0.5 + spec:allow_log=1.5 + spec:allow_invtrig=2 ⇒ 6] · D=25` |

## Integrals — multi-trick

<a id="int_multi"></a>

`calc_indef_int_multi_trick` · pack `int_multi` · topic label: c1: Multi-technique (u-sub then PFD) · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **3** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `u_sub_then_pfd_trig` | 14 |
| `u_sub_then_pfd_exp` | 5 |
| `u_sub_then_pfd_log` | 5 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\int \frac{3\left(e^{4x}\right)+7}{\left(e^{4x}+1\right)\left(e^{4x}+3\right)}\cdot 4e^{4x}\,dx$ | $2\ln\|\left(e^{4x}+1\right)\|+\ln\|\left(e^{4x}+3\right)\|+C$ | `u_sub,pfd` | `spec_pack=integral_multi_trick · tricks=[u_sub,pfd] · form_id=u_sub_then_pfd_exp · costs[form:u_sub_then_pfd_exp=5 + spec:allow_exp=1.5 + spec:allow_log=1.5 + spec:nest_depth=2 ⇒ 10] · D=0` |
| 0 | $\int \frac{4\left(\cos(3x)\right)-2}{\left(\cos(3x)-2\right)\left(\cos(3x)\right)}\left(-3\sin(3x)\right)\,dx$ | $3\ln\|\left(\cos(3x)-2\right)\|+\ln\|\left(\cos(3x)\right)\|+C$ | `u_sub,pfd` | `spec_pack=integral_multi_trick · tricks=[u_sub,pfd] · form_id=u_sub_then_pfd_trig · costs[form:u_sub_then_pfd_trig=5 + spec:allow_log=1.5 + spec:allow_trig=1.5 + spec:nest_depth=2 ⇒ 10] · D=0` |
| 0 | $\int \frac{0\left(\cos(3x)\right)+2}{\left(\cos(3x)-2\right)\left(\cos(3x)-3\right)}\left(-3\sin(3x)\right)\,dx$ | $-2\ln\|\left(\cos(3x)-2\right)\|+2\ln\|\left(\cos(3x)-3\right)\|+C$ | `u_sub,pfd` | `spec_pack=integral_multi_trick · tricks=[u_sub,pfd] · form_id=u_sub_then_pfd_trig · costs[form:u_sub_then_pfd_trig=5 + spec:allow_log=1.5 + spec:allow_trig=1.5 + spec:nest_depth=2 ⇒ 10] · D=0` |
| 3 | $\int \frac{5\left(\cos(x)\right)+5}{\left(\cos(x)-3\right)\left(\cos(x)+2\right)}\left(-\sin(x)\right)\,dx$ | $4\ln\|\left(\cos(x)-3\right)\|+\ln\|\left(\cos(x)+2\right)\|+C$ | `u_sub,pfd` | `spec_pack=integral_multi_trick · tricks=[u_sub,pfd] · form_id=u_sub_then_pfd_trig · costs[form:u_sub_then_pfd_trig=5 + spec:allow_log=1.5 + spec:allow_trig=1.5 + spec:nest_depth=2 ⇒ 10] · D=3` |
| 3 | $\int \frac{-\sin(4x)-9}{\left(\sin(4x)\right)\left(\sin(4x)+3\right)}\cdot 4\cos(4x)\,dx$ | $-3\ln\|\left(\sin(4x)\right)\|+2\ln\|\left(\sin(4x)+3\right)\|+C$ | `u_sub,pfd` | `spec_pack=integral_multi_trick · tricks=[u_sub,pfd] · form_id=u_sub_then_pfd_trig · costs[form:u_sub_then_pfd_trig=5 + spec:allow_log=1.5 + spec:allow_trig=1.5 + spec:nest_depth=2 ⇒ 10] · D=3` |
| 3 | $\int \frac{5\left(\sin(4x)\right)-7}{\left(\sin(4x)-1\right)\left(\sin(4x)-2\right)}\cdot 4\cos(4x)\,dx$ | $2\ln\|\left(\sin(4x)-1\right)\|+3\ln\|\left(\sin(4x)-2\right)\|+C$ | `u_sub,pfd` | `spec_pack=integral_multi_trick · tricks=[u_sub,pfd] · form_id=u_sub_then_pfd_trig · costs[form:u_sub_then_pfd_trig=5 + spec:allow_log=1.5 + spec:allow_trig=1.5 + spec:nest_depth=2 ⇒ 10] · D=3` |
| 6 | $\int \frac{2\left(\cos(3x)\right)+16}{\left(\cos(3x)+4\right)\left(\cos(3x)-4\right)}\left(-3\sin(3x)\right)\,dx$ | $-\ln\|\left(\cos(3x)+4\right)\|+3\ln\|\left(\cos(3x)-4\right)\|+C$ | `u_sub,pfd` | `spec_pack=integral_multi_trick · tricks=[u_sub,pfd] · form_id=u_sub_then_pfd_trig · costs[form:u_sub_then_pfd_trig=5 + spec:allow_log=1.5 + spec:allow_trig=1.5 + spec:nest_depth=2 ⇒ 10] · D=6` |
| 6 | $\int  -\frac{4\left(e^{x}\right)-7}{\left(e^{x}-3\right)\left(e^{x}+2\right)}e^{x}\,dx$ | $-\left(\ln\|\left(e^{x}-3\right)\|+3\ln\|\left(e^{x}+2\right)\|\right)+C$ | `u_sub,pfd` | `spec_pack=integral_multi_trick · tricks=[u_sub,pfd] · form_id=u_sub_then_pfd_exp · dress=[sign] · costs[form:u_sub_then_pfd_exp=5 + dress:spec_sign=0.5 + spec:allow_exp=1.5 + spec:allow_log=1.5 + spec:nest_depth=2 ⇒ 10.5] · D=6` |
| 6 | $\int \frac{2\left(\ln\|x - 3\|\right)-4}{\left(\ln\|x - 3\|-3\right)\left(\ln\|x - 3\|-1\right)}\frac{1}{x - 3}\,dx$ | $\ln\|\left(\ln\|x - 3\|-3\right)\|+\ln\|\left(\ln\|x - 3\|-1\right)\|+C$ | `u_sub,pfd` | `spec_pack=integral_multi_trick · tricks=[u_sub,pfd] · form_id=u_sub_then_pfd_log · costs[form:u_sub_then_pfd_log=5 + spec:allow_log=1.5 + spec:nest_depth=2 ⇒ 8.5] · D=6` |
| 8 | $\int  -\left(\frac{2}{\left(\cos(3x)\right)^{2}+9}\left(-3\sin(3x)\right)\right)\,dx$ | $-\left(2\ln\|\cos(3x) - 3\|+\frac{2}{3}\arctan(\frac{\cos(3x)}{3})\right)+C$ | `u_sub,pfd` | `spec_pack=integral_multi_trick · tricks=[u_sub,pfd] · form_id=u_sub_then_pfd_trig · dress=[sign] · costs[form:u_sub_then_pfd_trig=5 + dress:spec_sign=0.5 + spec:allow_invtrig=2 + spec:allow_log=1.5 + spec:allow_trig=1.5 + spec:nest_depth=2 ⇒ 12.5] · D=8` |
| 8 | $\int \frac{4}{\left(\sin(2x)\right)^{2}+9}\cdot 2\cos(2x)\,dx$ | $-\ln\|\sin(2x) - 6\|+\frac{4}{3}\arctan(\frac{\sin(2x)}{3})+C$ | `u_sub,pfd` | `spec_pack=integral_multi_trick · tricks=[u_sub,pfd] · form_id=u_sub_then_pfd_trig · costs[form:u_sub_then_pfd_trig=5 + spec:allow_invtrig=2 + spec:allow_log=1.5 + spec:allow_trig=1.5 + spec:nest_depth=2 ⇒ 12] · D=8` |
| 8 | $\int \frac{3}{\left(\ln\|2x - 5\|\right)^{2}+1}\frac{2}{2x - 5}\,dx$ | $\ln\|\ln\|2x - 5\| + 3\|+3\arctan(\ln\|2x - 5\|)+C$ | `u_sub,pfd` | `spec_pack=integral_multi_trick · tricks=[u_sub,pfd] · form_id=u_sub_then_pfd_log · costs[form:u_sub_then_pfd_log=5 + spec:allow_invtrig=2 + spec:allow_log=1.5 + spec:nest_depth=2 ⇒ 10.5] · D=8` |
| 12 | $\int  -2\frac{3}{\left(\sin(4x)\right)^{2}+9}\cdot 4\cos(4x)\,dx$ | $2\left(5\ln\|\sin(4x) + 6\|+\arctan(\frac{\sin(4x)}{3})\right)+C$ | `u_sub,pfd` | `spec_pack=integral_multi_trick · tricks=[u_sub,pfd] · form_id=u_sub_then_pfd_trig · dress=[constant_multiple] · costs[form:u_sub_then_pfd_trig=5 + dress:spec_scale=1.5 + spec:allow_invtrig=2 + spec:allow_log=1.5 + spec:allow_trig=1.5 + spec:nest_depth=2 ⇒ 13.5] · D=12` |
| 12 | $\int  -3\frac{3}{\left(e^{2x}\right)^{2}+4}\cdot 2e^{2x}\,dx$ | $3\left(5\ln\|e^{2x} + 1\|+\frac{3}{2}\arctan(\frac{e^{2x}}{2})\right)+C$ | `u_sub,pfd` | `spec_pack=integral_multi_trick · tricks=[u_sub,pfd] · form_id=u_sub_then_pfd_exp · dress=[constant_multiple] · costs[form:u_sub_then_pfd_exp=5 + dress:spec_scale=1.5 + spec:allow_exp=1.5 + spec:allow_invtrig=2 + spec:allow_log=1.5 + spec:nest_depth=2 ⇒ 13.5] · D=12` |
| 12 | $\int  -\frac{1}{\left(\sin(3x)\right)^{2}+1}\cdot 3\cos(3x)\,dx$ | $-\left(2\ln\|\sin(3x) - 1\|+\arctan(\sin(3x))\right)+C$ | `u_sub,pfd` | `spec_pack=integral_multi_trick · tricks=[u_sub,pfd] · form_id=u_sub_then_pfd_trig · dress=[sign] · costs[form:u_sub_then_pfd_trig=5 + dress:spec_sign=0.5 + spec:allow_invtrig=2 + spec:allow_log=1.5 + spec:allow_trig=1.5 + spec:nest_depth=2 ⇒ 12.5] · D=12` |
| 16 | $\int  -3\frac{-1\left(\tan(3x)\right)}{\left(\tan(3x)\right)^{2}+1}\cdot 3\sec^{2}(3x)\,dx$ | $-3\left(4\ln\|\tan(3x)\|-\frac{1}{2}\ln\|\tan(3x)^{2}+1\|\right)+C$ | `u_sub,pfd` | `spec_pack=integral_multi_trick · tricks=[u_sub,pfd] · form_id=u_sub_then_pfd_trig · dress=[sign,constant_multiple] · costs[form:u_sub_then_pfd_trig=5 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:allow_invtrig=2 + spec:allow_log=1.5 + spec:allow_trig=1.5 + spec:nest_depth=2 ⇒ 14] · D=16` |
| 16 | $\int  2\frac{3}{\left(\sin(x)\right)^{2}+16}\cdot \cos(x)\,dx$ | $2\left(\ln\|\sin(x)\|+\frac{3}{4}\arctan(\frac{\sin(x)}{4})\right)+C$ | `u_sub,pfd` | `spec_pack=integral_multi_trick · tricks=[u_sub,pfd] · form_id=u_sub_then_pfd_trig · dress=[sign,constant_multiple] · costs[form:u_sub_then_pfd_trig=5 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:allow_invtrig=2 + spec:allow_log=1.5 + spec:allow_trig=1.5 + spec:nest_depth=2 ⇒ 14] · D=16` |
| 16 | $\int  -3\left(\frac{-2\left(\cos(2x)\right)+5}{\left(\cos(2x)\right)^{2}+9}\left(-2\sin(2x)\right)\right)\,dx$ | $-3\left(16\ln\|\cos(2x) - 1\|-\ln\|\cos(2x)^{2}+9\|+\frac{5}{3}\arctan(\frac{\cos(2x)}{3})\right)+C$ | `u_sub,pfd` | `spec_pack=integral_multi_trick · tricks=[u_sub,pfd] · form_id=u_sub_then_pfd_trig · dress=[constant_multiple] · costs[form:u_sub_then_pfd_trig=5 + dress:spec_scale=1.5 + spec:allow_invtrig=2 + spec:allow_log=1.5 + spec:allow_trig=1.5 + spec:nest_depth=2 ⇒ 13.5] · D=16` |
| 20 | $\int  -3\left(\frac{3}{\left(\cos(2x)\right)^{2}+1}\left(-2\sin(2x)\right)\right)\,dx$ | $-3\left(2\ln\|\cos(2x) - 6\|+3\arctan(\cos(2x))\right)+C$ | `u_sub,pfd` | `spec_pack=integral_multi_trick · tricks=[u_sub,pfd] · form_id=u_sub_then_pfd_trig · dress=[constant_multiple] · costs[form:u_sub_then_pfd_trig=5 + dress:spec_scale=1.5 + spec:allow_invtrig=2 + spec:allow_log=1.5 + spec:allow_trig=1.5 + spec:nest_depth=2 ⇒ 13.5] · D=20` |
| 20 | $\int  -2\frac{-2}{\left(\ln\|2x + 4\|\right)^{2}+9}\frac{2}{2x + 4}\,dx$ | $2\left(\ln\|\ln\|2x + 4\| - 7\|-\frac{2}{3}\arctan(\frac{\ln\|2x + 4\|}{3})\right)+C$ | `u_sub,pfd` | `spec_pack=integral_multi_trick · tricks=[u_sub,pfd] · form_id=u_sub_then_pfd_log · dress=[sign,constant_multiple] · costs[form:u_sub_then_pfd_log=5 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:allow_invtrig=2 + spec:allow_log=1.5 + spec:nest_depth=2 ⇒ 12.5] · D=20` |
| 20 | $\int  -2\frac{-10\left(e^{3x}\right)}{\left(e^{3x}\right)^{2}+1}\cdot 3e^{3x}\,dx$ | $2\left(8\ln\|e^{3x} + 6\|-5\ln\|e^{3x}^{2}+1\|\right)+C$ | `u_sub,pfd` | `spec_pack=integral_multi_trick · tricks=[u_sub,pfd] · form_id=u_sub_then_pfd_exp · dress=[constant_multiple] · costs[form:u_sub_then_pfd_exp=5 + dress:spec_scale=1.5 + spec:allow_exp=1.5 + spec:allow_invtrig=2 + spec:allow_log=1.5 + spec:nest_depth=2 ⇒ 13.5] · D=20` |
| 25 | $\int  -3\frac{1\left(\ln\|x + 3\|\right)+2}{\left(\ln\|x + 3\|\right)^{2}+1}\frac{1}{x + 3}\,dx$ | $-3\left(\ln\|\ln\|x + 3\| - 2\|+\frac{1}{2}\ln\|\ln\|x + 3\|^{2}+1\|+2\arctan(\ln\|x + 3\|)\right)+C$ | `u_sub,pfd` | `spec_pack=integral_multi_trick · tricks=[u_sub,pfd] · form_id=u_sub_then_pfd_log · dress=[sign,constant_multiple] · costs[form:u_sub_then_pfd_log=5 + dress:spec_sign=0.5 + dress:spec_scale=1.5 + spec:allow_invtrig=2 + spec:allow_log=1.5 + spec:nest_depth=2 ⇒ 12.5] · D=25` |
| 25 | $\int  -\frac{-4}{\left(e^{2x}\right)^{2}+9}\cdot 2e^{2x}\,dx$ | $2\ln\|e^{2x} - 2\|-\frac{4}{3}\arctan(\frac{e^{2x}}{3})+C$ | `u_sub,pfd` | `spec_pack=integral_multi_trick · tricks=[u_sub,pfd] · form_id=u_sub_then_pfd_exp · dress=[sign] · costs[form:u_sub_then_pfd_exp=5 + dress:spec_sign=0.5 + spec:allow_exp=1.5 + spec:allow_invtrig=2 + spec:allow_log=1.5 + spec:nest_depth=2 ⇒ 12.5] · D=25` |
| 25 | $\int  -4\frac{3\left(\ln\|x + 9\|\right)}{\left(\ln\|x + 9\|\right)^{2}+1}\frac{1}{x + 9}\,dx$ | $-4\left(4\ln\|\ln\|x + 9\| - 1\|+\frac{3}{2}\ln\|\ln\|x + 9\|^{2}+1\|\right)+C$ | `u_sub,pfd` | `spec_pack=integral_multi_trick · tricks=[u_sub,pfd] · form_id=u_sub_then_pfd_log · dress=[constant_multiple] · costs[form:u_sub_then_pfd_log=5 + dress:spec_scale=1.5 + spec:allow_invtrig=2 + spec:allow_log=1.5 + spec:nest_depth=2 ⇒ 12] · D=25` |

## FTC — first

<a id="ftc1"></a>

`calc_def_int_first_fundamental_theorem_of_calculus` · pack `ftc1` · topic label: c1: First Fundamental Theorem of Calculus · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **4** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `linear` | 9 |
| `sin` | 7 |
| `quad` | 5 |
| `sqrt` | 3 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\int_{0}^{2} x\,dx$ | $2$ | `ftc` | `spec_pack=integral_ftc1 · tricks=[ftc] · form_id=linear · costs[form:linear=2 ⇒ 2] · D=0` |
| 0 | $\int_{0}^{3} x\,dx$ | $\frac{9}{2}$ | `ftc` | `spec_pack=integral_ftc1 · tricks=[ftc] · form_id=linear · costs[form:linear=2 ⇒ 2] · D=0` |
| 0 | $\int_{0}^{\pi/2} \sin(x)\,dx$ | $1$ | `ftc` | `spec_pack=integral_ftc1 · tricks=[ftc] · form_id=sin · costs[form:sin=2 + spec:allow_trig=1.5 ⇒ 3.5] · D=0` |
| 3 | $\int_{0}^{4} x^{2}\,dx$ | $\frac{64}{3}$ | `ftc` | `spec_pack=integral_ftc1 · tricks=[ftc] · form_id=quad · costs[form:quad=2 ⇒ 2] · D=3` |
| 3 | $\int_{0}^{\pi/2} \sin(x)\,dx$ | $1$ | `ftc` | `spec_pack=integral_ftc1 · tricks=[ftc] · form_id=sin · costs[form:sin=2 + spec:allow_trig=1.5 ⇒ 3.5] · D=3` |
| 3 | $\int_{0}^{5} x\,dx$ | $\frac{25}{2}$ | `ftc` | `spec_pack=integral_ftc1 · tricks=[ftc] · form_id=linear · costs[form:linear=2 ⇒ 2] · D=3` |
| 6 | $\int_{0}^{2} x\,dx$ | $2$ | `ftc` | `spec_pack=integral_ftc1 · tricks=[ftc] · form_id=linear · costs[form:linear=2 ⇒ 2] · D=6` |
| 6 | $\int_{0}^{2} 4x^{2}\,dx$ | $\frac{32}{3}$ | `ftc` | `spec_pack=integral_ftc1 · tricks=[ftc] · form_id=quad · costs[form:quad=2 ⇒ 2] · D=6` |
| 6 | $\int_{0}^{5} 2x^{2}\,dx$ | $\frac{250}{3}$ | `ftc` | `spec_pack=integral_ftc1 · tricks=[ftc] · form_id=quad · costs[form:quad=2 ⇒ 2] · D=6` |
| 8 | $\int_{0}^{\pi/2} \sin(x)\,dx$ | $1$ | `ftc` | `spec_pack=integral_ftc1 · tricks=[ftc] · form_id=sin · costs[form:sin=2 + spec:allow_trig=1.5 ⇒ 3.5] · D=8` |
| 8 | $\int_{0}^{5} x^{2}\,dx$ | $\frac{125}{3}$ | `ftc` | `spec_pack=integral_ftc1 · tricks=[ftc] · form_id=quad · costs[form:quad=2 ⇒ 2] · D=8` |
| 8 | $\int_{0}^{3} x\,dx$ | $\frac{9}{2}$ | `ftc` | `spec_pack=integral_ftc1 · tricks=[ftc] · form_id=linear · costs[form:linear=2 ⇒ 2] · D=8` |
| 12 | $\int_{0}^{3} x\,dx$ | $\frac{9}{2}$ | `ftc` | `spec_pack=integral_ftc1 · tricks=[ftc] · form_id=linear · costs[form:linear=2 ⇒ 2] · D=12` |
| 12 | $\int_{0}^{4} x\,dx$ | $8$ | `ftc` | `spec_pack=integral_ftc1 · tricks=[ftc] · form_id=linear · costs[form:linear=2 ⇒ 2] · D=12` |
| 12 | $\int_{0}^{\pi/2} \sin(x)\,dx$ | $1$ | `ftc` | `spec_pack=integral_ftc1 · tricks=[ftc] · form_id=sin · costs[form:sin=2 + spec:allow_trig=1.5 ⇒ 3.5] · D=12` |
| 16 | $\int_{0}^{9} \sqrt{x}\,dx$ | $18$ | `ftc` | `spec_pack=integral_ftc1 · tricks=[ftc] · form_id=sqrt · costs[form:sqrt=2 ⇒ 2] · D=16` |
| 16 | $\int_{0}^{\pi/2} \sin(x)\,dx$ | $1$ | `ftc` | `spec_pack=integral_ftc1 · tricks=[ftc] · form_id=sin · costs[form:sin=2 + spec:allow_trig=1.5 ⇒ 3.5] · D=16` |
| 16 | $\int_{0}^{2} x\,dx$ | $2$ | `ftc` | `spec_pack=integral_ftc1 · tricks=[ftc] · form_id=linear · costs[form:linear=2 ⇒ 2] · D=16` |
| 20 | $\int_{0}^{5} 3x^{2}\,dx$ | $125$ | `ftc` | `spec_pack=integral_ftc1 · tricks=[ftc] · form_id=quad · costs[form:quad=2 ⇒ 2] · D=20` |
| 20 | $\int_{0}^{1} \sqrt{x}\,dx$ | $\frac{2}{3}$ | `ftc` | `spec_pack=integral_ftc1 · tricks=[ftc] · form_id=sqrt · costs[form:sqrt=2 ⇒ 2] · D=20` |
| 20 | $\int_{0}^{9} \sqrt{x}\,dx$ | $18$ | `ftc` | `spec_pack=integral_ftc1 · tricks=[ftc] · form_id=sqrt · costs[form:sqrt=2 ⇒ 2] · D=20` |
| 25 | $\int_{0}^{\pi/2} \sin(x)\,dx$ | $1$ | `ftc` | `spec_pack=integral_ftc1 · tricks=[ftc] · form_id=sin · costs[form:sin=2 + spec:allow_trig=1.5 ⇒ 3.5] · D=25` |
| 25 | $\int_{0}^{\pi/2} \sin(x)\,dx$ | $1$ | `ftc` | `spec_pack=integral_ftc1 · tricks=[ftc] · form_id=sin · costs[form:sin=2 + spec:allow_trig=1.5 ⇒ 3.5] · D=25` |
| 25 | $\int_{0}^{3} x\,dx$ | $\frac{9}{2}$ | `ftc` | `spec_pack=integral_ftc1 · tricks=[ftc] · form_id=linear · costs[form:linear=2 ⇒ 2] · D=25` |

## FTC — second

<a id="ftc2"></a>

`calc_def_int_second_fundamental_theorem_of_calculus` · pack `ftc2` · topic label: c1: Second Fundamental Theorem of Calculus · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **4** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `sin` | 8 |
| `linear` | 7 |
| `sqrt` | 6 |
| `quad` | 3 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\int_{0}^{4} \sqrt{x}\,dx$ | $\frac{16}{3}$ | `ftc` | `spec_pack=integral_ftc2 · tricks=[ftc] · form_id=sqrt · costs[form:sqrt=2 ⇒ 2] · D=0` |
| 0 | $\int_{0}^{\pi/2} \sin(x)\,dx$ | $1$ | `ftc` | `spec_pack=integral_ftc2 · tricks=[ftc] · form_id=sin · costs[form:sin=2 + spec:allow_trig=1.5 ⇒ 3.5] · D=0` |
| 0 | $\int_{0}^{2} x\,dx$ | $2$ | `ftc` | `spec_pack=integral_ftc2 · tricks=[ftc] · form_id=linear · costs[form:linear=2 ⇒ 2] · D=0` |
| 3 | $\int_{0}^{\pi/2} \sin(x)\,dx$ | $1$ | `ftc` | `spec_pack=integral_ftc2 · tricks=[ftc] · form_id=sin · costs[form:sin=2 + spec:allow_trig=1.5 ⇒ 3.5] · D=3` |
| 3 | $\int_{0}^{2} 4x^{2}\,dx$ | $\frac{32}{3}$ | `ftc` | `spec_pack=integral_ftc2 · tricks=[ftc] · form_id=quad · costs[form:quad=2 ⇒ 2] · D=3` |
| 3 | $\int_{0}^{\pi/2} \sin(x)\,dx$ | $1$ | `ftc` | `spec_pack=integral_ftc2 · tricks=[ftc] · form_id=sin · costs[form:sin=2 + spec:allow_trig=1.5 ⇒ 3.5] · D=3` |
| 6 | $\int_{0}^{5} x\,dx$ | $\frac{25}{2}$ | `ftc` | `spec_pack=integral_ftc2 · tricks=[ftc] · form_id=linear · costs[form:linear=2 ⇒ 2] · D=6` |
| 6 | $\int_{0}^{5} x\,dx$ | $\frac{25}{2}$ | `ftc` | `spec_pack=integral_ftc2 · tricks=[ftc] · form_id=linear · costs[form:linear=2 ⇒ 2] · D=6` |
| 6 | $\int_{0}^{4} \sqrt{x}\,dx$ | $\frac{16}{3}$ | `ftc` | `spec_pack=integral_ftc2 · tricks=[ftc] · form_id=sqrt · costs[form:sqrt=2 ⇒ 2] · D=6` |
| 8 | $\int_{0}^{\pi/2} \sin(x)\,dx$ | $1$ | `ftc` | `spec_pack=integral_ftc2 · tricks=[ftc] · form_id=sin · costs[form:sin=2 + spec:allow_trig=1.5 ⇒ 3.5] · D=8` |
| 8 | $\int_{0}^{2} 3x^{2}\,dx$ | $8$ | `ftc` | `spec_pack=integral_ftc2 · tricks=[ftc] · form_id=quad · costs[form:quad=2 ⇒ 2] · D=8` |
| 8 | $\int_{0}^{5} x\,dx$ | $\frac{25}{2}$ | `ftc` | `spec_pack=integral_ftc2 · tricks=[ftc] · form_id=linear · costs[form:linear=2 ⇒ 2] · D=8` |
| 12 | $\int_{0}^{3} x\,dx$ | $\frac{9}{2}$ | `ftc` | `spec_pack=integral_ftc2 · tricks=[ftc] · form_id=linear · costs[form:linear=2 ⇒ 2] · D=12` |
| 12 | $\int_{0}^{9} \sqrt{x}\,dx$ | $18$ | `ftc` | `spec_pack=integral_ftc2 · tricks=[ftc] · form_id=sqrt · costs[form:sqrt=2 ⇒ 2] · D=12` |
| 12 | $\int_{0}^{5} x\,dx$ | $\frac{25}{2}$ | `ftc` | `spec_pack=integral_ftc2 · tricks=[ftc] · form_id=linear · costs[form:linear=2 ⇒ 2] · D=12` |
| 16 | $\int_{0}^{\pi/2} \sin(x)\,dx$ | $1$ | `ftc` | `spec_pack=integral_ftc2 · tricks=[ftc] · form_id=sin · costs[form:sin=2 + spec:allow_trig=1.5 ⇒ 3.5] · D=16` |
| 16 | $\int_{0}^{\pi/2} \sin(x)\,dx$ | $1$ | `ftc` | `spec_pack=integral_ftc2 · tricks=[ftc] · form_id=sin · costs[form:sin=2 + spec:allow_trig=1.5 ⇒ 3.5] · D=16` |
| 16 | $\int_{0}^{\pi/2} \sin(x)\,dx$ | $1$ | `ftc` | `spec_pack=integral_ftc2 · tricks=[ftc] · form_id=sin · costs[form:sin=2 + spec:allow_trig=1.5 ⇒ 3.5] · D=16` |
| 20 | $\int_{0}^{4} \sqrt{x}\,dx$ | $\frac{16}{3}$ | `ftc` | `spec_pack=integral_ftc2 · tricks=[ftc] · form_id=sqrt · costs[form:sqrt=2 ⇒ 2] · D=20` |
| 20 | $\int_{0}^{\pi/2} \sin(x)\,dx$ | $1$ | `ftc` | `spec_pack=integral_ftc2 · tricks=[ftc] · form_id=sin · costs[form:sin=2 + spec:allow_trig=1.5 ⇒ 3.5] · D=20` |
| 20 | $\int_{0}^{5} 4x^{2}\,dx$ | $\frac{500}{3}$ | `ftc` | `spec_pack=integral_ftc2 · tricks=[ftc] · form_id=quad · costs[form:quad=2 ⇒ 2] · D=20` |
| 25 | $\int_{0}^{4} x\,dx$ | $8$ | `ftc` | `spec_pack=integral_ftc2 · tricks=[ftc] · form_id=linear · costs[form:linear=2 ⇒ 2] · D=25` |
| 25 | $\int_{0}^{1} \sqrt{x}\,dx$ | $\frac{2}{3}$ | `ftc` | `spec_pack=integral_ftc2 · tricks=[ftc] · form_id=sqrt · costs[form:sqrt=2 ⇒ 2] · D=25` |
| 25 | $\int_{0}^{4} \sqrt{x}\,dx$ | $\frac{16}{3}$ | `ftc` | `spec_pack=integral_ftc2 · tricks=[ftc] · form_id=sqrt · costs[form:sqrt=2 ⇒ 2] · D=25` |

## Definite — substitution / change of variables

<a id="def_sub"></a>

`calc_def_int_substitution_with_change_of_variables` · pack `def_sub` · topic label: c1: Substitution with change of variables · ok 24/24

### Structures in this topic

Structures / families / templates actually used in this sample set (from live question metadata — not a static template list).

- distinct structures: **5** · samples: **24**

| Structure / family | Count |
|--------|------:|
| `power_linear_du` | 8 |
| `du_over_u_linear` | 6 |
| `root_quad_x_du` | 5 |
| `power_quad_x_du` | 3 |
| `alteration_linear_over_root` | 2 |

| D | Prompt | Answer | tricks | Metadata |
|--:|--------|--------|--------|----------|
| 0 | $\int 3\left(3x\right)^{2}\,dx$ | $\frac{1}{3}\left(3x\right)^{3}+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=power_linear_du · costs[form:power_linear_du=1 ⇒ 1] · D=0` |
| 0 | $\int 3\left(3x + 6\right)^{2}\,dx$ | $\frac{1}{3}\left(3x + 6\right)^{3}+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=power_linear_du · costs[form:power_linear_du=1 ⇒ 1] · D=0` |
| 0 | $\int 4\left(4x + 2\right)^{3}\,dx$ | $\frac{1}{4}\left(4x + 2\right)^{4}+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=power_linear_du · costs[form:power_linear_du=1 ⇒ 1] · D=0` |
| 3 | $\int 3\left(3x - 5\right)^{3}\,dx$ | $\frac{1}{4}\left(3x - 5\right)^{4}+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=power_linear_du · costs[form:power_linear_du=1 ⇒ 1] · D=3` |
| 3 | $\int \frac{4}{4x + 3}\,dx$ | $\ln\|4x + 3\|+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=du_over_u_linear · costs[form:du_over_u_linear=2 + spec:allow_log=1.5 ⇒ 3.5] · D=3` |
| 3 | $\int \frac{3}{3x + 6}\,dx$ | $\ln\|3x + 6\|+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=du_over_u_linear · costs[form:du_over_u_linear=2 + spec:allow_log=1.5 ⇒ 3.5] · D=3` |
| 6 | $\int  -\left(2\left(2x - 5\right)^{5}\right)\,dx$ | $-\left(\frac{1}{6}\left(2x - 5\right)^{6}\right)+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=power_linear_du · dress=[sign] · costs[form:power_linear_du=1 + dress:spec_sign=0.5 ⇒ 1.5] · D=6` |
| 6 | $\int x\sqrt{x^{2}+1}\,dx$ | $\frac{1}{3}\left(x^{2}+1\right)^{\frac{3}{2}}+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=root_quad_x_du · costs[form:root_quad_x_du=2 ⇒ 2] · D=6` |
| 6 | $\int 4\left(4x + 6\right)^{5}\,dx$ | $\frac{1}{6}\left(4x + 6\right)^{6}+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=power_linear_du · costs[form:power_linear_du=1 ⇒ 1] · D=6` |
| 8 | $\int \frac{2}{2x + 6}\,dx$ | $\ln\|2x + 6\|+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=du_over_u_linear · costs[form:du_over_u_linear=2 + spec:allow_log=1.5 ⇒ 3.5] · D=8` |
| 8 | $\int \frac{4}{4x + 5}\,dx$ | $\ln\|4x + 5\|+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=du_over_u_linear · costs[form:du_over_u_linear=2 + spec:allow_log=1.5 ⇒ 3.5] · D=8` |
| 8 | $\int \frac{2}{2x + 1}\,dx$ | $\ln\|2x + 1\|+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=du_over_u_linear · costs[form:du_over_u_linear=2 + spec:allow_log=1.5 ⇒ 3.5] · D=8` |
| 12 | $\int 2x\left(x^{2}+5\right)^{3}\,dx$ | $\frac{1}{4}\left(x^{2}+5\right)^{4}+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=power_quad_x_du · costs[form:power_quad_x_du=1 ⇒ 1] · D=12` |
| 12 | $\int  -\frac{x}{\sqrt{x-1}}\,dx$ | $-\left(\frac{2}{3}\left(x-1\right)^{\frac{3}{2}}+2\sqrt{x-1}\right)+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=alteration_linear_over_root · dress=[sign] · costs[form:alteration_linear_over_root=2 + dress:spec_sign=0.5 ⇒ 2.5] · D=12` |
| 12 | $\int  3\left(4\left(4x + 1\right)^{2}\right)\,dx$ | $3\left(\frac{1}{3}\left(4x + 1\right)^{3}\right)+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=power_linear_du · dress=[constant_multiple] · costs[form:power_linear_du=1 + dress:spec_scale=1.5 ⇒ 2.5] · D=12` |
| 16 | $\int  -\left(2x\left(x^{2}+2\right)^{4}\right)\,dx$ | $-\left(\frac{1}{5}\left(x^{2}+2\right)^{5}\right)+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=power_quad_x_du · dress=[sign] · costs[form:power_quad_x_du=1 + dress:spec_sign=0.5 ⇒ 1.5] · D=16` |
| 16 | $\int  -4x\sqrt{x^{2}+7}\,dx$ | $-4\left(\frac{1}{3}\left(x^{2}+7\right)^{\frac{3}{2}}\right)+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=root_quad_x_du · dress=[constant_multiple] · costs[form:root_quad_x_du=2 + dress:spec_scale=1.5 ⇒ 3.5] · D=16` |
| 16 | $\int  -3\frac{x}{\sqrt{x-1}}\,dx$ | $-3\left(\frac{2}{3}\left(x-1\right)^{\frac{3}{2}}+2\sqrt{x-1}\right)+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=alteration_linear_over_root · dress=[constant_multiple] · costs[form:alteration_linear_over_root=2 + dress:spec_scale=1.5 ⇒ 3.5] · D=16` |
| 20 | $\int  -2\left(3\left(3x + 7\right)^{4}\right)\,dx$ | $-2\left(\frac{1}{5}\left(3x + 7\right)^{5}\right)+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=power_linear_du · dress=[constant_multiple,sign] · costs[form:power_linear_du=1 + dress:spec_scale=1.5 + dress:spec_sign=0.5 ⇒ 3] · D=20` |
| 20 | $\int  -x\sqrt{x^{2}+2}\,dx$ | $-\left(\frac{1}{3}\left(x^{2}+2\right)^{\frac{3}{2}}\right)+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=root_quad_x_du · dress=[sign] · costs[form:root_quad_x_du=2 + dress:spec_sign=0.5 ⇒ 2.5] · D=20` |
| 20 | $\int  -3\frac{2}{2x - 1}\,dx$ | $-3\left(\ln\|2x - 1\|\right)+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=du_over_u_linear · dress=[constant_multiple,sign] · costs[form:du_over_u_linear=2 + dress:spec_scale=1.5 + dress:spec_sign=0.5 + spec:allow_log=1.5 ⇒ 5.5] · D=20` |
| 25 | $\int  -x\sqrt{x^{2}+7}\,dx$ | $-\left(\frac{1}{3}\left(x^{2}+7\right)^{\frac{3}{2}}\right)+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=root_quad_x_du · dress=[sign] · costs[form:root_quad_x_du=2 + dress:spec_sign=0.5 ⇒ 2.5] · D=25` |
| 25 | $\int  -4\left(2x\left(x^{2}+2\right)^{3}\right)\,dx$ | $-4\left(\frac{1}{4}\left(x^{2}+2\right)^{4}\right)+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=power_quad_x_du · dress=[constant_multiple,sign] · costs[form:power_quad_x_du=1 + dress:spec_scale=1.5 + dress:spec_sign=0.5 ⇒ 3] · D=25` |
| 25 | $\int  -x\sqrt{x^{2}+8}\,dx$ | $-\left(\frac{1}{3}\left(x^{2}+8\right)^{\frac{3}{2}}\right)+C$ | `u_sub` | `spec_pack=integral_u_sub · tricks=[u_sub] · form_id=root_quad_x_du · dress=[sign] · costs[form:root_quad_x_du=2 + dress:spec_sign=0.5 ⇒ 2.5] · D=25` |
