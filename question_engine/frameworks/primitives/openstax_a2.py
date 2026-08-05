"""OpenStax Intermediate Algebra 2e form-catalog helpers for Algebra 2 leaves.

Selects a ``form_id`` (D-weighted) from ``openstax_form_catalogs/algebra2_*.json``
and stamps standard metadata via ``catalog_form_meta``.
"""

from __future__ import annotations

import random
from typing import Any

from question_engine.frameworks.primitives.openstax_form_catalogs import (
    catalog_form_meta,
    forms_for_leaf,
    load_form_catalog,
    select_form_id,
)

# Catalog name → default leaf filter (when caller passes leaf_id).
A2_CATALOGS = (
    "algebra2_polys",
    "algebra2_rationals",
    "algebra2_radicals",
    "algebra2_exp_log",
    "algebra2_function_ops",
)


def select_a2_form(
    catalog_name: str,
    *,
    d: float,
    rng: random.Random | None = None,
    leaf_id: str = "",
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return ``(form_entry, metadata_stamp)`` for an A2 form catalog."""
    catalog = load_form_catalog(catalog_name)
    forms = forms_for_leaf(catalog, leaf_id)
    if not forms:
        raise ValueError(f"No implemented forms in catalog {catalog_name!r} for {leaf_id!r}")
    r = rng if rng is not None else random.Random()
    form = select_form_id(forms, d=float(d), rng=r)
    return form, catalog_form_meta(form, catalog)


def a2_form_constraints(form: dict[str, Any]) -> dict[str, Any]:
    """Copy ``constraints`` dict from a form entry (never None)."""
    c = form.get("constraints")
    return dict(c) if isinstance(c, dict) else {}
