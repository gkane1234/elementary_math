"""ML-ready structured-pack metadata for algebraic (non-calc) generators.

Mirrors the calc ``_madlibs_meta`` / Spec snapshot pattern so A1/A2/PC rows
emit ``spec_snapshot``, ``function_classes``, ``methods_used``, ``structure_id``,
and ``effort_features`` for export / hand-rating join keys — even when the
underlying sampler is a constructive/primitive engine rather than
``ExpressionSpec``.
"""

from __future__ import annotations

from typing import Any


def enrich_algebraic_meta(
    base: dict[str, Any] | None,
    *,
    pack: str,
    generator: str,
    family: str | None = None,
    function_classes: list[str] | tuple[str, ...] | None = None,
    methods_used: list[str] | tuple[str, ...] | None = None,
    knobs: dict[str, Any] | None = None,
    answer: str | None = None,
    course_tag: str = "",
    shape_id: str | None = None,
    nest_depth: int | None = None,
    degree_max: int | None = None,
    n_terms: int | None = None,
    n_factors: int | None = None,
) -> dict[str, Any]:
    """Merge ML join fields onto an existing question metadata dict.

    Existing keys in ``base`` win for non-ML fields; ML fields are filled when
    missing or always refreshed for ``spec_snapshot`` / ``effort_features``.
    """
    meta: dict[str, Any] = dict(base or {})
    # Prefer OpenStax form_id as the stable family/shape when present.
    fid = str(meta.get("form_id") or meta.get("openstax_form") or "")
    fam = family or fid or str(meta.get("method") or meta.get("pattern") or pack)
    classes = list(function_classes or meta.get("function_classes") or ["algebraic"])
    methods = list(methods_used or meta.get("methods_used") or ["algebraic"])
    structure_id = str(meta.get("structure_id") or f"{generator}:{fam}")
    depth = int(
        nest_depth
        if nest_depth is not None
        else meta.get("nest_depth")
        or meta.get("chain_depth")
        or 0
    )
    deg = int(
        degree_max
        if degree_max is not None
        else meta.get("degree")
        or meta.get("poly_degree")
        or meta.get("max_degree")
        or meta.get("degree_max")
        or 0
    )
    terms = int(
        n_terms
        if n_terms is not None
        else meta.get("n_terms")
        or meta.get("n_hot_terms")
        or 0
    )
    factors = int(
        n_factors
        if n_factors is not None
        else meta.get("n_factors")
        or meta.get("left_terms")
        or 0
    )

    snap: dict[str, Any] = {
        "pack": pack,
        "family": fam,
        "generator": generator,
        "course_tag": course_tag or str(meta.get("course_tag") or ""),
        "function_classes": classes,
        "methods_used": methods,
        "degree_max": deg,
        "n_terms": terms,
        "n_factors": factors,
        "nest_depth": depth,
    }
    # Promote resolved knobs / allow_* / scalar θ into the snapshot.
    for src in (knobs or {}, meta.get("target_constraints") or {}, meta):
        if not isinstance(src, dict):
            continue
        for key, val in src.items():
            if key.startswith("_"):
                continue
            if key in snap and snap[key] not in (None, "", [], 0):
                continue
            if isinstance(val, (bool, int, float, str)) or val is None:
                if key.startswith("allow_") or key.startswith("require_") or key in {
                    "coef_abs_max",
                    "coef_min",
                    "coef_max",
                    "degree_min",
                    "degree_max",
                    "max_degree",
                    "min_degree",
                    "max_terms",
                    "exact_terms",
                    "term_count",
                    "term_count_min",
                    "term_count_max",
                    "cancel_factor_count",
                    "factor_count_min",
                    "factor_count_max",
                    "pfd_term_count",
                    "pfd_coef_abs_max",
                    "pfd_root_abs_max",
                    "max_nesting",
                    "max_factors",
                    "prefer_single_hot",
                    "integers_only",
                    "d_spend",
                    "effective_d",
                    "op",
                    "pattern",
                    "method",
                    "level",
                    "composition_depth",
                    "n_terms",
                }:
                    snap[key] = val
            elif isinstance(val, (list, tuple)) and key in {
                "allowed_ops",
                "allowed_functions",
                "inflators",
                "upgrades",
            }:
                snap[key] = list(val)

    # Prefer explicit effective_d / difficulty when present.
    if "effective_d" not in snap and meta.get("effective_d") is not None:
        snap["effective_d"] = meta["effective_d"]
    if "d_spend" not in snap and meta.get("difficulty") is not None:
        try:
            snap["d_spend"] = float(meta["difficulty"])
        except (TypeError, ValueError):
            pass

    ans = answer or ""
    effort = {
        "answer_len": len(ans),
        "nest_depth": depth,
        "n_terms": terms,
        "n_factors": factors,
        "degree_max": deg,
        "methods": methods,
        "pack": pack,
        "family": fam,
        "cancel_factor_count": int(meta.get("cancel_factor_count") or 0),
    }
    # Preserve richer AST effort features if a Spec path already filled them.
    existing_ef = meta.get("effort_features")
    if isinstance(existing_ef, dict):
        merged_ef = dict(effort)
        merged_ef.update(existing_ef)
        effort = merged_ef

    meta["generator"] = meta.get("generator") or generator
    meta["family"] = fam
    meta["structure_id"] = structure_id
    meta["shape_id"] = shape_id or str(meta.get("shape_id") or fam)
    meta["function_classes"] = classes
    meta["methods_used"] = methods
    meta["nest_depth"] = depth
    if deg:
        meta.setdefault("degree_max", deg)
    if terms:
        meta.setdefault("n_terms", terms)
    meta["spec_snapshot"] = snap
    meta["effort_features"] = effort
    if course_tag:
        meta["course_tag"] = course_tag
    return meta


def algebraic_metadata_builder(
    last: dict[str, Any],
    *,
    pack: str,
    generator: str,
    family: str | None = None,
    function_classes: list[str] | tuple[str, ...] | None = None,
    methods_used: list[str] | tuple[str, ...] | None = None,
    knobs: dict[str, Any] | None = None,
    course_tag: str = "",
):
    """``make_questions`` metadata_builder that stamps algebraic ML fields."""

    def metadata_builder(_p: str, _t: str, answer: str | None) -> dict[str, Any]:
        return enrich_algebraic_meta(
            last.get("meta"),
            pack=pack,
            generator=generator,
            family=family,
            function_classes=function_classes,
            methods_used=methods_used,
            knobs=knobs,
            answer=answer,
            course_tag=course_tag,
        )

    return metadata_builder
