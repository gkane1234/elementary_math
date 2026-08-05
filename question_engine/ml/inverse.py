"""Inverse difficulty optimizer: g(type_id, target_effort) → θ*.

Uses a trained forward model and random search over controllable knobs
(primarily continuous ``difficulty`` plus optional domain bounds).
"""

from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Any

import numpy as np

from .forward import ForwardEffortModel
from .schema import GenerationRecord


@dataclass(frozen=True)
class InverseCandidate:
    theta: dict[str, Any]
    predicted_effort: float
    abs_error: float
    target_effort: float


# Knobs the optimizer is allowed to vary (schema-valid continuous / bounds).
_SEARCHABLE_FLOAT: tuple[tuple[str, float, float], ...] = (
    ("difficulty", 0.0, 25.0),
    ("ratio_part_min", 1.0, 8.0),
    ("ratio_part_max", 4.0, 40.0),
    ("num_min", 1.0, 20.0),
    ("num_max", 5.0, 80.0),
    ("denom_min", 2.0, 6.0),
    ("denom_max", 4.0, 24.0),
)


def _base_theta(type_id: str, seed: int | None = None) -> dict[str, Any]:
    theta: dict[str, Any] = {
        "type_id": type_id,
        "difficulty": 6.0,
        "count": 1,
        "include_answer_key": True,
    }
    if seed is not None:
        theta["seed"] = seed
    return theta


def _record_from_theta(type_id: str, theta: dict[str, Any]) -> GenerationRecord:
    """Synthetic record for model scoring (no live generation required)."""
    difficulty = None
    try:
        difficulty = float(theta.get("difficulty")) if theta.get("difficulty") is not None else None
    except (TypeError, ValueError):
        difficulty = None
    return GenerationRecord(
        type_id=type_id,
        seed=int(theta["seed"]) if theta.get("seed") is not None else None,
        difficulty=difficulty,
        theta_full=dict(theta),
        prompt_latex="",
        prompt_text="",
        answer_latex="",
        answer_text="",
        structural_features={},
        y_effort=None,
    )


def sample_theta(
    type_id: str,
    rng: np.random.Generator,
    *,
    seed: int | None = None,
    vary_extra_bounds: bool = True,
) -> dict[str, Any]:
    """Draw a random schema-plausible θ for search."""
    theta = _base_theta(type_id, seed=seed)
    for key, lo, hi in _SEARCHABLE_FLOAT:
        if key != "difficulty" and not vary_extra_bounds:
            continue
        theta[key] = float(rng.uniform(lo, hi))
    # Keep min ≤ max for paired bounds.
    for a, b in (
        ("ratio_part_min", "ratio_part_max"),
        ("num_min", "num_max"),
        ("denom_min", "denom_max"),
    ):
        if a in theta and b in theta and theta[a] > theta[b]:
            theta[a], theta[b] = theta[b], theta[a]
    return theta


def optimize_theta(
    model: ForwardEffortModel,
    type_id: str,
    target_effort: float,
    *,
    n_candidates: int = 200,
    seed: int = 0,
    vary_extra_bounds: bool = False,
    base_theta: dict[str, Any] | None = None,
) -> InverseCandidate:
    """Random-search for θ minimizing |f(θ) - target_effort|."""
    rng = np.random.default_rng(seed)
    best: InverseCandidate | None = None
    for i in range(n_candidates):
        if base_theta is not None:
            theta = copy.deepcopy(base_theta)
            theta["difficulty"] = float(rng.uniform(0.0, 25.0))
            theta["type_id"] = type_id
        else:
            theta = sample_theta(
                type_id,
                rng,
                seed=seed + i,
                vary_extra_bounds=vary_extra_bounds,
            )
        rec = _record_from_theta(type_id, theta)
        pred = model.predict_records([rec])[0]
        if pred is None:
            continue
        err = abs(float(pred) - float(target_effort))
        cand = InverseCandidate(
            theta=theta,
            predicted_effort=float(pred),
            abs_error=float(err),
            target_effort=float(target_effort),
        )
        if best is None or cand.abs_error < best.abs_error:
            best = cand
    if best is None:
        raise RuntimeError("Inverse search produced no candidates")
    return best


def optimize_difficulty_ladder(
    model: ForwardEffortModel,
    type_id: str,
    targets: list[float],
    *,
    n_candidates: int = 150,
    seed: int = 0,
) -> list[InverseCandidate]:
    """Find θ* (difficulty-focused) for each target effort on a ladder."""
    return [
        optimize_theta(
            model,
            type_id,
            target,
            n_candidates=n_candidates,
            seed=seed + i * 17,
            vary_extra_bounds=False,
        )
        for i, target in enumerate(targets)
    ]
