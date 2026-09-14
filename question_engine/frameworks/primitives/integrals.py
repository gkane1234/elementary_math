"""Integral Spec + ordered trick pipeline (Calc 1 algebraic).

Hybrid generation strategy
--------------------------
1. **Derivative-backed (inverse)** — ``u_sub`` / chain-style: sample a
   differentiable outer ``F(u(x))`` via ExpressionSpec, take ``F'``, so the
   integrand is solvable by construction (inner′ factor present).

2. **Forward form-based** — technique families (power, trig, ln/exp, invtrig,
   parts, PFD, FTC) sample from closed forms conducive to that technique.

3. **Multi-trick pipelines** — ordered ``tricks_required`` (e.g.
   ``["u_sub", "pfd"]``). Construction starts from a later-stage core
   (PFD-candidate rational), then wraps/composes so earlier tricks become
   necessary. Not random unsolvable stacks.

ML metadata: ``spec_snapshot``, ``tricks_required``, ``pipeline``, θ knobs,
``effort_features``, seed/difficulty join via generator wrappers.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field, replace
from fractions import Fraction
from math import factorial
from typing import Any, Callable, Literal, Sequence

from question_engine.frameworks.difficulty_budget import (
    DifficultyFactor,
    select_upgrades,
    settings_difficulty,
)
from question_engine.generators.utils import (
    format_linear_latex,
    format_monomial_latex,
    format_polynomial_latex,
    frac_latex,
    random_int_range,
)

TrickId = Literal[
    "power",
    "trig",
    "ln_exp",
    "invtrig",
    "u_sub",
    "parts",
    "pfd",
    "ftc",
    "trig_sub",
]

TRICK_ALLOW_KEYS: tuple[str, ...] = (
    "allow_trig",
    "allow_exp",
    "allow_log",
    "allow_invtrig",
    "allow_substitution",
    "allow_parts",
    "allow_pfd",
    "allow_trig_sub",
    "allow_ftc",
    "require_substitution",
    "require_parts",
    "require_pfd",
    "require_trig",
    "require_trig_sub",
    "include_plus_c",
    "definite",
)

# Max pipeline length continuous D can buy (Calc 1 algebraic).
_MAX_PIPELINE_LEN = 3

_TOPIC_DEFAULTS: dict[str, dict[str, bool]] = {
    "integral_power_rule": {
        "allow_trig": False,
        "allow_exp": False,
        "allow_log": False,
        "allow_invtrig": False,
        "allow_substitution": False,
        "allow_parts": False,
        "allow_pfd": False,
        "allow_trig_sub": False,
        "allow_ftc": False,
        "require_substitution": False,
        "require_parts": False,
        "require_pfd": False,
        "require_trig": False,
        "require_trig_sub": False,
        "include_plus_c": True,
        "definite": False,
    },
    "integral_trigonometric": {
        "allow_trig": True,
        "allow_exp": False,
        "allow_log": False,
        "allow_invtrig": False,
        # Catalog forms may use u=sin/cos internally; do not buy a u_sub pipeline.
        "allow_substitution": False,
        "allow_parts": False,
        "allow_pfd": False,
        "allow_trig_sub": False,
        "allow_ftc": False,
        "require_trig": True,
        "include_plus_c": True,
        "definite": False,
    },
    "integral_log_exp": {
        "allow_trig": False,
        "allow_exp": True,
        "allow_log": True,
        "allow_invtrig": False,
        "allow_substitution": False,
        "allow_parts": False,
        "allow_pfd": False,
        "allow_trig_sub": False,
        "allow_ftc": False,
        "include_plus_c": True,
        "definite": False,
    },
    "integral_inverse_trig": {
        "allow_trig": False,
        "allow_exp": False,
        "allow_log": False,
        "allow_invtrig": True,
        "allow_substitution": False,
        "allow_parts": False,
        "allow_pfd": False,
        "allow_trig_sub": False,
        "allow_ftc": False,
        "include_plus_c": True,
        "definite": False,
    },
    "integral_substitution": {
        "allow_trig": False,
        "allow_exp": False,
        "allow_log": False,
        "allow_invtrig": False,
        "allow_substitution": True,
        "allow_parts": False,
        "allow_pfd": False,
        "allow_trig_sub": False,
        "allow_ftc": False,
        "require_substitution": True,
        "include_plus_c": True,
        "definite": False,
    },
    "integral_trig_substitution": {
        "allow_trig": True,
        "allow_exp": False,
        "allow_log": False,
        "allow_invtrig": False,
        "allow_substitution": True,  # optional wrap; not plain u-sub
        "allow_parts": False,
        "allow_pfd": False,
        "allow_trig_sub": True,
        "allow_ftc": False,
        "require_substitution": False,
        "require_trig_sub": True,
        "include_plus_c": True,
        "definite": False,
    },
    "integral_log_exp_substitution": {
        "allow_trig": True,
        "allow_exp": True,
        "allow_log": True,
        "allow_invtrig": False,
        "allow_substitution": True,
        "allow_parts": False,
        "allow_pfd": False,
        "allow_trig_sub": False,
        "allow_ftc": False,
        "require_substitution": True,
        "include_plus_c": True,
        "definite": False,
    },
    "integral_invtrig_substitution": {
        "allow_trig": False,
        "allow_exp": False,
        "allow_log": False,
        "allow_invtrig": True,
        "allow_substitution": True,
        "allow_parts": False,
        "allow_pfd": False,
        "allow_trig_sub": False,
        "allow_ftc": False,
        "require_substitution": True,
        "include_plus_c": True,
        "definite": False,
    },
    "integration_by_parts": {
        "allow_trig": True,
        "allow_exp": True,
        "allow_log": True,
        "allow_invtrig": True,
        "allow_substitution": False,
        "allow_parts": True,
        "allow_pfd": False,
        "allow_trig_sub": False,
        "allow_ftc": False,
        "require_parts": True,
        "include_plus_c": True,
        "definite": False,
    },
    "integral_partial_fractions": {
        "allow_trig": False,
        "allow_exp": False,
        "allow_log": True,
        "allow_invtrig": False,
        "allow_substitution": False,
        "allow_parts": False,
        "allow_pfd": True,
        "allow_trig_sub": False,
        "allow_ftc": False,
        "require_pfd": True,
        "include_plus_c": True,
        "definite": False,
    },
    "integral_multi_trick": {
        "allow_trig": False,
        "allow_exp": False,
        "allow_log": True,
        "allow_invtrig": False,
        "allow_substitution": True,
        "allow_parts": False,
        "allow_pfd": True,
        "allow_trig_sub": False,
        "allow_ftc": False,
        "require_substitution": True,
        "require_pfd": True,
        "include_plus_c": True,
        "definite": False,
    },
    # Mixed technique leaf: checkboxes default ON (like derivative_general).
    "integral_general": {
        "allow_trig": True,
        "allow_exp": True,
        "allow_log": True,
        "allow_invtrig": True,
        "allow_substitution": True,
        "allow_parts": True,
        "allow_pfd": True,
        "allow_trig_sub": True,
        "allow_ftc": False,
        "require_substitution": False,
        "require_parts": False,
        "require_pfd": False,
        "require_trig": False,
        "require_trig_sub": False,
        "include_plus_c": True,
        "definite": False,
    },
    "first_fundamental_theorem": {
        "allow_trig": False,
        "allow_exp": False,
        "allow_log": False,
        "allow_invtrig": False,
        "allow_substitution": False,
        "allow_parts": False,
        "allow_pfd": False,
        "allow_trig_sub": False,
        "allow_ftc": True,
        "include_plus_c": False,
        "definite": True,
    },
    "second_fundamental_theorem": {
        "allow_trig": False,
        "allow_exp": False,
        "allow_log": False,
        "allow_invtrig": False,
        "allow_substitution": True,
        "allow_parts": False,
        "allow_pfd": False,
        "allow_trig_sub": False,
        "allow_ftc": True,
        "include_plus_c": False,
        "definite": True,
    },
    # Definite u-sub with changed limits (OpenStax Vol 1 §5.5).
    "integral_definite_substitution": {
        "allow_trig": False,
        "allow_exp": False,
        "allow_log": False,
        "allow_invtrig": False,
        "allow_substitution": True,
        "allow_parts": False,
        "allow_pfd": False,
        "allow_trig_sub": False,
        "allow_ftc": False,
        "require_substitution": True,
        "include_plus_c": False,
        "definite": True,
    },
}

_TYPE_ID_TO_GENERATOR: dict[str, str] = {
    "calc_indef_int_power_rule": "integral_power_rule",
    "calc_indef_int_trigonometric": "integral_trigonometric",
    "calc_indef_int_logarithmic_rule_and_exponentials": "integral_log_exp",
    "calc_indef_int_inverse_trigonometric": "integral_inverse_trig",
    "calc_indef_int_power_rule_with_substitution": "integral_substitution",
    "calc_indef_int_trigonometric_with_substitution": "integral_trig_substitution",
    "calc_indef_int_logarithmic_rule_and_exponentials_with_substitution": "integral_log_exp_substitution",
    "calc_indef_int_inverse_trigonometric_with_substitution": "integral_invtrig_substitution",
    "calc_indef_int_integration_by_parts": "integration_by_parts",
    "calc_indef_int_partial_fractions": "integral_partial_fractions",
    "calc_indef_int_multi_trick": "integral_multi_trick",
    "calc_indef_int_general": "integral_general",
    "calc_def_int_first_fundamental_theorem_of_calculus": "first_fundamental_theorem",
    "calc_def_int_second_fundamental_theorem_of_calculus": "second_fundamental_theorem",
    "calc_def_int_substitution_with_change_of_variables": "integral_definite_substitution",
    "pc_indefinite_integrals": "integral_power_rule",
}


# ---------------------------------------------------------------------------
# Spec + pipeline types
# ---------------------------------------------------------------------------


@dataclass
class IntegralSpec:
    """Constraint pack for algebraic integral generation."""

    variable: str = "x"
    definite: bool = False
    bound_abs_max: int = 5
    tricks_allowed: frozenset[str] = frozenset({"power"})
    tricks_required: tuple[str, ...] = ()
    allow_trig: bool = False
    allow_exp: bool = False
    allow_log: bool = False
    allow_invtrig: bool = False
    allow_substitution: bool = False
    allow_parts: bool = False
    allow_pfd: bool = False
    allow_trig_sub: bool = False
    allow_ftc: bool = False
    require_substitution: bool = False
    require_parts: bool = False
    require_pfd: bool = False
    require_trig: bool = False
    require_trig_sub: bool = False
    include_plus_c: bool = True
    coef_abs_max: int = 5
    degree_max: int = 4
    term_count_max: int = 3
    nest_budget: int = 1
    parts_depth: int = 1
    max_pipeline_len: int = 1
    d_spend: float = 6.0
    pack: str = "integral_power"
    # Construction mode hints
    construction: str = "forward"  # forward | derivative_backed | pipeline
    # Named OpenStax u-sub family (settings ``u_sub_form_preset``).
    u_sub_form_preset: str = "auto"
    # auto | catalog | reverse_chain
    u_sub_construction: str = "auto"
    # Named IBP / PFD / trig-sub families (settings ``*_form_preset``).
    parts_form_preset: str = "auto"
    pfd_form_preset: str = "auto"
    trig_sub_form_preset: str = "auto"

    def snapshot(self) -> dict[str, Any]:
        return {
            "pack": self.pack,
            "variable": self.variable,
            "definite": self.definite,
            "bound_abs_max": self.bound_abs_max,
            "tricks_allowed": sorted(self.tricks_allowed),
            "tricks_required": list(self.tricks_required),
            "allow_trig": self.allow_trig,
            "allow_exp": self.allow_exp,
            "allow_log": self.allow_log,
            "allow_invtrig": self.allow_invtrig,
            "allow_substitution": self.allow_substitution,
            "allow_parts": self.allow_parts,
            "allow_pfd": self.allow_pfd,
            "allow_trig_sub": self.allow_trig_sub,
            "allow_ftc": self.allow_ftc,
            "require_substitution": self.require_substitution,
            "require_parts": self.require_parts,
            "require_pfd": self.require_pfd,
            "require_trig": self.require_trig,
            "require_trig_sub": self.require_trig_sub,
            "include_plus_c": self.include_plus_c,
            "coef_abs_max": self.coef_abs_max,
            "degree_max": self.degree_max,
            "term_count_max": self.term_count_max,
            "nest_budget": self.nest_budget,
            "parts_depth": self.parts_depth,
            "max_pipeline_len": self.max_pipeline_len,
            "d_spend": self.d_spend,
            "construction": self.construction,
            "u_sub_form_preset": self.u_sub_form_preset,
            "u_sub_construction": self.u_sub_construction,
            "parts_form_preset": self.parts_form_preset,
            "pfd_form_preset": self.pfd_form_preset,
            "trig_sub_form_preset": self.trig_sub_form_preset,
        }


@dataclass
class TrickStage:
    """One stage in an ordered trick pipeline.

    ``input_kind``: ``\"1\"`` (seed) or ``\"prior\"`` (wrap previous expression).
    ``transform``: what this stage does to force the trick.
    """

    trick: str
    input_kind: str  # "1" | "prior"
    transform: str
    notes: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "trick": self.trick,
            "input_kind": self.input_kind,
            "transform": self.transform,
            "notes": self.notes,
        }


@dataclass
class TrickPipeline:
    """Ordered list of tricks the student must apply."""

    stages: tuple[TrickStage, ...] = ()

    @property
    def tricks_required(self) -> list[str]:
        return [s.trick for s in self.stages]

    def as_dict(self) -> dict[str, Any]:
        return {
            "stages": [s.as_dict() for s in self.stages],
            "tricks_required": self.tricks_required,
            "length": len(self.stages),
        }


@dataclass(frozen=True)
class IntegralSample:
    prompt_latex: str
    answer_latex: str
    technique: str
    tricks_required: tuple[str, ...]
    upgrades: tuple[str, ...]
    effective_d: float
    band: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def as_metadata(self) -> dict[str, Any]:
        gen_key = str(self.metadata.get("generator") or "")
        # Prefer explicit OpenStax / Spec form ids over the coarse technique label.
        family = str(
            self.metadata.get("form_id")
            or self.metadata.get("openstax_form")
            or self.metadata.get("shape_id")
            or self.metadata.get("family")
            or self.technique
        )
        structure_id = f"{gen_key}:{family}" if gen_key else family
        return {
            "family": family,
            "structure_id": structure_id,
            "technique": self.technique,
            "tricks_required": list(self.tricks_required),
            "methods_used": list(self.tricks_required) or [self.technique],
            "function_classes": list(
                self.metadata.get("function_classes") or ["algebraic"]
            ),
            "upgrades": list(self.upgrades),
            "effective_d": self.effective_d,
            "band": self.band,
            **self.metadata,
            # Re-assert after **metadata so form taxonomy wins.
            "family": family,
            "structure_id": structure_id,
            "form_id": self.metadata.get("form_id") or family,
            "openstax_form": self.metadata.get("openstax_form")
            or self.metadata.get("form_id")
            or family,
        }


# ---------------------------------------------------------------------------
# Resolve / structure
# ---------------------------------------------------------------------------


def resolve_generator_key(topic_or_generator: str | None) -> str | None:
    if not topic_or_generator:
        return None
    key = str(topic_or_generator).strip()
    if key in _TOPIC_DEFAULTS:
        return key
    if key in _TYPE_ID_TO_GENERATOR:
        return _TYPE_ID_TO_GENERATOR[key]
    if key.startswith("c1_") and key[3:] in _TYPE_ID_TO_GENERATOR:
        return _TYPE_ID_TO_GENERATOR[key[3:]]
    return None


def topic_allow_defaults(generator_key: str | None) -> dict[str, bool]:
    base = {k: False for k in TRICK_ALLOW_KEYS}
    base["include_plus_c"] = True
    base["definite"] = False
    if generator_key and generator_key in _TOPIC_DEFAULTS:
        base.update(_TOPIC_DEFAULTS[generator_key])
    return base


def resolve_integral_allows(
    settings: dict[str, Any],
    *,
    generator_key: str | None = None,
    topic: str | None = None,
) -> dict[str, bool]:
    key = generator_key or resolve_generator_key(topic)
    defaults = topic_allow_defaults(key)
    out = dict(defaults)
    for k in list(defaults.keys()):
        if k in settings and settings[k] is not None:
            out[k] = bool(settings[k])
    return out


def _rng(settings: dict[str, Any]) -> random.Random:
    seed = settings.get("seed")
    if seed is None:
        return random.Random()
    return random.Random(int(seed) ^ 0x494E5431)


def _band(d: float) -> str:
    if d < 5:
        return "easy"
    if d < 12:
        return "medium"
    return "hard"


def _plus_c(body: str, *, include: bool) -> str:
    if not include:
        return body
    if body.endswith("+C") or body.endswith("+ C"):
        return body
    return f"{body}+C"


def _neg_power_antideriv(
    inner: str,
    n: int,
    du_scale: int,
    *,
    include: bool,
    num_coef: int = 1,
) -> str:
    """Antiderivative of ``num_coef`` · u^{-n} · (du / du_scale) for integer n≥2.

    ∫ num u^{-n} du/k = −num / (k (n−1) u^{n−1}). ``du_scale`` is k (may be negative).
    """
    k = int(du_scale)
    num = int(num_coef)
    if n < 2 or k == 0:
        raise ValueError((n, k, num))
    coef = Fraction(-num, k * (n - 1))
    wrap = rf"\left({inner}\right)"
    power = n - 1
    den_inner = wrap if power == 1 else rf"{wrap}^{{{power}}}"
    sign = "-" if coef < 0 else ""
    abs_c = abs(coef)
    if abs_c == 1:
        body = rf"{sign}\frac{{1}}{{{den_inner}}}"
    elif abs_c.denominator == 1:
        body = rf"{sign}\frac{{{abs_c.numerator}}}{{{den_inner}}}"
    elif abs_c.numerator == 1:
        body = rf"{sign}\frac{{1}}{{{abs_c.denominator}{den_inner}}}"
    else:
        body = rf"{sign}\frac{{{abs_c.numerator}}}{{{abs_c.denominator}{den_inner}}}"
    return _plus_c(body, include=include)


def _spec_allow_map(spec: IntegralSpec) -> dict[str, bool]:
    """Checkbox dict for ``filter_forms_by_allows``."""
    return {
        "allow_trig": spec.allow_trig,
        "allow_exp": spec.allow_exp,
        "allow_log": spec.allow_log,
        "allow_invtrig": spec.allow_invtrig,
        "allow_substitution": spec.allow_substitution,
        "allow_parts": spec.allow_parts,
        "allow_pfd": spec.allow_pfd,
        "allow_trig_sub": spec.allow_trig_sub,
        "allow_ftc": spec.allow_ftc,
        "require_substitution": spec.require_substitution,
        "require_parts": spec.require_parts,
        "require_pfd": spec.require_pfd,
        "require_trig": spec.require_trig,
        "require_trig_sub": spec.require_trig_sub,
    }


def _gated_form_pool(
    catalog: dict[str, Any],
    spec: IntegralSpec,
    *,
    extra_ids: set[str] | None = None,
) -> list[dict[str, Any]]:
    """Implemented catalog forms that pass teacher allow_* / tricks gates."""
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        filter_forms_by_allows,
        implemented_forms,
    )

    pool = implemented_forms(catalog)
    if extra_ids:
        subset = [f for f in pool if str(f.get("form_id")) in extra_ids]
        if subset:
            pool = subset
    return filter_forms_by_allows(
        pool,
        _spec_allow_map(spec),
        conceptual_d=float(spec.d_spend),
        soft_c_schedule=False,
        fallback_on_empty=False,
    )


def _coef(rng: random.Random, hi: int, *, exclude_zero: bool = True) -> int:
    excl = {0} if exclude_zero else set()
    return random_int_range(-hi, hi, exclude=excl) if hi > 0 else (1 if exclude_zero else 0)


def _integral_upgrades() -> list[DifficultyFactor]:
    return [
        DifficultyFactor("extra_term", 2.0, ("ops",)),
        DifficultyFactor("higher_degree", 2.5, ("ops",)),
        DifficultyFactor("use_trig", 3.0, ("class",)),
        DifficultyFactor("use_exp_log", 3.0, ("class",)),
        DifficultyFactor("use_invtrig", 3.5, ("class",)),
        DifficultyFactor("use_u_sub", 3.5, ("method",)),
        DifficultyFactor("use_parts", 4.0, ("method",)),
        DifficultyFactor("use_pfd", 4.5, ("method",)),
        DifficultyFactor("use_trig_sub", 5.0, ("method",)),
        DifficultyFactor("pipeline_len_2", 5.0, ("pipeline",)),
        DifficultyFactor("pipeline_len_3", 7.0, ("pipeline",)),
        DifficultyFactor("parts_twice", 4.0, ("method",)),
        DifficultyFactor("nested_u", 3.5, ("nesting",)),
        DifficultyFactor("definite_bounds", 2.0, ("form",)),
    ]


# ---------------------------------------------------------------------------
# Pipeline planner
# ---------------------------------------------------------------------------

# Supported multi-trick combos (ordered).
_SUPPORTED_PIPELINES: tuple[tuple[str, ...], ...] = (
    ("u_sub", "pfd"),
    ("u_sub", "trig_sub"),
)


def plan_trick_pipeline(
    spec: IntegralSpec,
    *,
    purchased: set[str],
    rng: random.Random,
) -> TrickPipeline:
    """Choose an ordered trick list from Spec requires + D purchases.

    Prefer explicit ``tricks_required`` on Spec; else require_* flags; else
    single primary trick from leaf pack; else buy pipeline length from D.

    Trig-sub leaves must not collapse to plain ``u_sub`` just because
    ``allow_substitution`` is on (that flag only means a preliminary
    linear wrap is *allowed*, not required).
    """
    if spec.tricks_required:
        stages = tuple(
            TrickStage(
                trick=t,
                input_kind="1" if i == 0 else "prior",
                transform=_default_transform(t),
            )
            for i, t in enumerate(spec.tricks_required)
        )
        return TrickPipeline(stages=stages)

    # Dedicated trig-sub leaf: primary is trig_sub; optional u wrap at high D.
    if spec.require_trig_sub or spec.pack == "integral_trig_sub":
        want_u_wrap = (
            spec.allow_substitution
            and ("nested_u" in purchased or "use_u_sub" in purchased)
            and spec.d_spend >= 12
            and rng.random() < 0.35
        )
        if want_u_wrap:
            return TrickPipeline(
                stages=(
                    TrickStage(
                        trick="u_sub",
                        input_kind="1",
                        transform="compose_linear_inner",
                        notes="u=cx+d before trig sub",
                    ),
                    TrickStage(
                        trick="trig_sub",
                        input_kind="prior",
                        transform="sample_trig_sub_form",
                        notes="√(a²±u²) / √(u²−a²) after u-sub",
                    ),
                )
            )
        return TrickPipeline(
            stages=(
                TrickStage(
                    trick="trig_sub",
                    input_kind="1",
                    transform="sample_trig_sub_form",
                    notes="x=a·sinθ / a·tanθ / a·secθ",
                ),
            )
        )

    required: list[str] = []
    if spec.require_substitution:
        required.append("u_sub")
    if spec.require_trig_sub:
        required.append("trig_sub")
    if spec.require_pfd:
        required.append("pfd")
    if spec.require_parts:
        required.append("parts")
    if spec.require_trig and "trig" not in required:
        # Dedicated trig-integrals leaf: never collapse to u_sub just because
        # allow_substitution is on (that flag only gates internal identities).
        required.append("trig")

    # Multi-trick leaf or D bought pipeline_len_2 with both u_sub+pfd allowed
    want_multi = (
        spec.pack == "integral_multi_trick"
        or (
            "pipeline_len_2" in purchased
            and spec.allow_substitution
            and spec.allow_pfd
            and spec.max_pipeline_len >= 2
        )
    )
    if want_multi and spec.allow_substitution and spec.allow_pfd:
        return TrickPipeline(
            stages=(
                TrickStage(
                    trick="u_sub",
                    input_kind="1",
                    transform="compose_linear_inner",
                    notes="wrap PFD-core so u-sub first",
                ),
                TrickStage(
                    trick="pfd",
                    input_kind="prior",
                    transform="seed_pfd_rational",
                    notes="PFD of substituted rational",
                ),
            )
        )

    if len(required) >= 2:
        # Order: u_sub before trig_sub/pfd when both required
        order = [
            t
            for t in (
                "u_sub",
                "trig_sub",
                "parts",
                "pfd",
                "trig",
                "ln_exp",
                "invtrig",
                "power",
                "ftc",
            )
            if t in required
        ]
        if not order:
            order = required
        return TrickPipeline(
            stages=tuple(
                TrickStage(
                    trick=t,
                    input_kind="1" if i == 0 else "prior",
                    transform=_default_transform(t),
                )
                for i, t in enumerate(order)
            )
        )

    if required:
        t = required[0]
        return TrickPipeline(
            stages=(TrickStage(trick=t, input_kind="1", transform=_default_transform(t)),)
        )

    if spec.pack == "integral_general":
        return _plan_general_pipeline(spec, purchased=purchased, rng=rng)

    # Single-trick from pack / allowed
    primary = _primary_trick_for_pack(spec.pack, spec)
    return TrickPipeline(
        stages=(
            TrickStage(
                trick=primary,
                input_kind="1",
                transform=_default_transform(primary),
            ),
        )
    )


def _plan_general_pipeline(
    spec: IntegralSpec,
    *,
    purchased: set[str],
    rng: random.Random,
) -> TrickPipeline:
    """D-gated mix of allowed techniques for ``integral_general``.

    D=0 stays table/power. Bank-hard families (parts/PFD/trig-sub) unlock mid/high D.
    Toggles drop the corresponding technique entirely.
    """
    d = float(spec.d_spend)
    weighted: list[tuple[str, float]] = [("power", 3.2 if d < 6 else 0.7)]
    if spec.allow_trig:
        weighted.append(("trig", 1.3 if d >= 2 else 0.35))
    if spec.allow_exp or spec.allow_log:
        weighted.append(("ln_exp", 1.1 if d >= 2 else 0.3))
    if spec.allow_invtrig and d >= 6:
        weighted.append(("invtrig", 1.0))
    if spec.allow_substitution and d >= 4:
        weighted.append(("u_sub", 1.6 if d >= 8 else 0.85))
    if spec.allow_parts and d >= 8:
        weighted.append(("parts", 1.3 if d >= 12 else 0.55))
    if spec.allow_pfd and d >= 8:
        weighted.append(("pfd", 1.3 if d >= 12 else 0.55))
    if spec.allow_trig_sub and d >= 10:
        weighted.append(("trig_sub", 1.0))
    if "use_parts" in purchased and spec.allow_parts:
        weighted = [(t, w * (1.8 if t == "parts" else 1.0)) for t, w in weighted]
    if "use_pfd" in purchased and spec.allow_pfd:
        weighted = [(t, w * (1.8 if t == "pfd" else 1.0)) for t, w in weighted]
    tricks, weights = zip(*weighted)
    chosen = rng.choices(list(tricks), weights=list(weights), k=1)[0]
    return TrickPipeline(
        stages=(
            TrickStage(
                trick=chosen,
                input_kind="1",
                transform=_default_transform(chosen),
            ),
        )
    )


def _default_transform(trick: str) -> str:
    return {
        "power": "sample_power_poly",
        "trig": "sample_trig_form",
        "ln_exp": "sample_ln_exp_form",
        "invtrig": "sample_invtrig_form",
        "u_sub": "derivative_backed_chain",
        "parts": "sample_parts_liate",
        "pfd": "seed_pfd_forward",
        "ftc": "sample_definite_poly",
        "trig_sub": "sample_trig_sub_form",
    }.get(trick, "sample_forward")


def _primary_trick_for_pack(pack: str, spec: IntegralSpec) -> str:
    mapping = {
        "integral_power": "power",
        "integral_trig": "trig",
        "integral_ln_exp": "ln_exp",
        "integral_invtrig": "invtrig",
        "integral_u_sub": "u_sub",
        "integral_u_sub_definite": "u_sub",
        "integral_trig_sub": "trig_sub",
        "integral_log_exp_sub": "u_sub",
        "integral_invtrig_sub": "u_sub",
        "integral_parts": "parts",
        "integral_pfd": "pfd",
        "integral_multi_trick": "u_sub",
        "integral_general": "power",
        "integral_ftc1": "ftc",
        "integral_ftc2": "ftc",
    }
    if pack in mapping:
        return mapping[pack]
    if spec.allow_ftc and spec.definite:
        return "ftc"
    if spec.allow_pfd:
        return "pfd"
    if spec.allow_parts:
        return "parts"
    if spec.allow_substitution:
        return "u_sub"
    if spec.allow_trig:
        return "trig"
    return "power"


def build_integral_spec(
    settings: dict[str, Any],
    *,
    generator_key: str | None = None,
    allows: dict[str, bool] | None = None,
    purchased: set[str] | None = None,
    d: float | None = None,
) -> IntegralSpec:
    key = generator_key or "integral_power_rule"
    allows = allows or resolve_integral_allows(settings, generator_key=key)
    purchased = purchased or set()
    d = float(d if d is not None else settings_difficulty(settings, default=6.0))
    var = str(settings.get("variable", "x"))
    coef_hi = int(settings.get("coef_max", 6) or 6)
    coef_hi = max(coef_hi, 3 + int(d // 4))
    degree_max = int(settings.get("power_max", 4) or 4)
    if "higher_degree" in purchased:
        degree_max = max(degree_max, min(6, degree_max + 1))

    tricks: set[str] = {"power"}
    pack = "integral_power"
    construction = "forward"
    max_pipe = 1

    if key == "integral_trigonometric":
        tricks = {"trig"}
        pack = "integral_trig"
    elif key == "integral_log_exp":
        tricks = {"ln_exp"}
        pack = "integral_ln_exp"
    elif key == "integral_inverse_trig":
        tricks = {"invtrig"}
        pack = "integral_invtrig"
    elif key == "integral_substitution":
        tricks = {"u_sub"}
        pack = "integral_u_sub"
        construction = "derivative_backed"
    elif key == "integral_definite_substitution":
        tricks = {"u_sub"}
        pack = "integral_u_sub_definite"
        construction = "forward"
    elif key == "integral_trig_substitution":
        tricks = {"trig_sub"}
        pack = "integral_trig_sub"
        construction = "forward"
        if allows.get("allow_substitution"):
            tricks.add("u_sub")
    elif key == "integral_log_exp_substitution":
        tricks = {"u_sub", "ln_exp"}
        pack = "integral_log_exp_sub"
        construction = "derivative_backed"
    elif key == "integral_invtrig_substitution":
        tricks = {"u_sub", "invtrig"}
        pack = "integral_invtrig_sub"
        construction = "derivative_backed"
    elif key == "integration_by_parts":
        tricks = {"parts"}
        pack = "integral_parts"
    elif key == "integral_partial_fractions":
        tricks = {"pfd"}
        pack = "integral_pfd"
        construction = "forward"
    elif key == "integral_multi_trick":
        tricks = {"u_sub", "pfd"}
        pack = "integral_multi_trick"
        construction = "pipeline"
        max_pipe = 2
    elif key == "integral_general":
        tricks = {"power"}
        pack = "integral_general"
        construction = "forward"
    elif key == "first_fundamental_theorem":
        tricks = {"ftc", "power"}
        pack = "integral_ftc1"
    elif key == "second_fundamental_theorem":
        tricks = {"ftc", "u_sub"}
        pack = "integral_ftc2"
    else:
        pack = "integral_power"

    if allows.get("allow_trig"):
        tricks.add("trig")
    if allows.get("allow_exp") or allows.get("allow_log"):
        tricks.add("ln_exp")
    if allows.get("allow_invtrig"):
        tricks.add("invtrig")
    if allows.get("allow_substitution"):
        tricks.add("u_sub")
    if allows.get("allow_parts"):
        tricks.add("parts")
    if allows.get("allow_pfd"):
        tricks.add("pfd")
    if allows.get("allow_trig_sub"):
        tricks.add("trig_sub")
    if allows.get("allow_ftc"):
        tricks.add("ftc")

    if "pipeline_len_2" in purchased:
        max_pipe = max(max_pipe, 2)
    if "pipeline_len_3" in purchased:
        max_pipe = max(max_pipe, 3)
    max_pipe = min(_MAX_PIPELINE_LEN, max(max_pipe, int(settings.get("max_pipeline_len", 1) or 1)))

    nest = 1
    if "nested_u" in purchased or "use_u_sub" in purchased:
        nest = 2
    parts_depth = 2 if "parts_twice" in purchased else 1

    req_tricks: tuple[str, ...] = ()
    if allows.get("require_substitution") and allows.get("require_pfd"):
        req_tricks = ("u_sub", "pfd")
        construction = "pipeline"
        max_pipe = max(max_pipe, 2)
    elif key == "integral_multi_trick":
        req_tricks = ("u_sub", "pfd")
    elif key == "integral_trig_substitution" or allows.get("require_trig_sub"):
        # Pipeline planner may upgrade to u_sub→trig_sub; leave empty so it can.
        req_tricks = ()

    return IntegralSpec(
        variable=var,
        definite=bool(allows.get("definite")),
        bound_abs_max=int(settings.get("bound_max", 5) or 5),
        tricks_allowed=frozenset(tricks),
        tricks_required=req_tricks,
        allow_trig=bool(allows.get("allow_trig")),
        allow_exp=bool(allows.get("allow_exp")),
        allow_log=bool(allows.get("allow_log")),
        allow_invtrig=bool(allows.get("allow_invtrig")),
        allow_substitution=bool(allows.get("allow_substitution")),
        allow_parts=bool(allows.get("allow_parts")),
        allow_pfd=bool(allows.get("allow_pfd")),
        allow_trig_sub=bool(allows.get("allow_trig_sub")),
        allow_ftc=bool(allows.get("allow_ftc")),
        require_substitution=bool(allows.get("require_substitution")),
        require_parts=bool(allows.get("require_parts")),
        require_pfd=bool(allows.get("require_pfd")),
        require_trig=bool(allows.get("require_trig")),
        require_trig_sub=bool(allows.get("require_trig_sub")),
        include_plus_c=bool(allows.get("include_plus_c", True)),
        coef_abs_max=coef_hi,
        degree_max=degree_max,
        term_count_max=max(1, int(settings.get("term_count", 3) or 3)),
        nest_budget=nest,
        parts_depth=parts_depth,
        max_pipeline_len=max_pipe,
        d_spend=d,
        pack=pack,
        construction=construction,
        u_sub_form_preset=str(settings.get("u_sub_form_preset") or "auto").strip().lower(),
        u_sub_construction=str(settings.get("u_sub_construction") or "auto").strip().lower(),
        parts_form_preset=str(settings.get("parts_form_preset") or "auto").strip().lower(),
        pfd_form_preset=str(settings.get("pfd_form_preset") or "auto").strip().lower(),
        trig_sub_form_preset=str(settings.get("trig_sub_form_preset") or "auto").strip().lower(),
    )


# ---------------------------------------------------------------------------
# Forward samplers (single-trick)
# ---------------------------------------------------------------------------


def _effort(
    *,
    technique: str,
    tricks: Sequence[str],
    degree: int,
    coef_hi: int,
    n_terms: int,
    answer: str,
    pack: str,
    nest: int = 0,
) -> dict[str, Any]:
    return {
        "technique": technique,
        "tricks_required": list(tricks),
        "pipeline_len": len(tricks),
        "degree_max": degree,
        "coef_abs_max": coef_hi,
        "n_terms": n_terms,
        "answer_len": len(answer or ""),
        "nest_depth": nest,
        "pack": pack,
        "methods": list(tricks) or [technique],
    }


def _join_poly_int_terms(terms: list[tuple[Fraction | int, int | Fraction]], var: str) -> str:
    """Build antiderivative latex from (coef, new_power) pieces."""
    pieces: list[str] = []
    for c, p in terms:
        c = Fraction(c)
        if isinstance(p, Fraction):
            # fractional power after integrating e.g. x^{1/2} → (2/3)x^{3/2}
            cl = frac_latex(c)
            num, den = p.numerator, p.denominator
            pow_l = rf"{var}^{{\frac{{{num}}}{{{den}}}}}" if den != 1 else (
                var if num == 1 else rf"{var}^{{{num}}}"
            )
            if cl == "1":
                pieces.append(pow_l)
            elif cl == "-1":
                pieces.append(f"-{pow_l}")
            else:
                pieces.append(f"{cl}{pow_l}")
            continue
        p = int(p)
        cl = frac_latex(c)
        if p == 0:
            pieces.append(cl)
            continue
        if p == 1:
            mon = var
        else:
            mon = f"{var}^{{{p}}}"
        if cl == "1":
            pieces.append(mon)
        elif cl == "-1":
            pieces.append(f"-{mon}")
        else:
            pieces.append(f"{cl}{mon}")
    if not pieces:
        return "0"
    out = pieces[0]
    for p in pieces[1:]:
        if p.startswith("-"):
            out += p
        else:
            out += "+" + p
    return out


POWER_GENERATOR = "integral_power_rule"

_POWER_BANDS: dict[str, tuple[str, ...]] = {
    "easy": ("poly_sum", "sqrt_x"),
    "medium": (
        "poly_sum",
        "sqrt_x",
        "one_over_sqrt_x",
        "x_sqrt_x",
        "neg_power",
        "rewrite_over_x",
    ),
    "hard": ("one_over_sqrt_x", "x_sqrt_x", "neg_power", "rewrite_over_x"),
    "expert": ("neg_power", "rewrite_over_x"),
}


def power_forms_for_difficulty(d: float) -> tuple[str, ...]:
    """Leftover lockout of D=0 poly_sum / √x; D=22 is rewrite / neg-power."""
    if d < 8.0:
        return _POWER_BANDS["easy"]
    if d < 16.0:
        return _POWER_BANDS["medium"]
    if d < 20.0:
        return _POWER_BANDS["hard"]
    return _POWER_BANDS["expert"]


def _sample_power(
    rng: random.Random, spec: IntegralSpec
) -> tuple[str, str, dict[str, Any]]:
    """OpenStax power/rewrite forms driven by ``basic_power_integrals`` catalog.

    High D locks out D=0 poly_sum / √x leftovers. Same six old builders.
    """
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        catalog_form_meta,
        implemented_forms,
        load_form_catalog,
        select_form_id,
    )

    var = spec.variable
    d = float(spec.d_spend)
    catalog = load_form_catalog("basic_power_integrals")
    allowed = set(power_forms_for_difficulty(d))
    pool = _gated_form_pool(catalog, spec) or implemented_forms(catalog)
    pool = [f for f in pool if str(f.get("form_id")) in allowed]
    if not pool:
        pool = [f for f in implemented_forms(catalog) if str(f.get("form_id")) in allowed]
    form = select_form_id(pool, d=d, rng=rng)
    form_id = str(form["form_id"])
    include = spec.include_plus_c
    meta_base = {
        **catalog_form_meta(form, catalog),
        "generator": POWER_GENERATOR,
    }

    if form_id == "sqrt_x":
        prompt = rf"\int \sqrt{{{var}}}\,d{var}"
        answer = _plus_c(rf"\frac{{2}}{{3}}{var}^{{\frac{{3}}{{2}}}}", include=include)
        return prompt, answer, {**meta_base, "function_classes": ["algebraic"], "family": form_id, "n_terms": 1}
    if form_id == "one_over_sqrt_x":
        prompt = rf"\int \frac{{1}}{{\sqrt{{{var}}}}}\,d{var}"
        answer = _plus_c(rf"2\sqrt{{{var}}}", include=include)
        return prompt, answer, {**meta_base, "function_classes": ["algebraic"], "family": form_id, "n_terms": 1}
    if form_id == "x_sqrt_x":
        prompt = rf"\int {var}\sqrt{{{var}}}\,d{var}"
        answer = _plus_c(rf"\frac{{2}}{{5}}{var}^{{\frac{{5}}{{2}}}}", include=include)
        return prompt, answer, {**meta_base, "function_classes": ["algebraic"], "family": form_id, "n_terms": 1}
    if form_id == "neg_power":
        n = rng.randint(2, max(2, min(4, spec.degree_max)))
        k = rng.randint(1, max(1, min(6, spec.coef_abs_max)))
        prompt = rf"\int \frac{{{k}}}{{{var}^{{{n}}}}}\,d{var}"
        new_c = Fraction(k, 1 - n)
        answer = _plus_c(_join_poly_int_terms([(new_c, 1 - n)], var), include=include)
        return prompt, answer, {**meta_base, "function_classes": ["algebraic"], "family": form_id, "n_terms": 1}
    if form_id == "rewrite_over_x":
        c = rng.randint(1, max(1, min(5, spec.coef_abs_max)))
        prompt = rf"\int \frac{{{var}^{{2}}+{c}\sqrt[3]{{{var}}}}}{{{var}}}\,d{var}"
        answer = _plus_c(
            rf"\frac{{1}}{{2}}{var}^{{2}}+{3 * c}{var}^{{\frac{{1}}{{3}}}}",
            include=include,
        )
        return prompt, answer, {**meta_base, "function_classes": ["algebraic"], "family": form_id, "n_terms": 2}

    # poly_sum (default)
    n_terms = rng.randint(1, max(1, spec.term_count_max))
    used: set[int] = set()
    terms: list[tuple[int, int]] = []
    for _ in range(n_terms):
        p = rng.randint(0, max(0, spec.degree_max))
        while p in used and len(used) <= spec.degree_max:
            p = rng.randint(0, max(0, spec.degree_max))
        used.add(p)
        terms.append((_coef(rng, spec.coef_abs_max), p))
    max_p = max(p for _, p in terms)
    coeffs = [0] * (max_p + 1)
    for c, p in terms:
        coeffs[max_p - p] += c
    body = format_polynomial_latex(coeffs, variable=var)
    int_terms: list[tuple[Fraction, int]] = []
    for c, p in terms:
        int_terms.append((Fraction(c, p + 1), p + 1))
    answer = _plus_c(_join_poly_int_terms(int_terms, var), include=include)
    prompt = rf"\int {body} \, d{var}"
    return prompt, answer, {
        **meta_base,
        "form_id": "poly_sum",
        "openstax_form": "poly_sum",
        "function_classes": ["algebraic"],
        "family": "poly_sum",
        "n_terms": n_terms,
    }


def _trig_pow(fn: str, power: int, arg: str) -> str:
    if power == 1:
        return rf"\{fn}({arg})"
    return rf"\{fn}^{{{power}}}({arg})"


TRIG_GENERATOR = "integral_trigonometric"

_TRIG_TABLE = (
    "basic_sin_kx",
    "basic_cos_kx",
    "basic_sec2",
    "basic_sec_tan",
    "basic_tan",
)
_TRIG_EASY_USUB = (
    "cos_j_sin",
    "sin_j_cos",
)
_TRIG_MID = (
    "sin_even_power",
    "cos_even_power",
    "tan2",
    "sin_odd_cos_any",
    "cos_odd_sin_any",
    "sec_j_tan",
    "tan_k_sec2",
)
_TRIG_HIGH = (
    "product_sin_a_cos_b",
    "product_cos_a_cos_b",
    "product_sin_a_sin_b",
    "sin_cos_both_even",
    "sin_cos_both_odd",
    "csc_j_cot",
    "sin_over_one_plus_cos2",
    "tan_odd_alone",
    "tan_sec_sec_even",
    "tan_odd_sec_any",
    "one_over_one_plus_cos",
    "one_over_one_plus_sin",
    "tan_even_reduction",
    "sec3_reduction",
    "sec_odd_reduction_n5",
)

_TRIG_BANDS: dict[str, tuple[str, ...]] = {
    "easy": _TRIG_TABLE + _TRIG_EASY_USUB + (
        "sin_even_power",
        "cos_even_power",
        "tan2",
    ),
    "medium": _TRIG_EASY_USUB + _TRIG_MID + _TRIG_HIGH,
    "hard": _TRIG_MID + _TRIG_HIGH,
    "expert": _TRIG_HIGH,
}


def trig_forms_for_difficulty(d: float) -> tuple[str, ...]:
    """Leftover lockout of D=0 table / D=8 ``cos_j_sin``; D=22 is high catalog only."""
    if d < 8.0:
        return _TRIG_BANDS["easy"]
    if d < 16.0:
        return _TRIG_BANDS["medium"]
    if d < 20.0:
        return _TRIG_BANDS["hard"]
    return _TRIG_BANDS["expert"]


def _sample_trig(
    rng: random.Random, spec: IntegralSpec
) -> tuple[str, str, dict[str, Any]]:
    """Forward trig integrals driven by OpenStax §3.2 form catalog.

    High D locks out D=0 table leftovers and D=8 ``cos_j_sin`` / ``sin_j_cos``.
    Same implemented builders; catalog ``d_min`` still unlocks within each band.
    """
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        implemented_forms,
        load_form_catalog,
        select_form_id,
    )

    var = spec.variable
    d = float(spec.d_spend)
    catalog = load_form_catalog("trig_integrals")
    allowed = set(trig_forms_for_difficulty(d))
    pool = _gated_form_pool(catalog, spec)
    if not pool:
        if spec.allow_trig:
            pool = implemented_forms(catalog)
        else:
            return _sample_power(rng, spec)
    pool = [f for f in pool if str(f.get("form_id")) in allowed]
    if not pool:
        pool = [
            f for f in implemented_forms(catalog) if str(f.get("form_id")) in allowed
        ]
    if not pool:
        return _sample_power(rng, spec)
    form = select_form_id(pool, d=d, rng=rng)
    form_id = str(form["form_id"])
    if form_id not in allowed:
        form_id = trig_forms_for_difficulty(d)[0]
    tricks = [str(t) for t in (form.get("tricks") or ["trig"])]
    k = rng.randint(1, max(1, min(6, spec.coef_abs_max)))
    include = spec.include_plus_c

    def _odd_ge(lo: int = 3, hi: int = 5) -> int:
        odds = [n for n in range(lo, hi + 1) if n % 2 == 1]
        return rng.choice(odds)

    def _even_ge(lo: int = 2, hi: int = 4) -> int:
        evens = [n for n in range(lo, hi + 1) if n % 2 == 0]
        return rng.choice(evens)

    # --- dispatch by form_id -------------------------------------------------
    if form_id == "basic_sin_kx":
        arg = format_monomial_latex(k, variable=var) or f"{k}{var}"
        prompt = rf"\int \sin({arg})\,d{var}"
        answer = _plus_c(
            rf"-\cos({arg})" if k == 1 else rf"-\frac{{1}}{{{k}}}\cos({arg})",
            include=include,
        )
    elif form_id == "basic_cos_kx":
        arg = format_monomial_latex(k, variable=var) or f"{k}{var}"
        prompt = rf"\int \cos({arg})\,d{var}"
        answer = _plus_c(
            rf"\sin({arg})" if k == 1 else rf"\frac{{1}}{{{k}}}\sin({arg})",
            include=include,
        )
    elif form_id == "basic_sec2":
        arg = format_monomial_latex(k, variable=var) or f"{k}{var}"
        prompt = rf"\int \sec^{{2}}({arg})\,d{var}"
        answer = _plus_c(
            rf"\tan({arg})" if k == 1 else rf"\frac{{1}}{{{k}}}\tan({arg})",
            include=include,
        )
    elif form_id == "basic_sec_tan":
        prompt = rf"\int \sec({var})\tan({var})\,d{var}"
        answer = _plus_c(rf"\sec({var})", include=include)
    elif form_id == "basic_tan":
        prompt = rf"\int \tan({var})\,d{var}"
        answer = _plus_c(rf"-\ln|\cos({var})|", include=include)

    elif form_id == "cos_j_sin":
        j = rng.choice([2, 3, 4, 5])
        prompt = rf"\int {_trig_pow('cos', j, var)}\sin({var})\,d{var}"
        answer = _plus_c(
            rf"-\frac{{1}}{{{j + 1}}}{_trig_pow('cos', j + 1, var)}",
            include=include,
        )
    elif form_id == "sin_j_cos":
        j = rng.choice([2, 3, 4, 5])
        prompt = rf"\int {_trig_pow('sin', j, var)}\cos({var})\,d{var}"
        answer = _plus_c(
            rf"\frac{{1}}{{{j + 1}}}{_trig_pow('sin', j + 1, var)}",
            include=include,
        )

    elif form_id == "sin_odd_cos_any":
        # ∫ cos^j sin^{2n+1} — save one sin; classic j=0 → sin³, or j=2 → cos² sin³
        n_odd = _odd_ge(3, 5)
        j = rng.choice([0, 2]) if spec.d_spend < 14 else rng.choice([0, 2, 4])
        if j == 0 and n_odd == 3:
            prompt = rf"\int \sin^{{3}}({var})\,d{var}"
            answer = _plus_c(
                rf"-\cos({var})+\frac{{1}}{{3}}\cos^{{3}}({var})",
                include=include,
            )
        elif j == 0 and n_odd == 5:
            # ∫ sin⁵ = ∫ (1-cos²)² sin → −cos + 2cos³/3 − cos⁵/5
            prompt = rf"\int \sin^{{5}}({var})\,d{var}"
            answer = _plus_c(
                rf"-\cos({var})+\frac{{2}}{{3}}\cos^{{3}}({var})"
                rf"-\frac{{1}}{{5}}\cos^{{5}}({var})",
                include=include,
            )
        else:
            # cos² sin³: ∫ cos²(1−cos²)sin = −cos³/3 + cos⁵/5
            prompt = rf"\int \cos^{{2}}({var})\sin^{{3}}({var})\,d{var}"
            answer = _plus_c(
                rf"-\frac{{1}}{{3}}\cos^{{3}}({var})+\frac{{1}}{{5}}\cos^{{5}}({var})",
                include=include,
            )

    elif form_id == "cos_odd_sin_any":
        n_odd = _odd_ge(3, 5)
        k_sin = rng.choice([0, 2]) if spec.d_spend < 14 else rng.choice([0, 2])
        if k_sin == 0 and n_odd == 3:
            prompt = rf"\int \cos^{{3}}({var})\,d{var}"
            answer = _plus_c(
                rf"\sin({var})-\frac{{1}}{{3}}\sin^{{3}}({var})",
                include=include,
            )
        elif k_sin == 0 and n_odd == 5:
            prompt = rf"\int \cos^{{5}}({var})\,d{var}"
            answer = _plus_c(
                rf"\sin({var})-\frac{{2}}{{3}}\sin^{{3}}({var})"
                rf"+\frac{{1}}{{5}}\sin^{{5}}({var})",
                include=include,
            )
        else:
            # cos³ sin²: ∫ (1−sin²)sin² cos = sin³/3 − sin⁵/5
            prompt = rf"\int \cos^{{3}}({var})\sin^{{2}}({var})\,d{var}"
            answer = _plus_c(
                rf"\frac{{1}}{{3}}\sin^{{3}}({var})-\frac{{1}}{{5}}\sin^{{5}}({var})",
                include=include,
            )

    elif form_id == "sin_even_power":
        p = 2 if spec.d_spend < 12 else _even_ge(2, 4)
        if p == 2:
            prompt = rf"\int \sin^{{2}}({var})\,d{var}"
            answer = _plus_c(
                rf"\frac{{{var}}}{{2}}-\frac{{1}}{{4}}\sin(2{var})",
                include=include,
            )
        else:
            # sin⁴ = [(1−cos2x)/2]² = (1 − 2cos2x + cos²2x)/4
            # = 3/8 − (1/2)cos2x/2 wait standard: 3x/8 − sin(2x)/4 + sin(4x)/32
            prompt = rf"\int \sin^{{4}}({var})\,d{var}"
            answer = _plus_c(
                rf"\frac{{3{var}}}{{8}}-\frac{{1}}{{4}}\sin(2{var})"
                rf"+\frac{{1}}{{32}}\sin(4{var})",
                include=include,
            )

    elif form_id == "cos_even_power":
        if spec.d_spend >= 10 and rng.random() < 0.45:
            a = rng.choice([2, 3, 4])
            prompt = rf"\int \cos^{{2}}({a}{var})\,d{var}"
            answer = _plus_c(
                rf"\frac{{{var}}}{{2}}+\frac{{1}}{{{4 * a}}}\sin({2 * a}{var})",
                include=include,
            )
        else:
            p = 2 if spec.d_spend < 12 else _even_ge(2, 4)
            if p == 2:
                prompt = rf"\int \cos^{{2}}({var})\,d{var}"
                answer = _plus_c(
                    rf"\frac{{{var}}}{{2}}+\frac{{1}}{{4}}\sin(2{var})",
                    include=include,
                )
            else:
                prompt = rf"\int \cos^{{4}}({var})\,d{var}"
                answer = _plus_c(
                    rf"\frac{{3{var}}}{{8}}+\frac{{1}}{{4}}\sin(2{var})"
                    rf"+\frac{{1}}{{32}}\sin(4{var})",
                    include=include,
                )

    elif form_id == "sin_cos_both_even":
        # ∫ sin² cos² = ∫ (sin 2x / 2)² = (1/4)∫ (1−cos4x)/2 = x/8 − sin(4x)/32
        prompt = rf"\int \sin^{{2}}({var})\cos^{{2}}({var})\,d{var}"
        answer = _plus_c(
            rf"\frac{{{var}}}{{8}}-\frac{{1}}{{32}}\sin(4{var})",
            include=include,
        )

    elif form_id == "product_sin_a_cos_b":
        a, b = rng.sample([2, 3, 4, 5, 6], 2)
        # sin A cos B = [sin(A+B)+sin(A−B)]/2
        prompt = rf"\int \sin({a}{var})\cos({b}{var})\,d{var}"
        sp, sm = a + b, a - b
        # ∫ = −cos(a+b)/(2(a+b)) − cos(a−b)/(2(a−b))   (sm may be negative)
        if sm == 0:
            answer = _plus_c(
                rf"-\frac{{1}}{{{2 * sp}}}\cos({sp}{var})",
                include=include,
            )
        else:
            answer = _plus_c(
                rf"-\frac{{1}}{{{2 * sp}}}\cos({sp}{var})"
                rf"-\frac{{1}}{{{2 * sm}}}\cos({sm}{var})",
                include=include,
            )

    elif form_id == "product_cos_a_cos_b":
        a, b = rng.sample([2, 3, 4, 5, 6], 2)
        # cos A cos B = [cos(A+B)+cos(A−B)]/2
        prompt = rf"\int \cos({a}{var})\cos({b}{var})\,d{var}"
        sp, sm = a + b, a - b
        answer = _plus_c(
            rf"\frac{{1}}{{{2 * sp}}}\sin({sp}{var})"
            rf"+\frac{{1}}{{{2 * sm}}}\sin({sm}{var})",
            include=include,
        )

    elif form_id == "product_sin_a_sin_b":
        a, b = rng.sample([2, 3, 4, 5, 6], 2)
        # sin A sin B = [cos(A−B) − cos(A+B)]/2
        prompt = rf"\int \sin({a}{var})\sin({b}{var})\,d{var}"
        sp, sm = a + b, a - b
        answer = _plus_c(
            rf"\frac{{1}}{{{2 * sm}}}\sin({sm}{var})"
            rf"-\frac{{1}}{{{2 * sp}}}\sin({sp}{var})",
            include=include,
        )

    elif form_id == "sec_j_tan":
        j = rng.choice([2, 3, 4, 5])
        prompt = rf"\int {_trig_pow('sec', j, var)}\tan({var})\,d{var}"
        # ∫ sec^j tan = sec^j / j
        answer = _plus_c(
            rf"\frac{{1}}{{{j}}}{_trig_pow('sec', j, var)}",
            include=include,
        )

    elif form_id == "tan_k_sec2":
        kk = rng.choice([2, 3, 4, 5])
        prompt = rf"\int {_trig_pow('tan', kk, var)}\sec^{{2}}({var})\,d{var}"
        answer = _plus_c(
            rf"\frac{{1}}{{{kk + 1}}}{_trig_pow('tan', kk + 1, var)}",
            include=include,
        )

    elif form_id == "tan2":
        prompt = rf"\int \tan^{{2}}({var})\,d{var}"
        answer = _plus_c(rf"\tan({var})-{var}", include=include)

    elif form_id == "tan_sec_sec_even":
        # ∫ tan² sec⁴ = ∫ tan² sec² · sec² = ∫ (sec²−1)sec² · sec² wait
        # Standard Example 3.15 style: tan^m sec^4 = tan^m sec² · sec²
        # Use tan² sec⁴: u=tan → ∫ u²(u²+1) du = u³/3 + u⁵/5? 
        # sec⁴ = sec² · sec² = (1+tan²)sec², so ∫ tan²(1+tan²)sec² = ∫(u²+u⁴)du
        prompt = rf"\int \tan^{{2}}({var})\sec^{{4}}({var})\,d{var}"
        answer = _plus_c(
            rf"\frac{{1}}{{3}}\tan^{{3}}({var})+\frac{{1}}{{5}}\tan^{{5}}({var})",
            include=include,
        )

    elif form_id == "tan_odd_sec_any":
        # ∫ tan³ sec = ∫ (sec²−1) sec tan? Classic: tan³ sec = (sec²−1)tan? 
        # Example-like: tan³ sec → save sec·tan, u=sec: ∫(u²−1) du = u³/3 − u
        # Or tan sec³: ∫ sec² · sec tan = ∫ u² du with u=sec → sec³/3
        if rng.random() < 0.5:
            prompt = rf"\int \tan^{{3}}({var})\sec({var})\,d{var}"
            answer = _plus_c(
                rf"\frac{{1}}{{3}}\sec^{{3}}({var})-\sec({var})",
                include=include,
            )
        else:
            prompt = rf"\int \tan({var})\sec^{{3}}({var})\,d{var}"
            answer = _plus_c(rf"\frac{{1}}{{3}}\sec^{{3}}({var})", include=include)

    elif form_id == "tan_odd_alone":
        # ∫ tan³ = ∫ (sec²−1)tan = (1/2)tan²? No: ∫ tan·sec² − ∫ tan = tan²/2 + ln|cos|
        prompt = rf"\int \tan^{{3}}({var})\,d{var}"
        answer = _plus_c(
            rf"\frac{{1}}{{2}}\tan^{{2}}({var})+\ln|\cos({var})|",
            include=include,
        )

    elif form_id == "sec3_reduction":
        prompt = rf"\int \sec^{{3}}({var})\,d{var}"
        answer = _plus_c(
            rf"\frac{{1}}{{2}}\left(\sec({var})\tan({var})"
            rf"+\ln|\sec({var})+\tan({var})|\right)",
            include=include,
        )

    elif form_id == "sec_odd_reduction_n5":
        # ∫ sec⁵ = (sec³ tan)/4 + (3/4)∫ sec³
        # ∫ sec³ = (1/2)(sec tan + ln|sec+tan|)
        prompt = rf"\int \sec^{{5}}({var})\,d{var}"
        answer = _plus_c(
            rf"\frac{{1}}{{4}}\sec^{{3}}({var})\tan({var})"
            rf"+\frac{{3}}{{8}}\left(\sec({var})\tan({var})"
            rf"+\ln|\sec({var})+\tan({var})|\right)",
            include=include,
        )

    elif form_id == "tan_even_reduction":
        # ∫ tan⁴ = ∫ tan²(sec²−1) = ∫(sec²−1)tan²? = ∫ tan² sec² − ∫ tan²
        # = tan³/3 − (tan − x) = tan³/3 − tan + x
        prompt = rf"\int \tan^{{4}}({var})\,d{var}"
        answer = _plus_c(
            rf"\frac{{1}}{{3}}\tan^{{3}}({var})-\tan({var})+{var}",
            include=include,
        )

    elif form_id == "sin_cos_both_odd":
        # ∫ sin³ cos³ = ∫ sin³ (1−sin²) cos → u=sin: u³ − u⁵
        prompt = rf"\int \sin^{{3}}({var})\cos^{{3}}({var})\,d{var}"
        answer = _plus_c(
            rf"\frac{{1}}{{4}}\sin^{{4}}({var})-\frac{{1}}{{6}}\sin^{{6}}({var})",
            include=include,
        )

    elif form_id == "csc_j_cot":
        j = rng.choice([2, 3, 4])
        prompt = rf"\int {_trig_pow('csc', j, var)}\cot({var})\,d{var}"
        answer = _plus_c(
            rf"-\frac{{1}}{{{j}}}{_trig_pow('csc', j, var)}",
            include=include,
        )

    elif form_id == "sin_over_one_plus_cos2":
        if rng.random() < 0.5:
            prompt = rf"\int \frac{{\sin({var})}}{{1+\cos^{{2}}({var})}}\,d{var}"
            answer = _plus_c(rf"-\arctan(\cos({var}))", include=include)
        else:
            prompt = rf"\int \frac{{\cos({var})}}{{1+\sin^{{2}}({var})}}\,d{var}"
            answer = _plus_c(rf"\arctan(\sin({var}))", include=include)

    elif form_id == "one_over_one_plus_cos":
        prompt = rf"\int \frac{{1}}{{1+\cos({var})}}\,d{var}"
        answer = _plus_c(rf"\tan\left(\frac{{{var}}}{{2}}\right)", include=include)

    elif form_id == "one_over_one_plus_sin":
        prompt = rf"\int \frac{{1}}{{1+\sin({var})}}\,d{var}"
        answer = _plus_c(
            rf"\tan({var})-\sec({var})",
            include=include,
        )

    else:
        # Should not reach for implemented catalog; fall back to basic sin
        form_id = "basic_sin_kx"
        tricks = ["trig"]
        prompt = rf"\int \sin({var})\,d{var}"
        answer = _plus_c(rf"-\cos({var})", include=include)

    return prompt, answer, {
        "function_classes": ["trig"],
        "family": form_id,
        "form_id": form_id,
        "openstax_form": form_id,
        "openstax_case": form.get("openstax_case"),
        "strategy": form.get("strategy"),
        "tricks_required": tricks,
        "n_terms": 1,
        "construction": "forward_form_catalog",
        "catalog_id": catalog.get("catalog_id"),
        "generator": TRIG_GENERATOR,
    }


LOG_EXP_GENERATOR = "integral_log_exp"

_LOG_EXP_BANDS: dict[str, tuple[str, ...]] = {
    "easy": ("ln", "exp"),
    "medium": ("ln", "exp", "ln_linear", "exp_k", "base_a"),
    "hard": ("ln_linear", "exp_k", "base_a"),
    "expert": ("ln_linear", "base_a"),
}

_LOG_EXP_LOG_FORMS = frozenset({"ln", "ln_linear"})
_LOG_EXP_EXP_FORMS = frozenset({"exp", "exp_k", "base_a"})


def log_exp_forms_for_difficulty(d: float) -> tuple[str, ...]:
    """Leftover lockout of D=0 ∫1/x / ∫e^x; D=22 is ln_linear / base_a."""
    if d < 8.0:
        return _LOG_EXP_BANDS["easy"]
    if d < 16.0:
        return _LOG_EXP_BANDS["medium"]
    if d < 20.0:
        return _LOG_EXP_BANDS["hard"]
    return _LOG_EXP_BANDS["expert"]


def _log_exp_form_rows(forms: tuple[str, ...]) -> list[dict[str, Any]]:
    return [
        {
            "form_id": fid,
            "d_min": 0.0,
            "d_weight": 1.0,
            "generation_status": "implemented",
            "generator_keys": [LOG_EXP_GENERATOR],
        }
        for fid in forms
    ]


def _filter_log_exp_forms(
    forms: tuple[str, ...], spec: IntegralSpec
) -> tuple[str, ...]:
    """Drop log vs exp families the teacher allow_* checkboxes forbid."""
    out = [
        fid
        for fid in forms
        if (fid in _LOG_EXP_LOG_FORMS and spec.allow_log)
        or (fid in _LOG_EXP_EXP_FORMS and spec.allow_exp)
    ]
    if out:
        return tuple(out)
    fallback = [
        fid
        for fid in ("ln", "ln_linear", "exp", "exp_k", "base_a")
        if (fid in _LOG_EXP_LOG_FORMS and spec.allow_log)
        or (fid in _LOG_EXP_EXP_FORMS and spec.allow_exp)
    ]
    return tuple(fallback) or ("exp",)


def _sample_ln_exp(
    rng: random.Random, spec: IntegralSpec
) -> tuple[str, str, dict[str, Any]]:
    """OpenStax §5.6 table ln/exp forms. High D locks out D=0 ∫1/x / ∫e^x.

    Same five old builders. ``exp`` is always ∫e^x; ``exp_k`` always k≥2.
    """
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        select_form_id,
    )

    var = spec.variable
    d = float(spec.d_spend)
    forms = _filter_log_exp_forms(log_exp_forms_for_difficulty(d), spec)
    form = select_form_id(_log_exp_form_rows(forms), d=d, rng=rng)
    family = str(form.get("form_id") or forms[0])
    if family not in forms:
        family = forms[0]
    include = spec.include_plus_c

    if family == "ln":
        prompt = rf"\int \frac{{1}}{{{var}}}\,d{var}"
        answer = _plus_c(rf"\ln|{var}|", include=include)
        classes = ["log"]
    elif family == "ln_linear":
        a = rng.randint(1, max(1, min(4, spec.coef_abs_max)))
        b = _coef(rng, max(2, spec.coef_abs_max))
        inner = format_linear_latex(a, b, variable=var)
        prompt = rf"\int \frac{{{a}}}{{{inner}}}\,d{var}"
        answer = _plus_c(rf"\ln|{inner}|", include=include)
        classes = ["log"]
    elif family == "base_a":
        base = rng.choice([2, 3, 5])
        prompt = rf"\int {base}^{{{var}}}\,d{var}"
        answer = _plus_c(
            rf"\frac{{{base}^{{{var}}}}}{{\ln {base}}}",
            include=include,
        )
        classes = ["exp"]
    elif family == "exp_k":
        k = rng.randint(2, max(2, min(5, spec.coef_abs_max)))
        prompt = rf"\int e^{{{k}{var}}}\,d{var}"
        answer = _plus_c(
            rf"\frac{{1}}{{{k}}}e^{{{k}{var}}}",
            include=include,
        )
        classes = ["exp"]
    else:
        family = "exp"
        prompt = rf"\int e^{{{var}}}\,d{var}"
        answer = _plus_c(rf"e^{{{var}}}", include=include)
        classes = ["exp"]
    return prompt, answer, {
        "function_classes": classes,
        "family": family,
        "form_id": family,
        "openstax_form": family,
        "generator": LOG_EXP_GENERATOR,
        "n_terms": 1,
        "construction": "forward_form_catalog",
    }


INVTRIG_GENERATOR = "integral_inverse_trig"

_INVTRIG_BANDS: dict[str, tuple[str, ...]] = {
    "easy": ("arctan_basic",),
    "medium": (
        "arctan_basic",
        "arctan_a2",
        "arctan_scaled",
        "arcsin_basic",
        "arcsin_a2",
        "arcsin_scaled",
    ),
    "hard": (
        "arctan_a2",
        "arctan_scaled",
        "arcsin_basic",
        "arcsin_a2",
        "arcsin_scaled",
    ),
    "expert": ("arctan_scaled", "arcsin_scaled"),
}


def invtrig_forms_for_difficulty(d: float) -> tuple[str, ...]:
    """Leftover lockout of D=0 ∫1/(1+x²); D=22 is scaled arctan / arcsin."""
    if d < 8.0:
        return _INVTRIG_BANDS["easy"]
    if d < 16.0:
        return _INVTRIG_BANDS["medium"]
    if d < 20.0:
        return _INVTRIG_BANDS["hard"]
    return _INVTRIG_BANDS["expert"]


def _sample_invtrig(
    rng: random.Random, spec: IntegralSpec
) -> tuple[str, str, dict[str, Any]]:
    """OpenStax §5.7 invtrig table forms via ``invtrig_integrals`` catalog.

    High D locks out D=0 ∫1/(1+x²). Same six old builders.
    """
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        catalog_form_meta,
        implemented_forms,
        load_form_catalog,
        select_form_id,
    )

    var = spec.variable
    d = float(spec.d_spend)
    catalog = load_form_catalog("invtrig_integrals")
    allowed = set(invtrig_forms_for_difficulty(d))
    pool = _gated_form_pool(catalog, spec) or implemented_forms(catalog)
    pool = [f for f in pool if str(f.get("form_id")) in allowed]
    if not pool:
        pool = [
            f for f in implemented_forms(catalog) if str(f.get("form_id")) in allowed
        ]
    form = select_form_id(pool, d=d, rng=rng)
    form_id = str(form["form_id"])
    if form_id not in allowed:
        form_id = invtrig_forms_for_difficulty(d)[0]
    include = spec.include_plus_c
    meta = {
        **catalog_form_meta(form, catalog),
        "function_classes": ["invtrig"],
        "family": form_id,
        "form_id": form_id,
        "openstax_form": form_id,
        "generator": INVTRIG_GENERATOR,
        "n_terms": 1,
    }
    a = rng.randint(2, max(2, min(5, spec.coef_abs_max)))
    b = rng.randint(2, max(2, min(4, spec.coef_abs_max)))
    a2, b2 = a * a, b * b

    if form_id == "arctan_basic":
        prompt = rf"\int \frac{{1}}{{1+{var}^{{2}}}}\,d{var}"
        answer = _plus_c(rf"\arctan({var})", include=include)
    elif form_id == "arctan_a2":
        prompt = rf"\int \frac{{1}}{{{a2}+{var}^{{2}}}}\,d{var}"
        answer = _plus_c(
            rf"\frac{{1}}{{{a}}}\arctan\left(\frac{{{var}}}{{{a}}}\right)",
            include=include,
        )
    elif form_id == "arctan_scaled":
        prompt = rf"\int \frac{{1}}{{{a2}+{b2}{var}^{{2}}}}\,d{var}"
        den = a * b
        body = (
            rf"\arctan({var})"
            if den == 1
            else rf"\frac{{1}}{{{den}}}\arctan\left(\frac{{{b}{var}}}{{{a}}}\right)"
        )
        answer = _plus_c(body, include=include)
    elif form_id == "arcsin_basic":
        prompt = rf"\int \frac{{1}}{{\sqrt{{1-{var}^{{2}}}}}}\,d{var}"
        answer = _plus_c(rf"\arcsin({var})", include=include)
    elif form_id == "arcsin_a2":
        prompt = rf"\int \frac{{1}}{{\sqrt{{{a2}-{var}^{{2}}}}}}\,d{var}"
        answer = _plus_c(
            rf"\arcsin\left(\frac{{{var}}}{{{a}}}\right)",
            include=include,
        )
    else:  # arcsin_scaled
        form_id = "arcsin_scaled"
        prompt = rf"\int \frac{{1}}{{\sqrt{{{a2}-{b2}{var}^{{2}}}}}}\,d{var}"
        answer = _plus_c(
            rf"\frac{{1}}{{{b}}}\arcsin\left(\frac{{{b}{var}}}{{{a}}}\right)"
            if b != 1
            else rf"\arcsin\left(\frac{{{var}}}{{{a}}}\right)",
            include=include,
        )
    meta["form_id"] = form_id
    meta["openstax_form"] = form_id
    meta["family"] = form_id
    return prompt, answer, meta


# Calc BC drill bank §2 (not OpenStax). Mid/high D; D=0 auto stays one-step LIATE.
PARTS_FORM_PRESETS: dict[str, frozenset[str] | None] = {
    "auto": None,
    "bc_bank": frozenset(
        {
            "poly2_exp",
            "poly3_exp",
            "poly2_sin",
            "poly2_cos",
            "poly3_sin",
            "poly3_cos",
            "poly2_ln",
            "ln_power_2",
            "ln_power_3",
            "cyclic_exp_sin",
            "cyclic_exp_cos",
            "arctan_alone",
            "poly1_arctan",
            "poly1_arcsin",
            "arcsin_alone",
            "power_frac_ln",
            "ln_quad",
        }
    ),
}
PARTS_FORM_PRESET_OPTIONS: tuple[str, ...] = tuple(PARTS_FORM_PRESETS.keys())

# Calc BC drill bank §4 families the existing PFD core can emit.
PFD_FORM_PRESETS: dict[str, frozenset[str] | None] = {
    "auto": None,
    "bc_bank": frozenset(
        {
            "distinct_linear_2",
            "distinct_linear_3",
            "irreducible_quad_arctan",
            "irreducible_quad_ln",
            "mixed_linear_quad",
            "repeated_linear_square",
        }
    ),
}
PFD_FORM_PRESET_OPTIONS: tuple[str, ...] = tuple(PFD_FORM_PRESETS.keys())

# Calc BC drill bank §5 families the existing trig-sub sampler can emit.
# D=0 auto stays ∫√(a²−x²); easy OpenStax form is not in this hard set.
TRIG_SUB_FORM_PRESETS: dict[str, frozenset[str] | None] = {
    "auto": None,
    "bc_bank": frozenset(
        {
            "sqrt_a2_plus_x2",
            "sqrt_x2_minus_a2",
            "one_over_sqrt_x2_plus_a2",
            "one_over_sqrt_x2_minus_a2",
            "x2_over_sqrt_a2_minus_x2",
            "x2_over_sqrt_x2_plus_a2",
            "x2_over_sqrt_x2_minus_a2",
            "pow_3_2_a2_minus",
            "pow_3_2_a2_plus",
            "pow_m3_2_a2_plus",
            "pow_m3_2_a2_minus",
            "pow_m3_2_x2_minus",
        }
    ),
}
TRIG_SUB_FORM_PRESET_OPTIONS: tuple[str, ...] = tuple(TRIG_SUB_FORM_PRESETS.keys())


def resolve_parts_form_preset(name: str | None) -> frozenset[str] | None:
    key = str(name or "auto").strip().lower()
    if key not in PARTS_FORM_PRESETS:
        return None
    return PARTS_FORM_PRESETS[key]


def resolve_pfd_form_preset(name: str | None) -> frozenset[str] | None:
    key = str(name or "auto").strip().lower()
    if key not in PFD_FORM_PRESETS:
        return None
    return PFD_FORM_PRESETS[key]


def resolve_trig_sub_form_preset(name: str | None) -> frozenset[str] | None:
    key = str(name or "auto").strip().lower()
    if key not in TRIG_SUB_FORM_PRESETS:
        return None
    return TRIG_SUB_FORM_PRESETS[key]


def _parts_kx(k: int, var: str) -> str:
    return var if k == 1 else f"{k}{var}"


def _parts_exp_kx(k: int, var: str) -> str:
    return rf"e^{{{_parts_kx(k, var)}}}"


def _parts_trig(fn: str, k: int, var: str) -> str:
    arg = _parts_kx(k, var)
    if fn == "sin":
        return rf"\sin({arg})"
    if fn == "cos":
        return rf"\cos({arg})"
    return rf"\tan({arg})"


def _parts_chain_k(rng: random.Random, spec: IntegralSpec, *, floor_d: float = 8.0) -> int:
    """Scale inner frequency/base: D=0 stays k=1 (old easy); mid+ D uses k≥2."""
    if float(spec.d_spend) < floor_d:
        return 1
    hi = max(2, min(4, int(spec.coef_abs_max)))
    return rng.randint(2, hi)


def _parts_allows_ok(form: dict[str, Any], spec: IntegralSpec) -> bool:
    flags = {
        "allow_trig": spec.allow_trig,
        "allow_exp": spec.allow_exp,
        "allow_log": spec.allow_log,
        "allow_invtrig": spec.allow_invtrig,
    }
    for key in form.get("requires_allows") or []:
        if not flags.get(str(key), True):
            return False
    return True


def _parts_coef_term(coef: int, tex: str) -> str:
    if coef == 1:
        return tex
    if coef == -1:
        return rf"-{tex}"
    return rf"{coef}{tex}"


def _parts_poly_desc(coeffs: Sequence[int], var: str) -> str:
    """Highest-degree-first integer polynomial, no wrapping parens."""
    n = len(list(coeffs)) - 1
    pieces: list[str] = []
    for i, c in enumerate(coeffs):
        if c == 0:
            continue
        power = n - i
        mag = abs(int(c))
        if power == 0:
            body = str(mag)
        elif power == 1:
            body = var if mag == 1 else f"{mag}{var}"
        else:
            body = rf"{var}^{{{power}}}" if mag == 1 else rf"{mag}{var}^{{{power}}}"
        if not pieces:
            pieces.append(f"-{body}" if c < 0 else body)
        else:
            pieces.append(f"-{body}" if c < 0 else f"+{body}")
    return "".join(pieces) or "0"


def _ibp_poly_exp(n: int, k: int, var: str, include: bool) -> tuple[str, str]:
    """∫ x^n e^{kx} dx via tabular parts (n≥1)."""
    exp = _parts_exp_kx(k, var)
    xn = var if n == 1 else rf"{var}^{{{n}}}"
    prompt = rf"\int {xn}{exp}\,d{var}"
    coeffs = [
        ((-1) ** j) * (factorial(n) // factorial(n - j)) * (k ** (n - j))
        for j in range(n + 1)
    ]
    poly = _parts_poly_desc(coeffs, var)
    den = k ** (n + 1)
    if den == 1:
        answer = _plus_c(rf"e^{{{var}}}({poly})", include=include)
    else:
        answer = _plus_c(
            rf"{frac_latex(Fraction(1, den))}{exp}({poly})",
            include=include,
        )
    return prompt, answer


def _parts_ln_scale(rng: random.Random, spec: IntegralSpec, var: str) -> tuple[int, str]:
    a = 1
    if float(spec.d_spend) >= 8:
        a = rng.randint(2, max(2, min(4, spec.coef_abs_max)))
    arg = var if a == 1 else f"{a}{var}"
    return a, arg


def _sample_parts(
    rng: random.Random, spec: IntegralSpec
) -> tuple[str, str, dict[str, Any]]:
    """LIATE forms driven by ``integration_by_parts`` catalog.

    D=0 rotates one-step OpenStax shapes with k=1 (∫ ln x, ∫ x e^x, ∫ x sin x,
    ∫ x cos x). Mid D scales the inner (e^{kx}, sin(kx), ln(ax)). High D
    unlocks tabular (x^n n≤3), (ln)^n, cyclic e^{ax}sin/cos, and invtrig.
    """
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        catalog_form_meta,
        implemented_forms,
        load_form_catalog,
        select_form_id,
    )

    var = spec.variable
    catalog = load_form_catalog("integration_by_parts")
    preset_ids = resolve_parts_form_preset(spec.parts_form_preset)
    pool = _gated_form_pool(
        catalog, spec, extra_ids=set(preset_ids) if preset_ids else None
    )
    if not pool and preset_ids:
        pool = _gated_form_pool(catalog, spec)
    if not pool:
        # Dedicated parts leaf with every class off: keep ln_alone only if log is on.
        pool = [
            f
            for f in implemented_forms(catalog)
            if str(f.get("form_id")) == "ln_alone" and spec.allow_log
        ]
    if not pool:
        return _sample_power(rng, spec)
    # Repeated parts (tabular / cyclic) when the D budget bought parts_twice.
    if spec.parts_depth >= 2:
        rich = [f for f in pool if float(f.get("d_min") or 0) >= 10]
        if rich:
            pool = rich
    form = select_form_id(pool, d=float(spec.d_spend), rng=rng)
    form_id = str(form["form_id"])
    include = spec.include_plus_c
    meta = {
        **catalog_form_meta(form, catalog),
        "family": form_id,
        "n_terms": 1,
        "nest": spec.parts_depth,
    }
    k = _parts_chain_k(rng, spec)

    if form_id == "ln_alone":
        a, b = 1, 0
        if float(spec.d_spend) >= 8:
            a = rng.randint(1, max(1, min(4, spec.coef_abs_max)))
            b = rng.randint(0, max(0, min(3, spec.coef_abs_max))) if spec.d_spend >= 12 else 0
            if a == 1 and b == 0:
                a = 2
        arg = var if (a == 1 and b == 0) else format_linear_latex(a, b, variable=var)
        prompt = rf"\int \ln({arg})\,d{var}"
        if a == 1 and b == 0:
            answer = _plus_c(rf"{var}\ln({var})-{var}", include=include)
        elif b == 0:
            answer = _plus_c(rf"{var}\ln({arg})-{var}", include=include)
        else:
            body = rf"{frac_latex(Fraction(1, a))}\left({arg}\right)\ln({arg})-{var}"
            answer = _plus_c(body, include=include)
        classes = ["log"]
    elif form_id == "poly1_ln":
        a = 1 if float(spec.d_spend) < 8 else rng.randint(2, max(2, min(4, spec.coef_abs_max)))
        arg = var if a == 1 else f"{a}{var}"
        prompt = rf"\int {var}\ln({arg})\,d{var}"
        if a == 1:
            answer = _plus_c(
                rf"\frac{{1}}{{2}}{var}^{{2}}\ln({var})-\frac{{1}}{{4}}{var}^{{2}}",
                include=include,
            )
        else:
            answer = _plus_c(
                rf"\frac{{1}}{{2}}{var}^{{2}}\ln({arg})-\frac{{1}}{{4}}{var}^{{2}}",
                include=include,
            )
        classes = ["log"]
    elif form_id == "poly1_exp":
        prompt, answer = _ibp_poly_exp(1, k, var, include)
        classes = ["exp"]
    elif form_id == "poly1_sin":
        s = _parts_trig("sin", k, var)
        c = _parts_trig("cos", k, var)
        prompt = rf"\int {var}{s}\,d{var}"
        if k == 1:
            answer = _plus_c(rf"-{var}\cos({var})+\sin({var})", include=include)
        else:
            answer = _plus_c(
                rf"-{frac_latex(Fraction(1, k))}{var}{c}+{frac_latex(Fraction(1, k * k))}{s}",
                include=include,
            )
        classes = ["trig"]
    elif form_id == "poly1_cos":
        s = _parts_trig("sin", k, var)
        c = _parts_trig("cos", k, var)
        prompt = rf"\int {var}{c}\,d{var}"
        if k == 1:
            answer = _plus_c(rf"{var}\sin({var})+\cos({var})", include=include)
        else:
            answer = _plus_c(
                rf"{frac_latex(Fraction(1, k))}{var}{s}+{frac_latex(Fraction(1, k * k))}{c}",
                include=include,
            )
        classes = ["trig"]
    elif form_id == "poly2_exp":
        prompt, answer = _ibp_poly_exp(2, k, var, include)
        classes = ["exp"]
    elif form_id == "poly3_exp":
        prompt, answer = _ibp_poly_exp(3, k, var, include)
        classes = ["exp"]
    elif form_id == "poly2_sin":
        s = _parts_trig("sin", k, var)
        c = _parts_trig("cos", k, var)
        prompt = rf"\int {var}^{{2}}{s}\,d{var}"
        if k == 1:
            answer = _plus_c(
                rf"-{var}^{{2}}\cos({var})+2{var}\sin({var})+2\cos({var})",
                include=include,
            )
        else:
            # (−k² x² cos + 2k x sin + 2 cos) / k³
            num = rf"-{k * k}{var}^{{2}}{c}+{2 * k}{var}{s}+2{c}"
            answer = _plus_c(
                rf"{frac_latex(Fraction(1, k ** 3))}({num})",
                include=include,
            )
        classes = ["trig"]
    elif form_id == "poly2_cos":
        s = _parts_trig("sin", k, var)
        c = _parts_trig("cos", k, var)
        prompt = rf"\int {var}^{{2}}{c}\,d{var}"
        if k == 1:
            answer = _plus_c(
                rf"{var}^{{2}}\sin({var})+2{var}\cos({var})-2\sin({var})",
                include=include,
            )
        else:
            # (k² x² sin + 2k x cos − 2 sin) / k³
            num = rf"{k * k}{var}^{{2}}{s}+{2 * k}{var}{c}-2{s}"
            answer = _plus_c(
                rf"{frac_latex(Fraction(1, k ** 3))}({num})",
                include=include,
            )
        classes = ["trig"]
    elif form_id == "poly3_sin":
        s = _parts_trig("sin", k, var)
        c = _parts_trig("cos", k, var)
        prompt = rf"\int {var}^{{3}}{s}\,d{var}"
        if k == 1:
            answer = _plus_c(
                rf"-{var}^{{3}}\cos({var})+3{var}^{{2}}\sin({var})"
                rf"+6{var}\cos({var})-6\sin({var})",
                include=include,
            )
        else:
            # (−k³ x³ cos + 3k² x² sin + 6k x cos − 6 sin) / k⁴
            num = (
                rf"-{k ** 3}{var}^{{3}}{c}+{3 * k * k}{var}^{{2}}{s}"
                rf"+{6 * k}{var}{c}-6{s}"
            )
            answer = _plus_c(
                rf"{frac_latex(Fraction(1, k ** 4))}({num})",
                include=include,
            )
        classes = ["trig"]
    elif form_id == "poly3_cos":
        s = _parts_trig("sin", k, var)
        c = _parts_trig("cos", k, var)
        prompt = rf"\int {var}^{{3}}{c}\,d{var}"
        if k == 1:
            answer = _plus_c(
                rf"{var}^{{3}}\sin({var})+3{var}^{{2}}\cos({var})"
                rf"-6{var}\sin({var})-6\cos({var})",
                include=include,
            )
        else:
            # (k³ x³ sin + 3k² x² cos − 6k x sin − 6 cos) / k⁴
            num = (
                rf"{k ** 3}{var}^{{3}}{s}+{3 * k * k}{var}^{{2}}{c}"
                rf"-{6 * k}{var}{s}-6{c}"
            )
            answer = _plus_c(
                rf"{frac_latex(Fraction(1, k ** 4))}({num})",
                include=include,
            )
        classes = ["trig"]
    elif form_id == "poly2_ln":
        _a, arg = _parts_ln_scale(rng, spec, var)
        prompt = rf"\int {var}^{{2}}\ln({arg})\,d{var}"
        answer = _plus_c(
            rf"\frac{{1}}{{3}}{var}^{{3}}\ln({arg})-\frac{{1}}{{9}}{var}^{{3}}",
            include=include,
        )
        classes = ["log"]
    elif form_id == "ln_power_2":
        _a, arg = _parts_ln_scale(rng, spec, var)
        prompt = rf"\int (\ln({arg}))^{{2}}\,d{var}"
        answer = _plus_c(
            rf"{var}(\ln({arg}))^{{2}}-2{var}\ln({arg})+2{var}",
            include=include,
        )
        classes = ["log"]
    elif form_id == "ln_power_3":
        _a, arg = _parts_ln_scale(rng, spec, var)
        prompt = rf"\int (\ln({arg}))^{{3}}\,d{var}"
        answer = _plus_c(
            rf"{var}(\ln({arg}))^{{3}}-3{var}(\ln({arg}))^{{2}}"
            rf"+6{var}\ln({arg})-6{var}",
            include=include,
        )
        classes = ["log"]
    elif form_id == "power_frac_ln":
        _a, arg = _parts_ln_scale(rng, spec, var)
        if rng.random() < 0.5:
            prompt = rf"\int \sqrt{{{var}}}\ln({arg})\,d{var}"
            answer = _plus_c(
                rf"\frac{{2}}{{3}}{var}^{{3/2}}\ln({arg})-\frac{{4}}{{9}}{var}^{{3/2}}",
                include=include,
            )
        else:
            prompt = rf"\int {var}^{{3/2}}\ln({arg})\,d{var}"
            answer = _plus_c(
                rf"\frac{{2}}{{5}}{var}^{{5/2}}\ln({arg})-\frac{{4}}{{25}}{var}^{{5/2}}",
                include=include,
            )
        classes = ["log"]
    elif form_id == "cyclic_exp_sin":
        a = b = 1
        if float(spec.d_spend) >= 16:
            a = rng.randint(1, 3)
            b = rng.randint(1, 3)
            if a == 1 and b == 1:
                a = 2
        exp = _parts_exp_kx(a, var)
        s = _parts_trig("sin", b, var)
        c = _parts_trig("cos", b, var)
        prompt = rf"\int {exp}{s}\,d{var}"
        if a == 1 and b == 1:
            answer = _plus_c(
                rf"\frac{{1}}{{2}}e^{{{var}}}(\sin({var})-\cos({var}))",
                include=include,
            )
        else:
            num = rf"{_parts_coef_term(a, s)}-{_parts_coef_term(b, c)}"
            den = a * a + b * b
            answer = _plus_c(rf"\frac{{{exp}({num})}}{{{den}}}", include=include)
        classes = ["exp", "trig"]
    elif form_id == "cyclic_exp_cos":
        a = b = 1
        if float(spec.d_spend) >= 16:
            a = rng.randint(1, 3)
            b = rng.randint(1, 3)
            if a == 1 and b == 1:
                a = 2
        exp = _parts_exp_kx(a, var)
        s = _parts_trig("sin", b, var)
        c = _parts_trig("cos", b, var)
        prompt = rf"\int {exp}{c}\,d{var}"
        if a == 1 and b == 1:
            answer = _plus_c(
                rf"\frac{{1}}{{2}}e^{{{var}}}(\sin({var})+\cos({var}))",
                include=include,
            )
        else:
            # (a cos(bx) + b sin(bx))
            num = rf"{_parts_coef_term(a, c)}+{_parts_coef_term(b, s)}"
            den = a * a + b * b
            answer = _plus_c(rf"\frac{{{exp}({num})}}{{{den}}}", include=include)
        classes = ["exp", "trig"]
    elif form_id == "arctan_alone":
        a = 1 if float(spec.d_spend) < 18 else rng.randint(2, 3)
        arg = var if a == 1 else f"{a}{var}"
        prompt = rf"\int \arctan({arg})\,d{var}"
        if a == 1:
            answer = _plus_c(
                rf"{var}\arctan({var})-\frac{{1}}{{2}}\ln(1+{var}^{{2}})",
                include=include,
            )
        else:
            # ∫ arctan(ax) = x arctan(ax) − (1/(2a)) ln(1+a²x²)
            answer = _plus_c(
                rf"{var}\arctan({arg})-{frac_latex(Fraction(1, 2 * a))}\ln(1+{a * a}{var}^{{2}})",
                include=include,
            )
        classes = ["invtrig"]
    elif form_id == "poly1_arctan":
        a = 1 if float(spec.d_spend) < 18 else rng.randint(2, 3)
        arg = var if a == 1 else f"{a}{var}"
        prompt = rf"\int {var}\arctan({arg})\,d{var}"
        # (x²/2) arctan(ax) − x/(2a) + arctan(ax)/(2a²)
        answer = _plus_c(
            rf"\frac{{1}}{{2}}{var}^{{2}}\arctan({arg})"
            rf"-{frac_latex(Fraction(1, 2 * a))}{var}"
            rf"+{frac_latex(Fraction(1, 2 * a * a))}\arctan({arg})",
            include=include,
        )
        classes = ["invtrig"]
    elif form_id == "arcsin_alone":
        a = 1 if float(spec.d_spend) < 18 else rng.randint(2, 3)
        arg = var if a == 1 else f"{a}{var}"
        prompt = rf"\int \arcsin({arg})\,d{var}"
        if a == 1:
            answer = _plus_c(
                rf"{var}\arcsin({var})+\sqrt{{1-{var}^{{2}}}}",
                include=include,
            )
        else:
            answer = _plus_c(
                rf"{var}\arcsin({arg})+{frac_latex(Fraction(1, a))}"
                rf"\sqrt{{1-{a * a}{var}^{{2}}}}",
                include=include,
            )
        classes = ["invtrig"]
    elif form_id == "poly1_arcsin":
        prompt = rf"\int {var}\arcsin({var})\,d{var}"
        answer = _plus_c(
            rf"\frac{{1}}{{2}}{var}^{{2}}\arcsin({var})"
            rf"+\frac{{1}}{{4}}{var}\sqrt{{1-{var}^{{2}}}}"
            rf"-\frac{{1}}{{4}}\arcsin({var})",
            include=include,
        )
        classes = ["invtrig"]
    elif form_id == "ln_quad":
        a = 1 if float(spec.d_spend) < 18 else rng.randint(2, 3)
        inner = rf"{var}^{{2}}+1" if a == 1 else rf"{var}^{{2}}+{a * a}"
        prompt = rf"\int \ln({inner})\,d{var}"
        atan_arg = var if a == 1 else rf"\frac{{{var}}}{{{a}}}"
        atan_coef = 2 * a
        atan_tex = (
            rf"2\arctan({atan_arg})"
            if atan_coef == 2
            else rf"{atan_coef}\arctan({atan_arg})"
        )
        answer = _plus_c(
            rf"{var}\ln({inner})-2{var}+{atan_tex}",
            include=include,
        )
        classes = ["log", "invtrig"]
    else:
        prompt = rf"\int {var}e^{{{var}}}\,d{var}"
        answer = _plus_c(rf"e^{{{var}}}({var}-1)", include=include)
        classes = ["exp"]
        meta["form_id"] = "poly1_exp"
        meta["openstax_form"] = "poly1_exp"
        meta["family"] = "poly1_exp"
    meta["function_classes"] = classes
    meta["tricks_required"] = [str(t) for t in (form.get("tricks") or ["parts"])]
    meta["parts_k"] = k
    meta["parts_form_preset"] = spec.parts_form_preset
    return prompt, answer, meta


FTC1_GENERATOR = "first_fundamental_theorem"

_FTC1_BANDS: dict[str, tuple[str, ...]] = {
    "easy": ("ftc1_linear", "ftc1_quad"),
    "medium": ("ftc1_linear", "ftc1_quad", "ftc1_quad_const"),
    "hard": ("ftc1_quad_const", "ftc1_sqrt", "ftc1_sin"),
    "expert": ("ftc1_sqrt", "ftc1_sin"),
}


def ftc1_forms_for_difficulty(d: float) -> tuple[str, ...]:
    """Leftover lockout of D=0 ∫x / ∫kx²; D=22 is √x / sin only."""
    if d < 8.0:
        return _FTC1_BANDS["easy"]
    if d < 16.0:
        return _FTC1_BANDS["medium"]
    if d < 20.0:
        return _FTC1_BANDS["hard"]
    return _FTC1_BANDS["expert"]


def _ftc1_form_rows(forms: tuple[str, ...]) -> list[dict[str, Any]]:
    return [
        {
            "form_id": fid,
            "d_min": 0.0,
            "d_weight": 1.0,
            "generation_status": "implemented",
            "generator_keys": [FTC1_GENERATOR],
        }
        for fid in forms
    ]


def _sample_ftc1_linear(
    rng: random.Random, var: str, b_hi: int
) -> tuple[str, str, list[str]]:
    """Old-path D=0 leftover: ∫_0^b x dx."""
    b = rng.randint(2, max(2, b_hi))
    prompt = rf"\int_{{0}}^{{{b}}} {var}\,d{var}"
    return prompt, frac_latex(Fraction(b * b, 2)), ["algebraic"]


def _sample_ftc1_quad(
    rng: random.Random, var: str, b_hi: int, coef_hi: int
) -> tuple[str, str, list[str]]:
    """Old-path D=0 leftover: ∫_0^b k x^2 dx (k≥1)."""
    b = rng.randint(2, max(2, b_hi))
    k = rng.randint(1, max(1, min(6, coef_hi)))
    f = format_monomial_latex(k, variable=var, degree=2) or f"{k}{var}^{{2}}"
    prompt = rf"\int_{{0}}^{{{b}}} {f}\,d{var}"
    return prompt, frac_latex(Fraction(k * b**3, 3)), ["algebraic"]


def _sample_ftc1_quad_const(
    rng: random.Random, var: str, b_hi: int, coef_hi: int
) -> tuple[str, str, list[str]]:
    """Old mid unlock: ∫_0^b (p x^2 + q) dx."""
    b = rng.randint(2, max(2, b_hi))
    p = rng.randint(1, max(1, min(4, coef_hi)))
    q = _coef(rng, max(2, min(4, coef_hi)))
    f = format_polynomial_latex([p, 0, q], variable=var)
    prompt = rf"\int_{{0}}^{{{b}}} \left({f}\right)\,d{var}"
    return prompt, frac_latex(Fraction(p * b**3, 3) + q * b), ["algebraic"]


def _sample_ftc1_sqrt(
    rng: random.Random, var: str, d: float
) -> tuple[str, str, list[str]]:
    """Old high unlock: ∫_0^b √x dx; b a perfect square for a clean key."""
    b = rng.choice([1, 4, 9] if d < 18 else [1, 4, 9, 16])
    prompt = rf"\int_{{0}}^{{{b}}} \sqrt{{{var}}}\,d{var}"
    root = int(b**0.5)
    return prompt, frac_latex(Fraction(2 * b * root, 3)), ["algebraic"]


def _sample_ftc1_sin(var: str) -> tuple[str, str, list[str]]:
    """Old high unlock: ∫_0^{π/2} sin(x) dx = 1."""
    prompt = rf"\int_{{0}}^{{\pi/2}} \sin({var})\,d{var}"
    return prompt, "1", ["trig"]


def _sample_ftc(
    rng: random.Random, spec: IntegralSpec
) -> tuple[str, str, dict[str, Any]]:
    """FTC evaluation ∫_a^b f (OpenStax Part 2 / first_fundamental_theorem leaf).

    High D locks out D=0 ∫x / ∫kx² leftovers. Same five old builders.
    """
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        select_form_id,
    )

    var = spec.variable
    d = float(spec.d_spend)
    forms = ftc1_forms_for_difficulty(d)
    b_hi = max(2, min(8, spec.bound_abs_max))
    form = select_form_id(_ftc1_form_rows(forms), d=d, rng=rng)
    fid = str(form.get("form_id") or forms[0])
    if fid == "ftc1_linear" and fid in forms:
        prompt, answer, classes = _sample_ftc1_linear(rng, var, b_hi)
    elif fid == "ftc1_quad" and fid in forms:
        prompt, answer, classes = _sample_ftc1_quad(
            rng, var, b_hi, spec.coef_abs_max
        )
    elif fid == "ftc1_quad_const" and fid in forms:
        prompt, answer, classes = _sample_ftc1_quad_const(
            rng, var, b_hi, spec.coef_abs_max
        )
    elif fid == "ftc1_sqrt" and fid in forms:
        prompt, answer, classes = _sample_ftc1_sqrt(rng, var, d)
    elif fid == "ftc1_sin" and fid in forms:
        prompt, answer, classes = _sample_ftc1_sin(var)
    else:
        fid = forms[0]
        if fid == "ftc1_quad":
            prompt, answer, classes = _sample_ftc1_quad(
                rng, var, b_hi, spec.coef_abs_max
            )
        elif fid == "ftc1_quad_const":
            prompt, answer, classes = _sample_ftc1_quad_const(
                rng, var, b_hi, spec.coef_abs_max
            )
        elif fid == "ftc1_sqrt":
            prompt, answer, classes = _sample_ftc1_sqrt(rng, var, d)
        elif fid == "ftc1_sin":
            prompt, answer, classes = _sample_ftc1_sin(var)
        else:
            prompt, answer, classes = _sample_ftc1_linear(rng, var, b_hi)
    return prompt, answer, {
        "function_classes": classes,
        "family": fid,
        "form_id": fid,
        "generator": FTC1_GENERATOR,
        "n_terms": 1,
        "definite": True,
    }


FTC2_GENERATOR = "second_fundamental_theorem"

_FTC2_BANDS: dict[str, tuple[str, ...]] = {
    "easy": ("ftc2_poly",),
    "medium": ("ftc2_poly", "ftc2_trig"),
    "hard": ("ftc2_trig", "ftc2_chain"),
    "expert": ("ftc2_chain",),
}


def ftc2_forms_for_difficulty(d: float) -> tuple[str, ...]:
    """Leftover lockout of D=0 d/dx ∫ t²; D=22 is chain g(x)=kx only."""
    if d < 8.0:
        return _FTC2_BANDS["easy"]
    if d < 16.0:
        return _FTC2_BANDS["medium"]
    if d < 20.0:
        return _FTC2_BANDS["hard"]
    return _FTC2_BANDS["expert"]


def _ftc2_form_rows(forms: tuple[str, ...]) -> list[dict[str, Any]]:
    return [
        {
            "form_id": fid,
            "d_min": 0.0,
            "d_weight": 1.0,
            "generation_status": "implemented",
            "generator_keys": [FTC2_GENERATOR],
        }
        for fid in forms
    ]


def _sample_ftc2_poly(rng: random.Random, var: str) -> tuple[str, str, list[str]]:
    """Old-path D=0 leftover: d/dx ∫_a^x t^2 dt → x^2."""
    a = rng.randint(0, 3)
    prompt = rf"\frac{{d}}{{d{var}}}\int_{{{a}}}^{{{var}}} t^{{2}}\,dt"
    return prompt, rf"{var}^{{2}}", ["algebraic"]


def _sample_ftc2_trig(rng: random.Random, var: str) -> tuple[str, str, list[str]]:
    """Old mid unlock: d/dx ∫_a^x sin(t) dt → sin(x)."""
    a = rng.randint(0, 3)
    prompt = rf"\frac{{d}}{{d{var}}}\int_{{{a}}}^{{{var}}} \sin(t)\,dt"
    return prompt, rf"\sin({var})", ["trig"]


def _sample_ftc2_chain(
    rng: random.Random, var: str, coef_hi: int
) -> tuple[str, str, list[str]]:
    """Old high unlock: d/dx ∫_a^{kx} e^t dt → k e^{kx}."""
    a = rng.randint(0, 3)
    k = rng.randint(2, max(2, min(5, coef_hi)))
    prompt = rf"\frac{{d}}{{d{var}}}\int_{{{a}}}^{{{k}{var}}} e^{{t}}\,dt"
    return prompt, rf"{k}e^{{{k}{var}}}", ["exp"]


def _sample_ftc2(
    rng: random.Random, spec: IntegralSpec
) -> tuple[str, str, dict[str, Any]]:
    """FTC Part 1: d/dx ∫_a^{g(x)} f(t) dt (second_fundamental_theorem leaf).

    High D locks out D=0 t² leftover. Same three old builders.
    """
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        select_form_id,
    )

    var = spec.variable
    d = float(spec.d_spend)
    forms = ftc2_forms_for_difficulty(d)
    form = select_form_id(_ftc2_form_rows(forms), d=d, rng=rng)
    fid = str(form.get("form_id") or forms[0])
    if fid == "ftc2_poly" and fid in forms:
        prompt, answer, classes = _sample_ftc2_poly(rng, var)
    elif fid == "ftc2_trig" and fid in forms:
        prompt, answer, classes = _sample_ftc2_trig(rng, var)
    elif fid == "ftc2_chain" and fid in forms:
        prompt, answer, classes = _sample_ftc2_chain(rng, var, spec.coef_abs_max)
    else:
        fid = forms[0]
        if fid == "ftc2_trig":
            prompt, answer, classes = _sample_ftc2_trig(rng, var)
        elif fid == "ftc2_chain":
            prompt, answer, classes = _sample_ftc2_chain(
                rng, var, spec.coef_abs_max
            )
        else:
            prompt, answer, classes = _sample_ftc2_poly(rng, var)
    return prompt, answer, {
        "function_classes": classes,
        "family": fid,
        "form_id": fid,
        "generator": FTC2_GENERATOR,
        "n_terms": 1,
        "definite": True,
        "construction": "ftc_variable_upper",
    }


def _sample_trig_sub(
    rng: random.Random,
    spec: IntegralSpec,
    *,
    with_u_wrap: bool = False,
) -> tuple[str, str, dict[str, Any]]:
    """Genuine trig-substitution integrands (OpenStax Vol. 2 Ch. 3 style).

    Forms force ``x = a sinθ``, ``x = a tanθ``, or ``x = a secθ`` — never plain
    power u-sub like ∫ 2x(x²+1)^n dx.

    Optional ``with_u_wrap`` uses ``u = x + b`` (b≠0) so a preliminary
    u-sub is truly required before the trig sub.
    """
    var = spec.variable
    a = rng.randint(2, max(2, min(5, spec.coef_abs_max)))

    # Catalog-driven form_id (family names match catalog entries).
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        catalog_form_meta,
        implemented_forms,
        load_form_catalog,
        select_form_id,
    )

    catalog = load_form_catalog("trig_substitution")
    wrap_ok = {
        "sqrt_a2_minus_x2",
        "sqrt_a2_plus_x2",
        "sqrt_x2_minus_a2",
        "one_over_sqrt_x2_plus_a2",
        "one_over_sqrt_x2_minus_a2",
        "pow_3_2_a2_minus",
        "pow_3_2_a2_plus",
        "pow_m3_2_a2_plus",
        "pow_m3_2_a2_minus",
        "pow_m3_2_x2_minus",
    }
    preset_ids = resolve_trig_sub_form_preset(spec.trig_sub_form_preset)
    extra: set[str] | None = set(preset_ids) if preset_ids else None
    do_wrap = bool(with_u_wrap)
    if do_wrap:
        allowed_wrap = wrap_ok if extra is None else (extra & wrap_ok)
        if allowed_wrap:
            extra = allowed_wrap if extra is not None else wrap_ok
        else:
            do_wrap = False
    b_shift = rng.choice([-3, -2, -1, 1, 2, 3]) if do_wrap else 0

    # Inner linear for wrap: u = x + b (always parenthesize when shifted so
    # ``(1/2)u`` does not parse as ``(1/2)x - 2``).
    if b_shift == 0:
        u = var
        u_disp = var
        u2 = f"{var}^{{2}}"
    else:
        u = format_linear_latex(1, b_shift, variable=var)
        u_disp = rf"\left({u}\right)"
        u2 = rf"{u_disp}^{{2}}"

    pool = _gated_form_pool(catalog, spec, extra_ids=extra)
    if not pool:
        pool = _gated_form_pool(catalog, spec)
    if not pool:
        if spec.allow_trig_sub:
            pool = implemented_forms(catalog)
        else:
            return _sample_power(rng, spec)
    form = select_form_id(pool, d=float(spec.d_spend), rng=rng)
    family = str(form["form_id"])
    catalog_meta = catalog_form_meta(form, catalog)
    tricks: list[str] = ["u_sub", "trig_sub"] if b_shift != 0 else ["trig_sub"]

    a2_i = a * a
    a2 = str(a2_i)
    half_a2 = frac_latex(Fraction(a2_i, 2))
    power = Fraction(1, 2)

    if family == "sqrt_a2_minus_x2":
        prompt = rf"\int \sqrt{{{a2}-{u2}}}\,d{var}"
        answer = _plus_c(
            rf"\frac{{1}}{{2}}{u_disp}\sqrt{{{a2}-{u2}}}"
            rf"+{half_a2}\arcsin\left(\frac{{{u}}}{{{a}}}\right)",
            include=spec.include_plus_c,
        )
        sub = "sin"
    elif family == "sqrt_a2_plus_x2":
        prompt = rf"\int \sqrt{{{a2}+{u2}}}\,d{var}"
        answer = _plus_c(
            rf"\frac{{1}}{{2}}{u_disp}\sqrt{{{a2}+{u2}}}"
            rf"+{half_a2}\ln\left|{u}+\sqrt{{{a2}+{u2}}}\right|",
            include=spec.include_plus_c,
        )
        sub = "tan"
    elif family == "sqrt_x2_minus_a2":
        prompt = rf"\int \sqrt{{{u2}-{a2}}}\,d{var}"
        answer = _plus_c(
            rf"\frac{{1}}{{2}}{u_disp}\sqrt{{{u2}-{a2}}}"
            rf"-{half_a2}\ln\left|{u}+\sqrt{{{u2}-{a2}}}\right|",
            include=spec.include_plus_c,
        )
        sub = "sec"
    elif family == "one_over_sqrt_x2_plus_a2":
        power = Fraction(-1, 2)
        prompt = rf"\int \frac{{1}}{{\sqrt{{{u2}+{a2}}}}}\,d{var}"
        answer = _plus_c(
            rf"\ln\left|{u}+\sqrt{{{u2}+{a2}}}\right|",
            include=spec.include_plus_c,
        )
        sub = "tan"
    elif family == "one_over_sqrt_x2_minus_a2":
        power = Fraction(-1, 2)
        prompt = rf"\int \frac{{1}}{{\sqrt{{{u2}-{a2}}}}}\,d{var}"
        answer = _plus_c(
            rf"\ln\left|{u}+\sqrt{{{u2}-{a2}}}\right|",
            include=spec.include_plus_c,
        )
        sub = "sec"
    elif family == "x2_over_sqrt_a2_minus_x2":
        tricks = ["trig_sub"]
        b_shift = 0
        prompt = rf"\int \frac{{{var}^{{2}}}}{{\sqrt{{{a2}-{var}^{{2}}}}}}\,d{var}"
        answer = _plus_c(
            rf"-\frac{{1}}{{2}}{var}\sqrt{{{a2}-{var}^{{2}}}}"
            rf"+{half_a2}\arcsin\left(\frac{{{var}}}{{{a}}}\right)",
            include=spec.include_plus_c,
        )
        sub = "sin"
    elif family == "x2_over_sqrt_x2_plus_a2":
        tricks = ["trig_sub"]
        b_shift = 0
        prompt = rf"\int \frac{{{var}^{{2}}}}{{\sqrt{{{var}^{{2}}+{a2}}}}}\,d{var}"
        answer = _plus_c(
            rf"\frac{{1}}{{2}}{var}\sqrt{{{var}^{{2}}+{a2}}}"
            rf"-{half_a2}\ln\left|{var}+\sqrt{{{var}^{{2}}+{a2}}}\right|",
            include=spec.include_plus_c,
        )
        sub = "tan"
    elif family == "x2_over_sqrt_x2_minus_a2":
        tricks = ["trig_sub"]
        b_shift = 0
        prompt = rf"\int \frac{{{var}^{{2}}}}{{\sqrt{{{var}^{{2}}-{a2}}}}}\,d{var}"
        answer = _plus_c(
            rf"\frac{{1}}{{2}}{var}\sqrt{{{var}^{{2}}-{a2}}}"
            rf"+{half_a2}\ln\left|{var}+\sqrt{{{var}^{{2}}-{a2}}}\right|",
            include=spec.include_plus_c,
        )
        sub = "sec"
    elif family == "pow_3_2_a2_minus":
        # OpenStax: ∫ (a²−x²)^{3/2} dx after x=a sinθ
        power = Fraction(3, 2)
        prompt = rf"\int \left({a2}-{u2}\right)^{{\frac{{3}}{{2}}}}\,d{var}"
        answer = _plus_c(
            rf"\frac{{{u_disp}}}{{8}}\left(2{u2}+{a2}\right)\sqrt{{{a2}-{u2}}}"
            rf"+\frac{{{a2_i * a2_i}}}{{8}}\arcsin\left(\frac{{{u}}}{{{a}}}\right)",
            include=spec.include_plus_c,
        )
        sub = "sin"
    elif family == "pow_3_2_a2_plus":
        power = Fraction(3, 2)
        prompt = rf"\int \left({a2}+{u2}\right)^{{\frac{{3}}{{2}}}}\,d{var}"
        answer = _plus_c(
            rf"\frac{{{u_disp}}}{{8}}\left(2{u2}+{a2}\right)\sqrt{{{a2}+{u2}}}"
            rf"+\frac{{{a2_i * a2_i}}}{{8}}\ln\left|{u}+\sqrt{{{a2}+{u2}}}\right|",
            include=spec.include_plus_c,
        )
        sub = "tan"
    elif family == "pow_m3_2_a2_plus":
        power = Fraction(-3, 2)
        prompt = rf"\int \frac{{1}}{{\left({a2}+{u2}\right)^{{\frac{{3}}{{2}}}}}}\,d{var}"
        answer = _plus_c(
            rf"\frac{{{u}}}{{{a2}\sqrt{{{a2}+{u2}}}}}",
            include=spec.include_plus_c,
        )
        sub = "tan"
    elif family == "pow_m3_2_a2_minus":
        power = Fraction(-3, 2)
        prompt = rf"\int \frac{{1}}{{\left({a2}-{u2}\right)^{{\frac{{3}}{{2}}}}}}\,d{var}"
        answer = _plus_c(
            rf"\frac{{{u}}}{{{a2}\sqrt{{{a2}-{u2}}}}}",
            include=spec.include_plus_c,
        )
        sub = "sin"
    elif family == "pow_m3_2_x2_minus":
        power = Fraction(-3, 2)
        prompt = rf"\int \frac{{1}}{{\left({u2}-{a2}\right)^{{\frac{{3}}{{2}}}}}}\,d{var}"
        answer = _plus_c(
            rf"-\frac{{{u}}}{{{a2}\sqrt{{{u2}-{a2}}}}}",
            include=spec.include_plus_c,
        )
        sub = "sec"
    elif family == "pow_m5_2_a2_plus":
        power = Fraction(-5, 2)
        prompt = rf"\int \frac{{1}}{{\left({a2}+{u2}\right)^{{\frac{{5}}{{2}}}}}}\,d{var}"
        answer = _plus_c(
            rf"\frac{{{u}\left(2{u2}+3{a2}\right)}}{{3{a2}^{{2}}\left({a2}+{u2}\right)^{{\frac{{3}}{{2}}}}}}",
            include=spec.include_plus_c,
        )
        sub = "tan"
    elif family == "pow_5_2_a2_minus":
        power = Fraction(5, 2)
        prompt = rf"\int \left({a2}-{u2}\right)^{{\frac{{5}}{{2}}}}\,d{var}"
        answer = _plus_c(
            rf"\frac{{{u_disp}}}{{48}}\left(8{u2}^{{2}}+10{a2}{u2}+15{a2}^{{2}}\right)"
            rf"\sqrt{{{a2}-{u2}}}"
            rf"+\frac{{{a2_i ** 3}}}{{16}}\arcsin\left(\frac{{{u}}}{{{a}}}\right)",
            include=spec.include_plus_c,
        )
        sub = "sin"
    else:
        # Catalog fallback: denser rational×sqrt (OpenStax, not BC §5).
        tricks = ["trig_sub"]
        b_shift = 0
        power = Fraction(-1, 2)
        prompt = (
            rf"\int \frac{{1}}{{{var}^{{2}}\sqrt{{{var}^{{2}}+{a2}}}}}\,d{var}"
        )
        answer = _plus_c(
            rf"-\frac{{\sqrt{{{var}^{{2}}+{a2}}}}}{{{a2}{var}}}",
            include=spec.include_plus_c,
        )
        family = "one_over_x2_sqrt_x2_plus_a2"
        sub = "tan"

    return prompt, answer, {
        **catalog_meta,
        "function_classes": ["trig", "algebraic"],
        "family": family,
        "form_id": family,
        "openstax_form": family,
        "n_terms": 1,
        "trig_sub_kind": sub,
        "trig_sub_exponent": str(power),
        "tricks_required": tricks,
        "trig_sub_form_preset": spec.trig_sub_form_preset,
        "u_linear": [1, b_shift] if b_shift != 0 else None,
        "nest": 1 if b_shift != 0 else 0,
    }


# ---------------------------------------------------------------------------
# Derivative-backed u-sub
# ---------------------------------------------------------------------------


DEFINITE_USUB_GENERATOR = "integral_definite_substitution"

_DEFINITE_USUB_BANDS: dict[str, tuple[str, ...]] = {
    "easy": ("definite_power_linear_du",),
    "medium": ("definite_power_linear_du", "definite_power_quad_x_du"),
    "hard": ("definite_power_quad_x_du", "definite_du_over_u"),
    "expert": ("definite_du_over_u",),
}


def definite_usub_forms_for_difficulty(d: float) -> tuple[str, ...]:
    """Leftover lockout of D=0 linear changed-limits; D=22 is du/u only."""
    if d < 8.0:
        return _DEFINITE_USUB_BANDS["easy"]
    if d < 16.0:
        return _DEFINITE_USUB_BANDS["medium"]
    if d < 20.0:
        return _DEFINITE_USUB_BANDS["hard"]
    return _DEFINITE_USUB_BANDS["expert"]


def _definite_usub_form_rows(forms: tuple[str, ...]) -> list[dict[str, Any]]:
    return [
        {
            "form_id": fid,
            "d_min": 0.0,
            "d_weight": 1.0,
            "generation_status": "implemented",
            "generator_keys": [DEFINITE_USUB_GENERATOR],
        }
        for fid in forms
    ]


def _sample_definite_power_linear_du(
    rng: random.Random, spec: IntegralSpec, d: float
) -> tuple[str, str]:
    """Old-path D=0 leftover: ∫_0^b p(px+q)^n dx (linear u)."""
    var = spec.variable
    p = rng.randint(2, max(2, min(4, spec.coef_abs_max)))
    q = rng.randint(0, max(0, min(3, spec.coef_abs_max)))
    n = rng.randint(2, 3 if d < 10 else 5)
    lo = 0
    hi = rng.randint(1, max(1, min(3, spec.bound_abs_max)))
    u_lo = p * lo + q
    u_hi = p * hi + q
    inner = format_linear_latex(p, q, variable=var)
    prompt = rf"\int_{{{lo}}}^{{{hi}}} {p}\left({inner}\right)^{{{n}}}\,d{var}"
    ans = Fraction(u_hi ** (n + 1) - u_lo ** (n + 1), n + 1)
    return prompt, frac_latex(ans)


def _sample_definite_power_quad_x_du(
    rng: random.Random, spec: IntegralSpec, d: float
) -> tuple[str, str]:
    """Old mid unlock: ∫_0^a 2x (x²+1)^n dx, u=x²+1."""
    var = spec.variable
    a = rng.randint(1, max(1, min(3, spec.bound_abs_max)))
    n = rng.randint(2, 2 if d < 14 else 3)
    prompt = rf"\int_{{0}}^{{{a}}} 2{var}\left({var}^{{2}}+1\right)^{{{n}}}\,d{var}"
    u_hi = a * a + 1
    ans = Fraction(u_hi ** (n + 1) - 1, n + 1)
    return prompt, frac_latex(ans)


def _sample_definite_du_over_u(
    rng: random.Random, spec: IntegralSpec
) -> tuple[str, str]:
    """Old high unlock: ∫_0^a 2x/(x²+1) dx = ln(a²+1)."""
    var = spec.variable
    a = rng.randint(1, max(1, min(3, spec.bound_abs_max)))
    prompt = rf"\int_{{0}}^{{{a}}} \frac{{2{var}}}{{{var}^{{2}}+1}}\,d{var}"
    return prompt, rf"\ln({a * a + 1})"


def _sample_definite_u_sub(
    rng: random.Random, spec: IntegralSpec
) -> tuple[str, str, dict[str, Any]]:
    """Definite u-sub with changed limits (OpenStax Vol 1 §5.5).

    High D locks out D=0 linear leftover. Same three old builders.
    """
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        select_form_id,
    )

    d = float(spec.d_spend)
    forms = definite_usub_forms_for_difficulty(d)
    form = select_form_id(_definite_usub_form_rows(forms), d=d, rng=rng)
    fid = str(form.get("form_id") or forms[0])
    if fid == "definite_power_linear_du" and fid in forms:
        prompt, answer = _sample_definite_power_linear_du(rng, spec, d)
    elif fid == "definite_power_quad_x_du" and fid in forms:
        prompt, answer = _sample_definite_power_quad_x_du(rng, spec, d)
    elif fid == "definite_du_over_u" and fid in forms:
        prompt, answer = _sample_definite_du_over_u(rng, spec)
    else:
        fid = forms[0]
        if fid == "definite_power_quad_x_du":
            prompt, answer = _sample_definite_power_quad_x_du(rng, spec, d)
        elif fid == "definite_du_over_u":
            prompt, answer = _sample_definite_du_over_u(rng, spec)
        else:
            prompt, answer = _sample_definite_power_linear_du(rng, spec, d)

    return prompt, answer, {
        "function_classes": ["algebraic"],
        "family": fid,
        "form_id": fid,
        "generator": DEFINITE_USUB_GENERATOR,
        "n_terms": 1,
        "definite": True,
        "tricks_required": ["u_sub"],
        "construction": "definite_change_of_variables",
    }


def _sample_u_sub_derivative_backed(
    rng: random.Random, spec: IntegralSpec, *, flavor: str = "power"
) -> tuple[str, str, dict[str, Any]]:
    """Catalog-driven u-sub; optional reverse-chain via Diff expr_skeleton."""
    from question_engine.frameworks.primitives import u_substitution as usub
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        catalog_form_meta,
        implemented_forms,
        load_form_catalog,
        select_form_id,
    )
    from question_engine.frameworks.primitives.skeleton_difficulty import (
        SkeletonDifficultyBands,
    )

    var = spec.variable
    include = spec.include_plus_c
    bands = SkeletonDifficultyBands.from_d(float(spec.d_spend))
    preset_forms = usub.resolve_u_sub_form_preset(spec.u_sub_form_preset)
    construction = str(spec.u_sub_construction or "auto")
    use_reverse = False
    if construction == "reverse_chain":
        use_reverse = True
    elif construction != "catalog" and preset_forms is None and bands.format_tier >= 1:
        p_rev = (0.0, 0.4, 0.65, 0.8, 0.9)[min(4, bands.format_tier)]
        use_reverse = rng.random() < p_rev
    if use_reverse:
        try:
            sample = usub.sample_reverse_chain_integral(
                d=float(spec.d_spend),
                flavor=flavor,
                variable=var,
                include_plus_c=include,
                allow_trig=spec.allow_trig,
                allow_exp=spec.allow_exp,
                allow_log=spec.allow_log,
                allow_invtrig=spec.allow_invtrig,
                rng=rng,
            )
            meta = dict(sample.metadata)
            meta["n_terms"] = 1
            meta["u_sub_form_preset"] = spec.u_sub_form_preset
            return sample.prompt_latex, sample.answer_latex, meta
        except (KeyError, ValueError, TypeError):
            use_reverse = False

    catalog = load_form_catalog("u_substitution")
    # Flavor packs bias which forms are eligible
    flavor_allow = {
        "power": {
            "power_linear_du",
            "power_quad_x_du",
            "power_cubic_x2_du",
            "root_quad_x_du",
            "du_over_u_linear",
            "alteration_linear_over_root",
            "power_quad_neg",
            "power_cubic_neg",
            "root_quad_minus",
            "power_quad_m3_2",
            "du_over_u_quadratic",
            "sin_of_sqrt",
            "power_hex_neg",
            "root_of_x4",
        },
        "ln_exp": {
            "exp_of_trig",
            "exp_of_poly",
            "exp_of_cubic",
            "exp_of_quartic",
            "exp_root_chain",
            "exp_power_of_exp",
            "du_over_u_linear",
            "ln_squared_chain",
            "nested_trig_exp",
            "du_over_u_trig",
            "ln_power_over_x",
            "power_of_one_plus_ln",
            "exp_over_power_of_exp",
            "exp_e2x_over_power",
            "ln_ln_nested",
            "ln_over_x_sqrt",
            "arctan_of_ln",
            "du_over_ln_of_poly",
            "cos_of_ln_over_x",
            "exp_of_sqrt",
            "root_ln_of_linear",
            "ln_sq_over_root_ln_cube",
        },
        "trig": {
            "du_over_u_trig",
            "trig_of_linear",
            "sec2_of_u",
            "exp_of_trig",
            "nested_trig_exp",
            "composite_ln_of_trig",
            "trig_over_linear_trig_power",
            "sin_of_sqrt",
        },
        "invtrig": {
            "arctan_of_linear",
            "du_over_u_linear",
            "power_linear_du",
            "arctan_of_ln",
        },
    }
    allow = set(flavor_allow.get(flavor) or ())
    if preset_forms is not None:
        allow = (allow & set(preset_forms)) or set(preset_forms)
    pool = _gated_form_pool(catalog, spec, extra_ids=allow or None)
    if not pool and preset_forms is not None:
        # Forced named preset on a host whose allow_* would empty the
        # intersection (trig_chain showcase on the algebraic power leaf).
        pool = [
            f
            for f in implemented_forms(catalog)
            if str(f.get("form_id")) in allow
        ]
    if not pool:
        pool = _gated_form_pool(catalog, spec)
    if not pool:
        pool = _gated_form_pool(catalog, spec, extra_ids={"power_linear_du"})
    if not pool:
        pool = implemented_forms(catalog)[:1]
    form = select_form_id(pool, d=float(spec.d_spend), rng=rng)
    form_id = str(form["form_id"])
    form_tricks = [str(t) for t in (form.get("tricks") or ["u_sub"])]
    meta = {
        **catalog_form_meta(form, catalog),
        "n_terms": 1,
        "tricks_required": form_tricks,
        "family": form_id,
    }

    nt = bands.numeric_tier
    a_hi = (2, 3, 4, 6, 8)[nt]
    n_hi = (2, 3, 4, 5, 6)[nt]
    a = rng.randint(2, max(2, min(a_hi, spec.coef_abs_max)))
    b_hi = (2, 3, 5, 8, 12)[nt]
    b = _coef(rng, max(2, min(b_hi, spec.coef_abs_max)), exclude_zero=False)
    n = rng.randint(2, max(2, min(n_hi, spec.degree_max)))
    c = rng.randint(1, max(1, min((3, 4, 6, 9, 12)[nt], spec.coef_abs_max)))
    meta["u_sub_form_preset"] = spec.u_sub_form_preset
    meta["numeric_tier"] = nt
    meta["format_tier"] = bands.format_tier

    if form_id == "power_linear_du":
        inner = format_linear_latex(a, b, variable=var)
        hide = bands.format_tier >= 2
        if hide:
            prompt = rf"\int \left({inner}\right)^{{{n}}}\,d{var}"
            answer = _plus_c(
                rf"\frac{{1}}{{{a * (n + 1)}}}\left({inner}\right)^{{{n + 1}}}",
                include=include,
            )
            meta["omit_du_constant"] = True
        else:
            prompt = rf"\int {a}\left({inner}\right)^{{{n}}}\,d{var}"
            answer = _plus_c(
                rf"\frac{{1}}{{{n + 1}}}\left({inner}\right)^{{{n + 1}}}",
                include=include,
            )
        meta["function_classes"] = ["algebraic"]
        return prompt, answer, meta
    if form_id == "power_quad_x_du":
        prompt = rf"\int 2{var}\left({var}^{{2}}+{c}\right)^{{{n}}}\,d{var}"
        answer = _plus_c(
            rf"\frac{{1}}{{{n + 1}}}\left({var}^{{2}}+{c}\right)^{{{n + 1}}}",
            include=include,
        )
        meta["function_classes"] = ["algebraic"]
        return prompt, answer, meta
    if form_id == "power_cubic_x2_du":
        # Checkpoint 5.25: ∫ 3x² (x³-3)² dx; 5.26 omits the 3.
        shift = c if rng.random() < 0.5 else -c
        inner = (
            rf"{var}^{{3}}+{shift}" if shift > 0 else rf"{var}^{{3}}-{abs(shift)}"
        )
        hide = bands.format_tier >= 2
        if hide:
            prompt = rf"\int {var}^{{2}}\left({inner}\right)^{{{n}}}\,d{var}"
            answer = _plus_c(
                rf"\frac{{1}}{{{3 * (n + 1)}}}\left({inner}\right)^{{{n + 1}}}",
                include=include,
            )
            meta["omit_du_constant"] = True
        else:
            prompt = rf"\int 3{var}^{{2}}\left({inner}\right)^{{{n}}}\,d{var}"
            answer = _plus_c(
                rf"\frac{{1}}{{{n + 1}}}\left({inner}\right)^{{{n + 1}}}",
                include=include,
            )
        meta["function_classes"] = ["algebraic"]
        return prompt, answer, meta
    if form_id == "root_quad_x_du":
        prompt = rf"\int {var}\sqrt{{{var}^{{2}}+{c}}}\,d{var}"
        answer = _plus_c(
            rf"\frac{{1}}{{3}}\left({var}^{{2}}+{c}\right)^{{\frac{{3}}{{2}}}}",
            include=include,
        )
        meta["function_classes"] = ["algebraic"]
        return prompt, answer, meta
    if form_id == "du_over_u_linear":
        inner = format_linear_latex(a, b, variable=var)
        prompt = rf"\int \frac{{{a}}}{{{inner}}}\,d{var}"
        answer = _plus_c(rf"\ln|{inner}|", include=include)
        meta["function_classes"] = ["log", "algebraic"]
        return prompt, answer, meta
    if form_id == "du_over_u_trig":
        if rng.random() < 0.5:
            prompt = rf"\int \frac{{\sin({var})}}{{\cos^{{3}}({var})}}\,d{var}"
            answer = _plus_c(rf"\frac{{1}}{{2}}\sec^{{2}}({var})", include=include)
        else:
            prompt = rf"\int \frac{{\cos({var})}}{{\sin^{{2}}({var})}}\,d{var}"
            answer = _plus_c(rf"-\frac{{1}}{{\sin({var})}}", include=include)
        meta["function_classes"] = ["trig"]
        return prompt, answer, meta
    if form_id in {"exp_of_trig", "nested_trig_exp"}:
        k = 1 if form_id == "exp_of_trig" else rng.choice([2, 3])
        arg = var if k == 1 else f"{k}{var}"
        if rng.random() < 0.5:
            prompt = rf"\int e^{{\sin({arg})}}\cos({arg})\,d{var}"
            if k == 1:
                answer = _plus_c(rf"e^{{\sin({var})}}", include=include)
            else:
                answer = _plus_c(
                    rf"\frac{{1}}{{{k}}}e^{{\sin({arg})}}",
                    include=include,
                )
        else:
            prompt = rf"\int e^{{\cos({arg})}}\sin({arg})\,d{var}"
            if k == 1:
                answer = _plus_c(rf"-e^{{\cos({var})}}", include=include)
            else:
                answer = _plus_c(
                    rf"-\frac{{1}}{{{k}}}e^{{\cos({arg})}}",
                    include=include,
                )
        meta["function_classes"] = ["exp", "trig"]
        return prompt, answer, meta
    if form_id == "exp_of_poly":
        inner = format_linear_latex(a, b, variable=var)
        prompt = rf"\int {a}e^{{{inner}}}\,d{var}"
        answer = _plus_c(rf"e^{{{inner}}}", include=include)
        meta["function_classes"] = ["exp"]
        return prompt, answer, meta
    if form_id == "exp_of_cubic":
        # Example 5.39: ∫ 3x² e^{2x³}; Checkpoint 5.31: x² e^{-2x³} (omit 3).
        a_exp = rng.choice([-2, -1, 1, 2]) if nt >= 1 else rng.choice([1, 2])
        if a_exp == 1:
            inner = rf"{var}^{{3}}"
        elif a_exp == -1:
            inner = rf"-{var}^{{3}}"
        else:
            inner = rf"{a_exp}{var}^{{3}}"
        hide = bands.format_tier >= 2
        if hide:
            prompt = rf"\int {var}^{{2}}e^{{{inner}}}\,d{var}"
            scale = 3 * a_exp
        else:
            prompt = rf"\int 3{var}^{{2}}e^{{{inner}}}\,d{var}"
            scale = a_exp
            meta["omit_du_constant"] = False
        if hide:
            meta["omit_du_constant"] = True
        if scale == 1:
            body = rf"e^{{{inner}}}"
        elif scale == -1:
            body = rf"-e^{{{inner}}}"
        else:
            body = rf"{frac_latex(Fraction(1, scale))}e^{{{inner}}}"
        answer = _plus_c(body, include=include)
        meta["function_classes"] = ["exp", "algebraic"]
        return prompt, answer, meta
    if form_id == "exp_of_quartic":
        # Checkpoint 5.33: ∫ 2x³ e^{x⁴} dx (u=x⁴, du=4x³ dx).
        a_exp = rng.choice([-2, -1, 1, 2]) if nt >= 1 else rng.choice([1, 2])
        if a_exp == 1:
            inner = rf"{var}^{{4}}"
        elif a_exp == -1:
            inner = rf"-{var}^{{4}}"
        else:
            inner = rf"{a_exp}{var}^{{4}}"
        hide = bands.format_tier >= 2
        if hide:
            prompt = rf"\int {var}^{{3}}e^{{{inner}}}\,d{var}"
            scale = 4 * a_exp
            meta["omit_du_constant"] = True
        else:
            prompt = rf"\int 2{var}^{{3}}e^{{{inner}}}\,d{var}"
            scale = 2 * a_exp
            meta["omit_du_constant"] = False
        if scale == 1:
            body = rf"e^{{{inner}}}"
        elif scale == -1:
            body = rf"-e^{{{inner}}}"
        else:
            body = rf"{frac_latex(Fraction(1, scale))}e^{{{inner}}}"
        answer = _plus_c(body, include=include)
        meta["function_classes"] = ["exp", "algebraic"]
        return prompt, answer, meta
    if form_id == "exp_root_chain":
        # Example 5.38: ∫ e^x √(1+e^x) dx
        c0 = rng.choice([1, 2, 3])
        prompt = rf"\int e^{{{var}}}\sqrt{{{c0}+e^{{{var}}}}}\,d{var}"
        answer = _plus_c(
            rf"\frac{{2}}{{3}}\left({c0}+e^{{{var}}}\right)^{{\frac{{3}}{{2}}}}",
            include=include,
        )
        meta["function_classes"] = ["exp", "algebraic"]
        return prompt, answer, meta
    if form_id == "exp_power_of_exp":
        # Checkpoint 5.32: ∫ e^x (3e^x-2)² dx
        aa = rng.randint(2, max(2, a_hi))
        bb = rng.randint(1, max(1, min(4, spec.coef_abs_max)))
        inner = (
            rf"{aa}e^{{{var}}}+{bb}"
            if rng.random() < 0.5
            else rf"{aa}e^{{{var}}}-{bb}"
        )
        prompt = rf"\int e^{{{var}}}\left({inner}\right)^{{{n}}}\,d{var}"
        answer = _plus_c(
            rf"\frac{{1}}{{{aa * (n + 1)}}}\left({inner}\right)^{{{n + 1}}}",
            include=include,
        )
        meta["function_classes"] = ["exp", "algebraic"]
        return prompt, answer, meta
    if form_id == "trig_of_linear":
        inner = format_linear_latex(a, b, variable=var)
        if rng.random() < 0.5:
            prompt = rf"\int {a}\cos({inner})\,d{var}"
            answer = _plus_c(rf"\sin({inner})", include=include)
        else:
            prompt = rf"\int {a}\sin({inner})\,d{var}"
            answer = _plus_c(rf"-\cos({inner})", include=include)
        meta["function_classes"] = ["trig"]
        return prompt, answer, meta
    if form_id == "arctan_of_linear":
        inner = format_linear_latex(a, b, variable=var)
        prompt = rf"\int \frac{{{a}}}{{1+({inner})^{{2}}}}\,d{var}"
        answer = _plus_c(rf"\arctan({inner})", include=include)
        meta["function_classes"] = ["invtrig"]
        return prompt, answer, meta
    if form_id == "ln_squared_chain":
        inner = format_linear_latex(a, b, variable=var)
        prompt = rf"\int \frac{{{a}}}{{{inner}}}\ln|{inner}|\,d{var}"
        answer = _plus_c(
            rf"\frac{{1}}{{2}}\left(\ln|{inner}|\right)^{{2}}",
            include=include,
        )
        meta["function_classes"] = ["log"]
        return prompt, answer, meta
    if form_id == "alteration_linear_over_root":
        # ∫ x/√(x−1): let u=x−1 → ∫ (u+1)/√u = ∫(u^{1/2}+u^{-1/2})
        aa = rng.choice([1, 2])
        prompt = rf"\int \frac{{{var}}}{{\sqrt{{{var}-{aa}}}}}\,d{var}"
        # antideriv: (2/3)(x−a)^{3/2} + 2a(x−a)^{1/2}
        answer = _plus_c(
            rf"\frac{{2}}{{3}}\left({var}-{aa}\right)^{{\frac{{3}}{{2}}}}"
            rf"+{2 * aa}\sqrt{{{var}-{aa}}}",
            include=include,
        )
        meta["function_classes"] = ["algebraic"]
        return prompt, answer, meta
    if form_id == "sec2_of_u":
        inner = format_linear_latex(a, b, variable=var)
        prompt = rf"\int {a}\sec^{{2}}({inner})\,d{var}"
        answer = _plus_c(rf"\tan({inner})", include=include)
        meta["function_classes"] = ["trig"]
        return prompt, answer, meta
    if form_id == "composite_ln_of_trig":
        # ∫ cot = ln|sin|; ∫ tan = −ln|cos| (rewrite then du/u).
        if rng.random() < 0.5:
            prompt = rf"\int \cot({var})\,d{var}"
            answer = _plus_c(rf"\ln|\sin({var})|", include=include)
        else:
            prompt = rf"\int \tan({var})\,d{var}"
            answer = _plus_c(rf"-\ln|\cos({var})|", include=include)
        meta["function_classes"] = ["trig", "log"]
        return prompt, answer, meta

    # BC bank §1 families (closed reverse-chain / du-over-u). D-gated in catalog.
    n_neg = rng.choice([2, 3, 4] if nt >= 2 else [2, 3])
    if form_id == "power_quad_neg":
        # Bank ∫ x/(x²+1)⁴ is one draw of ∫ a x / (b x² + c)^n.
        bq = 1 if nt < 2 else rng.choice([1, 1, 2])
        aq = 1 if (nt < 2 or rng.random() < 0.55) else rng.randint(2, min(3, a_hi))
        inner = rf"{var}^{{2}}+{c}" if bq == 1 else rf"{bq}{var}^{{2}}+{c}"
        num = var if aq == 1 else rf"{aq}{var}"
        prompt = rf"\int \frac{{{num}}}{{\left({inner}\right)^{{{n_neg}}}}}\,d{var}"
        answer = _neg_power_antideriv(
            inner, n_neg, 2 * bq, include=include, num_coef=aq
        )
        meta["function_classes"] = ["algebraic"]
        meta["omit_du_constant"] = True
        return prompt, answer, meta
    if form_id == "power_cubic_neg":
        shift = c if rng.random() < 0.5 else -c
        bq = 1 if nt < 2 else rng.choice([1, 1, 2])
        inner = (
            rf"{var}^{{3}}+{shift}"
            if bq == 1 and shift > 0
            else (
                rf"{var}^{{3}}-{abs(shift)}"
                if bq == 1
                else (
                    rf"{bq}{var}^{{3}}+{shift}"
                    if shift > 0
                    else rf"{bq}{var}^{{3}}-{abs(shift)}"
                )
            )
        )
        hide = bands.format_tier >= 2
        if hide:
            prompt = rf"\int \frac{{{var}^{{2}}}}{{\left({inner}\right)^{{{n_neg}}}}}\,d{var}"
            answer = _neg_power_antideriv(
                inner, n_neg, 3 * bq, include=include, num_coef=1
            )
            meta["omit_du_constant"] = True
        else:
            num = rf"3{var}^{{2}}" if bq == 1 else rf"{3 * bq}{var}^{{2}}"
            prompt = rf"\int \frac{{{num}}}{{\left({inner}\right)^{{{n_neg}}}}}\,d{var}"
            answer = _neg_power_antideriv(
                inner, n_neg, 3 * bq, include=include, num_coef=3 * bq
            )
        meta["function_classes"] = ["algebraic"]
        return prompt, answer, meta
    if form_id == "root_quad_minus":
        cc = rng.choice([4, 9, 16] if nt >= 1 else [4, 9])
        prompt = rf"\int \frac{{{var}}}{{\sqrt{{{cc}-{var}^{{2}}}}}}\,d{var}"
        answer = _plus_c(rf"-\sqrt{{{cc}-{var}^{{2}}}}", include=include)
        meta["function_classes"] = ["algebraic"]
        meta["omit_du_constant"] = True
        return prompt, answer, meta
    if form_id == "power_quad_m3_2":
        inner = rf"1+{var}^{{2}}" if rng.random() < 0.5 else rf"{var}^{{2}}+{c}"
        prompt = (
            rf"\int \frac{{{var}}}{{\left({inner}\right)\sqrt{{{inner}}}}}\,d{var}"
        )
        answer = _plus_c(rf"-\frac{{1}}{{\sqrt{{{inner}}}}}", include=include)
        meta["function_classes"] = ["algebraic"]
        meta["omit_du_constant"] = True
        return prompt, answer, meta
    if form_id == "ln_power_over_x":
        pn = rng.choice([2, 3] if nt < 3 else [2, 3, 4])
        prompt = rf"\int \frac{{\left(\ln {var}\right)^{{{pn}}}}}{{{var}}}\,d{var}"
        answer = _plus_c(
            rf"\frac{{1}}{{{pn + 1}}}\left(\ln {var}\right)^{{{pn + 1}}}",
            include=include,
        )
        meta["function_classes"] = ["log"]
        return prompt, answer, meta
    if form_id == "power_of_one_plus_ln":
        aa = rng.choice([1, 2])
        inner = rf"{aa}+\ln {var}" if aa != 1 else rf"1+\ln {var}"
        prompt = rf"\int \frac{{1}}{{{var}\left({inner}\right)^{{{n_neg}}}}}\,d{var}"
        answer = _neg_power_antideriv(inner, n_neg, 1, include=include)
        meta["function_classes"] = ["log"]
        return prompt, answer, meta
    if form_id == "exp_over_power_of_exp":
        aa = rng.choice([1, 2, 3])
        inner = rf"{aa}+e^{{{var}}}" if aa != 1 else rf"1+e^{{{var}}}"
        prompt = rf"\int \frac{{e^{{{var}}}}}{{\left({inner}\right)^{{{n_neg}}}}}\,d{var}"
        answer = _neg_power_antideriv(inner, n_neg, 1, include=include)
        meta["function_classes"] = ["exp"]
        return prompt, answer, meta
    if form_id == "exp_e2x_over_power":
        # u=a+e^x, e^{2x} dx = (u-a) du; n=3 bank item.
        aa = rng.choice([1, 2])
        inner = rf"{aa}+e^{{{var}}}" if aa != 1 else rf"1+e^{{{var}}}"
        prompt = rf"\int \frac{{e^{{2{var}}}}}{{\left({inner}\right)^{{3}}}}\,d{var}"
        # ∫ (u-a)/u^3 du = −1/u + a/(2 u^2)
        if aa == 1:
            body = rf"-\frac{{1}}{{{inner}}}+\frac{{1}}{{2\left({inner}\right)^{{2}}}}"
        else:
            body = (
                rf"-\frac{{1}}{{{inner}}}"
                rf"+\frac{{{aa}}}{{2\left({inner}\right)^{{2}}}}"
            )
        answer = _plus_c(body, include=include)
        meta["function_classes"] = ["exp"]
        return prompt, answer, meta
    if form_id == "trig_over_linear_trig_power":
        aa = rng.choice([1, 2, 3])
        kind = rng.choice(["sin_cos", "cos_sin", "sec2_tan", "sectan_sec"])
        if kind == "sin_cos":
            inner = rf"{aa}+\cos({var})"
            prompt = rf"\int \frac{{\sin({var})}}{{\left({inner}\right)^{{{n_neg}}}}}\,d{var}"
            answer = _neg_power_antideriv(inner, n_neg, -1, include=include)
        elif kind == "cos_sin":
            inner = rf"{aa}+\sin({var})"
            prompt = rf"\int \frac{{\cos({var})}}{{\left({inner}\right)^{{{n_neg}}}}}\,d{var}"
            answer = _neg_power_antideriv(inner, n_neg, 1, include=include)
        elif kind == "sec2_tan":
            inner = rf"{aa}+\tan({var})"
            prompt = rf"\int \frac{{\sec^{{2}}({var})}}{{\left({inner}\right)^{{{n_neg}}}}}\,d{var}"
            answer = _neg_power_antideriv(inner, n_neg, 1, include=include)
        else:
            inner = rf"{aa}+\sec({var})"
            prompt = (
                rf"\int \frac{{\sec({var})\tan({var})}}"
                rf"{{\left({inner}\right)^{{{n_neg}}}}}\,d{var}"
            )
            answer = _neg_power_antideriv(inner, n_neg, 1, include=include)
        meta["function_classes"] = ["trig"]
        return prompt, answer, meta
    if form_id == "ln_ln_nested":
        prompt = (
            rf"\int \frac{{1}}{{{var}\ln {var}\left(\ln(\ln {var})\right)^{{2}}}}"
            rf"\,d{var}"
        )
        answer = _neg_power_antideriv(rf"\ln(\ln {var})", 2, 1, include=include)
        meta["function_classes"] = ["log"]
        return prompt, answer, meta
    if form_id == "ln_over_x_sqrt":
        prompt = rf"\int \frac{{1}}{{{var}\sqrt{{\ln {var}}}}}\,d{var}"
        answer = _plus_c(rf"2\sqrt{{\ln {var}}}", include=include)
        meta["function_classes"] = ["log"]
        return prompt, answer, meta
    if form_id == "arctan_of_ln":
        prompt = rf"\int \frac{{1}}{{{var}\left(1+(\ln {var})^{{2}}\right)}}\,d{var}"
        answer = _plus_c(rf"\arctan(\ln {var})", include=include)
        meta["function_classes"] = ["log", "invtrig"]
        return prompt, answer, meta
    if form_id == "du_over_u_quadratic":
        bb = rng.choice([1, 2])
        cc = rng.randint(2, max(2, min(9, spec.coef_abs_max)))
        lin = rf"{var}" if bb == 1 else rf"{bb}{var}"
        inner = rf"{var}^{{2}}+{lin}+{cc}"
        num = rf"2{var}+{bb}"
        prompt = rf"\int \frac{{{num}}}{{{inner}}}\,d{var}"
        answer = _plus_c(rf"\ln|{inner}|", include=include)
        meta["function_classes"] = ["log", "algebraic"]
        return prompt, answer, meta
    if form_id == "du_over_ln_of_poly":
        shift = c if rng.random() < 0.5 else -c
        poly = (
            rf"{var}^{{3}}+{shift}" if shift > 0 else rf"{var}^{{3}}-{abs(shift)}"
        )
        prompt = (
            rf"\int \frac{{{var}^{{2}}}}{{\left({poly}\right)\ln\left({poly}\right)}}"
            rf"\,d{var}"
        )
        answer = _plus_c(
            rf"\frac{{1}}{{3}}\ln\left|\ln\left({poly}\right)\right|",
            include=include,
        )
        meta["function_classes"] = ["log"]
        meta["omit_du_constant"] = True
        return prompt, answer, meta
    if form_id == "cos_of_ln_over_x":
        if rng.random() < 0.5:
            prompt = rf"\int \frac{{\cos(\ln {var})}}{{{var}}}\,d{var}"
            answer = _plus_c(rf"\sin(\ln {var})", include=include)
        else:
            prompt = rf"\int \frac{{\sin(\ln {var})}}{{{var}}}\,d{var}"
            answer = _plus_c(rf"-\cos(\ln {var})", include=include)
        meta["function_classes"] = ["log", "trig"]
        return prompt, answer, meta
    if form_id == "sin_of_sqrt":
        prompt = rf"\int \frac{{\sin(\sqrt{{{var}}})}}{{\sqrt{{{var}}}}}\,d{var}"
        answer = _plus_c(rf"-2\cos(\sqrt{{{var}}})", include=include)
        meta["function_classes"] = ["trig", "algebraic"]
        meta["omit_du_constant"] = True
        return prompt, answer, meta
    if form_id == "exp_of_sqrt":
        prompt = rf"\int \frac{{e^{{\sqrt{{{var}}}}}}}{{\sqrt{{{var}}}}}\,d{var}"
        answer = _plus_c(rf"2e^{{\sqrt{{{var}}}}}", include=include)
        meta["function_classes"] = ["exp", "algebraic"]
        meta["omit_du_constant"] = True
        return prompt, answer, meta
    if form_id == "root_ln_of_linear":
        aa = rng.choice([1, 2])
        lin = rf"{var}+{aa}"
        prompt = rf"\int \frac{{1}}{{\left({lin}\right)\sqrt{{\ln({lin})}}}}\,d{var}"
        answer = _plus_c(rf"2\sqrt{{\ln({lin})}}", include=include)
        meta["function_classes"] = ["log"]
        return prompt, answer, meta
    if form_id == "ln_sq_over_root_ln_cube":
        prompt = (
            rf"\int \frac{{\left(\ln {var}\right)^{{2}}}}"
            rf"{{{var}\sqrt{{1+\left(\ln {var}\right)^{{3}}}}}}\,d{var}"
        )
        answer = _plus_c(
            rf"\frac{{2}}{{3}}\sqrt{{1+\left(\ln {var}\right)^{{3}}}}",
            include=include,
        )
        meta["function_classes"] = ["log"]
        return prompt, answer, meta
    if form_id == "power_hex_neg":
        bq = 1 if nt < 2 else rng.choice([1, 1, 2])
        inner = rf"{var}^{{6}}+{c}" if bq == 1 else rf"{bq}{var}^{{6}}+{c}"
        prompt = rf"\int \frac{{{var}^{{5}}}}{{\left({inner}\right)^{{{n_neg}}}}}\,d{var}"
        answer = _neg_power_antideriv(inner, n_neg, 6 * bq, include=include)
        meta["function_classes"] = ["algebraic"]
        meta["omit_du_constant"] = True
        return prompt, answer, meta
    if form_id == "root_of_x4":
        bq = 1 if nt < 2 else rng.choice([1, 1, 2])
        inner = (
            rf"1+{var}^{{4}}"
            if bq == 1 and rng.random() < 0.5
            else (rf"{var}^{{4}}+{c}" if bq == 1 else rf"{bq}{var}^{{4}}+{c}")
        )
        prompt = rf"\int \frac{{{var}^{{3}}}}{{\sqrt{{{inner}}}}}\,d{var}"
        # ∫ x³ / √(b x⁴ + c) = (1/(2b)) * 2 √u = √u / b
        if bq == 1:
            answer = _plus_c(rf"\frac{{1}}{{2}}\sqrt{{{inner}}}", include=include)
        else:
            answer = _plus_c(
                rf"{frac_latex(Fraction(1, 2 * bq))}\sqrt{{{inner}}}",
                include=include,
            )
        meta["function_classes"] = ["algebraic"]
        meta["omit_du_constant"] = True
        return prompt, answer, meta

    # Fallback: shared sampler
    u_spec = usub.usub_spec_from_integral_flavor(
        flavor,
        d=float(spec.d_spend),
        variable=spec.variable,
        coef_abs_max=spec.coef_abs_max,
        degree_max=spec.degree_max,
        include_plus_c=spec.include_plus_c,
    )
    sample = usub.sample_u_sub(u_spec, rng=rng)
    out = dict(sample.metadata)
    out.update(meta)
    out["construction"] = "shared_u_sub"
    out["n_terms"] = 1
    return sample.prompt_latex, sample.answer_latex, out


# ---------------------------------------------------------------------------
# Forward PFD — reuse constructive PartialFractionTarget / construct_pfd
# ---------------------------------------------------------------------------


def _forced_var(spec: IntegralSpec):
    from question_engine.frameworks.primitives.variables import SampledVariable

    return SampledVariable(
        name=spec.variable,
        effective_d=float(spec.d_spend),
        cost=0.0,
        locked=True,
    )


def _pfd_ctx(rng: random.Random, spec: IntegralSpec):
    from question_engine.frameworks.primitives import (
        PRIM_NUMBERS,
        PRIM_VARIABLE,
        build_context,
    )
    from question_engine.frameworks.primitives.expression_policy import (
        POLYNOMIAL_POLICY_DEFAULT,
    )

    settings = {
        "difficulty": float(spec.d_spend),
        "seed": rng.randint(0, 2_000_000_000),
        "variable": spec.variable,
        "allow_other_letters": False,
    }
    return build_context(
        settings,
        [PRIM_NUMBERS, PRIM_VARIABLE],
        policy=POLYNOMIAL_POLICY_DEFAULT,
        leaf_id="integral_partial_fractions",
        rng=rng,
    )


def _seed_pfd_target(rng: random.Random, spec: IntegralSpec, *, n_terms: int = 2):
    """Shared core with precalc ``pc_partial_fraction_decomposition``."""
    from question_engine.frameworks.primitives import partial_fractions as pf

    ctx = _pfd_ctx(rng, spec)
    allow_q = float(spec.d_spend) >= 8.0
    return pf.seed_partial_fraction_target(
        ctx,
        n_terms=max(2, min(3, n_terms)),
        d=float(spec.d_spend),
        allow_quadratic=allow_q,
    )


def _factor_latex(var: str, root: Fraction) -> str:
    if root.denominator == 1:
        return format_linear_latex(1, -int(root), variable=var)
    return rf"({var}-{frac_latex(root)})"


def _coef_ln_piece(coef: Fraction, den: str) -> str:
    """Render ``A\\ln|den|`` with clean ±1 coefficients."""
    if coef == 1:
        return rf"\ln|{den}|"
    if coef == -1:
        return rf"-\ln|{den}|"
    return rf"{frac_latex(coef)}\ln|{den}|"


def _join_signed_pieces(pieces: list[str]) -> str:
    if not pieces:
        return "0"
    out = pieces[0]
    for p in pieces[1:]:
        if p.startswith("-"):
            out += p
        else:
            out += "+" + p
    return out


def _antideriv_from_pfd_target(target, var: str, *, include_plus_c: bool) -> str:
    """∫ PF terms → ln and/or arctan (OpenStax irreducible quadratic)."""
    pieces: list[str] = []
    for t in target.terms:
        kind = getattr(t, "kind", "linear")
        if kind == "quadratic":
            a2 = Fraction(t.quad_a2)
            a = Fraction(a2).limit_denominator()
            # a = sqrt(a2) when perfect square
            a_int = int(round(float(a2) ** 0.5))
            if a_int * a_int != int(a2):
                a_int = int(a2)  # fallback leave as a2 in latex
            B, C = Fraction(t.lin_coef), Fraction(t.numerator)
            den_q = rf"{var}^{{2}}+{int(a2) if a2.denominator == 1 else frac_latex(a2)}"
            if B != 0:
                # (B/2) ln(x²+a²)
                half_b = B / 2
                if half_b == 1:
                    pieces.append(rf"\ln|{den_q}|")
                elif half_b == -1:
                    pieces.append(rf"-\ln|{den_q}|")
                else:
                    pieces.append(rf"{frac_latex(half_b)}\ln|{den_q}|")
            if C != 0:
                # (C/a) arctan(x/a)
                if a_int * a_int == int(a2) and a_int > 0:
                    coef = C / a_int
                    arg = (
                        var
                        if a_int == 1
                        else rf"\frac{{{var}}}{{{a_int}}}"
                    )
                    if coef == 1:
                        pieces.append(rf"\arctan({arg})")
                    elif coef == -1:
                        pieces.append(rf"-\arctan({arg})")
                    else:
                        pieces.append(rf"{frac_latex(coef)}\arctan({arg})")
                else:
                    pieces.append(
                        rf"{frac_latex(C)}\arctan\left(\frac{{{var}}}{{\sqrt{{{frac_latex(a2)}}}}}\right)"
                    )
        else:
            den = _factor_latex(var, Fraction(t.root))
            pieces.append(_coef_ln_piece(Fraction(t.numerator), den))
    return _plus_c(_join_signed_pieces(pieces), include=include_plus_c)


def _sample_pfd_integral(
    rng: random.Random, spec: IntegralSpec
) -> tuple[str, str, dict[str, Any]]:
    """PFD integrals driven by ``partial_fractions`` form catalog."""
    from question_engine.frameworks.primitives import partial_fractions as pf
    from question_engine.frameworks.primitives.constructive import (
        PartialFractionTerm,
        PartialFractionTarget,
    )
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        catalog_form_meta,
        implemented_forms,
        load_form_catalog,
        select_form_id,
    )

    # Multi-trick pipeline forms are sampled elsewhere; keep single-trick here.
    catalog = load_form_catalog("partial_fractions")
    pool = [
        f
        for f in implemented_forms(catalog)
        if not str(f.get("form_id", "")).startswith("u_sub_then_pfd")
    ]
    preset_ids = resolve_pfd_form_preset(spec.pfd_form_preset)
    if preset_ids:
        subset = [f for f in pool if str(f.get("form_id")) in preset_ids]
        if subset:
            pool = subset
    pool = _gated_form_pool(
        {"forms": pool, "catalog_id": catalog.get("catalog_id")},
        spec,
    ) or pool
    form = select_form_id(pool, d=float(spec.d_spend), rng=rng)
    form_id = str(form["form_id"])
    ctx = _pfd_ctx(rng, spec)
    var = spec.variable
    include = spec.include_plus_c
    meta = {
        **catalog_form_meta(form, catalog),
        "family": form_id,
        "construction": "partial_fractions.combine_pf_to_rational",
        "pfd_source": "partial_fractions.combine_pf_to_rational",
        "tricks_required": ["pfd"],
        "pfd_form_preset": spec.pfd_form_preset,
    }

    if form_id == "repeated_linear_square":
        # Hand-built: A/(x−r) + B/(x−r)²
        r = Fraction(rng.randint(-3, 3))
        A = Fraction(rng.randint(1, 4) * rng.choice([-1, 1]))
        B = Fraction(rng.randint(1, 4) * rng.choice([-1, 1]))
        # Combined: [(A)(x−r) + B] / (x−r)² = (A x + (B−A r)) / (x−r)²
        num_a = int(A)
        num_b = int(B - A * r)
        den = _factor_latex(var, r)
        num = format_linear_latex(num_a, num_b, variable=var)
        prompt = rf"\int \frac{{{num}}}{{\left({den}\right)^{{2}}}}\,d{var}"
        # ∫ A/(x−r) + B/(x−r)² = A ln|x−r| − B/(x−r)
        pieces = [_coef_ln_piece(A, den)]
        if B == 1:
            pieces.append(rf"-\frac{{1}}{{{den}}}")
        elif B == -1:
            pieces.append(rf"\frac{{1}}{{{den}}}")
        else:
            pieces.append(rf"{frac_latex(-B)}\frac{{1}}{{{den}}}")
        answer = _plus_c(_join_signed_pieces(pieces), include=include)
        meta.update(
            {
                "function_classes": ["algebraic", "log"],
                "n_terms": 2,
                "has_quadratic": False,
            }
        )
        return prompt, answer, meta

    if form_id == "irreducible_quad_arctan":
        a_int = rng.choice([1, 2, 3])
        C = Fraction(rng.randint(1, 4) * rng.choice([-1, 1]))
        target = PartialFractionTarget(
            terms=(
                PartialFractionTerm(
                    numerator=C,
                    root=Fraction(0),
                    kind="quadratic",
                    lin_coef=Fraction(0),
                    quad_a2=Fraction(a_int * a_int),
                ),
            )
        )
    elif form_id == "irreducible_quad_ln":
        a_int = rng.choice([1, 2, 3])
        Blin = Fraction(rng.randint(1, 4) * rng.choice([-1, 1]))
        target = PartialFractionTarget(
            terms=(
                PartialFractionTerm(
                    numerator=Fraction(0),
                    root=Fraction(0),
                    kind="quadratic",
                    lin_coef=Blin,
                    quad_a2=Fraction(a_int * a_int),
                ),
            )
        )
    elif form_id == "distinct_linear_3":
        target = pf.seed_partial_fraction_target(
            ctx, n_terms=3, d=float(spec.d_spend), allow_quadratic=False
        )
    elif form_id == "mixed_linear_quad":
        target = pf.seed_partial_fraction_target(
            ctx, n_terms=2, d=max(10.0, float(spec.d_spend)), allow_quadratic=True
        )
        # Ensure quadratic present
        if not any(t.kind == "quadratic" for t in target.terms):
            target = pf.seed_partial_fraction_target(
                ctx, n_terms=2, d=14.0, allow_quadratic=True
            )
    else:
        # distinct_linear_2 default
        target = pf.seed_partial_fraction_target(
            ctx, n_terms=2, d=float(spec.d_spend), allow_quadratic=False
        )
        form_id = "distinct_linear_2"
        meta["form_id"] = form_id
        meta["openstax_form"] = form_id
        meta["family"] = form_id

    surface = pf.combine_pf_to_rational(
        ctx, d=float(spec.d_spend), var=_forced_var(spec), target=target
    )
    prompt = rf"\int {surface.latex}\,d{var}"
    answer = _antideriv_from_pfd_target(target, var, include_plus_c=include)
    has_q = any(getattr(t, "kind", "linear") == "quadratic" for t in target.terms)
    classes = ["algebraic", "log"]
    if has_q:
        classes.append("invtrig")
    meta.update(
        {
            "function_classes": classes,
            "n_terms": len(target.terms),
            "pf_target": target.as_dict(),
            "has_quadratic": has_q,
            "constructive": surface.metadata,
        }
    )
    return prompt, answer, meta


# ---------------------------------------------------------------------------
# Multi-trick: genuine u_sub then PFD (rational in u · u')
# ---------------------------------------------------------------------------

MULTI_TRICK_GENERATOR = "integral_multi_trick"

_MULTI_TRICK_BANDS: dict[str, tuple[str, ...]] = {
    "easy": (
        "u_sub_then_pfd_linear",
        "u_sub_then_pfd_exp",
        "u_sub_then_pfd_trig",
    ),
    "medium": (
        "u_sub_then_pfd_exp",
        "u_sub_then_pfd_trig",
        "u_sub_then_pfd_log",
    ),
    "hard": ("u_sub_then_pfd_log",),
    "expert": ("u_sub_then_pfd_log",),
}

_MULTI_TRICK_INNER_PREFER: dict[str, tuple[str, ...]] = {
    "u_sub_then_pfd_linear": ("poly",),
    "u_sub_then_pfd_exp": ("exp",),
    "u_sub_then_pfd_trig": ("trig",),
    "u_sub_then_pfd_log": ("log",),
}


def multi_trick_forms_for_difficulty(d: float) -> tuple[str, ...]:
    """Leftover lockout of D=0 linear/exp/trig wraps; D=22 is log only."""
    if d < 8.0:
        return _MULTI_TRICK_BANDS["easy"]
    if d < 16.0:
        return _MULTI_TRICK_BANDS["medium"]
    if d < 20.0:
        return _MULTI_TRICK_BANDS["hard"]
    return _MULTI_TRICK_BANDS["expert"]


def _multi_trick_form_rows(forms: tuple[str, ...]) -> list[dict[str, Any]]:
    return [
        {
            "form_id": fid,
            "d_min": 0.0,
            "d_weight": 1.0,
            "generation_status": "implemented",
            "generator_keys": [MULTI_TRICK_GENERATOR],
        }
        for fid in forms
    ]


def _rational_latex_in_u(target, u_sym: str = "u") -> tuple[str, str]:
    """Combined rational latex in variable ``u_sym`` + antideriv in u."""
    # Build combined num/den from linear+quadratic terms symbolically as latex
    # For 2 linear terms: (A+B)u - (A r2 + B r1) / ((u-r1)(u-r2))
    linears = [t for t in target.terms if getattr(t, "kind", "linear") == "linear"]
    quads = [t for t in target.terms if getattr(t, "kind", "linear") == "quadratic"]
    if len(linears) >= 2 and not quads:
        t0, t1 = linears[0], linears[1]
        r1, r2 = Fraction(t0.root), Fraction(t1.root)
        A, B = Fraction(t0.numerator), Fraction(t1.numerator)
        num_a = A + B
        num_b = -(A * r2 + B * r1)
        if num_a.denominator == 1 and num_b.denominator == 1:
            num_l = format_linear_latex(int(num_a), int(num_b), variable=u_sym)
        else:
            num_l = (
                rf"{frac_latex(num_a)}{u_sym}+{frac_latex(num_b)}"
                if num_b >= 0
                else rf"{frac_latex(num_a)}{u_sym}{frac_latex(num_b)}"
            )
        d1 = _factor_latex(u_sym, r1)
        d2 = _factor_latex(u_sym, r2)
        rat = rf"\frac{{{num_l}}}{{({d1})({d2})}}"
        pieces = [_coef_ln_piece(A, d1), _coef_ln_piece(B, d2)]
        return rat, _join_signed_pieces(pieces)
    # Fallback: single quadratic C/(u²+a²)
    if quads:
        t = quads[0]
        a2 = int(Fraction(t.quad_a2)) if Fraction(t.quad_a2).denominator == 1 else Fraction(t.quad_a2)
        C = Fraction(t.numerator)
        B = Fraction(t.lin_coef)
        num = format_linear_latex(int(B), int(C), variable=u_sym) if B.denominator == 1 and C.denominator == 1 else rf"{frac_latex(B)}{u_sym}+{frac_latex(C)}"
        den = rf"{u_sym}^{{2}}+{a2}"
        rat = rf"\frac{{{num}}}{{{den}}}"
        # antideriv handled by _antideriv_from_pfd_target with var=u
        return rat, ""
    # One linear leftover
    t = linears[0]
    rat = rf"\frac{{{frac_latex(Fraction(t.numerator))}}}{{{_factor_latex(u_sym, Fraction(t.root))}}}"
    return rat, _coef_ln_piece(Fraction(t.numerator), _factor_latex(u_sym, Fraction(t.root)))


def _sample_pipeline_u_sub_then_pfd(
    rng: random.Random, spec: IntegralSpec
) -> tuple[str, str, dict[str, Any]]:
    """Genuine multi-trick: ∫ R(g(x)) g'(x) dx with R PFD-integrable.

    OpenStax-style wraps (not linear-in-x that collapse to plain PFD):
      - u = e^x  →  R(e^x)·e^x
      - u = sin x → R(sin x)·cos x
      - u = cos x → R(cos x)·(−sin x)  (sign absorbed)
      - u = ln x  → R(ln x)/x
      - u = ax+b (a≥2) only as D=0 leftover

    High D locks out D=0 linear/exp/trig leftovers. Same four old builders.
    """
    from question_engine.frameworks.primitives import u_substitution as usub
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        select_form_id,
    )

    var = spec.variable
    d = float(spec.d_spend)
    target = _seed_pfd_target(rng, spec, n_terms=2)
    if len(target.terms) < 1:
        return _sample_pfd_integral(rng, spec)

    forms = multi_trick_forms_for_difficulty(d)
    form = select_form_id(_multi_trick_form_rows(forms), d=d, rng=rng)
    fid = str(form.get("form_id") or forms[0])
    if fid not in forms:
        fid = forms[0]
    prefer = list(_MULTI_TRICK_INNER_PREFER.get(fid) or ("exp",))

    wrap_spec = usub.pack_u_sub_for_pfd_wrap(
        d,
        variable=var,
        coef_abs_max=spec.coef_abs_max,
    )
    inner = usub.sample_u_inner_only(wrap_spec, rng=rng, prefer=prefer)
    fam = str(inner["family"])
    u_tex = str(inner["u_latex"])
    du = str(inner["du_factor_latex"])

    rat_u, ans_u = _rational_latex_in_u(target, u_sym="u")
    # Substitute u → g(x) in the rational display
    rat_g = rat_u.replace("u", f"({u_tex})" if " " in u_tex or "^" in u_tex or "\\" in u_tex else u_tex)
    # Cleaner: rebuild with u_tex as variable name in factors
    rat_g, ans_u = _rational_latex_in_u_display(target, u_tex)

    # Integrand = R(g)·g'  (absorb leading minus on du into writing)
    if du.startswith("-"):
        # ∫ R(cos)·(−sin) → write ∫ R(cos)·sin with answer negated later... 
        # Prefer keep du explicit for teaching
        integrand = rf"{rat_g}\left({du}\right)"
    else:
        # juxtaposition: R(e^x) e^x
        if du in {rf"e^{{{var}}}", "e^{x}"} or du.startswith("e^"):
            integrand = rf"{rat_g}{du}"
        elif du.startswith(r"\frac"):
            integrand = rf"{rat_g}{du}"
        else:
            integrand = rf"{rat_g}\cdot {du}" if not du.isdigit() else rf"{du}{rat_g}"

    prompt = rf"\int {integrand}\,d{var}"

    # Antiderivative in terms of u = g(x)
    if ans_u:
        answer_body = ans_u  # already in g latex from display helper
    else:
        answer_body = _antideriv_from_pfd_target(
            target, "U", include_plus_c=False
        ).replace("U", u_tex)
        # strip +C if any
        if answer_body.endswith("+C"):
            answer_body = answer_body[:-2]
    answer = _plus_c(answer_body, include=spec.include_plus_c)

    pipeline = TrickPipeline(
        stages=(
            TrickStage(
                trick="u_sub",
                input_kind="1",
                transform="compose_transcendental_inner",
                notes=f"u={u_tex}, du factor={du}",
            ),
            TrickStage(
                trick="pfd",
                input_kind="prior",
                transform="partial_fractions.seed_partial_fraction_target",
                notes="PFD in u (ln and/or arctan)",
            ),
        )
    )
    has_q = any(getattr(t, "kind", "linear") == "quadratic" for t in target.terms)
    classes = ["algebraic", "log"] + list(inner.get("classes") or [])
    if has_q:
        classes.append("invtrig")
    return prompt, answer, {
        "function_classes": sorted(set(classes)),
        "family": fid,
        "form_id": fid,
        "openstax_form": fid,
        "generator": MULTI_TRICK_GENERATOR,
        "catalog_id": "partial_fractions",
        "n_terms": len(target.terms),
        "construction": "pipeline_shared_u_sub",
        "nest": 2,
        "pipeline": pipeline.as_dict(),
        "pfd_source": "partial_fractions.seed_partial_fraction_target",
        "pf_target": target.as_dict(),
        "has_quadratic": has_q,
        "u_latex": u_tex,
        "du_factor": du,
        "u_inner_family": fam,
        "tricks_required": ["u_sub", "pfd"],
        "u_sub_spec": inner.get("u_sub_spec"),
    }


def _rational_latex_in_u_display(target, u_tex: str) -> tuple[str, str]:
    """Rational R(u_tex) and antiderivative expressed in u_tex."""
    linears = [t for t in target.terms if getattr(t, "kind", "linear") == "linear"]
    quads = [t for t in target.terms if getattr(t, "kind", "linear") == "quadratic"]
    u = u_tex
    up = rf"\left({u}\right)" if any(c in u for c in r"\^ ") or len(u) > 1 else u

    if len(linears) >= 2 and not quads:
        t0, t1 = linears[0], linears[1]
        r1, r2 = Fraction(t0.root), Fraction(t1.root)
        A, B = Fraction(t0.numerator), Fraction(t1.numerator)
        num_a, num_b = A + B, -(A * r2 + B * r1)
        # num = num_a * u + num_b
        if num_a == 1:
            num_l = u if num_b == 0 else (
                rf"{u}+{frac_latex(num_b)}" if num_b > 0 else rf"{u}{frac_latex(num_b)}"
            )
        elif num_a == -1:
            num_l = rf"-{u}" if num_b == 0 else (
                rf"-{u}+{frac_latex(num_b)}" if num_b > 0 else rf"-{u}{frac_latex(num_b)}"
            )
        else:
            num_l = (
                rf"{frac_latex(num_a)}{up}+{frac_latex(num_b)}"
                if num_b >= 0
                else rf"{frac_latex(num_a)}{up}{frac_latex(num_b)}"
            )
        def _d(r: Fraction) -> str:
            if r == 0:
                return up if up != u else u
            if r.denominator == 1:
                rr = int(r)
                return rf"\left({u}-{rr}\right)" if rr > 0 else rf"\left({u}+{-rr}\right)"
            return rf"\left({u}-{frac_latex(r)}\right)"
        d1, d2 = _d(r1), _d(r2)
        rat = rf"\frac{{{num_l}}}{{{d1}{d2}}}"
        pieces = [
            _coef_ln_piece(A, d1.strip(r"\left").strip(r"\right") if False else d1[6:-7] if d1.startswith(r"\left(") else d1),
            _coef_ln_piece(B, d2[6:-7] if d2.startswith(r"\left(") else d2),
        ]
        # Simpler ln pieces with full \left(u-r\right)
        pieces = [_coef_ln_piece(A, d1), _coef_ln_piece(B, d2)]
        return rat, _join_signed_pieces(pieces)

    if quads:
        t = quads[0]
        a2 = Fraction(t.quad_a2)
        B, C = Fraction(t.lin_coef), Fraction(t.numerator)
        a2s = int(a2) if a2.denominator == 1 else frac_latex(a2)
        if B == 0:
            num_l = frac_latex(C)
        elif C == 0:
            num_l = rf"{frac_latex(B)}{up}" if B != 1 else up
        else:
            num_l = (
                rf"{frac_latex(B)}{up}+{frac_latex(C)}"
                if C > 0
                else rf"{frac_latex(B)}{up}{frac_latex(C)}"
            )
        den = rf"{up}^{{2}}+{a2s}"
        rat = rf"\frac{{{num_l}}}{{{den}}}"
        # Build a fake target answer via antideriv with var placeholder
        ans = _antideriv_from_pfd_target(target, "Z", include_plus_c=False)
        if ans.endswith("+C"):
            ans = ans[:-2]
        ans = ans.replace("Z", u)
        return rat, ans

    t = linears[0]
    d = (
        up
        if Fraction(t.root) == 0
        else rf"\left({u}-{frac_latex(Fraction(t.root))}\right)"
    )
    rat = rf"\frac{{{frac_latex(Fraction(t.numerator))}}}{{{d}}}"
    return rat, _coef_ln_piece(Fraction(t.numerator), d)


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------


def _run_pipeline(
    rng: random.Random,
    spec: IntegralSpec,
    pipeline: TrickPipeline,
) -> tuple[str, str, dict[str, Any]]:
    tricks = pipeline.tricks_required
    if tricks == ["u_sub", "pfd"] or (
        len(tricks) >= 2 and tricks[0] == "u_sub" and "pfd" in tricks
    ):
        return _sample_pipeline_u_sub_then_pfd(rng, spec)

    if tricks == ["u_sub", "trig_sub"] or (
        len(tricks) >= 2 and tricks[0] == "u_sub" and "trig_sub" in tricks
    ):
        return _sample_trig_sub(rng, spec, with_u_wrap=True)

    # Single-trick (or unknown multi → fall back to first)
    primary = tricks[0] if tricks else "power"
    if primary == "u_sub":
        flavor = "power"
        if spec.pack == "integral_general":
            flavs = ["power"]
            if spec.allow_trig:
                flavs.append("trig")
            if spec.allow_exp or spec.allow_log:
                flavs.append("ln_exp")
            if spec.allow_invtrig:
                flavs.append("invtrig")
            flavor = rng.choice(flavs)
        else:
            if "ln_exp" in spec.tricks_allowed or spec.pack.endswith("log_exp_sub"):
                flavor = "ln_exp"
            if "invtrig" in spec.tricks_allowed or spec.pack.endswith("invtrig_sub"):
                flavor = "invtrig"
            if spec.pack == "integral_log_exp_sub":
                flavor = "ln_exp"
            if spec.pack == "integral_invtrig_sub":
                flavor = "invtrig"
        # Never treat trig-sub leaf as plain algebraic u-sub
        if spec.pack == "integral_trig_sub" or spec.require_trig_sub:
            return _sample_trig_sub(rng, spec, with_u_wrap=False)
        if spec.pack == "integral_u_sub_definite" or (
            spec.definite and spec.pack == "integral_u_sub"
        ):
            return _sample_definite_u_sub(rng, spec)
        return _sample_u_sub_derivative_backed(rng, spec, flavor=flavor)
    if primary == "pfd":
        return _sample_pfd_integral(rng, spec)
    if primary == "trig":
        return _sample_trig(rng, spec)
    if primary == "ln_exp":
        return _sample_ln_exp(rng, spec)
    if primary == "invtrig":
        return _sample_invtrig(rng, spec)
    if primary == "parts":
        return _sample_parts(rng, spec)
    if primary == "ftc":
        if spec.pack == "integral_ftc2":
            return _sample_ftc2(rng, spec)
        return _sample_ftc(rng, spec)
    if primary == "trig_sub":
        return _sample_trig_sub(rng, spec, with_u_wrap=False)
    return _sample_power(rng, spec)


def sample_integral_expression(
    settings: dict[str, Any],
    *,
    generator_key: str | None = None,
    topic: str | None = None,
    rng: random.Random | None = None,
) -> IntegralSample:
    rng = rng or _rng(settings)
    key = generator_key or resolve_generator_key(topic) or "integral_power_rule"
    allows = resolve_integral_allows(settings, generator_key=key, topic=topic)
    d = settings_difficulty(settings, default=6.0)
    band = _band(d)

    upgrades = _integral_upgrades()
    id_gate = {
        "extra_term": True,
        "higher_degree": True,
        "use_trig": allows.get("allow_trig"),
        "use_exp_log": allows.get("allow_exp") or allows.get("allow_log"),
        "use_invtrig": allows.get("allow_invtrig"),
        "use_u_sub": allows.get("allow_substitution"),
        "use_parts": allows.get("allow_parts"),
        "use_pfd": allows.get("allow_pfd"),
        "use_trig_sub": allows.get("allow_trig_sub"),
        "pipeline_len_2": allows.get("allow_substitution") and allows.get("allow_pfd"),
        "pipeline_len_3": False,  # reserved
        "parts_twice": allows.get("allow_parts"),
        "nested_u": allows.get("allow_substitution"),
        "definite_bounds": allows.get("allow_ftc") or allows.get("definite"),
    }
    allowed_ids = {uid for uid, ok in id_gate.items() if ok}
    purchased_list, remaining_budget, _skipped = select_upgrades(
        upgrades, d, allowed_ids=allowed_ids, rng=rng
    )
    purchased = {f.id for f in purchased_list}
    if allows.get("require_substitution"):
        purchased.add("use_u_sub")
    if allows.get("require_parts"):
        purchased.add("use_parts")
    if allows.get("require_pfd"):
        purchased.add("use_pfd")
    if allows.get("require_trig_sub"):
        purchased.add("use_trig_sub")

    difficulty_costs = [
        {"source": "spec", "feature": f.id, "cost": float(f.cost)}
        for f in purchased_list
    ]
    difficulty_cost_total = float(sum(f.cost for f in purchased_list))
    difficulty_shortfall = (
        float(remaining_budget) if remaining_budget > 1e-9 else 0.0
    )

    spec = build_integral_spec(
        settings, generator_key=key, allows=allows, purchased=purchased, d=d
    )
    pipeline = plan_trick_pipeline(spec, purchased=purchased, rng=rng)
    # Force multi on multi_trick leaf
    if key == "integral_multi_trick" and pipeline.tricks_required != ["u_sub", "pfd"]:
        pipeline = TrickPipeline(
            stages=(
                TrickStage("u_sub", "1", "compose_linear_inner"),
                TrickStage("pfd", "prior", "seed_pfd_rational"),
            )
        )
    # Hard guarantee: trig-sub leaf never emits a lone u_sub pipeline
    if key == "integral_trig_substitution" and "trig_sub" not in pipeline.tricks_required:
        pipeline = TrickPipeline(
            stages=(
                TrickStage(
                    "trig_sub",
                    "1",
                    "sample_trig_sub_form",
                    notes="x=a·sinθ / a·tanθ / a·secθ",
                ),
            )
        )

    prompt, answer, extra = _run_pipeline(rng, spec, pipeline)
    # Sampler may refine tricks (e.g. drop wrap on some families)
    if isinstance(extra.get("tricks_required"), (list, tuple)) and extra["tricks_required"]:
        tricks = tuple(str(t) for t in extra["tricks_required"])
        pipeline = TrickPipeline(
            stages=tuple(
                TrickStage(
                    trick=t,
                    input_kind="1" if i == 0 else "prior",
                    transform=_default_transform(t),
                )
                for i, t in enumerate(tricks)
            )
        )
    else:
        tricks = tuple(pipeline.tricks_required)
    technique = "+".join(tricks) if len(tricks) > 1 else (tricks[0] if tricks else "power")

    snap = spec.snapshot()
    snap["tricks_required"] = list(tricks)
    snap["pipeline"] = pipeline.as_dict()
    snap["technique"] = technique
    if "family" in extra:
        snap["family"] = extra["family"]
    if "construction" in extra:
        snap["construction"] = extra["construction"]
    if "deriv_spec_snapshot" in extra:
        snap["deriv_spec_snapshot"] = extra["deriv_spec_snapshot"]
    if "pipeline" in extra:
        snap["pipeline"] = extra["pipeline"]

    effort = _effort(
        technique=technique,
        tricks=tricks,
        degree=spec.degree_max,
        coef_hi=spec.coef_abs_max,
        n_terms=int(extra.get("n_terms") or 1),
        answer=answer,
        pack=spec.pack,
        nest=int(extra.get("nest") or 0),
    )

    meta: dict[str, Any] = {
        "generator": key,
        "variable": spec.variable,
        "d_spend": d,
        "spec_snapshot": snap,
        "effort_features": effort,
        "function_classes": extra.get("function_classes") or ["algebraic"],
        "tricks_required": list(tricks),
        "pipeline": pipeline.as_dict(),
        "shape_id": extra.get("family") or technique,
        "construction": extra.get("construction") or spec.construction,
        "difficulty_costs": difficulty_costs,
        "difficulty_cost_total": difficulty_cost_total,
        "difficulty_shortfall": difficulty_shortfall,
        "wrappers_applied": [],
        "core_form_id": extra.get("form_id")
        or extra.get("openstax_form")
        or extra.get("family")
        or technique,
    }
    for k in (
        "pfd_roots",
        "pfd_nums",
        "u_linear",
        "u_latex",
        "du_factor",
        "u_inner_family",
        "u_sub_spec",
        "has_quadratic",
        "deriv_spec_snapshot",
        "pfd_source",
        "pf_target",
        "constructive",
        "trig_sub_kind",
        "trig_sub_exponent",
        "openstax_form",
        "form_id",
        "openstax_case",
        "strategy",
        "catalog_id",
        "family",
        "u_sub_form_preset",
        "parts_form_preset",
        "pfd_form_preset",
        "trig_sub_form_preset",
        "omit_du_constant",
        "numeric_tier",
        "format_tier",
    ):
        if k in extra and extra[k] is not None:
            meta[k] = extra[k]
    if extra.get("form_id") or extra.get("openstax_form") or extra.get("family"):
        fid = str(
            extra.get("form_id") or extra.get("openstax_form") or extra.get("family")
        )
        meta["form_id"] = fid
        meta["openstax_form"] = fid
        meta["shape_id"] = fid
        meta["family"] = fid
        snap["form_id"] = fid
        snap["family"] = fid
        snap["generator"] = str(extra.get("generator") or meta.get("generator") or key)
        if extra.get("catalog_id"):
            snap["catalog_id"] = extra["catalog_id"]
        if extra.get("strategy"):
            snap["strategy"] = extra["strategy"]

    return IntegralSample(
        prompt_latex=prompt,
        answer_latex=answer,
        technique=technique,
        tricks_required=tricks,
        upgrades=tuple(sorted(purchased)),
        effective_d=d,
        band=band,
        metadata=meta,
    )


def sample_integral_problem(
    topic: str,
    settings: dict[str, Any],
    *,
    generator_key: str | None = None,
) -> tuple[str, str, str | None, dict[str, Any]]:
    include_answer_key = bool(settings.get("include_answer_key", False))
    key = generator_key or resolve_generator_key(topic)
    sample = sample_integral_expression(settings, generator_key=key, topic=topic)
    label = {
        "integral_power_rule": "power rule integral",
        "integral_trigonometric": "trigonometric integral",
        "integral_log_exp": "log/exp integral",
        "integral_inverse_trig": "inverse trig integral",
        "integral_substitution": "substitution integral",
        "integral_definite_substitution": "definite substitution integral",
        "integral_trig_substitution": "trig substitution integral",
        "integral_log_exp_substitution": "log/exp substitution integral",
        "integral_invtrig_substitution": "invtrig substitution integral",
        "integration_by_parts": "integration by parts",
        "integral_partial_fractions": "partial fractions integral",
        "integral_multi_trick": "multi-trick integral",
        "integral_general": "general integral",
        "first_fundamental_theorem": "first fundamental theorem",
        "second_fundamental_theorem": "second fundamental theorem",
    }.get(key or "", "integral")
    answer = sample.answer_latex if include_answer_key else None
    return sample.prompt_latex, label, answer, sample.as_metadata()
