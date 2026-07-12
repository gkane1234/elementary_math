"""Rebuild question_engine/catalogs/algebra_1.py from canonical type metadata."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
QE = ROOT / "question_engine"

# Canonical catalog metadata (home course category, generator, instructions).
# Reconstructed from the pre-refactor _ALGEBRA_CATALOG in catalog.py.
ENTRIES: list[dict] = [
    {"id": "verbal_expressions", "name": "Verbal expressions", "category": "Pre-Algebra — Beginning Algebra", "instruction_latex": "\\text{Write as an algebraic expression.}", "instruction_text": "Write as an algebraic expression."},
    {"id": "order_of_operations", "name": "Order of operations", "category": "Pre-Algebra — Beginning Algebra", "instruction_latex": "\\text{Evaluate.}", "instruction_text": "Evaluate."},
    {"id": "sets_of_numbers", "name": "Sets of numbers", "category": "Algebra 1 — Beginning Algebra", "instruction_latex": "\\text{Classify the number.}", "instruction_text": "Classify the number."},
    {"id": "rational_add_subtract", "name": "Adding and subtracting rational numbers", "category": "Algebra 1 — Beginning Algebra", "generator": "rational_add_subtract", "instruction_latex": "\\text{Evaluate.}", "instruction_text": "Evaluate."},
    {"id": "rational_multiply", "name": "Multiplying rational numbers", "category": "Algebra 1 — Beginning Algebra", "generator": "rational_multiply", "instruction_latex": "\\text{Evaluate.}", "instruction_text": "Evaluate."},
    {"id": "rational_divide", "name": "Dividing rational numbers", "category": "Algebra 1 — Beginning Algebra", "generator": "rational_divide", "instruction_latex": "\\text{Evaluate.}", "instruction_text": "Evaluate."},
    {"id": "distributive_property", "name": "The Distributive Property", "category": "Pre-Algebra — Beginning Algebra", "generator": "distributive_property", "instruction_latex": "\\text{Evaluate.}", "instruction_text": "Evaluate."},
    {"id": "one_step_equations", "name": "One-step equations", "category": "Pre-Algebra — Equations", "generator": "one_step_equations", "instruction_latex": "\\text{Solve for } x.", "instruction_text": "Solve for x."},
    {"id": "two_step_equations", "name": "Two-step equations", "category": "Pre-Algebra — Equations", "generator": "two_step_equations", "instruction_latex": "\\text{Solve for } x.", "instruction_text": "Solve for x."},
    {"id": "multi_step_equations", "name": "Multi-step equations", "category": "Algebra 1 — Equations", "generator": "multi_step_equations", "instruction_latex": "\\text{Solve for } x.", "instruction_text": "Solve for x."},
    {"id": "absolute_value_equations", "name": "Absolute value equations", "category": "Algebra 1 — Equations", "generator": "absolute_value_equations", "instruction_latex": "\\text{Solve for } x.", "instruction_text": "Solve for x."},
    {"id": "mixture_word_problems", "name": "Mixture word problems", "category": "Algebra 1 — Equations", "instruction_latex": "\\text{Solve the problem.}", "instruction_text": "Solve the problem.", "count_default": 5},
    {"id": "distance_rate_time_word_problems", "name": "Distance, rate, time word problems", "category": "Algebra 1 — Equations", "instruction_latex": "\\text{Solve the problem.}", "instruction_text": "Solve the problem.", "count_default": 5},
    {"id": "work_word_problems", "name": "Work word problems", "category": "Algebra 1 — Equations", "instruction_latex": "\\text{Solve the problem.}", "instruction_text": "Solve the problem.", "count_default": 5},
    {"id": "literal_equations", "name": "Literal equations", "category": "Algebra 1 — Equations", "instruction_latex": "\\text{Solve for the indicated variable.}", "instruction_text": "Solve for the indicated variable."},
    {"id": "graphing_single_variable_inequalities", "name": "Graphing single-variable inequalities", "category": "Pre-Algebra — Inequalities", "instruction_latex": "\\text{Graph the solution.}", "instruction_text": "Graph the solution."},
    {"id": "one_step_inequalities", "name": "One-step inequalities", "category": "Pre-Algebra — Inequalities", "generator": "one_step_inequalities", "instruction_latex": "\\text{Solve for } x.", "instruction_text": "Solve for x."},
    {"id": "two_step_inequalities", "name": "Two-step inequalities", "category": "Pre-Algebra — Inequalities", "generator": "two_step_inequalities", "instruction_latex": "\\text{Solve for } x.", "instruction_text": "Solve for x."},
    {"id": "multi_step_inequalities", "name": "Multi-step inequalities", "category": "Algebra 1 — Inequalities", "generator": "multi_step_inequalities", "instruction_latex": "\\text{Solve for } x.", "instruction_text": "Solve for x."},
    {"id": "compound_inequalities", "name": "Compound inequalities", "category": "Algebra 1 — Inequalities", "generator": "compound_inequalities", "instruction_latex": "\\text{Solve for } x.", "instruction_text": "Solve for x."},
    {"id": "absolute_value_inequalities", "name": "Absolute value inequalities", "category": "Algebra 1 — Inequalities", "generator": "absolute_value_inequalities", "instruction_latex": "\\text{Solve for } x.", "instruction_text": "Solve for x."},
    {"id": "solving_proportions", "name": "Solving proportions", "category": "Pre-Algebra — Proportions and Similarity", "generator": "solving_proportions", "instruction_latex": "\\text{Solve for } x.", "instruction_text": "Solve for x."},
    {"id": "percents", "name": "Percents", "category": "Pre-Algebra — Percents", "generator": "percents", "instruction_latex": "\\text{Find the value.}", "instruction_text": "Find the value."},
    {"id": "percent_of_change", "name": "Percent of change", "category": "Pre-Algebra — Percents", "generator": "percent_of_change", "instruction_latex": "\\text{Find the percent of change.}", "instruction_text": "Find the percent of change."},
    {"id": "discrete_relations", "name": "Discrete relations", "category": "Algebra 1 — Relations and Introduction to Functions", "generator": "discrete_relations", "instruction_latex": "\\text{Evaluate the relation.}", "instruction_text": "Evaluate the relation."},
    {"id": "continuous_relations", "name": "Continuous relations", "category": "Algebra 1 — Relations and Introduction to Functions", "generator": "continuous_relations", "instruction_latex": "\\text{Evaluate the relation.}", "instruction_text": "Evaluate the relation."},
    {"id": "evaluating_graphing_functions", "name": "Evaluating and graphing functions", "category": "Algebra 1 — Relations and Introduction to Functions", "generator": "evaluating_graphing_functions", "instruction_latex": "\\text{Evaluate.}", "instruction_text": "Evaluate."},
    {"id": "slope", "name": "Slope", "category": "Pre-Algebra — Linear Equations and Inequalities", "instruction_latex": "\\text{Find the slope.}", "instruction_text": "Find the slope."},
    {"id": "more_on_slope", "name": "More on slope", "category": "Algebra 1 — Linear Equations and Inequalities", "instruction_latex": "\\text{Find the slope.}", "instruction_text": "Find the slope."},
    {"id": "graphing_linear_equations", "name": "Graphing linear equations", "category": "Pre-Algebra — Linear Equations and Inequalities", "instruction_latex": "\\text{Graph the equation.}", "instruction_text": "Graph the equation."},
    {"id": "writing_linear_equations", "name": "Writing linear equations", "category": "Pre-Algebra — Linear Equations and Inequalities", "generator": "writing_linear_equations", "instruction_latex": "\\text{Write an equation of the line.}", "instruction_text": "Write an equation of the line."},
    {"id": "graphing_linear_inequalities", "name": "Graphing linear inequalities", "category": "Pre-Algebra — Linear Equations and Inequalities", "instruction_latex": "\\text{Graph the inequality.}", "instruction_text": "Graph the inequality."},
    {"id": "graphing_absolute_value_equations", "name": "Graphing absolute value equations", "category": "Algebra 1 — Linear Equations and Inequalities", "instruction_latex": "\\text{Graph the equation.}", "instruction_text": "Graph the equation."},
    {"id": "direct_inverse_variation", "name": "Direct and inverse variation", "category": "Algebra 1 — Direct and inverse variation", "generator": "direct_inverse_variation", "instruction_latex": "\\text{Write the variation equation.}", "instruction_text": "Write the variation equation."},
    {"id": "systems_graphing", "name": "Solving by graphing", "category": "Algebra 1 — Systems of Equations and Inequalities", "instruction_latex": "\\text{Solve the system.}", "instruction_text": "Solve the system."},
    {"id": "systems_elimination", "name": "Solving by elimination", "category": "Algebra 1 — Systems of Equations and Inequalities", "generator": "systems_elimination", "instruction_latex": "\\text{Solve the system.}", "instruction_text": "Solve the system."},
    {"id": "systems_substitution", "name": "Solving by substitution", "category": "Algebra 1 — Systems of Equations and Inequalities", "generator": "systems_substitution", "instruction_latex": "\\text{Solve the system.}", "instruction_text": "Solve the system."},
    {"id": "graphing_systems_of_inequalities", "name": "Graphing systems of inequalities", "category": "Algebra 1 — Systems of Equations and Inequalities", "instruction_latex": "\\text{Graph the system.}", "instruction_text": "Graph the system."},
    {"id": "systems_word_problems", "name": "Word problems", "category": "Algebra 1 — Systems of Equations and Inequalities", "instruction_latex": "\\text{Solve the problem.}", "instruction_text": "Solve the problem.", "count_default": 5},
    {"id": "properties_of_exponents", "name": "Properties of exponents", "category": "Pre-Algebra — Factors and Exponents", "instruction_latex": "\\text{Simplify.}", "instruction_text": "Simplify."},
    {"id": "graphing_exponential_functions", "name": "Graphing exponential functions", "category": "Algebra 1 — Exponents", "instruction_latex": "\\text{Graph the function.}", "instruction_text": "Graph the function."},
    {"id": "scientific_notation_write", "name": "Writing scientific notation", "category": "Pre-Algebra — Factors and Exponents", "generator": "scientific_notation_write", "instruction_latex": "\\text{Write in scientific notation.}", "instruction_text": "Write in scientific notation."},
    {"id": "scientific_notation_operations", "name": "Operations and scientific notation", "category": "Pre-Algebra — Factors and Exponents", "generator": "scientific_notation_operations", "instruction_latex": "\\text{Evaluate. Write in scientific notation.}", "instruction_text": "Evaluate. Write in scientific notation."},
    {"id": "scientific_notation_add_subtract", "name": "Addition/Subtraction and scientific notation", "category": "Algebra 1 — Exponents", "generator": "scientific_notation_add_subtract", "instruction_latex": "\\text{Evaluate. Write in scientific notation.}", "instruction_text": "Evaluate. Write in scientific notation."},
    {"id": "exponential_growth_decay", "name": "Discrete exponential growth and decay word problems", "category": "Algebra 1 — Exponents", "generator": "exponential_growth_decay", "instruction_latex": "\\text{Solve the problem.}", "instruction_text": "Solve the problem.", "count_default": 5},
    {"id": "polynomial_naming", "name": "Naming", "category": "Algebra 1 — Polynomials", "generator": "polynomial_naming", "instruction_latex": "\\text{Name the polynomial.}", "instruction_text": "Name the polynomial."},
    {"id": "polynomial_add_subtract", "name": "Adding and subtracting", "category": "Algebra 1 — Polynomials", "generator": "polynomial_add_subtract", "instruction_latex": "\\text{Simplify.}", "instruction_text": "Simplify."},
    {"id": "polynomial_multiply", "name": "Multiplying", "category": "Algebra 1 — Polynomials", "generator": "polynomial_multiply", "instruction_latex": "\\text{Multiply.}", "instruction_text": "Multiply."},
    {"id": "polynomial_multiply_special", "name": "Multiplying special cases", "category": "Algebra 1 — Polynomials", "generator": "polynomial_multiply_special", "instruction_latex": "\\text{Multiply.}", "instruction_text": "Multiply."},
    {"id": "polynomial_factoring_common_factor", "name": "Common factor only", "category": "Algebra 1 — Polynomials", "subcategory": "Factoring", "generator": "polynomial_factoring_common_factor", "instruction_latex": "\\text{Factor completely.}", "instruction_text": "Factor completely."},
    {"id": "polynomial_factoring_special_cases", "name": "Special cases", "category": "Algebra 1 — Polynomials", "subcategory": "Factoring", "generator": "polynomial_factoring_special_cases", "instruction_latex": "\\text{Factor completely.}", "instruction_text": "Factor completely."},
    {"id": "polynomial_factoring_grouping", "name": "By grouping", "category": "Algebra 1 — Polynomials", "subcategory": "Factoring", "generator": "polynomial_factoring_grouping", "instruction_latex": "\\text{Factor completely.}", "instruction_text": "Factor completely."},
    {"id": "graphing_quadratic_functions", "name": "Graphing", "category": "Algebra 1 — Quadratic Functions", "instruction_latex": "\\text{Graph the function.}", "instruction_text": "Graph the function."},
    {"id": "graphing_quadratic_inequalities", "name": "Graphing quadratic inequalities", "category": "Algebra 1 — Quadratic Functions", "instruction_latex": "\\text{Graph the inequality.}", "instruction_text": "Graph the inequality."},
    {"id": "quadratic_square_roots", "name": "Solving equations by taking square roots", "category": "Algebra 1 — Quadratic Functions", "generator": "quadratic_square_roots", "instruction_latex": "\\text{Solve for } x.", "instruction_text": "Solve for x."},
    {"id": "quadratic_factoring_equations", "name": "Solving equations by factoring", "category": "Algebra 1 — Quadratic Functions", "generator": "quadratic_factoring_equations", "instruction_latex": "\\text{Solve for } x.", "instruction_text": "Solve for x."},
    {"id": "quadratic_formula", "name": "Solving equations with the Quadratic Formula", "category": "Algebra 1 — Quadratic Functions", "generator": "quadratic_formula", "instruction_latex": "\\text{Solve for } x.", "instruction_text": "Solve for x."},
    {"id": "quadratic_discriminant", "name": "Understanding the discriminant", "category": "Algebra 1 — Quadratic Functions", "generator": "quadratic_discriminant", "instruction_latex": "\\text{Find the discriminant and describe the roots.}", "instruction_text": "Find the discriminant and describe the roots."},
    {"id": "quadratic_completing_square_constant", "name": "Completing the square by finding the constant", "category": "Algebra 1 — Quadratic Functions", "generator": "quadratic_completing_square_constant", "instruction_latex": "\\text{Find the value of } c.", "instruction_text": "Find the value of c."},
    {"id": "quadratic_completing_square_solve", "name": "Solving equations by completing the square", "category": "Algebra 1 — Quadratic Functions", "generator": "quadratic_completing_square_solve", "instruction_latex": "\\text{Solve for } x.", "instruction_text": "Solve for x."},
    {"id": "radical_distance_formula", "name": "The Distance Formula", "category": "Pre-Algebra — Right Triangles", "generator": "radical_distance_formula", "instruction_latex": "\\text{Find the distance.}", "instruction_text": "Find the distance."},
    {"id": "radical_midpoint_formula", "name": "The Midpoint Formula", "category": "Pre-Algebra — Linear Equations and Inequalities", "generator": "radical_midpoint_formula", "instruction_latex": "\\text{Find the midpoint.}", "instruction_text": "Find the midpoint."},
    {"id": "radical_add_subtract", "name": "Adding and subtracting", "category": "Algebra 1 — Radical Expressions", "generator": "radical_add_subtract", "instruction_latex": "\\text{Simplify.}", "instruction_text": "Simplify."},
    {"id": "radical_multiply", "name": "Multiplying", "category": "Algebra 1 — Radical Expressions", "generator": "radical_multiply", "instruction_latex": "\\text{Simplify.}", "instruction_text": "Simplify."},
    {"id": "radical_divide", "name": "Dividing", "category": "Algebra 1 — Radical Expressions", "generator": "radical_divide", "instruction_latex": "\\text{Simplify.}", "instruction_text": "Simplify."},
    {"id": "radical_equations", "name": "Equations", "category": "Algebra 1 — Radical Expressions", "generator": "radical_equations", "instruction_latex": "\\text{Solve for } x.", "instruction_text": "Solve for x."},
    {"id": "rational_expression_multiply_divide", "name": "Multiplying and dividing", "category": "Algebra 1 — Rational Expressions", "generator": "rational_expression_multiply_divide", "instruction_latex": "\\text{Simplify.}", "instruction_text": "Simplify."},
    {"id": "rational_expressions_equations", "name": "Equations", "category": "Algebra 1 — Rational Expressions", "generator": "rational_equations", "instruction_latex": "\\text{Solve for } x.", "instruction_text": "Solve for x."},
    {"id": "finding_sine_cosine_tangent", "name": "Finding sine, cosine, tangent", "category": "Algebra 1 — Beginning Trigonometry", "instruction_latex": "\\text{Find the trigonometric ratio.}", "instruction_text": "Find the trigonometric ratio."},
    {"id": "finding_angles", "name": "Finding angles", "category": "Algebra 1 — Beginning Trigonometry", "instruction_latex": "\\text{Find the angle measure.}", "instruction_text": "Find the angle measure."},
    {"id": "find_missing_sides_of_triangles", "name": "Find missing sides of triangles", "category": "Algebra 1 — Beginning Trigonometry", "instruction_latex": "\\text{Find the missing side.}", "instruction_text": "Find the missing side."},
    {"id": "visualizing_data", "name": "Visualizing data", "category": "Pre-Algebra — Statistics", "instruction_latex": "\\text{Interpret the display.}", "instruction_text": "Interpret the display."},
    {"id": "center_and_spread", "name": "Center and spread", "category": "Pre-Algebra — Statistics", "instruction_latex": "\\text{Find the measure.}", "instruction_text": "Find the measure."},
    {"id": "scatter_plots", "name": "Scatter plots", "category": "Pre-Algebra — Statistics", "instruction_latex": "\\text{Interpret the scatter plot.}", "instruction_text": "Interpret the scatter plot."},
    {"id": "using_statistical_models", "name": "Using statistical models", "category": "Pre-Algebra — Statistics", "instruction_latex": "\\text{Use the model.}", "instruction_text": "Use the model."},
]


def emit_entry(entry: dict) -> str:
    lines = [
        "    entry(",
        f'        "{entry["id"]}",',
        f'        "{entry["name"]}",',
        f'        "{entry["category"]}",',
    ]
    if entry.get("subcategory"):
        lines.append(f'        subcategory="{entry["subcategory"]}",')
    if entry.get("generator", "scaffold") != "scaffold":
        lines.append(f'        generator="{entry["generator"]}",')
    if entry.get("instruction_latex"):
        lines.append(f'        instruction_latex="{entry["instruction_latex"]}",')
    if entry.get("instruction_text"):
        lines.append(f'        instruction_text="{entry["instruction_text"]}",')
    if entry.get("count_default", 10) != 10:
        lines.append(f'        count_default={entry["count_default"]},')
    lines.append("    ),")
    return "\n".join(lines)


def main() -> None:
    categories: list[str] = []
    for entry in ENTRIES:
        if entry["category"] not in categories:
            categories.append(entry["category"])

    body = "\n".join(emit_entry(entry) for entry in ENTRIES)
    content = f'''from .base import entry

COURSE_ID = "algebra_1"

CATEGORY_ORDER: tuple[str, ...] = (
{chr(10).join(f'    "{c}",' for c in categories)}
)

CATALOG: tuple = (
{body}
)
'''
    out = QE / "catalogs" / "algebra_1.py"
    out.parent.mkdir(exist_ok=True)
    out.write_text(content, encoding="utf-8")
    print(f"Wrote {out} with {len(ENTRIES)} entries")


if __name__ == "__main__":
    main()
