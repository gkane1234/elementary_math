# Algebra 2 type index

Inventory of question **type_ids** for Algebra 2.
Setup-only: suggested engine family is a proposal, not a wiring change.
Notes pass is **steps 1–3 only** (old path, `notes/<slug>.md`, OpenStax).
Do not implement Algebra 2 generators in this wave unless the leaf is already on a skeleton.

## Gallery stubs + Limitations (2026-08 wave)

- Every A2 catalog `type_id` has `notes/<type_id>.md` with a **## Limitations** section.
- `gen_examples.py` auto-stubs any A2 leaf not already in `SECTIONS` (`_build_a2_stub_sections`); thin A1 twins get aliases via `_ensure_a2_aliases_on_sections`.
- **Graphing / spatial UNCLEAR** leaves carry `UNCLEAR` + `NOT_IMPLEMENTED` → red gallery header + why not on an algebraic core.
- Regen touched A2 rows:  
  `python scripts/output/skeleton_phase01_gallery/gen_examples.py --only <slug[,slug…]>`
- **Implemented this wave:** none new (graph gold still unclear). Shipped earlier: complex ±/×/abs/rationalize, 3×3 systems, variation packaging (residual frame Limitations).

## Counts

| Source | A2 |
|---|---:|
| Catalog (`question_engine/catalogs/algebra_2.py`) = Algebra 2 `QUESTION_TYPES` leaves | 145 |
| Already on a phase-01 skeleton (gallery `type_id` / alias, or catalog generator is a gallery type) | 44 |
| Thin A1 aliases (prefixed id on skeleton via shared A1/unprefixed canonical) | 41 |

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
| `a2_beginning_algebra_simplifying_algebraic_expressions` | Simplifying algebraic expressions | `g6_distributive_property_algebraic` | `distribute` | affine |
| `a2_equations_and_inequalities_multi_step_equations` | Multi-step equations | `multi_step_equations` | `multi_step` | solve |
| `a2_equations_and_inequalities_literal_equations` | Literal equations | `literal_equations` | `literal` | solve |
| `a2_equations_and_inequalities_absolute_value_equations` | Absolute value equations | `absolute_value_equations` | `abs_eq` | solve |
| `a2_equations_and_inequalities_multi_step_inequalities` | Multi-step inequalities | `multi_step_inequalities` | `multi_step_ineq` | solve |
| `a2_equations_and_inequalities_compound_inequalities` | Compound inequalities | `compound_inequalities` | `compound_ineq` | solve |
| `a2_equations_and_inequalities_absolute_value_inequalities` | Absolute value inequalities | `absolute_value_inequalities` | `abs_ineq` | solve |
| `a2_relations_and_introduction_to_functions_discrete_relations` | Discrete relations | `discrete_relations` | `discrete_relations` | other |
| `a2_relations_and_introduction_to_functions_continuous_relations` | Continuous relations | `continuous_relations` | `continuous_relations` | other |
| `a2_relations_and_introduction_to_functions_evaluating_and_graphing_functions` | Evaluating and graphing functions | `evaluating_graphing_functions` | `evaluating_graphing_functions` | other |
| `a2_linear_relations_and_functions_writing_linear_equations` | Writing linear equations | `pa_writing_linear_equations` | `pa_write_linear` | other |
| `a2_systems_of_equations_and_inequalities_solving_systems_by_elimination_2_variables` | Solving systems by elimination (2 variables) | `systems_elimination` | `systems_elimination` | other |
| `a2_systems_of_equations_and_inequalities_solving_systems_by_substitution_2_variables` | Solving systems by substitution (2 variables) | `pa_systems_substitution` | `pa_systems_sub` | other |
| `a2_quadratic_functions_and_inequalities_factoring_quadratic_expressions` | Factoring quadratic expressions | `quadratic_factoring` | `factor_quadratic` | other |
| `a2_quadratic_functions_and_inequalities_factoring_special_case_quadratic_expressions` | Factoring special case quadratic expressions | `polynomial_factoring_special_cases` | `factor_special` | other |
| `a2_quadratic_functions_and_inequalities_solving_equations_by_taking_square_roots` | Solving equations by taking square roots | `quadratic_square_roots` | `quadratic_square_roots` | solve |
| `a2_quadratic_functions_and_inequalities_solving_equations_by_factoring` | Solving equations by factoring | `quadratic_factoring_equations` | `factor_equations` | other |
| `a2_quadratic_functions_and_inequalities_completing_the_square` | Completing the square | `quadratic_completing_square_constant` | `quadratic_completing_square_constant` | solve |
| `a2_quadratic_functions_and_inequalities_solving_equations_by_completing_the_square` | Solving equations by completing the square | `quadratic_completing_square_solve` | `quadratic_completing_square_solve` | solve |
| `a2_quadratic_functions_and_inequalities_solving_equations_with_the_quadratic_formula` | Solving equations with the Quadratic Formula | `quadratic_formula` | `quadratic_formula` | solve |
| `a2_quadratic_functions_and_inequalities_the_discriminant` | The discriminant | `quadratic_discriminant` | `quadratic_discriminant` | solve |
| `a2_polynomial_functions_naming` | Naming | `polynomial_naming` | `polynomial_naming` | other |
| `a2_polynomial_functions_simplifying` | Simplifying | `simplify_polynomials` | `simplify_polynomials` | other |
| `a2_polynomial_functions_adding_and_subtracting` | Adding and subtracting | `polynomial_add_subtract` | `poly_add_sub` | other |
| `a2_polynomial_functions_multiplying` | Multiplying | `polynomial_multiply` | `multiply` | other |
| `a2_polynomial_functions_multiplying_special_cases` | Multiplying special cases | `polynomial_multiply_special` | `multiply_special` | other |
| `a2_polynomial_functions_dividing` | Dividing | `polynomial_long_division` | `polynomial_long_division` | other |
| `a2_polynomial_functions_factoring_by_grouping` | Factoring by grouping | `polynomial_factoring_grouping` | `factor_grouping` | other |
| `a2_polynomial_functions_factoring_all_techniques` | Factoring all techniques | `polynomial_factoring_general_strategy` | `factor_all_techniques` | other |
| `a2_polynomial_functions_conjugate_roots_and_factoring` | Conjugate roots & factoring | `polynomial_factoring_special_cases` | `factor_special` | other |
| `a2_polynomial_functions_solving_polynomial_equations` | Solving polynomial equations | `quadratic_factoring_equations` | `factor_equations` | other |
| `a2_radical_functions_and_rational_exponents_simplifying_radicals` | Simplifying radicals | `radical_simplification` | `radical_simplification` | other |
| `a2_radical_functions_and_rational_exponents_adding_and_subtracting_radical_expressions` | Adding and subtracting radical expressions | `radical_add_subtract` | `radical_add_subtract` | other |
| `a2_radical_functions_and_rational_exponents_multiplying_radical_expressions` | Multiplying radical expressions | `radical_multiply` | `radical_multiply` | other |
| `a2_radical_functions_and_rational_exponents_dividing_radical_expressions` | Dividing radical expressions | `radical_divide` | `radical_divide` | other |
| `a2_radical_functions_and_rational_exponents_radical_equations` | Radical equations | `radical_equations` | `radical_equations` | solve |
| `a2_radical_functions_and_rational_exponents_rational_exponent_equations` | Rational exponent equations | `radical_equations` | `radical_equations` | solve |
| `a2_rational_expressions_simplifying` | Simplifying rational expressions | `rational_simplification` | `simplify_cancel` | other |
| `a2_rational_expressions_multiplying_and_dividing` | Multiplying and dividing rational expressions | `rational_expression_multiply_divide` | `mul_div_cancel` | other |
| `a2_rational_expressions_adding_and_subtracting` | Adding and subtracting rational expressions | `rational_expression_simplification` | `add_sub_cancel` | other |
| `a2_rational_expressions_equations` | Rational equations | `rational_expressions_equations` | `eq_cancel` | other |

## Notes backfill (already-on-skeleton)

Already-skeletoned leaves still need notes before wiring changes.
A notes file counts as filled if it has an `openstax.org` cite **and** a
`What old path actually produced` section (same skip rule as `_sample_pa.py`).

Filled: **44** / 44. Still need backfill: **0**.

Filled already-on-skeleton notes:

| type_id | gallery slug | notes file |
|---|---|---|
| `a2_beginning_algebra_simplifying_algebraic_expressions` | `distribute` | `distribute.md` |
| `a2_equations_and_inequalities_multi_step_equations` | `multi_step` | `multi_step.md` |
| `a2_equations_and_inequalities_literal_equations` | `literal` | `literal.md` |
| `a2_equations_and_inequalities_absolute_value_equations` | `abs_eq` | `abs_eq.md` |
| `a2_equations_and_inequalities_multi_step_inequalities` | `multi_step_ineq` | `multi_step_ineq.md` |
| `a2_equations_and_inequalities_compound_inequalities` | `compound_ineq` | `compound_ineq.md` |
| `a2_equations_and_inequalities_absolute_value_inequalities` | `abs_ineq` | `abs_ineq.md` |
| `a2_relations_and_introduction_to_functions_discrete_relations` | `discrete_relations` | `discrete_relations.md` |
| `a2_relations_and_introduction_to_functions_continuous_relations` | `continuous_relations` | `continuous_relations.md` |
| `a2_relations_and_introduction_to_functions_evaluating_and_graphing_functions` | `evaluating_graphing_functions` | `evaluating_graphing_functions.md` |
| `a2_linear_relations_and_functions_writing_linear_equations` | `pa_write_linear` | `a2_linear_relations_and_functions_writing_linear_equations.md` |
| `a2_systems_of_equations_and_inequalities_solving_systems_by_elimination_2_variables` | `systems_elimination` | `systems_elimination.md` |
| `a2_systems_of_equations_and_inequalities_solving_systems_by_substitution_2_variables` | `pa_systems_sub` | `a2_systems_of_equations_and_inequalities_solving_systems_by_substitution_2_variables.md` |
| `a2_quadratic_functions_and_inequalities_factoring_quadratic_expressions` | `factor_quadratic` | `factor_quadratic.md` |
| `a2_quadratic_functions_and_inequalities_factoring_special_case_quadratic_expressions` | `factor_special` | `factor_special.md` |
| `a2_quadratic_functions_and_inequalities_solving_equations_by_taking_square_roots` | `quadratic_square_roots` | `quadratic_square_roots.md` |
| `a2_quadratic_functions_and_inequalities_solving_equations_by_factoring` | `factor_equations` | `factor_equations.md` |
| `a2_quadratic_functions_and_inequalities_completing_the_square` | `quadratic_completing_square_constant` | `quadratic_completing_square_constant.md` |
| `a2_quadratic_functions_and_inequalities_solving_equations_by_completing_the_square` | `quadratic_completing_square_solve` | `quadratic_completing_square_solve.md` |
| `a2_quadratic_functions_and_inequalities_solving_equations_with_the_quadratic_formula` | `quadratic_formula` | `quadratic_formula.md` |
| `a2_quadratic_functions_and_inequalities_the_discriminant` | `quadratic_discriminant` | `quadratic_discriminant.md` |
| `a2_polynomial_functions_naming` | `polynomial_naming` | `polynomial_naming.md` |
| `a2_polynomial_functions_simplifying` | `simplify_polynomials` | `simplify_polynomials.md` |
| `a2_polynomial_functions_adding_and_subtracting` | `poly_add_sub` | `poly_add_sub.md` |
| `a2_polynomial_functions_multiplying` | `multiply` | `multiply.md` |
| `a2_polynomial_functions_multiplying_special_cases` | `multiply_special` | `multiply_special.md` |
| `a2_polynomial_functions_dividing` | `polynomial_long_division` | `polynomial_long_division.md` |
| `a2_polynomial_functions_factoring_by_grouping` | `factor_grouping` | `factor_grouping.md` |
| `a2_polynomial_functions_factoring_sum_difference_of_cubes` | `factor_cubes` | `a2_polynomial_functions_factoring_sum_difference_of_cubes.md` |
| `a2_polynomial_functions_factoring_quadratic_form` | `factor_quadratic_form` | `a2_polynomial_functions_factoring_quadratic_form.md` |
| `a2_polynomial_functions_factoring_all_techniques` | `factor_all_techniques` | `factor_all_techniques.md` |
| `a2_polynomial_functions_conjugate_roots_and_factoring` | `factor_special` | `factor_special.md` |
| `a2_polynomial_functions_solving_polynomial_equations` | `factor_equations` | `factor_equations.md` |
| `a2_radical_functions_and_rational_exponents_simplifying_radicals` | `radical_simplification` | `radical_simplification.md` |
| `a2_radical_functions_and_rational_exponents_adding_and_subtracting_radical_expressions` | `radical_add_subtract` | `radical_add_subtract.md` |
| `a2_radical_functions_and_rational_exponents_multiplying_radical_expressions` | `radical_multiply` | `radical_multiply.md` |
| `a2_radical_functions_and_rational_exponents_dividing_radical_expressions` | `radical_divide` | `radical_divide.md` |
| `a2_radical_functions_and_rational_exponents_radical_equations` | `radical_equations` | `radical_equations.md` |
| `a2_radical_functions_and_rational_exponents_rational_exponent_equations` | `radical_equations` | `radical_equations.md` |
| `a2_rational_expressions_simplifying` | `simplify_cancel` | `simplify_cancel.md` |
| `a2_rational_expressions_multiplying_and_dividing` | `mul_div_cancel` | `mul_div_cancel.md` |
| `a2_rational_expressions_adding_and_subtracting` | `add_sub_cancel` | `add_sub_cancel.md` |
| `a2_rational_expressions_complex_fractions` | `complex_frac_cancel` | `a2_rational_expressions_complex_fractions.md` |
| `a2_rational_expressions_equations` | `eq_cancel` | `eq_cancel.md` |

## Algebra 2 catalog

| type_id | display name | already-on-skeleton? | suggested engine family | A1 alias |
|---|---|---|---|---|
|  | **Algebra 2 — Beginning Algebra** |  |  |  |
| `a2_beginning_algebra_order_of_operations` | Order of operations | no | number | `order_of_operations` |
| `a2_beginning_algebra_simplifying_algebraic_expressions` | Simplifying algebraic expressions | yes | affine | `g6_distributive_property_algebraic` |
|  | **Algebra 2 — Equations and Inequalities** |  |  |  |
| `a2_equations_and_inequalities_multi_step_equations` | Multi-step equations | yes | solve | `multi_step_equations` |
| `a2_equations_and_inequalities_literal_equations` | Literal equations | yes | solve | `literal_equations` |
| `a2_equations_and_inequalities_work_word_problems` | Work word problems | no | wp | `work_word_problems` |
| `a2_equations_and_inequalities_distance_rate_time_word_problems` | Distance, rate, time word problems | no | wp | `distance_rate_time_word_problems` |
| `a2_equations_and_inequalities_mixture_word_problems` | Mixture word problems | no | wp | `mixture_word_problems` |
| `a2_equations_and_inequalities_absolute_value_equations` | Absolute value equations | yes | solve | `absolute_value_equations` |
| `a2_equations_and_inequalities_multi_step_inequalities` | Multi-step inequalities | yes | solve | `multi_step_inequalities` |
| `a2_equations_and_inequalities_compound_inequalities` | Compound inequalities | yes | solve | `compound_inequalities` |
| `a2_equations_and_inequalities_absolute_value_inequalities` | Absolute value inequalities | yes | solve | `absolute_value_inequalities` |
|  | **Algebra 2 — Relations and Introduction to Functions** |  |  |  |
| `a2_relations_and_introduction_to_functions_discrete_relations` | Discrete relations | yes | other | `discrete_relations` |
| `a2_relations_and_introduction_to_functions_continuous_relations` | Continuous relations | yes | other | `continuous_relations` |
| `a2_relations_and_introduction_to_functions_evaluating_and_graphing_functions` | Evaluating and graphing functions | yes | other | `evaluating_graphing_functions` |
|  | **Algebra 2 — Linear Relations and Functions** |  |  |  |
| `a2_linear_relations_and_functions_graphing_linear_equations` | Graphing linear equations | no | solve | `graphing_linear_equations` |
| `a2_linear_relations_and_functions_writing_linear_equations` | Writing linear equations | yes | other | `pa_writing_linear_equations` |
| `a2_linear_relations_and_functions_graphing_absolute_value_equations` | Graphing absolute value equations | no | solve | `graphing_absolute_value_equations` |
| `a2_linear_relations_and_functions_graphing_linear_inequalities` | Graphing linear inequalities | no | solve | `graphing_linear_inequalities` |
|  | **Algebra 2 — Systems of Equations and Inequalities** |  |  |  |
| `a2_systems_of_equations_and_inequalities_graphing_systems_of_linear_inequalities` | Graphing systems of linear inequalities | no | solve | `graphing_systems_of_inequalities` |
| `a2_systems_of_equations_and_inequalities_solving_systems_by_graphing_2_variables` | Solving systems by graphing (2 variables) | no | solve | `systems_graphing` |
| `a2_systems_of_equations_and_inequalities_solving_systems_by_elimination_2_variables` | Solving systems by elimination (2 variables) | yes | other | `systems_elimination` |
| `a2_systems_of_equations_and_inequalities_solving_systems_by_substitution_2_variables` | Solving systems by substitution (2 variables) | yes | other | `pa_systems_substitution` |
| `a2_systems_of_equations_and_inequalities_systems_of_equations_word_problems_2_variables` | Systems of equations word problems (2 variables) | no | wp | `systems_word_problems` |
| `a2_systems_of_equations_and_inequalities_points_in_three_dimensions` | Points in three dimensions | no | solve | — |
| `a2_systems_of_equations_and_inequalities_planes` | Planes | no | solve | — |
| `a2_systems_of_equations_and_inequalities_solving_systems_with_three_variables` | Solving systems with three variables | no | solve | — |
|  | **Algebra 2 — Polynomial Functions** |  |  |  |
| `a2_polynomial_functions_naming` | Naming | yes | other | `polynomial_naming` |
| `a2_polynomial_functions_simplifying` | Simplifying | yes | other | `simplify_polynomials` |
| `a2_polynomial_functions_adding_and_subtracting` | Adding and subtracting | yes | other | `polynomial_add_subtract` |
| `a2_polynomial_functions_multiplying` | Multiplying | yes | other | `polynomial_multiply` |
| `a2_polynomial_functions_multiplying_special_cases` | Multiplying special cases | yes | other | `polynomial_multiply_special` |
| `a2_polynomial_functions_the_binomial_theorem` | The Binomial Theorem | no | other | — |
| `a2_polynomial_functions_dividing` | Dividing | yes | other | `polynomial_long_division` |
| `a2_polynomial_functions_factoring_by_grouping` | Factoring by grouping | yes | other | `polynomial_factoring_grouping` |
| `a2_polynomial_functions_factoring_sum_difference_of_cubes` | Factoring a sum/difference of cubes | yes | other | — |
| `a2_polynomial_functions_factoring_quadratic_form` | Factoring quadratic form | yes | other | — |
| `a2_polynomial_functions_factoring_all_techniques` | Factoring all techniques | yes | other | `polynomial_factoring_general_strategy` |
| `a2_polynomial_functions_the_remainder_theorem` | The Remainder Theorem | no | other | — |
| `a2_polynomial_functions_writing_functions` | Writing functions | no | other | — |
| `a2_polynomial_functions_conjugate_roots_and_factoring` | Conjugate roots & factoring | yes | other | `polynomial_factoring_special_cases` |
| `a2_polynomial_functions_conjugate_roots_and_writing_functions` | Conjugate roots & writing functions | no | other | — |
| `a2_polynomial_functions_descartes_rule_of_signs` | Descartes' Rule of Signs | no | other | — |
| `a2_polynomial_functions_rational_zero_root_theorem` | Rational Zero/Root Theorem | no | other | — |
| `a2_polynomial_functions_fundamental_theorem_of_algebra` | Fundamental Theorem of Algebra | no | other | — |
| `a2_polynomial_functions_solving_polynomial_equations` | Solving polynomial equations | yes | other | `quadratic_factoring_equations` |
| `a2_polynomial_functions_end_behavior_and_general_graph_shape` | End behavior and general graph shape | no | other | — |
| `a2_polynomial_functions_graphing` | Graphing | no | other | `graphing_quadratic_functions` |
|  | **Algebra 2 — Quadratic Functions and Inequalities** |  |  |  |
| `a2_quadratic_functions_and_inequalities_graphing_quadratic_functions` | Graphing quadratic functions | no | solve | — |
| `a2_quadratic_functions_and_inequalities_graphing_quadratic_inequalities` | Graphing quadratic inequalities | no | solve | — |
| `a2_quadratic_functions_and_inequalities_solving_equations_by_graphing` | Solving equations by graphing | no | solve | `quadratic_solve_by_graphing` |
| `a2_quadratic_functions_and_inequalities_factoring_quadratic_expressions` | Factoring quadratic expressions | yes | other | `quadratic_factoring` |
| `a2_quadratic_functions_and_inequalities_factoring_special_case_quadratic_expressions` | Factoring special case quadratic expressions | yes | other | `polynomial_factoring_special_cases` |
| `a2_quadratic_functions_and_inequalities_solving_equations_by_taking_square_roots` | Solving equations by taking square roots | yes | solve | `quadratic_square_roots` |
| `a2_quadratic_functions_and_inequalities_solving_equations_by_factoring` | Solving equations by factoring | yes | other | `quadratic_factoring_equations` |
| `a2_quadratic_functions_and_inequalities_completing_the_square` | Completing the square | yes | solve | `quadratic_completing_square_constant` |
| `a2_quadratic_functions_and_inequalities_solving_equations_by_completing_the_square` | Solving equations by completing the square | yes | solve | `quadratic_completing_square_solve` |
| `a2_quadratic_functions_and_inequalities_solving_equations_with_the_quadratic_formula` | Solving equations with the Quadratic Formula | yes | solve | `quadratic_formula` |
| `a2_quadratic_functions_and_inequalities_the_discriminant` | The discriminant | yes | solve | `quadratic_discriminant` |
|  | **Algebra 2 — Rational Expressions** |  |  |  |
| `a2_rational_expressions_graphing` | Graphing rational functions | no | other | — |
| `a2_rational_expressions_simplifying` | Simplifying rational expressions | yes | other | `rational_simplification` |
| `a2_rational_expressions_multiplying_and_dividing` | Multiplying and dividing rational expressions | yes | other | `rational_expression_multiply_divide` |
| `a2_rational_expressions_adding_and_subtracting` | Adding and subtracting rational expressions | yes | other | `rational_expression_simplification` |
| `a2_rational_expressions_complex_fractions` | Complex fractions | yes | other | — |
| `a2_rational_expressions_equations` | Rational equations | yes | other | `rational_expressions_equations` |
|  | **Algebra 2 — Radical Functions and Rational Exponents** |  |  |  |
| `a2_radical_functions_and_rational_exponents_simplifying_radicals` | Simplifying radicals | yes | other | `radical_simplification` |
| `a2_radical_functions_and_rational_exponents_adding_and_subtracting_radical_expressions` | Adding and subtracting radical expressions | yes | other | `radical_add_subtract` |
| `a2_radical_functions_and_rational_exponents_multiplying_radical_expressions` | Multiplying radical expressions | yes | other | `radical_multiply` |
| `a2_radical_functions_and_rational_exponents_dividing_radical_expressions` | Dividing radical expressions | yes | other | `radical_divide` |
| `a2_radical_functions_and_rational_exponents_connecting_radical_expressions_and_rational_exponents` | Connecting radical expressions and rational exponents | no | other | `properties_of_exponents` |
| `a2_radical_functions_and_rational_exponents_evaluating_rational_exponent_expressions` | Evaluating rational exponent expressions | no | other | `properties_of_exponents` |
| `a2_radical_functions_and_rational_exponents_the_properties_of_exponents` | The properties of exponents | no | other | `properties_of_exponents` |
| `a2_radical_functions_and_rational_exponents_radical_equations` | Radical equations | yes | solve | `radical_equations` |
| `a2_radical_functions_and_rational_exponents_rational_exponent_equations` | Rational exponent equations | yes | solve | `radical_equations` |
| `a2_radical_functions_and_rational_exponents_graphing_radical_equations` | Graphing radical equations | no | solve | — |
| `a2_radical_functions_and_rational_exponents_domain_and_range_of_radical_functions` | Domain and range of radical functions | no | other | — |
|  | **Algebra 2 — Exponential and Logarithmic Expressions** |  |  |  |
| `a2_exponential_and_logarithmic_expressions_graphing_exponential_functions` | Graphing exponential functions | no | other | `graphing_exponential_functions` |
| `a2_exponential_and_logarithmic_expressions_exponential_equations_not_requiring_logarithms` | Exponential equations not requiring logarithms | no | solve | — |
| `a2_exponential_and_logarithmic_expressions_exponents_and_logarithms` | Exponents and logarithms | no | other | — |
| `a2_exponential_and_logarithmic_expressions_evaluating_logarithms` | Evaluating logarithms | no | other | — |
| `a2_exponential_and_logarithmic_expressions_logarithms_and_exponents_as_inverses` | Logarithms and exponents as inverses | no | other | — |
| `a2_exponential_and_logarithmic_expressions_properties_of_logarithms` | Properties of logarithms | no | other | — |
| `a2_exponential_and_logarithmic_expressions_writing_logs_in_terms_of_others` | Writing logs in terms of others | no | other | — |
| `a2_exponential_and_logarithmic_expressions_exponential_equations_requiring_logarithms` | Exponential equations requiring logarithms | no | solve | — |
| `a2_exponential_and_logarithmic_expressions_inverses_of_exponential_and_logarithmic_functions` | Inverses of exponential and logarithmic functions | no | other | — |
| `a2_exponential_and_logarithmic_expressions_logarithmic_equations_simple` | Logarithmic equations, simple | no | solve | — |
| `a2_exponential_and_logarithmic_expressions_logarithmic_equations_hard` | Logarithmic equations, hard | no | solve | — |
| `a2_exponential_and_logarithmic_expressions_graphing_logarithmic_functions` | Graphing logarithmic functions | no | other | — |
| `a2_exponential_and_logarithmic_expressions_discrete_exponential_growth_and_decay_word_problems` | Discrete exponential growth and decay word problems | no | wp | `exponential_growth_decay` |
| `a2_exponential_and_logarithmic_expressions_continuous_exponential_growth_and_decay_word_problems` | Continuous exponential growth and decay word problems | no | wp | `exponential_growth_decay` |
|  | **Algebra 2 — Conic Sections** |  |  |  |
| `a2_conic_sections_parabolas_graphing_and_properties` | Parabolas graphing & properties | no | other | — |
| `a2_conic_sections_parabolas_writing_equations` | Parabolas writing equations | no | solve | — |
| `a2_conic_sections_circles_graphing_and_properties` | Circles graphing & properties | no | other | — |
| `a2_conic_sections_circles_writing_equations` | Circles writing equations | no | solve | — |
| `a2_conic_sections_ellipses_graphing_and_properties` | Ellipses graphing & properties | no | other | — |
| `a2_conic_sections_ellipses_writing_equations` | Ellipses writing equations | no | solve | — |
| `a2_conic_sections_hyperbolas_graphing_and_properties` | Hyperbolas graphing & properties | no | other | — |
| `a2_conic_sections_hyperbolas_writing_equations` | Hyperbolas writing equations | no | solve | — |
| `a2_conic_sections_classifying` | Classifying | no | other | — |
| `a2_conic_sections_systems_of_quadratic_equations` | Systems of quadratic equations | no | solve | — |
|  | **Algebra 2 — Sequences and Series** |  |  |  |
| `a2_sequences_and_series_general_sequences` | General sequences | no | other | — |
| `a2_sequences_and_series_arithmetic_sequences` | Arithmetic sequences | no | other | — |
| `a2_sequences_and_series_geometric_sequences` | Geometric sequences | no | other | — |
| `a2_sequences_and_series_arithmetic_and_geometric_mean` | Arithmetic and geometric mean | no | other | — |
| `a2_sequences_and_series_general_series` | General series | no | other | — |
| `a2_sequences_and_series_arithmetic_series` | Arithmetic series | no | other | — |
| `a2_sequences_and_series_geometric_series` | Geometric series | no | other | — |
|  | **Algebra 2 — Matrices** |  |  |  |
| `a2_matrices_operations` | Operations | no | other | — |
| `a2_matrices_determinants` | Determinants | no | other | — |
| `a2_matrices_inverses` | Inverses | no | other | — |
| `a2_matrices_cramers_rule` | Cramer's Rule | no | other | — |
| `a2_matrices_equations` | Equations | no | solve | — |
| `a2_matrices_geometric_transformations` | Geometric transformations | no | other | — |
|  | **Algebra 2 — Complex Numbers** |  |  |  |
| `a2_complex_numbers_operations` | Operations | no | other | — |
| `a2_complex_numbers_graphing` | Graphing | no | other | — |
| `a2_complex_numbers_absolute_value` | Absolute value | no | solve | — |
| `a2_complex_numbers_rationalizing_denominators` | Rationalizing denominators | no | other | — |
|  | **Algebra 2 — Trigonometry** |  |  |  |
| `a2_trigonometry_angles_and_angle_measure` | Angles and angle measure | no | geometry | — |
| `a2_trigonometry_radians_and_degrees` | Radians and degrees | no | geometry | — |
| `a2_trigonometry_degrees_and_degrees_minutes_seconds` | Degrees and degrees-minutes-seconds | no | geometry | — |
| `a2_trigonometry_coterminal_angles` | Coterminal angles | no | geometry | — |
| `a2_trigonometry_arc_length_and_sector_area` | Arc length and sector area | no | geometry | — |
| `a2_trigonometry_right_triangle_trig_finding_ratios` | Right triangle trig, finding ratios | no | geometry | `finding_sine_cosine_tangent` |
| `a2_trigonometry_right_triangle_trig_finding_angle_measures` | Right triangle trig, finding angle measures | no | geometry | — |
| `a2_trigonometry_right_triangle_trig_angles_and_sides` | Right triangle trig, angles and sides | no | geometry | — |
| `a2_trigonometry_trig_functions_of_any_angle` | Trig functions of any angle | no | geometry | — |
| `a2_trigonometry_the_law_of_sines` | Law of Sines | no | geometry | — |
| `a2_trigonometry_the_law_of_cosines` | Law of Cosines | no | geometry | — |
| `a2_trigonometry_area_and_laws_of_sines_and_cosines` | Area and Laws | no | geometry | — |
| `a2_trigonometry_graphing_trig_functions` | Graphing trig functions | no | geometry | — |
| `a2_trigonometry_angle_sum_difference_identities` | Angle sum/difference identities | no | geometry | — |
| `a2_trigonometry_double_angle_half_angle_identities` | Double-angle/half-angle identities | no | geometry | — |
| `a2_trigonometry_equations` | Equations | no | solve | — |
|  | **Algebra 2 — Probability and Statistics** |  |  |  |
| `a2_probability_and_statistics_sample_spaces_and_the_fundamental_counting_principle` | Sample spaces and the Fundamental Counting Principle | no | other | — |
| `a2_probability_and_statistics_probability_of_independent_and_dependent_events_word_problems` | Probability of independent and dependent events, word problems | no | wp | — |
| `a2_probability_and_statistics_probability_of_independent_and_dependent_events` | Probability of independent and dependent events | no | other | — |
| `a2_probability_and_statistics_probability_of_mutually_exclusive_events_word_problems` | Probability of mutually exclusive events, word problems | no | wp | — |
| `a2_probability_and_statistics_probability_of_mutually_exclusive_events` | Probability of mutually exclusive events | no | other | — |
| `a2_probability_and_statistics_permutations` | Permutations | no | other | — |
| `a2_probability_and_statistics_combinations` | Combinations | no | other | — |
| `a2_probability_and_statistics_permutations_vs_combinations` | Permutations vs combinations | no | other | — |
| `a2_probability_and_statistics_probability_with_permutations_and_combinations` | Probability with permutations and combinations | no | other | — |
|  | **Algebra 2 — Direct and Inverse Variation** |  |  |  |
| `a2_direct_and_inverse_variation_direct_and_inverse_variation` | Direct and inverse variation | no | other | `direct_inverse_variation` |
|  | **Algebra 2 — General Functions** |  |  |  |
| `a2_general_functions_evaluating` | Evaluating | no | other | — |
| `a2_general_functions_operations` | Operations | no | other | — |
| `a2_general_functions_inverses` | Inverses | no | other | — |

## Appendix — not extra catalog leaves

### Generator keys that differ from catalog `id`

| type_id | generator |
|---|---|
| `a2_beginning_algebra_order_of_operations` | `order_of_operations` |
| `a2_beginning_algebra_simplifying_algebraic_expressions` | `expand_simplify` |
| `a2_equations_and_inequalities_multi_step_equations` | `multi_step_equations` |
| `a2_equations_and_inequalities_literal_equations` | `literal_equations` |
| `a2_equations_and_inequalities_work_word_problems` | `wp_work` |
| `a2_equations_and_inequalities_distance_rate_time_word_problems` | `wp_distance_rate_time` |
| `a2_equations_and_inequalities_mixture_word_problems` | `wp_mixture` |
| `a2_equations_and_inequalities_absolute_value_equations` | `absolute_value_equations` |
| `a2_equations_and_inequalities_multi_step_inequalities` | `multi_step_inequalities` |
| `a2_equations_and_inequalities_compound_inequalities` | `compound_inequalities` |
| `a2_equations_and_inequalities_absolute_value_inequalities` | `absolute_value_inequalities` |
| `a2_relations_and_introduction_to_functions_discrete_relations` | `discrete_relations` |
| `a2_relations_and_introduction_to_functions_continuous_relations` | `continuous_relations` |
| `a2_relations_and_introduction_to_functions_evaluating_and_graphing_functions` | `evaluating_graphing_functions` |
| `a2_linear_relations_and_functions_graphing_linear_equations` | `graph_linear_equation` |
| `a2_linear_relations_and_functions_writing_linear_equations` | `writing_linear_equations` |
| `a2_linear_relations_and_functions_graphing_absolute_value_equations` | `graph_absolute_value` |
| `a2_linear_relations_and_functions_graphing_linear_inequalities` | `graph_linear_inequality` |
| `a2_direct_and_inverse_variation_direct_and_inverse_variation` | `direct_inverse_variation` |
| `a2_systems_of_equations_and_inequalities_graphing_systems_of_linear_inequalities` | `graph_system_inequalities` |
| `a2_systems_of_equations_and_inequalities_solving_systems_by_graphing_2_variables` | `graph_system` |
| `a2_systems_of_equations_and_inequalities_solving_systems_by_elimination_2_variables` | `systems_elimination` |
| `a2_systems_of_equations_and_inequalities_solving_systems_by_substitution_2_variables` | `systems_substitution` |
| `a2_systems_of_equations_and_inequalities_systems_of_equations_word_problems_2_variables` | `wp_systems` |
| `a2_systems_of_equations_and_inequalities_points_in_three_dimensions` | `points_three_dimensions` |
| `a2_systems_of_equations_and_inequalities_planes` | `planes` |
| `a2_systems_of_equations_and_inequalities_solving_systems_with_three_variables` | `system_three_variables` |
| `a2_matrices_operations` | `matrix_operations` |
| `a2_matrices_determinants` | `matrix_operations` |
| `a2_matrices_inverses` | `matrix_inverse` |
| `a2_matrices_cramers_rule` | `matrix_cramers_rule` |
| `a2_matrices_equations` | `matrix_operations` |
| `a2_matrices_geometric_transformations` | `matrix_transformation` |
| `a2_complex_numbers_operations` | `complex_operations` |
| `a2_complex_numbers_graphing` | `complex_graph` |
| `a2_complex_numbers_absolute_value` | `complex_absolute_value` |
| `a2_complex_numbers_rationalizing_denominators` | `complex_rationalize_denominator` |
| `a2_quadratic_functions_and_inequalities_graphing_quadratic_functions` | `quadratic_graph_vertex` |
| `a2_quadratic_functions_and_inequalities_graphing_quadratic_inequalities` | `quadratic_graph_inequality` |
| `a2_quadratic_functions_and_inequalities_solving_equations_by_graphing` | `solve_polynomial_by_graphing` |
| `a2_quadratic_functions_and_inequalities_factoring_quadratic_expressions` | `quadratic_factoring` |
| `a2_quadratic_functions_and_inequalities_factoring_special_case_quadratic_expressions` | `polynomial_factoring_special_cases` |
| `a2_quadratic_functions_and_inequalities_solving_equations_by_taking_square_roots` | `quadratic_square_roots` |
| `a2_quadratic_functions_and_inequalities_solving_equations_by_factoring` | `quadratic_factoring_equations` |
| `a2_quadratic_functions_and_inequalities_completing_the_square` | `quadratic_completing_square_constant` |
| `a2_quadratic_functions_and_inequalities_solving_equations_by_completing_the_square` | `quadratic_completing_square_solve` |
| `a2_quadratic_functions_and_inequalities_solving_equations_with_the_quadratic_formula` | `quadratic_formula` |
| `a2_quadratic_functions_and_inequalities_the_discriminant` | `quadratic_discriminant` |
| `a2_polynomial_functions_naming` | `polynomial_naming` |
| `a2_polynomial_functions_simplifying` | `simplify_polynomials` |
| `a2_polynomial_functions_adding_and_subtracting` | `polynomial_add_subtract` |
| `a2_polynomial_functions_multiplying` | `polynomial_multiply` |
| `a2_polynomial_functions_multiplying_special_cases` | `polynomial_multiply_special` |
| `a2_polynomial_functions_the_binomial_theorem` | `binomial_theorem` |
| `a2_polynomial_functions_dividing` | `polynomial_long_division` |
| `a2_polynomial_functions_factoring_by_grouping` | `polynomial_factoring_grouping` |
| `a2_polynomial_functions_the_remainder_theorem` | `remainder_theorem` |
| `a2_polynomial_functions_writing_functions` | `polynomial_writing` |
| `a2_polynomial_functions_conjugate_roots_and_factoring` | `polynomial_factoring_special_cases` |
| `a2_polynomial_functions_conjugate_roots_and_writing_functions` | `polynomial_conjugate_writing` |
| `a2_polynomial_functions_descartes_rule_of_signs` | `descartes_rule_of_signs` |
| `a2_polynomial_functions_rational_zero_root_theorem` | `rational_zero_root_theorem` |
| `a2_polynomial_functions_fundamental_theorem_of_algebra` | `fundamental_theorem_algebra` |
| `a2_polynomial_functions_solving_polynomial_equations` | `quadratic_factoring_equations` |
| `a2_polynomial_functions_end_behavior_and_general_graph_shape` | `polynomial_end_behavior` |
| `a2_polynomial_functions_graphing` | `graph_quadratic` |
| `a2_general_functions_evaluating` | `function_evaluate` |
| `a2_general_functions_operations` | `function_operations` |
| `a2_general_functions_inverses` | `inverse_function_basic` |
| `a2_radical_functions_and_rational_exponents_simplifying_radicals` | `radical_simplification` |
| `a2_radical_functions_and_rational_exponents_adding_and_subtracting_radical_expressions` | `radical_add_subtract` |
| `a2_radical_functions_and_rational_exponents_multiplying_radical_expressions` | `radical_multiply` |
| `a2_radical_functions_and_rational_exponents_dividing_radical_expressions` | `radical_divide` |
| `a2_radical_functions_and_rational_exponents_connecting_radical_expressions_and_rational_exponents` | `properties_of_exponents` |
| `a2_radical_functions_and_rational_exponents_evaluating_rational_exponent_expressions` | `properties_of_exponents` |
| `a2_radical_functions_and_rational_exponents_the_properties_of_exponents` | `properties_of_exponents` |
| `a2_radical_functions_and_rational_exponents_radical_equations` | `radical_equations` |
| `a2_radical_functions_and_rational_exponents_rational_exponent_equations` | `radical_equations` |
| `a2_radical_functions_and_rational_exponents_graphing_radical_equations` | `graph_radical` |
| `a2_radical_functions_and_rational_exponents_domain_and_range_of_radical_functions` | `radical_domain_range` |
| `a2_conic_sections_parabolas_graphing_and_properties` | `quadratic_graph_vertex` |
| `a2_conic_sections_parabolas_writing_equations` | `quadratic_vertex_form_write` |
| `a2_conic_sections_circles_graphing_and_properties` | `conic_sections` |
| `a2_conic_sections_circles_writing_equations` | `conic_sections` |
| `a2_conic_sections_ellipses_graphing_and_properties` | `conic_sections` |
| `a2_conic_sections_ellipses_writing_equations` | `conic_sections` |
| `a2_conic_sections_hyperbolas_graphing_and_properties` | `conic_sections` |
| `a2_conic_sections_hyperbolas_writing_equations` | `conic_sections` |
| `a2_conic_sections_classifying` | `conic_sections` |
| `a2_conic_sections_systems_of_quadratic_equations` | `quadratic_system` |
| `a2_rational_expressions_graphing` | `graph_rational` |
| `a2_rational_expressions_simplifying` | `rational_simplification` |
| `a2_rational_expressions_multiplying_and_dividing` | `rational_expression_multiply_divide` |
| `a2_rational_expressions_adding_and_subtracting` | `rational_expression_simplification` |
| `a2_rational_expressions_complex_fractions` | `complex_fractions` |
| `a2_rational_expressions_equations` | `rational_equations` |
| `a2_exponential_and_logarithmic_expressions_graphing_exponential_functions` | `graph_exponential` |
| `a2_exponential_and_logarithmic_expressions_exponential_equations_not_requiring_logarithms` | `exponential_equation_simple` |
| `a2_exponential_and_logarithmic_expressions_exponents_and_logarithms` | `log_evaluate` |
| `a2_exponential_and_logarithmic_expressions_evaluating_logarithms` | `log_evaluate` |
| `a2_exponential_and_logarithmic_expressions_logarithms_and_exponents_as_inverses` | `log_evaluate` |
| `a2_exponential_and_logarithmic_expressions_properties_of_logarithms` | `log_change_of_base` |
| `a2_exponential_and_logarithmic_expressions_writing_logs_in_terms_of_others` | `log_change_of_base` |
| `a2_exponential_and_logarithmic_expressions_exponential_equations_requiring_logarithms` | `exponential_equation_with_log` |
| `a2_exponential_and_logarithmic_expressions_inverses_of_exponential_and_logarithmic_functions` | `inverse_exponential_logarithmic` |
| `a2_exponential_and_logarithmic_expressions_logarithmic_equations_simple` | `log_equation_simple` |
| `a2_exponential_and_logarithmic_expressions_logarithmic_equations_hard` | `log_equation_simple` |
| `a2_exponential_and_logarithmic_expressions_graphing_logarithmic_functions` | `graph_logarithmic` |
| `a2_exponential_and_logarithmic_expressions_discrete_exponential_growth_and_decay_word_problems` | `exponential_growth_decay` |
| `a2_exponential_and_logarithmic_expressions_continuous_exponential_growth_and_decay_word_problems` | `exponential_growth_decay` |
| `a2_sequences_and_series_general_sequences` | `sequence_arithmetic_nth_term` |
| `a2_sequences_and_series_arithmetic_sequences` | `sequence_arithmetic_nth_term` |
| `a2_sequences_and_series_geometric_sequences` | `sequence_geometric_nth_term` |
| `a2_sequences_and_series_arithmetic_and_geometric_mean` | `sequence_arithmetic_geometric_mean` |
| `a2_sequences_and_series_general_series` | `sequence_arithmetic_series` |
| `a2_sequences_and_series_arithmetic_series` | `sequence_arithmetic_series` |
| `a2_sequences_and_series_geometric_series` | `sequence_geometric_series` |
| `a2_trigonometry_angles_and_angle_measure` | `angle_measure` |
| `a2_trigonometry_radians_and_degrees` | `trig_unit_circle` |
| `a2_trigonometry_degrees_and_degrees_minutes_seconds` | `degrees_minutes_seconds` |
| `a2_trigonometry_coterminal_angles` | `trig_unit_circle` |
| `a2_trigonometry_arc_length_and_sector_area` | `geo_arc_sector` |
| `a2_trigonometry_right_triangle_trig_finding_ratios` | `geo_right_triangle_trig_ratio` |
| `a2_trigonometry_right_triangle_trig_finding_angle_measures` | `geo_right_triangle_trig_angle` |
| `a2_trigonometry_right_triangle_trig_angles_and_sides` | `geo_right_triangle_trig` |
| `a2_trigonometry_trig_functions_of_any_angle` | `trig_evaluate` |
| `a2_trigonometry_the_law_of_sines` | `law_of_sines` |
| `a2_trigonometry_the_law_of_cosines` | `law_of_cosines` |
| `a2_trigonometry_area_and_laws_of_sines_and_cosines` | `law_of_sines` |
| `a2_trigonometry_graphing_trig_functions` | `graphing_trig_functions` |
| `a2_trigonometry_angle_sum_difference_identities` | `trig_sum_difference` |
| `a2_trigonometry_double_angle_half_angle_identities` | `trig_multiple_angle` |
| `a2_trigonometry_equations` | `simple_trig_equations` |
| `a2_probability_and_statistics_sample_spaces_and_the_fundamental_counting_principle` | `stats_counting_principle` |
| `a2_probability_and_statistics_probability_of_independent_and_dependent_events_word_problems` | `stats_probability_compound_independent` |
| `a2_probability_and_statistics_probability_of_independent_and_dependent_events` | `stats_probability_compound_independent` |
| `a2_probability_and_statistics_probability_of_mutually_exclusive_events_word_problems` | `stats_probability_mutually_exclusive` |
| `a2_probability_and_statistics_probability_of_mutually_exclusive_events` | `stats_probability_mutually_exclusive` |
| `a2_probability_and_statistics_permutations` | `stats_permutations` |
| `a2_probability_and_statistics_combinations` | `stats_combinations` |
| `a2_probability_and_statistics_permutations_vs_combinations` | `stats_permutations_vs_combinations` |
| `a2_probability_and_statistics_probability_with_permutations_and_combinations` | `stats_permutations_vs_combinations` |

### `QUESTION_TYPES` vs catalog

Every Algebra 2 catalog `id` is registered in `QUESTION_TYPES`.

Per-type notes: copy `_TEMPLATE.md` → `notes/<gallery-slug>.md` (or
`<type_id>.md` / `<slug>/NOTES.md`). Process: `.cursor/rules/topic-notes-process.mdc`.
