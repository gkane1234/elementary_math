"""Curriculum-only units used by the progression graph.

OpenStax has no dedicated Grade 6 book; our curriculum is the spine.
Geometry is also curriculum-only in this repo.
"""

from __future__ import annotations

# (node_id, chapter_index, title)
GRADE_6_UNITS: list[tuple[str, int, str]] = [
    ("ratios", 1, "Ratios"),
    ("rates", 2, "Rates"),
    ("percents", 3, "Percents"),
    ("dividing_fractions", 4, "Dividing Fractions"),
    ("decimal_arithmetic", 5, "Decimal Arithmetic"),
    ("common_factors_and_common_multiples", 6, "Common Factors and Common Multiples"),
    ("negative_numbers_and_absolute_value", 7, "Negative Numbers and Absolute Value"),
    ("coordinate_plane", 8, "Coordinate Plane"),
    ("numeric_expressions_exponents_and_order_of_operations", 9, "Numeric Expressions, Exponents, and the Order of Operations"),
    ("variables_and_algebraic_expressions", 10, "Variables and Algebraic Expressions"),
    ("equivalent_expressions", 11, "Equivalent Expressions"),
    ("equations", 12, "Equations"),
    ("inequalities", 13, "Inequalities"),
    ("equations_as_relationships_between_two_variables", 14, "Equations as Relationships between Two Variables"),
    ("polygons", 15, "Polygons"),
    ("polyhedra", 16, "Polyhedra"),
    ("area_and_volume_with_fractions", 17, "Area and Volume with Fractions"),
    ("data_sets_and_distributions", 18, "Data Sets and Distributions"),
]

BOOK_ID = "grade_6_math"
DISPLAY_NAME = "Grade 6 Math"

FOUNDATIONS_UNITS: list[tuple[str, int, str]] = [
    ("whole_numbers", 1, "Whole Numbers"),
    ("addition_subtraction_multiplication_division", 2, "Arithmetic Operations"),
    ("number_line", 3, "Number Line"),
    ("fractions_meaning", 4, "Fractions: Meaning and Models"),
    ("equivalent_fractions", 5, "Equivalent Fractions"),
    ("fraction_operations", 6, "Fraction Operations"),
    ("decimal_place_value", 7, "Decimal Place Value"),
]

FOUNDATIONS_BOOK_ID = "foundations_math"
FOUNDATIONS_DISPLAY_NAME = "Foundations Math"

GEOMETRY_UNITS: list[tuple[str, int, str]] = [
    ("review_of_algebra", 1, "Review of Algebra"),
    ("basics_of_geometry", 2, "Basics of Geometry"),
    ("parallel_lines_and_the_coordinate_plane", 3, "Parallel Lines and the Coordinate Plane"),
    ("congruent_triangles", 4, "Congruent Triangles"),
    ("properties_of_triangles", 5, "Properties of Triangles"),
    ("quadrilaterals_and_polygons", 6, "Quadrilaterals and Polygons"),
    ("similarity", 7, "Similarity"),
    ("right_triangles", 8, "Right Triangles"),
    ("trigonometry", 9, "Trigonometry"),
    ("surface_area_and_volume", 10, "Surface Area and Volume"),
    ("circles", 11, "Circles"),
    ("transformations", 12, "Transformations"),
    ("probability_and_statistics", 13, "Probability and Statistics"),
    ("constructions", 14, "Constructions"),
]

GEOMETRY_BOOK_ID = "geometry"
GEOMETRY_DISPLAY_NAME = "Geometry"
