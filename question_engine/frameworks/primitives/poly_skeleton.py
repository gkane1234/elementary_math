"""Polynomial FactorProduct skeleton — goal-first factor inventory.

Species
-------
- **FactorProduct** — sample factors via ``factor_sampler``, surface as an
  expanded poly (factor) or factored product (multiply); answer is the other
  form.

Pipeline
--------
1. Map catalog ``form_id`` / leaf → knobs (kind, n_factors, monic, GCF, deg cap).
2. Sample inventory with ``sample_factor_product`` (same sampler as rationals).
3. Package prompt/answer from ``dens_style`` + ``task``.
4. Stamp ``skeleton_pattern=FactorProduct``.

Rational-lane caps (k≤2, deg D≤2) stay in ``rational_skeleton``. This module
may raise ``max_product_degree`` for A2 grouping (3), cubes (3), quadratic form
(4), or 3-linear products — real factor structure, not a cost pad.

Opt-out (legacy ``factor_poly`` / ``polynomials`` samplers):
``use_factor_poly=True``, ``use_factor_product_skeleton=False``, or
``skeleton_pattern`` in {factor_poly, constructive, hand}.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Literal

from question_engine.frameworks.primitives.factor_sampler import (
    DEFAULT_MAX_PRODUCT_DEGREE,
    FactorConstraints,
    FactorDraw,
    FactorKind,
    PolyFactor,
    constraints_from_settings,
    render_factor_product,
    sample_factor_product,
)
from question_engine.frameworks.primitives.poly_helpers import (
    combine_coeff_maps,
    poly_degree,
    render_poly,
    sample_poly_coeffs,
    scale_coeffs,
)
from question_engine.frameworks.primitives.registry import PrimitiveContext

Task = Literal["factor", "multiply"]

# form_id → skeleton knobs (forms, not technique-pack forks).
_FORM_KNOBS: dict[str, dict[str, Any]] = {
    "trinomial_x2_bx_c": {
        "kind": "linear",
        "n_factors": 2,
        "allow_nonmonic": False,
        "task": "factor",
        "dens_style": "expanded",
        "max_product_degree": 2,
    },
    "trinomial_ax2_bx_c": {
        "kind": "linear",
        "n_factors": 2,
        "allow_nonmonic": True,
        "task": "factor",
        "dens_style": "expanded",
        "max_product_degree": 2,
    },
    "trinomial_a_gt_1": {
        "kind": "linear",
        "n_factors": 2,
        "allow_nonmonic": True,
        "task": "factor",
        "dens_style": "expanded",
        "max_product_degree": 2,
    },
    "trinomial_ax2_bx_c": {
        "kind": "linear",
        "n_factors": 2,
        "allow_nonmonic": True,
        "task": "factor",
        "dens_style": "expanded",
        "max_product_degree": 2,
    },
    "difference_of_squares": {
        "kind": "diff_squares",
        "task": "factor",
        "dens_style": "expanded",
        "max_product_degree": 2,
    },
    "perfect_square_trinomial": {
        "kind": "perfect_square",
        "task": "factor",
        "dens_style": "expanded",
        "max_product_degree": 2,
    },
    "factor_by_grouping": {
        "kind": "grouping",
        "task": "factor",
        "dens_style": "expanded",
        "max_product_degree": 3,
    },
    "sum_diff_cubes": {
        "kind": "cubes",
        "task": "factor",
        "dens_style": "expanded",
        "max_product_degree": 3,
    },
    "quadratic_form": {
        "kind": "quadratic_form",
        "task": "factor",
        "dens_style": "expanded",
        "max_product_degree": 4,
    },
    "gcf_then_pattern": {
        "kind": "linear",
        "n_factors": 2,
        "require_gcf": True,
        "task": "factor",
        "dens_style": "expanded",
        "max_product_degree": 2,
    },
    "gcf_monomial": {"kind": "gcf_monomial", "task": "factor"},
    "gcf_factor": {"kind": "gcf_monomial", "task": "factor"},
    "quadratic_equation_factor": {
        "kind": "linear",
        "n_factors": 2,
        "allow_nonmonic": False,
        "task": "factor",
        "dens_style": "expanded",
        "max_product_degree": 2,
        "package": "equation",
    },
    "binomial_times_binomial": {
        "kind": "linear",
        "n_factors": 2,
        "task": "multiply",
        "dens_style": "factored",
        "max_product_degree": 2,
    },
    "mono_times_poly": {
        "kind": "mono_poly",
        "task": "multiply",
        "dens_style": "factored",
        "max_product_degree": 3,
    },
    "poly_times_poly": {
        "kind": "linear",
        "n_factors": 3,
        "task": "multiply",
        "dens_style": "factored",
        "max_product_degree": 3,
    },
    "special_product_square": {
        "kind": "perfect_square",
        "task": "multiply",
        "dens_style": "factored",
        "max_product_degree": 2,
    },
    "special_product_diff_squares": {
        "kind": "diff_squares",
        "task": "multiply",
        "dens_style": "factored",
        "max_product_degree": 2,
    },
}

_EQUATION_LEAF_KEYS = (
    "quadratic_factoring_equations",
    "solving_equations_by_factoring",
    "solving_polynomial_equations",
)


def _is_equation_leaf(leaf_id: str) -> bool:
    leaf = str(leaf_id or "")
    return any(key in leaf for key in _EQUATION_LEAF_KEYS)


def _is_grouping_leaf(leaf_id: str) -> bool:
    leaf = str(leaf_id or "")
    return "grouping" in leaf


def _quadratic_factoring_knobs() -> dict[str, Any]:
    from question_engine.frameworks.primitives.difficulty_knobs import section

    return section("quadratic_factoring") or {}


def _equation_knobs_for_d(d: float, rng) -> dict[str, Any]:
    """Solve-by-factoring knobs — same families as ``factor_poly._quadratic``.

    Old path (``sample_quadratic_equation_by_factoring``): always degree-2
    ``(px+q)(rx+s)=0``. D<8 monic; D≥ ``nonmonic_from_d`` (8) forces a≠1
    (ac method); D> ``unsimplify_from_d`` (10) dresses the expanded stem;
    D≥ ``gcf_from_d`` (12) may add an outer GCF. Never grouping / cubes /
    quadratic form — those are other leaves.
    """
    kn = dict(_FORM_KNOBS["quadratic_equation_factor"])
    qk = _quadratic_factoring_knobs()
    nonmonic_from = float(qk.get("nonmonic_from_d", 8.0))
    const_hi_easy = int(qk.get("const_hi_easy", 4))
    const_hi_mid = int(qk.get("const_hi_mid", 6))
    const_hi_hard = int(qk.get("const_hi_hard", 9))
    d = max(0.0, float(d))
    if d < nonmonic_from:
        kn["allow_nonmonic"] = False
        kn["nonmonic_weight"] = 0.0
        if d < 3.0:
            kn["const_min"] = 1
            kn["const_max"] = const_hi_easy
        elif d < 6.0:
            kn["const_min"] = -const_hi_easy
            kn["const_max"] = const_hi_easy
        else:
            kn["const_min"] = -const_hi_mid
            kn["const_max"] = const_hi_mid
    else:
        kn["allow_nonmonic"] = True
        kn["nonmonic_weight"] = 1.0
        kn["leading_min"] = 1
        kn["leading_max"] = 3
        kn["const_min"] = -const_hi_hard
        kn["const_max"] = const_hi_hard
        # Old path multiplies unreduced (px+q)(rx+s); reducing contents
        # would turn (2x-4) into (x-2) and drop a≠1 from the stem.
        kn["content_primitive"] = False
    gcf_from = float(qk.get("gcf_from_d", 12.0))
    gcf_chance = float(qk.get("gcf_chance", 0.3))
    if d >= gcf_from and rng.random() < gcf_chance:
        kn["require_gcf"] = True
    return kn


@dataclass(frozen=True)
class FactorProductResult:
    prompt_latex: str
    prompt_text: str
    answer_latex: str
    answer_text: str
    task: Task
    method: str
    degree: int
    form_id: str | None
    dens_style: str
    factor_kind: str
    outer_gcf: Fraction
    poly_coeffs: dict[int, Fraction]
    factor_coeffs: tuple[dict[int, Fraction], ...]
    upgrades: tuple[str, ...]
    effective_d: float
    metadata: dict[str, Any]

    def debug_dict(self) -> dict[str, Any]:
        return {
            "pattern": "FactorProduct",
            "task": self.task,
            "method": self.method,
            "degree": self.degree,
            "form_id": self.form_id,
            "factor_kind": self.factor_kind,
            "dens_style": self.dens_style,
            **self.metadata,
        }


def _present_expanded_for_factor(
    ctx: PrimitiveContext,
    product: dict[int, Fraction],
    var,
    *,
    d: float,
    unsimplify_from_d: float | None = None,
) -> tuple[str, str, tuple[str, ...]]:
    """Render expanded poly; optionally unsimplify.

    Default: format_tier ≥ 3 (D≥22). Equation packaging passes the old
    ``factor_poly`` gate (``unsimplify_from_d``, default 10).
    """
    from question_engine.frameworks.primitives.skeleton_difficulty import (
        skeleton_format_tier,
    )

    plain_l, plain_t = render_poly(product, var, descending=True)
    if unsimplify_from_d is not None:
        gate = float(unsimplify_from_d)
        if d <= gate:
            return plain_l, plain_t, ()
        inflate_d = max(1.0, d - gate)
    elif skeleton_format_tier(d) < 3:
        return plain_l, plain_t, ()
    else:
        inflate_d = max(1.0, d - 20.0)

    from question_engine.frameworks.primitives.constructive import (
        ExpressionScope,
        PolynomialTarget,
        construct_poly,
        verify_poly,
    )

    min_inflators = 1 + int(inflate_d // 8)
    for _ in range(8):
        surface = construct_poly(
            ctx,
            d=inflate_d,
            var=var,
            target=PolynomialTarget.from_dict(dict(product), single_hot=False),
            scope=ExpressionScope(max_degree=max(2, poly_degree(product))),
            prefer_distribute=True,
            min_inflators=min_inflators,
        )
        if verify_poly(surface, surface.target):
            tags = (
                "unsimplified",
                *tuple(
                    t
                    for t in surface.inflators_applied
                    if str(t).startswith("compose:")
                )[:4],
            )
            return surface.latex, surface.text, tags
    return plain_l, plain_t, ()


def _multiply_knobs_for_d(knobs: dict[str, Any], d: float, rng) -> dict[str, Any]:
    """At high format tier, unlock richer multiply shapes (deterministic)."""
    from question_engine.frameworks.primitives.skeleton_difficulty import (
        skeleton_format_tier,
    )

    if knobs.get("task") != "multiply":
        return knobs
    ft = skeleton_format_tier(d)
    if ft >= 3:
        return dict(_FORM_KNOBS["poly_times_poly"])
    if ft >= 2:
        return dict(_FORM_KNOBS["mono_times_poly"])
    return knobs


def knobs_from_form_id(form_id: str | None) -> dict[str, Any] | None:
    fid = str(form_id or "").strip()
    if not fid:
        return None
    kn = _FORM_KNOBS.get(fid)
    return dict(kn) if kn else None


def knobs_from_form(form: dict[str, Any] | None) -> dict[str, Any] | None:
    if not isinstance(form, dict):
        return None
    kn = knobs_from_form_id(str(form.get("form_id") or ""))
    if kn:
        return kn
    cons = form.get("constraints") if isinstance(form.get("constraints"), dict) else {}
    kind = str(cons.get("kind") or cons.get("pattern") or "").lower()
    leading = str(cons.get("leading") or "")
    if cons.get("a_gt_1") or leading == "nonmonic":
        return dict(_FORM_KNOBS["trinomial_ax2_bx_c"])
    if leading == "monic" or kind == "trinomial":
        return dict(_FORM_KNOBS["trinomial_x2_bx_c"])
    if kind in {"equation"} or str(cons.get("strategy") or "") == "zero_product":
        return dict(_FORM_KNOBS["quadratic_equation_factor"])
    if kind in {"gcf_monomial", "gcf"}:
        return dict(_FORM_KNOBS["gcf_monomial"])
    if kind in {"grouping"}:
        return dict(_FORM_KNOBS["factor_by_grouping"])
    if kind in {"cubes"} or str(cons.get("pattern")) == "cubes":
        return dict(_FORM_KNOBS["sum_diff_cubes"])
    if str(cons.get("pattern")) in {"diff_squares"}:
        return dict(_FORM_KNOBS["difference_of_squares"])
    if str(cons.get("pattern")) in {"perfect_square", "square_binom"}:
        return dict(_FORM_KNOBS["perfect_square_trinomial"])
    if str(cons.get("pattern")) in {"binom_binom"}:
        return dict(_FORM_KNOBS["binomial_times_binomial"])
    if str(cons.get("pattern")) in {"mono_poly"}:
        return dict(_FORM_KNOBS["mono_times_poly"])
    if str(cons.get("pattern")) in {"poly_poly"}:
        return dict(_FORM_KNOBS["poly_times_poly"])
    return None


def default_knobs_for_leaf(leaf_id: str, *, task: Task = "factor") -> dict[str, Any]:
    leaf = str(leaf_id or "")
    if task == "multiply":
        if "special" in leaf:
            return dict(_FORM_KNOBS["special_product_square"])
        return dict(_FORM_KNOBS["binomial_times_binomial"])
    if any(
        key in leaf
        for key in (
            "common_factor",
            "factor_gcf",
            "g6_factor_gcf",
        )
    ) or leaf in {"factor_gcf", "g6_factor_gcf"}:
        return dict(_FORM_KNOBS["gcf_monomial"])
    if _is_equation_leaf(leaf):
        return dict(_FORM_KNOBS["quadratic_equation_factor"])
    if _is_grouping_leaf(leaf):
        return dict(_FORM_KNOBS["factor_by_grouping"])
    if "cubes" in leaf:
        return dict(_FORM_KNOBS["sum_diff_cubes"])
    if "quadratic_form" in leaf:
        return dict(_FORM_KNOBS["quadratic_form"])
    if "special" in leaf or ("conjugate" in leaf and "factoring" in leaf):
        return dict(_FORM_KNOBS["difference_of_squares"])
    return dict(_FORM_KNOBS["trinomial_x2_bx_c"])


def _catalog_for_leaf(leaf_id: str, *, task: Task) -> str | None:
    leaf = str(leaf_id or "")
    if _is_equation_leaf(leaf):
        return "algebra1_factoring"
    if leaf.startswith("a2_"):
        return "algebra2_polys"
    if task == "multiply":
        return "algebra1_polynomials"
    if any(
        key in leaf
        for key in (
            "factoring",
            "quadratic_factoring",
            "general_strategy",
            "factor_gcf",
            "common_factor",
        )
    ):
        return "algebra1_factoring"
    return None


def _select_form(
    ctx: PrimitiveContext,
    *,
    leaf_id: str,
    catalog_name: str | None,
) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    if not catalog_name:
        return None, {}
    from question_engine.frameworks.primitives.openstax_form_catalogs import (
        catalog_form_meta,
        forms_for_leaf,
        load_form_catalog,
        select_form_id,
    )

    catalog = load_form_catalog(catalog_name)
    forms = forms_for_leaf(catalog, leaf_id)
    mappable = [f for f in forms if knobs_from_form(f)]
    if not mappable:
        return None, {}
    d = float(getattr(ctx, "topic_d", 0.0) or 0.0)
    form = select_form_id(mappable, d=d, rng=ctx.rng)
    return form, catalog_form_meta(form, catalog)


def _constraints_from_knobs(
    settings: dict[str, Any],
    knobs: dict[str, Any],
    *,
    d: float,
) -> FactorConstraints:
    merged = dict(settings)
    kind = str(knobs.get("kind") or "linear")
    if kind != "gcf_monomial":
        merged["factor_kind"] = kind
    if knobs.get("n_factors") is not None:
        merged["n_factors"] = int(knobs["n_factors"])
        merged["min_factors"] = int(knobs["n_factors"])
        merged["max_factors"] = int(knobs["n_factors"])
    if knobs.get("allow_nonmonic") is not None:
        merged["allow_nonmonic"] = bool(knobs["allow_nonmonic"])
        if knobs["allow_nonmonic"]:
            merged.setdefault("leading_max", 4)
    for key in (
        "const_min",
        "const_max",
        "nonmonic_weight",
        "leading_min",
        "leading_max",
        "require_gcf",
        "content_primitive",
    ):
        if knobs.get(key) is not None:
            merged[key] = knobs[key]
    merged["max_product_degree"] = int(
        knobs.get("max_product_degree", DEFAULT_MAX_PRODUCT_DEGREE)
    )
    if kind == "grouping":
        merged["max_product_degree"] = max(3, int(merged["max_product_degree"]))
    dens = knobs.get("dens_style")
    if dens in {"factored", "expanded", "auto"}:
        merged["dens_style"] = dens
    return constraints_from_settings(merged, d=d)


def _method_for(kind: str, draw: FactorDraw) -> str:
    if kind == "diff_squares":
        return "difference_of_squares"
    if kind == "perfect_square":
        return "perfect_square"
    if kind == "grouping":
        return "grouping_cubic" if draw.degree >= 3 else "grouping_quadratic"
    if kind == "cubes":
        prod = draw.product
        const = prod.get(0, Fraction(0))
        return "sum_of_cubes" if const > 0 else "difference_of_cubes"
    if kind == "quadratic_form":
        return "quadratic_form_simple"
    if kind == "mono_poly":
        return "distribute"
    if draw.constraints.allow_nonmonic and any(
        not f.is_monic() for f in draw.factors
    ):
        return "ac_method"
    return "monic_simple" if draw.degree <= 2 else "linear_product"


def _package_draw(
    ctx: PrimitiveContext,
    draw: FactorDraw,
    *,
    task: Task,
    form_meta: dict[str, Any],
    knobs: dict[str, Any],
) -> FactorProductResult:
    var = ctx.sample_variable()
    kind = draw.factor_kind
    as_square = kind == "perfect_square"
    factored_l, factored_t = render_factor_product(
        draw, var.latex, dens_style="factored", as_square=as_square
    )
    expanded_l, expanded_t = render_factor_product(
        draw, var.latex, dens_style="expanded"
    )
    dress_tags: tuple[str, ...] = ()
    if task == "multiply":
        prompt_l, prompt_t = factored_l, factored_t
        ans_l, ans_t = expanded_l, expanded_t
    else:
        d = float(getattr(ctx, "topic_d", 0.0) or 0.0)
        unsim = None
        if knobs.get("package") == "equation":
            qk = _quadratic_factoring_knobs()
            unsim = float(qk.get("unsimplify_from_d", 10.0))
        if kind != "gcf_monomial":
            prompt_l, prompt_t, dress_tags = _present_expanded_for_factor(
                ctx, draw.product, var, d=d, unsimplify_from_d=unsim
            )
        else:
            prompt_l, prompt_t = expanded_l, expanded_t
        ans_l, ans_t = factored_l, factored_t

    if knobs.get("package") == "equation":
        prompt_l = f"{prompt_l} = 0"
        prompt_t = f"{prompt_t} = 0"
        ans_l = f"{factored_l} = 0"
        ans_t = f"{factored_t} = 0"

    method = _method_for(kind, draw)
    fid = str(form_meta.get("form_id") or knobs.get("form_id") or method)
    pieces = list(draw.poly_factors) if draw.poly_factors else [
        PolyFactor.from_coeffs(f.coeffs()) for f in draw.factors
    ]
    tags = [
        method,
        f"degree:{draw.degree}",
        f"kind:{kind}",
        f"task:{task}",
        f"d:{draw.effective_d:.1f}",
    ]
    if dress_tags:
        tags = [*dress_tags, *tags]
    if draw.outer_gcf != 1:
        tags.append("with_gcf")
    meta = {
        "skeleton_pattern": "FactorProduct",
        "skeleton_source": "poly_skeleton",
        "task": task,
        "method": method,
        "degree": draw.degree,
        "dens_style": draw.dens_style,
        "factor_kind": kind,
        "n_factors": draw.n_factors,
        "outer_gcf": str(draw.outer_gcf),
        "max_product_degree": draw.constraints.max_product_degree,
        "factor_bias": draw.as_dict().get("bias_label"),
        **form_meta,
        "form_id": fid,
        "openstax_form": form_meta.get("openstax_form") or fid,
        "shape_id": form_meta.get("shape_id") or fid,
    }
    if knobs.get("package") == "equation":
        meta["packaging"] = "zero_product"
        meta["task"] = "factor"
    if form_meta.get("catalog_id"):
        meta["construction"] = form_meta.get("construction") or "forward_form_catalog"
    return FactorProductResult(
        prompt_latex=prompt_l,
        prompt_text=prompt_t,
        answer_latex=ans_l,
        answer_text=ans_t,
        task=task,
        method=method,
        degree=int(draw.degree),
        form_id=fid,
        dens_style=draw.dens_style,
        factor_kind=kind,
        outer_gcf=draw.outer_gcf,
        poly_coeffs=dict(draw.product),
        factor_coeffs=tuple(dict(p.coeffs()) for p in pieces),
        upgrades=tuple(tags),
        effective_d=draw.effective_d,
        metadata=meta,
    )


def _from_factor_gcf(
    ctx: PrimitiveContext,
    form_meta: dict[str, Any],
) -> FactorProductResult:
    """GCF-only OpenStax form: residual need not fully factor — keep factor_gcf."""
    from question_engine.frameworks.primitives.factor_gcf import sample_factor_gcf

    g = sample_factor_gcf(ctx)
    fid = str(form_meta.get("form_id") or "gcf_monomial")
    meta = {
        "skeleton_pattern": "FactorGcf",
        "skeleton_source": "factor_gcf",
        "task": "factor",
        "method": "gcf",
        "degree": int(g.max_degree),
        **form_meta,
        "form_id": fid,
        "openstax_form": form_meta.get("openstax_form") or fid,
        "shape_id": form_meta.get("shape_id") or fid,
        "construction": form_meta.get("construction") or "forward_form_catalog",
    }
    return FactorProductResult(
        prompt_latex=g.latex,
        prompt_text=g.text,
        answer_latex=g.factored_latex,
        answer_text=g.factored_text,
        task="factor",
        method="gcf",
        degree=int(g.max_degree),
        form_id=fid,
        dens_style="expanded",
        factor_kind="gcf_monomial",
        outer_gcf=Fraction(1),
        poly_coeffs={},
        factor_coeffs=(),
        upgrades=tuple(["gcf", *g.upgrades]),
        effective_d=g.effective_d,
        metadata=meta,
    )


def sample_factor_product_item(
    ctx: PrimitiveContext,
    *,
    task: Task | None = None,
    leaf_id: str | None = None,
    catalog_name: str | None = None,
    form_id: str | None = None,
    knobs: dict[str, Any] | None = None,
) -> FactorProductResult:
    """Generate one FactorProduct item (form knobs → factor_sampler → package)."""
    settings = dict(getattr(ctx, "settings", None) or {})
    leaf = leaf_id or str(getattr(ctx, "leaf_id", "") or "")
    resolved_task: Task = task or "factor"
    form: dict[str, Any] | None = None
    form_meta: dict[str, Any] = {}

    if form_id:
        knobs = knobs or knobs_from_form_id(form_id) or default_knobs_for_leaf(
            leaf, task=resolved_task
        )
        knobs["form_id"] = form_id
        form_meta = {
            "form_id": form_id,
            "openstax_form": form_id,
            "shape_id": form_id,
            "construction": "forward_form_catalog",
        }
    else:
        cat = catalog_name or _catalog_for_leaf(leaf, task=resolved_task)
        form, form_meta = _select_form(ctx, leaf_id=leaf, catalog_name=cat)
        knobs = knobs or knobs_from_form(form) or default_knobs_for_leaf(
            leaf, task=resolved_task
        )

    if knobs.get("task") in {"factor", "multiply"}:
        resolved_task = knobs["task"]
    d = float(getattr(ctx, "topic_d", 0.0) or 0.0)
    if resolved_task == "multiply":
        knobs = _multiply_knobs_for_d(knobs, d, ctx.rng)
    leaf_l = str(leaf or "")
    if _is_equation_leaf(leaf_l):
        knobs = _equation_knobs_for_d(d, ctx.rng)
        fid = (
            "trinomial_ax2_bx_c"
            if knobs.get("allow_nonmonic")
            else "quadratic_equation_factor"
        )
        form_meta = {
            **form_meta,
            "form_id": fid,
            "openstax_form": fid,
            "shape_id": fid,
            "construction": "forward_form_catalog",
        }
    elif any(
        key in leaf_l
        for key in ("common_factor", "factor_gcf", "g6_factor_gcf")
    ) or leaf_l in {"factor_gcf", "g6_factor_gcf"}:
        knobs = dict(_FORM_KNOBS["gcf_monomial"])
        form_meta = {
            **form_meta,
            "form_id": "gcf_monomial",
            "openstax_form": "gcf_monomial",
            "shape_id": "gcf_monomial",
            "construction": "forward_form_catalog",
        }
    elif _is_grouping_leaf(leaf_l):
        knobs = dict(_FORM_KNOBS["factor_by_grouping"])
        form_meta = {
            **form_meta,
            "form_id": "factor_by_grouping",
            "openstax_form": "factor_by_grouping",
            "shape_id": "factor_by_grouping",
            "construction": "forward_form_catalog",
        }

    if knobs.get("kind") == "gcf_monomial":
        return _from_factor_gcf(ctx, form_meta)

    cons = _constraints_from_knobs(settings, knobs, d=d)
    n = knobs.get("n_factors")
    last_err: Exception | None = None
    for _ in range(24):
        try:
            draw = sample_factor_product(
                ctx,
                n_factors=int(n) if n is not None else None,
                d=d,
                constraints=cons,
                dens_style=knobs.get("dens_style"),
                factor_kind=str(knobs.get("kind") or cons.factor_kind),
            )
            if poly_degree(draw.product) < 1:
                continue
            return _package_draw(
                ctx, draw, task=resolved_task, form_meta=form_meta, knobs=knobs
            )
        except (ValueError, ZeroDivisionError) as exc:
            last_err = exc
            continue
    raise RuntimeError(f"sample_factor_product_item failed: {last_err}")


_MIXER_FORMS_A2 = (
    "trinomial_x2_bx_c",
    "trinomial_a_gt_1",
    "difference_of_squares",
    "perfect_square_trinomial",
    "factor_by_grouping",
    "sum_diff_cubes",
    "gcf_then_pattern",
    "gcf_factor",
)
_MIXER_FORMS_A1 = (
    "trinomial_x2_bx_c",
    "trinomial_ax2_bx_c",
    "difference_of_squares",
    "perfect_square_trinomial",
    "factor_by_grouping",
    "gcf_monomial",
    "gcf_then_pattern",
)


def sample_factor_product_mixer(
    ctx: PrimitiveContext,
    *,
    leaf_id: str | None = None,
) -> FactorProductResult:
    """D-weighted form mixer for all-techniques / general-strategy leaves."""
    leaf = leaf_id or str(getattr(ctx, "leaf_id", "") or "")
    d = float(getattr(ctx, "topic_d", 0.0) or 0.0)
    include_cubes = "all_techniques" in leaf
    pool = list(_MIXER_FORMS_A2 if include_cubes else _MIXER_FORMS_A1)
    if include_cubes and d < 6:
        pool = [f for f in pool if f != "sum_diff_cubes"]
    weights = []
    for fid in pool:
        kn = _FORM_KNOBS[fid]
        w = 1.0
        if fid in {"trinomial_x2_bx_c", "trinomial_ax2_bx_c", "trinomial_a_gt_1"}:
            w = 1.4
        if fid in {"gcf_factor", "gcf_monomial"} and d < 4:
            w = 1.2
        if kn.get("allow_nonmonic") and d < 6:
            w = 0.15
        if kn.get("allow_nonmonic") and d >= 14:
            w = 1.2
        if fid == "factor_by_grouping" and d < 3:
            w = 0.4
        weights.append(w)
    fid = ctx.rng.choices(pool, weights=weights, k=1)[0]
    result = sample_factor_product_item(ctx, task="factor", leaf_id=leaf, form_id=fid)
    meta = dict(result.metadata)
    meta["mixer_pick"] = fid
    upgrades = ("all_techniques", fid, *result.upgrades)
    return FactorProductResult(
        prompt_latex=result.prompt_latex,
        prompt_text=result.prompt_text,
        answer_latex=result.answer_latex,
        answer_text=result.answer_text,
        task=result.task,
        method=f"all:{result.method}",
        degree=result.degree,
        form_id=result.form_id,
        dens_style=result.dens_style,
        factor_kind=result.factor_kind,
        outer_gcf=result.outer_gcf,
        poly_coeffs=result.poly_coeffs,
        factor_coeffs=result.factor_coeffs,
        upgrades=upgrades,
        effective_d=result.effective_d,
        metadata=meta,
    )


def generate_factor_product_question(
    settings: dict[str, Any] | None = None,
    *,
    task: Task = "factor",
    leaf_id: str = "quadratic_factoring",
) -> FactorProductResult:
    """Demo / gallery API: build context and sample one FactorProduct item."""
    from question_engine.frameworks.primitives import (
        PRIM_FACTOR_GCF,
        PRIM_FACTOR_POLY,
        PRIM_NUMBERS,
        PRIM_VARIABLE,
        build_context,
    )
    from question_engine.frameworks.primitives.expression_policy import polynomial_policy

    settings = dict(settings or {})
    settings.setdefault("count", 1)
    max_deg = int(settings.get("max_degree", settings.get("max_product_degree", 4)))
    resolved_leaf = str(settings.get("_leaf_id") or leaf_id)
    gcf_leaf = (
        any(k in resolved_leaf for k in ("common_factor", "factor_gcf"))
        or resolved_leaf in {"factor_gcf", "g6_factor_gcf"}
    )
    prims = (
        [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_FACTOR_GCF]
        if gcf_leaf
        else [PRIM_NUMBERS, PRIM_VARIABLE, PRIM_FACTOR_POLY]
    )
    ctx = build_context(
        settings,
        prims,
        policy=polynomial_policy(max_degree=max(2, max_deg)),
        leaf_id=resolved_leaf,
    )
    return sample_factor_product_item(
        ctx,
        task=task,
        leaf_id=str(settings.get("_leaf_id") or leaf_id),
        form_id=settings.get("form_id"),
    )


def use_factor_product_skeleton(settings: dict[str, Any] | None) -> bool:
    """FactorProduct is the live default for wired poly factor/multiply leaves."""
    s = dict(settings or {})
    if bool(s.get("use_factor_poly")) or bool(s.get("use_constructive_poly")):
        return False
    pat = str(s.get("skeleton_pattern", "")).strip()
    if pat in {
        "factor_poly",
        "constructive",
        "Constructive",
        "hand",
        "constructive_poly",
        "polynomials",
    }:
        return False
    if "use_factor_product_skeleton" in s:
        return bool(s.get("use_factor_product_skeleton"))
    if pat in {"FactorProduct", "factor_product"}:
        return True
    return True


_LEGACY_ADD_SUB = {
    "sample_polynomial_add_subtract",
    "polynomials",
    "hand",
    "constructive",
    "legacy",
}


def use_poly_add_sub_skeleton(settings: dict[str, Any] | None) -> bool:
    """PolyAddSub inflate is the live default for add/subtract leaves."""
    s = dict(settings or {})
    if bool(s.get("use_sample_polynomial_add_subtract")):
        return False
    if bool(s.get("use_poly_add_sub_skeleton") is False):
        return False
    pat = str(s.get("skeleton_pattern", "")).strip()
    if pat in _LEGACY_ADD_SUB:
        return False
    if "use_poly_add_sub_skeleton" in s:
        return bool(s.get("use_poly_add_sub_skeleton"))
    return True


@dataclass(frozen=True)
class PolyAddSubResult:
    prompt_latex: str
    prompt_text: str
    answer_latex: str
    answer_text: str
    op: str
    degree: int
    upgrades: tuple[str, ...]
    effective_d: float
    metadata: dict[str, Any]

    def debug_dict(self) -> dict[str, Any]:
        return {
            "pattern": "PolyAddSub",
            "op": self.op,
            "degree": self.degree,
            **self.metadata,
        }


def _wrap_poly(latex: str, text: str) -> tuple[str, str]:
    return f"\\left({latex}\\right)", f"({text})"


def sample_poly_add_sub(ctx: PrimitiveContext) -> PolyAddSubResult:
    """Inflate two polynomials and add/subtract. Not FactorProduct.

    D=0: two degree-1 binomials ``(2x+1)+(x+3)``. Numeric grows coeffs;
    format unlocks degree 2, then more terms, then constructive dress.
    """
    from question_engine.frameworks.primitives.skeleton_difficulty import (
        SkeletonDifficultyBands,
    )

    rng = ctx.rng
    d = float(getattr(ctx, "topic_d", 0.0) or 0.0)
    bands = SkeletonDifficultyBands.from_d(d)
    nt, ft = bands.numeric_tier, bands.format_tier
    var = ctx.sample_variable()
    hi = (4, 8, 12, 18, 28)[max(0, min(4, nt))]
    if ft == 0:
        deg = 1
        n_terms = 2
    elif ft == 1:
        deg = 2
        n_terms = 3
    else:
        deg = 3 if ft >= 2 else 2
        n_terms = deg + 1
    op = "+" if (ft == 0 or rng.random() < 0.55) else "-"
    settings = dict(getattr(ctx, "settings", None) or {})
    forced_op = settings.get("poly_add_sub_op")
    if forced_op in ("+", "-"):
        op = forced_op
    if ft == 0 and nt == 0:
        a1, b1 = rng.randint(1, 3), rng.randint(1, 4)
        a2, b2 = rng.randint(1, 3), rng.randint(1, 4)
        p = {1: Fraction(a1), 0: Fraction(b1)}
        q = {1: Fraction(a2), 0: Fraction(b2)}
    else:
        p = sample_poly_coeffs(ctx, degree=deg, n_terms=n_terms, require_leading=True)
        q_deg = deg if rng.random() < 0.75 else max(1, deg - 1)
        q = sample_poly_coeffs(
            ctx,
            degree=q_deg,
            n_terms=min(q_deg + 1, n_terms),
            require_leading=True,
        )

        def _clamp(m: dict[int, Fraction]) -> dict[int, Fraction]:
            out: dict[int, Fraction] = {}
            for k, v in m.items():
                if v == 0:
                    continue
                mag = min(abs(int(v.numerator)), hi)
                mag = max(1, mag)
                out[k] = Fraction(mag if v > 0 else -mag)
            return out

        p, q = _clamp(p), _clamp(q)
    if op == "+":
        result = combine_coeff_maps(p, q)
    else:
        result = combine_coeff_maps(p, scale_coeffs(q, Fraction(-1)))
    pl, pt = render_poly(p, var, descending=True)
    ql, qt = render_poly(q, var, descending=True)
    pl, pt = _wrap_poly(pl, pt)
    ql, qt = _wrap_poly(ql, qt)
    prompt_l = f"{pl} + {ql}" if op == "+" else f"{pl} - {ql}"
    prompt_t = f"{pt} + {qt}" if op == "+" else f"{pt} - {qt}"
    tags: list[str] = ["poly_add_sub", f"deg:{deg}", op]
    if ft >= 3:
        from question_engine.frameworks.primitives.constructive import (
            PolynomialTarget,
            construct_poly,
            verify_poly,
        )

        inflate_d = max(1.0, d - 18.0)
        for _ in range(6):
            try:
                surf_p = construct_poly(
                    ctx,
                    d=inflate_d,
                    var=var,
                    target=PolynomialTarget(
                        coeffs=tuple((k, v) for k, v in sorted(p.items()))
                    ),
                    min_inflators=1,
                )
                if verify_poly(
                    surf_p,
                    PolynomialTarget(
                        coeffs=tuple((k, v) for k, v in sorted(p.items()))
                    ),
                ):
                    pl, pt = _wrap_poly(surf_p.latex, surf_p.text)
                    prompt_l = f"{pl} + {ql}" if op == "+" else f"{pl} - {ql}"
                    prompt_t = f"{pt} + {qt}" if op == "+" else f"{pt} - {qt}"
                    tags.append("inflate")
                    break
            except Exception:
                continue
    ans_l, ans_t = render_poly(result, var, descending=True)
    meta = {
        "skeleton_pattern": "PolyAddSub",
        "skeleton_source": "poly_skeleton",
        "op": op,
        "degree": deg,
        "numeric_tier": nt,
        "format_tier": ft,
        "form_id": str(settings.get("_openstax_form_id") or "poly_add_sub"),
        "construction": "affine_inflate_pair",
    }
    return PolyAddSubResult(
        prompt_latex=prompt_l,
        prompt_text=prompt_t,
        answer_latex=ans_l,
        answer_text=ans_t,
        op=op,
        degree=int(poly_degree(result) or deg),
        upgrades=tuple(tags),
        effective_d=d,
        metadata=meta,
    )
