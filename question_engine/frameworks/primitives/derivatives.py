"""Derivative expression sampler — continuous-D + function/method allow-lists.

Grounded in OpenStax Calculus Vol. 1 Ch. 3 patterns (power / product / quotient /
chain / trig / exp / log). Algebraic atoms are cheapest; each distinct special
function class and each composition / product / quotient method spends budget.

Generators call ``sample_derivative_problem`` with a topic leaf / generator id;
settings ``allow_*`` gates hard-exclude classes and methods; continuous D buys
structure upgrades via ``DifficultyFactor``.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any, Literal, Sequence

from question_engine.frameworks.difficulty_budget import (
    DifficultyFactor,
    dual_axis_rngs,
    select_upgrades,
    settings_difficulty,
    settings_spec_difficulty,
)
from question_engine.frameworks.primitives.difficulty_knobs import fget
from question_engine.frameworks.primitives import poly_expression as poly_expr
from question_engine.generators.utils import (
    format_linear_latex,
    format_monomial_latex,
    format_polynomial_latex,
    frac_latex,
)
from fractions import Fraction

FunctionClass = Literal[
    "algebraic",
    "trig",
    "exp",
    "log",
    "hyperbolic",
    "roots",
    "invtrig",
]
MethodName = Literal["power", "sum", "product", "quotient", "chain", "implicit"]

FUNCTION_ALLOW_KEYS: tuple[str, ...] = (
    "allow_trig",
    "allow_exp",
    "allow_log",
    "allow_hyperbolic",
    "allow_roots",
    "allow_invtrig",
)
METHOD_ALLOW_KEYS: tuple[str, ...] = (
    "allow_chain",
    "allow_product",
    "allow_quotient",
    "allow_implicit",
)
REQUIRE_METHOD_KEYS: tuple[str, ...] = (
    "require_chain",
    "require_product",
    "require_quotient",
)

# Topic-leaf defaults: specials OFF on algebraic leaves; topic specialty ON.
_TOPIC_DEFAULTS: dict[str, dict[str, bool]] = {
    # Algebraic / power / poly
    "derivative_power_rule": {
        "allow_trig": False,
        "allow_exp": False,
        "allow_log": False,
        "allow_hyperbolic": False,
        "allow_roots": True,  # x^{p/q} is power-rule territory
        "allow_invtrig": False,
        "allow_chain": False,
        "allow_product": False,
        "allow_quotient": False,
        "allow_implicit": False,
        "require_chain": False,
        "require_product": False,
        "require_quotient": False,
    },
    "derivative_higher_order": {
        # Soft-unlock trig/exp; D + Spec order≥2 gate appearance.
        "allow_trig": True,
        "allow_exp": True,
        "allow_log": False,
        "allow_hyperbolic": False,
        "allow_roots": False,
        "allow_invtrig": False,
        "allow_chain": True,
        "allow_product": False,
        "allow_quotient": False,
        "allow_implicit": False,
    },
    "derivative_product_rule": {
        # Soft-unlock: D gates when specials appear; low D stays algebraic-heavy.
        "allow_trig": True,
        "allow_exp": True,
        "allow_log": True,
        "allow_hyperbolic": False,
        "allow_roots": False,
        "allow_invtrig": False,
        "allow_chain": True,
        "allow_product": True,
        "allow_quotient": False,
        "allow_implicit": False,
        "require_product": True,
    },
    "derivative_quotient_rule": {
        "allow_trig": False,
        "allow_exp": False,
        "allow_log": False,
        "allow_hyperbolic": False,
        "allow_roots": False,
        "allow_invtrig": False,
        "allow_chain": True,
        "allow_product": False,
        "allow_quotient": True,
        "allow_implicit": False,
        "require_quotient": True,
    },
    "derivative_chain_rule": {
        # Soft-unlock: D gates when specials appear; low D stays algebraic-heavy.
        "allow_trig": True,
        "allow_exp": True,
        "allow_log": True,
        "allow_hyperbolic": False,
        "allow_roots": True,
        "allow_invtrig": False,
        "allow_chain": True,
        "allow_product": True,
        "allow_quotient": False,
        "allow_implicit": False,
        "require_chain": True,
    },
    "derivative_trigonometric": {
        "allow_trig": True,
        "allow_exp": False,
        "allow_log": False,
        "allow_hyperbolic": False,
        "allow_roots": False,
        "allow_invtrig": False,
        "allow_chain": True,
        "allow_product": True,
        "allow_quotient": True,
        "allow_implicit": False,
    },
    "derivative_ln_exp": {
        "allow_trig": False,
        "allow_exp": True,
        "allow_log": True,
        "allow_hyperbolic": False,
        "allow_roots": False,
        "allow_invtrig": False,
        "allow_chain": True,
        "allow_product": True,
        "allow_quotient": False,
        "allow_implicit": False,
    },
    "derivative_other_base": {
        "allow_trig": False,
        "allow_exp": True,
        "allow_log": True,
        "allow_hyperbolic": False,
        "allow_roots": False,
        "allow_invtrig": False,
        "allow_chain": True,
        "allow_product": False,
        "allow_quotient": False,
        "allow_implicit": False,
    },
    "derivative_inverse_trig": {
        "allow_trig": False,
        "allow_exp": False,
        "allow_log": False,
        "allow_hyperbolic": False,
        "allow_roots": False,
        "allow_invtrig": True,
        "allow_chain": True,
        "allow_product": False,
        "allow_quotient": False,
        "allow_implicit": False,
    },
    "derivative_implicit": {
        "allow_trig": False,
        "allow_exp": False,
        "allow_log": False,
        "allow_hyperbolic": False,
        "allow_roots": False,
        "allow_invtrig": False,
        "allow_chain": True,
        "allow_product": True,
        "allow_quotient": False,
        "allow_implicit": True,
        "require_implicit": True,
    },
    "derivative_logarithmic": {
        "allow_trig": False,
        "allow_exp": True,
        "allow_log": True,
        "allow_hyperbolic": False,
        "allow_roots": False,
        "allow_invtrig": False,
        "allow_chain": True,
        "allow_product": True,
        "allow_quotient": True,
        "allow_implicit": False,
    },
    # Fully tunable general leaf: all classes/methods soft-on; settings can disable.
    "derivative_general": {
        "allow_trig": True,
        "allow_exp": True,
        "allow_log": True,
        "allow_hyperbolic": True,
        "allow_roots": True,
        "allow_invtrig": True,
        "allow_chain": True,
        "allow_product": True,
        "allow_quotient": True,
        "allow_implicit": False,
        "require_chain": False,
        "require_product": False,
        "require_quotient": False,
    },
}

# Map type_id prefixes / exact ids → generator key for defaults.
_TYPE_ID_TO_GENERATOR: dict[str, str] = {
    "calc_diff_power_rule": "derivative_power_rule",
    "calc_diff_product_rule": "derivative_product_rule",
    "calc_diff_quotient_rule": "derivative_quotient_rule",
    "calc_diff_chain_rule": "derivative_chain_rule",
    "calc_diff_trigonometric": "derivative_trigonometric",
    "calc_diff_natural_logarithms_and_exponentials": "derivative_ln_exp",
    "calc_diff_other_base_logarithms_and_exponentials": "derivative_other_base",
    "calc_diff_inverse_trigonometric": "derivative_inverse_trig",
    "calc_diff_implicit": "derivative_implicit",
    "calc_diff_logarithmic": "derivative_logarithmic",
    "calc_diff_higher_order_derivatives": "derivative_higher_order",
    "calc_diff_general": "derivative_general",
}


def _upgrade_cost(factor_id: str, default: float) -> float:
    return fget("derivatives", f"upgrade_{factor_id}_cost", default)


def _derivative_upgrades() -> tuple[DifficultyFactor, ...]:
    """Live costs from difficulty_knobs → derivatives section."""
    return (
        DifficultyFactor("extra_term", _upgrade_cost("extra_term", 1.0), ("ops",)),
        DifficultyFactor("higher_power", _upgrade_cost("higher_power", 1.5), ("ops",)),
        DifficultyFactor("use_product", _upgrade_cost("use_product", 3.0), ("method",)),
        DifficultyFactor("use_quotient", _upgrade_cost("use_quotient", 3.5), ("method",)),
        DifficultyFactor("use_chain", _upgrade_cost("use_chain", 2.5), ("method",)),
        DifficultyFactor("chain_depth_2", _upgrade_cost("chain_depth_2", 4.0), ("nesting",)),
        DifficultyFactor("class_trig", _upgrade_cost("class_trig", 3.0), ("class",)),
        DifficultyFactor("class_exp", _upgrade_cost("class_exp", 3.5), ("class",)),
        DifficultyFactor("class_log", _upgrade_cost("class_log", 4.0), ("class",)),
        DifficultyFactor("class_roots", _upgrade_cost("class_roots", 2.5), ("class",)),
        DifficultyFactor("class_invtrig", _upgrade_cost("class_invtrig", 5.0), ("class",)),
        DifficultyFactor("class_hyperbolic", _upgrade_cost("class_hyperbolic", 5.5), ("class",)),
        DifficultyFactor("mix_classes", _upgrade_cost("mix_classes", 2.0), ("class",)),
        DifficultyFactor("fn_power", _upgrade_cost("fn_power", 2.5), ("ops",)),
        DifficultyFactor("higher_order", _upgrade_cost("higher_order", 4.5), ("ops",)),
    )


DERIVATIVE_SETTINGS_SCHEMA: dict[str, Any] = {
    key: {"type": "bool", "default": False}
    for key in (
        *FUNCTION_ALLOW_KEYS,
        *METHOD_ALLOW_KEYS,
        *REQUIRE_METHOD_KEYS,
        "require_implicit",
    )
}


@dataclass(frozen=True)
class DerivativeAllowConfig:
    allow_trig: bool = False
    allow_exp: bool = False
    allow_log: bool = False
    allow_hyperbolic: bool = False
    allow_roots: bool = False
    allow_invtrig: bool = False
    allow_chain: bool = False
    allow_product: bool = False
    allow_quotient: bool = False
    allow_implicit: bool = False
    require_chain: bool = False
    require_product: bool = False
    require_quotient: bool = False
    require_implicit: bool = False

    def class_allowed(self, cls: FunctionClass) -> bool:
        if cls == "algebraic":
            return True
        return bool(getattr(self, f"allow_{cls}", False))

    def method_allowed(self, method: MethodName) -> bool:
        if method in ("power", "sum"):
            return True
        return bool(getattr(self, f"allow_{method}", False))


@dataclass(frozen=True)
class DerivativeExpr:
    """Sampled differentiable expression with closed-form derivative latex."""

    body_latex: str
    deriv_latex: str
    function_classes: frozenset[str]
    methods_used: frozenset[str]
    chain_depth: int = 0


@dataclass(frozen=True)
class DerivativeSample:
    prompt_latex: str
    answer_latex: str
    function_classes: tuple[str, ...]
    methods_used: tuple[str, ...]
    chain_depth: int
    upgrades: tuple[str, ...]
    effective_d: float
    allow: DerivativeAllowConfig
    band: str
    coef_hi: int
    power_max: int
    term_budget: int
    metadata: dict[str, Any] = field(default_factory=dict)

    def as_metadata(self) -> dict[str, Any]:
        methods = list(self.methods_used)
        classes = list(self.function_classes)
        gen_key = str(self.metadata.get("generator") or "")
        # Methods are the structural template for framework derivatives.
        family = "+".join(methods) if methods else (gen_key or "derivative")
        structure_id = f"{gen_key}:{family}" if gen_key else family
        return {
            "family": family,
            "structure_id": structure_id,
            "function_classes": classes,
            "methods_used": methods,
            "chain_depth": self.chain_depth,
            "upgrades": list(self.upgrades),
            "effective_d": self.effective_d,
            "band": self.band,
            **self.metadata,
        }


def resolve_generator_key(topic_or_generator: str | None) -> str | None:
    if not topic_or_generator:
        return None
    key = str(topic_or_generator).strip()
    if key in _TOPIC_DEFAULTS:
        return key
    if key in _TYPE_ID_TO_GENERATOR:
        return _TYPE_ID_TO_GENERATOR[key]
    # Strip course prefix c1_
    if key.startswith("c1_") and key[3:] in _TYPE_ID_TO_GENERATOR:
        return _TYPE_ID_TO_GENERATOR[key[3:]]
    return None


def topic_allow_defaults(generator_key: str | None) -> dict[str, bool]:
    base = {
        "allow_trig": False,
        "allow_exp": False,
        "allow_log": False,
        "allow_hyperbolic": False,
        "allow_roots": False,
        "allow_invtrig": False,
        "allow_chain": False,
        "allow_product": False,
        "allow_quotient": False,
        "allow_implicit": False,
        "require_chain": False,
        "require_product": False,
        "require_quotient": False,
        "require_implicit": False,
    }
    if generator_key and generator_key in _TOPIC_DEFAULTS:
        base.update(_TOPIC_DEFAULTS[generator_key])
    return base


def resolve_derivative_allows(
    settings: dict[str, Any],
    *,
    generator_key: str | None = None,
    topic: str | None = None,
) -> DerivativeAllowConfig:
    """Merge topic defaults with explicit settings (settings win when present).

    When neither a generator/topic leaf nor any ``allow_*`` key is supplied,
    specials/methods are treated as D-open (legacy continuous-D unlock ladder).
    Topic leaves still default specials OFF via ``topic_allow_defaults``.
    """
    key = generator_key or resolve_generator_key(topic) or resolve_generator_key(
        str(settings.get("generator") or "")
    )
    has_explicit = any(k in settings and settings[k] is not None for k in (
        *FUNCTION_ALLOW_KEYS,
        *METHOD_ALLOW_KEYS,
        *REQUIRE_METHOD_KEYS,
        "require_implicit",
    ))
    if key:
        defaults = topic_allow_defaults(key)
    elif has_explicit:
        defaults = topic_allow_defaults(None)
    else:
        # Bare continuous-D / EMH structure probe: unlocks follow D only.
        defaults = {
            "allow_trig": True,
            "allow_exp": True,
            "allow_log": True,
            "allow_hyperbolic": True,
            "allow_roots": True,
            "allow_invtrig": True,
            "allow_chain": True,
            "allow_product": True,
            "allow_quotient": True,
            "allow_implicit": True,
            "require_chain": False,
            "require_product": False,
            "require_quotient": False,
            "require_implicit": False,
        }
    merged: dict[str, bool] = dict(defaults)
    for k in defaults:
        if k in settings and settings[k] is not None:
            merged[k] = bool(settings[k])
    # Required methods imply allow
    if merged.get("require_chain"):
        merged["allow_chain"] = True
    if merged.get("require_product"):
        merged["allow_product"] = True
    if merged.get("require_quotient"):
        merged["allow_quotient"] = True
    if merged.get("require_implicit"):
        merged["allow_implicit"] = True
    return DerivativeAllowConfig(**{k: bool(merged[k]) for k in defaults})


def _band_for_d(d: float) -> str:
    if d <= 4.0 + 1e-9:
        return "easy"
    if d <= 11.0 + 1e-9:
        return "medium"
    return "hard"


def structure_knobs_from_d(d: float) -> dict[str, Any]:
    """Coef / power / term spans from continuous D (independent of allow flags).

    D≈16–25 is tightened so hard worksheets stay challenging but not absurd.
    Past D=25, knobs grow slowly for uncapped Spec / typed-difficulty paths.
    """
    if d < 4.0:
        return {
            "band": "easy",
            "coef_hi": 3,
            "power_max": 4,
            "term_budget": 2,
        }
    if d < 10.0:
        return {
            "band": "medium",
            "coef_hi": 4 + int(d // 5),
            "power_max": 5,
            "term_budget": 3,
        }
    if d < 16.0:
        return {
            "band": "hard",
            "coef_hi": 5 + int((d - 10) // 3),
            "power_max": 6,
            "term_budget": 4,
        }
    if d <= 25.0:
        # Tightened hard band (was coef≤10 / power≤8 / terms≤6)
        return {
            "band": "hard",
            "coef_hi": min(7, 5 + int((d - 16) // 5)),
            "power_max": min(6, 5 + int((d - 16) // 6)),
            "term_budget": min(4, 3 + int((d - 16) // 8)),
        }
    # Uncapped Spec path: mild linear growth beyond worksheet/UI soft max
    return {
        "band": "hard",
        "coef_hi": min(20, 7 + int((d - 25) // 10)),
        "power_max": min(12, 6 + int((d - 25) // 15)),
        "term_budget": min(8, 4 + int((d - 25) // 20)),
    }


def derivative_rule_structure(
    settings: dict[str, Any],
    *,
    generator_key: str | None = None,
    topic: str | None = None,
) -> dict[str, Any]:
    """Full continuous-D structure + resolved allow flags.

    When continuous ``difficulty`` is absent, still resolves allows from topic
    defaults / explicit settings and EMH band spans.
    """
    allow = resolve_derivative_allows(
        settings, generator_key=generator_key, topic=topic
    )
    d = None
    if "difficulty" in settings and settings["difficulty"] is not None:
        try:
            d = float(settings["difficulty"])
        except (TypeError, ValueError):
            d = None
    if d is None:
        # EMH fallback spans
        tier = str(settings.get("difficulty_tier", settings.get("difficulty", "easy")))
        tier = tier.strip().lower()
        legacy = {"1": "easy", "e": "easy", "2": "medium", "m": "medium", "3": "hard", "h": "hard"}
        band = legacy.get(tier, tier if tier in {"easy", "medium", "hard"} else "easy")
        spans = {
            "easy": {"coef_hi": 4, "power_max": 5, "term_budget": 2},
            "medium": {"coef_hi": 4, "power_max": 5, "term_budget": 3},
            "hard": {"coef_hi": 4, "power_max": 6, "term_budget": 4},
        }[band]
        d_approx = {"easy": 3.0, "medium": 8.0, "hard": 14.0}[band]
        # Soft EMH unlocks only when class is allowed by settings
        emh_trig = band != "easy" and allow.allow_trig
        emh_exp = band != "easy" and allow.allow_exp
        emh_log = band == "hard" and allow.allow_log
        emh_nested = band == "hard" and allow.allow_chain
        return {
            "difficulty": d_approx,
            "band": band,
            **spans,
            "allow_trig": emh_trig,
            "allow_exp": emh_exp,
            "allow_ln": emh_log,  # back-compat alias
            "allow_log": emh_log,
            "allow_nested": emh_nested,
            "allow_hyperbolic": band == "hard" and allow.allow_hyperbolic,
            "allow_roots": allow.allow_roots and band != "easy",
            "allow_invtrig": band != "easy" and allow.allow_invtrig,
            "allow_chain": allow.allow_chain and (band != "easy" or allow.require_chain),
            "allow_product": allow.allow_product and (band != "easy" or allow.require_product),
            "allow_quotient": allow.allow_quotient and (band != "easy" or allow.require_quotient),
            "allow_implicit": allow.allow_implicit,
            "require_chain": allow.require_chain,
            "require_product": allow.require_product,
            "require_quotient": allow.require_quotient,
            "require_implicit": allow.require_implicit,
            "_allow": allow,
        }

    spans = structure_knobs_from_d(d)
    # D-gated unlocks within allowed classes (settings hard-gate)
    unlocked_trig = allow.allow_trig and d >= fget("derivatives", "unlock_trig_d", 6.0)
    unlocked_exp = allow.allow_exp and d >= fget("derivatives", "unlock_exp_d", 7.0)
    unlocked_log = allow.allow_log and d >= fget("derivatives", "unlock_log_d", 12.0)
    unlocked_roots = allow.allow_roots and d >= fget("derivatives", "unlock_roots_d", 4.0)
    unlocked_invtrig = allow.allow_invtrig and d >= fget(
        "derivatives", "unlock_invtrig_d", 10.0
    )
    unlocked_hyp = allow.allow_hyperbolic and d >= fget(
        "derivatives", "unlock_hyperbolic_d", 16.0
    )
    unlocked_nested = allow.allow_chain and d >= fget(
        "derivatives", "unlock_nested_d", 14.0
    )
    unlocked_product = allow.allow_product and (
        allow.require_product or d >= fget("derivatives", "unlock_product_d", 5.0)
    )
    unlocked_quotient = allow.allow_quotient and (
        allow.require_quotient or d >= fget("derivatives", "unlock_quotient_d", 6.0)
    )
    unlocked_chain = allow.allow_chain and (
        allow.require_chain or d >= fget("derivatives", "unlock_chain_d", 4.0)
    )
    # Exponent-style knobs: explicit settings win; else D defaults for chain topics
    frac_exp = settings.get("allow_fractional_exponents")
    irr_exp = settings.get("allow_irrational_exponents")
    int_exp = settings.get("allow_integer_exponents")
    neg_exp = settings.get("allow_negative_exponents")
    return {
        "difficulty": d,
        **spans,
        "allow_trig": unlocked_trig,
        "allow_exp": unlocked_exp,
        "allow_ln": unlocked_log,
        "allow_log": unlocked_log,
        "allow_nested": unlocked_nested,
        "allow_hyperbolic": unlocked_hyp,
        "allow_roots": unlocked_roots,
        "allow_invtrig": unlocked_invtrig,
        "allow_chain": unlocked_chain,
        "allow_product": unlocked_product,
        "allow_quotient": unlocked_quotient,
        "allow_implicit": allow.allow_implicit,
        "require_chain": allow.require_chain,
        "require_product": allow.require_product,
        "require_quotient": allow.require_quotient,
        "require_implicit": allow.require_implicit,
        "allow_integer_exponents": True if int_exp is None else bool(int_exp),
        "allow_fractional_exponents": (
            None if frac_exp is None else bool(frac_exp)
        ),
        "allow_irrational_exponents": (
            None if irr_exp is None else bool(irr_exp)
        ),
        "allow_negative_exponents": (
            None if neg_exp is None else bool(neg_exp)
        ),
        "_allow": allow,
    }


def _allowed_upgrade_ids(
    allow: DerivativeAllowConfig,
    *,
    force_methods: set[str],
) -> set[str]:
    ids: set[str] = {"extra_term", "higher_power", "fn_power", "higher_order"}
    if allow.allow_product or "product" in force_methods:
        ids.add("use_product")
    if allow.allow_quotient or "quotient" in force_methods:
        ids.add("use_quotient")
    if allow.allow_chain or "chain" in force_methods:
        ids.add("use_chain")
        ids.add("chain_depth_2")
    if allow.allow_trig:
        ids.add("class_trig")
    if allow.allow_exp:
        ids.add("class_exp")
    if allow.allow_log:
        ids.add("class_log")
    if allow.allow_roots:
        ids.add("class_roots")
    if allow.allow_invtrig:
        ids.add("class_invtrig")
    if allow.allow_hyperbolic:
        ids.add("class_hyperbolic")
    # Mix only makes sense with ≥2 class upgrades purchasable
    class_ids = {
        "class_trig",
        "class_exp",
        "class_log",
        "class_roots",
        "class_invtrig",
        "class_hyperbolic",
    }
    if len(ids & class_ids) >= 2:
        ids.add("mix_classes")
    return ids


def _derivative_order_for_sample(
    d: float,
    purchased_ids: set[str],
    rng: random.Random,
    *,
    key: str | None,
) -> int:
    """Gate 2nd/3rd derivatives by D; prefer simpler inners upstream via packs.

    Mid–high D specialty/general packs raise order=2 rate; packs tighten
    factor/nest/power budgets so expanded answers stay within length gates.
    """
    if key == "derivative_higher_order":
        # Dedicated leaf always differentiates ≥2 times via Spec packs.
        if d < 12.0:
            return 2
        if d < 20.0:
            return 3 if rng.random() < 0.25 else 2
        return 3 if rng.random() < 0.45 else 2
    if key in {"derivative_product_rule", "derivative_quotient_rule"}:
        # Product/quotient leaves already stress method; keep first-order
        return 1
    if d < 12.0 and "higher_order" not in purchased_ids:
        return 1
    # Probability grows with D; specialty/general get a bump
    specialty = key in {
        "derivative_trigonometric",
        "derivative_ln_exp",
        "derivative_inverse_trig",
        "derivative_general",
    }
    if specialty:
        p2 = 0.2 if d < 16 else (0.32 if d < 20 else (0.42 if d < 25 else 0.5))
        p3 = 0.0 if d < 22 else (0.06 if d < 28 else 0.12)
    else:
        p2 = 0.14 if d < 18 else (0.24 if d < 22 else 0.34)
        p3 = 0.0 if d < 22 else (0.08 if d < 30 else 0.15)
    if "higher_order" in purchased_ids:
        p2 = max(p2, 0.4)
        if d >= 20:
            p3 = max(p3, 0.1)
    r = rng.random()
    if r < p3:
        return 3
    if r < p3 + p2:
        return 2
    return 1


def _rng(settings: dict[str, Any]) -> random.Random:
    raw = settings.get("seed")
    if raw is None:
        return random.Random()
    try:
        base = int(raw)
        idx = int(settings.get("_batch_index") or 0)
        return random.Random(base + idx * 1009)
    except (TypeError, ValueError):
        return random.Random()


def _mono(coef: int, var: str, power: int = 1) -> str:
    return format_monomial_latex(coef, variable=var, degree=power) or (
        "0" if coef == 0 else str(coef)
    )


def _linear_pair(rng: random.Random, coef_hi: int) -> tuple[int, int]:
    a = rng.randint(1, max(1, coef_hi))
    b = rng.choice([i for i in range(-coef_hi, coef_hi + 1) if i != 0] or [1])
    return a, b


# ---------------------------------------------------------------------------
# Atom builders
# ---------------------------------------------------------------------------


def _from_poly_pair(pair: poly_expr.PolyLatexPair) -> DerivativeExpr:
    return DerivativeExpr(
        pair.body_latex,
        pair.deriv_latex,
        pair.function_classes,
        pair.methods_used,
        pair.chain_depth,
    )


def _atom_poly(
    rng: random.Random, var: str, coef_hi: int, power_max: int, *, extra_term: bool
) -> DerivativeExpr:
    return _from_poly_pair(
        poly_expr.sample_poly_atom(rng, var, coef_hi, power_max, extra_term=extra_term)
    )


def _atom_trig(rng: random.Random, var: str, *, chained: bool, coef_hi: int) -> DerivativeExpr:
    fn, der = rng.choice(
        [
            ("\\sin", "\\cos"),
            ("\\cos", "-\\sin"),
            ("\\tan", "\\sec^{2}"),
        ]
    )
    if chained:
        k = rng.randint(2, max(2, coef_hi))
        arg = f"{k}{var}"
        body = rf"{fn}({arg})"
        if der.startswith("-"):
            answer = rf"-{k}{der[1:]}({arg})"
        else:
            answer = rf"{k}{der}({arg})"
        return DerivativeExpr(
            body, answer, frozenset({"trig", "algebraic"}), frozenset({"chain"}), 1
        )
    body = rf"{fn}({var})"
    answer = f"{der}({var})"
    return DerivativeExpr(body, answer, frozenset({"trig"}), frozenset({"power"}), 0)


def _atom_exp(rng: random.Random, var: str, *, chained: bool, coef_hi: int) -> DerivativeExpr:
    if chained:
        a, b = _linear_pair(rng, coef_hi)
        inner = format_linear_latex(a, b, variable=var)
        body = rf"e^{{{inner}}}"
        answer = rf"{a}e^{{{inner}}}"
        return DerivativeExpr(
            body, answer, frozenset({"exp", "algebraic"}), frozenset({"chain"}), 1
        )
    body = rf"e^{{{var}}}"
    return DerivativeExpr(body, body, frozenset({"exp"}), frozenset({"power"}), 0)


def _atom_log(rng: random.Random, var: str, *, chained: bool, coef_hi: int) -> DerivativeExpr:
    if chained:
        a, b = _linear_pair(rng, coef_hi)
        inner = format_linear_latex(a, b, variable=var)
        body = rf"\ln\left({inner}\right)"
        answer = rf"\frac{{{a}}}{{{inner}}}"
        return DerivativeExpr(
            body, answer, frozenset({"log", "algebraic"}), frozenset({"chain"}), 1
        )
    body = rf"\ln({var})"
    answer = rf"\frac{{1}}{{{var}}}"
    return DerivativeExpr(body, answer, frozenset({"log"}), frozenset({"power"}), 0)


def _atom_roots(rng: random.Random, var: str, *, chained: bool, coef_hi: int) -> DerivativeExpr:
    if chained:
        a = rng.choice([1, 4, 9])
        b = rng.randint(0, max(1, coef_hi))
        inner = _mono(a, var, 1) if b == 0 else format_linear_latex(a, b, variable=var)
        body = rf"\sqrt{{{inner}}}"
        std = format_linear_latex(a, b, variable=var)
        answer = rf"\frac{{{a}}}{{2\sqrt{{{std}}}}}"
        return DerivativeExpr(
            body, answer, frozenset({"roots", "algebraic"}), frozenset({"chain"}), 1
        )
    p, q = rng.choice([(1, 2), (3, 2), (2, 3)])
    body = rf"{var}^{{{p}/{q}}}"
    coef = frac_latex(Fraction(p, q))
    g = Fraction(p - q, q)
    if g.denominator == 1:
        exp = str(g.numerator)
    else:
        exp = rf"{g.numerator}/{g.denominator}"
    answer = rf"{coef}{var}^{{{exp}}}"
    return DerivativeExpr(body, answer, frozenset({"roots", "algebraic"}), frozenset({"power"}), 0)


def _atom_invtrig(rng: random.Random, var: str, *, chained: bool, coef_hi: int) -> DerivativeExpr:
    fn = rng.choice(["\\arcsin", "\\arctan", "\\arccos"])
    if chained:
        k = rng.randint(2, max(2, min(5, coef_hi)))
        arg = f"{k}{var}"
        body = rf"{fn}({arg})"
        if fn == "\\arcsin":
            answer = rf"\frac{{{k}}}{{\sqrt{{1-({k}{var})^{{2}}}}}}"
        elif fn == "\\arccos":
            answer = rf"-\frac{{{k}}}{{\sqrt{{1-({k}{var})^{{2}}}}}}"
        else:
            answer = rf"\frac{{{k}}}{{1+({k}{var})^{{2}}}}"
        return DerivativeExpr(
            body, answer, frozenset({"invtrig", "algebraic"}), frozenset({"chain"}), 1
        )
    body = rf"{fn}({var})"
    if fn == "\\arcsin":
        answer = rf"\frac{{1}}{{\sqrt{{1-{var}^{{2}}}}}}"
    elif fn == "\\arccos":
        answer = rf"-\frac{{1}}{{\sqrt{{1-{var}^{{2}}}}}}"
    else:
        answer = rf"\frac{{1}}{{1+{var}^{{2}}}}"
    return DerivativeExpr(body, answer, frozenset({"invtrig"}), frozenset({"power"}), 0)


def _atom_hyperbolic(rng: random.Random, var: str, *, chained: bool, coef_hi: int) -> DerivativeExpr:
    fn, der = rng.choice([("\\sinh", "\\cosh"), ("\\cosh", "\\sinh")])
    if chained:
        k = rng.randint(2, max(2, coef_hi))
        arg = f"{k}{var}"
        body = rf"{fn}({arg})"
        answer = rf"{k}{der}({arg})"
        return DerivativeExpr(
            body, answer, frozenset({"hyperbolic", "algebraic"}), frozenset({"chain"}), 1
        )
    body = rf"{fn}({var})"
    answer = rf"{der}({var})"
    return DerivativeExpr(body, answer, frozenset({"hyperbolic"}), frozenset({"power"}), 0)


def _atom_linear(rng: random.Random, var: str, coef_hi: int) -> DerivativeExpr:
    return _from_poly_pair(poly_expr.sample_linear_atom(rng, var, coef_hi))


def _compose_power(
    rng: random.Random, inner: DerivativeExpr, var: str, power_max: int
) -> DerivativeExpr:
    """(inner)^n — classic chain + power (OpenStax 3.6)."""
    pair = poly_expr.compose_power(
        rng,
        poly_expr.PolyLatexPair(
            inner.body_latex,
            inner.deriv_latex,
            inner.function_classes,
            inner.methods_used,
            inner.chain_depth,
        ),
        var,
        power_max,
    )
    return _from_poly_pair(pair)


def _product(left: DerivativeExpr, right: DerivativeExpr, rng: random.Random) -> DerivativeExpr:
    pair = poly_expr.product_pair(
        poly_expr.PolyLatexPair(
            left.body_latex,
            left.deriv_latex,
            left.function_classes,
            left.methods_used,
            left.chain_depth,
        ),
        poly_expr.PolyLatexPair(
            right.body_latex,
            right.deriv_latex,
            right.function_classes,
            right.methods_used,
            right.chain_depth,
        ),
        rng,
    )
    return _from_poly_pair(pair)


def _quotient(num: DerivativeExpr, den: DerivativeExpr) -> DerivativeExpr:
    return _from_poly_pair(
        poly_expr.quotient_pair(
            poly_expr.PolyLatexPair(
                num.body_latex,
                num.deriv_latex,
                num.function_classes,
                num.methods_used,
                num.chain_depth,
            ),
            poly_expr.PolyLatexPair(
                den.body_latex,
                den.deriv_latex,
                den.function_classes,
                den.methods_used,
                den.chain_depth,
            ),
        )
    )


def _spec_pair_to_expr(pair: poly_expr.PolyLatexPair) -> DerivativeExpr:
    return _from_poly_pair(pair)


def _fn_class_names(classes: Sequence[FunctionClass]) -> frozenset[str]:
    """Map FunctionClass labels onto Spec ``allowed_functions`` tokens."""
    out: set[str] = set()
    for c in classes:
        if c == "trig":
            out.add("trig")
        elif c == "exp":
            out.add("exp")
        elif c == "log":
            out.add("log")
        elif c == "invtrig":
            out.add("invtrig")
        elif c == "hyperbolic":
            out.add("hyperbolic")
        elif c == "roots":
            out.add("roots")
            out.add("sqrt")
    return frozenset(out)


def _exponent_overrides(structure: dict[str, Any]) -> dict[str, Any]:
    """Pass-through Spec exponent flags when explicitly set in structure/settings."""
    out: dict[str, Any] = {}
    for key in (
        "allow_integer_exponents",
        "allow_fractional_exponents",
        "allow_irrational_exponents",
        "allow_negative_exponents",
    ):
        val = structure.get(key)
        if val is not None:
            out[key] = bool(val)
    irr_set = structure.get("irrational_exponent_set")
    if irr_set is not None:
        out["irrational_exponent_set"] = frozenset(irr_set)
    return out


def _pick_atom(
    rng: random.Random,
    var: str,
    coef_hi: int,
    power_max: int,
    *,
    classes: Sequence[FunctionClass],
    prefer_chain: bool,
    extra_term: bool,
) -> DerivativeExpr:
    cls = rng.choice(list(classes) if classes else ["algebraic"])
    chained = prefer_chain and cls != "algebraic"
    if cls == "trig":
        return _atom_trig(rng, var, chained=chained or prefer_chain, coef_hi=coef_hi)
    if cls == "exp":
        return _atom_exp(rng, var, chained=chained or prefer_chain, coef_hi=coef_hi)
    if cls == "log":
        return _atom_log(rng, var, chained=chained or prefer_chain, coef_hi=coef_hi)
    if cls == "roots":
        return _atom_roots(rng, var, chained=chained, coef_hi=coef_hi)
    if cls == "invtrig":
        return _atom_invtrig(rng, var, chained=chained or prefer_chain, coef_hi=coef_hi)
    if cls == "hyperbolic":
        return _atom_hyperbolic(rng, var, chained=chained or prefer_chain, coef_hi=coef_hi)
    return _atom_poly(rng, var, coef_hi, power_max, extra_term=extra_term)


def _available_classes(
    purchased: set[str],
    allow: DerivativeAllowConfig,
    *,
    structure: dict[str, Any],
) -> list[FunctionClass]:
    classes: list[FunctionClass] = ["algebraic"]
    # Prefer D-unlocked structure flags; fall back to purchased class upgrades
    mapping: list[tuple[str, str, FunctionClass]] = [
        ("allow_trig", "class_trig", "trig"),
        ("allow_exp", "class_exp", "exp"),
        ("allow_log", "class_log", "log"),
        ("allow_roots", "class_roots", "roots"),
        ("allow_invtrig", "class_invtrig", "invtrig"),
        ("allow_hyperbolic", "class_hyperbolic", "hyperbolic"),
    ]
    for struct_key, upgrade_id, cls in mapping:
        if not allow.class_allowed(cls):
            continue
        if structure.get(struct_key) or upgrade_id in purchased:
            classes.append(cls)
    return classes


def _sample_via_spec(
    rng: random.Random,
    *,
    key: str | None,
    var: str,
    coef_hi: int,
    power_max: int,
    d: float,
    allow: DerivativeAllowConfig,
    classes: list[FunctionClass],
    structure: dict[str, Any],
    force_product: bool,
    force_chain: bool,
    prefer_chain: bool,
    deep_chain: bool,
    extra_term: bool,
    want_mix: bool,
    allow_fn_power: bool = False,
    derivative_order: int = 1,
    catalog_fid: str = "",
) -> tuple[DerivativeExpr, dict[str, Any]]:
    """Route power / product / alg-chain / specials / general through ExpressionSpec packs.

    When ``catalog_fid`` maps to an ``expr_skeleton`` pattern, fill that pattern
    (OpenStax form → structure → hole fill) and skip pack-only sampling.
    """
    order = max(1, int(derivative_order))
    if catalog_fid:
        from question_engine.frameworks.primitives.expr_skeleton import (
            has_form_pattern,
            sample_from_form,
        )

        if has_form_pattern(catalog_fid):
            try:
                _skel_allows = {
                    "allow_trig": bool(allow.allow_trig) or "trig" in classes,
                    "allow_exp": bool(allow.allow_exp) or "exp" in classes,
                    "allow_log": bool(allow.allow_log) or "log" in classes,
                    "allow_roots": bool(structure.get("allow_roots"))
                    or "roots" in classes,
                    "allow_invtrig": bool(allow.allow_invtrig) or "invtrig" in classes,
                }
                expr_ast, _d_ast, body, deriv, inv = sample_from_form(
                    catalog_fid,
                    conceptual_d=float(d),
                    allows=_skel_allows,
                    rng=rng,
                    var=var,
                    derivative_order=order,
                )
                inv = dict(inv)
                inv.setdefault(
                    "spec_snapshot",
                    {
                        "pack": "expr_skeleton",
                        "skeleton_pattern": inv.get("skeleton_pattern"),
                        "skeleton_kind": inv.get("skeleton_kind"),
                        "derivative_order": order,
                        "variable": var,
                        "coef_abs_max": coef_hi,
                        "degree_max": power_max,
                    },
                )
                methods = frozenset(inv.get("methods_used") or [])
                classes_set = frozenset(inv.get("function_classes") or [])
                pair = poly_expr.PolyLatexPair(
                    body_latex=body,
                    deriv_latex=deriv,
                    function_classes=classes_set
                    or poly_expr.function_classes_of(expr_ast),
                    methods_used=methods or poly_expr.methods_used_of(expr_ast),
                    chain_depth=int(
                        inv.get("chain_depth") or poly_expr.chain_depth_of(expr_ast)
                    ),
                )
                return _from_poly_pair(pair), inv
            except Exception:
                pass

    fn_tokens = _fn_class_names([c for c in classes if c != "algebraic"])

    require_fn: str | None = None
    if key == "derivative_trigonometric" and allow.allow_trig:
        require_fn = "trig"
        # Topic-primary: do not inherit off-topic purchased classes
        fn_tokens = frozenset({"trig"})
    elif key == "derivative_ln_exp":
        toks: set[str] = set()
        if allow.allow_exp:
            toks.add("exp")
        if allow.allow_log:
            toks.add("log")
        if allow.allow_exp and allow.allow_log:
            require_fn = rng.choice(["exp", "log"])
        elif allow.allow_exp:
            require_fn = "exp"
        elif allow.allow_log:
            require_fn = "log"
        fn_tokens = frozenset(toks) if toks else frozenset()
        if require_fn and require_fn not in fn_tokens:
            fn_tokens = fn_tokens | frozenset({require_fn})
    elif key == "derivative_inverse_trig" and allow.allow_invtrig:
        require_fn = "invtrig"
        fn_tokens = frozenset({"invtrig"})
    elif key == "derivative_higher_order":
        # Mostly poly power-rule; occasionally trig/exp atoms when D unlocks them.
        specials = [c for c in ("trig", "exp") if c in classes]
        p_special = 0.0 if d < 8 else (0.3 if d < 16 else (0.45 if d < 22 else 0.55))
        if specials and rng.random() < p_special:
            require_fn = rng.choice(specials)
            fn_tokens = frozenset({require_fn})

    specialty_topic = key in {
        "derivative_trigonometric",
        "derivative_ln_exp",
        "derivative_inverse_trig",
    }
    general_topic = key == "derivative_general"
    # Structure D-unlocks + purchased classes → specials enter the same Spec sampler
    specials_on = bool(fn_tokens) and (
        structure.get("allow_trig")
        or structure.get("allow_exp")
        or structure.get("allow_log")
        or structure.get("allow_roots")
        or structure.get("allow_invtrig")
        or structure.get("allow_hyperbolic")
        or any(
            allow.class_allowed(c)
            for c in ("trig", "exp", "log", "invtrig", "hyperbolic", "roots")
            if c in classes
        )
    )
    # Specialty: mix only within topic tokens (log↔exp). Never pull trig into ln-exp.
    if specialty_topic:
        mix = key == "derivative_ln_exp" and "exp" in fn_tokens and "log" in fn_tokens
    else:
        mix = bool(want_mix or general_topic) and len(fn_tokens) >= 2

    # Fn-powers unlock early; allowed on order=2 (safer bases) but not order≥3
    fn_power = bool(allow_fn_power and order <= 2 and d >= 6)
    exp_ov = _exponent_overrides(structure)

    if general_topic:
        spec = poly_expr.pack_general_derivatives(
            d,
            coef_hi=coef_hi,
            power_max=power_max,
            extra_term=extra_term and order == 1,
            deep_chain=(deep_chain or mix) and order == 1,
            variable=var,
            allowed_functions=fn_tokens,
            allow_product=bool(
                structure.get("allow_product") or allow.allow_product or allow.require_product
            ),
            allow_fn_power=fn_power,
            mix_fn_classes=mix or len(fn_tokens) >= 2,
            derivative_order=order,
            **exp_ov,
        )
    elif specialty_topic and require_fn and not force_product and not force_chain:
        # Specialty leaf: multi-Fn products / nested chains via pack_special_atom
        spec = poly_expr.pack_special_atom(
            d,
            primary=require_fn,
            coef_hi=coef_hi,
            power_max=power_max,
            prefer_chained_fn=prefer_chain or d >= 6,
            variable=var,
            allowed_functions=fn_tokens or frozenset({require_fn}),
            mix_fn_classes=mix,
            allow_fn_power=fn_power,
            derivative_order=order,
            **exp_ov,
        )
    elif force_product or (specialty_topic and require_fn and force_product):
        product_fns: frozenset[str] = frozenset()
        if require_fn:
            product_fns = fn_tokens or frozenset({require_fn})
        elif specials_on and fn_tokens:
            product_fns = fn_tokens
        spec = poly_expr.pack_product_rule(
            d,
            coef_hi=coef_hi,
            power_max=power_max,
            extra_term=extra_term and not bool(product_fns) and order == 1,
            variable=var,
            allowed_functions=product_fns,
            prefer_chained_fn=prefer_chain and bool(product_fns),
            require_function=require_fn,
            prefer_special_structure=bool(require_fn) or specialty_topic,
            mix_fn_classes=mix,
            allow_fn_power=fn_power,
            derivative_order=order,
            **exp_ov,
        )
    elif force_chain:
        if require_fn or (specials_on and fn_tokens and specialty_topic):
            primary = require_fn or (
                "trig" if "trig" in fn_tokens else next(iter(fn_tokens))
            )
            # Specialty under chain: use special-atom pack (products + nest)
            if specialty_topic:
                spec = poly_expr.pack_special_atom(
                    d,
                    primary=primary,
                    coef_hi=coef_hi,
                    power_max=power_max,
                    prefer_chained_fn=True,
                    variable=var,
                    allowed_functions=fn_tokens or frozenset({primary}),
                    mix_fn_classes=mix,
                    allow_fn_power=fn_power,
                    derivative_order=order,
                    **exp_ov,
                )
            else:
                spec = poly_expr.pack_algebraic_chain(
                    d,
                    coef_hi=coef_hi,
                    power_max=power_max,
                    extra_term=extra_term and order == 1,
                    deep_chain=(deep_chain or mix) and order == 1,
                    variable=var,
                    allowed_functions=fn_tokens,
                    prefer_chained_fn=True,
                    require_function=None if mix else primary,
                    prefer_special_structure=True,
                    mix_fn_classes=mix,
                    allow_fn_power=fn_power,
                    derivative_order=order,
                    **exp_ov,
                )
        elif specials_on and fn_tokens and rng.random() < (
            0.85
            if mix or any(c in fn_tokens for c in ("trig", "exp", "log", "invtrig"))
            else 0.45
        ):
            primary = require_fn or rng.choice(sorted(fn_tokens))
            spec = poly_expr.pack_algebraic_chain(
                d,
                coef_hi=coef_hi,
                power_max=power_max,
                extra_term=extra_term and order == 1,
                deep_chain=(deep_chain or mix or primary in {"trig", "exp", "sin", "cos"})
                and order == 1,
                variable=var,
                allowed_functions=fn_tokens,
                prefer_chained_fn=True,
                # Mixed chain: no single primary so nests can be heterogeneous
                require_function=None if mix else primary,
                prefer_special_structure=True,
                mix_fn_classes=mix or len(fn_tokens) >= 2,
                allow_fn_power=fn_power,
                derivative_order=order,
                **exp_ov,
            )
        else:
            spec = poly_expr.pack_algebraic_chain(
                d,
                coef_hi=coef_hi,
                power_max=power_max,
                extra_term=extra_term and order == 1,
                deep_chain=deep_chain and order == 1,
                variable=var,
                allowed_functions=frozenset(),
                prefer_chained_fn=False,
                derivative_order=order,
                **exp_ov,
            )
    elif require_fn:
        # Bare specialty atom path
        spec = poly_expr.pack_special_atom(
            d,
            primary=require_fn,
            coef_hi=coef_hi,
            power_max=power_max,
            prefer_chained_fn=prefer_chain or d >= 6,
            variable=var,
            allowed_functions=fn_tokens or frozenset({require_fn}),
            mix_fn_classes=mix,
            allow_fn_power=fn_power,
            derivative_order=order,
            **exp_ov,
        )
    elif key == "derivative_power_rule":
        allow_roots = bool(structure.get("allow_roots")) and "roots" in classes and d >= 4
        spec = poly_expr.pack_power_rule(
            d,
            coef_hi=coef_hi,
            power_max=power_max,
            extra_term=extra_term,
            allow_roots=allow_roots,
            variable=var,
            derivative_order=order,
            **exp_ov,
        )
    else:
        spec = poly_expr.pack_power_rule(
            d,
            coef_hi=coef_hi,
            power_max=power_max,
            extra_term=extra_term,
            allow_roots=False,
            variable=var,
            derivative_order=order,
            **exp_ov,
        )

    expr_ast, _d_ast, body, deriv, inv = poly_expr.sample_and_differentiate(spec, rng=rng)
    inv = dict(inv)
    inv["spec_snapshot"] = poly_expr.spec_snapshot(spec)
    pair = poly_expr.PolyLatexPair(
        body_latex=body,
        deriv_latex=deriv,
        function_classes=poly_expr.function_classes_of(expr_ast),
        methods_used=poly_expr.methods_used_of(expr_ast),
        chain_depth=poly_expr.chain_depth_of(expr_ast),
    )
    return _from_poly_pair(pair), inv


def sample_derivative_expression(
    settings: dict[str, Any],
    *,
    generator_key: str | None = None,
    topic: str | None = None,
    rng: random.Random | None = None,
) -> DerivativeSample:
    """Sample one derivative problem respecting allow-lists + continuous D."""
    if rng is None:
        rng, dress_rng = dual_axis_rngs(settings, xor_mask=0xD311)
    else:
        dress_rng = rng
    key = generator_key or resolve_generator_key(topic)
    allow = resolve_derivative_allows(settings, generator_key=key, topic=topic)
    d = settings_difficulty(settings, default=6.0)
    structure = derivative_rule_structure(settings, generator_key=key, topic=topic)
    coef_hi = int(structure["coef_hi"])
    power_max = int(structure["power_max"])
    band = str(structure["band"])
    var = str(settings.get("variable", "x"))

    force_methods: set[str] = set()
    if allow.require_product:
        force_methods.add("product")
    if allow.require_quotient:
        force_methods.add("quotient")
    if allow.require_chain:
        force_methods.add("chain")

    # OpenStax form catalog — textbook case label + structure hints
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        catalog_form_meta,
        forms_for_leaf,
        load_form_catalog,
        select_form_id,
    )

    deriv_catalog = load_form_catalog("derivatives")
    deriv_forms = forms_for_leaf(deriv_catalog, key or "")
    catalog_form = (
        select_form_id(deriv_forms, d=d, rng=rng) if deriv_forms else None
    )
    catalog_fid = str(catalog_form["form_id"]) if catalog_form else ""
    if catalog_fid.startswith("product"):
        force_methods.add("product")
    elif catalog_fid.startswith("quotient"):
        force_methods.add("quotient")
    elif catalog_fid.startswith("chain"):
        force_methods.add("chain")
    elif catalog_fid.startswith("power"):
        force_methods.discard("product")
        force_methods.discard("quotient")

    allowed_ids = _allowed_upgrade_ids(allow, force_methods=force_methods)
    upgrades = _derivative_upgrades()
    purchased, _, _ = select_upgrades(upgrades, d, allowed_ids=allowed_ids, rng=rng)
    purchased_ids = {f.id for f in purchased}

    if allow.require_product:
        purchased_ids.add("use_product")
    if allow.require_quotient:
        purchased_ids.add("use_quotient")
    if allow.require_chain:
        purchased_ids.add("use_chain")
    if catalog_fid.startswith("product"):
        purchased_ids.add("use_product")
    if catalog_fid.startswith("quotient"):
        purchased_ids.add("use_quotient")
    if catalog_fid.startswith("chain") or catalog_fid in {
        "trig_product_chain",
        "invtrig_chained",
        "ln_exp_product",
    }:
        purchased_ids.add("use_chain")
    if catalog_fid == "chain_nested":
        purchased_ids.add("use_chain")
        purchased_ids.add("chain_depth_2")
    if catalog_fid == "power_root":
        purchased_ids.add("use_roots")

    classes = _available_classes(purchased_ids, allow, structure=structure)
    if key == "derivative_trigonometric" and allow.allow_trig and "trig" not in classes:
        classes.append("trig")
    if key == "derivative_ln_exp":
        if allow.allow_exp and "exp" not in classes:
            classes.append("exp")
        if allow.allow_log and "log" not in classes:
            classes.append("log")
    if key == "derivative_inverse_trig" and allow.allow_invtrig and "invtrig" not in classes:
        classes.append("invtrig")
    if key == "derivative_general":
        # Soft-on defaults: ensure allowed classes appear once D unlocks them
        for cls, flag in (
            ("trig", allow.allow_trig and structure.get("allow_trig")),
            ("exp", allow.allow_exp and structure.get("allow_exp")),
            ("log", allow.allow_log and structure.get("allow_log")),
            ("roots", allow.allow_roots and structure.get("allow_roots")),
            ("invtrig", allow.allow_invtrig and structure.get("allow_invtrig")),
            ("hyperbolic", allow.allow_hyperbolic and structure.get("allow_hyperbolic")),
        ):
            if flag and cls not in classes:
                classes.append(cls)  # type: ignore[arg-type]

    want_mix = "mix_classes" in purchased_ids and len(classes) >= 2
    if key == "derivative_general" and len([c for c in classes if c != "algebraic"]) >= 2:
        want_mix = True
    prefer_chain = "use_chain" in purchased_ids or allow.require_chain
    deep_chain = "chain_depth_2" in purchased_ids and structure.get("allow_nested")
    # Chain / general with many classes: allow deep nests without waiting for nested unlock
    if key in {"derivative_chain_rule", "derivative_general"} and want_mix and d >= 12:
        deep_chain = True
    extra_term = "extra_term" in purchased_ids or "higher_power" in purchased_ids
    use_product = "use_product" in purchased_ids and (
        structure.get("allow_product") or allow.require_product
    )
    use_quotient = "use_quotient" in purchased_ids and (
        structure.get("allow_quotient") or allow.require_quotient
    )
    allow_fn_power = "fn_power" in purchased_ids or d >= 8.0
    derivative_order = _derivative_order_for_sample(
        d, purchased_ids, rng, key=key
    )
    if catalog_fid == "higher_order_2":
        derivative_order = 2
    elif catalog_fid == "higher_order_3":
        derivative_order = 3

    force_chain = (
        allow.require_chain
        or key == "derivative_chain_rule"
        or catalog_fid.startswith("chain")
        or (key == "derivative_general" and prefer_chain and not use_product)
    )
    force_product = (
        allow.require_product
        or key == "derivative_product_rule"
        or catalog_fid.startswith("product")
    )
    force_quotient = (
        allow.require_quotient
        or key == "derivative_quotient_rule"
        or catalog_fid.startswith("quotient")
    )
    specialty_topic = key in {
        "derivative_trigonometric",
        "derivative_ln_exp",
        "derivative_inverse_trig",
    }
    general_topic = key == "derivative_general"
    higher_order_topic = key == "derivative_higher_order"

    inventory: dict[str, Any] = {}

    # Specialty leaves + general + higher-order always use Spec packs.
    # Legacy quotient sampling must not steal trig/ln-exp/invtrig/general topics.
    if specialty_topic or general_topic or higher_order_topic:
        expr, inventory = _sample_via_spec(
            rng,
            key=key,
            var=var,
            coef_hi=coef_hi,
            power_max=power_max,
            d=d,
            allow=allow,
            classes=classes,
            structure=structure,
            force_product=bool(
                force_product or (use_product and not (force_chain or prefer_chain))
            ),
            force_chain=bool(force_chain or prefer_chain or general_topic),
            prefer_chain=prefer_chain or general_topic,
            deep_chain=bool(deep_chain),
            extra_term=extra_term,
            want_mix=want_mix,
            allow_fn_power=allow_fn_power,
            derivative_order=derivative_order,
            catalog_fid=catalog_fid,
        )
    elif force_quotient or (use_quotient and not force_product and not force_chain):
        # Prefer OpenStax quotient patterns when mapped.
        from question_engine.frameworks.primitives.expr_skeleton import (
            has_form_pattern,
            sample_from_form,
        )

        if catalog_fid and has_form_pattern(catalog_fid):
            try:
                _skel_allows = {
                    "allow_trig": bool(allow.allow_trig) or "trig" in classes,
                    "allow_exp": bool(allow.allow_exp) or "exp" in classes,
                    "allow_log": bool(allow.allow_log) or "log" in classes,
                    "allow_roots": bool(structure.get("allow_roots"))
                    or "roots" in classes,
                    "allow_invtrig": bool(allow.allow_invtrig) or "invtrig" in classes,
                }
                expr_ast, _d_ast, body_q, deriv_q, inv_q = sample_from_form(
                    catalog_fid,
                    conceptual_d=float(d),
                    allows=_skel_allows,
                    rng=rng,
                    var=var,
                    derivative_order=1,
                )
                inv_q = dict(inv_q)
                inv_q.setdefault(
                    "spec_snapshot",
                    {
                        "pack": "expr_skeleton",
                        "skeleton_pattern": inv_q.get("skeleton_pattern"),
                        "skeleton_kind": inv_q.get("skeleton_kind"),
                        "derivative_order": 1,
                        "variable": var,
                        "coef_abs_max": coef_hi,
                        "degree_max": power_max,
                        "allow_quotient": True,
                    },
                )
                pair = poly_expr.PolyLatexPair(
                    body_latex=body_q,
                    deriv_latex=deriv_q,
                    function_classes=frozenset(
                        inv_q.get("function_classes")
                        or poly_expr.function_classes_of(expr_ast)
                    ),
                    methods_used=frozenset(
                        inv_q.get("methods_used")
                        or poly_expr.methods_used_of(expr_ast)
                    ),
                    chain_depth=int(
                        inv_q.get("chain_depth")
                        or poly_expr.chain_depth_of(expr_ast)
                    ),
                )
                expr = _from_poly_pair(pair)
                inventory = inv_q
                inventory["derivative_order"] = 1
            except Exception:
                catalog_fid_quot_fail = True
            else:
                catalog_fid_quot_fail = False
        else:
            catalog_fid_quot_fail = True

        if catalog_fid_quot_fail:
            if want_mix:
                c1, c2 = (
                    rng.sample(classes, 2)
                    if len(classes) >= 2
                    else (classes[0], "algebraic")
                )
                num = _pick_atom(
                    rng,
                    var,
                    coef_hi,
                    power_max,
                    classes=[c1],
                    prefer_chain=prefer_chain,
                    extra_term=False,
                )
                den = _pick_atom(
                    rng,
                    var,
                    coef_hi,
                    power_max,
                    classes=[c2],
                    prefer_chain=False,
                    extra_term=False,
                )
            else:
                num = _pick_atom(
                    rng,
                    var,
                    coef_hi,
                    power_max,
                    classes=classes,
                    prefer_chain=prefer_chain,
                    extra_term=extra_term,
                )
                den = _atom_linear(rng, var, coef_hi)
            expr = _quotient(num, den)
            derivative_order = 1  # quotient path stays first-order
            # Legacy (non-Spec) quotient: still emit joinable structure / effort hints.
            inventory = {
                "shape_id": "quotient",
                "nest_depth": int(expr.chain_depth),
                "n_terms": 2,
                "n_factors": 0,
                "has_fn_power": False,
                "derivative_order": 1,
                "effort_features": {
                    "answer_len": len(expr.deriv_latex or ""),
                    "nest_depth": int(expr.chain_depth),
                    "chain_applications": int(expr.chain_depth),
                    "product_applications": 0,
                    "quotient_applications": 1,
                    "n_factors": 0,
                    "n_terms": 2,
                    "degree_max": power_max,
                    "coef_abs_max": coef_hi,
                    "has_fn_power": False,
                    "derivative_order": 1,
                    "methods": sorted(expr.methods_used),
                    "n_fn_nodes": sum(
                        1
                        for c in expr.function_classes
                        if c not in {"algebraic", "roots"}
                    ),
                },
                # Not a full ExpressionSpec; record resolved exponent / method θ instead.
                "spec_snapshot": {
                    "pack": "legacy_quotient",
                    "allow_quotient": True,
                    "require_quotient": bool(allow.require_quotient),
                    "allow_integer_exponents": True,
                    "allow_fractional_exponents": bool(structure.get("allow_roots")),
                    "allow_irrational_exponents": False,
                    "allow_negative_exponents": bool(
                        structure.get("allow_negative_exponents")
                    ),
                    "derivative_order": 1,
                    "coef_abs_max": coef_hi,
                    "degree_max": power_max,
                    "variable": var,
                },
            }
    else:
        expr, inventory = _sample_via_spec(
            rng,
            key=key,
            var=var,
            coef_hi=coef_hi,
            power_max=power_max,
            d=d,
            allow=allow,
            classes=classes,
            structure=structure,
            force_product=bool(force_product or (use_product and not force_chain)),
            force_chain=bool(force_chain or prefer_chain),
            prefer_chain=prefer_chain,
            deep_chain=bool(deep_chain),
            extra_term=extra_term,
            want_mix=want_mix,
            allow_fn_power=allow_fn_power,
            derivative_order=derivative_order,
            catalog_fid=catalog_fid,
        )

    order = int(inventory.get("derivative_order") or derivative_order or 1)
    body = expr.body_latex
    undressed_body = body
    # Spec identity extras (thin): demoted cancel wraps stay weight 0.
    _spec_d = settings_spec_difficulty(settings)
    if _spec_d is not None and float(_spec_d) > 0:
        from question_engine.frameworks.primitives.expression_flesh import (
            flesh_from_skeleton,
            flesh_meta,
            stamp_flesh_sources,
        )

        dressed_body, wraps = flesh_from_skeleton(
            body,
            float(_spec_d),
            dress_rng,
            var=var,
            leaf=key,
            allows={
                "allow_trig": "trig" in classes,
                "allow_exp": "exp" in classes,
                "allow_log": "log" in classes,
                "allow_roots": "roots" in classes,
                "allow_invtrig": "invtrig" in classes,
            },
        )
        if wraps:
            body = dressed_body
            expr = DerivativeExpr(
                body_latex=body,
                deriv_latex=expr.deriv_latex,
                function_classes=expr.function_classes,
                methods_used=expr.methods_used,
                chain_depth=expr.chain_depth,
            )
            inventory = dict(inventory)
            inventory.update(
                flesh_meta(undressed_body=undressed_body, wrappers=wraps)
            )
            inventory["difficulty_sources_extra"] = stamp_flesh_sources(wraps)
    if order >= 3:
        prompt = rf"\frac{{d^{{3}}}}{{d{var}^{{3}}}}\left[{body}\right]"
    elif order == 2:
        prompt = rf"\frac{{d^{{2}}}}{{d{var}^{{2}}}}\left[{body}\right]"
    elif rng.choice([True, False]):
        prompt = rf"\frac{{d}}{{d{var}}}\left[{body}\right]"
    else:
        prompt = rf"\text{{Find }}\frac{{d}}{{d{var}}}\left({body}\right)"

    classes_sorted = tuple(sorted(expr.function_classes))
    methods_sorted = tuple(sorted(expr.methods_used))
    meta: dict[str, Any] = {
        "generator": key or "",
        "variable": var,
        "derivative_order": order,
        "d_spend": d,
    }
    if catalog_form:
        meta.update(catalog_form_meta(catalog_form, deriv_catalog))
        meta["form_id"] = catalog_fid
        meta["openstax_form"] = catalog_fid
    elif catalog_fid:
        meta["form_id"] = catalog_fid
        meta["openstax_form"] = catalog_fid
    if inventory:
        for field_name in (
            "shape_id",
            "nest_depth",
            "degree_max",
            "n_terms",
            "n_factors",
            "ops",
            "has_fn_power",
            "effort_features",
            "spec_snapshot",
            "core_form_id",
            "skeleton_source",
            "skeleton_pattern",
            "skeleton_kind",
            "productions",
            "shared_inner",
            "undressed_body_latex",
            "wrappers_applied",
            "spec_answer_preserved",
            "expression_flesh",
            "spec_presentation",
            "difficulty_sources_extra",
        ):
            if field_name in inventory:
                meta[field_name] = inventory[field_name]
    return DerivativeSample(
        prompt_latex=prompt,
        answer_latex=expr.deriv_latex,
        function_classes=classes_sorted,
        methods_used=methods_sorted,
        chain_depth=int(expr.chain_depth),
        upgrades=tuple(sorted(purchased_ids)),
        effective_d=d,
        allow=allow,
        band=band,
        coef_hi=coef_hi,
        power_max=power_max,
        term_budget=int(structure["term_budget"]),
        metadata=meta,
    )


def sample_derivative_problem(
    topic: str,
    settings: dict[str, Any],
    *,
    generator_key: str | None = None,
) -> tuple[str, str, str | None, dict[str, Any]]:
    """Convenience for generators: (prompt, label, answer|None, metadata)."""
    include_answer_key = bool(settings.get("include_answer_key", False))
    sample = sample_derivative_expression(
        settings, generator_key=generator_key, topic=topic
    )
    label = {
        "derivative_power_rule": "power rule derivative",
        "derivative_product_rule": "product rule",
        "derivative_quotient_rule": "quotient rule",
        "derivative_chain_rule": "chain rule",
        "derivative_trigonometric": "trigonometric derivative",
        "derivative_ln_exp": "ln/exp derivative",
        "derivative_other_base": "other-base derivative",
        "derivative_inverse_trig": "inverse trigonometric derivative",
        "derivative_implicit": "implicit differentiation",
        "derivative_logarithmic": "logarithmic differentiation",
        "derivative_higher_order": "higher order derivative",
        "derivative_general": "general derivative",
    }.get(generator_key or "", "derivative")
    answer = sample.answer_latex if include_answer_key else None
    return sample.prompt_latex, label, answer, sample.as_metadata()
