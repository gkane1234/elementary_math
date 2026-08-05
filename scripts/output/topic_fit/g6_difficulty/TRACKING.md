# G6 continuous-difficulty TRACKING

**Branch:** `experiment/difficulty-slider`  
**Date:** 2026-07-27  
**Ready G6 topics:** 78  
**After SKIP first 11:** 67 remaining → batches 0–6

## Summary counts

| Status | Count |
|---|---|
| verified_ramp | 72 |
| weak_ramp | 2 |
| failed_ramp | 4 |
| blocked | 0 |
| **total** | **78** |

## Batch file status

| Batch | Remaining indices | Verification file | Status | Batch counts |
|---|---|---|---|---|
| 0 | [0, 10) | `batch_0_verification.json` | complete | verified_ramp=10 |
| 1 | [10, 20) | `batch_1_verification.json` | complete | verified_ramp=10, weak_ramp=0, failed_ramp=0, blocked=0 |
| 2 | [20, 30) | `batch_2_verification.json` | complete | verified_ramp=4, weak_ramp=2, failed_ramp=4 |
| 3 | [30, 40) | `batch_3_verification.json` | complete | verified_ramp=10, weak_ramp=0, failed_ramp=0, blocked=0 |
| 4 | [40, 50) | `batch_4_verification.json` | complete | verified_ramp=10, weak_ramp=0, failed_ramp=0, blocked=0 |
| 5 | [50, 60) | `batch_5_verification.json` | complete | verified_ramp=10 |
| 6 | [60, end) | `batch_6_verification.json` | complete | verified_ramp=7 |

## Prior pass (first 11 Ready)

All marked **verified_ramp** from `g6_difficulty_effort_specs.md` (means from `verification_summary.json`). Not overwritten by later batches.

- `g6_introduction_to_ratios`
- `g6_equivalent_ratios`
- `g6_part_part_whole_ratios`
- `g6_comparing_ratios`
- `g6_unit_rates_and_equivalent_rates`
- `g6_comparing_rates`
- `g6_converting_units`
- `g6_introduction_to_percents`
- `g6_relating_percents_fractions_and_decimals`
- `g6_finding_percents_with_equivalent_fractions`
- `g6_solving_percent_problems_with_formulas`

## Needs fix later

Every `weak_ramp`, `failed_ramp`, and `blocked` topic across batches 0–6 (none in prior_11). Fix these before treating the G6 difficulty ladder as done.

| type_id | name | batch | status | note |
|---|---|---|---|---|
| `g6_points_on_the_coordinate_plane` | Points on the coordinate plane | 2 | **weak_ramp** | effort is quadrant/grid-range only; no task-mode ladder |
| `g6_distances_on_the_coordinate_plane` | Distances on the coordinate plane | 2 | **failed_ramp** | axis_aligned_only locked True at all bands; effort is span/sign-crossing only |
| `g6_shapes_and_perimeter_on_the_coordinate_plane` | Shapes and perimeter on the coordinate plane | 2 | **failed_ramp** | allow_l_shape unlock blocked by setting_defaults (always rectangles; coord span flat) |
| `g6_coordinate_plane_distances_word_problems` | Distances, word problems | 2 | **failed_ramp** | continuous D ignored; always diagonal non-unit distances |
| `g6_properties_of_addition_and_multiplication` | Properties of addition and multiplication | 2 | **weak_ramp** | hard property rate weak (D0=0.0 -> D25=0.225) |
| `g6_distributive_property_numeric` | Distributive property, numeric | 2 | **failed_ramp** | G6 number lane wrong: negatives/fractions/decimals appear; presets allow_negative=False ignored by primitive |

## All Ready topics (curriculum order)

| # | type_id | name | batch | status |
|---|---|---|---|---|
| 0 | `g6_introduction_to_ratios` | Introduction to ratios | prior_11 | verified_ramp |
| 1 | `g6_equivalent_ratios` | Equivalent ratios | prior_11 | verified_ramp |
| 2 | `g6_part_part_whole_ratios` | Part-part-whole ratios | prior_11 | verified_ramp |
| 3 | `g6_comparing_ratios` | Comparing ratios | prior_11 | verified_ramp |
| 4 | `g6_unit_rates_and_equivalent_rates` | Unit rates and equivalent rates | prior_11 | verified_ramp |
| 5 | `g6_comparing_rates` | Comparing rates | prior_11 | verified_ramp |
| 6 | `g6_converting_units` | Converting units | prior_11 | verified_ramp |
| 7 | `g6_introduction_to_percents` | Introduction to percents | prior_11 | verified_ramp |
| 8 | `g6_relating_percents_fractions_and_decimals` | Relating percents, fractions, and decimals | prior_11 | verified_ramp |
| 9 | `g6_finding_percents_with_equivalent_fractions` | Finding percents with equivalent fractions | prior_11 | verified_ramp |
| 10 | `g6_solving_percent_problems_with_formulas` | Solving percent problems with formulas | prior_11 | verified_ramp |
| 11 | `g6_dividing_fractions` | Dividing fractions | 0 | verified_ramp |
| 12 | `g6_decimal_addition` | Decimal addition | 0 | verified_ramp |
| 13 | `g6_decimal_subtraction` | Decimal subtraction | 0 | verified_ramp |
| 14 | `g6_decimal_multiplication_with_equivalent_fractions` | Decimal multiplication with equivalent fractions | 0 | verified_ramp |
| 15 | `g6_decimal_multiplication` | Decimal multiplication | 0 | verified_ramp |
| 16 | `g6_long_division_with_remainders` | Long division with remainders | 0 | verified_ramp |
| 17 | `g6_dividing_whole_numbers_that_result_in_decimals` | Dividing whole numbers that result in decimals | 0 | verified_ramp |
| 18 | `g6_dividing_decimals_by_whole_numbers` | Dividing decimals by whole numbers | 0 | verified_ramp |
| 19 | `g6_dividing_whole_numbers_by_decimals` | Dividing whole numbers by decimals | 0 | verified_ramp |
| 20 | `g6_dividing_decimals_by_decimals` | Dividing decimals by decimals | 0 | verified_ramp |
| 21 | `g6_factoring` | Factoring | 1 | verified_ramp |
| 22 | `g6_greatest_common_factor` | Greatest common factor | 1 | verified_ramp |
| 23 | `g6_least_common_multiple` | Least common multiple | 1 | verified_ramp |
| 24 | `g6_gcf_and_lcm_word_problems` | GCF and LCM word problems | 1 | verified_ramp |
| 25 | `g6_numbers_on_a_number_line` | Numbers on a number line | 1 | verified_ramp |
| 26 | `g6_number_line_word_problems` | Number line word problems | 1 | verified_ramp |
| 27 | `g6_comparing_numbers` | Comparing numbers | 1 | verified_ramp |
| 28 | `g6_ordering_numbers` | Ordering numbers | 1 | verified_ramp |
| 29 | `g6_absolute_values` | Absolute values | 1 | verified_ramp |
| 30 | `g6_comparing_with_absolute_values` | Comparing with absolute values | 1 | verified_ramp |
| 31 | `g6_ordering_with_absolute_values` | Ordering with absolute values | 2 | verified_ramp |
| 32 | `g6_points_on_the_coordinate_plane` | Points on the coordinate plane | 2 | weak_ramp |
| 33 | `g6_distances_on_the_coordinate_plane` | Distances on the coordinate plane | 2 | failed_ramp |
| 34 | `g6_shapes_and_perimeter_on_the_coordinate_plane` | Shapes and perimeter on the coordinate plane | 2 | failed_ramp |
| 35 | `g6_coordinate_plane_distances_word_problems` | Distances, word problems | 2 | failed_ramp |
| 36 | `g6_writing_numeric_expressions` | Writing numeric expressions | 2 | verified_ramp |
| 37 | `g6_numeric_expressions_with_exponents` | Numeric expressions with exponents | 2 | verified_ramp |
| 38 | `g6_properties_of_addition_and_multiplication` | Properties of addition and multiplication | 2 | weak_ramp |
| 39 | `g6_numeric_expressions_and_order_of_operations` | Numeric expressions and the order of operations | 2 | verified_ramp |
| 40 | `g6_distributive_property_numeric` | Distributive property, numeric | 2 | failed_ramp |
| 41 | `g6_writing_algebraic_expressions` | Writing algebraic expressions | 3 | verified_ramp |
| 42 | `g6_evaluating_algebraic_expressions` | Evaluating linear expressions | 3 | verified_ramp |
| 43 | `g6_combining_like_terms` | Combining like terms | 3 | verified_ramp |
| 44 | `g6_distributive_property_area_diagrams_algebraic` | Distributive property with area diagrams, algebraic | 3 | verified_ramp |
| 45 | `g6_distributive_property_algebraic` | Distributive property, algebraic | 3 | verified_ramp |
| 46 | `g6_solutions_to_equations` | Solutions to equations | 3 | verified_ramp |
| 47 | `g6_equations_tape_diagrams` | Tape diagrams | 3 | verified_ramp |
| 48 | `g6_equations_hanger_diagrams` | Hanger diagrams | 3 | verified_ramp |
| 49 | `g6_equations_word_problems` | Equations word problems | 3 | verified_ramp |
| 50 | `g6_solutions_to_inequalities` | Solutions to inequalities | 3 | verified_ramp |
| 51 | `g6_writing_and_graphing_inequalities` | Writing and graphing inequalities | 4 | verified_ramp |
| 52 | `g6_inequalities_word_problems` | Inequalities word problems | 4 | verified_ramp |
| 53 | `g6_solving_and_graphing_one_step_inequalities` | Solving and graphing one-step inequalities | 4 | verified_ramp |
| 54 | `g6_inequalities_hanger_diagrams` | Hanger diagrams | 4 | verified_ramp |
| 55 | `g6_equivalent_ratio_equations` | Equivalent ratio equations | 4 | verified_ramp |
| 56 | `g6_constant_rate_equations` | Constant rate equations | 4 | verified_ramp |
| 57 | `g6_equations_for_other_relationships` | Equations for other relationships | 4 | verified_ramp |
| 58 | `g6_parallelograms_understanding_area_formula` | Parallelograms, understanding area formula | 4 | verified_ramp |
| 59 | `g6_parallelograms` | Parallelograms | 4 | verified_ramp |
| 60 | `g6_triangles_understanding_area_formula` | Triangles, understanding area formula | 4 | verified_ramp |
| 61 | `g6_triangles` | Triangles | 5 | verified_ramp |
| 62 | `g6_trapezoids` | Trapezoids | 5 | verified_ramp |
| 63 | `g6_kites` | Kites | 5 | verified_ramp |
| 64 | `g6_polygons_on_a_grid_or_coordinate_plane` | Polygons on a grid or coordinate plane | 5 | verified_ramp |
| 65 | `g6_polygons_and_shaded_regions` | Polygons and shaded regions | 5 | verified_ramp |
| 66 | `g6_classifying_and_naming` | Classifying and naming | 5 | verified_ramp |
| 67 | `g6_volume_and_surface_area_using_isometric_drawings` | Volume and surface area using isometric drawings | 5 | verified_ramp |
| 68 | `g6_formulas_for_volume_and_surface_area_of_a_cube` | Formulas for volume and surface area of a cube | 5 | verified_ramp |
| 69 | `g6_rectangles_with_fraction_side_lengths` | Rectangles with fraction side lengths | 5 | verified_ramp |
| 70 | `g6_triangles_with_fraction_side_lengths` | Triangles with fraction side lengths | 5 | verified_ramp |
| 71 | `g6_right_rectangular_prisms_with_fraction_side_lengths` | Right rectangular prisms with fraction side lengths | 6 | verified_ramp |
| 72 | `g6_interpreting_dot_plots` | Interpreting dot plots | 6 | verified_ramp |
| 73 | `g6_drawing_dot_plots` | Drawing dot plots | 6 | verified_ramp |
| 74 | `g6_interpreting_histograms` | Interpreting histograms | 6 | verified_ramp |
| 75 | `g6_drawing_histograms` | Drawing histograms | 6 | verified_ramp |
| 76 | `g6_data_center_and_spread` | Center and spread | 6 | verified_ramp |
| 77 | `g6_interpreting_box_plots` | Interpreting box plots | 6 | verified_ramp |

## Sources

- Prior 11 specs: `../g6_difficulty_effort_specs.md`
- Prior 11 means: `verification_summary.json`
- Batches: `batch_0_verification.json` … `batch_6_verification.json`
- Per-batch specs: `batch_0_specs.md` … `batch_6_specs.md`
