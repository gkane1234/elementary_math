"""Wire newly implemented scaffold types to real generators + create stubs."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# (type_id, generator, course, chapter)
WIRING: list[tuple[str, str, str, str]] = [
    # Geometry basics / triangles / parallel
    ("geo_basics_angle_addition_postulate", "geo_angle_addition", "geometry", "basics_of_geometry"),
    ("geo_basics_segment_addition_postulate", "geo_segment_addition", "geometry", "basics_of_geometry"),
    ("geo_basics_angle_relationships", "geo_angle_relationships", "geometry", "basics_of_geometry"),
    ("geo_basics_basic_angle_terminology", "geo_classifying_angles", "geometry", "basics_of_geometry"),
    ("geo_congruent_exterior_angle_theorem", "geo_exterior_angle", "geometry", "congruent_triangles"),
    ("geo_congruent_classifying_triangles", "geo_classifying_triangles", "geometry", "congruent_triangles"),
    ("geo_congruent_isosceles_and_equilateral_triangles", "geo_isosceles_triangle", "geometry", "congruent_triangles"),
    ("geo_parallel_parallel_lines_and_transversals", "geo_parallel_transversal", "geometry", "parallel_lines_and_the_coordinate_plane"),
    ("geo_properties_triangle_inequality_theorem", "geo_triangle_inequality", "geometry", "properties_of_triangles"),
    ("geo_properties_inequalities_in_one_triangle", "geo_triangle_inequality", "geometry", "properties_of_triangles"),
    ("geo_right_multi_step_special_right_triangle_problems", "geo_special_right_triangle", "geometry", "right_triangles"),
    ("geo_quadrilaterals_angles", "geo_polygon_interior", "geometry", "quadrilaterals_and_polygons"),
    ("geo_quadrilaterals_polygon_basics", "geo_polygon_interior", "geometry", "quadrilaterals_and_polygons"),
    ("geo_quadrilaterals_parallelograms", "geo_parallelogram_area", "geometry", "quadrilaterals_and_polygons"),
    ("geo_quadrilaterals_trapezoids", "geo_trapezoid_area", "geometry", "quadrilaterals_and_polygons"),
    ("geo_quadrilaterals_kites", "geo_kite_area", "geometry", "quadrilaterals_and_polygons"),
    ("geo_quadrilaterals_rhombuses", "geo_parallelogram_area", "geometry", "quadrilaterals_and_polygons"),
    ("geo_circles_measures_of_arcs_and_central_angles", "geo_central_arc", "geometry", "circles"),
    ("geo_circles_naming_arcs_and_central_angles", "geo_central_arc", "geometry", "circles"),
    ("geo_circles_inscribed_angles", "geo_inscribed_angle", "geometry", "circles"),
    ("geo_circles_arc_length_and_sector_area", "geo_arc_sector", "geometry", "circles"),
    ("geo_solid_figures_identifying_volume_and_area", "geo_solid_volume_surface", "geometry", "surface_area_and_volume"),
    ("geo_similar_solids", "geo_solid_volume_surface", "geometry", "surface_area_and_volume"),
    # Re-wire demoted right-triangle trig to diagram-aware generator
    ("geo_trig_finding_trig_ratios", "geo_right_triangle_trig_ratio", "geometry", "trigonometry"),
    ("geo_trig_finding_angle_measures", "geo_right_triangle_trig_angle", "geometry", "trigonometry"),
    ("geo_trig_solving_right_triangles", "geo_right_triangle_trig_side", "geometry", "trigonometry"),
    ("geo_trig_multi_step_trig_problems", "geo_right_triangle_trig", "geometry", "trigonometry"),
    ("geo_right_special_right_triangles", "geo_special_right_triangle", "geometry", "right_triangles"),
    # Grade 6
    ("g6_parallelograms", "geo_parallelogram_area", "grade_6", "polygons"),
    ("g6_parallelograms_understanding_area_formula", "geo_parallelogram_area", "grade_6", "polygons"),
    ("g6_triangles", "geo_triangle_area", "grade_6", "polygons"),
    ("g6_triangles_understanding_area_formula", "geo_triangle_area", "grade_6", "polygons"),
    ("g6_trapezoids", "geo_trapezoid_area", "grade_6", "polygons"),
    ("g6_kites", "geo_kite_area", "grade_6", "polygons"),
    ("g6_dividing_decimals_by_decimals", "g6_decimal_divide", "grade_6", "decimal_arithmetic"),
    ("g6_formulas_for_volume_and_surface_area_of_a_cube", "geo_solid_volume_surface", "grade_6", "polyhedra"),
    ("g6_rectangles_with_fraction_side_lengths", "geo_triangle_area", "grade_6", "area_and_volume_with_fractions"),
    ("g6_triangles_with_fraction_side_lengths", "geo_triangle_area", "grade_6", "area_and_volume_with_fractions"),
    ("g6_right_rectangular_prisms_with_fraction_side_lengths", "geo_solid_volume_surface", "grade_6", "area_and_volume_with_fractions"),
    # Fix incorrect writing expressions
    ("g6_writing_numeric_expressions", "writing_numeric_expressions", "grade_6", "numeric_expressions_exponents_and_order_of_operations"),
    # Pre-Algebra plane figures
    ("pa_drawing_and_measuring_angles", "geo_angles", "pre_algebra", "plane_figures"),
    ("pa_angle_relationships", "geo_angle_relationships", "pre_algebra", "plane_figures"),
    ("pa_plane_figures_triangles", "geo_triangle_area", "pre_algebra", "plane_figures"),
    ("pa_circles", "geo_circle_measure", "pre_algebra", "plane_figures"),
    ("pa_quadrilaterals", "geo_parallelogram_area", "pre_algebra", "plane_figures"),
    ("pa_classifying_volume_and_surface_area", "geo_solid_volume_surface", "pre_algebra", "solid_figures"),
    # Algebra 1 / A2 / PC trig rewire
    ("finding_sine_cosine_tangent", "geo_right_triangle_trig_ratio", "algebra_1", "right_triangles"),
    ("finding_angles", "finding_angles", "algebra_1", "right_triangles"),
    ("find_missing_sides_of_triangles", "geo_pythagorean_theorem", "algebra_1", "right_triangles"),
    ("a2_trigonometry_right_triangle_trig_finding_ratios", "geo_right_triangle_trig_ratio", "algebra_2", "trigonometry"),
    ("a2_trigonometry_right_triangle_trig_finding_angle_measures", "geo_right_triangle_trig_angle", "algebra_2", "trigonometry"),
    ("a2_trigonometry_right_triangle_trig_angles_and_sides", "geo_right_triangle_trig", "algebra_2", "trigonometry"),
    ("a2_trigonometry_the_law_of_sines", "law_of_sines", "algebra_2", "trigonometry"),
    ("a2_trigonometry_the_law_of_cosines", "law_of_cosines", "algebra_2", "trigonometry"),
    ("a2_trigonometry_arc_length_and_sector_area", "geo_arc_sector", "algebra_2", "trigonometry"),
    ("a2_trigonometry_area_and_laws_of_sines_and_cosines", "law_of_sines", "algebra_2", "trigonometry"),
    ("a2_polynomial_functions_the_binomial_theorem", "binomial_theorem", "algebra_2", "polynomial_functions"),
    ("a2_polynomial_functions_the_remainder_theorem", "remainder_theorem", "algebra_2", "polynomial_functions"),
    # Precalculus
    ("pc_law_of_sines", "law_of_sines", "precalculus", "trigonometry"),
    ("pc_law_of_cosines", "law_of_cosines", "precalculus", "trigonometry"),
    ("pc_area_and_laws_of_sines_and_cosines", "law_of_sines", "precalculus", "trigonometry"),
    ("pc_right_triangle_trig_finding_ratios", "geo_right_triangle_trig_ratio", "precalculus", "trigonometry"),
    ("pc_right_triangle_trig_finding_angles_and_sides", "geo_right_triangle_trig", "precalculus", "trigonometry"),
    ("pc_inverse_trig_functions", "inverse_trig_functions", "precalculus", "trigonometry"),
    ("pc_binomial_theorem", "binomial_theorem", "precalculus", "discrete_mathematics"),
    ("pc_compound_interest", "compound_interest", "precalculus", "exponential_and_logarithmic_expressions"),
    ("pc_remainder_theorem_and_bounds_of_real_zeros", "remainder_theorem", "precalculus", "power_polynomial_and_rational_functions"),
    ("pc_vectors_basics", "vector_basics", "precalculus", "vectors"),
    ("pc_dot_products", "dot_product", "precalculus", "vectors"),
    ("pc_polar_coordinates", "polar_coordinates", "precalculus", "polar_coordinates"),
    ("pc_limits_at_removable_discontinuities", "limit_removable", "precalculus", "introduction_to_calculus"),
    ("pc_limits_at_infinity", "limit_at_infinity", "precalculus", "introduction_to_calculus"),
    # Calculus
    ("calc_app_diff_related_rates", "related_rates_simple", "calculus", "applications_of_differentiation"),
    ("calc_app_diff_intervals_of_increase_and_decrease", "intervals_increase_decrease", "calculus", "applications_of_differentiation"),
    ("calc_app_diff_lhopitals_rule", "lhopitals_rule", "calculus", "applications_of_differentiation"),
    ("calc_diff_natural_logarithms_and_exponentials", "derivative_ln_exp", "calculus", "differentiation"),
    ("calc_diff_logarithmic", "derivative_ln_exp", "calculus", "differentiation"),
    ("calc_app_int_area_between_curves", "area_between_curves", "calculus", "applications_of_integration"),
    ("calc_limits_at_essential_discontinuities", "limit_removable", "calculus", "limits"),
]

CATALOG_FILES = {
    "algebra_1": ROOT / "question_engine" / "catalogs" / "algebra_1.py",
    "grade_6": ROOT / "question_engine" / "catalogs" / "grade_6.py",
    "pre_algebra": ROOT / "question_engine" / "catalogs" / "pre_algebra.py",
    "algebra_2": ROOT / "question_engine" / "catalogs" / "algebra_2.py",
    "geometry": ROOT / "question_engine" / "catalogs" / "geometry.py",
    "precalculus": ROOT / "question_engine" / "catalogs" / "precalculus.py",
    "calculus": ROOT / "question_engine" / "catalogs" / "calculus.py",
}

STUB = '''"""Catalog generator type: {type_id}."""

from question_engine.types._from_generator import register_from_catalog

register_from_catalog("{type_id}")
'''


def set_generator(catalog_path: Path, type_id: str, generator: str) -> str:
    """Set or replace generator= on a catalog entry. Returns status."""
    text = catalog_path.read_text(encoding="utf-8")
    if f'"{type_id}"' not in text:
        return "missing"

    # Already correct
    if re.search(
        rf'"{re.escape(type_id)}"[\s\S]{{0,400}}?generator="{re.escape(generator)}"',
        text,
    ):
        return "ok"

    # Replace existing generator=
    pattern = rf'("{re.escape(type_id)}"[\s\S]{{0,400}}?generator=")[^"]+(")'
    new_text, n = re.subn(pattern, rf'\1{generator}\2', text, count=1)
    if n == 1:
        catalog_path.write_text(new_text, encoding="utf-8")
        return "replaced"

    # Insert generator= after name for scaffold entries (reuse prior patterns)
    patterns = [
        (
            rf'(_g6\("[^"]+",\s*"{re.escape(type_id)}",\s*"[^"]+",)\s*(instruction)',
            rf'\1 generator="{generator}", \2',
        ),
        (
            rf'(_pa\("[^"]+",\s*"{re.escape(type_id)}",\s*"[^"]+",)\s*(instruction)',
            rf'\1 generator="{generator}", \2',
        ),
        (
            rf'(_a2\("[^"]+",\s*"{re.escape(type_id)}",\s*"[^"]+",)\s*(instruction)',
            rf'\1 generator="{generator}", \2',
        ),
        (
            rf'(_pc\("[^"]+",\s*"{re.escape(type_id)}",\s*"[^"]+",)\s*(instruction)',
            rf'\1 generator="{generator}", \2',
        ),
        (
            rf'(_calc\(\s*\n\s*"[^"]+",\s*\n\s*"{re.escape(type_id)}",\s*\n\s*"[^"]+",)\s*\n(\s*instruction)',
            rf'\1\n        generator="{generator}",\n\2',
        ),
        (
            rf'(entry\(\s*\n\s*"{re.escape(type_id)}",[\s\S]*?"[^"]+",\s*\n\s*"[^"]+",)\s*\n(\s*instruction)',
            rf'\1\n        generator="{generator}",\n\2',
        ),
        (
            rf'("{re.escape(type_id)}",\s*\n\s*"[^"]+",)\s*\n(\s*(?:instruction|count_default)=)',
            rf'\1\n        generator="{generator}",\n\2',
        ),
        (
            rf'("{re.escape(type_id)}",\s*"[^"]+",)\s*(instruction)',
            rf'\1 generator="{generator}", \2',
        ),
    ]
    for pat, repl in patterns:
        new_text, n = re.subn(pat, repl, text, count=1)
        if n == 1:
            catalog_path.write_text(new_text, encoding="utf-8")
            return "inserted"
    return "failed"


def create_stub(course: str, chapter: str, type_id: str) -> None:
    stub_dir = ROOT / "question_engine" / "types" / course / chapter
    stub_dir.mkdir(parents=True, exist_ok=True)
    path = stub_dir / f"{type_id}.py"
    if not path.exists():
        path.write_text(STUB.format(type_id=type_id), encoding="utf-8")


def main() -> None:
    ok = fail = skip = 0
    for type_id, generator, course, chapter in WIRING:
        status = set_generator(CATALOG_FILES[course], type_id, generator)
        if status in ("ok", "replaced", "inserted"):
            create_stub(course, chapter, type_id)
            print(f"{status.upper():8} {type_id} -> {generator}")
            ok += 1
        elif status == "missing":
            print(f"MISSING  {type_id}")
            fail += 1
        else:
            print(f"FAILED   {type_id}")
            fail += 1
    print(f"\nDone: ok={ok} fail={fail}")


if __name__ == "__main__":
    main()
