"""Pilot calculus generators emphasizing expression ordering + function variety.

These replace thin ``calculus_foundations`` stubs for a small set of topics so
we can review sample quality before wiring the full remaining stub list.
Patterns generalized from OpenStax Calculus Vol. 1 §§3.1, 4.2, 5.5–5.6.
"""

from __future__ import annotations

import random
from fractions import Fraction
from typing import Callable

from ..core.models import Question
from .utils import (
    _make_questions,
    format_linear_latex,
    format_polynomial_latex,
    frac_latex,
    random_int_range,
)


def _difficulty_tier(settings: dict) -> str:
    """Map continuous ``difficulty`` or legacy EMH tier to easy|medium|hard."""
    from question_engine.frameworks.difficulty_budget import settings_difficulty_band

    return settings_difficulty_band(settings, default=8.0)


def _pilot_structure(settings: dict) -> dict:
    """Reuse derivative-rule continuous unlocks for pilot function-class pools."""
    from question_engine.frameworks.primitives.derivatives import derivative_rule_structure

    structure = derivative_rule_structure(settings)
    structure.pop("_allow", None)
    return structure


def _structure_unlocks(structure: dict) -> list[str]:
    """Active continuous-D unlock knobs (for gallery structure inventory)."""
    return [
        key
        for key in (
            "allow_trig",
            "allow_exp",
            "allow_ln",
            "allow_nested",
            "allow_roots",
            "allow_invtrig",
        )
        if structure.get(key)
    ]


def _family_structure_meta(
    family: str,
    *,
    generator: str,
    structure: dict,
    variant: str | None = None,
) -> dict:
    """Lightweight live structure fingerprint for topic-fit galleries + ML."""
    classes = ["algebraic"]
    if family in {"trig"} or (variant and variant in {"sin", "cos", "tan"}):
        classes = ["trig"]
    elif family in {"exp", "chain_exp"}:
        classes = ["exp"]
    elif family == "ln":
        classes = ["log"]
    elif family == "radical":
        classes = ["algebraic", "roots"]
    methods = ["differential"]
    if family in {"product"}:
        methods.append("product")
    if family in {"quotient"}:
        methods.append("quotient")
    if family in {"chain_exp"}:
        methods.append("chain")
    snap = {
        "pack": f"structured_{generator}",
        "family": family,
        "generator": generator,
        "function_classes": classes,
        "methods_used": methods,
        "allow_trig": bool(structure.get("allow_trig")),
        "allow_exp": bool(structure.get("allow_exp")),
        "allow_log": bool(structure.get("allow_ln") or structure.get("allow_log")),
        "allow_roots": bool(structure.get("allow_roots")),
    }
    if variant:
        snap["variant"] = variant
    meta: dict = {
        "family": family,
        "structure_id": f"{generator}:{family}",
        "band": structure.get("band"),
        "upgrades_applied": _structure_unlocks(structure),
        "function_classes": classes,
        "methods_used": methods,
        "effective_d": structure.get("difficulty"),
        "spec_snapshot": snap,
        "effort_features": {
            "family": family,
            "pack": snap["pack"],
            "n_terms": 1,
            "methods": methods,
            "n_fn_nodes": sum(1 for c in classes if c not in {"algebraic", "roots"}),
        },
    }
    if variant:
        meta["variant"] = variant
    return meta


# ---------------------------------------------------------------------------
# Linear approximations / local linearization (OpenStax 4.2)
# ---------------------------------------------------------------------------


def _linear_approx_families(structure: dict) -> list[str]:
    """Leftover bands (easy √x / x²; lock out x² at high D; D=22 reciprocal/exp)."""
    from question_engine.frameworks.primitives.calc_app_diff import (
        linear_approx_forms_for_difficulty,
    )

    d = float(structure.get("difficulty", 8.0))
    return list(linear_approx_forms_for_difficulty(d))


def _linear_approximation(topic: str, settings: dict) -> list[Question]:
    """Delegate to leftover-lockout sampler (same builders, exclusive bands)."""
    from question_engine.frameworks.primitives.calc_app_diff import (
        LINEAR_APPROX_GENERATOR,
        sample_linear_approximation,
    )

    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        item = sample_linear_approximation(random, settings)
        fid = item.form_id
        snap = item.metadata.get("spec_snapshot")
        build._last_meta = {  # type: ignore[attr-defined]
            **item.metadata,
            "form_id": fid,
            "family": fid,
            "generator": LINEAR_APPROX_GENERATOR,
            "structure_id": f"{LINEAR_APPROX_GENERATOR}:{fid}",
            "spec_snapshot": {
                **(snap if isinstance(snap, dict) else {}),
                "form_id": fid,
                "family": fid,
                "generator": LINEAR_APPROX_GENERATOR,
            },
        }
        answer = item.answer_latex if include_answer_key else None
        return item.prompt_latex, item.label, answer

    def metadata_builder(_p: str, _t: str, _a: str | None) -> dict:
        return dict(getattr(build, "_last_meta", {}) or {})

    return _make_questions(
        topic,
        count,
        include_answer_key,
        build,
        metadata_builder=metadata_builder,
        settings=settings,
    )


def _poly_display(coeffs: list[int], variable: str, *, style: str | None = None) -> str:
    """Render a polynomial with alternate term orderings / factorizations."""
    style = style or random.choice(["standard", "reversed", "factored_linear"])
    standard = format_polynomial_latex(coeffs, variable=variable)
    if style == "standard":
        return standard

    # Dense coeffs: [a_n, ..., a_0]
    terms: list[tuple[int, int]] = []
    deg = len(coeffs) - 1
    for i, c in enumerate(coeffs):
        if c:
            terms.append((c, deg - i))

    if style == "reversed" and len(terms) >= 2:
        # Low degree first: e.g. 3 + 2x + x^2
        parts: list[str] = []
        for i, (c, p) in enumerate(sorted(terms, key=lambda t: t[1])):
            if p == 0:
                piece = str(c)
            elif p == 1:
                if c == 1:
                    piece = variable
                elif c == -1:
                    piece = f"-{variable}"
                else:
                    piece = f"{c}{variable}"
            else:
                if c == 1:
                    piece = f"{variable}^{{{p}}}"
                elif c == -1:
                    piece = f"-{variable}^{{{p}}}"
                else:
                    piece = f"{c}{variable}^{{{p}}}"
            if i == 0:
                parts.append(piece)
            elif piece.startswith("-"):
                parts.append(f" - {piece[1:]}")
            else:
                parts.append(f" + {piece}")
        return "".join(parts)

    # Factored-ish for quadratics like x^2 + bx = x(x+b) when constant is 0
    if (
        style == "factored_linear"
        and len(coeffs) == 3
        and coeffs[0] == 1
        and coeffs[2] == 0
        and coeffs[1] != 0
    ):
        inner = format_linear_latex(1, coeffs[1], variable=variable)
        return rf"{variable}\left({inner}\right)"

    return standard


def _point_eval_poly(coeffs: list[int], a: int) -> int:
    value = 0
    for c in coeffs:
        value = value * a + c
    return value


def _deriv_coeffs(coeffs: list[int]) -> list[int]:
    deg = len(coeffs) - 1
    if deg <= 0:
        return [0]
    out = []
    for i, c in enumerate(coeffs[:-1]):
        power = deg - i
        out.append(c * power)
    return out if any(out) else [0]


# ---------------------------------------------------------------------------
# Pilot 1: tangent / normal lines (OpenStax 3.1: f=x^2, f=1/x, poly)
# ---------------------------------------------------------------------------


def _tangent_families(structure: dict) -> list[str]:
    """Leftover bands (easy mix; lock out poly/trig/exp/ln at high D; D=22 nested/cubic)."""
    from question_engine.frameworks.primitives.calc_app_diff import (
        tangent_forms_for_difficulty,
    )

    d = float(structure.get("difficulty", 8.0))
    return list(tangent_forms_for_difficulty(d))


def _tangent_sketch_meta(
    prompt_latex: str, settings: dict, last_meta: dict
) -> dict:
    from question_engine.diagrams.figure_families import sample_figure_from_settings

    features = ["curve", "point", "label_point"]
    low = (prompt_latex or "").lower()
    if "normal" in low:
        features.append("normal")
    else:
        features.append("tangent")
    curve_kind = "parabola"
    if r"\frac{1}{" in (prompt_latex or "") or "^{-1}" in (prompt_latex or ""):
        curve_kind = "reciprocal"
    elif r"\sin" in (prompt_latex or "") or r"\cos" in (prompt_latex or ""):
        curve_kind = "sine"
    elif r"e^{" in (prompt_latex or ""):
        curve_kind = "exp"
    elif r"\sqrt" in (prompt_latex or ""):
        curve_kind = "abs_linear"
    sample = sample_figure_from_settings(
        "function_sketch",
        settings,
        features=features,
        curve_kind=curve_kind,
    )
    return {**(last_meta or {}), **sample.to_metadata_extras()}


def _tangent_normal_line(topic: str, settings: dict) -> list[Question]:
    """Delegate to leftover-lockout sampler (same builders, exclusive bands)."""
    from question_engine.frameworks.primitives.calc_app_diff import (
        TANGENT_GENERATOR,
        sample_tangent_normal_line,
    )

    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        item = sample_tangent_normal_line(random, settings)
        fid = item.form_id
        snap = item.metadata.get("spec_snapshot")
        build._last_meta = {  # type: ignore[attr-defined]
            **item.metadata,
            "form_id": fid,
            "family": fid,
            "generator": TANGENT_GENERATOR,
            "structure_id": f"{TANGENT_GENERATOR}:{fid}",
            "spec_snapshot": {
                **(snap if isinstance(snap, dict) else {}),
                "form_id": fid,
                "family": fid,
                "generator": TANGENT_GENERATOR,
            },
        }
        answer = item.answer_latex if include_answer_key else None
        return item.prompt_latex, item.label, answer

    def metadata_builder(prompt_latex: str, _t: str, _a: str | None) -> dict:
        return _tangent_sketch_meta(
            prompt_latex, settings, dict(getattr(build, "_last_meta", {}) or {})
        )

    return _make_questions(
        topic,
        count,
        include_answer_key,
        build,
        metadata_builder=metadata_builder,
        settings=settings,
    )


# ---------------------------------------------------------------------------
# Pilot 2: differentials (OpenStax 4.2 Ex 4.8: y=x^2+2x and y=cos x)
# ---------------------------------------------------------------------------


def _differential_families(structure: dict) -> list[str]:
    """Leftover bands (easy mix; lock out log/power at high D; D=22 nested only)."""
    from question_engine.frameworks.primitives.calc_app_diff import (
        differential_forms_for_difficulty,
    )

    d = float(structure.get("difficulty", 8.0))
    return list(differential_forms_for_difficulty(d))


def _differentials(topic: str, settings: dict) -> list[Question]:
    """Delegate to leftover-lockout sampler (same builders, exclusive bands)."""
    from question_engine.frameworks.primitives.calc_app_diff import (
        DIFFERENTIALS_GENERATOR,
        sample_differentials,
    )

    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        item = sample_differentials(random, settings)
        fid = item.form_id
        snap = item.metadata.get("spec_snapshot")
        build._last_meta = {  # type: ignore[attr-defined]
            **item.metadata,
            "form_id": fid,
            "family": fid,
            "generator": DIFFERENTIALS_GENERATOR,
            "structure_id": f"{DIFFERENTIALS_GENERATOR}:{fid}",
            "spec_snapshot": {
                **(snap if isinstance(snap, dict) else {}),
                "form_id": fid,
                "family": fid,
                "generator": DIFFERENTIALS_GENERATOR,
            },
        }
        answer = item.answer_latex if include_answer_key else None
        return item.prompt_latex, item.label, answer

    def metadata_builder(_p: str, _t: str, _a: str | None) -> dict:
        return dict(getattr(build, "_last_meta", {}) or {})

    return _make_questions(
        topic,
        count,
        include_answer_key,
        build,
        metadata_builder=metadata_builder,
        settings=settings,
    )


# ---------------------------------------------------------------------------
# Pilot 3: log/exp with substitution (OpenStax 5.5–5.6)
# ---------------------------------------------------------------------------


def _integral_sub_families(structure: dict) -> list[str]:
    d = float(structure.get("difficulty", 8.0))
    families = ["plain_exp", "exp_linear", "reciprocal_linear"]
    if d >= 5.0:
        families.append("log_du_over_u")
    if d >= 7.0:
        families.extend(["exp_chain_poly", "exp_over_one_plus_exp"])
    if d >= 12.0:
        families.extend(["log_du_over_u_reordered", "mixed_rewrite"])
    return families


def _integral_log_exp_substitution(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    structure = _pilot_structure(settings)
    tier = str(structure["band"])
    x = str(settings.get("variable", "x"))
    last: dict = {"meta": {}}

    def build() -> tuple[str, str, str | None]:
        family = random.choice(_integral_sub_families(structure))
        variant: str | None = None

        if family == "plain_exp":
            # OpenStax 5.37: ∫ e^{-x} dx — also e^{kx}
            k = random.choice([-1, 1, 2, 3, -2])
            variant = f"k{k}"
            if k == 1:
                integrand = rf"e^{{{x}}}"
                answer = rf"e^{{{x}}}+C"
            elif k == -1:
                integrand = random.choice([rf"e^{{-{x}}}", rf"e^{{(-1){x}}}"])
                answer = rf"-e^{{-{x}}}+C"
            else:
                integrand = rf"e^{{{k}{x}}}"
                answer = rf"\frac{{1}}{{{k}}}e^{{{k}{x}}}+C"
        elif family == "exp_linear":
            a = random.randint(2, 5)
            b = random_int_range(-4, 4, exclude={0})
            # ∫ e^{ax+b} dx — standard ax+b vs constant-first b+ax
            std = format_linear_latex(a, b, variable=x)
            if random.choice([True, False]):
                exponent = std
                variant = "ax+b"
            else:
                mono = format_monomial_safe(a, x)
                exponent = f"{b}+{mono}" if b > 0 else f"{b}+{mono}"
                variant = "b+ax"
            integrand = rf"e^{{{exponent}}}"
            answer = rf"\frac{{1}}{{{a}}}e^{{{std}}}+C"
        elif family == "reciprocal_linear":
            # ∫ 1/(ax+b) dx = (1/a) ln|ax+b|
            a = random.randint(1, 5)
            b = random_int_range(-5, 5, exclude={0})
            inner = format_linear_latex(a, b, variable=x)
            form = random.choice(["frac", "recip_power", "reversed_inner"])
            variant = form
            if form == "frac":
                integrand = rf"\frac{{1}}{{{inner}}}"
            elif form == "recip_power":
                integrand = rf"\left({inner}\right)^{{-1}}"
            else:
                mono = format_monomial_safe(a, x)
                inner_rev = f"{b}+{mono}"
                integrand = rf"\frac{{1}}{{{inner_rev}}}"
            if a == 1:
                answer = rf"\ln\left|{inner}\right|+C"
            else:
                answer = rf"\frac{{1}}{{{a}}}\ln\left|{inner}\right|+C"
        elif family == "log_du_over_u":
            # ∫ 2x/(x^2+1) dx = ln|x^2+1|
            # orderings: 2x/(x^2+1), (x^2+1)^{-1}·2x, left-multiplied inverse
            c = random.randint(1, 4)
            # ∫ n x^{n-1} / (x^n + c)  or specifically 2x/(x^2+c)
            power = random.choice([2, 3]) if tier != "easy" else 2
            coef = power  # so du matches
            den = rf"{x}^{{{power}}}+{c}"
            form = random.choice(["frac", "right_mul", "left_mul"])
            variant = form
            if form == "frac":
                integrand = rf"\frac{{{coef}{x}^{{{power - 1}}}}}{{{den}}}"
            elif form == "right_mul":
                integrand = rf"{coef}{x}^{{{power - 1}}}\left({den}\right)^{{-1}}"
            else:
                integrand = rf"\left({den}\right)^{{-1}}({coef}{x}^{{{power - 1}}})"
            answer = rf"\ln\left|{den}\right|+C"
        elif family == "log_du_over_u_reordered":
            # Same skill, harder rewrite: \frac{x}{x^2+4} needs factor 1/2
            c = random.choice([1, 4, 9])
            form = random.choice(["half_missing", "three_x", "reversed_den"])
            variant = form
            if form == "half_missing":
                integrand = rf"\frac{{{x}}}{{{x}^{{2}}+{c}}}"
                answer = rf"\frac{{1}}{{2}}\ln\left|{x}^{{2}}+{c}\right|+C"
            elif form == "three_x":
                integrand = rf"\frac{{3{x}}}{{{x}^{{2}}+{c}}}"
                answer = rf"\frac{{3}}{{2}}\ln\left|{x}^{{2}}+{c}\right|+C"
            else:
                integrand = rf"\frac{{2{x}}}{{{c}+{x}^{{2}}}}"
                answer = rf"\ln\left|{x}^{{2}}+{c}\right|+C"
        elif family == "exp_chain_poly":
            # OpenStax 5.39: ∫ 3x^2 e^{2x^3} dx
            # variants: 2x e^{x^2}, x e^{x^2}, e^{x^2}·2x (order)
            choice = random.choice(["x2", "x3", "reordered"])
            variant = choice
            if choice == "x2":
                integrand = random.choice(
                    [
                        rf"2{x}e^{{{x}^{{2}}}}",
                        rf"e^{{{x}^{{2}}}}\cdot 2{x}",
                        rf"2{x}\exp({x}^{{2}})",
                    ]
                )
                answer = rf"e^{{{x}^{{2}}}}+C"
            elif choice == "x3":
                integrand = random.choice(
                    [
                        rf"3{x}^{{2}}e^{{{x}^{{3}}}}",
                        rf"e^{{{x}^{{3}}}}\cdot 3{x}^{{2}}",
                    ]
                )
                answer = rf"e^{{{x}^{{3}}}}+C"
            else:
                # 6x^2 e^{2x^3}
                integrand = random.choice(
                    [
                        rf"6{x}^{{2}}e^{{2{x}^{{3}}}}",
                        rf"e^{{2{x}^{{3}}}}\cdot 6{x}^{{2}}",
                    ]
                )
                answer = rf"e^{{2{x}^{{3}}}}+C"
        elif family == "exp_over_one_plus_exp":
            # OpenStax 5.38 pattern: e^x / (1+e^x)
            form = random.choice(["frac", "rewrite"])
            variant = form
            if form == "frac":
                integrand = rf"\frac{{e^{{{x}}}}}{{1+e^{{{x}}}}}"
            else:
                integrand = rf"e^{{{x}}}\left(1+e^{{{x}}}\right)^{{-1}}"
            answer = rf"\ln\left|1+e^{{{x}}}\right|+C"
        else:  # mixed_rewrite
            # ∫ e^{2x}/(e^{2x}+5) or (2e^{2x})/(e^{2x}+5)
            c = random.randint(2, 6)
            form = random.choice(["exact_du", "half_factor", "reordered"])
            variant = form
            if form == "exact_du":
                integrand = rf"\frac{{2e^{{2{x}}}}}{{e^{{2{x}}}+{c}}}"
                answer = rf"\ln\left|e^{{2{x}}}+{c}\right|+C"
            elif form == "half_factor":
                integrand = rf"\frac{{e^{{2{x}}}}}{{e^{{2{x}}}+{c}}}"
                answer = rf"\frac{{1}}{{2}}\ln\left|e^{{2{x}}}+{c}\right|+C"
            else:
                integrand = rf"\left(e^{{2{x}}}+{c}\right)^{{-1}}\cdot 2e^{{2{x}}}"
                answer = rf"\ln\left|e^{{2{x}}}+{c}\right|+C"

        last["meta"] = _family_structure_meta(
            family,
            generator="integral_log_exp_substitution",
            structure=structure,
            variant=variant,
        )
        prompt = rf"\int {integrand}\,d{x}"
        return prompt, "log/exp substitution integral", answer if include_answer_key else None

    def metadata_builder(_p: str, _t: str, _a: str | None) -> dict:
        return dict(last.get("meta") or {})

    return _make_questions(
        topic,
        count,
        include_answer_key,
        build,
        metadata_builder=metadata_builder,
        settings=settings,
    )


def format_monomial_safe(coef: int, variable: str) -> str:
    if coef == 1:
        return variable
    if coef == -1:
        return f"-{variable}"
    return f"{coef}{variable}"


GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = {
    "tangent_normal_line": _tangent_normal_line,
    "differentials": _differentials,
    "linear_approximation": _linear_approximation,
    "integral_log_exp_substitution": _integral_log_exp_substitution,
}
