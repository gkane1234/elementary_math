"""Precalculus generators: trigonometry, logarithms, exponentials, sequences."""

from __future__ import annotations

import math
import random
from fractions import Fraction
from typing import Any, Callable

from ..core.metadata import question_metadata
from ..core.models import Question
from ..frameworks.graphing import include_graph_metadata, origin_centered_bounds
from ..settings.params import (
    exponential_params_from_settings,
    logarithm_params_from_settings,
    sequence_params_from_settings,
    trigonometry_params_from_settings,
)
from .utils import (
    _make_questions,
    format_linear_latex,
    format_monomial_latex,
    frac_latex,
    random_int_range,
)

# Standard unit-circle angles (degrees) and exact values
_UNIT_CIRCLE_DEG: dict[int, tuple[str, str, str]] = {
    0: (r"0", r"1", r"0"),
    30: (r"\frac{1}{2}", r"\frac{\sqrt{3}}{2}", r"\frac{\sqrt{3}}{3}"),
    45: (r"\frac{\sqrt{2}}{2}", r"\frac{\sqrt{2}}{2}", "1"),
    60: (r"\frac{\sqrt{3}}{2}", r"\frac{1}{2}", r"\sqrt{3}"),
    90: (r"1", r"0", r"\infty"),
    120: (r"\frac{\sqrt{3}}{2}", r"-\frac{1}{2}", r"-\sqrt{3}"),
    135: (r"\frac{\sqrt{2}}{2}", r"-\frac{\sqrt{2}}{2}", "-1"),
    150: (r"\frac{1}{2}", r"-\frac{\sqrt{3}}{2}", r"-\frac{\sqrt{3}}{3}"),
    180: (r"0", r"-1", r"0"),
    210: (r"-\frac{1}{2}", r"-\frac{\sqrt{3}}{2}", r"\frac{\sqrt{3}}{3}"),
    225: (r"-\frac{\sqrt{2}}{2}", r"-\frac{\sqrt{2}}{2}", "1"),
    240: (r"-\frac{\sqrt{3}}{2}", r"-\frac{1}{2}", r"\sqrt{3}"),
    270: (r"-1", r"0", r"\infty"),
    300: (r"-\frac{\sqrt{3}}{2}", r"\frac{1}{2}", r"-\sqrt{3}"),
    315: (r"-\frac{\sqrt{2}}{2}", r"\frac{\sqrt{2}}{2}", "-1"),
    330: (r"-\frac{1}{2}", r"\frac{\sqrt{3}}{2}", r"-\frac{\sqrt{3}}{3}"),
    360: (r"0", r"1", r"0"),
}

_RADIAN_LABELS: dict[int, str] = {
    0: "0",
    30: r"\frac{\pi}{6}",
    45: r"\frac{\pi}{4}",
    60: r"\frac{\pi}{3}",
    90: r"\frac{\pi}{2}",
    120: r"\frac{2\pi}{3}",
    135: r"\frac{3\pi}{4}",
    150: r"\frac{5\pi}{6}",
    180: r"\pi",
    210: r"\frac{7\pi}{6}",
    225: r"\frac{5\pi}{4}",
    240: r"\frac{4\pi}{3}",
    270: r"\frac{3\pi}{2}",
    300: r"\frac{5\pi}{3}",
    315: r"\frac{7\pi}{4}",
    330: r"\frac{11\pi}{6}",
    360: r"2\pi",
}


def _pick_unit_circle_angle(params) -> tuple[int, str]:
    candidates = [deg for deg in _UNIT_CIRCLE_DEG if params.angle_min <= deg <= params.angle_max]
    if not candidates:
        candidates = list(_UNIT_CIRCLE_DEG)
    deg = random.choice(candidates)
    if params.angle_unit == "radians":
        return deg, _RADIAN_LABELS[deg]
    if params.angle_unit == "both" and random.choice([True, False]):
        return deg, _RADIAN_LABELS[deg]
    return deg, rf"{deg}^\circ"


def _trig_fn_latex(fn: str, angle_latex: str) -> str:
    return f"\\{fn}\\left({angle_latex}\\right)"


def _trig_evaluate(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = trigonometry_params_from_settings(settings)

    def build() -> tuple[str, str, str | None]:
        deg, angle_latex = _pick_unit_circle_angle(params)
        fn = random.choice(params.functions)
        sin_v, cos_v, tan_v = _UNIT_CIRCLE_DEG[deg]
        values = {"sin": sin_v, "cos": cos_v, "tan": tan_v, "cot": tan_v}
        if fn == "cot" and tan_v in ("0", r"\infty"):
            fn = random.choice(["sin", "cos"])
        prompt = _trig_fn_latex(fn, angle_latex)
        answer = values[fn] if include_answer_key else None
        return prompt, f"{fn}({deg}°)", answer

    return _make_questions(topic, count, include_answer_key, build)


def _simple_trig_equations(topic: str, settings: dict) -> list[Question]:
    """Solve basic unit-circle trig equations like sin(x) = 1/2."""
    from question_engine.frameworks.primitives.algebraic_ml import enrich_algebraic_meta

    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = trigonometry_params_from_settings(settings)
    use_pc = str(topic).startswith("pc_")
    difficulty = float(settings["difficulty"] if settings.get("difficulty") is not None else 6)
    last: dict[str, Any] = {"meta": {}}

    # Exact unit-circle solutions in [0, 360) for common RHS values.
    solutions: dict[tuple[str, str], list[int]] = {
        ("sin", r"0"): [0, 180],
        ("sin", r"\frac{1}{2}"): [30, 150],
        ("sin", r"\frac{\sqrt{2}}{2}"): [45, 135],
        ("sin", r"\frac{\sqrt{3}}{2}"): [60, 120],
        ("sin", r"1"): [90],
        ("sin", r"-1"): [270],
        ("sin", r"-\frac{1}{2}"): [210, 330],
        ("sin", r"-\frac{\sqrt{2}}{2}"): [225, 315],
        ("sin", r"-\frac{\sqrt{3}}{2}"): [240, 300],
        ("cos", r"0"): [90, 270],
        ("cos", r"1"): [0],
        ("cos", r"-1"): [180],
        ("cos", r"\frac{1}{2}"): [60, 300],
        ("cos", r"\frac{\sqrt{2}}{2}"): [45, 315],
        ("cos", r"\frac{\sqrt{3}}{2}"): [30, 330],
        ("cos", r"-\frac{1}{2}"): [120, 240],
        ("cos", r"-\frac{\sqrt{2}}{2}"): [135, 225],
        ("cos", r"-\frac{\sqrt{3}}{2}"): [150, 210],
    }
    allowed_fns = [fn for fn in params.functions if fn in ("sin", "cos")]
    if not allowed_fns:
        allowed_fns = ["sin", "cos"]
    keys = [key for key in solutions if key[0] in allowed_fns]

    def _angle_latex(deg: int) -> str:
        if params.angle_unit == "radians":
            return _RADIAN_LABELS.get(deg, rf"{deg}^\circ")
        if params.angle_unit == "both" and random.choice([True, False]):
            return _RADIAN_LABELS.get(deg, rf"{deg}^\circ")
        return rf"{deg}^\circ"

    def build() -> tuple[str, str, str | None]:
        form_stamp: dict[str, Any] = {}
        if use_pc:
            from question_engine.frameworks.primitives.openstax_precalc import select_pc_form

            _form, form_stamp = select_pc_form(
                "precalculus_trig_equations",
                d=difficulty,
                leaf_id=str(topic or ""),
            )
        fn, rhs = random.choice(keys)
        degs = solutions[(fn, rhs)]
        prompt = f"\\{fn}(x) = {rhs}"
        if include_answer_key:
            answers = ", ".join(_angle_latex(deg) for deg in degs)
            answer = rf"x = {answers}"
        else:
            answer = None
        last["meta"] = {
            "primitive_engine": "simple_trig_equations",
            "mode": "linear_value",
            "function_classes": ["trig", "algebraic"],
            "methods_used": ["trig_equation"],
            **form_stamp,
        }
        return prompt, "trig equation", answer

    def metadata_builder(_p: str, _t: str, answer: str | None) -> dict[str, Any]:
        return enrich_algebraic_meta(
            last.get("meta"),
            pack="structured_trig_equation",
            generator="simple_trig_equations",
            methods_used=["trig_equation"],
            answer=answer,
            course_tag="pc" if use_pc else "a2",
        )

    return _make_questions(
        topic,
        count,
        include_answer_key,
        build,
        metadata_builder=metadata_builder if use_pc else None,
        settings=settings,
    )


def _trig_unit_circle(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = trigonometry_params_from_settings(settings)

    def build() -> tuple[str, str, str | None]:
        deg, angle_latex = _pick_unit_circle_angle(params)
        fn = random.choice([f for f in ("sin", "cos") if f in params.functions] or ["sin", "cos"])
        sin_v, cos_v, _ = _UNIT_CIRCLE_DEG[deg]
        value = sin_v if fn == "sin" else cos_v
        if random.choice([True, False]):
            prompt = (
                f"\\text{{Find }} {_trig_fn_latex(fn, angle_latex)} "
                f"\\text{{ on the unit circle.}}"
            )
            answer = value if include_answer_key else None
            label = f"unit circle {fn} at {deg}°"
        else:
            prompt = (
                f"\\text{{An angle on the unit circle has }} \\{fn} = {value}. "
                f"\\text{{Which standard angle (in degrees) has this value?}}"
            )
            answer = str(deg) if include_answer_key else None
            label = f"unit circle angle for {fn}={value}"
        return prompt, label, answer

    return _make_questions(topic, count, include_answer_key, build)


def _trig_basic_identities(topic: str, settings: dict) -> list[Question]:
    from question_engine.frameworks.primitives.algebraic_ml import enrich_algebraic_meta

    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = trigonometry_params_from_settings(settings)
    use_pc = str(topic).startswith("pc_")
    d = float(settings["difficulty"] if settings.get("difficulty") is not None else 6)
    last: dict[str, Any] = {"meta": {}}

    pythagorean = [
        (r"\sin^2 \theta + \cos^2 \theta", "1"),
        (r"\sec^2 \theta - \tan^2 \theta", "1"),
        (r"1 + \cot^2 \theta", r"\csc^2 \theta"),
    ]
    reciprocal = [
        (r"\tan \theta", r"\frac{\sin \theta}{\cos \theta}"),
        (r"\cot \theta", r"\frac{\cos \theta}{\sin \theta}"),
        (r"\sec \theta", r"\frac{1}{\cos \theta}"),
        (r"\csc \theta", r"\frac{1}{\sin \theta}"),
    ]

    def build() -> tuple[str, str, str | None]:
        form_stamp: dict[str, Any] = {}
        family = "pythagorean"
        if use_pc:
            from question_engine.frameworks.primitives.openstax_precalc import (
                pc_form_constraints,
                select_pc_form,
            )

            form, form_stamp = select_pc_form(
                "precalculus_trig_identities",
                d=d,
                leaf_id=str(topic or ""),
            )
            family = str(pc_form_constraints(form).get("family") or "pythagorean")
        elif params.allow_pythagorean_identities and params.allow_reciprocal_identities:
            family = random.choice(["pythagorean", "reciprocal"])
        elif params.allow_reciprocal_identities:
            family = "reciprocal"

        if family == "reciprocal" and (
            params.allow_reciprocal_identities or use_pc
        ):
            pool = reciprocal
        elif params.allow_pythagorean_identities or use_pc:
            pool = pythagorean
        else:
            pool = pythagorean
        lhs, rhs = random.choice(pool)
        if random.choice([True, False]):
            prompt = f"\\text{{Simplify: }} {lhs}"
            answer = rhs if include_answer_key else None
        else:
            prompt = f"\\text{{Rewrite using a fundamental identity: }} {lhs} = {rhs}"
            answer = lhs if include_answer_key else None
        last["meta"] = {
            "primitive_engine": "trig_basic_identities",
            "mode": family,
            "function_classes": ["trig", "algebraic"],
            "methods_used": ["trig_identity", family],
            **form_stamp,
        }
        return prompt, "trig identity", answer

    def metadata_builder(_p: str, _t: str, answer: str | None) -> dict[str, Any]:
        return enrich_algebraic_meta(
            last.get("meta"),
            pack="structured_trig_identity",
            generator="trig_basic_identities",
            methods_used=["trig_identity"],
            answer=answer,
            course_tag="pc" if use_pc else "a2",
        )

    return _make_questions(
        topic,
        count,
        include_answer_key,
        build,
        metadata_builder=metadata_builder if use_pc else None,
        settings=settings,
    )


def _random_log_base(params) -> tuple[int | str, str]:
    choices: list[tuple[int | str, str]] = []
    lo, hi = params.base_min, params.base_max
    for base in range(lo, hi + 1):
        choices.append((base, str(base)))
    if params.allow_common_log:
        choices.append(("10", r"10"))
    if params.allow_natural_log:
        choices.append(("e", "e"))
    return random.choice(choices or [(2, "2")])


def _log_base_latex(base_key: int | str, base_label: str) -> str:
    if base_key == "e":
        return r"\ln"
    if base_key == "10":
        return r"\log"
    return rf"\log_{{{base_label}}}"


def _log_evaluate(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = logarithm_params_from_settings(settings)

    def build() -> tuple[str, str, str | None]:
        base_key, base_label = _random_log_base(params)
        if params.require_integer_result:
            exponent = random.randint(1, 6)
            if isinstance(base_key, int):
                argument = base_key**exponent
            elif base_key == "e":
                argument = round(math.e**exponent, 4)
                exponent = exponent
            else:
                argument = 10**exponent
            answer_value = str(exponent)
        else:
            argument = random.randint(params.argument_min, params.argument_max)
            if isinstance(base_key, int):
                answer_value = f"{math.log(argument, base_key):.3g}"
            elif base_key == "e":
                answer_value = f"{math.log(argument):.3g}"
            else:
                answer_value = f"{math.log10(argument):.3g}"
        log_latex = _log_base_latex(base_key, base_label)
        prompt = f"{log_latex}\\left({argument}\\right)"
        answer = answer_value if include_answer_key else None
        return prompt, f"log eval base={base_label}", answer

    return _make_questions(topic, count, include_answer_key, build)


def _log_change_of_base(topic: str, settings: dict) -> list[Question]:
    from question_engine.frameworks.primitives.algebraic_ml import enrich_algebraic_meta

    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = logarithm_params_from_settings(settings)
    use_pc = str(topic).startswith("pc_")
    use_a2 = str(topic).startswith("a2_")
    d = float(settings["difficulty"] if settings.get("difficulty") is not None else 6)
    last: dict[str, Any] = {"meta": {}}

    def build() -> tuple[str, str, str | None]:
        form_stamp: dict[str, Any] = {}
        rule = "change_of_base"
        if use_a2:
            from question_engine.frameworks.primitives.openstax_a2 import (
                a2_form_constraints,
                select_a2_form,
            )

            form, form_stamp = select_a2_form(
                "algebra2_exp_log",
                d=d,
                leaf_id=str(topic or ""),
            )
            kind = str(a2_form_constraints(form).get("kind") or "properties")
            if kind == "change_of_base":
                rule = "change_of_base"
            else:
                rule = random.choice(["product", "quotient", "power"])
        elif use_pc:
            from question_engine.frameworks.primitives.openstax_precalc import (
                pc_form_constraints,
                select_pc_form,
            )

            form, form_stamp = select_pc_form(
                "precalculus_exp_log",
                d=d,
                leaf_id=str(topic or ""),
            )
            rule = str(pc_form_constraints(form).get("rule") or "change_of_base")

        base = random.randint(params.base_min, params.base_max)
        if rule == "product":
            m = random.randint(2, 9)
            n = random.randint(2, 9)
            prompt = (
                f"\\text{{Expand: }} \\log_{{{base}}}\\left({m * n}\\right)"
            )
            answer = (
                rf"\log_{{{base}}}({m})+\log_{{{base}}}({n})"
                if include_answer_key
                else None
            )
            mode = "product"
            methods = ["log_product"]
        elif rule == "quotient":
            n = random.randint(2, 8)
            m = n * random.randint(2, 6)
            prompt = (
                f"\\text{{Expand: }} \\log_{{{base}}}\\left(\\frac{{{m}}}{{{n}}}\\right)"
            )
            answer = (
                rf"\log_{{{base}}}({m})-\log_{{{base}}}({n})"
                if include_answer_key
                else None
            )
            mode = "quotient"
            methods = ["log_quotient"]
        elif rule == "power":
            arg = random.randint(2, 9)
            p = random.randint(2, 5)
            prompt = (
                f"\\text{{Expand: }} \\log_{{{base}}}\\left({arg}^{{{p}}}\\right)"
            )
            answer = (
                rf"{p}\log_{{{base}}}({arg})" if include_answer_key else None
            )
            mode = "power"
            methods = ["log_power"]
        else:
            exponent = random.randint(2, 5)
            argument = base**exponent
            new_base = random.randint(params.base_min, params.base_max)
            while new_base == base:
                new_base = random.randint(params.base_min, params.base_max)
            prompt = (
                f"\\text{{Rewrite using change of base: }} "
                f"\\log_{{{base}}}({argument})"
            )
            answer = (
                rf"\frac{{\log_{{{new_base}}}({argument})}}{{\log_{{{new_base}}}({base})}}"
                if include_answer_key
                else None
            )
            mode = "change_of_base"
            methods = ["change_of_base"]
        last["meta"] = {
            "primitive_engine": "log_change_of_base",
            "mode": mode,
            "log_base_min": params.base_min,
            "log_base_max": params.base_max,
            "function_classes": ["log", "algebraic"],
            "methods_used": methods,
            **form_stamp,
        }
        return prompt, mode, answer

    def metadata_builder(_p: str, _t: str, answer: str | None) -> dict[str, Any]:
        return enrich_algebraic_meta(
            last.get("meta"),
            pack="structured_log_props",
            generator="log_change_of_base",
            methods_used=["log_props"],
            knobs={
                "log_base_min": params.base_min,
                "log_base_max": params.base_max,
                "allow_natural_log": getattr(params, "allow_natural_log", False),
                "allow_common_log": getattr(params, "allow_common_log", False),
            },
            answer=answer,
            course_tag="pc" if use_pc else "a2",
        )

    return _make_questions(
        topic,
        count,
        include_answer_key,
        build,
        metadata_builder=metadata_builder,
        settings=settings,
    )


def _int_log_base(params) -> tuple[int, str]:
    """Prefer integer bases for clean equation answers (OpenStax §4.6 / IA §10.5)."""
    lo, hi = int(params.base_min), int(params.base_max)
    candidates = [b for b in range(max(2, lo), max(hi, 2) + 1) if b != 1]
    if not candidates:
        candidates = [2, 3, 4, 5, 10]
    base = random.choice(candidates)
    return base, str(base)


def _format_log_eq_answer(
    valid: list[int],
    extraneous: list[int] | None = None,
    *,
    include_answer_key: bool,
) -> str | None:
    if not include_answer_key:
        return None
    extra = [e for e in (extraneous or []) if e not in valid]
    valid_parts = [f"x = {v}" for v in sorted(set(valid))]
    extra_parts = [f"x = {e}" for e in sorted(set(extra))]
    if not valid_parts:
        if extra_parts:
            discarded = r" \text{ or } ".join(extra_parts)
            return rf"\text{{no solution}};\ {discarded} \text{{ (extraneous)}}"
        return r"\text{no solution}"
    body = r" \text{ or } ".join(valid_parts)
    if extra_parts:
        discarded = r" \text{ or } ".join(extra_parts)
        return rf"{body};\ {discarded} \text{{ (extraneous)}}"
    return body


def _build_log_definition(params, include_answer_key: bool) -> tuple[str, str, str | None, str]:
    base_key, base_label = _int_log_base(params)
    # Keep modest exponents so D=0 stays textbook-easy.
    exponent = random.randint(1, 4)
    solution = base_key**exponent
    log_latex = _log_base_latex(base_key, base_label)
    prompt = f"{log_latex}(x) = {exponent}"
    answer = _format_log_eq_answer([solution], include_answer_key=include_answer_key)
    return prompt, "log equation", answer, "definition"


def _build_log_linear_argument(
    params, include_answer_key: bool, *, d: float
) -> tuple[str, str, str | None, str]:
    """OpenStax §4.6: log_b(ax + c) = k."""
    base, base_label = _int_log_base(params)
    k = random.randint(1, 3 if d < 12 else 4)
    a = random.choice([1, 2, 3, 4, 5, 7])
    rhs = base**k
    sol = random.randint(1, 8)
    c = rhs - a * sol
    if c == 0:
        c = -a
        sol = (rhs - c) // a
    log_latex = _log_base_latex(base, base_label)
    arg = format_linear_latex(a, c, variable="x")
    prompt = f"{log_latex}\\left({arg}\\right) = {k}"
    answer = _format_log_eq_answer([sol], include_answer_key=include_answer_key)
    return prompt, "log equation", answer, "linear_argument"


def _build_log_algebra_coeff(
    params, include_answer_key: bool
) -> tuple[str, str, str | None, str]:
    """OpenStax §4.6 Ex. 9: a log_b(x) + c = d."""
    base, base_label = _int_log_base(params)
    a = random.choice([2, 3, 4, 5, 6])
    expo = random.randint(1, 3)
    c = random.randint(1, 6)
    d_val = a * expo + c
    sol = base**expo
    log_latex = _log_base_latex(base, base_label)
    prompt = f"{a} {log_latex}(x) + {c} = {d_val}"
    answer = _format_log_eq_answer([sol], include_answer_key=include_answer_key)
    return prompt, "log equation", answer, "algebra_coeff"


def _build_log_product_sum(
    params, include_answer_key: bool, *, d: float
) -> tuple[str, str, str | None, str]:
    """OpenStax IA §10.5 Ex. 10.39: log_b(x) + log_b(x − p) = k; discard extraneous."""
    base, base_label = _int_log_base(params)
    p = random.randint(2, 6 if d < 12 else 9)
    for _ in range(40):
        expo = random.randint(1, 3 if d < 14 else 4)
        product = base**expo
        disc = p * p + 4 * product
        root = int(round(disc**0.5))
        if root * root != disc or (p + root) % 2 != 0:
            continue
        r = (p + root) // 2
        if r <= p:
            continue
        extra = (p - root) // 2
        log_latex = _log_base_latex(base, base_label)
        prompt = f"{log_latex}(x) + {log_latex}(x - {p}) = {expo}"
        answer = _format_log_eq_answer(
            [r],
            [extra] if extra != r else None,
            include_answer_key=include_answer_key,
        )
        return prompt, "log equation", answer, "product_sum"
    # Fallback: log_2(x) + log_2(x − 2) = 3 → x=4; x=-2 extraneous
    log_latex = _log_base_latex(2, "2")
    prompt = f"{log_latex}(x) + {log_latex}(x - 2) = 3"
    answer = _format_log_eq_answer([4], [-2], include_answer_key=include_answer_key)
    return prompt, "log equation", answer, "product_sum"


def _build_log_one_to_one(
    params, include_answer_key: bool, *, d: float
) -> tuple[str, str, str | None, str]:
    """log_b(ax+c) = log_b(dx+e) — equate linear arguments; check domain."""
    _ = d
    base, base_label = _int_log_base(params)
    log_latex = _log_base_latex(base, base_label)
    # Plant a valid root; choose slopes so algebra is one-step.
    sol = random.randint(2, 8)
    a = random.choice([1, 2, 3])
    d_coef = random.choice([1, 2, 3])
    while d_coef == a:
        d_coef = random.choice([1, 2, 3, 4])
    c = random.randint(1, 10)
    # a*sol + c = d_coef*sol + e  ⇒  e = a*sol + c - d_coef*sol
    e = a * sol + c - d_coef * sol
    left = format_linear_latex(a, c, variable="x")
    right = format_linear_latex(d_coef, e, variable="x")
    prompt = f"{log_latex}\\left({left}\\right) = {log_latex}\\left({right}\\right)"
    # Domain: both linear args > 0 at sol (by construction equal and positive if we force).
    left_val = a * sol + c
    if left_val <= 0:
        # Flip constants to keep positive argument.
        c = abs(c) + 1
        e = a * sol + c - d_coef * sol
        left = format_linear_latex(a, c, variable="x")
        right = format_linear_latex(d_coef, e, variable="x")
        prompt = f"{log_latex}\\left({left}\\right) = {log_latex}\\left({right}\\right)"
    answer = _format_log_eq_answer([sol], include_answer_key=include_answer_key)
    return prompt, "log equation", answer, "one_to_one"


def _build_log_one_to_one_quadratic(
    params, include_answer_key: bool
) -> tuple[str, str, str | None, str]:
    """OpenStax §4.6 Ex. 12: log_b(x^2 − p) = log_b(q x); one root fails domain."""
    base, base_label = _int_log_base(params)
    log_latex = _log_base_latex(base, base_label)
    # Roots r > 0 and s < 0 of x^2 − q x + p = 0 with p = r*s < 0:
    # log(x^2 − |p|) wait: x^2 + p = q x with p = r s < 0 ⇒ log(x^2 − |p|) = log(q x).
    r = random.randint(3, 8)
    s = -random.randint(1, 4)
    if r + s == 0:
        s = -1 if r != 1 else -2
    q = r + s
    p = r * s  # negative
    left = rf"x^{{2}} - {abs(p)}"
    right = format_linear_latex(q, 0, variable="x")
    prompt = f"{log_latex}\\left({left}\\right) = {log_latex}\\left({right}\\right)"
    valid: list[int] = []
    extraneous: list[int] = []
    for cand in (r, s):
        left_val = cand * cand + p
        right_val = q * cand
        if left_val > 0 and right_val > 0:
            valid.append(cand)
        else:
            extraneous.append(cand)
    if not valid:
        # Guaranteed fallback: log(x^2 - 6) = log(x) → roots of x^2 - x - 6 = 0 → 3, -2
        prompt = f"{log_latex}\\left(x^{{2}} - 6\\right) = {log_latex}(x)"
        valid, extraneous = [3], [-2]
    answer = _format_log_eq_answer(
        valid, extraneous, include_answer_key=include_answer_key
    )
    return prompt, "log equation", answer, "one_to_one_quadratic"


def _build_log_quotient_diff(
    params, include_answer_key: bool
) -> tuple[str, str, str | None, str]:
    """OpenStax exercises: log_b(x + a) − log_b(x) = log_b(k)."""
    base, base_label = _int_log_base(params)
    k = random.choice([2, 3, 4, 5])
    a = random.randint(2, 12) * (k - 1)
    sol = a // (k - 1)
    log_latex = _log_base_latex(base, base_label)
    prompt = (
        f"{log_latex}\\left(x + {a}\\right) - {log_latex}(x) = {log_latex}({k})"
    )
    answer = _format_log_eq_answer([sol], include_answer_key=include_answer_key)
    return prompt, "log equation", answer, "quotient_diff"


def _log_equation_simple(topic: str, settings: dict) -> list[Question]:
    from question_engine.frameworks.primitives.algebraic_ml import enrich_algebraic_meta

    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = logarithm_params_from_settings(settings)
    use_a2 = str(topic).startswith("a2_")
    use_pc = str(topic).startswith("pc_")
    # Do not use `or 6` — difficulty 0 is valid and must stay 0.
    _raw_d = settings.get("difficulty")
    d = float(6 if _raw_d is None else _raw_d)
    leaf = str(topic or "")
    hard_leaf = leaf.endswith("logarithmic_equations_hard") or leaf.endswith(
        "_logarithmic_equations_hard"
    )
    last: dict[str, Any] = {"meta": {}}

    def build() -> tuple[str, str, str | None]:
        form_stamp: dict[str, Any] = {}
        kind = "definition"
        if use_a2:
            from question_engine.frameworks.primitives.openstax_a2 import (
                a2_form_constraints,
                select_a2_form,
            )

            form, form_stamp = select_a2_form(
                "algebra2_exp_log",
                d=d,
                leaf_id=leaf,
                rng=random,
            )
            kind = str(a2_form_constraints(form).get("kind") or "definition")
        elif use_pc:
            from question_engine.frameworks.primitives.openstax_precalc import (
                pc_form_constraints,
                select_pc_form,
            )

            form, form_stamp = select_pc_form(
                "precalculus_exp_log",
                d=d,
                leaf_id=leaf,
                rng=random,
            )
            kind = str(pc_form_constraints(form).get("kind") or "definition")
        elif hard_leaf:
            # Non-catalog hard leaf: still avoid definition-only stamps.
            kind = "product_sum" if d < 8 else ("one_to_one" if d < 14 else "quotient_diff")

        kind_aliases = {
            "basic_log_eq": "definition",
            "linear_arg": "linear_argument",
            "algebra_steps": "algebra_coeff",
            "product_equation": "product_sum",
            "log_eq_properties": "product_sum",
        }
        kind = kind_aliases.get(kind, kind)
        builders = {
            "definition": lambda: _build_log_definition(params, include_answer_key),
            "linear_argument": lambda: _build_log_linear_argument(
                params, include_answer_key, d=d
            ),
            "algebra_coeff": lambda: _build_log_algebra_coeff(
                params, include_answer_key
            ),
            "product_sum": lambda: _build_log_product_sum(
                params, include_answer_key, d=d
            ),
            "one_to_one": lambda: _build_log_one_to_one(
                params, include_answer_key, d=d
            ),
            "one_to_one_quadratic": lambda: _build_log_one_to_one_quadratic(
                params, include_answer_key
            ),
            "quotient_diff": lambda: _build_log_quotient_diff(
                params, include_answer_key
            ),
        }
        builder = builders.get(kind) or builders["definition"]
        prompt, topic_label, answer, mode = builder()
        methods = ["log_equation"]
        if mode in {"product_sum", "quotient_diff"}:
            methods.append("log_properties")
        if mode in {"one_to_one", "one_to_one_quadratic"}:
            methods.append("log_1to1")
        if answer and "extraneous" in answer:
            methods.append("extraneous_check")
        last["meta"] = {
            "primitive_engine": "log_equation_simple",
            "mode": mode,
            "methods_used": methods,
            **form_stamp,
        }
        return prompt, topic_label, answer

    def metadata_builder(_p: str, _t: str, answer: str | None) -> dict[str, Any]:
        return enrich_algebraic_meta(
            last.get("meta"),
            pack="structured_log_equation",
            generator="log_equation_simple",
            methods_used=list(last.get("meta", {}).get("methods_used") or ["log_equation"]),
            answer=answer,
            course_tag="a2" if use_a2 else ("pc" if use_pc else None),
        )

    return _make_questions(
        topic,
        count,
        include_answer_key,
        build,
        metadata_builder=metadata_builder if (use_a2 or use_pc) else None,
        settings=settings,
    )


def _exponential_equation_simple(topic: str, settings: dict) -> list[Question]:
    from question_engine.frameworks.primitives.algebraic_ml import enrich_algebraic_meta

    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = exponential_params_from_settings(settings)
    use_pc = str(topic).startswith("pc_")
    use_a2 = str(topic).startswith("a2_")
    d = float(settings["difficulty"] if settings.get("difficulty") is not None else 6)
    last: dict[str, Any] = {"meta": {}}

    def build() -> tuple[str, str, str | None]:
        form_stamp: dict[str, Any] = {}
        kind = "same_base"
        if use_a2:
            from question_engine.frameworks.primitives.openstax_a2 import (
                a2_form_constraints,
                select_a2_form,
            )

            form, form_stamp = select_a2_form(
                "algebra2_exp_log",
                d=d,
                leaf_id=str(topic or ""),
            )
            kind = str(a2_form_constraints(form).get("kind") or "same_base")
        elif use_pc:
            from question_engine.frameworks.primitives.openstax_precalc import (
                pc_form_constraints,
                select_pc_form,
            )

            form, form_stamp = select_pc_form(
                "precalculus_exp_log",
                d=d,
                leaf_id=str(topic or ""),
            )
            kind = str(pc_form_constraints(form).get("kind") or "same_base")

        if kind == "rewrite_common_base":
            # Textbook-style rewrite-to-common-base (OpenStax §4.6 Ex. 2)
            pair = random.choice(
                [
                    ("4^{x} = 8^{x - 1}", 3),
                    ("8^{x + 2} = 16^{x + 1}", 2),
                    ("9^{x} = 27^{x - 1}", 3),
                    ("25^{x} = 5^{x + 2}", 1),
                ]
            )
            prompt, sol = pair
            answer = f"x = {sol}" if include_answer_key else None
            mode = "rewrite_common_base"
            methods = ["rewrite_common_base"]
        else:
            base = random.randint(params.base_min, params.base_max)
            exponent = random.randint(params.exponent_min, params.exponent_max)
            rhs = base**exponent
            prompt = f"{base}^{{x}} = {rhs}"
            answer = f"x = {exponent}" if include_answer_key else None
            mode = "same_base"
            methods = ["same_base"]
        last["meta"] = {
            "primitive_engine": "exponential_equation_simple",
            "mode": mode,
            "base_min": params.base_min,
            "base_max": params.base_max,
            "exponent_min": params.exponent_min,
            "exponent_max": params.exponent_max,
            "function_classes": ["exp", "algebraic"],
            "methods_used": methods,
            **form_stamp,
        }
        return prompt, "exponential equation", answer

    def metadata_builder(_p: str, _t: str, answer: str | None) -> dict[str, Any]:
        return enrich_algebraic_meta(
            last.get("meta"),
            pack="structured_exp_equation",
            generator="exponential_equation_simple",
            methods_used=["exp_equation"],
            knobs={
                "base_min": params.base_min,
                "base_max": params.base_max,
                "exponent_min": params.exponent_min,
                "exponent_max": params.exponent_max,
            },
            answer=answer,
            course_tag="pc" if use_pc else "a2",
        )

    return _make_questions(
        topic,
        count,
        include_answer_key,
        build,
        metadata_builder=metadata_builder,
        settings=settings,
    )


def _exponential_equation_with_log(topic: str, settings: dict) -> list[Question]:
    """OpenStax §4.6 — exponential equations that need logarithms (bases differ)."""
    from question_engine.frameworks.primitives.algebraic_ml import enrich_algebraic_meta

    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = exponential_params_from_settings(settings)
    use_pc = str(topic).startswith("pc_")
    use_a2 = str(topic).startswith("a2_")
    d = float(settings["difficulty"] if settings.get("difficulty") is not None else 6)
    last: dict[str, Any] = {"meta": {}}

    def build() -> tuple[str, str, str | None]:
        form_stamp: dict[str, Any] = {}
        if use_a2:
            from question_engine.frameworks.primitives.openstax_a2 import select_a2_form

            _, form_stamp = select_a2_form(
                "algebra2_exp_log",
                d=d,
                leaf_id=str(topic or ""),
            )
        elif use_pc:
            from question_engine.frameworks.primitives.openstax_precalc import select_pc_form

            _form, form_stamp = select_pc_form(
                "precalculus_exp_log",
                d=d,
                leaf_id=str(topic or ""),
            )

        # Honest "needs log": RHS is not a pure power of the same base.
        # OpenStax shapes: b^{cx} = k, or a^{x+c} = b^{x}, or A e^{kt} = B.
        mode = "needs_log"
        if d < 8:
            base = random.randint(max(2, params.base_min), max(params.base_max, 5))
            coef = random.choice([1, 2, 3]) if d >= 4 else 1
            # Pick k that is NOT a pure power of base.
            k = random.choice([3, 5, 6, 7, 10, 12, 15, 20, 24, 30])
            while k > 1:
                # reject if k is base^n for small n
                pure = False
                pwr = base
                for _ in range(1, 8):
                    if pwr == k:
                        pure = True
                        break
                    if pwr > k:
                        break
                    pwr *= base
                if not pure:
                    break
                k += 1
            expo_tex = format_monomial_latex(coef) or "x"
            prompt = f"{base}^{{{expo_tex}}} = {k}"
            if include_answer_key:
                if coef == 1:
                    answer = rf"x = \log_{{{base}}}({k})"
                else:
                    answer = rf"x = \dfrac{{\log_{{{base}}}({k})}}{{{coef}}}"
            else:
                answer = None
        elif d < 16:
            # Different bases: a^{x+c} = b^{x} (OpenStax Ex. 5 style)
            a = random.choice([2, 3, 4, 5])
            b = random.choice([2, 3, 4, 5, 6, 7])
            while b == a:
                b = random.choice([2, 3, 4, 5, 6, 7, 10])
            c = random.randint(1, 3)
            prompt = f"{a}^{{x + {c}}} = {b}^{{x}}"
            if include_answer_key:
                if c == 1:
                    answer = rf"x = \dfrac{{\ln({a})}}{{\ln({b}) - \ln({a})}}"
                else:
                    answer = rf"x = \dfrac{{{c}\ln({a})}}{{\ln({b}) - \ln({a})}}"
            else:
                answer = None
            mode = "different_bases"
        else:
            # Continuous form: A e^{kt} = B (OpenStax Ex. 6)
            A = random.choice([2, 3, 4, 5, 10, 20])
            B = random.choice([6, 11, 12, 15, 20, 50, 100])
            while B == A:
                B = random.choice([7, 11, 15, 25, 50])
            k = random.choice([1, 2, 3, 5])
            # Prefer variable x for leaf consistency (catalog says solve for x).
            prompt = f"{A} e^{{{k} x}} = {B}"
            if include_answer_key:
                if A == 1:
                    answer = rf"x = \dfrac{{\ln({B})}}{{{k}}}"
                else:
                    answer = rf"x = \dfrac{{\ln\!\left(\dfrac{{{B}}}{{{A}}}\right)}}{{{k}}}"
            else:
                answer = None
            mode = "exp_ae_kt"

        last["meta"] = {
            "primitive_engine": "exponential_equation_with_log",
            "mode": mode,
            "function_classes": ["exp", "log", "algebraic"],
            "methods_used": ["take_log"],
            **form_stamp,
        }
        return prompt, "exponential equation with log", answer

    def metadata_builder(_p: str, _t: str, answer: str | None) -> dict[str, Any]:
        return enrich_algebraic_meta(
            last.get("meta"),
            pack="structured_exp_equation",
            generator="exponential_equation_with_log",
            methods_used=["take_log"],
            answer=answer,
            course_tag="pc" if use_pc else "a2",
        )

    return _make_questions(
        topic,
        count,
        include_answer_key,
        build,
        metadata_builder=metadata_builder if (use_pc or use_a2) else None,
        settings=settings,
    )


def _sequence_arithmetic_nth_term(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = sequence_params_from_settings(settings)

    def build() -> tuple[str, str, str | None]:
        a1 = random.randint(params.first_term_min, params.first_term_max)
        d = random.randint(params.common_diff_min, params.common_diff_max)
        while d == 0:
            d = random.randint(params.common_diff_min, params.common_diff_max)
        n = random.randint(params.nth_min, params.nth_max)
        an = a1 + (n - 1) * d
        prompt = (
            f"\\text{{Find the }} {n}^{{\\text{{th}}}} \\text{{ term of the arithmetic sequence "
            f"with }} a_1 = {a1} \\text{{ and }} d = {d}."
        )
        answer = str(an) if include_answer_key else None
        return prompt, f"arithmetic a_{n}", answer

    return _make_questions(topic, count, include_answer_key, build)


def _sequence_geometric_nth_term(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = sequence_params_from_settings(settings)

    def build() -> tuple[str, str, str | None]:
        a1 = random.randint(params.first_term_min, params.first_term_max)
        if a1 == 0:
            a1 = 1
        lo, hi = params.common_ratio_min, params.common_ratio_max
        if not params.allow_negative_ratio:
            lo, hi = max(1, lo), max(1, hi)
        r = random.randint(lo, hi)
        while r in (0, 1):
            r = random.randint(lo, hi)
        n = random.randint(params.nth_min, params.nth_max)
        an = a1 * (r ** (n - 1))
        prompt = (
            f"\\text{{Find the }} {n}^{{\\text{{th}}}} \\text{{ term of the geometric sequence "
            f"with }} a_1 = {a1} \\text{{ and }} r = {r}."
        )
        answer = str(an) if include_answer_key else None
        return prompt, f"geometric a_{n}", answer

    return _make_questions(topic, count, include_answer_key, build)


def _sequence_arithmetic_geometric_mean(topic: str, settings: dict) -> list[Question]:
    """Find the arithmetic or geometric mean between two numbers."""
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = sequence_params_from_settings(settings)

    def build() -> tuple[str, str, str | None]:
        use_geo = random.choice([True, False])
        if use_geo:
            a = random.randint(1, max(2, abs(params.first_term_max)))
            lo, hi = params.common_ratio_min, params.common_ratio_max
            if not params.allow_negative_ratio:
                lo, hi = max(2, lo), max(2, hi)
            r = random.randint(lo, hi)
            while r in (0, 1, -1):
                r = random.randint(lo, hi)
            c = a * r * r
            prompt = (
                rf"\text{{Find the geometric mean of }} {a} \text{{ and }} {c}."
            )
            answer = str(abs(a * r))
        else:
            a = random.randint(params.first_term_min, params.first_term_max)
            c = random.randint(params.first_term_min, params.first_term_max)
            while c == a:
                c = random.randint(params.first_term_min, params.first_term_max)
            prompt = (
                rf"\text{{Find the arithmetic mean of }} {a} \text{{ and }} {c}."
            )
            mean = Fraction(a + c, 2)
            answer = frac_latex(mean) if mean.denominator != 1 else str(mean.numerator)
        return prompt, "arithmetic or geometric mean", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _sequence_arithmetic_series(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = sequence_params_from_settings(settings)

    def build() -> tuple[str, str, str | None]:
        a1 = random.randint(params.first_term_min, params.first_term_max)
        d = random.randint(params.common_diff_min, params.common_diff_max)
        while d == 0:
            d = random.randint(params.common_diff_min, params.common_diff_max)
        n = random.randint(max(3, params.nth_min), max(4, params.nth_max))
        an = a1 + (n - 1) * d
        total = n * (a1 + an) // 2
        prompt = (
            rf"\text{{Find the sum of the first }} {n} \text{{ terms of the arithmetic "
            rf"sequence with }} a_1 = {a1} \text{{ and }} d = {d}."
        )
        return prompt, f"arithmetic series S_{n}", str(total) if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _sequence_geometric_series(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    params = sequence_params_from_settings(settings)

    def build() -> tuple[str, str, str | None]:
        a1 = random.randint(1, 5)
        r = random.choice([2, 3, -2, -3])
        n = random.randint(3, 6)
        if r == 1:
            total = n * a1
        else:
            total = a1 * (r**n - 1) // (r - 1)
        prompt = (
            rf"\text{{Find the sum of the first }} {n} \text{{ terms of the geometric "
            rf"sequence with }} a_1 = {a1} \text{{ and }} r = {r}."
        )
        return prompt, f"geometric series S_{n}", str(total) if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _trig_sum_difference(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))
    from question_engine.frameworks.primitives.algebraic_ml import enrich_algebraic_meta
    from question_engine.settings.params import apply_trigonometry_continuous_knobs

    local = apply_trigonometry_continuous_knobs(settings)
    use_pc = str(topic).startswith("pc_")
    difficulty = float(
        local["difficulty"]
        if local.get("difficulty") is not None
        else (settings["difficulty"] if settings.get("difficulty") is not None else 6)
    )
    last: dict[str, Any] = {"meta": {}}
    pool = [
        (r"\sin(\alpha+\beta)", r"\sin\alpha\cos\beta+\cos\alpha\sin\beta"),
        (r"\sin(\alpha-\beta)", r"\sin\alpha\cos\beta-\cos\alpha\sin\beta"),
        (r"\cos(\alpha+\beta)", r"\cos\alpha\cos\beta-\sin\alpha\sin\beta"),
        (r"\cos(\alpha-\beta)", r"\cos\alpha\cos\beta+\sin\alpha\sin\beta"),
    ]
    if bool(local.get("allow_tan", False)) or _continuous_d_absent(settings):
        pool.append(
            (
                r"\tan(\alpha+\beta)",
                r"\frac{\tan\alpha+\tan\beta}{1-\tan\alpha\tan\beta}",
            )
        )

    def build() -> tuple[str, str, str | None]:
        form_stamp: dict[str, Any] = {}
        if use_pc:
            from question_engine.frameworks.primitives.openstax_precalc import select_pc_form

            _form, form_stamp = select_pc_form(
                "precalculus_trig_identities",
                d=difficulty,
                leaf_id=str(topic or ""),
            )
        choice = random.choice(pool)
        prompt = rf"\text{{Expand }}{choice[0]}."
        last["meta"] = {
            "primitive_engine": "trig_sum_difference",
            "mode": "sum_difference",
            "function_classes": ["trig", "algebraic"],
            "methods_used": ["sum_difference"],
            **form_stamp,
        }
        return prompt, "sum/difference identity", choice[1] if keyed else None

    def metadata_builder(_p: str, _t: str, answer: str | None) -> dict[str, Any]:
        return enrich_algebraic_meta(
            last.get("meta"),
            pack="structured_trig_identity",
            generator="trig_sum_difference",
            methods_used=["sum_difference"],
            answer=answer,
            course_tag="pc" if use_pc else "a2",
        )

    return _make_questions(
        topic,
        count,
        keyed,
        build,
        metadata_builder=metadata_builder if use_pc else None,
        settings=settings,
    )


def _continuous_d_absent(settings: dict) -> bool:
    return "difficulty" not in settings or settings["difficulty"] is None


def _trig_multiple_angle(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))
    from question_engine.frameworks.primitives.algebraic_ml import enrich_algebraic_meta
    from question_engine.settings.params import apply_trigonometry_continuous_knobs

    local = apply_trigonometry_continuous_knobs(settings)
    use_pc = str(topic).startswith("pc_")
    difficulty = float(
        local["difficulty"]
        if local.get("difficulty") is not None
        else (settings["difficulty"] if settings.get("difficulty") is not None else 6)
    )
    last: dict[str, Any] = {"meta": {}}
    pool = [
        (r"\sin(2\theta)", r"2\sin\theta\cos\theta"),
        (r"\cos(2\theta)", r"\cos^2\theta-\sin^2\theta"),
    ]
    if bool(local.get("allow_tan", False)) or _continuous_d_absent(settings):
        pool.append(
            (r"\tan(2\theta)", r"\frac{2\tan\theta}{1-\tan^2\theta}")
        )
    if bool(local.get("allow_double_angle_identities", True)) or _continuous_d_absent(
        settings
    ):
        pool.append((r"\sin\theta\cos\theta", r"\frac{1}{2}\sin(2\theta)"))

    def build() -> tuple[str, str, str | None]:
        form_stamp: dict[str, Any] = {}
        if use_pc:
            from question_engine.frameworks.primitives.openstax_precalc import select_pc_form

            _form, form_stamp = select_pc_form(
                "precalculus_trig_identities",
                d=difficulty,
                leaf_id=str(topic or ""),
            )
        choice = random.choice(pool)
        prompt = rf"\text{{Rewrite }}{choice[0]}\text{{ using a double-angle identity.}}"
        last["meta"] = {
            "primitive_engine": "trig_multiple_angle",
            "mode": "double_angle",
            "function_classes": ["trig", "algebraic"],
            "methods_used": ["double_angle"],
            **form_stamp,
        }
        return prompt, "multiple-angle identity", choice[1] if keyed else None

    def metadata_builder(_p: str, _t: str, answer: str | None) -> dict[str, Any]:
        return enrich_algebraic_meta(
            last.get("meta"),
            pack="structured_trig_identity",
            generator="trig_multiple_angle",
            methods_used=["double_angle"],
            answer=answer,
            course_tag="pc" if use_pc else "a2",
        )

    return _make_questions(
        topic,
        count,
        keyed,
        build,
        metadata_builder=metadata_builder if use_pc else None,
        settings=settings,
    )


def _trig_product_to_sum(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))
    from question_engine.frameworks.primitives.algebraic_ml import enrich_algebraic_meta
    from question_engine.settings.params import apply_trigonometry_continuous_knobs

    local = apply_trigonometry_continuous_knobs(settings)
    use_pc = str(topic).startswith("pc_")
    difficulty = float(
        local["difficulty"]
        if local.get("difficulty") is not None
        else (settings["difficulty"] if settings.get("difficulty") is not None else 6)
    )
    last: dict[str, Any] = {"meta": {}}
    # At low continuous D, product-to-sum is locked; fall back to a single
    # sin·cos identity so the generator still produces valid prompts.
    full_pool = [
        (
            r"\sin A\cos B",
            r"\frac{1}{2}\left[\sin(A+B)+\sin(A-B)\right]",
        ),
        (
            r"\cos A\cos B",
            r"\frac{1}{2}\left[\cos(A+B)+\cos(A-B)\right]",
        ),
        (
            r"\sin A\sin B",
            r"\frac{1}{2}\left[\cos(A-B)-\cos(A+B)\right]",
        ),
    ]
    if _continuous_d_absent(settings) or bool(
        local.get("allow_product_to_sum_identities", True)
    ):
        pool = full_pool
    else:
        pool = [full_pool[0]]

    def build() -> tuple[str, str, str | None]:
        form_stamp: dict[str, Any] = {}
        if use_pc:
            from question_engine.frameworks.primitives.openstax_precalc import select_pc_form

            _form, form_stamp = select_pc_form(
                "precalculus_trig_identities",
                d=difficulty,
                leaf_id=str(topic or ""),
            )
        choice = random.choice(pool)
        prompt = rf"\text{{Rewrite }}{choice[0]}\text{{ as a sum.}}"
        last["meta"] = {
            "primitive_engine": "trig_product_to_sum",
            "mode": "product_to_sum",
            "function_classes": ["trig", "algebraic"],
            "methods_used": ["product_to_sum"],
            **form_stamp,
        }
        return prompt, "product-to-sum", choice[1] if keyed else None

    def metadata_builder(_p: str, _t: str, answer: str | None) -> dict[str, Any]:
        return enrich_algebraic_meta(
            last.get("meta"),
            pack="structured_trig_identity",
            generator="trig_product_to_sum",
            methods_used=["product_to_sum"],
            answer=answer,
            course_tag="pc" if use_pc else "a2",
        )

    return _make_questions(
        topic,
        count,
        keyed,
        build,
        metadata_builder=metadata_builder if use_pc else None,
        settings=settings,
    )


def _trig_factoring_equations(topic: str, settings: dict) -> list[Question]:
    """Simple trig equations that factor with fundamental identities."""
    from question_engine.frameworks.primitives.algebraic_ml import enrich_algebraic_meta

    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))
    use_pc = str(topic).startswith("pc_")
    difficulty = float(settings["difficulty"] if settings.get("difficulty") is not None else 6)
    last: dict[str, Any] = {"meta": {}}

    templates = {
        "sin2": (
            r"\text{Solve }2\sin\theta\cos\theta=0\text{ for }0\le\theta<2\pi.",
            r"\theta=0,\frac{\pi}{2},\pi,\frac{3\pi}{2}",
            "factor_fundamental",
        ),
        "cos2": (
            r"\text{Solve }\cos(2\theta)=0\text{ for }0\le\theta<\pi.",
            r"\theta=\frac{\pi}{4},\frac{3\pi}{4}",
            "double_angle_equation",
        ),
        "factor": (
            r"\text{Solve }2\sin^2\theta-\sin\theta=0\text{ for }0\le\theta<2\pi.",
            r"\theta=0,\frac{\pi}{6},\pi,\frac{5\pi}{6}",
            "quadratic_in_trig",
        ),
    }

    def build() -> tuple[str, str, str | None]:
        form_stamp: dict[str, Any] = {}
        choice = "factor"
        if use_pc:
            from question_engine.frameworks.primitives.openstax_precalc import (
                pc_form_constraints,
                select_pc_form,
            )

            form, form_stamp = select_pc_form(
                "precalculus_trig_equations",
                d=difficulty,
                leaf_id=str(topic or ""),
            )
            cons = pc_form_constraints(form)
            choice = str(cons.get("choice") or form.get("form_id") or "factor")
            if choice not in templates:
                # Map form_id → template key
                fid = str(form.get("form_id") or "")
                if "double" in fid:
                    choice = "cos2"
                elif "quadratic" in fid:
                    choice = "factor"
                elif "factor" in fid:
                    choice = "sin2"
                else:
                    choice = random.choice(list(templates))
        else:
            choice = random.choice(list(templates))
        prompt, answer, mode = templates[choice]
        last["meta"] = {
            "primitive_engine": "trig_factoring_equations",
            "mode": mode,
            "function_classes": ["trig", "algebraic"],
            "methods_used": ["trig_equation", mode],
            **form_stamp,
        }
        return prompt, "trig factoring equation", answer if keyed else None

    def metadata_builder(_p: str, _t: str, answer: str | None) -> dict[str, Any]:
        return enrich_algebraic_meta(
            last.get("meta"),
            pack="structured_trig_equation",
            generator="trig_factoring_equations",
            methods_used=["trig_equation"],
            answer=answer,
            course_tag="pc" if use_pc else "a2",
        )

    return _make_questions(
        topic,
        count,
        keyed,
        build,
        metadata_builder=metadata_builder if use_pc else None,
        settings=settings,
    )


def _vector_3d_basics(topic: str, settings: dict) -> list[Question]:
    """Magnitude / unit direction for 3D vectors (not cross products)."""
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        components = random.choice(
            [
                (3, 4, 0),
                (2, 3, 6),
                (1, 2, 2),
                (4, 4, 7),
                (1, 4, 8),
            ]
        )
        x, y, z = components
        mag_sq = x * x + y * y + z * z
        root = int(math.isqrt(mag_sq))
        mag = str(root) if root * root == mag_sq else rf"\sqrt{{{mag_sq}}}"
        if random.choice([True, False]):
            prompt = rf"\text{{Find the magnitude of }}\langle {x},{y},{z}\rangle."
            answer = mag
        else:
            prompt = rf"\text{{Find a unit vector in the direction of }}\langle {x},{y},{z}\rangle."
            if root * root == mag_sq:
                answer = rf"\left\langle\frac{{{x}}}{{{root}}},\frac{{{y}}}{{{root}}},\frac{{{z}}}{{{root}}}\right\rangle"
            else:
                answer = rf"\left\langle\frac{{{x}}}{{\sqrt{{{mag_sq}}}}},\frac{{{y}}}{{\sqrt{{{mag_sq}}}}},\frac{{{z}}}{{\sqrt{{{mag_sq}}}}}\right\rangle"
        return prompt, "3d vector basics", answer if keyed else None

    return _make_questions(topic, count, keyed, build, settings=settings)


def _precalc_foundations(topic: str, settings: dict) -> list[Question]:
    """Generate compact exact questions for the remaining precalculus topics."""
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        n, m = random.randint(2, 6), random.randint(2, 6)
        if "circle" in topic:
            h, k, r = random.randint(-4, 4), random.randint(-4, 4), random.randint(2, 6)
            prompt, value = (
                f"\\text{{Write the equation of the circle with center }}({h},{k})"
                f"\\text{{ and radius }}{r}.",
                rf"(x-({h}))^2+(y-({k}))^2={r**2}",
            )
        elif "ellipse" in topic:
            a, b = random.randint(3, 6), random.randint(2, 5)
            prompt, value = (
                f"\\text{{Write an ellipse centered at the origin with }}a={a}\\text{{ and }}b={b}.",
                rf"\frac{{x^2}}{{{a * a}}}+\frac{{y^2}}{{{b * b}}}=1",
            )
        elif "hyperbola" in topic:
            a, b = random.randint(2, 5), random.randint(2, 5)
            prompt, value = (
                f"\\text{{Write a horizontal hyperbola centered at the origin with }}a={a}"
                f"\\text{{ and }}b={b}.",
                rf"\frac{{x^2}}{{{a * a}}}-\frac{{y^2}}{{{b * b}}}=1",
            )
        elif "parabola" in topic:
            p = random.randint(1, 5)
            prompt, value = (
                f"\\text{{Write the equation of a parabola with vertex }}(0,0)"
                f"\\text{{ and focus }}(0,{p}).",
                rf"x^2={4 * p}y",
            )
        elif "permutation" in topic:
            total = n + m
            prompt, value = (
                f"\\text{{How many ordered selections of }}{m}\\text{{ items can be made from }}"
                f"{total}\\text{{ distinct items?}}",
                str(math.factorial(total) // math.factorial(total - m)),
            )
        elif "induction" in topic:
            n0 = random.choice([1, 2])
            prompt, value = (
                rf"\text{{Verify the base case }}n={n0}\text{{ for }}"
                rf"\sum_{{k=1}}^n k=\frac{{n(n+1)}}2.",
                f"{n0}={n0}" if n0 == 1 else r"1+2=3",
            )
        elif "average_rates" in topic:
            a, b = random.randint(-3, 2), random.randint(3, 6)
            prompt, value = (
                rf"\text{{Find the average rate of change of }}f(x)=x^2\text{{ on }}[{a},{b}].",
                str(a + b),
            )
        elif "extrema_intervals" in topic:
            a = random.choice([1, 2, 3])
            prompt, value = (
                rf"\text{{Find the extrema and intervals of increase for }}f(x)={a}x^2.",
                rf"\text{{minimum }}0\text{{ at }}x=0;\ \text{{increasing on }}(0,\infty)",
            )
        elif "piecewise" in topic:
            from question_engine.settings.params import piecewise_structure_from_continuous

            structure = piecewise_structure_from_continuous(settings)
            if structure is None:
                c = random.randint(-3, 4)
                x0 = random.randint(-2, 3)
                prompt, value = (
                    rf"f(x)=\begin{{cases}}x+{c},&x<0\\{c},&x\ge0\end{{cases}}."
                    rf"\quad\text{{Evaluate }}f({x0}).",
                    str(x0 + c if x0 < 0 else c),
                )
            else:
                span = int(structure["coef_span"])
                bp_span = int(structure["breakpoint_span"])
                c = random.randint(-span, span)
                bp = random.randint(-bp_span, bp_span)
                x0 = random.randint(-bp_span - 1, bp_span + 1)
                if structure["piece_count"] >= 3:
                    c2 = random.randint(-span, span)
                    left = bp - 1
                    right = bp + 1
                    use_linear_right = bool(structure["allow_quadratic_piece"])
                    right_expr = rf"{c2}x" if use_linear_right else str(c2)
                    if x0 < left:
                        value = str(x0 + c)
                    elif x0 < right:
                        value = str(c)
                    else:
                        value = str(c2 * x0 if use_linear_right else c2)
                    prompt = (
                        rf"f(x)=\begin{{cases}}x+{c},&x<{left}\\{c},&"
                        rf"{left}\le x<{right}\\{right_expr},&x\ge{right}\end{{cases}}."
                        rf"\quad\text{{Evaluate }}f({x0})."
                    )
                elif structure["allow_quadratic_piece"] and random.random() < 0.5:
                    a = random.randint(1, max(1, span // 2))
                    value = str(a * x0 * x0 + c if x0 < bp else c)
                    prompt = (
                        rf"f(x)=\begin{{cases}}{a}x^2+{c},&x<{bp}\\{c},&x\ge{bp}"
                        rf"\end{{cases}}.\quad\text{{Evaluate }}f({x0})."
                    )
                else:
                    value = str(x0 + c if x0 < bp else c)
                    prompt = (
                        rf"f(x)=\begin{{cases}}x+{c},&x<{bp}\\{c},&x\ge{bp}"
                        rf"\end{{cases}}.\quad\text{{Evaluate }}f({x0})."
                    )
        elif "continuity" in topic:
            c = random.randint(-3, 4)
            prompt, value = (
                rf"f(x)=\begin{{cases}}x+{c},&x<0\\{c},&x\ge0\end{{cases}}."
                rf"\quad\text{{Is }}f\text{{ continuous at }}0?",
                "Yes",
            )
        elif "power_functions" in topic:
            prompt, value = (rf"\text{{Evaluate }}f(x)=x^{{{n}}}\text{{ at }}x={m}.", str(m**n))
        elif "logarithmic" in topic:
            base, shift = random.randint(2, 5), random.randint(-3, 3)
            prompt, value = (
                rf"\text{{State the vertical asymptote of }}f(x)=\log_{{{base}}}(x-({shift})).",
                f"x = {shift}",
            )
        elif "parametric" in topic:
            t = random.randint(1, 5)
            prompt, value = (
                rf"x=t^2,\ y=2t+1.\quad\text{{Find }}(x,y)\text{{ when }}t={t}.",
                f"({t * t}, {2 * t + 1})",
            )
        elif "projectile" in topic:
            v = random.randint(3, 8)
            prompt, value = (
                rf"h(t)=-16t^2+{32 * v}t.\quad\text{{Find the time of maximum height.}}",
                str(v),
            )
        elif "3d_points" in topic:
            x, y, z = (random.randint(1, 6) for _ in range(3))
            if random.random() < 0.5:
                x, y, z = random.choice([(3, 4, 12), (2, 3, 6), (1, 2, 2), (4, 4, 7)])
            dist_sq = x * x + y * y + z * z
            root = int(math.isqrt(dist_sq))
            ans = str(root) if root * root == dist_sq else rf"\sqrt{{{dist_sq}}}"
            prompt, value = (
                rf"\text{{Find the distance from }}(0,0,0)\text{{ to }}({x},{y},{z}).",
                ans,
            )
        elif "cross_products" in topic:
            a = [random.randint(-3, 3) for _ in range(3)]
            b = [random.randint(-3, 3) for _ in range(3)]
            cx = a[1] * b[2] - a[2] * b[1]
            cy = a[2] * b[0] - a[0] * b[2]
            cz = a[0] * b[1] - a[1] * b[0]
            prompt, value = (
                rf"\text{{Find }}({a[0]},{a[1]},{a[2]})\times({b[0]},{b[1]},{b[2]}).",
                rf"({cx},{cy},{cz})",
            )
        elif "3d_vectors_operations" in topic:
            # Kept for opt-out / legacy; live catalog uses vector_3d_operations (add/sub).
            a = [random.randint(-3, 3) for _ in range(3)]
            b = [random.randint(-3, 3) for _ in range(3)]
            op_add = random.choice([True, False])
            if op_add:
                c = [a[i] + b[i] for i in range(3)]
                prompt, value = (
                    rf"\text{{Find }}\langle {a[0]},{a[1]},{a[2]}\rangle+"
                    rf"\langle {b[0]},{b[1]},{b[2]}\rangle.",
                    rf"\langle {c[0]},{c[1]},{c[2]}\rangle",
                )
            else:
                c = [a[i] - b[i] for i in range(3)]
                prompt, value = (
                    rf"\text{{Find }}\langle {a[0]},{a[1]},{a[2]}\rangle-"
                    rf"\langle {b[0]},{b[1]},{b[2]}\rangle.",
                    rf"\langle {c[0]},{c[1]},{c[2]}\rangle",
                )
        elif "3d_vectors" in topic:
            # Basics fallback: magnitude
            x, y, z = random.choice([(3, 4, 0), (2, 3, 6), (1, 2, 2)])
            mag_sq = x * x + y * y + z * z
            root = int(math.isqrt(mag_sq))
            prompt, value = (
                rf"\text{{Find the magnitude of }}\langle {x},{y},{z}\rangle.",
                str(root) if root * root == mag_sq else rf"\sqrt{{{mag_sq}}}",
            )
        elif "partial_fraction" in topic:
            num = format_linear_latex(n, m)
            prompt, value = (
                rf"\text{{Decompose }}\frac{{{num}}}{{(x+1)(x+2)}}.",
                rf"\frac{{{m - n}}}{{x+1}}+\frac{{{2 * n - m}}}{{x+2}}",
            )
        elif "multivariable" in topic:
            s = random.randint(4, 9)
            z = random.randint(1, 3)
            x = (s - z) // 2
            y = x
            prompt, value = (
                rf"\text{{Solve }}x+y+z={s},\ x-y=0,\ z={z}.",
                rf"({x},{y},{z})",
            )
        elif "rational_inequalities" in topic:
            # (x-n)/(x+m) > 0 with critical points n and -m
            prompt, value = (
                rf"\frac{{x-{n}}}{{x+{m}}}>0.",
                rf"x<-{m}\text{{ or }}x>{n}",
            )
        elif "polynomial_inequalities" in topic or "inequalities" in topic:
            prompt, value = (
                rf"(x-{n})(x+{m})>0.",
                rf"x<-{m}\text{{ or }}x>{n}",
            )
        elif "rational_equations" in topic:
            prompt, value = (rf"\frac{{1}}{{x}}=\frac{{1}}{{{n}}}.", f"x = {n}")
        elif "complex_zeros" in topic:
            k = random.randint(2, 6)
            prompt, value = (rf"\text{{Find the zeros of }}x^2+{k * k}=0.", rf"x=\pm {k}i")
        elif "conjugate_roots" in topic:
            re = random.randint(1, 4)
            im = random.randint(1, 4)
            prompt, value = (
                rf"\text{{Write the monic polynomial with roots }}{re}+{im}i"
                rf"\text{{ and }}{re}-{im}i.",
                rf"x^2-{2 * re}x+{re * re + im * im}",
            )
        elif "power_series" in topic:
            c = random.choice([1, 2, 3])
            prompt, value = (
                rf"\text{{Find the radius of convergence of }}\sum_{{n=0}}^{{\infty}}({c}x)^n.",
                frac_latex(Fraction(1, c)),
            )
        elif "angles_and_angle" in topic:
            prompt, value = (
                rf"\text{{Convert }}{n * 30}^\circ\text{{ to radians.}}",
                _RADIAN_LABELS[n * 30],
            )
        elif "limits_at_essential" in topic or "essential_discontinuities" in topic:
            p = random.choice([1, 2])
            prompt, value = (rf"\lim_{{x\to0}}\frac{{1}}{{x^{{{p}}}}}", r"\text{does not exist}")
        elif "kinks" in topic or "jumps" in topic:
            c = random.randint(1, 4)
            prompt, value = (rf"\lim_{{x\to0}}|{c}x|", "0")
        elif "definition_of_the_derivative" in topic or "definition_of_derivative" in topic:
            prompt, value = (
                rf"\lim_{{h\to0}}\frac{{({n}+h)^{{2}}-{n * n}}}{{h}}",
                str(2 * n),
            )
        elif "instantaneous" in topic:
            prompt, value = (
                rf"\text{{Find }}f'({n})\text{{ for }}f(x)=x^{{2}}.",
                str(2 * n),
            )
        elif "approximating_area" in topic:
            L = 2 * n
            # Midpoint Riemann, 2 intervals, f(x)=x on [0,L] equals exact area L^2/2
            prompt, value = (
                rf"\text{{Use a midpoint Riemann sum with 2 equal intervals for }}"
                rf"f(x)=x\text{{ on }}[0,{L}].",
                frac_latex(Fraction(L * L, 2)),
            )
        elif "area_under" in topic or "limit_of_sums" in topic:
            prompt, value = (
                rf"\text{{Find the area under }}y=x\text{{ from }}0\text{{ to }}{n}.",
                frac_latex(Fraction(n * n, 2)),
            )
        elif "motion" in topic:
            prompt, value = (rf"s(t)=t^2+{n}t.\quad\text{{Find }}v(2).", str(4 + n))
        else:
            # Last-resort: still topic-shaped rather than n+m arithmetic.
            prompt, value = (
                rf"\text{{Evaluate }}f({n})\text{{ for }}f(x)=x^{{2}}.",
                str(n * n),
            )
        return prompt, topic, value if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _conic_rotation_identify(topic: str, settings: dict) -> list[Question]:
    """Identify whether an xy-term requires axis rotation, and the angle formula."""
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        a = random.randint(1, 5)
        b = random.choice([0, 2, 4, 6])
        c = random.randint(1, 5)
        # Ax^2 + Bxy + Cy^2 + ...
        if b == 0:
            ax2 = format_monomial_latex(a, degree=2) or "0"
            cy2 = format_monomial_latex(c, variable="y", degree=2) or "0"
            prompt = (
                f"\\text{{Does }} {ax2} + {cy2} = 1 "
                f"\\text{{ require a rotation of axes to eliminate an }} xy "
                f"\\text{{ term?}}"
            )
            answer = "no"
        else:
            # cot(2θ) = (A-C)/B
            ax2 = format_monomial_latex(a, degree=2) or "0"
            bxy = format_monomial_latex(b, variable="xy", degree=1) or "0"
            cy2 = format_monomial_latex(c, variable="y", degree=2) or "0"
            prompt = (
                f"\\text{{For }} {ax2} + {bxy} + {cy2} = 1,\\ "
                f"\\text{{find }} \\cot 2\\theta \\text{{ used to eliminate the }} xy "
                f"\\text{{ term.}}"
            )
            answer = f"\\frac{{{a - c}}}{{{b}}}"
        return prompt, "conic rotation", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _polar_graph_meta(
    settings: dict, *, curve: str, features: list[tuple[float, float]]
) -> dict[str, Any]:
    if not include_graph_metadata(settings):
        return {}
    x_min, x_max, y_min, y_max = origin_centered_bounds(features, settings=settings)
    answer_gs = {
        "x_min": x_min,
        "x_max": x_max,
        "y_min": y_min,
        "y_max": y_max,
        "functions": [curve] if curve else [],
        "points": [],
        "show_grid": bool(settings.get("show_grid", True)),
        "show_points": False,
    }
    return question_metadata(
        graph_spec={
            **answer_gs,
            "functions": [],
            "points": [],
            "show_points": False,
        },
        answer_graph_spec=answer_gs,
        graph_role="blank",
    )


def _polar_graphs(topic: str, settings: dict) -> list[Question]:
    """Graph / identify classic polar curves (circles, roses, cardioids, limaçons)."""
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))
    last: dict[str, Any] = {"meta": {}}

    def build() -> tuple[str, str, str | None]:
        last["meta"] = {}
        kind = random.choice(
            ["circle_cos", "circle_sin", "cardioid", "rose", "limaçon", "line_theta"]
        )
        a = random.randint(2, 5)

        if kind == "circle_cos":
            prompt = rf"r={2 * a}\cos\theta"
            answer = rf"\text{{circle, center }}({a},0),\ \text{{radius }}{a}"
            last["meta"] = _polar_graph_meta(
                settings,
                curve=f"circle({a},0,{a})",
                features=[(0, 0), (2 * a, 0), (a, a), (a, -a)],
            )
        elif kind == "circle_sin":
            prompt = rf"r={2 * a}\sin\theta"
            answer = rf"\text{{circle, center }}(0,{a}),\ \text{{radius }}{a}"
            last["meta"] = _polar_graph_meta(
                settings,
                curve=f"circle(0,{a},{a})",
                features=[(0, 0), (0, 2 * a), (a, a), (-a, a)],
            )
        elif kind == "cardioid":
            sign = random.choice(["+", "-"])
            prompt = rf"r={a}(1{sign}\cos\theta)"
            answer = r"\text{cardioid}"
            # Blank plane only — cardioid is not a cartesian function curve.
            last["meta"] = _polar_graph_meta(
                settings, curve="", features=[(0, 0), (2 * a, 0), (0, a), (0, -a)]
            )
        elif kind == "rose":
            n = random.choice([2, 3, 4])
            fn = random.choice(["cos", "sin"])
            prompt = rf"r={a}\cos({n}\theta)" if fn == "cos" else rf"r={a}\sin({n}\theta)"
            petals = 2 * n if n % 2 == 0 else n
            answer = rf"\text{{rose with }}{petals}\text{{ petals}}"
            last["meta"] = _polar_graph_meta(
                settings, curve="", features=[(a, 0), (-a, 0), (0, a), (0, -a)]
            )
        elif kind == "limaçon":
            b = random.randint(1, max(1, a - 1))
            prompt = rf"r={a}+{b}\cos\theta"
            answer = r"\text{limacon}"
            last["meta"] = _polar_graph_meta(
                settings,
                curve="",
                features=[(a + b, 0), (b - a, 0), (0, a), (0, -a)],
            )
        else:
            k = random.choice([2, 3, 4, 6])
            prompt = rf"\theta=\frac{{\pi}}{{{k}}}"
            answer = r"\text{line through the origin}"
            last["meta"] = _polar_graph_meta(
                settings, curve="", features=[(0, 0), (4, 4), (-4, -4)]
            )
        return prompt, "polar graph", answer if keyed else None

    def metadata_builder(_p: str, _t: str, _a: str | None) -> dict[str, Any]:
        return dict(last.get("meta") or {})

    return _make_questions(
        topic, count, keyed, build, metadata_builder=metadata_builder, settings=settings
    )


def _polar_rectangular_forms(topic: str, settings: dict) -> list[Question]:
    """Convert equations between polar and rectangular form."""
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        mode = random.choice(["r_to_rect_circle", "r_to_rect_line", "rect_to_polar"])
        a = random.randint(2, 6)
        if mode == "r_to_rect_circle":
            # r = 2a cos θ → (x-a)^2 + y^2 = a^2
            prompt = (
                rf"\text{{Convert }}r={2 * a}\cos\theta"
                rf"\text{{ to rectangular form.}}"
            )
            answer = rf"(x-{a})^2+y^2={a * a}"
        elif mode == "r_to_rect_line":
            prompt = rf"\text{{Convert }}r\cos\theta={a}\text{{ to rectangular form.}}"
            answer = rf"x={a}"
        else:
            prompt = (
                rf"\text{{Convert }}x^2+y^2={a * a}"
                rf"\text{{ to polar form.}}"
            )
            answer = rf"r={a}"
        return prompt, "polar rectangular forms", answer if keyed else None

    return _make_questions(topic, count, keyed, build, settings=settings)


def _polar_conic_forms(topic: str, settings: dict) -> list[Question]:
    """Identify conic type from polar form r = ed / (1 ± e cos/sin θ)."""
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        # e < 1 ellipse, e = 1 parabola, e > 1 hyperbola
        kind = random.choice(["ellipse", "parabola", "hyperbola"])
        d = random.randint(2, 6)
        trig = random.choice(["\\cos", "\\sin"])
        sign = random.choice(["+", "-"])
        if kind == "ellipse":
            # Use e = p/q with p < q
            p, q = random.choice([(1, 2), (1, 3), (2, 3), (1, 4), (3, 4)])
            e_latex = rf"\frac{{{p}}}{{{q}}}"
            num = p * d
            den = q
            prompt = rf"r=\frac{{{num}}}{{{den}{sign}{p}{trig}\theta}}"
            # Normalize display: r = (ed)/(1 ± e cos) with ed = p*d/q
            # Prefer integer numerator form already above; answer is type + e
            answer = rf"\text{{ellipse }}, e={e_latex}"
        elif kind == "parabola":
            prompt = rf"r=\frac{{{d}}}{{1{sign}{trig}\theta}}"
            answer = r"\text{parabola }, e=1"
        else:
            p, q = random.choice([(3, 2), (4, 3), (5, 2), (5, 3), (5, 4)])
            e_latex = rf"\frac{{{p}}}{{{q}}}"
            prompt = rf"r=\frac{{{p * d}}}{{{q}{sign}{p}{trig}\theta}}"
            answer = rf"\text{{hyperbola }}, e={e_latex}"
        return prompt, "polar conic", answer if keyed else None

    return _make_questions(topic, count, keyed, build, settings=settings)


def _complex_polar_form(topic: str, settings: dict) -> list[Question]:
    """Convert complex numbers between rectangular and polar (cis) form."""
    count = int(settings.get("count", 10))
    keyed = bool(settings.get("include_answer_key", False))

    exact: list[tuple[int, int, str]] = [
        (1, 0, r"\cos 0+i\sin 0"),
        (0, 1, r"\cos\frac{\pi}{2}+i\sin\frac{\pi}{2}"),
        (-1, 0, r"\cos\pi+i\sin\pi"),
        (0, -1, r"\cos\frac{3\pi}{2}+i\sin\frac{3\pi}{2}"),
        (1, 1, r"\sqrt{2}\left(\cos\frac{\pi}{4}+i\sin\frac{\pi}{4}\right)"),
        (-1, 1, r"\sqrt{2}\left(\cos\frac{3\pi}{4}+i\sin\frac{3\pi}{4}\right)"),
        (-1, -1, r"\sqrt{2}\left(\cos\frac{5\pi}{4}+i\sin\frac{5\pi}{4}\right)"),
        (1, -1, r"\sqrt{2}\left(\cos\frac{7\pi}{4}+i\sin\frac{7\pi}{4}\right)"),
    ]

    def rect_latex(a: int, b: int) -> str:
        if a == 0 and b == 1:
            return "i"
        if a == 0 and b == -1:
            return "-i"
        if b == 0:
            return str(a)
        if a == 0:
            return f"{b}i"
        imag = "i" if abs(b) == 1 else f"{abs(b)}i"
        return f"{a}+{imag}" if b > 0 else f"{a}-{imag}"

    def build() -> tuple[str, str, str | None]:
        if random.random() < 0.55:
            a, b, polar = random.choice(exact)
            prompt = rf"\text{{Write }}{rect_latex(a, b)}\text{{ in polar form.}}"
            answer = polar
        else:
            a, b, polar = random.choice(exact)
            prompt = rf"\text{{Write }}{polar}\text{{ in rectangular form.}}"
            answer = rect_latex(a, b)
        return prompt, "complex polar", answer if keyed else None

    return _make_questions(topic, count, keyed, build, settings=settings)


GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = {
    "trig_evaluate": _trig_evaluate,
    "simple_trig_equations": _simple_trig_equations,
    "trig_unit_circle": _trig_unit_circle,
    "trig_basic_identities": _trig_basic_identities,
    "log_evaluate": _log_evaluate,
    "log_change_of_base": _log_change_of_base,
    "log_equation_simple": _log_equation_simple,
    "exponential_equation_simple": _exponential_equation_simple,
    "exponential_equation_with_log": _exponential_equation_with_log,
    "sequence_arithmetic_nth_term": _sequence_arithmetic_nth_term,
    "sequence_geometric_nth_term": _sequence_geometric_nth_term,
    "sequence_arithmetic_geometric_mean": _sequence_arithmetic_geometric_mean,
    "sequence_arithmetic_series": _sequence_arithmetic_series,
    "sequence_geometric_series": _sequence_geometric_series,
    "precalc_foundations": _precalc_foundations,
    "trig_sum_difference": _trig_sum_difference,
    "trig_multiple_angle": _trig_multiple_angle,
    "trig_product_to_sum": _trig_product_to_sum,
    "trig_factoring_equations": _trig_factoring_equations,
    "vector_3d_basics": _vector_3d_basics,
    "conic_rotation_identify": _conic_rotation_identify,
    "polar_graphs": _polar_graphs,
    "polar_rectangular_forms": _polar_rectangular_forms,
    "polar_conic_forms": _polar_conic_forms,
    "complex_polar_form": _complex_polar_form,
}
