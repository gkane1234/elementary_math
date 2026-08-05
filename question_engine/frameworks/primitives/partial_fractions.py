"""Shared partial-fraction API for A2/PC (and future calc integrals).

Relationship to rational add/subtract
-------------------------------------
``construct_pfd`` (L4) **seeds** Σ Aᵢ/(x−rᵢ) as the answer, then **combines**
over an LCD to a single rational prompt — the pedagogical reverse of
``construct_rational_sum(..., as_sum=True)`` (L3), which seeds summands and
asks students to combine.

Both live on the constructive spine today (``constructive.py``). This module
is the **stable import surface** so calc integral PFD can migrate later without
forking a third implementation.

Inheritance
-----------
- **Core:** ``construct_pfd`` / ``seed_partial_fraction_target`` in
  ``constructive.py`` (PFD ← constructive partials).
- **PC leaf:** ``pc_partial_fraction_decomposition`` wraps this module.
- **A2:** rational add/simplify only today; a future A2 PFD leaf should wrap
  ``construct_pfd`` here — do not invent a new core.
- **Future reverse-of-add:** L3 ``construct_rational_sum(as_sum=True)`` and L4
  PFD already share LCD combine; a true bidirectional adapter can come later.
- **Calc integrals:** ``integrals._sample_pfd_forward`` wraps
  ``combine_pf_to_rational`` / ``PartialFractionTarget`` with ∫ framing and
  ln antiderivatives; multi-trick ``u_sub→pfd`` seeds the same target then
  composes a linear inner. Future: reverse-of-rational-add unify;
  quadratic / repeated factors later.
"""

from __future__ import annotations

from typing import Any

from question_engine.frameworks.primitives.constructive import (
    PartialFractionTarget,
    PartialFractionTerm,
    SurfaceExpression,
    construct_pfd,
    seed_partial_fraction_target,
    verify_pfd_combine,
)
from question_engine.frameworks.primitives.registry import PrimitiveContext
from question_engine.frameworks.primitives.variables import SampledVariable

__all__ = [
    "PartialFractionTarget",
    "PartialFractionTerm",
    "apply_pfd_continuous_knobs",
    "combine_pf_to_rational",
    "construct_pfd",
    "pfd_term_count_from_d",
    "seed_partial_fraction_target",
    "verify_pfd_combine",
]


def pfd_term_count_from_d(d: float) -> int:
    """Continuous-D → number of linear PF terms (2–4)."""
    d = max(0.0, float(d))
    if d < 8.0:
        return 2
    if d < 14.0:
        return 3
    return 4


def apply_pfd_continuous_knobs(settings: dict[str, Any]) -> dict[str, Any]:
    """Map continuous D → PFD structure knobs (term count, coef spans).

    Explicit settings win. Fills ``pfd_term_count`` / ``n_terms`` when missing
    so generators and ML snapshots see resolved θ.
    """
    from question_engine.frameworks.difficulty_budget import settings_difficulty

    out = dict(settings)
    d = float(settings_difficulty(out))
    out.setdefault("difficulty", d)
    if out.get("pfd_term_count") is None and out.get("n_terms") is None:
        n = pfd_term_count_from_d(d)
        out["pfd_term_count"] = n
        out["n_terms"] = n
    else:
        n = int(out.get("pfd_term_count") or out.get("n_terms") or 2)
        n = max(2, min(4, n))
        out["pfd_term_count"] = n
        out["n_terms"] = n
    # Coef / root spans for future adapters (constructive seed uses number lanes).
    if d < 4.0:
        out.setdefault("pfd_coef_abs_max", 3)
        out.setdefault("pfd_root_abs_max", 3)
    elif d < 10.0:
        out.setdefault("pfd_coef_abs_max", 5)
        out.setdefault("pfd_root_abs_max", 5)
    else:
        out.setdefault("pfd_coef_abs_max", min(9, 5 + int((d - 10) // 4)))
        out.setdefault("pfd_root_abs_max", min(8, 5 + int((d - 10) // 5)))
    out.setdefault("allow_repeated_factors", False)  # reserved; spine is simple linears
    # Mid+ D: irreducible x²+a² → arctan after ∫ (OpenStax Calc 2 PFD)
    if d >= 8.0:
        out.setdefault("allow_quadratic_irreducible", True)
    else:
        out.setdefault("allow_quadratic_irreducible", False)
    return out


def combine_pf_to_rational(
    ctx: PrimitiveContext,
    *,
    d: float | None = None,
    var: SampledVariable | None = None,
    target: PartialFractionTarget | None = None,
    n_terms: int | None = None,
    allow_quadratic: bool | None = None,
) -> SurfaceExpression:
    """Adapter: seed PF (optional) → combined rational surface (L4 PFD).

    Prefer this name from new callers; implementation delegates to
    ``construct_pfd`` so A2/PC and future calc share one core.
    """
    eff = float(d if d is not None else max(ctx.topic_d, 0.0))
    tgt = target
    if tgt is None:
        tgt = seed_partial_fraction_target(
            ctx,
            n_terms=n_terms,
            d=eff,
            allow_quadratic=allow_quadratic,
        )
    return construct_pfd(ctx, d=eff, var=var, target=tgt)
