"""Live-path smoke for A2 leaves wired to A1 / skeleton engines."""

from __future__ import annotations

import re

from question_engine.api.handler import _generate_for_type
from question_engine.frameworks.primitives.wp_packaging import looks_like_dumped_equation


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


def _inner_a(q) -> int:
    raw = (q.metadata or {}).get("inner_a")
    assert raw is not None, q.metadata
    return abs(int(str(raw).split("/")[0])) if "/" in str(raw) else abs(int(raw))


def test_a2_multi_step_and_literal_alias_a1():
    for type_id, pat in (
        ("a2_equations_and_inequalities_multi_step_equations", "SolveLinear"),
        ("a2_equations_and_inequalities_literal_equations", "SolveLiteral"),
        ("a2_equations_and_inequalities_compound_inequalities", "CompoundInequality"),
    ):
        q = _q(type_id, 0.0)
        assert _pat(q) == pat, (type_id, _pat(q))


def test_a2_abs_ineq_linear_inner_at_high_d():
    for type_id in (
        "absolute_value_inequalities",
        "a2_equations_and_inequalities_absolute_value_inequalities",
    ):
        q0 = _q(type_id, 0.0, seed=101)
        assert _pat(q0) == "AbsInequality"
        assert _inner_a(q0) == 1
        hi = _q(type_id, 8.0, seed=207)
        assert _pat(hi) == "AbsInequality"
        assert _inner_a(hi) >= 2, (type_id, hi.prompt_latex, hi.metadata)


def test_a2_rational_skeleton_aliases():
    for type_id, pat in (
        ("a2_rational_expressions_simplifying", "SimplifyCancel"),
        ("a2_rational_expressions_adding_and_subtracting", "AddSubCancel"),
        ("a2_rational_expressions_multiplying_and_dividing", "MulDivCancel"),
        ("a2_rational_expressions_complex_fractions", "ComplexFracCancel"),
        ("a2_rational_expressions_equations", "EqCancel"),
    ):
        q = _q(type_id, 0.0)
        assert _pat(q) == pat, (type_id, _pat(q), q.prompt_latex)
        assert q.answer_latex


def test_a2_systems_skeleton_not_framework_dump():
    for type_id in (
        "a2_systems_of_equations_and_inequalities_solving_systems_by_elimination_2_variables",
        "a2_systems_of_equations_and_inequalities_solving_systems_by_substitution_2_variables",
    ):
        q = _q(type_id, 0.0)
        assert _pat(q) == "LinearSystem", (type_id, _pat(q))
        assert r"\begin{cases}" in (q.prompt_latex or "")


def test_a2_systems_wp_story_not_dump():
    for seed in range(12):
        q = _q(
            "a2_systems_of_equations_and_inequalities_systems_of_equations_word_problems_2_variables",
            0.0,
            seed=100 + seed,
        )
        prompt = (q.prompt_latex or "") + " " + (q.prompt_text or "")
        assert not looks_like_dumped_equation(prompt), prompt
        assert "costs satisfy" not in prompt.lower()
        assert _pat(q) == "SystemsWP"
        assert (q.metadata or {}).get("frame_id") in {"sys_number", "sys_tickets"}


def test_a2_work_drt_mixture_stamp_patterns():
    work = _q("a2_equations_and_inequalities_work_word_problems", 0.0)
    assert _pat(work) == "WorkWP"
    drt = _q("a2_equations_and_inequalities_distance_rate_time_word_problems", 0.0)
    assert _pat(drt) == "DistanceRateTime"
    mix = _q("a2_equations_and_inequalities_mixture_word_problems", 0.0)
    assert _pat(mix) == "MixtureWP"


def test_a2_variation_rotates_direct_and_inverse():
    frames: set[str] = set()
    kinds: set[str] = set()
    for seed in range(24):
        q = _q(
            "a2_direct_and_inverse_variation_direct_and_inverse_variation",
            0.0,
            seed=100 + seed,
        )
        assert _pat(q) == "VariationEq"
        meta = q.metadata or {}
        frames.add(str(meta.get("frame_id") or ""))
        kinds.add(str(meta.get("variation_kind") or ""))
        prompt = (q.prompt_latex or "").lower()
        assert "dump" not in prompt
    assert "direct" in kinds and "inverse" in kinds, kinds
    assert frames & {
        "var_direct_k",
        "var_direct_point",
        "var_direct_rate",
        "var_inverse_k",
        "var_inverse_point",
    }, frames


def test_a2_complex_and_three_var_stamps():
    ops = _q("a2_complex_numbers_operations", 0.0)
    assert _pat(ops) == "ComplexOp"
    assert re.search(r"[+\-]|\\left\(", ops.prompt_latex or "")
    mod = _q("a2_complex_numbers_absolute_value", 0.0)
    assert _pat(mod) == "ComplexAbs"
    rat = _q("a2_complex_numbers_rationalizing_denominators", 0.0)
    assert _pat(rat) == "ComplexRationalize"
    sys3 = _q(
        "a2_systems_of_equations_and_inequalities_solving_systems_with_three_variables",
        0.0,
    )
    assert _pat(sys3) == "LinearSystem3"
    assert "z" in (sys3.prompt_latex or "")
