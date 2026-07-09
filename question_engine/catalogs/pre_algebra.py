COURSE_ID = "pre_algebra"

CATEGORY_ORDER: tuple[str, ...] = (
    'Pre-Algebra — Integers, Decimals, and Fractions',
    'Pre-Algebra — Equations',
    'Pre-Algebra — Inequalities',
    'Pre-Algebra — Factors and Exponents',
    'Pre-Algebra — Proportions and Similarity',
    'Pre-Algebra — Percents',
    'Pre-Algebra — Linear Equations and Inequalities',
    'Pre-Algebra — Plane Figures',
    'Pre-Algebra — Solid Figures',
    'Pre-Algebra — Right Triangles',
    'Pre-Algebra — Beginning Polynomials',
)

from .base import TypeCatalogEntry



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
        instruction_latex=instruction_latex or "\\text{Solve.}",
        instruction_text=instruction_text or "Solve.",
        count_default=count_default,
    )


CATALOG: tuple[TypeCatalogEntry, ...] = (
    # Integers, Decimals, and Fractions
    _pa(
        "Integers, Decimals, and Fractions",
        "pa_naming_decimal_places_and_rounding",
        "Naming decimal places and rounding",
        instruction_text="Name the place value or round.",
    ),
    _pa(
        "Integers, Decimals, and Fractions",
        "pa_writing_numbers_with_words",
        "Writing numbers with words",
        instruction_text="Write the number in words.",
    ),
    _pa(
        "Integers, Decimals, and Fractions",
        "pa_integers_adding_and_subtracting",
        "Adding and subtracting",
        instruction_text="Evaluate.",
    ),
    _pa(
        "Integers, Decimals, and Fractions",
        "pa_integers_multiplying",
        "Multiplying",
        instruction_text="Multiply.",
    ),
    _pa(
        "Integers, Decimals, and Fractions",
        "pa_integers_dividing",
        "Dividing",
        instruction_text="Divide.",
    ),
    _pa(
        "Integers, Decimals, and Fractions",
        "pa_factoring",
        "Factoring",
        instruction_text="Factor.",
    ),
    _pa(
        "Integers, Decimals, and Fractions",
        "pa_greatest_common_factor",
        "Greatest common factor",
        instruction_text="Find the GCF.",
    ),
    _pa(
        "Integers, Decimals, and Fractions",
        "pa_least_common_multiple",
        "Least common multiple",
        instruction_text="Find the LCM.",
    ),
    _pa(
        "Integers, Decimals, and Fractions",
        "pa_simplifying_fractions",
        "Simplifying fractions",
        instruction_text="Simplify.",
    ),
    _pa(
        "Integers, Decimals, and Fractions",
        "pa_converting_fractions_and_decimals",
        "Converting fractions and decimals",
        instruction_text="Convert.",
    ),
    # Beginning Algebra
    # Equations
    _pa(
        "Equations",
        "pa_equations_one_step_word_problems",
        "One-step equations, word problems",
        instruction_latex="\\text{Solve the problem.}",
        instruction_text="Solve the problem.",
        count_default=5,
    ),
    _pa(
        "Equations",
        "pa_equations_two_step_word_problems",
        "Two-step equations word problems",
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
        "Divisibility",
        instruction_text="Determine if the number is divisible.",
    ),
    # Proportions and Similarity
    _pa(
        "Proportions and Similarity",
        "pa_checking_for_a_proportion",
        "Checking for a proportion",
        instruction_text="Determine if the ratios form a proportion.",
    ),
    _pa(
        "Proportions and Similarity",
        "pa_proportions_word_problems",
        "Proportions word problems",
        instruction_latex="\\text{Solve the problem.}",
        instruction_text="Solve the problem.",
        count_default=5,
    ),
    _pa(
        "Proportions and Similarity",
        "pa_similar_figures",
        "Similar figures",
        instruction_text="Find the missing measure.",
    ),
    _pa(
        "Proportions and Similarity",
        "pa_similar_figures_word_problems",
        "Similar figures word problems",
        instruction_latex="\\text{Solve the problem.}",
        instruction_text="Solve the problem.",
        count_default=5,
    ),
    # Percents
    _pa(
        "Percents",
        "pa_fractions_decimals_and_percents",
        "Fractions, decimals, and percents",
        instruction_text="Write the equivalent value.",
    ),
    _pa(
        "Percents",
        "pa_markup_discount_and_tax",
        "Markup, discount, and tax",
        instruction_latex="\\text{Solve the problem.}",
        instruction_text="Solve the problem.",
        count_default=5,
    ),
    _pa(
        "Percents",
        "pa_simple_and_compound_interest",
        "Simple and compound interest",
        instruction_latex="\\text{Solve the problem.}",
        instruction_text="Solve the problem.",
        count_default=5,
    ),
    # Linear Equations and Inequalities
    _pa(
        "Linear Equations and Inequalities",
        "pa_plotting_points",
        "Plotting points",
        instruction_text="Plot the point.",
    ),
    _pa(
        "Linear Equations and Inequalities",
        "pa_graphing_systems_of_equations",
        "Graphing systems of equations",
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
        instruction_latex="\\text{Solve the problem.}",
        instruction_text="Solve the problem.",
        count_default=5,
    ),
    # Plane Figures
    _pa(
        "Plane Figures",
        "pa_drawing_and_measuring_angles",
        "Drawing and measuring angles",
        instruction_text="Measure or draw the angle.",
    ),
    _pa(
        "Plane Figures",
        "pa_angle_relationships",
        "Angle relationships",
        instruction_text="Find the angle measure.",
    ),
    _pa(
        "Plane Figures",
        "pa_plane_figures_triangles",
        "Triangles",
        instruction_text="Find the measure.",
    ),
    _pa(
        "Plane Figures",
        "pa_quadrilaterals",
        "Quadrilaterals",
        instruction_text="Find the measure.",
    ),
    _pa(
        "Plane Figures",
        "pa_area_of_triangles_and_quadrilaterals",
        "Area of triangles and quadrilaterals",
        instruction_text="Find the area.",
    ),
    _pa(
        "Plane Figures",
        "pa_circles",
        "Circles",
        instruction_text="Find the measure.",
    ),
    _pa(
        "Plane Figures",
        "pa_transformations",
        "Transformations",
        instruction_text="Describe or perform the transformation.",
    ),
    # Solid Figures
    _pa(
        "Solid Figures",
        "pa_classifying_volume_and_surface_area",
        "Classifying, volume, and surface area",
        instruction_text="Find the volume or surface area.",
    ),
    # Right Triangles
    _pa(
        "Right Triangles",
        "pa_squares_and_square_roots",
        "Squares and square roots",
        instruction_text="Evaluate.",
    ),
    _pa(
        "Right Triangles",
        "pythagorean_theorem",
        "The Pythagorean Theorem",
        instruction_latex="\\text{Find the missing side.}",
        instruction_text="Find the missing side.",
    ),
    # Beginning Polynomials
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
    # Statistics
)
