"""Reusable domain setting profiles composed from atomic field builders."""

from __future__ import annotations

from ..core.models import SettingField
from .domains.equation import (
    equation_coef_settings,
    equation_operation_settings,
    equation_solution_settings,
    equation_variable_settings,
)
from .domains.geometry import (
    angle_bounds_settings,
    angle_unit_settings,
    circle_radius_settings,
    geometry_metadata_settings,
    geometry_settings,
    measurement_unit_settings,
    polygon_sides_settings,
    proof_difficulty_settings,
    side_length_settings,
    similarity_ratio_settings,
    triangle_type_settings,
)
from .domains.graphing import (
    absolute_value_graph_settings,
    exponential_graph_settings,
    graph_dimension_settings,
    graphing_metadata_settings,
    number_line_range_settings,
    polynomial_solve_graph_settings,
    quadratic_graph_settings,
)
from .domains.inequality import (
    compound_inequality_settings,
    inequality_direction_settings,
    inequality_settings,
)
from .domains.linear import (
    coordinate_bounds_settings,
    linear_intercept_settings,
    linear_slope_settings,
    more_on_slope_settings,
    quadrant_settings,
    relations_settings,
    systems_settings,
    variation_settings,
)
from .domains.number import (
    allow_negative_settings,
    decimal_places_settings,
    denominator_settings,
    factor_bounds_settings,
    number_coef_settings,
    pemdas_settings,
    percent_settings,
    prime_factorization_settings,
    ratio_settings,
    scientific_notation_settings,
    sets_of_numbers_settings,
    writing_numeric_expression_settings,
    unit_rate_settings,
)
from .domains.common import (
    answer_format_settings,
    difficulty_settings,
    multiple_choice_settings,
    primitive_layered_settings,
    sign_restrictions,
)
from .domains.misc import misc_expression_settings
from .domains.polynomial import (
    polynomial_coef_settings,
    polynomial_degree_settings,
    polynomial_division_settings,
    polynomial_factoring_settings,
    polynomial_variable_settings,
)
from .domains.radical import radical_settings
from .domains.rational import fraction_form_settings
from .domains.calculus import derivative_settings, integral_settings, limit_settings
from .domains.logarithm import exponential_equation_settings, logarithm_settings
from .domains.sequence import sequence_settings
from .domains.trigonometry import trigonometry_settings
from .domains.word_problem import word_problem_settings
from .domains.statistics import statistics_settings
from .standard import merge_settings


def polynomial_settings() -> list[SettingField]:
    """Core polynomial customization: degree, coefficients, variable."""
    return merge_settings(
        polynomial_degree_settings(),
        polynomial_coef_settings(),
        polynomial_variable_settings(),
    )


def polynomial_factoring_profile() -> list[SettingField]:
    """Polynomial factoring types inherit polynomial + method toggles."""
    return merge_settings(
        polynomial_settings(),
        polynomial_factoring_settings(),
    )


def polynomial_division_profile() -> list[SettingField]:
    """Long division and rational-expression degree controls."""
    return merge_settings(
        polynomial_coef_settings(),
        polynomial_division_settings(),
        polynomial_variable_settings(),
    )


def equation_settings() -> list[SettingField]:
    """Linear equation solving: coefficients, variable, solution type, operations."""
    return merge_settings(
        equation_coef_settings(),
        equation_variable_settings(),
        equation_solution_settings(),
        equation_operation_settings(),
    )


def inequality_profile() -> list[SettingField]:
    """Inequality solving inherits equation bounds plus graph/step options."""
    return merge_settings(
        equation_coef_settings(),
        equation_variable_settings(),
        equation_solution_settings(),
        inequality_settings(),
        inequality_direction_settings(),
        number_line_range_settings(),
        graphing_metadata_settings(),
    )


def compound_inequality_profile() -> list[SettingField]:
    """Compound inequalities: base inequality profile plus and/or style."""
    return merge_settings(
        inequality_profile(),
        compound_inequality_settings(),
    )


def number_settings() -> list[SettingField]:
    """Rational / numeric expression bounds."""
    return merge_settings(
        number_coef_settings(),
        denominator_settings(),
        allow_negative_settings(),
    )


def rational_settings() -> list[SettingField]:
    """Rational arithmetic and expression types."""
    return merge_settings(
        number_settings(),
        fraction_form_settings(),
        polynomial_coef_settings(coef_min_default=-10, coef_max_default=10),
    )


def percent_profile() -> list[SettingField]:
    return merge_settings(
        percent_settings(),
    )


def decimal_profile() -> list[SettingField]:
    return merge_settings(
        decimal_places_settings(),
        allow_negative_settings(default=False),
    )


def ratio_profile() -> list[SettingField]:
    return merge_settings(
        ratio_settings(),
    )


def unit_rate_profile() -> list[SettingField]:
    return merge_settings(
        unit_rate_settings(),
    )


def scientific_notation_profile() -> list[SettingField]:
    return merge_settings(
        scientific_notation_settings(),
    )


def proportion_profile() -> list[SettingField]:
    return merge_settings(
        ratio_settings(part_min_default=2, part_max_default=12),
    )


def order_of_operations_profile() -> list[SettingField]:
    return primitive_layered_settings(
        primitive_ids=["numbers", "variable", "ooo"],
        include_number_profile=True,
        default_d=6,
    )


def writing_numeric_expressions_profile() -> list[SettingField]:
    return merge_settings(
        writing_numeric_expression_settings(),
        number_coef_settings(num_min_default=2, num_max_default=20, num_bound=50),
    )


def integer_profile() -> list[SettingField]:
    return merge_settings(
        number_coef_settings(num_min_default=-20, num_max_default=20, num_bound=50),
        allow_negative_settings(),
    )


def number_sets_profile() -> list[SettingField]:
    """Classify numbers into natural, whole, integer, rational, irrational, real."""
    return sets_of_numbers_settings()


def factor_profile() -> list[SettingField]:
    return merge_settings(
        factor_bounds_settings(),
        prime_factorization_settings(),
    )


def distributive_profile() -> list[SettingField]:
    return primitive_layered_settings(
        primitive_ids=["numbers", "variable", "distributive"],
        include_number_profile=True,
        default_d=5,
    )


def evaluate_expressions_profile() -> list[SettingField]:
    """Settings for evaluate-linear-expressions (catalog leaves still map here)."""
    return primitive_layered_settings(
        primitive_ids=["numbers", "variable", "evaluate"],
        include_number_profile=True,
        default_d=5,
    )


def evaluate_linear_expressions_profile() -> list[SettingField]:
    return evaluate_expressions_profile()


def like_terms_profile() -> list[SettingField]:
    return primitive_layered_settings(
        primitive_ids=["numbers", "variable", "like_terms"],
        include_number_profile=True,
        default_d=5,
    )


def expand_simplify_profile() -> list[SettingField]:
    return primitive_layered_settings(
        primitive_ids=["numbers", "variable", "expand_simplify"],
        include_number_profile=True,
        default_d=5,
    )


def constructive_rational_profile() -> list[SettingField]:
    return primitive_layered_settings(
        primitive_ids=["numbers", "variable"],
        include_number_profile=True,
        default_d=6,
    )


def partial_fraction_profile() -> list[SettingField]:
    return primitive_layered_settings(
        primitive_ids=["numbers", "variable"],
        include_number_profile=True,
        default_d=6,
    )


def primitive_equations_profile() -> list[SettingField]:
    return primitive_layered_settings(
        primitive_ids=["numbers", "variable", "equations"],
        include_number_profile=True,
        default_d=5,
    )


def primitive_inequalities_profile() -> list[SettingField]:
    return primitive_layered_settings(
        primitive_ids=["numbers", "variable", "inequalities"],
        include_number_profile=True,
        default_d=5,
    )


def factor_gcf_profile() -> list[SettingField]:
    return primitive_layered_settings(
        primitive_ids=["numbers", "variable", "factor_gcf"],
        include_number_profile=True,
        default_d=5,
    )


def linear_settings() -> list[SettingField]:
    """Slope, intercept, and coordinate-plane bounds."""
    return merge_settings(
        linear_slope_settings(),
        linear_intercept_settings(),
        coordinate_bounds_settings(),
        quadrant_settings(),
        graphing_metadata_settings(),
    )


def more_on_slope_profile() -> list[SettingField]:
    """More on slope: linear bounds plus multi-mode ask toggles."""
    return merge_settings(
        linear_settings(),
        more_on_slope_settings(),
    )


def coordinate_plane_settings() -> list[SettingField]:
    """Coordinate-plane types without slope/intercept controls."""
    return merge_settings(
        coordinate_bounds_settings(),
        quadrant_settings(),
        graphing_metadata_settings(),
    )


def number_line_profile() -> list[SettingField]:
    """1D number-line types: range, optional zero mark, and graph metadata."""
    return merge_settings(
        number_line_range_settings(),
        graphing_metadata_settings(),
    )


def graphing_profile() -> list[SettingField]:
    """Graphing generators: bounds, grid, number line, and table options."""
    return merge_settings(
        linear_slope_settings(),
        linear_intercept_settings(),
        coordinate_bounds_settings(),
        quadrant_settings(),
        graphing_metadata_settings(),
        graph_dimension_settings(),
        number_line_range_settings(),
        relations_settings(),
    )


def systems_profile() -> list[SettingField]:
    """Linear systems: coefficient bounds, size, and method weights."""
    return merge_settings(
        linear_intercept_settings(),
        linear_slope_settings(),
        coordinate_bounds_settings(),
        systems_settings(),
    )


def variation_profile() -> list[SettingField]:
    """Direct and inverse variation constant bounds and mix weights."""
    return merge_settings(
        variation_settings(),
    )


def relations_profile() -> list[SettingField]:
    """Function/relation evaluation with linear parameters and tables."""
    return merge_settings(
        linear_slope_settings(),
        linear_intercept_settings(),
        coordinate_bounds_settings(),
        relations_settings(),
        graphing_metadata_settings(),
    )


def geometry_basic_profile() -> list[SettingField]:
    """Segment lengths, units, and diagram metadata."""
    return merge_settings(
        geometry_metadata_settings(),
        measurement_unit_settings(),
        side_length_settings(),
    )


def geometry_angles_profile() -> list[SettingField]:
    """Angle measure and classification types."""
    return merge_settings(
        geometry_basic_profile(),
        angle_bounds_settings(),
        angle_unit_settings(),
    )


def geometry_triangles_profile() -> list[SettingField]:
    """Triangle measures, area, perimeter, and similarity."""
    return merge_settings(
        geometry_basic_profile(),
        angle_bounds_settings(),
        angle_unit_settings(),
        triangle_type_settings(),
        similarity_ratio_settings(),
        proof_difficulty_settings(),
    )


def geometry_circles_profile() -> list[SettingField]:
    """Circle circumference, area, and arc types."""
    return merge_settings(
        geometry_basic_profile(),
        circle_radius_settings(),
        angle_bounds_settings(angle_min_default=30, angle_max_default=330),
    )


def coordinate_geometry_profile() -> list[SettingField]:
    """Coordinate-plane geometry; reuses linear bounds where they overlap."""
    return merge_settings(
        geometry_metadata_settings(),
        coordinate_bounds_settings(),
        quadrant_settings(),
        graphing_metadata_settings(),
    )


def radical_profile() -> list[SettingField]:
    return radical_settings()


def quadratic_profile() -> list[SettingField]:
    """Quadratic equation / expression types."""
    return merge_settings(
        polynomial_coef_settings(coef_min_default=-12, coef_max_default=12),
        polynomial_degree_settings(min_degree_default=2, max_degree_default=2),
        polynomial_factoring_settings(),
    )


def quadratic_graph_profile() -> list[SettingField]:
    """Graphing quadratic functions: form toggles, transforms, and plane metadata."""
    return merge_settings(
        quadratic_graph_settings(),
        linear_intercept_settings(),
        coordinate_bounds_settings(),
        graphing_metadata_settings(),
    )


def quadratic_inequality_graph_profile() -> list[SettingField]:
    """Graphing quadratic inequalities: forms, symbols, and plane metadata."""
    return merge_settings(
        quadratic_graph_profile(),
        inequality_direction_settings(),
    )


def polynomial_solve_graph_profile() -> list[SettingField]:
    """Solve polynomial equations by graphing: monic/stretch, roots, degree, plane."""
    return merge_settings(
        polynomial_solve_graph_settings(),
        coordinate_bounds_settings(),
        graphing_metadata_settings(),
    )


def exponential_growth_decay_settings() -> list[SettingField]:
    return [
        SettingField(
            "ask_mode",
            "Question style",
            "select",
            "find_final",
            options=[
                "find_final",
                "find_rate",
                "find_periods",
                "find_initial",
                "mixed",
            ],
            group="exponential",
        ),
        SettingField(
            "allow_growth",
            "Allow growth problems",
            "bool",
            True,
            group="exponential",
        ),
        SettingField(
            "allow_decay",
            "Allow decay problems",
            "bool",
            True,
            group="exponential",
        ),
        SettingField(
            "rate_min",
            "Rate min (%)",
            "int",
            5,
            min=1,
            max=50,
            group="exponential",
        ),
        SettingField(
            "rate_max",
            "Rate max (%)",
            "int",
            20,
            min=1,
            max=50,
            group="exponential",
        ),
        SettingField(
            "periods_min",
            "Periods min",
            "int",
            2,
            min=1,
            max=20,
            group="exponential",
        ),
        SettingField(
            "periods_max",
            "Periods max",
            "int",
            6,
            min=1,
            max=20,
            group="exponential",
        ),
        SettingField(
            "discrete_only",
            "Discrete (compound) model only",
            "bool",
            True,
            group="exponential",
        ),
        SettingField(
            "allow_how_much_more",
            "Allow “how much more” questions",
            "bool",
            False,
            group="exponential",
        ),
        SettingField(
            "allow_compare",
            "Allow compare-two-investments questions",
            "bool",
            False,
            group="exponential",
        ),
        SettingField(
            "allow_threshold",
            "Allow “when exceeds threshold” questions",
            "bool",
            False,
            group="exponential",
        ),
        SettingField(
            "allow_half_life",
            "Allow discrete half-life questions",
            "bool",
            False,
            group="exponential",
        ),
        SettingField(
            "allow_fractional_periods",
            "Allow fractional periods",
            "bool",
            False,
            group="exponential",
        ),
    ]


def exponential_profile() -> list[SettingField]:
    """Exponential equations and growth/decay word problems."""
    return merge_settings(
        exponential_growth_decay_settings(),
        exponential_equation_settings(),
    )


def exponential_graph_profile() -> list[SettingField]:
    """Graphing exponential functions: form toggles, bounds, and plane metadata."""
    return merge_settings(
        exponential_graph_settings(),
        coordinate_bounds_settings(),
        graphing_metadata_settings(),
    )


def absolute_value_graph_profile() -> list[SettingField]:
    """Graphing absolute-value equations: transform toggles, coefs, and plane metadata."""
    return merge_settings(
        absolute_value_graph_settings(),
        linear_intercept_settings(),
        coordinate_bounds_settings(),
        graphing_metadata_settings(),
    )


def trigonometry_profile() -> list[SettingField]:
    return trigonometry_settings()


def logarithm_profile() -> list[SettingField]:
    return logarithm_settings()


def sequence_profile() -> list[SettingField]:
    return sequence_settings()


def limits_profile() -> list[SettingField]:
    return limit_settings()


def derivatives_profile() -> list[SettingField]:
    return derivative_settings()


def integrals_profile() -> list[SettingField]:
    return integral_settings()


def algebra_expression_profile() -> list[SettingField]:
    """Simplifying expressions, like terms, verbal expressions."""
    return merge_settings(
        equation_coef_settings(coef_min_default=-12, coef_max_default=12),
        misc_expression_settings(),
    )


def statistics_profile() -> list[SettingField]:
    """Data set size, integer data, and probability formatting."""
    return statistics_settings()


def common_enrichment_profile() -> list[SettingField]:
    """Cross-cutting enrichment mixin: difficulty, answer format, signs, MC.

    Term-count controls live on domain profiles / extras that actually use them
    (e.g. radical add/subtract), not on every generator.
    """
    return merge_settings(
        difficulty_settings(),
        answer_format_settings(),
        sign_restrictions(),
        multiple_choice_settings(),
    )


PROFILE_BUILDERS: dict[str, callable] = {
    "common_enrichment": common_enrichment_profile,
    "polynomial": polynomial_settings,
    "polynomial_factoring": polynomial_factoring_profile,
    "polynomial_division": polynomial_division_profile,
    "equation": equation_settings,
    "inequality": inequality_profile,
    "compound_inequality": compound_inequality_profile,
    "number": number_settings,
    "rational": rational_settings,
    "percent": percent_profile,
    "decimal": decimal_profile,
    "ratio": ratio_profile,
    "unit_rate": unit_rate_profile,
    "scientific_notation": scientific_notation_profile,
    "proportion": proportion_profile,
    "order_of_operations": order_of_operations_profile,
    "writing_numeric_expressions": writing_numeric_expressions_profile,
    "integer": integer_profile,
    "number_sets": number_sets_profile,
    "factor": factor_profile,
    "distributive": distributive_profile,
    "evaluate_expressions": evaluate_expressions_profile,
    "evaluate_linear_expressions": evaluate_linear_expressions_profile,
    "like_terms": like_terms_profile,
    "expand_simplify": expand_simplify_profile,
    "constructive_rational": constructive_rational_profile,
    "partial_fraction": partial_fraction_profile,
    "primitive_equations": primitive_equations_profile,
    "primitive_inequalities": primitive_inequalities_profile,
    "factor_gcf": factor_gcf_profile,
    "linear": linear_settings,
    "more_on_slope": more_on_slope_profile,
    "coordinate_plane": coordinate_plane_settings,
    "number_line": number_line_profile,
    "graphing": graphing_profile,
    "absolute_value_graph": absolute_value_graph_profile,
    "systems": systems_profile,
    "variation": variation_profile,
    "relations": relations_profile,
    "radical": radical_profile,
    "quadratic": quadratic_profile,
    "quadratic_graph": quadratic_graph_profile,
    "quadratic_inequality_graph": quadratic_inequality_graph_profile,
    "polynomial_solve_graph": polynomial_solve_graph_profile,
    "exponential": exponential_profile,
    "exponential_graph": exponential_graph_profile,
    "trigonometry": trigonometry_profile,
    "logarithm": logarithm_profile,
    "sequence": sequence_profile,
    "limits": limits_profile,
    "derivatives": derivatives_profile,
    "integrals": integrals_profile,
    "algebra_expression": algebra_expression_profile,
    "word_problem": word_problem_settings,
    "geometry": geometry_settings,
    "geometry_basic": geometry_basic_profile,
    "geometry_angles": geometry_angles_profile,
    "geometry_triangles": geometry_triangles_profile,
    "geometry_circles": geometry_circles_profile,
    "coordinate_geometry": coordinate_geometry_profile,
    "statistics": statistics_profile,
}
