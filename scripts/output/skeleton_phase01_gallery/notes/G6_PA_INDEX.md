# G6 + Pre-Algebra type index

Inventory of question **type_ids** for Grade 6 and Pre-Algebra.
Setup-only: suggested engine family is a proposal, not a wiring change.

## Counts

| Source | G6 | PA |
|---|---:|---:|
| Catalog (`question_engine/catalogs/`) = `QUESTION_TYPES` with `g6_`/`pa_` (PA also lists `pythagorean_theorem`) | 88 | 47 |
| Already on a phase-01 skeleton (gallery `type_id` / alias, or catalog generator is a gallery type) | 12 | 10 |

**Already-on-skeleton** = yes if the leaf is a `SECTIONS` `type_id` or alias in
`scripts/output/skeleton_phase01_gallery/gen_examples.py`, **or** its catalog
`generator` is itself a gallery type (shared family already on that engine).

Engine family is one of: `number` / `affine` / `solve` / `wp` / `proportion` / `geometry` / `other`.

Also checked: `lib/curriculum.ts`, `scripts/_curriculum_type_mapping.json`,
`question_engine/settings/` (including `domains/`), `question_engine/generators/`.
Those sources did not add extra `g6_*`/`pa_*` **catalog leaves** beyond the tables
below. Generator-only keys and shared curriculum type_ids are in the appendix.

## Grade 6

| type_id | display name | already-on-skeleton? | suggested engine family |
|---|---|---|---|
|  | **Grade 6 — Ratios** |  |  |
| `g6_introduction_to_ratios` | Introduction to ratios | no | proportion |
| `g6_equivalent_ratios` | Equivalent ratios | no | proportion |
| `g6_part_part_whole_ratios` | Part-part-whole ratios | no | proportion |
| `g6_comparing_ratios` | Comparing ratios | no | proportion |
|  | **Grade 6 — Rates** |  |  |
| `g6_unit_rates_and_equivalent_rates` | Unit rates and equivalent rates | no | proportion |
| `g6_comparing_rates` | Comparing rates | no | proportion |
| `g6_converting_units` | Converting units | no | proportion |
|  | **Grade 6 — Percents** |  |  |
| `g6_introduction_to_percents` | Introduction to percents | no | number |
| `g6_relating_percents_fractions_and_decimals` | Relating percents, fractions, and decimals | no | number |
| `g6_finding_percents_with_equivalent_fractions` | Finding percents with equivalent fractions | no | number |
| `g6_solving_percent_problems_with_diagrams` | Solving percent problems with diagrams | no | wp |
| `g6_solving_percent_problems_with_formulas` | Solving percent problems with formulas | no | wp |
|  | **Grade 6 — Dividing Fractions** |  |  |
| `g6_how_many_groups_times` | How many groups/times? | no | number |
| `g6_what_fraction_of_a_whole` | What fraction of a whole? | no | number |
| `g6_how_much_in_each_group_time` | How much in each group/time? | no | number |
| `g6_dividing_fractions` | Dividing fractions | no | number |
|  | **Grade 6 — Decimal Arithmetic** |  |  |
| `g6_decimal_addition_with_diagrams` | Decimal addition with diagrams | no | number |
| `g6_decimal_addition` | Decimal addition | no | number |
| `g6_decimal_subtraction_with_diagrams` | Decimal subtraction with diagrams | no | number |
| `g6_decimal_subtraction` | Decimal subtraction | no | number |
| `g6_decimal_multiplication_with_equivalent_fractions` | Decimal multiplication with equivalent fractions | no | number |
| `g6_decimal_multiplication_with_area_diagrams` | Decimal multiplication with area diagrams | no | number |
| `g6_decimal_multiplication` | Decimal multiplication | no | number |
| `g6_long_division_with_remainders` | Long division with remainders | no | number |
| `g6_dividing_whole_numbers_that_result_in_decimals` | Dividing whole numbers that result in decimals | no | number |
| `g6_dividing_decimals_by_whole_numbers` | Dividing decimals by whole numbers | no | number |
| `g6_dividing_whole_numbers_by_decimals` | Dividing whole numbers by decimals | no | number |
| `g6_dividing_decimals_by_decimals` | Dividing decimals by decimals | no | number |
|  | **Grade 6 — Common Factors and Common Multiples** |  |  |
| `g6_factoring` | Factoring | no | number |
| `g6_greatest_common_factor` | Greatest common factor | no | number |
| `g6_least_common_multiple` | Least common multiple | no | number |
| `g6_gcf_and_lcm_word_problems` | GCF and LCM word problems | no | wp |
|  | **Grade 6 — Negative Numbers and Absolute Value** |  |  |
| `g6_numbers_on_a_number_line` | Numbers on a number line | no | number |
| `g6_number_line_word_problems` | Number line word problems | no | wp |
| `g6_opposites_of_numbers` | Opposites of numbers | no | number |
| `g6_comparing_numbers` | Comparing numbers | no | number |
| `g6_ordering_numbers` | Ordering numbers | no | number |
| `g6_absolute_values` | Absolute values | no | number |
| `g6_comparing_with_absolute_values` | Comparing with absolute values | no | number |
| `g6_ordering_with_absolute_values` | Ordering with absolute values | no | number |
|  | **Grade 6 — Coordinate Plane** |  |  |
| `g6_points_on_the_coordinate_plane` | Points on the coordinate plane | no | geometry |
| `g6_distances_on_the_coordinate_plane` | Distances on the coordinate plane | no | geometry |
| `g6_shapes_and_perimeter_on_the_coordinate_plane` | Shapes and perimeter on the coordinate plane | no | geometry |
| `g6_coordinate_plane_distances_word_problems` | Distances, word problems | no | wp |
|  | **Grade 6 — Numeric Expressions, Exponents, and the Order of Operations** |  |  |
| `g6_writing_numeric_expressions` | Writing numeric expressions | no | number |
| `g6_numeric_expressions_with_exponents` | Numeric expressions with exponents | no | number |
| `g6_properties_of_addition_and_multiplication` | Properties of addition and multiplication | no | number |
| `g6_numeric_expressions_and_order_of_operations` | Numeric expressions and the order of operations | no | number |
| `g6_distributive_property_area_diagrams_numeric` | Distributive property with area diagrams, numeric | no | affine |
| `g6_distributive_property_numeric` | Distributive property, numeric | no | affine |
|  | **Grade 6 — Variables and Algebraic Expressions** |  |  |
| `g6_writing_algebraic_expressions` | Writing algebraic expressions | no | affine |
| `g6_evaluating_algebraic_expressions` | Evaluating linear expressions | yes | affine |
|  | **Grade 6 — Equivalent Expressions** |  |  |
| `g6_combining_like_terms` | Combining like terms | yes | affine |
| `g6_distributive_property_area_diagrams_algebraic` | Distributive property with area diagrams, algebraic | no | affine |
| `g6_distributive_property_algebraic` | Distributive property, algebraic | yes | affine |
|  | **Grade 6 — Equations** |  |  |
| `g6_solutions_to_equations` | Solutions to equations | yes | solve |
| `g6_equations_tape_diagrams` | Tape diagrams | no | solve |
| `g6_equations_hanger_diagrams` | Hanger diagrams | no | solve |
| `g6_equations_word_problems` | Equations word problems | yes | wp |
|  | **Grade 6 — Inequalities** |  |  |
| `g6_solutions_to_inequalities` | Solutions to inequalities | yes | solve |
| `g6_writing_and_graphing_inequalities` | Writing and graphing inequalities | yes | solve |
| `g6_inequalities_word_problems` | Inequalities word problems | yes | wp |
| `g6_solving_and_graphing_one_step_inequalities` | Solving and graphing one-step inequalities | yes | solve |
| `g6_inequalities_hanger_diagrams` | Hanger diagrams | no | solve |
|  | **Grade 6 — Equations as Relationships between Two Variables** |  |  |
| `g6_equivalent_ratio_equations` | Equivalent ratio equations | yes | proportion |
| `g6_constant_rate_equations` | Constant rate equations | yes | wp |
| `g6_equations_for_other_relationships` | Equations for other relationships | yes | wp |
|  | **Grade 6 — Polygons** |  |  |
| `g6_parallelograms_understanding_area_formula` | Parallelograms, understanding area formula | no | geometry |
| `g6_parallelograms` | Parallelograms | no | geometry |
| `g6_triangles_understanding_area_formula` | Triangles, understanding area formula | no | geometry |
| `g6_triangles` | Triangles | no | geometry |
| `g6_trapezoids` | Trapezoids | no | geometry |
| `g6_kites` | Kites | no | geometry |
| `g6_polygons_on_a_grid_or_coordinate_plane` | Polygons on a grid or coordinate plane | no | geometry |
| `g6_polygons_and_shaded_regions` | Polygons and shaded regions | no | geometry |
|  | **Grade 6 — Polyhedra** |  |  |
| `g6_classifying_and_naming` | Classifying and naming | no | geometry |
| `g6_volume_and_surface_area_using_isometric_drawings` | Volume and surface area using isometric drawings | no | geometry |
| `g6_formulas_for_volume_and_surface_area_of_a_cube` | Formulas for volume and surface area of a cube | no | geometry |
|  | **Grade 6 — Area and Volume with Fractions** |  |  |
| `g6_rectangles_with_fraction_side_lengths` | Rectangles with fraction side lengths | no | geometry |
| `g6_triangles_with_fraction_side_lengths` | Triangles with fraction side lengths | no | geometry |
| `g6_right_rectangular_prisms_with_fraction_side_lengths` | Right rectangular prisms with fraction side lengths | no | geometry |
|  | **Grade 6 — Data Sets and Distributions** |  |  |
| `g6_interpreting_dot_plots` | Interpreting dot plots | no | other |
| `g6_drawing_dot_plots` | Drawing dot plots | no | other |
| `g6_interpreting_histograms` | Interpreting histograms | no | other |
| `g6_drawing_histograms` | Drawing histograms | no | other |
| `g6_data_center_and_spread` | Center and spread | no | other |
| `g6_interpreting_box_plots` | Interpreting box plots | no | other |
| `g6_drawing_box_plots` | Drawing box plots | no | other |

## Pre-Algebra

| type_id | display name | already-on-skeleton? | suggested engine family |
|---|---|---|---|
|  | **Pre-Algebra — Integers, Decimals, and Fractions** |  |  |
| `pa_naming_decimal_places_and_rounding` | Naming decimal places and rounding | no | number |
| `pa_writing_numbers_with_words` | Writing numbers with words | no | number |
| `pa_integers_adding_and_subtracting` | Adding and subtracting | no | number |
| `pa_integers_multiplying` | Multiplying | no | number |
| `pa_integers_dividing` | Dividing | no | number |
| `pa_factoring` | Factoring | no | number |
| `pa_greatest_common_factor` | Greatest common factor | no | number |
| `pa_least_common_multiple` | Least common multiple | no | number |
| `pa_simplifying_fractions` | Simplifying fractions | no | number |
| `pa_fractions_add_like` | Adding fractions (like denominators) | no | number |
| `pa_fractions_subtract_like` | Subtracting fractions (like denominators) | no | number |
| `pa_fractions_add_unlike` | Adding fractions (unlike denominators) | no | number |
| `pa_fractions_subtract_unlike` | Subtracting fractions (unlike denominators) | no | number |
| `pa_fractions_multiply` | Multiplying fractions | no | number |
| `pa_fractions_divide` | Dividing fractions | no | number |
| `pa_converting_fractions_and_decimals` | Converting fractions and decimals | no | number |
|  | **Pre-Algebra — Equations** |  |  |
| `pa_equations_one_step_word_problems` | One-step equations, word problems | yes | wp |
| `pa_equations_two_step_word_problems` | Two-step equations word problems | yes | wp |
| `pa_equations_multi_step_equations` | Multi-step equations | yes | solve |
|  | **Pre-Algebra — Inequalities** |  |  |
| `pa_multi_step_inequalities` | Multi-step inequalities | yes | solve |
|  | **Pre-Algebra — Factors and Exponents** |  |  |
| `pa_divisibility` | Divisibility | no | number |
| `pa_squares_and_square_roots` | Squares and square roots | no | number |
|  | **Pre-Algebra — Proportions and Similarity** |  |  |
| `pa_checking_for_a_proportion` | Checking for a proportion | yes | proportion |
| `pa_proportions_word_problems` | Proportions word problems | yes | wp |
| `pa_similar_figures` | Similar figures | yes | geometry |
| `pa_similar_figures_word_problems` | Similar figures word problems | yes | wp |
|  | **Pre-Algebra — Percents** |  |  |
| `pa_fractions_decimals_and_percents` | Fractions, decimals, and percents | no | number |
| `pa_markup_discount_and_tax` | Markup, discount, and tax | no | wp |
| `pa_simple_and_compound_interest` | Simple and compound interest | no | wp |
|  | **Pre-Algebra — Linear Equations and Inequalities** |  |  |
| `pa_plotting_points` | Plotting points | no | geometry |
| `pa_slope` | Slope | no | other |
| `pa_writing_linear_equations` | Writing linear equations | no | other |
| `pa_graphing_systems_of_equations` | Graphing systems of equations | no | other |
| `pa_systems_substitution` | Solving systems of equations by substitution | no | other |
| `pa_systems_word_problems` | Systems of equations word problems | no | wp |
|  | **Pre-Algebra — Plane Figures** |  |  |
| `pa_drawing_and_measuring_angles` | Drawing and measuring angles | no | geometry |
| `pa_angle_relationships` | Angle relationships | no | geometry |
| `pa_plane_figures_triangles` | Triangles | no | geometry |
| `pa_quadrilaterals` | Quadrilaterals | no | geometry |
| `pa_area_of_triangles_and_quadrilaterals` | Area of triangles and quadrilaterals | no | geometry |
| `pa_circles` | Circles | no | geometry |
| `pa_transformations` | Transformations | no | geometry |
|  | **Pre-Algebra — Solid Figures** |  |  |
| `pa_classifying_volume_and_surface_area` | Classifying, volume, and surface area | no | geometry |
|  | **Pre-Algebra — Right Triangles** |  |  |
| `pythagorean_theorem` | The Pythagorean Theorem | no | geometry |
|  | **Pre-Algebra — Beginning Polynomials** |  |  |
| `pa_polynomials_simplifying` | Simplifying | no | other |
| `pa_polynomials_adding_and_subtracting` | Adding and subtracting | yes | other |
| `pa_polynomials_multiplying` | Multiplying | yes | other |

## Appendix — not extra catalog leaves

### Generator / alias keys (no matching catalog `id`)

These appear in generators, settings, or the primitive registry. They are
producers or aliases, not additional picker type_ids.

**G6 generator keys:** `g6_fraction_add_like`, `g6_fraction_add_unlike`,
`g6_fraction_subtract_like`, `g6_fraction_subtract_unlike`, `g6_fraction_multiply`,
`g6_fraction_divide`, `g6_fraction_divide_groups`, `g6_fraction_divide_each`,
`g6_fraction_of_whole`, `g6_integer_add_subtract`, `g6_integer_multiply`,
`g6_integer_divide`, `g6_negative_number_operations`, `g6_divisibility`,
`g6_unit_rates` (catalog id `g6_unit_rates_and_equivalent_rates`),
`g6_decimal_divide`, `g6_whole_by_decimal_divide`, `g6_coordinate_perimeter`,
`g6_polygon_grid_area`, `g6_shaded_polygon_area`, `g6_area_model_algebraic`,
`g6_classify_polyhedron`, `g6_isometric_measure`, `g6_isometric_solid`,
`g6_fraction_rectangle_area`, `g6_fraction_triangle_area`, `g6_fraction_prism_volume`,
`g6_drawing_dot_plot`, `g6_drawing_histogram`, `g6_factor_gcf`
(gallery alias of `polynomial_factoring_common_factor` / FactorGcf — **on skeleton**,
not a G6 catalog leaf).

**PA generator / preset keys:** `pa_verbal_expressions` (preset; curriculum uses
`verbal_expressions`), `pa_systems_of_equations_elimination`,
`pa_systems_of_equations_substitution` (generators; catalog id is
`pa_systems_substitution`).

### Shared type_ids on the PA curriculum tree (no `pa_` prefix)

Listed under Pre-Algebra in `lib/curriculum.ts` but owned as shared/A1-style ids:
`verbal_expressions`, `order_of_operations`, `distributive_property`, `percents`,
`percent_of_change`, `one_step_equations`, `two_step_equations`,
`graphing_linear_equations`, `graphing_linear_inequalities`,
`graphing_single_variable_inequalities`, `one_step_inequalities`,
`two_step_inequalities`, `solving_proportions`, `properties_of_exponents`,
`scientific_notation_write`, `scientific_notation_operations`,
`radical_midpoint_formula`, `radical_distance_formula`, `visualizing_data`,
`center_and_spread`, `scatter_plots`. `pythagorean_theorem` **is** in the PA catalog.

Per-type notes: copy `_TEMPLATE.md` → `notes/<gallery-slug>.md` (or
`<slug>/NOTES.md`). Process: `.cursor/rules/topic-notes-process.mdc`.
