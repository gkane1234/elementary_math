"""Consolidate duplicate question types across course catalogs.

Run from repo root: python scripts/consolidate_duplicates.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# duplicate_id -> canonical_id
MERGE_MAP: dict[str, str] = {
    # Pre-Algebra -> Algebra 1 (or shared) canonical IDs
    "pa_verbal_expressions": "verbal_expressions",
    "pa_order_of_operations": "order_of_operations",
    "pa_distributive_property": "distributive_property",
    "pa_equations_one_step_equations": "one_step_equations",
    "pa_equations_two_step_equations": "two_step_equations",
    "pa_graphing_single_variable_inequalities": "graphing_single_variable_inequalities",
    "pa_one_step_inequalities": "one_step_inequalities",
    "pa_two_step_inequalities": "two_step_inequalities",
    "pa_properties_of_exponents": "properties_of_exponents",
    "pa_writing_scientific_notation": "scientific_notation_write",
    "pa_operations_and_scientific_notation": "scientific_notation_operations",
    "pa_solving_proportions": "solving_proportions",
    "pa_percent_of_change": "percent_of_change",
    "pa_percents_percents": "percents",
    "pa_slope": "slope",
    "pa_graphing_linear_equations": "graphing_linear_equations",
    "pa_writing_linear_equations": "writing_linear_equations",
    "pa_graphing_linear_inequalities": "graphing_linear_inequalities",
    "pa_midpoint_formula": "radical_midpoint_formula",
    "pa_distance_formula": "radical_distance_formula",
    "pa_pythagorean_theorem": "pythagorean_theorem",
    "pa_visualizing_data": "visualizing_data",
    "pa_center_and_spread": "center_and_spread",
    "pa_scatter_plots": "scatter_plots",
    "pa_using_statistical_models": "using_statistical_models",
    # Geometry -> shared
    "geo_similarity_solving_proportions": "solving_proportions",
    "geo_parallel_midpoint_formula": "radical_midpoint_formula",
    "geo_parallel_distance_formula": "radical_distance_formula",
    "geo_right_pythagorean_theorem": "pythagorean_theorem",
    # Algebra 2 -> Algebra 1 (review / identical topics)
    "a2_beginning_algebra_order_of_operations": "order_of_operations",
    "a2_equations_and_inequalities_absolute_value_equations": "absolute_value_equations",
    "a2_equations_and_inequalities_absolute_value_inequalities": "absolute_value_inequalities",
    "a2_equations_and_inequalities_compound_inequalities": "compound_inequalities",
    "a2_equations_and_inequalities_work_word_problems": "work_word_problems",
    "a2_equations_and_inequalities_distance_rate_time_word_problems": "distance_rate_time_word_problems",
    "a2_equations_and_inequalities_mixture_word_problems": "mixture_word_problems",
    "a2_relations_and_introduction_to_functions_discrete_relations": "discrete_relations",
    "a2_relations_and_introduction_to_functions_continuous_relations": "continuous_relations",
    "a2_relations_and_introduction_to_functions_evaluating_and_graphing_functions": "evaluating_graphing_functions",
    "a2_linear_relations_and_functions_graphing_linear_equations": "graphing_linear_equations",
    "a2_linear_relations_and_functions_writing_linear_equations": "writing_linear_equations",
    "a2_linear_relations_and_functions_graphing_absolute_value_equations": "graphing_absolute_value_equations",
    "a2_linear_relations_and_functions_graphing_linear_inequalities": "graphing_linear_inequalities",
    "a2_direct_and_inverse_variation_direct_and_inverse_variation": "direct_inverse_variation",
    "a2_exponential_and_logarithmic_expressions_discrete_exponential_growth_and_decay_word_problems": "exponential_growth_decay",
    "a2_exponential_and_logarithmic_expressions_graphing_exponential_functions": "graphing_exponential_functions",
    "a2_quadratic_functions_and_inequalities_graphing_quadratic_inequalities": "graphing_quadratic_inequalities",
    "a2_quadratic_functions_and_inequalities_solving_equations_by_taking_square_roots": "quadratic_square_roots",
    "a2_quadratic_functions_and_inequalities_solving_equations_by_factoring": "quadratic_factoring_equations",
    "a2_quadratic_functions_and_inequalities_solving_equations_by_completing_the_square": "quadratic_completing_square_solve",
    "a2_quadratic_functions_and_inequalities_solving_equations_with_the_quadratic_formula": "quadratic_formula",
    "a2_polynomial_functions_naming": "polynomial_naming",
    "a2_polynomial_functions_adding_and_subtracting": "polynomial_add_subtract",
    "a2_polynomial_functions_multiplying": "polynomial_multiply",
    "a2_polynomial_functions_multiplying_special_cases": "polynomial_multiply_special",
    "a2_rational_expressions_multiplying_and_dividing": "rational_expression_multiply_divide",
    # Precalculus -> Algebra 2 (identical topics)
    "pc_matrices_operations": "a2_matrices_operations",
    "pc_determinants": "a2_matrices_determinants",
    "pc_matrices_inverses": "a2_matrices_inverses",
    "pc_cramers_rule": "a2_matrices_cramer_s_rule",
    "pc_matrices_equations": "a2_matrices_equations",
    "pc_permutations": "a2_probability_and_statistics_permutations",
    "pc_combinations": "a2_probability_and_statistics_combinations",
    "pc_general_sequences": "a2_sequences_and_series_general_sequences",
    "pc_arithmetic_sequences": "a2_sequences_and_series_arithmetic_sequences",
    "pc_geometric_sequences": "a2_sequences_and_series_geometric_sequences",
    "pc_arithmetic_and_geometric_mean": "a2_sequences_and_series_arithmetic_and_geometric_mean",
    "pc_general_series": "a2_sequences_and_series_general_series",
    "pc_arithmetic_series": "a2_sequences_and_series_arithmetic_series",
    "pc_geometric_series": "a2_sequences_and_series_geometric_series",
}

# canonical_id -> category from earliest course appearance
CATEGORY_OVERRIDES: dict[str, str] = {
    "verbal_expressions": "Pre-Algebra — Beginning Algebra",
    "order_of_operations": "Pre-Algebra — Beginning Algebra",
    "distributive_property": "Pre-Algebra — Beginning Algebra",
    "one_step_equations": "Pre-Algebra — Equations",
    "two_step_equations": "Pre-Algebra — Equations",
    "graphing_single_variable_inequalities": "Pre-Algebra — Inequalities",
    "one_step_inequalities": "Pre-Algebra — Inequalities",
    "two_step_inequalities": "Pre-Algebra — Inequalities",
    "properties_of_exponents": "Pre-Algebra — Factors and Exponents",
    "scientific_notation_write": "Pre-Algebra — Factors and Exponents",
    "scientific_notation_operations": "Pre-Algebra — Factors and Exponents",
    "solving_proportions": "Pre-Algebra — Proportions and Similarity",
    "percent_of_change": "Pre-Algebra — Percents",
    "percents": "Pre-Algebra — Percents",
    "slope": "Pre-Algebra — Linear Equations and Inequalities",
    "graphing_linear_equations": "Pre-Algebra — Linear Equations and Inequalities",
    "writing_linear_equations": "Pre-Algebra — Linear Equations and Inequalities",
    "graphing_linear_inequalities": "Pre-Algebra — Linear Equations and Inequalities",
    "radical_midpoint_formula": "Pre-Algebra — Linear Equations and Inequalities",
    "radical_distance_formula": "Pre-Algebra — Right Triangles",
    "pythagorean_theorem": "Pre-Algebra — Right Triangles",
    "visualizing_data": "Pre-Algebra — Statistics",
    "center_and_spread": "Pre-Algebra — Statistics",
    "scatter_plots": "Pre-Algebra — Statistics",
    "using_statistical_models": "Pre-Algebra — Statistics",
}

CATALOG_FILES = {
  "catalogs/pre_algebra.py": "CATALOG",
  "catalogs/geometry.py": "CATALOG",
  "catalogs/algebra_2.py": "CATALOG",
  "catalogs/precalculus.py": "CATALOG",
}


def remove_entry_blocks(source: str, ids_to_remove: set[str]) -> str:
    """Remove catalog helper call blocks whose id string appears in ids_to_remove."""
    lines = source.splitlines(keepends=True)
    result: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if re.match(r"\s+_(?:pa|geo|a2|calc|pc|entry)\(", line):
            block = [line]
            i += 1
            depth = line.count("(") - line.count(")")
            while i < len(lines) and depth > 0:
                block.append(lines[i])
                depth += lines[i].count("(") - lines[i].count(")")
                i += 1
            block_text = "".join(block)
            id_match = re.search(r'"(?:[^"]+)"\s*,\s*"([^"]+)"\s*,', block_text)
            if not id_match:
                id_match = re.search(r'_entry\(\s*"([^"]+)"', block_text)
            entry_id = id_match.group(1) if id_match else None
            if entry_id and entry_id in ids_to_remove:
                continue
            result.extend(block)
        else:
            result.append(line)
            i += 1
    return "".join(result)


def apply_category_overrides(catalog_path: Path) -> None:
    text = catalog_path.read_text(encoding="utf-8")
    for canonical_id, category in CATEGORY_OVERRIDES.items():
        pattern = (
            rf'(_entry\(\s*"{re.escape(canonical_id)}"\s*,\s*"[^"]+"\s*,\s*)'
            rf'"([^"]+)"'
        )
        text, count = re.subn(pattern, rf'\1"{category}"', text, count=1)
        if count == 0:
            print(f"Warning: category override not applied for {canonical_id}")
    catalog_path.write_text(text, encoding="utf-8")


def add_pythagorean_canonical(catalog_path: Path) -> None:
    """Ensure pythagorean_theorem exists in prealgebra catalog with neutral id."""
    text = catalog_path.read_text(encoding="utf-8")
    if '"pythagorean_theorem"' in text:
        return
    # Should not happen if rename worked
    print("Warning: pythagorean_theorem entry missing")


def update_curriculum(curriculum_path: Path) -> None:
    text = curriculum_path.read_text(encoding="utf-8")
    for old_id, new_id in MERGE_MAP.items():
        text = text.replace(f'id: "{old_id}"', f'id: "{new_id}"')
    # Algebra 2 curriculum uses shortened ids - map those too
    a2_curriculum_map = {
        "a2_order_of_operations": "order_of_operations",
        "a2_absolute_value_equations": "absolute_value_equations",
        "a2_absolute_value_inequalities": "absolute_value_inequalities",
        "a2_compound_inequalities": "compound_inequalities",
        "a2_work_word_problems": "work_word_problems",
        "a2_distance_rate_time_word_problems": "distance_rate_time_word_problems",
        "a2_mixture_word_problems": "mixture_word_problems",
        "a2_discrete_relations": "discrete_relations",
        "a2_continuous_relations": "continuous_relations",
        "a2_evaluating_and_graphing_functions": "evaluating_graphing_functions",
        "a2_graphing_linear_equations": "graphing_linear_equations",
        "a2_writing_linear_equations": "writing_linear_equations",
        "a2_graphing_absolute_value_equations": "graphing_absolute_value_equations",
        "a2_graphing_linear_inequalities": "graphing_linear_inequalities",
        "a2_direct_and_inverse_variation": "direct_inverse_variation",
        "a2_graphing_quadratic_inequalities": "graphing_quadratic_inequalities",
        "a2_solving_equations_by_taking_square_roots": "quadratic_square_roots",
        "a2_solving_equations_by_factoring": "quadratic_factoring_equations",
        "a2_solving_equations_by_completing_the_square": "quadratic_completing_square_solve",
        "a2_solving_equations_with_the_quadratic_formula": "quadratic_formula",
        "a2_polynomial_functions_naming": "polynomial_naming",
        "a2_polynomial_functions_adding_and_subtracting": "polynomial_add_subtract",
        "a2_polynomial_functions_multiplying": "polynomial_multiply",
        "a2_polynomial_functions_multiplying_special_cases": "polynomial_multiply_special",
        "geo_similarity_solving_proportions": "solving_proportions",
    }
    curriculum_only_map = {
        "pa_pythagorean_theorem": "pythagorean_theorem",
    }
    for old_id, new_id in curriculum_only_map.items():
        text = text.replace(f'id: "{old_id}"', f'id: "{new_id}"')
    for old_id, new_id in a2_curriculum_map.items():
        text = text.replace(f'id: "{old_id}"', f'id: "{new_id}"')
    # Precalc curriculum shortened ids
    pc_curriculum_map = {
        "pc_matrices_operations": "a2_matrices_operations",
        "pc_determinants": "a2_matrices_determinants",
        "pc_matrices_inverses": "a2_matrices_inverses",
        "pc_cramers_rule": "a2_matrices_cramer_s_rule",
        "pc_permutations": "a2_probability_and_statistics_permutations",
        "pc_combinations": "a2_probability_and_statistics_combinations",
        "pc_general_sequences": "a2_sequences_and_series_general_sequences",
        "pc_arithmetic_sequences": "a2_sequences_and_series_arithmetic_sequences",
        "pc_geometric_sequences": "a2_sequences_and_series_geometric_sequences",
        "pc_arithmetic_and_geometric_mean": "a2_sequences_and_series_arithmetic_and_geometric_mean",
        "pc_general_series": "a2_sequences_and_series_general_series",
        "pc_arithmetic_series": "a2_sequences_and_series_arithmetic_series",
        "pc_geometric_series": "a2_sequences_and_series_geometric_series",
    }
    for old_id, new_id in pc_curriculum_map.items():
        text = text.replace(f'id: "{old_id}"', f'id: "{new_id}"')
    curriculum_path.write_text(text, encoding="utf-8")


def main() -> None:
    engine = ROOT / "question_engine"
    ids_to_remove = set(MERGE_MAP.keys())

    # Fix algebra2 export name
    a2_path = engine / "algebra2_catalog.py"
    a2_text = a2_path.read_text(encoding="utf-8")
    a2_text = a2_text.replace("A2_CATALOG:", "ALGEBRA2_CATALOG:")
    if "ALGEBRALGEBRA2_CATALOG" in a2_text:
        a2_text = a2_text.replace("ALGEBRALGEBRA2_CATALOG", "ALGEBRA2_CATALOG")
    a2_path.write_text(a2_text, encoding="utf-8")

    # Rename pythagorean canonical id in prealgebra before removal pass
    pa_path = engine / "prealgebra_catalog.py"
    pa_text = pa_path.read_text(encoding="utf-8")
    pa_text = pa_text.replace('"pa_pythagorean_theorem"', '"pythagorean_theorem"')
    pa_path.write_text(pa_text, encoding="utf-8")
    ids_to_remove.discard("pa_pythagorean_theorem")

    for filename in CATALOG_FILES:
        path = engine / filename
        text = path.read_text(encoding="utf-8")
        new_text = remove_entry_blocks(text, ids_to_remove)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8")
            print(f"Updated {filename}")

    apply_category_overrides(engine / "catalog.py")
    update_curriculum(ROOT / "lib" / "curriculum.ts")
    print(f"Merged {len(MERGE_MAP)} duplicate entries")
    print("Done.")


if __name__ == "__main__":
    main()
