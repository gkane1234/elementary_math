# Algebra 1 type index

Inventory of question **type_ids** for Algebra 1.
Setup-only: suggested engine family is a proposal, not a wiring change.
Notes pass is **steps 1–3 only** (old path, `notes/<slug>.md`, OpenStax).
Do not implement A1 generators in this wave unless the leaf is already on a skeleton.

## Counts

| Source | A1 |
|---|---:|
| Catalog (`question_engine/catalogs/algebra_1.py`) = A1 `QUESTION_TYPES` leaves | 86 |
| Already on a phase-01 skeleton (gallery `type_id` / alias, or catalog generator is a gallery type) | 26 (+`direct_inverse_variation`) |
| Gallery stub pages for remaining A1 catalog leaves (`_build_a1_stub_sections`) | 19 |

**Already-on-skeleton** = yes if the leaf is a `SECTIONS` `type_id` or alias in
`scripts/output/skeleton_phase01_gallery/gen_examples.py`, **or** its catalog
`generator` is itself a gallery type (shared family already on that engine).

Engine family is one of: `number` / `affine` / `solve` / `wp` / `proportion` / `geometry` / `other`.

Also checked: `lib/curriculum.ts`, `question_engine/core/registry.py` (`ALGEBRA1_CATALOG`),
`QUESTION_TYPES`. Catalog ids match the A1 curriculum tree; extras vs G6/PA shared ids
are listed in the appendix.

## Notes backfill (already-on-skeleton)

Already-skeletoned leaves still need notes (may exist from the G6/PA wave).
A notes file counts as filled if it has an `openstax.org` cite **and** a
`What old path actually produced` section (same skip rule as `_sample_pa.py`).

Filled: **26** / 26 skeletoned (incl. variation). All **86** A1 leaves have notes + **Limitations**.

Gallery loads `notes/<slug>.md` first, then `notes/<type_id>.md`.

Filled already-on-skeleton notes:

| type_id | gallery slug | notes file |
|---|---|---|
| `one_step_equations` | `one_step` | `one_step.md` |
| `two_step_equations` | `two_step` | `two_step.md` |
| `multi_step_equations` | `multi_step` | `multi_step.md` |
| `absolute_value_equations` | `abs_eq` | `abs_eq.md` |
| `literal_equations` | `literal` | `literal.md` |
| `graphing_single_variable_inequalities` | `graph_ineq` | `graph_ineq.md` |
| `one_step_inequalities` | `one_step_ineq` | `one_step_ineq.md` |
| `two_step_inequalities` | `two_step_ineq` | `two_step_ineq.md` |
| `multi_step_inequalities` | `multi_step_ineq` | `multi_step_ineq.md` |
| `compound_inequalities` | `compound_ineq` | `compound_ineq.md` |
| `absolute_value_inequalities` | `abs_ineq` | `abs_ineq.md` |
| `solving_proportions` | `proportion` | `proportion.md` |
| `polynomial_add_subtract` | `poly_add_sub` | `poly_add_sub.md` |
| `polynomial_multiply` | `multiply` | `multiply.md` |
| `polynomial_multiply_special` | `multiply_special` | `multiply_special.md` |
| `polynomial_factoring_common_factor` | `factor_gcf` | `factor_gcf.md` |
| `polynomial_factoring_special_cases` | `factor_special` | `factor_special.md` |
| `polynomial_factoring_grouping` | `factor_grouping` | `factor_grouping.md` |
| `quadratic_factoring` | `factor_quadratic` | `factor_quadratic.md` |
| `polynomial_factoring_general_strategy` | `factor_all_techniques` | `factor_all_techniques.md` |
| `quadratic_factoring_equations` | `factor_equations` | `factor_equations.md` |
| `rational_simplification` | `simplify_cancel` | `simplify_cancel.md` |
| `rational_expression_simplification` | `add_sub_cancel` | `add_sub_cancel.md` |
| `rational_expression_multiply_divide` | `mul_div_cancel` | `mul_div_cancel.md` |
| `rational_expressions_equations` | `eq_cancel` | `eq_cancel.md` |
| `direct_inverse_variation` | `direct_inverse_variation` | `direct_inverse_variation.md` |

Non-skeletoned A1 leaves: all 86 have notes (percents / percent_of_change
backfilled as NOT_IMPLEMENTED stubs this pass). Every A1 notes file has a
**Limitations** section (variety / D-scaling / OpenStax / dump / duplicate /
evaluate-without-graph flags as applicable). Gallery stubs auto-fill remaining
catalog gaps via `_build_a1_stub_sections()` in `gen_examples.py`.

This pass backfilled gallery-slug notes for the 15 skeletoned leaves that lacked them:
`abs_eq`, `literal`, `compound_ineq`, `abs_ineq`, `multiply`, `multiply_special`,
`factor_special`, `factor_grouping`, `factor_quadratic`, `factor_all_techniques`,
`factor_equations`, `simplify_cancel`, `add_sub_cancel`, `mul_div_cancel`, `eq_cancel`.
(`factor_grouping` notes flag `UNCLEAR`: old D=0 was a trinomial, not grouping.)

## Algebra 1 catalog

| type_id | display name | already-on-skeleton? | suggested engine family |
|---|---|---|---|
|  | **Pre-Algebra — Beginning Algebra** |  |  |
| `verbal_expressions` | Verbal expressions | no | affine |
| `order_of_operations` | Order of operations | no | number |
| `distributive_property` | The Distributive Property | no | affine |
|  | **Algebra 1 — Beginning Algebra** |  |  |
| `sets_of_numbers` | Sets of numbers | no | number |
| `rational_add_subtract` | Adding and subtracting rational numbers | no | number |
| `rational_multiply` | Multiplying rational numbers | no | number |
| `rational_divide` | Dividing rational numbers | no | number |
|  | **Pre-Algebra — Equations** |  |  |
| `one_step_equations` | One-step equations | yes | solve |
| `two_step_equations` | Two-step equations | yes | solve |
|  | **Algebra 1 — Equations** |  |  |
| `multi_step_equations` | Multi-step equations | yes | solve |
| `absolute_value_equations` | Absolute value equations | yes | solve |
| `mixture_word_problems` | Mixture word problems | no | wp |
| `distance_rate_time_word_problems` | Distance, rate, time word problems | no | wp |
| `work_word_problems` | Work word problems | no | wp |
| `age_word_problems` | Age word problems | no | wp |
| `coin_word_problems` | Coin word problems | no | wp |
| `consecutive_integers_word_problems` | Consecutive integers word problems | no | wp |
| `percent_word_problems` | Percent word problems | no | wp |
| `literal_equations` | Literal equations | yes | solve |
|  | **Pre-Algebra — Inequalities** |  |  |
| `graphing_single_variable_inequalities` | Graphing single-variable inequalities | yes | solve |
| `one_step_inequalities` | One-step inequalities | yes | solve |
| `two_step_inequalities` | Two-step inequalities | yes | solve |
|  | **Algebra 1 — Inequalities** |  |  |
| `multi_step_inequalities` | Multi-step inequalities | yes | solve |
| `compound_inequalities` | Compound inequalities | yes | solve |
| `absolute_value_inequalities` | Absolute value inequalities | yes | solve |
|  | **Pre-Algebra — Percents** |  |  |
| `percents` | Percents | no | number |
| `percent_of_change` | Percent of change | no | number |
|  | **Pre-Algebra — Proportions and Similarity** |  |  |
| `solving_proportions` | Solving proportions | yes | proportion |
|  | **Algebra 1 — Linear Equations and Inequalities** |  |  |
| `more_on_slope` | More on slope | no | other |
| `graphing_absolute_value_equations` | Graphing absolute value equations | no | other |
|  | **Pre-Algebra — Linear Equations and Inequalities** |  |  |
| `slope` | Slope | no | other |
| `graphing_linear_equations` | Graphing linear equations | no | other |
| `writing_linear_equations` | Writing linear equations | no | other |
| `graphing_linear_inequalities` | Graphing linear inequalities | no | other |
| `radical_midpoint_formula` | The Midpoint Formula | no | geometry |
|  | **Algebra 1 — Systems of Equations and Inequalities** |  |  |
| `systems_graphing` | Solving by graphing | no | other |
| `systems_elimination` | Solving by elimination | no | other |
| `systems_substitution` | Solving by substitution | no | other |
| `graphing_systems_of_inequalities` | Graphing systems of inequalities | no | other |
| `systems_word_problems` | Word problems | no | wp |
|  | **Algebra 1 — Polynomials** |  |  |
| `polynomial_naming` | Naming | no | other |
| `polynomial_add_subtract` | Adding and subtracting | yes | other |
| `simplify_polynomials` | Simplifying polynomials | no | affine |
| `polynomial_multiply` | Multiplying | yes | other |
| `polynomial_multiply_special` | Multiplying special cases | yes | other |
| `polynomial_long_division` | Dividing | no | other |
|  | *Algebra 1 — Polynomials — Factoring* |  |  |
| `polynomial_factoring_common_factor` | Common factor only | yes | other |
| `polynomial_factoring_special_cases` | Special cases | yes | other |
| `polynomial_factoring_grouping` | By grouping | yes | other |
| `quadratic_factoring` | Quadratic expressions | yes | other |
| `polynomial_factoring_general_strategy` | General strategy | yes | other |
|  | **Algebra 1 — Quadratic Functions** |  |  |
| `graphing_quadratic_functions` | Graphing | no | other |
| `quadratic_solve_by_graphing` | Solving equations by graphing | no | other |
| `graphing_quadratic_inequalities` | Graphing quadratic inequalities | no | other |
| `quadratic_square_roots` | Solving equations by taking square roots | no | solve |
| `quadratic_factoring_equations` | Solving equations by factoring | yes | other |
| `quadratic_formula` | Solving equations with the Quadratic Formula | no | solve |
| `quadratic_discriminant` | Understanding the discriminant | no | solve |
| `quadratic_completing_square_constant` | Completing the square by finding the constant | no | solve |
| `quadratic_completing_square_solve` | Solving equations by completing the square | no | solve |
|  | **Algebra 1 — Rational Expressions** |  |  |
| `rational_simplification` | Simplifying and excluded values | yes | other |
| `rational_expression_simplification` | Adding and subtracting rational expressions | yes | other |
| `rational_expression_multiply_divide` | Multiplying and dividing rational expressions | yes | other |
| `rational_expressions_equations` | Rational equations | yes | other |
|  | **Algebra 1 — Radical Expressions** |  |  |
| `radical_simplification` | Simplifying single radicals | no | other |
| `radical_add_subtract` | Adding and subtracting | no | other |
| `radical_multiply` | Multiplying | no | other |
| `radical_divide` | Dividing | no | other |
| `radical_equations` | Equations | no | solve |
|  | **Algebra 1 — Relations and Introduction to Functions** |  |  |
| `discrete_relations` | Discrete relations | no | other |
| `continuous_relations` | Continuous relations | no | other |
| `evaluating_graphing_functions` | Evaluating and graphing functions | no | other |
|  | **Algebra 1 — Direct and inverse variation** |  |  |
| `direct_inverse_variation` | Direct and inverse variation | yes (`VariationEq`) | other |
|  | **Pre-Algebra — Factors and Exponents** |  |  |
| `properties_of_exponents` | Properties of exponents | no | number |
| `scientific_notation_write` | Writing scientific notation | no | number |
| `scientific_notation_operations` | Operations and scientific notation | no | number |
|  | **Algebra 1 — Exponents** |  |  |
| `graphing_exponential_functions` | Graphing exponential functions | no | other |
| `scientific_notation_add_subtract` | Addition/Subtraction and scientific notation | no | number |
| `exponential_growth_decay` | Discrete exponential growth and decay word problems | no | wp |
|  | **Pre-Algebra — Right Triangles** |  |  |
| `radical_distance_formula` | The Distance Formula | no | geometry |
|  | **Algebra 1 — Beginning Trigonometry** |  |  |
| `finding_sine_cosine_tangent` | Finding sine, cosine, tangent | no | geometry |
| `finding_angles` | Finding angles | no | geometry |
| `find_missing_sides_of_triangles` | Find missing sides of triangles | no | geometry |
|  | **Pre-Algebra — Statistics** |  |  |
| `visualizing_data` | Visualizing data | no | other |
| `center_and_spread` | Center and spread | no | other |
| `scatter_plots` | Scatter plots | no | other |

## Appendix — not extra catalog leaves

### Shared with Pre-Algebra / G6 (A1 catalog owns the unprefixed id)

These sit in `algebra_1.py` (often under a `Pre-Algebra — …` category) and also
appear on the PA curriculum tree in `lib/curriculum.ts`. They are **A1 catalog
leaves**, not extras. G6/PA notes may already exist under the same `type_id` or a
gallery slug.

`verbal_expressions`, `order_of_operations`, `distributive_property`, `one_step_equations`, `two_step_equations`, `graphing_single_variable_inequalities`, `one_step_inequalities`, `two_step_inequalities`, `solving_proportions`, `percents`, `percent_of_change`, `slope`, `graphing_linear_equations`, `writing_linear_equations`, `graphing_linear_inequalities`, `properties_of_exponents`, `scientific_notation_write`, `scientific_notation_operations`, `radical_distance_formula`, `radical_midpoint_formula`, `visualizing_data`, `center_and_spread`, `scatter_plots`.

### Generator keys that differ from catalog `id`

Catalog `generator=` is a producer, not an extra picker type_id:

| type_id | generator |
|---|---|
| `mixture_word_problems` | `wp_mixture` |
| `distance_rate_time_word_problems` | `wp_distance_rate_time` |
| `work_word_problems` | `wp_work` |
| `age_word_problems` | `wp_age` |
| `coin_word_problems` | `wp_coin` |
| `consecutive_integers_word_problems` | `wp_consecutive_integers` |
| `percent_word_problems` | `wp_percent` |
| `graphing_single_variable_inequalities` | `graph_single_variable_inequality` |
| `graphing_linear_equations` | `graph_linear_equation` |
| `graphing_linear_inequalities` | `graph_linear_inequality` |
| `graphing_absolute_value_equations` | `graph_absolute_value` |
| `systems_graphing` | `graph_system` |
| `graphing_systems_of_inequalities` | `graph_system_inequalities` |
| `systems_word_problems` | `wp_systems` |
| `graphing_exponential_functions` | `graph_exponential` |
| `graphing_quadratic_functions` | `graph_quadratic` |
| `quadratic_solve_by_graphing` | `solve_polynomial_by_graphing` |
| `graphing_quadratic_inequalities` | `graph_quadratic_inequality` |
| `rational_expressions_equations` | `rational_equations` |
| `finding_sine_cosine_tangent` | `geo_right_triangle_trig_ratio` |
| `find_missing_sides_of_triangles` | `geo_right_triangle_trig_side` |
| `visualizing_data` | `stats_dot_plot_read` |
| `center_and_spread` | `stats_center_spread` |
| `scatter_plots` | `scatter_plot_interpret` |

### `QUESTION_TYPES` vs catalog

Every A1 catalog `id` is registered in `QUESTION_TYPES`.

Per-type notes: copy `_TEMPLATE.md` → `notes/<gallery-slug>.md` (or
`<type_id>.md` / `<slug>/NOTES.md`). Process: `.cursor/rules/topic-notes-process.mdc`.
