"""Collect generator family statistics for FRAMEWORK.md."""
from __future__ import annotations

import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from question_engine.base import QUESTION_TYPES
from question_engine.catalog import TYPE_CATALOG
import question_engine.types  # noqa: F401

HAND_WRITTEN = {
    "quadratic_factoring",
    "polynomial_long_division",
    "radical_simplification",
    "rational_simplification",
    "rational_expression_simplification",
}

FAMILY_RULES: list[tuple[str, str]] = [
    ("one_step_equations|two_step_equations|multi_step_equations|absolute_value_equations|literal_equations|radical_equations", "Equation solving"),
    ("inequalit", "Inequalities"),
    ("percent", "Percents"),
    ("ratio|rate|proportion", "Ratios, rates, proportions"),
    ("fraction|decimal|rational_add|rational_multiply|rational_divide", "Rational numbers & fractions"),
    ("polynomial|factoring|quadratic", "Polynomials & quadratics"),
    ("radical|square_root", "Radicals"),
    ("rational_expression|rational_simpl", "Rational expressions"),
    ("trig|sine|cosine|tangent", "Trigonometry"),
    ("logarithm|exponential", "Logs & exponentials"),
    ("matrix|determinant|cramer", "Matrices"),
    ("sequence|series|arithmetic|geometric", "Sequences & series"),
    ("area|volume|surface|perimeter|polygon|circle|triangle|quadrilateral", "Geometry measurement"),
    ("graph|slope|linear_equation|coordinate", "Graphing & linear functions"),
    ("word_problem|mixture|distance_rate|work_word", "Word problems"),
    ("scientific_notation", "Scientific notation"),
    ("stat|scatter|histogram|box_plot|mean|median", "Statistics & data"),
    ("limit|continuity|derivative|differentiat", "Calculus — limits & derivatives"),
    ("integrat|riemann|fundamental_theorem", "Calculus — integration"),
    ("conic|parabola|ellipse|hyperbola", "Conic sections"),
    ("probability|permutation|combination", "Probability & counting"),
]


def has_real_generator(type_id: str) -> bool:
    if type_id in HAND_WRITTEN:
        return True
    entry = next((e for e in TYPE_CATALOG if e.id == type_id), None)
    return entry is not None and entry.generator != "scaffold"


def classify(entry_id: str, name: str) -> str:
    blob = f"{entry_id} {name.lower()}"
    for pattern, family in FAMILY_RULES:
        if any(part in blob for part in pattern.split("|")):
            return family
    return "Other / misc"


def main() -> None:
    real = sum(1 for tid in QUESTION_TYPES if has_real_generator(tid))
    print(f"total={len(QUESTION_TYPES)} real={real} scaffold={len(QUESTION_TYPES)-real}")

    by_course = Counter(e.category.split(" — ")[0] for e in TYPE_CATALOG)
    print("by_course", dict(by_course))

    families: dict[str, list[str]] = defaultdict(list)
    for entry in TYPE_CATALOG:
        families[classify(entry.id, entry.name)].append(entry.id)

    print("families:")
    for fam, ids in sorted(families.items(), key=lambda x: -len(x[1])):
        real_count = sum(1 for i in ids if has_real_generator(i))
        print(f"  {fam}: {len(ids)} total, {real_count} implemented")


if __name__ == "__main__":
    main()
