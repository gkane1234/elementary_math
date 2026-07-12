/**
 * Frontend mirror of `question_engine/diagram_readiness.py`.
 *
 * Keep in sync with the Python set (verified by `scripts/verify_diagram_ready.py`).
 */
export const REQUIRES_DIAGRAM_TYPE_IDS: ReadonlySet<string> = new Set([
  // Grade 6 decimal / percent “with diagrams” still lack true models (stand-ins).
  "g6_decimal_addition_with_diagrams",
  "g6_decimal_subtraction_with_diagrams",
  "g6_decimal_multiplication_with_area_diagrams",
  "g6_solving_percent_problems_with_diagrams",
  // Box-plot “drawing” still uses the interpret-basics stand-in.
  "g6_drawing_box_plots",
  "scatter_plots",
  // Tip-to-tail vector diagram UI.
  "pc_vectors_diagrams",
  // Composite rhombus/kite + right-triangle figure not yet composed.
  "geo_trig_rhombuses_and_kites_with_right_triangles",
  // Calculus sketch / multi-graph UI.
  "calc_app_diff_curve_sketching",
  "calc_app_diff_graphical_comparison_of_f_f_prime_and_f_double_prime",
]);

/** Frontend mirror of `question_engine/type_readiness.py` INCORRECT_IMPLEMENTATION_TYPE_IDS. */
export const INCORRECT_IMPLEMENTATION_TYPE_IDS: ReadonlySet<string> = new Set([
  "g6_distributive_property_area_diagrams_numeric",
]);

export function typeRequiresDiagram(typeId: string, apiFlag?: boolean): boolean {
  return Boolean(apiFlag) || REQUIRES_DIAGRAM_TYPE_IDS.has(typeId);
}

export function typeIncorrectImplementation(typeId: string, apiFlag?: boolean): boolean {
  return Boolean(apiFlag) || INCORRECT_IMPLEMENTATION_TYPE_IDS.has(typeId);
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
    typeIncorrectImplementation(type.id, type.incorrect_implementation) ||
    typeRequiresDiagram(type.id, type.requires_diagram)
  );
}
