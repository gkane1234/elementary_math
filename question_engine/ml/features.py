"""Tabular feature extraction from GenerationRecord θ_full + structural hints.



Prefer recording **all** scalar/bool generation settings and known Spec fields

over maintaining an ever-growing hand list of knobs. Nested dicts of interest

(``effort_features``, ``spec_snapshot``, ``spend``) are flattened with prefixes.

"""



from __future__ import annotations



from typing import Any



from .schema import GenerationRecord





# Still used as a soft priority / documentation of common G6 bounds; discovery

# below also pulls any other bool/numeric keys present on θ / structural.

_SCALAR_KEYS: tuple[str, ...] = (

    "difficulty",

    "coef_min",

    "coef_max",

    "num_min",

    "num_max",

    "denom_min",

    "denom_max",

    "ratio_part_min",

    "ratio_part_max",

    "unit_rate_min",

    "unit_rate_max",

    "unit_rate_multiplier_min",

    "unit_rate_multiplier_max",

    "sci_exp_min",

    "sci_exp_max",

    "sci_exp_diff_min",

    "sci_exp_diff_max",

    "mantissa_decimals",

    "decimal_places",

    "n_ops",

    "n_terms",

    "n_parens",

    "nest_depth",

    "n_groups",

    "n_lone",

    "n_factors",

    "degree_max",

    "chain_depth",

    "derivative_order",

    "effective_d",

    "power_max",

    "power_min",

    "term_count",

    "coef_abs_max",

    "degree_min",

    "term_count_min",

    "term_count_max",

    "max_nesting",

    "max_factors",

    "d_spend",

    "min_special_nodes",

)



_BOOL_KEYS: tuple[str, ...] = (

    "allow_negative",

    "allow_negatives",

    "allow_fractions",

    "allow_decimals",

    "allow_mixed",

    "require_proper",

    "require_normalization",

    "allow_negative_exponents",

    "allow_magnitude_compare",

    "integers_only",

    "exclude_zero",

    # Derivative function / method / exponent knobs

    "allow_trig",

    "allow_exp",

    "allow_log",

    "allow_hyperbolic",

    "allow_roots",

    "allow_invtrig",

    "allow_chain",

    "allow_product",

    "allow_quotient",

    "allow_implicit",

    "require_chain",

    "require_product",

    "require_quotient",

    "require_implicit",

    "allow_integer_exponents",

    "allow_fractional_exponents",

    "allow_irrational_exponents",

    "allow_rational_powers",

    "allow_fn_power",

    "prefer_fn_power",

    "mix_fn_classes",

    "deep_chain",

    "extra_term",

    "has_fn_power",

    "include_constant_term",

)



_CAT_KEYS: tuple[str, ...] = (

    "difficulty_tier",

    "expression_complexity",

    "phrase_complexity",

    "sci_write_direction",

    "sci_operation",

    "form",

    "mode",

    "method",

    "shape",

    "shape_id",

    "primitive_engine",

    "number_profile",

    "variable_lane",

    "band",

    "family",

    "structure_id",

    "generator",

    "require_function",

    "variable",

    "paren_style",

)



# Nested blobs we flatten with a prefix (or special-case for spend).

_NESTED_FEATURE_KEYS: tuple[str, ...] = ("effort_features", "spec_snapshot")



# Keys never auto-promoted as top-level features (too large / redundant).

_SKIP_AUTO_KEYS: frozenset[str] = frozenset(

    {

        "sample_log",

        "upgrades",

        "qa_flags",

        "prompt_latex",

        "prompt_text",

        "answer_latex",

        "answer_text",

        "instruction_latex",

        "generation_settings",

        "type_id",

        "seed",

        "count",

        "max_columns",

        "include_answer_key",

        "ops",  # often a list of op tokens; handled as cat join below

    }

)





def _as_float(value: Any) -> float | None:

    if value is None or isinstance(value, bool):

        return None

    if isinstance(value, (int, float)):

        if isinstance(value, float) and (value != value):  # NaN

            return None

        f = float(value)

        if f != f or f in (float("inf"), float("-inf")):

            return None

        return f

    if isinstance(value, str) and value.strip():

        low = value.strip().lower()

        # Avoid float("infinity") / float("nan") poisoning the design matrix.

        if low in {"inf", "infinity", "+inf", "-inf", "-infinity", "nan"}:

            return None

        try:

            f = float(value)

        except ValueError:

            return None

        if f != f or f in (float("inf"), float("-inf")):

            return None

        return f

    return None





def _as_bool01(value: Any) -> float | None:

    if isinstance(value, bool):

        return 1.0 if value else 0.0

    if isinstance(value, (int, float)) and value in (0, 1):

        return float(value)

    if isinstance(value, str):

        low = value.strip().lower()

        if low in {"true", "1", "yes"}:

            return 1.0

        if low in {"false", "0", "no"}:

            return 0.0

    return None





def _flatten_spend(theta: dict[str, Any], structural: dict[str, Any]) -> dict[str, float]:

    spend = theta.get("spend") or structural.get("spend") or {}

    out: dict[str, float] = {}

    if not isinstance(spend, dict):

        return out

    for key, val in spend.items():

        f = _as_float(val)

        if f is not None:

            out[f"spend_{key}"] = f

    return out





def _upgrade_count(theta: dict[str, Any], structural: dict[str, Any]) -> float:

    upgrades = theta.get("upgrades") or structural.get("upgrades") or []

    if isinstance(upgrades, (list, tuple)):

        return float(len(upgrades))

    return 0.0





def _set_feat(feats: dict[str, float | str], key: str, value: Any) -> None:

    """Assign a feature if value is bool / numeric / short categorical / str-list."""

    if value is None or key in feats:

        return

    b = _as_bool01(value)

    if b is not None and (isinstance(value, bool) or isinstance(value, str)):

        feats[key] = b

        return

    if isinstance(value, bool):

        feats[key] = 1.0 if value else 0.0

        return

    f = _as_float(value)

    if f is not None:

        feats[key] = f

        return

    if isinstance(value, (list, tuple, set, frozenset)):

        items = [str(x) for x in value if x is not None and str(x).strip() != ""]

        if not items:

            return

        # Multi-hot for short token lists (function_classes, methods_used, …).

        if all(len(x) < 40 for x in items) and len(items) <= 24:

            for item in items:

                feats[f"{key}:{item}"] = 1.0

            feats[f"n_{key}"] = float(len(items))

            return

        feats[key] = ",".join(sorted(items))

        return

    if isinstance(value, str) and value.strip():

        feats[key] = value.strip()





def _flatten_nested(

    feats: dict[str, float | str],

    prefix: str,

    blob: Any,

    *,

    depth: int = 0,

) -> None:

    if not isinstance(blob, dict) or depth > 1:

        return

    for key, val in blob.items():

        if key.startswith("_") or key in _SKIP_AUTO_KEYS:

            continue

        feat_key = f"{prefix}_{key}" if prefix else str(key)

        if isinstance(val, dict) and depth == 0:

            _flatten_nested(feats, feat_key, val, depth=depth + 1)

            continue

        _set_feat(feats, feat_key, val)





def _auto_ingest_mapping(feats: dict[str, float | str], mapping: dict[str, Any]) -> None:

    """Pull every bool/numeric/cat/list leaf from a flat mapping."""

    for key, val in mapping.items():

        if key in _SKIP_AUTO_KEYS or key in {"spend", "effort_features", "spec_snapshot"}:

            continue

        if key.startswith("_"):

            continue

        if isinstance(val, dict):

            continue

        _set_feat(feats, key, val)





def record_feature_dict(record: GenerationRecord) -> dict[str, float | str]:

    """Flatten a GenerationRecord into mixed numeric/categorical features."""

    theta = record.theta_full or {}

    structural = record.structural_features or {}

    merged: dict[str, Any] = {**theta, **structural}



    feats: dict[str, float | str] = {"type_id": record.type_id}

    if record.difficulty is not None:

        feats["difficulty"] = float(record.difficulty)



    for key in _SCALAR_KEYS:

        if key == "difficulty" and "difficulty" in feats:

            continue

        f = _as_float(merged.get(key))

        if f is not None:

            feats[key] = f



    for key in _BOOL_KEYS:

        b = _as_bool01(merged.get(key))

        if b is not None:

            feats[key] = b



    for key in _CAT_KEYS:

        val = merged.get(key)

        if val is not None and str(val).strip() != "":

            feats[key] = str(val)



    # Discovery pass: catch new allow_*/numeric knobs without updating lists.

    _auto_ingest_mapping(feats, merged)



    for nested_key in _NESTED_FEATURE_KEYS:

        blob = merged.get(nested_key)

        if blob is None and nested_key == "effort_features":

            # Prefer AST effort_features; fall back to scorer effort_feats later.

            blob = (record.metadata or {}).get("effort_features")

        prefix = "spec" if nested_key == "spec_snapshot" else "ast_ef"

        if nested_key == "effort_features":

            prefix = "ast_ef"

        _flatten_nested(feats, prefix, blob)



    feats.update(_flatten_spend(theta, structural))

    feats["n_upgrades"] = _upgrade_count(theta, structural)

    feats["n_sample_log"] = float(

        len(theta.get("sample_log") or structural.get("sample_log") or [])

        if isinstance(theta.get("sample_log") or structural.get("sample_log") or [], (list, tuple))

        else 0

    )

    # Effort-side structural signals when present in effort_feats (regex scorers).

    for key, val in (record.effort_feats or {}).items():

        if key in {"parse_fail"}:

            feats[f"ef_{key}"] = 1.0 if val else 0.0

            continue

        f = _as_float(val)

        if f is not None:

            feats[f"ef_{key}"] = f

        elif isinstance(val, bool):

            feats[f"ef_{key}"] = 1.0 if val else 0.0

        elif isinstance(val, str) and val.strip():

            feats[f"ef_{key}"] = val

        elif isinstance(val, (list, tuple)):

            _set_feat(feats, f"ef_{key}", val)

    return feats





def build_design_matrix(

    records: list[GenerationRecord],

    *,

    feature_names: list[str] | None = None,

) -> tuple[list[list[float]], list[float], list[str], list[int]]:

    """Build a dense numeric design matrix from records with effort labels.



    Categorical features are one-hot encoded jointly across the batch.

    Returns ``(X, y, feature_names, kept_indices)``.

    """

    labeled: list[tuple[int, dict[str, float | str], float]] = []

    for i, rec in enumerate(records):

        if rec.y_effort is None:

            continue

        labeled.append((i, record_feature_dict(rec), float(rec.y_effort)))



    if not labeled:

        return [], [], feature_names or [], []



    # Discover categoricals.

    cat_values: dict[str, set[str]] = {}

    numeric_keys: set[str] = set()

    for _, feats, _ in labeled:

        for key, val in feats.items():

            if key == "type_id" or isinstance(val, str):

                cat_values.setdefault(key, set()).add(str(val))

            else:

                numeric_keys.add(key)



    if feature_names is None:

        names: list[str] = sorted(numeric_keys)

        for key in sorted(cat_values):

            for level in sorted(cat_values[key]):

                names.append(f"{key}={level}")

    else:

        names = list(feature_names)



    name_index = {n: i for i, n in enumerate(names)}

    X: list[list[float]] = []

    y: list[float] = []

    kept: list[int] = []

    for idx, feats, target in labeled:

        row = [0.0] * len(names)

        for key, val in feats.items():

            if isinstance(val, str) or key == "type_id":

                col = f"{key}={val}"

                if col in name_index:

                    row[name_index[col]] = 1.0

            elif key in name_index:

                row[name_index[key]] = float(val)

        X.append(row)

        y.append(target)

        kept.append(idx)

    return X, y, names, kept


