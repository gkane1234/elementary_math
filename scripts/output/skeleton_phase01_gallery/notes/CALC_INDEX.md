# Calculus type index

Inventory of question **type_ids** for Calculus.
Setup-only: suggested engine family is a proposal, not a wiring change.
Notes pass is **steps 1–3 only** (old path, `notes/<slug>.md`, OpenStax).
Do **not** implement Calculus generators in this wave unless the leaf is
already on Diff / `expr_skeleton` (then notes/gallery only).

## Course layout

- **Single catalog:** `question_engine/catalogs/calculus.py`
  (`COURSE_ID = "calculus"`). No `calculus_1` / `calculus_2` catalog modules.
- **`lib/curriculum.ts`:** one `calculus` level (Limits → DE).
- **Settings:** many calc leaves use `setting_profile="derivatives"` in
  `question_engine/settings/generator_profiles.py`; presets under
  `"derivatives"` in `presets.py` / `domains/calculus.py`.
- **Diff live path:** `generators/calculus_derivative_rules.py` →
  `frameworks/primitives/derivatives.py` → `expr_skeleton` when the
  OpenStax form_id is in `FORM_PATTERNS`. Gallery:
  `scripts/output/diff_skeleton_gallery/`.

## Counts

| Source | Count |
|---|---:|
| Catalog (`question_engine/catalogs/calculus.py`) = Calculus `QUESTION_TYPES` leaves | 68 |
| Heuristic **Calc1** band (Vol 1 / AB spine) | 64 |
| Heuristic **Calc2** band (technique-heavy integration) | 4 |
| Already on **Diff** `expr_skeleton` (live + `diff_skeleton_gallery`) | 9 |
| Already on phase-01 gallery (`skeleton_phase01_gallery` SECTIONS) | 10 Diff (+implicit Mad-Lib) |

**Already-on-Diff-skeleton** = catalog leaf whose generator is one of the
nine Diff gallery topics **and** has implemented `derivatives.json` forms
mapped in `expr_skeleton.FORM_PATTERNS` (power / product / quotient / chain /
trig / ln·exp / invtrig / higher_order / general).

**Calc2 heuristic** (inside the unified catalog) =
`calc_indef_int_trigonometric_with_substitution`,
`calc_indef_int_integration_by_parts`,
`calc_indef_int_partial_fractions`,
`calc_indef_int_multi_trick`. All other leaves are tagged Calc1-band.

Engine family is one of: `diff` / `limit` / `integral` / `de` / `other`
(proposal only; differs from G6–PA’s number/affine/solve set).

Also checked: `lib/curriculum.ts`, `question_engine/core/registry.py`,
`QUESTION_TYPES`, `question_engine/settings/`, Diff gallery,
`derivatives.py` `_TYPE_ID_TO_GENERATOR`, Precalc intro-to-calc aliases.

## `QUESTION_TYPES` vs catalog

Every Calculus catalog `id` is registered in `QUESTION_TYPES`.

## `lib/curriculum.ts` vs catalog

Curriculum lists **64** `calc_*` type_ids; catalog has **68**. Catalog-only
(not yet in `lib/curriculum.ts`):

| type_id | notes |
|---|---|
| `calc_diff_general` | on Diff skeleton |
| `calc_app_diff_linear_approximations` | apps of differentiation |
| `calc_indef_int_partial_fractions` | Calc2-band |
| `calc_indef_int_multi_trick` | Calc2-band |

No curriculum-only calc ids (curriculum ⊆ catalog).

## Already on Diff `expr_skeleton`

These Differentiation leaves are live on Diff / `expr_skeleton` (9 / 68).
Per-leaf notes already exist for all nine (see backfill below).

| type_id | display name | generator | diff gallery slug | Precalc alias |
|---|---|---|---|---|
| `calc_diff_power_rule` | Power Rule | `derivative_power_rule` | `power_rule` | `pc_power_rule_for_differentiation` |
| `calc_diff_higher_order_derivatives` | Higher order derivatives | `derivative_higher_order` | `higher_order` | — |
| `calc_diff_product_rule` | Product Rule | `derivative_product_rule` | `product_rule` | — |
| `calc_diff_quotient_rule` | Quotient Rule | `derivative_quotient_rule` | `quotient_rule` | — |
| `calc_diff_chain_rule` | Chain Rule | `derivative_chain_rule` | `chain_rule` | — |
| `calc_diff_general` | General derivatives | `derivative_general` | `general` | — |
| `calc_diff_trigonometric` | Trigonometric | `derivative_trigonometric` | `trigonometric` | — |
| `calc_diff_inverse_trigonometric` | Inverse trigonometric | `derivative_inverse_trig` | `inverse_trig` | — |
| `calc_diff_natural_logarithms_and_exponentials` | Natural logarithms and exponentials | `derivative_ln_exp` | `ln_exp` | — |

### Notes backfill (already-on-Diff)

Filled if notes have an `openstax.org` cite **and** a live old-path section
(`What old / live path actually produced` or `Live `_generate_for_type``).

Filled: **9** / 9. Still need backfill: **0**.

## Differentiation leaves **not** on Diff skeleton yet

Still Differentiation `calc_diff_*` (excludes `calc_diff_eq_*` DE leaves),
but not in the nine expr_skeleton gallery topics (or forms are stub-only).

| type_id | display name | generator | suggested family | notes |
|---|---|---|---|---|
| `calc_diff_average_rates_of_change` | Average rates of change | `average_rate_of_change` | diff | other path |
| `calc_diff_definition_of_the_derivative` | Definition of the derivative | `definition_of_derivative` | diff | other path |
| `calc_diff_instantaneous_rates_of_change` | Instantaneous rates of change | `instantaneous_rate_of_change` | diff | other path |
| `calc_diff_rules_using_tables` | Rules, using tables | `derivative_from_tables` | diff | other path |
| `calc_diff_other_base_logarithms_and_exponentials` | Other base logarithms and exponentials | `derivative_other_base` | diff | catalog-routed other_base_* |
| `calc_diff_logarithmic` | Logarithmic | `derivative_logarithmic` | diff | catalog-routed logdiff_* |
| `calc_diff_implicit` | Implicit | `derivative_implicit` | diff | catalog-routed implicit_* |
| `calc_diff_inverse_functions` | Inverse functions | `derivative_inverse_functions` | diff | catalog-routed invfn_* |

## Precalc intro-to-calc aliases

Precalculus Introduction-to-Calculus leaves sharing a generator or explicit
skill pair with a Calculus leaf. See `PRECALC_INDEX.md`.

| calc type_id | Precalc alias | shared generator | on Diff? |
|---|---|---|---|
| `calc_limits_by_direct_evaluation` | `pc_limits_by_direct_evaluation` | `limit_direct_evaluation` | no |
| `calc_limits_at_jump_discontinuities_and_kinks` | `pc_limits_at_kinks_and_jumps` | `limit_jump` | no |
| `calc_limits_at_removable_discontinuities` | `pc_limits_at_removable_discontinuities` | `limit_removable` | no |
| `calc_limits_at_essential_discontinuities` | `pc_limits_at_essential_discontinuities` | `limit_essential` | no |
| `calc_limits_at_infinity` | `pc_limits_at_infinity` | `limit_at_infinity` | no |
| `calc_diff_definition_of_the_derivative` | `pc_definition_of_the_derivative` | `definition_of_derivative` | no |
| `calc_diff_instantaneous_rates_of_change` | `pc_instantaneous_rates_of_change` | `instantaneous_rate_of_change` | no |
| `calc_diff_power_rule` | `pc_power_rule_for_differentiation` | `derivative_power_rule` | yes |
| `calc_app_diff_motion_along_a_line` | `pc_motion_along_a_line` | `motion_along_a_line` | no |
| `calc_app_diff_limits_in_form_of_definition_of_derivative` | `pc_definition_of_the_derivative` | `definition_of_derivative` | no |
| `calc_indef_int_power_rule` | `pc_indefinite_integrals` | `integral_power_rule` | no |
| `calc_def_int_approximating_area_under_a_curve` | `pc_approximating_area_under_a_curve` | `riemann_approximate_area` | no |
| `calc_def_int_area_under_a_curve_by_limit_of_sums` | `pc_area_under_a_curve_by_limit_of_sums` | `area_under_curve` | no |
| `calc_app_int_area_under_a_curve` | `pc_area_under_a_curve_by_limit_of_sums` | `area_under_curve` | no |

## Calculus catalog

| type_id | display name | band | already-on-Diff? | suggested engine family | Precalc alias |
|---|---|---|---|---|---|
|  | **Calculus — Limits** |  |  |  |  |
| `calc_limits_by_direct_evaluation` | By direct evaluation | Calc1 | no | limit | `pc_limits_by_direct_evaluation` |
| `calc_limits_at_jump_discontinuities_and_kinks` | At jump discontinuities and kinks | Calc1 | no | limit | `pc_limits_at_kinks_and_jumps` |
| `calc_limits_at_removable_discontinuities` | At removable discontinuities | Calc1 | no | limit | `pc_limits_at_removable_discontinuities` |
| `calc_limits_at_essential_discontinuities` | At essential discontinuities | Calc1 | no | limit | `pc_limits_at_essential_discontinuities` |
| `calc_limits_at_infinity` | At infinity | Calc1 | no | limit | `pc_limits_at_infinity` |
|  | **Calculus — Continuity** |  |  |  |  |
| `calc_continuity_determining_and_classifying` | Determining and classifying | Calc1 | no | limit | — |
|  | **Calculus — Differentiation** |  |  |  |  |
| `calc_diff_average_rates_of_change` | Average rates of change | Calc1 | no | diff | — |
| `calc_diff_definition_of_the_derivative` | Definition of the derivative | Calc1 | no | diff | `pc_definition_of_the_derivative` |
| `calc_diff_instantaneous_rates_of_change` | Instantaneous rates of change | Calc1 | no | diff | `pc_instantaneous_rates_of_change` |
| `calc_diff_power_rule` | Power Rule | Calc1 | yes | diff | `pc_power_rule_for_differentiation` |
| `calc_diff_higher_order_derivatives` | Higher order derivatives | Calc1 | yes | diff | — |
| `calc_diff_product_rule` | Product Rule | Calc1 | yes | diff | — |
| `calc_diff_quotient_rule` | Quotient Rule | Calc1 | yes | diff | — |
| `calc_diff_chain_rule` | Chain Rule | Calc1 | yes | diff | — |
| `calc_diff_general` | General derivatives | Calc1 | yes | diff | — |
| `calc_diff_rules_using_tables` | Rules, using tables | Calc1 | no | diff | — |
| `calc_diff_trigonometric` | Trigonometric | Calc1 | yes | diff | — |
| `calc_diff_inverse_trigonometric` | Inverse trigonometric | Calc1 | yes | diff | — |
| `calc_diff_natural_logarithms_and_exponentials` | Natural logarithms and exponentials | Calc1 | yes | diff | — |
| `calc_diff_other_base_logarithms_and_exponentials` | Other base logarithms and exponentials | Calc1 | no | diff | — |
| `calc_diff_logarithmic` | Logarithmic | Calc1 | no | diff | — |
| `calc_diff_implicit` | Implicit | Calc1 | no | diff | — |
| `calc_diff_inverse_functions` | Inverse functions | Calc1 | no | diff | — |
|  | **Calculus — Applications of Differentiation** |  |  |  |  |
| `calc_app_diff_slope_tangent_and_normal_lines` | Slope, tangent, and normal lines | Calc1 | no | other | — |
| `calc_app_diff_rolles_theorem` | Rolle's Theorem | Calc1 | no | other | — |
| `calc_app_diff_mean_value_theorem` | Mean Value Theorem | Calc1 | no | other | — |
| `calc_app_diff_intervals_of_increase_and_decrease` | Intervals of increase and decrease | Calc1 | no | other | — |
| `calc_app_diff_intervals_of_concavity` | Intervals of concavity | Calc1 | no | other | — |
| `calc_app_diff_relative_extrema` | Relative extrema | Calc1 | no | other | — |
| `calc_app_diff_absolute_extrema` | Absolute extrema | Calc1 | no | other | — |
| `calc_app_diff_optimization` | Optimization | Calc1 | no | other | — |
| `calc_app_diff_curve_sketching` | Curve sketching | Calc1 | no | other | — |
| `calc_app_diff_graphical_comparison_of_f_f_prime_and_f_double_prime` | Graphical comparison of f, f', and f'' | Calc1 | no | other | — |
| `calc_app_diff_motion_along_a_line` | Motion along a line | Calc1 | no | other | `pc_motion_along_a_line` |
| `calc_app_diff_related_rates` | Related rates | Calc1 | no | other | — |
| `calc_app_diff_differentials` | Differentials | Calc1 | no | other | — |
| `calc_app_diff_linear_approximations` | Linear approximations | Calc1 | no | other | — |
| `calc_app_diff_newtons_method` | Newton's Method | Calc1 | no | other | — |
| `calc_app_diff_limits_in_form_of_definition_of_derivative` | Limits in form of definition of derivative | Calc1 | no | other | `pc_definition_of_the_derivative` |
| `calc_app_diff_lhopitals_rule` | L'Hôpital's Rule | Calc1 | no | other | — |
|  | **Calculus — Indefinite Integration** |  |  |  |  |
| `calc_indef_int_power_rule` | Power Rule | Calc1 | no | integral | `pc_indefinite_integrals` |
| `calc_indef_int_logarithmic_rule_and_exponentials` | Logarithmic Rule and Exponentials | Calc1 | no | integral | — |
| `calc_indef_int_trigonometric` | Trigonometric | Calc1 | no | integral | — |
| `calc_indef_int_inverse_trigonometric` | Inverse trigonometric | Calc1 | no | integral | — |
| `calc_indef_int_power_rule_with_substitution` | Power rule with substitution | Calc1 | no | integral | — |
| `calc_indef_int_logarithmic_rule_and_exponentials_with_substitution` | Logarithmic rule and exponentials with subs. | Calc1 | no | integral | — |
| `calc_indef_int_trigonometric_with_substitution` | Trigonometric substitution | Calc2 | no | integral | — |
| `calc_indef_int_inverse_trigonometric_with_substitution` | Inverse trigonometric with substitution | Calc1 | no | integral | — |
| `calc_indef_int_integration_by_parts` | Integration by parts | Calc2 | no | integral | — |
| `calc_indef_int_partial_fractions` | Partial fractions | Calc2 | no | integral | — |
| `calc_indef_int_multi_trick` | Multi-technique (u-sub then PFD) | Calc2 | no | integral | — |
|  | **Calculus — Definite Integration** |  |  |  |  |
| `calc_def_int_approximating_area_under_a_curve` | Approximating area under a curve | Calc1 | no | integral | `pc_approximating_area_under_a_curve` |
| `calc_def_int_area_under_a_curve_by_limit_of_sums` | Area under a curve by limit of sums | Calc1 | no | integral | `pc_area_under_a_curve_by_limit_of_sums` |
| `calc_def_int_riemann_sum_tables` | Riemann sum tables | Calc1 | no | integral | — |
| `calc_def_int_first_fundamental_theorem_of_calculus` | First Fundamental Theorem of Calculus | Calc1 | no | integral | — |
| `calc_def_int_substitution_with_change_of_variables` | Substitution with change of variables | Calc1 | no | integral | — |
| `calc_def_int_mean_value_theorem` | Mean Value Theorem | Calc1 | no | integral | — |
| `calc_def_int_second_fundamental_theorem_of_calculus` | Second Fundamental Theorem of Calculus | Calc1 | no | integral | — |
|  | **Calculus — Applications of Integration** |  |  |  |  |
| `calc_app_int_area_under_a_curve` | Area under a curve | Calc1 | no | integral | `pc_area_under_a_curve_by_limit_of_sums` |
| `calc_app_int_area_between_curves` | Area between curves | Calc1 | no | integral | — |
| `calc_app_int_volume_by_slicing_disks_and_washers` | Volume by slicing, disks and washers | Calc1 | no | integral | — |
| `calc_app_int_volume_by_cylinders` | Volume by cylinders | Calc1 | no | integral | — |
| `calc_app_int_volume_of_solids_with_known_cross_sections` | Volume of solids with known cross sections | Calc1 | no | integral | — |
| `calc_app_int_motion_along_a_line_revisited` | Motion along a line revisited | Calc1 | no | integral | — |
|  | **Calculus — Differential Equations** |  |  |  |  |
| `calc_diff_eq_slope_fields` | Slope fields | Calc1 | no | de | — |
| `calc_diff_eq_introduction` | Introduction | Calc1 | no | de | — |
| `calc_diff_eq_separable` | Separable | Calc1 | no | de | — |
| `calc_diff_eq_exponential_growth_and_decay` | Exponential growth and decay | Calc1 | no | de | — |

## Appendix — generator keys

| type_id | catalog generator | Diff-mapped generator |
|---|---|---|
| `calc_limits_by_direct_evaluation` | `limit_direct_evaluation` | — |
| `calc_limits_at_jump_discontinuities_and_kinks` | `limit_jump` | — |
| `calc_limits_at_removable_discontinuities` | `limit_removable` | — |
| `calc_limits_at_essential_discontinuities` | `limit_essential` | — |
| `calc_limits_at_infinity` | `limit_at_infinity` | — |
| `calc_continuity_determining_and_classifying` | `limit_continuity` | — |
| `calc_diff_average_rates_of_change` | `average_rate_of_change` | — |
| `calc_diff_definition_of_the_derivative` | `definition_of_derivative` | — |
| `calc_diff_instantaneous_rates_of_change` | `instantaneous_rate_of_change` | — |
| `calc_diff_power_rule` | `derivative_power_rule` | — |
| `calc_diff_higher_order_derivatives` | `derivative_higher_order` | — |
| `calc_diff_product_rule` | `derivative_product_rule` | — |
| `calc_diff_quotient_rule` | `derivative_quotient_rule` | — |
| `calc_diff_chain_rule` | `derivative_chain_rule` | — |
| `calc_diff_general` | `derivative_general` | — |
| `calc_diff_rules_using_tables` | `derivative_from_tables` | — |
| `calc_diff_trigonometric` | `derivative_trigonometric` | — |
| `calc_diff_inverse_trigonometric` | `derivative_inverse_trig` | — |
| `calc_diff_natural_logarithms_and_exponentials` | `derivative_ln_exp` | — |
| `calc_diff_other_base_logarithms_and_exponentials` | `derivative_other_base` | — |
| `calc_diff_logarithmic` | `derivative_logarithmic` | — |
| `calc_diff_implicit` | `derivative_implicit` | — |
| `calc_diff_inverse_functions` | `derivative_inverse_functions` | — |
| `calc_app_diff_slope_tangent_and_normal_lines` | `tangent_normal_line` | — |
| `calc_app_diff_rolles_theorem` | `rolles_theorem` | — |
| `calc_app_diff_mean_value_theorem` | `mean_value_theorem` | — |
| `calc_app_diff_intervals_of_increase_and_decrease` | `intervals_increase_decrease` | — |
| `calc_app_diff_intervals_of_concavity` | `intervals_concavity` | — |
| `calc_app_diff_relative_extrema` | `relative_extrema` | — |
| `calc_app_diff_absolute_extrema` | `absolute_extrema` | — |
| `calc_app_diff_optimization` | `calculus_foundations` | — |
| `calc_app_diff_curve_sketching` | `curve_sketching` | — |
| `calc_app_diff_graphical_comparison_of_f_f_prime_and_f_double_prime` | `calculus_foundations` | — |
| `calc_app_diff_motion_along_a_line` | `motion_along_a_line` | — |
| `calc_app_diff_related_rates` | `related_rates_simple` | — |
| `calc_app_diff_differentials` | `differentials` | — |
| `calc_app_diff_linear_approximations` | `linear_approximation` | — |
| `calc_app_diff_newtons_method` | `newtons_method` | — |
| `calc_app_diff_limits_in_form_of_definition_of_derivative` | `definition_of_derivative` | — |
| `calc_app_diff_lhopitals_rule` | `lhopitals_rule` | — |
| `calc_indef_int_power_rule` | `integral_power_rule` | — |
| `calc_indef_int_logarithmic_rule_and_exponentials` | `integral_log_exp` | — |
| `calc_indef_int_trigonometric` | `integral_trigonometric` | — |
| `calc_indef_int_inverse_trigonometric` | `integral_inverse_trig` | — |
| `calc_indef_int_power_rule_with_substitution` | `integral_substitution` | — |
| `calc_indef_int_logarithmic_rule_and_exponentials_with_substitution` | `integral_log_exp_substitution` | — |
| `calc_indef_int_trigonometric_with_substitution` | `integral_trig_substitution` | — |
| `calc_indef_int_inverse_trigonometric_with_substitution` | `integral_invtrig_substitution` | — |
| `calc_indef_int_integration_by_parts` | `integration_by_parts` | — |
| `calc_indef_int_partial_fractions` | `integral_partial_fractions` | — |
| `calc_indef_int_multi_trick` | `integral_multi_trick` | — |
| `calc_def_int_approximating_area_under_a_curve` | `riemann_approximate_area` | — |
| `calc_def_int_area_under_a_curve_by_limit_of_sums` | `area_under_curve` | — |
| `calc_def_int_riemann_sum_tables` | `riemann_sum_tables` | — |
| `calc_def_int_first_fundamental_theorem_of_calculus` | `first_fundamental_theorem` | — |
| `calc_def_int_substitution_with_change_of_variables` | `integral_substitution` | — |
| `calc_def_int_mean_value_theorem` | `def_int_mean_value` | — |
| `calc_def_int_second_fundamental_theorem_of_calculus` | `second_fundamental_theorem` | — |
| `calc_app_int_area_under_a_curve` | `area_under_curve` | — |
| `calc_app_int_area_between_curves` | `area_between_curves` | — |
| `calc_app_int_volume_by_slicing_disks_and_washers` | `volume_disk_washer` | — |
| `calc_app_int_volume_by_cylinders` | `volume_shell` | — |
| `calc_app_int_volume_of_solids_with_known_cross_sections` | `volume_cross_sections` | — |
| `calc_app_int_motion_along_a_line_revisited` | `motion_along_a_line_integral` | — |
| `calc_diff_eq_slope_fields` | `slope_field_interpret` | — |
| `calc_diff_eq_introduction` | `calculus_foundations` | — |
| `calc_diff_eq_separable` | `separable_diff_eq` | — |
| `calc_diff_eq_exponential_growth_and_decay` | `calc_continuous_growth_decay` | — |

## Appendix — Diff gallery topics

From `scripts/output/diff_skeleton_gallery/gen_examples.py` `TOPICS`:

| slug | display | generator key |
|---|---|---|
| `power_rule` | Power rule | `derivative_power_rule` |
| `product_rule` | Product rule | `derivative_product_rule` |
| `quotient_rule` | Quotient rule | `derivative_quotient_rule` |
| `chain_rule` | Chain rule | `derivative_chain_rule` |
| `trigonometric` | Trigonometric | `derivative_trigonometric` |
| `ln_exp` | Exp / ln | `derivative_ln_exp` |
| `inverse_trig` | Inverse trig | `derivative_inverse_trig` |
| `higher_order` | Higher order | `derivative_higher_order` |
| `general` | General / mixed | `derivative_general` |

Per-type notes: copy `_TEMPLATE.md` → `notes/<gallery-slug>.md` (or
`<type_id>.md`). Process: `.cursor/rules/topic-notes-process.mdc`,
`benchmark-old-path.mdc`, `regenerate-galleries.mdc`,
`gallery-html-katex.mdc`.
