"""Rational + PFD generators on the constructive spine (L2–L4).

Inheritance
-----------
- L2 simplify / L3 add-subtract: ``construct_rational_sum`` (shared core).
- L4 PFD: ``partial_fractions.combine_pf_to_rational`` → same constructive
  combine as L3, but seeded from PF terms (pedagogical reverse of add).

Higher-course leaves (A2 / PC) reuse these generators via catalog aliases;
do not fork Mad-Libs rationals for course variants.
"""

from __future__ import annotations

from typing import Any

from question_engine.core.models import Question
from question_engine.frameworks.primitives import (
    PRIM_NUMBERS,
    PRIM_VARIABLE,
    build_context,
)
from question_engine.frameworks.primitives.algebraic_ml import enrich_algebraic_meta
from question_engine.frameworks.primitives.constructive import construct_rational_sum
from question_engine.frameworks.primitives.expression_policy import POLYNOMIAL_POLICY_DEFAULT
from question_engine.frameworks.primitives.partial_fractions import (
    apply_pfd_continuous_knobs,
    combine_pf_to_rational,
)
from question_engine.frameworks.primitives.rational_cancel import resolve_rational_cancel_count
from question_engine.generators.utils import make_questions
from question_engine.generators.rational_multiply_divide import (
    generate_rational_expression_multiply_divide,
)
from question_engine.generators.complex_fractions import generate_complex_fractions


def rational_expression_multiply_divide(topic: str, settings: dict) -> list[Question]:
    return generate_rational_expression_multiply_divide(topic, settings)


def complex_fractions(topic: str, settings: dict) -> list[Question]:
    return generate_complex_fractions(topic, settings)


def _course_tag_for(topic: str) -> str:
    t = str(topic or "")
    if t.startswith("a2_"):
        return "a2"
    if t.startswith("pc_"):
        return "pc"
    return "a1"


def _maybe_a2_rational_form(topic: str, settings: dict):
    """Select OpenStax rational form for A2 leaves; else ``(None, {})``."""
    if not str(topic or "").startswith("a2_"):
        return None, {}
    import random as _random

    from question_engine.frameworks.difficulty_budget import settings_difficulty
    from question_engine.frameworks.primitives.openstax_a2 import select_a2_form

    d = float(settings_difficulty(settings))
    seed = settings.get("seed")
    batch = int(settings.get("_batch_index") or 0)
    if seed is not None:
        try:
            rng = _random.Random(int(seed) + batch * 1009)
        except (TypeError, ValueError):
            rng = _random.Random()
    else:
        rng = _random.Random()
    return select_a2_form(
        "algebra2_rationals", d=d, rng=rng, leaf_id=str(topic or "")
    )


def _build_common_den_sum(ctx, *, op: str = "+"):
    """Two rationals sharing a linear denominator (OpenStax §7.2 common-den form)."""
    from fractions import Fraction

    from packages.polynomial_core import rational_excluded_values_latex
    from question_engine.frameworks.primitives._algebra_render import sample_integerish
    from question_engine.frameworks.primitives.constructive import (
        RationalPolyTarget,
        SurfaceExpression,
        _fraction_latex,
        _poly_add,
        _poly_from_linear,
        _pick_distinct_roots,
    )

    v = ctx.sample_variable()
    root = _pick_distinct_roots(ctx, 1)[0]
    den = _poly_from_linear(root)
    n1 = int(sample_integerish(ctx, exclude_zero=True).value)
    n2 = int(sample_integerish(ctx, exclude_zero=True).value)
    if op == "-":
        combined = _poly_add({0: Fraction(n1)}, {0: Fraction(-n2)})
        join = "-"
        n2_tex = str(n2) if n2 >= 0 else f"({n2})"
    else:
        combined = _poly_add({0: Fraction(n1)}, {0: Fraction(n2)})
        join = "+"
        n2_tex = str(n2)
    var_tex = v.latex or v.name
    if root == 0:
        den_l = var_tex
    elif root > 0:
        den_l = f"{var_tex} - {root}"
    else:
        den_l = f"{var_tex} + {abs(root)}"
    latex = f"\\frac{{{n1}}}{{{den_l}}} {join} \\frac{{{n2_tex}}}{{{den_l}}}"
    text = f"({n1})/({den_l}) {join} ({n2_tex})/({den_l})"
    ans_l, ans_t = _fraction_latex(combined, den, v)
    excl = int(root) if root.denominator == 1 else str(root)
    note = rational_excluded_values_latex([root])
    if note:
        note = note.replace("x \\neq", f"{var_tex} \\neq", 1)
        ans_l = f"{ans_l},\\; {note}"
        ans_t = f"{ans_t}, {v.name} ≠ {excl}"
    target = RationalPolyTarget(
        num=tuple(sorted(combined.items(), reverse=True)),
        den=tuple(sorted(den.items(), reverse=True)),
        level="L3",
    )
    return SurfaceExpression(
        latex=latex,
        text=text,
        target=target,
        level="L3",
        inflators_applied=("common_den",),
        simplified_latex=ans_l,
        simplified_text=ans_t,
        metadata={
            "mode": "add_subtract_rationals",
            "n_terms": 2,
            "cancel_factor_count": 0,
            "same_den": True,
            "excluded_values": [excl],
        },
    )


def _meta_builder(
    last: dict[str, Any],
    topic: str,
    *,
    pack: str,
    generator: str,
    methods_used: list[str] | None = None,
):
    tag = _course_tag_for(topic)

    def metadata_builder(_p: str, _t: str, answer: str | None) -> dict[str, Any]:
        meta = dict(last.get("meta") or {})
        knobs = {
            k: meta[k]
            for k in (
                "cancel_factor_count",
                "n_terms",
                "pfd_term_count",
                "pfd_coef_abs_max",
                "pfd_root_abs_max",
                "allow_repeated_factors",
                "allow_quadratic_irreducible",
                "term_count",
                "level",
            )
            if k in meta
        }
        # Promote continuous structure from constructive metadata.
        constructive = meta.get("constructive")
        if isinstance(constructive, dict):
            for k in ("n_terms", "cancel_factor_count", "mode", "effective_d"):
                if k in constructive and k not in knobs:
                    knobs[k] = constructive[k]
        mode = meta.get("mode")
        if not mode and isinstance(constructive, dict):
            mode = constructive.get("mode")
        return enrich_algebraic_meta(
            meta,
            pack=pack,
            generator=generator,
            family=str(mode or pack),
            methods_used=methods_used or ["rational"],
            knobs=knobs,
            answer=answer,
            course_tag=tag,
            n_terms=meta.get("n_terms") or knobs.get("n_terms"),
            n_factors=meta.get("cancel_factor_count"),
        )

    return metadata_builder


def _rational_ctx(settings: dict, *, leaf_id: str = ""):
    return build_context(
        settings,
        [PRIM_NUMBERS, PRIM_VARIABLE],
        policy=POLYNOMIAL_POLICY_DEFAULT,
        leaf_id=leaf_id
        or str(settings.get("_leaf_id") or settings.get("type_id") or ""),
    )


def _use_add_sub_cancel_skeleton(settings: dict) -> bool:
    """AddSubCancel is the live default for ± rationals.

    Opt out (legacy constructive / OpenStax form path):
    - ``use_constructive_rational=True``
    - ``use_add_sub_cancel_skeleton=False``
    - ``skeleton_pattern`` in {constructive, constructive_rational}
    """
    if bool(settings.get("use_constructive_rational")):
        return False
    pat = str(settings.get("skeleton_pattern", "")).strip()
    if pat in {"constructive", "Constructive", "constructive_rational"}:
        return False
    if "use_add_sub_cancel_skeleton" in settings:
        return bool(settings.get("use_add_sub_cancel_skeleton"))
    if pat in {"AddSubCancel", "add_sub_cancel"}:
        return True
    return True


def _use_simplify_cancel_skeleton(settings: dict) -> bool:
    """SimplifyCancel is the live default for single-fraction simplify.

    Opt out:
    - ``use_constructive_rational=True``
    - ``use_simplify_cancel_skeleton=False``
    - ``skeleton_pattern`` in {constructive, constructive_rational}
    """
    if bool(settings.get("use_constructive_rational")):
        return False
    pat = str(settings.get("skeleton_pattern", "")).strip()
    if pat in {"constructive", "Constructive", "constructive_rational"}:
        return False
    if "use_simplify_cancel_skeleton" in settings:
        return bool(settings.get("use_simplify_cancel_skeleton"))
    if pat in {"SimplifyCancel", "simplify_cancel"}:
        return True
    return True


def rational_add_subtract(topic: str, settings: dict) -> list[Question]:
    """L3: add/subtract rational expressions via AddSubCancel skeleton.

    Default: goal→inflate→PFD+2D-kernel (``rational_skeleton``).
    Legacy constructive / A2 form-catalog path: set
    ``use_constructive_rational=True`` (or ``use_add_sub_cancel_skeleton=False``).
    """
    from question_engine.frameworks.primitives.rational_cancel import (
        apply_continuous_rational_structure,
    )

    settings = apply_continuous_rational_structure(settings)
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}
    use_skeleton = _use_add_sub_cancel_skeleton(settings)

    def build() -> tuple[str, str, str | None]:
        if use_skeleton:
            from question_engine.frameworks.primitives.rational_skeleton import (
                sample_add_sub_cancel,
            )

            ctx = _rational_ctx(settings, leaf_id=str(topic or ""))
            result = sample_add_sub_cancel(ctx)
            last["meta"] = {
                **ctx.metadata(),
                "primitive_engine": "rational_skeleton",
                "level": "L3",
                "mode": "add_subtract_rationals",
                "cancel_factor_count": result.cancel_count,
                "n_terms": len(result.terms),
                "term_count": len(result.terms),
                "excluded_values": result.metadata.get("excluded_values") or [],
                "constructive": result.debug_dict(),
                **result.metadata,
            }
            answer = result.answer_latex if include_answer_key else None
            return (
                rf"\text{{Combine and simplify: }} {result.prompt_latex}",
                f"Combine and simplify: {result.prompt_text}",
                answer,
            )

        form, form_meta = _maybe_a2_rational_form(topic, settings)
        ctx = _rational_ctx(settings, leaf_id=str(topic or ""))
        constraints = (form or {}).get("constraints") or {}
        if form_meta.get("form_id") == "add_common_den":
            op = "+" if ctx.rng.random() < 0.55 else "-"
            surface = _build_common_den_sum(ctx, op=op)
        else:
            k = resolve_rational_cancel_count(settings, d=ctx.topic_d, rng=ctx.rng)
            if constraints.get("cancel_count") is not None:
                k = int(constraints["cancel_count"])
            elif constraints.get("cancel_min") is not None:
                k = max(k, int(constraints["cancel_min"]))
            n_terms = (
                int(constraints["n_terms"])
                if constraints.get("n_terms") is not None
                else (
                    int(settings["term_count"])
                    if settings.get("term_count") is not None
                    else None
                )
            )
            surface = construct_rational_sum(
                ctx, d=ctx.topic_d, cancel_count=k, as_sum=True, n_terms=n_terms
            )
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "constructive_rational",
            "level": surface.level,
            "mode": "add_subtract_rationals",
            "cancel_factor_count": surface.metadata.get("cancel_factor_count", 0),
            "n_terms": surface.metadata.get("n_terms"),
            "term_count": surface.metadata.get("n_terms"),
            "excluded_values": surface.metadata.get("excluded_values") or [],
            "constructive": surface.metadata,
            **form_meta,
        }
        answer = surface.simplified_latex if include_answer_key else None
        return (
            rf"\text{{Combine and simplify: }} {surface.latex}",
            f"Combine and simplify: {surface.text}",
            answer,
        )

    return make_questions(
        topic,
        count,
        include_answer_key,
        build,
        metadata_builder=_meta_builder(
            last,
            topic,
            pack="structured_rational_add",
            generator="rational_expression_simplification",
            methods_used=["rational", "combine", "cancel"],
        ),
        settings=settings,
    )


def rational_simplify(topic: str, settings: dict) -> list[Question]:
    """L2: simplify a rational with planned cancellation via SimplifyCancel.

    Default: goal→inflate→single fraction (``rational_skeleton``).
    Legacy constructive / form-catalog path: set
    ``use_constructive_rational=True`` (or ``use_simplify_cancel_skeleton=False``).
    """
    from question_engine.frameworks.primitives.rational_cancel import (
        apply_continuous_rational_structure,
    )

    settings = apply_continuous_rational_structure(settings)
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}
    tid = str(topic or "rational_simplification")
    use_skeleton = _use_simplify_cancel_skeleton(settings)

    def build() -> tuple[str, str, str | None]:
        if use_skeleton:
            from question_engine.frameworks.primitives.rational_skeleton import (
                sample_simplify_cancel,
            )

            ctx = _rational_ctx(settings, leaf_id=tid)
            result = sample_simplify_cancel(ctx)
            form_meta = {
                "form_id": "simplify_cancel",
                "openstax_form": "simplify_cancel",
                "shape_id": "simplify_cancel",
                "catalog_id": (
                    "algebra2_rationals" if tid.startswith("a2_") else "algebra1_rationals"
                ),
                "construction": "forward_form_catalog",
            }
            last["meta"] = {
                **ctx.metadata(),
                "primitive_engine": "rational_skeleton",
                "level": "L2",
                "mode": "simplify_rational",
                "cancel_factor_count": result.cancel_count,
                "n_terms": 1,
                "excluded_values": result.metadata.get("excluded_values") or [],
                "constructive": result.debug_dict(),
                **result.metadata,
                **form_meta,
            }
            answer = result.answer_latex if include_answer_key else None
            return (
                rf"\text{{Simplify: }} {result.prompt_latex}",
                f"Simplify: {result.prompt_text}",
                answer,
            )

        form, form_meta = _maybe_a2_rational_form(topic, settings)
        ctx = _rational_ctx(settings, leaf_id=tid)
        if not form_meta and not tid.startswith("a2_"):
            from question_engine.frameworks.primitives.openstax_form_catalogs import (
                catalog_form_meta,
                forms_for_leaf,
                load_form_catalog,
                select_form_id,
            )

            catalog = load_form_catalog("algebra1_rationals")
            forms = forms_for_leaf(catalog, tid)
            # This leaf only generates cancel-simplify; filter to that form.
            simplify_forms = [
                f for f in forms if str(f.get("form_id")) == "simplify_cancel"
            ] or forms
            form = select_form_id(simplify_forms, d=float(ctx.topic_d), rng=ctx.rng)
            form_meta = catalog_form_meta(form, catalog)
        constraints = (form or {}).get("constraints") or {}
        k = resolve_rational_cancel_count(settings, d=ctx.topic_d, rng=ctx.rng)
        if constraints.get("cancel_min") is not None:
            k = max(k, int(constraints["cancel_min"]))
        surface = construct_rational_sum(
            ctx, d=ctx.topic_d, cancel_count=k, as_sum=False
        )
        actual_k = surface.metadata.get("cancel_factor_count", k)
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "constructive_rational",
            "level": surface.level,
            "mode": "simplify_rational",
            "cancel_factor_count": actual_k,
            "n_terms": surface.metadata.get("n_terms") or 1,
            "excluded_values": surface.metadata.get("excluded_values") or [],
            "constructive": surface.metadata,
            **form_meta,
            "shape_id": form_meta.get("form_id") or "simplify_cancel",
        }
        answer = surface.simplified_latex if include_answer_key else None
        return (
            rf"\text{{Simplify: }} {surface.latex}",
            f"Simplify: {surface.text}",
            answer,
        )

    return make_questions(
        topic,
        count,
        include_answer_key,
        build,
        metadata_builder=_meta_builder(
            last,
            topic,
            pack="structured_rational_simplify",
            generator="rational_simplification",
            methods_used=["rational", "cancel"],
        ),
        settings=settings,
    )


def partial_fraction_decomposition(topic: str, settings: dict) -> list[Question]:
    """L4: seed PF answer, combine to single rational prompt (shared PFD core)."""
    settings = apply_pfd_continuous_knobs(settings)
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}
    n_terms_default = int(settings.get("pfd_term_count") or settings.get("n_terms") or 2)
    use_catalog = str(topic or "").startswith("pc_")

    def build() -> tuple[str, str, str | None]:
        ctx = _rational_ctx(settings, leaf_id=str(topic or ""))
        n_terms = n_terms_default
        allow_quadratic: bool | None = None
        form_stamp: dict[str, Any] = {}
        if use_catalog:
            from question_engine.frameworks.primitives.openstax_precalc import (
                pc_form_constraints,
                select_pc_form,
            )

            form, form_stamp = select_pc_form(
                "precalculus_partial_fractions",
                d=float(ctx.topic_d),
                rng=ctx.rng,
                leaf_id=str(topic or ""),
            )
            cons = pc_form_constraints(form)
            n_lin = cons.get("n_linear")
            want_quad = cons.get("quadratic")
            if want_quad is True:
                allow_quadratic = True
                # seed: n_terms includes the quadratic slot
                n_terms = int(n_lin or 1) + 1
            elif want_quad is False:
                allow_quadratic = False
                n_terms = int(n_lin or n_terms_default)
            n_terms = max(2, min(4, n_terms))
        surface = combine_pf_to_rational(
            ctx,
            d=ctx.topic_d,
            n_terms=n_terms,
            allow_quadratic=allow_quadratic,
        )
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "constructive_pfd",
            "level": surface.level,
            "mode": "pfd",
            "n_terms": surface.metadata.get("n_terms") or n_terms,
            "pfd_term_count": n_terms,
            "pfd_coef_abs_max": settings.get("pfd_coef_abs_max"),
            "pfd_root_abs_max": settings.get("pfd_root_abs_max"),
            "allow_repeated_factors": bool(settings.get("allow_repeated_factors")),
            "allow_quadratic_irreducible": bool(
                settings.get("allow_quadratic_irreducible")
                if allow_quadratic is None
                else allow_quadratic
            ),
            "constructive": surface.metadata,
            **form_stamp,
        }
        answer = surface.simplified_latex if include_answer_key else None
        return (
            rf"\text{{Decompose }} {surface.latex}",
            f"Decompose {surface.text}",
            answer,
        )

    return make_questions(
        topic,
        count,
        include_answer_key,
        build,
        metadata_builder=_meta_builder(
            last,
            topic,
            pack="structured_pfd",
            generator="partial_fraction_decomposition",
            methods_used=["partial_fractions", "combine"],
        ),
        settings=settings,
        )


def _use_eq_cancel_skeleton(settings: dict) -> bool:
    from question_engine.frameworks.primitives.rational_skeleton import use_eq_cancel_skeleton

    return use_eq_cancel_skeleton(settings)


def rational_equations(topic: str, settings: dict) -> list[Question]:
    """EqCancel: clear dens + extraneous. D=0 is a proportion."""
    if not _use_eq_cancel_skeleton(settings):
        from question_engine.generators.rational_equations import (
            generate_rational_equations,
        )

        return generate_rational_equations(topic, settings)

    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}

    def build() -> tuple[str, str, str | None]:
        from question_engine.frameworks.primitives.rational_skeleton import (
            sample_eq_cancel,
        )

        ctx = _rational_ctx(settings, leaf_id=str(topic or ""))
        result = sample_eq_cancel(ctx)
        last["meta"] = {
            **ctx.metadata(),
            "primitive_engine": "rational_skeleton",
            **result.metadata,
            "upgrades": list(result.upgrades),
        }
        answer = result.answer_latex if include_answer_key else None
        return (
            rf"\text{{Solve: }} {result.prompt_latex}",
            f"Solve: {result.prompt_text}",
            answer,
        )

    def metadata_builder(_p: str, _t: str, _a: str | None) -> dict[str, Any]:
        return dict(last.get("meta") or {})

    return make_questions(
        topic, count, include_answer_key, build,
        metadata_builder=metadata_builder, settings=settings,
    )


GENERATORS = {
    "rational_expression_simplification": rational_add_subtract,
    "a2_rational_expressions_adding_and_subtracting": rational_add_subtract,
    "rational_expressions_adding_and_subtracting": rational_add_subtract,
    "rational_simplification": rational_simplify,
    "a2_rational_expressions_simplifying": rational_simplify,
    "rational_expressions_simplifying": rational_simplify,
    "partial_fraction_decomposition": partial_fraction_decomposition,
    "pc_partial_fraction_decomposition": partial_fraction_decomposition,
    "rational_equations": rational_equations,
    "rational_expressions_equations": rational_equations,
    "a2_rational_expressions_equations": rational_equations,
    "a2_rational_expressions_multiplying_and_dividing": rational_expression_multiply_divide,
    "a2_rational_expressions_complex_fractions": complex_fractions,
    "pc_rational_equations": rational_equations,
}
