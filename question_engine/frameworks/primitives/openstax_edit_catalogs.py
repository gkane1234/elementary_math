"""OpenStax within-form edits, one list per question family.

Each row is a change OpenStax already uses inside a form: a coefficient move,
a factoring or distributing step, or a different question about the same figure.
Weights start even, with the ordinary textbook moves rated higher.

``stage`` is ``edit`` when the change is applied after a plain form exists, and
``sample`` when the generator already chooses it while building the form.
Actions are not applied to a family until that family builds the part the
action names.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FamilyEdit:
    action_id: str
    family: str
    part: str
    summary: str
    weight: float
    kind: str  # rewrite (same answer) or value (answer changes)
    stage: str  # edit or sample
    evidence: str


def _e(
    action_id: str,
    family: str,
    part: str,
    summary: str,
    weight: float,
    kind: str,
    stage: str,
    evidence: str,
) -> FamilyEdit:
    return FamilyEdit(action_id, family, part, summary, weight, kind, stage, evidence)


# Limits: OpenStax Calculus Vol. 1 §2.3 and §4.6. The post-sample dresses that
# already exist are sign and a constant multiple of the whole expression.
LIMIT_EDITS: tuple[FamilyEdit, ...] = (
    _e(
        "sign",
        "limits",
        "limit_body",
        "Multiply the whole limit expression by -1. The limit answer changes sign.",
        2.0,
        "value",
        "edit",
        "limits.json direct families; complexity_wrap allowed_wraps_for_limit",
    ),
    _e(
        "constant_multiple",
        "limits",
        "limit_body",
        "Multiply the whole limit expression by a small integer and scale the answer.",
        2.0,
        "value",
        "edit",
        "OpenStax §2.3 constant multiple law; complexity_wrap sample_safe_scale",
    ),
    _e(
        "expand_cancelled_numerator",
        "limits",
        "removable_numerator",
        "Write a factored removable numerator as an expanded polynomial.",
        1.5,
        "rewrite",
        "sample",
        "limits.py removable_expand when difficulty is high",
    ),
)

# Integrals: OpenStax §5.5 shows the inner derivative visibly, and later
# exercises omit that constant so the student supplies it.
INTEGRAL_EDITS: tuple[FamilyEdit, ...] = (
    _e(
        "omit_du_constant",
        "integrals",
        "integrand",
        "Hide the constant factor that is the inner derivative, as in later §5.5 exercises.",
        2.0,
        "rewrite",
        "sample",
        "integrals.py hide when format_tier >= 2; u_substitution catalog",
    ),
    _e(
        "linear_inner_u_equals_x_plus_b",
        "integrals",
        "trig_sub_radicand",
        "Replace x with x+b inside a trig-substitution radicand.",
        1.2,
        "value",
        "sample",
        "integrals.py _sample_trig_sub do_wrap",
    ),
)

# Algebra: OpenStax Elementary Algebra ch. 2 and ch. 7. Most of this variation
# is which form is chosen. These rows are the rewrites inside a form.
ALGEBRA_EDITS: tuple[FamilyEdit, ...] = (
    _e(
        "distribute",
        "algebra",
        "equation",
        "Present a linear equation with a factor that must be distributed.",
        2.0,
        "rewrite",
        "sample",
        "algebra1_linear_equations.json form multi_step_distribute",
    ),
    _e(
        "factor_gcf",
        "algebra",
        "polynomial",
        "Ask for a greatest common factor, then a second factor pattern.",
        2.0,
        "rewrite",
        "sample",
        "algebra1_factoring.json forms gcf_monomial and gcf_then_pattern",
    ),
    _e(
        "rationalize",
        "algebra",
        "radical_quotient",
        "Ask the student to rationalize a one-term or two-term denominator.",
        1.5,
        "rewrite",
        "sample",
        "algebra1_radicals.json form divide_rationalize",
    ),
)

# Figures and data: the variation already in the generators, named so an edit
# seed can re-roll it. A topic with one sentence is not given a fake second form.
FIGURE_EDITS: tuple[FamilyEdit, ...] = (
    _e(
        "reroll_circle_quantity",
        "figures",
        "circle",
        "Ask for circumference or for area of the same circle.",
        2.0,
        "value",
        "edit",
        "geometry.py CircleMeasureFramework circle_quantity",
    ),
    _e(
        "reroll_triangle_layout",
        "figures",
        "triangle",
        "Place the altitude inside the triangle, outside it, or on a right angle.",
        1.5,
        "value",
        "edit",
        "geometry.py _triangle_area_layout",
    ),
    _e(
        "reroll_box_plot_stat",
        "data",
        "box_plot",
        "Ask for the median, the range, the IQR, Q1, or Q3 of the same plot.",
        2.0,
        "value",
        "edit",
        "statistics.py _box_plot_task_mode",
    ),
    _e(
        "reroll_center_spread_measure",
        "data",
        "data_list",
        "Ask for the mean, median, mode, or range of the same list.",
        2.0,
        "value",
        "edit",
        "statistics.py _pick_center_spread_measure",
    ),
)

FAMILY_EDITS: dict[str, tuple[FamilyEdit, ...]] = {
    "limits": LIMIT_EDITS,
    "integrals": INTEGRAL_EDITS,
    "algebra": ALGEBRA_EDITS,
    "figures": FIGURE_EDITS,
}


def catalog_rows(family: str | None = None) -> list[dict[str, Any]]:
    groups = FAMILY_EDITS.values() if family is None else (FAMILY_EDITS[family],)
    rows: list[dict[str, Any]] = []
    for group in groups:
        for action in group:
            rows.append(
                {
                    "action_id": action.action_id,
                    "family": action.family,
                    "part": action.part,
                    "summary": action.summary,
                    "weight": action.weight,
                    "kind": action.kind,
                    "stage": action.stage,
                    "evidence": action.evidence,
                }
            )
    return rows


def weighted_edit_id(
    family: str,
    candidates: list[str],
    rng: random.Random,
) -> str | None:
    """Pick one catalog action among ``candidates``, using catalog weights."""
    if not candidates:
        return None
    by_id = {action.action_id: action for action in FAMILY_EDITS.get(family, ())}
    weighted = [(name, by_id[name].weight) for name in candidates if name in by_id and by_id[name].weight > 0]
    if not weighted:
        return rng.choice(candidates)
    names = [name for name, _weight in weighted]
    weights = [weight for _name, weight in weighted]
    return rng.choices(names, weights=weights, k=1)[0]
