"""Wire tier-3 scaffold catalog entries to existing generators (dedup + hand-written keys)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# (catalog_id, generator, course, chapter_folder)
TIER3_WIRING: list[tuple[str, str, str, str]] = [
    # Algebra 1 — trigonometry dedup
    ("finding_sine_cosine_tangent", "trig_evaluate", "algebra_1", "beginning_trigonometry"),
    ("finding_angles", "finding_angles", "algebra_1", "beginning_trigonometry"),
    ("find_missing_sides_of_triangles", "geo_pythagorean_theorem", "algebra_1", "beginning_trigonometry"),
    # Algebra 2 — polynomials, radicals, rationals, logs, trig, sequences
    ("a2_beginning_algebra_order_of_operations", "order_of_operations", "algebra_2", "beginning_algebra"),
    (
        "a2_polynomial_functions_conjugate_roots_and_factoring",
        "polynomial_factoring_special_cases",
        "algebra_2",
        "polynomial_functions",
    ),
    (
        "a2_radical_functions_and_rational_exponents_evaluating_rational_exponent_expressions",
        "properties_of_exponents",
        "algebra_2",
        "radical_functions_and_rational_exponents",
    ),
    (
        "a2_radical_functions_and_rational_exponents_rational_exponent_equations",
        "radical_equations",
        "algebra_2",
        "radical_functions_and_rational_exponents",
    ),
    ("a2_rational_expressions_equations", "radical_equations", "algebra_2", "rational_expressions"),
    ("a2_rational_expressions_graphing", "rational_simplification", "algebra_2", "rational_expressions"),
    (
        "a2_exponential_and_logarithmic_expressions_exponential_equations_requiring_logarithms",
        "exponential_equation_with_log",
        "algebra_2",
        "exponential_and_logarithmic_expressions",
    ),
    (
        "a2_exponential_and_logarithmic_expressions_evaluating_logarithms",
        "log_evaluate",
        "algebra_2",
        "exponential_and_logarithmic_expressions",
    ),
    (
        "a2_exponential_and_logarithmic_expressions_properties_of_logarithms",
        "log_change_of_base",
        "algebra_2",
        "exponential_and_logarithmic_expressions",
    ),
    (
        "a2_exponential_and_logarithmic_expressions_logarithmic_equations_simple",
        "log_equation_simple",
        "algebra_2",
        "exponential_and_logarithmic_expressions",
    ),
    (
        "a2_exponential_and_logarithmic_expressions_logarithmic_equations_hard",
        "log_equation_simple",
        "algebra_2",
        "exponential_and_logarithmic_expressions",
    ),
    (
        "a2_exponential_and_logarithmic_expressions_exponents_and_logarithms",
        "properties_of_exponents",
        "algebra_2",
        "exponential_and_logarithmic_expressions",
    ),
    (
        "a2_trigonometry_right_triangle_trig_finding_ratios",
        "trig_evaluate",
        "algebra_2",
        "trigonometry",
    ),
    (
        "a2_trigonometry_right_triangle_trig_finding_angle_measures",
        "trig_evaluate",
        "algebra_2",
        "trigonometry",
    ),
    (
        "a2_trigonometry_right_triangle_trig_angles_and_sides",
        "geo_pythagorean_theorem",
        "algebra_2",
        "trigonometry",
    ),
    ("a2_trigonometry_trig_functions_of_any_angle", "trig_evaluate", "algebra_2", "trigonometry"),
    (
        "a2_trigonometry_angle_sum_difference_identities",
        "trig_basic_identities",
        "algebra_2",
        "trigonometry",
    ),
    (
        "a2_trigonometry_double_angle_half_angle_identities",
        "trig_basic_identities",
        "algebra_2",
        "trigonometry",
    ),
    (
        "a2_sequences_and_series_arithmetic_series",
        "sequence_arithmetic_nth_term",
        "algebra_2",
        "sequences_and_series",
    ),
    (
        "a2_sequences_and_series_geometric_series",
        "sequence_geometric_nth_term",
        "algebra_2",
        "sequences_and_series",
    ),
    (
        "a2_probability_and_statistics_probability_of_independent_and_dependent_events_word_problems",
        "wp_percent",
        "algebra_2",
        "probability_and_statistics",
    ),
    (
        "a2_probability_and_statistics_probability_of_mutually_exclusive_events_word_problems",
        "wp_percent",
        "algebra_2",
        "probability_and_statistics",
    ),
    # Pre-Algebra — integer ops dedup to rational generators
    ("pa_integers_adding_and_subtracting", "rational_add_subtract", "pre_algebra", "integers_decimals_and_fractions"),
    ("pa_integers_multiplying", "rational_multiply", "pre_algebra", "integers_decimals_and_fractions"),
    ("pa_integers_dividing", "rational_divide", "pre_algebra", "integers_decimals_and_fractions"),
    (
        "pa_greatest_common_factor",
        "polynomial_factoring_common_factor",
        "pre_algebra",
        "integers_decimals_and_fractions",
    ),
    ("pa_least_common_multiple", "g6_least_common_multiple", "pre_algebra", "integers_decimals_and_fractions"),
    ("pa_factoring", "g6_factoring", "pre_algebra", "integers_decimals_and_fractions"),
    ("pa_simplifying_fractions", "rational_simplification", "pre_algebra", "integers_decimals_and_fractions"),
    ("pa_fractions_decimals_and_percents", "percents", "pre_algebra", "percents"),
    ("pa_checking_for_a_proportion", "solving_proportions", "pre_algebra", "proportions_and_similarity"),
    ("pa_similar_figures", "wp_similar_figures", "pre_algebra", "proportions_and_similarity"),
    ("pa_squares_and_square_roots", "pa_squares_and_square_roots", "pre_algebra", "factors_and_exponents"),
    ("pythagorean_theorem", "geo_pythagorean_theorem", "pre_algebra", "right_triangles"),
    # Grade 6 — dedup variants
    ("g6_comparing_ratios", "g6_equivalent_ratios", "grade_6", "ratios"),
    ("g6_comparing_rates", "g6_comparing_rates", "grade_6", "rates"),
    ("g6_solving_percent_problems_with_diagrams", "wp_percent", "grade_6", "percents"),
    (
        "g6_distributive_property_area_diagrams_algebraic",
        "distributive_property",
        "grade_6",
        "equivalent_expressions",
    ),
    # Algebra 2 — logs / trig / more dedup
    (
        "a2_exponential_and_logarithmic_expressions_inverses_of_exponential_and_logarithmic_functions",
        "inverse_function_basic",
        "algebra_2",
        "exponential_and_logarithmic_expressions",
    ),
    (
        "a2_exponential_and_logarithmic_expressions_writing_logs_in_terms_of_others",
        "log_change_of_base",
        "algebra_2",
        "exponential_and_logarithmic_expressions",
    ),
    ("a2_trigonometry_radians_and_degrees", "trig_unit_circle", "algebra_2", "trigonometry"),
    ("a2_trigonometry_equations", "radical_equations", "algebra_2", "trigonometry"),
    # Pre-Algebra — more integer/number dedup
    ("pa_converting_fractions_and_decimals", "percents", "pre_algebra", "integers_decimals_and_fractions"),
    ("pa_writing_numbers_with_words", "verbal_expressions", "pre_algebra", "integers_decimals_and_fractions"),
    (
        "pa_naming_decimal_places_and_rounding",
        "polynomial_naming",
        "pre_algebra",
        "integers_decimals_and_fractions",
    ),
    # Algebra 1 — number classification uses rational generator settings
    ("sets_of_numbers", "rational_add_subtract", "algebra_1", "beginning_algebra"),
]

CATALOG_FILES = {
    "algebra_1": ROOT / "question_engine" / "catalogs" / "algebra_1.py",
    "grade_6": ROOT / "question_engine" / "catalogs" / "grade_6.py",
    "pre_algebra": ROOT / "question_engine" / "catalogs" / "pre_algebra.py",
    "algebra_2": ROOT / "question_engine" / "catalogs" / "algebra_2.py",
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
    if re.search(rf'"{re.escape(type_id)}"[\s\S]{{0,300}}?generator="{re.escape(generator)}"', text):
        print(f"  already wired: {type_id}")
        return False
    if re.search(rf'"{re.escape(type_id)}"[\s\S]{{0,300}}?generator="(?!scaffold")[^"]+"', text):
        print(f"  SKIP catalog: {type_id} has different generator")
        return False

    pattern_entry = (
        rf'(entry\(\s*\n\s*"{re.escape(type_id)}",[\s\S]*?"[^"]+",\s*\n\s*"[^"]+",)\s*\n(\s*instruction)'
    )
    new_text, count = re.subn(
        pattern_entry,
        rf'\1\n        generator="{generator}",\n\2',
        text,
        count=1,
    )
    if count != 1:
        pattern_ml = rf'("{re.escape(type_id)}",\s*\n\s*"[^"]+",)\s*\n(\s*(?:instruction|count_default)=)'
        new_text, count = re.subn(
            pattern_ml,
            rf'\1\n        generator="{generator}",\n\2',
            text,
            count=1,
        )
    if count != 1:
        pattern_sl = rf'("{re.escape(type_id)}",\s*"[^"]+",)\s*(instruction)'
        new_text, count = re.subn(
            pattern_sl,
            rf'\1 generator="{generator}", \2',
            text,
            count=1,
        )
    if count != 1:
        print(f"  FAIL catalog patch: {type_id}")
        return False
    catalog_path.write_text(new_text, encoding="utf-8")
    return True


def create_stub(course: str, chapter: str, type_id: str) -> Path:
    stub_dir = ROOT / "question_engine" / "types" / course / chapter
    stub_dir.mkdir(parents=True, exist_ok=True)
    stub_path = stub_dir / f"{type_id}.py"
    if not stub_path.exists():
        stub_path.write_text(STUB_TEMPLATE.format(type_id=type_id), encoding="utf-8")
    return stub_path


def main() -> None:
    wired: list[tuple[str, str]] = []
    for type_id, generator, course, chapter in TIER3_WIRING:
        catalog_path = CATALOG_FILES[course]
        if wire_catalog(catalog_path, type_id, generator):
            create_stub(course, chapter, type_id)
            wired.append((type_id, generator))
            print(f"WIRED {type_id} -> {generator}")
    print(f"\nTotal wired: {len(wired)}")


if __name__ == "__main__":
    main()
