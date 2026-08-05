"""OpenStax Precalculus 2e form-catalog helpers for PC algebraic leaves.

Selects a ``form_id`` (D-weighted) from ``openstax_form_catalogs/precalculus_*.json``
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

PC_CATALOGS = (
    "precalculus_function_ops",
    "precalculus_exp_log",
    "precalculus_trig_identities",
    "precalculus_trig_equations",
    "precalculus_partial_fractions",
)


def select_pc_form(
    catalog_name: str,
    *,
    d: float,
    rng: random.Random | None = None,
    leaf_id: str = "",
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Return ``(form_entry, metadata_stamp)`` for a Precalculus form catalog."""
    catalog = load_form_catalog(catalog_name)
    forms = forms_for_leaf(catalog, leaf_id)
    if not forms:
        raise ValueError(f"No implemented forms in catalog {catalog_name!r} for {leaf_id!r}")
    r = rng if rng is not None else random.Random()
    form = select_form_id(forms, d=float(d), rng=r)
    return form, catalog_form_meta(form, catalog)


def pc_form_constraints(form: dict[str, Any]) -> dict[str, Any]:
    """Copy ``constraints`` dict from a form entry (never None)."""
    c = form.get("constraints")
    return dict(c) if isinstance(c, dict) else {}


def is_pc_leaf(topic: str) -> bool:
    return str(topic or "").startswith("pc_")
