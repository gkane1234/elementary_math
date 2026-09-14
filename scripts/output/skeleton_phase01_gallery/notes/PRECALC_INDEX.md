# Precalculus type index

Inventory of question **type_ids** for Precalculus.
Setup-only: suggested engine family is a proposal, not a wiring change.
Notes pass is **steps 1–3 only** (old path, `notes/<slug>.md`, OpenStax).
Do not implement Precalculus generators in this wave unless the leaf is already on a skeleton.

## Counts

| Source | Precalc |
|---|---:|
| Catalog (`question_engine/catalogs/precalculus.py`) = Precalculus `QUESTION_TYPES` leaves | 94 |
| Already on a phase-01 skeleton (gallery `type_id` / alias, or catalog generator is a gallery type) | 1 |
| Thin A1 aliases (prefixed id on skeleton via shared A1/unprefixed canonical) | 1 |

**Already-on-skeleton** = yes if the leaf is a `SECTIONS` `type_id` or alias in
`scripts/output/skeleton_phase01_gallery/gen_examples.py`, **or** its catalog
`generator` is itself a gallery type (shared family already on that engine).

**A1 alias** = unprefixed (or A1-catalog) `type_id` whose skeleton engine this leaf
reuses — gallery alias, or same `generator=` as an A1 catalog entry already on skeleton.

Engine family is one of: `number` / `affine` / `solve` / `wp` / `proportion` / `geometry` / `other`.

Also checked: `lib/curriculum.ts`, `question_engine/core/registry.py`,
`QUESTION_TYPES`, `question_engine/settings/` (including `domains/`),
`question_engine/generators/`.

## Thin A1 skeleton aliases

These prefixed leaves are already on a phase-01 skeleton by alias or shared
`generator=` with an A1 (or unprefixed shared) canonical. Notes/process follow
the A1 gallery slug unless the A2/PC old path diverges.

| type_id | display name | A1 alias | gallery slug | engine family |
|---|---|---|---|---|
| `pc_dividing_polynomial_functions` | Dividing polynomial functions | `polynomial_long_division` | `polynomial_long_division` | other |

## Notes backfill (already-on-skeleton)

Already-skeletoned leaves still need notes before wiring changes.
A notes file counts as filled if it has an `openstax.org` cite **and** a
`What old path actually produced` section (same skip rule as `_sample_pa.py`).

Filled: **1** / 1. Still need backfill: **0**.

Filled already-on-skeleton notes:

| type_id | gallery slug | notes file |
|---|---|---|
| `pc_dividing_polynomial_functions` | `polynomial_long_division` | `polynomial_long_division.md` |

## Precalculus catalog

| type_id | display name | already-on-skeleton? | suggested engine family | A1 alias |
|---|---|---|---|---|
|  | **Precalculus — Functions** |  |  |  |
| `pc_continuity` | Continuity | no | other | — |
| `pc_extrema_intervals_of_increase_and_decrease` | Extrema, intervals of increase and decrease | no | other | — |
| `pc_power_functions` | Power functions | no | other | — |
| `pc_average_rates_of_change` | Average rates of change | no | other | — |
| `pc_transformations_of_graphs` | Transformations of graphs | no | other | — |
| `pc_piecewise_functions` | Piecewise functions | no | other | — |
| `pc_functions_operations` | Operations | no | other | — |
| `pc_inverses` | Inverses | no | other | — |
|  | **Precalculus — Power, Polynomial, and Rational Functions** |  |  |  |
| `pc_polynomial_graphs_real_zeros_and_end_behavior` | Graphs, real zeros, and end behavior of polynomial functions | no | other | — |
| `pc_dividing_polynomial_functions` | Dividing polynomial functions | yes | other | `polynomial_long_division` |
| `pc_remainder_theorem_and_bounds_of_real_zeros` | The Remainder Theorem and bounds of real zeros | no | other | — |
| `pc_writing_polynomial_functions_and_conjugate_roots` | Writing polynomial functions and conjugate roots | no | other | — |
| `pc_complex_zeros_and_fundamental_theorem_of_algebra` | Complex zeros and The Fundamental Theorem of Algebra | no | other | — |
| `pc_graphs_of_rational_functions` | Graphs of rational functions | no | other | — |
| `pc_rational_equations` | Rational equations | no | solve | `rational_expressions_equations` |
| `pc_polynomial_inequalities` | Polynomial inequalities | no | solve | — |
| `pc_rational_inequalities` | Rational inequalities | no | solve | — |
|  | **Precalculus — Exponential and Logarithmic Expressions** |  |  |  |
| `pc_graphing_exponential_functions` | Graphing exponential functions | no | other | `graphing_exponential_functions` |
| `pc_exponential_equations_not_requiring_logarithms` | Exponential equations not requiring logarithms | no | solve | — |
| `pc_exponents_and_logarithms` | Exponents and logarithms | no | other | — |
| `pc_evaluating_logarithms` | Evaluating logarithms | no | other | — |
| `pc_logarithms_and_exponents_as_inverses` | Logarithms and exponents as inverses | no | other | — |
| `pc_properties_of_logarithms` | Properties of logarithms | no | other | — |
| `pc_writing_logs_in_terms_of_others` | Writing logs in terms of others | no | other | — |
| `pc_exponential_equations_requiring_logarithms` | Exponential equations requiring logarithms | no | solve | — |
| `pc_logarithmic_equations_simple` | Logarithmic equations, simple | no | solve | — |
| `pc_logarithmic_equations_hard` | Logarithmic equations, hard | no | solve | — |
| `pc_graphing_logarithmic_functions` | Graphing logarithmic functions | no | other | — |
| `pc_compound_interest` | Compound interest | no | solve | — |
|  | **Precalculus — Trigonometry** |  |  |  |
| `pc_angles_and_angle_measure` | Angles and angle measure | no | geometry | — |
| `pc_radians_and_degrees` | Radians and degrees | no | geometry | — |
| `pc_right_triangle_trig_finding_ratios` | Right triangle trig, finding ratios | no | geometry | `finding_sine_cosine_tangent` |
| `pc_right_triangle_trig_finding_angles_and_sides` | Right triangle trig, finding angles and sides | no | geometry | — |
| `pc_trig_functions_of_any_angle` | Trig functions of any angle | no | geometry | — |
| `pc_graphing_trig_functions` | Graphing trig functions | no | geometry | — |
| `pc_simple_trig_equations` | Simple trig equations | no | solve | — |
| `pc_inverse_trig_functions` | Inverse trig functions | no | geometry | — |
| `pc_fundamental_identities` | Fundamental identities | no | geometry | — |
| `pc_equations_with_factoring_and_fundamental_identities` | Equations with factoring and fundamental identities | no | solve | — |
| `pc_sum_and_difference_identities` | Sum and Difference Identities | no | geometry | — |
| `pc_multiple_angle_identities` | Multiple-Angle Identities | no | geometry | — |
| `pc_product_to_sum_identities` | Product-to-Sum Identities | no | geometry | — |
| `pc_equations_and_multiple_angle_identities` | Equations and Multiple-Angle Identities | no | solve | — |
| `pc_law_of_sines` | The Law of Sines | no | geometry | — |
| `pc_law_of_cosines` | The Law of Cosines | no | geometry | — |
| `pc_area_and_laws_of_sines_and_cosines` | Area and Laws of Sines and Cosines | no | geometry | — |
|  | **Precalculus — Matrices and Systems** |  |  |  |
| `pc_multivariable_linear_systems_and_row_operations` | Multivariable linear systems and row operations | no | other | — |
| `pc_partial_fraction_decomposition` | Partial fraction decomposition | no | other | — |
|  | **Precalculus — Conic Sections** |  |  |  |
| `pc_parabolas_graphing_and_properties` | Parabolas, graphing and properties | no | other | `graphing_quadratic_functions` |
| `pc_parabolas_writing_equations` | Parabolas, writing equations | no | solve | — |
| `pc_circles_graphing_and_properties` | Circles, graphing and properties | no | other | — |
| `pc_circles_writing_equations` | Circles, writing equations | no | solve | — |
| `pc_ellipses_graphing_and_properties` | Ellipses, graphing and properties | no | other | — |
| `pc_ellipses_writing_equations` | Ellipses, writing equations | no | solve | — |
| `pc_hyperbolas_graphing_and_properties` | Hyperbolas, graphing and properties | no | other | — |
| `pc_hyperbolas_writing_equations` | Hyperbolas, writing equations | no | solve | — |
| `pc_rotations_of_conic_sections` | Rotations of conic sections | no | other | — |
|  | **Precalculus — Discrete Mathematics** |  |  |  |
| `pc_sample_spaces_and_fundamental_counting_principle` | Sample spaces and Fundamental Counting Principle | no | other | — |
| `pc_permutations_vs_combinations` | Permutations vs combinations | no | other | — |
| `pc_binomial_theorem` | The Binomial Theorem | no | other | — |
| `pc_mathematical_induction` | Mathematical induction | no | other | — |
| `pc_probability_independent_dependent_events_word_problems` | Probability: Independent/dependent events, word problems | no | wp | — |
| `pc_probability_independent_dependent_events` | Probability: Independent/dependent events | no | other | — |
| `pc_probability_mutually_exclusive_word_problems` | Probability: Mutually exclusive, word problems | no | wp | — |
| `pc_probability_mutually_exclusive` | Probability: Mutually exclusive | no | other | — |
| `pc_probability_with_permutations_and_combinations` | Probability: With permutations and combinations | no | other | — |
|  | **Precalculus — Sequences and Series** |  |  |  |
| `pc_power_series` | Power series | no | other | — |
|  | **Precalculus — Introduction to Calculus** |  |  |  |
| `pc_limits_by_direct_evaluation` | Limits by direct evaluation | no | other | — |
| `pc_limits_at_kinks_and_jumps` | Limits at kinks and jumps | no | other | — |
| `pc_limits_at_removable_discontinuities` | Limits at removable discontinuities | no | other | — |
| `pc_limits_at_essential_discontinuities` | Limits at essential discontinuities | no | other | — |
| `pc_limits_at_infinity` | Limits at infinity | no | other | — |
| `pc_definition_of_the_derivative` | Definition of the derivative | no | other | — |
| `pc_instantaneous_rates_of_change` | Instantaneous rates of change | no | other | — |
| `pc_power_rule_for_differentiation` | Power rule for differentiation | no | other | — |
| `pc_motion_along_a_line` | Motion along a line | no | other | — |
| `pc_approximating_area_under_a_curve` | Approximating area under a curve | no | other | — |
| `pc_area_under_a_curve_by_limit_of_sums` | Area under a curve by limit of sums | no | other | — |
| `pc_indefinite_integrals` | Indefinite integrals | no | other | — |
|  | **Precalculus — Parametric Equations** |  |  |  |
| `pc_parametric_equations` | Parametric equations | no | solve | — |
| `pc_projectile_motion` | Projectile motion | no | other | — |
|  | **Precalculus — Polar Coordinates** |  |  |  |
| `pc_polar_coordinates` | Polar coordinates | no | other | — |
| `pc_graphs_of_polar_equations` | Graphs of polar equations | no | solve | — |
| `pc_polar_and_rectangular_forms_of_equations` | Polar and rectangular forms of equations | no | solve | — |
| `pc_polar_forms_of_conic_sections` | Polar forms of conic sections | no | other | — |
| `pc_complex_numbers_in_polar_form` | Complex numbers in polar form | no | other | — |
|  | **Precalculus — Vectors** |  |  |  |
| `pc_vectors_basics` | Basics | no | other | — |
| `pc_vectors_diagrams` | Diagrams | no | other | — |
| `pc_vectors_operations` | Operations | no | other | — |
| `pc_dot_products` | Dot products | no | other | — |
|  | **Precalculus — Three-Dimensional Vectors** |  |  |  |
| `pc_3d_points_in_three_dimensions` | Points in three dimensions | no | other | — |
| `pc_3d_vectors_basics` | Basics | no | other | — |
| `pc_3d_vectors_operations` | Operations | no | other | — |
| `pc_cross_products` | Cross products | no | other | — |

## Appendix — not extra catalog leaves

### Generator keys that differ from catalog `id`

| type_id | generator |
|---|---|
| `pc_continuity` | `pc_continuity` |
| `pc_extrema_intervals_of_increase_and_decrease` | `pc_extrema_intervals` |
| `pc_power_functions` | `pc_power_functions` |
| `pc_average_rates_of_change` | `average_rate_of_change` |
| `pc_transformations_of_graphs` | `graph_transformations` |
| `pc_piecewise_functions` | `pc_piecewise_functions` |
| `pc_functions_operations` | `function_operations` |
| `pc_inverses` | `inverse_function_basic` |
| `pc_polynomial_graphs_real_zeros_and_end_behavior` | `polynomial_end_behavior` |
| `pc_dividing_polynomial_functions` | `polynomial_long_division` |
| `pc_remainder_theorem_and_bounds_of_real_zeros` | `remainder_theorem` |
| `pc_writing_polynomial_functions_and_conjugate_roots` | `polynomial_conjugate_writing` |
| `pc_complex_zeros_and_fundamental_theorem_of_algebra` | `pc_complex_zeros` |
| `pc_graphs_of_rational_functions` | `graph_rational` |
| `pc_rational_equations` | `rational_equations` |
| `pc_polynomial_inequalities` | `pc_polynomial_inequalities` |
| `pc_rational_inequalities` | `pc_rational_inequalities` |
| `pc_graphing_exponential_functions` | `graph_exponential` |
| `pc_exponential_equations_not_requiring_logarithms` | `exponential_equation_simple` |
| `pc_exponents_and_logarithms` | `log_evaluate` |
| `pc_evaluating_logarithms` | `log_evaluate` |
| `pc_logarithms_and_exponents_as_inverses` | `log_evaluate` |
| `pc_properties_of_logarithms` | `log_change_of_base` |
| `pc_writing_logs_in_terms_of_others` | `log_change_of_base` |
| `pc_exponential_equations_requiring_logarithms` | `exponential_equation_with_log` |
| `pc_logarithmic_equations_simple` | `log_equation_simple` |
| `pc_logarithmic_equations_hard` | `log_equation_simple` |
| `pc_graphing_logarithmic_functions` | `graph_logarithmic` |
| `pc_compound_interest` | `compound_interest` |
| `pc_angles_and_angle_measure` | `pc_angles_and_angle_measure` |
| `pc_radians_and_degrees` | `trig_unit_circle` |
| `pc_right_triangle_trig_finding_ratios` | `geo_right_triangle_trig_ratio` |
| `pc_right_triangle_trig_finding_angles_and_sides` | `geo_right_triangle_trig` |
| `pc_trig_functions_of_any_angle` | `trig_evaluate` |
| `pc_graphing_trig_functions` | `graphing_trig_functions` |
| `pc_simple_trig_equations` | `simple_trig_equations` |
| `pc_inverse_trig_functions` | `inverse_trig_functions` |
| `pc_fundamental_identities` | `trig_basic_identities` |
| `pc_equations_with_factoring_and_fundamental_identities` | `trig_factoring_equations` |
| `pc_sum_and_difference_identities` | `trig_sum_difference` |
| `pc_multiple_angle_identities` | `trig_multiple_angle` |
| `pc_product_to_sum_identities` | `trig_product_to_sum` |
| `pc_equations_and_multiple_angle_identities` | `trig_factoring_equations` |
| `pc_law_of_sines` | `law_of_sines` |
| `pc_law_of_cosines` | `law_of_cosines` |
| `pc_area_and_laws_of_sines_and_cosines` | `law_of_sines` |
| `pc_parametric_equations` | `pc_parametric_equations` |
| `pc_projectile_motion` | `pc_projectile_motion` |
| `pc_polar_coordinates` | `polar_coordinates` |
| `pc_graphs_of_polar_equations` | `polar_graphs` |
| `pc_polar_and_rectangular_forms_of_equations` | `polar_rectangular_forms` |
| `pc_polar_forms_of_conic_sections` | `polar_conic_forms` |
| `pc_complex_numbers_in_polar_form` | `complex_polar_form` |
| `pc_vectors_basics` | `vector_basics` |
| `pc_vectors_diagrams` | `vector_diagrams` |
| `pc_vectors_operations` | `vector_basics` |
| `pc_dot_products` | `dot_product` |
| `pc_3d_points_in_three_dimensions` | `pc_3d_points` |
| `pc_3d_vectors_basics` | `vector_3d_basics` |
| `pc_3d_vectors_operations` | `vector_3d_operations` |
| `pc_cross_products` | `cross_products` |
| `pc_multivariable_linear_systems_and_row_operations` | `pc_multivariable_systems` |
| `pc_partial_fraction_decomposition` | `partial_fraction_decomposition` |
| `pc_parabolas_graphing_and_properties` | `graph_quadratic` |
| `pc_parabolas_writing_equations` | `conic_sections` |
| `pc_circles_graphing_and_properties` | `conic_sections` |
| `pc_circles_writing_equations` | `conic_sections` |
| `pc_ellipses_graphing_and_properties` | `conic_sections` |
| `pc_ellipses_writing_equations` | `conic_sections` |
| `pc_hyperbolas_graphing_and_properties` | `conic_sections` |
| `pc_hyperbolas_writing_equations` | `conic_sections` |
| `pc_rotations_of_conic_sections` | `conic_rotation_identify` |
| `pc_sample_spaces_and_fundamental_counting_principle` | `stats_counting_principle` |
| `pc_permutations_vs_combinations` | `stats_permutations_vs_combinations` |
| `pc_binomial_theorem` | `binomial_theorem` |
| `pc_mathematical_induction` | `pc_mathematical_induction` |
| `pc_probability_independent_dependent_events_word_problems` | `stats_probability_compound_independent` |
| `pc_probability_independent_dependent_events` | `stats_probability_compound_independent` |
| `pc_probability_mutually_exclusive_word_problems` | `stats_probability_mutually_exclusive` |
| `pc_probability_mutually_exclusive` | `stats_probability_mutually_exclusive` |
| `pc_probability_with_permutations_and_combinations` | `stats_counting_principle` |
| `pc_power_series` | `pc_power_series` |
| `pc_limits_by_direct_evaluation` | `limit_direct_evaluation` |
| `pc_limits_at_kinks_and_jumps` | `limit_jump` |
| `pc_limits_at_removable_discontinuities` | `limit_removable` |
| `pc_limits_at_essential_discontinuities` | `limit_essential` |
| `pc_limits_at_infinity` | `limit_at_infinity` |
| `pc_definition_of_the_derivative` | `definition_of_derivative` |
| `pc_instantaneous_rates_of_change` | `instantaneous_rate_of_change` |
| `pc_power_rule_for_differentiation` | `derivative_power_rule` |
| `pc_motion_along_a_line` | `pc_motion_along_a_line` |
| `pc_approximating_area_under_a_curve` | `riemann_approximate_area` |
| `pc_area_under_a_curve_by_limit_of_sums` | `area_under_curve` |
| `pc_indefinite_integrals` | `integral_power_rule` |

### `QUESTION_TYPES` vs catalog

Every Precalculus catalog `id` is registered in `QUESTION_TYPES`.

Per-type notes: copy `_TEMPLATE.md` → `notes/<gallery-slug>.md` (or
`<type_id>.md` / `<slug>/NOTES.md`). Process: `.cursor/rules/topic-notes-process.mdc`.

## Limitations audit (2026-08-20)

Every catalog `pc_*` has `notes/<type_id>.md` with a **Limitations** section and a
phase-01 gallery folder (`scripts/output/skeleton_phase01_gallery/<type_id>/`).
`PC_DEFERRED` is empty — no leftover engine to implement this pass; gold is **not**
locked on flat-D / red-header leaves (do not invent variety).

| Flag / gap | Count | Notes |
|---|---:|---|
| `## Limitations` section | 94 / 94 | Always present |
| `LOW_VARIETY` red-header | 18 | Flat D / one stem (trig eqns, identities, polar, probability, limits, …) |
| `LIMITATIONS` red-header (no `LOW_VARIETY`) | 19 | Graphing text-only, diagram-named-no-SVG, D-plateau identities, etc. |
| Newly implemented this pass | 0 | Leftover only if notes lock gold — none did |

**Trig equations (explicit):** `pc_simple_trig_equations`,
`pc_equations_and_multiple_angle_identities`,
`pc_equations_with_factoring_and_fundamental_identities` — keep red-header until
OpenStax §7.5 catalog expands (same stem across D common).

**Other HIGH-signal gaps:** `pc_fundamental_identities` (simplify-only / flat D);
`pc_sum_and_difference_identities` (D≥8 tan expand plateau);
`pc_vectors_diagrams` (diagram-named, no SVG); graphing leaves (text property
stems, no axes SVG).
