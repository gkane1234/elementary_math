"""OpenStax family edit catalogs and limit/integral seed stamps."""

from question_engine.frameworks.primitives.openstax_edit_catalogs import (
    FAMILY_EDITS,
    catalog_rows,
    weighted_edit_id,
)
from question_engine.frameworks.primitives.limits import sample_limit_expression
from question_engine.frameworks.primitives.integrals import sample_integral_expression
import random


def test_family_catalogs_name_openstax_variation() -> None:
    rows = catalog_rows()
    ids = {row["action_id"] for row in rows}
    assert "sign" in ids
    assert "constant_multiple" in ids
    assert "omit_du_constant" in ids
    assert "factor_gcf" in ids
    assert "reroll_box_plot_stat" in ids
    assert all(row["evidence"] and row["weight"] > 0 for row in rows)
    assert set(FAMILY_EDITS) == {"limits", "integrals", "algebra", "figures"}


def test_weighted_limit_edit_is_stable() -> None:
    rng = random.Random(5)
    first = weighted_edit_id("limits", ["sign", "constant_multiple"], rng)
    rng = random.Random(5)
    second = weighted_edit_id("limits", ["sign", "constant_multiple"], rng)
    assert first == second
    assert first in {"sign", "constant_multiple"}


def test_unseeded_limits_stamp_seeds_and_vary() -> None:
    settings = {"difficulty": 8, "spec_difficulty": 0}
    samples = [
        sample_limit_expression(settings, generator_key="limit_direct_evaluation")
        for _ in range(6)
    ]
    assert len({s.prompt_latex for s in samples}) >= 2
    assert all("structure_seed" in s.metadata for s in samples)
    first = samples[0]
    replay = sample_limit_expression(
        {
            "difficulty": 8,
            "spec_difficulty": 0,
            "structure_seed": first.metadata["structure_seed"],
            "number_seed": first.metadata["number_seed"],
            "edit_seed": first.metadata["edit_seed"],
        },
        generator_key="limit_direct_evaluation",
    )
    assert replay.prompt_latex == first.prompt_latex


def test_unseeded_power_integral_stamps_seeds() -> None:
    sample = sample_integral_expression(
        {"difficulty": 6},
        generator_key="integral_power_rule",
    )
    assert "structure_seed" in sample.metadata
    assert "edit_seed" in sample.metadata
