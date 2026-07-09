"""Wire additional batch3 scaffold entries (pass 3)."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.apply_batch3_wiring_v2 import wire_entry, create_stub

EXTRA: list[tuple[str, str, str, str]] = [
    ("g6_relating_percents_fractions_and_decimals", "percents", "grade_6", "percents"),
    ("g6_finding_percents_with_equivalent_fractions", "percents", "grade_6", "percents"),
    ("g6_solving_percent_problems_with_formulas", "percents", "grade_6", "percents"),
    ("g6_equivalent_ratio_equations", "solving_proportions", "grade_6", "equations_as_relationships_between_two_variables"),
    ("pa_greatest_common_factor", "g6_greatest_common_factor", "pre_algebra", "integers_decimals_and_fractions"),
    ("pa_least_common_multiple", "g6_least_common_multiple", "pre_algebra", "integers_decimals_and_fractions"),
    ("pa_simplifying_fractions", "rational_divide", "pre_algebra", "integers_decimals_and_fractions"),
    ("a2_exponential_and_logarithmic_expressions_logarithmic_equations_hard", "log_equation_simple", "algebra_2", "exponential_and_logarithmic_expressions"),
    ("a2_trigonometry_right_triangle_trig_finding_angle_measures", "trig_evaluate", "algebra_2", "trigonometry"),
    ("a2_trigonometry_right_triangle_trig_angles_and_sides", "trig_evaluate", "algebra_2", "trigonometry"),
    ("geo_right_special_right_triangles", "geo_pythagorean_theorem", "geometry", "right_triangles"),
    ("geo_probability_permutations", "stats_counting_principle", "geometry", "probability_and_statistics"),
    ("geo_probability_combinations", "stats_counting_principle", "geometry", "probability_and_statistics"),
    ("pc_radians_and_degrees", "trig_evaluate", "precalculus", "trigonometry"),
]

CATALOG_FILES = {
    "grade_6": ROOT / "question_engine" / "catalogs" / "grade_6.py",
    "pre_algebra": ROOT / "question_engine" / "catalogs" / "pre_algebra.py",
    "algebra_2": ROOT / "question_engine" / "catalogs" / "algebra_2.py",
    "geometry": ROOT / "question_engine" / "catalogs" / "geometry.py",
    "precalculus": ROOT / "question_engine" / "catalogs" / "precalculus.py",
}


def main() -> None:
    wired = 0
    for type_id, generator, course, chapter in EXTRA:
        if wire_entry(CATALOG_FILES[course], type_id, generator):
            create_stub(course, chapter, type_id)
            wired += 1
            print(f"WIRED {type_id} -> {generator}")
    print(f"Total: {wired}")


if __name__ == "__main__":
    main()
