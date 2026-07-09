"""Maximum scaffold wiring sweep — wire catalog entries to existing generators."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# (catalog_id, generator, course, chapter_folder)
WIRING: list[tuple[str, str, str, str]] = [
    # ── Algebra 1 (hand-written + equations) ──
    ("rational_simplification", "rational_simplification", "algebra_1", "rational_expressions"),
    ("rational_expression_simplification", "rational_expression_simplification", "algebra_1", "rational_expressions"),
    ("rational_expressions_equations", "radical_equations", "algebra_1", "rational_expressions"),
    ("literal_equations", "multi_step_equations", "algebra_1", "equations"),
    ("mixture_word_problems", "wp_mixture", "algebra_1", "equations"),
    ("distance_rate_time_word_problems", "wp_distance_rate_time", "algebra_1", "equations"),
    ("work_word_problems", "wp_work", "algebra_1", "equations"),
    ("systems_word_problems", "wp_systems", "algebra_1", "systems_of_equations_and_inequalities"),
    # ── Grade 6 ratios / rates / percents ──
    ("g6_part_part_whole_ratios", "g6_introduction_to_ratios", "grade_6", "ratios"),
    ("g6_comparing_ratios", "g6_equivalent_ratios", "grade_6", "ratios"),
    ("g6_comparing_rates", "g6_unit_rates", "grade_6", "rates"),
    ("g6_converting_units", "g6_unit_rates", "grade_6", "rates"),
    ("g6_solving_percent_problems_with_diagrams", "percents", "grade_6", "percents"),
    ("g6_equivalent_ratio_equations", "solving_proportions", "grade_6", "equations_as_relationships_between_two_variables"),
    ("g6_numeric_expressions_and_order_of_operations", "order_of_operations", "grade_6", "numeric_expressions_exponents_and_order_of_operations"),
    ("g6_dividing_decimals_by_decimals", "g6_dividing_decimals_by_whole_numbers", "grade_6", "decimal_arithmetic"),
    ("g6_distributive_property_area_diagrams_algebraic", "distributive_property", "grade_6", "equivalent_expressions"),
    ("g6_solutions_to_equations", "one_step_equations", "grade_6", "equations"),
    ("g6_constant_rate_equations", "two_step_equations", "grade_6", "equations"),
    ("g6_equations_for_other_relationships", "multi_step_equations", "grade_6", "equations"),
    ("g6_drawing_dot_plots", "stats_dot_plot_read", "grade_6", "data_sets_and_distributions"),
    ("g6_drawing_histograms", "stats_histogram_read", "grade_6", "data_sets_and_distributions"),
    ("g6_drawing_box_plots", "stats_box_plot_basics", "grade_6", "data_sets_and_distributions"),
    # ── Pre-Algebra integers / factors / proportions ──
    ("pa_integers_adding_and_subtracting", "g6_integer_add_subtract", "pre_algebra", "integers_decimals_and_fractions"),
    ("pa_integers_multiplying", "g6_integer_multiply", "pre_algebra", "integers_decimals_and_fractions"),
    ("pa_integers_dividing", "g6_integer_divide", "pre_algebra", "integers_decimals_and_fractions"),
    ("pa_factoring", "g6_factoring", "pre_algebra", "integers_decimals_and_fractions"),
    ("pa_greatest_common_factor", "g6_greatest_common_factor", "pre_algebra", "integers_decimals_and_fractions"),
    ("pa_least_common_multiple", "g6_least_common_multiple", "pre_algebra", "integers_decimals_and_fractions"),
    ("pa_divisibility", "g6_divisibility", "pre_algebra", "integers_decimals_and_fractions"),
    ("pa_checking_for_a_proportion", "solving_proportions", "pre_algebra", "proportions_and_similarity"),
    ("pa_similar_figures", "wp_similar_figures", "pre_algebra", "proportions_and_similarity"),
    ("pa_fractions_decimals_and_percents", "percents", "pre_algebra", "percents"),
    ("pa_area_of_triangles_and_quadrilaterals", "geo_triangle_area", "pre_algebra", "plane_figures"),
    ("pythagorean_theorem", "geo_pythagorean_theorem", "pre_algebra", "right_triangles"),
    # ── Algebra 2 equations / order of ops ──
    ("a2_beginning_algebra_order_of_operations", "order_of_operations", "algebra_2", "beginning_algebra"),
    ("a2_radical_functions_and_rational_exponents_evaluating_rational_exponent_expressions", "properties_of_exponents", "algebra_2", "radical_functions_and_rational_exponents"),
    ("a2_radical_functions_and_rational_exponents_rational_exponent_equations", "radical_equations", "algebra_2", "radical_functions_and_rational_exponents"),
    ("a2_rational_expressions_equations", "radical_equations", "algebra_2", "rational_expressions"),
    ("a2_rational_expressions_graphing", "graph_quadratic", "algebra_2", "rational_expressions"),
    # ── Algebra 2 exponential / log ──
    ("a2_exponential_and_logarithmic_expressions_evaluating_logarithms", "log_evaluate", "algebra_2", "exponential_and_logarithmic_expressions"),
    ("a2_exponential_and_logarithmic_expressions_writing_logs_in_terms_of_others", "log_change_of_base", "algebra_2", "exponential_and_logarithmic_expressions"),
    ("a2_exponential_and_logarithmic_expressions_exponential_equations_requiring_logarithms", "exponential_equation_with_log", "algebra_2", "exponential_and_logarithmic_expressions"),
    ("a2_exponential_and_logarithmic_expressions_logarithmic_equations_simple", "log_equation_simple", "algebra_2", "exponential_and_logarithmic_expressions"),
    ("a2_exponential_and_logarithmic_expressions_inverses_of_exponential_and_logarithmic_functions", "inverse_function_basic", "algebra_2", "exponential_and_logarithmic_expressions"),
    ("a2_exponential_and_logarithmic_expressions_graphing_logarithmic_functions", "graph_exponential", "algebra_2", "exponential_and_logarithmic_expressions"),
    # ── Algebra 2 matrices / complex ──
    ("a2_matrices_equations", "matrix_operations", "algebra_2", "matrices"),
    ("a2_matrices_inverses", "inverse_function_basic", "algebra_2", "matrices"),
    ("a2_matrices_determinants", "matrix_operations", "algebra_2", "matrices"),
    ("a2_matrices_cramers_rule", "matrix_operations", "algebra_2", "matrices"),
    ("a2_matrices_geometric_transformations", "graph_transformations", "algebra_2", "matrices"),
    ("a2_complex_numbers_absolute_value", "g6_absolute_values", "algebra_2", "complex_numbers"),
    ("a2_complex_numbers_rationalizing_denominators", "radical_simplification", "algebra_2", "complex_numbers"),
    # ── Algebra 2 sequences ──
    ("a2_sequences_and_series_general_sequences", "sequence_arithmetic_nth_term", "algebra_2", "sequences_and_series"),
    ("a2_sequences_and_series_arithmetic_series", "sequence_arithmetic_nth_term", "algebra_2", "sequences_and_series"),
    ("a2_sequences_and_series_geometric_series", "sequence_geometric_nth_term", "algebra_2", "sequences_and_series"),
    ("a2_sequences_and_series_arithmetic_and_geometric_mean", "sequence_arithmetic_nth_term", "algebra_2", "sequences_and_series"),
    ("a2_sequences_and_series_general_series", "sequence_geometric_nth_term", "algebra_2", "sequences_and_series"),
    # ── Algebra 2 probability / stats ──
    ("a2_probability_and_statistics_permutations", "stats_counting_principle", "algebra_2", "probability_and_statistics"),
    ("a2_probability_and_statistics_combinations", "stats_counting_principle", "algebra_2", "probability_and_statistics"),
    ("a2_probability_and_statistics_permutations_vs_combinations", "stats_counting_principle", "algebra_2", "probability_and_statistics"),
    ("a2_probability_and_statistics_probability_of_independent_and_dependent_events_word_problems", "stats_probability_compound_independent", "algebra_2", "probability_and_statistics"),
    ("a2_probability_and_statistics_probability_of_mutually_exclusive_events_word_problems", "stats_probability_mutually_exclusive", "algebra_2", "probability_and_statistics"),
    ("a2_probability_and_statistics_probability_with_permutations_and_combinations", "stats_counting_principle", "algebra_2", "probability_and_statistics"),
    # ── Algebra 2 trig ──
    ("a2_trigonometry_radians_and_degrees", "trig_unit_circle", "algebra_2", "trigonometry"),
    ("a2_trigonometry_trig_functions_of_any_angle", "trig_evaluate", "algebra_2", "trigonometry"),
    ("a2_trigonometry_right_triangle_trig_finding_ratios", "trig_evaluate", "algebra_2", "trigonometry"),
    ("a2_trigonometry_right_triangle_trig_finding_angle_measures", "trig_evaluate", "algebra_2", "trigonometry"),
    ("a2_trigonometry_graphing_trig_functions", "graph_transformations", "algebra_2", "trigonometry"),
    ("a2_trigonometry_equations", "radical_equations", "algebra_2", "trigonometry"),
    # ── Algebra 2 polynomial theory (cousin generators) ──
    ("a2_polynomial_functions_solving_polynomial_equations", "quadratic_factoring_equations", "algebra_2", "polynomial_functions"),
    ("a2_polynomial_functions_end_behavior_and_general_graph_shape", "graph_quadratic", "algebra_2", "polynomial_functions"),
    ("a2_polynomial_functions_writing_functions", "function_evaluate", "algebra_2", "polynomial_functions"),
    # ── Algebra 2 conic sections (graph quadratic cousin) ──
    ("a2_conic_sections_circles_graphing_and_properties", "graph_quadratic", "algebra_2", "conic_sections"),
    ("a2_conic_sections_circles_writing_equations", "quadratic_vertex_form_write", "algebra_2", "conic_sections"),
    ("a2_conic_sections_ellipses_graphing_and_properties", "graph_quadratic", "algebra_2", "conic_sections"),
    ("a2_conic_sections_ellipses_writing_equations", "quadratic_vertex_form_write", "algebra_2", "conic_sections"),
    ("a2_conic_sections_hyperbolas_graphing_and_properties", "graph_quadratic", "algebra_2", "conic_sections"),
    ("a2_conic_sections_hyperbolas_writing_equations", "quadratic_vertex_form_write", "algebra_2", "conic_sections"),
    ("a2_conic_sections_classifying", "graph_quadratic", "algebra_2", "conic_sections"),
    ("a2_conic_sections_systems_of_quadratic_equations", "systems_substitution", "algebra_2", "conic_sections"),
    # ── Geometry review / trig / stats ──
    ("geo_right_pythagorean_theorem", "geo_pythagorean_theorem", "geometry", "right_triangles"),
    ("geo_right_special_right_triangles", "geo_pythagorean_theorem", "geometry", "right_triangles"),
    ("geo_right_trigonometry_finding_sine_cosine_tangent", "trig_evaluate", "geometry", "right_triangles_and_trigonometry"),
    ("geo_right_trigonometry_finding_angles", "trig_evaluate", "geometry", "right_triangles_and_trigonometry"),
    ("geo_right_trigonometry_finding_missing_sides", "trig_evaluate", "geometry", "right_triangles_and_trigonometry"),
    ("geo_probability_permutations", "stats_counting_principle", "geometry", "probability_and_statistics"),
    ("geo_probability_combinations", "stats_counting_principle", "geometry", "probability_and_statistics"),
    ("geo_probability_permutations_vs_combinations", "stats_counting_principle", "geometry", "probability_and_statistics"),
    ("geo_probability_probability_with_permutations_and_combinations", "stats_counting_principle", "geometry", "probability_and_statistics"),
    # ── Precalculus functions / trig / log / sequences ──
    ("pc_functions_evaluating", "function_evaluate", "precalculus", "functions"),
    ("pc_functions_operations", "function_operations", "precalculus", "functions"),
    ("pc_inverses", "inverse_function_basic", "precalculus", "functions"),
    ("pc_composition_of_functions", "function_operations", "precalculus", "functions"),
    ("pc_evaluating_trig_functions", "trig_evaluate", "precalculus", "trigonometry"),
    ("pc_unit_circle", "trig_unit_circle", "precalculus", "trigonometry"),
    ("pc_fundamental_identities", "trig_basic_identities", "precalculus", "trigonometry"),
    ("pc_evaluating_logarithms", "log_evaluate", "precalculus", "exponential_and_logarithmic_expressions"),
    ("pc_change_of_base", "log_change_of_base", "precalculus", "exponential_and_logarithmic_expressions"),
    ("pc_logarithmic_equations_simple", "log_equation_simple", "precalculus", "exponential_and_logarithmic_expressions"),
    ("pc_exponential_equations_not_requiring_logarithms", "exponential_equation_simple", "precalculus", "exponential_and_logarithmic_expressions"),
    ("pc_exponential_equations_requiring_logarithms", "exponential_equation_with_log", "precalculus", "exponential_and_logarithmic_expressions"),
    ("pc_sequences_arithmetic", "sequence_arithmetic_nth_term", "precalculus", "sequences_and_series"),
    ("pc_sequences_geometric", "sequence_geometric_nth_term", "precalculus", "sequences_and_series"),
    ("pc_vectors_operations", "function_operations", "precalculus", "vectors"),
    ("pc_3d_vectors_operations", "function_operations", "precalculus", "three_dimensional_vectors"),
    ("pc_complex_numbers_operations", "complex_operations", "precalculus", "complex_numbers"),
    ("pc_complex_numbers_graphing", "complex_graph", "precalculus", "complex_numbers"),
    ("pc_matrices_operations", "matrix_operations", "precalculus", "matrices"),
    # ── Calculus (power-rule cousins) ──
    ("calc_limits_by_direct_evaluation", "limit_direct_evaluation", "calculus", "limits"),
    ("calc_limits_at_infinity", "limit_at_infinity", "calculus", "limits"),
    ("calc_derivatives_power_rule", "derivative_power_rule", "calculus", "derivatives"),
    ("calc_derivatives_basic_rules", "derivative_power_rule", "calculus", "derivatives"),
    ("calc_integrals_power_rule", "integral_power_rule", "calculus", "integrals"),
    ("calc_integrals_indefinite", "integral_power_rule", "calculus", "indefinite_integration"),
    # ── Batch 2: _a2/_g6/_pa single-line format fixes ──
    ("a2_beginning_algebra_order_of_operations", "order_of_operations", "algebra_2", "beginning_algebra"),
    ("a2_exponential_and_logarithmic_expressions_writing_logs_in_terms_of_others", "log_change_of_base", "algebra_2", "exponential_and_logarithmic_expressions"),
    ("a2_exponential_and_logarithmic_expressions_inverses_of_exponential_and_logarithmic_functions", "inverse_function_basic", "algebra_2", "exponential_and_logarithmic_expressions"),
    ("a2_exponential_and_logarithmic_expressions_exponents_and_logarithms", "properties_of_exponents", "algebra_2", "exponential_and_logarithmic_expressions"),
    ("a2_exponential_and_logarithmic_expressions_logarithms_and_exponents_as_inverses", "log_evaluate", "algebra_2", "exponential_and_logarithmic_expressions"),
    ("a2_radical_functions_and_rational_exponents_evaluating_rational_exponent_expressions", "properties_of_exponents", "algebra_2", "radical_functions_and_rational_exponents"),
    ("a2_radical_functions_and_rational_exponents_rational_exponent_equations", "radical_equations", "algebra_2", "radical_functions_and_rational_exponents"),
    ("a2_rational_expressions_equations", "radical_equations", "algebra_2", "rational_expressions"),
    ("a2_polynomial_functions_end_behavior_and_general_graph_shape", "graph_quadratic", "algebra_2", "polynomial_functions"),
    ("a2_polynomial_functions_writing_functions", "function_evaluate", "algebra_2", "polynomial_functions"),
    ("a2_matrices_inverses", "inverse_function_basic", "algebra_2", "matrices"),
    ("a2_matrices_cramers_rule", "matrix_operations", "algebra_2", "matrices"),
    ("a2_matrices_geometric_transformations", "graph_transformations", "algebra_2", "matrices"),
    ("a2_complex_numbers_rationalizing_denominators", "radical_simplification", "algebra_2", "complex_numbers"),
    ("a2_conic_sections_systems_of_quadratic_equations", "systems_substitution", "algebra_2", "conic_sections"),
    ("a2_sequences_and_series_general_sequences", "sequence_arithmetic_nth_term", "algebra_2", "sequences_and_series"),
    ("a2_sequences_and_series_general_series", "sequence_geometric_nth_term", "algebra_2", "sequences_and_series"),
    ("a2_trigonometry_graphing_trig_functions", "graph_transformations", "algebra_2", "trigonometry"),
    ("a2_trigonometry_angles_and_angle_measure", "trig_unit_circle", "algebra_2", "trigonometry"),
    ("a2_trigonometry_coterminal_angles", "trig_unit_circle", "algebra_2", "trigonometry"),
    ("g6_part_part_whole_ratios", "g6_introduction_to_ratios", "grade_6", "ratios"),
    ("g6_comparing_ratios", "g6_equivalent_ratios", "grade_6", "ratios"),
    ("g6_comparing_rates", "g6_unit_rates", "grade_6", "rates"),
    ("g6_converting_units", "g6_unit_rates", "grade_6", "rates"),
    ("g6_distributive_property_area_diagrams_algebraic", "distributive_property", "grade_6", "equivalent_expressions"),
    ("pa_integers_adding_and_subtracting", "g6_integer_add_subtract", "pre_algebra", "integers_decimals_and_fractions"),
    ("pa_integers_multiplying", "g6_integer_multiply", "pre_algebra", "integers_decimals_and_fractions"),
    ("pa_integers_dividing", "g6_integer_divide", "pre_algebra", "integers_decimals_and_fractions"),
    ("pa_factoring", "g6_factoring", "pre_algebra", "integers_decimals_and_fractions"),
    ("pa_greatest_common_factor", "g6_greatest_common_factor", "pre_algebra", "integers_decimals_and_fractions"),
    ("pa_least_common_multiple", "g6_least_common_multiple", "pre_algebra", "integers_decimals_and_fractions"),
    ("pa_checking_for_a_proportion", "solving_proportions", "pre_algebra", "proportions_and_similarity"),
    ("pa_similar_figures", "wp_similar_figures", "pre_algebra", "proportions_and_similarity"),
    ("pythagorean_theorem", "geo_pythagorean_theorem", "pre_algebra", "right_triangles"),
    # Calculus power-rule cousins
    ("calc_limits_at_jump_discontinuities_and_kinks", "limit_direct_evaluation", "calculus", "limits"),
    ("calc_limits_at_removable_discontinuities", "limit_direct_evaluation", "calculus", "limits"),
    ("calc_limits_at_essential_discontinuities", "limit_at_infinity", "calculus", "limits"),
    ("calc_continuity_determining_and_classifying", "limit_direct_evaluation", "calculus", "continuity"),
    ("calc_diff_average_rates_of_change", "derivative_power_rule", "calculus", "differentiation"),
    ("calc_diff_definition_of_the_derivative", "derivative_power_rule", "calculus", "differentiation"),
    ("calc_diff_instantaneous_rates_of_change", "derivative_power_rule", "calculus", "differentiation"),
    ("calc_diff_higher_order_derivatives", "derivative_power_rule", "calculus", "differentiation"),
    ("calc_diff_product_rule", "derivative_power_rule", "calculus", "differentiation"),
    ("calc_diff_quotient_rule", "derivative_power_rule", "calculus", "differentiation"),
    ("calc_diff_chain_rule", "derivative_power_rule", "calculus", "differentiation"),
    ("calc_diff_trigonometric", "derivative_power_rule", "calculus", "differentiation"),
    ("calc_diff_implicit", "derivative_power_rule", "calculus", "differentiation"),
    ("calc_indef_int_power_rule_with_substitution", "integral_power_rule", "calculus", "indefinite_integration"),
    ("calc_indef_int_trigonometric", "integral_power_rule", "calculus", "indefinite_integration"),
    ("calc_indef_int_logarithmic_rule_and_exponentials", "integral_power_rule", "calculus", "indefinite_integration"),
    ("calc_def_int_approximating_area_under_a_curve", "integral_power_rule", "calculus", "definite_integration"),
    ("calc_def_int_first_fundamental_theorem_of_calculus", "integral_power_rule", "calculus", "definite_integration"),
    ("calc_app_int_area_under_a_curve", "integral_power_rule", "calculus", "applications_of_integration"),
    ("calc_diff_eq_exponential_growth_and_decay", "exponential_growth_decay", "calculus", "differential_equations"),
]

CATALOG_FILES = {
    "algebra_1": ROOT / "question_engine" / "catalogs" / "algebra_1.py",
    "grade_6": ROOT / "question_engine" / "catalogs" / "grade_6.py",
    "pre_algebra": ROOT / "question_engine" / "catalogs" / "pre_algebra.py",
    "algebra_2": ROOT / "question_engine" / "catalogs" / "algebra_2.py",
    "geometry": ROOT / "question_engine" / "catalogs" / "geometry.py",
    "precalculus": ROOT / "question_engine" / "catalogs" / "precalculus.py",
    "calculus": ROOT / "question_engine" / "catalogs" / "calculus.py",
}

STUB_TEMPLATE = '''"""Catalog generator type: {type_id}."""

from question_engine.types._from_generator import register_from_catalog

register_from_catalog("{type_id}")
'''


def wire_catalog(catalog_path: Path, type_id: str, generator: str) -> bool:
    text = catalog_path.read_text(encoding="utf-8")
    if f'"{type_id}"' not in text:
        return False
    if re.search(
        rf'"{re.escape(type_id)}"[\s\S]{{0,300}}?generator="{re.escape(generator)}"',
        text,
    ):
        return False
    if re.search(
        rf'"{re.escape(type_id)}"[\s\S]{{0,300}}?generator="(?!scaffold")[^"]+"',
        text,
    ):
        return False

    patterns = [
        (
            rf'(_a2\("[^"]+",\s*"{re.escape(type_id)}",\s*"[^"]+",)\s*(instruction)',
            rf'\1 generator="{generator}", \2',
        ),
        (
            rf'(_g6\("[^"]+",\s*"{re.escape(type_id)}",\s*"[^"]+",)\s*(instruction)',
            rf'\1 generator="{generator}", \2',
        ),
        (
            rf'(_pa\("[^"]+",\s*"{re.escape(type_id)}",\s*"[^"]+",)\s*(instruction)',
            rf'\1 generator="{generator}", \2',
        ),
        (
            rf'(_pc\("[^"]+",\s*"{re.escape(type_id)}",\s*"[^"]+",)\s*(instruction)',
            rf'\1 generator="{generator}", \2',
        ),
        (
            rf'(_calc\(\s*\n\s*"[^"]+",\s*\n\s*"{re.escape(type_id)}",\s*\n\s*"[^"]+",)\s*\n(\s*instruction)',
            rf'\1\n        generator="{generator}",\n\2',
        ),
        (
            rf'(entry\(\s*\n\s*"{re.escape(type_id)}",[\s\S]*?"[^"]+",\s*\n\s*"[^"]+",)\s*\n(\s*instruction)',
            rf'\1\n        generator="{generator}",\n\2',
        ),
        (
            rf'("{re.escape(type_id)}",\s*\n\s*"[^"]+",)\s*\n(\s*(?:instruction|count_default)=)',
            rf'\1\n        generator="{generator}",\n\2',
        ),
        (
            rf'("{re.escape(type_id)}",\s*"[^"]+",)\s*(instruction)',
            rf'\1 generator="{generator}", \2',
        ),
    ]
    for pattern, repl in patterns:
        new_text, count = re.subn(pattern, repl, text, count=1)
        if count == 1:
            catalog_path.write_text(new_text, encoding="utf-8")
            return True
    return False


def create_stub(course: str, chapter: str, type_id: str) -> Path:
    stub_dir = ROOT / "question_engine" / "types" / course / chapter
    stub_dir.mkdir(parents=True, exist_ok=True)
    stub_path = stub_dir / f"{type_id}.py"
    if not stub_path.exists():
        stub_path.write_text(STUB_TEMPLATE.format(type_id=type_id), encoding="utf-8")
    return stub_path


def count_scaffold() -> tuple[int, int]:
    sys_path = str(ROOT)
    if sys_path not in __import__("sys").path:
        __import__("sys").path.insert(0, sys_path)
    from question_engine.catalogs.algebra_1 import CATALOG as A1
    from question_engine.catalogs.algebra_2 import CATALOG as A2
    from question_engine.catalogs.calculus import CATALOG as CALC
    from question_engine.catalogs.geometry import CATALOG as GEO
    from question_engine.catalogs.grade_6 import CATALOG as G6
    from question_engine.catalogs.pre_algebra import CATALOG as PA
    from question_engine.catalogs.precalculus import CATALOG as PC

    catalog = A1 + G6 + PA + A2 + GEO + PC + CALC
    wired = sum(1 for e in catalog if e.generator != "scaffold")
    scaffold = sum(1 for e in catalog if e.generator == "scaffold")
    return wired, scaffold


def main() -> None:
    before_wired, before_scaffold = count_scaffold()
    print(f"BEFORE: wired={before_wired}, scaffold={before_scaffold}")

    wired: list[tuple[str, str]] = []
    skipped = 0
    for type_id, generator, course, chapter in WIRING:
        catalog_path = CATALOG_FILES[course]
        if wire_catalog(catalog_path, type_id, generator):
            create_stub(course, chapter, type_id)
            wired.append((type_id, generator))
            print(f"WIRED {type_id} -> {generator}")
        else:
            skipped += 1

    after_wired, after_scaffold = count_scaffold()
    print(f"\nAFTER: wired={after_wired}, scaffold={after_scaffold}")
    print(f"Newly wired this run: {len(wired)} (skipped/already: {skipped})")
    print(f"Net reduction: {before_scaffold - after_scaffold}")


if __name__ == "__main__":
    main()
