"""Precalculus OpenStax form catalogs drive form_id metadata on PC leaves."""

from __future__ import annotations

from question_engine.frameworks.primitives.openstax_form_catalogs import (
    catalog_gaps,
    implemented_forms,
    load_form_catalog,
)
from question_engine.frameworks.primitives.openstax_precalc import (
    PC_CATALOGS,
    select_pc_form,
)
from question_engine.generators.algebra2 import GENERATORS as A2_GENERATORS
from question_engine.generators.precalc import GENERATORS as PC_GENERATORS
from question_engine.generators.primitive_rational import partial_fraction_decomposition


def test_precalc_catalogs_load_and_count():
    totals = {}
    for name in PC_CATALOGS:
        cat = load_form_catalog(name)
        impl = implemented_forms(cat)
        gaps = catalog_gaps(cat)
        assert impl, name
        totals[name] = (len(impl), len(gaps), len(cat["forms"]))
    # Sanity: five catalogs with real breadth
    assert len(totals) == 5
    assert sum(t[0] for t in totals.values()) >= 20


def test_select_pc_form_stamps_metadata():
    form, stamp = select_pc_form(
        "precalculus_partial_fractions",
        d=10.0,
        leaf_id="pc_partial_fraction_decomposition",
    )
    assert form["form_id"]
    assert stamp["form_id"] == form["form_id"]
    assert stamp["openstax_form"] == form["form_id"]
    assert stamp["catalog_id"] == "precalculus_partial_fractions"
    assert stamp["construction"] == "forward_form_catalog"


def test_pc_pfd_emits_form_id():
    seen: set[str] = set()
    for d, seed0 in ((4, 1), (10, 40), (16, 80)):
        for seed in range(seed0, seed0 + 12):
            qs = partial_fraction_decomposition(
                "pc_partial_fraction_decomposition",
                {
                    "difficulty": d,
                    "count": 1,
                    "seed": seed,
                    "include_answer_key": True,
                },
            )
            meta = qs[0].metadata or {}
            fid = str(meta.get("form_id") or "")
            assert fid, (d, seed, meta)
            assert meta.get("openstax_form") == fid
            seen.add(fid)
    assert len(seen) >= 2, seen
    assert any("linear" in s or "quadratic" in s for s in seen)


def test_pc_function_ops_emits_form_id():
    gen = A2_GENERATORS["function_operations"]
    seen: set[str] = set()
    for d, seed0 in ((2, 1), (8, 30), (14, 60)):
        for seed in range(seed0, seed0 + 10):
            qs = gen(
                "pc_functions_operations",
                {
                    "difficulty": d,
                    "count": 1,
                    "seed": seed,
                    "include_answer_key": True,
                },
            )
            meta = qs[0].metadata or {}
            fid = str(meta.get("form_id") or "")
            assert fid, (d, seed, meta.keys())
            seen.add(fid)
    assert len(seen) >= 2, seen


def test_pc_exp_log_and_trig_emit_form_ids():
    cases = [
        ("exponential_equation_simple", "pc_exponential_equations_not_requiring_logarithms"),
        ("log_change_of_base", "pc_properties_of_logarithms"),
        ("log_equation_simple", "pc_logarithmic_equations_hard"),
        ("log_equation_simple", "pc_logarithmic_equations_simple"),
        ("trig_basic_identities", "pc_fundamental_identities"),
        ("trig_factoring_equations", "pc_equations_with_factoring_and_fundamental_identities"),
        ("simple_trig_equations", "pc_simple_trig_equations"),
    ]
    for gen_key, leaf in cases:
        gen = PC_GENERATORS[gen_key]
        qs = gen(
            leaf,
            {"difficulty": 12, "count": 1, "seed": 77, "include_answer_key": True},
        )
        meta = qs[0].metadata or {}
        assert meta.get("form_id"), (gen_key, leaf, meta)
        assert meta.get("openstax_form") == meta.get("form_id")


def test_pc_log_equation_hard_d_ladder_shapes():
    """Hard leaf must not stamp bare definition at high D; D=0 stays multi-step."""
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        load_form_catalog,
    )

    load_form_catalog.cache_clear()
    gen = PC_GENERATORS["log_equation_simple"]
    easy_modes = set()
    hard_modes = set()
    for seed in range(200, 260):
        q0 = gen(
            "pc_logarithmic_equations_hard",
            {"difficulty": 0, "count": 1, "seed": seed, "include_answer_key": True},
        )[0]
        easy_modes.add(str((q0.metadata or {}).get("mode") or ""))
        qh = gen(
            "pc_logarithmic_equations_hard",
            {"difficulty": 22, "count": 1, "seed": seed, "include_answer_key": True},
        )[0]
        hard_modes.add(str((qh.metadata or {}).get("mode") or ""))
    assert "definition" not in easy_modes, easy_modes
    assert easy_modes <= {"linear_argument", "algebra_coeff"}, easy_modes
    assert "definition" not in hard_modes, hard_modes
    assert hard_modes & {
        "product_sum",
        "quotient_diff",
        "one_to_one_quadratic",
    }, hard_modes


def test_pc_log_equation_simple_d0_is_definition():
    """D=0 must not be coerced to 6 (falsy `or 6` bug) — stay definition-only."""
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        load_form_catalog,
    )

    load_form_catalog.cache_clear()
    gen = PC_GENERATORS["log_equation_simple"]
    modes = set()
    for seed in range(100, 140):
        q = gen(
            "pc_logarithmic_equations_simple",
            {"difficulty": 0, "count": 1, "seed": seed, "include_answer_key": True},
        )[0]
        modes.add(str((q.metadata or {}).get("mode") or ""))
        assert "\\log" in q.prompt_latex or "ln" in q.prompt_latex
        # Bare argument x, not linear ax+c / product of logs
        assert "+ \\log" not in q.prompt_latex.replace(" ", "")
        assert q.prompt_latex.count("x") == 1
    assert modes == {"definition"}, modes


def test_pc_log_props_diversifies_rules():
    gen = PC_GENERATORS["log_change_of_base"]
    modes: set[str] = set()
    for seed in range(200, 280):
        qs = gen(
            "pc_properties_of_logarithms",
            {
                "difficulty": 10,
                "count": 1,
                "seed": seed,
                "include_answer_key": True,
            },
        )
        meta = qs[0].metadata or {}
        modes.add(str(meta.get("mode") or meta.get("form_id") or ""))
    assert len(modes) >= 3, modes
