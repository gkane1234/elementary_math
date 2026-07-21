"""Find scaffold catalog entries that can wire to existing generators."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from question_engine.catalogs.algebra_1 import CATALOG as A1
from question_engine.catalogs.algebra_2 import CATALOG as A2
from question_engine.catalogs.calculus import CATALOG as CALC
from question_engine.catalogs.geometry import CATALOG as GEO
from question_engine.catalogs.grade_6 import CATALOG as G6
from question_engine.catalogs.pre_algebra import CATALOG as PA
from question_engine.catalogs.precalculus import CATALOG as PC
from question_engine.generators import GENERATORS

CATALOG = A1 + G6 + PA + A2 + GEO + PC + CALC
src = (ROOT / "lib" / "curriculum.ts").read_text(encoding="utf-8")
topic_re = re.compile(
    r'id:\s*"([^"]+)"[^}]*?type_id:\s*"([^"]+)"',
    re.DOTALL,
)
curriculum_map = dict(topic_re.findall(src))

gen_keys = set(GENERATORS.keys()) - {"scaffold"}
wired = {e.id: e.generator for e in CATALOG if e.generator != "scaffold"}
scaffold = [e for e in CATALOG if e.generator == "scaffold"]

# Manual semantic mappings (catalog_id -> generator)
MANUAL: dict[str, str] = {
    # Hand-written types where id == generator but catalog lacks generator=
    "rational_simplification": "rational_simplification",
    "rational_expression_simplification": "rational_expression_simplification",
    "rational_expressions_equations": "radical_equations",
    # Algebra 1 missing canonical entries (curriculum uses different topic ids)
    "literal_equations": "multi_step_equations",
    "mixture_word_problems": "multi_step_equations",
    "distance_rate_time_word_problems": "multi_step_equations",
    "work_word_problems": "multi_step_equations",
    "systems_word_problems": "systems_substitution",
    # Pre-algebra word problems -> equation generators
    "pa_equations_one_step_word_problems": "one_step_equations",
    "pa_equations_two_step_word_problems": "two_step_equations",
    "pa_proportions_word_problems": "solving_proportions",
    "pa_checking_for_a_proportion": "solving_proportions",
    "pa_similar_figures": "solving_proportions",
    "pa_similar_figures_word_problems": "solving_proportions",
    "pa_systems_word_problems": "systems_substitution",
    "pa_markup_discount_and_tax": "percents",
    "pa_fractions_decimals_and_percents": "percents",
    "pa_simple_and_compound_interest": "wp_simple_and_compound_interest",
    # Grade 6 ratios
    "g6_part_part_whole_ratios": "g6_introduction_to_ratios",
    "g6_comparing_ratios": "g6_equivalent_ratios",
    "g6_comparing_rates": "g6_comparing_rates",
    "g6_converting_units": "g6_unit_rates",
    "g6_equivalent_ratio_equations": "solving_proportions",
    "g6_relating_percents_fractions_and_decimals": "percents",
    "g6_finding_percents_with_equivalent_fractions": "percents",
    "g6_solving_percent_problems_with_formulas": "percents",
    "g6_solving_percent_problems_with_diagrams": "percents",
    "g6_numeric_expressions_and_order_of_operations": "order_of_operations",
    "g6_exponents": "properties_of_exponents",
    "g6_negative_exponents": "properties_of_exponents",
    # Algebra 2 duplicates
    "a2_beginning_algebra_order_of_operations": "order_of_operations",
    "a2_equations_and_inequalities_work_word_problems": "multi_step_equations",
    "a2_equations_and_inequalities_distance_rate_time_word_problems": "multi_step_equations",
    "a2_equations_and_inequalities_mixture_word_problems": "multi_step_equations",
    "a2_systems_of_equations_and_inequalities_systems_of_equations_word_problems_2_variables": "systems_substitution",
    "a2_polynomial_functions_factoring_quadratic_form": "quadratic_factoring",
    "a2_polynomial_functions_factoring_all_techniques": "polynomial_factoring_grouping",
    "a2_radical_functions_and_rational_exponents_rational_exponent_equations": "radical_equations",
    "a2_rational_expressions_equations": "radical_equations",
    "a2_rational_expressions_complex_fractions": "rational_expression_simplification",
    "a2_radical_functions_and_rational_exponents_evaluating_rational_exponent_expressions": "properties_of_exponents",
    "a2_radical_functions_and_rational_exponents_connecting_radical_expressions_and_rational_exponents": "properties_of_exponents",
    # Precalculus / calculus if generators exist
}

# Add curriculum dedup
for e in scaffold:
    canonical = curriculum_map.get(e.id)
    if canonical and canonical in gen_keys:
        MANUAL.setdefault(e.id, canonical)
    elif canonical and canonical in wired:
        MANUAL.setdefault(e.id, wired[canonical])

# Add id==gen
for e in scaffold:
    if e.id in gen_keys:
        MANUAL.setdefault(e.id, e.id)

matches = [(e.id, MANUAL[e.id], e.category) for e in scaffold if e.id in MANUAL and MANUAL[e.id] in gen_keys]
print(f"Scaffold: {len(scaffold)}, Wired: {len(wired)}, Generators: {len(gen_keys)}")
print(f"Proposed wiring: {len(matches)}")
for row in sorted(matches):
    print(row)
