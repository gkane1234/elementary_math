"""Enriched calculus derivative-rule generators.

Power / product / quotient / chain / trig / ln-exp / invtrig / higher-order route
through the continuous-D Spec sampler in ``frameworks.primitives.derivatives``.
Other-base, logarithmic differentiation, and implicit keep structured packs with
``spec_snapshot`` / ``function_classes`` / ``effort_features`` for ML export.
Rates, definition, and inverse-function leaves keep dedicated builders.
"""

from __future__ import annotations

import random
from fractions import Fraction
from typing import Callable

from ..core.models import Question
from .calculus_pilot import _poly_display
from .utils import (
    _make_questions,
    format_linear_latex,
    format_monomial_latex,
    format_polynomial_latex,
    frac_latex,
    random_int_range,
)


def _rule_structure(settings: dict, *, generator_key: str | None = None, topic: str | None = None) -> dict:
    """Continuous derivative-rule knobs + allow-lists (topic defaults applied)."""
    from question_engine.frameworks.primitives.derivatives import derivative_rule_structure
    from question_engine.settings.params import calc_topic_structure_from_continuous

    structure = derivative_rule_structure(
        settings, generator_key=generator_key, topic=topic
    )
    structure.pop("_allow", None)
    # Merge continuous topic unlock gates when numeric D is present.
    topic_struct = calc_topic_structure_from_continuous(settings)
    if topic_struct is not None:
        for key, value in topic_struct.items():
            if key.startswith("unlock_") or key in {
                "n_max",
                "k_max",
                "interval_width_max",
                "bound_max",
            }:
                structure[key] = value
        structure.setdefault("difficulty", topic_struct["difficulty"])
    else:
        # EMH fallback unlocks from band label.
        band = str(structure.get("band", "easy"))
        structure.setdefault("unlock_medium", band != "easy")
        structure.setdefault("unlock_hard", band == "hard")
        structure.setdefault("unlock_advanced", band == "hard")
        structure.setdefault("unlock_trig", band != "easy")
        structure.setdefault("unlock_exp", band != "easy")
        structure.setdefault("unlock_log", band == "hard")
        structure.setdefault("unlock_roots", band != "easy")
        structure.setdefault("unlock_reciprocal", band != "easy")
    return structure


def _pick_family(structure: dict, easy, medium=None, hard=None, *, advanced=None, extra=None) -> str:
    from question_engine.settings.params import pick_unlocked_families

    return random.choice(
        pick_unlocked_families(
            structure, easy, medium, hard, advanced=advanced, extra=extra
        )
    )


def _allow_snapshot_from_structure(structure: dict) -> dict:
    """Copy resolved course / allow knobs into a joinable pack snapshot."""
    keys = (
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
        "coef_hi",
        "power_max",
        "term_budget",
        "band",
        "difficulty",
        "unlock_medium",
        "unlock_hard",
        "unlock_advanced",
        "unlock_trig",
        "unlock_exp",
        "unlock_log",
        "unlock_roots",
        "n_max",
        "k_max",
    )
    out: dict = {}
    for key in keys:
        if key in structure and structure[key] is not None:
            out[key] = structure[key]
    return out


def _madlibs_meta(generator_key: str, structure: dict, *, pack: str | None = None):
    """Stash ML-ready metadata for structured (non-Spec) derivative packs.

    Emits ``family`` / ``structure_id`` for gallery inventory plus
    ``function_classes``, ``methods_used``, ``effort_features``, and a
    ``spec_snapshot`` with ``pack=structured_*`` so export / rating join
    keys match Spec leaves.
    """
    last: dict = {"meta": {}}
    pack_name = pack or f"structured_{generator_key.replace('derivative_', '')}"

    def note(
        family: str,
        variant: str | None = None,
        *,
        function_classes: list[str] | tuple[str, ...] | None = None,
        methods_used: list[str] | tuple[str, ...] | None = None,
        chain_depth: int = 0,
        derivative_order: int = 1,
        shape_id: str | None = None,
    ) -> None:
        classes = list(function_classes or ["algebraic"])
        methods = list(methods_used or ["power"])
        snap = {
            "pack": pack_name,
            "family": family,
            "generator": generator_key,
            "derivative_order": int(derivative_order),
            "chain_depth": int(chain_depth),
            "function_classes": classes,
            "methods_used": methods,
            **_allow_snapshot_from_structure(structure),
        }
        if variant:
            snap["variant"] = variant
        meta: dict = {
            "generator": generator_key,
            "family": family,
            "structure_id": f"{generator_key}:{family}",
            "shape_id": shape_id or family,
            "band": structure.get("band"),
            "function_classes": classes,
            "methods_used": methods,
            "chain_depth": int(chain_depth),
            "derivative_order": int(derivative_order),
            "effective_d": structure.get("difficulty"),
            "spec_snapshot": snap,
        }
        if variant:
            meta["variant"] = variant
        last["meta"] = meta

    def metadata_builder(_p: str, _t: str, answer: str | None) -> dict:
        meta = dict(last.get("meta") or {})
        if not meta:
            return meta
        snap = dict(meta.get("spec_snapshot") or {})
        ans = answer or ""
        effort = {
            "answer_len": len(ans),
            "nest_depth": int(meta.get("chain_depth") or 0),
            "chain_applications": int(meta.get("chain_depth") or 0),
            "product_applications": int("product" in (meta.get("methods_used") or [])),
            "quotient_applications": int("quotient" in (meta.get("methods_used") or [])),
            "n_factors": 0,
            "n_terms": 1,
            "degree_max": int(structure.get("power_max") or 0),
            "coef_abs_max": int(structure.get("coef_hi") or 0),
            "has_fn_power": False,
            "derivative_order": int(meta.get("derivative_order") or 1),
            "methods": list(meta.get("methods_used") or []),
            "n_fn_nodes": sum(
                1
                for c in (meta.get("function_classes") or [])
                if c not in {"algebraic", "roots"}
            ),
            "pack": pack_name,
            "family": meta.get("family"),
        }
        meta["effort_features"] = effort
        snap.setdefault("effort_answer_len", effort["answer_len"])
        meta["spec_snapshot"] = snap
        return meta

    return note, metadata_builder



def _framework_generator(generator_key: str):
    """Build a question list via the continuous-D derivative sampler."""

    def _gen(topic: str, settings: dict) -> list[Question]:
        from question_engine.frameworks.primitives.derivatives import (
            sample_derivative_expression,
        )

        count = int(settings.get("count", 10))
        include_answer_key = bool(settings.get("include_answer_key", False))
        label = {
            "derivative_power_rule": "power rule derivative",
            "derivative_product_rule": "product rule",
            "derivative_quotient_rule": "quotient rule",
            "derivative_chain_rule": "chain rule",
            "derivative_trigonometric": "trigonometric derivative",
            "derivative_ln_exp": "ln/exp derivative",
            "derivative_other_base": "other-base derivative",
            "derivative_inverse_trig": "inverse trigonometric derivative",
            "derivative_higher_order": "higher order derivative",
            "derivative_general": "general derivative",
        }.get(generator_key, "derivative")

        def build() -> tuple[str, str, str | None]:
            sample = sample_derivative_expression(
                settings, generator_key=generator_key, topic=topic
            )
            # Stash metadata on settings for metadata_builder via closure list
            build._last_meta = sample.as_metadata()  # type: ignore[attr-defined]
            answer = sample.answer_latex if include_answer_key else None
            return sample.prompt_latex, label, answer

        def metadata_builder(prompt_latex: str, prompt_text: str, answer: str | None) -> dict:
            meta = getattr(build, "_last_meta", {}) or {}
            return dict(meta)

        return _make_questions(
            topic,
            count,
            include_answer_key,
            build,
            metadata_builder=metadata_builder,
            settings=settings,
        )

    return _gen


def _linear_pair(coef_hi: int = 5) -> tuple[int, int]:
    a = random_int_range(1, coef_hi, exclude=set())
    b = random_int_range(-coef_hi, coef_hi, exclude={0})
    return a, b


def _d_prefix(x: str, body: str) -> str:
    """Alternate d/dx vs f'(x) framing."""
    if random.choice([True, False]):
        return rf"\frac{{d}}{{d{x}}}\left[{body}\right]"
    return rf"\text{{Find }}\frac{{d}}{{d{x}}}\left({body}\right)"


def _mono(coef: int, var: str, power: int = 1) -> str:
    return format_monomial_latex(coef, variable=var, degree=power) or (
        "0" if coef == 0 else str(coef)
    )


# ---------------------------------------------------------------------------
# Power / product / quotient / chain / trig / ln-exp / invtrig (framework)
# ---------------------------------------------------------------------------


_derivative_power_rule = _framework_generator("derivative_power_rule")
_derivative_product_rule = _framework_generator("derivative_product_rule")
_derivative_quotient_rule = _framework_generator("derivative_quotient_rule")
_derivative_chain_rule = _framework_generator("derivative_chain_rule")
_derivative_trigonometric = _framework_generator("derivative_trigonometric")
_derivative_inverse_trig = _framework_generator("derivative_inverse_trig")
_derivative_ln_exp = _framework_generator("derivative_ln_exp")
_derivative_general = _framework_generator("derivative_general")
_derivative_higher_order = _framework_generator("derivative_higher_order")


# ---------------------------------------------------------------------------
# Structured packs: other-base / log-diff / implicit (+ rates / definition)
# ---------------------------------------------------------------------------


# (power/product/quotient/chain/trig/invtrig/ln_exp/higher_order → framework above)

def _derivative_other_base(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    structure = _rule_structure(settings, generator_key="derivative_other_base", topic=topic)
    coef_hi = int(structure["coef_hi"])
    x = str(settings.get("variable", "x"))
    note, metadata_builder = _madlibs_meta(
        "derivative_other_base", structure, pack="structured_other_base"
    )

    def build() -> tuple[str, str, str | None]:
        base = random.randint(2, min(5, max(2, coef_hi)))
        family = _pick_family(
            structure,
            ["a_x", "log_x"],
            medium=["a_kx", "log_linear"],
            hard=["log_power", "a_poly", "change_order"],
        )
        if family == "a_x":
            body = random.choice([rf"{base}^{{{x}}}", rf"\exp({x}\ln({base}))"])
            answer = rf"{base}^{{{x}}}\ln({base})"
            prompt = rf"\frac{{d}}{{d{x}}}\left[{base}^{{{x}}}\right]"
            _ = body
            note(family, function_classes=["exp", "algebraic"], methods_used=["power"], chain_depth=0)
        elif family == "log_x":
            prompt = rf"\frac{{d}}{{d{x}}}\log_{{{base}}}({x})"
            answer = rf"\frac{{1}}{{{x}\ln({base})}}"
            note(family, function_classes=["log", "algebraic"], methods_used=["power"], chain_depth=0)
        elif family == "a_kx":
            k = random.randint(2, max(2, min(5, coef_hi)))
            arg = random.choice([f"{k}{x}", rf"{k}\cdot {x}"])
            prompt = rf"\frac{{d}}{{d{x}}}{base}^{{{arg}}}"
            answer = rf"{k}{base}^{{{k}{x}}}\ln({base})"
            note(
                family,
                function_classes=["exp", "algebraic"],
                methods_used=["chain"],
                chain_depth=1,
            )
        elif family == "log_linear":
            a, b = _linear_pair(min(3, coef_hi))
            inner = format_linear_latex(a, b, variable=x)
            prompt = rf"\frac{{d}}{{d{x}}}\log_{{{base}}}({inner})"
            answer = rf"\frac{{{a}}}{{\left({inner}\right)\ln({base})}}"
            note(
                family,
                function_classes=["log", "algebraic"],
                methods_used=["chain"],
                chain_depth=1,
            )
        elif family == "log_power":
            k = random.randint(2, max(2, min(4, coef_hi)))
            body = random.choice(
                [rf"\log_{{{base}}}({x}^{{{k}}})", rf"{k}\log_{{{base}}}({x})"]
            )
            prompt = rf"\frac{{d}}{{d{x}}}\left[{body}\right]"
            answer = rf"\frac{{{k}}}{{{x}\ln({base})}}"
            note(
                family,
                function_classes=["log", "algebraic"],
                methods_used=["chain", "power"],
                chain_depth=1,
            )
        elif family == "a_poly":
            prompt = rf"\frac{{d}}{{d{x}}}{base}^{{{x}^{{2}}}}"
            answer = rf"2{x}{base}^{{{x}^{{2}}}}\ln({base})"
            note(
                family,
                function_classes=["exp", "algebraic"],
                methods_used=["chain"],
                chain_depth=1,
            )
        else:
            prompt = rf"\frac{{d}}{{d{x}}}\left[{x}\cdot {base}^{{{x}}}\right]"
            answer = rf"{base}^{{{x}}}+{x}{base}^{{{x}}}\ln({base})"
            note(
                family,
                function_classes=["exp", "algebraic"],
                methods_used=["product"],
                chain_depth=0,
            )
        return prompt, "other-base log/exp derivative", answer if include_answer_key else None

    return _make_questions(
        topic, count, include_answer_key, build, metadata_builder=metadata_builder, settings=settings
    )


def _derivative_logarithmic(topic: str, settings: dict) -> list[Question]:
    """Logarithmic differentiation (not plain ln/exp rules)."""
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    structure = _rule_structure(settings, generator_key="derivative_logarithmic", topic=topic)
    x = str(settings.get("variable", "x"))
    note, metadata_builder = _madlibs_meta(
        "derivative_logarithmic", structure, pack="structured_logarithmic"
    )

    def build() -> tuple[str, str, str | None]:
        extra = []
        if structure.get("allow_trig") or structure.get("unlock_trig"):
            extra.append("trig_x")
        family = _pick_family(
            structure,
            ["power"],
            medium=["product_powers", "quotient_powers", "root"],
            hard=["x_x", "a_x_x"],
            extra=extra if structure.get("unlock_hard") else None,
        )
        log_methods = ["logarithmic"]
        if family == "power":
            n = random.randint(2, max(2, min(5, int(structure.get("power_max", 5)))))
            body = f"{x}^{{{n}}}"
            prompt = (
                rf"\text{{Use logarithmic differentiation to find }}"
                rf"\frac{{d}}{{d{x}}}\left[{body}\right]."
            )
            answer = rf"{n}{x}^{{{n - 1}}}"
            note(
                family,
                function_classes=["algebraic"],
                methods_used=log_methods + ["power"],
                chain_depth=0,
            )
        elif family == "product_powers":
            n = random.randint(2, 4)
            m = random.randint(2, 4)
            body = rf"{x}^{{{n}}}({x}+1)^{{{m}}}"
            prompt = (
                rf"\text{{Use logarithmic differentiation: }}"
                rf"y={body}.\ \text{{Find }}y'."
            )
            answer = (
                rf"{x}^{{{n}}}({x}+1)^{{{m}}}"
                rf"\left(\frac{{{n}}}{{{x}}}+\frac{{{m}}}{{{x}+1}}\right)"
            )
            note(
                family,
                function_classes=["algebraic"],
                methods_used=log_methods + ["product", "power"],
                chain_depth=0,
            )
        elif family == "quotient_powers":
            n = random.randint(2, 4)
            body = rf"\frac{{{x}^{{{n}}}}}{{{x}+1}}"
            prompt = (
                rf"\text{{Use logarithmic differentiation: }}"
                rf"y={body}.\ \text{{Find }}y'."
            )
            answer = (
                rf"\frac{{{x}^{{{n}}}}}{{{x}+1}}"
                rf"\left(\frac{{{n}}}{{{x}}}-\frac{{1}}{{{x}+1}}\right)"
            )
            note(
                family,
                function_classes=["algebraic"],
                methods_used=log_methods + ["quotient", "power"],
                chain_depth=0,
            )
        elif family == "root":
            body = rf"\sqrt{{{x}({x}+1)}}"
            prompt = (
                rf"\text{{Use logarithmic differentiation: }}"
                rf"y={body}.\ \text{{Find }}y'."
            )
            answer = (
                rf"\sqrt{{{x}({x}+1)}}"
                rf"\cdot\frac{{1}}{{2}}\left(\frac{{1}}{{{x}}}+\frac{{1}}{{{x}+1}}\right)"
            )
            note(
                family,
                function_classes=["roots", "algebraic"],
                methods_used=log_methods + ["product", "chain"],
                chain_depth=1,
            )
        elif family == "x_x":
            body = rf"{x}^{{{x}}}"
            prompt = (
                rf"\text{{Use logarithmic differentiation: }}"
                rf"y={body}.\ \text{{Find }}y'."
            )
            answer = rf"{x}^{{{x}}}\left(\ln({x})+1\right)"
            note(
                family,
                function_classes=["exp", "log", "algebraic"],
                methods_used=log_methods + ["chain"],
                chain_depth=1,
            )
        elif family == "a_x_x":
            body = rf"({x}+1)^{{{x}}}"
            prompt = (
                rf"\text{{Use logarithmic differentiation: }}"
                rf"y={body}.\ \text{{Find }}y'."
            )
            answer = (
                rf"({x}+1)^{{{x}}}"
                rf"\left(\ln({x}+1)+\frac{{{x}}}{{{x}+1}}\right)"
            )
            note(
                family,
                function_classes=["exp", "log", "algebraic"],
                methods_used=log_methods + ["chain"],
                chain_depth=1,
            )
        else:
            body = rf"\left(\sin({x})\right)^{{{x}}}"
            prompt = (
                rf"\text{{Use logarithmic differentiation: }}"
                rf"y={body}.\ \text{{Find }}y'."
            )
            answer = (
                rf"\left(\sin({x})\right)^{{{x}}}"
                rf"\left(\ln(\sin({x}))+{x}\cot({x})\right)"
            )
            note(
                family,
                function_classes=["trig", "exp", "log", "algebraic"],
                methods_used=log_methods + ["chain"],
                chain_depth=1,
            )
        return prompt, "logarithmic differentiation", answer if include_answer_key else None

    return _make_questions(
        topic, count, include_answer_key, build, metadata_builder=metadata_builder, settings=settings
    )


def _derivative_implicit(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    structure = _rule_structure(settings, generator_key="derivative_implicit", topic=topic)
    x = str(settings.get("variable", "x"))
    note, metadata_builder = _madlibs_meta(
        "derivative_implicit", structure, pack="structured_implicit"
    )

    def build() -> tuple[str, str, str | None]:
        a = random.randint(1, max(1, min(4, int(structure["coef_hi"]))))
        extra = []
        if structure.get("allow_trig") or structure.get("unlock_trig"):
            extra.append("trig")
        if structure.get("allow_exp") or structure.get("unlock_exp"):
            extra.append("exp_y")
        family = _pick_family(
            structure,
            ["circle"],
            medium=["xy_term", "ellipse", "line_prod"],
            hard=["cubes"],
            extra=extra if structure.get("unlock_hard") else None,
        )
        if family == "circle":
            eq = random.choice(
                [rf"{x}^{{2}}+y^{{2}}={a}", rf"y^{{2}}+{x}^{{2}}={a}"]
            )
            answer = rf"\frac{{dy}}{{d{x}}}=-\frac{{{x}}}{{y}}"
            note(
                family,
                function_classes=["algebraic"],
                methods_used=["implicit", "power"],
                chain_depth=0,
            )
        elif family == "xy_term":
            eq = random.choice(
                [rf"{x}^{{2}}+{x}y={a}", rf"{x}y+{x}^{{2}}={a}"]
            )
            answer = rf"\frac{{dy}}{{d{x}}}=-\frac{{2{x}+y}}{{{x}}}"
            note(
                family,
                function_classes=["algebraic"],
                methods_used=["implicit", "product", "power"],
                chain_depth=0,
            )
        elif family == "ellipse":
            b = random.randint(2, max(2, min(5, int(structure["coef_hi"]))))
            eq = rf"{b}{x}^{{2}}+y^{{2}}={a}"
            answer = rf"\frac{{dy}}{{d{x}}}=-\frac{{{2 * b}{x}}}{{y}}"
            note(
                family,
                function_classes=["algebraic"],
                methods_used=["implicit", "power"],
                chain_depth=0,
            )
        elif family == "line_prod":
            eq = rf"{x}y={a}"
            answer = rf"\frac{{dy}}{{d{x}}}=-\frac{{y}}{{{x}}}"
            note(
                family,
                function_classes=["algebraic"],
                methods_used=["implicit", "product"],
                chain_depth=0,
            )
        elif family == "cubes":
            eq = random.choice(
                [rf"{x}^{{3}}+y^{{3}}={a}", rf"y^{{3}}+{x}^{{3}}={a}"]
            )
            answer = rf"\frac{{dy}}{{d{x}}}=-\frac{{{x}^{{2}}}}{{y^{{2}}}}"
            note(
                family,
                function_classes=["algebraic"],
                methods_used=["implicit", "power"],
                chain_depth=0,
            )
        elif family == "trig":
            eq = rf"\sin({x})+\cos(y)=0"
            answer = rf"\frac{{dy}}{{d{x}}}=\frac{{\cos({x})}}{{\sin(y)}}"
            note(
                family,
                function_classes=["trig", "algebraic"],
                methods_used=["implicit", "chain"],
                chain_depth=1,
            )
        else:
            eq = rf"e^{{y}}+{x}={a}"
            answer = rf"\frac{{dy}}{{d{x}}}=-e^{{-y}}"
            note(
                family,
                function_classes=["exp", "algebraic"],
                methods_used=["implicit", "chain"],
                chain_depth=1,
            )
        prompt = (
            rf"\text{{Differentiate implicitly: }}{eq}."
            rf"\text{{ Solve for }}\frac{{dy}}{{d{x}}}."
        )
        return prompt, "implicit differentiation", answer if include_answer_key else None

    return _make_questions(
        topic, count, include_answer_key, build, metadata_builder=metadata_builder, settings=settings
    )


# ---------------------------------------------------------------------------
# Rates + definition + inverse functions (stubs / enrichment)
# ---------------------------------------------------------------------------


def _average_rate_of_change(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    structure = _rule_structure(settings)
    x = str(settings.get("variable", "x"))
    note, metadata_builder = _madlibs_meta("average_rate_of_change", structure)

    def build() -> tuple[str, str, str | None]:
        a0 = random.randint(0, 3)
        width_max = max(1, int(structure.get("interval_width_max", 4)))
        width = random.randint(1, max(1, min(4, width_max)))
        if structure.get("unlock_medium"):
            width = random.randint(1, max(1, min(5, width_max)))
        b0 = a0 + width
        extra = []
        if structure.get("unlock_reciprocal"):
            extra.append("reciprocal")
        family = _pick_family(
            structure,
            ["quad"],
            medium=["cubic", "quad_const", "linear"],
            hard=["poly", "shifted"],
            extra=extra if structure.get("unlock_hard") else None,
        )
        note(family)
        a, b = a0, b0
        if family == "quad":
            f = f"{x}^{{2}}"
            fa, fb = a0 * a0, b0 * b0
        elif family == "cubic":
            k = random.randint(1, 3)
            f = _mono(k, x, 3)
            fa, fb = k * a**3, k * b**3
        elif family == "quad_const":
            p = random.randint(1, 3)
            q = random_int_range(-4, 4, exclude={0})
            f = _poly_display([p, 0, q], x)
            fa, fb = p * a * a + q, p * b * b + q
        elif family == "linear":
            m = random_int_range(-5, 5, exclude={0})
            c = random.randint(-3, 3)
            f = format_linear_latex(m, c, variable=x)
            fa, fb = m * a + c, m * b + c
        elif family == "reciprocal":
            a = random.randint(1, 3)
            b = a + random.randint(1, 3)
            f = random.choice([rf"\frac{{1}}{{{x}}}", rf"{x}^{{-1}}"])
            fa, fb = Fraction(1, a), Fraction(1, b)
        elif family == "shifted":
            f = rf"{x}^{{3}}+{x}"
            fa, fb = a**3 + a, b**3 + b
        else:
            p = random.randint(1, 2)
            q = random_int_range(-3, 3, exclude={0})
            r = random.randint(-2, 2)
            f = _poly_display([p, q, r], x)
            fa = p * a * a + q * a + r
            fb = p * b * b + q * b + r
        rate = Fraction(fb - fa, b - a)
        prompt = (
            rf"\text{{Find the average rate of change of }}f({x})={f}"
            rf"\text{{ on }}[{a},{b}]."
        )
        return prompt, "average rate of change", (
            frac_latex(rate) if include_answer_key else None
        )

    return _make_questions(
        topic, count, include_answer_key, build, metadata_builder=metadata_builder, settings=settings
    )


def _instantaneous_rate_of_change(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    structure = _rule_structure(settings)
    x = str(settings.get("variable", "x"))
    note, metadata_builder = _madlibs_meta("instantaneous_rate_of_change", structure)

    def build() -> tuple[str, str, str | None]:
        a = random.randint(1, max(1, min(4, int(structure.get("n_max", 4)))))
        extra = []
        if structure.get("allow_trig") or structure.get("unlock_trig"):
            extra.append("trig")
        if structure.get("allow_exp") or structure.get("unlock_exp"):
            extra.append("exp")
        family = _pick_family(
            structure,
            ["power"],
            medium=["poly", "sqrt", "reciprocal"],
            hard=["cubic"],
            extra=extra if structure.get("unlock_hard") else None,
        )
        note(family)
        if family == "power":
            n = random.randint(2, max(2, min(4, int(structure.get("power_max", 4)))))
            f = f"{x}^{{{n}}}"
            answer = str(n * a ** (n - 1))
        elif family == "poly":
            p = random.randint(1, 3)
            q = random_int_range(-4, 4, exclude={0})
            f = _poly_display([p, 0, q], x)
            answer = str(2 * p * a)
        elif family == "sqrt":
            a = random.choice([1, 4, 9])
            f = random.choice([rf"\sqrt{{{x}}}", rf"{x}^{{1/2}}"])
            answer = frac_latex(Fraction(1, 2 * int(a**0.5)))
        elif family == "reciprocal":
            a = random.randint(1, 4)
            f = random.choice([rf"\frac{{1}}{{{x}}}", rf"{x}^{{-1}}"])
            answer = frac_latex(Fraction(-1, a * a))
        elif family == "trig":
            a = 0
            f = random.choice([rf"\sin({x})", rf"\cos({x})"])
            answer = "1" if "sin" in f else "0"
        elif family == "exp":
            a = 0
            k = random.randint(1, max(1, min(3, int(structure.get("k_max", 3)))))
            f = rf"e^{{{k}{x}}}" if k != 1 else rf"e^{{{x}}}"
            answer = str(k)
        else:
            p = random.randint(1, 2)
            q = random_int_range(-3, 3, exclude={0})
            f = _poly_display([p, 0, q, 0], x)
            answer = str(3 * p * a * a + q)
        prompt = (
            rf"\text{{Find the instantaneous rate of change of }}"
            rf"f({x})={f}\text{{ at }}{x}={a}."
        )
        return prompt, "instantaneous rate of change", (
            answer if include_answer_key else None
        )

    return _make_questions(
        topic, count, include_answer_key, build, metadata_builder=metadata_builder, settings=settings
    )


def _definition_of_derivative(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    structure = _rule_structure(settings)
    x = str(settings.get("variable", "x"))
    note, metadata_builder = _madlibs_meta("definition_of_derivative", structure)

    def build() -> tuple[str, str, str | None]:
        a = random.randint(1, max(1, min(5, int(structure.get("n_max", 5)))))
        family = _pick_family(
            structure,
            ["limit_h", "limit_x"],
            medium=["cube", "linear_coef", "named"],
            hard=["reciprocal", "sqrt", "poly"],
        )
        note(family)
        if family == "limit_h":
            prompt = rf"\lim_{{h\to 0}}\frac{{({a}+h)^{{2}}-{a * a}}}{{h}}"
            answer = str(2 * a)
        elif family == "limit_x":
            prompt = rf"\lim_{{{x}\to {a}}}\frac{{{x}^{{2}}-{a * a}}}{{{x}-{a}}}"
            answer = str(2 * a)
        elif family == "cube":
            prompt = rf"\lim_{{h\to 0}}\frac{{({a}+h)^{{3}}-{a ** 3}}}{{h}}"
            answer = str(3 * a * a)
        elif family == "linear_coef":
            k = random.randint(2, max(2, min(4, int(structure.get("k_max", 4)))))
            prompt = rf"\lim_{{h\to 0}}\frac{{{k}({a}+h)^{{2}}-{k * a * a}}}{{h}}"
            answer = str(2 * k * a)
        elif family == "named":
            k = random.randint(2, max(2, min(4, int(structure.get("k_max", 4)))))
            prompt = (
                rf"\text{{Use the definition to find }}f'({a})"
                rf"\text{{ for }}f({x})={k}{x}^{{2}}."
            )
            answer = str(2 * k * a)
        elif family == "reciprocal":
            prompt = (
                rf"\lim_{{h\to 0}}\frac{{\frac{{1}}{{{a}+h}}-\frac{{1}}{{{a}}}}}{{h}}"
            )
            answer = frac_latex(Fraction(-1, a * a))
        elif family == "sqrt":
            a = random.choice([1, 4, 9])
            prompt = (
                rf"\lim_{{h\to 0}}\frac{{\sqrt{{{a}+h}}-\sqrt{{{a}}}}}{{h}}"
            )
            answer = frac_latex(Fraction(1, 2 * int(a**0.5)))
        else:
            p = random.randint(1, 3)
            q = random_int_range(-3, 3, exclude={0})
            f = _poly_display([p, 0, q], x)
            prompt = (
                rf"\text{{Use the definition to find }}f'({a})"
                rf"\text{{ for }}f({x})={f}."
            )
            answer = str(2 * p * a)
        return prompt, "definition of the derivative", (
            answer if include_answer_key else None
        )

    return _make_questions(
        topic, count, include_answer_key, build, metadata_builder=metadata_builder, settings=settings
    )


def _derivative_inverse_functions(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    structure = _rule_structure(settings)
    x = str(settings.get("variable", "x"))
    note, metadata_builder = _madlibs_meta("derivative_inverse_functions", structure)

    def build() -> tuple[str, str, str | None]:
        family = _pick_family(
            structure,
            ["power"],
            medium=["power_med", "table", "linear"],
            hard=["exp", "ln", "cubic"],
        )
        note(family)
        if family in {"power", "power_med"}:
            n = random.randint(2, 4 if family == "power" else 3)
            a = random.randint(1, 3 if family == "power" else 2)
            fp = n * a ** (n - 1)
            prompt = (
                rf"f({x})={x}^{{{n}}};\quad f'({a})={fp}."
                rf"\quad\text{{Find }}(f^{{-1}})'({a ** n})."
            )
            answer = frac_latex(Fraction(1, fp))
        elif family == "table":
            b = random.randint(1, 5)
            y = random.randint(2, 8)
            fp = random_int_range(-6, 6, exclude={0})
            prompt = (
                rf"f({b})={y},\ f'({b})={fp}."
                rf"\quad\text{{Find }}(f^{{-1}})'({y})."
            )
            answer = frac_latex(Fraction(1, fp))
        elif family == "linear":
            m = random.randint(2, 5)
            c = random.randint(-3, 3)
            prompt = (
                rf"f({x})={format_linear_latex(m, c, variable=x)}."
                rf"\quad\text{{Find }}(f^{{-1}})'({x})."
            )
            answer = frac_latex(Fraction(1, m))
        elif family == "exp":
            prompt = (
                rf"f({x})=e^{{{x}}};\quad f(0)=1,\ f'(0)=1."
                rf"\quad\text{{Find }}(f^{{-1}})'(1)."
            )
            answer = "1"
        elif family == "ln":
            prompt = (
                rf"f({x})=\ln({x});\quad f(e)=1,\ f'(e)=\frac{{1}}{{e}}."
                rf"\quad\text{{Find }}(f^{{-1}})'(1)."
            )
            answer = "e"
        else:
            a = random.randint(1, 2)
            fp = 3 * a * a + 1
            y = a**3 + a
            prompt = (
                rf"f({x})={x}^{{3}}+{x};\quad f'({a})={fp}."
                rf"\quad\text{{Find }}(f^{{-1}})'({y})."
            )
            answer = frac_latex(Fraction(1, fp))
        return prompt, "inverse function derivative", (
            answer if include_answer_key else None
        )

    return _make_questions(
        topic, count, include_answer_key, build, metadata_builder=metadata_builder, settings=settings
    )


GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = {
    "derivative_power_rule": _derivative_power_rule,
    "derivative_product_rule": _derivative_product_rule,
    "derivative_quotient_rule": _derivative_quotient_rule,
    "derivative_chain_rule": _derivative_chain_rule,
    "derivative_trigonometric": _derivative_trigonometric,
    "derivative_inverse_trig": _derivative_inverse_trig,
    "derivative_ln_exp": _derivative_ln_exp,
    "derivative_general": _derivative_general,
    "derivative_other_base": _derivative_other_base,
    "derivative_logarithmic": _derivative_logarithmic,
    "derivative_implicit": _derivative_implicit,
    "derivative_higher_order": _derivative_higher_order,
    "average_rate_of_change": _average_rate_of_change,
    "instantaneous_rate_of_change": _instantaneous_rate_of_change,
    "definition_of_derivative": _definition_of_derivative,
    "derivative_inverse_functions": _derivative_inverse_functions,
}
