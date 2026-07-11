"""Types that must not show as curriculum-picker Ready until diagrams render.

The frontend ``QuestionGraph`` component renders ``graph_spec`` /
``number_line_spec``. ``QuestionDiagram`` renders ``diagram_svg`` from the
geometry diagram DSL. Types that still depend on unrendered assets
(``chart_spec``, tape/hanger/nets, etc.) stay listed here.

Any catalog type whose intended student experience depends on those unrendered
visuals should be listed here. The question-types API exposes
``requires_diagram: true``, and the curriculum picker treats those ids as
**Coming soon** (not selectable) even when a generator is wired.

Keepers (do NOT list here)
--------------------------
Types that render via ``QuestionGraph`` — e.g. ``graphing_linear_equations``,
number-line inequality graphing, ``pa_plotting_points``, conic graphing.
Types that emit ``diagram_svg`` via ``question_engine.diagrams`` and are wired
in the UI — e.g. ``geo_basics_angles_and_their_measures``,
``geo_congruent_triangle_angle_sum``, ``geo_circles_circumference_and_area``.

Re-enable later
---------------
1. Implement UI rendering for the relevant metadata (diagram/chart/net/etc.).
2. Remove the type id from ``REQUIRES_DIAGRAM_TYPE_IDS`` (or clear the flag).
3. Confirm the picker shows Ready and a sample worksheet draws the asset.
"""

from __future__ import annotations

# Curriculum-linked (and related catalog) ids that over-claim Ready today.
REQUIRES_DIAGRAM_TYPE_IDS: frozenset[str] = frozenset(
    {
        # Grade 6 — topic names promise diagrams; generators are text-only stand-ins.
        "g6_decimal_addition_with_diagrams",
        "g6_decimal_subtraction_with_diagrams",
        "g6_decimal_multiplication_with_area_diagrams",
        "g6_distributive_property_area_diagrams_numeric",
        "g6_distributive_property_area_diagrams_algebraic",
        "g6_solving_percent_problems_with_diagrams",
        # Grade 6 — tape / hanger / nets / area figures.
        "g6_equations_tape_diagrams",
        "g6_equations_hanger_diagrams",
        "g6_inequalities_hanger_diagrams",
        "g6_nets",
        "g6_nets_and_surface_area",
        "g6_nets_and_surface_area_on_a_grid",
        "g6_identifying_invalid_nets",
        "g6_parallelograms",
        "g6_parallelograms_understanding_area_formula",
        "g6_triangles",
        "g6_triangles_understanding_area_formula",
        "g6_volume_and_surface_area_using_isometric_drawings",
        "g6_isometric_sketching",
        "g6_rectangles_with_fraction_side_lengths",
        "g6_triangles_with_fraction_side_lengths",
        # Stats — chart_spec is emitted but not drawn in the UI.
        "g6_interpreting_dot_plots",
        "g6_drawing_dot_plots",
        "g6_interpreting_histograms",
        "g6_drawing_histograms",
        "g6_interpreting_box_plots",
        "g6_drawing_box_plots",
        "visualizing_data",
        "scatter_plots",
        # Pre-Algebra — figures / similar figures / plane geometry.
        "pa_area_of_triangles_and_quadrilaterals",
        "pa_drawing_and_measuring_angles",
        "pa_angle_relationships",
        "pa_plane_figures_triangles",
        "pa_circles",
        "pa_similar_figures",
        "pa_similar_figures_word_problems",
        # Algebra 1 — right-triangle trig that expects a drawn triangle.
        "finding_sine_cosine_tangent",
        "finding_angles",
        "find_missing_sides_of_triangles",
        # Geometry — still need diagram wiring.
        "geo_basics_line_segments_and_their_measures",
        "geo_basics_geometric_diagrams_and_notation",
        "geo_congruent_triangle_perimeter",
        "geo_quadrilaterals_area_of_triangles_and_quadrilaterals",
        "geo_similarity_similar_triangles",
        "geo_similarity_similar_right_triangles",
        "geo_right_pythagorean_theorem",
        "geo_right_multi_step_pythagorean_theorem_problems",
        "geo_right_special_right_triangles",
        "geo_right_multi_step_special_right_triangle_problems",
        "geo_trig_finding_trig_ratios",
        "geo_trig_finding_angle_measures",
        "geo_trig_solving_right_triangles",
        "geo_trig_multi_step_trig_problems",
        "geo_trig_rhombuses_and_kites_with_right_triangles",
        "geo_trig_trigonometry_and_area",
        "geo_nets_of_solids",
        # Algebra 2 / Precalculus — right-triangle trig figures.
        "a2_trigonometry_right_triangle_trig_finding_ratios",
        "a2_trigonometry_right_triangle_trig_finding_angle_measures",
        "a2_trigonometry_right_triangle_trig_angles_and_sides",
        "pc_right_triangle_trig_finding_ratios",
        "pc_right_triangle_trig_finding_angles_and_sides",
        "pc_vectors_diagrams",
    }
)


def type_requires_diagram(type_id: str) -> bool:
    return type_id in REQUIRES_DIAGRAM_TYPE_IDS
