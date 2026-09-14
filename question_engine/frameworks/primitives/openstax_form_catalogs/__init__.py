"""Load OpenStax form catalogs used by Spec samplers.

Catalogs live under ``openstax_form_catalogs/`` next to this package.
Each catalog enumerates textbook-enumerated form cases (``form_id``) with
D gates, strategies, and mining ``example_item_ids`` when available.
"""

from __future__ import annotations

import contextvars
import json
import math
from contextlib import contextmanager
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterator

# Optional live-rater tilt. Absent / empty → D-weights only (today's behavior).
_LIVE_QUALITY_FORM_WEIGHTS: contextvars.ContextVar[dict[str, float] | None] = (
    contextvars.ContextVar("live_quality_form_weights", default=None)
)
QUALITY_WEIGHT_BETA: float = 1.0
_QUALITY_SCORE_CLIP: float = 4.0

_CATALOG_DIR = Path(__file__).resolve().parent


@lru_cache(maxsize=32)
def load_form_catalog(name: str) -> dict[str, Any]:
    """Load ``{name}.json`` (e.g. ``trig_integrals``, ``algebra1_factoring``)."""
    path = _CATALOG_DIR / f"{name}.json"
    if not path.is_file():
        raise FileNotFoundError(f"OpenStax form catalog missing: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "forms" not in data:
        raise ValueError(f"Invalid form catalog shape: {path}")
    return data


def catalog_form_meta(form: dict[str, Any], catalog: dict[str, Any]) -> dict[str, Any]:
    """Standard metadata stamp for catalog-driven samples."""
    fid = str(form.get("form_id") or "")
    meta = {
        "form_id": fid,
        "openstax_form": fid,
        "openstax_case": form.get("openstax_case"),
        "strategy": form.get("strategy"),
        "catalog_id": catalog.get("catalog_id"),
        "construction": "forward_form_catalog",
        "shape_id": fid,
        "family": fid,
    }
    if form.get("indeterminate_form"):
        meta["indeterminate_form"] = form["indeterminate_form"]
    tricks = form.get("tricks")
    if isinstance(tricks, list) and tricks:
        meta["tricks"] = [str(t) for t in tricks]
        meta["tricks_required"] = [str(t) for t in tricks]
    reqs = form.get("requires_allows")
    if isinstance(reqs, list) and reqs:
        meta["requires_allows"] = [str(k) for k in reqs]
    return meta


def implemented_forms(
    catalog: dict[str, Any],
    *,
    generator_key: str | None = None,
) -> list[dict[str, Any]]:
    """Implemented forms; optional filter by ``generator_keys`` / ``leaves``."""
    out: list[dict[str, Any]] = []
    for f in catalog.get("forms") or []:
        if not isinstance(f, dict) or f.get("generation_status") != "implemented":
            continue
        if generator_key:
            tags = f.get("generator_keys") or f.get("leaves")
            if isinstance(tags, list) and tags and generator_key not in tags:
                continue
        out.append(f)
    return out


def catalog_gaps(catalog: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        f
        for f in catalog.get("forms") or []
        if isinstance(f, dict) and f.get("generation_status") in {"stub", "deferred"}
    ]


def forms_for_leaf(
    catalog: dict[str, Any],
    leaf_id: str,
    *,
    implemented_only: bool = True,
) -> list[dict[str, Any]]:
    """Filter catalog forms tagged with ``generator_keys`` / ``leaves``.

    If no form lists the leaf, falls back to all (implemented) forms so a
    catalog-wide sampler still works for shared generators.
    """
    pool = (
        implemented_forms(catalog)
        if implemented_only
        else [f for f in (catalog.get("forms") or []) if isinstance(f, dict)]
    )
    leaf = str(leaf_id or "").strip()
    if not leaf:
        return pool
    explicit = [
        f
        for f in pool
        if leaf in (f.get("generator_keys") or f.get("leaves") or [])
    ]
    return explicit or pool


# Catalog ``tricks`` → teacher allow_* checkboxes (integrals + shared catalogs).
# ``u_sub`` is not mapped: trig identities may substitute internally without the
# substitution-pipeline checkbox. Use ``requires_allows`` for allow_substitution.
_TRICK_TO_ALLOW: dict[str, str] = {
    "trig": "allow_trig",
    "parts": "allow_parts",
    "pfd": "allow_pfd",
    "trig_sub": "allow_trig_sub",
    "invtrig": "allow_invtrig",
    "ftc": "allow_ftc",
}


def filter_forms_by_allows(
    forms: list[dict[str, Any]],
    allows: dict[str, Any] | None,
    *,
    conceptual_d: float = 0.0,
    soft_c_schedule: bool = True,
    fallback_on_empty: bool = True,
) -> list[dict[str, Any]]:
    """Hard-gate forms by checkbox allows; optionally soft-gate fancy forms by C.

    Policy:
      - ``requires_allows`` / ``requires_chain`` = hard checkbox gates (ALL keys)
      - catalog ``tricks`` mapped through ``_TRICK_TO_ALLOW`` are also hard gates
        (e.g. ``parts`` → ``allow_parts``). Multi-trick items need every mapped
        skill toggled on.
      - when ``soft_c_schedule``: at low C drop multi-skill / specialty forms even
        if checkboxes are on, so low difficulty sticks to the topic core.
      - ``fallback_on_empty``: derivatives keep the old “if nothing remains, use
        the unfiltered pool” behavior. Integral samplers pass False so a toggle
        actually excludes questions.
    """
    allows = dict(allows or {})
    d = float(conceptual_d)
    out: list[dict[str, Any]] = []
    for f in forms:
        if not isinstance(f, dict):
            continue
        req_chain = bool(f.get("requires_chain"))
        if req_chain and not (
            allows.get("allow_chain") or allows.get("require_chain")
        ):
            continue
        reqs = f.get("requires_allows") or []
        if isinstance(reqs, list) and reqs:
            if not all(bool(allows.get(str(k))) for k in reqs):
                continue
        skip_tricks = False
        for trick in f.get("tricks") or []:
            key = _TRICK_TO_ALLOW.get(str(trick))
            if key and not bool(allows.get(key)):
                skip_tricks = True
                break
        if skip_tricks:
            continue
        if soft_c_schedule and d < 4:
            if req_chain and not allows.get("require_chain"):
                continue
            strategy = str(f.get("strategy") or "")
            if strategy in {"trig_advanced", "ln_exp_mix", "general"} and d < 3:
                continue
            fid = str(f.get("form_id") or "")
            if fid in {
                "product_poly_trig",
                "product_poly_exp",
                "product_one_chain",
                "product_chain_powers",
                "product_trig_exp_chain",
                "quotient_mixed_special",
                "chain_nested",
                "chain_nested_power",
                "general_mixed",
                "ln_exp_product",
                "trig_product_chain",
                "invtrig_chained",
            }:
                continue
        out.append(f)
    if out:
        return out
    if fallback_on_empty:
        return list(forms)
    return []


@contextmanager
def live_quality_form_weights(weights: dict[str, float] | None) -> Iterator[None]:
    """Thread-safe generate-time hook. ``None`` / ``{}`` leaves catalog D-weights."""
    token = _LIVE_QUALITY_FORM_WEIGHTS.set(weights if weights else None)
    try:
        yield
    finally:
        _LIVE_QUALITY_FORM_WEIGHTS.reset(token)


def current_live_quality_form_weights() -> dict[str, float] | None:
    return _LIVE_QUALITY_FORM_WEIGHTS.get()


def select_form_id(
    forms: list[dict[str, Any]],
    *,
    d: float,
    rng,
    quality_weights: dict[str, float] | None = None,
) -> dict[str, Any]:
    """D-weighted choice among forms with ``d_min <= d`` (and optional ``d_max``).

    Prefer forms whose ``d_min`` is near the current spend so low-D leftovers
    (e.g. table ∫sin/cos) do not dominate mid/high D when richer forms unlock.
    If none match the D window, fall back to forms with lowest ``d_min``.

    Optional ``quality_weights`` (or the ``live_quality_form_weights`` context)
    multiplies each D-weight by ``exp(β · score)``. Cold start / missing model
    leaves this unset so behavior is identical to D-weights only. This tilts
    which form is sampled — it does not change difficulty accounting.
    """
    eligible = []
    for f in forms:
        d_min = float(f.get("d_min") or 0)
        d_max = f.get("d_max")
        if d < d_min:
            continue
        if d_max is not None and d > float(d_max):
            continue
        eligible.append(f)
    if not eligible:
        # Prefer easiest implemented forms rather than crashing
        eligible = sorted(forms, key=lambda x: float(x.get("d_min") or 0))[:3] or forms
    weights = [max(0.05, float(f.get("d_weight") or 1.0)) for f in eligible]
    # Soft preference for forms near current D (stronger as D rises).
    proximity = 0.06 if d < 6 else (0.10 if d < 12 else 0.14)
    weights = [
        w * (1.0 + proximity * float(f.get("d_min") or 0))
        for w, f in zip(weights, eligible)
    ]
    qw = quality_weights
    if qw is None:
        qw = current_live_quality_form_weights()
    if qw:
        tilted: list[float] = []
        for w, f in zip(weights, eligible):
            score = float(qw.get(str(f.get("form_id") or ""), 0.0))
            score = max(-_QUALITY_SCORE_CLIP, min(_QUALITY_SCORE_CLIP, score))
            tilted.append(w * math.exp(QUALITY_WEIGHT_BETA * score))
        weights = tilted
    return rng.choices(eligible, weights=weights, k=1)[0]
