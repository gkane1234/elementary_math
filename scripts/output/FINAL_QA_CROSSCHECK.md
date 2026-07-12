# FINAL QA Cross-Check

- Ready catalog types (unique, selectable): **588**
- Sampled in this run: **469**
- Per type: Easy/Medium/Hard × 3 = 9 generations

## Summary counts

| Status | Count |
|--------|------:|
| PASS | 290 |
| FAIL | 0 |
| NOTE (soft) | 179 |

### By bucket

| Bucket | PASS | FAIL | NOTE |
|--------|-----:|-----:|-----:|
| algebra1 | 69 | 0 | 12 |
| algebra2 | 83 | 0 | 41 |
| calculus | 39 | 0 | 23 |
| geometry_review | 4 | 0 | 1 |
| geometry_sample | 16 | 0 | 24 |
| grade6_sample | 10 | 0 | 15 |
| prealgebra_sample | 12 | 0 | 8 |
| precalculus | 38 | 0 | 52 |
| radical_rational | 19 | 0 | 3 |

## FAIL details

_None._

## NOTE (soft / deferred)

- `coin_word_problems` (wp_coin): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `finding_sine_cosine_tangent` (geo_right_triangle_trig_ratio): same prompt text E/H (difficulty in numbers/graph/diagram; answers differ)
- `mixture_word_problems` (wp_mixture): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `percent_of_change` (percent_of_change): weak E/H diversity: same skeleton after number-normalization
- `quadratic_completing_square_constant` (quadratic_completing_square_constant): weak E/H diversity: same skeleton after number-normalization
- `radical_distance_formula` (radical_distance_formula): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `radical_midpoint_formula` (radical_midpoint_formula): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `scientific_notation_add_subtract` (scientific_notation_add_subtract): weak E/H diversity: same skeleton after number-normalization
- `slope` (slope): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `solving_proportions` (solving_proportions): weak E/H diversity: same skeleton after number-normalization
- `systems_word_problems` (wp_systems): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `writing_linear_equations` (writing_linear_equations): same prompt text E/H (difficulty in numbers/graph/diagram; answers differ); weak diversity: all 9 samples same normalized template
- `a2_complex_numbers_absolute_value` (complex_absolute_value): weak E/H diversity: same skeleton after number-normalization
- `a2_conic_sections_circles_graphing_and_properties` (conic_sections): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `a2_conic_sections_circles_writing_equations` (conic_sections): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `a2_conic_sections_ellipses_graphing_and_properties` (conic_sections): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `a2_conic_sections_ellipses_writing_equations` (conic_sections): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `a2_conic_sections_hyperbolas_writing_equations` (conic_sections): weak E/H diversity: same skeleton after number-normalization
- `a2_conic_sections_parabolas_writing_equations` (quadratic_vertex_form_write): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `a2_equations_and_inequalities_mixture_word_problems` (wp_mixture): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `a2_exponential_and_logarithmic_expressions_exponential_equations_not_requiring_logarithms` (exponential_equation_simple): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `a2_exponential_and_logarithmic_expressions_logarithmic_equations_hard` (log_equation_simple): weak E/H diversity: same skeleton after number-normalization
- `a2_exponential_and_logarithmic_expressions_properties_of_logarithms` (log_change_of_base): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `a2_exponential_and_logarithmic_expressions_writing_logs_in_terms_of_others` (log_change_of_base): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `a2_linear_relations_and_functions_writing_linear_equations` (writing_linear_equations): same prompt text E/H (difficulty in numbers/graph/diagram; answers differ); weak diversity: all 9 samples same normalized template
- `a2_matrices_determinants` (matrix_operations): weak E/H diversity: same skeleton after number-normalization
- `a2_matrices_equations` (matrix_operations): weak E/H diversity: same skeleton after number-normalization
- `a2_matrices_inverses` (matrix_inverse): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `a2_polynomial_functions_conjugate_roots_and_writing_functions` (polynomial_conjugate_writing): weak E/H diversity: same skeleton after number-normalization
- `a2_polynomial_functions_fundamental_theorem_of_algebra` (fundamental_theorem_algebra): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `a2_polynomial_functions_the_binomial_theorem` (binomial_theorem): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `a2_polynomial_functions_writing_functions` (polynomial_writing): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `a2_probability_and_statistics_combinations` (stats_combinations): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `a2_probability_and_statistics_permutations` (stats_permutations): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `a2_probability_and_statistics_permutations_vs_combinations` (stats_permutations_vs_combinations): weak E/H diversity: same skeleton after number-normalization
- `a2_probability_and_statistics_probability_with_permutations_and_combinations` (stats_permutations_vs_combinations): weak E/H diversity: same skeleton after number-normalization
- `a2_relations_and_introduction_to_functions_evaluating_and_graphing_functions` (evaluating_graphing_functions): weak E/H diversity: same skeleton after number-normalization
- `a2_sequences_and_series_arithmetic_and_geometric_mean` (sequence_arithmetic_geometric_mean): weak E/H diversity: same skeleton after number-normalization
- `a2_sequences_and_series_arithmetic_sequences` (sequence_arithmetic_nth_term): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `a2_sequences_and_series_arithmetic_series` (sequence_arithmetic_series): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `a2_sequences_and_series_general_sequences` (sequence_arithmetic_nth_term): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `a2_sequences_and_series_general_series` (sequence_arithmetic_series): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `a2_sequences_and_series_geometric_sequences` (sequence_geometric_nth_term): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `a2_sequences_and_series_geometric_series` (sequence_geometric_series): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `a2_systems_of_equations_and_inequalities_points_in_three_dimensions` (points_three_dimensions): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `a2_systems_of_equations_and_inequalities_systems_of_equations_word_problems_2_variables` (wp_systems): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `a2_trigonometry_angles_and_angle_measure` (angle_measure): weak E/H diversity: same skeleton after number-normalization
- `a2_trigonometry_arc_length_and_sector_area` (geo_arc_sector): weak E/H diversity: same skeleton after number-normalization
- `a2_trigonometry_area_and_laws_of_sines_and_cosines` (law_of_sines): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `a2_trigonometry_degrees_and_degrees_minutes_seconds` (degrees_minutes_seconds): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `a2_trigonometry_the_law_of_cosines` (law_of_cosines): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `a2_trigonometry_the_law_of_sines` (law_of_sines): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `a2_trigonometry_trig_functions_of_any_angle` (trig_evaluate): weak E/H diversity: same skeleton after number-normalization
- `calc_app_diff_absolute_extrema` (calculus_foundations): weak E/H diversity: same skeleton after number-normalization; thin generator: calculus_foundations (topic-routed fallback); weak diversity: all 9 samples same normalized template
- `calc_app_diff_differentials` (calculus_foundations): thin generator: calculus_foundations (topic-routed fallback)
- `calc_app_diff_intervals_of_concavity` (calculus_foundations): weak E/H diversity: same skeleton after number-normalization; thin generator: calculus_foundations (topic-routed fallback); weak diversity: all 9 samples same normalized template
- `calc_app_diff_lhopitals_rule` (lhopitals_rule): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `calc_app_diff_motion_along_a_line` (calculus_foundations): weak E/H diversity: same skeleton after number-normalization; thin generator: calculus_foundations (topic-routed fallback); weak diversity: all 9 samples same normalized template
- `calc_app_diff_newtons_method` (calculus_foundations): weak E/H diversity: same skeleton after number-normalization; thin generator: calculus_foundations (topic-routed fallback); weak diversity: all 9 samples same normalized template
- `calc_app_diff_optimization` (calculus_foundations): weak E/H diversity: same skeleton after number-normalization; thin generator: calculus_foundations (topic-routed fallback); weak diversity: all 9 samples same normalized template
- `calc_app_diff_related_rates` (related_rates_simple): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `calc_app_diff_relative_extrema` (calculus_foundations): weak E/H diversity: same skeleton after number-normalization; thin generator: calculus_foundations (topic-routed fallback); weak diversity: all 9 samples same normalized template
- `calc_app_diff_slope_tangent_and_normal_lines` (calculus_foundations): thin generator: calculus_foundations (topic-routed fallback)
- `calc_app_int_area_between_curves` (area_between_curves): E/H sample sets matched (small discrete pool / fixed template; soft); weak diversity: all 9 samples same normalized template
- `calc_app_int_motion_along_a_line_revisited` (calculus_foundations): weak E/H diversity: same skeleton after number-normalization; thin generator: calculus_foundations (topic-routed fallback); weak diversity: all 9 samples same normalized template
- `calc_def_int_approximating_area_under_a_curve` (riemann_approximate_area): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `calc_diff_eq_introduction` (calculus_foundations): thin generator: calculus_foundations (topic-routed fallback)
- `calc_diff_implicit` (derivative_implicit): weak E/H diversity: same skeleton after number-normalization
- `calc_diff_instantaneous_rates_of_change` (calculus_foundations): weak E/H diversity: same skeleton after number-normalization; thin generator: calculus_foundations (topic-routed fallback); weak diversity: all 9 samples same normalized template
- `calc_diff_inverse_functions` (calculus_foundations): weak E/H diversity: same skeleton after number-normalization; thin generator: calculus_foundations (topic-routed fallback); weak diversity: all 9 samples same normalized template
- `calc_diff_logarithmic` (derivative_ln_exp): weak E/H diversity: same skeleton after number-normalization
- `calc_indef_int_inverse_trigonometric_with_substitution` (calculus_foundations): weak E/H diversity: same skeleton after number-normalization; thin generator: calculus_foundations (topic-routed fallback); weak diversity: all 9 samples same normalized template
- `calc_indef_int_logarithmic_rule_and_exponentials_with_substitution` (calculus_foundations): weak E/H diversity: same skeleton after number-normalization; thin generator: calculus_foundations (topic-routed fallback); weak diversity: all 9 samples same normalized template
- `calc_indef_int_trigonometric_with_substitution` (calculus_foundations): weak E/H diversity: same skeleton after number-normalization; thin generator: calculus_foundations (topic-routed fallback); weak diversity: all 9 samples same normalized template
- `calc_limits_at_essential_discontinuities` (limit_removable): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `calc_limits_at_removable_discontinuities` (limit_removable): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `geo_review_simplifying_square_roots` (radical_simplification): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `geo_circles_arc_length_and_sector_area` (geo_arc_sector): weak E/H diversity: same skeleton after number-normalization
- `geo_circles_circumference_and_area` (geo_circle_measure): weak E/H diversity: same skeleton after number-normalization
- `geo_circles_measures_of_arcs_and_central_angles` (geo_central_arc): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `geo_circles_naming_arcs_and_central_angles` (geo_central_arc): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `geo_circles_secant_and_tangent_angles` (geo_secant_tangent_segments): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `geo_circles_segment_measures` (geo_circle_segment_measures): E/H sample sets matched (small discrete pool / fixed template; soft); weak diversity: all 9 samples same normalized template
- `geo_circles_using_equations_of_circles` (geo_circle_equation_using): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `geo_circles_writing_equations_of_circles` (geo_circle_equation_writing): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `geo_congruent_classifying_triangles` (geo_classifying_triangles): same prompt text E/H (difficulty in numbers/graph/diagram; answers differ)
- `geo_congruent_exterior_angle_theorem` (geo_exterior_angle): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `geo_congruent_isosceles_and_equilateral_triangles` (geo_isosceles_triangle): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `geo_congruent_triangle_perimeter` (geo_triangle_perimeter): same prompt text E/H (difficulty in numbers/graph/diagram; answers differ); weak diversity: all 9 samples same normalized template
- `geo_congruent_triangles_and_congruence` (geo_triangle_congruence): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `geo_quadrilaterals_angles` (geo_polygon_interior): weak E/H diversity: same skeleton after number-normalization
- `geo_quadrilaterals_area_of_regular_polygons` (geo_regular_polygon_area): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `geo_quadrilaterals_area_of_triangles_and_quadrilaterals` (geo_triangle_area): same prompt text E/H (difficulty in numbers/graph/diagram; answers differ); weak diversity: all 9 samples same normalized template
- `geo_quadrilaterals_kites` (geo_kite_area): same prompt text E/H (difficulty in numbers/graph/diagram; answers differ); weak diversity: all 9 samples same normalized template
- `geo_quadrilaterals_parallelograms` (geo_parallelogram_area): same prompt text E/H (difficulty in numbers/graph/diagram; answers differ); weak diversity: all 9 samples same normalized template
- `geo_quadrilaterals_rhombuses` (geo_parallelogram_area): same prompt text E/H (difficulty in numbers/graph/diagram; answers differ); weak diversity: all 9 samples same normalized template
- `geo_quadrilaterals_trapezoids` (geo_trapezoid_area): same prompt text E/H (difficulty in numbers/graph/diagram; answers differ); weak diversity: all 9 samples same normalized template
- `geo_similarity_proportional_parts_in_triangles_and_parallel_lines` (geo_proportional_parts): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `geo_similarity_similar_polygons` (geo_similar_polygons): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `geo_trig_finding_angle_measures` (geo_right_triangle_trig_angle): weak E/H diversity: same skeleton after number-normalization
- `geo_trig_trigonometry_and_area` (geo_triangle_area): same prompt text E/H (difficulty in numbers/graph/diagram; answers differ); weak diversity: all 9 samples same normalized template
- `g6_comparing_rates` (g6_unit_rates): weak E/H diversity: same skeleton after number-normalization
- `g6_comparing_ratios` (g6_equivalent_ratios): weak E/H diversity: same skeleton after number-normalization
- `g6_decimal_addition` (g6_decimal_addition): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `g6_decimal_multiplication` (g6_decimal_multiplication): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `g6_decimal_subtraction` (g6_decimal_subtraction): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `g6_dividing_decimals_by_decimals` (g6_decimal_divide): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `g6_dividing_decimals_by_whole_numbers` (g6_dividing_decimals_by_whole_numbers): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `g6_dividing_whole_numbers_that_result_in_decimals` (g6_integer_divide): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `g6_equivalent_ratios` (g6_equivalent_ratios): weak E/H diversity: same skeleton after number-normalization
- `g6_factoring` (g6_factoring): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `g6_finding_percents_with_equivalent_fractions` (percents): weak E/H diversity: same skeleton after number-normalization
- `g6_how_much_in_each_group_time` (g6_fraction_divide_each): weak E/H diversity: same skeleton after number-normalization
- `g6_long_division_with_remainders` (g6_long_division_with_remainders): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `g6_relating_percents_fractions_and_decimals` (g6_relating_percents_fractions_and_decimals): weak E/H diversity: same skeleton after number-normalization
- `g6_what_fraction_of_a_whole` (g6_fraction_of_whole): weak E/H diversity: same skeleton after number-normalization
- `pa_checking_for_a_proportion` (solving_proportions): weak E/H diversity: same skeleton after number-normalization
- `pa_divisibility` (g6_divisibility): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `pa_equations_multi_step_equations` (multi_step_equations): weak E/H diversity: same skeleton after number-normalization
- `pa_equations_two_step_word_problems` (wp_two_step_equation): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `pa_factoring` (g6_factoring): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `pa_greatest_common_factor` (g6_greatest_common_factor): weak E/H diversity: same skeleton after number-normalization
- `pa_similar_figures` (wp_similar_figures): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `pa_similar_figures_word_problems` (wp_similar_figures): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `pc_3d_points_in_three_dimensions` (precalc_foundations): weak E/H diversity: same skeleton after number-normalization; thin generator: precalc_foundations (topic-routed fallback); weak diversity: all 9 samples same normalized template
- `pc_3d_vectors_basics` (vector_3d_basics): weak E/H diversity: same skeleton after number-normalization
- `pc_3d_vectors_operations` (precalc_foundations): weak E/H diversity: same skeleton after number-normalization; thin generator: precalc_foundations (topic-routed fallback); weak diversity: all 9 samples same normalized template
- `pc_angles_and_angle_measure` (precalc_foundations): weak E/H diversity: same skeleton after number-normalization; thin generator: precalc_foundations (topic-routed fallback); weak diversity: all 9 samples same normalized template
- `pc_approximating_area_under_a_curve` (riemann_approximate_area): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `pc_area_and_laws_of_sines_and_cosines` (law_of_sines): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `pc_average_rates_of_change` (precalc_foundations): weak E/H diversity: same skeleton after number-normalization; thin generator: precalc_foundations (topic-routed fallback); weak diversity: all 9 samples same normalized template
- `pc_binomial_theorem` (binomial_theorem): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `pc_circles_graphing_and_properties` (conic_sections): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `pc_circles_writing_equations` (conic_sections): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `pc_complex_zeros_and_fundamental_theorem_of_algebra` (precalc_foundations): weak E/H diversity: same skeleton after number-normalization; thin generator: precalc_foundations (topic-routed fallback); weak diversity: all 9 samples same normalized template
- `pc_compound_interest` (compound_interest): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `pc_continuity` (precalc_foundations): weak E/H diversity: same skeleton after number-normalization; thin generator: precalc_foundations (topic-routed fallback); weak diversity: all 9 samples same normalized template
- `pc_cross_products` (precalc_foundations): weak E/H diversity: same skeleton after number-normalization; thin generator: precalc_foundations (topic-routed fallback); weak diversity: all 9 samples same normalized template
- `pc_dot_products` (dot_product): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `pc_ellipses_graphing_and_properties` (conic_sections): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `pc_ellipses_writing_equations` (conic_sections): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `pc_evaluating_logarithms` (log_evaluate): weak E/H diversity: same skeleton after number-normalization
- `pc_exponential_equations_not_requiring_logarithms` (exponential_equation_simple): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `pc_extrema_intervals_of_increase_and_decrease` (precalc_foundations): weak E/H diversity: same skeleton after number-normalization; thin generator: precalc_foundations (topic-routed fallback); weak diversity: all 9 samples same normalized template
- `pc_hyperbolas_graphing_and_properties` (conic_sections): weak E/H diversity: same skeleton after number-normalization
- `pc_hyperbolas_writing_equations` (conic_sections): weak E/H diversity: same skeleton after number-normalization
- `pc_instantaneous_rates_of_change` (precalc_foundations): weak E/H diversity: same skeleton after number-normalization; thin generator: precalc_foundations (topic-routed fallback); weak diversity: all 9 samples same normalized template
- `pc_inverses` (inverse_function_basic): weak E/H diversity: same skeleton after number-normalization
- `pc_law_of_cosines` (law_of_cosines): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `pc_law_of_sines` (law_of_sines): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `pc_limits_at_essential_discontinuities` (precalc_foundations): weak E/H diversity: same skeleton after number-normalization; thin generator: precalc_foundations (topic-routed fallback); weak diversity: all 9 samples same normalized template
- `pc_limits_at_kinks_and_jumps` (precalc_foundations): weak E/H diversity: same skeleton after number-normalization; thin generator: precalc_foundations (topic-routed fallback); weak diversity: all 9 samples same normalized template
- `pc_limits_at_removable_discontinuities` (limit_removable): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `pc_logarithmic_equations_hard` (log_equation_simple): weak E/H diversity: same skeleton after number-normalization
- `pc_mathematical_induction` (precalc_foundations): E/H sample sets matched (small discrete pool / fixed template; soft); thin generator: precalc_foundations (topic-routed fallback); weak diversity: all 9 samples same normalized template
- `pc_motion_along_a_line` (precalc_foundations): weak E/H diversity: same skeleton after number-normalization; thin generator: precalc_foundations (topic-routed fallback); weak diversity: all 9 samples same normalized template
- `pc_multivariable_linear_systems_and_row_operations` (precalc_foundations): weak E/H diversity: same skeleton after number-normalization; thin generator: precalc_foundations (topic-routed fallback); weak diversity: all 9 samples same normalized template
- `pc_parabolas_writing_equations` (conic_sections): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `pc_parametric_equations` (precalc_foundations): weak E/H diversity: same skeleton after number-normalization; thin generator: precalc_foundations (topic-routed fallback); weak diversity: all 9 samples same normalized template
- `pc_partial_fraction_decomposition` (precalc_foundations): weak E/H diversity: same skeleton after number-normalization; thin generator: precalc_foundations (topic-routed fallback); weak diversity: all 9 samples same normalized template
- `pc_permutations_vs_combinations` (precalc_foundations): weak E/H diversity: same skeleton after number-normalization; thin generator: precalc_foundations (topic-routed fallback); weak diversity: all 9 samples same normalized template
- `pc_piecewise_functions` (precalc_foundations): weak E/H diversity: same skeleton after number-normalization; thin generator: precalc_foundations (topic-routed fallback); weak diversity: all 9 samples same normalized template
- `pc_polar_coordinates` (polar_coordinates): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `pc_polynomial_inequalities` (precalc_foundations): weak E/H diversity: same skeleton after number-normalization; thin generator: precalc_foundations (topic-routed fallback); weak diversity: all 9 samples same normalized template
- `pc_power_functions` (precalc_foundations): weak E/H diversity: same skeleton after number-normalization; thin generator: precalc_foundations (topic-routed fallback); weak diversity: all 9 samples same normalized template
- `pc_power_series` (precalc_foundations): weak E/H diversity: same skeleton after number-normalization; thin generator: precalc_foundations (topic-routed fallback); weak diversity: all 9 samples same normalized template
- `pc_probability_independent_dependent_events` (stats_probability_compound_independent): weak E/H diversity: same skeleton after number-normalization
- `pc_probability_independent_dependent_events_word_problems` (stats_probability_compound_independent): weak E/H diversity: same skeleton after number-normalization
- `pc_product_to_sum_identities` (trig_product_to_sum): E/H sample sets matched (small discrete pool / fixed template; soft)
- `pc_projectile_motion` (precalc_foundations): weak E/H diversity: same skeleton after number-normalization; thin generator: precalc_foundations (topic-routed fallback); weak diversity: all 9 samples same normalized template
- `pc_properties_of_logarithms` (log_change_of_base): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `pc_sample_spaces_and_fundamental_counting_principle` (stats_counting_principle): weak E/H diversity: same skeleton after number-normalization
- `pc_transformations_of_graphs` (graph_transformations): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `pc_vectors_operations` (vector_basics): weak E/H diversity: same skeleton after number-normalization
- `pc_writing_logs_in_terms_of_others` (log_change_of_base): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `pc_writing_polynomial_functions_and_conjugate_roots` (precalc_foundations): weak E/H diversity: same skeleton after number-normalization; thin generator: precalc_foundations (topic-routed fallback); weak diversity: all 9 samples same normalized template
- `a2_complex_numbers_rationalizing_denominators` (radical_simplification): weak E/H diversity: same skeleton after number-normalization; uses radical_simplification for rationalizing denominators; weak diversity: all 9 samples same normalized template
- `a2_radical_functions_and_rational_exponents_simplifying_radicals` (radical_simplification): weak E/H diversity: same skeleton after number-normalization; weak diversity: all 9 samples same normalized template
- `pc_rational_inequalities` (precalc_foundations): weak E/H diversity: same skeleton after number-normalization; thin generator: precalc_foundations (topic-routed fallback); weak diversity: all 9 samples same normalized template

## PASS types

290 types passed hard checks. IDs:

### algebra1 (69)

`absolute_value_equations`, `absolute_value_inequalities`, `age_word_problems`, `center_and_spread`, `compound_inequalities`, `consecutive_integers_word_problems`, `continuous_relations`, `direct_inverse_variation`
`discrete_relations`, `distance_rate_time_word_problems`, `distributive_property`, `evaluating_graphing_functions`, `exponential_growth_decay`, `find_missing_sides_of_triangles`, `finding_angles`, `graphing_absolute_value_equations`
`graphing_exponential_functions`, `graphing_linear_equations`, `graphing_linear_inequalities`, `graphing_quadratic_functions`, `graphing_quadratic_inequalities`, `graphing_single_variable_inequalities`, `graphing_systems_of_inequalities`, `literal_equations`
`more_on_slope`, `multi_step_equations`, `multi_step_inequalities`, `one_step_equations`, `one_step_inequalities`, `order_of_operations`, `percent_word_problems`, `percents`
`polynomial_add_subtract`, `polynomial_factoring_common_factor`, `polynomial_factoring_grouping`, `polynomial_factoring_special_cases`, `polynomial_multiply`, `polynomial_multiply_special`, `polynomial_naming`, `properties_of_exponents`
`quadratic_completing_square_solve`, `quadratic_discriminant`, `quadratic_factoring_equations`, `quadratic_formula`, `quadratic_solve_by_graphing`, `quadratic_square_roots`, `radical_add_subtract`, `radical_divide`
`radical_equations`, `radical_multiply`, `rational_add_subtract`, `rational_divide`, `rational_expression_multiply_divide`, `rational_expression_simplification`, `rational_expressions_equations`, `rational_multiply`
`rational_simplification`, `scientific_notation_operations`, `scientific_notation_write`, `sets_of_numbers`, `systems_elimination`, `systems_graphing`, `systems_substitution`, `two_step_equations`
`two_step_inequalities`, `using_statistical_models`, `verbal_expressions`, `visualizing_data`, `work_word_problems`

### algebra2 (83)

`a2_beginning_algebra_order_of_operations`, `a2_beginning_algebra_simplifying_algebraic_expressions`, `a2_complex_numbers_graphing`, `a2_complex_numbers_operations`, `a2_conic_sections_classifying`, `a2_conic_sections_hyperbolas_graphing_and_properties`, `a2_conic_sections_parabolas_graphing_and_properties`, `a2_conic_sections_systems_of_quadratic_equations`
`a2_direct_and_inverse_variation_direct_and_inverse_variation`, `a2_equations_and_inequalities_absolute_value_equations`, `a2_equations_and_inequalities_absolute_value_inequalities`, `a2_equations_and_inequalities_compound_inequalities`, `a2_equations_and_inequalities_distance_rate_time_word_problems`, `a2_equations_and_inequalities_multi_step_equations`, `a2_equations_and_inequalities_multi_step_inequalities`, `a2_equations_and_inequalities_work_word_problems`
`a2_exponential_and_logarithmic_expressions_continuous_exponential_growth_and_decay_word_problems`, `a2_exponential_and_logarithmic_expressions_discrete_exponential_growth_and_decay_word_problems`, `a2_exponential_and_logarithmic_expressions_evaluating_logarithms`, `a2_exponential_and_logarithmic_expressions_exponential_equations_requiring_logarithms`, `a2_exponential_and_logarithmic_expressions_exponents_and_logarithms`, `a2_exponential_and_logarithmic_expressions_graphing_exponential_functions`, `a2_exponential_and_logarithmic_expressions_graphing_logarithmic_functions`, `a2_exponential_and_logarithmic_expressions_inverses_of_exponential_and_logarithmic_functions`
`a2_exponential_and_logarithmic_expressions_logarithmic_equations_simple`, `a2_exponential_and_logarithmic_expressions_logarithms_and_exponents_as_inverses`, `a2_general_functions_evaluating`, `a2_general_functions_inverses`, `a2_general_functions_operations`, `a2_linear_relations_and_functions_graphing_absolute_value_equations`, `a2_linear_relations_and_functions_graphing_linear_equations`, `a2_linear_relations_and_functions_graphing_linear_inequalities`
`a2_matrices_cramers_rule`, `a2_matrices_geometric_transformations`, `a2_matrices_operations`, `a2_polynomial_functions_adding_and_subtracting`, `a2_polynomial_functions_conjugate_roots_and_factoring`, `a2_polynomial_functions_descartes_rule_of_signs`, `a2_polynomial_functions_dividing`, `a2_polynomial_functions_end_behavior_and_general_graph_shape`
`a2_polynomial_functions_factoring_all_techniques`, `a2_polynomial_functions_factoring_by_grouping`, `a2_polynomial_functions_factoring_quadratic_form`, `a2_polynomial_functions_factoring_sum_difference_of_cubes`, `a2_polynomial_functions_graphing`, `a2_polynomial_functions_multiplying`, `a2_polynomial_functions_multiplying_special_cases`, `a2_polynomial_functions_naming`
`a2_polynomial_functions_solving_polynomial_equations`, `a2_polynomial_functions_the_remainder_theorem`, `a2_probability_and_statistics_probability_of_independent_and_dependent_events`, `a2_probability_and_statistics_probability_of_independent_and_dependent_events_word_problems`, `a2_probability_and_statistics_probability_of_mutually_exclusive_events`, `a2_probability_and_statistics_probability_of_mutually_exclusive_events_word_problems`, `a2_probability_and_statistics_sample_spaces_and_the_fundamental_counting_principle`, `a2_quadratic_functions_and_inequalities_completing_the_square`
`a2_quadratic_functions_and_inequalities_factoring_quadratic_expressions`, `a2_quadratic_functions_and_inequalities_factoring_special_case_quadratic_expressions`, `a2_quadratic_functions_and_inequalities_graphing_quadratic_functions`, `a2_quadratic_functions_and_inequalities_graphing_quadratic_inequalities`, `a2_quadratic_functions_and_inequalities_solving_equations_by_completing_the_square`, `a2_quadratic_functions_and_inequalities_solving_equations_by_factoring`, `a2_quadratic_functions_and_inequalities_solving_equations_by_graphing`, `a2_quadratic_functions_and_inequalities_solving_equations_by_taking_square_roots`
`a2_quadratic_functions_and_inequalities_solving_equations_with_the_quadratic_formula`, `a2_quadratic_functions_and_inequalities_the_discriminant`, `a2_relations_and_introduction_to_functions_continuous_relations`, `a2_relations_and_introduction_to_functions_discrete_relations`, `a2_systems_of_equations_and_inequalities_graphing_systems_of_linear_inequalities`, `a2_systems_of_equations_and_inequalities_planes`, `a2_systems_of_equations_and_inequalities_solving_systems_by_elimination_2_variables`, `a2_systems_of_equations_and_inequalities_solving_systems_by_graphing_2_variables`
`a2_systems_of_equations_and_inequalities_solving_systems_by_substitution_2_variables`, `a2_systems_of_equations_and_inequalities_solving_systems_with_three_variables`, `a2_trigonometry_angle_sum_difference_identities`, `a2_trigonometry_coterminal_angles`, `a2_trigonometry_double_angle_half_angle_identities`, `a2_trigonometry_equations`, `a2_trigonometry_graphing_trig_functions`, `a2_trigonometry_radians_and_degrees`
`a2_trigonometry_right_triangle_trig_angles_and_sides`, `a2_trigonometry_right_triangle_trig_finding_angle_measures`, `a2_trigonometry_right_triangle_trig_finding_ratios`

### calculus (39)

`calc_app_diff_intervals_of_increase_and_decrease`, `calc_app_diff_limits_in_form_of_definition_of_derivative`, `calc_app_diff_mean_value_theorem`, `calc_app_diff_rolles_theorem`, `calc_app_int_area_under_a_curve`, `calc_app_int_volume_by_cylinders`, `calc_app_int_volume_by_slicing_disks_and_washers`, `calc_app_int_volume_of_solids_with_known_cross_sections`
`calc_continuity_determining_and_classifying`, `calc_def_int_area_under_a_curve_by_limit_of_sums`, `calc_def_int_first_fundamental_theorem_of_calculus`, `calc_def_int_mean_value_theorem`, `calc_def_int_riemann_sum_tables`, `calc_def_int_second_fundamental_theorem_of_calculus`, `calc_def_int_substitution_with_change_of_variables`, `calc_diff_average_rates_of_change`
`calc_diff_chain_rule`, `calc_diff_definition_of_the_derivative`, `calc_diff_eq_exponential_growth_and_decay`, `calc_diff_eq_separable`, `calc_diff_eq_slope_fields`, `calc_diff_higher_order_derivatives`, `calc_diff_inverse_trigonometric`, `calc_diff_natural_logarithms_and_exponentials`
`calc_diff_other_base_logarithms_and_exponentials`, `calc_diff_power_rule`, `calc_diff_product_rule`, `calc_diff_quotient_rule`, `calc_diff_rules_using_tables`, `calc_diff_trigonometric`, `calc_indef_int_integration_by_parts`, `calc_indef_int_inverse_trigonometric`
`calc_indef_int_logarithmic_rule_and_exponentials`, `calc_indef_int_power_rule`, `calc_indef_int_power_rule_with_substitution`, `calc_indef_int_trigonometric`, `calc_limits_at_infinity`, `calc_limits_at_jump_discontinuities_and_kinks`, `calc_limits_by_direct_evaluation`

### geometry_review (4)

`geo_review_adding_and_subtracting_square_roots`, `geo_review_dividing_square_roots`, `geo_review_multi_step_equations`, `geo_review_multiplying_square_roots`

### geometry_sample (16)

`geo_circles_arcs_and_chords`, `geo_circles_inscribed_angles`, `geo_circles_tangents`, `geo_congruent_proving_triangles_congruent`, `geo_congruent_triangle_angle_sum`, `geo_constructions_circles`, `geo_quadrilaterals_classifying`, `geo_quadrilaterals_polygon_basics`
`geo_right_multi_step_pythagorean_theorem_problems`, `geo_right_pythagorean_theorem`, `geo_similar_solids`, `geo_similarity_similar_right_triangles`, `geo_similarity_similar_triangles`, `geo_trig_finding_trig_ratios`, `geo_trig_multi_step_trig_problems`, `geo_trig_solving_right_triangles`

### grade6_sample (10)

`g6_converting_units`, `g6_decimal_multiplication_with_equivalent_fractions`, `g6_dividing_fractions`, `g6_dividing_whole_numbers_by_decimals`, `g6_how_many_groups_times`, `g6_introduction_to_percents`, `g6_introduction_to_ratios`, `g6_part_part_whole_ratios`
`g6_solving_percent_problems_with_formulas`, `g6_unit_rates_and_equivalent_rates`

### prealgebra_sample (12)

`pa_converting_fractions_and_decimals`, `pa_equations_one_step_word_problems`, `pa_fractions_decimals_and_percents`, `pa_integers_adding_and_subtracting`, `pa_integers_dividing`, `pa_integers_multiplying`, `pa_least_common_multiple`, `pa_multi_step_inequalities`
`pa_naming_decimal_places_and_rounding`, `pa_proportions_word_problems`, `pa_simplifying_fractions`, `pa_writing_numbers_with_words`

### precalculus (38)

`pc_area_under_a_curve_by_limit_of_sums`, `pc_complex_numbers_in_polar_form`, `pc_definition_of_the_derivative`, `pc_dividing_polynomial_functions`, `pc_equations_and_multiple_angle_identities`, `pc_equations_with_factoring_and_fundamental_identities`, `pc_exponential_equations_requiring_logarithms`, `pc_exponents_and_logarithms`
`pc_functions_operations`, `pc_fundamental_identities`, `pc_graphing_exponential_functions`, `pc_graphing_logarithmic_functions`, `pc_graphing_trig_functions`, `pc_graphs_of_polar_equations`, `pc_indefinite_integrals`, `pc_inverse_trig_functions`
`pc_limits_at_infinity`, `pc_limits_by_direct_evaluation`, `pc_logarithmic_equations_simple`, `pc_logarithms_and_exponents_as_inverses`, `pc_multiple_angle_identities`, `pc_parabolas_graphing_and_properties`, `pc_polar_and_rectangular_forms_of_equations`, `pc_polar_forms_of_conic_sections`
`pc_polynomial_graphs_real_zeros_and_end_behavior`, `pc_power_rule_for_differentiation`, `pc_probability_mutually_exclusive`, `pc_probability_mutually_exclusive_word_problems`, `pc_probability_with_permutations_and_combinations`, `pc_radians_and_degrees`, `pc_remainder_theorem_and_bounds_of_real_zeros`, `pc_right_triangle_trig_finding_angles_and_sides`
`pc_right_triangle_trig_finding_ratios`, `pc_rotations_of_conic_sections`, `pc_simple_trig_equations`, `pc_sum_and_difference_identities`, `pc_trig_functions_of_any_angle`, `pc_vectors_basics`

### radical_rational (19)

`a2_polynomial_functions_rational_zero_root_theorem`, `a2_radical_functions_and_rational_exponents_adding_and_subtracting_radical_expressions`, `a2_radical_functions_and_rational_exponents_connecting_radical_expressions_and_rational_exponents`, `a2_radical_functions_and_rational_exponents_dividing_radical_expressions`, `a2_radical_functions_and_rational_exponents_domain_and_range_of_radical_functions`, `a2_radical_functions_and_rational_exponents_evaluating_rational_exponent_expressions`, `a2_radical_functions_and_rational_exponents_graphing_radical_equations`, `a2_radical_functions_and_rational_exponents_multiplying_radical_expressions`
`a2_radical_functions_and_rational_exponents_radical_equations`, `a2_radical_functions_and_rational_exponents_rational_exponent_equations`, `a2_radical_functions_and_rational_exponents_the_properties_of_exponents`, `a2_rational_expressions_adding_and_subtracting`, `a2_rational_expressions_complex_fractions`, `a2_rational_expressions_equations`, `a2_rational_expressions_graphing`, `a2_rational_expressions_multiplying_and_dividing`
`a2_rational_expressions_simplifying`, `pc_graphs_of_rational_functions`, `pc_rational_equations`

## Method

1. Collect Ready = catalog entries with non-scaffold generator, not `type_not_ready`, registered in `QUESTION_TYPES`.
2. Stratify: all A1 + all radical/rational + recently fixed + all A2/PC/Calc Ready + geo/G6/PA samples.
3. Generate E/M/H × 3; assert non-empty prompts/answers; stub detection; topic keyword rules; Easy≠Hard normalized templates; known miswire heuristics.
4. Soft weak-diversity → NOTE only.

## Fixes applied in this pass

- `calc_app_diff_newtons_method`: varied `f`/`x0` by tier (was hardcoded `x^2-2` from `x_0=1`).
- `calc_diff_eq_introduction`: varied DE coefficient; hard uses `y=Cx^k` (was always `y=Ce^{2x}`).
- `graphing_trig_functions` (A2/PC): Easy parents, Medium amplitude, Hard amplitude+period(+phase) (was ±sin/±cos only at every tier).
- `_int_bounds` duplicate overwrite in `frameworks/number.py`: removed second definition that broke `lo_default`/`hi_default` (absolute value / ordering).
- `geo_circles_arcs_and_chords` / `geo_circles_tangents`: tiered prompts (were single fixed flashcards).
- `geo_congruent_proving_triangles_congruent`: SSS/SAS/ASA/AAS/HL by tier (was always SSS).
- `geo_constructions_circles`: tiered construction prompts (was a single fixed identify-the-construction card).
- Soft deferred: diagram/graph types with fixed prompt text but differing answers; thin `precalc_foundations` / `calculus_foundations` fallbacks (not stub prompts when topic-routed).
