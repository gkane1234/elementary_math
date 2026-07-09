"""Apply batch 3 non-graphing scaffold wiring (40+ types)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# (catalog_id, generator, course, chapter_folder)
WIRING: list[tuple[str, str, str, str]] = [
    # Algebra 1
    ("sets_of_numbers", "order_of_operations", "algebra_1", "beginning_algebra"),
    # Grade 6
    ("g6_part_part_whole_ratios", "g6_introduction_to_ratios", "grade_6", "ratios"),
    ("g6_comparing_ratios", "g6_equivalent_ratios", "grade_6", "ratios"),
    ("g6_comparing_rates", "g6_unit_rates", "grade_6", "rates"),
    ("g6_converting_units", "g6_unit_rates", "grade_6", "rates"),
    ("g6_solving_percent_problems_with_diagrams", "percents", "grade_6", "percents"),
    # Pre-Algebra
    ("pa_checking_for_a_proportion", "solving_proportions", "pre_algebra", "proportions_and_similarity"),
    ("pa_fractions_decimals_and_percents", "percents", "pre_algebra", "percents"),
    ("pa_converting_fractions_and_decimals", "percents", "pre_algebra", "percents"),
    ("pa_factoring", "g6_factoring", "pre_algebra", "integers_decimals_and_fractions"),
    ("pa_similar_figures", "wp_similar_figures", "pre_algebra", "proportions_and_similarity"),
    ("pythagorean_theorem", "geo_pythagorean_theorem", "pre_algebra", "right_triangles"),
    # Algebra 2
    ("a2_beginning_algebra_order_of_operations", "order_of_operations", "algebra_2", "beginning_algebra"),
    ("a2_radical_functions_and_rational_exponents_evaluating_rational_exponent_expressions", "properties_of_exponents", "algebra_2", "radical_functions_and_rational_exponents"),
    ("a2_radical_functions_and_rational_exponents_rational_exponent_equations", "radical_equations", "algebra_2", "radical_functions_and_rational_exponents"),
    ("a2_rational_expressions_equations", "radical_equations", "algebra_2", "rational_expressions"),
    ("a2_exponential_and_logarithmic_expressions_exponents_and_logarithms", "log_evaluate", "algebra_2", "exponential_and_logarithmic_expressions"),
    ("a2_exponential_and_logarithmic_expressions_writing_logs_in_terms_of_others", "log_change_of_base", "algebra_2", "exponential_and_logarithmic_expressions"),
    ("a2_exponential_and_logarithmic_expressions_logarithms_and_exponents_as_inverses", "log_evaluate", "algebra_2", "exponential_and_logarithmic_expressions"),
    ("a2_sequences_and_series_general_sequences", "sequence_arithmetic_nth_term", "algebra_2", "sequences_and_series"),
    ("a2_sequences_and_series_general_series", "sequence_arithmetic_nth_term", "algebra_2", "sequences_and_series"),
    ("a2_sequences_and_series_arithmetic_and_geometric_mean", "sequence_arithmetic_nth_term", "algebra_2", "sequences_and_series"),
    ("a2_trigonometry_radians_and_degrees", "trig_evaluate", "algebra_2", "trigonometry"),
    ("a2_probability_and_statistics_permutations", "stats_counting_principle", "algebra_2", "probability_and_statistics"),
    ("a2_probability_and_statistics_combinations", "stats_counting_principle", "algebra_2", "probability_and_statistics"),
    ("a2_complex_numbers_rationalizing_denominators", "radical_simplification", "algebra_2", "complex_numbers"),
    # Geometry
    ("geo_trig_finding_trig_ratios", "trig_evaluate", "geometry", "trigonometry"),
    ("geo_trig_finding_angle_measures", "trig_evaluate", "geometry", "trigonometry"),
    ("geo_trig_solving_right_triangles", "geo_pythagorean_theorem", "geometry", "right_triangles"),
    ("geo_right_multi_step_pythagorean_theorem_problems", "geo_pythagorean_theorem", "geometry", "right_triangles"),
    ("geo_trig_multi_step_trig_problems", "trig_evaluate", "geometry", "trigonometry"),
    ("geo_trig_rhombuses_and_kites_with_right_triangles", "geo_pythagorean_theorem", "geometry", "trigonometry"),
    ("geo_trig_trigonometry_and_area", "geo_triangle_area", "geometry", "trigonometry"),
    ("geo_similarity_similar_right_triangles", "geo_similar_triangles", "geometry", "similarity"),
    ("geo_probability_independent_and_dependent_events_word_problems", "stats_probability_compound_independent", "geometry", "probability_and_statistics"),
    ("geo_probability_mutually_exclusive_events_word_problems", "stats_probability_mutually_exclusive", "geometry", "probability_and_statistics"),
    ("geo_probability_with_permutations_and_combinations", "stats_counting_principle", "geometry", "probability_and_statistics"),
    # Precalculus
    ("pc_right_triangle_trig_finding_ratios", "trig_evaluate", "precalculus", "trigonometry"),
    ("pc_right_triangle_trig_finding_angles_and_sides", "trig_evaluate", "precalculus", "trigonometry"),
    ("pc_simple_trig_equations", "trig_evaluate", "precalculus", "trigonometry"),
    ("pc_probability_independent_dependent_events_word_problems", "stats_probability_compound_independent", "precalculus", "probability_and_statistics"),
    ("pc_probability_mutually_exclusive_word_problems", "stats_probability_mutually_exclusive", "precalculus", "probability_and_statistics"),
    ("pc_probability_with_permutations_and_combinations", "stats_counting_principle", "precalculus", "probability_and_statistics"),
    ("pc_properties_of_logarithms", "log_change_of_base", "precalculus", "exponential_and_logarithmic_expressions"),
    ("pc_logarithmic_equations_hard", "log_equation_simple", "precalculus", "exponential_and_logarithmic_expressions"),
    ("pc_exponents_and_logarithms", "log_evaluate", "precalculus", "exponential_and_logarithmic_expressions"),
    ("pc_logarithms_and_exponents_as_inverses", "log_evaluate", "precalculus", "exponential_and_logarithmic_expressions"),
    # Pre-Algebra extras
    ("pa_writing_numbers_with_words", "verbal_expressions", "pre_algebra", "integers_decimals_and_fractions"),
]

CATALOG_FILES = {
    "grade_6": ROOT / "question_engine" / "catalogs" / "grade_6.py",
    "pre_algebra": ROOT / "question_engine" / "catalogs" / "pre_algebra.py",
    "algebra_1": ROOT / "question_engine" / "catalogs" / "algebra_1.py",
    "algebra_2": ROOT / "question_engine" / "catalogs" / "algebra_2.py",
    "geometry": ROOT / "question_engine" / "catalogs" / "geometry.py",
    "precalculus": ROOT / "question_engine" / "catalogs" / "precalculus.py",
}

STUB_TEMPLATE = '''"""Catalog generator type: {type_id}."""

from question_engine.types._from_generator import register_from_catalog

register_from_catalog("{type_id}")
'''


def wire_catalog(catalog_path: Path, type_id: str, generator: str) -> bool:
    text = catalog_path.read_text(encoding="utf-8")
    if f'"{type_id}"' not in text:
        print(f"  SKIP catalog: {type_id} not in {catalog_path.name}")
        return False
    if re.search(
        rf'"{re.escape(type_id)}"[\s\S]{{0,400}}?generator="{re.escape(generator)}"',
        text,
    ):
        print(f"  already wired: {type_id}")
        return False
    if re.search(
        rf'"{re.escape(type_id)}"[\s\S]{{0,400}}?generator="(?!scaffold")[^"]+"',
        text,
    ):
        print(f"  SKIP catalog: {type_id} has different generator")
        return False

    patterns = [
        (
            rf'("{re.escape(type_id)}",\s*\n\s*"[^"]+",)\s*\n(\s*(?:instruction|count_default)=)',
            rf'\1\n        generator="{generator}",\n\2',
        ),
        (
            rf'("{re.escape(type_id)}",\s*"[^"]+",)\s*(instruction)',
            rf'\1 generator="{generator}", \2',
        ),
        (
            rf'(\s+"{re.escape(type_id)}",\s*\n\s+"[^"]+",\s*\n\s+"[^"]+",)\s*\n(\s+instruction)',
            rf'\1\n        generator="{generator}",\n\2',
        ),
    ]
    for pattern, repl in patterns:
        new_text, count = re.subn(pattern, repl, text, count=1)
        if count == 1:
            catalog_path.write_text(new_text, encoding="utf-8")
            return True
    print(f"  FAIL catalog patch: {type_id}")
    return False


def create_stub(course: str, chapter: str, type_id: str) -> None:
    stub_dir = ROOT / "question_engine" / "types" / course / chapter
    stub_dir.mkdir(parents=True, exist_ok=True)
    stub_path = stub_dir / f"{type_id}.py"
    if not stub_path.exists():
        stub_path.write_text(STUB_TEMPLATE.format(type_id=type_id), encoding="utf-8")


def main() -> None:
    wired: list[tuple[str, str]] = []
    for type_id, generator, course, chapter in WIRING:
        catalog_path = CATALOG_FILES[course]
        if wire_catalog(catalog_path, type_id, generator):
            create_stub(course, chapter, type_id)
            wired.append((type_id, generator))
            print(f"WIRED {type_id} -> {generator}")
    print(f"\nTotal newly wired: {len(wired)}")


if __name__ == "__main__":
    main()
