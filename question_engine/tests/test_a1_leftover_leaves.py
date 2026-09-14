"""Live-path smoke for leftover A1 poly / quadratic / radical / numeric-rational leaves."""

from __future__ import annotations

from question_engine.api.handler import _generate_for_type


def _q(type_id: str, d: float, seed: int = 101, extra: dict | None = None):
    settings = {
        "difficulty": d,
        "seed": seed,
        "count": 1,
        "include_answer_key": True,
        "integers_only": True,
        "only_x": True,
        **(extra or {}),
    }
    qs = _generate_for_type(type_id, settings)
    assert qs, (type_id, d, seed)
    return qs[0]


def _pat(q) -> str:
    return str((q.metadata or {}).get("skeleton_pattern") or "")


def test_poly_simplify_and_naming():
    q = _q("simplify_polynomials", 0.0)
    assert _pat(q) == "PolySimplify"
    assert q.answer_latex
    hi = _q("simplify_polynomials", 16.0, seed=207)
    assert _pat(hi) == "PolySimplify"
    name = _q("polynomial_naming", 0.0)
    assert _pat(name) == "PolyNaming"
    assert "Name the polynomial" in (name.prompt_latex or "")
    assert name.answer_latex


def test_poly_long_division_stamps_and_generates():
    q = _q("polynomial_long_division", 0.0)
    assert _pat(q) == "PolyLongDiv"
    assert r"\frac" in (q.prompt_latex or "")
    assert q.answer_latex
    hi = _q("polynomial_long_division", 16.0, seed=207)
    assert _pat(hi) == "PolyLongDiv"


def test_numeric_rationals_and_sets():
    add = _q("rational_add_subtract", 0.0)
    assert _pat(add) == "FractionAddSub"
    assert r"\frac" in (add.prompt_latex or "")
    mul = _q("rational_multiply", 0.0)
    assert _pat(mul) == "FractionMul"
    div = _q("rational_divide", 0.0)
    assert _pat(div) == "FractionDiv"
    sets = _q("sets_of_numbers", 0.0)
    assert _pat(sets) == "NumberCore"
    assert sets.answer_latex


def test_quadratic_solve_leaves_stamp_patterns():
    for type_id, pat in (
        ("quadratic_square_roots", "QuadraticSqrt"),
        ("quadratic_formula", "QuadraticFormula"),
        ("quadratic_discriminant", "QuadraticDiscriminant"),
        ("quadratic_completing_square_constant", "CompleteSquareConst"),
        ("quadratic_completing_square_solve", "CompleteSquareSolve"),
    ):
        q = _q(type_id, 0.0)
        assert _pat(q) == pat, (type_id, _pat(q), q.prompt_latex)
        assert q.prompt_latex
        assert q.answer_latex
        hi = _q(type_id, 16.0, seed=207)
        assert _pat(hi) == pat


def test_quadratic_square_roots_d0_is_isolated_square():
    blob = (_q("quadratic_square_roots", 0.0).prompt_latex or "").replace(" ", "")
    assert "^{2}" in blob or "^2" in blob
    assert "=" in blob


def test_radical_leaves_stamp_patterns():
    for type_id, pat in (
        ("radical_simplification", "RadicalSimplify"),
        ("radical_add_subtract", "RadicalAddSub"),
        ("radical_multiply", "RadicalMul"),
        ("radical_divide", "RadicalDiv"),
        ("radical_equations", "RadicalEq"),
    ):
        q = _q(type_id, 0.0)
        assert _pat(q) == pat, (type_id, _pat(q), q.prompt_latex)
        assert r"\sqrt" in (q.prompt_latex or "")
        assert q.answer_latex
        hi = _q(type_id, 16.0, seed=207)
        assert _pat(hi) == pat


def test_quadratic_graph_leaves_stamp_red_header_patterns():
    g = _q("graphing_quadratic_functions", 0.0)
    assert _pat(g) == "GraphQuadratic"
    assert "x" in (g.prompt_latex or "")
    s = _q("quadratic_solve_by_graphing", 0.0)
    assert _pat(s) == "SolveByGraphing"
    assert "= 0" in (s.prompt_latex or "") or "=0" in (s.prompt_latex or "").replace(
        " ", ""
    )
    iq = _q("graphing_quadratic_inequalities", 0.0)
    assert _pat(iq) == "GraphQuadraticIneq"
    assert "<" in (iq.prompt_latex or "") or ">" in (iq.prompt_latex or "")
