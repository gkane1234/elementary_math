"""Default setting-profile inheritance keyed by generator name."""

from __future__ import annotations

from .domains.rational import rational_expression_extra_settings, rational_operation_settings
from .resolve import TypeSettingConfig

_ENRICHMENT = "common_enrichment"


def _with_common_enrichment(config: TypeSettingConfig) -> TypeSettingConfig:
    inherits = config.inherits
    if _ENRICHMENT not in inherits:
        inherits = (_ENRICHMENT, *inherits)
    return TypeSettingConfig(
        setting_profile=config.setting_profile,
        inherits=inherits,
        exclude_settings=config.exclude_settings,
        include_settings=config.include_settings,
        extra_settings=config.extra_settings,
        setting_defaults=config.setting_defaults,
        count_default=config.count_default,
        count_max=config.count_max,
    )


_RAW_GENERATOR_SETTING_CONFIGS: dict[str, TypeSettingConfig] = {    # Equations
    "one_step_equations": TypeSettingConfig(setting_profile="equation"),
    "two_step_equations": TypeSettingConfig(
        setting_profile="equation",
        exclude_settings=("allow_multiply", "allow_divide"),
    ),
    "multi_step_equations": TypeSettingConfig(
        setting_profile="equation",
        exclude_settings=("allow_multiply", "allow_divide", "allow_add", "allow_subtract"),
    ),
    "absolute_value_equations": TypeSettingConfig(
        setting_profile="equation",
        exclude_settings=("allow_multiply", "allow_divide", "allow_add", "allow_subtract"),
    ),
    # Inequalities
    "one_step_inequalities": TypeSettingConfig(setting_profile="inequality"),
    "two_step_inequalities": TypeSettingConfig(setting_profile="inequality"),
    "multi_step_inequalities": TypeSettingConfig(setting_profile="inequality"),
    "compound_inequalities": TypeSettingConfig(
        setting_profile="inequality",
        exclude_settings=("steps",),
    ),
    "absolute_value_inequalities": TypeSettingConfig(
        setting_profile="inequality",
        exclude_settings=("steps",),
    ),
    # Numbers
    "rational_add_subtract": TypeSettingConfig(setting_profile="rational"),
    "rational_multiply": TypeSettingConfig(setting_profile="rational"),
    "rational_divide": TypeSettingConfig(setting_profile="rational"),
    "percents": TypeSettingConfig(setting_profile="percent"),
    "percent_of_change": TypeSettingConfig(setting_profile="percent"),
    "solving_proportions": TypeSettingConfig(setting_profile="proportion"),
    "scientific_notation_write": TypeSettingConfig(setting_profile="scientific_notation"),
    "scientific_notation_operations": TypeSettingConfig(setting_profile="scientific_notation"),
    "scientific_notation_add_subtract": TypeSettingConfig(setting_profile="scientific_notation"),
    "g6_introduction_to_ratios": TypeSettingConfig(setting_profile="ratio"),
    "g6_equivalent_ratios": TypeSettingConfig(setting_profile="ratio"),
    "g6_unit_rates": TypeSettingConfig(setting_profile="unit_rate"),
    "g6_decimal_addition": TypeSettingConfig(setting_profile="decimal"),
    "g6_decimal_subtraction": TypeSettingConfig(setting_profile="decimal"),
    "g6_decimal_multiplication": TypeSettingConfig(setting_profile="decimal"),
    "g6_fraction_add_like": TypeSettingConfig(setting_profile="rational"),
    "g6_fraction_subtract_like": TypeSettingConfig(setting_profile="rational"),
    "g6_fraction_add_unlike": TypeSettingConfig(setting_profile="rational"),
    "g6_fraction_subtract_unlike": TypeSettingConfig(setting_profile="rational"),
    "g6_fraction_multiply": TypeSettingConfig(setting_profile="rational"),
    "g6_fraction_divide": TypeSettingConfig(setting_profile="rational"),
    "g6_fraction_divide_groups": TypeSettingConfig(setting_profile="rational"),
    "g6_fraction_divide_each": TypeSettingConfig(setting_profile="rational"),
    "g6_fraction_of_whole": TypeSettingConfig(setting_profile="rational"),
    "g6_integer_add_subtract": TypeSettingConfig(setting_profile="integer"),
    "g6_integer_multiply": TypeSettingConfig(setting_profile="integer"),
    "g6_integer_divide": TypeSettingConfig(setting_profile="integer"),
    "g6_negative_number_operations": TypeSettingConfig(
        setting_profile="integer",
        setting_defaults={"allow_negative": True},
    ),
    "g6_greatest_common_factor": TypeSettingConfig(setting_profile="factor"),
    "g6_least_common_multiple": TypeSettingConfig(setting_profile="factor"),
    "g6_gcf_and_lcm_word_problems": TypeSettingConfig(
        setting_profile="factor",
        count_default=5,
    ),
    "g6_factoring": TypeSettingConfig(setting_profile="factor"),
    "g6_divisibility": TypeSettingConfig(setting_profile="factor"),
    "g6_absolute_values": TypeSettingConfig(setting_profile="integer"),
    "g6_comparing_with_absolute_values": TypeSettingConfig(setting_profile="integer"),
    "g6_ordering_with_absolute_values": TypeSettingConfig(setting_profile="integer"),
    "g6_opposites_of_numbers": TypeSettingConfig(setting_profile="integer"),
    "g6_comparing_numbers": TypeSettingConfig(
        setting_profile="integer",
        inherits=("decimal", "rational"),
    ),
    "g6_ordering_numbers": TypeSettingConfig(
        setting_profile="integer",
        inherits=("decimal", "rational"),
    ),
    "g6_relating_percents_fractions_and_decimals": TypeSettingConfig(
        setting_profile="rational",
        inherits=("decimal",),
    ),
    "g6_long_division_with_remainders": TypeSettingConfig(setting_profile="integer"),
    "g6_dividing_decimals_by_whole_numbers": TypeSettingConfig(setting_profile="decimal"),
    "g6_introduction_to_percents": TypeSettingConfig(setting_profile="percent"),
    "g6_finding_percents_with_equivalent_fractions": TypeSettingConfig(setting_profile="percent"),
    "g6_solving_percent_problems_with_formulas": TypeSettingConfig(setting_profile="percent"),
    "g6_numeric_expressions_and_order_of_operations": TypeSettingConfig(setting_profile="order_of_operations"),
    "g6_numeric_expressions_with_exponents": TypeSettingConfig(setting_profile="order_of_operations"),
    "order_of_operations": TypeSettingConfig(setting_profile="order_of_operations"),
    "distributive_property": TypeSettingConfig(setting_profile="distributive"),
    "g6_distributive_property_numeric": TypeSettingConfig(setting_profile="distributive"),
    "g6_distributive_property_algebraic": TypeSettingConfig(setting_profile="distributive"),
    # Linear
    "writing_linear_equations": TypeSettingConfig(setting_profile="linear"),
    "slope": TypeSettingConfig(
        setting_profile="linear",
        setting_defaults={"include_graph_metadata": True},
    ),
    "more_on_slope": TypeSettingConfig(
        setting_profile="linear",
        setting_defaults={"include_graph_metadata": True},
    ),
    "plotting_points": TypeSettingConfig(
        setting_profile="coordinate_plane",
        setting_defaults={"include_graph_metadata": True},
    ),
    "systems_elimination": TypeSettingConfig(setting_profile="systems"),
    "systems_substitution": TypeSettingConfig(setting_profile="systems"),
    "direct_inverse_variation": TypeSettingConfig(setting_profile="variation"),
    "discrete_relations": TypeSettingConfig(
        setting_profile="relations",
        setting_defaults={"include_graph_metadata": True},
    ),
    "continuous_relations": TypeSettingConfig(
        setting_profile="relations",
        setting_defaults={"include_graph_metadata": True},
    ),
    "evaluating_graphing_functions": TypeSettingConfig(
        setting_profile="relations",
        setting_defaults={"include_graph_metadata": True},
    ),
    # Graphing (coordinate plane / number line)
    "graph_linear_equation": TypeSettingConfig(
        setting_profile="graphing",
        setting_defaults={"include_graph_metadata": True},
    ),
    "graph_inequality": TypeSettingConfig(
        setting_profile="graphing",
        setting_defaults={"include_graph_metadata": True, "graph_dimension": "coordinate"},
    ),
    "graph_linear_inequality": TypeSettingConfig(
        setting_profile="graphing",
        setting_defaults={"include_graph_metadata": True, "graph_dimension": "coordinate"},
    ),
    "graph_inequality_number_line": TypeSettingConfig(
        setting_profile="graphing",
        setting_defaults={"include_graph_metadata": True, "graph_dimension": "number_line"},
    ),
    "graph_absolute_value": TypeSettingConfig(
        setting_profile="graphing",
        setting_defaults={"include_graph_metadata": True},
    ),
    "graph_system": TypeSettingConfig(
        setting_profile="graphing",
        inherits=("systems",),
        setting_defaults={"include_graph_metadata": True},
    ),
    "graph_system_inequalities": TypeSettingConfig(
        setting_profile="graphing",
        inherits=("systems",),
        setting_defaults={"include_graph_metadata": True},
    ),
    "read_slope_from_graph": TypeSettingConfig(
        setting_profile="graphing",
        setting_defaults={"include_graph_metadata": True},
    ),
    "read_intercept_from_graph": TypeSettingConfig(
        setting_profile="graphing",
        setting_defaults={"include_graph_metadata": True},
    ),
    "graph_point_table": TypeSettingConfig(
        setting_profile="graphing",
        setting_defaults={"include_graph_metadata": True},
    ),
    "graph_transformations": TypeSettingConfig(
        setting_profile="graphing",
        setting_defaults={"include_graph_metadata": True},
    ),
    "graph_exponential": TypeSettingConfig(
        setting_profile="exponential",
        setting_defaults={"include_graph_metadata": True},
    ),
    "graph_quadratic": TypeSettingConfig(
        setting_profile="quadratic",
        setting_defaults={"include_graph_metadata": True},
    ),
    "graph_quadratic_inequality": TypeSettingConfig(
        setting_profile="quadratic",
        setting_defaults={"include_graph_metadata": True},
    ),
    "number_line_plot": TypeSettingConfig(
        setting_profile="coordinate_plane",
        setting_defaults={"include_graph_metadata": True},
    ),
    "graph_single_variable_inequality": TypeSettingConfig(
        setting_profile="graphing",
        setting_defaults={"include_graph_metadata": True, "graph_dimension": "number_line"},
    ),
    # Polynomials
    "polynomial_naming": TypeSettingConfig(
        setting_profile="polynomial",
        exclude_settings=("integer_coefficients_only",),
    ),
    "polynomial_add_subtract": TypeSettingConfig(
        setting_profile="polynomial",
        extra_settings=(rational_operation_settings,),
        exclude_settings=("allow_multiply", "allow_divide"),
    ),
    "polynomial_multiply": TypeSettingConfig(setting_profile="polynomial"),
    "polynomial_multiply_special": TypeSettingConfig(
        setting_profile="polynomial",
        exclude_settings=("min_degree", "max_degree"),
    ),
    "polynomial_factoring_common_factor": TypeSettingConfig(setting_profile="polynomial_factoring"),
    "polynomial_factoring_special_cases": TypeSettingConfig(setting_profile="polynomial_factoring"),
    "polynomial_factoring_grouping": TypeSettingConfig(setting_profile="polynomial_factoring"),
    "polynomial_long_division": TypeSettingConfig(setting_profile="polynomial_division"),
    "quadratic_factoring": TypeSettingConfig(
        setting_profile="polynomial_factoring",
        exclude_settings=("min_degree", "max_degree"),
        setting_defaults={"min_degree": 2, "max_degree": 2},
    ),
    # Quadratics
    "quadratic_square_roots": TypeSettingConfig(setting_profile="quadratic"),
    "quadratic_factoring_equations": TypeSettingConfig(setting_profile="quadratic"),
    "quadratic_formula": TypeSettingConfig(setting_profile="quadratic"),
    "quadratic_discriminant": TypeSettingConfig(setting_profile="quadratic"),
    "quadratic_completing_square_constant": TypeSettingConfig(setting_profile="quadratic"),
    "quadratic_completing_square_solve": TypeSettingConfig(setting_profile="quadratic"),
    "quadratic_graph_vertex": TypeSettingConfig(
        setting_profile="quadratic_graph",
        setting_defaults={"include_graph_metadata": True},
    ),
    "quadratic_graph_inequality": TypeSettingConfig(
        setting_profile="quadratic_graph",
        setting_defaults={"include_graph_metadata": True},
    ),
    "quadratic_vertex_identify": TypeSettingConfig(setting_profile="quadratic"),
    "quadratic_vertex_form_write": TypeSettingConfig(setting_profile="quadratic"),
    "quadratic_completing_square_vertex": TypeSettingConfig(setting_profile="quadratic"),
    "complex_add_subtract": TypeSettingConfig(setting_profile="algebra_expression"),
    "complex_multiply": TypeSettingConfig(setting_profile="algebra_expression"),
    "complex_operations": TypeSettingConfig(setting_profile="algebra_expression"),
    "complex_graph": TypeSettingConfig(
        setting_profile="coordinate_plane",
        setting_defaults={"include_graph_metadata": True},
    ),
    "matrix_add_subtract": TypeSettingConfig(setting_profile="algebra_expression"),
    "matrix_scalar_multiply": TypeSettingConfig(setting_profile="algebra_expression"),
    "matrix_operations": TypeSettingConfig(setting_profile="algebra_expression"),
    "inverse_function_basic": TypeSettingConfig(setting_profile="linear"),
    "function_evaluate": TypeSettingConfig(setting_profile="relations"),
    "function_operations": TypeSettingConfig(setting_profile="relations"),
    # Radicals
    "radical_simplification": TypeSettingConfig(setting_profile="radical"),
    "radical_add_subtract": TypeSettingConfig(setting_profile="radical"),
    "radical_multiply": TypeSettingConfig(setting_profile="radical"),
    "radical_divide": TypeSettingConfig(setting_profile="radical"),
    "radical_equations": TypeSettingConfig(
        inherits=("radical", "equation"),
        exclude_settings=("steps", "include_graph_metadata"),
    ),
    "radical_distance_formula": TypeSettingConfig(setting_profile="linear"),
    "radical_midpoint_formula": TypeSettingConfig(setting_profile="linear"),
    "geo_review_simplifying_square_roots": TypeSettingConfig(setting_profile="radical"),
    "geo_review_adding_and_subtracting_square_roots": TypeSettingConfig(setting_profile="radical"),
    "geo_review_multiplying_square_roots": TypeSettingConfig(setting_profile="radical"),
    "geo_review_dividing_square_roots": TypeSettingConfig(setting_profile="radical"),
    # Rational expressions
    "rational_simplification": TypeSettingConfig(
        setting_profile="polynomial_division",
        inherits=("polynomial_factoring",),
        exclude_settings=("divide_cleanly",),
        setting_defaults={
            "numerator_degree_min": 2,
            "numerator_degree_max": 4,
            "denominator_degree_min": 2,
            "denominator_degree_max": 4,
        },
    ),
    "rational_expression_simplification": TypeSettingConfig(
        setting_profile="polynomial_division",
        inherits=("polynomial_factoring",),
        exclude_settings=(
            "numerator_degree_min",
            "numerator_degree_max",
            "divide_cleanly",
        ),
        include_settings=tuple(rational_expression_extra_settings()),
        count_default=5,
        setting_defaults={
            "denominator_degree_min": 2,
            "denominator_degree_max": 3,
        },
    ),
    "rational_expression_multiply_divide": TypeSettingConfig(setting_profile="polynomial_factoring"),
    # Exponential / misc
    "exponential_growth_decay": TypeSettingConfig(setting_profile="exponential"),
    "properties_of_exponents": TypeSettingConfig(
        setting_profile="algebra_expression",
        exclude_settings=("term_count", "phrase_complexity", "constant_min", "constant_max"),
    ),
    "combining_like_terms": TypeSettingConfig(
        setting_profile="algebra_expression",
        exclude_settings=("phrase_complexity", "exponent_min", "exponent_max"),
    ),
    "g6_combining_like_terms": TypeSettingConfig(
        setting_profile="algebra_expression",
        exclude_settings=("phrase_complexity", "exponent_min", "exponent_max"),
    ),
    "verbal_expressions": TypeSettingConfig(
        setting_profile="algebra_expression",
        exclude_settings=("term_count", "exponent_min", "exponent_max"),
    ),
    "pa_verbal_expressions": TypeSettingConfig(
        setting_profile="algebra_expression",
        exclude_settings=("term_count", "exponent_min", "exponent_max"),
    ),
    "g6_writing_algebraic_expressions": TypeSettingConfig(
        setting_profile="algebra_expression",
        exclude_settings=("term_count", "exponent_min", "exponent_max"),
    ),
    # Trigonometry
    "trig_evaluate": TypeSettingConfig(
        setting_profile="trigonometry",
        setting_defaults={"unit_circle_only": True, "angle_max": 360},
    ),
    "trig_unit_circle": TypeSettingConfig(
        setting_profile="trigonometry",
        exclude_settings=("allow_tan", "allow_cot"),
        setting_defaults={"unit_circle_only": True},
    ),
    "trig_basic_identities": TypeSettingConfig(
        setting_profile="trigonometry",
        exclude_settings=(
            "angle_min",
            "angle_max",
            "angle_unit",
            "unit_circle_only",
            "allow_sin",
            "allow_cos",
            "allow_tan",
            "allow_cot",
        ),
    ),
    # Logarithms and exponentials
    "log_evaluate": TypeSettingConfig(
        setting_profile="logarithm",
        exclude_settings=("allow_change_of_base",),
    ),
    "log_change_of_base": TypeSettingConfig(
        setting_profile="logarithm",
        exclude_settings=("allow_natural_log", "allow_common_log", "require_integer_result"),
        setting_defaults={"allow_change_of_base": True},
    ),
    "log_equation_simple": TypeSettingConfig(
        setting_profile="logarithm",
        inherits=("equation",),
        exclude_settings=("allow_change_of_base", "steps", "include_graph_metadata"),
        setting_defaults={"require_integer_result": True},
    ),
    "exponential_equation_simple": TypeSettingConfig(
        setting_profile="exponential",
        exclude_settings=(
            "growth_rate_min",
            "growth_rate_max",
            "years_min",
            "years_max",
            "allow_fractional_exponents",
        ),
    ),
    "exponential_equation_with_log": TypeSettingConfig(
        setting_profile="exponential",
        exclude_settings=(
            "growth_rate_min",
            "growth_rate_max",
            "years_min",
            "years_max",
            "allow_fractional_exponents",
        ),
        setting_defaults={"exp_exponent_max": 4},
    ),
    # Sequences
    "sequence_arithmetic_nth_term": TypeSettingConfig(
        setting_profile="sequence",
        exclude_settings=("common_ratio_min", "common_ratio_max", "allow_negative_ratio"),
    ),
    "sequence_geometric_nth_term": TypeSettingConfig(
        setting_profile="sequence",
        exclude_settings=("common_diff_min", "common_diff_max"),
        setting_defaults={"allow_negative_ratio": False},
    ),
    # Calculus
    "limit_direct_evaluation": TypeSettingConfig(
        setting_profile="limits",
        exclude_settings=("allow_infinity",),
    ),
    "limit_at_infinity": TypeSettingConfig(
        setting_profile="limits",
        setting_defaults={"allow_infinity": True, "power_min": 1, "power_max": 3},
    ),
    "derivative_power_rule": TypeSettingConfig(
        setting_profile="derivatives",
        setting_defaults={"term_count": 3, "power_max": 4},
    ),
    "integral_power_rule": TypeSettingConfig(
        setting_profile="integrals",
        setting_defaults={"require_positive_power": True, "term_count": 2},
    ),
    # Geometry
    "geo_angles": TypeSettingConfig(setting_profile="geometry_angles"),
    "geo_classifying_angles": TypeSettingConfig(setting_profile="geometry_angles"),
    "geo_segment_length": TypeSettingConfig(setting_profile="geometry_basic"),
    "geo_triangle_angle_sum": TypeSettingConfig(setting_profile="geometry_triangles"),
    "geo_triangle_area": TypeSettingConfig(
        setting_profile="geometry_triangles",
        exclude_settings=(
            "allow_acute",
            "allow_right",
            "allow_obtuse",
            "allow_equilateral",
            "allow_isosceles",
            "allow_scalene",
            "similarity_ratio_min",
            "similarity_ratio_max",
            "proof_difficulty",
        ),
    ),
    "geo_triangle_perimeter": TypeSettingConfig(
        setting_profile="geometry_triangles",
        exclude_settings=(
            "allow_acute",
            "allow_right",
            "allow_obtuse",
            "allow_equilateral",
            "allow_isosceles",
            "allow_scalene",
            "similarity_ratio_min",
            "similarity_ratio_max",
            "proof_difficulty",
            "angle_min",
            "angle_max",
            "angle_unit",
        ),
    ),
    "geo_pythagorean_theorem": TypeSettingConfig(
        setting_profile="geometry_triangles",
        exclude_settings=(
            "allow_acute",
            "allow_obtuse",
            "allow_equilateral",
            "allow_isosceles",
            "allow_scalene",
            "similarity_ratio_min",
            "similarity_ratio_max",
            "proof_difficulty",
            "angle_min",
            "angle_max",
            "angle_unit",
        ),
        setting_defaults={"allow_right": True},
    ),
    "geo_similar_triangles": TypeSettingConfig(setting_profile="geometry_triangles"),
    "geo_circle_measure": TypeSettingConfig(setting_profile="geometry_circles"),
    "geo_coordinate_distance": TypeSettingConfig(
        setting_profile="coordinate_geometry",
        setting_defaults={"include_graph_metadata": True},
    ),
    # Statistics and probability
    "stats_mean": TypeSettingConfig(
        setting_profile="statistics",
        exclude_settings=("measure_type", "probability_format"),
        setting_defaults={"measure_type": "mean"},
    ),
    "stats_median": TypeSettingConfig(
        setting_profile="statistics",
        exclude_settings=("measure_type", "probability_format"),
        setting_defaults={"measure_type": "median"},
    ),
    "stats_mode": TypeSettingConfig(
        setting_profile="statistics",
        exclude_settings=("measure_type", "probability_format"),
        setting_defaults={"measure_type": "mode"},
    ),
    "stats_range": TypeSettingConfig(
        setting_profile="statistics",
        exclude_settings=("measure_type", "probability_format"),
        setting_defaults={"measure_type": "range"},
    ),
    "stats_center_spread": TypeSettingConfig(
        setting_profile="statistics",
        exclude_settings=("probability_format",),
    ),
    "stats_dot_plot_read": TypeSettingConfig(
        setting_profile="statistics",
        exclude_settings=("measure_type", "probability_format"),
    ),
    "stats_histogram_read": TypeSettingConfig(
        setting_profile="statistics",
        exclude_settings=("measure_type", "probability_format"),
    ),
    "stats_box_plot_basics": TypeSettingConfig(
        setting_profile="statistics",
        exclude_settings=("measure_type", "probability_format"),
    ),
    "stats_probability_single": TypeSettingConfig(
        setting_profile="statistics",
        exclude_settings=("measure_type", "data_set_size_min", "data_set_size_max", "value_min", "value_max", "integer_data_only"),
    ),
    "stats_probability_compound_independent": TypeSettingConfig(
        setting_profile="statistics",
        exclude_settings=("measure_type", "data_set_size_min", "data_set_size_max", "value_min", "value_max", "integer_data_only"),
    ),
    "stats_probability_mutually_exclusive": TypeSettingConfig(
        setting_profile="statistics",
        exclude_settings=("measure_type", "data_set_size_min", "data_set_size_max", "value_min", "value_max", "integer_data_only"),
    ),
    "stats_counting_principle": TypeSettingConfig(
        setting_profile="statistics",
        exclude_settings=("measure_type", "probability_format", "data_set_size_min", "data_set_size_max", "value_min", "value_max", "integer_data_only"),
    ),
    # Word problems
    "wp_distance_rate_time": TypeSettingConfig(setting_profile="word_problem"),
    "wp_work": TypeSettingConfig(setting_profile="word_problem"),
    "wp_age": TypeSettingConfig(setting_profile="word_problem"),
    "wp_consecutive_integers": TypeSettingConfig(setting_profile="word_problem"),
    "wp_coin": TypeSettingConfig(setting_profile="word_problem"),
    "wp_mixture": TypeSettingConfig(setting_profile="word_problem"),
    "wp_perimeter_area": TypeSettingConfig(setting_profile="word_problem"),
    "wp_percent": TypeSettingConfig(setting_profile="word_problem"),
    "wp_proportion": TypeSettingConfig(setting_profile="word_problem"),
    "wp_one_step_equation": TypeSettingConfig(setting_profile="word_problem"),
    "wp_two_step_equation": TypeSettingConfig(setting_profile="word_problem"),
    "wp_systems": TypeSettingConfig(setting_profile="word_problem"),
    "wp_inequality": TypeSettingConfig(setting_profile="word_problem"),
    "wp_gcf_lcm": TypeSettingConfig(setting_profile="word_problem"),
    "wp_number_line": TypeSettingConfig(setting_profile="word_problem"),
    "wp_coordinate_distance": TypeSettingConfig(setting_profile="word_problem"),
    "wp_similar_figures": TypeSettingConfig(setting_profile="word_problem"),
}

# Each wired generator inherits the cross-cutting common_enrichment mixin.
GENERATOR_SETTING_CONFIGS: dict[str, TypeSettingConfig] = {
    key: _with_common_enrichment(config) for key, config in _RAW_GENERATOR_SETTING_CONFIGS.items()
}


def config_for_generator(generator_key: str) -> TypeSettingConfig | None:
    return GENERATOR_SETTING_CONFIGS.get(generator_key)


def schema_for_generator(
    generator_key: str,
    *,
    count_default: int | None = None,
    count_max: int | None = None,
) -> list:
    """Resolve the full settings schema for a generator key."""
    from .resolve import resolve_type_settings

    config = config_for_generator(generator_key)
    if config is None:
        from .standard import standard_question_settings

        return standard_question_settings(
            count_default=count_default or 10,
            count_max=count_max or 50,
        )

    overrides: dict = {}
    if count_default is not None:
        overrides["count_default"] = count_default
    if count_max is not None:
        overrides["count_max"] = count_max
    if overrides:
        config = TypeSettingConfig(
            setting_profile=config.setting_profile,
            inherits=config.inherits,
            exclude_settings=config.exclude_settings,
            include_settings=config.include_settings,
            extra_settings=config.extra_settings,
            setting_defaults=config.setting_defaults,
            count_default=overrides.get("count_default", config.count_default),
            count_max=overrides.get("count_max", config.count_max),
        )
    return resolve_type_settings(config)
