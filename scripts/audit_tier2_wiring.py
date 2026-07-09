"""Audit scaffold catalog entries that can wire to existing generators."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from question_engine.catalogs.algebra_1 import CATALOG as ALGEBRA1_CATALOG
from question_engine.catalogs.algebra_2 import CATALOG as ALGEBRA2_CATALOG
from question_engine.catalogs.calculus import CATALOG as CALCULUS_CATALOG
from question_engine.catalogs.geometry import CATALOG as GEOMETRY_CATALOG
from question_engine.catalogs.grade_6 import CATALOG as GRADE6_CATALOG
from question_engine.catalogs.pre_algebra import CATALOG as PREALGEBRA_CATALOG
from question_engine.catalogs.precalculus import CATALOG as PRECALC_CATALOG

TYPE_CATALOG = (
    ALGEBRA1_CATALOG
    + GRADE6_CATALOG
    + PREALGEBRA_CATALOG
    + ALGEBRA2_CATALOG
    + GEOMETRY_CATALOG
    + PRECALC_CATALOG
    + CALCULUS_CATALOG
)

# Generator keys from basic.py (avoid importing polynomial_core)
REAL_GENERATORS = {
    "rational_add_subtract", "rational_multiply", "rational_divide",
    "distributive_property", "one_step_equations", "two_step_equations",
    "multi_step_equations", "absolute_value_equations",
    "one_step_inequalities", "two_step_inequalities", "multi_step_inequalities",
    "compound_inequalities", "absolute_value_inequalities",
    "solving_proportions", "percents", "percent_of_change",
    "discrete_relations", "continuous_relations", "evaluating_graphing_functions",
    "writing_linear_equations", "direct_inverse_variation",
    "systems_elimination", "systems_substitution",
    "scientific_notation_write", "scientific_notation_operations",
    "scientific_notation_add_subtract", "exponential_growth_decay",
    "polynomial_naming", "polynomial_add_subtract", "polynomial_multiply",
    "polynomial_multiply_special", "polynomial_factoring_common_factor",
    "polynomial_factoring_special_cases", "polynomial_factoring_grouping",
    "quadratic_square_roots", "quadratic_factoring_equations", "quadratic_formula",
    "quadratic_discriminant", "quadratic_completing_square_constant",
    "quadratic_completing_square_solve", "radical_distance_formula",
    "radical_midpoint_formula", "radical_add_subtract", "radical_multiply",
    "radical_divide", "radical_equations", "rational_expression_multiply_divide",
}

src = (ROOT / "lib" / "curriculum.ts").read_text(encoding="utf-8")
topic_re = re.compile(
    r'id:\s*"([^"]+)"[^}]*?type_id:\s*"([^"]+)"',
    re.DOTALL,
)
curriculum_map = dict(topic_re.findall(src))

real_gens = REAL_GENERATORS
wired = {e.id: e.generator for e in TYPE_CATALOG if e.generator != "scaffold"}


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def main() -> None:
    id_matches: list[tuple[str, str, str]] = []
    curriculum_matches: list[tuple[str, str, str, str]] = []
    name_matches: list[tuple[str, str, str, str]] = []

    for e in TYPE_CATALOG:
        if e.generator != "scaffold":
            continue
        if e.id in real_gens:
            id_matches.append((e.id, e.id, e.category))
            continue
        canonical = curriculum_map.get(e.id)
        if canonical and canonical != e.id and canonical in wired:
            curriculum_matches.append((e.id, wired[canonical], e.category, canonical))

    gen_by_norm = {norm(g.replace("_", " ")): g for g in real_gens}
    seen = {x[0] for x in id_matches + curriculum_matches}
    for e in TYPE_CATALOG:
        if e.generator != "scaffold" or e.id in seen:
            continue
        n = norm(e.name)
        if n in gen_by_norm:
            g = gen_by_norm[n]
            if g != e.id:
                name_matches.append((e.id, g, e.category, e.name))

    # pa-specific polynomial matches
    poly_matches = []
    for e in TYPE_CATALOG:
        if e.generator != "scaffold":
            continue
        if e.id == "pa_polynomials_adding_and_subtracting":
            poly_matches.append((e.id, "polynomial_add_subtract", e.category))
        elif e.id == "pa_polynomials_multiplying":
            poly_matches.append((e.id, "polynomial_multiply", e.category))
        elif e.id == "pa_systems_substitution":
            poly_matches.append((e.id, "systems_substitution", e.category))

    print("=== ID matches (scaffold id == generator key) ===")
    for row in sorted(id_matches):
        print(row)

    print("\n=== Curriculum dedup matches ===")
    for row in sorted(curriculum_matches):
        print(row)

    print("\n=== Name matches ===")
    for row in sorted(name_matches):
        print(row)

    print("\n=== PA polynomial/system matches ===")
    for row in poly_matches:
        print(row)

    print(f"\nTotal catalog: {len(TYPE_CATALOG)}")
    print(f"Already wired: {len(wired)}")
    print(f"Scaffold: {sum(1 for e in TYPE_CATALOG if e.generator == 'scaffold')}")


if __name__ == "__main__":
    main()
