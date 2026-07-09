"""Build and apply curriculum topic -> question type_id mapping."""
from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
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

COURSE_PREFIX = {
    "grade_6_math": "Grade 6",
    "pre_algebra": "Pre-Algebra",
    "algebra_1": "Algebra 1",
    "geometry": "Geometry",
    "algebra_2": "Algebra 2",
    "precalculus": "Precalculus",
    "calculus": "Calculus",
}

# Curriculum topic id -> canonical type_id when ids differ
CURRICULUM_ID_OVERRIDES: dict[str, str] = {
    "g6_distributive_property_numeric": "distributive_property",
    "g6_distributive_property_algebraic": "distributive_property",
    "g6_solving_and_graphing_one_step_inequalities": "one_step_inequalities",
    "the_distributive_property": "distributive_property",
    "pa_equations_multi_step_equations": "multi_step_equations",
    "pa_multi_step_inequalities": "multi_step_inequalities",
    "pa_systems_substitution": "systems_substitution",
    "adding_and_subtracting_rational_numbers": "rational_add_subtract",
    "multiplying_rational_numbers": "rational_multiply",
    "dividing_rational_numbers": "rational_divide",
    "evaluating_and_graphing_functions": "evaluating_graphing_functions",
    "solving_by_elimination": "systems_elimination",
    "solving_by_substitution": "systems_substitution",
    "writing_scientific_notation": "scientific_notation_write",
    "operations_and_scientific_notation": "scientific_notation_operations",
    "addition_subtraction_and_scientific_notation": "scientific_notation_add_subtract",
    "discrete_exponential_growth_and_decay_word_problems": "exponential_growth_decay",
    "polynomials_naming": "polynomial_naming",
    "polynomials_adding_and_subtracting": "polynomial_add_subtract",
    "polynomials_dividing": "polynomial_long_division",
    "polynomials_multiplying": "polynomial_multiply",
    "polynomials_multiplying_special_cases": "polynomial_multiply_special",
    "common_factor_only": "polynomial_factoring_common_factor",
    "quadratic_expressions": "quadratic_factoring",
    "factoring_special_cases": "polynomial_factoring_special_cases",
    "factoring_by_grouping": "polynomial_factoring_grouping",
    "solving_equations_by_taking_square_roots": "quadratic_square_roots",
    "solving_equations_by_factoring": "quadratic_factoring_equations",
    "solving_equations_with_the_quadratic_formula": "quadratic_formula",
    "understanding_the_discriminant": "quadratic_discriminant",
    "completing_the_square_by_finding_the_constant": "quadratic_completing_square_constant",
    "solving_equations_by_completing_the_square": "quadratic_completing_square_solve",
    "simplifying_single_radicals": "radical_simplification",
    "the_distance_formula": "radical_distance_formula",
    "the_midpoint_formula": "radical_midpoint_formula",
    "radical_expressions_adding_and_subtracting": "radical_add_subtract",
    "radical_expressions_multiplying": "radical_multiply",
    "radical_expressions_dividing": "radical_divide",
    "radical_expressions_equations": "radical_equations",
    "simplifying_and_excluded_values": "rational_expression_simplification",
    "rational_expressions_multiplying_and_dividing": "rational_expression_multiply_divide",
    "rational_expressions_adding_and_subtracting": "rational_simplification",
    "a2_equations_and_inequalities_multi_step_equations": "multi_step_equations",
    "a2_equations_and_inequalities_absolute_value_equations": "absolute_value_equations",
    "a2_equations_and_inequalities_multi_step_inequalities": "multi_step_inequalities",
    "a2_equations_and_inequalities_compound_inequalities": "compound_inequalities",
    "a2_equations_and_inequalities_absolute_value_inequalities": "absolute_value_inequalities",
    "a2_relations_and_introduction_to_functions_discrete_relations": "discrete_relations",
    "a2_relations_and_introduction_to_functions_continuous_relations": "continuous_relations",
    "a2_relations_and_introduction_to_functions_evaluating_and_graphing_functions": "evaluating_graphing_functions",
    "a2_linear_relations_and_functions_writing_linear_equations": "writing_linear_equations",
    "a2_direct_and_inverse_variation_direct_and_inverse_variation": "direct_inverse_variation",
    "a2_systems_of_equations_and_inequalities_solving_systems_by_elimination_2_variables": "systems_elimination",
    "a2_systems_of_equations_and_inequalities_solving_systems_by_substitution_2_variables": "systems_substitution",
    "a2_quadratic_functions_and_inequalities_factoring_quadratic_expressions": "quadratic_factoring",
    "a2_quadratic_functions_and_inequalities_solving_equations_by_taking_square_roots": "quadratic_square_roots",
    "a2_quadratic_functions_and_inequalities_solving_equations_by_factoring": "quadratic_factoring_equations",
    "a2_quadratic_functions_and_inequalities_solving_equations_by_completing_the_square": "quadratic_completing_square_solve",
    "a2_quadratic_functions_and_inequalities_solving_equations_with_the_quadratic_formula": "quadratic_formula",
    "a2_polynomial_functions_naming": "polynomial_naming",
    "a2_polynomial_functions_adding_and_subtracting": "polynomial_add_subtract",
    "a2_polynomial_functions_multiplying": "polynomial_multiply",
    "a2_polynomial_functions_multiplying_special_cases": "polynomial_multiply_special",
    "a2_polynomial_functions_dividing": "polynomial_long_division",
    "a2_polynomial_functions_factoring_by_grouping": "polynomial_factoring_grouping",
    "a2_radical_functions_and_rational_exponents_simplifying_radicals": "radical_simplification",
    "a2_radical_functions_and_rational_exponents_adding_and_subtracting_radical_expressions": "radical_add_subtract",
    "a2_radical_functions_and_rational_exponents_multiplying_radical_expressions": "radical_multiply",
    "a2_radical_functions_and_rational_exponents_dividing_radical_expressions": "radical_divide",
    "a2_radical_functions_and_rational_exponents_radical_equations": "radical_equations",
    "a2_rational_expressions_simplifying": "rational_expression_simplification",
    "a2_rational_expressions_multiplying_and_dividing": "rational_expression_multiply_divide",
    "a2_rational_expressions_adding_and_subtracting": "rational_simplification",
    "a2_exponential_and_logarithmic_expressions_discrete_exponential_growth_and_decay_word_problems": "exponential_growth_decay",
    "geo_review_multi_step_equations": "multi_step_equations",
    "geo_parallel_writing_linear_equations": "writing_linear_equations",
}


def has_real_generator(type_id: str) -> bool:
    if type_id in HAND_WRITTEN:
        return True
    entry = next((e for e in TYPE_CATALOG if e.id == type_id), None)
    return entry is not None and entry.generator != "scaffold"


def real_type_ids() -> set[str]:
    return {tid for tid in QUESTION_TYPES if has_real_generator(tid)}


def parse_curriculum_leaves(src: str) -> list[dict]:
    leaves: list[dict] = []
    course: str | None = None
    course_re = re.compile(
        r'^\s*id:\s*"(grade_6_math|pre_algebra|algebra_1|geometry|algebra_2|precalculus|calculus)"',
        re.MULTILINE,
    )
    topic_start_re = re.compile(r'\{\s*id:\s*"([^"]+)",\s*name:\s*"([^"]+)"')

    for block_m in topic_start_re.finditer(src):
        course_slice = src[: block_m.start()]
        course_matches = course_re.findall(course_slice)
        if course_matches:
            course = course_matches[-1]

        tid, tname = block_m.group(1), block_m.group(2)
        after = src[block_m.end() : block_m.end() + 300]
        if re.match(r"\s*,\s*topics:\s*\[", after):
            continue
        if not course:
            continue
        leaves.append({"course": course, "path": [course, tname], "id": tid, "name": tname})

    return leaves


def build_course_name_index() -> dict[tuple[str, str], list[str]]:
    """Map (course_prefix, name) -> list of catalog type ids with real generators."""
    index: dict[tuple[str, str], list[str]] = defaultdict(list)
    for entry in TYPE_CATALOG:
        if not has_real_generator(entry.id):
            continue
        prefix = entry.category.split(" — ")[0]
        index[(prefix, entry.name.lower().strip())].append(entry.id)
    return index


def resolve_type_id(
    leaf: dict,
    real_types: set[str],
    by_course_name: dict[tuple[str, str], list[str]],
) -> str | None:
    tid = leaf["id"]

    if tid in CURRICULUM_ID_OVERRIDES:
        candidate = CURRICULUM_ID_OVERRIDES[tid]
        if candidate in real_types:
            return candidate

    if tid in real_types:
        return tid

    course_prefix = COURSE_PREFIX.get(leaf["course"], "")
    name_key = leaf["name"].lower().strip()
    matches = by_course_name.get((course_prefix, name_key), [])
    if len(matches) == 1:
        return matches[0]

    return None


def build_mapping() -> dict[str, str]:
    real_types = real_type_ids()
    leaves = parse_curriculum_leaves((ROOT / "lib" / "curriculum.ts").read_text(encoding="utf-8"))
    by_course_name = build_course_name_index()
    mapping: dict[str, str] = {}
    for leaf in leaves:
        type_id = resolve_type_id(leaf, real_types, by_course_name)
        if type_id:
            mapping[leaf["id"]] = type_id
    return mapping


def apply_to_curriculum(mapping: dict[str, str]) -> None:
    path = ROOT / "lib" / "curriculum.ts"
    src = path.read_text(encoding="utf-8")
    src = re.sub(r",\s*type_id:\s*\"[^\"]+\"", "", src)
    src = re.sub(r",\s*type_id:\s*null", "", src)

    topic_start_re = re.compile(r'\{\s*id:\s*"([^"]+)",\s*name:\s*"([^"]+)"')
    replacements: list[tuple[int, int, str]] = []

    for match in topic_start_re.finditer(src):
        tid = match.group(1)
        after = src[match.end() : match.end() + 300]
        if re.match(r"\s*,\s*topics:\s*\[", after):
            continue
        if tid not in mapping:
            continue

        close = src.find("}", match.end())
        if close == -1:
            continue
        block = src[match.start() : close + 1]
        type_id = mapping[tid]
        if block.rstrip().endswith("}"):
            new_block = block[:-1].rstrip().rstrip(",") + f', type_id: "{type_id}" }}'
        else:
            continue
        replacements.append((match.start(), close + 1, new_block))

    for start, end, new_block in reversed(replacements):
        src = src[:start] + new_block + src[end:]

    path.write_text(src, encoding="utf-8")


def verify(mapping: dict[str, str]) -> bool:
    real_types = real_type_ids()
    ok = True

    missing = sorted(real_types - set(mapping.values()))
    if missing:
        ok = False
        print("Real generator types without curriculum type_id:")
        for tid in missing:
            entry = next((e for e in TYPE_CATALOG if e.id == tid), None)
            print(f"  - {tid} ({entry.name if entry else 'hand-written'})")

    invalid = sorted({v for v in mapping.values() if v not in QUESTION_TYPES})
    if invalid:
        ok = False
        print("Invalid type_id values:", invalid)

    scaffold_linked = sorted(
        tid for tid, type_id in mapping.items() if not has_real_generator(type_id)
    )
    if scaffold_linked:
        ok = False
        print("Curriculum topics linked to scaffold-only types:", scaffold_linked)

    print(f"\nMapped topics: {len(mapping)}")
    print(f"Unique type_ids: {len(set(mapping.values()))}")
    print(f"Real generator types: {len(real_types)}")
    return ok


def main() -> None:
    mapping = build_mapping()
    out = ROOT / "scripts" / "_curriculum_type_mapping.json"
    out.write_text(json.dumps(mapping, indent=2, sort_keys=True), encoding="utf-8")
    print(f"Built mapping with {len(mapping)} entries -> {out}")

    if verify(mapping):
        apply_to_curriculum(mapping)
        print("Applied type_id to lib/curriculum.ts")
    else:
        print("Verification failed — not applying until fixed")
        sys.exit(1)


if __name__ == "__main__":
    main()
