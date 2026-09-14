"""Unified generation record for knob-logging / difficulty learning.



Each record captures:

  θ_full   — resolved generation settings + budget spend + sample draws

  structural features — compact numeric/categorical hints for tabular models

  y_effort — rule-based effort label when a scorer exists for the type

  optional human rating fields (rating_1_to_5 / minutes / notes)

"""



from __future__ import annotations



from dataclasses import asdict, dataclass, field

from typing import Any





# Hints commonly emitted by primitive / framework generators.

STRUCTURAL_HINT_KEYS: tuple[str, ...] = (

    "n_ops",

    "n_terms",

    "n_parens",

    "nest_depth",

    "n_groups",

    "n_lone",

    "n_factors",

    "degree_max",

    "shape",

    "shape_id",

    "steps",

    "form",

    "mode",

    "method",

    "methods_used",

    "function_classes",

    "chain_depth",

    "derivative_order",

    "effective_d",

    "band",

    "family",

    "structure_id",

    "generator",

    "has_fn_power",

    "ops",

    "effort_features",

    "spec_snapshot",

    "spend",

    "upgrades",

    "primitive_engine",

    "expression_policy",

    "op_pool",

    "nested",

    "flipped",

    "degraded",

    "sample_log",

    # expr_skeleton debug / richness features
    "skeleton_source",
    "skeleton_pattern",
    "skeleton_kind",
    "core_form_id",
    "form_id",
    "openstax_form",
    "catalog_id",
    "strategy",
    "construction",
    "conceptual_difficulty",
    "cost_spend",
    "richness_band",
    "richness_knobs",
    "inner_kind",
    "productions",
    "shared_inner",

)



# Spec / derivative knobs that should also land in θ_full when only on Spec.

_SPEC_THETA_BOOL_KEYS: tuple[str, ...] = (

    "allow_integer_exponents",

    "allow_fractional_exponents",

    "allow_irrational_exponents",

    "allow_negative_exponents",

    "allow_rational_powers",

    "allow_quotient",

    "allow_fn_power",

    "prefer_fn_power",

    "mix_fn_classes",

    "deep_chain",

    "extra_term",

    "prefer_chained_fn",

    "prefer_special_structure",

    "require_product",

    "require_sum",

    "require_power_of_poly",

    "forbid_product",

    "forbid_quotient",

    "allow_negative_coefs",

    # Course / structured-pack allow flags when only on spec_snapshot

    "allow_trig",

    "allow_exp",

    "allow_log",

    "allow_hyperbolic",

    "allow_roots",

    "allow_invtrig",

    "allow_chain",

    "allow_product",

    "allow_implicit",

    "require_chain",

    "require_quotient",

    "require_implicit",

    # Limit / integral Spec allow flags
    "allow_rational",
    "allow_removable",
    "allow_rationalize",
    "allow_piecewise",
    "allow_essential",
    "allow_indet",
    "allow_one_sided",
    "apply_lhopital",
    "require_removable",
    "require_indet",
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



_SPEC_THETA_SCALAR_KEYS: tuple[str, ...] = (

    "degree_min",

    "degree_max",

    "term_count_min",

    "term_count_max",

    "coef_abs_max",

    "max_nesting",

    "max_factors",

    "d_spend",

    "min_special_nodes",

    "derivative_order",

    "factor_count_min",

    "factor_count_max",

    "composition_depth",

)



_SPEC_THETA_LIST_KEYS: tuple[str, ...] = (

    "allowed_ops",

    "allowed_functions",

    "irrational_exponent_set",

    "tricks_allowed",

    "tricks_required",

    "forms",

)





@dataclass

class GenerationRecord:

    """One generated item with full knob snapshot and optional effort / human labels."""



    type_id: str

    seed: int | None

    difficulty: float | None

    theta_full: dict[str, Any]

    prompt_latex: str

    prompt_text: str

    answer_latex: str

    answer_text: str

    structural_features: dict[str, Any] = field(default_factory=dict)

    y_effort: float | None = None

    y_mode: str | None = None

    effort_feats: dict[str, Any] = field(default_factory=dict)

    qa_flags: list[Any] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)

    # Human rating fields (null until hand-labeled).

    rating_1_to_5: int | None = None

    minutes: float | None = None

    notes: str | None = None



    def to_dict(self) -> dict[str, Any]:

        return asdict(self)





def structural_features_from_metadata(metadata: dict[str, Any] | None) -> dict[str, Any]:

    """Extract a compact feature dict from question metadata."""

    if not metadata:

        return {}

    out: dict[str, Any] = {}

    for key in STRUCTURAL_HINT_KEYS:

        if key in metadata and metadata[key] is not None:

            out[key] = metadata[key]

    # Nested solution / generation hints sometimes carry the same keys.

    solution = metadata.get("solution")

    if isinstance(solution, dict):

        for key in STRUCTURAL_HINT_KEYS:

            if key not in out and key in solution and solution[key] is not None:

                out[key] = solution[key]

    return out





def _merge_spec_into_theta(theta: dict[str, Any], meta: dict[str, Any]) -> None:

    """Copy resolved Spec knobs into θ so featurization sees exponent / pack flags."""

    spec = meta.get("spec_snapshot")

    if not isinstance(spec, dict):

        return

    theta.setdefault("spec_snapshot", spec)

    for key in _SPEC_THETA_BOOL_KEYS:

        if key in spec and key not in theta:

            theta[key] = bool(spec[key])

    for key in _SPEC_THETA_SCALAR_KEYS:

        if key in spec and key not in theta and spec[key] is not None:

            theta[key] = spec[key]

    for key in _SPEC_THETA_LIST_KEYS:

        if key in spec and key not in theta and spec[key] is not None:

            theta[key] = spec[key]

    if "require_function" in spec and "require_function" not in theta:

        theta["require_function"] = spec.get("require_function")

    if "variable" in spec and "variable" not in theta:

        theta["variable"] = spec.get("variable")





def _theta_full_from_question(

    settings: dict[str, Any],

    metadata: dict[str, Any] | None,

) -> dict[str, Any]:

    """Build θ_full: resolved settings plus generation internals when present."""

    meta = metadata or {}

    generation_settings = meta.get("generation_settings")

    theta: dict[str, Any] = dict(generation_settings) if isinstance(generation_settings, dict) else dict(settings)



    # Budget / primitive allocation.

    spend = meta.get("spend")

    if spend is not None:

        theta["spend"] = spend

    sample_log = meta.get("sample_log")

    if sample_log is not None:

        theta["sample_log"] = sample_log

    upgrades = meta.get("upgrades")

    if upgrades is not None:

        theta["upgrades"] = upgrades

    degraded = meta.get("degraded")

    if degraded is not None:

        theta["degraded"] = degraded

    expression_policy = meta.get("expression_policy")

    if expression_policy is not None:

        theta["expression_policy"] = expression_policy

    primitive_engine = meta.get("primitive_engine")

    if primitive_engine is not None:

        theta["primitive_engine"] = primitive_engine



    # Derivative structure signals useful for join / regenerate.

    for key in (

        "generator",

        "function_classes",

        "methods_used",

        "chain_depth",

        "shape_id",

        "family",

        "structure_id",

        "form_id",

        "openstax_form",

        "core_form_id",

        "catalog_id",

        "strategy",

        "construction",

        "effective_d",

        "band",

    "derivative_order",

    "max_lhopital_steps",

    "max_pipeline_len",

    "parts_depth",

    "nest_budget",

    "approach_abs_max",

    "bound_abs_max",

):

        if key in meta and key not in theta and meta[key] is not None:

            theta[key] = meta[key]



    _merge_spec_into_theta(theta, meta)

    return theta





def _parse_difficulty(settings: dict[str, Any], metadata: dict[str, Any] | None) -> float | None:

    meta = metadata or {}

    for source in (meta, settings, meta.get("generation_settings") or {}):

        if not isinstance(source, dict):

            continue

        raw = source.get("difficulty")

        if raw is None or str(raw).strip() == "":

            continue

        try:

            return float(raw)

        except (TypeError, ValueError):

            continue

    return None





def _parse_seed(settings: dict[str, Any], metadata: dict[str, Any] | None) -> int | None:

    meta = metadata or {}

    for source in (meta.get("generation_settings") or {}, settings, meta):

        if not isinstance(source, dict):

            continue

        raw = source.get("seed")

        if raw is None or str(raw).strip() == "":

            continue

        try:

            return int(raw)

        except (TypeError, ValueError):

            continue

    return None





def build_generation_record(

    type_id: str,

    question: Any,

    settings: dict[str, Any],

    *,

    y_effort: float | None = None,

    y_mode: str | None = None,

    effort_feats: dict[str, Any] | None = None,

    rating_1_to_5: int | None = None,

    minutes: float | None = None,

    notes: str | None = None,

) -> GenerationRecord:

    """Build a GenerationRecord from a Question (or duck-typed object) + settings."""

    metadata = getattr(question, "metadata", None) or {}

    if not isinstance(metadata, dict):

        metadata = {}



    qa_flags = metadata.get("qa_flags") or []

    if not isinstance(qa_flags, list):

        qa_flags = [qa_flags]



    return GenerationRecord(

        type_id=type_id,

        seed=_parse_seed(settings, metadata),

        difficulty=_parse_difficulty(settings, metadata),

        theta_full=_theta_full_from_question(settings, metadata),

        prompt_latex=(getattr(question, "prompt_latex", None) or "").strip(),

        prompt_text=(getattr(question, "prompt_text", None) or "").strip(),

        answer_latex=(getattr(question, "answer_latex", None) or "").strip(),

        answer_text=(

            getattr(question, "answer_text", None)

            or getattr(question, "answer_latex", None)

            or ""

        ).strip(),

        structural_features=structural_features_from_metadata(metadata),

        y_effort=y_effort,

        y_mode=y_mode,

        effort_feats=dict(effort_feats or {}),

        qa_flags=list(qa_flags),

        metadata={

            k: v

            for k, v in metadata.items()

            if k

            not in {

                "generation_settings",

                "instruction_latex",

                "spend",

                "sample_log",

                "upgrades",

                "degraded",

                "expression_policy",

                "primitive_engine",

            }

        },

        rating_1_to_5=rating_1_to_5,

        minutes=minutes,

        notes=notes,

    )


