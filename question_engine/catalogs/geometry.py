COURSE_ID = "geometry"

CATEGORY_ORDER: tuple[str, ...] = (
    'Geometry — Review of Algebra',
    'Geometry — Basics of Geometry',
    'Geometry — Parallel Lines and the Coordinate Plane',
    'Geometry — Congruent Triangles',
    'Geometry — Properties of Triangles',
    'Geometry — Quadrilaterals and Polygons',
    'Geometry — Similarity',
    'Geometry — Right Triangles',
    'Geometry — Trigonometry',
    'Geometry — Surface Area and Volume',
    'Geometry — Circles',
    'Geometry — Transformations',
    'Geometry — Probability and Statistics',
    'Geometry — Constructions',
)

from .base import TypeCatalogEntry, resolve_instruction_latex, resolve_instruction_text



def _geo(
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
        category=f"Geometry — {chapter}",
        generator=generator,
        description=f"Practice {name.lower()}.",
        instruction_latex=resolve_instruction_latex(instruction_latex, instruction_text),
        instruction_text=resolve_instruction_text(instruction_text),
        count_default=count_default,
    )


CATALOG: tuple[TypeCatalogEntry, ...] = (
    # Review of Algebra
    _geo(
        "Review of Algebra",
        "geo_review_multi_step_equations",
        "Multi-step equations", generator="multi_step_equations", instruction_text="Solve.",
    ),
    _geo(
        "Review of Algebra",
        "geo_review_simplifying_square_roots",
        "Simplifying square roots", generator="radical_simplification", instruction_text="Simplify.",
    ),
    _geo(
        "Review of Algebra",
        "geo_review_adding_and_subtracting_square_roots",
        "Adding and subtracting square roots", generator="radical_add_subtract", instruction_text="Simplify.",
    ),
    _geo(
        "Review of Algebra",
        "geo_review_multiplying_square_roots",
        "Multiplying square roots", generator="radical_multiply", instruction_text="Simplify.",
    ),
    _geo(
        "Review of Algebra",
        "geo_review_dividing_square_roots",
        "Dividing square roots", generator="radical_divide", instruction_text="Simplify.",
    ),
    # Basics of Geometry
    _geo(
        "Basics of Geometry",
        "geo_basics_line_segments_and_their_measures",
        "Line segments and their measures",
        generator="geo_segment_length",
        instruction_text="Find the measure.",
    ),
    _geo(
        "Basics of Geometry",
        "geo_basics_segment_addition_postulate",
        "Segment Addition Postulate",
        instruction_text="Find the measure.",
    ),
    _geo(
        "Basics of Geometry",
        "geo_basics_angles_and_their_measures",
        "Angles and their measures",
        generator="geo_angles",
        instruction_text="Find the measure.",
    ),
    _geo(
        "Basics of Geometry",
        "geo_basics_classifying_angles",
        "Classifying angles",
        generator="geo_classifying_angles",
        instruction_text="Classify the angle.",
    ),
    _geo(
        "Basics of Geometry",
        "geo_basics_basic_angle_terminology",
        "Basic angle terminology",
        instruction_text="Identify the angle.",
    ),
    _geo(
        "Basics of Geometry",
        "geo_basics_angle_addition_postulate",
        "Angle Addition Postulate",
        instruction_text="Find the measure.",
    ),
    _geo(
        "Basics of Geometry",
        "geo_basics_angle_relationships",
        "Angle relationships",
        instruction_text="Find the measure.",
    ),
    _geo(
        "Basics of Geometry",
        "geo_basics_geometric_diagrams_and_notation",
        "Geometric diagrams and notation",
        instruction_text="Identify the figure.",
    ),
    # Parallel Lines and the Coordinate Plane
    _geo(
        "Parallel Lines and the Coordinate Plane",
        "geo_parallel_parallel_lines_and_transversals",
        "Parallel lines and transversals",
        instruction_text="Find the measure.",
    ),
    _geo(
        "Parallel Lines and the Coordinate Plane",
        "geo_parallel_points_of_the_coordinate_plane",
        "Points of the coordinate plane",
        generator="plotting_points",
        instruction_text="Identify the point.",
    ),
    _geo(
        "Parallel Lines and the Coordinate Plane",
        "geo_parallel_slope_and_lines",
        "Slope and lines",
        generator="slope",
        instruction_text="Find the slope.",
    ),
    _geo(
        "Parallel Lines and the Coordinate Plane",
        "geo_parallel_distance_formula",
        "The distance formula",
        generator="geo_coordinate_distance",
        instruction_text="Find the distance.",
    ),
    _geo(
        "Parallel Lines and the Coordinate Plane",
        "geo_parallel_graphing_linear_equations",
        "Graphing linear equations",
        generator="graph_linear_equation",
        instruction_text="Graph the equation.",
    ),
    _geo(
        "Parallel Lines and the Coordinate Plane",
        "geo_parallel_writing_linear_equations",
        "Writing linear equations", generator="writing_linear_equations", instruction_text="Write the equation.",
    ),
    # Congruent Triangles
    _geo(
        "Congruent Triangles",
        "geo_congruent_classifying_triangles",
        "Classifying triangles",
        instruction_text="Classify the triangle.",
    ),
    _geo(
        "Congruent Triangles",
        "geo_congruent_triangle_angle_sum",
        "Triangle angle sum",
        generator="geo_triangle_angle_sum",
        instruction_text="Find the measure.",
    ),
    _geo(
        "Congruent Triangles",
        "geo_congruent_triangle_perimeter",
        "Triangle perimeter",
        generator="geo_triangle_perimeter",
        instruction_text="Find the perimeter.",
    ),
    _geo(
        "Congruent Triangles",
        "geo_congruent_exterior_angle_theorem",
        "Exterior Angle Theorem",
        instruction_text="Find the measure.",
    ),
    _geo(
        "Congruent Triangles",
        "geo_congruent_triangles_and_congruence",
        "Triangles and congruence",
        instruction_text="Determine if the triangles are congruent.",
    ),
    _geo(
        "Congruent Triangles",
        "geo_congruent_proving_triangles_congruent",
        "Proving triangles congruent",
        instruction_text="Prove the triangles are congruent.",
    ),
    _geo(
        "Congruent Triangles",
        "geo_congruent_isosceles_and_equilateral_triangles",
        "Isosceles and equilateral triangles",
        instruction_text="Find the measure.",
    ),
    # Properties of Triangles
    _geo(
        "Properties of Triangles",
        "geo_properties_midsegment",
        "Midsegment",
        instruction_text="Find the measure.",
    ),
    _geo(
        "Properties of Triangles",
        "geo_properties_angle_bisectors",
        "Angle bisectors",
        instruction_text="Find the measure.",
    ),
    _geo(
        "Properties of Triangles",
        "geo_properties_medians",
        "Medians",
        instruction_text="Find the measure.",
    ),
    _geo(
        "Properties of Triangles",
        "geo_properties_centroid",
        "Centroid",
        instruction_text="Find the coordinates.",
    ),
    _geo(
        "Properties of Triangles",
        "geo_properties_triangle_inequality_theorem",
        "Triangle Inequality Theorem",
        instruction_text="Determine if the sides can form a triangle.",
    ),
    _geo(
        "Properties of Triangles",
        "geo_properties_inequalities_in_one_triangle",
        "Inequalities in one triangle",
        instruction_text="Order the sides or angles.",
    ),
    # Quadrilaterals and Polygons
    _geo(
        "Quadrilaterals and Polygons",
        "geo_quadrilaterals_classifying",
        "Classifying",
        instruction_text="Classify the figure.",
    ),
    _geo(
        "Quadrilaterals and Polygons",
        "geo_quadrilaterals_angles",
        "Angles",
        instruction_text="Find the measure.",
    ),
    _geo(
        "Quadrilaterals and Polygons",
        "geo_quadrilaterals_parallelograms",
        "Parallelograms",
        instruction_text="Find the measure.",
    ),
    _geo(
        "Quadrilaterals and Polygons",
        "geo_quadrilaterals_trapezoids",
        "Trapezoids",
        instruction_text="Find the measure.",
    ),
    _geo(
        "Quadrilaterals and Polygons",
        "geo_quadrilaterals_rhombuses",
        "Rhombuses",
        instruction_text="Find the measure.",
    ),
    _geo(
        "Quadrilaterals and Polygons",
        "geo_quadrilaterals_kites",
        "Kites",
        instruction_text="Find the measure.",
    ),
    _geo(
        "Quadrilaterals and Polygons",
        "geo_quadrilaterals_area_of_triangles_and_quadrilaterals",
        "Area of triangles and quadrilaterals",
        generator="geo_triangle_area",
        instruction_text="Find the area.",
    ),
    _geo(
        "Quadrilaterals and Polygons",
        "geo_quadrilaterals_polygon_basics",
        "Polygon basics",
        instruction_text="Find the measure.",
    ),
    _geo(
        "Quadrilaterals and Polygons",
        "geo_quadrilaterals_area_of_regular_polygons",
        "Area of regular polygons",
        instruction_text="Find the area.",
    ),
    # Similarity
    _geo(
        "Similarity",
        "geo_similarity_similar_polygons",
        "Similar polygons",
        instruction_text="Determine if the polygons are similar.",
    ),
    _geo(
        "Similarity",
        "geo_similarity_similar_triangles",
        "Similar triangles",
        generator="geo_similar_triangles",
        instruction_text="Determine if the triangles are similar.",
    ),
    _geo(
        "Similarity",
        "geo_similarity_similar_right_triangles",
        "Similar right triangles", generator="geo_similar_triangles", instruction_text="Find the measure.",
    ),
    _geo(
        "Similarity",
        "geo_similarity_proportional_parts_in_triangles_and_parallel_lines",
        "Proportional parts in triangles and parallel lines",
        instruction_text="Find the measure.",
    ),
    # Right Triangles
    _geo(
        "Right Triangles",
        "geo_right_pythagorean_theorem",
        "The Pythagorean Theorem",
        generator="geo_pythagorean_theorem",
        instruction_latex="\\text{Find the missing side.}",
        instruction_text="Find the missing side.",
    ),
    _geo(
        "Right Triangles",
        "geo_right_multi_step_pythagorean_theorem_problems",
        "Multi-step Pythagorean Theorem problems",
        generator="geo_pythagorean_theorem",
        instruction_text="Solve the problem.",
        count_default=5,
    ),
    _geo(
        "Right Triangles",
        "geo_right_special_right_triangles",
        "Special right triangles", generator="geo_pythagorean_theorem", instruction_text="Find the measure.",
    ),
    _geo(
        "Right Triangles",
        "geo_right_multi_step_special_right_triangle_problems",
        "Multi-step special right triangle problems",
        instruction_text="Solve the problem.",
        count_default=5,
    ),
    # Trigonometry
    _geo(
        "Trigonometry",
        "geo_trig_finding_trig_ratios",
        "Finding trig. ratios", generator="trig_evaluate", instruction_text="Find the ratio.",
    ),
    _geo(
        "Trigonometry",
        "geo_trig_finding_angle_measures",
        "Finding angle measures", generator="trig_evaluate", instruction_text="Find the angle measure.",
    ),
    _geo(
        "Trigonometry",
        "geo_trig_solving_right_triangles",
        "Solving right triangles", generator="geo_pythagorean_theorem", instruction_text="Solve the triangle.",
    ),
    _geo(
        "Trigonometry",
        "geo_trig_multi_step_trig_problems",
        "Multi-step trig. problems", generator="trig_evaluate", instruction_text="Solve the problem.",
        count_default=5,
    ),
    _geo(
        "Trigonometry",
        "geo_trig_rhombuses_and_kites_with_right_triangles",
        "Rhombuses and kites with right triangles", generator="geo_pythagorean_theorem", instruction_text="Find the measure.",
    ),
    _geo(
        "Trigonometry",
        "geo_trig_trigonometry_and_area",
        "Trigonometry and area", generator="geo_triangle_area", instruction_text="Find the area.",
    ),
    # Surface Area and Volume
    _geo(
        "Surface Area and Volume",
        "geo_solid_figures_identifying_volume_and_area",
        "Solid figures: identifying, volume, and area",
        instruction_text="Find the volume or surface area.",
    ),
    _geo(
        "Surface Area and Volume",
        "geo_nets_of_solids",
        "Nets of solids",
        instruction_text="Identify the net.",
    ),
    _geo(
        "Surface Area and Volume",
        "geo_similar_solids",
        "Similar solids",
        instruction_text="Find the measure.",
    ),
    # Circles
    _geo(
        "Circles",
        "geo_circles_naming_arcs_and_central_angles",
        "Naming arcs and central angles",
        instruction_text="Name the arc or angle.",
    ),
    _geo(
        "Circles",
        "geo_circles_measures_of_arcs_and_central_angles",
        "Measures of arcs and central angles",
        instruction_text="Find the measure.",
    ),
    _geo(
        "Circles",
        "geo_circles_arcs_and_chords",
        "Arcs and chords",
        instruction_text="Find the measure.",
    ),
    _geo(
        "Circles",
        "geo_circles_circumference_and_area",
        "Circumference and area",
        generator="geo_circle_measure",
        instruction_text="Find the circumference or area.",
    ),
    _geo(
        "Circles",
        "geo_circles_arc_length_and_sector_area",
        "Arc length and sector area",
        instruction_text="Find the arc length or sector area.",
    ),
    _geo(
        "Circles",
        "geo_circles_inscribed_angles",
        "Inscribed angles",
        instruction_text="Find the measure.",
    ),
    _geo(
        "Circles",
        "geo_circles_tangents",
        "Tangents",
        instruction_text="Find the measure.",
    ),
    _geo(
        "Circles",
        "geo_circles_secant_and_tangent_angles",
        "Secant and tangent angles",
        instruction_text="Find the measure.",
    ),
    _geo(
        "Circles",
        "geo_circles_segment_measures",
        "Segment measures",
        instruction_text="Find the measure.",
    ),
    _geo(
        "Circles",
        "geo_circles_using_equations_of_circles",
        "Using equations of circles",
        instruction_text="Use the equation of the circle.",
    ),
    _geo(
        "Circles",
        "geo_circles_writing_equations_of_circles",
        "Writing equations of circles",
        instruction_text="Write the equation of the circle.",
    ),
    # Transformations
    _geo(
        "Transformations",
        "geo_transformations_translations_rotations_reflections_and_dilations",
        "Translations, rotations, reflections, and dilations",
        instruction_text="Describe the transformation.",
    ),
    # Probability and Statistics
    _geo(
        "Probability and Statistics",
        "geo_probability_sample_spaces_and_fundamental_counting_principle",
        "Sample spaces and the Fundamental Counting Principle",
        generator="stats_counting_principle",
        instruction_text="Find the number of outcomes.",
    ),
    _geo(
        "Probability and Statistics",
        "geo_probability_independent_and_dependent_events_word_problems",
        "Probability of independent and dependent events, word problems",
        generator="stats_probability_compound_independent",
        instruction_text="Solve the problem.",
        count_default=5,
    ),
    _geo(
        "Probability and Statistics",
        "geo_probability_independent_and_dependent_events",
        "Probability of independent and dependent events",
        generator="stats_probability_compound_independent",
        instruction_text="Find the probability.",
    ),
    _geo(
        "Probability and Statistics",
        "geo_probability_mutually_exclusive_events_word_problems",
        "Probability of mutually exclusive events, word problems",
        generator="stats_probability_mutually_exclusive",
        instruction_text="Solve the problem.",
        count_default=5,
    ),
    _geo(
        "Probability and Statistics",
        "geo_probability_mutually_exclusive_events",
        "Probability of mutually exclusive events",
        generator="stats_probability_mutually_exclusive",
        instruction_text="Find the probability.",
    ),
    _geo(
        "Probability and Statistics",
        "geo_probability_permutations",
        "Permutations", generator="stats_counting_principle", instruction_text="Find the number of permutations.",
    ),
    _geo(
        "Probability and Statistics",
        "geo_probability_combinations",
        "Combinations", generator="stats_counting_principle", instruction_text="Find the number of combinations.",
    ),
    _geo(
        "Probability and Statistics",
        "geo_probability_permutations_vs_combinations",
        "Permutations vs combinations", generator="stats_counting_principle", instruction_text="Determine whether to use permutations or combinations.",
    ),
    _geo(
        "Probability and Statistics",
        "geo_probability_with_permutations_and_combinations",
        "Probability with permutations and combinations", generator="stats_counting_principle", instruction_text="Find the probability.",
    ),
    # Constructions
    _geo(
        "Constructions",
        "geo_constructions_line_segments",
        "Line segments",
        instruction_text="Construct the segment.",
    ),
    _geo(
        "Constructions",
        "geo_constructions_perpendicular_segments",
        "Perpendicular segments",
        instruction_text="Construct the perpendicular segment.",
    ),
    _geo(
        "Constructions",
        "geo_constructions_angles",
        "Angles",
        instruction_text="Construct the angle.",
    ),
    _geo(
        "Constructions",
        "geo_constructions_triangles",
        "Triangles",
        instruction_text="Construct the triangle.",
    ),
    _geo(
        "Constructions",
        "geo_constructions_medians_of_a_triangle",
        "Medians of a triangle",
        instruction_text="Construct the median.",
    ),
    _geo(
        "Constructions",
        "geo_constructions_altitudes_of_a_triangle",
        "Altitudes of a triangle",
        instruction_text="Construct the altitude.",
    ),
    _geo(
        "Constructions",
        "geo_constructions_angle_bisectors",
        "Angle bisectors",
        instruction_text="Construct the angle bisector.",
    ),
    _geo(
        "Constructions",
        "geo_constructions_circles",
        "Circles",
        instruction_text="Construct the circle.",
    ),
)
