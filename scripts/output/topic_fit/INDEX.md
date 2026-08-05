# Topic-fit galleries INDEX

Generated: `2026-07-29 06:22 UTC`

Topic labels use a short **course prefix** + human name (`g6: ...`, `pa: ...`, `a1: ...`, `ge: ...`, `a2: ...`, `pc: ...`, `c1`/`c2`/`c3: ...`). See [`lib/topic-labels.ts`](../../../lib/topic-labels.ts) / [`question_engine/topic_labels.py`](../../../question_engine/topic_labels.py). Internal `type_id`s are unchanged.

All **by_topic** samples use the **live continuous-D generate API path** (`QUESTION_TYPES` → `_generate_for_type` → presets / annotation), same as WorksheetGenerator. Open any **gallery.html** in a browser (KaTeX). Cursor markdown preview does not render `$...$` math.

## How to open

```powershell
# From repo root — example
start scripts/output/topic_fit/INDEX.md
start scripts/output/topic_fit/by_topic/g6_decimal_addition/gallery.html
start scripts/output/topic_fit/by_topic/a1_coin_word_problems/gallery.html
start scripts/output/topic_fit/ooo_audit/gallery.html
```

## Regenerate

```powershell
$env:PYTHONPATH='.'
python scripts/build_verified_topic_galleries.py --course all --force-live
python scripts/build_verified_topic_galleries.py --course pa --include-second-tranche --force-live
python scripts/build_verified_topic_galleries.py --course a1 --force-live
python scripts/build_verified_topic_galleries.py --include-ooo
python scripts/build_verified_topic_galleries.py --only-ooo
python scripts/build_layer1_primitive_audits.py  # refreshes ooo_audit via live path
python scripts/render_topic_fit_gallery_html.py --all-missing
python scripts/relabel_topic_fit_galleries.py  # titles/h1 + INDEX only
```

## Summary

| Existing HTML galleries (indexed) | 249 |
| by_topic galleries written this run | 0 |
| OOO skipped this run | 0 |
| Failures this run | 0 |

## Done vs remaining

- G6 weak/failed ramp topics (6) — not gallery-verified until fixed (see g6_difficulty/TRACKING.md).
- PA galleries cover first + second tranche (33). Remaining PA: extend_primitive / hard geo / blocked markup (see pa_difficulty/TRACKING.md).
- A1 continuous effort — `73`/`73` by_topic galleries (a1_export_types.json scorers); refresh via `--course a1`. Family audit folders remain for deeper reviews.
- OOO by_topic + `ooo_audit` use the same live continuous-D path (`_generate_for_type`); refresh via `--only-ooo` / layer1 script.
- Full refresh: `python scripts/build_verified_topic_galleries.py --course all --force-live` (g6+pa verified; add `--course a1` and/or `--include-second-tranche` / `--include-ooo` as needed).
- Dated one-off folders (`20260713T…`) skipped from INDEX.

## Per-topic continuous galleries (`by_topic/`)

| Topic | HTML |
|-------|------|
| a1: Absolute value equations | [by_topic/a1_absolute_value_equations/gallery.html](by_topic/a1_absolute_value_equations/gallery.html) |
| a1: Absolute value inequalities | [by_topic/a1_absolute_value_inequalities/gallery.html](by_topic/a1_absolute_value_inequalities/gallery.html) |
| a1: Age word problems | [by_topic/a1_age_word_problems/gallery.html](by_topic/a1_age_word_problems/gallery.html) |
| a1: Coin word problems | [by_topic/a1_coin_word_problems/gallery.html](by_topic/a1_coin_word_problems/gallery.html) |
| a1: Compound inequalities | [by_topic/a1_compound_inequalities/gallery.html](by_topic/a1_compound_inequalities/gallery.html) |
| a1: Consecutive integers word problems | [by_topic/a1_consecutive_integers_word_problems/gallery.html](by_topic/a1_consecutive_integers_word_problems/gallery.html) |
| a1: Distance, rate, time word problems | [by_topic/a1_distance_rate_time_word_problems/gallery.html](by_topic/a1_distance_rate_time_word_problems/gallery.html) |
| a1: The Distributive Property | [by_topic/a1_distributive_property/gallery.html](by_topic/a1_distributive_property/gallery.html) |
| a1: Evaluating and graphing functions | [by_topic/a1_evaluating_graphing_functions/gallery.html](by_topic/a1_evaluating_graphing_functions/gallery.html) |
| a1: Graphing absolute value equations | [by_topic/a1_graphing_absolute_value_equations/gallery.html](by_topic/a1_graphing_absolute_value_equations/gallery.html) |
| a1: Graphing exponential functions | [by_topic/a1_graphing_exponential_functions/gallery.html](by_topic/a1_graphing_exponential_functions/gallery.html) |
| a1: Graphing linear equations | [by_topic/a1_graphing_linear_equations/gallery.html](by_topic/a1_graphing_linear_equations/gallery.html) |
| a1: Graphing | [by_topic/a1_graphing_quadratic_functions/gallery.html](by_topic/a1_graphing_quadratic_functions/gallery.html) |
| a1: Graphing quadratic inequalities | [by_topic/a1_graphing_quadratic_inequalities/gallery.html](by_topic/a1_graphing_quadratic_inequalities/gallery.html) |
| a1: Graphing systems of inequalities | [by_topic/a1_graphing_systems_of_inequalities/gallery.html](by_topic/a1_graphing_systems_of_inequalities/gallery.html) |
| a1: Literal equations | [by_topic/a1_literal_equations/gallery.html](by_topic/a1_literal_equations/gallery.html) |
| a1: Mixture word problems | [by_topic/a1_mixture_word_problems/gallery.html](by_topic/a1_mixture_word_problems/gallery.html) |
| a1: More on slope | [by_topic/a1_more_on_slope/gallery.html](by_topic/a1_more_on_slope/gallery.html) |
| a1: Multi-step equations | [by_topic/a1_multi_step_equations/gallery.html](by_topic/a1_multi_step_equations/gallery.html) |
| a1: Multi-step inequalities | [by_topic/a1_multi_step_inequalities/gallery.html](by_topic/a1_multi_step_inequalities/gallery.html) |
| a1: One-step equations | [by_topic/a1_one_step_equations/gallery.html](by_topic/a1_one_step_equations/gallery.html) |
| a1: One-step inequalities | [by_topic/a1_one_step_inequalities/gallery.html](by_topic/a1_one_step_inequalities/gallery.html) |
| a1: Order of operations | [by_topic/a1_order_of_operations/gallery.html](by_topic/a1_order_of_operations/gallery.html) |
| a1: Percent of change | [by_topic/a1_percent_of_change/gallery.html](by_topic/a1_percent_of_change/gallery.html) |
| a1: Percent word problems | [by_topic/a1_percent_word_problems/gallery.html](by_topic/a1_percent_word_problems/gallery.html) |
| a1: Percents | [by_topic/a1_percents/gallery.html](by_topic/a1_percents/gallery.html) |
| a1: Adding and subtracting | [by_topic/a1_polynomial_add_subtract/gallery.html](by_topic/a1_polynomial_add_subtract/gallery.html) |
| a1: Common factor only | [by_topic/a1_polynomial_factoring_common_factor/gallery.html](by_topic/a1_polynomial_factoring_common_factor/gallery.html) |
| a1: General strategy | [by_topic/a1_polynomial_factoring_general_strategy/gallery.html](by_topic/a1_polynomial_factoring_general_strategy/gallery.html) |
| a1: By grouping | [by_topic/a1_polynomial_factoring_grouping/gallery.html](by_topic/a1_polynomial_factoring_grouping/gallery.html) |
| a1: Special cases | [by_topic/a1_polynomial_factoring_special_cases/gallery.html](by_topic/a1_polynomial_factoring_special_cases/gallery.html) |
| a1: Dividing | [by_topic/a1_polynomial_long_division/gallery.html](by_topic/a1_polynomial_long_division/gallery.html) |
| a1: Multiplying | [by_topic/a1_polynomial_multiply/gallery.html](by_topic/a1_polynomial_multiply/gallery.html) |
| a1: Multiplying special cases | [by_topic/a1_polynomial_multiply_special/gallery.html](by_topic/a1_polynomial_multiply_special/gallery.html) |
| a1: Naming | [by_topic/a1_polynomial_naming/gallery.html](by_topic/a1_polynomial_naming/gallery.html) |
| a1: Properties of exponents | [by_topic/a1_properties_of_exponents/gallery.html](by_topic/a1_properties_of_exponents/gallery.html) |
| a1: Completing the square by finding the constant | [by_topic/a1_quadratic_completing_square_constant/gallery.html](by_topic/a1_quadratic_completing_square_constant/gallery.html) |
| a1: Solving equations by completing the square | [by_topic/a1_quadratic_completing_square_solve/gallery.html](by_topic/a1_quadratic_completing_square_solve/gallery.html) |
| a1: Understanding the discriminant | [by_topic/a1_quadratic_discriminant/gallery.html](by_topic/a1_quadratic_discriminant/gallery.html) |
| a1: Quadratic expressions | [by_topic/a1_quadratic_factoring/gallery.html](by_topic/a1_quadratic_factoring/gallery.html) |
| a1: Solving equations by factoring | [by_topic/a1_quadratic_factoring_equations/gallery.html](by_topic/a1_quadratic_factoring_equations/gallery.html) |
| a1: Solving equations with the Quadratic Formula | [by_topic/a1_quadratic_formula/gallery.html](by_topic/a1_quadratic_formula/gallery.html) |
| a1: Solving equations by graphing | [by_topic/a1_quadratic_solve_by_graphing/gallery.html](by_topic/a1_quadratic_solve_by_graphing/gallery.html) |
| a1: Solving equations by taking square roots | [by_topic/a1_quadratic_square_roots/gallery.html](by_topic/a1_quadratic_square_roots/gallery.html) |
| a1: Adding and subtracting | [by_topic/a1_radical_add_subtract/gallery.html](by_topic/a1_radical_add_subtract/gallery.html) |
| a1: Dividing | [by_topic/a1_radical_divide/gallery.html](by_topic/a1_radical_divide/gallery.html) |
| a1: Equations | [by_topic/a1_radical_equations/gallery.html](by_topic/a1_radical_equations/gallery.html) |
| a1: Multiplying | [by_topic/a1_radical_multiply/gallery.html](by_topic/a1_radical_multiply/gallery.html) |
| a1: Simplifying single radicals | [by_topic/a1_radical_simplification/gallery.html](by_topic/a1_radical_simplification/gallery.html) |
| a1: Adding and subtracting rational numbers | [by_topic/a1_rational_add_subtract/gallery.html](by_topic/a1_rational_add_subtract/gallery.html) |
| a1: Dividing rational numbers | [by_topic/a1_rational_divide/gallery.html](by_topic/a1_rational_divide/gallery.html) |
| a1: Multiplying and dividing rational expressions | [by_topic/a1_rational_expression_multiply_divide/gallery.html](by_topic/a1_rational_expression_multiply_divide/gallery.html) |
| a1: Adding and subtracting rational expressions | [by_topic/a1_rational_expression_simplification/gallery.html](by_topic/a1_rational_expression_simplification/gallery.html) |
| a1: Rational equations | [by_topic/a1_rational_expressions_equations/gallery.html](by_topic/a1_rational_expressions_equations/gallery.html) |
| a1: Multiplying rational numbers | [by_topic/a1_rational_multiply/gallery.html](by_topic/a1_rational_multiply/gallery.html) |
| a1: Simplifying and excluded values | [by_topic/a1_rational_simplification/gallery.html](by_topic/a1_rational_simplification/gallery.html) |
| a1: Scatter plots | [by_topic/a1_scatter_plots/gallery.html](by_topic/a1_scatter_plots/gallery.html) |
| a1: Addition/Subtraction and scientific notation | [by_topic/a1_scientific_notation_add_subtract/gallery.html](by_topic/a1_scientific_notation_add_subtract/gallery.html) |
| a1: Operations and scientific notation | [by_topic/a1_scientific_notation_operations/gallery.html](by_topic/a1_scientific_notation_operations/gallery.html) |
| a1: Writing scientific notation | [by_topic/a1_scientific_notation_write/gallery.html](by_topic/a1_scientific_notation_write/gallery.html) |
| a1: Simplifying polynomials | [by_topic/a1_simplify_polynomials/gallery.html](by_topic/a1_simplify_polynomials/gallery.html) |
| a1: Slope | [by_topic/a1_slope/gallery.html](by_topic/a1_slope/gallery.html) |
| a1: Solving proportions | [by_topic/a1_solving_proportions/gallery.html](by_topic/a1_solving_proportions/gallery.html) |
| a1: Solving by elimination | [by_topic/a1_systems_elimination/gallery.html](by_topic/a1_systems_elimination/gallery.html) |
| a1: Solving by graphing | [by_topic/a1_systems_graphing/gallery.html](by_topic/a1_systems_graphing/gallery.html) |
| a1: Solving by substitution | [by_topic/a1_systems_substitution/gallery.html](by_topic/a1_systems_substitution/gallery.html) |
| a1: Word problems | [by_topic/a1_systems_word_problems/gallery.html](by_topic/a1_systems_word_problems/gallery.html) |
| a1: Two-step equations | [by_topic/a1_two_step_equations/gallery.html](by_topic/a1_two_step_equations/gallery.html) |
| a1: Two-step inequalities | [by_topic/a1_two_step_inequalities/gallery.html](by_topic/a1_two_step_inequalities/gallery.html) |
| a1: Verbal expressions | [by_topic/a1_verbal_expressions/gallery.html](by_topic/a1_verbal_expressions/gallery.html) |
| a1: Visualizing data | [by_topic/a1_visualizing_data/gallery.html](by_topic/a1_visualizing_data/gallery.html) |
| a1: Work word problems | [by_topic/a1_work_word_problems/gallery.html](by_topic/a1_work_word_problems/gallery.html) |
| a1: Writing linear equations | [by_topic/a1_writing_linear_equations/gallery.html](by_topic/a1_writing_linear_equations/gallery.html) |
| g6: Absolute values | [by_topic/g6_absolute_values/gallery.html](by_topic/g6_absolute_values/gallery.html) |
| g6: Classifying and naming | [by_topic/g6_classifying_and_naming/gallery.html](by_topic/g6_classifying_and_naming/gallery.html) |
| g6: Combining like terms | [by_topic/g6_combining_like_terms/gallery.html](by_topic/g6_combining_like_terms/gallery.html) |
| g6: Comparing numbers | [by_topic/g6_comparing_numbers/gallery.html](by_topic/g6_comparing_numbers/gallery.html) |
| g6: Comparing rates | [by_topic/g6_comparing_rates/gallery.html](by_topic/g6_comparing_rates/gallery.html) |
| g6: Comparing ratios | [by_topic/g6_comparing_ratios/gallery.html](by_topic/g6_comparing_ratios/gallery.html) |
| g6: Comparing with absolute values | [by_topic/g6_comparing_with_absolute_values/gallery.html](by_topic/g6_comparing_with_absolute_values/gallery.html) |
| g6: Constant rate equations | [by_topic/g6_constant_rate_equations/gallery.html](by_topic/g6_constant_rate_equations/gallery.html) |
| g6: Converting units | [by_topic/g6_converting_units/gallery.html](by_topic/g6_converting_units/gallery.html) |
| g6: Center and spread | [by_topic/g6_data_center_and_spread/gallery.html](by_topic/g6_data_center_and_spread/gallery.html) |
| g6: Decimal addition | [by_topic/g6_decimal_addition/gallery.html](by_topic/g6_decimal_addition/gallery.html) |
| g6: Decimal multiplication | [by_topic/g6_decimal_multiplication/gallery.html](by_topic/g6_decimal_multiplication/gallery.html) |
| g6: Decimal multiplication with equivalent fractions | [by_topic/g6_decimal_multiplication_with_equivalent_fractions/gallery.html](by_topic/g6_decimal_multiplication_with_equivalent_fractions/gallery.html) |
| g6: Decimal subtraction | [by_topic/g6_decimal_subtraction/gallery.html](by_topic/g6_decimal_subtraction/gallery.html) |
| g6: Distributive property, algebraic | [by_topic/g6_distributive_property_algebraic/gallery.html](by_topic/g6_distributive_property_algebraic/gallery.html) |
| g6: Distributive property with area diagrams, algebraic | [by_topic/g6_distributive_property_area_diagrams_algebraic/gallery.html](by_topic/g6_distributive_property_area_diagrams_algebraic/gallery.html) |
| g6: Distributive property, numeric | [by_topic/g6_distributive_property_numeric/gallery.html](by_topic/g6_distributive_property_numeric/gallery.html) |
| g6: Dividing decimals by decimals | [by_topic/g6_dividing_decimals_by_decimals/gallery.html](by_topic/g6_dividing_decimals_by_decimals/gallery.html) |
| g6: Dividing decimals by whole numbers | [by_topic/g6_dividing_decimals_by_whole_numbers/gallery.html](by_topic/g6_dividing_decimals_by_whole_numbers/gallery.html) |
| g6: Dividing fractions | [by_topic/g6_dividing_fractions/gallery.html](by_topic/g6_dividing_fractions/gallery.html) |
| g6: Dividing whole numbers by decimals | [by_topic/g6_dividing_whole_numbers_by_decimals/gallery.html](by_topic/g6_dividing_whole_numbers_by_decimals/gallery.html) |
| g6: Dividing whole numbers that result in decimals | [by_topic/g6_dividing_whole_numbers_that_result_in_decimals/gallery.html](by_topic/g6_dividing_whole_numbers_that_result_in_decimals/gallery.html) |
| g6: Drawing dot plots | [by_topic/g6_drawing_dot_plots/gallery.html](by_topic/g6_drawing_dot_plots/gallery.html) |
| g6: Drawing histograms | [by_topic/g6_drawing_histograms/gallery.html](by_topic/g6_drawing_histograms/gallery.html) |
| g6: Equations for other relationships | [by_topic/g6_equations_for_other_relationships/gallery.html](by_topic/g6_equations_for_other_relationships/gallery.html) |
| g6: Hanger diagrams | [by_topic/g6_equations_hanger_diagrams/gallery.html](by_topic/g6_equations_hanger_diagrams/gallery.html) |
| g6: Tape diagrams | [by_topic/g6_equations_tape_diagrams/gallery.html](by_topic/g6_equations_tape_diagrams/gallery.html) |
| g6: Equations word problems | [by_topic/g6_equations_word_problems/gallery.html](by_topic/g6_equations_word_problems/gallery.html) |
| g6: Equivalent ratio equations | [by_topic/g6_equivalent_ratio_equations/gallery.html](by_topic/g6_equivalent_ratio_equations/gallery.html) |
| g6: Equivalent ratios | [by_topic/g6_equivalent_ratios/gallery.html](by_topic/g6_equivalent_ratios/gallery.html) |
| g6: Evaluating linear expressions | [by_topic/g6_evaluating_algebraic_expressions/gallery.html](by_topic/g6_evaluating_algebraic_expressions/gallery.html) |
| g6: Factoring | [by_topic/g6_factoring/gallery.html](by_topic/g6_factoring/gallery.html) |
| g6: Finding percents with equivalent fractions | [by_topic/g6_finding_percents_with_equivalent_fractions/gallery.html](by_topic/g6_finding_percents_with_equivalent_fractions/gallery.html) |
| g6: Formulas for volume and surface area of a cube | [by_topic/g6_formulas_for_volume_and_surface_area_of_a_cube/gallery.html](by_topic/g6_formulas_for_volume_and_surface_area_of_a_cube/gallery.html) |
| g6: GCF and LCM word problems | [by_topic/g6_gcf_and_lcm_word_problems/gallery.html](by_topic/g6_gcf_and_lcm_word_problems/gallery.html) |
| g6: Greatest common factor | [by_topic/g6_greatest_common_factor/gallery.html](by_topic/g6_greatest_common_factor/gallery.html) |
| g6: Hanger diagrams | [by_topic/g6_inequalities_hanger_diagrams/gallery.html](by_topic/g6_inequalities_hanger_diagrams/gallery.html) |
| g6: Inequalities word problems | [by_topic/g6_inequalities_word_problems/gallery.html](by_topic/g6_inequalities_word_problems/gallery.html) |
| g6: Interpreting box plots | [by_topic/g6_interpreting_box_plots/gallery.html](by_topic/g6_interpreting_box_plots/gallery.html) |
| g6: Interpreting dot plots | [by_topic/g6_interpreting_dot_plots/gallery.html](by_topic/g6_interpreting_dot_plots/gallery.html) |
| g6: Interpreting histograms | [by_topic/g6_interpreting_histograms/gallery.html](by_topic/g6_interpreting_histograms/gallery.html) |
| g6: Introduction to percents | [by_topic/g6_introduction_to_percents/gallery.html](by_topic/g6_introduction_to_percents/gallery.html) |
| g6: Introduction to ratios | [by_topic/g6_introduction_to_ratios/gallery.html](by_topic/g6_introduction_to_ratios/gallery.html) |
| g6: Kites | [by_topic/g6_kites/gallery.html](by_topic/g6_kites/gallery.html) |
| g6: Least common multiple | [by_topic/g6_least_common_multiple/gallery.html](by_topic/g6_least_common_multiple/gallery.html) |
| g6: Long division with remainders | [by_topic/g6_long_division_with_remainders/gallery.html](by_topic/g6_long_division_with_remainders/gallery.html) |
| g6: Number line word problems | [by_topic/g6_number_line_word_problems/gallery.html](by_topic/g6_number_line_word_problems/gallery.html) |
| g6: Numbers on a number line | [by_topic/g6_numbers_on_a_number_line/gallery.html](by_topic/g6_numbers_on_a_number_line/gallery.html) |
| g6: Numeric expressions and the order of operations | [by_topic/g6_numeric_expressions_and_order_of_operations/gallery.html](by_topic/g6_numeric_expressions_and_order_of_operations/gallery.html) |
| g6: Numeric expressions with exponents | [by_topic/g6_numeric_expressions_with_exponents/gallery.html](by_topic/g6_numeric_expressions_with_exponents/gallery.html) |
| g6: Ordering numbers | [by_topic/g6_ordering_numbers/gallery.html](by_topic/g6_ordering_numbers/gallery.html) |
| g6: Ordering with absolute values | [by_topic/g6_ordering_with_absolute_values/gallery.html](by_topic/g6_ordering_with_absolute_values/gallery.html) |
| g6: Parallelograms | [by_topic/g6_parallelograms/gallery.html](by_topic/g6_parallelograms/gallery.html) |
| g6: Parallelograms, understanding area formula | [by_topic/g6_parallelograms_understanding_area_formula/gallery.html](by_topic/g6_parallelograms_understanding_area_formula/gallery.html) |
| g6: Part-part-whole ratios | [by_topic/g6_part_part_whole_ratios/gallery.html](by_topic/g6_part_part_whole_ratios/gallery.html) |
| g6: Polygons and shaded regions | [by_topic/g6_polygons_and_shaded_regions/gallery.html](by_topic/g6_polygons_and_shaded_regions/gallery.html) |
| g6: Polygons on a grid or coordinate plane | [by_topic/g6_polygons_on_a_grid_or_coordinate_plane/gallery.html](by_topic/g6_polygons_on_a_grid_or_coordinate_plane/gallery.html) |
| g6: Rectangles with fraction side lengths | [by_topic/g6_rectangles_with_fraction_side_lengths/gallery.html](by_topic/g6_rectangles_with_fraction_side_lengths/gallery.html) |
| g6: Relating percents, fractions, and decimals | [by_topic/g6_relating_percents_fractions_and_decimals/gallery.html](by_topic/g6_relating_percents_fractions_and_decimals/gallery.html) |
| g6: Right rectangular prisms with fraction side lengths | [by_topic/g6_right_rectangular_prisms_with_fraction_side_lengths/gallery.html](by_topic/g6_right_rectangular_prisms_with_fraction_side_lengths/gallery.html) |
| g6: Solutions to equations | [by_topic/g6_solutions_to_equations/gallery.html](by_topic/g6_solutions_to_equations/gallery.html) |
| g6: Solutions to inequalities | [by_topic/g6_solutions_to_inequalities/gallery.html](by_topic/g6_solutions_to_inequalities/gallery.html) |
| g6: Solving and graphing one-step inequalities | [by_topic/g6_solving_and_graphing_one_step_inequalities/gallery.html](by_topic/g6_solving_and_graphing_one_step_inequalities/gallery.html) |
| g6: Solving percent problems with formulas | [by_topic/g6_solving_percent_problems_with_formulas/gallery.html](by_topic/g6_solving_percent_problems_with_formulas/gallery.html) |
| g6: Trapezoids | [by_topic/g6_trapezoids/gallery.html](by_topic/g6_trapezoids/gallery.html) |
| g6: Triangles | [by_topic/g6_triangles/gallery.html](by_topic/g6_triangles/gallery.html) |
| g6: Triangles, understanding area formula | [by_topic/g6_triangles_understanding_area_formula/gallery.html](by_topic/g6_triangles_understanding_area_formula/gallery.html) |
| g6: Triangles with fraction side lengths | [by_topic/g6_triangles_with_fraction_side_lengths/gallery.html](by_topic/g6_triangles_with_fraction_side_lengths/gallery.html) |
| g6: Unit rates and equivalent rates | [by_topic/g6_unit_rates_and_equivalent_rates/gallery.html](by_topic/g6_unit_rates_and_equivalent_rates/gallery.html) |
| g6: Volume and surface area using isometric drawings | [by_topic/g6_volume_and_surface_area_using_isometric_drawings/gallery.html](by_topic/g6_volume_and_surface_area_using_isometric_drawings/gallery.html) |
| g6: Writing algebraic expressions | [by_topic/g6_writing_algebraic_expressions/gallery.html](by_topic/g6_writing_algebraic_expressions/gallery.html) |
| g6: Writing and graphing inequalities | [by_topic/g6_writing_and_graphing_inequalities/gallery.html](by_topic/g6_writing_and_graphing_inequalities/gallery.html) |
| g6: Writing numeric expressions | [by_topic/g6_writing_numeric_expressions/gallery.html](by_topic/g6_writing_numeric_expressions/gallery.html) |
| pa: Checking for a proportion | [by_topic/pa_checking_for_a_proportion/gallery.html](by_topic/pa_checking_for_a_proportion/gallery.html) |
| pa: Converting fractions and decimals | [by_topic/pa_converting_fractions_and_decimals/gallery.html](by_topic/pa_converting_fractions_and_decimals/gallery.html) |
| pa: Multi-step equations | [by_topic/pa_equations_multi_step_equations/gallery.html](by_topic/pa_equations_multi_step_equations/gallery.html) |
| pa: One-step equations, word problems | [by_topic/pa_equations_one_step_word_problems/gallery.html](by_topic/pa_equations_one_step_word_problems/gallery.html) |
| pa: Two-step equations word problems | [by_topic/pa_equations_two_step_word_problems/gallery.html](by_topic/pa_equations_two_step_word_problems/gallery.html) |
| pa: Factoring | [by_topic/pa_factoring/gallery.html](by_topic/pa_factoring/gallery.html) |
| pa: Adding fractions (like denominators) | [by_topic/pa_fractions_add_like/gallery.html](by_topic/pa_fractions_add_like/gallery.html) |
| pa: Adding fractions (unlike denominators) | [by_topic/pa_fractions_add_unlike/gallery.html](by_topic/pa_fractions_add_unlike/gallery.html) |
| pa: Fractions, decimals, and percents | [by_topic/pa_fractions_decimals_and_percents/gallery.html](by_topic/pa_fractions_decimals_and_percents/gallery.html) |
| pa: Dividing fractions | [by_topic/pa_fractions_divide/gallery.html](by_topic/pa_fractions_divide/gallery.html) |
| pa: Multiplying fractions | [by_topic/pa_fractions_multiply/gallery.html](by_topic/pa_fractions_multiply/gallery.html) |
| pa: Subtracting fractions (like denominators) | [by_topic/pa_fractions_subtract_like/gallery.html](by_topic/pa_fractions_subtract_like/gallery.html) |
| pa: Subtracting fractions (unlike denominators) | [by_topic/pa_fractions_subtract_unlike/gallery.html](by_topic/pa_fractions_subtract_unlike/gallery.html) |
| pa: Graphing systems of equations | [by_topic/pa_graphing_systems_of_equations/gallery.html](by_topic/pa_graphing_systems_of_equations/gallery.html) |
| pa: Greatest common factor | [by_topic/pa_greatest_common_factor/gallery.html](by_topic/pa_greatest_common_factor/gallery.html) |
| pa: Adding and subtracting | [by_topic/pa_integers_adding_and_subtracting/gallery.html](by_topic/pa_integers_adding_and_subtracting/gallery.html) |
| pa: Dividing | [by_topic/pa_integers_dividing/gallery.html](by_topic/pa_integers_dividing/gallery.html) |
| pa: Multiplying | [by_topic/pa_integers_multiplying/gallery.html](by_topic/pa_integers_multiplying/gallery.html) |
| pa: Least common multiple | [by_topic/pa_least_common_multiple/gallery.html](by_topic/pa_least_common_multiple/gallery.html) |
| pa: Multi-step inequalities | [by_topic/pa_multi_step_inequalities/gallery.html](by_topic/pa_multi_step_inequalities/gallery.html) |
| pa: Naming decimal places and rounding | [by_topic/pa_naming_decimal_places_and_rounding/gallery.html](by_topic/pa_naming_decimal_places_and_rounding/gallery.html) |
| pa: Adding and subtracting | [by_topic/pa_polynomials_adding_and_subtracting/gallery.html](by_topic/pa_polynomials_adding_and_subtracting/gallery.html) |
| pa: Multiplying | [by_topic/pa_polynomials_multiplying/gallery.html](by_topic/pa_polynomials_multiplying/gallery.html) |
| pa: Simplifying | [by_topic/pa_polynomials_simplifying/gallery.html](by_topic/pa_polynomials_simplifying/gallery.html) |
| pa: Proportions word problems | [by_topic/pa_proportions_word_problems/gallery.html](by_topic/pa_proportions_word_problems/gallery.html) |
| pa: Simple and compound interest | [by_topic/pa_simple_and_compound_interest/gallery.html](by_topic/pa_simple_and_compound_interest/gallery.html) |
| pa: Simplifying fractions | [by_topic/pa_simplifying_fractions/gallery.html](by_topic/pa_simplifying_fractions/gallery.html) |
| pa: Slope | [by_topic/pa_slope/gallery.html](by_topic/pa_slope/gallery.html) |
| pa: Squares and square roots | [by_topic/pa_squares_and_square_roots/gallery.html](by_topic/pa_squares_and_square_roots/gallery.html) |
| pa: Solving systems of equations by substitution | [by_topic/pa_systems_substitution/gallery.html](by_topic/pa_systems_substitution/gallery.html) |
| pa: Systems of equations word problems | [by_topic/pa_systems_word_problems/gallery.html](by_topic/pa_systems_word_problems/gallery.html) |
| pa: Writing linear equations | [by_topic/pa_writing_linear_equations/gallery.html](by_topic/pa_writing_linear_equations/gallery.html) |
| pa: Writing numbers with words | [by_topic/pa_writing_numbers_with_words/gallery.html](by_topic/pa_writing_numbers_with_words/gallery.html) |

## Audit / family galleries

| Folder | HTML | Notes |
|--------|------|-------|
| `absolute_value_equations_audit` | [absolute_value_equations_audit/gallery.html](absolute_value_equations_audit/gallery.html) |  |
| `absolute_value_inequalities_audit` | [absolute_value_inequalities_audit/gallery.html](absolute_value_inequalities_audit/gallery.html) |  |
| `c1_calc_app_diff_differentials` | [c1_calc_app_diff_differentials/gallery.html](c1_calc_app_diff_differentials/gallery.html) |  |
| `c1_calc_app_diff_slope_tangent_and_normal_lines` | [c1_calc_app_diff_slope_tangent_and_normal_lines/gallery.html](c1_calc_app_diff_slope_tangent_and_normal_lines/gallery.html) |  |
| `c1_calc_diff_average_rates_of_change` | [c1_calc_diff_average_rates_of_change/gallery.html](c1_calc_diff_average_rates_of_change/gallery.html) |  |
| `c1_calc_diff_chain_rule` | [c1_calc_diff_chain_rule/gallery.html](c1_calc_diff_chain_rule/gallery.html) |  |
| `c1_calc_diff_definition_of_the_derivative` | [c1_calc_diff_definition_of_the_derivative/gallery.html](c1_calc_diff_definition_of_the_derivative/gallery.html) |  |
| `c1_calc_diff_higher_order_derivatives` | [c1_calc_diff_higher_order_derivatives/gallery.html](c1_calc_diff_higher_order_derivatives/gallery.html) |  |
| `c1_calc_diff_implicit` | [c1_calc_diff_implicit/gallery.html](c1_calc_diff_implicit/gallery.html) |  |
| `c1_calc_diff_instantaneous_rates_of_change` | [c1_calc_diff_instantaneous_rates_of_change/gallery.html](c1_calc_diff_instantaneous_rates_of_change/gallery.html) |  |
| `c1_calc_diff_inverse_functions` | [c1_calc_diff_inverse_functions/gallery.html](c1_calc_diff_inverse_functions/gallery.html) |  |
| `c1_calc_diff_inverse_trigonometric` | [c1_calc_diff_inverse_trigonometric/gallery.html](c1_calc_diff_inverse_trigonometric/gallery.html) |  |
| `c1_calc_diff_logarithmic` | [c1_calc_diff_logarithmic/gallery.html](c1_calc_diff_logarithmic/gallery.html) |  |
| `c1_calc_diff_natural_logarithms_and_exponentials` | [c1_calc_diff_natural_logarithms_and_exponentials/gallery.html](c1_calc_diff_natural_logarithms_and_exponentials/gallery.html) |  |
| `c1_calc_diff_other_base_logarithms_and_exponentials` | [c1_calc_diff_other_base_logarithms_and_exponentials/gallery.html](c1_calc_diff_other_base_logarithms_and_exponentials/gallery.html) |  |
| `c1_calc_diff_power_rule` | [c1_calc_diff_power_rule/gallery.html](c1_calc_diff_power_rule/gallery.html) |  |
| `c1_calc_diff_product_rule` | [c1_calc_diff_product_rule/gallery.html](c1_calc_diff_product_rule/gallery.html) |  |
| `c1_calc_diff_quotient_rule` | [c1_calc_diff_quotient_rule/gallery.html](c1_calc_diff_quotient_rule/gallery.html) |  |
| `c1_calc_diff_trigonometric` | [c1_calc_diff_trigonometric/gallery.html](c1_calc_diff_trigonometric/gallery.html) |  |
| `c1_calc_indef_int_logarithmic_rule_and_exponentials_with_substitution` | [c1_calc_indef_int_logarithmic_rule_and_exponentials_with_substitution/gallery.html](c1_calc_indef_int_logarithmic_rule_and_exponentials_with_substitution/gallery.html) |  |
| `c1_calculus_derivative_rules` | [c1_calculus_derivative_rules/gallery.html](c1_calculus_derivative_rules/gallery.html) |  |
| `c1_calculus_pilot` | [c1_calculus_pilot/gallery.html](c1_calculus_pilot/gallery.html) |  |
| `combine_like_terms_audit` | [combine_like_terms_audit/gallery.html](combine_like_terms_audit/gallery.html) |  |
| `combine_like_terms_linear_gate_audit` | [combine_like_terms_linear_gate_audit/gallery.html](combine_like_terms_linear_gate_audit/gallery.html) |  |
| `compound_inequalities_audit` | [compound_inequalities_audit/gallery.html](compound_inequalities_audit/gallery.html) |  |
| `constructive_expand_audit` | [constructive_expand_audit/gallery.html](constructive_expand_audit/gallery.html) |  |
| `constructive_ooo_audit` | [constructive_ooo_audit/gallery.html](constructive_ooo_audit/gallery.html) | OOO family audit |
| `constructive_pfd_audit` | [constructive_pfd_audit/gallery.html](constructive_pfd_audit/gallery.html) |  |
| `constructive_rational_audit` | [constructive_rational_audit/gallery.html](constructive_rational_audit/gallery.html) |  |
| `difficulty_sweep` | [difficulty_sweep/gallery.html](difficulty_sweep/gallery.html) |  |
| `equations_audit` | [equations_audit/gallery.html](equations_audit/gallery.html) |  |
| `evaluate_linear_expressions_audit` | [evaluate_linear_expressions_audit/gallery.html](evaluate_linear_expressions_audit/gallery.html) |  |
| `evaluate_polynomial_audit` | [evaluate_polynomial_audit/gallery.html](evaluate_polynomial_audit/gallery.html) |  |
| `expand_simplify_audit` | [expand_simplify_audit/gallery.html](expand_simplify_audit/gallery.html) |  |
| `factor_gcf_audit` | [factor_gcf_audit/gallery.html](factor_gcf_audit/gallery.html) |  |
| `factor_gcf_linear_policy_audit` | [factor_gcf_linear_policy_audit/gallery.html](factor_gcf_linear_policy_audit/gallery.html) |  |
| `factor_gcf_poly_policy_audit` | [factor_gcf_poly_policy_audit/gallery.html](factor_gcf_poly_policy_audit/gallery.html) |  |
| `g6_pa_continuous` | [g6_pa_continuous/gallery.html](g6_pa_continuous/gallery.html) |  |
| `graph_linear_audit` | [graph_linear_audit/gallery.html](graph_linear_audit/gallery.html) |  |
| `identify_property_verify` | [identify_property_verify/gallery.html](identify_property_verify/gallery.html) |  |
| `inequalities_audit` | [inequalities_audit/gallery.html](inequalities_audit/gallery.html) |  |
| `literal_equations_audit` | [literal_equations_audit/gallery.html](literal_equations_audit/gallery.html) |  |
| `multistep_equations_audit` | [multistep_equations_audit/gallery.html](multistep_equations_audit/gallery.html) |  |
| `multistep_inequalities_audit` | [multistep_inequalities_audit/gallery.html](multistep_inequalities_audit/gallery.html) |  |
| `number_profile_audit` | [number_profile_audit/gallery.html](number_profile_audit/gallery.html) |  |
| `ooo_audit` | [ooo_audit/gallery.html](ooo_audit/gallery.html) | OOO family audit |
| `poly_combine_like_terms_audit` | [poly_combine_like_terms_audit/gallery.html](poly_combine_like_terms_audit/gallery.html) |  |
| `poly_compose` | [poly_compose/gallery.html](poly_compose/gallery.html) |  |
| `poly_expand_simplify_audit` | [poly_expand_simplify_audit/gallery.html](poly_expand_simplify_audit/gallery.html) |  |
| `poly_quad_smoke` | [poly_quad_smoke/gallery.html](poly_quad_smoke/gallery.html) |  |
| `polynomial_add_subtract_audit` | [polynomial_add_subtract_audit/gallery.html](polynomial_add_subtract_audit/gallery.html) |  |
| `polynomial_factoring_grouping_audit` | [polynomial_factoring_grouping_audit/gallery.html](polynomial_factoring_grouping_audit/gallery.html) |  |
| `polynomial_factoring_special_audit` | [polynomial_factoring_special_audit/gallery.html](polynomial_factoring_special_audit/gallery.html) |  |
| `polynomial_multiply_audit` | [polynomial_multiply_audit/gallery.html](polynomial_multiply_audit/gallery.html) |  |
| `polynomial_multiply_special_audit` | [polynomial_multiply_special_audit/gallery.html](polynomial_multiply_special_audit/gallery.html) |  |
| `polynomial_naming_audit` | [polynomial_naming_audit/gallery.html](polynomial_naming_audit/gallery.html) |  |
| `proportions_audit` | [proportions_audit/gallery.html](proportions_audit/gallery.html) |  |
| `quadratic_factoring` | [quadratic_factoring/gallery.html](quadratic_factoring/gallery.html) |  |
| `quadratic_factoring_audit` | [quadratic_factoring_audit/gallery.html](quadratic_factoring_audit/gallery.html) |  |
| `slope_audit` | [slope_audit/gallery.html](slope_audit/gallery.html) |  |
| `systems_elim_audit` | [systems_elim_audit/gallery.html](systems_elim_audit/gallery.html) |  |
| `systems_graph_audit` | [systems_graph_audit/gallery.html](systems_graph_audit/gallery.html) |  |
| `systems_sub_audit` | [systems_sub_audit/gallery.html](systems_sub_audit/gallery.html) |  |
| `variable_lane_audit` | [variable_lane_audit/gallery.html](variable_lane_audit/gallery.html) |  |
| `word_problems_linear_audit` | [word_problems_linear_audit/gallery.html](word_problems_linear_audit/gallery.html) |  |
| `wp_systems_audit` | [wp_systems_audit/gallery.html](wp_systems_audit/gallery.html) |  |
| `writing_linear_equations_audit` | [writing_linear_equations_audit/gallery.html](writing_linear_equations_audit/gallery.html) |  |

## Nested galleries

- [number_profile_audit/lane_from_d/gallery.html](number_profile_audit/lane_from_d/gallery.html)
- [number_profile_audit/per_profile/gallery.html](number_profile_audit/per_profile/gallery.html)
- [variable_lane_audit/lane_from_d/gallery.html](variable_lane_audit/lane_from_d/gallery.html)

