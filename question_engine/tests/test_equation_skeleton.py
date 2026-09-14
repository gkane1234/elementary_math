"""Tests for SolveLinear equation skeleton."""

from __future__ import annotations

import re

from question_engine.api.handler import _generate_for_type
from question_engine.frameworks.primitives import (
    PRIM_EQUATIONS,
    PRIM_INEQUALITIES,
    PRIM_NUMBERS,
    PRIM_VARIABLE,
    build_context,
)
from question_engine.frameworks.primitives.equation_skeleton import (
    generate_solve_linear_question,
    knobs_from_form_id,
    sample_solve_linear,
    solve_linear_knobs,
    use_solve_linear_skeleton,
)
from question_engine.frameworks.primitives.expression_policy import LINEAR_POLICY
from question_engine.generators.primitive_g6 import (
    multi_step_equations,
    one_step_equations,
    two_step_equations,
)


def _ctx(d: float, seed: int, *, force: str = "multi", extra: dict | None = None):
    settings = {
        "difficulty": d,
        "seed": seed,
        "integers_only": True,
        "only_x": True,
        "lock_variable": "x",
        "force_steps": force,
        **(extra or {}),
    }
    return build_context(
        settings,
        [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_EQUATIONS],
        policy=LINEAR_POLICY,
        leaf_id={
            "one": "one_step_equations",
            "two": "two_step_equations",
            "multi": "multi_step_equations",
        }[force],
    )


def _ints(latex: str) -> list[int]:
    return [int(n) for n in re.findall(r"\d+", latex or "")]


def _var_sides(latex: str, var: str = "x") -> tuple[bool, bool]:
    parts = (latex or "").split("=")
    if len(parts) != 2:
        return False, False
    left, right = parts[0], parts[1]
    return (var in left, var in right)


def test_knobs_from_form_ids():
    assert knobs_from_form_id("one_step_add_sub")["species"] == "one"
    assert knobs_from_form_id("one_step_mul_div")["ops"] == ("mul", "div")
    assert knobs_from_form_id("two_step")["species"] == "two"
    assert knobs_from_form_id("vars_both_sides")["require_both_sides"] is True
    assert knobs_from_form_id("multi_step_distribute")["require_distribute"] is True


def test_numeric_before_format_for_multi():
    k0 = solve_linear_knobs(0.0, "multi")
    k8 = solve_linear_knobs(8.0, "multi")
    k16 = solve_linear_knobs(16.0, "multi")
    assert k0.numeric_tier == 0 and k0.format_tier == 0
    assert k8.numeric_tier >= 1 and k8.format_tier == 0
    assert k8.addend_hi > k0.addend_hi
    assert k16.format_tier >= 2
    assert k0.allow_nested is False
    assert k8.allow_nested is False


def test_use_solve_linear_default_and_opt_out():
    assert use_solve_linear_skeleton({}) is True
    assert use_solve_linear_skeleton({"use_sample_linear_equation": True}) is False
    assert use_solve_linear_skeleton({"use_solve_linear_skeleton": False}) is False
    assert use_solve_linear_skeleton({"skeleton_pattern": "equations"}) is False


def test_one_step_is_one_op():
    for d in (0.0, 8.0, 16.0):
        for seed in range(12):
            item = sample_solve_linear(_ctx(d, seed, force="one"), force_steps="one")
            assert item.steps == "one"
            assert item.n_ops == 1
            left, right = item.latex.split("=")
            left_var, right_var = _var_sides(item.latex)
            assert left_var is True
            assert right_var is False
            # One op: either ax=b (no +/− on left besides leading minus) or x±a=b.
            assert item.metadata.get("skeleton_pattern") == "SolveLinear"
            assert item.form_id in {"one_step_add_sub", "one_step_mul_div"}


def test_two_step_is_ax_plus_b():
    for d in (0.0, 8.0, 16.0):
        for seed in range(10):
            item = sample_solve_linear(_ctx(d, seed, force="two"), force_steps="two")
            assert item.steps == "two"
            assert item.n_ops == 2
            left_var, right_var = _var_sides(item.latex)
            assert left_var is True
            assert right_var is False
            assert "(" not in item.latex and "\\left(" not in item.latex
            assert item.form_id == "two_step"


def test_multi_d0_is_simple():
    seen_dist = 0
    seen_both = 0
    for seed in range(48):
        item = sample_solve_linear(_ctx(0.0, seed, force="multi"), force_steps="multi")
        assert item.steps == "multi"
        assert item.metadata.get("skeleton_pattern") == "SolveLinear"
        assert item.n_ops <= 3
        assert "\\frac" not in item.latex
        nums = _ints(item.latex)
        assert nums, item.latex
        assert max(nums) <= 40, item.latex
        paren = item.latex.count("(") + item.latex.count("\\left(")
        left_var, right_var = _var_sides(item.latex)
        if paren:
            seen_dist += 1
            assert paren == 1, item.latex
            assert right_var is False, item.latex
            assert item.form_id == "multi_step_distribute"
        else:
            seen_both += 1
            assert left_var and right_var, item.latex
            assert item.form_id == "vars_both_sides"
        # Not nested + both sides at once.
        assert not (paren >= 1 and right_var)
    assert seen_dist >= 10, seen_dist
    assert seen_both >= 10, seen_both


def test_multi_high_d_can_combine_formats():
    rich = 0
    for seed in range(30):
        item = sample_solve_linear(_ctx(16.0, seed, force="multi"), force_steps="multi")
        assert item.steps == "multi"
        paren = item.latex.count("(") + item.latex.count("\\left(")
        _lv, right_var = _var_sides(item.latex)
        if paren >= 1 and right_var:
            rich += 1
        assert item.metadata.get("skeleton_pattern") == "SolveLinear"
    assert rich >= 4, rich


def test_generators_default_to_solve_linear():
    for fn, tid, steps in (
        (one_step_equations, "one_step_equations", "one"),
        (two_step_equations, "two_step_equations", "two"),
        (multi_step_equations, "multi_step_equations", "multi"),
    ):
        qs = fn(
            tid,
            {
                "difficulty": 4,
                "count": 3,
                "seed": 11,
                "include_answer_key": True,
                "integers_only": True,
                "only_x": True,
            },
        )
        assert qs
        for q in qs:
            assert q.metadata.get("skeleton_pattern") == "SolveLinear"
            assert q.metadata.get("primitive_engine") == "equation_skeleton"
            assert q.metadata.get("steps") == steps
            assert q.answer_latex

    qs_old = multi_step_equations(
        "multi_step_equations",
        {
            "difficulty": 4,
            "count": 2,
            "seed": 11,
            "include_answer_key": True,
            "use_sample_linear_equation": True,
        },
    )
    assert qs_old[0].metadata.get("primitive_engine") == "equations"
    assert qs_old[0].metadata.get("skeleton_pattern") != "SolveLinear"


def test_live_generate_smoke():
    for tid, pat_steps in (
        ("one_step_equations", "one"),
        ("two_step_equations", "two"),
        ("multi_step_equations", "multi"),
        ("pa_equations_multi_step_equations", "multi"),
    ):
        qs = _generate_for_type(
            tid,
            {
                "difficulty": 0,
                "count": 1,
                "seed": 42,
                "include_answer_key": True,
                "integers_only": True,
                "only_x": True,
            },
        )
        meta = qs[0].metadata or {}
        assert meta.get("skeleton_pattern") == "SolveLinear"
        assert meta.get("steps") == pat_steps
        assert qs[0].prompt_latex
        assert qs[0].answer_latex


def test_demo_api_and_forced_form():
    r = generate_solve_linear_question(
        {"difficulty": 0, "seed": 1, "form_id": "multi_step_distribute", "integers_only": True},
        force_steps="multi",
        leaf_id="multi_step_equations",
    )
    assert r.metadata.get("skeleton_pattern") == "SolveLinear"
    assert r.form_id == "multi_step_distribute"
    assert "(" in r.latex or "\\left(" in r.latex


def test_aliases_use_skeleton():
    for tid in (
        "a2_equations_and_inequalities_multi_step_equations",
        "geo_review_multi_step_equations",
    ):
        qs = _generate_for_type(
            tid,
            {"difficulty": 2, "count": 1, "seed": 7, "include_answer_key": True},
        )
        assert qs[0].metadata.get("skeleton_pattern") == "SolveLinear"


def _ineq_ctx(d: float, seed: int, *, force: str = "one", extra: dict | None = None):
    settings = {
        "difficulty": d,
        "seed": seed,
        "integers_only": True,
        "only_x": True,
        "lock_variable": "x",
        "force_steps": force,
        **(extra or {}),
    }
    leaf = {
        "one": "one_step_inequalities",
        "two": "two_step_inequalities",
        "multi": "multi_step_inequalities",
    }[force]
    return build_context(
        settings,
        [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_INEQUALITIES],
        policy=LINEAR_POLICY,
        leaf_id=leaf,
    )


def _rel_sides(latex: str, var: str = "x") -> tuple[bool, bool]:
    for sep in ("\\le", "\\ge", "\\leq", "\\geq", "<", ">"):
        if sep in latex:
            left, right = latex.split(sep, 1)
            return (var in left, var in right)
    return _var_sides(latex, var)


def test_use_inequality_and_literal_opt_out():
    from question_engine.frameworks.primitives.equation_skeleton import (
        use_solve_inequality_skeleton,
        use_solve_literal_skeleton,
    )

    assert use_solve_inequality_skeleton({}) is True
    assert use_solve_inequality_skeleton({"use_sample_linear_inequality": True}) is False
    assert use_solve_literal_skeleton({}) is True
    assert use_solve_literal_skeleton({"use_sample_literal_equation": True}) is False


def test_one_step_inequality_is_one_op():
    from question_engine.frameworks.primitives.equation_skeleton import (
        sample_solve_inequality,
    )

    for d in (0.0, 8.0, 16.0):
        for seed in range(12):
            item = sample_solve_inequality(_ineq_ctx(d, seed, force="one"), force_steps="one")
            assert item.steps == "one"
            assert item.n_ops == 1
            left_var, right_var = _rel_sides(item.latex)
            assert left_var is True
            assert right_var is False
            assert item.metadata.get("skeleton_pattern") == "SolveInequality"
            assert item.form_id in {"one_step_ineq_add_sub", "one_step_ineq_mul_div"}
            assert item.op in {"<", ">", "\\le", "\\ge"}
            assert item.op in item.solution_latex


def test_inequality_d0_no_flip():
    from question_engine.frameworks.primitives.equation_skeleton import (
        sample_solve_inequality,
    )

    for force in ("one", "two", "multi"):
        for seed in range(24):
            item = sample_solve_inequality(
                _ineq_ctx(0.0, seed, force=force), force_steps=force
            )
            assert item.flipped is False, item.latex
            assert item.leading > 0, (item.latex, item.leading)
            assert item.op == item.relation


def test_multi_inequality_d0_is_simple():
    from question_engine.frameworks.primitives.equation_skeleton import (
        sample_solve_inequality,
    )

    seen_dist = 0
    seen_both = 0
    for seed in range(48):
        item = sample_solve_inequality(
            _ineq_ctx(0.0, seed, force="multi"), force_steps="multi"
        )
        assert item.steps == "multi"
        assert item.n_ops <= 3
        assert "\\frac" not in item.latex
        nums = _ints(item.latex)
        assert nums and max(nums) <= 40, item.latex
        paren = item.latex.count("(") + item.latex.count("\\left(")
        left_var, right_var = _rel_sides(item.latex)
        if paren:
            seen_dist += 1
            assert paren == 1, item.latex
            assert right_var is False, item.latex
            assert item.form_id == "multi_step_ineq_distribute"
        else:
            seen_both += 1
            assert left_var and right_var, item.latex
            assert item.form_id == "vars_both_sides_ineq"
        assert not (paren >= 1 and right_var)
    assert seen_dist >= 10, seen_dist
    assert seen_both >= 10, seen_both


def test_negative_multiply_flips_inequality():
    from question_engine.frameworks.primitives.equation_skeleton import (
        sample_solve_inequality,
        _flip_op,
    )

    found = 0
    for seed in range(40):
        item = sample_solve_inequality(
            _ineq_ctx(
                8.0,
                seed,
                force="one",
                extra={"force_negative_coeff": True},
            ),
            force_steps="one",
        )
        if item.leading >= 0:
            continue
        found += 1
        assert item.flipped is True, item.latex
        assert item.relation == _flip_op(item.op), (item.latex, item.relation, item.op)
        assert item.op in item.solution_latex
        assert item.relation in item.latex
    assert found >= 8, found


def test_inequality_generators_default_and_opt_out():
    from question_engine.generators.primitive_g6 import (
        multi_step_inequalities,
        one_step_inequalities,
        two_step_inequalities,
    )

    for fn, tid, steps in (
        (one_step_inequalities, "one_step_inequalities", "one"),
        (two_step_inequalities, "two_step_inequalities", "two"),
        (multi_step_inequalities, "multi_step_inequalities", "multi"),
    ):
        qs = fn(
            tid,
            {
                "difficulty": 4,
                "count": 3,
                "seed": 11,
                "include_answer_key": True,
                "integers_only": True,
                "only_x": True,
            },
        )
        assert qs
        for q in qs:
            assert q.metadata.get("skeleton_pattern") == "SolveInequality"
            assert q.metadata.get("primitive_engine") == "equation_skeleton"
            assert q.metadata.get("steps") == steps
            assert q.answer_latex
            assert q.metadata.get("number_line_spec")

    qs_old = multi_step_inequalities(
        "multi_step_inequalities",
        {
            "difficulty": 4,
            "count": 2,
            "seed": 11,
            "include_answer_key": True,
            "use_sample_linear_inequality": True,
        },
    )
    assert qs_old[0].metadata.get("primitive_engine") == "inequalities"
    assert qs_old[0].metadata.get("skeleton_pattern") != "SolveInequality"


def test_live_inequality_and_literal_generate_smoke():
    for tid, pat, steps in (
        ("one_step_inequalities", "SolveInequality", "one"),
        ("two_step_inequalities", "SolveInequality", "two"),
        ("multi_step_inequalities", "SolveInequality", "multi"),
        ("pa_multi_step_inequalities", "SolveInequality", "multi"),
        ("g6_solving_and_graphing_one_step_inequalities", "SolveInequality", "one"),
        ("literal_equations", "SolveLiteral", None),
        ("a2_equations_and_inequalities_literal_equations", "SolveLiteral", None),
    ):
        qs = _generate_for_type(
            tid,
            {
                "difficulty": 0,
                "count": 1,
                "seed": 42,
                "include_answer_key": True,
                "integers_only": True,
                "only_x": True,
            },
        )
        meta = qs[0].metadata or {}
        assert meta.get("skeleton_pattern") == pat, (tid, meta.get("skeleton_pattern"))
        if steps:
            assert meta.get("steps") == steps
        assert qs[0].prompt_latex
        assert qs[0].answer_latex


def test_literal_d0_is_one_step():
    from question_engine.frameworks.primitives.equation_skeleton import (
        sample_solve_literal,
    )

    for seed in range(20):
        ctx = build_context(
            {
                "difficulty": 0,
                "seed": seed,
                "integers_only": True,
            },
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_EQUATIONS],
            policy=LINEAR_POLICY,
            leaf_id="literal_equations",
        )
        item = sample_solve_literal(ctx)
        assert item.n_ops == 1, item.latex
        assert item.form_id == "literal_equation"
        assert item.metadata.get("skeleton_pattern") == "SolveLiteral"
        assert item.metadata.get("literal_shape") in {"product2", "circ"}
        assert "(" not in item.latex.split("\\quad")[0]


def test_literal_high_d_unlocks_format():
    from question_engine.frameworks.primitives.equation_skeleton import (
        sample_solve_literal,
    )

    shapes = set()
    ops = set()
    for seed in range(24):
        ctx = build_context(
            {
                "difficulty": 16,
                "seed": seed,
                "integers_only": True,
            },
            [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_EQUATIONS],
            policy=LINEAR_POLICY,
            leaf_id="literal_equations",
        )
        item = sample_solve_literal(ctx)
        shapes.add(item.metadata.get("literal_shape"))
        ops.add(item.n_ops)
        assert item.form_id == "literal_equation"
    assert ops & {2}, ops
    assert shapes & {"perimeter", "slope_x", "linear_two"}


def test_literal_opt_out():
    from question_engine.generators.primitive_linear import literal_equations

    qs = literal_equations(
        "literal_equations",
        {
            "difficulty": 4,
            "count": 1,
            "seed": 3,
            "include_answer_key": True,
            "use_sample_literal_equation": True,
        },
    )
    assert qs[0].metadata.get("primitive_engine") == "literal_equations"
    assert qs[0].metadata.get("skeleton_pattern") != "SolveLiteral"
