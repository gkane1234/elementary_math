"""Advanced generators: law of sines/cosines, binomial, remainder, vectors, limits extras."""

from __future__ import annotations

import math
import random
from fractions import Fraction
from typing import Callable

from ..core.models import Question
from .utils import (
    _make_questions,
    format_monomial_latex,
    format_polynomial_latex,
    frac_latex,
    random_int_range,
)


def _law_of_sines(topic: str, settings: dict) -> list[Question]:
    from question_engine.settings.params import apply_triangle_laws_continuous_knobs

    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    local = apply_triangle_laws_continuous_knobs(settings)
    side_min = int(local.get("triangle_side_min", 5))
    side_max = int(local.get("triangle_side_max", 20))
    angle_choices = tuple(local.get("triangle_angle_choices", (30, 40, 45, 50, 60, 70)))

    def build() -> tuple[str, str, str | None]:
        angle_a = random.choice(angle_choices)
        angle_b = random.choice(angle_choices)
        while angle_a + angle_b >= 170:
            angle_b = random.choice(angle_choices)
        side_a = random.randint(side_min, side_max)
        # sin B / b = sin A / a  => b = a * sin B / sin A
        b = side_a * math.sin(math.radians(angle_b)) / math.sin(math.radians(angle_a))
        prompt = (
            f"\\text{{In }} \\triangle ABC,\\ m\\angle A = {angle_a}^\\circ,\\ "
            f"m\\angle B = {angle_b}^\\circ,\\ a = {side_a}.\\ "
            f"\\text{{Find }} b \\text{{ (Law of Sines).}}"
        )
        answer = f"{b:.2f}" if include_answer_key else None
        return prompt, "law of sines", answer

    return _make_questions(topic, count, include_answer_key, build)


def _law_of_cosines(topic: str, settings: dict) -> list[Question]:
    from question_engine.settings.params import apply_triangle_laws_continuous_knobs

    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    local = apply_triangle_laws_continuous_knobs(settings)
    side_min = int(local.get("triangle_side_min", 5))
    side_max = int(local.get("triangle_side_max", 15))
    angle_choices = list(local.get("triangle_angle_choices", (40, 50, 60, 70, 80, 100, 120)))
    if not bool(local.get("allow_obtuse", True)):
        angle_choices = [a for a in angle_choices if a < 90] or [40, 50, 60, 70]

    def build() -> tuple[str, str, str | None]:
        a = random.randint(side_min, side_max)
        b = random.randint(side_min, side_max)
        angle_c = random.choice(angle_choices)
        c2 = a * a + b * b - 2 * a * b * math.cos(math.radians(angle_c))
        c = math.sqrt(max(c2, 0.01))
        prompt = (
            f"\\text{{In }} \\triangle ABC,\\ a = {a},\\ b = {b},\\ "
            f"m\\angle C = {angle_c}^\\circ.\\ \\text{{Find }} c \\text{{ (Law of Cosines).}}"
        )
        answer = f"{c:.2f}" if include_answer_key else None
        return prompt, "law of cosines", answer

    return _make_questions(topic, count, include_answer_key, build)


def _binomial_theorem(topic: str, settings: dict) -> list[Question]:
    from question_engine.settings.params import apply_polynomial_theory_continuous_knobs

    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    local = apply_polynomial_theory_continuous_knobs(settings)
    n_lo = int(local.get("binomial_n_min", 3))
    n_hi = int(local.get("binomial_n_max", 6))
    a_max = int(local.get("binomial_a_max", 4))

    def build() -> tuple[str, str, str | None]:
        n = random.randint(max(3, n_lo), max(3, n_hi))
        a = random.randint(1, max(1, a_max))
        k = random.randint(1, n - 1)
        # Coefficient of x^k in (a+x)^n is C(n,k) * a^(n-k)
        from math import comb

        coef = comb(n, k) * (a ** (n - k))
        prompt = (
            f"\\text{{Find the coefficient of }} x^{{{k}}} "
            f"\\text{{ in }} ({a} + x)^{{{n}}}."
        )
        answer = str(coef) if include_answer_key else None
        return prompt, "binomial theorem", answer

    return _make_questions(topic, count, include_answer_key, build)


def _remainder_theorem(topic: str, settings: dict) -> list[Question]:
    from question_engine.settings.params import apply_polynomial_theory_continuous_knobs

    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    local = apply_polynomial_theory_continuous_knobs(settings)
    coef_lo = int(local.get("poly_theory_coef_min", -6))
    coef_hi = int(local.get("poly_theory_coef_max", 6))
    span = int(local.get("root_span", 5))

    def build() -> tuple[str, str, str | None]:
        # p(x) = x^2 + bx + c, divide by (x - a), remainder p(a)
        b = random_int_range(coef_lo, coef_hi, exclude={0})
        c = random_int_range(coef_lo, coef_hi, exclude={0})
        a = random_int_range(-span, span, exclude={0})
        rem = a * a + b * a + c
        prompt = (
            f"\\text{{Find the remainder when }} {format_polynomial_latex([1, b, c])} "
            f"\\text{{ is divided by }} (x - {a})."
        )
        answer = str(rem) if include_answer_key else None
        return prompt, "remainder theorem", answer

    return _make_questions(topic, count, include_answer_key, build)


def _compound_interest(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    from question_engine.frameworks.difficulty_budget import settings_difficulty_band
    from question_engine.settings.params import compound_interest_structure_from_continuous

    structure = compound_interest_structure_from_continuous(settings)
    if structure is None:
        band = settings_difficulty_band(settings, default=8.0)
        structure = {
            "band": band,
            "principals": {
                "easy": (500, 1000, 1500, 2000),
                "medium": (1000, 1500, 2000, 2500),
                "hard": (1000, 2000, 2500, 5000, 8000),
            }[band],
            "rates": {
                "easy": (3, 4, 5, 6, 8),
                "medium": (3, 4, 5, 6, 8),
                "hard": (3, 4, 5, 6, 7, 8, 9, 12),
            }[band],
            "t_min": {"easy": 2, "medium": 2, "hard": 4}[band],
            "t_max": {"easy": 4, "medium": 6, "hard": 10}[band],
            "n_choices": {
                "easy": (1,),
                "medium": (1, 2, 4),
                "hard": (2, 4, 12),
            }[band],
            "allow_interest_question": band != "easy",
        }

    def build() -> tuple[str, str, str | None]:
        p = random.choice(structure["principals"])
        r = random.choice(structure["rates"])
        t = random.randint(int(structure["t_min"]), int(structure["t_max"]))
        n = random.choice(structure["n_choices"])

        amount = p * (1 + r / (100 * n)) ** (n * t)
        interest = amount - p
        years = "year" if t == 1 else "years"
        freq = {1: "annually", 2: "semiannually", 4: "quarterly", 12: "monthly"}[n]
        find_interest = bool(structure.get("allow_interest_question")) and random.random() < 0.4

        if n == 1:
            core = (
                f"\\text{{An account starts with }} \\${p} \\text{{ and earns }} "
                f"{r}\\% \\text{{ interest compounded annually for }} {t} "
                f"\\text{{ {years}.}}"
            )
        else:
            core = (
                f"\\text{{An account starts with }} \\${p} \\text{{ at }} {r}\\% "
                f"\\text{{ interest compounded {freq} for }} {t} "
                f"\\text{{ {years}.}}"
            )

        if find_interest:
            prompt = core + " \\text{ How much interest is earned?}"
            answer_val = interest
        else:
            prompt = core + " \\text{ What is the ending balance?}"
            answer_val = amount

        answer = f"{answer_val:.2f}" if include_answer_key else None
        if answer is not None:
            answer = f"\\${answer}"
        return prompt, "compound interest", answer

    return _make_questions(topic, count, include_answer_key, build)


def _writing_numeric_complexity_from_continuous(settings: dict) -> tuple[str, int] | None:
    """Map continuous difficulty → (expression_complexity, num_max).

    Returns None when continuous ``difficulty`` is absent so EMH presets win.
    """
    if "difficulty" not in settings or settings["difficulty"] is None:
        return None
    try:
        d = float(settings["difficulty"])
    except (TypeError, ValueError):
        return None
    if d < 3.0:
        return "simple", 10
    if d < 8.0:
        return "simple" if random.random() < 0.5 else "standard", 12
    if d < 14.0:
        return "standard", 15
    if d < 20.0:
        return "standard" if random.random() < 0.4 else "advanced", 18
    return "advanced", 20


def _writing_numeric_expressions(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    local = dict(settings)
    mapped = _writing_numeric_complexity_from_continuous(local)
    if mapped is not None:
        complexity, num_hi = mapped
        local["expression_complexity"] = complexity
        local.setdefault("num_min", 2)
        local["num_max"] = max(int(local.get("num_min", 2)), num_hi)
    complexity = str(local.get("expression_complexity", "standard"))
    lo = max(1, int(local.get("num_min", 2)))
    hi = max(lo, int(local.get("num_max", 20)))

    def _n(cap: int | None = None) -> int:
        upper = min(hi, cap) if cap is not None else hi
        return random.randint(lo, max(lo, upper))

    def simple_forms() -> list[tuple[str, str]]:
        a, b = _n(), _n()
        return [
            (
                f"\\text{{Write an expression for }} {a} \\text{{ more than }} {b}.",
                f"{b} + {a}",
            ),
            (
                f"\\text{{Write an expression for }} {a} \\text{{ less than }} {b}.",
                f"{b} - {a}",
            ),
            (
                f"\\text{{Write an expression for the sum of }} {a} \\text{{ and }} {b}.",
                f"{a} + {b}",
            ),
            (
                f"\\text{{Write an expression for the difference of }} {a} \\text{{ and }} {b}.",
                f"{a} - {b}",
            ),
            (
                f"\\text{{Write an expression for the product of }} {a} \\text{{ and }} {b}.",
                f"{a} \\cdot {b}",
            ),
            (
                f"\\text{{Write an expression for }} {a} \\text{{ times }} {b}.",
                f"{a} \\cdot {b}",
            ),
            (
                f"\\text{{Write an expression for }} {a} \\text{{ increased by }} {b}.",
                f"{a} + {b}",
            ),
            (
                f"\\text{{Write an expression for }} {a} \\text{{ decreased by }} {b}.",
                f"{a} - {b}",
            ),
            (
                f"\\text{{Write an expression for twice }} {a}.",
                f"2 \\cdot {a}",
            ),
            (
                f"\\text{{Write an expression for the quotient of }} {a} \\text{{ and }} {b}.",
                f"{a} \\div {b}",
            ),
        ]

    def standard_forms() -> list[tuple[str, str]]:
        a, b, c = _n(12), _n(12), _n(9)
        return [
            (
                f"\\text{{Write an expression for }} {a} \\text{{ times the sum of }} {b} "
                f"\\text{{ and }} {c}.",
                f"{a}({b} + {c})",
            ),
            (
                f"\\text{{Write an expression for }} {a} \\text{{ times the difference of }} {b} "
                f"\\text{{ and }} {c}.",
                f"{a}({b} - {c})",
            ),
            (
                f"\\text{{Write an expression for the sum of }} {a} \\text{{ and the product of }} "
                f"{b} \\text{{ and }} {c}.",
                f"{a} + {b} \\cdot {c}",
            ),
            (
                f"\\text{{Write an expression for the product of }} {a} \\text{{ and the sum of }} "
                f"{b} \\text{{ and }} {c}.",
                f"{a}({b} + {c})",
            ),
            (
                f"\\text{{Write an expression for }} {a} \\text{{ more than the product of }} "
                f"{b} \\text{{ and }} {c}.",
                f"{b} \\cdot {c} + {a}",
            ),
            (
                f"\\text{{Write an expression for }} {a} \\text{{ less than the product of }} "
                f"{b} \\text{{ and }} {c}.",
                f"{b} \\cdot {c} - {a}",
            ),
            (
                f"\\text{{Write an expression for the quotient of the sum of }} {a} \\text{{ and }} "
                f"{b}\\text{{, and }} {c}.",
                f"({a} + {b}) \\div {c}",
            ),
            (
                f"\\text{{Write an expression for }} {a} \\text{{ times the quantity of }} {b} "
                f"\\text{{ plus }} {c}.",
                f"{a}({b} + {c})",
            ),
            (
                f"\\text{{Write an expression for the difference of }} {a} \\text{{ and the "
                f"product of }} {b} \\text{{ and }} {c}.",
                f"{a} - {b} \\cdot {c}",
            ),
            (
                f"\\text{{Write an expression for }} {c} \\text{{ groups of the sum of }} {a} "
                f"\\text{{ and }} {b}.",
                f"{c}({a} + {b})",
            ),
        ]

    def advanced_forms() -> list[tuple[str, str]]:
        a, b, c = _n(10), _n(10), _n(8)
        return [
            (
                f"\\text{{Write an expression for the square of }} {a}.",
                f"{a}^{{2}}",
            ),
            (
                f"\\text{{Write an expression for }} {a} \\text{{ squared plus }} {b}.",
                f"{a}^{{2}} + {b}",
            ),
            (
                f"\\text{{Write an expression for the product of }} {a} \\text{{ squared and }} {b}.",
                f"{a}^{{2}} \\cdot {b}",
            ),
            (
                f"\\text{{Write an expression for }} {a} \\text{{ times the square of }} {b}.",
                f"{a} \\cdot {b}^{{2}}",
            ),
            (
                f"\\text{{Write an expression for the sum of }} {a} \\text{{ squared and }} "
                f"{b} \\text{{ squared.}}",
                f"{a}^{{2}} + {b}^{{2}}",
            ),
            (
                f"\\text{{Write an expression for the square of the sum of }} {a} \\text{{ and }} {b}.",
                f"({a} + {b})^{{2}}",
            ),
            (
                f"\\text{{Write an expression for }} {a} \\text{{ times the quantity }} {b} "
                f"\\text{{ squared plus }} {c}.",
                f"{a}({b}^{{2}} + {c})",
            ),
            (
                f"\\text{{Write an expression for the sum of }} {a} \\text{{ cubed and }} {b}.",
                f"{a}^{{3}} + {b}",
            ),
            (
                f"\\text{{Write an expression for }} {a} \\text{{ more than }} {b} \\text{{ squared.}}",
                f"{b}^{{2}} + {a}",
            ),
            (
                f"\\text{{Write an expression for the product of the sum of }} {a} \\text{{ and }} "
                f"{b}\\text{{, and }} {c} \\text{{ squared.}}",
                f"({a} + {b}) \\cdot {c}^{{2}}",
            ),
        ]

    if complexity == "simple":
        pool_builders = [simple_forms]
    elif complexity == "advanced":
        # Prefer multi-operation and exponent phrase shapes on hard.
        pool_builders = [standard_forms, advanced_forms, advanced_forms]
    else:
        pool_builders = [simple_forms, standard_forms]

    def build() -> tuple[str, str, str | None]:
        forms: list[tuple[str, str]] = []
        for builder in pool_builders:
            forms.extend(builder())
        prompt, expr = random.choice(forms)
        answer = expr if include_answer_key else None
        return prompt, "writing numeric expression", answer

    return _make_questions(
        topic,
        count,
        include_answer_key,
        build,
        metadata={"skeleton_pattern": "WriteNumeric", "primitive_engine": "number"},
        settings=local,
    )


def _decimal_divide(topic: str, settings: dict) -> list[Question]:
    from ..frameworks.number import DecimalDivideByDecimalFramework

    return DecimalDivideByDecimalFramework().generate_batch(topic, settings)


def _vector_basics(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        a1, a2 = random.randint(-5, 5), random.randint(-5, 5)
        b1, b2 = random.randint(-5, 5), random.randint(-5, 5)
        op = random.choice(["add", "subtract", "magnitude"])
        if op == "add":
            prompt = (
                f"\\text{{Find }} \\langle {a1}, {a2} \\rangle + "
                f"\\langle {b1}, {b2} \\rangle."
            )
            answer = f"\\langle {a1 + b1}, {a2 + b2} \\rangle"
        elif op == "subtract":
            prompt = (
                f"\\text{{Find }} \\langle {a1}, {a2} \\rangle - "
                f"\\langle {b1}, {b2} \\rangle."
            )
            answer = f"\\langle {a1 - b1}, {a2 - b2} \\rangle"
        else:
            prompt = f"\\text{{Find }} \\lVert \\langle {a1}, {a2} \\rangle \\rVert."
            mag = math.sqrt(a1 * a1 + a2 * a2)
            answer = f"{mag:.3g}" if mag != int(mag) else str(int(mag))
        return prompt, f"vector {op}", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _vector_diagrams(topic: str, settings: dict) -> list[Question]:
    """Tip-to-tail / resultant from described vector diagrams (text until UI)."""
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        a1, a2 = random.randint(-6, 6), random.randint(-6, 6)
        b1, b2 = random.randint(-6, 6), random.randint(-6, 6)
        while a1 == 0 and a2 == 0:
            a1, a2 = random.randint(-6, 6), random.randint(-6, 6)
        while b1 == 0 and b2 == 0:
            b1, b2 = random.randint(-6, 6), random.randint(-6, 6)
        mode = random.choice(["resultant", "resultant_mag", "opposite"])
        if mode == "resultant":
            prompt = (
                f"\\text{{The diagram shows }} \\langle {a1}, {a2} \\rangle "
                f"\\text{{ tip-to-tail with }} \\langle {b1}, {b2} \\rangle. "
                f"\\text{{Find the resultant vector.}}"
            )
            answer = f"\\langle {a1 + b1}, {a2 + b2} \\rangle"
            topic_key = "vector diagram resultant"
        elif mode == "resultant_mag":
            rx, ry = a1 + b1, a2 + b2
            mag = math.sqrt(rx * rx + ry * ry)
            prompt = (
                f"\\text{{On the tip-to-tail diagram, }} \\langle {a1}, {a2} \\rangle "
                f"\\text{{ is followed by }} \\langle {b1}, {b2} \\rangle. "
                f"\\text{{Find the magnitude of the resultant.}}"
            )
            answer = f"{mag:.3g}" if mag != int(mag) else str(int(mag))
            topic_key = "vector diagram magnitude"
        else:
            prompt = (
                f"\\text{{The diagram shows vector }} \\mathbf{{u}} = "
                f"\\langle {a1}, {a2} \\rangle.\\ "
                f"\\text{{Find the opposite vector }} -\\mathbf{{u}}."
            )
            answer = f"\\langle {-a1}, {-a2} \\rangle"
            topic_key = "vector diagram opposite"
        return prompt, topic_key, answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _dot_product(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        a1, a2 = random.randint(-6, 6), random.randint(-6, 6)
        b1, b2 = random.randint(-6, 6), random.randint(-6, 6)
        prompt = (
            f"\\text{{Find }} \\langle {a1}, {a2} \\rangle \\cdot "
            f"\\langle {b1}, {b2} \\rangle."
        )
        answer = str(a1 * b1 + a2 * b2) if include_answer_key else None
        return prompt, "dot product", answer

    return _make_questions(topic, count, include_answer_key, build)


def _polar_coordinates(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        r = random.randint(2, 10)
        theta = random.choice([0, 30, 45, 60, 90, 120, 135, 150, 180])
        x = r * math.cos(math.radians(theta))
        y = r * math.sin(math.radians(theta))
        prompt = (
            f"\\text{{Convert }} ({r}, {theta}^\\circ) "
            f"\\text{{ from polar to rectangular coordinates.}}"
        )
        answer = f"({x:.2f}, {y:.2f})" if include_answer_key else None
        return prompt, "polar to rectangular", answer

    return _make_questions(topic, count, include_answer_key, build)


def _limit_removable(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        a = random.randint(1, 6)
        # lim x->a of (x^2 - a^2)/(x - a) = 2a
        prompt = (
            f"\\lim_{{x \\to {a}}} \\frac{{x^{{2}} - {a * a}}}{{x - {a}}}"
        )
        answer = str(2 * a) if include_answer_key else None
        return prompt, "removable discontinuity limit", answer

    return _make_questions(topic, count, include_answer_key, build)


def _related_rates_simple(topic: str, settings: dict) -> list[Question]:
    """Related rates via OpenStax §4.1 frames (circle / balloon / ladder / …)."""
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    from question_engine.frameworks.primitives.related_rates_frames import (
        sample_related_rates_frame,
    )
    from question_engine.settings.params import calc_application_structure_from_continuous

    structure = calc_application_structure_from_continuous(settings)

    def build() -> tuple[str, str, str | None]:
        if structure is None:
            frames: tuple[str, ...] = ("expanding_circle",)
            r_max, rate_max = 10, 5
        else:
            raw = structure.get("related_frames") or structure.get("related_shapes") or (
                "expanding_circle",
            )
            legacy = {
                "circle": "expanding_circle",
                "sphere": "expanding_sphere",
                "cone": "cone_similar",
            }
            frames = tuple(legacy.get(str(f), str(f)) for f in raw)
            r_max = max(3, int(structure["radius_max"]))
            rate_max = max(1, int(structure["rate_max"]))
        item = sample_related_rates_frame(
            random,
            frames=frames,
            r_max=r_max,
            rate_max=rate_max,
        )
        build._last_meta = {  # type: ignore[attr-defined]
            "frame_id": item.frame_id,
            "related_rates_frame": item.frame_id,
            **item.metadata,
        }
        answer = item.answer_latex if include_answer_key else None
        return item.prompt_latex, item.label, answer

    def _sketch_meta(prompt_latex: str, prompt_text: str, answer: str | None) -> dict:
        from question_engine.diagrams.figure_families import sample_figure_from_settings

        sample = sample_figure_from_settings(
            "function_sketch",
            settings,
            features=["curve", "related_rates_circle", "related_rates_ladder"],
            curve_kind="parabola",
        )
        extras = sample.to_metadata_extras()
        extras.update(getattr(build, "_last_meta", {}) or {})
        return extras

    return _make_questions(
        topic,
        count,
        include_answer_key,
        build,
        metadata_builder=_sketch_meta,
        settings=settings,
    )


def _derivative_ln_exp(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        if random.choice([True, False]):
            n = random.randint(2, 5)
            prompt = f"\\frac{{d}}{{dx}}\\left[\\ln(x^{{{n}}})\\right]"
            answer = f"\\frac{{{n}}}{{x}}"
        else:
            k = random.randint(2, 5)
            prompt = f"\\frac{{d}}{{dx}}\\left[e^{{{k}x}}\\right]"
            answer = f"{k}e^{{{k}x}}"
        return prompt, "ln/exp derivative", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _intervals_increase_decrease(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        # f(x) = x^2 + bx + c → critical point at x = -b/2
        b = random_int_range(-8, 8, exclude={0})
        c = random.randint(-5, 5)
        crit = -b / 2
        sign_b = f"+ {b}x" if b > 0 else f"- {-b}x"
        sign_c = f"+ {c}" if c > 0 else (f"- {-c}" if c < 0 else "")
        prompt = (
            f"\\text{{Find the intervals where }} f(x) = x^{{2}} {sign_b}{sign_c} "
            f"\\text{{ is increasing.}}"
        )
        answer = f"({crit:g}, \\infty)" if include_answer_key else None
        return prompt, "intervals of increase", answer

    return _make_questions(topic, count, include_answer_key, build)


def _lhopitals_rule(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    def build() -> tuple[str, str, str | None]:
        a = random.randint(2, 6)
        # lim x->0 (sin(ax))/x = a
        arg = format_monomial_latex(a) or "0"
        prompt = f"\\lim_{{x \\to 0}} \\frac{{\\sin({arg})}}{{x}}"
        answer = str(a) if include_answer_key else None
        return prompt, "lhopital / standard limit", answer

    return _make_questions(topic, count, include_answer_key, build)


def _area_between_curves(topic: str, settings: dict) -> list[Question]:
    """Area between curves — OpenStax Calc Vol 1 §6.1 shapes (∫(top−bottom))."""
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))
    from question_engine.settings.params import calc_application_structure_from_continuous

    structure = calc_application_structure_from_continuous(settings)
    x = str(settings.get("variable", "x"))
    d = float(settings.get("difficulty", 8.0) or 8.0)
    if structure is not None:
        band = str(structure.get("band") or "easy")
        bound_max = max(2, int(structure.get("bound_max", 4)))
    else:
        band = "easy" if d < 8 else ("medium" if d < 16 else "hard")
        bound_max = 4 if d < 8 else (5 if d < 16 else 6)

    def build() -> tuple[str, str, str | None]:
        b = random.randint(2, bound_max)
        if band == "easy":
            # y=x above y=0 on [0,b]
            prompt = (
                rf"\text{{Find the area between }}y={x}\text{{ and }}y=0"
                rf"\text{{ from }}{x}=0\text{{ to }}{x}={b}."
            )
            answer = frac_latex(Fraction(b * b, 2))
        elif band == "medium":
            if random.choice([True, False]):
                # y=x^2 above y=0
                prompt = (
                    rf"\text{{Find the area between }}y={x}^{{2}}\text{{ and }}y=0"
                    rf"\text{{ from }}{x}=0\text{{ to }}{x}={b}."
                )
                answer = frac_latex(Fraction(b**3, 3))
            else:
                # horizontal line above y=x on [0,k] where they meet at x=k
                k = random.randint(2, max(2, min(5, bound_max)))
                prompt = (
                    rf"\text{{Find the area of the region bounded by }}"
                    rf"y={k},\ y={x},\text{{ and }}{x}=0."
                )
                # ∫_0^k (k-x) dx = k^2/2
                answer = frac_latex(Fraction(k * k, 2))
        else:
            # classic: y=x and y=x^2 on [0,1] (or scale)
            if random.choice([True, False]):
                prompt = (
                    rf"\text{{Find the area of the region bounded by }}"
                    rf"y={x}\text{{ and }}y={x}^{{2}}."
                )
                answer = frac_latex(Fraction(1, 6))
            else:
                k = random.randint(2, 4)
                # y=k-x and y=0 from 0 to k
                prompt = (
                    rf"\text{{Find the area between }}y={k}-{x}\text{{ and }}y=0"
                    rf"\text{{ from }}{x}=0\text{{ to }}{x}={k}."
                )
                answer = frac_latex(Fraction(k * k, 2))
        return prompt, "area between curves", answer if include_answer_key else None

    return _make_questions(topic, count, include_answer_key, build)


def _inverse_trig_functions(topic: str, settings: dict) -> list[Question]:
    count = int(settings.get("count", 10))
    include_answer_key = bool(settings.get("include_answer_key", False))

    values = {
        ("arcsin", "0"): "0",
        ("arcsin", r"\frac{1}{2}"): r"\frac{\pi}{6}",
        ("arcsin", r"\frac{\sqrt{2}}{2}"): r"\frac{\pi}{4}",
        ("arcsin", "1"): r"\frac{\pi}{2}",
        ("arccos", "0"): r"\frac{\pi}{2}",
        ("arccos", r"\frac{1}{2}"): r"\frac{\pi}{3}",
        ("arctan", "0"): "0",
        ("arctan", "1"): r"\frac{\pi}{4}",
    }

    def build() -> tuple[str, str, str | None]:
        (fn, arg), val = random.choice(list(values.items()))
        prompt = f"\\{fn}\\left({arg}\\right)"
        answer = val if include_answer_key else None
        return prompt, "inverse trig", answer

    return _make_questions(topic, count, include_answer_key, build)


GENERATORS: dict[str, Callable[[str, dict], list[Question]]] = {
    "law_of_sines": _law_of_sines,
    "law_of_cosines": _law_of_cosines,
    "binomial_theorem": _binomial_theorem,
    "remainder_theorem": _remainder_theorem,
    "compound_interest": _compound_interest,
    "writing_numeric_expressions": _writing_numeric_expressions,
    "g6_decimal_divide": _decimal_divide,
    "vector_basics": _vector_basics,
    "vector_diagrams": _vector_diagrams,
    "dot_product": _dot_product,
    "polar_coordinates": _polar_coordinates,
    "limit_removable": _limit_removable,
    "related_rates_simple": _related_rates_simple,
    "derivative_ln_exp": _derivative_ln_exp,
    "intervals_increase_decrease": _intervals_increase_decrease,
    "lhopitals_rule": _lhopitals_rule,
    "area_between_curves": _area_between_curves,
    "inverse_trig_functions": _inverse_trig_functions,
}
