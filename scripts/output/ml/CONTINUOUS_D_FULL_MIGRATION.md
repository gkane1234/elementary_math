# Continuous-D full curriculum migration

Updated: 2026-07-28 22:01 UTC

## Hard requirement

All catalog topics expose continuous numeric `difficulty` (slider), not EMH-only.
Legacy `difficulty_tier` may remain for preset fallback; the UI hides it when
`difficulty` is present.

## Before / after bucket counts

- **Before:** total=601; already_continuous=138, extend_primitive=38, hard=296, knob_retarget=50, new_generator=78, thin_wrapper=1
- **After:** total=601; already_continuous=601
- **Rows moved to `already_continuous` this pass:** 463

### By course (before → after already_continuous)

| Course | Before already_continuous | After already_continuous | Remaining non-continuous buckets |
|--------|---------------------------:|-------------------------:|----------------------------------|
| grade_6 | 11 | 88 | — |
| pre_algebra | 17 | 41 | — |
| algebra_1 | 53 | 84 | — |
| algebra_2 | 52 | 144 | — |
| geometry | 4 | 86 | — |
| precalculus | 1 | 94 | — |
| calculus | 0 | 64 | — |

## Live schema coverage

- Catalog rows with continuous `difficulty`: **601 / 601**
- EMH-only remaining type_ids: **0** (none)
- Ready missing continuous D: **0**
- Note: `_continuous_d_buckets.json` may still list `pc_vectors_diagrams` as `scaffold`; live catalog uses `generator="vector_diagrams"`.

## Strategy applied

1. **Profile-level**: `continuous_difficulty_settings()` on domain profiles (number/ratio/percent/…, linear/graphing/systems/quadratic/radical/…, trig/log/calc, geometry, sequence, statistics).
2. **Enrichment mixin**: `common_enrichment_profile` includes continuous `difficulty` so every wired generator inherits the slider.
3. **Scaffolds**: unwired catalog types default to `inherits=('common_enrichment',)` so they still expose the field.
4. **UI**: `TopicSettingsFields` hides `difficulty_tier` when continuous `difficulty` is present.

## Remaining stubs / coarse ladders

Schema field is present everywhere. Some generators still sample coarsely (EMH bands via `settings_difficulty_band`, or ignore D and use fixed knobs). True fine-grained D ladders are ongoing per-family work.

Former scaffold leaves (resolved):

- `pc_vectors_diagrams` — now `generator="vector_diagrams"` (tip-to-tail / resultant / opposite stems) + `effort_vector_diagram`.

### Former hard / new_generator / extend_primitive moved this pass (412) — ladders may still be coarse

These now expose continuous `difficulty` but sampling may still map D→EMH bands or fixed knob ranges until family-specific ladders land.

#### grade_6 (37)

- `g6_greatest_common_factor (was hard)`
- `g6_least_common_multiple (was hard)`
- `g6_numbers_on_a_number_line (was hard)`
- `g6_number_line_word_problems (was extend_primitive)`
- `g6_points_on_the_coordinate_plane (was hard)`
- `g6_distances_on_the_coordinate_plane (was hard)`
- `g6_shapes_and_perimeter_on_the_coordinate_plane (was hard)`
- `g6_coordinate_plane_distances_word_problems (was extend_primitive)`
- `g6_properties_of_addition_and_multiplication (was new_generator)`
- `g6_distributive_property_area_diagrams_numeric (was hard)`
- `g6_distributive_property_area_diagrams_algebraic (was hard)`
- `g6_solutions_to_equations (was hard)`
- `g6_equations_tape_diagrams (was hard)`
- `g6_equations_hanger_diagrams (was hard)`
- `g6_solutions_to_inequalities (was extend_primitive)`
- `g6_writing_and_graphing_inequalities (was extend_primitive)`
- `g6_inequalities_hanger_diagrams (was hard)`
- `g6_constant_rate_equations (was extend_primitive)`
- `g6_equations_for_other_relationships (was extend_primitive)`
- `g6_parallelograms_understanding_area_formula (was hard)`
- `g6_parallelograms (was hard)`
- `g6_triangles_understanding_area_formula (was hard)`
- `g6_triangles (was hard)`
- `g6_trapezoids (was hard)`
- `g6_kites (was hard)`
- `g6_polygons_on_a_grid_or_coordinate_plane (was hard)`
- `g6_polygons_and_shaded_regions (was hard)`
- `g6_classifying_and_naming (was hard)`
- `g6_volume_and_surface_area_using_isometric_drawings (was hard)`
- `g6_formulas_for_volume_and_surface_area_of_a_cube (was hard)`
- `g6_interpreting_dot_plots (was hard)`
- `g6_drawing_dot_plots (was hard)`
- `g6_interpreting_histograms (was hard)`
- `g6_drawing_histograms (was hard)`
- `g6_data_center_and_spread (was hard)`
- `g6_interpreting_box_plots (was hard)`
- `g6_drawing_box_plots (was hard)`

#### pre_algebra (13)

- `pa_divisibility (was new_generator)`
- `pa_similar_figures (was extend_primitive)`
- `pa_similar_figures_word_problems (was extend_primitive)`
- `pa_plotting_points (was extend_primitive)`
- `pa_drawing_and_measuring_angles (was hard)`
- `pa_angle_relationships (was hard)`
- `pa_plane_figures_triangles (was hard)`
- `pa_quadrilaterals (was hard)`
- `pa_area_of_triangles_and_quadrilaterals (was hard)`
- `pa_circles (was hard)`
- `pa_transformations (was hard)`
- `pa_classifying_volume_and_surface_area (was hard)`
- `pythagorean_theorem (was hard)`

#### algebra_1 (31)

- `sets_of_numbers (was hard)`
- `mixture_word_problems (was extend_primitive)`
- `distance_rate_time_word_problems (was extend_primitive)`
- `discrete_relations (was new_generator)`
- `continuous_relations (was new_generator)`
- `evaluating_graphing_functions (was new_generator)`
- `graphing_absolute_value_equations (was extend_primitive)`
- `direct_inverse_variation (was hard)`
- `graphing_exponential_functions (was new_generator)`
- `exponential_growth_decay (was new_generator)`
- `graphing_quadratic_functions (was new_generator)`
- `quadratic_solve_by_graphing (was extend_primitive)`
- `graphing_quadratic_inequalities (was extend_primitive)`
- `quadratic_square_roots (was new_generator)`
- `quadratic_formula (was new_generator)`
- `quadratic_discriminant (was new_generator)`
- `quadratic_completing_square_constant (was new_generator)`
- `quadratic_completing_square_solve (was extend_primitive)`
- `radical_distance_formula (was new_generator)`
- `radical_midpoint_formula (was extend_primitive)`
- `radical_add_subtract (was new_generator)`
- `radical_multiply (was new_generator)`
- `radical_divide (was new_generator)`
- `radical_equations (was new_generator)`
- `rational_expression_multiply_divide (was extend_primitive)`
- `rational_expressions_equations (was extend_primitive)`
- `finding_angles (was new_generator)`
- `find_missing_sides_of_triangles (was new_generator)`
- `visualizing_data (was hard)`
- `center_and_spread (was hard)`
- `scatter_plots (was hard)`

#### algebra_2 (92)

- `a2_equations_and_inequalities_distance_rate_time_word_problems (was extend_primitive)`
- `a2_equations_and_inequalities_mixture_word_problems (was extend_primitive)`
- `a2_relations_and_introduction_to_functions_discrete_relations (was new_generator)`
- `a2_relations_and_introduction_to_functions_continuous_relations (was new_generator)`
- `a2_relations_and_introduction_to_functions_evaluating_and_graphing_functions (was new_generator)`
- `a2_linear_relations_and_functions_graphing_absolute_value_equations (was extend_primitive)`
- `a2_direct_and_inverse_variation_direct_and_inverse_variation (was hard)`
- `a2_systems_of_equations_and_inequalities_points_in_three_dimensions (was extend_primitive)`
- `a2_systems_of_equations_and_inequalities_planes (was extend_primitive)`
- `a2_systems_of_equations_and_inequalities_solving_systems_with_three_variables (was extend_primitive)`
- `a2_matrices_inverses (was hard)`
- `a2_matrices_cramers_rule (was hard)`
- `a2_matrices_geometric_transformations (was new_generator)`
- `a2_complex_numbers_graphing (was new_generator)`
- `a2_complex_numbers_rationalizing_denominators (was new_generator)`
- `a2_quadratic_functions_and_inequalities_graphing_quadratic_functions (was extend_primitive)`
- `a2_quadratic_functions_and_inequalities_graphing_quadratic_inequalities (was extend_primitive)`
- `a2_quadratic_functions_and_inequalities_solving_equations_by_graphing (was extend_primitive)`
- `a2_quadratic_functions_and_inequalities_solving_equations_by_taking_square_roots (was new_generator)`
- `a2_quadratic_functions_and_inequalities_completing_the_square (was new_generator)`
- `a2_quadratic_functions_and_inequalities_solving_equations_by_completing_the_square (was new_generator)`
- `a2_quadratic_functions_and_inequalities_solving_equations_with_the_quadratic_formula (was new_generator)`
- `a2_quadratic_functions_and_inequalities_the_discriminant (was extend_primitive)`
- `a2_general_functions_evaluating (was new_generator)`
- `a2_general_functions_inverses (was new_generator)`
- `a2_radical_functions_and_rational_exponents_simplifying_radicals (was new_generator)`
- `a2_radical_functions_and_rational_exponents_adding_and_subtracting_radical_expressions (was new_generator)`
- `a2_radical_functions_and_rational_exponents_multiplying_radical_expressions (was new_generator)`
- `a2_radical_functions_and_rational_exponents_dividing_radical_expressions (was new_generator)`
- `a2_radical_functions_and_rational_exponents_connecting_radical_expressions_and_rational_exponents (was new_generator)`
- `a2_radical_functions_and_rational_exponents_evaluating_rational_exponent_expressions (was new_generator)`
- `a2_radical_functions_and_rational_exponents_the_properties_of_exponents (was new_generator)`
- `a2_radical_functions_and_rational_exponents_radical_equations (was new_generator)`
- `a2_radical_functions_and_rational_exponents_rational_exponent_equations (was new_generator)`
- `a2_radical_functions_and_rational_exponents_graphing_radical_equations (was new_generator)`
- `a2_radical_functions_and_rational_exponents_domain_and_range_of_radical_functions (was new_generator)`
- `a2_conic_sections_parabolas_graphing_and_properties (was new_generator)`
- `a2_conic_sections_parabolas_writing_equations (was new_generator)`
- `a2_conic_sections_circles_graphing_and_properties (was hard)`
- `a2_conic_sections_circles_writing_equations (was hard)`
- … +52 more

#### geometry (82)

- `geo_review_simplifying_square_roots (was new_generator)`
- `geo_review_adding_and_subtracting_square_roots (was new_generator)`
- `geo_review_multiplying_square_roots (was new_generator)`
- `geo_review_dividing_square_roots (was new_generator)`
- `geo_basics_line_segments_and_their_measures (was hard)`
- `geo_basics_segment_addition_postulate (was hard)`
- `geo_basics_angles_and_their_measures (was hard)`
- `geo_basics_classifying_angles (was hard)`
- `geo_basics_basic_angle_terminology (was hard)`
- `geo_basics_angle_addition_postulate (was hard)`
- `geo_basics_angle_relationships (was hard)`
- `geo_basics_geometric_diagrams_and_notation (was hard)`
- `geo_parallel_parallel_lines_and_transversals (was hard)`
- `geo_parallel_points_of_the_coordinate_plane (was hard)`
- `geo_parallel_distance_formula (was hard)`
- `geo_congruent_classifying_triangles (was hard)`
- `geo_congruent_triangle_angle_sum (was hard)`
- `geo_congruent_triangle_perimeter (was hard)`
- `geo_congruent_exterior_angle_theorem (was hard)`
- `geo_congruent_triangles_and_congruence (was hard)`
- `geo_congruent_proving_triangles_congruent (was hard)`
- `geo_congruent_isosceles_and_equilateral_triangles (was hard)`
- `geo_properties_midsegment (was hard)`
- `geo_properties_angle_bisectors (was hard)`
- `geo_properties_medians (was hard)`
- `geo_properties_centroid (was hard)`
- `geo_properties_triangle_inequality_theorem (was hard)`
- `geo_properties_inequalities_in_one_triangle (was hard)`
- `geo_quadrilaterals_classifying (was hard)`
- `geo_quadrilaterals_angles (was hard)`
- `geo_quadrilaterals_parallelograms (was hard)`
- `geo_quadrilaterals_trapezoids (was hard)`
- `geo_quadrilaterals_rhombuses (was hard)`
- `geo_quadrilaterals_kites (was hard)`
- `geo_quadrilaterals_area_of_triangles_and_quadrilaterals (was hard)`
- `geo_quadrilaterals_polygon_basics (was hard)`
- `geo_quadrilaterals_area_of_regular_polygons (was hard)`
- `geo_similarity_similar_polygons (was hard)`
- `geo_similarity_similar_triangles (was hard)`
- `geo_similarity_similar_right_triangles (was hard)`
- … +42 more

#### precalculus (93)

- `pc_continuity (was hard)`
- `pc_extrema_intervals_of_increase_and_decrease (was hard)`
- `pc_power_functions (was hard)`
- `pc_average_rates_of_change (was hard)`
- `pc_transformations_of_graphs (was hard)`
- `pc_piecewise_functions (was hard)`
- `pc_functions_operations (was hard)`
- `pc_inverses (was hard)`
- `pc_polynomial_graphs_real_zeros_and_end_behavior (was hard)`
- `pc_dividing_polynomial_functions (was hard)`
- `pc_remainder_theorem_and_bounds_of_real_zeros (was hard)`
- `pc_writing_polynomial_functions_and_conjugate_roots (was hard)`
- `pc_complex_zeros_and_fundamental_theorem_of_algebra (was hard)`
- `pc_graphs_of_rational_functions (was hard)`
- `pc_rational_equations (was extend_primitive)`
- `pc_polynomial_inequalities (was hard)`
- `pc_rational_inequalities (was hard)`
- `pc_graphing_exponential_functions (was hard)`
- `pc_exponential_equations_not_requiring_logarithms (was hard)`
- `pc_exponents_and_logarithms (was hard)`
- `pc_evaluating_logarithms (was hard)`
- `pc_logarithms_and_exponents_as_inverses (was hard)`
- `pc_properties_of_logarithms (was hard)`
- `pc_writing_logs_in_terms_of_others (was hard)`
- `pc_exponential_equations_requiring_logarithms (was hard)`
- `pc_logarithmic_equations_simple (was hard)`
- `pc_logarithmic_equations_hard (was hard)`
- `pc_graphing_logarithmic_functions (was hard)`
- `pc_compound_interest (was hard)`
- `pc_angles_and_angle_measure (was hard)`
- `pc_radians_and_degrees (was hard)`
- `pc_right_triangle_trig_finding_ratios (was hard)`
- `pc_right_triangle_trig_finding_angles_and_sides (was hard)`
- `pc_trig_functions_of_any_angle (was hard)`
- `pc_graphing_trig_functions (was hard)`
- `pc_simple_trig_equations (was hard)`
- `pc_inverse_trig_functions (was hard)`
- `pc_fundamental_identities (was hard)`
- `pc_equations_with_factoring_and_fundamental_identities (was hard)`
- `pc_sum_and_difference_identities (was hard)`
- … +53 more

#### calculus (64)

- `calc_limits_by_direct_evaluation (was hard)`
- `calc_limits_at_jump_discontinuities_and_kinks (was hard)`
- `calc_limits_at_removable_discontinuities (was hard)`
- `calc_limits_at_essential_discontinuities (was hard)`
- `calc_limits_at_infinity (was hard)`
- `calc_continuity_determining_and_classifying (was hard)`
- `calc_diff_average_rates_of_change (was hard)`
- `calc_diff_definition_of_the_derivative (was hard)`
- `calc_diff_instantaneous_rates_of_change (was hard)`
- `calc_diff_power_rule (was hard)`
- `calc_diff_higher_order_derivatives (was hard)`
- `calc_diff_product_rule (was hard)`
- `calc_diff_quotient_rule (was hard)`
- `calc_diff_chain_rule (was hard)`
- `calc_diff_rules_using_tables (was hard)`
- `calc_diff_trigonometric (was hard)`
- `calc_diff_inverse_trigonometric (was hard)`
- `calc_diff_natural_logarithms_and_exponentials (was hard)`
- `calc_diff_other_base_logarithms_and_exponentials (was hard)`
- `calc_diff_logarithmic (was hard)`
- `calc_diff_implicit (was hard)`
- `calc_diff_inverse_functions (was hard)`
- `calc_app_diff_slope_tangent_and_normal_lines (was hard)`
- `calc_app_diff_rolles_theorem (was hard)`
- `calc_app_diff_mean_value_theorem (was hard)`
- `calc_app_diff_intervals_of_increase_and_decrease (was hard)`
- `calc_app_diff_intervals_of_concavity (was hard)`
- `calc_app_diff_relative_extrema (was hard)`
- `calc_app_diff_absolute_extrema (was hard)`
- `calc_app_diff_optimization (was hard)`
- `calc_app_diff_curve_sketching (was hard)`
- `calc_app_diff_graphical_comparison_of_f_f_prime_and_f_double_prime (was hard)`
- `calc_app_diff_motion_along_a_line (was hard)`
- `calc_app_diff_related_rates (was hard)`
- `calc_app_diff_differentials (was hard)`
- `calc_app_diff_newtons_method (was hard)`
- `calc_app_diff_limits_in_form_of_definition_of_derivative (was hard)`
- `calc_app_diff_lhopitals_rule (was hard)`
- `calc_indef_int_power_rule (was hard)`
- `calc_indef_int_logarithmic_rule_and_exponentials (was hard)`
- … +24 more

## Files touched (this / sibling session)

- `question_engine/settings/domains/common.py` — `continuous_difficulty_settings`
- `question_engine/settings/profiles.py` — domain profiles + `common_enrichment`
- `question_engine/settings/domains/geometry.py` — base `geometry_settings`
- `question_engine/core/scaffold.py` — default enrichment for unwired types
- `question_engine/settings/generator_profiles.py` — per-type wiring / excludes
- `scripts/output/_continuous_d_buckets.json` — bucket audit refresh
- `question_engine/tests/test_continuous_d_migration.py` — full ready-catalog assert

