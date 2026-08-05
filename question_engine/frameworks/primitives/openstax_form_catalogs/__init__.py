"""Load OpenStax form catalogs used by Spec samplers.

Catalogs live under ``openstax_form_catalogs/`` next to this package.
Each catalog enumerates textbook-enumerated form cases (``form_id``) with
D gates, strategies, and mining ``example_item_ids`` when available.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

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


def select_form_id(
    forms: list[dict[str, Any]],
    *,
    d: float,
    rng,
) -> dict[str, Any]:
    """D-weighted choice among forms with ``d_min <= d`` (and optional ``d_max``).

    Prefer forms whose ``d_min`` is near the current spend so low-D leftovers
    (e.g. table ∫sin/cos) do not dominate mid/high D when richer forms unlock.
    If none match the D window, fall back to forms with lowest ``d_min``.
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
    return rng.choices(eligible, weights=weights, k=1)[0]
