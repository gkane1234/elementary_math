"""Expression-edit catalog: weights, cleaning, and unseeded derivative variety."""

from __future__ import annotations

import random

from question_engine.frameworks.difficulty_budget import (
    edit_cap_from_difficulty,
    resolve_edit_cap,
)
from question_engine.frameworks.primitives.expression_edits import (
    EDIT_CATALOG,
    apply_expression_edits,
    clean_adjacent_constants,
    catalog_rows,
)
from question_engine.frameworks.primitives.poly_expression import (
    Add,
    Const,
    Fn,
    Mul,
    Var,
    render_latex,
)
from question_engine.frameworks.primitives.derivatives import sample_derivative_expression


def _sum(coef: int, const: int, var: str = "x"):
    return Add((Mul((Const(coef), Var(var))), Const(const)))


def test_catalog_weights_are_readable_and_wraps_are_rare() -> None:
    rows = catalog_rows()
    assert [row["action_id"] for row in rows] == [action.action_id for action in EDIT_CATALOG]
    by_id = {row["action_id"]: row for row in rows}
    assert by_id["factor_common_sum"]["weight"] > by_id["reciprocal_exp_wrap"]["weight"]
    assert by_id["reciprocal_exp_wrap"]["kind"] == "wrap"
    assert "3x+3" in by_id["factor_common_sum"]["summary"]
    assert all(row["weight"] > 0 for row in rows)


def test_clean_folds_adjacent_constants_of_a_sum() -> None:
    expr = Mul((Const(2), Mul((Const(3), Add((Var("x"), Const(1)))))))
    cleaned = clean_adjacent_constants(expr)
    latex = render_latex(cleaned)
    assert "6" in latex
    assert "x" in latex
    assert "2" not in latex.replace("6", "")


def test_clean_does_not_distribute_a_factor_across_a_sum() -> None:
    inner = _sum(3, 3)
    expr = Fn("exp", Mul((Const(2), inner)))
    cleaned = clean_adjacent_constants(expr)
    latex = render_latex(cleaned)
    assert r"e^{" in latex
    assert "2" in latex
    assert "3x" in latex
    assert "6x" not in latex


def test_factor_common_sum_and_not_a_bare_coefficient() -> None:
    expr = Fn("exp", _sum(3, 3))
    edited, meta = apply_expression_edits(
        expr,
        random.Random(1),
        cap=1,
        coef_abs_max=4,
    )
    # Force the factor action by applying it through a seed search.
    found = None
    for seed in range(80):
        edited, meta = apply_expression_edits(
            expr,
            random.Random(seed),
            cap=1,
            coef_abs_max=4,
        )
        ids = [row["action_id"] for row in meta["edits_applied"]]
        if ids == ["factor_common_sum"]:
            found = render_latex(edited)
            break
    assert found is not None
    assert "3" in found
    assert "x + 1" in found or "x+1" in found.replace(" ", "")

    bare = Mul((Const(6), Var("x")))
    _edited, bare_meta = apply_expression_edits(
        bare,
        random.Random(0),
        cap=3,
        coef_abs_max=5,
    )
    assert all(row["action_id"] != "factor_common_sum" for row in bare_meta["edits_applied"])


def test_one_wrap_and_edit_cap_staircase() -> None:
    assert edit_cap_from_difficulty(0) == 0
    assert edit_cap_from_difficulty(4) == 1
    assert edit_cap_from_difficulty(6) == 2
    assert edit_cap_from_difficulty(12) == 3
    assert resolve_edit_cap({"difficulty": 6, "edit_max": 0}) == 0
    assert resolve_edit_cap({"difficulty": 6, "edit_max": 3}) == 2

    expr = Fn("exp", _sum(3, 3))
    wraps = 0
    for seed in range(40):
        _edited, meta = apply_expression_edits(
            expr,
            random.Random(seed),
            cap=3,
            coef_abs_max=4,
        )
        kinds = [row["kind"] for row in meta["edits_applied"]]
        assert kinds.count("wrap") <= 1
        wraps += kinds.count("wrap")
    assert wraps >= 1


def test_unseeded_quotient_draws_are_not_identical() -> None:
    settings = {
        "difficulty": 6,
        "conceptual_difficulty": 6,
        "spec_difficulty": 0,
        "edit_max": 3,
    }
    prompts = [
        sample_derivative_expression(
            settings, generator_key="derivative_quotient_rule"
        ).prompt_latex
        for _ in range(10)
    ]
    assert len(set(prompts)) >= 2


def test_seeded_derivative_replays_from_stamped_seeds() -> None:
    settings = {
        "difficulty": 6,
        "conceptual_difficulty": 6,
        "spec_difficulty": 0,
        "seed": 17,
    }
    first = sample_derivative_expression(
        settings, generator_key="derivative_quotient_rule"
    )
    second = sample_derivative_expression(
        settings, generator_key="derivative_quotient_rule"
    )
    assert first.prompt_latex == second.prompt_latex
    replay = sample_derivative_expression(
        {
            "difficulty": 6,
            "conceptual_difficulty": 6,
            "spec_difficulty": 0,
            "structure_seed": first.metadata["structure_seed"],
            "number_seed": first.metadata["number_seed"],
            "edit_seed": first.metadata["edit_seed"],
        },
        generator_key="derivative_quotient_rule",
    )
    assert replay.prompt_latex == first.prompt_latex
    assert replay.answer_latex == first.answer_latex
    assert "structure_pool_size" in first.metadata
