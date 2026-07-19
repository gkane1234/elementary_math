"""Shared primitive registry, leaf→primitive map, and per-question PrimitiveContext."""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any, Callable

from question_engine.frameworks.difficulty_budget import (
    BudgetPlan,
    allocate_budget,
    parse_optional_prereq_cap,
    settings_difficulty,
)
from question_engine.frameworks.primitives import numbers as numbers_mod
from question_engine.frameworks.primitives import variables as variables_mod
from question_engine.frameworks.primitives.expression_policy import (
    LINEAR_POLICY,
    ExpressionPolicy,
    resolve_policy,
)
from question_engine.frameworks.primitives.numbers import SampledNumber
from question_engine.frameworks.primitives.variables import SampledVariable

# --- Primitive IDs (few shared engines) ---
PRIM_NUMBERS = "numbers"
PRIM_VARIABLE = "variable"
PRIM_OOO = "ooo"
PRIM_DISTRIBUTIVE = "distributive"
PRIM_EVALUATE = "evaluate"
PRIM_LIKE_TERMS = "like_terms"
PRIM_EXPAND_SIMPLIFY = "expand_simplify"
PRIM_EQUATIONS = "equations"
PRIM_INEQUALITIES = "inequalities"
PRIM_FACTOR_GCF = "factor_gcf"
PRIM_POLYNOMIALS = "polynomials"
PRIM_FACTOR_POLY = "factor_poly"

CORE_PRIMITIVES: tuple[str, ...] = (
    PRIM_NUMBERS,
    PRIM_VARIABLE,
    PRIM_OOO,
    PRIM_DISTRIBUTIVE,
    PRIM_EVALUATE,
    PRIM_LIKE_TERMS,
    PRIM_EXPAND_SIMPLIFY,
    PRIM_EQUATIONS,
    PRIM_INEQUALITIES,
    PRIM_FACTOR_GCF,
    PRIM_POLYNOMIALS,
    PRIM_FACTOR_POLY,
)

SETTINGS_SCHEMAS: dict[str, dict[str, Any]] = {
    PRIM_NUMBERS: numbers_mod.NUMBER_SETTINGS_SCHEMA,
    PRIM_VARIABLE: variables_mod.VARIABLE_SETTINGS_SCHEMA,
    PRIM_OOO: {},
    PRIM_DISTRIBUTIVE: {},
    PRIM_EVALUATE: {},
    PRIM_LIKE_TERMS: {},
    PRIM_EXPAND_SIMPLIFY: {},
    PRIM_EQUATIONS: {},
    PRIM_INEQUALITIES: {},
    PRIM_FACTOR_GCF: {},
    PRIM_POLYNOMIALS: {},
    PRIM_FACTOR_POLY: {},
}

# Curriculum / prereq leaf IDs → shared primitive (many leaves, few engines).
LEAF_TO_PRIMITIVE: dict[str, str] = {
    # Foundations / Layer 0
    "foundations_math:whole_numbers": PRIM_NUMBERS,
    "foundations_math:addition_subtraction_multiplication_division": PRIM_NUMBERS,
    "foundations_math:fractions_meaning": PRIM_NUMBERS,
    "foundations_math:equivalent_fractions": PRIM_NUMBERS,
    "foundations_math:fraction_operations": PRIM_NUMBERS,
    "foundations_math:decimal_place_value": PRIM_NUMBERS,
    "layer0.numbers": PRIM_NUMBERS,
    "layer0.variable": PRIM_VARIABLE,
    # Grade 6 expression family → ooo / distributive
    "grade_6_math:numeric_expressions_exponents_and_order_of_operations": PRIM_OOO,
    "g6_numeric_expressions_and_order_of_operations": PRIM_OOO,
    "g6_numeric_expressions_with_exponents": PRIM_OOO,
    "order_of_operations": PRIM_OOO,
    "grade_6_math:equivalent_expressions": PRIM_DISTRIBUTIVE,
    "g6_distributive_property_numeric": PRIM_DISTRIBUTIVE,
    "g6_distributive_property_algebraic": PRIM_DISTRIBUTIVE,
    "g6_distributive_property_area_diagrams_numeric": PRIM_DISTRIBUTIVE,
    "g6_distributive_property_area_diagrams_algebraic": PRIM_DISTRIBUTIVE,
    # Layer 1 algebra family
    "g6_evaluating_algebraic_expressions": PRIM_EVALUATE,
    "evaluate_algebraic_expressions": PRIM_EVALUATE,
    "g6_combining_like_terms": PRIM_LIKE_TERMS,
    "combining_like_terms": PRIM_LIKE_TERMS,
    # Expand then simplify (distributive + combine)
    "expand_simplify": PRIM_EXPAND_SIMPLIFY,
    "expand_then_simplify": PRIM_EXPAND_SIMPLIFY,
    # Equations / inequalities by step family
    "one_step_equations": PRIM_EQUATIONS,
    "two_step_equations": PRIM_EQUATIONS,
    "multi_step_equations": PRIM_EQUATIONS,
    "pa_equations_multi_step_equations": PRIM_EQUATIONS,
    "a2_equations_and_inequalities_multi_step_equations": PRIM_EQUATIONS,
    "a2_beginning_algebra_simplifying_algebraic_expressions": PRIM_EXPAND_SIMPLIFY,
    "geo_review_multi_step_equations": PRIM_EQUATIONS,
    "one_step_inequalities": PRIM_INEQUALITIES,
    "two_step_inequalities": PRIM_INEQUALITIES,
    "multi_step_inequalities": PRIM_INEQUALITIES,
    "pa_multi_step_inequalities": PRIM_INEQUALITIES,
    "a2_equations_and_inequalities_multi_step_inequalities": PRIM_INEQUALITIES,
    "g6_solving_and_graphing_one_step_inequalities": PRIM_INEQUALITIES,
    "polynomial_factoring_common_factor": PRIM_FACTOR_GCF,
    "factor_gcf": PRIM_FACTOR_GCF,
    "g6_factor_gcf": PRIM_FACTOR_GCF,
    # Polynomial expression family
    "polynomial_naming": PRIM_POLYNOMIALS,
    "a2_polynomial_functions_naming": PRIM_POLYNOMIALS,
    "polynomial_add_subtract": PRIM_POLYNOMIALS,
    "pa_polynomials_adding_and_subtracting": PRIM_POLYNOMIALS,
    "a2_polynomial_functions_adding_and_subtracting": PRIM_POLYNOMIALS,
    "polynomial_multiply": PRIM_POLYNOMIALS,
    "pa_polynomials_multiplying": PRIM_POLYNOMIALS,
    "a2_polynomial_functions_multiplying": PRIM_POLYNOMIALS,
    "polynomial_multiply_special": PRIM_POLYNOMIALS,
    "a2_polynomial_functions_multiplying_special_cases": PRIM_POLYNOMIALS,
    "evaluate_polynomial": PRIM_EVALUATE,
    "poly_combine_like_terms": PRIM_LIKE_TERMS,
    "poly_expand_simplify": PRIM_EXPAND_SIMPLIFY,
    "quadratic_factoring": PRIM_FACTOR_POLY,
    "a2_quadratic_functions_and_inequalities_factoring_quadratic_expressions": PRIM_FACTOR_POLY,
    "a2_polynomial_functions_factoring_quadratic_form": PRIM_FACTOR_POLY,
    "polynomial_factoring_special_cases": PRIM_FACTOR_POLY,
    "a2_quadratic_functions_and_inequalities_factoring_special_case_quadratic_expressions": PRIM_FACTOR_POLY,
    "a2_polynomial_functions_factoring_sum_difference_of_cubes": PRIM_FACTOR_POLY,
    "polynomial_factoring_grouping": PRIM_FACTOR_POLY,
    "a2_polynomial_functions_factoring_by_grouping": PRIM_FACTOR_POLY,
    "a2_polynomial_functions_factoring_all_techniques": PRIM_FACTOR_POLY,
    # Absolute value / compound / proportions / literals
    "absolute_value_equations": PRIM_EQUATIONS,
    "a2_equations_and_inequalities_absolute_value_equations": PRIM_EQUATIONS,
    "absolute_value_inequalities": PRIM_INEQUALITIES,
    "a2_equations_and_inequalities_absolute_value_inequalities": PRIM_INEQUALITIES,
    "compound_inequalities": PRIM_INEQUALITIES,
    "a2_equations_and_inequalities_compound_inequalities": PRIM_INEQUALITIES,
    "literal_equations": PRIM_EQUATIONS,
    "solving_proportions": PRIM_EQUATIONS,
    "pa_checking_for_a_proportion": PRIM_EQUATIONS,
    # Slope / writing / graph / systems
    "slope": PRIM_EQUATIONS,
    "more_on_slope": PRIM_EQUATIONS,
    "pa_slope": PRIM_EQUATIONS,
    "writing_linear_equations": PRIM_EQUATIONS,
    "pa_writing_linear_equations": PRIM_EQUATIONS,
    "graphing_linear_equations": PRIM_EQUATIONS,
    "graph_linear_equation": PRIM_EQUATIONS,
    "graphing_linear_inequalities": PRIM_INEQUALITIES,
    "graph_linear_inequality": PRIM_INEQUALITIES,
    "graphing_single_variable_inequalities": PRIM_INEQUALITIES,
    "systems_elimination": PRIM_EQUATIONS,
    "systems_substitution": PRIM_EQUATIONS,
    "systems_graphing": PRIM_EQUATIONS,
    "graph_system": PRIM_EQUATIONS,
    "graphing_systems_of_inequalities": PRIM_INEQUALITIES,
    "graph_system_inequalities": PRIM_INEQUALITIES,
    # Word problems
    "wp_mixture": PRIM_EQUATIONS,
    "wp_distance_rate_time": PRIM_EQUATIONS,
    "wp_work": PRIM_EQUATIONS,
    "wp_age": PRIM_EQUATIONS,
    "wp_coin": PRIM_EQUATIONS,
    "wp_consecutive_integers": PRIM_EQUATIONS,
    "wp_percent": PRIM_EQUATIONS,
    "wp_one_step_equation": PRIM_EQUATIONS,
    "wp_two_step_equation": PRIM_EQUATIONS,
    "wp_systems": PRIM_EQUATIONS,
    "wp_proportion": PRIM_EQUATIONS,
    "wp_inequality": PRIM_INEQUALITIES,
}


def resolve_primitive(leaf_or_primitive_id: str) -> str:
    if leaf_or_primitive_id in CORE_PRIMITIVES:
        return leaf_or_primitive_id
    return LEAF_TO_PRIMITIVE.get(leaf_or_primitive_id, leaf_or_primitive_id)


@dataclass
class PrimitiveContext:
    """Bound once per generated question; every sample_* call reads this.

    Guarantees: every instance of a primitive in this item uses difficulty ≤
    that primitive's effective_D and the same prereq_settings.
    Degree / monomial alphabet come from ``policy`` (never bought with leftover D
    on linear leaves).
    """

    topic_d: float
    plan: BudgetPlan
    prereq_settings: dict[str, dict[str, Any]] = field(default_factory=dict)
    rng: random.Random = field(default_factory=random.Random)
    degraded: list[str] = field(default_factory=list)
    policy: ExpressionPolicy = field(default_factory=lambda: LINEAR_POLICY)
    _sample_log: list[dict[str, Any]] = field(default_factory=list)

    def effective_d(self, primitive_id: str) -> float:
        pid = resolve_primitive(primitive_id)
        return self.plan.effective_for(pid)

    def settings_for(self, primitive_id: str) -> dict[str, Any]:
        pid = resolve_primitive(primitive_id)
        # Allow either primitive id or original leaf key in prereq_settings.
        if pid in self.prereq_settings:
            return dict(self.prereq_settings[pid])
        for key, val in self.prereq_settings.items():
            if resolve_primitive(key) == pid:
                return dict(val)
        return {}

    def sample_number(self, **kwargs: Any) -> SampledNumber:
        result = numbers_mod.sample_number(
            self.effective_d(PRIM_NUMBERS),
            settings=self.settings_for(PRIM_NUMBERS),
            rng=self.rng,
            **kwargs,
        )
        entry: dict[str, Any] = {
            "primitive": PRIM_NUMBERS,
            "latex": result.latex,
            "d": result.effective_d,
            "lane": result.profile,
        }
        if result.lane is not None:
            entry["lane_selection"] = result.lane.as_dict()
        self._sample_log.append(entry)
        return result

    def sample_variable(self) -> SampledVariable:
        result = variables_mod.sample_variable(
            self.effective_d(PRIM_VARIABLE),
            settings=self.settings_for(PRIM_VARIABLE),
            rng=self.rng,
        )
        entry: dict[str, Any] = {
            "primitive": PRIM_VARIABLE,
            "name": result.name,
            "latex": result.latex,
            "d": result.effective_d,
            "lane": result.profile,
        }
        if result.lane is not None:
            entry["lane_selection"] = result.lane.as_dict()
        self._sample_log.append(entry)
        return result

    def note_degraded(self, factor_id: str) -> None:
        self.degraded.append(factor_id)
        self.plan.degraded.append(factor_id)

    def metadata(self) -> dict[str, Any]:
        return {
            "difficulty": self.topic_d,
            "spend": self.plan.to_spend_dict(),
            "degraded": list(self.degraded),
            "sample_log": list(self._sample_log),
            "expression_policy": self.policy.as_dict(),
        }


def build_context(
    settings: dict[str, Any],
    contributing_primitives: list[str],
    *,
    rng: random.Random | None = None,
    d_max: float | None = None,
    policy: ExpressionPolicy | None = None,
    leaf_id: str | None = None,
) -> PrimitiveContext:
    """Create a per-question context from topic settings + contributing primitive list.

    ``contributing_primitives`` should be in prereq order (early → late / downstream).
    ``d_max`` is an optional explicit ceiling; omit it so user-entered difficulty
    is not crushed to a soft UI guidance value.
    """
    rng = rng or random.Random()
    topic_d = settings_difficulty(settings, default=0.0)
    caps_raw = dict(settings.get("prereq_caps") or {})
    # Flat UI keys: prereq_cap_numbers, prereq_cap_ooo, ...
    # Empty / null / "none" means no cap — omit from the caps dict.
    for key, val in list(settings.items()):
        if str(key).startswith("prereq_cap_"):
            pid = str(key)[len("prereq_cap_") :]
            parsed = parse_optional_prereq_cap(val)
            if parsed is None:
                caps_raw.pop(pid, None)
            else:
                caps_raw[pid] = parsed
    # Normalize cap keys to primitive ids; drop no-cap sentinels.
    caps: dict[str, float] = {}
    for key, val in caps_raw.items():
        parsed = parse_optional_prereq_cap(val)
        if parsed is None:
            continue
        caps[resolve_primitive(str(key))] = parsed

    prims = [resolve_primitive(p) for p in contributing_primitives]
    # Deduplicate while preserving order (first occurrence wins position).
    seen: set[str] = set()
    ordered: list[str] = []
    for p in prims:
        if p not in seen:
            seen.add(p)
            ordered.append(p)

    # Always include numbers + variable as Layer 0 when building expression-like items
    # if caller forgot — but only if empty? Prefer explicit caller lists.
    plan = allocate_budget(
        topic_d,
        ordered,
        prereq_caps=caps,
        d_max=d_max,
        rng=rng,
    )
    prereq_settings = dict(settings.get("prereq_settings") or {})
    # Flat nested settings: number constraints / optional force profile / variable locks
    num_settings = dict(prereq_settings.get(PRIM_NUMBERS) or {})
    for key in (
        "number_profile",
        "force_number_profile",
        "integers_only",
        "allow_negatives",
        "allow_fractions",
        "allow_decimals",
        "exclude_zero",
        "number_domain",
        "no_fractions",
        "no_decimals",
    ):
        if key in settings:
            num_settings[key] = settings[key]
    if num_settings:
        prereq_settings[PRIM_NUMBERS] = num_settings
    var_settings = dict(prereq_settings.get(PRIM_VARIABLE) or {})
    for key in (
        "lock_variable",
        "allow_other_letters",
        "only_x",
        "allow_greek",
        "no_greek",
        "max_variable_lane",
        "variable_lane",
        "force_variable_lane",
    ):
        if key in settings:
            var_settings[key] = settings[key]
    if var_settings:
        prereq_settings[PRIM_VARIABLE] = var_settings

    # Layer-1 structure knobs (optional flat keys).
    if "force_steps" in settings:
        for pid in (PRIM_EQUATIONS, PRIM_INEQUALITIES):
            layer = dict(prereq_settings.get(pid) or {})
            layer.setdefault("force_steps", settings["force_steps"])
            prereq_settings[pid] = layer
    for key in (
        "allow_special_solutions",
        "clear_fractions",
        "force_lcd",
        "compound_style",
        "slope_mode",
        "writing_mode",
        "method",
        "solution_type",
    ):
        if key in settings:
            for pid in (PRIM_EQUATIONS, PRIM_INEQUALITIES):
                layer = dict(prereq_settings.get(pid) or {})
                layer.setdefault(key, settings[key])
                prereq_settings[pid] = layer

    resolved = resolve_policy(
        leaf_id or settings.get("leaf_id") or settings.get("generator"),
        settings=settings,
        explicit=policy,
    )
    ctx = PrimitiveContext(
        topic_d=plan.topic_d,
        plan=plan,
        prereq_settings=prereq_settings,
        rng=rng,
        policy=resolved,
    )
    # Topic settings (e.g. presentation overrides) readable by shared helpers.
    ctx.settings = dict(settings)  # type: ignore[attr-defined]
    return ctx


@dataclass(frozen=True)
class PrimitiveSpec:
    id: str
    settings_schema: dict[str, Any]
    sampler: Callable[..., Any] | None = None


def get_primitive_spec(primitive_id: str) -> PrimitiveSpec:
    pid = resolve_primitive(primitive_id)
    return PrimitiveSpec(
        id=pid,
        settings_schema=SETTINGS_SCHEMAS.get(pid, {}),
    )
