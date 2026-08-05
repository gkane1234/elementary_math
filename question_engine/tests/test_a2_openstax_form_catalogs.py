"""OpenStax Intermediate Algebra form catalogs drive A2 algebraic generation."""

from __future__ import annotations

import random

from question_engine.frameworks.primitives.openstax_a2 import (
    A2_CATALOGS,
    select_a2_form,
)
from question_engine.frameworks.primitives.openstax_form_catalogs import (
    catalog_gaps,
    implemented_forms,
    load_form_catalog,
)
from question_engine.generators.algebra2 import GENERATORS as A2_GENERATORS
from question_engine.generators.primitive_polynomial import polynomial_add_subtract
from question_engine.generators.primitive_rational import (
    rational_add_subtract,
    rational_simplify,
)
from question_engine.generators.radical_equations import generate_radical_equations


def test_a2_catalogs_load_and_have_implemented_forms():
    totals = {}
    for name in A2_CATALOGS:
        cat = load_form_catalog(name)
        assert cat["catalog_id"] == name
        impl = implemented_forms(cat)
        gaps = catalog_gaps(cat)
        assert impl, f"{name} needs at least one implemented form"
        totals[name] = (len(impl), len(gaps), len(cat["forms"]))
        # D-weighted select works
        form, meta = select_a2_form(name, d=8.0, rng=random.Random(0))
        assert form["form_id"]
        assert meta["form_id"] == form["form_id"]
        assert meta["openstax_form"] == form["form_id"]
        assert meta["construction"] == "forward_form_catalog"
    # Sanity: five catalogs
    assert len(totals) == 5


def test_a2_rational_add_emits_form_id():
    qs = rational_add_subtract(
        "a2_rational_expressions_adding_and_subtracting",
        {"difficulty": 6, "count": 8, "include_answer_key": True, "seed": 42},
    )
    assert len(qs) == 8
    ids = {str((q.metadata or {}).get("form_id") or "") for q in qs}
    ids.discard("")
    assert ids, "expected form_id metadata on A2 rational add"
    assert ids <= {
        "add_common_den",
        "add_unlike_dens",
        "add_unlike_with_cancel",
    }
    for q in qs:
        meta = q.metadata or {}
        assert meta.get("openstax_form") == meta.get("form_id")


def test_a2_rational_simplify_emits_form_id():
    qs = rational_simplify(
        "a2_rational_expressions_simplifying",
        {"difficulty": 4, "count": 3, "include_answer_key": True, "seed": 7},
    )
    assert qs
    meta = qs[0].metadata or {}
    assert meta.get("form_id") == "simplify_cancel"
    assert meta.get("openstax_form") == "simplify_cancel"


def test_a2_poly_add_respects_form_op():
    qs = polynomial_add_subtract(
        "a2_polynomial_functions_adding_and_subtracting",
        {"difficulty": 4, "count": 12, "include_answer_key": True, "seed": 11},
    )
    assert qs
    for q in qs:
        meta = q.metadata or {}
        fid = meta.get("form_id")
        assert fid in {"poly_add", "poly_subtract"}
        if fid == "poly_add":
            assert meta.get("op") == "+"
        if fid == "poly_subtract":
            assert meta.get("op") == "-"


def test_a2_function_ops_catalog_drives_form_ids():
    gen = A2_GENERATORS["function_operations"]
    seen = set()
    for d, seed in ((0.0, 1), (8.0, 2), (12.0, 3), (16.0, 4)):
        qs = gen(
            "a2_general_functions_operations",
            {"difficulty": d, "count": 6, "include_answer_key": True, "seed": seed},
        )
        for q in qs:
            fid = str((q.metadata or {}).get("form_id") or "")
            if fid:
                seen.add(fid)
    assert seen & {"fn_add", "fn_subtract", "fn_product", "fn_compose"}


def test_a2_radical_equations_catalog_form_ids():
    qs = generate_radical_equations(
        "a2_radical_functions_and_rational_exponents_radical_equations",
        {
            "difficulty": 14,
            "count": 6,
            "include_answer_key": True,
            "seed": 99,
            "allow_light_prep": True,
            "allow_isolate_algebra": True,
            "allow_radical_equals_linear": True,
            "allow_two_radicals": True,
        },
    )
    assert qs
    ids = {str((q.metadata or {}).get("form_id") or "") for q in qs}
    ids.discard("")
    assert ids, "expected catalog form_id on A2 radical equations"
    assert ids <= {
        "radical_eq_isolate",
        "radical_eq_equals_linear",
        "radical_eq_two_radicals",
    }


def test_a2_catalog_gaps_document_stubs():
    """PFD / apps / GCF remain non-implemented gaps in IntAlg catalogs."""
    rats = load_form_catalog("algebra2_rationals")
    gap_ids = {f["form_id"] for f in catalog_gaps(rats)}
    assert "pfd_linear_factors" in gap_ids
    assert "rational_apps" in gap_ids
    polys = load_form_catalog("algebra2_polys")
    poly_gaps = {f["form_id"] for f in catalog_gaps(polys)}
    assert "gcf_factor" in poly_gaps or "long_division" in poly_gaps
