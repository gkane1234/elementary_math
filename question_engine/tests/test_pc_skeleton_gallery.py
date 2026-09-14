"""Precalc gallery wiring — reuse engines, deferred stub leaves."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

from question_engine.api.handler import _generate_for_type

_ROOT = Path(__file__).resolve().parents[2]
_GALLERY = _ROOT / "scripts" / "output" / "skeleton_phase01_gallery" / "gen_examples.py"


def _load_gallery_module():
    spec = importlib.util.spec_from_file_location("pc_gallery_gen", _GALLERY)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def gallery_mod():
    return _load_gallery_module()


def test_pc_deferred_count():
    mod = _load_gallery_module()
    # Other agent owns the deferred foundations list; may be empty while they rework it.
    assert isinstance(mod.PC_DEFERRED, frozenset)


def test_pc_shipped_sections_exclude_deferred_and_manual(gallery_mod):
    shipped_ids = {s["type_id"] for s in gallery_mod._build_pc_sections()}
    assert gallery_mod.PC_DEFERRED.isdisjoint(shipped_ids)
    assert gallery_mod.PC_MANUAL_SLUGS.isdisjoint(shipped_ids)
    # 94 PC catalog leaves − 5 manual trig skeleton sections (− deferred if any).
    expected = 94 - len(gallery_mod.PC_MANUAL_SLUGS) - len(gallery_mod.PC_DEFERRED)
    assert len(shipped_ids) == expected


@pytest.mark.parametrize(
    "type_id,pattern,engine",
    [
        ("pc_rational_equations", "EqCancel", "rational_skeleton"),
        ("pc_partial_fraction_decomposition", None, "constructive_pfd"),
        ("pc_functions_operations", None, "function_operations"),
        ("pc_dividing_polynomial_functions", "PolyLongDiv", "poly_long_division"),
        ("pc_exponential_equations_not_requiring_logarithms", None, "exponential_equation_simple"),
        ("pc_3d_vectors_operations", None, "vector_3d_operations"),
        ("pc_cross_products", None, "cross_products"),
        ("pc_average_rates_of_change", None, "average_rate_of_change"),
        ("pc_limits_at_essential_discontinuities", None, "limit_essential"),
        ("pc_continuity", None, "pc_continuity"),
    ],
)
def test_priority_pc_leaves_live(type_id: str, pattern: str | None, engine: str):
    qs = _generate_for_type(
        type_id,
        {"difficulty": 0, "seed": 101, "count": 1, "include_answer_key": True},
    )
    assert qs and qs[0].prompt_latex
    meta = qs[0].metadata or {}
    if pattern:
        assert meta.get("skeleton_pattern") == pattern
    if engine:
        assert meta.get("primitive_engine") == engine or meta.get("generator") == engine


def test_deferred_pc_empty(gallery_mod):
    assert len(gallery_mod.PC_DEFERRED) == 0
    # Former stub leaves now ship in gallery sections.
    shipped_ids = {s["type_id"] for s in gallery_mod._build_pc_sections()}
    for tid in (
        "pc_3d_vectors_operations",
        "pc_piecewise_functions",
        "pc_polynomial_inequalities",
        "pc_limits_at_kinks_and_jumps",
    ):
        assert tid in shipped_ids
        qs = _generate_for_type(tid, {"difficulty": 0, "seed": 101, "count": 1})
        assert qs and qs[0].prompt_latex
