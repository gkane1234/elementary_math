"""Create type stubs for manually wired graphing catalog entries."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STUB = '''"""Graphing catalog type: {tid}."""

from question_engine.types._from_generator import register_from_catalog

register_from_catalog("{tid}")
'''

WIRED = [
    ("pa_graphing_systems_of_equations", "pre_algebra", "linear_equations_and_inequalities"),
    ("a2_linear_relations_and_functions_graphing_linear_equations", "algebra_2", "linear_relations_and_functions"),
    ("a2_linear_relations_and_functions_graphing_linear_inequalities", "algebra_2", "linear_relations_and_functions"),
    ("a2_systems_of_equations_and_inequalities_solving_systems_by_graphing_2_variables", "algebra_2", "systems_of_equations_and_inequalities"),
    ("a2_quadratic_functions_and_inequalities_graphing_quadratic_inequalities", "algebra_2", "quadratic_functions_and_inequalities"),
    ("a2_radical_functions_and_rational_exponents_graphing_radical_equations", "algebra_2", "radical_functions_and_rational_exponents"),
    ("geo_parallel_graphing_linear_equations", "geometry", "parallel_lines_and_the_coordinate_plane"),
    ("g6_shapes_and_perimeter_on_the_coordinate_plane", "grade_6", "coordinate_plane"),
    ("g6_distances_on_the_coordinate_plane", "grade_6", "coordinate_plane"),
    ("g6_solutions_to_inequalities", "grade_6", "inequalities"),
    ("pc_polynomial_graphs_real_zeros_and_end_behavior", "precalculus", "power_polynomial_and_rational_functions"),
    ("pc_graphs_of_rational_functions", "precalculus", "power_polynomial_and_rational_functions"),
]

for tid, course, chapter in WIRED:
    path = ROOT / "question_engine" / "types" / course / chapter / f"{tid}.py"
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(STUB.format(tid=tid), encoding="utf-8")
        print(f"created {tid}")
