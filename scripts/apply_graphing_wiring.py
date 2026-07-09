"""Wire graphing-heavy scaffold catalog types to graphing generators."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# (catalog_id, generator, course, chapter_folder)
GRAPHING_WIRING = [
    # Algebra 1 — canonical graphing types
    ("graphing_single_variable_inequalities", "graph_single_variable_inequality", "algebra_1", "inequalities"),
    ("graphing_linear_equations", "graph_linear_equation", "algebra_1", "linear_equations_and_inequalities"),
    ("graphing_linear_inequalities", "graph_linear_inequality", "algebra_1", "linear_equations_and_inequalities"),
    ("graphing_absolute_value_equations", "graph_absolute_value", "algebra_1", "linear_equations_and_inequalities"),
    ("systems_graphing", "graph_system", "algebra_1", "systems_of_equations_and_inequalities"),
    ("graphing_systems_of_inequalities", "graph_system_inequalities", "algebra_1", "systems_of_equations_and_inequalities"),
    ("graphing_exponential_functions", "graph_exponential", "algebra_1", "exponents"),
    ("graphing_quadratic_functions", "graph_quadratic", "algebra_1", "quadratic_functions"),
    ("graphing_quadratic_inequalities", "graph_quadratic_inequality", "algebra_1", "quadratic_functions"),
    # Grade 6
    ("g6_numbers_on_a_number_line", "number_line_plot", "grade_6", "negative_numbers_and_absolute_value"),
    ("g6_points_on_the_coordinate_plane", "plotting_points", "grade_6", "coordinate_plane"),
    ("g6_writing_and_graphing_inequalities", "graph_single_variable_inequality", "grade_6", "inequalities"),
    ("g6_solutions_to_inequalities", "graph_single_variable_inequality", "grade_6", "inequalities"),
    # Pre-Algebra
    ("pa_graphing_systems_of_equations", "graph_system", "pre_algebra", "linear_equations_and_inequalities"),
    # Algebra 2 — dedup to graphing generators
    ("a2_linear_relations_and_functions_graphing_linear_equations", "graph_linear_equation", "algebra_2", "linear_relations_and_functions"),
    ("a2_linear_relations_and_functions_graphing_absolute_value_equations", "graph_absolute_value", "algebra_2", "linear_relations_and_functions"),
    ("a2_linear_relations_and_functions_graphing_linear_inequalities", "graph_linear_inequality", "algebra_2", "linear_relations_and_functions"),
    ("a2_systems_of_equations_and_inequalities_graphing_systems_of_linear_inequalities", "graph_system_inequalities", "algebra_2", "systems_of_equations_and_inequalities"),
    ("a2_systems_of_equations_and_inequalities_solving_systems_by_graphing_2_variables", "graph_system", "algebra_2", "systems_of_equations_and_inequalities"),
    ("a2_quadratic_functions_and_inequalities_graphing_quadratic_functions", "graph_quadratic", "algebra_2", "quadratic_functions_and_inequalities"),
    ("a2_quadratic_functions_and_inequalities_graphing_quadratic_inequalities", "graph_quadratic_inequality", "algebra_2", "quadratic_functions_and_inequalities"),
    ("a2_exponential_and_logarithmic_expressions_graphing_exponential_functions", "graph_exponential", "algebra_2", "exponential_and_logarithmic_expressions"),
    ("a2_polynomial_functions_graphing", "graph_quadratic", "algebra_2", "polynomial_functions"),
    # Geometry
    ("geo_parallel_graphing_linear_equations", "graph_linear_equation", "geometry", "parallel_lines_and_the_coordinate_plane"),
    # Precalculus (non-trig graphing)
    ("pc_graphing_exponential_functions", "graph_exponential", "precalculus", "exponential_and_logarithmic_expressions"),
    ("pc_parabolas_graphing_and_properties", "graph_quadratic", "precalculus", "conic_sections"),
    ("pc_polynomial_graphs_real_zeros_and_end_behavior", "graph_quadratic", "precalculus", "power_polynomial_and_rational_functions"),
    ("pc_transformations_of_graphs", "graph_quadratic", "precalculus", "functions"),
]

CATALOG_FILES = {
    "algebra_1": ROOT / "question_engine" / "catalogs" / "algebra_1.py",
    "grade_6": ROOT / "question_engine" / "catalogs" / "grade_6.py",
    "pre_algebra": ROOT / "question_engine" / "catalogs" / "pre_algebra.py",
    "algebra_2": ROOT / "question_engine" / "catalogs" / "algebra_2.py",
    "geometry": ROOT / "question_engine" / "catalogs" / "geometry.py",
    "precalculus": ROOT / "question_engine" / "catalogs" / "precalculus.py",
}

STUB_TEMPLATE = '''"""Graphing catalog type: {type_id}."""

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

    # algebra_1 entry(...) style
    pattern_entry = rf'(entry\(\s*\n\s*"{re.escape(type_id)}",[\s\S]*?"[^"]+",\s*\n\s*"[^"]+",)\s*\n(\s*instruction)'
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
    wired = []
    for type_id, generator, course, chapter in GRAPHING_WIRING:
        catalog_path = CATALOG_FILES[course]
        if wire_catalog(catalog_path, type_id, generator):
            create_stub(course, chapter, type_id)
            wired.append((type_id, generator))
            print(f"WIRED {type_id} -> {generator}")
    print(f"\nTotal wired: {len(wired)}")


if __name__ == "__main__":
    main()
