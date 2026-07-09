"""Apply Tier 2 generator wiring: catalog entries + type stubs."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# (catalog_id, generator, course, chapter_folder)
WIRING = [
    # Grade 6 — curriculum dedup
    ("g6_distributive_property_numeric", "distributive_property", "grade_6", "numeric_expressions_exponents_and_order_of_operations"),
    ("g6_distributive_property_algebraic", "distributive_property", "grade_6", "equivalent_expressions"),
    ("g6_solving_and_graphing_one_step_inequalities", "one_step_inequalities", "grade_6", "inequalities"),
    # Pre-Algebra
    ("pa_equations_multi_step_equations", "multi_step_equations", "pre_algebra", "equations"),
    ("pa_multi_step_inequalities", "multi_step_inequalities", "pre_algebra", "inequalities"),
    ("pa_systems_substitution", "systems_substitution", "pre_algebra", "linear_equations_and_inequalities"),
    ("pa_polynomials_adding_and_subtracting", "polynomial_add_subtract", "pre_algebra", "beginning_polynomials"),
    ("pa_polynomials_multiplying", "polynomial_multiply", "pre_algebra", "beginning_polynomials"),
    # Algebra 2 — curriculum dedup to basic.py generators
    ("a2_equations_and_inequalities_multi_step_equations", "multi_step_equations", "algebra_2", "equations_and_inequalities"),
    ("a2_equations_and_inequalities_absolute_value_equations", "absolute_value_equations", "algebra_2", "equations_and_inequalities"),
    ("a2_equations_and_inequalities_multi_step_inequalities", "multi_step_inequalities", "algebra_2", "equations_and_inequalities"),
    ("a2_equations_and_inequalities_compound_inequalities", "compound_inequalities", "algebra_2", "equations_and_inequalities"),
    ("a2_equations_and_inequalities_absolute_value_inequalities", "absolute_value_inequalities", "algebra_2", "equations_and_inequalities"),
    ("a2_relations_and_introduction_to_functions_discrete_relations", "discrete_relations", "algebra_2", "relations_and_introduction_to_functions"),
    ("a2_relations_and_introduction_to_functions_continuous_relations", "continuous_relations", "algebra_2", "relations_and_introduction_to_functions"),
    ("a2_relations_and_introduction_to_functions_evaluating_and_graphing_functions", "evaluating_graphing_functions", "algebra_2", "relations_and_introduction_to_functions"),
    ("a2_linear_relations_and_functions_writing_linear_equations", "writing_linear_equations", "algebra_2", "linear_relations_and_functions"),
    ("a2_direct_and_inverse_variation_direct_and_inverse_variation", "direct_inverse_variation", "algebra_2", "direct_and_inverse_variation"),
    ("a2_systems_of_equations_and_inequalities_solving_systems_by_elimination_2_variables", "systems_elimination", "algebra_2", "systems_of_equations_and_inequalities"),
    ("a2_systems_of_equations_and_inequalities_solving_systems_by_substitution_2_variables", "systems_substitution", "algebra_2", "systems_of_equations_and_inequalities"),
    ("a2_quadratic_functions_and_inequalities_solving_equations_by_taking_square_roots", "quadratic_square_roots", "algebra_2", "quadratic_functions_and_inequalities"),
    ("a2_quadratic_functions_and_inequalities_solving_equations_by_factoring", "quadratic_factoring_equations", "algebra_2", "quadratic_functions_and_inequalities"),
    ("a2_quadratic_functions_and_inequalities_solving_equations_by_completing_the_square", "quadratic_completing_square_solve", "algebra_2", "quadratic_functions_and_inequalities"),
    ("a2_quadratic_functions_and_inequalities_solving_equations_with_the_quadratic_formula", "quadratic_formula", "algebra_2", "quadratic_functions_and_inequalities"),
    ("a2_polynomial_functions_naming", "polynomial_naming", "algebra_2", "polynomial_functions"),
    ("a2_polynomial_functions_adding_and_subtracting", "polynomial_add_subtract", "algebra_2", "polynomial_functions"),
    ("a2_polynomial_functions_multiplying", "polynomial_multiply", "algebra_2", "polynomial_functions"),
    ("a2_polynomial_functions_multiplying_special_cases", "polynomial_multiply_special", "algebra_2", "polynomial_functions"),
    ("a2_polynomial_functions_factoring_by_grouping", "polynomial_factoring_grouping", "algebra_2", "polynomial_functions"),
    ("a2_radical_functions_and_rational_exponents_adding_and_subtracting_radical_expressions", "radical_add_subtract", "algebra_2", "radical_functions_and_rational_exponents"),
    ("a2_radical_functions_and_rational_exponents_multiplying_radical_expressions", "radical_multiply", "algebra_2", "radical_functions_and_rational_exponents"),
    ("a2_radical_functions_and_rational_exponents_dividing_radical_expressions", "radical_divide", "algebra_2", "radical_functions_and_rational_exponents"),
    ("a2_radical_functions_and_rational_exponents_radical_equations", "radical_equations", "algebra_2", "radical_functions_and_rational_exponents"),
    ("a2_rational_expressions_multiplying_and_dividing", "rational_expression_multiply_divide", "algebra_2", "rational_expressions"),
    ("a2_exponential_and_logarithmic_expressions_discrete_exponential_growth_and_decay_word_problems", "exponential_growth_decay", "algebra_2", "exponential_and_logarithmic_expressions"),
    # Geometry
    ("geo_review_multi_step_equations", "multi_step_equations", "geometry", "review_of_algebra"),
    ("geo_parallel_writing_linear_equations", "writing_linear_equations", "geometry", "parallel_lines_and_the_coordinate_plane"),
]

CATALOG_FILES = {
    "grade_6": ROOT / "question_engine" / "catalogs" / "grade_6.py",
    "pre_algebra": ROOT / "question_engine" / "catalogs" / "pre_algebra.py",
    "algebra_2": ROOT / "question_engine" / "catalogs" / "algebra_2.py",
    "geometry": ROOT / "question_engine" / "catalogs" / "geometry.py",
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

    # Multiline catalog helper (_g6, _pa, _geo): id + name then instruction/count
    pattern_ml = (
        rf'("{re.escape(type_id)}",\s*\n\s*"[^"]+",)\s*\n(\s*(?:instruction|count_default)=)'
    )
    new_text, count = re.subn(
        pattern_ml,
        rf'\1\n        generator="{generator}",\n\2',
        text,
        count=1,
    )
    if count != 1:
        # Single-line _a2(..., "id", "name", instruction_...)
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
    stub_path.write_text(STUB_TEMPLATE.format(type_id=type_id), encoding="utf-8")
    return stub_path


def main() -> None:
    wired = []
    for type_id, generator, course, chapter in WIRING:
        catalog_path = CATALOG_FILES[course]
        if wire_catalog(catalog_path, type_id, generator):
            create_stub(course, chapter, type_id)
            wired.append((type_id, generator))
            print(f"WIRED {type_id} -> {generator}")
    print(f"\nTotal wired: {len(wired)}")


if __name__ == "__main__":
    main()
