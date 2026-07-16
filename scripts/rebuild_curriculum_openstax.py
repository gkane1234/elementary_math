"""
Rebuild lib/curriculum.ts:
  1) Fold unmapped catalog types into course curricula
  2) Reorder chapters to OpenStax textbook order (where we have a TOC)

Preserves existing leaf topic ids / names / type_ids when possible.
Prefers course-specific catalog type_ids over shared aliases when a leaf
id matches a catalog entry (so those types leave the “Other” bucket).

Usage:
  python scripts/rebuild_curriculum_openstax.py
  python scripts/rebuild_curriculum_openstax.py --dry-run
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from question_engine.catalog import TYPE_CATALOG
import question_engine.types  # noqa: F401

CURRICULUM_PATH = ROOT / "lib" / "curriculum.ts"
GAPS_DOC = ROOT / "scripts" / "output" / "curriculum_gaps" / "OPENSTAX_REORG.md"

# Catalog category prefix -> curriculum course id
PREFIX_TO_COURSE = {
    "Grade 6": "grade_6_math",
    "Pre-Algebra": "pre_algebra",
    "Algebra 1": "algebra_1",
    "Algebra 2": "algebra_2",
    "Geometry": "geometry",
    "Precalculus": "precalculus",
    "Calculus": "calculus",
}

COURSE_META = {
    "grade_6_math": ("Grade 6 Math", "Illustrative Math–style units (not OpenStax Prealgebra)"),
    "pre_algebra": ("Pre-Algebra", "OpenStax Prealgebra 2e"),
    "algebra_1": ("Algebra 1", "OpenStax Elementary Algebra 2e"),
    "algebra_2": ("Algebra 2", "OpenStax Intermediate Algebra 2e + supplemental"),
    "geometry": ("Geometry", "No OpenStax HS Geometry TOC in-repo — keep prior chapter order"),
    "precalculus": ("Precalculus", "OpenStax Precalculus 2e"),
    "calculus": ("Calculus", "OpenStax Calculus Vol. 1–2 (limits → DE)"),
}

# OpenStax (or documented) chapter spines. id, display name.
# Supplemental chapters (extra vs OpenStax) listed after the spine.
OPENSTAX_CHAPTERS: dict[str, list[tuple[str, str]]] = {
    # Grade 6: keep existing IM-style order (OpenStax Prealgebra is PA's book).
    "grade_6_math": [
        ("ratios", "Ratios"),
        ("rates", "Rates"),
        ("percents", "Percents"),
        ("dividing_fractions", "Dividing Fractions"),
        ("decimal_arithmetic", "Decimal Arithmetic"),
        ("common_factors_and_common_multiples", "Common Factors and Common Multiples"),
        ("negative_numbers_and_absolute_value", "Negative Numbers and Absolute Value"),
        ("coordinate_plane", "Coordinate Plane"),
        ("numeric_expressions_exponents_and_order_of_operations", "Numeric Expressions, Exponents, and the Order of Operations"),
        ("variables_and_algebraic_expressions", "Variables and Algebraic Expressions"),
        ("equivalent_expressions", "Equivalent Expressions"),
        ("equations", "Equations"),
        ("inequalities", "Inequalities"),
        ("equations_as_relationships_between_two_variables", "Equations as Relationships between Two Variables"),
        ("polygons", "Polygons"),
        ("polyhedra", "Polyhedra"),
        ("area_and_volume_with_fractions", "Area and Volume with Fractions"),
        ("data_sets_and_distributions", "Data Sets and Distributions"),
    ],
    # OpenStax Prealgebra 2e chs 1–11 + supplemental geometry/stats chapters we already teach.
    "pre_algebra": [
        ("whole_numbers", "Whole Numbers"),
        ("the_language_of_algebra", "The Language of Algebra"),
        ("integers", "Integers"),
        ("fractions", "Fractions"),
        ("decimals", "Decimals"),
        ("percents", "Percents"),
        ("the_properties_of_real_numbers", "The Properties of Real Numbers"),
        ("solving_linear_equations", "Solving Linear Equations"),
        ("math_models_and_geometry", "Math Models and Geometry"),
        ("polynomials", "Polynomials"),
        ("graphs", "Graphs"),
        # Supplemental (beyond OpenStax Prealgebra TOC)
        ("inequalities", "Inequalities"),
        ("factors_and_exponents", "Factors and Exponents"),
        ("proportions_and_similarity", "Proportions and Similarity"),
        ("right_triangles", "Right Triangles"),
        ("solid_figures", "Solid Figures"),
        ("statistics", "Statistics"),
    ],
    # OpenStax Elementary Algebra 2e chs 1–10 + extras we keep.
    "algebra_1": [
        ("foundations", "Foundations"),
        ("solving_linear_equations_and_inequalities", "Solving Linear Equations and Inequalities"),
        ("math_models", "Math Models"),
        ("graphs", "Graphs"),
        ("systems_of_linear_equations", "Systems of Linear Equations"),
        ("polynomials", "Polynomials"),
        ("factoring", "Factoring"),
        ("rational_expressions_and_equations", "Rational Expressions and Equations"),
        ("roots_and_radicals", "Roots and Radicals"),
        ("quadratic_equations", "Quadratic Equations"),
        # Supplemental vs Elementary Algebra TOC
        ("relations_and_introduction_to_functions", "Relations and Introduction to Functions"),
        ("exponents", "Exponents"),
        ("direct_and_inverse_variation", "Direct and Inverse Variation"),
        ("beginning_trigonometry", "Beginning Trigonometry"),
        ("statistics", "Statistics"),
    ],
    # OpenStax Intermediate Algebra 2e chs 1–12 + supplemental.
    "algebra_2": [
        ("foundations", "Foundations"),
        ("solving_linear_equations_and_inequalities", "Solving Linear Equations and Inequalities"),
        ("graphs_and_functions", "Graphs and Functions"),
        ("systems_of_linear_equations", "Systems of Linear Equations"),
        ("polynomials_and_polynomial_functions", "Polynomials and Polynomial Functions"),
        ("factoring", "Factoring"),
        ("rational_expressions_and_functions", "Rational Expressions and Functions"),
        ("roots_and_radicals", "Roots and Radicals"),
        ("quadratic_equations_and_functions", "Quadratic Equations and Functions"),
        ("exponential_and_logarithmic_functions", "Exponential and Logarithmic Functions"),
        ("conics", "Conics"),
        ("sequences_series_and_the_binomial_theorem", "Sequences, Series and the Binomial Theorem"),
        # Supplemental
        ("matrices", "Matrices"),
        ("complex_numbers", "Complex Numbers"),
        ("trigonometry", "Trigonometry"),
        ("probability_and_statistics", "Probability and Statistics"),
        ("direct_and_inverse_variation", "Direct and Inverse Variation"),
        ("general_functions", "General Functions"),
    ],
    # No OpenStax HS Geometry book in project sources — preserve prior order.
    "geometry": [
        ("review_of_algebra", "Review of Algebra"),
        ("basics_of_geometry", "Basics of Geometry"),
        ("parallel_lines_and_the_coordinate_plane", "Parallel Lines and the Coordinate Plane"),
        ("congruent_triangles", "Congruent Triangles"),
        ("properties_of_triangles", "Properties of Triangles"),
        ("quadrilaterals_and_polygons", "Quadrilaterals and Polygons"),
        ("similarity", "Similarity"),
        ("right_triangles", "Right Triangles"),
        ("trigonometry", "Trigonometry"),
        ("surface_area_and_volume", "Surface Area and Volume"),
        ("circles", "Circles"),
        ("transformations", "Transformations"),
        ("probability_and_statistics", "Probability and Statistics"),
        ("constructions", "Constructions"),
    ],
    # OpenStax Precalculus 2e chs 1–12 (trig split mapped into 5–8; systems/conics/etc.).
    "precalculus": [
        ("functions", "Functions"),
        ("linear_functions", "Linear Functions"),
        ("polynomial_and_rational_functions", "Polynomial and Rational Functions"),
        ("exponential_and_logarithmic_functions", "Exponential and Logarithmic Functions"),
        ("trigonometric_functions", "Trigonometric Functions"),
        ("periodic_functions", "Periodic Functions"),
        ("trigonometric_identities_and_equations", "Trigonometric Identities and Equations"),
        ("further_applications_of_trigonometry", "Further Applications of Trigonometry"),
        ("systems_of_equations_and_inequalities", "Systems of Equations and Inequalities"),
        ("analytic_geometry", "Analytic Geometry"),
        ("sequences_probability_and_counting_theory", "Sequences, Probability and Counting Theory"),
        ("introduction_to_calculus", "Introduction to Calculus"),
        # Supplemental slices we already teach as separate units
        ("parametric_equations", "Parametric Equations"),
        ("polar_coordinates", "Polar Coordinates"),
        ("vectors", "Vectors"),
        ("three_dimensional_vectors", "Three-Dimensional Vectors"),
    ],
    # OpenStax Calculus Vol.1 spine (+ continuity as sibling of limits).
    "calculus": [
        ("limits", "Limits"),
        ("continuity", "Continuity"),
        ("derivatives", "Derivatives"),
        ("applications_of_derivatives", "Applications of Derivatives"),
        ("integration", "Integration"),
        ("applications_of_integration", "Applications of Integration"),
        ("differential_equations", "Differential Equations"),
        # Keep prior split of indefinite/definite if we still have content mapped there via remap
    ],
}

# Map old curriculum chapter id OR catalog chapter name (casefold) -> new chapter id
CHAPTER_REMAP: dict[str, dict[str, str]] = {
    "grade_6_math": {},  # identity via matching names
    "pre_algebra": {
        "integers_decimals_and_fractions": "integers",  # split further by topic rules below
        "beginning_algebra": "the_language_of_algebra",
        "equations": "solving_linear_equations",
        "inequalities": "inequalities",
        "factors_and_exponents": "factors_and_exponents",
        "proportions_and_similarity": "proportions_and_similarity",
        "percents": "percents",
        "linear_equations_and_inequalities": "graphs",
        "plane_figures": "math_models_and_geometry",
        "solid_figures": "solid_figures",
        "right_triangles": "right_triangles",
        "beginning_polynomials": "polynomials",
        "statistics": "statistics",
        # catalog chapter names
        "Integers, Decimals, and Fractions": "integers",
        "Beginning Algebra": "the_language_of_algebra",
        "Equations": "solving_linear_equations",
        "Inequalities": "inequalities",
        "Factors and Exponents": "factors_and_exponents",
        "Proportions and Similarity": "proportions_and_similarity",
        "Percents": "percents",
        "Linear Equations and Inequalities": "graphs",
        "Plane Figures": "math_models_and_geometry",
        "Solid Figures": "solid_figures",
        "Right Triangles": "right_triangles",
        "Beginning Polynomials": "polynomials",
        "Statistics": "statistics",
    },
    "algebra_1": {
        "beginning_algebra": "foundations",
        "equations": "solving_linear_equations_and_inequalities",
        "inequalities": "solving_linear_equations_and_inequalities",
        "proportions_and_percents": "math_models",
        "relations_and_introduction_to_functions": "relations_and_introduction_to_functions",
        "linear_equations_and_inequalities": "graphs",
        "direct_and_inverse_variation": "direct_and_inverse_variation",
        "systems_of_equations_and_inequalities": "systems_of_linear_equations",
        "exponents": "exponents",
        "polynomials": "polynomials",
        "quadratic_functions": "quadratic_equations",
        "radical_expressions": "roots_and_radicals",
        "rational_expressions": "rational_expressions_and_equations",
        "beginning_trigonometry": "beginning_trigonometry",
        "statistics": "statistics",
        "Beginning Algebra": "foundations",
        "Equations": "solving_linear_equations_and_inequalities",
        "Inequalities": "solving_linear_equations_and_inequalities",
        "Proportions and Percents": "math_models",
        "Relations and Introduction to Functions": "relations_and_introduction_to_functions",
        "Linear Equations and Inequalities": "graphs",
        "Direct and inverse variation": "direct_and_inverse_variation",
        "Systems of Equations and Inequalities": "systems_of_linear_equations",
        "Exponents": "exponents",
        "Polynomials": "polynomials",
        "Quadratic Functions": "quadratic_equations",
        "Radical Expressions": "roots_and_radicals",
        "Rational Expressions": "rational_expressions_and_equations",
        "Beginning Trigonometry": "beginning_trigonometry",
        "Statistics": "statistics",
        "Factoring": "factoring",
    },
    "algebra_2": {
        "beginning_algebra": "foundations",
        "equations_and_inequalities": "solving_linear_equations_and_inequalities",
        "relations_and_introduction_to_functions": "graphs_and_functions",
        "linear_relations_and_functions": "graphs_and_functions",
        "direct_and_inverse_variation": "direct_and_inverse_variation",
        "systems_of_equations_and_inequalities": "systems_of_linear_equations",
        "matrices": "matrices",
        "complex_numbers": "complex_numbers",
        "quadratic_functions_and_inequalities": "quadratic_equations_and_functions",
        "polynomial_functions": "polynomials_and_polynomial_functions",
        "general_functions": "general_functions",
        "radical_functions_and_rational_exponents": "roots_and_radicals",
        "conic_sections": "conics",
        "rational_expressions": "rational_expressions_and_functions",
        "exponential_and_logarithmic_expressions": "exponential_and_logarithmic_functions",
        "sequences_and_series": "sequences_series_and_the_binomial_theorem",
        "trigonometry": "trigonometry",
        "probability_and_statistics": "probability_and_statistics",
        "Beginning Algebra": "foundations",
        "Equations and Inequalities": "solving_linear_equations_and_inequalities",
        "Relations and Introduction to Functions": "graphs_and_functions",
        "Linear Relations and Functions": "graphs_and_functions",
        "Direct and Inverse Variation": "direct_and_inverse_variation",
        "Systems of Equations and Inequalities": "systems_of_linear_equations",
        "Matrices": "matrices",
        "Complex Numbers": "complex_numbers",
        "Quadratic Functions and Inequalities": "quadratic_equations_and_functions",
        "Polynomial Functions": "polynomials_and_polynomial_functions",
        "General Functions": "general_functions",
        "Radical Functions and Rational Exponents": "roots_and_radicals",
        "Conic Sections": "conics",
        "Rational Expressions": "rational_expressions_and_functions",
        "Exponential and Logarithmic Expressions": "exponential_and_logarithmic_functions",
        "Sequences and Series": "sequences_series_and_the_binomial_theorem",
        "Trigonometry": "trigonometry",
        "Probability and Statistics": "probability_and_statistics",
    },
    "geometry": {
        # identity by matching names; also catalog names
        "Review of Algebra": "review_of_algebra",
        "Basics of Geometry": "basics_of_geometry",
        "Parallel Lines and the Coordinate Plane": "parallel_lines_and_the_coordinate_plane",
        "Congruent Triangles": "congruent_triangles",
        "Properties of Triangles": "properties_of_triangles",
        "Quadrilaterals and Polygons": "quadrilaterals_and_polygons",
        "Similarity": "similarity",
        "Right Triangles": "right_triangles",
        "Trigonometry": "trigonometry",
        "Surface Area and Volume": "surface_area_and_volume",
        "Circles": "circles",
        "Transformations": "transformations",
        "Probability and Statistics": "probability_and_statistics",
        "Constructions": "constructions",
    },
    "precalculus": {
        "functions": "functions",
        "power_polynomial_and_rational_functions": "polynomial_and_rational_functions",
        "exponential_and_logarithmic_expressions": "exponential_and_logarithmic_functions",
        "trigonometry": "trigonometric_functions",  # refined by topic rules
        "parametric_equations": "parametric_equations",
        "polar_coordinates": "polar_coordinates",
        "vectors": "vectors",
        "three_dimensional_vectors": "three_dimensional_vectors",
        "matrices_and_systems": "systems_of_equations_and_inequalities",
        "conic_sections": "analytic_geometry",
        "discrete_mathematics": "sequences_probability_and_counting_theory",
        "sequences_and_series": "sequences_probability_and_counting_theory",
        "introduction_to_calculus": "introduction_to_calculus",
        "Functions": "functions",
        "Power, Polynomial, and Rational Functions": "polynomial_and_rational_functions",
        "Exponential and Logarithmic Expressions": "exponential_and_logarithmic_functions",
        "Trigonometry": "trigonometric_functions",
        "Parametric Equations": "parametric_equations",
        "Polar Coordinates": "polar_coordinates",
        "Vectors": "vectors",
        "Three-Dimensional Vectors": "three_dimensional_vectors",
        "Matrices and Systems": "systems_of_equations_and_inequalities",
        "Conic Sections": "analytic_geometry",
        "Discrete Mathematics": "sequences_probability_and_counting_theory",
        "Sequences and Series": "sequences_probability_and_counting_theory",
        "Introduction to Calculus": "introduction_to_calculus",
    },
    "calculus": {
        "limits": "limits",
        "continuity": "continuity",
        "differentiation": "derivatives",
        "applications_of_differentiation": "applications_of_derivatives",
        "indefinite_integration": "integration",
        "definite_integration": "integration",
        "applications_of_integration": "applications_of_integration",
        "differential_equations": "differential_equations",
        "Limits": "limits",
        "Continuity": "continuity",
        "Differentiation": "derivatives",
        "Applications of Differentiation": "applications_of_derivatives",
        "Indefinite Integration": "integration",
        "Definite Integration": "integration",
        "Applications of Integration": "applications_of_integration",
        "Differential Equations": "differential_equations",
    },
}


@dataclass
class Leaf:
    id: str
    name: str
    type_id: str | None = None
    source: str = "curriculum"  # curriculum | catalog


@dataclass
class Chapter:
    id: str
    name: str
    leaves: list[Leaf] = field(default_factory=list)


def slugify(name: str) -> str:
    s = name.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return s.strip("_") or "topic"


def parse_existing_curriculum(src: str) -> dict[str, list[tuple[str, str, list[Leaf]]]]:
    """Return course_id -> [(chapter_id, chapter_name, leaves including nested flattened with path notes)]."""
    courses: dict[str, list[tuple[str, str, list[Leaf]]]] = {}
    course_ids = list(COURSE_META.keys())

    for i, cid in enumerate(course_ids):
        m = re.search(
            rf'id:\s*"{cid}",\s*\n\s*name:\s*"[^"]+",\s*\n\s*topics:\s*\[',
            src,
        )
        if not m:
            continue
        start = m.end()
        end = len(src)
        for other in course_ids[i + 1 :]:
            om = re.search(rf'id:\s*"{other}",', src[start:])
            if om:
                end = min(end, start + om.start())
        block = src[start:end]
        chapters: list[tuple[str, str, list[Leaf]]] = []
        # Find top-level chapters at indent 6
        chap_re = re.compile(
            r'^\s{6}\{\s*\n\s{8}id:\s*"([^"]+)",\s*\n\s{8}name:\s*"([^"]+)",\s*\n\s{8}topics:\s*\[',
            re.MULTILINE,
        )
        matches = list(chap_re.finditer(block))
        for j, cm in enumerate(matches):
            ch_id, ch_name = cm.group(1), cm.group(2)
            ch_start = cm.end()
            ch_end = matches[j + 1].start() if j + 1 < len(matches) else len(block)
            ch_block = block[ch_start:ch_end]
            leaves = extract_leaves(ch_block)
            chapters.append((ch_id, ch_name, leaves))
        courses[cid] = chapters
    return courses


def extract_leaves(block: str) -> list[Leaf]:
    """Extract leaf topics (no nested topics array) from a chapter block."""
    leaves: list[Leaf] = []
    # Match objects with id + name; skip those that open a nested topics: [
    topic_re = re.compile(
        r'\{\s*id:\s*"([^"]+)",\s*name:\s*"([^"]+)"([^}]*)\}',
        re.DOTALL,
    )
    for m in topic_re.finditer(block):
        tid, tname, rest = m.group(1), m.group(2), m.group(3)
        # Nested container: has topics: [ before closing — our regex stops at first }
        # so containers with nested topics won't match the simple pattern well.
        # Detect containers separately:
        if "topics:" in rest:
            continue
        type_m = re.search(r'type_id:\s*"([^"]+)"', rest)
        type_id = type_m.group(1) if type_m else None
        leaves.append(Leaf(id=tid, name=tname, type_id=type_id, source="curriculum"))

    # Also pull nested factoring-style leaves: topics: [ { id... } ]
    # The simple regex may miss nested ones if they're deeper. Scan for all type_id leaves.
    # Re-scan for any type_id-bearing leaf-like objects we missed:
    deep_re = re.compile(
        r'\{\s*id:\s*"([^"]+)",\s*name:\s*"([^"]+)",\s*type_id:\s*"([^"]+)"\s*\}'
    )
    seen = {lf.id for lf in leaves}
    for m in deep_re.finditer(block):
        tid, tname, type_id = m.group(1), m.group(2), m.group(3)
        if tid in seen:
            # Prefer updating type_id if we had a stub without it
            continue
        # Skip if this id is a chapter-like container already processed
        leaves.append(Leaf(id=tid, name=tname, type_id=type_id, source="curriculum"))
        seen.add(tid)

    # Coming-soon stubs without type_id (e.g. percent diagrams)
    stub_re = re.compile(
        r'\{\s*id:\s*"([^"]+)",\s*\n?\s*name:\s*"([^"]+)",?\s*\n?\s*\}'
    )
    for m in stub_re.finditer(block):
        tid, tname = m.group(1), m.group(2)
        if tid in seen:
            continue
        # Heuristic: if followed soon by topics:, it's a container
        after = block[m.end() : m.end() + 40]
        if "topics:" in after:
            continue
        leaves.append(Leaf(id=tid, name=tname, type_id=None, source="curriculum"))
        seen.add(tid)

    return leaves


def resolve_chapter_id(course_id: str, old_chapter_id: str, old_chapter_name: str) -> str:
    remap = CHAPTER_REMAP.get(course_id, {})
    if old_chapter_id in remap:
        return remap[old_chapter_id]
    if old_chapter_name in remap:
        return remap[old_chapter_name]
    # identity if chapter id already in spine
    spine_ids = {cid for cid, _ in OPENSTAX_CHAPTERS[course_id]}
    if old_chapter_id in spine_ids:
        return old_chapter_id
    # try slug of name
    slug = slugify(old_chapter_name)
    if slug in spine_ids:
        return slug
    return old_chapter_id


def refine_chapter_for_leaf(course_id: str, chapter_id: str, leaf: Leaf) -> str:
    """Topic-level refinements into OpenStax chapters."""
    name = leaf.name.casefold()
    tid = leaf.id.casefold()
    type_id = (leaf.type_id or "").casefold()

    if course_id == "pre_algebra" and chapter_id == "integers":
        # Split former Integers/Decimals/Fractions bucket
        if any(k in name or k in tid for k in ("decimal", "rounding", "place", "writing_numbers")):
            return "decimals"
        if any(k in name or k in tid for k in ("fraction", "mixed")):
            return "fractions"
        if any(k in name or k in tid for k in ("whole",)):
            return "whole_numbers"
        if any(k in name or k in tid for k in ("factor", "gcf", "lcm")):
            return "factors_and_exponents"
        return "integers"

    if course_id == "algebra_1":
        if chapter_id == "polynomials" and any(
            k in name or k in tid or k in type_id
            for k in ("factor", "grouping", "quadratic_expressions", "special_cases", "common_factor")
        ):
            return "factoring"
        if chapter_id == "solving_linear_equations_and_inequalities":
            if any(k in name for k in ("mixture", "distance", "work", "age", "coin", "consecutive", "percent word")):
                return "math_models"
            if "word problem" in name and "equation" not in name:
                return "math_models"

    if course_id == "algebra_2":
        if chapter_id == "polynomials_and_polynomial_functions" and "factor" in name:
            return "factoring"
        if chapter_id == "sequences_series_and_the_binomial_theorem" and "binomial" in name:
            return "sequences_series_and_the_binomial_theorem"

    if course_id == "precalculus":
        if chapter_id == "trigonometric_functions":
            # Split trig into OpenStax 5–8
            if any(k in name or k in tid for k in ("identity", "sum and", "multiple", "product-to", "product_to", "factoring and fundamental")):
                return "trigonometric_identities_and_equations"
            if any(k in name or k in tid for k in ("law of", "area and law", "sine", "cosine")) and "graph" not in name:
                if any(k in name for k in ("law of", "area and")):
                    return "further_applications_of_trigonometry"
            if any(k in name or k in tid for k in ("graphing trig", "periodic", "amplitude")):
                return "periodic_functions"
            if any(k in name or k in tid for k in ("inverse trig",)):
                return "trigonometric_functions"
        if chapter_id == "functions":
            # linear-ish leftovers stay; power functions -> poly chapter
            if "power function" in name:
                return "polynomial_and_rational_functions"

    if course_id == "calculus":
        if chapter_id == "integration":
            return "integration"

    return chapter_id


def catalog_entries_by_course() -> dict[str, list]:
    by: dict[str, list] = defaultdict(list)
    for e in TYPE_CATALOG:
        prefix = e.category.split(" — ")[0] if " — " in e.category else e.category
        course = PREFIX_TO_COURSE.get(prefix)
        if course:
            by[course].append(e)
    return by


def catalog_chapter_name(entry) -> str:
    if " — " in entry.category:
        return entry.category.split(" — ", 1)[1]
    return entry.category


def build_courses(existing: dict[str, list[tuple[str, str, list[Leaf]]]]) -> dict[str, list[Chapter]]:
    catalog_by_course = catalog_entries_by_course()
    id_to_entry = {e.id: e for e in TYPE_CATALOG}
    result: dict[str, list[Chapter]] = {}

    for course_id, spine_src in OPENSTAX_CHAPTERS.items():
        spine: list[tuple[str, str]] = list(spine_src)
        chapters = {cid: Chapter(id=cid, name=name) for cid, name in spine}
        placed_type_ids: set[str] = set()
        placed_leaf_ids: set[str] = set()
        placed_generators: set[str] = set()
        course_catalog = catalog_by_course.get(course_id, [])
        prefixes = ("pa_", "a2_", "geo_", "pc_", "g6_", "calc_")

        def generator_of(type_id: str | None) -> str | None:
            if not type_id:
                return None
            entry = id_to_entry.get(type_id)
            return entry.generator if entry else type_id

        def prefer_course_type_id(leaf: Leaf) -> str | None:
            """Keep stable type_ids; only retarget shared ids to course-local catalog twins."""
            # If the leaf id is a catalog type, that is the canonical wiring for this row.
            if leaf.id and any(e.id == leaf.id for e in course_catalog):
                return leaf.id
            # Preserve an existing type_id when it is already a real catalog entry.
            if leaf.type_id and leaf.type_id in id_to_entry:
                # Upgrade shared → course-local twin with the same name, when unique.
                name_key = leaf.name.casefold().strip()
                twins = [
                    e
                    for e in course_catalog
                    if e.name.casefold().strip() == name_key and e.id.startswith(prefixes)
                ]
                if len(twins) == 1 and not leaf.type_id.startswith(prefixes):
                    return twins[0].id
                return leaf.type_id
            # No type_id yet: try course-local name match, then any name match.
            name_key = leaf.name.casefold().strip()
            matches = [e for e in course_catalog if e.name.casefold().strip() == name_key]
            preferred = [e for e in matches if e.id.startswith(prefixes)]
            if len(preferred) == 1:
                return preferred[0].id
            if len(matches) == 1:
                return matches[0].id
            return leaf.type_id

        # 1) Place existing curriculum leaves
        for old_ch_id, old_ch_name, leaves in existing.get(course_id, []):
            base_ch = resolve_chapter_id(course_id, old_ch_id, old_ch_name)
            for leaf in leaves:
                ch_id = refine_chapter_for_leaf(course_id, base_ch, leaf)
                if ch_id not in chapters:
                    chapters[ch_id] = Chapter(
                        id=ch_id,
                        name=old_ch_name if ch_id == old_ch_id else ch_id.replace("_", " ").title(),
                    )
                    spine.append((ch_id, chapters[ch_id].name))
                type_id = prefer_course_type_id(leaf)
                new_leaf = Leaf(id=leaf.id, name=leaf.name, type_id=type_id, source="curriculum")
                if new_leaf.id in placed_leaf_ids:
                    continue
                # Skip duplicate display+generator in same chapter
                gen = generator_of(type_id)
                if any(
                    lf.name.casefold() == new_leaf.name.casefold()
                    and generator_of(lf.type_id) == gen
                    for lf in chapters[ch_id].leaves
                ):
                    continue
                chapters[ch_id].leaves.append(new_leaf)
                placed_leaf_ids.add(new_leaf.id)
                if type_id:
                    placed_type_ids.add(type_id)
                if gen:
                    placed_generators.add(gen)

        # 2) Fold remaining catalog entries into this course
        for entry in course_catalog:
            if entry.id in placed_type_ids or entry.id in placed_leaf_ids:
                continue
            if any(lf.type_id == entry.id for ch in chapters.values() for lf in ch.leaves):
                continue
            cat_ch = catalog_chapter_name(entry)
            ch_id = resolve_chapter_id(course_id, slugify(cat_ch), cat_ch)
            leaf = Leaf(id=entry.id, name=entry.name, type_id=entry.id, source="catalog")
            ch_id = refine_chapter_for_leaf(course_id, ch_id, leaf)
            if ch_id not in chapters:
                chapters[ch_id] = Chapter(id=ch_id, name=cat_ch)
                spine.append((ch_id, cat_ch))
            if any(lf.type_id == entry.id for lf in chapters[ch_id].leaves):
                continue
            # Same label in chapter: retarget to course catalog id (avoid duplicate rows)
            same_name = [
                lf for lf in chapters[ch_id].leaves if lf.name.casefold() == entry.name.casefold()
            ]
            if same_name:
                target = same_name[0]
                if target.type_id != entry.id:
                    # Only retarget when current type is shared / other-course
                    if not (target.type_id or "").startswith(prefixes):
                        target.type_id = entry.id
                        placed_type_ids.add(entry.id)
                        placed_generators.add(entry.generator)
                else:
                    placed_type_ids.add(entry.id)
                continue
            # Same generator already on a course-local leaf elsewhere: skip (alias)
            if entry.generator in placed_generators:
                already_local = False
                for ch in chapters.values():
                    for lf in ch.leaves:
                        if not lf.type_id:
                            continue
                        ent = id_to_entry.get(lf.type_id)
                        if (
                            ent
                            and ent.generator == entry.generator
                            and lf.type_id.startswith(prefixes)
                        ):
                            already_local = True
                            break
                    if already_local:
                        break
                if already_local:
                    continue
            chapters[ch_id].leaves.append(leaf)
            placed_type_ids.add(entry.id)
            placed_leaf_ids.add(entry.id)
            placed_generators.add(entry.generator)

        ordered: list[Chapter] = []
        seen_ch: set[str] = set()
        for cid, _name in spine:
            if cid in chapters and cid not in seen_ch:
                ordered.append(chapters[cid])
                seen_ch.add(cid)
        for cid, ch in chapters.items():
            if cid not in seen_ch:
                ordered.append(ch)
                seen_ch.add(cid)

        result[course_id] = [ch for ch in ordered if ch.leaves]

    return result


def emit_ts(courses: dict[str, list[Chapter]]) -> str:
    lines: list[str] = [
        'import type { CurriculumLevel } from "@/lib/types";',
        "",
        "export const CURRICULUM: CurriculumLevel[] = [",
    ]
    course_order = list(COURSE_META.keys())
    for course_id in course_order:
        name, _src = COURSE_META[course_id]
        chapters = courses.get(course_id, [])
        lines.append("  {")
        lines.append(f'    id: "{course_id}",')
        lines.append(f'    name: "{name}",')
        lines.append("    topics: [")
        for ch in chapters:
            lines.append("      {")
            lines.append(f'        id: "{ch.id}",')
            lines.append(f'        name: "{ch.name}",')
            lines.append("        topics: [")
            for leaf in ch.leaves:
                name_esc = leaf.name.replace("\\", "\\\\").replace('"', '\\"')
                if leaf.type_id:
                    lines.append(
                        f'          {{ id: "{leaf.id}", name: "{name_esc}", type_id: "{leaf.type_id}" }},'
                    )
                else:
                    lines.append(
                        f'          {{ id: "{leaf.id}", name: "{name_esc}" }},'
                    )
            lines.append("        ],")
            lines.append("      },")
        lines.append("    ],")
        lines.append("  },")
    lines.append("];")
    lines.append("")
    lines.append("export function getCurriculumLevel(levelId: string): CurriculumLevel | undefined {")
    lines.append("  return CURRICULUM.find((level) => level.id === levelId);")
    lines.append("}")
    lines.append("")
    return "\n".join(lines)


def write_gaps_doc(courses: dict[str, list[Chapter]], unmapped_after: list) -> None:
    lines = [
        "# OpenStax curriculum reorganization notes",
        "",
        "Generated by `scripts/rebuild_curriculum_openstax.py`.",
        "",
        "## Course spines",
        "",
    ]
    for cid, (name, source) in COURSE_META.items():
        lines.append(f"### `{cid}` — {name}")
        lines.append(f"- Source: {source}")
        chs = courses.get(cid, [])
        lines.append(f"- Chapters ({len(chs)}): " + ", ".join(f"**{c.name}**" for c in chs))
        n_leaves = sum(len(c.leaves) for c in chs)
        lines.append(f"- Leaves: {n_leaves}")
        lines.append("")

    lines.append("## Types still in “Other question types”")
    lines.append("")
    if not unmapped_after:
        lines.append("_None — all catalog types are wired into a curriculum leaf._")
    else:
        lines.append(f"{len(unmapped_after)} catalog type(s) remain unmapped:")
        lines.append("")
        by_cat: dict[str, list] = defaultdict(list)
        for e in unmapped_after:
            by_cat[e.category].append(e)
        for cat in sorted(by_cat):
            lines.append(f"### {cat}")
            for e in by_cat[cat]:
                lines.append(f"- `{e.id}` — {e.name}")
            lines.append("")

    lines.append("## Known gaps / caveats")
    lines.append("")
    lines.append("- **Grade 6** keeps Illustrative Math–style unit order; OpenStax Prealgebra is the Pre-Algebra spine.")
    lines.append("- **Geometry** has no OpenStax HS Geometry TOC in-repo; prior chapter order preserved.")
    lines.append("- Supplemental chapters (trig on A1, matrices/complex on A2, vectors/polar on PC, etc.) sit after the OpenStax spine.")
    lines.append("- Nested factoring groups were flattened into the Factoring chapter (A1) / appropriate A2 chapter.")
    lines.append("- Catalog `CATEGORY_ORDER` may still use older chapter labels until a follow-up catalog rename pass.")
    lines.append("")
    GAPS_DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", dest="dry_run")
    args = parser.parse_args()

    src = CURRICULUM_PATH.read_text(encoding="utf-8")
    existing = parse_existing_curriculum(src)
    courses = build_courses(existing)
    out = emit_ts(courses)

    # Compute remaining unmapped
    mapped = set(re.findall(r'type_id:\s*"([^"]+)"', out))
    unmapped_after = [e for e in TYPE_CATALOG if e.id not in mapped]

    if args.dry_run:
        print(out[:2000])
        print("...")
        for cid, chs in courses.items():
            print(f"{cid}: {len(chs)} chapters, {sum(len(c.leaves) for c in chs)} leaves")
        print(f"Remaining unmapped: {len(unmapped_after)}")
        return

    CURRICULUM_PATH.write_text(out, encoding="utf-8")
    write_gaps_doc(courses, unmapped_after)
    print(f"Wrote {CURRICULUM_PATH}")
    print(f"Wrote {GAPS_DOC}")
    for cid, chs in courses.items():
        print(f"  {cid}: {len(chs)} chapters, {sum(len(c.leaves) for c in chs)} leaves")
    print(f"Remaining unmapped catalog types: {len(unmapped_after)}")
    if unmapped_after:
        for e in unmapped_after[:30]:
            print(f"  - {e.id} ({e.category})")
        if len(unmapped_after) > 30:
            print(f"  ... +{len(unmapped_after) - 30} more")


if __name__ == "__main__":
    main()
