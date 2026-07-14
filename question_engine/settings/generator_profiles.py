"""Default setting-profile inheritance keyed by generator name."""

from __future__ import annotations

from .domains.equation import (
    absolute_value_equation_form_settings,
    absolute_value_inequality_form_settings,
    quadratic_square_root_form_settings,
)
from .domains.number import (
    decimal_multiplication_settings,
    gcf_constraint_settings,
    long_division_remainder_settings,
    mixed_number_form_settings,
    squares_and_square_roots_form_settings,
)
from .domains.polynomial import polynomial_multiply_settings
from .domains.radical import (
    radical_add_subtract_form_settings,
    radical_divide_form_settings,
    radical_equation_form_settings,
    radical_multiply_form_settings,
)
from .domains.rational import (
    division_notation_settings,
    rational_equation_form_settings,
    rational_expression_extra_settings,
    rational_multiply_divide_settings,
    rational_operation_settings,
)
from .domains.word_problem import (
    consecutive_integers_settings,
    distance_rate_time_settings,
    percent_word_problem_settings,
    similar_figures_prompt_settings,
    work_problem_settings,
)
from .domains.graphing import number_line_range_settings
from .domains.statistics import chart_drawing_settings
from .factoring_settings import special_case_extra_settings
from .resolve import TypeSettingConfig

_ENRICHMENT = "common_enrichment"

# Inherited enrichment knobs that only apply to expression / term-count generators.
_TERM_SETTINGS = ("min_terms", "max_terms")
# Phrase / verbal-expression knobs that equations and inequalities should not show.
_PHRASE_SETTINGS = ("phrase_complexity", "max_phrase_operations")
# Coordinate-plane knobs irrelevant to pure number-line types.
_COORD_PLANE_SETTINGS = (
    "slope_min",
    "slope_max",
    "intercept_min",
    "intercept_max",
    "coord_min",
    "coord_max",
    "integer_coordinates",
    "quadrant",
    "show_grid",
    "show_points",
    "table_row_count",
)
# Number-line knobs irrelevant to pure coordinate-plane types.
_NUMBER_LINE_SETTINGS = (
    "number_line_min",
    "number_line_max",
    "number_line_tick_interval",
    "number_line_show_zero",
)


def _excludes(*groups: tuple[str, ...], extra: tuple[str, ...] = ()) -> tuple[str, ...]:
    keys: list[str] = []
    for group in groups:
        keys.extend(group)
    keys.extend(extra)
    return tuple(dict.fromkeys(keys))


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
    "one_step_equations": TypeSettingConfig(
        setting_profile="equation",
        exclude_settings=_excludes(_TERM_SETTINGS, _PHRASE_SETTINGS),
    ),
    "two_step_equations": TypeSettingConfig(
        setting_profile="equation",
        exclude_settings=_excludes(
            _TERM_SETTINGS,
            _PHRASE_SETTINGS,
            extra=("allow_multiply", "allow_divide"),
        ),
    ),
    "multi_step_equations": TypeSettingConfig(
        setting_profile="equation",
        exclude_settings=_excludes(
            _TERM_SETTINGS,
            _PHRASE_SETTINGS,
            extra=("allow_multiply", "allow_divide", "allow_add", "allow_subtract"),
        ),
    ),
    "literal_equations": TypeSettingConfig(
        setting_profile="equation",
        exclude_settings=_excludes(
            _TERM_SETTINGS,
            _PHRASE_SETTINGS,
            extra=("allow_multiply", "allow_divide", "allow_add", "allow_subtract"),
        ),
    ),
    "absolute_value_equations": TypeSettingConfig(
        setting_profile="equation",
        exclude_settings=_excludes(
            _TERM_SETTINGS,
            _PHRASE_SETTINGS,
            extra=("allow_multiply", "allow_divide", "allow_add", "allow_subtract"),
        ),
        extra_settings=(absolute_value_equation_form_settings,),
        setting_defaults={
            "allow_basic": True,
            "allow_isolated_right": True,
            "allow_simple": True,
            "allow_abs_plus_constant": True,
            "allow_factored_inside": True,
            "allow_coeff_outside": False,
            "allow_abs_equals_abs": False,
            "allow_abs_equals_linear": False,
        },
    ),
    # Inequalities — blank number line for student work (answer key shows shading).
    "one_step_inequalities": TypeSettingConfig(
        setting_profile="inequality",
        exclude_settings=_excludes(_TERM_SETTINGS, _PHRASE_SETTINGS),
        setting_defaults={"include_graph_metadata": True},
    ),
    "two_step_inequalities": TypeSettingConfig(
        setting_profile="inequality",
        exclude_settings=_excludes(_TERM_SETTINGS, _PHRASE_SETTINGS),
        setting_defaults={"include_graph_metadata": True},
    ),
    "multi_step_inequalities": TypeSettingConfig(
        setting_profile="inequality",
        exclude_settings=_excludes(_TERM_SETTINGS, _PHRASE_SETTINGS),
        setting_defaults={"include_graph_metadata": True},
    ),
    "compound_inequalities": TypeSettingConfig(
        setting_profile="compound_inequality",
        exclude_settings=_excludes(_TERM_SETTINGS, _PHRASE_SETTINGS),
        setting_defaults={"include_graph_metadata": True},
    ),
    "absolute_value_inequalities": TypeSettingConfig(
        setting_profile="inequality",
        exclude_settings=_excludes(_TERM_SETTINGS, _PHRASE_SETTINGS, extra=("steps",)),
        extra_settings=(absolute_value_inequality_form_settings,),
        setting_defaults={
            "allow_simple": True,
            "allow_shifted": True,
            "allow_linear": True,
            "allow_abs_plus_constant": False,
            "allow_abs_vs_linear": False,
            "include_graph_metadata": True,
        },
    ),
    # Numbers
    "sets_of_numbers": TypeSettingConfig(
        setting_profile="number_sets",
        exclude_settings=_excludes(_TERM_SETTINGS, _PHRASE_SETTINGS),
        setting_defaults={
            "ask_mode": "mixed",
            "include_natural": True,
            "include_whole": True,
            "include_integer": True,
            "include_rational": True,
            "include_irrational": True,
            "include_real": True,
            "allow_negative": True,
            "allow_fractions": True,
            "allow_irrationals": True,
        },
    ),
    "rational_add_subtract": TypeSettingConfig(setting_profile="rational"),
    "pa_integers_adding_and_subtracting": TypeSettingConfig(
        setting_profile="integer",
        extra_settings=(mixed_number_form_settings,),
    ),
    "rational_multiply": TypeSettingConfig(setting_profile="rational"),
    "rational_divide": TypeSettingConfig(
        setting_profile="rational",
        extra_settings=(division_notation_settings,),
    ),
    "percents": TypeSettingConfig(setting_profile="percent"),
    "percent_of_change": TypeSettingConfig(setting_profile="percent"),
    "converting_fractions_and_decimals": TypeSettingConfig(
        setting_profile="rational",
        inherits=("decimal",),
    ),
    "fractions_decimals_and_percents": TypeSettingConfig(
        setting_profile="percent",
        inherits=("rational", "decimal"),
        setting_defaults={"include_percent_conversions": True},
    ),
    "pa_fractions_decimals_and_percents": TypeSettingConfig(
        setting_profile="percent",
        inherits=("rational", "decimal"),
        setting_defaults={"include_percent_conversions": True},
    ),
    "solving_proportions": TypeSettingConfig(setting_profile="proportion"),
    "scientific_notation_write": TypeSettingConfig(setting_profile="scientific_notation"),
    "scientific_notation_operations": TypeSettingConfig(setting_profile="scientific_notation"),
    "scientific_notation_add_subtract": TypeSettingConfig(setting_profile="scientific_notation"),
    "pa_squares_and_square_roots": TypeSettingConfig(
        extra_settings=(squares_and_square_roots_form_settings,),
        exclude_settings=_excludes(_TERM_SETTINGS, _PHRASE_SETTINGS),
        setting_defaults={
            "allow_square_roots": True,
            "allow_squares": True,
            "allow_word_prompts": True,
            "perfect_squares_only": True,
            "allow_extract_square_factors": False,
            "base_min": 2,
            "base_max": 12,
        },
    ),
    "g6_introduction_to_ratios": TypeSettingConfig(setting_profile="ratio"),
    "g6_equivalent_ratios": TypeSettingConfig(setting_profile="ratio"),
    "g6_unit_rates": TypeSettingConfig(setting_profile="unit_rate"),
    "g6_decimal_addition": TypeSettingConfig(setting_profile="decimal"),
    "g6_decimal_subtraction": TypeSettingConfig(setting_profile="decimal"),
    "g6_decimal_multiplication": TypeSettingConfig(
        setting_profile="decimal",
        extra_settings=(decimal_multiplication_settings,),
    ),
    "g6_fraction_add_like": TypeSettingConfig(setting_profile="rational"),
    "g6_fraction_subtract_like": TypeSettingConfig(setting_profile="rational"),
    "g6_fraction_add_unlike": TypeSettingConfig(setting_profile="rational"),
    "g6_fraction_subtract_unlike": TypeSettingConfig(setting_profile="rational"),
    "g6_fraction_multiply": TypeSettingConfig(setting_profile="rational"),
    "g6_fraction_divide": TypeSettingConfig(
        setting_profile="rational",
        extra_settings=(division_notation_settings,),
    ),
    "g6_fraction_divide_groups": TypeSettingConfig(setting_profile="rational"),
    "g6_fraction_divide_each": TypeSettingConfig(setting_profile="rational"),
    "g6_fraction_of_whole": TypeSettingConfig(setting_profile="rational"),
    "g6_integer_add_subtract": TypeSettingConfig(setting_profile="integer"),
    "g6_integer_multiply": TypeSettingConfig(setting_profile="integer"),
    "g6_properties_of_addition_and_multiplication": TypeSettingConfig(
        setting_profile="integer",
        setting_defaults={"multiple_choice": True, "allow_negative": False},
    ),
    "g6_integer_divide": TypeSettingConfig(setting_profile="integer"),
    "g6_negative_number_operations": TypeSettingConfig(
        setting_profile="integer",
        setting_defaults={"allow_negative": True},
    ),
    "g6_greatest_common_factor": TypeSettingConfig(
        setting_profile="factor",
        extra_settings=(gcf_constraint_settings,),
        setting_defaults={"require_gcf_greater_than_one": True},
    ),
    "g6_least_common_multiple": TypeSettingConfig(setting_profile="factor"),
    "g6_gcf_and_lcm_word_problems": TypeSettingConfig(
        setting_profile="factor",
        extra_settings=(gcf_constraint_settings,),
        setting_defaults={"require_gcf_greater_than_one": True},
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
    "g6_long_division_with_remainders": TypeSettingConfig(
        setting_profile="integer",
        exclude_settings=("num_min", "num_max", "allow_negative"),
        extra_settings=(long_division_remainder_settings,),
        setting_defaults={"allow_negative": False},
    ),
    "g6_dividing_whole_numbers_that_result_in_decimals": TypeSettingConfig(
        setting_profile="decimal",
        setting_defaults={"allow_negative": False},
    ),
    "g6_dividing_decimals_by_whole_numbers": TypeSettingConfig(setting_profile="decimal"),
    "g6_introduction_to_percents": TypeSettingConfig(setting_profile="percent"),
    "g6_finding_percents_with_equivalent_fractions": TypeSettingConfig(setting_profile="percent"),
    "g6_solving_percent_problems_with_formulas": TypeSettingConfig(setting_profile="percent"),
    "g6_numeric_expressions_and_order_of_operations": TypeSettingConfig(setting_profile="order_of_operations"),
    "g6_numeric_expressions_with_exponents": TypeSettingConfig(setting_profile="order_of_operations"),
    "order_of_operations": TypeSettingConfig(setting_profile="order_of_operations"),
    "distributive_property": TypeSettingConfig(setting_profile="distributive"),
    "distributive_property_algebraic": TypeSettingConfig(setting_profile="distributive"),
    "complex_rationalize_denominator": TypeSettingConfig(setting_profile="algebra_expression"),
    "trigonometry_and_area": TypeSettingConfig(setting_profile="geometry_triangles"),
    "scatter_plot_interpret": TypeSettingConfig(setting_profile="statistics"),
    "g6_whole_by_decimal_divide": TypeSettingConfig(setting_profile="decimal"),
    "check_equation_solution": TypeSettingConfig(setting_profile="equation"),
    "write_one_step_equation": TypeSettingConfig(setting_profile="equation"),
    "simplifying_numeric_fractions": TypeSettingConfig(setting_profile="rational"),
    "place_value_and_rounding": TypeSettingConfig(setting_profile="decimal"),
    "writing_numbers_with_words": TypeSettingConfig(setting_profile="integer"),
    "g6_distributive_property_numeric": TypeSettingConfig(setting_profile="distributive"),
    "g6_distributive_property_algebraic": TypeSettingConfig(setting_profile="distributive"),
    # Linear
    "writing_linear_equations": TypeSettingConfig(
        setting_profile="graphing",
        exclude_settings=_excludes(_TERM_SETTINGS, _NUMBER_LINE_SETTINGS, extra=("graph_dimension",)),
        setting_defaults={
            "include_graph_metadata": True,
            "show_points": False,
            "ask_mode": "mixed",
        },
    ),
    "slope": TypeSettingConfig(
        setting_profile="linear",
        exclude_settings=_excludes(_TERM_SETTINGS, _NUMBER_LINE_SETTINGS),
        setting_defaults={
            # Equation forms never need a figure; two-point blank graph is opt-in.
            "include_graph_metadata": False,
            "graph_for_two_points": False,
            "ask_mode": "mixed",
        },
    ),
    "more_on_slope": TypeSettingConfig(
        setting_profile="more_on_slope",
        exclude_settings=_excludes(_TERM_SETTINGS, _NUMBER_LINE_SETTINGS),
        setting_defaults={
            # True for from_graph / classify stimulus; two-point blank graphs stay off.
            "include_graph_metadata": True,
            "show_points": False,
            "graph_for_two_points": False,
            "ask_mode": "mixed",
        },
    ),
    "plotting_points": TypeSettingConfig(
        setting_profile="coordinate_plane",
        exclude_settings=_excludes(_TERM_SETTINGS, _NUMBER_LINE_SETTINGS),
        setting_defaults={"include_graph_metadata": True},
    ),
    "systems_elimination": TypeSettingConfig(
        setting_profile="systems",
        exclude_settings=_excludes(_TERM_SETTINGS),
    ),
    "systems_substitution": TypeSettingConfig(
        setting_profile="systems",
        exclude_settings=_excludes(_TERM_SETTINGS),
    ),
    "direct_inverse_variation": TypeSettingConfig(
        setting_profile="variation",
        exclude_settings=_excludes(_TERM_SETTINGS),
    ),
    "discrete_relations": TypeSettingConfig(
        setting_profile="relations",
        exclude_settings=_excludes(_TERM_SETTINGS, _NUMBER_LINE_SETTINGS),
        setting_defaults={"include_graph_metadata": True},
    ),
    "continuous_relations": TypeSettingConfig(
        setting_profile="relations",
        exclude_settings=_excludes(_TERM_SETTINGS, _NUMBER_LINE_SETTINGS),
        setting_defaults={"include_graph_metadata": True},
    ),
    "evaluating_graphing_functions": TypeSettingConfig(
        setting_profile="relations",
        exclude_settings=_excludes(_TERM_SETTINGS, _NUMBER_LINE_SETTINGS),
        setting_defaults={"include_graph_metadata": True},
    ),
    # Graphing (coordinate plane / number line)
    "graph_linear_equation": TypeSettingConfig(
        setting_profile="graphing",
        exclude_settings=_excludes(_TERM_SETTINGS, _NUMBER_LINE_SETTINGS, extra=("graph_dimension",)),
        setting_defaults={"include_graph_metadata": True},
    ),
    "graph_inequality": TypeSettingConfig(
        setting_profile="graphing",
        exclude_settings=_excludes(_TERM_SETTINGS),
        setting_defaults={"include_graph_metadata": True, "graph_dimension": "coordinate"},
    ),
    "graph_linear_inequality": TypeSettingConfig(
        setting_profile="graphing",
        exclude_settings=_excludes(_TERM_SETTINGS, _NUMBER_LINE_SETTINGS, extra=("graph_dimension",)),
        setting_defaults={"include_graph_metadata": True, "graph_dimension": "coordinate"},
    ),
    "graph_inequality_number_line": TypeSettingConfig(
        setting_profile="number_line",
        exclude_settings=_excludes(
            _TERM_SETTINGS,
            _PHRASE_SETTINGS,
            _COORD_PLANE_SETTINGS,
            extra=("graph_dimension", "number_line_tick_interval"),
        ),
        setting_defaults={"include_graph_metadata": True, "graph_dimension": "number_line"},
    ),
    "graph_absolute_value": TypeSettingConfig(
        setting_profile="absolute_value_graph",
        exclude_settings=_excludes(_TERM_SETTINGS, _NUMBER_LINE_SETTINGS, extra=("graph_dimension",)),
        setting_defaults={
            "include_graph_metadata": True,
            "allow_shift_h": True,
            "allow_shift_k": False,
            "allow_stretch": False,
            "allow_reflection": False,
            "coef_min": 1,
            "coef_max": 1,
            "integer_only": True,
        },
    ),
    "graph_radical": TypeSettingConfig(
        setting_profile="absolute_value_graph",
        exclude_settings=_excludes(_TERM_SETTINGS, _NUMBER_LINE_SETTINGS, extra=("graph_dimension",)),
        setting_defaults={
            "include_graph_metadata": True,
            "allow_shift_h": True,
            "allow_shift_k": False,
            "allow_stretch": False,
            "allow_reflection": False,
        },
    ),
    "graph_rational": TypeSettingConfig(
        setting_profile="absolute_value_graph",
        exclude_settings=_excludes(_TERM_SETTINGS, _NUMBER_LINE_SETTINGS, extra=("graph_dimension",)),
        setting_defaults={
            "include_graph_metadata": True,
            "allow_shift_h": True,
            "allow_shift_k": False,
            "allow_stretch": False,
            "allow_reflection": False,
        },
    ),
    "graph_system": TypeSettingConfig(
        setting_profile="graphing",
        inherits=("systems",),
        exclude_settings=_excludes(_TERM_SETTINGS, _NUMBER_LINE_SETTINGS, extra=("graph_dimension",)),
        setting_defaults={"include_graph_metadata": True},
    ),
    "graph_system_inequalities": TypeSettingConfig(
        setting_profile="graphing",
        inherits=("systems",),
        exclude_settings=_excludes(_TERM_SETTINGS, _NUMBER_LINE_SETTINGS, extra=("graph_dimension",)),
        setting_defaults={"include_graph_metadata": True},
    ),
    "read_slope_from_graph": TypeSettingConfig(
        setting_profile="graphing",
        exclude_settings=_excludes(_TERM_SETTINGS, _NUMBER_LINE_SETTINGS, extra=("graph_dimension",)),
        setting_defaults={"include_graph_metadata": True, "show_points": False},
    ),
    "read_intercept_from_graph": TypeSettingConfig(
        setting_profile="graphing",
        exclude_settings=_excludes(_TERM_SETTINGS, _NUMBER_LINE_SETTINGS, extra=("graph_dimension",)),
        setting_defaults={"include_graph_metadata": True},
    ),
    "read_equation_from_graph": TypeSettingConfig(
        setting_profile="graphing",
        exclude_settings=_excludes(_TERM_SETTINGS, _NUMBER_LINE_SETTINGS, extra=("graph_dimension",)),
        setting_defaults={
            "include_graph_metadata": True,
            "show_points": False,
        },
    ),
    "graph_point_table": TypeSettingConfig(
        setting_profile="graphing",
        exclude_settings=_excludes(_TERM_SETTINGS, _NUMBER_LINE_SETTINGS, extra=("graph_dimension",)),
        setting_defaults={"include_graph_metadata": True},
    ),
    "graph_transformations": TypeSettingConfig(
        setting_profile="graphing",
        exclude_settings=_excludes(_TERM_SETTINGS, _NUMBER_LINE_SETTINGS, extra=("graph_dimension",)),
        setting_defaults={"include_graph_metadata": True},
    ),
    "graph_exponential": TypeSettingConfig(
        setting_profile="exponential_graph",
        exclude_settings=_excludes(_TERM_SETTINGS, _NUMBER_LINE_SETTINGS),
        setting_defaults={
            "include_graph_metadata": True,
            "allow_decay": False,
            "allow_stretch": False,
            "allow_vertical_shift": False,
            "allow_horizontal_shift": False,
            "allow_reflection": False,
        },
    ),
    "graph_logarithmic": TypeSettingConfig(
        setting_profile="exponential_graph",
        exclude_settings=_excludes(_TERM_SETTINGS, _NUMBER_LINE_SETTINGS),
        setting_defaults={
            "include_graph_metadata": True,
            "allow_stretch": False,
            "allow_vertical_shift": False,
            "allow_horizontal_shift": False,
            "allow_reflection": False,
            "base_min": 2,
        },
    ),
    "graph_quadratic": TypeSettingConfig(
        setting_profile="quadratic_graph",
        exclude_settings=_excludes(_TERM_SETTINGS, _NUMBER_LINE_SETTINGS, extra=("graph_dimension",)),
        setting_defaults={
            "include_graph_metadata": True,
            "allow_vertex_form": True,
            "allow_standard_form": False,
            "allow_factored_form": False,
            "allow_messy_form": False,
            "allow_shift_h": True,
            "allow_shift_k": True,
            "allow_stretch": False,
            "allow_reflection": False,
            "coef_min": 1,
            "coef_max": 1,
            "integer_only": True,
        },
    ),
    "graph_quadratic_inequality": TypeSettingConfig(
        setting_profile="quadratic_inequality_graph",
        exclude_settings=_excludes(_TERM_SETTINGS, _NUMBER_LINE_SETTINGS, extra=("graph_dimension",)),
        setting_defaults={
            "include_graph_metadata": True,
            "allow_vertex_form": True,
            "allow_standard_form": True,
            "allow_factored_form": False,
            "allow_messy_form": False,
            "allow_shift_h": True,
            "allow_shift_k": True,
            "allow_stretch": False,
            "allow_reflection": False,
            "coef_min": 1,
            "coef_max": 1,
            "integer_only": True,
            "allow_lt": True,
            "allow_gt": True,
            "allow_lte": False,
            "allow_gte": False,
        },
    ),
    "solve_polynomial_by_graphing": TypeSettingConfig(
        setting_profile="polynomial_solve_graph",
        exclude_settings=_excludes(_TERM_SETTINGS, _NUMBER_LINE_SETTINGS, extra=("graph_dimension",)),
        setting_defaults={
            "include_graph_metadata": True,
            "leading_coefficient_one": True,
            "monic_only": True,
            "allow_stretch": False,
            "allow_reflection": False,
            "allow_factored_form": False,
            "coef_min": 1,
            "coef_max": 1,
            "root_min": -3,
            "root_max": 3,
            "min_degree": 2,
            "max_degree": 2,
            "integer_only": True,
        },
    ),
    "number_line_plot": TypeSettingConfig(
        setting_profile="number_line",
        exclude_settings=_excludes(
            _TERM_SETTINGS,
            _PHRASE_SETTINGS,
            _COORD_PLANE_SETTINGS,
            extra=("number_line_tick_interval",),
        ),
        setting_defaults={"include_graph_metadata": True},
    ),
    "graph_single_variable_inequality": TypeSettingConfig(
        setting_profile="number_line",
        exclude_settings=_excludes(
            _TERM_SETTINGS,
            _PHRASE_SETTINGS,
            _COORD_PLANE_SETTINGS,
            extra=("graph_dimension", "number_line_tick_interval"),
        ),
        setting_defaults={"include_graph_metadata": True, "graph_dimension": "number_line"},
    ),
    # Polynomials
    "polynomial_naming": TypeSettingConfig(
        setting_profile="polynomial",
        exclude_settings=_excludes(_TERM_SETTINGS, _PHRASE_SETTINGS, extra=("integer_coefficients_only",)),
    ),
    "polynomial_add_subtract": TypeSettingConfig(
        setting_profile="polynomial",
        extra_settings=(rational_operation_settings,),
        exclude_settings=_excludes(_TERM_SETTINGS, _PHRASE_SETTINGS, extra=("allow_multiply", "allow_divide")),
    ),
    "polynomial_multiply": TypeSettingConfig(
        setting_profile="polynomial",
        extra_settings=(polynomial_multiply_settings,),
        exclude_settings=_excludes(_TERM_SETTINGS, _PHRASE_SETTINGS),
        setting_defaults={
            "allow_monomial_binomial": True,
            "allow_binomial_binomial": True,
            "allow_trinomial": False,
            "leading_coefficient_one": True,
            "max_factor_terms": 2,
        },
    ),
    "polynomial_multiply_special": TypeSettingConfig(
        setting_profile="polynomial",
        exclude_settings=_excludes(_TERM_SETTINGS, _PHRASE_SETTINGS, extra=("min_degree", "max_degree")),
    ),
    "polynomial_factoring_common_factor": TypeSettingConfig(
        setting_profile="polynomial_factoring",
        exclude_settings=_excludes(_TERM_SETTINGS, _PHRASE_SETTINGS),
    ),
    "polynomial_factoring_special_cases": TypeSettingConfig(
        setting_profile="polynomial_factoring",
        extra_settings=(special_case_extra_settings,),
        exclude_settings=_excludes(
            _TERM_SETTINGS,
            _PHRASE_SETTINGS,
            extra=(
                "factor_rrt",
                "factor_normal",
                "factor_grouping",
                "factor_substitution",
                "difference_of_squares_only",
                "min_degree",
                "max_degree",
            ),
        ),
        setting_defaults={
            "factor_difference_of_squares": True,
            "factor_perfect_square_trinomial": True,
            "factor_difference_of_cubes": True,
            "factor_sum_of_cubes": True,
            "allow_higher_even_powers": False,
            "max_even_power": 8,
            "require_gcf": False,
        },
    ),
    "polynomial_factoring_grouping": TypeSettingConfig(
        setting_profile="polynomial_factoring",
        exclude_settings=_excludes(_TERM_SETTINGS, _PHRASE_SETTINGS),
    ),
    "polynomial_long_division": TypeSettingConfig(
        setting_profile="polynomial_division",
        exclude_settings=_excludes(_TERM_SETTINGS, _PHRASE_SETTINGS),
    ),
    "quadratic_factoring": TypeSettingConfig(
        setting_profile="polynomial_factoring",
        exclude_settings=_excludes(_TERM_SETTINGS, _PHRASE_SETTINGS),
        setting_defaults={"min_degree": 2, "max_degree": 2},
    ),
    # Quadratics
    "quadratic_square_roots": TypeSettingConfig(
        setting_profile="quadratic",
        exclude_settings=_excludes(_TERM_SETTINGS, _PHRASE_SETTINGS),
        extra_settings=(quadratic_square_root_form_settings,),
        setting_defaults={
            "allow_isolated": True,
            "allow_vertex": True,
            "allow_complete_square": False,
        },
    ),
    "quadratic_factoring_equations": TypeSettingConfig(setting_profile="quadratic"),
    "quadratic_formula": TypeSettingConfig(setting_profile="quadratic"),
    "quadratic_discriminant": TypeSettingConfig(setting_profile="quadratic"),
    "quadratic_completing_square_constant": TypeSettingConfig(setting_profile="quadratic"),
    "quadratic_completing_square_solve": TypeSettingConfig(setting_profile="quadratic"),
    "quadratic_graph_vertex": TypeSettingConfig(
        setting_profile="quadratic_graph",
        setting_defaults={
            "include_graph_metadata": True,
            "allow_vertex_form": True,
            "allow_standard_form": False,
            "allow_factored_form": False,
            "allow_messy_form": False,
            "allow_shift_h": True,
            "allow_shift_k": True,
            "allow_stretch": False,
            "allow_reflection": False,
            "coef_min": 1,
            "coef_max": 1,
            "integer_only": True,
        },
    ),
    "quadratic_graph_inequality": TypeSettingConfig(
        setting_profile="quadratic_inequality_graph",
        setting_defaults={
            "include_graph_metadata": True,
            "allow_vertex_form": True,
            "allow_standard_form": True,
            "allow_factored_form": False,
            "allow_messy_form": False,
            "allow_shift_h": True,
            "allow_shift_k": True,
            "allow_stretch": False,
            "allow_reflection": False,
            "coef_min": 1,
            "coef_max": 1,
            "integer_only": True,
            "allow_lt": True,
            "allow_gt": True,
            "allow_lte": False,
            "allow_gte": False,
        },
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
    "complex_absolute_value": TypeSettingConfig(setting_profile="algebra_expression"),
    "conic_sections": TypeSettingConfig(
        setting_profile="graphing",
        setting_defaults={"include_graph_metadata": True},
    ),
    "polar_graphs": TypeSettingConfig(
        setting_profile="graphing",
        setting_defaults={"include_graph_metadata": True},
    ),
    "polar_rectangular_forms": TypeSettingConfig(setting_profile="geometry_angles"),
    "polar_conic_forms": TypeSettingConfig(setting_profile="algebra_expression"),
    "complex_polar_form": TypeSettingConfig(setting_profile="algebra_expression"),
    "matrix_add_subtract": TypeSettingConfig(setting_profile="algebra_expression"),
    "matrix_scalar_multiply": TypeSettingConfig(setting_profile="algebra_expression"),
    "matrix_operations": TypeSettingConfig(setting_profile="algebra_expression"),
    "inverse_function_basic": TypeSettingConfig(setting_profile="linear"),
    "function_evaluate": TypeSettingConfig(setting_profile="relations"),
    "function_operations": TypeSettingConfig(setting_profile="relations"),
    # Radicals
    "radical_simplification": TypeSettingConfig(setting_profile="radical"),
    "complex_fractions": TypeSettingConfig(
        setting_profile="polynomial",
        exclude_settings=(
            "min_degree",
            "max_degree",
            "variable",
            "integer_coefficients_only",
            "monic_only",
            "leading_coefficient_one",
        ),
        setting_defaults={
            "coef_min": -6,
            "coef_max": 6,
        },
    ),
    "radical_add_subtract": TypeSettingConfig(
        setting_profile="radical",
        extra_settings=(radical_add_subtract_form_settings,),
        setting_defaults={
            "allow_like_radicals": True,
            "allow_unsimplified_radicals": False,
            "allow_coeff_unsimplified": False,
            "coef_min": 1,
            "coef_max": 6,
            "min_terms": 2,
            "max_terms": 2,
        },
    ),
    "radical_multiply": TypeSettingConfig(
        setting_profile="radical",
        exclude_settings=("radical_index", "require_simplifiable"),
        extra_settings=(radical_multiply_form_settings,),
        setting_defaults={
            "allow_simple_product": True,
            "allow_coeff_product": False,
            "allow_binomial_product": False,
            "coef_min": 1,
            "coef_max": 4,
        },
    ),
    "radical_divide": TypeSettingConfig(
        setting_profile="radical",
        extra_settings=(radical_divide_form_settings,),
        setting_defaults={
            "allow_reduced_quotients": True,
            "allow_simplify_quotients": False,
            "allow_rationalize_divide": False,
            "coef_min": 1,
            "coef_max": 6,
        },
    ),
    "radical_equations": TypeSettingConfig(
        inherits=("radical", "equation"),
        exclude_settings=(
            "steps",
            "include_graph_metadata",
            "radicand_min",
            "radicand_max",
            "radical_index",
            "require_simplifiable",
            "allow_add",
            "allow_subtract",
            "allow_multiply",
            "allow_divide",
            *_TERM_SETTINGS,
            *_PHRASE_SETTINGS,
        ),
        extra_settings=(radical_equation_form_settings,),
        setting_defaults={
            "allow_light_prep": True,
            "allow_isolate_algebra": False,
            "allow_radical_equals_linear": False,
            "allow_two_radicals": False,
            "integer_only": True,
        },
    ),
    "radical_distance_formula": TypeSettingConfig(setting_profile="linear"),
    "radical_midpoint_formula": TypeSettingConfig(setting_profile="linear"),
    "geo_review_simplifying_square_roots": TypeSettingConfig(setting_profile="radical"),
    "geo_review_adding_and_subtracting_square_roots": TypeSettingConfig(
        setting_profile="radical",
        extra_settings=(radical_add_subtract_form_settings,),
        setting_defaults={
            "allow_like_radicals": True,
            "allow_unsimplified_radicals": False,
            "allow_coeff_unsimplified": False,
            "coef_min": 1,
            "coef_max": 6,
            "min_terms": 2,
            "max_terms": 2,
        },
    ),
    "geo_review_multiplying_square_roots": TypeSettingConfig(setting_profile="radical"),
    "geo_review_dividing_square_roots": TypeSettingConfig(
        setting_profile="radical",
        extra_settings=(radical_divide_form_settings,),
        setting_defaults={
            "allow_reduced_quotients": True,
            "allow_simplify_quotients": False,
            "allow_rationalize_divide": False,
            "coef_min": 1,
            "coef_max": 6,
        },
    ),
    "a2_radical_functions_and_rational_exponents_adding_and_subtracting_radical_expressions": TypeSettingConfig(
        setting_profile="radical",
        extra_settings=(radical_add_subtract_form_settings,),
        setting_defaults={
            "allow_like_radicals": True,
            "allow_unsimplified_radicals": False,
            "allow_coeff_unsimplified": False,
            "coef_min": 1,
            "coef_max": 6,
            "min_terms": 2,
            "max_terms": 2,
        },
    ),
    "a2_radical_functions_and_rational_exponents_dividing_radical_expressions": TypeSettingConfig(
        setting_profile="radical",
        extra_settings=(radical_divide_form_settings,),
        setting_defaults={
            "allow_reduced_quotients": True,
            "allow_simplify_quotients": False,
            "allow_rationalize_divide": False,
            "coef_min": 1,
            "coef_max": 6,
        },
    ),
    # Rational expressions
    "rational_simplification": TypeSettingConfig(
        setting_profile="polynomial_division",
        inherits=("polynomial_factoring",),
        exclude_settings=(
            "divide_cleanly",
            # Factoring-method toggles are unused: this type always builds from
            # linear factors so every difficulty stays classroom-factorable.
            "factor_rrt",
            "factor_normal",
            "factor_grouping",
            "factor_substitution",
            "factor_difference_of_squares",
            "factor_perfect_square_trinomial",
            "factor_difference_of_cubes",
            "factor_sum_of_cubes",
            "require_gcf",
            "difference_of_squares_only",
        ),
        setting_defaults={
            "numerator_degree_min": 2,
            "numerator_degree_max": 3,
            "denominator_degree_min": 2,
            "denominator_degree_max": 3,
            "leading_coefficient_one": True,
            "monic_only": True,
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
    "rational_expression_multiply_divide": TypeSettingConfig(
        setting_profile="polynomial",
        exclude_settings=(
            "min_degree",
            "max_degree",
            "variable",
            "integer_coefficients_only",
        ),
        extra_settings=(
            rational_multiply_divide_settings,
            division_notation_settings,
        ),
        setting_defaults={
            "allow_multiply": True,
            "allow_divide": True,
            "cancel_factor_count": 1,
            "max_factor_degree": 1,
            "expand_polynomials": False,
            "operand_count": 2,
            "leading_coefficient_one": True,
            "allow_obelus": True,
            "allow_complex_fraction": True,
            "allow_slash": False,
        },
    ),
    "rational_equations": TypeSettingConfig(
        inherits=("equation",),
        exclude_settings=(
            "steps",
            "include_graph_metadata",
            "allow_add",
            "allow_subtract",
            "allow_multiply",
            "allow_divide",
            *_TERM_SETTINGS,
            *_PHRASE_SETTINGS,
        ),
        extra_settings=(rational_equation_form_settings,),
        setting_defaults={
            "allow_simple_fraction": True,
            "allow_proportion": False,
            "allow_fraction_plus_constant": False,
            "allow_two_fractions": False,
            "integer_only": True,
        },
    ),
    # Exponential / misc
    "exponential_growth_decay": TypeSettingConfig(
        setting_profile="exponential",
        exclude_settings=(
            "exp_base_min",
            "exp_base_max",
            "exp_exponent_min",
            "exp_exponent_max",
            "allow_fractional_exponents",
            "coef_min",
            "coef_max",
        ),
        setting_defaults={"discrete_only": True},
    ),
    "properties_of_exponents": TypeSettingConfig(
        setting_profile="algebra_expression",
        exclude_settings=_excludes(
            _TERM_SETTINGS,
            extra=("term_count", "phrase_complexity", "constant_min", "constant_max"),
        ),
    ),
    "combining_like_terms": TypeSettingConfig(
        setting_profile="algebra_expression",
        exclude_settings=_excludes(_TERM_SETTINGS, extra=("phrase_complexity", "exponent_min", "exponent_max")),
    ),
    "g6_combining_like_terms": TypeSettingConfig(
        setting_profile="algebra_expression",
        exclude_settings=_excludes(_TERM_SETTINGS, extra=("phrase_complexity", "exponent_min", "exponent_max")),
    ),
    "verbal_expressions": TypeSettingConfig(
        setting_profile="algebra_expression",
        exclude_settings=_excludes(_TERM_SETTINGS, extra=("term_count", "exponent_min", "exponent_max")),
    ),
    "pa_verbal_expressions": TypeSettingConfig(
        setting_profile="algebra_expression",
        exclude_settings=_excludes(_TERM_SETTINGS, extra=("term_count", "exponent_min", "exponent_max")),
    ),
    "g6_writing_algebraic_expressions": TypeSettingConfig(
        setting_profile="algebra_expression",
        exclude_settings=_excludes(_TERM_SETTINGS, extra=("term_count", "exponent_min", "exponent_max")),
    ),
    # Trigonometry
    "trig_evaluate": TypeSettingConfig(
        setting_profile="trigonometry",
        setting_defaults={"unit_circle_only": True, "angle_max": 360},
    ),
    "simple_trig_equations": TypeSettingConfig(
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
            "ask_mode",
            "allow_growth",
            "allow_decay",
            "rate_min",
            "rate_max",
            "periods_min",
            "periods_max",
            "discrete_only",
            "allow_how_much_more",
            "allow_compare",
            "allow_threshold",
            "allow_half_life",
            "allow_fractional_periods",
            "allow_fractional_exponents",
        ),
    ),
    "exponential_equation_with_log": TypeSettingConfig(
        setting_profile="exponential",
        exclude_settings=(
            "ask_mode",
            "allow_growth",
            "allow_decay",
            "rate_min",
            "rate_max",
            "periods_min",
            "periods_max",
            "discrete_only",
            "allow_how_much_more",
            "allow_compare",
            "allow_threshold",
            "allow_half_life",
            "allow_fractional_periods",
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
    "sequence_arithmetic_geometric_mean": TypeSettingConfig(setting_profile="sequence"),
    "sequence_arithmetic_series": TypeSettingConfig(
        setting_profile="sequence",
        exclude_settings=("common_ratio_min", "common_ratio_max", "allow_negative_ratio"),
    ),
    "sequence_geometric_series": TypeSettingConfig(
        setting_profile="sequence",
        exclude_settings=("common_diff_min", "common_diff_max"),
        setting_defaults={"allow_negative_ratio": True},
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
    "derivative_product_rule": TypeSettingConfig(setting_profile="derivatives"),
    "derivative_quotient_rule": TypeSettingConfig(setting_profile="derivatives"),
    "derivative_chain_rule": TypeSettingConfig(setting_profile="derivatives"),
    "derivative_trigonometric": TypeSettingConfig(setting_profile="derivatives"),
    "derivative_implicit": TypeSettingConfig(setting_profile="derivatives"),
    "derivative_higher_order": TypeSettingConfig(setting_profile="derivatives"),
    "average_rate_of_change": TypeSettingConfig(setting_profile="derivatives"),
    "definition_of_derivative": TypeSettingConfig(setting_profile="derivatives"),
    "integral_trigonometric": TypeSettingConfig(setting_profile="integrals"),
    "integral_substitution": TypeSettingConfig(setting_profile="integrals"),
    "riemann_approximate_area": TypeSettingConfig(setting_profile="integrals"),
    "first_fundamental_theorem": TypeSettingConfig(setting_profile="integrals"),
    "area_under_curve": TypeSettingConfig(setting_profile="integrals"),
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
    "geo_triangles_and_quadrilaterals_area": TypeSettingConfig(
        setting_profile="geometry_basic",
    ),
    "geo_quadrilateral_area": TypeSettingConfig(setting_profile="geometry_basic"),
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
    "geo_similar_triangles": TypeSettingConfig(
        setting_profile="geometry_triangles",
        extra_settings=(similar_figures_prompt_settings,),
        setting_defaults={"prompt_style": "diagram", "include_figure": True, "include_diagram": True},
    ),
    "geo_circle_measure": TypeSettingConfig(setting_profile="geometry_circles"),
    "geo_coordinate_distance": TypeSettingConfig(
        setting_profile="coordinate_geometry",
        setting_defaults={"include_graph_metadata": True},
    ),
    "g6_coordinate_perimeter": TypeSettingConfig(
        setting_profile="coordinate_geometry",
        setting_defaults={
            "include_diagram": True,
            "coord_min": 0,
            "coord_max": 8,
            "max_side": 5,
            "allow_l_shape": False,
        },
    ),
    "geo_angle_addition": TypeSettingConfig(setting_profile="geometry_angles"),
    "geo_segment_addition": TypeSettingConfig(setting_profile="geometry_basic"),
    "geo_angle_relationships": TypeSettingConfig(setting_profile="geometry_angles"),
    "finding_angles": TypeSettingConfig(setting_profile="geometry_angles"),
    "geo_exterior_angle": TypeSettingConfig(setting_profile="geometry_triangles"),
    "geo_classifying_triangles": TypeSettingConfig(setting_profile="geometry_triangles"),
    "geo_isosceles_triangle": TypeSettingConfig(setting_profile="geometry_triangles"),
    "geo_parallel_transversal": TypeSettingConfig(setting_profile="geometry_angles"),
    "geo_triangle_inequality": TypeSettingConfig(setting_profile="geometry_triangles"),
    "geo_special_right_triangle": TypeSettingConfig(setting_profile="geometry_triangles"),
    "geo_polygon_interior": TypeSettingConfig(setting_profile="geometry_angles"),
    "geo_parallelogram_area": TypeSettingConfig(setting_profile="geometry_basic"),
    "geo_rectangle_area": TypeSettingConfig(setting_profile="geometry_basic"),
    "geo_square_area": TypeSettingConfig(setting_profile="geometry_basic"),
    "geo_rhombus_area": TypeSettingConfig(setting_profile="geometry_basic"),
    "geo_trapezoid_area": TypeSettingConfig(setting_profile="geometry_basic"),
    "geo_kite_area": TypeSettingConfig(setting_profile="geometry_basic"),
    "geo_central_arc": TypeSettingConfig(setting_profile="geometry_circles"),
    "geo_inscribed_angle": TypeSettingConfig(setting_profile="geometry_circles"),
    "geo_arc_sector": TypeSettingConfig(setting_profile="geometry_circles"),
    "geo_solid_volume_surface": TypeSettingConfig(setting_profile="geometry_basic"),
    "geo_right_triangle_trig": TypeSettingConfig(setting_profile="geometry_triangles"),
    "geo_right_triangle_trig_ratio": TypeSettingConfig(setting_profile="geometry_triangles"),
    "geo_right_triangle_trig_angle": TypeSettingConfig(setting_profile="geometry_triangles"),
    "geo_right_triangle_trig_side": TypeSettingConfig(setting_profile="geometry_triangles"),
    "law_of_sines": TypeSettingConfig(setting_profile="geometry_triangles"),
    "law_of_cosines": TypeSettingConfig(setting_profile="geometry_triangles"),
    "binomial_theorem": TypeSettingConfig(setting_profile="polynomial"),
    "remainder_theorem": TypeSettingConfig(setting_profile="polynomial"),
    "compound_interest": TypeSettingConfig(setting_profile="percent"),
    "writing_numeric_expressions": TypeSettingConfig(
        setting_profile="writing_numeric_expressions"
    ),
    "g6_writing_numeric_expressions": TypeSettingConfig(
        setting_profile="writing_numeric_expressions"
    ),
    "g6_decimal_divide": TypeSettingConfig(setting_profile="decimal"),
    "vector_basics": TypeSettingConfig(setting_profile="coordinate_plane"),
    "dot_product": TypeSettingConfig(setting_profile="coordinate_plane"),
    "polar_coordinates": TypeSettingConfig(setting_profile="geometry_angles"),
    "limit_removable": TypeSettingConfig(setting_profile="limits"),
    "related_rates_simple": TypeSettingConfig(setting_profile="derivatives"),
    "derivative_ln_exp": TypeSettingConfig(setting_profile="derivatives"),
    "intervals_increase_decrease": TypeSettingConfig(setting_profile="derivatives"),
    "lhopitals_rule": TypeSettingConfig(setting_profile="limits"),
    "area_between_curves": TypeSettingConfig(setting_profile="integrals"),
    "inverse_trig_functions": TypeSettingConfig(setting_profile="trigonometry"),
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
    "stats_statistical_model": TypeSettingConfig(
        setting_profile="statistics",
        exclude_settings=(
            "measure_type",
            "probability_format",
            "data_set_size_min",
            "data_set_size_max",
            "value_min",
            "value_max",
            "integer_data_only",
        ),
    ),
    "g6_drawing_dot_plot": TypeSettingConfig(
        extra_settings=(chart_drawing_settings,),
        setting_defaults={"include_axis": True},
    ),
    "g6_drawing_histogram": TypeSettingConfig(
        extra_settings=(chart_drawing_settings,),
        setting_defaults={"include_axis": True},
    ),
    "conic_rotation_identify": TypeSettingConfig(setting_profile="polynomial"),
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
    "stats_permutations": TypeSettingConfig(
        setting_profile="statistics",
        exclude_settings=("measure_type", "probability_format", "data_set_size_min", "data_set_size_max", "value_min", "value_max", "integer_data_only"),
    ),
    "stats_combinations": TypeSettingConfig(
        setting_profile="statistics",
        exclude_settings=("measure_type", "probability_format", "data_set_size_min", "data_set_size_max", "value_min", "value_max", "integer_data_only"),
    ),
    "stats_permutations_vs_combinations": TypeSettingConfig(
        setting_profile="statistics",
        exclude_settings=("measure_type", "probability_format", "data_set_size_min", "data_set_size_max", "value_min", "value_max", "integer_data_only"),
    ),
    # Word problems
    "wp_distance_rate_time": TypeSettingConfig(
        setting_profile="word_problem",
        extra_settings=(distance_rate_time_settings,),
        exclude_settings=("answer_units", "max_steps"),
        setting_defaults={
            "allow_drt_find_missing": True,
            "allow_drt_round_trip": False,
            "allow_drt_two_segments": False,
            "allow_drt_opposite": False,
            "allow_drt_same_direction": False,
            "allow_distance_mi": True,
            "allow_distance_km": True,
            "allow_distance_m": True,
            "allow_distance_ft": True,
            "allow_time_hr": True,
            "allow_time_min": True,
        },
    ),
    "wp_work": TypeSettingConfig(
        setting_profile="word_problem",
        extra_settings=(work_problem_settings,),
        exclude_settings=("answer_units", "max_steps"),
        setting_defaults={
            "allow_work_together": True,
            "allow_work_find_one_rate": True,
            "allow_work_three": False,
            "allow_work_find_one_time": False,
            "allow_work_starts_later": False,
            "allow_work_pipes": False,
            "allow_work_time_hr": True,
            "allow_work_time_min": True,
        },
    ),
    "wp_age": TypeSettingConfig(setting_profile="word_problem"),
    "wp_consecutive_integers": TypeSettingConfig(
        setting_profile="word_problem",
        extra_settings=(consecutive_integers_settings,),
        exclude_settings=("max_steps",),
    ),
    "wp_coin": TypeSettingConfig(setting_profile="word_problem"),
    "wp_mixture": TypeSettingConfig(setting_profile="word_problem"),
    "wp_perimeter_area": TypeSettingConfig(setting_profile="word_problem"),
    "wp_percent": TypeSettingConfig(
        setting_profile="word_problem",
        extra_settings=(percent_word_problem_settings,),
        setting_defaults={
            "allow_discount": True,
            "allow_tax": True,
            "allow_markup": True,
            "allow_tip": True,
            "allow_price_cents": False,
            "allow_decimal_rates": False,
            "allow_multi_step": False,
            "integer_only_answers": False,
        },
    ),
    "pa_markup_discount_and_tax": TypeSettingConfig(
        setting_profile="word_problem",
        extra_settings=(percent_word_problem_settings,),
        setting_defaults={
            "allow_discount": True,
            "allow_tax": True,
            "allow_markup": True,
            "allow_tip": True,
            "allow_price_cents": False,
            "allow_decimal_rates": False,
            "allow_multi_step": False,
            "integer_only_answers": False,
        },
        count_default=5,
    ),
    "percent_word_problems": TypeSettingConfig(
        setting_profile="word_problem",
        extra_settings=(percent_word_problem_settings,),
        setting_defaults={
            "allow_discount": True,
            "allow_tax": True,
            "allow_markup": True,
            "allow_tip": True,
            "allow_price_cents": False,
            "allow_decimal_rates": False,
            "allow_multi_step": False,
            "integer_only_answers": False,
        },
        count_default=5,
    ),
    "wp_simple_and_compound_interest": TypeSettingConfig(
        setting_profile="word_problem"
    ),
    "pa_simple_and_compound_interest": TypeSettingConfig(
        setting_profile="word_problem"
    ),
    "wp_proportion": TypeSettingConfig(setting_profile="word_problem"),
    "wp_one_step_equation": TypeSettingConfig(setting_profile="word_problem"),
    "wp_two_step_equation": TypeSettingConfig(setting_profile="word_problem"),
    "wp_systems": TypeSettingConfig(setting_profile="word_problem"),
    "wp_inequality": TypeSettingConfig(setting_profile="word_problem"),
    "wp_gcf_lcm": TypeSettingConfig(
        setting_profile="word_problem",
        extra_settings=(gcf_constraint_settings,),
        setting_defaults={"require_gcf_greater_than_one": True},
    ),
    "wp_number_line": TypeSettingConfig(
        setting_profile="word_problem",
        extra_settings=(number_line_range_settings,),
        setting_defaults={"include_graph_metadata": True},
    ),
    "wp_coordinate_distance": TypeSettingConfig(setting_profile="word_problem"),
    "wp_similar_figures": TypeSettingConfig(
        setting_profile="word_problem",
        extra_settings=(similar_figures_prompt_settings,),
        setting_defaults={"prompt_style": "diagram", "include_figure": True},
    ),
    # Consolidation: previously unprofiled Ready generators (session scaffolds).
    "trig_sum_difference": TypeSettingConfig(setting_profile="trigonometry"),
    "trig_multiple_angle": TypeSettingConfig(setting_profile="trigonometry"),
    "trig_product_to_sum": TypeSettingConfig(setting_profile="trigonometry"),
    "trig_factoring_equations": TypeSettingConfig(setting_profile="trigonometry"),
    "vector_3d_basics": TypeSettingConfig(setting_profile="algebra_expression"),
    "precalc_foundations": TypeSettingConfig(setting_profile="algebra_expression"),
    "calculus_foundations": TypeSettingConfig(setting_profile="derivatives"),
    "derivative_inverse_trig": TypeSettingConfig(setting_profile="derivatives"),
    "derivative_other_base": TypeSettingConfig(setting_profile="derivatives"),
    "derivative_from_tables": TypeSettingConfig(setting_profile="derivatives"),
    "rolles_theorem": TypeSettingConfig(setting_profile="derivatives"),
    "mean_value_theorem": TypeSettingConfig(setting_profile="derivatives"),
    "integral_log_exp": TypeSettingConfig(setting_profile="integrals"),
    "integral_inverse_trig": TypeSettingConfig(setting_profile="integrals"),
    "integration_by_parts": TypeSettingConfig(setting_profile="integrals"),
    "riemann_sum_tables": TypeSettingConfig(setting_profile="integrals"),
    "second_fundamental_theorem": TypeSettingConfig(setting_profile="integrals"),
    "def_int_mean_value": TypeSettingConfig(setting_profile="integrals"),
    "volume_disk_washer": TypeSettingConfig(setting_profile="integrals"),
    "volume_shell": TypeSettingConfig(setting_profile="integrals"),
    "volume_cross_sections": TypeSettingConfig(setting_profile="integrals"),
    "slope_field_interpret": TypeSettingConfig(setting_profile="derivatives"),
    "separable_diff_eq": TypeSettingConfig(setting_profile="derivatives"),
    "angle_measure": TypeSettingConfig(setting_profile="geometry_angles"),
    "degrees_minutes_seconds": TypeSettingConfig(setting_profile="geometry_angles"),
    "descartes_rule_of_signs": TypeSettingConfig(setting_profile="polynomial"),
    "fundamental_theorem_algebra": TypeSettingConfig(setting_profile="polynomial"),
    "rational_zero_root_theorem": TypeSettingConfig(setting_profile="polynomial"),
    "polynomial_conjugate_writing": TypeSettingConfig(setting_profile="polynomial"),
    "polynomial_end_behavior": TypeSettingConfig(setting_profile="polynomial"),
    "polynomial_writing": TypeSettingConfig(setting_profile="polynomial"),
    "inverse_exponential_logarithmic": TypeSettingConfig(setting_profile="logarithm"),
    "graphing_trig_functions": TypeSettingConfig(setting_profile="trigonometry"),
    "matrix_cramers_rule": TypeSettingConfig(setting_profile="algebra_expression"),
    "matrix_inverse": TypeSettingConfig(setting_profile="algebra_expression"),
    "matrix_transformation": TypeSettingConfig(setting_profile="algebra_expression"),
    "quadratic_system": TypeSettingConfig(setting_profile="systems"),
    "system_three_variables": TypeSettingConfig(setting_profile="systems"),
    "radical_domain_range": TypeSettingConfig(setting_profile="radical"),
    "points_three_dimensions": TypeSettingConfig(setting_profile="coordinate_plane"),
    "planes": TypeSettingConfig(setting_profile="coordinate_plane"),
    "g6_area_model_algebraic": TypeSettingConfig(setting_profile="distributive"),
    "g6_classify_polyhedron": TypeSettingConfig(setting_profile="geometry_basic"),
    "g6_equations_hanger_diagrams": TypeSettingConfig(setting_profile="equation"),
    "g6_equations_tape_diagrams": TypeSettingConfig(setting_profile="equation"),
    "g6_inequalities_hanger_diagrams": TypeSettingConfig(setting_profile="inequality"),
    "g6_fraction_prism_volume": TypeSettingConfig(setting_profile="geometry_basic"),
    "g6_fraction_rectangle_area": TypeSettingConfig(setting_profile="geometry_basic"),
    "g6_fraction_triangle_area": TypeSettingConfig(setting_profile="geometry_basic"),
    "g6_polygon_grid_area": TypeSettingConfig(setting_profile="geometry_basic"),
    "g6_shaded_polygon_area": TypeSettingConfig(setting_profile="geometry_basic"),
    "geo_circle_chords": TypeSettingConfig(setting_profile="geometry_circles"),
    "geo_circle_equation_using": TypeSettingConfig(setting_profile="geometry_circles"),
    "geo_circle_equation_writing": TypeSettingConfig(setting_profile="geometry_circles"),
    "geo_circle_segment_measures": TypeSettingConfig(setting_profile="geometry_circles"),
    "geo_circle_tangents": TypeSettingConfig(setting_profile="geometry_circles"),
    "geo_secant_tangent_segments": TypeSettingConfig(setting_profile="geometry_circles"),
    "geo_construction_altitudes": TypeSettingConfig(setting_profile="geometry_basic"),
    "geo_construction_angles": TypeSettingConfig(setting_profile="geometry_angles"),
    "geo_construction_bisectors": TypeSettingConfig(setting_profile="geometry_angles"),
    "geo_construction_circles": TypeSettingConfig(setting_profile="geometry_circles"),
    "geo_construction_medians": TypeSettingConfig(setting_profile="geometry_triangles"),
    "geo_construction_perpendicular": TypeSettingConfig(setting_profile="geometry_basic"),
    "geo_construction_segments": TypeSettingConfig(setting_profile="geometry_basic"),
    "geo_construction_triangles": TypeSettingConfig(setting_profile="geometry_triangles"),
    "geo_geometric_notation": TypeSettingConfig(setting_profile="geometry_basic"),
    "geo_proportional_parts": TypeSettingConfig(setting_profile="geometry_triangles"),
    "geo_quadrilateral_classifying": TypeSettingConfig(setting_profile="geometry_basic"),
    "geo_regular_polygon_area": TypeSettingConfig(setting_profile="geometry_basic"),
    "geo_similar_polygons": TypeSettingConfig(
        setting_profile="geometry_triangles",
        extra_settings=(similar_figures_prompt_settings,),
        setting_defaults={"prompt_style": "diagram", "include_figure": True, "include_diagram": True},
    ),
    "geo_transformations": TypeSettingConfig(
        setting_profile="coordinate_plane",
        setting_defaults={
            "include_graph_metadata": True,
            "include_diagram": True,
            "show_preimage_graph": True,
        },
    ),
    "geo_triangle_angle_bisector": TypeSettingConfig(setting_profile="geometry_triangles"),
    "geo_triangle_centroid": TypeSettingConfig(setting_profile="geometry_triangles"),
    "geo_triangle_congruence": TypeSettingConfig(setting_profile="geometry_triangles"),
    "geo_triangle_congruence_proof": TypeSettingConfig(setting_profile="geometry_triangles"),
    "geo_triangle_median": TypeSettingConfig(setting_profile="geometry_triangles"),
    "geo_triangle_midsegment": TypeSettingConfig(setting_profile="geometry_triangles"),
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
