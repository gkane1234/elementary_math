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
        "allow_trig": False,
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
        "allow_log": False,
        "allow_invtrig": False,
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
    "calc_def_int_first_fundamental_theorem_of_calculus": "first_fundamental_theorem",
    "calc_def_int_second_fundamental_theorem_of_calculus": "second_fundamental_theorem",
    "calc_def_int_substitution_with_change_of_variables": "integral_substitution",
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
        "integral_trig_sub": "trig_sub",
        "integral_log_exp_sub": "u_sub",
        "integral_invtrig_sub": "u_sub",
        "integral_parts": "parts",
        "integral_pfd": "pfd",
        "integral_multi_trick": "u_sub",
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


def _sample_power(
    rng: random.Random, spec: IntegralSpec
) -> tuple[str, str, dict[str, Any]]:
    """OpenStax power/rewrite forms driven by ``basic_power_integrals`` catalog."""
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        catalog_form_meta,
        implemented_forms,
        load_form_catalog,
        select_form_id,
    )

    var = spec.variable
    catalog = load_form_catalog("basic_power_integrals")
    form = select_form_id(implemented_forms(catalog), d=float(spec.d_spend), rng=rng)
    form_id = str(form["form_id"])
    include = spec.include_plus_c
    meta_base = catalog_form_meta(form, catalog)

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


def _sample_trig(
    rng: random.Random, spec: IntegralSpec
) -> tuple[str, str, dict[str, Any]]:
    """Forward trig integrals driven by OpenStax §3.2 form catalog.

    Selects a ``form_id`` (D-weighted) from ``openstax_form_catalogs/trig_integrals``
    and builds a closed-form integrand matching that textbook case — not a single
    bland ∫sin / ∫sin·cos template.
    """
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        implemented_forms,
        load_form_catalog,
        select_form_id,
    )

    var = spec.variable
    catalog = load_form_catalog("trig_integrals")
    form = select_form_id(implemented_forms(catalog), d=float(spec.d_spend), rng=rng)
    form_id = str(form["form_id"])
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
    }


def _sample_ln_exp(
    rng: random.Random, spec: IntegralSpec
) -> tuple[str, str, dict[str, Any]]:
    var = spec.variable
    k = rng.randint(1, max(1, min(5, spec.coef_abs_max)))
    families: list[str] = []
    if spec.allow_log:
        families.extend(["ln", "ln_linear"])
    if spec.allow_exp:
        families.extend(["exp", "exp_k", "base_a"])
    if not families:
        families = ["exp"]
    family = rng.choice(families)

    if family == "ln":
        prompt = rf"\int \frac{{1}}{{{var}}}\,d{var}"
        answer = _plus_c(rf"\ln|{var}|", include=spec.include_plus_c)
        classes = ["log"]
    elif family == "ln_linear":
        a = rng.randint(1, max(1, min(4, spec.coef_abs_max)))
        b = _coef(rng, max(2, spec.coef_abs_max))
        inner = format_linear_latex(a, b, variable=var)
        prompt = rf"\int \frac{{{a}}}{{{inner}}}\,d{var}"
        answer = _plus_c(rf"\ln|{inner}|", include=spec.include_plus_c)
        classes = ["log"]
    elif family == "base_a":
        base = rng.choice([2, 3, 5])
        prompt = rf"\int {base}^{{{var}}}\,d{var}"
        answer = _plus_c(
            rf"\frac{{{base}^{{{var}}}}}{{\ln {base}}}",
            include=spec.include_plus_c,
        )
        classes = ["exp"]
    elif family == "exp_k" or k != 1:
        prompt = rf"\int e^{{{k}{var}}}\,d{var}" if k != 1 else rf"\int e^{{{var}}}\,d{var}"
        answer = _plus_c(
            rf"\frac{{1}}{{{k}}}e^{{{k}{var}}}" if k != 1 else rf"e^{{{var}}}",
            include=spec.include_plus_c,
        )
        family = "exp_k" if k != 1 else "exp"
        classes = ["exp"]
    else:
        prompt = rf"\int e^{{{var}}}\,d{var}"
        answer = _plus_c(rf"e^{{{var}}}", include=spec.include_plus_c)
        family = "exp"
        classes = ["exp"]
    return prompt, answer, {
        "function_classes": classes,
        "family": family,
        "n_terms": 1,
    }


def _sample_invtrig(
    rng: random.Random, spec: IntegralSpec
) -> tuple[str, str, dict[str, Any]]:
    """OpenStax §5.7 invtrig table forms via ``invtrig_integrals`` catalog."""
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        catalog_form_meta,
        implemented_forms,
        load_form_catalog,
        select_form_id,
    )

    var = spec.variable
    catalog = load_form_catalog("invtrig_integrals")
    form = select_form_id(implemented_forms(catalog), d=float(spec.d_spend), rng=rng)
    form_id = str(form["form_id"])
    include = spec.include_plus_c
    meta = {
        **catalog_form_meta(form, catalog),
        "function_classes": ["invtrig"],
        "family": form_id,
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


def _sample_parts(
    rng: random.Random, spec: IntegralSpec
) -> tuple[str, str, dict[str, Any]]:
    """LIATE forms driven by ``integration_by_parts`` catalog."""
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        catalog_form_meta,
        implemented_forms,
        load_form_catalog,
        select_form_id,
    )

    var = spec.variable
    catalog = load_form_catalog("integration_by_parts")
    form = select_form_id(implemented_forms(catalog), d=float(spec.d_spend), rng=rng)
    form_id = str(form["form_id"])
    include = spec.include_plus_c
    meta = {
        **catalog_form_meta(form, catalog),
        "family": form_id,
        "n_terms": 1,
        "nest": spec.parts_depth,
    }

    if form_id == "ln_alone":
        prompt = rf"\int \ln({var})\,d{var}"
        answer = _plus_c(rf"{var}\ln({var})-{var}", include=include)
        classes = ["log"]
    elif form_id == "poly1_ln":
        prompt = rf"\int {var}\ln({var})\,d{var}"
        answer = _plus_c(
            rf"\frac{{1}}{{2}}{var}^{{2}}\ln({var})-\frac{{1}}{{4}}{var}^{{2}}",
            include=include,
        )
        classes = ["log"]
    elif form_id == "poly1_exp":
        prompt = rf"\int {var}e^{{{var}}}\,d{var}"
        answer = _plus_c(rf"e^{{{var}}}({var}-1)", include=include)
        classes = ["exp"]
    elif form_id == "poly1_sin":
        prompt = rf"\int {var}\sin({var})\,d{var}"
        answer = _plus_c(rf"-{var}\cos({var})+\sin({var})", include=include)
        classes = ["trig"]
    elif form_id == "poly1_cos":
        prompt = rf"\int {var}\cos({var})\,d{var}"
        answer = _plus_c(rf"{var}\sin({var})+\cos({var})", include=include)
        classes = ["trig"]
    elif form_id == "poly2_exp":
        prompt = rf"\int {var}^{{2}}e^{{{var}}}\,d{var}"
        answer = _plus_c(rf"e^{{{var}}}({var}^{{2}}-2{var}+2)", include=include)
        classes = ["exp"]
    elif form_id == "poly2_sin":
        prompt = rf"\int {var}^{{2}}\sin({var})\,d{var}"
        answer = _plus_c(
            rf"-{var}^{{2}}\cos({var})+2{var}\sin({var})+2\cos({var})",
            include=include,
        )
        classes = ["trig"]
    elif form_id == "cyclic_exp_sin":
        prompt = rf"\int e^{{{var}}}\sin({var})\,d{var}"
        answer = _plus_c(
            rf"\frac{{1}}{{2}}e^{{{var}}}(\sin({var})-\cos({var}))",
            include=include,
        )
        classes = ["exp", "trig"]
    elif form_id == "cyclic_exp_cos":
        prompt = rf"\int e^{{{var}}}\cos({var})\,d{var}"
        answer = _plus_c(
            rf"\frac{{1}}{{2}}e^{{{var}}}(\sin({var})+\cos({var}))",
            include=include,
        )
        classes = ["exp", "trig"]
    elif form_id == "arctan_alone":
        prompt = rf"\int \arctan({var})\,d{var}"
        answer = _plus_c(
            rf"{var}\arctan({var})-\frac{{1}}{{2}}\ln(1+{var}^{{2}})",
            include=include,
        )
        classes = ["invtrig"]
    else:
        prompt = rf"\int {var}e^{{{var}}}\,d{var}"
        answer = _plus_c(rf"e^{{{var}}}({var}-1)", include=include)
        classes = ["exp"]
        meta["form_id"] = "poly1_exp"
        meta["openstax_form"] = "poly1_exp"
        meta["family"] = "poly1_exp"
    meta["function_classes"] = classes
    meta["tricks_required"] = ["parts"]
    return prompt, answer, meta


def _sample_ftc(
    rng: random.Random, spec: IntegralSpec
) -> tuple[str, str, dict[str, Any]]:
    var = spec.variable
    a = 0
    b = rng.randint(2, max(2, min(5, spec.bound_abs_max)))
    family = rng.choice(["linear", "quad", "sqrt", "sin"])
    if family == "linear":
        prompt = rf"\int_{{{a}}}^{{{b}}} {var}\,d{var}"
        answer = frac_latex(Fraction(b * b, 2))
        classes = ["algebraic"]
    elif family == "quad":
        k = rng.randint(1, max(1, min(4, spec.coef_abs_max)))
        f = format_monomial_latex(k, variable=var, degree=2) or f"{k}{var}^{{2}}"
        prompt = rf"\int_{{{a}}}^{{{b}}} {f}\,d{var}"
        answer = frac_latex(Fraction(k * b**3, 3))
        classes = ["algebraic"]
    elif family == "sqrt":
        # ∫_0^b √x dx = (2/3) b^{3/2}; keep b a perfect square for clean key
        b = rng.choice([1, 4, 9])
        prompt = rf"\int_{{{a}}}^{{{b}}} \sqrt{{{var}}}\,d{var}"
        # (2/3) b^{3/2} = (2/3) (√b)^3 = (2/3) b √b
        root = int(b**0.5)
        answer = frac_latex(Fraction(2 * b * root, 3))
        classes = ["algebraic"]
    else:
        # ∫_0^{π/2} or simple ∫_0^π/2 cos — use numeric π/2 carefully
        prompt = rf"\int_{{0}}^{{\pi/2}} \sin({var})\,d{var}"
        answer = "1"
        classes = ["trig"]
        family = "sin"
    return prompt, answer, {
        "function_classes": classes,
        "family": family,
        "n_terms": 1,
        "definite": True,
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
    b_shift = 0
    if with_u_wrap:
        b_shift = rng.choice([-3, -2, -1, 1, 2, 3])

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
    }
    pool = implemented_forms(catalog)
    if b_shift != 0:
        pool = [f for f in pool if str(f.get("form_id")) in wrap_ok] or pool
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
        "u_linear": [1, b_shift] if b_shift != 0 else None,
        "nest": 1 if b_shift != 0 else 0,
    }


# ---------------------------------------------------------------------------
# Derivative-backed u-sub
# ---------------------------------------------------------------------------


def _sample_u_sub_derivative_backed(
    rng: random.Random, spec: IntegralSpec, *, flavor: str = "power"
) -> tuple[str, str, dict[str, Any]]:
    """Catalog-driven u-sub; falls back to shared sampler for unmatched forms."""
    from question_engine.frameworks.primitives import u_substitution as usub
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        catalog_form_meta,
        implemented_forms,
        load_form_catalog,
        select_form_id,
    )

    var = spec.variable
    include = spec.include_plus_c
    catalog = load_form_catalog("u_substitution")
    # Flavor packs bias which forms are eligible
    flavor_allow = {
        "power": {
            "power_linear_du",
            "power_quad_x_du",
            "root_quad_x_du",
            "du_over_u_linear",
            "alteration_linear_over_root",
        },
        "ln_exp": {
            "exp_of_trig",
            "exp_of_poly",
            "du_over_u_linear",
            "ln_squared_chain",
            "nested_trig_exp",
            "du_over_u_trig",
        },
        "trig": {
            "du_over_u_trig",
            "trig_of_linear",
            "sec2_of_u",
            "exp_of_trig",
            "nested_trig_exp",
        },
        "invtrig": {"arctan_of_linear", "du_over_u_linear", "power_linear_du"},
    }
    allow = flavor_allow.get(flavor) or None
    pool = implemented_forms(catalog)
    if allow:
        filtered = [f for f in pool if str(f.get("form_id")) in allow]
        if filtered:
            pool = filtered
    form = select_form_id(pool, d=float(spec.d_spend), rng=rng)
    form_id = str(form["form_id"])
    meta = {
        **catalog_form_meta(form, catalog),
        "n_terms": 1,
        "tricks_required": ["u_sub"],
        "family": form_id,
    }

    a = rng.randint(2, max(2, min(4, spec.coef_abs_max)))
    b = _coef(rng, max(2, spec.coef_abs_max), exclude_zero=False)
    n = rng.randint(2, max(2, min(5, spec.degree_max)))
    c = rng.randint(1, max(1, spec.coef_abs_max))

    if form_id == "power_linear_du":
        inner = format_linear_latex(a, b, variable=var)
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
      - u = ax+b (a≥2) only as low-D fallback
    """
    from question_engine.frameworks.primitives import u_substitution as usub

    var = spec.variable
    target = _seed_pfd_target(rng, spec, n_terms=2)
    if len(target.terms) < 1:
        return _sample_pfd_integral(rng, spec)

    wrap_spec = usub.pack_u_sub_for_pfd_wrap(
        float(spec.d_spend),
        variable=var,
        coef_abs_max=spec.coef_abs_max,
    )
    # Prefer transcendental inners so PFD-in-x is impossible
    prefer = ["exp", "trig", "log"] if spec.d_spend >= 6 else ["exp", "trig", "poly"]
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
    if fam.startswith("exp"):
        fid = "u_sub_then_pfd_exp"
    elif fam.startswith("trig") or fam.startswith("log"):
        fid = "u_sub_then_pfd_trig" if fam.startswith("trig") else "u_sub_then_pfd_log"
    else:
        fid = "u_sub_then_pfd_exp"
    return prompt, answer, {
        "function_classes": sorted(set(classes)),
        "family": f"u_sub_then_pfd__{fam}",
        "form_id": fid,
        "openstax_form": fid,
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
    purchased_list, _, _ = select_upgrades(
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
        "integral_trig_substitution": "trig substitution integral",
        "integral_log_exp_substitution": "log/exp substitution integral",
        "integral_invtrig_substitution": "invtrig substitution integral",
        "integration_by_parts": "integration by parts",
        "integral_partial_fractions": "partial fractions integral",
        "integral_multi_trick": "multi-trick integral",
        "first_fundamental_theorem": "first fundamental theorem",
        "second_fundamental_theorem": "second fundamental theorem",
    }.get(key or "", "integral")
    answer = sample.answer_latex if include_answer_key else None
    return sample.prompt_latex, label, answer, sample.as_metadata()
