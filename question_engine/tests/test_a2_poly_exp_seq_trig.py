"""A2 poly-only / exp-log / sequences / trig wiring (non-graph)."""

from __future__ import annotations

import re

import pytest

from question_engine.api.handler import _generate_for_type
from question_engine.generators import GENERATORS


def _one(type_id: str, *, d: float = 0.0, seed: int = 101) -> dict:
    qs = _generate_for_type(
        type_id,
        {
            "difficulty": d,
            "seed": seed,
            "count": 1,
            "include_answer_key": True,
        },
    )
    q = qs[0]
    meta = dict(q.metadata or {})
    return {
        "prompt": q.prompt_latex or q.prompt_text or "",
        "answer": q.answer_latex or "",
        "pattern": meta.get("skeleton_pattern") or "",
        "meta": meta,
    }


@pytest.mark.parametrize(
    "type_id,pattern",
    [
        ("a2_polynomial_functions_the_binomial_theorem", "BinomialTheorem"),
        ("a2_polynomial_functions_the_remainder_theorem", "RemainderTheorem"),
        ("a2_polynomial_functions_conjugate_roots_and_writing_functions", "ConjugateWrite"),
        ("a2_exponential_and_logarithmic_expressions_evaluating_logarithms", "LogEvaluate"),
        ("a2_sequences_and_series_arithmetic_sequences", "ArithSequence"),
        ("a2_sequences_and_series_geometric_sequences", "GeomSequence"),
        ("a2_trigonometry_trig_functions_of_any_angle", "TrigEvaluate"),
        ("a2_trigonometry_right_triangle_trig_finding_ratios", "RightTriRatio"),
        ("a2_trigonometry_the_law_of_sines", "LawOfSines"),
    ],
)
def test_a2_stamps_skeleton_pattern(type_id: str, pattern: str) -> None:
    row = _one(type_id)
    assert row["pattern"] == pattern


def test_a2_conjugate_factoring_is_factor_not_multiply() -> None:
    row = _one("a2_polynomial_functions_conjugate_roots_and_factoring", seed=101)
    assert row["pattern"] == "FactorProduct"
    assert row["meta"].get("task", "factor") == "factor"
    assert "multiply" not in str(row["meta"].get("method") or "")
    assert row["answer"]
    assert "(" in row["answer"]


def test_a2_cubes_and_quadratic_form_on_factor_product() -> None:
    cubes = _one("a2_polynomial_functions_factoring_sum_difference_of_cubes")
    assert cubes["pattern"] == "FactorProduct"
    assert re.search(r"x\^\{3\}|x\^3", cubes["prompt"])

    qf = _one("a2_polynomial_functions_factoring_quadratic_form")
    assert qf["pattern"] == "FactorProduct"
    assert re.search(r"x\^\{4\}|x\^4", qf["prompt"])


def test_a2_all_techniques_mixer() -> None:
    row = _one("a2_polynomial_functions_factoring_all_techniques", d=10.0, seed=207)
    assert row["pattern"] == "FactorProduct"
    assert row["meta"].get("mixer_pick") or row["meta"].get("form_id")


def test_a2_writing_linear_form_conversion_not_from_points() -> None:
    row = _one("a2_linear_relations_and_functions_writing_linear_equations")
    prompt = row["prompt"]
    assert "slope-intercept" in prompt.lower()
    assert "through" not in prompt.lower()
    assert row["answer"].startswith("y =")


def test_a2_writing_linear_differs_from_a1_at_same_seed() -> None:
    a2 = _one("a2_linear_relations_and_functions_writing_linear_equations", seed=101)
    a1 = _one("writing_linear_equations", seed=101)
    assert a2["prompt"] != a1["prompt"]


def test_primitive_a2_stamps_binomial() -> None:
    from question_engine.generators.advanced import GENERATORS as ADV

    assert GENERATORS["binomial_theorem"] is not ADV["binomial_theorem"]
    assert "a2_polynomial_functions_the_binomial_theorem" in GENERATORS


@pytest.mark.parametrize(
    "type_id",
    [
        "a2_polynomial_functions_factoring_sum_difference_of_cubes",
        "a2_polynomial_functions_factoring_quadratic_form",
        "a2_radical_functions_and_rational_exponents_simplifying_radicals",
    ],
)
def test_a2_thin_a1_aliases_generate(type_id: str) -> None:
    row = _one(type_id)
    assert row["prompt"]
    assert row["answer"]
