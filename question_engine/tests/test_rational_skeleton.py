"""Tests for AddSubCancel inflate/package invariants + factor_sampler constraints."""

from __future__ import annotations

from fractions import Fraction

import pytest

from question_engine.frameworks.primitives import PRIM_NUMBERS, PRIM_VARIABLE, build_context
from question_engine.frameworks.primitives.expression_policy import POLYNOMIAL_POLICY_DEFAULT
from question_engine.frameworks.primitives.factor_sampler import (
    FactorConstraints,
    constraints_from_settings,
    sample_factor_product,
    sample_linear_factor,
)
from question_engine.frameworks.primitives.poly_helpers import poly_degree
from question_engine.frameworks.primitives.rational_skeleton import (
    MAX_CANCEL_K,
    MAX_DEN_DEGREE,
    ResidualKernel,
    clear_factor_from_coeffs,
    clear_fractional_package,
    generate_add_sub_cancel_question,
    package_with_kernel,
    pfd_atomic_coeffs,
    sample_add_sub_cancel,
    sample_residual_kernel,
    verify_packaged_equals_r,
)


def _ctx(seed: int = 0, d: float = 5.0, **extra):
    settings = {"difficulty": d, "seed": seed, "factor_rrt": False, **extra}
    return build_context(
        settings,
        [PRIM_NUMBERS, PRIM_VARIABLE],
        policy=POLYNOMIAL_POLICY_DEFAULT,
        leaf_id="rational_expression_simplification",
    )


def test_factor_constraints_honor_monic_box():
    cons = FactorConstraints(
        min_factors=2,
        max_factors=2,
        allow_nonmonic=False,
        leading_max=1,
        const_min=-3,
        const_max=3,
    ).clamped()
    ctx = _ctx(1, d=20.0)  # high D but box forbids nonmonic
    draw = sample_factor_product(ctx, n_factors=2, constraints=cons, d=20.0)
    assert all(f.is_monic() for f in draw.factors)
    assert draw.degree <= MAX_DEN_DEGREE


def test_factor_sampler_d_bias_widens_nonmonic_weight():
    low = constraints_from_settings({}, d=2.0)
    high = constraints_from_settings({"allow_nonmonic": True}, d=16.0)
    assert low.nonmonic_weight < high.nonmonic_weight
    assert high.allow_nonmonic


def test_cancel_count_capped_at_two():
    from question_engine.frameworks.primitives.rational_skeleton import (
        MAX_CANCEL_K,
        rational_skeleton_caps,
    )

    for seed in range(12):
        r = generate_add_sub_cancel_question(
            {"difficulty": 4.0, "seed": seed, "n_factors": 2}
        )
        caps = rational_skeleton_caps(4.0)
        assert 0 <= r.cancel_count <= caps.max_cancel_k
        assert poly_degree(r.r_den) <= caps.max_inventory_factors
    for seed in range(8):
        r = generate_add_sub_cancel_question(
            {"difficulty": 22.0, "seed": seed, "n_factors": 3}
        )
        caps = rational_skeleton_caps(22.0)
        assert 0 <= r.cancel_count <= caps.max_cancel_k
        assert poly_degree(r.r_den) <= caps.max_inventory_factors
        assert len(r.remain_factors) <= caps.max_answer_den_degree


def test_inflate_package_recombine_invariant():
    for seed in range(20):
        r = generate_add_sub_cancel_question(
            {
                "difficulty": 8.0,
                "seed": seed,
                "n_factors": 2,
                "cancel_factor_count": seed % 3,
            }
        )
        assert verify_packaged_equals_r(list(r.terms), r.r_num, r.factors.factors)


def test_kernel_zero_and_nonzero_modes():
    ctx = _ctx(3, d=10.0)
    z = sample_residual_kernel(
        ctx, d=10.0, den_degree=2, cancel_count=0, force_mode="zero"
    )
    assert z.is_zero and z.dim == 0

    c = sample_residual_kernel(
        ctx, d=10.0, den_degree=2, cancel_count=0, force_mode="constant"
    )
    assert not c.is_zero and c.b == 0 and c.dim == 1

    full = sample_residual_kernel(
        ctx, d=10.0, den_degree=2, cancel_count=0, force_mode="full"
    )
    assert full.a != 0 and full.b != 0 and full.dim == 2

    a0 = sample_residual_kernel(
        ctx, d=10.0, den_degree=2, cancel_count=0, force_mode="a0"
    )
    assert a0.a == 0 and a0.b != 0


def test_kernel_package_rebalance_k_zero_and_2d():
    from question_engine.frameworks.primitives.factor_sampler import LinearFactor

    f1 = LinearFactor(a=Fraction(1), b=Fraction(-1))  # x-1
    f2 = LinearFactor(a=Fraction(1), b=Fraction(-2))  # x-2
    # R = 5(x-1)/((x-1)(x-2)) → goal 5/(x-2)
    r_num = {1: Fraction(5), 0: Fraction(-5)}

    _, terms0 = package_with_kernel(
        r_num=r_num, factors=(f1, f2), kernel=ResidualKernel()
    )
    assert verify_packaged_equals_r(terms0, r_num, (f1, f2))

    kern = ResidualKernel(a=Fraction(2), b=Fraction(-1))
    _, terms1 = package_with_kernel(r_num=r_num, factors=(f1, f2), kernel=kern)
    assert any(t.kind == "kernel" for t in terms1)
    assert verify_packaged_equals_r(terms1, r_num, (f1, f2))


def test_k_ge1_gets_visible_cancel_or_kernel():
    """With cancels, package should include kernel (so cancel dens can appear)."""
    r = generate_add_sub_cancel_question(
        {
            "difficulty": 5.0,
            "seed": 7,
            "n_factors": 2,
            "cancel_factor_count": 1,
            "kernel_mode": "constant",
        }
    )
    assert r.cancel_count == 1
    assert not r.kernel.is_zero
    assert r.package_mode == "residual"


def test_full_cancel_constant_goal():
    r = generate_add_sub_cancel_question(
        {
            "difficulty": 6.0,
            "seed": 11,
            "n_factors": 2,
            "cancel_factor_count": 2,
            "kernel_mode": "constant",
        }
    )
    assert r.goal_mode == "constant"
    assert r.cancel_count == 2
    assert len(r.remain_factors) == 0


def test_pfd_atomic_distinct_linears():
    from question_engine.frameworks.primitives.factor_sampler import LinearFactor

    f1 = LinearFactor(Fraction(1), Fraction(-1))
    f2 = LinearFactor(Fraction(1), Fraction(-3))
    # 1/((x-1)(x-3)) → A=1/(1-3)=-1/2 at r=1; B=1/(3-1)=1/2
    num = {0: Fraction(1)}
    A, B = pfd_atomic_coeffs(num, (f1, f2))
    assert A == Fraction(-1, 2)
    assert B == Fraction(1, 2)


def test_clear_factor_lcm_of_denominators():
    assert clear_factor_from_coeffs(Fraction(1, 2), Fraction(1, 3)) == 6
    assert clear_factor_from_coeffs(Fraction(3), Fraction(-2)) == 1
    assert clear_factor_from_coeffs(Fraction(0), Fraction(5, 4)) == 4


def test_clear_fractional_package_scales_to_integer_and_mg():
    """∑ (M aᵢ)/dᵢ = M R; goal becomes M·G (classroom clear-denominators)."""
    from question_engine.frameworks.primitives.factor_sampler import LinearFactor
    from question_engine.frameworks.primitives.rational_skeleton import PackagedTerm

    f1 = LinearFactor(Fraction(1), Fraction(-1))
    f2 = LinearFactor(Fraction(1), Fraction(-3))
    # Raw PF of 1/((x-1)(x-3)): -1/2, +1/2
    terms = [
        PackagedTerm(num={0: Fraction(-1, 2)}, den_factors=(f1,), kind="atomic"),
        PackagedTerm(num={0: Fraction(1, 2)}, den_factors=(f2,), kind="atomic"),
    ]
    r_num = {0: Fraction(1)}
    goal_num = {0: Fraction(1)}
    scaled_terms, scaled_r, scaled_goal, scaled_k, scaled_poly, m = (
        clear_fractional_package(
            terms,
            r_num=r_num,
            goal_num=goal_num,
            kernel=ResidualKernel(),
            poly_part={},
        )
    )
    assert m == 2
    assert all(
        all(c.denominator == 1 for c in t.num.values()) for t in scaled_terms
    )
    assert scaled_terms[0].num[0] == Fraction(-1)
    assert scaled_terms[1].num[0] == Fraction(1)
    assert scaled_r == {0: Fraction(2)}
    assert scaled_goal == {0: Fraction(2)}  # answer = M·G
    assert verify_packaged_equals_r(scaled_terms, scaled_r, (f1, f2))
    assert scaled_k.is_zero
    assert scaled_poly == {}


def test_sampler_clears_fractional_pf_numerators():
    """Live path: packaged atomic/kernel nums are integers; M tracked."""
    saw_m_gt1 = False
    for seed in range(40):
        r = generate_add_sub_cancel_question(
            {
                "difficulty": 8.0,
                "seed": seed,
                "n_factors": 2,
                "cancel_factor_count": 0,
                "kernel_mode": "zero",
                "allow_nonmonic": True,
            }
        )
        for t in r.terms:
            for c in t.num.values():
                assert Fraction(c).denominator == 1, (
                    f"seed={seed} fractional coeff {c} with M={r.clear_factor}"
                )
        assert r.clear_factor >= 1
        assert verify_packaged_equals_r(list(r.terms), r.r_num, r.factors.factors)
        if r.clear_factor > 1:
            saw_m_gt1 = True
            # Scaled goal = M · unscaled
            unscaled = r.goal_num_unscaled or {}
            for deg, c in r.goal_num.items():
                assert c == Fraction(unscaled.get(deg, 0)) * r.clear_factor
            assert "M*G" in (r.metadata.get("scaling_convention") or "")
            assert r.debug_dict().get("clear_factor") == r.clear_factor
    assert saw_m_gt1, "expected at least one sample needing clear factor M>1"


def test_low_d_kernel_often_zero_when_no_cancel():
    zeros = 0
    n = 40
    for seed in range(n):
        r = generate_add_sub_cancel_question(
            {
                "difficulty": 2.0,
                "seed": seed,
                "n_factors": 2,
                "cancel_factor_count": 0,
                "kernel_mode": None,  # auto — but settings key absent
            }
        )
        # Clear forced mode: regenerate via sample with no kernel_mode in settings
        ctx = _ctx(seed, d=2.0, cancel_factor_count=0, n_factors=2)
        r = sample_add_sub_cancel(ctx, cancel_count=0, n_factors=2)
        if r.kernel.is_zero:
            zeros += 1
    # Low D, k=0: majority should be K=0 (policy ~12% nonzero)
    assert zeros >= n // 2


def test_demo_api_and_default_generator():
    r = generate_add_sub_cancel_question({"difficulty": 7.0, "seed": 1})
    assert r.prompt_latex
    assert r.answer_latex
    assert "AddSubCancel" in r.metadata.get("skeleton_pattern", "")

    from question_engine.generators.primitive_rational import rational_add_subtract

    # Live default is AddSubCancel (no opt-in flag required).
    qs = rational_add_subtract(
        "rational_expressions_adding_and_subtracting",
        {
            "count": 1,
            "seed": 2,
            "difficulty": 6.0,
            "include_answer_key": True,
        },
    )
    assert len(qs) == 1
    assert qs[0].metadata.get("skeleton_pattern") == "AddSubCancel"
    assert qs[0].metadata.get("primitive_engine") == "rational_skeleton"
    assert "excluded_values" in qs[0].metadata

    # Explicit constructive opt-out still available.
    qs_old = rational_add_subtract(
        "rational_expressions_adding_and_subtracting",
        {
            "count": 1,
            "seed": 2,
            "difficulty": 6.0,
            "include_answer_key": True,
            "use_constructive_rational": True,
        },
    )
    assert qs_old[0].metadata.get("primitive_engine") == "constructive_rational"


def test_simplify_cancel_default_and_opt_out():
    from question_engine.frameworks.primitives.rational_skeleton import (
        generate_simplify_cancel_question,
    )
    from question_engine.generators.primitive_rational import rational_simplify

    r = generate_simplify_cancel_question(
        {"difficulty": 6.0, "seed": 3, "cancel_factor_count": 1, "n_factors": 2}
    )
    assert r.metadata.get("skeleton_pattern") == "SimplifyCancel"
    assert r.cancel_count == 1
    assert r"\neq" in r.answer_latex

    qs = rational_simplify(
        "rational_simplification",
        {
            "count": 1,
            "seed": 4,
            "difficulty": 6.0,
            "include_answer_key": True,
            "cancel_factor_count": 1,
            "n_factors": 2,
        },
    )
    assert qs[0].metadata.get("skeleton_pattern") == "SimplifyCancel"
    assert qs[0].metadata.get("primitive_engine") == "rational_skeleton"

    qs_old = rational_simplify(
        "rational_simplification",
        {
            "count": 1,
            "seed": 4,
            "difficulty": 6.0,
            "include_answer_key": True,
            "use_constructive_rational": True,
            "cancel_factor_count": 1,
        },
    )
    assert qs_old[0].metadata.get("primitive_engine") == "constructive_rational"


def test_mul_div_cancel_default_and_exclusions():
    from question_engine.frameworks.primitives.rational_skeleton import (
        generate_mul_div_cancel_question,
    )
    from question_engine.generators.rational_multiply_divide import (
        generate_rational_expression_multiply_divide,
    )

    r = generate_mul_div_cancel_question(
        {
            "difficulty": 6.0,
            "seed": 5,
            "cancel_factor_count": 1,
            "allow_divide": False,
        }
    )
    assert r.metadata.get("skeleton_pattern") == "MulDivCancel"
    assert r.operation == "multiply"
    assert len(r.remain_den_factors) <= MAX_DEN_DEGREE
    assert r.cancel_count == 1
    assert len(r.metadata.get("excluded_values") or []) == 1

    qs = generate_rational_expression_multiply_divide(
        "rational_expression_multiply_divide",
        {
            "count": 1,
            "seed": 6,
            "difficulty": 5.0,
            "include_answer_key": True,
            "operand_count": 2,
            "allow_divide": False,
            "cancel_factor_count": 1,
        },
    )
    assert qs[0].metadata.get("skeleton_pattern") == "MulDivCancel"
    assert qs[0].metadata.get("primitive_engine") == "rational_skeleton"


def test_complex_frac_cancel_stamps_display_intent():
    from question_engine.frameworks.primitives.rational_skeleton import (
        generate_complex_frac_cancel_question,
    )
    from question_engine.generators.complex_fractions import generate_complex_fractions

    r = generate_complex_frac_cancel_question({"difficulty": 3.0, "seed": 8})
    assert r.metadata.get("skeleton_pattern") == "ComplexFracCancel"
    assert r.metadata.get("display_intent") == "complex_fraction_skill"
    assert r.cancel_count >= 1
    assert r"\neq" in r.answer_latex

    qs = generate_complex_fractions(
        "complex_fractions",
        {"count": 2, "difficulty": 5, "seed": 9, "include_answer_key": True},
    )
    assert qs
    for q in qs:
        assert q.metadata.get("skeleton_pattern") == "ComplexFracCancel"
        assert q.metadata.get("display_intent") == "complex_fraction_skill"
        assert q.metadata.get("primitive_engine") == "rational_skeleton"


def test_exclusions_are_cancelled_roots_only():
    """x≠ notes list removable holes only — not poles left in the final den."""
    # Partial cancel: one cancelled root must appear; remain root must not.
    r = generate_add_sub_cancel_question(
        {
            "difficulty": 5.0,
            "seed": 103,
            "n_factors": 2,
            "cancel_factor_count": 1,
            "kernel_mode": "constant",
            "allow_nonmonic": False,
        }
    )
    assert r.cancel_count == 1
    assert len(r.cancel_factors) == 1
    assert len(r.remain_factors) == 1
    cancel_root = r.cancel_factors[0].root()
    remain_root = r.remain_factors[0].root()
    excl = r.metadata.get("excluded_values") or []
    expected = (
        [int(cancel_root)]
        if cancel_root.denominator == 1
        else [f"{cancel_root.numerator}/{cancel_root.denominator}"]
    )
    assert excl == expected
    # Remain pole must not be in the exclusion metadata / note list.
    remain_meta = (
        int(remain_root)
        if remain_root.denominator == 1
        else f"{remain_root.numerator}/{remain_root.denominator}"
    )
    assert remain_meta not in excl
    assert r"\neq" in r.answer_latex
    # Final-den factor still appears in the simplified fraction (before the note).
    goal_part = r.answer_latex.split(",")[0]
    assert "neq" not in goal_part
    # Cancel root appears after ≠; remain root does not (as a listed exclusion).
    note = r.answer_latex.split(r"\neq", 1)[1]
    from question_engine.frameworks.primitives._algebra_render import num_latex

    assert num_latex(cancel_root) in note
    # Listed exclusions are comma-separated; remain must not be one of them.
    listed = [p.strip() for p in note.replace(r"\;", "").split(",")]
    assert num_latex(remain_root) not in listed


def test_exclusions_empty_when_no_cancel():
    """k=0: all original poles remain in the final den → no x≠ note."""
    r = generate_add_sub_cancel_question(
        {
            "difficulty": 4.0,
            "seed": 5,
            "n_factors": 2,
            "cancel_factor_count": 0,
            "kernel_mode": "zero",
        }
    )
    assert r.cancel_count == 0
    assert (r.metadata.get("excluded_values") or []) == []
    assert r"\neq" not in r.answer_latex


def test_exclusions_all_roots_on_full_cancel():
    """Full cancel → constant goal; every original den root is a removable hole."""
    r = generate_add_sub_cancel_question(
        {
            "difficulty": 6.0,
            "seed": 11,
            "n_factors": 2,
            "cancel_factor_count": 2,
            "kernel_mode": "constant",
        }
    )
    assert r.goal_mode == "constant"
    assert r.cancel_count == 2
    cancel_roots = {f.root() for f in r.cancel_factors}
    excl = r.metadata.get("excluded_values") or []
    assert len(excl) == len(cancel_roots)
    assert r"\neq" in r.answer_latex
