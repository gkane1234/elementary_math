/**
 * Frontend mirror of `question_engine/diagram_readiness.py`.
 *
 * Defense in depth: even if the API omits `requires_diagram`, the curriculum
 * picker must not treat these ids as Ready. Keep in sync with the Python set
 * (verified by `scripts/verify_diagram_ready.py`).
 *
 * QuestionGraph only renders graph_spec / number_line_spec — not diagram_spec,
 * figure_spec, chart_spec, nets, etc.
 */
export const REQUIRES_DIAGRAM_TYPE_IDS: ReadonlySet<string> = new Set([
  // Grade 6 — topic names promise diagrams; generators are text-only stand-ins.
  "g6_decimal_addition_with_diagrams",
  "g6_decimal_subtraction_with_diagrams",
  "g6_decimal_multiplication_with_area_diagrams",
  "g6_distributive_property_area_diagrams_numeric",
  "g6_distributive_property_area_diagrams_algebraic",
  "g6_solving_percent_problems_with_diagrams",
  // Grade 6 — tape / hanger / nets / area figures.
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
  // Stats — chart_spec is emitted but not drawn in the UI.
  "g6_interpreting_dot_plots",
  "g6_drawing_dot_plots",
  "g6_interpreting_histograms",
  "g6_drawing_histograms",
  "g6_interpreting_box_plots",
  "g6_drawing_box_plots",
  "visualizing_data",
  "scatter_plots",
  // Pre-Algebra — figures / similar figures / plane geometry.
  "pa_area_of_triangles_and_quadrilaterals",
  "pa_drawing_and_measuring_angles",
  "pa_angle_relationships",
  "pa_plane_figures_triangles",
  "pa_circles",
  "pa_similar_figures",
  "pa_similar_figures_word_problems",
  // Algebra 1 — right-triangle trig that expects a drawn triangle.
  "finding_sine_cosine_tangent",
  "finding_angles",
  "find_missing_sides_of_triangles",
  // Geometry — figure_spec / diagram-oriented measurement.
  "geo_basics_line_segments_and_their_measures",
  "geo_basics_angles_and_their_measures",
  "geo_basics_classifying_angles",
  "geo_basics_geometric_diagrams_and_notation",
  "geo_congruent_triangle_angle_sum",
  "geo_congruent_triangle_perimeter",
  "geo_quadrilaterals_area_of_triangles_and_quadrilaterals",
  "geo_similarity_similar_triangles",
  "geo_similarity_similar_right_triangles",
  "geo_right_pythagorean_theorem",
  "geo_right_multi_step_pythagorean_theorem_problems",
  "geo_right_special_right_triangles",
  "geo_right_multi_step_special_right_triangle_problems",
  "geo_circles_circumference_and_area",
  "geo_trig_finding_trig_ratios",
  "geo_trig_finding_angle_measures",
  "geo_trig_solving_right_triangles",
  "geo_trig_multi_step_trig_problems",
  "geo_trig_rhombuses_and_kites_with_right_triangles",
  "geo_trig_trigonometry_and_area",
  "geo_nets_of_solids",
  // Algebra 2 / Precalculus — right-triangle trig figures.
  "a2_trigonometry_right_triangle_trig_finding_ratios",
  "a2_trigonometry_right_triangle_trig_finding_angle_measures",
  "a2_trigonometry_right_triangle_trig_angles_and_sides",
  "pc_right_triangle_trig_finding_ratios",
  "pc_right_triangle_trig_finding_angles_and_sides",
  "pc_vectors_diagrams",
]);

export function typeRequiresDiagram(typeId: string, apiFlag?: boolean): boolean {
  return Boolean(apiFlag) || REQUIRES_DIAGRAM_TYPE_IDS.has(typeId);
}

/** True when the picker must treat this API type as not Ready / Coming soon. */
export function typeIsNotReady(type: {
  id: string;
  requires_diagram?: boolean;
  incorrect_implementation?: boolean;
  not_ready?: boolean;
}): boolean {
  return (
    Boolean(type.not_ready) ||
    Boolean(type.incorrect_implementation) ||
    typeRequiresDiagram(type.id, type.requires_diagram)
  );
}
