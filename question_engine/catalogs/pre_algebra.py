COURSE_ID = "pre_algebra"

CATEGORY_ORDER: tuple[str, ...] = (
    # OpenStax Prealgebra 2e spine (catalog chapter labels still use prior names where content lives)
    'Pre-Algebra — Integers, Decimals, and Fractions',  # maps → Whole Numbers / Integers / Fractions / Decimals
    'Pre-Algebra — Beginning Algebra',  # Language of Algebra
    'Pre-Algebra — Equations',  # Solving Linear Equations
    'Pre-Algebra — Percents',
    'Pre-Algebra — Plane Figures',  # Math Models and Geometry
    'Pre-Algebra — Beginning Polynomials',
    'Pre-Algebra — Linear Equations and Inequalities',  # Graphs
    # Supplemental
    'Pre-Algebra — Inequalities',
    'Pre-Algebra — Factors and Exponents',
    'Pre-Algebra — Proportions and Similarity',
    'Pre-Algebra — Right Triangles',
    'Pre-Algebra — Solid Figures',
    'Pre-Algebra — Statistics',
)

from .base import TypeCatalogEntry, resolve_instruction_latex, resolve_instruction_text



def _pa(
    chapter: str,
    id: str,
    name: str,
    *,
    instruction_latex: str = "",
    instruction_text: str = "",
    count_default: int = 10,
    generator: str = "scaffold",
) -> TypeCatalogEntry:
    return TypeCatalogEntry(
        id=id,
        name=name,
        category=f"Pre-Algebra — {chapter}",
        generator=generator,
        description=f"Practice {name.lower()}.",
        instruction_latex=resolve_instruction_latex(instruction_latex, instruction_text),
        instruction_text=resolve_instruction_text(instruction_text),
        count_default=count_default,
    )


CATALOG: tuple[TypeCatalogEntry, ...] = (
    # Integers, Decimals, and Fractions
    _pa(
        "Integers, Decimals, and Fractions",
        "pa_naming_decimal_places_and_rounding",
        "Naming decimal places and rounding", generator="place_value_and_rounding", instruction_text="Name the place value or round.",
    ),
    _pa(
        "Integers, Decimals, and Fractions",
        "pa_writing_numbers_with_words",
        "Writing numbers with words",
        generator="writing_numbers_with_words",
        instruction_text="Write the number in words.",
    ),
    _pa(
        "Integers, Decimals, and Fractions",
        "pa_integers_adding_and_subtracting",
        "Adding and subtracting",
        generator="pa_integers_adding_and_subtracting",
        instruction_text="Evaluate.",
    ),
    _pa(
        "Integers, Decimals, and Fractions",
        "pa_integers_multiplying",
        "Multiplying", generator="g6_integer_multiply", instruction_text="Multiply.",
    ),
    _pa(
        "Integers, Decimals, and Fractions",
        "pa_integers_dividing",
        "Dividing", generator="g6_integer_divide", instruction_text="Divide.",
    ),
    _pa(
        "Integers, Decimals, and Fractions",
        "pa_factoring",
        "Factoring",
        generator="g6_factoring",
        instruction_text="Factor.",
    ),
    _pa(
        "Integers, Decimals, and Fractions",
        "pa_greatest_common_factor",
        "Greatest common factor", generator="g6_greatest_common_factor", instruction_text="Find the GCF.",
    ),
    _pa(
        "Integers, Decimals, and Fractions",
        "pa_least_common_multiple",
        "Least common multiple", generator="g6_least_common_multiple", instruction_text="Find the LCM.",
    ),
    _pa(
        "Integers, Decimals, and Fractions",
        "pa_simplifying_fractions",
        "Simplifying fractions", generator="simplifying_numeric_fractions", instruction_text="Simplify.",
    ),
    _pa(
        "Integers, Decimals, and Fractions",
        "pa_converting_fractions_and_decimals",
        "Converting fractions and decimals",
        generator="converting_fractions_and_decimals",
        instruction_text="Convert.",
    ),
    # Beginning Algebra
    # Equations
    _pa(
        "Equations",
        "pa_equations_one_step_word_problems",
        "One-step equations, word problems",
        generator="wp_one_step_equation",
        instruction_latex="\\text{Solve the problem.}",
        instruction_text="Solve the problem.",
        count_default=5,
    ),
    _pa(
        "Equations",
        "pa_equations_two_step_word_problems",
        "Two-step equations word problems",
        generator="wp_two_step_equation",
        instruction_latex="\\text{Solve the problem.}",
        instruction_text="Solve the problem.",
        count_default=5,
    ),
    _pa(
        "Equations",
        "pa_equations_multi_step_equations",
        "Multi-step equations", generator="multi_step_equations", instruction_latex="\\text{Solve for } x.",
        instruction_text="Solve for x.",
    ),
    # Inequalities
    _pa(
        "Inequalities",
        "pa_multi_step_inequalities",
        "Multi-step inequalities", generator="multi_step_inequalities", instruction_latex="\\text{Solve for } x.",
        instruction_text="Solve for x.",
    ),
    # Factors and Exponents
    _pa(
        "Factors and Exponents",
        "pa_divisibility",
        "Divisibility", generator="g6_divisibility", instruction_text="Determine if the number is divisible.",
    ),
    _pa(
        "Factors and Exponents",
        "pa_squares_and_square_roots",
        "Squares and square roots",
        generator="pa_squares_and_square_roots",
        instruction_text="Evaluate.",
    ),
    # Proportions and Similarity
    _pa(
        "Proportions and Similarity",
        "pa_checking_for_a_proportion",
        "Checking for a proportion",
        generator="solving_proportions",
        instruction_text="Determine if the ratios form a proportion.",
    ),
    _pa(
        "Proportions and Similarity",
        "pa_proportions_word_problems",
        "Proportions word problems",
        generator="wp_proportion",
        instruction_latex="\\text{Solve the problem.}",
        instruction_text="Solve the problem.",
        count_default=5,
    ),
    _pa(
        "Proportions and Similarity",
        "pa_similar_figures",
        "Similar figures",
        generator="wp_similar_figures",
        instruction_text="Find the missing measure.",
    ),
    _pa(
        "Proportions and Similarity",
        "pa_similar_figures_word_problems",
        "Similar figures word problems",
        generator="wp_similar_figures",
        instruction_latex="\\text{Solve the problem.}",
        instruction_text="Solve the problem.",
        count_default=5,
    ),
    # Percents
    _pa(
        "Percents",
        "pa_fractions_decimals_and_percents",
        "Fractions, decimals, and percents",
        generator="fractions_decimals_and_percents",
        instruction_text="Write the equivalent value.",
    ),
    _pa(
        "Percents",
        "pa_markup_discount_and_tax",
        "Markup, discount, and tax",
        generator="wp_percent",
        instruction_latex="\\text{Solve the problem.}",
        instruction_text="Solve the problem.",
        count_default=5,
    ),
    _pa(
        "Percents",
        "pa_simple_and_compound_interest",
        "Simple and compound interest",
        generator="wp_simple_and_compound_interest",
        instruction_latex="\\text{Solve the problem.}",
        instruction_text="Solve the problem.",
        count_default=5,
    ),
    # Linear Equations and Inequalities
    _pa(
        "Linear Equations and Inequalities",
        "pa_plotting_points",
        "Plotting points",
        generator="plotting_points",
        instruction_text="Plot the following points on the coordinate plane.",
    ),
    _pa(
        "Linear Equations and Inequalities",
        "pa_slope",
        "Slope",
        generator="slope",
        instruction_latex="\\text{Find the slope.}",
        instruction_text="Find the slope.",
    ),
    _pa(
        "Linear Equations and Inequalities",
        "pa_writing_linear_equations",
        "Writing linear equations",
        generator="writing_linear_equations",
        instruction_latex=r"\text{Write the equation.}",
        instruction_text="Write the equation.",
    ),
    _pa(
        "Linear Equations and Inequalities",
        "pa_graphing_systems_of_equations",
        "Graphing systems of equations",
        generator="graph_system",
        instruction_latex="\\text{Solve the system.}",
        instruction_text="Solve the system.",
    ),
    _pa(
        "Linear Equations and Inequalities",
        "pa_systems_substitution",
        "Solving systems of equations by substitution", generator="systems_substitution", instruction_latex="\\text{Solve the system.}",
        instruction_text="Solve the system.",
    ),
    _pa(
        "Linear Equations and Inequalities",
        "pa_systems_word_problems",
        "Systems of equations word problems",
        generator="wp_systems",
        instruction_latex="\\text{Solve the problem.}",
        instruction_text="Solve the problem.",
        count_default=5,
    ),
    # Removed: using_statistical_models (not real statistical modeling — not selectable as Ready).
    # Plane Figures
    _pa(
        "Plane Figures",
        "pa_drawing_and_measuring_angles",
        "Drawing and measuring angles",
        generator="geo_angles", instruction_text="Measure or draw the angle.",
    ),
    _pa(
        "Plane Figures",
        "pa_angle_relationships",
        "Angle relationships",
        generator="geo_angle_relationships", instruction_text="Find the angle measure.",
    ),
    _pa(
        "Plane Figures",
        "pa_plane_figures_triangles",
        "Triangles",
        generator="geo_triangle_area", instruction_text="Find the measure.",
    ),
    _pa(
        "Plane Figures",
        "pa_quadrilaterals",
        "Quadrilaterals",
        generator="geo_quadrilateral_area", instruction_text="Find the measure.",
    ),
    _pa(
        "Plane Figures",
        "pa_area_of_triangles_and_quadrilaterals",
        "Area of triangles and quadrilaterals",
        generator="geo_triangles_and_quadrilaterals_area",
        instruction_text="Find the area.",
    ),
    _pa(
        "Plane Figures",
        "pa_circles",
        "Circles",
        generator="geo_circle_measure", instruction_text="Find the measure.",
    ),
    _pa(
        "Plane Figures",
        "pa_transformations",
        "Transformations",
        generator="geo_transformations",
        instruction_latex="\\text{Graph the transformation.}",
        instruction_text="Graph the transformation.",
    ),
    # Solid Figures
    _pa(
        "Solid Figures",
        "pa_classifying_volume_and_surface_area",
        "Classifying, volume, and surface area",
        generator="geo_solid_volume_surface", instruction_text="Find the volume or surface area.",
    ),
    # Right Triangles
    _pa(
        "Right Triangles",
        "pythagorean_theorem",
        "The Pythagorean Theorem", generator="geo_pythagorean_theorem", instruction_latex="\\text{Find the missing side.}",
        instruction_text="Find the missing side.",
    ),
    # Beginning Polynomials
    _pa(
        "Beginning Polynomials",
        "pa_polynomials_simplifying",
        "Simplifying",
        generator="simplify_polynomials",
        instruction_latex=r"\text{Simplify.}",
        instruction_text="Simplify.",
    ),
    _pa(
        "Beginning Polynomials",
        "pa_polynomials_adding_and_subtracting",
        "Adding and subtracting", generator="polynomial_add_subtract", instruction_latex="\\text{Simplify.}",
        instruction_text="Simplify.",
    ),
    _pa(
        "Beginning Polynomials",
        "pa_polynomials_multiplying",
        "Multiplying", generator="polynomial_multiply", instruction_latex="\\text{Multiply.}",
        instruction_text="Multiply.",
    ),
)
